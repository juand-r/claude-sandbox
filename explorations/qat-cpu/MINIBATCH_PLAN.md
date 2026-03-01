# Mini-batch Implementation Plan

## Goal
Add mini-batching (batch_size=8) to improve hardware utilization (MFU).
Currently batch=1, M=64 in GEMMs. With batch=8, M=512 for linear layers.

## Architecture Decision

**For linear layers (QATLinear, output head):** Stack all tokens from all
sequences into a single `[batch*seq_len, dim]` matrix. These are already
batch-agnostic — they process each row independently.

**For attention:** Loop over batch items, computing `[seq_len x seq_len]`
attention per sequence. This avoids the `[B*seq x B*seq]` blowup and keeps
the causal mask simple. The per-head GEMM is small anyway (64x64x64); the
big win from batching is in the linear layers.

## Changes Required

### 1. train.c: gpt_forward()
- Accept `int batch_size` parameter (in addition to seq_len)
- **Embedding**: Loop `for b in [0, batch)`, use relative position `s` not `b*seq_len + s`
- **Transformer blocks**: Pass `[batch*seq_len, dim]` tensor (blocks are batch-agnostic)
- **Return**: `[batch*seq_len, vocab_size]` logits

### 2. layers.c: attention_forward()
- Accept `int batch_size` parameter
- **Before per-head loop**: Reshape input from `[batch*seq_len, dim]` perspective
- **Per head, per batch item**: Extract head slice, compute scores, causal mask, softmax, value multiply
- **After**: Scatter results back into `[batch*seq_len, dim]` output
- Saved attention: `[batch * n_heads * seq_len, seq_len]`

### 3. layers.c: attention_backward()
- Same batch loop structure as forward
- Use saved attention per (batch, head) pair

### 4. layers.c: transformer_block_forward/backward()
- Accept batch_size parameter, pass through to attention
- Everything else (RMSNorm, QATLinear, GeLU, residuals) works as-is

### 5. train.c: gpt_backward()
- Embedding gradient scatter: use relative positions
- saved_tokens becomes `[batch * seq_len]`

### 6. train.c: train_step()
- Sample `batch_size` random starting positions
- Build `[batch*seq_len]` token array
- Build `[batch*seq_len]` target array
- Forward, loss, backward as before but with larger tensors

### 7. train.c: eval / generate
- Eval can use batch=1 (keep simple, it's not the bottleneck)
- Generate stays batch=1 (autoregressive)

### 8. Constants
- Add `#define BATCH_SIZE 8`
- Update `estimate_flops_per_step()` to include batch

## What does NOT change
- qat_linear.c (forward/backward) — already batch-agnostic
- loss.c — already batch-agnostic
- optimizer.c — already batch-agnostic
- layers.c: rmsnorm, gelu — already batch-agnostic
- quantize.c — already batch-agnostic

## Memory impact
- Activations scale by 8x (batch=8): ~8x more memory for saved states
- Attention saved: 8 * 8heads * 64*64 * 4 bytes = 1MB (trivial)
- Gradients: same size (parameters don't scale with batch)
- Main concern: intermediate tensors in QATLinear (INT8 buffers) scale with batch
  Currently these are allocated per-call, so they auto-scale.

## Expected outcome
- Linear layer GEMMs go from M=64 to M=512
- MFU should increase significantly (maybe 5-10% from 1.5%)
- tokens/sec should increase (processing 8x more tokens per step, step time < 8x longer)
- QAT speedup ratio should be preserved or improve

## Actual results (5K steps, dim=512, batch=8)

```
                    FP32          QAT
Val perplexity:     4.48          4.48
Val BPB:            2.163         2.164
ms/step:            183.8         187.6
Tokens/sec:         2785          2729
Effective TFLOPS:   0.1062        0.1041
QAT speedup:        --            0.98x
```

- MFU: ~5% (up from 1.5%) -- correct prediction
- tokens/sec: ~2700 (up from ~900) -- correct prediction, 3x improvement
- QAT speedup: 0.98x (WRONG prediction) -- batching eliminated QAT's advantage
  because the FP32 backward pass (same in both modes) also benefits from larger
  GEMMs and now dominates step time. See OPTIMIZATION_NOTES.md for analysis.
