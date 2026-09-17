#!/usr/bin/env bash
set -uo pipefail

echo "FATAL: this bundle carries no reference application." >&2
echo "STATE: MECHANICALLY-GREEN, NO-SOLUTION" >&2
echo "The app is generated downstream from solution/checklist.md and never ships inside the bundle." >&2
exit 1
