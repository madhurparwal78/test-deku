# Kilnly

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, watch the intro reel finish, throw the pile of pills in the hero, open the catalogue, filter to outerwear, start a project from the `Washed Work Jacket` card, and then sign in as an operator, read one comparable landed cost per unit for five supplier replies that arrived in three currencies on two unit bases, accept an offer, and watch a buyer check out of the storefront on to order `KLN-000412`, all without hitting an error page. Three things in that sentence cannot be arranged inside the app's own screens. The money is one of them: a fiat order that has settled must exist as an invoice for its own total in `USD` on an account in the billing platform at `PAYMENTS_API_URL`, keyed by the buyer's address, and a confirmation the app returns to itself does not count. The stock is the second: `available` for every stock keeping unit at every location is the sum of an append-only ledger, so when two buyers reach for the last `KJ-WORK-M` in Newark at the same instant, exactly one order exists afterwards and the other buyer is refused. The promise is the third: the delivery window a buyer is given at checkout is recorded with the inputs that produced it, and when a factory slip, a carrier degradation and a customs hold land on one order, that order carries one recomputed window, one recorded cause and one notification in the buyer's inbox, never three and never silence.

## Overview

Kilnly is two products on one origin. The public marketing site sells an end to end merchandise service to small brands: a landing page that opens with a reel of the chores it takes away and a hero pile of coloured pills naming each of them, a catalogue of pieces already sourced, sampled and shipped, a page that walks the whole of what happens after manufacturing, a no-minimum offer, a company page, a field-notes index, a brand kit and the legal set. The console behind it is the machine that page describes: briefs become factory quotes, quotes become sampled and inspected production runs, finished goods land in two warehouses on different continents, a gated storefront sells them in fiat or in tokens, and every order walks pick, pack, carrier handoff, customs, sales tax, tracking and returns with one place to watch it.

Six audiences use it. A founder briefing a product, who needs to know what a run costs before committing to it. An operator running that run day to day. A finance member who reads landed cost, margin, tax and payouts. A viewer who may read and change nothing. A buyer, usually on a phone, who wants the thing and a date. And a software agent shopping on somebody's behalf, which must walk exactly the same corridor as the buyer.

The site's own argument is the specification's spine, and it is stated on the fulfillment page in four words: nobody owns the delivery date. Four vendors each do their piece correctly, none of them can see the other three, and the brand is the only party with a view of the whole chain. This product owns that date, which is why a promise here carries its inputs, an owning stage and an explicit re-promise rather than a silently moving estimate.

What it deliberately is not. There is no real factory, carrier, customs authority, tax authority, chain node, wallet provider or card network: each is modelled inside this app against seeded data and operator actions, and every one of them is observable through the product's own surfaces. No comments, no likes, no follower graph, no chat. No native application. No second datastore, cache, queue, object store, identity provider or mail vendor. No downloaded image, video or font binary ships: every mark, garment, panel and partner logo is drawn or generated from a seed at run time.

The genuinely hard part is that physical objects and money are both unforgiving and neither of them lives in a screen. A count of shirts is not a column, it is the sum of every movement ever recorded; a quote in Brazilian real per dozen delivered under one incoterm is not comparable with a quote in euro per piece under another until both have been carried all the way to a landed cost per unit at the brief's own quantity; tax that rounds per line must still sum exactly to the invoice, and a refund of one line must give back exactly the tax that line contributed, which is only possible if the split was written down when the order was priced.

## User roles

Two roles live on the public surfaces and four live inside a brand workspace. A role is read from the signed-in member's membership row and never from a request body, a query parameter or a header the caller controls.

| Role | Can do | Cannot do |
|---|---|---|
| Visitor | Read every marketing route, the catalogue, the field notes, the brand kit and the legal set; read the storefront's ungated listings; place an order as a guest; read their own order by its reference and access token | **Read any project, brief, quote, supplier, cost, inventory figure, another buyer's order, or any gated listing or gated price without proving the entitlement** |
| Buyer | Everything a visitor can, plus sign in, read their own orders and returns, open a return, prove an entitlement, pull a gacha and claim a redemption | **Read another buyer's order, return or claim, and read anything inside a brand workspace** |
| Viewer | Read every project, brief, quote comparison, sample round, run, inventory figure, order and report inside their own workspace | **Write anything at all: approve a sample, accept an offer, move a run stage, adjust stock, change a price, answer a support conversation, or send an announcement** |
| Operator | Everything a viewer can, plus run projects: write briefs, request and accept quotes, decide sample rounds, move run stages, receive and transfer stock, build storefronts and gates, run drops, fulfil orders and answer support | **Change a member's role, change the workspace's return or approval policy, issue or revoke an agent credential, or read a payout record** |
| Finance | Everything a viewer can, plus read landed cost, lot cost, margin, the money ledger, tax by jurisdiction, backer payouts and the filing report, and issue a refund | **Move goods: decide a sample, accept an offer, move a run stage, adjust stock, or fulfil an order** |
| Owner | Everything inside their own workspace, including member roles, policy, agent credentials and closing a project | **Reach another workspace's projects, suppliers, costs, inventory, orders or buyers by any route** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Viewer session to any Operator-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create an account, and an account with no membership is a buyer. Joining a workspace is by invitation from its Owner. A buyer's entitlements are never granted by signup: they are proven, and they are recomputed every time they are read.

Eight accounts are seeded, every one of them on the password named in `## Data model`. Inside the workspace `Tidewater Goods`: `owner@example.com` is Imogen Hale, the Owner; `operator@example.com` is Sam Oyelaran, the Operator; `finance@example.com` is Grace Lindqvist, Finance; `viewer@example.com` is Nell Okonjo, the Viewer. Inside the workspace `Copperline Club`: `owner2@example.com` is Bea Calder, its Owner. Three buyers belong to no workspace: `buyer@example.com` is Tomas Renn, who holds the `kilnfolk-genesis` collection and is therefore entitled to the gated listing and the holder price; `buyer2@example.com` is Ada Sorensen, who holds nothing; `buyer3@example.com` is Milo Fenn, who holds nothing.
## Core features

### Auth

Email and password are exchanged for a bearer token returned as `access_token`. Passwords are stored under a modern memory-hard password hash and never in any recoverable form. The client sends the token as a bearer credential on every API call.

1. Signing in with a wrong password is refused, and the refusal names neither field, so the form cannot be used to discover which addresses have accounts.
2. Signing out invalidates the token; a request replaying that token afterwards is denied.
3. An account with no membership row is a buyer and reaches no workspace route.
4. A password reset request answers identically for an address that exists and one that does not.

### The marketing site

Nine public routes, listed in `## User flow`, all on the same origin as everything else. They are rendered from the product's own components against the seeded fixtures, never from a static export, so a price on the marketing site and a price in the quoting catalogue cannot disagree.

1. First load plays an intro reel once per session: a vertical column of star glyphs and a rotating status line naming the chores the product replaces. The twelve lines are pinned in `## Front-end specification` and appear exactly as written.
2. The reel never blocks navigation. A visitor who asks for another route while it is playing gets that route.
3. The header is a floating pill carrying the wordmark, two dropdown menus and a whitelist link, and a contextual strip at its right that begins as a line of text with an inline link and becomes a solid `Book a demo` pill once the page has scrolled past the hero.
4. The footer carries four columns, named in `## Front-end specification`, over the copyright line, on every route.
5. Each public route leads with one primary action, visually distinct from every secondary one on that route.

### The landing page

The band order is fixed and is the order given in `## Front-end specification`.

1. The hero carries a backer endorsement chip, the display headline, the two-line standfirst and the mascot, and beneath them the pile of pills.
2. The pile is a two-dimensional physics simulation. Its thirteen pills, each naming one chore, fall, collide, come to rest in a heap, and can be thrown with the pointer. They remain readable at rest, never leave their container, and settle rather than jittering indefinitely.
3. The pills are decorative. Their words are also present as an ordinary list for assistive technology, and their meaning does not depend on the simulation running.
4. Under a reduced-motion preference the simulation does not run and the pills render in a designed static arrangement.
5. The simulation starts after first paint, caps how many bodies it steps, stops stepping while it is off screen or while the tab is in the background, and is torn down on navigation.
6. Four capability panels each carry a headline, a line of copy and a working product mock built from the product's own components on the seeded fixtures, not a picture of one.
7. The extras grid carries eight cards, each with a status chip and one line of copy. Every one of those eight names a platform capability specified below, and a card whose capability is absent is an unfinished page rather than a rendered one.

### The catalogue

1. The catalogue lists eight products. Each card carries a generated product image, the title, a from-price and a minimum order quantity, and a `Start a project` action.
2. The eight are, with their from-prices in minor units and their minimums: `Acid-Wash Patch Tee` at `3400` with `100`; `Embroidered Logo Tee` at `3000` with `100`; `Acid-Wash Embroidered Hoodie` at `4800` with `50`; `Embroidered Quarter-Zip` at `4800` with `50`; `Embroidered Dad Cap` at `1900` with `100`; `Washed Work Jacket` at `6800` with `50`; `Canvas Duffel Bag` at `4200` with `50`; `Canvas Tote` at `2200` with `100`.
3. Category chips filter the grid: `All`, `Apparel`, `Outerwear`, `Headwear`, `Accessories`. The active filter is carried in the address, so a filtered catalogue is a link somebody can send.
4. The grid stays responsive at ten thousand rows by drawing only what is on screen, and the price and the minimum stay on the card at every width.
5. `Start a project` carries the product identity into a new brief, and the brief opens with that product already chosen.
6. Prices and minimums are read from the same catalogue the quoting engine reads. A marketing page may never show a price the platform would not honour.

### The fulfillment page

