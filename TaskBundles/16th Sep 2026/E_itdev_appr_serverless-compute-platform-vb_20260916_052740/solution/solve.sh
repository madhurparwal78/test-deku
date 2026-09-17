#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'MESSAGE'
NO-SOLUTION: this bundle ships MECHANICALLY-GREEN, NO-SOLUTION.

The generation kit authors the brief, the coverage checklist, the answer key and
the grading layer. It never authors the application. There is no reference app
inside this bundle and there is no oracle trajectory to replay, so this script
exits non-zero rather than reporting a success it cannot produce.

To make this bundle admissible, generate the reference application downstream
from solution/checklist.md, then run the oracle twice and record the reward.
MESSAGE

exit 70
