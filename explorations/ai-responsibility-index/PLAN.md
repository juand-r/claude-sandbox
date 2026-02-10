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
- [x] 4. `scorer.py` -- Multi-provider LLM scoring (Anthropic + OpenAI), auto-detect from model name
- [x] 5. `pipeline.py` -- tie it together: ingest docs, build store, score all indicators, aggregate
- [x] 6. `run.py` -- CLI: point at a PDF/XML, get a scored report

## Phase 2.5: Testing on Real Documents
- [x] Download real corporate RAI reports (CSIRO framework, OpenAI system card, Anthropic model card)
- [x] Test ingestion and chunking on real PDFs (all pass)
- [x] Test retrieval quality per indicator (CSIRO: 0.65+ scores, all 10 indicators retrieve)
- [x] End-to-end pipeline test with mock LLM on real PDFs
- [ ] **BLOCKED**: Live LLM scoring -- no API keys in environment. Need ANTHROPIC_API_KEY or OPENAI_API_KEY.

### Known Issues
- **References section pollution**: OpenAI system card's References section acts as a keyword honeypot, dominating retrieval results (4/5 top results for gov_04). Need to filter out reference/bibliography sections during ingestion.
- **Anthropic model card section detection**: Only 1 section detected (font size threshold issue for this PDF's formatting).

## Phase 3: Validation & Iteration
- [ ] Run live LLM scoring on real documents (requires API keys)
- [ ] Manual review of scores for accuracy
- [ ] Fix References section filtering in ingestion
- [ ] Iterate on prompts and retrieval based on live results
- [ ] Add deep dive indicators (42 questions) if governance indicators work well

## Open Questions (resolved)
1. Start with governance indicators (10) -- simpler, more binary, more reliably extractable
2. RAG: yes, simplified (one embedding model, one FAISS index). Justified by lost-in-the-middle, citability, cost.
3. LLM: Claude via Anthropic API initially, now supports OpenAI too (auto-detect from model name)
