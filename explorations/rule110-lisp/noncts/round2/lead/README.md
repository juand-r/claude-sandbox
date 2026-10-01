# Lead's spot-checks of round-2 claims

Re-run by the lead with the agents' own reproduce commands (not their logs):
- `lead_check_gate.log`: `gate/verify_ra.py` on (Z6 N)^10 with its posted
  classes, inputs 0..9: 10/10 = (v-10) mod 7, no garbage, CA == glidersim.
- `lead_check_verify.log`: `verify/plan_check.py` on (J^5 Z^6)^4 parity,
  planned on 0..12, tested on 0..15: PASS (3 out-of-sample inputs), control
  changes 1/13 inputs.
