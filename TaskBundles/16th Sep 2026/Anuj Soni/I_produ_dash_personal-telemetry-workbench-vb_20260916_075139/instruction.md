# Personal Telemetry Workbench

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, sign in as the owner, open a
project, drag a rectangle across the event field, and read a cohort size that equals the number of
distinct people in the raw events underneath that rectangle, then save that cohort and find it
again after a reload, without hitting an error page. The same span read at the coarsest
magnification and at the finest must report the same number of events, because the whole offer of
this product is that the owner is looking at the data rather than at a summary of it. A different
stranger who owns another workspace must NOT be able to read that project, those events, that
person or that operation log by any means, including a direct request naming an identifier they
somehow learned. A number the interface shows itself does not count; the stored events are the
fact, and every figure the workbench displays has to be reachable back to them.

## Overview

One developer, working solo, runs this workbench to measure the software they ship. It is
local-first in the one sense that matters here: every analytical question is answered by the
workbench's own query engine out of its own store, and the interface says on every result where
that answer came from and how much it read. It holds their own archive of behavioural events, the session recordings captured alongside those events, the feature flags
evaluated for them, the experiments running over them, the error groups raised by them and the
survey answers collected from them. All six resolve to one person identity and one clock, so any of
them can be pivoted to from any other in a single interaction.

The people whose behaviour the archive describes are data subjects, not users of the workbench.
They never sign in, they hold no account and they have no interface. They exist in the data as
persons and aliases, and the owner carries their access, deletion and consent rights personally,
which is why those obligations are first-class features here rather than an administrative corner.

The primary surface is the Grain: a field whose horizontal axis is wall-clock time across the whole
retained archive and whose vertical axis is a bound dimension, by default the distinct person
ordered by when that person was first seen. Every event is one mark. The Grain is the event
explorer, the query result surface, the cohort builder and the way into a recording, all at once.
Analysis is not a section of this product; analysis is the product, and every other surface is a
lens on the field.

Tenancy is one account, one workspace, and every row in every table belongs to exactly one
workspace. Governance here is a privacy baseline the owner discharges personally rather than a
compliance programme run by somebody else.

It deliberately is not several other things. There is no organisation above the account, no second
member, no seat, no invitation and no delegated administration. There is no file upload and no
object store, no email and no notification, no payment and no billing, no marketplace, no
artificial intelligence feature and no external network call at run time.

The genuinely hard part is reconciliation. Every number the workbench shows has to agree with the
raw events it was computed from, at every magnification, through every surface and in both
directions, and the product has to stay honest about where each number came from and how much it
read to produce it.

## User roles

One person signs in: the owner. Two further principals act without a session, and both are bounded
by a scope the owner wrote.

| Principal | Can do | Cannot do |
|---|---|---|
| `owner` | everything in the workspace that account owns: read and write projects, events, insights, dashboards, cohorts, flags, experiments, issues, surveys, destinations, shares and keys, and read the operation log and the audit chain | **cannot** reach any workspace that account does not own, by any route, including a direct request naming an identifier |
| `key` | exactly the actions its scope set names, in the workspace that issued it, over the API only | **cannot** act outside its scopes, **cannot** erase a person, **cannot** generate an access package, and **cannot** create or revoke another key |
| `link` | read the one artefact its share token scopes, at the fidelity that token permits | **cannot** reach any other artefact, **cannot** reach an underlying event or person identifier unless the scope permits, and **cannot** be told whether something outside the scope exists |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `key` session to any `owner`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

A key's scope set is drawn from exactly six names: `event:read`, `insight:write`, `flag:write`,
`experiment:write`, `pipeline:write` and `share:write`. The scope set is the whole permission
matrix here: there is no role hierarchy above the owner and
no delegated administration beneath them, so a request either comes from the account that owns the
resource or presents a scope that names the exact action. A scoped key is refused with the scope it
was missing named in the refusal, so the owner can fix
the key rather than guess. Erasing a person and generating an access package both need an
interactive session that has re-confirmed the password within the step-up window; a key is never
sufficient for either, whatever scopes it carries.

Signup is open. A new account owns a new empty workspace and reaches nothing else, so it sees its
own workspace with no projects in it and nothing further. Every seeded account uses the password
`deku-demo-pw-2026`. `owner@example.com` is Marisol Vega, who owns `Northlight Labs`.
`other@example.com` is Anders Roeg, who owns `Coldwater Games` and holds nothing in
`Northlight Labs`.

## Core features

### Reconciliation, which is the point of the product

1. **A total read at any band equals the total read at any other band, for the same span and the
   same filter.** `GET /api/projects/{projectSlug}/field` takes `from`, `to`, `band` and `dim` and
   returns the marks for that band together with `total`, the number of events in the span, and
   `persons`, the number of distinct persons in it. Requesting the same `from` and `to` at `epoch`,
   `season`, `week`, `session` and `moment` returns five different drawings of one span and one
   value of `total`. A band that reports its own rounded figure is the defect this rule exists to
   catch.
2. **A cohort's size equals the distinct persons in the raw events underneath it.**
   `POST /api/projects/{projectSlug}/cohorts/resolve` takes `from`, `to`, `dimFrom`, `dimTo` and an
   optional `types` list, and returns `cardinality`, `eventCount` and `personIds`. `cardinality`
   equals the length of `personIds`, and `personIds` equals the distinct `personId` values in
   `GET /api/projects/{projectSlug}/events` over the same span and the same filter.
3. **A funnel step count equals the persons the raw events place at that step.** A funnel is
   ordered: a person counts at a step only when that person has the step's event after the previous
   step's event.
4. Resolving the same region twice returns the same numbers. Nothing about a reconciliation depends
   on which surface asked or on how magnified the field was when it was asked.
5. Worked example, and the algorithm must reproduce it exactly. The seeded `Ledgerline` archive
   holds `2400` events across `8` persons. Brushing the whole archive with no filter resolves a
   cohort of `8` with an event count of `2400`. The funnel `app_opened` then `search_run` then
   `report_exported` over the whole archive gives `8`, `7` and `5` persons, so the second step
   converts at `87.50%`, the third at `71.43%` and the whole funnel at `62.50%`. Those eight
   numbers are the ones to reproduce.
6. Percentages are never rounded in a way that hides a decision boundary. A conversion of `71.43%`
   is shown as `71.43%` and not as `71%`. A count above `10000` may be abbreviated in the
   interface, and the exact value is always reachable on hover and is always what assistive
   technology reads.

### The Grain

1. The field draws one mark per event, with time across and the bound dimension down. `dim` takes
   exactly `person`, `session` or `release`, and `person` is the default, ordered by the moment
   each person was first seen.
2. Five bands occupy the zoom range and each is addressed by the exact slug `epoch`, `season`,
   `week`, `session` or `moment`. Which band is in force follows from the visible span; the spans
   at which the boundaries sit are yours to choose. `epoch` is a density field of one cell per
   person and day coloured by the dominant event class, `season` is banded density with a hue per
   event type, `week` groups nearby events into one mark, `session` is one mark per event with
   person lanes resolved and session boundaries drawn, and `moment` is one mark per event carrying
   property labels with replay frames and log lines interleaved.
3. Crossing a boundary cross-fades the two representations into one another rather than swapping
   them, and each boundary carries enough hysteresis that a viewport resting on a boundary and
   nudged back and forth stays on one representation. A band transition never shows an empty field:
   the outgoing band persists until the incoming one has something to draw.
4. Zoom is continuous from the whole archive down to a single millisecond, with no boundary the
   owner has to cancel an interaction to cross. One wheel notch or one pinch changes the visible
   span by the same proportion at every scale, so zooming is exponential in the span rather than
   linear in it, and the time axis under the pointer does not move while it happens.
5. Overlays draw into the same field under the same view as the marks beneath them. Funnel steps,
   retention bands, variant splits and error clusters are geometry over the raw events rather than
   a chart that replaces them. Across the whole zoom range an overlay and the events under it stay
   registered against each other.
6. Brushing a rectangle defines a cohort. While the drag is running an approximate size is shown
   and is labelled approximate; the exact figure replaces it on release. On release the marks
   outside the region dim and the marks inside hold their full presence.
7. A resolved cohort is saved by name through
   `POST /api/projects/{projectSlug}/cohorts`, and a saved cohort states whether it is fixed or
   recomputing and when it was last computed.
8. The field's whole state is in its address: the time bounds, the bound dimension, the active
   overlays, the colour mapping and the event-type filter. An address copied at any moment restores
   an identical view. Moving the viewport does not fill the history; one history entry is committed
   once movement settles, so going back means going back to the previous place the owner settled.
9. An unrecognised address renders the workbench's own not-found page inside the shell with the
   rail intact, and the field is not torn down by it.
10. A project with no events renders the shape the field will take once data exists, at almost no
    strength, and says why it is empty. No demonstration dataset and no fabricated events are ever
    shown.

### Ingest

1. `POST /i/v1/events` takes a batch of up to `500` events and an `X-Ingest-Key` header carrying
   the target project's ingest key. The body is a JSON array; each entry carries `type`,
   `distinctId`, `timestamp` and an optional `properties` object and `dedupeKey`.
