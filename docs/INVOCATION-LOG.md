# Invocation Log

## Decision

LongTable records role and panel invocations in `.longtable/state.json`.

This is the next step after provider-native skill installation. Skills make
LongTable easier to call, but invocation records make those calls inspectable
after the session.

## What Gets Recorded

The first implemented path is panel planning:

```bash
longtable panel --prompt "Review this methods section." --json
```

When this command runs inside a LongTable project workspace, LongTable appends an
`InvocationRecord` to:

```text
.longtable/state.json
```

The record includes:

- `InvocationIntent`: what the user asked for
- `PanelPlan`: which roles were selected and why
- `PanelResult`: current planned panel result
- provider and execution surface
- degradation/fallback reason when native team execution is not used

`CURRENT.md` is regenerated after the append and shows recent LongTable
invocations.

## Why This Matters

This closes the gap between a natural-language skill trigger and durable project
memory.

Without invocation records, a panel call only exists in the conversation. With
invocation records, the project can later answer:

- Which roles were consulted?
- Was this a native team execution or sequential fallback?
- What decision or checkpoint should this invocation connect to?
- Did a later claim depend on a previous panel result?

## Current Scope

Implemented:

- panel invocation logging
- `CURRENT.md` recent invocation summary
- backward-compatible state loading for older `.longtable/state.json` files

Not yet implemented:

- logging every natural-language skill activation
- appending answered `QuestionRecord` entries
- linking invocation records to final `DecisionRecord` entries
- storing native provider subagent transcripts

The next expansion should connect checkpoint questions and decisions to the
invocation that produced them.