1. The page opens with its title and the paragraph about brands stitching fulfillment together from a third-party logistics provider, a customs broker, a tax filer and whoever picked up the phone.
2. Its thesis line `Nobody owns the delivery date.` appears exactly, followed by the paragraph explaining that four vendors each do their piece correctly and none can see the other three.
3. Two figures anchor the page: `11` operations surfaces run, and a minimum order of `1`.
4. Six subject sections follow, each a heading and a paragraph: warehousing, third-party distribution, customs and duties, sales tax, returns, and quality control before any of it. Their copy is pinned in `## Front-end specification`.
5. Four questions follow in an accordion, and the closing band carries `One chain, one place to watch it.`
6. Every claim on this page binds a capability below: the eleven surfaces are the eleven named in the fulfillment feature, the delivery-date ownership is the promise feature, and the quality gate is the sampling feature.

### The no-minimum offer, about, field notes and the brand kit

1. The no-minimum route states the offer, the trade-off between unit price and commitment in plain words, which products are available on that path, and a way into a brief. It binds the quoting engine, which must price a single unit as honestly as a thousand.
2. The about route carries the company position and the team on the paper ground with drifting panels.
3. The field-notes index carries cards with a category, a title and a read time, and each article opens in a reading shell. The categories are `Supply chain`, `Commerce` and `Industry`.
4. The brand kit route shows the marks and their clear space, the palette swatches, the two families with specimens and the usage rules. Every swatch is generated from the same token source the rest of the site reads, so the page cannot contradict the site.

### The legal set, the not-found screen and the machine-readable routes

1. `/legal/website-terms-of-use` renders the terms in a reading column with a dated header, and is reachable from the footer of every page and from the signup form.
2. `/legal/privacy` renders the privacy statement in the same shell and states what the product records about a buyer and how long it is kept.
3. An unknown address renders the product's own not-found screen carrying the line `Page not found` and a way back to the landing page, and the response is a not-found answer rather than a success.
4. Every internal link on every public route resolves. A link in the header, the footer or the body of a public route that answers not found is a defect.
5. `/sitemap.xml` lists every public route, and `/robots.txt` points at it.
6. Every public route carries its own title and description, and no two public routes share either. Every public route also declares a social preview title and a preview image, and that preview image resolves.

### The console shell and projects

1. Behind sign-in, a member works inside one brand workspace holding projects. A project is one product journey from brief to shipped units and carries its state, its quotes, its samples, its run, its inventory and its orders.
2. The project list is a grid of cards, each carrying a state chip and a line naming the one next action. It has an empty state naming its one next action.
3. A global search reaches projects, orders, suppliers and stock keeping units inside the caller's own workspace and nothing outside it.
4. A notification centre carries promise revisions, stock refusals, quality decisions and support escalations, newest first.
5. Creating a project is its own route rather than a layer over the list, and the route is reachable by address.
6. Every list surface in the console carries a designed empty state naming its one next action: no projects, no quotes yet on a brief, a supplier that declined, an empty warehouse location, a drop with nothing left, and a support queue at zero. A list that renders nothing at all is an unfinished screen.

### The brief and the artwork gate

1. A brief captures the base product, the quantity or range, the colourways, the sizes and their curve, the decoration method per placement, the artwork per placement, the materials and weight, the packaging, the target landed price per unit and the date the goods are needed by.
2. Decoration methods are `screen_print`, `embroidery`, `patch` and `wash`, and each placement carries exactly one.
3. Artwork is validated against the chosen method before a quote may be requested. The rules are: an effective resolution of at least `150` pixels per inch at the printed size; at most `6` spot colours for `screen_print`; at most `12` thread colours for `embroidery`, with a stitch-count estimate recorded; a bleed of at least `3` millimetres; and artwork wholly inside the placement's safe area.
4. A refusal is written in the artwork's own terms and names the offending measurement. An artwork `900` pixels wide placed at a printed width of `30` centimetres is `76` pixels per inch, and the refusal says so against the `150` minimum rather than reporting a generic failure.
5. A brief whose artwork has not passed cannot request quotes, and a request that names it is refused.
6. Every form in the console refuses invalid input inline, names the field it refuses, and writes nothing.

### Sourcing, quotes and landed cost

1. Requesting quotes fans the brief out to every eligible supplier. Eligibility is a match on capability, that is the decoration methods, the materials, the minimum quantity, the certifications and the region, and it is data rather than code.
2. Suppliers reply with different response times, some partially, some with a counter-offer, and some with a decline. Requests, replies and reminders are durable: a restart loses none of them.
3. An offer carries its currency, its incoterm, its unit basis, its setup and tooling fees, its price breaks, its lead time, its minimum quantity and its validity.
4. Every offer is normalised into one landed cost per unit, in integer minor units, at the brief's own quantity, and the working is shown: the unit price, the setup amortised across the run, freight by mode, duty by classification and destination, insurance, and the currency rate with the date it was taken.
5. The arithmetic is exactly this. A per-dozen quote of `46800` minor units is `3900` minor units per piece. A price of `3900` minor units in `eur` at a recorded rate of `1.08` taken on `2026-09-01` is `4212` minor units in `usd`. A setup fee of `85000` minor units across a run of `500` units adds `170` minor units per unit. Sea freight of `120000` minor units for that run adds `240` minor units per unit. Duty at `12` percent of `4212` adds `505` minor units. Insurance at `0.4` percent of `4212` adds `17` minor units. The landed cost per unit is `5144` minor units.
6. The seeded comparison makes the point the site makes. At a quantity of `500` units of the `Washed Work Jacket`, `tirupur-mills` carries the lowest headline unit price at `2900` minor units and the highest landed cost at `6010` minor units, because its setup of `900000` minor units amortises to `1800` per unit and its air freight adds `950`. `aveiro-knitworks` carries a headline of `4212` and a landed cost of `5144`, and is the offer that should be accepted. Choosing on headline unit price alone is the wrong answer here.
7. Two offers may be compared only after normalisation, and the comparison is stable under reordering: the same set of offers returns the same ranking whatever order they arrived in or were requested in.
8. A quote records the rate it used and the date of that rate. A later rate movement never changes a historical quote.
9. Price breaks are reported as the quantity thresholds at which a supplier's unit cost steps down, and the brief's quantity is evaluated against the resulting cost curve rather than a single headline figure. `aveiro-knitworks` steps at `250`, `500` and `1000` units.
10. An offer expires `14` days after it is made. Expiry is a state the offer moves into, not a warning drawn on a screen: an expired offer cannot be accepted and must be re-requested, and an attempt to accept one is refused.
11. A supplier's contacts, its quoted prices and its terms are readable by the Owner, the Operator and Finance only. They never appear in a storefront payload, an agent payload, a buyer-facing page or an export a buyer can reach.

### Samples and quality control

1. A project may run several sample rounds. A round records what was requested, what arrived, photographic evidence per angle, measurements against a size specification with tolerances, and one decision: `accept`, `rework` or `reject`.
2. A defect carries a severity from `critical`, `major` and `minor`, and a location on the garment, from a fixed taxonomy.
3. A rework carries its defect list forward, so a later round is checked against exactly what was asked for.
4. An approval is attributable and immutable: who accepted, when, and against which evidence. An accepted sample becomes the reference the batch is judged against.
5. Before a run may ship, a batch inspection samples it by the acceptance rule recorded on the project. The seeded rule inspects `80` units from a run of `500` and accepts at most `0` critical, `2` major and `5` minor defects.
6. Exceeding the rule blocks the shipment and raises a decision to the brand of `rework`, `partial_accept` or `reject`. A blocked batch cannot be dispatched, and a dispatch attempt against it is refused.

### Production runs

1. A run is an accepted quote turned into work, and it walks the stages `purchase_order`, `deposit`, `materials`, `production`, `quality`, `packing` and `freight_handover`.
2. Each stage carries an expected window, an actual, and an owning member.
3. A stage that slips recomputes the projected ready date and raises the re-promise described below. A projected date that moves without a recorded cause is a defect.
4. A run may split across two factories when capacity requires it. Split lots are tracked separately through quality and inventory, so a defect in one lot cannot be masked by the other.
5. A purchase order records its deposit percentage and its payment terms, and deposits paid, balances due and outstanding liabilities appear in the finance view and reconcile to the money ledger.

### Inventory across warehouses

1. Stock lives in two locations, `rotterdam` and `newark`, on different continents, and inventory is multi-location everywhere it appears.
2. The inventory ledger is append-only, in whole units, per stock keeping unit per location. Its kinds are `receipt`, `reservation`, `allocation`, `pick`, `shipment`, `return`, `write_off`, `transfer_out` and `transfer_in`.
3. `on_hand` and `available` are summed from that ledger every time they are read. No mutable count of stock exists anywhere in the product, and no surface may show a figure that was not computed this way.
4. `available` equals `on_hand` minus reservations minus damaged.
5. An order reserves stock when it is placed and allocates it when it is picked. A cancelled or expired order releases its reservation.
6. Two orders racing for the last unit resolve to exactly one reservation and one clear refusal. A balance never goes negative and stock is never oversold, however many times the race is run. The seeded boundary is one unit of `KJ-WORK-M` available at `newark` and none at `rotterdam`.
7. A cross-continent transfer between locations is an in-flight state, and routing an order is decided against both. Units leave the origin's `on_hand` when the transfer departs and join the destination's when it is received, and they belong to neither location while in transit, where they are visible as in transit rather than missing.
8. An order is routed to the location that can actually serve it, weighing stock, destination, carrier cost and customs consequence. An order split across two locations is one order with two parcels and one delivery promise.
9. Consumption rates per stock keeping unit produce a projected stockout date and a suggested reorder point, and the forecast flags both stockouts and dead stock.
### The storefront and gating

