#!/bin/bash
# Build and validate several M2 programs with my own assembler (sequential:
# one heavy process at a time).
cd "$(dirname "$0")"
for spec in "JJJJJZZZZZZJJJJJZZZZZZ 6" "JJJJJJZZZZZZZJJJJJJZZZZZZZJJJJJJZZZZZZZ 6" "ZZZZZZZZZ 6" "XZZZZZZZZZ 6"; do
  set -- $spec
  echo "=== build $1 vmax $2"
  python3 adaptive_ca.py $1 $2 | tail -2
  if [ -f adaptive_$1.json ] && grep -q '"ok": true' adaptive_$1.json; then
    echo "=== validate $1"
    python3 m2_validate.py adaptive_$1.json 12
  fi
done
echo BATCH DONE
