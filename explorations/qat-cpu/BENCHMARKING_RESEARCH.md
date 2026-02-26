# QAT / Quantized Training Benchmarking Research

How papers and repos benchmark quantized training performance and quality.

---

## 1. Training Speed Metrics

### Tokens per Second (tokens/s)
The most common raw throughput metric. Directly measures how fast the system consumes training data.

- **nanoGPT**: Reports `iter N: loss X.XXXX, time XXXms` per iteration, and documents tokens/iter (e.g., 32,768 tokens/iter on a single GPU, 491,520 tokens/iter for 8xA100 GPT-2 training).
- **LLM.c**: ~1.8M tokens/sec on 8xH100 for GPT-2 124M (10B tokens in ~90 min).
- **nanoGPT speedrun**: Reports tokens/sec explicitly. ~160-216k tok/s on RTX 4090 setups.
- **BitNet b1.58 70B**: 2977 tokens/s inference throughput (8.9x over FP16 baseline). Note: BitNet papers report *inference* throughput, not training throughput.

**Caveat**: Tokens/s is not comparable across tokenizers. A model with a larger vocabulary produces fewer tokens for the same text. This is why BPB exists (see below).

### Model FLOPS Utilization (MFU)
The ratio of observed throughput to theoretical peak throughput. Hardware-agnostic efficiency metric.

```
MFU = observed_FLOPS / theoretical_peak_FLOPS
```

Where:
```
flops_per_token = 2 * N_params           (forward pass)
flops_per_step  = 6 * N_params * tokens_per_step  (fwd + bwd + optimizer)
observed_FLOPS  = flops_per_step / step_time_seconds
```

Typical values:
- GPT-3: 21.3% MFU
- PaLM: 46.2% MFU
- Llama-3.1: 38-43% MFU
- MegaScale (175B, 12288 GPUs): 55.2% MFU
- Most LLM trainings: 35-45%

**nanochat** (Karpathy) monitors: `val_bpb`, `total_training_time`, `total_training_flops`.

### Hardware FLOPS Utilization (HFU)
Like MFU but accounts for implementation details (e.g., activation recomputation). HFU >= MFU. Less comparable across implementations.

### Wall-Clock Time
The nanoGPT speedrun defines its benchmark as: *minimize wall-clock time to reach a fixed validation loss target on fixed hardware*. Target: val loss <= 3.28 on FineWeb, on 8xH100.

### Samples per Second
Less common for LLMs (more common in vision). Equivalent to tokens/s divided by sequence length.

---

## 2. Quality Metrics

### Cross-Entropy Loss (nats)
The raw training/validation loss. What every framework computes natively. Measured in nats (natural log base e).

```
CE = -(1/N) * sum( ln p(x_i | x_{<i}) )
```

This is what nanoGPT and LLM.c report directly.

### Perplexity (PPL)
The exponential of cross-entropy loss. Lower is better.

```
PPL = exp(CE)
```

Where CE is the average per-token cross-entropy in nats.

**This is the dominant quality metric in quantization papers.**

