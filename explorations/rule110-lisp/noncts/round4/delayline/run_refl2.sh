#!/bin/bash
# reflector SAT, wider (W 36, T 1000) strict, then W 30 with a moved closed window
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/delayline
for ca in 0 1 2; do for cb in 0 1 2; do
  timeout 1700 nice -n 10 python -u sat_refl.py --target refl --W 36 --WZ 30 --ca $ca --cb $cb --T 1000 || echo "{\"target\": \"refl\", \"W\": 36, \"ca\": $ca, \"cb\": $cb, \"timeout_or_error\": true}"
done; done
for ca in 0 1 2; do for cb in 0 1 2; do
  timeout 1700 nice -n 10 python -u sat_refl.py --target refl --W 30 --WZ 30 --ca $ca --cb $cb --T 900 --moved || echo "{\"target\": \"refl\", \"moved\": true, \"ca\": $ca, \"cb\": $cb, \"timeout_or_error\": true}"
done; done
echo CAMPAIGN_DONE
