# Handoff contract: voice-synthesis-workbench (variant b)

Exit stamp: **MECHANICALLY-GREEN, NO-SOLUTION**. This bundle is the spec and the test harness.
It is NOT admissible yet: `solution/` carries no application code, no image has been built, no
oracle has run. Admission requires generating the app from `solution/checklist.md` and
`harbor run -a oracle` returning `1.0` twice.

## The app-generation step (downstream)

Generate `solution/app/` from `instruction.md` + `solution/checklist.md`, build the environment
image, deploy it, then run the oracle. The kit never writes application code (plan D20).

## The seven gates the kit cannot run (handoff-owned)

Run each downstream against the built image and the generated app. Expected verdicts:

| Gate | What it proves | Command | Expected |
|---|---|---|---|
| G13 | environment + verifier images build | `docker buildx build environment/` and `tests/` | build succeeds on amd64 and arm64 |
| G15 | zero-credential boot | `docker compose up --wait` with only the bundle's own env | every sidecar healthy, app answers `GET /api/health` 200 |
| G18 | the app deploys and is reachable | deploy, then `curl $APP_PUBLIC_URL/api/health` | `200` after a cold start |
| G19 | the oracle solution scores 1.0 twice | `harbor run -a oracle` x2 | `1.0` both runs |
| G20 | a nop agent scores 0.0 | `harbor run -a nop` | `0.0` |
| G21 | a faked integration scores below 1.0 | `harbor run -a fake` | `< 1.0` |
| G25 | exploit sweep finds no reward-without-work path | `harbor run -a exploit-sweep` | no path scores reward |

G23 (implementation coupling) is a human prose review and does not scale to a tool.

## Notes for the downstream builder

- Backing services are postgres (`DATABASE_URL`/`DB_URL`) and minio
  (`STORAGE_ENDPOINT`/`STORAGE_BUCKET`/`STORAGE_ACCESS_KEY`/`STORAGE_SECRET_KEY`); both already run.
- The app binds `0.0.0.0`, serves a production build on container port 4173 behind `APP_PUBLIC_URL`,
  and must outlive the session (detached start).
- Seeded accounts all use the password `deku-demo-pw-2026`; write them into `/app/USER_README.md`.
- The hard parts the graders watch: exactly-one take under a duplicated idempotency key, a private
  take object refused to non-owners, credits never driven below zero, and cursor pagination.
