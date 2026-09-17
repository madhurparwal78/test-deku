#!/usr/bin/env bash
set -euo pipefail

echo "NO-SOLUTION: this bundle ships no reference implementation." >&2
echo "solution/ holds the coverage target (checklist.md), the answer-key source" >&2
echo "(trinity/grounding.yaml) and the artifacts recompute.py derives from it." >&2
echo "The application is built by the agent under test from instruction.md alone." >&2
exit 1
