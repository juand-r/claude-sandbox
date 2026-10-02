#!/bin/bash
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
while kill -0 29693 2>/dev/null; do sleep 10; done
nice -n 10 python pstar.py 50 125 9 pstar9.jsonl
echo done
