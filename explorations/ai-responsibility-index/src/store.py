"""
Vector Store Module

Embeds document chunks and stores them in a FAISS index for retrieval.
Uses sentence-transformers for embeddings.

The store supports:
- Building an index from a list of Chunks
- Querying with multiple search terms per indicator
- Returning top-k results with source metadata for citation
"""

import json
import logging
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from .ingest import Chunk

logger = logging.getLogger(__name__)

# Default embedding model -- good balance of quality and speed
DEFAULT_MODEL = "all-MiniLM-L6-v2"


@dataclass
class RetrievalResult:
    """A retrieved passage with its similarity score and source metadata."""
    text: str
    score: float
    source_file: str
    page: int | None
    section: str | None
    chunk_index: int


class VectorStore:
    """
    FAISS-backed vector store for document chunks.

    Usage:
        store = VectorStore()
        store.build(chunks)
        results = store.query(["board AI oversight", "AI governance"], top_k=5)
    """

    def __init__(self, model_name: str = DEFAULT_MODEL):
        if faiss is None:
            raise ImportError("faiss-cpu is required. Install with: pip install faiss-cpu")
        if SentenceTransformer is None:
            raise ImportError("sentence-transformers is required. Install with: pip install sentence-transformers")

        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks: list[Chunk] = []
        self.dimension = None

    def build(self, chunks: list[Chunk]) -> None:
        """
        Build the FAISS index from a list of document chunks.

        Args:
            chunks: List of Chunk objects from the ingest module.
        """
        if not chunks:
            raise ValueError("No chunks to index")

        self.chunks = chunks
        texts = [c.text for c in chunks]

        logger.info(f"Embedding {len(texts)} chunks...")
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        embeddings = embeddings.astype(np.float32)

        # Normalize for cosine similarity (inner product on normalized vectors = cosine sim)
        faiss.normalize_L2(embeddings)

        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(self.dimension)  # inner product = cosine sim after normalization
        self.index.add(embeddings)

        logger.info(f"Built FAISS index with {self.index.ntotal} vectors (dim={self.dimension})")

    def query(self, search_terms: list[str], top_k: int = 5) -> list[RetrievalResult]:
        """
        Query the index with one or more search terms and return deduplicated top-k results.

        Embeds each search term, queries the index, and merges results by taking
        the best score per chunk across all terms.

        Args:
            search_terms: List of search queries (from indicator metadata).
            top_k: Number of results to return.

        Returns:
            List of RetrievalResult sorted by descending score.
        """
        if self.index is None:
            raise RuntimeError("Index not built. Call build() first.")

        # Embed all search terms at once
        query_embeddings = self.model.encode(search_terms, convert_to_numpy=True).astype(np.float32)
        faiss.normalize_L2(query_embeddings)

        # Query with more results per term, then deduplicate
        per_term_k = min(top_k * 2, self.index.ntotal)
        scores, indices = self.index.search(query_embeddings, per_term_k)

        # Merge: keep best score per chunk index across all search terms
        best_scores: dict[int, float] = {}
        for term_idx in range(len(search_terms)):
            for rank in range(per_term_k):
                chunk_idx = int(indices[term_idx][rank])
                score = float(scores[term_idx][rank])
                if chunk_idx < 0:  # FAISS returns -1 for empty results
                    continue
                if chunk_idx not in best_scores or score > best_scores[chunk_idx]:
                    best_scores[chunk_idx] = score

        # Sort by score descending, take top_k
        sorted_results = sorted(best_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for chunk_idx, score in sorted_results:
            chunk = self.chunks[chunk_idx]
            results.append(RetrievalResult(
                text=chunk.text,
                score=score,
                source_file=chunk.source_file,
                page=chunk.page,
                section=chunk.section,
                chunk_index=chunk.chunk_index,
            ))

        return results

    def save(self, dirpath: str | Path) -> None:
        """Save the index and chunk metadata to disk."""
        dirpath = Path(dirpath)
        dirpath.mkdir(parents=True, exist_ok=True)

        faiss.write_index(self.index, str(dirpath / "index.faiss"))

        # Save chunk metadata (text + provenance)
        meta = []
        for c in self.chunks:
            meta.append({
                "text": c.text,
                "source_file": c.source_file,
                "page": c.page,
                "section": c.section,
                "chunk_index": c.chunk_index,
                "metadata": c.metadata,
            })
        with open(dirpath / "chunks.json", "w") as f:
            json.dump(meta, f)

    def load(self, dirpath: str | Path) -> None:
        """Load a previously saved index and chunk metadata."""
        dirpath = Path(dirpath)

        self.index = faiss.read_index(str(dirpath / "index.faiss"))
        self.dimension = self.index.d

        with open(dirpath / "chunks.json") as f:
            meta = json.load(f)

        self.chunks = []
        for m in meta:
            self.chunks.append(Chunk(
                text=m["text"],
                source_file=m["source_file"],
                page=m["page"],
                section=m["section"],
                chunk_index=m["chunk_index"],
                metadata=m.get("metadata", {}),
            ))
