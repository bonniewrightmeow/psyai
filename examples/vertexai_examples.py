"""
Example usage of Vertex AI integration in PsyAI.

This module demonstrates how to use the new Vertex AI components.
"""

import asyncio
from typing import List

from psyai.platform.vertexai_integration import (
    AgentBuilder,
    ConversationalAgent,
    CustomMetricEvaluator,
    Document,
    FunctionCallingAgent,
    SimpleAgent,
    VertexVectorStoreManager,
    get_vertex_embedding_service,
    get_vertex_evaluator,
    get_vertexai_client,
)


async def example_simple_client():
    """Example: Using the Vertex AI client directly."""
    print("\n=== Example: Simple Client ===")

    client = get_vertexai_client()

    # Generate a response
    response = await client.agenerate("What is artificial intelligence?")
    print(f"Response: {response}")

    # Count tokens
    token_count = client.count_tokens("Hello, how are you?")
    print(f"Token count: {token_count}")


async def example_simple_agent():
    """Example: Using a simple agent."""
    print("\n=== Example: Simple Agent ===")

    agent = SimpleAgent(
        system_instruction="You are a helpful AI assistant specializing in psychology."
    )

    response = await agent.arun("Explain the concept of cognitive load.")
    print(f"Agent response: {response.content}")


async def example_conversational_agent():
    """Example: Using a conversational agent with memory."""
    print("\n=== Example: Conversational Agent ===")

    agent = ConversationalAgent(
        system_instruction="You are a friendly assistant with memory."
    )

    # First message
    response1 = await agent.arun("My name is Alice and I'm working on PsyAI.")
    print(f"Response 1: {response1.content}")

    # Second message - agent remembers context
    response2 = await agent.arun("What project am I working on?")
    print(f"Response 2: {response2.content}")

    # Get conversation history
    history = agent.get_history()
    print(f"Conversation history: {len(history)} messages")


async def example_function_calling_agent():
    """Example: Using an agent with function calling."""
    print("\n=== Example: Function Calling Agent ===")

    def get_user_data(user_id: str) -> str:
        """Retrieve user data from the database."""
        # Simulated database lookup
        return f"User {user_id}: Active researcher in cognitive psychology"

    def calculate_confidence(score: float) -> str:
        """Calculate confidence level from a score."""
        if score > 0.8:
            return "High confidence"
        elif score > 0.5:
            return "Medium confidence"
        else:
            return "Low confidence"

    agent = FunctionCallingAgent(
        functions=[get_user_data, calculate_confidence],
        system_instruction="You help analyze user data and confidence scores.",
    )

    response = await agent.arun(
        "Get data for user_123 and determine if a score of 0.75 is high confidence."
    )
    print(f"Function calling response: {response.content}")


async def example_agent_builder():
    """Example: Using the AgentBuilder pattern."""
    print("\n=== Example: Agent Builder ===")

    # Build a conversational agent with custom settings
    agent = (
        AgentBuilder()
        .with_system_instruction("You are an expert in human-AI collaboration.")
        .with_model("gemini-1.5-pro")
        .with_conversation()
        .build()
    )

    response = await agent.arun("What is human-in-the-loop AI?")
    print(f"Builder agent response: {response.content}")


async def example_embeddings():
    """Example: Using Vertex AI embeddings."""
    print("\n=== Example: Embeddings ===")

    service = get_vertex_embedding_service()

    # Embed documents
    documents = [
        "PsyAI is a framework for human-AI collaboration.",
        "The Centaur model predicts human decision-making.",
        "Cognitive load affects human performance in AI systems.",
    ]

    embeddings = await service.aembed_documents(documents)
    print(f"Generated {len(embeddings)} embeddings")
    print(f"Embedding dimension: {len(embeddings[0])}")

    # Embed a query
    query_embedding = await service.aembed_query("What is PsyAI?")
    print(f"Query embedding dimension: {len(query_embedding)}")


