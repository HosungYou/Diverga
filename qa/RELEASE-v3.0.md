# Diverga QA Protocol v3.0 Release Notes

## True Automated Testing Edition

**Release Date**: 2026-01-29
**Version**: QA Protocol v3.0

---

## Overview

QA Protocol v3.0 represents a paradigm shift from **simulation-based testing** to **true automated testing with real AI responses**. This release replaces hardcoded `RESPONSE_TEMPLATES` with actual CLI-based AI invocations, enabling genuine functional validation of the Diverga Research Coordinator.

---

## Core Philosophy

> **"Test with Real AI, Not Simulations"**
> **"시뮬레이션이 아닌 실제 AI로 테스트"**

---

## What's New

### 1. CLI-Based Automated Testing

Execute tests programmatically via CLI tools with no manual intervention:

| CLI Tool | Command | Session Support |
|----------|---------|-----------------|
| `claude` | `claude -p "message"` | `--continue` for multi-turn |
| `opencode` | `opencode run "message"` | Single-turn |
| `codex` | `codex exec "message"` | `--resume` |

### 2. CLITestRunner Class

New Python class for orchestrating CLI-based tests:

```python
from qa.runners import CLITestRunner

runner = CLITestRunner(
    scenario_id='QUAL-002',
    cli_tool='claude',
    verbose=True,
    dry_run=False,
    timeout=300
)

session = runner.run()
runner.save_results('qa/reports/sessions')
```

#### Key Features

- **Subprocess-based execution**: Capture real AI responses via `subprocess.run()`
- **Multi-turn sessions**: Maintain conversation context with `--continue` flag
- **Checkpoint detection**: Regex patterns for 🔴, 🟠, 🟡 markers
- **Agent tracking**: Detect `diverga:*` and `A1-*` style agent invocations
- **VS option extraction**: Parse T-Score values from responses
- **Dry run mode**: Test framework without API calls

### 3. Batch Testing Script

Run all scenarios with a single command:

```bash
# Real AI testing
./qa/run_all_scenarios.sh

# Dry run mode
./qa/run_all_scenarios.sh --dry-run

# Alternative CLI tool
./qa/run_all_scenarios.sh --cli opencode
```

### 4. Structured Output

Each test generates four files:

| File | Description |
|------|-------------|
| `README.md` | Session overview with metrics |
| `conversation_transcript.md` | Human-readable conversation |
| `conversation_raw.json` | RAW data with full metadata |
| `{SCENARIO}_test_result.yaml` | Test results and validation |

### 5. VERIFICATION HUDDLE (v3.0.1)

**Purpose**: Confirm responses are from real AI API calls, not simulation or dry-run.

The Verification Huddle runs 6 automated checks on every test:

| Check | Description | Pass Criteria |
|-------|-------------|---------------|
| **NO_SIMULATION_MARKERS** | Detect `[DRY RUN]`, `[SIMULATED]` markers | No markers found |
| **RESPONSE_LENGTH_VARIANCE** | Natural response length variation | >200 chars variance |
| **TIMESTAMP_VARIANCE** | Natural response timing intervals | Non-identical intervals |
| **CONTEXT_AWARENESS** | AI references specific user input | ≥2 context references |
| **UNIQUE_SESSION_ID** | Valid UUID session identifier | Valid UUID format |
| **DYNAMIC_CONTENT** | Non-templated, reasoning-based content | No template patterns |

#### Example Output

```
🔍 VERIFICATION HUDDLE

Result: ✅ VERIFICATION PASSED (6/6 checks)

| Check                    | Status  | Detail                              |
|--------------------------|---------|-------------------------------------|
| NO_SIMULATION_MARKERS    | ✅ PASS | No simulation markers found         |
| RESPONSE_LENGTH_VARIANCE | ✅ PASS | Length variance: 3241 chars         |
| TIMESTAMP_VARIANCE       | ✅ PASS | Response intervals: 19.7s, 168.5s   |
| CONTEXT_AWARENESS        | ✅ PASS | 12 context references found         |
| UNIQUE_SESSION_ID        | ✅ PASS | Session ID: 3f2de307...             |
| DYNAMIC_CONTENT          | ✅ PASS | Content appears dynamic             |
```

#### Why Verification Huddle?

