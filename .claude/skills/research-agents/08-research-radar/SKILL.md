---
name: research-radar
version: 4.0.0
description: |
  VS-Enhanced Research Radar - Prevents Mode Collapse with differentiated trend analysis
  Enhanced VS 3-Phase process: Avoids simple keyword tracking, delivers strategic research monitoring
  Use when: tracking new publications, monitoring research trends, staying updated
  Triggers: latest research, trends, new publications, recent papers, research developments
upgrade_level: ENHANCED
tier: Support
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
  checkpoints:
    - CP-INIT-002
    - CP-VS-001
    - CP-VS-003
    - CP-SD-001
---

# Research Radar

**Agent ID**: 08
**Category**: B - Literature & Evidence
**VS Level**: Enhanced (3-Phase)
**Tier**: Support
**Icon**: 🌐

## Overview

Monitors new publications on specific topics in real-time and analyzes research trends.
Tracks various sources including preprints, journal publications, and conference presentations.

**VS-Research methodology** is applied to go beyond simple keyword alerts and provide
strategic monitoring that captures changes and opportunities in the research ecosystem.

## VS-Research 3-Phase Process (Enhanced)

### Phase 1: Identify Modal Research Tracking Approaches

**Purpose**: Recognize limitations of simple keyword alerts

```markdown
⚠️ **Modal Warning**: These are the most predictable research tracking approaches:

| Modal Approach | T-Score | Limitations |
|----------------|---------|-------------|
| "Keyword-based alerts" | 0.90 | Miss new terminology/concepts |
| "Author tracking only" | 0.85 | Exclude emerging researchers |
| "Single DB monitoring" | 0.88 | Miss preprints/grey literature |

➡️ Basic tracking is baseline. Expanding to strategic radar.
```

### Phase 2: Strategic Research Monitoring

**Purpose**: Strategies to capture research opportunities and threats early

```markdown
**Direction A** (T ≈ 0.7): Multi-Source Integration
- Integrate keyword + author + citation alerts
- Include preprint servers
- Suitable for: General research updates

**Direction B** (T ≈ 0.4): Ecosystem Monitoring
- Track competing research teams
- Early detection of methodological innovations
- Funding trend analysis
- Suitable for: Research strategy development

**Direction C** (T < 0.3): Predictive Radar
- Early detection of emerging topics (burst analysis)
- Capture paradigm shift signals
- Identify research gap opportunities
- Suitable for: Leading research, long-term strategy
```

### Phase 4: Execute Recommendation

**Based on selected monitoring strategy**:
1. Multi-source alert setup guide
2. Trend analysis dashboard
3. Prioritized reading list
4. Research opportunity/threat report

---

## Research Monitoring Typicality Score Reference Table

```
T > 0.8 (Modal - Needs Expansion):
├── Single keyword alerts
├── Track major authors only
├── Monitor journal publications only
└── Passive alert reception

T 0.5-0.8 (Established - Needs Integration):
├── Multiple keyword combinations
├── Include preprint servers
├── Add citation alerts
└── Periodic manual searches

T 0.3-0.5 (Strategic - Recommended):
├── Competing research team trend analysis
├── Methodological innovation tracking
├── Conference presentation monitoring
└── Link to funding trends

T < 0.3 (Predictive - For Leading Research):
├── Burst analysis to detect emerging topics
├── Network analysis-based trend prediction
├── Automatic research gap identification
└── Paradigm shift early warning
```

## When to Use

- When tracking latest developments on a research topic
- When monitoring competing research teams' publications
- When tracking citations of key papers
- When exploring new research opportunities

## Core Functions

1. **Automatic Alert Setup**
   - Keyword-based alerts
   - Author-based alerts
   - Journal-based alerts
   - Citation alerts

2. **Preprint Monitoring**
   - arXiv, SSRN, OSF
   - bioRxiv, medRxiv
   - Field-specific preprint servers

3. **Trend Analysis**
   - Identify emerging research topics
   - Research methodology trends
   - Citation pattern analysis

4. **Summary Report Generation**
   - Weekly/monthly updates
   - Key paper highlights
   - Relevance scores

## Monitoring Platforms

| Platform | Type | Features | Alert Method |
|----------|------|----------|--------------|
| Google Scholar | Comprehensive | Broad coverage | Email |
| Semantic Scholar | Comprehensive | AI-based recommendations | API |
| arXiv | Preprint | CS, physics, math | RSS, API |
| SSRN | Preprint | Social sciences, business | RSS |
| OSF Preprints | Preprint | Multidisciplinary | API |
| PubMed | Medical | MEDLINE indexed | RSS, Email |

## Input Requirements

```yaml
Required:
  - Tracking keywords: "Topic-related keywords"
  - Field of interest: "Academic domain"

Optional:
  - Authors of interest: "Researchers to track"
  - Key papers: "Papers to track citations"
  - Time period: "Monitoring period"
  - Language: "Preferred language"
```

## Output Format

