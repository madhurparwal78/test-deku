# Checklist: deku/creator-commerce-console-vb
Items: 285
Unpinned values flagged: 4
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents a creator console covering the catalog, the orders, the money, the discount codes, the pricing decomposition `src: Overview`
- [ ] `C-OV-02` `capability` The app presents buyer surfaces comprising a storefront, a product page, a checkout, a durable library `src: Overview`
- [ ] `C-OV-03` `role` One account holds exactly one creator, with readers scoped to their own purchases `src: Overview`
- [ ] `C-OV-04` `constraint` A reader sees no creator-side figure `src: Overview`
- [ ] `C-OV-05` `contract` Every order carries a resolved tax jurisdiction with the rate that was applied `src: Overview`
- [ ] `C-OV-06` `contract` The checkout surface names the selling entity alongside the creator brand `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A creator can raise, edit, publish, unpublish products with their tiers `src: User roles`
- [ ] `C-RL-02` `role` A creator can raise discount codes `src: User roles`
- [ ] `C-RL-03` `role` A creator can read every order with the full money decomposition `src: User roles`
- [ ] `C-RL-04` `role` A creator can read the chart of accounts, the entry stream, the trial balance `src: User roles`
- [ ] `C-RL-05` `role` A creator cannot buy anything `src: User roles`
- [ ] `C-RL-06` `role` A creator holds no entitlement `src: User roles`
- [ ] `C-RL-07` `role` A reader can browse published products, open a checkout, confirm a purchase `src: User roles`
- [ ] `C-RL-08` `role` A reader can read their own library `src: User roles`
- [ ] `C-RL-09` `role` A reader cannot reach any console route `src: User roles`
- [ ] `C-RL-10` `role` A reader cannot see another reader entitlement `src: User roles`
- [ ] `C-RL-11` `constraint` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-12` `constraint` A direct API call from a reader session to a creator-only endpoint is denied, leaving the protected state unchanged `src: User roles`
- [ ] `C-RL-13` `role` Signup is open, producing a reader every time `src: User roles`
- [ ] `C-RL-14` `role` The creator account cannot be produced by signing up `src: User roles`
- [ ] `C-RL-15` `constraint` A request for an order the caller does not hold is answered as absent rather than as forbidden `src: User roles`
- [ ] `C-RL-16` `literal` The seeded principals are `creator@example.com`, `buyer@example.com`, `buyer2@example.com` `src: User roles`
- [ ] `C-RL-17` `literal` Every seeded principal signs in with `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-18` `literal` The seeded display names are `Marlowe Quill`, `Ines Calder`, `Tobias Renn` `src: User roles`
- [ ] `C-RL-19` `literal` The seeded reader countries are `IE` for the first reader, `US` for the second `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `literal` A successful login returns a bearer token under the key `access_token` `src: Core features ### Auth`
- [ ] `C-CF-02` `contract` An authenticated request carries the bearer token in the Authorization header `src: Core features ### Auth`
- [ ] `C-CF-03` `capability` Signup takes an email, a display name, a country, a password, producing a reader `src: Core features ### Auth`
- [ ] `C-CF-04` `contract` An email already in use is refused, producing no second account `src: Core features ### Auth`
- [ ] `C-CF-05` `capability` A principal read returns the signed-in principal with the role held `src: Core features ### Auth`
- [ ] `C-CF-06` `contract` A request with no token to an authenticated route is denied, leaving the protected state unchanged `src: Core features ### Auth`
- [ ] `C-CF-07` `literal` The signup form carries an unattended decoy field named `company_website` `src: Core features ### Auth`
- [ ] `C-CF-08` `contract` A submission arriving with the decoy field filled is refused, writing nothing `src: Core features ### Auth`
- [ ] `C-CF-09` `contract` The same signup submitted repeatedly in quick succession is refused `src: Core features ### Auth`
- [ ] `C-CF-10` `capability` The public storefront list returns every published product with its permalink, its name, its tiers `src: Core features ### The catalog and the product page`
- [ ] `C-CF-11` `capability` The public product read returns one product with every tier code, tier name, tier price `src: Core features ### The catalog and the product page`
- [ ] `C-CF-12` `constraint` A draft product is not readable by a stranger at either public endpoint `src: Core features ### The catalog and the product page`
- [ ] `C-CF-13` `ui` An unpublished product renders a designed unavailable state offering the storefront rather than an error `src: Core features ### The catalog and the product page`
- [ ] `C-CF-14` `constraint` A permalink may be changed freely until the product takes a first paid order `src: Core features ### The catalog and the product page`
- [ ] `C-CF-15` `constraint` A permalink change after the first paid order is refused `src: Core features ### The catalog and the product page`
- [ ] `C-CF-16` `constraint` Every creator catalog endpoint is denied to a reader `src: Core features ### The catalog and the product page`
- [ ] `C-CF-17` `contract` Every storefront page carries its own title with its own description in the served HTML `src: Core features ### The catalog and the product page`
- [ ] `C-CF-18` `contract` A product price is present in the served HTML before any script runs `src: Core features ### The catalog and the product page`
- [ ] `C-CF-19` `capability` Opening a checkout session takes a permalink, a tier code, a quantity, an attribution channel, an idempotency key `src: Core features ### Checkout`
- [ ] `C-CF-20` `contract` A checkout session locks the unit price, the resolved tax jurisdiction, the tax rate at the moment the session opens `src: Core features ### Checkout`
- [ ] `C-CF-21` `literal` The attribution channel is `direct` or `marketplace`, never another value `src: Core features ### Checkout`
- [ ] `C-CF-22` `contract` The tax jurisdiction resolved for a session is the buying reader country `src: Core features ### Checkout`
- [ ] `C-CF-23` `literal` The seeded tax rate for `IE` is `1900` bps `src: Core features ### Checkout`
- [ ] `C-CF-24` `literal` The seeded tax rate for `US` is zero bps `src: Core features ### Checkout`
- [ ] `C-CF-25` `contract` Repricing a tier during an open session leaves the session locked figures untouched at confirm `src: Core features ### Checkout`
- [ ] `C-CF-26` `contract` A discount code is matched without regard to case `src: Core features ### Checkout`
- [ ] `C-CF-27` `contract` A discount is computed on the subtotal, with the tax then re-resolved on the discounted base `src: Core features ### Checkout`
- [ ] `C-CF-28` `contract` A code whose window has closed is refused with the reason named, leaving the session total unchanged `src: Core features ### Checkout`
- [ ] `C-CF-29` `contract` A code whose total usage cap is exhausted is refused `src: Core features ### Checkout`
- [ ] `C-CF-30` `contract` A code already used by a reader up to the per-reader cap is refused for that reader `src: Core features ### Checkout`
- [ ] `C-CF-31` `contract` A code belonging to no account is refused `src: Core features ### Checkout`
- [ ] `C-CF-32` `contract` Confirming a session twice with one idempotency key produces exactly one order `src: Core features ### Checkout`
- [ ] `C-CF-33` `contract` Confirming a session twice with one idempotency key produces exactly one invoice `src: Core features ### Checkout`
- [ ] `C-CF-34` `contract` Confirming a session twice with one idempotency key produces exactly one entitlement `src: Core features ### Checkout`
- [ ] `C-CF-35` `contract` Confirming a session twice with one idempotency key produces exactly one ledger entry `src: Core features ### Checkout`
- [ ] `C-CF-36` `contract` Confirming a session twice with one idempotency key sends exactly one receipt `src: Core features ### Checkout`
- [ ] `C-CF-37` `contract` A confirm that cannot complete leaves behind no order, no invoice, no entitlement, no ledger entry, no mail `src: Core features ### Checkout`
- [ ] `C-CF-38` `ui` The checkout surface shows the unit price, the discount, the tax, the total as separate lines `src: Core features ### Checkout`
- [ ] `C-CF-39` `contract` The checkout session endpoint refuses a submission that fills the decoy field `src: Core features ### Checkout`
- [ ] `C-CF-40` `data` Every order decomposes into a subtotal, a discount, a tax, a total, a platform fee, a payment fee, an affiliate share, a net `src: Core features ### The money decomposition`
- [ ] `C-CF-41` `contract` An order net equals the subtotal less the discount, less the platform fee, less the payment fee, less the affiliate share `src: Core features ### The money decomposition`
- [ ] `C-CF-42` `literal` The affiliate share on every order is `0` `src: Core features ### The money decomposition`
- [ ] `C-CF-43` `contract` An order total equals the subtotal less the discount, plus the tax `src: Core features ### The money decomposition`
- [ ] `C-CF-44` `literal` The platform fee on the `direct` channel is `1000` bps of the discounted subtotal plus a fixed `30` minor units `src: Core features ### The money decomposition`
- [ ] `C-CF-45` `literal` The platform fee on the `marketplace` channel is `2000` bps of the discounted subtotal with no fixed component `src: Core features ### The money decomposition`
- [ ] `C-CF-46` `literal` The payment fee is `290` bps of the total plus a fixed `30` minor units `src: Core features ### The money decomposition`
- [ ] `C-CF-47` `ui` The payment fee is itemised separately from the platform fee on every order `src: Core features ### The money decomposition`
- [ ] `C-CF-48` `contract` Every arithmetic step rounds half up to the nearest minor unit `src: Core features ### The money decomposition`
- [ ] `C-CF-49` `literal` In the worked case the subtotal is `2400`, the discount is `480`, the tax is `365`, the total is `2285` `src: Core features ### The money decomposition`
- [ ] `C-CF-50` `literal` In the worked case the platform fee is `222`, the payment fee is `96`, the net is `1602` `src: Core features ### The money decomposition`
- [ ] `C-CF-51` `literal` In the zero-rated worked case the total is `2400`, the platform fee is `480`, the payment fee is `100`, the net is `1820` `src: Core features ### The money decomposition`
- [ ] `C-CF-52` `data` Every financial fact is an immutable entry carrying two or more balanced legs `src: Core features ### The ledger`
- [ ] `C-CF-53` `constraint` Balances, earnings, the trial balance are derived from postings, never stored as counters `src: Core features ### The ledger`
- [ ] `C-CF-54` `literal` The seeded chart of accounts holds `1100` Provider receivable as an asset `src: Core features ### The ledger`
- [ ] `C-CF-55` `literal` The seeded chart of accounts holds `2000` Creator payable as a liability `src: Core features ### The ledger`
- [ ] `C-CF-56` `literal` The seeded chart of accounts holds `2100` Tax payable as a liability, once per jurisdiction `src: Core features ### The ledger`
- [ ] `C-CF-57` `literal` The seeded chart of accounts holds `4000` Platform fee revenue as a revenue account `src: Core features ### The ledger`
- [ ] `C-CF-58` `literal` The seeded chart of accounts holds `5000` Payment processing expense as an expense account `src: Core features ### The ledger`
- [ ] `C-CF-59` `contract` A paid order posts one entry debiting Provider receivable by the order total `src: Core features ### The ledger`
- [ ] `C-CF-60` `contract` A paid order entry credits Tax payable for the order jurisdiction by the tax `src: Core features ### The ledger`
- [ ] `C-CF-61` `contract` A paid order entry credits Platform fee revenue by the platform fee `src: Core features ### The ledger`
- [ ] `C-CF-62` `contract` A paid order entry credits Payment processing expense by the payment fee `src: Core features ### The ledger`
- [ ] `C-CF-63` `contract` A paid order entry credits Creator payable by the net `src: Core features ### The ledger`
- [ ] `C-CF-64` `constraint` A leg worth nothing is not written at all `src: Core features ### The ledger`
- [ ] `C-CF-65` `contract` Within one entry the debit legs sum to the same amount as the credit legs, per currency `src: Core features ### The ledger`
- [ ] `C-CF-66` `constraint` An entry that would not balance is refused whole, never written in part `src: Core features ### The ledger`
- [ ] `C-CF-67` `contract` The trial balance reads exactly zero per currency after every order `src: Core features ### The ledger`
- [ ] `C-CF-68` `constraint` No account of type liability ever holds a negative balance `src: Core features ### The ledger`
- [ ] `C-CF-69` `constraint` A posted entry is never changed, never removed `src: Core features ### The ledger`
- [ ] `C-CF-70` `constraint` Every ledger read endpoint is denied to a reader `src: Core features ### The ledger`
- [ ] `C-CF-71` `contract` Every billing platform call carries the basic credentials read from the environment `src: Core features ### The billing record`
- [ ] `C-CF-72` `contract` Every billing platform call carries the api key header alongside the api secret header `src: Core features ### The billing record`
- [ ] `C-CF-73` `contract` A billing platform write carries a created-by header `src: Core features ### The billing record`
- [ ] `C-CF-74` `contract` Exactly one billing account exists per reader `src: Core features ### The billing record`
- [ ] `C-CF-75` `literal` The billing external key for the first reader is `handsel-ines-calder` `src: Core features ### The billing record`
- [ ] `C-CF-76` `literal` The billing external key for the second reader is `handsel-tobias-renn` `src: Core features ### The billing record`
- [ ] `C-CF-77` `contract` A second attempt at one external key is refused by the store rather than by application code `src: Core features ### The billing record`
- [ ] `C-CF-78` `contract` Exactly one invoice exists per paid order on the buying reader billing account `src: Core features ### The billing record`
- [ ] `C-CF-79` `contract` The invoice carries the order total with the order currency `src: Core features ### The billing record`
- [ ] `C-CF-80` `literal` The worked case invoice reads `22.85` as a decimal amount `src: Core features ### The billing record`
- [ ] `C-CF-81` `constraint` An order counts as complete only once the invoice exists `src: Core features ### The billing record`
- [ ] `C-CF-82` `contract` A paid order grants one entitlement for the product bought at the tier bought `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-83` `contract` The library read returns every entitlement the signed-in reader holds, never another reader entitlement `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-84` `constraint` The entitlement is the source of truth for access, with the receipt a convenience `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-85` `capability` Opening an entitlement records the access, returning the deliverable `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-86` `constraint` Unpublishing a product does not revoke an entitlement already granted `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-87` `contract` The receipt is addressed to the buying reader email address, with no cc, no bcc `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-88` `literal` The receipt subject begins with `Handsel receipt: ` followed by the product name `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-89` `contract` The receipt body is not empty, naming the product, the tier, the total paid `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-90` `constraint` A refused discount sends no mail at all `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-91` `constraint` A refused confirm sends no mail at all `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-92` `constraint` Publishing a product sends no mail at all `src: Core features ### Entitlement, library and the receipt`
- [ ] `C-CF-93` `literal` The limited product `lantern-press-kit` carries exactly one unit `src: Core features ### The contention rule`
- [ ] `C-CF-94` `constraint` A product carrying a quantity limit never sells more units than the limit allows `src: Core features ### The contention rule`
- [ ] `C-CF-95` `contract` Two readers confirming the last unit at one moment produce exactly one order `src: Core features ### The contention rule`
- [ ] `C-CF-96` `ui` The losing reader is told the product is sold out, with the storefront offered `src: Core features ### The contention rule`
- [ ] `C-CF-97` `constraint` Nothing is written anywhere for the losing reader `src: Core features ### The contention rule`
- [ ] `C-CF-98` `capability` The pricing read takes a tier code, a discount depth, an attribution channel, a tax jurisdiction `src: Core features ### The pricing decomposition`
- [ ] `C-CF-99` `contract` The pricing read returns the same eight figures an order carries `src: Core features ### The pricing decomposition`
- [ ] `C-CF-100` `contract` The pricing figures for a set of parameters equal the figures an order would carry, to the minor unit `src: Core features ### The pricing decomposition`
- [ ] `C-CF-101` `literal` The pricing read at depth `2000` on the `direct` channel for jurisdiction `IE` returns a net of `1602` `src: Core features ### The pricing decomposition`
- [ ] `C-CF-102` `literal` The same read on the `marketplace` channel returns a platform fee of `384` with a net of `1440` `src: Core features ### The pricing decomposition`
- [ ] `C-CF-103` `ui` When a parameter change moves the net, the surface names the component that moved `src: Core features ### The pricing decomposition`
- [ ] `C-CF-104` `ui` The surface never presents the moved total alone `src: Core features ### The pricing decomposition`
- [ ] `C-CF-105` `contract` A reader-facing order response carries the subtotal, the discount, the tax, the total `src: Core features ### Audience isolation`
- [ ] `C-CF-106` `constraint` A reader-facing order response carries no platform fee, no payment fee, no affiliate share, no net `src: Core features ### Audience isolation`
- [ ] `C-CF-107` `constraint` A reader asking for an order belonging to another reader is answered as absent `src: Core features ### Audience isolation`
- [ ] `C-CF-108` `constraint` A reader asking for an entitlement belonging to another reader is answered as absent `src: Core features ### Audience isolation`
- [ ] `C-CF-109` `constraint` A reader reaching the creator order list is denied, leaving the protected state unchanged `src: Core features ### Audience isolation`
- [ ] `C-CF-110` `constraint` A reader reaching the pricing read is denied `src: Core features ### Audience isolation`
- [ ] `C-CF-111` `capability` The creator discount surface lists codes, raising new ones `src: Core features ### Discount codes`
- [ ] `C-CF-112` `constraint` Every discount endpoint is denied to a reader `src: Core features ### Discount codes`
- [ ] `C-CF-113` `literal` The seeded code `LAUNCH20` sits at `2000` bps with a total cap of `5` uses `src: Core features ### Discount codes`
- [ ] `C-CF-114` `literal` The seeded code `LAUNCH20` carries a per-reader cap of `1` `src: Core features ### Discount codes`
- [ ] `C-CF-115` `literal` The seeded code `EXPIRED10` sits at `1000` bps with a window already closed `src: Core features ### Discount codes`
- [ ] `C-CF-116` `contract` A code whose window has closed is refused when raised `src: Core features ### Discount codes`
- [ ] `C-CF-117` `contract` A depth that would take a total below zero is refused `src: Core features ### Discount codes`
- [ ] `C-CF-118` `ui` A terms page is reachable from the footer of every page `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-119` `ui` The terms page is linked from the signup form `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-120` `literal` The terms page names the seller of record as `Handsel Commerce Ltd` `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-121` `constraint` The seller-of-record disclosure cannot be suppressed by branding `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-122` `ui` The same disclosure appears at checkout, also on the receipt `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-123` `ui` Every form rejects invalid input inline, naming the field that was wrong `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-124` `constraint` A form rejecting invalid input writes nothing `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-125` `ui` An unknown address renders the product own not-found page, with a way back `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-126` `contract` An unknown address answers not-found `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-127` `ui` Every list has an empty state naming the next concrete action `src: Core features ### The terms page and the surfaces every page owes`
- [ ] `C-CF-128` `literal` The seeded catalog holds `field-notes-vol-one` named `Field Notes Volume One`, published `src: Data model`
- [ ] `C-CF-129` `literal` The seeded catalog holds `lantern-press-kit` named `Lantern Press Kit`, published `src: Data model`
- [ ] `C-CF-130` `literal` The seeded catalog holds `tide-tables-draft` named `Tide Tables Draft`, still a draft `src: Data model`
- [ ] `C-CF-131` `literal` The tier `standard` on `field-notes-vol-one` is named `Standard`, priced `2400` `src: Data model`
- [ ] `C-CF-132` `literal` The tier `studio` on `field-notes-vol-one` is named `Studio`, priced `5600` `src: Data model`
- [ ] `C-CF-133` `literal` The tier `standard` on `lantern-press-kit` is priced `1000` `src: Data model`
- [ ] `C-CF-134` `literal` The first order number is `HS-00001` `src: Data model`

