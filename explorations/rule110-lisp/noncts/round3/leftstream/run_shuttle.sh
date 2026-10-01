#!/bin/bash
# Shuttle SAT sweep (resumable): B-trains then Bbar-trains, k = 2 then 1,
# every slip sY; single m = 3 (R2 back) and n = 4 (R1 front).
cd "$(dirname "$0")"
for k in 2 1; do
  for sY in 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
    python3 sat_shuttle.py 4 -2 20 $sY 20 $k 300 --ms 3 --ns 4 >> sat_shuttle.log 2>&1
  done
done
for k in 2 1; do
  for sY in 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
    python3 sat_shuttle.py 12 -6 24 $sY 20 $k 300 --ms 3 --ns 4 >> sat_shuttle.log 2>&1
  done
done
