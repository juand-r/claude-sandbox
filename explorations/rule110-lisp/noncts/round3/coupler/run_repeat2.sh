#!/bin/sh
# Single coupling + two N correctors: J I N Z^7 N J I N N, v1 = 0 (two
# couplings) and v1 = 5 (one), all 9 corrector class pairs.
cd "$(dirname "$0")"
for a in 0 1 2; do for b in 0 1 2; do
  echo "== N1 class $a, N2 class $b"
  python3 repeat.py 3 JINZZZZZZZNJINN 0,5 2:$a,10:$b
done; done
echo ALLDONE
