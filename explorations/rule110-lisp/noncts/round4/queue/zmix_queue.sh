#!/bin/bash
# sequential queue of zmix screens (one heavy process at a time)
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
for spec in "Ebar Ebar -330 -190 150" "E^3 Ebar -150 37 150" "Ebar E^3 -150 37 150" "E^3 E^3 -150 37 150" "E E^5 -150 37 150" "E^5 E -150 37 150" "E^2 E^4 -150 37 150" "E^4 E^2 -150 37 150"; do
  set -- $spec
  echo "$(date -u +%H:%M) start $spec"
  nice -n 10 python zmix.py $1 $2 $3 $4 $5 zmix.jsonl
done
echo "$(date -u +%H:%M) all done"
