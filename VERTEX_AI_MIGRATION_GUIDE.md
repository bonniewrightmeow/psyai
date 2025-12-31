# Vertex AI Migration Guide

This guide explains how to migrate from LangChain/LangGraph to Google Vertex AI ADK and GenAI Evaluation.

## Overview

PsyAI has been migrated from LangChain/LangGraph to Google Vertex AI to leverage:

- **Vertex AI Gemini Models**: State-of-the-art LLMs with enhanced capabilities
- **Vertex AI Vector Search**: Scalable vector similarity search
- **Vertex AI GenAI Evaluation**: Comprehensive model evaluation with built-in metrics
- **Better GCP Integration**: Native integration with Google Cloud Platform services

## Prerequisites

1. **GCP Project**: You need a Google Cloud Platform project
2. **Authentication**: Set up GCP authentication
3. **APIs Enabled**: Enable the following APIs in your GCP project:
   - Vertex AI API
   - Cloud AI Platform API
   - Cloud Storage API

### Setting up Authentication

**Option 1: Service Account Key (Development)**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

**Option 2: Application Default Credentials (Recommended for Production)**
```bash
gcloud auth application-default login
```

## Configuration Changes

### Environment Variables

Update your `.env` file with the following variables:

```bash
# GCP Configuration
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GCP_CREDENTIALS_PATH=/path/to/credentials.json  # Optional

# Vertex AI Model Configuration
VERTEX_MODEL=gemini-1.5-pro
VERTEX_TEMPERATURE=0.7
VERTEX_MAX_TOKENS=2048
VERTEX_TOP_P=0.95
VERTEX_TOP_K=40

# Vertex AI Embeddings
VERTEX_EMBEDDING_MODEL=text-embedding-004
VERTEX_EMBEDDING_DIMENSION=768

# Vertex AI Vector Search (optional)
VERTEX_INDEX_ID=your-index-id
VERTEX_INDEX_ENDPOINT_ID=your-endpoint-id
VERTEX_DEPLOYED_INDEX_ID=your-deployed-index-id

# Vertex AI Evaluation
VERTEX_EVAL_ENABLED=true
```

## Code Migration

### 1. Client Migration

**Before (LangChain):**
```python
from psyai.platform.langchain_integration import get_langchain_client

client = get_langchain_client()
response = await client.agenerate("What is PsyAI?")
```

**After (Vertex AI):**
```python
from psyai.platform.vertexai_integration import get_vertexai_client

client = get_vertexai_client()
response = await client.agenerate("What is PsyAI?")
```

### 2. Chains → Agents Migration

**Before (LangChain Chains):**
```python
from psyai.platform.langchain_integration import create_chat_chain

chain = create_chat_chain(
    system_message="You are a helpful assistant",
    human_message_template="Answer: {question}"
)
response = await chain.ainvoke({"question": "What is AI?"})
```

**After (Vertex AI Agents):**
```python
from psyai.platform.vertexai_integration import SimpleAgent

agent = SimpleAgent(system_instruction="You are a helpful assistant")
response = await agent.arun("What is AI?")
print(response.content)
```

### 3. Conversational Chains → Conversational Agents

**Before (LangChain with Memory):**
```python
from psyai.platform.langchain_integration import create_conversational_chain

chain = create_conversational_chain(
    system_message="You are helpful"
)
# Chain maintains history internally
```

**After (Vertex AI Conversational Agent):**
```python
from psyai.platform.vertexai_integration import ConversationalAgent

agent = ConversationalAgent(system_instruction="You are helpful")
response1 = await agent.arun("My name is Alice")
response2 = await agent.arun("What's my name?")  # Remembers context
```

### 4. Embeddings Migration

**Before (LangChain):**
```python
from psyai.platform.langchain_integration.rag import get_embedding_service

service = get_embedding_service(provider="openai")
embeddings = await service.aembed_documents(["Hello", "World"])
```

**After (Vertex AI):**
```python
from psyai.platform.vertexai_integration import get_vertex_embedding_service

service = get_vertex_embedding_service()
embeddings = await service.aembed_documents(["Hello", "World"])
```

### 5. Vector Store Migration

**Before (LangChain with Chroma):**
```python
from psyai.platform.langchain_integration.rag import VectorStoreManager

manager = VectorStoreManager(store_type="chroma")
await manager.aadd_texts(["PsyAI is awesome!"])
results = await manager.asimilarity_search("What is PsyAI?")
```

