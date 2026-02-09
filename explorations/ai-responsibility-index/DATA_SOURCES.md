# RAI Data Sources: Where to Find Corporate AI Responsibility Disclosures

## 1. Dedicated Responsible AI Reports

Companies publish these voluntarily. Format is almost always PDF or HTML.

| Company | Report | URL | Format |
|---------|--------|-----|--------|
| Microsoft | Responsible AI Transparency Report (annual, since 2024) | [microsoft.com/.../responsible-ai-transparency-report](https://www.microsoft.com/en-us/corporate-responsibility/responsible-ai-transparency-report/) | HTML + PDF |
| Google | Responsible AI Progress Report (annual, since 2019) | [ai.google/responsibility](https://ai.google/responsibility/) | PDF |
| Anthropic | Responsible Scaling Policy, Transparency Hub | [anthropic.com/transparency](https://www.anthropic.com/transparency) | HTML + PDF |
| IBM | Trust & Transparency Principles | [ibm.com/trust/responsible-ai](https://www.ibm.com/trust/responsible-ai) | HTML |
| NVIDIA | Trustworthy AI Center | [nvidia.com/.../trustworthy-ai](https://www.nvidia.com/en-us/ai-trust-center/trustworthy-ai/) | HTML |

These are our richest source for governance indicators. They typically cover board oversight, policy frameworks, training programs, incident management, and metrics -- exactly what our 10 indicators assess.

## 2. Model Cards and System Cards

Structured documentation of specific AI models/systems. More technical than governance reports.

| Type | Who Publishes | Where | Format |
|------|---------------|-------|--------|
| **System Cards** | OpenAI, Anthropic | Company websites + CDN PDFs | PDF, HTML |
| **Model Cards** | Meta (Llama), Google (Gemini), Anthropic (Claude) | GitHub repos, company sites | Markdown, PDF |
| **Hugging Face Model Cards** | Everyone (1M+ models) | [huggingface.co](https://huggingface.co/) | Markdown + YAML |

Relevant for our index: model cards sometimes disclose bias testing results, fairness metrics, energy consumption, and safety evaluations. These map to indicators gov_04 (sensitive use cases), gov_09 (incidents), gov_10 (metrics disclosure).

The Hugging Face model cards dataset is bulk-downloadable: [librarian-bots/model_cards_with_metadata](https://huggingface.co/datasets/librarian-bots/model_cards_with_metadata) (updated daily).

## 3. Regulatory Filings

### SEC 10-K Filings (US public companies)

The most standardized and machine-readable source. 72% of S&P 500 companies now disclose AI risks (up from 12% in 2023). AI mentions grew 700% from 2019-2024.

- **Where:** [SEC EDGAR](https://www.sec.gov/search-filings)
- **Format:** HTML, XBRL/iXBRL (machine-readable)
- **Access:** Free REST APIs at [data.sec.gov](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), no API key needed
- **Python tools:** [edgartools](https://pypi.org/project/edgartools/) (open source), [sec-api](https://sec-api.io/) (freemium)
- **Key sections:** Item 1A (Risk Factors), Item 1 (Business Description)

AI governance disclosures in 10-Ks tend to be thin and risk-focused compared to dedicated RAI reports, but they're standardized and cover thousands of companies.

### EU ESRS (European Sustainability Reporting Standards)

- **Where:** Company websites, national business registries
- **Format:** iXBRL (mandated), PDF
- **Relevance:** AI governance may appear under governance, environmental (AI energy use), and social (workforce impact) topics
- **Status:** CSRD reporting requirements being phased in 2024-2026

### EU AI Act Transparency Requirements (effective August 2026)

- Article 50: mandatory disclosure that users are interacting with AI, marking AI-generated content
- Article 13: technical documentation for high-risk AI systems
- GPAI model providers must disclose training data sources and methodologies
- Penalties: up to 35M EUR or 7% global turnover

## 4. Transparency Indices and Benchmarks

These aggregate and score companies, so they're useful both as data sources and as validation for our index.

| Source | What It Covers | Access | URL |
|--------|---------------|--------|-----|
| **Stanford FMTI** | 13 AI companies scored on 100-point transparency scale | Free, GitHub | [crfm.stanford.edu/fmti](https://crfm.stanford.edu/fmti/December-2025/index.html) |
| **OECD HAIP Reports** | G7 company transparency reports (Amazon, Google, Microsoft, OpenAI, etc.) | Free | [transparency.oecd.ai](https://transparency.oecd.ai/) |
| **Stanford AI Index** | Annual report on AI trends including governance | Free, PDF + Kaggle | [hai.stanford.edu/ai-index](https://hai.stanford.edu/ai-index) |
| **Evident Insights** | Banking sector RAI benchmarking | Commercial | [evidentinsights.com](https://evidentinsights.com/insights/responsible-ai-report/) |

**Notable finding:** Stanford FMTI average score dropped from 58/100 (2024) to 40/100 (2025). Transparency is declining among major AI labs.

## 5. Incident Databases

Not corporate disclosures per se, but useful for validating whether companies report their own incidents.

| Source | Coverage | Access | URL |
|--------|----------|--------|-----|
| **AI Incident Database** | 3,000+ incidents | Free, GraphQL API | [incidentdatabase.ai](https://incidentdatabase.ai/) |
| **MIT AI Incident Tracker** | 1,200+ incidents by risk domain | Free | [airisk.mit.edu/ai-incident-tracker](https://airisk.mit.edu/ai-incident-tracker) |

## 6. Frameworks and Standards (Reference, Not Data)

| Framework | Org | Relevance |
|-----------|-----|-----------|
| NIST AI RMF | NIST | De facto international standard, 4 functions (Govern, Map, Measure, Manage) |
| ISO/IEC 42001 | ISO | First certifiable AI management system standard |
| OECD AI Principles | OECD | Adopted by 46 countries, basis for many national frameworks |
| Partnership on AI | Industry consortium | Responsible practices for synthetic media, vendor transparency templates |
| WEF AI Governance Alliance | WEF | Presidio Framework, Responsible AI Innovation Playbook |
| IEEE 7000 | IEEE | Ethical system design process, maps to EU AI Act |

## 7. What's Actually Useful for Our Pipeline

**Priority data sources (richest RAI content, most accessible):**

1. **Dedicated RAI reports** (PDF) -- Microsoft, Google, Anthropic, IBM. Richest content for all 10 governance indicators. Download PDFs from company websites.
2. **SEC 10-K filings** (iXBRL) -- via EDGAR APIs. Standardized, machine-readable, covers thousands of companies. AI content is thinner but consistent.
3. **Stanford FMTI company reports** (HTML/PDF) -- useful for AI-specific companies. Good validation source.
4. **OECD HAIP reports** (HTML) -- G7 company self-reports against a standard framework.

**Secondary sources (useful but harder to process):**

5. **System cards / model cards** (PDF, Markdown) -- technical depth on specific models, good for metrics indicators.
6. **Corporate sustainability reports** (PDF) -- AI governance buried in broader ESG reporting, requires good RAG retrieval.
7. **NYC LL144 bias audits** (PDF) -- narrow scope (hiring algorithms only) but interesting niche data.

**Not worth pursuing yet:**

- Hugging Face model cards -- too technical, not governance-focused
- ESG data platforms (Bloomberg, MSCI) -- commercial, no raw text access
- EU ESRS filings -- still being phased in, limited AI content so far

## 8. Gaps in the Landscape

- **No single open dataset** of structured corporate AI disclosures across industries
- **Only 10%** of companies publicly disclose RAI policies (CSIRO finding)
- **Bias audits** under NYC LL144: only ~18 out of 391 employers posted audit reports (very low compliance)
- **AI-specific** metrics (energy use, fairness scores, incident rates) are rarely reported outside dedicated RAI reports from big tech