1. Each workspace publishes one hosted storefront with collections, product pages, a cart and a checkout, themed from the same token source the marketing site reads.
2. A gate rule binds a listing or a price to an audience. The audience tests are an allowlist of addresses, ownership of a token or a collection, a minimum balance, a purchase history and a code, and they compose with `and`, `or` and `not`.
3. Gate evaluation happens on the server, both when a listing is rendered and again when the order is placed. A request forged for a gated listing or a gated price by a caller without the entitlement is refused at the order, not merely hidden at the render. Hiding a listing in the interface is not gating.
4. The seeded gate is `holder-work-jacket`: the `Washed Work Jacket` at a holder price of `5900` minor units against a public price of `8900`, released to holders of the `kilnfolk-genesis` collection. `buyer@example.com` is entitled; `buyer2@example.com` is not.
5. Proving an entitlement recomputes the visible catalogue, the prices and the perks in place, without a page reload and without the page flashing through an intermediate state.
6. A visitor who disconnects mid-session returns cleanly to the ungated state. Anything already in the cart is re-evaluated, and a line that is no longer eligible is marked as such and left in the cart for the buyer to decide about. Silently dropping it is a defect.
7. Proving ownership of an address is a signature challenge carrying a nonce and an expiry and bound to the session. A replayed signature is refused, and the challenge asks for nothing beyond proof of control of the address.
8. The storefront is designed for a phone first. Gating, cart and checkout are complete and comfortable at a narrow viewport, with the wallet connection and the signature flow handled in the page.

### Checkout, payments and money

One checkout accepts both rails and settles both into one order and one money ledger.

1. An order is priced once. Its line amounts, its shipping, its tax and its total are recorded in integer minor units of its settlement currency at that moment, and the tax and the shipping are computed before payment rather than after.
2. An order reference is `KLN-` followed by six digits allocated in sequence, for example `KLN-000412`.
3. The fiat rail is the billing platform named in `## Technical requirements`. A settled fiat order creates or reuses one account there keyed by the buyer's address lowercased as its `externalKey`, and raises one invoice on that account for the order total in `USD`.
4. A checkout replayed with an `Idempotency-Key` the server has already seen returns the same order it returned the first time, and creates no second account, no second invoice and no second confirmation mail.
5. The token rail quotes an amount that holds for `15` minutes against a rate recorded with its timestamp. The buyer pays, and the platform treats the payment as settled only at a confirmation depth of `12`.
6. The four token edge cases are an underpayment, an overpayment, a late payment and a reorg of the chain. Each has a defined, non-destructive resolution, and none of them may leave the order and the money ledger disagreeing. An underpayment credits what arrived and leaves the order awaiting the balance. An overpayment credits the order and records the excess as refundable. A payment arriving after the quote window has expired is re-quoted rather than refused outright. A chain reorganisation that undoes a confirmation already treated as settled re-opens the order and reverses its settlement entry, and the ledger carries both the entry and its reversal.
7. Treating a single confirmation as settled is a defect: the depth is `12`.
8. The buyer's receipt, the workspace's order record and the finance report agree to the minor unit for every order.
9. A refund mirrors the rail it came from, is recorded as its own ledger event, and never exceeds the captured amount.
10. Every money movement is a row in an append-only money ledger, and every figure in a finance view is a sum of that ledger.

### Fulfillment, the eleven surfaces

1. The platform runs eleven operations surfaces as one chain, and they are exactly: `receiving`, `put_away`, `storage`, `replenishment`, `pick`, `pack`, `carrier_handoff`, `customs`, `sales_tax`, `tracking` and `returns`.
2. An order walks a forward-only state machine with a terminal set. Its states are `placed`, `reserved`, `picked`, `packed`, `handed_over`, `in_transit`, `delivered`, `cancelled` and `returned`, and a transition backwards is refused.
3. Every transition is recorded with the member or the system that made it and the moment it happened, and every transition is visible to the buyer in ordinary words on their own order page.
4. Pick lists are batched across orders. Packing is verified against the order's contents, and the parcel's dimensions and weight produce the shipping quote.
5. Carrier handoff records the label and the tracking identity. Several carriers sit behind one interface offering rates, transit estimates, label creation and tracking updates.
6. A carrier outage reroutes the parcel to an alternate and records the cost difference. It never changes the buyer's promised window silently.
7. Tracking events flow from the carrier into the order timeline and into the buyer's chosen channel, deduplicated so a carrier resending an event does not notify twice.
8. Exceptions are first-class, each with a defined path, an owner and a clock: an address failure, a customs hold, damage in transit and carrier loss. An order that sits in `handed_over` with no exception and no movement past its clock is raised rather than forgotten.

### Customs, duties and sales tax

1. Every product carries a customs classification code, a country of origin and a declared value basis. A cross-border shipment generates its documentation set from those three.
2. A missing or invalid classification blocks the dispatch before it leaves, rather than at the border. The seeded case is the stock keeping unit `CT-NAT-OS`, which carries no classification: an attempt to dispatch it cross-border is refused and names the missing classification.
3. Duty and import tax are estimated at checkout for delivered-duty-paid destinations and shown to the buyer as their own line. The difference between the estimate and the actual assessment is reconciled into the order and the money ledger rather than absorbed.
4. Sales tax is computed by destination jurisdiction from a rate table carrying effective dates, respecting product taxability categories. The seeded jurisdictions are `NL` at `21` percent rounding per invoice, `GB` at `20` percent rounding per invoice, and `US-CA` at `8.5` percent rounding per line.
5. Tax is computed on the taxable base per line, rounded by the jurisdiction's own rule, and the sum of the lines equals the invoice total exactly. Any rounding remainder is allocated by largest remainder rather than dropped.
6. The worked case is pinned. An order into `NL` with three lines of `3333`, `3333` and `3334` minor units carries an invoice tax of `2100` minor units. The unrounded line shares are `699.93`, `699.93` and `700.14`, which floor to `699`, `699` and `700` and sum to `2098`. The remainder of `2` is allocated to the two largest fractional parts, so the recorded allocation is `700`, `700` and `700`.
7. A refund of one line returns exactly the tax that line contributed, read from the allocation recorded when the order was priced rather than recomputed at refund time.
8. Economic nexus thresholds are tracked per jurisdiction and the workspace is warned before one is crossed. The seeded threshold is `10000000` minor units of sales into a jurisdiction in a calendar year.
9. A period filing report per jurisdiction reconciles collected tax to orders and refunds, and balances to a difference of zero.

### Returns

1. A return is a fulfillment run in reverse: authorisation with a reason code inside a window, a label issued, receipt at a warehouse, inspection against a condition grade, then `restock`, `refurbish` or `write_off`.
2. The refund and the inventory event are issued from that one inspection decision, so the money and the stock can never disagree about what came back.
3. A return crossing a border generates its own customs paperwork and may reclaim duty.
4. A refund never precedes the inspection unless the workspace's policy says so explicitly, and that policy choice is recorded on the order at the time the order was placed rather than read from today's setting.
5. The return window is `30` days from delivery, and a return authorisation requested outside it is refused.

### The delivery date

1. At checkout a buyer is given one delivery window, computed from real inputs: the production stage if the goods are not yet made, warehouse availability and location, carrier transit for the destination, the customs profile and the current backlog.
2. The promise is recorded with the inputs that produced it. A promise with no recorded inputs is not a promise.
3. Every open promise has one owning stage, and ownership moves with the order as it moves.
4. When any input moves enough to change the window, the platform recomputes it, records the revision with its cause, and notifies the buyer once with the new window and the reason. Letting a date pass silently, or recomputing without telling anybody, is a defect.
5. A factory slip, a carrier degradation and a customs hold landing on one order produce one recomputed window, one recorded cause naming all three, and one notification. Three notifications for one recomputation is a defect.
6. The console shows every promise at risk, ranked by how far it has slipped.
7. A promise kept or missed is recorded per order, and on-time performance is reported by stage, by supplier, by carrier and by lane.

### Drops, gachas and pre-sales

1. A drop is a scheduled sale with a start instant, a supply, an allowance per buyer and an optional gate. The seeded drop is `kilnfolk-winter` with a supply of `40` and an allowance of `2`.
2. A fixed supply sold into a rush never oversells, and the per-buyer allowance holds across parallel sessions and across agent credentials belonging to the same owner.
3. A buyer who arrives after the supply is committed is placed in a queue with an honest position rather than left on a spinner.
4. A gacha is a blind box with published odds per outcome. The seeded odds are `common` at `0.70`, `rare` at `0.25` and `grail` at `0.05`.
5. The odds are published before the drop opens and are immutable while it runs.
6. Each pull is drawn from a randomness scheme committed before the drop: the seed's digest is published beforehand and the seed itself is revealed afterwards, so a buyer can check that their own pull was decided before they paid. Drawing an outcome from an uncommitted source at pull time is a defect.
7. A pull maps to a physical stock keeping unit. A pull that would exceed the remaining stock of its own outcome is prevented before the money is taken, never resolved afterwards.
8. After the drop closes, the realised distribution is reconciled against the published odds and the comparison is readable.
9. A pre-sale sells a product before it is produced, with a funding threshold of `5000000` minor units, a deadline, a refund path if the threshold is missed, and a revenue-share record per backer that survives into the payout report. Money taken for an unproduced good is held as its own ledger kind, distinct from settled revenue.

### The agent channel

1. A machine-readable catalogue exposes products, variants, prices, availability, lead times and shipping options, under the same gating and the same inventory truth as the human storefront.
2. An authenticated agent may quote, reserve, pay and receive a confirmation without a browser, walking exactly the same reservation, tax and promise machinery a buyer walks. A second code path for agents is a defect: it is how the inventory and tax invariants quietly diverge.
3. An agent acts under a scoped credential carrying an owner, a set of scopes, a spend limit and a rate limit, with every call recorded against it.
4. A credential is revocable, and revoking one releases its open reservations immediately.
5. An agent cannot be used to exceed a drop allowance or to pass a gate its owner does not hold. A drop allowance counts a buyer's own orders and the orders of every agent credential that buyer owns together.

### Reporting, support and procedures

1. Reporting covers revenue, units, landed cost and margin per product, per channel and per period; on-time performance; inventory turns and dead-stock exposure; tax collected per jurisdiction; and backer payouts.
2. Every figure derives from a ledger, and the same period totalled by different axes agrees exactly. Revenue for a month by product, by channel and by lane are three sums of one ledger and must return the same total.
3. Support is a queue of buyer conversations with the order context attached. An answer is written by a member or drafted by an assistant that may cite only the workspace's own procedures and the facts of that order.
4. An assistant that cannot ground an answer in a procedure or an order fact escalates the conversation to a member instead of improvising. An answer that cites neither is a defect.
5. Procedures are versioned documents. An answer records which version it was drafted from, so a later policy change does not rewrite what a buyer was told. The seeded workspace carries three procedure versions of its returns policy.
6. The support queue at zero carries an empty state naming its one next action.

