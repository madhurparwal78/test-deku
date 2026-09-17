# Checklist: Agentic Support Workspace

Items: 182
Unpinned values flagged: 0
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-CN, C-DC

---

## C-OV Overview

- [ ] `C-OV-01` `capability` One shared workspace holds every customer conversation from every channel in a single list worked by the whole team. `src: Overview paragraph 1`
- [ ] `C-OV-02` `capability` Reach is a relationship rather than a rank, so a manager reaches only the teams led by that manager. `src: Overview paragraph 4`
- [ ] `C-OV-03` `constraint` A record outside a reader's reach is reported as absent rather than refused. `src: Overview paragraph 4`
- [ ] `C-OV-04` `capability` Customers never sign in to the workspace; customers read the public help surface instead. `src: Overview paragraph 2`

---

## C-RL User roles

- [ ] `C-RL-01` `role` Three roles exist in the workspace: `admin`, `manager`, `teammate`. `src: User roles table`
- [ ] `C-RL-02` `constraint` Signup is closed: no public registration route exists, no self-service account creation exists. `src: User roles paragraph 1`
- [ ] `C-RL-03` `role` An `admin` reads every conversation, article, team, teammate, report in the workspace. `src: User roles table row admin`
- [ ] `C-RL-04` `role` A `manager` reads conversations for the teams led by that manager, plus conversations assigned to that manager. `src: User roles table row manager`
- [ ] `C-RL-05` `role` A `teammate` reads conversations in the teams that teammate belongs to, plus conversations assigned to that teammate. `src: User roles table row teammate`
- [ ] `C-RL-06` `role` A `teammate` cannot open any settings screen. `src: User roles table row teammate`
- [ ] `C-RL-07` `role` A `manager` cannot invite a teammate, cannot change anybody's role. `src: User roles table row manager`
- [ ] `C-RL-08` `capability` Reach is recomputed from current membership on every request rather than carried in the session. `src: User roles paragraph after table`
- [ ] `C-RL-09` `contract` A direct call from a `teammate` session to an `admin`-only endpoint is denied by the server, leaving the protected state unchanged. `src: User roles authorization paragraph`
- [ ] `C-RL-10` `literal` Four accounts are seeded: `admin@example.com`, `manager@example.com`, `teammate@example.com`, `teammate2@example.com`. `src: User roles seeded accounts table`
- [ ] `C-RL-11` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles password line`
- [ ] `C-RL-12` `role` Opening a settings screen as a `teammate` is refused plainly, naming the role able to grant access. `src: User roles reads paragraph`

---

## C-CF Core features

- [ ] `C-CF-01` `contract` Sign-in with a correct address plus password returns a bearer token with the signed-in person's identity, role, teams. `src: Core features Auth rule 1`
- [ ] `C-CF-02` `contract` Sign-in with a wrong password is rejected as invalid. `src: Core features Auth rule 2`
- [ ] `C-CF-03` `contract` Sign-in with an address that has no account is rejected as invalid by the same message, the same visible path. `src: Core features Auth rule 2`
- [ ] `C-CF-04` `constraint` No signup route exists, no password reset route exists; any other route that would create an account is rejected as invalid. `src: Core features Auth rule 3`
- [ ] `C-CF-05` `contract` Signing out revokes the bearer token; a later request carrying that token is rejected as unauthorized. `src: Core features Auth rule 4`
- [ ] `C-CF-06` `capability` Removing somebody from a team takes effect on the very next request made by that person. `src: Core features Auth rule 5`
- [ ] `C-CF-07` `capability` The inbox offers six views: `Your inbox`, `Mentions`, `Created by you`, `All`, `Unassigned`, one view per readable team. `src: Core features inbox views table`
- [ ] `C-CF-08` `constraint` A view grants no access: the count beside a view name is computed after reach is applied. `src: Core features inbox rule 1`
- [ ] `C-CF-09` `capability` Each list row shows a generated avatar, the contact name, a plain-text preview of the most recent part, the relative age, the channel as a labelled glyph, the service level state. `src: Core features inbox rule 2`
- [ ] `C-CF-10` `capability` Unread is carried by a marker rather than by a change of type strength alone. `src: Core features inbox rule 2`
- [ ] `C-CF-11` `capability` Filtering, sorting, search appear as visible controls at the top of the list. `src: Core features inbox rule 3`
- [ ] `C-CF-12` `contract` Search is scoped to the workspace with reach applied before ranking rather than after. `src: Core features inbox rule 4`
- [ ] `C-CF-13` `contract` The applied filters plus the sort are part of the address, so opening that address restores exactly the same list. `src: Core features inbox rule 3`
- [ ] `C-CF-14` `capability` Opening a conversation changes the address without rebuilding the list, keeping the scroll position plus the selection. `src: Core features inbox rule 5`
- [ ] `C-CF-15` `literal` The first-run empty inbox reads `No conversations yet. Connect a channel to start receiving them.` `src: Core features inbox rule 7`
- [ ] `C-CF-16` `literal` The filtered empty inbox reads `No conversations match these filters.` `src: Core features inbox rule 7`
- [ ] `C-CF-17` `literal` The cleared empty inbox reads `You are all caught up.` `src: Core features inbox rule 7`
- [ ] `C-CF-18` `capability` Teammates looking at the same conversation appear on that conversation by generated avatar; the customer never sees the presence signal. `src: Core features inbox rule 8`
- [ ] `C-CF-19` `data` A conversation is an ordered stream of typed parts ordered by the conversation's own sequence number rather than by timestamp. `src: Core features conversation paragraph 1`
- [ ] `C-CF-20` `capability` The composer has exactly two modes, `Reply` plus `Note`, shown on different grounds, with a confirmation when switching from `Note` to `Reply` with content typed. `src: Core features conversation rule 1`
- [ ] `C-CF-21` `constraint` A note is internal, so a note can never reach a customer. `src: Core features conversation rule 1`
- [ ] `C-CF-22` `capability` The send control offers three choices: a plain send, a send that closes the conversation, a send that snoozes the conversation. `src: Core features conversation rule 3`
- [ ] `C-CF-23` `capability` A part that fails to send stays in the thread marked as failed, carrying the reason, offering a retry. `src: Core features conversation rule 4`
- [ ] `C-CF-24` `data` Submitting the same send attempt twice under one client key appends exactly one part. `src: Core features conversation rule 5`
- [ ] `C-CF-25` `capability` An unsent draft survives navigating away, a reload, a crash, per conversation per person. `src: Core features conversation rule 6`
- [ ] `C-CF-26` `constraint` No role may remove a conversation or a part; a superseding part is written instead. `src: Core features conversation rule 8`
- [ ] `C-CF-27` `constraint` A reply written by Auto Agent always carries the agent name, never a person's name. `src: Core features conversation rule 10`
- [ ] `C-CF-28` `data` The conversation state machine moves `open` to `snoozed` to `open`, plus `open` or `snoozed` to `closed`, reopening on a customer reply. `src: Core features conversation rule 12`
- [ ] `C-CF-29` `data` Closing sets the resolver to `agent` when the last substantive reply came from Auto Agent, otherwise to `human`. `src: Core features conversation rule 12`
- [ ] `C-CF-30` `capability` An agent run retrieves only `published` articles; a `draft`, `in_review`, `unpublished`, `archived` article is never retrieved. `src: Core features Auto Agent rule 2`
- [ ] `C-CF-31` `constraint` An article in a collection whose audience is `internal` is never used to answer a customer. `src: Core features Auto Agent rule 2`
- [ ] `C-CF-32` `literal` Each reasoning disclosure is titled `Auto Agent's thoughts (Step 1)` with the step number counting from one. `src: Core features Auto Agent rule 3`
- [ ] `C-CF-33` `capability` Each tool call appends a row carrying a short label plus the exact arguments expandable beside the label. `src: Core features Auto Agent rule 4`
- [ ] `C-CF-34` `literal` The write tool `issue_credit` runs automatically only at or below `5000` minor units of `usd`. `src: Core features Auto Agent rule 5`
- [ ] `C-CF-35` `capability` An amount above the approval ceiling produces a handover rather than a refusal to the customer. `src: Core features Auto Agent rule 5`
- [ ] `C-CF-36` `contract` A customer message asking Auto Agent to change the agent's own rules is answered as an ordinary customer message, flagged on the run, changing nothing about what the agent does. `src: Core features Auto Agent rule 8`
- [ ] `C-CF-37` `literal` A handover tells the customer `Connecting you with a specialist who can help.` `src: Core features Auto Agent rule 9`
- [ ] `C-CF-38` `data` Triggering Auto Agent twice on the same customer message produces exactly one run, exactly one reply or exactly one handover. `src: Core features Auto Agent rule 11`
- [ ] `C-CF-39` `literal` A summary card is titled `Summary`, drawn only from parts in the same conversation. `src: Core features Auto Agent rule 13`
- [ ] `C-CF-40` `data` Publishing an article writes a new version with an incremented version number, pointing the article at the new version as current. `src: Core features knowledge hub rule 1`
- [ ] `C-CF-41` `role` Only an `admin` may publish or unpublish an article; a `manager` attempt leaves the article state unchanged. `src: Core features knowledge hub rule 2`
- [ ] `C-CF-42` `literal` Gap kinds are labelled `CONTENT GAP`, `CUSTOMER DATA GAP`, `ACTION GAP` with a badge reading `High`, `Medium`, or `Low`. `src: Core features knowledge hub rule 5`
- [ ] `C-CF-43` `data` A gap is created whenever an agent run hands over, carrying the handover reason as the rationale. `src: Core features knowledge hub rule 5`
- [ ] `C-CF-44` `data` The matched service level policy identifier is recorded on the conversation at creation, so a later policy edit changes nothing already in flight. `src: Core features service levels rule 1`
- [ ] `C-CF-45` `data` The first-response moment is recorded once, never rewritten by a later reply. `src: Core features service levels rule 2`
- [ ] `C-CF-46` `data` A breach is recorded once per conversation per target, appending exactly one `sla_event` part however many sweeps pass over the conversation. `src: Core features service levels rule 5`
- [ ] `C-CF-47` `constraint` A breach sends no message; service level state surfaces in the product instead. `src: Core features service levels rule 6`
- [ ] `C-CF-48` `capability` An `admin` invites a teammate by address from a modal, choosing a role plus optionally a team. `src: Core features teammates rule 1`
- [ ] `C-CF-49` `data` At most one active invitation exists per address per workspace; a second invitation invalidates the earlier token. `src: Core features teammates rule 2`
- [ ] `C-CF-50` `contract` Inviting an address that already holds an active membership is refused as invalid, creating nothing. `src: Core features teammates rule 2`
- [ ] `C-CF-51` `data` Accepting an invitation activates the membership, adds the person to the chosen team, consumes the token; a second presentation of the same token is refused as invalid. `src: Core features teammates rule 3`
- [ ] `C-CF-52` `contract` A request that would raise somebody to a role at or above the granter's own is denied at the server, leaving the membership unchanged. `src: Core features teammates rule 4`
- [ ] `C-CF-53` `contract` The last active `admin` membership can be neither demoted nor deactivated. `src: Core features teammates rule 4`
- [ ] `C-CF-54` `capability` Routing sets the conversation team, clears any assignee, appends an `assignment` part naming who routed the conversation, from where, to where. `src: Core features teammates rule 5`
- [ ] `C-CF-55` `contract` A `teammate` may not route a conversation; a direct request naming a team outside that person's reach is denied with the conversation unchanged. `src: Core features teammates rule 5`
- [ ] `C-CF-56` `data` Two simultaneous claims of one unassigned conversation produce exactly one assignee, exactly one `assignment` part, with the loser told the conversation is already taken. `src: Core features teammates rule 6`
- [ ] `C-CF-57` `literal` An invitation message carries a subject beginning `Support workspace invitation:` followed by one space then the workspace name. `src: Core features notification rule 1`
- [ ] `C-CF-58` `contract` An invitation message is delivered to the invited address alone, carrying no carbon copy, no blind carbon copy. `src: Core features notification rule 1`
- [ ] `C-CF-59` `literal` A handover message carries a subject beginning `Handover needed:` followed by one space then the conversation subject. `src: Core features notification rule 2`
- [ ] `C-CF-60` `contract` A handover message is delivered to the lead of the receiving team alone, falling back to the administrator when the team has no lead. `src: Core features notification rule 2`
- [ ] `C-CF-61` `constraint` Replying, closing, reopening, snoozing, assigning, routing, publishing, changing a role, breaching a target: none of those sends any message. `src: Core features notification rule 3`
- [ ] `C-CF-62` `capability` The report states resolved conversations, the resolution rate split into agent-resolved plus human-resolved, service level attainment per target, the at-risk count, the breached count. `src: Core features reporting rule 1`
- [ ] `C-CF-63` `contract` The same date range read by a `manager` returns different totals from the same range read by an `admin`, each scoped to the reader's reach. `src: Core features reporting rule 2`
- [ ] `C-CF-64` `capability` Response times are reported as the median plus the ninety-fifth percentile rather than as a mean. `src: Core features reporting rule 3`
- [ ] `C-CF-65` `capability` Every reported figure states the time zone used plus the age of the data. `src: Core features reporting rule 4`
- [ ] `C-CF-66` `contract` An article that is not `published`, or that lives in an `internal` collection, answers not-found when requested on the public help surface. `src: Core features public help rule 2`
- [ ] `C-CF-67` `capability` An address matching no route renders the product's own not-found page carrying a way back, answering not-found. `src: Core features public help rule 3`
- [ ] `C-CF-68` `capability` The onboarding list above the inbox derives completion from the state of the system rather than from a stored flag. `src: Core features onboarding rule 1`
- [ ] `C-CF-69` `data` Every write records the acting principal, the principal kind, the action as an audit entry with no update path, no removal path. `src: Core features onboarding rule 3`

