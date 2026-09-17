#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors instruction.md, the checklist and the graders; it never builds the app." >&2
echo "Build the app from solution/checklist.md downstream, then re-run the oracle." >&2
exit 1
