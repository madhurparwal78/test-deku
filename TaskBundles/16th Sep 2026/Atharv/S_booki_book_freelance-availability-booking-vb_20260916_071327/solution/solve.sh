#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors instruction.md, solution/checklist.md and the" >&2
echo "grading layer. It never builds the app. The reference application is built" >&2
echo "downstream from solution/checklist.md and does not ship inside the bundle." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
