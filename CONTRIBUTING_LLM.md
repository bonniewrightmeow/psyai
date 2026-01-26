# Contributing to PsyAI as an LLM Assistant

This guide helps LLM assistants (like Claude Code, GitHub Copilot, Cursor, etc.) effectively contribute to the PsyAI research project.

## Quick Start for LLMs

1. **Read PROJECT_CONTEXT.md first** - This is your primary reference
2. **Understand the research outline** - `Collaborative Writing/psyAI Research Paper - Outline 2.md`
3. **Check current epic/story** - All work should map to Epic 1, 2, or 3
4. **Review relevant epic documentation** - `docs/epics/EPIC_[1|2|3]_*.md`
5. **Code with research in mind** - Every feature supports specific hypotheses

## This is a Research Project

Unlike typical software projects, PsyAI has specific research objectives:

### Primary Hypothesis
If an LLM trained on psychology data predicts human decisions with >80% accuracy, then humans can make better decisions faster in agentic applications using a proxy agent framework.

### Your Code Must Support
1. **Data collection** - Comprehensive logging for research analysis
2. **Measurable outcomes** - Decision speed, accuracy, cognitive load reduction
3. **Research compliance** - Privacy, consent, audit trails
4. **Statistical analysis** - Exportable data in standard formats

## Development Workflow

### 1. Identify the Epic/Story

Every task should relate to a specific user story:

- **Epic 1:** CENTAUR Model Integration (Backend confidence scoring)
- **Epic 2:** Expert Review UI (Frontend review interface)
- **Epic 3:** Analytics Dashboard (Research metrics and export)

Ask yourself: "Which story from the outline does this implement?"

### 2. Research-First Development

Before writing code, consider:

```
┌─────────────────────────────────────────────────┐
│ What hypothesis does this validate?              │
│ What metrics will this collect?                  │
│ How will researchers analyze this data?          │
│ What privacy implications exist?                 │
└─────────────────────────────────────────────────┘
```

### 3. Code with Logging in Mind

**ALWAYS include:**
- Decision logging (what was decided, by whom, when)
- Timing data (how long decisions took)
- Confidence scores and classifications
- User actions and overrides
- Metadata for research analysis

**Example:**
```python
@log_decision(epic=1, story=1.2)
async def score_confidence(decision: Decision) -> ConfidenceScore:
    """
    Score AI decision confidence against expert patterns.

    Research Purpose:
        - Validates hypothesis about prediction accuracy
        - Collects data for confidence calibration analysis
        - Supports Story 1.2: Real-time confidence classification

    Metrics Collected:
        - confidence_score: float (0-1)
        - confidence_color: str (green/orange/red)
        - prediction_time_ms: int
        - pattern_match_count: int
    """
    start_time = time.time()

    # ... implementation ...

    await log_research_metric({
        'epic': 1,
        'story': '1.2',
        'decision_id': decision.id,
        'confidence_score': score,
        'confidence_color': color,
        'prediction_time_ms': (time.time() - start_time) * 1000,
        'pattern_match_count': matches
    })

    return ConfidenceScore(score=score, color=color)
```

### 4. Privacy-First Design

**Automatically anonymize PII:**
```python
# GOOD
user_id = anonymize_user_id(raw_user_id)
decision_log.store(user_id=user_id, ...)

# BAD - Don't log raw PII
decision_log.store(email=user.email, ...)
```

