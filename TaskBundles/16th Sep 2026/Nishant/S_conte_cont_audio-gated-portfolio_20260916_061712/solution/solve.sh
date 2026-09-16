#!/usr/bin/env bash
set -euo pipefail

echo "FAIL: this bundle is MECHANICALLY-GREEN, NO-SOLUTION." >&2
echo "The kit authors instruction.md, the environment and the graders. It never authors the app." >&2
echo "Build the reference application downstream from solution/checklist.md, then deploy it and" >&2
echo "run the handoff gates listed in _handoff/*.handoff.md." >&2
exit 1
