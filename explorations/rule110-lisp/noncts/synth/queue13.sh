#!/bin/sh
# final queue (06:40): after queue11 (G30 transport, copy-left), only the
# two strict hard-gate variants at width 44
cd "$(dirname "$0")"
until grep -q QUEUE11-DONE queue.log 2>/dev/null; do sleep 30; done
python -u hardgate.py 44 170 none --k 0 >> hardgate.log 2>&1
python -u hardgate.py 44 170 GB4 --k 0 >> hardgate.log 2>&1
echo QUEUE13-DONE >> queue.log
