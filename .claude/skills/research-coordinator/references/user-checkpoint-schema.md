---
name: user-checkpoint-schema
description: Schema definition for AskUserQuestion checkpoint integration
version: "3.0.0"
---

# User Checkpoint Schema Reference

## Standard Checkpoint Schema

```yaml
checkpoint:
  # Required fields
  id: "CP-{MODULE}-{NUMBER}"      # Unique identifier
  type: "PREFERENCE | APPROVAL | GUARDRAIL | ITERATION"
  phase: "string"                  # Where this checkpoint occurs

  # Question definition
  question:
    header: "string"               # Max 12 chars, shown as chip/tag
    text: "string"                 # Main question text
    context: "string"              # Optional additional context

  # Options (2-4 required)
  options:
    - label: "string"              # Display text (1-5 words)
      description: "string"        # Explanation
      risk_level: "low|medium|high"  # GUARDRAIL type only
      recommended: boolean         # Highlight as default

  # Behavior
  multiSelect: boolean            # Allow multiple selections
  fallback: "string"              # Default if no response
```

## Checkpoint Type Behaviors

| Type | Icon | When Triggered | User Action Required |
|------|------|----------------|---------------------|
| PREFERENCE | Blue | Preference needed | Select option(s) |
| APPROVAL | Yellow | Explicit approval | Confirm or reject |
| GUARDRAIL | Red | Risk detected | Acknowledge risk |
| ITERATION | Green | Process control | Continue or loop |

## AskUserQuestion Mapping

Checkpoint to AskUserQuestion tool call:

```python
# Checkpoint definition
checkpoint = {
    "id": "CP-INIT-002",
    "type": "PREFERENCE",
    "question": {
        "header": "Creativity",
        "text": "Select your desired creativity level."
    },
    "options": [
        {"label": "Conservative", "description": "Safe, established approaches"},
        {"label": "Balanced", "description": "Balanced approach", "recommended": True},
        {"label": "Innovative", "description": "Novel, experimental approaches"}
    ],
    "multiSelect": False
}

# Converts to AskUserQuestion
AskUserQuestion(
    questions=[{
        "header": "Creativity",
        "question": "Select your desired creativity level.",
        "options": [
            {"label": "Conservative", "description": "Safe, established approaches"},
            {"label": "Balanced (Recommended)", "description": "Balanced approach"},
            {"label": "Innovative", "description": "Novel, experimental approaches"}
        ],
        "multiSelect": False
    }]
)
```

## Checkpoint Registry

### Initialization Checkpoints (CP-INIT-*)

| ID | Type | Purpose | Options |
|----|------|---------|---------|
| CP-INIT-001 | PREFERENCE | Research Type Selection | Quantitative, Qualitative, Mixed, Meta-Analysis |
| CP-INIT-002 | PREFERENCE | Creativity Level Selection | Conservative, Balanced, Innovative, Extreme |
| CP-INIT-003 | PREFERENCE | T-Score Mode Selection | Static, Dynamic, Hybrid |

**CP-INIT-001 Definition**:
```yaml
id: "CP-INIT-001"
type: "PREFERENCE"
phase: "initialization"
question:
  header: "Research Type"
  text: "What type of research are you conducting?"
  context: "This determines which agents and workflows are available."
options:
  - label: "Quantitative"
    description: "Statistical analysis, hypothesis testing"
  - label: "Qualitative"
    description: "Interviews, thematic analysis"
  - label: "Mixed Methods"
    description: "Combined quantitative and qualitative"
  - label: "Meta-Analysis"
    description: "Systematic review and synthesis"
    recommended: false
multiSelect: false
fallback: "Quantitative"
```

**CP-INIT-002 Definition**:
```yaml
id: "CP-INIT-002"
type: "PREFERENCE"
phase: "initialization"
question:
  header: "Creativity"
  text: "Select your desired creativity level."
  context: "Higher creativity enables more experimental approaches."
options:
  - label: "Conservative"
    description: "Established methods only"
  - label: "Balanced"
    description: "Mix of proven and novel approaches"
    recommended: true
  - label: "Innovative"
    description: "Emphasize novel approaches"
  - label: "Extreme"
    description: "Maximum creativity, experimental"
multiSelect: false
fallback: "Balanced"
```

