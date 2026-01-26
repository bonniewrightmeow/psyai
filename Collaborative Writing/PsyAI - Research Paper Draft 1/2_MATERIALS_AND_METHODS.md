# Materials and Methods

## Study Design

This study employed a comparative experimental design with repeated measures across four decision-making conditions. The research followed an agile development methodology for system implementation, followed by controlled experimental evaluation. The study protocol received approval from [IRB/Ethics Committee - TBD], and all participants provided informed consent prior to participation.

### Experimental Conditions

Participants completed decision-making tasks under four conditions, presented in counterbalanced order to control for learning effects:

1. **AI-Alone:** Decisions made entirely by the AI agent without human review
2. **Human-Alone:** Decisions made entirely by human experts without AI assistance
3. **Traditional Human-AI Collaboration:** All AI decisions presented to human experts for review and validation
4. **Proxy Agent Framework:** AI decisions pre-classified by confidence; only medium and low-confidence decisions presented for expert review

### Outcome Measures

**Primary Outcomes:**
- Decision accuracy (percentage agreement with gold standard expert consensus)
- Decision throughput (decisions completed per hour)
- Decision quality metrics (consistency, appropriateness, alignment with domain standards)

**Secondary Outcomes:**
- Cognitive load (NASA-TLX scores, time-on-task, decision reversals)
- Expert satisfaction (post-task surveys)
- Efficiency metrics (time saved, batch approval rates)

## Materials

### Decision Confidence Framework Backend

**Core Components:**
- **Centaur Model Integration:** Python implementation of the Centaur Foundation Model for predicting human expert decisions
- **Confidence Scoring API:** RESTful API built with FastAPI providing real-time confidence classification
- **Google Vertex AI Integration:** Gemini 1.5 Pro model for agentic workflow execution
- **Vector Search System:** Vertex AI Vector Search for retrieving similar past expert decisions (RAG)

**Technical Specifications:**
- Cloud infrastructure: Google Cloud Platform
- Database: PostgreSQL 15 for decision logs and user data
- Cache layer: Redis for performance optimization
- API response time target: <200ms (95th percentile)

**Confidence Classification Algorithm:**
The system classifies AI decisions into three categories based on predicted alignment with expert decision patterns:
- **Green (High Confidence):** >85% predicted match probability
- **Orange (Medium Confidence):** 60-85% predicted match probability
- **Red (Low Confidence):** <60% predicted match probability

Confidence scores are calculated using:
1. Centaur Model prediction of expert decision
2. Vector similarity to past expert decisions in similar contexts
3. Decision context complexity assessment
4. Historical override rates for similar decision types

### Expert Decision Review Interface

**Frontend Application:**
- Framework: React 18 with Next.js 14
- Real-time updates: WebSocket connection for live decision feeds
- Responsive design: Mobile, tablet, and desktop support
- Accessibility: WCAG 2.1 AA compliant

**Key Features:**
- Color-coded decision queue organized by confidence level
- Batch approval interface for high-confidence decisions
- Detailed decision cards showing:
  - AI reasoning and confidence breakdown
  - Similar past expert decisions (RAG-retrieved)
  - Key factors influencing confidence rating
  - Decision context and relevant data
- Feedback mechanism for rating AI decision quality
- Performance dashboard showing throughput and accuracy metrics

### Cognitive Load Measurement Instruments

**NASA Task Load Index (NASA-TLX):**
Administered after each experimental condition to assess subjective workload across six dimensions:
- Mental demand
- Physical demand
- Temporal demand
- Performance
- Effort
- Frustration

**Objective Cognitive Load Indicators:**
- Time spent per decision (milliseconds, logged automatically)
- Decision reversal rate (frequency of changing initial decision)
- Session duration and break patterns
- Accuracy degradation over time (indicator of fatigue)

### Data Logging and Analytics System

**Comprehensive Data Capture:**
All system interactions logged in PostgreSQL database with:
- Decision metadata (timestamp, user ID, decision type, context)
- AI predictions and confidence scores
- Expert actions (accept, reject, modify, skip)
- Timing data (decision duration, session length, idle time)
- Feedback ratings and comments
- Experimental condition identifiers

**Privacy and Compliance:**
- Automatic PII anonymization using one-way hashing
- Data retention policies: 2 years for research analysis
- GDPR-compliant consent management
- Audit trails for all data access
- Secure cloud storage with encryption at rest and in transit

## Participants

### Recruitment

Target sample: N=50 expert users recruited through:
- Professional networks in target domains
- Industry partnerships
- Academic collaborations
- Participant referrals

### Inclusion Criteria

- Minimum 2 years professional experience in relevant domain (e.g., medical diagnosis, financial analysis, legal review, or similar fields requiring expert judgment)
- Regular engagement with AI-assisted decision-making tools (at least weekly)
- Proficiency with web-based software applications
- Availability for 4-6 hour study commitment (across multiple sessions)

### Exclusion Criteria

- Prior exposure to the Centaur Model or similar decision prediction systems
- Cognitive impairments affecting decision-making ability
- Concurrent participation in other decision-making studies

### Participant Compensation

Participants received $150 compensation for study completion, pro-rated for partial completion.

### Sample Characteristics

Demographic data collected (anonymized):
- Age range and distribution
- Years of professional experience
- Domain expertise area
- Prior AI tool usage frequency
- Educational background

[Note: Actual demographic statistics to be added after data collection]

## Procedure

### Phase 1: Baseline Assessment (Week 1)

**Participant Onboarding:**
1. Informed consent process
2. Demographic survey and expertise assessment
3. System training (30 minutes, standardized tutorial)
4. Practice tasks (10 decisions, not included in analysis)

