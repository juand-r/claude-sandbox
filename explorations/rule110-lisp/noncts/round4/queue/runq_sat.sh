#!/bin/bash
# sequential SAT queue: each line of sat_queue.txt = "TIMEOUT ENV... cmd args"; one at a time
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
while read -r line; do
  [ -z "$line" ] && continue
  case "$line" in \#*) continue;; esac
  to=${line%% *}; rest=${line#* }
  echo "$(date -u +%H:%M:%S) START $rest"
  eval "timeout $to nice -n 10 env $rest"
  echo "$(date -u +%H:%M:%S) END rc=$? $rest"
done < sat_queue.txt
echo "$(date -u +%H:%M:%S) queue done"
