"""
Platform layer for PsyAI.

This module provides platform services that features depend on.
"""

# Vertex AI integration (primary)
from psyai.platform.vertexai_integration import (
    AgentBuilder,
    AgentResponse,
    ConversationalAgent,
    CustomMetricEvaluator,
    Document,
    EvaluationResult,
    FunctionCallingAgent,
    SimpleAgent,
    VertexAIClient,
    VertexEmbeddingService,
    VertexEvaluator,
    VertexVectorStoreManager,
    get_vertex_embedding_service,
    get_vertex_evaluator,
    get_vertexai_client,
)

__all__ = [
    # Vertex AI - Client
    "VertexAIClient",
    "get_vertexai_client",
    # Vertex AI - Agents
    "AgentBuilder",
    "AgentResponse",
    "ConversationalAgent",
    "FunctionCallingAgent",
    "SimpleAgent",
    # Vertex AI - RAG
    "Document",
    "VertexEmbeddingService",
    "VertexVectorStoreManager",
    "get_vertex_embedding_service",
    # Vertex AI - Evaluation
    "CustomMetricEvaluator",
    "EvaluationResult",
    "VertexEvaluator",
    "get_vertex_evaluator",
]
