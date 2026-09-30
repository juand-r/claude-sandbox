#!/bin/sh
# single sequential queue (06:05): hard-gate G-train variant before G30
cd "$(dirname "$0")"
while kill -0 26648 2>/dev/null; do sleep 20; done
python -u hardgate.py 30 150 gtrain --k 0 --slips 0,1,2,3,4,5,6,7,8,9,10,11,12,13 >> hardgate.log 2>&1
python -u encross.py 42 -14 30 1100 --ns 1,2,3 >> encross_G30.log 2>&1
python -u copyspec.py 20 30 -8 300 --left --k 7,8,9,10,11 >> copy_F_anyleft.log 2>&1
echo QUEUE11-DONE >> queue.log
