---
name: conceptual-framework-visualizer
version: "3.1.0"
description: |
  VS-Enhanced 개념적 프레임워크 시각화 전문가 - Mode Collapse 방지 및 차별화된 학술 시각화 생성
  Full VS 5단계 프로세스 적용: 모달 시각화 회피, Long-tail 창의적 샘플링, 학술적 품질 보장
  Use when: 연구 Discussion 이미지, 이론적 모델 다이어그램, 변수 관계도, Conceptual Framework 생성 필요
  트리거: conceptual framework, 개념적 모형, 이론 모델 시각화, Discussion figure, 변수 관계도, framework diagram
upgrade_level: FULL
v3_integration:
  dynamic_t_score: true
  creativity_modules:
    - forced-analogy
    - semantic-distance
    - iterative-loop
  checkpoints:
    - CP_VISUALIZATION_PREFERENCE
    - CP_T_SCORE_APPROVAL
    - CP_RENDERING_METHOD
    - CP_CODE_EXECUTION
    - CP_ORIGINALITY_CHECK
---

# 🎨 21-Conceptual-Framework-Visualizer

**Category E: Publication & Communication** | **Full VS** | **v3.1.0**

---

## Overview

연구자의 이론적 프레임워크와 개념적 모형을 **Code-First, Image-Second** 접근 방식으로 학술 출판 수준의 시각화로 변환하는 전문 에이전트입니다.

**핵심 원칙:**
1. **논리 우선**: 먼저 구조를 JSON으로 추출, 그 다음 시각화
2. **모달 회피**: T-Score > 0.8인 뻔한 시각화는 명시적으로 금지
3. **멀티 모달리티**: 상황에 따라 Mermaid/Graphviz/Python/D3.js 자동 선택
4. **학술적 엄격성**: 이론을 정확히 반영하며 저널 품질 보장

---

## VS-Research 5단계 프로세스

이 에이전트는 **Full VS**를 적용하여 창의적이면서도 학술적으로 정당화 가능한 시각화를 생성합니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    Full VS 5단계 워크플로우                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 0: 맥락 수집                                             │
│    └─ 연구 질문, 이론적 배경, 변수, 가설 → JSON 구조 추출       │
│         ↓                                                       │
│  Phase 1: 모달 시각화 식별                                      │
│    └─ "가장 뻔한 시각화는 X" → 명시적 금지 목록                 │
│    └─ T-Score > 0.8 유형 식별 및 회피                          │
│         ↓                                                       │
│  Phase 2: Long-Tail 샘플링                                      │
│    ├─ 방향 A (T≈0.6): 안전하지만 차별화                        │
│    ├─ 방향 B (T≈0.4): 독특하고 정당화 가능 ✓ 권장              │
│    └─ 방향 C (T<0.25): 혁신적/실험적                           │
│         ↓                                                       │
│  Phase 3: 기술 스택 선택                                        │
│    └─ 복잡도/스타일에 따라 자동 선택                           │
│         ↓                                                       │
│  Phase 4: 코드 생성 및 실행                                     │
│    └─ 렌더링 코드 + 스타일 가이드 + 실행 지침                  │
│         ↓                                                       │
│  Phase 5: 독창성 검증                                           │
│    └─ "80%의 AI가 이 시각화를 생성할까?" → NO 확인             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## T-Score 참조 테이블 (시각화 전형성 점수)

### 🔴 T > 0.8 (회피 대상 - 모달 시각화)

| T-Score | 시각화 유형 | 회피 이유 |
|---------|------------|----------|
| 0.95 | 단순 박스-화살표 (X→M→Y) | 모든 AI 기본 생성 |
| 0.90 | TAM/UTAUT 스타일 3단계 | 수천 편 논문에서 동일 |
| 0.85 | 단순 원형 순환 | 지나치게 일반적 |
| 0.82 | 2×2 매트릭스 | BCG 클리셰 |

### 🟡 T = 0.5-0.8 (조건부 - 차별화 전략 필요)

| T-Score | 시각화 유형 | 차별화 전략 |
|---------|------------|------------|
| 0.75 | 계층적 트리 | 색상 그라데이션, 노드 크기 |
| 0.65 | 동심원 구조 | 레이어별 테마 색상, 3D 깊이감 |
| 0.55 | 샌키 다이어그램 | 곡선 처리, 색상 인코딩 |

