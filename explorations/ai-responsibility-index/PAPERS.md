# Literature Synthesis: AI Responsibility Index

## Paper 1: CSIRO/Alphinity RAI-ESG Framework for Investors (2024)

**Source:** CSIRO Data61 + Alphinity Investment Management
**Type:** Open-source investor toolkit (Creative Commons BY-SA 4.0)
**Based on:** 28 company interviews, 25 desktop analyses, 12-month collaboration (Feb 2023 - Mar 2024)

### What It Does

Provides a 3-step framework for investors to assess responsible AI practices at companies, grounded in Australia's 8 AI Ethics Principles and aligned with ESG investing.

### The Three Steps

#### Step 1: AI Use Case Analysis (Materiality Screening)

Identifies 27 material AI use cases across 9 industry sectors and scores them on:

- **Regulatory risk** (mapped to EU AI Act categories):
  - Unacceptable (prohibited: social scoring, manipulation of vulnerable groups)
  - High (biometrics, critical infrastructure, credit scoring, resume-scanning)
  - Medium (human-interaction systems)
  - Low (video games, spam filters)
  - Not determined

- **Environmental & Social Impact** across 9 ESG topics:
  - Environmental: GHG emissions, resource efficiency, ecosystem impact
  - Social: DEI, human rights, labor management, customer/community, data privacy/cybersecurity, health/safety
  - Scoring: High (>=8 topics impacted), Medium (3 < N <= 7), Low (<= 3)

- **Impact Scope**: Industry-level disruption vs. systemic economic risk

- **Materiality formula**: F = w1*R + w2*I + w3*S (equal weights)
  - Output: High / Medium / Low materiality per use case

#### Step 2: RAI Governance Indicators (10 indicators, 4 categories)

Scores companies 0-10 on governance maturity:

| Category | # | Indicator | What It Assesses |
|----------|---|-----------|-----------------|
| Board Oversight | 1 | Board Accountability | RAI assigned to Board/subcommittee, annual reporting |
| | 2 | Board Capability | >= 1 Director with AI/tech experience |
| RAI Commitment | 3 | Public RAI Policy | Published framework aligned with standards (ISO 42001, etc.) |
| | 4 | Sensitive Use Cases | High-risk applications explicitly addressed |
| | 5 | RAI Target | Clear measurable objectives (training %, incident reduction %) |
| RAI Implementation | 6 | Dedicated RAI Responsibility | Named AI Officer or equivalent |
| | 7 | Employee Awareness | Formal AI ethics + ESG training program |
| | 8 | System Integration | RAI embedded in risk mgmt, product dev, procurement, ESG |
| | 9 | AI Incidents Management | Internal tracking + external reporting |
| RAI Metrics | 10 | RAI Metrics Disclosure | Externally reported metrics tied to policy |

**Scoring**: F = sum(wg * Gi), each indicator equally weighted
- Weak: 0-3, Moderate: 4-7, Strong: 8-10

#### Step 3: RAI Deep Dive Assessment

42 questions across 8 AI Ethics Principles, with 27 specific indicators and 43 guide metrics.

**The 8 Principles:**
1. Human, Societal & Environmental Wellbeing
2. Human-Centred Values
3. Fairness
4. Privacy & Security
5. Reliability & Safety
6. Transparency & Explainability
7. Contestability
8. Accountability

**Scoring (6-point Likert):**
- 0 = Not-disclosed (no evidence)
- 1 = Minimal (insufficient info)
- 2-4 = Moderate (reasonably detailed)
- 5 = Comprehensive (exemplary)

**Final Decision Levels:**
- Strong: Average >= 4.5
- Moderate: 3 <= Average < 4.5
- Weak: 1.5 <= Average < 3
- Unacceptable: Average < 1.5

**6 Mandatory Metrics for High-Risk AI / Foundation Models:**
1. Energy usage
2. GHG emissions
3. Tonnes of waste generated/saved
4. AI system performance (accuracy, precision, recall, F-score)
5. Size of AI model (foundation models)
6. Time to model training (foundation models)

