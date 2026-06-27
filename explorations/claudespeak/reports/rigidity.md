# Register rigidity (reproducible: src/analyze_rigidity.py)

eta^2 = fraction of a source's style variance explained by the task/context grouping. **Lower eta^2 = more rigid** (context barely moves the style); higher = adapts style to context. Style features standardized within each track; CIs are 95% bootstrap.


## PROSE-only, length-controlled


**HC3** (axis: domain, 4 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |   n |
|:----------------|-------:|--------:|--------:|----:|
| human           |  0.038 |   0.031 |   0.088 | 200 |
| gpt-4o          |  0.089 |   0.074 |   0.154 | 200 |
| claude-opus-4-8 |  0.11  |   0.092 |   0.167 | 200 |
| chatgpt-hc3     |  0.11  |   0.089 |   0.17  | 200 |


**AlpacaEval** (axis: domain, 5 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source                    |   eta2 |   ci_lo |   ci_hi |   n |
|:--------------------------|-------:|--------:|--------:|----:|
| gemini-pro                |  0.015 |   0.019 |   0.047 | 200 |
| Qwen2-72B-Instruct        |  0.017 |   0.022 |   0.046 | 200 |
| gpt-4o-2024-05-13         |  0.022 |   0.027 |   0.061 | 200 |
| claude-opus-4-8           |  0.024 |   0.027 |   0.058 | 200 |
| Meta-Llama-3-70B-Instruct |  0.025 |   0.028 |   0.059 | 200 |
| gpt-4-turbo-2024-04-09    |  0.028 |   0.029 |   0.069 | 200 |
| deepseek-llm-67b-chat     |  0.034 |   0.03  |   0.081 | 200 |


**NoRobots** (axis: task_type, 10 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |    n |
|:----------------|-------:|--------:|--------:|-----:|
| claude-opus-4-8 |  0.062 |   0.057 |   0.081 | 1500 |
| human           |  0.078 |   0.071 |   0.104 | 1500 |


## PROSE-only


**HC3** (axis: domain, 4 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |   n |
|:----------------|-------:|--------:|--------:|----:|
| human           |  0.064 |   0.048 |   0.123 | 200 |
| gpt-4o          |  0.108 |   0.084 |   0.178 | 200 |
| claude-opus-4-8 |  0.11  |   0.092 |   0.167 | 200 |
| chatgpt-hc3     |  0.116 |   0.095 |   0.175 | 200 |


**AlpacaEval** (axis: domain, 5 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source                    |   eta2 |   ci_lo |   ci_hi |   n |
|:--------------------------|-------:|--------:|--------:|----:|
| Qwen2-72B-Instruct        |  0.025 |   0.028 |   0.058 | 200 |
| claude-opus-4-8           |  0.026 |   0.029 |   0.06  | 200 |
| gemini-pro                |  0.029 |   0.029 |   0.061 | 200 |
| gpt-4o-2024-05-13         |  0.031 |   0.033 |   0.072 | 200 |
| Meta-Llama-3-70B-Instruct |  0.032 |   0.033 |   0.065 | 200 |
| deepseek-llm-67b-chat     |  0.036 |   0.031 |   0.081 | 200 |
| gpt-4-turbo-2024-04-09    |  0.038 |   0.035 |   0.078 | 200 |


**NoRobots** (axis: task_type, 10 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |    n |
|:----------------|-------:|--------:|--------:|-----:|
| claude-opus-4-8 |  0.084 |   0.075 |   0.106 | 1500 |
| human           |  0.125 |   0.108 |   0.16  | 1500 |


## ALL style feats, length-controlled


**HC3** (axis: domain, 4 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |   n |
|:----------------|-------:|--------:|--------:|----:|
| human           |  0.045 |   0.038 |   0.097 | 200 |
| claude-opus-4-8 |  0.084 |   0.074 |   0.132 | 200 |
| gpt-4o          |  0.091 |   0.075 |   0.147 | 200 |
| chatgpt-hc3     |  0.11  |   0.09  |   0.17  | 200 |


**AlpacaEval** (axis: domain, 5 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source                    |   eta2 |   ci_lo |   ci_hi |   n |
|:--------------------------|-------:|--------:|--------:|----:|
| gemini-pro                |  0.019 |   0.023 |   0.05  | 200 |
| Qwen2-72B-Instruct        |  0.021 |   0.025 |   0.05  | 200 |
| Meta-Llama-3-70B-Instruct |  0.025 |   0.028 |   0.055 | 200 |
| gpt-4o-2024-05-13         |  0.026 |   0.031 |   0.061 | 200 |
| claude-opus-4-8           |  0.027 |   0.029 |   0.06  | 200 |
| gpt-4-turbo-2024-04-09    |  0.03  |   0.032 |   0.068 | 200 |
| deepseek-llm-67b-chat     |  0.036 |   0.033 |   0.08  | 200 |


**NoRobots** (axis: task_type, 10 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |    n |
|:----------------|-------:|--------:|--------:|-----:|
| human           |  0.086 |   0.077 |   0.111 | 1500 |
| claude-opus-4-8 |  0.138 |   0.119 |   0.17  | 1500 |


## ALL style feats


**HC3** (axis: domain, 4 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |   n |
|:----------------|-------:|--------:|--------:|----:|
| human           |  0.064 |   0.049 |   0.124 | 200 |
| claude-opus-4-8 |  0.087 |   0.077 |   0.136 | 200 |
| chatgpt-hc3     |  0.117 |   0.095 |   0.175 | 200 |
| gpt-4o          |  0.123 |   0.093 |   0.19  | 200 |


**AlpacaEval** (axis: domain, 5 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source                    |   eta2 |   ci_lo |   ci_hi |   n |
|:--------------------------|-------:|--------:|--------:|----:|
| Qwen2-72B-Instruct        |  0.027 |   0.029 |   0.059 | 200 |
| claude-opus-4-8           |  0.027 |   0.029 |   0.06  | 200 |
| gemini-pro                |  0.031 |   0.032 |   0.064 | 200 |
| gpt-4o-2024-05-13         |  0.033 |   0.036 |   0.069 | 200 |
| Meta-Llama-3-70B-Instruct |  0.034 |   0.035 |   0.066 | 200 |
| deepseek-llm-67b-chat     |  0.036 |   0.032 |   0.078 | 200 |
| gpt-4-turbo-2024-04-09    |  0.037 |   0.037 |   0.073 | 200 |


**NoRobots** (axis: task_type, 10 groups) — sorted by rigidity (lowest eta^2 = most rigid):

| source          |   eta2 |   ci_lo |   ci_hi |    n |
|:----------------|-------:|--------:|--------:|-----:|
| human           |  0.127 |   0.111 |   0.16  | 1500 |
| claude-opus-4-8 |  0.159 |   0.14  |   0.191 | 1500 |
