#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The kit authors instruction.md, the checklist and the graders; it never builds the app." >&2
echo "Exit state: MECHANICALLY-GREEN, NO-SOLUTION." >&2
exit 3