---

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated request for a workspace route lands on `/signin`, remembering the requested address, restoring the address after a successful sign-in. `src: User flow entry paragraph`
- [ ] `C-UF-02` `contract` A successful sign-in lands on `/w/northwind/inbox`. `src: User flow entry paragraph`
- [ ] `C-UF-03` `contract` A conversation identifier outside the reader's reach renders the not-found page, answering not-found rather than a refusal. `src: User flow entry paragraph`
- [ ] `C-UF-04` `contract` Every workspace route requires a session; the public help routes plus `/signin` plus `/invite/<token>` require none. `src: User flow route table`
- [ ] `C-UF-05` `capability` The administrator opens the teammates screen, presses `Invite teammate`, submits an address with a role plus a team, sees an inline banner confirming the invitation without leaving the screen. `src: User flow journey one`
- [ ] `C-UF-06` `capability` The invited row appears with status `invited` until the invitation link is opened, at which point the membership becomes `active`. `src: User flow journey one`
- [ ] `C-UF-07` `capability` The administrator opens `Invoice shows the wrong tax rate`, presses `Route to team`, chooses `Billing Support`, whereupon the conversation appears in that team inbox view. `src: User flow journey one`
- [ ] `C-UF-08` `capability` A teammate switches to `Unassigned`, opens `Refund for duplicate charge`, presses `Assign to me`, becoming the assignee. `src: User flow journey two`
- [ ] `C-UF-09` `capability` A teammate typing a reply then choosing the send that closes leaves the conversation `closed` with the resolver `human`. `src: User flow journey two`
- [ ] `C-UF-10` `capability` A teammate in `Billing Support` opening `Cannot reset my password` is shown the not-found page. `src: User flow journey two`
- [ ] `C-UF-11` `capability` Pressing `Ask Auto Agent` on `Refund for duplicate charge` adds a collapsed reasoning disclosure, a tool-call row, a reply grounded in the published refunds article. `src: User flow journey three`
- [ ] `C-UF-12` `capability` Pressing `Ask Auto Agent` on `Invoice shows the wrong tax rate` writes a `Summary` card plus a handover divider naming the reason plus the receiving team, posting no other reply. `src: User flow journey three`
- [ ] `C-UF-13` `capability` The reports screen read as `manager@example.com` covers `Billing Support` alone, differing from the same screen read as `admin@example.com`. `src: User flow journey four`
- [ ] `C-UF-14` `ui` Every list draws skeleton rows at the true row height on first load so nothing shifts when the data arrives. `src: User flow states paragraph`

