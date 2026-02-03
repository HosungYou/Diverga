# B5-ParallelDocumentProcessor 한국어 가이드

## 개요

B5-ParallelDocumentProcessor는 **대용량 PDF 컬렉션**을 효율적으로 처리하기 위한 병렬 처리 에이전트입니다.

### 왜 필요한가?

기존 방식 (순차 처리):
```
PDF 1 읽기 → PDF 2 읽기 → PDF 3 읽기 → ... → 메모리 오버플로우! ❌
```

새로운 방식 (병렬 처리):
```
Worker 1: PDF 1-20  ─┐
Worker 2: PDF 21-40 ─┼─→ 결과 통합 → 완료! ✓
Worker 3: PDF 41-60 ─┘
```

---

## 핵심 메커니즘

### 1. 코디네이터-워커 아키텍처

```
                  ┌─────────────┐
                  │ COORDINATOR │  (Opus - 전체 조정)
                  │   코디네이터  │
                  └──────┬──────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Worker1 │    │ Worker2 │    │ Worker3 │
    │ (Haiku) │    │ (Haiku) │    │ (Haiku) │
    │ PDF1-20 │    │ PDF21-40│    │ PDF41-60│
    └────┬────┘    └────┬────┘    └────┬────┘
         │              │              │
         └──────────────┼──────────────┘
                        ▼
                   결과 통합
```

### 2. Task Tool 병렬 실행

Claude Code에서 **단일 메시지에 여러 Task tool을 호출**하면 병렬로 실행됩니다:

```xml
<function_calls>
  <invoke name="Task">Worker 1 실행</invoke>
  <invoke name="Task">Worker 2 실행</invoke>  ← 동시에 실행됨!
  <invoke name="Task">Worker 3 실행</invoke>
</function_calls>
```

### 3. oh-my-claudecode:executor 활용

```yaml
사용하는 에이전트:
  - oh-my-claudecode:executor-low   # Haiku (빠르고 저렴)
  - oh-my-claudecode:executor       # Sonnet (표준)
  - oh-my-claudecode:executor-high  # Opus (복잡한 작업)

핵심 옵션:
  - run_in_background: true  # 백그라운드 실행
  - model: "haiku"           # 모델 지정
```

---

## 처리 단계

| 단계 | 설명 | 체크포인트 |
|------|------|-----------|
| **1. Discovery** | PDF 디렉토리 스캔, 파일 목록 수집 | 🔴 파일 수 확인 |
| **2. Planning** | 워커 수 결정, 배치 할당 | - |
| **3. Execution** | 워커 병렬 실행, 데이터 추출 | 🟠 50% 진행 확인 |
| **4. Aggregation** | 결과 통합, 실패 파일 재시도 | - |
| **5. Validation** | 완전성 검증, 최종 보고 | 🟡 결과 검토 |

---

## 워커 유형

| 워커 | 모델 | 배치 크기 | 용도 |
|------|------|-----------|------|
| **Light** | Haiku | 20개 | 메타데이터, 초록 |
| **Standard** | Sonnet | 10개 | 전체 텍스트, 테이블 |
| **Heavy** | Opus | 5개 | 복잡한 분석 |

---

## 사용 예시

### 예시 1: 체계적 문헌고찰
```
"내 SR 폴더에 있는 87개 PDF 처리해줘"

결과:
- 총 파일: 87
- 성공: 84
- 실패: 3 (손상, OCR 필요, 암호화)
- 처리 시간: 12분 (순차 처리 대비 4배 빠름)
```

### 예시 2: 타겟 추출
```
"메타분석 논문들에서 표본크기와 효과크기만 추출해줘"

출력 (CSV):
file,sample_size,effect_size
smith_2021.pdf,1234,0.45
wang_2022.pdf,567,0.62
```

### 예시 3: 대용량 파일
```
"500페이지 박사논문 처리해줘"

전략:
1. 50페이지씩 10개 청크로 분할
2. 각 청크를 별도 워커가 처리
3. 순서대로 재조립
```

---

## 에러 처리

| 에러 | 복구 전략 |
|------|-----------|
| 메모리 오버플로우 | 배치 크기 축소, Light 워커로 재시도 |
| 손상된 PDF | 건너뛰고 로깅 |
| 타임아웃 | 확장된 타임아웃으로 재시도 |
| OCR 필요 | 별도 OCR 전처리 필요 플래그 |

---

## 트리거 키워드

| 한국어 | 영어 |
|--------|------|
| "병렬 처리해줘" | "parallel processing" |
| "대용량 PDF" | "large PDF" |
| "여러 PDF 처리" | "batch PDF" |
| "PDF 일괄 추출" | "bulk extraction" |

---

## 연동 에이전트

```
B1-SystematicLiteratureScout  (검색)
         ↓
B5-ParallelDocumentProcessor  (추출) ← 현재 에이전트
         ↓
    ┌────┴────┐
    ↓         ↓
B2-Evidence  B3-EffectSize
 (품질평가)    (효과크기)
```

---

## 성능 비교

| PDF 수 | 순차 처리 | 병렬 처리 | 속도 향상 |
|--------|-----------|-----------|-----------|
| 10개 | 5분 | 1.5분 | **3.3배** |
| 50개 | 25분 | 6분 | **4.2배** |
| 100개 | 50분 | 12분 | **4.2배** |

---

## 관련 문서

- [SKILL.md](./SKILL.md) - 에이전트 정의
- [MECHANISM.md](./MECHANISM.md) - 상세 메커니즘 (영문)
- [workflow-parallel-pdf.md](./workflow-parallel-pdf.md) - 워크플로우
