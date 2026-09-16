#!/usr/bin/env sh
set -eu

BASE="${PAYMENTS_API_URL:-http://killbill:8080}"
USER="${PAYMENTS_ADMIN_USER:-admin}"
PASS="${PAYMENTS_ADMIN_PASSWORD:-password}"
KEY="${PAYMENTS_API_KEY:-orbit-labs}"
SECRET="${PAYMENTS_API_SECRET:-orbit-labs-secret-9f14c73e}"

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

seed_account() {
    name="$1"; key="$2"; email="$3"; currency="$4"; country="$5"
    found=$(curl -s -o /dev/null -w "%{http_code}" -u "$USER:$PASS" \
            -H "X-Killbill-ApiKey: $KEY" -H "X-Killbill-ApiSecret: $SECRET" \
            "$BASE/1.0/kb/accounts?externalKey=$key")
    [ "$found" = "200" ] && return 0
    curl -s -o /dev/null -X POST -u "$USER:$PASS" \
         -H "X-Killbill-ApiKey: $KEY" -H "X-Killbill-ApiSecret: $SECRET" \
         -H 'X-Killbill-CreatedBy: init' -H 'Content-Type: application/json' \
         -d "{\"name\":\"$name\",\"externalKey\":\"$key\",\"email\":\"$email\",\"currency\":\"$currency\",\"country\":\"$country\"}" \
         "$BASE/1.0/kb/accounts" || true
}

seed_account "Amelia Ortega"    "orbit-amelia"    "amelia.ortega@orbit-labs.com"  "EUR" "ES"
seed_account "Acme Partner Ltd" "orbit-acme"      "accounts@acme-partner.example.com" "EUR" "IE"
seed_account "Northwind Trading" "orbit-northwind" "billing@northwind.example.com"    "USD" "US"

echo "killbill-init: tenant and accounts ready"
