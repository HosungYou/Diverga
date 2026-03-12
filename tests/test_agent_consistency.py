#!/usr/bin/env python3
"""
Tests for Agent System Consistency
====================================

Validates that the agent system is internally consistent:
- All agents referenced in CLAUDE.md exist as skill directories
- Model routing counts match (Opus/Sonnet/Haiku)
- Parallel execution groups reference valid agents
- Sequential pipeline agents exist

Usage:
    pytest tests/test_agent_consistency.py -v
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"
CLAUDE_MD = BASE_DIR / "CLAUDE.md"

# 24 core agent IDs (v11.1 — consolidated from 44; excludes V1-V5 VS Arena personas)
AGENT_IDS = [
    "a1", "a2", "a5",
    "b1", "b2",
    "c1", "c2", "c3", "c5",
    "d2", "d4",
    "e1", "e2", "e3",
    "f5",
    "g1", "g2", "g5", "g6",
    "i0", "i1", "i2", "i3",
    "x1",
]

# Model routing per agents.json (v11.1)
OPUS_AGENTS = [
    "a1", "a2",
    "c1", "c2", "c3",
    "e1", "e2", "e3",
    "g6",
    "i0",
    "x1",
]  # 11 agents

SONNET_AGENTS = [
    "a5",
    "b1", "b2",
    "c5",
    "d2", "d4",
    "g1", "g2", "g5",
    "i1", "i2",
]  # 11 agents

HAIKU_AGENTS = [
    "f5",
    "i3",
]  # 2 agents

# Parallel execution groups from CLAUDE.md
PARALLEL_GROUPS = {
    "Group 1: Research Design": ["a1", "a2", "a5"],
    "Group 2: Literature & Evidence": ["b1", "b2"],
    "Group 5: Publication Prep": ["g1", "g2", "g5"],
    "Group 6: Systematic Review Screening (parallel)": ["i1", "i2"],
}

# Sequential pipeline agents from CLAUDE.md
SEQUENTIAL_PIPELINES = {
    "Humanization Pipeline": ["g5", "g6", "f5"],
    "Systematic Review Pipeline": ["i0", "i1", "i2", "i3"],
}


class TestAgentDirectoryExistence:
    """Tests that all agents referenced in CLAUDE.md exist as skill directories."""

    def test_all_24_agents_have_skill_directories(self):
        """Every one of the 24 core agent IDs must have a corresponding skill directory."""
        missing = [
            aid for aid in AGENT_IDS
            if not (SKILLS_DIR / aid).is_dir()
        ]
        assert not missing, (
            f"Agent IDs referenced in CLAUDE.md but missing skill directories: {missing}"
        )

    def test_all_24_agents_have_skill_md(self):
        """Every agent skill directory must contain a SKILL.md file."""
        missing_md = [
            aid for aid in AGENT_IDS
            if (SKILLS_DIR / aid).is_dir()
            and not (SKILLS_DIR / aid / "SKILL.md").exists()
        ]
        assert not missing_md, (
            f"Agent directories missing SKILL.md: {missing_md}"
        )

    def test_claude_md_references_all_agents(self):
        """CLAUDE.md must reference all 24 core agent IDs."""
        assert CLAUDE_MD.exists(), f"CLAUDE.md not found at {CLAUDE_MD}"
        content = CLAUDE_MD.read_text(encoding="utf-8")
        content_upper = content.upper()

        unreferenced = []
        for aid in AGENT_IDS:
            # IDs appear as "A1", "B1" (uppercase) in CLAUDE.md tables
            if aid.upper() not in content_upper:
                unreferenced.append(aid)

        assert not unreferenced, (
            f"Agent IDs not referenced in CLAUDE.md: {unreferenced}"
        )


class TestModelRoutingConsistency:
    """Tests that model routing matches expected counts."""

    def test_opus_agent_count(self):
        """There must be exactly 11 Opus (HIGH tier) agents."""
        assert len(OPUS_AGENTS) == 11, (
            f"Expected 11 Opus agents, defined {len(OPUS_AGENTS)}: {OPUS_AGENTS}"
        )

    def test_sonnet_agent_count(self):
        """There must be exactly 11 Sonnet (MEDIUM tier) agents."""
        assert len(SONNET_AGENTS) == 11, (
            f"Expected 11 Sonnet agents, defined {len(SONNET_AGENTS)}: {SONNET_AGENTS}"
        )

    def test_haiku_agent_count(self):
        """There must be exactly 2 Haiku (LOW tier) agents."""
        assert len(HAIKU_AGENTS) == 2, (
            f"Expected 2 Haiku agents, defined {len(HAIKU_AGENTS)}: {HAIKU_AGENTS}"
        )

    def test_model_routing_covers_all_24_agents(self):
        """Opus + Sonnet + Haiku must total 24 agents (all core agents routed)."""
        all_routed = set(OPUS_AGENTS + SONNET_AGENTS + HAIKU_AGENTS)
        total = len(OPUS_AGENTS) + len(SONNET_AGENTS) + len(HAIKU_AGENTS)
        assert total == 24, (
            f"Model routing covers {total} agents, expected 24 "
            f"(11 Opus + 11 Sonnet + 2 Haiku)"
        )

    def test_no_duplicate_agents_across_tiers(self):
        """No agent should appear in more than one model tier."""
        opus_set = set(OPUS_AGENTS)
        sonnet_set = set(SONNET_AGENTS)
        haiku_set = set(HAIKU_AGENTS)

        opus_sonnet = opus_set & sonnet_set
        opus_haiku = opus_set & haiku_set
        sonnet_haiku = sonnet_set & haiku_set

        errors = []
        if opus_sonnet:
            errors.append(f"In both Opus and Sonnet: {opus_sonnet}")
        if opus_haiku:
            errors.append(f"In both Opus and Haiku: {opus_haiku}")
        if sonnet_haiku:
            errors.append(f"In both Sonnet and Haiku: {sonnet_haiku}")

        assert not errors, "Duplicate agents across tiers:\n" + "\n".join(errors)

    def test_all_routed_agents_are_valid(self):
        """Every agent in model routing must be a valid agent ID."""
        all_routed = set(OPUS_AGENTS + SONNET_AGENTS + HAIKU_AGENTS)
        invalid = all_routed - set(AGENT_IDS)
        assert not invalid, (
            f"Model routing references invalid agent IDs: {invalid}"
        )

    def test_all_agents_are_routed(self):
        """All 24 core agents should be in the model routing table."""
        all_routed = set(OPUS_AGENTS + SONNET_AGENTS + HAIKU_AGENTS)
        unrouted = set(AGENT_IDS) - all_routed
        assert not unrouted, (
            f"Unrouted agents: {sorted(unrouted)} — all agents should be assigned a tier"
        )


class TestParallelExecutionGroups:
    """Tests that parallel execution groups reference valid agents."""

    def test_all_parallel_group_agents_exist(self):
        """Every agent referenced in a parallel execution group must exist."""
        invalid = {}
        for group_name, agents in PARALLEL_GROUPS.items():
            missing = [a for a in agents if a not in AGENT_IDS]
            if missing:
                invalid[group_name] = missing

        assert not invalid, (
            "Parallel groups reference invalid agents:\n"
            + "\n".join(f"  {g}: {a}" for g, a in invalid.items())
        )

    def test_all_parallel_group_agents_have_directories(self):
        """Every agent in a parallel group must have a skill directory."""
        missing = {}
        for group_name, agents in PARALLEL_GROUPS.items():
            no_dir = [a for a in agents if not (SKILLS_DIR / a).is_dir()]
            if no_dir:
                missing[group_name] = no_dir

        assert not missing, (
            "Parallel groups reference agents without directories:\n"
            + "\n".join(f"  {g}: {a}" for g, a in missing.items())
        )


class TestSequentialPipelines:
    """Tests that sequential pipeline agents exist and are valid."""

    def test_all_pipeline_agents_exist(self):
        """Every agent in a sequential pipeline must be a valid agent ID."""
        invalid = {}
        for pipeline_name, agents in SEQUENTIAL_PIPELINES.items():
            missing = [a for a in agents if a not in AGENT_IDS]
            if missing:
                invalid[pipeline_name] = missing

        assert not invalid, (
            "Sequential pipelines reference invalid agents:\n"
            + "\n".join(f"  {p}: {a}" for p, a in invalid.items())
        )

    def test_all_pipeline_agents_have_directories(self):
        """Every agent in a sequential pipeline must have a skill directory."""
        missing = {}
        for pipeline_name, agents in SEQUENTIAL_PIPELINES.items():
            no_dir = [a for a in agents if not (SKILLS_DIR / a).is_dir()]
            if no_dir:
                missing[pipeline_name] = no_dir

        assert not missing, (
            "Sequential pipelines reference agents without directories:\n"
            + "\n".join(f"  {p}: {a}" for p, a in missing.items())
        )


class TestAutoTriggerKeywords:
    """Tests that auto-trigger keyword tables reference valid agent IDs."""

    def test_claude_md_trigger_table_agents_are_valid(self):
        """All diverga:XX references in CLAUDE.md must be valid agents or VS Arena personas."""
        assert CLAUDE_MD.exists(), f"CLAUDE.md not found at {CLAUDE_MD}"
        content = CLAUDE_MD.read_text(encoding="utf-8")

        # Extract all diverga:XX references
        references = set(re.findall(r"diverga:([a-z]\d+)", content))

        # Valid includes core agents + VS Arena personas (v1-v5)
        all_valid = set(AGENT_IDS) | {"v1", "v2", "v3", "v4", "v5"}
        invalid = references - all_valid
        assert not invalid, (
            f"CLAUDE.md references invalid agent IDs: {sorted(invalid)}"
        )

    def test_every_agent_has_trigger_keywords(self):
        """Every agent ID should appear in the CLAUDE.md trigger keyword tables."""
        assert CLAUDE_MD.exists()
        content = CLAUDE_MD.read_text(encoding="utf-8")

        # Extract the auto-trigger section
        trigger_section_match = re.search(
            r"## Auto-Trigger Agent Dispatch.*?(?=^## |\Z)",
            content,
            re.DOTALL | re.MULTILINE,
        )
        if trigger_section_match is None:
            pytest.skip("Auto-Trigger Agent Dispatch section not found in CLAUDE.md")

        trigger_section = trigger_section_match.group(0)
        missing_triggers = []
        for aid in AGENT_IDS:
            if f"diverga:{aid}" not in trigger_section:
                missing_triggers.append(aid)

        assert not missing_triggers, (
            f"Agents without trigger keywords in CLAUDE.md: {missing_triggers}"
        )


class TestCategoryStructure:
    """Tests that agent categories match the documented structure."""

    CATEGORIES = {
        "A: Foundation": ["a1", "a2", "a5"],
        "B: Evidence": ["b1", "b2"],
        "C: Design & Meta-Analysis": ["c1", "c2", "c3", "c5"],
        "D: Data Collection": ["d2", "d4"],
        "E: Analysis": ["e1", "e2", "e3"],
        "F: Quality": ["f5"],
        "G: Communication": ["g1", "g2", "g5", "g6"],
        "I: Systematic Review": ["i0", "i1", "i2", "i3"],
        "X: Cross-Cutting": ["x1"],
    }

    def test_category_agent_counts(self):
        """Each category must have the documented number of agents."""
        expected_counts = {
            "A: Foundation": 3,
            "B: Evidence": 2,
            "C: Design & Meta-Analysis": 4,
            "D: Data Collection": 2,
            "E: Analysis": 3,
            "F: Quality": 1,
            "G: Communication": 4,
            "I: Systematic Review": 4,
            "X: Cross-Cutting": 1,
        }

        for category, expected_count in expected_counts.items():
            agents = self.CATEGORIES[category]
            assert len(agents) == expected_count, (
                f"Category '{category}' has {len(agents)} agents, "
                f"expected {expected_count}"
            )

    def test_total_agents_across_categories_is_24(self):
        """Sum of all category agents must equal 24."""
        total = sum(len(agents) for agents in self.CATEGORIES.values())
        assert total == 24, (
            f"Total agents across categories is {total}, expected 24"
        )

    def test_no_duplicate_agents_across_categories(self):
        """No agent should appear in more than one category."""
        seen: dict[str, str] = {}
        duplicates = []
        for category, agents in self.CATEGORIES.items():
            for agent in agents:
                if agent in seen:
                    duplicates.append(
                        f"{agent} in both '{seen[agent]}' and '{category}'"
                    )
                seen[agent] = category

        assert not duplicates, (
            "Duplicate agents across categories:\n"
            + "\n".join(f"  {d}" for d in duplicates)
        )
