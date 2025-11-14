#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
INPUT_DIR="$SCRIPT_DIR/all_inputs/inputs"
MAX_JOBS=8   # <= IMPORTANT: reduce this number
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=10
export OMP_NUM_THREADS=10
job_count=0

for file in $INPUT_DIR/input_group*.txt; do
    echo "Running: $file"
    python3 "$SCRIPT_DIR/main.py" "$file" &

    ((job_count++))
    if (( job_count % MAX_JOBS == 0 )); then
        wait
    fi
done

wait
echo "All tasks complete."
