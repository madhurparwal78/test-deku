# Checklist: Nimbus Payments Platform Console
Items: 190
Unpinned values flagged: 2
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` A public India storefront plus an authenticated console are served from one deployment. `src: Overview`
- [ ] `C-OV-02` `capability` An account is an organisation whose members hold different powers. `src: Overview`
- [ ] `C-OV-03` `capability` A pending refund request causes no movement of money before a decision. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A `support` member may create a refund at or below a ceiling of `500000` paise. `src: User roles table`
- [ ] `C-RL-02` `role` A `support` member may raise a refund request above the ceiling. `src: User roles table`
- [ ] `C-RL-03` `role` A `support` member may not approve any approval request. `src: User roles table`
- [ ] `C-RL-04` `role` A `finance` member may create a refund of any amount. `src: User roles table`
- [ ] `C-RL-05` `role` A `finance` member may approve a refund request another person raised. `src: User roles table`
- [ ] `C-RL-06` `role` A `finance` member may not approve a request the same member raised. `src: User roles table`
- [ ] `C-RL-07` `role` An `administrator` may not create a refund. `src: User roles table`
- [ ] `C-RL-08` `role` An `administrator` alone may read the audit log. `src: User roles table`
- [ ] `C-RL-09` `role` An `administrator` alone may read API credentials. `src: User roles table`
- [ ] `C-RL-10` `role` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-11` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles seeded accounts`

## C-CF Core features

- [ ] `C-CF-01` `contract` Login at `POST /api/auth/login` returns a bearer access token. `src: Core features rule 1`
- [ ] `C-CF-02` `contract` A wrong password is refused at login. `src: Core features rule 1`
- [ ] `C-CF-03` `contract` `GET /api/me` returns the signed-in person with every membership held. `src: Core features rule 3`
- [ ] `C-CF-04` `contract` `GET /api/accounts` returns only organisations the caller belongs to. `src: Core features rule 4`
- [ ] `C-CF-05` `contract` A member of one organisation reading another organisation's payment receives a not-found answer. `src: Core features rule 5`
- [ ] `C-CF-06` `contract` A console read defaults to the live environment when no environment parameter is given. `src: Core features rule 7`
- [ ] `C-CF-07` `contract` A sandbox payment identifier read under live is answered as not found. `src: Core features rule 8`
- [ ] `C-CF-08` `data` A payment carries a refunded total computed from non-failed refunds. `src: Core features rule 11`
- [ ] `C-CF-09` `data` A payment status is one of succeeded, partially_refunded, refunded, disputed. `src: Core features rule 12`
- [ ] `C-CF-10` `capability` A refund at or below the caller's ceiling writes a refund row at once. `src: Core features rule 15`
- [ ] `C-CF-11` `data` A refund at or below the ceiling debits the available balance by the refund amount. `src: Core features rule 15`
- [ ] `C-CF-12` `data` A refund covering the whole captured amount moves the payment status to refunded. `src: Core features rule 15`
- [ ] `C-CF-13` `literal` A refund above the caller's ceiling is refused with the code `approval_required`. `src: Core features rule 16`
- [ ] `C-CF-14` `constraint` A refund above the ceiling writes no refund row. `src: Core features rule 16`
- [ ] `C-CF-15` `ui` The refund composer shows the notice naming the caller's own limit. `src: Core features rule 16`
- [ ] `C-CF-16` `data` Raising a refund request stores a mandatory justification. `src: Core features rule 17`
- [ ] `C-CF-17` `constraint` A pending refund request leaves every balance unchanged. `src: Core features rule 18`
- [ ] `C-CF-18` `constraint` A pending refund request owns no ledger entry. `src: Core features rule 18`
- [ ] `C-CF-19` `literal` A refund request expires after the seconds named in `REFUND_REQUEST_TTL_SEC`. `src: Core features rule 17`
- [ ] `C-CF-20` `contract` The approval queue is ordered soonest to expire first. `src: Core features rule 19`
- [ ] `C-CF-21` `literal` Approving a request as the raiser is refused with the code `self_approval_forbidden`. `src: Core features rule 20`
- [ ] `C-CF-22` `role` Approving a request as a support member is denied by the server. `src: Core features rule 20`
- [ ] `C-CF-23` `constraint` A denied approval leaves the request state unchanged. `src: Core features rule 20`
- [ ] `C-CF-24` `ui` The approve control is absent on a request the viewer raised. `src: Core features rule 20`
- [ ] `C-CF-25` `capability` Approving a pending request writes exactly one refund. `src: Core features rule 21`
- [ ] `C-CF-26` `constraint` Approving a request a second time writes no second refund. `src: Core features rule 21`
- [ ] `C-CF-27` `data` An executed request records the deciding member, the decision time, the resulting refund. `src: Core features rule 21`
- [ ] `C-CF-28` `contract` Rejecting a request requires a note. `src: Core features rule 21a`
- [ ] `C-CF-29` `role` Withdrawing a request is permitted only to the requester who raised the request. `src: Core features rule 21b`
- [ ] `C-CF-30` `literal` Approving an expired request is refused with the code `approval_expired`. `src: Core features rule 22`
- [ ] `C-CF-31` `capability` Expiry of a request is computed when the row is read. `src: Core features rule 22`
- [ ] `C-CF-32` `literal` A refund larger than the remaining refundable amount is refused with the code `amount_too_large`. `src: Core features rule 23`
- [ ] `C-CF-33` `literal` A refund of a disputed payment is refused with the code `payment_disputed`. `src: Core features rule 24`
- [ ] `C-CF-34` `capability` Two simultaneous approvals of one request produce exactly one refund. `src: Core features rule 25`
- [ ] `C-CF-35` `capability` Replaying an idempotency key with an identical body creates nothing new. `src: Core features rule 26`
- [ ] `C-CF-36` `literal` Replaying an idempotency key with a different body is refused with the code `idempotency_conflict`. `src: Core features rule 26`
- [ ] `C-CF-37` `constraint` A refused refund leaves the underlying rows unchanged. `src: Core features rule 27`
- [ ] `C-CF-38` `data` The balances of one organisation, one environment, one currency sum to zero. `src: Core features rule 30`
- [ ] `C-CF-39` `data` Each balance equals the sum of the signed amounts of the matching ledger entries. `src: Core features rule 31`
- [ ] `C-CF-40` `data` The signed amounts of one ledger transaction sum to zero. `src: Core features rule 32`
- [ ] `C-CF-41` `data` An amount is an integer in the minor unit travelling with a currency code. `src: Core features rule 33`
- [ ] `C-CF-42` `data` A payout amount equals the sum of the net amounts of the listed transactions. `src: Core features rule 34`
- [ ] `C-CF-43` `data` A dispute moves the disputed amount out of the available balance. `src: Core features rule 36`
- [ ] `C-CF-44` `contract` The API credential list never returns a secret value. `src: Core features rule 38`
- [ ] `C-CF-45` `capability` Creating an API credential returns the secret value exactly once. `src: Core features rule 39`
- [ ] `C-CF-46` `data` A stored credential keeps only a hash plus a short display prefix. `src: Core features rule 40`
- [ ] `C-CF-47` `data` A revoked credential stays listed rather than being removed. `src: Core features rule 41`
- [ ] `C-CF-48` `literal` A webhook address on a loopback host is refused with the code `endpoint_address_forbidden`. `src: Core features rule 43`
- [ ] `C-CF-49` `constraint` A webhook address using plain transport is refused. `src: Core features rule 43`
- [ ] `C-CF-50` `contract` A webhook endpoint accepts only the nine named event types. `src: Core features rule 44`
- [ ] `C-CF-51` `data` An executed refund request produces an approval-approved event plus a refund-created event. `src: Core features rule 45`
- [ ] `C-CF-52` `data` Every mutation appends one audit record. `src: Core features rule 46`
- [ ] `C-CF-53` `data` Audit sequence numbers rise by one per organisation with no gap. `src: Core features rule 47`
- [ ] `C-CF-54` `data` Each audit record hash covers the previous record hash. `src: Core features rule 47`
- [ ] `C-CF-55` `constraint` No route edits an audit record. `src: Core features rule 49`
- [ ] `C-CF-56` `constraint` No route deletes an audit record. `src: Core features rule 49`
- [ ] `C-CF-57` `contract` A lead submission carrying a non-empty decoy field is refused. `src: Core features rule 70`
- [ ] `C-CF-58` `constraint` A refused lead submission writes no lead row. `src: Core features rule 70`
- [ ] `C-CF-59` `capability` A repeated identical lead submission returns the first lead identifier. `src: Core features rule 70`
- [ ] `C-CF-60` `contract` An unknown address answers not found. `src: Core features rule 73`
- [ ] `C-CF-61` `literal` The not-found page carries the copy `We cannot find that page.` `src: Core features rule 73`
- [ ] `C-CF-62` `literal` The gated product route carries the badge `Not available in your country`. `src: Core features rule 60`
- [ ] `C-CF-63` `literal` The gated product route offers the control `Join the waitlist`. `src: Core features rule 60`
- [ ] `C-CF-64` `ui` The gated product pricing band renders a note in place of prices. `src: Core features rule 60`
- [ ] `C-CF-65` `literal` The country home eyebrow reads `Global GDP running on Nimbus:`. `src: Core features rule 52`
- [ ] `C-CF-66` `literal` The country home lead sentence reads `Financial infrastructure to grow your revenue.` `src: Core features rule 52`
- [ ] `C-CF-67` `literal` The country home carries one primary control reading `Request an invite`. `src: Core features rule 52`
- [ ] `C-CF-68` `literal` The footer carries the locale label `India (English)`. `src: Core features rule 68`
- [ ] `C-CF-69` `literal` The footer carries the copyright line `(c) 2026 Nimbus`. `src: Core features rule 68`
- [ ] `C-CF-70` `ui` Amounts render under Indian digit grouping. `src: Core features rule 66`
- [ ] `C-CF-71` `literal` The sandbox band carries the copy `Sandbox. No real money moves here.` `src: UI/UX notes`
- [ ] `C-CF-72` `ui` The country home bands appear in the stated order. `src: Core features rule 51`
- [ ] `C-CF-73` `capability` The primary storefront control carries the product plus the locale into the lead form. `src: Core features rule 62`
- [ ] `C-CF-74` `capability` Filter state on an index route lives in the address. `src: Core features rule 63`
- [ ] `C-CF-75` `capability` The lead form works with client scripting unavailable. `src: Core features rule 71`

## C-UF User flow

- [ ] `C-UF-01` `contract` `/in` serves the country home. `src: User flow route table`
- [ ] `C-UF-02` `contract` `/in/billing` serves a light available product route. `src: User flow route table`
- [ ] `C-UF-03` `contract` `/in/guard` serves a dark available product route. `src: User flow route table`
- [ ] `C-UF-04` `contract` `/in/query` serves a gated product route. `src: User flow route table`
- [ ] `C-UF-05` `contract` `/in/guides` serves a filterable guides index. `src: User flow route table`
- [ ] `C-UF-06` `contract` `/in/customer-stories` serves a customer stories index. `src: User flow route table`
- [ ] `C-UF-07` `contract` `/in/pricing` serves prices in rupees. `src: User flow route table`
- [ ] `C-UF-08` `contract` `/sitemap.xml` lists every public route. `src: User flow route table`
- [ ] `C-UF-09` `contract` `/robots.txt` names the sitemap address. `src: User flow route table`
- [ ] `C-UF-10` `contract` `/signin` serves the console sign-in form. `src: User flow route table`
- [ ] `C-UF-11` `contract` `/accounts` serves the account chooser. `src: User flow route table`
- [ ] `C-UF-12` `ui` The payments route shows a list beside a detail pane. `src: User flow route table`
- [ ] `C-UF-13` `contract` The refund composer sits at a dedicated address beneath the payment. `src: User flow route table`
- [ ] `C-UF-14` `ui` The approval queue shows a queue beside a detail pane. `src: User flow route table`
- [ ] `C-UF-15` `capability` An anonymous request for a console address lands on the sign-in route. `src: User flow entry and redirects`
- [ ] `C-UF-16` `capability` A sign-in with two memberships lands on the account chooser. `src: User flow entry and redirects`
- [ ] `C-UF-17` `capability` A sign-in with one membership lands on that organisation's home. `src: User flow entry and redirects`
- [ ] `C-UF-18` `capability` A member opening an organisation not held is told the organisation was not found. `src: User flow entry and redirects`
- [ ] `C-UF-19` `ui` Every list carries an empty state naming what would appear there. `src: User flow states`
- [ ] `C-UF-20` `ui` A filtered list returning nothing names each active filter. `src: User flow states`
- [ ] `C-UF-21` `ui` A partial failure shows loaded rows with an inline retry for the failed range. `src: User flow states`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-white neutral. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The primary action is the only element on a page wearing the vivid blue. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Success, failure, in-progress each wear a colour used nowhere else. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` A refunded row wears a neutral rather than a meaning-bearing colour. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Elevation is two stacked shadows fading inward at the edges. `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Motion carries one character across the whole product. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` A reduced-motion visitor sees the finished frame rather than a blank one. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Every state badge carries a label plus a shape. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Body text meets a contrast ratio of at least 4.5 to 1 against the ground. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Interactive targets are no smaller than 44 by 44. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` The environment control never collapses at any viewport width. `src: UI/UX notes`
- [ ] `C-UX-12` `ui` A navigation group the member holds nothing in is absent from the rail. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Keyboard navigation reaches every control with a visible focus indicator. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The dense table becomes a list of cards at a phone breakpoint. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The browser layer is SolidJS built with Vite. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The server layer is Hono on Node 20. `src: Technical requirements`
- [ ] `C-TR-03` `literal` PostgreSQL is reached with the connection string in `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-04` `literal` Keycloak is reached at `AUTH_URL`. `src: Technical requirements`
- [ ] `C-TR-05` `literal` The realm name is read from `AUTH_REALM`. `src: Technical requirements`
- [ ] `C-TR-06` `literal` The client identifier is read from `AUTH_CLIENT_ID`. `src: Technical requirements`
- [ ] `C-TR-07` `literal` The client secret is read from `AUTH_CLIENT_SECRET`. `src: Technical requirements`
- [ ] `C-TR-08` `literal` The refund request lifetime is read from `REFUND_REQUEST_TTL_SEC`. `src: Technical requirements`
- [ ] `C-TR-09` `contract` The JSON API is served from the same origin as the pages. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No outbound network call is made at runtime. `src: Technical requirements`
- [ ] `C-TR-11` `capability` Authorization is decided once per request before the body is validated. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` A field the caller may not read is absent from the response. `src: Technical requirements`
- [ ] `C-TR-13` `capability` Every read carries an organisation predicate plus an environment predicate. `src: Technical requirements`
- [ ] `C-TR-14` `contract` One request identifier is returned on every response. `src: Technical requirements`
- [ ] `C-TR-15` `constraint` No response body carries a stored credential secret. `src: Technical requirements`
- [ ] `C-TR-16` `constraint` No console list route returns a total count of the collection. `src: Technical requirements`
- [ ] `C-TR-17` `capability` Pagination uses opaque cursors rather than offsets. `src: Technical requirements`
- [ ] `C-TR-18` `contract` The application serves a favicon declared in every document head. `src: Technical requirements`
- [ ] `C-TR-19` `contract` Every public route declares a social preview title plus a preview image. `src: Technical requirements`
- [ ] `C-TR-20` `contract` The sitemap is generated from the same route manifest the footer renders. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-02` `data` Every amount is an integer in the minor unit stored beside a currency code. `src: Data model`
- [ ] `C-DM-03` `data` Every console table carries an account column plus an environment column. `src: Data model`
- [ ] `C-DM-04` `constraint` A ledger entry is never updated. `src: Data model ledger_entry`
- [ ] `C-DM-05` `constraint` A ledger entry is never deleted. `src: Data model ledger_entry`
- [ ] `C-DM-06` `data` The sum of non-failed refunds of a payment never exceeds the captured amount. `src: Data model refund`
- [ ] `C-DM-07` `capability` Seeding is idempotent across restarts. `src: Data model seed data`
- [ ] `C-DM-08` `data` The seeded northbeam live available balance is `27226598` paise. `src: Data model seed data`
- [ ] `C-DM-09` `data` The seeded wellspring live available balance is `759200` paise. `src: Data model seed data`
- [ ] `C-DM-10` `data` The seeded northbeam sandbox available balance is `97700` paise. `src: Data model seed data`
- [ ] `C-DM-11` `data` The fee of a captured payment is two percent rounded half to even plus `300` paise. `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Display type scales continuously with the width of the window. `src: Front-end specification`
- [ ] `C-FE-02` `ui` Body type does not scale with the width of the window. `src: Front-end specification`
- [ ] `C-FE-03` `ui` The heaviest step of the type scale is `500`. `src: Front-end specification`
- [ ] `C-FE-04` `ui` The ordinary body step of the type scale is `300`. `src: Front-end specification`
- [ ] `C-FE-05` `literal` The code face is `SourceCodePro`. `src: Front-end specification`
- [ ] `C-FE-06` `ui` Console-dense text is set at `14px`. `src: Front-end specification`
- [ ] `C-FE-07` `ui` Body copy is set at `16px`. `src: Front-end specification`
- [ ] `C-FE-08` `ui` Icons are geometry drawn in the page rather than fetched files. `src: Front-end specification`
- [ ] `C-FE-09` `ui` The menu control becomes a cross by rotating two coincident bars. `src: Front-end specification`
- [ ] `C-FE-10` `ui` The four disclosures open one shared panel rather than four panels. `src: Front-end specification`
- [ ] `C-FE-11` `ui` Hover intent survives a diagonal pointer path into the panel. `src: Front-end specification`
- [ ] `C-FE-12` `ui` Section dividers lean rather than sitting level. `src: Front-end specification`
- [ ] `C-FE-13` `ui` A product demonstration is composed from markup rather than played as a video. `src: Front-end specification`
- [ ] `C-FE-14` `ui` A gradient numeral carries a solid fallback colour applied first. `src: Front-end specification`
- [ ] `C-FE-15` `ui` The fake browser window never becomes fully opaque. `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No subscriptions, invoices, usage meters exist in the product. `src: Constraints`
- [ ] `C-CN-02` `constraint` No email, push, outbound webhook delivery exists. `src: Constraints`
- [ ] `C-CN-03` `constraint` No background job, cron, scheduler, queue exists. `src: Constraints`
- [ ] `C-CN-04` `constraint` One currency, the Indian rupee, is served. `src: Constraints`
- [ ] `C-CN-05` `constraint` One locale, India in English, is served. `src: Constraints`
- [ ] `C-CN-06` `constraint` No cross-organisation data is visible at any address. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-03` `literal` The outside port is read from `APP_PUBLIC_PORT`. `src: Deployment contract`
- [ ] `C-DC-04` `literal` The HTTP API is served under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-05` `contract` `GET /api/health` returns `200`. `src: Deployment contract`
- [ ] `C-DC-06` `literal` Credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-07` `literal` A reserved `.browser_screenshots/` directory exists at the app root. `src: Deployment contract`
- [ ] `C-DC-08` `literal` A reserved `.downloads/` directory exists at the app root. `src: Deployment contract`
- [ ] `C-DC-09` `capability` The app serves without a manual step after the environment image starts. `src: Deployment contract`
- [ ] `C-DC-10` `capability` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-11` `literal` The server binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-12` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` An invalid request is rejected as a client error rather than a server error. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` An error body carries a stable machine-readable code. `src: Deployment contract API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded password | `C-RL-11` |
| `500000` | the support refund ceiling in paise | `C-RL-01` |
| `support` | the lower console role | `C-RL-01` |
| `finance` | the approving console role | `C-RL-04` |
| `administrator` | the governing console role | `C-RL-07` |
| `POST /api/auth/login` | the login endpoint | `C-CF-01` |
| `GET /api/me` | the identity endpoint | `C-CF-03` |
| `GET /api/accounts` | the organisation list endpoint | `C-CF-04` |
| `approval_required` | the above-ceiling refusal code | `C-CF-13` |
| `REFUND_REQUEST_TTL_SEC` | the request lifetime variable | `C-CF-19` |
| `self_approval_forbidden` | the self-approval refusal code | `C-CF-21` |
| `approval_expired` | the expired-request refusal code | `C-CF-30` |
| `amount_too_large` | the over-remainder refusal code | `C-CF-32` |
| `payment_disputed` | the disputed-payment refusal code | `C-CF-33` |
| `idempotency_conflict` | the key-reuse refusal code | `C-CF-36` |
| `endpoint_address_forbidden` | the unsafe-address refusal code | `C-CF-48` |
| `We cannot find that page.` | the not-found copy | `C-CF-61` |
| `Not available in your country` | the availability badge | `C-CF-62` |
| `Join the waitlist` | the gated primary control | `C-CF-63` |
| `Global GDP running on Nimbus:` | the hero eyebrow | `C-CF-65` |
| `Financial infrastructure to grow your revenue.` | the hero lead sentence | `C-CF-66` |
| `Request an invite` | the country home primary control | `C-CF-67` |
| `India (English)` | the locale control label | `C-CF-68` |
| `(c) 2026 Nimbus` | the copyright line | `C-CF-69` |
| `Sandbox. No real money moves here.` | the sandbox band copy | `C-CF-71` |
| `/in` | the country home route | `C-UF-01` |
| `/in/billing` | the billing product route | `C-UF-02` |
| `/in/guard` | the fraud product route | `C-UF-03` |
| `/in/query` | the gated product route | `C-UF-04` |
| `/in/guides` | the guides index route | `C-UF-05` |
| `/in/customer-stories` | the customer stories route | `C-UF-06` |
| `/in/pricing` | the pricing route | `C-UF-07` |
| `/sitemap.xml` | the sitemap route | `C-UF-08` |
| `/robots.txt` | the robots route | `C-UF-09` |
| `/signin` | the sign-in route | `C-UF-10` |
| `/accounts` | the account chooser route | `C-UF-11` |
| `DATABASE_URL` | the datastore connection variable | `C-TR-03` |
| `AUTH_URL` | the identity provider address variable | `C-TR-04` |
| `AUTH_REALM` | the realm name variable | `C-TR-05` |
| `AUTH_CLIENT_ID` | the client identifier variable | `C-TR-06` |
| `AUTH_CLIENT_SECRET` | the client secret variable | `C-TR-07` |
| `27226598` | the seeded northbeam live available balance | `C-DM-08` |
| `759200` | the seeded wellspring live available balance | `C-DM-09` |
| `97700` | the seeded northbeam sandbox available balance | `C-DM-10` |
| `300` | the flat part of the fee in paise | `C-DM-11` |
| `500` | the heaviest step of the type scale | `C-FE-03` |
| `14px` | the console-dense text size | `C-FE-06` |
| `16px` | the body copy size | `C-FE-07` |
| `SourceCodePro` | the code face | `C-FE-05` |
| `APP_PUBLIC_URL` | the public address variable | `C-DC-01` |
| `4173` | the container-internal port | `C-DC-02` |
| `APP_PUBLIC_PORT` | the outside port variable | `C-DC-03` |
| `/api` | the API prefix | `C-DC-04` |
| `GET /api/health` | the health endpoint | `C-DC-05` |
| `200` | the health response status | `C-DC-05` |
| `/app/USER_README.md` | the credential file path | `C-DC-06` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-07` |
| `.downloads/` | the reserved download directory | `C-DC-08` |
| `0.0.0.0` | the bind address | `C-DC-11` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact shade of every colour role | `C-UX-01` |
| the base spacing unit the layout is built on | `C-UX-05` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 3 |
| User roles | 4 | 11 |
| Core features | 37 | 75 |
| User flow | 16 | 21 |
| UI/UX notes | 9 | 14 |
| Technical requirements | 14 | 20 |
| Data model | 5 | 11 |
| Front-end specification | 11 | 15 |
| Constraints | 4 | 6 |
| Deployment contract | 12 | 14 |
