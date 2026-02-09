# AI Responsibility Index: Project Plan

## Phase 1: Indicator Framework (Current)

- [x] Literature review: CSIRO RAI-ESG Framework
- [x] Literature review: Springer peer-reviewed version
- [x] Literature review: ESGReveal implementation
- [x] Synthesis of papers (PAPERS.md)
- [ ] Define indicator schema adapted from CSIRO framework
- [ ] Create metadata module (ESGReveal-style) for each indicator

## Phase 2: Data Pipeline (MVP)

- [ ] PDF ingestion and chunking (start simple: PyMuPDF + text splitting)
- [ ] Vector store setup (FAISS or similar)
- [ ] RAG retrieval for indicator-relevant passages
- [ ] LLM extraction prompts per indicator
- [ ] Output: structured `<Disclosure, Value, Evidence, Score>` per indicator

## Phase 3: Scoring Engine

- [ ] Implement governance scoring (10 indicators, 0-10 scale)
- [ ] Implement deep dive scoring (42 questions, 0-5 Likert)
- [ ] Aggregation to principle-level and overall scores
- [ ] Final decision level classification (Strong/Moderate/Weak/Unacceptable)

## Phase 4: Validation & Evaluation

- [ ] Manual annotation of a small sample
- [ ] Compute AccDC and AccDE metrics (ESGReveal-style)
- [ ] Compare automated scores vs. manual scores
- [ ] Iterate on prompts and retrieval

## Phase 5: Index Construction

- [ ] Run across a set of companies
- [ ] Normalize and rank
- [ ] Visualize results

## Open Questions

1. Start with governance indicators (10) or full deep dive (42 questions)?
   - Recommendation: Start with governance indicators. They're simpler, more binary, and more reliably extractable.
2. Which companies to target first?
   - Options: Big tech (FAANG+), major AI companies, ASX-listed (CSIRO's original set)
3. Where do we get reports?
   - Corporate sustainability reports (usually PDFs on company websites)
   - SEC 10-K filings (for US companies)
   - AI-specific disclosures (e.g., Google's AI Principles report, Microsoft's RAI report)
4. What LLM to use?
   - Claude for extraction (strong at document analysis)
   - Evaluate cost/accuracy tradeoff
5. How to handle companies that don't publish AI-specific disclosures?
   - Score as "not disclosed" (0 on Likert scale) -- this is valid and informative
