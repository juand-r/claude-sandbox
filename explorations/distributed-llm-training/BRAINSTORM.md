# Distributed LLM Training via Claude Code Web Sessions

## The Idea

Launch 10-100 Claude Code web sessions (each on a separate sandboxed machine),
same repo. Each runs a small LLM training run. Merge results. Repeat.

This is essentially **federated learning using Claude Code sessions as compute nodes**.

---

## Honest Feasibility Assessment

### The Hard Problems

**1. No GPUs (likely dealbreaker for LLM-scale work)**

Claude Code web sessions are sandboxed containers designed for coding. They
almost certainly don't have GPU access. LLM training on CPU is orders of
magnitude slower. Even a 100M parameter model would crawl.

What you *could* train on CPU in a reasonable time:
- Sub-10M parameter models (toy transformers, small LSTMs)
- Maybe a small GPT-2-like model (124M params) for a few steps, not full training
- LoRA/QLoRA fine-tuning of a frozen small model (still slow without GPU)

**2. Resource Limits**

Each session has CPU, memory, and time constraints. Training runs need to fit
within whatever those limits are (likely ~30 min to a few hours, unclear RAM
ceiling, probably 4-16GB).

**3. No Direct Networking Between Sessions**

Sessions can't talk to each other. Communication must go through the git repo
(push/pull). This is very high-latency "networking" -- minutes per round trip.
Traditional distributed training needs millisecond-level communication for
gradient sync. This rules out synchronous approaches entirely.

**4. Orchestration**

Who launches the 100 sessions? Who tells each one what to do? Who monitors
them? Claude Code web is interactive -- there's no batch API to spin up N
sessions programmatically (as far as I know).

**5. Cost & ToS**

Using coding sessions as a compute cluster is almost certainly not the intended
use. And if each session costs API credits, 100 sessions x training time adds up
fast relative to just renting GPU time on Lambda/Vast/RunPod.

### What Actually Works Given These Constraints

If we accept the limitations (CPU-only, small models, high-latency
communication, manual-ish orchestration), here's what the idea reduces to:

**Asynchronous federated learning on toy-scale models, coordinated via git.**

This is actually a well-defined and somewhat interesting research direction,
just not for practical LLM training.

---

## Approaches for Merging

Assuming each node independently trains a model (or partial model), here are
the merging strategies, ranked by promise:

### 1. FedAvg (Federated Averaging)
- Each node trains on a data shard for E local epochs
- Push model weights to repo
- Orchestrator averages the weights
- Push averaged model back, repeat
- **Proven to work.** McMahan et al. 2017.
- Problem: with high-latency git communication, each "round" takes a long time.

### 2. Model Souping / Weight Averaging
- Train N models independently (different data, different hyperparams, or
  different random seeds)
- Average all the weights at the end
- Wortsman et al. 2022 showed this works surprisingly well
- Simpler than FedAvg -- only one merge step at the end
- **Most practical for this setup** since it doesn't need frequent communication

### 3. TIES-Merging / DARE
- More sophisticated merge strategies for combining independently fine-tuned models
- Trim redundant parameters, resolve sign conflicts, then merge
- Better than naive averaging when models diverge significantly
- Yadav et al. 2023 (TIES), Yu et al. 2024 (DARE)

### 4. Local SGD / Post-Local SGD
- Like FedAvg but with less frequent communication
- Fits the high-latency constraint
- Lin et al. 2020

### 5. Population-Based Training (PBT)
- Each node trains with different hyperparameters
- Periodically, bad performers copy weights from good performers
- Good use of parallelism even without merging
- Jaderberg et al. 2017

---

## What Would Be Worth Building (If We Do This)

A **proof of concept** that demonstrates:

1. A small transformer (e.g., character-level GPT, ~1-5M params)
2. Training data split across N workers
3. Each worker trains locally for K steps
4. Weights are serialized and committed to git
5. A merge script combines them (FedAvg or model soup)
6. Merged model is distributed back for next round

This can all run on **one machine** to prove the concept (simulate the
distributed part). No need to actually spin up 100 sessions to validate the
approach.

**Scale**: character-level language model on a small text corpus. Shakespeare,
wiki snippets, something manageable.

---

## Verdict

| Aspect | Rating | Notes |
|--------|--------|-------|
| Novelty | Medium | Federated learning via git is a funny twist, but the ML is well-trodden |
| Feasibility (toy scale) | High | Totally doable with small models on CPU |
| Feasibility (real LLM) | Very Low | No GPUs, too slow, wrong tool for the job |
| Learning value | High | Covers distributed training, model merging, federated learning |
| Practical utility | Low | You'd use actual GPU clusters for real work |
| Fun factor | High | It's a weird and interesting hack |

**Bottom line**: As a learning exercise and proof-of-concept, this is solid.
You'll learn about federated learning, model merging, and distributed
coordination. As a practical training strategy, it doesn't compete with a
single A100 for 10 minutes. The model size ceiling is probably sub-10M params
if you want training to finish in a reasonable time per session.

**Recommendation**: Build the proof-of-concept locally first (simulated
workers, one machine). If it works and is interesting, *then* consider whether
the multi-session orchestration is worth the effort.

---

## Open Questions

- What are the actual resource limits of Claude Code web sessions? (CPU cores,
  RAM, time limit, disk)
- Is there an API or programmatic way to launch multiple sessions?
- What's the actual use case -- learning federated learning, or genuinely
  trying to train something useful?
- What model/task do you care about?
