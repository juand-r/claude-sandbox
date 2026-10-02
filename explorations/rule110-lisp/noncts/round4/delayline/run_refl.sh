#!/bin/bash
# reusable-reflector SAT campaign (sat_refl.py), W 30, T 900 (reaction of a
# width-30 G packet ends by ~15*34 steps; Z needs ~250 more to separate)
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/delayline
timeout 1700 nice -n 10 python -u sat_refl.py --target walk --W 30 --ca 0 --cb 2 --T 900 || echo '{"control": "walk", "timeout_or_error": true}'
for ca in 0 1 2; do for cb in 0 1 2; do
  timeout 1700 nice -n 10 python -u sat_refl.py --target refl --W 30 --WZ 30 --ca $ca --cb $cb --T 900 || echo "{\"target\": \"refl\", \"ca\": $ca, \"cb\": $cb, \"timeout_or_error\": true}"
done; done
echo CAMPAIGN_DONE
