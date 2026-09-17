# Handoff contract - S_commu_feed_realtime-drawing-party-vb_20260916_074441

What the kit could not run, and what an operator with Docker and the harness must run before this
bundle counts as anything.

| | |
|---|---|
| Task code | `S_commu_feed_realtime-drawing-party-vb_20260916_074441` |
| Task id | `deku/realtime-drawing-party-vb` |
| Bundle | `output_16sep/S_commu_feed_realtime-drawing-party-vb_20260916_074441/` |
| Exit state | NOT ADMISSIBLE, NO-SOLUTION, 1 red gate |

## Before anything: close the one red gate

Read `_handoff/S_commu_feed_realtime-drawing-party-vb_20260916_074441.report.md` for the full gate
log. Twenty-eight gates are green, one is a WARN and one is NOT-APPLICABLE. One is red, and it is
not a defect in the task's content.

1. **G46, placement.** The bundle sits inside the generation kit rather than beside it. Move the
   bundle root one directory up, out of `GreenField-GenKit2/`, and re-run the sweep. Nothing
   inside the bundle changes.
2. **G47** clears on its own once G46 is green.

The seven certification prompts have been run and their scorecards are recorded in
`_handoff/S_commu_feed_realtime-drawing-party-vb_20260916_074441.receipts.json`, answering all 292
checks their registries declare. Owner and verifier were the same agent, so each reports as
SELF-ATTESTED: a recorded verdict, never an independent one. **Running them again under a second
identity is the single highest-value thing a reviewer can do with this bundle**, because owner is
not verifier is the kit's own rule and this run could not satisfy it.

## Re-running G51, which needs its waiver list

`revalidate.py` takes `--waive` but records no waiver list of its own, so the gate is only
reproducible with the file beside the spec folder:

```
python3 "$OUT/_spec/run-g51.py" "$OUT/S_commu_feed_realtime-drawing-party-vb_20260916_074441"
```

or pass `--waive <value>` to `revalidate.py` once per line of
`_spec/S_commu_feed_realtime-drawing-party-vb_20260916_074441-g51-waivers.txt`. Without them the
gate reports thirty-two findings, every one of them a deliberate drop recorded in
`_spec/<code>/00-decisions.md`.

## Then fill the two operator-owned values

- `[delivery.images]` is absent from `task.toml`. The block is optional and the bundle validates
  without it, but a delivery package wants it. Pull the digests once the images are built: `main`
  from the `FROM` line of `environment/Dockerfile`, and one entry per sidecar image in
  `environment/docker-compose.yaml`.
- `[metadata]` calibration fields (`difficulty`, `pass_rate`, `pass_rate_ci`,
  `calibration_trials`, `reference_model_used`) are present and deliberately empty. The kit never
  writes them.

## The seven gates the kit cannot run

Each needs Docker, the harness, or both. Run them in this order; a failure routes back to the
stage named in the last column.

| Gate | What it proves | Command | Expected | Routes back to |
|---|---|---|---|---|
| **G13** | the environment image builds and every sidecar reaches healthy | `docker compose -f environment/docker-compose.yaml up --wait` | every service healthy, no service stranding the wait | S5 |
| **G15** | the verifier image builds on the pinned base and carries the five task files | `docker build -t deku-verifier-task -f tests/Dockerfile tests/` | build succeeds, `/tests` carries `workflows.yaml`, `rubric.json`, `conftest.py`, `test_output.py`, `test.sh` | S7 |
| **G18** | the app the agent builds is reachable and healthy at the contract's address | `curl -fsS "$APP_PUBLIC_URL/api/health"` | `200` | the agent phase |
| **G19** | the pytest layer collects and runs against a live app | `pytest /tests/test_output.py` | 27 tests collected, none skipped, none errored at collection | S7 |
| **G20** | `solution/solve.sh` fails loudly rather than pretending | `bash solution/solve.sh; echo $?` | non-zero, with the NO-SOLUTION reason on stderr | S3 |
| **G21** | the oracle scores the reference app at full reward | `harbor run -a oracle` | `reward` `1.0`, twice in a row | the app build |
| **G25** | the reward file lands where `[delivery]` says it does | inspect `/logs/verifier/reward.json` after a run | present, `reward` within `[0.0, 1.0]` | S4 |

## What has to exist before G21 can run at all

The bundle ships **no reference application**, by design. `solution/checklist.md` is the coverage
target it is built from: 340 items across ten sections, every one of them cited by a grader.
`solution/TRUTH.md` carries the ordered correct solve and the thirteen wrong routes it defeats,
and `solution/USER_README.md` carries the seeded logins and the corpus canary. Both are generated
from `solution/trinity/grounding.yaml`, so neither can drift from the other.

Build the app from the checklist, then run the oracle. Until `harbor run -a oracle` returns `1.0`
twice, `task_code.py ledger` must refuse to count this bundle toward any corpus target.

## What the graders expect of the app

- Four seeded accounts, all on `deku-demo-pw-2026`, written into `/app/USER_README.md`:
  `player@example.com` as `Ivy`, `player2@example.com` as `Bo`, `player3@example.com` as `Ren`,
  and `moderator@example.com` as `Wren`.
- `Friday Night Doodles`, code `PARROT42`, seeded with three players against a cap of `4`, so
  exactly one seat is free when the sweep starts. The last-seat test consumes that seat and it is
  not re-seeded between runs, so a second consecutive run against the same database will fail
  that assertion. Reset the volume between oracle runs.
- `Open Table` seeded in `lobby`, which is the room matchmaking reaches.
- An English word list of at least `2000` entries across `easy`, `medium` and `hard`. Several
  tests read the live word from the drawer's own snapshot and then assert it appears nowhere
  else, so the list must be real rather than a single fixture word.
- One unreviewed report against a seat in `Friday Night Doodles`, which is what the moderator
  boundary reads.
- A live event stream at `GET /api/rooms/{code}/events` that a client can hold open. One test
  reads it under a three-second budget and asserts the word is absent from everything it
  receives; a stream that never sends a byte passes that assertion vacuously, so the oracle
  should be checked against a stream that actually carries turn events.
- Room state readable only with a seat token in `X-Seat-Token`, and the room summary readable
  only by a caller who already has the code in the path. Both denials are asserted at the API,
  not in the interface.

## Two things a reviewer should look at first

- **The rubric split.** Fifty-one ui-tagged obligations are shared between two judgment channels:
  thirteen go to `tests/rubric.json` and thirty-eight to browser substeps, because G29 allows an
  item one channel or the other and never both. If a reviewer disagrees with where a particular
  obligation landed, moving it is a `grounding.yaml` edit plus a regeneration, never a
  `tests/rubric.json` edit.
- **The account decision.** The companion is normative that the product has no sign-up, and the
  kit's contract is equally firm that seeded email-and-password accounts exist. The brief keeps
  both by making an account optional and guest play the default front door. That is the one place
  where a reader of the companion will find the brief saying more than its source, and
  `00-decisions.md` records why.

## Exit stamp

```
MECHANICALLY-GREEN except CON-1 placement, NO-SOLUTION
1 red gate: G46 placement, with G47 consequential
NOT ADMISSIBLE
```
