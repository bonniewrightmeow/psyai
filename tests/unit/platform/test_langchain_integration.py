"""Tests for LangChain integration."""

from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest

from psyai.core.exceptions import LLMError


class TestLangChainClient:
    """Tests for LangChainClient."""

    @patch("psyai.platform.langchain_integration.client.ChatOpenAI")
    def test_client_initialization(self, mock_chat_openai):
        """Test client initializes correctly."""
        from psyai.platform.langchain_integration import LangChainClient

        client = LangChainClient(model_name="gpt-4", temperature=0.5)

        assert client.model_name == "gpt-4"
        assert client.temperature == 0.5
        mock_chat_openai.assert_called_once()

    @patch("psyai.platform.langchain_integration.client.ChatOpenAI")
    def test_get_langchain_client_singleton(self, mock_chat_openai):
        """Test get_langchain_client returns singleton."""
        from psyai.platform.langchain_integration import get_langchain_client

        # Clear any existing singleton
        get_langchain_client(force_new=True)

        client1 = get_langchain_client()
        client2 = get_langchain_client()

        assert client1 is client2

    @patch("psyai.platform.langchain_integration.client.ChatOpenAI")
    def test_generate_success(self, mock_chat_openai):
        """Test successful text generation."""
        from psyai.platform.langchain_integration import LangChainClient

        # Mock the LLM response
        mock_response = Mock()
        mock_response.content = "This is a test response"
        mock_llm = Mock()
        mock_llm.invoke.return_value = mock_response
        mock_chat_openai.return_value = mock_llm

        client = LangChainClient()
        response = client.generate("Test prompt")

        assert response == "This is a test response"
        mock_llm.invoke.assert_called_once()

    @patch("psyai.platform.langchain_integration.client.ChatOpenAI")
    @pytest.mark.asyncio
    async def test_agenerate_success(self, mock_chat_openai):
        """Test successful async text generation."""
        from psyai.platform.langchain_integration import LangChainClient

        # Mock the async LLM response
        mock_response = Mock()
        mock_response.content = "This is a test response"
        mock_llm = Mock()
        mock_llm.ainvoke = AsyncMock(return_value=mock_response)
        mock_chat_openai.return_value = mock_llm

        client = LangChainClient()
        response = await client.agenerate("Test prompt")

        assert response == "This is a test response"
        mock_llm.ainvoke.assert_called_once()


class TestChains:
    """Tests for chain builders."""

    @patch("psyai.platform.langchain_integration.chains.base.get_langchain_client")
    def test_create_simple_chain(self, mock_get_client):
        """Test simple chain creation."""
        from psyai.platform.langchain_integration import create_simple_chain

        mock_client = Mock()
        mock_client.llm = Mock()
        mock_get_client.return_value = mock_client

        chain = create_simple_chain("What is {topic}?")

        assert chain is not None
        mock_get_client.assert_called_once()

    @patch("psyai.platform.langchain_integration.chains.base.get_langchain_client")
    def test_create_chat_chain(self, mock_get_client):
        """Test chat chain creation."""
        from psyai.platform.langchain_integration import create_chat_chain

        mock_client = Mock()
        mock_client.llm = Mock()
        mock_get_client.return_value = mock_client

        chain = create_chat_chain(
            system_message="You are helpful",
            human_message_template="Answer: {question}",
        )

        assert chain is not None
        mock_get_client.assert_called_once()

    @patch("psyai.platform.langchain_integration.chains.base.get_langchain_client")
    def test_base_chain_builder(self, mock_get_client):
        """Test BaseChainBuilder fluent interface."""
        from psyai.platform.langchain_integration import BaseChainBuilder

        mock_client = Mock()
        mock_client.llm = Mock()
        mock_get_client.return_value = mock_client

        chain = (
            BaseChainBuilder()
            .with_system_message("You are helpful")
            .with_template("Answer: {question}")
            .with_model("gpt-4")
            .build()
        )

        assert chain is not None

    def test_base_chain_builder_requires_template(self):
        """Test that BaseChainBuilder requires template."""
        from psyai.platform.langchain_integration import BaseChainBuilder

        builder = BaseChainBuilder().with_model("gpt-4")

        with pytest.raises(ValueError, match="Template is required"):
            builder.build()