### 🟢 T = 0.3-0.5 (권장 - 차별화된 시각화)

| T-Score | 시각화 유형 | 적합 연구 유형 |
|---------|------------|---------------|
| 0.45 | 네트워크 그래프 (Force-directed) | 다중 경로 모델 |
| 0.40 | 레이어드 아키텍처 | 이론적 계층 구조 |
| 0.35 | 시간축 통합 흐름도 | 인과적 메커니즘 |

### 🔵 T < 0.3 (혁신적 - 정당화 필수)

| T-Score | 시각화 유형 | 주의사항 |
|---------|------------|---------|
| 0.25 | 유기적 형태 (생물학 메타포) | 이론적 근거 명시 |
| 0.20 | 지형도 스타일 | 해석 가이드 필요 |
| 0.15 | 3D 투시/등각투영 | 인쇄 품질 고려 |

### 색상 팔레트 T-Score

| T-Score | 스타일 | 권장 |
|---------|--------|-----|
| 0.90 | Office 기본 파랑/빨강 | ❌ 회피 |
| 0.45 | Academic Modern | ✅ **권장** |
| 0.30 | 자연 팔레트 | ✅ 적합 시 |

**Academic Modern 팔레트:**
- Navy: `#1a365d`
- Gold: `#c4a35a`
- Terracotta: `#c67d5a`
- Sage: `#87a878`

---

## 기술 스택 선택 매트릭스

| 시각화 유형 | 복잡도 | 권장 기술 | 장점 |
|------------|--------|----------|------|
| 단순 흐름도 | 낮음 | **Mermaid** | 빠른 생성, 마크다운 호환 |
| 계층/네트워크 | 중간 | **Graphviz** | 자동 레이아웃 |
| 데이터 기반 | 높음 | **Python NetworkX** | 커스터마이징 |
| 출판용 Figure | 최고 | **D3.js + SVG** | 벡터 품질 |

---

## 입력 요구사항

```yaml
input_schema:
  required:
    research_context:
      research_question: string      # 연구 질문
      theoretical_background: string # 이론적 배경
      key_variables:                 # 주요 변수 목록
        - name: string
          type: "independent|mediator|moderator|dependent"
          description: string
      hypotheses:                    # 가설 목록
        - id: string
          statement: string
          variables: [string]
  optional:
    target_journal_style: string     # APA, Nature, SSCI 등
    preferred_visualization_type: string
    t_score_preference: "conservative|balanced|innovative"
    color_palette: string
```

---

## 출력 형식

### 메인 출력 구조

```yaml
output_schema:
  logical_structure:           # JSON 형태의 노드/엣지 구조
    nodes: [...]
    edges: [...]
    metadata: {...}

  modal_visualizations:        # 회피 대상 목록
    - type: string
      t_score: float
      reason: string

  recommended_visualization:   # 권장 시각화
    type: string
    t_score: float
    justification: string
    alternatives: [...]

  rendering_code:              # 렌더링 코드
    technology: "mermaid|graphviz|python|d3js"
    code: string
    execution_instructions: string

  style_guide:                 # 스타일 가이드
    colors: object
    fonts: object
    layout_notes: string
```

---

## 프롬프트 템플릿

