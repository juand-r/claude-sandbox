#!/bin/sh
# waits for the gun batch (PID in run_gun.pid), then builds the bouncer tables
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
P=$(cat run_gun.pid)
while kill -0 $P 2>/dev/null; do sleep 20; done
nice -n 10 python3 bounce.py heads_L.jsonl trains_7_0_20.jsonl L bounce_L.jsonl 500 > bounce_L.log 2>&1
nice -n 10 python3 bounce.py heads_R.jsonl trains_7_0_20.jsonl R bounce_R.jsonl 500 > bounce_R.log 2>&1
echo ALLDONE >> bounce_R.log
