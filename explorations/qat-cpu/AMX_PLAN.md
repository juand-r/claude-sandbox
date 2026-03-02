# AMX-INT8 GEMM Kernel Plan

## STATUS: AMX BLOCKED — container does not expose AMX hardware

CPUID reports AMX-INT8/AMX-BF16/AMX-TILE as available and XCR0 has bits
17+18 set, but AMX instructions (LDTILECFG, TDPBSSD) cause SIGILL.
The arch_prctl(ARCH_REQ_XCOMP_PERM) syscall returns EINVAL.

This is a container/VM limitation — the hypervisor exposes the CPUID
flags but does not enable the AMX XSAVE state for guests.

**Fallback: AVX-512 BF16 for backward GEMMs** — VDPBF16PS works correctly.
This targets the biggest bottleneck (1573 ms, 37%) with proven hardware.
See BF16_BACKWARD_PLAN.md.

The AMX research below is preserved for when we have bare-metal access.

---

## AMX ISA Summary (research notes)

### Tile Registers
- 8 tile registers: tmm0-tmm7
- Each tile: up to 16 rows x 64 bytes = 1024 bytes
- Configured via 64-byte `__tilecfg` struct loaded with `_tile_loadconfig()`

### Tile Config Struct
```c
typedef struct __tile_config {
    uint8_t palette_id;    // must be 1
    uint8_t start_row;     // 0
    uint8_t reserved[14];
    uint16_t colsb[16];   // bytes per row for tiles 0-15
    uint8_t rows[16];      // number of rows for tiles 0-15
} __tilecfg;
```

### INT8 Tile Dimensions (TDPBSSD/TDPBUSD)
- A tile: 16 rows x 64 bytes = 16 x 64 INT8 elements
- B tile: 16 rows x 64 bytes = re-laid-out from 64 x 16 INT8
- C tile: 16 rows x 64 bytes = 16 x 16 INT32 elements

One TDPBSSD instruction: C[16x16] += A[16x64] * B[64x16]
= 16 * 16 * 64 = 16384 INT8 MACs per instruction!

Compare VNNI VPDPBUSD: 16 * 4 = 64 MACs per instruction.
AMX does 256x more work per instruction.

### Key Insight: TDPBSSD (signed * signed)
AMX has four dot-product variants:
- TDPBSSD: signed * signed -> int32
- TDPBUSD: unsigned * signed -> int32
- TDPBSUD: signed * unsigned -> int32
- TDPBUUD: unsigned * unsigned -> int32

VNNI only has VPDPBUSD (unsigned * signed), which forces the unsigned
trick (+128 conversion + correction). **With TDPBSSD, we don't need the
unsigned trick at all.** Both A (activations) and B (weights) are signed
INT8, so TDPBSSD handles them natively. This simplifies the kernel.

### B Matrix Layout (same as VNNI interleaving!)
B must be packed so that 4 consecutive K values for each of 16 columns
are in one row of 64 bytes. This is the exact same interleaving as our
VNNI prepacking:

```
VNNI chunk (64 bytes):
  byte[j*4 + dk] = B[(ks*4+dk) * ldb + (js*16 + j)]
  for j=0..15, dk=0..3

AMX B tile (1024 bytes = 16 rows of 64 bytes):
  = 16 consecutive VNNI chunks covering K=64
```

So the AMX B tile is just 16 contiguous VNNI chunks. Same packing code,
different iteration pattern. We can **reuse** the VNNI packing function.

### A Matrix Layout
A tiles are loaded directly from row-major memory:
- `_tile_loadd(tmm, A + m*lda + k, lda)` loads 16 rows x 64 cols
- No special packing needed

### C Matrix Layout
C tiles are stored directly to row-major memory:
- `_tile_stored(tmm, C + m*ldc + n, ldc * sizeof(int32_t))` stores 16 rows x 16 cols

### OS Setup Required
Before first use, must request XSTATE permission:
```c
#include <sys/syscall.h>
#define ARCH_REQ_XCOMP_PERM 0x1023
#define XFEATURE_XTILEDATA 18
syscall(SYS_arch_prctl, ARCH_REQ_XCOMP_PERM, XFEATURE_XTILEDATA);
```

### Intrinsics
```c
#include <immintrin.h>
_tile_loadconfig(const void *cfg);   // load 64-byte tile config
_tile_zero(tmm_num);                 // zero a tile register
_tile_loadd(tmm_num, ptr, stride);   // load from memory (stride = bytes between rows)
_tile_stored(tmm_num, ptr, stride);  // store to memory
_tile_dpbssd(dst, src1, src2);       // C += A * B (signed * signed INT8 -> INT32)
_tile_release();                     // release tile state (like vzeroupper for AVX)
```

### Compiler Flags
```
-mamx-int8 -mamx-tile
```

## Our GEMM Sizes

| Call site          | M    | K    | N    | M/16 | K/64 | N/16 |
|--------------------|------|------|------|------|------|------|
| QAT fwd (proj)     | 512  | 1024 | 1024 | 32   | 16   | 64   |
| QAT fwd (up/gate)  | 512  | 1024 | 4096 | 32   | 16   | 256  |
| QAT fwd (down)     | 512  | 4096 | 1024 | 32   | 64   | 64   |
| Attn scores        | 64   | 128  | 64   | 4    | 2    | 4    |
| Attn values        | 64   | 64   | 128  | 4    | 1    | 8    |

