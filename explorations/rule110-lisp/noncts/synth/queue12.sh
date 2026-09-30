#!/bin/sh
cd "$(dirname "$0")"
until grep -q QUEUE11-DONE queue.log 2>/dev/null; do sleep 30; done
python -u hardgate.py 44 170 none --k 0 >> hardgate.log 2>&1
python -u hardgate.py 44 170 GB4 --k 0 >> hardgate.log 2>&1
python -u hardgate.py 44 170 gtrain --k 0 --slips 0,1,2,3,4,5,6,7,8,9,11,12,13 >> hardgate.log 2>&1
echo QUEUE12-DONE >> queue.log
