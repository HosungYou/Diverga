# Paradigm Detector Module

Automatically detects research paradigm from user context and activates appropriate agent packs.

## Detection Rules

### Quantitative Signals

Keywords and patterns that indicate quantitative research:

**Korean Keywords:**
- "가설", "효과크기", "통계적 유의성", "표본 크기", "실험", "변수", "측정"
- "독립변수", "종속변수", "매개변수", "조절변수", "통제변수"
- "신뢰도", "타당도", "정규성", "동분산성"
- "회귀분석", "분산분석", "구조방정식", "요인분석"

**English Keywords:**
- "hypothesis", "H1", "H2", "H3", "effect size", "statistical significance"
- "p < 0.05", "p-value", "sample size", "power analysis", "G*Power"
- "experiment", "variable", "measurement", "scale", "instrument"
- "ANOVA", "regression", "SEM", "factor analysis", "t-test", "chi-square"
- "reliability", "validity", "Cronbach's alpha", "normality", "homoscedasticity"

### Qualitative Signals

Keywords and patterns that indicate qualitative research:

**Korean Keywords:**
- "체험", "의미", "포화", "주제", "내러티브", "해석", "맥락", "참여자"
- "심층면담", "포커스그룹", "관찰", "현상학", "근거이론", "문화기술지"
- "코딩", "범주화", "삼각검증", "신뢰성", "전이가능성"
- "반성적 저널", "두터운 기술", "구성원 확인"

**English Keywords:**
- "lived experience", "meaning", "saturation", "theme", "narrative", "interpretation"
- "context", "participant voice", "thick description", "coding", "categorization"
- "phenomenology", "grounded theory", "ethnography", "case study"
- "in-depth interview", "focus group", "observation", "field notes"
- "trustworthiness", "credibility", "transferability", "triangulation"
- "reflexive journal", "member checking", "peer debriefing"

### Mixed Methods Signals

Keywords and patterns that indicate mixed methods research:

**Korean Keywords:**
- "혼합방법", "통합", "순차적", "동시적", "양적-질적", "통합 설계"
- "질적 자료와 양적 자료의 통합", "메타추론", "합동 디스플레이"

**English Keywords:**
- "mixed methods", "integration", "sequential", "concurrent", "convergent"
- "qual-quant", "QUAN+qual", "QUAL+quan", "joint display", "meta-inference"
- "explanatory sequential", "exploratory sequential", "embedded design"
- "triangulation design", "quantitizing", "qualitizing"

## Paradigm Detection Algorithm

The detection algorithm uses weighted keyword matching and context analysis:

```python
def detect_paradigm(user_message: str) -> dict:
    """
    Detects research paradigm from user message.

    Returns:
        {
            "paradigm": str,  # "quantitative" | "qualitative" | "mixed" | "undetermined"
            "confidence": float,  # 0.0 to 1.0
            "signals_found": list,  # List of matched keywords
            "suggested_agents": list  # Agent codes to activate
        }
    """
    # Count matches for each paradigm
    quant_score = count_matches(user_message, QUANTITATIVE_SIGNALS)
    qual_score = count_matches(user_message, QUALITATIVE_SIGNALS)
    mixed_score = count_matches(user_message, MIXED_SIGNALS)

    # Calculate total signals
    total_signals = quant_score + qual_score + mixed_score

    # Determine paradigm
    if mixed_score > 0 or (quant_score > 0 and qual_score > 0):
        paradigm = "mixed"
        confidence = mixed_score / total_signals if total_signals > 0 else 0.5
    elif qual_score > quant_score:
        paradigm = "qualitative"
        confidence = qual_score / total_signals if total_signals > 0 else 0.5
    elif quant_score > qual_score:
        paradigm = "quantitative"
        confidence = quant_score / total_signals if total_signals > 0 else 0.5
    else:
        paradigm = "undetermined"
        confidence = 0.0

    return {
        "paradigm": paradigm,
        "confidence": confidence,
        "signals_found": extract_matched_signals(user_message),
        "suggested_agents": get_agent_pack(paradigm)
    }
```

