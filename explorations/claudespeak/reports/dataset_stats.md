# Corpus statistics (reproducible: src/dataset_stats.py)

## 1. Volume and response length by source

| track      | source                    |   records |   resp_words_total |   resp_words_mean |   resp_words_median |   resp_words_p25 |   resp_words_p75 |
|:-----------|:--------------------------|----------:|-------------------:|------------------:|--------------------:|-----------------:|-----------------:|
| HC3        | chatgpt-hc3               |       200 |              35267 |             176.3 |               178   |            129.2 |            215.5 |
| HC3        | claude-opus-4-8           |       200 |              50741 |             253.7 |               267   |            230.2 |            292.8 |
| HC3        | gpt-4o                    |       200 |              45513 |             227.6 |               238.5 |            163.2 |            294.8 |
| HC3        | human                     |       200 |              24015 |             120.1 |                76.5 |             37   |            148.5 |
| AlpacaEval | Meta-Llama-3-70B-Instruct |       200 |              59445 |             297.2 |               307.5 |            179.2 |            419.8 |
| AlpacaEval | Qwen2-72B-Instruct        |       200 |              52032 |             260.2 |               258.5 |            137   |            366.5 |
| AlpacaEval | claude-opus-4-8           |       200 |              50779 |             253.9 |               229.5 |            166.5 |            279.8 |
| AlpacaEval | deepseek-llm-67b-chat     |       200 |              37199 |             186   |               184   |             98   |            254.2 |
| AlpacaEval | gemini-pro                |       200 |              44399 |             222   |               234   |             82.5 |            317.5 |
| AlpacaEval | gpt-4-turbo-2024-04-09    |       200 |              54468 |             272.3 |               284.5 |            117.5 |            383.8 |
| AlpacaEval | gpt-4o-2024-05-13         |       200 |              55897 |             279.5 |               284.5 |            122.2 |            385.8 |

## 2. Prompt length by track (unique prompts)

| track      |   prompts |   prompt_words_mean |   prompt_words_median |   prompt_words_p25 |   prompt_words_p75 |   pct_with_question_mark |
|:-----------|----------:|--------------------:|----------------------:|-------------------:|-------------------:|-------------------------:|
| HC3        |       200 |                25.5 |                    10 |                6   |               42.8 |                       54 |
| AlpacaEval |       200 |                28.5 |                    18 |               10.2 |               31.8 |                       52 |

## 2b. Prompt mood (syntactic; % of unique prompts)

Questions vs declaratives etc. for the PROMPTS (what we ask Claude).

| track      |   interrogative% |   imperative% |   declarative% |
|:-----------|-----------------:|--------------:|---------------:|
| HC3        |               74 |             2 |             24 |
| AlpacaEval |               58 |            20 |             21 |

## 3. Volume by domain (response words, all sources)

| track      | domain       |   prompts |   records |   resp_words_total |
|:-----------|:-------------|----------:|----------:|-------------------:|
| AlpacaEval | helpful_base |        35 |       245 |              70233 |
| AlpacaEval | koala        |        35 |       245 |              66620 |
| AlpacaEval | oasst        |        49 |       343 |              95684 |
| AlpacaEval | selfinstruct |        64 |       448 |              78924 |
| AlpacaEval | vicuna       |        17 |       119 |              42758 |
| HC3        | cs_ai        |        40 |       160 |              35366 |
| HC3        | finance      |        40 |       160 |              39914 |
| HC3        | general      |        80 |       320 |              47162 |
| HC3        | medicine     |        40 |       160 |              33094 |

## 4. Sentence mood in responses by source (% of sentences; questions vs declaratives etc.)

