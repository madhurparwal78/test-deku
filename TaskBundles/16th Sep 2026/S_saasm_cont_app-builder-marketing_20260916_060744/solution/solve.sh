#!/usr/bin/env bash
set -euo pipefail

echo "FAIL this bundle ships no reference application." >&2
echo "FAIL the kit authors the brief, the environment and the graders; it never" >&2
echo "FAIL writes the app. solution/app/ is retired and the reference build, if" >&2
echo "FAIL one is made, is generated downstream from solution/checklist.md and" >&2
echo "FAIL never ships inside the bundle." >&2
echo "FAIL exit state is MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 1
