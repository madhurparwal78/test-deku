#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the graders and the answer key; it never builds the app." >&2
echo "The reference app is generated downstream from solution/checklist.md, after which" >&2
echo "'harbor run -a oracle' must return 1.0 twice before this task is admissible." >&2
exit 1
