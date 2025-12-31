"""
Vertex AI integration for PsyAI.

This module provides Vertex AI clients, agents, RAG components, and evaluation tools
as a replacement for LangChain/LangGraph integration.

Example:
    >>> from psyai.platform.vertexai_integration import (
    ...     get_vertexai_client,
    ...     SimpleAgent,
    ...     get_vertex_embedding_service,
    ...     VertexVectorStoreManager,
    ...     get_vertex_evaluator,
    ... )
    >>>
    >>> # Create a simple agent
    >>> agent = SimpleAgent(system_instruction="You are a helpful assistant")
    >>> response = await agent.arun("What is PsyAI?")
    >>>
    >>> # Use vector store for RAG
    >>> vectorstore = VertexVectorStoreManager()
    >>> await vectorstore.aadd_texts(["PsyAI is awesome!"])
    >>> results = await vectorstore.asimilarity_search("What is PsyAI?")
    >>>
    >>> # Evaluate responses
    >>> evaluator = get_vertex_evaluator()
    >>> result = await evaluator.aevaluate(
    ...     prompt="What is AI?",
    ...     response="AI is artificial intelligence",
    ...     metrics=["coherence", "fluency"]
    ... )
"""

# Client
from psyai.platform.vertexai_integration.client import (
    VertexAIClient,
    get_vertexai_client,
)

# Agents
from psyai.platform.vertexai_integration.agents import (
    AgentBuilder,
    AgentResponse,
    ConversationalAgent,
    FunctionCallingAgent,
    SimpleAgent,
)

# RAG
from psyai.platform.vertexai_integration.rag import (
    Document,
    VertexEmbeddingService,
    VertexVectorStoreManager,
    get_vertex_embedding_service,
)

# Evaluation
from psyai.platform.vertexai_integration.evaluation import (
    CustomMetricEvaluator,
    EvaluationResult,
    VertexEvaluator,
    get_vertex_evaluator,
)

__all__ = [
    # Client
    "VertexAIClient",
    "get_vertexai_client",
    # Agents
    "AgentBuilder",
    "AgentResponse",
    "ConversationalAgent",
    "FunctionCallingAgent",
    "SimpleAgent",
    # RAG - Embeddings
    "VertexEmbeddingService",
    "get_vertex_embedding_service",
    # RAG - Vector Stores
    "Document",
    "VertexVectorStoreManager",
    # Evaluation
    "CustomMetricEvaluator",
    "EvaluationResult",
    "VertexEvaluator",
    "get_vertex_evaluator",
]
