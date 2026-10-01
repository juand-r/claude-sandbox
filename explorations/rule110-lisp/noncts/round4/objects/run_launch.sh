#!/bin/bash
# Wall-launch SAT, B-lattice trains, widths 24/32/40 (resumable by width)
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
for W in 24 32 40; do
  if grep -q "\"train\": \[4, -2, $W, 4, 0, 13\]" launch2_B.jsonl 2>/dev/null; then continue; fi
  nice -n 10 python3 launch2.py 12 160 5 $D/launch2_B.jsonl --train 4 -2 $W 4 --taus 0
done