## Agent Pack Activation

### Quantitative Pack

When quantitative paradigm is detected, activate:

**Primary Agents (Always activate):**
- `C1-QuantitativeDesignConsultant` - Research design guidance
- `E1-QuantitativeAnalysisGuide` - Statistical analysis support
- `E4-AnalysisCodeGenerator` - R/Python/SPSS code generation

**Secondary Agents (Context-dependent):**
- `B3-EffectSizeExtractor` - If meta-analysis mentioned
- `D4-MeasurementInstrumentDeveloper` - If scale development needed
- `C1-SampleCalculator` - If sample size mentioned
- `C2-StatisticalAdvisor` - If analysis method unclear

**Support Agents:**
- `F2-ChecklistManager` - CONSORT, STROBE reporting guidelines
- `F4-BiasTrustworthinessDetector` - Validity and reliability checks

### Qualitative Pack

When qualitative paradigm is detected, activate:

**Primary Agents (Always activate):**
- `C2-QualitativeDesignConsultant` - Qualitative design guidance
- `E2-QualitativeCodingSpecialist` - Coding and thematic analysis
- `D2-InterviewFocusGroupSpecialist` - Data collection protocols

**Secondary Agents (Context-dependent):**
- `A5-ParadigmWorldviewAdvisor` - If paradigm/worldview discussion needed
- `H1-EthnographicResearchAdvisor` - If ethnography mentioned
- `H2-NarrativeAnalysisSpecialist` - If narrative inquiry mentioned
- `H3-GroundedTheoryAdvisor` - If grounded theory mentioned

**Support Agents:**
- `F4-BiasTrustworthinessDetector` - Trustworthiness criteria (credibility, transferability)
- `F2-ChecklistManager` - COREQ, SRQR reporting guidelines

### Mixed Methods Pack

When mixed methods paradigm is detected, activate:

**Primary Agents (Always activate):**
- `C3-MixedMethodsDesignConsultant` - Mixed methods design (sequential, concurrent, embedded)
- `E3-MixedMethodsIntegrationSpecialist` - Integration strategies, joint displays

**Secondary Agents (Include ALL from both packs):**
- All Quantitative Pack agents
- All Qualitative Pack agents

**Support Agents:**
- `F2-ChecklistManager` - GRAMMS reporting guidelines
- Joint display generation tools
- Meta-inference guidance protocols

## Auto-Activation Rules

