---
name: dynamic-t-score-spec
description: Technical specification for dynamic T-Score calculation
version: "3.0.0"
---

# Dynamic T-Score Technical Specification

## Overview

T-Score (Typicality Score) measures how commonly a theoretical framework is used in a specific research domain. Dynamic T-Score calculation augments static reference values with real-time publication data.

## Calculation Formula

```
T_dynamic = T_base + M_recency + M_domain + M_trend

Where:
  T_base ∈ [0.0, 1.0]     # From static reference table
  M_recency ∈ [-0.15, +0.15]  # 3-year usage trend
  M_domain ∈ [-0.10, +0.10]   # Domain-specific adjustment
  M_trend ∈ [-0.10, +0.10]    # Popularity trajectory

Final T-Score is clamped to [0.0, 1.0]
```

## Mode Specifications

### Static Mode

```yaml
mode: static
source: "references/VS-Research-Framework.md tables"
latency: 0ms
reliability: 100%
use_when:
  - Offline operation required
  - Speed is critical
  - API unavailable
  - Testing/development
```

**Static Table Example**:
```yaml
# From VS-Research-Framework.md
static_t_scores:
  education:
    TAM: 0.85
    UTAUT: 0.75
    SCT: 0.70
    SDT: 0.65
    TPB: 0.60
    ACT: 0.40

  psychology:
    SCT: 0.90
    SDT: 0.85
    TPB: 0.80
    ACT: 0.55
    TAM: 0.35

  HRD:
    TAM: 0.80
    JD-R: 0.75
    SCT: 0.70
    SDT: 0.60
    UTAUT: 0.55
```

### Dynamic Mode

```yaml
mode: dynamic
source: "Semantic Scholar API + OpenAlex API"
latency: 500-2000ms
reliability: ~95% (API dependent)
use_when:
  - Accuracy is critical
  - Recent trends matter
  - Novel domain exploration
  - Publication preparation
```

**Dynamic Calculation Flow**:
```
1. Receive (theory, domain) query
2. Query Semantic Scholar for recent papers
3. Query OpenAlex for publication counts
4. Calculate M_recency from 3-year trend
5. Apply M_domain from domain modifiers
6. Calculate M_trend from growth rate
7. Combine: T_dynamic = T_base + modifiers
8. Clamp to [0.0, 1.0]
9. Cache result
```

### Hybrid Mode (Recommended)

```yaml
mode: hybrid
source: "Static base + API adjustments (cached)"
latency: 0-500ms (cached hits)
reliability: ~99% (static fallback)
use_when:
  - Production use
  - Balance of speed and accuracy
  - Intermittent connectivity
```

**Hybrid Logic**:
```python
def get_t_score_hybrid(theory: str, domain: str) -> float:
    cache_key = f"{theory}:{domain}"

    # Check cache first
    if cache.has(cache_key) and not cache.expired(cache_key):
        return cache.get(cache_key)

    # Get static base
    t_base = get_static_t_score(theory, domain)

    # Try dynamic adjustment
    try:
        modifiers = calculate_dynamic_modifiers(theory, domain)
        t_dynamic = clamp(t_base + sum(modifiers), 0.0, 1.0)
        cache.set(cache_key, t_dynamic, ttl=86400)  # 24h
        return t_dynamic
    except APIError:
        # Fallback to static
        return t_base
```

## API Configuration

### Semantic Scholar

```yaml
semantic_scholar:
  base_url: "https://api.semanticscholar.org/graph/v1"

  endpoints:
    paper_search: "/paper/search"
    paper_details: "/paper/{paper_id}"

  query_template: |
    query={theory}+AND+{domain}
    &year={year_start}-{year_end}
    &fields=title,year,citationCount,fieldsOfStudy
    &limit=100

  headers:
    x-api-key: "${SEMANTIC_SCHOLAR_API_KEY}"  # Optional but recommended

  rate_limits:
    without_key: 100/5min
    with_key: 100/1min

  timeout: 5000ms
  retry:
    max_attempts: 3
    backoff: exponential
    initial_delay: 1000ms
```

**Example Query**:
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/search?\
query=Technology+Acceptance+Model+AND+education&\
year=2021-2024&\
fields=title,year,citationCount&\
limit=100"
```

### OpenAlex

```yaml
openalex:
  base_url: "https://api.openalex.org"

  endpoints:
    works: "/works"
    concepts: "/concepts"

  query_template: |
    filter=title.search:{theory},
           publication_year:{year_start}-{year_end},
           concepts.display_name.search:{domain}
    &per_page=100

  headers:
    mailto: "${OPENALEX_EMAIL}"  # Polite pool access

  rate_limits:
    impolite: 10/second
    polite: 100/second

  timeout: 5000ms
  retry:
    max_attempts: 3
    backoff: linear
    delay: 1000ms
