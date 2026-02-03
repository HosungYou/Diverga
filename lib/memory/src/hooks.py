"""
Lifecycle Hooks for Diverga Memory System.

Provides Claude Code / Codex compatible hook system for:
- Session start: Auto-load project context and relevant memories
- Checkpoint reached: Save decisions and update project state
- Session end: Generate summary and consolidate memories

Designed for integration with research agents and the Diverga pipeline.
"""

import os
import uuid
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

try:
    from .memory_api import DivergeMemory, DivergeMemoryConfig
    from .schema import MemoryType, DecisionType, Priority
except ImportError:
    # Support direct imports when not used as package
    from memory_api import DivergeMemory, DivergeMemoryConfig
    from schema import MemoryType, DecisionType, Priority


@dataclass
class ContextInjection:
    """
    Context to inject into agent prompts at session start.

    This provides agents with project history, recent decisions,
    and relevant patterns to avoid re-asking established information.
    """
    project_name: str
    research_question: Optional[str] = None
    current_stage: Optional[str] = None
    recent_decisions: List[str] = None  # Formatted decision strings
    relevant_memories: List[str] = None  # Formatted memory strings
    active_sessions: List[str] = None   # Active session summaries

    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.recent_decisions is None:
            self.recent_decisions = []
        if self.relevant_memories is None:
            self.relevant_memories = []
        if self.active_sessions is None:
            self.active_sessions = []

    def to_prompt(self) -> str:
        """
        Generate formatted prompt text for agent context injection.

        Returns:
            Formatted markdown string ready to inject into agent prompts
        """
        sections = []

        # Header
        sections.append("## Research Context (Auto-Loaded from Memory)")
        sections.append("")
        sections.append(f"**Project**: {self.project_name}")

        if self.research_question:
            sections.append(f"**Research Question**: {self.research_question}")

        if self.current_stage:
            sections.append(f"**Current Stage**: {self.current_stage}")

        sections.append("")

        # Recent Decisions
        if self.recent_decisions:
            sections.append("### Recent Decisions")
            for decision in self.recent_decisions:
                sections.append(f"- {decision}")
            sections.append("")

        # Relevant Context
        if self.relevant_memories:
            sections.append("### Relevant Context")
            for memory in self.relevant_memories:
                sections.append(f"{memory}")
            sections.append("")

        # Active Sessions
        if self.active_sessions:
            sections.append("### Active Sessions")
            for session in self.active_sessions:
                sections.append(f"- {session}")
            sections.append("")

        # Footer
        sections.append("---")
        sections.append("**Use this context. Do not re-ask for established information.**")
        sections.append("")

        return "\n".join(sections)


