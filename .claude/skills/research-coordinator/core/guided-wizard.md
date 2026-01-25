---
name: guided-wizard
version: "4.0.0"
description: |
  Guided Conversation Wizard - AskUserQuestion-based UX for researchers with limited coding experience.
  Provides explicit choice points and natural language dialogue for accessibility.
---

# Guided Conversation Wizard

## Overview

Research Coordinator uses a guided conversation approach with explicit choice points (AskUserQuestion) followed by natural language dialogue. This ensures accessibility for researchers with limited technical experience.

---

## Entry Point Flow

### Welcome Screen

When Research Coordinator is activated, present:

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│           Welcome to Research Coordinator                   │
│                                                             │
│     Your AI research assistant for the complete             │
│     research lifecycle - from question to publication       │
│                                                             │
└─────────────────────────────────────────────────────────────┘

[AskUserQuestion Tool - Single Select]

Question: "What would you like to do?"
Header: "Action"

Options:
1. "Start a new research project"
   Description: "Set up a new systematic review, experiment, or survey"

2. "Continue existing project"
   Description: "Resume work on a project in progress"

3. "Get help with a specific task"
   Description: "Literature search, statistics, writing, etc."

4. "Learn about available tools"
   Description: "See what integrations and features are available"
```

---

## Flow 1: New Research Project

### Step 1.1: Project Type Selection

```
[AskUserQuestion Tool - Single Select]

Question: "What type of research are you conducting?"
Header: "Research Type"

Options:
1. "Systematic Review & Meta-Analysis"
   Description: "PRISMA 2020 workflow with quantitative synthesis"

2. "Experimental Study"
   Description: "RCT, quasi-experiment, or intervention study"

3. "Survey Research"
   Description: "Cross-sectional or longitudinal survey"

4. "Qualitative Study"
   Description: "Interviews, focus groups, or document analysis"
```

### Step 1.2: After Selection → Natural Language

```
Great! Let's set up your {selected_type}.

Tell me about your research interest. What topic, phenomenon,
or problem are you curious about?

(You can write in English or 한국어 - I understand both)

────────────────────────────────────────────────────────
[User types freely in natural language]
────────────────────────────────────────────────────────
```

### Step 1.3: Research Question Checkpoint

After discussion, present refined options:

```
[AskUserQuestion Tool - Single Select]

Question: "Based on our discussion, which research question direction
feels right for you?"
Header: "RQ Direction"

Options:
1. "Direction A (Narrow scope)"
   Description: "How does X affect Y in specific population Z?"

2. "Direction B (Moderate scope)"
   Description: "What mechanisms mediate the relationship..."

3. "Direction C (Broad scope)"
   Description: "How do contextual factors moderate..."

4. "None of these - let me refine further"
   Description: "Continue discussing to find the right question"
```

---

## Flow 2: Specific Task Help

### Step 2.1: Task Category Selection

```
[AskUserQuestion Tool - Single Select]

Question: "What aspect of your research do you need help with?"
Header: "Task Area"

Options:
1. "Research Design"
   Description: "Questions, theories, hypotheses, methods"

2. "Literature Review"
   Description: "Searching, screening, extracting, synthesizing"

3. "Data Analysis"
   Description: "Statistical methods, code generation, interpretation"

4. "Quality & Validation"
   Description: "Checklists, bias assessment, reproducibility"

5. "Publication Preparation"
   Description: "Writing, journal selection, peer review response"

6. "Visualization"
   Description: "Conceptual frameworks, figures, diagrams"
```

### Step 2.2: Specific Task (Conditional on Selection)

**If "Research Design" selected:**

```
[AskUserQuestion Tool - Single Select]

Question: "What stage of research design are you at?"
Header: "Design Stage"

Options:
1. "I need to develop/refine my research question"
   Description: "Starting from an idea, need to make it precise"

2. "I need to select a theoretical framework"
   Description: "Have a question, need theoretical grounding"

3. "I need critical review of my design"
   Description: "Want to anticipate reviewer concerns"

4. "I need IRB/ethics guidance"
   Description: "Preparing ethics application materials"

5. "I need methodology consultation"
   Description: "Choosing research design and methods"
```

**If "Literature Review" selected:**

```
[AskUserQuestion Tool - Single Select]

Question: "What do you need help with?"
Header: "Lit Review"

