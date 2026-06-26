# Per-domain robustness (Claude vs.\ pooled others, prose only)

Cohen's $d$ within each domain for the headline prose features. Positive = Claude higher (for func-word, negative = Claude denser, as expected). Stable sign/magnitude across domains ⇒ not a topic artifact.

| track      | domain       |   n_prompts |   burstiness |   func-word |   em-dash |   question |
|:-----------|:-------------|------------:|-------------:|------------:|----------:|-----------:|
| HC3        | cs_ai        |          40 |         2.5  |       -1.86 |      1.12 |       1.02 |
| HC3        | finance      |          40 |         2.11 |       -1.75 |      0.94 |       1.55 |
| HC3        | general      |          80 |         1.46 |       -0.97 |      0.95 |       0.17 |
| HC3        | medicine     |          40 |         2.65 |       -1.28 |      2.41 |       0.72 |
| AlpacaEval | helpful_base |          35 |         1.19 |       -0.81 |      0.66 |       0.85 |
| AlpacaEval | koala        |          35 |         0.99 |       -0.43 |      2.02 |       0.25 |
| AlpacaEval | oasst        |          49 |         1.46 |       -0.77 |      1.38 |       1.26 |
| AlpacaEval | selfinstruct |          64 |         0.56 |       -0.4  |      0.26 |       0.29 |
| AlpacaEval | vicuna       |          17 |         1.98 |       -1.17 |      3.22 |       2.21 |