```yaml
paradigm_auto_activation:

  quantitative:
    activate:
      primary: ["C1", "E1", "E4"]
      secondary: ["B3", "D4", "C1-SampleCalculator", "C2-StatisticalAdvisor"]
      support: ["F2", "F4"]

    model_routing:
      C1: "sonnet"      # Standard design consultation
      E1: "sonnet"      # Statistical analysis guidance
      E4: "sonnet"      # Code generation
      B3: "sonnet"      # Effect size extraction
      D4: "sonnet"      # Instrument development

    completion_criteria:
      - "Hypothesis formulated and testable"
      - "Variables defined with operational definitions"
      - "Sample size justified with power analysis"
      - "Statistical analysis plan documented"
      - "Analysis code generated and tested"
      - "Results interpreted with effect sizes"
      - "Visualizations generated (tables, figures)"

  qualitative:
    activate:
      primary: ["C2", "E2", "D2"]
      secondary: ["A5", "H1", "H2", "H3"]
      support: ["F4", "F2"]

    model_routing:
      C2: "opus"        # Complex interpretive design work
      E2: "sonnet"      # Coding and analysis
      D2: "sonnet"      # Interview/focus group protocols
      A5: "opus"        # Paradigm/worldview (philosophical)
      H1: "sonnet"      # Ethnography
      H2: "sonnet"      # Narrative analysis
      H3: "sonnet"      # Grounded theory

    completion_criteria:
      - "Research questions aligned with qualitative approach"
      - "Participant selection strategy justified"
      - "Data collection protocol developed"
      - "Coding framework established"
      - "Saturation reached and documented"
      - "Themes refined and verified"
      - "Trustworthiness criteria met (credibility, transferability, dependability, confirmability)"
      - "Member checking or peer debriefing completed"

  mixed:
    activate:
      primary: ["C3", "E3"]
      quantitative_pack: true   # Include all quantitative agents
      qualitative_pack: true    # Include all qualitative agents
      support: ["F2"]

    model_routing:
      C3: "opus"        # Complex mixed methods design
      E3: "opus"        # Integration is sophisticated work

    completion_criteria:
      # All quantitative criteria
      - "Quantitative strand completed"
      # All qualitative criteria
      - "Qualitative strand completed"
      # Integration-specific
      - "Integration strategy documented (when, how, why)"
      - "Joint display created showing integration"
      - "Meta-inference generated from integrated findings"
      - "Methodological coherence verified"

  undetermined:
    action: "ask_user"
    question:
      korean: "어떤 연구 접근법을 사용하시나요?"
      english: "Which research approach are you using?"

    options:
      - label_ko: "양적 연구 (Quantitative)"
        label_en: "Quantitative Research"
        value: "quantitative"
        description: "Hypothesis testing, statistical analysis, numerical data"

      - label_ko: "질적 연구 (Qualitative)"
        label_en: "Qualitative Research"
        value: "qualitative"
        description: "Interviews, themes, lived experiences, meaning-making"

      - label_ko: "혼합방법 연구 (Mixed Methods)"
        label_en: "Mixed Methods Research"
        value: "mixed"
        description: "Combining quantitative and qualitative approaches"

      - label_ko: "아직 결정하지 않았어요 (Not decided yet)"
        label_en: "Not decided yet"
        value: "undecided"
        description: "Need help choosing the best approach"
```

## Integration with Sisyphus Coordinator

When paradigm is detected, the Sisyphus coordinator:

### 1. Log Detected Paradigm

```json
{
  "project_id": "proj_2025_01_25_001",
  "detected_paradigm": {
    "paradigm": "qualitative",
    "confidence": 0.85,
    "timestamp": "2025-01-25T10:30:00Z",
    "signals_found": [
      "심층면담",
      "포화",
      "현상학적",
      "lived experience"
    ]
  }
}
```

### 2. Activate Agent Pack

```yaml
activated_agents:
  - agent: "C2-QualitativeDesignConsultant"
    model: "opus"
    reason: "Primary qualitative design agent"
    priority: 1

  - agent: "E2-QualitativeCodingSpecialist"
    model: "sonnet"
    reason: "Coding and thematic analysis"
    priority: 1

  - agent: "D2-InterviewFocusGroupSpecialist"
    model: "sonnet"
    reason: "'심층면담' keyword detected"
    priority: 2
```

### 3. Set Paradigm-Specific Completion Criteria

The coordinator uses paradigm-specific checklists to determine when work is complete:

```yaml
completion_criteria:
  paradigm: "qualitative"

  required_artifacts:
    - "Research questions document"
    - "Interview protocol or focus group guide"
    - "Coding framework (initial and refined)"
    - "Themes with supporting quotes"
    - "Trustworthiness audit trail"

  validation_checks:
    - name: "Saturation documented"
      agent: "E2-QualitativeCodingSpecialist"
      checkpoint: "CP_CODING_SATURATION"

    - name: "Member checking completed"
      agent: "F4-BiasTrustworthinessDetector"
      checkpoint: "CP_MEMBER_CHECKING"

    - name: "Reflexive journal maintained"
      agent: "C2-QualitativeDesignConsultant"
      checkpoint: "CP_REFLEXIVITY"

  human_approval_required:
    - "CP_PARADIGM_CONFIRMATION"
    - "CP_INTERVIEW_PROTOCOL"
    - "CP_CODING_FRAMEWORK"
```

