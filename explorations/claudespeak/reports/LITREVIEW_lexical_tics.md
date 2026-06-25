# Literature review + reconciliation: is "delve" a Claude tic? (No — it's a GPT/ChatGPT one)

**Date:** 2026-06-24 · **Why:** the pilot reported that lexical tics "barely
separate Claude" (mean |d| ≈ 0.15), which seems to contradict the well-known
"LLMs overuse delve" narrative. JdR asked whether the contradiction is real, and
in particular whether "delve" is actually a *GPT* preference rather than a Claude
one. It is. This note reconciles the apparent contradiction against both the
published literature and our own corpus.

## 1. What the literature actually says

### "delve" and the excess-vocabulary family are tied to ChatGPT/GPT, not Claude

Kobak, González-Márquez, Horvát et al., *"Delving into LLM-assisted writing in
biomedical publications through excess vocabulary"* (arXiv 2406.07016; published
in *Science Advances*, 2024) tracked word-frequency shifts across **14M+ PubMed
abstracts (2010–2024)**, measuring "excess" usage after ChatGPT's release the way
epidemiologists measure excess mortality. Findings:

- The post-2022 surge consisted **almost entirely of style words** (66% verbs,
  18% adjectives), not content words.
- Top excess terms by frequency ratio: **"delves" (r ≈ 25×)**, "showcasing"
  (r ≈ 9×), "underscores" (r ≈ 9×); plus "intricate", "meticulously", "pivotal",
  "comprehensive", "crucial", "notably", "potential".
- The shift is dated to "roughly one year after ChatGPT was released" and
  attributed to **ChatGPT/LLM-assisted writing**. ([arXiv](https://arxiv.org/abs/2406.07016))

So the canonical "tic vocabulary" is empirically a **ChatGPT-era** signature.

### The proposed *origin* of "delve" is specifically about OpenAI's pipeline

The widely cited explanation is that OpenAI's RLHF annotation was heavily
outsourced to workers in Nigeria, where formal/business English uses "delve" far
more than US/UK English; annotator preferences got rewarded and amplified
(Alex Hern / *The Guardian*; summarized by Simon Willison,
["How cheap, outsourced labour in Africa is shaping AI English"](https://simonwillison.net/2024/Apr/18/delve/)).
Whatever the merits of the causal story, it is a story about **OpenAI's training
process**, not Anthropic's.

### A direct Claude-vs-GPT comparison points the other way for Claude

A controlled style comparison (*Trial-Error-Explain* in-context personalization,
arXiv 2502.08972, 2025) reports, in its lexical analysis:

- **GPT-4o-favored:** formal constructions — **"crucial to"**, "additionally",
  "therefore".
- **Claude-favored:** subjective/casual — **"believe"**, **"feel that"**,
  **"things like"**, **"kind of"**.
- Readability: Claude's characteristic words score **FRE ≈ 120** (very easy,
  conversational); GPT-4o's score **FRE ≈ 77** (formal). ([arXiv](https://arxiv.org/abs/2502.08972))

So the literature's own Claude-vs-GPT contrast says Claude leans **conversational**,
GPT leans **formal-academic** — exactly the register the delve-family lives in.

## 2. What our corpus says (`src/analyze_lexicon.py`, per 1000 words)

### GPT-excess family — GPT-4o leads, Claude does not

| term | chatgpt-hc3 | claude-opus-4-8 | gpt-4o | human |
|---|---|---|---|---|
| delve / delves / delving | 0 | 0 | 0 | 0 |
| crucial | 0 | **0.04** | **0.73** | 0 |
| comprehensive | 0.11 | 0.08 | **0.26** | 0.04 |
| essential | 0.03 | 0.14 | **0.29** | 0.04 |
| robust | 0 | 0.02 | **0.07** | 0 |
| realm / seamless / intricate / meticulous | 0 | 0 | **0.02 each** | 0 |
| potential | 1.02 | 0.24 | **1.41** | 0.13 |

Every excess word that appears at all is used **more by GPT-4o than by Claude** —
"crucial" by ~18×. "delve" itself appears **zero** times in this Q&A corpus (it is
a hedging/academic verb that rarely fits ELI5/finance/medicine answers, and it is
not a Claude word regardless).

### Claude-casual markers — Claude leads

| term | chatgpt-hc3 | claude-opus-4-8 | gpt-4o | human |
|---|---|---|---|---|
| actually | 0.20 | **1.38** | 0.22 | 0.13 |
| feel | 0.48 | **0.61** | 0.40 | 0.21 |
| it's worth | 0.06 | **0.22** | 0.02 | 0.04 |
| think | 0.11 | 0.65 | 0.29 | 0.71 |

Claude leads on conversational/subjective markers — most strikingly **"actually"**
(~6× GPT-4o) — matching the literature's "Claude is more casual/subjective."

## 3. Reconciliation

There is **no contradiction** — the pilot's aggregate tic measure was mislabeled.

- The "lexical tic" list used in the pilot was, in effect, a list of
  **ChatGPT/GPT excess words** (delve, crucial, intricate, …) drawn from the
  popular discourse. Applied to Claude, it correctly returns ~null: **those are
  not Claude's words.** Both the literature and our data agree GPT-4o uses them
  more.
- So the popular belief "LLMs overuse delve" is **true — for GPT/ChatGPT.** It was
  never a Claude property, and our null result for Claude is consistent with the
  literature, not against it.
- Claude *does* have a lexical lean, just a different one: toward conversational,
  subjective discourse markers ("actually", "feel", "it's worth", "think"). This
  signal is real but **smaller** than Claude's structural/rhythmic signature
  (markdown, sentence-length burstiness, function-word density), which is why a
  word-list approach underweights Claude's identity.

## 4. Correction to the pilot writeup

`FINDINGS_pilot.md` §5 originally framed this as "popular belief not supported."
That is imprecise. The accurate statement:

> The stereotyped "delve"-class vocabulary is a **GPT/ChatGPT** signature, not a
> Claude one — confirmed in our data (GPT-4o > Claude on every excess word that
> appears; "crucial" ~18×). Claude's own lexical lean is toward conversational
> markers ("actually", "feel", "it's worth"), but it is a **secondary** signal;
> Claude's primary fingerprint is structural and rhythmic, not a word list.

## 5. Caveats

- Our corpus is factual Q&A (HC3); "delve"-type academic verbs are rare here by
  genre, so absolute frequencies are low. The *relative* GPT>Claude ordering is
  the robust point, not the absolute zero for "delve."
- "old-ChatGPT" here is GPT-3.5-era; the modern GPT contrast is GPT-4o.
- A cleaner test of GPT-favored vocabulary would use a genre where these words are
  natural (essays, academic explanation) — a good check for the AlpacaEval track.

## Sources
- Kobak et al., *Delving into LLM-assisted writing in biomedical publications through excess vocabulary*, arXiv [2406.07016](https://arxiv.org/abs/2406.07016) (Science Advances 2024).
- Hern / Willison, *How cheap, outsourced labour in Africa is shaping AI English*, [simonwillison.net](https://simonwillison.net/2024/Apr/18/delve/) (2024).
- *Tuning-Free Personalized Alignment via Trial-Error-Explain In-Context Learning*, arXiv [2502.08972](https://arxiv.org/abs/2502.08972) (2025) — Claude vs GPT-4o lexical/readability contrast.
- GPTZero, [AI vocabulary list](https://gptzero.me/ai-vocabulary) (popular reference list of AI-associated words).
