# Diverga QA Reports

QA test reports and session transcripts for Diverga plugin validation.

---

## Directory Structure

```
reports/
├── sessions/                    # Individual test sessions (NEW in v2.0)
│   ├── META-002/               # Advanced Meta-Analysis test
│   │   ├── README.md           # Session overview
│   │   ├── conversation_transcript.md   # Human-readable transcript
│   │   ├── conversation_raw.json        # Raw conversation data
│   │   ├── META-002_test_result.yaml    # Test evaluation
│   │   └── META-002_report.html         # Visual HTML report
│   ├── QUAL-002/               # (Future) Qualitative test
│   └── MIXED-002/              # (Future) Mixed methods test
│
├── real-transcripts/           # Legacy location (deprecated)
├── SIMULATION_TRANSCRIPTS.md   # v1.0 mock transcripts (archived)
└── *.yaml                      # Legacy v1.0 reports
```

---

## Session-Based Organization (v2.0)

Each test session is now organized in its own folder containing:

| File | Purpose | Format |
|------|---------|--------|
| `README.md` | Session overview and metrics | Markdown |
| `conversation_transcript.md` | Full conversation, human-readable | Markdown |
| `conversation_raw.json` | Complete conversation data | JSON |
| `*_test_result.yaml` | Test evaluation results | YAML |
| `*_report.html` | Visual report | HTML |

**Note**: Original JSONL session logs are excluded from Git due to size (~8MB each).

---

## Available Sessions

| Session | Scenario | Status | Date |
|---------|----------|--------|------|
| [META-002](sessions/META-002/) | Advanced Meta-Analysis with Technical Challenges | ✅ PASSED | 2026-01-29 |

---

## How to Add a New Session

1. Run the test in Claude Code
2. Extract the conversation:
   ```bash
   python qa/runners/extract_conversation.py \
     --session ~/.claude/projects/{project-id}/{session-id}.jsonl \
     --output qa/reports/sessions/{SCENARIO-ID}/
   ```
3. Evaluate against expected scenario:
   ```bash
   python qa/run_tests.py \
     --evaluate-extracted \
     --input qa/reports/sessions/{SCENARIO-ID}/*.yaml \
     --expected qa/protocol/test_{scenario}.yaml
   ```
4. Commit and push

---

## Legacy Reports (v1.0)

The following files are from QA Protocol v1.0 (mock-based testing):
- `META-001_*.yaml`, `QUAL-001_*.yaml`, etc.
- `SIMULATION_TRANSCRIPTS.md`

These are kept for reference but are superseded by v2.0 real conversation tests.
