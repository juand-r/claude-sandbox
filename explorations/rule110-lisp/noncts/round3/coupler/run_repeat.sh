#!/bin/sh
# Triple coupling + R1 correctors: enumerate the two N corrector classes.
cd "$(dirname "$0")"
for a in 0 1 2; do for b in 0 1 2; do
  echo "== N1 class $a, N2 class $b"
  python3 repeat.py 3 JIJIJINZZZZZZZNJINN 0,1 6:$a,14:$b
done; done
echo ALLDONE
