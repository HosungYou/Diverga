# 21-Conceptual-Framework-Visualizer: Nanobanana Integration Update

**Date:** 2025-01-25
**Version:** v3.1.1
**Author:** Research Coordinator System

---

## Summary

21-Conceptual-Framework-Visualizer 에이전트에 Google Gemini API 기반 **Nanobanana** 이미지 생성 기능을 통합하였습니다. 이를 통해 연구자는 ASCII Blueprint로 구조를 설계한 후, AI 이미지 생성으로 전문적인 학술 시각화를 빠르게 생성할 수 있습니다.

---

## New Features

### 1. CP_RENDERING_METHOD Checkpoint

Phase 4 (코드 생성) 완료 후 렌더링 방식을 선택하는 체크포인트 추가:

| 옵션 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **Code-First** | Python/Mermaid/Graphviz/D3.js | 정확한 레이아웃, 벡터 품질 | 복잡한 디버깅 |
| **Nanobanana** | Gemini API 이미지 생성 | 빠른 프로토타이핑 | API 키 필요 |
| **Hybrid** (권장) | Code 구조 + Nanobanana 렌더링 | 정확한 구조 + 고품질 | 두 단계 필요 |

### 2. ASCII Blueprint → Nanobanana Workflow

**핵심 원칙:** ASCII 레이아웃으로 구조를 확정한 후, 이를 Nanobanana의 "청사진"으로 전달

```
Phase 2: ASCII 레이아웃 제시
    ↓
[CP_VISUALIZATION_PREFERENCE] 방향 선택
    ↓
Phase 4: ASCII Blueprint 확정
    ↓
[CP_RENDERING_METHOD] → Nanobanana 선택
    ↓
Nanobanana: Blueprint 기반 창의적 렌더링
    ↓
[CP_QUALITY_REVIEW] → AI 품질 검토
```

**ASCII Blueprint의 역할:**
- 📐 **구조적 제약**: 요소의 위치, 계층, 연결 관계를 고정
- 🎨 **창의적 자유**: 색상, 스타일, 시각적 표현은 Nanobanana에게 위임
- ✅ **검증 가능**: 생성된 이미지가 Blueprint 구조를 따르는지 확인

### 3. CP_QUALITY_REVIEW Checkpoint

Nanobanana 생성 후 AI가 이미지를 검토하여 품질 문제를 식별:

| 카테고리 | 검토 항목 | 심각도 |
|---------|----------|--------|
| 텍스트 정확성 | 라벨/제목 정확성, 철자 오류 | 🔴 Critical |
| 구조적 정합성 | ASCII Blueprint 준수, 요소 포함 | 🟠 High |
| 시각적 품질 | 해상도, 색상 대비 | 🟡 Medium |
| 이론적 정확성 | 인용(저자명, 연도) 정확성 | 🔴 Critical |

### 4. Nanobanana Model Comparison

| 모델 | 텍스트 품질 | 권장 용도 |
|------|-----------|----------|
| `gemini-2.0-flash-exp` | ⚠️ 낮음 | 빠른 프로토타이핑 |
| `gemini-2.5-flash-image` | 🟡 중간 | 일반 사용 (Nano Banana) |
| `gemini-3-pro-image-preview` | ✅ 높음 | **출판용 권장 (Nano Banana Pro)** |

---

## Implementation Example: AIMC Framework v2.3

### Context

GenAI-HE-Review 프로젝트의 AIMC Framework를 새로운 이론적 기반으로 시각화:

**이론적 통합:**
- Nelson & Narens (1990): 이중 수준 메타인지 모델
- Efklides (2008): 메타인지 3차원 (Knowledge, Experiences, Skills)
- Salomon (1993): "effects OF" vs "effects WITH" technology

### ASCII Blueprint (선택된 방향 B)

```
          Efklides' Metacognitive Dimensions
          ─────────────────────────────────────
          Knowledge  │ Experiences │  Skills
┌─────────┼──────────┼─────────────┼──────────┐
│   L3    │  Task    │   Transfer  │ Autonomy │
│Autonomous│ Strategy │   JOL/FOK   │ Planning │
├─────────┼──────────┼─────────────┼──────────┤
│   L2    │   AI     │ Calibration │  AI      │
│Meta-AI  │Capability│  Accuracy   │Selection │
├─────────┼──────────┼─────────────┼──────────┤
│   L1    │ Expanded │  Supported  │ Guided   │
│Supported│ Object   │   FOD/JOL   │Monitoring│
└─────────┴──────────┴─────────────┴──────────┘
                    ▲
      DISTRIBUTED METACOGNITION
```