### Marketing email

1. An announcement sends to a consented audience with the suppression list honoured, and a send is recorded per recipient.
2. An unsubscribe takes effect immediately and across every future send, and a suppressed address receives nothing thereafter.
3. Mail leaves over real SMTP at `SMTP_HOST` and `SMTP_PORT`. Three transactional subjects are pinned. A confirmed order sends a mail to the ordering buyer's address alone whose subject begins `Kilnly order confirmed: ` followed by the order reference. A promise revision sends a mail whose subject begins `Kilnly delivery update: ` followed by the order reference. An authorised return sends a mail whose subject begins `Kilnly return authorised: ` followed by the return reference. The seeded announcement's subject is exactly `Kilnfolk winter drop opens Friday`.
4. Every one of those bodies names the order or return it is about and the buyer it is addressed to, and carries no other recipient in copy.
5. Moving an order from `picked` to `packed` sends no mail. Only the three transitions named above send anything, and a mail sent on any other transition is a defect.

### The holder community and redemption

1. A holder's standing is computed at read time from current entitlements: token or collection ownership, allowlist entry and purchase history. A membership flag written once at signup and never re-checked is a defect, because holders sell their tokens and a perk must follow the asset rather than the account.
2. A short cached view of standing is allowed, and it is invalidated explicitly when an entitlement changes.
3. The holders hub shows what a holder owns, what it entitles them to, which past drops they took part in, and what is redeemable now.
4. A redemption claim does three things together: it marks the entitlement as used, it reserves physical stock, and it creates a zero-price or reduced-price order that walks the ordinary fulfillment chain. Either all three happen or none of them does.
5. A claim that reserves stock but fails to mark the entitlement would let one token claim twice. A claim that marks the entitlement but fails to reserve would leave a holder owed a product that does not exist. A failure in any one leg unwinds the other two.
6. An entitlement transferred to another address in the same instant as a claim resolves once. Exactly one of the claim and the transfer takes effect, never both.
7. Redemption windows open and close on a schedule. An unclaimed entitlement past its window is reported as unclaimed rather than silently expired.
8. An allowlist entry may be imported, earned by an action, or granted per campaign, and every entry records why it exists.

### Production economics and capacity

1. The cost model per run carries unit cost, tooling and setup, freight by mode, duty, insurance, inspection, warehousing per unit-month, pick and pack per order, carrier cost per lane, payment fees per rail and a returns allowance.
2. Margin per product is computed against the actual landed cost of the lot a unit came from, never an average across lots.
3. Units are consumed from lots in a stated order, and the cost of goods sold for an order is the cost of the lots actually shipped. A mixed-lot order reports its margin per lot. The seeded case carries two lots of `KJ-WORK-M` at landed costs of `5144` and `6010` minor units.
4. Each supplier declares a throughput per method per week. The quoting engine refuses a lead time that throughput cannot support rather than quoting it, and the run board shows the queue a new run would join.
## User flow

The information architecture is two route families on one origin: nine public marketing routes and a storefront that anyone may reach, and a console behind sign-in.

| Route | Purpose | Auth |
|---|---|---|
| `/` | Landing: intro reel, hero and pill pile, supported-by band, positioning, four capability panels, the extras grid, closing band | public |
| `/catalogue` | Latest productions with category chips, prices and minimums | public |
| `/merch-fulfillment` | The eleven operations surfaces, the six subjects and the four questions | public |
| `/custom-merch-no-minimum` | The no-minimum offer and its trade-offs | public |
| `/about` | The company page | public |
| `/blog` | Field notes index | public |
| `/blog/:slug` | One field note in its reading shell | public |
| `/brand` | Brand kit: marks, palette, type and usage | public |
| `/legal/website-terms-of-use` | The terms document | public |
| `/legal/privacy` | The privacy statement | public |
| `/sitemap.xml` | Every public route | public |
| `/robots.txt` | Points at the sitemap | public |
| `/shop` | The storefront collections | public, gates evaluated |
| `/shop/:slug` | One listing and its price | public, gates evaluated |
| `/cart` | The cart and its re-evaluated lines | public |
| `/checkout` | One checkout for both rails | public |
| `/order/:reference` | A buyer's own order, its timeline and its promise | reference and access token, or the owning buyer |
| `/drops/:slug` | A drop, its odds, its queue and its pulls | public, gates evaluated |
| `/holders` | The holders hub | buyer, entitlement proven |
| `/sign-in` | Sign in | public |
| `/sign-up` | Create an account | public |
| `/app` | Project list | member |
| `/app/projects/new` | Create a project | operator, owner |
| `/app/projects/:id` | One project: brief, quotes, samples, run, inventory, orders | member |
| `/app/inventory` | Ledger, balances and transfers across both locations | member |
| `/app/orders` | Every order in the workspace | member |
| `/app/orders/:reference` | One order, its chain, its promise and its exceptions | member |
| `/app/customs` | Classifications, documents and holds | member |
| `/app/tax` | Rate table, nexus warnings and the filing report | member |
| `/app/returns` | Authorisations, receipts and inspections | member |
| `/app/drops` | Drops, gachas, pre-sales and their reconciliation | member |
| `/app/agents` | Agent credentials, scopes, limits and revocation | owner |
| `/app/support` | The conversation queue and its procedures | member |
| `/app/procedures` | Versioned procedures | member |
| `/app/reports` | Revenue, margin, on-time, turns, tax and payouts | member |
| `/app/settings` | Members, roles and workspace policy | owner |

**Entry and redirects.** An unauthenticated request for any `/app` route lands on `/sign-in` and returns to the requested route once signed in. Signing out ends the session and a replayed token afterwards is denied. A token that expires mid-action returns the member to `/sign-in` with the pending work unwritten, and nothing is written on their behalf. A Viewer who opens `/app/projects/:id` reads it and finds no approval control; the same session calling the approval endpoint directly is refused by the server. A buyer who opens `/app` is refused. A member of `Tidewater Goods` who asks for a `Copperline Club` project by its identifier is answered not found, so the existence of the other workspace's rows does not leak.

**Journeys.**

1. A visitor opens `/`, lets the intro reel finish, reads the hero, throws the pile of pills with the pointer and watches it settle, scrolls the four capability panels and the eight extras cards, then opens `/catalogue`, chooses the `Outerwear` chip, and presses `Start a project` on the `Washed Work Jacket` card. They are asked to sign in, and the brief that opens already names that product.
2. `operator@example.com` completes the brief at `500` units, uploads an artwork `900` pixels wide for a printed width of `30` centimetres, reads the refusal naming `76` pixels per inch against the `150` minimum, replaces it with artwork that passes, and requests quotes.
3. Five suppliers reply over the following minutes in three currencies on two unit bases. The operator reads the comparison, sees `tirupur-mills` at the lowest headline of `2900` and the highest landed cost of `6010`, opens the working on `aveiro-knitworks` at `5144`, and accepts that offer. They then try to accept an offer that has expired and are refused.
4. A sample round arrives. The operator records two `major` defects with their locations, asks for a rework, accepts the second round, and then runs the batch inspection on `80` units. It finds three `major` defects, exceeds the acceptance rule, and the shipment is blocked with a decision raised to the Owner.
5. `buyer@example.com` opens `/shop`, connects and signs a challenge, and watches the gated `Washed Work Jacket` and the holder price of `5900` appear in place with no page reload. They check out, land on `/order/KLN-000412`, read a delivery window, and find one mail in their inbox whose subject begins `Kilnly order confirmed: `.
6. `buyer2@example.com` requests the same gated listing directly without the entitlement and is refused at the order.
7. `buyer2@example.com` and `buyer3@example.com` place orders for the last `KJ-WORK-M` at the same instant. One order exists; the other buyer is refused with a conflict naming the stock keeping unit, and `available` at `newark` is `0`, never negative.
8. The operator records a factory slip, a carrier degradation and a customs hold against one order. The buyer's order page shows one new window with one cause naming all three, and the buyer's inbox holds exactly one mail whose subject begins `Kilnly delivery update: `.
9. `buyer@example.com` opens `/holders`, claims a redemption, and the entitlement is marked, a unit is reserved and a reduced-price order is created together. The Owner then transfers the entitlement away and the perk is gone on the next read.
10. `finance@example.com` opens `/app/reports`, totals one month by product, by channel and by lane, and reads the same figure three times. They then refund one line of a `NL` order and see exactly `700` minor units of tax returned.

**States.** Every list carries a designed empty state naming its one next action. Every route carries a loading state, and the console's lists show their shape while they load rather than an empty page. An error is a message inside the surface that asked for the work, offering the action again; nothing throws the visitor to a blank screen, and a failed write leaves what the member typed in the field they typed it into.

## UI/UX notes

The north star: somebody arriving should believe a small brand can have real objects made without holding the whole chain in their head, and should feel the work is already underway. The register is split and the split is deliberate. The marketing site is consumer editorial with a point of view, and the product it is selling is the first thing seen. The console is an operational tool: quiet, dense but organised, built for scanning and for repeated action, with no oversized heroes and no editorial composition where the working interface belongs.

The page ground is a warm near-white, nearer paper than white, ruled on the landing page by a faint blueprint grid. The site alternates between that paper sheet and deep near-black panels, and that alternation is its one structural rhythm; nothing else is allowed to carry it. The ink is a near-black cool neutral and does the work of every piece of text. One light, vivid red-orange is the signal: it marks the things that can be pressed and it appears nowhere decorative, so a page with two things in that colour is claiming two primary actions. A softer tint of the same hue carries gradients and glows and never stands in for the signal itself. Three further colours carry meaning and appear nowhere else: one for a live or successful state, one for something pending, one for something destructive. A state that is none of the three borrows none of them. The exact shades are yours, so long as those exclusivity rules hold and body text meets WCAG AA contrast against the surface it sits on.