Options:
1. "Develop a search strategy"
   Description: "Keywords, databases, boolean operators"

2. "Screen papers for inclusion"
   Description: "Apply eligibility criteria"

3. "Extract data from papers"
   Description: "Effect sizes, study characteristics"

4. "Assess study quality"
   Description: "Risk of bias, GRADE assessment"

5. "Synthesize findings"
   Description: "Narrative or quantitative synthesis"
```

**If "Data Analysis" selected:**

```
[AskUserQuestion Tool - Single Select]

Question: "What analysis support do you need?"
Header: "Analysis"

Options:
1. "Choose the right statistical method"
   Description: "Match analysis to research design"

2. "Generate analysis code (R/Python)"
   Description: "Get runnable code for your analysis"

3. "Interpret results"
   Description: "Understand what the numbers mean"

4. "Check assumptions"
   Description: "Verify analysis prerequisites"

5. "Run sensitivity analyses"
   Description: "Test robustness of findings"
```

**If "Publication Preparation" selected:**

```
[AskUserQuestion Tool - Single Select]

Question: "What publication help do you need?"
Header: "Publication"

Options:
1. "Find target journals"
   Description: "Match your paper to appropriate journals"

2. "Draft manuscript sections"
   Description: "Methods, results, discussion help"

3. "Respond to peer review"
   Description: "Craft responses to reviewer comments"

4. "Prepare pre-registration"
   Description: "OSF, AsPredicted, or Registered Report"

5. "Create supplementary materials"
   Description: "Organize and format supplements"
```

**If "Visualization" selected:**

```
[AskUserQuestion Tool - Single Select]

Question: "What would you like to visualize?"
Header: "Visualization"

Options:
1. "Conceptual/Theoretical Framework"
   Description: "Visual model of your theory"

2. "Statistical Results"
   Description: "Forest plot, funnel plot, path diagram"

3. "PRISMA Flow Diagram"
   Description: "Study selection flowchart"

4. "Research Process"
   Description: "Methodology or procedure diagram"
```

---

## Flow 3: Integration Setup Guidance

### Step 3.1: Integration Category

```
[AskUserQuestion Tool - Single Select]

Question: "Which tool would you like to set up?"
Header: "Tool Setup"

Options:
1. "Office Suite (Excel, PowerPoint, Word)"
   Description: "No setup needed - ready to use via Skills"

2. "Literature Databases (Semantic Scholar, OpenAlex)"
   Description: "API key configuration"

3. "Reference Manager (Zotero)"
   Description: "MCP server configuration"

4. "Visualization (Nanobanana)"
   Description: "Gemini API key setup"

5. "Statistical Software (R)"
   Description: "Local R installation check"
