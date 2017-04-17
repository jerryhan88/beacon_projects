#!/usr/bin/env bash

#for i in {2..3}; do
#    python -c "from a0a_trajectory import run; run($i)" &
#done

#for i in {0..4}; do
#    python -c "from a2_Uzk import run; run($i)" &
#done

for i in {0..3}; do
    python -c "from a3_Zf import run; run($i)" &
done
