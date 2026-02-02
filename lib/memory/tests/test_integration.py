"""
Integration tests for DIVERGA Memory System.

Tests the complete flow of the memory system including:
- Store → Search → Retrieve → Export workflow
- Lifecycle hooks integration (session_start → checkpoint → session_end)
- Cross-platform path handling (Windows/Mac/Linux)
- Fallback embedding chain (Local → OpenAI → TF-IDF)
- SQLite FTS5 search functionality
- Namespace isolation (global vs project)

Uses temporary directories for test isolation.
"""

import pytest
import tempfile
import shutil
import json
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import List

# Import system modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database import MemoryDatabase
from memory_api import DivergeMemory, DivergeMemoryConfig
from embeddings import (
    EmbeddingProvider, EmbeddingManager, LocalEmbeddings,
    OpenAIEmbeddings, TFIDFEmbeddings
)
from hooks import (
    MemoryHooks, on_session_start, on_checkpoint_reached, on_session_end,
    ContextInjection
)
from exporter import MemoryExporter
from schema import (
    Memory, MemoryType, Decision, DecisionType, Priority,
    SearchScope, MemoryIndex, MemoryContext
)


# ========== FIXTURES ==========

@pytest.fixture
def temp_dir():
    """
    Create a temporary directory for test isolation.

    Automatically cleaned up after each test.
    """
    tmpdir = tempfile.mkdtemp(prefix="diverga_test_")
    yield Path(tmpdir)
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def db_path(temp_dir):
    """
    Create a temporary database path.

    Returns absolute path compatible with all platforms.
    """
    db_file = temp_dir / "test_memories.db"
    return str(db_file.resolve())


@pytest.fixture
def database(db_path):
    """
    Create a fresh MemoryDatabase instance for testing.

    Returns database with initialized schema.
    """
    db = MemoryDatabase(db_path)
    yield db
    # Cleanup handled by temp_dir fixture


@pytest.fixture
def memory(temp_dir):
    """
    Create a DivergeMemory instance with project scope.

    Uses temporary directory as project path.
    """
    config = DivergeMemoryConfig(
        project_path=str(temp_dir),
        enable_embeddings=True,
        embedding_cache=False,  # Disable cache for tests
        auto_detect_project=False
    )
    mem = DivergeMemory(config=config)
    yield mem


@pytest.fixture
def global_memory():
    """
    Create a DivergeMemory instance with global scope.

    Uses temporary directory for global storage.
    """
    tmpdir = tempfile.mkdtemp(prefix="diverga_global_")
    config = DivergeMemoryConfig(
        project_path=None,
        global_path=tmpdir,
        enable_embeddings=True,
        embedding_cache=False,
        auto_detect_project=False
    )
    mem = DivergeMemory(config=config)
    yield mem
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def hooks(memory):
    """
    Create MemoryHooks instance with test memory.
    """
    return MemoryHooks(memory=memory, auto_detect_project=False)


@pytest.fixture
def exporter(db_path):
    """
    Create MemoryExporter instance for testing.
    """
    return MemoryExporter(db_path)


# ========== COMPLETE FLOW TESTS ==========

