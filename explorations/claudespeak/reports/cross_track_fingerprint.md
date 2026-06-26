# Cross-track fingerprint replication (reproducible: src/analyze_tracks.py)

Claude vs pooled non-Claude sources, Cohen's d, per track. Positive d = Claude uses it MORE.

## Records per track and source

| generator                 |   AlpacaEval |   HC3 |   NoRobots |   WildChat |
|:--------------------------|-------------:|------:|-----------:|-----------:|
| Meta-Llama-3-70B-Instruct |          200 |     0 |          0 |          0 |
| Qwen2-72B-Instruct        |          200 |     0 |          0 |          0 |
| chatgpt-hc3               |            0 |   200 |          0 |          0 |
| claude-opus-4-8           |          200 |   200 |       1500 |        628 |
| deepseek-llm-67b-chat     |          200 |     0 |          0 |          0 |
| gemini-pro                |          200 |     0 |          0 |          0 |
| gpt-4-0314                |            0 |     0 |          0 |       1500 |
| gpt-4-turbo-2024-04-09    |          200 |     0 |          0 |          0 |
| gpt-4o                    |            0 |   200 |          0 |          0 |
| gpt-4o-2024-05-13         |          200 |     0 |          0 |          0 |
| human                     |            0 |   200 |       1500 |          0 |

## Claude-vs-pooled effect sizes (headline features)

n (Claude, others) per track: HC3=(200, 600), AlpacaEval=(200, 1200), WildChat=(628, 628), NoRobots=(1500, 1500)

|                     | feature_meaning                                        |   HC3 |   AlpacaEval |   WildChat |   NoRobots | sign_agree   |
|:--------------------|:-------------------------------------------------------|------:|-------------:|-----------:|-----------:|:-------------|
| sentence_burstiness | rhythm: std/mean sentence length (Claude higher)       |  1.56 |         0.45 |       0.58 |       0.63 | 4/4          |
| function_word_rate  | content density: function-word fraction (Claude lower) | -1.29 |        -0.57 |      -0.49 |      -0.24 | 4/4          |
| emdash_per100       | em-dash rate /100w (Claude higher)                     |  0.86 |         0.12 |       0.48 |       0.34 | 4/4          |
| md_bullet_per100w   | markdown bullets /100w                                 |  2.03 |         0.29 |       0.35 |       0.05 | 4/4          |
| md_header_per100w   | markdown headers /100w                                 |  4.06 |         1.81 |       1.26 |       0.66 | 4/4          |
| md_bold_per100w     | markdown bold /100w                                    |  2.72 |         0.88 |       1.12 |       1.09 | 4/4          |
| question_per100     | questions /100w (offer-to-continue proxy)              |  0.35 |         0.4  |       0.32 |       0.03 | 4/4          |
| colon_per100        | colon rate /100w (scaffolding)                         |  0.52 |        -0.15 |       0.11 |       0.25 | 3/4          |
| ttr                 | type-token ratio                                       | -0    |         0.48 |       0.06 |      -0.37 | 2/4          |

`sign_agree` = how many tracks share the majority sign (higher = more consistent fingerprint).