```

**Example Query**:
```bash
curl "https://api.openalex.org/works?\
filter=title.search:Technology%20Acceptance%20Model,\
publication_year:2021-2024&\
mailto=research@example.com&\
per_page=100"
```

## Modifier Calculations

### Recency Modifier (M_recency)

Measures change in framework usage over recent years.

```python
def calc_recency_modifier(theory: str, domain: str) -> float:
    """
    Calculate recency modifier based on 3-year publication trend.

    Returns: float in range [-0.15, +0.15]
    """
    current_year = datetime.now().year

    # Get publication counts
    recent_count = query_papers(
        theory=theory,
        domain=domain,
        year_start=current_year - 2,
        year_end=current_year
    ).count

    historical_count = query_papers(
        theory=theory,
        domain=domain,
        year_start=current_year - 10,
        year_end=current_year - 3
    ).count

    # Calculate average annual rate
    historical_avg = historical_count / 7  # 7 years of history
    recent_avg = recent_count / 3          # 3 recent years

    # Calculate ratio
    ratio = recent_avg / max(historical_avg, 1)

    # Map to modifier range
    if ratio > 1.5:
        # Growing significantly → more modal
        return min(0.15, (ratio - 1.0) * 0.1)
    elif ratio < 0.5:
        # Declining significantly → less modal
        return max(-0.15, (ratio - 1.0) * 0.1)
    else:
        # Stable
        return 0.0
```

**Recency Modifier Table**:

| Ratio | Interpretation | Modifier |
|-------|---------------|----------|
| > 2.0 | Rapidly growing | +0.15 |
| 1.5 - 2.0 | Growing | +0.05 to +0.15 |
| 0.8 - 1.5 | Stable | 0.0 |
| 0.5 - 0.8 | Declining | -0.05 to 0.0 |
| < 0.5 | Rapidly declining | -0.15 |

### Domain Modifier (M_domain)

Pre-defined adjustments for theory-domain combinations.

```yaml
domain_modifiers:
  education:
    TAM: +0.05      # Very common in ed-tech
    SDT: -0.05      # Less common than psychology
    UTAUT: +0.03    # Growing in education
    SCT: 0.0        # Baseline
    ACT: -0.08      # Rare in education

  psychology:
    SCT: +0.05      # Core psychology theory
    SDT: +0.05      # Core psychology theory
    ACT: -0.10      # More theoretical
    TAM: -0.05      # Borrowed from IS

  HRD:
    TAM: +0.10      # Very dominant
    JD-R: +0.05     # Core HRD theory
    SCT: -0.03      # Less common than education
    SDT: -0.05      # Emerging in HRD

  information_systems:
    TAM: +0.10      # Foundational
    UTAUT: +0.08    # Core IS theory
    TPB: +0.03      # Common
    SCT: -0.05      # Borrowed from psychology

  healthcare:
    TPB: +0.05      # Common in health behavior
    SCT: +0.03      # Used for patient education
    TAM: 0.0        # Growing in health IT
    UTAUT: -0.03    # Less common
```

### Trend Modifier (M_trend)

Calculates trajectory of framework popularity.

```python
def calc_trend_modifier(theory: str, domain: str) -> float:
    """
    Calculate trend modifier using linear regression on yearly counts.

    Returns: float in range [-0.10, +0.10]
    """
    current_year = datetime.now().year

    # Get yearly counts for past 5 years
    year_counts = []
    for year in range(current_year - 4, current_year + 1):
        count = query_papers(
            theory=theory,
            domain=domain,
            year_start=year,
            year_end=year
        ).count
        year_counts.append((year, count))

    # Calculate linear regression slope
    slope = linear_regression(year_counts).slope

    # Normalize slope (papers per year)
    normalized_slope = slope / max(year_counts[-1][1], 10)

    # Map to modifier
    if normalized_slope > 0.2:
        return +0.10   # Rising rapidly
    elif normalized_slope > 0.1:
        return +0.05   # Rising
    elif normalized_slope > -0.1:
        return 0.0     # Stable
    elif normalized_slope > -0.2:
        return -0.05   # Declining
    else:
        return -0.10   # Declining rapidly
```

**Trend Interpretation**:

| Slope | Pattern | Modifier | Recommendation |
|-------|---------|----------|----------------|
| > +20%/yr | Rapid growth | +0.10 | Highly modal, safe choice |
| +10-20%/yr | Growth | +0.05 | Modal, good choice |
| -10 to +10%/yr | Stable | 0.0 | Established, reliable |
| -10 to -20%/yr | Decline | -0.05 | Consider alternatives |
| < -20%/yr | Rapid decline | -0.10 | May face skepticism |

## Cache Strategy

```yaml
cache:
  type: "LRU (Least Recently Used)"

  settings:
    max_entries: 1000
    default_ttl: 86400  # 24 hours
    storage: "in-memory"

  key_format: "{theory}:{domain}:{mode}"

  invalidation:
    - manual: "cache.invalidate(key)"
    - ttl_expired: "automatic"
    - api_update: "on significant change detected"

  persistence:
    enabled: false  # Memory-only by default
    file: ".cache/t_scores.json"  # Optional persistence
