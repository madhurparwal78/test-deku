#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the graders and the answer key; it never builds the app." >&2
echo "The app is generated downstream from solution/checklist.md, then harbor run -a oracle must return 1.0 twice." >&2
exit 1
