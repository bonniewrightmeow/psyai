# Overview

This is a human-in-the-loop decision-making application built with Streamlit and LangGraph. The system implements a "Centaur" approach where AI models provide predictions and recommendations, but humans retain final decision-making authority. The application uses a state machine architecture to manage decision workflows, capturing scenarios, model predictions, confidence scores, and human approvals in a structured manner.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit for web UI and user interaction (port 5000)
- **State Management**: Streamlit's built-in session state for persisting workflow data, decision history, thread IDs, model instances, and chat parsing state across reruns
- **Component Structure**: Multi-module application with app.py (main UI) and chat_parser.py (natural language parsing service)
- **UI Tabs**: 
  - "Chat Input" for natural language decision descriptions with AI extraction
  - "New Decision" for manual structured scenario entry
  - "Review Prediction" for human-in-the-loop review and decision approval/override

## Backend Architecture
- **Workflow Engine**: LangGraph StateGraph for orchestrating decision-making workflows
- **State Machine Pattern**: TypedDict-based state structure (DecisionState) tracking scenarios, options, predictions, confidence, human decisions, approval status, and timestamps
- **Checkpointing**: MemorySaver for workflow state persistence, enabling workflow resumption and historical tracking across different threads
- **Thread Management**: Thread-based workflow instances for handling multiple concurrent decision processes
- **Workflow Caching**: @st.cache_resource decorator for get_workflow_app() ensures single workflow instance with persistent MemorySaver across all operations

## ML/AI Components

### Centaur Decision Model
- **Model Architecture**: Hugging Face Transformers pipeline for zero-shot classification
- **Current Implementation**: Facebook BART-large-MNLI model (1.63GB) as a proxy for decision prediction
- **Inference**: CPU-based inference (device=-1 configuration)
- **Model Caching**: Streamlit's @st.cache_resource decorator on load_centaur_model() to avoid reloading models on each rerun
- **Design Pattern**: The application is designed to support swapping in a custom "Centaur" model when available

### Chat Parser (Natural Language Extraction)
- **Provider**: OpenAI via Replit AI Integrations (no API key required, charges billed to credits)
- **Model**: gpt-5-mini for fast, cost-effective parsing
- **Function**: Extracts structured decision prompts (scenario + options) from natural language chat input
- **Output Format**: JSON with response_format for reliable structured extraction
- **Error Handling**: Returns None on parsing failures with user-friendly error messages

## Data Structure
- **Decision State Schema**:
  - scenario: Text description of the decision context
  - options: List of available choices (2-4 options)
  - model_prediction: AI-recommended option
  - confidence: Confidence score for prediction (0-1)
  - human_decision: Final human choice
  - human_approved: Boolean approval flag
  - timestamp: Decision timestamp (ISO format)
  - status: Current workflow status (initialized → scenario_collected → prediction_made → awaiting_human_review → completed)

**Rationale**: TypedDict provides type safety while maintaining flexibility for state machine transitions. The schema balances AI assistance with human oversight.

## Key Architectural Decisions

### Human-in-the-Loop Design
**Problem**: Need to balance AI automation with human judgment for critical decisions
**Solution**: Centaur architecture where AI provides recommendations but humans make final decisions
**Rationale**: Ensures accountability and allows humans to override AI when context or nuance requires human judgment. LangGraph interrupt_after feature pauses workflow after prediction for human review.

### State Machine Workflow  
**Problem**: Complex decision workflows with multiple steps and potential branches
**Solution**: LangGraph StateGraph with typed state management and interrupt points
**Rationale**: Provides clear workflow definition, state transitions, and debugging capabilities. Memory checkpointing enables workflow resumption and audit trails. The workflow uses interrupt_after=["human_review"] to pause execution after the human_review node sets status to "awaiting_human_review".

### Workflow Instance Persistence
**Problem**: Each button click in Streamlit rebuilds the graph, losing checkpoint context
**Solution**: get_workflow_app() function that caches the compiled workflow in st.session_state.workflow_app
**Rationale**: Ensures the same LangGraph instance with the same MemorySaver handles both initial execution and resume operations. Human inputs are persisted via update_state() before calling stream(None, config) to continue the workflow.

