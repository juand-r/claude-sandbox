#!/bin/sh
cd "$(dirname "$0")"
until grep -q QUEUE9-DONE queue.log 2>/dev/null; do sleep 30; done
python -u hardgate.py 30 150 gtrain --k 0 --slips 0,1,2,3,4,5,6,7,8,9,10,11,12,13 >> hardgate.log 2>&1
echo QUEUE10-DONE >> queue.log
