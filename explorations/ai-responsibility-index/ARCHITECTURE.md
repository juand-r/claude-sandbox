# Architecture Notes

## ESGReveal Pipeline: What to Keep, Simplify, or Drop

### Context

ESGReveal (late 2023) was built for a world of 8k-32k context windows where LLMs
couldn't read PDFs. Many of its components addressed limitations that no longer exist.
However, the core RAG pattern remains valuable -- see "Why RAG still matters" below.

### Component-by-component assessment

| Component | ESGReveal | Our approach | Rationale |
|-----------|-----------|--------------|-----------|
| Indicator metadata | `<Aspect, KPI, Topic, Quantity>` + `<Knowledge>` + `<SearchTerm>` + `<Expressions>` | **KEEP as-is** | Core design insight. Defines what to look for AND how to find it. Adapt for RAI indicators. |
| PDF layout extraction | LayoutLMv3 + GeoLayoutLM | **DROP** | LLMs now read PDFs natively. Modern PDF parsers (PyMuPDF, marker, docling) handle text+layout. |
| Table extraction | Table-Transformer + LORE-TSR | **DROP** | Same reason. Modern LLMs and PDF parsers handle tables. |
| Text summarization | mt5 | **DROP** | Was a compression trick for small embedding windows. Not needed with modern embeddings and large context. |
| Embeddings | m3e (Chinese-focused) | **REPLACE** | Use a standard English embedding model (OpenAI text-embedding-3, or open-source like e5/bge). |
| Vector store | 3 parallel stores (text, outlines, tables) in FAISS/Milvus | **SIMPLIFY** | One vector store, one index. Chunk by section/page with metadata tags. |
| Reranking | coROM | **OPTIONAL** | Nice-to-have for precision. Could use Cohere rerank or cross-encoder. Not critical for MVP. |
| LLM extraction | GPT-4 with 5-element prompt | **KEEP pattern, update model** | Use Claude or GPT-4o. The 5-element prompt structure (preset + reference + expert knowledge + question + format) is solid. |
| Output schema | `<Disclosure, KPI, Topic, Value, Unit, Target, Action>` | **ADAPT** | Modify for RAI: `<Disclosure, Indicator, Principle, Evidence, Score, Justification>` |

### Why RAG still matters

Initial instinct was to skip RAG and feed full documents to LLM. This was wrong, or at
least oversimplified. RAG earns its place for three reasons:

1. **Lost-in-the-middle problem.** LLMs perform worse on information buried in the
   middle of long contexts. RAI-relevant disclosures are often a single sentence on
   page 47 of a 90-page report. RAG surfaces the needle instead of hoping the LLM
   finds it in the haystack.

2. **Citability.** We don't just want a score -- we want to point to WHERE the evidence
   came from. RAG gives us the retrieved passages, so we can show "scored 3/5 on
   Board Accountability based on text from page 12, paragraph 3." Full-document
   passes give you answers without reliable citations.

3. **Cost at scale.** 42 indicators x 100 companies = 4,200 queries. Targeted retrieval
   of ~2-4k tokens per query is much cheaper than 4,200 full-document passes at
   50-100k tokens each.

### Simplified RAG architecture

```
PDF  -->  Parser  -->  Chunks (by section/page)  -->  Embedding  -->  Vector Store
                           |                                              |
                           +-- metadata: page, section title,             |
                               document name, company                     |
                                                                          |
For each indicator:                                                       |
  SearchTerms from metadata  -->  Query embedding  -->  Top-k retrieval --+
                                                              |
                                                              v
                                              Retrieved passages (with citations)
                                                              |
                                                              v
                                              LLM(passages + indicator def + rubric)
                                                              |
                                                              v
                                              {score, evidence, justification, page_ref}
```

One PDF parser. One embedding model. One vector store. One LLM.

### Hybrid fallback strategy

If RAG retrieval returns low-confidence results (low similarity scores, or the LLM
reports insufficient evidence), fall back to a broader context window pass. This handles
cases where the relevant content is described in unexpected terms that the search
terms don't capture.

### The real pipeline

```
┌─────────────────┐     ┌──────────────┐     ┌──────────┐     ┌──────────────┐     ┌───────────┐
│  RAI Indicator   │     │  PDF Parse   │     │  RAG     │     │  LLM Query   │     │ Aggregate │
│  Metadata        │     │  + Chunk     │     │  Retrieval│     │  + Score     │     │ + Classify│
│  (CSIRO-derived) │     │  + Embed     │     │          │     │              │     │           │
└────────┬────────┘     └──────┬───────┘     └────┬─────┘     └──────┬───────┘     └─────┬─────┘
         │                     │                   │                   │                   │
    What to look for     Build searchable     Find relevant      Extract + judge      Weighted avg
    + how to find it     knowledge base       passages           with rubric          → final score
    + domain knowledge                        per indicator      per indicator        per principle
                                                                 {score, evidence}    → decision level
```