2. The answer names what happened to every entry: `accepted`, the number admitted, and `rejected`,
   an array whose entries each carry `index` and `code`. A batch carrying two malformed events out
   of five hundred admits four hundred and ninety-eight and names both refusals by index. No valid
   event is discarded because an invalid one travelled beside it.
3. Acceptance means durably recorded, and the workbench says so rather than implying the event is
   already queryable.
4. Deduplication is by `dedupeKey` within one project over the trailing `24` hours. The same key
   twice yields one event, and the second entry is reported as accepted with the duplicate named
   rather than as a failure.
5. A `timestamp` more than `24` hours in the future is clamped to the moment it was received and
   the event is flagged as clamped. A `timestamp` more than `5` years in the past is refused on live
   ingest and is accepted only through a backfill import, because a live event dated years ago is a
   clock fault and accepting it quietly corrupts every trend.
6. An ingest key that names a different project than the one addressed is refused with
   `project_mismatch`, and the refusal states the scope the key actually holds.
7. An event arriving for an erased person is refused with `person_erased` and no person record is
   recreated.

### Persons and identity

1. `GET /api/projects/{projectSlug}/persons/{personId}` returns one person with their properties,
   their aliases and their correlated timeline: events, session boundaries, recordings, error
   occurrences, flag evaluations and survey answers, on one clock, newest first.
2. `POST /api/projects/{projectSlug}/persons/resolve` takes `identifier` and returns the person it
   resolves to through the alias graph, or a refusal naming the identifier when nothing matches.
3. A person property carries its current value, its previous value, and the moment and the source
   of the last change. A property written by more than one source lists all of them.
4. An identity merge is recorded with the moment and the alias that caused it, is reversible for
   `30` days, and the surface states how much of that window is left.
5. `POST /api/projects/{projectSlug}/persons/{personId}/access-package` gathers every event,
   property, recording, survey answer, flag evaluation and alias for that person into one
   machine-readable document and one human-readable summary. It reaches every alias the identity
   graph resolves, including those the owner did not name, and states `aliasCount`, how many were
   found. The result is downloadable once through a link that expires.
6. `POST /api/projects/{projectSlug}/persons/{personId}/erase` records the request with its
   `legalBasis` before any data is touched, then propagates through the archive, the recordings,
   the derived rollups and every enabled destination.
7. `GET /api/projects/{projectSlug}/erasures/{erasureId}` returns a completion certificate naming
   `storesCompleted`, `storesUnreachable` and `residualWindowDays`. A store that could not be
   reached is listed by name. The certificate never claims a completeness it cannot support.
8. Both the access package and the erasure require an interactive session that has re-confirmed the
   password inside the step-up window. A key is refused for either, with the reason named.

### Insights

1. An insight is a saved analysis of exactly one kind, addressed by the exact slug `trend`,
   `funnel`, `retention`, `path` or `distribution`. It carries its series, its filters, its
   breakdown, its time range and its name.
2. **An insight is created through a three-step wizard, and each step has its own address.** Step
   one chooses the kind, step two defines the series, the filters and the breakdown, and step
   three names it and saves it. Moving back and forward between steps preserves everything already
   entered, a step reached directly by its address restores what the earlier steps hold, and the
   save control exists only on the third step.
3. `POST /api/projects/{projectSlug}/query` runs an analysis without saving it and
   `POST /api/projects/{projectSlug}/insights` saves one.
   `GET /api/projects/{projectSlug}/insights/{insightId}/result` runs a saved one.
4. **Every result carries its own provenance.** The answer holds an `execution` object with
   `source`, which takes exactly `store` or `rollup`, `rowsScanned`, `durationMs`, `sampled` and
   `samplingRate`. A result with no `execution` object is not displayable, and the interface shows
   that provenance beside every number it draws.
5. A time range is either relative, which re-evaluates whenever the insight is opened, or absolute,
   which is frozen. Which one an insight holds is visible in the interface, because a saved
   analysis that silently re-evaluates is a source of wrong decisions.
6. A funnel holds at least `2` and at most `20` steps. A retention analysis needs a start event and
   a return event. Steps are reordered by dragging and by keyboard, and reordering re-runs the
   analysis and cancels any run still in flight.
7. A breakdown on a property carrying more than `10000` distinct values is refused. The refusal
   states the measured count and offers the top of the list instead.
8. A query projected to read more than `2000000` rows is refused before it runs, the projection is
   stated, and nothing partial is cached.
9. Sampling is offered before execution on a large scan and defaults to off. While sampling is
   active every derived number carries an interval, and a sampled count is never displayed as an
   exact whole number.

### Dashboards

1. A dashboard is a saved arrangement of insight tiles over a shared filter, holding at most `40`
   tiles. Tiles are repositioned and resized by dragging and by keyboard, and each keyboard move
   announces the new position.
2. A dashboard-level filter overrides a tile's own filter, and the override is shown on the tile
   that carries it.
3. A tile whose own filter contradicts the dashboard filter renders an explicit conflict marker
   rather than quietly resolving the disagreement in one direction.
4. Tiles load in priority order, the visible ones first, and each tile is cancellable on its own
   without disturbing the others.

### Session replay

1. A recording is one person's session: a first full frame and the changes that followed it.
   `GET /api/projects/{projectSlug}/recordings/{recordingId}` returns its manifest, and
   `GET /api/projects/{projectSlug}/recordings/{recordingId}/frames` returns the ordered frames.
2. Playback begins at the first meaningful frame rather than at zero.
3. Scrubbing the recording scrubs the event list, the console lines, the network entries and the
   flag state together, because all four are bound to one clock rather than to four independent
   subscriptions. Every one of the four shows the state at the playhead and no other.
4. Inactivity, a dropped stretch and the end of capture are three visibly different things on the
   scrubber, and a dropped stretch is never interpolated across. Each scrubber track carries
   `data-track` taking exactly `frames`, `events`, `errors`, `gaps` or `activity`.
5. Masking is applied at capture and never at playback, so the player offers no control that would
   reveal a masked value, because there is nothing held to reveal. The player states which masking
   rules were in force for that recording, so the owner can show a sceptical reader exactly what
   was collected.
6. A recording whose frames are partly expired plays the part it has, draws the missing stretches
   on the scrubber as gaps, and interpolates nothing.

### Feature flags

1. A flag is addressed by a key matching `^[a-z0-9][a-z0-9-]{0,63}$`, unique within its project and
   immutable after creation. Renaming produces a new flag and the interface says so rather than
   appearing to rename.
2. `kind` takes exactly `boolean` or `multivariate`. A multivariate flag holds at most `8` variants
   and their rollout percentages sum to exactly `100`. A variant key is immutable once that variant
   has been evaluated even once.
3. Targeting is built from condition groups. Each level of a group carries exactly one conjunction,
   so `AND` and `OR` never mix at one level. Nesting reaches `3` levels and no deeper, and a rule
   holds at most `24` conditions. The editor renders the effective expression in plain text beneath
   the visual builder, because a targeting rule the owner misreads is a production incident.
4. `POST /api/projects/{projectSlug}/flags/{flagKey}/blast-radius` is computed against current data
   before any rollout change is saved and returns `matchedPersons`, `sharePercent` and
   `windowDays`. A rollout increase of more than `25` percentage points in one edit is refused
   unless the request carries `confirmExposure` naming the projected newly-exposed person count.
5. `POST /api/projects/{projectSlug}/flags/{flagKey}/scheduled-changes` queues a change with the
   moment it applies and the condition that must still hold then. A scheduled change never
   overwrites a concurrent edit the owner made: the owner's edit wins, and the schedule either
   re-evaluates against the new definition or records `skipped_guard` with the reason.
6. `POST /api/projects/{projectSlug}/flags/{flagKey}/kill` sets the flag to its default variant for
   everybody at once, bypasses every scheduled change, records `killedFromState` so the flag can be
   restored, and appends an audit entry naming the actor and the state before the kill. It is
   idempotent: a second kill returns the same terminal state rather than a failure.
7. A flag's `state` takes exactly `draft`, `active`, `scheduled`, `ramping`, `halted`, `killed` or
   `archived`, and `version` increases on every change. A `PATCH` carries `If-Match` holding the
   version it read; a mismatch is refused with `version_mismatch` and the current representation,
   so the caller can merge rather than re-read blind.
8. Evaluation is deterministic: `POST /api/projects/{projectSlug}/flags/evaluate` takes `flagKey`
   and `distinctId` and returns `variantKey` and `reason`, where `reason` takes exactly
   `targeting_match`, `rollout_bucket`, `default`, `killed` or `error_fallback`. The same flag and
   the same person always resolve to the same variant, and the answer is the same whether it is
   read here, from the person timeline or from the experiment's own assignment.
9. `GET /api/projects/{projectSlug}/flags/{flagKey}/evaluations` returns the evaluation log. Above
   its display rate the live stream aggregates rather than falling silent, and the change of mode
   is stated on the surface.

### Experiments

