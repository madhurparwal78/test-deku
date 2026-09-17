# Checklist: Curated Box Subscription

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, constraints, deployment
Sections absent: buildplan, frontend
Items: 307
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app reveals six or seven editions at the opening of each monthly cycle. `src: Overview para 2`
- [ ] `C-OV-02` `capability` The app lets a member build a box from the revealed editions. `src: Overview para 2`
- [ ] `C-OV-03` `constraint` The app limits a box to three editions. `src: Overview para 2`
- [ ] `C-OV-04` `constraint` The app requires at least one edition from the current month in a placed box. `src: Overview para 2`
- [ ] `C-OV-05` `constraint` The app keeps every edition addable rather than disabling ineligible ones. `src: Overview para 6`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor browses the home reveal. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor browses the catalogue. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor buys a gift subscription. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A signed-out visitor redeems a gift code. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` The app denies a signed-out visitor any box action. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A signed-in member builds a box of their own. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A signed-in member reads their own credit ledger. `src: User roles table row 2`
- [ ] `C-RL-08` `constraint` The app denies one member a read of another member's box. `src: User roles table row 2`
- [ ] `C-RL-09` `constraint` The app denies one member a read of another member's order. `src: User roles table row 2`
- [ ] `C-RL-10` `constraint` The app enforces authorization server-side on every mutating endpoint. `src: User roles para 2`
- [ ] `C-RL-11` `constraint` The app leaves protected state unchanged after a denied request. `src: User roles para 2`
- [ ] `C-RL-12` `capability` The app opens signup to anybody. `src: User roles para 3`
- [ ] `C-RL-13` `literal` The app seeds an account `member@example.com` in country `US`. `src: User roles table of accounts`
- [ ] `C-RL-14` `literal` The app seeds an account `member2@example.com` in country `CA`. `src: User roles table of accounts`
- [ ] `C-RL-15` `literal` The app seeds an account `member3@example.com` in country `US`. `src: User roles table of accounts`

## C-CF Core features

- [ ] `C-CF-01` `literal` The app accepts an email with a password at `/api/auth/login`. `src: Core features, Auth`
- [ ] `C-CF-02` `capability` The app issues a bearer token at login. `src: Core features, Auth`
- [ ] `C-CF-03` `constraint` The app accepts only a country of `US` or `CA` at signup. `src: Core features, Auth`
- [ ] `C-CF-04` `literal` The app opens a cycle at `00:00:00` UTC on the first of the month. `src: Core features, The monthly cycle rule 1`
- [ ] `C-CF-05` `capability` The app closes a cycle at the opening of the next cycle. `src: Core features, The monthly cycle rule 1`
- [ ] `C-CF-06` `capability` The app applies one cycle instant to every member in every country. `src: Core features, The monthly cycle rule 1`
- [ ] `C-CF-07` `constraint` The app makes a cycle's editions current together rather than singly. `src: Core features, The monthly cycle rule 2`
- [ ] `C-CF-08` `constraint` The app never exposes a partial reveal by any route. `src: Core features, The monthly cycle rule 2`
- [ ] `C-CF-09` `constraint` The app changes nothing when a reveal is applied a second time. `src: Core features, The monthly cycle rule 3`
- [ ] `C-CF-10` `constraint` The app duplicates no edition when a reveal is applied a second time. `src: Core features, The monthly cycle rule 3`
- [ ] `C-CF-11` `literal` The app lists every orderable edition at `/allbooks`. `src: Core features, The catalogue rule 1`
- [ ] `C-CF-12` `capability` The app filters the catalogue by genre. `src: Core features, The catalogue rule 1`
- [ ] `C-CF-13` `literal` The app offers the browse genre `Gothic Fiction`. `src: Core features, The catalogue rule 1`
- [ ] `C-CF-14` `literal` The app treats `and more!` as copy rather than a filterable genre. `src: Core features, The catalogue rule 1`
- [ ] `C-CF-15` `constraint` The app keeps the edition tag list flat. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-16` `literal` The app carries the tag `Includes a Dog`. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-17` `literal` The app carries the tag `Includes a Cat`. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-18` `literal` The app carries the tag `Award Worthy`. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-19` `literal` The app carries the tag `LGBTQIA+`. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-20` `literal` The app carries the tag `Pangolin Original`. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-21` `capability` The app renders every tag identically whatever the tag's kind. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-22` `capability` The app stores a kind on each tag for filtering. `src: Core features, The catalogue rule 2`
- [ ] `C-CF-23` `literal` The app serves an edition page at `/books/` followed by the edition slug. `src: Core features, The catalogue rule 3`
- [ ] `C-CF-24` `capability` The app shows a ribbon on an edition marked as a special edition. `src: Core features, The catalogue rule 3`
- [ ] `C-CF-25` `constraint` The app treats `salt-and-static-reprint` as a record distinct from `salt-and-static`. `src: Core features, The catalogue rule 4`
- [ ] `C-CF-26` `constraint` The app assigns each box to exactly one cycle. `src: Core features, The box rule 1`
- [ ] `C-CF-27` `constraint` The app places a box only when the box holds three editions at most. `src: Core features, The box rule 2`
- [ ] `C-CF-28` `constraint` The app places a box only when at least one edition belongs to the box's own cycle. `src: Core features, The box rule 2`
- [ ] `C-CF-29` `constraint` The app evaluates box validity at placement rather than at each addition. `src: Core features, The box rule 2`
- [ ] `C-CF-30` `constraint` The app disables no control because an addition would leave a box invalid. `src: Core features, The box rule 3`
- [ ] `C-CF-31` `capability` The app restates the reason a box may not be placed after each change. `src: Core features, The box rule 3`
- [ ] `C-CF-32` `capability` The app states the incomplete-box notice for a box holding no current-cycle edition. `src: Core features, The box rule 4`
- [ ] `C-CF-33` `literal` The app states `Three books is the limit. Remove one to add another.` for a fourth addition. `src: Core features, The box rule 5`
- [ ] `C-CF-34` `constraint` The app leaves a box unchanged after a refused fourth addition. `src: Core features, The box rule 5`
- [ ] `C-CF-35` `constraint` The app adds no edition twice to one box. `src: Core features, The box rule 6`
- [ ] `C-CF-36` `constraint` The app refuses a box holding only `salt-and-static-reprint` from outside the current cycle. `src: Core features, The box rule 7`
- [ ] `C-CF-37` `capability` The app pre-seeds a box from slugs given in the query of `/box`. `src: Core features, The box rule 8`
- [ ] `C-CF-38` `capability` The app reads pre-seeded slugs in the order given. `src: Core features, The box rule 8`
- [ ] `C-CF-39` `constraint` The app drops a pre-seeded slug naming an edition that is not orderable. `src: Core features, The box rule 8`
- [ ] `C-CF-40` `constraint` The app keeps at most the first three surviving pre-seeded slugs. `src: Core features, The box rule 8`
- [ ] `C-CF-41` `capability` The app tells a member which pre-seeded slugs were dropped. `src: Core features, The box rule 8`
- [ ] `C-CF-42` `constraint` The app creates no second order when one box is submitted twice. `src: Core features, The box rule 9`
- [ ] `C-CF-43` `constraint` The app creates no second invoice when one box is submitted twice. `src: Core features, The box rule 9`
- [ ] `C-CF-44` `capability` The app ships a box already placed when a membership is cancelled. `src: Core features, The box rule 10`
- [ ] `C-CF-45` `constraint` The app offers one membership rather than a table of plans. `src: Core features, Pricing rule 1`
- [ ] `C-CF-46` `literal` The app stores a `US` base of `1799` in `usd`. `src: Core features, Pricing rule 2`
- [ ] `C-CF-47` `literal` The app stores a `US` extra-book charge of `1099`. `src: Core features, Pricing rule 2`
- [ ] `C-CF-48` `literal` The app stores a `CA` base of `2599` in `cad`. `src: Core features, Pricing rule 2`
- [ ] `C-CF-49` `literal` The app stores a `CA` extra-book charge of `1599`. `src: Core features, Pricing rule 2`
- [ ] `C-CF-50` `capability` The app computes every total from a stored base with a stored extra charge. `src: Core features, Pricing rule 1`
- [ ] `C-CF-51` `literal` The app totals a two-book `US` box at `2898`. `src: Core features, Pricing rule 3`
- [ ] `C-CF-52` `literal` The app totals a three-book `US` box at `3997`. `src: Core features, Pricing rule 3`
- [ ] `C-CF-53` `literal` The app totals a two-book `CA` box at `4198`. `src: Core features, Pricing rule 3`
- [ ] `C-CF-54` `literal` The app totals a three-book `CA` box at `5797`. `src: Core features, Pricing rule 3`
- [ ] `C-CF-55` `literal` The app banks one credit with reason `unchosen_cycle` when a paid cycle closes unchosen. `src: Core features, Pricing rule 4`
- [ ] `C-CF-56` `constraint` The app banks at most one unchosen-cycle credit per member per cycle. `src: Core features, Pricing rule 4`
- [ ] `C-CF-57` `capability` The app stores on each placed box the base charge that applied at placement. `src: Core features, Pricing rule 5`
- [ ] `C-CF-58` `constraint` The app leaves an agreed total unmoved by a later pricing change. `src: Core features, Pricing rule 5`
- [ ] `C-CF-59` `literal` The app replaces the base charge with `400` under the code `SUMMER`. `src: Core features, The promotion rule 1`
- [ ] `C-CF-60` `constraint` The app accepts `SUMMER` on a member's first order only. `src: Core features, The promotion rule 1`
- [ ] `C-CF-61` `constraint` The app accepts `SUMMER` from a `US` member only. `src: Core features, The promotion rule 1`
- [ ] `C-CF-62` `literal` The app totals a first three-book `US` box under `SUMMER` at `2598`. `src: Core features, The promotion rule 2`
- [ ] `C-CF-63` `literal` The app states `That code is for USA orders only.` to a `CA` member entering `SUMMER`. `src: Core features, The promotion rule 3`
- [ ] `C-CF-64` `constraint` The app leaves a box unchanged after a refused promotional code. `src: Core features, The promotion rule 4`
- [ ] `C-CF-65` `capability` The app keeps a credit ledger separate from the monthly entitlement. `src: Core features, Credits rule 1`
- [ ] `C-CF-66` `literal` The app records a credit earned from a postcard challenge with reason `postcard_challenge`. `src: Core features, Credits rule 1`
- [ ] `C-CF-67` `capability` The app removes the charge for one book per credit applied. `src: Core features, Credits rule 2`
- [ ] `C-CF-68` `constraint` The app applies a credit to the base charge before any extra-book charge. `src: Core features, Credits rule 2`
- [ ] `C-CF-69` `literal` The app totals a three-book `US` box with one credit at `2198`. `src: Core features, Credits rule 3`
- [ ] `C-CF-70` `literal` The app states `One free credit applied. You have` with the remaining balance. `src: Core features, Credits rule 4`
- [ ] `C-CF-71` `constraint` The app lets no member spend more credits than the member's balance. `src: Core features, Credits rule 5`
- [ ] `C-CF-72` `capability` The app derives a credit balance from the sum of ledger entries. `src: Core features, Credits rule 5`
- [ ] `C-CF-73` `constraint` The app refuses a credit offered on an order already carrying a promotional code. `src: Core features, Credits rule 6`
- [ ] `C-CF-74` `constraint` The app writes no credit ledger entry when an order does not complete. `src: Core features, Credits rule 7`
- [ ] `C-CF-75` `capability` The app creates an order carrying the computed total at placement. `src: Core features, Placing the box rule 1`
- [ ] `C-CF-76` `capability` The app lands a member on a confirmation route naming the order. `src: Core features, Placing the box rule 1`
- [ ] `C-CF-77` `capability` The app creates an invoice in `killbill` for the computed total. `src: Core features, Placing the box rule 2`
- [ ] `C-CF-78` `constraint` The app substitutes no local record for an invoice in `killbill`. `src: Core features, Placing the box rule 2`
- [ ] `C-CF-79` `literal` The app sends the header `X-Killbill-ApiKey` set to `orbit-labs` on every tenant call. `src: Core features, Placing the box rule 3`
- [ ] `C-CF-80` `literal` The app sends the header `X-Killbill-ApiSecret` set to `orbit-labs-secret-9f14c73e` on every tenant call. `src: Core features, Placing the box rule 3`
- [ ] `C-CF-81` `constraint` The app creates one billing account per member however often signup is submitted. `src: Core features, Placing the box rule 4`
- [ ] `C-CF-82` `literal` The app records a three-book `US` order in billing as `39.97` in `USD`. `src: Core features, Placing the box rule 5`
- [ ] `C-CF-83` `constraint` The app leaves no order row behind after a failed placement. `src: Core features, Placing the box rule 6`
- [ ] `C-CF-84` `constraint` The app moves no box to `placed` after a failed placement. `src: Core features, Placing the box rule 6`
- [ ] `C-CF-85` `capability` The app sends one message over SMTP when a box becomes placed. `src: Core features, The confirmation email rule 1`
- [ ] `C-CF-86` `constraint` The app addresses the confirmation message to the placing member alone. `src: Core features, The confirmation email rule 1`
- [ ] `C-CF-87` `constraint` The app sets no cc on the confirmation message. `src: Core features, The confirmation email rule 1`
- [ ] `C-CF-88` `constraint` The app sets no bcc on the confirmation message. `src: Core features, The confirmation email rule 1`
- [ ] `C-CF-89` `literal` The app begins the confirmation subject with `Box confirmed: `. `src: Core features, The confirmation email rule 2`
- [ ] `C-CF-90` `capability` The app names every title of the box in the confirmation body. `src: Core features, The confirmation email rule 3`
- [ ] `C-CF-91` `constraint` The app sends no message when an edition is added to a box. `src: Core features, The confirmation email rule 4`
- [ ] `C-CF-92` `constraint` The app sends no message when a box placement is refused. `src: Core features, The confirmation email rule 4`
- [ ] `C-CF-93` `capability` The app issues a gift code to the buyer at purchase. `src: Core features, Gift subscriptions rule 1`
- [ ] `C-CF-94` `literal` The app begins the gift subject with `Your e-gift card: `. `src: Core features, Gift subscriptions rule 1`
- [ ] `C-CF-95` `capability` The app names the gift code in the gift message body. `src: Core features, Gift subscriptions rule 1`
- [ ] `C-CF-96` `capability` The app lets any holder of a gift code redeem the code. `src: Core features, Gift subscriptions rule 2`
- [ ] `C-CF-97` `constraint` The app creates a membership only at redemption of a gift. `src: Core features, Gift subscriptions rule 3`
- [ ] `C-CF-98` `constraint` The app denies a gift buyer a read of the recipient's box. `src: Core features, Gift subscriptions rule 4`
- [ ] `C-CF-99` `constraint` The app redeems a gift code at most once. `src: Core features, Gift subscriptions rule 5`
- [ ] `C-CF-100` `constraint` The app refuses redemption of a gift code by the code's purchaser. `src: Core features, Gift subscriptions rule 6`
- [ ] `C-CF-101` `constraint` The app extends an existing membership when a member redeems a gift. `src: Core features, Gift subscriptions rule 7`
- [ ] `C-CF-102` `constraint` The app produces exactly one winner per vote round. `src: Core features, The annual vote rule 1`
- [ ] `C-CF-103` `constraint` The app accepts one ballot per member per vote round. `src: Core features, The annual vote rule 2`
- [ ] `C-CF-104` `constraint` The app leaves a first ballot unchanged after a refused second ballot. `src: Core features, The annual vote rule 2`
- [ ] `C-CF-105` `literal` The app states `Voting closes` with the closing date on the ballot page. `src: Core features, The annual vote rule 3`
- [ ] `C-CF-106` `constraint` The app records a vote winner as a new orderable edition. `src: Core features, The annual vote rule 4`
- [ ] `C-CF-107` `capability` The app carries an author portrait on a vote-winner edition. `src: Core features, The annual vote rule 4`
- [ ] `C-CF-108` `capability` The app shows the forthcoming round as a placeholder beside past winners. `src: Core features, The annual vote rule 5`
- [ ] `C-CF-109` `capability` The app recognises a Puerto Rico address at address entry. `src: Core features, Addresses rule 1`
- [ ] `C-CF-110` `capability` The app recognises an APO or FPO address at address entry. `src: Core features, Addresses rule 1`
- [ ] `C-CF-111` `capability` The app recognises a PO box address at address entry. `src: Core features, Addresses rule 1`
- [ ] `C-CF-112` `capability` The app states the special-address notice for an address outside the ordinary flow. `src: Core features, Addresses rule 1`
- [ ] `C-CF-113` `constraint` The app identifies an unservable address before payment. `src: Core features, Addresses rule 2`
- [ ] `C-CF-114` `literal` The app publishes `the-pangolin-anthology` with the club as publisher. `src: Core features, The exclusive title`
- [ ] `C-CF-115` `literal` The app serves every question at `/faq`. `src: Core features, The supporting surfaces rule 1`
- [ ] `C-CF-116` `capability` The app surfaces three questions on the home page. `src: Core features, The supporting surfaces rule 1`
- [ ] `C-CF-117` `literal` The app serves the gifting copy `No spying on shelves needed.` at `/gifting`. `src: Core features, The supporting surfaces rule 2`
- [ ] `C-CF-118` `literal` The app serves a privacy page at `/privacy-policy`. `src: Core features, The supporting surfaces rule 3`
- [ ] `C-CF-119` `capability` The app links the privacy page from the footer of every page. `src: Core features, The supporting surfaces rule 3`
- [ ] `C-CF-120` `capability` The app states on the privacy page what the club records about a member. `src: Core features, The supporting surfaces rule 3`
- [ ] `C-CF-121` `literal` The app shows `Thank you, you joined us!` on a successful mailing-list submission. `src: Core features, The supporting surfaces rule 4`
- [ ] `C-CF-122` `capability` The app shows the mailing-list failure notice on a failed submission. `src: Core features, The supporting surfaces rule 4`
- [ ] `C-CF-123` `literal` The app serves a terms page at `/terms-of-service`. `src: Core features, The supporting surfaces rule 4`
- [ ] `C-CF-124` `literal` The app shows the join band copy `Want to join the Club?`. `src: Core features, The supporting surfaces rule 5`
- [ ] `C-CF-125` `constraint` The app renders the join band from one component rather than repeated copies. `src: Core features, The supporting surfaces rule 5`
- [ ] `C-CF-126` `capability` The app asks a first-time visitor once about non-essential cookies. `src: Core features, The supporting surfaces rule 6`
- [ ] `C-CF-127` `capability` The app remembers a cookie answer across a reload. `src: Core features, The supporting surfaces rule 6`
- [ ] `C-CF-128` `constraint` The app asks no returning visitor about cookies a second time in one browser. `src: Core features, The supporting surfaces rule 6`
- [ ] `C-CF-129` `constraint` The app rejects invalid form input before writing any record. `src: Core features, The supporting surfaces rule 7`
- [ ] `C-CF-130` `capability` The app names the offending field beside a rejected form input. `src: Core features, The supporting surfaces rule 7`
- [ ] `C-CF-131` `constraint` The app leaves no record behind after a rejected form submission. `src: Core features, The supporting surfaces rule 7`
- [ ] `C-CF-132` `capability` The app opens a new empty box for the cycle once a box is placed. `src: Core features, The box rule 11`

