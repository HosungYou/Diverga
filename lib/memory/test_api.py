"""Test script for Diverga Memory API."""
import sys
import tempfile
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from database import MemoryDatabase
from embeddings import EmbeddingManager
from schema import MemoryType, Priority, DecisionType, SearchScope
from memory_api import DivergeMemory, DivergeMemoryConfig

def test_memory_api():
    """Run comprehensive tests on Memory API."""
    print("=== Testing Diverga Memory API ===\n")
    
    # Create temp directory for testing
    temp_dir = tempfile.mkdtemp()
    print(f"Test directory: {temp_dir}\n")
    
    try:
        # Initialize memory
        config = DivergeMemoryConfig(
            project_path=temp_dir,
            enable_embeddings=False,  # Disable for quick test
            auto_detect_project=False
        )
        
        memory = DivergeMemory(config=config)
        print(f"✅ DivergeMemory initialized (scope: {memory.scope})\n")
        
        # Test 1: Store memory
        print("Test 1: Store memory")
        memory_id = memory.store(
            content="Used regression analysis to test hypothesis about learning outcomes",
            memory_type=MemoryType.DECISION,
            namespace="analysis.statistical",
            priority=Priority.HIGH,
            tags=["regression", "hypothesis-testing"],
            agent_id="diverga:e1"
        )
        print(f"✅ Stored memory ID: {memory_id}\n")
        
        # Test 2: Search (Layer 1)
        print("Test 2: Search memories")
        results = memory.search("regression", limit=5)
        print(f"✅ Found {len(results)} results")
        if results:
            print(f"   First result: {results[0].title[:50]}...\n")
        
        # Test 3: Get context (Layer 2)
        print("Test 3: Get context")
        context = memory.get_context(memory_id)
        if context:
            print(f"✅ Retrieved context for memory")
            print(f"   Related memories: {len(context.related_memories)}\n")
        
        # Test 4: Retrieve full (Layer 3)
        print("Test 4: Retrieve full memory")
        full_memories = memory.retrieve([memory_id])
        if full_memories:
            print(f"✅ Retrieved {len(full_memories)} full memories")
            print(f"   Content length: {len(full_memories[0].content)} chars\n")
        
        # Test 5: Record decision
        print("Test 5: Record decision")
        decision_id = memory.record_decision(
            stage="analysis",
            agent_id="diverga:e1",
            decision_type=DecisionType.DESIGN,
            description="Chose linear regression over logistic",
            rationale="Outcome is continuous, not binary",
            t_score=0.65
        )
        print(f"✅ Recorded decision ID: {decision_id}\n")
        
        # Test 6: Session management
        print("Test 6: Save session")
        session_id = memory.save_session(
            session_id="test-session-001",
            summary="Statistical analysis session",
            agents_used=["diverga:e1", "diverga:c1"]
        )
        print(f"✅ Saved session ID: {session_id}\n")
        
        # Test 7: Project context
        print("Test 7: Get project context")
        proj_context = memory.get_project_context()
        print(f"✅ Project context:")
        print(f"   Total memories: {proj_context['total_memories']}")
        print(f"   Recent decisions: {len(proj_context['recent_decisions'])}\n")
        
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    success = test_memory_api()
    sys.exit(0 if success else 1)