Type is two families with real distance between them. The interface family is a variable grotesk, `Inter`, and it does everything functional: body, tables, figures, controls, the console entire. The display family is a rounded face, `Baloo 2`, and it carries the wordmark and the display headlines and is where the brand's warmth lives; it never sets a table or a form label. The measured scale is carried: display lines at 80px and 60px, section heads at 48px, secondary statements at 35px, card titles at 24px, leads at 20px, standfirsts at 18px, body at 16px, dense interface text at 15px and 14px, metadata at 12px, and micro labels on chips and tags at 11px and 10px. Figures line up in a column wherever amounts stack, because this product stacks amounts constantly and a ragged column of money is unreadable.

The pill is the dominant shape, from the header through the chips to the buttons, and corners elsewhere are softened rather than rounded away. Depth is soft and warm rather than grey: cards sit on the paper with a small lift and a wide, warm blur, and dark panels sit flush. The header pill and the live chips carry a faint white inner rim that swells and subsides, which is the only thing on the page that breathes on its own. Space carries separation rather than rules: sections read as separate at a glance without a dividing line, and the gap between sections is several times the gap beneath a heading and about halves on a narrow screen. Space over dividers, and calm over expressive, throughout.

Motion has one character across the whole product: everything settles rather than snapping, leaving quickly and arriving slowly, and nothing uses a different speed to feel special. Entrances rise a short distance while they fade, once per band, and then stay arrived. The display headline arrives a word at a time, each word a fraction behind the one before, reading as somebody setting type rather than a machine drawing it. Photographic panels drift and scale very slowly. Dark panels twinkle and carry slow horizontal beams of light. Logo rows and testimonial columns run as continuous marquees. There is no scroll-scrubbed timeline anywhere: a reveal has two states and plays once. Under a reduced-motion preference the physics pile is arranged rather than simulated, and the drift, the twinkle, the beams and the marquees all stop; content renders in its finished arrangement rather than vanishing, and every transition that remains is a change of state rather than a journey across the screen.

The console commits to one arrangement: navigation down the left, work in the middle, detail beside it where comparison matters. Projects read as a grid of cards carrying a state chip and the one next action, because a founder scans for what needs them; quotes, inventory and orders read as tables, because a reader is comparing rows. Density is comfortable rather than cramped, since these decisions carry money and a mis-read row costs a run. Creating a project is its own destination rather than a layer floating over the list. A change a member makes appears in its row at once, and if the write fails the row returns to what the service actually holds with a message offering the action again, rather than leaving a number on screen that nothing agrees with.

Every control has resting, pointed-at, pressed, focused and unavailable states, and unavailable is never signalled by colour alone. Escape closes anything that opened over the page, and a destructive action asks first. Where there is no hover, anything that hover would reveal is pinned to its visible state instead of being unreachable, and every hovered affordance has a focus-visible twin that shows the same change, so keyboard navigation reveals exactly what a pointer reveals. Icon-only controls carry labels. Live regions announce order state changes, promise revisions, stock refusals and drop queue positions, batched so that a burst of events produces one announcement rather than one per event. Colour never carries meaning alone: live, pending and failed each carry a word as well as a mark.

Accessibility is a floor rather than a finish. The whole product is responsive across three widths and holds at every width between them. On a phone the landing page keeps its pile of pills with fewer bodies in a shorter container, the four capability panels stack with their mocks beneath the copy, the extras grid becomes two columns, and the header pill keeps its shape with the menus collapsing behind one control. The catalogue steps from four columns to two to one and keeps the price and the minimum on the card at every step. The console is honest about being a desk tool: below the tablet breakpoint the project list, the order detail, the support queue and the approvals stay fully usable, while the quote comparison and the inventory grid scroll sideways with their first column pinned. The storefront is designed for the phone first, because that is where buyers actually are. At a narrow viewport nothing overflows sideways and every navigation target stays reachable.

What this must not look like: a page dominated by one hue family with no second signal; decoration standing in for content; a marketing composition where the working console belongs; or a console that borrows the landing page's atmosphere and becomes hard to scan. Where the marketing site may be warm, the console earns its quiet.

## Technical requirements

The stack is fixed. The frontend is **SolidJS built with Vite**: the browser receives an application shell and the routes fetch their data from the JSON API on the same origin, except that every public marketing route carries its own title, description and social preview inside the document the server returns, so a route is identifiable before any script runs. The backend is **Litestar** on Python 3.12, serving the HTTP API on that same origin under the `/api` prefix. The datastore is **PostgreSQL** at `DATABASE_URL`. Mail goes over real SMTP to **Mailpit** at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. Billing is **killbill** at `PAYMENTS_API_URL`, with `PAYMENTS_API_KEY` and `PAYMENTS_API_SECRET`. Read every host, port and credential from the environment and never hardcode one.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL, Mailpit and killbill, and reaching for anything else is a contract violation.

Every call to the billing platform under `/1.0/kb/` carries three credentials together: the tenant key from `PAYMENTS_API_KEY` as `X-Killbill-ApiKey`, the tenant secret from `PAYMENTS_API_SECRET` as `X-Killbill-ApiSecret`, and HTTP Basic credentials whose user is `admin` and whose password is `password`. A write also carries `X-Killbill-CreatedBy`. The billing platform is a billing platform, not a card processor: there is no card, no token and no decline in it. `GET /1.0/healthcheck` is unauthenticated liveness. `GET /1.0/kb/accounts?externalKey=<key>` answers `200` when the account exists and `404` when it does not, and `externalKey` is unique per tenant. `POST /1.0/kb/accounts` takes `name`, `externalKey`, `email`, `currency` and `country`. `GET /1.0/kb/accounts/pagination` lists every account and `GET /1.0/kb/invoices/pagination` lists every invoice, reporting `amount` as a decimal such as `89.00` and `currency` uppercase. The tenant already holds the accounts `orbit-amelia`, `orbit-acme` and `orbit-northwind`.

**Simultaneous requests.** Two buyers placing an order for the same last unit at the same instant produce exactly one reservation; the winner receives their order and the loser receives a `409` conflict response naming the stock keeping unit that was taken, never a silent success and never a second reservation written behind the first. The same holds for a drop at its open, for a redemption claim racing a transfer of the entitlement it is spending, and for two members moving one run stage together: exactly one of them takes effect. A checkout replayed with an `Idempotency-Key` the server has already seen returns the same order and must not create a second invoice, so a shaky connection that submits twice leaves no duplicate charge behind it. Choose any mechanism.

**Money and units.** Money is integer minor units throughout, in `usd` unless an offer's own currency is being reported, and no floating-point value ever carries an amount. Counts of physical things are whole units. Every timestamp is stored absolute in UTC and rendered in the reader's own zone.

**Liveness.** One stream of events carries order transitions, inventory events, promise revisions and tracking updates, with a fallback that asks once a second where the stream is unavailable. The console, the storefront and a buyer's own order page all render from it, so two people watching one order see the same state within about a second of each other, and a change made in one of them appears in the others without a reload.

**Performance.** The physics simulation starts after first paint, caps its body count and its step rate, sleeps while off screen, and never holds the main thread while the page is idle. The inventory grid and the order list hold their frame rate at ten thousand rows by drawing only what is on screen and by asking the service for one page at a time. The quote comparison recomputes twenty landed costs inside a single frame. Gate evaluation for a visitor resolves inside a bounded budget and is cached per session, and the cache is dropped the moment an entitlement changes. A drop open serves a queue rather than collapsing. Carrier tracking is ingested away from the request that a buyer is waiting on.

**Assets.** Nothing binary ships. The wordmark is drawn geometry, the mascot is drawn from layered vector shapes, product photography is generated procedurally from a seed derived from the product's slug so the same product always renders the same image, panel and editorial imagery are seeded gradient fields with grain, and partner and backer marks are set as text wordmarks. The two type families are requested by name with a local fallback stack behind them, and no font file is committed.

**Health and logging.** `GET /api/health` returns `200` once the app is ready. One structured line is written per request carrying the route, the outcome and the acting workspace, and no personal data, supplier price or secret appears in any of them.

**Security.** State-changing requests are protected against cross-site forgery and no state changes on a read. Session cookies are http-only and same-site. Uploaded artwork is validated for type and size on the server, stored outside anything the web server will serve directly, delivered through short-lived signed links, and stripped of its metadata. Order creation carries a velocity limit per buyer and per credential, and a suspicious order can be held, which pauses its fulfillment without cancelling it. No secret is ever returned by any read path.

## Data model

Thirty-eight tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`workspace`**: `id`, `name` unique, `slug`, `return_policy` in `refund_on_inspection` and `refund_on_authorisation`, `created_at`. Seeded as `Tidewater Goods` and `Copperline Club`.

**`account`**: `id`, `email` unique and lowercased, `display_name`, `password_hash`, `created_at`.

**`membership`**: `id`, `workspace_id`, `account_id`, `role` in `owner`, `operator`, `finance` and `viewer`. One row per account per workspace. The acting role is read from here and from nowhere else.

**`product`**: `id`, `slug` unique, `title`, `category` in `apparel`, `outerwear`, `headwear` and `accessories`, `from_price_minor`, `minimum_quantity`, `customs_code` nullable, `country_of_origin`, `taxability_category`. The eight seeded rows carry the titles, prices and minimums listed in Core features.

**`sku`**: `id`, `code` unique, `product_id`, `size`, `colourway`. `KJ-WORK-M` is the `Washed Work Jacket` in medium. `CT-NAT-OS` is the `Canvas Tote` in one size, and its product carries no `customs_code`.

**`location`**: `id`, `code` unique, `name`, `country`. Seeded as `rotterdam` and `newark`.

**`project`**: `id`, `workspace_id`, `product_id`, `state` in `brief`, `sourcing`, `sampling`, `production`, `inventory`, `selling` and `closed`, `owner_id`, `created_at`. State moves forward only and every move is recorded.

**`brief`**: `id`, `project_id`, `quantity`, `colourways`, `size_curve`, `materials`, `weight_grams`, `packaging`, `target_landed_minor`, `needed_by`.

