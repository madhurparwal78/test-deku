#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the environment and the graders." >&2
echo "It never authors the app. Build one downstream from solution/checklist.md," >&2
echo "then replace this stub and run the oracle." >&2
exit 3
