#!/bin/sh
# waits for queue3 to finish (marker in queue.log), then G-speed transport through E_n
cd "$(dirname "$0")"
until grep -q QUEUE3-DONE queue.log 2>/dev/null; do sleep 30; done
python -u encross.py 42 -14 30 1100 --ns 1,2,3 >> encross_G30.log 2>&1
echo QUEUE4-DONE >> queue.log
