# Intel AMX INT8 ISA Reference for GEMM Kernels

## 1. Tile Registers

AMX introduces **8 tile registers** named `TMM0` through `TMM7`. Each tile is a 2D register:

- **Max dimensions**: 16 rows x 64 bytes = 1024 bytes (1 KB) per tile
- **Total tile storage**: 8 KB across all 8 tiles (palette 1)
- Tiles are configured dynamically -- each tile can have fewer rows or fewer column-bytes than the max
- For INT8: 64 bytes = 64 elements per row
- For INT32: 64 bytes = 16 elements per row (used for accumulators)

### Tile Configuration via LDTILECFG

Tiles are configured by loading a 64-byte structure from memory using `LDTILECFG` (intrinsic: `_tile_loadconfig`). Two palettes exist:
- **Palette 0**: Init state. All tiles zeroed. No storage allocated.
- **Palette 1**: 8 tiles, each up to 16 rows x 64 bytes.

---

## 2. The TILECFG Structure (64 bytes)

```
Offset  Size     Field           Description
------  -------  --------------- -------------------------------------------
0       1 byte   palette_id      0 = init state, 1 = 8 tiles active
1       1 byte   start_row       Restart row for interrupted instructions (set to 0)
2-15    14 bytes reserved        Must be zero
16-47   32 bytes colsb[0..15]    Column bytes (uint16_t) for each tile
48-63   16 bytes rows[0..15]     Row count (uint8_t) for each tile
```

C structure:
```c
typedef struct __tile_config {
    uint8_t  palette_id;       // Byte 0
    uint8_t  start_row;        // Byte 1
    uint8_t  reserved_0[14];   // Bytes 2-15
    uint16_t colsb[16];       // Bytes 16-47: column bytes per tile
    uint8_t  rows[16];        // Bytes 48-63: rows per tile
} __tilecfg;
```

### start_row field

This is used internally by the processor for **restartable instructions**. TILELOADD, TILESTORED, and TDP* instructions can be interrupted by page faults mid-execution. The processor saves progress in `start_row` so the instruction can resume from that row rather than restarting. **Always initialize to 0.**

### Unused tiles

If a tile is not used, its `rows[i]` and `colsb[i]` must both be 0. Specifying more tiles than the palette supports causes a #GP fault.

---

## 3. TDPBSSD and Variants: The Dot-Product Instructions

These are the AMX-INT8 multiply-accumulate instructions. The naming convention `TDPB<s1><s2>D` encodes signedness:

| Instruction | src1 (A) | src2 (B) | Mnemonic                    |
|-------------|----------|----------|-----------------------------|
| TDPBSSD     | signed   | signed   | Tile Dot Product S*S -> Dword |
| TDPBUSD     | unsigned | signed   | Tile Dot Product U*S -> Dword |
| TDPBSUD     | signed   | unsigned | Tile Dot Product S*U -> Dword |
| TDPBUUD     | unsigned | unsigned | Tile Dot Product U*U -> Dword |

All accumulate into INT32 (dword) elements.

### Operation

```
dst_tile += matmul(src1_tile, src2_tile)
```

Concretely, the DPBD (dot product byte->dword) helper for each 4-byte group:

```
// For TDPBSSD: extend_src1 = SIGN_EXTEND, extend_src2 = SIGN_EXTEND
// For TDPBUSD: extend_src1 = ZERO_EXTEND, extend_src2 = SIGN_EXTEND
// etc.

p0 = extend_src1(x.byte[0]) * extend_src2(y.byte[0])
p1 = extend_src1(x.byte[1]) * extend_src2(y.byte[1])
p2 = extend_src1(x.byte[2]) * extend_src2(y.byte[2])
p3 = extend_src1(x.byte[3]) * extend_src2(y.byte[3])
c  = c + p0 + p1 + p2 + p3
```

### Full pseudocode

