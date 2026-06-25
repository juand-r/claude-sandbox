# Step 3 — AlpacaEval modern-model track

## Conclusion

Three results, all confirming and extending the HC3 track against **modern**
frontier models (gpt-4-turbo, gpt-4o, gemini-pro, deepseek-67b, Qwen2-72B,
Llama-3-70B) on instruction/essay prompts.

1. **The structural/rhythmic signature replicates vs modern models.**
   Claude vs pooled-modern, markdown-stripped prose: sentence burstiness d=1.01
   (0.68 vs 0.39), em-dash d=0.63 (0.93 vs 0.20), function-word density (lower
   rate) d=−0.55, question/offer rate d=0.50, longer sentences (39.7 vs 22 words).
   Same fingerprint as the HC3 track — not specific to GPT-4o/human.

2. **Vocabulary reconciliation, decisively confirmed (JdR's hypothesis).** In the
   essay genre that *does* elicit the "AI-slop" words, **Claude is the LEAST
   delve/crucial model of all seven**:
   - "delve"/"delves": Claude is the **only** model at **0.000** for both; every
     other model uses them (gpt-4o "delves" 0.089, gpt-4-turbo, gemini, deepseek,
     llama, qwen all > 0).
   - "crucial": **Claude 0.039 — the lowest**, vs gpt-4-turbo 0.422, gpt-4o 0.340,
     Qwen 0.346, Llama 0.185.
   - "intricate"/"pivotal": Claude 0; several others > 0.
   So the famous tic vocabulary is a property of GPT *and other models* — and
   Claude is the cleanest of the frontier models on it. The popular "AI uses
   delve" belief holds, but it is the *opposite* of a Claude signature.

3. **The offer-closer n-gram signature replicates.** Top Claude 3-grams vs modern
   models: "would you like", "like me to", "let me know", "you like me", "if you'd
   like", "want me to", "me know if", "how it works". The
   recap-and-offer-to-continue closer is Claude's most stable lexical fingerprint
   across both corpora and against modern models.

**Caveats.** AlpacaEval outputs are the published vintages (gemini-pro 1.0,
deepseek-67b, Qwen2-72B, gpt-4-turbo/4o 2024) — modern-ish, not absolute latest.
No human cell in this track (by design; HC3 carries the human anchor).

---

Records: 1400 across 7 sources (Claude self-gen vs 6 reused modern-ish models; no human).

```
generator
claude-opus-4-8              200
gpt-4-turbo-2024-04-09       200
gpt-4o-2024-05-13            200
gemini-pro                   200
deepseek-llm-67b-chat        200
Qwen2-72B-Instruct           200
Meta-Llama-3-70B-Instruct    200
```

## (A) Claude vs pooled modern models — prose effect sizes (markdown stripped)

Does the HC3-track signature replicate against modern models?

|                     |   d_vs_pooled_modern |   claude_mean |   others_mean |
|:--------------------|---------------------:|--------------:|--------------:|
| sentence_burstiness |                 1.01 |          0.68 |          0.39 |
| mean_sentence_len   |                 0.68 |         39.72 |         22.12 |
| emdash_per100       |                 0.63 |          0.93 |          0.2  |
| function_word_rate  |                -0.55 |          0.32 |          0.37 |
| ttr                 |                 0.53 |          0.65 |          0.57 |
| question_per100     |                 0.5  |          0.51 |          0.1  |
| hapax_rate          |                 0.46 |          0.5  |          0.41 |
| tricolon_per100w    |                -0.23 |          0.18 |          0.3  |
| comma_per100        |                -0.21 |          4.86 |          5.71 |
| lexical_tic_per1k   |                -0.18 |          0.38 |          0.93 |
| canned_phrase_per1k |                -0.18 |          0.49 |          1.05 |
| colon_per100        |                -0.16 |          1.94 |          2.48 |

## (B) GPT-excess vocabulary by source (per 1000 words), essay genre

Where do delve/crucial/intricate land now that the genre fits them?

| term          |   Meta-Llama-3-70B-Instruct |   Qwen2-72B-Instruct |   claude-opus-4-8 |   deepseek-llm-67b-chat |   gemini-pro |   gpt-4-turbo-2024-04-09 |   gpt-4o-2024-05-13 |
|:--------------|----------------------------:|---------------------:|------------------:|------------------------:|-------------:|-------------------------:|--------------------:|
| delve         |                       0.017 |                0     |             0     |                   0     |        0     |                    0.018 |               0.018 |
| delves        |                       0.034 |                0.019 |             0     |                   0.027 |        0.023 |                    0.037 |               0.089 |
| delving       |                       0     |                0     |             0     |                   0     |        0     |                    0     |               0     |
| intricate     |                       0.05  |                0.019 |             0     |                   0     |        0.023 |                    0     |               0     |
| crucial       |                       0.185 |                0.346 |             0.039 |                   0.054 |        0.09  |                    0.422 |               0.34  |
| pivotal       |                       0     |                0.038 |             0     |                   0     |        0     |                    0.073 |               0.018 |
| comprehensive |                       0.101 |                0.077 |             0.079 |                   0.054 |        0.225 |                    0.165 |               0.215 |
| meticulous    |                       0     |                0     |             0     |                   0     |        0     |                    0.018 |               0.018 |
| realm         |                       0.017 |                0.019 |             0     |                   0     |        0.045 |                    0.018 |               0     |
| robust        |                       0.034 |                0.135 |             0.079 |                   0.108 |        0.18  |                    0.147 |               0.179 |
| seamless      |                       0.05  |                0.019 |             0.02  |                   0     |        0.045 |                    0.018 |               0.054 |
| underscore    |                       0     |                0     |             0.02  |                   0     |        0     |                    0     |               0.036 |
| showcase      |                       0.05  |                0.038 |             0.02  |                   0.027 |        0.068 |                    0.018 |               0.018 |
| essential     |                       0.421 |                0.115 |             0.138 |                   0.242 |        0.158 |                    0.165 |               0.179 |
| nuanced       |                       0.017 |                0.019 |             0.02  |                   0     |        0     |                    0.037 |               0.054 |
| leverage      |                       0.067 |                0.058 |             0.079 |                   0.027 |        0     |                    0.073 |               0.089 |

## (C) Claude n-gram signature vs pooled modern models


### 1-gram — most Claude-like

| term       |     z |   claude_ct |   other_ct |
|:-----------|------:|------------:|-----------:|
| me         | 16.56 |         151 |        135 |
| what       | 10.64 |         133 |        275 |
| like       | 10.33 |         218 |        616 |
| would      | 10.32 |         132 |        283 |
| you        |  9.7  |         502 |       1977 |
| credential |  9.51 |          44 |         10 |
| so         |  8.57 |         110 |        265 |
| actually   |  8.54 |          34 |         10 |
| specific   |  8.43 |         101 |        236 |
| know       |  8.32 |          81 |        167 |
| let        |  7.73 |          59 |        107 |
| particular |  7.36 |          30 |         27 |
| most       |  7.31 |          88 |        223 |
| did        |  7.27 |          31 |         31 |
| no         |  7.2  |          68 |        151 |


### 2-gram — most Claude-like

| term           |     z |   claude_ct |   other_ct |
|:---------------|------:|------------:|-----------:|
| me to          | 14.1  |          73 |         24 |
| you like       | 13.02 |          84 |         10 |
| let me         | 10.74 |          42 |         26 |
| would you      | 10.48 |          85 |          4 |
| i can          |  9.76 |          43 |         52 |
| like me        |  9.55 |          58 |          4 |
| a specific     |  9.46 |          39 |         44 |
| to know        |  8.15 |          39 |         69 |
| me know        |  8.02 |          25 |         21 |
| on any         |  7.45 |          20 |          8 |
| to go          |  7.27 |          19 |          8 |
| a few          |  7.25 |          43 |        105 |
| any of         |  6.85 |          17 |         10 |
| you'd like     |  6.57 |          16 |          5 |
| smart contract |  6.42 |          16 |          4 |


### 3-gram — most Claude-like

| term           |     z |   claude_ct |   other_ct |
|:---------------|------:|------------:|-----------:|
| would you like | 11.28 |          83 |          4 |
| like me to     | 10.16 |          57 |          4 |
| let me know    |  8.63 |          25 |         21 |
| you like me    |  8.61 |          55 |          2 |
| any of these   |  6.94 |          16 |          5 |
| if you'd like  |  5.67 |          13 |          2 |
| me know if     |  5.4  |          11 |         13 |
| to know we     |  5.33 |          17 |         40 |
| how it works   |  5.23 |          10 |         11 |
| want me to     |  5.19 |          10 |          2 |
| is one of      |  5.04 |          11 |         17 |
| know if you'd  |  4.44 |           9 |          1 |
| to a specific  |  4.34 |           6 |          3 |
| on any of      |  4.34 |           6 |          3 |
| focus on a     |  4.34 |           6 |          3 |
