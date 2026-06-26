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
| WildChat   | claude-opus-4-8           |       628 |             383927 |             611.3 |               333.5 |            202.5 |            841.8 |
| WildChat   | gpt-4-0314                |      1500 |             561697 |             374.5 |               357   |            168.2 |            554.8 |
| NoRobots   | claude-opus-4-8           |      1500 |             262520 |             175   |               162   |             72.2 |            244   |
| NoRobots   | human                     |      1500 |             134690 |              89.8 |                48   |             21   |            120   |

## 2. Prompt length by track (unique prompts)

| track      |   prompts |   prompt_words_mean |   prompt_words_median |   prompt_words_p25 |   prompt_words_p75 |   pct_with_question_mark |
|:-----------|----------:|--------------------:|----------------------:|-------------------:|-------------------:|-------------------------:|
| HC3        |       200 |                25.5 |                    10 |                6   |               42.8 |                       54 |
| AlpacaEval |       200 |                28.5 |                    18 |               10.2 |               31.8 |                       52 |
| WildChat   |      1500 |                60.5 |                    35 |               13.2 |               78   |                       21 |
| NoRobots   |      1500 |               101.6 |                    49 |               18.2 |              153   |                       53 |

## 2b. Prompt mood (syntactic; % of unique prompts)

Questions vs declaratives etc. for the PROMPTS (what we ask Claude).

| track      |   interrogative% |   imperative% |   declarative% |
|:-----------|-----------------:|--------------:|---------------:|
| HC3        |               74 |             2 |             24 |
| AlpacaEval |               58 |            20 |             21 |
| WildChat   |               27 |            35 |             38 |
| NoRobots   |               54 |            21 |             26 |

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
| NoRobots   | Brainstorm   |       150 |       300 |              70478 |
| NoRobots   | Chat         |       150 |       300 |              25949 |
| NoRobots   | Classify     |       150 |       300 |              27189 |
| NoRobots   | Closed QA    |       150 |       300 |              16235 |
| NoRobots   | Coding       |       150 |       300 |              62946 |
| NoRobots   | Extract      |       150 |       300 |              11921 |
| NoRobots   | Generation   |       150 |       300 |              65266 |
| NoRobots   | Open QA      |       150 |       300 |              32729 |
| NoRobots   | Rewrite      |       150 |       300 |              57942 |
| NoRobots   | Summarize    |       150 |       300 |              26555 |
| WildChat   | ?            |      1500 |      2128 |             945624 |

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
| WildChat   | claude-opus-4-8           |           6 |        1 |         3 |        91 |
| WildChat   | gpt-4-0314                |           3 |        1 |         2 |        94 |
| NoRobots   | claude-opus-4-8           |           9 |        1 |         5 |        86 |
| NoRobots   | human                     |           5 |        1 |         5 |        90 |

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
| WildChat   | claude-opus-4-8           |                  1.31 |                   1.3  |     44.9 |
| WildChat   | gpt-4-0314                |                  1.07 |                   1.16 |     42.9 |
| NoRobots   | claude-opus-4-8           |                  1.2  |                   1.4  |     48.2 |
| NoRobots   | human                     |                  1.3  |                   1.68 |     58.7 |

## 6. Prompt variety by dimension (counts of 200 per track)


### category

| category                  |   ? |   AlpacaEval |   HC3 |   NoRobots |   WildChat |
|:--------------------------|----:|-------------:|------:|-----------:|-----------:|
| advice_recommendation     |   0 |           31 |    49 |         35 |         18 |
| classification_extraction |   0 |            9 |     0 |        101 |          5 |
| code                      |   0 |           11 |     0 |         39 |         44 |
| creative_writing          |   0 |           24 |     0 |         40 |        166 |
| explanation               |   0 |           33 |    94 |         14 |         37 |
| factual_qa                |   0 |           29 |    53 |         78 |         44 |
| instruction_task          |   0 |           26 |     3 |          9 |         32 |
| math_reasoning            |   0 |           14 |     0 |          1 |         11 |
| opinion_subjective        |   0 |           11 |     0 |          1 |          8 |
| other                     |   0 |            1 |     1 |          2 |         15 |
| personal_emotional        |   0 |            0 |     0 |          6 |          0 |
| roleplay                  |   0 |            4 |     0 |          0 |          9 |
| summarize_rewrite_edit    |   1 |            7 |     0 |         74 |         11 |


### speech_act

| speech_act   |   ? |   AlpacaEval |   HC3 |   NoRobots |   WildChat |
|:-------------|----:|-------------:|------:|-----------:|-----------:|
| assertion    |   0 |            0 |     1 |          1 |          9 |
| directive    |   1 |           94 |    46 |        238 |        295 |
| expressive   |   0 |            0 |     1 |          6 |          0 |
| other        |   0 |            0 |     2 |          0 |          2 |
| question     |   0 |          106 |   150 |        155 |         94 |


### register

| register   |   ? |   AlpacaEval |   HC3 |   NoRobots |   WildChat |
|:-----------|----:|-------------:|------:|-----------:|-----------:|
| casual     |   1 |           62 |    70 |         77 |        108 |
| formal     |   0 |            7 |     0 |          4 |         42 |
| neutral    |   0 |          131 |   130 |        319 |        250 |


### tone

| tone      |   ? |   AlpacaEval |   HC3 |   NoRobots |   WildChat |
|:----------|----:|-------------:|------:|-----------:|-----------:|
| emotional |   0 |            5 |    20 |          7 |          7 |
| neutral   |   1 |          176 |   165 |        363 |        346 |
| playful   |   0 |           18 |     1 |         29 |         45 |
| urgent    |   0 |            1 |    14 |          1 |          2 |


### topic

| topic            |   ? |   AlpacaEval |   HC3 |   NoRobots |   WildChat |
|:-----------------|----:|-------------:|------:|-----------:|-----------:|
| arts_humanities  |   0 |           17 |     4 |         59 |         32 |
| education_howto  |   0 |           21 |     2 |         25 |         21 |
| entertainment    |   0 |           18 |    15 |         72 |        121 |
| finance_business |   0 |           18 |    41 |         28 |         35 |
| health_medicine  |   0 |            6 |    57 |         17 |         32 |
| math_logic       |   0 |           14 |     8 |          2 |         14 |
| other            |   0 |            9 |     8 |         28 |         21 |
| personal_life    |   0 |           20 |     1 |         43 |          9 |
| science_tech     |   0 |           34 |    48 |         44 |         21 |
| society_politics |   0 |           18 |    11 |         37 |         15 |
| software_code    |   1 |           25 |     5 |         45 |         79 |


### interaction flags (count)

| track      |   subjective |   sensitive |   multiturn_implied |
|:-----------|-------------:|------------:|--------------------:|
| ?          |            0 |           0 |                   0 |
| AlpacaEval |           39 |          16 |                   4 |
| HC3        |           14 |          61 |                   8 |
| NoRobots   |           33 |          25 |                   4 |
| WildChat   |           44 |          80 |                  27 |
