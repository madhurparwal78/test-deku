# Handoff contract: S_commu_crud_crowdsourced-cartography-platform-vb_20260916_062745

exit state: MECHANICALLY-GREEN, NO-SOLUTION
NOT ADMISSIBLE. Nothing counts toward corpus targets until the app lands and
`harbor run -a oracle` returns 1.0 twice.

## What the kit did not and could not run

The kit has no Docker and no harness access, so the seven gates below are
declared here with their commands and expected verdicts, never proven above.

| Gate | What it proves | Command | Expected |
|---|---|---|---|
| G13 | the environment image builds | `docker build environment/` | exit 0 |
| G15 | the environment boots with no external account or API key | `docker compose -f environment/docker-compose.yaml up --wait` | every service healthy |
| G18 | `/app/USER_README.md` carries the seeded logins, and the reserved directories exist at the app root | inspect the running container | the three mapper addresses, the corpus password, and empty `.browser_screenshots/` and `.downloads/` |
| G19 | the app answers its health route | `curl -fsS "$APP_PUBLIC_URL/api/health"` | HTTP 200 |
| G20 | `solution/solve.sh` fails loudly rather than pretending | `bash solution/solve.sh` | non-zero exit, NO-SOLUTION on stderr |
| G21 | the server outlives the session | end the session, then re-request the root | the app still answers |
| G25 | the oracle scores the task | `harbor run -a oracle` | reward 1.0, twice |

## The app-generation step

The bundle ships no reference app by design. The app is generated downstream from
`solution/checklist.md`, which is the coverage target every channel is joined
against. Build it, then run G13 through G25 in order.

## What is held out from the agent

The agent sees `instruction.md` and nothing else. `tests/`, `solution/` and all of
`_handoff/` are held out for the whole agent phase. `_handoff/` is on that list
for the same reason `solution/` is: the literals ledger enumerates every value a
grader may assert, and the report names every gate and its verdict.

## Before publishing

The gate log is SELF-ATTESTED on the seven certification prompts: one agent both
authored the bundle and reviewed it, which the kit records as a verdict rather
than an independent one. An independent reviewer re-running
`prompts/QC_instruction.md`, `prompts/qc_toml.md`, `prompts/qc_docker.md` and
`prompts/qc_rubric.md` against this bundle is what turns those four into real
verdicts.

## Verifier mode

`[verifier].environment_mode = "separate"`: the grader ships its own image, built
from `tests/Dockerfile` on `deku-verifier-base`, and reaches the app through the
`4173:4173` publish on `main` rather than over the compose network. Nothing in
`tests/` reads the agent's filesystem, because under this mode it cannot.

## Reproducing the sweep

The companion document is recorded in `<project>.sources.json`, so the sweep can
be re-run without remembering what the Task Order carried. The G51 waivers are
recorded in this bundle's receipts and in the companion carry table in
`Output/_spec/<project>/00-decisions.md`.
