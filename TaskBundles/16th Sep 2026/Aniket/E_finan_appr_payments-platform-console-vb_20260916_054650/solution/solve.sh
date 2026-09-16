#!/usr/bin/env bash
set -u
echo "NO-SOLUTION: this bundle ships no reference application." >&2
echo "The kit authors instruction.md, the checklist, the graders and the answer-key source." >&2
echo "The reference app is built downstream from solution/checklist.md, after which this" >&2
echo "stub is replaced by a real solve script." >&2
exit 1
