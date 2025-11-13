"""
LangChain and LangGraph integration for PsyAI.

This module provides LangChain clients, chains, agents, graphs, and RAG components.

Example:
    >>> from psyai.platform.langchain_integration import (
    ...     get_langchain_client,
    ...     create_chat_chain,
    ...     get_embedding_service,
    ...     VectorStoreManager,
    ... )
    >>>
    >>> # Create a simple chat chain
    >>> chain = create_chat_chain(
    ...     system_message="You are a helpful assistant",
    ...     human_message_template="Answer: {question}"
    ... )
    >>>
    >>> # Use vector store for RAG
    >>> vectorstore = VectorStoreManager()
    >>> await vectorstore.aadd_texts(["PsyAI is awesome!"])
    >>> results = await vectorstore.asimilarity_search("What is PsyAI?")
"""

# Client
from psyai.platform.langchain_integration.client import (
    LangChainClient,
    get_langchain_client,
)

# Chains
from psyai.platform.langchain_integration.chains import (
    BaseChainBuilder,
    ConversationManager,
    create_chain_with_fallback,
    create_chain_with_history,
    create_chat_chain,
    create_chat_memory,
    create_conversational_chain,
    create_map_reduce_chain,
    create_sequential_chain,
    create_simple_chain,
)

# RAG
from psyai.platform.langchain_integration.rag import (
    EmbeddingService,
    VectorStoreManager,
    get_embedding_service,
)

__all__ = [
    # Client
    "LangChainClient",
    "get_langchain_client",
    # Chains - Base
    "BaseChainBuilder",
    "create_chain_with_fallback",
    "create_chat_chain",
    "create_map_reduce_chain",
    "create_sequential_chain",
    "create_simple_chain",
    # Chains - Conversational
    "ConversationManager",
    "create_chain_with_history",
    "create_chat_memory",
    "create_conversational_chain",
    # RAG - Embeddings
    "EmbeddingService",
    "get_embedding_service",
    # RAG - Vector Stores
    "VectorStoreManager",
]
