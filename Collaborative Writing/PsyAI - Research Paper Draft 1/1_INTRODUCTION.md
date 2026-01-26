# Introduction

## Background and Significance

The integration of artificial intelligence into expert decision-making workflows has accelerated rapidly across industries, yet 95% of AI adoption efforts fail to generate meaningful business impact (Machine Learning Quarterly, 2025). This paradox stems not from limitations in AI capabilities, but from inadequate frameworks for human-AI collaboration. Current approaches often impose significant cognitive burdens on experts who must constantly evaluate and validate AI-generated recommendations, leading to decision fatigue and reduced effectiveness (Benda et al., 2019).

Human-in-the-loop (HITL) systems represent a critical paradigm for responsible AI deployment, particularly in high-stakes domains requiring expert judgment. However, existing HITL frameworks struggle with a fundamental tension: they demand continuous human oversight while simultaneously overwhelming experts with validation tasks. This challenge is particularly acute in agentic AI workflows, where autonomous agents generate numerous decisions requiring expert review. The cognitive load imposed by reviewing every AI decision creates a bottleneck that negates many efficiency gains promised by automation.

Recent advances in foundation models for human cognition, particularly the Centaur Model developed at the Institute for Human-Centered AI at Helmholtz Munich (Binz et al., 2024), offer a novel approach to this challenge. The Centaur Model demonstrates that large language models trained on psychological data can predict human decision patterns with notable accuracy. This capability suggests an underexplored opportunity: if AI systems can reliably predict which decisions align with expert judgment, they could pre-classify decisions by confidence, enabling experts to focus their limited cognitive resources on genuinely ambiguous cases.

## Current State of Knowledge

### Limitations of AI in Simulating Human Psychology

Existing research reveals significant gaps in LLMs' ability to replicate human psychological processes and decision-making patterns. Thorstad (2024) demonstrated that while LLMs can approximate some aspects of human cognition, they exhibit systematic deviations from human decision patterns, particularly in complex reasoning tasks requiring intuitive judgment. Similarly, studies on synthetic participant models show that current AI systems struggle to capture the nuanced, context-dependent nature of human expert decisions (Chen et al., 2024).

### Human-AI Collaborative Decision-Making

The literature on human-AI decision-making reveals mixed results regarding collaborative effectiveness. Some studies demonstrate improved outcomes when humans and AI work together (Lai et al., 2021), while others show that poor integration can lead to automation bias, over-reliance on AI, or complete disengagement (Cabrera et al., 2019). A critical finding is that the effectiveness of human-AI collaboration depends heavily on how information is presented and how cognitive load is managed during the decision process.

### Research Gap

Despite extensive research on human-AI collaboration and recent advances in modeling human cognition, limited work has explored predictive frameworks that anticipate expert decisions in real-time agentic workflows. Existing HITL systems typically operate reactively, presenting decisions for review after they occur. This reactive approach fails to leverage predictive capabilities that could optimize the allocation of human attention and expertise.

## Research Hypotheses

### Primary Hypothesis

If a large language model trained on psychology data can predict human expert decisions with greater than 80% accuracy, then experts using a proxy agent framework will make better decisions faster compared to AI-alone, human-alone, or traditional human-AI collaborative approaches.

**Rationale:** High-accuracy prediction enables confident pre-classification of decisions, allowing experts to allocate cognitive resources efficiently. Decisions predicted with high confidence can be batch-processed or auto-approved, while low-confidence predictions receive focused expert attention.

### Secondary Hypothesis

Expert users experiencing repetitive LLM training and decision-making workflows will demonstrate measurable reductions in decision fatigue and cognitive load when using a predictive decision framework compared to traditional review approaches.

**Rationale:** By filtering decisions through confidence-based classification, experts avoid the cognitive burden of reviewing routine decisions that align with their established patterns, preserving mental resources for complex cases requiring deep expertise.

## Research Objectives

This study aims to:

1. **Develop and validate a proxy agent framework** that predicts expert decision-making in agentic AI applications using the Centaur Model as a foundation for modeling human cognition.

2. **Measure the effectiveness** of AI-predicted decisions across four experimental conditions:
   - AI-alone decision-making
   - Human-alone decision-making
   - Traditional human-AI collaboration (all decisions reviewed)
   - Proxy agent framework (confidence-based review prioritization)

3. **Establish a measurement framework** for evaluating the quality and efficiency of AI-predicted decisions, including metrics for:
   - Decision accuracy and consistency
   - Expert satisfaction and confidence
   - Conversation quality in agentic workflows
   - Business outcome metrics

4. **Evaluate the impact** on three critical dimensions:
   - **Decision-making speed:** Time required to complete decision workflows
   - **Decision quality:** Accuracy and consistency of final decisions
   - **Cognitive load reduction:** Measured through task completion time, decision reversals, and validated cognitive load instruments (e.g., NASA-TLX)

## Significance and Expected Contributions

This research addresses a critical gap in human-AI collaboration by introducing a predictive, rather than reactive, framework for expert engagement. The expected contributions include:

**Theoretical Contributions:**
- Demonstration that LLM-based human decision models can be operationalized for real-time workflow optimization
- Framework for reducing the "black-box" effect in LLMs through alignment with human decision patterns
- Evidence for cognitive load reduction through intelligent task filtering in HITL systems

**Practical Contributions:**
- Implementable framework for improving expert efficiency in AI-assisted workflows
- Methodology for measuring and optimizing human-AI collaboration effectiveness
- Open-source reference implementation for researchers and practitioners

**Broader Impact:**
- Potential to transform how human-AI collaboration is structured across professional domains
- Advancement of responsible AI deployment through improved human oversight mechanisms
- Foundation for future research on adaptive, human-centered AI systems

The ultimate goal is to demonstrate that predictive decision frameworks can fundamentally improve how experts interact with agentic AI systems, reducing cognitive burden while maintaining or improving decision quality. Success would establish a new paradigm for HITL systems that prioritizes efficient use of human expertise rather than exhaustive review.

---

## References

Benda, N. C., Veinot, T. C., Sieck, C. J., & Ancker, J. S. (2019). Broadband Internet Access Is a Social Determinant of Health! *Journal of the American Medical Informatics Association*, 26(10), 1141-1142.

Binz, M., Alaniz, S., Risi, K., Buffart, D., Nakajima, S., Schulz, E., & Wichmann, F. A. (2024). Centaur: A Foundation Model for Human Cognition. *arXiv preprint arXiv:2410.20268*.

Cabrera, Á. A., Epperson, W., Hohman, F., Kahng, M., Morgenstern, J., & Chau, D. H. (2019). FairVis: Visual Analytics for Discovering Intersectional Bias in Machine Learning. *IEEE Conference on Visual Analytics Science and Technology (VAST)*.

Chen, Y., et al. (2024). Limitations of Synthetic Participant Models in Replicating Human Decision Patterns. *arXiv preprint arXiv:2508.07887*.

Lai, V., Chen, C., Liao, Q. V., Smith-Renner, A., & Tan, C. (2021). Towards a Science of Human-AI Decision Making: A Survey of Empirical Studies. *arXiv preprint arXiv:2112.11471*.

Machine Learning Quarterly. (2025). State of AI in Business 2025 Report. *MLQ Media*.

Thorstad, R. (2024). Limitations of Large Language Models in Simulating Human Psychology. *arXiv preprint arXiv:2508.06950*.
