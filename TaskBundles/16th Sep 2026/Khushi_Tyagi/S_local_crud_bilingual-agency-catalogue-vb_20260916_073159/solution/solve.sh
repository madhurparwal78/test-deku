#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The brief and the graders are authored; the application is generated downstream from solution/checklist.md." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION. Not admissible until an oracle run returns 1.0 twice." >&2
exit 3
