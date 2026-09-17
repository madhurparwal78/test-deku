#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The kit authors the brief and the graders; the app is generated downstream" >&2
echo "from solution/checklist.md. Until it lands, an oracle run cannot pass." >&2
exit 1
