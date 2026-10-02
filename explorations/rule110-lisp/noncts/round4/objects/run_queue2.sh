#!/bin/bash
# Serial queue v2 (one heavy process at a time). Resumable pieces.
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
C=$(cat $D/s1_child.pid)
while kill -0 $C 2>/dev/null; do sleep 10; done
# (1) can ANY content right of the back launch a phase domain? free cells
#     starting K cells inside the back (K=0: entirely outside the rod)
for K in 0 2 4 6 8; do
  if grep -q "\"overlap\": \[$K, 40\]" $D/launch2_K.jsonl 2>/dev/null; then continue; fi
  nice -n 10 python3 launch2.py 12 160 5 $D/launch2_K.jsonl --overlap $K 40 >> $D/launch2_K.log 2>&1
done
s1() { f=$D/s1_$6.jsonl
  if [ -f $f ] && [ $(grep -c . $f) -ge 196 ]; then return; fi
  nice -n 10 python3 s1_pass.py $1 $2 $3 $4 $5 $f >> $D/s1_$6.log 2>&1; }
s1 4 -2 24 12 160 B_24_12
nice -n 10 python3 bouncer_sat.py 22 22 16 16 180 $D/bR_22_16.jsonl --onlyR --s 0,2,4,6,8,10,12 --sV 0 >> $D/bR_22_16.log 2>&1
nice -n 10 python3 bouncer_sat.py 22 22 16 16 180 $D/bL_22_16.jsonl --onlyL --s 0,2,4,6,8,10,12 --sW 0 >> $D/bL_22_16.log 2>&1
PMIN=29 nice -n 10 python3 wallsat.py 000000111 63 30 $D/walls_p9_long.jsonl > $D/walls_p9_long.log 2>&1
PMIN=29 nice -n 10 python3 wallsat.py 00000010011 63 30 $D/walls_p11_long.jsonl > $D/walls_p11_long.log 2>&1
s1 3 2 30 16 200 A_30_16
s1 4 -2 30 16 200 B_30_16
