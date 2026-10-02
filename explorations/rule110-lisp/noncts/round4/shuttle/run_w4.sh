#!/bin/sh
# W4 enumeration (route 23): class-dependent back reactions, Delta per class
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
nice -n 10 python3 w4.py --px 12,-6 --wx 30 --dmin -6 --dmax 14 --depth 56 --T 220 --not_all_equal --max 150 --N 30 --out w4_B30.jsonl > w4_B30.log 2>&1
nice -n 10 python3 w4.py --px 42,-14 --wx 40 --dmin -6 --dmax 14 --depth 56 --T 320 --not_all_equal --max 150 --N 30 --out w4_G40.jsonl > w4_G40.log 2>&1
echo ALLDONE >> w4_G40.log
