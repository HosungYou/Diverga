# LongTable 0.1.44 Release Notes

## Summary

LongTable 0.1.44 expands `$longtable-interview` from a short First Research
Shape closure into a fuller Research Specification workflow. The new layer keeps
the early handle, but gives later agents a durable specification for scope,
construct ontology, theory framing, coding, method, evidence/access, and
epistemic alignment.

## Research Specification Workflow

- Adds a `ResearchSpecification` state model to `@longtable/core` and
  `@longtable/cli`.
- Stores Research Specifications in `.longtable/state.json`,
  `.longtable/current-session.json`, and regenerated `CURRENT.md`.
- Keeps First Research Shape as the shorter handle layer rather than replacing
  it.
- Renders a `Research Specification Preview` before final confirmation so the
  researcher can inspect what is about to become durable project state.

## MCP Surface

- Adds `summarize_research_specification` for storing the fuller specification
  after enough interview context exists.
- Adds `read_research_specification` for retrieving the current specification
  and preview text.
- Adds `confirm_research_specification` for MCP form confirmation with options
  to save, ask one more question, revise a section, or keep the draft open.
- Keeps `confirm_first_research_shape` for cases where the researcher
  intentionally stops at the shorter handle layer.

## Provider Skills

- Updates Codex and Claude `$longtable-interview` skill guidance to create the
  Research Specification after `summarize_interview`.
- Makes the Research Specification checkpoint the final substantive interview
  confirmation point.
- Preserves one-question-at-a-time interview behavior and content-based closure
  readiness.

## Documentation

- Updates README, MCP documentation, command-surface documentation, and runtime
  boundary audit notes to describe the Research Specification layer.
- Documents that `CURRENT.md` now renders Research Specification state when
  present.

## Verification

- `npm run test`
- `npm run release:check`
- MCP self-test includes `summarize_research_specification`,
  `read_research_specification`, and `confirm_research_specification`
- Temporary workspace smoke test confirmed Research Specification rendering in
  `CURRENT.md`

## Package Alignment

- Workspace packages are aligned on version `0.1.44`.
- Internal `@longtable/*` dependencies are pinned to `0.1.44`.
