"""
Cross-platform embedding system with multiple provider fallbacks.

Provider chain:
1. LocalEmbeddings (sentence-transformers) - Best quality, offline
2. OpenAIEmbeddings (API) - Good quality, requires API key
3. TFIDFEmbeddings (fallback) - Basic similarity, always works

All providers implement the same interface for seamless fallback.
"""

import hashlib
import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Tuple, Optional, Dict, Any
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass

    @property
    @abstractmethod
    def dimension(self) -> int:
        """Return embedding dimension."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return provider name."""
        pass


class LocalEmbeddings(EmbeddingProvider):
    """Sentence-transformers based local embeddings."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize local embedding model.

        Args:
            model_name: HuggingFace model name (default is small, fast model)
        """
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self._dimension = self.model.get_sentence_embedding_dimension()
            self._name = f"local:{model_name}"
            logger.info(f"Initialized LocalEmbeddings with {model_name}")
        except ImportError:
            raise ImportError(
                "sentence-transformers not installed. "
                "Install with: pip install sentence-transformers"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_name}: {e}")

    def embed(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        return self.model.encode(text, convert_to_numpy=True).tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def name(self) -> str:
        return self._name


class OpenAIEmbeddings(EmbeddingProvider):
    """OpenAI API-based embeddings."""

    def __init__(self, api_key: Optional[str] = None, model: str = "text-embedding-3-small"):
        """
        Initialize OpenAI embeddings.

        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
            model: OpenAI embedding model name
        """
        try:
            import openai
            self.api_key = api_key or os.getenv("OPENAI_API_KEY")
            if not self.api_key:
                raise ValueError("OPENAI_API_KEY not set")

            self.client = openai.OpenAI(api_key=self.api_key)
            self.model = model

            # Model dimensions
            self._dimensions = {
                "text-embedding-3-small": 1536,
                "text-embedding-3-large": 3072,
                "text-embedding-ada-002": 1536,
            }
            self._dimension = self._dimensions.get(model, 1536)
            self._name = f"openai:{model}"
            logger.info(f"Initialized OpenAIEmbeddings with {model}")

        except ImportError:
            raise ImportError(
                "openai package not installed. "
                "Install with: pip install openai"
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize OpenAI client: {e}")

    def embed(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"OpenAI API batch error: {e}")
            raise

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def name(self) -> str:
        return self._name


class TFIDFEmbeddings(EmbeddingProvider):
    """TF-IDF based embeddings (fallback, no external dependencies)."""

    def __init__(self, max_features: int = 384):
        """
        Initialize TF-IDF embeddings.

        Args:
            max_features: Maximum number of features (embedding dimension)
        """
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1
            )
            self._dimension = max_features
            self._name = "tfidf"
            self._is_fitted = False
            self._corpus = []
            logger.info(f"Initialized TFIDFEmbeddings with dimension {max_features}")
        except ImportError:
            raise ImportError(
                "scikit-learn not installed. "
                "Install with: pip install scikit-learn"
            )

    def _ensure_fitted(self, texts: List[str]):
        """Ensure vectorizer is fitted on corpus."""
        if not self._is_fitted or texts:
            # Add new texts to corpus
            self._corpus.extend(texts)
            self._corpus = list(set(self._corpus))  # Deduplicate

            if len(self._corpus) > 0:
                self.vectorizer.fit(self._corpus)
                self._is_fitted = True

    def embed(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        self._ensure_fitted([text])
        vector = self.vectorizer.transform([text]).toarray()[0]
        return vector.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        self._ensure_fitted(texts)
        vectors = self.vectorizer.transform(texts).toarray()
        return vectors.tolist()

    @property
    def dimension(self) -> int:
        return self._dimension

    @property
    def name(self) -> str:
        return self._name


class EmbeddingCache:
    """Simple disk-based cache for embeddings."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize cache.

        Args:
            cache_dir: Directory for cache files (defaults to ~/.cache/claude_memory)
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "claude_memory" / "embeddings"

        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Embedding cache at {self.cache_dir}")

    def _get_key(self, text: str, provider_name: str) -> str:
        """Generate cache key from text and provider."""
        content = f"{provider_name}:{text}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, text: str, provider_name: str) -> Optional[List[float]]:
        """Get cached embedding if exists."""
        key = self._get_key(text, provider_name)
        cache_file = self.cache_dir / f"{key}.json"

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                return data['embedding']
            except Exception as e:
                logger.warning(f"Failed to load cache {key}: {e}")
                return None
        return None

    def set(self, text: str, provider_name: str, embedding: List[float]):
        """Cache embedding."""
        key = self._get_key(text, provider_name)
        cache_file = self.cache_dir / f"{key}.json"

        try:
            with open(cache_file, 'w') as f:
                json.dump({
                    'text': text[:100],  # Store preview
                    'provider': provider_name,
                    'embedding': embedding
                }, f)
        except Exception as e:
            logger.warning(f"Failed to cache embedding {key}: {e}")

    def clear(self):
        """Clear all cached embeddings."""
        import shutil
        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Embedding cache cleared")


class EmbeddingManager:
    """
    Main embedding manager with automatic provider detection and fallback.

    Usage:
        manager = EmbeddingManager()
        embedding = manager.embed("Hello world")
        similarity = manager.similarity(embedding1, embedding2)
    """

    def __init__(
        self,
        provider: Optional[EmbeddingProvider] = None,
        cache_dir: Optional[Path] = None,
        enable_cache: bool = True
    ):
        """
        Initialize embedding manager.

        Args:
            provider: Specific provider to use (auto-detect if None)
            cache_dir: Cache directory
            enable_cache: Whether to enable caching
        """
        self.provider = provider or self._auto_detect_provider()
        self.cache = EmbeddingCache(cache_dir) if enable_cache else None

        logger.info(f"EmbeddingManager initialized with provider: {self.provider.name}")

    def _auto_detect_provider(self) -> EmbeddingProvider:
        """Auto-detect best available provider."""

        # Try Local (sentence-transformers)
        try:
            provider = LocalEmbeddings()
            logger.info("Using LocalEmbeddings (sentence-transformers)")
            return provider
        except Exception as e:
            logger.debug(f"LocalEmbeddings not available: {e}")

        # Try OpenAI
        try:
            provider = OpenAIEmbeddings()
            logger.info("Using OpenAIEmbeddings (API)")
            return provider
        except Exception as e:
            logger.debug(f"OpenAIEmbeddings not available: {e}")

        # Fallback to TF-IDF
        try:
            provider = TFIDFEmbeddings()
            logger.warning("Using TFIDFEmbeddings (fallback) - limited semantic understanding")
            return provider
        except Exception as e:
            logger.error(f"All embedding providers failed: {e}")
            raise RuntimeError(
                "No embedding provider available. Install one of:\n"
                "  - sentence-transformers (pip install sentence-transformers)\n"
                "  - openai (pip install openai and set OPENAI_API_KEY)\n"
                "  - scikit-learn (pip install scikit-learn)"
            )

    def embed(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        # Check cache
        if self.cache:
            cached = self.cache.get(text, self.provider.name)
            if cached is not None:
                logger.debug("Cache hit for embedding")
                return cached

        # Generate embedding
        embedding = self.provider.embed(text)

        # Cache result
        if self.cache:
            self.cache.set(text, self.provider.name, embedding)

        return embedding

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of input texts

        Returns:
            List of embedding vectors
        """
        # Check which are cached
        embeddings = []
        uncached_indices = []
        uncached_texts = []

        for i, text in enumerate(texts):
            if self.cache:
                cached = self.cache.get(text, self.provider.name)
                if cached is not None:
                    embeddings.append(cached)
                    continue

            uncached_indices.append(i)
            uncached_texts.append(text)
            embeddings.append(None)  # Placeholder

        # Generate embeddings for uncached
        if uncached_texts:
            new_embeddings = self.provider.embed_batch(uncached_texts)

            # Insert and cache
            for idx, text, embedding in zip(uncached_indices, uncached_texts, new_embeddings):
                embeddings[idx] = embedding
                if self.cache:
                    self.cache.set(text, self.provider.name, embedding)

        return embeddings

    @staticmethod
    def similarity(embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.

        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector

        Returns:
            Cosine similarity (0-1)
        """
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def search(
        self,
        query_embedding: List[float],
        corpus_embeddings: List[List[float]],
        top_k: int = 5
    ) -> List[Tuple[int, float]]:
        """
        Search for most similar embeddings.

        Args:
            query_embedding: Query vector
            corpus_embeddings: List of candidate vectors
            top_k: Number of results to return

        Returns:
            List of (index, similarity_score) tuples, sorted by score descending
        """
        similarities = [
            (i, self.similarity(query_embedding, emb))
            for i, emb in enumerate(corpus_embeddings)
        ]

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    @property
    def dimension(self) -> int:
        """Get embedding dimension."""
        return self.provider.dimension

    @property
    def provider_name(self) -> str:
        """Get active provider name."""
        return self.provider.name

    def clear_cache(self):
        """Clear embedding cache."""
        if self.cache:
            self.cache.clear()


# Convenience functions for quick usage
_default_manager = None


def get_default_manager() -> EmbeddingManager:
    """Get or create default embedding manager singleton."""
    global _default_manager
    if _default_manager is None:
        _default_manager = EmbeddingManager()
    return _default_manager


def embed(text: str) -> List[float]:
    """Convenience function to embed text using default manager."""
    return get_default_manager().embed(text)


def embed_batch(texts: List[str]) -> List[List[float]]:
    """Convenience function to embed multiple texts using default manager."""
    return get_default_manager().embed_batch(texts)


def similarity(embedding1: List[float], embedding2: List[float]) -> float:
    """Convenience function to compute similarity."""
    return EmbeddingManager.similarity(embedding1, embedding2)


if __name__ == "__main__":
    # Demo usage
    logging.basicConfig(level=logging.INFO)

    print("Initializing EmbeddingManager...")
    manager = EmbeddingManager()
    print(f"Active provider: {manager.provider_name}")
    print(f"Embedding dimension: {manager.dimension}\n")

    # Single embedding
    print("Testing single embedding...")
    text = "Machine learning is a subset of artificial intelligence"
    emb = manager.embed(text)
    print(f"Text: {text}")
    print(f"Embedding shape: {len(emb)}")
    print(f"First 5 values: {emb[:5]}\n")

    # Batch embedding
    print("Testing batch embedding...")
    texts = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks",
        "Natural language processing analyzes text"
    ]
    embeddings = manager.embed_batch(texts)
    print(f"Generated {len(embeddings)} embeddings\n")

    # Similarity search
    print("Testing similarity search...")
    query = "AI and neural networks"
    query_emb = manager.embed(query)
    results = manager.search(query_emb, embeddings, top_k=3)

    print(f"Query: {query}")
    print("Top matches:")
    for idx, score in results:
        print(f"  {score:.3f} - {texts[idx]}")
