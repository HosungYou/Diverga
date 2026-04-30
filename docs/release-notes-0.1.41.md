# LongTable 0.1.41 Release Notes

## Summary

LongTable 0.1.41 is a follow-up patch to 0.1.40. It keeps the
advisory-first question harness behavior and fixes MCP version reporting.

## Runtime Changes

- `@longtable/mcp` now reads its self-test/server version from its own
  `package.json` instead of a hardcoded string.
- `npx -y @longtable/mcp@0.1.41 --self-test` reports `version: "0.1.41"`.

## Verification

- `npm run release:check`
- `npx -y @longtable/mcp@0.1.41 --self-test`

## Package Alignment

- Workspace packages are aligned on version `0.1.41`.
- MCP install snippets point to `@longtable/mcp@0.1.41`.
