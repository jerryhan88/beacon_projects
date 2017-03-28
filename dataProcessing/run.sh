#!/usr/bin/env bash
#for i in {0..5}; do
#    python -c "from a2_Uzk import run; run($i)" &
#done

for i in {0..5}; do
    python -c "from a3_Zf import run; run($i)" &
done
