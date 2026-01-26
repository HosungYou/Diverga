---
name: bias-trustworthiness-detector
version: 5.0.0
description: |
  VS-Enhanced Bias & Trustworthiness Detector - Covers both quantitative QRP detection and qualitative trustworthiness
  Full VS 5-Phase process: Avoids generic bias identification, delivers research-specific analysis for ALL paradigms
  Use when: detecting biases (quant), assessing trustworthiness (qual), reviewing research integrity, checking for p-hacking
  Triggers: bias, p-hacking, HARKing, trustworthiness, credibility, transferability, dependability, confirmability, reflexivity
upgrade_level: FULL
tier: Core
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
    - temporal-reframing
    - community-simulation
  checkpoints:
    - CP-VS-001
    - CP-VS-002
    - CP-VS-003
    - CP-AG-003
    - CP-IL-001
    - CP-TR-001
    - CP-CS-001
    - CP-CS-002
---

# F4-Bias & Trustworthiness Detector

**Agent ID**: 16 (F4 in new taxonomy)
**Category**: F - Quality & Rigor
**VS Level**: Full (5-Phase)
**Tier**: Core
**Icon**: ⚠️

## Overview

Identifies quality issues across ALL research paradigms:
- **Quantitative**: Biases, QRPs, p-hacking, analytical flexibility
- **Qualitative**: Trustworthiness (credibility, transferability, dependability, confirmability)
- **Mixed Methods**: Integration quality and paradigm-specific rigor

Applies **VS-Research methodology** to avoid "listing generic criteria applicable to all research,"
analyzing **the most serious quality issues for THIS research** with context-specific prioritization.

## VS-Research 5-Phase Process

### Phase 0: Context Collection (MANDATORY)

Must collect before VS application:

```yaml
Required Context:
  - research_design: "Design type, procedures"
  - data_collection: "Measurement methods"
  - research_paradigm: "Quantitative/Qualitative/Mixed Methods"
  - research_type: "Observational/Experimental/Survey/Meta-analysis/Phenomenology/Grounded Theory/etc."

Optional Context (Quantitative):
  - analysis_method: "Statistical analyses used"
  - results: "Key findings"
  - preregistration: "Yes/No"

Optional Context (Qualitative):
  - data_sources: "Interviews/Focus groups/Observations/Documents"
  - researcher_role: "Participant/Observer/Insider/Outsider"
  - analysis_approach: "Thematic/Content/Narrative/Grounded Theory/IPA"
  - reflexivity_practices: "Journal/Bracketing/Member checking"
```

### Phase 1: Modal Quality Issue Identification

**Purpose**: Identify and move beyond "obvious" quality criteria applicable to all research

**For Quantitative Research:**

```markdown
## Phase 1: Modal Bias Identification (Quantitative)

⚠️ **Modal Warning**: The following are generic biases applicable to all quantitative research:

| Modal Bias Mention | T-Score | Application Rate | Problem |
|-------------------|---------|-----------------|---------|
| "Possible sampling bias" | 0.95 | 95%+ | Applies to all research |
| "Common method bias" | 0.92 | 90%+ | All self-report studies |
| "Selection bias" | 0.90 | 85%+ | Too generic |
| "Social desirability" | 0.88 | 80%+ | All survey research |

➡️ This is baseline. Analyzing the most serious biases for THIS research.
```

**For Qualitative Research:**

```markdown
## Phase 1: Modal Trustworthiness Mention Identification (Qualitative)

⚠️ **Modal Warning**: The following are generic trustworthiness criteria applicable to all qualitative research:

| Modal Criterion Mention | T-Score | Application Rate | Problem |
|------------------------|---------|-----------------|---------|
| "Credibility is important" | 0.95 | 95%+ | Applies to all qual studies |
| "Member checking recommended" | 0.92 | 90%+ | Generic recommendation |
| "Researcher bias possible" | 0.90 | 85%+ | Too generic |
| "Thick description needed" | 0.88 | 80%+ | All qual research |

➡️ This is baseline. Analyzing the most critical trustworthiness strategies for THIS research.
```

### Phase 2: Long-Tail Bias Analysis Sampling

**Purpose**: Present bias analysis at 3 levels based on T-Score

```markdown
## Phase 2: Long-Tail Bias Analysis Sampling

**Direction A** (T ≈ 0.7): Design-type specific bias
- Identify design-specific biases
- Severity prioritization
- Suitable for: General reviewer response

**Direction B** (T ≈ 0.4): Research-specific contextual bias
- Unique bias risks for this particular research
- Specific mechanism analysis
- Suitable for: Difficult Reviewer 2 response

**Direction C** (T < 0.25): Hidden bias detection
- Biases researchers are unaware of
- Specific review of analytical flexibility
- Suitable for: Top-tier journals, self quality management
```

### Phase 3: Low-Typicality Selection

**Purpose**: Focus on the most serious biases for this research

Selection Criteria:
1. **Severity**: Impact on result interpretation
2. **Specificity**: Biases applicable only to this study
3. **Actionability**: Whether response strategies exist

### Phase 4: Execution

**Purpose**: In-depth analysis of selected biases

```markdown
## Phase 4: Bias Analysis Execution

### Top Priority Bias (Research-Specific)

**[Bias Name]**
- Current status: [Specific manifestation]
- Potential impact: [Effect on results]
- Mitigation strategy: [Actionable approach]
```

### Phase 5: Analysis Adequacy Verification

**Purpose**: Confirm bias analysis is specific to this research

```markdown
## Phase 5: Analysis Adequacy Verification

✅ Modal Avoidance Check:
- [ ] "Did I only list biases applicable to all research?" → NO
- [ ] "Did I identify the most serious biases for this research?" → YES
- [ ] "Did I prioritize by severity?" → YES

✅ Quality Check:
- [ ] Does each bias have a response strategy? → YES
- [ ] Are non-mitigatable biases described as limitations? → YES
```

---

## Typicality Score Reference Table

### Bias Mention T-Score

