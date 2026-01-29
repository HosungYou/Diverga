# Diverga QA Protocol v2.1

Real Conversation Testing for Diverga Research Methodology Plugin

**v2.1 New**: Session-based folder management + RAW conversation extraction

## Overview

This QA protocol validates Diverga plugin functionality through **real Claude Code conversations**, not mock simulations. It tests:

- **Checkpoint System** - Mandatory HALT at critical decision points
- **Agent Invocation** - Correct agent triggering and execution
- **VS Methodology** - T-Score based alternative presentation
- **Complex User Interactions** - Technical questions, methodological challenges, agent transitions
- **Language Consistency** - Response matches input language (English/Korean)

## Quick Start

### 1. Run a Test Scenario

```bash
# Start Claude Code in the Diverga project
cd /Volumes/External\ SSD/Projects/Diverga
claude

# Invoke the research coordinator skill
/diverga:research-coordinator

# Or start with a natural language prompt from the scenario
```

### 2. Follow Test Script

Use the conversation flows defined in `qa/protocol/test_*.yaml`:

| Scenario | File | Focus |
|----------|------|-------|
| META-002 | `test_meta_002.yaml` | Advanced meta-analysis with technical challenges |
| QUAL-002 | `test_qual_002.yaml` | Phenomenology with paradigm debates (Korean) |
| MIXED-002 | `test_mixed_002.yaml` | Mixed methods integration challenges |
| HUMAN-002 | `test_human_002.yaml` | Academic humanization with ethics |

### 3. Extract and Evaluate

```bash
# Extract conversation from Claude Code session log
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/{project-id}/{session}.jsonl \
  --output qa/reports/real-transcripts/

# Evaluate against expected scenario
python qa/run_tests.py \
  --evaluate-extracted \
  --input qa/reports/real-transcripts/META-002.yaml \
  --expected qa/protocol/test_meta_002.yaml
```

## Directory Structure (v2.1)

```
qa/
├── README.md                    # This file
├── run_tests.py                 # Test runner and evaluator
├── .gitignore                   # Excludes large JSONL files
├── docs/
│   ├── QA_PROTOCOL_v2.md        # Full protocol documentation
│   ├── CHECKPOINT_SPEC.md       # Checkpoint system spec
│   └── AGENT_TRIGGER_SPEC.md    # 40 agent trigger map
├── runners/
│   ├── __init__.py
│   └── extract_conversation.py  # Session log extractor
├── protocol/
│   ├── test_meta_002.yaml       # Advanced meta-analysis scenario
│   ├── test_qual_002.yaml       # Advanced qualitative (Korean)
│   ├── test_mixed_002.yaml      # Advanced mixed methods
│   └── test_human_002.yaml      # Academic humanization
└── reports/
    ├── README.md                # Reports guide
    ├── sessions/                # [v2.1] Session-based folders
    │   └── META-002/            # Complete test session
    │       ├── README.md
    │       ├── conversation_transcript.md  # Human-readable
    │       ├── conversation_raw.json       # RAW data
    │       ├── META-002_test_result.yaml
    │       └── META-002_report.html
    └── (legacy files...)        # v1.0 outputs
```

## Test Scenarios

### META-002: Advanced Meta-Analysis

**Complexity:** HIGH (10-15 turns)
**Language:** English
**Agents:** C5, C6, C7, B1, B3, E1, E5, A2

Tests:
- Effect size methodology questions (Hedges' g vs Cohen's d)
- Sample size concerns for random-effects models
- Agent transition to theoretical framework
- Gray literature inclusion decisions
- Bayesian meta-analysis alternatives
- Subgroup analysis feasibility

### QUAL-002: Advanced Phenomenology (Korean)

**Complexity:** HIGH (8-12 turns)
**Language:** Korean
**Agents:** A1, A5, C2, D2, E2, A3, C3

Tests:
- Phenomenological approach selection (Husserl vs Heidegger vs van Manen)
- Philosophical depth questions
- Devil's advocate reviewer anticipation
- Sample size justification (n=5)
- Paradigm reconsideration (pure qual vs mixed)
- Korean language consistency throughout

### MIXED-002: Complex Mixed Methods

**Complexity:** HIGH (8-10 turns)
**Language:** English
**Agents:** A1, C3, E3, D1, D2

Tests:
- Morse notation explanation
- Sequential vs concurrent design selection
- Joint display creation guidance
- Timeline constraint handling
- Sample size ratio recommendations
- Methodological flexibility defense

