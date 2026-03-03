# Swarm LLM

Can a swarm of small communicating transformers match a single larger transformer with the same total parameters?

## The idea

Instead of one ~800K-param model, train 5 x ~120K-param models that exchange learned messages between forward passes. Each communication round lets models share compressed information about what they've learned from the input.

## How to run

```bash
cd explorations/swarm-llm
pip install torch
python train.py --mode baseline   # single ~800K model
python train.py --mode swarm      # 5-model swarm with message passing
```

## Key question

Does the swarm match or beat the baseline on character-level language modeling (Shakespeare)?
