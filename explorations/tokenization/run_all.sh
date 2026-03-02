#!/bin/bash
# Run all 5 tokenization experiments and collect results.
# Run from explorations/tokenization/ directory.

set -e

echo "========================================"
echo "Tokenization Strategy Comparison"
echo "========================================"
echo ""

# Build all binaries
echo "Building all configurations..."
make -j4 all 2>&1 | tail -5
echo ""

# Run experiments from fastest to slowest
MODES="char nibble base4 bigram binary"

for mode in $MODES; do
    echo "========================================"
    echo "Running: $mode"
    echo "========================================"
    ./train_tok_$mode 2>&1 | tee ${mode}_output.txt
    echo ""
done

# Collect summary
echo "========================================"
echo "COMPARISON TABLE"
echo "========================================"
echo ""
printf "%-10s %7s %8s %7s %8s %8s %8s %8s %10s\n" \
    "Mode" "Vocab" "Tok/Chr" "SeqLen" "Params" "BPC" "Loss" "PPL" "Time(s)"
printf "%-10s %7s %8s %7s %8s %8s %8s %8s %10s\n" \
    "----" "-----" "-------" "------" "------" "---" "----" "---" "-------"

for mode in $MODES; do
    line=$(grep "^SUMMARY:" ${mode}_output.txt | sed 's/SUMMARY://')
    if [ -n "$line" ]; then
        name=$(echo "$line" | cut -d, -f1)
        vocab=$(echo "$line" | cut -d, -f2)
        tpc=$(echo "$line" | cut -d, -f3)
        seqlen=$(echo "$line" | cut -d, -f4)
        params=$(echo "$line" | cut -d, -f5)
        bpc=$(echo "$line" | cut -d, -f6)
        loss=$(echo "$line" | cut -d, -f7)
        ppl=$(echo "$line" | cut -d, -f8)
        time=$(echo "$line" | cut -d, -f9)
        printf "%-10s %7s %8s %7s %8s %8s %8s %8s %10s\n" \
            "$name" "$vocab" "$tpc" "$seqlen" "$params" "$bpc" "$loss" "$ppl" "$time"
    fi
done

echo ""
echo "CSV files: binary.csv base4.csv nibble.csv char.csv bigram.csv"
echo "Done."
