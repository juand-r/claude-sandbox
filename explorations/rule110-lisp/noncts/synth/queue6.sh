#!/bin/sh
# after queue5 finishes: compound -> (19,23) split pair, scene (a) only first
cd "$(dirname "$0")"
until grep -q QUEUE5-DONE queue.log 2>/dev/null; do sleep 30; done
python -u zsplit.py 24 900 --only-a --pk 0 --s 0 >> zsplit.log 2>&1
python -u zsplit.py 24 900 --only-a --pk 0 --debris >> zsplit.log 2>&1
echo QUEUE6-DONE >> queue.log