class TestConversationalChains:
    """Tests for conversational chains with memory."""

    @patch("psyai.platform.langchain_integration.chains.conversational.get_langchain_client")
    def test_create_conversational_chain(self, mock_get_client):
        """Test conversational chain creation."""
        from psyai.platform.langchain_integration import create_conversational_chain

        mock_client = Mock()
        mock_client.llm = Mock()
        mock_get_client.return_value = mock_client

        chain = create_conversational_chain(
            system_message="You are helpful",
            memory_type="buffer",
        )

        assert chain is not None
        assert hasattr(chain, "memory")

    def test_create_conversational_chain_invalid_memory_type(self):
        """Test that invalid memory type raises error."""
        from psyai.platform.langchain_integration import create_conversational_chain

        with pytest.raises(ValueError, match="Invalid memory type"):
            create_conversational_chain(memory_type="invalid")

    def test_create_chat_memory(self):
        """Test chat memory creation."""
        from psyai.platform.langchain_integration import create_chat_memory

        memory = create_chat_memory("session-123")

        assert memory is not None
        assert len(memory.messages) == 0

    @patch("psyai.platform.langchain_integration.chains.conversational.get_langchain_client")
    def test_conversation_manager(self, mock_get_client):
        """Test ConversationManager."""
        from psyai.platform.langchain_integration import ConversationManager

        mock_client = Mock()
        mock_client.llm = Mock()
        mock_get_client.return_value = mock_client

        manager = ConversationManager(session_id="test-123")

        assert manager.session_id == "test-123"
        assert hasattr(manager, "chain")

    @patch("psyai.platform.langchain_integration.chains.conversational.get_langchain_client")
    def test_conversation_manager_clear_history(self, mock_get_client):
        """Test clearing conversation history."""
        from psyai.platform.langchain_integration import ConversationManager

        mock_client = Mock()
        mock_client.llm = Mock()
        mock_get_client.return_value = mock_client

        manager = ConversationManager(session_id="test-123")
        manager.clear_history()

        # Should not raise an error
        history = manager.get_history()
        assert isinstance(history, list)


class TestEmbeddingService:
    """Tests for embedding service."""

    @patch("psyai.platform.langchain_integration.rag.embeddings.HuggingFaceEmbeddings")
    def test_embedding_service_initialization(self, mock_hf_embeddings):
        """Test embedding service initializes correctly."""
        from psyai.platform.langchain_integration.rag import EmbeddingService

        service = EmbeddingService(provider="huggingface")

        assert service.provider == "huggingface"
        mock_hf_embeddings.assert_called_once()

    @patch("psyai.platform.langchain_integration.rag.embeddings.OpenAIEmbeddings")
    def test_embedding_service_openai_provider(self, mock_openai_embeddings):
        """Test embedding service with OpenAI provider."""
        from psyai.platform.langchain_integration.rag import EmbeddingService

        service = EmbeddingService(provider="openai")

        assert service.provider == "openai"
        mock_openai_embeddings.assert_called_once()

    def test_embedding_service_invalid_provider(self):
        """Test that invalid provider raises error."""
        from psyai.core.exceptions import LLMError
        from psyai.platform.langchain_integration.rag import EmbeddingService

        with pytest.raises(LLMError):
            EmbeddingService(provider="invalid")

    @patch("psyai.platform.langchain_integration.rag.embeddings.HuggingFaceEmbeddings")
    def test_embed_query(self, mock_hf_embeddings):
        """Test embedding a single query."""
        from psyai.platform.langchain_integration.rag import EmbeddingService

        # Mock the embeddings
        mock_embeddings_instance = Mock()
        mock_embeddings_instance.embed_query.return_value = [0.1, 0.2, 0.3]
        mock_hf_embeddings.return_value = mock_embeddings_instance

        service = EmbeddingService(provider="huggingface")
        embedding = service.embed_query("test query")

        assert embedding == [0.1, 0.2, 0.3]
        mock_embeddings_instance.embed_query.assert_called_once_with("test query")

    @patch("psyai.platform.langchain_integration.rag.embeddings.HuggingFaceEmbeddings")
    def test_embed_documents(self, mock_hf_embeddings):
        """Test embedding multiple documents."""
        from psyai.platform.langchain_integration.rag import EmbeddingService

        # Mock the embeddings
        mock_embeddings_instance = Mock()
        mock_embeddings_instance.embed_documents.return_value = [
            [0.1, 0.2, 0.3],
            [0.4, 0.5, 0.6],
        ]
        mock_hf_embeddings.return_value = mock_embeddings_instance

        service = EmbeddingService(provider="huggingface")
        embeddings = service.embed_documents(["doc1", "doc2"])

        assert len(embeddings) == 2
        assert embeddings[0] == [0.1, 0.2, 0.3]
        mock_embeddings_instance.embed_documents.assert_called_once()

    @patch("psyai.platform.langchain_integration.rag.embeddings.HuggingFaceEmbeddings")
    def test_get_embedding_service_singleton(self, mock_hf_embeddings):
        """Test get_embedding_service returns singleton."""
        from psyai.platform.langchain_integration.rag import get_embedding_service

        # Clear any existing singleton
        get_embedding_service(force_new=True)

        service1 = get_embedding_service()
        service2 = get_embedding_service()

        assert service1 is service2


