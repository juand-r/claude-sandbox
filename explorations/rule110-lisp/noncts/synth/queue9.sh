#!/bin/sh
# replaces queue8 (05:57): joint zsplit needs the slot geometry (asked architect)
cd "$(dirname "$0")"
while kill -0 26648 2>/dev/null; do sleep 20; done
python -u encross.py 42 -14 30 1100 --ns 1,2,3 >> encross_G30.log 2>&1
python -u copyspec.py 20 30 -8 300 --left --k 7,8,9,10,11 >> copy_F_anyleft.log 2>&1
echo QUEUE9-DONE >> queue.log