**CP-INIT-003 Definition**:
```yaml
id: "CP-INIT-003"
type: "PREFERENCE"
phase: "initialization"
question:
  header: "T-Score Mode"
  text: "How should theory typicality scores be calculated?"
  context: "Affects framework selection recommendations."
options:
  - label: "Static"
    description: "Use reference tables (fast, offline)"
  - label: "Dynamic"
    description: "Query APIs for current data (accurate)"
  - label: "Hybrid"
    description: "Static base with dynamic adjustments"
    recommended: true
multiSelect: false
fallback: "Hybrid"
```

### VS Engine Checkpoints (CP-VS-*)

| ID | Type | Purpose | Options |
|----|------|---------|---------|
| CP-VS-001 | PREFERENCE | Direction Selection | Multiple framework directions |
| CP-VS-002 | GUARDRAIL | Low-Typicality Warning | Proceed, Switch, Explain |
| CP-VS-003 | ITERATION | Satisfaction Check | Satisfied, Iterate, Reset |

**CP-VS-001 Definition**:
```yaml
id: "CP-VS-001"
type: "PREFERENCE"
phase: "vs_phase_3"
question:
  header: "Direction"
  text: "Which theoretical direction would you like to explore?"
  context: "Generated directions based on your research context."
options: []  # Dynamically populated
multiSelect: false
fallback: null  # Must select
```

**CP-VS-002 Definition**:
```yaml
id: "CP-VS-002"
type: "GUARDRAIL"
phase: "vs_phase_3"
question:
  header: "Warning"
  text: "Selected framework has low typicality (T < 0.3). This may face reviewer skepticism."
  context: "Low-typicality frameworks are novel but may require stronger justification."
options:
  - label: "Proceed Anyway"
    description: "Continue with selected framework"
    risk_level: "medium"
  - label: "Switch Framework"
    description: "Choose a higher-typicality alternative"
    risk_level: "low"
    recommended: true
  - label: "Explain More"
    description: "Get detailed justification strategy"
    risk_level: "low"
multiSelect: false
fallback: "Switch Framework"
```

**CP-VS-003 Definition**:
```yaml
id: "CP-VS-003"
type: "ITERATION"
phase: "vs_phase_5"
question:
  header: "Satisfaction"
  text: "Are you satisfied with this output?"
  context: "You can iterate for improvements or proceed."
options:
  - label: "Satisfied"
    description: "Accept and continue"
    recommended: true
  - label: "Iterate"
    description: "Generate alternative approaches"
  - label: "Reset"
    description: "Start VS process over"
multiSelect: false
fallback: "Satisfied"
```

### Creativity Mechanism Checkpoints

#### Forced Analogy (CP-FA-*)

| ID | Type | Purpose |
|----|------|---------|
| CP-FA-001 | PREFERENCE | Source domain selection |
| CP-FA-002 | APPROVAL | Analogy validation |

#### Iterative Loop (CP-IL-*)

| ID | Type | Purpose |
|----|------|---------|
| CP-IL-001 | PREFERENCE | Initial direction |
| CP-IL-002 | ITERATION | Iteration 1 check |
| CP-IL-003 | ITERATION | Iteration 2 check |
| CP-IL-004 | APPROVAL | Final selection |

#### Semantic Distance (CP-SD-*)

| ID | Type | Purpose |
|----|------|---------|
| CP-SD-001 | PREFERENCE | Distance threshold |
| CP-SD-002 | PREFERENCE | Integration selection |

#### Temporal Reframing (CP-TR-*)

| ID | Type | Purpose |
|----|------|---------|
| CP-TR-001 | PREFERENCE | Temporal frame selection |

#### Community Simulation (CP-CS-*)

| ID | Type | Purpose |
|----|------|---------|
| CP-CS-001 | PREFERENCE | Persona selection |
| CP-CS-002 | APPROVAL | Feedback integration |

