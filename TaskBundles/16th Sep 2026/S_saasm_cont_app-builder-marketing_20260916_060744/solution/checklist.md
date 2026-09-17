# Checklist: Slate - App Builder Marketing Site

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, constraints, technical, datamodel, deployment, frontend
Sections absent: buildplan
Items: 130
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents seven public reading surfaces. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app presents one shared not-found surface. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The app presents a signed-in studio for the site's own authors. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The app carries the same primary action on every route. `src: Overview para 2`
- [ ] `C-OV-05` `constraint` The app excludes a visual editor. `src: Overview para 3`
- [ ] `C-OV-06` `constraint` The app keeps an unpublished article unreachable by anyone but its author. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An author creates records in all four collections. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An author publishes their own records. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An author uploads a cover for their own article. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An author is denied any record owned by another author. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A reader reads every published surface. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A reader is denied every authoring endpoint. `src: User roles table row 2`
- [ ] `C-RL-07` `role` An anonymous visitor reads every published surface. `src: User roles para 1`
- [ ] `C-RL-08` `role` An anonymous visitor files a build request. `src: User roles para 1`
- [ ] `C-RL-09` `constraint` The app enforces authorization server-side on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-10` `constraint` The app leaves protected state unchanged after a denied request. `src: User roles para 2`
- [ ] `C-RL-11` `capability` The app creates a reader account through open signup. `src: User roles para 3`
- [ ] `C-RL-12` `constraint` The app offers no self-serve author signup. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `capability` The app authenticates an account against a stored password hash. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `capability` The app issues a bearer token the client sends on every authenticated call. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `constraint` The app rejects a mutating call carrying an expired token. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `constraint` The app leaves a record unchanged after rejecting an expired token. `src: Core features, Auth para 1`
- [ ] `C-CF-05` `capability` A public collection route lists published records only. `src: Core features rule 1`
- [ ] `C-CF-06` `capability` A public collection route orders records newest first. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` The app serves a draft record only to the account in its author field. `src: Core features rule 2`
- [ ] `C-CF-08` `constraint` The app returns an identical denial whether or not a draft slug exists. `src: Core features rule 2`
- [ ] `C-CF-09` `constraint` The app holds at most one featured article at any time. `src: Core features rule 3`
- [ ] `C-CF-10` `capability` The app clears the previous featured article when a second is featured. `src: Core features rule 3`
- [ ] `C-CF-11` `constraint` The app leaves exactly one featured row after two simultaneous featuring requests. `src: Core features rule 3`
- [ ] `C-CF-12` `role` The app denies an author a record owned by another author. `src: Core features rule 4`
- [ ] `C-CF-13` `constraint` The app leaves the row unchanged after denying a cross-author request. `src: Core features rule 4`
- [ ] `C-CF-14` `constraint` The app omits a job with open false from the careers list. `src: Core features rule 5`
- [ ] `C-CF-15` `capability` The app resolves the route of a job with open false. `src: Core features rule 5`
- [ ] `C-CF-16` `capability` The app computes the careers department grouping on read. `src: Core features rule 5`
- [ ] `C-CF-17` `capability` The app writes a cover into the MinIO bucket. `src: Core features rule 6`
- [ ] `C-CF-18` `data` The app stores the cover key on the article row. `src: Core features rule 6`
- [ ] `C-CF-19` `constraint` The app keeps cover bytes off the application filesystem. `src: Core features rule 6`
- [ ] `C-CF-20` `constraint` The app keeps cover bytes out of every database column. `src: Core features rule 6`
- [ ] `C-CF-21` `capability` The app serves a published article's cover to any requester. `src: Core features rule 7`
- [ ] `C-CF-22` `constraint` The app serves a draft article's cover only to its author. `src: Core features rule 7`
- [ ] `C-CF-23` `constraint` The app issues no presigned read URL for a cover. `src: Core features rule 7`
- [ ] `C-CF-24` `ui` The app presents the prompt composer on every route. `src: Core features rule 8`
- [ ] `C-CF-25` `ui` The app pins the composer to the bottom of the viewport past the home hero. `src: Core features rule 8`
- [ ] `C-CF-26` `ui` The app preserves the composer's typed value across the pinning transition. `src: Core features rule 8`
- [ ] `C-CF-27` `capability` The app issues a presigned PUT grant for an attachment. `src: Core features rule 9`
- [ ] `C-CF-28` `literal` The app expires an attachment upload grant 300 seconds after issue. `src: Core features rule 9`
- [ ] `C-CF-29` `constraint` The app never proxies attachment bytes. `src: Core features rule 9`
- [ ] `C-CF-30` `capability` The app returns the same subscription response for a known address as for a new one. `src: Core features rule 10`