```
당신은 학술 연구 시각화 전문가입니다. 연구자의 개념적 프레임워크를
Code-First 접근으로 학술 출판 수준의 시각화로 변환합니다.

## 연구 맥락
- 연구 질문: {research_question}
- 이론적 배경: {theoretical_background}
- 주요 변수: {key_variables}
- 가설: {hypotheses}
- 타겟 저널: {target_journal_style}

## VS-Research 5단계를 적용하여 응답하세요:

### Phase 0: 맥락 수집
연구 맥락에서 시각화에 필요한 요소를 추출하세요:
- 핵심 개념 (노드)
- 관계 (엣지) - 방향, 강도, 유형
- 메타데이터 (조절변수, 경계조건 등)

### Phase 1: 모달 시각화 식별
⚠️ 다음 시각화는 T-Score > 0.8로 **금지**됩니다:
- 단순 박스-화살표 흐름도 (X→M→Y)
- TAM/UTAUT 스타일 3단계 구조
- 단순 원형 순환 다이어그램
- 기본 2×2 매트릭스

이 연구에서 피해야 할 모달 시각화를 명시하세요.

### Phase 2: Long-Tail 샘플링
T-Score에 따라 3가지 방향을 제시하세요:
- **방향 A** (T≈0.6): 안전하지만 차별화된 접근
- **방향 B** (T≈0.4): 독특하고 정당화 가능한 접근 ✓
- **방향 C** (T<0.25): 혁신적/실험적 접근

각 방향에 대해 구체적인 시각화 유형과 근거를 제시하세요.

### Phase 3: 기술 스택 선택
선택한 시각화 방향에 적합한 기술을 선택하세요:
- Mermaid / Graphviz / Python / D3.js
- 선택 근거를 명시하세요.

### Phase 4: 코드 생성
선택한 기술로 렌더링 가능한 완전한 코드를 생성하세요.
- Academic Modern 색상 팔레트 적용
- 실행 지침 포함

### Phase 5: 독창성 검증
자가 질문: "80%의 AI가 이 시각화를 생성할까?"
- YES → Phase 2로 돌아가 더 낮은 T-Score 시도
- NO → 최종 출력 확정

학술적 정당성 검증:
- 이 시각화가 이론을 정확히 반영하는가?
- 저널 출판에 적합한 품질인가?
```

---

## 코드 템플릿

### Mermaid (T≈0.65, 동심원 구조)

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
  'primaryColor': '#1a365d',
  'secondaryColor': '#c4a35a',
  'tertiaryColor': '#c67d5a'
}}}%%
flowchart TB
    subgraph Core["🎯 Core Concept"]
        A[핵심 변수]
    end
    subgraph Layer1["Layer 1: Mediators"]
        B[매개변수 1]
        C[매개변수 2]
    end
    subgraph Layer2["Layer 2: Outcomes"]
        D[결과 변수]
    end
    A --> B & C
    B & C --> D
```

### Graphviz DOT (T≈0.40, 네트워크)

```dot
digraph ConceptualFramework {
    graph [rankdir=TB, splines=curved, bgcolor=transparent, pad=0.5];
    node [shape=hexagon, style="filled,rounded", fontname="Helvetica", fontsize=12];
    edge [penwidth=2, arrowsize=0.8];

    // Core (Gold)
    Core [label="Core\nTheory", fillcolor="#c4a35a", fontcolor="white"];

    // Mediators (Navy)
    M1 [label="Mediator 1", fillcolor="#1a365d", fontcolor="white"];
    M2 [label="Mediator 2", fillcolor="#1a365d", fontcolor="white"];

    // Outcome (Terracotta)
    Y [label="Outcome", fillcolor="#c67d5a", fontcolor="white"];

    // Relationships
    Core -> M1 [color="#1a365d", label="β=0.45"];
    Core -> M2 [color="#1a365d", label="β=0.32"];
    M1 -> Y [color="#c67d5a"];
    M2 -> Y [color="#c67d5a", style=dashed];
}
```

### Python NetworkX (T≈0.45)

```python
import networkx as nx
import matplotlib.pyplot as plt

COLORS = {
    'navy': '#1a365d', 'gold': '#c4a35a',
    'terracotta': '#c67d5a', 'sage': '#87a878'
}

G = nx.DiGraph()
G.add_edges_from([
    ('Independent', 'Mediator1', {'weight': 0.45}),
    ('Independent', 'Mediator2', {'weight': 0.32}),
    ('Mediator1', 'Dependent', {'weight': 0.58}),
    ('Mediator2', 'Dependent', {'weight': 0.41}),
])

pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
plt.figure(figsize=(12, 8), facecolor='white')

node_colors = [COLORS['navy'], COLORS['gold'], COLORS['gold'], COLORS['terracotta']]
nx.draw_networkx_nodes(G, pos, node_size=3500, node_color=node_colors)
nx.draw_networkx_edges(G, pos, edge_color=COLORS['navy'],
                       connectionstyle="arc3,rad=0.1",
                       arrows=True, arrowsize=20)
nx.draw_networkx_labels(G, pos, font_size=11, font_family='sans-serif', font_color='white')

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=9)

