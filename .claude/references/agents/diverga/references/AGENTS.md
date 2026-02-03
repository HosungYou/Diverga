# Diverga Agent Reference

**Version**: 6.6.1
**Total Agents**: 40

## Quick Reference

| Category | Count | Agents |
|----------|-------|--------|
| A - Research Foundation | 6 | A1, A2, A3, A4, A5, A6 |
| B - Literature & Evidence | 5 | B1, B2, B3, B4, B5 |
| C - Study Design & Meta-Analysis | 7 | C1, C2, C3, C4, C5, C6, C7 |
| D - Data Collection | 4 | D1, D2, D3, D4 |
| E - Analysis | 5 | E1, E2, E3, E4, E5 |
| F - Quality & Validation | 5 | F1, F2, F3, F4, F5 |
| G - Publication | 6 | G1, G2, G3, G4, G5, G6 |
| H - Specialized | 2 | H1, H2 |

**Total: 6 + 5 + 7 + 4 + 5 + 5 + 6 + 2 = 40 agents**

---

## Model Tier Reference

| Tier | Model | Count |
|------|-------|-------|
| HIGH | o1 | 14 |
| MEDIUM | gpt-4 | 19 |
| LOW | gpt-3.5-turbo | 7 |

---

## Detailed Agent Specifications

### Category A: Research Foundation

#### A1 - Research Question Refiner
- **Model**: gpt-4
- **Purpose**: PICO/SPIDER frameworks, scope optimization
- **Triggers**: "research question", "PICO", "SPIDER", "RQ"
- **Output**: Refined research question with scope boundaries

#### A2 - Theoretical Framework Architect
- **Model**: o1
- **Purpose**: Theory selection, conceptual models, hypothesis derivation
- **Triggers**: "theoretical framework", "theory", "conceptual model"
- **Output**: Framework diagram, theoretical propositions

#### A3 - Devil's Advocate
- **Model**: gpt-4
- **Purpose**: Weakness identification, reviewer simulation, counterarguments
- **Triggers**: "criticism", "devil's advocate", "reviewer", "weakness"
- **Output**: Critical review with anticipated objections

#### A4 - Research Ethics Advisor
- **Model**: gpt-4
- **Purpose**: IRB protocols, consent forms, ethical considerations
- **Triggers**: "ethics", "IRB", "consent", "privacy"
- **Output**: Ethics checklist, consent templates

#### A5 - Paradigm & Worldview Advisor
- **Model**: o1
- **Purpose**: Epistemology, ontology, methodology alignment
- **Triggers**: "paradigm", "worldview", "epistemology", "ontology"
- **Output**: Paradigm justification, philosophical foundations

#### A6 - Conceptual Framework Visualizer
- **Model**: o1
- **Purpose**: Framework diagrams, visual models, variable relationships
- **Triggers**: "conceptual framework", "framework diagram", "visual model"
- **Output**: Mermaid/ASCII diagrams, visual representations

---

### Category B: Literature & Evidence

#### B1 - Literature Review Strategist
- **Model**: gpt-4
- **Purpose**: PRISMA-compliant search, scoping review, database selection
- **Triggers**: "literature review", "PRISMA", "systematic search"
- **Output**: Search strategy, database recommendations

#### B2 - Evidence Quality Appraiser
- **Model**: gpt-4
- **Purpose**: Risk of Bias assessment, CASP, JBI, GRADE
- **Triggers**: "quality appraisal", "RoB", "GRADE", "bias assessment"
- **Output**: Quality assessment tables, bias ratings

#### B3 - Effect Size Extractor
- **Model**: gpt-3.5-turbo
- **Purpose**: Calculate and convert effect sizes (d, g, r, OR)
- **Triggers**: "effect size", "Cohen's d", "Hedges' g", "odds ratio"
- **Output**: Effect size calculations with confidence intervals

#### B4 - Research Radar
- **Model**: gpt-3.5-turbo
- **Purpose**: Track recent publications, emerging trends
- **Triggers**: "recent research", "trends", "new publications"
- **Output**: Recent paper summaries, trend analysis

