#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief and the graders, never the app." >&2
echo "Build the application downstream from solution/checklist.md, write the" >&2
echo "oracle steps into this file, then run the handoff gates." >&2
exit 1