All dimensions are divisible by tile sizes (M%16=0, K%64=0, N%16=0).
Exception: attention K=64 is fine (K/64=1, one tile), but attention
N=64 has K=64 which divides. OK, all clean.

Wait: head_dim=128, K=128 for attention scores. 128/64=2. Fine.
For attention values: K=seq_len=64, N=head_dim=128. 64/64=1, 128/16=8. Fine.

## Implementation Plan

### Step 1: OS setup in cpu_detect.c
Add `amx_request_permission()` function that calls arch_prctl.
Call it from cpu_detect() if AMX tiles are detected.

### Step 2: New file kernels_amx.c
```
gemm_int8_amx(M, N, K, A, lda, B, ldb, C, ldc)
```

Algorithm:
1. **Pack B** into VNNI-interleaved format (reuse existing packing code,
   or inline same logic). Layout: for each N-strip of 16 columns,
   for each K-block of 64, store 16 rows x 64 bytes (= 16 VNNI chunks).

2. **Configure tiles**: one-time tilecfg for A[16x64], B[16x64], C[16x16].

3. **Main GEMM loop** (OpenMP over m-blocks):
   ```
   for m_block = 0 .. M/16-1:     // 32 blocks for M=512
     for n_block = 0 .. N/16-1:   // 64 or 256 blocks
       _tile_zero(tmm0)            // C accumulator
       for k_block = 0 .. K/64-1: // 16 blocks for K=1024
         _tile_loadd(tmm1, A + m*lda + k*64, lda)        // A: row-major
         _tile_loadd(tmm2, packed_B[n_block,k_block], 64) // B: packed
         _tile_dpbssd(tmm0, tmm1, tmm2)                  // C += A * B
       _tile_stored(tmm0, C + m*ldc + n, ldc*4)           // store result
   ```

4. **No unsigned trick**: TDPBSSD handles signed*signed natively.
   Correction computation is eliminated entirely.

5. **Tail handling**: Assert M%16==0, K%64==0, N%16==0 for now.
   All our actual GEMMs satisfy this. Add fallback to VNNI later if needed.

### Step 3: Update Makefile
```makefile
CFLAGS_AMX = $(CFLAGS_BASE) -mamx-int8 -mamx-tile -mavx512f -mavx512bw
SRC_AMX = kernels_amx.c
OBJ_AMX = $(SRC_AMX:.c=.o)
```

### Step 4: Update dispatch.c
```
INT8: AMX (if amx_int8 && amx_tile) > VNNI > AVX2 > scalar
```

### Step 5: Declare in qat_cpu.h
```c
void gemm_int8_amx(int M, int N, int K,
                   const int8_t *A, int lda,
                   const int8_t *B, int ldb,
                   int32_t *C, int ldc);
```

### Step 6: Test
- Run existing test_qat (GEMM correctness tests)
- Compare AMX output vs scalar for same inputs
- Verify training still converges (short run)

### Step 7: Benchmark
- Run profile_qat and compare AMX vs VNNI
- Key metric: QATLinear forward time (currently 982 ms)

## Expected Performance

VNNI: 64 INT8 MACs per VPDPBUSD instruction, 16-wide vector, K=4 per op.
AMX:  16384 INT8 MACs per TDPBSSD instruction, 16x16x64 tile.

AMX throughput is ~2 TDPBSSD per cycle (Sapphire Rapids), so:
  16384 * 2 = 32768 MACs/cycle at ~2.1 GHz = ~68.8 GINT8OPS/core
  vs VNNI: 64 * 2 = 128 MACs/cycle = ~268 MINT8OPS/core (0.268 GOPS)

Wait, that's 256x more? That seems too high. Let me reconsider.

VNNI: 2 ports can execute VPDPBUSD, so 128 MACs/cycle per core.
AMX: TDPBSSD has throughput of ~16 cycles for a 16x16x64 tile
  = 16384 MACs / 16 cycles = 1024 MACs/cycle per core.

So AMX is ~8x more MACs/cycle than VNNI. At 16 cores:
  VNNI: 128 * 16 * 2.1G = ~4.3 TOPS
  AMX:  1024 * 16 * 2.1G = ~34.4 TOPS

But we're not compute-bound at these sizes — we're memory-bandwidth bound
for the GEMM loads. The real speedup depends on:
1. Elimination of unsigned trick (saves correction computation + A conversion)
2. Fewer load instructions per MAC (each tile load serves 16K MACs vs 64)
3. Better cache utilization (tiles fit in L1)

Realistic expectation: **2-4x speedup** on the GEMM portion of QATLinear forward.

## Risks
- AMX context switch overhead: tiles are large (8KB total), OS save/restore
  is expensive. But this only matters with frequent switches.
- First-use penalty: ~70 microseconds for first TDPBSSD (lazy state init).
  Negligible over a training run.
- Compiler support: need gcc 11+ for AMX intrinsics. Our gcc should be fine.
