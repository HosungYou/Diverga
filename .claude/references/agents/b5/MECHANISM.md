# B5-ParallelDocumentProcessor: 작동 메커니즘 상세 문서

## 개요

B5-ParallelDocumentProcessor는 **oh-my-claudecode의 executor 패턴**을 기반으로 대용량 PDF 컬렉션을 병렬로 처리하는 에이전트입니다. 단일 에이전트가 모든 문서를 순차적으로 처리하는 대신, **코디네이터-워커 아키텍처**를 사용하여 작업을 분산합니다.

---

## 핵심 문제: 왜 병렬 처리가 필요한가?

### 순차 처리의 한계

```
┌─────────────────────────────────────────────────────────────────┐
│                    순차 처리 (Sequential)                        │
│                                                                  │
│   PDF 1 → PDF 2 → PDF 3 → ... → PDF 100                         │
│   ════════════════════════════════════════►                      │
│                                                                  │
│   문제점:                                                        │
│   1. Context Window 누적: 각 PDF 내용이 컨텍스트에 쌓임           │
│   2. 메모리 오버플로우: 50+ PDFs 처리 시 context limit 도달       │
│   3. 단일 실패 = 전체 중단: 에러 발생 시 파이프라인 중단          │
│   4. 처리 시간: 100 PDFs × 30초 = 50분+                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 병렬 처리의 해결책

```
┌─────────────────────────────────────────────────────────────────┐
│                    병렬 처리 (Parallel)                          │
│                                                                  │
│   Worker 1: PDF 1-20   ════════►  Results 1                     │
│   Worker 2: PDF 21-40  ════════►  Results 2                     │
│   Worker 3: PDF 41-60  ════════►  Results 3    → Aggregation    │
│   Worker 4: PDF 61-80  ════════►  Results 4                     │
│   Worker 5: PDF 81-100 ════════►  Results 5                     │
│                                                                  │
│   장점:                                                          │
│   1. 격리된 컨텍스트: 각 워커가 독립적 context 사용               │
│   2. 메모리 안전: 워커당 20 PDFs만 처리                          │
│   3. 내결함성: 워커 1 실패해도 워커 2-5는 계속 진행               │
│   4. 처리 시간: 20 PDFs × 30초 = 10분 (5배 빠름)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 아키텍처: 코디네이터-워커 패턴

### 전체 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│                    ┌───────────────────┐                         │
│                    │   COORDINATOR     │                         │
│                    │   (Opus Model)    │                         │
│                    │                   │                         │
│                    │ • 작업 분할        │                         │
│                    │ • 워커 생성        │                         │
│                    │ • 진행 모니터링    │                         │
│                    │ • 결과 집계        │                         │
│                    └─────────┬─────────┘                         │
│                              │                                   │
│              ┌───────────────┼───────────────┐                   │
│              │               │               │                   │
│              ▼               ▼               ▼                   │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│    │  WORKER 1   │  │  WORKER 2   │  │  WORKER N   │             │
│    │  (Haiku)    │  │  (Haiku)    │  │  (Haiku)    │             │
│    │             │  │             │  │             │             │
│    │ PDF 1-20    │  │ PDF 21-40   │  │ PDF ...     │             │
│    │             │  │             │  │             │             │
│    └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│           │                │                │                    │
│           ▼                ▼                ▼                    │
│    ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│    │  Results 1  │  │  Results 2  │  │  Results N  │             │
│    └─────────────┘  └─────────────┘  └─────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 구성 요소 설명

#### 1. Coordinator (코디네이터)

| 속성 | 값 |
|------|-----|
| **모델** | Opus (복잡한 조정 작업) |
| **역할** | 전체 작업 오케스트레이션 |
| **상태 관리** | `.omc/state/b5-parallel-state.json` |

**책임:**
- PDF 디렉토리 스캔 및 파일 목록 생성
- 최적 배치 크기 및 워커 수 결정
- Task tool을 통한 워커 에이전트 생성
- 각 워커의 진행 상황 모니터링
- 실패한 작업 재시도 조정
- 최종 결과 집계 및 보고