### Agent-Specific Checkpoints (CP-AG-*)

| ID | Type | Purpose | Triggering Agents |
|----|------|---------|-------------------|
| CP-AG-001 | GUARDRAIL | Ethics Confirmation | D4-EthicsAdvisor |
| CP-AG-002 | APPROVAL | Critique Acceptance | All Category D agents |
| CP-AG-003 | GUARDRAIL | Bias Acknowledgment | D1-BiasDetector |

**CP-AG-001 Definition**:
```yaml
id: "CP-AG-001"
type: "GUARDRAIL"
phase: "agent_execution"
question:
  header: "Ethics"
  text: "Potential ethical concerns identified. Please review."
  context: "The following concerns were flagged by D4-EthicsAdvisor."
options:
  - label: "Acknowledged"
    description: "I understand and will address these concerns"
    risk_level: "low"
    recommended: true
  - label: "Need Guidance"
    description: "Please provide more detailed guidance"
    risk_level: "low"
  - label: "Disagree"
    description: "I believe these concerns don't apply"
    risk_level: "high"
multiSelect: false
fallback: "Acknowledged"
```

### End Checkpoints (CP-END-*)

| ID | Type | Purpose |
|----|------|---------|
| CP-END-001 | ITERATION | Overall Satisfaction |

**CP-END-001 Definition**:
```yaml
id: "CP-END-001"
type: "ITERATION"
phase: "completion"
question:
  header: "Complete"
  text: "Are you satisfied with the overall research coordination results?"
  context: "You can request modifications or accept the current output."
options:
  - label: "Fully Satisfied"
    description: "Accept all outputs"
    recommended: true
  - label: "Minor Revisions"
    description: "Request small adjustments"
  - label: "Major Revisions"
    description: "Significant changes needed"
  - label: "Start Over"
    description: "Begin new coordination session"
multiSelect: false
fallback: "Fully Satisfied"
```

## Response Processing

### Response Schema

```yaml
checkpoint_response:
  checkpoint_id: "string"
  timestamp: "ISO8601"
  selected_options: ["string"]  # Array even for single select
  user_comment: "string"        # Optional free-text
  processing_time_ms: integer
```

### Response Handlers

```python
def handle_checkpoint_response(checkpoint_id: str, response: dict) -> Action:
    """Process user response and determine next action."""

    checkpoint = get_checkpoint(checkpoint_id)
    selected = response["selected_options"]

    if checkpoint.type == "PREFERENCE":
        return update_context(checkpoint_id, selected)

    elif checkpoint.type == "APPROVAL":
        if "Approved" in selected or "Proceed" in selected:
            return continue_execution()
        else:
            return handle_rejection(checkpoint_id, selected)

    elif checkpoint.type == "GUARDRAIL":
        log_risk_acknowledgment(checkpoint_id, selected)
        return continue_with_caution(selected)

    elif checkpoint.type == "ITERATION":
        if "Satisfied" in selected:
            return proceed_to_next_phase()
        elif "Iterate" in selected:
            return trigger_iteration()
        else:
            return handle_reset()
```

## Localization Support

### Korean Labels

```yaml
localization:
  ko:
    CP-INIT-001:
      header: "연구 유형"
      text: "어떤 유형의 연구를 수행하시나요?"
      options:
        - label: "양적 연구"
        - label: "질적 연구"
        - label: "혼합 연구"
        - label: "메타분석"

    CP-INIT-002:
      header: "창의성"
      text: "원하시는 창의성 수준을 선택하세요."
      options:
        - label: "보수적"
        - label: "균형"
        - label: "혁신적"
        - label: "극단적"
```

## Validation Rules

```yaml
validation:
  id_format: "^CP-[A-Z]{2,4}-\\d{3}$"
  header_max_length: 12
  text_max_length: 200
  option_count:
    min: 2
    max: 4
  label_max_length: 20
  description_max_length: 100
```

## Version History

| Version | Changes |
|---------|---------|
| 3.0.0 | Initial schema definition |
| 3.0.1 | Added localization support |
| 3.0.2 | Extended validation rules |
