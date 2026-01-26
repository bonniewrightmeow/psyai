# Results

[Note: This section contains hypothetical results based on the research design. Actual data will be collected during the Q1 2026 study and results will be updated accordingly.]

## Participant Characteristics

A total of 52 participants were recruited, with 50 completing all experimental sessions (96% retention rate). Two participants withdrew due to scheduling conflicts. The final sample (N=50) comprised experts from three primary domains:

- Medical diagnosis and treatment planning: n=18 (36%)
- Financial analysis and investment decisions: n=16 (32%)
- Legal document review and case assessment: n=16 (32%)

**Demographic Characteristics:**
- Mean age: 38.4 years (SD=7.2, range: 28-56)
- Mean years of professional experience: 12.6 years (SD=5.8, range: 2-28)
- Gender distribution: 26 female (52%), 24 male (48%)
- Prior AI tool usage: Weekly (n=31, 62%), Daily (n=19, 38%)

There were no significant demographic differences across experimental condition orders (all p>.05), confirming successful randomization.

## Model Performance

### Centaur Model Prediction Accuracy

The Centaur Model achieved varying levels of prediction accuracy across participants:

**Overall Prediction Accuracy:**
- Mean accuracy: 72.4% (SD=8.6%, range: 58.2%-88.7%)
- Participants achieving >80% threshold: n=14 (28%)
- Participants achieving >70% threshold: n=36 (72%)
- Participants below 60% threshold: n=2 (4%, excluded from primary analysis)

**Accuracy by Confidence Classification:**
- High confidence (green) predictions: 89.3% accurate (n=1,247 decisions)
- Medium confidence (orange) predictions: 71.8% accurate (n=892 decisions)
- Low confidence (red) predictions: 42.1% accurate (n=361 decisions)

These results demonstrate strong calibration of the confidence classification system, with high-confidence predictions showing substantially higher accuracy than low-confidence predictions, χ²(2)=486.2, p<.001.

### API Performance Metrics

The confidence scoring API consistently met performance targets:

**Response Time:**
- Mean: 142ms (SD=28ms)
- 95th percentile: 187ms
- 99th percentile: 214ms
- Target: <200ms (95th percentile) ✓ Achieved

**System Reliability:**
- Uptime: 99.94% during experimental period
- Zero data loss events
- Database write latency: Mean=34ms (SD=12ms)

## Primary Outcomes

### Decision Accuracy

A repeated-measures ANOVA revealed a significant main effect of experimental condition on decision accuracy, F(3,147)=18.42, p<.001, partial η²=.273.

**Mean Decision Accuracy by Condition:**
| Condition | Mean | SD | 95% CI |
|-----------|------|----|----|
| AI-Alone | 76.2% | 6.4% | [74.4%, 78.0%] |
| Human-Alone | 82.8% | 5.1% | [81.4%, 84.2%] |
| Traditional Human-AI | 85.3% | 4.8% | [84.0%, 86.6%] |
| Proxy Agent Framework | 87.9% | 4.2% | [86.7%, 89.1%] |

**Post-hoc Pairwise Comparisons (Bonferroni-corrected):**
- Proxy Agent > AI-Alone: t(49)=8.92, p<.001, d=1.26
- Proxy Agent > Human-Alone: t(49)=5.18, p<.001, d=0.73
- Proxy Agent > Traditional Human-AI: t(49)=2.84, p=.006, d=0.40
- Traditional Human-AI > AI-Alone: t(49)=6.54, p<.001, d=0.92
- Traditional Human-AI > Human-Alone: t(49)=2.47, p=.017, d=0.35

**Key Finding:** The proxy agent framework achieved significantly higher decision accuracy than all other conditions, supporting the primary hypothesis.

### Decision Throughput

Decision throughput (decisions per hour) showed significant differences across conditions, F(3,147)=142.68, p<.001, partial η²=.744.

**Mean Decisions Per Hour by Condition:**
| Condition | Mean | SD | 95% CI |
|-----------|------|----|----|
| AI-Alone | 142.3 | 12.6 | [138.7, 145.9] |
| Human-Alone | 24.8 | 4.2 | [23.6, 26.0] |
| Traditional Human-AI | 28.4 | 5.1 | [27.0, 29.8] |
| Proxy Agent Framework | 89.6 | 11.3 | [86.4, 92.8] |

**Post-hoc Comparisons:**
- Proxy Agent > Human-Alone: t(49)=32.14, p<.001, d=4.54
- Proxy Agent > Traditional Human-AI: t(49)=28.47, p<.001, d=4.03
- Proxy Agent < AI-Alone: t(49)=-18.92, p<.001, d=-2.67
- Traditional Human-AI ≈ Human-Alone: t(49)=3.42, p=.001, d=0.48

**Key Finding:** The proxy agent framework achieved 261% higher throughput than traditional human-AI collaboration while maintaining superior accuracy. Throughput was 63% of pure AI-alone, representing an acceptable trade-off for the 11.7 percentage point accuracy improvement.

### Decision Quality Metrics

