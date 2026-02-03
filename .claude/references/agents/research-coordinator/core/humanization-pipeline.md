---
name: humanization-pipeline
version: "1.0.0"
description: |
  Humanization Pipeline - Integrates AI pattern detection and transformation
  into the Research Coordinator workflow. Connects G5 (Auditor), G6 (Humanizer),
  and F5 (Verifier) with existing writing agents.
---

# Humanization Pipeline

## Overview

The Humanization Pipeline provides an optional but recommended step for all AI-generated academic text. It integrates seamlessly with existing Research Coordinator workflows to help researchers produce natural, authentic writing while maintaining academic integrity.

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         HUMANIZATION PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  STAGE 1: CONTENT GENERATION                                        │   │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │   │
│  │  │     G2       │  │     G3       │  │  Auto-Doc    │              │   │
│  │  │  Academic    │  │    Peer      │  │   System     │              │   │
│  │  │ Communicator │  │   Review     │  │              │              │   │
│  │  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │   │
│  │         │                 │                 │                       │   │
│  │         └─────────────────┴─────────────────┘                       │   │
│  │                           │                                         │   │
│  │                           ▼                                         │   │
│  └───────────────────────────┼─────────────────────────────────────────┘   │
│                              │                                              │
│  ┌───────────────────────────┼─────────────────────────────────────────┐   │
│  │  STAGE 2: ANALYSIS        │                                         │   │
│  │                           ▼                                         │   │
│  │           ┌───────────────────────────────┐                        │   │
│  │           │     G5-AcademicStyleAuditor   │                        │   │
│  │           │  ┌─────────────────────────┐  │                        │   │
│  │           │  │ • Pattern Detection     │  │                        │   │
│  │           │  │ • Risk Classification   │  │                        │   │
│  │           │  │ • AI Probability Score  │  │                        │   │
│  │           │  │ • Recommendations       │  │                        │   │
│  │           │  └─────────────────────────┘  │                        │   │
│  │           └───────────────┬───────────────┘                        │   │
│  │                           │                                         │   │
│  │                           ▼                                         │   │
│  │  ┌────────────────────────────────────────────────────────────┐    │   │
│  │  │  🟠 CHECKPOINT: CP_HUMANIZATION_REVIEW                     │    │   │
│  │  │                                                            │    │   │
│  │  │  "AI patterns detected. Would you like to humanize?"       │    │   │
│  │  │                                                            │    │   │
│  │  │  [A] Conservative  [B] Balanced ⭐  [C] Aggressive         │    │   │
│  │  │  [D] View Report   [E] Skip                                │    │   │
│  │  └────────────────────────────────────────────────────────────┘    │   │
│  └───────────────────────────┼─────────────────────────────────────────┘   │
│                              │                                              │
│                     ┌────────┴────────┐                                     │
│                     │                 │                                     │
│              User selects          User selects                             │
│                mode                 "Skip"                                  │
│                     │                 │                                     │
│                     ▼                 │                                     │
│  ┌───────────────────────────────────┐│                                     │
│  │  STAGE 3: TRANSFORMATION         ││                                     │
│  │           ▼                      ││                                     │
│  │  ┌─────────────────────────────┐ ││                                     │
│  │  │ G6-AcademicStyleHumanizer   │ ││                                     │
│  │  │ ┌─────────────────────────┐ │ ││                                     │
│  │  │ │ • Apply Transformations │ │ ││                                     │
│  │  │ │ • Preserve Citations    │ │ ││                                     │
│  │  │ │ • Maintain Integrity    │ │ ││                                     │
│  │  │ │ • Generate Diff Report  │ │ ││                                     │
│  │  │ └─────────────────────────┘ │ ││                                     │
│  │  └─────────────┬───────────────┘ ││                                     │
│  │                │                 ││                                     │
│  └────────────────┼─────────────────┘│                                     │
│                   │                  │                                      │
│                   ▼                  │                                      │
│  ┌───────────────────────────────────┼─────────────────────────────────┐   │
│  │  STAGE 4: VERIFICATION           │                                  │   │
│  │           ▼                      │                                  │   │
│  │  ┌─────────────────────────────┐ │                                  │   │
│  │  │  F5-HumanizationVerifier    │ │                                  │   │
│  │  │  ┌───────────────────────┐  │ │                                  │   │
│  │  │  │ • Re-run AI Detection │  │ │                                  │   │
│  │  │  │ • Check Integrity     │  │ │                                  │   │
│  │  │  │ • Verify Citations    │  │ │                                  │   │
│  │  │  │ • Confirm Meaning     │  │ │                                  │   │
│  │  │  └───────────────────────┘  │ │                                  │   │
│  │  └─────────────┬───────────────┘ │                                  │   │
│  │                │                 │                                  │   │
│  │                ▼                 │                                  │   │
│  │  ┌──────────────────────────────┐│                                  │   │
│  │  │  🟡 CHECKPOINT (Optional)   ││                                  │   │
│  │  │  CP_HUMANIZATION_VERIFY     ││                                  │   │
│  │  │                             ││                                  │   │
│  │  │  Review changes before      ││                                  │   │
│  │  │  final export               ││                                  │   │
│  │  └──────────────────────────────┘│                                  │   │
│  └───────────────────────────────────┼─────────────────────────────────┘   │
│                                      │                                      │
│                                      ▼                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  STAGE 5: OUTPUT                                                      │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                │ │
│  │  │   Word       │  │  PDF         │  │  Other       │                │ │
│  │  │  Export      │  │ Export       │  │ Formats      │                │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘                │ │
│  │                                                                       │ │
│  │  + Optional: AI Pattern Report Appendix                              │ │
│  │  + Optional: Transformation Audit Trail                              │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Integration Points

