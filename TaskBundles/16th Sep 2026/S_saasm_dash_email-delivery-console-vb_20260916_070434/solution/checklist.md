# Checklist: deku/email-delivery-console-vb

Items: 130
Unpinned values flagged: 4
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` A developer hands a message to the sending interface over HTTP `src: Overview`
- [ ] `C-OV-02` `capability` The console records what happened to every message afterwards `src: Overview`
- [ ] `C-OV-03` `constraint` The product omits a mailbox reading interface `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` An owner changes the workspace plan `src: User roles`
- [ ] `C-RL-02` `role` An admin verifies a sending domain `src: User roles`
- [ ] `C-RL-03` `role` A member composes a broadcast draft `src: User roles`
- [ ] `C-RL-04` `role` A member minting a credential is denied `src: User roles`
- [ ] `C-RL-05` `role` A member sending a broadcast to a live audience is denied `src: User roles`
- [ ] `C-RL-06` `literal` Every seeded account signs in with `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-07` `capability` Signup stays open to any visitor `src: User roles`
- [ ] `C-RL-08` `role` A credential secret stays hidden from everybody after creation `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` Signup creates a person carrying a display name `src: Core features`
- [ ] `C-CF-02` `contract` Login returns an access token `src: Core features`
- [ ] `C-CF-03` `contract` A duplicate signup address is rejected as invalid `src: Core features`
- [ ] `C-CF-04` `contract` A wrong password login is denied `src: Core features`
- [ ] `C-CF-05` `contract` A console request carrying no bearer token is denied `src: Core features`
- [ ] `C-CF-06` `contract` Adding a domain creates a pending domain `src: Core features`
- [ ] `C-CF-07` `data` A created domain generates three publication records `src: Core features`
- [ ] `C-CF-08` `data` Each domain record carries its own status value `src: Core features`
- [ ] `C-CF-09` `contract` A verification pass refreshes every record status `src: Core features`
- [ ] `C-CF-10` `data` A domain missing a record stays pending `src: Core features`
- [ ] `C-CF-11` `data` A domain whose records read correct becomes verified `src: Core features`
- [ ] `C-CF-12` `contract` A domain owned by another workspace answers as not found `src: Core features`
- [ ] `C-CF-13` `contract` Minting a credential returns the secret exactly once `src: Core features`
- [ ] `C-CF-14` `data` A credential row stores a twelve-character prefix `src: Core features`
- [ ] `C-CF-15` `contract` Listing credentials omits every secret `src: Core features`
- [ ] `C-CF-16` `contract` A revoked credential presented for sending is denied `src: Core features`
- [ ] `C-CF-17` `role` A member minting a credential writes no credential row `src: Core features`
- [ ] `C-CF-18` `contract` A credential minting another credential is denied `src: Core features`
- [ ] `C-CF-19` `contract` The sending interface accepts a message from a verified domain `src: Core features`
- [ ] `C-CF-20` `contract` A send from an unverified domain is refused `src: Core features`
- [ ] `C-CF-21` `contract` A send missing the idempotency key header is refused `src: Core features`
- [ ] `C-CF-22` `data` A replayed idempotency key produces no second message row `src: Core features`
- [ ] `C-CF-23` `contract` A replayed idempotency key carrying a different body is refused `src: Core features`
- [ ] `C-CF-24` `data` Two simultaneous sends under one key admit exactly one message `src: Core features`
- [ ] `C-CF-25` `contract` Retrieving a message returns its current state `src: Core features`
- [ ] `C-CF-26` `contract` Cancelling a queued message reaches the canceled state `src: Core features`
- [ ] `C-CF-27` `contract` A pinned credential sending from another domain is refused `src: Core features`
- [ ] `C-CF-28` `contract` A sending-scope credential reading domains is denied `src: Core features`
- [ ] `C-CF-29` `capability` The reserved delivered address produces a delivered event `src: Core features`
- [ ] `C-CF-30` `capability` The reserved bounced address produces a diagnostic `src: Core features`
- [ ] `C-CF-31` `capability` The reserved complained address produces a complaint event `src: Core features`
- [ ] `C-CF-32` `capability` An ordinary recipient receives real mail `src: Core features`
- [ ] `C-CF-33` `data` A hard bounce writes a suppression row for that address `src: Core features`
- [ ] `C-CF-34` `contract` A send to a suppressed address is refused before queueing `src: Core features`
- [ ] `C-CF-35` `contract` The log filters server-side by message state `src: Core features`
- [ ] `C-CF-36` `contract` A message detail returns events in occurrence order `src: Core features`
- [ ] `C-CF-37` `data` A late event is recorded without moving the state backwards `src: Core features`
- [ ] `C-CF-38` `contract` The overview counters match the underlying message rows `src: Core features`
- [ ] `C-CF-39` `data` The overview buckets sum to the counters exactly `src: Core features`
- [ ] `C-CF-40` `ui` Each overview counter links into the log pre-filtered `src: Core features`
- [ ] `C-CF-41` `ui` The current bucket is drawn as partial `src: Core features`
- [ ] `C-CF-42` `contract` Upserting a contact by address writes no duplicate row `src: Core features`
- [ ] `C-CF-43` `contract` Sending a broadcast writes a message per subscribed contact `src: Core features`
- [ ] `C-CF-44` `role` A member sending a broadcast leaves the broadcast unsent `src: Core features`
- [ ] `C-CF-45` `contract` Deleting a referenced audience is refused `src: Core features`
- [ ] `C-CF-46` `contract` Creating a notification endpoint returns a signing secret once `src: Core features`
- [ ] `C-CF-47` `data` A delivery attempt writes one notification row `src: Core features`
- [ ] `C-CF-48` `contract` A notification replay keeps the original event identifier `src: Core features`
- [ ] `C-CF-49` `contract` Usage returns the metered count beside the allowance `src: Core features`
- [ ] `C-CF-50` `contract` A send past the monthly allowance is refused `src: Core features`
- [ ] `C-CF-51` `capability` Reserved relay addresses stay unmetered `src: Core features`
- [ ] `C-CF-52` `ui` A workspace switcher lists every workspace membership `src: Core features`
- [ ] `C-CF-53` `ui` The terms route is readable by a signed-out visitor `src: Core features`
- [ ] `C-CF-54` `ui` A signup form refuses an invalid address inline `src: Core features`
- [ ] `C-CF-55` `ui` An unknown address renders the product not-found page `src: Core features`
- [ ] `C-CF-56` `ui` Every internal link on a reachable route resolves `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated console request redirects to the login route `src: User flow`
- [ ] `C-UF-02` `contract` A signed-in visitor opening the login route lands on the overview `src: User flow`
- [ ] `C-UF-03` `ui` Every list route offers an empty state naming the missing thing `src: User flow`
- [ ] `C-UF-04` `ui` A route in flight shows a skeleton rather than a spinner `src: User flow`
- [ ] `C-UF-05` `ui` A refused request renders its reason in place `src: User flow`
- [ ] `C-UF-06` `ui` A filter matching nothing keeps the filter visible `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-black neutral edge to edge `src: UI/UX notes`
- [ ] `C-UX-02` `ui` A state chip carries its word beside its colour `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The primary action reads distinct from every secondary control `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Entrances travel a short distance with eased motion `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Body text meets the WCAG AA contrast bar `src: UI/UX notes`
- [ ] `C-UX-06` `ui` A narrow viewport collapses the rail to icons `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The backend serves JSON under the api prefix `src: Technical requirements`
- [ ] `C-TR-02` `contract` The frontend ships as a built production bundle `src: Technical requirements`
- [ ] `C-TR-03` `capability` The datastore is reached at the database environment variable `src: Technical requirements`
- [ ] `C-TR-04` `capability` Mail leaves over SMTP to the mail sidecar `src: Technical requirements`
- [ ] `C-TR-05` `contract` The health route answers without a token `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every response carries a request identifier header `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every response carries a nosniff content-type header `src: Technical requirements`
- [ ] `C-TR-08` `contract` Every response carries a strict transport security header `src: Technical requirements`
- [ ] `C-TR-09` `contract` An authenticated response carries a no-store cache header `src: Technical requirements`
- [ ] `C-TR-10` `constraint` Nothing the browser downloads carries a credential `src: Technical requirements`
- [ ] `C-TR-11` `contract` A versioned list response carries a cursor page envelope `src: Technical requirements`
- [ ] `C-TR-12` `contract` An error body carries a type beside a request identifier `src: Technical requirements`
- [ ] `C-TR-13` `contract` A validation failure reports every failing field `src: Technical requirements`
- [ ] `C-TR-14` `data` Two simultaneous contact creates admit exactly one row `src: Technical requirements`
- [ ] `C-TR-15` `contract` Every response carries the rate limit budget headers `src: Technical requirements`
- [ ] `C-TR-16` `contract` A caller over the send budget is refused `src: Technical requirements`
- [ ] `C-TR-17` `capability` A deprecated interface version answers with sunset headers `src: Technical requirements`
- [ ] `C-TR-18` `contract` An unknown field on a write is refused `src: Technical requirements`
- [ ] `C-TR-19` `data` An address is normalised before comparison `src: Technical requirements`
- [ ] `C-TR-20` `capability` A deferred message records its attempt number `src: Technical requirements`
- [ ] `C-TR-21` `capability` A notification delivery retries after a server error `src: Technical requirements`
- [ ] `C-TR-22` `capability` Every log line carries a request identifier `src: Technical requirements`
- [ ] `C-TR-23` `capability` A rollup figure states the instant computed `src: Technical requirements`
- [ ] `C-TR-24` `contract` The permissions policy denies camera access `src: Technical requirements`
- [ ] `C-TR-25` `contract` The post-sign-in return path stays relative to the serving origin `src: Technical requirements`
- [ ] `C-TR-26` `data` Every external identifier carries a type prefix `src: Technical requirements`
- [ ] `C-TR-27` `constraint` A password reaches a stated minimum length `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Every stored timestamp is UTC `src: Data model`
- [ ] `C-DM-02` `data` A message row records its state beside an idempotency key `src: Data model`
- [ ] `C-DM-03` `data` A message event row is appended rather than updated `src: Data model`
- [ ] `C-DM-04` `data` Deleting a domain keeps every message already sent `src: Data model`
- [ ] `C-DM-05` `data` Seeding runs idempotently across a restart `src: Data model`
- [ ] `C-DM-06` `data` The seeded workspace carries three membership roles `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Identifiers sit in a monospace face with tabular figures `src: Front-end specification`
- [ ] `C-FE-02` `ui` Interface text is set in Inter `src: Front-end specification`
- [ ] `C-FE-03` `ui` Section boundaries are hairlines fading at both ends `src: Front-end specification`
- [ ] `C-FE-04` `ui` A pointed-at control appears to emit light `src: Front-end specification`
- [ ] `C-FE-05` `ui` The left rail groups sending destinations above marketing ones `src: Front-end specification`
- [ ] `C-FE-06` `ui` A label chip draws from a fixed hue set `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The build omits a payment processor `src: Constraints`
- [ ] `C-CN-02` `constraint` The build omits open tracking `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at the public url environment variable `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The server binds every interface rather than loopback `src: Deployment contract`
- [ ] `C-DC-04` `contract` The server outlives the session that started the process `src: Deployment contract`
- [ ] `C-DC-05` `contract` Every list endpoint returns a top-level JSON array `src: Deployment contract`
- [ ] `C-DC-06` `contract` Login, signup, health answer without a bearer token `src: Deployment contract`
- [ ] `C-DC-07` `constraint` The log reflects message rows stored in the named datastore `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served rather than a development server `src: Deployment contract`
- [ ] `C-DC-09` `constraint` Backing services are reached rather than started `src: Deployment contract`
- [ ] `C-DC-10` `contract` An unauthorized call is rejected as a client error `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded password | `C-RL-06` |
| `4173` | the container-internal port | `C-DC-02` |
| `owner@example.com` | the seeded owner account | `C-RL-01` |
| `admin@example.com` | the seeded admin account | `C-RL-02` |
| `member@example.com` | the seeded member account | `C-RL-03` |
| `owner2@example.com` | the second workspace owner | `C-CF-12` |
| `Northwind Relay` | the seeded workspace | `C-DM-06` |
| `Acme Relay` | the second seeded workspace | `C-CF-12` |
| `mail.northwind.example.com` | the seeded verified domain | `C-CF-11` |
| `docs.northwind.example.com` | the seeded pending domain | `C-CF-10` |
| `mail.acme.example.com` | the other workspace domain | `C-CF-12` |
| `delivered@relay.example.com` | the reserved delivered address | `C-CF-29` |
| `bounced@relay.example.com` | the reserved bounced address | `C-CF-30` |
| `complained@relay.example.com` | the reserved complained address | `C-CF-31` |
| `Launch List` | the seeded audience | `C-CF-43` |
| `sendline` | the record selector | `C-CF-07` |
| `skey_` | the credential secret opener | `C-CF-13` |
| `starter` | the seeded plan name | `C-CF-49` |
| `500` | the monthly allowance | `C-CF-50` |
| `queued` | the accepted message state | `C-CF-25` |
| `delivered` | the confirmed message state | `C-CF-29` |
| `bounced` | the returned message state | `C-CF-30` |
| `complained` | the junk-marked message state | `C-CF-31` |
| `canceled` | the withdrawn message state | `C-CF-26` |
| `pending` | the unverified domain state | `C-CF-06` |
| `verified` | the proven domain state | `C-CF-11` |
| `sending` | the narrow credential scope | `C-CF-28` |
| `full` | the wide credential scope | `C-CF-13` |
| `draft` | the unsent broadcast state | `C-RL-03` |
| `requested` | the broadcast state a member reaches | `C-CF-44` |
| `sent` | the finished broadcast state | `C-CF-43` |
| `Idempotency-Key` | the required send header | `C-CF-21` |
| `X-Request-Id` | the request identifier header | `C-TR-06` |
| `/api/health` | the health route | `C-TR-05` |
| `/api/v1/emails` | the send route | `C-CF-19` |
| `/api/overview` | the counters route | `C-CF-38` |
| `/api/usage` | the metering route | `C-CF-49` |
| `Production sender` | the credential minted in the journey | `C-CF-13` |

### Referenced but not pinned

| What | Item |
|---|---|
| the exact record host names a domain generates | `C-CF-07` |
| the exact bounce diagnostic text a receiving server returns | `C-CF-30` |
| the exact wording of a plain-language bounce reading | `C-CF-36` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 3 | 3 |
| User roles | 8 | 8 |
| Core features | 41 | 56 |
| User flow | 6 | 6 |
| UI and UX notes | 6 | 6 |
| Technical requirements | 27 | 27 |
| Data model | 6 | 6 |
| Front-end specification | 6 | 6 |
| Constraints | 2 | 2 |
| Deployment contract | 10 | 10 |
