# Step 1 — Claude n-gram signature (Fightin' Words log-odds)

Markdown stripped; z>0 = more Claude. Prior kappa=500, min total count 5.

## Interpretation (the discovered Claude signature)

Claude's lexical fingerprint here is **interactional, not the "delve" family** —
exactly the point JdR raised. Data-driven, the strongest Claudean terms are:

- **The offer-to-continue closing move (the single clearest Claudeism):** top
  trigrams are "would you like", "like me to", "me to explain", "in more detail",
  "to go deeper", "any specific aspect", "me to go", "deeper into any". I.e.
  *"Would you like me to explain any of these in more detail / go deeper into any
  specific aspect?"* — a recap-and-offer closer the other sources rarely produce.
- **Second-person engagement + framing:** "you", "you're", "let me", "think of
  it", "how it works", "this is".
- **Conversational markers:** "actually", "like", "no", "don't".

The **anti-signature** (what Claude uses *less* than others) is just as telling:

- **Formal hedge-frames:** "it is important to", "is important to", "it's
  important to" — a classic GPT/ChatGPT frame; here it is markedly *anti-Claude*.
- **Formal deferral phrasing:** "your healthcare provider", "a healthcare
  professional" (more GPT / old-ChatGPT).
- **Function-word-heavy connectives:** "of", "and", "to", "the", "can be", "such
  as", "a variety of" — corroborating that Claude's prose is *denser in content
  words* (lower function-word rate).

So Claude does have a genuine n-gram signature; it is **engagement- and
offer-oriented**, and it specifically *avoids* the formal "it is important
to"/"crucial to" register that characterizes GPT.

---


## Contrast: claude_vs_pooled


### 1-gram — most Claude-like

| term     |     z |   claude_ct |   other_ct |
|:---------|------:|------------:|-----------:|
| me       | 11.85 |         152 |         24 |
| what     | 11.06 |         200 |        117 |
| you're   |  9.65 |         135 |         68 |
| why      |  8.87 |         102 |         43 |
| like     |  8.54 |         331 |        368 |
| explain  |  8.42 |          79 |         10 |
| would    |  8.34 |         153 |        116 |
| actually |  7.9  |          70 |         20 |
| how      |  7.85 |         174 |        155 |
| let      |  7.44 |          63 |         19 |
| key      |  7.09 |          74 |         38 |
| don't    |  7.05 |          76 |         41 |
| no       |  6.9  |          88 |         58 |
| common   |  6.83 |         102 |         77 |
| detail   |  6.63 |          48 |          7 |
| please   |  6.58 |          47 |         11 |
| real     |  6.47 |          71 |         43 |
| here's   |  6.39 |          51 |         20 |
| line     |  6.22 |          46 |         16 |
| you      |  6.16 |         707 |       1119 |


### 1-gram — least Claude-like (anti-signature)

| term   |      z |   claude_ct |   other_ct |
|:-------|-------:|------------:|-----------:|
| of     | -14.63 |         691 |       2707 |
| and    | -12.15 |        1043 |       3369 |
| to     | -11.89 |        1019 |       3279 |
| as     |  -9.44 |         186 |        846 |
| the    |  -9.22 |        1858 |       5012 |
| be     |  -8.57 |         188 |        798 |
| in     |  -8.23 |         528 |       1682 |
| also   |  -7.54 |          27 |        263 |
| that   |  -7.42 |         326 |       1102 |
| can    |  -7.28 |         294 |       1009 |
| is     |  -7.28 |         583 |       1746 |
| are    |  -7.04 |         271 |        933 |


### 2-gram — most Claude-like

| term           |    z |   claude_ct |   other_ct |
|:---------------|-----:|------------:|-----------:|
| me to          | 8.19 |          80 |          4 |
| would you      | 8.19 |         120 |          2 |
| let me         | 7.96 |          56 |          8 |
| this is        | 7.04 |          92 |         92 |
| to explain     | 6.75 |          45 |          4 |
| e g            | 6.66 |          39 |         13 |
| your doctor    | 6.3  |          42 |         23 |
| you like       | 5.99 |         119 |          0 |
| in more        | 5.67 |          31 |          3 |
| how it         | 5.4  |          25 |          7 |
| more detail    | 5.28 |          45 |          1 |
| what to        | 5.17 |          23 |          4 |
| it works       | 5.17 |          23 |          4 |
| great question | 5.15 |          28 |          2 |
| what you       | 5.03 |          27 |         15 |
| on any         | 4.94 |          21 |          6 |
| your brain     | 4.84 |          20 |          4 |
| to go          | 4.83 |          25 |         14 |
| like a         | 4.83 |          42 |         41 |
| think of       | 4.81 |          20 |          6 |


