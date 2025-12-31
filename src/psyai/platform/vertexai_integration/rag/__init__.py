"""
RAG components using Vertex AI.

This module provides embeddings and vector search functionality.
"""

from psyai.platform.vertexai_integration.rag.embeddings import (
    VertexEmbeddingService,
    get_vertex_embedding_service,
)
from psyai.platform.vertexai_integration.rag.vectorstore import (
    Document,
    VertexVectorStoreManager,
)

__all__ = [
    "Document",
    "VertexEmbeddingService",
    "VertexVectorStoreManager",
    "get_vertex_embedding_service",
]
