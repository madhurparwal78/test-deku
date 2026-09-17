#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'MSG'
solve.sh: NO-SOLUTION.

This bundle is MECHANICALLY-GREEN, NO-SOLUTION. The generation kit authors the
brief, the coverage target and the grading layer; it never authors the
application. There is no reference app inside this bundle to install, build or
serve, so there is nothing here that could bring the product up.

The bundle is not admissible until the application is generated from
solution/checklist.md and the oracle scores 1.0 twice.
MSG
exit 1
