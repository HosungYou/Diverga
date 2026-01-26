# Checkpoint Handler Protocol v6.0 (Human-Centered Edition)

## Core Principle
**Human decisions are NEVER bypassed. AI assists, humans decide.**

> "인간이 할 일은 인간이, AI는 인간의 범주를 벗어난 것을 수행"

## Checkpoint Levels

### REQUIRED (🔴)
- System STOPS and waits for human input
- No timeout, no auto-proceed
- Must be explicitly approved

### RECOMMENDED (🟠)
- System pauses and requests review
- Can auto-proceed after timeout if configured
- Human notified of auto-proceed

### OPTIONAL (🟡)
- System offers choice
- Uses default if human doesn't respond
- Records default was used

## Implementation

When reaching a checkpoint:
1. STOP current execution
2. Present checkpoint information to user
3. Wait for human response
4. Record decision with timestamp
5. Proceed only after approval (for required)

## Checkpoint State Storage
Location: `.claude/state/checkpoints.json`

Format:
```json
{
  "session_id": "...",
  "checkpoints": [
    {
      "id": "CP_RESEARCH_DIRECTION",
      "timestamp": "2026-01-25T...",
      "status": "approved",
      "human_decision": "Approved research question B",
      "agent": "A1-research-question-refiner"
    }
  ]
}
```

## Checkpoint Presentation Format

When presenting a checkpoint to the user:

```
🔴 HUMAN CHECKPOINT REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Checkpoint: CP_RESEARCH_DIRECTION
Agent: A1-research-question-refiner

Decision Required: Review and approve research question

[Agent's analysis and recommendations presented here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Please respond with:
- "approve" or "approved" to proceed
- "reject" or "revise" to request changes
- Your feedback for modifications
```

## Agent-Checkpoint Mapping (v6.0)

| Agent | Checkpoint | Level |
|-------|------------|-------|
| A1-research-question-refiner | CP_RESEARCH_DIRECTION | 🔴 REQUIRED |
| A2-theoretical-framework-architect | CP_THEORY_SELECTION | 🔴 REQUIRED |
| A5-paradigm-worldview-advisor | CP_PARADIGM_SELECTION | 🔴 REQUIRED |
| C1/C2/C3-design-consultants | CP_METHODOLOGY_APPROVAL | 🔴 REQUIRED |
| E1-quantitative-analysis-guide | CP_ANALYSIS_PLAN | 🟠 RECOMMENDED |
| E3-mixed-methods-integration | CP_INTEGRATION_STRATEGY | 🟠 RECOMMENDED |
| G3-peer-review-strategist | CP_RESPONSE_APPROVAL | 🟠 RECOMMENDED |
| A6-conceptual-framework-visualizer | CP_VISUALIZATION_PREFERENCE | 🟡 OPTIONAL |

## Checkpoint Recording

All checkpoint decisions are recorded in `.claude/state/checkpoints.json` with:
- Timestamp of decision
- Human's exact response
- Checkpoint ID and associated agent
- Status (approved/rejected/deferred)

This creates an audit trail of all human decisions during the research process.

## Auto-Proceed Rules (for RECOMMENDED checkpoints)

If a checkpoint has `can_auto_proceed: true`:
1. Present checkpoint to user
2. Wait for `auto_proceed_delay` seconds
3. If no response, notify user of auto-proceed
4. Record that auto-proceed was used
5. Continue with default action

User can override auto-proceed at any time before it triggers.

## Checkpoint Override (Emergency)

Users can override checkpoint behavior:
- `--skip-optional`: Skip all optional checkpoints, use defaults
- `--fast-track`: Reduce recommended checkpoint delays to 10 seconds
- `--strict`: Require review even for optional checkpoints

**Never override REQUIRED checkpoints.**

## v6.0 Changes

| Before (v5.0) | After (v6.0) |
|---------------|--------------|
| Sisyphus could bypass checkpoints | All checkpoints enforced |
| "agent OR checkpoint" (Iron Law) | "checkpoint THEN agent" |
| State in `.omc/` | State in `.claude/` |
| Numbered agents (01-21) | Category agents (A1-H2) |