- **Trust**: Confirm test results are from actual AI, not cached/simulated data
- **Debugging**: Quickly identify if dry-run mode was accidentally enabled
- **Audit Trail**: Each test session includes verification evidence in `README.md`

---

## Multi-CLI Architecture (v3.0.3)

### Overview

Diverga now supports three CLI tools with different invocation patterns:

```
                          ┌─────────────────────────────────────────┐
                          │         Diverga Research Coordinator    │
                          │         40 Agents | 8 Categories        │
                          └─────────────────────┬───────────────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    │                           │                           │
            ┌───────┴───────┐           ┌───────┴───────┐           ┌───────┴───────┐
            │  Claude Code  │           │   Codex CLI   │           │   OpenCode    │
            │    (Native)   │           │   (Adapted)   │           │ (oh-my-oc)    │
            └───────┬───────┘           └───────┬───────┘           └───────┬───────┘
                    │                           │                           │
    ┌───────────────┴───────────────┐   ┌───────┴───────┐   ┌───────────────┴───────────────┐
    │ Task(subagent="diverga:a1")  │   │ Read SKILL.md │   │ Task(subagent="diverga:a1")  │
    │ Full parallel execution       │   │ Follow instns │   │ oh-my-opencode compatible    │
    └───────────────────────────────┘   └───────────────┘   └───────────────────────────────┘
```

### Installation Paths

| CLI Tool | Installation Path | Adapter Template |
|----------|-------------------|------------------|
| Claude Code | `~/.claude/plugins/diverga/` | `claude-settings.template.json` |
| Codex CLI | `~/.codex/diverga/` + `~/.codex/skills/diverga/` | `AGENTS.md.template` |
| OpenCode | `~/.config/opencode/plugins/diverga/` | `oh-my-opencode.template.json` |

### Unified Installation

```bash
# Install for all CLI tools
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash

# Install for specific CLI only
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --claude
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --codex
curl -sSL https://raw.githubusercontent.com/HosungYou/Diverga/main/scripts/install-multi-cli.sh | bash -s -- --opencode
```

### Agent Invocation Patterns

**Claude Code** (Native Task Tool):
```python
Task(
    subagent_type="diverga:a1",
    model="opus",
    prompt="Refine this research question: [user input]"
)
```

**Codex CLI** (Skill File):
```bash
# Agent behavior is loaded from skill file
cat ~/.codex/skills/diverga/A1-research-question-refiner/SKILL.md
# Then AI follows the instructions in the file
```

**OpenCode** (oh-my-opencode):
```python
# Same as Claude Code if oh-my-opencode is installed
Task(
    subagent_type="diverga:a1",
    model="opus",
    prompt="Refine this research question: [user input]"
)
```

---

## v2.x vs v3.0 Comparison

| Aspect | v2.x (Simulation) | v3.0 (True Automation) |
|--------|-------------------|------------------------|
| **AI Response** | `RESPONSE_TEMPLATES` dict | **Real AI generation** |
| **Execution** | Python simulator | **CLI non-interactive mode** |
| **Validation** | Protocol format only | **Actual functionality** |
| **API Calls** | None | Real token consumption |
| **Response Variety** | Fixed templates | **Different every run** |

---

## Test Results: QUAL-002

First successful run with real AI on 2026-01-29:

```
============================================================
Diverga QA Protocol v3.0 - True Automated Testing
Scenario: QUAL-002
CLI Tool: claude
Mode: LIVE
============================================================

[Turn 1] INITIAL_REQUEST
  Received: 792 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 2] METHODOLOGICAL_CHALLENGE
  Received: 1810 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 3] SELECTION
  Received: 2469 chars
  ✓ Completed (CP: 1, Agents: 0)

...

[Turn 8] APPROVAL
  Received: 889 chars
  ✓ Completed (CP: 1, Agents: 0)

============================================================
Test Completed: QUAL-002
Turns: 8 | Checkpoints: 8 | Duration: ~4 min
============================================================
```

### Metrics Summary

| Metric | Value |
|--------|-------|
| Total Turns | 8 |
| Checkpoints Found | 8 |
| Total Response Characters | ~21,000 |
| Test Duration | ~4 minutes |

---

## Test Results: QUAL-003 (with Verification Huddle)