1. An experiment carries a hypothesis, a `primaryMetric`, a list of `guardrailMetrics`, a
   `minimumDetectableEffect`, an `exposureEvent` and an `assignmentSalt` that never changes once
   the experiment exists.
2. Assignment is deterministic from the person key and the salt, so the same person resolves to the
   same variant every time and everywhere the question is asked. Exposure is recorded only when the
   variant was actually shown, never when it was merely assigned.
3. `POST /api/projects/{projectSlug}/experiments/{experimentKey}/power` states `samplePerVariant`,
   `projectedDays` and `projectedPower` from recent arrival rates. Launching below a projected
   power of `0.60` is refused unless the request carries `confirmPower`.
4. `GET /api/projects/{projectSlug}/experiments/{experimentKey}/results` reports a statistic that
   survives being looked at every day, names the `statisticalMethod` in force, and never returns a
   fixed-horizon significance figure. Guardrails are reported in their own group against their own
   tolerances.
5. When exposure events are missing for a variant the results refuse to draw a conclusion and name
   the missing exposure, rather than treating an absence as a zero.
6. `POST /api/projects/{projectSlug}/experiments/{experimentKey}/ship` writes the winning variant
   to `100` and ends the experiment as one operation: both happen or neither does. It accepts an
   `Idempotency-Key`, and a repeat with the same key returns the first answer with the header
   `Idempotency-Replayed: true` rather than shipping twice.
7. A shipped experiment freezes its definition, so the assignment salt, the metric definitions, the
   method and the data window are all readable afterwards and the result can be reproduced.

### Error groups

1. Occurrences group by a fingerprint computed from the shape of the stack.
   `GET /api/projects/{projectSlug}/issues/{issueId}` returns the group with `firstSeenAt`,
   `lastSeenAt`, `occurrenceCount`, `personCount`, the releases and platforms it spans, the
   correlated variant shares and the recordings that contain it.
2. A frame that cannot be resolved back to source renders as the raw frame, is labelled
   unresolved, and names the artefact that is missing, which is the source-map artefact uploaded
   by the release tooling for that release. An unresolved frame is never presented as
   though it were source.
3. A group is split and groups are merged. Both are reversible and both are recorded, and neither
   rewrites historical occurrences: a regrouping creates a new revision and re-projects, so the
   earlier assignment survives.
4. `status` takes exactly `unresolved`, `resolved`, `auto_resolved`, `ignored`, `regressed` or
   `muted`.

### Surveys

1. A survey holds at most `20` ordered questions of exactly five kinds, addressed by the slugs
   `open_text`, `single_choice`, `multiple_choice`, `rating` and `recommendation`.
2. Targeting combines a behavioural cohort with display conditions, a frequency cap and a sampling
   rate, and is previewed against the archive before the survey is published.
3. Open-text answers cluster into themes carrying representative quotes and a size. A theme built
   from fewer than `5` answers is labelled as such and is never shown as a percentage.

### The pipeline

1. Routing data outward is a first-class surface: a destination is a named sink the workbench
   routes the owner's own events to. In this
   environment the workbench serves its own destinations and records every delivery, so delivery,
   failure, the breaker and the replay are all observable without reaching outside.
   `GET /api/projects/{projectSlug}/destinations` lists each with `state`, `deliveryRate`,
   `errorRate`, `breakerState`, `backlogDepth` and `lastSuccessAt`.
2. A transformation is a declared rewrite applied before an event leaves: dropping named
   properties, replacing a named property with a digest of its value, or renaming one.
3. `POST /api/projects/{projectSlug}/destinations/{destinationId}/dry-run` runs the chain against
   up to `100` recent real events and returns the before and the after for each, with the changed
   fields named. A destination is refused activation until at least one dry run has succeeded, and
   the refusal carries `dry_run_required`.
4. Resilience is stated rather than assumed. A destination that keeps failing opens its breaker:
   delivery pauses, the backlog is held and nothing is dropped. Held events are inspectable one at a time with their failure reason and
   their full payload.
5. `POST /api/projects/{projectSlug}/destinations/{destinationId}/replay` re-delivers the held
   events at a rate that keeps replay beneath live traffic, resumes from its own cursor if it is
   interrupted, and never delivers one event twice.
6. A transformation that fails on one malformed event quarantines that event with its reason. It
   never halts the pipeline and it never affects another destination.

### Share links

1. A share link is the only route by which anything in this workspace reaches a second human. It is
   read-only, bounded to one artefact, revocable, and it issues no session.
   `POST /api/projects/{projectSlug}/shares` mints one and returns the token exactly once; the
   workbench stores only a digest of it and can never show it again.
2. The share sheet opens at its most restrictive setting: no underlying events, no person
   identifiers, no drilling down, an expiry of `7` days and the result frozen at the moment it was
   computed. The owner widens from there deliberately, and the sheet states in one sentence what
   the recipient will be able to see.
3. `GET /api/public/shares/{shareToken}` returns the one scoped artefact and the owner's
   attribution and nothing else. A project holds at most `50` shares.
4. Every request outside the token's scope is refused with no signal about whether the thing
   exists. A revoked token, an expired token and a token that never existed are answered
   identically, in the same words and with the same code.
5. `DELETE /api/projects/{projectSlug}/shares/{shareId}` revokes immediately. Each share row
   records how often it was opened and when it was last opened.

### Held mode and pending work

1. The workbench is put into a held state deliberately through
   `PUT /api/workspace/held` carrying `held`. This is how the owner works while deliberately
   disconnected from anything the workbench would otherwise reach.
2. While held, authoring continues. An insight, a dashboard, a cohort, a flag draft and a survey
   draft are all written and recorded as pending work with their order preserved, and
   `GET /api/workspace/pending` returns them.
3. While held, exactly six operations are refused outright rather than queued: publishing a flag,
   killing a flag, shipping an experiment, erasing a person, revoking a share and revoking a key.
   Each refusal carries `workspace_held` and names the held state as the reason. An action that
   appears to have taken effect and has not is worse than one that was refused.
4. `POST /api/workspace/release` applies the pending work in order. Where two edits touched the same
   field one wins by a stated rule, the other is retained, and the owner is told afterwards rather
   than being interrupted at the moment of release. Resolution is never modal.
5. `GET /api/workspace/conflicts` lists each resolution with `winningValue`, `losingValue`,
   `ruleApplied` and `restorableUntil`, and
   `POST /api/workspace/conflicts/{conflictId}/restore` puts the losing value back in one
   interaction. A losing value is restorable for `30` days.

### The processing policy

1. `GET /api/workspace/processing` returns `localOnly` and `disabledCapabilities`, the exact list of
   capabilities the master switch takes away.
2. `PUT /api/workspace/processing` sets it. Before it is enabled the interface states exactly which
   capabilities become unavailable; it never turns them off and lets the owner discover the loss.
3. The two capabilities the switch takes away are named exactly `survey_theme_clustering` and
   `destination_delivery`. With the switch on, a request for either is refused with
   `local_only_processing` naming the switch, and neither degrades quietly into a weaker version
   of itself.

### The operation log and the audit chain

1. Every write appends exactly one operation to the workspace's log. Nothing ever updates an
   operation and nothing ever deletes one.
2. An operation carries its own identifier, a `sequence`, the moment it happened, the actor that
   caused it, the `kind` of change, the type and identifier of what it touched, and the values
   `before` and `after`.
3. Within one workspace `sequence` starts at `1`, increases strictly, is never reused and never
   skipped. Four writes arriving at the same moment take four different sequence numbers, the log
   left behind holds no gap and no repeat, and none of the four writes is lost.
4. Operations group into transactions. A transaction is atomic across every operation inside it:
   either all of them are in the log or none is, and a reader never sees half of one.
5. `GET /api/workspace/operations` returns the log newest first and accepts `since`, returning only
   operations after that sequence.
6. Every audit entry carries the digest of the entry before it.
   `GET /api/workspace/audit/verify` answers `agrees`, and where the chain has been broken it names
   `firstDivergentSequence`. An entry altered directly in storage makes this verification fail,
   which is the whole reason the chain exists.

### Health and cost

1. `GET /api/workspace/health` answers four questions in four groups. **Ingest**: events accepted,
   events refused by reason with every reason enumerated rather than totalled into one number, and
   events dropped against an allowance. **Storage**: counts by store and by content class,
   reconciled against the workbench's own accounting with any disagreement shown rather than
   hidden. **Materialisation**: which ranges of the archive are held close and how much room the
   archive takes. **Cost**: metered usage against allowance per dimension.
2. The metered dimensions are exactly `events`, `recordings`, `flagEvaluations`, `exceptions` and
   `rowsScanned`.
3. A projection states the assumption it projects from, which is the trailing `7` day mean rate, and
   shows a low and a high figure rather than one number.

### Limits, declared rather than discovered

`GET /api/projects/{projectSlug}` carries a `limits` object naming every structural limit and its
value, under the exact keys `eventsPerRequest`, `eventsPerProject`, `projectsPerWorkspace`,
`flagsPerProject`, `variantsPerFlag`, `stepsPerFunnel`, `tilesPerDashboard`, `questionsPerSurvey`,
`conditionsPerRule`, `ruleNestingDepth`, `sharesPerProject`, `rowsPerQuery` and
`breakdownCardinality`. A refusal for a structural limit names the same key and the same value.

