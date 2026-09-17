# Checklist: Vocalis Console

Items: 215
Unpinned values flagged: 0
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-1` `capability` The product is a console for an organisation that buys metered speech recognition. `src: Overview`
- [ ] `C-OV-2` `capability` An organisation holds projects as the unit of isolation, of metering, of configuration. `src: Overview`
- [ ] `C-OV-3` `capability` A credential is a principal in its own right, never a stand-in for the person who created one. `src: Overview`

## C-RL User roles

- [ ] `C-RL-1` `role` An owner reads the organisation, every project, all usage, invoices, the balance ledger, the audit record. `src: User roles`
- [ ] `C-RL-2` `role` An owner writes organisation settings, projects, member roles, credentials, approval decisions. `src: User roles`
- [ ] `C-RL-3` `role` An administrator writes projects, ordinary credentials, member roles up to the administrator's own level. `src: User roles`
- [ ] `C-RL-4` `role` An administrator is refused reading an invoice. `src: User roles`
- [ ] `C-RL-5` `role` An administrator is refused reading the audit record. `src: User roles`
- [ ] `C-RL-6` `role` A member writes nothing beyond playground requests, revoking a credential the member issued. `src: User roles`
- [ ] `C-RL-7` `role` A member is refused creating a project. `src: User roles`
- [ ] `C-RL-8` `role` An auditor reads the audit record. `src: User roles`
- [ ] `C-RL-9` `role` An auditor writes nothing at all. `src: User roles`
- [ ] `C-RL-10` `role` An auditor is refused using the playground. `src: User roles`
- [ ] `C-RL-11` `contract` A direct call from a member session to an owner-only endpoint is refused by the server. `src: User roles`
- [ ] `C-RL-12` `contract` A refused call leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-13` `constraint` Signup is closed, so no registration form exists. `src: User roles`
- [ ] `C-RL-14` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`
- [ ] `C-RL-15` `literal` The seeded owner is `owner@example.com`. `src: User roles`
- [ ] `C-RL-16` `literal` The seeded second owner is `owner2@example.com`. `src: User roles`
- [ ] `C-RL-17` `literal` The seeded administrator is `admin@example.com`. `src: User roles`
- [ ] `C-RL-18` `literal` The seeded member is `member@example.com`. `src: User roles`
- [ ] `C-RL-19` `literal` The seeded denied member is `member2@example.com`. `src: User roles`
- [ ] `C-RL-20` `literal` The seeded auditor is `auditor@example.com`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-1` `capability` A correct email with a correct password returns a bearer token. `src: Core features > Auth`
- [ ] `C-CF-2` `capability` A wrong password is refused identically to an unknown email. `src: Core features > Auth`
- [ ] `C-CF-3` `capability` Signing out invalidates the token. `src: Core features > Auth`
- [ ] `C-CF-4` `contract` A call carrying an invalidated token is refused. `src: Core features > Auth`
- [ ] `C-CF-5` `constraint` No response body carries a password. `src: Core features > Auth`
- [ ] `C-CF-6` `constraint` No response body carries a session token beyond the sign-in reply. `src: Core features > Auth`
- [ ] `C-CF-7` `capability` The organisation switcher lists only organisations the principal belongs to. `src: Core features > The console shell`
- [ ] `C-CF-8` `capability` The project switcher lists only projects the principal can read. `src: Core features > The console shell`
- [ ] `C-CF-9` `capability` Changing organisation clears the project selection. `src: Core features > The console shell`
- [ ] `C-CF-10` `capability` Changing organisation lands the principal on the organisation overview. `src: Core features > The console shell`
- [ ] `C-CF-11` `contract` A project identifier from the previous organisation reaches no screen in the newly selected one. `src: Core features > The console shell`
- [ ] `C-CF-12` `capability` Search returns no resource the principal cannot read. `src: Core features > The console shell`
- [ ] `C-CF-13` `ui` Each screen leads with one primary action distinct from every secondary control. `src: Core features > The console shell`
- [ ] `C-CF-14` `capability` Creating a project opens a modal on the project index. `src: Core features > Projects`
- [ ] `C-CF-15` `data` An archived project keeps its usage readable after archiving. `src: Core features > Projects`
- [ ] `C-CF-16` `contract` A member attempting to create a project is denied. `src: Core features > Projects`
- [ ] `C-CF-17` `contract` No project is created by a denied attempt. `src: Core features > Projects`
- [ ] `C-CF-18` `capability` Archiving a project is terminal, so no project is ever deleted. `src: Core features > Projects`
- [ ] `C-CF-19` `data` An archived project keeps every metering row the project already had. `src: Core features > Projects`
- [ ] `C-CF-20` `data` An archived project keeps every invoice line the project already had. `src: Core features > Projects`
- [ ] `C-CF-21` `contract` A project the principal may not read is reported as not found rather than as forbidden. `src: Core features > Projects`
- [ ] `C-CF-22` `data` A credential carries exactly one project, fixed at creation. `src: Core features > Scoped credentials`
- [ ] `C-CF-23` `literal` A credential secret is forty characters beginning `vclk`. `src: Core features > Scoped credentials`
- [ ] `C-CF-24` `data` A credential prefix is the first eight characters of the secret. `src: Core features > Scoped credentials`
- [ ] `C-CF-25` `data` A credential prefix is unique across every credential. `src: Core features > Scoped credentials`
- [ ] `C-CF-26` `capability` A credential secret is shown exactly once, at creation. `src: Core features > Scoped credentials`
- [ ] `C-CF-27` `ui` The one-time secret appears on a full-page confirmation that requires acknowledgement before dismissal. `src: Core features > Scoped credentials`
- [ ] `C-CF-28` `contract` No endpoint returns a credential secret after creation. `src: Core features > Scoped credentials`
- [ ] `C-CF-29` `contract` No credential index row carries a secret field. `src: Core features > Scoped credentials`
- [ ] `C-CF-30` `data` The stored form of a secret is a hash that cannot be reversed. `src: Core features > Scoped credentials`
- [ ] `C-CF-31` `contract` An unknown prefix is refused identically to a wrong secret. `src: Core features > Scoped credentials`
- [ ] `C-CF-32` `capability` A revoke call returns the credential carrying a revoked state. `src: Core features > Scoped credentials`
- [ ] `C-CF-33` `contract` A revoked credential is refused from the instant of revocation. `src: Core features > Scoped credentials`
- [ ] `C-CF-34` `literal` The elevated scopes are `manage:keys` plus `admin:project`. `src: Core features > Scoped credentials`
- [ ] `C-CF-35` `capability` A request for an elevated credential records an approval request instead of issuing one. `src: Core features > Scoped credentials`
- [ ] `C-CF-36` `contract` An elevated credential issues only when a different owner approves the request. `src: Core features > Scoped credentials`
- [ ] `C-CF-37` `contract` A request approved by the principal who raised one issues no credential. `src: Core features > Scoped credentials`
- [ ] `C-CF-38` `data` An issued elevated credential carries a mandatory expiry. `src: Core features > Scoped credentials`
- [ ] `C-CF-39` `contract` A submission by a revoked credential writes no metering row. `src: Core features > Scoped credentials`
- [ ] `C-CF-40` `ui` A credential never used renders the word `never` in the last-used cell. `src: Core features > Scoped credentials`
- [ ] `C-CF-41` `literal` Credential status is one of `active`, `expiring`, `expired`, `revoked`. `src: Core features > Scoped credentials`
- [ ] `C-CF-42` `capability` Submitting a clip for recognition returns the transcript of the clip. `src: Core features > The playground`
- [ ] `C-CF-43` `capability` Submitting a clip for recognition returns the accuracy as a percentage to one decimal place. `src: Core features > The playground`
- [ ] `C-CF-44` `capability` Submitting a clip for recognition returns the latency of the request in milliseconds. `src: Core features > The playground`
- [ ] `C-CF-45` `literal` The clip `Quarterly Review Call` runs `180` audio seconds at accuracy `97.4%`. `src: Core features > The playground`
- [ ] `C-CF-46` `literal` The clip `Support Voicemail` runs `45` audio seconds at accuracy `92.1%`. `src: Core features > The playground`
- [ ] `C-CF-47` `literal` The clip `Product Demo` runs `120` audio seconds at accuracy `95.8%`. `src: Core features > The playground`
- [ ] `C-CF-48` `data` A playground recognition writes exactly one metering row attributed to the submitting project. `src: Core features > The playground`
- [ ] `C-CF-49` `data` A playground recognition raises the project open-period total by the clip duration. `src: Core features > The playground`
- [ ] `C-CF-50` `contract` A playground request against an archived project is refused. `src: Core features > The playground`
- [ ] `C-CF-51` `contract` An auditor attempting a playground request is denied. `src: Core features > The playground`
- [ ] `C-CF-52` `data` A failed playground request meters nothing. `src: Core features > The playground`
- [ ] `C-CF-53` `capability` Submitting text for synthesis returns the count of characters accepted. `src: Core features > The playground`
- [ ] `C-CF-54` `contract` The usage intake verifies a presented credential by prefix followed by hash comparison. `src: Core features > The metering intake`
- [ ] `C-CF-55` `contract` The usage intake refuses a revoked credential. `src: Core features > The metering intake`
- [ ] `C-CF-56` `contract` The usage intake refuses a credential lacking the scope for the submitted line. `src: Core features > The metering intake`
- [ ] `C-CF-57` `data` A refused submission writes no metering row. `src: Core features > The metering intake`
- [ ] `C-CF-58` `data` A submission repeating an idempotency key already seen writes no second row. `src: Core features > The metering intake`
- [ ] `C-CF-59` `data` A submission repeating an idempotency key already seen moves no total. `src: Core features > The metering intake`
- [ ] `C-CF-60` `data` An event is attributed to the project the presenting credential belongs to. `src: Core features > The metering intake`
- [ ] `C-CF-61` `contract` An archived project accepts no new metering row. `src: Core features > The metering intake`
- [ ] `C-CF-62` `data` A metering row records the occurrence time separately from the time of writing. `src: Core features > The metering intake`
- [ ] `C-CF-63` `capability` A usage screen takes a date range. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-64` `ui` A usage screen shows a stacked area chart above a table of the same figures. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-65` `data` The chart figures equal the table figures on one usage screen. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-66` `data` A usage total equals the sum of the rows beneath one total, exactly. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-67` `literal` For `2026-08-01` to `2026-08-31` the project `Contact Centre` totals `5400` audio seconds. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-68` `literal` For the same range the project `Contact Centre` totals `6500` characters. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-69` `literal` For the same range the project `Voice Notes` totals `1500` audio seconds. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-70` `literal` For the same range the organisation `Northwind Audio` totals `7200` audio seconds. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-71` `data` An organisation usage figure excludes every project the reading principal may not read. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-72` `literal` The same range read by `member2@example.com` totals `5700` audio seconds. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-73` `data` An event occurring inside an already finalised period restates the daily figures of that period. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-74` `data` An event occurring inside an already finalised period leaves the invoice total unchanged. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-75` `ui` A range holding no usage shows an empty state on the chart alongside the table. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-76` `capability` A project exceeding the trailing average by a configured multiple is surfaced as a notification. `src: Core features > Usage and reconciliation`
- [ ] `C-CF-77` `data` A balance is an append-only ledger rather than a mutable number. `src: Core features > Billing`
- [ ] `C-CF-78` `data` A balance equals the sum of the entries of that balance. `src: Core features > Billing`
- [ ] `C-CF-79` `literal` The organisation `Northwind Audio` holds a balance of `900` minor units. `src: Core features > Billing`
- [ ] `C-CF-80` `data` No ledger entry is ever updated. `src: Core features > Billing`
- [ ] `C-CF-81` `data` An invoice number is allocated at finalisation rather than at draft. `src: Core features > Billing`
- [ ] `C-CF-82` `data` Invoice numbers run gaplessly per legal entity. `src: Core features > Billing`
- [ ] `C-CF-83` `literal` The next number `Northwind Audio Ltd` allocates is `NW-2026-0002`. `src: Core features > Billing`
- [ ] `C-CF-84` `data` A finalised invoice is never updated. `src: Core features > Billing`
- [ ] `C-CF-85` `data` An invoice total equals the sum of the lines of that invoice. `src: Core features > Billing`
- [ ] `C-CF-86` `literal` The invoice `NW-2026-0001` totals `19100` minor units. `src: Core features > Billing`
- [ ] `C-CF-87` `contract` An administrator attempting to read an invoice is denied. `src: Core features > Billing`
- [ ] `C-CF-88` `data` Money is held as an integer count of minor units. `src: Core features > Billing`
- [ ] `C-CF-89` `literal` The roles are `owner`, `administrator`, `member`, `auditor`. `src: Core features > Roles`
- [ ] `C-CF-90` `data` A per-project override names a principal, a permission, an effect. `src: Core features > Roles`
- [ ] `C-CF-91` `contract` An explicit project deny defeats the organisation role that would otherwise grant. `src: Core features > Roles`
- [ ] `C-CF-92` `contract` An approval by a second owner returns the issued credential secret. `src: Core features > Roles`
- [ ] `C-CF-93` `contract` A self-approved request leaves the credential count unchanged. `src: Core features > Roles`
- [ ] `C-CF-94` `data` A refused project creation leaves the project count unchanged. `src: Core features > Roles`
- [ ] `C-CF-95` `data` Every credential issue appends one row to the audit record. `src: Core features > Roles`
- [ ] `C-CF-96` `data` Every refusal appends one row to the audit record. `src: Core features > Roles`
- [ ] `C-CF-97` `data` A blank project name is rejected as a client error. `src: Core features > Roles`
- [ ] `C-CF-98` `data` An event caused by a credential names the credential as the actor. `src: Core features > Roles`
- [ ] `C-CF-99` `ui` A terms page is reachable from the footer of every page. `src: Core features > The public surface`
- [ ] `C-CF-100` `ui` The terms page is linked from the sign-in form. `src: Core features > The public surface`
- [ ] `C-CF-101` `ui` An address matching no route renders the not-found page of the product. `src: Core features > The public surface`
- [ ] `C-CF-102` `contract` An address matching no route answers with a not-found result. `src: Core features > The public surface`
- [ ] `C-CF-103` `ui` Every internal link on every reachable page resolves. `src: Core features > The public surface`
- [ ] `C-CF-104` `contract` Every response carries a strict transport policy header. `src: Core features > The public surface`
- [ ] `C-CF-105` `contract` Every response carries a content-type policy header refusing sniffing. `src: Core features > The public surface`
- [ ] `C-CF-106` `ui` A form rejects invalid input in place, naming the offending field. `src: Core features > The public surface`
- [ ] `C-CF-107` `data` A form rejecting invalid input writes nothing. `src: Core features > The public surface`

## C-UF User flow

- [ ] `C-UF-1` `literal` The sign-in route is `/sign-in`. `src: User flow`
- [ ] `C-UF-2` `literal` The organisation overview route is `/overview`. `src: User flow`
- [ ] `C-UF-3` `literal` The project index route is `/projects`. `src: User flow`
- [ ] `C-UF-4` `literal` The organisation usage route is `/usage`. `src: User flow`
- [ ] `C-UF-5` `literal` The billing route is `/billing`. `src: User flow`
- [ ] `C-UF-6` `literal` The approvals route is `/approvals`. `src: User flow`
- [ ] `C-UF-7` `literal` The audit route is `/audit`. `src: User flow`
- [ ] `C-UF-8` `literal` The terms route is `/terms`. `src: User flow`
- [ ] `C-UF-9` `capability` An unauthenticated request for a protected route goes to the sign-in route. `src: User flow`
- [ ] `C-UF-10` `capability` A successful sign-in opens the originally requested route. `src: User flow`
- [ ] `C-UF-11` `capability` A sign-in with no held destination lands on the organisation overview. `src: User flow`
- [ ] `C-UF-12` `contract` An expired token mid-action refuses the action, writing nothing. `src: User flow`
- [ ] `C-UF-13` `ui` Every list carries an empty state naming what is missing. `src: User flow`
- [ ] `C-UF-14` `ui` A failed request shows a banner in place, leaving the shell standing. `src: User flow`
- [ ] `C-UF-15` `ui` A second playground submit is refused during the flight of the first. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The page ground is a near-black neutral that almost nothing brightens. `src: UI/UX notes`
- [ ] `C-UX-2` `ui` Running text is a light neutral rather than white. `src: UI/UX notes`
- [ ] `C-UX-3` `ui` White is reserved for headings alongside primary control labels. `src: UI/UX notes`
- [ ] `C-UX-4` `ui` The brand green is a mid, vivid teal. `src: UI/UX notes`
- [ ] `C-UX-5` `ui` The focus ring is a light, soft blue. `src: UI/UX notes`
- [ ] `C-UX-6` `ui` Depth is carried by coloured glow rather than by conventional shadow. `src: UI/UX notes`
- [ ] `C-UX-7` `ui` A primary action carries a horizontal glow pair with no vertical offset. `src: UI/UX notes`
- [ ] `C-UX-8` `literal` The display face is `Space Grotesk`. `src: UI/UX notes`
- [ ] `C-UX-9` `literal` The text face is `Inter`. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Figures that stack in a column are set in tabular figures. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Density is compact, so a full credential list reads in one screen. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Motion is eased, so nothing overshoots. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` A heading settles downward into place rather than rising into place. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` A reduced-motion preference stops every self-running animation. `src: UI/UX notes`
- [ ] `C-UX-15` `ui` The product commits to dark mode with no light mode implied. `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Contrast meets WCAG AA in the committed dark mode. `src: UI/UX notes`
- [ ] `C-UX-17` `ui` A visible focus ring accompanies full keyboard navigation. `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Meaning is never carried by colour alone. `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Below the phone tier a console table becomes stacked cards. `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Nothing overflows sideways at any viewport width. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` The sign-in page is served as complete HTML carrying its own links. `src: Technical requirements`
- [ ] `C-TR-2` `contract` The terms page is served as complete HTML carrying its own links. `src: Technical requirements`
- [ ] `C-TR-3` `contract` Every console route arrives as complete HTML on first paint. `src: Technical requirements`
- [ ] `C-TR-4` `literal` Storage is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-5` `constraint` The metering rows are readable from the declared PostgreSQL backend. `src: Technical requirements`
- [ ] `C-TR-6` `constraint` The daily rollup rows are readable from the declared PostgreSQL backend. `src: Technical requirements`
- [ ] `C-TR-7` `contract` The console session token identifies a user. `src: Technical requirements`
- [ ] `C-TR-8` `contract` The usage intake bearer token identifies a credential. `src: Technical requirements`
- [ ] `C-TR-9` `data` Passwords are stored hashed. `src: Technical requirements`
- [ ] `C-TR-10` `contract` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements`
- [ ] `C-TR-11` `constraint` Nothing in the browser bundle carries a credential. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` Every response carries a referrer policy header. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-1` `data` All timestamps are stored in coordinated universal time. `src: Data model`
- [ ] `C-DM-2` `data` Every table carrying tenant data carries a tenant column. `src: Data model`
- [ ] `C-DM-3` `literal` The seeded organisations are `Northwind Audio` alongside `Halyard Labs`. `src: Data model`
- [ ] `C-DM-4` `literal` The seeded project `Contact Centre` carries the slug `contact-centre`. `src: Data model`
- [ ] `C-DM-5` `literal` The seeded project `Voice Notes` carries the slug `voice-notes`. `src: Data model`
- [ ] `C-DM-6` `literal` The seeded project `Meeting Capture` is archived. `src: Data model`
- [ ] `C-DM-7` `literal` The seeded credential on `Contact Centre` carries the prefix `vclk2f8a`. `src: Data model`
- [ ] `C-DM-8` `literal` The seeded credential on `Meeting Capture` carries the prefix `vclk6b1d`. `src: Data model`
- [ ] `C-DM-9` `data` The project `Voice Notes` holds no credential at seed time. `src: Data model`
- [ ] `C-DM-10` `literal` The rate card `2026-01` prices `recognize.stream` at `2` minor units per audio second. `src: Data model`
- [ ] `C-DM-11` `literal` The seeded grant on `Northwind Audio` is `20000` minor units. `src: Data model`
- [ ] `C-DM-12` `literal` The seeded drawdown on `Northwind Audio` is `-19100` minor units. `src: Data model`
- [ ] `C-DM-13` `data` A daily rollup is recomputable from the metering rows beneath one rollup. `src: Data model`
- [ ] `C-DM-14` `data` An idempotency key appears on at most one metering row. `src: Data model`
- [ ] `C-DM-15` `data` A repeat submission returns a success rather than an error. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` Surfaces step upward from the ground in four further near-black neutrals. `src: Front-end specification`
- [ ] `C-FE-2` `ui` The heading fill paints one phrase per heading with a cyan to teal ramp. `src: Front-end specification`
- [ ] `C-FE-3` `ui` Every mark is drawn as geometry rather than loaded as a file. `src: Front-end specification`
- [ ] `C-FE-4` `ui` Every mark carries an accessible label. `src: Front-end specification`
- [ ] `C-FE-5` `ui` Hover treatments are gated to a real pointer. `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` A marketing pricing address answers not found. `src: Constraints`
- [ ] `C-CN-2` `constraint` An audio streaming address answers not found. `src: Constraints`
- [ ] `C-CN-3` `constraint` An object upload address answers not found. `src: Constraints`
- [ ] `C-CN-4` `constraint` A mail preview address answers not found. `src: Constraints`
- [ ] `C-CN-5` `constraint` A payment address answers not found. `src: Constraints`
- [ ] `C-CN-6` `constraint` Nothing a principal reads includes a row from an organisation the principal does not belong to. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-2` `contract` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-3` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-4` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-5` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-6` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-7` `contract` A production build is served behind a static or preview server. `src: Deployment contract`
- [ ] `C-DC-8` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-9` `contract` The server binds `0.0.0.0` rather than a loopback address. `src: Deployment contract`
- [ ] `C-DC-10` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-11` `contract` An invalid call is rejected as a client error rather than as a server error. `src: Deployment contract`
- [ ] `C-DC-12` `contract` Bearer auth is required on every endpoint except sign-in, health, the terms page. `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | a pinned value in the brief | `C-RL-14` |
| `owner@example.com` | a pinned value in the brief | `C-RL-15` |
| `owner2@example.com` | a pinned value in the brief | `C-RL-16` |
| `admin@example.com` | a pinned value in the brief | `C-RL-17` |
| `member@example.com` | a pinned value in the brief | `C-RL-18` |
| `member2@example.com` | a pinned value in the brief | `C-RL-19` |
| `auditor@example.com` | a pinned value in the brief | `C-RL-20` |
| `vclk` | a pinned value in the brief | `C-CF-23` |
| `manage:keys` | a pinned value in the brief | `C-CF-34` |
| `admin:project` | a pinned value in the brief | `C-CF-34` |
| `active` | a pinned value in the brief | `C-CF-41` |
| `expiring` | a pinned value in the brief | `C-CF-41` |
| `expired` | a pinned value in the brief | `C-CF-41` |
| `revoked` | a pinned value in the brief | `C-CF-41` |
| `Quarterly Review Call` | a pinned value in the brief | `C-CF-45` |
| `180` | a pinned value in the brief | `C-CF-45` |
| `97.4%` | a pinned value in the brief | `C-CF-45` |
| `Support Voicemail` | a pinned value in the brief | `C-CF-46` |
| `45` | a pinned value in the brief | `C-CF-46` |
| `92.1%` | a pinned value in the brief | `C-CF-46` |
| `Product Demo` | a pinned value in the brief | `C-CF-47` |
| `120` | a pinned value in the brief | `C-CF-47` |
| `95.8%` | a pinned value in the brief | `C-CF-47` |
| `2026-08-01` | a pinned value in the brief | `C-CF-67` |
| `2026-08-31` | a pinned value in the brief | `C-CF-67` |
| `Contact Centre` | a pinned value in the brief | `C-CF-67` |
| `5400` | a pinned value in the brief | `C-CF-67` |
| `6500` | a pinned value in the brief | `C-CF-68` |
| `Voice Notes` | a pinned value in the brief | `C-CF-69` |
| `1500` | a pinned value in the brief | `C-CF-69` |
| `Northwind Audio` | a pinned value in the brief | `C-CF-70` |
| `7200` | a pinned value in the brief | `C-CF-70` |
| `5700` | a pinned value in the brief | `C-CF-72` |
| `900` | a pinned value in the brief | `C-CF-79` |
| `Northwind Audio Ltd` | a pinned value in the brief | `C-CF-83` |
| `NW-2026-0002` | a pinned value in the brief | `C-CF-83` |
| `NW-2026-0001` | a pinned value in the brief | `C-CF-86` |
| `19100` | a pinned value in the brief | `C-CF-86` |
| `owner` | a pinned value in the brief | `C-CF-89` |
| `administrator` | a pinned value in the brief | `C-CF-89` |
| `member` | a pinned value in the brief | `C-CF-89` |
| `auditor` | a pinned value in the brief | `C-CF-89` |
| `/sign-in` | a pinned value in the brief | `C-UF-1` |
| `/overview` | a pinned value in the brief | `C-UF-2` |
| `/projects` | a pinned value in the brief | `C-UF-3` |
| `/usage` | a pinned value in the brief | `C-UF-4` |
| `/billing` | a pinned value in the brief | `C-UF-5` |
| `/approvals` | a pinned value in the brief | `C-UF-6` |
| `/audit` | a pinned value in the brief | `C-UF-7` |
| `/terms` | a pinned value in the brief | `C-UF-8` |
| `Space Grotesk` | a pinned value in the brief | `C-UX-8` |
| `Inter` | a pinned value in the brief | `C-UX-9` |
| `DATABASE_URL` | a pinned value in the brief | `C-TR-4` |
| `Halyard Labs` | a pinned value in the brief | `C-DM-3` |
| `contact-centre` | a pinned value in the brief | `C-DM-4` |
| `voice-notes` | a pinned value in the brief | `C-DM-5` |
| `Meeting Capture` | a pinned value in the brief | `C-DM-6` |
| `vclk2f8a` | a pinned value in the brief | `C-DM-7` |
| `vclk6b1d` | a pinned value in the brief | `C-DM-8` |
| `2026-01` | a pinned value in the brief | `C-DM-10` |
| `recognize.stream` | a pinned value in the brief | `C-DM-10` |
| `2` | a pinned value in the brief | `C-DM-10` |
| `20000` | a pinned value in the brief | `C-DM-11` |
| `-19100` | a pinned value in the brief | `C-DM-12` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 3 |
| User roles | 1 | 20 |
| Core features | 18 | 107 |
| User flow | 10 | 15 |
| UI and UX notes | 3 | 20 |
| Technical requirements | 3 | 12 |
| Data model | 6 | 15 |
| Front-end specification | 0 | 5 |
| Constraints | 1 | 6 |
| Deployment contract | 12 | 12 |