- **GPTQ**: Reports WikiText-2 perplexity. OPT-175B: FP16=8.34, GPTQ-4bit=8.37, RTN-4bit=10.54.
- **QLoRA**: Reports perplexity for NF4 vs FP4 vs INT4 comparisons.
- **EfficientQAT**: Reports WikiText-2 PPL (e.g., 8.02 vs OmniQuant's 15.02).

### Bits Per Byte (BPB)
**Tokenizer-agnostic** quality metric. The key advantage over perplexity: BPB does not change when you change the tokenizer.

#### Formula

```
BPB = total_nats / (ln(2) * total_bytes)
```

Where:
- `total_nats` = sum of per-token negative log-likelihoods (in natural log / nats)
- `total_bytes` = sum of UTF-8 byte lengths of all target tokens
- `ln(2)` ≈ 0.6931 (converts nats to bits)

#### Step-by-step calculation:
1. Run model on validation set, get per-token NLL (cross-entropy with `reduction='none'`)
2. For each token, look up its byte length in UTF-8
3. Sum all NLLs -> `total_nats`
4. Sum all byte lengths -> `total_bytes`
5. `BPB = total_nats / (ln(2) * total_bytes)`

#### Nanochat implementation (Karpathy):
```python
# Pseudocode from nanochat/loss_eval.py
total_nats = 0.0
total_bytes = 0.0
for batch in batches:
    logits = model(batch)
    targets = batch[:, 1:]
    per_token_loss = cross_entropy(logits, targets, reduction='none')  # nats
    for each valid token y (y >= 0, not special):
        byte_len = token_bytes[y]  # precomputed lookup table
        if byte_len > 0:
            total_nats += per_token_loss[y]
            total_bytes += byte_len

bpb = total_nats / (math.log(2) * total_bytes)
```

Key details:
- Special tokens (BOS, EOS, PAD) are excluded (byte_len = 0)
- Masked/ignored tokens (target < 0) are excluded
- The `token_bytes` lookup is precomputed from the tokenizer

#### Why BPB matters:
A model with vocabulary size 100k will have lower per-token CE than one with vocab size 32k, even if they model language equally well. BPB normalizes this away by measuring bits of information per byte of raw text.

### Bits Per Character (BPC)
Same idea as BPB but normalized per character instead of per byte. For ASCII text, BPC ≈ BPB. For UTF-8 with multi-byte characters, they differ.

```
BPC = total_nats / (ln(2) * total_characters)
```

Used in older character-level model papers (e.g., enwiki8 benchmark).

### Conversion Table

| From | To | Formula |
|------|----|---------|
| CE (nats, per-token) | Perplexity | `PPL = exp(CE)` |
| CE (nats, per-token) | Bits per token | `bpt = CE / ln(2)` |
| CE (nats, per-token) | BPB | `BPB = CE * (N_tokens / N_bytes) / ln(2)` |
| Perplexity | CE (nats) | `CE = ln(PPL)` |
| Perplexity | BPB | `BPB = ln(PPL) * (N_tokens / N_bytes) / ln(2)` |
| BPB | Perplexity | `PPL = 2^(BPB * N_bytes / N_tokens)` |
| BPC | BPB | `BPB = BPC * (N_chars / N_bytes)` (≈1.0 for ASCII) |

---

## 3. How Specific Papers Report Results

### BitNet / BitNet b1.58 (Microsoft)
- **Quality**: Perplexity (matches FP16 LLaMA at 3B+ params). Zero-shot accuracy on downstream tasks (ARC, HellaSwag, WinoGrande, etc.).
- **Speed**: Inference latency (ms), inference throughput (tokens/s), memory usage (GB), energy consumption (J per token).
- **Key result**: BitNet b1.58 70B is 4.1x faster, 7.16x less memory, 8.9x throughput vs LLaMA FP16.
- **Training**: Does NOT report training tokens/s. Training still uses full-precision latent weights for gradients. The gains are at inference time.
- **Dataset**: Evaluated on standard benchmarks (WikiText-2 implied).

### GPTQ
- **Quality**: WikiText-2 perplexity (primary), Penn Treebank perplexity, C4 perplexity. Zero-shot accuracy on downstream tasks.
- **Speed**: Quantization time (GPU-hours). E.g., "175B parameters in ~4 GPU hours."
- **Key result tables**: Model x bitwidth grid showing PPL on WikiText-2. E.g., OPT-175B at FP16=8.34, 4bit-GPTQ=8.37, 3bit-GPTQ=8.68.
- **Calibration**: 128 samples from WikiText-2 or C4, sequence length 2048.

### QLoRA
- **Quality**: 5-shot MMLU accuracy (primary for instruction-tuned models), perplexity (for base model quantization comparisons), GLUE, chatbot Elo ratings (human eval).
- **Speed**: Memory usage (GB), training time (hours on single GPU).
- **Key result**: 4-bit NF4 + LoRA fully recovers 16-bit finetuning quality on MMLU. Guanaco 65B reaches 99.3% of ChatGPT on Vicuna benchmark.
- **Comparison**: NF4 vs FP4 vs INT4 at matched bitwidths.

### nanoGPT (Karpathy)
- **Quality**: Validation loss (cross-entropy on OpenWebText). HellaSwag accuracy.
- **Speed**: Time per iteration (ms), tokens per iteration, total training time.
- **Target**: val loss ~2.85 (matches finetuned GPT-2).

### LLM.c (Karpathy)
- **Quality**: FineWeb validation loss, HellaSwag accuracy (29.9% vs GPT-2's 29.4%).
- **Speed**: Total wall-clock time (90 min for GPT-2 124M), implying ~1.8M tokens/s on 8xH100.
- **Dataset**: 10B tokens of FineWeb.

### nanoGPT Speedrun (Keller Jordan / modded-nanogpt)
- **Quality**: FineWeb validation loss <= 3.28 (cross-entropy).
- **Speed**: Wall-clock time on 8xH100 (primary metric). Current record: ~90 seconds.
- **Token efficiency**: Tokens needed to reach target (500M vs original 10B).

### nanochat (Karpathy)
- **Quality**: BPB on validation set (primary, tokenizer-agnostic), CORE score (average of 22 downstream benchmarks including ARC, MMLU, GSM8K, HumanEval).
- **Speed**: Total training time, total training FLOPS.
- **Key innovation**: Switched from loss to BPB as the primary training metric specifically because it is vocab-size-invariant.

---

## 4. Standard Benchmarks and Datasets

### For Perplexity (Language Modeling Quality)
| Dataset | Description | Usage |
|---------|-------------|-------|
| **WikiText-2** | Wikipedia articles, ~2M tokens | The #1 standard for quantization papers |
| **Penn Treebank (PTB)** | WSJ articles, ~1M tokens | Often alongside WikiText-2 |
| **C4** | Colossal Clean Crawled Corpus subset | Used by GPTQ, EfficientQAT |
| **FineWeb** | High-quality web text | Used by LLM.c, nanoGPT speedrun |
| **OpenWebText** | Reddit-filtered web text | Used by nanoGPT |
| **LAMBADA** | Narrative passages, predict last word | Tests long-range dependencies |

### For Downstream Task Accuracy
| Benchmark | Metric | What it Tests |
|-----------|--------|---------------|
| **HellaSwag** | Accuracy | Commonsense reasoning (sentence completion) |
| **MMLU** | 5-shot accuracy | Broad knowledge (57 subjects) |
| **ARC-Easy/Challenge** | Accuracy | Science question answering |
| **WinoGrande** | Accuracy | Commonsense coreference resolution |
| **PIQA** | Accuracy | Physical intuition |
| **GSM8K** | Accuracy | Grade school math |
| **HumanEval** | pass@1 | Code generation |
| **TruthfulQA** | Accuracy | Factuality / hallucination resistance |

### Evaluation Framework
The standard tool is **EleutherAI/lm-evaluation-harness** (lm-eval). Most papers and repos use it for downstream benchmarks.

For perplexity, papers typically roll their own eval loop or use llama.cpp's built-in perplexity script.

---

## 5. Summary: What We Should Report

For a QAT training project, the standard would be:

**Speed metrics:**
1. **Tokens/second** — raw throughput during training
2. **Wall-clock time** — total time to reach a quality target
3. **MFU** — if targeting hardware efficiency claims (optional for small-scale work)

**Quality metrics:**
1. **Validation loss** (cross-entropy in nats) — the raw training signal
2. **BPB** (bits per byte) — tokenizer-agnostic, best for comparing across different setups. Formula: `BPB = total_nats / (ln(2) * total_bytes)`
3. **Perplexity** on WikiText-2 — if comparing to published quantization results
4. **HellaSwag accuracy** — lightweight downstream sanity check (used by LLM.c, nanoGPT)
5. **MMLU** — if making broader quality claims

**What to compare against:**
- FP16/BF16 baseline (same architecture, same data, same tokens)
- Published quantization results at matched bitwidths (e.g., GPTQ 4-bit, QLoRA NF4)

---

## Sources

- [BitNet paper (JMLR)](http://www.jmlr.org/papers/volume26/24-2050/24-2050.pdf)
- [BitNet b1.58 (arXiv)](https://arxiv.org/html/2402.17764v1)
- [GPTQ paper (arXiv)](https://arxiv.org/abs/2210.17323)
- [GPTQ repo](https://github.com/IST-DASLab/gptq)
- [QLoRA paper (arXiv)](https://arxiv.org/abs/2305.14314)
- [EfficientQAT (arXiv)](https://arxiv.org/pdf/2407.11062)
- [nanoGPT repo](https://github.com/karpathy/nanoGPT)
- [LLM.c repo](https://github.com/karpathy/llm.c)
- [LLM.c GPT-2 in 90 min discussion](https://github.com/karpathy/llm.c/discussions/481)
- [modded-nanogpt (speedrun)](https://github.com/KellerJordan/modded-nanogpt)
- [nanochat repo](https://github.com/karpathy/nanochat)
- [nanochat loss_eval.py (BPB implementation)](https://github.com/karpathy/nanochat/blob/master/nanochat/loss_eval.py)
- [nanochat DeepWiki (CORE + BPB)](https://deepwiki.com/karpathy/nanochat/6.1-core-score-and-base-model-evaluation)
- [BPB explainer (dipkumar.dev)](https://dipkumar.dev/posts/llm/bits-per-byte/)
- [BPC explainer (bauwenst)](https://bauwenst.github.io/posts/explainers/2024-07-29-Bits-per-character/)
- [Skeptric: Measuring a Language Model](https://skeptric.com/perplexity/)
- [PaLM paper (MFU origin)](https://arxiv.org/pdf/2204.02311)
- [MFU explainer (glennklockwood)](https://www.glennklockwood.com/garden/MFU)
- [Stas ml-engineering (training perf)](https://github.com/stas00/ml-engineering/blob/master/training/performance/README.md)
- [Comprehensive quantization eval (arXiv)](https://arxiv.org/html/2402.16775v1)
- [LLaMA3 quantization study](https://arxiv.org/pdf/2404.14047)