**`placement`**: `id`, `brief_id`, `position`, `method` in `screen_print`, `embroidery`, `patch` and `wash`, `artwork_id` nullable, `printed_width_mm`, `safe_area_ok`.

**`artwork`**: `id`, `brief_id`, `pixel_width`, `pixel_height`, `colour_count`, `stitch_estimate` nullable, `bleed_mm`, `state` in `pending`, `passed` and `refused`, `refusal_reason` nullable.

**`supplier`** and **`supplier_capability`**: the supplier carries `id`, `slug` unique, `name`, `country`, `currency`, `unit_basis` in `piece` and `dozen`, `incoterm`, and contact fields readable only by Owner, Operator and Finance. The capability carries `supplier_id`, `method`, `material`, `minimum_quantity`, `certification`, `weekly_throughput`. Five suppliers are seeded, including `aveiro-knitworks` and `tirupur-mills`.

**`quote_request`**: `id`, `brief_id`, `supplier_id`, `state` in `sent`, `replied`, `declined` and `reminded`, `sent_at`.

**`offer`**: `id`, `quote_request_id`, `currency`, `incoterm`, `unit_basis`, `unit_price_minor`, `setup_minor`, `lead_days`, `minimum_quantity`, `valid_until`, `state` in `open`, `accepted`, `expired` and `withdrawn`. An offer is immutable once made; expiry is a state it moves into.

**`price_break`**: `id`, `offer_id`, `quantity_threshold`, `unit_price_minor`.

**`landed_cost`**: `id`, `offer_id`, `quantity`, `unit_minor`, `setup_per_unit_minor`, `freight_per_unit_minor`, `duty_per_unit_minor`, `insurance_per_unit_minor`, `total_per_unit_minor`, `rate`, `rate_date`. Every component is stored, because the working is shown and a refund of an assumption is impossible.

**`sample_round`**: `id`, `project_id`, `round_number`, `requested`, `received_at`, `decision` in `accept`, `rework` and `reject`, `decided_by`, `decided_at`. Decisions are append-only.

**`sample_evidence`**: `id`, `sample_round_id`, `angle`, `generated_key`, `measurement_json`.

**`defect`**: `id`, `sample_round_id` nullable, `inspection_id` nullable, `severity` in `critical`, `major` and `minor`, `location`, `note`.

**`acceptance_rule`**: `id`, `project_id`, `sample_size`, `max_critical`, `max_major`, `max_minor`. Seeded at `80`, `0`, `2` and `5`.

**`run`** and **`lot`**: the run carries `id`, `project_id`, `offer_id`, `stage`, `deposit_percent`, `payment_terms`, `projected_ready_on`. The lot carries `id`, `run_id`, `supplier_id`, `units`, `landed_cost_minor`, `quality_state`. Lot identity is preserved through quality and inventory, and two lots of `KJ-WORK-M` are seeded at `5144` and `6010`.

**`inventory_event`**: `id`, `sku_id`, `location_id`, `kind`, `units`, `reference`, `at`. Append-only. `on_hand` and `available` are derived from this table and stored nowhere.

**`reservation`** and **`allocation`**: `id`, `order_line_id`, `sku_id`, `location_id`, `units`, `expires_at`, `state`. A reservation is never negative and a race resolves to one.

**`transfer`**: `id`, `sku_id`, `from_location_id`, `to_location_id`, `units`, `state` in `departed` and `received`, `departed_at`, `received_at`. Units belong to neither location while the state is `departed`.

**`storefront`**, **`listing`** and **`gate_rule`**: the listing carries `id`, `workspace_id`, `sku_id`, `slug`, `public_price_minor`, `gated_price_minor` nullable. The gate rule carries `id`, `listing_id`, `audience_expression`, `scope` in `listing` and `price`. The expression composes address allowlists, collection ownership, minimum balance, purchase history and codes with `and`, `or` and `not`, and it is evaluated at render and again at the order.

**`entitlement`**: `id`, `account_id`, `kind` in `collection`, `allowlist`, `history` and `code`, `reference`, `granted_reason`, `state` in `held`, `transferred` and `redeemed`. Standing is computed from these rows at read time; no membership flag is stored.

**`order`** and **`order_line`**: the order carries `id`, `reference` unique in the form `KLN-` and six digits, `workspace_id`, `buyer_account_id` nullable, `buyer_email`, `channel` in `storefront`, `agent`, `drop` and `redemption`, `currency`, `subtotal_minor`, `shipping_minor`, `tax_minor`, `duty_minor`, `total_minor`, `rail` in `fiat` and `token`, `state`, `access_token_hash`, `return_policy_at_order`, `killbill_external_key` nullable, `placed_at`. The line carries `id`, `order_id`, `listing_id`, `sku_id`, `units`, `unit_price_minor`, `taxable_base_minor`, `tax_allocation_minor`, `lot_id` nullable. The order total equals the sum of its line totals plus shipping plus tax plus duty at every moment after the order exists.

**`payment`**, **`capture`** and **`refund`**: `id`, `order_id`, `rail`, `idempotency_key` nullable, `chain_reference` nullable, `confirmations`, `amount_minor`, `state`. One capture exists per idempotency key, and the sum of an order's refunds never exceeds its captured amount.

**`money_ledger`**: `id`, `kind` in `settlement`, `refund`, `reversal`, `presale_held`, `payout` and `fee`, `order_id` nullable, `amount_minor`, `currency`, `source`, `at`. Append-only, and every finance figure is a sum of it.

**`tax_rate`** and **`nexus_threshold`**: the rate carries `jurisdiction`, `category`, `rate`, `effective_from`, `rounding` in `per_line` and `per_invoice`. Seeded as `NL` at `0.21` per invoice, `GB` at `0.20` per invoice and `US-CA` at `0.085` per line. The threshold carries `jurisdiction`, `amount_minor` seeded at `10000000`, and `window` of one calendar year.

**`customs_profile`**: `id`, `product_id`, `classification`, `origin`, `value_basis`. A product with no row here cannot be dispatched across a border.

**`shipment`**, **`parcel`** and **`tracking_event`**: the parcel carries its dimensions, its weight and its label; the tracking event carries `carrier`, `external_id`, `status`, `at`, and the same `external_id` arriving twice records once.

**`return_request`** and **`inspection`**: the request carries `reference`, `order_id`, `reason_code`, `window_closes_at`, `state`; the inspection carries `condition_grade` and `disposition` in `restock`, `refurbish` and `write_off`. The refund and the inventory event both issue from the inspection row.

**`promise`** and **`promise_revision`**: the promise carries `id`, `order_id`, `window_opens_on`, `window_closes_on`, `owner_stage`, `inputs_json`, `made_at`. The revision carries `promise_id`, `window_opens_on`, `window_closes_on`, `cause`, `notified_at`. Every revision records its cause, and a window that changes with no revision row is a defect.

**`drop`**, **`gacha_outcome`** and **`pull`**: the drop carries `slug`, `opens_at`, `supply`, `allowance_per_buyer`, `seed_commitment`, `seed_revealed` nullable, `gate_rule_id` nullable. The outcome carries `drop_id`, `name`, `odds`, `sku_id`, `remaining`. The pull carries `drop_id`, `buyer_account_id`, `outcome_id`, `nonce`, `at`, and is verifiable against the revealed seed.

**`presale`**, **`backer`** and **`payout`**: the presale carries `threshold_minor`, `deadline`, `state`; the backer carries `account_id`, `amount_minor`, `share`; the payout carries its period, its amount and its ledger row.

**`agent_credential`**: `id`, `workspace_id`, `owner_account_id`, `scopes`, `spend_limit_minor`, `rate_limit_per_minute`, `state` in `active` and `revoked`. Revoking one releases its open reservations.

**`procedure_version`**, **`support_conversation`** and **`support_answer`**: the answer records the `procedure_version_id` it cited, or that it escalated. Three versions of the returns procedure are seeded.

**`announcement`**, **`subscriber`** and **`send_record`**: the subscriber carries `email`, `consented_at`, `suppressed_at` nullable; the send record carries one row per recipient per announcement.

**`page_view`**: `id`, `route`, `at`, readable by an Owner.

**Schema evolution.** Catalogue shapes, tax rate tables, customs classification sets and gate-rule grammars each carry a version, and every stored order, quote and promise records the version it was written under. A historical record is read through its own version: a tax rate change, a duty reclassification or a gate-grammar extension leaves an existing order, quote or promise reading exactly as it read when it was written. Rewriting history to match today's rules is a defect.

**Seed data.** Two workspaces, eight accounts with their memberships, eight products, twelve stock keeping units, five suppliers with their capabilities, two locations, one project already at `sourcing` with five offers of which one is expired, one accepted sample round and one blocked batch inspection, one run with two lots, an inventory ledger leaving exactly one unit of `KJ-WORK-M` available at `newark` and none at `rotterdam`, one in-flight transfer of `6` units of `KJ-WORK-M` from `rotterdam` to `newark`, one storefront with the gated `holder-work-jacket` listing, one entitlement held by `buyer@example.com` against the `kilnfolk-genesis` collection, one scheduled drop `kilnfolk-winter` with its three published odds and its seed commitment, one pre-sale, three procedure versions, one open support conversation, one consented subscriber and one suppressed one, and the order `KLN-000412` already placed and delivered so its return path can be walked.

Seeding must be idempotent: restarting the app must not duplicate rows.
## Front-end specification

This section carries the visual and copy detail the six judged sections have no room for. Nothing here contradicts `## UI/UX notes`; it is the same product described closer in.

### Ground, rhythm and the container ladder

Content sits inside a ladder of fixed measures rather than a fluid width, and the ladder is the same one everywhere: ten steps rising from a narrow card measure to a wide page measure, each step a recognisable jump rather than a smooth stretch. Every surface picks a rung and holds it, so two panels of the same kind are the same width on every route.

The landing page is ruled by a faint blueprint grid over the paper ground. The site alternates paper and deep ink panels down the page, and that alternation is the structural rhythm; no other device is allowed to mark a section boundary.

