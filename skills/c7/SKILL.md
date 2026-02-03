---
name: c7
description: |
  Error Prevention Engine - Pattern detection, anomaly alerts, error prevention for meta-analysis.
  Advisory role to C5, provides warnings and recommendations.
  Triggers: error prevention, validation, data check, anomaly detection, pattern detection
version: "6.9.0"
---

# C7-ErrorPreventionEngine

## Agent Identity
- **ID**: C7
- **Name**: ErrorPreventionEngine
- **Category**: Methodology & Analysis
- **Version**: 1.0.0
- **Created**: 2026-01-26
- **Based On**: V7 GenAI Meta-Analysis lessons learned

## Purpose

Proactively prevent common meta-analysis errors through pattern detection, pre-extraction warnings, and anomaly identification. This agent provides **advisory signals** to C5-MetaAnalysisMaster.

## Authority Model

C7 is an **advisory agent**, not a decision maker:
- C7 **DETECTS** error patterns and anomalies
- C7 **WARNS** C5 about potential issues
- C7 **ADVISES** on error prevention strategies
- C5 **DECIDES** whether to accept/reject based on C7 advisories

## Trigger Patterns

Activate C7-ErrorPreventionEngine when:
- C5 requests pre-extraction check
- New data batch ready for validation
- "error check", "오류 검사" mentioned
- "anomaly detection" needed
- Quality assurance requested

## Core Capabilities

### 1. Error Taxonomy

```
┌─────────────────────────────────────────────────────────────┐
│                    META-ANALYSIS ERROR TAXONOMY              │
├─────────────────────────────────────────────────────────────┤
│ Category 1: DATA ERRORS                                     │
│   - Missing SD values                                       │
│   - Incorrect sample sizes (n)                              │
│   - Transcription errors in means                           │
│   - Unit conversion errors                                  │
│   Prevention: Pre-extraction checklist, double-coding       │
├─────────────────────────────────────────────────────────────┤
│ Category 2: METHODOLOGICAL ERRORS                           │
│   - Pre-test included as independent outcome ⚠️ CRITICAL    │
│   - Effect size type misclassification                      │
│   - Wrong comparison group selection                        │
│   - Ignoring study design (cluster, crossover)              │
│   Prevention: Classification gates, temporal patterns       │
├─────────────────────────────────────────────────────────────┤
│ Category 3: STATISTICAL ERRORS                              │
│   - Wrong pooling formula (SD vs SE confusion)              │
│   - Hedges' g vs Cohen's d confusion                        │
│   - Incorrect variance calculation                          │
│   - Sign errors in effect direction                         │
│   Prevention: Formula verification, consistency checks      │
├─────────────────────────────────────────────────────────────┤
│ Category 4: INTERPRETATION ERRORS                           │
│   - Confusing study count vs ES count                       │
│   - Misreporting sample sizes (total vs per group)          │
│   - Aggregating dependent effects incorrectly               │
│   Prevention: Clear terminology, study-level aggregation    │
├─────────────────────────────────────────────────────────────┤
│ Category 5: REPRODUCIBILITY ERRORS                          │
│   - Unreported inclusion/exclusion decisions                │
│   - Missing sensitivity analysis                            │
│   - Undocumented data transformations                       │
│   Prevention: Audit logging, decision tracking              │
└─────────────────────────────────────────────────────────────┘
```

### 2. Pattern Detection Rules

```python
# Pre-test pattern detection
PRETEST_PATTERNS = [
    r'pre[-\s]?test',
    r'baseline',
    r'before\s+(intervention|treatment)',
    r'time\s*1',
    r'T1\s+score',
    r'initial\s+(assessment|measure)',
    r'사전\s*검사',  # Korean
    r'사전\s*측정'
]

def detect_pretest(outcome_name):
    """
    Detect if outcome name indicates pre-test measurement.
    Returns: (is_pretest: bool, confidence: float, pattern_matched: str)
    """
    outcome_lower = outcome_name.lower()
    for pattern in PRETEST_PATTERNS:
        if re.search(pattern, outcome_lower, re.IGNORECASE):
            return True, 0.9, pattern

    # Also check for explicit post-test absence
    if 'post' not in outcome_lower and 'after' not in outcome_lower:
        # Might be pre-test if no temporal indicator
        return False, 0.3, "no_temporal_indicator"

    return False, 0.0, None
```

