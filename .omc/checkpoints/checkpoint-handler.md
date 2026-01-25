# Checkpoint Handler Protocol

## Core Principle
**Human decisions are NEVER bypassed. AI assists, humans decide.**

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
Location: .omc/state/checkpoints.json

Format:
```json
{
  "session_id": "...",
  "checkpoints": [
    {
      "id": "CP_RESEARCH_DIRECTION",
      "timestamp": "2025-01-25T...",
      "status": "approved",
      "human_decision": "Approved research question B",
      "agent": "01-research-question-refiner"
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
Agent: 01-research-question-refiner

Decision Required: Review and approve research question

[Agent's analysis and recommendations presented here]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Please respond with:
- "approve" or "approved" to proceed
- "reject" or "revise" to request changes
- Your feedback for modifications
```

## Checkpoint Recording

All checkpoint decisions are recorded in `.omc/state/checkpoints.json` with:
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

Never override REQUIRED checkpoints.
