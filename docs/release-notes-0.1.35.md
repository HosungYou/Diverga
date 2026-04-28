# LongTable 0.1.35 Release Notes

## Documentation

- Clarifies that Codex and Claude Code use the shell working directory at
  process start as the provider session workspace.
- Documents `codex -C "<research-folder>"` as the direct way to start Codex from
  a target project folder without changing the current shell directory first.
- Adds macOS/Linux and Windows PowerShell examples for project folder paths.
- Notes that changing directories after a provider session is already running
  does not change the provider session root or rerun LongTable's `SessionStart`
  hook.

## Packaging

- Workspace packages are aligned on version `0.1.35`.
- MCP install snippets point to `@longtable/mcp@0.1.35`.
