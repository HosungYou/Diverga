#!/usr/bin/env python3
"""
Tests for Diverga Patch Changes & Branding
=============================================

Validates key structural changes:
- English-First UI
- Box-Drawing Layout
- ScholaRAG Branding Removal
- Dashboard existence

Usage:
    pytest tests/test_patch4_changes.py -v
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent


class TestEnglishFirstUI:
    """Phase A: English-First UI Tests"""

    def test_config_has_english_language(self):
        """Test that diverga-config.json has language: en (not auto)"""
        config_path = BASE_DIR / "config" / "diverga-config.json"
        assert config_path.exists(), f"Config file not found: {config_path}"

        with open(config_path, encoding="utf-8") as f:
            config = json.load(f)

        assert "language" in config, "Config missing 'language' field"
        assert config["language"] == "en", f"Expected language='en', got '{config['language']}'"

    def test_setup_skill_config_template_version(self):
        """Test that setup SKILL.md config template has a version field"""
        setup_skill = BASE_DIR / "skills" / "setup" / "SKILL.md"
        assert setup_skill.exists(), f"Setup skill not found: {setup_skill}"

        content = setup_skill.read_text(encoding="utf-8")
        assert '"version"' in content, "Config template should have a version field"

    def test_research_coordinator_checkpoint_ascii_markers(self):
        """Test that research-coordinator SKILL.md checkpoint protocol uses ASCII [X] and [OK]"""
        skill_path = BASE_DIR / "skills" / "research-coordinator" / "SKILL.md"
        assert skill_path.exists(), f"Research coordinator skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        # Should contain ASCII markers
        assert "[X]" in content, "Checkpoint protocol should contain [X] marker"
        assert "[OK]" in content, "Checkpoint protocol should contain [OK] marker"

    def test_research_coordinator_no_korean_in_checkpoint(self):
        """Test that research-coordinator SKILL.md does NOT contain Korean text in checkpoint protocol"""
        skill_path = BASE_DIR / "skills" / "research-coordinator" / "SKILL.md"
        assert skill_path.exists(), f"Research coordinator skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        # Should not contain Korean text fragments
        assert "진행하겠습니다" not in content, "Checkpoint protocol should not contain Korean text"
        assert "어떤 방향으로" not in content, "Checkpoint protocol should not contain Korean text"

    def test_research_orchestrator_no_korean_dialog(self):
        """Test that research-orchestrator SKILL.md does NOT contain Korean-only dialog examples"""
        skill_path = BASE_DIR / "skills" / "research-orchestrator" / "SKILL.md"
        assert skill_path.exists(), f"Research orchestrator skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        # Check for common Korean particles/patterns that indicate Korean-only text
        key_principle_match = re.search(r'Key Principle.*?(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if key_principle_match:
            key_principle_text = key_principle_match.group(0)
            # Should not have Korean characters
            korean_pattern = re.compile(r'[\uAC00-\uD7A3]')  # Hangul syllables
            assert not korean_pattern.search(key_principle_text), \
                "Key Principle section should not contain Korean-only dialog examples"


class TestBoxDrawingFixes:
    """Phase A.5: Box-Drawing Layout Tests"""

    def test_readme_agent_section_structure(self):
        """Test that README.md has agent category information"""
        readme_path = BASE_DIR / "README.md"
        assert readme_path.exists(), f"README.md not found: {readme_path}"

        content = readme_path.read_text(encoding="utf-8")

        # Should have agent-related content
        has_agents = any(cat in content for cat in [
            'Foundation', 'Evidence', 'Design', 'Analysis',
            'Quality', 'Communication', 'Agent', 'agent'
        ])
        assert has_agents, "README should reference agent categories"

    def test_agents_md_checkpoint_no_emoji(self):
        """Test that AGENTS.md checkpoint protocol box does NOT contain emoji"""
        agents_path = BASE_DIR / "AGENTS.md"
        assert agents_path.exists(), f"AGENTS.md not found: {agents_path}"

        content = agents_path.read_text(encoding="utf-8")

        # Look for checkpoint protocol section
        checkpoint_match = re.search(r'checkpoint.*?protocol.*?(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
        if checkpoint_match:
            checkpoint_text = checkpoint_match.group(0)
            assert '❌' not in checkpoint_text, "Checkpoint protocol should not contain ❌ emoji"
            assert '✅' not in checkpoint_text, "Checkpoint protocol should not contain ✅ emoji"

    def test_agents_md_has_checkpoint_content(self):
        """Test that AGENTS.md contains checkpoint-related content"""
        agents_path = BASE_DIR / "AGENTS.md"
        assert agents_path.exists(), f"AGENTS.md not found: {agents_path}"

        content = agents_path.read_text(encoding="utf-8")
        assert "checkpoint" in content.lower() or "REQUIRED" in content, (
            "AGENTS.md should contain checkpoint documentation"
        )

    def test_codex_config_exists_if_applicable(self):
        """Test .codex/diverga-codex.cjs if it exists"""
        codex_path = BASE_DIR / ".codex" / "diverga-codex.cjs"
        if not codex_path.exists():
            pytest.skip(".codex/diverga-codex.cjs not found (may have been removed)")

        content = codex_path.read_text(encoding="utf-8")
        assert "visualWidth" in content, "Codex config should contain visualWidth function"

    def test_checkpoint_spec_no_emoji(self):
        """Test that qa/docs/CHECKPOINT_SPEC.md does NOT contain emoji"""
        spec_path = BASE_DIR / "qa" / "docs" / "CHECKPOINT_SPEC.md"
        assert spec_path.exists(), f"Checkpoint spec not found: {spec_path}"

        content = spec_path.read_text(encoding="utf-8")

        forbidden_emoji = ['🔴', '❌', '✅', '⚠️']
        for emoji in forbidden_emoji:
            assert emoji not in content, f"Checkpoint spec should not contain emoji: {emoji}"


class TestBrandingRemoval:
    """Phase C: ScholaRAG Removal Tests"""

    @pytest.mark.parametrize("file_path", [
        "CLAUDE.md",
        "AGENTS.md",
        "README.md",
        "PLUGIN.md",
        "docs/SDD.md",
        "skills/i1/SKILL.md",
        "skills/i2/SKILL.md",
        "skills/i3/SKILL.md",
        "agents/i0.md",
        "agents/i1.md",
        "agents/i2.md",
        "agents/i3.md",
        "templates/README.md",
        "config/diverga-config.json",
    ])
    def test_active_files_no_scholarag(self, file_path):
        """Test that active files do NOT contain 'ScholaRAG' (case-insensitive)"""
        full_path = BASE_DIR / file_path
        if not full_path.exists():
            pytest.skip(f"File not found: {file_path}")

        content = full_path.read_text(encoding="utf-8")

        # Case-insensitive check
        assert "scholarag" not in content.lower(), \
            f"File {file_path} should not contain 'ScholaRAG' references"

    def test_old_checkpoint_files_cleaned_up(self):
        """Test that old checkpoint YAML files have been cleaned up"""
        old_checkpoint = BASE_DIR / ".claude" / "checkpoints" / "scholarag-checkpoints.yaml"
        assert not old_checkpoint.exists(), "Old ScholaRAG checkpoint file should not exist"


class TestDashboard:
    """Phase B: Dashboard Tests"""

    def test_diverga_skill_has_system_status_section(self):
        """Test that skills/diverga/SKILL.md contains SYSTEM STATUS section"""
        skill_path = BASE_DIR / "skills" / "diverga" / "SKILL.md"
        assert skill_path.exists(), f"Diverga skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        assert re.search(r'SYSTEM\s+STATUS', content, re.IGNORECASE), \
            "Dashboard should contain SYSTEM STATUS section"

    def test_diverga_skill_has_configuration_section(self):
        """Test that skills/diverga/SKILL.md contains CONFIGURATION section"""
        skill_path = BASE_DIR / "skills" / "diverga" / "SKILL.md"
        assert skill_path.exists(), f"Diverga skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        assert "CONFIGURATION" in content, \
            "Dashboard should contain CONFIGURATION section"

    def test_diverga_skill_has_api_status_section(self):
        """Test that skills/diverga/SKILL.md contains API STATUS section"""
        skill_path = BASE_DIR / "skills" / "diverga" / "SKILL.md"
        assert skill_path.exists(), f"Diverga skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        assert re.search(r'API\s+STATUS', content, re.IGNORECASE), \
            "Dashboard should contain API STATUS section"

    def test_diverga_skill_has_quick_actions_section(self):
        """Test that skills/diverga/SKILL.md contains QUICK ACTIONS section"""
        skill_path = BASE_DIR / "skills" / "diverga" / "SKILL.md"
        assert skill_path.exists(), f"Diverga skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        assert re.search(r'QUICK\s+ACTIONS', content, re.IGNORECASE), \
            "Dashboard should contain QUICK ACTIONS section"

    def test_diverga_skill_has_ascii_art_logo(self):
        """Test that skills/diverga/SKILL.md contains ASCII art logo"""
        skill_path = BASE_DIR / "skills" / "diverga" / "SKILL.md"
        assert skill_path.exists(), f"Diverga skill not found: {skill_path}"

        content = skill_path.read_text(encoding="utf-8")

        has_diverga_caps = "DIVERGA" in content
        has_box_drawing = any(char in content for char in ['╔', '╚', '═', '║', '╗', '╝', '┌', '└', '─', '│', '┐', '┘'])

        assert has_diverga_caps or has_box_drawing, \
            "Dashboard should contain ASCII art logo (DIVERGA or box-drawing frame)"


class TestUpgradeRoadmap:
    """Roadmap Documents — old files should be cleaned up in v11.1"""

    def test_old_upgrade_roadmap_removed(self):
        """Old upgrade roadmap files should have been cleaned up in v11.1"""
        roadmap_path = BASE_DIR / "docs" / "UPGRADE-ROADMAP-v8.1-v9.md"
        assert not roadmap_path.exists(), (
            "Old upgrade roadmap should have been removed in v11.1 cleanup"
        )
