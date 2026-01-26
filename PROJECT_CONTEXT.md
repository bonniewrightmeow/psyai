# PsyAI Project Context for LLM Contributors

## Project Overview

PsyAI is a research project developing the **CENTAUR Model** - a proxy agent framework that predicts human decisions in expert workflows to reduce cognitive load and decision fatigue.

### Core Hypothesis
If an LLM trained on psychology data predicts human decisions with >80% accuracy, then humans can make better decisions faster in agentic applications using a proxy agent framework.

### Research Timeline
- **Target Study Date:** Q1 2026
- **Expected Outcome:** Published research paper
- **Current Phase:** Development & Prototyping

## Research Structure (Outline 2)

### Research Question
How can AI predict human expert decisions to improve human-AI collaborative workflows?

### Key Objectives
1. Develop proxy agent framework predicting human decision-making in agentic AI applications
2. Measure effectiveness vs AI-alone, human-alone, and traditional human-AI collaboration
3. Propose framework for measuring AI-predicted decision effectiveness
4. Evaluate impact on decision speed, accuracy, and cognitive load reduction

### Expected Results
- Proxy agent framework outperforms all baseline approaches
- >60% accuracy in predicting human decisions (target >80%)
- Measurable reduction in decision fatigue and cognitive load
- Improved workflow efficiency metrics

## Technical Architecture

### Platform Layer (Sequential Dependencies)
1. **Core Infrastructure** - Config, logging, utilities
2. **Vertex AI Integration** - Gemini models, agents, workflow orchestration
3. **Vertex AI Evaluation** - GenAI evaluation service
4. **Centaur Model Integration** - Decision alignment prediction
5. **Storage Layer** - PostgreSQL, Redis, Vertex AI Vector Search
6. **API Framework** - REST and WebSocket APIs

### Feature Layer (Parallel Development)
- **Chat** - Multi-mode chat (AI, Expert, Passthrough)
- **Evals** - Vertex AI evaluations with RAG
- **HITL** - Human-in-the-loop review workflow for failed evals
- **Confidence Score** - Centaur-based decision confidence scoring

## Development Epics (From Outline 2)

### Epic 1: CENTAUR Model Integration Prototype
- **Story 1.1:** Confidence scoring API analyzing AI decisions against expert patterns
- **Story 1.2:** Real-time confidence scores (green/orange/red) for expert review prioritization
- **Story 1.3:** Comprehensive logging for research analysis

### Epic 2: Expert Review User Interface
- **Story 2.1:** Color-coded AI decisions by confidence level
- **Story 2.2:** Batch-approve high-confidence decisions
- **Story 2.3:** Detailed explanations for medium/low-confidence decisions
- **Story 2.4:** Feedback mechanism for AI decision quality

### Epic 3: Analytics and Research Dashboard
- **Story 3.1:** Real-time dashboards for decision throughput and accuracy
- **Story 3.2:** Cognitive load tracking (time spent, decision reversals, feedback)
- **Story 3.3:** Export capabilities for statistical analysis

## Key Requirements

### Confidence Classification System
- **Green (High):** >85% match probability with expert decision pattern
- **Orange (Medium):** 60-85% match probability
- **Red (Low):** <60% match probability

### Performance Targets
- API response time: <200ms for confidence scoring
- Support: 100+ concurrent expert users
- Uptime: 99.9% during research periods
- GDPR/privacy compliance for expert decision data

## Technology Stack
- **Language:** Python 3.11+
- **Framework:** FastAPI
- **AI/ML:** Vertex AI (Gemini), Centaur Foundation Model, Vertex AI Vector Search
- **Storage:** PostgreSQL, Redis, Vertex AI Vector Search
- **DevOps:** Docker, pytest, GitHub Actions, Google Cloud Platform

## Important Context for LLM Contributors

### What This Project IS
- Research-driven development with specific measurable outcomes
- Framework for human-AI decision collaboration
- Open-source contribution to HITL and LLM-as-a-judge research
- Agile development methodology with epic/story structure

### What This Project IS NOT
- A production therapy/mental health application
- A replacement for human experts
- A general-purpose chatbot
- Focused on generating therapy content

### Contributing as an LLM
When working on this codebase:
1. **Follow the research outline** - Development aligns with research objectives
2. **Maintain epic/story traceability** - Link code to specific stories from Outline 2
3. **Focus on measurability** - All features must support research data collection
4. **Prioritize research compliance** - Logging, privacy, and audit trails are critical
5. **Use scientific writing principles** - Documentation should be clear, concise, objective

## File Structure

```
psyai/
├── src/psyai/
│   ├── core/              # Core infrastructure
│   ├── platform/          # Platform layer (Vertex AI, storage, API)
│   ├── features/          # Feature layer (chat, evals, hitl, confidence)
│   └── __init__.py
├── tests/                 # Test suite
├── docs/                  # Research documentation
│   ├── research/          # Research papers and references
│   ├── epics/             # Epic and story documentation
│   └── architecture/      # Technical architecture docs
├── Collaborative Writing/ # Research paper drafts and outlines
├── examples/              # Code examples and demos
├── scripts/               # Utility scripts
└── docker/                # Docker configuration

```

## Key References

### Research Papers
1. [Centaur Foundation Model](https://arxiv.org/abs/2410.20268) - Foundation model for human cognition
2. [State of AI in Business 2025](https://mlq.ai/media/quarterly_decks/v0.1_State_of_AI_in_Business_2025_Report.pdf) - 95% AI adoption failure rate
3. [Human-AI Decision Making](https://academic.oup.com/jamia/article/26/10/1141/5519579) - Decision fatigue in expert systems
4. [LLM Limitations in Psychology](https://arxiv.org/abs/2508.06950) - Limitations in simulating human psychology
5. [Synthetic Participant Models](https://arxiv.org/abs/2508.07887) - Gaps in replicating human decision patterns

### Outline Location
- **Primary Research Outline:** `Collaborative Writing/psyAI Research Paper - Outline 2.md`
- **Project Tasks:** `Collaborative Writing/Project Tasks.md`

## Quick Commands (Claude Code)

Use these slash commands for common workflows:
- `/review-code` - Review code changes for research compliance
- `/epic [number]` - Get context for a specific epic
- `/research-context` - Display research objectives and hypotheses
- `/architecture` - Show system architecture overview

## Getting Started as an LLM Contributor

1. **Read the research outline:** `Collaborative Writing/psyAI Research Paper - Outline 2.md`
2. **Review architecture:** See README.md and this file
3. **Check current tasks:** See `Collaborative Writing/Project Tasks.md`
4. **Follow development workflow:** See GETTING_STARTED.md
5. **Understand the research goals:** Focus on measurable outcomes aligned with hypotheses

## Questions to Ask

When working on any task, consider:
1. Which epic/story does this relate to?
2. How does this support the research hypotheses?
3. What data will this collect for analysis?
4. Does this maintain research compliance (logging, privacy)?
5. How will this be measured in the study?

## License
MIT License - See LICENSE file for details