## C-UF User flow

- [ ] `C-UF-01` `ui` The storefront home lists every published product `src: User flow`
- [ ] `C-UF-02` `ui` A product page renders at its permalink route `src: User flow`
- [ ] `C-UF-03` `ui` A checkout route renders one open session `src: User flow`
- [ ] `C-UF-04` `ui` A thanks route renders the order with a way into the library `src: User flow`
- [ ] `C-UF-05` `ui` The library route renders every entitlement the reader holds `src: User flow`
- [ ] `C-UF-06` `ui` A console route renders only for a creator session `src: User flow`
- [ ] `C-UF-07` `contract` An unauthenticated request for a protected route goes to the sign-in route `src: User flow`
- [ ] `C-UF-08` `contract` After a successful sign-in the reader lands on the route that was asked for `src: User flow`
- [ ] `C-UF-09` `contract` A reader signing in with no destination lands on the library `src: User flow`
- [ ] `C-UF-10` `contract` The creator signing in with no destination lands on the console home `src: User flow`
- [ ] `C-UF-11` `contract` Signing out returns to the storefront home, ending the session `src: User flow`
- [ ] `C-UF-12` `contract` Going back after signing out does not restore the session `src: User flow`
- [ ] `C-UF-13` `contract` A creator session reaching the library is denied `src: User flow`
- [ ] `C-UF-14` `contract` A token expiring part way through an action leaves the action undone `src: User flow`
- [ ] `C-UF-15` `ui` Every list carries an empty state naming the next concrete action `src: User flow`
- [ ] `C-UF-16` `ui` Every page carries a loading placeholder occupying the space the content will occupy `src: User flow`
- [ ] `C-UF-17` `ui` An error is stated in place, never leaving the app unusable `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page ground is a near-white warm neutral `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Primary text is a near-black neutral, with muted text the same hue held lighter `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The primary action wears a mid, vivid orange, the only thing on a page wearing that colour `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Revenue carries a mid, vivid green, with anything declined carrying a mid, vivid red `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The money decomposition carries an ordered ramp, one distinguishable colour per component `src: UI/UX notes`
- [ ] `C-UX-06` `ui` Every money ramp segment carries a written label beside its colour `src: UI/UX notes`
- [ ] `C-UX-07` `constraint` Every semantic colour ships with a foreground holding WCAG AA contrast against the background `src: UI/UX notes`
- [ ] `C-UX-08` `ui` A variable grotesque carries interface text, with a monospace carrying money, order numbers, identifiers `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Every numeric context uses tabular figures `src: UI/UX notes`
- [ ] `C-UX-10` `literal` Body text is `16px` on a `24px` line, with interface text `14px` on `20px` `src: UI/UX notes`
- [ ] `C-UX-11` `constraint` The monospace family is never overridable `src: UI/UX notes`
- [ ] `C-UX-12` `ui` The console is compact, with the buyer surfaces spacious `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Motion carries an eased character on entrance, also on exit `src: UI/UX notes`
- [ ] `C-UX-14` `constraint` No overshoot is applied to a monetary figure, a total, any control on the buy path `src: UI/UX notes`
- [ ] `C-UX-15` `constraint` Nothing on the checkout surface delays input, moves a target after appearing, animates a total `src: UI/UX notes`
- [ ] `C-UX-16` `ui` A transition re-triggered part way through re-targets from where the transition is `src: UI/UX notes`
- [ ] `C-UX-17` `ui` A skeleton whose blocks occupy the space the content will occupy ends by settling into that content `src: UI/UX notes`
- [ ] `C-UX-18` `ui` A changed figure arrives by counting to its new value `src: UI/UX notes`
- [ ] `C-UX-19` `ui` A filtered list reorders by sliding its rows to their new positions `src: UI/UX notes`
- [ ] `C-UX-20` `ui` A confirmed purchase arrives as one settled state `src: UI/UX notes`
- [ ] `C-UX-21` `constraint` Reduced motion removes the movement rather than the information `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Every interactive component carries a resting, pointed-at, pressed, focused, unavailable, loading, errored state `src: UI/UX notes`
- [ ] `C-UX-23` `ui` A loading control keeps its width so nothing beside the control moves `src: UI/UX notes`
- [ ] `C-UX-24` `ui` A destructive control confirms first, naming what will be destroyed `src: UI/UX notes`
- [ ] `C-UX-25` `constraint` Unavailable is never signalled by colour alone `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Each page leads with one clear primary action, visually distinct from every secondary one `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Every money figure renders with its currency written out, at full precision `src: UI/UX notes`
- [ ] `C-UX-28` `constraint` Every surface meets WCAG 2.2 Level AA with effects active `src: UI/UX notes`
- [ ] `C-UX-29` `constraint` Every content image carries alternative text `src: UI/UX notes`
- [ ] `C-UX-30` `constraint` A decorative image declares itself decorative `src: UI/UX notes`
- [ ] `C-UX-31` `constraint` Every interactive element is reachable by keyboard navigation with a visible focus ring `src: UI/UX notes`
- [ ] `C-UX-32` `constraint` An icon-only control carries a label `src: UI/UX notes`
- [ ] `C-UX-33` `constraint` Meaning is never carried by colour alone `src: UI/UX notes`
- [ ] `C-UX-34` `constraint` At a narrow viewport nothing overflows sideways `src: UI/UX notes`
- [ ] `C-UX-35` `constraint` At a narrow viewport every navigation target stays reachable `src: UI/UX notes`
- [ ] `C-UX-36` `ui` The console rail collapses to icons at medium widths, becoming a bottom bar at narrow ones `src: UI/UX notes`
- [ ] `C-UX-37` `ui` The product page becomes a single column with the buy action pinned to the foot of the viewport `src: UI/UX notes`
- [ ] `C-UX-38` `ui` Checkout stays a single column at every width `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The console carries a persistent left rail holding seven destinations `src: Front-end specification`
- [ ] `C-FE-02` `ui` Every console working route is a split detail pane `src: Front-end specification`
- [ ] `C-FE-03` `ui` Selecting a record changes the right column with the address, never losing the left `src: Front-end specification`
- [ ] `C-FE-04` `ui` The buyer surfaces carry a branded header, the page, a footer linking the terms page `src: Front-end specification`
- [ ] `C-FE-05` `ui` Raising a new product opens a modal over the product list `src: Front-end specification`
- [ ] `C-FE-06` `ui` Raising a new discount code opens a modal over the code list `src: Front-end specification`
- [ ] `C-FE-07` `ui` Every confirmation appears as a banner at the top of the working pane `src: Front-end specification`
- [ ] `C-FE-08` `ui` A refusal banner names why, naming what to do next `src: Front-end specification`
- [ ] `C-FE-09` `ui` A banner persists until dismissed, or until the pane changes `src: Front-end specification`
- [ ] `C-FE-10` `ui` The price block states the currency explicitly beside every figure `src: Front-end specification`
- [ ] `C-FE-11` `constraint` The buy action is reachable by keyboard within a short run of tab stops at every width `src: Front-end specification`
- [ ] `C-FE-12` `ui` Checkout is a single column of at most four fields `src: Front-end specification`
- [ ] `C-FE-13` `ui` The ledger surface renders debit distinguishably from credit without colour `src: Front-end specification`
- [ ] `C-FE-14` `ui` Every ledger entry expands to show its legs with the account code, the account name `src: Front-end specification`
- [ ] `C-FE-15` `constraint` Iconography is drawn inline rather than loaded as a font `src: Front-end specification`
- [ ] `C-FE-16` `constraint` Creator branding never alters the money ramp, the focus ring contrast, any checkout control contrast `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server produces the HTML for every route `src: Technical requirements`
- [ ] `C-TR-02` `contract` A stranger landing on a product page receives the name, the tier prices, the buy action in the first response `src: Technical requirements`
- [ ] `C-TR-03` `literal` The datastore is PostgreSQL, reached at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-04` `literal` Billing is `killbill`, reached at `PAYMENTS_API_URL` `src: Technical requirements`
- [ ] `C-TR-05` `literal` Mail is Mailpit over real SMTP, reached at `SMTP_HOST` with `SMTP_PORT` `src: Technical requirements`
- [ ] `C-TR-06` `constraint` Every money value is an integer count of minor units carrying a currency code beside the value `src: Technical requirements`
- [ ] `C-TR-07` `constraint` No monetary value is held as a floating-point number anywhere `src: Technical requirements`
- [ ] `C-TR-08` `constraint` No credential appears in anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-09` `contract` A mutating request replayed with one idempotency key returns the stored outcome `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `constraint` Seeding is idempotent, so restarting creates no second copy of a seeded row `src: Data model`
- [ ] `C-DM-02` `literal` The account handle is `marlowe-quill` with payout currency `usd` `src: Data model`
- [ ] `C-DM-03` `data` A product carries a permalink unique per account, a name, a state, a quantity limit, a quantity sold `src: Data model`
- [ ] `C-DM-04` `literal` A product state is `draft`, `published`, or `unpublished` `src: Data model`
- [ ] `C-DM-05` `data` A tier carries a code unique per product, a name, a price in minor units, a currency `src: Data model`
- [ ] `C-DM-06` `data` A discount code carries a value in bps, a total cap, a per-reader cap, a validity window `src: Data model`
- [ ] `C-DM-07` `literal` The seeded fee schedule at version `1` holds `direct` at `1000` with a fixed `30` `src: Data model`
- [ ] `C-DM-08` `literal` The seeded fee schedule at version `1` holds `marketplace` at `2000` with no fixed component `src: Data model`
- [ ] `C-DM-09` `data` A checkout session carries the locked unit price, the jurisdiction, the rate, written when the session opens `src: Data model`
- [ ] `C-DM-10` `literal` A checkout session state is `open`, `confirmed`, `refused`, or `expired` `src: Data model`
- [ ] `C-DM-11` `data` An order carries a number unique per account, an idempotency key unique per account `src: Data model`
- [ ] `C-DM-12` `literal` An order number is `HS-` followed by five digits, counted per account `src: Data model`
- [ ] `C-DM-13` `data` A billing account carries a user reference, an external key unique across the table, a currency `src: Data model`
- [ ] `C-DM-14` `data` An invoice carries a unique order reference, an external key, an amount in minor units `src: Data model`
- [ ] `C-DM-15` `literal` An entitlement state is `active` or `revoked` `src: Data model`
- [ ] `C-DM-16` `data` An entitlement is unique on the order, the product, the tier together `src: Data model`
- [ ] `C-DM-17` `data` An access event carries an entitlement reference with the moment of access `src: Data model`
- [ ] `C-DM-18` `literal` A ledger account type is `asset`, `liability`, `revenue`, or `expense` `src: Data model`
- [ ] `C-DM-19` `data` A ledger account is unique on the account, the code, the currency, the jurisdiction together `src: Data model`
- [ ] `C-DM-20` `data` A ledger entry carries an idempotency key unique per account `src: Data model`
- [ ] `C-DM-21` `literal` A ledger posting direction is `debit` or `credit` `src: Data model`
- [ ] `C-DM-22` `constraint` Every posting amount is greater than zero `src: Data model`
- [ ] `C-DM-23` `constraint` Every balance is computed from postings, held in no counter anywhere `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` There is one creator account with one catalog, no second creator `src: Constraints`
- [ ] `C-CN-02` `constraint` There are no memberships, no recurring billing, no dunning `src: Constraints`
- [ ] `C-CN-03` `constraint` There are no refunds, no disputes, no chargebacks `src: Constraints`
- [ ] `C-CN-04` `constraint` There are no payouts, no tax filing, no held funds `src: Constraints`
- [ ] `C-CN-05` `constraint` There are no custom domains, no certificates `src: Constraints`
- [ ] `C-CN-06` `constraint` There is no storefront design tool, no live collaboration, no multiplayer presence `src: Constraints`
- [ ] `C-CN-07` `constraint` There is no marketplace browse, no search `src: Constraints`
- [ ] `C-CN-08` `constraint` There is no file upload, no media processing, no object storage `src: Constraints`
- [ ] `C-CN-09` `constraint` There is no review surface, so nothing in one can be edited by the seller `src: Constraints`
- [ ] `C-CN-10` `constraint` There is one currency, with no presentment currency, no exchange rate `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at the public URL read from the environment `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is read from the environment, never hardcoded `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the api prefix `src: Deployment contract`
- [ ] `C-DC-04` `literal` The route `/api/health` returns `200` once the app is ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-06` `contract` The server binds the all-interfaces address rather than loopback `src: Deployment contract`
- [ ] `C-DC-07` `contract` A list endpoint returns a top-level JSON array `src: Deployment contract`
- [ ] `C-DC-08` `contract` An invalid call is rejected as a client error, never as a server error `src: Deployment contract`
- [ ] `C-DC-09` `constraint` An invalid call never succeeds silently `src: Deployment contract`
- [ ] `C-DC-10` `contract` Bearer auth is carried on everything except login, signup, health, the public storefront reads, the terms page `src: Deployment contract`
- [ ] `C-DC-11` `constraint` An in-memory list of invoices does not stand in for the billing platform `src: Deployment contract`
- [ ] `C-DC-12` `constraint` A receipt written to a log file does not stand in for a message sent over SMTP `src: Deployment contract`
- [ ] `C-DC-13` `constraint` An order row written with no invoice in the billing platform does not count as a sale `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `creator@example.com` | the seeded creator address | `C-RL-16` |
| `buyer@example.com` | the first seeded reader address | `C-RL-16` |
| `buyer2@example.com` | the second seeded reader address | `C-RL-16` |
| `deku-demo-pw-2026` | the seeded password | `C-RL-17` |
| `Marlowe Quill` | the creator display name | `C-RL-18` |
| `Ines Calder` | the first reader display name | `C-RL-18` |
| `Tobias Renn` | the second reader display name | `C-RL-18` |
| `IE` | the taxed jurisdiction | `C-RL-19` |
| `US` | the zero-rated jurisdiction | `C-RL-19` |
| `access_token` | the login response key | `C-CF-01` |
| `company_website` | the decoy field name | `C-CF-07` |
| `direct` | the lower fee tier channel | `C-CF-21` |
| `marketplace` | the higher fee tier channel | `C-CF-21` |
| `1900` | the taxed jurisdiction rate in bps | `C-CF-23` |
| `0` | the affiliate share on every order | `C-CF-42` |
| `1000` | the direct channel fee rate in bps | `C-CF-44` |
| `30` | the fixed fee component in minor units | `C-CF-44` |
| `2000` | the marketplace channel fee rate in bps | `C-CF-45` |
| `290` | the payment fee rate in bps | `C-CF-46` |
| `2400` | the worked case subtotal | `C-CF-49` |
| `480` | the worked case discount | `C-CF-49` |
| `365` | the worked case tax | `C-CF-49` |
| `2285` | the worked case total | `C-CF-49` |
| `222` | the worked case platform fee | `C-CF-50` |
| `96` | the worked case payment fee | `C-CF-50` |
| `1602` | the worked case net | `C-CF-50` |
| `100` | the zero-rated case payment fee | `C-CF-51` |
| `1820` | the zero-rated case net | `C-CF-51` |
| `1100` | the provider receivable account code | `C-CF-54` |
| `2100` | the tax payable account code | `C-CF-56` |
| `4000` | the platform fee revenue account code | `C-CF-57` |
| `5000` | the payment processing expense account code | `C-CF-58` |
| `handsel-ines-calder` | the first reader billing external key | `C-CF-75` |
| `handsel-tobias-renn` | the second reader billing external key | `C-CF-76` |
| `22.85` | the worked case invoice decimal amount | `C-CF-80` |
| `Handsel receipt: ` | the receipt subject prefix | `C-CF-88` |
| `lantern-press-kit` | the limited product permalink | `C-CF-93` |
| `384` | the marketplace channel platform fee | `C-CF-102` |
| `1440` | the marketplace channel net | `C-CF-102` |
| `LAUNCH20` | the open discount code | `C-CF-113` |
| `5` | the open code total usage cap | `C-CF-113` |
| `1` | the open code per-reader cap | `C-CF-114` |
| `EXPIRED10` | the closed discount code | `C-CF-115` |
| `Handsel Commerce Ltd` | the seller of record | `C-CF-120` |
| `field-notes-vol-one` | the first seeded product permalink | `C-CF-128` |
| `Field Notes Volume One` | the first seeded product name | `C-CF-128` |
| `Lantern Press Kit` | the limited product name | `C-CF-129` |
| `tide-tables-draft` | the draft product permalink | `C-CF-130` |
| `Tide Tables Draft` | the draft product name | `C-CF-130` |
| `standard` | the base tier code | `C-CF-131` |
| `Standard` | the base tier name | `C-CF-131` |
| `2400` | the base tier price on the first product | `C-CF-131` |
| `studio` | the upper tier code | `C-CF-132` |
| `Studio` | the upper tier name | `C-CF-132` |
| `5600` | the upper tier price | `C-CF-132` |
| `1000` | the limited product tier price | `C-CF-133` |
| `HS-00001` | the first order number | `C-CF-134` |
| `16px` | the body text size | `C-UX-10` |
| `24px` | the body line height | `C-UX-10` |
| `14px` | the interface text size | `C-UX-10` |
| `20px` | the interface line height | `C-UX-10` |
| `DATABASE_URL` | the datastore variable | `C-TR-03` |
| `killbill` | the billing provider slug | `C-TR-04` |
| `PAYMENTS_API_URL` | the billing platform variable | `C-TR-04` |
| `SMTP_HOST` | the mail host variable | `C-TR-05` |
| `SMTP_PORT` | the mail port variable | `C-TR-05` |
| `marlowe-quill` | the account handle | `C-DM-02` |
| `usd` | the payout currency | `C-DM-02` |
| `draft` | the unpublished-from-new product state | `C-DM-04` |
| `published` | the publicly readable product state | `C-DM-04` |
| `unpublished` | the withdrawn product state | `C-DM-04` |
| `1` | the seeded fee schedule version | `C-DM-07` |
| `open` | the live checkout session state | `C-DM-10` |
| `confirmed` | the completed checkout session state | `C-DM-10` |
| `refused` | the rejected checkout session state | `C-DM-10` |
| `expired` | the lapsed checkout session state | `C-DM-10` |
| `HS-` | the order number prefix | `C-DM-12` |
| `active` | the live entitlement state | `C-DM-15` |
| `revoked` | the withdrawn entitlement state | `C-DM-15` |
| `asset` | the asset account type | `C-DM-18` |
| `liability` | the liability account type | `C-DM-18` |
| `revenue` | the revenue account type | `C-DM-18` |
| `expense` | the expense account type | `C-DM-18` |
| `debit` | the left posting direction | `C-DM-21` |
| `credit` | the right posting direction | `C-DM-21` |
| `/api/health` | the readiness route | `C-DC-04` |
| `200` | the readiness response code | `C-DC-04` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the session identifier in a checkout address | `C-UF-03` |
| the entitlement identifier in a library address | `C-CF-85` |
| the bearer token value returned at sign-in | `C-CF-01` |
| the moment a seeded row is first written | `C-DM-01` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 4 | 6 |
| User roles | 1 | 19 |
| Core features | 21 | 134 |
| User flow | 5 | 17 |
| UI and UX notes | 8 | 38 |
| Front-end specification | 6 | 16 |
| Technical requirements | 4 | 9 |
| Data model | 3 | 23 |
| Constraints | 1 | 10 |
| Deployment contract | 10 | 13 |