**Customization dimensions:**
- By organizational type: AI Developer, AI Purchaser, or Both
- By AI system category: high-risk, low-risk, foundation models
- By ESG topics (12 standardized aspects)

### ESG-to-AI Ethics Mapping

The framework maps each of the 8 AI ethics principles to the 12 ESG topics:
- Accountability is strongest on Governance topics (4-5 connections)
- Transparency & Explainability is strongest on Social topics (6 connections)
- Privacy & Security: 4 social connections
- Environmental topics primarily connect to Human/Societal/Environmental Wellbeing and Accountability

### Key Findings

- Only 10% of companies publicly disclose RAI policies (40% have internal ones)
- 62% implementing or planning AI strategies
- Data privacy is the most cited concern; human rights is underexplored
- Strong ESG track record is a reasonable proxy for responsible AI management
- Global companies significantly ahead of Australian peers

### Regulatory Alignment

- 67% of deep dive questions align with EU AI Act and/or NIST AI RMF
- 29% address both EU + NIST, 24% EU-only, 14% NIST-only

---

## Paper 2: "Integrating ESG and AI: A Comprehensive Responsible AI Assessment Framework" (Springer, 2025)

**Source:** AI and Ethics (Springer Nature), DOI: 10.1007/s43681-025-00741-5
**Published:** June 2025

This is the peer-reviewed academic version of Paper 1. The content is essentially the same framework with more rigorous presentation. Key additions/clarifications vs. the CSIRO report:

- Formal materiality calculation with explicit formula notation
- More detailed scoring rubrics for the 6-point Likert scale
- Explicit table mapping RAI principles to ESG topics with connection counts
- Six design drivers identified:
  1. Employee engagement essential for AI success
  2. Board capability strengthening critical
  3. RAI governance should be embedded in existing systems (not a parallel structure)
  4. Balance threats and opportunities
  5. Supply chain management is often overlooked
  6. Data privacy is prioritized but other issues underexplored

The framework and scoring are identical to Paper 1.

---

## Paper 3: ESGReveal (Zou et al., 2024/2025)

**Source:** Journal of Cleaner Production (ScienceDirect). arXiv: 2312.17264
**What it is:** An LLM-based system for extracting structured ESG data from unstructured corporate reports
**Evaluated on:** 166 companies listed on Hong Kong Stock Exchange (2022 reports)

### Why It Matters For Us

This paper shows how to *implement* automated extraction of structured indicators from unstructured corporate documents. While it targets ESG broadly, the architecture is directly applicable to extracting RAI-specific indicators.

### Architecture: Three Modules

#### Module 1: ESG Metadata

Defines the structured schema for what to extract. Data organized as:

```
<Aspect, KPI, Topic, Quantity>
```

**70 indicators total:**
- 12 environmental numeric
- 18 social numeric
- 4 governance numeric
- 36 textual indicators across all categories

Each indicator is extended with:
- `<Knowledge>`: Domain expertise from ESG specialists, embedded via in-context learning
- `<SearchTerm>`: Customized retrieval keywords derived from ESG report analysis (improves RAG recall)
- `<Expressions>`: Prompt templates and output format specs for automatic prompt generation

**This is the key design insight:** the metadata module effectively encodes both *what to look for* and *how to look for it*, making the system adaptable to different indicator frameworks.

#### Module 2: Report Preprocessing

Converts unstructured PDF reports into a searchable knowledge base:

1. **Layout extraction:** LayoutLMv3 and GeoLayoutLM extract structural components (headers, paragraphs, tables)
2. **Document outline:** Font characteristic analysis constructs a hierarchical outline linking structure to content
3. **Table extraction:** Table-Transformer and LORE-TSR identify and reconstruct table structures
4. **Knowledge base construction** (three parallel vector stores):
   - Textual content: Summarized via mt5, vectorized with m3e, stored in FAISS/Milvus
   - Document outlines: Same vectorization pipeline
   - Table content: One-to-many mapping highlighting ESG indicator names, vectorized separately

