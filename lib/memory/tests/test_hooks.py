"""
Test suite for Diverga Memory Lifecycle Hooks.

Tests the three core hooks:
1. on_session_start - Context loading
2. on_checkpoint_reached - Decision tracking
3. on_session_end - Session summarization
"""

import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hooks import MemoryHooks, ContextInjection
from memory_api import DivergeMemory, DivergeMemoryConfig
from schema import MemoryType, DecisionType, Priority


def test_session_start():
    """Test on_session_start hook."""
    print("=" * 60)
    print("TEST 1: on_session_start")
    print("=" * 60)

    # Create temporary project directory
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test-project"
        project_path.mkdir()

        # Create .research directory with project state
        research_dir = project_path / ".research"
        research_dir.mkdir()

        # Create sample project state
        import yaml
        state = {
            "project_name": "Test-Project",
            "research_question": "How do AI agents improve research workflows?",
            "current_stage": "foundation",
            "last_updated": "2024-02-01T10:00:00"
        }
        with open(research_dir / "project-state.yaml", "w") as f:
            yaml.dump(state, f)

        # Initialize hooks with project path
        config = DivergeMemoryConfig(project_path=str(project_path))
        memory = DivergeMemory(config=config)
        hooks = MemoryHooks(memory=memory, auto_detect_project=False)

        # Store some test memories
        memory.store(
            content="Used qualitative paradigm for exploratory research",
            memory_type=MemoryType.DECISION,
            namespace="foundation",
            priority=Priority.HIGH,
            title="Paradigm Selection"
        )

        memory.store(
            content="PICO framework is effective for structuring research questions",
            memory_type=MemoryType.PATTERN,
            namespace="foundation",
            priority=Priority.HIGH,
            title="RQ Structure Pattern"
        )

        # Test session start
        context = hooks.on_session_start(
            project_path=str(project_path),
            session_id="test-session-001"
        )

        # Verify context
        assert isinstance(context, ContextInjection)
        assert context.project_name == "Test-Project"
        assert context.research_question == "How do AI agents improve research workflows?"
        assert context.current_stage == "foundation"

        # Print formatted prompt
        print("\nGenerated Context Prompt:")
        print("-" * 60)
        print(context.to_prompt())
        print("-" * 60)

        print("\n✓ TEST PASSED: Session start context loaded successfully\n")


def test_checkpoint_reached():
    """Test on_checkpoint_reached hook."""
    print("=" * 60)
    print("TEST 2: on_checkpoint_reached")
    print("=" * 60)

    # Create temporary project directory
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test-project"
        project_path.mkdir()
        research_dir = project_path / ".research"
        research_dir.mkdir()

        # Initialize hooks
        config = DivergeMemoryConfig(project_path=str(project_path))
        memory = DivergeMemory(config=config)
        hooks = MemoryHooks(memory=memory, auto_detect_project=False)

        # Start session
        context = hooks.on_session_start(
            project_path=str(project_path),
            session_id="test-session-002"
        )

        # Trigger checkpoint
        decision_data = {
            "decision": "Selected qualitative paradigm",
            "rationale": "Focus on lived experiences and contextual meaning",
            "before_state": "Undecided between quantitative and qualitative",
            "after_state": "Qualitative paradigm confirmed",
            "options_considered": [
                "Quantitative (T=0.8)",
                "Qualitative (T=0.5) - SELECTED",
                "Mixed methods (T=0.3)"
            ]
        }

        hooks.on_checkpoint_reached(
            checkpoint_id="CP_PARADIGM_SELECTION",
            stage="foundation",
            agent_id="diverga:a5",
            decision_data=decision_data,
            session_id="test-session-002",
            t_score=0.5
        )

        # Verify decision saved
        recent_decisions = memory.get_recent_decisions(limit=1)
        assert len(recent_decisions) > 0
        assert "qualitative paradigm" in recent_decisions[0]['content'].lower()

        print("\n✓ Decision saved to memory")

        # Verify project state updated
        import yaml
        state_file = research_dir / "project-state.yaml"
        assert state_file.exists()

        with open(state_file, 'r') as f:
            state = yaml.safe_load(f)

        assert state['current_stage'] == 'foundation'
        assert state['last_checkpoint'] == 'CP_PARADIGM_SELECTION'
        assert 'CP_PARADIGM_SELECTION' in state

        print("✓ Project state updated")
        print(f"  - Current stage: {state['current_stage']}")
        print(f"  - Last checkpoint: {state['last_checkpoint']}")

        print("\n✓ TEST PASSED: Checkpoint reached and logged successfully\n")


