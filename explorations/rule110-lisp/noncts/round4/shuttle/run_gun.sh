#!/bin/sh
# gun searches: front guns (B output) and back guns (A output), K = 1
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
for j in 0 1 2 3 4 5 6; do
  nice -n 10 python3 gun.py --face back --j $j --wL 20 --wR 20 --out gun_back_A.jsonl 2>&1 | grep -v "^SAT" | sed "s/^/back j=$j /" >> run_gun.log
done
for j in 1 2 3 4 5 6; do
  nice -n 10 python3 gun.py --face front --j $j --wL 24 --wR 20 --out gun_front_B.jsonl 2>&1 | grep -v "^SAT" | sed "s/^/front j=$j /" >> run_gun.log
done
echo ALLDONE >> run_gun.log
