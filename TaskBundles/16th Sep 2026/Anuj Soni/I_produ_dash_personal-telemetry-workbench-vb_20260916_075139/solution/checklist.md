# Checklist: Personal Telemetry Workbench

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Items: 433
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` One developer owns one workspace of projects. `src: Overview para 1`
- [ ] `C-OV-02` `capability` Every analytical question is answered out of the workbench's own store. `src: Overview para 1`
- [ ] `C-OV-03` `capability` A project holds events, recordings, flag evaluations, error occurrences, survey answers. `src: Overview para 1`
- [ ] `C-OV-04` `capability` All six kinds of record resolve to one person identity. `src: Overview para 1`
- [ ] `C-OV-05` `capability` All six kinds of record resolve to one clock. `src: Overview para 1`
- [ ] `C-OV-06` `capability` A data subject never signs in to the workbench. `src: Overview para 2`
- [ ] `C-OV-07` `capability` The event field draws one mark per event. `src: Overview para 3`
- [ ] `C-OV-08` `capability` The event field binds its vertical axis to a chosen dimension. `src: Overview para 3`
- [ ] `C-OV-09` `constraint` Every row in every table belongs to exactly one workspace. `src: Overview para 4`
- [ ] `C-OV-10` `capability` Every number the workbench shows agrees with the raw events beneath. `src: Overview para 6`

## C-RL User roles

- [ ] `C-RL-01` `role` An owner reads every project in the workspace that account owns. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An owner writes insights, dashboards, cohorts, flags, experiments, surveys. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An owner reads the operation log of the workspace that account owns. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An owner is denied reaching a workspace that account does not own. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A scoped key acts only within the scope set the key names. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A scoped key is denied erasing a person. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A scoped key is denied generating an access package. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A scoped key is denied creating another key. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A share token reads the one artefact the scope of that token names. `src: User roles table row 3`
- [ ] `C-RL-10` `role` A share token is denied reaching any other artefact. `src: User roles table row 3`
- [ ] `C-RL-11` `contract` The server enforces authorization on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-12` `contract` A refusal for a missing scope names the scope that was missing. `src: User roles para 4`
- [ ] `C-RL-13` `contract` Erasing a person needs a session that re-confirmed the password. `src: User roles para 4`
- [ ] `C-RL-14` `contract` Generating an access package needs a session that re-confirmed the password. `src: User roles para 4`
- [ ] `C-RL-15` `contract` Signup creates a new account with a new empty workspace. `src: User roles para 5`
- [ ] `C-RL-16` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles para 5`
- [ ] `C-RL-17` `literal` The seeded owner account is `owner@example.com`. `src: User roles para 5`
- [ ] `C-RL-18` `literal` The second seeded account is `other@example.com`. `src: User roles para 5`

## C-CF Core features

- [ ] `C-CF-01` `data` A span total is identical at every band for one filter. `src: Core features reconciliation rule 1`
- [ ] `C-CF-02` `contract` The field endpoint accepts a from bound, a to bound, a band, a dimension. `src: Core features reconciliation rule 1`
- [ ] `C-CF-03` `data` The field answer carries a total of the events in the span. `src: Core features reconciliation rule 1`
- [ ] `C-CF-04` `data` The field answer carries a count of distinct persons in the span. `src: Core features reconciliation rule 1`
- [ ] `C-CF-05` `data` A cohort cardinality equals the distinct persons in the brushed region. `src: Core features reconciliation rule 2`
- [ ] `C-CF-06` `data` A cohort cardinality equals the length of the returned person list. `src: Core features reconciliation rule 2`
- [ ] `C-CF-07` `data` The returned person list equals the distinct persons in the raw events. `src: Core features reconciliation rule 2`
- [ ] `C-CF-08` `contract` The cohort resolve endpoint accepts a time span, a dimension range, a type filter. `src: Core features reconciliation rule 2`
- [ ] `C-CF-09` `data` A funnel step count equals the persons the raw events place at that step. `src: Core features reconciliation rule 3`
- [ ] `C-CF-10` `data` A funnel is ordered so a person counts at a step only after the previous step. `src: Core features reconciliation rule 3`
- [ ] `C-CF-11` `data` Resolving one region twice returns identical numbers. `src: Core features reconciliation rule 4`
- [ ] `C-CF-12` `literal` The seeded archive holds `2400` events. `src: Core features reconciliation rule 5`
- [ ] `C-CF-13` `literal` The seeded archive holds `8` persons. `src: Core features reconciliation rule 5`
- [ ] `C-CF-14` `data` Brushing the whole seeded archive resolves a cohort of eight persons. `src: Core features reconciliation rule 5`
- [ ] `C-CF-15` `data` The seeded three-step funnel reports eight, seven, five persons. `src: Core features reconciliation rule 5`
- [ ] `C-CF-16` `literal` The seeded funnel second step converts at `87.50%`. `src: Core features reconciliation rule 5`
- [ ] `C-CF-17` `literal` The seeded funnel third step converts at `71.43%`. `src: Core features reconciliation rule 5`
- [ ] `C-CF-18` `literal` The seeded funnel converts end to end at `62.50%`. `src: Core features reconciliation rule 5`
- [ ] `C-CF-19` `data` A percentage keeps the decimal places that carry a decision boundary. `src: Core features reconciliation rule 6`
- [ ] `C-CF-20` `ui` An abbreviated count exposes the exact value on hover. `src: Core features reconciliation rule 6`
- [ ] `C-CF-21` `contract` The bound dimension accepts exactly person, session, release. `src: Core features grain rule 1`
- [ ] `C-CF-22` `contract` The bound dimension defaults to person ordered by first-seen. `src: Core features grain rule 1`
- [ ] `C-CF-23` `contract` A band is addressed by the slug epoch, season, week, session, moment. `src: Core features grain rule 2`
- [ ] `C-CF-24` `ui` The epoch band draws a density cell per person per day. `src: Core features grain rule 2`
- [ ] `C-CF-25` `ui` The season band draws banded density with a hue per event type. `src: Core features grain rule 2`
- [ ] `C-CF-26` `ui` The week band groups nearby events into one mark. `src: Core features grain rule 2`
- [ ] `C-CF-27` `ui` The session band draws one mark per event with person lanes resolved. `src: Core features grain rule 2`
- [ ] `C-CF-28` `ui` The moment band draws property labels beside each mark. `src: Core features grain rule 2`
- [ ] `C-CF-29` `ui` Crossing a band boundary cross-fades the two representations. `src: Core features grain rule 3`
- [ ] `C-CF-30` `ui` A viewport nudged back across a boundary stays on one representation. `src: Core features grain rule 3`
- [ ] `C-CF-31` `ui` A band transition never shows an empty field. `src: Core features grain rule 3`
- [ ] `C-CF-32` `ui` Zoom runs continuously from the whole archive to a single millisecond. `src: Core features grain rule 4`
- [ ] `C-CF-33` `ui` One wheel notch changes the visible span by one proportion at every scale. `src: Core features grain rule 4`
- [ ] `C-CF-34` `ui` The time axis under the pointer holds still during a zoom. `src: Core features grain rule 4`
- [ ] `C-CF-35` `ui` An overlay draws into the field under the same view as the marks. `src: Core features grain rule 5`
- [ ] `C-CF-36` `ui` An overlay stays registered against the events beneath at every zoom. `src: Core features grain rule 5`
- [ ] `C-CF-37` `ui` A brush in progress shows an approximate size labelled approximate. `src: Core features grain rule 6`
- [ ] `C-CF-38` `ui` Releasing a brush dims the marks outside the resolved cohort. `src: Core features grain rule 6`
- [ ] `C-CF-39` `capability` A resolved cohort is saved by name. `src: Core features grain rule 7`
- [ ] `C-CF-40` `data` A saved cohort states whether the membership recomputes. `src: Core features grain rule 7`
- [ ] `C-CF-41` `data` A saved cohort states when the membership was last computed. `src: Core features grain rule 7`
- [ ] `C-CF-42` `contract` The field address carries the time bounds of the viewport. `src: Core features grain rule 8`
- [ ] `C-CF-43` `contract` The field address carries the bound dimension, the overlays, the filter. `src: Core features grain rule 8`
- [ ] `C-CF-44` `ui` One history entry is committed once viewport movement settles. `src: Core features grain rule 8`
- [ ] `C-CF-45` `contract` An unrecognised address answers as not found. `src: Core features grain rule 9`
- [ ] `C-CF-46` `ui` The not-found page renders inside the shell with the rail intact. `src: Core features grain rule 9`
- [ ] `C-CF-47` `ui` A project with no events renders the shape the field will take. `src: Core features grain rule 10`
- [ ] `C-CF-48` `constraint` No fabricated event is ever shown on an empty project. `src: Core features grain rule 10`
- [ ] `C-CF-49` `contract` The ingest endpoint accepts a batch keyed by an ingest key header. `src: Core features ingest rule 1`
- [ ] `C-CF-50` `literal` An ingest batch holds at most `500` events. `src: Core features ingest rule 1`
- [ ] `C-CF-51` `contract` An ingest entry carries a type, a distinct identifier, a timestamp. `src: Core features ingest rule 1`
- [ ] `C-CF-52` `data` The ingest answer names the number of accepted events. `src: Core features ingest rule 2`
- [ ] `C-CF-53` `data` The ingest answer names each rejection by index. `src: Core features ingest rule 2`
- [ ] `C-CF-54` `data` The ingest answer names each rejection by code. `src: Core features ingest rule 2`
- [ ] `C-CF-55` `data` A malformed entry never discards a valid entry beside the malformed one. `src: Core features ingest rule 2`
- [ ] `C-CF-56` `data` Two entries under one dedupe key inside the window leave one event. `src: Core features ingest rule 4`
- [ ] `C-CF-57` `literal` The deduplication window is the trailing `24` hours. `src: Core features ingest rule 4`
- [ ] `C-CF-58` `data` A timestamp far in the future is clamped to the moment of receipt. `src: Core features ingest rule 5`
- [ ] `C-CF-59` `data` A clamped event is flagged as clamped. `src: Core features ingest rule 5`
- [ ] `C-CF-60` `data` A live timestamp more than five years old is refused. `src: Core features ingest rule 5`
- [ ] `C-CF-61` `contract` An ingest key naming another project is refused as a project mismatch. `src: Core features ingest rule 6`
- [ ] `C-CF-62` `contract` An event for an erased person is refused as a person erasure. `src: Core features ingest rule 7`
- [ ] `C-CF-63` `data` The person endpoint returns the correlated timeline newest first. `src: Core features persons rule 1`
- [ ] `C-CF-64` `data` The correlated timeline merges events, recordings, errors, evaluations, answers. `src: Core features persons rule 1`
- [ ] `C-CF-65` `contract` The resolve endpoint returns the person an alias resolves to. `src: Core features persons rule 2`
- [ ] `C-CF-66` `data` A person property carries the previous value beside the current value. `src: Core features persons rule 3`
- [ ] `C-CF-67` `data` A person property carries the moment of the last change. `src: Core features persons rule 3`
- [ ] `C-CF-68` `data` A person property written by several sources lists every source. `src: Core features persons rule 3`
- [ ] `C-CF-69` `data` An identity merge is recorded with the alias that caused the merge. `src: Core features persons rule 4`
- [ ] `C-CF-70` `literal` An identity merge is reversible for `30` days. `src: Core features persons rule 4`
- [ ] `C-CF-71` `capability` An access package gathers every record held about one person. `src: Core features persons rule 5`
- [ ] `C-CF-72` `data` An access package states how many aliases were found. `src: Core features persons rule 5`
- [ ] `C-CF-73` `capability` An access package is downloadable once through a link that expires. `src: Core features persons rule 5`
- [ ] `C-CF-74` `data` An erasure records the basis before any data is touched. `src: Core features persons rule 6`
- [ ] `C-CF-75` `data` An erasure propagates through the archive, the recordings, the rollups. `src: Core features persons rule 6`
- [ ] `C-CF-76` `data` A certificate names every store the erasure reached. `src: Core features persons rule 7`
- [ ] `C-CF-77` `data` A certificate names every store the erasure could not reach. `src: Core features persons rule 7`
- [ ] `C-CF-78` `data` A certificate names the residual window in days. `src: Core features persons rule 7`
- [ ] `C-CF-79` `contract` An insight is addressed by the kind trend, funnel, retention, path, distribution. `src: Core features insights rule 1`
- [ ] `C-CF-80` `ui` Creating an insight runs a three-step wizard with an address per step. `src: Core features insights rule 2`
- [ ] `C-CF-81` `ui` Moving between wizard steps preserves everything already entered. `src: Core features insights rule 2`
- [ ] `C-CF-82` `ui` The save control of the insight wizard exists only on the third step. `src: Core features insights rule 2`
- [ ] `C-CF-83` `data` A result carries an execution object naming where the answer was computed. `src: Core features insights rule 4`
- [ ] `C-CF-84` `data` An execution object names the rows scanned, the duration, the sampling. `src: Core features insights rule 4`
- [ ] `C-CF-85` `ui` The provenance of a result appears beside every number drawn. `src: Core features insights rule 4`
- [ ] `C-CF-86` `data` A relative time range re-evaluates whenever the insight is opened. `src: Core features insights rule 5`
- [ ] `C-CF-87` `ui` The interface shows whether a saved range is relative or frozen. `src: Core features insights rule 5`
- [ ] `C-CF-88` `literal` A funnel holds at most `20` steps. `src: Core features insights rule 6`
- [ ] `C-CF-89` `ui` Funnel steps are reordered by dragging. `src: Core features insights rule 6`
- [ ] `C-CF-90` `data` Reordering a funnel step cancels an analysis still running. `src: Core features insights rule 6`
- [ ] `C-CF-91` `literal` A breakdown is refused above `10000` distinct values. `src: Core features insights rule 7`
- [ ] `C-CF-92` `data` A refused breakdown states the measured count of distinct values. `src: Core features insights rule 7`
- [ ] `C-CF-93` `literal` A query is refused above `2000000` projected rows. `src: Core features insights rule 8`
- [ ] `C-CF-94` `data` A refused query caches nothing partial. `src: Core features insights rule 8`
- [ ] `C-CF-95` `data` A sampled count is never displayed as an exact whole number. `src: Core features insights rule 9`
- [ ] `C-CF-96` `literal` A dashboard holds at most `40` tiles. `src: Core features dashboards rule 1`
- [ ] `C-CF-97` `ui` A dashboard tile is repositioned by dragging. `src: Core features dashboards rule 1`
- [ ] `C-CF-98` `ui` A keyboard move of a tile announces the new position. `src: Core features dashboards rule 1`
- [ ] `C-CF-99` `ui` A tile whose filter the dashboard overrides says so on the tile. `src: Core features dashboards rule 2`
- [ ] `C-CF-100` `ui` A tile filter contradicting the dashboard filter shows a conflict marker. `src: Core features dashboards rule 3`
- [ ] `C-CF-101` `ui` Dashboard tiles load with the visible tiles first. `src: Core features dashboards rule 4`
- [ ] `C-CF-102` `ui` A dashboard tile is cancellable without disturbing the other tiles. `src: Core features dashboards rule 4`
- [ ] `C-CF-103` `contract` The recording endpoint returns a manifest for one session. `src: Core features replay rule 1`
- [ ] `C-CF-104` `data` The frames endpoint returns the ordered frames of one recording. `src: Core features replay rule 1`
- [ ] `C-CF-105` `ui` Playback begins at the first meaningful frame. `src: Core features replay rule 2`
- [ ] `C-CF-106` `ui` Scrubbing moves the event list, the console, the network entries, the flag state. `src: Core features replay rule 3`
- [ ] `C-CF-107` `ui` Every panel bound to the playhead shows the state at the playhead. `src: Core features replay rule 3`
- [ ] `C-CF-108` `ui` Inactivity, a dropped stretch, the end of capture are three different treatments. `src: Core features replay rule 4`
- [ ] `C-CF-109` `contract` A scrubber track is marked frames, events, errors, gaps, activity. `src: Core features replay rule 4`
- [ ] `C-CF-110` `ui` The player offers no control that would reveal a masked value. `src: Core features replay rule 5`
- [ ] `C-CF-111` `data` The player states which masking rules were in force at capture. `src: Core features replay rule 5`
- [ ] `C-CF-112` `contract` A flag key matches the pinned pattern of lowercase characters. `src: Core features flags rule 1`
- [ ] `C-CF-113` `contract` A flag key never changes after creation. `src: Core features flags rule 1`
- [ ] `C-CF-114` `contract` A flag kind is exactly boolean or multivariate. `src: Core features flags rule 2`
- [ ] `C-CF-115` `literal` A multivariate flag holds at most `8` variants. `src: Core features flags rule 2`
- [ ] `C-CF-116` `data` Variant rollout percentages sum to exactly one hundred. `src: Core features flags rule 2`
- [ ] `C-CF-117` `contract` A variant key never changes after the first evaluation of that variant. `src: Core features flags rule 2`
- [ ] `C-CF-118` `data` Each level of a targeting group carries exactly one conjunction. `src: Core features flags rule 3`
- [ ] `C-CF-119` `literal` Targeting nesting reaches `3` levels. `src: Core features flags rule 3`
- [ ] `C-CF-120` `literal` A targeting rule holds at most `24` conditions. `src: Core features flags rule 3`
- [ ] `C-CF-121` `ui` The targeting editor prints the effective expression in plain text. `src: Core features flags rule 3`
- [ ] `C-CF-122` `data` A blast radius answer names the matched persons, the share, the window. `src: Core features flags rule 4`
- [ ] `C-CF-123` `literal` A rollout increase beyond `25` in one edit needs a confirmation. `src: Core features flags rule 4`
- [ ] `C-CF-124` `data` A scheduled change carries the moment of application, the guard condition. `src: Core features flags rule 5`
- [ ] `C-CF-125` `data` A manual edit beats a scheduled change that collides with the edit. `src: Core features flags rule 5`
- [ ] `C-CF-126` `data` A skipped schedule records the reason for skipping. `src: Core features flags rule 5`
- [ ] `C-CF-127` `capability` A kill sets the flag to the default variant for everybody at once. `src: Core features flags rule 6`
- [ ] `C-CF-128` `data` A kill records the state the flag was killed from. `src: Core features flags rule 6`
- [ ] `C-CF-129` `data` A kill appends an audit entry naming the actor. `src: Core features flags rule 6`
- [ ] `C-CF-130` `data` A second kill returns the same terminal state. `src: Core features flags rule 6`
- [ ] `C-CF-131` `contract` A flag state is exactly one of the seven pinned words. `src: Core features flags rule 7`
- [ ] `C-CF-132` `data` A flag version increases on every change. `src: Core features flags rule 7`
- [ ] `C-CF-133` `contract` A change naming a stale version is refused as a version mismatch. `src: Core features flags rule 7`
- [ ] `C-CF-134` `data` A refused change returns the current representation of the flag. `src: Core features flags rule 7`
- [ ] `C-CF-135` `data` One flag with one person always resolves to one variant. `src: Core features flags rule 8`
- [ ] `C-CF-136` `contract` An evaluation reason is exactly one of the five pinned words. `src: Core features flags rule 8`
- [ ] `C-CF-137` `data` The evaluation answer agrees with the person timeline. `src: Core features flags rule 8`
- [ ] `C-CF-138` `ui` The live evaluation stream aggregates above the display rate. `src: Core features flags rule 9`
- [ ] `C-CF-139` `data` An experiment carries a primary metric, guardrail metrics, an exposure event. `src: Core features experiments rule 1`
- [ ] `C-CF-140` `contract` An assignment salt never changes once the experiment exists. `src: Core features experiments rule 1`
- [ ] `C-CF-141` `data` One person resolves to one variant everywhere the question is asked. `src: Core features experiments rule 2`
- [ ] `C-CF-142` `data` An exposure is recorded only when the variant was shown. `src: Core features experiments rule 2`
- [ ] `C-CF-143` `data` A power answer names the sample per variant, the projected days, the power. `src: Core features experiments rule 3`
- [ ] `C-CF-144` `literal` A launch below a projected power of `0.60` needs a confirmation. `src: Core features experiments rule 3`
- [ ] `C-CF-145` `data` A results answer names the statistical method in force. `src: Core features experiments rule 4`
- [ ] `C-CF-146` `data` Guardrails are reported in a group of their own. `src: Core features experiments rule 4`
- [ ] `C-CF-147` `data` Missing exposure refuses a conclusion rather than reading as a zero. `src: Core features experiments rule 5`
- [ ] `C-CF-148` `data` Shipping writes the winning variant, ends the experiment, as one operation. `src: Core features experiments rule 6`
- [ ] `C-CF-149` `data` A repeated ship under one idempotency key returns the first answer. `src: Core features experiments rule 6`
- [ ] `C-CF-150` `data` A shipped experiment freezes the definition of that experiment. `src: Core features experiments rule 7`
- [ ] `C-CF-151` `data` An issue carries the first seen moment, the last seen moment, the counts. `src: Core features errors rule 1`
- [ ] `C-CF-152` `data` An issue names the releases spanned by the occurrences. `src: Core features errors rule 1`
- [ ] `C-CF-153` `data` An unresolved frame is labelled unresolved. `src: Core features errors rule 2`
- [ ] `C-CF-154` `data` An unresolved frame names the artefact that is missing. `src: Core features errors rule 2`
- [ ] `C-CF-155` `data` A regrouping creates a new revision rather than rewriting occurrences. `src: Core features errors rule 3`
- [ ] `C-CF-156` `contract` An issue status is exactly one of the six pinned words. `src: Core features errors rule 4`
- [ ] `C-CF-157` `literal` A survey holds at most `20` questions. `src: Core features surveys rule 1`
- [ ] `C-CF-158` `contract` A question kind is open text, single choice, multiple choice, rating, recommendation. `src: Core features surveys rule 1`
- [ ] `C-CF-159` `capability` Survey targeting is previewed against the archive before publishing. `src: Core features surveys rule 2`
- [ ] `C-CF-160` `literal` A theme built from fewer than `5` answers is labelled as small. `src: Core features surveys rule 3`
- [ ] `C-CF-161` `data` A small theme is never shown as a percentage. `src: Core features surveys rule 3`
- [ ] `C-CF-162` `data` A destination lists the breaker state, the backlog depth, the last success. `src: Core features pipeline rule 1`
- [ ] `C-CF-163` `capability` A transformation drops a named property, hashes one, renames one. `src: Core features pipeline rule 2`
- [ ] `C-CF-164` `data` A dry run returns the before shape beside the after shape. `src: Core features pipeline rule 3`
- [ ] `C-CF-165` `literal` A dry run reads at most `100` recent events. `src: Core features pipeline rule 3`
- [ ] `C-CF-166` `contract` Activation without a passing dry run is refused. `src: Core features pipeline rule 3`
- [ ] `C-CF-167` `data` An open breaker pauses delivery without dropping the backlog. `src: Core features pipeline rule 4`
- [ ] `C-CF-168` `data` A held event is inspectable with the failure reason, the full payload. `src: Core features pipeline rule 4`
- [ ] `C-CF-169` `data` A replay never delivers one event twice. `src: Core features pipeline rule 5`
- [ ] `C-CF-170` `data` A failing transformation quarantines the one malformed event. `src: Core features pipeline rule 6`
- [ ] `C-CF-171` `data` A share token is returned exactly once at creation. `src: Core features shares rule 1`
- [ ] `C-CF-172` `contract` The workbench stores only a digest of a share token. `src: Core features shares rule 1`
- [ ] `C-CF-173` `ui` The share sheet opens at the most restrictive setting. `src: Core features shares rule 2`
- [ ] `C-CF-174` `literal` A share defaults to an expiry of `7` days. `src: Core features shares rule 2`
- [ ] `C-CF-175` `ui` The share sheet states in one sentence what the recipient will see. `src: Core features shares rule 2`
- [ ] `C-CF-176` `contract` The public share endpoint returns the one scoped artefact. `src: Core features shares rule 3`
- [ ] `C-CF-177` `literal` A project holds at most `50` shares. `src: Core features shares rule 3`
- [ ] `C-CF-178` `contract` A request outside the token scope gives no signal about existence. `src: Core features shares rule 4`
- [ ] `C-CF-179` `contract` A revoked token, an expired token, an unknown token answer identically. `src: Core features shares rule 4`
- [ ] `C-CF-180` `data` A share row records the access count, the moment of last access. `src: Core features shares rule 5`
- [ ] `C-CF-181` `capability` The workspace is put into a held state deliberately. `src: Core features held rule 1`
- [ ] `C-CF-182` `data` Authoring writes are recorded as pending work with the order preserved. `src: Core features held rule 2`
- [ ] `C-CF-183` `contract` Six named operations are refused outright during a workspace hold. `src: Core features held rule 3`
- [ ] `C-CF-184` `contract` A refusal for a held workspace names the held state as the reason. `src: Core features held rule 3`
- [ ] `C-CF-185` `data` Releasing the hold applies the pending work in order. `src: Core features held rule 4`
- [ ] `C-CF-186` `ui` Conflict resolution is never modal. `src: Core features held rule 4`
- [ ] `C-CF-187` `data` A conflict row keeps the winning value, the losing value, the rule applied. `src: Core features held rule 5`
- [ ] `C-CF-188` `capability` A losing value is restored in one interaction. `src: Core features held rule 5`
- [ ] `C-CF-189` `data` The processing answer names the capabilities the master switch takes away. `src: Core features processing rule 1`
- [ ] `C-CF-190` `ui` The interface states the loss before the master switch is enabled. `src: Core features processing rule 2`
- [ ] `C-CF-191` `contract` A disabled capability is refused as local-only processing. `src: Core features processing rule 3`
- [ ] `C-CF-192` `constraint` A disabled capability never degrades into a weaker version. `src: Core features processing rule 3`
- [ ] `C-CF-193` `data` Every write appends exactly one operation to the workspace log. `src: Core features log rule 1`
- [ ] `C-CF-194` `constraint` Nothing ever updates an operation. `src: Core features log rule 1`
- [ ] `C-CF-195` `constraint` Nothing ever deletes an operation. `src: Core features log rule 1`
- [ ] `C-CF-196` `data` An operation carries the actor, the kind, the target, the before, the after. `src: Core features log rule 2`
- [ ] `C-CF-197` `data` A workspace sequence starts at one, increases strictly, never repeats. `src: Core features log rule 3`
- [ ] `C-CF-198` `data` Four simultaneous writes take four different sequence numbers. `src: Core features log rule 3`
- [ ] `C-CF-199` `data` A transaction lands entirely in the log or not at all. `src: Core features log rule 4`
- [ ] `C-CF-200` `contract` The operations endpoint returns the log newest first. `src: Core features log rule 5`
- [ ] `C-CF-201` `contract` The operations endpoint accepts a since bound. `src: Core features log rule 5`
- [ ] `C-CF-202` `data` Every audit entry carries the digest of the preceding entry. `src: Core features log rule 6`
- [ ] `C-CF-203` `data` The audit answer names the first sequence where the chain parts. `src: Core features log rule 6`
- [ ] `C-CF-204` `data` The health answer enumerates every ingest refusal reason. `src: Core features health rule 1`
- [ ] `C-CF-205` `data` The health answer reconciles storage counts against the workbench accounting. `src: Core features health rule 1`
- [ ] `C-CF-206` `contract` The metered dimensions are events, recordings, evaluations, exceptions, rows. `src: Core features health rule 2`
- [ ] `C-CF-207` `data` A projection states the assumption the projection rests on. `src: Core features health rule 3`
- [ ] `C-CF-208` `data` A projection shows a low figure beside a high figure. `src: Core features health rule 3`
- [ ] `C-CF-209` `data` The project document carries a limits object naming thirteen keys. `src: Core features limits`
- [ ] `C-CF-210` `data` A structural refusal names the same key with the same value. `src: Core features limits`
- [ ] `C-CF-211` `contract` Login returns a bearer token. `src: Core features auth`
- [ ] `C-CF-212` `contract` A step-up takes the password again for a short-lived token. `src: Core features auth`
- [ ] `C-CF-213` `contract` A password is hashed so the plaintext is returned nowhere. `src: Core features auth`
- [ ] `C-CF-214` `contract` An absent token reads as not signed in with nothing written. `src: Core features auth`
- [ ] `C-CF-215` `contract` An unnamed address under the API prefix answers as not found. `src: Core features auth`
- [ ] `C-CF-216` `data` Five kinds of refusal read as five different things. `src: Core features refusals`
- [ ] `C-CF-217` `constraint` No refusal leaves a partial write behind. `src: Core features refusals`
- [ ] `C-CF-218` `ui` A fallback is stated at the point of use. `src: Core features refusals`
- [ ] `C-CF-219` `ui` A form rejects invalid input beside the field that was wrong. `src: Core features forms`
- [ ] `C-CF-220` `ui` A form validates when a field is left rather than on every keystroke. `src: Core features forms`
- [ ] `C-CF-221` `data` A form holding invalid input writes nothing. `src: Core features forms`
- [ ] `C-CF-222` `capability` The privacy page states what the workbench stores about the owner. `src: Core features privacy`
- [ ] `C-CF-223` `capability` The privacy page states what the workbench stores about a data subject. `src: Core features privacy`
- [ ] `C-CF-224` `capability` The privacy page is readable without signing in. `src: Core features privacy`
- [ ] `C-CF-225` `ui` The privacy page is reachable from the footer of every page. `src: Core features privacy`
- [ ] `C-CF-226` `capability` Every internal link on every route resolves to a real page. `src: Core features links`
- [ ] `C-CF-227` `ui` The not-found page carries a way back to the field. `src: Core features links`

## C-UF User flow

- [ ] `C-UF-01` `contract` The root address redirects a signed-in owner to the last project field. `src: User flow route table`
- [ ] `C-UF-02` `contract` The root address redirects an unknown visitor to the sign-in route. `src: User flow route table`
- [ ] `C-UF-03` `contract` Every project route carries the project slug as a path segment. `src: User flow route table`
- [ ] `C-UF-04` `contract` The recipient route sits outside the application shell. `src: User flow route table`
- [ ] `C-UF-05` `contract` An unauthenticated request for a required route lands on the sign-in route. `src: User flow entry`
- [ ] `C-UF-06` `capability` Signing in returns the owner to the route originally requested. `src: User flow entry`
- [ ] `C-UF-07` `capability` Signing out stops the old bearer token working. `src: User flow entry`
- [ ] `C-UF-08` `contract` A project in a workspace the caller does not own answers as absent. `src: User flow entry`
- [ ] `C-UF-09` `capability` Brushing the whole archive reports a cohort size counting up to eight. `src: User flow journey 1`
- [ ] `C-UF-10` `capability` A saved cohort reopens after a reload with the same two numbers. `src: User flow journey 1`
- [ ] `C-UF-11` `capability` Zooming out then in moves the band indicator through five bands. `src: User flow journey 2`
- [ ] `C-UF-12` `capability` A funnel dropped on the field draws as geometry over the marks. `src: User flow journey 3`
- [ ] `C-UF-13` `capability` Clicking a funnel drop-off reaches the persons who fell out. `src: User flow journey 3`
- [ ] `C-UF-14` `capability` A person timeline opens the recording belonging to that person. `src: User flow journey 4`
- [ ] `C-UF-15` `capability` A blast radius is read before a rollout change is saved. `src: User flow journey 5`
- [ ] `C-UF-16` `capability` An audit entry names the state a killed flag was killed from. `src: User flow journey 5`
- [ ] `C-UF-17` `capability` Shipping twice under one idempotency key ships once. `src: User flow journey 6`
- [ ] `C-UF-18` `capability` An insight saved during a hold appears as pending work. `src: User flow journey 7`
- [ ] `C-UF-19` `capability` Released pending work crosses into applied in acknowledgement order. `src: User flow journey 7`
- [ ] `C-UF-20` `capability` A share link opened without a session shows no way into the workbench. `src: User flow journey 9`
- [ ] `C-UF-21` `capability` An empty project reads the honest empty state naming the reason. `src: User flow journey 10`
- [ ] `C-UF-22` `ui` Being filtered to nothing names the filter responsible. `src: User flow states`
- [ ] `C-UF-23` `ui` Every page carries a loading state. `src: User flow states`
- [ ] `C-UF-24` `ui` Four kinds of failure are told apart on every surface. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Four design principles govern every surface of the workbench. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The chrome of the workbench carries no hue of its own. `src: UI/UX notes para 4`
- [ ] `C-UX-03` `ui` Ground, panels, wells, dividers, borders, text read as one neutral family. `src: UI/UX notes para 4`
- [ ] `C-UX-04` `ui` One accent means interactive, reading as a blue. `src: UI/UX notes para 4`
- [ ] `C-UX-05` `ui` A green carries increase, success, a resolved group. `src: UI/UX notes para 4`
- [ ] `C-UX-06` `ui` A red carries decrease, error, an unresolved group. `src: UI/UX notes para 4`
- [ ] `C-UX-07` `ui` An orange carries a guardrail breach, an approaching allowance. `src: UI/UX notes para 4`
- [ ] `C-UX-08` `ui` A cyan carries a neutral notice. `src: UI/UX notes para 4`
- [ ] `C-UX-09` `ui` The categorical palette spans eight named hue families. `src: UI/UX notes para 5`
- [ ] `C-UX-10` `ui` Past eight categories the palette switches to a lightness ramp. `src: UI/UX notes para 5`
- [ ] `C-UX-11` `ui` A density mapping runs monotonically from dark to bright. `src: UI/UX notes para 5`
- [ ] `C-UX-12` `ui` An increase carries a glyph beside the hue. `src: UI/UX notes para 5`
- [ ] `C-UX-13` `ui` The workbench is committed to a dark ground with a light theme beside. `src: UI/UX notes para 5`
- [ ] `C-UX-14` `ui` One typeface carries the interface, one carries numbers. `src: UI/UX notes para 6`
- [ ] `C-UX-15` `ui` Numeric displays set figures on lining numerals of equal width. `src: UI/UX notes para 6`
- [ ] `C-UX-16` `ui` Nothing in the workbench is set larger than the hero metric value. `src: UI/UX notes para 6`
- [ ] `C-UX-17` `ui` Corners are barely softened throughout the workbench. `src: UI/UX notes para 7`
- [ ] `C-UX-18` `ui` Elevation pairs a border with a shadow across four levels. `src: UI/UX notes para 7`
- [ ] `C-UX-19` `ui` Every gap is a multiple of one base unit. `src: UI/UX notes para 7`
- [ ] `C-UX-20` `ui` An icon is never the sole carrier of meaning. `src: UI/UX notes para 7`
- [ ] `C-UX-21` `ui` Every animated moment declares one of five interruption behaviours. `src: UI/UX notes para 8`
- [ ] `C-UX-22` `ui` Panning the field carries momentum with a settle rather than a snap. `src: UI/UX notes para 9`
- [ ] `C-UX-23` `ui` The field resists beyond the ends of the archive rather than stopping dead. `src: UI/UX notes para 9`
- [ ] `C-UX-24` `ui` The brush follows the pointer with no smoothing. `src: UI/UX notes para 9`
- [ ] `C-UX-25` `ui` A live arrival blooms briefly where the arrival lands. `src: UI/UX notes para 9`
- [ ] `C-UX-26` `ui` A changing number counts through intermediate values with a fixed width. `src: UI/UX notes para 10`
- [ ] `C-UX-27` `ui` A metric crossing a threshold thickens, then settles a little heavier. `src: UI/UX notes para 10`
- [ ] `C-UX-28` `ui` The element under the pointer holds position during a reflow. `src: UI/UX notes para 10`
- [ ] `C-UX-29` `ui` A progress rail is driven by real completed units. `src: UI/UX notes para 10`
- [ ] `C-UX-30` `ui` A progress rail runs to the end before leaving. `src: UI/UX notes para 10`
- [ ] `C-UX-31` `ui` Reduced motion gives every moment a designed alternative. `src: UI/UX notes para 12`
- [ ] `C-UX-32` `ui` Reduced motion keeps the cohort dimming. `src: UI/UX notes para 12`
- [ ] `C-UX-33` `ui` Reduced motion keeps the progress rail. `src: UI/UX notes para 12`
- [ ] `C-UX-34` `ui` Feedback arrives as an inline banner that stays until dismissed. `src: UI/UX notes para 13`
- [ ] `C-UX-35` `ui` Each page leads with exactly one primary action. `src: UI/UX notes para 14`
- [ ] `C-UX-36` `ui` Every content image carries alternative text. `src: UI/UX notes para 14`
- [ ] `C-UX-37` `literal` Body text holds a contrast ratio of at least `4.5:1`. `src: UI/UX notes para 15`
- [ ] `C-UX-38` `literal` A focus ring holds a contrast ratio of at least `3:1`. `src: UI/UX notes para 15`
- [ ] `C-UX-39` `literal` A touch target is at least `44` CSS pixels on each side. `src: UI/UX notes para 15`
- [ ] `C-UX-40` `ui` Every gesture of the field has a keyboard equivalent. `src: UI/UX notes para 15`
- [ ] `C-UX-41` `ui` The field announces the settled viewport to assistive technology. `src: UI/UX notes para 15`
- [ ] `C-UX-42` `ui` A complete table of the drawn rows is reachable by one keystroke. `src: UI/UX notes para 15`
- [ ] `C-UX-43` `ui` The workbench draws at three tiers with no capability differing. `src: UI/UX notes para 16`
- [ ] `C-UX-44` `ui` A tier change is announced rather than silent. `src: UI/UX notes para 16`
- [ ] `C-UX-45` `ui` The rail collapses to icons as the viewport narrows. `src: UI/UX notes para 17`
- [ ] `C-UX-46` `ui` At phone width the field is read only with the reason stated. `src: UI/UX notes para 17`
- [ ] `C-UX-47` `ui` Nothing overflows sideways at any viewport width. `src: UI/UX notes para 17`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The field is persistent so no contextual surface tears the field down. `src: Front-end specification shell`
- [ ] `C-FE-02` `ui` A surface mounted beside the field keeps the visible time range. `src: Front-end specification shell`
- [ ] `C-FE-03` `ui` Moving between surfaces carries the active time range. `src: Front-end specification shell`
- [ ] `C-FE-04` `ui` The rail carries exactly eight destinations in a fixed order. `src: Front-end specification rail`
- [ ] `C-FE-05` `ui` Project switching lives in the rail header rather than the rail body. `src: Front-end specification rail`
- [ ] `C-FE-06` `ui` Switching project keeps the current surface. `src: Front-end specification rail`
- [ ] `C-FE-07` `ui` The command surface resolves typed text against every saved object. `src: Front-end specification command`
- [ ] `C-FE-08` `ui` The command surface moves the selection with the arrow keys. `src: Front-end specification command`
- [ ] `C-FE-09` `ui` A time ribbon runs across the top of the field. `src: Front-end specification field`
- [ ] `C-FE-10` `ui` A hover card carries the event name, the timestamp, the person. `src: Front-end specification field`
- [ ] `C-FE-11` `ui` A minimap marks the current viewport within the whole archive. `src: Front-end specification field`
- [ ] `C-FE-12` `ui` Tab moves focus between marks in time order inside the viewport. `src: Front-end specification keyboard`
- [ ] `C-FE-13` `ui` The insight builder sits beside the result above a wide width. `src: Front-end specification insight`
- [ ] `C-FE-14` `ui` A virtualised table of the same rows sits beneath the result. `src: Front-end specification insight`
- [ ] `C-FE-15` `ui` The scrubber carries five marked tracks. `src: Front-end specification player`
- [ ] `C-FE-16` `ui` The player side panel becomes a bottom sheet below a narrow width. `src: Front-end specification player`
- [ ] `C-FE-17` `ui` The kill control is reachable in one interaction from an error group. `src: Front-end specification flag`
- [ ] `C-FE-18` `ui` A conflict row shows both values with the rule that decided. `src: Front-end specification sync`
- [ ] `C-FE-19` `ui` The recipient surface loads no rail, no command surface. `src: Front-end specification recipient`
- [ ] `C-FE-20` `ui` A refused recipient surface holds the last frame as a still image. `src: Front-end specification recipient`
- [ ] `C-FE-21` `contract` The field root carries a band attribute taking the five band slugs. `src: Front-end specification hooks`
- [ ] `C-FE-22` `contract` The field root carries a state attribute taking four pinned words. `src: Front-end specification hooks`
- [ ] `C-FE-23` `contract` Every element holding a result carries a source attribute. `src: Front-end specification hooks`
- [ ] `C-FE-24` `contract` Each rail destination carries a rail attribute taking the destination slug. `src: Front-end specification hooks`
- [ ] `C-FE-25` `contract` Every lifecycle chip carries a state-chip attribute taking six pinned words. `src: Front-end specification hooks`
- [ ] `C-FE-26` `contract` The recipient surface root carries a share-scope attribute. `src: Front-end specification hooks`
- [ ] `C-FE-27` `ui` An empty project offers the ingest snippet rather than documentation. `src: Front-end specification empty`
- [ ] `C-FE-28` `ui` Every control carries resting, pointed-at, pressed, focused, unavailable states. `src: Front-end specification components`
- [ ] `C-FE-29` `ui` Unavailable is never signalled by colour alone. `src: Front-end specification components`
- [ ] `C-FE-30` `ui` A destructive action asks for confirmation naming what will be removed. `src: Front-end specification components`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` The frontend is Lit with Vite. `src: Technical requirements para 1`
- [ ] `C-TR-02` `constraint` The HTTP API is NestJS on Node 20. `src: Technical requirements para 1`
- [ ] `C-TR-03` `constraint` PostgreSQL is the only backing service. `src: Technical requirements para 2`
- [ ] `C-TR-04` `contract` The database address is read from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-05` `contract` The public address is read from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-06` `contract` A list endpoint answers with a data array beside a page object. `src: Technical requirements para 5`
- [ ] `C-TR-07` `contract` Paging is by cursor, never by offset. `src: Technical requirements para 5`
- [ ] `C-TR-08` `contract` A cursor against a different sort order is refused as a sort mismatch. `src: Technical requirements para 5`
- [ ] `C-TR-09` `contract` A refusal carries a code, a message, a trace identifier. `src: Technical requirements para 6`
- [ ] `C-TR-10` `contract` A refusal code comes from the closed set of twenty. `src: Technical requirements para 6`
- [ ] `C-TR-11` `contract` Every enumeration is closed so an unknown value is refused. `src: Technical requirements para 6`
- [ ] `C-TR-12` `contract` Every response carries three rate-limit headers. `src: Technical requirements para 7`
- [ ] `C-TR-13` `contract` Every response carries the standard security headers. `src: Technical requirements para 8`
- [ ] `C-TR-14` `contract` Every public route declares a title, a description, sharing neither. `src: Technical requirements para 9`
- [ ] `C-TR-15` `contract` The health route answers two hundred once the app is ready. `src: Technical requirements para 10`
- [ ] `C-TR-16` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements para 10`

## C-DM Data model

- [ ] `C-DM-01` `data` An account email is unique when compared without case. `src: Data model accounts`
- [ ] `C-DM-02` `data` A project slug is unique within the workspace of that project. `src: Data model projects`
- [ ] `C-DM-03` `data` A person distinct identifier is unique within the project of that person. `src: Data model persons`
- [ ] `C-DM-04` `data` A non-empty erasure moment tombstones the person. `src: Data model persons`
- [ ] `C-DM-05` `data` An alias is unique within the project of that alias. `src: Data model person aliases`
- [ ] `C-DM-06` `data` A rollup bucket count equals the event rows inside the bucket. `src: Data model invariants`
- [ ] `C-DM-07` `data` A masking policy is snapshotted per recording. `src: Data model recordings`
- [ ] `C-DM-08` `data` A recording frame sequence is unique within the recording. `src: Data model recording frames`
- [ ] `C-DM-09` `data` Variant percentages across one flag total exactly one hundred. `src: Data model flag variants`
- [ ] `C-DM-10` `data` One assignment row exists per experiment per person. `src: Data model assignments`
- [ ] `C-DM-11` `data` An exposure row is written only when the variant was shown. `src: Data model exposures`
- [ ] `C-DM-12` `data` One delivery row exists per destination per event. `src: Data model deliveries`
- [ ] `C-DM-13` `data` The raw share token is stored nowhere. `src: Data model shares`
- [ ] `C-DM-14` `data` A key secret is shown once at creation, never again. `src: Data model keys`
- [ ] `C-DM-15` `data` An operation row is never changed after being written. `src: Data model invariants`
- [ ] `C-DM-16` `data` An event admitted twice under one dedupe key leaves one row. `src: Data model invariants`
- [ ] `C-DM-17` `data` A tombstoned person leaves no event row naming that person. `src: Data model invariants`
- [ ] `C-DM-18` `data` A tombstoned person creates no new person row on a later arrival. `src: Data model invariants`
- [ ] `C-DM-19` `literal` The seeded workspace of the owner is `Northlight Labs`. `src: Data model seed data`
- [ ] `C-DM-20` `literal` The seeded archive project slug is `ledgerline`. `src: Data model seed data`
- [ ] `C-DM-21` `literal` The seeded empty project slug is `quarry`. `src: Data model seed data`
- [ ] `C-DM-22` `literal` The second workspace project slug is `stonefall`. `src: Data model seed data`
- [ ] `C-DM-23` `literal` The seeded archive spans the trailing `180` days. `src: Data model seed data`
- [ ] `C-DM-24` `data` The six seeded event types carry the pinned counts. `src: Data model seed data`
- [ ] `C-DM-25` `literal` The seeded multivariate flag is `export-v2`. `src: Data model seed data`
- [ ] `C-DM-26` `literal` The seeded boolean flag is `fast-search`. `src: Data model seed data`
- [ ] `C-DM-27` `literal` The seeded experiment is `export-v2-trial`. `src: Data model seed data`
- [ ] `C-DM-28` `data` One seeded error group resolves its frames back to source. `src: Data model seed data`
- [ ] `C-DM-29` `data` One seeded error group renders unresolved frames. `src: Data model seed data`
- [ ] `C-DM-30` `data` One seeded recording carries an inactive stretch beside a dropped stretch. `src: Data model seed data`
- [ ] `C-DM-31` `literal` The seeded open destination holds a backlog of `41` events. `src: Data model seed data`
- [ ] `C-DM-32` `data` The seeded operation log starts at sequence one. `src: Data model seed data`
- [ ] `C-DM-33` `data` Seeding is idempotent so a restart duplicates no row. `src: Data model seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The workbench holds no organisation above the account. `src: Constraints bullet 2`
- [ ] `C-CN-02` `constraint` The workbench accepts no uploaded file. `src: Constraints bullet 3`
- [ ] `C-CN-03` `constraint` The workbench sends no email. `src: Constraints bullet 4`
- [ ] `C-CN-04` `constraint` The workbench takes no payment. `src: Constraints bullet 5`
- [ ] `C-CN-05` `constraint` The workbench offers no federated sign-in. `src: Constraints bullet 6`
- [ ] `C-CN-06` `constraint` The workbench hosts no external table. `src: Constraints bullet 8`
- [ ] `C-CN-07` `constraint` The workbench ingests no advertising cost data. `src: Constraints bullet 10`
- [ ] `C-CN-08` `constraint` The workbench pushes nothing in real time between people. `src: Constraints bullet 11`
- [ ] `C-CN-09` `constraint` The workbench carries no artificial intelligence feature. `src: Constraints bullet 12`
- [ ] `C-CN-10` `constraint` The workbench makes no external network call at run time. `src: Constraints bullet 13`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at the public address from the environment. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served under the API prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The health route answers two hundred once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `literal` The credentials file is written at `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `literal` The reserved screenshots directory is `.browser_screenshots/`. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `literal` The reserved downloads directory is `.downloads/`. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` A production build is served rather than a development server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `literal` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `constraint` No copy of a backing service is downloaded or started. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `constraint` No persistent volume, container name, custom network is declared. `src: Deployment contract bullet 12`
- [ ] `C-DC-14` `data` A list endpoint answers the named shape with the exact field names. `src: Deployment contract response shapes`
- [ ] `C-DC-15` `contract` An unauthorized call is rejected as a client error. `src: Deployment contract response shapes`
- [ ] `C-DC-16` `contract` Bearer auth is carried on every endpoint outside the five named. `src: Deployment contract response shapes`
- [ ] `C-DC-17` `constraint` The database is the fact rather than an in-memory array. `src: Deployment contract no mocks`
- [ ] `C-DC-18` `constraint` No operation log is kept only in the running process. `src: Deployment contract no mocks`