Second test run demonstrating the new VERIFICATION HUDDLE feature:

```
============================================================
Diverga QA Protocol v3.0 - True Automated Testing
Scenario: QUAL-003
CLI Tool: claude
Mode: LIVE
============================================================

[Turn 1] INITIAL_REQUEST
  Received: 988 chars
  ✓ Completed (CP: 1, Agents: 3)

[Turn 2] METHODOLOGICAL_CHALLENGE
  Received: 2979 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 3] SELECTION
  Received: 2905 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 4] PRACTICAL_CONSTRAINT
  Received: 4229 chars
  ✓ Completed (CP: 1, Agents: 0)

[Turn 5] APPROVAL
  Received: 3986 chars
  ✓ Completed (CP: 1, Agents: 3)

============================================================
Test Completed: QUAL-003
Turns: 5 | Checkpoints: 5 | Agents: 6
VERIFICATION HUDDLE: ✅ PASSED (6/6 checks)
============================================================
```

### QUAL-003 Metrics

| Metric | Value |
|--------|-------|
| Total Turns | 5 |
| Checkpoints Found | 5 |
| Agents Detected | 6 (A1, A5, C2, D1, D2, A4) |
| Response Length Range | 988 - 4,229 chars |
| Test Duration | ~4 minutes |
| Verification Huddle | ✅ PASSED (6/6) |

---

## Breaking Changes

### Removed

- `RESPONSE_TEMPLATES` dictionary in `automated_test.py` (v2.x only)
- Simulated response generation

### Changed

- `__init__.py` now exports both v2.x and v3.0 components
- Module structure supports backward compatibility

### Added

- `cli_test_runner.py` - New CLI test runner
- `run_all_scenarios.sh` - Batch testing script
- `CLITurn` alias to distinguish from v2.x `Turn`

---

## Directory Structure

```
qa/
├── README.md                    # Updated documentation
├── run_all_scenarios.sh         # v3.0 batch test script (NEW)
├── RELEASE-v3.0.md              # This file (NEW)
│
├── protocol/                    # Test scenario definitions
│   ├── test_qual_001.yaml
│   ├── test_qual_002.yaml       # QUAL-002 tested
│   ├── test_qual_003.yaml       # QUAL-003 with Verification Huddle (NEW)
│   ├── test_meta_001.yaml
│   ├── test_meta_002.yaml
│   ├── test_mixed_001.yaml
│   ├── test_mixed_002.yaml
│   ├── test_human_001.yaml
│   └── test_human_002.yaml
│
├── runners/                     # Test runners
│   ├── __init__.py              # Updated exports
│   ├── cli_test_runner.py       # v3.0 CLI runner (NEW)
│   ├── automated_test.py        # v2.x simulator
│   ├── extract_conversation.py
│   ├── checkpoint_validator.py
│   └── agent_tracker.py
│
└── reports/                     # Test results
    ├── sessions/
    │   ├── QUAL-002/            # Real AI test results
    │   │   ├── README.md
    │   │   ├── conversation_transcript.md
    │   │   ├── conversation_raw.json
    │   │   └── QUAL-002_test_result.yaml
    │   └── QUAL-003/            # With Verification Huddle (NEW)
    │       ├── README.md        # Includes VERIFICATION HUDDLE section
    │       ├── conversation_transcript.md
    │       ├── conversation_raw.json
    │       └── QUAL-003_test_result.yaml
    └── real-transcripts/
```

---

## Usage Guide

### Single Scenario (Real AI)

```bash
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --cli claude
```

### Single Scenario (Dry Run)

```bash
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 --dry-run
```

### All Scenarios (Batch)

```bash
./qa/run_all_scenarios.sh
```

### Verbose Mode

```bash
python3 qa/runners/cli_test_runner.py --scenario QUAL-002 -v
```

---

## Requirements

1. **Claude Code CLI**: `npm install -g @anthropic-ai/claude-code`
2. **Authentication**: `claude` command must have API access
3. **Diverga Plugin**: Installed at `~/.claude/plugins/`

---

## Future Enhancements

