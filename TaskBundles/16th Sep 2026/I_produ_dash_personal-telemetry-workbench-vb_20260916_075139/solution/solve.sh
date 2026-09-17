#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The kit authors the brief, the answer key and the graders; the application is" >&2
echo "generated downstream from solution/checklist.md and is not part of the bundle." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
