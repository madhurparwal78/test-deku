#!/usr/bin/env bash
set -euo pipefail

cat >&2 <<'MSG'
NO SOLUTION SHIPS WITH THIS BUNDLE.

This bundle is MECHANICALLY-GREEN, NO-SOLUTION. The kit authors the brief, the
checklist, the environment and the grading layer; it never authors the
application. The reference application is built downstream from
solution/checklist.md and instruction.md, and only then does this task become
admissible.

Build the app from instruction.md, then run the oracle agent against it. This
stub exits non-zero so that nothing mistakes an absent solution for a passing
one.
MSG

exit 1
