# LongTable 0.1.23 Release Notes

## Summary

This patch fixes the Codex granular approval policy emitted by LongTable when
Codex UI Researcher Checkpoints are enabled. It preserves the `0.1.22`
architecture: MCP elicitation remains an opt-in transport for form-style
Researcher Checkpoints, while `QuestionRecord -> DecisionRecord` and numbered
fallback remain the durable LongTable contract.

## Fixed

- Replaced the incomplete Codex approval policy emitted for
  `--checkpoint-ui interactive|strong`.
- The previous `0.1.22` snippet set only `mcp_elicitations = true`, which caused
  current Codex config parsing to fail with a missing `sandbox_approval` field.
- The emitted config now includes the required granular fields:

```toml
approval_policy = { granular = { sandbox_approval = false, rules = false, mcp_elicitations = true } }
```

## Preserved

- `longtable setup --provider codex --surfaces skills_mcp --checkpoint-ui strong`
  remains the opt-in path for Codex UI Researcher Checkpoints.
- `longtable mcp install --provider codex --checkpoint-ui strong --write`
  still writes the LongTable MCP server block and MCP elicitation approval.
- `elicit_question` still creates a durable `QuestionRecord` before attempting
  MCP elicitation.
- If elicitation is unavailable, declined, canceled, or unsupported, LongTable
  still returns numbered fallback transport and expects `longtable decide`.

## Verification

```bash
npm run test
npm run pack:check
codex debug prompt-input -c 'approval_policy={granular={sandbox_approval=false,rules=false,mcp_elicitations=true}}' test
node packages/longtable/dist/cli.js mcp install --provider codex --checkpoint-ui strong
```