**Follow GDPR principles:**
- Data minimization (only collect what's needed)
- Purpose limitation (only use for research)
- Storage limitation (respect retention policies)
- Consent management (track user consent)

### 5. Write Tests That Validate Research Requirements

```python
def test_confidence_score_logging():
    """Ensure all confidence scores are logged for research."""
    decision = create_test_decision()
    score = await score_confidence(decision)

    # Research requirement: All scores must be logged
    log_entry = DecisionLog.get_latest()
    assert log_entry.confidence_score == score.score
    assert log_entry.confidence_color == score.color
    assert log_entry.timestamp is not None
    assert log_entry.epic == 1
    assert log_entry.story == '1.2'
```

## Epic-Specific Guidelines

### Epic 1: CENTAUR Model Integration

**Focus:** Backend confidence scoring API

**Key Requirements:**
- <200ms response time
- >60% prediction accuracy (target >80%)
- Comprehensive decision logging
- Configurable confidence thresholds

**When working on Epic 1:**
1. Optimize for latency (use async, caching)
2. Log every prediction vs actual expert decision
3. Make confidence thresholds configurable (not hardcoded)
4. Include confidence breakdown in responses

**Code locations:**
- `src/psyai/features/confidence/` - Confidence scoring
- `src/psyai/platform/centaur/` - Centaur Model integration

### Epic 2: Expert Review UI

**Focus:** Frontend review interface

**Key Requirements:**
- Reduce cognitive load (color-coding, prioritization)
- Batch operations for efficiency
- Mobile-responsive
- Accessibility (WCAG 2.1 AA)

**When working on Epic 2:**
1. Every UI decision should reduce expert effort
2. Instrument timing data (time on each decision)
3. Track user interactions for cognitive load analysis
4. Prioritize red (low-confidence) items visually

**Code locations:**
- `src/psyai/features/hitl/` - Backend for HITL
- `frontend/` - React/Next.js frontend (to be created)

### Epic 3: Analytics Dashboard

**Focus:** Research metrics and data export

**Key Requirements:**
- Real-time metrics (<5s lag)
- Comprehensive data export (CSV/JSON)
- Statistical analysis support
- GDPR-compliant anonymization

**When working on Epic 3:**
1. Design for both real-time monitoring and post-hoc analysis
2. Export formats must work with R, Python, SPSS
3. Include all metadata researchers might need
4. Make visualizations publication-ready

**Code locations:**
- `src/psyai/features/analytics/` - Analytics feature
- `scripts/export_research_data.py` - Data export

## Commit Message Format

Link commits to research outline:

```
[Epic X.Y] Brief description

Longer description of what was implemented and why.

Research Impact:
- Supports hypothesis: [primary/secondary]
- Enables metric: [specific metric from outline]
- Epic X, Story X.Y: [story description]

Technical Notes:
- [Implementation details]
- [Performance considerations]
```

**Example:**
```
[Epic 1.2] Implement confidence color classification

Added real-time confidence classification (green/orange/red) based
on configurable thresholds. Default thresholds: >85% (green),
60-85% (orange), <60% (red).

Research Impact:
- Supports primary hypothesis (>80% prediction accuracy)
- Enables metric: Expert override rates by confidence color
- Epic 1, Story 1.2: Real-time confidence scores for prioritization

Technical Notes:
- Thresholds configurable via environment variables
- <200ms response time maintained
- Added comprehensive logging for research analysis
```

## Testing Requirements

### Unit Tests
- Test core functionality
- Test edge cases
- Test error handling

### Integration Tests
- Test API endpoints
- Test database operations
- Test external integrations (Centaur Model, Vertex AI)

### Research Validation Tests
- Test that all metrics are logged
- Test data export functionality
- Test anonymization
- Test GDPR compliance

### Example Test Structure
```python
class TestConfidenceScoring:
    """Tests for Epic 1, Story 1.1-1.3"""

    def test_score_accuracy(self):
        """Validate scoring logic."""
        pass

    def test_response_time(self):
        """Ensure <200ms requirement."""
        pass

    def test_logging_completeness(self):
        """Research: All scores must be logged."""
        pass

    def test_privacy_compliance(self):
        """Research: No PII in logs."""
        pass
```

## Documentation Requirements

### Code Documentation
```python
def function_name():
    """
    Brief description.

    Research Purpose:
        Explain which hypothesis/epic/story this supports.

    Metrics Collected:
        List what data is logged for research.

    Privacy Considerations:
        Note any PII handling or anonymization.

    Args:
        ...

    Returns:
        ...
    """
```

### API Documentation
- OpenAPI/Swagger specs
- Include research context in endpoint descriptions
- Document what metrics each endpoint collects

### Epic Documentation
- Update epic docs when implementing stories
- Check off acceptance criteria
- Note any deviations from the plan

## Common LLM Contribution Scenarios

### Scenario 1: "Implement Story 1.1"

1. Read `docs/epics/EPIC_1_CENTAUR_INTEGRATION.md`
2. Review Story 1.1 acceptance criteria
3. Check existing code in `src/psyai/features/confidence/`
4. Implement with research logging
5. Write tests validating research requirements
6. Update epic doc (check off acceptance criteria)
7. Commit with epic reference

### Scenario 2: "Add a new feature"

**Stop and ask:**
- Which epic does this belong to?
- Is this in the research outline?
- If not, should we add it to the outline first?

All features must support the research objectives. Don't add features that don't align with Epics 1-3 without discussion.

### Scenario 3: "Fix a bug"

**Consider research impact:**
- Does this affect logged metrics?
- Could this change research results?
- Should we document this in the research paper (methods section)?

Even bug fixes can have research implications.

### Scenario 4: "Optimize performance"

**Maintain research requirements:**
- Keep all logging in place
- Preserve metric collection
- Don't sacrifice data completeness for speed
- Document performance improvements (these are results!)

## Helpful Claude Code Commands

Use these slash commands for quick context:

- `/research-context` - Display research hypotheses and objectives
- `/epic [1|2|3]` - Get details on a specific epic
- `/architecture` - Show system architecture
- `/review-code` - Review code for research compliance

## Key Principles for LLM Contributors

1. **Research-first development** - Every line of code supports the study
2. **Comprehensive logging** - If it's not logged, it didn't happen
3. **Privacy by default** - Anonymize first, ask questions later
4. **Measurable outcomes** - How will researchers analyze this?
5. **Epic traceability** - Link all work to Epic 1, 2, or 3
6. **Scientific rigor** - Documentation should be publication-ready
7. **Reproducibility** - Future researchers should understand your code

## Questions to Ask Before Contributing

Before implementing any feature, ask:

1. **Which epic/story does this implement?**
2. **What hypothesis does this help validate?**
3. **What metrics will this collect?**
4. **How will researchers export/analyze this data?**
5. **What are the privacy implications?**
6. **Does this maintain <200ms API response time?**
7. **Is this documented clearly for future researchers?**

If you can't answer these questions, read the epic documentation or ask for clarification.

## Getting Help

### Documentation Resources
- `PROJECT_CONTEXT.md` - Project overview
- `docs/epics/` - Epic and story specifications
- `Collaborative Writing/psyAI Research Paper - Outline 2.md` - Research outline
- `README.md` - Technical setup and architecture
- `GETTING_STARTED.md` - Development workflow

### When Stuck
1. Read the relevant epic documentation
2. Check the research outline for context
3. Review existing code in the feature area
4. Look for similar implementations in other features
5. Ask the project maintainers (open an issue)

## Remember

You're not just writing code - you're contributing to scientific research that could improve human-AI collaboration. Your work will be part of a published research paper and could influence future HITL and LLM-as-a-judge systems.

Write code that future researchers will thank you for.

## License

By contributing to PsyAI, you agree to license your contributions under the MIT License.
