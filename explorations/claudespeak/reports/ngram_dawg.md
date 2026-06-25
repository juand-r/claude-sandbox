# Step 5 — rusty-dawg / suffix-automaton n-gram mining

Markdown-stripped prose, word-level tokens. Built with AI2 rusty-dawg (pip rusty_dawg 0.2.2).

## Conclusion

The arbitrary-length suffix-automaton mining gives the strongest, most concrete
form of the signature.

1. **Exact long templates unique to Claude.** Multi-word spans up to **8-grams**
   that Claude produces dozens of times and that occur **ZERO times across humans
   + all six other models combined**:
   - HC3: "would you like me to explain any" (×20), "would you like me to go
     deeper into" (×14).
   - AlpacaEval (vs 6 modern models): "would you like me to go deeper on" (×7),
     "would you like me to expand on any" (×7), "is there a particular" (×8).
   This is the offer-to-continue closer (Step 1) confirmed as a verbatim template
   no other source ever emits — the single most diagnostic Claudeism found.

2. **Claude has the highest n-gram novelty of every source.** Fraction of a
   source's n-grams absent from the pooled others (higher = phrasing overlaps less
   with the pool):
   - AlpacaEval: Claude leads at every n (bigram novelty 0.519 vs 0.27–0.36 for
     the six others) — its word sequences overlap least with the other-model pool.
   - HC3: Claude's bigram novelty (0.583) exceeds even the human's (0.524).
   Claude's exact phrasing is the most distinctive in the set.

**Caveat on novelty.** "Novelty" is measured *relative to the other sources in our
corpus*, not against a large external reference. The six AlpacaEval models may
share phrasing with each other (similar instruction tuning / GPT-distillation),
which lowers their mutual novelty and makes Claude — the one outsider, and the
only freshly-generated source — look more novel partly by being the odd one out.
Read it as "Claude's phrasing separates from this pool," corroborating the
classifier and effect-size results from an information-theoretic angle, not as a
claim of absolute creativity.


## HC3 (human-anchored)

### n-gram novelty by source (fraction of source n-grams absent from pooled others)

Lower = more recombined-from-others; higher = more novel spans.

| source          |    n1 |    n2 |    n3 |    n4 |    n5 |    n6 |    n8 |   n10 |
|:----------------|------:|------:|------:|------:|------:|------:|------:|------:|
| chatgpt-hc3     | 0.024 | 0.362 | 0.744 | 0.904 | 0.955 | 0.974 | 0.993 | 0.997 |
| claude-opus-4-8 | 0.053 | 0.583 | 0.889 | 0.96  | 0.983 | 0.989 | 0.997 | 0.999 |
| gpt-4o          | 0.027 | 0.469 | 0.815 | 0.927 | 0.966 | 0.979 | 0.992 | 0.996 |
| human           | 0.066 | 0.524 | 0.878 | 0.964 | 0.986 | 0.99  | 0.995 | 0.997 |

### Characteristic long Claude spans (Claude count >=3, ZERO occurrences in pooled non-Claude)

|   n |   claude_count | span                                |
|----:|---------------:|:------------------------------------|
|   5 |             69 | would you like me to                |
|   4 |             69 | would you like me                   |
|   4 |             69 | you like me to                      |
|   4 |             36 | like me to explain                  |
|   6 |             33 | would you like me to explain        |
|   5 |             33 | you like me to explain              |
|   4 |             24 | me to explain any                   |
|   6 |             21 | would you like me to go             |
|   5 |             21 | you like me to go                   |
|   4 |             21 | like me to go                       |
|   7 |             20 | would you like me to explain any    |
|   7 |             20 | would you like me to go deeper      |
|   6 |             20 | you like me to explain any          |
|   6 |             20 | you like me to go deeper            |
|   5 |             20 | like me to explain any              |
|   5 |             20 | like me to go deeper                |
|   4 |             20 | me to go deeper                     |
|   4 |             15 | would you like help                 |
|   8 |             14 | would you like me to go deeper into |
|   8 |             14 | you like me to go deeper into any   |
|   7 |             14 | you like me to go deeper into       |
|   7 |             14 | like me to go deeper into any       |
|   6 |             14 | like me to go deeper into           |
|   6 |             14 | me to go deeper into any            |
|   5 |             14 | me to go deeper into                |


## AlpacaEval (modern models)

### n-gram novelty by source (fraction of source n-grams absent from pooled others)

Lower = more recombined-from-others; higher = more novel spans.

| source                    |    n1 |    n2 |    n3 |    n4 |    n5 |    n6 |    n8 |   n10 |
|:--------------------------|------:|------:|------:|------:|------:|------:|------:|------:|
| Meta-Llama-3-70B-Instruct | 0.025 | 0.34  | 0.683 | 0.838 | 0.907 | 0.948 | 0.975 | 0.986 |
| Qwen2-72B-Instruct        | 0.017 | 0.317 | 0.665 | 0.828 | 0.898 | 0.939 | 0.969 | 0.982 |
| claude-opus-4-8           | 0.034 | 0.519 | 0.835 | 0.928 | 0.961 | 0.977 | 0.989 | 0.994 |
| deepseek-llm-67b-chat     | 0.012 | 0.266 | 0.604 | 0.789 | 0.881 | 0.929 | 0.965 | 0.98  |
| gemini-pro                | 0.023 | 0.329 | 0.686 | 0.85  | 0.92  | 0.955 | 0.979 | 0.99  |
| gpt-4-turbo-2024-04-09    | 0.018 | 0.36  | 0.709 | 0.852 | 0.913 | 0.948 | 0.973 | 0.988 |
| gpt-4o-2024-05-13         | 0.019 | 0.333 | 0.67  | 0.83  | 0.895 | 0.935 | 0.968 | 0.983 |

### Characteristic long Claude spans (Claude count >=3, ZERO occurrences in pooled non-Claude)

|   n |   claude_count | span                               |
|----:|---------------:|:-----------------------------------|
|   4 |             13 | me to go deeper                    |
|   7 |             12 | would you like me to go deeper     |
|   6 |             12 | would you like me to go            |
|   6 |             12 | you like me to go deeper           |
|   5 |             12 | you like me to go                  |
|   5 |             12 | like me to go deeper               |
|   4 |             12 | like me to go                      |
|   6 |             10 | would you like me to expand        |
|   5 |             10 | you like me to expand              |
|   4 |             10 | like me to expand                  |
|   5 |              8 | me to go deeper on                 |
|   4 |              8 | to go deeper on                    |
|   4 |              8 | would you like more                |
|   4 |              8 | is there a particular              |
|   8 |              7 | would you like me to go deeper on  |
|   8 |              7 | would you like me to expand on any |
|   7 |              7 | you like me to go deeper on        |
|   7 |              7 | would you like me to expand on     |
|   7 |              7 | you like me to expand on any       |
|   6 |              7 | like me to go deeper on            |
|   6 |              7 | me to go deeper on any             |
|   6 |              7 | you like me to expand on           |
|   6 |              7 | like me to expand on any           |
|   5 |              7 | to go deeper on any                |
|   5 |              7 | like me to expand on               |