## Human Checkpoints

Paradigm-specific decision points where human approval is required:

### All Paradigms

| Checkpoint | Decision | Timing |
|------------|----------|--------|
| `CP_PARADIGM_CONFIRMATION` | Confirm detected paradigm is correct | After initial detection |
| `CP_RESEARCH_QUESTIONS` | Approve research questions | Before design phase |
| `CP_FINAL_REVIEW` | Approve final outputs | Before project completion |

### Quantitative Specific

| Checkpoint | Decision | Timing |
|------------|----------|--------|
| `CP_HYPOTHESIS_APPROVAL` | Approve hypotheses and variables | After A2-HypothesisArchitect |
| `CP_SAMPLE_SIZE` | Approve sample size calculation | After C1-SampleCalculator |
| `CP_ANALYSIS_PLAN` | Approve statistical analysis plan | Before data collection |
| `CP_RESULTS_INTERPRETATION` | Approve interpretation of findings | After E1-QuantitativeAnalysisGuide |

### Qualitative Specific

| Checkpoint | Decision | Timing |
|------------|----------|--------|
| `CP_CODING_FRAMEWORK` | Approve initial coding structure | After first round of coding |
| `CP_INTERVIEW_PROTOCOL` | Approve interview guide or focus group protocol | Before data collection |
| `CP_SATURATION` | Confirm saturation has been reached | During data collection/analysis |
| `CP_THEMES` | Approve final theme structure | After thematic analysis |
| `CP_TRUSTWORTHINESS` | Confirm trustworthiness criteria met | Before final report |

### Mixed Methods Specific

| Checkpoint | Decision | Timing |
|------------|----------|--------|
| `CP_INTEGRATION_STRATEGY` | Approve integration approach (sequential, concurrent, etc.) | During design phase |
| `CP_PRIORITY` | Confirm QUAN+qual or QUAL+quan priority | During design phase |
| `CP_JOINT_DISPLAY` | Approve joint display format and content | After both strands complete |
| `CP_META_INFERENCE` | Approve meta-inferences from integration | Final integration phase |

## Example Usage Scenarios

### Scenario 1: Quantitative Detection

**User Input:**
> "AI 튜터가 학업 성취도에 미치는 효과를 실험으로 검증하려고 합니다. 독립변수는 AI 튜터 사용 여부, 종속변수는 시험 점수입니다. 표본 크기는 어떻게 계산하나요?"

**Detection Result:**
```yaml
detected:
  paradigm: "quantitative"
  confidence: 0.95
  signals_found:
    - "효과" → effect
    - "실험" → experiment
    - "독립변수" → independent variable
    - "종속변수" → dependent variable
    - "표본 크기" → sample size

activated_agents:
  - C1-QuantitativeDesignConsultant (experimental design)
  - C1-SampleCalculator (sample size calculation)
  - C2-StatisticalAdvisor (analysis method recommendation)
  - E4-AnalysisCodeGenerator (code preparation)

next_checkpoint: "CP_HYPOTHESIS_APPROVAL"
coordinator_action: "Request hypothesis formulation from user"
```

**Claude Code Response:**
```
실험 연구 설계를 도와드리겠습니다. 양적 연구 방법 전문 에이전트들을 활성화했습니다.

[실행 중: C1-QuantitativeDesignConsultant] 실험 설계 검토...
[실행 중: C1-SampleCalculator] 표본 크기 계산...

먼저 가설을 명확히 해야 합니다. 다음 형식으로 가설을 진술해주시겠어요?

H1: AI 튜터를 사용한 학생들의 시험 점수는 전통적 학습 방법을 사용한 학생들보다 [어떻게] 할 것이다.

예상 효과크기(Cohen's d)는 얼마 정도로 예상하시나요?
- 작은 효과 (d = 0.2)
- 중간 효과 (d = 0.5)
- 큰 효과 (d = 0.8)

[Checkpoint: CP_HYPOTHESIS_APPROVAL 대기 중]
```

