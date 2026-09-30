#!/bin/sh
cd "$(dirname "$0")"
while kill -0 16717 2>/dev/null; do sleep 20; done
python -u encross.py 3 2 24 300 --ns 1,2,3 >> encross_A24.log 2>&1
echo QUEUE2-DONE >> queue.log