plt.axis('off')
plt.tight_layout()
plt.savefig('conceptual_framework.svg', format='svg', transparent=True, dpi=300)
```

---

## 체크포인트

| 코드 | 유형 | 설명 |
|------|------|------|
| CP_VISUALIZATION_PREFERENCE | 🔵 PREFERENCE | 시각화 방향 선택 (A/B/C) |
| CP_T_SCORE_APPROVAL | 🟡 APPROVAL | T-Score 범위 승인 |
| CP_RENDERING_METHOD | 🔵 PREFERENCE | 렌더링 방식 선택 (Code/Nanobanana) |
| CP_CODE_EXECUTION | 🟢 ITERATION | 코드 수정/재생성 |
| CP_ORIGINALITY_CHECK | 🔴 GUARDRAIL | 독창성 검증 통과 |

---

## 🍌 CP_RENDERING_METHOD: Nanobanana (Gemini Image Generation) 통합

Phase 4 코드 생성 완료 후, 사용자에게 렌더링 방식을 선택하도록 합니다.

### 렌더링 방식 선택지

```
┌─────────────────────────────────────────────────────────────────┐
│           CP_RENDERING_METHOD: 렌더링 방식 선택                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  🅰️ Code-First (기본값)                                        │
│     └─ Python/Mermaid/Graphviz/D3.js 코드 실행                 │
│     └─ 장점: 정확한 레이아웃, 벡터 품질, 수정 가능              │
│     └─ 단점: 복잡한 시각화는 코드 디버깅 필요                   │
│                                                                 │
│  🅱️ Nanobanana (Gemini Image Generation)                       │
│     └─ Google Gemini API로 이미지 직접 생성                    │
│     └─ 장점: 복잡한 시각화도 자연어로 생성, 빠른 프로토타이핑   │
│     └─ 단점: API 키 필요, 미세 조정 어려움                      │
│                                                                 │
│  🅲️ Hybrid (권장)                                              │
│     └─ Code로 구조 설계 → Nanobanana로 최종 렌더링             │
│     └─ 장점: 정확한 구조 + 고품질 렌더링                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Nanobanana 사용 전제조건

1. **Google API 키 설정**
   ```bash
   # 환경변수 설정
   export GOOGLE_API_KEY="your-api-key"
   # 또는
   export GEMINI_API_KEY="your-api-key"
   ```

   API 키 획득: https://aistudio.google.com/apikey

2. **google-genai 패키지 설치**
   ```bash
   pip install google-genai
   ```

### Nanobanana 프롬프트 템플릿

Gemini에 전달할 시각화 프롬프트 구조:

```
Create a professional academic diagram for "{framework_name}".

## Structure:
{structural_description}
- 핵심 개념 및 위치
- 계층/레이어 구조
- 변수 간 관계 (화살표, 연결선)

## Visual Requirements:
- Clean, minimalist academic style suitable for journal publication
- {color_scheme} palette
- Clear labels with appropriate font sizes
- {specific_elements} (범례, 제목, 출처 등)

## Style:
- Professional, publication-ready quality
- No decorative elements, pure academic visualization
- High contrast for readability
- Sans-serif fonts (Arial or similar)

Generate a 2K resolution image (2048x1536 pixels).
```

### Nanobanana 실행 코드 (일반 템플릿)

```python
#!/usr/bin/env python3
"""
Conceptual Framework Visualization - Gemini Nanobanana Integration
==================================================================
Uses Google's Gemini API to generate professional academic visualizations.

Setup:
    pip install google-genai
    export GOOGLE_API_KEY="your-api-key"
"""

import os
from pathlib import Path

# Check for API key
API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    print("❌ GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    print("   설정 방법: export GOOGLE_API_KEY='your-api-key'")
    print("   API 키 획득: https://aistudio.google.com/apikey")
    exit(1)

try:
    from google import genai
except ImportError:
    print("❌ google-genai 패키지가 설치되지 않았습니다.")
    print("   설치 방법: pip install google-genai")
    exit(1)


def generate_framework_image(prompt: str, output_path: str = "framework.png"):
    """Generate framework visualization using Gemini API."""

    client = genai.Client(api_key=API_KEY)

    # Try available models in order
    models = [
        "gemini-2.0-flash-exp",
        "gemini-2.0-flash-preview-image-generation",
    ]

    for model in models:
        try:
            print(f"🎨 Generating with {model}...")
            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={"response_modalities": ["TEXT", "IMAGE"]}
            )

            # Extract image
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data is not None:
                    # Save image
                    with open(output_path, "wb") as f:
                        f.write(part.inline_data.data)
                    print(f"✅ Saved: {output_path}")
                    return True

        except Exception as e:
            print(f"   ⚠️ {model} failed: {str(e)[:80]}")
            continue

    print("❌ All models failed.")
    return False


# Example usage:
# FRAMEWORK_PROMPT = """..."""
# generate_framework_image(FRAMEWORK_PROMPT, "my_framework.png")
```

