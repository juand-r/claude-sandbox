# AI Responsibility Index

Automated scoring of corporate AI responsibility from sustainability reports and ESG filings.

## What It Does

Takes a corporate report (PDF or XML/XBRL) and scores it against 10 RAI governance indicators derived from the CSIRO/Alphinity RAI-ESG Framework. Uses RAG retrieval + LLM scoring to extract evidence and assign 0-5 scores per indicator, then aggregates to an overall assessment (Strong/Moderate/Weak/Unacceptable).

## Usage

```bash
# Score a PDF report
python run.py report.pdf

# Score an XML/XBRL filing
python run.py filing.xml

# With options
python run.py report.pdf --output results.json --model claude-sonnet-4-5-20250929 --top-k 8 -v
```

Requires `ANTHROPIC_API_KEY` environment variable (or `--api-key` flag).

## Install

```bash
pip install -r requirements.txt
```

## Architecture

```
PDF/XML  →  Chunk + Embed  →  RAG Retrieve per indicator  →  LLM Score  →  Aggregate
```

1. **Indicator Metadata** (`src/indicators.py`): 10 governance indicators with search terms, domain knowledge, rubrics, and prompt templates
2. **Document Ingestion** (`src/ingest.py`): PDF (PyMuPDF) and XML/XBRL (lxml) parsing into text chunks with page/section metadata
3. **Vector Store** (`src/store.py`): sentence-transformers embedding + FAISS index for retrieval
4. **LLM Scorer** (`src/scorer.py`): Claude API with structured prompts, outputs `{score, evidence, justification, disclosed}`
5. **Pipeline** (`src/pipeline.py`): Orchestration and aggregation into category/overall scores

## The 10 Governance Indicators

| Category | Indicator | What It Assesses |
|----------|-----------|-----------------|
| Board Oversight | Board Accountability | AI explicitly in board/committee mandate |
| Board Oversight | Board Capability | Directors with AI/tech experience |
| RAI Commitment | Public RAI Policy | Published RAI framework aligned with standards |
| RAI Commitment | Sensitive Use Cases | High-risk AI applications addressed |
| RAI Commitment | RAI Target | Measurable AI responsibility objectives |
| RAI Implementation | Dedicated RAI Responsibility | Named AI officer or team |
| RAI Implementation | Employee Awareness | Formal RAI training programs |
| RAI Implementation | System Integration | RAI embedded in risk/product/procurement |
| RAI Implementation | AI Incidents Management | Incident tracking and reporting |
| RAI Metrics | RAI Metrics Disclosure | Externally reported RAI metrics |

## Key References

- CSIRO/Alphinity RAI-ESG Framework (2024) - indicator taxonomy and scoring methodology
- "Integrating ESG and AI" (Springer, 2025) - peer-reviewed version
- ESGReveal (Zou et al., 2024) - LLM+RAG extraction pipeline design

See `PAPERS.md` for detailed synthesis and `ARCHITECTURE.md` for design decisions.
