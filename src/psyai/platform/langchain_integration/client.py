"""
LangChain client wrapper and configuration.

This module provides a centralized client for interacting with LangChain
LLMs with proper error handling, retry logic, and configuration.
"""

from typing import Any, Dict, List, Optional

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from psyai.core.config import settings
from psyai.core.exceptions import LLMError, LLMRateLimitError, LLMTimeoutError
from psyai.core.logging import get_logger
from psyai.core.utils import retry_async, retry_sync

logger = get_logger(__name__)


class LangChainClient:
    """
    Wrapper for LangChain LLM client with error handling and retry logic.

    This class provides a centralized interface for interacting with LLMs
    through LangChain, with automatic retry, error handling, and logging.

    Example:
        >>> client = LangChainClient()
        >>> response = await client.agenerate("What is PsyAI?")
        >>> print(response)
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        callbacks: Optional[List[BaseCallbackHandler]] = None,
        **kwargs: Any,
    ):
        """
        Initialize LangChain client.

        Args:
            model_name: Model name (defaults to settings.openai_model)
            temperature: Model temperature (defaults to settings.openai_temperature)
            max_tokens: Max tokens (defaults to settings.openai_max_tokens)
            callbacks: Optional callback handlers
            **kwargs: Additional arguments passed to the LLM
        """
        self.model_name = model_name or settings.openai_model
        self.temperature = temperature or settings.openai_temperature
        self.max_tokens = max_tokens or settings.openai_max_tokens
        self.callbacks = callbacks or []

        # Initialize the LLM
        self._llm = self._create_llm(**kwargs)

        logger.info(
            "langchain_client_initialized",
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

    def _create_llm(self, **kwargs: Any) -> BaseChatModel:
        """
        Create the LLM instance.

        Args:
            **kwargs: Additional arguments

        Returns:
            BaseChatModel instance

        Raises:
            LLMError: If LLM creation fails
        """
        try:
            # For now, using OpenAI. This can be extended to support other providers
            llm = ChatOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                callbacks=self.callbacks,
                **kwargs,
            )
            return llm
        except Exception as e:
            logger.error("llm_creation_failed", error=str(e))
            raise LLMError(f"Failed to create LLM: {str(e)}")

    @property
    def llm(self) -> BaseChatModel:
        """Get the underlying LLM instance."""
        return self._llm

    @retry_sync(
        max_attempts=3,
        exceptions=(LLMRateLimitError, LLMTimeoutError),
        base_delay=2.0,
    )
    def generate(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response synchronously.

        Args:
            prompt: Input prompt
            stop: Stop sequences
            **kwargs: Additional arguments

        Returns:
            Generated response

        Raises:
            LLMError: If generation fails
            LLMRateLimitError: If rate limit is hit
            LLMTimeoutError: If request times out
        """
        try:
            logger.debug("llm_generate_start", prompt_length=len(prompt))

            messages = [{"role": "user", "content": prompt}]
            response = self._llm.invoke(messages, stop=stop, **kwargs)

            result = response.content

            logger.info(
                "llm_generate_complete",
                prompt_length=len(prompt),
                response_length=len(result),
            )

            return result

        except Exception as e:
            error_msg = str(e).lower()

            if "rate limit" in error_msg or "quota" in error_msg:
                logger.warning("llm_rate_limit", error=str(e))
                raise LLMRateLimitError(str(e))
            elif "timeout" in error_msg or "timed out" in error_msg:
                logger.warning("llm_timeout", error=str(e))
                raise LLMTimeoutError(str(e))
            else:
                logger.error("llm_generate_error", error=str(e))
                raise LLMError(f"LLM generation failed: {str(e)}")

    @retry_async(
        max_attempts=3,
        exceptions=(LLMRateLimitError, LLMTimeoutError),
        base_delay=2.0,
    )
    async def agenerate(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> str:
        """
        Generate a response asynchronously.

        Args:
            prompt: Input prompt
            stop: Stop sequences
            **kwargs: Additional arguments

        Returns:
            Generated response

        Raises:
            LLMError: If generation fails
            LLMRateLimitError: If rate limit is hit
            LLMTimeoutError: If request times out
        """
        try:
            logger.debug("llm_agenerate_start", prompt_length=len(prompt))

            messages = [{"role": "user", "content": prompt}]
            response = await self._llm.ainvoke(messages, stop=stop, **kwargs)

            result = response.content

            logger.info(
                "llm_agenerate_complete",
                prompt_length=len(prompt),
                response_length=len(result),
            )

            return result

        except Exception as e:
            error_msg = str(e).lower()

            if "rate limit" in error_msg or "quota" in error_msg:
                logger.warning("llm_rate_limit", error=str(e))
                raise LLMRateLimitError(str(e))
            elif "timeout" in error_msg or "timed out" in error_msg:
                logger.warning("llm_timeout", error=str(e))
                raise LLMTimeoutError(str(e))
            else:
                logger.error("llm_agenerate_error", error=str(e))
                raise LLMError(f"LLM generation failed: {str(e)}")

    def batch_generate(
        self,
        prompts: List[str],
        **kwargs: Any,
    ) -> List[str]:
        """
        Generate responses for multiple prompts in batch.

        Args:
            prompts: List of input prompts
            **kwargs: Additional arguments

        Returns:
            List of generated responses

        Raises:
            LLMError: If batch generation fails
        """
        try:
            logger.info("llm_batch_generate_start", batch_size=len(prompts))

            messages_list = [[{"role": "user", "content": p}] for p in prompts]
            responses = self._llm.batch(messages_list, **kwargs)

            results = [r.content for r in responses]

            logger.info(
                "llm_batch_generate_complete",
                batch_size=len(prompts),
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("llm_batch_generate_error", error=str(e))
            raise LLMError(f"LLM batch generation failed: {str(e)}")

    async def abatch_generate(
        self,
        prompts: List[str],
        **kwargs: Any,
    ) -> List[str]:
        """
        Generate responses for multiple prompts in batch asynchronously.

        Args:
            prompts: List of input prompts
            **kwargs: Additional arguments

        Returns:
            List of generated responses

        Raises:
            LLMError: If batch generation fails
        """
        try:
            logger.info("llm_abatch_generate_start", batch_size=len(prompts))

            messages_list = [[{"role": "user", "content": p}] for p in prompts]
            responses = await self._llm.abatch(messages_list, **kwargs)

            results = [r.content for r in responses]

            logger.info(
                "llm_abatch_generate_complete",
                batch_size=len(prompts),
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("llm_abatch_generate_error", error=str(e))
            raise LLMError(f"LLM batch generation failed: {str(e)}")

    def get_num_tokens(self, text: str) -> int:
        """
        Get the number of tokens in a text.

        Args:
            text: Input text

        Returns:
            Number of tokens

        Raises:
            LLMError: If token counting fails
        """
        try:
            return self._llm.get_num_tokens(text)
        except Exception as e:
            logger.error("token_count_error", error=str(e))
            raise LLMError(f"Token counting failed: {str(e)}")

    def with_structured_output(self, schema: Dict[str, Any]) -> BaseChatModel:
        """
        Get LLM configured for structured output.

        Args:
            schema: JSON schema for structured output

        Returns:
            LLM configured for structured output
        """
        return self._llm.with_structured_output(schema)


# Singleton instance
_client: Optional[LangChainClient] = None


def get_langchain_client(
    model_name: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    force_new: bool = False,
) -> LangChainClient:
    """
    Get or create a LangChain client instance.

    By default, returns a singleton instance. Set force_new=True to create a new instance.

    Args:
        model_name: Model name (defaults to settings.openai_model)
        temperature: Model temperature (defaults to settings.openai_temperature)
        max_tokens: Max tokens (defaults to settings.openai_max_tokens)
        force_new: Force creation of new instance

    Returns:
        LangChainClient instance

    Example:
        >>> client = get_langchain_client()
        >>> response = await client.agenerate("Hello!")
    """
    global _client

    if force_new or _client is None:
        _client = LangChainClient(
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    return _client