#### 2. Workers (워커)

| 워커 타입 | 모델 | 배치 크기 | 사용 시나리오 |
|-----------|------|-----------|---------------|
| **Light** | Haiku | 20 PDFs | 메타데이터, 초록 추출 |
| **Standard** | Sonnet | 10 PDFs | 전체 텍스트, 테이블 |
| **Heavy** | Opus | 5 PDFs | 복잡한 분석 |

**책임:**
- 할당된 PDF 배치 처리
- 지정된 데이터 추출 (텍스트, 메타데이터, 테이블 등)
- 구조화된 결과 반환
- 에러 발생 시 로깅

---

## 실행 흐름: 단계별 메커니즘

### Phase 1: Discovery (발견)

```python
# 의사 코드 - 실제 구현은 Task tool 사용

def discovery_phase(pdf_directory):
    """
    PDF 디렉토리를 스캔하고 처리 계획 수립
    """
    # 1. 파일 목록 수집
    pdf_files = glob(f"{pdf_directory}/*.pdf")

    # 2. 파일 크기 분석
    file_stats = []
    for pdf in pdf_files:
        size = get_file_size(pdf)
        file_stats.append({
            "path": pdf,
            "size_mb": size,
            "category": categorize_by_size(size)  # small/medium/large
        })

    # 3. 처리 예상 시간 계산
    estimated_time = calculate_estimated_time(file_stats)

    # 4. 사용자 확인 (CHECKPOINT)
    return {
        "total_files": len(pdf_files),
        "total_size_mb": sum(f["size_mb"] for f in file_stats),
        "estimated_time": estimated_time,
        "size_distribution": count_by_category(file_stats)
    }
```

### Phase 2: Planning (계획)

```python
def planning_phase(discovery_result, extraction_task, max_workers=5):
    """
    최적 워커 배치 계획 수립
    """
    total_files = discovery_result["total_files"]

    # 1. 워커 수 결정 (파일 수 기반)
    optimal_workers = min(max_workers, ceil(total_files / 10))

    # 2. 배치 할당
    batch_size = ceil(total_files / optimal_workers)
    batches = []

    for i in range(optimal_workers):
        start_idx = i * batch_size
        end_idx = min((i + 1) * batch_size, total_files)
        batches.append({
            "worker_id": i + 1,
            "files": pdf_files[start_idx:end_idx],
            "model": select_model_for_task(extraction_task)
        })

    # 3. 워커 설정 생성
    worker_configs = []
    for batch in batches:
        worker_configs.append({
            "worker_id": batch["worker_id"],
            "model": batch["model"],
            "files": batch["files"],
            "extraction_task": extraction_task,
            "timeout_seconds": 120,
            "retry_attempts": 2
        })

    return worker_configs
```

### Phase 3: Parallel Execution (병렬 실행)

```python
def parallel_execution_phase(worker_configs):
    """
    Task tool을 사용하여 워커를 병렬로 실행

    핵심: 단일 메시지에서 여러 Task tool 호출 = 병렬 실행
    """

    # Claude Code에서 실제 구현:
    # 단일 응답에서 여러 Task tool을 호출하면 병렬 실행됨

    tasks = []
    for config in worker_configs:
        task = Task(
            subagent_type="oh-my-claudecode:executor-low",  # Haiku 워커
            model="haiku",
            description=f"PDF Worker {config['worker_id']}",
            prompt=f"""
            PDF 추출 작업 수행:

            파일 목록: {config['files']}
            추출 유형: {config['extraction_task']}

            각 파일에 대해:
            1. PDF 읽기 (Read tool 사용)
            2. 지정된 데이터 추출
            3. JSON 형식으로 결과 반환

            실패 시 에러 메시지 포함하여 계속 진행
            """,
            run_in_background=True  # 백그라운드 실행
        )
        tasks.append(task)

    # 모든 Task를 단일 메시지에서 호출 = 병렬 실행
    return tasks
```

