#!/bin/bash
# Queue 2: wall converter (fixed stable-scene encoding), then Bbar crossing.
cd "$(dirname "$0")"
for sB in 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
  python3 sat_conv.py 24 $sB 24 250 --ns 2,3 >> sat_conv.log 2>&1
done
python3 sat_crossL.py 12 -6 24 24 350 --ns 3 --kY "0;1;2" >> sat_crossL.log 2>&1