### Auth

Sign-in is an address and a password the workbench itself holds. Nothing else exists: an address
under `/api` this brief never names answers as not found, rather than as some capability nobody
wrote down. `POST /api/auth/signup` opens an account together with the empty workspace that account
will own.
`POST /api/auth/login` returns a bearer token. Every other endpoint except `GET /api/health` and
`GET /api/public/shares/{shareToken}` carries `Authorization: Bearer <token>`.
`GET /api/auth/me` returns the signed-in account. `POST /api/auth/step-up` takes the password a
second time and returns a short-lived step-up token. A password is held only as a hash, so the
plaintext is in no table and in no answer. A bearer token runs out; once it has, and whenever none
was sent, the caller reads as signed out, the request is denied, and the workbench writes nothing.

### Refusals

Five kinds of refusal exist and they read as five different things: a refusal because the caller
holds no grant, a refusal because a scoped key lacks the scope, a refusal for a structural limit, a
refusal because the workspace is held, and a refusal for invalid input. Every one names what was
refused and why in the product's own words, and none of them is a generic failure. No refusal
leaves a partial write behind.

Silent degradation is prohibited everywhere. Wherever a surface falls back to a narrower
computation, a cached answer, a coarser resolution or an approximate match, it states that fallback
at the point of use rather than in a log nobody reads.

### Forms refuse invalid input where the owner is standing

Every form in the workbench rejects invalid input inline, beside the field that was wrong, naming
that field and what was wrong with it, and writes nothing while it is doing so. Validation runs when
a field is left or when the form is submitted, never on every keystroke, and correcting the field
clears the refusal.

### A privacy page

`/privacy` states what the workbench stores about the owner, which is their email address, their
display name, the projects they own and every operation they caused, and what it stores about a
data subject, which is their events, their properties, their aliases, their recordings and their
survey answers. Beside each of those it names a retention window. A footer link reaches it from
anywhere in the product, `/login` and `/signup` included, and a visitor with no session reads it in
full.

### Every internal link resolves

An internal link the workbench draws is a link to a page that exists: walk every one of them from
any route and none answers not-found. An address the workbench has never heard of renders its own
not-found page, which offers a way back to the field, and answers as not found rather than
pretending the page worked.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | redirect to the last project's field when signed in, `/login` otherwise | none |
| `/login` | sign in | none |
| `/signup` | create an account and its empty workspace | none |
| `/go` | the command surface as its own address | required |
| `/p/:projectSlug/grain` | the event field | required |
| `/p/:projectSlug/insights` | saved insights | required |
| `/p/:projectSlug/insights/new/step/:stepNumber` | one step of the three-step insight wizard | required |
| `/p/:projectSlug/insights/:insightId` | one insight, its builder and its result | required |
| `/p/:projectSlug/dashboards` | saved dashboards | required |
| `/p/:projectSlug/dashboards/:dashboardId` | one dashboard | required |
| `/p/:projectSlug/replay` | the recordings list | required |
| `/p/:projectSlug/replay/:recordingId` | one recording | required |
| `/p/:projectSlug/flags` | the flags list | required |
| `/p/:projectSlug/flags/:flagKey` | one flag | required |
| `/p/:projectSlug/experiments` | the experiments list | required |
| `/p/:projectSlug/experiments/:experimentKey` | one experiment | required |
| `/p/:projectSlug/issues` | the error groups list | required |
| `/p/:projectSlug/issues/:issueId` | one error group | required |
| `/p/:projectSlug/surveys` | the surveys list | required |
| `/p/:projectSlug/persons/:personId` | one person's correlated timeline | required |
| `/p/:projectSlug/cohorts/:cohortId` | one saved cohort | required |
| `/p/:projectSlug/sql` | the query surface | required |
| `/p/:projectSlug/pipeline` | destinations, transformations and the held backlog | required |
| `/w/settings` | keys, processing, appearance and data | required |
| `/w/health` | ingest, storage, materialisation and cost | required |
| `/w/shares` | every share, its scope, its access record and its revoke control | required |
| `/w/sync` | held mode, pending work and the conflict history | required |
| `/privacy` | what the workbench stores and for how long | none |
| `/s/:shareToken` | the recipient surface, with no application shell | none |

**Entry and redirects.** Asking for a required route with no session sends the visitor to `/login`,
and finishing there returns them to the route they first asked for rather than to a home screen.
Signing out also lands on `/login`, and the token that was in hand stops opening anything. A token
that runs out part-way through an action leaves the account signed out with nothing written behind
it. An owner reaching for a project in a workspace they do not own is told no such project exists,
rather than being shown a surface with everything greyed out. An address the workbench does not
recognise renders the not-found page.

**Journeys.**

1. Sign in as `owner@example.com`, land on the `Ledgerline` field, drag a rectangle across the
   whole archive, and read a cohort of `8` counting up to its final figure beside an event count of
   `2400`. Name it and save it. Reload, open the saved cohort, and read the same two numbers.
2. Zoom out until the field is a density image and zoom back in until it is individual marks. The
   band indicator moves through `epoch`, `season`, `week`, `session` and `moment`, no transition
   leaves the field blank, and the total for the visible span is the same at every band.
3. Drop the three-step funnel `app_opened`, `search_run`, `report_exported` onto the field from the
   command surface. The funnel draws as geometry over the marks and reports `8`, `7` and `5`, with
   `87.50%`, `71.43%` and `62.50%` beside the steps. Click the drop-off between the second and the
   third step and reach the `2` persons who fell out.
4. Open one of those persons, read their correlated timeline, and open the recording on it. Scrub
   the recording and watch the event list, the console, the network entries and the flag state move
   with the playhead. A dropped stretch of the recording is drawn differently from an inactive
   stretch, and the player plays across neither.
5. Open `export-v2`, raise its rollout, and read the blast radius before saving. Raise it by more
   than `25` percentage points and the workbench refuses until the projected exposure is confirmed.
   Then kill the flag, confirm once, and read the audit entry naming the state it was killed from.
6. Open `export-v2-trial`, read the results with the method named beside them, and ship the winner.
   Ship it a second time with the same idempotency key and read the same answer rather than a
   second shipment.
7. Open `/w/sync`, hold the workspace, save a new insight while held and watch it appear as pending
   work, then attempt to kill a flag and read the refusal naming the held state. Release the hold
   and watch the pending work move across, in acknowledgement order, into applied.
8. Sign in as `other@example.com` and ask for `Ledgerline` by its slug and then for one of its
   persons by identifier. Both are answered as though no such thing exists.
9. Mint a share link on an insight at the default scope, open it in a window with no session, and
   read the chart with no rail, no command surface and no way into the workbench. Ask for an
   underlying person through that token and be refused with no hint about whether the person
   exists. Revoke the link and read the same refusal an expired link gives.
10. Open `Quarry`, which has no events, and read the honest empty state naming why the field is
    empty and offering the one action that fixes it.
11. From the footer of any page open `/privacy` and read what the workbench stores about the owner
    and about a data subject.

**States.** Every list has a written empty state offering exactly one action and saying why the
list is empty. Being filtered to nothing is a different state from being empty and names the filter
responsible. Every page has a loading state. Every surface tells four kinds of failure apart:
nothing to reach right now, over the allowance, the scope is missing, and something unexpected with
a correlation reference the owner can quote. Errors never crash the app and never leave a partial
write.

## UI/UX notes

Four design principles govern every surface: data first and chrome last; density is a feature;
colour carries meaning or it is absent; and motion explains causality.

The north star: somebody opening this workbench understands in one look what the archive holds, how
far across it they are looking, and whether what they are reading is live, held or frozen. The
register is operational throughout. This is an instrument a developer reads for an hour at a time,
usually beside the editor they are working in, so data comes first and chrome comes last: any pixel
not showing data or enabling an action on data is a candidate for removal. Density over decoration,
and stability over movement, because the same person opens the same field forty times a day.

Density is a feature rather than a compromise. The default reading is tight, so a long list fits one
screen and the owner scans rather than scrolls, and a roomier setting exists for anybody who wants
it rather than roominess being the default that tightness has to argue against.

The governing constraint on colour is that hue is reserved for encoding data. Event class, variant,
series and state are what a hue means here, so the chrome carries no hue of its own and a
decorative hue anywhere in the chrome is a defect. Ground, panels, raised surfaces, the sunk well
the field sits in, dividers, borders and all three levels of text read as shades of one neutral
family. One accent means interactive and appears nowhere else: the primary action, the focus ring,
the selection edge and a link, and it reads as a blue. Four further colours each carry exactly one
meaning and appear nowhere else: a green for an increase, a success and a resolved group; a red for
a decrease, an error and an unresolved group; an orange for a guardrail breach and an approaching
allowance; and a cyan for a neutral notice. The exact shades are yours, so long as those two rules
hold.

