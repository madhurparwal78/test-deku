# Build report - S_saasm_cont_reactive-notebook-showcase-vb_20260916_072253

Rendered at S10 from the receipts of the run. Every number below was read out of an
artifact or a gate receipt; none is transcribed from memory.

## Identity

| Field | Value | Source |
|---|---|---|
| Task code | `S_saasm_cont_reactive-notebook-showcase-vb_20260916_072253` | minted at S1, certified by `task_code_verifier.md` (G3) |
| Task id | `deku/reactive-notebook-showcase-vb` | `[task].name` |
| Category | solo_founder (`S`) | Task Order |
| Domain | `saas-micro-tools` (`saasm`) | Task Order said `saas-productivity`, which is not a level-2 code |
| Pattern | `content-publishing` (`cont`) | Task Order |
| Archetype | `reactive-notebook-showcase` | Task Order |
| Variant | `b` | a companion document was supplied |
| Service profile | `P4-db-storage` | the only profile legal for solo_founder + content-publishing |
| Slots | `backend = postgres`, `storage = minio` | `[metadata.services]` |
| Language | `python` | 2.9 draw: Flask + Jinja |
| uuid_v5 | `17c365a1-2c67-5cbd-a5c4-d6ee681de0fb` | recomputes from `uuid5(NAMESPACE_URL, "deku/<task_code>")` |
| Grader version | `0.22.0` | equals `config/kit-config.yaml` (INV5) |
| QL | Abhishek Shaw `abhishek.shaw@ethara.ai` | `[task].authors[0]` |
| Contributor | Atharv Mahalwar `atharv.mahalwar@ethara.ai` | `[task].authors[1]`, `[metadata].contributor_id` |

**The domain substitution, on the record.** The Task Order arrived with
`domain: saas-productivity`. That string is not one of the 36 level-2 codes, and the
level-2 table partitions domains by category: the nearer data-vocabulary domains
(`analytics-reporting`, `it-devtools`) belong to `enterprise`, which is illegal for a
public-signup storefront. It was keyed to `saas-micro-tools`, the only solo_founder SaaS
domain in the taxonomy. The companion records the same substitution from the other side
in its own section 23. Written into `00-decisions.md` rather than corrected silently.

The contributor address in the Task Order was `atharv/mahalwar@ethara.ai`.
`taskorder_lint` requires a bare `local@domain`, so it was corrected to
`atharv.mahalwar@ethara.ai` in both places it appears.

## Derived-design draws

SHA-256 over the **archetype** at the documented byte offsets, per
`generate_instruction.md` 2.9 / 2.10 and `reference/L` L.6. Never Python's builtin
`hash()`, which is randomised per process.

```
draw: render_model = mpa-progressive
draw: backend      = Flask + Jinja
draw: frontend     = Alpine.js + server templates
draw: nav          = top-nav
draw: work_surface = split detail-pane
draw: create_flow  = dedicated-route
draw: feedback     = toast
```

| Axis | Drawn | Used | Why |
|---|---|---|---|
| `design_direction` | `playful-consumer` | `companion` | `reference/L` L.6.1: a supplied companion beats the bank draw. A drawn direction would overwrite measured fact. |

Every other draw governs. `top-nav` agrees with the companion's own three-item header.
`split detail-pane`, `dedicated-route` and `toast` land on the authoring studio, which the
companion never captured — its section 23 records that the application behind the account
wall was unreachable — so the draw governs there without contradicting anything measured.

**Launch surface**, drawn over the archetype per `reference/O` O.3:

```
no_frontend_secrets, security_headers, sitemap_robots, spam_protection, terms_page
```

Four of the five overlap what the companion already states, so one sentence satisfies both
the draw and the source. `flag_lint` (G41) reports nine bank obligations present against
five drawn — `colour_contrast`, `custom_404`, `form_validation` and `privacy_page` were
already in the brief on the companion's own account. That surplus is a WARN, not a defect.

## Companion document

`C:\Users\Admin\Downloads\observablehq_prd.md`, a capture of a live product.

