#!/bin/bash

mkdir -p /logs/verifier

cat > /logs/verifier/reward.json <<'EOF'
{"reward": 0.0}
EOF

: "${APP_PUBLIC_URL:?APP_PUBLIC_URL is not set}"
APP_PUBLIC_URL="${APP_PUBLIC_URL%/}"
export APP_PUBLIC_URL

DEPLOYED=0.0
for _ in $(seq 1 30); do
  if curl -fsS --max-time 10 "${APP_PUBLIC_URL}/api/health" > /dev/null 2>&1 \
     || curl -fsS --max-time 10 "${APP_PUBLIC_URL}/" > /dev/null 2>&1; then
    DEPLOYED=1.0
    break
  fi
  sleep 5
done

if [ "$DEPLOYED" != "1.0" ]; then
  echo "app never became reachable at ${APP_PUBLIC_URL} - scoring 0" >&2
  /tests/score.py \
    --workflows /tests/workflows.yaml \
    --pytest /nonexistent-ctrf.json \
    --browser /nonexistent-browser.json \
    --deployed 0.0 \
    --out /logs/verifier/reward.json || {
      echo '{"reward": 0.0}' > /logs/verifier/reward.json
      printf '{"summary": {"reward": 0.0, "invalid": ["deploy_failed", "scorer_crashed"]}}\n' \
        > /logs/verifier/workflows.json
    }
  exit 0
fi

BROWSER_RESULTS=/tmp/browser_results.json
if [ -x /tests/run_workflows.py ]; then
  /tests/run_workflows.py \
    --workflows /tests/workflows.yaml \
    --url "$APP_PUBLIC_URL" \
    --out "$BROWSER_RESULTS"
else
  echo "no browser executor in this image - pytest substeps only" >&2
fi

pytest /tests -rA --ctrf /logs/verifier/ctrf.json || true

if [ ! -s /logs/verifier/ctrf.json ]; then
  echo "PYTEST WROTE NO CTRF REPORT - collection failed before running any test." >&2
  echo "The reward below is a harness fault, not an agent score." >&2
  printf '{"error": "ctrf_missing"}\n' > /logs/verifier/ctrf-error.json
fi

JUDGE_RESULTS=/logs/verifier/judge.json
if [ "${DEKU_SKIP_RUBRIC:-0}" = "1" ]; then
  echo "DEKU_SKIP_RUBRIC=1 - skipping the advisory rubric judge" >&2
  printf '{"judge_score": null, "dimensions": {}, "meta": {"skipped": "DEKU_SKIP_RUBRIC"}}\n' > "$JUDGE_RESULTS"
elif [ -x /tests/run_rubric.py ] && [ -f /tests/instruction.md ]; then
  RUBRIC_ARG=""
  if [ -f /tests/rubric.json ]; then
    RUBRIC_ARG="--rubric /tests/rubric.json"
  else
    echo "no /tests/rubric.json - judging against the built-in dimension prose" >&2
  fi
  /tests/run_rubric.py \
    --instruction /tests/instruction.md \
    --url "$APP_PUBLIC_URL" \
    --screenshot-dir /logs/verifier/shots \
    $RUBRIC_ARG \
    --out "$JUDGE_RESULTS" || true
else
  echo "no rubric judge in this image (or no instruction.md) - skipping" >&2
fi

if ! /tests/score.py \
    --workflows /tests/workflows.yaml \
    --pytest /logs/verifier/ctrf.json \
    --browser "$BROWSER_RESULTS" \
    --judge "$JUDGE_RESULTS" \
    --deployed "$DEPLOYED" \
    --out /logs/verifier/reward.json; then
  echo "score.py crashed - emitting invalid marker so this run is not read as an agent score" >&2
  echo '{"reward": 0.0}' > /logs/verifier/reward.json
  printf '{"summary": {"reward": 0.0, "invalid": ["scorer_crashed"]}}\n' \
    > /logs/verifier/workflows.json
fi

exit 0
