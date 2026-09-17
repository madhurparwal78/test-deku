# Checklist: Ravel Financial Data Network

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 263
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents an operator console for one financial data network organisation. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app answers what is happening now for the signed-in organisation. `src: Overview para 2`
- [ ] `C-OV-03` `constraint` The app ships no marketing site. `src: Overview para 3`
- [ ] `C-OV-04` `constraint` The app ships no documentation site. `src: Overview para 3`
- [ ] `C-OV-05` `constraint` The app ships no embedded bank-connection widget. `src: Overview para 3`
- [ ] `C-OV-06` `constraint` The app ships no consumer portal. `src: Overview para 3`
- [ ] `C-OV-07` `constraint` The app ships no billing surface. `src: Overview para 3`

## C-RL User roles

- [ ] `C-RL-01` `role` The app recognises exactly four member roles. `src: User roles para 1`
- [ ] `C-RL-02` `literal` The app accepts the seeded password `deku-demo-pw-2026` at login for every seeded account. `src: User roles para 1`
- [ ] `C-RL-03` `constraint` The app exposes no route that creates an account. `src: User roles para 1`
- [ ] `C-RL-04` `role` The app lets a member of role `developer` create an application. `src: User roles table row 1`
- [ ] `C-RL-05` `role` The app lets a member of role `developer` create a credential in `sandbox`. `src: User roles table row 1`
- [ ] `C-RL-06` `role` The app lets a member of role `developer` file a production access request. `src: User roles table row 1`
- [ ] `C-RL-07` `role` The app denies a member of role `developer` the creation of a `production` credential. `src: User roles table row 1`
- [ ] `C-RL-08` `role` The app denies a member of role `developer` every access-request decision endpoint. `src: User roles table row 1`
- [ ] `C-RL-09` `role` The app lets a member of role `administrator` change another member's role. `src: User roles table row 2`
- [ ] `C-RL-10` `role` The app denies a member of role `administrator` every access-request decision endpoint. `src: User roles table row 2`
- [ ] `C-RL-11` `role` The app lets a member of role `compliance_approver` read the full audit log. `src: User roles table row 3`
- [ ] `C-RL-12` `role` The app denies a member of role `compliance_approver` the creation of an application. `src: User roles table row 3`
- [ ] `C-RL-13` `role` The app denies a member of role `analyst` every mutating endpoint. `src: User roles table row 4`
- [ ] `C-RL-14` `role` The app enforces every authorization decision on the server for each mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-15` `role` The app leaves protected state unchanged after a denied request. `src: User roles para 2`
- [ ] `C-RL-16` `role` The app restricts a member of role `developer` to writes against applications owned by that member's own team. `src: User roles para 3`
- [ ] `C-RL-17` `role` The app denies a member of one organisation every read of another organisation's records. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `data` The app scopes one access request to one application, one environment, one product. `src: Core features rule 1`
- [ ] `C-CF-02` `literal` The app holds an access request in one of the nine states beginning `draft`. `src: Core features rule 1`
- [ ] `C-CF-03` `role` The app denies a member of role `developer` the claim, approve, deny or return endpoint. `src: Core features rule 2`
- [ ] `C-CF-04` `role` The app leaves an access request's `state` unchanged after a denied decision call. `src: Core features rule 2`
- [ ] `C-CF-05` `role` The app leaves an access request's `claimed_by` unchanged after a denied decision call. `src: Core features rule 2`
- [ ] `C-CF-06` `role` The app leaves an access request's `decided_by` unchanged after a denied decision call. `src: Core features rule 2`
- [ ] `C-CF-07` `role` The app denies the member who filed an access request every decision on that same request. `src: Core features rule 3`
- [ ] `C-CF-08` `literal` The app refuses every approval of `AR-1004` because its filer is the only approver. `src: Core features rule 3`
- [ ] `C-CF-09` `literal` The app requires the answer `intended_use` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-10` `literal` The app requires the answer `consumer_disclosure` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-11` `literal` The app requires the answer `retention_period_days` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-12` `literal` The app requires the answer `sub_processors` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-13` `literal` The app requires the answer `security_contact` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-14` `literal` The app requires the answer `expected_monthly_volume` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-15` `literal` The app requires the answer `regulatory_basis` before an access request may be submitted. `src: Core features rule 4`
- [ ] `C-CF-16` `constraint` The app rejects an incomplete submit as invalid. `src: Core features rule 4`
- [ ] `C-CF-17` `capability` The app leaves an access request in `draft` after an incomplete submit. `src: Core features rule 4`
- [ ] `C-CF-18` `capability` The app moves a `submitted` access request to `in_review` when an approver claims the request. `src: Core features rule 5`
- [ ] `C-CF-19` `capability` The app moves a `returned` access request back to `submitted`. `src: Core features rule 5`
- [ ] `C-CF-20` `constraint` The app rejects a decision call against any other state as a conflict. `src: Core features rule 5`
- [ ] `C-CF-21` `capability` The app stamps `decided_by` on approval of an access request. `src: Core features rule 6`
- [ ] `C-CF-22` `capability` The app stamps `decided_at` on approval of an access request. `src: Core features rule 6`
- [ ] `C-CF-23` `capability` The app moves the matching entitlement to `live` on approval of an access request. `src: Core features rule 6`
- [ ] `C-CF-24` `constraint` The app leaves every other product entitlement unusable after one approval. `src: Core features rule 6`
- [ ] `C-CF-25` `literal` The app requires a denial reason of 1 to `280` characters. `src: Core features rule 6`
- [ ] `C-CF-26` `constraint` The app leaves every entitlement untouched after a denial. `src: Core features rule 6`
- [ ] `C-CF-27` `role` The app hides another organisation's access requests from every list a member reads. `src: Core features rule 7`
- [ ] `C-CF-28` `literal` The app derives a connection status from the closed set beginning `healthy`. `src: Core features rule 8`
- [ ] `C-CF-29` `ui` The app distinguishes `requires_reauthentication` from `institution_unavailable` at a glance. `src: Core features rule 8`
- [ ] `C-CF-30` `constraint` The app returns no balance on any console response. `src: Core features rule 9`
- [ ] `C-CF-31` `constraint` The app returns no transaction on any console response. `src: Core features rule 9`
- [ ] `C-CF-32` `constraint` The app returns no account number on any console response. `src: Core features rule 9`
- [ ] `C-CF-33` `constraint` The app returns no identity record on any console response. `src: Core features rule 9`
- [ ] `C-CF-34` `literal` The app exposes a masked consumer reference such as `cst_****7Q2A` on a connection. `src: Core features rule 9`
- [ ] `C-CF-35` `literal` The app rejects a re-authentication prompt over `100` connections without a second approver. `src: Core features rule 10`
- [ ] `C-CF-36` `data` The app fixes an application's region at creation. `src: Core features rule 11`
- [ ] `C-CF-37` `data` The app gives one application three environments at once. `src: Core features rule 11`
- [ ] `C-CF-38` `literal` The app returns a created credential's secret exactly once as `sec_2b9f41c7d0a84e6395fd1c8b7a02e5d4` shape. `src: Core features rule 12`
- [ ] `C-CF-39` `constraint` The app returns no secret value on any later read. `src: Core features rule 12`
- [ ] `C-CF-40` `literal` The app retains the last four characters `e5d4` of a created secret for later display. `src: Core features rule 12`
- [ ] `C-CF-41` `literal` The app holds at most `2` unrevoked credentials per application per environment. `src: Core features rule 13`
- [ ] `C-CF-42` `constraint` The app rejects a third credential creation as invalid. `src: Core features rule 13`
- [ ] `C-CF-43` `literal` The app expires a `production` credential `365` days after creation. `src: Core features rule 13`
- [ ] `C-CF-44` `literal` The app refuses a new connection once an application holds `25` live ones in `development`. `src: Core features rule 15`
- [ ] `C-CF-45` `constraint` The app writes no secret value into any log line. `src: Core features rule 16`
- [ ] `C-CF-46` `constraint` The app writes no secret value into any audit entry. `src: Core features rule 16`
- [ ] `C-CF-47` `literal` The app holds at most `5` webhook endpoints per application per environment. `src: Core features rule 17`
- [ ] `C-CF-48` `constraint` The app rejects a webhook target that omits a secure scheme at creation. `src: Core features rule 17`
- [ ] `C-CF-49` `literal` The app holds a new webhook endpoint as `unverified` until a challenge is answered. `src: Core features rule 17`
- [ ] `C-CF-50` `constraint` The app delivers nothing to an `unverified` webhook endpoint. `src: Core features rule 17`
- [ ] `C-CF-51` `literal` The app subscribes a webhook endpoint to event types drawn from a set beginning `connection.created`. `src: Core features rule 18`
- [ ] `C-CF-52` `constraint` The app carries references only in a webhook delivery payload. `src: Core features rule 18`
- [ ] `C-CF-53` `constraint` The app never deletes a member row. `src: Core features rule 19`
- [ ] `C-CF-54` `literal` The app sets a consumer data request due `30` days after receipt. `src: Core features rule 20`
- [ ] `C-CF-55` `capability` The app records an audit entry when a consumer data request is completed. `src: Core features rule 20`
- [ ] `C-CF-56` `literal` The app appends every mutation to a gapless per-organisation sequence starting at `1`. `src: Core features rule 21`
- [ ] `C-CF-57` `constraint` The app exposes no route that updates an audit entry. `src: Core features rule 21`
- [ ] `C-CF-58` `constraint` The app exposes no route that deletes an audit entry. `src: Core features rule 21`
- [ ] `C-CF-59` `data` The app stores `previous_hash` on every audit entry. `src: Core features rule 22`
- [ ] `C-CF-60` `data` The app stores `entry_hash` on every audit entry. `src: Core features rule 22`
- [ ] `C-CF-61` `literal` The app computes `entry_hash` as a lowercase hex SHA-256 over seven fields joined by a pipe. `src: Core features rule 22`
- [ ] `C-CF-62` `literal` The app uses the `0000000000000000000000000000000000000000000000000000000000000000` previous hash on an organisation's first entry. `src: Core features rule 22`
- [ ] `C-CF-63` `capability` The app returns an audit chain that recomputes correctly from the stored fields. `src: Core features rule 22`
- [ ] `C-CF-64` `literal` The app delegates authentication to the Keycloak instance at `AUTH_ISSUER_URL`. `src: Core features rule 23`
- [ ] `C-CF-65` `literal` The app performs the OIDC code exchange with `AUTH_CLIENT_SECRET` on the server. `src: Core features rule 23`
- [ ] `C-CF-66` `constraint` The app never exposes the identity provider's own tokens to the browser. `src: Core features rule 23`
- [ ] `C-CF-67` `literal` The app exposes `POST /api/auth/login` returning an `access_token` field. `src: Core features rule 23`
- [ ] `C-CF-68` `literal` The app expires a session token `8` hours after issue. `src: Core features rule 23`
- [ ] `C-CF-69` `capability` The app revokes a session token at logout. `src: Core features rule 23`

## C-UF User flow

- [ ] `C-UF-01` `ui` The app serves a route `/login` without authentication. `src: User flow route table`
- [ ] `C-UF-02` `ui` The app serves an overview route `/` to every signed-in role. `src: User flow route table`
- [ ] `C-UF-03` `ui` The app serves an application list at `/applications`. `src: User flow route table`
- [ ] `C-UF-04` `ui` The app serves an access request queue at `/access-requests`. `src: User flow route table`
- [ ] `C-UF-05` `ui` The app serves a connection list at `/connections`. `src: User flow route table`
- [ ] `C-UF-06` `ui` The app serves a webhook endpoint list at `/webhooks`. `src: User flow route table`
- [ ] `C-UF-07` `ui` The app serves a member list at `/team`. `src: User flow route table`
- [ ] `C-UF-08` `ui` The app serves a consumer data request list at `/data-requests`. `src: User flow route table`
- [ ] `C-UF-09` `ui` The app serves an audit log at `/audit`. `src: User flow route table`
- [ ] `C-UF-10` `ui` The app reports requests used against committed volume at `/usage`. `src: User flow route table`
- [ ] `C-UF-11` `capability` The app redirects an unauthenticated visitor to `/login` from every other route. `src: User flow entry para`
- [ ] `C-UF-12` `capability` The app lands a successful sign-in on the overview route. `src: User flow entry para`
- [ ] `C-UF-13` `capability` The app returns a logged-out visitor to `/login`. `src: User flow entry para`
- [ ] `C-UF-14` `capability` The app preserves typed input when a session expires mid-action. `src: User flow entry para`
- [ ] `C-UF-15` `ui` The app replaces a write control with a line naming the role holding the action. `src: User flow entry para`
- [ ] `C-UF-16` `ui` The app renders an empty state naming what would fill each list. `src: User flow states para`
- [ ] `C-UF-17` `ui` The app renders a loading state shaped like each list's own columns. `src: User flow states para`
- [ ] `C-UF-18` `ui` The app renders a filtered-empty state carrying the filter summary. `src: User flow states para`
- [ ] `C-UF-19` `ui` The app serves lists cursor-paginated with a total. `src: User flow states para`
- [ ] `C-UF-20` `ui` The app reports a total alongside every paginated list. `src: User flow states para`
- [ ] `C-UF-21` `ui` The app names the missing permission on a denied action. `src: User flow states para`
- [ ] `C-UF-22` `ui` The app quotes the request identifier on an error re-render. `src: User flow states para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app reads as an operational console built for scanning. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The app carries one refined sans across every surface with monospace reserved for tabular numerals. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` The app expresses hierarchy through translucent surfaces layered at readable depths. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` The app keeps a full working set visible on one screen at comfortable density. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` The app gives every transition the same eased entrance character. `src: UI/UX notes para 3`
- [ ] `C-UX-06` `ui` The app honours a reduced-motion preference through a single duration switch. `src: UI/UX notes para 3`
- [ ] `C-UX-07` `ui` The app carries a persistent collapsible left sidebar holding the primary navigation. `src: UI/UX notes para 4`
- [ ] `C-UX-08` `ui` The app renders each queue as a board of columns with one card per record. `src: UI/UX notes para 4`
- [ ] `C-UX-09` `ui` The app fills a status chip from the lightest step of its family. `src: UI/UX notes para 5`
- [ ] `C-UX-10` `ui` The app borders a status chip from the darkest step of its family. `src: UI/UX notes para 5`
- [ ] `C-UX-11` `ui` The app renders a hovered button identical to a pressed button across three variants. `src: UI/UX notes para 6`
- [ ] `C-UX-12` `ui` The app renders a loading button identical to a pressed button across three variants. `src: UI/UX notes para 6`
- [ ] `C-UX-13` `ui` The app changes a text field's background only in the invalid state. `src: UI/UX notes para 6`
- [ ] `C-UX-14` `ui` The app accompanies an invalid field with message text. `src: UI/UX notes para 6`
- [ ] `C-UX-15` `ui` The app closes any overlay on the Escape key. `src: UI/UX notes para 6`
- [ ] `C-UX-16` `ui` The app lands a committed decision on a full confirmation page naming what changed. `src: UI/UX notes para 4`
- [ ] `C-UX-17` `ui` The app meets WCAG AA contrast on the token pairs actually used. `src: UI/UX notes para 7`
- [ ] `C-UX-18` `ui` The app supports keyboard navigation with a visible focus ring on every ground. `src: UI/UX notes para 7`
- [ ] `C-UX-19` `ui` The app avoids horizontal page overflow at every viewport width. `src: UI/UX notes para 7`
- [ ] `C-UX-20` `ui` The app stacks each board into one column below the desktop breakpoint. `src: UI/UX notes para 7`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app authors every spacing value as a multiple of one root unit. `src: Front-end specification, Scaling`
- [ ] `C-FE-02` `ui` The app sizes type in relative units so raised browser text enlarges the console. `src: Front-end specification, Scaling`
- [ ] `C-FE-03` `ui` The app authors no colour outside the recorded ramps. `src: Front-end specification, Palette`
- [ ] `C-FE-04` `ui` The app re-exports every ramp value under a semantic role name. `src: Front-end specification, semantic layer`
- [ ] `C-FE-05` `ui` The app leaves the seven per-component slot tokens transparent at the document root. `src: Front-end specification, unresolved tokens`
- [ ] `C-FE-06` `ui` The app builds all eight elevation shadows from one near-black alpha. `src: Front-end specification, elevation`
- [ ] `C-FE-07` `ui` The app renders a solid button's contact state as a translucent overlay. `src: Front-end specification, component matrix`
- [ ] `C-FE-08` `ui` The app draws an icon one ramp step lighter than adjacent words. `src: Front-end specification, component matrix`
- [ ] `C-FE-09` `ui` The app ships no font file with the build. `src: Front-end specification, Typography`
- [ ] `C-FE-10` `ui` The app loads every face with a swap display strategy. `src: Front-end specification, Typography`
- [ ] `C-FE-11` `ui` The app overshoots on the primary arrive curve. `src: Front-end specification, Motion tokens`
- [ ] `C-FE-12` `ui` The app uses only the four named layer tokens in application code. `src: Front-end specification, Layer order`
- [ ] `C-FE-13` `ui` The app renders a skeleton of the correct row count during a list load. `src: Front-end specification, Skeletons`
- [ ] `C-FE-14` `ui` The app keeps every surface usable at 400 per cent zoom. `src: Front-end specification, Responsive`
- [ ] `C-FE-15` `ui` The app places a skip link first in the order reaching the main content. `src: Front-end specification, Responsive`
- [ ] `C-FE-16` `ui` The app emits no typographic dash anywhere in product copy. `src: Front-end specification, Copy`
- [ ] `C-FE-17` `ui` The app ships no image file with the build. `src: Front-end specification, Performance budgets`
- [ ] `C-FE-18` `ui` The app downloads no other route's code on any single route. `src: Front-end specification, Performance budgets`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app renders every route as complete HTML on the server. `src: Technical requirements para 1`
- [ ] `C-TR-02` `capability` The app rejects a re-authentication prompt over the bulk threshold without a second approver. `src: Technical requirements, operational limits`
- [ ] `C-TR-03` `role` The app denies a member of one organisation every write on another organisation's records. `src: Technical requirements, operational limits`
- [ ] `C-TR-04` `contract` The app serves its JSON API under `/api` on one origin with the rendered routes. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` The app reads its datastore location from `DATABASE_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-06` `literal` The app reads its identity provider location from `AUTH_ISSUER_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-07` `literal` The app reads its public origin from `APP_PUBLIC_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-08` `literal` The app reads its public port from `APP_PUBLIC_PORT`. `src: Technical requirements para 2`
- [ ] `C-TR-09` `constraint` The app introduces no second database. `src: Technical requirements para 3`
- [ ] `C-TR-10` `constraint` The app introduces no second identity provider. `src: Technical requirements para 3`
- [ ] `C-TR-11` `literal` The app answers `GET /api/health` with a JSON body once seeding has completed. `src: Technical requirements para 4`
- [ ] `C-TR-12` `capability` The app logs one structured JSON line per request. `src: Technical requirements para 5`
- [ ] `C-TR-13` `constraint` The app logs no request body. `src: Technical requirements para 5`
- [ ] `C-TR-14` `capability` The app carries one request identifier into the log line. `src: Technical requirements para 6`
- [ ] `C-TR-15` `capability` The app returns one request identifier in the error response body. `src: Technical requirements para 6`
- [ ] `C-TR-16` `capability` The app decides authorization in one place that every route consults. `src: Technical requirements para 7`
- [ ] `C-TR-17` `constraint` The app defaults an authorization decision to deny. `src: Technical requirements para 7`
- [ ] `C-TR-18` `constraint` The app lets an explicit denial defeat every allow a member otherwise holds. `src: Technical requirements para 7`
- [ ] `C-TR-19` `capability` The app applies the same authorization answer again when rows are selected. `src: Technical requirements para 7`
- [ ] `C-TR-20` `capability` The app isolates each organisation's rows at the data layer. `src: Technical requirements, Backend architecture`
- [ ] `C-TR-21` `capability` The app exposes opaque type-prefixed identifiers outside the service. `src: Technical requirements, Backend architecture`
- [ ] `C-TR-22` `capability` The app produces one effect when a job runs twice. `src: Technical requirements, Idempotency`
- [ ] `C-TR-23` `capability` The app records a decision against the exact form version in force at decision time. `src: Technical requirements, Idempotency`
- [ ] `C-TR-24` `capability` The app refuses a caller over its limit with a retry interval in seconds. `src: Technical requirements, Rate limiting`
- [ ] `C-TR-25` `constraint` The app stores no authenticated route in a shared cache. `src: Technical requirements, Caching`
- [ ] `C-TR-26` `constraint` The app refuses a cross-region read with the resource's region named. `src: Technical requirements, Regionality`
- [ ] `C-TR-27` `capability` The app refuses every write when the datastore is unreachable. `src: Technical requirements, Observability`
- [ ] `C-TR-28` `capability` The app names the identity provider when a new sign-in fails. `src: Technical requirements, Observability`