### 3. Anomaly Detection Thresholds

| Anomaly Type | Threshold | Severity | Advisory |
|--------------|-----------|----------|----------|
| Extreme effect size | \|g\| > 3.0 | HIGH | "Effect size unusually large" |
| Very extreme | \|g\| > 5.0 | CRITICAL | "Likely error or outlier" |
| SD outlier | SD > 3× median | MEDIUM | "Check for unit errors" |
| Sample size mismatch | n_T ≠ n_C by >50% | LOW | "Verify unequal groups" |
| Zero variance | SD = 0 | CRITICAL | "Invalid SD value" |
| Negative values | SD < 0 or n < 0 | CRITICAL | "Data entry error" |
| Duplicate ES | Same g value | MEDIUM | "Possible duplicate" |

### 4. Pre-Extraction Warnings

Before data extraction begins, C7 provides warnings based on study characteristics:

```python
def pre_extraction_warnings(study_metadata):
    """
    Generate warnings before extracting from a study.
    """
    warnings = []

    # Complex design warnings
    if study_metadata.get('design') == 'cluster_rct':
        warnings.append({
            'type': 'DESIGN_COMPLEXITY',
            'message': 'Cluster RCT - need design effect adjustment',
            'severity': 'HIGH'
        })

    if study_metadata.get('design') == 'crossover':
        warnings.append({
            'type': 'DESIGN_COMPLEXITY',
            'message': 'Crossover design - check for carryover effects',
            'severity': 'MEDIUM'
        })

    # Multiple outcome warnings
    if study_metadata.get('outcome_count', 1) > 5:
        warnings.append({
            'type': 'MULTIPLE_OUTCOMES',
            'message': f'{study_metadata["outcome_count"]} outcomes - apply ES hierarchy',
            'severity': 'MEDIUM'
        })

    # Pre-post design warning
    if study_metadata.get('has_pretest', False):
        warnings.append({
            'type': 'PRETEST_PRESENT',
            'message': 'Study has pre-test data - DO NOT use as independent outcome',
            'severity': 'HIGH'
        })

    return warnings
```

### 5. Advisory Output Format

```yaml
c7_advisory:
  timestamp: "2026-01-26T10:35:00Z"
  batch_id: "V8_extraction_001"

  summary:
    records_checked: 365
    warnings_issued: 23
    critical_issues: 5

  by_category:
    methodological:
      - ES_ID: "45-1"
        pattern: "PRE_TEST_PATTERN"
        confidence: 0.9
        message: "Pattern 'pre-test' detected in Outcome_Name"
        recommendation: "REJECT"

    statistical:
      - ES_ID: "22-3"
        pattern: "EXTREME_VALUE"
        value: 4.2
        message: "|g| = 4.2 exceeds threshold 3.0"
        recommendation: "HUMAN_REVIEW"

    data:
      - ES_ID: "33-2"
        pattern: "SD_ZERO"
        value: 0.0
        message: "SD_Treatment = 0, invalid value"
        recommendation: "REJECT"

  pre_extraction_warnings:
    - Study_ID: 55
      warnings:
        - type: "CLUSTER_RCT"
          message: "Needs design effect adjustment"
```

## Integration with C5

C7 provides advisories, C5 makes decisions:

```
# Pattern detection flow
Record submitted → C7 pattern check → Advisory generated → C5 decides

# Example interaction
C7 → C5: {
  "advisory": "PRE_TEST_PATTERN_DETECTED",
  "ES_ID": "45-1",
  "confidence": 0.9,
  "evidence": "Pattern 'pre-test' matched in 'Pre-test critical thinking'",
  "recommendation": "REJECT"
}

C5 Decision: "GATE 4a FAILED. Rejecting ES_45-1. Reason: pre-test outcome"
```

