# Developer Notes

## SKILL.md Format for Claude Code Plugins

When creating skills for Claude Code plugins, the `SKILL.md` frontmatter must follow a specific format.

### Correct Format

```yaml
---
name: skill-name
description: |
  Brief description of the skill.
  Include triggers and additional info as text here.
version: "1.0.0"
---

# Skill Title

Markdown content follows...
```

### Rules

1. Only `name`, `description`, `version` fields are supported
2. Put extra metadata (triggers, dependencies) in description text
3. Quote version numbers: `"1.0.0"` not `1.0.0`
4. Do NOT use `command` field -- it breaks skill recognition

### Fields That Break Parsing

These frontmatter fields cause "Unknown skill" errors:
- `command` -- BREAKS parsing
- `category` -- Not supported
- `model_tier` -- Not supported
- `triggers` (as array) -- Not supported
- `dependencies` (as object) -- Not supported

---

## Plugin Directory Structure

```
~/.claude/plugins/diverga/
+-- .claude/
|   +-- skills/
|       +-- memory/
|       |   +-- SKILL.md
|       +-- research-coordinator/
|       |   +-- SKILL.md
|       +-- ...
+-- .claude-plugin/
|   +-- marketplace.json
+-- CLAUDE.md
```

---

## Symlink-Based Development (Recommended for Plugin Authors)

### The Problem

Claude Code plugin은 파일을 **3곳에 복사**해서 사용합니다:

```
~/.claude/plugins/diverga/              ← Plugin 디렉토리
~/.claude/plugins/cache/diverga/.../    ← Plugin 캐시 (스킬 로딩용)
~/.claude/skills/diverga-*/             ← 개별 스킬 디렉토리 (35+개)
```

Git repo에서 파일을 수정해도 이 3곳에는 반영되지 않아서, 매번 수동으로 복사해야 합니다. 스킬이 35개면 35번 복사해야 합니다.

### The Solution: Symlink

**Symlink (심볼릭 링크)** = 파일 바로가기. 원본을 가리키는 포인터입니다.

```
일반 복사:     원본 수정 → 복사본 변하지 않음 (별도 파일)
Symlink:       원본 수정 → 링크도 즉시 반영 (같은 파일을 가리키므로)
```

Git repo를 유일한 소스로 두고, 나머지 3곳을 모두 symlink로 연결하면 파일을 한 곳에서만 관리할 수 있습니다.

### Setup

```bash
REPO="/path/to/your/Diverga"  # Git repo 경로

# 1. Plugin 디렉토리 → repo
rm -rf ~/.claude/plugins/diverga
ln -s "$REPO" ~/.claude/plugins/diverga

# 2. Cache 디렉토리 → repo
rm -rf ~/.claude/plugins/cache/diverga/diverga/<VERSION>
ln -s "$REPO" ~/.claude/plugins/cache/diverga/diverga/<VERSION>

# 3. Skills 디렉토리 → repo/skills/
for skill_dir in "$REPO"/skills/*/; do
  skill_name=$(basename "$skill_dir")
  rm -rf ~/.claude/skills/diverga-${skill_name}
  ln -s "$skill_dir" ~/.claude/skills/diverga-${skill_name}
done
```

### After Setup

```
Git Repo (단일 소스)
/path/to/Diverga/
    │
    ├── push → GitHub (다른 사용자는 일반 복사본을 받음)
    │
    ├── symlink ← ~/.claude/plugins/diverga/
    ├── symlink ← ~/.claude/plugins/cache/diverga/.../
    └── skills/
        ├── a1/    ← symlink ← ~/.claude/skills/diverga-a1/
        ├── setup/ ← symlink ← ~/.claude/skills/diverga-setup/
        └── ...
```

**Workflow:**
1. Repo에서 SKILL.md 수정 → 즉시 반영 (Claude Code 재시작 필요 없음)
2. `git push` → GitHub 업데이트
3. 끝. 수동 복사 불필요.

### Tips

#### 1. `plugin.json` 이중 관리

Repo에 `plugin.json`이 두 곳에 있습니다:
- `plugin.json` (루트) ← Plugin 시스템이 읽는 파일
- `.claude-plugin/plugin.json` ← Marketplace 등록용

**버전이나 내용을 바꿀 때 두 파일 모두 수정하세요.** 또는 `.claude-plugin/plugin.json`을 제거하고 루트 파일 하나만 유지해도 됩니다.

