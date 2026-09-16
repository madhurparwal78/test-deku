#!/usr/bin/env bash
set -u

cat >&2 <<'MSG'
NO-SOLUTION.

This bundle is MECHANICALLY-GREEN, NO-SOLUTION. deku-green-field authors the
brief, the answer key and the graders; it never authors the application. There
is no reference app inside this bundle and therefore nothing for an oracle run
to execute.

Build the reference application downstream from solution/checklist.md, replace
this stub with a script that deploys it, and only then run:

    harbor run -p <task> -a oracle

The bundle becomes admissible when that returns 1.0 twice.
MSG

exit 1
