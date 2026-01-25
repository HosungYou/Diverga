# CLAUDE.md

# Research Coordinator v4.0

AI Research Assistant for the Complete Research Lifecycle - from question formulation to publication.

**Language**: English base with Korean support (한국어 입력 지원)

## Project Overview

Research Coordinator provides **context-persistent research support** through 21 specialized agents. Unlike other AI tools, its real value is maintaining research context across the entire project lifecycle in a single platform.

## Core Value Proposition

1. **Context Persistence**: No re-explaining your research question, methodology, or decisions
2. **Single Platform**: Claude Code as your unified research environment
3. **Research Pipeline**: Structured workflow from idea to publication
4. **Tool Discovery**: Easy access to tools/platforms you didn't know existed
5. **Human-Centered**: AI assists, humans decide

> **Core Principle**: "Human decisions remain with humans. AI handles what's beyond human scope."
> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

## Quick Start

Simply tell Research Coordinator what you want to do:

```
"I want to conduct a systematic review on AI in education"
"메타분석 연구를 시작하고 싶어"
"Help me design an experimental study"
```

The system guides you through a conversational wizard with clear choice points.

## Core Systems (v4.0)

| System | Purpose | Location |
|--------|---------|----------|
| Project State | Context persistence | `.research/project-state.yaml` |
| Pipeline Templates | PRISMA 2020 workflow | `core/pipeline-templates.md` |
| Integration Hub | Tool connections | `core/integration-hub.md` |
| Guided Wizard | AskUserQuestion UX | `core/guided-wizard.md` |
| Auto-Documentation | Document generation | `core/auto-documentation.md` |

## Agent Structure (3-Tier)

| Tier | Agents | Purpose |
|------|--------|---------|
| **Flagship** | #02, #03, #10, #21 | Full VS methodology, strategic decisions |
| **Core** | #01, #05, #06, #09, #16, #17 | Essential capabilities |
| **Support** | #04, #07-08, #11-15, #18-20 | Specialized tasks |

## Tool Integrations

### Ready to Use (No Setup)
- **Excel**: Data extraction, coding → "Create extraction spreadsheet"
- **PowerPoint**: Presentations → "Create conference slides"
- **Word**: Manuscripts → "Export methods to Word"
- **Python**: Analysis → Built-in
- **Mermaid**: Diagrams → "Create PRISMA flow diagram"

### Needs Setup
- **Semantic Scholar**: API key for literature search
- **OpenAlex**: Email for polite pool
- **Zotero**: MCP server for references
- **R Scripts**: Local R installation
- **Nanobanana**: Gemini API key for visualization

## GitHub Repository

https://github.com/HosungYou/research-coordinator

---

## OMC Integration (v3.2.0+)

Research Coordinator integrates with **oh-my-claudecode** for parallel processing and smart model routing.

### Human Checkpoints

| Level | Checkpoints | Action |
|-------|-------------|--------|
| 🔴 REQUIRED | CP_RESEARCH_DIRECTION, CP_THEORY_SELECTION, CP_METHODOLOGY_APPROVAL | User approval required |
| 🟠 RECOMMENDED | CP_ANALYSIS_PLAN, CP_QUALITY_REVIEW | Review recommended |
| 🟡 OPTIONAL | CP_VISUALIZATION_PREFERENCE, CP_RENDERING_METHOD | Defaults available |

### Model Routing

| Tier | Model | Agents |
|------|-------|--------|
| HIGH | Opus | #01, #02, #03, #09, #19 |
| MEDIUM | Sonnet | #04, #06, #10, #12, #15-18, #20-21 |
| LOW | Haiku | #05, #07, #08, #11, #13-14 |

### OMC Modes

```bash
ulw: 문헌 검색해줘     # ultrawork - maximum parallelism
eco: 통계 분석해줘     # ecomode - token efficient
ralph: 연구 설계 완료해줘  # persistence until done
```
