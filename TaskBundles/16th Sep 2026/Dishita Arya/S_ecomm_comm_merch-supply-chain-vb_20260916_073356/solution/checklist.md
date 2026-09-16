# Checklist: Kilnly

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 449
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves a public marketing site for an end to end merchandise service. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The product serves an operations console behind sign-in. `src: Overview para 1`
- [ ] `C-OV-03` `constraint` One origin carries the marketing site alongside the console. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The console turns a brief into factory quotes. `src: Overview para 1`
- [ ] `C-OV-05` `capability` Finished goods land in two warehouses on different continents. `src: Overview para 1`
- [ ] `C-OV-06` `capability` A gated storefront sells finished goods in fiat or in tokens. `src: Overview para 1`
- [ ] `C-OV-07` `capability` The product owns one delivery date per order. `src: Overview para 3`
- [ ] `C-OV-08` `constraint` The product carries no comments feature. `src: Overview para 4`
- [ ] `C-OV-09` `constraint` The product carries no follower graph. `src: Overview para 4`
- [ ] `C-OV-10` `constraint` No downloaded image, video or font binary ships. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A Visitor reads every marketing route without signing in. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A Visitor places an order as a guest. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A Visitor cannot read any project inside a workspace. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A Visitor cannot read a gated listing without proving the entitlement. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A Buyer reads their own orders. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A Buyer cannot read another buyer's order. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A Viewer reads every project inside their own workspace. `src: User roles table row 3`
- [ ] `C-RL-08` `role` A Viewer cannot approve a sample round. `src: User roles table row 3`
- [ ] `C-RL-09` `role` A Viewer cannot accept an offer. `src: User roles table row 3`
- [ ] `C-RL-10` `role` An Operator writes briefs. `src: User roles table row 4`
- [ ] `C-RL-11` `role` An Operator cannot change a member's role. `src: User roles table row 4`
- [ ] `C-RL-12` `role` An Operator cannot issue an agent credential. `src: User roles table row 4`
- [ ] `C-RL-13` `role` A Finance member reads the money ledger. `src: User roles table row 5`
- [ ] `C-RL-14` `role` A Finance member cannot move a run stage. `src: User roles table row 5`
- [ ] `C-RL-15` `role` An Owner changes member roles inside their own workspace. `src: User roles table row 6`
- [ ] `C-RL-16` `role` An Owner cannot reach another workspace's projects. `src: User roles table row 6`
- [ ] `C-RL-17` `constraint` The acting role is read from the membership row rather than from a request body. `src: User roles para 1`
- [ ] `C-RL-18` `constraint` The server rejects a Viewer session calling an Operator-only endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-19` `constraint` A rejected authorization leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-20` `capability` Signup is open to anyone. `src: User roles, signup paragraph`
- [ ] `C-RL-21` `constraint` An account with no membership row reaches no workspace route. `src: User roles, signup paragraph`
- [ ] `C-RL-22` `constraint` Signup grants a buyer no entitlement. `src: User roles, signup paragraph`
- [ ] `C-RL-23` `literal` The seeded Owner of Tidewater Goods is `owner@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-24` `literal` The seeded Operator is `operator@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-25` `literal` The seeded Finance member is `finance@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-26` `literal` The seeded Viewer is `viewer@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-27` `literal` The seeded Owner of Copperline Club is `owner2@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-28` `literal` The seeded entitled buyer is `buyer@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-29` `literal` The seeded unentitled buyer is `buyer2@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-30` `literal` The seeded third buyer is `buyer3@example.com`. `src: User roles, seeded accounts paragraph`
- [ ] `C-RL-31` `literal` The two seeded workspaces are `Tidewater Goods`, `Copperline Club`. `src: User roles, seeded accounts paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` Email with password is exchanged for a bearer token. `src: Core features, Auth`
- [ ] `C-CF-02` `literal` The sign-in response carries the token in `access_token`. `src: Core features, Auth`
- [ ] `C-CF-03` `constraint` A password is stored under a memory-hard hash rather than in recoverable form. `src: Core features, Auth rule 1`
- [ ] `C-CF-04` `constraint` A wrong password refusal names neither field. `src: Core features, Auth rule 1`
- [ ] `C-CF-05` `constraint` A token replayed after sign-out is denied. `src: Core features, Auth rule 2`
- [ ] `C-CF-06` `constraint` A reset request answers identically for an unknown address. `src: Core features, Auth rule 4`
- [ ] `C-CF-07` `capability` Nine public marketing routes are served on the same origin as the console. `src: Core features, marketing site`
- [ ] `C-CF-08` `constraint` Marketing routes render from the product's own components rather than a static export. `src: Core features, marketing site`
- [ ] `C-CF-09` `ui` The intro reel plays once per session. `src: Core features, marketing site rule 1`
- [ ] `C-CF-10` `ui` The intro reel never blocks navigation to another route. `src: Core features, marketing site rule 2`
- [ ] `C-CF-11` `ui` The header is a floating pill carrying the wordmark, two dropdown menus, a whitelist link. `src: Core features, marketing site rule 3`
- [ ] `C-CF-12` `ui` The header's right strip becomes a solid `Book a demo` pill once the page scrolls past the hero. `src: Core features, marketing site rule 3`
- [ ] `C-CF-13` `ui` The footer carries four columns over the copyright line on every route. `src: Core features, marketing site rule 4`
- [ ] `C-CF-14` `ui` Each public route leads with one primary action distinct from every secondary one. `src: Core features, marketing site rule 5`
- [ ] `C-CF-15` `ui` The hero carries a backer endorsement chip, the display headline, the two-line standfirst, the mascot. `src: Core features, landing rule 1`
- [ ] `C-CF-16` `ui` Thirteen pills fall, collide, come to rest in a heap. `src: Core features, landing rule 2`
- [ ] `C-CF-17` `ui` A pill can be thrown with the pointer. `src: Core features, landing rule 2`
- [ ] `C-CF-18` `ui` Pills stay readable at rest. `src: Core features, landing rule 2`
- [ ] `C-CF-19` `ui` No pill leaves its container. `src: Core features, landing rule 2`
- [ ] `C-CF-20` `ui` The pile settles rather than jittering indefinitely. `src: Core features, landing rule 2`
- [ ] `C-CF-21` `ui` The pills' words are present as an ordinary list for assistive technology. `src: Core features, landing rule 3`
- [ ] `C-CF-22` `ui` Under a reduced-motion preference the simulation does not run. `src: Core features, landing rule 4`
- [ ] `C-CF-23` `ui` Under a reduced-motion preference the pills render in a designed static arrangement. `src: Core features, landing rule 4`
- [ ] `C-CF-24` `ui` The simulation stops stepping once off screen. `src: Core features, landing rule 5`
- [ ] `C-CF-25` `ui` The simulation is torn down on navigation. `src: Core features, landing rule 5`
- [ ] `C-CF-26` `ui` Four capability panels each carry a headline, a line of copy, a working product mock. `src: Core features, landing rule 6`
- [ ] `C-CF-27` `ui` The extras grid carries eight cards, each with a status chip. `src: Core features, landing rule 7`
- [ ] `C-CF-28` `data` The catalogue lists eight products. `src: Core features, catalogue rule 1`
- [ ] `C-CF-29` `ui` A catalogue card carries a generated image, the title, a from-price, a minimum order quantity. `src: Core features, catalogue rule 1`
- [ ] `C-CF-30` `literal` `Acid-Wash Patch Tee` starts at `3400` minor units with a minimum of `100`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-31` `literal` `Embroidered Logo Tee` starts at `3000` minor units with a minimum of `100`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-32` `literal` `Acid-Wash Embroidered Hoodie` starts at `4800` minor units with a minimum of `50`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-33` `literal` `Embroidered Quarter-Zip` starts at `4800` minor units with a minimum of `50`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-34` `literal` `Embroidered Dad Cap` starts at `1900` minor units with a minimum of `100`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-35` `literal` `Washed Work Jacket` starts at `6800` minor units with a minimum of `50`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-36` `literal` `Canvas Duffel Bag` starts at `4200` minor units with a minimum of `50`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-37` `literal` `Canvas Tote` starts at `2200` minor units with a minimum of `100`. `src: Core features, catalogue rule 2`
- [ ] `C-CF-38` `literal` The five category chips read `All`, `Apparel`, `Outerwear`, `Headwear`, `Accessories`. `src: Core features, catalogue rule 3`
- [ ] `C-CF-39` `capability` The active catalogue filter is carried in the address. `src: Core features, catalogue rule 3`
- [ ] `C-CF-40` `ui` The catalogue keeps the price beside the minimum on the card at every width. `src: Core features, catalogue rule 4`
- [ ] `C-CF-41` `capability` `Start a project` opens a brief with that product already chosen. `src: Core features, catalogue rule 5`
- [ ] `C-CF-42` `constraint` A marketing price is read from the catalogue the quoting engine reads. `src: Core features, catalogue rule 6`
- [ ] `C-CF-43` `literal` The fulfillment page carries the line `Nobody owns the delivery date.` `src: Core features, fulfillment rule 2`
- [ ] `C-CF-44` `literal` The fulfillment page carries the figure `11` for operations surfaces run. `src: Core features, fulfillment rule 3`
- [ ] `C-CF-45` `literal` The fulfillment page carries the figure `1` for the minimum order. `src: Core features, fulfillment rule 3`
- [ ] `C-CF-46` `ui` Six subject sections follow, each a heading above a paragraph. `src: Core features, fulfillment rule 4`
- [ ] `C-CF-47` `ui` Four questions follow in an accordion. `src: Core features, fulfillment rule 5`
- [ ] `C-CF-48` `ui` The fulfillment page closes on a band naming one chain above one place to watch. `src: Core features, fulfillment rule 5`
- [ ] `C-CF-49` `capability` The no-minimum route offers a path into a brief. `src: Core features, no-minimum rule 1`
- [ ] `C-CF-50` `capability` The quoting engine prices a single unit as honestly as a thousand. `src: Core features, no-minimum rule 1`
- [ ] `C-CF-51` `ui` The about route carries the company position on the paper ground with drifting panels. `src: Core features, about rule 2`
- [ ] `C-CF-52` `literal` The field-note categories are `Supply chain`, `Commerce`, `Industry`. `src: Core features, field notes rule 3`
- [ ] `C-CF-53` `constraint` Brand kit swatches are generated from the same token source the site reads. `src: Core features, brand kit rule 4`
- [ ] `C-CF-54` `literal` The terms document is served at `/legal/website-terms-of-use`. `src: Core features, legal rule 1`
- [ ] `C-CF-55` `capability` The terms route is reachable from the footer of every page. `src: Core features, legal rule 1`
- [ ] `C-CF-56` `capability` The terms route is linked from the signup form. `src: Core features, legal rule 1`
- [ ] `C-CF-57` `literal` The privacy statement is served at `/legal/privacy`. `src: Core features, legal rule 2`
- [ ] `C-CF-58` `capability` The privacy route states what the product records about a buyer. `src: Core features, legal rule 2`
- [ ] `C-CF-59` `literal` An unknown address renders the product's own screen carrying `Page not found`. `src: Core features, not-found rule 3`
- [ ] `C-CF-60` `contract` An unknown address answers as not found rather than as a success. `src: Core features, not-found rule 3`
- [ ] `C-CF-61` `constraint` Every internal link on every public route resolves. `src: Core features, links rule 4`
- [ ] `C-CF-62` `literal` `/sitemap.xml` lists every public route. `src: Core features, machine routes rule 5`
- [ ] `C-CF-63` `literal` `/robots.txt` names the sitemap. `src: Core features, machine routes rule 5`
- [ ] `C-CF-64` `constraint` No two public routes share a title. `src: Core features, head rule 6`
- [ ] `C-CF-65` `constraint` No two public routes share a description. `src: Core features, head rule 6`
- [ ] `C-CF-66` `capability` Every public route declares a social preview title with an image that resolves. `src: Core features, head rule 6`
- [ ] `C-CF-67` `capability` A member works inside one brand workspace holding projects. `src: Core features, console rule 1`
- [ ] `C-CF-68` `ui` The project list is a grid of cards, each carrying a state chip above the next action. `src: Core features, console rule 2`
- [ ] `C-CF-69` `constraint` Global search reaches nothing outside the caller's own workspace. `src: Core features, console rule 3`
- [ ] `C-CF-70` `ui` The notification centre carries promise revisions, stock refusals, quality decisions, support escalations, newest first. `src: Core features, console rule 4`
- [ ] `C-CF-71` `capability` Creating a project is its own route reachable by address. `src: Core features, console rule 5`
- [ ] `C-CF-72` `ui` Every console list carries a designed empty state naming its one next action. `src: Core features, console rule 6`
- [ ] `C-CF-73` `data` A brief records the base product, the quantity, the colourways, the size curve, the target landed price, the needed-by date. `src: Core features, brief rule 1`
- [ ] `C-CF-74` `literal` The four decoration methods are `screen_print`, `embroidery`, `patch`, `wash`. `src: Core features, brief rule 2`
- [ ] `C-CF-75` `literal` Artwork needs at least `150` pixels per inch at the printed size. `src: Core features, artwork rule 3`
- [ ] `C-CF-76` `literal` `screen_print` permits at most `6` spot colours. `src: Core features, artwork rule 3`
- [ ] `C-CF-77` `literal` `embroidery` permits at most `12` thread colours. `src: Core features, artwork rule 3`
- [ ] `C-CF-78` `literal` Artwork needs a bleed of at least `3` millimetres. `src: Core features, artwork rule 3`
- [ ] `C-CF-79` `capability` An artwork refusal names the offending measurement in the artwork's own terms. `src: Core features, artwork rule 4`
- [ ] `C-CF-80` `literal` Artwork `900` pixels wide at a printed width of `30` centimetres is `76` pixels per inch. `src: Core features, artwork rule 4`
- [ ] `C-CF-81` `constraint` A brief whose artwork has not passed cannot request quotes. `src: Core features, artwork rule 5`
- [ ] `C-CF-82` `constraint` A console form refuses invalid input inline, names the field, writes nothing. `src: Core features, artwork rule 6`
- [ ] `C-CF-83` `capability` Requesting quotes fans a brief out to every eligible supplier. `src: Core features, sourcing rule 1`
- [ ] `C-CF-84` `constraint` Supplier eligibility is matched from capability data rather than from code. `src: Core features, sourcing rule 1`
- [ ] `C-CF-85` `constraint` A restart loses no quote request, reply or reminder. `src: Core features, sourcing rule 2`
- [ ] `C-CF-86` `data` An offer records its currency, its incoterm, its unit basis, its setup fee, its lead time, its validity. `src: Core features, sourcing rule 3`
- [ ] `C-CF-87` `capability` Every offer normalises to one landed cost per unit in integer minor units at the brief's quantity. `src: Core features, sourcing rule 4`
- [ ] `C-CF-88` `capability` The landed-cost working shows the unit price, the amortised setup, freight, duty, insurance, the rate with its date. `src: Core features, sourcing rule 4`
- [ ] `C-CF-89` `literal` A per-dozen quote of `46800` minor units is `3900` minor units per piece. `src: Core features, sourcing rule 5`
- [ ] `C-CF-90` `literal` `3900` minor units in `eur` at a recorded rate of `1.08` is `4212` minor units in `usd`. `src: Core features, sourcing rule 5`
- [ ] `C-CF-91` `literal` A setup fee of `85000` minor units across `500` units adds `170` minor units per unit. `src: Core features, sourcing rule 5`
- [ ] `C-CF-92` `literal` Sea freight of `120000` minor units across `500` units adds `240` minor units per unit. `src: Core features, sourcing rule 5`
- [ ] `C-CF-93` `literal` Duty at `12` percent of `4212` minor units adds `505` minor units. `src: Core features, sourcing rule 5`
- [ ] `C-CF-94` `literal` Insurance at `0.4` percent of `4212` minor units adds `17` minor units. `src: Core features, sourcing rule 5`
- [ ] `C-CF-95` `literal` The seeded `aveiro-knitworks` landed cost per unit is `5144` minor units. `src: Core features, sourcing rule 6`
- [ ] `C-CF-96` `literal` The seeded `tirupur-mills` headline unit price is `2900` minor units. `src: Core features, sourcing rule 6`
- [ ] `C-CF-97` `literal` The seeded `tirupur-mills` landed cost per unit is `6010` minor units. `src: Core features, sourcing rule 6`
- [ ] `C-CF-98` `constraint` Offers are compared only after normalisation. `src: Core features, sourcing rule 7`
- [ ] `C-CF-99` `constraint` The same set of offers returns the same ranking whatever the arrival order. `src: Core features, sourcing rule 7`
- [ ] `C-CF-100` `constraint` A later rate movement never changes a historical quote. `src: Core features, sourcing rule 8`
- [ ] `C-CF-101` `literal` `aveiro-knitworks` steps its unit cost at `250`, `500`, `1000` units. `src: Core features, sourcing rule 9`
- [ ] `C-CF-102` `literal` An offer expires `14` days after the offer is made. `src: Core features, sourcing rule 10`
- [ ] `C-CF-103` `constraint` An expired offer cannot be accepted. `src: Core features, sourcing rule 10`
- [ ] `C-CF-104` `constraint` A supplier's quoted prices never appear in a storefront payload. `src: Core features, sourcing rule 11`
- [ ] `C-CF-105` `constraint` A supplier's quoted prices never appear in an agent payload. `src: Core features, sourcing rule 11`
- [ ] `C-CF-106` `data` A sample round records what was requested, what arrived, evidence per angle, measurements against a size specification. `src: Core features, samples rule 1`
- [ ] `C-CF-107` `literal` A sample round decision is one of `accept`, `rework`, `reject`. `src: Core features, samples rule 1`
- [ ] `C-CF-108` `data` A defect records a grade from the three the brief pins above a location on the garment. `src: Core features, samples rule 2`
- [ ] `C-CF-109` `capability` A rework carries its defect list forward into the next round. `src: Core features, samples rule 3`
- [ ] `C-CF-110` `constraint` An approval records who accepted, when, against which evidence, immutably. `src: Core features, samples rule 4`
- [ ] `C-CF-111` `literal` The seeded acceptance rule inspects `80` units from a run of `500`. `src: Core features, samples rule 5`
- [ ] `C-CF-112` `literal` The seeded acceptance rule permits at most `2` major defects. `src: Core features, samples rule 5`
- [ ] `C-CF-113` `literal` The seeded acceptance rule permits at most `5` minor defects. `src: Core features, samples rule 5`
- [ ] `C-CF-114` `constraint` An inspection that exceeds the acceptance rule blocks the shipment. `src: Core features, samples rule 6`
- [ ] `C-CF-115` `literal` A blocked batch raises a decision of `rework`, `partial_accept` or `reject`. `src: Core features, samples rule 6`
- [ ] `C-CF-116` `constraint` A dispatch attempt against a blocked batch is refused. `src: Core features, samples rule 6`
- [ ] `C-CF-117` `literal` A run walks the stages `purchase_order`, `deposit`, `materials`, `production`, `quality`, `packing`, `freight_handover`. `src: Core features, runs rule 1`
- [ ] `C-CF-118` `data` Each run stage records an expected window, an actual, an owning member. `src: Core features, runs rule 2`
- [ ] `C-CF-119` `capability` A slipped stage recomputes the projected ready date. `src: Core features, runs rule 3`
- [ ] `C-CF-120` `constraint` A projected date never moves without a recorded cause. `src: Core features, runs rule 3`
- [ ] `C-CF-121` `capability` A run splits across two factories with lots tracked separately. `src: Core features, runs rule 4`
- [ ] `C-CF-122` `data` A purchase order records its deposit percentage above its payment terms. `src: Core features, runs rule 5`
- [ ] `C-CF-123` `literal` Stock lives in the two locations `rotterdam`, `newark`. `src: Core features, inventory rule 1`
- [ ] `C-CF-124` `literal` The inventory ledger kinds are `receipt`, `reservation`, `allocation`, `pick`, `shipment`, `return`, `write_off`, `transfer_out`, `transfer_in`. `src: Core features, inventory rule 2`
- [ ] `C-CF-125` `constraint` The inventory ledger is append-only in whole units per stock keeping unit per location. `src: Core features, inventory rule 2`
- [ ] `C-CF-126` `constraint` `on_hand` is summed from the ledger every time the figure is read. `src: Core features, inventory rule 3`
- [ ] `C-CF-127` `constraint` No mutable count of stock exists anywhere in the product. `src: Core features, inventory rule 3`
- [ ] `C-CF-128` `data` `available` equals `on_hand` minus reservations minus damaged. `src: Core features, inventory rule 4`
- [ ] `C-CF-129` `capability` An order reserves stock when placed, allocates at pick. `src: Core features, inventory rule 5`
- [ ] `C-CF-130` `capability` A cancelled order releases its reservation. `src: Core features, inventory rule 5`
- [ ] `C-CF-131` `constraint` Two orders racing for the last unit resolve to exactly one reservation. `src: Core features, inventory rule 6`
- [ ] `C-CF-132` `constraint` An inventory balance never goes negative. `src: Core features, inventory rule 6`
- [ ] `C-CF-133` `literal` The seeded boundary leaves one unit of `KJ-WORK-M` available at `newark`. `src: Core features, inventory rule 6`
- [ ] `C-CF-134` `capability` Units in a departed transfer belong to neither location until receipt. `src: Core features, inventory rule 7`
- [ ] `C-CF-135` `ui` Units crossing between continents read as in transit rather than as missing. `src: Core features, inventory rule 7`
- [ ] `C-CF-136` `capability` An order routes to the location that can serve the destination. `src: Core features, inventory rule 8`
- [ ] `C-CF-137` `capability` An order split across two locations carries one delivery promise. `src: Core features, inventory rule 8`
- [ ] `C-CF-138` `capability` A forecast produces a projected stockout date beside a suggested reorder point. `src: Core features, inventory rule 9`
- [ ] `C-CF-139` `capability` Each workspace publishes one hosted storefront with collections, product pages, a cart, a checkout. `src: Core features, storefront rule 1`
- [ ] `C-CF-140` `literal` Gate audience tests compose with `and`, `or`, `not`. `src: Core features, storefront rule 2`
- [ ] `C-CF-141` `constraint` Gate evaluation runs on the server at render. `src: Core features, storefront rule 3`
- [ ] `C-CF-142` `constraint` Gate evaluation runs again on the server at the order. `src: Core features, storefront rule 3`
- [ ] `C-CF-143` `constraint` A forged request for a gated listing is refused at the order rather than hidden at the render. `src: Core features, storefront rule 3`
- [ ] `C-CF-144` `literal` The seeded gated listing `holder-work-jacket` carries a holder price of `5900` minor units. `src: Core features, storefront rule 4`
- [ ] `C-CF-145` `literal` The seeded gated listing carries a public price of `8900` minor units. `src: Core features, storefront rule 4`
- [ ] `C-CF-146` `literal` The seeded gate releases to holders of the `kilnfolk-genesis` collection. `src: Core features, storefront rule 4`
- [ ] `C-CF-147` `ui` Proving an entitlement recomputes the catalogue, the prices, the perks in place without a page reload. `src: Core features, storefront rule 5`
- [ ] `C-CF-148` `ui` A disconnecting visitor returns cleanly to the ungated state. `src: Core features, storefront rule 6`
- [ ] `C-CF-149` `capability` A cart line that is no longer eligible is marked rather than dropped. `src: Core features, storefront rule 6`
- [ ] `C-CF-150` `capability` Proving an address is a signature challenge carrying a nonce above an expiry. `src: Core features, storefront rule 7`
- [ ] `C-CF-151` `constraint` A replayed signature is refused. `src: Core features, storefront rule 7`
- [ ] `C-CF-152` `constraint` An order is priced once, with tax computed before payment. `src: Core features, checkout rule 1`
- [ ] `C-CF-153` `literal` An order reference is `KLN-` followed by six digits, for example `KLN-000412`. `src: Core features, checkout rule 2`
- [ ] `C-CF-154` `capability` A settled fiat order creates or reuses one billing account keyed by the buyer's address lowercased. `src: Core features, checkout rule 3`
- [ ] `C-CF-155` `contract` A settled fiat order raises one invoice for the order total in `USD`. `src: Core features, checkout rule 3`
- [ ] `C-CF-156` `constraint` A replayed `Idempotency-Key` returns the original order with no second invoice. `src: Core features, checkout rule 4`
- [ ] `C-CF-157` `constraint` A replayed `Idempotency-Key` sends no second confirmation mail. `src: Core features, checkout rule 4`
- [ ] `C-CF-158` `literal` A token quote holds for `15` minutes against a recorded rate. `src: Core features, checkout rule 5`
- [ ] `C-CF-159` `literal` A token payment settles at a confirmation depth of `12`. `src: Core features, checkout rule 5`
- [ ] `C-CF-160` `capability` An underpayment credits what arrived, leaving the order awaiting the balance. `src: Core features, checkout rule 6`
- [ ] `C-CF-161` `capability` An overpayment credits the order, recording the excess as refundable. `src: Core features, checkout rule 6`
- [ ] `C-CF-162` `capability` A payment arriving after the quote window is re-quoted rather than refused. `src: Core features, checkout rule 6`
- [ ] `C-CF-163` `capability` A chain reorganisation re-opens the order, reversing its settlement entry. `src: Core features, checkout rule 6`
- [ ] `C-CF-164` `constraint` The receipt, the order record, the finance report agree to the minor unit. `src: Core features, checkout rule 8`
- [ ] `C-CF-165` `constraint` A refund never exceeds the captured amount. `src: Core features, checkout rule 9`
- [ ] `C-CF-166` `constraint` Every money movement is a row in an append-only ledger. `src: Core features, checkout rule 10`
- [ ] `C-CF-167` `literal` The eleven operations surfaces are `receiving`, `put_away`, `storage`, `replenishment`, `pick`, `pack`, `carrier_handoff`, `customs`, `sales_tax`, `tracking`, `returns`. `src: Core features, fulfillment rule 1`
- [ ] `C-CF-168` `literal` The order states are `placed`, `reserved`, `picked`, `packed`, `handed_over`, `in_transit`, `delivered`, `cancelled`, `returned`. `src: Core features, fulfillment rule 2`
- [ ] `C-CF-169` `constraint` A backward order transition is refused. `src: Core features, fulfillment rule 2`
- [ ] `C-CF-170` `data` Every order transition records the actor beside the moment. `src: Core features, fulfillment rule 3`
- [ ] `C-CF-171` `ui` A buyer reads every order transition in ordinary words on their own order page. `src: Core features, fulfillment rule 3`
- [ ] `C-CF-172` `capability` Packing is verified against the order's contents before handoff. `src: Core features, fulfillment rule 4`
- [ ] `C-CF-173` `capability` Carrier handoff records the label beside the tracking identity. `src: Core features, fulfillment rule 5`
- [ ] `C-CF-174` `capability` A carrier outage reroutes the parcel, recording the cost difference. `src: Core features, fulfillment rule 6`
- [ ] `C-CF-175` `constraint` A tracking event resent by a carrier notifies the buyer once. `src: Core features, fulfillment rule 7`
- [ ] `C-CF-176` `capability` An address failure, a customs hold, damage in transit, carrier loss each carry a defined path with an owner. `src: Core features, fulfillment rule 8`
- [ ] `C-CF-177` `data` Every product carries a customs classification code, a country of origin, a declared value basis. `src: Core features, customs rule 1`
- [ ] `C-CF-178` `constraint` A missing classification blocks the dispatch before the parcel leaves. `src: Core features, customs rule 2`
- [ ] `C-CF-179` `literal` The seeded stock keeping unit `CT-NAT-OS` carries no classification. `src: Core features, customs rule 2`
- [ ] `C-CF-180` `capability` Duty is estimated at checkout for delivered-duty-paid destinations as its own line. `src: Core features, customs rule 3`
- [ ] `C-CF-181` `capability` An actual duty assessment differing from the estimate reconciles into the ledger. `src: Core features, customs rule 3`
- [ ] `C-CF-182` `literal` The seeded jurisdiction `NL` charges `21` percent, rounding per invoice. `src: Core features, tax rule 4`
- [ ] `C-CF-183` `literal` The seeded jurisdiction `GB` charges `20` percent, rounding per invoice. `src: Core features, tax rule 4`
- [ ] `C-CF-184` `literal` The seeded jurisdiction `US-CA` charges `8.5` percent, rounding per line. `src: Core features, tax rule 4`
- [ ] `C-CF-185` `constraint` The sum of per-line tax equals the invoice tax exactly. `src: Core features, tax rule 5`
- [ ] `C-CF-186` `constraint` A rounding remainder is allocated by largest remainder rather than dropped. `src: Core features, tax rule 5`
- [ ] `C-CF-187` `literal` Three `NL` lines of `3333`, `3333`, `3334` minor units carry an invoice tax of `2100` minor units. `src: Core features, tax rule 6`
- [ ] `C-CF-188` `literal` The recorded `NL` allocation across those three lines is `700`, `700`, `700`. `src: Core features, tax rule 6`
- [ ] `C-CF-189` `constraint` Refunding one line returns exactly the tax recorded against that line. `src: Core features, tax rule 7`
- [ ] `C-CF-190` `literal` The seeded nexus threshold is `10000000` minor units in a calendar year. `src: Core features, tax rule 8`
- [ ] `C-CF-191` `constraint` A period filing report balances to a difference of zero. `src: Core features, tax rule 9`
- [ ] `C-CF-192` `literal` A return walks authorisation, a label, receipt, inspection, then `restock`, `refurbish` or `write_off`. `src: Core features, returns rule 1`
- [ ] `C-CF-193` `constraint` The refund with the inventory event issue from one inspection decision. `src: Core features, returns rule 2`
- [ ] `C-CF-194` `capability` A cross-border return generates its own customs paperwork. `src: Core features, returns rule 3`
- [ ] `C-CF-195` `constraint` The return policy recorded on the order governs the refund rather than today's setting. `src: Core features, returns rule 4`
- [ ] `C-CF-196` `literal` The return window is `30` days from delivery. `src: Core features, returns rule 5`
- [ ] `C-CF-197` `constraint` A return requested outside the window is refused. `src: Core features, returns rule 5`
- [ ] `C-CF-198` `capability` A buyer is given one delivery window at checkout. `src: Core features, promise rule 1`
- [ ] `C-CF-199` `data` A promise records the inputs that produced the window. `src: Core features, promise rule 2`
- [ ] `C-CF-200` `data` Every open promise carries one owning stage. `src: Core features, promise rule 3`
- [ ] `C-CF-201` `capability` A moved input recomputes the window, recording the revision with its cause. `src: Core features, promise rule 4`
- [ ] `C-CF-202` `constraint` A buyer is notified once per recomputation. `src: Core features, promise rule 4`
- [ ] `C-CF-203` `constraint` A factory slip, a carrier degradation, a customs hold together produce one recomputed window. `src: Core features, promise rule 5`
- [ ] `C-CF-204` `ui` The console ranks every promise at risk by how far the promise has slipped. `src: Core features, promise rule 6`
- [ ] `C-CF-205` `capability` On-time performance reports by stage, by supplier, by carrier, by lane. `src: Core features, promise rule 7`
- [ ] `C-CF-206` `literal` The seeded drop `kilnfolk-winter` carries a supply of `40`. `src: Core features, drops rule 1`
- [ ] `C-CF-207` `literal` The seeded drop allows `2` per buyer. `src: Core features, drops rule 1`
- [ ] `C-CF-208` `constraint` A fixed drop supply never oversells under a rush. `src: Core features, drops rule 2`
- [ ] `C-CF-209` `constraint` A per-buyer allowance holds across parallel sessions. `src: Core features, drops rule 2`
- [ ] `C-CF-210` `ui` A late arrival receives an honest queue position rather than a spinner. `src: Core features, drops rule 3`
- [ ] `C-CF-211` `literal` The seeded odds are `common` at `0.70`, `rare` at `0.25`, `grail` at `0.05`. `src: Core features, drops rule 4`
- [ ] `C-CF-212` `constraint` Published odds stay immutable for the whole time a drop runs. `src: Core features, drops rule 5`
- [ ] `C-CF-213` `capability` A seed digest is published before the drop opens. `src: Core features, drops rule 6`
- [ ] `C-CF-214` `capability` The seed is revealed after the drop closes so a buyer can check their own pull. `src: Core features, drops rule 6`
- [ ] `C-CF-215` `constraint` A pull that would exceed its outcome's remaining stock is prevented before the money is taken. `src: Core features, drops rule 7`
- [ ] `C-CF-216` `capability` The realised distribution reconciles against the published odds after the drop closes. `src: Core features, drops rule 8`
- [ ] `C-CF-217` `literal` The seeded pre-sale threshold is `5000000` minor units. `src: Core features, drops rule 9`
- [ ] `C-CF-218` `constraint` Money taken for an unproduced good is held as its own ledger kind. `src: Core features, drops rule 9`
- [ ] `C-CF-219` `capability` A machine-readable catalogue exposes products, variants, prices, availability, lead times. `src: Core features, agent rule 1`
- [ ] `C-CF-220` `constraint` The machine catalogue carries the same gating the human storefront carries. `src: Core features, agent rule 1`
- [ ] `C-CF-221` `constraint` An agent order walks the same reservation, tax, promise machinery a buyer walks. `src: Core features, agent rule 2`
- [ ] `C-CF-222` `data` An agent credential carries an owner, scopes, a spend limit, a rate limit. `src: Core features, agent rule 3`
- [ ] `C-CF-223` `capability` Revoking a credential releases its open reservations. `src: Core features, agent rule 4`
- [ ] `C-CF-224` `constraint` A drop allowance counts a buyer's own orders together with their agents' orders. `src: Core features, agent rule 5`
- [ ] `C-CF-225` `constraint` The same period totalled by different axes agrees exactly. `src: Core features, reporting rule 2`
- [ ] `C-CF-226` `capability` A support conversation carries the order context. `src: Core features, support rule 3`
- [ ] `C-CF-227` `constraint` An assistant answer cites a procedure version or escalates. `src: Core features, support rule 4`
- [ ] `C-CF-228` `data` An answer records which procedure version the answer was drafted from. `src: Core features, support rule 5`
- [ ] `C-CF-229` `literal` The seeded workspace carries `3` versions of its returns procedure. `src: Core features, support rule 5`
- [ ] `C-CF-230` `constraint` An announcement honours the suppression list. `src: Core features, email rule 1`
- [ ] `C-CF-231` `constraint` An unsubscribe takes effect across every future send. `src: Core features, email rule 2`
- [ ] `C-CF-232` `literal` An order confirmation subject begins `Kilnly order confirmed: ` before the order reference. `src: Core features, email rule 3`
- [ ] `C-CF-233` `literal` A promise revision subject begins `Kilnly delivery update: ` before the order reference. `src: Core features, email rule 3`
- [ ] `C-CF-234` `literal` A return authorisation subject begins `Kilnly return authorised: ` before the return reference. `src: Core features, email rule 3`
- [ ] `C-CF-235` `literal` The seeded announcement subject is `Kilnfolk winter drop opens Friday`. `src: Core features, email rule 3`
- [ ] `C-CF-236` `constraint` A confirmation reaches the ordering buyer's address alone with nobody in copy. `src: Core features, email rule 4`
- [ ] `C-CF-237` `constraint` Moving an order from `picked` to `packed` sends no mail. `src: Core features, email rule 5`
- [ ] `C-CF-238` `constraint` A holder's standing is computed at read time from current entitlements. `src: Core features, holders rule 1`
- [ ] `C-CF-239` `constraint` No membership flag is written once at signup. `src: Core features, holders rule 1`
- [ ] `C-CF-240` `capability` A cached standing is invalidated when an entitlement changes. `src: Core features, holders rule 2`
- [ ] `C-CF-241` `ui` The holders hub shows what a holder owns beside what is redeemable now. `src: Core features, holders rule 3`
- [ ] `C-CF-242` `constraint` A claim marks the entitlement, reserves stock, creates the order together or not at all. `src: Core features, holders rule 4`
- [ ] `C-CF-243` `constraint` A failure in any claim leg unwinds the other two. `src: Core features, holders rule 5`
- [ ] `C-CF-244` `constraint` A claim racing a transfer of the same entitlement resolves once. `src: Core features, holders rule 6`
- [ ] `C-CF-245` `capability` An unclaimed entitlement past its window is reported rather than silently expired. `src: Core features, holders rule 7`
- [ ] `C-CF-246` `data` Every allowlist entry records why the entry exists. `src: Core features, holders rule 8`
- [ ] `C-CF-247` `data` The run cost model carries unit cost, tooling, freight, duty, insurance, inspection, warehousing, pick-and-pack, carrier cost, payment fees, a returns allowance. `src: Core features, economics rule 1`
- [ ] `C-CF-248` `constraint` Margin is computed against the landed cost of the lot a unit came from. `src: Core features, economics rule 2`
- [ ] `C-CF-249` `constraint` Cost of goods sold uses the lots actually shipped rather than an average. `src: Core features, economics rule 3`
- [ ] `C-CF-250` `literal` The two seeded lots of `KJ-WORK-M` carry landed costs of `5144`, `6010` minor units. `src: Core features, economics rule 3`
- [ ] `C-CF-251` `constraint` The quoting engine refuses a lead time a supplier's throughput cannot support. `src: Core features, economics rule 4`

## C-UF User flow

- [ ] `C-UF-01` `literal` The landing route is `/`. `src: User flow route table`
- [ ] `C-UF-02` `literal` The catalogue route is `/catalogue`. `src: User flow route table`
- [ ] `C-UF-03` `literal` The fulfillment route is `/merch-fulfillment`. `src: User flow route table`
- [ ] `C-UF-04` `literal` The no-minimum route is `/custom-merch-no-minimum`. `src: User flow route table`
- [ ] `C-UF-05` `literal` The brand kit route is `/brand`. `src: User flow route table`
- [ ] `C-UF-06` `literal` The storefront route is `/shop`. `src: User flow route table`
- [ ] `C-UF-07` `literal` A buyer's own order reads at `/order/:reference`. `src: User flow route table`
- [ ] `C-UF-08` `literal` The holders hub route is `/holders`. `src: User flow route table`
- [ ] `C-UF-09` `literal` The project list route is `/app`. `src: User flow route table`
- [ ] `C-UF-10` `literal` The inventory route is `/app/inventory`. `src: User flow route table`
- [ ] `C-UF-11` `capability` An unauthenticated request for a console route lands on sign-in, returning afterwards. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `capability` An expired token mid-action returns the member to sign-in with the pending work unwritten. `src: User flow, entry and redirects`
- [ ] `C-UF-13` `constraint` A buyer who opens the console is refused. `src: User flow, entry and redirects`
- [ ] `C-UF-14` `constraint` A cross-workspace project identifier answers not found. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `ui` A visitor throws the pile, then filters the catalogue, then starts a project. `src: User flow, journey 1`
- [ ] `C-UF-16` `ui` An entitled buyer watches the gated price appear in place with no page reload. `src: User flow, journey 5`
- [ ] `C-UF-17` `ui` Every list carries a designed empty state naming its one next action. `src: User flow, states`
- [ ] `C-UF-18` `ui` A failed write leaves what the member typed in the field the member typed into. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product is built to one north star, a founder believing real objects can be made without holding the chain in mind. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The marketing register is consumer editorial with a point of view. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The console register is operational, quiet, built for scanning. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` The page ground is a warm near-white, nearer paper than white. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` A faint blueprint grid rules the landing page. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` The site alternates paper sheets with deep near-black panels as its one structural rhythm. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` One light, vivid red-orange marks what can be pressed, appearing nowhere decorative. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` Three meaning colours carry live, pending, destructive, borrowed by nothing else. `src: UI/UX notes para 2`
- [ ] `C-UX-09` `ui` Body text meets WCAG AA contrast against the surface the text sits on. `src: UI/UX notes para 2`
- [ ] `C-UX-10` `literal` The interface family is `Inter`. `src: UI/UX notes para 3`
- [ ] `C-UX-11` `literal` The display family is `Baloo 2`. `src: UI/UX notes para 3`
- [ ] `C-UX-12` `ui` The display family never sets a table or a form label. `src: UI/UX notes para 3`
- [ ] `C-UX-13` `ui` Figures line up in a column wherever amounts stack. `src: UI/UX notes para 3`
- [ ] `C-UX-14` `ui` The pill is the dominant shape from the header through the chips to the buttons. `src: UI/UX notes para 4`
- [ ] `C-UX-15` `ui` Sections read as separate at a glance without a dividing rule. `src: UI/UX notes para 4`
- [ ] `C-UX-16` `ui` Everything moves on one character, settling rather than snapping. `src: UI/UX notes para 5`
- [ ] `C-UX-17` `ui` The display headline arrives one word at a time. `src: UI/UX notes para 5`
- [ ] `C-UX-18` `ui` A scroll reveal has two states, playing once per band. `src: UI/UX notes para 5`
- [ ] `C-UX-19` `ui` Under reduced motion the drift, the twinkle, the beams, the marquees stop. `src: UI/UX notes para 5`
- [ ] `C-UX-20` `ui` The console places navigation down the left, work in the middle. `src: UI/UX notes para 6`
- [ ] `C-UX-21` `ui` A failed console write returns the row to what the service holds, offering the action again. `src: UI/UX notes para 6`
- [ ] `C-UX-22` `ui` Every control carries resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes para 7`
- [ ] `C-UX-23` `ui` Unavailable is never signalled by colour alone. `src: UI/UX notes para 7`
- [ ] `C-UX-24` `ui` Every hovered affordance carries a focus-visible twin showing the same change. `src: UI/UX notes para 7`
- [ ] `C-UX-25` `ui` Keyboard navigation reveals exactly what a pointer reveals. `src: UI/UX notes para 7`
- [ ] `C-UX-26` `ui` Live regions announce order state changes, promise revisions, stock refusals, queue positions. `src: UI/UX notes para 7`
- [ ] `C-UX-27` `ui` A burst of events produces one announcement rather than one per event. `src: UI/UX notes para 7`
- [ ] `C-UX-28` `ui` At a narrow viewport nothing overflows sideways. `src: UI/UX notes para 8`
- [ ] `C-UX-29` `ui` The catalogue steps from four columns to two to one. `src: UI/UX notes para 8`
- [ ] `C-UX-30` `ui` Below the tablet breakpoint the quote comparison scrolls sideways with its first column pinned. `src: UI/UX notes para 8`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is SolidJS built with Vite. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The backend is Litestar on Python 3.12. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The datastore is PostgreSQL at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` Mail goes over real SMTP to Mailpit at `SMTP_HOST`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` Billing is killbill at `PAYMENTS_API_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `constraint` Every public marketing route carries its title inside the document the server returns. `src: Technical requirements para 1`
- [ ] `C-TR-07` `constraint` No second datastore, cache, queue, object store, identity provider or mail vendor is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-08` `literal` A call under `/1.0/kb/` carries `X-Killbill-ApiKey` beside `X-Killbill-ApiSecret`. `src: Technical requirements para 3`
- [ ] `C-TR-09` `literal` The billing Basic credentials are the user `admin` with the password `password`. `src: Technical requirements para 3`
- [ ] `C-TR-10` `constraint` The loser of a race for the last unit receives a `409` conflict response naming the stock keeping unit. `src: Technical requirements, simultaneous requests`
- [ ] `C-TR-11` `constraint` Money is integer minor units throughout, never a floating-point value. `src: Technical requirements, money and units`
- [ ] `C-TR-12` `constraint` Every timestamp is stored absolute in UTC. `src: Technical requirements, money and units`
- [ ] `C-TR-13` `capability` One event stream carries order transitions, inventory events, promise revisions, tracking updates. `src: Technical requirements, liveness`
- [ ] `C-TR-14` `constraint` Two people watching one order converge within about a second. `src: Technical requirements, liveness`
- [ ] `C-TR-15` `constraint` The inventory grid holds its frame rate at ten thousand rows. `src: Technical requirements, performance`
- [ ] `C-TR-16` `constraint` Product photography is generated from a seed derived from the product's slug. `src: Technical requirements, assets`
- [ ] `C-TR-17` `literal` `GET /api/health` returns `200` once the app is ready. `src: Technical requirements, health`
- [ ] `C-TR-18` `constraint` Uploaded artwork is delivered through short-lived signed links, stripped of metadata. `src: Technical requirements, security`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model, password paragraph`
- [ ] `C-DM-02` `contract` The seeded logins are written into `/app/USER_README.md`. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` A `membership` row carries its workspace, its account, its role. `src: Data model, membership`
- [ ] `C-DM-04` `literal` The four workspace roles are `owner`, `operator`, `finance`, `viewer`. `src: Data model, membership`
- [ ] `C-DM-05` `literal` The four product categories are `apparel`, `outerwear`, `headwear`, `accessories`. `src: Data model, product`
- [ ] `C-DM-06` `literal` The stock keeping unit `KJ-WORK-M` is the `Washed Work Jacket` in medium. `src: Data model, sku`
- [ ] `C-DM-07` `data` A `project` moves forward only through its states. `src: Data model, project`
- [ ] `C-DM-08` `data` An `artwork` row records its pixel width, its colour count, its bleed, its state. `src: Data model, artwork`
- [ ] `C-DM-09` `data` A `landed_cost` row stores every component separately. `src: Data model, landed cost`
- [ ] `C-DM-10` `data` An `offer` is immutable once made. `src: Data model, offer`
- [ ] `C-DM-11` `data` An `inventory_event` row carries its stock keeping unit, its location, its kind, its units. `src: Data model, inventory event`
- [ ] `C-DM-12` `data` A `transfer` in state `departed` holds units that belong to neither location. `src: Data model, transfer`
- [ ] `C-DM-13` `data` An `order` records the return policy that applied when the order was placed. `src: Data model, order`
- [ ] `C-DM-14` `data` An `order_line` records its tax allocation. `src: Data model, order line`
- [ ] `C-DM-15` `constraint` An order total equals its line totals plus shipping plus tax plus duty at every moment. `src: Data model, order`
- [ ] `C-DM-16` `data` One capture exists per idempotency key. `src: Data model, payment`
- [ ] `C-DM-17` `literal` The money ledger kinds are `settlement`, `refund`, `reversal`, `presale_held`, `payout`, `fee`. `src: Data model, money ledger`
- [ ] `C-DM-18` `data` A `tax_rate` row carries its jurisdiction, its rate, its effective date, its rounding rule. `src: Data model, tax rate`
- [ ] `C-DM-19` `data` A `promise_revision` records its cause. `src: Data model, promise`
- [ ] `C-DM-20` `data` A `pull` is verifiable against the revealed seed. `src: Data model, drop`
- [ ] `C-DM-21` `constraint` A stored order records the version of the rules the order was written under. `src: Data model, schema evolution`
- [ ] `C-DM-22` `constraint` A tax rate change leaves an existing order reading as the order read when written. `src: Data model, schema evolution`
- [ ] `C-DM-23` `constraint` Seeding is idempotent, so restarting the app duplicates no row. `src: Data model, seed data`
- [ ] `C-DM-24` `literal` The seeded in-flight transfer moves `6` units of `KJ-WORK-M` from `rotterdam` to `newark`. `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Content sits inside a ladder of ten fixed measures rather than a fluid width. `src: Front-end specification, ground`
- [ ] `C-FE-02` `ui` The layout changes at one dominant breakpoint above lighter steps. `src: Front-end specification, ground`
- [ ] `C-FE-03` `ui` Where a device cannot hover, hover-revealed affordances are pinned visible. `src: Front-end specification, ground`
- [ ] `C-FE-04` `ui` Stacking follows a closed ladder that nothing is introduced outside of. `src: Front-end specification, ground`
- [ ] `C-FE-05` `ui` A four-step ink-alpha ladder carries hairlines, dividers, secondary text, the card shadow. `src: Front-end specification, palette`
- [ ] `C-FE-06` `ui` Two gradients exist, a flat paper one beside an accent one. `src: Front-end specification, palette`
- [ ] `C-FE-07` `ui` Partner marks are set as greyscale text wordmarks. `src: Front-end specification, palette`
- [ ] `C-FE-08` `literal` Body text sits at 16px with dense interface text at 14px. `src: Front-end specification, type`
- [ ] `C-FE-09` `literal` Micro labels sit at 11px, 10px, never growing at any width. `src: Front-end specification, type`
- [ ] `C-FE-10` `ui` The wordmark is drawn geometry of four closed letterform paths rather than a font glyph. `src: Front-end specification, marks`
- [ ] `C-FE-11` `ui` The wordmark carries a text label beside the wordmark for assistive technology. `src: Front-end specification, marks`
- [ ] `C-FE-12` `ui` The mascot is a goldfish character in sunglasses appearing once per page at most. `src: Front-end specification, marks`
- [ ] `C-FE-13` `ui` A chevron rotates a half turn when its disclosure opens. `src: Front-end specification, icons`
- [ ] `C-FE-14` `ui` The up-and-right arrow shifts a hair right with a hair up when its parent is pointed at. `src: Front-end specification, icons`
- [ ] `C-FE-15` `ui` A status mark is always paired with its word. `src: Front-end specification, icons`
- [ ] `C-FE-16` `literal` The intro reel's first line reads `Pondering manufacturers...` `src: Front-end specification, intro reel`
- [ ] `C-FE-17` `literal` The intro reel carries `12` rotating status lines. `src: Front-end specification, intro reel`
- [ ] `C-FE-18` `literal` The header's two menu labels read `Past drops`, `Kilnfolk`. `src: Front-end specification, header`
- [ ] `C-FE-19` `literal` The header's third link reads `Whitelist`. `src: Front-end specification, header`
- [ ] `C-FE-20` `literal` The footer copyright line reads `(C) 2026 Kilnly`. `src: Front-end specification, footer`
- [ ] `C-FE-21` `literal` The footer's four column heads are Past drops, Resources, Community, Social. `src: Front-end specification, footer`
- [ ] `C-FE-22` `ui` A text link falls to about two thirds of its strength when pointed at. `src: Front-end specification, hover`
- [ ] `C-FE-23` `ui` Buttons come in three, a signal pill, an ink pill, a ghost with a hairline border. `src: Front-end specification, furniture`
- [ ] `C-FE-24` `ui` Category chips are fully round buttons that fill with ink when selected. `src: Front-end specification, furniture`
- [ ] `C-FE-25` `ui` Ten named motion moments share the product's one character. `src: Front-end specification, motion`
- [ ] `C-FE-26` `constraint` No scroll-scrubbed timeline is introduced anywhere. `src: Front-end specification, motion`
- [ ] `C-FE-27` `literal` The hero headline reads `Create your dream merch on autopilot`. `src: Front-end specification, landing bands`
- [ ] `C-FE-28` `literal` The positioning line reads `Grow your brand, not your ops.` `src: Front-end specification, landing bands`
- [ ] `C-FE-29` `ui` The extras grid carries the joking heading the brief pins above eight cards. `src: Front-end specification, landing bands`
- [ ] `C-FE-30` `literal` The first capability panel reads `Find your ideal suppliers.` `src: Front-end specification, landing bands`
- [ ] `C-FE-31` `literal` The first pill reads `emailing 12 manufacturers`. `src: Front-end specification, pill pile`
- [ ] `C-FE-32` `literal` The catalogue page is headed `Latest productions`. `src: Front-end specification, catalogue`
- [ ] `C-FE-33` `literal` The fulfillment page is headed `Merch fulfillment, end to end.` `src: Front-end specification, fulfillment`
- [ ] `C-FE-34` `literal` The fulfillment figures read `11 Ops surfaces we run`, `1 Minimum order`. `src: Front-end specification, fulfillment`
- [ ] `C-FE-35` `ui` The console adds no colour, no new corner softness, no new spacing step, no new type step. `src: Front-end specification, console`
- [ ] `C-FE-36` `ui` The quote comparison is readable as a table rather than only as a chart. `src: Front-end specification, console`
- [ ] `C-FE-37` `ui` Console tables are navigable with the arrow keys. `src: Front-end specification, console`
- [ ] `C-FE-38` `ui` Product photography is a seeded flat-lay silhouette on the paper ground under a soft shadow. `src: Front-end specification, substitution`
- [ ] `C-FE-39` `ui` Panel imagery is a seeded gradient field with grain carrying its caption. `src: Front-end specification, substitution`
- [ ] `C-FE-40` `constraint` One generator feeds both the catalogue images with the storefront mocks. `src: Front-end specification, substitution`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One workspace's data is unreachable from another through search. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` A cross-workspace read answers not found rather than denied. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` Supplier terms never appear in a buyer-reachable export. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` No real carrier, customs authority, tax authority or chain node is contacted. `src: Constraints bullet 3`
- [ ] `C-CN-05` `constraint` The server makes no call to any host outside the environment at run time. `src: Constraints bullet 4`
- [ ] `C-CN-06` `constraint` No native application, browser extension or desktop client ships. `src: Constraints bullet 7`
- [ ] `C-CN-07` `constraint` No direct messaging between buyers exists. `src: Constraints bullet 8`
- [ ] `C-CN-08` `constraint` No card primary account number is stored anywhere. `src: Constraints bullet 9`
- [ ] `C-CN-09` `constraint` No wallet private key is stored anywhere. `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` The product stays responsive with ten thousand orders. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on that same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-05` `contract` A reserved `.browser_screenshots/` directory exists empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-06` `contract` A reserved `.downloads/` directory exists empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-07` `contract` A production build is served behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `literal` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `contract` The backing services are already running, so none is downloaded or started. `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `contract` No persistent volumes, no fixed container names, no custom networks. `src: Deployment contract bullet 12`
- [ ] `C-DC-12` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-13` `contract` An invalid or unauthorized call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-14` `contract` Bearer auth is required on everything except sign-in, sign-up, health, public reads. `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `constraint` An in-memory array of orders is a contract violation. `src: Deployment contract, No mocks`
- [ ] `C-DC-16` `constraint` A stock count written rather than summed is a contract violation. `src: Deployment contract, No mocks`
- [ ] `C-DC-17` `constraint` A hardcoded invoice object the app returns to itself is a contract violation. `src: Deployment contract, No mocks`

## Pinned literals

| Value | What it is | Item | Source |
|---|---|---|---|
| `owner@example.com` | pinned by the brief | C-RL-23 | User roles, seeded accounts paragraph |
| `operator@example.com` | pinned by the brief | C-RL-24 | User roles, seeded accounts paragraph |
| `finance@example.com` | pinned by the brief | C-RL-25 | User roles, seeded accounts paragraph |
| `viewer@example.com` | pinned by the brief | C-RL-26 | User roles, seeded accounts paragraph |
| `owner2@example.com` | pinned by the brief | C-RL-27 | User roles, seeded accounts paragraph |
| `buyer@example.com` | pinned by the brief | C-RL-28 | User roles, seeded accounts paragraph |
| `buyer2@example.com` | pinned by the brief | C-RL-29 | User roles, seeded accounts paragraph |
| `buyer3@example.com` | pinned by the brief | C-RL-30 | User roles, seeded accounts paragraph |
| `Tidewater Goods` | pinned by the brief | C-RL-31 | User roles, seeded accounts paragraph |
| `Copperline Club` | pinned by the brief | C-RL-31 | User roles, seeded accounts paragraph |
| `access_token` | pinned by the brief | C-CF-02 | Core features, Auth |
| `Acid-Wash Patch Tee` | pinned by the brief | C-CF-30 | Core features, catalogue rule 2 |
| `3400` | pinned by the brief | C-CF-30 | Core features, catalogue rule 2 |
| `100` | pinned by the brief | C-CF-30 | Core features, catalogue rule 2 |
| `Embroidered Logo Tee` | pinned by the brief | C-CF-31 | Core features, catalogue rule 2 |
| `3000` | pinned by the brief | C-CF-31 | Core features, catalogue rule 2 |
| `Acid-Wash Embroidered Hoodie` | pinned by the brief | C-CF-32 | Core features, catalogue rule 2 |
| `4800` | pinned by the brief | C-CF-32 | Core features, catalogue rule 2 |
| `50` | pinned by the brief | C-CF-32 | Core features, catalogue rule 2 |
| `Embroidered Quarter-Zip` | pinned by the brief | C-CF-33 | Core features, catalogue rule 2 |
| `Embroidered Dad Cap` | pinned by the brief | C-CF-34 | Core features, catalogue rule 2 |
| `1900` | pinned by the brief | C-CF-34 | Core features, catalogue rule 2 |
| `Washed Work Jacket` | pinned by the brief | C-CF-35 | Core features, catalogue rule 2 |
| `6800` | pinned by the brief | C-CF-35 | Core features, catalogue rule 2 |
| `Canvas Duffel Bag` | pinned by the brief | C-CF-36 | Core features, catalogue rule 2 |
| `4200` | pinned by the brief | C-CF-36 | Core features, catalogue rule 2 |
| `Canvas Tote` | pinned by the brief | C-CF-37 | Core features, catalogue rule 2 |
| `2200` | pinned by the brief | C-CF-37 | Core features, catalogue rule 2 |
| `All` | pinned by the brief | C-CF-38 | Core features, catalogue rule 3 |
| `Apparel` | pinned by the brief | C-CF-38 | Core features, catalogue rule 3 |
| `Outerwear` | pinned by the brief | C-CF-38 | Core features, catalogue rule 3 |
| `Headwear` | pinned by the brief | C-CF-38 | Core features, catalogue rule 3 |
| `Accessories` | pinned by the brief | C-CF-38 | Core features, catalogue rule 3 |
| `Nobody owns the delivery date.` | pinned by the brief | C-CF-43 | Core features, fulfillment rule 2 |
| `11` | pinned by the brief | C-CF-44 | Core features, fulfillment rule 3 |
| `1` | pinned by the brief | C-CF-45 | Core features, fulfillment rule 3 |
| `Supply chain` | pinned by the brief | C-CF-52 | Core features, field notes rule 3 |
| `Commerce` | pinned by the brief | C-CF-52 | Core features, field notes rule 3 |
| `Industry` | pinned by the brief | C-CF-52 | Core features, field notes rule 3 |
| `/legal/website-terms-of-use` | pinned by the brief | C-CF-54 | Core features, legal rule 1 |
| `/legal/privacy` | pinned by the brief | C-CF-57 | Core features, legal rule 2 |
| `Page not found` | pinned by the brief | C-CF-59 | Core features, not-found rule 3 |
| `/sitemap.xml` | pinned by the brief | C-CF-62 | Core features, machine routes rule 5 |
| `/robots.txt` | pinned by the brief | C-CF-63 | Core features, machine routes rule 5 |
| `screen_print` | pinned by the brief | C-CF-74 | Core features, brief rule 2 |
| `embroidery` | pinned by the brief | C-CF-74 | Core features, brief rule 2 |
| `patch` | pinned by the brief | C-CF-74 | Core features, brief rule 2 |
| `wash` | pinned by the brief | C-CF-74 | Core features, brief rule 2 |
| `150` | pinned by the brief | C-CF-75 | Core features, artwork rule 3 |
| `6` | pinned by the brief | C-CF-76 | Core features, artwork rule 3 |
| `12` | pinned by the brief | C-CF-77 | Core features, artwork rule 3 |
| `3` | pinned by the brief | C-CF-78 | Core features, artwork rule 3 |
| `900` | pinned by the brief | C-CF-80 | Core features, artwork rule 4 |
| `30` | pinned by the brief | C-CF-80 | Core features, artwork rule 4 |
| `76` | pinned by the brief | C-CF-80 | Core features, artwork rule 4 |
| `46800` | pinned by the brief | C-CF-89 | Core features, sourcing rule 5 |
| `3900` | pinned by the brief | C-CF-89 | Core features, sourcing rule 5 |
| `eur` | pinned by the brief | C-CF-90 | Core features, sourcing rule 5 |
| `1.08` | pinned by the brief | C-CF-90 | Core features, sourcing rule 5 |
| `4212` | pinned by the brief | C-CF-90 | Core features, sourcing rule 5 |
| `usd` | pinned by the brief | C-CF-90 | Core features, sourcing rule 5 |
| `85000` | pinned by the brief | C-CF-91 | Core features, sourcing rule 5 |
| `500` | pinned by the brief | C-CF-91 | Core features, sourcing rule 5 |
| `170` | pinned by the brief | C-CF-91 | Core features, sourcing rule 5 |
| `120000` | pinned by the brief | C-CF-92 | Core features, sourcing rule 5 |
| `240` | pinned by the brief | C-CF-92 | Core features, sourcing rule 5 |
| `505` | pinned by the brief | C-CF-93 | Core features, sourcing rule 5 |
| `0.4` | pinned by the brief | C-CF-94 | Core features, sourcing rule 5 |
| `17` | pinned by the brief | C-CF-94 | Core features, sourcing rule 5 |
| `aveiro-knitworks` | pinned by the brief | C-CF-95 | Core features, sourcing rule 6 |
| `5144` | pinned by the brief | C-CF-95 | Core features, sourcing rule 6 |
| `tirupur-mills` | pinned by the brief | C-CF-96 | Core features, sourcing rule 6 |
| `2900` | pinned by the brief | C-CF-96 | Core features, sourcing rule 6 |
| `6010` | pinned by the brief | C-CF-97 | Core features, sourcing rule 6 |
| `250` | pinned by the brief | C-CF-101 | Core features, sourcing rule 9 |
| `1000` | pinned by the brief | C-CF-101 | Core features, sourcing rule 9 |
| `14` | pinned by the brief | C-CF-102 | Core features, sourcing rule 10 |
| `accept` | pinned by the brief | C-CF-107 | Core features, samples rule 1 |
| `rework` | pinned by the brief | C-CF-107 | Core features, samples rule 1 |
| `reject` | pinned by the brief | C-CF-107 | Core features, samples rule 1 |
| `80` | pinned by the brief | C-CF-111 | Core features, samples rule 5 |
| `2` | pinned by the brief | C-CF-112 | Core features, samples rule 5 |
| `5` | pinned by the brief | C-CF-113 | Core features, samples rule 5 |
| `partial_accept` | pinned by the brief | C-CF-115 | Core features, samples rule 6 |
| `purchase_order` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `deposit` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `materials` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `production` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `quality` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `packing` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `freight_handover` | pinned by the brief | C-CF-117 | Core features, runs rule 1 |
| `rotterdam` | pinned by the brief | C-CF-123 | Core features, inventory rule 1 |
| `newark` | pinned by the brief | C-CF-123 | Core features, inventory rule 1 |
| `receipt` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `reservation` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `allocation` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `pick` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `shipment` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `return` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `write_off` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `transfer_out` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `transfer_in` | pinned by the brief | C-CF-124 | Core features, inventory rule 2 |
| `KJ-WORK-M` | pinned by the brief | C-CF-133 | Core features, inventory rule 6 |
| `and` | pinned by the brief | C-CF-140 | Core features, storefront rule 2 |
| `or` | pinned by the brief | C-CF-140 | Core features, storefront rule 2 |
| `not` | pinned by the brief | C-CF-140 | Core features, storefront rule 2 |
| `holder-work-jacket` | pinned by the brief | C-CF-144 | Core features, storefront rule 4 |
| `5900` | pinned by the brief | C-CF-144 | Core features, storefront rule 4 |
| `8900` | pinned by the brief | C-CF-145 | Core features, storefront rule 4 |
| `kilnfolk-genesis` | pinned by the brief | C-CF-146 | Core features, storefront rule 4 |
| `KLN-` | pinned by the brief | C-CF-153 | Core features, checkout rule 2 |
| `KLN-000412` | pinned by the brief | C-CF-153 | Core features, checkout rule 2 |
| `15` | pinned by the brief | C-CF-158 | Core features, checkout rule 5 |
| `receiving` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `put_away` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `storage` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `replenishment` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `pack` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `carrier_handoff` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `customs` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `sales_tax` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `tracking` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `returns` | pinned by the brief | C-CF-167 | Core features, fulfillment rule 1 |
| `placed` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `reserved` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `picked` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `packed` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `handed_over` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `in_transit` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `delivered` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `cancelled` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `returned` | pinned by the brief | C-CF-168 | Core features, fulfillment rule 2 |
| `CT-NAT-OS` | pinned by the brief | C-CF-179 | Core features, customs rule 2 |
| `NL` | pinned by the brief | C-CF-182 | Core features, tax rule 4 |
| `21` | pinned by the brief | C-CF-182 | Core features, tax rule 4 |
| `GB` | pinned by the brief | C-CF-183 | Core features, tax rule 4 |
| `20` | pinned by the brief | C-CF-183 | Core features, tax rule 4 |
| `US-CA` | pinned by the brief | C-CF-184 | Core features, tax rule 4 |
| `8.5` | pinned by the brief | C-CF-184 | Core features, tax rule 4 |
| `3333` | pinned by the brief | C-CF-187 | Core features, tax rule 6 |
| `3334` | pinned by the brief | C-CF-187 | Core features, tax rule 6 |
| `2100` | pinned by the brief | C-CF-187 | Core features, tax rule 6 |
| `700` | pinned by the brief | C-CF-188 | Core features, tax rule 6 |
| `10000000` | pinned by the brief | C-CF-190 | Core features, tax rule 8 |
| `restock` | pinned by the brief | C-CF-192 | Core features, returns rule 1 |
| `refurbish` | pinned by the brief | C-CF-192 | Core features, returns rule 1 |
| `kilnfolk-winter` | pinned by the brief | C-CF-206 | Core features, drops rule 1 |
| `40` | pinned by the brief | C-CF-206 | Core features, drops rule 1 |
| `common` | pinned by the brief | C-CF-211 | Core features, drops rule 4 |
| `0.70` | pinned by the brief | C-CF-211 | Core features, drops rule 4 |
| `rare` | pinned by the brief | C-CF-211 | Core features, drops rule 4 |
| `0.25` | pinned by the brief | C-CF-211 | Core features, drops rule 4 |
| `grail` | pinned by the brief | C-CF-211 | Core features, drops rule 4 |
| `0.05` | pinned by the brief | C-CF-211 | Core features, drops rule 4 |
| `5000000` | pinned by the brief | C-CF-217 | Core features, drops rule 9 |
| `Kilnly order confirmed: ` | pinned by the brief | C-CF-232 | Core features, email rule 3 |
| `Kilnly delivery update: ` | pinned by the brief | C-CF-233 | Core features, email rule 3 |
| `Kilnly return authorised: ` | pinned by the brief | C-CF-234 | Core features, email rule 3 |
| `Kilnfolk winter drop opens Friday` | pinned by the brief | C-CF-235 | Core features, email rule 3 |
| `/` | pinned by the brief | C-UF-01 | User flow route table |
| `/catalogue` | pinned by the brief | C-UF-02 | User flow route table |
| `/merch-fulfillment` | pinned by the brief | C-UF-03 | User flow route table |
| `/custom-merch-no-minimum` | pinned by the brief | C-UF-04 | User flow route table |
| `/brand` | pinned by the brief | C-UF-05 | User flow route table |
| `/shop` | pinned by the brief | C-UF-06 | User flow route table |
| `/order/:reference` | pinned by the brief | C-UF-07 | User flow route table |
| `/holders` | pinned by the brief | C-UF-08 | User flow route table |
| `/app` | pinned by the brief | C-UF-09 | User flow route table |
| `/app/inventory` | pinned by the brief | C-UF-10 | User flow route table |
| `Inter` | pinned by the brief | C-UX-10 | UI/UX notes para 3 |
| `Baloo 2` | pinned by the brief | C-UX-11 | UI/UX notes para 3 |
| `DATABASE_URL` | pinned by the brief | C-TR-03 | Technical requirements para 1 |
| `SMTP_HOST` | pinned by the brief | C-TR-04 | Technical requirements para 1 |
| `PAYMENTS_API_URL` | pinned by the brief | C-TR-05 | Technical requirements para 1 |
| `/1.0/kb/` | pinned by the brief | C-TR-08 | Technical requirements para 3 |
| `X-Killbill-ApiKey` | pinned by the brief | C-TR-08 | Technical requirements para 3 |
| `X-Killbill-ApiSecret` | pinned by the brief | C-TR-08 | Technical requirements para 3 |
| `admin` | pinned by the brief | C-TR-09 | Technical requirements para 3 |
| `password` | pinned by the brief | C-TR-09 | Technical requirements para 3 |
| `GET /api/health` | pinned by the brief | C-TR-17 | Technical requirements, health |
| `200` | pinned by the brief | C-TR-17 | Technical requirements, health |
| `deku-demo-pw-2026` | pinned by the brief | C-DM-01 | Data model, password paragraph |
| `owner` | pinned by the brief | C-DM-04 | Data model, membership |
| `operator` | pinned by the brief | C-DM-04 | Data model, membership |
| `finance` | pinned by the brief | C-DM-04 | Data model, membership |
| `viewer` | pinned by the brief | C-DM-04 | Data model, membership |
| `apparel` | pinned by the brief | C-DM-05 | Data model, product |
| `outerwear` | pinned by the brief | C-DM-05 | Data model, product |
| `headwear` | pinned by the brief | C-DM-05 | Data model, product |
| `accessories` | pinned by the brief | C-DM-05 | Data model, product |
| `settlement` | pinned by the brief | C-DM-17 | Data model, money ledger |
| `refund` | pinned by the brief | C-DM-17 | Data model, money ledger |
| `reversal` | pinned by the brief | C-DM-17 | Data model, money ledger |
| `presale_held` | pinned by the brief | C-DM-17 | Data model, money ledger |
| `payout` | pinned by the brief | C-DM-17 | Data model, money ledger |
| `fee` | pinned by the brief | C-DM-17 | Data model, money ledger |
| `Pondering manufacturers...` | pinned by the brief | C-FE-16 | Front-end specification, intro reel |
| `Past drops` | pinned by the brief | C-FE-18 | Front-end specification, header |
| `Kilnfolk` | pinned by the brief | C-FE-18 | Front-end specification, header |
| `Whitelist` | pinned by the brief | C-FE-19 | Front-end specification, header |
| `(C) 2026 Kilnly` | pinned by the brief | C-FE-20 | Front-end specification, footer |
| `Create your dream merch on autopilot` | pinned by the brief | C-FE-27 | Front-end specification, landing bands |
| `Grow your brand, not your ops.` | pinned by the brief | C-FE-28 | Front-end specification, landing bands |
| `Find your ideal suppliers.` | pinned by the brief | C-FE-30 | Front-end specification, landing bands |
| `emailing 12 manufacturers` | pinned by the brief | C-FE-31 | Front-end specification, pill pile |
| `Latest productions` | pinned by the brief | C-FE-32 | Front-end specification, catalogue |
| `Merch fulfillment, end to end.` | pinned by the brief | C-FE-33 | Front-end specification, fulfillment |
| `11 Ops surfaces we run` | pinned by the brief | C-FE-34 | Front-end specification, fulfillment |
| `1 Minimum order` | pinned by the brief | C-FE-34 | Front-end specification, fulfillment |
| `${APP_PUBLIC_PORT}:4173` | pinned by the brief | C-DC-02 | Deployment contract bullet 1 |
| `0.0.0.0` | pinned by the brief | C-DC-09 | Deployment contract bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the container ladder's ten measures | C-FE-01 | the count is pinned, the widths are the builder's |
| the dominant breakpoint's width | C-FE-02 | named as one step with no figure given |
| the confirmation window a queue position is served inside | C-CF-190 | named as a bounded budget with no figure given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 5 | 10 |
| User roles | 5 | 31 |
| Core features | 42 | 251 |
| User flow | 6 | 18 |
| UI and UX notes | 4 | 30 |
| Technical requirements | 7 | 18 |
| Data model | 6 | 24 |
| Front-end specification | 5 | 40 |
| Constraints | 1 | 10 |
| Deployment contract | 17 | 17 |
