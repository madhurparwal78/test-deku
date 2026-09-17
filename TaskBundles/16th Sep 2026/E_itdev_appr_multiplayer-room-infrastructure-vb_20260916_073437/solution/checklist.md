# Checklist: deku/multiplayer-room-infrastructure-vb

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Items: 173
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` One authorisation decision governs every surface `src: Overview, one authorisation decision`
- [ ] `C-OV-02` `capability` A change approval workflow guards the dangerous actions `src: Overview, a change approval workflow`
- [ ] `C-OV-03` `capability` A metered bill reconciles to the lines on the invoice `src: Overview, a metered bill`
- [ ] `C-OV-04` `capability` An append only record names who did what `src: Overview, an append only record`
- [ ] `C-OV-05` `capability` Leaving the directory ends access `src: Overview, a directory connection where leaving means leaving`

## C-RL User roles

- [ ] `C-RL-01` `role` An analyst writes nothing `src: User roles, write anything, or reach a credential`
- [ ] `C-RL-02` `role` An admin never approves a request raised by that same admin `src: User roles, approve a request they raised`
- [ ] `C-RL-03` `role` The admin holding ownership may use break glass `src: User roles, adding legal hold release, break glass`
- [ ] `C-RL-04` `role` A developer approving any request is refused `src: User roles, approve anything, or read a production credential`
- [ ] `C-RL-05` `role` An end user identity fails closed on a console route `src: User roles, that identity fails closed on a console route`
- [ ] `C-RL-06` `constraint` A refusal never reveals whether a resource exists `src: User roles, never says whether a resource exists`

## C-CF Core features

- [ ] `C-CF-01` `capability` A change request carries an impact summary counting rooms, connections, end users, members, credentials `src: Core features, an impact summary counting the rooms, connections`
- [ ] `C-CF-02` `constraint` Expiry produces an outcome `src: Core features, an expired request says so and its requester is told`
- [ ] `C-CF-03` `capability` The requester of an expired request is told `src: Core features, an expired request says so and its requester is told`
- [ ] `C-CF-04` `constraint` Self approval is refused wherever attempted `src: Core features, Self approval is refused wherever it is attempted`
- [ ] `C-CF-05` `constraint` Executing arguments nobody approved is refused `src: Core features, Executing other arguments than those approved is refused`
- [ ] `C-CF-06` `constraint` A materially grown impact returns the request to pending `src: Core features, returns the request to pending with the difference shown`
- [ ] `C-CF-07` `capability` Revocation terminates every open room connection of the group `src: Core features, every open room connection naming them is terminated`
- [ ] `C-CF-08` `capability` Revocation revokes every console session held by group members `src: Core features, every console session its members hold is revoked`
- [ ] `C-CF-09` `capability` Revocation retires every credential the group members issued `src: Core features, every credential they issued is retired`
- [ ] `C-CF-10` `constraint` A production credential is shown once `src: Core features, a production credential is shown once`
- [ ] `C-CF-11` `capability` Every development credential reveal is recorded `src: Core features, A development credential is revealable again and every reveal is recorded`
- [ ] `C-CF-12` `constraint` An environment region is fixed at creation `src: Core features, Kind and region are fixed at creation`
- [ ] `C-CF-13` `capability` Opening the inspector is recorded as a read of customer content `src: Core features, the inspector is a read of another company's content, recorded as such`
- [ ] `C-CF-14` `capability` The admission check reads the entitlement table `src: Core features, the admission check deciding whether one more connection is allowed`
- [ ] `C-CF-15` `capability` The comparison matrix reads the entitlement table `src: Core features, The pricing page, the comparison matrix`
- [ ] `C-CF-16` `capability` The console warning threshold reads the entitlement table `src: Core features, the warning threshold`
- [ ] `C-CF-17` `capability` The invoice line reads the entitlement table `src: Core features, the warning threshold and the invoice all read it`
- [ ] `C-CF-18` `constraint` Collaboration minutes accrue per room only with two or more connections `src: Core features, Collaboration minutes accrue per room only while two or more connections are held`
- [ ] `C-CF-19` `capability` Every refusal enters the append only record `src: Core features, refusal is written to an append only record`
- [ ] `C-CF-20` `constraint` Each record entry is sealed against the previous entry `src: Core features, sealed against the one before it`
- [ ] `C-CF-21` `capability` An unknown address renders a not-found page in the product's own dress `src: Core features, a not-found page in the product's own dress`
- [ ] `C-CF-22` `capability` The site serves a favicon `src: Core features, a not-found page in the product's own dress, a favicon`
- [ ] `C-CF-23` `capability` An owner reads recorded page views `src: Core features, a page view an owner can read`
- [ ] `C-CF-24` `constraint` The enquiry form refuses a submission arriving repeatedly `src: Core features, a form refusing a submission that arrives repeatedly`

