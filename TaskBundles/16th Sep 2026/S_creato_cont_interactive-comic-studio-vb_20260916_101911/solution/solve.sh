#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The kit authors the brief, the checklist and the graders; it never builds the app." >&2
echo "Exit state is MECHANICALLY-GREEN, NO-SOLUTION. Generate the app downstream from" >&2
echo "solution/checklist.md, then run the oracle twice before treating this task as admissible." >&2
exit 1
