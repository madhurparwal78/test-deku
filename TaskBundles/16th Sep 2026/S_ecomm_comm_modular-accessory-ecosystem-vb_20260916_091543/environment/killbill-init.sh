set -eu
BASE="${PAYMENTS_API_URL:-http://killbill:8080}"
USER="${PAYMENTS_ADMIN_USER:-admin}"
PASS="${PAYMENTS_ADMIN_PASSWORD:-password}"
KEY="${PAYMENTS_API_KEY:-orbit-labs}"
SECRET="${PAYMENTS_API_SECRET:-orbit-labs-secret-9f14c73e}"
APP_USER="${PAYMENTS_API_USER:-lattice-app}"
APP_PASS="${PAYMENTS_API_PASSWORD:-kb-app-5d2e91}"
i=0
while [ "$i" -lt 180 ]; do
    code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 \
           "$BASE/1.0/healthcheck" 2>/dev/null || echo 000)
    [ "$code" = "200" ] && break
    i=$((i + 1))
    sleep 2
done
[ "$i" -lt 180 ] || { echo "killbill-init: never became healthy" >&2; exit 1; }
curl -s -o /dev/null -X POST -u "$USER:$PASS" \
     -H 'Content-Type: application/json' -H 'X-Killbill-CreatedBy: init' \
     -d "{\"apiKey\":\"$KEY\",\"apiSecret\":\"$SECRET\"}" \
     "$BASE/1.0/kb/tenants" || true
curl -s -o /dev/null -X POST -u "$USER:$PASS" \
     -H "X-Killbill-ApiKey: $KEY" -H "X-Killbill-ApiSecret: $SECRET" \
     -H 'Content-Type: application/json' -H 'X-Killbill-CreatedBy: init' \
     -d '{"role":"storefront","permissions":["account:*","invoice:*"]}' \
     "$BASE/1.0/kb/security/roles" || true
curl -s -o /dev/null -X POST -u "$USER:$PASS" \
     -H "X-Killbill-ApiKey: $KEY" -H "X-Killbill-ApiSecret: $SECRET" \
     -H 'Content-Type: application/json' -H 'X-Killbill-CreatedBy: init' \
     -d "{\"username\":\"$APP_USER\",\"password\":\"$APP_PASS\",\"roles\":[\"storefront\"]}" \
     "$BASE/1.0/kb/security/users" || true
echo "killbill-init: tenant and storefront user ready"