The layout changes at one dominant breakpoint and at lighter steps above and below it, and the arrangement holds at every width in between. Pointer capability is asked about explicitly rather than assumed: where the device can hover, hover-revealed affordances stay hidden until pointed at; where it cannot, those affordances are pinned to their revealed state so nothing is unreachable. Reduced motion is honoured in four separate places: the physics simulation, the drifting panels, the twinkles and beams, and the marquees.

Stacking is a closed ladder and nothing is introduced outside it: ambient backdrops sit behind the page, content sits on it, raised chrome sits above content, the header pill and any sticky bar sit above that, and modals and toasts sit above everything. A new surface takes an existing rung.

### Palette, by role

- **Ground**: a warm near-white, nearer paper than white. It is the page.
- **Secondary paper**: a second warm near-white, very slightly cooler, for inset bands that need to read as a different sheet without a border.
- **Ink**: a near-black cool neutral. Every piece of text, and the shadow colour at low opacity.
- **Signal**: a light, vivid red-orange. Primary buttons, accents and live dots wear it, and nothing decorative does.
- **Signal tint**: a slightly lighter, softer version of the same hue, for gradients and glows only.
- **Deep panel**: a near-black cool neutral, one step warmer than the ink, for the dark bands and the storefront mock.
- **Raised dark surface**: a deep cool neutral that sits on the deep panel.
- **Card**: a plain near-white with no warmth in it, so a card reads as a separate object on the paper ground without needing a shadow.
- **Inset panel**: a neutral near-white, a shade off the card, for panels set into a card.
- **Ink alphas**: a four-step ladder of the ink at low opacities carries hairlines, dividers, secondary text and the card shadow. Four steps, no more, and each has one job.
- **Meaning**: an emerald for live and success, an amber for pending, a red for destructive. Each appears only in that role.

Two gradients exist and no third: a flat one between two stops of the paper colour, which lets a band cross-fade its ground, and an accent one between two stops of the signal.

Vendor and partner colours are those companies' own and are never treated as brand colours: partner marks are set as greyscale text wordmarks.

### Type

`Inter` is the interface family across its whole weight range. `Baloo 2` is the display family and sets the wordmark and the display headlines only. The scale is the one given in `## UI/UX notes`; the two workhorse sizes are body at 16px in regular and in medium, and dense interface text at 14px. Micro labels on chips and tags sit at 11px and 10px and never grow at any width.

### Iconography and the marks

- The wordmark is drawn geometry, not a font glyph: four closed letterform paths on one wide, short box, each a soft rounded character with swelling strokes. It carries a text label beside it for assistive technology in every header and footer.
- The mascot is a small goldfish character wearing sunglasses, built from layered vector shapes in the signal colour, floating at the upper right of the landing hero. It appears once per page at most.
- Interface icons are a thin stroke set on one square box, inheriting the colour of the text beside them. Four are drawn geometry and are pinned: a menu of three horizontal bars; a chevron pointing down, which rotates a half turn when its disclosure opens; an arrow pointing up and to the right, which shifts a hair right and up when its parent is pointed at; and a play triangle with rounded corners, offset a hair to the right for optical centring rather than mathematical centring.
- The rest of the set follows the same construction: a check inside a circle for order states, a headset for support, an envelope for marketing mail, a box for inventory, a magnifier for sourcing and a padlock for gated listings.
- Status marks are a live dot in emerald, a pending dot in amber and a destructive mark in red, and each is always paired with its word.

### Global chrome

**The intro reel.** A vertical reel of star glyphs beside a rotating status line, over two soft drifting colour blobs, one warm and one cool, with the wordmark rising into place. Each line fades up, holds, and fades out as the reel travels. It plays once per session and never blocks navigation. The twelve lines, exactly:

`Pondering manufacturers...` `Herding fulfillment partners...` `Schmoozing Stripe...` `Bamboozling customs...` `Wrangling storefront plugins...` `Cogitating on tax filings...` `Befriending ChatGPT...` `Whispering to spreadsheets...` `Untangling the ops stack...` `Bribing the QC agent...` `Coaxing the supply chain...` `Marinating the supply chain...`

**The header.** A floating white pill inset from the top, carrying a wide soft bloom. The wordmark sits at its left; two dropdown menus and a whitelist link sit at its centre; a contextual strip sits at its right. That strip begins as the line `Want to see Kilnly in action? Request a demo` with the last two words as the link, and becomes a solid signal-coloured `Book a demo` pill once the page has scrolled past the hero. The two menu labels are `Past drops` and `Kilnfolk`, and the third link reads `Whitelist`. Dropdown panels open by animating their height.

**The footer.** Four columns on ink, over the copyright line `(C) 2026 Kilnly`, with the legal entity line `Kilnly Labs Ltd` beneath it on the legal routes. The columns are: **Past drops**, carrying two campaign names and `Redeem`; **Resources**, carrying `Latest productions`, `No minimum order`, `Merch fulfillment`, `About us`, `Field notes`, `Brand kit` and `Legal`; **Community**, carrying `Telegram`, `Holders Hub`, `Support` and `Contact`; and **Social**, carrying `Twitter`, `LinkedIn`, `Instagram`, `GitHub`, `Product Hunt` and `Crunchbase`. Column heads are small and uppercase, and links lift when pointed at.

**Hover and pointer.** Text links and the wordmark fall to about two thirds of their strength when pointed at. The up-and-right arrow inside a pointed-at group shifts a hair right and up without its parent moving. Affordances that hover reveals, such as the arrow on a logo card or the read arrow on an article card, fade in from nothing. Chevrons rotate a half turn on disclosure. Cards take the card lift with a colour change slightly slower than the lift itself. Every one of these has a focus-visible twin showing the same change, and on a coarse pointer the revealed state is pinned rather than unreachable.

**Shared furniture.** Buttons come in three: a signal-coloured primary pill, an ink secondary pill, and a ghost with a hairline border. Each has the five states. Accordions animate their height. Category chips are fully round buttons that fill with ink when selected. Marquee rows run horizontally for logo rows and vertically for testimonial columns, each travelling a full track plus one gap before repeating.

### Motion, as named moments

The easing vocabulary is small and shared. Entrances settle. Word and card reveals settle a little faster. The default interface transition is the quickest thing in the product. Decelerating entrances arrive after a short delay. Long ambient loops ease evenly at both ends. Chips overshoot slightly and come back. Accelerating exits leave faster than they arrived rather than easing out. Nothing outside that vocabulary is introduced.

Each of these is a moment with a name, and all of them share the product's one character.

- **Hero fade-up**: content rises a short distance while it fades in.
- **Word-by-word reveal**: a display headline arrives one word at a time, each behind the one before.
- **Illustration float**: the mascot bobs gently up and down, holding its rotation.
- **Endorsement gradient float**: the background gradient under the supported-by band travels through four stations so the band appears to breathe.
- **Pill edge glow**: a white inner rim swells and subsides on the header pill and on live chips.
- **Ken burns**: a photographic panel scales up very slightly and rises a fraction over a long, slow loop.
- **Twinkle and beam**: dots flicker on staggered loops and horizontal beams of light drift across dark panels.
- **Shimmer**: a highlight sweeps across a track, used on loading skeletons and once across the wordmark.
- **Marquee**: logo rows and testimonial columns travel a full track plus a gap, continuously.
- **Accordion**: a disclosure animates its own height open and closed.

Scroll reveals have two states and play once per band. There is no scroll-scrubbed timeline, and none is to be introduced. Under reduced motion there is no physics, no drift, no twinkle, no ken burns and no marquee.

### The landing page, band by band

1. The intro reel, then the header pill.
2. The hero: a `Backed by` chip, the headline `Create your dream merch on autopilot` with `on autopilot` set inside a dark rounded plate, the standfirst `Ditch the maze of tools, vendors and middlemen.` and `Go from prompt to physical product in 5 minutes.`, and the mascot at the upper right. The pill pile sits beneath.
3. The supported-by band: partner wordmarks in a marquee under a short line.
4. Positioning: `Grow your brand, not your ops.` with the paragraph `Try the first AI commerce platform that replaces the manual maze of tools, vendors, and middlemen.` and `Book a demo to automate your storefront, supply chain, and everything in between.`
5. Four capability panels, each a headline, a line and a working mock: `Find your ideal suppliers.` with `Kilnly agents reach out to global manufacturers and return with the best quotes for your brief.`; `Check samples & batches super fast.` with `No int'l shipping downtime. Kilnly QC's your products locally.`; `Ship globally without headaches.` with `Pick & pack + sales tax support wherever you sell.`, illustrated by an order card moving from received to contacting the warehouse; and `Launch a new store that converts every visitor.` with `Gate products, calibrate price, and offer perks in real time to win over every human or agent.`, illustrated by a dark storefront mock showing a recognised high-value wallet being offered a jacket.
6. The extras grid, headed `Oh yeah, and all this too.`, carrying chips `Live · $1M GMV` and `Coming soon` and eight cards: `Create Gachas` with `Your own interactive blind box drops.`; `Launch Pre-sales` with `Pre-sell products w/ rev share for backers.`; `Forecast inventory` with `Avoid stockouts or dead stock.`; `AI + human support` with `Handled according to your SOPs.`; `Send mkt emails` with `Beautiful announcement emails in-house.`; `Sell to AI agents` with `Discoverable to agents & x402-ready checkout.`; `Accept fiat & crypto` with `Cards, SPL tokens. One native checkout.`; and `Tracking on every order` with `Live status updates across every channel.`
7. The closing band and the footer.

### The pill pile

Thirteen pills, each naming one chore, exactly: `emailing 12 manufacturers`, `fiat checkout`, `three fulfillment partners`, `two warehouses on different continents`, `a storefront + 5 plugins`, `accept crypto`, `a tax filing service per region`, `agent discoverability`, `email updates & promos`, `a support team in Manila`, `a sampling and QC agent`, `an inventory spreadsheet`, `a workspace of SOPs`.

### The catalogue page

Headed `Latest productions`, with the standfirst `Pieces Kilnly has sourced, sampled and shipped for real brands. Every product here went from a brief to a finished run. See something close to what you want, and we'll make yours.` The chips read `All`, `Apparel`, `Outerwear`, `Headwear` and `Accessories`, and every card's action reads `Start a project`.

