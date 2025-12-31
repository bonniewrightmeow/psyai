"""
Embedding service for RAG using Vertex AI.

This module provides embedding generation using Vertex AI text embeddings API.
"""

from typing import List, Optional

from vertexai.language_models import TextEmbeddingModel

from psyai.core.config import settings
from psyai.core.exceptions import LLMError
from psyai.core.logging import get_logger

logger = get_logger(__name__)


class VertexEmbeddingService:
    """
    Service for generating embeddings using Vertex AI.

    Example:
        >>> service = VertexEmbeddingService()
        >>> embeddings = await service.aembed_documents(["Hello world", "Goodbye"])
        >>> query_embedding = await service.aembed_query("Hello")
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
    ):
        """
        Initialize Vertex AI embedding service.

        Args:
            model_name: Optional model name override

        Raises:
            LLMError: If initialization fails
        """
        self.model_name = model_name or settings.vertex_embedding_model

        try:
            self._model = TextEmbeddingModel.from_pretrained(self.model_name)
        except Exception as e:
            logger.error("vertex_embedding_model_creation_failed", error=str(e))
            raise LLMError(f"Failed to create Vertex AI embedding model: {str(e)}")

        logger.info(
            "vertex_embedding_service_initialized",
            model=self.model_name,
        )

    @property
    def model(self) -> TextEmbeddingModel:
        """Get the underlying model instance."""
        return self._model

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
            logger.debug("vertex_embedding_documents", count=len(texts))

            embeddings_response = self._model.get_embeddings(texts)
            embeddings = [emb.values for emb in embeddings_response]

            logger.info(
                "vertex_embeddings_generated",
                count=len(texts),
                dimension=len(embeddings[0]) if embeddings else 0,
            )

            return embeddings

        except Exception as e:
            logger.error("vertex_embedding_documents_failed", error=str(e))
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
            logger.debug("vertex_embedding_documents_async", count=len(texts))

            embeddings_response = await self._model.get_embeddings_async(texts)
            embeddings = [emb.values for emb in embeddings_response]

            logger.info(
                "vertex_embeddings_generated_async",
                count=len(texts),
                dimension=len(embeddings[0]) if embeddings else 0,
            )

            return embeddings

        except Exception as e:
            logger.error("vertex_embedding_documents_async_failed", error=str(e))
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
            logger.debug("vertex_embedding_query", text_length=len(text))

            embeddings_response = self._model.get_embeddings([text])
            embedding = embeddings_response[0].values

            logger.info("vertex_query_embedded", dimension=len(embedding))

            return embedding

        except Exception as e:
            logger.error("vertex_embedding_query_failed", error=str(e))
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
            logger.debug("vertex_embedding_query_async", text_length=len(text))

            embeddings_response = await self._model.get_embeddings_async([text])
            embedding = embeddings_response[0].values

            logger.info("vertex_query_embedded_async", dimension=len(embedding))

            return embedding

        except Exception as e:
            logger.error("vertex_embedding_query_async_failed", error=str(e))
            raise LLMError(f"Failed to embed query: {str(e)}")

    def get_embedding_dimension(self) -> int:
        """
        Get the dimension of the embeddings.

        Returns:
            Embedding dimension

        Example:
            >>> dimension = service.get_embedding_dimension()
            >>> print(dimension)  # e.g., 768 for text-embedding-004
        """
        try:
            # Generate a test embedding to get dimension
            test_embedding = self.embed_query("test")
            return len(test_embedding)
        except Exception as e:
            logger.warning("vertex_embedding_dimension_check_failed", error=str(e))
            # Return configured dimension as fallback
            return settings.vertex_embedding_dimension


# Singleton instance
_embedding_service: Optional[VertexEmbeddingService] = None


def get_vertex_embedding_service(
    model_name: Optional[str] = None,
    force_new: bool = False,
) -> VertexEmbeddingService:
    """
    Get or create a Vertex AI embedding service instance.

    By default, returns a singleton instance. Set force_new=True to create a new instance.

    Args:
        model_name: Optional model name override
        force_new: Force creation of new instance

    Returns:
        VertexEmbeddingService instance

    Example:
        >>> service = get_vertex_embedding_service()
        >>> embeddings = await service.aembed_query("Hello world")
    """
    global _embedding_service

    if force_new or _embedding_service is None:
        _embedding_service = VertexEmbeddingService(model_name=model_name)

    return _embedding_service
