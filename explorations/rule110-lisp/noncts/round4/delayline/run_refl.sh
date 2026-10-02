#!/bin/bash
# reusable-reflector SAT campaign (sat_refl.py), all 9 class pairs, W 30
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/delayline
for ca in 0 1 2; do for cb in 0 1 2; do
  timeout 1500 nice -n 10 python -u sat_refl.py --target refl --W 30 --WZ 30 --ca $ca --cb $cb --T 700 || echo "{\"target\": \"refl\", \"ca\": $ca, \"cb\": $cb, \"timeout_or_error\": true}"
done; done
echo CAMPAIGN_DONE
