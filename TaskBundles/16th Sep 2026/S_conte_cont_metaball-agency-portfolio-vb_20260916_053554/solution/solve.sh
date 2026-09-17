#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the environment and the graders; it never authors the app." >&2
echo "Build the app downstream from solution/checklist.md, then run the oracle." >&2
exit 1