class TestVectorStoreManager:
    """Tests for vector store manager."""

    @patch("psyai.platform.langchain_integration.rag.vectorstore.get_embedding_service")
    @patch("psyai.platform.langchain_integration.rag.vectorstore.Chroma")
    def test_vectorstore_manager_initialization(self, mock_chroma, mock_get_embedding):
        """Test vector store manager initializes correctly."""
        from psyai.platform.langchain_integration.rag import VectorStoreManager

        mock_embedding_service = Mock()
        mock_embedding_service.embeddings = Mock()
        mock_get_embedding.return_value = mock_embedding_service

        manager = VectorStoreManager(store_type="chroma")

        assert manager.store_type == "chroma"
        mock_chroma.assert_called_once()

    @patch("psyai.platform.langchain_integration.rag.vectorstore.get_embedding_service")
    @patch("psyai.platform.langchain_integration.rag.vectorstore.Chroma")
    def test_add_texts(self, mock_chroma, mock_get_embedding):
        """Test adding texts to vector store."""
        from psyai.platform.langchain_integration.rag import VectorStoreManager

        # Mock embedding service
        mock_embedding_service = Mock()
        mock_embedding_service.embeddings = Mock()
        mock_get_embedding.return_value = mock_embedding_service

        # Mock vector store
        mock_vectorstore_instance = Mock()
        mock_vectorstore_instance.add_texts.return_value = ["id1", "id2"]
        mock_chroma.return_value = mock_vectorstore_instance

        manager = VectorStoreManager(store_type="chroma")
        ids = manager.add_texts(["text1", "text2"])

        assert ids == ["id1", "id2"]
        mock_vectorstore_instance.add_texts.assert_called_once()

    @patch("psyai.platform.langchain_integration.rag.vectorstore.get_embedding_service")
    @patch("psyai.platform.langchain_integration.rag.vectorstore.Chroma")
    def test_similarity_search(self, mock_chroma, mock_get_embedding):
        """Test similarity search."""
        from langchain_core.documents import Document

        from psyai.platform.langchain_integration.rag import VectorStoreManager

        # Mock embedding service
        mock_embedding_service = Mock()
        mock_embedding_service.embeddings = Mock()
        mock_get_embedding.return_value = mock_embedding_service

        # Mock vector store
        mock_vectorstore_instance = Mock()
        mock_docs = [
            Document(page_content="doc1"),
            Document(page_content="doc2"),
        ]
        mock_vectorstore_instance.similarity_search.return_value = mock_docs
        mock_chroma.return_value = mock_vectorstore_instance

        manager = VectorStoreManager(store_type="chroma")
        results = manager.similarity_search("query", k=2)

        assert len(results) == 2
        assert results[0].page_content == "doc1"
        mock_vectorstore_instance.similarity_search.assert_called_once()
