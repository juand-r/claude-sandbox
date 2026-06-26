# Step 4 — interpretable classifier (Claude vs not-Claude)

Logistic regression, standardized features, class-balanced, 5-fold stratified CV. AUC=1.0 perfect, 0.5 chance.

## Summary

| track                      | condition       |   AUC |   acc |   n_claude |   n_total |
|:---------------------------|:----------------|------:|------:|-----------:|----------:|
| HC3 (human-anchored)       | with_formatting | 0.982 | 0.976 |        200 |       800 |
| HC3 (human-anchored)       | prose_only      | 0.946 | 0.895 |        200 |       800 |
| AlpacaEval (modern models) | with_formatting | 0.901 | 0.869 |        200 |      1400 |
| AlpacaEval (modern models) | prose_only      | 0.867 | 0.826 |        200 |      1400 |
| WildChat (vs GPT-4-0314)   | with_formatting | 0.973 | 0.934 |        628 |      2128 |
| WildChat (vs GPT-4-0314)   | prose_only      | 0.854 | 0.789 |        628 |      2128 |
| NoRobots (vs human)        | with_formatting | 0.922 | 0.864 |       1500 |      3000 |
| NoRobots (vs human)        | prose_only      | 0.788 | 0.721 |       1500 |      3000 |


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


## WildChat (vs GPT-4-0314) — with_formatting (AUC=0.973, acc=0.934)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| md_bold_per100w     |       7.43 |
| md_header_per100w   |       2.36 |
| hapax_rate          |       1.79 |
| ttr                 |      -1.74 |
| md_bullet_per100w   |      -1.03 |
| md_code_per100w     |      -0.93 |
| lexical_tic_per1k   |      -0.83 |
| colon_per100        |      -0.74 |
| emdash_per100       |       0.46 |
| canned_phrase_per1k |      -0.37 |


## WildChat (vs GPT-4-0314) — prose_only (AUC=0.854, acc=0.789)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| sentence_burstiness |       1.16 |
| emdash_per100       |       0.84 |
| function_word_rate  |      -0.5  |
| lexical_tic_per1k   |      -0.48 |
| question_per100     |       0.39 |
| comma_per100        |      -0.36 |
| colon_per100        |      -0.33 |
| canned_phrase_per1k |      -0.32 |
| ttr                 |       0.25 |
| exclaim_per100      |      -0.25 |


## NoRobots (vs human) — with_formatting (AUC=0.922, acc=0.864)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| md_bold_per100w     |       8.83 |
| hapax_rate          |       0.72 |
| emoji_per100        |       0.62 |
| ttr                 |      -0.56 |
| md_header_per100w   |       0.34 |
| sentence_burstiness |       0.32 |
| mean_sentence_len   |       0.26 |
| emdash_per100       |       0.25 |
| md_code_per100w     |       0.23 |
| comma_per100        |       0.2  |


## NoRobots (vs human) — prose_only (AUC=0.788, acc=0.721)

Top features (|standardized coef|); + = pushes toward Claude:

| feature             |   std_coef |
|:--------------------|-----------:|
| sentence_burstiness |       0.81 |
| mean_sentence_len   |       0.73 |
| semicolon_per100    |      -0.64 |
| emdash_per100       |       0.53 |
| function_word_rate  |      -0.3  |
| exclaim_per100      |      -0.19 |
| colon_per100        |       0.15 |
| comma_per100        |       0.08 |
| tricolon_per100w    |      -0.08 |
| ttr                 |       0.07 |