```markdown
## Research Trend Report

### Monitoring Period: [Start Date] ~ [End Date]
### Tracked Keywords: [Keyword List]

---

### 1. New Publications Summary

**Total Papers Found**: [N] papers
- Journal publications: [N] papers
- Preprints: [N] papers
- Conferences: [N] papers

### 2. Key Paper Highlights (Top 5)

#### 🥇 [Paper 1]
- **Title**: [Title]
- **Authors**: [Authors]
- **Source**: [Journal/Preprint]
- **Date**: [Publication Date]
- **Abstract Summary**: [3-4 sentence summary]
- **Key Findings**: [Main contributions]
- **Relevance Score**: ⭐⭐⭐⭐⭐ (5/5)
- **Implications**: [Implications for current research]

#### 🥈 [Paper 2]
...

### 3. Trend Analysis

#### Major Research Directions
1. **[Trend 1]**: [Description]
   - Related papers: [N] papers
   - Representative paper: [Paper name]

2. **[Trend 2]**: [Description]
   - Related papers: [N] papers
   - Representative paper: [Paper name]

#### Emerging Keywords
| Keyword | Frequency | Growth Rate |
|---------|-----------|-------------|
| [Keyword1] | [N] | +[X]% |
| [Keyword2] | [N] | +[X]% |

#### Methodology Trends
- [New methodology 1]: [Description]
- [New methodology 2]: [Description]

### 4. Author Activity

| Author | New Papers | Main Topics |
|--------|------------|-------------|
| [Author1] | [N] papers | [Topic] |
| [Author2] | [N] papers | [Topic] |

### 5. Citation Alerts (Key Paper Citations)

**[Key Paper Title]** Citation Status:
- New citations: [N] papers
- Notable citations:
  - [Citing paper 1]: [Citation context]
  - [Citing paper 2]: [Citation context]

### 6. Research Gaps and Opportunities

Research gaps discovered in current trends:
1. [Gap 1]: [Description]
2. [Gap 2]: [Description]

### 7. Recommended Actions

- [ ] Must-read papers: [List]
- [ ] Papers to add to citations: [List]
- [ ] Researchers to contact: [List]
- [ ] Keywords to add to next search: [List]
```

## Prompt Template

```
You are an academic literature monitoring expert.

Please track the latest research developments on the following topic:

[Tracking Keywords]: {keywords}
[Authors of Interest]: {authors}
[Time Period]: {time_period}

Tasks to perform:
1. Explore latest publications
   - Search papers published within specified period
   - Include preprints
   - Include conference presentations

2. For each paper:
   - Title, authors, source, date
   - Abstract summary (3-4 sentences)
   - Key findings/contributions
   - Relevance to current research (1-5 points)

3. Trend analysis
   - Major research directions
   - Newly emerging concepts/methods
   - Research gaps

4. Priority paper recommendations
   - Must-read papers (top 5)
   - Rationale for each paper's importance
```

## Alert Setup Guide

### Google Scholar Alerts
```
1. Go to scholar.google.com
2. Execute search
3. Click "Create alert"
4. Configure email settings
```

### Semantic Scholar
```
1. Go to semanticscholar.org
2. Search author/topic
3. "Create Alert" or "Follow"
4. Set alert frequency
```

### arXiv
```
1. Go to arxiv.org
2. Select category of interest
3. Subscribe to RSS feed or
4. Use arXiv API
```

### PubMed
```
1. Go to pubmed.ncbi.nlm.nih.gov
2. Execute search
3. Click "Create alert"
4. Set email frequency
```

## Relevance Score Criteria

| Score | Criteria |
|-------|----------|
| ⭐⭐⭐⭐⭐ | Direct relevance, immediate citation needed |
| ⭐⭐⭐⭐ | High relevance, reference methodology/theory |
| ⭐⭐⭐ | Medium relevance, reference as background |
| ⭐⭐ | Indirect relevance, potential future reference |
| ⭐ | Low relevance, monitoring only |

## Related Agents

- **05-systematic-literature-scout**: Systematic literature search
- **02-theoretical-framework-architect**: Reflect new theoretical developments
- **17-journal-matcher**: Identify publication trends

## v3.0 Creative Device Integration

### Available Creative Devices (ENHANCED)

| Device | Application Point | Usage Example |
|--------|-------------------|---------------|
| **Forced Analogy** | Phase 2 | Apply trend tracking methods from other fields by analogy |
| **Iterative Loop** | Phase 2 | 4-round divergence-convergence to refine monitoring strategy |
| **Semantic Distance** | Phase 2 | Discover emerging trends with semantically distant keyword combinations |

### Checkpoint Integration

```yaml
Applied Checkpoints:
  - CP-INIT-002: Select creativity level
  - CP-VS-001: Select monitoring strategy direction (multiple)
  - CP-VS-003: Confirm final radar setup satisfaction
  - CP-SD-001: Concept combination distance threshold
```

### Module References

```
../../research-coordinator/core/vs-engine.md
../../research-coordinator/core/t-score-dynamic.md
../../research-coordinator/creativity/forced-analogy.md
../../research-coordinator/creativity/iterative-loop.md
../../research-coordinator/creativity/semantic-distance.md
../../research-coordinator/interaction/user-checkpoints.md
```

---

## References

- **VS Engine v3.0**: `../../research-coordinator/core/vs-engine.md`
- **Dynamic T-Score**: `../../research-coordinator/core/t-score-dynamic.md`
- **Creativity Mechanisms**: `../../research-coordinator/references/creativity-mechanisms.md`
- **Project State v4.0**: `../../research-coordinator/core/project-state.md`
- **Pipeline Templates v4.0**: `../../research-coordinator/core/pipeline-templates.md`
- **Integration Hub v4.0**: `../../research-coordinator/core/integration-hub.md`
- **Guided Wizard v4.0**: `../../research-coordinator/core/guided-wizard.md`
- **Auto-Documentation v4.0**: `../../research-coordinator/core/auto-documentation.md`
- Semantic Scholar API Documentation
- arXiv API User Manual
- OpenAlex Documentation
- Google Scholar Help
