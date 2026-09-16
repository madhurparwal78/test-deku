#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors instruction.md, the answer key and the grading" >&2
echo "layer. It never builds the app. Generate the app downstream from" >&2
echo "solution/checklist.md, then run the oracle agent against it." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
