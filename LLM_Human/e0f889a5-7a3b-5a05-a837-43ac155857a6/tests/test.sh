#!/bin/bash
# Verifier entrypoint, HUMAN-EVAL BUILD. pytest is the only automated grader and
# it alone sets the reward; workflow and rubric are graded by hand against
# tests/workflows.yaml and tests/rubric.json, so run_workflows.py, run_rubric.py
# and score.py are deliberately not called.
#
# NO `set -e`. A failing pytest is a SCORE, not a harness error. A verifier that
# exits without a reward file raises RewardFileNotFoundError and the trial is
# LOST, not scored zero.

mkdir -p /logs/verifier

# 1. Zero reward FIRST, so every later exit path already has a reward file.
#    Single key only: Harbor registers every top-level key here as its own
#    reward stream, so diagnostics belong in workflows.json.
cat > /logs/verifier/reward.json <<'EOF'
{"reward": 0.0}
EOF

: "${APP_PUBLIC_URL:?APP_PUBLIC_URL is not set}"
APP_PUBLIC_URL="${APP_PUBLIC_URL%/}"
export APP_PUBLIC_URL

# 2. Deploy gate. Hard zero, no partial credit. Gate on /api/health rather than
#    `/`: an app can serve a static frontend while its health endpoint reports
#    503, and that is not deployed.
DEPLOYED=0.0
HEALTH_CODE=""
for _ in $(seq 1 30); do
  HEALTH_CODE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 \
                "${APP_PUBLIC_URL}/api/health" 2>/dev/null)
  if [ "$HEALTH_CODE" = "200" ]; then
    DEPLOYED=1.0
    break
  fi
  sleep 5
done

# 404 means the spec exposes no health endpoint; any other code is the app
# reporting its own failure, so only 404 may fall back to `/`.
if [ "$DEPLOYED" != "1.0" ] && [ "$HEALTH_CODE" = "404" ]; then
  echo "no /api/health endpoint (404); falling back to GET / for the deploy gate" >&2
  if curl -fsS --max-time 10 "${APP_PUBLIC_URL}/" > /dev/null 2>&1; then
    DEPLOYED=1.0
  fi
elif [ "$DEPLOYED" != "1.0" ]; then
  echo "deploy gate: /api/health last returned '${HEALTH_CODE:-no response}' - the app" >&2
  echo "is reporting itself NOT ready, so this is a deploy failure even if / serves." >&2
fi

if [ "$DEPLOYED" != "1.0" ]; then
  echo "app never became reachable at ${APP_PUBLIC_URL} - scoring 0" >&2
  # The marker goes in workflows.json: a bare {"reward": 0.0} is
  # indistinguishable from a legitimate agent 0.
  echo '{"reward": 0.0}' > /logs/verifier/reward.json
  printf '{"summary": {"reward": 0.0, "invalid": ["deploy_failed"]}}\n' \
    > /logs/verifier/workflows.json
  exit 0
fi

# 3. Baseline row counts. Kept although the browser pass is gone: the
#    `pre_browser` fixture is unconditional, and without this file every
#    seed-count assertion SKIPs instead of running. The counts cannot be
#    hardcoded -- they vary per seed, and a stale number fails a working app.
python3 - >/logs/verifier/pre_browser_counts.json 2>>/logs/verifier/pre_browser_snapshot.err <<'SNAPSHOT' || true
import json, os, sys
sys.path.insert(0, "/tests")
try:
    from capabilities import make_backend
    b = make_backend()
    # query() is PostgresBackend-only; PocketBaseBackend has just count/rows.
    # Fall back to DEKU_SNAPSHOT_TABLES so a non-SQL slot degrades to a smaller
    # snapshot rather than an empty one.
    counts = {}
    names = []
    if hasattr(b, "query"):
        try:
            names = [
                r.get("table_name") if isinstance(r, dict) else r[0]
                for r in b.query(
                    "SELECT table_name FROM information_schema.tables "
                    "WHERE table_schema='public' AND table_type='BASE TABLE'")
            ]
        except Exception:
            names = []
    if not names:
        names = [t for t in os.environ.get("DEKU_SNAPSHOT_TABLES", "").split(",") if t.strip()]
    for t in names:
        try:
            counts[t.strip()] = b.count(t.strip())
        except Exception:
            pass
    # Without _snapshot_ok, {} means both "no tables" and "this blew up", and
    # the consumer has to guess.
    counts["_snapshot_ok"] = True
    json.dump(counts, sys.stdout)
except Exception as exc:
    json.dump({"_snapshot_ok": False,
               "_snapshot_error": f"{exc.__class__.__name__}: {exc}"[:300]},
              sys.stdout)
SNAPSHOT
if [ -s /logs/verifier/pre_browser_snapshot.err ]; then
  echo "  [snapshot] stderr while taking the pre-browser baseline:" >&2
  sed 's/^/    /' /logs/verifier/pre_browser_snapshot.err >&2
fi
if ! grep -q '"_snapshot_ok": *true' /logs/verifier/pre_browser_counts.json 2>/dev/null; then
  echo "  [snapshot] NO pre-browser baseline; seed-count assertions will SKIP" >&2
  echo "             rather than compare against a number nobody measured." >&2
fi

# 4. pytest pass -- the only automated grader in this build.
pytest /tests -rA --ctrf /logs/verifier/ctrf.json || true

# A collection-time error writes no report, which stage 5 would otherwise score
# as an honest 0.
if [ ! -s /logs/verifier/ctrf.json ]; then
  echo "PYTEST WROTE NO CTRF REPORT - collection failed before running any test." >&2
  echo "The reward below is a harness fault, not an agent score." >&2
  printf '{"error": "ctrf_missing"}\n' > /logs/verifier/ctrf-error.json
fi

# 5. Score. Three channels fold into one number:
#       combined = workflow**0.50 * pytest**0.25 * (rubric * coverage)**0.25
#
#    pytest is graded here. The workflow and rubric channels are graded by a
#    person, who writes marks into browser_results.json and judge.json. Until
#    both arrive score.py reports combined_score: null rather than the pytest
#    term alone, so an unfinished review never reads as a finished low score.
#
#    Run `score.py --template DIR` to emit blank mark sheets for the reviewer.
INVALID=""
if [ ! -s /logs/verifier/ctrf.json ]; then
  INVALID="ctrf_missing"
else
  # pytest-json-ctrf writes a well-formed report with tests:0 when collection
  # fails, so checking only that the file is readable lets a broken conftest
  # score as an honest agent 0.
  grep -q '"tests"[[:space:]]*:[[:space:]]*0[^0-9]' /logs/verifier/ctrf.json \
    && INVALID="no_tests_collected"
fi

python3 /tests/score.py \
  --pytest    /logs/verifier/ctrf.json \
  --browser   /logs/verifier/browser_results.json \
  --judge     /logs/verifier/judge.json \
  --rubric    /tests/rubric.json \
  --workflows /tests/workflows.yaml \
  --out       /logs/verifier/final_score.json \
  --reward-out /logs/verifier/reward.json \
  --invalid   "$INVALID"

if [ -n "$INVALID" ]; then
  echo "VERIFIER FAULT: $INVALID - this run is not an agent score" >&2
fi

echo "score: $(cat /logs/verifier/reward.json)" >&2

exit 0