### Phase 4: Aggregation (집계)

```python
def aggregation_phase(worker_results):
    """
    모든 워커 결과를 통합
    """
    aggregated = {
        "summary": {
            "total_files": 0,
            "successful": 0,
            "failed": 0,
            "processing_time": ""
        },
        "results": [],
        "failed_files": []
    }

    for result in worker_results:
        aggregated["summary"]["total_files"] += result["processed_count"]
        aggregated["summary"]["successful"] += result["success_count"]
        aggregated["summary"]["failed"] += result["fail_count"]

        aggregated["results"].extend(result["extractions"])
        aggregated["failed_files"].extend(result["failures"])

    # 실패한 파일 재시도
    if aggregated["failed_files"] and retry_enabled:
        retry_results = retry_failed_files(aggregated["failed_files"])
        merge_retry_results(aggregated, retry_results)

    return aggregated
```

### Phase 5: Validation (검증)

```python
def validation_phase(aggregated_results, original_file_count):
    """
    결과 완전성 검증
    """
    validation = {
        "completeness": {
            "expected": original_file_count,
            "processed": aggregated_results["summary"]["total_files"],
            "missing": []
        },
        "quality": {
            "empty_extractions": 0,
            "malformed_data": 0
        }
    }

    # 누락 파일 확인
    processed_files = set(r["file"] for r in aggregated_results["results"])
    for original in original_files:
        if original not in processed_files:
            validation["completeness"]["missing"].append(original)

    # 데이터 품질 검사
    for result in aggregated_results["results"]:
        if not result.get("extracted_data"):
            validation["quality"]["empty_extractions"] += 1

    return validation
```

---

## Task Tool 병렬 실행 메커니즘

### 핵심 원리

Claude Code의 Task tool은 **단일 응답에서 여러 번 호출되면 병렬로 실행**됩니다.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TASK TOOL 병렬 실행                           │
│                                                                  │
│   단일 Claude 응답:                                              │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  <function_calls>                                      │   │
│   │    <invoke name="Task">Worker 1</invoke>                    │   │
│   │    <invoke name="Task">Worker 2</invoke>  ← 동시 호출       │   │
│   │    <invoke name="Task">Worker 3</invoke>                    │   │
│   │  </function_calls>                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              Claude Code 런타임                          │   │
│   │                                                          │   │
│   │   Worker 1 ─────► [실행 중]                              │   │
│   │   Worker 2 ─────► [실행 중]   ← 동시에 실행됨            │   │
│   │   Worker 3 ─────► [실행 중]                              │   │
│   │                                                          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### oh-my-claudecode:executor 패턴 활용

B5 에이전트는 `oh-my-claudecode`의 executor 에이전트 패턴을 활용합니다:

```yaml
Agent Types Used:
  - oh-my-claudecode:executor-low   # Haiku - 간단한 추출
  - oh-my-claudecode:executor       # Sonnet - 표준 추출
  - oh-my-claudecode:executor-high  # Opus - 복잡한 분석

Key Features:
  - run_in_background: true         # 백그라운드 실행
  - model: "haiku" | "sonnet"       # 모델 명시적 지정
  - Parallel invocation             # 단일 메시지에서 다중 호출
```

---

## 상태 관리

### 상태 파일 구조

```json
// .omc/state/b5-parallel-state.json
{
  "session_id": "b5-2026-01-26-abc123",
  "status": "in_progress",
  "started_at": "2026-01-26T10:30:00Z",

  "discovery": {
    "total_files": 87,
    "total_size_mb": 342,
    "file_list": ["paper1.pdf", "paper2.pdf", ...]
  },

  "workers": [
    {
      "worker_id": 1,
      "status": "completed",
      "assigned_files": 18,
      "processed": 18,
      "failed": 0,
      "task_id": "task-abc-001"
    },
    {
      "worker_id": 2,
      "status": "in_progress",
      "assigned_files": 18,
      "processed": 12,
      "failed": 1,
      "task_id": "task-abc-002",
      "current_file": "thesis_2021.pdf"
    }
  ],

  "aggregation": {
    "status": "pending",
    "total_extracted": 0,
    "total_failed": 0
  },

  "checkpoints": {
    "CP-INIT-001": "approved",
    "CP-PROGRESS-001": "pending"
  }
}
```

