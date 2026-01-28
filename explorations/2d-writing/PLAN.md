# 2D Writing System

## Goal
Generate a 5x5 word grid where:
- Each row is a coherent English sentence/phrase
- Each column is also a coherent English sentence/phrase

## Approach

### Core Idea
Use log probabilities from a small LM (GPT-2) to score how "natural" a sequence of words is.
Optimize the grid to maximize total score across all rows AND columns.

### Algorithm Options

1. **Greedy with backtracking** - Fill cell by cell, backtrack when stuck
2. **Beam search** - Maintain top-k partial grids, expand best candidates
3. **MCMC / Gibbs sampling** - Start with random grid, iteratively improve by resampling words
4. **Iterative refinement** - Generate rows first, then adjust to improve columns

### Starting Point
Try **Gibbs sampling**:
1. Initialize grid with random common words
2. For each cell, resample the word conditioned on making both its row and column more coherent
3. Repeat until convergence or max iterations

This is simple to implement and naturally handles the bidirectional constraints.

### Scoring
For a sequence of words [w1, w2, ..., wn]:
- Score = sum of log P(wi | w1...w(i-1)) for each word
- Higher = more natural/fluent

Total grid score = sum of all row scores + sum of all column scores

## Tasks
- [x] Create project structure
- [ ] Implement basic LM scoring with GPT-2
- [ ] Implement grid data structure
- [ ] Implement Gibbs sampler
- [ ] Test and iterate

## Notes
- GPT-2 small (124M params) should be fast enough
- May need to constrain vocabulary to common words
- Quality will likely be rough at first - this is exploratory
