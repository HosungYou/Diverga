# CLI Test Runner Changelog

## v3.2.2 (2026-01-30) - Dual CLI Transcript Support

### New Feature: Multi-CLI Session Storage

Test results now support multiple CLI tools in the same session folder without overwriting.

#### File Naming Convention

| File Type | Old Name | New Name (v3.2.2) |
|-----------|----------|-------------------|
| Transcript | `conversation_transcript.md` | `conversation_transcript_claude.md` / `conversation_transcript_codex.md` |
| Raw JSON | `conversation_raw.json` | `conversation_raw_claude.json` / `conversation_raw_codex.json` |
| Result YAML | `QUANT-004_test_result.yaml` | `QUANT-004_test_result_claude.yaml` / `QUANT-004_test_result_codex.yaml` |

#### Benefits

- Run both Claude Code and Codex CLI tests for the same scenario
- Compare results side-by-side
- No data loss from overwriting

#### Usage

```bash
# Run Claude Code test
python qa/runners/cli_test_runner.py --scenario QUANT-004 --cli claude

# Run Codex CLI test (same folder, different files)
python qa/runners/cli_test_runner.py --scenario QUANT-004 --cli codex

# Both results saved in qa/reports/sessions/QUANT-004/
# - conversation_transcript_claude.md
# - conversation_transcript_codex.md
# - QUANT-004_test_result_claude.yaml
# - QUANT-004_test_result_codex.yaml
```

---

## v3.2.0 (2026-01-30) - Hybrid Checkpoint Detection

### New Feature: Hybrid Detection System

The checkpoint detection now supports both formal CP_ identifiers AND descriptive checkpoint names.

#### CHECKPOINT_ALIASES Dictionary

Maps 50+ descriptive names to formal CP_ identifiers:

```python
CHECKPOINT_ALIASES = {
    # Research Direction
    'Research Direction': 'CP_RESEARCH_DIRECTION',
    '연구 방향': 'CP_RESEARCH_DIRECTION',

    # Effect Size
    'Effect Size Selection': 'CP_EFFECT_SIZE_SELECTION',
    'Effect Size Target Selection': 'CP_EFFECT_SIZE_SELECTION',
    '효과크기 선택': 'CP_EFFECT_SIZE_SELECTION',

    # Moderator Analysis
    'Moderator Analysis Strategy': 'CP_MODERATOR_ANALYSIS',
    '조절변수 분석': 'CP_MODERATOR_ANALYSIS',

    # ... 50+ more aliases
}
```

#### Three-Phase Detection

1. **Phase 1**: Detect formal `CP_XXX` identifiers (highest priority)
2. **Phase 2**: Detect descriptive names and map via aliases
3. **Phase 3**: LOW confidence partial mentions

#### New Methods

- `_normalize_checkpoint_name()`: Maps descriptive names to formal CP_ IDs
- Updated `_detect_checkpoints()`: Three-phase hybrid detection

#### Test Scenario

Created QUANT-004 to test hybrid detection with:
- Formal CP_ checkpoints
- Descriptive English names
- Korean aliases (한국어)

### Usage Example

AI Response:
```markdown
🟠 CHECKPOINT: Effect Size Target Selection
어떤 효과크기 지표를 사용하시겠습니까?
```

Detection Result:
```yaml
id: CP_EFFECT_SIZE_SELECTION
confidence: MEDIUM
context: "descriptive → CP_EFFECT_SIZE_SELECTION"
original: "Effect Size Target Selection"
```

### Checkpoint Equivalence Mapping

Added equivalence groups for semantically similar checkpoint IDs:

```python
CHECKPOINT_EQUIVALENCES = {
    'CP_PARADIGM_SELECTION': 'CP_PARADIGM_CONFIRMATION',
    'CP_MODERATOR_SELECTION': 'CP_MODERATOR_ANALYSIS',
    'CP_ANALYSIS_PLAN_APPROVAL': 'CP_METHODOLOGY_APPROVAL',
    'CP_ANALYSIS_MODEL': 'CP_HETEROGENEITY_ANALYSIS',
}
```

