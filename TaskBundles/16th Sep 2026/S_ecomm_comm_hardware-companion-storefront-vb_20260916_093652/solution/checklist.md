# Checklist: hardware-companion-storefront

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, buildplan, deployment
Sections absent: constraints
Items: 38
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` A visitor reads the founder letter, then buys a camera through a server side cart. `src: Overview para 1`
- [ ] `C-OV-02` `capability` Placing an order raises one invoice on the buyer account for the exact total. `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` A customer checks out, then manages their own orders, devices, firmware. `src: User roles table row 1`
- [ ] `C-RL-02` `contract` A direct call for another account's order or device is refused server side. `src: User roles para 1`
- [ ] `C-RL-03` `contract` An anonymous caller to an account scoped endpoint is refused. `src: User roles para 1`

## C-CF Core features

- [ ] `C-CF-01` `capability` Login with a seeded account returns a bearer token. `src: Core features Accounts and sessions`
- [ ] `C-CF-02` `capability` Signup with an already registered email is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-03` `capability` Signup with a password shorter than `8` characters is refused. `src: Core features Accounts and sessions`
- [ ] `C-CF-04` `capability` The catalogue lists cameras with accessories, each carrying a price. `src: Core features The storefront and the founder letter`
- [ ] `C-CF-05` `capability` Adding a variant to the cart returns the line with its quantity. `src: Core features The cart`
- [ ] `C-CF-06` `capability` A cart line stores the unit price captured at add time. `src: Core features The cart`
- [ ] `C-CF-07` `capability` Checkout re-prices every line before the order is placed. `src: Core features Checkout and the order`
- [ ] `C-CF-08` `capability` Placing an order raises exactly one invoice on the buyer account for the total in `usd`. `src: Core features Checkout and the order`
- [ ] `C-CF-09` `capability` Placing an order sends a confirmation email carrying the order reference. `src: Core features Checkout and the order`
- [ ] `C-CF-10` `capability` A placed order records a status of `paid`. `src: Core features Checkout and the order`
- [ ] `C-CF-11` `capability` A customer registers a camera by serial; a duplicate serial is refused. `src: Core features The account`
- [ ] `C-CF-12` `capability` A customer flashes a registered device to a newer firmware version. `src: Core features The account`
- [ ] `C-CF-13` `contract` A device belonging to another account cannot be flashed. `src: Core features The account`
- [ ] `C-CF-14` `capability` A first time visitor is asked once about cookies; the choice survives a reload. `src: Core features Consent, telemetry and abuse control`
- [ ] `C-CF-15` `capability` Each page view is recorded with its route, readable by an owner. `src: Core features Consent, telemetry and abuse control`
- [ ] `C-CF-16` `capability` A contact form submitted repeatedly by a bot is refused. `src: Core features Consent, telemetry and abuse control`

## C-UF User flow

- [ ] `C-UF-01` `contract` An unauthenticated visit to an account route redirects to login. `src: User flow Entry and redirects`
- [ ] `C-UF-02` `ui` The buy journey shows the order paid with an invoice raised afterwards. `src: User flow Journeys`
- [ ] `C-UF-03` `ui` Each list has a loading state, then an empty cart state with a link. `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Every status carries a text label so meaning never rides on colour alone. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Motion eases to a stop with no bounce; the video stage stays muted. `src: UI/UX notes Motion`
- [ ] `C-UX-03` `ui` At a narrow viewport nothing overflows sideways. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-04` `ui` Body text holds a readable contrast; every control shows a focus ring. `src: UI/UX notes Accessibility and responsiveness`
- [ ] `C-UX-05` `ui` Each page leads with one primary action set apart from secondary controls. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Server credentials never reach the served frontend bundle. `src: Technical requirements`
- [ ] `C-TR-02` `contract` Two checkouts with one key place exactly one order, raise one invoice. `src: Technical requirements`
- [ ] `C-TR-03` `contract` A list response carries `next_cursor` beside a `has_more` flag. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` An order total equals the sum of its re-priced lines. `src: Data model`
- [ ] `C-DM-02` `data` Seeding is idempotent so a restart duplicates no row. `src: Data model`
- [ ] `C-DM-03` `data` A placed order is persisted in the `orders` table. `src: Data model`
- [ ] `C-DM-04` `data` A checkout replay with the same key raises no second invoice. `src: Data model`

## C-BP Build plan

- [ ] `C-BP-01` `contract` `GET /api/health` returns `200` when the app is ready. `src: Build plan step 1`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` List endpoints return their rows under an `items` array. `src: Deployment contract API shapes`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the seeded account password | `C-CF-01` |
| `customer@example.com` | the seeded customer | `C-RL-01` |
| `customer2@example.com` | the second seeded customer | `C-CF-02` |
| `Opal One` | the seeded camera | `C-CF-04` |
| `79900` | the camera price in minor units | `C-CF-08` |
| `usd` | the order currency | `C-CF-08` |
| `paid` | the placed order status | `C-CF-10` |
| `1.0.0` | the seeded device firmware version | `C-CF-12` |
| `1.1.0` | the newer firmware release | `C-CF-12` |
| `8` | the minimum password length | `C-CF-03` |
| `409` | the conflict status for a mismatched key | `C-TR-02` |
| `20` | the default page size | `C-TR-03` |
| `100` | the maximum page size | `C-TR-03` |
| `next_cursor` | the pagination cursor field | `C-TR-03` |
| `/api/health` | the health route | `C-BP-01` |
| `200` | the health ready status | `C-BP-01` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the founder letter copy | `C-OV-01` |
| the companion application version | `C-CF-12` |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 3 | 3 |
| Core features | 16 | 16 |
| User flow | 3 | 3 |
| UI and UX notes | 5 | 5 |
| Technical requirements | 3 | 3 |
| Data model | 4 | 4 |
| Build plan | 1 | 1 |
| Deployment contract | 1 | 1 |