#### 2. 버전 올릴 때 Cache 경로 업데이트

Cache 경로에 버전 번호가 포함됩니다:
```
~/.claude/plugins/cache/diverga/diverga/11.1.1/
                                         ^^^^^
```

버전을 `11.2.0`으로 올리면:
```bash
# 기존 symlink 제거 후 새 경로로 재생성
rm ~/.claude/plugins/cache/diverga/diverga/11.1.1
mkdir -p ~/.claude/plugins/cache/diverga/diverga/
ln -s "$REPO" ~/.claude/plugins/cache/diverga/diverga/11.2.0
```

#### 3. 새 스킬 추가 시

Repo에 `skills/new-skill/SKILL.md`를 만든 후:
```bash
ln -s "$REPO/skills/new-skill" ~/.claude/skills/diverga-new-skill
```

#### 4. Repo가 외장 디스크에 있다면

Symlink 대상이 분리 가능한 디스크에 있으면, 디스크 미연결 시 plugin이 작동하지 않습니다. **항상 연결된 디스크**에서만 사용하세요.

#### 5. `.git/`, `.research/` 등 추가 파일

Symlink로 repo 전체를 연결하면 `.git/`, `.research/`, `.omc/` 등 plugin에 불필요한 디렉토리도 보입니다. Claude Code는 이를 무시하므로 문제없습니다.

#### 6. `plugin update` / `plugin install` 주의

Plugin 시스템의 update/install 명령이 symlink를 일반 디렉토리로 덮어쓸 수 있습니다. 업데이트 후 symlink가 깨졌는지 확인하세요:
```bash
file ~/.claude/plugins/diverga
# 정상: symbolic link to /path/to/Diverga
# 비정상: directory
```

#### 7. 다른 사용자에게 영향 없음

Symlink는 로컬 머신에만 존재합니다. 다른 사용자가 GitHub에서 `plugin install`하면 일반 복사본을 받습니다. Repo에 커밋된 파일 중 symlink가 있으면 (예: `plugin.json`) **실제 파일로 변환**하세요. Git symlink는 Windows에서 관리자 권한이 필요합니다.

### Testing Skills (with Symlink)

```bash
# Symlink 사용 시: repo에서 직접 수정하면 끝
vim skills/setup/SKILL.md   # 수정 즉시 반영

# 새 세션에서 테스트
claude   # Claude Code 시작
/diverga:setup   # 수정된 스킬 확인
```

### Testing Skills (without Symlink)

```bash
# Symlink 미사용 시: 수동 복사 필요
cp skills/your-skill/SKILL.md \
   ~/.claude/skills/diverga-your-skill/SKILL.md
cp skills/your-skill/SKILL.md \
   ~/.claude/plugins/cache/diverga/diverga/<VERSION>/skills/your-skill/SKILL.md

# Claude Code 재시작
/exit
```

---

## Project File Structure

```
project-root/
+-- .research/                  # System files (hidden - internal use only)
|   +-- hud-state.json          # HUD cache
|   +-- priority-context.md     # Compressed context (500 chars)
|   +-- sessions/               # Session records
|
+-- research/                   # Researcher-visible files (public)
|   +-- project-state.yaml      # Project metadata
|   +-- decision-log.yaml       # All research decisions
|   +-- checkpoints.yaml        # Checkpoint states
|   +-- baselines/              # Stable research foundations
|   +-- changes/
|       +-- current/            # Active work
|       +-- archive/            # Completed stages
|
+-- docs/                       # Auto-generated documentation
```

**Migration Note**: Existing projects with files in `.research/` are automatically migrated to `research/` on first access. System-only files remain in `.research/`.

---

## MCP Server Architecture

```
diverga-server.js --> tool-registry.js (16 tools)
      |
      +-- checkpoint-server   memory-server     comm-server
      |        |                    |                |
      |   YAML (default)      YAML (default)    JSON (default)
      |        |                    |                |
      +-- sqlite-servers.js (WAL mode, DIVERGA_BACKEND=sqlite)
```

### Dual Backend

| Backend | Env Var | Description |
|---------|---------|-------------|
| YAML (default) | `DIVERGA_BACKEND=yaml` | Human-readable, backward-compatible |
| SQLite (opt-in) | `DIVERGA_BACKEND=sqlite` | WAL-mode ACID transactions for parallel execution |

First SQLite startup auto-migrates existing YAML/JSON data.

---

## Version History

See `docs/CHANGELOG.md` for full version history.
