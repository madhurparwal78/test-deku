#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'MESSAGE'
NO-SOLUTION.

This bundle ships a brief, a checklist, an answer key and a grading layer. It
does not ship the application. The kit authors the specification and the
graders; it never authors the app, so there is nothing here for an oracle run
to execute.

The bundle's honest exit state is MECHANICALLY-GREEN, NO-SOLUTION. It becomes
admissible only once the reference application is generated downstream from
solution/checklist.md and `harbor run -a oracle` returns 1.0 twice.
MESSAGE

exit 1
