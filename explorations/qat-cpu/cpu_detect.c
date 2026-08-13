/*
 * cpu_detect.c - CPU feature detection via CPUID
 *
 * Detects AVX2, AVX-512, VNNI, AMX, etc.
 * Call cpu_detect() once at startup.
 */

#include "qat_cpu.h"
#include <cpuid.h>
#include <unistd.h>

/*
 * CPUID wrapper. leaf = EAX input, subleaf = ECX input.
 * Returns EAX, EBX, ECX, EDX via pointers.
 */
static void cpuid(uint32_t leaf, uint32_t subleaf,
                  uint32_t *eax, uint32_t *ebx, uint32_t *ecx, uint32_t *edx) {
    __cpuid_count(leaf, subleaf, *eax, *ebx, *ecx, *edx);
}

/*
 * Read XGETBV to check OS support for extended state (AVX, AVX-512, AMX).
 */
static uint64_t xgetbv(uint32_t index) {
    uint32_t eax, edx;
    __asm__ __volatile__("xgetbv" : "=a"(eax), "=d"(edx) : "c"(index));
    return ((uint64_t)edx << 32) | eax;
}

void cpu_detect(CpuFeatures *f) {
    memset(f, 0, sizeof(*f));

    uint32_t eax, ebx, ecx, edx;

    /* Get max standard leaf */
    cpuid(0, 0, &eax, &ebx, &ecx, &edx);
    uint32_t max_leaf = eax;

    /* Brand string (leaves 0x80000002-0x80000004) */
    cpuid(0x80000000, 0, &eax, &ebx, &ecx, &edx);
    if (eax >= 0x80000004) {
        uint32_t *brand = (uint32_t *)f->brand_string;
        cpuid(0x80000002, 0, &brand[0], &brand[1], &brand[2], &brand[3]);
        cpuid(0x80000003, 0, &brand[4], &brand[5], &brand[6], &brand[7]);
        cpuid(0x80000004, 0, &brand[8], &brand[9], &brand[10], &brand[11]);
        f->brand_string[48] = '\0';
    }

    /* Leaf 1: basic features */
    if (max_leaf >= 1) {
        cpuid(1, 0, &eax, &ebx, &ecx, &edx);
        /* ECX bit 20 = SSE4.2... actually SSE4.2 is bit 20 of ECX */
        f->has_sse42 = (ecx >> 20) & 1;
    }

    /* Check if OS supports XSAVE (needed for AVX and beyond) */
    cpuid(1, 0, &eax, &ebx, &ecx, &edx);
    bool os_xsave = (ecx >> 27) & 1;
    if (!os_xsave) goto done;

    uint64_t xcr0 = xgetbv(0);
    bool os_avx = (xcr0 & 0x6) == 0x6;           /* XMM + YMM state */
    bool os_avx512 = (xcr0 & 0xE6) == 0xE6;      /* XMM + YMM + ZMM + opmask */
    bool os_amx = (xcr0 & ((1ULL << 17) | (1ULL << 18))) ==
                  ((1ULL << 17) | (1ULL << 18));   /* XTILECFG + XTILEDATA */

    /* Leaf 7, subleaf 0: extended features */
    if (max_leaf >= 7) {
        cpuid(7, 0, &eax, &ebx, &ecx, &edx);

        if (os_avx) {
            f->has_avx2 = (ebx >> 5) & 1;
            f->has_fma  = true;  /* If AVX2, FMA is guaranteed on modern CPUs */
            /* Double-check FMA from leaf 1 */
            uint32_t eax1, ebx1, ecx1, edx1;
            cpuid(1, 0, &eax1, &ebx1, &ecx1, &edx1);
            f->has_fma = (ecx1 >> 12) & 1;
        }

        if (os_avx512) {
            f->has_avx512f  = (ebx >> 16) & 1;
            f->has_avx512bw = (ebx >> 30) & 1;
            f->has_avx512vnni = (ecx >> 11) & 1;
        }

        if (os_amx) {
            f->has_amx_tile = (edx >> 24) & 1;
            f->has_amx_int8 = (edx >> 25) & 1;
            f->has_amx_bf16 = (edx >> 22) & 1;
        }

        /* Leaf 7, subleaf 1 for AVX-512 BF16 */
        cpuid(7, 1, &eax, &ebx, &ecx, &edx);
        if (os_avx512) {
            f->has_avx512bf16 = (eax >> 5) & 1;
        }
    }

done:
    /* Get number of logical cores */
    f->num_cores = (int)sysconf(_SC_NPROCESSORS_ONLN);
    if (f->num_cores <= 0) f->num_cores = 1;
}

void cpu_features_print(const CpuFeatures *f) {
    printf("CPU: %s\n", f->brand_string[0] ? f->brand_string : "(unknown)");
    printf("Cores: %d\n", f->num_cores);
    printf("Features:\n");
    printf("  SSE4.2:       %s\n", f->has_sse42       ? "YES" : "no");
    printf("  AVX2:         %s\n", f->has_avx2         ? "YES" : "no");
    printf("  FMA:          %s\n", f->has_fma          ? "YES" : "no");
    printf("  AVX-512F:     %s\n", f->has_avx512f      ? "YES" : "no");
    printf("  AVX-512BW:    %s\n", f->has_avx512bw     ? "YES" : "no");
    printf("  AVX-512 VNNI: %s\n", f->has_avx512vnni   ? "YES" : "no");
    printf("  AVX-512 BF16: %s\n", f->has_avx512bf16   ? "YES" : "no");
    printf("  AMX-TILE:     %s\n", f->has_amx_tile     ? "YES" : "no");
    printf("  AMX-INT8:     %s\n", f->has_amx_int8     ? "YES" : "no");
    printf("  AMX-BF16:     %s\n", f->has_amx_bf16     ? "YES" : "no");
}