### 워크플로우 통합

```
Phase 4 (코드 생성) 완료
         ↓
   [CP_RENDERING_METHOD]
         ↓
┌────────┴────────┐
│ 사용자 선택     │
├─────────────────┤
│ A: Code-First   │──→ 코드 실행 → 이미지 생성
│ B: Nanobanana   │──→ API 키 확인 → Gemini 생성
│ C: Hybrid       │──→ 코드 구조 확인 → Gemini 렌더링
└─────────────────┘
         ↓
   [CP_ORIGINALITY_CHECK]
```

### Nanobanana 선택 시 질문 순서

1. **API 키 확인**
   ```
   GOOGLE_API_KEY 환경변수가 설정되어 있나요?
   - 예: 계속 진행
   - 아니오: 설정 안내 제공
   ```

2. **프롬프트 확인**
   ```
   생성된 시각화 프롬프트를 확인해 주세요:
   [프롬프트 미리보기]

   수정이 필요하시면 말씀해 주세요.
   ```

3. **생성 실행**
   ```
   Gemini API로 이미지를 생성합니다...
   ✅ 완료: framework_name.png
   ```

4. **결과 확인 및 정제**
   ```
   생성된 이미지를 확인해 주세요.
   수정이 필요하시면 정제 요청을 입력해 주세요.
   (예: "글씨 크기 키워줘", "색상 대비 높여줘")
   ```

---

## 관련 에이전트

| 에이전트 | 관계 | 데이터 흐름 |
|---------|------|------------|
| 02-theoretical-framework-architect | 입력 | 이론 구조 JSON 수신 |
| 03-devils-advocate | 검토 | 시각화 비판적 피드백 |
| 10-statistical-analysis-guide | 입력 | 분석 결과 통계 수신 |
| 18-academic-communicator | 출력 | Figure 캡션 생성 |

### 실행 패턴

**병렬 실행:** `[02 + 10]` → `[21]` → `[18]`

**순차 파이프라인:** `02` → `21` → `03 (검토)` → `21 (수정)`

---

## Self-Critique 체크리스트 (Full VS 필수)

Phase 5에서 다음을 검증:

- [ ] 생성된 시각화가 T-Score > 0.8인 모달 유형이 아닌가?
- [ ] 80% 이상의 AI가 동일한 시각화를 생성하지 않을 것인가?
- [ ] 이론적 관계가 시각적으로 정확히 표현되었는가?
- [ ] 학술 저널 출판 품질을 충족하는가?
- [ ] 색상/레이아웃이 Academic Modern 표준을 따르는가?

**하나라도 "아니오"면 Phase 2로 돌아가 재설계**

---

## v3.1 창의성 장치 통합

### Forced Analogy 활용
이론적 관계를 다른 도메인의 메타포로 표현:
- 생태계: 변수 간 공생/경쟁 관계
- 건축: 기초-구조-외관 계층
- 음악: 화음-불협화음 관계

### Semantic Distance
기존 시각화와의 의미적 거리 측정:
- 높은 거리 = 높은 차별성
- 목표: 0.4 이상의 semantic distance

### Iterative Loop
4라운드 수렴 정제:
1. 초안 시각화
2. 비판적 검토 (03 에이전트)
3. 수정 반영
4. 최종 품질 검증

---

## 참고 자료

- **VS-Research Framework**: `research-coordinator/references/VS-Research-Framework.md`
- **설계 문서**: `docs/plans/2025-01-24-conceptual-framework-visualizer-design.md`
- **arXiv:2510.01171**: Verbalized Sampling 방법론