#### B5 - Parallel Document Processor
- **Model**: gpt-4
- **Purpose**: Batch PDF processing, parallel extraction
- **Triggers**: "batch PDF", "multiple PDFs", "parallel processing"
- **Output**: Extracted data tables, processed documents

---

### Category C: Study Design & Meta-Analysis

#### C1 - Quantitative Design Consultant
- **Model**: o1
- **Purpose**: Experimental, quasi-experimental, survey designs
- **Triggers**: "experimental design", "RCT", "quasi-experimental", "survey design"
- **Output**: Design specifications, validity considerations

#### C2 - Qualitative Design Consultant
- **Model**: o1
- **Purpose**: Phenomenology, grounded theory, case study, narrative inquiry
- **Triggers**: "phenomenology", "grounded theory", "case study", "qualitative"
- **Output**: Design rationale, sampling strategy, rigor criteria

#### C3 - Mixed Methods Design Consultant
- **Model**: o1
- **Purpose**: Convergent, sequential, embedded, transformative designs
- **Triggers**: "mixed methods", "convergent", "sequential", "embedded"
- **Output**: Design diagram, integration strategy, Morse notation

#### C4 - Experimental Materials Developer
- **Model**: gpt-4
- **Purpose**: Stimuli, instruments, protocols, manipulation checks
- **Triggers**: "experimental materials", "stimuli", "manipulation check"
- **Output**: Material specifications, pilot testing plans

#### C5 - Meta-Analysis Master
- **Model**: o1
- **Purpose**: Multi-gate validation, heterogeneity analysis, publication bias
- **Triggers**: "meta-analysis", "MASEM", "pooled effect", "heterogeneity"
- **Output**: Analysis plan, forest plots, funnel plots

#### C6 - Data Integrity Guard
- **Model**: gpt-4
- **Purpose**: Data completeness, Hedges' g calculation, SD recovery
- **Triggers**: "data extraction", "data integrity", "SD recovery"
- **Output**: Data validation reports, imputation recommendations

#### C7 - Error Prevention Engine
- **Model**: gpt-4
- **Purpose**: Pattern detection, anomaly alerts, error prevention
- **Triggers**: "error check", "validation", "anomaly detection"
- **Output**: Error reports, correction suggestions

---

### Category D: Data Collection

#### D1 - Sampling Strategy Advisor
- **Model**: gpt-4
- **Purpose**: Probability sampling, purposeful sampling, sample size
- **Triggers**: "sampling", "sample size", "G*Power", "purposeful"
- **Output**: Sampling plan, power analysis

#### D2 - Interview & Focus Group Specialist
- **Model**: gpt-4
- **Purpose**: Protocol development, probing strategies, moderation guides
- **Triggers**: "interview", "focus group", "interview protocol"
- **Output**: Interview guides, focus group protocols

#### D3 - Observation Protocol Designer
- **Model**: gpt-3.5-turbo
- **Purpose**: Structured observation guides, coding schemes
- **Triggers**: "observation", "observation protocol", "field notes"
- **Output**: Observation checklists, coding guides

#### D4 - Measurement Instrument Developer
- **Model**: o1
- **Purpose**: Scale development, validity evidence, reliability testing
- **Triggers**: "instrument", "scale development", "validity"
- **Output**: Item bank, validation plan

---

### Category E: Analysis

#### E1 - Quantitative Analysis Guide
- **Model**: o1
- **Purpose**: Statistical method selection, SEM, multilevel modeling
- **Triggers**: "statistical analysis", "regression", "SEM", "ANOVA"
- **Output**: Analysis plan, assumption checks, interpretation guide

#### E2 - Qualitative Coding Specialist
- **Model**: gpt-4
- **Purpose**: Thematic analysis, grounded theory coding, codebook
- **Triggers**: "thematic analysis", "coding", "codebook", "themes"
- **Output**: Coding framework, theme hierarchy

#### E3 - Mixed Methods Integration
- **Model**: o1
- **Purpose**: Joint displays, data transformation, meta-inference
- **Triggers**: "integration", "joint display", "meta-inference"
- **Output**: Integration matrix, joint display templates

