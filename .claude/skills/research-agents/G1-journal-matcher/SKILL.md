---
name: journal-matcher
version: 4.0.0
description: |
  VS-Enhanced Journal Matcher - Prevents Mode Collapse with differentiated submission strategy
  Light VS applied: Avoids IF-centric recommendations + multi-dimensional matching strategy
  Use when: selecting target journals, planning submissions, comparing publication options
  Triggers: journal, submission, impact factor, academic journal, publication, submit
upgrade_level: LIGHT
tier: Core
v3_integration:
  dynamic_t_score: false
  creativity_modules: []
  checkpoints:
    - CP-INIT-001
    - CP-VS-003
---

# Journal Matcher

**Agent ID**: 17
**Category**: E - Publication & Communication
**VS Level**: Light (Modal Awareness)
**Tier**: Core
**Icon**: 📝

## Overview

Identifies optimal target journals for research and develops submission strategies.
Comprehensively analyzes journal scope, impact, review timeline, OA policies, and more.

Applies **VS-Research methodology** (Light) to go beyond Impact Factor-centric recommendations,
presenting multi-dimensional matching strategies suited to research context and goals.

## VS Modal Awareness (Light)

⚠️ **Modal Journal Matching**: The following are the most predictable approaches:

| Criterion | Modal Approach (T>0.8) | Multi-dimensional Approach (T<0.5) |
|-----------|------------------------|-----------------------------------|
| Ranking | "Recommend by highest IF" | Scope fit + Readership + IF integrated |
| Selection | "Top journal → downward" | Goal-optimized (Speed/Impact/OA) |
| Strategy | "Next tier on rejection" | Parallel strategy (Preprint + Submit) |
| Cost | "Minimize APC" | ROI analysis (Visibility vs. Cost) |

**Multi-dimensional Principle**: IF is just one indicator; select optimal journal for research goals

## When to Use

- When selecting journals for paper submission
- When comparing between journals
- When developing submission strategy (1st, 2nd, 3rd choice)
- When reviewing OA publication options

## Core Functions

1. **Scope Matching**
   - Research topic and journal scope fit
   - Recent publication trend analysis
   - Special Issue information

2. **Impact Analysis**
   - Impact Factor, CiteScore
   - h-index, SNIP, SJR
   - Within-field ranking

3. **Practical Information**
   - Average review time
   - Acceptance/rejection rate
   - Publication cost (APC)

4. **OA Policy**
   - Gold/Green OA options
   - Institutional agreements
   - Preprint policy

5. **Submission Strategy**
   - Sequential submission plan
   - Cover letter points
   - Reviewer suggestions/exclusions

## Journal Tier Classification

| Tier | Characteristics | Examples (General) | Acceptance Rate |
|------|----------------|-------------------|-----------------|
| **Tier 1** | Top, multidisciplinary | Nature, Science, PNAS | <10% |
| **Tier 2** | Field top | Psychological Bulletin, RER | 10-20% |
| **Tier 3** | Field upper | JEP:LMC, C&E, BJET | 20-35% |
| **Tier 4** | Field mid-level | Field-specific journals | 35-50% |
| **Tier 5** | Emerging, regional | Newer, regional journals | >50% |

## Input Requirements

```yaml
Required:
  - research_abstract: "Research summary"
  - field: "Academic area"

Optional:
  - priorities: "IF vs. Speed vs. OA"
  - study_type: "Empirical/Theoretical/Review"
  - constraints: "Time, cost"
```

## Output Format

```markdown
## Journal Matching Report

### Research Information
- Title: [Research title]
- Field: [Academic field]
- Study Type: [Empirical/Theoretical/Review/Meta-analysis]
- Analysis Date: [Date]

---

### 1. Research Characteristics Analysis

| Item | Analysis |
|------|----------|
| Subject Area | [Specific topic] |
| Methodological Approach | [Quantitative/Qualitative/Mixed] |
| Contribution Type | Theoretical/Empirical/Methodological |
| Potential Impact | High/Medium/Low |
| Target Audience | [Target readers] |

---

### 2. Recommended Journals List

#### 🥇 1st Choice: [Journal Name]

| Item | Information |
|------|-------------|
| Publisher | [Publisher name] |
| Impact Factor (2024) | [X.XXX] |
| CiteScore | [X.X] |
| Field Ranking | Q1 in [Field] (X/XX) |
| Scope Fit | ⭐⭐⭐⭐⭐ (5/5) |
| Average Review Time | [X] weeks (Initial → Decision) |
| Estimated Acceptance Rate | ~XX% |
| OA Options | Gold (APC: $X,XXX) / Hybrid |
| Preprint Policy | Allowed/Not allowed |

**Fit Analysis**:
- ✅ Recent similar topic published: [Paper example]
- ✅ Methodology preference: [Methodology]
- ⚠️ Caution: [Considerations]

**Submission Strategy**:
- Cover letter emphasis: [Points]
- Suggested reviewers: [Field/Names]
- Exclude reviewers: [If applicable, with reason]

---

#### 🥈 2nd Choice: [Journal Name]
[Same format]

---

#### 🥉 3rd Choice: [Journal Name]
[Same format]

---

### 3. Journal Comparison Table

| Criterion | [Journal 1] | [Journal 2] | [Journal 3] |
|-----------|-------------|-------------|-------------|
| Impact Factor | X.XXX | X.XXX | X.XXX |
| Scope Fit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Review Speed | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Acceptance Rate | ~X% | ~X% | ~X% |
| OA Cost | $X,XXX | $X,XXX | Free |

---

### 4. Sequential Submission Plan

```
Submission Strategy Timeline
─────────────────────────────────────────────

