#!/bin/bash
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
export VMULT=2 ZLO=-104 ZHI=-2
for spec in "Ebar:14:-74;E^3:12:-52" "E^3:5:-87;Ebar:21:-50" "Ebar:21:-71;E^3:12:-52" "Ebar:26:-78;E^3:9:-64"; do
  for tape in YYNN YNYN; do
    nice -n 10 python t_zfull.py $tape 8 "$spec" KF
  done
done
echo done
