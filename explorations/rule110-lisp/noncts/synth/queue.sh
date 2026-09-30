#!/bin/sh
# Sequential job queue (lead's CPU budget: one heavy process per agent).
# Waits for the running spec-Z job, then runs the remaining searches one
# after another. Each job appends to its own log.
cd "$(dirname "$0")"
while kill -0 13401 2>/dev/null; do sleep 20; done
python -u encross.py 4 -2 24 400 --ns 1,2,3 --s 4,5,6,7,8,9,10,11,12,13 >> encross_B24.log 2>&1
python -u pump.py 20 460 --D0 51 --k 1 --s 1,2,3,4,5,6,7,8,9,10,11,12,13 >> pump_W20.log 2>&1
python -u pump.py 20 460 --D0 51 --k 2,3 >> pump_W20.log 2>&1
python -u pump.py 20 460 --D0 65 >> pump_W20.log 2>&1
python -u copyspec.py 20 30 -8 300 --left --k 7,8,9,10,11 >> copy_F_anyleft.log 2>&1
echo QUEUE-DONE >> queue.log