Carried under the supplied-source rules: every measured fact kept, every colour hex
translated to family/tone/shade words by `source_lint.colour_words()`, the font families
carried exactly, the identities re-cast. `<BRAND>` became **Datalume**;
`<PRACTITIONER_A>` / `<PRACTITIONER_B>` became Alex Rivera (Founder) and Sam Okafor
(Software Engineer III); the notebook authors became Ada Kovacs, Noor Haddad and
Wren Alvarez. No real customer identity survives into the bundle (C-CN-08).

`source_lint` (G51) holds with **nine** recorded waivers, each naming a companion subject
the brief deliberately says less about than the capture:

```
18. performance          zero-asset               acceptance checklist
design-token prefixes    panel / hover grey       pink-orange gradient linear-gradient
microsoft -1 -1 23 23    domain and pattern substitution      media lazy-loads
```

Four companion sections are marked WAIVED in the carry table of `00-decisions.md`
(sections 18, 20, 22, 23) with the reason recorded per section.

The **D5 contradiction sweep** was run over every design, motion, layout and accessibility
sentence in the brief against its companion line. No inversion found. A waiver says the
brief says *less*; an inversion would be the brief saying the *opposite*, and no gate can
tell those apart — which is why the sweep is a reading and not a lint.

## Feature resolution

Nine must-have features in `01-PRD.md`, resolved into ten H2 sections in `instruction.md`.
`## Build plan` is withheld at baseline per `generate_instruction.md` 2.1, which is also
why `06-implementation-plan.md` is absent from the spec folder.

Eight open questions the companion left unanswerable were resolved and recorded in
`00-decisions.md` rather than guessed silently at authoring time.

**The critical focus**, which is what the hidden checklist attacks: object-store
visibility across the draft/publish boundary. A page is a draft at creation. Media
uploaded against a draft page lands in the bucket at
`media/{page_slug}/{sha256_of_bytes}.{ext}` and is **not publicly readable**. The moment
any referencing page publishes, that same object becomes readable **without moving**.
Stated as a storage-level property, graded three ways, and named in the G21 note of the
handoff as the fake-integration target.

## Slot obligations

| Slot | Provider | Critical pytest substep asserting a real side effect |
|---|---|---|
| `backend` | `postgres` | `test_concurrent_publish_yields_one_published_row` |
| `storage` | `minio` | `test_uploaded_bytes_live_in_the_object_store_at_the_digest_key` |

Both read the provider directly through the vendored capability layer, never through the
app's own claim about itself (INV6, certified by `reward_path_lint` G14).

## Grading layer

| Channel | Count | What it owns |
|---|---|---|
| Checklist items | 265 | every obligation in the brief, one per item |
| pytest tests | 53 | one module, `tests/test_output.py` |
| Workflows | 16 | `tests/workflows.yaml` |
| Browser substeps | 39 | the walked, rendered half |
| Judged criteria | 19 | `tests/rubric.json`, generated from `grounding.yaml` |
| Trajectory steps | 16 | `solution/trinity/grounding.yaml` |
| Rejected routes | 12 | the paths the answer key explicitly forecloses |

**Coverage, both directions (G24).** Every checklist item is cited by at least one
grader, and every grader cites at least one item. **Channel exclusivity (G28/G29).** Every
part of every ask is graded by exactly one channel: pytest 183, browser 65, rubric 23,
with six items legitimately shared by pytest and browser because a deterministic aspect
and a walked one are different parts.

Eight items were judged twice at first pass — `C-CF-31`, `C-CF-33`, `C-CF-38`, `C-UX-12`,
`C-UX-24`, `C-UX-32`, `C-UX-34`, `C-UX-39`. The rubric kept each; the browser `cov:` tags
were dropped, and the four substeps whose only citation was one of those were removed.

### Rubric dimension shares, positive scores only

| Dimension | Criteria | Points | Share | Frozen weight |
|---|---|---|---|---|
| instruction_following | 4 | 18 | 0.300 | 0.30 |
| functionality | 3 | 15 | 0.250 | 0.25 |
| ui_visual | 3 | 9 | 0.150 | 0.15 |
| ux_flow | 3 | 9 | 0.150 | 0.15 |
| motion | 2 | 3 | 0.050 | 0.05 |
| accessibility | 2 | 3 | 0.050 | 0.05 |
| responsiveness | 2 | 3 | 0.050 | 0.05 |

