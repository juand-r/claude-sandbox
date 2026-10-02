#!/bin/bash
D=/home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/objects
cd $D
nice -n 10 python3 wallsat.py 000000111 28 30 $D/walls_p9.jsonl > $D/walls_p9.log 2>&1
nice -n 10 python3 wallsat.py 00000010011 28 30 $D/walls_p11.jsonl > $D/walls_p11.log 2>&1