```
// dst = M x N tile (INT32 accumulator)
// src1 = M x K tile (INT8, A matrix)
// src2 = K x N tile (INT8, B matrix, in VNNI layout)
// Dimensions in dwords: K_dwords = src1.colsb/4, N_dwords = dst.colsb/4

for m in 0..dst.rows-1:
    tmp = dst.row[m]              // copy row of accumulator
    for k in 0..K_dwords-1:
        for n in 0..N_dwords-1:
            DPBD(tmp.dword[n], src1.row[m].dword[k], src2.row[k].dword[n])
    dst.row[m] = tmp
```

### Tile dimension constraints for a single TDPB* instruction

For INT8 GEMM computing C[M,N] += A[M,K] * B[K,N]:

| Tile | Role          | Max rows | Max colsb | Interpretation             |
|------|---------------|----------|-----------|----------------------------|
| A    | src1          | 16       | 64        | 16 x 64 INT8 elements      |
| B    | src2          | 16       | 64        | 16 rows x 64 bytes (VNNI)  |
| C    | dst (accum)   | 16       | 64        | 16 x 16 INT32 elements     |

The K dimension in a single instruction: A has K = colsb = 64 INT8 elements. B has K = rows = 16 (but each row contains 4 INT8 packed into dwords, so effective K = 16 * 4 = 64).

**Result of one TDPB* instruction**: C[16x16] += A[16x64] * B[64x16] -- that is, 16x16 INT32 output from 16x64 times 64x16 INT8 inputs.

---

## 4. Memory Layout: TILELOADD and the B Matrix Re-Layout

### TILELOADD basics

`TILELOADD tmm, [base + stride*row]` loads tile data from memory row by row.
- Each row is loaded from `base + row_index * stride`
- `stride` is the byte distance between consecutive rows in memory
- Unloaded bytes (if colsb < 64) are zero-filled

Intrinsic: `_tile_loadd(tile_id, base_ptr, stride)`

### A matrix layout: straightforward row-major

Matrix A (M x K, INT8) can be stored in standard row-major format. If A is M=16 rows, K=64 columns, store 64 bytes per row. Load with stride = K (or larger if padded).

### B matrix layout: VNNI-style re-layout required

**This is the critical detail.** AMX accesses all tile registers row-wise. In standard GEMM, B is accessed column-wise. AMX cannot do this, so B must be re-laid-out into a special format.

The TDPB* instructions process INT8 data in groups of 4 bytes (one dword). The B matrix must be arranged so that 4 consecutive K-dimension elements from the same column are packed together.

#### Re-layout transformation

Original B matrix shape: K x N (e.g., 64 x 16), row-major:
```
Row 0:  B[0,0]  B[0,1]  ... B[0,15]
Row 1:  B[1,0]  B[1,1]  ... B[1,15]
Row 2:  B[2,0]  B[2,1]  ... B[2,15]
Row 3:  B[3,0]  B[3,1]  ... B[3,15]
...
Row 63: B[63,0] B[63,1] ... B[63,15]
```

Re-laid-out B for AMX (16 rows x 64 bytes):
```
Row 0:  B[0,0] B[1,0] B[2,0] B[3,0] | B[0,1] B[1,1] B[2,1] B[3,1] | ... | B[0,15] B[1,15] B[2,15] B[3,15]
Row 1:  B[4,0] B[5,0] B[6,0] B[7,0] | B[4,1] B[5,1] B[6,1] B[7,1] | ... | B[4,15] B[5,15] B[6,15] B[7,15]
...
Row 15: B[60,0] B[61,0] B[62,0] B[63,0] | ... | B[60,15] B[61,15] B[62,15] B[63,15]
```

Each row of the re-laid-out B contains: N columns * 4 bytes = 16 * 4 = 64 bytes.
Number of rows: K / 4 = 64 / 4 = 16 rows.

#### Re-layout code

