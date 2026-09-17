# Checklist: audience-gated-publishing

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, buildplan, deployment
Sections absent: constraints
Items: 42
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The publisher sets a post's paywall by moving the gate across the real audience. `src: Overview para 1`
- [ ] `C-OV-02` `capability` A gated post's audio edition stays readable only by a subscriber whose paid tier reaches the gate. `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` An author writes, gates, publishes posts, reads the audience, reads the ledger. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A reader reads free posts, reads gated posts with an active paid tier, never authors. `src: User roles table row 2`
- [ ] `C-RL-03` `contract` A direct call from a reader session to an author only endpoint is refused server side. `src: User roles para 1`

## C-CF Core features

- [ ] `C-CF-01` `capability` Login with a seeded account returns a bearer token. `src: Core features Accounts and sessions`
- [ ] `C-CF-02` `capability` Signup with an already registered email is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-03` `capability` An author creates a post as a draft. `src: Core features Posts and the composer`
- [ ] `C-CF-04` `capability` Publishing a post stores one audio edition object in the bucket. `src: Core features Posts and the composer`
- [ ] `C-CF-05` `capability` The projected reach for a gate is the count of subscribers at or above the gated tier. `src: Core features The audience field and the gate`
- [ ] `C-CF-06` `capability` Below the minimum cohort the projection refuses a revenue figure. `src: Core features The audience field and the gate`
- [ ] `C-CF-07` `capability` Committing the gate writes the post's paywall. `src: Core features The audience field and the gate`
- [ ] `C-CF-08` `capability` A gate naming an unknown tier is refused. `src: Core features The audience field and the gate`
- [ ] `C-CF-09` `contract` A gated audio edition is refused to a free reader. `src: Core features The gated audio edition`
- [ ] `C-CF-10` `capability` A gated audio edition streams to an entitled subscriber. `src: Core features The gated audio edition`
- [ ] `C-CF-11` `literal` A premium subscription is priced at `800` minor units. `src: Core features Tiers, offers and subscribing`
- [ ] `C-CF-12` `literal` The offer `WELCOME25` takes `25` percent off, resolving to `600`. `src: Core features Tiers, offers and subscribing`
- [ ] `C-CF-13` `capability` A duplicate subscribe for the same active tier creates no second active subscription. `src: Core features Tiers, offers and subscribing`
- [ ] `C-CF-14` `capability` A subscription charge is booked into the double-entry ledger as one balanced transaction. `src: Core features The double-entry ledger`
- [ ] `C-CF-15` `capability` The `/privacy` page renders readable content. `src: Core features Static pages, links and error handling`
- [ ] `C-CF-16` `capability` Every internal link on every public route resolves. `src: Core features Static pages, links and error handling`
- [ ] `C-CF-17` `capability` Signup with a password shorter than `8` characters is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-18` `capability` Releasing a post creates one delivery per resolved recipient with no duplicates. `src: Core features The audience and newsletter release`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated caller to a protected route is refused. `src: User flow Entry and redirects`
- [ ] `C-UF-02` `ui` The gate journey shows the projected reach with the revenue before the commit. `src: User flow Journeys`
- [ ] `C-UF-03` `ui` Each list has a loading state, then an empty state carrying a prompt. `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every status carries a text label so meaning never rides on colour alone. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Motion eases to a stop with no bounce except the gate settle. `src: UI/UX notes Motion`
- [ ] `C-UX-03` `ui` On a narrow viewport the field becomes a cohort table with no sideways scroll. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-04` `ui` Body text holds a readable contrast, every control shows a focus ring. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-05` `contract` Every content image carries alternative text. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-06` `ui` The audience field renders on its own dark plane distinct from the console. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Server credentials never reach the served frontend bundle. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Two simultaneous subscribes with one key create exactly one subscription. `src: Technical requirements`
- [ ] `C-TR-03` `contract` A list response carries `next_cursor` beside a `has_more` flag for the following page. `src: Technical requirements`
- [ ] `C-TR-04` `contract` A `sitemap` lists every public route, a robots file references the sitemap. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Every public route declares a social preview title with a resolving preview image. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` For every ledger transaction the debits equal the credits. `src: Data model`
- [ ] `C-DM-02` `data` Seeding is idempotent so a restart duplicates no row. `src: Data model`
- [ ] `C-DM-03` `data` A post audio edition lives under `audio_key` in the store, never as a database blob. `src: Data model`

## C-BP Build plan

- [ ] `C-BP-01` `contract` `GET /api/health` returns `200` when the app is ready. `src: Build plan step 1`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` List endpoints return their rows under an `items` array. `src: Deployment contract API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-CF-01` |
| `author@example.com` | the seeded publisher | `C-RL-01` |
| `reader@example.com` | the seeded premium subscriber | `C-CF-10` |
| `reader2@example.com` | the seeded free reader | `C-CF-09` |
| `800` | the premium price in minor units | `C-CF-11` |
| `WELCOME25` | the seeded discount code | `C-CF-12` |
| `25` | the discount percentage | `C-CF-12` |
| `600` | the discounted premium price | `C-CF-12` |
| `3` | the minimum projection cohort | `C-CF-06` |
| `20` | the default page size | `C-TR-03` |
| `100` | the maximum page size | `C-TR-03` |
| `8` | the minimum password length | `C-CF-17` |
| `409` | the conflict status for a mismatched key | `C-TR-02` |
| `editions/{post_id}/{sha256}.mp3` | the audio object key scheme | `C-DM-03` |
| `next_cursor` | the pagination cursor field | `C-TR-03` |
| `/api/health` | the health route | `C-BP-01` |
| `200` | the health ready status | `C-BP-01` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the projected recurring revenue figure | `C-OV-01` |
| the privacy page copy | `C-CF-15` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 3 | 3 |
| Core features | 18 | 18 |
| User flow | 3 | 3 |
| UI and UX notes | 6 | 6 |
| Technical requirements | 5 | 5 |
| Data model | 3 | 3 |
| Build plan | 1 | 1 |
| Deployment contract | 1 | 1 |
