#!/bin/sh
# sequential queue (one heavy process at a time), started 05:17
cd "$(dirname "$0")"
while kill -0 21893 2>/dev/null; do sleep 20; done
python -u hardgate.py 30 150 GB4 --k 0,1,2,3,4,5,6,7,8 >> hardgate.log 2>&1
python -u zc.py 24 900 --k 0 >> zc.log 2>&1
python -u zc.py 24 900 --k 0 --debris >> zc.log 2>&1
python -u encross.py 3 2 24 300 --ns 1,2,3 >> encross_A24.log 2>&1
python -u encross.py 42 -14 30 1100 --ns 1,2,3 >> encross_G30.log 2>&1
python -u copyspec.py 20 30 -8 300 --left --k 7,8,9,10,11 >> copy_F_anyleft.log 2>&1
echo QUEUE5-DONE >> queue.log
