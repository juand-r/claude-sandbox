#!/bin/sh
# A-trains (w<=22) and library right-movers vs the 36 NEW decorated fronts
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
for i in 1 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40; do
  nice -n 10 python3 frontsim.py trains_3_2_22.jsonl 0 700 dec/fsA22_f$i.jsonl 10,11 fronts_24_10.jsonl $i > dec/fsA22_f$i.log 2>&1
done
echo ALLDONE > dec/done.txt
