#!/bin/sh
# W4 (route 23), physical gap 18: X + E^m -> E^(m+d_c) + A's with
# Delta_c = d_c - #A pairwise distinct (SAT assumes <= 6 A's per class;
# every witness re-simulated). One phase per call, 25-min cap each.
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/shuttle
cd $D
# (12,-6) part dropped: objects enumerates it (01:40)
for ph in 1 3 5 7 9 11 13; do
  grep -q "^G40 phiR $ph " w4b.log 2>/dev/null && continue
  timeout 1500 nice -n 10 python3 w4.py --px 42,-14 --wx 40 --gap 18 --dmin -6 --dmax 14 --depth 56 --T 560 --N 30 --distinct_delta --max 20 --phiR $ph --out w4b_G40.jsonl > w4b_tmp.log 2>&1
  echo "G40 phiR $ph exit $? $(grep -c '^{' w4b_tmp.log) solutions $(tail -1 w4b_tmp.log | cut -c1-80)" >> w4b.log
done
echo ALLDONE >> w4b.log
