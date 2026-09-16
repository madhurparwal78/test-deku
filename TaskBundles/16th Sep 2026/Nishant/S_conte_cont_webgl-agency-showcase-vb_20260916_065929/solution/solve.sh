#!/usr/bin/env bash
set -euo pipefail

echo "solve.sh: this bundle ships MECHANICALLY-GREEN, NO-SOLUTION." >&2
echo "solve.sh: solution/ carries no reference application. The app is generated downstream from solution/checklist.md, and solution/app/ is retired from the bundle layout (CON-2)." >&2
echo "solve.sh: refusing to report success on a task with no solution." >&2
echo "VERDICT FAIL app-deferred: no reference application present" >&2
exit 1