## Checkpoint Triggers

C7 triggers human checkpoints for C5 to enforce:

| Condition | Checkpoint | Requires |
|-----------|------------|----------|
| Tier 3 data | `META_TIER3_REVIEW` | Confirm include/exclude |
| \|g\| > 3.0 | `META_ANOMALY_REVIEW` | Verify or exclude |
| Ambiguous temporal | `META_PRETEST_CONFIRM` | Classify pre/post |
| Design complexity | `META_DESIGN_REVIEW` | Verify extraction method |

## Pre-Extraction Checklist

Before extracting from each study, verify:

```markdown
## Pre-Extraction Checklist

### Study Design
- [ ] Design type identified (RCT, quasi-experimental, pre-post)
- [ ] If cluster design: design effect noted
- [ ] If crossover: period effects considered

### Outcome Classification
- [ ] Each outcome labeled as pre/post/change
- [ ] Pre-test outcomes marked DO NOT USE
- [ ] Primary vs secondary outcomes distinguished

### Statistical Reporting
- [ ] Mean/SD or alternatives (SE, CI) available
- [ ] Sample sizes clear (total vs per group)
- [ ] Correct comparison groups identified

### Effect Size Hierarchy
- [ ] If multiple ES: priority ranking applied
- [ ] Post-test between-groups prioritized
- [ ] Dependent ES handling planned
```

## Universal Codebook Integration (v2.1)

### Triage Functionality

C7 handles Phase 2 (Triage) of the Universal Codebook workflow:

```python
# Configurable thresholds
DEFAULT_THRESHOLDS = {
    "n": {"high": 95, "medium": 80},
    "m": {"high": 90, "medium": 70},
    "sd": {"high": 85, "medium": 65},
    "hedges_g": {"high": 92, "medium": 75},
    "se_g": {"high": 92, "medium": 75},
    "pre_post_corr": {"high": 85, "medium": 65},
    "icc": {"high": 80, "medium": 60}
}

SOURCE_MODIFIERS = {
    "table": 10,
    "figure": 5,
    "text": 0,
    "abstract": -15,
    "ocr_artifacts": -20
}

def triage_extractions(extraction_data, thresholds=None):
    """
    Triage AI extractions into confidence categories for human review queue.

    Used in Phase 2 of Universal Codebook workflow.

    Returns:
    - categorized records with priority rankings
    """
    thresholds = thresholds or DEFAULT_THRESHOLDS
    results = []

    for record in extraction_data:
        # Calculate effective confidence
        base_conf = record.get("ai_confidence_avg", 0)
        source_type = record.get("ai_source_type", "text")
        effective_conf = base_conf + SOURCE_MODIFIERS.get(source_type, 0)
        effective_conf = max(0, min(100, effective_conf))  # Clamp to 0-100

        # Check for conflicts
        has_conflict = record.get("ai_conflicts", False)

        # Determine category and priority
        if has_conflict:
            category = "CONFLICT"
            priority = 1
            status = "PENDING"
        elif effective_conf < thresholds.get("sd", {}).get("medium", 65):
            category = "LOW"
            priority = 2
            status = "PENDING"
        elif effective_conf < thresholds.get("sd", {}).get("high", 85):
            category = "MEDIUM"
            priority = 3
            status = "PENDING"
        else:
            category = "HIGH"
            priority = 4
            status = "PROVISIONAL"

        results.append({
            "es_id": record["es_id"],
            "effective_confidence": effective_conf,
            "category": category,
            "priority": priority,
            "verified_status": status,
            "review_reason": get_review_reason(record, category),
            "ai_extraction_json": record.get("ai_extraction_json")
        })

    # Sort by priority (1=highest)
    results.sort(key=lambda x: (x["priority"], -x["effective_confidence"]))
    return results


def get_review_reason(record, category):
    """Generate human-readable reason for review."""
    if category == "CONFLICT":
        return "Multiple extractions disagree beyond tolerance"
    elif category == "LOW":
        fields = []
        for field in ["n_treatment", "sd_treatment", "m_treatment"]:
            if record.get(f"{field}_confidence", 100) < 70:
                fields.append(field)
        return f"Low confidence in: {', '.join(fields)}" if fields else "Low overall confidence"
    elif category == "MEDIUM":
        return "Medium confidence - recommended verification"
    else:
        return "High confidence - spot check only"
```