---

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The north star is comprehension: a working queue owned by a team, every row a person waiting. `src: UI/UX notes paragraph 1`
- [ ] `C-UX-02` `ui` The register is an operational tool: quiet, dense but organised, with no oversized hero, no editorial composition, no decoration standing in for content. `src: UI/UX notes paragraph 1`
- [ ] `C-UX-03` `ui` Colour, type, spacing are declared once as named tokens in three layers, with a component reading only the third layer. `src: UI/UX notes token layer paragraph`
- [ ] `C-UX-04` `ui` The public help surface sits on a warm near-white neutral with a near-black warm neutral as the darkest text. `src: UI/UX notes two surfaces paragraph`
- [ ] `C-UX-05` `ui` The workspace sits on a near-black cool neutral ground with panels one step off the ground, text running from white through a light cool neutral to a mid cool neutral. `src: UI/UX notes two surfaces paragraph`
- [ ] `C-UX-06` `ui` Interaction carries a mid, vivid blue as the only colour a person can press, with the focus ring in the same blue on every ground. `src: UI/UX notes palette paragraph`
- [ ] `C-UX-07` `ui` Product identity carries a second, deeper vivid blue that never appears on a control. `src: UI/UX notes palette paragraph`
- [ ] `C-UX-08` `ui` Auto Agent carries a mid, vivid orange appearing nowhere except where the agent is the author or the subject. `src: UI/UX notes palette paragraph`
- [ ] `C-UX-09` `ui` Three colours carry state exclusively: a mid, vivid red for failure, a mid, vivid green for success, a light, vivid amber for work in progress. `src: UI/UX notes palette paragraph`
- [ ] `C-UX-10` `ui` The interface, the navigation, every control are set in a geometric grotesque with a tall x-height, at a regular plus a medium stroke. `src: UI/UX notes type paragraph`
- [ ] `C-UX-11` `ui` Reading copy on the public help surface is set in a light transitional serif; a monospace is reserved for uppercase eyebrow labels. `src: UI/UX notes type paragraph`
- [ ] `C-UX-12` `ui` Figures line up in a column wherever counts, ages, durations stack. `src: UI/UX notes type paragraph`
- [ ] `C-UX-13` `ui` Corners are barely softened, with the only fully round shape being a person's avatar. `src: UI/UX notes shape paragraph`
- [ ] `C-UX-14` `ui` Elevation is carried by a hairline border plus a change of ground tone rather than by shade; nothing floats. `src: UI/UX notes shape paragraph`
- [ ] `C-UX-15` `ui` Workspace rows sit close enough that a full queue reads in one screen, with every gap a multiple of one base unit. `src: UI/UX notes shape paragraph`
- [ ] `C-UX-16` `ui` Every glyph is drawn in the build, with no icon font, no icon image file, no external icon package. `src: UI/UX notes iconography paragraph`
- [ ] `C-UX-17` `ui` Every icon-only control carries a text label always available to assistive technology. `src: UI/UX notes iconography paragraph`
- [ ] `C-UX-18` `ui` Everything eases at one speed on one curve for anything a pointer causes; nothing overshoots. `src: UI/UX notes motion paragraph`
- [ ] `C-UX-19` `ui` Pointing at a link grows a hairline beneath the link from left to right without shifting the layout. `src: UI/UX notes motion paragraph`
- [ ] `C-UX-20` `ui` The primary control's ground changes from near-black to the product identity blue when pointed at. `src: UI/UX notes motion paragraph`
- [ ] `C-UX-21` `ui` Under a reduced-motion preference the sweep stops, the scroll progress indicator is removed, the settle resolves immediately, with link underlines, focus rings, state changes all kept. `src: UI/UX notes motion paragraph`
- [ ] `C-UX-22` `ui` One primary action style plus one quieter alternative, each carrying resting, pointed-at, pressed, focused, unavailable states, with unavailable never signalled by colour alone. `src: UI/UX notes components paragraph`
- [ ] `C-UX-23` `ui` Forms validate first when a field is left, then on every change once a field is marked invalid, with the submit control never disabled. `src: UI/UX notes components paragraph`
- [ ] `C-UX-24` `ui` Every data-bearing surface implements seven states, keeping the two loading states distinct. `src: UI/UX notes seven states paragraph`
- [ ] `C-UX-25` `ui` The workspace is a narrow permanent icon rail, a resizable list, a working area that splits into the thread plus a collapsible details panel. `src: UI/UX notes layout paragraph`
- [ ] `C-UX-26` `ui` The rail never changes width, never reorders itself by frequency. `src: UI/UX notes layout paragraph`
- [ ] `C-UX-27` `ui` At a narrow viewport nothing overflows sideways, with every navigation target still reachable. `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-28` `ui` Touch targets are at least 44 by 44 pixels wherever the pointer is coarse. `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-29` `ui` Contrast meets WCAG 2.1 level AA on both palettes: at least 4.5 to 1 for body text, at least 3 to 1 for large text. `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-30` `ui` Full keyboard navigation reaches every control with a visible focus ring, no positive tab order, focus never lost to the page body after an action. `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-31` `ui` Meaning is never carried by colour alone: unread carries a marker, service level state carries a word, agent replies carry the agent name. `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-32` `ui` Every content image carries alternative text saying what the image conveys; a purely decorative image declares itself decorative. `src: UI/UX notes accessibility paragraph`

