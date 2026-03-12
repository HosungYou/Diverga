#!/usr/bin/env python3
"""
Tests for Checkpoint System
==============================

Validates the human checkpoint system:
- All checkpoints are defined (at least 5 REQUIRED)
- Required checkpoints include CP_PARADIGM and CP_METHODOLOGY
- Checkpoint enforcement via prereq-enforcer hook
- Checkpoint levels (REQUIRED/RECOMMENDED/OPTIONAL) are documented

Usage:
    pytest tests/test_checkpoint_system.py -v
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent
CLAUDE_MD = BASE_DIR / "CLAUDE.md"
MEMORY_SKILL_PATH = BASE_DIR / "skills" / "memory" / "SKILL.md"
SETUP_SKILL_PATH = BASE_DIR / "skills" / "setup" / "SKILL.md"
CONFIG_PATH = BASE_DIR / "config" / "diverga-config.json"


def _load_all_checkpoint_sources() -> str:
    """Load all files that define or reference checkpoints."""
    sources = []
    for path in [CLAUDE_MD, MEMORY_SKILL_PATH]:
        if path.exists():
            sources.append(path.read_text(encoding="utf-8"))
    return "\n".join(sources)


# Known checkpoint IDs (v11.1 — 5 REQUIRED + 4 RECOMMENDED)
REQUIRED_CHECKPOINTS = [
    "CP_RESEARCH_DIRECTION",
    "CP_PARADIGM_SELECTION",
    "CP_METHODOLOGY_APPROVAL",
    "SCH_DATABASE_SELECTION",
    "SCH_SCREENING_CRITERIA",
]

RECOMMENDED_CHECKPOINTS = [
    "CP_VS_001",
    "CP_VS_003",
    "CP_THEORY_SELECTION",
    "SCH_API_KEY_VALIDATION",
]


class TestCheckpointDefinitions:
    """Tests that all checkpoints are properly defined."""

    def test_at_least_5_required_checkpoints(self):
        """At least 5 REQUIRED checkpoints must be defined."""
        content = _load_all_checkpoint_sources()
        found = [cp for cp in REQUIRED_CHECKPOINTS if cp in content]
        assert len(found) >= 5, (
            f"Expected at least 5 REQUIRED checkpoints, found {len(found)}: {found}"
        )

    def test_required_checkpoints_are_defined(self):
        """All 5 REQUIRED checkpoint IDs must appear in documentation."""
        content = _load_all_checkpoint_sources()
        missing = [cp for cp in REQUIRED_CHECKPOINTS if cp not in content]
        assert not missing, (
            f"Missing REQUIRED checkpoint definitions: {missing}"
        )

    def test_setup_mentions_checkpoints(self):
        """Setup SKILL.md should reference checkpoints."""
        content = SETUP_SKILL_PATH.read_text(encoding="utf-8")
        assert "checkpoint" in content.lower(), (
            "Setup SKILL.md should mention checkpoints"
        )


class TestRequiredCheckpoints:
    """Tests that mandatory checkpoints are correctly identified."""

    def test_cp_paradigm_is_required(self):
        """CP_PARADIGM_SELECTION must be in the required checkpoints."""
        content = _load_all_checkpoint_sources()
        assert "CP_PARADIGM_SELECTION" in content, (
            "CP_PARADIGM_SELECTION checkpoint must be defined"
        )

    def test_cp_methodology_is_required(self):
        """CP_METHODOLOGY_APPROVAL must be defined."""
        content = _load_all_checkpoint_sources()
        assert "CP_METHODOLOGY_APPROVAL" in content, (
            "CP_METHODOLOGY_APPROVAL checkpoint must be defined"
        )

    def test_config_has_cp_paradigm_in_required(self):
        """diverga-config.json must list CP_PARADIGM in required checkpoints."""
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        required = data.get("human_checkpoints", {}).get("required", [])
        has_paradigm = any("PARADIGM" in cp for cp in required)
        assert has_paradigm, (
            f"Config required checkpoints {required} must include CP_PARADIGM"
        )

    def test_config_has_cp_methodology_in_required(self):
        """diverga-config.json must list CP_METHODOLOGY in required checkpoints."""
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        required = data.get("human_checkpoints", {}).get("required", [])
        has_methodology = any("METHODOLOGY" in cp for cp in required)
        assert has_methodology, (
            f"Config required checkpoints {required} must include CP_METHODOLOGY"
        )


class TestCheckpointProtocol:
    """Tests that checkpoint protocol rules are properly documented."""

    @pytest.fixture()
    def claude_content(self) -> str:
        """Load CLAUDE.md content."""
        return CLAUDE_MD.read_text(encoding="utf-8")

    def test_stop_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include enforcement rules."""
        assert (
            "STOP" in claude_content
            or "hard block" in claude_content.lower()
            or "cannot run" in claude_content.lower()
        ), "Checkpoint protocol must document enforcement behavior"

    def test_wait_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include waiting for human approval."""
        content_lower = claude_content.lower()
        assert "wait" in content_lower or "human" in content_lower, (
            "Checkpoint protocol must document human approval requirement"
        )

    def test_do_not_proceed_rule_documented(self, claude_content: str):
        """Checkpoint protocol must include enforcement rules."""
        assert (
            "DO NOT proceed" in claude_content
            or "do not proceed" in claude_content.lower()
            or "Cannot proceed" in claude_content
            or "cannot run" in claude_content.lower()
            or "hard block" in claude_content.lower()
        ), "Checkpoint protocol must specify enforcement behavior"

    def test_enforcement_rules_documented(self, claude_content: str):
        """Checkpoint enforcement must be documented (hook or protocol)."""
        assert (
            "DO NOT assume" in claude_content
            or "do not assume" in claude_content.lower()
            or "hard block" in claude_content.lower()
            or "cannot run" in claude_content.lower()
            or "Hook Enforcement" in claude_content
        ), "Checkpoint enforcement rules must be documented"

    def test_checkpoint_enforcement_section_exists(self, claude_content: str):
        """CLAUDE.md must contain checkpoint enforcement documentation."""
        assert (
            "Hook Enforcement" in claude_content
            or "CHECKPOINT PROTOCOL" in claude_content
            or "Checkpoint" in claude_content
        ), "CLAUDE.md must contain checkpoint enforcement documentation"


class TestCheckpointLevels:
    """Tests that checkpoint levels are properly defined."""

    def test_required_level_defined(self):
        """REQUIRED checkpoint level must be defined."""
        content = _load_all_checkpoint_sources()
        assert "REQUIRED" in content, (
            "REQUIRED checkpoint level must be defined"
        )

    def test_recommended_level_defined(self):
        """RECOMMENDED checkpoint level must be defined."""
        content = _load_all_checkpoint_sources()
        assert "RECOMMENDED" in content, (
            "RECOMMENDED checkpoint level must be defined"
        )

    def test_optional_level_defined(self):
        """OPTIONAL checkpoint level must be defined."""
        content = _load_all_checkpoint_sources()
        assert "OPTIONAL" in content or "pass through" in content.lower(), (
            "OPTIONAL checkpoint level or pass-through behavior must be defined"
        )

    def test_required_level_has_stop_behavior(self):
        """REQUIRED level must specify that the system blocks/stops."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        required_section = re.search(
            r"REQUIRED.*?(STOP|block|cannot|CANNOT)|"
            r"(STOP|block|cannot|CANNOT).*?REQUIRED",
            content,
            re.DOTALL | re.IGNORECASE,
        )
        assert required_section is not None, (
            "REQUIRED checkpoint level must specify blocking/stop behavior"
        )

    def test_checkpoint_levels_documented(self):
        """Checkpoint levels should have visual or text indicators documented."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        has_required = "REQUIRED" in content
        has_recommended = "RECOMMENDED" in content
        has_optional = "OPTIONAL" in content or "pass through" in content.lower()

        assert has_required, "REQUIRED checkpoint level should be documented"
        assert has_recommended, "RECOMMENDED checkpoint level should be documented"
        assert has_optional, "OPTIONAL or pass-through behavior should be documented"


class TestCheckpointInMemorySystem:
    """Tests that the memory system properly integrates with checkpoints."""

    @pytest.fixture()
    def memory_content(self) -> str:
        """Load memory SKILL.md content."""
        return MEMORY_SKILL_PATH.read_text(encoding="utf-8")

    def test_memory_tracks_checkpoint_status(self, memory_content: str):
        """Memory system must track checkpoint completion status."""
        content_lower = memory_content.lower()
        assert (
            "status" in content_lower
            and ("completed" in content_lower or "pending" in content_lower)
        ), "Memory system must track checkpoint status (completed/pending)"

    def test_memory_records_checkpoint_timestamp(self, memory_content: str):
        """Memory system must record timestamps for checkpoint events."""
        assert (
            "timestamp" in memory_content.lower()
            or "completed_at" in memory_content
            or "triggered_at" in memory_content
        ), "Memory system must record timestamps for checkpoints"

    def test_memory_links_checkpoints_to_decisions(self, memory_content: str):
        """Memory system must link checkpoints to decision IDs."""
        assert (
            "decision_id" in memory_content
            or "decision" in memory_content.lower()
        ), "Memory system must link checkpoints to decisions"

    def test_memory_defines_checkpoint_stages(self, memory_content: str):
        """Memory system must define checkpoint stages (foundation, design, etc.)."""
        stages = ["foundation", "design", "planning", "execution"]
        found = [s for s in stages if s in memory_content.lower()]
        assert len(found) >= 3, (
            f"Memory system should define at least 3 checkpoint stages. "
            f"Found: {found}"
        )


class TestCheckpointEnforcement:
    """Tests that checkpoint enforcement rules are clearly stated."""

    def test_enforcement_behavior_documented(self):
        """Documentation must state enforcement behavior for checkpoints."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert (
            "DO NOT proceed" in content
            or "DO NOT assume" in content
            or "NEVER" in content
            or "cannot run" in content.lower()
            or "hard block" in content.lower()
            or "continue: false" in content
        ), "Must document checkpoint enforcement behavior"

    def test_emphasis_pattern(self):
        """Documentation must use emphasis patterns for checkpoint enforcement."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert "ALWAYS" in content or "MUST" in content or "REQUIRED" in content, (
            "Documentation must use emphasis (ALWAYS/MUST/REQUIRED) for enforcement"
        )

    def test_human_centered_principle(self):
        """Documentation must state the human-centered principle."""
        content = CLAUDE_MD.read_text(encoding="utf-8")
        assert (
            "Human" in content
            and ("decide" in content.lower() or "decision" in content.lower())
        ), "Documentation must state the human-centered decision principle"