### With G2-AcademicCommunicator

When G2 generates content:

```yaml
trigger: "After G2 generates any output"
condition: "humanization_enabled: true (default)"

workflow:
  1. G2 generates content (abstract, summary, etc.)
  2. Auto-invoke G5 for pattern analysis
  3. Present CP_HUMANIZATION_REVIEW
  4. If user approves → invoke G6
  5. Verify with F5
  6. Output final version

commands:
  - "Generate abstract with humanization"
  - "Create summary (humanize: balanced)"
  - "Write press release (skip humanization)"
```

### With G3-PeerReviewStrategist

When G3 generates response letters:

```yaml
trigger: "After G3 generates response letter"
condition: "humanization_enabled: true"

special_rules:
  - Preserve professional gratitude phrases
  - Keep reviewer reference numbers
  - Maintain point-by-point structure
  - Focus on language/vocabulary patterns

workflow:
  1. G3 generates response letter
  2. G5 analysis with "response_letter" context
  3. Checkpoint with response-specific options
  4. G6 transformation (preserves structure)
  5. F5 verification
```

### With Auto-Documentation System

When exporting documents:

```yaml
trigger: "Export to Word/PDF/etc."
condition: "humanization_before_export: true"

workflow:
  1. Auto-doc prepares content
  2. G5 analyzes (section-aware)
  3. Checkpoint before export
  4. If approved → G6 transforms
  5. F5 verifies
  6. Export with humanized content

export_options:
  - "Export methods (with humanization)"
  - "Export manuscript (humanize: conservative)"
  - "Export draft (raw, no humanization)"
```

---

## Configuration

### Pipeline Settings

```yaml
# .research/humanization-config.yaml

humanization:
  enabled: true                    # Master switch
  default_mode: "balanced"         # conservative/balanced/aggressive

  auto_check: true                 # Auto-run G5 on exports
  show_checkpoint: true            # Show CP_HUMANIZATION_REVIEW
  require_verification: false      # Require F5 before export

  thresholds:
    skip_if_below: 20              # Skip if AI probability < 20%
    recommend_if_above: 40         # Recommend if > 40%
    require_if_above: 70           # Require review if > 70%

  reports:
    include_pattern_report: false  # Add to exports
    include_audit_trail: true      # Keep transformation log
    save_original: true            # Keep pre-humanization version

  ethics:
    show_disclosure_reminder: true
    suggest_acknowledgment: true
```

### Section-Specific Settings

```yaml
sections:
  abstract:
    mode: "conservative"
    strict_preservation: true

  methods:
    mode: "conservative"
    allow_boilerplate: true

  results:
    mode: "conservative"
    preserve_all_statistics: true

  discussion:
    mode: "balanced"
    allow_more_changes: true

  response_letter:
    mode: "balanced"
    preserve_gratitude: true
    preserve_structure: true
```

---

## Commands Reference

### Analysis Commands

```
"Check AI patterns"
→ Run G5 analysis only, show report

"Quick AI check"
→ Summary only (score + pattern count)

"Detailed pattern analysis"
→ Full G5 report with all patterns

"Show flagged vocabulary"
→ List all AI-typical words found
```

### Transformation Commands

```
"Humanize my draft"
→ Full pipeline with balanced mode

"Humanize (conservative)"
→ Pipeline with conservative mode

"Humanize (aggressive)"
→ Pipeline with aggressive mode

"Humanize section: methods"
→ Section-specific humanization
```

### Export Commands

```
"Export with humanization"
→ Export after full pipeline

"Export to Word (humanize: balanced)"
→ Word export with balanced mode

"Export raw (no humanization)"
→ Export without pipeline

"Export with AI report"
→ Include pattern analysis in appendix
```

### Utility Commands

```
"Compare original and humanized"
→ Side-by-side diff view

"Revert to original"
→ Undo humanization

"Show transformation log"
→ View all changes made

"Configure humanization"
→ Adjust pipeline settings
```

---

## Checkpoints

### CP_HUMANIZATION_REVIEW (🟠 Recommended)

**When:** After G5 analysis, before transformation

