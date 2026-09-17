#!/usr/bin/env bash
set -u

cat >&2 <<'MSG'
NO-SOLUTION.

This bundle is MECHANICALLY-GREEN, NO-SOLUTION. The generation kit authors the
brief, the environment and the grading layer. It never authors the application,
so there is no reference implementation here to run.

The reference app is generated downstream from solution/checklist.md. Until that
app lands and an oracle run returns 1.0 twice, this task is not admissible and
nothing about it counts toward a corpus target.

Exiting non-zero on purpose: a stub that exited 0 would read as a passing oracle.
MSG

exit 1
