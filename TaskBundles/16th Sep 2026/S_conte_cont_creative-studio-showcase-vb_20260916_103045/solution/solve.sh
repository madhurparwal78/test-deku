#!/usr/bin/env bash
set -u

cat >&2 <<'MSG'
NO-SOLUTION.

This bundle carries the brief, the graders and the answer key. It carries no
reference application: the generation kit authors the specification and the
grading surface, never the app under test.

Build the application downstream from solution/checklist.md, then replace this
stub with the oracle that starts it, and run the harness twice.
MSG
exit 1
