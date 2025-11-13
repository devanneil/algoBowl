#!/bin/bash

SCRIPT_DIR="$(dirname "$0")"
INPUT_DIR="$SCRIPT_DIR/all_inputs/inputs"

for file in $INPUT_DIR/input_group*.txt; do
    echo "Running: $file"
    python3 "$SCRIPT_DIR/main.py" "$file" &
done

wait
echo "All tasks complete."
