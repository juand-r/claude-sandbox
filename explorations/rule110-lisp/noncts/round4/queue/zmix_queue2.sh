#!/bin/bash
# runs after zmix_queue.sh (PID in zmix_queue.pid) finishes
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
while kill -0 $(cat zmix_queue.pid) 2>/dev/null; do sleep 20; done
for spec in "Ebar Ebar -330 37 150" "E^3 Ebar -150 37 120" "Ebar E^3 -150 37 120"; do
  set -- $spec
  echo "$(date -u +%H:%M) start tight $spec"
  nice -n 10 python zmix.py $1 $2 $3 $4 $5 zmix_tight.jsonl tight
done
echo "$(date -u +%H:%M) all done"
