#!/bin/bash
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
while kill -0 28703 2>/dev/null; do sleep 10; done
export VMULT=2
for tape in YYNN YNYN; do nice -n 10 python t_plainctl.py $tape 8; done
echo done