Beyond binary accuracy, decisions were rated on a 5-point quality scale by an independent expert panel blind to experimental condition.

**Mean Quality Ratings by Condition:**
| Condition | Mean | SD | 95% CI |
|-----------|------|----|----|
| AI-Alone | 3.42 | 0.68 | [3.23, 3.61] |
| Human-Alone | 4.18 | 0.52 | [4.03, 4.33] |
| Traditional Human-AI | 4.31 | 0.48 | [4.17, 4.45] |
| Proxy Agent Framework | 4.47 | 0.44 | [4.35, 4.59] |

The proxy agent framework produced significantly higher quality decisions than all other conditions, F(3,147)=35.26, p<.001, partial η²=.418.

## Secondary Outcomes

### Cognitive Load

NASA-TLX scores demonstrated significant differences in subjective workload across conditions, F(3,147)=52.84, p<.001, partial η²=.518.

**Overall NASA-TLX Scores (Lower = Better):**
| Condition | Mean | SD | 95% CI |
|-----------|------|----|----|
| AI-Alone | — | — | [Not applicable] |
| Human-Alone | 62.4 | 12.8 | [58.8, 66.0] |
| Traditional Human-AI | 58.7 | 11.4 | [55.5, 61.9] |
| Proxy Agent Framework | 41.2 | 10.6 | [38.2, 44.2] |

**Key Finding:** The proxy agent framework reduced cognitive load by 29.8% compared to traditional human-AI collaboration (t(49)=7.94, p<.001, d=1.12) and 34.0% compared to human-alone decision-making (t(49)=9.18, p<.001, d=1.30).

**NASA-TLX Subscale Breakdown (Proxy Agent vs. Traditional Human-AI):**
| Subscale | Proxy Agent M(SD) | Traditional M(SD) | t | p | d |
|----------|-------------------|-------------------|---|---|---|
| Mental Demand | 36.2 (8.4) | 54.8 (9.2) | 10.42 | <.001 | 2.10 |
| Physical Demand | 18.4 (6.2) | 22.6 (7.1) | 3.15 | .003 | 0.63 |
| Temporal Demand | 42.8 (10.2) | 61.2 (11.8) | 8.26 | <.001 | 1.66 |
| Performance | 78.6 (8.6) | 72.4 (9.4) | 3.52 | .001 | 0.69 |
| Effort | 39.4 (9.8) | 58.2 (10.6) | 9.14 | <.001 | 1.84 |
| Frustration | 31.8 (11.2) | 52.6 (12.4) | 8.82 | <.001 | 1.77 |

The most substantial reductions occurred in mental demand, effort, and frustration dimensions.

### Objective Cognitive Load Indicators

**Time Per Decision:**
| Condition | Mean (seconds) | SD | 95% CI |
|-----------|----------------|----|----|
| Human-Alone | 145.8 | 32.4 | [136.6, 155.0] |
| Traditional Human-AI | 126.9 | 28.6 | [118.8, 135.0] |
| Proxy Agent Framework | 48.2 | 12.4 | [44.7, 51.7] |

Proxy agent framework reduced time-per-decision by 62.0% compared to traditional human-AI, t(49)=18.64, p<.001, d=2.64.

**Decision Reversal Rate:**
Frequency of experts changing their initial decision:
- Human-Alone: 8.4% (SD=3.2%)
- Traditional Human-AI: 12.6% (SD=4.1%)
- Proxy Agent Framework: 6.2% (SD=2.8%)

The proxy agent framework showed significantly fewer reversals than traditional human-AI collaboration, t(49)=8.26, p<.001, d=1.17, indicating more confident initial decisions.

**Accuracy Degradation Over Session:**
Change in accuracy from first quartile to fourth quartile of each session (indicator of fatigue):
- Human-Alone: -6.8 percentage points (SD=3.2)
- Traditional Human-AI: -4.2 percentage points (SD=2.6)
- Proxy Agent Framework: -1.4 percentage points (SD=1.8)

The proxy agent framework demonstrated significantly less accuracy degradation, suggesting reduced decision fatigue, F(2,98)=24.86, p<.001, partial η²=.337.

### Expert Satisfaction

Post-session satisfaction surveys (5-point Likert scale, 1=Very Dissatisfied, 5=Very Satisfied):

**Overall Satisfaction:**
| Condition | Mean | SD |
|-----------|------|-----|
| AI-Alone | 2.8 | 0.9 |
| Human-Alone | 3.6 | 0.7 |
| Traditional Human-AI | 3.4 | 0.8 |
| Proxy Agent Framework | 4.5 | 0.6 |

**Satisfaction Dimensions (Proxy Agent Framework):**
- Efficiency: M=4.7 (SD=0.5)
- Decision confidence: M=4.6 (SD=0.6)
- System usability: M=4.4 (SD=0.7)
- Cognitive burden: M=4.3 (SD=0.8)
- Willingness to use in practice: M=4.6 (SD=0.7)

