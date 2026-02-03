---
name: integration-hub
version: "4.0.0"
description: |
  Integration Hub - Connects Research Coordinator to external tools and platforms.
  Office Suite, Literature APIs, Reference Management, Statistics, and Visualization.
---

# Integration Hub: Tools & Skills Guide

## Overview

Research Coordinator connects you to various tools and platforms that support your research workflow. This guide helps you discover what's available and how to use each integration.

---

## Quick Reference: Available Integrations

| Category | Tool | Access Method | Setup Required |
|----------|------|---------------|----------------|
| **Office Suite** | Excel | Skill | None |
| **Office Suite** | PowerPoint | Skill | None |
| **Office Suite** | Word | Skill | None |
| **Literature** | Semantic Scholar | API | API Key |
| **Literature** | OpenAlex | API | Email only |
| **Literature** | arXiv | API | None |
| **Literature** | KCI/RISS | Web | None |
| **References** | Zotero | MCP | MCP Server |
| **References** | BibTeX | Built-in | None |
| **Statistics** | R Scripts | Generated | R installed |
| **Statistics** | Python | Built-in | None |
| **Visualization** | Nanobanana | API | Gemini API Key |
| **Visualization** | Mermaid | Built-in | None |
| **Open Science** | OSF | Web | Account |
| **Protocol** | PROSPERO | Web | Account |

---

## Office Suite Integration

### Excel (Data Management & Extraction)

**When to Use**:
- Data extraction verification
- Effect size calculation sheets
- Moderator coding
- Summary statistics tables

**How to Use**:
```
"Create an Excel spreadsheet for my data extraction"
"Export the extracted effect sizes to Excel"
"Generate a coding sheet with the moderator variables"
```

**What Gets Created**:
- Formatted spreadsheets with headers
- Data validation rules
- Conditional formatting for quality checks
- Formulas for automatic calculations

**Example Output**:
```
📊 Data Extraction Template.xlsx
├─ Sheet 1: Study Characteristics
│   ├─ Study ID, Authors, Year, Country
│   ├─ Sample Size, Design, Duration
│   └─ Data validation dropdowns
├─ Sheet 2: Effect Sizes
│   ├─ Outcome, Statistic Type, Value
│   ├─ Automatic Hedges' g conversion
│   └─ 95% CI calculation
└─ Sheet 3: Moderators
    ├─ Coded variables
    └─ Coding definitions
```

---

### PowerPoint (Presentations)

**When to Use**:
- Conference presentations
- Lab meetings
- Dissertation defense
- Research proposals

**How to Use**:
```
"Create a presentation summarizing my meta-analysis results"
"Generate slides for my dissertation defense"
"Make a 10-minute conference presentation"
```

**What Gets Created**:
- Title slide with research question
- Background/rationale slides
- Methods overview
- Results with figures
- Discussion points
- Conclusion

**Template Styles**:
- Academic (minimal, formal)
- Conference (visual, engaging)
- Defense (comprehensive)

---

### Word (Manuscript Drafting)

**When to Use**:
- Manuscript drafts
- IRB applications
- Protocol documents
- Supplementary materials

**How to Use**:
```
"Draft my methods section in Word"
"Create an IRB application document"
"Export the manuscript to Word format"
```

**What Gets Created**:
- Properly formatted document
- APA/MLA/Chicago style
- Heading structure (IMRAD)
- Table and figure placeholders
- Citation placeholders

**Journal Templates**:
- Generic APA 7th edition
- Specific journal formats (on request)

---

## Literature Search Integration

### Semantic Scholar API

**What It Does**:
- Search 200M+ academic papers
- Access open-access PDFs
- Get citation information
- Find related papers

**Setup**:
```
1. Go to: https://www.semanticscholar.org/product/api
2. Request API key (free for academic use)
3. Set environment variable: SEMANTIC_SCHOLAR_API_KEY
```

**Usage**:
```
"Search Semantic Scholar for AI tutoring effectiveness studies"
"Find papers citing Smith et al. 2020"
"Get open access PDFs for my included studies"
```

---

### OpenAlex API

**What It Does**:
- Access 250M+ works
- Free, no key required
- Good coverage of recent publications
- Institution and funder data

**Setup**:
```
Just provide your email for the "polite pool" (faster rate limits)
```

**Usage**:
```
"Search OpenAlex for generative AI in education"
"Get publication trends for my research topic"
```

---

### Korean Academic Databases (KCI/RISS)

**What They Do**:
- KCI: Korea Citation Index (peer-reviewed Korean journals)
- RISS: Research Information Sharing Service (theses, reports)

**Access**:
- Web-based search (no API)
- Research Coordinator provides search strategy guidance

