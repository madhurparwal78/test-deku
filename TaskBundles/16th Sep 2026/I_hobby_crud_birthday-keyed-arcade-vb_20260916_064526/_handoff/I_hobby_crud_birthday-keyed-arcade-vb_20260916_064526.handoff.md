# Handoff contract - deku/birthday-keyed-arcade-vb

Exit state: **MECHANICALLY-GREEN, NO-SOLUTION**. Every static gate is green. The
bundle becomes admissible when the app is generated downstream from
`solution/checklist.md` and `harbor run -a oracle` returns `1.0` twice.

## What the operator must run

```
docker build --platform linux/amd64,linux/arm64 -f environment/Dockerfile .
docker build -t deku-verifier-base -f <grader>/Dockerfile <grader-root>
docker build -f tests/Dockerfile tests/
docker compose -f environment/docker-compose.yaml up --wait
harbor run -a oracle
```

## Gates this kit cannot run (battery 3, handoff-owned)

G13 dual-architecture image build - G15 provider resolution at boot - G18
environment boots - G19 oracle returns 1.0 twice - G20 solve.sh deploys a real
app - G21 reward path - G25 calibration.

## Two defects in the Task Order, corrected

`domain: hobby-collections` is not in the closed enum; the value is
`hobby-collection`. `pattern: media-gallery` is not one of the fifteen patterns
at all. The product's own spine is a catalogue of sixteen series browsed and
kept from, so the pattern is `crud-catalog`, whose critical focus -- a persisted
row matching the interface and surviving a reload -- lands exactly on PRD
section 14.2.

## The architectural conflict, and how it was resolved

PRD section 0.1 fixes the runtime at the browser: *"There is no server in this
product"*. The kit's App Contract requires a served origin and `GET /api/health`,
and the empty-services loophole is closed in `validate_task.py`, so every legal
profile forces a backing service.

The resolution, stated in the brief rather than hidden:

- The App Contract governs **deployment**. A production server serves the built
  application and answers the readiness probe. Section 0.1 fixes the runtime of
  **product behaviour**, which stays in the browser. These do not collide.
- The `db` slot holds the **read-only catalogue** only: sixteen series, 366 day
  colours, the hub order, the award record, the wheel categories, the oracle
  decks, the prompts and the prize odds. PRD section 23.11 independently
  requires exactly this content be editable without touching code, so the slot
  is PRD-mandated rather than forced.
- **Every piece of reader state stays on the device** -- collection, bests,
  daily history, shard ledger, preferences. Section 19's "no server-held
  collection" holds, and a critical test probes `/api/collection`,
  `/api/scores` and `/api/shards` to prove no write route exists.

`concurrency_hardening` was **dropped** from `capability_flags` for the same
reason: its gate demands a `409 Conflict` signal, which requires a server-side
write the PRD forbids. Declaring it would have written a self-contradiction into
the brief. The two-tabs-one-balance and double-press traps remain, graded by the
browser channel.

## G40 is SELF-ATTESTED, and that is recorded rather than hidden

All 292 check ids across the six certification prompts carry a verdict in
`<code>.receipts.json`, every token bound to this bundle. `verifier` is `self`
on every row: the agent that authored the artifacts also ran the QC prompts, so
the kit's `owner != verifier` rule is NOT satisfied. The gate reports
SELF-ATTESTED and the sweep records WARN, not PASS-as-independent. An
independent reviewer re-running the prompts is still owed.

The review found and fixed one real defect and recorded three deprecations:

| Check | Finding | Outcome |
|---|---|---|
| RC-16 | All eighteen evaluation rules were written to one template, `Answer yes when X; answer no when Y`, with only the claims swapped. A stamp hides missing facts. | Every rule rewritten to say what a reviewer actually does on the running product, in its own shape |
| SIGN-001/2/3 | Deprecated in the prompt on 2026-09-15, superseded by SIGN-004 | Recorded NOT-APPLICABLE; the bundle carries no `[signoff]` table, which SIGN-004 and G62 both require |
| BP-003 | `nodejs` installs from the NodeSource `node_20.x` channel, so the minor floats | WARN, recorded; pinning every apt version would break per-architecture resolution |
| QC_spec S1-S10 | They audit the seven-doc `spec/` folder that CON-1 retires | NOT-APPLICABLE |

