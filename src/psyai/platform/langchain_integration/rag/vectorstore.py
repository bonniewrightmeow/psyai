"""
Vector store abstraction for RAG.

This module provides a unified interface for vector stores (Chroma, Pinecone, Weaviate).
"""

from typing import Any, Dict, List, Optional, Tuple

from langchain_community.vectorstores import Chroma, Weaviate
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore

from psyai.core.config import settings
from psyai.core.exceptions import VectorStoreError
from psyai.core.logging import get_logger
from psyai.platform.langchain_integration.rag.embeddings import get_embedding_service

logger = get_logger(__name__)


class VectorStoreManager:
    """
    Manager for vector store operations.

    Provides a unified interface for different vector store backends.

    Example:
        >>> manager = VectorStoreManager()
        >>> await manager.add_documents([
        ...     Document(page_content="PsyAI is awesome", metadata={"source": "doc1"})
        ... ])
        >>> results = await manager.similarity_search("What is PsyAI?", k=5)
    """

    def __init__(
        self,
        store_type: Optional[str] = None,
        collection_name: str = "psyai",
        embedding_service: Optional[Any] = None,
    ):
        """
        Initialize vector store manager.

        Args:
            store_type: Type of vector store ("chroma", "pinecone", "weaviate")
            collection_name: Name of the collection/index
            embedding_service: Optional embedding service (creates default if None)

        Raises:
            VectorStoreError: If initialization fails
        """
        self.store_type = (store_type or settings.vector_db_type).lower()
        self.collection_name = collection_name

        # Get embedding service
        if embedding_service is None:
            embedding_service = get_embedding_service()

        self.embedding_service = embedding_service

        # Create vector store
        self._vectorstore = self._create_vectorstore()

        logger.info(
            "vectorstore_manager_initialized",
            store_type=self.store_type,
            collection=collection_name,
        )

    def _create_vectorstore(self) -> VectorStore:
        """
        Create vector store instance.

        Returns:
            VectorStore instance

        Raises:
            VectorStoreError: If creation fails
        """
        try:
            embeddings = self.embedding_service.embeddings

            if self.store_type == "chroma":
                return Chroma(
                    collection_name=self.collection_name,
                    embedding_function=embeddings,
                    persist_directory=settings.chroma_persist_directory,
                )

            elif self.store_type == "weaviate":
                return Weaviate(
                    embedding=embeddings,
                    index_name=self.collection_name,
                    text_key="text",
                    by_text=False,
                )

            elif self.store_type == "pinecone":
                # Note: Pinecone requires additional setup
                # This is a placeholder - actual implementation needs pinecone-client
                raise VectorStoreError(
                    "Pinecone support requires pinecone-client package. "
                    "Install with: pip install pinecone-client"
                )

            else:
                raise ValueError(f"Invalid vector store type: {self.store_type}")

        except Exception as e:
            logger.error("vectorstore_creation_failed", error=str(e))
            raise VectorStoreError(f"Failed to create vector store: {str(e)}")

    @property
    def vectorstore(self) -> VectorStore:
        """Get the underlying vector store instance."""
        return self._vectorstore

    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add texts to the vector store.

        Args:
            texts: List of texts to add
            metadatas: Optional list of metadata dicts
            ids: Optional list of IDs

        Returns:
            List of IDs for added documents

        Raises:
            VectorStoreError: If adding texts fails

        Example:
            >>> ids = manager.add_texts(
            ...     texts=["Hello world", "Goodbye world"],
            ...     metadatas=[{"source": "doc1"}, {"source": "doc2"}]
            ... )
        """
        try:
            logger.debug("vectorstore_adding_texts", count=len(texts))

            ids = self._vectorstore.add_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids,
            )

            logger.info("vectorstore_texts_added", count=len(texts))

            return ids

        except Exception as e:
            logger.error("vectorstore_add_texts_failed", error=str(e))
            raise VectorStoreError(f"Failed to add texts: {str(e)}")

    async def aadd_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add texts to the vector store asynchronously.

        Args:
            texts: List of texts to add
            metadatas: Optional list of metadata dicts
            ids: Optional list of IDs

        Returns:
            List of IDs for added documents

        Raises:
            VectorStoreError: If adding texts fails
        """
        try:
            logger.debug("vectorstore_adding_texts_async", count=len(texts))

            ids = await self._vectorstore.aadd_texts(
                texts=texts,
                metadatas=metadatas,
                ids=ids,
            )

            logger.info("vectorstore_texts_added_async", count=len(texts))

            return ids

        except Exception as e:
            logger.error("vectorstore_add_texts_async_failed", error=str(e))
            raise VectorStoreError(f"Failed to add texts: {str(e)}")

    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add documents to the vector store.

        Args:
            documents: List of Document objects
            ids: Optional list of IDs

        Returns:
            List of IDs for added documents

        Raises:
            VectorStoreError: If adding documents fails

        Example:
            >>> docs = [
            ...     Document(page_content="Hello", metadata={"source": "doc1"}),
            ...     Document(page_content="World", metadata={"source": "doc2"}),
            ... ]
            >>> ids = manager.add_documents(docs)
        """
        try:
            logger.debug("vectorstore_adding_documents", count=len(documents))

            ids = self._vectorstore.add_documents(documents=documents, ids=ids)

            logger.info("vectorstore_documents_added", count=len(documents))

            return ids

        except Exception as e:
            logger.error("vectorstore_add_documents_failed", error=str(e))
            raise VectorStoreError(f"Failed to add documents: {str(e)}")

    async def aadd_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add documents to the vector store asynchronously.

        Args:
            documents: List of Document objects
            ids: Optional list of IDs

        Returns:
            List of IDs for added documents

        Raises:
            VectorStoreError: If adding documents fails
        """
        try:
            logger.debug("vectorstore_adding_documents_async", count=len(documents))

            ids = await self._vectorstore.aadd_documents(documents=documents, ids=ids)

            logger.info("vectorstore_documents_added_async", count=len(documents))

            return ids

        except Exception as e:
            logger.error("vectorstore_add_documents_async_failed", error=str(e))
            raise VectorStoreError(f"Failed to add documents: {str(e)}")

    def similarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Search for similar documents.

        Args:
            query: Query text
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of similar documents

        Raises:
            VectorStoreError: If search fails

        Example:
            >>> results = manager.similarity_search("What is PsyAI?", k=5)
            >>> for doc in results:
            ...     print(doc.page_content)
        """
        try:
            logger.debug("vectorstore_similarity_search", query_length=len(query), k=k)

            results = self._vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter,
            )

            logger.info(
                "vectorstore_search_complete",
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("vectorstore_search_failed", error=str(e))
            raise VectorStoreError(f"Similarity search failed: {str(e)}")

    async def asimilarity_search(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Search for similar documents asynchronously.

        Args:
            query: Query text
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of similar documents

        Raises:
            VectorStoreError: If search fails
        """
        try:
            logger.debug("vectorstore_similarity_search_async", query_length=len(query), k=k)

            results = await self._vectorstore.asimilarity_search(
                query=query,
                k=k,
                filter=filter,
            )

            logger.info(
                "vectorstore_search_complete_async",
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("vectorstore_search_async_failed", error=str(e))
            raise VectorStoreError(f"Similarity search failed: {str(e)}")

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 4,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[Document, float]]:
        """
        Search for similar documents with similarity scores.

        Args:
            query: Query text
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of (document, score) tuples

        Example:
            >>> results = manager.similarity_search_with_score("What is PsyAI?", k=5)
            >>> for doc, score in results:
            ...     print(f"Score: {score:.3f} - {doc.page_content}")
        """
        try:
            logger.debug("vectorstore_search_with_score", query_length=len(query), k=k)

            results = self._vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter,
            )

            logger.info(
                "vectorstore_search_with_score_complete",
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("vectorstore_search_with_score_failed", error=str(e))
            raise VectorStoreError(f"Similarity search with score failed: {str(e)}")

    def delete(self, ids: List[str]) -> None:
        """
        Delete documents by IDs.

        Args:
            ids: List of document IDs to delete

        Raises:
            VectorStoreError: If deletion fails

        Example:
            >>> manager.delete(["id1", "id2", "id3"])
        """
        try:
            logger.debug("vectorstore_deleting", count=len(ids))

            self._vectorstore.delete(ids=ids)

            logger.info("vectorstore_deleted", count=len(ids))

        except Exception as e:
            logger.error("vectorstore_delete_failed", error=str(e))
            raise VectorStoreError(f"Delete failed: {str(e)}")

    def as_retriever(self, **kwargs: Any) -> Any:
        """
        Get the vector store as a retriever.

        Args:
            **kwargs: Arguments passed to as_retriever

        Returns:
            Retriever instance

        Example:
            >>> retriever = manager.as_retriever(search_kwargs={"k": 5})
            >>> results = retriever.get_relevant_documents("What is PsyAI?")
        """
        return self._vectorstore.as_retriever(**kwargs)
