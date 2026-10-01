#!/bin/bash
# Crossing sweep (resumable): conv mode, ns 2,3, all slips and classes.
cd "$(dirname "$0")"
for W in 24 32 40; do
  python3 sat_cross.py $W $W 350 conv --ns 2,3 >> sat_cross.log 2>&1
done
