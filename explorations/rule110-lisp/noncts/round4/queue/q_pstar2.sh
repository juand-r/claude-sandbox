#!/bin/bash
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
while kill -0 $(cat q_pstar.pid) 2>/dev/null; do sleep 10; done
echo "$(date -u +%H:%M) start pstar core slip 2"
nice -n 10 python pstar.py 22 125 2 pstar2.jsonl
echo "$(date -u +%H:%M) done"