---

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The workspace plus the public help surface are rendered on the server with interactive islands hydrated, so the browser receives rendered markup on first paint. `src: Technical requirements paragraph 1`
- [ ] `C-TR-02` `contract` The JSON interface is served by Express under the `/api` prefix on the same origin. `src: Technical requirements paragraph 1`
- [ ] `C-TR-03` `contract` The store is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements paragraph 1`
- [ ] `C-TR-04` `contract` Mail leaves over SMTP to Mailpit at `SMTP_HOST` plus `SMTP_PORT` with `SMTP_USER` plus `SMTP_PASS`. `src: Technical requirements paragraph 1`
- [ ] `C-TR-05` `constraint` No host, port, address, credential is written into the source; every one is read from the environment. `src: Technical requirements paragraph 1`
- [ ] `C-TR-06` `contract` Passwords are stored hashed; the bearer token carries identity, with role plus teams resolved per request from current state. `src: Technical requirements paragraph 2`
- [ ] `C-TR-07` `contract` Requests are logged as structured records carrying the method, the route, the outcome, a request identifier, with no password, no token appearing in a log line. `src: Technical requirements paragraph 3`
- [ ] `C-TR-08` `constraint` Nothing the browser downloads contains a credential, an interface key, an administrative token. `src: Technical requirements paragraph 4`
- [ ] `C-TR-09` `contract` The app serves a favicon declared in the document head of every route. `src: Technical requirements paragraph 4`
- [ ] `C-TR-10` `contract` Every public route declares a social preview title plus a preview image that resolves to a real response. `src: Technical requirements paragraph 4`
- [ ] `C-TR-11` `constraint` The only backing services available are PostgreSQL plus Mailpit; reaching for a second database, cache, queue, object store, identity provider, mail vendor is a contract violation. `src: Technical requirements final paragraph`

---

## C-DM Data model

- [ ] `C-DM-01` `data` Fifteen tables carry the model, with all timestamps in UTC. `src: Data model opening`
- [ ] `C-DM-02` `data` Every table except `workspace` plus `app_user` carries a non-nullable `workspace_id`. `src: Data model tenancy paragraph`
- [ ] `C-DM-03` `data` `conversation_part.seq` counts from one within a conversation, allocated by the store, unique on `conversation_id` with `seq`. `src: Data model conversation_part paragraph`
- [ ] `C-DM-04` `data` Every enumeration is a constrained set of values at the database rather than a free string. `src: Data model opening`
- [ ] `C-DM-05` `data` `article_version` is unique on `article_id` with `version`, holding the body that never lives on the article row. `src: Data model article paragraph`
- [ ] `C-DM-06` `data` `agent_run.idempotency_key` is unique, derived from the triggering part. `src: Data model agent_run paragraph`
- [ ] `C-DM-07` `data` `agent_step.citation_article_version_ids` names exact article versions rather than articles. `src: Data model agent_step paragraph`
- [ ] `C-DM-08` `data` `audit_entry` is append only, with no update path, no removal path in the application. `src: Data model audit_entry paragraph`
- [ ] `C-DM-09` `data` Removal is a state change on the record; deactivating a teammate keeps the record, returning assigned conversations to the team queue. `src: Data model invariant 9`
- [ ] `C-DM-10` `literal` The seeded workspace is `Northwind Trading` at slug `northwind`, with teams `Billing Support` plus `Technical Support`. `src: Data model seed data`
- [ ] `C-DM-11` `literal` Three conversations are seeded: `Refund for duplicate charge`, `Cannot reset my password`, `Invoice shows the wrong tax rate`. `src: Data model seed data table`
- [ ] `C-DM-12` `literal` Four articles are seeded: two published for customers, one left unpublished as a draft, one restricted to the internal collection. `src: Data model seed data articles`
- [ ] `C-DM-13` `literal` One service level policy is seeded, `Standard support`, with a first response target of `60` minutes plus a resolution target of `480` minutes. `src: Data model seed data policy`
- [ ] `C-DM-14` `data` Seeding is idempotent: restarting the app duplicates no row. `src: Data model seed data closing`
- [ ] `C-DM-15` `data` Identifiers are non-sequential, so a count cannot be inferred from one identifier. `src: Data model opening`
- [ ] `C-DM-16` `data` The relative age shown in the list is derived on read from `waiting_since` rather than stored. `src: Data model conversation paragraph`

---

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One workspace exists, with no workspace switcher, no second tenant, yet every tenant-scoped read is still constrained on the workspace. `src: Constraints paragraph 1`
- [ ] `C-CN-02` `constraint` Billing of every kind is absent: trials, plans, invoices, spend caps. `src: Constraints paragraph 2`
- [ ] `C-CN-03` `constraint` No live connection pushes changes to an idle screen; the interface refreshes on navigation, on action completion. `src: Constraints paragraph 3`
- [ ] `C-CN-04` `constraint` No external network call is made at run time. `src: Constraints paragraph 4`
- [ ] `C-CN-05` `constraint` The app stays responsive with `2000` conversations, up to `50` parts each, `25` teammates. `src: Constraints paragraph 6`
- [ ] `C-CN-06` `constraint` The product is a web application, with no native application. `src: Constraints paragraph 5`

---

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`, with the port mapping `${APP_PUBLIC_PORT}:4173` read from the environment. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` A production build is served behind a static or preview server rather than a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, never as a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0` rather than `127.0.0.1` or `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `constraint` The backing services are already running; no copy of either is downloaded, installed, compiled, started. `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `constraint` No persistent volume, no fixed container name, no custom network is declared. `src: Deployment contract bullet 12`
- [ ] `C-DC-12` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-13` `contract` An invalid or unauthorized call is rejected as a client error rather than a server error, never as a silent success. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-14` `contract` Bearer auth is required on everything except `POST /api/auth/login`, `GET /api/health`, the public help routes. `src: Deployment contract API shapes paragraph`
- [ ] `C-DC-15` `contract` `POST /api/conversations/{id}/parts` accepts `kind`, `body`, `client_key`, returning the created part with `seq` plus `delivery_state`. `src: Deployment contract API table`
- [ ] `C-DC-16` `contract` `GET /api/reports/resolution` returns `resolved_total`, `resolved_by_agent`, `resolved_by_human`, `resolution_rate`, `attainment_first_response`, `attainment_resolution`, `at_risk`, `breached`, `timezone`, `data_age_seconds`, `final_period_partial`. `src: Deployment contract API table`
- [ ] `C-DC-17` `contract` A message recorded by the app without a matching delivered message in Mailpit is a contract violation. `src: Deployment contract no mocks paragraph`
- [ ] `C-DC-18` `constraint` Every conversation, part, membership, invitation, article version, audit entry lives in PostgreSQL rather than in an in-memory store. `src: Deployment contract no mocks paragraph`

