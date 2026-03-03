#!/bin/bash
#
# sweep_factored.sh - Sweep factored embedding dimensions (d_in, d_out)
#
# Runs for binary (mode 0) and bigram (mode 4) only.
# d_model=128 is fixed throughout.
#
# Phase 1: Sweep d_in with d_out=DIM (128)
# Phase 2: Sweep d_out with d_in=DIM (128)
#
# Usage:
#   ./sweep_factored.sh              # full sweep
#   ./sweep_factored.sh din          # phase 1 only (d_in sweep)
#   ./sweep_factored.sh dout         # phase 2 only (d_out sweep)
#   ./sweep_factored.sh din binary   # d_in sweep, binary only
#   ./sweep_factored.sh dout bigram  # d_out sweep, bigram only

set -e

QAT_DIR=../qat-cpu
CC=gcc
CFLAGS="-std=c11 -Wall -Wextra -O2 -g -D_GNU_SOURCE -fopenmp -I${QAT_DIR}"
LDFLAGS="-lm -fopenmp"

QAT_OBJ="${QAT_DIR}/memory.o ${QAT_DIR}/cpu_detect.o ${QAT_DIR}/kernels_scalar.o \
         ${QAT_DIR}/quantize.o ${QAT_DIR}/dispatch.o ${QAT_DIR}/qat_linear.o \
         ${QAT_DIR}/layers.o ${QAT_DIR}/optimizer.o ${QAT_DIR}/loss.o \
         ${QAT_DIR}/kernels_avx2.o ${QAT_DIR}/kernels_vnni.o ${QAT_DIR}/kernels_bf16.o"

# Config
DIM=128
N_STEPS=3000
D_VALUES="1 2 4 8 16 32 64 128"

# Modes to sweep: "0 4" = binary and bigram
MODES_BINARY="0"
MODES_BIGRAM="4"
MODE_NAMES=("binary" "" "" "" "bigram")

PHASE="${1:-all}"     # din, dout, or all
MODE_FILTER="${2:-}"  # binary, bigram, or empty for both

RESULTS_DIR="factored_results"
mkdir -p "$RESULTS_DIR"

SUMMARY_FILE="${RESULTS_DIR}/summary.csv"

# Write CSV header if new
if [ ! -f "$SUMMARY_FILE" ]; then
    echo "phase,mode,vocab,tok_per_char,seq_len,d_in,d_out,n_params,bpc,loss,ppl,time_sec,random_bpc" \
        > "$SUMMARY_FILE"
fi

# Ensure QAT objects are built
make -C "$QAT_DIR" memory.o cpu_detect.o kernels_scalar.o quantize.o dispatch.o \
    qat_linear.o layers.o optimizer.o loss.o kernels_avx2.o kernels_vnni.o kernels_bf16.o

# Ensure data file
[ -f shakespeare.txt ] || ln -sf ${QAT_DIR}/shakespeare.txt .

get_modes() {
    case "$MODE_FILTER" in
        binary) echo "0" ;;
        bigram) echo "4" ;;
        *)      echo "0 4" ;;
    esac
}

run_one() {
    local mode=$1
    local d_in=$2
    local d_out=$3
    local phase_name=$4

    local mode_name="${MODE_NAMES[$mode]}"
    local bin_name="train_tok_${mode_name}_din${d_in}_dout${d_out}"

    echo "=== ${phase_name}: mode=${mode_name} d_in=${d_in} d_out=${d_out} ==="

    # Compile
    $CC $CFLAGS \
        -DTOKENIZE_MODE=${mode} \
        -DD_IN=${d_in} \
        -DD_OUT=${d_out} \
        -DN_STEPS=${N_STEPS} \
        train_tok.c $QAT_OBJ -o "$bin_name" $LDFLAGS

    # Run and capture output
    local out_file="${RESULTS_DIR}/${mode_name}_din${d_in}_dout${d_out}.txt"
    ./"$bin_name" 2>&1 | tee "$out_file"

    # Extract SUMMARY line and append to CSV
    local summary
    summary=$(grep "^SUMMARY:" "$out_file" | sed 's/^SUMMARY://')
    if [ -n "$summary" ]; then
        echo "${phase_name},${summary}" >> "$SUMMARY_FILE"
    fi

    # Move CSV log to results dir
    local csv_log="${mode_name}_din${d_in}_dout${d_out}.csv"
    [ -f "$csv_log" ] && mv "$csv_log" "${RESULTS_DIR}/"

    # Clean up binary
    rm -f "$bin_name"

    echo ""
}

# Phase 1: Sweep d_in with d_out = DIM
if [ "$PHASE" = "din" ] || [ "$PHASE" = "all" ]; then
    echo "============================================"
    echo "Phase 1: Sweeping d_in (d_out=${DIM} fixed)"
    echo "============================================"
    echo ""

    for mode in $(get_modes); do
        for d_in in $D_VALUES; do
            run_one "$mode" "$d_in" "$DIM" "din_sweep"
        done
    done
fi

# Phase 2: Sweep d_out with d_in = DIM
if [ "$PHASE" = "dout" ] || [ "$PHASE" = "all" ]; then
    echo "============================================"
    echo "Phase 2: Sweeping d_out (d_in=${DIM} fixed)"
    echo "============================================"
    echo ""

    for mode in $(get_modes); do
        for d_out in $D_VALUES; do
            run_one "$mode" "$DIM" "$d_out" "dout_sweep"
        done
    done
fi

echo "============================================"
echo "Sweep complete. Results in ${RESULTS_DIR}/"
echo "Summary: ${SUMMARY_FILE}"
echo "============================================"
echo ""

# Print summary table
echo "--- Summary Table ---"
column -t -s',' "$SUMMARY_FILE"
