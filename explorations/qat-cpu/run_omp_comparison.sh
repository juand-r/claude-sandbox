#!/bin/bash
# 4-way comparison of attention OMP configurations
# All QAT mode, 300 steps, same config as convergence runs
set -e

COMMON_TRAIN="-DDIM=1024 -DN_LAYERS=6 -DN_HEADS=16 -DHIDDEN_DIM=4096 -DSEQ_LEN=128 -DMAX_SEQ_LEN=256 -DN_STEPS=300 -DEVAL_EVERY=50 -DGEN_EVERY=300 -DTRAIN_MODE=2 -DLR=0.000300f -DBATCH_SIZE=8"
BASE_FLAGS="-std=c11 -Wall -Wextra -O2 -g -D_GNU_SOURCE -fopenmp"

# Clean everything
rm -f *.o train_omp_* omp_none.csv omp_bwd.csv omp_fwd.csv omp_both.csv

# Build variant 1: no OMP on attention
echo "Building: no OMP attention..."
make train_qat CFLAGS_BASE="$BASE_FLAGS" TRAIN_CFLAGS="$COMMON_TRAIN -DCSV_PREFIX=omp_none" 2>&1 | tail -1
cp train_qat train_omp_none
rm -f layers.o train.o

# Build variant 2: BWD OMP only (the old default)
echo "Building: BWD OMP only..."
make train_qat CFLAGS_BASE="$BASE_FLAGS -DATTN_OMP_BWD" TRAIN_CFLAGS="$COMMON_TRAIN -DCSV_PREFIX=omp_bwd" 2>&1 | tail -1
cp train_qat train_omp_bwd
rm -f layers.o train.o

# Build variant 3: FWD OMP only
echo "Building: FWD OMP only..."
make train_qat CFLAGS_BASE="$BASE_FLAGS -DATTN_OMP_FWD" TRAIN_CFLAGS="$COMMON_TRAIN -DCSV_PREFIX=omp_fwd" 2>&1 | tail -1
cp train_qat train_omp_fwd
rm -f layers.o train.o

# Build variant 4: FWD+BWD OMP
echo "Building: FWD+BWD OMP..."
make train_qat CFLAGS_BASE="$BASE_FLAGS -DATTN_OMP_FWD -DATTN_OMP_BWD" TRAIN_CFLAGS="$COMMON_TRAIN -DCSV_PREFIX=omp_both" 2>&1 | tail -1
cp train_qat train_omp_both

echo ""
echo "All 4 binaries built. Running..."
echo ""

# Run each variant
for variant in none bwd fwd both; do
    echo "========================================"
    echo "Running: OMP=$variant"
    echo "========================================"
    ./train_omp_$variant 2>&1
    echo ""
done

echo "All done. CSVs: omp_none.csv omp_bwd.csv omp_fwd.csv omp_both.csv"
