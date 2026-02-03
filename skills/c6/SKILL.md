---
name: c6
description: |
  Data Integrity Guard - Data completeness validation, Hedges g calculation, SD recovery.
  Service provider to C5, handles extraction from PDFs and data validation.
  Triggers: data extraction, PDF extract, data completeness, SD recovery, Hedges g calculation
---

# C6-DataIntegrityGuard

## Agent Identity
- **ID**: C6
- **Name**: DataIntegrityGuard
- **Category**: Methodology & Analysis
- **Version**: 1.0.0
- **Created**: 2026-01-26
- **Based On**: V7 GenAI Meta-Analysis lessons learned

## Purpose

Ensure data completeness, track versions, calculate derived statistics (Hedges' g), and implement SD recovery strategies. This agent **provides integrity reports** to C5-MetaAnalysisMaster for gate decisions.

## Authority Model

C6 is a **service provider**, not a decision maker:
- C6 **REPORTS** data integrity status to C5
- C6 **CALCULATES** Hedges' g and SE
- C6 **RECOVERS** missing SD values using multiple strategies
- C5 **DECIDES** based on C6 reports

## Trigger Patterns

Activate C6-DataIntegrityGuard when:
- C5 requests integrity report
- "data completeness" mentioned
- "missing values", "결측치" mentioned
- "Hedges' g calculation" needed
- "SD recovery", "표준편차 복구" mentioned
- Version tracking required

## Core Capabilities

### 1. Hedges' g Calculation

```python
def calculate_hedges_g(m1, sd1, n1, m2, sd2, n2):
    """
    Calculate Hedges' g with small-sample correction.

    Parameters:
    - m1, sd1, n1: Treatment group (mean, SD, n)
    - m2, sd2, n2: Control group (mean, SD, n)

    Returns:
    - g: Hedges' g (bias-corrected effect size)
    - se_g: Standard error of g
    """
    if any(pd.isna([m1, sd1, n1, m2, sd2, n2])):
        return None, None
    if sd1 <= 0 or sd2 <= 0 or n1 <= 1 or n2 <= 1:
        return None, None

    # Pooled standard deviation
    pooled_sd = np.sqrt(
        ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) /
        (n1 + n2 - 2)
    )

    if pooled_sd <= 0:
        return None, None

    # Cohen's d
    d = (m1 - m2) / pooled_sd

    # Hedges' correction factor J
    df = n1 + n2 - 2
    J = 1 - (3 / (4 * df - 1))

    # Hedges' g
    g = d * J

    # Standard error of g
    se_g = np.sqrt(
        (n1 + n2) / (n1 * n2) + (g**2) / (2 * (n1 + n2))
    ) * J

    return g, se_g
```

### 2. Data Completeness Scoring

```python
def calculate_completeness(record):
    """
    Calculate data completeness score (0-1).

    Required fields: Study_ID, ES_ID, Outcome_Name (must be present)
    Statistical fields: M_Treatment, SD_Treatment, n_Treatment,
                       M_Control, SD_Control, n_Control
    """
    required = ['Study_ID', 'ES_ID', 'Outcome_Name']
    statistical = ['M_Treatment', 'SD_Treatment', 'n_Treatment',
                   'M_Control', 'SD_Control', 'n_Control']

    # Required must all be present
    for field in required:
        if pd.isna(record.get(field)):
            return 0.0  # Tier 3 - incomplete

    # Statistical completeness
    stat_present = sum(1 for f in statistical if pd.notna(record.get(f)))
    completeness = stat_present / len(statistical)

    return completeness

def assign_tier(completeness):
    """Assign data tier based on completeness."""
    if completeness >= 0.70:
        return 1  # High confidence
    elif completeness >= 0.40:
        return 2  # Medium confidence
    else:
        return 3  # Low confidence - HUMAN REVIEW
```

### 3. SD Recovery Strategies

```
┌─────────────────────────────────────────────────────────────┐
│                    SD RECOVERY STRATEGIES                    │
├─────────────────────────────────────────────────────────────┤
│ Priority 1: DIRECT EXTRACTION                               │
│   - Check tables, figures, appendices in PDF                │
│   - Often SD is reported but not in main text               │
│   Success rate: ~40%                                        │
├─────────────────────────────────────────────────────────────┤
│ Priority 2: CALCULATE FROM CI/SE                            │
│   - SE → SD: SD = SE × √n                                   │
│   - 95% CI → SE: SE = (upper - lower) / 3.92               │
│   Success rate: ~25%                                        │
├─────────────────────────────────────────────────────────────┤
│ Priority 3: IMPUTATION FROM SIMILAR STUDIES                 │
│   - Use median SD from same outcome domain                  │
│   - Apply coefficient of variation method                   │
│   - Document imputation method                              │
│   Success rate: ~20%                                        │
├─────────────────────────────────────────────────────────────┤
│ Priority 4: CONTACT AUTHORS                                 │
│   - Email corresponding author                              │
│   - Request raw data or unreported statistics               │
│   Success rate: ~15%                                        │
└─────────────────────────────────────────────────────────────┘
```

### 4. Version Tracking

```python
def track_version_changes(old_df, new_df, version_name):
    """
    Track changes between dataset versions.

    Returns:
    - added: New records
    - removed: Deleted records
    - modified: Changed records with diff
    - data_loss: Fields that lost values (critical!)
    """
    report = {
        'version': version_name,
        'timestamp': datetime.now().isoformat(),
        'old_rows': len(old_df),
        'new_rows': len(new_df),
        'added': [],
        'removed': [],
        'modified': [],
        'data_loss': []
    }

    # Check for unexpected data loss
    for col in ['SD_Treatment', 'SD_Control', 'Hedges_g']:
        old_available = old_df[col].notna().sum()
        new_available = new_df[col].notna().sum()
        if new_available < old_available:
            report['data_loss'].append({
                'field': col,
                'lost': old_available - new_available,
                'severity': 'HIGH'
            })

    return report
```

### 5. Study-Level Aggregation

```python
def study_level_summary(df):
    """
    Aggregate effect sizes to study level.
    Prevents confusion between study count and ES count.
    """
    summary = df.groupby('Study_ID').agg({
        'ES_ID': 'count',
        'Hedges_g': lambda x: x.notna().sum(),
        'Data_Tier': 'min'  # Worst tier in study
    }).rename(columns={
        'ES_ID': 'effect_size_count',
        'Hedges_g': 'valid_hedges_g_count',
        'Data_Tier': 'worst_tier'
    })

    summary['all_g_missing'] = (
        summary['valid_hedges_g_count'] == 0
    )

    return summary
```

## Output Formats

### Integrity Report

```yaml
integrity_report:
  version: "V8"
  timestamp: "2026-01-26T10:30:00Z"

  record_summary:
    total_records: 365
    records_with_hedges_g: 243
    missing_hedges_g: 122
    missing_percentage: 33.4%

  tier_distribution:
    tier_1: 180
    tier_2: 145
    tier_3: 40

  study_summary:
    total_studies: 66
    studies_with_valid_g: 47
    studies_all_g_missing: 19

  field_completeness:
    M_Treatment: 85.2%
    SD_Treatment: 72.3%
    n_Treatment: 89.5%
    M_Control: 82.1%
    SD_Control: 69.6%
    n_Control: 87.4%

  version_changes:
    from_version: "V7"
    records_added: 0
    records_removed: 0
    hedges_g_gained: 33
    data_loss_warnings: []

  recovery_potential:
    sd_recoverable_from_ci: 15
    sd_recoverable_from_se: 8
    recommended_strategy: "Priority 1: Direct extraction"
```

### Anomaly Report

```yaml
anomalies_detected:
  - ES_ID: "45-3"
    type: "EXTREME_VALUE"
    value: 4.2
    message: "|g| > 3.0, requires human review"

  - ES_ID: "22-1"
    type: "SD_OUTLIER"
    value: 45.2
    message: "SD > 3× median, check for unit errors"
```

## Integration with C5

C6 provides reports, C5 makes decisions:

```
C5 → C6: "Calculate Hedges' g for all records"
C6 → C5: integrity_report with calculations

C5 → C6: "Recover missing SD values"
C6 → C5: recovery_report with strategies applied

C5 → C6: "Track V7 → V8 changes"
C6 → C5: version_change_report
```

## Universal Codebook Integration (v2.1)

### Extraction with Provenance

C6 now tracks extraction provenance for AI-Human collaboration:

```python
def extract_with_provenance(pdf_path, fields, methods=["rag", "ocr"]):
    """
    Extract statistical values with full provenance tracking.

    Returns:
    - ai_extraction_json: {field: {ai_value, source, method, confidence, derived_from}}
    """
    results = {}

    for field in fields:
        extractions = []

        # Try RAG extraction
        if "rag" in methods:
            rag_result = rag_extract(pdf_path, field)
            if rag_result:
                extractions.append({
                    "value": rag_result.value,
                    "source": rag_result.location,
                    "method": "RAG",
                    "confidence": rag_result.confidence,
                    "source_type": classify_source(rag_result.location)
                })

        # Try OCR extraction
        if "ocr" in methods:
            ocr_result = ocr_extract(pdf_path, field)
            if ocr_result:
                extractions.append({
                    "value": ocr_result.value,
                    "source": ocr_result.location,
                    "method": "OCR",
                    "confidence": ocr_result.confidence,
                    "source_type": classify_source(ocr_result.location)
                })

        # Reconcile if multiple extractions
        if len(extractions) > 1:
            final = reconcile_extractions(extractions, get_field_type(field))
        elif len(extractions) == 1:
            final = extractions[0]
        else:
            final = {"value": None, "confidence": 0, "method": "NOT_FOUND"}

        results[field] = {
            "ai_value": final["value"],
            "source": final.get("source"),
            "method": final["method"],
            "confidence": final["confidence"],
            "derived_from": final.get("derived_from"),
            "candidates": extractions if len(extractions) > 1 else None
        }

    return results
```

### Hedges' g with Provenance

```python
def calculate_hedges_g_with_provenance(m1, sd1, n1, m2, sd2, n2, sources=None):
    """
    Calculate Hedges' g with source provenance tracking.

    Args:
        sources: {m1_source, sd1_source, n1_source, ...}

    Returns:
        {g, se_g, confidence, provenance}
    """
    g, se_g = calculate_hedges_g(m1, sd1, n1, m2, sd2, n2)

    if g is None:
        return {"g": None, "se_g": None, "confidence": 0, "status": "CALC_FAIL"}

    # Propagate confidence from source values
    source_confidences = [
        sources.get(f"{f}_confidence", 100)
        for f in ["m1", "sd1", "n1", "m2", "sd2", "n2"]
        if sources
    ]

    min_confidence = min(source_confidences) if source_confidences else 100
    derived_confidence = min_confidence * 0.95  # Formula reliability factor

    return {
        "g": round(g, 4),
        "se_g": round(se_g, 4),
        "confidence": round(derived_confidence, 1),
        "provenance": {
            "formula": "Hedges' g with small-sample correction",
            "sources": sources,
            "assumptions": ["Pooled SD", "Equal variances assumed"]
        },
        "status": "CALCULATED"
    }
```

### ScholaRAG Integration

```python
def extract_from_scholarag_rag(rag_instance, study_id, fields):
    """
    Extract values from ScholaRAG RAG system with provenance.

    Used in Phase 1 of Universal Codebook workflow.
    """
    prompt_template = """
    From study {study_id}, extract the following statistical values:
    {field_list}

    For each value found, provide:
    1. The extracted value
    2. The exact location (page, table, paragraph)
    3. Your confidence (0-100%)

    If not found, respond with "NOT_FOUND".
    """

    response = rag_instance.query(
        prompt_template.format(
            study_id=study_id,
            field_list="\n".join(f"- {f}" for f in fields)
        )
    )

    return parse_rag_response(response)
```

## Error Messages

| Code | Message | Action |
|------|---------|--------|
| `C6_CALC_FAIL` | Cannot calculate g: missing {field} | Report to C5 |
| `C6_SD_ZERO` | SD ≤ 0 detected | Report anomaly |
| `C6_DATA_LOSS` | {n} values lost in {field} | Critical warning |
| `C6_TIER3` | Record below 40% completeness | Flag for review |
| `C6_RECOVERY_FAIL` | All SD recovery strategies failed | Report to C5 |
| `C6_CONFLICT` | Multiple extractions disagree beyond tolerance | Flag for human review |
| `C6_LOW_CONF` | Extraction confidence below threshold | Flag for human review |

## Version History

- **1.0.0** (2026-01-26): Initial release based on V7 data integrity issues

## Related Agents

- **C5-MetaAnalysisMaster**: Uses C6 reports for gate decisions
- **C7-ErrorPreventionEngine**: Works alongside for error detection
- **B3-EffectSizeExtractor**: Upstream data source

## References

- Borenstein et al. (2021). Introduction to Meta-Analysis
- Pigott (2012). Advances in Meta-Analysis
- Cochrane Handbook Chapter 6: Extracting data
