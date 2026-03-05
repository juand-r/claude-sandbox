#!/bin/bash
# Watchdog for sweep_factored.sh
# Checks if the sweep is still running; if not, checks progress and restarts from where it left off.

cd /home/user/claude-sandbox/explorations/tokenization

SUMMARY="factored_results/summary.csv"
D_VALUES="4 8 16 32 64 128"

get_completed() {
    # Return list of d_in values already completed (have SUMMARY lines)
    if [ -f "$SUMMARY" ]; then
        grep "^din_sweep," "$SUMMARY" | awk -F',' '{print $6}' | sort -n
    fi
}

get_next_din() {
    local completed
    completed=$(get_completed)
    for d in $D_VALUES; do
        if ! echo "$completed" | grep -qx "$d"; then
            echo "$d"
            return
        fi
    done
    echo "DONE"
}

run_one_config() {
    local d_in=$1
    echo "[watchdog] Running d_in=$d_in at $(date)"

    QAT_DIR=../qat-cpu
    local bin_name="train_tok_binary_din${d_in}_dout128"
    local out_file="factored_results/binary_din${d_in}_dout128.txt"
    local csv_log="binary_din${d_in}_dout128.csv"

    # Compile
    gcc -std=c11 -Wall -Wextra -O2 -g -D_GNU_SOURCE -fopenmp -I${QAT_DIR} \
        -DTOKENIZE_MODE=0 -DD_IN=${d_in} -DD_OUT=128 -DN_STEPS=3000 \
        train_tok.c ${QAT_DIR}/memory.o ${QAT_DIR}/cpu_detect.o ${QAT_DIR}/kernels_scalar.o \
        ${QAT_DIR}/quantize.o ${QAT_DIR}/dispatch.o ${QAT_DIR}/qat_linear.o \
        ${QAT_DIR}/layers.o ${QAT_DIR}/optimizer.o ${QAT_DIR}/loss.o \
        ${QAT_DIR}/kernels_avx2.o ${QAT_DIR}/kernels_vnni.o ${QAT_DIR}/kernels_bf16.o \
        -o "$bin_name" -lm -fopenmp

    # Run
    OMP_NUM_THREADS=2 ./"$bin_name" > "$out_file" 2>&1
    local exit_code=$?

    echo "[watchdog] d_in=$d_in finished with exit code $exit_code at $(date)"
    cat "$out_file"

    if [ $exit_code -eq 0 ]; then
        # Extract summary
        local summary
        summary=$(grep "^SUMMARY:" "$out_file" | sed 's/^SUMMARY://')
        if [ -n "$summary" ]; then
            echo "din_sweep,${summary}" >> "$SUMMARY"
        fi
        # Move CSV
        [ -f "$csv_log" ] && mv "$csv_log" factored_results/
        # Cleanup binary
        rm -f "$bin_name"
    fi

    return $exit_code
}

echo "[watchdog] Starting at $(date)"
echo "[watchdog] Completed so far: $(get_completed | tr '\n' ' ')"

while true; do
    next=$(get_next_din)
    if [ "$next" = "DONE" ]; then
        echo "[watchdog] All d_in configs complete!"
        echo "[watchdog] Summary:"
        cat "$SUMMARY"
        break
    fi

    echo "[watchdog] Next: d_in=$next"
    run_one_config "$next"

    if [ $? -ne 0 ]; then
        echo "[watchdog] ERROR: d_in=$next failed. Retrying in 10s..."
        sleep 10
    fi
done

echo "[watchdog] Done at $(date)"
