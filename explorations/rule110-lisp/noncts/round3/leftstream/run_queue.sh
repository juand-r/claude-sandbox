#!/bin/bash
# Queue (one heavy process at a time; every step resumable):
# 1. wait for A-train W24 crossing (PID 10621);
# 2. left-mover crossing, B-trains W24 joint n 2,3;
# 3. wall converter (theory s.6.5): F = I_L, B free W24, every slip sB,
#    X free slip 6, n 2,3, T2 250;
# 4. left-mover crossing, Bbar-trains W24, n 3, classes 0,1,2.
cd "$(dirname "$0")"
while ps -p 10621 > /dev/null; do sleep 10; done
python3 sat_crossL.py 4 -2 24 24 350 --ns 2,3 >> sat_crossL.log 2>&1
for sB in 0 1 2 3 4 5 6 7 8 9 10 11 12 13; do
  python3 sat_conv.py 24 $sB 24 250 --ns 2,3 >> sat_conv.log 2>&1
done
python3 sat_crossL.py 12 -6 24 24 350 --ns 3 --kY "0;1;2" >> sat_crossL.log 2>&1