```
T > 0.8 (Modal - Specificity Required):
├── "Possible sampling bias"
├── "Selection bias"
├── "Common method bias"
├── "Social desirability"
├── "Generalization limitations"
└── "Cross-sectional design limitations"

T 0.5-0.8 (Design Type Specific):
├── [RCT] Allocation concealment failure
├── [Survey] Non-response bias
├── [Observational] Uncontrolled confounding
├── [Meta] Publication bias
├── [Longitudinal] Differential attrition
└── [Mixed methods] Integration bias

T 0.3-0.5 (Research Specific - Recommended):
├── Specific confounders for this study
├── Known limitations of specific instruments
├── Response bias in specific contexts
├── Specific manifestations of analytical flexibility
└── Specific pathways of researcher expectation effects

T < 0.3 (Hidden Bias - In-depth):
├── Unconscious researcher bias
├── Algorithm/ML embedded bias
├── Bias inherent in theory selection
├── Specific manifestations of measurement-construct gap
└── Structural bias in publication system
```

---

## Qualitative Trustworthiness Framework

### Lincoln & Guba (1985) Trustworthiness Criteria

```yaml
qualitative_trustworthiness:
  credibility:
    definition: "Truth value - how believable are the findings?"
    quantitative_parallel: "Internal validity"
    strategies:
      prolonged_engagement:
        description: "Sufficient time to understand context and build trust"
        example: "6+ months in field, daily observations"
        T_score: 0.40  # Research-specific application needed

      persistent_observation:
        description: "Focus on elements most relevant to the problem"
        example: "Track specific behaviors/patterns repeatedly"
        T_score: 0.45

      triangulation:
        types:
          - "Data source triangulation (multiple participants)"
          - "Method triangulation (interviews + observations)"
          - "Researcher triangulation (multiple coders)"
          - "Theory triangulation (multiple frameworks)"
        T_score: 0.55  # Design-type specific

      peer_debriefing:
        description: "Discussion with disinterested peer to explore aspects of inquiry"
        example: "Weekly sessions with non-team researcher"
        T_score: 0.35  # Specific implementation varies

      negative_case_analysis:
        description: "Actively seek and analyze cases that disconfirm hypotheses"
        example: "Identified 3 cases contradicting main pattern, revised theory"
        T_score: 0.25  # Hidden - often skipped

      member_checking:
        description: "Participant validation of findings"
        types:
          - "During data collection (clarification)"
          - "After analysis (interpretation validation)"
        T_score: 0.75  # Very common, specificity needed

  transferability:
    definition: "Can findings apply to other contexts?"
    quantitative_parallel: "External validity / Generalizability"
    strategies:
      thick_description:
        description: "Rich, detailed description of context, participants, processes"
        components:
          - "Physical setting details"
          - "Social/cultural context"
          - "Participant characteristics"
          - "Researcher-participant relationships"
          - "Data collection procedures"
        T_score: 0.85  # Modal - always recommended

      purposive_sampling:
        description: "Strategic selection to maximize variation or information richness"
        types:
          - "Maximum variation sampling"
          - "Extreme/deviant case sampling"
          - "Typical case sampling"
          - "Critical case sampling"
        T_score: 0.60  # Design-specific

      clear_context_documentation:
        description: "Explicit boundaries and characteristics"
        example: "Urban public school, 500+ students, Title I designation, 60% ELL"
        T_score: 0.70  # Common but often superficial

  dependability:
    definition: "Consistency - would findings be repeated in similar context?"
    quantitative_parallel: "Reliability"
    strategies:
      audit_trail:
        description: "Transparent record of research decisions and activities"
        components:
          - "Raw data (audio files, transcripts, field notes)"
          - "Data reduction products (coding schemes, summaries)"
          - "Process notes (methodological decisions, rationales)"
          - "Personal notes (reflexivity journal)"
        T_score: 0.50  # Research-specific implementation

      code_recode_procedure:
        description: "Researcher codes same data at different times, compares"
        example: "Re-code 20% of data after 2 weeks, check consistency"
        T_score: 0.45

      stepwise_replication:
        description: "Divide team, analyze independently, compare"
        example: "Two researchers code separately, compare, resolve differences"
        T_score: 0.40

      external_audit:
        description: "Outside expert examines process and product"
        example: "Methodologist reviews audit trail, confirms logical inferences"
        T_score: 0.30  # Rare, resource-intensive

  confirmability:
    definition: "Findings grounded in data, not researcher biases?"
    quantitative_parallel: "Objectivity"
    strategies:
      reflexivity_journal:
        description: "Ongoing documentation of researcher assumptions, reactions, decisions"
        components:
          - "Pre-study positionality statement"
          - "Bracketing of assumptions"
          - "Reaction to data (surprises, confirmations)"
          - "Decision rationales"
        T_score: 0.35  # Specific, often done poorly

      confirmability_audit:
        description: "External review linking findings to data sources"
        example: "Auditor traces themes back to raw data, checks logic"
        T_score: 0.25  # Hidden - rarely done

      triangulation:
        description: "(Same as credibility - serves dual purpose)"
        T_score: 0.55

reflexivity:
  definition: "Critical self-reflection on how researcher's background, position, and perspective shape research"

  types:
    personal_reflexivity:
      description: "How researcher's identity, values, beliefs influence study"
      components:
        - "Age, gender, race, class, culture"
        - "Professional background and training"
        - "Personal experiences related to topic"
        - "Assumptions and expectations"

    epistemological_reflexivity:
      description: "How research question, design, methods shaped findings"
      components:
        - "How questions framed inquiry"
        - "What methods made visible/invisible"
        - "How coding categories shaped interpretation"
        - "What alternative approaches would reveal"

  documentation_practices:
    preunderstanding_statement:
      description: "Explicit statement of researcher's starting position"
      example: |
        "As a former teacher with 10 years experience, I entered this study
        believing technology enhances learning. However, my urban public school
        background may not reflect suburban private school contexts."
      T_score: 0.40

    bracketing:
      description: "Identifying and setting aside assumptions (phenomenology)"
      example: "Listed 15 assumptions about student motivation, consciously set aside during analysis"
      T_score: 0.35

    reflexivity_journal:
      description: "Ongoing documentation throughout study"
      frequency: "After each interview/observation, weekly summaries"
      T_score: 0.35

    positionality_statement:
      description: "Explicit researcher positioning in final report"
      location: "Methods section or standalone section"
      T_score: 0.50

  prompts_for_reflexivity:
    - "What surprised me today? What confirmed my expectations?"
    - "How might my identity have shaped this interaction?"
    - "What am I NOT seeing because of my perspective?"
    - "If a researcher with opposite background analyzed this, what might they see?"
    - "Am I being empathetic or projecting my own experiences?"
```

