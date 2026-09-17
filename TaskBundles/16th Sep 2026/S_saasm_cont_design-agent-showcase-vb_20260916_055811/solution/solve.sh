#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors instruction.md, the environment and the graders." >&2
echo "The application is generated downstream from solution/checklist.md." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