## C-UF User flow

- [ ] `C-UF-01` `ui` A sidebar carries the organisation switcher, project list, environment badge, surface links `src: User flow, carries the organisation switcher, the project list, the environment badge and the surface links`
- [ ] `C-UF-02` `ui` The sidebar survives every route change `src: User flow, It survives every route change`
- [ ] `C-UF-03` `contract` An unauthenticated console request is refused rather than redirected `src: User flow, an unauthenticated request is refused, never redirected`
- [ ] `C-UF-04` `ui` A console surface shows a loading state shaped like the content arriving `src: User flow, loading shaped like what replaces it`
- [ ] `C-UF-05` `ui` A console surface shows an error state carrying the request identifier `src: User flow, error carrying the request identifier`
- [ ] `C-UF-06` `ui` A partial surface renders loaded rows under a strip naming the missing dependency `src: User flow, partial, where loaded rows render and a strip names what did not`
- [ ] `C-UF-07` `ui` The approvals queue lists requests filtered by state `src: User flow, the queue, filtered by state`
- [ ] `C-UF-08` `ui` Raising a request walks a three step wizard `src: User flow, the three step wizard`
- [ ] `C-UF-09` `ui` A toast confirms an executed request `src: User flow, a toast confirms the outcome`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The ground is true black with one raised step `src: UI/UX notes, a true black ground with one raised step`
- [ ] `C-UX-02` `ui` Cards share edges `src: UI/UX notes, Cards share edges`
- [ ] `C-UX-03` `ui` Body copy is grey rather than white `src: UI/UX notes, a grey light neutral for body`
- [ ] `C-UX-04` `ui` A large soft bloom sits behind the hero `src: UI/UX notes, a soft pink bloom behind the hero`
- [ ] `C-UX-05` `ui` Motion follows eased curves with one slight overshoot `src: UI/UX notes, one slight overshoot used once`
- [ ] `C-UX-06` `ui` Reduced motion keeps colour changes, disclosures, the spinner `src: UI/UX notes, colour changes, disclosures and the spinner stay`
- [ ] `C-UX-07` `ui` Focus is never removed `src: UI/UX notes, a focus ring never removed`
- [ ] `C-UX-08` `constraint` Body text meets the WCAG AA contrast bar `src: UI/UX notes, text keeps clear contrast against its ground`
- [ ] `C-UX-09` `constraint` alternative text on every content image `src: UI/UX notes, alternative text on every content image`
- [ ] `C-UX-10` `constraint` Nothing overflows sideways at the narrowest viewport `src: UI/UX notes, nothing overflowing at the narrowest viewport`
- [ ] `C-UX-11` `ui` Danger, success, warning states each carry a hue plus a word `src: UI/UX notes, Danger, success and warning each own a hue and always carry a word beside it`
- [ ] `C-UX-12` `ui` The primary action is a white button darkening on hover `src: UI/UX notes, The primary action is a white button that darkens on hover`
- [ ] `C-UX-13` `ui` An input label sits above its field with the error below `src: UI/UX notes, An input's label sits above and its error below`
- [ ] `C-UX-14` `ui` A toast confirms an outcome then leaves on its own `src: UI/UX notes, a toast confirms and leaves`
- [ ] `C-UX-15` `ui` An overlay closes on Escape `src: UI/UX notes, an overlay closes on Escape`
- [ ] `C-UX-16` `ui` Icon only controls carry labels `src: UI/UX notes, labels on icon only controls`
- [ ] `C-UX-17` `ui` Meaning is never carried by colour alone `src: UI/UX notes, meaning never by colour alone`
- [ ] `C-UX-18` `ui` Touch targets are comfortable `src: UI/UX notes, comfortable touch targets`
- [ ] `C-UX-19` `ui` Aligned numbers use tabular figures `src: UI/UX notes, tabular figures where numbers align`
- [ ] `C-UX-20` `ui` Keyboard navigation reaches every feature a pointer reaches `src: UI/UX notes, keyboard navigation with a focus ring never removed`
- [ ] `C-UX-21` `ui` Handwritten annotations point at the working miniatures `src: UI/UX notes, working miniatures, and handwritten annotations`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` A developer issuing a production credential is refused `src: Technical requirements, production keys are issued by an admin or owner`
- [ ] `C-TR-02` `contract` A sign in returns an access token naming a session row `src: Technical requirements, a bearer token that names that row`
- [ ] `C-TR-03` `constraint` A revoked session bearer token is refused `src: Technical requirements, A revoked session's bearer token is refused on the next call`
- [ ] `C-TR-04` `constraint` An identity token outside the realtime prefix is refused `src: Technical requirements, An identity token presented to any`
- [ ] `C-TR-05` `constraint` Room grant layers resolve by replacement `src: Technical requirements, The more specific layer replaces the less specific one entirely`
- [ ] `C-TR-06` `constraint` A user grant of read over a group grant of write narrows the end user to read `src: Technical requirements, sitting over a group grant of`
- [ ] `C-TR-07` `constraint` Room write carries no implied comment write `src: Technical requirements, room:write does not imply comment:write`
- [ ] `C-TR-08` `constraint` Permission is re-evaluated on every operation `src: Technical requirements, Permission is re-evaluated on every operation, not at admission`
- [ ] `C-TR-09` `constraint` Removing read closes the connection `src: Technical requirements, Remove read and the connection is closed instead`
- [ ] `C-TR-10` `constraint` The connection past the ceiling is refused with the oldest kept open `src: Technical requirements, the oldest connection is never dropped to make room`
- [ ] `C-TR-11` `contract` The argument hash is SHA-256 over sorted whitespace-free JSON `src: Technical requirements, arguments object serialised as JSON with keys sorted, no whitespace`
- [ ] `C-TR-12` `constraint` A grown impact answers impact_changed carrying both summaries `src: Technical requirements, carrying both summaries as approved_impact`
- [ ] `C-TR-13` `capability` Every eligible approver is notified again after impact growth `src: Technical requirements, every eligible approver is notified again`
- [ ] `C-TR-14` `constraint` Break glass requires a second factor asserted within 300 seconds `src: Technical requirements, requires a second factor asserted within the last 300 seconds`
- [ ] `C-TR-15` `capability` Break glass notifies every owner plus every eligible approver `src: Technical requirements, notifies every owner and every eligible approver immediately`
- [ ] `C-TR-16` `capability` Break glass opens a review item outstanding until justified `src: Technical requirements, opens a review item that GET /api/review-items reports as outstanding`
- [ ] `C-TR-17` `constraint` A regulated room refuses the inspector without a grant `src: Technical requirements, refuses the inspector outright`
- [ ] `C-TR-18` `constraint` A just in time grant expires rather than renewing `src: Technical requirements, it expires rather than renewing`
- [ ] `C-TR-19` `capability` Revocation removes every grant keyed by the group `src: Technical requirements, row keyed by that group survives`
- [ ] `C-TR-20` `capability` Revocation marks every group membership deprovisioned `src: Technical requirements, every membership it carries reads deprovisioned`
- [ ] `C-TR-21` `constraint` A level meter bills the highest sample of the period `src: Technical requirements, highest sample recorded in the period, never the sum`
- [ ] `C-TR-22` `constraint` Six people in a room for one minute bill one minute `src: Technical requirements, Six people in a room for one minute is one minute, not six`
- [ ] `C-TR-23` `constraint` The invoice total equals the sum of the visible invoice lines `src: Technical requirements, The invoice total equals the sum of its own visible lines`
- [ ] `C-TR-24` `constraint` Every money figure is an integer in minor units `src: Technical requirements, Every figure is an integer in minor units of usd`
- [ ] `C-TR-25` `capability` A downgrade breaching an entitlement is accepted for period end `src: Technical requirements, accepted and scheduled for period end`
- [ ] `C-TR-26` `constraint` Identical simultaneous interval writes leave one interval row `src: Technical requirements, interval row exists afterwards`
- [ ] `C-TR-27` `constraint` An interval with a different quantity for an existing key is refused `src: Technical requirements, is a client bug and hiding it makes it permanent`
- [ ] `C-TR-28` `constraint` A repeated idempotency key with the same body creates no second row `src: Technical requirements, row, a second audit event or a second outbound event`
- [ ] `C-TR-29` `constraint` A repeated idempotency key with a different body answers 409 Conflict `src: Technical requirements, A repeat with the same key and a different body returns 409 Conflict`
- [ ] `C-TR-30` `constraint` A cursor walk returns every row once during inserts `src: Technical requirements, returns every row exactly once and never repeats one`
- [ ] `C-TR-31` `contract` A page carries next_cursor, has_more, page_size with no total_count `src: Technical requirements, the response echoes the size it used as page_size`
- [ ] `C-TR-32` `constraint` The page size runs from 1 to 100 `src: Technical requirements, between 1 and 100`
- [ ] `C-TR-33` `contract` Every response carries X-Request-Id echoing a supplied value `src: Technical requirements, has its value echoed rather than replaced`
- [ ] `C-TR-34` `contract` Every error body carries the request_id `src: Technical requirements, Every error body carries the same value under request_id`
- [ ] `C-TR-35` `contract` The audit hash chains from sixty four zeroes over canonical payloads `src: Technical requirements, event in an organisation's chain uses a prev_hash of sixty four zeroes`
- [ ] `C-TR-36` `constraint` The audit sequence stays gapless under concurrent writes `src: Technical requirements, so a missing event is detectable`
- [ ] `C-TR-37` `constraint` The application credential cannot update an audit_event row `src: Technical requirements, unable to update or delete a row of audit_event`
- [ ] `C-TR-38` `capability` A refusal event carries outcome denied with the error code as reason `src: Technical requirements, A refusal's event carries outcome denied`
- [ ] `C-TR-39` `capability` An inspector read under a grant carries the access request identifier `src: Technical requirements, carries that access request's identifier as its reason`
- [ ] `C-TR-40` `constraint` A private or loopback destination is refused at creation `src: Technical requirements, resolves to a loopback or private network range, is refused at creation`
- [ ] `C-TR-41` `constraint` The delivery signature covers the timestamp `src: Technical requirements, delivery captured today and replayed next week is rejectable by the consumer`
- [ ] `C-TR-42` `constraint` The retry ladder starts immediately then waits five seconds `src: Technical requirements, The retry ladder is immediately, then 5s, 5m`
- [ ] `C-TR-43` `constraint` A replay reuses the original event identifier `src: Technical requirements, a replay reuses the original event identifier`
- [ ] `C-TR-44` `constraint` Document change events collapse per room `src: Technical requirements, that ceiling is per room and never global`
- [ ] `C-TR-45` `contract` Approval request mail reaches every eligible approver except the requester `src: Technical requirements, every eligible approver except the requester`
- [ ] `C-TR-46` `constraint` Mail goes out as one message per recipient `src: Technical requirements, One message per recipient, no cc and no bcc`
- [ ] `C-TR-47` `constraint` Moving a request to executed sends no mail `src: Technical requirements, sends nothing at all`
- [ ] `C-TR-48` `contract` The not-found route answers 404 `src: Technical requirements, answers with status 404`
- [ ] `C-TR-49` `contract` The favicon is declared in every document head `src: Technical requirements, is declared in the head of every document`
- [ ] `C-TR-50` `constraint` Page views are readable by an owner alone `src: Technical requirements, returns them to an owner and to nobody else`
- [ ] `C-TR-51` `constraint` An enquiry filling the decoy field is refused `src: Technical requirements, which no person can see`
- [ ] `C-TR-52` `constraint` No credential appears in anything the browser downloads `src: Technical requirements, No credential, secret key, client secret or database address appears`
- [ ] `C-TR-53` `constraint` Deletion under a legal hold is refused for an owner `src: Technical requirements, deletion is refused everywhere including for an owner`
- [ ] `C-TR-54` `constraint` A retired key closes its connections `src: Technical requirements, key revoked | within 30s, connections closed`
- [ ] `C-TR-55` `constraint` A retired key mints no identity token `src: Technical requirements, a retired key is 401 key_retired`
- [ ] `C-TR-56` `constraint` A group membership change reaches open connections within five seconds `src: Technical requirements, group membership changed | within 5s`
- [ ] `C-TR-57` `constraint` A second environment of one kind in a project is refused `src: Technical requirements, a second environment of one kind is 409 environment_exists`
- [ ] `C-TR-58` `constraint` A resource owned by another organisation answers not_found `src: Technical requirements, or that the caller's organisation does not own`
- [ ] `C-TR-59` `constraint` A role lacking a permission answers forbidden `src: Technical requirements, A principal whose role does not carry the permission`
- [ ] `C-TR-60` `constraint` A decision by an ineligible principal answers approver_not_eligible `src: Technical requirements, A principal who is neither eligible nor the requester`
- [ ] `C-TR-61` `constraint` A second decision by one approver is refused `src: Technical requirements, A second decision by the same approver`
- [ ] `C-TR-62` `capability` The seeded revocation request executes through the console `src: Technical requirements, One request is seeded in pending`
- [ ] `C-TR-63` `capability` A second factor code is mailed to the challenged member `src: Technical requirements, a six digit code is mailed to the member`
- [ ] `C-TR-64` `constraint` An expired request refuses execution `src: Technical requirements, Executing it returns 409 with code request_expired`
- [ ] `C-TR-65` `constraint` An expiry mail reaches the requester once `src: Technical requirements, within one minute of expiry, exactly once`
- [ ] `C-TR-66` `constraint` Two executions of one approved request arriving together run the change once `src: Technical requirements, run the change once: exactly one answers `200``
- [ ] `C-TR-67` `constraint` Two eligible approvers deciding at the same moment are both recorded `src: Technical requirements, neither decision overwrites the other`
- [ ] `C-TR-68` `constraint` Connections arriving together are admitted only up to the room ceiling `src: Technical requirements, exactly as many are admitted as fit`
- [ ] `C-TR-69` `constraint` The same room identifier, meter plus start in another environment is a different interval `src: Technical requirements, in another environment is a different interval`
- [ ] `C-TR-70` `constraint` A meter line rounds half up once on the period quantity `src: Technical requirements, the rounding happens once per line and never per interval`
- [ ] `C-TR-71` `constraint` An approved deletion of a held room is refused at execution `src: Technical requirements, executing an approved deletion of a held room answers `409``
- [ ] `C-TR-72` `constraint` Break glass cannot delete a room under a legal hold `src: Technical requirements, Break glass is no way around a hold either`
- [ ] `C-TR-73` `constraint` A second factor code serves only the member the code was mailed to `src: Technical requirements, A second factor code serves only the member it was mailed to`
- [ ] `C-TR-74` `contract` A stale room version marker answers 409 version_conflict carrying the current room `src: Technical requirements, a stale marker answers `409` with code `version_conflict``
- [ ] `C-TR-75` `contract` A cursor presented under a different filter or order answers 422 cursor_invalid `src: Technical requirements, a cursor presented with a different filter or order answers `422``
- [ ] `C-TR-76` `contract` A room identifier is not reused within 24 hours of deletion `src: Technical requirements, is not reused within 24 hours of its room's deletion`
- [ ] `C-TR-77` `constraint` An idempotency key is scoped to the credential presenting the key `src: Technical requirements, A key is scoped to the credential presenting it`
- [ ] `C-TR-78` `constraint` The room named at admission is looked up in the environment of the minting secret key `src: Technical requirements, The room named at admission is looked up in the secret key's environment`