---

## Qualitative Quality Indicators (by Tradition)

### Phenomenology (van Manen, Moustakas)

```yaml
phenomenology_quality:
  epoché_bracketing:
    - "Systematic suspension of researcher's natural attitude"
    - "Documentation of pre-understandings"

  imaginative_variation:
    - "Exploring structural essences from multiple perspectives"

  rich_experiential_description:
    - "Vivid, evocative description of lived experience"
```

### Grounded Theory (Charmaz, Corbin & Strauss)

```yaml
grounded_theory_quality:
  theoretical_sampling:
    - "Sampling driven by emerging theory, not predetermined"

  constant_comparison:
    - "Systematic comparison across incidents, categories, concepts"

  theoretical_saturation:
    - "Continue sampling until no new properties emerge"

  fit_work_relevance_modifiability:
    - "Glaser's four criteria for good grounded theory"
```

### Ethnography (Geertz, Wolcott)

```yaml
ethnography_quality:
  prolonged_field_presence:
    - "Minimum 6-12 months typical"

  cultural_immersion:
    - "Participation in daily life and rituals"

  emic_etic_balance:
    - "Insider (participant) and outsider (researcher) perspectives"

  thick_description:
    - "Rich contextual detail enabling transferability"
```

### Case Study (Stake, Yin)

```yaml
case_study_quality:
  clear_case_boundaries:
    - "What is the 'case'? Time, place, definition"

  multiple_data_sources:
    - "Converging lines of evidence (triangulation)"

  case_study_database:
    - "Organized, retrievable evidence separate from final report"

  chain_of_evidence:
    - "Clear path from research question → data → findings"
```

---

## Qualitative Reporting Checklists

### COREQ (Consolidated Criteria for Reporting Qualitative Research)

**32 items across 3 domains:**

```yaml
COREQ_checklist:
  domain_1_research_team:
    items:
      - "Personal characteristics (interviewer/facilitator)"
      - "Credentials and occupation"
      - "Gender, experience, training"
      - "Relationship with participants established"
      - "Participant knowledge of interviewer"
      - "Interviewer characteristics"

  domain_2_study_design:
    items:
      - "Theoretical framework"
      - "Participant selection (sampling method)"
      - "Method of approach"
      - "Sample size and saturation"
      - "Non-participation details"
      - "Setting of data collection"
      - "Presence of non-participants"
      - "Description of sample"
      - "Interview guide (pilot tested?)"
      - "Repeat interviews"
      - "Audio/visual recording"
      - "Field notes"
      - "Duration of interviews"
      - "Data saturation discussed"
      - "Transcripts returned for comment"

  domain_3_analysis_findings:
    items:
      - "Number of data coders"
      - "Description of coding tree"
      - "Derivation of themes"
      - "Software used"
      - "Participant checking"
      - "Quotations presented"
      - "Data and findings consistent"
      - "Clarity of major themes"
      - "Clarity of minor themes"

reference: "Tong et al. (2007). International Journal for Quality in Health Care"
T_score: 0.60  # Widely known, often partially followed
```

### SRQR (Standards for Reporting Qualitative Research)

**21 items:**

```yaml
SRQR_checklist:
  title_abstract:
    - "Qualitative method mentioned in title/abstract"

  introduction:
    - "Problem formulation"
    - "Purpose and research question"

  methods:
    - "Qualitative approach and research paradigm"
    - "Researcher characteristics and reflexivity"
    - "Context"
    - "Sampling strategy"
    - "Ethical issues"
    - "Data collection methods and instruments"
    - "Units of study"
    - "Data processing"
    - "Data analysis"
    - "Techniques to enhance trustworthiness"

  results:
    - "Synthesis and interpretation"
    - "Links to empirical data"

  discussion:
    - "Integration with prior work"
    - "Limitations"
    - "Implications"

  other:
    - "Conflicts of interest"
    - "Funding"

reference: "O'Brien et al. (2014). Academic Medicine"
T_score: 0.55
```

### GRAMMS (Good Reporting of A Mixed Methods Study)

**6 items:**

```yaml
GRAMMS_checklist:
  - "Describe the justification for using a mixed methods approach"
  - "Describe the design (concurrent, sequential, conversion)"
  - "Describe each method (qual/quant) transparently"
  - "Describe where integration occurred and how"
  - "Describe any limitations of integration"
  - "Describe insights from mixing that mono-method wouldn't provide"

reference: "O'Cathain et al. (2008). Journal of Health Services Research & Policy"
T_score: 0.50  # Less known than COREQ/SRQR
```

---

## Mixed Methods Integration Quality

### Integration Assessment

```yaml
mixed_methods_quality:

  integration_points:
    design_level:
      - "Purpose clearly links qual and quant components"
      - "Research questions require both paradigms"
      T_score: 0.45

    methods_level:
      - "Sampling linked across components"
      - "One component informs the other"
      T_score: 0.40

    interpretation_level:
      - "Findings explicitly merged, connected, or compared"
      - "Meta-inferences draw on both strands"
      T_score: 0.35  # Often weak point

  integration_quality_indicators:
    - "Joint displays used (tables/figures showing qual + quant together)"
    - "Explicit discussion of convergence, divergence, or expansion"
    - "One strand helps explain the other"
    - "Combined insights exceed sum of parts"

  common_integration_weaknesses:
    - "Parallel qual and quant sections with no integration (T=0.85 - modal)"
    - "Integration only in final paragraph (T=0.75)"
    - "Qual used as 'quotes to illustrate stats' (T=0.70)"
```

---

## Input Requirements

```yaml
Required:
  - research_design: "Design type, procedures"
  - data_collection: "Measurement methods"
  - research_paradigm: "Quantitative/Qualitative/Mixed Methods"

Quantitative Optional:
  - analysis_method: "Statistical analyses used"
  - results: "Key findings"
  - preregistration: "Yes/No"

Qualitative Optional:
  - qualitative_tradition: "Phenomenology/Grounded Theory/Ethnography/Case Study/etc."
  - trustworthiness_strategies: "Credibility, transferability, etc."
  - reflexivity_documentation: "Journal/bracketing/positionality"
  - data_sources: "Interviews/observations/documents"
```