```

### Step 3.2: Setup Guidance (Example: Semantic Scholar)

```
┌─────────────────────────────────────────────────────────────┐
│  Setting up Semantic Scholar API                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Semantic Scholar provides access to 200M+ academic papers  │
│  with free API access for researchers.                      │
│                                                             │
│  Steps:                                                     │
│  1. Visit: https://www.semanticscholar.org/product/api     │
│  2. Click "Request API Key" (free for academic use)        │
│  3. Fill out the form with your institutional email        │
│  4. You'll receive your API key within 1-2 business days   │
│                                                             │
│  Once you have your key:                                    │
│  Set environment variable: SEMANTIC_SCHOLAR_API_KEY         │
│                                                             │
│  Or tell me: "My Semantic Scholar API key is [key]"        │
│  (I won't store it - just use for this session)            │
│                                                             │
└─────────────────────────────────────────────────────────────┘

[AskUserQuestion Tool - Single Select]

Question: "What would you like to do?"
Header: "Next Step"

Options:
1. "I already have an API key"
   Description: "Let's test the connection"

2. "I'll set this up later"
   Description: "Continue without Semantic Scholar"

3. "I need help with the setup"
   Description: "More detailed guidance"
```

---

## Natural Language Transitions

After each AskUserQuestion selection, transition to natural dialogue:

```
Selection Made: "I need to develop/refine my research question"

→ Activate Agent: #01 Research Question Refiner
→ Inject Project Context (if exists)
→ Begin Natural Conversation:

"Let's work on your research question together.

First, tell me about your research interest. What topic or
phenomenon has caught your attention? What gap or problem
do you want to address?

Feel free to share as much or as little as you'd like -
we'll refine it together."

[Natural conversation continues until next checkpoint]
```

---

## Language Handling

### Detection

```python
def detect_language(user_input: str) -> str:
    """Detect if input is Korean or English"""
    korean_chars = len(re.findall(r'[가-힣]', user_input))
    total_chars = len(re.findall(r'[a-zA-Z가-힣]', user_input))

    if korean_chars / max(total_chars, 1) > 0.3:
        return "ko"
    return "en"
```

### Bilingual Responses

When Korean is detected, respond bilingually:

```
[AskUserQuestion Options - Bilingual]

1. "Start a new research project"
   "새로운 연구 프로젝트 시작"
   Description: "Set up a new systematic review, experiment, or survey"
   "체계적 문헌고찰, 실험, 설문 연구 설정"

2. "Continue existing project"
   "기존 프로젝트 계속"
   Description: "Resume work on a project in progress"
   "진행 중인 프로젝트 작업 재개"
```

### Response Language Matching

```
User (Korean): "메타분석을 위한 통계 방법 추천해줘"

System Response (Korean with English terms):
"메타분석 통계 방법을 추천해 드리겠습니다.

현재 연구 설계를 보면, Three-level random-effects model이
적합할 것 같습니다. 이유는:

1. 동일 연구에서 다중 효과크기가 있어 dependency 처리 필요
2. 연구 간 이질성(heterogeneity)이 예상됨
3. Moderator analysis 계획이 있음

R 코드를 생성해 드릴까요?"
```

---

## Checkpoint Integration

At human checkpoint moments, use AskUserQuestion:

```
[CP_RESEARCH_DIRECTION Checkpoint]

[AskUserQuestion Tool - Single Select]

Question: "I've identified three possible research directions.
Which one aligns best with your goals?

세 가지 연구 방향을 도출했습니다. 어떤 방향이
연구 목표와 가장 잘 맞나요?"

Header: "Direction"

Options:
1. "Direction A: Narrow Focus (T=0.65) 🟢"
   Description: "Safe, well-supported approach / 안전하고 검증된 접근"

2. "Direction B: Balanced (T=0.45) 🔵"
   Description: "Some novelty, defensible / 적당한 새로움, 방어 가능"

3. "Direction C: Innovative (T=0.25) 🟡"
   Description: "High contribution, needs strong defense / 높은 기여도, 강한 방어 필요"

4. "Let me think more"
   Description: "Continue exploring options / 더 탐색하기"
```

---

## Error Recovery

When user seems confused or stuck:

```
┌─────────────────────────────────────────────────────────────┐
│  It seems like you might be looking for something else.     │
│                                                             │
│  무언가 다른 것을 찾고 계신 것 같습니다.                     │
├─────────────────────────────────────────────────────────────┤

[AskUserQuestion Tool - Single Select]

Question: "How can I help you better?"
Header: "Help"

Options:
1. "Show me all available features"
   Description: "See everything Research Coordinator can do"

2. "Start over from the beginning"
   Description: "Go back to the welcome screen"

3. "I have a specific question"
   Description: "Ask anything in natural language"

4. "I need to talk to a human"
   Description: "This isn't what I need right now"
```

---

## Output Guidance

When an action produces output (Excel, R code, etc.), guide the user:

```
┌─────────────────────────────────────────────────────────────┐
│  ✅ R Script Generated Successfully                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  I've created a complete R script for your meta-analysis.   │
│                                                             │
│  File: analysis/meta_analysis.R                             │
│                                                             │
│  To run this script:                                        │
│  1. Open R or RStudio                                       │
│  2. Set working directory to your project folder            │
│  3. Run: source("analysis/meta_analysis.R")                 │
│                                                             │
│  The script will:                                           │
│  • Install required packages automatically                  │
│  • Load your data from data/effects.csv                     │
│  • Run the three-level random-effects model                 │
│  • Generate forest and funnel plots                         │
│  • Save results to output/                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘

[AskUserQuestion Tool - Single Select]

Question: "What would you like to do next?"
Header: "Next"

Options:
1. "Explain the code step by step"
   Description: "Walk me through what each part does"

2. "Modify the analysis"
   Description: "Change model specifications or outputs"

3. "Continue to next stage"
   Description: "Move on to sensitivity analysis"

4. "Export to different format"
   Description: "Convert to Python or add more comments"
```