**Presents:**
- AI probability score
- Pattern summary (high/medium/low counts)
- Recommended mode
- User options

**Options:**
```
[A] Humanize (Conservative) - High-risk only
[B] Humanize (Balanced) ⭐ - Recommended
[C] Humanize (Aggressive) - Maximum
[D] View detailed report
[E] Skip humanization
```

### CP_HUMANIZATION_VERIFY (🟡 Optional)

**When:** After G6 transformation, before export

**Presents:**
- Before/after comparison
- Change summary
- New AI probability
- Integrity verification

**Options:**
```
[A] Approve and export
[B] Adjust specific changes
[C] Try different mode
[D] Revert to original
```

---

## Pipeline States

```yaml
states:
  idle:
    description: "No humanization in progress"
    transitions: [analyzing]

  analyzing:
    description: "G5 running pattern detection"
    agent: "G5-AcademicStyleAuditor"
    transitions: [awaiting_decision, idle]

  awaiting_decision:
    description: "Checkpoint presented, waiting for user"
    checkpoint: "CP_HUMANIZATION_REVIEW"
    transitions: [transforming, idle]

  transforming:
    description: "G6 applying transformations"
    agent: "G6-AcademicStyleHumanizer"
    transitions: [verifying]

  verifying:
    description: "F5 checking results"
    agent: "F5-HumanizationVerifier"
    transitions: [awaiting_approval, complete]

  awaiting_approval:
    description: "Optional verification checkpoint"
    checkpoint: "CP_HUMANIZATION_VERIFY"
    transitions: [complete, transforming, idle]

  complete:
    description: "Pipeline finished, ready for export"
    transitions: [idle]
```

---

## Error Handling

### Transformation Failures

```yaml
on_error:
  citation_modified:
    action: "ABORT"
    message: "Citation integrity violated. Reverting."
    log: true

  statistics_modified:
    action: "ABORT"
    message: "Statistical values changed. Reverting."
    log: true

  meaning_distorted:
    action: "FLAG"
    message: "Possible meaning change detected."
    require_review: true

  mode_inappropriate:
    action: "SUGGEST"
    message: "Consider different mode for this section."
    offer_alternatives: true
```

### Recovery Options

```
"Revert humanization"
→ Return to original text

"Undo last transformation"
→ Undo most recent change

"Reset pipeline"
→ Clear all state, start fresh
```

---

## Logging and Audit

### Transformation Log

```yaml
# .research/humanization-log.yaml

sessions:
  - session_id: "H001"
    timestamp: "2024-10-14T10:30:00Z"
    source: "G2-generated abstract"

    g5_analysis:
      ai_probability: 67%
      patterns_detected: 18
      high_risk: 5
      medium_risk: 9
      low_risk: 4

    user_decision:
      checkpoint: "CP_HUMANIZATION_REVIEW"
      selected: "balanced"
      timestamp: "2024-10-14T10:31:00Z"

    g6_transformation:
      mode: "balanced"
      changes_made: 12
      preserved: ["all citations", "all statistics"]

    f5_verification:
      new_ai_probability: 28%
      citation_integrity: true
      meaning_preserved: true

    final_action: "exported_to_word"
```

---

## Best Practices

### When to Use Each Mode

| Situation | Recommended Mode |
|-----------|------------------|
| Journal submission (high-impact) | Conservative |
| Journal submission (general) | Balanced |
| Conference paper | Balanced |
| Working paper | Balanced |
| Thesis chapter | Conservative |
| Grant proposal | Conservative |
| Blog post | Aggressive |
| Social media | Aggressive |
| Response letter | Balanced |

### When to Skip Humanization

- AI probability < 20%
- Human-written original text
- Direct quotes or transcripts
- Highly technical/formulaic sections
- When author prefers original style

---

## Integration with Existing Pipelines

### PRISMA Systematic Review Pipeline

Stage 7 (Manuscript Preparation) enhanced:

```yaml
stage_7_enhanced:
  steps:
    - "Draft sections (IMRAD)"
    - "Run G5 on each section"
    - "Present humanization options"
    - "Apply G6 if approved"
    - "Verify with F5"
    - "Create figures and tables"
    - "Export to Word"
```

### Experimental Study Pipeline

Stage 6 (Manuscript & Dissemination) enhanced:

```yaml
stage_6_enhanced:
  steps:
    - "Write manuscript sections"
    - "Humanization pipeline (optional)"
    - "Create figures"
    - "Prepare supplementary"
    - "Submit to journal"
```

---

## References

- **G5 Agent**: `../research-agents/G5-academic-style-auditor/SKILL.md`
- **G6 Agent**: `../research-agents/G6-academic-style-humanizer/SKILL.md`
- **F5 Agent**: `../research-agents/F5-humanization-verifier/SKILL.md`
- **User Checkpoints**: `./user-checkpoints.md`
- **Integration Hub**: `./integration-hub.md`
