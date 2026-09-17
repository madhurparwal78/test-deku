#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'MSG'
NO-SOLUTION.

This bundle ships no reference application. The generation kit authors the brief,
the checklist, the answer key and the graders; it never builds the app. The honest
exit state of this bundle is MECHANICALLY-GREEN, NO-SOLUTION, and it is not
admissible until an application is built downstream from solution/checklist.md and
`harbor run -a oracle` returns 1.0 twice.

Running this script as an oracle would report a success that never happened, so it
exits non-zero instead.
MSG

exit 1
