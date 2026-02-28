#!/bin/bash
# Standalone launcher — run with: bash launch_bs8.sh
# This script fully detaches from the calling terminal.
cd /home/user/claude-sandbox/explorations/qat-cpu

# Close inherited fds and redirect fresh
exec 0</dev/null
exec 1>converge_bs8.log
exec 2>&1

echo "Launched: $(date)"
echo "PID: $$"
echo $$ > converge_bs8.pid

exec ./train_qat_bs8_converge
