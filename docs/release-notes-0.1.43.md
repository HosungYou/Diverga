# LongTable 0.1.43 Release Notes

## Summary

LongTable 0.1.43 tightens the Codex question harness around three failures:
noisy advisory hook output, missed high-risk research questions, and hidden
panel disagreement.

## Codex Hook Changes

- `UserPromptSubmit` no longer injects raw response-only advisory question
  bundles into hook context.
- Product/tooling prompts now correctly match the normal `LongTable` spelling,
  not only malformed autocomplete text such as `$longlongtable`.
- Advisory research prompts stay out of `QuestionRecord` state and out of hook
  context.
- Required hook context is reserved for durable Researcher Checkpoints and
  explicit unresolved blocking state.

## Research Decision Stops

- Research question/scope, theory-frame, measurement/coding-standard,
  method-design, and analysis-strategy changes are treated as high-risk
  commitment areas.
- When multiple protected areas are changed in one prompt, LongTable creates one
  grouped `Research direction change` checkpoint instead of a long questionnaire.
- The action cue no longer treats a variable phrase such as `switch to AI` as a
  request to change the research direction.
- Question opportunities are sorted by risk and importance before being
  surfaced or persisted.

## Panel And Epistemic Alignment

- Provider skills now require visible deliberation records for panel/team work:
  roles consulted, role-level claims or objections, disagreement map, decision
  options, defensible recommendation, and the exact researcher-facing question.
- Runtime guidance documents now distinguish low-risk assumptions from
  must-stop research commitments.
- Knowledge conflicts between researcher intent, AI inference, prior requests,
  and durable project state are treated as alignment risks that may require
  human clarity before closure.

## Verification

- `npm run build`
- `npm run smoke:hooks`
- `longtable audit questions --json`
