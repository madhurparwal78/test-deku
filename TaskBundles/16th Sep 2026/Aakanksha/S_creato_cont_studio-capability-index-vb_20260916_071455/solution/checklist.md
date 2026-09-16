# Checklist: studio-capability-index

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, buildplan, deployment
Sections absent: constraints
Items: 39
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` A visitor reads a published case study filtered by its industry. `src: Overview para 1`
- [ ] `C-OV-02` `capability` A draft case study is unreadable by the public until published. `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` An editor publishes content, manages records, reads the enquiries. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor reads published content with no account. `src: User roles table row 2`
- [ ] `C-RL-03` `contract` An anonymous caller to an editor endpoint is refused server side. `src: User roles para 1`

## C-CF Core features

- [ ] `C-CF-01` `capability` Login with a seeded editor returns a bearer token. `src: Core features Accounts and sessions`
- [ ] `C-CF-02` `capability` Signup with an already registered email is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-03` `capability` Signup with a password shorter than eight characters is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-04` `capability` The case study index lists only published case studies. `src: Core features Case studies filtered by industry`
- [ ] `C-CF-05` `capability` The case study index narrows to one selected industry. `src: Core features Case studies filtered by industry`
- [ ] `C-CF-06` `capability` A published case study loads its media from the object store. `src: Core features Case studies filtered by industry`
- [ ] `C-CF-07` `capability` A managed case study with an unknown industry is refused. `src: Core features Case studies filtered by industry`
- [ ] `C-CF-08` `contract` A draft case study detail returns not-found to the public. `src: Core features Draft protection`
- [ ] `C-CF-09` `contract` A draft case study media object is refused to the public. `src: Core features Draft protection`
- [ ] `C-CF-10` `capability` Publishing a draft makes the record public. `src: Core features Draft protection`
- [ ] `C-CF-11` `capability` A service detail shows a proof row of case studies that credited the service. `src: Core features Services index and detail`
- [ ] `C-CF-12` `capability` The article index shows published articles with one pinned. `src: Core features Articles, the wall and the shelf`
- [ ] `C-CF-13` `capability` The experiments wall appends the next page with a load more control. `src: Core features Articles, the wall and the shelf`
- [ ] `C-CF-14` `capability` A valid enquiry is persisted as one record. `src: Core features Project enquiry`
- [ ] `C-CF-15` `capability` An enquiry with a short message is refused naming the field. `src: Core features Project enquiry`
- [ ] `C-CF-16` `capability` The privacy page renders readable content. `src: Core features Static pages and error handling`
- [ ] `C-CF-17` `capability` The sitemap lists the published routes. `src: Core features Static pages and error handling`
- [ ] `C-CF-18` `capability` An unknown route renders a custom not-found page. `src: Core features Static pages and error handling`
- [ ] `C-CF-19` `capability` A page view is recorded for a public route. `src: Core features Static pages and error handling`

## C-UF User flow

- [ ] `C-UF-01` `ui` A submitted enquiry lands on an acknowledgement page. `src: User flow Journeys`
- [ ] `C-UF-02` `ui` Each list has a loading state, an empty state with a prompt. `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every status carries a text label so meaning never rides on colour alone. `src: UI/UX notes Palette`
- [ ] `C-UX-02` `ui` Motion is held to a minimum with no bounce. `src: UI/UX notes Motion`
- [ ] `C-UX-03` `ui` The grids reflow to a single column at the small breakpoint. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-04` `ui` Body text meets a readable contrast, every control shows a focus ring. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-05` `ui` A headline resolves out of a character scramble on first view. `src: UI/UX notes Motion`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` A server side secret never reaches the served frontend bundle. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Two submissions with one idempotency key create exactly one enquiry. `src: Technical requirements`
- [ ] `C-TR-03` `contract` A list response carries `next_cursor`, a `has_more` flag for the following page. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` A case study media file lives under `storage_key` in the store, never a database blob. `src: Data model`
- [ ] `C-DM-02` `data` Seeding is idempotent so a restart duplicates no row. `src: Data model`
- [ ] `C-DM-03` `data` At most one article is pinned across the collection. `src: Data model`

## C-BP Build plan

- [ ] `C-BP-01` `contract` `GET /api/health` returns `200` when the app is ready. `src: Build plan step 1`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The studio inbox of enquiries is readable only by an editor. `src: Deployment contract API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-CF-01` |
| `editor@example.com` | the first seeded editor | `C-CF-01` |
| `editor2@example.com` | the second seeded editor | `C-RL-01` |
| `visitor@example.com` | the seeded visitor | `C-RL-02` |
| `20` | the default page size | `C-TR-03` |
| `8` | the minimum password length | `C-CF-03` |
| `409` | the replay conflict on a different body | `C-TR-02` |
| `next_cursor` | the pagination cursor field | `C-TR-03` |
| `casestudies/{id}/{sha256}.{ext}` | the media object key scheme | `C-DM-01` |
| `/api/health` | the health route | `C-BP-01` |
| `200` | the health ready status | `C-BP-01` |
| `4000` | the enquiry message ceiling | `C-CF-15` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the seven industry names | `C-CF-05` |
| the three service groups | `C-CF-11` |
| the privacy page copy | `C-CF-16` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 3 | 3 |
| Core features | 19 | 19 |
| User flow | 2 | 2 |
| UI and UX notes | 5 | 5 |
| Technical requirements | 3 | 3 |
| Data model | 3 | 3 |
| Build plan | 1 | 1 |
| Deployment contract | 1 | 1 |