### The fulfillment page

Headed `Merch fulfillment, end to end.` over the paragraph about brands stitching fulfillment together from a third-party logistics provider, a customs broker, a tax filer and whoever picked up the phone, against one chain run as a whole. Its thesis is `Nobody owns the delivery date.` The two figures read `11 Ops surfaces we run` and `1 Minimum order`.

The six subjects, each a heading and a paragraph:

- **Warehousing.** Where finished goods sit decides shipping times and margin, so it is decided with the run rather than after it.
- **3PL distribution.** Picking, packing and carrier handoff, one surface out of eleven.
- **Customs and duties.** A border has paperwork and a bill, and a wrong classification parks a shipment in a bonded warehouse accruing storage fees.
- **Sales tax.** Selling into a jurisdiction can create an obligation to collect and file, and it is the one that becomes a letter eighteen months later.
- **Returns.** A second fulfillment run in reverse: receive, inspect, restock or write off.
- **Quality control, before any of it.** Checked at the factory on samples and again on the run, because a bad batch caught at the factory costs a re-run and caught in your warehouse costs the season.

The four accordion questions read `What is merch fulfillment?`, `Do you handle fulfillment for merch you didn't manufacture?`, `How much does fulfillment cost?` and `What happens if a batch is wrong?`. The closing band reads `One chain, one place to watch it.` over `One call is enough to know if we can make it, what it costs, and how fast.`, with `Book Demo` and `Drop your email and we'll get you on the calendar.`

### Field notes and about

The field-notes index cards carry a category from `Supply chain`, `Commerce` and `Industry`, a title, a standfirst, an author and a read time. Article bodies ship as seeded placeholder copy inside the reading shell. The about page carries the company position and the team on the paper ground with drifting panels.

### The not-found screen

The measured line `Page not found` on the paper ground, with one control back to the landing page.

### Console surfaces

The console shares the token layer and adds no colour, no new corner softness, no new spacing step and no new type step. Its shell is navigation down the left, work in the middle, and a detail pane beside it on the comparison surfaces. The quote comparison is readable as a table and not only as a chart, its tables are navigable with the arrow keys, and every approval control is reachable from the keyboard with a visible focus ring. The storefront mock on the landing page and the real storefront are the same components on the same tokens.

### Zero-asset substitution

Nothing binary ships and every one of these is generated instead.

| Class | What it replaces | Substitute |
|---|---|---|
| mascot | the goldfish character render | a drawn vector character in layered shapes |
| product photography | catalogue garment shots | seeded procedural flat-lays, a garment silhouette in its colourway on the paper ground under a soft shadow, labelled with the product name |
| panel and editorial imagery | landing and blog photography | seeded gradient fields in the palette with grain, each carrying its caption, drifting on the ken-burns loop |
| partner, backer and vendor marks | logo images | greyscale text wordmarks in the interface family |
| storefront and order mocks | interface screenshots | the product's own components on the seeded fixtures |
| display font | the bespoke rounded face | a rounded geometric display face of matching proportion, recorded as a substitution |

The blueprint grid, the twinkle dots and the light beams are drawn. The same generator feeds both the catalogue images and the storefront mocks, so one product always looks like itself.

## Constraints

- One workspace's projects, briefs, quotes, costs, suppliers, inventory, orders and buyer data are unreachable from another, including through search, exports, the agent channel and any webhook. A cross-workspace read answers not found rather than denied, so existence does not leak.
- Supplier contacts, quoted prices and terms never appear in a storefront payload, an agent payload, a buyer-facing page or a buyer-reachable export.
- No real factory, carrier, customs authority, tax authority, chain node, wallet provider or card network is contacted. Each is modelled inside the product against seeded data and operator actions.
- The app's server makes no call to any host outside this environment at run time.
- No second datastore, cache, queue, object store, identity provider or mail vendor.
- No downloaded image, video or font binary is committed or fetched at build time.
- No native application, no browser extension, no desktop client.
- No comments, no likes, no follower graph, no direct messaging between buyers.
- No card primary account number, wallet private key or supplier bank detail is stored anywhere, ever.
- The product stays responsive with ten thousand inventory rows, ten thousand orders and twenty offers under comparison.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/sign-up` | `display_name`, `email`, `password` | the account with `access_token` |
| `POST /api/auth/sign-in` | `email`, `password` | the account with `access_token` |
| `POST /api/auth/sign-out` | bearer token | an empty acknowledgement |
| `GET /api/health` | none | `{"status": "ok"}` |
| `GET /api/products` | optional `category` | a top-level JSON array of products with `slug`, `title`, `category`, `from_price_minor`, `minimum_quantity` |
| `GET /api/projects` | bearer token | a top-level JSON array of the caller's workspace projects with `state` and `next_action` |
| `POST /api/projects` | `product_slug` | the project with its empty brief |
| `PUT /api/projects/{id}/brief` | the brief fields | the stored brief |
| `POST /api/projects/{id}/artwork` | the artwork description and its placement | the artwork with `state` and, when refused, `refusal_reason` naming the measurement |
| `POST /api/projects/{id}/quote-requests` | none | a top-level JSON array of the requests created |
| `GET /api/projects/{id}/offers` | optional `quantity` | a top-level JSON array of offers, each with its `landed_cost` object carrying `unit_minor`, `setup_per_unit_minor`, `freight_per_unit_minor`, `duty_per_unit_minor`, `insurance_per_unit_minor`, `total_per_unit_minor`, `rate` and `rate_date`, ordered by `total_per_unit_minor` |
| `POST /api/offers/{id}/accept` | none | the run created, or a refusal when the offer is `expired` |
| `POST /api/projects/{id}/sample-rounds` | the round, its evidence and its defects | the round with its `decision` |
| `POST /api/runs/{id}/inspection` | `sample_size` and the defects found | the inspection with `blocked` and the decision raised |
| `GET /api/inventory` | optional `sku`, optional `location` | a top-level JSON array of `{sku, location, on_hand, available}` summed from the ledger |
| `POST /api/transfers` | `sku`, `from`, `to`, `units` | the transfer in state `departed` |
| `GET /api/shop` | none | a top-level JSON array of listings visible to the caller, with the price the caller is entitled to |
| `POST /api/entitlements/challenge` | `address` | a `nonce` and its expiry |
| `POST /api/entitlements/prove` | `address`, `nonce`, `signature` | the entitlements now proven for the session |
| `POST /api/cart` | `listing_slug`, `units` | the cart with every line re-evaluated and any ineligible line marked |
| `POST /api/orders` | the cart, `buyer_email`, `destination`, `rail`, header `Idempotency-Key` | the order with `reference`, `total_minor`, `tax_minor`, `promise` and `access_token` |
| `GET /api/orders/{reference}` | `access_token` or the owning buyer | the order, its timeline, its promise and its revisions |
| `POST /api/orders/{reference}/transitions` | `to` | the order at its new state, or a refusal for a backward move |
| `POST /api/orders/{reference}/dispatch` | none | the shipment, or a refusal naming the missing customs classification |
| `POST /api/orders/{reference}/returns` | `reason_code` | the return authorisation and its reference |
| `POST /api/returns/{reference}/inspection` | `condition_grade`, `disposition` | the refund and the inventory event issued together |
| `POST /api/promises/{order_reference}/recompute` | the moved inputs | one revision carrying its cause |
| `GET /api/drops/{slug}` | none | the drop, its published odds, its `seed_commitment`, its remaining supply and the caller's queue position |
| `POST /api/drops/{slug}/pull` | header `Idempotency-Key` | the pull with its outcome and its nonce, or a refusal naming the allowance |
| `POST /api/redemptions` | `entitlement_id` | the order created, the reservation taken and the entitlement marked, together |
| `GET /api/agent/catalogue` | agent credential | the machine-readable catalogue under the same gating |
| `POST /api/agent/orders` | agent credential, the same body as `POST /api/orders` | the same order shape a buyer receives |
| `GET /api/reports/{axis}` | `period` and `axis` in `product`, `channel`, `lane`, `jurisdiction` | the totals for that period on that axis |
| `GET /api/support/conversations` | bearer token | the queue with order context |
| `POST /api/support/conversations/{id}/answers` | the draft | the answer with its `procedure_version_id`, or its escalation |
| `POST /api/announcements/{id}/send` | none | the send records created, suppressed addresses excluded |
| `POST /api/subscribers/unsubscribe` | `email` | an acknowledgement, effective immediately |

List endpoints return a top-level JSON array. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success. Bearer auth is required on everything except sign-in, sign-up, health, the public marketing routes, the ungated storefront reads and the webhook receivers, which authenticate by signature rather than by a user token.

### No mocks

The projects, briefs, offers, landed costs, sample rounds, runs, lots, inventory events, reservations, orders, promises, drops, pulls, entitlements, returns and ledgers live in PostgreSQL and nowhere else. The invoice for a settled fiat order lives in `killbill`. The confirmation, the delivery update, the return authorisation and the announcement live in the mail server, reached over SMTP.

An in-memory array of orders, a stock count held in a module variable or a column that is written rather than summed, a hardcoded invoice object the app returns to itself, a JSON file of products on the app's own disk, a mail body written to a log instead of sent, a gacha outcome drawn when the buyer pulls rather than from the committed seed, a gated listing hidden in the interface but served by the API, a membership flag written once at signup, a cost of goods averaged across lots, or a delivery window recomputed with nobody told are each contract violations however good the interface looks. The named provider is the fact: the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A founder can brief a product, read one comparable landed cost per unit for replies that arrived in different currencies and unit bases, accept an offer and follow the run into two warehouses. A buyer can prove an entitlement, watch the gated price appear in place, check out on either rail, and land on an order whose invoice exists in the billing platform for its own total and whose confirmation reached that address alone. Two buyers reaching for the last unit at the same instant produce one order and one refusal, and stock never goes negative. When the factory, the carrier and the border all move against one order, that order carries one new delivery window, one recorded cause and one message to its buyer.