### 진행 상황 모니터링

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROGRESS MONITORING                           │
│                                                                  │
│  Coordinator는 주기적으로 워커 상태를 확인:                       │
│                                                                  │
│  1. TaskOutput tool로 각 워커의 output_file 읽기                 │
│  2. 상태 파일 업데이트                                           │
│  3. 사용자에게 진행률 보고                                       │
│                                                                  │
│  Worker Progress:                                                │
│  [W1] ████████████████████ 100% ✓ (18/18)                       │
│  [W2] ████████████░░░░░░░░  60%   (11/18) - current: thesis.pdf  │
│  [W3] ████████████████░░░░  80%   (14/18)                        │
│  [W4] ████████░░░░░░░░░░░░  40%   (7/18)                         │
│  [W5] ████████████████████ 100% ✓ (18/18)                       │
│                                                                  │
│  Overall: 68/87 (78%) | ETA: 3 min | Errors: 1                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 에러 처리 메커니즘

### 에러 유형 및 복구 전략

| 에러 유형 | 감지 방법 | 복구 전략 |
|-----------|-----------|-----------|
| **Context Overflow** | 워커 크래시 | 배치 크기 축소, Light 워커로 재시도 |
| **Corrupted PDF** | 파싱 실패 | 건너뛰고 로깅, 수동 검토 대상 |
| **Timeout** | 60초 초과 | 확장된 타임아웃으로 재시도 |
| **Rate Limit** | API 429 | 동시성 감소, 딜레이 추가 |
| **Worker Crash** | Task 실패 | 해당 배치 격리 재시도 |

### 재시도 로직

```python
def retry_failed_files(failed_files, max_retries=2):
    """
    실패한 파일들을 격리하여 재시도
    """
    for attempt in range(max_retries):
        # 실패 파일만 별도 워커로 처리
        retry_worker = Task(
            subagent_type="oh-my-claudecode:executor",
            model="sonnet",  # 더 강력한 모델로 업그레이드
            description="Retry Worker",
            prompt=f"""
            이전에 실패한 PDF 파일 재처리:

            파일: {failed_files}
            시도: {attempt + 1}/{max_retries}

            각 파일에 대해:
            1. 더 긴 타임아웃 (120초)
            2. 에러 발생 시 상세 로깅
            3. 부분 추출이라도 반환
            """
        )

        results = execute_task(retry_worker)

        # 성공한 파일 제거
        failed_files = [f for f in failed_files
                       if f not in results["successful"]]

        if not failed_files:
            break

    return {
        "recovered": recovered_files,
        "still_failed": failed_files
    }
```

---

## 메모리 최적화 전략

### Context Window 관리

```
┌─────────────────────────────────────────────────────────────────┐
│                   CONTEXT WINDOW 관리                            │
│                                                                  │
│   문제: Claude의 context window는 제한적 (~200K tokens)          │
│                                                                  │
│   순차 처리 시:                                                  │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │ PDF1 + PDF2 + PDF3 + ... + PDF50 = OVERFLOW! ❌          │   │
│   └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│   병렬 처리 시 (각 워커 독립):                                   │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐                      │
│   │ Worker 1 │  │ Worker 2 │  │ Worker 3 │                      │
│   │ PDF1-10  │  │ PDF11-20 │  │ PDF21-30 │   각각 ✓             │
│   │ ~40K     │  │ ~40K     │  │ ~40K     │                      │
│   └──────────┘  └──────────┘  └──────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 대용량 파일 청킹

500+ 페이지 PDF의 경우:

```python
def chunk_large_pdf(pdf_path, chunk_size=50):
    """
    대용량 PDF를 페이지 기반으로 분할
    """
    total_pages = get_pdf_page_count(pdf_path)

    chunks = []
    for start_page in range(0, total_pages, chunk_size):
        end_page = min(start_page + chunk_size, total_pages)
        chunks.append({
            "pdf_path": pdf_path,
            "start_page": start_page,
            "end_page": end_page,
            "chunk_id": f"{start_page}-{end_page}"
        })

    return chunks

