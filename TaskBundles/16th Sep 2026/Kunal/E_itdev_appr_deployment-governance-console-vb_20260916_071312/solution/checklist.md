# Checklist: Meridian Deployment Governance Console

Items: 258
Unpinned values flagged: 7
Sections present: Overview, User roles, Core features, User flow, UI and UX notes, Technical requirements, Front-end specification, Data model, Constraints, Deployment contract

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a public marketing surface plus a governed console behind one identity system `src: Overview`
- [ ] `C-OV-02` `capability` The console holds teams, projects, deployments, access groups, spend limits, firewall rules, observability, audit logs `src: Overview`
- [ ] `C-OV-03` `role` A principal is an account, an agent, or a token `src: Overview`
- [ ] `C-OV-04` `capability` A commit produces a build, a build produces a deployment on a preview address, a promotion request moves that deployment to production `src: Overview`
- [ ] `C-OV-05` `constraint` The product does not run customer builds, serve customer traffic, or terminate TLS `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A developer may open a promotion request `src: User roles`
- [ ] `C-RL-02` `role` A developer may trigger a build `src: User roles`
- [ ] `C-RL-03` `role` A developer may not approve any promotion request `src: User roles`
- [ ] `C-RL-04` `role` A developer may not change a firewall rule, a spend cap, a role, a membership `src: User roles`
- [ ] `C-RL-05` `role` A reviewer may approve a promotion request raised by another principal `src: User roles`
- [ ] `C-RL-06` `role` A reviewer may reject a promotion request `src: User roles`
- [ ] `C-RL-07` `role` A reviewer may manage firewall rules `src: User roles`
- [ ] `C-RL-08` `role` A reviewer may not change billing, a spend cap, an invoice `src: User roles`
- [ ] `C-RL-09` `role` A reviewer may not deploy `src: User roles`
- [ ] `C-RL-10` `role` A finance principal may set a budget, set a spend cap, export cost attribution `src: User roles`
- [ ] `C-RL-11` `role` A finance principal may not deploy, promote, approve, read runtime logs `src: User roles`
- [ ] `C-RL-12` `role` A viewer may read project, deployment list, deployment status only `src: User roles`
- [ ] `C-RL-13` `role` A viewer may not read environment values, log lines, invoice amounts, member email addresses `src: User roles`
- [ ] `C-RL-14` `role` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-15` `role` A direct API call from a lower-role session to a reviewer-only endpoint is denied by the server `src: User roles`
- [ ] `C-RL-16` `role` A denied call leaves the protected state unchanged `src: User roles`
- [ ] `C-RL-17` `role` An explicit deny outranks every allow at every scope `src: User roles`
- [ ] `C-RL-18` `role` A refusal for an invisible resource is identical in shape to a refusal for a missing resource `src: User roles`
- [ ] `C-RL-19` `role` A bulk operation evaluates permission per item, returning a per-item result `src: User roles`
- [ ] `C-RL-20` `literal` Signup is closed: the six seeded accounts are `developer@example.com`, `reviewer@example.com`, `reviewer2@example.com`, `finance@example.com`, `viewer@example.com`, `developer2@example.com` `src: User roles`
- [ ] `C-RL-21` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-22` `role` developer2@example.com belongs only to the atlas team `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` POST /api/auth/login takes an email plus a password, returning an access token `src: Core features > Auth`
- [ ] `C-CF-02` `contract` Every endpoint other than health, login, the public reads, the webhook receiver requires a bearer token `src: Core features > Auth`
- [ ] `C-CF-03` `data` Passwords are stored hashed, never in clear `src: Core features > Auth`
- [ ] `C-CF-04` `contract` A token expires eight hours after issue, an expired token being refused `src: Core features > Auth`
- [ ] `C-CF-05` `capability` Keycloak is the directory of record for accounts, reachable at AUTH_ISSUER_URL `src: Core features > Auth`
- [ ] `C-CF-06` `contract` A login with a wrong password is rejected as invalid `src: Core features > Auth`
- [ ] `C-CF-07` `contract` A login for an unknown address is refused in the same shape as a wrong password `src: Core features > Auth`
- [ ] `C-CF-08` `contract` No state-changing operation is reachable by GET `src: Core features > Auth`
- [ ] `C-CF-09` `ui` The log-in screen lists Continue with Email, Google, GitHub, ChatGPT, SAML SSO, Passkey, Show other options in that order `src: Core features > Auth`
- [ ] `C-CF-10` `ui` The sign-up screen lists Google, GitHub, ChatGPT, Apple, Show other options, Continue with Email in that order `src: Core features > Auth`
- [ ] `C-CF-11` `constraint` SAML SSO is absent from the sign-up screen `src: Core features > Auth`
- [ ] `C-CF-12` `ui` Both identity screens fit one viewport at every supported size `src: Core features > Auth`
- [ ] `C-CF-13` `ui` Cancelling a provider sign-in returns to the same screen with no error shown `src: Core features > Auth`
- [ ] `C-CF-14` `contract` The session cookie is set HttpOnly, Secure, SameSite=Lax, host-only, at path / `src: Core features > Auth`
- [ ] `C-CF-15` `ui` /account lists every active session, each individually revocable `src: Core features > Auth`
- [ ] `C-CF-16` `literal` A team is addressed by slug at the first path segment, so `/northwind/checkout-web` names the checkout-web project `src: Core features > Teams`
- [ ] `C-CF-17` `contract` Team-level sections sit under a tilde segment that can never be a team slug or a project slug `src: Core features > Teams`
- [ ] `C-CF-18` `data` A team slug matching a reserved public route is refused as invalid, no team row being written `src: Core features > Teams`
- [ ] `C-CF-19` `data` Two teams may not share a slug `src: Core features > Teams`
- [ ] `C-CF-20` `data` Two projects inside one team may not share a slug `src: Core features > Teams`
- [ ] `C-CF-21` `ui` Switching teams is a navigation to the new team address, never a swap of client state `src: Core features > Teams`
- [ ] `C-CF-22` `ui` The team switcher names the current team, listing every team the principal belongs to `src: Core features > Teams`
- [ ] `C-CF-23` `ui` The breadcrumb names team, then project, then section `src: Core features > Teams`
- [ ] `C-CF-24` `literal` The deployment states are `QUEUED`, `BUILDING`, `READY`, `ERROR`, `CANCELED`, `PROMOTING`, `LIVE`, `SUPERSEDED` `src: Core features > Deployments`
- [ ] `C-CF-25` `contract` POST /api/webhooks/git verifies its signature header against the raw body before parsing `src: Core features > Deployments`
- [ ] `C-CF-26` `contract` A webhook timestamp more than five minutes old is refused `src: Core features > Deployments`
- [ ] `C-CF-27` `data` A replayed delivery identifier produces exactly one deployment `src: Core features > Deployments`
- [ ] `C-CF-28` `data` A repeated project plus source kind plus commit produces exactly one deployment `src: Core features > Deployments`
- [ ] `C-CF-29` `data` A failed build moves the deployment to ERROR, leaving the live alias untouched `src: Core features > Deployments`
- [ ] `C-CF-30` `ui` A queued deployment shows a real queue position `src: Core features > Deployments`
- [ ] `C-CF-31` `contract` The deployment list is keyset-paginated newest first `src: Core features > Deployments`
- [ ] `C-CF-32` `literal` The seeded production policy is `Production two-eyes`, version `1`, requiring `2` approvals from `release-reviewers` `src: Core features > Promotion`
- [ ] `C-CF-33` `literal` A promotion request state is one of `OPEN`, `APPROVED`, `REJECTED`, `EXPIRED`, `CANCELED`, `EXECUTED`, `FAILED` `src: Core features > Promotion`
- [ ] `C-CF-34` `role` Only a reviewer who belongs to an eligible access group may approve a promotion request `src: Core features > Promotion`
- [ ] `C-CF-35` `role` A developer calling the approve endpoint with a valid token is denied by the server `src: Core features > Promotion`
- [ ] `C-CF-36` `data` A denied approval leaves the gathered approval count unchanged `src: Core features > Promotion`
- [ ] `C-CF-37` `data` A denied approval leaves the request state at OPEN `src: Core features > Promotion`
- [ ] `C-CF-38` `data` A denied approval writes no approval decision row `src: Core features > Promotion`
- [ ] `C-CF-39` `role` A finance principal calling the approve endpoint is denied by the server `src: Core features > Promotion`
- [ ] `C-CF-40` `role` A viewer calling the approve endpoint is denied by the server `src: Core features > Promotion`
- [ ] `C-CF-41` `role` The requester may not approve their own request when self-approval is disabled `src: Core features > Promotion`
- [ ] `C-CF-42` `data` The same reviewer approving twice is refused as a duplicate, recording nothing the second time `src: Core features > Promotion`
- [ ] `C-CF-43` `data` One rejection closes the request into REJECTED with a mandatory comment `src: Core features > Promotion`
- [ ] `C-CF-44` `data` Two approvals arriving at the same instant are both recorded `src: Core features > Promotion`
- [ ] `C-CF-45` `data` Reaching the approval count writes APPROVED, a separate step writing EXECUTED `src: Core features > Promotion`
- [ ] `C-CF-46` `data` Two promotions racing for one alias produce exactly one winner `src: Core features > Promotion`
- [ ] `C-CF-47` `contract` The losing promotion is refused with a conflict naming the winning deployment `src: Core features > Promotion`
- [ ] `C-CF-48` `data` A promotion moves the alias to the approved deployment, records the previous deployment, moves the superseded deployment to SUPERSEDED, in one transaction `src: Core features > Promotion`
- [ ] `C-CF-49` `capability` Rollback is promoting a superseded deployment again under the same authorization `src: Core features > Promotion`
- [ ] `C-CF-50` `ui` The approval board groups open requests by state, newest first `src: Core features > Promotion`
- [ ] `C-CF-51` `ui` A request card shows the deployment, the commit, the requester, the elapsed time, the gathered approvals against the required approvals `src: Core features > Promotion`
- [ ] `C-CF-52` `ui` A request detail shows the environment-value diff by key with values never rendered `src: Core features > Promotion`
- [ ] `C-CF-53` `ui` The gathered approval count updates for a second reviewer without a reload `src: Core features > Promotion`
- [ ] `C-CF-54` `role` A principal sees only the requests that principal is eligible to act on plus their own `src: Core features > Promotion`
- [ ] `C-CF-55` `data` Every state change writes one audit record carrying a gapless per-organisation sequence number `src: Core features > Audit log`
- [ ] `C-CF-56` `data` An audit record carries the actor principal, the actor kind, the action verb, the resource, the outcome `src: Core features > Audit log`
- [ ] `C-CF-57` `data` An audit record carries a redacted before plus after, the request identifier, the address `src: Core features > Audit log`
- [ ] `C-CF-58` `data` A denial writes an audit record whose outcome is deny, carrying the authorization reason `src: Core features > Audit log`
- [ ] `C-CF-59` `data` No role the application holds may update or delete an audit row `src: Core features > Audit log`
- [ ] `C-CF-60` `data` Each audit record hashes its own content plus the previous record hash `src: Core features > Audit log`
- [ ] `C-CF-61` `constraint` An audit record is never deleted by any principal at any level of access `src: Core features > Audit log`
- [ ] `C-CF-62` `literal` The claimed compliance regimes are `SOC 2 Type 2`, `PCI DSS`, `ISO 27001`, `EU-U.S. DPF`, `HIPAA BAA`, `TISAX` `src: Core features > Audit log`
- [ ] `C-CF-63` `literal` A firewall rule action is one of `allow`, `deny`, `challenge`, `log`, `rate-limit`, `bypass` `src: Core features > Firewall`
- [ ] `C-CF-64` `capability` Firewall rules evaluate by ordering value ascending, first match winning `src: Core features > Firewall`
- [ ] `C-CF-65` `capability` A bypass rule evaluates before every other rule `src: Core features > Firewall`
- [ ] `C-CF-66` `literal` The three seeded firewall rules are `Log request starting with /`, `Challenge user agents that look like bots`, `Deny traffic from Germany` `src: Core features > Firewall`
- [ ] `C-CF-67` `literal` Custom firewall rule caps are `3` on Hobby, `40` on Pro, `1000` on Enterprise `src: Core features > Firewall`
- [ ] `C-CF-68` `literal` Address block caps are `3` on Hobby, `100` on Pro, `1000` on Enterprise `src: Core features > Firewall`
- [ ] `C-CF-69` `literal` System bypass rule caps are `0` on Hobby, `25` on Pro, `100` on Enterprise `src: Core features > Firewall`
- [ ] `C-CF-70` `capability` Firewall plan caps are read from the same plan definition the pricing page renders `src: Core features > Firewall`
- [ ] `C-CF-71` `ui` Reaching a firewall cap disables the create control, naming the cap, before a rule is written `src: Core features > Firewall`
- [ ] `C-CF-72` `capability` The rule editor previews how many requests in the last hour a rule would have matched `src: Core features > Firewall`
- [ ] `C-CF-73` `ui` An active challenge mode is announced prominently with a reason plus an off control `src: Core features > Firewall`
- [ ] `C-CF-74` `data` Money is integer minor units in usd everywhere, no floating-point value touching a monetary amount `src: Core features > Spend management`
- [ ] `C-CF-75` `literal` The Pro plan price is `2000` minor units a month, Hobby being `0` `src: Core features > Spend management`
- [ ] `C-CF-76` `data` A usage record carries an idempotency key, ingestion upserting on that key `src: Core features > Spend management`
- [ ] `C-CF-77` `data` A repeated metering submission charges once `src: Core features > Spend management`
- [ ] `C-CF-78` `literal` A spend hard-cap action is one of `notify`, `restrict`, `pause` `src: Core features > Spend management`
- [ ] `C-CF-79` `capability` At the hard cap under pause, new builds stop, production traffic continuing to be served `src: Core features > Spend management`
- [ ] `C-CF-80` `data` A spend pause writes an audit record, being reversible in one action `src: Core features > Spend management`
- [ ] `C-CF-81` `ui` The usage figure states its lag on screen, never more than five minutes behind `src: Core features > Spend management`
- [ ] `C-CF-82` `constraint` A billing restriction never takes production traffic offline `src: Core features > Spend management`
- [ ] `C-CF-83` `capability` Notification recipients are resolved from roles plus access groups at the moment of the event `src: Core features > Notifications`
- [ ] `C-CF-84` `literal` A query aggregate is one of `AVG`, `SUM`, `MAX`, `MIN`, `count`, `p50`, `p75`, `p90`, `p95`, `p99` `src: Core features > Observability`
- [ ] `C-CF-85` `capability` The scope filter is appended by the query compiler, expressible nowhere in the query text `src: Core features > Observability`
- [ ] `C-CF-86` `capability` A query exceeding its cost estimate is refused before running `src: Core features > Observability`
- [ ] `C-CF-87` `ui` A telemetry gap renders as a gap with its extent marked, never as a zero `src: Core features > Observability`
- [ ] `C-CF-88` `literal` The public routes are `/`, `/pricing`, `/enterprise`, `/security`, `/docs`, `/templates`, `/blog`, `/changelog`, `/customers`, `/ai`, `/i`, `/login`, `/signup` `src: Core features > The public surface`
- [ ] `C-CF-89` `ui` A privacy page at /privacy is reachable from the footer of every page `src: Core features > The public surface`
- [ ] `C-CF-90` `ui` A terms page at /terms is reachable from the footer of every page `src: Core features > The public surface`
- [ ] `C-CF-91` `ui` The terms page is linked from the sign-up form `src: Core features > The public surface`
- [ ] `C-CF-92` `contract` Every internal link on every public route resolves `src: Core features > The public surface`
- [ ] `C-CF-93` `contract` A sitemap at /sitemap.xml lists every public route `src: Core features > The public surface`
- [ ] `C-CF-94` `contract` A robots file at /robots.txt names the sitemap `src: Core features > The public surface`
- [ ] `C-CF-95` `ui` Each page leads with exactly one primary action, visually distinct from every secondary one `src: Core features > The public surface`
- [ ] `C-CF-96` `contract` An unknown address renders the product not-found page, answering as not found `src: Core features > The public surface`
- [ ] `C-CF-97` `ui` The command menu opens on the platform modifier plus K on every route `src: Core features > The public surface`
- [ ] `C-CF-98` `ui` Skip to content is the first focusable element on every route `src: Core features > The public surface`
- [ ] `C-CF-99` `ui` The pricing matrix is a real table whose cells announce plan plus feature `src: Core features > The public surface`
- [ ] `C-CF-100` `ui` The feature search filters matrix rows in place, keeping focus, keeping group headers with surviving children `src: Core features > The public surface`
- [ ] `C-CF-101` `ui` Below the medium container the matrix collapses to one column driven by a plan select `src: Core features > The public surface`
- [ ] `C-CF-102` `ui` Every form rejects invalid input inline, naming the field, writing nothing `src: Core features > The public surface`
- [ ] `C-CF-103` `ui` A failed submit moves focus to the first invalid field `src: Core features > The public surface`
- [ ] `C-CF-104` `contract` A repeated lead submission inside the idempotency window returns the first result `src: Core features > The public surface`
- [ ] `C-CF-105` `ui` A simulation module is inert, none of its controls navigating, submitting, or mutating `src: Core features > The public surface`
- [ ] `C-CF-106` `ui` A simulation module is one labelled figure in the tab order, its controls not focusable `src: Core features > The public surface`
- [ ] `C-CF-107` `ui` A simulation module announces its numbers as illustrative rather than as the reader's own `src: Core features > The public surface`
- [ ] `C-CF-108` `ui` Facets combine as a union inside one group, as an intersection across groups, reflected in the address `src: Core features > The public surface`
- [ ] `C-CF-109` `ui` Template results extend by a control rather than on scroll `src: Core features > The public surface`
- [ ] `C-CF-110` `ui` An editorial index page carries a canonical address per page `src: Core features > The public surface`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated request for a console route redirects to /login carrying the requested path as a return target `src: User flow`
- [ ] `C-UF-02` `contract` A return target is validated against an allowlist of internal paths, never a full address `src: User flow`
- [ ] `C-UF-03` `ui` After login the principal lands on the return target, or on /northwind when none was given `src: User flow`
- [ ] `C-UF-04` `ui` Visit Your Firewall routes a signed-out visitor through /login with a return target `src: User flow`
- [ ] `C-UF-05` `ui` Logging out clears the session, returning to / `src: User flow`
- [ ] `C-UF-06` `role` A principal reaching an unentitled route sees the same refusal a missing resource produces `src: User flow`
- [ ] `C-UF-07` `ui` Raising a promotion request runs across three addressed steps ending in a full-page confirmation `src: User flow`
- [ ] `C-UF-08` `ui` The approve control is not offered to the requester on their own request `src: User flow`
- [ ] `C-UF-09` `ui` Every list carries an empty state naming what would appear plus how to create the first one `src: User flow`
- [ ] `C-UF-10` `ui` Every page carries a loading state sized to the content that is coming `src: User flow`
- [ ] `C-UF-11` `ui` A failing section renders its own error inside its own frame carrying the request identifier `src: User flow`
- [ ] `C-UF-12` `ui` One failing panel never blanks the shell `src: User flow`
- [ ] `C-UF-13` `ui` A conflict renders as a screen naming what changed plus a refetch control `src: User flow`
- [ ] `C-UF-14` `ui` A rate-limited action renders the wait `src: User flow`
- [ ] `C-UF-15` `ui` No error leaves a blank page or crashes the app `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Body text meets WCAG AA at four point five to one against its ground `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Large text plus interface components meet three to one `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The focus ring carries two stops, a hairline of page ground inside the accent `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The focus ring is present on every focusable element in both themes `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The accent is a mid vivid blue used for focus plus links, appearing on nothing else `src: UI/UX notes`
- [ ] `C-UX-06` `ui` A failure colour, a success colour, a pending colour each carry one meaning, appearing nowhere else `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Headings render at the display stroke step between normal plus bold, never rounded up to bold `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Body copy is sixteen pixels with twenty-four pixel leading `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Figures align wherever amounts stack `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Elevation is a hairline border plus the faintest shadow rather than a soft glow `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Motion character is eased, one short duration across every interactive element `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The overshoot curve is reserved for overlays, applying to movement plus fade only `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Under reduced motion nothing loops, nothing enters, no content is lost `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Reveals fire once on approach, never reversing on the way back up `src: UI/UX notes`
- [ ] `C-UX-15` `ui` The page is delivered already revealed, being hidden a frame later `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Every hover treatment sits behind a pointer-capability query `src: UI/UX notes`
- [ ] `C-UX-17` `ui` No behaviour depends on hover alone `src: UI/UX notes`
- [ ] `C-UX-18` `ui` A data table becomes a card per row below the medium container `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Wide decorative geometry is cropped plus enlarged rather than compressed `src: UI/UX notes`
- [ ] `C-UX-20` `ui` The document reflows at four hundred percent zoom with no horizontal scrollbar `src: UI/UX notes`
- [ ] `C-UX-21` `ui` Everything operable by pointer is operable by keyboard `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Tab order follows visual order, no positive tab index existing anywhere `src: UI/UX notes`
- [ ] `C-UX-23` `ui` Dialogs plus drawers trap focus, restoring focus to the control that opened them `src: UI/UX notes`
- [ ] `C-UX-24` `ui` Every icon-only control carries an accessible name describing what happens `src: UI/UX notes`
- [ ] `C-UX-25` `ui` A deployment state chip carries its state as text beside its colour `src: UI/UX notes`
- [ ] `C-UX-26` `ui` No information is carried by colour alone anywhere `src: UI/UX notes`
- [ ] `C-UX-27` `ui` A live region exists in the document before being populated `src: UI/UX notes`
- [ ] `C-UX-28` `ui` One h1 per document matching the visible title, heading levels descending without skipping `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is Preact with Vite, served as a production static build `src: Technical requirements`
- [ ] `C-TR-02` `contract` The backend is FastAPI on Python 3.12 behind Uvicorn `src: Technical requirements`
- [ ] `C-TR-03` `contract` The API is served under /api on the same origin as the frontend `src: Technical requirements`
- [ ] `C-TR-04` `contract` The backend serves the built frontend for every non-API path so a deep link renders `src: Technical requirements`
- [ ] `C-TR-05` `literal` PostgreSQL is reachable at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-06` `literal` Keycloak is reachable at `AUTH_ISSUER_URL` with `AUTH_CLIENT_ID` plus `AUTH_CLIENT_SECRET` `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced `src: Technical requirements`
- [ ] `C-TR-08` `contract` GET /api/health is unauthenticated, returning 200 once the database is reachable `src: Technical requirements`
- [ ] `C-TR-09` `capability` One authorization decision function runs in the request path for every request, reads included `src: Technical requirements`
- [ ] `C-TR-10` `capability` The application connects as a role with no bypass privilege, the store filtering every row by scope `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No application query supplies its own tenant filter `src: Technical requirements`
- [ ] `C-TR-12` `contract` An unknown field on a write is refused rather than ignored `src: Technical requirements`
- [ ] `C-TR-13` `contract` Every string carries a maximum length, every collection a maximum size, every number a range `src: Technical requirements`
- [ ] `C-TR-14` `contract` Every response carries a request identifier matching the log line plus the audit record `src: Technical requirements`
- [ ] `C-TR-15` `contract` An error body carries a stable snake-case code, a message, the request identifier, a documentation path `src: Technical requirements`
- [ ] `C-TR-16` `constraint` No error response contains a stack trace, a query, an internal hostname, a table name, another tenant identifier `src: Technical requirements`
- [ ] `C-TR-17` `contract` Every response carries strict transport security, a content security policy, content type options `src: Technical requirements`
- [ ] `C-TR-18` `constraint` Frame ancestors are denied on console plus identity routes `src: Technical requirements`
- [ ] `C-TR-19` `constraint` No secret is ever placed in an address `src: Technical requirements`
- [ ] `C-TR-20` `contract` A secret value is never returned by any read endpoint after creation `src: Technical requirements`
- [ ] `C-TR-21` `contract` Paging is keyset, a limit plus an opaque cursor returning the next cursor `src: Technical requirements`
- [ ] `C-TR-22` `contract` Every timestamp is an instant with an offset, no local time appearing in the contract `src: Technical requirements`
- [ ] `C-TR-23` `capability` Every live surface is also fetchable `src: Technical requirements`
- [ ] `C-TR-24` `capability` Rate limits apply per address, per principal, per organisation, the strictest winning `src: Technical requirements`
- [ ] `C-TR-25` `contract` A rate-limited response carries a retry hint `src: Technical requirements`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The mark is drawn geometry in four forms rather than an image file `src: Front-end specification`
- [ ] `C-FE-02` `ui` Every icon is drawn geometry on a sixteen-unit grid filled with the current colour `src: Front-end specification`
- [ ] `C-FE-03` `ui` A navigation panel opens on hover after an intent delay, on click without one `src: Front-end specification`
- [ ] `C-FE-04` `ui` Only one navigation panel is open at a time, moving between triggers cross-fading `src: Front-end specification`
- [ ] `C-FE-05` `ui` The banner slot contributes its height to layout so sticky offsets stay correct `src: Front-end specification`
- [ ] `C-FE-06` `ui` No route requires an image file to render `src: Front-end specification`
- [ ] `C-FE-07` `ui` Every skeleton is sized to the content standing in for `src: Front-end specification`
- [ ] `C-FE-08` `ui` Headings are sentence case except product names plus proper nouns `src: Front-end specification`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are stored in UTC `src: Data model`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`, written into `/app/USER_README.md` `src: Data model`
- [ ] `C-DM-03` `data` A team belongs to exactly one organisation `src: Data model`
- [ ] `C-DM-04` `data` A membership role is one of developer, reviewer, finance, viewer `src: Data model`
- [ ] `C-DM-05` `data` No two membership rows share a team plus an account `src: Data model`
- [ ] `C-DM-06` `data` A project has exactly one environment whose kind is production, enforced by the store `src: Data model`
- [ ] `C-DM-07` `data` A deployment environment must belong to the same project as the deployment `src: Data model`
- [ ] `C-DM-08` `data` A host plus path may name only one alias `src: Data model`
- [ ] `C-DM-09` `data` The gathered approval count is derived on read from the decision rows `src: Data model`
- [ ] `C-DM-10` `data` A request plus a principal may appear only once among approval decisions `src: Data model`
- [ ] `C-DM-11` `data` An audit sequence value occurs only once within its organisation `src: Data model`
- [ ] `C-DM-12` `literal` The seeded teams are `northwind` on plan pro plus `atlas` on plan hobby `src: Data model`
- [ ] `C-DM-13` `literal` The seeded projects are `checkout-web` in northwind plus `atlas-site` in atlas `src: Data model`
- [ ] `C-DM-14` `literal` The seeded deployments on checkout-web are `a1b2c3d` READY, `9988776` LIVE, `5544332` SUPERSEDED `src: Data model`
- [ ] `C-DM-15` `literal` The production alias for checkout-web is `checkout-web.meridian.test` `src: Data model`
- [ ] `C-DM-16` `literal` The seeded access group is `release-reviewers`, holding both reviewer accounts `src: Data model`
- [ ] `C-DM-17` `data` Seeding is idempotent, a restart duplicating no rows `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No real build execution happens, a build being a recorded state machine `src: Constraints`
- [ ] `C-CN-02` `constraint` No public sign-up, password reset, invitation acceptance flow exists `src: Constraints`
- [ ] `C-CN-03` `constraint` The app stays responsive with two hundred deployments plus two thousand audit records `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at APP_PUBLIC_URL `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is APP_PUBLIC_PORT to the container-internal 4173 `src: Deployment contract`
- [ ] `C-DC-03` `contract` Both port values are read from the environment, neither being hardcoded `src: Deployment contract`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the /api prefix `src: Deployment contract`
- [ ] `C-DC-05` `contract` GET /api/health returns 200 once the app is ready `src: Deployment contract`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-07` `contract` Login credentials are written to /app/USER_README.md `src: Deployment contract`
- [ ] `C-DC-08` `contract` Reserved .browser_screenshots plus .downloads directories exist empty at the app root `src: Deployment contract`
- [ ] `C-DC-09` `contract` A production build is served behind a static or preview server, never a dev server `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends, never as a child of the shell `src: Deployment contract`
- [ ] `C-DC-11` `contract` The server binds 0.0.0.0 rather than a loopback address `src: Deployment contract`
- [ ] `C-DC-12` `constraint` The backing services are not downloaded, installed, compiled, started by the app `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No edge functions are used `src: Deployment contract`
- [ ] `C-DC-14` `constraint` No persistent volumes, fixed container names, custom networks are declared `src: Deployment contract`
- [ ] `C-DC-15` `contract` Every list endpoint returns a top-level JSON array `src: Deployment contract`
- [ ] `C-DC-16` `contract` An invalid or unauthorized call is rejected as a client error, never a 5xx, never a silent success `src: Deployment contract`
- [ ] `C-DC-17` `contract` POST /api/webhooks/git authenticates by signature, never by a user token `src: Deployment contract`
- [ ] `C-DC-18` `contract` GET /api/deployments returns id, commit, state, environment, preview address, creation time `src: Deployment contract`
- [ ] `C-DC-19` `contract` GET /api/promotions returns id, deployment, state, requester, required approvals, gathered approvals `src: Deployment contract`
- [ ] `C-DC-20` `contract` POST /api/promotions/{id}/approve returns the request with its new gathered count plus state `src: Deployment contract`
- [ ] `C-DC-21` `contract` GET /api/audit returns sequence, time, actor, actor kind, action, resource, outcome, reason `src: Deployment contract`
- [ ] `C-DC-22` `contract` GET /api/aliases returns host, path, deployment, previous deployment, assignment time `src: Deployment contract`
- [ ] `C-DC-23` `contract` POST /api/firewall/rules/preview returns a would-match count over the last hour window `src: Deployment contract`
- [ ] `C-DC-24` `contract` GET /api/spend returns the cap, the used amount, the cap action, the lag, in integer cents `src: Deployment contract`
- [ ] `C-DC-25` `constraint` A fact the product asserts lives in PostgreSQL rather than in application memory `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the password every seeded account signs in with | `C-RL-21` |
| `developer@example.com` | the seeded developer in northwind | `C-RL-20` |
| `reviewer@example.com` | the first seeded reviewer in northwind | `C-RL-20` |
| `reviewer2@example.com` | the second seeded reviewer in northwind | `C-RL-20` |
| `finance@example.com` | the seeded finance principal in northwind | `C-RL-20` |
| `viewer@example.com` | the seeded viewer in northwind | `C-RL-20` |
| `developer2@example.com` | the seeded developer in atlas | `C-RL-20` |
| `/northwind/checkout-web` | the console address of the seeded project | `C-CF-16` |
| `QUEUED` | a deployment state | `C-CF-24` |
| `BUILDING` | a deployment state | `C-CF-24` |
| `READY` | a deployment state | `C-CF-24` |
| `ERROR` | a deployment state | `C-CF-24` |
| `CANCELED` | a deployment state | `C-CF-24` |
| `PROMOTING` | a deployment state | `C-CF-24` |
| `LIVE` | a deployment state carried by the alias | `C-CF-24` |
| `SUPERSEDED` | a deployment state | `C-CF-24` |
| `Production two-eyes` | the seeded approval policy name | `C-CF-32` |
| `1` | the seeded approval policy version | `C-CF-32` |
| `2` | the approvals the seeded policy requires | `C-CF-32` |
| `release-reviewers` | the eligible access group | `C-CF-32` |
| `OPEN` | a promotion request state | `C-CF-33` |
| `APPROVED` | a promotion request state | `C-CF-33` |
| `REJECTED` | a promotion request state | `C-CF-33` |
| `EXPIRED` | a promotion request state | `C-CF-33` |
| `EXECUTED` | a promotion request state | `C-CF-33` |
| `FAILED` | a promotion request state | `C-CF-33` |
| `SOC 2 Type 2` | a claimed compliance regime | `C-CF-62` |
| `PCI DSS` | a claimed compliance regime | `C-CF-62` |
| `ISO 27001` | a claimed compliance regime | `C-CF-62` |
| `EU-U.S. DPF` | a claimed compliance regime | `C-CF-62` |
| `HIPAA BAA` | a claimed compliance regime | `C-CF-62` |
| `TISAX` | a claimed compliance regime | `C-CF-62` |
| `allow` | a firewall rule action | `C-CF-63` |
| `deny` | a firewall rule action | `C-CF-63` |
| `challenge` | a firewall rule action | `C-CF-63` |
| `log` | a firewall rule action | `C-CF-63` |
| `rate-limit` | a firewall rule action | `C-CF-63` |
| `bypass` | a firewall rule action | `C-CF-63` |
| `Log request starting with /` | a seeded firewall rule | `C-CF-66` |
| `Challenge user agents that look like bots` | a seeded firewall rule | `C-CF-66` |
| `Deny traffic from Germany` | a seeded firewall rule | `C-CF-66` |
| `3` | the Hobby custom rule cap | `C-CF-67` |
| `40` | the Pro custom rule cap | `C-CF-67` |
| `1000` | the Enterprise custom rule cap | `C-CF-67` |
| `100` | the Pro address block cap | `C-CF-68` |
| `0` | the Hobby system bypass cap, also the Hobby monthly price | `C-CF-69` |
| `25` | the Pro system bypass cap | `C-CF-69` |
| `2000` | the Pro monthly price in integer minor units | `C-CF-75` |
| `notify` | a spend hard-cap action | `C-CF-78` |
| `restrict` | a spend hard-cap action | `C-CF-78` |
| `pause` | a spend hard-cap action | `C-CF-78` |
| `AVG` | a query aggregate | `C-CF-84` |
| `SUM` | a query aggregate | `C-CF-84` |
| `MAX` | a query aggregate | `C-CF-84` |
| `MIN` | a query aggregate | `C-CF-84` |
| `count` | a query aggregate | `C-CF-84` |
| `p50` | a query percentile | `C-CF-84` |
| `p75` | a query percentile | `C-CF-84` |
| `p90` | a query percentile | `C-CF-84` |
| `p95` | a query percentile | `C-CF-84` |
| `p99` | a query percentile | `C-CF-84` |
| `/` | the home route | `C-CF-88` |
| `/pricing` | a public route | `C-CF-88` |
| `/enterprise` | a public route | `C-CF-88` |
| `/security` | a public route | `C-CF-88` |
| `/docs` | a public route | `C-CF-88` |
| `/templates` | a public route | `C-CF-88` |
| `/blog` | a public route | `C-CF-88` |
| `/changelog` | a public route | `C-CF-88` |
| `/customers` | a public route | `C-CF-88` |
| `/ai` | a public route | `C-CF-88` |
| `/i` | a public route | `C-CF-88` |
| `/login` | the sign-in route | `C-CF-88` |
| `/signup` | the sign-up route | `C-CF-88` |
| `DATABASE_URL` | the PostgreSQL connection variable | `C-TR-05` |
| `AUTH_ISSUER_URL` | the Keycloak realm variable | `C-TR-06` |
| `AUTH_CLIENT_ID` | the Keycloak client identifier variable | `C-TR-06` |
| `AUTH_CLIENT_SECRET` | the Keycloak client secret variable | `C-TR-06` |
| `/app/USER_README.md` | where the seeded logins are written | `C-DM-02` |
| `northwind` | the first seeded team slug | `C-DM-12` |
| `atlas` | the second seeded team slug | `C-DM-12` |
| `checkout-web` | the first seeded project slug | `C-DM-13` |
| `atlas-site` | the second seeded project slug | `C-DM-13` |
| `a1b2c3d` | the READY seeded deployment commit | `C-DM-14` |
| `9988776` | the LIVE seeded deployment commit | `C-DM-14` |
| `5544332` | the SUPERSEDED seeded deployment commit | `C-DM-14` |
| `checkout-web.meridian.test` | the production alias host | `C-DM-15` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| The exact shade of every neutral, accent, status colour | `C-UX-05` |
| The exact corner radius, control heights, spacing ladder values | `C-UX-10` |
| The exact transition duration, easing curve for interactive elements | `C-UX-11` |
| The exact breakpoint widths between the five named tiers | `C-UX-18` |
| The exact identifier format for a deployment, a request, an audit row | `C-DM-16` |
| The exact wording of an empty state per surface | `C-UF-11` |
| The exact retry hint value on a rate-limited response | `C-TR-23` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 5 | 5 |
| User roles | 6 | 22 |
| Core features | 51 | 110 |
| User flow | 12 | 15 |
| UI and UX notes | 7 | 28 |
| Technical requirements | 22 | 25 |
| Front-end specification | 3 | 8 |
| Data model | 8 | 17 |
| Constraints | 1 | 3 |
| Deployment contract | 15 | 25 |
