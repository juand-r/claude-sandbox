#!/bin/sh
cd "$(dirname "$0")"
while kill -0 20556 2>/dev/null; do sleep 20; done
python -u hardgate.py 30 150 none --k 0,1,2,3,4,5,6,7,8 >> hardgate.log 2>&1
python -u hardgate.py 30 150 GB4 --k 0,1,2,3,4,5,6,7,8 >> hardgate.log 2>&1
python -u encross.py 3 2 24 300 --ns 1,2,3 >> encross_A24.log 2>&1
python -u copyspec.py 20 30 -8 300 --left --k 7,8,9,10,11 >> copy_F_anyleft.log 2>&1
echo QUEUE3-DONE >> queue.log
