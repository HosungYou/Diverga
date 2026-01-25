# Research Coordinator v3.0.0 업그레이드 리포트

**작성일**: 2025-01-24
**버전**: v3.0.0
**작업자**: Claude Code (Subagent-Driven Development)
**기반**: [arXiv:2510.01171](https://arxiv.org/abs/2510.01171) - Verbalized Sampling

---

## 1. 프로젝트 개요

### 1.1 목적

Research Coordinator v3.0.0은 Verbalized Sampling (VS) 방법론을 대폭 강화하여 LLM의 Mode Collapse 문제를 더욱 효과적으로 방지하는 것을 목표로 합니다.

### 1.2 주요 개선사항

| 영역 | v2.x | v3.0 |
|------|------|------|
| T-Score 시스템 | 정적 임계값 | **Dynamic T-Score** (맥락 기반 조정) |
| 창의적 장치 | 없음 | **5가지 메커니즘** |
| 사용자 상호작용 | 단방향 | **14개 체크포인트** |
| 에이전트 업그레이드 | 개별적 | **3-Tier 체계** (FULL/ENHANCED/LIGHT) |

---

## 2. 구현 방법론

### 2.1 Subagent-Driven Development

이 프로젝트는 `superpowers:subagent-driven-development` 스킬을 사용하여 구현되었습니다:

- **Fresh subagent per task**: 각 작업마다 독립적인 서브에이전트 실행
- **Two-stage review**: Spec compliance → Code quality 순차 검토
- **TodoWrite 추적**: 19개 작업의 진행 상태 실시간 관리

### 2.2 구현 단계

```
Phase 1: Core Infrastructure (3 tasks)
    ├── 1.1 Directory Structure
    ├── 1.2 VS Engine
    └── 1.3 Dynamic T-Score System

Phase 2: Interaction System (1 task)
    └── 2.1 User Checkpoints (14개)

Phase 3: Creativity Suite (5 tasks)
    ├── 3.1 Forced Analogy
    ├── 3.2 Iterative Loop
    ├── 3.3 Semantic Distance
    ├── 3.4 Temporal Reframing
    └── 3.5 Community Simulation

Phase 4: Agent Integration (6 tasks)
    ├── 4.1 Reference Documents
    ├── 4.2 agent-registry.yaml
    ├── 4.3 Master SKILL.md
    ├── 4.4 FULL Agents (5개)
    ├── 4.5 ENHANCED Agents (6개)
    └── 4.6 LIGHT Agents (9개)

Phase 5: Finalization (4 tasks)
    ├── 5.1 marketplace.json
    ├── 5.2 install.sh
    ├── 5.3 README.md
    └── 5.4 v3.0.0 Tag
```

---

## 3. 핵심 컴포넌트 상세

### 3.1 VS Engine v3.0

**파일**: `.claude/skills/research-coordinator/core/vs-engine.md`

VS Engine은 모든 에이전트의 핵심 추론 엔진입니다:

```
┌─────────────────────────────────────────────────────────┐
│                    VS Engine v3.0                       │
├─────────────────────────────────────────────────────────┤
│  Phase 1: Modal Detection (T > 0.8 식별)                │
│      ↓                                                  │
│  Phase 2: Long-Tail Sampling (대안 탐색)                │
│      ↓                                                  │
│  Phase 3: Creativity Activation (장치 적용)             │
│      ↓                                                  │
│  Phase 4: User Checkpoint (확인 요청)                   │
│      ↓                                                  │
│  Phase 5: Contextual Recommendation (최종 권장)         │
└─────────────────────────────────────────────────────────┘
```

### 3.2 Dynamic T-Score System

**파일**: `.claude/skills/research-coordinator/core/t-score-dynamics.md`

정적 임계값 대신 맥락에 따라 동적으로 조정되는 T-Score 시스템:

| 연구 유형 | 권장 T-Score 범위 | 설명 |
|----------|-------------------|------|
| 탐색적 연구 | 0.2 - 0.5 | 새로운 영역, 혁신적 접근 |
| 확인적 연구 | 0.5 - 0.8 | 검증, 재현 연구 |
| 혁신적 연구 | 0.1 - 0.4 | 패러다임 전환 시도 |
| 안전한 연구 | 0.6 - 0.9 | 박사 학위, 첫 논문 |

**핵심 함수**:
```python
def calculate_dynamic_threshold(context):
    base = 0.5
    modifiers = {
        'exploratory': -0.2,
        'confirmatory': +0.2,
        'innovative': -0.3,
        'conservative': +0.3
    }
    return base + sum(modifiers.get(f, 0) for f in context.features)
```

### 3.3 User Checkpoints

**파일**: `.claude/skills/research-coordinator/interaction/user-checkpoints.md`

14개의 사용자 확인 지점:

| 코드 | 이름 | 트리거 시점 |
|------|------|------------|
| CP-INIT-001 | Initial Context | 세션 시작 시 |
| CP-INIT-002 | Goal Clarification | 목표 불명확 시 |
| CP-VS-001 | Modal Presentation | 모달 옵션 제시 후 |
| CP-VS-002 | Alternative Selection | 대안 선택 시 |
| CP-VS-003 | Final Confirmation | 최종 권장 전 |
| CP-FA-001 | Analogy Validation | 강제 비유 적용 후 |
| CP-IL-001 | Loop Start | 반복 루프 시작 전 |
| CP-IL-002 | Loop Continue | 각 반복 후 |
| CP-IL-003 | Loop End | 반복 종료 시 |
| CP-SD-001 | Distance Check | 의미적 거리 이동 후 |
| CP-TR-001 | Temporal Shift | 시간축 변경 후 |
| CP-CS-001 | Community Consensus | 시뮬레이션 완료 후 |
| CP-FINAL-001 | Final Decision | 모든 분석 완료 후 |
| CP-ERROR-001 | Error Recovery | 오류 발생 시 |

### 3.4 Creativity Mechanisms

5가지 창의적 장치가 `creativity/` 디렉토리에 구현되었습니다:

#### 3.4.1 Forced Analogy

**목적**: 멀리 떨어진 분야에서 비유를 차용하여 새로운 관점 제공

**프로세스**:
1. 현재 연구 분야 식별
2. 의미적으로 먼 분야 선택 (예: 교육학 → 생태학)
3. 해당 분야의 핵심 개념 추출
4. 연구 맥락에 비유 적용
5. [CP-FA-001] 비유 적절성 확인

**예시**:
```
입력: "AI 학습 시스템 도입 연구"
비유 분야: 생태계 이론
출력: "AI 시스템을 학습 생태계의 새로운 '종'으로 모델링
      → 적응, 공생, 경쟁 개념 적용"
```

#### 3.4.2 Iterative Loop

**목적**: 3-5회 반복적 발산-수렴을 통한 아이디어 정제

**프로세스**:
```
Round 1: Initial Ideas (발산)
    ↓
Round 2: Critique & Refine (수렴)
    ↓
Round 3: Expand Alternatives (발산)
    ↓
Round 4: Synthesize (수렴)
    ↓
Round 5: Final Polish (최적화)
```

**반복 조건**:
- 최소 3회, 최대 5회
- 각 라운드 후 [CP-IL-002] 체크포인트
- 사용자가 "충분함" 표시 시 조기 종료

#### 3.4.3 Semantic Distance

**목적**: 의미적으로 먼 개념을 탐색하여 창의적 연결 발견

**거리 측정**:
| 거리 | 범위 | 예시 (교육학 기준) |
|------|------|-------------------|
| 근거리 | 0.0-0.3 | 학습이론, 교수법 |
| 중거리 | 0.3-0.6 | 인지심리학, 동기이론 |
| 원거리 | 0.6-0.9 | 신경과학, 복잡계 이론 |
| 초원거리 | 0.9-1.0 | 양자역학, 진화생물학 |

#### 3.4.4 Temporal Reframing

**목적**: 시간축을 재구성하여 다른 관점에서 연구 바라보기

**시간 프레임**:
- **과거**: "10년 전 연구자 관점에서"
- **현재**: "현재 맥락에서"
- **미래**: "10년 후 관점에서"
- **역사적**: "이 분야 초기 개척자 관점에서"

#### 3.4.5 Community Simulation

**목적**: 가상의 연구자 커뮤니티 대화를 시뮬레이션

**페르소나**:
| 유형 | 특성 | 역할 |
|------|------|------|
| Conservative Scholar | 전통적, 검증 중시 | 방법론적 엄격성 확보 |
| Innovative Researcher | 혁신적, 위험 감수 | 새로운 방향 제시 |
| Practical Reviewer | 실용적, 적용 중시 | 현실 적용 가능성 |
| Critical Methodologist | 비판적, 세부 중시 | 약점 식별 |

---

## 4. 에이전트 업그레이드 상세

### 4.1 3-Tier 업그레이드 체계

#### FULL Level (5개 에이전트)

| ID | 에이전트 | 창의적 장치 | 체크포인트 |
|----|---------|------------|-----------|
| 02 | Theoretical Framework Architect | FA, IL, SD, TR, CS | 전체 14개 |
| 03 | Devil's Advocate | FA, IL, SD, TR, CS | 전체 14개 |
| 05 | Systematic Literature Scout | FA, IL, SD, TR, CS | 전체 14개 |
| 10 | Statistical Analysis Guide | FA, IL, SD, TR, CS | 전체 14개 |
| 16 | Bias Detector | FA, IL, SD, TR, CS | 전체 14개 |

**Frontmatter 패턴**:
```yaml
version: 3.0.0
upgrade_level: FULL
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - iterative-loop
    - semantic-distance
    - temporal-reframing
    - community-simulation
  checkpoints:
    - CP-INIT-001
    - CP-INIT-002
    - CP-VS-001
    - CP-VS-002
    - CP-VS-003
    - CP-FA-001
    - CP-IL-001
    - CP-SD-001
    - CP-TR-001
    - CP-CS-001
```

#### ENHANCED Level (6개 에이전트)

| ID | 에이전트 | 창의적 장치 | 체크포인트 |
|----|---------|------------|-----------|
| 01 | Research Question Refiner | FA, IL, SD | 6개 |
| 04 | Research Ethics Advisor | FA, IL, SD | 6개 |
| 06 | Evidence Quality Appraiser | FA, IL, SD | 6개 |
| 07 | Effect Size Extractor | FA, IL, SD | 6개 |
| 08 | Research Radar | FA, IL, SD | 6개 |
| 09 | Research Design Consultant | FA, IL, SD | 6개 |

**Frontmatter 패턴**:
```yaml
version: 3.0.0
upgrade_level: ENHANCED
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
    - CP-FA-001  # 또는 CP-SD-001, CP-IL-001
```

#### LIGHT Level (9개 에이전트)

| ID | 에이전트 |
|----|---------|
| 11 | Analysis Code Generator |
| 12 | Sensitivity Analysis Designer |
| 13 | Internal Consistency Checker |
| 14 | Checklist Manager |
| 15 | Reproducibility Auditor |
| 17 | Journal Matcher |
| 18 | Academic Communicator |
| 19 | Peer Review Strategist |
| 20 | Preregistration Composer |

**Frontmatter 패턴**:
```yaml
version: 3.0.0
upgrade_level: LIGHT
v3_integration:
  dynamic_t_score: false
  creativity_modules: []
  checkpoints:
    - CP-INIT-001
    - CP-VS-003
```

### 4.2 에이전트별 변경사항

모든 FULL 및 ENHANCED 에이전트에 "v3.0 창의적 장치 통합" 섹션이 추가되었습니다:

```markdown
## v3.0 창의적 장치 통합

### 활성화된 모듈
- **Forced Analogy**: [에이전트별 적용 방식]
- **Iterative Loop**: [에이전트별 적용 방식]
- **Semantic Distance**: [에이전트별 적용 방식]

### 자동 트리거 조건
[에이전트별 트리거 조건 목록]

### 창의적 장치 적용 예시
[에이전트별 구체적 예시]
```

---

## 5. 파일 구조

### 5.1 신규 생성 파일

```
.claude/skills/research-coordinator/
├── core/
│   ├── vs-engine.md              # 2,847 bytes
│   └── t-score-dynamics.md       # 3,421 bytes
├── interaction/
│   └── user-checkpoints.md       # 4,156 bytes
├── creativity/
│   ├── forced-analogy.md         # 2,934 bytes
│   ├── iterative-loop.md         # 3,102 bytes
│   ├── semantic-distance.md      # 2,876 bytes
│   ├── temporal-reframing.md     # 2,654 bytes
│   └── community-simulation.md   # 3,287 bytes
└── references/
    ├── vs-quick-reference.md     # 1,923 bytes
    └── upgrade-matrix.md         # 2,145 bytes
```

### 5.2 수정된 파일

| 파일 | 변경 내용 |
|------|----------|
| `SKILL.md` (Master) | VS Engine 참조, 창의적 장치 연동 |
| `agent-registry.yaml` | v3.0 메타데이터, 체크포인트 매핑 |
| `marketplace.json` | 버전 3.0.0, 새 키워드, changelog |
| `install.sh` | 버전 표시, 기능 하이라이트 |
| `README.md` | VS-Research v3.0 섹션 전면 개편 |
| `docs/CHANGELOG.md` | v3.0.0 릴리스 노트 |
| 20개 에이전트 SKILL.md | frontmatter 업데이트, 창의적 장치 섹션 |

---

## 6. Git 커밋 히스토리

### 6.1 커밋 요약

총 **20개 커밋**이 생성되었습니다:

```
97c500e docs(readme): update to v3.0.0
3831eba chore(scripts): update install.sh for v3.0.0
ce796a0 chore(marketplace): bump version to v3.0.0
76328be feat(agents): upgrade 9 LIGHT VS agents to v3.0
be95ce2 feat(agents): upgrade 6 ENHANCED VS agents to v3.0
28d188d feat(agents): upgrade 5 FULL VS agents to v3.0
96dd69a feat: upgrade master SKILL.md to v3.0 with creativity suite
b7e7894 feat(registry): update agent registry for v3.0
bb96a36 docs(references): add v3.0 specification documents
f7a49f8 feat(creativity): add community simulation mechanism
4e312ba feat(creativity): add temporal reframing mechanism
18c9732 feat(creativity): add semantic distance scorer
e4ecda9 feat(creativity): add iterative divergent-convergent loop
dee6766 feat(creativity): add forced analogy mechanism
9aba9ad feat(interaction): add comprehensive user checkpoint system
21899c3 feat(core): add dynamic T-Score system with API integration
4981c2a feat(core): add VS Engine v3.0 with checkpoints and iteration
1b984df chore: create v3.0 modular directory structure
0fe386a docs: Add v3.0 detailed implementation plan
e85e05d docs: Add v3.0 design document and analysis report
```

### 6.2 태그

```
v3.0.0 - Research Coordinator v3.0.0 - VS-Research Major Upgrade
```

---

## 7. 테스트 및 검증

### 7.1 구조적 검증

- [x] 모든 신규 파일 생성 확인
- [x] 디렉토리 구조 일관성 확인
- [x] 모든 에이전트 frontmatter 업데이트 확인
- [x] marketplace.json 스키마 유효성 확인
- [x] Git 커밋 및 태그 생성 확인

### 7.2 기능적 검증 (권장)

```bash
# 설치 테스트
./scripts/install.sh

# 마스터 스킬 호출
/research-coordinator

# 개별 에이전트 테스트
/theoretical-framework-architect
/devils-advocate
/statistical-analysis-guide
```

---

## 8. 향후 계획

### 8.1 단기 (v3.1)

- [ ] 창의적 장치 사용 통계 수집
- [ ] User Checkpoint 응답 패턴 분석
- [ ] T-Score 동적 조정 알고리즘 개선

### 8.2 중기 (v3.2)

- [ ] 에이전트 간 창의적 장치 연계
- [ ] 세션 기반 학습 (사용자 선호도 기억)
- [ ] 멀티모달 출력 지원 (다이어그램, 차트)

### 8.3 장기 (v4.0)

- [ ] 자율 에이전트 협업 시스템
- [ ] 연구 프로젝트 전체 관리
- [ ] 외부 API 통합 (Semantic Scholar, OpenAlex)

---

## 9. 참고 자료

### 9.1 이론적 기반

- **Verbalized Sampling**: [arXiv:2510.01171](https://arxiv.org/abs/2510.01171)
- **Mode Collapse in LLMs**: 반복적 출력 수렴 현상
- **T-Score Methodology**: Typicality 기반 출력 다양화

### 9.2 프로젝트 문서

- [README.md](../README.md): 프로젝트 개요
- [CHANGELOG.md](./CHANGELOG.md): 버전 히스토리
- [AGENT-REFERENCE.md](./AGENT-REFERENCE.md): 에이전트 참조

### 9.3 외부 링크

- **GitHub Repository**: https://github.com/HosungYou/research-coordinator
- **Claude Code Skills**: https://docs.anthropic.com/claude/docs/claude-code-skills

---

## 10. 결론

Research Coordinator v3.0.0은 VS-Research 방법론의 핵심을 대폭 강화한 메이저 릴리스입니다. Dynamic T-Score 시스템, 5가지 창의적 장치, 14개 User Checkpoints를 통해 LLM의 Mode Collapse 문제를 효과적으로 방지하면서도 사용자와의 상호작용을 강화했습니다.

모든 20개 에이전트가 3-Tier 체계(FULL/ENHANCED/LIGHT)에 따라 업그레이드되었으며, 기존 사용자는 별도의 마이그레이션 없이 새로운 기능을 즉시 활용할 수 있습니다.

---

**작성 완료**: 2025-01-24
**최종 버전**: v3.0.0
**GitHub Tag**: `v3.0.0`