**Usage**:
```
"Help me search KCI for 인공지능 교육 연구"
"Create a RISS search strategy for my Korean literature review"
```

---

## Reference Management

### Zotero Integration (via MCP)

**What It Does**:
- Import/export references
- Sync with Zotero library
- Auto-generate bibliographies
- PDF attachment handling

**Setup**:
```
1. Install Zotero desktop app
2. Configure Zotero MCP server
3. Connect via Claude Code MCP settings
```

**Usage**:
```
"Import these papers to my Zotero library"
"Generate a bibliography from my included studies"
"Find papers in my Zotero with 'motivation' in the title"
```

---

### BibTeX (Built-in)

**What It Does**:
- Generate BibTeX entries
- Format citations
- Export reference lists

**Usage**:
```
"Generate BibTeX for my reference list"
"Create a .bib file for my manuscript"
```

---

## Statistical Analysis

### R Script Generation

**What It Does**:
- Generates complete, runnable R scripts
- Includes package installation
- Comments explaining each step
- APA-formatted output

**Prerequisites**:
- R installed locally
- Recommended packages: metafor, tidyverse, ggplot2

**Usage**:
```
"Generate R code for my three-level meta-analysis"
"Create R script for forest plot"
"Write R code to test publication bias"
```

**Example Output**:
```r
# ═══════════════════════════════════════════════════════════
# Three-Level Random-Effects Meta-Analysis
# Generated by Research Coordinator
# ═══════════════════════════════════════════════════════════

# Install required packages (if needed)
if (!require("metafor")) install.packages("metafor")
if (!require("clubSandwich")) install.packages("clubSandwich")

library(metafor)
library(clubSandwich)

# Load data
data <- read.csv("data/meta_analysis_effects.csv")

# Three-level model
model <- rma.mv(
  yi = hedges_g,
  V = variance,
  random = ~ 1 | study_id / effect_id,
  data = data,
  method = "REML"
)

# Results
summary(model)

# Heterogeneity decomposition
# Level 2 (within-study): ...
# Level 3 (between-study): ...

# Forest plot
forest(model, header = TRUE,
       xlab = "Hedges' g",
       mlab = "RE Model")
```

---

### Python (Built-in)

**What It Does**:
- Data manipulation (pandas)
- Statistical analysis (scipy, statsmodels)
- Visualization (matplotlib, seaborn)
- Effect size calculations

**Usage**:
```
"Calculate effect sizes from my extracted data"
"Create a funnel plot using Python"
"Clean my dataset and check for outliers"
```

---

## Visualization

### Nanobanana (AI Image Generation)

**What It Does**:
- Generate publication-quality diagrams
- Conceptual framework visualizations
- Theoretical model figures
- Custom academic illustrations

**Setup**:
```
1. Get Gemini API key: https://makersuite.google.com/app/apikey
2. Set environment variable: GEMINI_API_KEY
```

**Usage**:
```
"Create a conceptual framework diagram using Nanobanana"
"Generate a visualization of my theoretical model"
"Make a publication-quality figure for my mediation model"
```

**Workflow**:
```
1. You describe your model
2. Research Coordinator creates structure (Mermaid/JSON)
3. You review and approve structure
4. Nanobanana generates final image
5. You review and request refinements
```

---

### Mermaid Diagrams (Built-in)

**What It Does**:
- Flowcharts
- Sequence diagrams
- PRISMA flow diagrams
- Conceptual models (basic)

**Usage**:
```
"Create a PRISMA flow diagram"
"Generate a flowchart of my research design"
```

---

## Open Science Platforms

### OSF (Open Science Framework)

**What It Does**:
- Pre-registration hosting
- Data/materials sharing
- Preprint hosting
- Project management

**Usage**:
```
"Help me prepare my OSF pre-registration"
"Create a data availability statement"
"Generate OSF project structure"
```

**Auto-Generated Package**:
```
osf_submission/
├─ README.md (project description)
├─ preregistration.md
├─ data/
│   ├─ raw/ (if sharing)
│   └─ processed/
├─ analysis/
│   └─ analysis_script.R
├─ materials/
│   └─ instruments/
└─ manuscript/
    └─ manuscript.docx
```

---

### PROSPERO (Systematic Review Protocol)

**What It Does**:
- Protocol registration for systematic reviews
- International prospective register

**Usage**:
```
"Help me fill out my PROSPERO registration"
"Draft my systematic review protocol"
```

---

## Integration Status Dashboard

When you ask "Show my integration status":

