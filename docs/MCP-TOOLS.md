# MCP Tools — v12.0.0

MCP server and tool reference for Diverga.

---

## Servers (.mcp.json)

| Server | Function |
|--------|----------|
| diverga | Checkpoints, memory, messaging (SQLite) |
| humanizer | AI pattern detection & transformation |
| journal | Journal intelligence (OpenAlex, Crossref) |

---

## Diverga Server Tools (16)

| Tool | Description |
|------|-------------|
| `diverga_check_prerequisites` | Verify agent prerequisites before execution |
| `diverga_mark_checkpoint` | Record checkpoint decision with rationale |
| `diverga_checkpoint_status` | Full checkpoint overview |
| `diverga_project_status` | Read project state |
| `diverga_project_update` | Update project state (deep merge) |
| `diverga_decision_add` | Record research decision |
| `diverga_decision_list` | List/filter decisions |
| `diverga_priority_read` | Read priority context |
| `diverga_priority_write` | Write priority context (500 char limit) |
| `diverga_export_yaml` | Export all state as YAML |
| `diverga_agent_register` | Register agent for messaging |
| `diverga_agent_list` | List registered agents |
| `diverga_message_send` | Send agent-to-agent message |
| `diverga_message_mailbox` | Read agent inbox |
| `diverga_message_acknowledge` | Acknowledge message receipt |
| `diverga_message_broadcast` | Broadcast to all agents |

---

## Journal MCP Tools (6)

| Tool | Description |
|------|-------------|
| `journal_search_by_field` | Search journals by research field |
| `journal_metrics` | Detailed metrics (h-index, citations, OA, APC) |
| `journal_publication_trends` | Works/citations per year |
| `journal_editor_info` | Top authors by publication count |
| `journal_compare` | Compare 2-5 journals side by side |
| `journal_special_issues` | Recent themed publications |

---

## Humanizer MCP Tools (5)

| Tool | Description |
|------|-------------|
| `humanizer_diff` | Show before/after transformation differences |
| `humanizer_discourse` | Analyze discourse patterns in text |
| `humanizer_metrics` | Compute humanization quality metrics |
| `humanizer_status` | Check humanizer pipeline status |
| `humanizer_verify` | Verify text passes AI detection thresholds |
