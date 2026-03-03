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
- [x] Baseline trains and converges (822K params, val PPL 6.52, 978s)
- [x] Swarm trains and converges (615K params, val PPL 6.68, 2290s)
- [x] Compare final validation loss

## Results (500 steps, batch=64, context=128, lr=3e-3)

| | Baseline | Swarm (5 models, 2 rounds) |
|---|---------|---------------------------|
| Params | 822,144 | 614,725 |
| Val PPL | **6.52** | 6.68 |
| Val Loss | **1.8744** | 1.8990 |
| Time | 978s | 2290s |
| s/step | 1.96 | 4.58 |

Swarm aggregation weights: [0.181, 0.176, 0.166, 0.234, 0.243]

**Key finding**: Swarm nearly matches baseline despite 25% fewer params. Message passing adds value beyond raw param count. But 2.3x slower per step.

## Next steps
- [ ] Fair comparison: match total param counts (scale up swarm models)
- [ ] Ablation: swarm without messages (just ensemble) vs with messages
- [ ] Longer training runs to see if gap widens or closes