### HUMAN-002: Academic Humanization

**Complexity:** MEDIUM (6-8 turns)
**Language:** English
**Agents:** G5, G6, F5, A4

Tests:
- AI pattern detection and categorization
- Detection logic explanation
- Humanization transformation modes
- Ethical considerations (AI disclosure)
- Citation integrity verification
- Meaning preservation checking

## User Input Types

The protocol tests these complex user interaction patterns:

| Type | Description | Example |
|------|-------------|---------|
| `TECHNICAL_FOLLOW_UP` | Deep statistical/methodological questions | "Why Hedges' g over Cohen's d?" |
| `METHODOLOGICAL_CHALLENGE` | Critical questioning of approach | "But random-effects assumes normality..." |
| `AGENT_TRANSITION_REQUEST` | Request to switch focus | "Wait, can we do theory first?" |
| `SCOPE_CHANGE` | Modify research scope | "Should I include gray literature?" |
| `ALTERNATIVE_EXPLORATION` | Ask about unlisted options | "What about Bayesian meta-analysis?" |
| `PRACTICAL_CONSTRAINT` | Real-world limitations | "I only have 12 studies..." |
| `SELECTION` | Option choice | "[B] Subject-specific effects" |
| `APPROVAL` | Confirm and proceed | "Approved. Proceed." |

## Checkpoint Levels

| Level | Symbol | Behavior | Examples |
|-------|--------|----------|----------|
| RED | 🔴 | MUST HALT, wait for approval | Research direction, methodology approval |
| ORANGE | 🟠 | SHOULD HALT, but can proceed with warning | Scope decisions, theory selection |
| YELLOW | 🟡 | MAY proceed, log decision | Minor adjustments |

## Validation Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Checkpoint Compliance | 100% | All RED checkpoints trigger HALT |
| Technical Depth | ≥90% | Accurate answers to follow-up questions |
| Methodological Accuracy | ≥90% | Valid responses to challenges |
| Context Retention | ≥95% | Remembers prior decisions after agent switch |
| Language Consistency | 100% | Response matches input language |
| Agent Transition | ≥90% | Smooth handoff with context preservation |

## Session Log Location

Claude Code session logs are stored at:

```
~/.claude/projects/{project-id}/{session-id}.jsonl
```

Each line is a JSON object containing:
- `type`: "user", "assistant", or "tool_result"
- `content`: Message content
- `tool_calls`: Array of tool invocations (for assistant)
- `timestamp`: ISO timestamp

## Extraction Script Usage

```bash
# Basic extraction
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/abc123/session.jsonl \
  --output qa/reports/real-transcripts/

# With scenario ID
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/abc123/session.jsonl \
  --scenario-id META-002 \
  --output qa/reports/real-transcripts/

# With evaluation
python qa/runners/extract_conversation.py \
  --session ~/.claude/projects/abc123/session.jsonl \
  --expected qa/protocol/test_meta_002.yaml \
  --output qa/reports/real-transcripts/
```

## Test Runner Usage

```bash
# Run all protocol tests
python qa/run_tests.py --all

# Run specific scenario evaluation
python qa/run_tests.py --evaluate-extracted \
  --input qa/reports/real-transcripts/META-002.yaml \
  --expected qa/protocol/test_meta_002.yaml

# Generate HTML report
python qa/run_tests.py --all --report-format html \
  --output qa/reports/2026-01-29/
```

## Contributing

When adding new test scenarios:

1. Create YAML file in `qa/protocol/` following existing format
2. Define conversation flow with expected behaviors
3. Specify checkpoints, agent invocations, and validation rules
4. Run actual conversation in Claude Code
5. Extract and evaluate against expected

## Changelog

### v2.1 (2026-01-29)
- **Session-based folder management** - Each test session in `reports/sessions/{SCENARIO-ID}/`
- **RAW conversation extraction** - `conversation_raw.json` + `conversation_transcript.md`
- **GitHub deployment support** - Large JSONL files excluded, extracted files included
- **Session README** - Each session folder has overview and test results

### v2.0 (2026-01-29)
- Migrated from mock Python scripts to real Claude Code conversations
- Added complex user input types (technical follow-up, methodological challenge)
- Implemented JSONL session log extraction
- Added language consistency validation
- Created four advanced test scenarios (META-002, QUAL-002, MIXED-002, HUMAN-002)
