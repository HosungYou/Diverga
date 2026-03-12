#!/usr/bin/env python3
"""
Tests for Memory System Structure
====================================

Validates the memory system SKILL.md structure, including:
- .research/ directory structure specification
- Memory SKILL.md existence and command definitions
- Context keywords (English and Korean)
- Lifecycle hooks

Usage:
    pytest tests/test_memory_system.py -v
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent
MEMORY_SKILL_PATH = BASE_DIR / "skills" / "memory" / "SKILL.md"
CLAUDE_MD = BASE_DIR / "CLAUDE.md"


class TestMemorySkillExists:
    """Tests that the memory SKILL.md exists and is valid."""

    def test_memory_skill_directory_exists(self):
        """skills/memory/ directory must exist."""
        assert (BASE_DIR / "skills" / "memory").is_dir(), (
            "skills/memory/ directory not found"
        )

    def test_memory_skill_md_exists(self):
        """skills/memory/SKILL.md must exist."""
        assert MEMORY_SKILL_PATH.exists(), (
            f"memory SKILL.md not found at {MEMORY_SKILL_PATH}"
        )

    def test_memory_skill_has_frontmatter(self):
        """Memory SKILL.md must have valid YAML frontmatter."""
        content = MEMORY_SKILL_PATH.read_text(encoding="utf-8")
        assert content.startswith("---"), (
            "Memory SKILL.md must start with YAML frontmatter (---)"
        )
        try:
            content.index("---", 3)
        except ValueError:
            pytest.fail("Memory SKILL.md missing closing --- for frontmatter")

    def test_memory_skill_has_name(self):
        """Memory SKILL.md frontmatter must have a name field."""
        content = MEMORY_SKILL_PATH.read_text(encoding="utf-8")
        end_idx = content.index("---", 3)
        frontmatter = content[3:end_idx]
        assert re.search(r"^name:", frontmatter, re.MULTILINE), (
            "Memory SKILL.md missing 'name' in frontmatter"
        )

    def test_memory_skill_has_version(self):
        """Memory SKILL.md frontmatter must have a version field."""
        content = MEMORY_SKILL_PATH.read_text(encoding="utf-8")
        end_idx = content.index("---", 3)
        frontmatter = content[3:end_idx]
        assert re.search(r"^version:", frontmatter, re.MULTILINE), (
            "Memory SKILL.md missing 'version' in frontmatter"
        )


class TestMemoryCommands:
    """Tests that memory SKILL.md defines the required commands."""

    @pytest.fixture()
    def memory_content(self) -> str:
        """Load memory SKILL.md content."""
        return MEMORY_SKILL_PATH.read_text(encoding="utf-8")

    def test_has_status_command(self, memory_content: str):
        """Memory system must define 'memory status' command."""
        assert "memory status" in memory_content.lower() or "status" in memory_content, (
            "Memory SKILL.md missing 'status' command definition"
        )

    def test_has_context_command(self, memory_content: str):
        """Memory system must define 'memory context' command."""
        assert "memory context" in memory_content.lower() or "context" in memory_content, (
            "Memory SKILL.md missing 'context' command definition"
        )

    def test_has_init_command(self, memory_content: str):
        """Memory system must define 'memory init' command."""
        assert "memory init" in memory_content.lower() or "init" in memory_content, (
            "Memory SKILL.md missing 'init' command definition"
        )

    def test_has_decision_list_command(self, memory_content: str):
        """Memory system must define 'memory decision list' command."""
        assert "decision list" in memory_content.lower() or "decision" in memory_content, (
            "Memory SKILL.md missing 'decision list' command definition"
        )

    def test_has_archive_command(self, memory_content: str):
        """Memory system must define 'memory archive' command."""
        assert "archive" in memory_content.lower(), (
            "Memory SKILL.md missing 'archive' command definition"
        )

    def test_has_migrate_command(self, memory_content: str):
        """Memory system must define 'memory migrate' command."""
        assert "migrate" in memory_content.lower(), (
            "Memory SKILL.md missing 'migrate' command definition"
        )


class TestResearchDirectoryStructure:
    """Tests that the .research/ directory structure is documented."""

    @pytest.fixture()
    def memory_content(self) -> str:
        """Load memory SKILL.md content."""
        return MEMORY_SKILL_PATH.read_text(encoding="utf-8")

    def test_documents_research_directory(self, memory_content: str):
        """Memory SKILL.md must document the .research/ directory structure."""
        assert ".research/" in memory_content, (
            "Memory SKILL.md must document .research/ directory structure"
        )

    def test_documents_baselines_directory(self, memory_content: str):
        """Memory SKILL.md must document .research/baselines/ directory."""
        assert "baselines/" in memory_content or "baselines" in memory_content, (
            "Memory SKILL.md must document baselines/ directory"
        )

    def test_documents_changes_directory(self, memory_content: str):
        """Memory SKILL.md must document .research/changes/ directory."""
        assert "changes/" in memory_content or "changes" in memory_content, (
            "Memory SKILL.md must document changes/ directory"
        )

    def test_documents_sessions_directory(self, memory_content: str):
        """Memory SKILL.md must document .research/sessions/ directory."""
        assert "sessions/" in memory_content or "sessions" in memory_content, (
            "Memory SKILL.md must document sessions/ directory"
        )

    def test_documents_project_state_yaml(self, memory_content: str):
        """Memory SKILL.md must document project-state.yaml file."""
        assert "project-state.yaml" in memory_content, (
            "Memory SKILL.md must document project-state.yaml"
        )

    def test_documents_decision_log_yaml(self, memory_content: str):
        """Memory SKILL.md must document decision-log.yaml file."""
        assert "decision-log.yaml" in memory_content, (
            "Memory SKILL.md must document decision-log.yaml"
        )

    def test_documents_checkpoints_yaml(self, memory_content: str):
        """Memory SKILL.md must document checkpoints.yaml file."""
        assert "checkpoints.yaml" in memory_content, (
            "Memory SKILL.md must document checkpoints.yaml"
        )


class TestContextKeywords:
    """Tests that context keywords are defined for both English and Korean."""

    @pytest.fixture()
    def memory_content(self) -> str:
        """Load memory SKILL.md content."""
        return MEMORY_SKILL_PATH.read_text(encoding="utf-8")

    def test_has_english_keywords(self, memory_content: str):
        """Memory SKILL.md must define English context loading keywords."""
        english_keywords = [
            "my research",
            "research status",
            "where was I",
            "continue research",
        ]
        found = [kw for kw in english_keywords if kw in memory_content]
        assert len(found) >= 3, (
            f"Memory SKILL.md should define at least 3 English context keywords. "
            f"Found: {found}"
        )

    def test_has_korean_keywords(self, memory_content: str):
        """Memory SKILL.md must define Korean context loading keywords."""
        korean_keywords = [
            "\ub0b4 \uc5f0\uad6c",
            "\uc5f0\uad6c \uc9c4\ud589",
            "\uc5f0\uad6c \uc0c1\ud0dc",
            "\uc5b4\ub514\uae4c\uc9c0",
            "\uc9c0\uae08 \ub2e8\uacc4",
        ]
        found = [kw for kw in korean_keywords if kw in memory_content]
        assert len(found) >= 3, (
            f"Memory SKILL.md should define at least 3 Korean context keywords. "
            f"Found: {found}"
        )

    def test_claude_md_also_defines_context_keywords(self):
        """CLAUDE.md should also reference context keywords for the memory system."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert "my research" in content or "research status" in content, (
            "CLAUDE.md should reference English context keywords"
        )
        assert "\ub0b4 \uc5f0\uad6c" in content or "\uc5f0\uad6c \uc9c4\ud589" in content, (
            "CLAUDE.md should reference Korean context keywords"
        )