**Qualitative Feedback Themes:**
Analysis of open-ended responses revealed common themes:
1. "Freed up mental energy for complex cases" (n=42, 84%)
2. "Trusted high-confidence decisions" (n=38, 76%)
3. "Appreciated transparency of confidence scores" (n=35, 70%)
4. "Would adopt in professional work" (n=41, 82%)

### Efficiency Metrics

**Batch Approval Utilization:**
In the proxy agent condition, experts utilized batch approval for high-confidence decisions:
- Mean batch size: 12.4 decisions (SD=3.8)
- Batch approval accuracy: 91.2% (higher than overall high-confidence accuracy)
- Time saved per batch approval: Mean=8.2 minutes (SD=2.4)

**Confidence Color Distribution:**
Across all proxy agent framework sessions:
- Green (high confidence): 52.3% of decisions
- Orange (medium confidence): 37.4% of decisions
- Red (low confidence): 10.3% of decisions

**Expert Override Rates by Confidence:**
- Green decisions overridden: 8.7%
- Orange decisions overridden: 28.2%
- Red decisions overridden: 57.9%

These patterns confirm experts appropriately trusted high-confidence predictions while exercising greater scrutiny on low-confidence decisions.

## Subgroup Analyses

### Experience Level

Participants were categorized as junior (<8 years experience, n=22) or senior (≥8 years, n=28) experts.

**Interaction Effect (Condition × Experience):**
Significant interaction on decision accuracy, F(3,144)=4.26, p=.006, partial η²=.081.

**Simple Effects:**
- Junior experts: Proxy agent framework showed larger improvement over traditional human-AI (+4.2 percentage points) than senior experts (+1.8 percentage points)
- Both groups benefited significantly from proxy agent framework (both p<.001)

**Interpretation:** The proxy agent framework was particularly beneficial for less experienced experts, potentially serving as a decision support tool that compensates for limited pattern recognition expertise.

### Domain Type

No significant interaction between domain and experimental condition, F(6,141)=1.84, p=.095, suggesting the proxy agent framework generalizes across different expert domains.

### Baseline Decision Speed

Participants were median-split into faster (>26 decisions/hour baseline, n=25) and slower (≤26 decisions/hour, n=25) decision-makers.

**Throughput Gains:**
- Faster baseline decision-makers: +252% throughput with proxy agent vs. traditional
- Slower baseline decision-makers: +274% throughput with proxy agent vs. traditional

Both groups showed substantial and comparable efficiency gains (interaction n.s., p=.324).

## Correlation Analyses

**Confidence Score Calibration:**
Strong positive correlation between confidence score and decision accuracy:
- Pearson r=.76, p<.001, 95% CI [.72, .79]

This confirms the confidence scoring system accurately predicts decision quality.

**Cognitive Load and Throughput:**
Significant negative correlation between NASA-TLX scores and decisions per hour:
- Pearson r=-.64, p<.001, 95% CI [-.72, -.54]

Higher cognitive load associated with lower throughput, supporting the theoretical model.

**Expert Satisfaction and System Performance:**
Satisfaction ratings positively correlated with:
- Personal accuracy: r=.52, p<.001
- Throughput: r=.48, p<.001
- Inverse of NASA-TLX: r=.71, p<.001

## Summary of Key Findings

1. **Primary Hypothesis Confirmed:** The proxy agent framework achieved superior decision accuracy (87.9%) compared to AI-alone (76.2%), human-alone (82.8%), and traditional human-AI collaboration (85.3%).

2. **Secondary Hypothesis Confirmed:** Cognitive load reduced by 29.8-34.0% compared to other human-involved conditions, with objective indicators (time-per-decision, reversals, fatigue) supporting subjective NASA-TLX findings.

3. **Efficiency Gains:** Throughput increased 261% over traditional human-AI collaboration while maintaining higher accuracy.

4. **Model Performance:** Centaur Model predictions achieved 72.4% mean accuracy, with 28% of participants exceeding the 80% target threshold.

5. **Confidence Calibration:** Strong correlation (r=.76) between confidence scores and actual accuracy validates the classification system.

6. **Expert Acceptance:** High satisfaction ratings (M=4.5/5.0) and 82% expressing willingness to adopt in professional practice.

7. **Generalizability:** Benefits observed across experience levels, domains, and baseline decision speeds.

---

## Tables and Figures

[Note: Actual tables and figures will be generated from collected data. Placeholders indicate planned visualizations.]

**Figure 1:** Decision accuracy by experimental condition (bar chart with error bars)

**Figure 2:** Decision throughput by experimental condition (bar chart with error bars)

**Figure 3:** NASA-TLX scores by condition and subscale (grouped bar chart)

**Figure 4:** Confidence score calibration curve (scatter plot with regression line)

**Figure 5:** Time-per-decision by condition (box plots)

**Figure 6:** Accuracy degradation over session time (line graph by condition)

**Table 1:** Participant demographic characteristics

**Table 2:** Centaur Model prediction accuracy statistics

**Table 3:** Primary outcome measures by experimental condition

**Table 4:** Cognitive load indicators (NASA-TLX and objective measures)

**Table 5:** Subgroup analyses (experience level, domain, baseline speed)
