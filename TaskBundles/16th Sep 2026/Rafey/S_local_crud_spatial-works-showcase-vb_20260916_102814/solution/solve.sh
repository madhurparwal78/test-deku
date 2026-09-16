#!/usr/bin/env bash
set -euo pipefail

echo "FATAL: this bundle is MECHANICALLY-GREEN, NO-SOLUTION." >&2
echo "The kit authors the brief, the checklist and the graders; it never authors" >&2
echo "the application. The reference app for deku/spatial-works-showcase-vb is" >&2
echo "generated downstream from solution/checklist.md and has not landed yet, so" >&2
echo "there is nothing here to install, build or serve." >&2
echo >&2
echo "Until it lands, solve.sh reports failure rather than reporting a success it" >&2
echo "cannot deliver: an oracle run against this bundle must not return 1.0." >&2
exit 1
