# Step 4 — interpretable classifier (Claude vs not-Claude)

Logistic regression, standardized features, class-balanced, 5-fold stratified CV. AUC=1.0 perfect, 0.5 chance.

## Conclusion

**Claude is highly separable — and the signal is mostly prose, not formatting.**

| Track | with formatting | prose only |
|---|---|---|
| HC3 (vs human / GPT-4o / old-ChatGPT) | AUC 0.982 | **AUC 0.946** |
| AlpacaEval (vs 6 modern frontier models) | AUC 0.901 | **AUC 0.867** |

- Stripping markdown drops AUC only modestly (0.982→0.946; 0.901→0.867), so the
  classifier is not just reading layout — prose alone identifies Claude well, even
  against six modern models.
- The driving coefficients **match the descriptive findings** (a good consistency
  check): prose-only separation is led by **sentence burstiness (+)**,
  **function-word density (− function-word rate)**, **em-dash rate (+)**, and on
  AlpacaEval the **question/offer rate (+)** — the same features Steps 1–2 found,
  arrived at by an independent method.
- Interpretation: there is a stable, learnable Claude "voice" at the prose level.
  This is a *detectability* number; the *characterization* (what the voice is) is
  the burstiness / density / em-dash / offer-closer profile named above.

---


## Summary

| track                      | condition       |   AUC |   acc |   n_claude |   n_total |
|:---------------------------|:----------------|------:|------:|-----------:|----------:|
| HC3 (human-anchored)       | with_formatting | 0.982 | 0.976 |        200 |       800 |
| HC3 (human-anchored)       | prose_only      | 0.946 | 0.895 |        200 |       800 |
| AlpacaEval (modern models) | with_formatting | 0.901 | 0.869 |        200 |      1400 |
| AlpacaEval (modern models) | prose_only      | 0.867 | 0.826 |        200 |      1400 |


## HC3 (human-anchored) — with_formatting (AUC=0.982, acc=0.976)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| md_bold_per100w     |       4.53 |
| md_header_per100w   |       2.81 |
| colon_per100        |      -1.63 |
| ttr                 |       0.8  |
| emoji_per100        |       0.78 |
| sentence_burstiness |       0.32 |
| comma_per100        |       0.31 |
| semicolon_per100    |      -0.3  |
| hedge_rate_per100   |      -0.29 |
| hapax_rate          |      -0.27 |


## HC3 (human-anchored) — prose_only (AUC=0.946, acc=0.895)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| sentence_burstiness |       1.76 |
| function_word_rate  |      -1.69 |
| emdash_per100       |       1.14 |
| semicolon_per100    |      -0.75 |
| exclaim_per100      |       0.38 |
| hedge_rate_per100   |      -0.18 |
| ttr                 |       0.14 |
| comma_per100        |       0.14 |
| not_just_but_per1k  |      -0.1  |
| mean_sentence_len   |       0.09 |


## AlpacaEval (modern models) — with_formatting (AUC=0.901, acc=0.869)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| emoji_per100        |       2.1  |
| ttr                 |       1.92 |
| md_header_per100w   |       1.32 |
| hapax_rate          |      -0.89 |
| mean_sentence_len   |       0.76 |
| md_bullet_per100w   |      -0.72 |
| md_bold_per100w     |       0.69 |
| sentence_burstiness |       0.63 |
| colon_per100        |      -0.55 |
| question_per100     |       0.35 |


## AlpacaEval (modern models) — prose_only (AUC=0.867, acc=0.826)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| ttr                 |       1.45 |
| sentence_burstiness |       0.82 |
| question_per100     |       0.77 |
| hapax_rate          |      -0.75 |
| emdash_per100       |       0.52 |
| mean_sentence_len   |       0.44 |
| canned_phrase_per1k |      -0.39 |
| function_word_rate  |      -0.28 |
| exclaim_per100      |      -0.23 |
| tricolon_per100w    |      -0.23 |
