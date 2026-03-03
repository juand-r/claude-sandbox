# Swarm LLM Experiment Plan

## Goal
Test whether a swarm of small communicating transformers can match a single larger transformer.

## Setup
- **Task**: Character-level language modeling on Shakespeare (~1.1MB)
- **Baseline**: Single transformer, ~800K params (embed=128, 4 layers, 4 heads, ffn=512)
- **Swarm**: 5 transformers, ~120K params each, with learned message passing
- **Metric**: Validation loss (cross-entropy), validation perplexity

## Architecture

### Swarm communication
1. All models embed input independently
2. Round 0: each model does a forward pass, produces a message (mean-pool + linear proj)
3. Rounds 1-R: each model gets other models' messages as prefix tokens, forward pass, new message
4. Final: learned weighted sum of all models' logits

## Status
- [x] Code written
- [ ] Baseline trains and converges
- [ ] Swarm trains (gradients flow through messages)
- [ ] Compare final validation loss
