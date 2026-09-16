# Checklist: voice-synthesis-workbench

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, buildplan, deployment
Sections absent: constraints
Items: 40
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` A signed in author turns a script into a narrated take saved in their asset library. `src: Overview para 1`
- [ ] `C-OV-02` `capability` A take that has not been published is readable only by its owner. `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` An author generates a take, publishes a take to the gallery, manages their own metered keys. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A reader plays published gallery takes but is refused generation. `src: User roles table row 2`
- [ ] `C-RL-03` `contract` A direct call from a reader session to an author only endpoint is refused server side. `src: User roles para 1`

## C-CF Core features

- [ ] `C-CF-01` `capability` Login with a seeded account returns a bearer token. `src: Core features Accounts and sessions`
- [ ] `C-CF-02` `capability` Signup with an already registered email is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-03` `capability` The voice catalogue narrows when filtered by a use case. `src: Core features Voice catalogue`
- [ ] `C-CF-04` `capability` The voice catalogue narrows when filtered by a language. `src: Core features Voice catalogue`
- [ ] `C-CF-05` `capability` A generate request stores one audio object in the bucket. `src: Core features Generate a take`
- [ ] `C-CF-06` `literal` A generate request charges `100` credits. `src: Core features Generate a take`
- [ ] `C-CF-07` `capability` A generate request with an empty script is refused. `src: Core features Generate a take`
- [ ] `C-CF-08` `capability` A generate request from a reader is refused. `src: Core features Generate a take`
- [ ] `C-CF-09` `capability` The asset library returns the caller's own takes newest first. `src: Core features Asset library`
- [ ] `C-CF-10` `capability` A published take appears in the public gallery. `src: Core features Visibility and the public gallery`
- [ ] `C-CF-11` `contract` A private take audio object is refused to a non owner. `src: Core features Visibility and the public gallery`
- [ ] `C-CF-12` `capability` Returning a take to private removes the take from the gallery. `src: Core features Visibility and the public gallery`
- [ ] `C-CF-13` `capability` A new API key secret is shown once at creation. `src: Core features Metered API keys`
- [ ] `C-CF-14` `contract` The key list shows the prefix, never the secret. `src: Core features Metered API keys`
- [ ] `C-CF-15` `capability` The `/privacy` page renders readable content. `src: Core features Static pages and error handling`
- [ ] `C-CF-16` `capability` The `/terms` page renders readable content. `src: Core features Static pages and error handling`
- [ ] `C-CF-17` `capability` An unknown route renders a custom not found page. `src: Core features Static pages and error handling`
- [ ] `C-CF-18` `capability` Signup with a password shorter than `8` characters is refused. `src: Core features Static pages and error handling`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated caller to a protected route is refused. `src: User flow Entry and redirects`
- [ ] `C-UF-02` `ui` The generate journey shows the take ready with the balance reduced afterwards. `src: User flow Journeys`
- [ ] `C-UF-03` `ui` Each list has a loading state, an empty state with a prompt. `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every status carries a text label so meaning never rides on colour alone. `src: UI/UX notes Palette`
- [ ] `C-UX-02` `ui` Motion glides to a stop with no bounce. `src: UI/UX notes Motion`
- [ ] `C-UX-03` `ui` The layout reflows to a single column at the small breakpoint with no sideways scroll. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-04` `ui` Body text meets a readable contrast, every control shows a focus ring. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-05` `ui` The clip player reads as the take's own audio. `src: UI/UX notes Palette`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Storage credentials never reach the served frontend bundle. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Two simultaneous generate requests with one key create exactly one take. `src: Technical requirements`
- [ ] `C-TR-03` `contract` A generate request the balance cannot cover is refused with `402`. `src: Technical requirements`
- [ ] `C-TR-04` `contract` A list response carries `next_cursor`, a `has_more` flag for the following page. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` The spendable balance is computed on read, never driven below zero. `src: Data model`
- [ ] `C-DM-02` `data` Seeding is idempotent so a restart duplicates no row. `src: Data model`
- [ ] `C-DM-03` `data` A take audio lives under `storage_key` in the store, never as a database blob. `src: Data model`

## C-BP Build plan

- [ ] `C-BP-01` `contract` `GET /api/health` returns `200` when the app is ready. `src: Build plan step 1`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` A key generation records a usage event carrying the request `request_id`. `src: Deployment contract API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-CF-01` |
| `author@example.com` | the first seeded author | `C-CF-09` |
| `author2@example.com` | the second seeded author | `C-CF-11` |
| `reader@example.com` | the seeded reader | `C-RL-02` |
| `100` | the credits a generation charges | `C-CF-06` |
| `300` | the first author seeded balance | `C-DM-01` |
| `50` | the second author seeded balance | `C-TR-03` |
| `20` | the default page size | `C-TR-04` |
| `8` | the minimum password length | `C-CF-18` |
| `402` | the refusal when the balance is short | `C-TR-03` |
| `next_cursor` | the pagination cursor field | `C-TR-04` |
| `takes/{take_id}/{sha256}.mp3` | the object key scheme | `C-DM-03` |
| `/api/health` | the health route | `C-BP-01` |
| `200` | the health ready status | `C-BP-01` |
| `request_id` | the usage correlation field | `C-DC-01` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the eight seeded voice names | `C-CF-03` |
| the generated take audio duration | `C-OV-01` |
| the privacy page copy | `C-CF-15` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 3 | 3 |
| Core features | 18 | 18 |
| User flow | 3 | 3 |
| UI and UX notes | 5 | 5 |
| Technical requirements | 4 | 4 |
| Data model | 3 | 3 |
| Build plan | 1 | 1 |
| Deployment contract | 1 | 1 |
