# LongTable

LongTable is a researcher-centered harness.

It is not meant to replace the researcher. It is meant to help the researcher ask better questions, keep uncertainty visible, preserve authorship, and maintain a durable project workspace across sessions.

This repository is the refactoring workspace and current source of truth for the next LongTable product contract.

LongTable is distributed as an npm-first product. Provider-specific surfaces such as Claude skills, Codex prompt aliases, and future MCP tools are generated adapter artifacts, not the source of truth.

## Core Flow

```mermaid
flowchart LR
    A[longtable init] --> B[Researcher profile seed]
    B --> C[longtable start]
    C --> D[Project workspace]
    D --> E[codex in project directory]
    E --> F[LongTable research conversation]
    F --> G[longtable resume]
    G --> H[CURRENT.md regenerated from state]
```

## Product Contract

LongTable is intentionally workspace-first.

- `longtable init` is the one-time global setup.
- `longtable start` creates a project workspace and memory seed.
- The real research conversation begins after opening `codex` inside that workspace.
- Claude Code and Codex should share the same LongTable semantics even when their native interaction surfaces differ.

The goal is to make the first minute clear for both novice researchers and power users.

## Start Contract

After `longtable start`, the root should stay minimal.

| Artifact | Role | Canonical? |
| --- | --- | --- |
| `AGENTS.md` | Runtime guidance for Codex | No |
| `CURRENT.md` | Human-facing current view | No, generated |
| `.longtable/project.json` | Stable project identity | Yes |
| `.longtable/current-session.json` | Current session cursor | Yes |
| `.longtable/state.json` | Layered memory state | Yes |
| `.longtable/sessions/` | Historical session snapshots | Yes |

The old root artifact set is being retired:

- `LONGTABLE.md`
- `START-HERE.md`
- `NEXT-STEPS.md`
- `SESSION-SNAPSHOT.md`

## Memory Model

LongTable separates memory into layers instead of flattening everything into one prompt.

- `explicitState`: confirmed facts and approved decisions
- `workingState`: current goal, blocker, next action, open questions
- `inferredHypotheses`: useful interpretations that still require confirmation
- `openTensions`: unresolved tradeoffs that should stay visible
- `narrativeTraces`: authorship and judgment traces that should not be flattened away

This is the core defense against false certainty around tacit knowledge.

```mermaid
flowchart TD
    A[Research session] --> B[workingState]
    A --> C[inferredHypotheses]
    A --> D[narrativeTraces]
    C -->|confirmed| E[explicitState]
    C -->|still unresolved| F[openTensions]
    D -->|supports judgment, not fact claims| F
```

## Example Workspace

```text
My-Project/
  AGENTS.md
  CURRENT.md
  .longtable/
    project.json
    current-session.json
    state.json
    sessions/
      project-name-1710000000000.json
```

## Quickstart

```bash
npm install -g @longtable/cli
longtable init --flow interview
longtable start
cd "<project-path>"
codex
```

When you return later:

```bash
cd "<project-path>"
longtable resume
codex
```

## Inside Codex

Most sessions should continue in natural language.

If you want an explicit invocation, use short text forms:

- `lt explore: <question>`
- `lt review: <claim or plan>`
- `lt panel: <object with disagreement>`
- `lt editor: <draft or positioning question>`
- `lt methods: <design or analysis plan>`

## Panel Orchestration

LongTable can create a structured research panel when disagreement matters.

```bash
longtable panel --prompt "review this methods section" --json
longtable review --role methods_critic,measurement_auditor --panel --prompt "review this methods section" --json
```

Panel orchestration is not persistent team orchestration. It creates a `PanelPlan`, asks selected research roles to produce inspectable outputs, and returns a `PanelResult`.

The stable fallback is sequential execution, so the panel contract works even when provider-native subagents or generated Claude skills are unavailable.

## Evidence And Search

LongTable should not behave like a generic web scraper.

Research search is scholar-first:

- clarify whether the researcher needs theory, empirical precedent, measurement instruments, venue fit, or citation verification
- prefer scholarly metadata sources before general web search
- produce evidence cards rather than raw link lists
- label claims as sourced fact, inference, or estimate
- verify whether a citation actually supports the claim attached to it

Planned scholarly routes include arXiv, Crossref, OpenAlex, Semantic Scholar, PubMed/NCBI, ERIC, DOAJ, and Unpaywall. These sources have different setup requirements. Some work without keys, some require a contact email or API key for reliable use.

LongTable should not call these sources on every question. It should route to scholarly search only when the user asks for literature discovery, citation verification, current publication metadata, or evidence-backed research decisions.

## Why This Shape

The current contract optimizes for:

1. successful first entry
2. minimal root artifacts
3. human-readable continuity
4. strict machine-readable state
5. visible disagreement when needed
6. evidence discipline for external claims
7. provider-neutral semantics with provider-specific native affordances

The system should feel simple at the root and structured under `.longtable/`.

## Local Validation

```bash
npm install
npm run typecheck
npm run build
```

## Packages

- `@longtable/cli`
- `@longtable/core`
- `@longtable/memory`
- `@longtable/checkpoints`
- `@longtable/setup`
- `@longtable/provider-codex`
- `@longtable/provider-claude`

## Key Docs

- [Spec](Spec.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Memory](docs/MEMORY.md)
- [Checkpointing](docs/CHECKPOINTING.md)
- [Evidence Policy](docs/EVIDENCE-POLICY.md)
- [Research Search](docs/RESEARCH-SEARCH.md)
- [Question Runtime](docs/QUESTION-RUNTIME.md)
- [LongTable Command Surface](docs/LONGTABLE-COMMAND-SURFACE.md)
- [Active Decisions](docs/ACTIVE-DECISIONS.md)
