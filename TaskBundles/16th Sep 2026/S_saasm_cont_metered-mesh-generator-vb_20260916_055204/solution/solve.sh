#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the environment and the graders." >&2
echo "The application is built downstream from solution/checklist.md." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
