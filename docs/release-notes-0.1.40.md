# LongTable 0.1.40 Release Notes

## Summary

LongTable 0.1.40 makes the question harness advisory-first. The runtime now
separates "LongTable noticed a useful question" from "LongTable must stop and
write a required Researcher Checkpoint."

## Runtime Changes

- Codex `UserPromptSubmit` hooks no longer create required checkpoints for
  LongTable product, hook, MCP, skill, release, documentation, or setup prompts.
- Research exploration and review prompts can surface response-only advisory
  questions without writing `.longtable/state.json`.
- Required `QuestionRecord` creation is restricted to research commitment
  prompts with closure cues such as finalizing, applying, submitting, recording,
  or freezing a research decision.
- Protected-decision closure checks now require a research-domain commitment
  cue; vague execution prompts such as "진행해 줘" are not enough by themselves.
- CLI automatic follow-up generation follows the same required-only gate.

## Classifier Changes

- Product/tooling prompts are classified as `product_runtime_guidance` and stay
  advisory.
- Knowledge-gap and tacit-assumption triggers are advisory by default.
- Commitment-family triggers only outrank exploration when a commitment cue is
  present.
- Panel disagreement collapse and external-facing submission remain eligible for
  required checkpoints.

## Regression Coverage

- Added hook smoke coverage for:
  - response-only research advisory prompts
  - required construct-boundary commitment prompts
  - documentation/procedure implementation prompts
  - product UX and skill-surface prompts
- Added checkpoint smoke coverage for product policy prompts and advisory
  exploration behavior.

## Verification

- `npm run release:check`
- `npm run smoke:hooks`
- `npm run smoke:checkpoints`
- `npm run smoke:question-audit`

## Package Alignment

- Workspace packages are aligned on version `0.1.40`.
- MCP install snippets point to `@longtable/mcp@0.1.40`.
