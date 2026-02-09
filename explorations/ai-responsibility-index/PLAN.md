# AI Responsibility Index: Project Plan

## Phase 1: Indicator Framework
- [x] Literature review and synthesis (PAPERS.md)
- [x] Architecture design (ARCHITECTURE.md)
- [ ] Define indicator schema adapted from CSIRO framework
- [ ] Create metadata module (ESGReveal-style) for each indicator

## Phase 2: Implementation

### Project structure
```
explorations/ai-responsibility-index/
├── src/
│   ├── __init__.py
│   ├── indicators.py      # RAI indicator metadata (what to look for + how)
│   ├── ingest.py           # PDF + XML ingestion → text chunks with metadata
│   ├── store.py            # Embedding + FAISS vector store + retrieval
│   ├── scorer.py           # LLM-based scoring per indicator
│   └── pipeline.py         # Orchestrator: ingest → store → retrieve → score → aggregate
├── requirements.txt
├── run.py                  # CLI entry point
├── README.md
├── PAPERS.md
├── ARCHITECTURE.md
└── PLAN.md
```

### Implementation order
- [x] 1. `indicators.py` -- 10 governance indicators + metadata (search terms, knowledge, rubric)
- [x] 2. `ingest.py` -- PDF (PyMuPDF) and XML (lxml) parsers → list of text chunks with page/section metadata
- [x] 3. `store.py` -- sentence-transformers embedding, FAISS index, top-k retrieval
- [x] 4. `scorer.py` -- Anthropic Claude API, structured prompt per indicator, output parsing
- [x] 5. `pipeline.py` -- tie it together: ingest docs, build store, score all indicators, aggregate
- [x] 6. `run.py` -- CLI: point at a PDF/XML, get a scored report

## Phase 3: Validation & Iteration
- [ ] Test on real corporate AI/sustainability reports
- [ ] Manual review of scores for accuracy
- [ ] Iterate on prompts and retrieval
- [ ] Add deep dive indicators (42 questions) if governance indicators work well

## Open Questions (resolved)
1. Start with governance indicators (10) -- simpler, more binary, more reliably extractable
2. RAG: yes, simplified (one embedding model, one FAISS index). Justified by lost-in-the-middle, citability, cost.
3. LLM: Claude via Anthropic API (configurable)
