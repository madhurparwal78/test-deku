#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The kit authors instruction.md, solution/checklist.md and the grading layer;" >&2
echo "it never builds the app. Build the reference app downstream from" >&2
echo "solution/checklist.md, then run the oracle agent against it." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
