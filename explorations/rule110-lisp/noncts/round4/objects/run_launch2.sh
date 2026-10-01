#!/bin/bash
# Wall-launch SAT, B-lattice trains, long rod and long time (resumable by width)
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
for W in 24 40 56; do
  if grep -q "\"train\": \[4, -2, $W, 4, 0, 13\]" launch2_B400.jsonl 2>/dev/null; then continue; fi
  nice -n 10 python3 launch2.py 36 400 5 $D/launch2_B400.jsonl --train 4 -2 $W 4 --taus 0 --pRs 0,2,4,6,8,10,12,13
done