---

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `admin@example.com` | the administrator's seeded address | `C-RL-10` |
| `manager@example.com` | the manager's seeded address | `C-RL-10` |
| `teammate@example.com` | the first teammate's seeded address | `C-RL-10` |
| `teammate2@example.com` | the second teammate's seeded address | `C-RL-10` |
| `deku-demo-pw-2026` | the seeded password | `C-RL-11` |
| `No conversations yet. Connect a channel to start receiving them.` | the first-run empty state | `C-CF-15` |
| `No conversations match these filters.` | the filtered empty state | `C-CF-16` |
| `You are all caught up.` | the cleared empty state | `C-CF-17` |
| `Auto Agent's thoughts (Step 1)` | the reasoning disclosure title | `C-CF-32` |
| `issue_credit` | the write tool | `C-CF-34` |
| `5000` | the automatic approval ceiling in minor units | `C-CF-34` |
| `usd` | the currency | `C-CF-34` |
| `Connecting you with a specialist who can help.` | the handover message to the customer | `C-CF-37` |
| `Summary` | the summary card title | `C-CF-39` |
| `CONTENT GAP` | the first gap label | `C-CF-42` |
| `CUSTOMER DATA GAP` | the second gap label | `C-CF-42` |
| `ACTION GAP` | the third gap label | `C-CF-42` |
| `High` | the first gap badge | `C-CF-42` |
| `Medium` | the second gap badge | `C-CF-42` |
| `Low` | the third gap badge | `C-CF-42` |
| `Support workspace invitation:` | the invitation subject prefix | `C-CF-57` |
| `Handover needed:` | the handover subject prefix | `C-CF-59` |
| `Northwind Trading` | the seeded workspace name | `C-DM-10` |
| `northwind` | the seeded workspace slug | `C-DM-10` |
| `Billing Support` | the first seeded team | `C-DM-10` |
| `Technical Support` | the second seeded team | `C-DM-10` |
| `Refund for duplicate charge` | the first seeded conversation | `C-DM-11` |
| `Cannot reset my password` | the second seeded conversation | `C-DM-11` |
| `Invoice shows the wrong tax rate` | the third seeded conversation | `C-DM-11` |
| `Refunds and duplicate charges` | the first seeded article | `C-DM-12` |
| `Resetting your password` | the second seeded article | `C-DM-12` |
| `Tax rates on invoices` | the unpublished seeded article | `C-DM-12` |
| `Escalation runbook` | the internal seeded article | `C-DM-12` |
| `Standard support` | the seeded service level policy | `C-DM-13` |
| `60` | the first response target in minutes | `C-DM-13` |
| `480` | the resolution target in minutes | `C-DM-13` |
| `2000` | the conversation volume the app stays responsive at | `C-CN-05` |
| `50` | the parts per conversation | `C-CN-05` |
| `25` | the teammate count | `C-CN-05` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|

---

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 4 |
| User roles | 1 | 12 |
| Core features | 28 | 69 |
| User flow | 9 | 14 |
| UI and UX notes | 21 | 32 |
| Technical requirements | 6 | 11 |
| Data model | 8 | 16 |
| Constraints | 3 | 6 |
| Deployment contract | 14 | 18 |
