# LongTable 0.1.37 Release Notes

## Hook Behavior

- `Stop` hooks no longer block only because a required Researcher Checkpoint is
  pending. This prevents Codex from re-entering the model instead of waiting for
  the researcher to answer the checkpoint.
- Pending-checkpoint hook context now explicitly says not to choose or record an
  answer unless the researcher provides the selection.
- Generated required checkpoint context carries the same researcher-agency
  instruction when multiple checkpoint records are surfaced.

## Provider Skills

- Codex and Claude skill guidance now says to ask for the researcher's selection
  and wait before recording `longtable decide`.

## Packaging

- Workspace packages are aligned on version `0.1.37`.
- MCP install snippets point to `@longtable/mcp@0.1.37`.
