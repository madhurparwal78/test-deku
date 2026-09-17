#!/bin/bash
set -euo pipefail

: "${APP_PUBLIC_PORT:=4173}"
: "${DATABASE_URL:?DATABASE_URL is not set}"
: "${STORAGE_ENDPOINT:?STORAGE_ENDPOINT is not set}"
: "${STORAGE_BUCKET:?STORAGE_BUCKET is not set}"

REFERENCE_APP="${DEKU_REFERENCE_APP:-}"

if [ -z "${REFERENCE_APP}" ] || [ ! -d "${REFERENCE_APP}" ]; then
  echo "No reference application is available at DEKU_REFERENCE_APP." >&2
  echo "The oracle gate cannot pass until one is built and pointed at by that variable." >&2
  exit 1
fi

cp -a "${REFERENCE_APP}/." /app/
cd /app
mkdir -p .browser_screenshots .downloads

npm ci --omit=dev
node ./server/scripts/migrate.js
node ./server/scripts/seed.js
setsid nohup node ./server/index.js > /tmp/server.log 2>&1 &

for _ in $(seq 1 90); do
  if curl -fsS "http://localhost:${APP_PUBLIC_PORT}/api/health" > /dev/null 2>&1; then
    echo "reference app up on ${APP_PUBLIC_PORT}"
    exit 0
  fi
  sleep 2
done

echo "reference app did not come up within 180s" >&2
tail -50 /tmp/server.log >&2 || true
exit 1