The categorical palette for series, variants and event classes is eight hues ordered for the
greatest perceptual distance between any two, spanning the blue, indigo, red, green, violet,
orange, cyan and magenta families, with a neutral carrying anything the owner has not categorised. Past eight categories the product stops cycling hues and switches to
an ordered lightness ramp with direct labels, because a ninth hue that repeats the first is a lie
about the data. The field's own density mappings are named and switchable and each runs
monotonically from dark to bright so density reads without a legend: a warm ramp on a dark ground,
a cool ramp on a dark ground, and an achromatic ramp for printing and for an owner who would rather
bind hue to event class. Direction is never carried by colour alone: every increase and decrease
carries a glyph and a sign as well as a hue, and the increase and the decrease colours are far
enough apart in lightness to stay distinct to a reader who cannot tell those two hues apart. The
product is committed to a dark ground, with a light theme carrying every role above at the same
contrast.

Typography is two typefaces. One carries the interface: labels, controls, headings and body. One carries numbers,
queries, identifiers and code, and it is where the numeric face earns its place. Every numeric
display sets its figures on lining numerals of equal width, because a column of numbers that shifts
width while it updates is unreadable. The weight axis moves in exactly two places and nowhere else:
on a metric value the moment it crosses a threshold the owner set, and on the field's time ruler as
tick density changes. The scale runs from a hero metric value down through a screen title, a
section heading, body and table cells, a field label and a caption; the sizes are yours, so long as
a heading reads as a title and a table cell reads comfortably at a working distance, and nothing in
the workbench is set larger than the hero metric value.

Spacing, radius and elevation are one system. Corners are barely softened throughout, because this
is an instrument and not a card deck. Elevation is expressed as a paired border and shadow rather
than as a shadow alone, because a shadow is invisible on a dark ground, and four levels are enough:
flush, a row or card, a popover or menu, and a sheet or modal. Every gap is a multiple of one base
unit, which is yours to choose, and no layout rule uses a value outside that scale. Iconography is
one icon set drawn on a consistent grid at two sizes, and an icon is never the sole carrier of
meaning: every icon-only control carries a name, and where an icon conveys a state it is joined by
a word or a shape.

Motion explains causality. Every animation answers either where this came from or what changed, and
one that answers neither is cut. Every animated moment declares how it behaves when something
interrupts it, as an explicit state rather than as whatever a library happens to do: it retargets,
keeping its velocity and heading for the new target; or it reverses along the path it came; or it
commits to its end and lets the next thing start from there; or it abandons the property where it
stands; or it queues, which is only allowed when the wait is short enough not to be felt.

The field itself is the one place this product is allowed to be expressive, and everything else is
quiet. Panning and zooming are physical rather than direct: input sets a target and the camera is
drawn toward it, so a flick carries its momentum and a stop settles rather than snapping, and
beyond the ends of the archive the field resists and returns rather than stopping dead. Zooming
about the pointer keeps the instant under the pointer exactly where it was. Crossing a band
boundary cross-fades one representation into the other and the time ruler's type settles just after
the geometry does. An overlay changing shape morphs from where it currently is rather than
restarting, and waits until the field beneath it has settled so geometry never chases a moving
ground. The brush follows the pointer with no smoothing at all, because a brush that lags its
pointer is unusable, and on release the marks outside the cohort drop back while the marks inside
hold. An event arriving on the live tail blooms briefly where it lands, and above a readable
arrival rate the blooms are sampled and the sampling is stated, because thousands of simultaneous
blooms convey nothing.

Away from the field the movement is short and purposeful. A number changing by more than a small
fraction counts through the intermediate values with its width fixed from the first frame, and a
group of counters in one panel shares one clock and finishes together. A metric crossing a
threshold thickens, takes its meaning colour and settles back a little heavier than it was, so the
lasting signal is the residual weight and the movement was only the notification. A list, a grid or
a set of funnel steps that reorders measures itself before and after and moves each element from
where it actually was, and the element under the pointer holds its exact position while the layout
moves around it. Results resolve from soft to sharp as they arrive, because dense text that only
fades reads as a flicker. A long operation shows a rail driven by real completed units and never by
an estimate; it never moves backward, and it runs to the end before it leaves, because a rail that
vanishes short of the end reads as a failure. A multi-stage operation shows all of its stages
before it begins so its shape is visible in advance, and advancing a stage is not eased, because a
stage advance is an event rather than a duration. A successful save nudges the control that caused
it and draws a confirming mark stroke by stroke. A row acted on before the answer arrives moves
slightly in the direction of the action, and if the write is refused it returns, flashes its
refusal colour and re-enters the list where it was rather than at the end. The playhead is driven
by the recording's own clock and interpolated between samples, and if it drifts too far it snaps
rather than easing, because a playhead that lags what is on screen is worse than one that jumps.
Seeking cross-fades the outgoing frame into the reconstructed one so a seek never flashes empty.
Recorded input events pulse where they happened during playback, which is the whole reason to watch
a recording rather than read the event list. Pivoting between surfaces lifts the originating
element, carries it to where it lands and cross-fades it into place, and cancelling a pivot
reverses it along the same path rather than jumping back. The command surface grows out of the
control that invoked it as one object rather than appearing at full size. A field failing
validation settles with a short shake well below the amplitude associated with discomfort, takes
the refusal colour on its border and opens its message beneath it. Connectivity, capability tier,
allowance and degradation are one indicator that morphs between states rather than several that
swap, and its changes settle before they are shown so a flapping state never produces a flickering
indicator. Pending work reconciling on release is a ladder: each operation crosses from pending to
applied as it is acknowledged, in acknowledgement order rather than list order, and a conflict
diverts to a third column showing both values and naming the rule that decided. Before a project
has data the field renders a slow procedural texture at almost no strength, which is the shape the
surface takes once data exists, shown honestly as empty. Boot reveals in priority order driven by
real readiness rather than by a timer, and any interaction during boot commits every stage at once,
because the owner is never made to wait for a reveal. A placeholder is laid out at the exact
geometry the real content will take and morphs into it without changing size, so nothing shifts;
where the real geometry cannot be predicted no placeholder is shown and a progress rail is used
instead.

Entrances stagger by one small constant interval per sibling and stop staggering after a bounded
number of items rather than sweeping down a long list, and the stagger is counted from position in
the visible window rather than position in the data. Entering elements slow as they arrive and
leaving elements speed up as they go. A thing that becomes another thing morphs; a thing that is
replaced cross-fades. Nothing animates position and size on two different curves at once. The whole
choreography of any single state change is over well inside a second.

Reduced motion is a designed track rather than a switch that turns animation off, and every moment
above has a stated alternative. The camera stops rather than drifting and the field clamps at its
bounds rather than resisting. The cohort dimming stays, because it is how the cohort is legible.
The counter shows its final value at once. The bloom becomes a count at the edge of the viewport,
the input pulse becomes a static marker, and the validation shake is dropped while its colour, its
message and its focus move are kept. The progress rail stays, because it is information rather than
decoration. Everything that remains is a short change of opacity carrying no movement, and every
animation still reaches the state it was going to reach.

Feedback is an inline banner that appears in the surface itself, beside the thing it is about, and
stays until it is dismissed or until another banner takes its place. Nothing that matters is
announced in something that removes itself on a timer, because the owner may be reading the other
half of the screen when it goes.

Each page leads with exactly one primary action, visually distinct from every secondary one: the
field leads with saving the brushed cohort, the flags surface with creating a flag, the pipeline
with adding a destination and the sign-in page with signing in. An image carrying content
carries alternative text with it; an image that is there for the look of the thing says so, so a
reader without sight is never handed a description of a texture.

The accessibility floors below are contract values rather than preferences. Body text and its background hold a contrast ratio of
at least `4.5:1` and large text at least `3:1`, in both themes and at every capability tier. Every
interactive element carries a visible focus ring at a contrast of at least `3:1` against its own
background, and over the field that ring is drawn into the scene as a light ring over a dark ring
so it holds its contrast over any mark colour and any density mapping. Focus is never suppressed.
Touch targets are at least `44` by `44` CSS pixels. Every gesture has a keyboard equivalent: arrows
pan the field, plus and minus zoom it, a modifier with the arrows brushes it, a modifier with the
arrows reorders a list, and the whole playback transport is reachable from the keyboard. An
interaction reachable only by pointer is a defect. The field is exposed to assistive technology two
ways: a live text description that announces the viewport as it settles, naming the span, the event
count and the person count; and a complete table of the same rows the field is drawing, reachable
by one keystroke and by a control in the surface header. That table is not a reduced subset and not
a fallback, it is the fastest way to read exact values, and a field shipped without it is
incomplete. Icon-only controls carry names. Colour is never the sole carrier of meaning and every
chart carries direct labels as well as hue. Nothing flashes more than three times a second, nothing
uses parallax or a full-screen zoom, and no decorative element travels far. Motion preference
resolves in a stated order: an explicit setting in the product first, then the operating system
preference, then full motion.