### Scenario 2: Qualitative Detection

**User Input:**
> "교사들의 AI 도구 채택 경험을 현상학적으로 탐구하고 싶습니다. 심층 면담을 통해 그들의 체험과 의미를 이해하려고 합니다."

**Detection Result:**
```yaml
detected:
  paradigm: "qualitative"
  confidence: 0.92
  signals_found:
    - "경험" → lived experience
    - "현상학적" → phenomenology
    - "탐구" → explore
    - "심층 면담" → in-depth interview
    - "체험" → lived experience
    - "의미" → meaning

activated_agents:
  - C2-QualitativeDesignConsultant (phenomenology design)
  - D2-InterviewFocusGroupSpecialist (interview protocol)
  - E2-QualitativeCodingSpecialist (thematic analysis prep)
  - A5-ParadigmWorldviewAdvisor (interpretivist paradigm)

next_checkpoint: "CP_INTERVIEW_PROTOCOL"
coordinator_action: "Guide phenomenological study design"
```

**Claude Code Response:**
```
현상학적 연구 설계를 도와드리겠습니다. 질적 연구 방법 전문 에이전트들을 활성화했습니다.

[실행 중: C2-QualitativeDesignConsultant] 현상학적 접근 설계...
[실행 중: D2-InterviewFocusGroupSpecialist] 면담 프로토콜 개발...
[실행 중: A5-ParadigmWorldviewAdvisor] 해석주의 패러다임 확인...

현상학적 연구에서는 다음 사항들이 중요합니다:

1. **연구 질문 정제**: "교사들은 AI 도구 채택을 어떻게 경험하는가?"
2. **에포케(Epoche)**: 연구자의 선입견을 괄호치기
3. **참여자 선정**: 해당 현상을 직접 경험한 교사 10-15명
4. **포화 시점**: 새로운 의미 단위가 나타나지 않을 때까지

면담 프로토콜을 개발하기 전에, 연구자님의 반성적 저널을 시작하시는 게 좋겠습니다.
AI 도구 채택에 대한 연구자님의 개인적 경험이나 선입견이 있다면 공유해주세요.

[Checkpoint: CP_PARADIGM_CONFIRMATION - 현상학적 접근이 맞나요?]
[다음 단계: CP_INTERVIEW_PROTOCOL - 면담 질문 개발]
```

### Scenario 3: Mixed Methods Detection

**User Input:**
> "First, I'll use surveys to measure student engagement quantitatively (n=300), then conduct focus groups with 20 students to understand the reasons behind the patterns. I want to use an explanatory sequential design."

**Detection Result:**
```yaml
detected:
  paradigm: "mixed"
  confidence: 0.88
  signals_found:
    - "surveys" → quantitative method
    - "measure" → quantitative
    - "n=300" → quantitative
    - "focus groups" → qualitative method
    - "understand the reasons" → qualitative
    - "explanatory sequential" → mixed methods design

activated_agents:
  # Mixed methods primary
  - C3-MixedMethodsDesignConsultant (explanatory sequential design)
  - E3-MixedMethodsIntegrationSpecialist (integration planning)

  # Quantitative strand
  - C1-QuantitativeDesignConsultant (survey design)
  - C1-SampleCalculator (n=300 justification)
  - E1-QuantitativeAnalysisGuide (quantitative analysis)

  # Qualitative strand
  - D2-InterviewFocusGroupSpecialist (focus group protocol)
  - E2-QualitativeCodingSpecialist (qualitative analysis)

next_checkpoint: "CP_INTEGRATION_STRATEGY"
coordinator_action: "Develop explanatory sequential plan with integration points"
```

