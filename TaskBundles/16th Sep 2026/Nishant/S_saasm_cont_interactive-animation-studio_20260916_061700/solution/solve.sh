#!/usr/bin/env bash
set -euo pipefail

echo "solve.sh: no reference application is present in this bundle" >&2
echo "solve.sh: solution/ carries the checklist, the answer key and this stub only" >&2
echo "solve.sh: the reference application is generated downstream from solution/checklist.md" >&2
echo "solve.sh: this bundle is MECHANICALLY-GREEN, NO-SOLUTION and is not admissible" >&2
exit 1
