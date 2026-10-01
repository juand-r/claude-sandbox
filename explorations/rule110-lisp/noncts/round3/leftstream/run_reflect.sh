#!/bin/bash
# Reflection at R1's inner face, Y = Bbar: k = 2,1,3; widths 24, 32; ns 3,4.
cd "$(dirname "$0")"
for W in 24 32; do
  for k in 2 1 3; do
    python3 sat_reflect.py $W $k 450 --Y Bbar --ns 3,4 >> sat_reflect.log 2>&1
  done
done
