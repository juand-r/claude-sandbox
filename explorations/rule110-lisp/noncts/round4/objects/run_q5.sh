#!/bin/bash
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
export WIN_VR=0.6667
nice -n 10 python3 launch2.py 36 480 5 $D/launchG_ctrl.jsonl --train 42 -14 24 4 --classes --target extend --win 40 >> $D/launchG_ctrl.log 2>&1
nice -n 10 python3 launch2.py 36 360 5 $D/launchG_16.jsonl --train 42 -14 16 4 --classes --win 40 >> $D/launchG_16.log 2>&1
nice -n 10 python3 launch2.py 36 480 5 $D/launchG_24.jsonl --train 42 -14 24 4 --classes --win 40 >> $D/launchG_24.log 2>&1
