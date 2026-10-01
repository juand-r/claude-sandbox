#!/bin/bash
# After the A-train W24 crossing run (PID 10621) ends: left-mover crossings
# from the back. B-trains (one class, joint n = 2,3), then Bbar and G
# families (3 classes, single n = 3 per instance, all three classes).
cd "$(dirname "$0")"
while ps -p 10621 > /dev/null; do sleep 10; done
python3 sat_crossL.py 4 -2 24 24 350 --ns 2,3 >> sat_crossL.log 2>&1
python3 sat_crossL.py 12 -6 24 24 350 --ns 3 --kY "0;1;2" >> sat_crossL.log 2>&1
python3 sat_crossL.py 4 -2 32 32 350 --ns 2,3 >> sat_crossL.log 2>&1
