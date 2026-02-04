"""
Diverga Memory System v8.0 - Local Embedder

Wrapper for sentence-transformers to generate embeddings locally.

Features:
- Zero API cost (runs locally)
- Lightweight model (all-MiniLM-L6-v2, ~90MB)
- Batch processing support
- Caching for repeated queries

Author: Diverga Project
Version: 8.0.0
"""

from __future__ import annotations

from typing import Optional, List, Union
from functools import lru_cache

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    np = None
    HAS_NUMPY = False

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    SentenceTransformer = None
    HAS_SENTENCE_TRANSFORMERS = False


class LocalEmbedder:
    """
    Local embedding generator using sentence-transformers.

    Uses the all-MiniLM-L6-v2 model by default (good balance
    of quality and speed for research contexts).

    Attributes:
        model_name: Name of the sentence-transformer model
        model: Loaded SentenceTransformer model
    """

    # Default model - good for research/academic text
    DEFAULT_MODEL = "all-MiniLM-L6-v2"

    # Alternative models
    MODELS = {
        "fast": "all-MiniLM-L6-v2",       # 384 dim, fast, good quality
        "accurate": "all-mpnet-base-v2",   # 768 dim, slower, better quality
        "multilingual": "paraphrase-multilingual-MiniLM-L12-v2",  # 384 dim, multi-lang
        "scientific": "allenai-specter",   # 768 dim, scientific papers
    }

    def __init__(
        self,
        model_name: Optional[str] = None,
        cache_size: int = 1000
    ):
        """
        Initialize local embedder.

        Args:
            model_name: Model name or preset (fast, accurate, multilingual, scientific)
            cache_size: Number of embeddings to cache

        Raises:
            ImportError: If sentence-transformers not installed
        """
        if not HAS_SENTENCE_TRANSFORMERS:
            raise ImportError(
                "sentence-transformers not installed. "
                "Run: pip install -r lib/memory/requirements-embeddings.txt"
            )

        if not HAS_NUMPY:
            raise ImportError("numpy required for embeddings")

        # Resolve model name from presets
        if model_name in self.MODELS:
            model_name = self.MODELS[model_name]
        elif model_name is None:
            model_name = self.DEFAULT_MODEL

        self.model_name = model_name
        self._model: Optional[SentenceTransformer] = None
        self._cache_size = cache_size

    @property
    def model(self) -> SentenceTransformer:
        """Lazy-load the model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model

    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> Optional[np.ndarray]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding as numpy array, or None on error
        """
        try:
            # Use cached version
            return self._embed_cached(text)
        except Exception as e:
            print(f"Warning: Embedding error: {e}")
            return None

    @lru_cache(maxsize=1000)
    def _embed_cached(self, text: str) -> np.ndarray:
        """
        Cached embedding generation.

        Args:
            text: Text to embed

        Returns:
            Embedding as numpy array
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.astype(np.float32)

    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[np.ndarray]:
        """
        Generate embeddings for multiple texts.

        More efficient than calling embed() repeatedly.

        Args:
            texts: List of texts to embed
            batch_size: Batch size for processing

        Returns:
            List of embeddings as numpy arrays
        """
        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=len(texts) > 100
            )
            return [emb.astype(np.float32) for emb in embeddings]
        except Exception as e:
            print(f"Warning: Batch embedding error: {e}")
            return []

    def embed_to_bytes(self, text: str) -> Optional[bytes]:
        """
        Generate embedding and convert to bytes for storage.

        Args:
            text: Text to embed

        Returns:
            Embedding as bytes (float32), or None on error
        """
        embedding = self.embed(text)
        if embedding is not None:
            return embedding.tobytes()
        return None

    def bytes_to_embedding(self, data: bytes) -> Optional[np.ndarray]:
        """
        Convert bytes back to embedding array.

        Args:
            data: Bytes from embed_to_bytes()

        Returns:
            Embedding as numpy array, or None on error
        """
        try:
            return np.frombuffer(data, dtype=np.float32)
        except Exception:
            return None

    def similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Cosine similarity (-1 to 1)
        """
        emb1 = self.embed(text1)
        emb2 = self.embed(text2)

        if emb1 is None or emb2 is None:
            return 0.0

        dot_product = np.dot(emb1, emb2)
        norm1 = np.linalg.norm(emb1)
        norm2 = np.linalg.norm(emb2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def find_most_similar(
        self,
        query: str,
        candidates: List[str],
        top_k: int = 5
    ) -> List[tuple]:
        """
        Find most similar texts from candidates.

        Args:
            query: Query text
            candidates: List of candidate texts
            top_k: Number of results

        Returns:
            List of (index, text, similarity) tuples
        """
        query_emb = self.embed(query)
        if query_emb is None:
            return []

        candidate_embs = self.embed_batch(candidates)
        if not candidate_embs:
            return []

        # Calculate similarities
        similarities = []
        for i, (text, emb) in enumerate(zip(candidates, candidate_embs)):
            dot_product = np.dot(query_emb, emb)
            norm_q = np.linalg.norm(query_emb)
            norm_c = np.linalg.norm(emb)

            if norm_q > 0 and norm_c > 0:
                sim = float(dot_product / (norm_q * norm_c))
            else:
                sim = 0.0

            similarities.append((i, text, sim))

        # Sort by similarity
        similarities.sort(key=lambda x: x[2], reverse=True)

        return similarities[:top_k]

    def clear_cache(self):
        """Clear the embedding cache."""
        self._embed_cached.cache_clear()

    def get_cache_info(self) -> dict:
        """Get cache statistics."""
        info = self._embed_cached.cache_info()
        return {
            "hits": info.hits,
            "misses": info.misses,
            "size": info.currsize,
            "maxsize": info.maxsize
        }


def is_embeddings_available() -> bool:
    """
    Check if embeddings are available.

    Returns:
        True if sentence-transformers is installed
    """
    return HAS_SENTENCE_TRANSFORMERS and HAS_NUMPY


def get_recommended_model(use_case: str = "general") -> str:
    """
    Get recommended model for a use case.

    Args:
        use_case: Use case (general, scientific, multilingual, fast, accurate)

    Returns:
        Model name
    """
    models = {
        "general": "all-MiniLM-L6-v2",
        "fast": "all-MiniLM-L6-v2",
        "accurate": "all-mpnet-base-v2",
        "scientific": "allenai-specter",
        "multilingual": "paraphrase-multilingual-MiniLM-L12-v2",
    }
    return models.get(use_case, models["general"])
