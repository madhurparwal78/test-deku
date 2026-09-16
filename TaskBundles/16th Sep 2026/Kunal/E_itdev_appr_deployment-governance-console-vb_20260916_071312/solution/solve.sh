#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The generation kit authors the brief, the checklist, the answer key and the graders." >&2
echo "It never builds the app. Build one downstream from solution/checklist.md, then replace" >&2
echo "this stub and run the handoff gates listed in _handoff/*.handoff.md." >&2
exit 3