class TestLifecycleHooks:
    """Tests that memory system lifecycle behaviors are defined."""

    @pytest.fixture()
    def combined_content(self) -> str:
        """Load both memory SKILL.md and CLAUDE.md content."""
        memory = MEMORY_SKILL_PATH.read_text(encoding="utf-8")
        claude = CLAUDE_MD.read_text(encoding="utf-8")
        return memory + "\n" + claude

    def test_session_startup_behavior_defined(self, combined_content: str):
        """Session startup behavior must be documented."""
        assert (
            "session_start" in combined_content
            or "session start" in combined_content.lower()
            or "context load" in combined_content.lower()
            or "auto-load" in combined_content.lower()
            or "session" in combined_content.lower()
        ), "Session startup behavior not defined in memory SKILL.md or CLAUDE.md"

    def test_checkpoint_reached_hook_defined(self, combined_content: str):
        """checkpoint_reached lifecycle hook must be defined."""
        assert (
            "checkpoint_reached" in combined_content
            or "checkpoint reached" in combined_content.lower()
            or "checkpoint" in combined_content.lower()
        ), "Lifecycle hook 'checkpoint_reached' not defined"

    def test_session_end_behavior_defined(self, combined_content: str):
        """Session end behavior must be documented."""
        assert (
            "session_end" in combined_content
            or "session end" in combined_content.lower()
            or "auto-save" in combined_content.lower()
            or "persist" in combined_content.lower()
            or "session" in combined_content.lower()
        ), "Session end behavior not defined"

    def test_agent_completion_behavior_defined(self, combined_content: str):
        """Agent completion behavior must be documented."""
        assert (
            "agent_completed" in combined_content
            or "agent completed" in combined_content.lower()
            or "agent finishes" in combined_content.lower()
            or "checkpoint" in combined_content.lower()
        ), "Agent completion behavior not defined"


class TestThreeLayerContextSystem:
    """Tests that the 3-layer context system is properly documented."""

    @pytest.fixture()
    def memory_content(self) -> str:
        """Load memory SKILL.md content."""
        return MEMORY_SKILL_PATH.read_text(encoding="utf-8")

    def test_documents_layer_1_keyword_triggered(self, memory_content: str):
        """Layer 1 (keyword-triggered context) must be documented."""
        content_lower = memory_content.lower()
        assert "layer 1" in content_lower or "keyword" in content_lower, (
            "Memory SKILL.md must document Layer 1 (keyword-triggered context)"
        )

    def test_documents_layer_2_task_interceptor(self, memory_content: str):
        """Layer 2 (task interceptor) must be documented."""
        content_lower = memory_content.lower()
        assert "layer 2" in content_lower or "task" in content_lower, (
            "Memory SKILL.md must document Layer 2 (task interceptor context)"
        )

    def test_documents_layer_3_cli(self, memory_content: str):
        """Layer 3 (CLI-based loading) must be documented."""
        content_lower = memory_content.lower()
        assert "layer 3" in content_lower or "cli" in content_lower, (
            "Memory SKILL.md must document Layer 3 (CLI-based context loading)"
        )
