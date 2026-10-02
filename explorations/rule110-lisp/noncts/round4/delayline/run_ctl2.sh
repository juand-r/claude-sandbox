#!/bin/bash
# positive control for the Z branch of sat_refl.py: E + Y -> B^2-like Z + E (library: width 47)
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/delayline
for cb in 0 1 2; do
  timeout 1700 nice -n 10 python -u sat_refl.py --target pass2 --only_b --W 48 --WZ 30 --cb $cb --T 700 || echo "{\"target\": \"pass2\", \"cb\": $cb, \"timeout_or_error\": true}"
done
echo CTL_DONE