1st Submission: [Journal 1] (Tier 2)
    │
    ├── Accept → 🎉 Complete
    │
    └── Reject (Expected: ~3 months later)
            │
            ▼
2nd Submission: [Journal 2] (Tier 3)
    │
    ├── Accept → 🎉 Complete
    │
    └── Reject (Expected: ~6 months later)
            │
            ▼
3rd Submission: [Journal 3] (Tier 3-4)
    │
    └── High acceptance probability
```

**Estimated Total Time**:
- Best case: 3-4 months (1st acceptance)
- Typical: 6-9 months (2nd acceptance)
- Worst case: 12+ months (3rd or beyond)

---

### 5. Cover Letter Template

```
Dear Editor,

We are pleased to submit our manuscript entitled "[Title]"
for consideration for publication in [Journal Name].

[Why this journal - 2-3 sentences]
This study aligns well with [Journal]'s scope in [Area] and
addresses [Topic] that would be of interest to your readership.

[Key contribution - 2-3 sentences]
Our research [Main contribution] by [Method]. We found that [Key finding].

[Significance - 1-2 sentences]
These findings have implications for [Implications].

We confirm that this manuscript has not been published
elsewhere and is not under consideration by another journal.

Suggested reviewers:
1. [Name], [Affiliation] - [Reason]
2. [Name], [Affiliation] - [Reason]

Thank you for your consideration.

Sincerely,
[Corresponding Author]
```

---

### 6. Additional Considerations

#### Open Access Options
| Journal | OA Type | APC | Institutional Agreement |
|---------|---------|-----|------------------------|
| [Journal 1] | Hybrid | $X,XXX | Check needed |
| [Journal 2] | Gold | $X,XXX | None |
| [Journal 3] | Green | Free | N/A |

#### Preprint Strategy
- ✅ Recommended: [Journal] allows preprints
- Recommended server: [arXiv/SSRN/OSF Preprints]
- Timing: Just before or after submission

#### Special Issue Opportunities
- [Journal]: "[Topic]" Special Issue (Deadline: [Date])
```

## Prompt Template

```
You are an academic publishing strategy expert.

Please recommend suitable journals for the following research:

[Research Abstract]: {abstract}
[Field]: {field}
[Priorities]: {priorities}
[Study Type]: {study_type}

Tasks to perform:
1. Research characteristics analysis
   - Subject area
   - Methodological approach
   - Contribution type (theoretical/empirical/methodological)
   - Potential impact

2. Journal recommendations (5-10)
   For each journal:
   - Journal name, publisher
   - Impact Factor / h-index
   - Scope fit (1-5)
   - Average review time
   - Estimated acceptance rate
   - OA options and APC
   - Recent similar paper publications

3. Journal-specific submission strategy
   - Cover letter emphasis points
   - Potential reviewer suggestions
   - Reviewers to avoid

4. Sequential submission plan
   - 1st submission: [Journal]
   - On rejection, 2nd: [Journal]
   - 3rd and beyond: [Journals]
```

## Field-Specific Major Journals (Examples)

### Educational Technology/EdTech
| Tier | Journal | IF |
|------|---------|-----|
| T2 | Computers & Education | ~12 |
| T2 | Internet & Higher Education | ~8 |
| T3 | British Journal of Educational Technology | ~6 |
| T3 | Educational Technology Research & Development | ~5 |
| T3 | Journal of Computer Assisted Learning | ~5 |

### Educational Psychology
| Tier | Journal | IF |
|------|---------|-----|
| T1 | Review of Educational Research | ~11 |
| T2 | Journal of Educational Psychology | ~5 |
| T3 | Learning and Instruction | ~5 |
| T3 | Contemporary Educational Psychology | ~5 |

### HRD/Organizational Psychology
| Tier | Journal | IF |
|------|---------|-----|
| T2 | Human Resource Development Quarterly | ~4 |
| T2 | Journal of Organizational Behavior | ~6 |
| T3 | Human Resource Development Review | ~5 |
| T3 | Human Resource Development International | ~3 |

## Related Agents

- **18-academic-communicator**: Abstract and summary writing
- **19-peer-review-strategist**: Review response
- **13-internal-consistency-checker**: Pre-submission check

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- Journal Citation Reports (Clarivate)
- Scimago Journal & Country Rank
- DOAJ (Directory of Open Access Journals)
- Sherpa Romeo (OA policies)
