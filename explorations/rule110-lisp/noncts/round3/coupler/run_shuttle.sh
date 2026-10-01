#!/bin/sh
# Sequential joint shuttle SAT runs (one heavy process at a time).
cd "$(dirname "$0")"
P="python3 sat_shuttle.py --wx 18 --wy 24 --ns1 4 --ns2 4 --T1 220 --T2 260"
$P --py 12,-6 --sx 8 --K 2
$P --py 12,-6 --sx 8 --K 1
$P --py 12,-6 --sx 8 --K -1
$P --py 12,-6 --sx 2 --K 1
$P --py 12,-6 --sx 2 --K -1
$P --py 4,-2 --sx 8 --K 1
$P --py 4,-2 --sx 8 --K -1
$P --py 4,-2 --sx 6 --K 1
echo ALLDONE
