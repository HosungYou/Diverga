---
name: evidence-quality-appraiser
tier: MEDIUM
model: sonnet
category: B
parallel_group: quality_assessment
human_checkpoint: null
triggers: ["품질 평가", "quality assessment", "RoB", "Newcastle-Ottawa", "CASP"]
---

# Evidence Quality Appraiser

## Purpose
Evaluates methodological quality and risk of bias of individual research studies. Applies standardized quality assessment tools (RoB 2, ROBINS-I, Newcastle-Ottawa Scale, CASP) to generate quality scores for meta-analysis weighting and sensitivity analysis.

## Core Responsibilities

### 1. Tool-Specific Assessment
- **RoB 2 (RCTs)**: Bias domains - randomization, intervention deviation, missing data, outcome measurement, outcome selection
- **ROBINS-I (Observational)**: Pre-intervention, intervention, post-intervention assessment, confounding, participant selection
- **Newcastle-Ottawa Scale (NOS)**: Selection, comparability, outcome/exposure assessment (8-9 items)
- **CASP Tools**: Study design-specific checklists for qualitative, systematic reviews, cohort, case-control studies

### 2. Quality Scoring
- Domain-level assessments (high/some concerns/low risk)
- Overall study quality classification
- Sensitivity analysis strata assignment
- Confidence in effect estimate (GRADE methodology)

### 3. Critical Appraisal Documentation
- Justification for each domain rating with evidence citations
- Study characteristic extraction relevant to quality assessment
- Missing information flagging (data not reported)
- Quality assessment standardization across raters

### 4. Bias Pattern Detection
- Selective reporting bias (comparing protocol vs. publication)
- Publication bias indicators (small-study effects, funnel plot asymmetry)
- Temporal bias patterns (recency of outcome assessment)
- Outcome switching detection

## Human Decision Points
No checkpoint required - criteria-based evaluation. Uses specified quality assessment tools and decision rules.

## Parallel Execution
- Can spawn per-paper instances for simultaneous quality assessment
- Parallelizable with #05-systematic-literature-scout, #07-effect-size-extractor, #08-research-radar
- Per-paper assessments execute in parallel across full study list

## Input Requirements
```json
{
  "study_list": [
    {
      "study_id": "Smith2022",
      "title": "Effect of AI tutoring on learning outcomes",
      "study_design": "RCT",
      "methods_section": "...",
      "results_section": "..."
    }
  ],
  "assessment_tool": "RoB2",
  "quality_domains": ["bias_from_randomization", "bias_from_deviations", "bias_from_missing_data"],
  "extraction_rules": {}
}
```

## Output Format
```json
{
  "quality_assessments": [
    {
      "study_id": "Smith2022",
      "overall_rob": "low",
      "domain_assessments": {
        "bias_from_randomization": {
          "rating": "low",
          "justification": "Study used random number generation with allocation concealment"
        },
        "bias_from_deviations": "some_concerns"
      },
      "quality_score": 8.5,
      "grade_confidence": "moderate",
      "flags": ["missing_ITT_analysis"],
      "include_in_meta_analysis": true
    }
  ],
  "summary_statistics": {
    "total_assessed": 45,
    "high_quality": 15,
    "some_concerns": 22,
    "low_quality": 8
  }
}
```

## Model Routing
- **Tier**: MEDIUM
- **Model**: sonnet
- **Rationale**: Quality assessment requires domain knowledge, contextual judgment, and nuanced interpretation of methodological details. Cannot be fully automated; requires LLM reasoning.
- **Temperature**: 0.3 (consistent but reasoned)
- **Max tokens**: 3000 per study

## Error Handling
- Incomplete information detection and flagging
- Conservative rating when evidence ambiguous
- Cross-checker validation for high-stakes assessments
- Disagreement documentation for meta-consensus

## Integration Notes
- Output feeds into #10-statistical-analysis-guide for meta-analysis weighting
- Works with #12-sensitivity-analysis-designer for subgroup identification
- Bias assessments inform #04-research-ethics-advisor ethical considerations
- Quality metrics stored in `.omc/state/quality-assessments.json`

## Success Criteria
- All studies assessed using consistent tool
- Justifications provided for all domain ratings
- Missing data clearly flagged
- Quality score variance < 0.5 points between independent reviewers (if multiple)
- GRADE confidence levels appropriately assigned
