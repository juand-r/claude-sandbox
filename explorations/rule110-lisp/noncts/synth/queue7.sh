#!/bin/sh
# replaces queue5/queue6 (05:45): zsplit before the E_n transport runs
cd "$(dirname "$0")"
while kill -0 25250 2>/dev/null; do sleep 20; done
python -u zsplit.py 24 900 --only-a --pk 0 --s 0 >> zsplit.log 2>&1
python -u zsplit.py 24 900 --only-a --pk 0 --debris >> zsplit.log 2>&1
python -u encross.py 3 2 24 300 --ns 1,2,3 >> encross_A24.log 2>&1
python -u encross.py 42 -14 30 1100 --ns 1,2,3 >> encross_G30.log 2>&1
python -u copyspec.py 20 30 -8 300 --left --k 7,8,9,10,11 >> copy_F_anyleft.log 2>&1
echo QUEUE7-DONE >> queue.log
