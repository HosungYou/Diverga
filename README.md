# Research Coordinator 🧬

**사회과학 연구자를 위한 20개 전문 에이전트 시스템**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skills-blue)](https://claude.ai/code)

---

## 🎯 Overview

Research Coordinator는 Claude Code Skills 시스템을 활용하여 사회과학 실증 연구의 전체 과정을 지원하는 20개 전문 에이전트 모음입니다.

연구 기획부터 출판까지, 각 단계에 특화된 에이전트가 자동으로 활성화되어 연구자를 지원합니다.

## ✨ Features

- **🎯 맥락 인식 자동 실행**: 대화 내용에서 키워드를 감지하여 적절한 에이전트 자동 활성화
- **⚡ 병렬 실행 지원**: 독립적인 작업은 동시에 여러 에이전트 실행
- **🔗 워크플로우 통합**: 연구 단계별 에이전트 파이프라인 구성
- **🌐 다국어 지원**: 한국어/영어 모두 지원

## 📦 Installation

### Quick Install

```bash
git clone https://github.com/HosungYou/research-coordinator.git
cd research-coordinator
./scripts/install.sh
```

### Manual Install

```bash
# 스킬 디렉토리 생성
mkdir -p ~/.claude/skills

# 심볼릭 링크 생성
ln -sf /path/to/research-coordinator/.claude/skills/research-coordinator ~/.claude/skills/
ln -sf /path/to/research-coordinator/.claude/skills/research-agents ~/.claude/skills/
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

---

**Made with ❤️ for Social Science Researchers**