### Test Results: QUANT-004

| CLI Tool | Checkpoints | Compliance | Skill Loaded |
|----------|-------------|------------|--------------|
| Claude Code | 6 detected | 100%* | ✅ Yes |
| Codex CLI | 1 detected | 0% | ❌ No |

*With equivalence mapping applied

See full report: `qa/reports/sessions/QUANT-004/QUANT-004_REPORT.md`

---

## v3.1.1 (2026-01-30) - Codex CLI Review Fixes

Based on Codex CLI (gpt-5.2-codex) review feedback.

### Issues Fixed

| Issue | Before | After |
|-------|--------|-------|
| **False Positive Agents** | `[A-Z]\d+` matched M1, N1, S1 | `[A-H][1-7]` only matches valid agents |
| **False Positive Checkpoints** | Captured "RESEARCH" as checkpoint | Requires full `CP_XXX_YYY` format |
| **No Skill Verification** | No way to verify Diverga was loaded | `_check_skill_loaded()` verifies skill |
| **Invocation vs Mention** | All mentions counted as invocations | Confidence scoring (HIGH/MEDIUM/LOW) |
| **Checkpoint Compliance** | Exact string match only | Fuzzy matching for partial names |

### New Features

#### 1. Agent Detection with Confidence Scoring

```python
def _detect_agents(self, response: str) -> List[Dict[str, Any]]:
    """
    Confidence levels:
    - HIGH: Task tool invocation (Task(subagent_type="diverga:a1"))
    - MEDIUM: Explicit execution ("A1 에이전트 실행")
    - LOW: Text mention only (not counted as invocations)
    """
```

**Valid Agent Pattern**: `[A-H][1-7]` only (40 agents total)
- A1-A6: Foundation
- B1-B5: Evidence
- C1-C7: Design & Meta-Analysis
- D1-D4: Data Collection
- E1-E5: Analysis
- F1-F5: Quality
- G1-G6: Communication
- H1-H2: Specialized

#### 2. Checkpoint Detection with Confidence Scoring

```python
def _detect_checkpoints(self, response: str) -> List[Dict[str, Any]]:
    """
    Confidence levels:
    - HIGH: Emoji marker + options (🔴 CHECKPOINT: CP_XXX with [Y]/[N])
    - MEDIUM: Plain text checkpoint format
    - LOW: Inferred from context (not counted)
    """
```

**Valid Checkpoint Pattern**: `CP_[A-Z][A-Z_]+`
- Examples: CP_RESEARCH_DIRECTION, CP_PARADIGM_SELECTION, CP_THEORY_SELECTION

#### 3. Skill Loading Verification

```python
def _check_skill_loaded(self, response: str) -> Dict[str, Any]:
    """
    Verifies Diverga skill is active by checking:
    1. Skill activation markers (Research Coordinator v6.x)
    2. VS methodology markers (T-Score, typicality)
    3. Checkpoint system markers (emoji + format)
    4. Agent invocation patterns (Task tool)

    Returns: {'loaded': bool, 'confidence': str, 'score': int, 'evidence': list}
    """
```

#### 4. Fuzzy Checkpoint Matching

```python
def _fuzzy_checkpoint_match(self, found: str, expected: str) -> bool:
    """
    Handles partial matches:
    - CP_RESEARCH matches CP_RESEARCH_DIRECTION
    - CP_EFFECT_SIZE matches CP_EFFECT_SIZE_SELECTION
    """
```

### Updated Output Format

#### Test Result Status

| Status | Condition |
|--------|-----------|
| PASSED | ≥80% checkpoint compliance + skill verified |
| PARTIAL | ≥80% compliance but skill not verified |
| FAILED | <80% compliance |

#### New Metrics

```yaml
metrics:
  skill_loaded: true
  skill_confidence: HIGH  # HIGH/MEDIUM/LOW/NONE
```

#### Enhanced Checkpoint Data

