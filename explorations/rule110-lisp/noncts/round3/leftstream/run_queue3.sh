#!/bin/bash
# After queue 2 (Bbar crossing) ends: converter brute-force scan.
cd "$(dirname "$0")"
while ps -p 19733 > /dev/null; do sleep 10; done
python3 conv_scan.py >> conv_scan.log 2>&1