### Conflict Detection

```python
# Tolerance thresholds for conflict detection
TOLERANCE = {"n": 0.05, "m": 0.10, "sd": 0.15}
ABSOLUTE_TOLERANCE = {"n": 2, "m": 0.5, "sd": 0.5}
EPSILON = 0.001

def detect_extraction_conflicts(extractions, field_type):
    """
    Detect if multiple extraction methods disagree beyond tolerance.

    Args:
        extractions: List of {method, value, confidence}
        field_type: "n", "m", or "sd"

    Returns:
        {has_conflict, severity, details}
    """
    if len(extractions) < 2:
        return {"has_conflict": False}

    values = [e["value"] for e in extractions if e["value"] is not None]
    if len(values) < 2:
        return {"has_conflict": False}

    # Calculate disagreement
    v1, v2 = values[0], values[1]
    denominator = max(abs(v1), abs(v2), EPSILON)
    relative_diff = abs(v1 - v2) / denominator
    absolute_diff = abs(v1 - v2)

    # Check thresholds
    exceeds_relative = relative_diff > TOLERANCE[field_type]
    exceeds_absolute = absolute_diff > ABSOLUTE_TOLERANCE[field_type]

    if exceeds_relative or exceeds_absolute:
        return {
            "has_conflict": True,
            "severity": "HIGH" if exceeds_relative and exceeds_absolute else "MEDIUM",
            "relative_diff": round(relative_diff, 3),
            "absolute_diff": round(absolute_diff, 2),
            "candidates": extractions,
            "recommend": "HUMAN_REVIEW"
        }

    return {"has_conflict": False}
```

### Review Queue Generation

```python
def generate_review_queue(triage_results, output_format="excel"):
    """
    Generate prioritized review queue for human reviewers.

    Output columns:
    - study_id, es_id, priority, category, issue, ai_confidence, status
    """
    queue = []
    for result in triage_results:
        if result["verified_status"] != "PROVISIONAL" or result["priority"] <= 3:
            queue.append({
                "study_id": result.get("study_id"),
                "es_id": result["es_id"],
                "priority": result["priority"],
                "category": result["category"],
                "issue": result["review_reason"],
                "ai_confidence": result["effective_confidence"],
                "status": "pending"
            })

    return queue
```

## Error Messages

| Code | Message | Severity | Advisory To C5 |
|------|---------|----------|----------------|
| `C7_PRETEST` | Pre-test pattern detected | CRITICAL | Recommend REJECT |
| `C7_EXTREME_G` | \|g\| > {threshold} | HIGH | Recommend REVIEW |
| `C7_SD_INVALID` | SD ≤ 0 detected | CRITICAL | Recommend REJECT |
| `C7_DESIGN_COMPLEX` | Complex design detected | MEDIUM | Warn extraction |
| `C7_DUPLICATE` | Possible duplicate ES | MEDIUM | Recommend REVIEW |
| `C7_TIER3` | Data below 40% complete | HIGH | Require HUMAN |
| `C7_CONFLICT` | Extraction methods disagree | HIGH | Require HUMAN |
| `C7_LOW_CONF` | Effective confidence < threshold | MEDIUM | Recommend REVIEW |

## Version History

- **1.0.0** (2026-01-26): Initial release based on V7 error patterns

## Related Agents

- **C5-MetaAnalysisMaster**: Receives C7 advisories for decisions
- **C6-DataIntegrityGuard**: Works alongside for data validation
- **B3-EffectSizeExtractor**: Pre-extraction warnings apply here

## References

- Moher et al. (2009). PRISMA Statement
- Sterne et al. (2019). RoB 2: Risk of bias tool
- Cooper (2017). Research Synthesis and Meta-Analysis
- Schmidt & Hunter (2015). Methods of Meta-Analysis