### 2-gram — least Claude-like (anti-signature)

| term                |     z |   claude_ct |   other_ct |
|:--------------------|------:|------------:|-----------:|
| it is               | -7.67 |          10 |        312 |
| of the              | -5.5  |         101 |        524 |
| important to        | -5.2  |           2 |        160 |
| can be              | -4.6  |          40 |        251 |
| you are             | -4.37 |           6 |        106 |
| used to             | -4.31 |           7 |        107 |
| in the              | -4.17 |         101 |        456 |
| is important        | -4    |           3 |         85 |
| they are            | -3.83 |           4 |         80 |
| such as             | -3.69 |          54 |        268 |
| healthcare provider | -3.67 |           6 |         81 |
| that is             | -3.4  |           5 |         69 |


### 3-gram — most Claude-like

| term                |    z |   claude_ct |   other_ct |
|:--------------------|-----:|------------:|-----------:|
| would you like      | 9.51 |         119 |          0 |
| like me to          | 7.37 |          72 |          0 |
| you like me         | 7.22 |          69 |          0 |
| me to explain       | 5.69 |          43 |          0 |
| in more detail      | 4.82 |          31 |          0 |
| see a doctor        | 4.75 |          18 |          5 |
| how it works        | 4.64 |          17 |          3 |
| to explain any      | 4.24 |          24 |          0 |
| any of these        | 4    |          13 |          4 |
| think of it         | 4    |          13 |          4 |
| to go deeper        | 3.97 |          21 |          0 |
| me to go            | 3.97 |          21 |          0 |
| here are the        | 3.89 |          12 |          3 |
| of it like          | 3.89 |          12 |          3 |
| any specific aspect | 3.87 |          20 |          0 |
| aspect such as      | 3.77 |          19 |          0 |
| deeper into any     | 3.77 |          19 |          0 |
| let me explain      | 3.67 |          18 |          0 |
| is there a          | 3.44 |          10 |          1 |
| is one of           | 3.41 |          10 |          4 |


### 3-gram — least Claude-like (anti-signature)

| term                      |     z |   claude_ct |   other_ct |
|:--------------------------|------:|------------:|-----------:|
| it is important           | -3.85 |           0 |         79 |
| is important to           | -3.59 |           1 |         70 |
| it's important to         | -3.34 |           1 |         61 |
| a variety of              | -2.93 |           0 |         46 |
| your healthcare provider  | -2.59 |           0 |         36 |
| to determine the          | -2.56 |           0 |         35 |
| a healthcare professional | -2.55 |           1 |         37 |
| be able to                | -2.41 |           0 |         31 |
| can lead to               | -2.33 |           0 |         29 |
| be used to                | -2.29 |           0 |         28 |
| it is also                | -2.29 |           0 |         28 |
| if you are                | -2.23 |           2 |         34 |


## Contrast: claude_vs_gpt4o


### 1-gram — most Claude-like

| term     |    z |   claude_ct |   other_ct |
|:---------|-----:|------------:|-----------:|
| you      | 9.1  |         707 |        366 |
| what     | 8.63 |         200 |         44 |
| would    | 7.65 |         153 |         32 |
| me       | 7.35 |         152 |          4 |
| why      | 6.19 |         102 |         22 |
| explain  | 5.77 |          79 |          4 |
| no       | 5.57 |          88 |         21 |
| don't    | 5.55 |          76 |         14 |
| actually | 5.53 |          70 |         10 |
| you're   | 5.28 |         135 |         53 |
| let      | 5.18 |          63 |         10 |
| how      | 5.17 |         174 |         80 |
| most     | 5.04 |         105 |         37 |
| common   | 4.87 |         102 |         37 |
| detail   | 4.59 |          48 |          3 |
| please   | 4.54 |          47 |          3 |
| about    | 4.51 |         131 |         60 |
| us       | 4.4  |          43 |          5 |
| line     | 4.26 |          46 |          9 |
| i        | 4.21 |          67 |         22 |


### 1-gram — least Claude-like (anti-signature)

