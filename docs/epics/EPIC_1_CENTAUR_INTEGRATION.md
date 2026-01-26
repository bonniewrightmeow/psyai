# Epic 1: CENTAUR Model Integration Prototype

## Epic Overview

Build the core confidence scoring system that analyzes AI decisions against expert patterns using the Centaur Foundation Model.

## Epic Goal

Create a backend API that can predict expert decisions and classify them by confidence level in real-time to enable efficient human-AI collaboration.

## User Stories

### Story 1.1: Confidence Scoring API

**As a** researcher
**I need** a confidence scoring API that analyzes AI decisions against expert patterns
**So I can** classify decision reliability

**Acceptance Criteria:**
- [ ] API endpoint accepts AI decision and context
- [ ] System compares decision against trained expert patterns
- [ ] Returns confidence score (0-100%) and classification
- [ ] Response time <200ms
- [ ] Handles concurrent requests (100+ users)

**Technical Implementation:**
- `/api/v1/confidence/score` POST endpoint
- Integration with Centaur Model
- Expert pattern database lookup
- Confidence calculation algorithm

**Research Metrics:**
- API response times
- Prediction accuracy vs actual expert decisions
- Pattern matching success rate

---

### Story 1.2: Real-time Confidence Classification

**As a** system
**I need to** return confidence scores (green/orange/red) in real-time
**So** experts can prioritize their review time

**Acceptance Criteria:**
- [ ] Green: >85% match probability
- [ ] Orange: 60-85% match probability
- [ ] Red: <60% match probability
- [ ] Color classification included in API response
- [ ] Classification logic is configurable
- [ ] Real-time processing (<200ms)

**Technical Implementation:**
- Confidence threshold configuration
- Color classification logic
- Response format: `{score: float, color: string, reasoning: string}`

**Research Metrics:**
- Distribution of confidence levels
- Expert override rates per color
- Time savings from green auto-approval

---

### Story 1.3: Comprehensive Decision Logging

**As a** developer
**I need** comprehensive logging of all decisions and confidence scores
**For** research analysis

**Acceptance Criteria:**
- [ ] Log every AI decision and confidence score
- [ ] Capture expert acceptance/rejection
- [ ] Track decision metadata (timestamp, context, user)
- [ ] Store for longitudinal analysis
- [ ] GDPR/privacy compliant
- [ ] Export capability for analysis

**Technical Implementation:**
- Database schema for decision logs
- Audit trail system
- Privacy compliance (anonymization, consent)
- Export API endpoint
- Data retention policies

**Research Metrics:**
- Total decisions logged
- Expert agreement rates
- Pattern evolution over time
- Cognitive load indicators

## Technical Requirements

### Backend Architecture
```
┌─────────────────┐
│  FastAPI        │
│  Endpoint       │
└────────┬────────┘
         │
┌────────▼────────┐
│  Confidence     │
│  Scorer         │
└────────┬────────┘
         │
┌────────▼────────┐     ┌──────────────┐
│  Centaur Model  │────▶│  Expert      │
│  Integration    │     │  Patterns DB │
└────────┬────────┘     └──────────────┘
         │
┌────────▼────────┐
│  Decision Log   │
│  Database       │
└─────────────────┘
```

### Performance Requirements
- API response time: <200ms (p95)
- Throughput: 100+ concurrent users
- Database write latency: <50ms
- Model inference time: <150ms

### Data Requirements
- Expert decision pattern storage
- Decision log retention: 2+ years
- Privacy compliance: GDPR, anonymization
- Backup and recovery: Daily backups

## Dependencies

### Platform Layer (Required)
- Core Infrastructure (config, logging)
- Vertex AI Integration (Gemini models)
- Storage Layer (PostgreSQL, Redis)
- API Framework (FastAPI)

### External Dependencies
- Centaur Foundation Model integration
- Vertex AI Vector Search (for pattern matching)
- Expert pattern training data

## Success Metrics

### Technical Metrics
- API uptime: 99.9%
- Response time p95: <200ms
- Prediction accuracy: >60% (target >80%)
- Zero data loss in logging

### Research Metrics
- Confidence score correlation with expert decisions
- False positive rate (green predictions that experts reject)
- False negative rate (red predictions that experts accept)
- Decision throughput improvement

## Implementation Phases

### Phase 1: Core API (Week 1-2)
- Basic confidence scoring endpoint
- Simple pattern matching
- Database logging

### Phase 2: Centaur Integration (Week 3-4)
- Full Centaur Model integration
- Advanced pattern matching
- Confidence calibration

### Phase 3: Optimization (Week 5-6)
- Performance tuning
- Concurrent user scaling
- Analytics dashboard integration

## Related Documentation

- [Centaur Foundation Model Paper](https://arxiv.org/abs/2410.20268)
- [API Specification](../architecture/API_SPEC.md)
- [Database Schema](../architecture/DATABASE_SCHEMA.md)
- [Research Outline](../../Collaborative Writing/psyAI Research Paper - Outline 2.md)

## Code Locations

```
src/psyai/features/confidence/     # Confidence scoring feature
src/psyai/platform/centaur/        # Centaur Model integration
src/psyai/platform/api/            # API endpoints
tests/features/confidence/         # Feature tests
```

## Notes for LLM Contributors

When implementing Story 1.x:
1. All code must include comprehensive logging for research
2. Follow privacy-first design (anonymization by default)
3. Make confidence thresholds configurable (not hardcoded)
4. Include detailed docstrings explaining research purpose
5. Write tests that validate research requirements