### Zero-Shot Classification Approach
**Problem**: Need flexible decision-making across varied scenarios without extensive training data
**Solution**: Zero-shot classification model (BART-large-MNLI) that can handle arbitrary decision options
**Rationale**: Allows the system to work with new decision scenarios without retraining, though may be replaced with domain-specific models as they become available. The model takes a scenario and candidate labels (options) and returns predictions with confidence scores.

## Workflow Execution Flow

### Manual Entry Flow (New Decision Tab)
1. User manually enters scenario with 2-4 decision options
2. Workflow executes: collect_scenario → model_prediction → human_review (interrupt)
3. Status changes through states and stops at "awaiting_human_review"
4. UI displays prediction with confidence score in Review Prediction tab
5. Human approves (uses AI decision) or overrides (selects different option)
6. update_state() persists human choice into checkpoint
7. Workflow resumes: finalize_decision → END
8. Completed decision added to decision_history in session state

### Chat-to-Centaur Flow (Chat Input Tab)
1. User describes decision in natural language
2. Chat parser (OpenAI gpt-5-mini) extracts scenario and 2-4 options via JSON response format
3. Extracted data displayed in editable form for user review/refinement
4. User submits edited or approved extraction to Centaur workflow
5. Follows same workflow as manual entry: collect_scenario → model_prediction → human_review
6. Continues to Review Prediction tab for human approval/override
7. Decision recorded in history

**Design Rationale**: Chat-to-Centaur service provides connective tissue between end-user natural language input and structured decision prompts, making the system more accessible while maintaining human oversight through the review/edit step.

# External Dependencies

## Third-Party Libraries
- **Streamlit**: Web application framework for building interactive data apps
- **LangGraph**: Workflow orchestration and state management library with checkpoint support
- **LangChain/LangChain-Core**: Supporting libraries for LangGraph functionality
- **Transformers (Hugging Face)**: ML model inference pipeline for Centaur decision predictions
- **PyTorch**: ML backend for model inference (CPU-only version)
- **OpenAI SDK**: Client library for OpenAI API (via Replit AI Integrations)
- **Pandas**: Data handling for decision history
- **Python typing**: For type hints and TypedDict state definitions

## ML Models
- **facebook/bart-large-mnli**: Zero-shot classification model from Hugging Face Model Hub (1.63GB)
  - Purpose: Proxy model for decision prediction using zero-shot classification
  - Deployment: Downloaded on first run from Hugging Face Hub and cached locally
  - Inference: CPU-based (device=-1 parameter)
  - First load time: ~20-30 seconds to download and initialize

## Package Management
- Uses uv for Python package management
- Python version constrained to >=3.11,<3.12 to ensure dependency compatibility
- Special pytorch-cpu index configuration for CPU-only PyTorch installation
- **Important**: Only torch, torchaudio, and torchvision are configured in [tool.uv.sources] to use the pytorch-cpu index. Other packages (including transformers and its dependencies) are resolved from PyPI. This prevents dependency resolution failures that occur when packages that don't exist on the pytorch-cpu index are incorrectly mapped to it.

## Recent Changes (November 2025)

### Chat-to-Centaur Service
Added natural language input capability to make the decision system more accessible:
- **chat_parser.py**: New module for parsing natural language into structured decision prompts
- **OpenAI Integration**: Uses Replit AI Integrations (gpt-5-mini) for extraction without requiring API keys
- **Chat Input Tab**: New UI tab allowing users to describe decisions conversationally
- **Editable Extraction**: Users can review and refine AI-extracted scenario/options before submission
- **Unified Workflow**: Chat inputs flow through the same LangGraph workflow as manual entries

### Deployment Configuration
Fixed pyproject.toml dependency resolution:
- Removed 1100+ incorrect package mappings from [tool.uv.sources]
- Retained only torch, torchaudio, and torchvision for pytorch-cpu index
- Allows transformers and other packages to resolve correctly from PyPI

## Future Integration Points
- Custom Centaur model (currently using BART as placeholder)
- Persistent database for decision history storage (currently in-memory session state)
- External APIs for scenario data ingestion (not currently implemented)
- User authentication and multi-user support
- Analytics and model performance tracking
- Conversational refinement loop for ambiguous chat inputs
- Logging/telemetry for chat parser performance and failure analysis