Exactly on the `reference/I` §I.5 budget. Three of the nineteen are negative criteria, and
each carries a *different* inversion-marker sentence rather than one pasted line, because
a stamped rule sentence is itself a G52 finding.

`rubric_context_lint` (G52) reports 19/19 criteria naming a surface drawn from the brief's
own route table and headings, over a 126-term anchor vocabulary.

## Literals ledger

104 pinned literals in `_handoff/<code>.literals-ledger.json`:

| Class | Count |
|---|---|
| scheme | 32 |
| seed_record | 16 |
| number | 14 |
| route | 10 |
| endpoint | 10 |
| env_var | 7 |
| design_phrase | 7 |
| status | 4 |
| account | 3 |
| credential | 1 |

`fixture_lint` (G6) confirms every one of them appears in `instruction.md` on a single
line, which is the failure mode that cost the previous run several passes: a pinned phrase
split across a line wrap reads as absent.

The seeded corpus is 33 notebooks, nine of them pinned by exact star value, one marked as
a fork; three published pages and one draft (`field-guide`, owned by the second author);
the listing pages at 30 per page across four sort tabs.

## Spec folder

`Output/_spec/S_saasm_cont_reactive-notebook-showcase-vb_20260916_072253/`

| Doc | Present |
|---|---|
| `00-decisions.md` | yes |
| `01-PRD.md` | yes |
| `02-TRD.md` | yes |
| `03-app-flow.md` | yes |
| `04-uiux-brief.md` | yes |
| `05-backend-schema.md` | yes |
| `06-implementation-plan.md` | **no** — `## Build plan` is not emitted at baseline, so the doc that feeds it has nothing to feed |

`05-backend-schema.md` carries twelve tables and eleven invariants stated as storage-level
properties, including the critical one. Seeding is idempotent and stated so.

Routes and endpoints round-trip between the brief and the spec in both directions. Three
strings are one-sided and none is graded-class: `/app/USER_README.md` (a bundle-contract
path), `/field-guide` (present in the spec as the slug and inside
`/studio/pages/field-guide`), and `/500` (present only inside the companion carry table,
recording that the companion's separate 500 screen was folded into the one not-found
screen).

## Grading window

`window_lint` (G33) reports length and never fails it.

| Section | Chars | Reference | Flag |
|---|---|---|---|
| core_features | 14687 | 2400 | past-slice |
| user_flow | 3055 | 1900 | past-slice |
| ui_ux_notes | 8548 | 1700 | past-slice |
| constraints | 1387 | 800 | over-reference |
| user_roles | 1574 | 1000 | over-reference |
| overview | 1531 | 700 | over-reference |
| **joined total** | **30782** | 8800 | past-slice |

The tail reaches the agent in full and the judge only to the slice. Graded rules are
front-loaded, and every judged criterion carries its own facts inside the criterion, so
the overage costs a diagnostic number rather than reward.

## Kit gate log

Rendered from `_handoff/<code>.gates.jsonl` — **32 rows**, one per gate, each carrying the
SHA-256 of the bytes it examined. **ALL GATES GREEN.**

Not proven here, by design:

- **battery 3, handoff-owned:** G13, G15, G18, G19, G20, G21, G25 — these need a built
  image and a running app.
- **prose / adversarial:** G23, G34, G35, G36, G37b — recorded as SELF-ATTESTED receipts
  (owner == verifier in a single-agent run), never as independent verdicts.
- **G2 / G16:** NOT-APPLICABLE. `[delivery]` is absent and grandfathered; see the handoff.
- **G48 replay half:** DEFERRED (NO-SOLUTION). There is no reference app and no
  known-wrong controls, so the liveness check runs downstream. An explicit deferral, not
  a quiet pass.

### Certification receipts (G40)

All thirteen prompts carry a current, bundle-bound receipt with the scorecard its own
registry declares: QC_instruction (24 checks), QC_spec (15), qc_docker (105),
qc_rubric (16), qc_solution_checklist (adjudication, no numbered registry), qc_toml (120),
task_code_verifier (12), plus the six advisory generator prompts.

Non-PASS verdicts on the scorecards, all recorded with their reason in the receipt:

