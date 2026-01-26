# Epic 3: Analytics and Research Dashboard

## Epic Overview

Build a comprehensive analytics dashboard that tracks decision throughput, accuracy metrics, and cognitive load indicators to support research data collection and real-time monitoring.

## Epic Goal

Enable researchers to monitor the study in real-time and collect quantitative data to validate the research hypotheses about decision quality, speed, and cognitive load reduction.

## User Stories

### Story 3.1: Real-time Decision Metrics Dashboard

**As a** researcher
**I need** real-time dashboards showing decision throughput and accuracy metrics
**So I can** monitor the study and identify issues quickly

**Acceptance Criteria:**
- [ ] Live metrics for decisions processed per hour/day
- [ ] Accuracy metrics (AI prediction vs expert decision)
- [ ] Confidence score distribution visualization
- [ ] Expert override rates by confidence color
- [ ] Comparison across experimental conditions
- [ ] Auto-refresh every 30 seconds

**Technical Implementation:**
- Analytics dashboard page (React/Next.js)
- Real-time metrics API: `GET /api/v1/analytics/realtime`
- WebSocket for live updates
- Charting library (Chart.js or D3.js)
- Metrics aggregation service

**Research Metrics:**
- Decision throughput (decisions/hour per expert)
- AI prediction accuracy (% agreement with expert)
- Confidence calibration (predicted vs actual accuracy by color)
- Override patterns (which types of decisions are overridden)

---

### Story 3.2: Cognitive Load Tracking

**As a** researcher
**I want to** track cognitive load indicators (time spent, decision reversals, user feedback)
**So I can** measure the impact of the proxy agent framework on expert workload

**Acceptance Criteria:**
- [ ] Time spent per decision (average, median, p95)
- [ ] Decision reversal rate (experts changing their mind)
- [ ] Self-reported cognitive load surveys (integrated)
- [ ] Session duration and break patterns
- [ ] Decision fatigue indicators (accuracy decline over time)
- [ ] Comparison across experimental groups

**Technical Implementation:**
- Client-side timing instrumentation
- Decision reversal detection algorithm
- Survey integration (periodic pop-ups)
- Session tracking with idle detection
- Time-series analysis of decision accuracy

**Research Metrics:**
- Average time per decision by confidence color
- Decision reversal frequency
- Cognitive load survey scores (NASA-TLX or similar)
- Session engagement patterns
- Accuracy degradation curves

---

### Story 3.3: Research Data Export

**As a** researcher
**I need** export capabilities for statistical analysis of experimental data
**So I can** perform rigorous statistical analysis and write the research paper

**Acceptance Criteria:**
- [ ] Export decisions and metrics to CSV/JSON
- [ ] Date range and filter selection
- [ ] Anonymized data export (GDPR compliant)
- [ ] Include all relevant metadata
- [ ] Export cognitive load survey responses
- [ ] Batch export for all participants
- [ ] Schedule automated exports

**Technical Implementation:**
- Export API: `POST /api/v1/analytics/export`
- Data anonymization pipeline
- CSV/JSON/Excel format support
- Async job processing for large exports
- S3/Cloud Storage integration
- Email notification on completion

**Research Metrics:**
- All decision log data
- Confidence scores and classifications
- Expert acceptance/rejection/override
- Timing data (decision duration, session length)
- Survey responses
- Demographic data (anonymized)

## Technical Requirements

### Analytics Architecture
```
┌─────────────────────────────────┐
│  Analytics Dashboard (Frontend) │
├─────────────────────────────────┤
│  - Real-time Metrics            │
│  - Cognitive Load Charts        │
│  - Export Interface             │
└────────────┬────────────────────┘
             │
    ┌────────▼────────┐
    │  WebSocket      │
    │  Live Updates   │
    └────────┬────────┘
             │
┌────────────▼────────────────────┐
│  Analytics Service              │
├─────────────────────────────────┤
│  - Metrics Aggregation          │
│  - Time-series Analysis         │
│  - Statistical Calculations     │
└────────────┬────────────────────┘
             │
┌────────────▼────────────────────┐
│  Decision Log Database          │
│  (PostgreSQL + TimescaleDB)     │
└─────────────────────────────────┘
```

### Data Requirements
- Real-time aggregation (<5 second lag)
- Historical data retention: 2+ years
- Query performance: <500ms for dashboard loads
- Export size support: Up to 1M records
- Anonymization: Automatic PII removal

### Visualization Requirements
- Interactive charts (zoom, filter, drill-down)
- Multiple chart types (line, bar, scatter, heatmap)
- Responsive design (mobile, tablet, desktop)
- Export charts as PNG/SVG
- Color-blind friendly palette

