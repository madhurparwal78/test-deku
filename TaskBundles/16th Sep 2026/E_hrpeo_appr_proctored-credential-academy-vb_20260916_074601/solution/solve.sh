#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "deku-green-field authors the brief, the answer key and the graders; the app is" >&2
echo "built downstream from solution/checklist.md. Until that lands, an oracle run" >&2
echo "cannot succeed and this script must not pretend otherwise." >&2
exit 1
