#!/bin/sh
# Batch 2 (priority order): Y in the Bbar family, widths X 30 / Y 30,
# n = m = 4, all 9 class pairs per (sX, K). Resumable (done runs skipped).
cd "$(dirname "$0")"
P="python3 sat_shuttle.py --wx 30 --wy 30 --ns1 4 --ns2 4 --T1 240 --T2 280 --py 12,-6"
$P --sx 8 --K 2
$P --sx 8 --K 1
$P --sx 2 --K 1
$P --sx 8 --K -1
$P --sx 2 --K -1
$P --sx 10 --K 2
$P --sx 4 --K 2
echo ALLDONE