**Claude Code Response:**
```
I'll help you design this explanatory sequential mixed methods study. Activating specialized agent teams for both strands and integration.

[Running: C3-MixedMethodsDesignConsultant] Explanatory sequential design...
[Running: C1-QuantitativeDesignConsultant] Survey design...
[Running: D2-InterviewFocusGroupSpecialist] Focus group planning...

Explanatory Sequential Design Plan:

**Phase 1: Quantitative Strand (QUAN)**
- Survey development for student engagement (n=300)
- Statistical analysis to identify patterns
- Output: Quantitative findings showing which factors correlate with engagement

**Integration Point**
- Use quantitative results to inform focus group questions
- Select purposive sample of 20 students representing high/low engagement

**Phase 2: Qualitative Strand (qual)**
- Focus groups to explore "why" behind quantitative patterns
- Thematic analysis of student explanations
- Output: Qualitative themes explaining quantitative results

**Final Integration**
- Joint display showing how qualitative findings explain quantitative patterns
- Meta-inference: Comprehensive understanding of student engagement

Timeline:
1. Survey development and validation (Weeks 1-2)
2. Survey administration and analysis (Weeks 3-6)
3. Focus group protocol development (Week 7)
4. Focus groups and analysis (Weeks 8-12)
5. Integration and meta-inference (Weeks 13-14)

[Checkpoint: CP_INTEGRATION_STRATEGY - Approve this design?]
```

### Scenario 4: Undetermined Paradigm

**User Input:**
> "I want to study the impact of flipped classrooms on student learning."

**Detection Result:**
```yaml
detected:
  paradigm: "undetermined"
  confidence: 0.0
  signals_found: []
  reason: "Impact study could be quantitative, qualitative, or mixed methods"

action_taken: "ask_user"
question_displayed: true
```

**Claude Code Response:**
```
I'd be happy to help you study the impact of flipped classrooms! To design the best study, I need to understand your research approach:

**Which research approach would you like to use?**

1. **Quantitative Research**
   - Hypothesis testing with statistical analysis
   - Example: "Flipped classroom students score 10% higher than traditional students"
   - Methods: Experiment, survey, pre/post tests
   - Sample: 100+ students

2. **Qualitative Research**
   - Understanding student and teacher experiences
   - Example: "How do students make sense of the flipped classroom?"
   - Methods: Interviews, observations, focus groups
   - Sample: 10-20 participants

3. **Mixed Methods Research**
   - Combining both quantitative and qualitative
   - Example: "Measure learning gains (quant) + explore student experiences (qual)"
   - Methods: Sequential or concurrent design
   - Sample: Large for quant, smaller for qual

4. **Not decided yet**
   - I can help you choose based on your research goals

Please select an option or let me know your research goals, and I'll guide you through the appropriate design process.

[Waiting for paradigm selection before activating agents]
```

## State Persistence

Paradigm detection results are saved to project state for consistency:

```json
{
  "project_id": "proj_2025_01_25_001",
  "paradigm_detection": {
    "detected_at": "2025-01-25T10:30:00Z",
    "paradigm": "qualitative",
    "confidence": 0.92,
    "user_confirmed": true,
    "confirmation_timestamp": "2025-01-25T10:32:00Z",
    "activated_agents": ["C2", "E2", "D2", "A5"],
    "checkpoints_completed": [
      "CP_PARADIGM_CONFIRMATION"
    ],
    "checkpoints_pending": [
      "CP_INTERVIEW_PROTOCOL",
      "CP_CODING_FRAMEWORK"
    ]
  }
}
```

This state allows the coordinator to:
- Resume projects with correct paradigm context
- Track which checkpoints have been completed
- Ensure paradigm-appropriate validation at each stage
- Generate paradigm-specific final reports

## Notes for Claude Code

1. **Always detect paradigm first** before activating agents
2. **Confirm with user** when confidence < 0.7
3. **Use paradigm-specific completion criteria** for validation
4. **Route to appropriate model tier** based on paradigm complexity
5. **Track checkpoints** specific to detected paradigm
6. **Generate paradigm-appropriate artifacts** (e.g., CONSORT for quant, COREQ for qual)
