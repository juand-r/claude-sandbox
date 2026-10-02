#!/bin/bash
cd /home/user/claude-sandbox/explorations/rule110-lisp/noncts/round4/queue
export VMULT=2
for tape in NYYN NNYY; do
  for spec in "Ebar:0:-73;Ebar:14:-4" "Ebar@(0,0)+Ebar@(-1,39):19:-243" "Ebar:15:-36;E^3:3:-12"; do
    nice -n 10 python t_zfull.py $tape 8 "$spec" KF
  done
  nice -n 10 python t_zfull.py $tape 8 "Ebar:21:-50;Ebar:7:-11" KK
  nice -n 10 python t_zfull.py $tape 8 "Ebar_8_Ebar:5:-28" KK
done
echo done
