"""
Embedding service for RAG.

This module provides embedding generation for vector similarity search.
"""

from typing import List, Optional

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from psyai.core.config import settings
from psyai.core.exceptions import LLMError
from psyai.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """
    Service for generating embeddings.

    Supports multiple embedding providers (OpenAI, HuggingFace).

    Example:
        >>> service = EmbeddingService()
        >>> embeddings = await service.aembed_documents(["Hello world", "Goodbye"])
        >>> query_embedding = await service.aembed_query("Hello")
    """

    def __init__(
        self,
        provider: str = "huggingface",
        model_name: Optional[str] = None,
    ):
        """
        Initialize embedding service.

        Args:
            provider: Embedding provider ("openai" or "huggingface")
            model_name: Optional model name override

        Raises:
            LLMError: If provider is invalid or initialization fails
        """
        self.provider = provider.lower()
        self.model_name = model_name

        self._embeddings = self._create_embeddings()

        logger.info(
            "embedding_service_initialized",
            provider=self.provider,
            model=self.model_name or "default",
        )

    def _create_embeddings(self) -> Embeddings:
        """
        Create embeddings instance based on provider.

        Returns:
            Embeddings instance

        Raises:
            LLMError: If provider is invalid or creation fails
        """
        try:
            if self.provider == "openai":
                return OpenAIEmbeddings(
                    model=self.model_name or "text-embedding-ada-002",
                )
            elif self.provider == "huggingface":
                return HuggingFaceEmbeddings(
                    model_name=self.model_name or settings.embedding_model,
                )
            else:
                raise ValueError(f"Invalid embedding provider: {self.provider}")

        except Exception as e:
            logger.error("embedding_creation_failed", error=str(e))
            raise LLMError(f"Failed to create embeddings: {str(e)}")

    @property
    def embeddings(self) -> Embeddings:
        """Get the underlying embeddings instance."""
        return self._embeddings

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            texts: List of document texts

        Returns:
            List of embedding vectors

        Raises:
            LLMError: If embedding generation fails

        Example:
            >>> embeddings = service.embed_documents(["doc1", "doc2"])
            >>> print(len(embeddings))  # 2
            >>> print(len(embeddings[0]))  # embedding dimension
        """
        try:
            logger.debug("embedding_documents", count=len(texts))

            embeddings = self._embeddings.embed_documents(texts)

            logger.info(
                "embeddings_generated",
                count=len(texts),
                dimension=len(embeddings[0]) if embeddings else 0,
            )

            return embeddings

        except Exception as e:
            logger.error("embedding_documents_failed", error=str(e))
            raise LLMError(f"Failed to embed documents: {str(e)}")

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents asynchronously.

        Args:
            texts: List of document texts

        Returns:
            List of embedding vectors

        Raises:
            LLMError: If embedding generation fails

        Example:
            >>> embeddings = await service.aembed_documents(["doc1", "doc2"])
        """
        try:
            logger.debug("embedding_documents_async", count=len(texts))

            embeddings = await self._embeddings.aembed_documents(texts)

            logger.info(
                "embeddings_generated_async",
                count=len(texts),
                dimension=len(embeddings[0]) if embeddings else 0,
            )

            return embeddings

        except Exception as e:
            logger.error("embedding_documents_async_failed", error=str(e))
            raise LLMError(f"Failed to embed documents: {str(e)}")

    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query.

        Args:
            text: Query text

        Returns:
            Embedding vector

        Raises:
            LLMError: If embedding generation fails

        Example:
            >>> embedding = service.embed_query("What is PsyAI?")
            >>> print(len(embedding))  # embedding dimension
        """
        try:
            logger.debug("embedding_query", text_length=len(text))

            embedding = self._embeddings.embed_query(text)

            logger.info("query_embedded", dimension=len(embedding))

            return embedding

        except Exception as e:
            logger.error("embedding_query_failed", error=str(e))
            raise LLMError(f"Failed to embed query: {str(e)}")

    async def aembed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a single query asynchronously.

        Args:
            text: Query text

        Returns:
            Embedding vector

        Raises:
            LLMError: If embedding generation fails

        Example:
            >>> embedding = await service.aembed_query("What is PsyAI?")
        """
        try:
            logger.debug("embedding_query_async", text_length=len(text))

            embedding = await self._embeddings.aembed_query(text)

            logger.info("query_embedded_async", dimension=len(embedding))

            return embedding

        except Exception as e:
            logger.error("embedding_query_async_failed", error=str(e))
            raise LLMError(f"Failed to embed query: {str(e)}")

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings.

        Returns:
            Embedding dimension

        Example:
            >>> dimension = service.get_embedding_dimension()
            >>> print(dimension)  # e.g., 384 for MiniLM, 1536 for Ada
        """
        # Generate a test embedding to get dimension
        try:
            test_embedding = self.embed_query("test")
            return len(test_embedding)
        except Exception as e:
            logger.warning("embedding_dimension_check_failed", error=str(e))
            # Return default based on provider
            if self.provider == "openai":
                return 1536  # text-embedding-ada-002
            else:
                return settings.embedding_dimension


# Singleton instance
_embedding_service: Optional[EmbeddingService] = None


def get_embedding_service(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    force_new: bool = False,
) -> EmbeddingService:
    """
    Get or create an embedding service instance.

    By default, returns a singleton instance. Set force_new=True to create a new instance.

    Args:
        provider: Embedding provider ("openai" or "huggingface")
        model_name: Optional model name override
        force_new: Force creation of new instance

    Returns:
        EmbeddingService instance

    Example:
        >>> service = get_embedding_service()
        >>> embeddings = await service.aembed_query("Hello world")
    """
    global _embedding_service

    if force_new or _embedding_service is None:
        _embedding_service = EmbeddingService(
            provider=provider or "huggingface",
            model_name=model_name,
        )

    return _embedding_service