## Three kit changes this revision, worth knowing

This kit revision differs from the one used on 11 September, and all three
reversed a previous requirement:

- **`[signoff]` is retired.** G62 now fails a bundle that carries one. The
  previous revision required it.
- **The instruction-following overlay is retired.** `tests/if_constraints.json`
  and `solution/trinity/if.yaml` must be absent; G56/G57/G58 fail a bundle
  shipping either. The previous revision required the file.
- **`solution/app/` is retired** and the canary moved to `solution/TRUTH.md` as
  a two-line block rendered from `grounding.yaml`'s `canary_block`, which must
  be a **list of two lines**, not a string; the generator iterates it.
- **Workflow substeps now carry `category` and `weight`**, and the category mix
  is enforced: at least one `core_outcome` and, with a storage slot declared, at
  least two `data_integrity`.

## Carriage record

The companion PRD (`myshaky_prd.md`, 3,312 lines) is recorded in
`<code>.sources.json`; the four waivers are passed on the sweep command line as
`--waive taxonomy --waive confidence --waive media-gallery --waive "freely chosen"`. G51 reports **16/16 colours, 160/160 topics and 284/284
enumerated items** carried into `instruction.md`, with four waivers: the PRD's
own taxonomy mapping, its confidence statement, and two rows of its taxonomy
table. All four are document apparatus explaining how to read the PRD, not build
obligations.

## What this task measures

Reward is `passing_workflows / total_workflows`, and the individual tier caps a
task at eleven workflows. **All eleven carry fewer than ten substeps, so every
one is all-or-nothing, and every one now carries at least one critical trap
drawn from the PRD's own acceptance checklist (section 23).** 69 substeps, 37
critical. The easy HTTP facts no longer own a workflow of their own; each rides
beside a trap, so a build that gets the arithmetic right and the device state
wrong scores near zero rather than near two thirds.

Each trap is a wrong default a competent build reaches for, observable from
outside, stated in the brief:

| Wrong default | PRD | Where it zeroes a workflow |
|---|---|---|
| Validate or count the day in the device's current year | 6.2, 23.1 | a finder refusing 29 February when the device believes 2027 |
| Page a non-unique ordering by keyset on that value alone, or decode a cursor unchecked | 16, 23.11 | the phase walk skips; a forged or foreign cursor answers 500 |
| Take the day from the UTC date | 14.9, 14.10, 23.5 | the prompt does not turn over one minute after local midnight in UTC+14; two readers on one local date meet two boards |
| One sequence of chance for every game | 14.9 | spinning the wheel first changes the puzzle's board |
| Remember only the last day a claim was made | 14.10 | clock forward, back, forward claims one day twice |
| Reset or rewrite the store when the date goes backwards | 14.10 | the collection or the purse changes after a backwards date |
| Hold the balance in the tab that loaded it | 14.5, 23.4 | the second tab keeps the old balance and overwrites the first tab's spend |
| No guard between an exchange and its reward | 13.10, 23.4 | a double press debits twice |
| Trust or emit a result inside a share link | 14.11, 23.5 | a forged number reaches the screen; a created link carries the number |
| Replace on import, add balances, concatenate ledgers | 14.12, 14.14, 23.5 | the later keeping time wins; two purses sum; the welcome counts twice |
| Import the sound entries of a partly bad file | 14.12, 23.5 | a file with one impossible date still adds its other entry |
| Shuffle the tiles by a uniform permutation | 13.3, 23.3 | thirty boards over six days include an unsolvable one |
| Undo the board without the counter | 13.3, 23.3 | the count keeps rising while the board goes back |
| Read storage unguarded at startup | 14.1, 23.2 | a blank page when the browser refuses storage |
| One `clear()` behind every delete | 14.8, 23.2 | deleting the collection empties the purse |
| A menu that does not take and hold focus | 7.1, 23.6 | Tab reaches the page behind; Escape strands focus |