#### Module 3: LLM Agent

Performs the actual extraction:

1. **Knowledge retrieval:** Query vectors from metadata are matched against the knowledge base via cosine similarity. coROM model refines semantic ordering of top matches.

2. **Prompt construction** from 5 elements:
   - Preset Information (behavioral instructions)
   - Reference Content (retrieved knowledge base entries)
   - Expert Knowledge (ESG domain insights)
   - Question (targeted indicator query)
   - Answer Format specification

3. **Output structure:** `<Disclosure, KPI, Topic, Value, Unit, Target, Action>`

### Evaluation Metrics

- **AccDC (Disclosure Coverage Accuracy):** Ratio of correctly identified disclosure indicators to actually disclosed indicators
- **AccDE (Data Extraction Accuracy):** Ratio of correctly extracted numeric values to true numeric values

### Performance Results

| Model | AccDC | AccDE |
|-------|-------|-------|
| GPT-4 | 83.7% | 76.9% |
| QWEN | 61.4% | 54.9% |
| GPT-3.5 | 51.9% | 47.1% |
| ChatGLM | 53.9% | 46.2% |

**Ablation study:**
- Enhanced RAG improved GPT-4 by +23.4% (disclosure) and +21.8% (extraction) vs. baseline
- Adding ESG expert knowledge: +2.5% GPT-4, +9.9% GPT-3.5

### Key Findings

- Environmental disclosure averaged 69.5%, social 57.2% -- neither exceeding 80% in any industry
- Industry-specific ESG patterns: telecom emphasizes renewable energy, healthcare focuses on digital medical services, financials lead green finance
- GPT-4 with enhanced RAG + domain knowledge is sufficient for reliable extraction
- Zero-shot approach works (no fine-tuning needed), but domain knowledge in prompts matters significantly

---

## Synthesis: What We Can Build

### The Architecture

The three papers together suggest a clear architecture for an AI Responsibility Index:

```
[Indicator Framework]  -->  [Document Processing]  -->  [LLM Extraction]  -->  [Scoring]
   (Papers 1 & 2)            (Paper 3)                  (Paper 3)           (Papers 1 & 2)
```

**From Papers 1 & 2 (CSIRO/Alphinity), we take:**
- The indicator taxonomy: 10 governance indicators, 8 ethics principles, 42 deep dive questions
- The scoring methodology: 0-5 Likert scale, weighted aggregation, final decision levels
- The materiality framework: regulatory risk * impact * scope
- The ESG-to-AI-ethics mapping

**From Paper 3 (ESGReveal), we take:**
- The metadata module pattern: define `<Aspect, KPI, Topic, Quantity>` + `<Knowledge>` + `<SearchTerm>` for each RAI indicator
- The RAG-based extraction pipeline: PDF -> structured knowledge base -> vector retrieval -> LLM extraction
- The evaluation approach: disclosure coverage + extraction accuracy
- The prompt engineering pattern: preset + reference + expert knowledge + question + format

### Key Design Decisions to Make

1. **Indicator scope:** Do we use the full CSIRO 42-question deep dive, or start with the 10 governance indicators?
2. **Data sources:** Corporate ESG/sustainability reports? AI-specific disclosures? 10-K filings? All of the above?
3. **LLM choice:** GPT-4 showed best results in ESGReveal. Claude could be a strong alternative. Cost vs. accuracy tradeoff.
4. **Document processing:** ESGReveal's full pipeline (LayoutLM, table extraction, etc.) is heavy. For an MVP we could use simpler PDF-to-text + chunking.
5. **Scoring granularity:** Company-level index? Principle-level scores? Both?
6. **Validation:** How do we validate the automated scores? Manual review sample? Inter-annotator agreement?

### What's Novel

Existing work (CSIRO) defines the *what* but not the *how* of automated assessment. ESGReveal shows the *how* but for generic ESG, not AI-specific indicators. Combining them -- an LLM-based system that automatically extracts and scores AI responsibility indicators from corporate disclosures -- is the gap we can fill.
