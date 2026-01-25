# Quick Start Guide

Get started with Research Coordinator in under 5 minutes!

---

## Installation (2 minutes)

### Option A: Clone and Install (Recommended)

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### Verify Installation

```bash
# Using CLI tool
./scripts/rc status

# Or in Claude Code
/research-coordinator
```

---

## Your First Agent Call (1 minute)

Open Claude Code and try one of these:

### Example 1: Research Question Refinement

```
/research-question-refiner

"AI 학습 시스템이 학생들에게 도움이 될 것 같은데, 연구 질문을 어떻게 만들어야 할까요?"
```

### Example 2: Statistical Analysis

```
/statistical-analysis-guide

"300명의 대학생 데이터로 AI 튜터 사용과 학업 성취도 관계를 분석하려고 해요.
어떤 통계 방법을 쓰면 좋을까요?"
```

### Example 3: Literature Review

```
/systematic-literature-scout

"AI 기반 적응형 학습에 대한 체계적 문헌고찰을 하려고 합니다.
검색 전략을 도와주세요."
```

---

## How It Works (2 minutes)

### VS-Research Methodology

Research Coordinator uses **Verbalized Sampling (VS)** to prevent "Mode Collapse" - the problem where AI always gives the same obvious answers.

```
❌ Without VS:
   "이론 추천해줘" → "TAM 쓰세요" (항상 같은 답)

✅ With VS:
   "이론 추천해줘"
   → Phase 1: "TAM, UTAUT는 가장 뻔한 선택입니다 (T=0.9)"
   → Phase 2: "대안을 탐색합니다..."
   → Phase 3: "맥락에 맞는 차별화된 이론: SDT × TAM 통합 (T=0.4)"
```

### T-Score System

Every recommendation comes with a **Typicality Score (T-Score)**:

| T-Score | Meaning | Recommendation |
|---------|---------|----------------|
| > 0.8 | Most common choice | ⚠️ Avoid |
| 0.5-0.8 | Established alternative | ✅ Safe differentiation |
| 0.3-0.5 | Emerging approach | ✅ Innovative, justified |
| < 0.3 | Creative | ⚠️ Needs strong justification |

### Agent Categories

| Category | Agents | Purpose |
|----------|--------|---------|
| A | 01-04 | Research Design (question, theory, ethics) |
| B | 05-08 | Literature (review, quality, effect sizes) |
| C | 09-12 | Methods (design, statistics, code) |
| D | 13-16 | Quality (consistency, checklists, bias) |
| E | 17-21 | Publication (journal, review, visualization) |

---

## Common Use Cases

### Use Case 1: Planning a New Study

```
1. /research-question-refiner
   → Define your research question

2. /theoretical-framework-architect
   → Build theoretical foundation

3. /research-design-consultant
   → Choose appropriate methodology

4. /research-ethics-advisor
   → Prepare IRB documentation
```

### Use Case 2: Literature Review

```
1. /systematic-literature-scout
   → Develop search strategy

2. /evidence-quality-appraiser
   → Assess study quality

3. /effect-size-extractor
   → Extract and convert effect sizes

4. /bias-detector
   → Check for publication bias
```

### Use Case 3: Data Analysis

```
1. /statistical-analysis-guide
   → Choose appropriate methods

2. /analysis-code-generator
   → Generate R/Python/SPSS code

3. /sensitivity-analysis-designer
   → Plan robustness checks
```

### Use Case 4: Publication

```
1. /journal-matcher
   → Find suitable journals

2. /checklist-manager
   → Complete PRISMA/CONSORT checklists

3. /peer-review-strategist
   → Prepare for reviewer comments

4. /conceptual-framework-visualizer
   → Create publication-ready figures
```

---

## Tips for Best Results

### 1. Provide Context

```
❌ "이론 추천해줘"

✅ "교육공학 분야에서 AI 기반 적응형 학습 시스템의
   학습 효과를 연구하려고 합니다.
   박사 학위 논문용으로 차별화된 이론을 추천해주세요."
```

### 2. Specify Your Goals

- First publication → Conservative approach (T > 0.5)
- Top-tier journal → Innovative approach (T < 0.5)
- Replication study → Standard approach (T > 0.6)

### 3. Use Agent Combinations

Agents work best together:

```
/research-question-refiner → /theoretical-framework-architect → /devils-advocate
```

### 4. Leverage User Checkpoints

When agents ask for confirmation (CP-VS-001, etc.), take time to review:

```
🔵 CP-VS-001: 연구 방향 A, B, C 중 선택해주세요
   → 각 방향의 T-Score와 장단점을 비교한 후 선택
```

---

## Getting Help

### CLI Tool

```bash
./scripts/rc help          # Show all commands
./scripts/rc list          # List all agents
./scripts/rc info 02       # Agent details
./scripts/rc doctor        # Diagnose issues
```

### Documentation

- [Full Documentation](./README.md)
- [Agent Reference](./AGENT-REFERENCE.md)
- [Usage Examples](./USAGE-EXAMPLES.md)
- [Setup Guide](./SETUP.md)

### Issues

- [GitHub Issues](https://github.com/HosungYou/research-coordinator/issues)

---

## Next Steps

1. **Explore agents**: `./scripts/rc list`
2. **Read documentation**: `docs/AGENT-REFERENCE.md`
3. **Try examples**: `docs/USAGE-EXAMPLES.md`
4. **Join the community**: Star the repo on GitHub!

---

**Happy Researching!** 🧬
