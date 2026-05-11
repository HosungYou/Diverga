# LongTable 0.1.46 Release Notes

## Summary

LongTable 0.1.46 hardens `$longtable-interview` so Research Specification is
the default substantive closure artifact and First Research Shape remains only a
short handle/resume layer. The release also repairs stale Codex MCP allowlists
that could hide Research Specification tools from the provider runtime.

## Interview Closure

- Demotes First Research Shape from a default endpoint to an optional short
  handle layer.
- Updates Codex and Claude skill guidance to continue directly into Research
  Specification when a confirmed shape exists without a specification.
- Adds a Research Specification return obligation when the researcher chooses
  `ask_one_more` or `revise_section` during specification confirmation.
- Renders missing or draft Research Specification state in regenerated
  `CURRENT.md` so later agents can see that interview closure is incomplete.

## Codex MCP Repair

- Makes Codex MCP install write approval blocks for the full managed LongTable
  MCP tool set.
- Adds doctor reporting for the configured `@longtable/mcp` package version,
  missing managed tools, and missing Research Specification tools.
- Lets `doctor --fix` repair stale Codex MCP package/tool configuration while
  preserving non-LongTable config sections that were accidentally placed inside
  older LongTable markers.

## Ontology Harness Documentation

- Updates the researcher-centered engineering philosophy one-pager to treat
  Research Specification as the ontology artifact.
- Updates the runtime boundary audit with an ontology harness boundary table.
- Extends non-negotiables and philosophical audit notes around short handles,
  durable specification state, and provider UI as transport.

## Verification

- `npm test`
- `npm run release:check`
- Live local `longtable doctor --json` confirmed:
  - `@longtable/mcp@0.1.46` expected after version bump
  - no missing Research Specification MCP tools after reinstall

## Package Alignment

- Workspace packages are aligned on version `0.1.46`.
- Internal `@longtable/*` dependencies are pinned to `0.1.46`.
