# Pilot stylometry — Claude vs human / GPT-4o / old-ChatGPT

Corpus: 800 records across 4 sources (HC3 pilot, 200 prompts).

## Records per source

```
generator
claude-opus-4-8    200
gpt-4o             200
human              200
chatgpt-hc3        200
```

## Top distinguishing features (ranked by mean |Cohen's d|, Claude vs others)

Positive d = Claude uses it MORE than the comparison source.

|                     |   d_vs_chatgpt-hc3 |   d_vs_gpt-4o |   d_vs_human |   mean_abs_d |
|:--------------------|-------------------:|--------------:|-------------:|-------------:|
| md_header_per100w   |               2.92 |          2.84 |         2.92 |         2.9  |
| md_bold_per100w     |               2.66 |          1.6  |         2.66 |         2.31 |
| md_bullet_per100w   |               2.18 |          1.06 |         2.19 |         1.81 |
| sentence_burstiness |               1.85 |          1.07 |         1.55 |         1.49 |
| function_word_rate  |              -2.24 |         -0.87 |        -1.29 |         1.47 |
| colon_per100        |               0.99 |         -0.22 |         1.28 |         0.83 |
| emoji_per100        |               0.83 |          0.83 |         0.83 |         0.83 |
| question_per100     |               0.98 |          1.32 |         0.17 |         0.82 |
| emdash_per100       |               1.07 |          0.45 |         0.82 |         0.78 |
| ttr                 |               0.79 |          0.3  |        -0.89 |         0.66 |
| hapax_rate          |               0.74 |          0.24 |        -0.87 |         0.62 |
| exclaim_per100      |               0.54 |          0.27 |         0.61 |         0.48 |
| mean_sentence_len   |              -0.01 |          0.9  |         0.22 |         0.38 |
| canned_phrase_per1k |              -0.64 |         -0.17 |         0.3  |         0.37 |
| comma_per100        |              -0.28 |         -0.56 |        -0.15 |         0.33 |
| hedge_rate_per100   |              -0.31 |         -0.33 |         0.17 |         0.27 |
| md_code_per100w     |               0.23 |          0.23 |         0.23 |         0.23 |
| semicolon_per100    |               0.27 |          0.24 |        -0.17 |         0.22 |

## Mean feature values by source (top 18 features)

|                     |   chatgpt-hc3 |   claude-opus-4-8 |   gpt-4o |   human |
|:--------------------|--------------:|------------------:|---------:|--------:|
| md_header_per100w   |          0    |              1.75 |     0.02 |    0    |
| md_bold_per100w     |          0    |              4.45 |     1.4  |    0    |
| md_bullet_per100w   |          0.01 |              3.86 |     1.62 |    0    |
| sentence_burstiness |          0.36 |              0.86 |     0.55 |    0.37 |
| function_word_rate  |          0.44 |              0.33 |     0.37 |    0.41 |
| colon_per100        |          0.4  |              1.41 |     1.69 |    0.24 |
| emoji_per100        |          0    |              0.52 |     0    |    0    |
| question_per100     |          0.07 |              0.61 |     0.01 |    0.28 |
| emdash_per100       |          0.01 |              0.88 |     0.4  |    0.15 |
| ttr                 |          0.55 |              0.62 |     0.59 |    0.73 |
| hapax_rate          |          0.37 |              0.46 |     0.43 |    0.59 |
| exclaim_per100      |          0.05 |              0.43 |     0.22 |    0.03 |
| mean_sentence_len   |         26.96 |             26.86 |    16.02 |   23.38 |
| canned_phrase_per1k |          2.96 |              0.8  |     1.18 |    0.3  |
| comma_per100        |          5.6  |              4.78 |     6.48 |    5.31 |
| hedge_rate_per100   |          2.35 |              1.87 |     2.39 |    1.6  |
| md_code_per100w     |          0    |              0.03 |     0    |    0    |
| semicolon_per100    |          0.01 |              0.04 |     0.01 |    0.2  |