## Pinned literals

| Value | What it is | Item |
|---|---|---|
| `deku-demo-pw-2026` | the password every seeded account uses | `C-RL-16` |
| `owner@example.com` | the seeded owner account | `C-RL-17` |
| `other@example.com` | the second seeded account | `C-RL-18` |
| `2400` | the seeded archive event total | `C-CF-12` |
| `8` | the seeded archive person total | `C-CF-13` |
| `87.50%` | the seeded funnel second-step conversion | `C-CF-16` |
| `71.43%` | the seeded funnel third-step conversion | `C-CF-17` |
| `62.50%` | the seeded funnel end-to-end conversion | `C-CF-18` |
| `500` | the ingest batch ceiling | `C-CF-50` |
| `24` | the deduplication window in hours | `C-CF-57` |
| `30` | the merge reversal window in days | `C-CF-70` |
| `20` | the funnel step ceiling | `C-CF-88` |
| `10000` | the breakdown cardinality ceiling | `C-CF-91` |
| `2000000` | the projected-row ceiling for one query | `C-CF-93` |
| `40` | the dashboard tile ceiling | `C-CF-96` |
| `8` | the variant ceiling per flag | `C-CF-115` |
| `3` | the targeting nesting ceiling | `C-CF-119` |
| `24` | the condition ceiling per targeting rule | `C-CF-120` |
| `25` | the rollout jump needing a confirmation | `C-CF-123` |
| `0.60` | the projected power needing a confirmation | `C-CF-144` |
| `20` | the survey question ceiling | `C-CF-157` |
| `5` | the answer count below which a theme reads as small | `C-CF-160` |
| `100` | the dry-run event ceiling | `C-CF-165` |
| `7` | the default share expiry in days | `C-CF-174` |
| `50` | the share ceiling per project | `C-CF-177` |
| `4.5:1` | the body-text contrast floor | `C-UX-37` |
| `3:1` | the focus-ring contrast floor | `C-UX-38` |
| `44` | the touch-target floor in CSS pixels | `C-UX-39` |
| `Northlight Labs` | the seeded owner workspace | `C-DM-19` |
| `ledgerline` | the seeded archive project slug | `C-DM-20` |
| `quarry` | the seeded empty project slug | `C-DM-21` |
| `stonefall` | the second workspace project slug | `C-DM-22` |
| `180` | the seeded archive span in days | `C-DM-23` |
| `export-v2` | the seeded multivariate flag key | `C-DM-25` |
| `fast-search` | the seeded boolean flag key | `C-DM-26` |
| `export-v2-trial` | the seeded experiment key | `C-DM-27` |
| `41` | the seeded held backlog depth | `C-DM-31` |
| `4173` | the container-internal port | `C-DC-02` |
| `/app/USER_README.md` | the credentials file path | `C-DC-06` |
| `.browser_screenshots/` | the reserved screenshots directory | `C-DC-07` |
| `.downloads/` | the reserved downloads directory | `C-DC-08` |
| `0.0.0.0` | the bind address | `C-DC-11` |
| `Coldwater Games` | the second seeded workspace | `` |
| `northlight-labs` | the seeded owner workspace slug | `` |
| `coldwater-games` | the second seeded workspace slug | `` |
| `Marisol Vega` | the display name of the seeded owner | `` |
| `Anders Roeg` | the display name of the second account | `` |
| `app_opened` | the most frequent seeded event type | `` |
| `search_run` | the second funnel step event type | `` |
| `report_exported` | the third funnel step event type | `` |
| `export_panel_seen` | the seeded exposure event type | `` |
| `invite_sent` | a seeded event type | `` |
| `plan_upgraded` | a seeded event type | `` |
| `960` | the seeded app_opened event count | `` |
| `612` | the seeded search_run event count | `` |
| `384` | the seeded export_panel_seen event count | `` |
| `312` | the seeded report_exported event count | `` |
| `108` | the seeded invite_sent event count | `` |
| `24` | the seeded plan_upgraded event count | `` |
| `anna-reyes` | a seeded person distinct identifier | `` |
| `northlight-export-2026` | the seeded assignment salt | `` |
| `control` | the default variant of the seeded flag | `` |
| `compact` | a variant of the seeded flag | `` |
| `wide` | a variant of the seeded flag | `` |
| `1.6.0` | the newest seeded release | `` |
| `warehouse-sink` | the seeded destination with an open breaker | `` |
| `metrics-mirror` | the seeded destination delivering normally | `` |
| `why-export` | the seeded survey key | `` |
| `Weekly exports` | the seeded insight name | `` |
| `Ledgerline weekly` | the seeded dashboard name | `` |
| `Exported this season` | the seeded cohort name | `` |
| `epoch` | the coarsest band slug | `` |
| `moment` | the finest band slug | `` |
| `store` | an execution source value | `` |
| `rollup` | an execution source value | `` |
| `data-band` | the band hook on the field root | `` |
| `data-field-state` | the state hook on the field root | `` |
| `data-source` | the provenance hook on a result | `` |
| `data-rail` | the destination hook on a rail entry | `` |
| `data-state-chip` | the lifecycle hook on a chip | `` |
| `data-track` | the track hook on a scrubber track | `` |
| `data-share-scope` | the scope hook on the recipient root | `` |
| `workspace_held` | the refusal code for a held workspace | `` |
| `local_only_processing` | the refusal code for a disabled capability | `` |
| `person_erased` | the refusal code for an erased person | `` |
| `project_mismatch` | the refusal code for the wrong project | `` |
| `dry_run_required` | the refusal code for an unproven transformation | `` |
| `version_mismatch` | the refusal code for a stale version | `` |
| `insufficient_scope` | the refusal code for a missing scope | `` |
| `DATABASE_URL` | the database environment variable | `` |
| `APP_PUBLIC_URL` | the public address environment variable | `` |
| `/api` | the HTTP API prefix | `` |
| `/i/v1/events` | the ingest endpoint | `` |
| `200` | the ready answer of the health route | `` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of each palette role | `C-UX-04` |
| the spans at which the band boundaries sit | `C-CF-23` |
| the base unit every gap is a multiple of | `C-UX-19` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| overview | 6 | 10 |
| user roles | 12 | 18 |
| core features | 96 | 227 |
| user flow | 14 | 24 |
| ui and ux notes | 18 | 47 |
| front-end specification | 12 | 30 |
| technical requirements | 11 | 16 |
| data model | 14 | 33 |
| constraints | 8 | 10 |
| deployment contract | 15 | 18 |