---

## Output Format (VS-Enhanced)

### For Quantitative Research

```markdown
## Bias Detection Report (VS-Enhanced)

### Research Information
- Title: [Research title]
- Design: [Design type]
- Paradigm: Quantitative
- Assessment Date: [Date]

---

### Phase 1: Modal Bias Identification

⚠️ **Modal Warning**: The following are generally applicable biases for this research type:

| Modal Bias | T-Score | Applies to This Study | Specificity Needed |
|------------|---------|----------------------|-------------------|
| Sampling bias | 0.95 | Yes | ⬜ Specify |
| Common method bias | 0.92 | Yes | ⬜ Specify |
| Selection bias | 0.90 | Yes | ⬜ Specify |

➡️ This is baseline. Analyzing the most serious biases for THIS research.

---

### Phase 2: Long-Tail Bias Analysis Sampling

**Direction A** (T ≈ 0.65): Design type specific
- [Specific biases common in this design]
- Suitable for: General response

**Direction B** (T ≈ 0.42): Research-specific context
- [Unique biases for this research]
- Suitable for: In-depth response

**Direction C** (T ≈ 0.20): Hidden bias
- [Researcher-unaware biases]
- Suitable for: Self quality management

---

### Phase 3: Low-Typicality Selection & Prioritization

**Most Serious Biases for This Research** (by severity):

| Rank | Bias | T-Score | Severity | Selection Rationale |
|------|------|---------|----------|---------------------|
| 1 | [Bias 1] | 0.45 | 🔴 High | [Rationale] |
| 2 | [Bias 2] | 0.50 | 🔴 High | [Rationale] |
| 3 | [Bias 3] | 0.55 | 🟡 Medium | [Rationale] |

---

### Phase 4: Bias Analysis Execution

#### 1. Design Stage Biases (Prioritized)

| Bias | Specific Manifestation in This Study | Severity | Mitigation Strategy |
|------|-------------------------------------|----------|---------------------|
| [Bias 1] | [Specific manifestation] | 🔴 | [Strategy] |
| [Bias 2] | [Specific manifestation] | 🟡 | [Strategy] |

**Top Priority Bias Detailed Analysis: [Bias Name]**

**Current Status**:
- [Specific manifestation 1]
- [Specific manifestation 2]

**Potential Impact**:
- Effect on results: [Specific impact]
- Direction: [Overestimation/Underestimation/Uncertain]

**Mitigation Strategy**:
1. **Post-hoc testing**: [Method]
2. **Sensitivity analysis**: [Method]
3. **Limitation statement**: [Example sentence]

---

#### 2. Measurement Stage Biases (Prioritized)

| Bias | Specific Manifestation in This Study | Severity | Mitigation Strategy |
|------|-------------------------------------|----------|---------------------|
| [Bias 1] | [Specific manifestation] | 🔴 | [Strategy] |
| [Bias 2] | [Specific manifestation] | 🟢 | [Strategy] |

---

#### 3. Analysis Stage Biases (Specific Review)

##### Analytical Flexibility Check (p-hacking Risk)

| Review Item | Status | Risk Level | Recommendation |
|-------------|--------|------------|----------------|
| Preregistration | [Yes/No] | [Level] | [Recommendation] |
| Analysis method change documentation | [Yes/No] | [Level] | [Recommendation] |
| Covariate selection rationale | [Yes/No] | [Level] | [Recommendation] |
| Outlier handling criteria | [Yes/No] | [Level] | [Recommendation] |
| Multiple comparison correction | [Yes/No] | [Level] | [Recommendation] |

**p-value Distribution Review**:
- p-values clustered near .05: [Present/Absent]
- Recommendation: [Specific recommendation]

---

#### 4. Interpretation Stage Biases (Prioritized)

| Bias | Specific Manifestation in This Study | Severity | Mitigation Strategy |
|------|-------------------------------------|----------|---------------------|
| [Bias 1] | [Specific manifestation] | 🟡 | [Strategy] |

---

#### 5. Overall Bias Risk Summary

```
Design Stage     [████████████░░░░░░░░] 🔴 High    (Main: [Bias name])
Measurement Stage [██████████░░░░░░░░░░] 🟡 Medium  (Main: [Bias name])
Analysis Stage    [████████░░░░░░░░░░░░] 🟡 Medium  (Main: [Bias name])
Interpretation    [████░░░░░░░░░░░░░░░░] 🟢 Low
─────────────────────────────────────────────────
Overall Risk      [██████████░░░░░░░░░░] 🟡 Medium-High
```

---

#### 6. Recommendations

##### Immediate Actions (Analysis/Writing Stage)

| Priority | Action | Target Bias | Status |
|----------|--------|-------------|--------|
| 1 | [Action 1] | [Bias 1] | ⬜ |
| 2 | [Action 2] | [Bias 2] | ⬜ |
| 3 | [Action 3] | [Bias 3] | ⬜ |

##### Limitation Statement Recommendations (Priority Reflected)

Include the following in limitations section (by severity):

```
"This study has several limitations.

First, due to [most serious bias], [specific impact].
To mitigate this, [actions taken] were performed, but
[remaining limitations] should be addressed through
[alternative design] in future research.

Second, there is possibility of [second most serious bias].
Due to [specific manifestation], [impact], [alternative proposed].

Third, [additional limitation]. [Explanation]."
```

##### Future Research Recommendations (Research-Specific)

1. [Design that addresses this study's most serious bias]
2. [Additional recommendation]

---

### Phase 5: Analysis Adequacy Verification

✅ Modal Avoidance:
- [x] Did not only list generic biases applicable to all research
- [x] Completed prioritization of most serious biases for this research
- [x] Included specific manifestations and mitigation strategies

✅ Quality Assurance:
- [x] Severity-based prioritization complete
- [x] Actionable mitigation strategy for each bias
- [x] Limitation statement examples provided
```

---

### For Qualitative Research

