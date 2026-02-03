---
name: ai-writing-ethics
version: "1.0.0"
description: |
  AI Writing Ethics Framework - Guidelines for responsible use of AI-assisted
  academic writing and humanization features in Research Coordinator.
---

# AI Writing Ethics Framework

## Core Principle

> **"Humanization improves expression, not deception."**

The humanization features in Research Coordinator are designed to help researchers express their ideas naturally and clearly—not to evade AI detection or circumvent academic integrity policies.

---

## Transparency Commitment

### What Humanization Does

✅ **Helps researchers:**
- Express ideas in natural language
- Avoid robotic or stilted phrasing
- Maintain scholarly tone while being readable
- Remove obvious AI artifacts that distract from content

### What Humanization Does NOT Do

❌ **Does not:**
- Make AI use "undetectable" (detection technology improves constantly)
- Replace the need for AI disclosure
- Generate original ideas or research
- Substitute for human judgment and expertise
- Guarantee acceptance or avoid scrutiny

---

## Researcher Responsibilities

### 1. Know Your Policies

Before using AI assistance, understand:

```yaml
check_policies:
  - institution: "Your university's AI use policy"
  - journal: "Target journal's AI disclosure requirements"
  - funding: "Grant agency requirements"
  - field: "Disciplinary norms and expectations"
```

### 2. Maintain Intellectual Ownership

The research must be yours:

```yaml
your_contribution:
  - research_question: "You formulated it"
  - methodology: "You designed or selected it"
  - data_collection: "You conducted or supervised it"
  - analysis: "You performed or directed it"
  - interpretation: "You understood and explained it"
  - conclusions: "You drew them from evidence"

ai_contribution:
  - writing_assistance: "Expression of your ideas"
  - editing: "Clarity and flow improvements"
  - formatting: "Structural suggestions"
```

### 3. Disclose AI Use

When required or recommended:

```yaml
disclosure_contexts:
  required:
    - "Journal explicitly requires AI disclosure"
    - "Institution mandates acknowledgment"
    - "Funding agency requires reporting"

  recommended:
    - "Substantial AI assistance in writing"
    - "AI used beyond basic grammar/spelling"
    - "When in doubt about expectations"

  typically_not_required:
    - "Basic spell-check and grammar tools"
    - "Translation assistance"
    - "Reference formatting"
```

---

## Disclosure Templates

### For Journal Submissions

```markdown
## AI Use Statement

This manuscript was prepared with AI writing assistance (Anthropic Claude)
for drafting and editing purposes. All AI-generated content was reviewed,
verified, and edited by the authors. The research conception, methodology,
data collection, analysis, and interpretation represent the original work
of the authors.
```

### For Conference Presentations

```markdown
## Acknowledgments

The authors acknowledge the use of AI tools (Anthropic Claude) for
assistance with presentation materials. All content reflects the
authors' original research findings.
```

### For Grant Proposals

```markdown
## AI Disclosure

AI writing tools were used to assist with proposal drafting. All
scientific content, methodology design, and research plans represent
the original work of the research team.
```

### For Theses/Dissertations

```markdown
## Declaration

I declare that this thesis represents my own original work. AI writing
assistance (Anthropic Claude) was used for drafting and editing certain
sections under my direction. All intellectual contributions, including
research design, analysis, and conclusions, are my own work.

[Signed]
```

---

## Ethical Red Lines

### NEVER Use AI To:

```yaml
prohibited_uses:
  - fabricate_data: "Generate fake research data"
  - create_citations: "Invent non-existent references"
  - plagiarize: "Pass off others' work as your own"
  - misrepresent: "Claim expertise you don't have"
  - deceive_reviewers: "Hide substantive AI authorship"
  - bypass_learning: "Avoid developing writing skills (students)"
  - violate_policies: "Circumvent explicit AI prohibitions"
```

### When AI Use is Inappropriate

```yaml
inappropriate_contexts:
  - "Exams or assessments prohibiting AI"
  - "Assignments meant to develop writing skills"
  - "When journal explicitly prohibits AI"
  - "When funding terms prohibit AI"
  - "When you can't verify AI output accuracy"
```

---

## Humanization Ethics Specifically

### Ethical Humanization

```yaml
ethical_use:
  purpose: "Improve clarity and naturalness"
  preserves: "All substantive content"
  maintains: "Academic integrity"
  acknowledges: "AI assistance when appropriate"
  respects: "Institutional and journal policies"
```

### Unethical Humanization

