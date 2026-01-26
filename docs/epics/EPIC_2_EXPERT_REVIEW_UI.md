# Epic 2: Expert Review User Interface

## Epic Overview

Build an intuitive web interface that allows expert users to efficiently review AI decisions, focusing their attention on low-confidence items while batch-approving high-confidence decisions.

## Epic Goal

Reduce expert cognitive load and decision fatigue by providing a color-coded, prioritized review interface that leverages confidence scores from the Centaur Model.

## User Stories

### Story 2.1: Color-Coded Decision Display

**As an** expert user
**I want to** see AI decisions color-coded by confidence level
**So I can** quickly identify which decisions need my attention

**Acceptance Criteria:**
- [ ] Decision queue shows color indicators (green/orange/red)
- [ ] Visual hierarchy prioritizes red items first
- [ ] Quick summary of decision and confidence score
- [ ] Filter by confidence color
- [ ] Sort by confidence score, timestamp, priority

**Technical Implementation:**
- React/Next.js dashboard
- Color-coded card components
- Real-time updates via WebSocket
- Filtering and sorting UI

**Research Metrics:**
- Time to identify low-confidence decisions
- Visual attention patterns (if eye-tracking available)
- User preference ratings

---

### Story 2.2: Batch Approval for High-Confidence Decisions

**As an** expert user
**I want to** batch-approve green (high-confidence) decisions
**So I can** focus time on red (low-confidence) decisions

**Acceptance Criteria:**
- [ ] Select multiple green decisions
- [ ] Single-click batch approval
- [ ] Confirmation dialog with summary
- [ ] Undo capability (time-limited)
- [ ] Audit trail of batch approvals

**Technical Implementation:**
- Multi-select UI component
- Batch API endpoint: `POST /api/v1/decisions/batch-approve`
- Optimistic UI updates
- Undo mechanism (5-minute window)

**Research Metrics:**
- Average batch size
- Time saved vs individual approvals
- Batch approval accuracy (measured by later reviews)
- Undo frequency

---

### Story 2.3: Detailed Decision Explanations

**As an** expert user
**I want** detailed explanations for orange/red decisions
**So I can** make informed override decisions

**Acceptance Criteria:**
- [ ] Expandable decision card showing full context
- [ ] AI reasoning and confidence breakdown
- [ ] Similar past expert decisions (using RAG/memory)
- [ ] Key factors influencing confidence rating
- [ ] Original prompt and AI response
- [ ] Suggested expert action

**Technical Implementation:**
- Expandable card component
- Decision detail API: `GET /api/v1/decisions/{id}/details`
- RAG integration for similar past decisions
- Confidence factor visualization

**Research Metrics:**
- Time spent reviewing orange vs red decisions
- Expert override rate by decision type
- User satisfaction with explanations

---

### Story 2.4: Expert Feedback Mechanism

**As an** expert user
**I want to** provide feedback on AI decisions
**So** the system can improve its confidence predictions

**Acceptance Criteria:**
- [ ] Thumbs up/down on AI decision quality
- [ ] Optional text feedback
- [ ] "This should have been [color]" reclassification
- [ ] Feedback stored for model improvement
- [ ] Feedback summary in analytics dashboard

**Technical Implementation:**
- Feedback UI component
- Feedback API: `POST /api/v1/decisions/{id}/feedback`
- Feedback storage in decision log
- Feedback aggregation for model training

**Research Metrics:**
- Feedback submission rate
- Correlation between feedback and confidence scores
- Model improvement from feedback loop
- Expert engagement with feedback feature

## Technical Requirements

### Frontend Architecture
```
┌─────────────────────────────────┐
│  Next.js/React Dashboard        │
├─────────────────────────────────┤
│  - Decision Queue (color-coded) │
│  - Batch Approval Interface     │
│  - Decision Detail View         │
│  - Feedback Components          │
│  - Analytics Display            │
└────────────┬────────────────────┘
             │
    ┌────────▼────────┐
    │  WebSocket      │
    │  Real-time      │
    │  Updates        │
    └────────┬────────┘
             │
┌────────────▼────────────────────┐
│  FastAPI Backend                │
│  - Decision API                 │
│  - Batch Operations             │
│  - Feedback API                 │
└─────────────────────────────────┘
```

### UI/UX Requirements
- Mobile-responsive design
- Accessible (WCAG 2.1 AA)
- Dark mode support
- Keyboard shortcuts for power users
- Loading states and error handling
- Optimistic UI updates

### Performance Requirements
- Initial page load: <2 seconds
- Decision card render: <100ms
- Real-time update latency: <500ms
- Smooth scrolling for 1000+ decisions

## Dependencies

### Backend Dependencies (Epic 1)
- Confidence scoring API
- Decision logging system
- Expert pattern database

### Frontend Dependencies
- Next.js/React framework
- WebSocket support
- Authentication system
- Analytics integration

## Success Metrics

### Technical Metrics
- Page load time p95: <2s
- UI responsiveness: 60fps
- WebSocket uptime: 99.9%
- Zero client-side errors

### Research Metrics
- Decision throughput (decisions/hour)
- Time saved vs traditional review
- Cognitive load reduction (self-reported + measured)
- Expert satisfaction scores
- Accuracy of batch-approved decisions

## Implementation Phases

### Phase 1: Basic UI (Week 1-2)
- Decision queue with color coding
- Single decision review
- Basic filtering and sorting

### Phase 2: Batch Operations (Week 3-4)
- Multi-select interface
- Batch approval API
- Undo functionality

### Phase 3: Advanced Features (Week 5-6)
- Detailed explanations with RAG
- Feedback mechanism
- Performance optimizations
- Analytics integration

## Design Mockups

### Decision Queue View
```
┌───────────────────────────────────────────┐
│  PsyAI Expert Review Dashboard            │
├───────────────────────────────────────────┤
│  [Filters: All | 🟢 Green | 🟠 Orange | 🔴 Red]│
│  [Sort: Priority ▼]  [Batch Actions ▼]    │
├───────────────────────────────────────────┤
│  🔴 HIGH PRIORITY (12)                     │
│  ┌─────────────────────────────────────┐  │
│  │ [checkbox] Decision #1234            │  │
│  │ Confidence: 45% - Review Required    │  │
│  │ Context: Patient case evaluation...  │  │
│  │ [Review Details] [Accept] [Reject]   │  │
│  └─────────────────────────────────────┘  │
│                                            │
│  🟠 MEDIUM PRIORITY (28)                   │
│  🟢 AUTO-APPROVED (156)                    │
└───────────────────────────────────────────┘
```

## Related Documentation

- [API Specification](../architecture/API_SPEC.md)
- [UI/UX Guidelines](../architecture/UI_UX_GUIDELINES.md)
- [Epic 1: CENTAUR Integration](./EPIC_1_CENTAUR_INTEGRATION.md)
- [Research Outline](../../Collaborative Writing/psyAI Research Paper - Outline 2.md)

## Code Locations

```
src/psyai/features/hitl/           # Human-in-the-loop review feature
frontend/                          # React/Next.js frontend (to be created)
src/psyai/platform/api/            # Backend API endpoints
tests/features/hitl/               # Feature tests
```

## Notes for LLM Contributors

When implementing Story 2.x:
1. Focus on reducing cognitive load - every UI decision should minimize expert effort
2. Prioritize accessibility - experts may work long hours
3. Include comprehensive analytics tracking for research
4. Follow Material Design or similar design system for consistency
5. Write integration tests that simulate expert workflows
6. Consider mobile/tablet use cases (experts on the go)