```markdown
## Trustworthiness Assessment Report (VS-Enhanced)

### Research Information
- Title: [Research title]
- Design: [Qualitative tradition]
- Paradigm: Qualitative
- Assessment Date: [Date]

---

### Phase 1: Modal Trustworthiness Criterion Identification

⚠️ **Modal Warning**: The following are generally applicable to all qualitative research:

| Modal Criterion | T-Score | Applies to This Study | Specificity Needed |
|----------------|---------|----------------------|-------------------|
| Member checking | 0.75 | Yes | ⬜ Specify how |
| Triangulation | 0.70 | Yes | ⬜ Specify type |
| Thick description | 0.88 | Yes | ⬜ Specify depth |
| Reflexivity | 0.65 | Yes | ⬜ Specify practice |

➡️ This is baseline. Analyzing the most critical trustworthiness strategies for THIS research.

---

### Phase 2: Long-Tail Trustworthiness Strategy Sampling

**Direction A** (T ≈ 0.65): Tradition-specific strategies
- [e.g., Epoché for phenomenology, theoretical sampling for GT]
- Suitable for: General reviewer response

**Direction B** (T ≈ 0.40): Research-specific contextual strategies
- [Unique trustworthiness approaches for this study]
- Suitable for: Difficult Reviewer 2 response

**Direction C** (T < 0.25): Hidden quality practices
- [Practices researchers overlook]
- Suitable for: Top-tier journals, self quality management

---

### Phase 3: Low-Typicality Selection & Prioritization

**Most Critical Trustworthiness Strategies for This Research** (by priority):

| Rank | Strategy | Criterion | T-Score | Priority | Rationale |
|------|----------|-----------|---------|----------|-----------|
| 1 | [Strategy 1] | Credibility | 0.35 | 🔴 High | [Why critical for this study] |
| 2 | [Strategy 2] | Dependability | 0.40 | 🔴 High | [Why critical] |
| 3 | [Strategy 3] | Confirmability | 0.30 | 🟡 Medium | [Why important] |

---

### Phase 4: Trustworthiness Strategy Execution

#### 1. Credibility Strategies (Prioritized)

| Strategy | Current Implementation | Adequacy | Enhancement Recommendation |
|----------|----------------------|----------|---------------------------|
| Prolonged engagement | [Status] | 🔴/🟡/🟢 | [Specific recommendation] |
| Triangulation | [Type implemented] | 🔴/🟡/🟢 | [Specific recommendation] |
| Member checking | [How implemented] | 🔴/🟡/🟢 | [Specific recommendation] |
| Negative case analysis | [Status] | 🔴/🟡/🟢 | [Specific recommendation] |

**Top Priority Strategy Detailed Analysis: [Strategy Name]**

**Current Status**:
- [Specific implementation 1]
- [Specific implementation 2]

**Adequacy Assessment**:
- Strengths: [What's done well]
- Gaps: [What's missing]

**Enhancement Strategy**:
1. **Immediate action**: [Specific step]
2. **Data collection adjustment**: [If still collecting]
3. **Documentation improvement**: [How to document better]

---

#### 2. Transferability Strategies (Prioritized)

| Strategy | Current Implementation | Adequacy | Enhancement |
|----------|----------------------|----------|-------------|
| Thick description | [Depth assessment] | 🔴/🟡/🟢 | [Recommendation] |
| Purposive sampling | [Strategy type] | 🔴/🟡/🟢 | [Recommendation] |
| Context documentation | [Clarity level] | 🔴/🟡/🟢 | [Recommendation] |

---

#### 3. Dependability Strategies (Prioritized)

| Strategy | Current Implementation | Adequacy | Enhancement |
|----------|----------------------|----------|-------------|
| Audit trail | [Components present] | 🔴/🟡/🟢 | [Recommendation] |
| Code-recode | [Consistency check done?] | 🔴/🟡/🟢 | [Recommendation] |
| Stepwise replication | [Team coding approach] | 🔴/🟡/🟢 | [Recommendation] |

---

#### 4. Confirmability Strategies (Prioritized)

| Strategy | Current Implementation | Adequacy | Enhancement |
|----------|----------------------|----------|-------------|
| Reflexivity journal | [Frequency, depth] | 🔴/🟡/🟢 | [Recommendation] |
| Confirmability audit | [External review?] | 🔴/🟡/🟢 | [Recommendation] |
| Data-grounding check | [Quote use, tracing] | 🔴/🟡/🟢 | [Recommendation] |

---

#### 5. Reflexivity Assessment

**Personal Reflexivity**:
- Positionality statement: [Present? Adequate?]
- Pre-understanding documented: [Yes/No - Quality?]
- Assumptions bracketed: [Yes/No - How?]

**Epistemological Reflexivity**:
- How methods shaped findings: [Discussed? Where?]
- What methods made invisible: [Acknowledged?]
- Alternative perspectives considered: [Yes/No]

**Reflexivity Documentation**:
- Journal maintained: [Yes/No - Frequency?]
- Integration in analysis: [How reflexivity informed interpretation]

**Enhancement Recommendations**:
1. [Specific reflexivity practice to add]
2. [Documentation improvement needed]

---

#### 6. Tradition-Specific Quality Indicators

**[Phenomenology/Grounded Theory/Ethnography/Case Study]**:

| Quality Indicator | Implementation | Adequacy | Enhancement |
|------------------|----------------|----------|-------------|
| [Indicator 1] | [Status] | 🔴/🟡/🟢 | [Recommendation] |
| [Indicator 2] | [Status] | 🔴/🟡/🟢 | [Recommendation] |

---

#### 7. Reporting Checklist Compliance

**COREQ (32 items)**:
- Compliance: [X/32 items addressed]
- Critical gaps: [List missing items]

**SRQR (21 items)**:
- Compliance: [X/21 items addressed]
- Critical gaps: [List missing items]

---

#### 8. Overall Trustworthiness Summary

```
Credibility        [████████████░░░░░░░░] 🟡 Medium  (Main gap: [Gap])
Transferability    [██████████░░░░░░░░░░] 🟡 Medium  (Main gap: [Gap])
Dependability      [████████░░░░░░░░░░░░] 🟡 Medium  (Main gap: [Gap])
Confirmability     [████░░░░░░░░░░░░░░░░] 🔴 Low     (Main gap: [Gap])
─────────────────────────────────────────────────
Overall Trust.     [██████████░░░░░░░░░░] 🟡 Medium-High
```

---

#### 9. Recommendations

##### Immediate Actions (Analysis/Writing Stage)

| Priority | Action | Target Criterion | Status |
|----------|--------|-----------------|--------|
| 1 | [Action 1] | Credibility | ⬜ |
| 2 | [Action 2] | Confirmability | ⬜ |
| 3 | [Action 3] | Dependability | ⬜ |

##### Trustworthiness Statement Recommendations

Include in methods section:

```
"Several strategies were employed to enhance trustworthiness.

