# Pilot ablation — Claude identifiability from RAW PROSE (markdown stripped)

Formatting features (headers/bullets/bold/code/emoji) are removed and markup is stripped from the text. If Claude still separates, the voice is more than a formatting habit.

## Prose-only distinguishing features (mean |Cohen's d|)

Positive d = Claude MORE than comparison.

|                     |   d_vs_chatgpt-hc3 |   d_vs_gpt-4o |   d_vs_human |   mean_abs_d |
|:--------------------|-------------------:|--------------:|-------------:|-------------:|
| sentence_burstiness |               1.74 |          1.87 |         1.45 |         1.69 |
| function_word_rate  |              -2.24 |         -0.87 |        -1.29 |         1.47 |
| emdash_per100       |               1.04 |          0.81 |         0.76 |         0.87 |
| colon_per100        |               0.99 |         -0.23 |         1.29 |         0.84 |
| question_per100     |               0.98 |          1.32 |         0.17 |         0.82 |
| ttr                 |               0.8  |          0.3  |        -0.88 |         0.66 |
| hapax_rate          |               0.75 |          0.25 |        -0.86 |         0.62 |
| mean_sentence_len   |               0.26 |          0.84 |         0.45 |         0.52 |
| exclaim_per100      |               0.54 |          0.28 |         0.61 |         0.48 |
| canned_phrase_per1k |              -0.63 |         -0.17 |         0.3  |         0.37 |
| comma_per100        |              -0.28 |         -0.55 |        -0.14 |         0.32 |
| hedge_rate_per100   |              -0.31 |         -0.33 |         0.17 |         0.27 |
| semicolon_per100    |               0.27 |          0.24 |        -0.17 |         0.22 |
| tricolon_per100w    |              -0.18 |         -0.15 |         0.32 |         0.22 |
| lexical_tic_per1k   |               0.03 |         -0.22 |         0.21 |         0.15 |

## Mean prose-feature values by source

|                     |   chatgpt-hc3 |   claude-opus-4-8 |   gpt-4o |   human |
|:--------------------|--------------:|------------------:|---------:|--------:|
| sentence_burstiness |          0.36 |              0.84 |     0.35 |    0.37 |
| function_word_rate  |          0.44 |              0.33 |     0.37 |    0.41 |
| emdash_per100       |          0.01 |              0.78 |     0.12 |    0.15 |
| colon_per100        |          0.4  |              1.4  |     1.69 |    0.24 |
| question_per100     |          0.07 |              0.61 |     0.01 |    0.28 |
| ttr                 |          0.55 |              0.62 |     0.59 |    0.73 |
| hapax_rate          |          0.37 |              0.46 |     0.43 |    0.59 |
| mean_sentence_len   |         27.01 |             31.38 |    19.4  |   23.38 |
| exclaim_per100      |          0.05 |              0.44 |     0.22 |    0.03 |
| canned_phrase_per1k |          2.96 |              0.8  |     1.18 |    0.3  |
| comma_per100        |          5.6  |              4.79 |     6.48 |    5.31 |
| hedge_rate_per100   |          2.35 |              1.87 |     2.39 |    1.6  |
| semicolon_per100    |          0.01 |              0.04 |     0.01 |    0.2  |
| tricolon_per100w    |          0.27 |              0.18 |     0.24 |    0.07 |
| lexical_tic_per1k   |          0.32 |              0.4  |     1.07 |    0.03 |