```
┌─────────────────────────────────────────────────────────────┐
│              Integration Status Dashboard                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ READY TO USE                                            │
│  ├─ Excel (Skill: ms-office-suite:excel)                   │
│  ├─ PowerPoint (Skill: ms-office-suite:powerpoint)         │
│  ├─ Word (Skill: ms-office-suite:word)                     │
│  ├─ BibTeX generation                                       │
│  ├─ Mermaid diagrams                                        │
│  ├─ Python analysis                                         │
│  └─ arXiv search                                            │
│                                                             │
│  ⚙️ NEEDS SETUP                                             │
│  ├─ Semantic Scholar API                                    │
│  │   └─ [How to setup] Get free API key                    │
│  ├─ Nanobanana (Gemini)                                     │
│  │   └─ [How to setup] Get Gemini API key                  │
│  ├─ Zotero MCP                                              │
│  │   └─ [How to setup] Configure MCP server                │
│  └─ R scripts                                               │
│      └─ [How to setup] Install R locally                   │
│                                                             │
│  📋 WEB-BASED (Manual Access)                               │
│  ├─ PROSPERO - https://www.crd.york.ac.uk/prospero/        │
│  ├─ OSF - https://osf.io/                                   │
│  ├─ KCI - https://www.kci.go.kr/                           │
│  └─ RISS - https://www.riss.kr/                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Skill Usage Guidance

When a task requires a specific skill, Research Coordinator will guide you:

```
┌─────────────────────────────────────────────────────────────┐
│  📊 Data Extraction Complete                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  I've extracted effect sizes from 46 studies.               │
│                                                             │
│  Recommended next step:                                     │
│  Export to Excel for verification and coding.               │
│                                                             │
│  I can create an Excel spreadsheet with:                    │
│  • Study characteristics                                    │
│  • Effect sizes with 95% CI                                 │
│  • Moderator coding columns                                 │
│  • Data validation rules                                    │
│                                                             │
│  Would you like me to create this spreadsheet?              │
│  [Yes, create Excel] [No, continue without]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Adding New Integrations

Research Coordinator can be extended with new integrations:

```yaml
# .research/custom-integrations.yaml

integrations:
  - name: "Custom Database"
    type: "api"
    base_url: "https://api.example.com"
    auth_type: "api_key"
    env_variable: "CUSTOM_DB_API_KEY"

  - name: "Lab Server"
    type: "local"
    path: "/path/to/lab/tools"
    scripts:
      - analyze.R
      - process.py
```

---

## Humanization Tools (v6.1)

### Overview

The Humanization Pipeline helps transform AI-generated academic text into natural, human-sounding prose while maintaining scholarly integrity.

### Available Tools

| Tool | Purpose | Setup |
|------|---------|-------|
| G5-AcademicStyleAuditor | AI pattern detection | Built-in |
| G6-AcademicStyleHumanizer | Pattern transformation | Built-in |
| F5-HumanizationVerifier | Quality verification | Built-in |

### Usage Commands

```
"Check AI patterns in my draft"
→ Runs G5 analysis, shows pattern report

"Humanize my abstract"
→ Full pipeline: G5 → Checkpoint → G6 → F5

"Humanize (conservative)"
→ Minimal changes, high-risk patterns only

"Humanize (balanced)"
→ Recommended for most academic writing

"Humanize (aggressive)"
→ Maximum naturalness, for informal writing

"Export with humanization"
→ Run pipeline before Word/PDF export
```

### Configuration

```yaml
# .research/humanization-config.yaml

humanization:
  enabled: true
  default_mode: "balanced"

  auto_check: true          # Auto-run G5 on exports
  show_checkpoint: true     # Show humanization options

  thresholds:
    skip_if_below: 20       # Skip if AI probability < 20%
    recommend_if_above: 40  # Recommend if > 40%

  reports:
    include_audit_trail: true
    save_original: true
```

### When to Use

| Situation | Recommendation |
|-----------|----------------|
| Journal submission | Conservative mode |
| Conference paper | Balanced mode |
| Response letter | Balanced mode |
| Blog/social media | Aggressive mode |
| AI probability < 25% | Skip (likely fine) |
| AI probability > 60% | Strongly recommend |

### Workflow Integration

The humanization pipeline integrates with:
- **G2-AcademicCommunicator**: Post-generation humanization
- **G3-PeerReviewStrategist**: Response letter humanization
- **Auto-Documentation**: Pre-export humanization
- **Word Export**: Optional humanization before export

### Ethical Considerations

Humanization helps express ideas naturally—it does not:
- Make AI use "undetectable" (detection will improve)
- Replace the need for AI disclosure
- Substitute for original research

Researchers should follow institutional and journal AI use policies.

### Pipeline Details

See: `humanization-pipeline.md` for full architecture