#### E4 - Analysis Code Generator
- **Model**: gpt-3.5-turbo
- **Purpose**: R, Python, SPSS, Stata, Mplus syntax
- **Triggers**: "R code", "Python code", "SPSS syntax", "Mplus"
- **Output**: Executable code with comments

#### E5 - Sensitivity Analysis Designer
- **Model**: gpt-4
- **Purpose**: Robustness checks, alternative specifications
- **Triggers**: "sensitivity analysis", "robustness check"
- **Output**: Sensitivity analysis plan, specification table

---

### Category F: Quality & Validation

#### F1 - Internal Consistency Checker
- **Model**: gpt-3.5-turbo
- **Purpose**: Logic flow verification, terminology consistency
- **Triggers**: "consistency check", "internal consistency"
- **Output**: Consistency report, alignment matrix

#### F2 - Checklist Manager
- **Model**: gpt-3.5-turbo
- **Purpose**: CONSORT, STROBE, PRISMA, COREQ compliance
- **Triggers**: "checklist", "CONSORT", "STROBE", "COREQ"
- **Output**: Compliance checklist, gap analysis

#### F3 - Reproducibility Auditor
- **Model**: gpt-4
- **Purpose**: OSF setup, open science practices, data sharing
- **Triggers**: "reproducibility", "OSF", "open science", "replication"
- **Output**: Reproducibility checklist, OSF project template

#### F4 - Bias & Trustworthiness Detector
- **Model**: gpt-4
- **Purpose**: Bias detection, trustworthiness criteria (qual), QRP screening
- **Triggers**: "bias", "trustworthiness", "credibility"
- **Output**: Bias assessment, trustworthiness matrix

#### F5 - Humanization Verifier
- **Model**: gpt-4
- **Purpose**: AI text transformation integrity, citation preservation
- **Triggers**: "humanization verify", "AI text check"
- **Output**: Verification report, integrity confirmation

---

### Category G: Publication

#### G1 - Journal Matcher
- **Model**: gpt-4
- **Purpose**: Journal recommendation, impact analysis, scope matching
- **Triggers**: "journal match", "where to publish", "target journal"
- **Output**: Journal shortlist with rationale

#### G2 - Academic Communicator
- **Model**: gpt-4
- **Purpose**: Plain language summaries, abstract writing, conference prep
- **Triggers**: "abstract", "plain language", "summary"
- **Output**: Abstract drafts, lay summaries

#### G3 - Peer Review Strategist
- **Model**: o1
- **Purpose**: Reviewer comment analysis, response letters, revision strategy
- **Triggers**: "peer review", "reviewer response", "revision"
- **Output**: Response letter template, revision plan

#### G4 - Pre-registration Composer
- **Model**: gpt-4
- **Purpose**: OSF pre-registration, AsPredicted, registered reports
- **Triggers**: "preregistration", "OSF", "registered report"
- **Output**: Pre-registration template, hypothesis register

#### G5 - Academic Style Auditor
- **Model**: gpt-4
- **Purpose**: AI pattern detection (24 categories), probability scoring
- **Triggers**: "AI pattern", "style audit", "AI writing check"
- **Output**: Pattern report with risk classification

#### G6 - Academic Style Humanizer
- **Model**: gpt-4
- **Purpose**: Transform AI patterns to natural prose, citation preservation
- **Triggers**: "humanize", "humanization", "natural writing"
- **Output**: Humanized text with change summary

---

### Category H: Specialized

#### H1 - Ethnographic Research Advisor
- **Model**: o1
- **Purpose**: Fieldwork planning, cultural immersion, thick description
- **Triggers**: "ethnography", "fieldwork", "participant observation"
- **Output**: Fieldwork protocol, reflexivity journal template

#### H2 - Action Research Facilitator
- **Model**: o1
- **Purpose**: PAR, CBPR, action research cycles, stakeholder collaboration
- **Triggers**: "action research", "participatory", "CBPR"
- **Output**: Action cycle plan, stakeholder engagement strategy
