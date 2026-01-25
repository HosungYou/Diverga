# Research Coordinator: Professional Repository Upgrade Roadmap

## Benchmark Analysis: oh-my-opencode

**Source**: https://github.com/code-yeongyu/oh-my-opencode
**Stats**: 23.7k Stars, 1.7k Forks, 1,477 Commits

### What Makes It Professional

| Category | oh-my-opencode | research-coordinator (Current) | Gap |
|----------|---------------|-------------------------------|-----|
| **Documentation** | 4-tier (README, CONTRIBUTING, /docs, external site) | 2-tier (README, /docs) | Medium |
| **Versioning** | Semantic + Beta cycles | Semantic only | Low |
| **CI/CD** | GitHub Actions (build, test, publish) | None | High |
| **Release Process** | Automated with categorized notes | Manual | High |
| **Multi-language** | EN, KO, JA, ZH | EN + KO | Low |
| **Contributing Guide** | Detailed with anti-patterns | Basic | Medium |
| **License** | SUL-1.0 + CLA | MIT | OK |
| **Community** | Discord + Twitter | None | Medium |
| **Installation** | One-command (plugin system) | Two-command (plugin) | OK |
| **AI-readable docs** | AGENTS.md | Partial | Low |

---

## Upgrade Roadmap

### Phase 1: Foundation (Week 1) 🔴 High Priority

#### 1.1 CONTRIBUTING.md Enhancement

**Current**: Basic or missing
**Target**: oh-my-opencode level detail

```markdown
# Contributing to Research Coordinator

## Development Setup

**Prerequisites:**
- Claude Code (latest)
- Git
- oh-my-claudecode plugin (optional)

## Code Conventions

| Convention | Rule |
|---|---|
| Language | English base, Korean comments OK |
| Agent naming | `XX-kebab-case-name` |
| VS Level | Specify Full/Enhanced/Light |

## Local Testing

1. Clone repository
2. Link to Claude Code skills:
   ```bash
   ./scripts/install.sh
   ```
3. Test with: "I want to start a systematic review"

## Pull Request Process

1. Create branch from `main`
2. Update documentation
3. Test with actual research scenario
4. Submit PR with description

## Anti-Patterns (Don't Do This)

- ❌ Don't add commands requiring coding knowledge
- ❌ Don't bypass human checkpoints
- ❌ Don't remove VS methodology
- ❌ Don't add features without documentation
```

**Action**: Create comprehensive CONTRIBUTING.md

---

#### 1.2 GitHub Actions CI/CD

**Files to Create**:

```yaml
# .github/workflows/validate.yml
name: Validate

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Validate SKILL.md files
        run: |
          python scripts/validate_agents.py

      - name: Check markdown links
        uses: gaurav-nelson/github-action-markdown-link-check@v1

      - name: Lint markdown
        uses: DavidAnson/markdownlint-cli2-action@v14
```

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          generate_release_notes: true
```

**Action**: Add GitHub Actions workflows

---

#### 1.3 Issue & PR Templates

```markdown
# .github/ISSUE_TEMPLATE/bug_report.md
---
name: Bug Report
about: Report a problem with Research Coordinator
---

## Description
[Clear description of the bug]

## Steps to Reproduce
1.
2.
3.

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Claude Code version:
- OS:
- Language: [English/Korean]

## Agent Involved
[Which agent(s) if applicable]
```

```markdown
# .github/ISSUE_TEMPLATE/feature_request.md
---
name: Feature Request
about: Suggest a new feature or improvement
---

## Problem
[What problem does this solve?]

## Proposed Solution
[Your idea]

## Research Use Case
[How would a researcher use this?]

## Alternatives Considered
[Other approaches]
```

**Action**: Create issue/PR templates

---

### Phase 2: Documentation (Week 2) 🟠 Medium Priority

#### 2.1 External Documentation Site

**Option A**: GitHub Pages (Free, Easy)
```
docs/
├── index.md          # Landing page
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── first-project.md
├── guides/
│   ├── systematic-review.md
│   ├── meta-analysis.md
│   └── survey-research.md
├── agents/
│   ├── overview.md
│   └── [agent-specific pages]
├── integrations/
│   ├── excel.md
│   ├── r-scripts.md
│   └── zotero.md
└── reference/
    ├── vs-methodology.md
    ├── checkpoints.md
    └── project-state.md
```

**Option B**: Mintlify/Docusaurus (Professional)
- Card-based navigation
- Search functionality
- Version switcher

**Recommended**: Start with GitHub Pages, migrate later

**Action**: Set up GitHub Pages with Jekyll/MkDocs

---

#### 2.2 Multi-Language READMEs

```
README.md        # English (primary)
README.ko.md     # Korean (한국어)
README.ja.md     # Japanese (日本語) - later
README.zh.md     # Chinese (中文) - later
```

**Action**: Create README.ko.md with full Korean content

---

#### 2.3 Philosophy Document

```markdown
# docs/PHILOSOPHY.md

# The Research Coordinator Philosophy

## Core Belief

> "Human decisions remain with humans. AI handles what's beyond human scope."
> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

## Why Context Persistence Matters

Research is a journey, not a task. When researchers switch between tools,
they lose the accumulated understanding of their project...

## The VS Methodology

We believe AI should expand possibilities, not narrow them...

## Human Checkpoints

