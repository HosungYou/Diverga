#!/usr/bin/env python3
"""
Example: Using Memory Lifecycle Hooks with Diverga Agents

This example demonstrates how to integrate lifecycle hooks
into a typical research workflow with Diverga agents.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from hooks import MemoryHooks, ContextInjection
from memory_api import DivergeMemory, DivergeMemoryConfig
from schema import MemoryType, Priority


def simulate_research_session():
    """
    Simulate a complete research session with hooks.

    This demonstrates:
    1. Session start with context loading
    2. Multiple agent invocations with checkpoints
    3. Session end with summary
    """
    print("=" * 70)
    print("DIVERGA RESEARCH SESSION SIMULATION")
    print("=" * 70)
    print()

    # Setup: Create hooks instance (auto-detects project)
    hooks = MemoryHooks(auto_detect_project=True)
    print("✓ Memory hooks initialized")
    print(f"  Scope: {hooks.memory.scope}")
    print(f"  DB Path: {hooks.memory.db_path}")
    print()

    # STAGE 1: Session Start
    print("-" * 70)
    print("STAGE 1: Session Start (Load Context)")
    print("-" * 70)

    session_id = "research-session-demo"
    context = hooks.on_session_start(session_id=session_id)

    print(f"\n✓ Session started: {session_id}")
    print(f"  Project: {context.project_name}")
    print(f"  Research Question: {context.research_question or 'Not set'}")
    print(f"  Current Stage: {context.current_stage or 'Not set'}")
    print(f"  Recent Decisions: {len(context.recent_decisions)}")
    print(f"  Relevant Memories: {len(context.relevant_memories)}")
    print()

    # Show context that would be injected into agent prompt
    print("Context to inject into agent prompt:")
    print("-" * 70)
    print(context.to_prompt())
    print("-" * 70)
    print()

    # STAGE 2: Agent Workflow with Checkpoints
    print("-" * 70)
    print("STAGE 2: Agent Workflow (Multiple Checkpoints)")
    print("-" * 70)
    print()

    # Checkpoint 1: Research Question Refinement
    print("[Agent: diverga:a1 - ResearchQuestionRefiner]")
    print("  Task: Refine research question")
    print("  Action: User approves refined question")

    hooks.on_checkpoint_reached(
        checkpoint_id="CP_RESEARCH_DIRECTION",
        stage="foundation",
        agent_id="diverga:a1",
        decision_data={
            "decision": "Refined research question to focus on AI-assisted learning",
            "rationale": "Original question too broad, narrowed to specific domain",
            "before_state": "How does AI help in education?",
            "after_state": "How do AI chatbots improve language learning outcomes "
                          "in higher education?",
            "options_considered": [
                "General AI in education (T=0.9) - Too broad",
                "AI chatbots in language learning (T=0.5) - SELECTED",
                "AI tutoring systems (T=0.4) - Too narrow"
            ]
        },
        session_id=session_id,
        t_score=0.5
    )
    print("  ✓ Checkpoint: CP_RESEARCH_DIRECTION saved\n")

    # Checkpoint 2: Paradigm Selection
    print("[Agent: diverga:a5 - ParadigmWorldviewAdvisor]")
    print("  Task: Determine research paradigm")
    print("  Action: User selects qualitative paradigm")

    hooks.on_checkpoint_reached(
        checkpoint_id="CP_PARADIGM_SELECTION",
        stage="foundation",
        agent_id="diverga:a5",
        decision_data={
            "decision": "Selected qualitative paradigm",
            "rationale": "Focus on lived experiences of language learners "
                        "using AI chatbots",
            "before_state": "Undecided between quantitative and qualitative",
            "after_state": "Qualitative paradigm with phenomenological approach",
            "options_considered": [
                "Quantitative experimental (T=0.8) - Doesn't capture experience depth",
                "Qualitative phenomenological (T=0.5) - SELECTED",
                "Mixed methods (T=0.3) - Too complex for initial study"
            ]
        },
        session_id=session_id,
        t_score=0.5
    )
    print("  ✓ Checkpoint: CP_PARADIGM_SELECTION saved\n")

    # Checkpoint 3: Theoretical Framework
    print("[Agent: diverga:a2 - TheoreticalFrameworkArchitect]")
    print("  Task: Select theoretical framework")
    print("  Action: User approves sociocultural theory")

    hooks.on_checkpoint_reached(
        checkpoint_id="CP_THEORY_SELECTION",
        stage="foundation",
        agent_id="diverga:a2",
        decision_data={
            "decision": "Selected sociocultural theory (Vygotsky)",
            "rationale": "Aligns with qualitative paradigm and focuses on "
                        "social interaction in learning",
            "before_state": "No theoretical framework selected",
            "after_state": "Sociocultural theory with focus on ZPD and scaffolding",
            "options_considered": [
                "Cognitive load theory (T=0.7) - More quantitative focus",
                "Sociocultural theory (T=0.4) - SELECTED",
                "Activity theory (T=0.3) - Complex but interesting"
            ]
        },
        session_id=session_id,
        t_score=0.4
    )
    print("  ✓ Checkpoint: CP_THEORY_SELECTION saved\n")

    # Store some additional context for next session
    print("[Storing additional context for future sessions...]")

    hooks.memory.store(
        content="Qualitative research in education requires 15-30 participants "
               "to achieve saturation (Creswell, 2013)",
        memory_type=MemoryType.PATTERN,
        namespace="design.sampling",
        priority=Priority.HIGH,
        title="Sample size for qualitative studies",
        session_id=session_id
    )

    hooks.memory.store(
        content="PICO framework (Population, Intervention, Comparison, Outcome) "
               "helps structure research questions clearly",
        memory_type=MemoryType.PATTERN,
        namespace="foundation.research_question",
        priority=Priority.HIGH,
        title="PICO framework for RQ structure",
        session_id=session_id
    )

    print("  ✓ Stored 2 pattern memories for future reference\n")

    # STAGE 3: Session End
    print("-" * 70)
    print("STAGE 3: Session End (Generate Summary)")
    print("-" * 70)
    print()

    agents_used = ["diverga:a1", "diverga:a5", "diverga:a2"]
    decisions_made = [
        "CP_RESEARCH_DIRECTION",
        "CP_PARADIGM_SELECTION",
        "CP_THEORY_SELECTION"
    ]

    hooks.on_session_end(
        session_id=session_id,
        agents_used=agents_used,
        decisions_made=decisions_made,
        auto_summarize=True
    )

    print(f"✓ Session ended: {session_id}")
    print(f"  Agents used: {len(agents_used)}")
    print(f"  Decisions made: {len(decisions_made)}")
    print(f"  Total memories: {len(hooks.memory.db.get_session_memories(session_id))}")
    print()

    # STAGE 4: Demonstrate Context Persistence (Next Session)
    print("-" * 70)
    print("STAGE 4: Next Session (Context Automatically Loaded)")
    print("-" * 70)
    print()

    print("[Starting new session...]")
    context2 = hooks.on_session_start(session_id="research-session-demo-2")

    print(f"\n✓ New session started with persistent context!")
    print(f"  Project: {context2.project_name}")
    print(f"  Loaded {len(context2.recent_decisions)} recent decisions:")

    for i, decision in enumerate(context2.recent_decisions, 1):
        print(f"    {i}. {decision}")

    print(f"\n  Loaded {len(context2.relevant_memories)} relevant patterns:")
    for i, memory in enumerate(context2.relevant_memories, 1):
        preview = memory[:80] + "..." if len(memory) > 80 else memory
        print(f"    {i}. {preview}")

    print()
    print("=" * 70)
    print("SIMULATION COMPLETE")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  1. Context automatically loads at session start")
    print("  2. Decisions saved at checkpoints persist across sessions")
    print("  3. Patterns stored during research are available to future agents")
    print("  4. No need to re-explain research question or methodology")
    print()


if __name__ == "__main__":
    try:
        simulate_research_session()
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)
