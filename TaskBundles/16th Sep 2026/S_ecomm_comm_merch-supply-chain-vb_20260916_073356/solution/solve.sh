#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief and the graders; the app is built" >&2
echo "downstream from solution/checklist.md before any oracle run." >&2
exit 1
