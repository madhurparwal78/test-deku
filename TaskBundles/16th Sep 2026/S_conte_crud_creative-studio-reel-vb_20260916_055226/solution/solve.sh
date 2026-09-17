#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships MECHANICALLY-GREEN, NO-SOLUTION." >&2
echo "The generation kit authors the brief and the graders; it never authors the app." >&2
echo "Build the reference app downstream from solution/checklist.md, then run the" >&2
echo "oracle twice and promote the mint only when both runs return 1.0." >&2
exit 3