# 사용 예시:
# 500페이지 PDF → 10개 청크 (각 50페이지)
# 각 청크를 별도 워커가 처리
# 결과를 순서대로 재조립
```

---

## 다른 에이전트와의 연동

### 업스트림 연동 (데이터 제공)

```yaml
B1-SystematicLiteratureScout → B5-ParallelDocumentProcessor:
  flow:
    1. B1이 검색 결과에서 PDF URL 목록 생성
    2. PDF 다운로드 완료 후 디렉토리 경로 전달
    3. B5가 병렬 추출 시작

Manual Upload → B5:
  flow:
    1. 사용자가 PDF 디렉토리 경로 제공
    2. B5가 직접 처리 시작
```

### 다운스트림 연동 (데이터 소비)

```yaml
B5 → B2-EvidenceQualityAppraiser:
  output: 추출된 전체 텍스트
  purpose: 연구 품질 평가

B5 → B3-EffectSizeExtractor:
  output: 추출된 통계 섹션, 테이블
  purpose: 효과크기 계산

B5 → E1-QuantitativeAnalysisGuide:
  output: CSV/JSON 형식의 집계 데이터
  purpose: 통계 분석
```

---

## 사용 예시

### 예시 1: 체계적 문헌고찰 PDF 추출

```
사용자: "내 SR 폴더에 있는 87개 PDF에서 전체 텍스트 추출해줘"

B5 코디네이터:
1. Discovery: 87 PDFs, 342 MB 확인
2. Planning: 5 워커, 배치당 18 PDFs
3. Execution: 5개 Task tool 병렬 호출
4. Aggregation: 결과 통합
5. Validation: 완전성 검증

출력:
{
  "summary": {
    "total_files": 87,
    "successful": 84,
    "failed": 3
  },
  "results": [...],
  "failed_files": [
    {"file": "corrupted.pdf", "reason": "Parse error"},
    {"file": "scanned.pdf", "reason": "OCR required"},
    {"file": "locked.pdf", "reason": "Password protected"}
  ]
}
```

### 예시 2: 타겟 데이터 추출

```
사용자: "메타분석 논문들에서 표본크기와 효과크기만 추출해줘"

B5 설정:
{
  "extraction_task": "specific_sections",
  "specific_fields": ["sample_size", "effect_size", "CI"],
  "output_format": "csv"
}

출력 (CSV):
file,sample_size,effect_size,effect_type,ci_lower,ci_upper
smith_2021.pdf,1234,0.45,Cohen's d,0.32,0.58
wang_2022.pdf,567,0.62,Hedge's g,0.48,0.76
```

---

## 성능 벤치마크

| 컬렉션 크기 | 순차 처리 | 병렬 처리 (5 워커) | 속도 향상 |
|-------------|-----------|-------------------|-----------|
| 10 PDFs | 5분 | 1.5분 | 3.3x |
| 50 PDFs | 25분 | 6분 | 4.2x |
| 100 PDFs | 50분 | 12분 | 4.2x |
| 200 PDFs | 100분 | 25분 | 4.0x |

---

## 참고 자료

### 내부 참조
- [oh-my-claudecode 문서](~/.claude/CLAUDE.md) - Task tool 병렬 실행
- [SKILL.md](./SKILL.md) - 에이전트 정의
- [workflow-parallel-pdf.md](./workflow-parallel-pdf.md) - 워크플로우 상세

### 관련 기술
- Claude Code Task tool
- run_in_background 옵션
- oh-my-claudecode:executor 에이전트 패턴