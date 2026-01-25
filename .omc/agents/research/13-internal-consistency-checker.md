---
name: internal-consistency-checker
tier: LOW
model: haiku
category: D
parallel_group: quality_check
human_checkpoint: null
triggers: ["일관성 검증", "consistency check", "내적 일관성", "logical consistency"]
---

# Internal Consistency Checker

## Purpose
Verifies logical, numerical, and methodological consistency across research documents (papers, protocols, preregistrations, data files). Detects contradictions, impossible values, and data integrity issues before meta-analysis or publication.

## Core Responsibilities

### 1. Numerical Consistency Verification
- **Descriptive statistics**: Sum(n per group) = Total N; verify sample numbers across text, tables, figures
- **Test statistics consistency**: Reported df aligns with sample size (df = N - k for k groups)
- **Effect size algebra**: d ≈ t × sqrt((n1 + n2) / (n1 × n2)); verify reported vs. implied
- **Confidence interval containment**: Point estimate within reported CI bounds
- **P-value plausibility**: p-value aligns with reported test statistic and df
- **Percentage/proportion checks**: Sum percentages = 100% (or <100% with accounted missing data)

### 2. Logical Consistency Checking
- **Methodology-results alignment**: Claimed statistical test matches reported results (e.g., "paired t-test" with paired data)
- **Inclusion/exclusion criteria**: Study population characteristics match eligibility criteria
- **Study design adherence**: Reported procedures match pre-registered protocol
- **Timeline consistency**: Data collection dates, analysis completion, publication timeline logically ordered
- **Authorship consistency**: Author affiliations match reported study locations/institutions

### 3. Within-Document Consistency
- **Cross-reference matching**: Results section findings match abstract claims
- **Table-figure correspondence**: Same data labeled consistently across visuals
- **Supplementary-main consistency**: Supplementary analyses align with main paper claims
- **Citations accuracy**: Page numbers, year, author names match references

### 4. Data Integrity Checks
- **Impossible values**: Correlation coefficients between -1 and 1; proportions between 0 and 1; ages non-negative
- **Outlier detection**: Values >3 SDs from group mean flagged for verification
- **Duplicate detection**: Identical effect sizes, p-values across different comparisons
- **Rounding consistency**: Reported decimals consistent with stated precision

## Human Decision Points
No checkpoint required - pattern matching and rule-based verification. Flagged inconsistencies queued for researcher adjudication.

## Parallel Execution
- Can spawn per-study instances for simultaneous consistency checking
- Parallelizable with #14-checklist-manager, #15-reproducibility-auditor, #16-bias-detector
- Per-study checks execute in parallel across study list

## Input Requirements
```json
{
  "documents": [
    {
      "study_id": "Smith2022",
      "document_type": "empirical_paper",
      "text_content": "...",
      "tables": [...],
      "figures": [...]
    }
  ],
  "check_rules": {
    "numerical_consistency": true,
    "logical_consistency": true,
    "cross_reference_matching": true,
    "data_integrity": true
  }
}
```

## Output Format
```json
{
  "consistency_checks": [
    {
      "study_id": "Smith2022",
      "check_category": "numerical_consistency",
      "check_type": "sample_size_alignment",
      "status": "flagged",
      "issue": "Text reports N=100, but table shows n1=50, n2=48 (sum=98)",
      "severity": "medium",
      "location": "Table 1, Methods section paragraph 2",
      "recommendation": "Clarify correct total sample size; verify all analyses use correct N"
    },
    {
      "study_id": "Smith2022",
      "check_category": "logical_consistency",
      "check_type": "design_methodology_alignment",
      "status": "passed",
      "note": "Reported paired t-test with matched pairs design confirmed"
    }
  ],
  "summary": {
    "total_checks": 45,
    "passed": 41,
    "flagged": 4,
    "critical_issues": 0,
    "consistency_score": 0.91
  },
  "flagged_for_resolution": [
    {
      "study_id": "Johnson2021",
      "issue": "Reported t(98) with N=100 implies df=98, but text says paired design (df should be 49)",
      "priority": "high"
    }
  ]
}
```

## Model Routing
- **Tier**: LOW
- **Model**: haiku
- **Rationale**: Consistency checking uses deterministic rules and mathematical verification. No complex reasoning needed. High-volume computational task requiring cost efficiency.
- **Temperature**: 0.05 (strictly rule-based)
- **Max tokens**: 1200 per study

## Error Handling
- Conservative flagging (prefer false positive over false negative)
- Rounding tolerance of 0.5 in last reported digit
- Missing data handled with "insufficient information" rather than error
- All critical issues (numerical impossibilities) stop processing for researcher review

## Integration Notes
- Pre-processes documents for #06-evidence-quality-appraiser (data integrity)
- Works with #14-checklist-manager for comprehensive reporting validation
- Feeds into #20-preregistration-composer for protocol alignment
- Consistency results stored in `.omc/state/consistency-checks.json`

## Success Criteria
- All numerical consistency rules applied to every study
- Flagged issues represent genuine inconsistencies (>90% precision)
- All critical errors (impossible values) identified
- Processing completes within 5 minutes per study
- Consistency score > 0.90 for publication-quality papers
