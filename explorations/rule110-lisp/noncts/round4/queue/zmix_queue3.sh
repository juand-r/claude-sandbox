#!/bin/bash
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
while kill -0 $(cat zmix_queue2.pid) 2>/dev/null; do sleep 20; done
for spec in "E^3 E^3 -150 37 120" "E E^5 -150 37 120" "E^5 E -150 37 120" "E^2 E^4 -150 37 120" "E^4 E^2 -150 37 120"; do
  set -- $spec
  echo "$(date -u +%H:%M) start tight $spec"
  nice -n 10 python zmix.py $1 $2 $3 $4 $5 zmix_tight.jsonl tight
done
echo "$(date -u +%H:%M) all done"
