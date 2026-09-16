#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the answer key and the graders; it never" >&2
echo "builds the app. Build one downstream from solution/checklist.md, then replace" >&2
echo "this stub and run the oracle." >&2
exit 1
