# Step 2 — length-stratified robustness (markdown-stripped prose)

## Conclusion

**The headline prose findings are NOT length artifacts.** Claude does write
longer (mean 253 words vs human 120, GPT-4o 228), but the signature survives both
controls:

- **Sentence burstiness** — positive Cohen's d in every length quartile
  (0.57 → 1.04 → 2.18 → 1.96); length-controlled OLS t = **20.6**. Robust.
- **Function-word density (lower function-word rate)** — negative d in every
  quartile; OLS t = **−14.4**. Robust.
- **Em-dash habit** — positive in Q2–Q4 (weak in the shortest bin); OLS
  t = **12.6**. Robust.
- **Question rate** (the offer-to-continue closer) — OLS t = **4.6**. Robust.

**Caveat — TTR / hapax are length-sensitive.** Type-token ratio mechanically
falls as texts get longer, and pooled "others" includes very short human answers,
so the raw cross-source TTR comparison is confounded. Length-controlled, Claude's
TTR is *slightly higher* than pooled others (OLS t = 9.6), but the earlier
**Claude < human** TTR fact still holds in a direct human-only comparison. Treat
lexical-diversity claims as length-conditioned.

---

## Answer length by source (words)

| generator       |   mean |   median |
|:----------------|-------:|---------:|
| chatgpt-hc3     |  176.3 |    178   |
| claude-opus-4-8 |  253.1 |    266   |
| gpt-4o          |  227.6 |    238.5 |
| human           |  120.1 |     76.5 |

## Claude share across length quartiles (sanity: is Claude just the long bin?)

| lenq   |   chatgpt-hc3 |   claude-opus-4-8 |   gpt-4o |   human |
|:-------|--------------:|------------------:|---------:|--------:|
| Q1     |            29 |                15 |       28 |     128 |
| Q2     |           102 |                14 |       46 |      38 |
| Q3     |            53 |                84 |       53 |      16 |
| Q4     |            16 |                87 |       73 |      18 |

## (1) Claude-vs-others Cohen's d WITHIN each length quartile

If the effect holds across Q1–Q4, it is not a length artifact.

| feature             |    Q1 |    Q2 |    Q3 |    Q4 |
|:--------------------|------:|------:|------:|------:|
| sentence_burstiness |  0.57 |  1.04 |  2.18 |  1.96 |
| function_word_rate  | -0.45 | -2.24 | -1.5  | -0.99 |
| emdash_per100       |  0.11 |  2.21 |  0.97 |  1.25 |
| colon_per100        |  1.08 |  1.49 |  0.16 | -0.63 |
| question_per100     |  0.13 |  1.88 |  2.06 |  1.47 |
| ttr                 | -0.29 |  1.12 |  1.33 |  1.43 |
| hapax_rate          | -0.28 |  1.24 |  1.19 |  1.33 |

## (2) Length-controlled OLS: feature ~ is_claude + z(n_words)

is_claude_beta = Claude effect holding length fixed; |t|>~2 is significant.

| feature             |   is_claude_beta |   t_stat |
|:--------------------|-----------------:|---------:|
| sentence_burstiness |            0.433 |     20.6 |
| function_word_rate  |           -0.078 |    -14.4 |
| emdash_per100       |            0.684 |     12.6 |
| colon_per100        |            0.249 |      2.6 |
| question_per100     |            0.559 |      4.6 |
| ttr                 |            0.073 |      9.6 |
| hapax_rate          |            0.079 |      7.8 |
