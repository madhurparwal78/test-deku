#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle carries no reference application." >&2
echo "The generation kit authors the brief and the graders; it never authors the app." >&2
echo "Build one downstream from solution/checklist.md, replace this stub, then run" >&2
echo "the handoff gates listed in _handoff/*.handoff.md." >&2
exit 1