- [x] ~~OpenCode and Codex CLI integration testing~~ (v3.0.2: Codex tested with QUANT-001)
- [x] ~~Multi-CLI Architecture Design~~ (v3.0.3: adapters/ directory with templates)
- [ ] OpenCode CLI testing with oh-my-opencode
- [ ] Parallel scenario execution
- [ ] Automated CI/CD integration
- [ ] Performance regression tracking
- [ ] Agent invocation verification

---

## Changelog

### v3.0.3 (2026-01-29)

**Multi-CLI Compatibility Edition**

- **ADDED**: `adapters/` directory with CLI-specific templates
  - `AGENTS.md.template` - Codex CLI bootstrap template
  - `oh-my-opencode.template.json` - OpenCode configuration
  - `claude-settings.template.json` - Claude Code settings
- **ADDED**: `scripts/install-multi-cli.sh` - Unified installer for all CLI tools
  - Supports `--claude`, `--codex`, `--opencode`, `--all` flags
  - Single command installation: `curl ... | bash`
- **DOCUMENTED**: CLI compatibility matrix
  - Claude Code: Full Task tool subagent support
  - Codex CLI: Skill file invocation (no native subagents)
  - OpenCode: oh-my-opencode compatible with Task tool support
- **VERIFIED**: QUANT-001 Claude Code retest passed (6/6 verification hurdles)

**CLI Compatibility Matrix**:

| Feature | Claude Code | Codex CLI | OpenCode |
|---------|-------------|-----------|----------|
| Plugin System | Native | 2025.12 Skills | oh-my-opencode |
| Task Tool (Subagents) | Native | Not supported | Supported |
| SKILL.md Format | Native | 2025.12 Added | Compatible |
| Agent Invocation | `diverga:a1` | Read skill file | `diverga:a1` |
| Installation Path | `~/.claude/plugins/` | `~/.codex/skills/` | `~/.config/opencode/` |

### v3.0.2 (2026-01-29)

- **FIXED**: Checkpoint detection regex to handle markdown bold markers (`**CP_WORD**`)
- **FIXED**: Agent detection regex with improved normalization
- **ADDED**: `test_quant_001.yaml` - Experimental Design with Power Analysis (English)
- **TESTED**: QUANT-001 with Codex CLI (6/6 verification checks passed)
- **DOCUMENTED**: CLI tool capability differences (Claude Code vs Codex vs OpenCode)
  - Claude Code: Full Diverga plugin/agent support
  - Codex: No plugin system, standalone LLM only
  - OpenCode: Limited plugin support

### v3.0.1 (2026-01-29)

- **ADDED**: VERIFICATION HUDDLE system with 6 automated checks
  - NO_SIMULATION_MARKERS: Detect `[DRY RUN]` markers
  - RESPONSE_LENGTH_VARIANCE: Natural length variation
  - TIMESTAMP_VARIANCE: Natural response timing
  - CONTEXT_AWARENESS: User input references
  - UNIQUE_SESSION_ID: Valid UUID verification
  - DYNAMIC_CONTENT: Non-templated content detection
- **ADDED**: `test_qual_003.yaml` - Grounded Theory scenario (English)
- **ADDED**: Verification Huddle section in session README.md
- **TESTED**: QUAL-003 with real AI + Verification Huddle (6/6 checks passed)

### v3.0.0 (2026-01-29)

- **ADDED**: `cli_test_runner.py` with `CLITestRunner` class
- **ADDED**: `run_all_scenarios.sh` batch test script
- **ADDED**: Dry run mode for framework testing
- **ADDED**: Multi-turn session support with `--continue`
- **UPDATED**: `__init__.py` to export v3.0 components
- **UPDATED**: `README.md` with v3.0 documentation
- **TESTED**: QUAL-002 scenario with real AI (8 turns, 8 checkpoints)

### v2.2.0 (2026-01-29)

- Automated test simulation with `RESPONSE_TEMPLATES`
- CLI-based execution: `python3 qa/runners/automated_test.py`

### v2.1.0 (2026-01-29)

- Session-based folder management
- RAW conversation extraction

### v2.0.0 (2026-01-29)

- Migrated to real Claude Code conversations
- Complex user input types
- JSONL session log extraction

---

## Contributors

- Hosung You (@HosungYou)
- Claude Opus 4.5 (AI Assistant)

---

## License

MIT License - Part of the Diverga Research Coordinator project.
