#!/bin/bash
# S1 pass searches (theory 23:18 spec), separation-fixed version. Resumable per config.
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
run() { # p d WH WC T2 tag
  f=$D/s1_$6.jsonl
  if [ -f $f ] && [ $(grep -c . $f) -ge 196 ]; then return; fi
  rm -f $f
  nice -n 10 python3 s1_pass.py $1 $2 $3 $4 $5 $f > $D/s1_$6.log 2>&1
}
run 3 2 24 12 160 A_24_12
run 4 -2 24 12 160 B_24_12
run 3 2 30 16 200 A_30_16
run 4 -2 30 16 200 B_30_16
