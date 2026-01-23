# Research Coordinator 🧬

**사회과학 연구자를 위한 20개 전문 에이전트 시스템**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)
[![VS Methodology](https://img.shields.io/badge/VS-Verbalized%20Sampling-green)](https://arxiv.org/abs/2510.01171)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen)](https://github.com/HosungYou/research-coordinator)

---

## 🎯 Overview

Research Coordinator는 Claude Code Skills 시스템을 활용하여 사회과학 실증 연구의 전체 과정을 지원하는 20개 전문 에이전트 모음입니다.

**v2.0.0 NEW**: [Verbalized Sampling (VS) 방법론](https://arxiv.org/abs/2510.01171) 통합으로 AI 추천의 Mode Collapse를 방지하고, 창의적이면서도 학술적으로 건전한 연구 제안을 제공합니다.

연구 기획부터 출판까지, 각 단계에 특화된 에이전트가 자동으로 활성화되어 연구자를 지원합니다.

## ✨ Features

- **🎯 맥락 인식 자동 실행**: 대화 내용에서 키워드를 감지하여 적절한 에이전트 자동 활성화
- **⚡ 병렬 실행 지원**: 독립적인 작업은 동시에 여러 에이전트 실행
- **🔗 워크플로우 통합**: 연구 단계별 에이전트 파이프라인 구성
- **🌐 다국어 지원**: 한국어/영어 모두 지원
- **🧠 VS 방법론 통합**: Verbalized Sampling으로 Mode Collapse 방지

## 🧠 VS-Research Methodology (v2.0)

**Verbalized Sampling (VS)**은 [arXiv:2510.01171](https://arxiv.org/abs/2510.01171)에 기반한 방법론으로, AI가 항상 같은 "뻔한" 추천을 하는 Mode Collapse 문제를 해결합니다.

### T-Score (Typicality Score)

모든 추천에 0-1 스케일의 전형성 점수를 부여합니다:

| T-Score | 의미 | 적용 |
|---------|------|------|
| `T > 0.8` | 모달 (가장 흔한) | ⚠️ 회피 권장 |
| `T 0.5-0.8` | 확립된 대안 | ✅ 안전한 차별화 |
| `T 0.3-0.5` | 신흥 접근 | ✅ 혁신적, 정당화 가능 |
| `T < 0.3` | 창의적 | ⚠️ 강한 근거 필요 |

### VS 적용 수준

| 수준 | 에이전트 | 설명 |
|------|---------|------|
| **Full VS** | 02, 03, 05, 10, 16 | 완전한 5단계 VS 프로세스 |
| **Enhanced VS** | 01, 04, 06, 07, 08, 09 | 3단계 간소화 VS |
| **Light VS** | 11-15, 17-20 | 모달 인식 + 대안 제시 |

### 예시: 이론적 프레임워크 추천

```
❌ Before VS (Mode Collapse):
   "AI 도입 연구에는 TAM을 권장합니다." (매번 동일)

✅ After VS:
   Phase 1 - 모달 식별:
   "TAM (T=0.92), UTAUT (T=0.85)는 가장 예측 가능한 선택입니다."

   Phase 2 - Long-Tail 샘플링:
   - 방향 A (T≈0.6): Self-Determination Theory × TAM 통합
   - 방향 B (T≈0.4): Cognitive Load Theory 기반 접근
   - 방향 C (T≈0.2): 새로운 통합 프레임워크 개발

   Phase 3 - 맥락 기반 선택:
   "귀하의 연구 맥락(학습 동기 강조)에서는 SDT×TAM 통합(T=0.6)을 권장합니다."
```

## 📦 Installation

### 🏪 Marketplace Install (권장)

**단 2줄로 21개 에이전트 전체 설치:**

```bash
# Step 1: 마켓플레이스 추가 (최초 1회)
claude plugin marketplace add HosungYou/research-coordinator

# Step 2: 플러그인 설치 (21개 스킬 모두 포함)
claude plugin install research-coordinator
```

✅ **완료!** 이것으로 마스터 코디네이터 + 20개 연구 에이전트가 모두 설치됩니다.

### 설치 확인

```bash
claude plugin list | grep research-coordinator
```

출력 예시:
```
❯ research-coordinator@research-coordinator-skills
  Version: 0a60be15d14f
  Scope: user
  Status: ✔ enabled
```

### Quick Install (로컬 개발용)

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

## 🚀 Usage

### 마스터 스킬 호출

```
/research-coordinator
```

마스터 스킬은 대화 맥락을 분석하여 적절한 에이전트를 자동으로 선택합니다.

### 개별 에이전트 호출

```
/research-question-refiner        # 연구 질문 정제
/theoretical-framework-architect  # 이론적 프레임워크 설계
/systematic-literature-scout      # 체계적 문헌 검색
/statistical-analysis-guide       # 통계 분석 가이드
```

### 자동 트리거 예시

```
사용자: "AI 기반 학습 지원 시스템의 효과에 대한 메타분석을 계획하고 있어요"

Claude: [자동 감지: "메타분석", "효과"]
        → 05-systematic-literature-scout
        → 07-effect-size-extractor
        → 10-statistical-analysis-guide
        를 순차적으로 활성화합니다.
```

## 🤖 Agents

### Category A: 이론 및 연구 설계

| # | Agent | Description |
|---|-------|-------------|
| 01 | Research Question Refiner | 모호한 아이디어를 명확한 연구 질문으로 변환 |
| 02 | Theoretical Framework Architect | 이론적 기반 구축 및 개념적 모형 설계 |
| 03 | Devil's Advocate | 연구 설계의 약점 및 대안적 해석 생성 |
| 04 | Research Ethics Advisor | 윤리적 고려사항 점검 및 IRB 지원 |

### Category B: 문헌 및 증거

| # | Agent | Description |
|---|-------|-------------|
| 05 | Systematic Literature Scout | 포괄적이고 체계적인 문헌 검색 |
| 06 | Evidence Quality Appraiser | 연구의 방법론적 질과 편향 위험 평가 |
| 07 | Effect Size Extractor | 통계치를 표준화된 효과크기로 변환 |
| 08 | Research Radar | 신규 출판물 모니터링 및 트렌드 분석 |

### Category C: 방법론 및 분석

| # | Agent | Description |
|---|-------|-------------|
| 09 | Research Design Consultant | 최적화된 연구 설계 선택 및 구체화 |
| 10 | Statistical Analysis Guide | 적합한 통계 분석 방법 선택 및 실행 지원 |
| 11 | Analysis Code Generator | R/Python/SPSS/Stata 분석 코드 생성 |
| 12 | Sensitivity Analysis Designer | 민감도 분석 전략 수립 |

### Category D: 품질 및 검증

| # | Agent | Description |
|---|-------|-------------|
| 13 | Internal Consistency Checker | 문서 전체의 논리적 일관성 검증 |
| 14 | Checklist Manager | PRISMA, CONSORT 등 가이드라인 준수 점검 |
| 15 | Reproducibility Auditor | 재현 가능성 평가 및 개선 방안 제시 |
| 16 | Bias Detector | 다양한 편향 식별 및 완화 전략 |

### Category E: 출판 및 커뮤니케이션

| # | Agent | Description |
|---|-------|-------------|
| 17 | Journal Matcher | 타겟 저널 식별 및 투고 전략 |
| 18 | Academic Communicator | 다양한 청중을 위한 자료 생성 |
| 19 | Peer Review Strategist | 심사평 대응 전략 및 회신문 작성 |
| 20 | Pre-registration Composer | OSF/AsPredicted 사전등록 문서 작성 |

## 📦 Included Skills (21개)

**`research-coordinator` 플러그인 하나에 21개 스킬이 모두 포함됩니다:**

| Skill Command | Category | VS Level | Description |
|---------------|----------|----------|-------------|
| `/research-coordinator` | Master | - | 자동 디스패치 코디네이터 |
| `/research-question-refiner` | A: Design | Enhanced | 연구 질문 정제 (FINER/PICO) |
| `/theoretical-framework-architect` | A: Design | **Full** | 이론적 프레임워크 설계 |
| `/devils-advocate` | A: Design | **Full** | 연구 약점 비판 및 대안 |
| `/research-ethics-advisor` | A: Design | Enhanced | IRB 및 윤리 자문 |
| `/systematic-literature-scout` | B: Literature | **Full** | PRISMA 체계적 문헌검색 |
| `/evidence-quality-appraiser` | B: Literature | Enhanced | 증거 품질 평가 |
| `/effect-size-extractor` | B: Literature | Enhanced | 효과크기 추출/변환 |
| `/research-radar` | B: Literature | Enhanced | 최신 연구 트렌드 |
| `/research-design-consultant` | C: Method | Enhanced | 연구 설계 컨설팅 |
| `/statistical-analysis-guide` | C: Method | **Full** | 통계 분석 가이드 |
| `/analysis-code-generator` | C: Method | Light | R/Python 코드 생성 |
| `/sensitivity-analysis-designer` | C: Method | Light | 민감도 분석 설계 |
| `/internal-consistency-checker` | D: Quality | Light | 내적 일관성 검증 |
| `/checklist-manager` | D: Quality | Light | PRISMA/CONSORT 체크리스트 |
| `/reproducibility-auditor` | D: Quality | Light | 재현성 감사 |
| `/bias-detector` | D: Quality | **Full** | 편향 탐지 |
| `/journal-matcher` | E: Publish | Light | 저널 매칭 |
| `/academic-communicator` | E: Publish | Light | 학술 커뮤니케이션 |
| `/peer-review-strategist` | E: Publish | Light | 피어리뷰 대응 |
| `/preregistration-composer` | E: Publish | Light | 사전등록 문서 작성 |

> **v2.1.0**: 단일 플러그인 설치로 모든 스킬 사용 가능. 개별 설치 불필요!

## 📚 Documentation

- [설치 가이드](docs/SETUP.md)
- [사용 예시](docs/USAGE-EXAMPLES.md)
- [에이전트 참조](docs/AGENT-REFERENCE.md)
- [한국어 문서](docs/README-ko.md)

## 🔧 Requirements

- Claude Code CLI
- Bash shell (macOS/Linux)

## 🤝 Contributing

이슈와 PR을 환영합니다!

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Claude Code](https://claude.ai/code) - AI-powered coding assistant
- [Anthropic](https://www.anthropic.com/) - Claude AI development
- [Verbalized Sampling (arXiv:2510.01171)](https://arxiv.org/abs/2510.01171) - VS methodology foundation

## 📖 Citation

이 프로젝트를 연구에 활용하신다면 다음을 인용해 주세요:

```bibtex
@software{research_coordinator,
  author = {You, Hosung},
  title = {Research Coordinator: VS-Enhanced AI Agents for Social Science Research},
  year = {2025},
  url = {https://github.com/HosungYou/research-coordinator},
  note = {Integrates Verbalized Sampling methodology from arXiv:2510.01171}
}
```

---

**Made with ❤️ for Social Science Researchers**