| Prompt | Id | Verdict | Reason |
|---|---|---|---|
| QC_spec | S1 | WARN | six spec docs, not seven (no `06-`) |
| QC_spec | S7 | NOT-APPLICABLE | nothing to shape-check |
| qc_docker | CMP-020 | WARN | `main` carries `extra_hosts` + `ports`; C12 in `validate_task.py` mandates exactly that and supersedes the row |
| qc_docker | ARCH-002/003/011, BLD-004, BP-005, DEP-015/016/017, ENV-003/004 | NOT-APPLICABLE | no digests, no COPY of app source, no VOLUME, no ENTRYPOINT, not a compiled language |
| qc_toml | BENCH-003 | WARN | turns/tokens sit in the `hard` band but `difficulty` is still the empty placeholder |
| qc_toml | BENCH-002/005, INST-007, SIGN-001/002/003, TAX-006 | NOT-APPLICABLE | not a trivial task, `instruction.md` present, `[signoff]` retired |

## Traceability

- `_handoff/<code>.sources.json` — which source document each artifact was built from
- `_handoff/<code>.literals-ledger.json` — 104 literals, `literals-ledger-v1`
- `_handoff/<code>.pytest-provenance.json` — 53 tests to the items they observe,
  `pytest-provenance-v1`
- `_handoff/<code>.rubric-provenance.json` — R1–R19 with their anchors and facets,
  `rubric-provenance-v1`
- `_handoff/<code>.checklist-qc.md` — the checklist review
- `_handoff/<code>.receipts.json` — `prompt-receipts-v2`, thirteen prompts
- `_handoff/<code>.gates.jsonl` — 32 gate receipts with content hashes
- `tests/traceability*` — item-to-grader matrices

Coverage citations live in the `pytest-provenance-v1` sidecar rather than in `# cov:`
comments, because `comment_lint` (G54) rejects a comment anywhere in an emitted file.

## Blocking findings

**None open.** Findings raised and closed during the run, worth recording because each was
a real defect rather than a lint artifact:

1. **A pinned type scale in `## UI/UX notes`.** The Typography paragraph handed over
   `6rem` / `5rem` and a full px ladder from `56px` on `64px` down to `8px`. QC_instruction
   C4 bans pinned type sizes as a numeric recipe, and the companion carve-out covers
   character phrases and font *families* only. Nothing in the checklist, the ledger or
   `grounding.yaml` cited those numbers, so the scale was rewritten as direction. Two
   numbers remain and both are contract rather than taste: `12px` for captions and
   metadata (graded as C-UX-13) and the `16px` body floor in the accessibility bar.
2. **Thirty G24 forward orphans.** Closed by writing one new test
   (`test_public_documents_reference_no_third_party_origin`), making two existing tests
   actually assert what they were cited for (UTC timestamps, author-email uniqueness),
   extending the provenance sidecar where a test genuinely observes the item, and adding
   six browser substeps for the constraint and typography claims a browser can see.
3. **Eight double-judged items.** Resolved in favour of the rubric; see Grading layer.
4. **One genuinely unobservable obligation.** `C-TR-05`, stdout request logging, removed
   from the checklist and escalated in the handoff under OPEN-DECISIONS D-H rather than
   left as an orphan or covered by a test that could not honestly see it. `C-TR-06..10`
   renumbered to `C-TR-05..09` across the checklist, `grounding.yaml` and the pytest
   provenance.
5. **A workflow count outside the band.** 18 workflows merged to 16 by folding the
   publish-idempotence and invalid-block-kind workflows into neighbours.

## Budget

`turns_expected = 170`, `tokens_expected = 7000000` — the documented `hard` band.
Standard resource tier: 4 cpus, 8192 MB, 20480 MB storage, 900 s build, 18000 s agent,
3600 s verifier. `difficulty` stays the empty placeholder until calibration writes one;
`pass_rate`, `pass_rate_ci` and `calibration_trials` are the zero placeholders. No
metric was fabricated.

## Exit state

```
MECHANICALLY-GREEN, NO-SOLUTION
```

All 32 kit gates green. Not admissible: the bundle carries no reference app, so nothing
here has been built, started or run. Read
`_handoff/S_saasm_cont_reactive-notebook-showcase-vb_20260916_072253.handoff.md` for the
ordered handoff gates, the two open items, and the route-back table.
