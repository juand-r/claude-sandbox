#!/bin/bash
# SAT for Z2 (zero answer = Z_L train), widths in order; one process at a time.
cd "$(dirname "$0")"
for W in 32 40 48; do
  python3 sat_zero.py 3 2 $W 360 ZL >> sat_zl.log 2>&1
done