## Dependencies

### Backend Dependencies
- Epic 1: Decision logging system
- Epic 2: Frontend framework
- TimescaleDB or similar time-series database
- Task queue (Celery/RQ) for async exports

### Frontend Dependencies
- Chart.js or D3.js
- Data grid component (AG Grid or similar)
- Export library (Papa Parse for CSV)

## Success Metrics

### Technical Metrics
- Dashboard load time: <2 seconds
- Real-time update latency: <5 seconds
- Export job completion: 95% within 5 minutes
- Zero data loss in aggregation

### Research Metrics
- Comprehensive data capture rate: >99%
- Survey response rate: >80%
- Export data validity: 100% (no corrupted exports)
- Researcher satisfaction with analytics tools

## Implementation Phases

### Phase 1: Core Metrics (Week 1-2)
- Basic decision throughput dashboard
- Accuracy metrics
- Simple CSV export

### Phase 2: Cognitive Load (Week 3-4)
- Timing instrumentation
- Cognitive load surveys
- Advanced visualizations

### Phase 3: Advanced Analytics (Week 5-6)
- Statistical analysis tools
- Comparison dashboards
- Automated reporting
- Publication-ready visualizations

## Dashboard Views

### Main Analytics View
```
┌─────────────────────────────────────────────────┐
│  PsyAI Research Analytics Dashboard             │
├─────────────────────────────────────────────────┤
│  [Date Range: Last 7 Days ▼]  [Export ▼]        │
├─────────────────────────────────────────────────┤
│  Key Metrics                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  │ 1,247    │ │ 78.4%    │ │ 142      │         │
│  │ Decisions│ │ Accuracy │ │ Decisions│         │
│  │ Processed│ │          │ │ /Hour    │         │
│  └──────────┘ └──────────┘ └──────────┘         │
├─────────────────────────────────────────────────┤
│  Decision Throughput Over Time                  │
│  [Line Chart: Decisions/hour by condition]      │
├─────────────────────────────────────────────────┤
│  Confidence Distribution                        │
│  [Stacked Bar: Green/Orange/Red by day]         │
├─────────────────────────────────────────────────┤
│  Cognitive Load Indicators                      │
│  [Multi-line: Avg time, Reversals, Accuracy]    │
└─────────────────────────────────────────────────┘
```

## Key Research Questions Answered

This epic directly supports answering:
1. Does the proxy agent framework improve decision speed?
2. Does it reduce cognitive load?
3. What is the accuracy of AI predictions vs expert decisions?
4. How do experts interact with different confidence levels?
5. What patterns emerge in expert decision-making?

## Related Documentation

- [Research Hypotheses](../research/HYPOTHESES.md)
- [Statistical Analysis Plan](../research/ANALYSIS_PLAN.md)
- [Data Dictionary](../architecture/DATA_DICTIONARY.md)
- [Research Outline](../../Collaborative Writing/psyAI Research Paper - Outline 2.md)

## Code Locations

```
src/psyai/features/analytics/      # Analytics feature
src/psyai/platform/api/analytics/  # Analytics API endpoints
frontend/components/analytics/     # Dashboard components
tests/features/analytics/          # Feature tests
scripts/export_research_data.py    # Research data export script
```

## Statistical Analysis Integration

### Planned Analyses (for Q1 2026 study)
- Repeated measures ANOVA (comparing 4 conditions)
- Mixed-effects models (accounting for individual differences)
- Time-series analysis (decision patterns over time)
- Correlation analysis (confidence scores vs accuracy)
- Cognitive load regression models

### Data Export Format
```csv
participant_id,condition,timestamp,decision_id,ai_decision,expert_decision,confidence_score,confidence_color,time_spent_ms,reversal,survey_score
P001,proxy_agent,2026-01-15T10:23:45,D12345,accept,accept,0.89,green,2341,false,3
P001,proxy_agent,2026-01-15T10:24:12,D12346,accept,reject,0.72,orange,8932,true,4
...
```

## Notes for LLM Contributors

When implementing Story 3.x:
1. All metrics must support research validity - design with statistical analysis in mind
2. Ensure data anonymization is automatic and irreversible
3. Build for both real-time monitoring and post-hoc analysis
4. Include comprehensive documentation for researchers unfamiliar with the codebase
5. Make visualizations publication-ready (high resolution, proper labeling)
6. Consider export formats compatible with R, Python (pandas), SPSS
7. Test with realistic data volumes (simulate 50 experts x 6 weeks)