**Every trap was proven both ways before it shipped.** A scratch reference of
the pinned contract (a stdlib server plus a vanilla client, kept outside the
bundle) passes all 46 non-datastore tests in the pinned verifier base image
(`playwright/python:v1.49.1-noble`, `playwright==1.49.1`). Twenty-four
wrong-default switches were then flipped one at a time, and each made exactly the
test aimed at it fail on its intended assertion, not on an error.

## Second audit pass, and what it found

Run after the first green sweep, hunting the gaps no gate checks.

| Gap | Why it mattered | Fix |
|---|---|---|
| `test_birthday_finder_refuses_a_bot_submission` POSTed to a GET-only route and accepted `405` | Every framework answers 405 there, so the test passed with **zero** spam protection built. A free point, and because reward is a ratio a free workflow raises a failing model's score | The decoy parameter `website` and a stated rate limit (more than 30 resolutions inside 10 seconds answers 429) are now pinned in the brief, and the test grades both |
| `assert "2026" not in blob or "ordinal" in blob` | The right-hand clause is always true, so the assertion could never fail | Replaced with the leap-year month-start table: the first of each month must resolve to 1, 32, 61, 92, 122, 153, 183, 214, 245, 275, 306, 336. A common-year build is off by one from March onward |
| Alt-text test passed on a route with no visuals at all | A page rendering nothing scored the point | Now also requires the route to render at least one image or inline vector |
| Secret scan skipped when no script asset resolved | A build serving no JS was never scanned | Now requires at least one same-origin script to resolve, and scans it |
| Social preview image check skipped for an absolute URL | A build could point the preview off-origin and skip the resolve check | The preview must be same-origin and must answer 200 |
| Write-probe test passed against a server that answers 404 to everything | A static-only build scored the architectural point | The read API must answer before the write probes count |
| `No route nests and no route takes a parameter` | Unqualified, it forbade the query parameters `/api/resolve` needs, contradicting `## Technical requirements` | Narrowed to page routes and path parameters, with the query-parameter case stated |

Also checked and clean: every response field the tests read is pinned in the
brief (29 of 29); all twenty browser substeps name a concrete target the brief
states; and `tests/traceability.md` / `.csv` are correctly absent, having been
retired on 2026-09-15 -- shipping them would fail G47.

## Realignment to the kit, 2026-09-16

The kit moved after this bundle was minted. Four commits landed between 11:35
and 12:27; the bundle was minted at 06:45. Every one of them invalidated
something, and the sweep found all four rather than a reading of the diff.

| Kit change | What broke | Realignment |
|---|---|---|
| `da24d3b` the pytest module is renamed `tests/test_output.py`, and the generated answer key becomes `test_ans.py` | G46 failed on the module name; G48 failed on the missing generator output | Module renamed, `workflows.yaml` and `tests/Dockerfile` references updated, `solution/trinity/test_output.py` removed in favour of the generated `test_ans.py` |
| `11eaf7b` `[verifier].environment_mode` defaults to `"separate"` | The bundle emitted the legacy `"shared"` | Switched. The agent image no longer carries the grader's Python packages, which G55 RD-1 skips under separate |
| `78e5ba6` the vendored `test.sh` was re-pinned | G0/INV5 failed on a byte mismatch | Re-vendored |
| `806eb0a` `solution/USER_README.md` is restored as a GENERATED file | G1 and G12 failed: the harness greps for the canary by that filename | Regenerated from `grounding.yaml` by `recompute.py`, so it cannot drift from `TRUTH.md` |

### The change that quietly broke a grader