```

**Cache Implementation**:
```python
class TScoreCache:
    def __init__(self, max_size: int = 1000, ttl: int = 86400):
        self._cache = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl

    def get(self, key: str) -> Optional[float]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() - entry["timestamp"] < self._ttl:
                # Move to end (most recently used)
                self._cache.move_to_end(key)
                return entry["value"]
            else:
                # Expired
                del self._cache[key]
        return None

    def set(self, key: str, value: float):
        if len(self._cache) >= self._max_size:
            # Remove oldest
            self._cache.popitem(last=False)
        self._cache[key] = {
            "value": value,
            "timestamp": time.time()
        }
```

## Error Handling

| Error | Detection | Action | Fallback |
|-------|-----------|--------|----------|
| API timeout | No response in 5s | Log, retry 3x | Static mode |
| Rate limit (429) | HTTP 429 | Wait 60s, retry | Cached or static |
| Invalid query | Malformed response | Log warning | Static mode |
| No results | Empty result set | Use base only | T_base + 0.0 |
| Network error | Connection failed | Log, use cache | Static mode |
| Parse error | JSON decode fail | Log error | Static mode |

**Error Handling Implementation**:
```python
def get_t_score_with_fallback(theory: str, domain: str, mode: str) -> float:
    """Get T-Score with comprehensive error handling."""

    # Always get static base
    t_base = get_static_t_score(theory, domain)

    if mode == "static":
        return t_base

    try:
        # Attempt dynamic calculation
        m_recency = calc_recency_modifier(theory, domain)
        m_domain = get_domain_modifier(theory, domain)
        m_trend = calc_trend_modifier(theory, domain)

        t_dynamic = clamp(t_base + m_recency + m_domain + m_trend, 0.0, 1.0)

        log.info(f"Dynamic T-Score: {theory}/{domain} = {t_dynamic}")
        return t_dynamic

    except APITimeoutError as e:
        log.warning(f"API timeout for {theory}/{domain}: {e}")
        return t_base

    except RateLimitError as e:
        log.warning(f"Rate limited for {theory}/{domain}: {e}")
        # Check cache
        cached = cache.get(f"{theory}:{domain}")
        return cached if cached else t_base

    except Exception as e:
        log.error(f"Unexpected error for {theory}/{domain}: {e}")
        return t_base
```

## Output Schema

```yaml
t_score_result:
  theory: "string"
  domain: "string"
  mode: "static | dynamic | hybrid"

  scores:
    t_base: float        # [0.0, 1.0]
    m_recency: float     # [-0.15, +0.15]
    m_domain: float      # [-0.10, +0.10]
    m_trend: float       # [-0.10, +0.10]
    t_final: float       # [0.0, 1.0]

  metadata:
    calculated_at: "ISO8601"
    cache_hit: boolean
    api_sources: ["semantic_scholar", "openalex"]
    paper_count: integer

  interpretation:
    level: "very_high | high | moderate | low | very_low"
    recommendation: "string"
```

**Example Output**:
```json
{
  "theory": "TAM",
  "domain": "education",
  "mode": "hybrid",
  "scores": {
    "t_base": 0.85,
    "m_recency": 0.05,
    "m_domain": 0.05,
    "m_trend": 0.02,
    "t_final": 0.97
  },
  "metadata": {
    "calculated_at": "2024-01-15T10:30:00Z",
    "cache_hit": false,
    "api_sources": ["semantic_scholar", "openalex"],
    "paper_count": 847
  },
  "interpretation": {
    "level": "very_high",
    "recommendation": "Highly modal framework. Safe choice with strong literature support."
  }
}
```

## Performance Benchmarks

| Operation | Static | Dynamic | Hybrid (cached) | Hybrid (miss) |
|-----------|--------|---------|-----------------|---------------|
| Latency | <1ms | 500-2000ms | <10ms | 500-2000ms |
| Accuracy | Baseline | +5-10% | +5-10% | +5-10% |
| Reliability | 100% | 95% | 99% | 95% |
| API calls | 0 | 2 | 0 | 2 |

## Testing

```python
# Unit test examples
def test_static_t_score():
    score = get_t_score("TAM", "education", mode="static")
    assert score == 0.85

def test_dynamic_modifiers():
    m_recency = calc_recency_modifier("TAM", "education")
    assert -0.15 <= m_recency <= 0.15

def test_cache_functionality():
    # First call - cache miss
    score1 = get_t_score("TAM", "education", mode="hybrid")
    # Second call - cache hit
    score2 = get_t_score("TAM", "education", mode="hybrid")
    assert score1 == score2

def test_fallback_on_error():
    with mock.patch("api.query", side_effect=APITimeoutError):
        score = get_t_score("TAM", "education", mode="dynamic")
        assert score == 0.85  # Falls back to static
```

## Version History

| Version | Changes |
|---------|---------|
| 3.0.0 | Initial dynamic T-Score specification |
| 3.0.1 | Added OpenAlex integration |
| 3.0.2 | Improved caching strategy |
| 3.0.3 | Added error handling matrix |
