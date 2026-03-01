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
| Feasibility (medium scale) | Medium | 50-150M params feasible with AMX/IPEX per session |
| Feasibility (real LLM, >1B) | Low | Full training too slow, but LoRA fine-tuning possible |
| Learning value | High | Covers distributed training, model merging, federated learning |
| Practical utility | Medium | 10-100 sessions = real CPU cluster, useful for some workloads |
| Fun factor | High | It's a weird and interesting hack |

**Bottom line**: Better than initially expected. Each session is a 16-core
AMX-enabled Xeon with 21GB RAM -- a real compute node, not a toy. For
small-to-medium models (up to ~150M params), distributed training via model
merging is genuinely feasible. For larger models, LoRA fine-tuning is an option.
Still can't compete with GPUs for raw training throughput, but the parallelism
(10-100 independent nodes) partially compensates.

**Recommendation**: Build the proof-of-concept locally first (simulated
workers, one machine). Benchmark AMX/IPEX performance to calibrate expectations.
If throughput is reasonable, the multi-session approach becomes genuinely
interesting -- not just as a learning exercise but as a practical (if eccentric)
training strategy.

---

## Measured Resource Limits (Claude Code Web Session, 2026-03-01)

Probed from inside a live session:

| Resource | Value | Notes |
|----------|-------|-------|
| **CPU cores** | 16 | Physical cores, 1 thread/core (no hyperthreading) |
| **CPU model** | Intel (family 6, model 207) | Emerald Rapids or Granite Rapids Xeon |
| **CPU clock** | 2.1 GHz | |
| **RAM** | 21 GB total | ~20 GB available |
| **Disk** | 30 GB | Mounted at / |
| **GPU** | None | No nvidia-smi, no /dev/dri |
| **Swap** | None | 0 B |
| **Internet** | Yes | Can pip install packages |
| **Python** | 3.11.14 | pip available |
| **PyTorch** | Not installed | Can be installed via pip |
| **AVX-512** | Yes | Full suite: F, DQ, CD, BW, VL, VBMI, VBMI2, VNNI, BITALG, VPOPCNTDQ, FP16 |
| **AMX** | Yes | BF16, INT8, TILE -- Intel Advanced Matrix Extensions |
| **VNNI** | Yes | Vector Neural Network Instructions |
| **ulimits** | Generous | No CPU time limit, unlimited processes, unlimited virtual memory |
| **Session timeout** | Unknown | Need to test empirically |

### Key Takeaway: Better Than Expected

This is a **beefy machine** for CPU work. The critical findings:

1. **16 cores with AVX-512 and AMX** -- these are serious instructions for
   matrix math. AMX (Advanced Matrix Extensions) is Intel's answer to GPU
   tensor cores for CPU. It can do BF16 and INT8 matrix multiplies in hardware.

2. **21 GB RAM** -- enough to hold a 1-2B parameter model in memory (in fp32,
   ~4 bytes/param, so ~500M params fit in 2GB, ~5B params in 20GB at fp32,
   much more at bf16/int8).

3. **Internet access** -- can pip install PyTorch, transformers, etc.

4. **No hard CPU time limit** in ulimits -- the session timeout is the
   constraint, not a process kill.

### Revised Model Size Estimates

With AMX/AVX-512 and 16 cores, CPU training is much more viable than I
initially assumed:

- PyTorch with Intel Extension for PyTorch (IPEX) can leverage AMX for BF16
  training, which is a significant speedup over vanilla FP32.
- oneDNN (MKL-DNN) backend in PyTorch already uses AVX-512 VNNI.
- Realistic training targets (per session, per round):
  - **10-50M params**: Comfortable. Multiple epochs on small datasets.
  - **50-150M params**: Feasible for a few hundred steps with IPEX/AMX.
  - **150M-500M params**: Possible for LoRA/QLoRA fine-tuning (frozen base).
  - **500M+**: Forward passes yes, full training probably too slow.

### Revised Verdict

The "no GPU = toy only" assessment was too pessimistic. With AMX-enabled Xeons,
16 cores, and 21GB RAM, each session is a legitimate compute node for
small-to-medium model training. This pushes the idea from "cute hack" toward
"might actually be interesting."

The parallelism angle becomes compelling: 10 sessions = 160 cores, 210 GB RAM.
100 sessions = 1600 cores, 2.1 TB RAM. That's a respectable CPU cluster,
especially for inference, hyperparameter search, and model merging experiments.

---

## Open Questions

- What is the actual session timeout? (Need to test empirically)
- Is there an API or programmatic way to launch multiple sessions?
- What's the actual use case -- learning federated learning, or genuinely
  trying to train something useful?
- What model/task do you care about?
- How fast is AMX BF16 matmul on this hardware? (Should benchmark)