**After (Vertex AI Vector Search):**
```python
from psyai.platform.vertexai_integration import VertexVectorStoreManager, Document

manager = VertexVectorStoreManager()
await manager.aadd_documents([
    Document(page_content="PsyAI is awesome!", metadata={"source": "doc1"})
])
results = await manager.asimilarity_search("What is PsyAI?", k=5)
```

### 6. Evaluation Migration

**Before (LangSmith):**
```python
from psyai.platform.langsmith_integration import evaluate_response

result = await evaluate_response(
    prompt="What is AI?",
    response="AI is artificial intelligence",
    reference="AI stands for artificial intelligence"
)
```

**After (Vertex AI GenAI Evaluation):**
```python
from psyai.platform.vertexai_integration import get_vertex_evaluator

evaluator = get_vertex_evaluator()
result = await evaluator.aevaluate(
    prompt="What is AI?",
    response="AI is artificial intelligence",
    reference="AI stands for artificial intelligence",
    metrics=["coherence", "fluency", "safety", "groundedness"]
)
print(result.metrics)
```

## Advanced Features

### Agent Builder Pattern

```python
from psyai.platform.vertexai_integration import AgentBuilder

agent = (
    AgentBuilder()
    .with_system_instruction("You are a helpful AI assistant")
    .with_model("gemini-1.5-pro")
    .with_conversation()  # Enables conversation memory
    .build()
)

response = await agent.arun("Hello!")
```

### Function Calling

```python
from psyai.platform.vertexai_integration import FunctionCallingAgent

def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"Weather in {location}: Sunny"

agent = FunctionCallingAgent(
    functions=[get_weather],
    system_instruction="You help with weather queries"
)

response = await agent.arun("What's the weather in NYC?")
```

### Custom Evaluation Metrics

```python
from psyai.platform.vertexai_integration import CustomMetricEvaluator

evaluator = CustomMetricEvaluator()
evaluator.add_custom_metric(
    name="helpfulness",
    criteria="Is the response helpful to the user?",
    rubric={"1": "Not helpful", "5": "Very helpful"}
)

result = await evaluator.aevaluate(
    prompt="Help me understand AI",
    response="Here's how AI works...",
    metrics=["helpfulness", "coherence"]
)
```

## Migration Checklist

- [ ] Enable Vertex AI APIs in GCP project
- [ ] Set up GCP authentication
- [ ] Update environment variables in `.env`
- [ ] Update import statements from `langchain_integration` to `vertexai_integration`
- [ ] Replace chains with agents
- [ ] Update RAG components to use Vertex AI embeddings and vector search
- [ ] Migrate evaluation code from LangSmith to Vertex AI Evaluation
- [ ] Test all migrated components
- [ ] Update tests to use new Vertex AI components
- [ ] Remove old LangChain dependencies (optional)

## Backward Compatibility

The old LangChain integration code is still available in `src/psyai/platform/langchain_integration/` for reference, but new code should use Vertex AI components.

## Common Issues

### Authentication Errors

If you see authentication errors:
```
google.auth.exceptions.DefaultCredentialsError
```

Make sure you've set up authentication properly:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
# OR
gcloud auth application-default login
```

### Quota Errors

If you hit quota limits, check your GCP quotas:
1. Go to GCP Console → IAM & Admin → Quotas
2. Search for "Vertex AI API"
3. Request quota increases if needed

### Model Not Found Errors

Ensure the model name is correct and available in your region:
- `gemini-1.5-pro` - Latest Gemini Pro model
- `gemini-1.5-flash` - Faster, lighter model
- `text-embedding-004` - Latest embedding model

## Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Vertex AI Gemini API](https://cloud.google.com/vertex-ai/docs/generative-ai/model-reference/gemini)
- [Vertex AI Evaluation](https://cloud.google.com/vertex-ai/docs/generative-ai/models/evaluate-models)
- [Vertex AI Vector Search](https://cloud.google.com/vertex-ai/docs/vector-search/overview)

## Support

For issues or questions:
1. Check the [PsyAI GitHub Issues](https://github.com/zayyanx/PsyAI/issues)
2. Review [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
3. Join the PsyAI community discussions
