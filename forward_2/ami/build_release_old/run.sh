#!/usr/bin/env bash
set -euo pipefail

DATETIME=$(date +%Y%m%d_%H%M%S)
OUTDIR="out/$DATETIME"
mkdir -p "$OUTDIR"

# start each program in background, redirect stdout+stderr to files, save pids
nohup ./muscle ../settings_muscle_left.py    > "$OUTDIR/muscle_left.txt"     2>&1 & echo $! > "$OUTDIR/muscle_left.pid"
nohup ./tendon ../settings_tendon.py         > "$OUTDIR/tendon.txt"          2>&1 & echo $! > "$OUTDIR/tendon.pid"
nohup ./only_mechanics_muscle ../settings_muscle_right.py > "$OUTDIR/muscle_right.txt" 2>&1 & echo $! > "$OUTDIR/muscle_right.pid"

echo "Logs and pids written to $OUTDIR"