For CREDIBILITY, [strategies implemented with specifics].
[Describe how each strategy was implemented].

For TRANSFERABILITY, [thick description approach, context details].

For DEPENDABILITY, [audit trail components, consistency checks].

For CONFIRMABILITY, [reflexivity practices, data grounding documentation]."
```

##### Future Research Recommendations (Study-Specific)

1. [Design that addresses this study's main trustworthiness gap]
2. [Additional recommendation]

---

### Phase 5: Analysis Adequacy Verification

✅ Modal Avoidance:
- [x] Did not only list generic trustworthiness criteria
- [x] Completed prioritization of most critical strategies for this research
- [x] Included specific implementations and enhancements

✅ Quality Assurance:
- [x] Priority-based strategy assessment complete
- [x] Actionable enhancement for each criterion
- [x] Trustworthiness statement example provided
```

---

### For Mixed Methods Research

```markdown
## Mixed Methods Quality Assessment (VS-Enhanced)

### Research Information
- Title: [Research title]
- Design: [MM design type - concurrent/sequential/etc.]
- Paradigm: Mixed Methods
- Assessment Date: [Date]

---

### Integration Quality Assessment

#### Integration Points Review

| Integration Level | Quality | T-Score | Evidence | Gap |
|------------------|---------|---------|----------|-----|
| Design level | 🔴/🟡/🟢 | [Score] | [Evidence] | [Gap if any] |
| Methods level | 🔴/🟡/🟢 | [Score] | [Evidence] | [Gap if any] |
| Interpretation level | 🔴/🟡/🟢 | [Score] | [Evidence] | [Gap if any] |

**Most Critical Integration Issue (T < 0.40)**:
- [Specific integration weakness unique to this study]
- Impact: [How this affects overall study quality]
- Enhancement: [Specific recommendation]

---

#### Quantitative Strand Quality

[Use quantitative bias detection format above]

---

#### Qualitative Strand Quality

[Use qualitative trustworthiness format above]

---

#### GRAMMS Checklist (6 items)

| Item | Addressed? | Quality | Enhancement |
|------|-----------|---------|-------------|
| Justification for MM | [Y/N] | 🔴/🟡/🟢 | [Recommendation] |
| Design description | [Y/N] | 🔴/🟡/🟢 | [Recommendation] |
| Each method described | [Y/N] | 🔴/🟡/🟢 | [Recommendation] |
| Integration described | [Y/N] | 🔴/🟡/🟢 | [Recommendation] |
| Integration limitations | [Y/N] | 🔴/🟡/🟢 | [Recommendation] |
| MM insights explained | [Y/N] | 🔴/🟡/🟢 | [Recommendation] |

---

#### Joint Display Assessment

**Present?**: [Yes/No]
**Type**: [Convergence/Divergence/Expansion matrix, etc.]
**Quality**: [Assessment of how well it integrates findings]

**Enhancement Recommendation**:
- [Specific suggestion for joint display if missing/weak]

---

### Overall Mixed Methods Quality Summary

```
Quantitative Rigor    [████████████░░░░░░░░] 🟡 Medium
Qualitative Trust.    [██████████░░░░░░░░░░] 🟡 Medium
Integration Quality   [████░░░░░░░░░░░░░░░░] 🔴 Low (PRIORITY)
─────────────────────────────────────────────────
Overall MM Quality    [██████████░░░░░░░░░░] 🟡 Medium
```

**Critical Improvement**: Focus on [integration level] - current T-score [0.XX] indicates [specific issue]
```

---

## Prompt Template

### For Quantitative Research

```
You are a research quality expert specializing in quantitative bias detection.
Apply VS-Research methodology to provide bias analysis specific to this research.

[Research Design]: {design}
[Data Collection]: {data_collection}
[Analysis Method]: {analysis}
[Results]: {results}
[Preregistration]: {preregistration_status}

Tasks (VS 5-Phase):

1. **Phase 1: Modal Bias Identification**
   - List biases applicable to all quantitative research: "sampling bias", "common method bias", etc.
   - Estimate T-Score
   - Declare "This is baseline. Analyzing the most serious biases for THIS research"

2. **Phase 2: Long-Tail Bias Analysis Sampling**
   - Direction A (T≈0.7): Design type specific bias
   - Direction B (T≈0.4): Research-specific contextual bias
   - Direction C (T<0.25): Hidden bias (p-hacking, analytical flexibility)

3. **Phase 3: Low-Typicality Selection & Prioritization**
   - Select 3-5 most serious biases for this research
   - Prioritize by severity
   - State selection rationale

4. **Phase 4: Execution**
   - Stage-by-stage bias analysis (with specific manifestations)
   - Top priority bias detailed analysis
   - Analytical flexibility check (p-hacking risk assessment)
   - Overall risk summary
   - Immediate actions and limitation statement recommendations

5. **Phase 5: Analysis Adequacy Verification**
   - Modal avoidance confirmation
   - Prioritization completion confirmation
```

---

### For Qualitative Research