### Generation Results

| 시도 | 모델 | 결과 |
|------|------|------|
| 1차 | `gemini-2.0-flash-exp` | ❌ 텍스트 깨짐 ("Frarrowork", "Experiencs") |
| 2차 | `gemini-3-pro-image-preview` | ✅ 텍스트 품질 개선 |

### Quality Review Issues (1차 생성)

| 위치 | 잘못된 텍스트 | 올바른 텍스트 |
|------|-------------|-------------|
| 제목 | "Frarrowork v2.3" | "Framework v2.3" |
| 헤더 | "EXPERIENCS", "SKILS" | "EXPERIENCES", "SKILLS" |
| L1 셀 | "Deplrocted (Al-entenpod)" | "Supported FOD/JOL" |
| 출처 | "Clark & Championatzra (198e9)" | "Clark & Chalmers (1998)" |

---

## Setup Instructions

### Prerequisites

```bash
# 1. Google API 키 설정
export GOOGLE_API_KEY="your-api-key"
# API 키 획득: https://aistudio.google.com/apikey

# 2. google-genai 패키지 설치
pip install google-genai
```

### Usage Template

```python
from google import genai

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",  # Nano Banana Pro
    contents=prompt,
    config={"response_modalities": ["TEXT", "IMAGE"]}
)
```

---

## Files Changed

### research-coordinator

| File | Change |
|------|--------|
| `.claude/skills/research-agents/21-conceptual-framework-visualizer/SKILL.md` | +152 lines |

**Commits:**
- `0ae63e6` - feat(agent): add Nanobanana (Gemini API) integration
- `1434c00` - feat(agent): add ASCII Blueprint → Nanobanana workflow rule
- `6e0a72f` - feat(agent): add CP_QUALITY_REVIEW checkpoint and update Nanobanana models

### GenAI-HE-Review

| File | Change |
|------|--------|
| `figures/generate_aimc_matrix_nanobanana.py` | New file |
| `figures/AIMC_Framework_v2.3_Matrix.jpg` | New file (Nano Banana Pro) |
| `figures/AIMC_Framework_v2.3_Matrix.png` | Previous version (gemini-2.0-flash-exp) |

**Commits:**
- `ae6a779` - feat(figures): add AIMC Framework v2.3 Matrix-Layer visualization
- `684fe60` - feat(figures): regenerate AIMC with Nano Banana Pro model

---

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│           21-Conceptual-Framework-Visualizer v3.1.1             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 0: 맥락 수집 (이론, 변수, 가설)                          │
│         ↓                                                       │
│  Phase 1: 모달 시각화 식별 (T > 0.8 금지)                       │
│         ↓                                                       │
│  Phase 2: Long-Tail 샘플링 (ASCII Layout 제시)                  │
│         ↓                                                       │
│  [CP_VISUALIZATION_PREFERENCE] 방향 선택                        │
│         ↓                                                       │
│  [CP_T_SCORE_APPROVAL] T-Score 승인                            │
│         ↓                                                       │
│  Phase 3: 기술 스택 선택                                        │
│         ↓                                                       │
│  Phase 4: 코드/Blueprint 생성                                   │
│         ↓                                                       │
│  [CP_RENDERING_METHOD] 렌더링 방식 선택                         │
│     ├─ Code-First → 코드 실행                                  │
│     ├─ Nanobanana → Gemini API 생성                            │
│     └─ Hybrid → 구조 + AI 렌더링                               │
│         ↓                                                       │
│  [CP_QUALITY_REVIEW] AI 품질 검토                               │
│     └─ 문제 발견 시 → 재생성                                   │
│         ↓                                                       │
│  [CP_ORIGINALITY_CHECK] 독창성 검증                             │
│         ↓                                                       │
│  Phase 5: 최종 출력                                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Best Practices

1. **모델 선택**: 출판용은 항상 `gemini-3-pro-image-preview` (Nano Banana Pro) 사용
2. **ASCII Blueprint**: Phase 2에서 구조를 명확히 정의하여 생성 품질 향상
3. **품질 검토**: CP_QUALITY_REVIEW에서 텍스트 정확성 우선 확인
4. **재생성 전략**: 텍스트 깨짐 시 더 나은 모델로 재생성 또는 Code-First 전환

---

## References

- [Gemini API Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [VS-Research Framework](../references/VS-Research-Framework.md)
- [Nelson & Narens (1990)](https://doi.org/10.1016/S0079-7421(08)60053-5)
- [Efklides (2008)](https://doi.org/10.1016/j.cedpsych.2006.12.001)
