#!/bin/sh
# sequential queue (one heavy process at a time, per the lead's request)
cd "$(dirname "$0")"
while pgrep -f "python gpackets.py" > /dev/null; do sleep 20; done
python cpairsF.py > cpairsF.log 2>&1
python rerun_unsettled.py 20000 >> cpairsF.log 2>&1
python regions.py >> cpairsF.log 2>&1
python query.py > /dev/null 2>> cpairsF.log
python verify.py >> cpairsF.log 2>&1
echo QUEUE-DONE >> cpairsF.log
