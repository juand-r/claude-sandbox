#!/bin/sh
# after run_w4b.sh: control that the G-lattice encoding reaches CLASS-
# DEPENDENT packets (d not all equal, no distinctness), 15-min cap per slip
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
P=$(cat run_w4b.pid)
while kill -0 $P 2>/dev/null; do sleep 30; done
for ph in 1 3 5 7 9 11 13; do
  timeout 900 nice -n 10 python3 w4.py --px 42,-14 --wx 40 --gap 18 --dmin -6 --dmax 14 --depth 56 --T 560 --N 30 --not_all_equal --max 3 --phiR $ph --out w4c_G40.jsonl > w4c_tmp.log 2>&1
  echo "G40-nae phiR $ph exit $? $(grep -c '^{' w4c_tmp.log) solutions" >> w4c.log
done
echo ALLDONE >> w4c.log