```c
// B is K x N row-major INT8; Brel is the VNNI-format output
// K must be a multiple of 4
void repack_B_vnni(const int8_t *B, int8_t *Brel, int K, int N) {
    for (int i = 0; i < K; i += 4) {
        for (int j = 0; j < N; j++) {
            Brel[(i * N) + (j * 4) + 0] = B[((i + 0) * N) + j];
            Brel[(i * N) + (j * 4) + 1] = B[((i + 1) * N) + j];
            Brel[(i * N) + (j * 4) + 2] = B[((i + 2) * N) + j];
            Brel[(i * N) + (j * 4) + 3] = B[((i + 3) * N) + j];
        }
    }
}
```

After re-layout, the B tile has shape (K/4) rows x (N*4) bytes, and is loaded with stride = N*4.

For the max tile: B_relaid is 16 rows x 64 bytes (fits in one tile), representing original 64x16 B.

---

## 5. C Intrinsics API

Header: `#include <immintrin.h>`

### Core intrinsics

| Intrinsic                              | Instruction    | Description                          |
|----------------------------------------|----------------|--------------------------------------|
| `_tile_loadconfig(const void *cfg)`    | LDTILECFG      | Load tile configuration (64 bytes)   |
| `_tile_storeconfig(void *cfg)`         | STTILECFG      | Store current tile config            |
| `_tile_loadd(tile_id, base, stride)`   | TILELOADD      | Load tile from memory                |
| `_tile_stored(tile_id, base, stride)`  | TILESTORED     | Store tile to memory                 |
| `_tile_zero(tile_id)`                  | TILEZERO       | Zero out a tile register             |
| `_tile_dpbssd(dst, src1, src2)`        | TDPBSSD        | signed * signed -> INT32 accum       |
| `_tile_dpbusd(dst, src1, src2)`        | TDPBUSD        | unsigned * signed -> INT32 accum     |
| `_tile_dpbsud(dst, src1, src2)`        | TDPBSUD        | signed * unsigned -> INT32 accum     |
| `_tile_dpbuud(dst, src1, src2)`        | TDPBUUD        | unsigned * unsigned -> INT32 accum   |
| `_tile_release()`                      | TILERELEASE    | Release tile state (back to init)    |

`tile_id`, `dst`, `src1`, `src2` are integer constants 0-7 selecting TMM registers.

### Note on clang vs gcc

- **clang/clang++**: supports `__tile1024i` struct type that wraps tile intrinsics and can hide TILECFG manipulation.
- **gcc/g++**: requires explicit TILECFG setup via the structure and `_tile_loadconfig`.

---

## 6. Compiler Flags

```
gcc -mamx-tile -mamx-int8 -O2 source.c -o output
```

- `-mamx-tile`: enables AMX-TILE instructions (LDTILECFG, TILELOADD, TILESTORED, TILEZERO, TILERELEASE)
- `-mamx-int8`: enables AMX-INT8 instructions (TDPBSSD, TDPBUSD, TDPBSUD, TDPBUUD)
- `-mamx-bf16`: enables AMX-BF16 instructions (if needed)

Minimum compiler versions: GCC 11, LLVM/Clang 12, Intel ICC.

For CPUs without AMX hardware, use Intel SDE (Software Development Emulator):
```
sde64 -spr -- ./your_binary
```

---

## 7. OS Setup: Linux XSTATE Permission

AMX tile data adds ~8 KB to the kernel-managed XSAVE state per process. The kernel does not allocate this by default. The application must explicitly request permission.

### Required syscall

```c
#include <sys/syscall.h>
#include <unistd.h>

#define ARCH_GET_XCOMP_PERM     0x1022
#define ARCH_REQ_XCOMP_PERM    0x1023
#define XFEATURE_XTILECFG      17
#define XFEATURE_XTILEDATA     18

static int enable_amx(void) {
    // Request permission for AMX tile data
    if (syscall(SYS_arch_prctl, ARCH_REQ_XCOMP_PERM, XFEATURE_XTILEDATA)) {
        perror("ARCH_REQ_XCOMP_PERM failed");
        return -1;
    }
    return 0;
}
```