def test_session_end():
    """Test on_session_end hook."""
    print("=" * 60)
    print("TEST 3: on_session_end")
    print("=" * 60)

    # Create temporary project directory
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test-project"
        project_path.mkdir()

        # Initialize hooks
        config = DivergeMemoryConfig(project_path=str(project_path))
        memory = DivergeMemory(config=config)
        hooks = MemoryHooks(memory=memory, auto_detect_project=False)

        # Start session
        context = hooks.on_session_start(
            project_path=str(project_path),
            session_id="test-session-003"
        )

        # Trigger some checkpoints
        hooks.on_checkpoint_reached(
            checkpoint_id="CP_PARADIGM_SELECTION",
            stage="foundation",
            agent_id="diverga:a5",
            decision_data={"decision": "Selected qualitative paradigm"},
            session_id="test-session-003"
        )

        hooks.on_checkpoint_reached(
            checkpoint_id="CP_THEORY_SELECTION",
            stage="foundation",
            agent_id="diverga:a2",
            decision_data={"decision": "Selected sociocultural theory"},
            session_id="test-session-003"
        )

        # End session
        hooks.on_session_end(
            session_id="test-session-003",
            agents_used=["diverga:a5", "diverga:a2"],
            decisions_made=["CP_PARADIGM_SELECTION", "CP_THEORY_SELECTION"]
        )

        # Verify session saved
        session_history = memory.get_session_history(limit=1)
        assert len(session_history) > 0
        assert session_history[0]['id'] == "test-session-003"

        print("\n✓ Session saved to database")
        print(f"  - Session ID: {session_history[0]['id']}")
        print(f"  - Summary: {session_history[0]['summary']}")
        print(f"  - Agents used: {session_history[0].get('agents_used', [])}")

        print("\n✓ TEST PASSED: Session ended and summarized successfully\n")


def test_full_workflow():
    """Test complete workflow: start → checkpoints → end."""
    print("=" * 60)
    print("TEST 4: Full Workflow")
    print("=" * 60)

    # Create temporary project directory
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test-project"
        project_path.mkdir()
        research_dir = project_path / ".research"
        research_dir.mkdir()

        # Create project state
        import yaml
        state = {
            "project_name": "Full-Workflow-Test",
            "research_question": "How do lifecycle hooks improve context persistence?",
            "current_stage": "foundation"
        }
        with open(research_dir / "project-state.yaml", "w") as f:
            yaml.dump(state, f)

        # Initialize hooks
        config = DivergeMemoryConfig(project_path=str(project_path))
        memory = DivergeMemory(config=config)
        hooks = MemoryHooks(memory=memory, auto_detect_project=False)

        # STEP 1: Session Start
        print("\n[1] Starting session...")
        context = hooks.on_session_start(
            project_path=str(project_path),
            session_id="workflow-session"
        )
        print(f"    ✓ Project: {context.project_name}")
        print(f"    ✓ RQ: {context.research_question}")

        # STEP 2: Multiple Checkpoints
        print("\n[2] Processing checkpoints...")

        checkpoints = [
            {
                "checkpoint_id": "CP_RESEARCH_DIRECTION",
                "stage": "foundation",
                "agent_id": "diverga:a1",
                "decision_data": {
                    "decision": "Refined research question",
                    "rationale": "Focused on specific context"
                }
            },
            {
                "checkpoint_id": "CP_PARADIGM_SELECTION",
                "stage": "foundation",
                "agent_id": "diverga:a5",
                "decision_data": {
                    "decision": "Selected qualitative paradigm",
                    "rationale": "Exploratory nature of study"
                }
            },
            {
                "checkpoint_id": "CP_THEORY_SELECTION",
                "stage": "foundation",
                "agent_id": "diverga:a2",
                "decision_data": {
                    "decision": "Selected activity theory",
                    "rationale": "Aligns with research context"
                }
            }
        ]

        for cp in checkpoints:
            hooks.on_checkpoint_reached(
                checkpoint_id=cp["checkpoint_id"],
                stage=cp["stage"],
                agent_id=cp["agent_id"],
                decision_data=cp["decision_data"],
                session_id="workflow-session"
            )
            print(f"    ✓ {cp['checkpoint_id']}")

        # STEP 3: Session End
        print("\n[3] Ending session...")
        hooks.on_session_end(
            session_id="workflow-session",
            agents_used=["diverga:a1", "diverga:a5", "diverga:a2"],
            decisions_made=[cp["checkpoint_id"] for cp in checkpoints]
        )
        print("    ✓ Session ended")

        # STEP 4: Verify Results
        print("\n[4] Verifying results...")

        # Check session saved
        session_history = memory.get_session_history(limit=1)
        assert len(session_history) > 0
        print(f"    ✓ Session saved: {session_history[0]['id']}")

        # Check decisions saved
        recent_decisions = memory.get_recent_decisions(limit=3)
        assert len(recent_decisions) == 3
        print(f"    ✓ Decisions saved: {len(recent_decisions)}")

        # Check project state updated
        with open(research_dir / "project-state.yaml", 'r') as f:
            final_state = yaml.safe_load(f)

        assert final_state['last_checkpoint'] == "CP_THEORY_SELECTION"
        print(f"    ✓ Project state updated: {final_state['last_checkpoint']}")

        # STEP 5: Test Context Reload
        print("\n[5] Testing context reload in new session...")
        context2 = hooks.on_session_start(
            project_path=str(project_path),
            session_id="workflow-session-2"
        )

        assert len(context2.recent_decisions) > 0
        print(f"    ✓ Loaded {len(context2.recent_decisions)} recent decisions")
        print("\n    Context Preview:")
        for decision in context2.recent_decisions[:2]:
            print(f"      - {decision}")

        print("\n✓ TEST PASSED: Full workflow completed successfully\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("DIVERGA MEMORY LIFECYCLE HOOKS - TEST SUITE")
    print("=" * 60 + "\n")

    try:
        test_session_start()
        test_checkpoint_reached()
        test_session_end()
        test_full_workflow()

        print("=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60 + "\n")

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