**Baseline Decision Pattern Collection:**
Participants completed 50 decision tasks without AI assistance to establish individual decision patterns. These baseline decisions were used to:
- Train participant-specific decision prediction models
- Establish gold standard for accuracy comparison
- Assess baseline decision speed and consistency

### Phase 2: Centaur Model Training (Week 2)

**Model Training Process:**
1. Centaur Model fine-tuned on psychology datasets (original model training)
2. Participant-specific adaptation using baseline decision data
3. Confidence threshold calibration for each participant
4. Validation testing on held-out decision set (10% of baseline)

**Model Performance Criteria:**
Minimum 60% prediction accuracy required before proceeding to experimental phases. Models achieving <60% accuracy underwent additional training or participant exclusion if performance did not improve.

### Phase 3: Experimental Testing (Weeks 3-5)

**Experimental Sessions:**
Each participant completed four sessions (one per condition), each consisting of:
- Pre-session NASA-TLX baseline
- Decision-making task (40 decisions per session)
- Post-session NASA-TLX
- Brief satisfaction survey

**Session Specifications:**
- Duration: Approximately 60-90 minutes per session
- Minimum 24-hour interval between sessions
- Randomized condition order (Latin square design)
- Identical decision sets across conditions (counterbalanced for order effects)

**Decision Task Characteristics:**
- Domain-appropriate realistic scenarios
- Range of difficulty levels (simple, moderate, complex)
- Clear correct answers established by expert consensus panel
- Matched across experimental conditions for difficulty and content

### Phase 4: Data Analysis (Week 6)

**Statistical Analysis Plan:**
- Repeated measures ANOVA for condition comparisons
- Mixed-effects models accounting for individual differences
- Post-hoc pairwise comparisons with Bonferroni correction
- Effect size calculations (Cohen's d, partial eta-squared)
- Correlation analyses between confidence scores and accuracy

**Subgroup Analyses:**
- Experience level (junior vs. senior experts)
- Domain type
- Baseline decision speed
- AI tool familiarity

## Development Framework

### Agile Implementation Methodology

The proxy agent framework was developed using three-week sprints across three major epics:

**Epic 1: CENTAUR Model Integration (Weeks 1-6)**
- Sprint 1-2: Confidence scoring API and Centaur Model integration
- Sprint 3: Real-time classification system and comprehensive logging

**Epic 2: Expert Review Interface (Weeks 7-12)**
- Sprint 4-5: Decision queue UI, color-coding, and filtering
- Sprint 6: Batch approval, detailed decision views, and feedback mechanisms

**Epic 3: Analytics Dashboard (Weeks 13-18)**
- Sprint 7-8: Real-time metrics dashboards and cognitive load tracking
- Sprint 9: Data export capabilities and research analysis tools

### Quality Assurance

**Testing Protocols:**
- Unit tests for all API endpoints (>90% code coverage)
- Integration tests for end-to-end workflows
- Performance testing under simulated load (100 concurrent users)
- Usability testing with pilot participants (N=5, not included in main study)

**Performance Validation:**
- API response times monitored continuously
- Database query optimization for <50ms latency
- Frontend rendering performance (60fps target)
- Real-time update latency <500ms

## Data Management

### Data Storage

**Primary Database (PostgreSQL):**
- Decision logs with full metadata
- User profiles (anonymized)
- Experimental session data
- Survey responses

**Vector Database (Vertex AI Vector Search):**
- Embedded representations of past decisions
- Similarity search for RAG functionality
- Indexed for <100ms retrieval time

**Analytics Data Warehouse:**
- Aggregated metrics for dashboard display
- Time-series data for trend analysis
- Export-ready datasets for statistical software

### Data Security

- AES-256 encryption at rest
- TLS 1.3 for data in transit
- Role-based access control (RBAC)
- Regular security audits
- Automated backup (daily, 30-day retention)

### Data Export

Research data exported in multiple formats:
- CSV for statistical analysis (R, Python, SPSS)
- JSON for programmatic access
- Excel for manual review
- Anonymized datasets for publication and replication

## Statistical Power Analysis

**Sample Size Justification:**
Power analysis conducted using G*Power 3.1:
- Effect size: d=0.50 (medium, based on pilot data and literature)
- Alpha: 0.05 (two-tailed)
- Power: 0.80
- Number of conditions: 4
- Repeated measures correlation: 0.50 (estimated)
- **Required N: 45 participants**
- Target N: 50 (accounting for 10% attrition)

## Ethical Considerations

### Informed Consent

Participants provided written informed consent covering:
- Study purpose and procedures
- Time commitment and compensation
- Data collection and privacy protections
- Right to withdraw without penalty
- Potential risks and benefits

### Privacy Protection

- Participant identifiers replaced with anonymous codes
- No collection of unnecessary personal information
- Secure data storage with restricted access
- Compliance with GDPR and institutional privacy policies

### Risk Mitigation

**Potential Risks:**
- Mild fatigue from decision-making tasks (mitigated by session breaks)
- Frustration with system interface (mitigated by training and support)
- Privacy concerns (mitigated by transparency and anonymization)

**Benefits:**
- Compensation for time
- Contribution to scientific knowledge
- Potential improvements to AI tools used in professional work

---

## References

Hart, S. G., & Staveland, L. E. (1988). Development of NASA-TLX (Task Load Index): Results of empirical and theoretical research. In *Advances in psychology* (Vol. 52, pp. 139-183). North-Holland.

[Additional methodological references to be added]