The workbench renders at three capability tiers and no capability differs between them: only how it
is drawn changes. Everything available at the richest tier is available at the plainest, where the
field becomes a coarse density image built from the same rollups, the brush still selects, the
overlays still render and every interaction returns the same answer. The tier is evaluated as the
workbench runs, a change is announced rather than silent, a reduction applies sooner than a
restoration so the tier does not oscillate, and the owner can pin a tier, which stops automatic
evaluation and says so on the surface.

Responsive behaviour holds at phone, tablet and desktop widths and at every width between them. As
the viewport narrows the rail collapses to icons, then the secondary navigation becomes a dropdown,
then the field's hover inspection becomes tap inspection and its filter bar becomes a bottom sheet.
At phone width the field is read and inspect only: brushing still works, authoring an overlay is
disabled with the reason stated, the deepest band is unavailable and the workbench says so. Nothing
overflows sideways at any width and the page body never scrolls horizontally; the field scrolls
inside its own container in both directions instead.

Failures to design against, stated so a reviewer can point at one. A surface whose whole meaning
arrives as one hue family, leaving a reader who cannot separate two of those hues with nothing else
to read. Ornament occupying room the archive should have had. A landing-page composition wrapped
around a working instrument. A headline sized for an announcement on a screen whose job is two
million marks and a ruler.

## Front-end specification

This section carries the detail that `## UI/UX notes` states in summary. It adds no business rule.

**The shell.** The field is persistent. Contextual surfaces mount beside it, over it, or in place
of it, and none of them tears it down. Insights, flags, issues and the pipeline mount beside it:
the field narrows and keeps the same visible time range rather than the same width, so narrowing
re-derives the scale and never crops time. The command surface, the share sheet, settings and a
person preview mount over it and it keeps drawing behind them. Replay, a dashboard, the query
surface and the recipient surface mount in place of it and it is paused rather than destroyed.
Moving between surfaces carries the active time range and the active cohort with it; a pivot that
resets the time range is a defect.

**The rail.** A narrow fixed rail on the left carries exactly eight destinations in this fixed
order: the field, insights, dashboards, replay, flags, experiments, issues and the pipeline. It
never grows; adding a ninth would mean removing one. Surveys, the query surface, a person, settings
and health are reached from the command surface and from contextual entry points instead. Project
switching is a control in the rail's header rather than a destination of its own, and switching
project keeps the current surface and the current time range and re-resolves against the new
project rather than returning the owner to a home screen.

**The command surface.** It opens over any surface and is also reachable at its own address. It
resolves typed text against every action, saved insight, dashboard, person, event type, flag,
experiment and issue in the workspace, groups the matches by what they are, and moves the selection
with the arrow keys. Every function reachable through the interface is reachable here. Enter goes
to the selected result and Escape closes without going anywhere.

**The field.** A time ribbon runs across the top with ticks whose density follows the visible span.
The canvas fills the stage, carrying the marks, the overlays, the brushed region with its outline
and corner handles, release markers drawn as vertical annotations, and a crosshair with a hover
halo. A dimension axis runs down the left. A hover card appears beside the pointer after a short
hover carrying the event name, the timestamp to the millisecond, the person and the first few
properties. A minimap below the canvas shows the whole archive with the current viewport marked. A
filter bar sits at the bottom carrying the time range picker, the event-type filter, the property
filter, the overlay picker, the tier indicator and the source indicator. The field's root element
carries `data-band` taking exactly `epoch`, `season`, `week`, `session` or `moment`, and
`data-field-state` taking exactly `live`, `brushing`, `cohort-resolved` or `held`.

**Reading the field with a keyboard.** Arrows pan by a fraction of the viewport and with a modifier
by a smaller fraction. Plus and minus zoom about the centre. Tab moves focus between marks in time
order inside the viewport, and past a bounded number of marks it moves by time bucket instead so a
dense viewport does not become an unusable tab order. A modifier with the arrows draws and extends
the brush.

**The insight surface.** A builder on one side and the result on the other above a certain width,
the builder collapsing to a sheet above the result below it, and below phone width the result is
read-only with authoring disabled and the reason stated. The builder carries one row per series
with its event type, its property filters, its aggregation and its breakdown; a step list for a
funnel, reorderable by dragging and by keyboard; a global filter group; a time range picker; and a
sampling control. Beneath the result sits a virtualised table of the same rows. Every result
carries its execution badge, and the element holding a result carries `data-source` taking exactly
`store` or `rollup`.

**The dashboard.** Tiles on a grid, dragged to reposition and resize, with keyboard equivalents
that announce the new position and the new span. A tile carrying a filter the dashboard overrides
says so on the tile. A tile whose own filter contradicts the dashboard filter carries a conflict
marker rather than resolving the disagreement quietly.

**The player.** The reconstruction fills the stage. Beneath it the scrubber carries five tracks,
each marked with `data-track` taking exactly `frames`, `events`, `errors`, `gaps` or `activity`. A
side panel carries tabs for events, console, network, flags and the person, and it becomes a bottom
sheet with the same tabs below a certain width. A transport bar carries play, speed, skip-inactive
and loop. Space plays and pauses, the arrows seek, comma and full stop step one frame, and the
shuttle keys run playback backwards and forwards at speed. Every scrubber track announces the
absolute time at its handle.

**The flag surface.** The targeting editor renders condition groups with their conjunction and
their evaluation order visible, and prints the effective expression in plain text beneath the
builder. The blast radius sits where the rollout is edited, not on another screen. The kill switch
is reachable in one interaction from the flag surface and from an error group. Every lifecycle chip
across the whole product carries `data-state-chip` taking exactly `draft`, `active`, `scheduled`,
`paused`, `failed` or `archived`, and an object with a state of its own maps into that vocabulary
rather than inventing a local treatment.

**The person surface.** One merged timeline carrying events, session boundaries, recordings, error
occurrences, flag evaluations, survey answers and identity merges, virtualised so a long history
scrolls smoothly. Properties show their current value, their previous value, and the moment and
source of the last change. The subject-rights actions live here, behind the step-up.

**The sync surface.** Held mode, the pending work ladder and the conflict history. Each conflict
row shows both values side by side, names the rule that decided, and offers to restore the losing
value in one interaction for as long as the window lasts.

**The recipient surface.** Its own route tree, its own bundle and its own service scope. It does
not load the application shell, the rail, the command surface or the query surface. It renders the
one scoped artefact and the owner's attribution and nothing else, and carries no navigation into
the workbench. Its root carries `data-share-scope` taking exactly `frozen` or `live`. A gesture
that would drill past the scope resists and stops rather than issuing a request. When the token is
refused, the surface holds the last thing it drew as a still image, removes every control and shows
one line of text; it never renders an error page and never distinguishes revoked from expired from
never-existed, in its words or in its answer.

**Machine-readable hooks.** These exact attribute names and values are a contract. `data-band` and
`data-field-state` on the field root. `data-source` on every element holding a result.
`data-rail` on each rail destination, taking exactly `grain`, `insights`, `dashboards`, `replay`,
`flags`, `experiments`, `issues` or `pipeline`. `data-state-chip` on every lifecycle chip.
`data-track` on every scrubber track. `data-share-scope` on the recipient surface root.

**Empty and error presentation, all written.** An empty project reads that no events have been
received on that project and offers the ingest snippet rather than documentation. An empty insight
list, an empty dashboard list, an empty flag list, an empty issue list, a survey with no answers, a
pipeline with no destination, a share list with nothing in it and a log with nothing since a chosen
sequence each carry their own sentence. Being filtered to nothing names the filter responsible and
never reuses the empty wording. A refusal appears beside the thing that was refused, naming what
was refused and why.

**Components and their states.** Every control has a resting, a pointed-at, a pressed, a focused
and an unavailable state, and unavailable is never signalled by colour alone. Escape closes any
popover, sheet or command surface. A destructive action, which is deleting an insight, a dashboard,
a cohort, a flag, a survey, a destination or a share, asks for confirmation first and names what
will be removed. A skeleton morphs into its content and never cross-fades into it.

## Technical requirements

Lit with Vite for the frontend and NestJS for the HTTP API, on Node 20, with PostgreSQL for
storage. The rendering model is a client-rendered single-page application behind a JSON API: a
static shell is served and every surface is drawn in the browser against that API, because the
field, the player and the command surface all need the browser's own drawing surface and none of
them would be produced by rendering the page on the server first. The recipient surface is the one
exception and is served as its own small bundle that does not load the application shell. Both
halves are served from one origin on container-internal port `4173`, bound `0.0.0.0`, with the
HTTP API under the `/api` prefix on that same origin and the ingest endpoint under the `/i` prefix
on it.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing service
available in this environment is `postgres`, and reaching for anything else is a contract
violation.

The archive lives in `postgres`, which is running before the workbench starts. Its address arrives
as `DATABASE_URL`, and the same address arrives a second time as `DB_URL`; read whichever, read both
from the environment, and write neither host nor port nor credential into the source. The workbench's
own address arrives the same way, as `APP_PUBLIC_URL` beside `APP_PUBLIC_PORT`.

