"""
Chain templates and builders for LangChain.

This module provides reusable chain templates for common patterns.
"""

from psyai.platform.langchain_integration.chains.base import (
    BaseChainBuilder,
    create_chain_with_fallback,
    create_chat_chain,
    create_map_reduce_chain,
    create_sequential_chain,
    create_simple_chain,
)
from psyai.platform.langchain_integration.chains.conversational import (
    ConversationManager,
    create_chain_with_history,
    create_chat_memory,
    create_conversational_chain,
)

__all__ = [
    # Base chains
    "BaseChainBuilder",
    "create_chain_with_fallback",
    "create_chat_chain",
    "create_map_reduce_chain",
    "create_sequential_chain",
    "create_simple_chain",
    # Conversational chains
    "ConversationManager",
    "create_chain_with_history",
    "create_chat_memory",
    "create_conversational_chain",
]