## C-UF User flow

- [ ] `C-UF-01` `capability` The app serves the home route at the site root. `src: User flow route table row 1`
- [ ] `C-UF-02` `capability` The app serves the editorial index at the blog route. `src: User flow route table row 4`
- [ ] `C-UF-03` `capability` The app serves the careers route. `src: User flow route table row 6`
- [ ] `C-UF-04` `capability` The app redirects an anonymous studio request to the login route. `src: User flow, Entry and redirects`
- [ ] `C-UF-05` `role` The app refuses a signed-in reader asking for the studio route. `src: User flow, Entry and redirects`
- [ ] `C-UF-06` `capability` The app sends an author to the studio route after signing in. `src: User flow, Entry and redirects`
- [ ] `C-UF-07` `capability` The app invalidates the token on sign-out. `src: User flow, Entry and redirects`
- [ ] `C-UF-08` `capability` The app renders the not-found surface for an unknown path. `src: User flow, Entry and redirects`
- [ ] `C-UF-09` `ui` The app shows an empty state on every collection surface. `src: User flow, States`
- [ ] `C-UF-10` `ui` The app shows a loading state on every route. `src: User flow, States`
- [ ] `C-UF-11` `ui` The app shows a message after a failed request without breaking the page. `src: User flow, States`
- [ ] `C-UF-12` `ui` The app anchors the footer to the viewport bottom on a route shorter than the viewport. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface reads as an operator's console rather than a brochure. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The studio sets type in monospace. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` A studio state change lands at once rather than easing in. `src: UI/UX notes para 3`
- [ ] `C-UX-04` `ui` The studio presents its records as a card grid beside a fixed rail. `src: UI/UX notes para 4`
- [ ] `C-UX-05` `ui` The studio opens record creation in a slide-over. `src: UI/UX notes para 4`
- [ ] `C-UX-06` `ui` One accent colour carries progress, documentation links, one large mark. `src: UI/UX notes para 5`
- [ ] `C-UX-07` `ui` The careers route carries a ground colour found on no other route. `src: UI/UX notes para 5`
- [ ] `C-UX-08` `ui` Every button is fully rounded at its ends. `src: UI/UX notes para 6`
- [ ] `C-UX-09` `ui` Every text surface meets WCAG AA contrast. `src: UI/UX notes para 7`
- [ ] `C-UX-10` `ui` Every control is reachable by keyboard with a visible focus ring. `src: UI/UX notes para 7`
- [ ] `C-UX-11` `ui` The layout holds at every viewport width between the named tiers. `src: UI/UX notes para 7`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app sends no email. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` The app makes no outbound network call at run time. `src: Constraints para 1`
- [ ] `C-CN-03` `constraint` The app uses no backing service the brief does not name. `src: Constraints para 1`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app serves its HTTP API under the /api prefix on the assets origin. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app reads PostgreSQL from DATABASE_URL. `src: Technical requirements para 3`
- [ ] `C-TR-03` `contract` The app reads MinIO from STORAGE_ENDPOINT. `src: Technical requirements para 3`
- [ ] `C-TR-04` `literal` The app names a cover object covers/{article_slug}/{sha256_of_bytes}.{ext}. `src: Technical requirements, Object keys para 1`
- [ ] `C-TR-05` `literal` The app names an attachment object build-requests/{request_id}/{sha256_of_bytes}.{ext}. `src: Technical requirements, Object keys para 1`
- [ ] `C-TR-06` `literal` The app rejects an attachment larger than 26214400 bytes. `src: Technical requirements, Object keys para 2`
- [ ] `C-TR-07` `constraint` The app decides an attachment's type by reading its content. `src: Technical requirements, Object keys para 2`
- [ ] `C-TR-08` `literal` The app rejects a build request prompt longer than 4000 characters. `src: Technical requirements, Object keys para 2`
- [ ] `C-TR-09` `capability` The app returns the request identifier in the build-request response. `src: Technical requirements, Object keys para 2`
- [ ] `C-TR-10` `capability` The app serves the question set as structured data at /api/questions. `src: Technical requirements, Object keys para 3`
- [ ] `C-TR-11` `capability` The app serves every documentation page as plain text at a derived path. `src: Technical requirements, Object keys para 3`
- [ ] `C-TR-12` `capability` The app paginates the press digest on the server. `src: Technical requirements, pagination para`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-02` `literal` Every seeded account uses the password deku-demo-pw-2026. `src: Data model, password callout`
- [ ] `C-DM-03` `contract` The app writes each seeded account into /app/USER_README.md. `src: Data model, password callout`
- [ ] `C-DM-04` `data` The app holds a unique slug on every article. `src: Data model, articles para`
- [ ] `C-DM-05` `data` The app sets published_at exactly when an article's status is published. `src: Data model, articles para`
- [ ] `C-DM-06` `data` The app holds 3 to 5 summary entries on a press item. `src: Data model, press_items para`
- [ ] `C-DM-07` `data` The app seeds the account author@example.com. `src: Data model, seed data para 1`
- [ ] `C-DM-08` `data` The app seeds the account author2@example.com. `src: Data model, seed data para 1`
- [ ] `C-DM-09` `data` The app seeds the account reader@example.com. `src: Data model, seed data para 1`
- [ ] `C-DM-10` `data` The app seeds the draft article agents-reading-your-schema owned by author@example.com. `src: Data model, seed data para 2`
- [ ] `C-DM-11` `data` The app seeds the published article spreadsheet-to-app-in-an-afternoon as featured. `src: Data model, seed data para 2`
- [ ] `C-DM-12` `data` The app seeds the closed job field-marketing-lead. `src: Data model, seed data para 4`
- [ ] `C-DM-13` `data` The app seeds the subscription subscriber@example.com as unconfirmed. `src: Data model, seed data para 6`
- [ ] `C-DM-14` `constraint` The app leaves row counts unchanged across a restart. `src: Data model, closing line`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at APP_PUBLIC_URL. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app listens on container-internal port 4173. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app answers GET /api/health with 200 once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-04` `contract` The app writes login credentials to /app/USER_README.md. `src: Deployment contract bullet 5`
- [ ] `C-DC-05` `contract` The app root holds an empty .browser_screenshots/ directory. `src: Deployment contract bullet 6`
- [ ] `C-DC-06` `contract` The app root holds an empty .downloads/ directory. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` The app serves a production build rather than a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds 0.0.0.0. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `contract` The app returns a top-level JSON array from GET /api/articles. `src: Deployment contract, API shapes table row 3`
- [ ] `C-DC-11` `contract` The app rejects an invalid call as a client error rather than a server error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-12` `constraint` The app records no article outside PostgreSQL. `src: Deployment contract, No mocks para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app serves the home route with the document title AI App Builder: Turn Spreadsheets into Business Apps. `src: Front-end specification, Information architecture para 1`
- [ ] `C-FE-02` `ui` The app renders the not-found surface for the path /e/ without an identifier. `src: Front-end specification, Information architecture para 1`
- [ ] `C-FE-03` `ui` The app carries five items in its primary navigation. `src: Front-end specification, Information architecture para 2`
- [ ] `C-FE-04` `ui` The app tokenises the documentation route separately from every other route. `src: Front-end specification, The two-layer reality`
- [ ] `C-FE-05` `ui` The app sets body text in one deep neutral that appears far more than any other. `src: Front-end specification, warm neutral ramp table row 7`
- [ ] `C-FE-06` `ui` The app uses one saturated teal as its accent on every route. `src: Front-end specification, accent and the chromatic set`
- [ ] `C-FE-07` `ui` The app grounds the careers route in a near-white warm neutral pear found on no other route. `src: Front-end specification, accent and the chromatic set`
- [ ] `C-FE-08` `ui` The app draws every hairline in one black alpha step. `src: Front-end specification, the alpha ladders`
- [ ] `C-FE-09` `ui` The display family renders normal text at 450 rather than at 400. `src: Front-end specification, Type families closing para`
- [ ] `C-FE-10` `ui` The app renders the composer placeholder Describe what you want to build.... `src: Front-end specification, Global chrome para 2`
- [ ] `C-FE-11` `ui` The app labels the composer attachment control Upload spreadsheet. `src: Front-end specification, Global chrome para 2`
- [ ] `C-FE-12` `ui` The app blurs the composer card ground by 12px. `src: Front-end specification, Global chrome para 2`
- [ ] `C-FE-13` `ui` The app draws the route progress bar 3px tall. `src: Front-end specification, Global chrome para 4`
- [ ] `C-FE-14` `ui` The app titles the editorial index The Column. `src: Front-end specification, Route compositions, Editorial index`
- [ ] `C-FE-15` `ui` The app writes a press item's date with the weekday spelled out. `src: Front-end specification, Route compositions, Press digest`
- [ ] `C-FE-16` `ui` The app expands the pagination range from the ellipsis button. `src: Front-end specification, Route compositions, Press digest`
- [ ] `C-FE-17` `ui` The app resolves every animation to its end state under prefers-reduced-motion. `src: Front-end specification, Motion language closing line`
- [ ] `C-FE-18` `ui` The app substitutes a single static composition for the hero on mobile. `src: Front-end specification, Responsive behaviour`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | seeded password for every account | C-DM-02 | Data model, password callout |
| `author@example.com` | seeded author account | C-DM-07 | Data model, seed data para 1 |
| `author2@example.com` | second seeded author account | C-DM-08 | Data model, seed data para 1 |
| `reader@example.com` | seeded reader account | C-DM-09 | Data model, seed data para 1 |
| `subscriber@example.com` | seeded unconfirmed subscription | C-DM-13 | Data model, seed data para 6 |
| `agents-reading-your-schema` | seeded draft article slug | C-DM-10 | Data model, seed data para 2 |
| `spreadsheet-to-app-in-an-afternoon` | seeded featured article slug | C-DM-11 | Data model, seed data para 2 |
| `field-marketing-lead` | seeded closed job slug | C-DM-12 | Data model, seed data para 4 |
| `/api/health` | health route | C-DC-03 | Deployment contract bullet 3 |
| `/api/questions` | structured question data route | C-TR-10 | Technical requirements, Object keys para 3 |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `300` | attachment grant lifetime in seconds | C-CF-28 | Core features rule 9 |
| `26214400` | maximum attachment size in bytes | C-TR-06 | Technical requirements, Object keys para 2 |
| `4000` | maximum prompt length in characters | C-TR-08 | Technical requirements, Object keys para 2 |
| deep neutral | body text colour, described rather than pinned | C-FE-05 | Front-end specification, warm neutral ramp |
| saturated teal | accent colour, described rather than pinned | C-FE-06 | Front-end specification, accent and the chromatic set |
| near-white warm neutral pear | careers ground, described rather than pinned | C-FE-07 | Front-end specification, accent and the chromatic set |
| black alpha step | default hairline, described rather than pinned | C-FE-08 | Front-end specification, the alpha ladders |
| `450` | the display family's normal setting | C-FE-09 | Front-end specification, Type families |
| `Describe what you want to build...` | composer placeholder | C-FE-10 | Front-end specification, Global chrome |
| `Upload spreadsheet` | composer attachment label | C-FE-11 | Front-end specification, Global chrome |
| `The Column` | editorial index title | C-FE-14 | Front-end specification, Route compositions |
| `covers/{article_slug}/{sha256_of_bytes}.{ext}` | cover object key scheme | C-TR-04 | Technical requirements, Object keys |
| `build-requests/{request_id}/{sha256_of_bytes}.{ext}` | attachment object key scheme | C-TR-05 | Technical requirements, Object keys |
| `DATABASE_URL` | PostgreSQL connection variable | C-TR-02 | Technical requirements para 3 |
| `STORAGE_ENDPOINT` | MinIO endpoint variable | C-TR-03 | Technical requirements para 3 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the token expiry window | C-CF-03 | the brief requires expiry without naming a duration |
| the named responsive tiers | C-UX-11 | the brief requires behaviour between tiers without pinning their widths |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 6 |
| User roles | 8 | 12 |
| Core features | 22 | 30 |
| User flow | 10 | 12 |
| UI and UX notes | 9 | 11 |
| Constraints | 3 | 3 |
| Technical requirements | 10 | 12 |
| Data model | 12 | 14 |
| Deployment contract | 12 | 12 |
| Front-end specification | 16 | 18 |
