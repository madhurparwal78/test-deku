# Ravel — access

There is no signup and no self-service account creation. Seven seeded accounts exist and every
one authenticates at the identity provider. All of them use the same password:

    deku-demo-pw-2026

| Email | Role | Sites |
|---|---|---|
| `plant@example.com` | Plant operator | `SITE-DEMO`, `SITE-PILOT` |
| `analyst@example.com` | Laboratory analyst | `SITE-DEMO`, `SITE-PILOT` |
| `quality@example.com` | Quality manager | `SITE-DEMO`, `SITE-PILOT` |
| `claims@example.com` | Claims manager | `SITE-DEMO`, `SITE-PILOT` |
| `signer@example.com` | Certificate signer | `SITE-DEMO`, `SITE-PILOT` |
| `signer2@example.com` | Certificate signer (narrower scope) | `SITE-PILOT` |
| `auditor@example.com` | Auditor (reads and exports only) | `SITE-DEMO`, `SITE-PILOT` |

Sign in at `/login`; the console is at `/console`. The public site needs no account, and
`/verify/{number}` is public and unauthenticated.

Every write the product accepts requires an `Idempotency-Key` header. Signing a certificate
re-authenticates: the signing request carries the account password again, and a session alone is
not a signing credential.