## C-DM Data model

- [ ] `C-DM-01` `data` The audit_event columns carry the chain key names `src: Data model, columns are named exactly as the chain keys`
- [ ] `C-DM-02` `data` An open connection carries no close time `src: Data model, An open connection is one whose closed at is absent`
- [ ] `C-DM-03` `data` Environment is unique on project plus kind `src: Data model, has exactly one production environment`
- [ ] `C-DM-04` `data` A production secret is never stored in the clear `src: Data model, a production secret cannot be stored in the clear`
- [ ] `C-DM-05` `data` The usage interval key stores a retried write once `src: Data model, makes a retried write store once`
- [ ] `C-DM-06` `data` An outbox row is written in the transaction of the change `src: Data model, A row is written in the same transaction as the change it describes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The display face is a geometric grotesque substitute for Suisse Intl `src: Front-end specification, Substitute a geometric grotesque carrying 400, 500 and 600`
- [ ] `C-FE-02` `ui` Inter sets long form body `src: Front-end specification, long form body, documentation`
- [ ] `C-FE-03` `ui` JetBrains Mono sets the letterspaced eyebrow `src: Front-end specification, monospace, uppercase, widely letterspaced eyebrow`
- [ ] `C-FE-04` `ui` Each feature route re-tints with the feature hue `src: Front-end specification, that hue re-themes the whole of its route`
- [ ] `C-FE-05` `ui` The copilot hue sits outside the accent family `src: Front-end specification, the only accent outside the family`
- [ ] `C-FE-06` `ui` Load bearing clauses are set in white inside grey paragraphs `src: Front-end specification, load bearing clauses are set in white at the same size and weight`
- [ ] `C-FE-07` `ui` The demonstration surface is a live composition `src: Front-end specification, It is a live composition of real interface furniture`
- [ ] `C-FE-08` `ui` Cursor badges travel curves between resting places `src: Front-end specification, travels a continuous curve between rest points`
- [ ] `C-FE-09` `ui` Header menu triggers open panels by keyboard `src: Front-end specification, Each trigger is a button with an expanded state, not a link`
- [ ] `C-FE-10` `ui` The comparison matrix becomes one panel per plan at the narrow width `src: Front-end specification, one panel per plan with the group headings repeated inside each`
- [ ] `C-FE-11` `ui` The documentation subsite runs on a light ground `src: Front-end specification, It runs on a light ground with its own chrome`
- [ ] `C-FE-12` `ui` Destructive confirmations tier by blast radius `src: Front-end specification, decided by blast radius`
- [ ] `C-FE-13` `ui` The not-authorised state offers request access `src: Front-end specification, offers one action, request access`
- [ ] `C-FE-14` `ui` Production carries a persistent tinted band `src: Front-end specification, production carries a persistent tinted band across the top of the context bar`
- [ ] `C-FE-15` `ui` The header collapses behind an Open menu control below the medium width `src: Front-end specification, collapses into one control named Open menu`
- [ ] `C-FE-16` `contract` Each matrix cell carries data-entitlement `src: Front-end specification, Each cell that renders an entitlement carries data-entitlement`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` A sequential identifier handed to a client is a contract violation `src: Constraints, a sequential one is a contract violation`
- [ ] `C-CN-02` `constraint` Seeding creates each seeded row once `src: Constraints, restarting must not create a second seeded row`
- [ ] `C-CN-03` `constraint` The record of who did what is append only `src: Constraints, The record of who did what is append only`
- [ ] `C-CN-04` `constraint` Money is integer minor units in usd `src: Constraints, Money is integer minor units in usd`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` GET /api/health returns 200 `src: Deployment contract, GET /api/health returns 200 once the app is ready`
- [ ] `C-DC-02` `contract` The server answers from outside its container after the session ends `src: Deployment contract, The server must keep running after this session ends and must not be a child of the shell`
- [ ] `C-DC-03` `contract` The server binds 0.0.0.0 `src: Deployment contract, Bind 0.0.0.0, never 127.0.0.1 or localhost`
- [ ] `C-DC-04` `contract` The HTTP API is served under the /api prefix `src: Deployment contract, The HTTP API is served on that same origin under the /api prefix`

## Pinned literals

- `deku-demo-pw-2026` the password of every seeded account
- `4173` the container-internal port
- `197630` the seeded Northlake invoice total for period 2026-09
- `grp-northlake-contractors` the directory group the seeded request revokes
- `hold-hollow-2026` the legal hold on doc-hollow-dispute

### Referenced but not pinned

- the exact colour values, carried by family plus tone plus shade
- the exact motion curves and durations, carried in words

## Coverage ledger

- sections carried: 10
- obligations recorded: 173