## C-DM Data model

- [ ] `C-DM-01` `data` The app holds thirteen tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` The app stores every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` The app writes the seeded password `deku-demo-pw-2026` into `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-04` `data` The app holds a unique organisation name. `src: Data model, organisation`
- [ ] `C-DM-05` `data` The app holds a member role drawn from the four named values. `src: Data model, member`
- [ ] `C-DM-06` `data` The app rejects a write that changes an application's region after creation. `src: Data model, application`
- [ ] `C-DM-07` `literal` The app caps `development` connections at `25` per application. `src: Data model, app_environment`
- [ ] `C-DM-08` `data` The app stores a credential secret as a one-way hash. `src: Data model, api_credential`
- [ ] `C-DM-09` `constraint` The app exposes no column that returns a credential secret. `src: Data model, api_credential`
- [ ] `C-DM-10` `constraint` The app lets exactly one of two simultaneous credential creations succeed at the limit. `src: Data model, api_credential`
- [ ] `C-DM-11` `constraint` The app leaves no row behind after a failed credential creation. `src: Data model, api_credential`
- [ ] `C-DM-12` `data` The app holds one entitlement row per application per environment per product. `src: Data model, entitlement`
- [ ] `C-DM-13` `data` The app names an access request `AR-` followed by four digits. `src: Data model, access_request`
- [ ] `C-DM-14` `constraint` The app never equates `decided_by_member_id` with `requested_by_member_id`. `src: Data model, access_request`
- [ ] `C-DM-15` `constraint` The app writes only a `compliance_approver` member into `decided_by_member_id`. `src: Data model, access_request`
- [ ] `C-DM-16` `constraint` The app lets exactly one of two simultaneous approvals of one request succeed. `src: Data model, access_request`
- [ ] `C-DM-17` `constraint` The app writes no audit entry for the losing simultaneous approval. `src: Data model, access_request`
- [ ] `C-DM-18` `data` The app holds seven answer rows before an access request leaves `draft`. `src: Data model, access_request_answer`
- [ ] `C-DM-19` `data` The app names a connection `con_` followed by four lowercase alphanumerics. `src: Data model, connection`
- [ ] `C-DM-20` `constraint` The app holds no balance column on a connection. `src: Data model, connection`
- [ ] `C-DM-21` `data` The app names a consumer data request `dsr_` followed by four digits. `src: Data model, data_request`
- [ ] `C-DM-22` `literal` The app seeds an organisation named `Vantor` in region `us`. `src: Data model, seed data`
- [ ] `C-DM-23` `literal` The app seeds an organisation named `Wrenwood` in region `eu`. `src: Data model, seed data`
- [ ] `C-DM-24` `literal` The app seeds a member `developer@example.com` on team `Payments Integration`. `src: Data model, seed data`
- [ ] `C-DM-25` `literal` The app seeds a member `developer2@example.com` on team `Risk Platform`. `src: Data model, seed data`
- [ ] `C-DM-26` `literal` The app seeds a member `administrator@example.com` with role `administrator`. `src: Data model, seed data`
- [ ] `C-DM-27` `literal` The app seeds a member `compliance@example.com` with role `compliance_approver`. `src: Data model, seed data`
- [ ] `C-DM-28` `literal` The app seeds a member `analyst@example.com` with role `analyst`. `src: Data model, seed data`
- [ ] `C-DM-29` `literal` The app seeds a member `administrator2@example.com` inside `Wrenwood`. `src: Data model, seed data`
- [ ] `C-DM-30` `literal` The app seeds an application `vantor-payouts` owned by `Payments Integration`. `src: Data model, seed data`
- [ ] `C-DM-31` `literal` The app seeds an application `vantor-risk-signals` owned by `Risk Platform`. `src: Data model, seed data`
- [ ] `C-DM-32` `literal` The app seeds an application `vantor-ledger-sync` owned by `Payments Integration`. `src: Data model, seed data`
- [ ] `C-DM-33` `literal` The app seeds an application `wrenwood-onboarding` inside `Wrenwood`. `src: Data model, seed data`
- [ ] `C-DM-34` `literal` The app seeds a product keyed `transactions`. `src: Data model, seed data`
- [ ] `C-DM-35` `literal` The app seeds `AR-1001` as `submitted` against `vantor-payouts`. `src: Data model, seed data`
- [ ] `C-DM-36` `literal` The app seeds `AR-1002` as `in_review` claimed by `compliance@example.com`. `src: Data model, seed data`
- [ ] `C-DM-37` `literal` The app seeds `AR-1003` as `approved`. `src: Data model, seed data`
- [ ] `C-DM-38` `literal` The app seeds `AR-1004` as `submitted` filed by `compliance@example.com`. `src: Data model, seed data`
- [ ] `C-DM-39` `literal` The app seeds `AR-2001` inside `Wrenwood`. `src: Data model, seed data`
- [ ] `C-DM-40` `literal` The app seeds connection `con_7hq2` as `healthy` at `Gantry Bank`. `src: Data model, seed data`
- [ ] `C-DM-41` `literal` The app seeds connection `con_9km4` as `requires_reauthentication` at `Anchor National`. `src: Data model, seed data`
- [ ] `C-DM-42` `literal` The app seeds connection `con_3wp8` as `institution_unavailable`. `src: Data model, seed data`
- [ ] `C-DM-43` `literal` The app seeds connection `con_5tz1` as `revoked_by_consumer` at `Metro Credit Union`. `src: Data model, seed data`
- [ ] `C-DM-44` `literal` The app seeds a webhook endpoint at `https://hooks.vantor.example/ravel`. `src: Data model, seed data`
- [ ] `C-DM-45` `literal` The app seeds a consumer data request `dsr_4410` as `received`. `src: Data model, seed data`
- [ ] `C-DM-46` `literal` The app seeds a consumer data request `dsr_4411` as `completed`. `src: Data model, seed data`
- [ ] `C-DM-47` `constraint` The app duplicates no row when the seeding runs a second time. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one console per organisation. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app provides no invoice surface. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The app provides no identity verification session. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` The app provides no single sign-on configuration screen. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The app makes no external network call at runtime beyond its two backing services. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` The app sends no email. `src: Constraints bullet 4`
- [ ] `C-CN-07` `constraint` The app delivers nothing to a recorded webhook endpoint. `src: Constraints bullet 4`
- [ ] `C-CN-08` `constraint` The app generates no data export file. `src: Constraints bullet 5`
- [ ] `C-CN-09` `literal` The app stays responsive with `10,000` audit entries. `src: Constraints bullet 6`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at the public origin given by its environment. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The app listens on the container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app hardcodes neither its public port nor its public origin. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves its HTTP API under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `literal` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `literal` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `literal` The app leaves a reserved empty `.browser_screenshots/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `literal` The app leaves a reserved empty `.downloads/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-11` `contract` The app keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The app runs outside the shell's process tree. `src: Deployment contract bullet 8`
- [ ] `C-DC-13` `literal` The app binds `0.0.0.0` rather than a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-14` `contract` The app starts no copy of either backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-15` `constraint` The app uses no edge function. `src: Deployment contract bullet 11`
- [ ] `C-DC-16` `constraint` The app declares no persistent volume. `src: Deployment contract bullet 12`
- [ ] `C-DC-17` `literal` The app returns `access_token` from `POST /api/auth/login`. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `literal` The app returns a top-level JSON array from `GET /api/applications`. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `literal` The app returns a top-level JSON array from `GET /api/access-requests`. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `literal` The app returns a top-level JSON array from `GET /api/connections`. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `literal` The app returns a top-level JSON array from `GET /api/audit`. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `literal` The app omits `secret` from every item of `GET /api/applications/{slug}/{environment}/credentials`. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `constraint` The app rejects an invalid call as a client error rather than a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `constraint` The app requires a bearer token on every endpoint but login or health. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `constraint` The app substitutes no in-process store for its datastore. `src: Deployment contract, No mocks`
- [ ] `C-DC-26` `constraint` The app substitutes no self-answered response for the identity provider exchange. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-RL-02 | User roles para 1 |
| `draft` | first access request state | C-CF-02 | Core features rule 1 |
| `AR-1004` | access request filed by the only approver | C-CF-08 | Core features rule 3 |
| `intended_use` | required request answer key | C-CF-09 | Core features rule 4 |
| `consumer_disclosure` | required request answer key | C-CF-10 | Core features rule 4 |
| `retention_period_days` | required request answer key | C-CF-11 | Core features rule 4 |
| `sub_processors` | required request answer key | C-CF-12 | Core features rule 4 |
| `security_contact` | required request answer key | C-CF-13 | Core features rule 4 |
| `expected_monthly_volume` | required request answer key | C-CF-14 | Core features rule 4 |
| `regulatory_basis` | required request answer key | C-CF-15 | Core features rule 4 |
| `280` | upper bound on a denial reason length | C-CF-25 | Core features rule 6 |
| `healthy` | first connection status value | C-CF-28 | Core features rule 8 |
| `cst_****7Q2A` | masked consumer reference on a seeded connection | C-CF-34 | Core features rule 9 |
| `100` | connection count above which a second approver is required | C-CF-35 | Core features rule 10 |
| `sec_2b9f41c7d0a84e6395fd1c8b7a02e5d4` | worked example of a created secret | C-CF-38 | Core features rule 12 |
| `e5d4` | last four characters of the worked example secret | C-CF-40 | Core features rule 12 |
| `2` | live credentials allowed per application per environment | C-CF-41 | Core features rule 13 |
| `production` | charged environment name | C-CF-43 | Core features rule 13 |
| `365` | days before a production credential expires | C-CF-43 | Core features rule 13 |
| `25` | development connection cap per application | C-CF-44 | Core features rule 15 |
| `development` | capped real-data environment name | C-CF-44 | Core features rule 15 |
| `5` | webhook endpoints allowed per application per environment | C-CF-47 | Core features rule 17 |
| `unverified` | state of a new webhook endpoint | C-CF-49 | Core features rule 17 |
| `connection.created` | first webhook event type | C-CF-51 | Core features rule 18 |
| `30` | days until a consumer data request falls due | C-CF-54 | Core features rule 20 |
| `1` | first audit sequence number | C-CF-56 | Core features rule 21 |
| `entry_hash` | audit chain field holding this entry's hash | C-CF-61 | Core features rule 22 |
| `0000000000000000000000000000000000000000000000000000000000000000` | previous hash of an organisation's first audit entry | C-CF-62 | Core features rule 22 |
| `AUTH_ISSUER_URL` | identity provider location variable | C-CF-64 | Core features rule 23 |
| `AUTH_CLIENT_SECRET` | confidential client secret variable | C-CF-65 | Core features rule 23 |
| `POST /api/auth/login` | password grant login endpoint | C-CF-67 | Core features rule 23 |
| `access_token` | session token field returned by login | C-CF-67 | Core features rule 23 |
| `8` | hours before a session token expires | C-CF-68 | Core features rule 23 |
| `DATABASE_URL` | datastore location variable | C-TR-05 | Technical requirements para 2 |
| `APP_PUBLIC_URL` | public origin variable | C-TR-07 | Technical requirements para 2 |
| `APP_PUBLIC_PORT` | public port variable | C-TR-08 | Technical requirements para 2 |
| `GET /api/health` | health endpoint | C-TR-11 | Technical requirements para 4 |
| `/app/USER_README.md` | credentials file path | C-DM-03 | Data model para 2 |
| `Vantor` | seeded organisation | C-DM-22 | Data model, seed data |
| `us` | seeded region of Vantor | C-DM-22 | Data model, seed data |
| `Wrenwood` | second seeded organisation | C-DM-23 | Data model, seed data |
| `eu` | seeded region of Wrenwood | C-DM-23 | Data model, seed data |
| `developer@example.com` | seeded developer account | C-DM-24 | Data model, seed data |
| `Payments Integration` | seeded team | C-DM-24 | Data model, seed data |
| `developer2@example.com` | second seeded developer account | C-DM-25 | Data model, seed data |
| `Risk Platform` | second seeded team | C-DM-25 | Data model, seed data |
| `administrator@example.com` | seeded administrator account | C-DM-26 | Data model, seed data |
| `administrator` | role that changes another member's role | C-DM-26 | Data model, seed data |
| `compliance@example.com` | seeded compliance approver account | C-DM-27 | Data model, seed data |
| `compliance_approver` | role that decides an access request | C-DM-27 | Data model, seed data |
| `analyst@example.com` | seeded analyst account | C-DM-28 | Data model, seed data |
| `analyst` | read-only role | C-DM-28 | Data model, seed data |
| `administrator2@example.com` | seeded administrator in the second organisation | C-DM-29 | Data model, seed data |
| `vantor-payouts` | seeded application slug | C-DM-30 | Data model, seed data |
| `vantor-risk-signals` | seeded application slug | C-DM-31 | Data model, seed data |
| `vantor-ledger-sync` | seeded application slug | C-DM-32 | Data model, seed data |
| `wrenwood-onboarding` | seeded application slug in the second organisation | C-DM-33 | Data model, seed data |
| `transactions` | seeded product key | C-DM-34 | Data model, seed data |
| `AR-1001` | seeded submitted access request | C-DM-35 | Data model, seed data |
| `submitted` | state of a complete access request awaiting a claim | C-DM-35 | Data model, seed data |
| `AR-1002` | seeded in-review access request | C-DM-36 | Data model, seed data |
| `in_review` | state of a claimed access request | C-DM-36 | Data model, seed data |
| `AR-1003` | seeded approved access request | C-DM-37 | Data model, seed data |
| `approved` | state of a signed-off access request | C-DM-37 | Data model, seed data |
| `AR-2001` | seeded access request in the second organisation | C-DM-39 | Data model, seed data |
| `con_7hq2` | seeded healthy connection | C-DM-40 | Data model, seed data |
| `Gantry Bank` | seeded institution | C-DM-40 | Data model, seed data |
| `con_9km4` | seeded connection needing re-authentication | C-DM-41 | Data model, seed data |
| `requires_reauthentication` | connection status needing the consumer | C-DM-41 | Data model, seed data |
| `Anchor National` | seeded institution | C-DM-41 | Data model, seed data |
| `con_3wp8` | seeded connection at an unavailable institution | C-DM-42 | Data model, seed data |
| `institution_unavailable` | connection status not needing the consumer | C-DM-42 | Data model, seed data |
| `con_5tz1` | seeded connection revoked by its consumer | C-DM-43 | Data model, seed data |
| `revoked_by_consumer` | connection status after a consumer withdrew | C-DM-43 | Data model, seed data |
| `Metro Credit Union` | seeded institution | C-DM-43 | Data model, seed data |
| `https://hooks.vantor.example/ravel` | seeded webhook target | C-DM-44 | Data model, seed data |
| `dsr_4410` | seeded consumer data request | C-DM-45 | Data model, seed data |
| `received` | state of a new consumer data request | C-DM-45 | Data model, seed data |
| `dsr_4411` | seeded consumer data request | C-DM-46 | Data model, seed data |
| `completed` | final state of a consumer data request | C-DM-46 | Data model, seed data |
| `10,000` | audit entry volume the console stays responsive at | C-CN-09 | Constraints bullet 6 |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `200` | status returned by the health endpoint when ready | C-DC-05 | Deployment contract bullet 3 |
| `.browser_screenshots/` | reserved empty directory | C-DC-08 | Deployment contract bullet 6 |
| `.downloads/` | reserved empty directory | C-DC-09 | Deployment contract bullet 6 |
| `0.0.0.0` | bind address | C-DC-13 | Deployment contract bullet 9 |
| `GET /api/applications` | application list endpoint | C-DC-18 | Deployment contract, API shapes |
| `GET /api/access-requests` | access request list endpoint | C-DC-19 | Deployment contract, API shapes |
| `GET /api/connections` | connection list endpoint | C-DC-20 | Deployment contract, API shapes |
| `GET /api/audit` | audit list endpoint | C-DC-21 | Deployment contract, API shapes |
| `secret` | field name absent from every credential list item | C-DC-22 | Deployment contract, API shapes |
| `GET /api/applications/{slug}/{environment}/credentials` | credential list endpoint | C-DC-22 | Deployment contract, API shapes |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the challenge a webhook endpoint answers to become verified | C-CF-49 | named as a challenge with no token format given |
| the second approver required for a large re-authentication prompt | C-CF-35 | named by role with no endpoint or token given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 0 | 7 |
| User roles | 4 | 17 |
| Core features | 9 | 69 |
| User flow | 3 | 22 |
| UI and UX notes | 1 | 20 |
| Front-end specification | 4 | 18 |
| Technical requirements | 12 | 28 |
| Data model | 11 | 47 |
| Constraints | 1 | 9 |
| Deployment contract | 11 | 26 |

The obligation-sentence column is the machine recount over instruction.md. Items exceed it in every row because one sentence routinely carries two asks.
