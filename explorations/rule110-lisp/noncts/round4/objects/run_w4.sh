#!/bin/bash
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
nice -n 10 python3 w4_enum.py 6 16 400 $D/w4_enum.jsonl --cond notallequal --max 100 >> $D/w4_enum.log 2>&1
nice -n 10 python3 w4_enum.py 6 24 500 $D/w4_enum.jsonl --cond notallequal --max 100 >> $D/w4_enum.log 2>&1