### What happens without permission

If a process uses an AMX instruction without having requested XCOMP_PERM, the kernel sends **SIGILL**.

### Permission rules

- Permission is per-process
- Inherited on `fork()`
- Cleared on `exec()`
- If the process has a sigaltstack that is too small for the expanded signal frame, `ARCH_REQ_XCOMP_PERM` returns `-ENOSUPP`
- Requires Linux kernel 5.16+ with AMX support enabled

### CPUID check

AMX-TILE: CPUID leaf 7, sub-leaf 0, EDX bit 24.
AMX-INT8: CPUID leaf 7, sub-leaf 0, EDX bit 25.

Also visible in `/proc/cpuinfo` flags: `amx_tile`, `amx_int8`, `amx_bf16`.

---

## 8. Minimal Working Example

```c
#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/syscall.h>
#include <unistd.h>

#define ARCH_REQ_XCOMP_PERM 0x1023
#define XFEATURE_XTILEDATA  18

typedef struct {
    uint8_t  palette_id;
    uint8_t  start_row;
    uint8_t  reserved[14];
    uint16_t colsb[16];
    uint8_t  rows[16];
} tilecfg_t;

int main(void) {
    // 1. Request AMX permission from OS
    if (syscall(SYS_arch_prctl, ARCH_REQ_XCOMP_PERM, XFEATURE_XTILEDATA))
        return 1;

    // 2. Configure tiles
    tilecfg_t cfg;
    memset(&cfg, 0, sizeof(cfg));
    cfg.palette_id = 1;

    // Tile 0: C accumulator, 16 rows x 64 bytes (= 16 INT32 columns)
    cfg.rows[0]  = 16;
    cfg.colsb[0] = 64;   // 16 * sizeof(int32_t) = 64

    // Tile 1: A operand, 16 rows x 64 bytes (= 64 INT8 columns)
    cfg.rows[1]  = 16;
    cfg.colsb[1] = 64;

    // Tile 2: B operand (VNNI format), 16 rows x 64 bytes
    cfg.rows[2]  = 16;
    cfg.colsb[2] = 64;

    _tile_loadconfig(&cfg);

    // 3. Prepare data
    int8_t  A[16 * 64];       // 16x64 INT8
    int8_t  B_vnni[16 * 64];  // 64x16 B, repacked to 16x64 VNNI
    int32_t C[16 * 16];       // 16x16 INT32

    // ... fill A, B_vnni, zero C ...
    memset(A, 1, sizeof(A));
    memset(B_vnni, 1, sizeof(B_vnni));
    memset(C, 0, sizeof(C));

    // 4. Load tiles
    _tile_loadd(0, C, 64);         // stride = 16 * sizeof(int32_t) = 64
    _tile_loadd(1, A, 64);         // stride = 64 (64 INT8 per row)
    _tile_loadd(2, B_vnni, 64);   // stride = 64

    // 5. Compute: C += A * B
    _tile_dpbssd(0, 1, 2);

    // 6. Store result
    _tile_stored(0, C, 64);

    // 7. Cleanup
    _tile_release();

    // Each C[i][j] = sum over k of A[i][k] * B[k][j]
    // With all 1s: each element = 64 (64 multiplications of 1*1)
    printf("C[0][0] = %d (expected 64)\n", C[0]);

    return 0;
}
```

Compile: `gcc -mamx-tile -mamx-int8 -O2 example.c -o example`

---

## 9. Tiling a Large M x N x K GEMM

A single TDPB* instruction computes C[16x16] += A[16x64] * B[64x16]. For larger matrices, you need three levels of tiling.

### Level 1: Tile Register Blocking (Microkernel)

You have 8 tile registers. Reserve 2 for loading A and B operands, use the remaining 6 as a 2D accumulator grid. Recommended configurations:

