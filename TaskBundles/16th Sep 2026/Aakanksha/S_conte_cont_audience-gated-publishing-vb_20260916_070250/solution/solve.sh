#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships MECHANICALLY-GREEN with no application code." >&2
echo "The reference application is generated downstream from solution/checklist.md;" >&2
echo "the kit authors the brief and the graders only, never the app." >&2
exit 1