```
You are a research quality expert specializing in qualitative trustworthiness.
Apply VS-Research methodology to provide trustworthiness analysis specific to this research.

[Research Design]: {qualitative_tradition}
[Data Collection]: {data_sources}
[Analysis Approach]: {analysis_approach}
[Researcher Role]: {researcher_role}
[Reflexivity Practices]: {reflexivity_documentation}

Tasks (VS 5-Phase):

1. **Phase 1: Modal Trustworthiness Criterion Identification**
   - List criteria applicable to all qualitative research: "member checking", "triangulation", etc.
   - Estimate T-Score
   - Declare "This is baseline. Analyzing the most critical trustworthiness strategies for THIS research"

2. **Phase 2: Long-Tail Trustworthiness Strategy Sampling**
   - Direction A (T≈0.65): Tradition-specific strategies (epoché, theoretical sampling, etc.)
   - Direction B (T≈0.40): Research-specific contextual strategies
   - Direction C (T<0.25): Hidden quality practices (confirmability audit, negative case analysis)

3. **Phase 3: Low-Typicality Selection & Prioritization**
   - Select 3-5 most critical trustworthiness strategies for this research
   - Map to Lincoln & Guba criteria (credibility, transferability, dependability, confirmability)
   - State selection rationale

4. **Phase 4: Execution**
   - Criterion-by-criterion strategy assessment (credibility, transferability, etc.)
   - Top priority strategy detailed analysis with current implementation and enhancement
   - Reflexivity assessment (personal + epistemological)
   - Tradition-specific quality indicators
   - Reporting checklist compliance (COREQ, SRQR)
   - Overall trustworthiness summary
   - Immediate actions and trustworthiness statement recommendations

5. **Phase 5: Analysis Adequacy Verification**
   - Modal avoidance confirmation
   - Prioritization completion confirmation
   - Research-specific strategy selection confirmed
```

---

### For Mixed Methods Research

```
You are a research quality expert specializing in mixed methods integration.
Apply VS-Research methodology to provide integration quality analysis specific to this research.

[MM Design Type]: {design_type}
[Quantitative Component]: {quant_design}
[Qualitative Component]: {qual_tradition}
[Integration Points]: {integration_description}
[Purpose Statement]: {mm_purpose}

Tasks (VS 5-Phase):

1. **Phase 1: Modal Integration Issue Identification**
   - List integration issues applicable to all MM research: "parallel reporting", "weak integration"
   - Estimate T-Score
   - Declare "This is baseline. Analyzing the most critical integration issues for THIS research"

2. **Phase 2: Long-Tail Integration Analysis Sampling**
   - Direction A (T≈0.70): Design-type specific integration issues
   - Direction B (T≈0.40): Research-specific integration weaknesses
   - Direction C (T<0.25): Hidden quality issues (paradigm conflicts, meta-inferences)

3. **Phase 3: Low-Typicality Selection & Prioritization**
   - Identify most critical integration weakness for this study
   - Assess quantitative strand quality (bias detection)
   - Assess qualitative strand quality (trustworthiness)
   - Prioritize overall

4. **Phase 4: Execution**
   - Integration point analysis (design, methods, interpretation levels)
   - Quantitative strand bias analysis (abbreviated)
   - Qualitative strand trustworthiness analysis (abbreviated)
   - GRAMMS checklist compliance
   - Joint display assessment
   - Overall MM quality summary
   - Integration enhancement recommendations

5. **Phase 5: Analysis Adequacy Verification**
   - Modal avoidance confirmation (not just "integration is important")
   - Research-specific integration weakness identified
   - Strand-specific quality assessed
   - Integration enhancement actionable
```

---

## Flexibility and Quality Checklists (VS Enhanced)

### Quantitative: p-hacking Risk Indicators (with T-Score)

| Indicator | T-Score | Risk Level |
|-----------|---------|------------|
| No preregistration | 0.85 | Modal - specificity needed |
| p ≈ .049 | 0.40 | Specific - review needed |
| Inconsistent outlier handling | 0.50 | Specific - review needed |
| Post-hoc covariate selection | 0.55 | Specific - review needed |
| No multiple comparison correction | 0.65 | Design specific |
| Unclear subgroup analysis rationale | 0.45 | Specific - review needed |
| Switching between one-tailed/two-tailed tests | 0.35 | Hidden - often not reported |
| Undisclosed scale transformations | 0.30 | Hidden - rarely discussed |

### Qualitative: Analytical Flexibility Indicators (with T-Score)

| Indicator | T-Score | Risk Level |
|-----------|---------|------------|
| No audit trail of coding decisions | 0.70 | Design-type specific |
| Codes/themes changed without documentation | 0.45 | Specific - review needed |
| Cherry-picking quotes supporting hypothesis | 0.50 | Specific - review needed |
| Ignoring negative cases | 0.40 | Specific - review needed |
| Reflexivity journal absent | 0.65 | Common but critical |
| Post-hoc theoretical framework selection | 0.35 | Hidden - often not discussed |
| Stopping data collection when "story emerges" | 0.55 | Specific - saturation claim issue |
| Changing research question to fit findings | 0.30 | Hidden - HARKing equivalent |

### Mixed Methods: Integration Flexibility Indicators (with T-Score)

| Indicator | T-Score | Risk Level |
|-----------|---------|------------|
| Post-hoc decision to add qual/quant strand | 0.60 | Design-specific |
| Selective integration (only convergent findings) | 0.45 | Specific - common issue |
| Reframing divergent findings as "complementary" | 0.40 | Specific - review needed |
| No documentation of integration decisions | 0.55 | Specific - often missing |
| Changing integration strategy without rationale | 0.35 | Hidden - flexibility not disclosed |

---

## Related Agents

- **03-devils-advocate** (Full VS): Critical review
- **06-evidence-quality-appraiser** (Enhanced VS): Quality assessment
- **12-sensitivity-analysis-designer** (Light VS): Robustness verification

---

## Self-Critique Requirements (Full VS Mandatory)

**This self-evaluation section must be included in all outputs.**

```markdown
---

## 🔍 Self-Critique

### Strengths
Advantages of this bias analysis:
- [ ] {Design-specific bias analysis}
- [ ] {Data collection-specific bias identification}
- [ ] {Analysis-specific bias review}
- [ ] {Reporting bias assessment}

### Weaknesses
Limitations of this bias analysis:
- [ ] {False positive possibility (over-detection)}: {Supplementation approach}
- [ ] {False negative possibility (missed detection)}: {Supplementation approach}

### Alternative Perspectives
Potentially missed biases:
- **Field specificity**: "{Whether field-specific biases considered}"
- **Research stage differences**: "{Whether stage-specific bias differences considered}"

### Improvement Suggestions
Suggestions for improving bias analysis:
1. {Areas requiring additional review}
2. {Areas requiring external expert consultation}

### Confidence Assessment
| Area | Confidence | Rationale |
|------|------------|-----------|
| Detection completeness | {High/Medium/Low} | {Rationale} |
| Severity assessment accuracy | {High/Medium/Low} | {Rationale} |
| Mitigation strategy feasibility | {High/Medium/Low} | {Rationale} |

**Overall Confidence**: {Score}/100

---
```