async def example_vector_store():
    """Example: Using Vertex AI Vector Search."""
    print("\n=== Example: Vector Store ===")

    # Note: This requires Vertex AI Vector Search index to be set up
    # For demo purposes, we'll show the API usage

    manager = VertexVectorStoreManager()

    # Add documents
    documents = [
        Document(
            page_content="PsyAI enables seamless human-AI transitions.",
            metadata={"source": "overview", "section": "intro"},
        ),
        Document(
            page_content="The Centaur model achieves >80% accuracy in predicting human decisions.",
            metadata={"source": "research", "section": "results"},
        ),
        Document(
            page_content="Cognitive load reduction is a key goal of PsyAI.",
            metadata={"source": "goals", "section": "objectives"},
        ),
    ]

    try:
        # Add documents to vector store
        ids = await manager.aadd_documents(documents)
        print(f"Added {len(ids)} documents to vector store")

        # Similarity search
        results = await manager.asimilarity_search("What is PsyAI?", k=2)
        print(f"\nSearch results:")
        for i, doc in enumerate(results, 1):
            print(f"{i}. {doc.page_content}")
            print(f"   Metadata: {doc.metadata}")

    except Exception as e:
        print(f"Vector store operation: {e}")
        print("Note: Vertex AI Vector Search requires index setup in GCP")


async def example_evaluation():
    """Example: Using Vertex AI GenAI Evaluation."""
    print("\n=== Example: Evaluation ===")

    evaluator = get_vertex_evaluator()

    # Evaluate a response
    result = await evaluator.aevaluate(
        prompt="What is artificial intelligence?",
        response="Artificial intelligence (AI) is the simulation of human intelligence by machines, particularly computer systems. It includes learning, reasoning, and self-correction.",
        context="AI is a broad field of computer science focused on creating intelligent machines.",
        metrics=["coherence", "fluency", "safety", "groundedness"],
    )

    print(f"Evaluation metrics: {result.metrics}")
    print(f"Summary: {result.summary}")


async def example_custom_evaluation():
    """Example: Using custom evaluation metrics."""
    print("\n=== Example: Custom Evaluation ===")

    evaluator = CustomMetricEvaluator()

    # Add custom metrics
    evaluator.add_custom_metric(
        name="helpfulness",
        criteria="Is the response helpful and actionable for the user?",
        rubric={
            "1": "Not helpful at all",
            "3": "Somewhat helpful",
            "5": "Very helpful and actionable",
        },
    )

    evaluator.add_custom_metric(
        name="empathy",
        criteria="Does the response show understanding and empathy?",
        rubric={
            "1": "No empathy",
            "3": "Some empathy",
            "5": "Highly empathetic",
        },
    )

    # Evaluate with custom metrics
    result = await evaluator.aevaluate(
        prompt="I'm struggling with decision fatigue.",
        response="I understand that decision fatigue can be overwhelming. Here are some strategies to help: 1) Prioritize important decisions, 2) Automate routine choices, 3) Take regular breaks.",
        metrics=["helpfulness", "empathy", "coherence"],
    )

    print(f"Custom evaluation metrics: {result.metrics}")


async def example_batch_operations():
    """Example: Batch operations for efficiency."""
    print("\n=== Example: Batch Operations ===")

    client = get_vertexai_client()

    # Batch generation
    prompts = [
        "Define cognitive load",
        "What is human-in-the-loop AI?",
        "Explain the Centaur model",
    ]

    responses = await client.abatch_generate(prompts)
    print(f"Generated {len(responses)} responses:")
    for i, response in enumerate(responses, 1):
        print(f"{i}. {response[:100]}...")

    # Batch evaluation
    evaluator = get_vertex_evaluator()

    evaluations = [
        {
            "prompt": "What is AI?",
            "response": "AI is artificial intelligence.",
            "context": "AI refers to machine intelligence.",
        },
        {
            "prompt": "Define ML",
            "response": "ML is machine learning.",
            "context": "ML is a subset of AI.",
        },
    ]

    results = await evaluator.abatch_evaluate(
        evaluations,
        metrics=["coherence", "groundedness"],
    )

    print(f"\nBatch evaluation results:")
    for i, result in enumerate(results, 1):
        print(f"{i}. Metrics: {result.metrics}")


async def main():
    """Run all examples."""
    print("=" * 60)
    print("Vertex AI Integration Examples for PsyAI")
    print("=" * 60)

    try:
        await example_simple_client()
        await example_simple_agent()
        await example_conversational_agent()
        await example_function_calling_agent()
        await example_agent_builder()
        await example_embeddings()
        await example_vector_store()
        await example_evaluation()
        await example_custom_evaluation()
        await example_batch_operations()

        print("\n" + "=" * 60)
        print("All examples completed!")
        print("=" * 60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        print("\nMake sure you have:")
        print("1. Set GCP_PROJECT_ID in your .env file")
        print("2. Configured GCP authentication")
        print("3. Enabled Vertex AI APIs in your GCP project")


if __name__ == "__main__":
    asyncio.run(main())
