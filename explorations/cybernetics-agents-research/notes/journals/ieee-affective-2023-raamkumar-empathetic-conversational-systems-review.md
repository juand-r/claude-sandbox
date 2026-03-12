# Sesagiri Raamkumar & Yang (2023) — Empathetic Conversational Systems: A Review of Current Advances, Gaps, and Opportunities

**Journal:** IEEE Transactions on Affective Computing, Vol. 14, pp. 2722–2739, 2023
**Authors:** Aravind Sesagiri Raamkumar, Yinping Yang
**DOI:** 10.1109/TAFFC.2022.3226693 (estimated from IEEE Xplore ID 9970384)
**IEEE Xplore:** https://ieeexplore.ieee.org/document/9970384/
**arXiv:** https://arxiv.org/abs/2206.05017 (open access)

## Access Status
- FULL TEXT AVAILABLE via arXiv (CC BY-SA 4.0)
- 20 pages, 3 figures, 4 tables

## Abstract / Summary

Comprehensive review of **empathetic conversational systems (ECS)** — systems that incorporate empathy into conversational AI. Examines the field across five review dimensions:
1. Conceptual empathy models and frameworks
2. Adopted empathy-related concepts
3. Datasets and algorithmic techniques
4. Evaluation strategies
5. State-of-the-art approaches

## Key Findings

- Most studies center on the **EMPATHETICDIALOGUES dataset** and text-based modality dominates
- Studies mainly focus on extracting features from messages, with **minimal emphasis on user modeling and profiling**
- Studies incorporating **emotion causes, external knowledge, and affect matching** in response generation achieved significantly better results
- Three types of dialogue systems surveyed: affective, personalized, knowledge-based

## Identified Gaps

1. **Entity-level emotion detection**: Need to detect and authenticate emotions at the individual level
2. **Multimodal input handling**: Most systems are text-only; need speech, facial expression, physiological signals
3. **Nuanced empathetic behaviors**: Current systems produce coarse empathetic responses
4. **User modeling**: Need to build models of individual users over time

## Conceptual Framework for Empathy in CAs

Ab Aziz et al. proposed a model with five modules:
1. Sensing
2. Emotion analysis / personality / event evaluation
3. Empathy analytics and behavior selection
4. Stress analytics and support
5. Feedback

## Relevance to Cybernetics-Agents Research

This review paper maps the landscape of empathetic agents:
- **Sensing → Processing → Response → Feedback**: The five-module conceptual model IS a cybernetic control loop for social-emotional regulation
- **Gap in user modeling**: From a cybernetic perspective, the system needs an internal model of the user (a "model of the environment" in Conant-Ashby terms) to regulate effectively
- **Multimodal gap**: True empathetic regulation requires multiple channels — analogous to how biological interoception integrates multiple sensory modalities
- **Affect matching**: The idea that response generation should "match" user affect is a form of requisite variety (Ashby) — the system needs enough emotional variety to respond to the variety of user states

## Connections
- Hu et al. (2023) — specific implementation of emotion-aware CA
- Aylett et al. (2021) — emotional expressions as social signals
- McKeown et al. (2012) — SEMAINE as foundational dataset for affective agents
