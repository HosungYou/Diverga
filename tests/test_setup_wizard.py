#!/usr/bin/env python3
"""
Tests for Setup Wizard System
===============================

Validates the setup wizard configuration, the diverga-config.json schema,
and that the setup SKILL.md describes the correct wizard flow.

Usage:
    pytest tests/test_setup_wizard.py -v
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent.parent
CONFIG_PATH = BASE_DIR / "config" / "diverga-config.json"
SETUP_SKILL_PATH = BASE_DIR / "skills" / "setup" / "SKILL.md"


class TestConfigFileValidity:
    """Tests that config/diverga-config.json exists and is valid."""

    def test_config_file_exists(self):
        """config/diverga-config.json must exist."""
        assert CONFIG_PATH.exists(), (
            f"diverga-config.json not found at {CONFIG_PATH}"
        )

    def test_config_is_valid_json(self):
        """config/diverga-config.json must be parseable as valid JSON."""
        content = CONFIG_PATH.read_text(encoding="utf-8")
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            pytest.fail(f"diverga-config.json is not valid JSON: {e}")

    def test_config_is_json_object(self):
        """config/diverga-config.json root must be a JSON object (dict)."""
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        assert isinstance(data, dict), (
            f"Expected JSON object at root, got {type(data).__name__}"
        )


class TestConfigRequiredFields:
    """Tests that diverga-config.json has all required fields."""

    @pytest.fixture()
    def config(self) -> dict:
        """Load the config file."""
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    def test_has_version_field(self, config: dict):
        """Config must have a 'version' field."""
        assert "version" in config, "Missing required field: 'version'"

    def test_has_human_checkpoints_field(self, config: dict):
        """Config must have a 'human_checkpoints' field."""
        assert "human_checkpoints" in config, (
            "Missing required field: 'human_checkpoints'"
        )

    def test_has_language_field(self, config: dict):
        """Config must have a 'language' field."""
        assert "language" in config, "Missing required field: 'language'"

    def test_has_model_routing_field(self, config: dict):
        """Config must have a 'model_routing' field."""
        assert "model_routing" in config, (
            "Missing required field: 'model_routing'"
        )

    def test_human_checkpoints_is_object(self, config: dict):
        """human_checkpoints must be a JSON object."""
        cp = config.get("human_checkpoints")
        assert isinstance(cp, dict), (
            f"'human_checkpoints' must be an object, got {type(cp).__name__}"
        )

    def test_human_checkpoints_has_enabled(self, config: dict):
        """human_checkpoints must have an 'enabled' boolean field."""
        cp = config.get("human_checkpoints", {})
        assert "enabled" in cp, "human_checkpoints missing 'enabled' field"
        assert isinstance(cp["enabled"], bool), (
            f"human_checkpoints.enabled must be boolean, got {type(cp['enabled']).__name__}"
        )

    def test_human_checkpoints_has_required_list(self, config: dict):
        """human_checkpoints must have a 'required' list."""
        cp = config.get("human_checkpoints", {})
        assert "required" in cp, "human_checkpoints missing 'required' list"
        assert isinstance(cp["required"], list), (
            f"human_checkpoints.required must be a list, got {type(cp['required']).__name__}"
        )

    def test_model_routing_has_tiers(self, config: dict):
        """model_routing must have high, medium, and low tier mappings."""
        routing = config.get("model_routing", {})
        for tier in ("high", "medium", "low"):
            assert tier in routing, (
                f"model_routing missing '{tier}' tier"
            )

    def test_model_routing_values(self, config: dict):
        """model_routing tiers must map to valid model names."""
        routing = config.get("model_routing", {})
        valid_models = {"opus", "sonnet", "haiku"}
        for tier in ("high", "medium", "low"):
            model = routing.get(tier, "")
            assert model in valid_models, (
                f"model_routing.{tier} = '{model}', expected one of {valid_models}"
            )


class TestSetupSkillStructure:
    """Tests that the setup SKILL.md describes the correct wizard flow."""

    @pytest.fixture()
    def setup_content(self) -> str:
        """Load setup SKILL.md content."""
        assert SETUP_SKILL_PATH.exists(), (
            f"setup SKILL.md not found at {SETUP_SKILL_PATH}"
        )
        return SETUP_SKILL_PATH.read_text(encoding="utf-8")

    def test_setup_skill_exists(self):
        """setup/SKILL.md must exist."""
        assert SETUP_SKILL_PATH.exists()

    def test_describes_multi_step_wizard(self, setup_content: str):
        """Setup SKILL.md must describe a multi-step wizard (Steps 1+)."""
        assert "Step 1:" in setup_content or "### Step 1" in setup_content, (
            "Setup SKILL.md missing Step 1"
        )
        assert "Step 2:" in setup_content or "### Step 2" in setup_content, (
            "Setup SKILL.md missing Step 2"
        )

    def test_step_0_is_project_detection(self, setup_content: str):
        """Step 0 must be Project Detection (auto-detection, not user-facing)."""
        assert "Step 0" in setup_content, "Setup SKILL.md missing Step 0"
        assert "Project Detection" in setup_content or "project" in setup_content.lower(), (
            "Step 0 should be Project Detection"
        )

    def test_step_1_is_checkpoint_level(self, setup_content: str):
        """Step 1 must include Checkpoint Level selection."""
        step1_match = re.search(
            r"### Step 1.*?(?=### Step 2|\Z)",
            setup_content,
            re.DOTALL,
        )
        assert step1_match is not None, "Cannot find Step 1 section"
        step1 = step1_match.group(0).lower()
        assert "checkpoint" in step1, (
            "Step 1 should include checkpoint level selection"
        )

    def test_has_hud_configuration(self, setup_content: str):
        """Setup must include HUD configuration step."""
        assert "hud" in setup_content.lower(), (
            "Setup should include HUD configuration"
        )

    def test_has_vs_arena_step(self, setup_content: str):
        """Setup must include VS Arena configuration step (v11.1)."""
        assert "vs arena" in setup_content.lower() or "VS Arena" in setup_content, (
            "Setup should include VS Arena configuration step"
        )

    def test_no_llm_selection_step(self, setup_content: str):
        """Setup must NOT include an LLM selection step.

        Claude Code is already authenticated, so LLM selection is removed.
        """
        content_lower = setup_content.lower()
        # Should not have a dedicated LLM provider selection step
        assert "llm selection" not in content_lower or "removed" in content_lower, (
            "Setup should not include LLM selection step "
            "(Claude Code is already authenticated)"
        )

    def test_no_old_wizard_format(self, setup_content: str):
        """Setup must NOT describe steps beyond Step 6 (old format)."""
        has_step_7_plus = any(
            f"### Step {n}" in setup_content
            for n in range(7, 9)
        )
        assert not has_step_7_plus, (
            "Setup SKILL.md should not have Steps 7-8 (old format)"
        )


class TestSetupOutputConfig:
    """Tests that the setup wizard generates correct config structure."""

    @pytest.fixture()
    def setup_content(self) -> str:
        """Load setup SKILL.md content."""
        return SETUP_SKILL_PATH.read_text(encoding="utf-8")

    def test_setup_mentions_config_output_path(self, setup_content: str):
        """Setup SKILL.md must reference the config output path."""
        assert "diverga-config.json" in setup_content, (
            "Setup SKILL.md should reference diverga-config.json output path"
        )

    def test_setup_generates_version_in_config(self, setup_content: str):
        """Setup SKILL.md config template must include version field."""
        assert '"version"' in setup_content, (
            "Setup config template should include version field"
        )

    def test_setup_generates_model_routing_in_config(self, setup_content: str):
        """Setup SKILL.md config template must include model_routing."""
        assert '"model_routing"' in setup_content, (
            "Setup config template should include model_routing field"
        )