| term       |      z |   claude_ct |   other_ct |
|:-----------|-------:|------------:|-----------:|
| and        | -10.76 |        1043 |       1478 |
| of         |  -8.44 |         691 |        969 |
| might      |  -8.4  |          54 |        184 |
| to         |  -7.95 |        1019 |       1307 |
| can        |  -7.55 |         294 |        476 |
| as         |  -6.87 |         186 |        324 |
| financial  |  -6.4  |          24 |         96 |
| healthcare |  -6.22 |          10 |         75 |
| s          |  -6.17 |          35 |        108 |
| provide    |  -5.95 |           8 |         68 |
| be         |  -5.69 |         188 |        296 |
| potential  |  -5.56 |          12 |         64 |


### 2-gram — most Claude-like

| term            |    z |   claude_ct |   other_ct |
|:----------------|-----:|------------:|-----------:|
| would you       | 6.25 |         120 |          0 |
| you like        | 6.22 |         119 |          0 |
| let me          | 5.36 |          56 |          3 |
| me to           | 5.09 |          80 |          0 |
| this is         | 4.94 |          92 |         39 |
| like me         | 4.83 |          72 |          0 |
| e g             | 4.49 |          39 |          6 |
| more detail     | 4.46 |          45 |          1 |
| in more         | 3.82 |          31 |          1 |
| to explain      | 3.82 |          45 |          0 |
| great question  | 3.67 |          28 |          1 |
| how it          | 3.65 |          25 |          2 |
| a specific      | 3.58 |          32 |          9 |
| specific aspect | 3.56 |          26 |          1 |
| what you        | 3.52 |          27 |          6 |
| what to         | 3.51 |          23 |          2 |
| to go           | 3.46 |          25 |          5 |
| it works        | 3.38 |          23 |          1 |
| your doctor     | 3.3  |          42 |         18 |
| on any          | 3.2  |          21 |          4 |


### 2-gram — least Claude-like (anti-signature)

| term                    |     z |   claude_ct |   other_ct |
|:------------------------|------:|------------:|-----------:|
| can be                  | -4.84 |          40 |        109 |
| it is                   | -4.33 |          10 |         50 |
| important to            | -4.2  |           2 |         40 |
| a healthcare            | -4    |           7 |         40 |
| used to                 | -3.85 |           7 |         38 |
| to ensure               | -3.74 |           2 |         31 |
| such as                 | -3.71 |          54 |        111 |
| can provide             | -3.68 |           3 |         30 |
| they can                | -3.54 |           7 |         34 |
| healthcare professional | -3.54 |           1 |         30 |
| healthcare provider     | -3.52 |           6 |         32 |
| lead to                 | -3.44 |           1 |         28 |


### 3-gram — most Claude-like

| term                 |    z |   claude_ct |   other_ct |
|:---------------------|-----:|------------:|-----------:|
| would you like       | 7.96 |         119 |          0 |
| like me to           | 6.14 |          72 |          0 |
| you like me          | 6    |          69 |          0 |
| me to explain        | 4.72 |          43 |          0 |
| in more detail       | 4    |          31 |          0 |
| to explain any       | 3.51 |          24 |          0 |
| to go deeper         | 3.28 |          21 |          0 |
| me to go             | 3.28 |          21 |          0 |
| any specific aspect  | 3.2  |          20 |          0 |
| deeper into any      | 3.12 |          19 |          0 |
| aspect such as       | 3.12 |          19 |          0 |
| let me explain       | 3.04 |          18 |          0 |
| how it works         | 2.87 |          17 |          1 |
| you like help        | 2.77 |          15 |          0 |
| go deeper into       | 2.77 |          15 |          0 |
| specific aspect such | 2.68 |          14 |          0 |
| see a doctor         | 2.6  |          18 |          3 |
| you like more        | 2.48 |          12 |          0 |
| more detail on       | 2.48 |          12 |          0 |
| question let me      | 2.48 |          12 |          0 |


### 3-gram — least Claude-like (anti-signature)

| term                      |     z |   claude_ct |   other_ct |
|:--------------------------|------:|------------:|-----------:|
| a healthcare professional | -4.09 |           1 |         29 |
| it's important to         | -3.71 |           1 |         24 |
| here are some             | -3.62 |           4 |         27 |
| not a doctor              | -3.32 |           0 |         19 |
| a doctor but              | -3.32 |           0 |         19 |
| your healthcare provider  | -3.23 |           0 |         18 |
| can lead to               | -3.23 |           0 |         18 |
| i'm not a                 | -3    |           3 |         19 |
| are a few                 | -2.95 |           2 |         17 |
| here are a                | -2.95 |           0 |         15 |
| the development of        | -2.78 |           1 |         14 |
| doctor but i              | -2.74 |           0 |         13 |
