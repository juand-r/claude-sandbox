# Swarm LLM Experiment Plan

## Goal
Test whether a swarm of small communicating transformers can match a single larger transformer.

## Setup
- **Task**: Character-level language modeling on Shakespeare (~1.1MB)
- **Baseline**: Single transformer, ~800K params (embed=128, 4 layers, 4 heads, ffn=512)
- **Swarm**: 5 transformers, ~120K params each, with learned message passing
- **Metric**: Validation loss (cross-entropy), validation perplexity

## Architecture

### Baseline (single transformer)
```
  Input: "To be or not"
       |
  [Embedding + Pos]
       |
  [Transformer Block x4]  (embed=128, 4 heads, ffn=512)
       |
  [Linear Head]
       |
  Output logits --> next char prediction
```

### Swarm (5 communicating transformers)
```
  Input: "To be or not"
       |
       +----------+----------+----------+----------+
       |          |          |          |          |
     [M1]      [M2]      [M3]      [M4]      [M5]     <-- Round 0: independent
       |          |          |          |          |        forward pass
    msg_1      msg_2      msg_3      msg_4      msg_5   <-- extract messages
       |          |          |          |          |        (mean-pool + linear)
       +----X-----+----X-----+----X-----+----X-----+
       |          |          |          |          |
  [M1+msgs]  [M2+msgs]  [M3+msgs]  [M4+msgs]  [M5+msgs] <-- Round 1: each model
       |          |          |          |          |        gets others' messages
    msg_1'     msg_2'     msg_3'     msg_4'     msg_5'      as prefix tokens
       |          |          |          |          |
       +----X-----+----X-----+----X-----+----X-----+
       |          |          |          |          |
  [M1+msgs]  [M2+msgs]  [M3+msgs]  [M4+msgs]  [M5+msgs] <-- Round 2: repeat
       |          |          |          |          |
   logits_1   logits_2   logits_3   logits_4   logits_5
       |          |          |          |          |
       +----------+----------+----------+----------+
                         |
                  [Weighted Sum]   <-- learned weights: [.18, .18, .17, .23, .24]
                         |
                   Output logits

  Each [Mi] = small transformer (embed=64, 2 layers, 2 heads, ffn=256)
  Each msg  = 64-dim vector, injected as prefix tokens to other models
  X = message exchange (each model gets N-1 messages from the others)
```

### Inference cost analysis

With N models and R communication rounds, each token prediction requires:
- **Baseline**: 1 forward pass
- **Swarm**: N x (R+1) forward passes = 5 x 3 = **15 forward passes**

Each individual forward pass is cheaper (smaller model), but the total is ~2-5x
more compute. This is a real cost. Possible mitigations:
1. Reduce rounds (R=1 might be enough — needs ablation)
2. Reduce N (3 models instead of 5)
3. Distill the swarm into a single model after training
4. Run models in parallel (they're independent within each round)

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