| Grid   | Accum tiles | A tiles | B tiles | C block size       |
|--------|-------------|---------|---------|--------------------|
| 2x3    | 6 (tmm0-5) | 1 (tmm6)| 1 (tmm7)| 32 x 48 INT32      |
| 3x2    | 6 (tmm0-5) | 1 (tmm6)| 1 (tmm7)| 48 x 32 INT32      |
| 2x2    | 4 (tmm0-3) | 2 (tmm4-5)| 2 (tmm6-7)| 32 x 32 INT32  |
| 1x1    | 1           | 1       | 1       | 16 x 16 INT32      |

The near-square grid minimizes loads per FMA (minimize x+y subject to x*y=6).

### Level 2: K-dimension loop

For K > 64, iterate over K in steps of 64. Each iteration loads new A and B sub-tiles and accumulates into the same C tiles.

### Level 3: Cache blocking

Divide M, N, K into blocks that fit in L1/L2/L3 cache. Typical hierarchy:
- L1 block: fits in ~48 KB L1D (the tile registers themselves live here)
- L2 block: ~1-2 MB
- L3 block: tens of MB

### Example: 2x2 accumulator grid, large GEMM

```
Tile register assignment:
  tmm0 = C[0,0]   tmm1 = C[0,1]     (accumulators, 16x16 INT32 each)
  tmm2 = C[1,0]   tmm3 = C[1,1]
  tmm4 = A[0,k]   tmm5 = A[1,k]     (A operand tiles, 16x64 INT8)
  tmm6 = B[k,0]   tmm7 = B[k,1]     (B operand tiles, VNNI, 16x64)

This computes a 32x32 output block per microkernel invocation.
```

### Pseudocode for large GEMM

```c
// C[M,N] += A[M,K] * B_vnni[K,N]
// A is M x K row-major INT8
// B_vnni is K x N repacked to VNNI format
// C is M x N INT32

// Tile blocking constants
#define TILE_M  16   // rows per A/C tile
#define TILE_N  16   // INT32 columns per B/C tile (= 64 bytes / 4)
#define TILE_K  64   // INT8 columns per A tile = K elements per step

// Using 2x2 accumulator grid: processes 32x32 output block
#define BLK_M  (2 * TILE_M)   // 32
#define BLK_N  (2 * TILE_N)   // 32

for (int m = 0; m < M; m += BLK_M) {
    for (int n = 0; n < N; n += BLK_N) {
        // Zero accumulator tiles
        _tile_zero(0);  // C[0,0]
        _tile_zero(1);  // C[0,1]
        _tile_zero(2);  // C[1,0]
        _tile_zero(3);  // C[1,1]

        for (int k = 0; k < K; k += TILE_K) {
            // Load A tiles: A[m..m+15, k..k+63] and A[m+16..m+31, k..k+63]
            _tile_loadd(4, &A[(m+0)  * K + k], K);
            _tile_loadd(5, &A[(m+16) * K + k], K);

            // Load B tiles (VNNI format): B[k..k+63, n..n+15] and B[k..k+63, n+16..n+31]
            // After VNNI repack, B_vnni stride = N * 4
            // Tile for B[:,n..n+15] starts at: B_vnni[k/4 * (N*4) + n*4]
            // which has 16 rows of 64 bytes each
            _tile_loadd(6, &B_vnni[(k/4) * (N*4) + (n+0)*4],  N * 4);
            _tile_loadd(7, &B_vnni[(k/4) * (N*4) + (n+16)*4], N * 4);

            // Accumulate: C[i,j] += A[i,k] * B[k,j]
            _tile_dpbssd(0, 4, 6);   // C[0,0] += A[0,k] * B[k,0]
            _tile_dpbssd(1, 4, 7);   // C[0,1] += A[0,k] * B[k,1]
            _tile_dpbssd(2, 5, 6);   // C[1,0] += A[1,k] * B[k,0]
            _tile_dpbssd(3, 5, 7);   // C[1,1] += A[1,k] * B[k,1]
        }

        // Store accumulator tiles to C
        int c_stride = N * sizeof(int32_t);
        _tile_stored(0, &C[(m+0)  * N + (n+0)],  c_stride);
        _tile_stored(1, &C[(m+0)  * N + (n+16)], c_stride);
        _tile_stored(2, &C[(m+16) * N + (n+0)],  c_stride);
        _tile_stored(3, &C[(m+16) * N + (n+16)], c_stride);
    }
}
```

