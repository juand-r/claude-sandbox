#!/bin/sh
# exhaustive front simulations: D trains (10,2) w<=30, C patterns (7,0) w<=34
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
nice -n 10 python3 frontsim.py trains_10_2_30.jsonl 0 700 fsD30.jsonl 10,11 > fsD30.log 2>&1
nice -n 10 python3 frontsim.py trains_7_0_34.jsonl 0 700 fsC34.jsonl 10,11 > fsC34.log 2>&1
echo ALLDONE >> fsC34.log