Identity is this app's own: an address, a password the app hashes, and a bearer token minted at
sign-in. That token travels on every call except `GET /api/health` and the public read a share token
authorises.

Three API conventions hold everywhere. Every list endpoint answers with the same envelope: an
object carrying `data`, the array of rows, and `page`, an object carrying `nextCursor` and
`hasMore`. Paging is by cursor and never by offset,
`limit` runs from `1` to `200` and defaults to `50`, and a cursor presented against a different
sort order is refused with `cursor_sort_mismatch` rather than quietly re-sorted.

Every refusal answers with one shape: an object under `error` carrying `code`, `message`, an
optional `detail` object and `traceId`. `code` comes from exactly this closed set:
`unauthenticated`, `invalid_credential`, `insufficient_scope`, `forbidden`, `not_found`, `conflict`,
`version_mismatch`, `validation_failed`, `payload_too_large`, `rate_limited`, `quota_exceeded`,
`idempotency_key_reused`, `cursor_sort_mismatch`, `sort_not_indexed`, `project_mismatch`,
`person_erased`, `workspace_held`, `local_only_processing`, `dry_run_required` and `internal`. The
`traceId` is what the interface shows the owner when something unexpected happens, so a report can
be traced to one request. Every enumeration named in this brief is closed: a value outside its set
is refused rather than coerced to a default, because quietly coercing an unknown state is how a
killed flag becomes an active one.

Every response carries `X-RateLimit-Limit`, `X-RateLimit-Remaining` and `X-RateLimit-Reset`, and a
refused-for-rate response also carries `Retry-After`.

Every response carries the standard security headers, including a strict transport policy under
the header name `Strict-Transport-Security` and a nosniff content-type policy under the header
name `X-Content-Type-Options`.

Every public route declares its own title and its own description in the document head, and no two
routes share either.

`GET /api/health` returns `200` once the app is ready.

Nothing the browser fetches on first paint carries a credential: not the HTML, not the CSS, not the
JavaScript, not a payload embedded in any of the three. That covers the ingest key of another project, a personal key's secret, a share
token and the database address.

## Data model

Fourteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a reader can sign in.

**accounts** - identifier, email (unique, compared without case), password hash, display name,
created at. The plaintext password is stored nowhere and returned nowhere.

**workspaces** - identifier, account, name, slug (unique), held, local only, created at. One
workspace per account.

**projects** - identifier, workspace, name, slug (unique within the workspace), ingest key,
retention days, recording retention days, created at.

**persons** - identifier, project, distinct identifier, properties, property sources, first seen at,
last seen at, erased at. The distinct identifier is unique within its project. A non-empty erased at
tombstones the person.

**person_aliases** - identifier, project, person, alias, merged at, merged from person, reversible
until. An alias is unique within its project.

**events** - identifier, project, person, session, type, timestamp, received at, properties,
release, ingest key, dedupe key, clamped. Ordering is by received at. The dedupe key is unique
within its project over the deduplication window.

**rollups** - project, bucket start, bucket width, person, event type, count. One row per bucket, so
a coarse band is read rather than recomputed, and the totals of the finer buckets inside one coarse
bucket equal that bucket's count.

**recordings** - identifier, project, person, session, started at, ended at, duration, frame count,
has gaps, masking policy snapshot, state. The masking policy is snapshotted per recording so the
player can state what was in force at capture.

**recording_frames** - identifier, recording, sequence, kind, payload, offset. The sequence is
unique within its recording, and a frame is either a full frame or a change on top of one.

**flags** - identifier, project, key, name, kind, targeting, rollout percentage, default variant,
state, version, killed at, killed from state. The key is unique within its project and never
changes.

**flag_variants** - identifier, flag, key, name, rollout percentage, payload. The percentages across
one flag's variants total exactly one hundred.

**flag_evaluations** - identifier, project, flag, person, variant key, reason, evaluated at.
Append-only.

**experiments** - identifier, project, flag, key, hypothesis, primary metric, guardrail metrics,
exposure event, assignment salt, minimum detectable effect, statistical method, state, started at,
ended at, frozen definition. The salt never changes once the experiment exists.

**assignments** - identifier, experiment, person, variant key, assigned at. One row per experiment
and person.

**exposures** - identifier, experiment, person, variant key, exposed at. Written only when the
variant was shown.

**issues** - identifier, project, fingerprint, grouping revision, title, culprit, first seen at,
last seen at, occurrence count, person count, status, merged into. The fingerprint is unique within
its project for a grouping revision.

**occurrences** - identifier, issue, project, person, event, release, raw stack, resolved stack,
resolution state, occurred at.

**insights** - identifier, project, name, kind, definition, time range, last computed at, last
computed rows, version.

**dashboards** - identifier, project, name, filters, and its tiles, each carrying its insight, its
position, its span and its filter override.

**cohorts** - identifier, project, name, kind, definition, member count, computed at.

**surveys** - identifier, project, name, questions, targeting, sampling rate, state, and its
answers, each carrying its person, its answers and whether it was partial.

**destinations** - identifier, project, name, state, breaker state, consecutive failures, backlog
depth, last success at, and its transformations, each carrying its sequence, its rewrite and
whether a dry run has passed.

**deliveries** - identifier, destination, event, attempt, state, failure reason, delivered at. One
row per destination and event.

**shares** - identifier, project, token digest, resource type, resource, scope, expires at, access
count, last accessed at, revoked at. The raw token is never stored.

**keys** - identifier, workspace, kind, prefix, secret digest, scopes, last used at, revoked at. The
secret is shown once at creation and never again.

**operations** - identifier, workspace, sequence, occurred at, actor, kind, target type, target
identifier, before, after, transaction, previous digest, own digest.

**pending_operations** - identifier, workspace, local sequence, entity type, entity identifier,
kind, payload, applied at.

**conflicts** - identifier, workspace, entity type, entity identifier, field, winning value, losing
value, rule applied, detected at, restorable until, restored at.

**erasures** - identifier, project, person, legal basis, requested at, state, stores completed,
stores unreachable, certificate, completed at.

**Invariants, stated as properties of the running system.**

Operation sequence numbers are unique within their workspace. Four writes to one workspace arriving
at the same moment produce four operations carrying four different sequence numbers; exactly one
sequence value is issued to each, the log holds no gap and no repeat, and none of the four writes is
lost. An operation row, once written, is never changed and never removed, and each one carries the
digest of the one before it so the chain can be verified from the first entry to the last.

A rollup bucket's count equals the number of event rows inside that bucket, so a total read from
rollups equals the same total read from events for the same span and the same filter.

A cohort resolution's cardinality equals the number of distinct persons among the event rows in the
brushed region.

An event admitted twice under one dedupe key inside the deduplication window leaves exactly one
event row.

A person tombstoned by an erasure leaves no event row, no recording, no survey answer, no flag
evaluation and no rollup contribution naming that person, and an event arriving afterwards for that
person's distinct identifier creates no new person row.

A refusal leaves nothing behind: no event, no row, no recomputed rollup and no appended operation.

**Seed data.** Two accounts: `owner@example.com` as Marisol Vega and `other@example.com` as Anders
Roeg.

Two workspaces. `Northlight Labs`, slug `northlight-labs`, owned by Marisol Vega.
`Coldwater Games`, slug `coldwater-games`, owned by Anders Roeg.

`Northlight Labs` holds two projects. `Ledgerline`, slug `ledgerline`, carries the seeded archive.
`Quarry`, slug `quarry`, carries no events at all, so the honest empty state is visible without
anything being fabricated. `Coldwater Games` holds one project, `Stonefall`, slug `stonefall`, with
its own small archive that nothing in `Northlight Labs` can reach.

The `Ledgerline` archive holds `2400` events across `8` persons over the `180` days ending at the
moment the app first starts. The eight persons carry the distinct identifiers `anna-reyes`,
`bo-lindqvist`, `cai-oyelaran`, `dara-whitlock`, `emil-sandoval`, `fern-adeyemi`, `gus-marchetti`
and `hana-vestergaard`. There are exactly six event types, and their counts and distinct-person
counts are these:

| Event type | Events | Distinct persons |
|---|---|---|
| `app_opened` | `960` | `8` |
| `search_run` | `612` | `7` |
| `export_panel_seen` | `384` | `6` |
| `report_exported` | `312` | `5` |
| `invite_sent` | `108` | `4` |
| `plan_upgraded` | `24` | `3` |

Three releases are tagged: `1.4.0`, `1.5.0` and `1.6.0`.

Two flags. `fast-search` is `boolean`. `export-v2` is `multivariate` with the variants `control` at
`55`, `compact` at `30` and `wide` at `15`, and `control` is its default variant.

One experiment, `export-v2-trial`, runs on `export-v2` with the primary metric `report_exported`,
the guardrail metric `error_rate`, the exposure event `export_panel_seen` and the assignment salt
`northlight-export-2026`.

Two error groups. `TypeError: cannot read length of undefined` has `24` occurrences across `5`
persons on releases `1.5.0` and `1.6.0`, and its frames resolve back to source.
`Timeout while exporting report` has `9` occurrences across `3` persons on release `1.6.0` only,
and it has no artefact to resolve against, so its frames render unresolved and named.