class MemoryHooks:
    """
    Lifecycle hooks for Claude Code / Codex integration.

    Provides automatic context loading, decision tracking, and session management
    for research agents in the Diverga ecosystem.

    Usage:
        hooks = MemoryHooks()

        # On session start
        context = hooks.on_session_start(
            project_path="/path/to/project",
            session_id="session-123"
        )
        print(context.to_prompt())  # Inject into agent prompt

        # On checkpoint
        hooks.on_checkpoint_reached(
            checkpoint_id="CP_PARADIGM_SELECTION",
            stage="foundation",
            agent_id="diverga:a5",
            decision_data={
                "paradigm": "qualitative",
                "rationale": "Focus on lived experiences"
            }
        )

        # On session end
        hooks.on_session_end(
            session_id="session-123",
            agents_used=["diverga:a1", "diverga:a5"],
            decisions_made=["CP_PARADIGM_SELECTION"]
        )
    """

    def __init__(
        self,
        memory: Optional[DivergeMemory] = None,
        auto_detect_project: bool = True
    ):
        """
        Initialize Memory Hooks.

        Args:
            memory: DivergeMemory instance (creates new if None)
            auto_detect_project: Auto-detect project path from cwd
        """
        if memory is None:
            # Create DivergeMemory with auto-detection config
            config = DivergeMemoryConfig(auto_detect_project=auto_detect_project)
            self.memory = DivergeMemory(config=config)
        else:
            self.memory = memory

        self._active_sessions: Dict[str, Dict[str, Any]] = {}

    def on_session_start(
        self,
        project_path: Optional[str] = None,
        session_id: Optional[str] = None,
        context_filters: Optional[Dict[str, Any]] = None
    ) -> ContextInjection:
        """
        Hook: Session Start

        Load project context from memory and return context injection for agent prompts.

        This hook:
        1. Loads project context (research question, stage, etc.)
        2. Finds relevant memories for current session
        3. Retrieves recent decisions
        4. Returns formatted context to inject into prompts

        Args:
            project_path: Path to project (auto-detects if None)
            session_id: Session identifier (generates UUID if None)
            context_filters: Optional filters for memory retrieval
                {
                    "memory_types": ["decision", "pattern"],
                    "stages": ["foundation", "design"],
                    "max_age_days": 7
                }

        Returns:
            ContextInjection object with formatted context
        """
        # Generate session ID if not provided
        if session_id is None:
            session_id = f"session-{uuid.uuid4().hex[:8]}"

        # Get project context
        project_context = self.memory.get_project_context()
        project_name = project_context.get('project_name', 'Unknown Project')

        # Initialize session tracking
        self._active_sessions[session_id] = {
            'session_id': session_id,
            'started_at': datetime.now().isoformat(),
            'project_name': project_name,
            'agents_used': [],
            'checkpoints_reached': []
        }

        # Load project state (from .research/project-state.yaml if exists)
        project_state = self._load_project_state(project_path)

        # Get recent decisions (last 5) using namespace retrieval
        try:
            # Get all decision memories from decision namespace
            recent_decision_memories = self.memory.db.get_memories_by_namespace(
                namespace="decisions",
                include_children=True,
                limit=5
            )
        except Exception:
            # Fallback if search fails
            recent_decision_memories = []

        # Format decisions
        recent_decisions = []
        for mem in recent_decision_memories:
            # Extract decision details from content
            content = mem.get('content', '')
            title = mem.get('title', '')
            created_at = mem.get('created_at', '')

            # Format as concise decision line
            decision_text = f"{title} ({created_at})"
            if content and content != title:
                # Add first line of rationale
                first_line = content.split('\n')[0][:100]
                decision_text += f" - {first_line}"

            recent_decisions.append(decision_text)

        # Get relevant memories (patterns and learnings)
        relevant_memories = []

        # Get high-priority patterns using namespace
        try:
            pattern_memories = self.memory.db.get_memories_by_namespace(
                namespace="",
                include_children=True,
                limit=50
            )

            # Filter for patterns with high priority
            for mem in pattern_memories:
                if mem.get('memory_type') == 'pattern' and mem.get('priority', 0) >= 7:
                    title = mem.get('title', 'Untitled')
                    content = mem.get('content', '')[:200]
                    relevant_memories.append(f"**{title}**: {content}")
                    if len(relevant_memories) >= 3:
                        break
        except Exception:
            pass

        # Get active sessions
        active_sessions = []
        session_history = self.memory.get_session_history(limit=5)
        for session in session_history:
            if session.get('ended_at') is None:  # Active session
                summary = session.get('summary', 'Ongoing session')
                active_sessions.append(f"{session.get('id')}: {summary}")

        # Build context injection
        context = ContextInjection(
            project_name=project_name,
            research_question=project_state.get('research_question'),
            current_stage=project_state.get('current_stage'),
            recent_decisions=recent_decisions,
            relevant_memories=relevant_memories,
            active_sessions=active_sessions
        )

        return context

    def on_checkpoint_reached(
        self,
        checkpoint_id: str,
        stage: str,
        agent_id: str,
        decision_data: Dict[str, Any],
        session_id: Optional[str] = None,
        t_score: Optional[float] = None
    ) -> None:
        """
        Hook: Checkpoint Reached

        Save decision to memory, update project context, and log checkpoint.

        This hook:
        1. Extracts decision details from decision_data
        2. Saves decision as memory with checkpoint metadata
        3. Updates project state file (.research/project-state.yaml)
        4. Logs checkpoint to session tracker

        Args:
            checkpoint_id: Checkpoint identifier (e.g., "CP_PARADIGM_SELECTION")
            stage: Research stage (e.g., "foundation", "design")
            agent_id: Agent that triggered checkpoint (e.g., "diverga:a5")
            decision_data: Dictionary with decision details
                {
                    "decision": "Selected qualitative paradigm",
                    "rationale": "Focus on lived experiences",
                    "before_state": "Undecided",
                    "after_state": "Qualitative paradigm confirmed",
                    "options_considered": [...],
                    "metadata": {...}
                }
            session_id: Session identifier (uses latest active if None)
            t_score: VS methodology typicality score (0.0-1.0)

        Returns:
            None (side effects: memory stored, project state updated)
        """
        # Get active session
        if session_id is None:
            # Use most recent active session
            active_sessions = [
                s for s in self._active_sessions.values()
            ]
            if active_sessions:
                session_id = active_sessions[-1]['session_id']

        # Extract decision details
        decision = decision_data.get('decision', checkpoint_id)
        rationale = decision_data.get('rationale', '')
        before_state = decision_data.get('before_state')
        after_state = decision_data.get('after_state')

        # Determine decision type from checkpoint_id
        decision_type = self._infer_decision_type(checkpoint_id)

        # Record decision
        decision_id = self.memory.record_decision(
            stage=stage,
            agent_id=agent_id,
            decision_type=decision_type,
            description=decision,
            before_state=before_state,
            after_state=after_state,
            rationale=rationale,
            t_score=t_score
        )

        # Update project state
        self._update_project_state(
            checkpoint_id=checkpoint_id,
            stage=stage,
            decision_data=decision_data
        )

        # Log checkpoint to session
        if session_id and session_id in self._active_sessions:
            self._active_sessions[session_id]['checkpoints_reached'].append({
                'checkpoint_id': checkpoint_id,
                'decision_id': decision_id,
                'timestamp': datetime.now().isoformat()
            })

    def on_session_end(
        self,
        session_id: str,
        agents_used: List[str],
        decisions_made: List[str],
        auto_summarize: bool = True
    ) -> None:
        """
        Hook: Session End

        Generate session summary, save session record, and consolidate memories.

        This hook:
        1. Generates session summary (AI-powered if embeddings available)
        2. Saves session record with agents and decisions
        3. Consolidates similar memories (deduplication)
        4. Cleans up active session tracker

        Args:
            session_id: Session identifier
            agents_used: List of agent IDs used (e.g., ["diverga:a1", "diverga:a5"])
            decisions_made: List of checkpoint IDs reached
            auto_summarize: Generate AI summary (requires embeddings)

        Returns:
            None (side effects: session saved, memories consolidated)
        """
        # Get session data
        session_data = self._active_sessions.get(session_id, {})

        # Generate summary
        if auto_summarize:
            summary = self._generate_session_summary(
                session_id=session_id,
                agents_used=agents_used,
                decisions_made=decisions_made,
                session_data=session_data
            )
        else:
            summary = f"Session with {len(agents_used)} agents, {len(decisions_made)} decisions"

        # Save session
        self.memory.save_session(
            session_id=session_id,
            summary=summary,
            agents_used=agents_used,
            decisions=decisions_made
        )

        # Consolidate memories (remove duplicates, merge similar patterns)
        if self.memory.embeddings:
            self._consolidate_memories(session_id)

        # Clean up active session
        if session_id in self._active_sessions:
            del self._active_sessions[session_id]

    # HELPER METHODS

    def _load_project_state(self, project_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load project state from .research/project-state.yaml.

        Args:
            project_path: Path to project (uses memory.config.project_path if None)

        Returns:
            Dictionary with project state or empty dict
        """
        if project_path is None:
            project_path = self.memory.config.project_path

        if not project_path:
            return {}

        state_file = Path(project_path) / ".research" / "project-state.yaml"

        if not state_file.exists():
            return {}

        try:
            import yaml
            with open(state_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Failed to load project state: {e}")
            return {}

    def _update_project_state(
        self,
        checkpoint_id: str,
        stage: str,
        decision_data: Dict[str, Any]
    ) -> None:
        """
        Update project state file with checkpoint decision.

        Args:
            checkpoint_id: Checkpoint identifier
            stage: Research stage
            decision_data: Decision data dictionary
        """
        project_path = self.memory.config.project_path

        if not project_path:
            return

        project_dir = Path(project_path)
        research_dir = project_dir / ".research"
        research_dir.mkdir(exist_ok=True)

        state_file = research_dir / "project-state.yaml"

        # Load existing state
        state = self._load_project_state(project_path)

        # Update state
        state['current_stage'] = stage
        state['last_checkpoint'] = checkpoint_id
        state['last_updated'] = datetime.now().isoformat()

        # Add checkpoint-specific data
        if checkpoint_id not in state:
            state[checkpoint_id] = {}

        state[checkpoint_id].update(decision_data)

        # Save state
        try:
            import yaml
            with open(state_file, 'w', encoding='utf-8') as f:
                yaml.dump(state, f, allow_unicode=True, sort_keys=False)
        except Exception as e:
            print(f"Warning: Failed to update project state: {e}")

    def _infer_decision_type(self, checkpoint_id: str) -> DecisionType:
        """
        Infer decision type from checkpoint ID.

        Args:
            checkpoint_id: Checkpoint identifier

        Returns:
            DecisionType enum value
        """
        checkpoint_upper = checkpoint_id.upper()

        if 'PARADIGM' in checkpoint_upper or 'THEORY' in checkpoint_upper:
            return DecisionType.ARCHITECTURE
        elif 'DESIGN' in checkpoint_upper or 'METHOD' in checkpoint_upper:
            return DecisionType.DESIGN
        elif 'IMPLEMENTATION' in checkpoint_upper or 'CODING' in checkpoint_upper:
            return DecisionType.IMPLEMENTATION
        elif 'DEBUG' in checkpoint_upper or 'ERROR' in checkpoint_upper:
            return DecisionType.DEBUGGING
        elif 'REFACTOR' in checkpoint_upper or 'IMPROVE' in checkpoint_upper:
            return DecisionType.REFACTORING
        elif 'OPTIMIZE' in checkpoint_upper or 'PERFORMANCE' in checkpoint_upper:
            return DecisionType.OPTIMIZATION
        else:
            return DecisionType.DESIGN  # Default

    def _generate_session_summary(
        self,
        session_id: str,
        agents_used: List[str],
        decisions_made: List[str],
        session_data: Dict[str, Any]
    ) -> str:
        """
        Generate AI-powered session summary.

        Args:
            session_id: Session identifier
            agents_used: List of agent IDs
            decisions_made: List of checkpoint IDs
            session_data: Session tracking data

        Returns:
            Human-readable session summary
        """
        # Get session memories
        session_memories = self.memory.db.get_session_memories(session_id)

        # Build summary parts
        parts = []
        parts.append(f"Session {session_id}")
        parts.append(f"Agents: {', '.join(agents_used)}")
        parts.append(f"Decisions: {len(decisions_made)}")

        # Add key decisions
        if decisions_made:
            parts.append("Key checkpoints:")
            for checkpoint in decisions_made[:3]:  # Top 3
                parts.append(f"  - {checkpoint}")

        # Add memory count
        parts.append(f"Memories created: {len(session_memories)}")

        return " | ".join(parts)

    def _consolidate_memories(self, session_id: str) -> None:
        """
        Consolidate similar memories to reduce duplication.

        Uses embeddings to find similar memories and merge them.

        Args:
            session_id: Session identifier
        """
        # Get session memories
        session_memories = self.memory.db.get_session_memories(session_id)

        # TODO: Implement semantic deduplication using embeddings
        # For now, just log the intent
        if len(session_memories) > 10:
            print(f"Note: Session created {len(session_memories)} memories. "
                  "Consider consolidating similar memories.")


# Convenience functions for direct usage

_default_hooks = None


def get_default_hooks() -> MemoryHooks:
    """Get or create default hooks instance."""
    global _default_hooks
    if _default_hooks is None:
        _default_hooks = MemoryHooks()
    return _default_hooks


def on_session_start(
    project_path: Optional[str] = None,
    session_id: Optional[str] = None
) -> ContextInjection:
    """Convenience function for session start hook."""
    return get_default_hooks().on_session_start(project_path, session_id)


def on_checkpoint_reached(
    checkpoint_id: str,
    stage: str,
    agent_id: str,
    decision_data: Dict[str, Any],
    **kwargs
) -> None:
    """Convenience function for checkpoint hook."""
    return get_default_hooks().on_checkpoint_reached(
        checkpoint_id, stage, agent_id, decision_data, **kwargs
    )


def on_session_end(
    session_id: str,
    agents_used: List[str],
    decisions_made: List[str],
    **kwargs
) -> None:
    """Convenience function for session end hook."""
    return get_default_hooks().on_session_end(
        session_id, agents_used, decisions_made, **kwargs
    )


# Example usage for testing
if __name__ == "__main__":
    print("=== Diverga Memory Hooks Demo ===\n")

    # Initialize hooks
    hooks = MemoryHooks()

    # Session start
    print("1. Session Start")
    context = hooks.on_session_start(
        project_path="/Volumes/External SSD/Projects/Diverga",
        session_id="demo-session-001"
    )
    print(context.to_prompt())
    print()

    # Checkpoint reached
    print("2. Checkpoint Reached")
    hooks.on_checkpoint_reached(
        checkpoint_id="CP_PARADIGM_SELECTION",
        stage="foundation",
        agent_id="diverga:a5",
        decision_data={
            "decision": "Selected qualitative paradigm",
            "rationale": "Focus on lived experiences and contextual meaning",
            "before_state": "Undecided between quantitative and qualitative",
            "after_state": "Qualitative paradigm confirmed",
            "options_considered": [
                "Quantitative (T=0.8)",
                "Qualitative (T=0.5) - SELECTED",
                "Mixed methods (T=0.3)"
            ]
        },
        session_id="demo-session-001",
        t_score=0.5
    )
    print("✓ Checkpoint logged and decision saved\n")

    # Session end
    print("3. Session End")
    hooks.on_session_end(
        session_id="demo-session-001",
        agents_used=["diverga:a1", "diverga:a5"],
        decisions_made=["CP_PARADIGM_SELECTION"]
    )
    print("✓ Session summary generated and saved\n")

    print("=== Demo Complete ===")