## C-UF User flow

- [ ] `C-UF-01` `literal` The app serves the home reveal at `/`. `src: User flow route table row 1`
- [ ] `C-UF-02` `literal` The app serves the gifting page at `/gifting` to a signed-out visitor. `src: User flow route table row 4`
- [ ] `C-UF-03` `literal` The app serves the signup page at `/signup`. `src: User flow route table row 7`
- [ ] `C-UF-04` `literal` The app serves the sign-in page at `/login`. `src: User flow route table row 8`
- [ ] `C-UF-05` `literal` The app serves the redemption page at `/redeem`. `src: User flow route table row 9`
- [ ] `C-UF-06` `literal` The app serves the box builder at `/box` to a member. `src: User flow route table row 10`
- [ ] `C-UF-07` `literal` The app serves the account page at `/account` to a member. `src: User flow route table row 12`
- [ ] `C-UF-08` `literal` The app serves the ballot at `/vote` to a member. `src: User flow route table row 13`
- [ ] `C-UF-09` `capability` The app redirects a signed-out visitor from a member route to the sign-in page. `src: User flow, Entry and redirects`
- [ ] `C-UF-10` `capability` The app preserves a destination across a sign-in redirect. `src: User flow, Entry and redirects`
- [ ] `C-UF-11` `capability` The app lands a member on the box builder after a sign-in with no destination. `src: User flow, Entry and redirects`
- [ ] `C-UF-12` `capability` The app returns a visitor to the home page after signing out. `src: User flow, Entry and redirects`
- [ ] `C-UF-13` `constraint` The app denies a member another member's confirmation route rather than redirecting. `src: User flow, Entry and redirects`
- [ ] `C-UF-14` `capability` The app shows an empty state on a genre filter matching no edition. `src: User flow, States`
- [ ] `C-UF-15` `capability` The app shows the composition rule on an empty box. `src: User flow, States`
- [ ] `C-UF-16` `capability` The app shows an empty state on an account with no orders. `src: User flow, States`
- [ ] `C-UF-17` `capability` The app shows a loading state on every route. `src: User flow, States`
- [ ] `C-UF-18` `constraint` The app leaves a page standing after a rejected action. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app grounds every page in white. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-02` `literal` The app carries a brand mark in a `light, vivid violet`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-03` `literal` The app carries a brand mark in a `mid, vivid teal`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-04` `literal` The app fills the primary button with a `light, soft amber`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-05` `literal` The app fills the alternate button with a `mid, vivid magenta`. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-06` `constraint` The app wears the primary fill on the primary action alone. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-07` `ui` The app gives failure, success, in-progress each a distinct meaning colour. `src: UI/UX notes, Palette by role`
- [ ] `C-UX-08` `ui` The app pairs each FAQ hue with a solid variant for the closed panel. `src: UI/UX notes, The FAQ palette`
- [ ] `C-UX-09` `ui` The app pairs each FAQ hue with a soft variant for the open panel. `src: UI/UX notes, The FAQ palette`
- [ ] `C-UX-10` `ui` The app keeps a question's hue identity across the open change. `src: UI/UX notes, The FAQ palette`
- [ ] `C-UX-11` `literal` The app sets headings in `Recoleta`. `src: UI/UX notes, Typography`
- [ ] `C-UX-12` `literal` The app sets read text in `Public Sans`. `src: UI/UX notes, Typography`
- [ ] `C-UX-13` `literal` The app sets the handwritten accent in `Caveat`. `src: UI/UX notes, Typography`
- [ ] `C-UX-14` `ui` The app scales content type fluidly between a minimum with a maximum. `src: UI/UX notes, Typography`
- [ ] `C-UX-15` `ui` The app holds interface labels at a fixed size. `src: UI/UX notes, Typography`
- [ ] `C-UX-16` `ui` The app shapes the primary button as a full pill. `src: UI/UX notes, Shape`
- [ ] `C-UX-17` `ui` The app shapes the alternate button with a small radius. `src: UI/UX notes, Shape`
- [ ] `C-UX-18` `ui` The app spaces pages generously rather than densely. `src: UI/UX notes, Density`
- [ ] `C-UX-19` `ui` The app floats a pill group of navigation items over the content. `src: UI/UX notes, Layout`
- [ ] `C-UX-20` `ui` The app shows the catalogue beside the box in the builder. `src: UI/UX notes, Layout`
- [ ] `C-UX-21` `ui` The app derives a card's background colour from the card's own cover. `src: UI/UX notes, The card`
- [ ] `C-UX-22` `ui` The app offsets carousel cards vertically from one another. `src: UI/UX notes, The card`
- [ ] `C-UX-23` `ui` The app overshoots motion with a visible settle. `src: UI/UX notes, Motion character`
- [ ] `C-UX-24` `ui` The app squashes a pressed button more than the button narrows. `src: UI/UX notes, Motion character`
- [ ] `C-UX-25` `ui` The app animates the two mascot ears on two different clocks. `src: UI/UX notes, Motion character`
- [ ] `C-UX-26` `constraint` The app mirrors neither mascot ear onto the other. `src: UI/UX notes, Motion character`
- [ ] `C-UX-27` `ui` The app moves page content upward in both navigation directions. `src: UI/UX notes, Motion character`
- [ ] `C-UX-28` `constraint` The app declares transitions per property rather than as a blanket rule. `src: UI/UX notes, Motion character`
- [ ] `C-UX-29` `constraint` The app holds the mascot ears still under reduced motion. `src: UI/UX notes, Reduced motion`
- [ ] `C-UX-30` `ui` The app replaces page transitions with a plain cross-fade under reduced motion. `src: UI/UX notes, Reduced motion`
- [ ] `C-UX-31` `constraint` The app gates a hover effect on a precise pointer being present. `src: UI/UX notes, Reduced motion`
- [ ] `C-UX-32` `constraint` The app gates a hover effect on no reduced-motion preference. `src: UI/UX notes, Reduced motion`
- [ ] `C-UX-33` `ui` The app collapses the header to a mark with a menu control at the narrowest width. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-34` `ui` The app aligns carousel card offsets at the narrowest width. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-35` `constraint` The app overflows nothing sideways at a narrow viewport. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-36` `constraint` The app keeps every navigation target reachable at a narrow viewport. `src: UI/UX notes, Responsive behaviour`
- [ ] `C-UX-37` `constraint` The app meets the WCAG AA contrast bar on body text. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-38` `constraint` The app shows a visible focus ring on every keyboard-reachable control. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-39` `constraint` The app labels every icon-only control. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-40` `constraint` The app carries no meaning by colour alone. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-41` `ui` The app disables a carousel arrow at the end of the row rather than hiding the arrow. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-42` `ui` The app announces the position within the carousel row. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-43` `ui` The app makes each carousel card one link. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-44` `constraint` The app carries no meaning on a tag's colour. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-45` `ui` The app carries a text alternative for the scroll sequence. `src: UI/UX notes, Accessibility floors`
- [ ] `C-UX-46` `ui` The app dims no title in the box builder. `src: UI/UX notes, Layout`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app renders complete HTML on the server for every route. `src: Technical requirements para 1`
- [ ] `C-TR-02` `literal` The app reads its datastore location from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The app reads its billing location from `PAYMENTS_API_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The app reads its mail host from `SMTP_HOST`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` The app reads its mail port from `SMTP_PORT`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The app authenticates the JSON API with bearer tokens. `src: Technical requirements para 1`
- [ ] `C-TR-07` `constraint` The app settles box validity on the server whatever the browser shows. `src: Technical requirements para 4`
- [ ] `C-TR-08` `contract` The app declares a social preview title on every public route. `src: Technical requirements para 5`
- [ ] `C-TR-09` `contract` The app declares a social preview image resolving to real bytes. `src: Technical requirements para 5`
- [ ] `C-TR-10` `constraint` The app declares no preview title shared by two public routes. `src: Technical requirements para 5`