Three recordings, one each for `anna-reyes`, `dara-whitlock` and `gus-marchetti`. The recording for
`anna-reyes` carries both an inactive stretch and a dropped stretch, so the two are visibly
different on the scrubber on first load.

One survey, `why-export`, with three questions and `18` answers.

Two destinations. `warehouse-sink` carries a transformation that drops `ip` and `user_agent` and
replaces `email` with a digest, and it sits with its breaker open holding a backlog of `41` events
after five consecutive failures, so the held backlog and the replay are both visible on first load.
`metrics-mirror` is delivering normally.

One saved insight, `Weekly exports`, a `trend` of `report_exported` broken down by release. One
dashboard, `Ledgerline weekly`, holding three tiles. One saved cohort, `Exported this season`. The
share list starts empty.

The operation log for `Northlight Labs` already carries the operations that created all of the
above, starting at sequence `1`, so the log, the audit verification and a person's history all
return something on first load.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Constraints

- One workbench, two seeded workspaces, one owner each. An owner reaches only their own workspace.
- No organisation, no second member, no seat, no invitation and no delegated administration.
- No file upload, no attachment and no object store.
- No email, no notification and no mail vendor.
- No payment, no plan purchase, no billing and no subscription.
- No federated sign-in, no directory provisioning, no domain capture and no enterprise
  administration panel.
- No legal hold, no discovery export, no customer-managed key and no residency guarantee.
- No managed warehouse, no external table hosting and no transformation project.
- No third-party application marketplace and no revenue-shared plugin.
- No advertising cost ingestion, no bid management and no probabilistic cross-device identity
  graph.
- No realtime push between people and no presence, because there is only one person.
- No artificial intelligence feature and no native application.
- No external network call at run time.
- The workbench must stay responsive with `2000000` events in a project.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
  The app root is `/app`, so the two reserved directories are `/app/.browser_screenshots` and
  `/app/.downloads`.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `displayName` | the created account and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token |
| `GET /api/auth/me` | none | the signed-in account |
| `POST /api/auth/step-up` | `password` | a short-lived step-up token |
| `GET /api/health` | none | a body stating the app is ready |
| `GET /api/projects` | `limit`, `cursor` | the paged projects of the caller's workspace |
| `GET /api/projects/{projectSlug}` | none | the project with its ingest key and its `limits` |
| `GET /api/projects/{projectSlug}/field` | `from`, `to`, `band`, `dim`, `types` | the marks plus `total`, `persons` and `band` |
| `GET /api/projects/{projectSlug}/events` | `from`, `to`, `types`, `limit`, `cursor` | the paged raw events |
| `POST /api/projects/{projectSlug}/cohorts/resolve` | `from`, `to`, `dimFrom`, `dimTo`, `types` | `cardinality`, `eventCount`, `personIds` |
| `POST /api/projects/{projectSlug}/cohorts` | `name`, `definition` | the saved cohort |
| `POST /api/projects/{projectSlug}/query` | a typed query object | the result and its `execution` |
| `POST /api/projects/{projectSlug}/insights` | `name`, `kind`, `definition`, `timeRange` | the saved insight |
| `GET /api/projects/{projectSlug}/insights/{insightId}/result` | none | the result and its `execution` |
| `GET /api/projects/{projectSlug}/persons/{personId}` | none | the person and the correlated timeline |
| `POST /api/projects/{projectSlug}/persons/resolve` | `identifier` | the person the alias graph resolves to |
| `POST /api/projects/{projectSlug}/persons/{personId}/access-package` | none, step-up required | the package and `aliasCount` |
| `POST /api/projects/{projectSlug}/persons/{personId}/erase` | `legalBasis`, step-up required | the erasure record |
| `GET /api/projects/{projectSlug}/erasures/{erasureId}` | none | the completion certificate |
| `GET /api/projects/{projectSlug}/flags` | `limit`, `cursor` | the paged flags |
| `PATCH /api/projects/{projectSlug}/flags/{flagKey}` | the change, `If-Match` | the updated flag |
| `POST /api/projects/{projectSlug}/flags/{flagKey}/blast-radius` | the proposed change | `matchedPersons`, `sharePercent`, `windowDays` |
| `POST /api/projects/{projectSlug}/flags/{flagKey}/kill` | none | the killed flag and `killedFromState` |
| `POST /api/projects/{projectSlug}/flags/evaluate` | `flagKey`, `distinctId` | `variantKey` and `reason` |
| `GET /api/projects/{projectSlug}/experiments/{experimentKey}/results` | none | the per-variant results and `statisticalMethod` |
| `POST /api/projects/{projectSlug}/experiments/{experimentKey}/ship` | `variantKey`, `Idempotency-Key` | the shipped experiment |
| `GET /api/projects/{projectSlug}/issues/{issueId}` | none | the error group and its resolution state |
| `GET /api/projects/{projectSlug}/recordings/{recordingId}` | none | the recording manifest |
| `POST /api/projects/{projectSlug}/destinations/{destinationId}/dry-run` | none | before and after for recent events |
| `POST /api/projects/{projectSlug}/destinations/{destinationId}/replay` | none | the replay summary |
| `POST /api/projects/{projectSlug}/shares` | `resourceType`, `resourceId`, `scope`, `expiresInDays` | the share and its token, once |
| `GET /api/public/shares/{shareToken}` | none | the one scoped artefact |
| `PUT /api/workspace/held` | `held` | the workspace held state |
| `GET /api/workspace/pending` | none | the pending operations in order |
| `POST /api/workspace/release` | none | the applied operations and any conflicts |
| `GET /api/workspace/conflicts` | none | each resolution with both values |
| `GET /api/workspace/processing` | none | `localOnly` and `disabledCapabilities` |
| `GET /api/workspace/operations` | `since`, `limit`, `cursor` | the paged log, newest first |
| `GET /api/workspace/audit/verify` | none | `agrees` and `firstDivergentSequence` |
| `GET /api/workspace/health` | none | ingest, storage, materialisation and cost |
| `POST /i/v1/events` | a JSON array, `X-Ingest-Key` | `accepted` and `rejected` by index and code |

**Response shapes.** These field names are exact.

- A project carries `id`, `name`, `slug`, `ingestKey` and `limits`.
- A field answer carries `band`, `total`, `persons` and `marks`.
- A cohort resolution carries `cardinality`, `eventCount` and `personIds`.
- A result carries `rows` and `execution`, and `execution` carries `source`, `rowsScanned`,
  `durationMs`, `sampled` and `samplingRate`.
- An event carries `id`, `type`, `personId`, `timestamp`, `receivedAt`, `properties` and `clamped`.
- A person carries `id`, `distinctId`, `properties`, `aliases` and `timeline`.
- A flag carries `id`, `key`, `kind`, `targeting`, `rolloutPercentage`, `defaultVariantKey`,
  `variants`, `state` and `version`.
- An evaluation carries `variantKey` and `reason`.
- An experiment result carries `variants`, `guardrails` and `statisticalMethod`.
- An issue carries `id`, `title`, `culprit`, `firstSeenAt`, `lastSeenAt`, `occurrenceCount`,
  `personCount`, `status` and `frames`, and a frame carries `resolved` and `missingArtefact`.
- An operation carries `id`, `sequence`, `occurredAt`, `actor`, `kind`, `targetType`, `targetId`,
  `before` and `after`.
- The audit answer carries `agrees` and, when the chain has parted, `firstDivergentSequence`.
- A conflict carries `id`, `field`, `winningValue`, `losingValue`, `ruleApplied` and
  `restorableUntil`.
- An erasure certificate carries `storesCompleted`, `storesUnreachable` and `residualWindowDays`.
- An ingest answer carries `accepted` and `rejected`, and each rejection carries `index` and
  `code`.
- A refusal carries `error`, an object holding `code`, `message`, an optional `detail` and
  `traceId`.

A successful call returns the named resource or shape. An invalid or unauthorized call is rejected
as a client error, never as a server error and never as a silent success. Bearer auth is carried on
everything except `POST /api/auth/signup`, `POST /api/auth/login`, `GET /api/health`,
`GET /api/public/shares/{shareToken}` and `POST /i/v1/events`, which carries its own ingest key.

**No mocks.** `postgres` is the fact. An in-memory array of events, a JSON file on the app's own
disk, a SQLite file beside the app, a hardcoded answer the app returns to itself, or an operation
log kept only in the running process are each a contract violation however good the interface
looks. The named provider is the fact - the app's interface and its own tables can only reflect
what lives in the provider, never substitute for it.

## Definition of done

Somebody signs in, opens the seeded project, brushes a region of the field and reads a cohort size
that equals the number of distinct persons in the raw events underneath it, saves that cohort and
finds it again after a reload. The same span reports the same total at every band. A funnel over the
whole archive reports the three step counts and the three conversions the brief pins. The owner of
the other workspace is answered as though the project does not exist. A write refused while the
workspace is held leaves nothing behind and names the held state, and the operation log and its
audit chain both verify from the first entry to the last.