Every strategic decision requires human approval because...
```

**Action**: Create PHILOSOPHY.md (like oh-my-opencode's ultrawork-manifesto.md)

---

### Phase 3: Community (Week 3-4) 🟡 Nice to Have

#### 3.1 Community Channels

| Platform | Purpose | Priority |
|----------|---------|----------|
| GitHub Discussions | Q&A, Feature ideas | High |
| Discord | Real-time support | Medium |
| Twitter/X | Announcements | Low |

**Action**: Enable GitHub Discussions first

---

#### 3.2 Showcase / Testimonials

```markdown
## Who Uses Research Coordinator?

> "Research Coordinator helped me complete my systematic review
> in half the time, with full PRISMA compliance."
> — Dr. [Name], [University]

## Research Published with Research Coordinator

- [Paper Title] - Journal, 2025
- [Paper Title] - Conference, 2025
```

**Action**: Collect user testimonials (after more usage)

---

#### 3.3 Badge Collection

```markdown
[![Version](https://img.shields.io/badge/version-4.0.0-blue)](...)
[![License](https://img.shields.io/badge/license-MIT-green)](...)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-purple)](...)
[![PRISMA 2020](https://img.shields.io/badge/PRISMA-2020-orange)](...)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-yellow)](...)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](...)
[![GitHub Stars](https://img.shields.io/github/stars/HosungYou/research-coordinator)](...)
```

**Action**: Add comprehensive badge collection

---

### Phase 4: Technical Excellence (Ongoing)

#### 4.1 Validation Scripts

```python
# scripts/validate_agents.py

def validate_skill_file(path):
    """Validate SKILL.md structure and content"""
    required_sections = [
        "name:", "description:", "version:",
        "VS Level", "Trigger Keywords", "Tier"
    ]
    # Check each section exists
    # Validate YAML frontmatter
    # Check for broken links
```

**Action**: Create validation scripts for CI

---

#### 4.2 Release Automation

**Conventional Commits**:
```
feat(agent): add new visualization capability
fix(vs-engine): correct T-Score calculation
docs(readme): update installation instructions
refactor(core): simplify checkpoint logic
```

**Automated Changelog**:
```yaml
# .github/workflows/changelog.yml
- uses: TriPSs/conventional-changelog-action@v5
  with:
    github-token: ${{ secrets.GITHUB_TOKEN }}
    output-file: "CHANGELOG.md"
```

**Action**: Adopt conventional commits + automated changelog

---

#### 4.3 AGENTS.md (AI-Readable)

```markdown
# AGENTS.md

## Project: Research Coordinator v4.0

## Architecture

Research Coordinator is a Claude Code Skills-based system providing
21 specialized agents for social science research.

## Core Systems

1. **Project State** (.research/project-state.yaml)
   - Maintains context across research lifecycle
   - Tracks decisions, methodology, integrations

2. **VS-Research Methodology**
   - Prevents mode collapse in AI recommendations
   - T-Score based typicality assessment

## Agent Registry

| ID | Name | Tier | VS Level |
|----|------|------|----------|
| 01 | Research Question Refiner | Core | Enhanced |
| 02 | Theoretical Framework Architect | Flagship | Full |
...

## File Structure

```
.claude/skills/
├── research-coordinator/     # Master coordinator
│   ├── SKILL.md             # Main entry point
│   └── core/                # v4.0 systems
└── research-agents/         # 21 specialized agents
```

## Key Principles

1. Human decisions remain with humans
2. Context persistence across lifecycle
3. VS methodology prevents mode collapse
```

**Action**: Create comprehensive AGENTS.md

---

## Implementation Priority Matrix

| Task | Impact | Effort | Priority |
|------|--------|--------|----------|
| CONTRIBUTING.md | High | Low | 🔴 P1 |
| GitHub Actions CI | High | Medium | 🔴 P1 |
| Issue/PR Templates | Medium | Low | 🔴 P1 |
| AGENTS.md | Medium | Low | 🔴 P1 |
| GitHub Pages docs | High | Medium | 🟠 P2 |
| README.ko.md | Medium | Medium | 🟠 P2 |
| PHILOSOPHY.md | Medium | Low | 🟠 P2 |
| GitHub Discussions | Medium | Low | 🟡 P3 |
| Validation scripts | Medium | Medium | 🟡 P3 |
| Changelog automation | Low | Medium | 🟡 P3 |
| External docs site | High | High | 🟢 P4 |
| Discord community | Medium | High | 🟢 P4 |

---

## Quick Wins (Do Today)

1. ✅ README.md → English v4.0
2. ✅ 21 agents → English
3. ⬜ Add GitHub issue templates
4. ⬜ Enable GitHub Discussions
5. ⬜ Create AGENTS.md
6. ⬜ Add more badges to README

---

## Success Metrics

| Metric | Current | Target (3 months) |
|--------|---------|-------------------|
| GitHub Stars | ~10 | 100+ |
| Forks | ~2 | 20+ |
| Contributors | 1 | 3+ |
| Issues (engagement) | ~5 | 30+ |
| Documentation pages | 10 | 30+ |
| Research publications using RC | 0 | 5+ |

---

## Comparison: Before vs After

### Before (v3.x)
```
- Korean-only README
- No CI/CD
- No contributing guide
- Basic documentation
- No community features
```

### After (v4.x Professional)
```
- Multi-language README (EN/KO)
- GitHub Actions CI/CD
- Comprehensive CONTRIBUTING.md
- 4-tier documentation
- GitHub Discussions enabled
- Issue/PR templates
- AGENTS.md for AI tools
- Automated releases
```

---

*Roadmap created: 2025-01-25*
*Based on: oh-my-opencode analysis*