### Software pipelining best practice

The Intel Optimization Manual recommends interleaving TILELOAD/TILESTORE with TDP instructions rather than batching all loads together. This prevents bottlenecks on the load/store unit.

Better pattern for the inner loop body:
```c
_tile_loadd(4, &A[...], K);           // Load A[0]
_tile_loadd(6, &B_vnni[...], N*4);    // Load B[0]
_tile_dpbssd(0, 4, 6);                // C[0,0] += A[0]*B[0]
_tile_loadd(7, &B_vnni[...], N*4);    // Load B[1] -- interleaved with compute
_tile_dpbssd(1, 4, 7);                // C[0,1] += A[0]*B[1]
_tile_loadd(5, &A[...], K);           // Load A[1]
_tile_dpbssd(2, 5, 6);                // C[1,0] += A[1]*B[0]  (B[0] still in tmm6)
_tile_dpbssd(3, 5, 7);                // C[1,1] += A[1]*B[1]
```

### Post-processing

Results from AMX tiles are INT32. Any post-processing (bias add, requantize, activation) must be done via AVX-512 vector registers:
1. `_tile_stored` the accumulator to a buffer (fits in L1, at most 4 KB)
2. Load into ZMM registers with AVX-512
3. Apply bias, scale, clamp, store final output

---

## 10. Performance Numbers

- Sapphire Rapids / Emerald Rapids: **2048 INT8 ops/cycle** per core (or 1024 BF16 ops/cycle)
- One TDPB* instruction: 16 * 16 * 64 * 2 = 32768 INT8 ops (multiply + add)
- At 2048 ops/cycle, one full 16x16x64 TDPB* takes ~16 cycles
- TILELOAD latency: ~40-50 cycles (from L1); hence the need for software pipelining

---

## 11. Key References

- [Intel AMX Intrinsics Code Sample](https://www.intel.com/content/www/us/en/developer/articles/code-sample/advanced-matrix-extensions-intrinsics-functions.html)
- [Intel AMX-TMUL-Code-Samples (GitHub)](https://github.com/intel/AMX-TMUL-Code-Samples)
- [TDPBSSD/TDPBUSD ISA Reference (Felix Cloutier)](https://www.felixcloutier.com/x86/tdpbssd:tdpbsud:tdpbusd:tdpbuud)
- [LDTILECFG ISA Reference](https://www.felixcloutier.com/x86/ldtilecfg)
- [Fixstars AMX Introduction (with B re-layout)](https://blog.us.fixstars.com/intel-amx-advanced-matrix-extension-explained-introduction/)
- [Intel Optimization Reference Manual (PDF, Ch. 20)](https://cdrdv2-public.intel.com/814201/355308-Optimization-Reference-Manual-049-Changes-Doc.pdf)
- [Linux Kernel XSTATE Documentation](https://docs.kernel.org/arch/x86/xstate.html)
- [Optimization of GEMM using Intel AMX (ACM)](https://dl.acm.org/doi/10.1145/3773656.3773660)
- [HJLebbink/AMX-matmul (GitHub)](https://github.com/HJLebbink/AMX-matmul)
- [ONNX Runtime AMX Optimization (Microsoft)](https://opensource.microsoft.com/blog/2023/09/07/boosting-performance-in-onnx-runtime-with-intel-amx-for-4th-gen-intel-xeon-processors)
