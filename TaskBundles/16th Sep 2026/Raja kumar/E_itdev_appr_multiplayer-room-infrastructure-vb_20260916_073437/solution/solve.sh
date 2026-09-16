#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-/app}"
MANIFEST="$APP_DIR/run.json"

if [ ! -f "$MANIFEST" ]; then
  echo "solve.sh: $MANIFEST is absent" >&2
  exit 1
fi

if [ -z "$(find "$APP_DIR" -type f -name 'run.json' -print -quit)" ]; then
  echo "solve.sh: no run manifest at $APP_DIR/run.json." >&2
  echo "solve.sh: this bundle is MECHANICALLY-GREEN, NO-SOLUTION." >&2
  exit 1
fi

INSTALL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["install"])' "$MANIFEST")"
BUILD="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["build"])' "$MANIFEST")"
SERVE="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["serve"])' "$MANIFEST")"

cd "$APP_DIR"
[ -n "$INSTALL" ] && eval "$INSTALL"
[ -n "$BUILD" ] && eval "$BUILD"

mkdir -p "$APP_DIR/.browser_screenshots" "$APP_DIR/.downloads"

setsid nohup bash -c "$SERVE" >> /tmp/app.log 2>&1 < /dev/null &
disown || true

for _ in $(seq 1 120); do
  if curl -fsS "http://127.0.0.1:4173/api/health" > /dev/null 2>&1; then
    echo "solve.sh: app is ready"
    exit 0
  fi
  sleep 2
done

echo "solve.sh: app did not become ready" >&2
exit 1
