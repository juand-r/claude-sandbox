#!/bin/sh
# extension tables: all physical heads x the 291 wall types that
# reflections produce but the 20-cell wall list lacks (walls_frontier.jsonl)
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
P=$(cat frontier.pid)
while kill -0 $P 2>/dev/null; do sleep 20; done
nice -n 10 python3 bounce.py heads_L_phys.jsonl walls_frontier.jsonl L ext_L.jsonl 500 > ext_L.log 2>&1
nice -n 10 python3 bounce.py heads_R_phys.jsonl walls_frontier.jsonl R ext_R.jsonl 500 > ext_R.log 2>&1
nice -n 10 python3 export.py LR ext_table.jsonl heads_R_phys.jsonl heads_L_phys.jsonl walls_frontier.jsonl ext_L.jsonl ext_R.jsonl > ext_export.log 2>&1
echo ALLDONE >> ext_export.log