```yaml
checkpoints:
  - id: CP_RESEARCH_DIRECTION
    turn: 1
    status: TRIGGERED
    confidence: HIGH  # Now includes confidence level
```

### Files Changed

- `qa/runners/cli_test_runner.py`: Main verification logic updates
  - `_detect_agents()`: Confidence scoring, valid pattern restriction
  - `_detect_checkpoints()`: Confidence scoring, full CP_ prefix requirement
  - `_check_skill_loaded()`: NEW - Skill verification method
  - `_fuzzy_checkpoint_match()`: NEW - Partial checkpoint matching
  - `_verify_skill_loading()`: NEW - Aggregated skill verification
  - `_validate_session()`: Updated to use new methods
  - `_save_result_yaml()`: Include skill loading status
  - `_save_readme()`: Add skill loading verification section
  - `_save_transcript()`: Show confidence levels per detection

### Testing

Run with dry-run to verify syntax:
```bash
python qa/runners/cli_test_runner.py --scenario QUANT-003 --dry-run -v
```

Run with real CLI:
```bash
python qa/runners/cli_test_runner.py --scenario QUANT-003 --cli claude
```

## v3.1.1 (2026-01-30) - Codex CLI Review Fixes

Based on Codex CLI (gpt-5.2-codex) code review feedback.

### Issues Fixed

| Issue | Before | After |
|-------|--------|-------|
| **Invalid Agent IDs Accepted** | `[A-H][1-7]` accepted B5, F5, G6, H7 | Strict per-category validation |
| **Checkpoint Pattern** | `[A-Z][A-Z_]+` (no digits) | `[A-Z0-9]+(?:_[A-Z0-9]+)*` |
| **Skill Markers** | Hardcoded "27 agents" | `(27|33|40)` for all versions |
| **Fuzzy Match** | 50% overlap | 75% overlap + all keywords for short names |
| **Agent Name Patterns** | `[A-Za-z]+` only | `[A-Za-z-]+` for hyphenated names |

### New: Strict Agent Validation Registry

```python
VALID_AGENTS = {
    'A': [1, 2, 3, 4, 5, 6],      # Foundation (6)
    'B': [1, 2, 3, 4],             # Evidence (4) - no B5
    'C': [1, 2, 3, 4, 5, 6, 7],    # Design & Meta-Analysis (7)
    'D': [1, 2, 3, 4],             # Data Collection (4)
    'E': [1, 2, 3, 4, 5],          # Analysis (5)
    'F': [1, 2, 3, 4],             # Quality (4) - no F5
    'G': [1, 2, 3, 4],             # Communication (4) - no G5-G7
    'H': [1, 2],                   # Specialized (2) - no H3-H7
}
# Total: 33 valid agents (not 40 as previously documented)
```

### Test Results: QUANT-003 with Claude Code

| Metric | Result |
|--------|--------|
| Skill Loaded | ✅ TRUE (HIGH confidence, score 80) |
| Verification Huddle | ✅ PASSED (6/6 checks) |
| Checkpoints Found | 1 (CP_PARADIGM_CONFIRMATION) |
| Expected Checkpoints | 4 |
| Checkpoint Compliance | 0.0% |
| Agents Detected | 0 |
| Overall Status | FAILED |

### Root Cause Identified

The AI uses **descriptive checkpoint names** (e.g., "Effect Size Target Selection") instead of formal **CP_XXX** identifiers (e.g., "CP_EFFECT_SIZE_SELECTION").

**Example from transcript:**
```markdown
🟠 CHECKPOINT: Effect Size Target Selection
```

**Detection pattern requires:**
```python
r'🟠\s*CHECKPOINT[:\s]+(CP_[A-Z0-9]+(?:_[A-Z0-9]+)*)'
```

### Recommended Next Steps

1. Add descriptive-to-formal checkpoint mapping
2. Update skill prompt to use formal CP_ identifiers
3. Implement hybrid detection (formal + descriptive fallback)

See full report: `qa/reports/sessions/QUANT-003/QUANT-003_REPORT.md`