## C-DM Data model

- [ ] `C-DM-01` `data` The app stores every timestamp in UTC. `src: Data model para 1`
- [ ] `C-DM-02` `literal` The app accepts `deku-demo-pw-2026` at login for every seeded account. `src: Data model, password paragraph`
- [ ] `C-DM-03` `data` The app keeps a unique email per member. `src: Data model, members`
- [ ] `C-DM-04` `data` The app derives a member's credit balance from the ledger rather than storing the balance. `src: Data model, members`
- [ ] `C-DM-05` `data` The app moves a subscription to `paused` after a failed payment. `src: Data model, subscriptions`
- [ ] `C-DM-06` `constraint` The app deletes no account after a failed payment. `src: Data model, subscriptions`
- [ ] `C-DM-07` `data` The app ends a cancelled membership at the close of the paid cycle. `src: Data model, subscriptions`
- [ ] `C-DM-08` `constraint` The app keeps exactly one cycle current at any instant. `src: Data model, cycles`
- [ ] `C-DM-09` `data` The app assigns a box the cycle current at the box's creation. `src: Data model, cycles`
- [ ] `C-DM-10` `data` The app keeps a unique slug per edition. `src: Data model, editions`
- [ ] `C-DM-11` `constraint` The app assigns each edition at most one cycle. `src: Data model, editions`
- [ ] `C-DM-12` `data` The app derives an edition's cover hue once at creation. `src: Data model, editions`
- [ ] `C-DM-13` `constraint` The app returns one unchanging cover hue across repeated reads of one edition. `src: Data model, editions`
- [ ] `C-DM-14` `data` The app sets an author portrait only on a vote-winner edition. `src: Data model, editions`
- [ ] `C-DM-15` `constraint` The app keeps at most one box in `building` per member per cycle. `src: Data model, boxes`
- [ ] `C-DM-16` `constraint` The app stores at most three item rows per box. `src: Data model, box_items`
- [ ] `C-DM-17` `constraint` The app produces at most one order per box. `src: Data model, orders`
- [ ] `C-DM-18` `literal` The app records a credit spend with reason `spent_on_order`. `src: Data model, credit_ledger`
- [ ] `C-DM-19` `constraint` The app keeps a credit balance at zero or above. `src: Data model, credit_ledger`
- [ ] `C-DM-20` `constraint` The app writes at most one unchosen-cycle ledger entry per member per cycle. `src: Data model, credit_ledger`
- [ ] `C-DM-21` `data` The app keeps a unique gift code. `src: Data model, gifts`
- [ ] `C-DM-22` `data` The app stores a base charge per country in one place. `src: Data model, country_pricing`
- [ ] `C-DM-23` `constraint` The app accepts at most one ballot per member per round. `src: Data model, ballots`
- [ ] `C-DM-24` `constraint` The app accepts exactly one of two simultaneous ballots by one member in one round. `src: Data model, concurrency invariants`
- [ ] `C-DM-25` `constraint` The app produces exactly one order under two simultaneous placements of one box. `src: Data model, concurrency invariants`
- [ ] `C-DM-26` `constraint` The app leaves exactly one invoice after two simultaneous placements of one box. `src: Data model, concurrency invariants`
- [ ] `C-DM-27` `constraint` The app refuses both of two simultaneous additions of a fourth edition. `src: Data model, concurrency invariants`
- [ ] `C-DM-28` `constraint` The app succeeds at most once across two simultaneous redemptions of one gift code. `src: Data model, concurrency invariants`
- [ ] `C-DM-29` `constraint` The app duplicates no row when the app restarts. `src: Data model, seed data`
- [ ] `C-DM-30` `literal` The app seeds an edition `the-orrery-thief` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-31` `literal` The app seeds an edition `salt-and-static` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-32` `literal` The app seeds an edition `a-quiet-inventory` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-33` `literal` The app seeds an edition `every-third-tuesday` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-34` `literal` The app seeds an edition `nine-yards-of-night` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-35` `literal` The app seeds an edition `the-lamplighters-daughter` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-36` `literal` The app seeds an edition `the-marmalade-conspiracy` into the current cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-37` `literal` The app seeds an edition `the-glass-cartographer` into the previous cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-38` `literal` The app seeds an edition `feral-arithmetic` into the previous cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-39` `literal` The app seeds an edition `salt-and-static-reprint` outside every cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-40` `literal` The app seeds an edition `saltmarsh-2024-members-choice-winner` outside every cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-41` `literal` The app seeds an edition `the-paper-wife-2025-members-choice-winner` outside every cycle. `src: Data model, seed data edition table`
- [ ] `C-DM-42` `constraint` The app shares one work row between `salt-and-static` with `salt-and-static-reprint`. `src: Data model, seed data`
- [ ] `C-DM-43` `literal` The app seeds an unredeemed gift code `PANGOLIN-GIFT-7K42`. `src: Data model, seed data`
- [ ] `C-DM-44` `literal` The app seeds an account `reader@example.com` as the gift recipient address used in the journeys. `src: User flow, journey 5`
- [ ] `C-DM-45` `data` The app seeds six FAQ entries, one per hue, in order. `src: Data model, seed data`
- [ ] `C-DM-46` `data` The app seeds four press mentions. `src: Data model, seed data`
- [ ] `C-DM-47` `data` The app seeds one open vote round for the current UTC year. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app offers one membership tier only. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The app offers no country beyond `US` with `CA` at signup. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The app ships no native mobile application. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The app serves the marketing pages from the same origin as the box builder. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` The app offers no comments. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The app offers no member profiles. `src: Constraints bullet 5`
- [ ] `C-CN-07` `constraint` The app offers no reviews. `src: Constraints bullet 5`
- [ ] `C-CN-08` `constraint` The app integrates no carrier for parcel tracking. `src: Constraints bullet 6`
- [ ] `C-CN-09` `constraint` The app exposes no refund flow to a member. `src: Constraints bullet 7`
- [ ] `C-CN-10` `constraint` The app reproduces no real book title. `src: Constraints bullet 8`
- [ ] `C-CN-11` `constraint` The app offers no recommendation engine. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app reads its public address from `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app listens on container-internal port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app reads its outside port from `APP_PUBLIC_PORT`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The app serves the HTTP API under the `/api` prefix on the same origin. `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` The app serves `/api/health` with status `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `contract` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-08` `literal` The app accepts an email with a password at `/api/auth/signup`. `src: Deployment contract, API shapes row 1`
- [ ] `C-DC-09` `literal` The app returns the current cycle at `/api/cycles/current`. `src: Deployment contract, API shapes row 4`
- [ ] `C-DC-10` `literal` The app returns a top-level JSON array of editions at `/api/editions`. `src: Deployment contract, API shapes row 5`
- [ ] `C-DC-11` `literal` The app returns the member's box at `/api/box`. `src: Deployment contract, API shapes row 7`
- [ ] `C-DC-12` `literal` The app adds an edition to the box at `/api/box/items`. `src: Deployment contract, API shapes row 8`
- [ ] `C-DC-13` `literal` The app places the box at `/api/box/place`. `src: Deployment contract, API shapes row 10`
- [ ] `C-DC-14` `literal` The app returns a top-level JSON array of the member's orders at `/api/orders`. `src: Deployment contract, API shapes row 11`
- [ ] `C-DC-15` `literal` The app returns the balance with the ledger at `/api/credits`. `src: Deployment contract, API shapes row 12`
- [ ] `C-DC-16` `literal` The app issues a gift at `/api/gifts`. `src: Deployment contract, API shapes row 13`
- [ ] `C-DC-17` `literal` The app redeems a gift at `/api/gifts/redeem`. `src: Deployment contract, API shapes row 14`
- [ ] `C-DC-18` `literal` The app records a ballot at `/api/vote`. `src: Deployment contract, API shapes row 16`
- [ ] `C-DC-19` `literal` The app screens an address at `/api/addresses/check`. `src: Deployment contract, API shapes row 17`
- [ ] `C-DC-20` `constraint` The app rejects an invalid call as a client error rather than a server error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-21` `constraint` The app requires bearer auth on every endpoint outside signup, login, health. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-22` `constraint` The app keeps no in-memory stand-in for a billing invoice. `src: Deployment contract, No mocks`
- [ ] `C-DC-23` `literal` The app cancels a membership at `/api/account/cancel`. `src: Deployment contract, API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `member@example.com` | seeded member, country US | C-RL-13 | User roles, accounts table |
| `member2@example.com` | seeded member, country CA | C-RL-14 | User roles, accounts table |
| `member3@example.com` | seeded member, country US | C-RL-15 | User roles, accounts table |
| `reader@example.com` | gift recipient used in the journeys | C-DM-44 | User flow, journey 5 |
| `deku-demo-pw-2026` | password for every seeded account | C-DM-02 | Data model, password paragraph |
| `US` | country code, United States | C-RL-13 | User roles, accounts table |
| `CA` | country code, Canada | C-RL-14 | User roles, accounts table |
| `1799` | US base charge, minor units | C-CF-46 | Core features, Pricing rule 2 |
| `1099` | US extra-book charge, minor units | C-CF-47 | Core features, Pricing rule 2 |
| `2599` | CA base charge, minor units | C-CF-48 | Core features, Pricing rule 2 |
| `1599` | CA extra-book charge, minor units | C-CF-49 | Core features, Pricing rule 2 |
| `usd` | US currency code | C-CF-46 | Core features, Pricing rule 2 |
| `cad` | CA currency code | C-CF-48 | Core features, Pricing rule 2 |
| `2898` | two-book US total | C-CF-51 | Core features, Pricing rule 3 |
| `3997` | three-book US total | C-CF-52 | Core features, Pricing rule 3 |
| `4198` | two-book CA total | C-CF-53 | Core features, Pricing rule 3 |
| `5797` | three-book CA total | C-CF-54 | Core features, Pricing rule 3 |
| `400` | promotional base charge | C-CF-59 | Core features, The promotion rule 1 |
| `2598` | three-book US total under the promotion | C-CF-62 | Core features, The promotion rule 2 |
| `2198` | three-book US total with one credit | C-CF-69 | Core features, Credits rule 3 |
| `39.97` | three-book US invoice amount as billing reports it | C-CF-82 | Core features, Placing the box rule 5 |
| `USD` | invoice currency as billing reports it | C-CF-82 | Core features, Placing the box rule 5 |
| `SUMMER` | promotional code | C-CF-59 | Core features, The promotion rule 1 |
| `PANGOLIN-GIFT-7K42` | seeded unredeemed gift code | C-DM-43 | Data model, seed data |
| `unchosen_cycle` | credit reason, unchosen paid cycle | C-CF-55 | Core features, Pricing rule 4 |
| `postcard_challenge` | credit reason, postcard challenge | C-CF-66 | Core features, Credits rule 1 |
| `spent_on_order` | credit reason, spend | C-DM-18 | Data model, credit_ledger |
| `placed` | box state after a successful placement | C-CF-84 | Core features, Placing the box rule 6 |
| `building` | box state before placement | C-DM-15 | Data model, boxes |
| `paused` | subscription state after a failed payment | C-DM-05 | Data model, subscriptions |
| `Includes a Dog` | edition tag | C-CF-16 | Core features, The catalogue rule 2 |
| `Includes a Cat` | edition tag | C-CF-17 | Core features, The catalogue rule 2 |
| `Award Worthy` | edition tag | C-CF-18 | Core features, The catalogue rule 2 |
| `LGBTQIA+` | edition tag | C-CF-19 | Core features, The catalogue rule 2 |
| `Pangolin Original` | edition tag | C-CF-20 | Core features, The catalogue rule 2 |
| `Gothic Fiction` | browse genre | C-CF-13 | Core features, The catalogue rule 1 |
| `and more!` | catalogue copy, never a genre | C-CF-14 | Core features, The catalogue rule 1 |
| `the-orrery-thief` | seeded current-cycle edition | C-DM-30 | Data model, seed data |
| `salt-and-static` | seeded current-cycle edition | C-DM-31 | Data model, seed data |
| `a-quiet-inventory` | seeded current-cycle edition | C-DM-32 | Data model, seed data |
| `every-third-tuesday` | seeded current-cycle edition | C-DM-33 | Data model, seed data |
| `nine-yards-of-night` | seeded current-cycle edition | C-DM-34 | Data model, seed data |
| `the-lamplighters-daughter` | seeded current-cycle edition | C-DM-35 | Data model, seed data |
| `the-marmalade-conspiracy` | seeded current-cycle edition | C-DM-36 | Data model, seed data |
| `the-glass-cartographer` | seeded previous-cycle edition | C-DM-37 | Data model, seed data |
| `feral-arithmetic` | seeded previous-cycle edition | C-DM-38 | Data model, seed data |
| `salt-and-static-reprint` | seeded reprint edition, no cycle | C-DM-39 | Data model, seed data |
| `saltmarsh-2024-members-choice-winner` | seeded vote-winner edition | C-DM-40 | Data model, seed data |
| `the-paper-wife-2025-members-choice-winner` | seeded vote-winner edition | C-DM-41 | Data model, seed data |
| `the-pangolin-anthology` | club-published edition | C-CF-114 | Core features, The exclusive title |
| `Box confirmed: ` | confirmation subject prefix | C-CF-89 | Core features, The confirmation email rule 2 |
| `Your e-gift card: ` | gift subject prefix | C-CF-94 | Core features, Gift subscriptions rule 1 |
| `Add at least one book from this month to complete your box.` | invalid-box copy | C-CF-32 | Core features, The box rule 4 |
| `Three books is the limit. Remove one to add another.` | full-box copy | C-CF-33 | Core features, The box rule 5 |
| `That code is for USA orders only.` | rejected-code copy | C-CF-63 | Core features, The promotion rule 3 |
| `This month's selections closed on the 1st. Here's what's new.` | cutoff copy | C-CF-15 | Core features, The monthly cycle rule 4 |
| `One free credit applied. You have` | credit-applied copy | C-CF-70 | Core features, Credits rule 4 |
| `We ship there, but we'll need to set it up by hand.` | special-address copy | C-CF-112 | Core features, Addresses rule 1 |
| `Voting closes` | vote-closing copy | C-CF-105 | Core features, The annual vote rule 3 |
| `Thank you, you joined us!` | mailing-list success copy | C-CF-121 | Core features, The supporting surfaces rule 4 |
| `Oops! Something went wrong while submitting the form.` | mailing-list failure copy | C-CF-122 | Core features, The supporting surfaces rule 4 |
| `Want to join the Club?` | join band copy | C-CF-124 | Core features, The supporting surfaces rule 5 |
| `No spying on shelves needed.` | gifting copy | C-CF-117 | Core features, The supporting surfaces rule 2 |
| `killbill` | billing provider slug | C-CF-77 | Core features, Placing the box rule 2 |
| `orbit-labs` | billing tenant api key | C-CF-79 | Core features, Placing the box rule 3 |
| `orbit-labs-secret-9f14c73e` | billing tenant api secret | C-CF-80 | Core features, Placing the box rule 3 |
| `X-Killbill-ApiKey` | billing tenant key header | C-CF-79 | Core features, Placing the box rule 3 |
| `X-Killbill-ApiSecret` | billing tenant secret header | C-CF-80 | Core features, Placing the box rule 3 |
| `/1.0/healthcheck` | billing liveness probe | C-CF-88 | Core features, Placing the box rule 3 |
| `DATABASE_URL` | datastore location variable | C-TR-02 | Technical requirements para 1 |
| `PAYMENTS_API_URL` | billing location variable | C-TR-03 | Technical requirements para 1 |
| `SMTP_HOST` | mail host variable | C-TR-04 | Technical requirements para 1 |
| `SMTP_PORT` | mail port variable | C-TR-05 | Technical requirements para 1 |
| `APP_PUBLIC_URL` | public address variable | C-DC-01 | Deployment contract bullet 1 |
| `APP_PUBLIC_PORT` | outside port variable | C-DC-03 | Deployment contract bullet 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `200` | health status | C-DC-05 | Deployment contract bullet 3 |
| `0.0.0.0` | bind address | C-DC-07 | Deployment contract bullet 9 |
| `/api` | API prefix | C-DC-04 | Deployment contract bullet 2 |
| `/api/health` | health route | C-DC-05 | Deployment contract bullet 3 |
| `/api/auth/login` | sign-in endpoint | C-CF-01 | Core features, Auth |
| `/api/auth/signup` | signup endpoint | C-DC-08 | Deployment contract, API shapes |
| `/api/cycles/current` | current cycle endpoint | C-DC-09 | Deployment contract, API shapes |
| `/api/editions` | editions endpoint | C-DC-10 | Deployment contract, API shapes |
| `/api/box` | box endpoint | C-DC-11 | Deployment contract, API shapes |
| `/api/box/items` | box item endpoint | C-DC-12 | Deployment contract, API shapes |
| `/api/box/place` | placement endpoint | C-DC-13 | Deployment contract, API shapes |
| `/api/orders` | orders endpoint | C-DC-14 | Deployment contract, API shapes |
| `/api/credits` | credits endpoint | C-DC-15 | Deployment contract, API shapes |
| `/api/gifts` | gift issue endpoint | C-DC-16 | Deployment contract, API shapes |
| `/api/gifts/redeem` | gift redemption endpoint | C-DC-17 | Deployment contract, API shapes |
| `/api/vote` | ballot endpoint | C-DC-18 | Deployment contract, API shapes |
| `/api/addresses/check` | address screening endpoint | C-DC-19 | Deployment contract, API shapes |
| `/api/account/cancel` | cancellation endpoint | C-DC-23 | Deployment contract, API shapes |
| `/` | home route | C-UF-01 | User flow route table |
| `/allbooks` | catalogue route | C-CF-11 | Core features, The catalogue rule 1 |
| `/books/` | edition route prefix | C-CF-23 | Core features, The catalogue rule 3 |
| `/gifting` | gifting route | C-UF-02 | User flow route table |
| `/faq` | FAQ route | C-CF-115 | Core features, The supporting surfaces rule 1 |
| `/privacy-policy` | privacy route | C-CF-118 | Core features, The supporting surfaces rule 3 |
| `/terms-of-service` | terms route | C-CF-123 | Core features, The supporting surfaces rule 4 |
| `/signup` | signup route | C-UF-03 | User flow route table |
| `/login` | sign-in route | C-UF-04 | User flow route table |
| `/redeem` | redemption route | C-UF-05 | User flow route table |
| `/box` | box builder route | C-UF-06 | User flow route table |
| `/account` | account route | C-UF-07 | User flow route table |
| `/vote` | ballot route | C-UF-08 | User flow route table |
| `/app/USER_README.md` | credential file path | C-DC-07 | Deployment contract bullet 5 |
| `.browser_screenshots/` | reserved directory | C-DC-08 | Deployment contract bullet 6 |
| `.downloads/` | reserved directory | C-DC-09 | Deployment contract bullet 6 |
| `00:00:00` | cycle opening instant | C-CF-04 | Core features, The monthly cycle rule 1 |
| `light, vivid violet` | brand mark colour words | C-UX-02 | UI/UX notes, Palette by role |
| `mid, vivid teal` | brand mark colour words | C-UX-03 | UI/UX notes, Palette by role |
| `light, soft amber` | primary button fill words | C-UX-04 | UI/UX notes, Palette by role |
| `mid, vivid magenta` | alternate button fill words | C-UX-05 | UI/UX notes, Palette by role |
| `Recoleta` | display family | C-UX-11 | UI/UX notes, Typography |
| `Public Sans` | interface family | C-UX-12 | UI/UX notes, Typography |
| `Caveat` | handwritten accent family | C-UX-13 | UI/UX notes, Typography |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the cycle label used in the confirmation subject | C-CF-89 | derived from the current month, so no fixed string is given |
| the gift code issued at purchase | C-CF-93 | generated per purchase, so only the seeded code is a fixed value |
| the closing date shown beside the voting copy | C-CF-105 | derived from the open round, sixty days after first start |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 5 |
| User roles | 1 | 15 |
| Core features | 21 | 132 |
| User flow | 7 | 18 |
| UI and UX notes | 4 | 46 |
| Technical requirements | 5 | 10 |
| Data model | 13 | 47 |
| Constraints | 3 | 11 |
| Deployment contract | 9 | 23 |
