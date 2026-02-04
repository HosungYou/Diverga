"""
Diverga Memory System v8.0 - Hybrid Search

FTS5 + numpy cosine similarity for hybrid search.

This module provides:
- Full-text search using SQLite FTS5
- Vector similarity search using numpy (fallback from sqlite-vec)
- RRF (Reciprocal Rank Fusion) for score combination

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

import json
from typing import Optional, List, Dict, Any, Tuple, TYPE_CHECKING

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

if TYPE_CHECKING:
    from .database import MemoryDatabase
    from .local_embedder import LocalEmbedder


class HybridSearch:
    """
    Hybrid search combining FTS5 and vector similarity.

    Uses numpy for vector operations (fallback from sqlite-vec).
    Combines results using Reciprocal Rank Fusion (RRF).

    Attributes:
        db: MemoryDatabase instance
        embedder: Optional LocalEmbedder for vector search
    """

    def __init__(
        self,
        db: "MemoryDatabase",
        embedder: Optional["LocalEmbedder"] = None
    ):
        """
        Initialize hybrid search.

        Args:
            db: MemoryDatabase instance
            embedder: Optional embedder for vector search
        """
        self.db = db
        self.embedder = embedder

    def search(
        self,
        query: str,
        top_k: int = 10,
        namespace: Optional[str] = None,
        memory_type: Optional[str] = None,
        fts_weight: float = 0.5,
        vector_weight: float = 0.5,
        query_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid search combining FTS5 and vector similarity.

        Args:
            query: Search query string
            top_k: Maximum number of results
            namespace: Filter by namespace prefix
            memory_type: Filter by memory type
            fts_weight: Weight for FTS5 results (0-1)
            vector_weight: Weight for vector results (0-1)
            query_type: Query type for weight presets:
                - "decision": FTS=30%, Vector=70%
                - "methodology": FTS=50%, Vector=50%
                - "citation": FTS=70%, Vector=30%
                - "general": FTS=50%, Vector=50%

        Returns:
            List of memory dictionaries with combined scores
        """
        # Apply query type presets
        if query_type:
            fts_weight, vector_weight = self._get_query_weights(query_type)

        # Normalize weights
        total = fts_weight + vector_weight
        fts_weight = fts_weight / total
        vector_weight = vector_weight / total

        # Get FTS5 results
        fts_results = self._fts_search(query, namespace, memory_type, top_k * 2)

        # Get vector results if embedder available
        vector_results = []
        if self.embedder and HAS_NUMPY:
            vector_results = self._vector_search(query, namespace, memory_type, top_k * 2)

        # Combine using RRF
        combined = self._rrf_fusion(fts_results, vector_results, fts_weight, vector_weight)

        return combined[:top_k]

    def search_decisions(
        self,
        query: str,
        top_k: int = 10,
        checkpoint: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search decisions with semantic matching.

        Args:
            query: Search query
            top_k: Maximum results
            checkpoint: Optional checkpoint filter

        Returns:
            List of matching decisions
        """
        namespace = f"decisions.{checkpoint}" if checkpoint else "decisions"
        return self.search(
            query,
            top_k=top_k,
            namespace=namespace,
            memory_type="decision",
            query_type="decision"
        )

    def find_similar_memories(
        self,
        memory_id: int,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find memories similar to a given memory.

        Args:
            memory_id: Source memory ID
            top_k: Maximum results

        Returns:
            List of similar memories (excluding source)
        """
        # Get source memory
        source = self.db.get_memory(memory_id)
        if not source:
            return []

        # Use title + content as query
        query = f"{source.get('title', '')} {source.get('content', '')[:500]}"

        # Search for similar
        results = self.search(
            query,
            top_k=top_k + 1,  # Account for self
            namespace=source.get('namespace', '').split('.')[0],
            memory_type=source.get('memory_type')
        )

        # Filter out self
        return [r for r in results if r.get('id') != memory_id][:top_k]

    def _fts_search(
        self,
        query: str,
        namespace: Optional[str],
        memory_type: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Perform FTS5 full-text search.

        Args:
            query: Search query
            namespace: Namespace filter
            memory_type: Type filter
            limit: Maximum results

        Returns:
            List of results with FTS rank scores
        """
        try:
            results = self.db.search_memories(
                query=query,
                namespace=namespace,
                memory_type=memory_type,
                limit=limit
            )

            # Add rank-based scores
            for i, result in enumerate(results):
                result['fts_rank'] = i + 1
                result['fts_score'] = 1.0 / (i + 1)  # Simple rank-based score

            return results
        except Exception as e:
            print(f"Warning: FTS search error: {e}")
            return []

    def _vector_search(
        self,
        query: str,
        namespace: Optional[str],
        memory_type: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search using numpy.

        Args:
            query: Search query
            namespace: Namespace filter
            memory_type: Type filter
            limit: Maximum results

        Returns:
            List of results with vector similarity scores
        """
        if not self.embedder or not HAS_NUMPY:
            return []

        try:
            # Get query embedding
            query_embedding = self.embedder.embed(query)
            if query_embedding is None:
                return []

            # Load all embeddings from DB (filtered by namespace/type)
            candidates = self._load_embeddings_from_db(namespace, memory_type)
            if not candidates:
                return []

            # Calculate cosine similarities
            similarities = []
            for memory_id, embedding in candidates:
                sim = self._cosine_similarity(query_embedding, embedding)
                similarities.append((memory_id, sim))

            # Sort by similarity
            similarities.sort(key=lambda x: x[1], reverse=True)

            # Get full memory data for top results
            results = []
            for memory_id, sim in similarities[:limit]:
                memory = self.db.get_memory(memory_id)
                if memory:
                    memory['vector_score'] = float(sim)
                    memory['vector_rank'] = len(results) + 1
                    results.append(memory)

            return results
        except Exception as e:
            print(f"Warning: Vector search error: {e}")
            return []

    def _load_embeddings_from_db(
        self,
        namespace: Optional[str],
        memory_type: Optional[str]
    ) -> List[Tuple[int, np.ndarray]]:
        """
        Load embeddings from database.

        Args:
            namespace: Namespace filter
            memory_type: Type filter

        Returns:
            List of (memory_id, embedding) tuples
        """
        # This is a simple implementation that loads all embeddings
        # For large datasets, consider chunking or indexing strategies

        with self.db._get_connection() as conn:
            cursor = conn.cursor()

            sql = """
                SELECT id, embedding FROM memories
                WHERE status = 'active' AND embedding IS NOT NULL
            """
            params = []

            if namespace:
                sql += " AND namespace LIKE ?"
                params.append(f"{namespace}%")

            if memory_type:
                sql += " AND memory_type = ?"
                params.append(memory_type)

            cursor.execute(sql, params)
            rows = cursor.fetchall()

            results = []
            for row in rows:
                memory_id = row[0]
                embedding_blob = row[1]
                if embedding_blob:
                    try:
                        # Assuming embedding is stored as float32 array
                        embedding = np.frombuffer(embedding_blob, dtype=np.float32)
                        results.append((memory_id, embedding))
                    except Exception:
                        pass

            return results

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            a: First vector
            b: Second vector

        Returns:
            Cosine similarity (-1 to 1)
        """
        if a.shape != b.shape:
            return 0.0

        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)

        if norm_a == 0 or norm_b == 0:
            return 0.0

        return float(dot_product / (norm_a * norm_b))

    def _rrf_fusion(
        self,
        fts_results: List[Dict[str, Any]],
        vector_results: List[Dict[str, Any]],
        fts_weight: float,
        vector_weight: float,
        k: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Combine results using Reciprocal Rank Fusion.

        RRF formula: score = sum(1 / (k + rank))

        Args:
            fts_results: FTS5 search results
            vector_results: Vector search results
            fts_weight: Weight for FTS results
            vector_weight: Weight for vector results
            k: RRF constant (default 60)

        Returns:
            Combined and re-ranked results
        """
        scores: Dict[int, Dict[str, Any]] = {}

        # Process FTS results
        for i, result in enumerate(fts_results):
            memory_id = result.get('id')
            if memory_id is None:
                continue

            rank = i + 1
            rrf_score = fts_weight * (1.0 / (k + rank))

            if memory_id not in scores:
                scores[memory_id] = {
                    'memory': result,
                    'rrf_score': 0.0,
                    'fts_rank': rank,
                    'vector_rank': None
                }
            scores[memory_id]['rrf_score'] += rrf_score
            scores[memory_id]['fts_rank'] = rank

        # Process vector results
        for i, result in enumerate(vector_results):
            memory_id = result.get('id')
            if memory_id is None:
                continue

            rank = i + 1
            rrf_score = vector_weight * (1.0 / (k + rank))

            if memory_id not in scores:
                scores[memory_id] = {
                    'memory': result,
                    'rrf_score': 0.0,
                    'fts_rank': None,
                    'vector_rank': rank
                }
            scores[memory_id]['rrf_score'] += rrf_score
            scores[memory_id]['vector_rank'] = rank

        # Sort by combined score
        sorted_results = sorted(
            scores.values(),
            key=lambda x: x['rrf_score'],
            reverse=True
        )

        # Build final results
        final_results = []
        for item in sorted_results:
            result = item['memory'].copy()
            result['combined_score'] = item['rrf_score']
            result['fts_rank'] = item['fts_rank']
            result['vector_rank'] = item['vector_rank']
            final_results.append(result)

        return final_results

    def _get_query_weights(self, query_type: str) -> Tuple[float, float]:
        """
        Get FTS/vector weights for query type.

        Args:
            query_type: Type of query

        Returns:
            Tuple of (fts_weight, vector_weight)
        """
        presets = {
            "decision": (0.3, 0.7),      # Conceptual matching important
            "methodology": (0.5, 0.5),   # Balanced
            "citation": (0.7, 0.3),      # Exact keywords important
            "general": (0.5, 0.5),       # Default balanced
        }
        return presets.get(query_type, (0.5, 0.5))


def create_hybrid_search(
    db: "MemoryDatabase",
    enable_embeddings: bool = False
) -> HybridSearch:
    """
    Factory function to create HybridSearch instance.

    Args:
        db: MemoryDatabase instance
        enable_embeddings: Whether to enable vector search

    Returns:
        HybridSearch instance
    """
    embedder = None

    if enable_embeddings:
        try:
            from .local_embedder import LocalEmbedder
            embedder = LocalEmbedder()
        except ImportError:
            print("Warning: sentence-transformers not available for vector search")

    return HybridSearch(db, embedder)