| track      | source                    |   interrog% |   imper% |   exclam% |   declar% |
|:-----------|:--------------------------|------------:|---------:|----------:|----------:|
| HC3        | chatgpt-hc3               |           2 |        1 |         0 |        97 |
| HC3        | claude-opus-4-8           |          17 |        1 |         7 |        75 |
| HC3        | gpt-4o                    |           1 |        1 |         2 |        95 |
| HC3        | human                     |           4 |        0 |         1 |        95 |
| AlpacaEval | Meta-Llama-3-70B-Instruct |           3 |        1 |         3 |        94 |
| AlpacaEval | Qwen2-72B-Instruct        |           2 |        1 |         1 |        96 |
| AlpacaEval | claude-opus-4-8           |          10 |        1 |         4 |        86 |
| AlpacaEval | deepseek-llm-67b-chat     |           1 |        1 |         1 |        97 |
| AlpacaEval | gemini-pro                |           2 |        2 |         1 |        96 |
| AlpacaEval | gpt-4-turbo-2024-04-09    |           1 |        1 |         2 |        96 |
| AlpacaEval | gpt-4o-2024-05-13         |           2 |        1 |         2 |        96 |

## 5. Register signals by source (per 100 words; Flesch readability)

| track      | source                    |   first_person_per100 |   second_person_per100 |   flesch |
|:-----------|:--------------------------|----------------------:|-----------------------:|---------:|
| HC3        | chatgpt-hc3               |                  0.25 |                   2.21 |     47.6 |
| HC3        | claude-opus-4-8           |                  0.67 |                   2.41 |     39.5 |
| HC3        | gpt-4o                    |                  0.14 |                   1.8  |     45.8 |
| HC3        | human                     |                  0.93 |                   2.14 |     47.8 |
| AlpacaEval | Meta-Llama-3-70B-Instruct |                  0.76 |                   1.37 |     48.6 |
| AlpacaEval | Qwen2-72B-Instruct        |                  0.75 |                   1.58 |     52.4 |
| AlpacaEval | claude-opus-4-8           |                  1.08 |                   1.64 |     39.9 |
| AlpacaEval | deepseek-llm-67b-chat     |                  0.92 |                   1.4  |     51.9 |
| AlpacaEval | gemini-pro                |                  0.73 |                   1.15 |     50.5 |
| AlpacaEval | gpt-4-turbo-2024-04-09    |                  0.51 |                   1.45 |     47.4 |
| AlpacaEval | gpt-4o-2024-05-13         |                  0.63 |                   1.31 |     48.8 |

## 6. Prompt variety by dimension (counts of 200 per track)


### category

| category                  |   AlpacaEval |   HC3 |
|:--------------------------|-------------:|------:|
| advice_recommendation     |           31 |    49 |
| classification_extraction |            8 |     0 |
| code                      |           11 |     0 |
| creative_writing          |           24 |     0 |
| explanation               |           33 |    94 |
| factual_qa                |           29 |    53 |
| instruction_task          |           26 |     3 |
| math_reasoning            |           14 |     0 |
| opinion_subjective        |           11 |     0 |
| other                     |            1 |     1 |
| roleplay                  |            4 |     0 |
| summarize_rewrite_edit    |            7 |     0 |


### speech_act

| speech_act   |   AlpacaEval |   HC3 |
|:-------------|-------------:|------:|
| assertion    |            0 |     1 |
| directive    |           93 |    46 |
| expressive   |            0 |     1 |
| other        |            0 |     2 |
| question     |          106 |   150 |


### register

| register   |   AlpacaEval |   HC3 |
|:-----------|-------------:|------:|
| casual     |           62 |    70 |
| formal     |            7 |     0 |
| neutral    |          130 |   130 |


### tone

| tone      |   AlpacaEval |   HC3 |
|:----------|-------------:|------:|
| emotional |            5 |    20 |
| neutral   |          175 |   165 |
| playful   |           18 |     1 |
| urgent    |            1 |    14 |


### topic

| topic            |   AlpacaEval |   HC3 |
|:-----------------|-------------:|------:|
| arts_humanities  |           17 |     4 |
| education_howto  |           21 |     2 |
| entertainment    |           18 |    15 |
| finance_business |           18 |    41 |
| health_medicine  |            6 |    57 |
| math_logic       |           14 |     8 |
| other            |            9 |     8 |
| personal_life    |           20 |     1 |
| science_tech     |           33 |    48 |
| society_politics |           18 |    11 |
| software_code    |           25 |     5 |


### interaction flags (count)

| track      |   subjective |   sensitive |   multiturn_implied |
|:-----------|-------------:|------------:|--------------------:|
| AlpacaEval |           39 |          16 |                   4 |
| HC3        |           14 |          61 |                   8 |
