#!/usr/bin/env bash
set -u

echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors instruction.md, the graders and the answer key." >&2
echo "It never builds the app. Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
echo "Build the app downstream from solution/checklist.md, then run the oracle." >&2
exit 1