> **Reference**: Self-Critique framework details at `../../research-coordinator/references/self-critique-framework.md`

---

## v3.0 Creativity Mechanism Integration

### Available Creativity Mechanisms

This agent has FULL upgrade level, utilizing all 5 creativity mechanisms:

| Mechanism | Application Timing | Usage Example |
|-----------|-------------------|---------------|
| **Forced Analogy** | Phase 2 | Apply bias detection patterns from other fields by analogy |
| **Iterative Loop** | Phase 2-4 | 4-round bias analysis refinement cycle |
| **Semantic Distance** | Phase 2 | Discover semantically distant hidden biases |
| **Temporal Reframing** | Phase 1-2 | Review bias patterns from past/future perspectives |
| **Community Simulation** | Phase 4 | Synthesize bias perspectives from 7 virtual researchers |

### Checkpoint Integration

```yaml
Applied Checkpoints:
  - CP-INIT-002: Select creativity level
  - CP-VS-001: Select bias analysis direction (multiple)
  - CP-VS-002: Hidden bias detection warning
  - CP-VS-003: Bias analysis satisfaction confirmation
  - CP-AG-003: Bias awareness and acceptance confirmation ⚠️ GUARDRAIL
  - CP-IL-001~004: Analysis refinement round progress
  - CP-TR-001: Time perspective selection
  - CP-CS-001: Feedback persona selection
  - CP-CS-002: Feedback incorporation confirmation
```

### Module References

```
../../research-coordinator/core/vs-engine.md
../../research-coordinator/core/t-score-dynamic.md
../../research-coordinator/creativity/forced-analogy.md
../../research-coordinator/creativity/iterative-loop.md
../../research-coordinator/creativity/semantic-distance.md
../../research-coordinator/creativity/temporal-reframing.md
../../research-coordinator/creativity/community-simulation.md
../../research-coordinator/interaction/user-checkpoints.md
```

---

## References

### Framework and System References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- **User Checkpoints**: `../../research-coordinator/interaction/user-checkpoints.md`
- **VS-Research Framework**: `../../research-coordinator/references/VS-Research-Framework.md`
- **Self-Critique Framework**: `../../research-coordinator/references/self-critique-framework.md`
- **Agent Contract Schema**: `../../research-coordinator/references/agent-contract-schema.md`

### Quantitative Research Integrity

- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-Positive Psychology: Undisclosed Flexibility in Data Collection and Analysis Allows Presenting Anything as Significant. *Psychological Science*, 22(11), 1359–1366.
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). The preregistration revolution. *Proceedings of the National Academy of Sciences*, 115(11), 2600-2606.
- Head, M. L., Holman, L., Lanfear, R., Kahn, A. T., & Jennions, M. D. (2015). The Extent and Consequences of P-Hacking in Science. *PLOS Biology*, 13(3), e1002106.
- John, L. K., Loewenstein, G., & Prelec, D. (2012). Measuring the Prevalence of Questionable Research Practices With Incentives for Truth Telling. *Psychological Science*, 23(5), 524-532.
- Wicherts, J. M., Veldkamp, C. L., Augusteijn, H. E., Bakker, M., van Aert, R. C., & van Assen, M. A. (2016). Degrees of Freedom in Planning, Running, Analyzing, and Reporting Psychological Studies: A Checklist to Avoid p-Hacking. *Frontiers in Psychology*, 7, 1832.

### Qualitative Research Trustworthiness

- Lincoln, Y. S., & Guba, E. G. (1985). *Naturalistic Inquiry*. Sage Publications.
- Guba, E. G., & Lincoln, Y. S. (1989). Fourth Generation Evaluation. Sage Publications.
- Tong, A., Sainsbury, P., & Craig, J. (2007). Consolidated criteria for reporting qualitative research (COREQ): a 32-item checklist for interviews and focus groups. *International Journal for Quality in Health Care*, 19(6), 349-357.
- O'Brien, B. C., Harris, I. B., Beckman, T. J., Reed, D. A., & Cook, D. A. (2014). Standards for Reporting Qualitative Research: A Synthesis of Recommendations. *Academic Medicine*, 89(9), 1245-1251.
- Tracy, S. J. (2010). Qualitative Quality: Eight "Big-Tent" Criteria for Excellent Qualitative Research. *Qualitative Inquiry*, 16(10), 837-851.
- Morse, J. M., Barrett, M., Mayan, M., Olson, K., & Spiers, J. (2002). Verification Strategies for Establishing Reliability and Validity in Qualitative Research. *International Journal of Qualitative Methods*, 1(2), 13-22.

### Reflexivity

- Finlay, L. (2002). "Outing" the Researcher: The Provenance, Process, and Practice of Reflexivity. *Qualitative Health Research*, 12(4), 531-545.
- Berger, R. (2015). Now I see it, now I don't: researcher's position and reflexivity in qualitative research. *Qualitative Research*, 15(2), 219-234.
- Pillow, W. (2003). Confession, catharsis, or cure? Rethinking the uses of reflexivity as methodological power in qualitative research. *International Journal of Qualitative Studies in Education*, 16(2), 175-196.

### Mixed Methods

- O'Cathain, A., Murphy, E., & Nicholl, J. (2008). The Quality of Mixed Methods Studies in Health Services Research. *Journal of Health Services Research & Policy*, 13(2), 92-98.
- Creswell, J. W., & Plano Clark, V. L. (2017). *Designing and Conducting Mixed Methods Research* (3rd ed.). Sage Publications.
- Fetters, M. D., Curry, L. A., & Creswell, J. W. (2013). Achieving Integration in Mixed Methods Designs—Principles and Practices. *Health Services Research*, 48(6 Pt 2), 2134-2156.

### Qualitative Traditions

- van Manen, M. (2016). *Researching Lived Experience: Human Science for an Action Sensitive Pedagogy* (2nd ed.). Routledge.
- Charmaz, K. (2014). *Constructing Grounded Theory* (2nd ed.). Sage Publications.
- Stake, R. E. (1995). *The Art of Case Study Research*. Sage Publications.
- Yin, R. K. (2017). *Case Study Research and Applications: Design and Methods* (6th ed.). Sage Publications.
