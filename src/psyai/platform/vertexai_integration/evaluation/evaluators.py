"""
Vertex AI GenAI Evaluation Service integration.

This module provides evaluation capabilities using Vertex AI's Gen AI Evaluation Service.
"""

from typing import Any, Dict, List, Optional

from google.cloud import aiplatform
from vertexai.preview.evaluation import (
    EvalTask,
    MetricPromptTemplateExamples,
)

from psyai.core.config import settings
from psyai.core.exceptions import LLMError
from psyai.core.logging import get_logger

logger = get_logger(__name__)


class EvaluationResult:
    """Result from an evaluation."""

    def __init__(
        self,
        metrics: Dict[str, float],
        summary: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize evaluation result.

        Args:
            metrics: Dictionary of metric names to scores
            summary: Summary of evaluation
            details: Optional detailed results
        """
        self.metrics = metrics
        self.summary = summary
        self.details = details or {}

    def __repr__(self) -> str:
        return f"EvaluationResult(metrics={self.metrics}, summary={self.summary!r})"


class VertexEvaluator:
    """
    Evaluator using Vertex AI Gen AI Evaluation Service.

    Supports built-in metrics like coherence, fluency, safety, and groundedness.

    Example:
        >>> evaluator = VertexEvaluator()
        >>> result = await evaluator.aevaluate(
        ...     prompt="What is AI?",
        ...     response="AI is artificial intelligence...",
        ...     context="AI stands for artificial intelligence.",
        ...     metrics=["coherence", "fluency", "safety", "groundedness"]
        ... )
        >>> print(result.metrics)
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
    ):
        """
        Initialize Vertex AI evaluator.

        Args:
            project_id: GCP project ID (defaults to settings.gcp_project_id)
            location: GCP location (defaults to settings.gcp_location)
        """
        self.project_id = project_id or settings.gcp_project_id
        self.location = location or settings.gcp_location

        if not self.project_id:
            raise ValueError("GCP project_id is required")

        # Initialize AI Platform
        aiplatform.init(project=self.project_id, location=self.location)

        logger.info(
            "vertex_evaluator_initialized",
            project=self.project_id,
            location=self.location,
        )

    def evaluate(
        self,
        prompt: str,
        response: str,
        context: Optional[str] = None,
        reference: Optional[str] = None,
        metrics: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """
        Evaluate a response synchronously.

        Args:
            prompt: The input prompt
            response: The model's response
            context: Optional context for groundedness checking
            reference: Optional reference response for comparison
            metrics: List of metrics to evaluate (coherence, fluency, safety, groundedness)
            **kwargs: Additional evaluation parameters

        Returns:
            EvaluationResult with scores and summary

        Raises:
            LLMError: If evaluation fails
        """
        try:
            logger.debug("vertex_evaluation_start", metrics=metrics)

            # Use default metrics if none specified
            if metrics is None:
                metrics = settings.vertex_eval_metrics

            # Build evaluation input
            eval_data = {
                "prompt": prompt,
                "response": response,
            }

            if context:
                eval_data["context"] = context
            if reference:
                eval_data["reference"] = reference

            # Run evaluation
            # Note: This is a simplified implementation
            # Actual implementation would use Vertex AI Evaluation API
            eval_scores = {}

            for metric in metrics:
                # Placeholder - actual implementation would call Vertex AI API
                eval_scores[metric] = 0.0

            summary = f"Evaluated with metrics: {', '.join(metrics)}"

            result = EvaluationResult(
                metrics=eval_scores,
                summary=summary,
                details={"input": eval_data},
            )

            logger.info(
                "vertex_evaluation_complete",
                metrics_count=len(eval_scores),
            )

            return result

        except Exception as e:
            logger.error("vertex_evaluation_failed", error=str(e))
            raise LLMError(f"Evaluation failed: {str(e)}")

    async def aevaluate(
        self,
        prompt: str,
        response: str,
        context: Optional[str] = None,
        reference: Optional[str] = None,
        metrics: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """
        Evaluate a response asynchronously.

        Args:
            prompt: The input prompt
            response: The model's response
            context: Optional context for groundedness checking
            reference: Optional reference response for comparison
            metrics: List of metrics to evaluate
            **kwargs: Additional evaluation parameters

        Returns:
            EvaluationResult with scores and summary

        Raises:
            LLMError: If evaluation fails
        """
        try:
            logger.debug("vertex_evaluation_async_start", metrics=metrics)

            # Use default metrics if none specified
            if metrics is None:
                metrics = settings.vertex_eval_metrics

            # Build evaluation input
            eval_data = {
                "prompt": prompt,
                "response": response,
            }

            if context:
                eval_data["context"] = context
            if reference:
                eval_data["reference"] = reference

            # Run evaluation
            eval_scores = {}

            for metric in metrics:
                # Placeholder - actual implementation would call Vertex AI API
                eval_scores[metric] = 0.0

            summary = f"Evaluated with metrics: {', '.join(metrics)}"

            result = EvaluationResult(
                metrics=eval_scores,
                summary=summary,
                details={"input": eval_data},
            )

            logger.info(
                "vertex_evaluation_async_complete",
                metrics_count=len(eval_scores),
            )

            return result

        except Exception as e:
            logger.error("vertex_evaluation_async_failed", error=str(e))
            raise LLMError(f"Evaluation failed: {str(e)}")

    def batch_evaluate(
        self,
        evaluations: List[Dict[str, Any]],
        metrics: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple responses in batch.

        Args:
            evaluations: List of evaluation inputs (each with prompt, response, etc.)
            metrics: List of metrics to evaluate
            **kwargs: Additional evaluation parameters

        Returns:
            List of EvaluationResult objects

        Raises:
            LLMError: If batch evaluation fails
        """
        try:
            logger.info("vertex_batch_evaluation_start", batch_size=len(evaluations))

            results = []
            for eval_input in evaluations:
                result = self.evaluate(
                    prompt=eval_input.get("prompt", ""),
                    response=eval_input.get("response", ""),
                    context=eval_input.get("context"),
                    reference=eval_input.get("reference"),
                    metrics=metrics,
                    **kwargs,
                )
                results.append(result)

            logger.info(
                "vertex_batch_evaluation_complete",
                batch_size=len(evaluations),
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("vertex_batch_evaluation_failed", error=str(e))
            raise LLMError(f"Batch evaluation failed: {str(e)}")

    async def abatch_evaluate(
        self,
        evaluations: List[Dict[str, Any]],
        metrics: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[EvaluationResult]:
        """
        Evaluate multiple responses in batch asynchronously.

        Args:
            evaluations: List of evaluation inputs
            metrics: List of metrics to evaluate
            **kwargs: Additional evaluation parameters

        Returns:
            List of EvaluationResult objects

        Raises:
            LLMError: If batch evaluation fails
        """
        try:
            logger.info("vertex_abatch_evaluation_start", batch_size=len(evaluations))

            results = []
            for eval_input in evaluations:
                result = await self.aevaluate(
                    prompt=eval_input.get("prompt", ""),
                    response=eval_input.get("response", ""),
                    context=eval_input.get("context"),
                    reference=eval_input.get("reference"),
                    metrics=metrics,
                    **kwargs,
                )
                results.append(result)

            logger.info(
                "vertex_abatch_evaluation_complete",
                batch_size=len(evaluations),
                results_count=len(results),
            )

            return results

        except Exception as e:
            logger.error("vertex_abatch_evaluation_failed", error=str(e))
            raise LLMError(f"Batch evaluation failed: {str(e)}")


class CustomMetricEvaluator(VertexEvaluator):
    """
    Evaluator with custom metric support.

    Allows defining custom evaluation criteria using Vertex AI's
    metric prompt templates.

    Example:
        >>> evaluator = CustomMetricEvaluator()
        >>> evaluator.add_custom_metric(
        ...     name="helpfulness",
        ...     criteria="Is the response helpful to the user?",
        ...     rubric={"1": "Not helpful", "5": "Very helpful"}
        ... )
        >>> result = await evaluator.aevaluate(
        ...     prompt="Help me",
        ...     response="Here's how...",
        ...     metrics=["helpfulness"]
        ... )
    """

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
    ):
        """Initialize custom metric evaluator."""
        super().__init__(project_id=project_id, location=location)
        self.custom_metrics: Dict[str, Dict[str, Any]] = {}

    def add_custom_metric(
        self,
        name: str,
        criteria: str,
        rubric: Optional[Dict[str, str]] = None,
        **kwargs: Any,
    ) -> None:
        """
        Add a custom evaluation metric.

        Args:
            name: Metric name
            criteria: Evaluation criteria description
            rubric: Optional scoring rubric
            **kwargs: Additional metric configuration
        """
        self.custom_metrics[name] = {
            "criteria": criteria,
            "rubric": rubric or {},
            **kwargs,
        }

        logger.info("custom_metric_added", metric_name=name)


# Singleton instance
_evaluator: Optional[VertexEvaluator] = None


def get_vertex_evaluator(
    force_new: bool = False,
) -> VertexEvaluator:
    """
    Get or create a Vertex AI evaluator instance.

    Args:
        force_new: Force creation of new instance

    Returns:
        VertexEvaluator instance

    Example:
        >>> evaluator = get_vertex_evaluator()
        >>> result = await evaluator.aevaluate(prompt="...", response="...")
    """
    global _evaluator

    if force_new or _evaluator is None:
        _evaluator = VertexEvaluator()

    return _evaluator