```yaml
unethical_use:
  purpose: "Evade detection to deceive"
  intent: "Hide substantial AI authorship"
  context: "Violating explicit AI policies"
  effect: "Misrepresenting work as fully human-written"
```

### The Key Distinction

```
ETHICAL: "I used AI to help express my research clearly."
         → Humanization improves your authentic work

UNETHICAL: "I used AI to write this and made it look human."
           → Humanization hides AI authorship
```

---

## Guidance for Specific Situations

### Situation 1: Journal Has No AI Policy

```yaml
recommendation:
  action: "Disclose proactively"
  reasoning: "Transparency builds trust"
  disclosure: "Brief acknowledgment in methods or acknowledgments"
```

### Situation 2: Journal Prohibits AI

```yaml
recommendation:
  action: "Do not use AI for that submission"
  alternative: "Use AI for other purposes (practice, outlining)"
  note: "Humanization cannot make prohibited AI use acceptable"
```

### Situation 3: Unsure About Policy

```yaml
recommendation:
  action: "Ask the editor"
  email_template: |
    Dear Editor,
    I am preparing a submission for [Journal] and would like to clarify
    your policy on AI writing assistance. Specifically, I have used AI
    tools for [specific use]. Is disclosure required, and if so, in what
    format?
    Thank you for your guidance.
```

### Situation 4: Reviewer Questions AI Use

```yaml
recommendation:
  action: "Respond honestly"
  if_used: "Acknowledge and explain the nature of assistance"
  if_not_used: "State clearly that AI was not used"
  note: "Deception to reviewers is serious misconduct"
```

---

## AI Detection Reality Check

### Current State of Detection

```yaml
reality:
  - "Detection tools exist but are imperfect"
  - "False positives affect non-native speakers"
  - "Detection technology continues to improve"
  - "No humanization guarantees undetectability"
  - "Journals increasingly use detection tools"
```

### Why Evasion is Futile

```yaml
reasons:
  - "Detection will improve faster than evasion"
  - "Reviewers are becoming AI-aware"
  - "Patterns beyond text (metadata, behavior) reveal AI use"
  - "Academic communities are small—reputation matters"
  - "Discovery after publication is worse than disclosure"
```

### Better Approach

```yaml
strategy:
  - "Use AI ethically and transparently"
  - "Focus on the quality of your research"
  - "Let AI improve expression, not replace thinking"
  - "Disclose when appropriate"
  - "Develop your own writing skills alongside AI use"
```

---

## Research Coordinator's Ethical Commitments

### What We Build Into the System

```yaml
design_principles:
  - "Checkpoints require human approval"
  - "Transformations preserve meaning, not hide authorship"
  - "Disclosure reminders at key points"
  - "Audit trails for transparency"
  - "No claims of undetectability"
```

### What We Encourage

```yaml
encouraged_behaviors:
  - "Understanding what AI contributes vs. what you contribute"
  - "Using AI as a tool, not a replacement for thinking"
  - "Developing writing skills alongside AI assistance"
  - "Transparent acknowledgment of AI use"
  - "Following institutional and journal policies"
```

---

## Checkpoint: Ethics Reminder

When humanization is requested, the system shows:

```
┌─────────────────────────────────────────────────────────────┐
│  📋 Ethics Reminder                                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Humanization helps express your ideas naturally.           │
│  It does not make AI use "undetectable."                   │
│                                                             │
│  Before proceeding:                                         │
│  □ I have checked my institution's AI policy               │
│  □ I have checked the target journal's AI policy           │
│  □ I understand that disclosure may be required            │
│  □ The research and ideas are my original work             │
│                                                             │
│  [Continue] [View Policies] [Learn More]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Resources

### Policy Databases

- **COPE**: Committee on Publication Ethics guidelines
- **ICMJE**: International Committee of Medical Journal Editors
- **Journal websites**: Individual journal AI policies

### Guidance Documents

- Nature: "Tools such as ChatGPT threaten transparent science" (2023)
- Science: "ChatGPT is fun, but not an author" (2023)
- COPE: "Authorship and AI tools" (2023)

### Institutional Resources

- Your university's academic integrity office
- Research ethics board
- Library research support services

---

## Summary: The Ethical Path

```
1. USE AI ethically
   → As a tool to improve expression of your ideas

2. VERIFY accuracy
   → Check all AI-generated content

3. DISCLOSE appropriately
   → Follow policies; when in doubt, disclose

4. MAINTAIN integrity
   → The research and ideas must be yours

5. HUMANIZE for clarity
   → Not to deceive, but to communicate better
```

---

## Version History

- v1.0.0: Initial ethics framework for Diverga v6.1 humanization features