Switching to `"separate"` put the grader in its own container, and
`test_structured_logs_carry_request_id` read `/tmp/app.log` **from the
filesystem**. Under shared mode that worked; under separate it cannot reach the
agent's filesystem at all, so the assertion would have failed on a correct
build. No gate catches this -- it is a cross-container reachability question.

The brief now requires every response to carry the same identifier in an
`X-Request-Id` header, and the test reads that instead. The `stdout` and
`/tmp/app.log` obligations stay in `## Technical requirements`, where the
observability flag needs them; the header is the observable an outside process
can actually reach.

### A gap the realignment exposed

With the grader's packages gone from the agent image, the `backend` fixture was
left unused: **no test touched the datastore at all.** The brief says `postgres`
holds the catalogue, and nothing verified it, so a build serving the catalogue
from a JSON file in the image would have passed every workflow.

`test_catalogue_is_served_from_the_datastore` now reads the datastore directly,
asserts a table holds at least 5856 rows, and reconciles that against the count
the API publishes. It is critical, and it closes the cheapest shortcut available
in this task.

## Difficulty revision, 2026-09-16

Requested after the bundle was green: make the model struggle in the harness,
from the PRD, without leaving the tier.

### A solvability defect this revision found and fixed

The session client was rooted at `APP_PUBLIC_URL/api` while every test asked for
`/api/...`, and httpx joins the two: every request went to `/api/api/...`, and
`/`, `/games` and `/index.html` went under `/api/`. Measured in the verifier base
image with `httpx==0.28.1`. **A perfect build would have failed nearly every
pytest substep.** The client is now rooted at `APP_PUBLIC_URL`.

### False coverage removed

`test_nothing_a_reader_produces_reaches_the_server` claimed twenty checklist items
(two tabs, the clock, the puzzle, undo, the matcher, merge, links) while sending
four POSTs. `test_prize_tiers_carry_prices_and_odds_that_sum_to_one` claimed the
ledger and the zero floor, and the oracle-deck test claimed the wheel. Each claim
now sits on the test that observes it. Two items stay cited nominally because no
outside observer can see them: `C-TR-01` (Flask) and `C-TR-02` (Vue 3 with Vite).
`C-TR-19` (two cards face up) is carried by a browser substep.

### A rate limit that would have failed a correct build

More than thirty resolutions in ten seconds answered `429` for any caller, while
the brief requires the browser to re-derive characters through the same endpoint.
The suite's own resolver tests already made thirty calls in seconds. The limit now
counts finder submissions, which carry the decoy `website`, and the flood test
runs last.

### What the brief now pins

Accessible names and copy for the finder, the collection, the menu, the machine,
the claim, the puzzle grid, the wheel, the challenge, removal and import; the
character link format and its validation; the store file format, what makes one
unreadable, and the merge rule for every kind, including the ledger rule the PRD
left to the build. Nothing pinned is a mechanism: no storage API, no event name,
no library. The judged window stays under its caps (joined 8961 of 9000).

### Definition of done rewritten

It was a fifteen-line bulleted list, which QC_instruction D3a refuses: the section
is one paragraph of two to four sentences naming the core outcome and the hardest
guarantee. It is now 78 words. Every fact the bullets carried is still stated in
`## Technical requirements` and `## Data model`.

### Still owed

- **The QC receipts predate this revision.** They certify the brief, checklist
  and graders as they stood at 13:00. G40 stays green because receipts bind to the
  prompt and the task code, not to file content, so a re-run of `QC_instruction`,
  `qc_solution_checklist` and `qc_rubric` against this revision is owed and has
  not been done.
- The datastore test was not run against the scratch reference, which has no
  datastore.
- Harness timing is unmeasured: the suite drove Chromium in 12s against the
  scratch reference, and a real Vue build with animations will be slower.

Final shape: 11 workflows, 69 substeps (22 browser, 47 pytest), 37 critical, all
eleven all-or-nothing, 47 tests in a 47-to-47 bijection with the cited substeps,
114 checklist items, 18 judged criteria.
