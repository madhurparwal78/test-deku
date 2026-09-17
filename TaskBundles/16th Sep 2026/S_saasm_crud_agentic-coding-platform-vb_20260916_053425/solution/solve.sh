#!/usr/bin/env bash
set -euo pipefail
echo "NO-SOLUTION: this bundle ships a brief and a grading layer, never an application." >&2
echo "The reference app is generated downstream from solution/checklist.md." >&2
exit 1