class TestCompleteFlow:
    """
    Test the complete flow: store → search → retrieve → export.

    Verifies that memories can be created, searched, retrieved with context,
    and exported to various formats.
    """

    def test_store_search_retrieve_export_markdown(self, memory, exporter, temp_dir):
        """
        Test complete workflow ending with Markdown export.

        Flow:
        1. Store multiple memories with different types
        2. Search using FTS5
        3. Retrieve full memories
        4. Export to Markdown format
        5. Verify exported file contains expected content
        """
        # Step 1: Store memories
        mem1_id = memory.store(
            content="Used regression analysis for hypothesis testing",
            memory_type=MemoryType.DECISION,
            namespace="analysis.statistical",
            priority=Priority.HIGH,
            tags=["regression", "statistics"]
        )

        mem2_id = memory.store(
            content="Discovered pattern in qualitative coding process",
            memory_type=MemoryType.PATTERN,
            namespace="analysis.qualitative",
            priority=Priority.MEDIUM,
            tags=["coding", "themes"]
        )

        mem3_id = memory.store(
            content="Integration approach for mixed methods",
            memory_type=MemoryType.LEARNING,
            namespace="design.mixed_methods",
            priority=Priority.HIGH,
            tags=["integration", "mixed_methods"]
        )

        assert mem1_id is not None
        assert mem2_id is not None
        assert mem3_id is not None

        # Step 2: Search
        results = memory.search(
            query="analysis",
            scope=SearchScope.PROJECT,
            limit=10
        )

        assert len(results) >= 2  # Should find at least regression and qualitative
        assert all(isinstance(r, MemoryIndex) for r in results)

        # Step 3: Retrieve full memories
        full_memories = memory.retrieve([mem1_id, mem2_id])

        assert len(full_memories) == 2
        assert all(isinstance(m, Memory) for m in full_memories)
        assert full_memories[0].content == "Used regression analysis for hypothesis testing"

        # Step 4: Export to Markdown
        export_path = temp_dir / "export.md"
        result_path = exporter.export_markdown(
            output_path=str(export_path),
            namespace="analysis"
        )

        assert Path(result_path).exists()

        # Step 5: Verify exported content
        exported_content = Path(result_path).read_text(encoding='utf-8')
        assert "DIVERGA Memory Export" in exported_content
        assert "regression analysis" in exported_content
        assert "qualitative coding" in exported_content


    def test_store_search_retrieve_export_json(self, memory, exporter, temp_dir):
        """
        Test complete workflow ending with JSON export.

        Verifies JSON structure includes metadata, memories, and proper encoding.
        """
        # Store memories
        memory.store(
            content="Sample size calculation using G*Power",
            memory_type=MemoryType.DECISION,
            namespace="design.sampling",
            priority=Priority.CRITICAL,
            tags=["power_analysis", "sample_size"]
        )

        memory.store(
            content="Korean text handling: 한글 텍스트 처리 방법",
            memory_type=MemoryType.LEARNING,
            namespace="implementation.i18n",
            priority=Priority.MEDIUM,
            tags=["korean", "i18n"]
        )

        # Export to JSON
        export_path = temp_dir / "export.json"
        result_path = exporter.export_json(
            output_path=str(export_path),
            include_decisions=False,
            include_sessions=False,
            pretty=True
        )

        assert Path(result_path).exists()

        # Verify JSON structure
        with open(result_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        assert "meta" in data
        assert "memories" in data
        assert data["meta"]["total_memories"] >= 2

        # Verify Korean text encoding
        memory_contents = [m["content"] for m in data["memories"]]
        assert any("한글" in c for c in memory_contents)


    def test_search_with_context_retrieval(self, memory):
        """
        Test search → get_context workflow.

        Verifies that context retrieval includes:
        - Full memory details
        - Related memories in same namespace
        - Session context if available
        """
        # Store related memories in same namespace
        mem1_id = memory.store(
            content="Primary decision: Use qualitative approach",
            memory_type=MemoryType.DECISION,
            namespace="methodology.paradigm",
            priority=Priority.HIGH,
            session_id="test-session-001"
        )

        mem2_id = memory.store(
            content="Related pattern: Phenomenological interviews",
            memory_type=MemoryType.PATTERN,
            namespace="methodology.paradigm.phenomenology",
            priority=Priority.MEDIUM,
            session_id="test-session-001"
        )

        mem3_id = memory.store(
            content="Supporting context: Lived experience focus",
            memory_type=MemoryType.CONTEXT,
            namespace="methodology.paradigm.phenomenology",
            priority=Priority.LOW,
            session_id="test-session-001"
        )

        # Get context for primary decision
        context = memory.get_context(mem1_id)

        assert context is not None
        assert isinstance(context, MemoryContext)
        assert context.memory.id == str(mem1_id)
        assert len(context.related_memories) >= 1  # Should find at least mem2 or mem3
        assert context.session_context is not None  # Should detect session


# ========== LIFECYCLE HOOKS TESTS ==========

class TestLifecycleHooks:
    """
    Test lifecycle hooks integration: session_start → checkpoint → session_end.

    Verifies that hooks properly track sessions, decisions, and context.
    """

    def test_session_start_context_injection(self, hooks, memory):
        """
        Test session start hook with context injection.

        Verifies:
        - Session is created and tracked
        - Context is loaded from existing memories
        - ContextInjection contains expected sections
        """
        # Pre-populate some memories
        memory.store(
            content="Previous decision: Mixed methods design",
            memory_type=MemoryType.DECISION,
            namespace="decisions.design",
            priority=Priority.HIGH
        )

        memory.store(
            content="Key pattern: Sequential explanatory approach",
            memory_type=MemoryType.PATTERN,
            namespace="patterns.methodology",
            priority=Priority.HIGH
        )

        # Start session
        context = hooks.on_session_start(
            project_path=str(memory.config.project_path),
            session_id="integration-test-001"
        )

        assert isinstance(context, ContextInjection)
        assert context.project_name is not None

        # Verify context contains loaded memories
        prompt = context.to_prompt()
        assert "Research Context" in prompt
        assert "Do not re-ask for established information" in prompt


    def test_checkpoint_reached_decision_tracking(self, hooks, memory):
        """
        Test checkpoint hook with decision tracking.

        Verifies:
        - Decision is stored as memory
        - Project state is updated
        - Session tracking includes checkpoint
        """
        # Start session
        session_id = "checkpoint-test-001"
        hooks.on_session_start(
            project_path=str(memory.config.project_path),
            session_id=session_id
        )

        # Trigger checkpoint
        hooks.on_checkpoint_reached(
            checkpoint_id="CP_PARADIGM_SELECTION",
            stage="foundation",
            agent_id="diverga:a5",
            decision_data={
                "decision": "Selected qualitative paradigm",
                "rationale": "Focus on lived experiences",
                "before_state": "Undecided",
                "after_state": "Qualitative confirmed",
                "t_score": 0.5
            },
            session_id=session_id,
            t_score=0.5
        )

        # Verify decision was stored
        decisions = memory.db.get_memories_by_namespace(
            namespace="decisions.foundation",
            include_children=True,
            limit=10
        )

        assert len(decisions) >= 1
        assert any("qualitative paradigm" in d.get('content', '').lower() for d in decisions)

        # Verify session tracking
        session_data = hooks._active_sessions.get(session_id)
        assert session_data is not None
        assert len(session_data['checkpoints_reached']) == 1


    def test_session_end_summary_generation(self, hooks, memory):
        """
        Test session end hook with summary generation.

        Verifies:
        - Session summary is generated
        - Session is saved to database
        - Active session is cleaned up
        """
        session_id = "summary-test-001"

        # Start session
        hooks.on_session_start(session_id=session_id)

        # Reach checkpoint
        hooks.on_checkpoint_reached(
            checkpoint_id="CP_THEORY_SELECTION",
            stage="foundation",
            agent_id="diverga:a2",
            decision_data={"decision": "Selected SDT framework"},
            session_id=session_id
        )

        # End session
        hooks.on_session_end(
            session_id=session_id,
            agents_used=["diverga:a1", "diverga:a2"],
            decisions_made=["CP_THEORY_SELECTION"],
            auto_summarize=True
        )

        # Verify session was saved
        sessions = memory.db.get_recent_sessions(limit=5)
        assert len(sessions) >= 1

        saved_session = next((s for s in sessions if s['id'] == session_id), None)
        assert saved_session is not None
        assert saved_session['summary'] is not None
        assert "diverga:a1" in saved_session['agents_used']

        # Verify active session cleanup
        assert session_id not in hooks._active_sessions


    def test_complete_lifecycle_flow(self, hooks, memory, temp_dir):
        """
        Test complete lifecycle: start → multiple checkpoints → end.

        Simulates a realistic research session with multiple decisions.
        """
        session_id = "lifecycle-flow-001"

        # 1. Session Start
        context = hooks.on_session_start(
            project_path=str(temp_dir),
            session_id=session_id
        )
        assert context is not None

        # 2. Multiple Checkpoints
        checkpoints = [
            ("CP_PARADIGM_SELECTION", "foundation", "diverga:a5",
             {"decision": "Qualitative paradigm"}),
            ("CP_THEORY_SELECTION", "foundation", "diverga:a2",
             {"decision": "Grounded theory"}),
            ("CP_METHODOLOGY_APPROVAL", "design", "diverga:c2",
             {"decision": "Interview-based data collection"})
        ]

        for cp_id, stage, agent, data in checkpoints:
            hooks.on_checkpoint_reached(
                checkpoint_id=cp_id,
                stage=stage,
                agent_id=agent,
                decision_data=data,
                session_id=session_id
            )

        # 3. Session End
        hooks.on_session_end(
            session_id=session_id,
            agents_used=["diverga:a5", "diverga:a2", "diverga:c2"],
            decisions_made=[cp[0] for cp in checkpoints]
        )

        # Verify all decisions were stored
        all_decisions = memory.db.get_memories_by_namespace(
            namespace="decisions",
            include_children=True,
            limit=50
        )

        assert len(all_decisions) >= 3

        # Verify session summary
        sessions = memory.db.get_recent_sessions(limit=1)
        assert len(sessions) == 1
        assert "3" in sessions[0]['summary'] or len(sessions[0]['agents_used']) == 3


# ========== CROSS-PLATFORM PATH TESTS ==========

class TestCrossPlatformPaths:
    """
    Test cross-platform path handling (Windows/Mac/Linux).

    Verifies that paths are correctly resolved on all platforms.
    """

    def test_path_resolution_unix(self, temp_dir):
        """
        Test path resolution on Unix-like systems (Mac/Linux).

        Verifies:
        - Absolute paths are correctly resolved
        - Forward slashes work
        - Home directory expansion works
        """
        # Create database with Unix-style path
        db_path = temp_dir / "unix" / "test.db"
        db = MemoryDatabase(str(db_path))

        assert db.db_path.exists()
        assert db.db_path.is_absolute()
        assert str(db.db_path).startswith("/")  # Unix absolute path


    def test_path_resolution_relative(self, temp_dir):
        """
        Test that relative paths are converted to absolute.

        Prevents issues with changing working directory.
        """
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(str(temp_dir))

        try:
            # Create with relative path
            db = MemoryDatabase("relative/test.db")

            # Should be absolute
            assert db.db_path.is_absolute()
            assert str(db.db_path).startswith(str(temp_dir))
        finally:
            os.chdir(original_cwd)


    def test_path_special_characters(self, temp_dir):
        """
        Test paths with spaces and special characters.

        Common on Windows ("Program Files") and user directories.
        """
        special_dir = temp_dir / "path with spaces" / "special-chars_123"
        db_path = special_dir / "test.db"

        db = MemoryDatabase(str(db_path))

        assert db.db_path.exists()
        assert "path with spaces" in str(db.db_path)


# ========== EMBEDDING FALLBACK TESTS ==========

class TestEmbeddingFallback:
    """
    Test fallback embedding chain: Local → OpenAI → TF-IDF.

    Verifies that the system gracefully falls back when providers fail.
    """

    def test_embedding_manager_auto_detection(self):
        """
        Test EmbeddingManager auto-detects best available provider.

        Should try Local → OpenAI → TF-IDF in order.
        """
        manager = EmbeddingManager(enable_cache=False)

        # Should have selected SOME provider
        assert manager.provider is not None
        assert manager.provider_name in ["local:all-MiniLM-L6-v2", "openai:text-embedding-3-small", "tfidf"]


    def test_tfidf_fallback_works(self):
        """
        Test that TF-IDF fallback always works (no external dependencies).

        This ensures the system never completely fails.
        """
        provider = TFIDFEmbeddings(max_features=384)

        # Should work without any setup
        embedding = provider.embed("Test text for embedding")

        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert all(isinstance(x, float) for x in embedding)


    def test_embedding_similarity_calculation(self):
        """
        Test embedding similarity calculation across providers.

        Verifies cosine similarity is computed correctly.
        """
        manager = EmbeddingManager(enable_cache=False)

        # Similar texts
        emb1 = manager.embed("Machine learning and AI")
        emb2 = manager.embed("Artificial intelligence and ML")

        # Different text
        emb3 = manager.embed("Cooking recipes and food")

        # Similarity should be higher for similar texts
        sim_similar = manager.similarity(emb1, emb2)
        sim_different = manager.similarity(emb1, emb3)

        assert sim_similar > sim_different
        assert 0 <= sim_similar <= 1
        assert 0 <= sim_different <= 1


    def test_memory_search_with_embeddings(self, memory):
        """
        Test semantic search using embeddings.

        Verifies that embeddings improve search quality.
        """
        # Store semantically related memories
        memory.store(
            content="Neural networks are the foundation of deep learning",
            memory_type=MemoryType.LEARNING,
            namespace="ml.deep_learning",
            priority=Priority.HIGH
        )

        memory.store(
            content="Convolutional neural networks excel at image processing",
            memory_type=MemoryType.PATTERN,
            namespace="ml.deep_learning.cnn",
            priority=Priority.MEDIUM
        )

        memory.store(
            content="Statistical hypothesis testing requires p-values",
            memory_type=MemoryType.LEARNING,
            namespace="statistics.hypothesis",
            priority=Priority.MEDIUM
        )

        # Search with semantic query
        results = memory.search(
            query="artificial intelligence neural nets",
            limit=5
        )

        # Should find ML-related memories
        assert len(results) >= 2

        # Top result should be most relevant
        top_result = results[0]
        assert "neural" in top_result.preview.lower() or "learning" in top_result.preview.lower()


# ========== FTS5 SEARCH TESTS ==========

class TestFTS5Search:
    """
    Test SQLite FTS5 full-text search functionality.

    Verifies search queries, ranking, and filtering.
    """

    def test_fts5_basic_search(self, database):
        """
        Test basic FTS5 search with single term.

        Verifies that FTS5 index is created and searchable.
        """
        # Store test memories
        database.store_memory(
            memory_type="learning",
            namespace="test",
            title="Regression Analysis",
            content="Linear regression is used for predicting continuous outcomes",
            priority=5
        )

        database.store_memory(
            memory_type="pattern",
            namespace="test",
            title="Correlation Study",
            content="Correlation analysis measures relationship strength",
            priority=5
        )

        # Search
        results = database.search_memories(query="regression", limit=10)

        assert len(results) >= 1
        assert any("regression" in r['content'].lower() for r in results)


    def test_fts5_phrase_search(self, database):
        """
        Test FTS5 phrase search with quotes.

        FTS5 supports "exact phrase" matching.
        """
        database.store_memory(
            memory_type="learning",
            namespace="test",
            title="Meta Analysis",
            content="Meta analysis combines results from multiple studies",
            priority=5
        )

        database.store_memory(
            memory_type="learning",
            namespace="test",
            title="Analysis Methods",
            content="Various analysis methods exist for different data types",
            priority=5
        )

        # Exact phrase search
        results = database.search_memories(query='"meta analysis"', limit=10)

        assert len(results) >= 1
        assert any("meta analysis" in r['content'].lower() for r in results)


    def test_fts5_boolean_operators(self, database):
        """
        Test FTS5 boolean operators (AND, OR, NOT).

        Verifies complex query support.
        """
        database.store_memory(
            memory_type="learning",
            namespace="test",
            title="Quantitative Methods",
            content="Quantitative research uses statistical analysis",
            priority=5
        )

        database.store_memory(
            memory_type="learning",
            namespace="test",
            title="Qualitative Methods",
            content="Qualitative research uses thematic analysis",
            priority=5
        )

        # AND search
        results = database.search_memories(query="research AND statistical", limit=10)
        assert len(results) >= 1

        # NOT search
        results = database.search_memories(query="research NOT qualitative", limit=10)
        quantitative_found = any("quantitative" in r['content'].lower() for r in results)
        assert quantitative_found


    def test_fts5_with_namespace_filter(self, database):
        """
        Test FTS5 search combined with namespace filtering.

        Verifies that filters work together.
        """
        database.store_memory(
            memory_type="decision",
            namespace="project.analysis",
            title="Statistical Decision",
            content="Chose ANOVA for multi-group comparison",
            priority=8
        )

        database.store_memory(
            memory_type="decision",
            namespace="project.design",
            title="Design Decision",
            content="Selected experimental design approach",
            priority=8
        )

        # Search with namespace filter
        results = database.search_memories(
            query="decision",
            namespace="project.analysis",
            limit=10
        )

        assert len(results) >= 1
        assert all(r['namespace'].startswith("project.analysis") for r in results)


# ========== NAMESPACE ISOLATION TESTS ==========

class TestNamespaceIsolation:
    """
    Test namespace isolation between global and project scopes.

    Verifies that memories are properly scoped and don't leak.
    """

    def test_project_vs_global_isolation(self, memory, global_memory):
        """
        Test that project and global memories are isolated.

        Verifies:
        - Project memories stored separately
        - Global memories stored separately
        - No cross-contamination
        """
        # Store in project scope
        project_id = memory.store(
            content="Project-specific learning",
            memory_type=MemoryType.LEARNING,
            namespace="project.specific",
            priority=Priority.HIGH
        )

        # Store in global scope
        global_id = global_memory.store(
            content="Global reusable pattern",
            memory_type=MemoryType.PATTERN,
            namespace="global.patterns",
            priority=Priority.HIGH
        )

        # Search in project scope - should NOT find global
        project_results = memory.search(
            query="pattern",
            scope=SearchScope.PROJECT,
            limit=10
        )

        # Should not find global memory
        assert all(r.id != str(global_id) for r in project_results)

        # Search in global scope - should NOT find project
        global_results = global_memory.search(
            query="learning",
            scope=SearchScope.GLOBAL,
            limit=10
        )

        # Should not find project memory
        assert all(r.id != str(project_id) for r in global_results)


    def test_namespace_hierarchy(self, memory):
        """
        Test hierarchical namespace querying.

        Verifies:
        - Child namespaces are found with include_children=True
        - Exact matching works with include_children=False
        """
        # Store in hierarchical namespaces
        memory.store(
            content="Root level",
            memory_type=MemoryType.LEARNING,
            namespace="methodology",
            priority=Priority.HIGH
        )

        memory.store(
            content="Child level",
            memory_type=MemoryType.LEARNING,
            namespace="methodology.qualitative",
            priority=Priority.HIGH
        )

        memory.store(
            content="Grandchild level",
            memory_type=MemoryType.LEARNING,
            namespace="methodology.qualitative.phenomenology",
            priority=Priority.HIGH
        )

        # Query with children
        all_results = memory.db.get_memories_by_namespace(
            namespace="methodology",
            include_children=True,
            limit=50
        )

        assert len(all_results) == 3

        # Query without children (exact match)
        exact_results = memory.db.get_memories_by_namespace(
            namespace="methodology",
            include_children=False,
            limit=50
        )

        assert len(exact_results) == 1


    def test_namespace_scoped_search(self, memory):
        """
        Test that search can be scoped to specific namespace.

        Useful for finding memories in specific project areas.
        """
        # Store in different namespaces
        memory.store(
            content="Statistical analysis method",
            memory_type=MemoryType.LEARNING,
            namespace="analysis.quantitative",
            priority=Priority.HIGH
        )

        memory.store(
            content="Thematic analysis method",
            memory_type=MemoryType.LEARNING,
            namespace="analysis.qualitative",
            priority=Priority.HIGH
        )

        # Search only in quantitative namespace
        quant_results = memory.db.search_memories(
            query="analysis",
            namespace="analysis.quantitative",
            limit=10
        )

        assert len(quant_results) >= 1
        assert all(r['namespace'].startswith("analysis.quantitative") for r in quant_results)


# ========== PERFORMANCE & STRESS TESTS ==========

class TestPerformance:
    """
    Test system performance with larger datasets.

    Not run by default - use pytest -m stress to run.
    """

    @pytest.mark.stress
    def test_bulk_insert_performance(self, memory):
        """
        Test performance with bulk memory insertion.

        Inserts 1000 memories and measures time.
        """
        import time

        start = time.time()

        for i in range(1000):
            memory.store(
                content=f"Test memory {i} with some content for searching",
                memory_type=MemoryType.LEARNING,
                namespace=f"test.batch_{i % 10}",
                priority=Priority.MEDIUM,
                tags=[f"tag_{i % 5}"]
            )

        elapsed = time.time() - start

        # Should complete in reasonable time (< 30 seconds)
        assert elapsed < 30
        print(f"\nBulk insert (1000 memories): {elapsed:.2f}s ({1000/elapsed:.1f} memories/sec)")


    @pytest.mark.stress
    def test_search_performance_large_dataset(self, memory):
        """
        Test search performance with large dataset.

        Verifies FTS5 index performance.
        """
        import time

        # Insert 500 memories
        for i in range(500):
            memory.store(
                content=f"Research finding {i} about various topics including AI, ML, statistics, and analysis methods",
                memory_type=MemoryType.LEARNING,
                namespace=f"research.topic_{i % 10}",
                priority=Priority.MEDIUM
            )

        # Measure search time
        start = time.time()
        results = memory.search(query="research AI statistics", limit=20)
        elapsed = time.time() - start

        # Should complete in < 1 second
        assert elapsed < 1.0
        assert len(results) > 0
        print(f"\nSearch on 500 memories: {elapsed:.3f}s")


# ========== ERROR HANDLING TESTS ==========

class TestErrorHandling:
    """
    Test error handling and edge cases.
    """

    def test_invalid_memory_type(self, memory):
        """
        Test that invalid memory type raises error.
        """
        with pytest.raises(AttributeError):
            memory.store(
                content="Test",
                memory_type="invalid_type",  # Not a valid MemoryType
                namespace="test"
            )


    def test_retrieve_nonexistent_memory(self, memory):
        """
        Test retrieving non-existent memory returns empty list.
        """
        results = memory.retrieve(["99999"])
        assert len(results) == 0


    def test_search_empty_database(self, memory):
        """
        Test search on empty database returns empty results.
        """
        results = memory.search("nonexistent query")
        assert len(results) == 0


    def test_export_empty_database(self, exporter, temp_dir):
        """
        Test exporting empty database creates valid file.
        """
        export_path = temp_dir / "empty_export.md"
        result_path = exporter.export_markdown(str(export_path))

        assert Path(result_path).exists()

        content = Path(result_path).read_text()
        assert "DIVERGA Memory Export" in content
        assert "Total Memories: 0" in content


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
