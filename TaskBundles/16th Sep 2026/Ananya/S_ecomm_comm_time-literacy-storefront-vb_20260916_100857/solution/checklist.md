# Checklist: Tock: Time Literacy Storefront

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 454
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` The TOCK 33 collection offers four colourways, Aqua, Navy, Fuchsia, Glow `src: Overview para 2`
- [ ] `C-OV-02` `capability` The catalogue offers watch case sizes 33 or 38 across TOCK 33 with TOCK 38 `src: Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor fills a cart without an account `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor without an account cannot place an order `src: User roles table row 1`
- [ ] `C-RL-03` `role` A customer calling an owner endpoint is denied `src: User roles authorization paragraph`
- [ ] `C-RL-04` `constraint` No account field or accounts column collects a child's name, age or birthday `src: User roles para after table`
- [ ] `C-RL-05` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: User roles seeded accounts`
- [ ] `C-RL-06` `literal` The seeded account `customer@example.com` is a customer named Casey Rivera `src: User roles seeded accounts table row 1`
- [ ] `C-RL-07` `literal` The seeded account `customer2@example.com` is a customer named Jordan Lee `src: User roles seeded accounts table row 2`
- [ ] `C-RL-08` `literal` The seeded account `owner@example.com` is the owner named Mara Ellison `src: User roles seeded accounts table row 3`
- [ ] `C-RL-09` `capability` Open signup creates a customer account for any visitor `src: User roles signup paragraph`

## C-CF Core features

- [ ] `C-CF-01` `contract` Signup returns an access token `src: Core features, Auth, para 1`
- [ ] `C-CF-02` `contract` Login with the seeded customer password returns an access token `src: Core features, Auth, para 1`
- [ ] `C-CF-03` `constraint` A signup with an already registered email is rejected without a second account row `src: Core features, Auth, rule 1`
- [ ] `C-CF-04` `constraint` A signup password shorter than 10 characters is rejected `src: Core features, Auth, rule 2`
- [ ] `C-CF-05` `constraint` A login with a wrong password is denied `src: Core features, Auth, rule 3`
- [ ] `C-CF-06` `capability` The sign-in link request answers `{"status": "sent"}` with the same body for an unknown address `src: Core features, Auth, rule 4`
- [ ] `C-CF-07` `literal` The sign-in link request sends one email with the subject `Your Tock sign-in link` `src: Core features, Auth, rule 4`
- [ ] `C-CF-08` `capability` Consuming a sign-in link for a new address returns `access_token` with `return_to`, creating a customer account `src: Core features, Auth, rule 5`
- [ ] `C-CF-09` `constraint` A consumed sign-in link is refused on second use `src: Core features, Auth, rule 6`
- [ ] `C-CF-10` `constraint` An external or protocol-relative `return_to` comes back as `/account`, a relative path unchanged `src: Core features, Auth, rule 7`
- [ ] `C-CF-11` `capability` A spent sign-in link page offers `Send a new link` `src: Core features, Auth, rule 8`
- [ ] `C-CF-12` `capability` The resend call answers `{"status": "sent"}`, mailing a fresh link to the spent token's address `src: Core features, Auth, rule 8`
- [ ] `C-CF-13` `constraint` A resend with an unissued token is rejected `src: Core features, Auth, rule 8`
- [ ] `C-CF-14` `contract` The account endpoint returns the email, name, role `src: Core features, Auth, rule 9`
- [ ] `C-CF-15` `constraint` The account patch rejects a child name or birthday field, leaving the stored name unchanged `src: Core features, Auth, rule 9`
- [ ] `C-CF-16` `constraint` Calls to account, order, checkout, review or owner endpoints without a bearer token are denied `src: Core features, Auth, rule 10`
- [ ] `C-CF-17` `capability` Selecting a tock turns the bezel by the start minute minus the tock start, times six `src: Core features, The dial demonstration, bezel tables`
- [ ] `C-CF-18` `capability` The hero dial bezel rotation stays from 0 to 359 for every tock length `src: Core features, The dial demonstration, bezel tables`
- [ ] `C-CF-19` `capability` The timer setter is a single-choice group of the options `5 min`, `10 min`, `15 min`, `30 min` `src: Core features, The dial demonstration, rule 1`
- [ ] `C-CF-20` `capability` The timer setter selects 15 min when the home page loads `src: Core features, The dial demonstration, rule 1`
- [ ] `C-CF-21` `capability` Arrow keys move the timer setter selection `src: Core features, The dial demonstration, rule 1`
- [ ] `C-CF-22` `capability` Run a tock fills the elapsed minutes up to the tock length within ten seconds `src: Core features, The dial demonstration, rule 3`
- [ ] `C-CF-23` `capability` Run a tock ends by saying `Tock complete` in a polite live region `src: Core features, The dial demonstration, rule 3`
- [ ] `C-CF-24` `capability` Under reduced motion the run completes at once `src: Core features, The dial demonstration, rule 4`
- [ ] `C-CF-25` `constraint` The demo never plays a sound `src: Core features, The dial demonstration, rule 5`
- [ ] `C-CF-26` `constraint` The demo never requests notification permission `src: Core features, The dial demonstration, rule 5`
- [ ] `C-CF-27` `capability` Pressing a colourway swatch sets the hero dial `data-colourway` to `aqua`, `navy`, `fuchsia` or `glow` `src: Core features, The dial demonstration, rule 6`
- [ ] `C-CF-28` `capability` Exactly one colourway swatch shows as pressed `src: Core features, The dial demonstration, rule 6`
- [ ] `C-CF-29` `capability` On load the Aqua swatch shows pressed with a 15 min tock set on the hero dial `src: Core features, The dial demonstration, rule 6`
- [ ] `C-CF-30` `capability` The hero dial text alternative follows `<Colourway> dial at <h:mm> with a <length> minute tock set`, updating on a change `src: Core features, The dial demonstration, rule 7`
- [ ] `C-CF-31` `capability` When the dial cannot be drawn the hero drops the setter card `src: Core features, The dial demonstration, rule 8`
- [ ] `C-CF-32` `literal` The Move the time slider runs from `0` to `719` in steps of `1`, starting at `158` `src: Core features, The dial comparison, para 1`
- [ ] `C-CF-33` `capability` Arrow keys move the comparison slider one minute `src: Core features, The dial comparison, rule 1`
- [ ] `C-CF-34` `capability` Page keys move the comparison slider one hour `src: Core features, The dial comparison, rule 1`
- [ ] `C-CF-35` `capability` Both comparison dials carry `data-hour-rotation` of `(hour mod 12) * 30 + minute * 0.5` for the slider time `src: Core features, The dial comparison, rule 2`
- [ ] `C-CF-36` `capability` The Tock dial lights the current hour zone, carrying that hour from `1` to `12` in `data-lit-hour` `src: Core features, The dial comparison, rule 3`
- [ ] `C-CF-37` `capability` The conventional dial caption reads the pinned between-hours wording for the slider time `src: Core features, The dial comparison, rule 4`
- [ ] `C-CF-38` `capability` The Tock dial caption reads the pinned in-the-hour wording for the slider time `src: Core features, The dial comparison, rule 4`
- [ ] `C-CF-39` `capability` The comparison dial text alternatives read `Conventional dial at h:mm`, `Tock dial at h:mm with the H zone lit` `src: Core features, The dial comparison, rule 5`
- [ ] `C-CF-40` `capability` The home page sections follow the stated order `src: Core features, The home page, para 1`
- [ ] `C-CF-41` `capability` The home page has one level-one heading, with the other sections opening at level two `src: Core features, The home page, para 1`
- [ ] `C-CF-42` `capability` The range eyebrows read `Premium kids' watch - From $189.00`, `The grown-up one - From $379.00`, the price being the lowest among in-stock or low-stock watches `src: Core features, The home page, rule 1`
- [ ] `C-CF-43` `capability` A sold-out range card shows Sold out without an add control `src: Core features, The home page, rule 2`
- [ ] `C-CF-44` `capability` The walkthrough stage dials show elapsed minutes 0, 15, 30 `src: Core features, The home page, rule 3`
- [ ] `C-CF-45` `capability` The testimonials disclaimer sits inside the testimonials section, reading the pinned wording `src: Core features, The home page, rule 4`
- [ ] `C-CF-46` `capability` The bundle band shows the grey aqua bundle card with an add control `src: Core features, The home page, rule 5`
- [ ] `C-CF-47` `capability` The home reassurance row shows the returns, warranty, age cells `src: Core features, The home page, rule 6`
- [ ] `C-CF-48` `capability` The pinned gift announcement bar shows on every page whenever both gift items have stock `src: Core features, The home page, rule 7`
- [ ] `C-CF-49` `capability` The announcement bar hides whenever a gift item has no stock `src: Core features, The home page, rule 7`
- [ ] `C-CF-50` `constraint` Collections list only published products `src: Core features, Catalogue and collections, rule 1`
- [ ] `C-CF-51` `literal` The all collection count is `20`, staying the unfiltered published count under an engaged filter `src: Core features, Catalogue and collections, rule 1`
- [ ] `C-CF-52` `constraint` The unpublished lilac product page, like its API, answers not found `src: Core features, Catalogue and collections, rule 1`
- [ ] `C-CF-53` `constraint` Reviews or restock requests on the unpublished lilac handle answer not found, writing no row `src: Core features, Catalogue and collections, rule 1`
- [ ] `C-CF-54` `capability` Collection filters narrow the products by family, colourway, case size, availability, price band `src: Core features, Catalogue and collections, rule 2`
- [ ] `C-CF-55` `capability` The collection page keeps engaged filters in its address `src: Core features, Catalogue and collections, rule 2`
- [ ] `C-CF-56` `constraint` An unknown collection filter or sort value is rejected naming the parameter `src: Core features, Catalogue and collections, rule 2`
- [ ] `C-CF-57` `contract` A collection response carries its eight top-level fields, with product elements carrying the listed product fields `src: Core features, Catalogue and collections, para 1`
- [ ] `C-CF-58` `capability` A single-value facet is left out unless engaged, so `/api/collections/tock-33` offers colourway with availability `src: Core features, Catalogue and collections, rule 3`
- [ ] `C-CF-59` `literal` The counts reflect value reads `all` unengaged, otherwise the engaged availability value `in_stock` or `sold_out` `src: Core features, Catalogue and collections, rule 4`
- [ ] `C-CF-60` `capability` The grid note reads `Counts include sold-out items`, `Counts show in-stock items only` or `Counts show sold-out items only` `src: Core features, Catalogue and collections, rule 4`
- [ ] `C-CF-61` `capability` The best-rated sort joins `featured`, `price-asc`, `price-desc`, `newest` only when two products shown have three or more published reviews `src: Core features, Catalogue and collections, rule 5`
- [ ] `C-CF-62` `capability` The price-asc sort orders products by price, then title `src: Core features, Catalogue and collections, rule 5`
- [ ] `C-CF-63` `capability` An empty filtered grid reads `No products match these filters.`, offering a `Clear <Filter>` control per engaged filter `src: Core features, Catalogue and collections, rule 6`
- [ ] `C-CF-64` `capability` The tock-31 collection page, like its `notice`, carries the discontinued wording `src: Core features, Catalogue and collections, rule 7`
- [ ] `C-CF-65` `capability` The filter control shows the word Filter at a narrow width `src: Core features, Catalogue and collections, rule 8`
- [ ] `C-CF-66` `capability` The sort control shows the word Sort at a narrow width `src: Core features, Catalogue and collections, rule 8`
- [ ] `C-CF-67` `capability` The density control offers `1 column`, `2 columns`, `3 columns`, `4 columns`, setting the grid column count `src: Core features, Catalogue and collections, rule 9`
- [ ] `C-CF-68` `capability` Colourway dots link to the sibling product page `src: Core features, Catalogue and collections, rule 10`
- [ ] `C-CF-69` `capability` The superseded grey copy handle redirects permanently to `/products/tock-38-grey` `src: Core features, Catalogue and collections, rule 11`
- [ ] `C-CF-70` `capability` The superseded shark handle redirects permanently to `/products/tock-38-shark` `src: Core features, Catalogue and collections, rule 11`
- [ ] `C-CF-71` `capability` Search returns published products matching the title whatever the letter case, each carrying the product fields, with the search page listing the same products `src: Core features, Catalogue and collections, rule 12`
- [ ] `C-CF-72` `capability` An empty search query returns an empty array `src: Core features, Catalogue and collections, rule 12`
- [ ] `C-CF-73` `contract` The product endpoint returns the named product fields `src: Core features, Product pages, para 1`
- [ ] `C-CF-74` `capability` Product availability reads in_stock at four or more units, low_stock at one to three, out_of_stock at none `src: Core features, Product pages, rule 1`
- [ ] `C-CF-75` `capability` A strap with sizes takes the availability of its best-stocked size `src: Core features, Product pages, rule 1`
- [ ] `C-CF-76` `constraint` A low stock page shows Only a few left, never the units count `src: Core features, Product pages, rule 1`
- [ ] `C-CF-77` `capability` The add control passes through Adding to Cart before Added to Cart `src: Core features, Product pages, rule 2`
- [ ] `C-CF-78` `capability` An out-of-stock product shows the pinned restock form instead of an add control, still showing the price `src: Core features, Product pages, rule 3`
- [ ] `C-CF-79` `capability` A sold-out strap size shows as unavailable `src: Core features, Product pages, rule 4`
- [ ] `C-CF-80` `capability` The TOCK 31 sale shows the compare-at price struck through beside a `Sale` badge with `Save $40.00` `src: Core features, Product pages, rule 5`
- [ ] `C-CF-81` `literal` The watch specification definition list headed `Specifications` lists fourteen keys in the fixed order `src: Core features, Product pages, rule 6`
- [ ] `C-CF-82` `capability` The product reassurance row carries `Swiftpost 2 day in the US` over `Flat $15`, `30 day returns` over `Any reason`, `2 year warranty` over the movement build note `src: Core features, Product pages, rule 7`
- [ ] `C-CF-83` `capability` The TOCK 33 reassurance row adds the age cell `src: Core features, Product pages, rule 7`
- [ ] `C-CF-84` `capability` The carousel position text such as `1 of 4` moves with arrow keys `src: Core features, Product pages, rule 8`
- [ ] `C-CF-85` `capability` The zoom dialog closes on Escape, returning focus `src: Core features, Product pages, rule 8`
- [ ] `C-CF-86` `literal` A watch page carries the seven editorial block headings `src: Core features, Product pages, rule 9`
- [ ] `C-CF-87` `capability` The `Related products` rail lists the family colourways `src: Core features, Product pages, rule 9`
- [ ] `C-CF-88` `constraint` A bundle owns no stock row `src: Core features, Bundles, para 1`
- [ ] `C-CF-89` `capability` Bundle availability follows the smaller watch count `src: Core features, Bundles, rule 1`
- [ ] `C-CF-90` `capability` A bundle missing a watch is unavailable, listing the missing watch title; `missing_components` stays empty for a bundle holding both watches `src: Core features, Bundles, rule 1`
- [ ] `C-CF-91` `capability` The bundle components list both watches, each carrying handle, title, availability, quantity `src: Core features, Bundles, rule 2`
- [ ] `C-CF-92` `capability` The bundle page names the missing watch with a restock form `src: Core features, Bundles, rule 3`
- [ ] `C-CF-93` `capability` The bundle compare-at price sums the watch prices, `saving` being that sum minus the bundle price `src: Core features, Bundles, rule 4`
- [ ] `C-CF-94` `literal` The black navy bundle page shows `Save $69.00` `src: Core features, Bundles, rule 4`
- [ ] `C-CF-95` `capability` The bundle buy box shows the complete-set returns notice `src: Core features, Bundles, rule 5`
- [ ] `C-CF-96` `capability` Published reviews render in the first HTML of the product page `src: Core features, Reviews and moderation, rule 1`
- [ ] `C-CF-97` `literal` The aqua review summary shows `4.1` based on 7 reviews `src: Core features, Reviews and moderation, rule 1`
- [ ] `C-CF-98` `constraint` A pending review is neither listed nor counted `src: Core features, Reviews and moderation, rule 1`
- [ ] `C-CF-99` `capability` The rating histogram maps the keys `5` down to `1` onto published review counts `src: Core features, Reviews and moderation, rule 2`
- [ ] `C-CF-100` `capability` The histogram text alternative gives the counts `src: Core features, Reviews and moderation, rule 2`
- [ ] `C-CF-101` `capability` The reviews rating filter returns only that rating, each review carrying the eight review fields `src: Core features, Reviews and moderation, rule 3`
- [ ] `C-CF-102` `capability` A histogram row links to the rating filtered page `src: Core features, Reviews and moderation, rule 3`
- [ ] `C-CF-103` `capability` A customer review is stored pending `src: Core features, Reviews and moderation, rule 4`
- [ ] `C-CF-104` `constraint` A second review of a product by one account is rejected as a duplicate `src: Core features, Reviews and moderation, rule 5`
- [ ] `C-CF-105` `constraint` A review rating outside 1 to 5 is rejected `src: Core features, Reviews and moderation, rule 5`
- [ ] `C-CF-106` `capability` The verified purchase flag follows the account order history `src: Core features, Reviews and moderation, rule 6`
- [ ] `C-CF-107` `capability` An owner publish lists the review, counting the review `src: Core features, Reviews and moderation, rule 7`
- [ ] `C-CF-108` `constraint` Publishing or rejecting a review that is not pending is rejected with the review unchanged `src: Core features, Reviews and moderation, rule 7`
- [ ] `C-CF-109` `constraint` A reject without an allowed policy clause is refused leaving the review pending, an allowed clause rejecting the review `src: Core features, Reviews and moderation, rule 8`
- [ ] `C-CF-110` `constraint` A minor review cannot publish without a basis, a non-empty basis publishing the review `src: Core features, Reviews and moderation, rule 9`
- [ ] `C-CF-111` `capability` The owner reply shows labelled Reply from Tock `src: Core features, Reviews and moderation, rule 10`
- [ ] `C-CF-112` `constraint` A second owner reply or an empty reply to one review is rejected with the first reply unchanged `src: Core features, Reviews and moderation, rule 10`
- [ ] `C-CF-113` `role` A customer owner review call is denied with the review unchanged `src: Core features, Reviews and moderation, rule 11`
- [ ] `C-CF-114` `constraint` Review title, body markup shows as text `src: Core features, Reviews and moderation, rule 12`
- [ ] `C-CF-115` `capability` A product without reviews shows No reviews yet `src: Core features, Reviews and moderation, rule 13`
- [ ] `C-CF-116` `contract` Cart create returns a cart token with `lines`, `notices`, `subtotal`, `item_count`, `hold_seconds_remaining` `src: Core features, Cart, holds and the free gifts, para 1`
- [ ] `C-CF-117` `capability` Adding a line holds stock for the cart `src: Core features, Cart, holds and the free gifts, rule 1`
- [ ] `C-CF-118` `capability` Adding the same sku raises the line quantity `src: Core features, Cart, holds and the free gifts, rule 1`
- [ ] `C-CF-119` `constraint` Adding an unpublished lilac sku or an unknown sku to a cart is rejected, holding nothing `src: Core features, Cart, holds and the free gifts, rule 1`
- [ ] `C-CF-120` `capability` Buying a tote sku beside a free tote line adds a separate paid line `src: Core features, Cart, holds and the free gifts, rule 1`
- [ ] `C-CF-121` `constraint` A line quantity outside 1 to 5 is rejected `src: Core features, Cart, holds and the free gifts, rule 2`
- [ ] `C-CF-122` `capability` A bundle line holds each watch `src: Core features, Cart, holds and the free gifts, rule 3`
- [ ] `C-CF-123` `constraint` An add exceeding availability holds nothing `src: Core features, Cart, holds and the free gifts, rule 4`
- [ ] `C-CF-124` `constraint` Concurrent adds of the last unit admit exactly one, the loser told why `src: Core features, Cart, holds and the free gifts, rule 5`
- [ ] `C-CF-125` `constraint` Held units never exceed the units on hand `src: Core features, Cart, holds and the free gifts, rule 5`
- [ ] `C-CF-126` `capability` Removing a line releases the hold `src: Core features, Cart, holds and the free gifts, rule 6`
- [ ] `C-CF-127` `capability` A watch cart carries one gift tote line with one gift beanie line, each holding one unit `src: Core features, Cart, holds and the free gifts, rule 7`
- [ ] `C-CF-128` `literal` A gift line carries `is_gift` true with the promotion `Gift with purchase` at price `0` `src: Core features, Cart, holds and the free gifts, rule 7`
- [ ] `C-CF-129` `constraint` More watches add no extra gifts `src: Core features, Cart, holds and the free gifts, rule 7`
- [ ] `C-CF-130` `constraint` A gift line patch or delete is rejected `src: Core features, Cart, holds and the free gifts, rule 8`
- [ ] `C-CF-131` `capability` Removing the last watch removes the gifts, releasing their holds, with the `promotion_removed` notice `src: Core features, Cart, holds and the free gifts, rule 9`
- [ ] `C-CF-132` `capability` A gift without stock is left out with the `gift_unavailable` notice naming that gift `src: Core features, Cart, holds and the free gifts, rule 10`
- [ ] `C-CF-133` `capability` The hold seconds remaining read `1800` or just under after a cart change, restarting the thirty minutes `src: Core features, Cart, holds and the free gifts, rule 11`
- [ ] `C-CF-134` `capability` The cart subtotal sums the non-gift lines `src: Core features, Cart, holds and the free gifts, rule 12`
- [ ] `C-CF-135` `capability` The cart item count sums non-gift quantities `src: Core features, Cart, holds and the free gifts, para 1`
- [ ] `C-CF-136` `literal` The empty cart control reads `$0.00` with `(0)` `src: Core features, Cart, holds and the free gifts, rule 12`
- [ ] `C-CF-137` `capability` A bundle cart line lists two watches `src: Core features, Cart, holds and the free gifts, rule 13`
- [ ] `C-CF-138` `capability` An anonymous checkout visit redirects to login with return_to `src: Core features, Checkout, rule 1`
- [ ] `C-CF-139` `constraint` A checkout without an idempotency key is rejected `src: Core features, Checkout, rule 2`
- [ ] `C-CF-140` `constraint` A checkout of an empty cart creates no order, raising no Kill Bill invoice `src: Core features, Checkout, rule 3`
- [ ] `C-CF-141` `constraint` A checkout country other than US is rejected `src: Core features, Checkout, rule 4`
- [ ] `C-CF-142` `constraint` A checkout missing an address field is rejected naming that field `src: Core features, Checkout, rule 4`
- [ ] `C-CF-143` `literal` The checkout answers `number`, `status`, `hold_reason`, `subtotal`, `shipping`, `total`, `currency`, `lines`, the number matching `TK-` with eight uppercase letters or digits `src: Core features, Checkout, rule 5`
- [ ] `C-CF-144` `literal` The order totals add shipping `1500` to the subtotal, TOCK 33 Aqua alone totalling `20400` `src: Core features, Checkout, rule 5`
- [ ] `C-CF-145` `capability` A bundle order line expands into two watch lines naming the bundle in parent_sku, each line carrying the six order line fields `src: Core features, Checkout, rule 5`
- [ ] `C-CF-146` `capability` Checkout converts the hold into a sale ledger entry noting the order number, lowering on hand with reserved `src: Core features, Checkout, rule 6`
- [ ] `C-CF-147` `constraint` A checked-out cart token rejects adds `src: Core features, Checkout, rule 6`
- [ ] `C-CF-148` `contract` The checkout invoice exists on the Kill Bill account keyed tock plus the lowercase account email, carrying that buyer email `src: Core features, Checkout, rule 7`
- [ ] `C-CF-149` `capability` The checkout invoice amount is the order total in USD `src: Core features, Checkout, rule 7`
- [ ] `C-CF-150` `constraint` A second order reuses the Kill Bill account with a second invoice `src: Core features, Checkout, rule 7`
- [ ] `C-CF-151` `constraint` A replayed idempotency key returns the same order with one invoice, one confirmation email `src: Core features, Checkout, rule 8`
- [ ] `C-CF-152` `constraint` A concurrent duplicate checkout produces one order, one invoice, one confirmation email, each caller receiving that same number `src: Core features, Checkout, rule 8`
- [ ] `C-CF-153` `literal` The order confirmation email subject names the order after `Tock order confirmed:` `src: Core features, Checkout, rule 9`
- [ ] `C-CF-154` `capability` The order confirmation email is addressed only to the account email `src: Core features, Checkout, rule 9`
- [ ] `C-CF-155` `capability` The order confirmation email body opens with the order number, total `src: Core features, Checkout, rule 9`
- [ ] `C-CF-156` `capability` A PO box order, in any letter case on either address line, is placed on hold with hold_reason po_box `src: Core features, Checkout, rule 10`
- [ ] `C-CF-157` `literal` A PO box order sends an email beginning `Address needed:` `src: Core features, Checkout, rule 10`
- [ ] `C-CF-158` `constraint` A street address order sends no address needed email `src: Core features, Checkout, rule 10`
- [ ] `C-CF-159` `capability` The orders endpoint returns own orders newest first, each own order readable by number `src: Core features, Checkout, rule 11`
- [ ] `C-CF-160` `constraint` A foreign order number answers 404 like a missing one `src: Core features, Checkout, rule 11`
- [ ] `C-CF-161` `role` The owner reading the seeded customer order gets 404 `src: User roles table row 3`
- [ ] `C-CF-162` `constraint` Non-order actions send no order mail `src: Core features, Checkout, rule 12`
- [ ] `C-CF-163` `capability` A restock subscription on an out-of-stock product answers `{"product": "<handle>", "email": "<email>", "status": "waiting"}` `src: Core features, Restock emails, rule 1`
- [ ] `C-CF-164` `constraint` A restock subscription on an in-stock or low-stock product is rejected `src: Core features, Restock emails, rule 1`
- [ ] `C-CF-165` `constraint` A repeat restock subscription creates no second row `src: Core features, Restock emails, rule 2`
- [ ] `C-CF-166` `contract` The owner stock rows carry sku, title, on hand, reserved, available `src: Core features, Restock emails, rule 3`
- [ ] `C-CF-167` `capability` A stock adjustment moves on hand with a ledger entry, answering sku, on hand, reserved, available `src: Core features, Restock emails, rule 4`
- [ ] `C-CF-168` `constraint` An adjustment below reserved is rejected `src: Core features, Restock emails, rule 4`
- [ ] `C-CF-169` `constraint` A zero delta or unknown sku adjustment is rejected `src: Core features, Restock emails, rule 4`
- [ ] `C-CF-170` `literal` A restock mails each waiting subscriber once with `Back in stock:` before the product title `src: Core features, Restock emails, rule 5`
- [ ] `C-CF-171` `capability` Mailed restock subscriptions become notified `src: Core features, Restock emails, rule 5`
- [ ] `C-CF-172` `constraint` An adjustment on an in-stock product sends no restock mail `src: Core features, Restock emails, rule 5`
- [ ] `C-CF-173` `role` A customer owner stock call is denied with stock unchanged `src: Core features, Restock emails, rule 6`
- [ ] `C-CF-174` `literal` The policies endpoint returns the returns window `30`, warranty `2`, minimum age `4`, flat shipping `1500`, currency `usd` `src: Core features, Content pages and shop policies, rule 1`
- [ ] `C-CF-175` `capability` Four policy surfaces state the same thirty day returns `src: Core features, Content pages and shop policies, rule 1`
- [ ] `C-CF-176` `capability` The about page ends with the indestructible close signed by the two founders `src: Core features, Content pages and shop policies, rule 2`
- [ ] `C-CF-177` `capability` The FAQ carries six anchored questions, `#service` through `#materials` `src: Core features, Content pages and shop policies, rule 3`
- [ ] `C-CF-178` `capability` The user guide carries three ordered procedures `src: Core features, Content pages and shop policies, rule 4`
- [ ] `C-CF-179` `literal` The user guide dial is set to 15 min at minute 38 with rotation `138` `src: Core features, Content pages and shop policies, rule 4`
- [ ] `C-CF-180` `capability` The shipping page headed `Shipping & Returns` carries the PO box rule `src: Core features, Content pages and shop policies, rule 5`
- [ ] `C-CF-181` `capability` The contact page shows the mailboxes `care@example.com`, `press@example.com` with the hours `src: Core features, Content pages and shop policies, rule 6`
- [ ] `C-CF-182` `capability` A support request returns an `SR-` reference with the routed queue, writing a support row `src: Core features, Content pages and shop policies, rule 7`
- [ ] `C-CF-183` `constraint` A support request with an invalid email, an unknown subject or a missing field is rejected naming the field, writing no row `src: Core features, Content pages and shop policies, rule 7`
- [ ] `C-CF-184` `capability` The footer links the privacy page on every public page `src: Core features, The public surface, rule 1`
- [ ] `C-CF-185` `capability` The footer links the terms page on every public page `src: Core features, Content pages and shop policies, rule 8`
- [ ] `C-CF-186` `capability` The privacy page states what the shop records, never a child's details, never card details `src: Core features, The public surface, rule 1`
- [ ] `C-CF-187` `capability` The sitemap lists every public route `src: Core features, The public surface, rule 2`
- [ ] `C-CF-188` `constraint` The sitemap excludes private routes, excluding any unpublished product `src: Core features, The public surface, rule 2`
- [ ] `C-CF-189` `literal` The robots file names the sitemap with `Disallow: /owner/`, `Disallow: /account`, `Disallow: /checkout`, `Disallow: /cart` `src: Core features, The public surface, rule 3`
- [ ] `C-CF-190` `capability` Every internal link on public routes resolves `src: Core features, The public surface, rule 4`
- [ ] `C-CF-191` `capability` Content images carry alternative text such as `TOCK 33 Aqua, front view` `src: Core features, The public surface, rule 5`
- [ ] `C-CF-192` `capability` At a narrow viewport the pages never scroll sideways `src: Core features, The public surface, rule 6`
- [ ] `C-CF-193` `capability` At a narrow viewport the menu reveals the navigation links `src: Core features, The public surface, rule 6`
- [ ] `C-CF-194` `capability` The owner stock page shows the stock columns `src: Core features, The owner console, para 1`
- [ ] `C-CF-195` `capability` The owner console asks for a basis before publishing a minor review `src: Core features, The owner console, para 1`
- [ ] `C-CF-196` `role` A customer opening an owner page sees not found `src: Core features, The owner console, para 1`
- [ ] `C-CF-197` `capability` An anonymous owner page visit redirects to login with return_to `src: Core features, The owner console, para 1`
- [ ] `C-CF-198` `constraint` Passwords are stored as werkzeug.security hashes, never in readable form `src: Core features, Auth, para 1`
- [ ] `C-CF-199` `capability` Email addresses sign in without regard to letter case `src: Core features, Auth, para 1`
- [ ] `C-CF-200` `constraint` A wrong-password login answers the same as an unknown email login `src: Core features, Auth, rule 3`
- [ ] `C-CF-201` `literal` The sign-in link email body opens with the `<APP_PUBLIC_URL>/account/link/<token>` link `src: Core features, Auth, rule 4`
- [ ] `C-CF-202` `capability` A customer changes their own name through the account patch, which answers the updated account `src: Core features, Auth, rule 9`
- [ ] `C-CF-203` `capability` The timer setter group is a single tab stop `src: Core features, The dial demonstration, rule 1`
- [ ] `C-CF-204` `capability` Under reduced motion selecting a tock moves the ring straight to its final turn `src: Core features, The dial demonstration, rule 4`
- [ ] `C-CF-205` `capability` The comparison readout shows the slider time as h:mm in a polite live region `src: Core features, The dial comparison, para 1`
- [ ] `C-CF-206` `capability` The best-rated sort orders products by average rating with under-three-review products after `src: Core features, Catalogue and collections, rule 5`
- [ ] `C-CF-207` `capability` The newest sort orders products by publication, newest first `src: Core features, Catalogue and collections, rule 5`
- [ ] `C-CF-208` `constraint` Every compare-at price is greater than its price `src: Core features, Product pages, rule 5`
- [ ] `C-CF-209` `capability` A product with no published reviews reads rating_average null `src: Core features, Reviews and moderation, rule 1`
- [ ] `C-CF-210` `capability` Published reviews list newest first `src: Core features, Reviews and moderation, rule 1`
- [ ] `C-CF-211` `capability` The cart follows the visitor across pages, surviving signing in `src: Core features, Cart, holds and the free gifts, para 1`
- [ ] `C-CF-212` `capability` A held reservation expires thirty minutes after the cart's last activity `src: Core features, Cart, holds and the free gifts, rule 11`
- [ ] `C-CF-213` `capability` Patching a line quantity moves the line's hold to the new quantity `src: Core features, Cart, holds and the free gifts, rule 2`
- [ ] `C-CF-214` `capability` The owner review queue shows `Reviews waiting` with Publish, Reject, Reply controls `src: Core features, The owner console, para 1`
- [ ] `C-CF-215` `capability` The owner reviews endpoint filtered by status returns reviews in that status `src: Deployment contract, API shapes`
- [ ] `C-CF-216` `constraint` A signup with a letter-case variant of a registered email is rejected `src: Core features, Auth, para 1`
- [ ] `C-CF-217` `capability` The hero price beside `Shop TOCK 33` follows the from-price rule without cents `src: Core features, The home page, rule 1`
- [ ] `C-CF-218` `constraint` Public product, collection, search responses state no unit counts `src: Core features, Product pages, rule 1`
- [ ] `C-CF-219` `constraint` A restock subscription on a bundle handle is rejected `src: Core features, Restock emails and the owner's stock, rule 1`
- [ ] `C-CF-220` `capability` A notified subscriber is mailed again after subscribing again `src: Core features, Restock emails and the owner's stock, rule 5`
- [ ] `C-CF-221` `literal` The shipping page states US-only shipping by `Swiftpost` in two days for a flat `$15` `src: Core features, Content pages and shop policies, rule 5`
- [ ] `C-CF-222` `capability` The shipping page states the bundle complete-set return rule `src: Core features, Content pages and shop policies, rule 5`
- [ ] `C-CF-223` `capability` The shipping page states the two year warranty `src: Core features, Content pages and shop policies, rule 5`
- [ ] `C-CF-224` `literal` Rejecting from the owner console asks for a `Policy clause` `src: Core features, The owner console, para 1`
- [ ] `C-CF-225` `literal` An owner stock row takes an adjustment through `Adjust by`, `Reason`, `Save adjustment` `src: Core features, The owner console, para 1`
- [ ] `C-CF-226` `capability` TOCK 33 watches carry the fourteen pinned specification values `src: Data model, Seed data`
- [ ] `C-CF-227` `capability` TOCK 38 watches differ from TOCK 33 only in the Case, Movement, Dial values `src: Data model, Seed data`
- [ ] `C-CF-228` `capability` TOCK 31 differs from TOCK 33 only in the Case value `src: Data model, Seed data`
- [ ] `C-CF-229` `capability` The bundle band card shows the grey aqua bundle price `src: Core features, The home page, rule 5`
- [ ] `C-CF-230` `capability` A collection card shows the title, price or Sold out with the rating summary `src: Core features, Catalogue and collections, para 1`
- [ ] `C-CF-231` `capability` The product carousel is a labelled group with previous, next controls `src: Core features, Product pages, rule 8`
- [ ] `C-CF-232` `capability` The zoom dialog takes focus when opened `src: Core features, Product pages, rule 8`
- [ ] `C-CF-233` `constraint` A refused checkout leaves the cart holding its units `src: Core features, Checkout, invoices and order mail, rule 4`
- [ ] `C-CF-234` `capability` The gift lines appear on the order at a price of 0 `src: Core features, Checkout, invoices and order mail, rule 5`
- [ ] `C-CF-235` `constraint` A foreign order page shows the not-found page `src: Core features, Checkout, invoices and order mail, rule 11`
- [ ] `C-CF-236` `capability` The six collections render product grids titled `TOCK 33`, `TOCK 38`, `TOCK 31`, `Bundles`, `Straps`, `Shop All` `src: Core features, Catalogue and collections, para 1`
- [ ] `C-CF-237` `capability` The in_stock availability filter includes low-stock products `src: Core features, Catalogue and collections, rule 2`
- [ ] `C-CF-238` `capability` The sold_out availability filter includes unavailable bundles `src: Core features, Catalogue and collections, rule 2`
- [ ] `C-CF-239` `capability` A known filter value matching nothing leaves the products empty without rejection `src: Core features, Catalogue and collections, rule 2`
- [ ] `C-CF-240` `contract` Each facet entry carries a value with its count `src: Core features, Catalogue and collections, rule 3`
- [ ] `C-CF-241` `capability` The price-desc sort orders products by descending price, then title `src: Core features, Catalogue and collections, rule 5`
- [ ] `C-CF-242` `capability` Sized strap pages offer a size control of `Small` with `Large` `src: Core features, Product pages, rule 4`
- [ ] `C-CF-243` `constraint` Watch, bundle, NATO strap, soft goods pages show no size control `src: Core features, Product pages, rule 4`
- [ ] `C-CF-244` `capability` The bundle page links each component watch to its own product page `src: Core features, Bundles, rule 2`
- [ ] `C-CF-245` `constraint` A rejected review is neither listed nor counted `src: Core features, Reviews and moderation, rule 1`
- [ ] `C-CF-246` `constraint` A reviewer-supplied verified purchase value never sets the flag `src: Core features, Reviews and moderation, rule 6`
- [ ] `C-CF-247` `literal` A verified review shows `Verified purchase` `src: Core features, Reviews and moderation, rule 6`
- [ ] `C-CF-248` `contract` Each cart line carries the eight cart line fields `src: Core features, Cart, holds and the free gifts, para 1`
- [ ] `C-CF-249` `capability` Removing a cart line marks the line reservation released `src: Core features, Cart, holds and the free gifts, rule 6`
- [ ] `C-CF-250` `capability` A checked-out cart row carries the checked_out status with converted reservations `src: Core features, Checkout, invoices and order mail, rule 6`
- [ ] `C-CF-251` `contract` Line add, patch, delete calls each answer the cart `src: Deployment contract, API shapes`
- [ ] `C-CF-252` `contract` Owner publish, reject, reply calls each answer the review `src: Deployment contract, API shapes`
- [ ] `C-CF-253` `capability` An account created through a sign-in link alone stores an empty password_hash `src: Data model, accounts`
- [ ] `C-CF-254` `capability` An in-stock range card shows the watch title with the watch price `src: Core features, The home page, rule 2`
- [ ] `C-CF-255` `constraint` Only the `Gift with purchase` promotion appears on a cart line `src: Constraints`
- [ ] `C-CF-256` `capability` A PO box order raises a Kill Bill invoice for the order total `src: Core features, Checkout, invoices and order mail, rule 10`
- [ ] `C-CF-257` `contract` The catalogue, cart, restock, support, policy, search endpoints answer without a bearer token `src: Deployment contract, API shapes`
- [ ] `C-CF-258` `capability` The review dialog closes on Escape, returning focus to `Write a review` `src: UI/UX notes, Components`
- [ ] `C-CF-259` `capability` The contact page support form carries the `Name`, `Email`, `Subject`, `Message` fields `src: Core features, Content pages and shop policies, rule 6`

## C-UF User flow

- [ ] `C-UF-01` `capability` An anonymous account or order visit redirects to login with return_to `src: User flow, Entry and redirects`
- [ ] `C-UF-02` `capability` A password sign-in lands on the return_to path, landing on `/account` without one `src: User flow, Entry and redirects`
- [ ] `C-UF-03` `capability` Sign out ends the session landing home `src: User flow, Entry and redirects`
- [ ] `C-UF-04` `capability` An unknown address shows the shop's own not-found page with a 404, linking back home `src: User flow, Entry and redirects`
- [ ] `C-UF-05` `capability` A visitor selects 30 min then runs the tock on the hero dial `src: User flow, Journeys, 1`
- [ ] `C-UF-06` `capability` A visitor presses Navy, turning the dial navy `src: User flow, Journeys, 2`
- [ ] `C-UF-07` `capability` A visitor moves the time slider to 3:04, reading both captions `src: User flow, Journeys, 3`
- [ ] `C-UF-08` `capability` A visitor filters TOCK 33 by In stock `src: User flow, Journeys, 4`
- [ ] `C-UF-09` `capability` A visitor finds the black navy bundle unavailable naming TOCK 33 Navy `src: User flow, Journeys, 5`
- [ ] `C-UF-10` `capability` A signed-in customer buys TOCK 33 Aqua landing on an order page with Order placed beside a `$204.00` total `src: User flow, Journeys, 6`
- [ ] `C-UF-11` `capability` A new address signs in by an emailed link landing on the account page after the sign-in link banner `src: User flow, Journeys, 7`
- [ ] `C-UF-12` `capability` A customer writes a review through `Submit review` that awaits moderation `src: User flow, Journeys, 8`
- [ ] `C-UF-13` `capability` The owner publishes Ravi's review from the moderation queue `src: User flow, Journeys, 9`
- [ ] `C-UF-14` `capability` A visitor opens the one-star reviews showing Dana's review with the reply `src: User flow, Journeys, 10`
- [ ] `C-UF-15` `capability` A visitor asks for a NATO Strap Navy restock email `src: User flow, Journeys, 11`
- [ ] `C-UF-16` `capability` A visitor sends a warranty contact form receiving a reference `src: User flow, Journeys, 12`
- [ ] `C-UF-17` `literal` An account with no orders shows `You have no orders yet.` with a link to `/collections/all` `src: User flow, States`
- [ ] `C-UF-18` `literal` An empty cart shows `Your cart is empty.` with `Continue browsing` `src: User flow, States`
- [ ] `C-UF-19` `capability` A refused action shows an inline banner naming the reason `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The page canvas is a warm bone near-white shared by the header `src: UI/UX notes, Palette`
- [ ] `C-UX-02` `ui` One soft blue carries every primary action with the section kickers `src: UI/UX notes, Palette`
- [ ] `C-UX-03` `ui` Vivid red appears only on sale prices `src: UI/UX notes, Palette`
- [ ] `C-UX-04` `ui` The header is separated from content by a hairline, never a shadow `src: UI/UX notes, Palette`
- [ ] `C-UX-05` `capability` Body text meets WCAG AA contrast against its background `src: UI/UX notes, Palette`
- [ ] `C-UX-06` `capability` Headings are set in semibold or bold Jost, body text in Cabin `src: UI/UX notes, Typography`
- [ ] `C-UX-07` `ui` The kicker is the only uppercase tracked text `src: UI/UX notes, Typography`
- [ ] `C-UX-08` `ui` Buttons are full pills `src: UI/UX notes, Shape and density`
- [ ] `C-UX-09` `capability` The cart drawer closes on Escape, returning focus `src: UI/UX notes, Components`
- [ ] `C-UX-10` `ui` Notices sit as inline banners beside the content concerned `src: UI/UX notes, Components`
- [ ] `C-UX-11` `ui` Motion starts quickly then settles softly with one shared character `src: UI/UX notes, Motion`
- [ ] `C-UX-12` `capability` Under reduced motion no decorative animation runs `src: UI/UX notes, Motion`
- [ ] `C-UX-13` `capability` A dark colour scheme preference keeps the light design `src: UI/UX notes, Mode`
- [ ] `C-UX-14` `capability` The comparison stacks on phones with the slider between the dials `src: UI/UX notes, Responsive`
- [ ] `C-UX-15` `capability` Skip to content is the first keyboard stop `src: UI/UX notes, Accessibility`
- [ ] `C-UX-16` `capability` Icon-only controls carry the hidden labels My Account, Search, Cart `src: UI/UX notes, Accessibility`
- [ ] `C-UX-17` `capability` Every page declares its language `src: UI/UX notes, Accessibility`
- [ ] `C-UX-18` `ui` A visible focus ring marks the focused control `src: UI/UX notes, Accessibility`
- [ ] `C-UX-19` `ui` Failure messages, success messages each wear a distinct meaning colour apart from the sale red `src: UI/UX notes, Palette`
- [ ] `C-UX-20` `ui` Figures align in tabular columns in the cart table `src: UI/UX notes, Typography`
- [ ] `C-UX-21` `ui` Unavailable controls show the state by more than colour alone `src: UI/UX notes, Components`
- [ ] `C-UX-22` `ui` The announcement bar is a near-black band with white text `src: UI/UX notes, Palette`
- [ ] `C-UX-23` `ui` The light-ground secondary action is a near-white, soft orange `src: UI/UX notes, Palette`
- [ ] `C-UX-24` `ui` Dark bands such as the testimonials use a near-black ground with warm bone text `src: UI/UX notes, Palette`
- [ ] `C-UX-25` `ui` Form inputs have barely rounded corners `src: UI/UX notes, Shape and density`
- [ ] `C-UX-26` `ui` The timer setter card is noticeably rounder than the review cards `src: UI/UX notes, Shape and density`
- [ ] `C-UX-27` `capability` An in-progress action shows the primary blue beside a moving indicator `src: UI/UX notes, Palette`
- [ ] `C-UX-28` `capability` At a phone width the hero stacks the dial below the copy `src: UI/UX notes, Responsive`
- [ ] `C-UX-29` `capability` At a phone width the header centres the wordmark `src: UI/UX notes, Responsive`
- [ ] `C-UX-30` `ui` Review cards are softly rounded `src: UI/UX notes, Shape and density`
- [ ] `C-UX-31` `capability` Pointing at the cart control grows a faint wash behind the icon `src: UI/UX notes, Components`
- [ ] `C-UX-32` `capability` Tock chips with colourway swatches change appearance under the pointer `src: UI/UX notes, Components`
- [ ] `C-UX-33` `capability` Keyboard navigation reaches the header controls in visual order `src: UI/UX notes, Accessibility`
- [ ] `C-UX-34` `capability` Colourway swatches with tock chips meet the 24 pixel WCAG 2.2 AA target size `src: UI/UX notes, Accessibility`
- [ ] `C-UX-35` `ui` At a phone width the hero watch face keeps legible bezel numerals `src: UI/UX notes, Responsive`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The health route answers 200 without a token `src: Technical requirements para 3`
- [ ] `C-TR-02` `contract` Product pages arrive as complete server-rendered HTML with prices, availability text, reviews `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The typefaces are served from the app's own origin `src: Technical requirements para 1`
- [ ] `C-TR-04` `constraint` A second Kill Bill account for one buyer is never created `src: Technical requirements para 4`
- [ ] `C-TR-05` `contract` API money fields are integer cents with currency usd `src: Technical requirements para 6`
- [ ] `C-TR-06` `constraint` A bundle add holds both watches or neither `src: Technical requirements para 7`
- [ ] `C-TR-07` `constraint` The order numbers, like support references, are not sequential `src: Technical requirements para 8`
- [ ] `C-TR-08` `contract` Stored timestamps are in UTC `src: Technical requirements, conventions`
- [ ] `C-TR-09` `contract` Absolute links in the sitemap, robots file, sign-in email use APP_PUBLIC_URL `src: Technical requirements, para 1`

## C-DM Data model

- [ ] `C-DM-01` `data` The accounts table stores seeded accounts by email `src: Data model, accounts`
- [ ] `C-DM-02` `data` The reserved count never exceeds on hand in inventory items, neither ever falling below zero `src: Data model, inventory_items`
- [ ] `C-DM-03` `data` The stock ledger deltas sum to on hand for every inventory item `src: Data model, stock_ledger`
- [ ] `C-DM-04` `data` The held reservations sum to the reserved count `src: Data model, reservations`
- [ ] `C-DM-05` `data` An order total equals subtotal plus shipping in the orders table `src: Data model, orders`
- [ ] `C-DM-06` `data` A bundle order line has two child watch lines priced zero `src: Data model, order_lines`
- [ ] `C-DM-07` `data` The order lines subtotal matches the stored order subtotal `src: Data model, order_lines`
- [ ] `C-DM-08` `data` The restock subscriptions table holds one waiting row per product email `src: Data model, restock_subscriptions`
- [ ] `C-DM-09` `literal` The seeded aqua product carries sku `TK33-AQUA` at price `18900` `src: Data model, Seed data`
- [ ] `C-DM-10` `data` The seeded bundles pair a TOCK 38 watch with a TOCK 33 watch `src: Data model, Seed data`
- [ ] `C-DM-11` `literal` The seeded order `TK-SEEDED01` belongs to customer2, `placed` for one NATO Strap Aqua to a US address, with one Kill Bill invoice for `37.00`, writing no ledger entry `src: Data model, Seed data`
- [ ] `C-DM-12` `data` Restarting the app duplicates no seeded rows `src: Data model, Seed data`
- [ ] `C-DM-13` `data` The seeded products carry their skus, prices, seed ledger units `src: Data model, Seed data`
- [ ] `C-DM-14` `data` The seeded units leave `bundle-black-navy`, `bundle-shark-fuchsia` unavailable, `bundle-glow-glow` low_stock, `bundle-grey-aqua` in_stock `src: Data model, Seed data`
- [ ] `C-DM-15` `data` The imported reviews carry their authors, ratings, titles, verified flags `src: Data model, Seed data`
- [ ] `C-DM-16` `literal` The seeded ratings read TOCK 38 Grey `4.5` from 2, with TOCK 33 Glow `4.7` from its three imported reviews `src: Data model, Seed data`
- [ ] `C-DM-17` `data` A product is published only with an active or discontinued status plus a published_at, TOCK 31 Mint being discontinued `src: Data model, products`
- [ ] `C-DM-18` `data` Stock ledger rows are only ever added `src: Data model, stock_ledger`
- [ ] `C-DM-19` `data` The orders table holds one order per account with idempotency key pair `src: Data model, orders`
- [ ] `C-DM-20` `data` Dana's imported review carries the pinned body with the pinned reply `src: Data model, Seed data`
- [ ] `C-DM-21` `data` The datastore holds the eighteen tables the data model names `src: Data model, para 1`
- [ ] `C-DM-22` `data` Each named table carries the columns the data model lists `src: Data model, para 1`
- [ ] `C-DM-23` `data` No column stores a derived availability, saving or rating value `src: Data model, Derived, never stored`
- [ ] `C-DM-24` `data` Product kind is one of watch, strap, bundle, accessory `src: Data model, products`
- [ ] `C-DM-25` `data` Each variant sku is present, unique across the catalogue `src: Data model, variants`
- [ ] `C-DM-26` `data` Every variant carries grams above zero `src: Data model, variants`
- [ ] `C-DM-27` `capability` The featured sort orders products by position `src: Core features, Catalogue and collections, rule 5`
- [ ] `C-DM-28` `data` Imported reviews carry an empty account_id `src: Data model, reviews`
- [ ] `C-DM-29` `data` A minor review published with a basis stores that basis in minor_basis `src: Data model, reviews`
- [ ] `C-DM-30` `data` A rejected review stores the policy clause in rejection_clause `src: Data model, reviews`

## C-FE Front-end specification

- [ ] `C-FE-01` `capability` Every dial root carries the data-dial hook with its image role, text alternative, hook attributes `src: Front-end specification, The dial's hooks`
- [ ] `C-FE-02` `ui` The plain dial draws twelve numerals with sixty minute ticks `src: Front-end specification, The dial, drawn`
- [ ] `C-FE-03` `ui` Each colourway recolours the whole dial in its own family `src: Front-end specification, The dial, drawn`
- [ ] `C-FE-04` `capability` The hero headline renders at the step 10 desktop size `src: Front-end specification, Type scale`
- [ ] `C-FE-05` `literal` The header carries the five links TOCK 33, TOCK 38, Bundles, Straps, About `src: Front-end specification, Global chrome`
- [ ] `C-FE-06` `literal` The footer carries the statement `Why Tock?` `src: Front-end specification, Global chrome`
- [ ] `C-FE-07` `ui` The hamburger keeps three bars of unequal length `src: Front-end specification, Global chrome`
- [ ] `C-FE-08` `literal` The hero carries the headline `Nobody is born knowing` over `how long fifteen minutes is.` `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-09` `literal` The comparison carries the heading `Most of a clock's day is spent between the numbers.` `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-10` `literal` The construction section carries the four specification card titles `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-11` `literal` The cart page trust row carries `Easy 30-Day Returns` `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-12` `capability` The collection grid shows up to four columns on desktop, one or two on small phones `src: Front-end specification, Layout across widths`
- [ ] `C-FE-13` `ui` Watch illustrations draw the crown on the left edge `src: Front-end specification, Imagery drawn from code`
- [ ] `C-FE-14` `ui` The drawer slides in from the right `src: Front-end specification, Motion, moment by moment`
- [ ] `C-FE-15` `capability` At a small phone width the timer setter chips wrap to two rows `src: Front-end specification, Layout across widths`
- [ ] `C-FE-16` `capability` At a phone width the cart shows stacked cards per line `src: Front-end specification, Layout across widths`
- [ ] `C-FE-17` `capability` At a phone width the sticky action bar never covers the end of the product page `src: Front-end specification, Layout across widths`
- [ ] `C-FE-18` `capability` At a phone width the footer groups fold into accordions `src: Front-end specification, Layout across widths`
- [ ] `C-FE-19` `capability` At 400 percent zoom the home page reflows to one column without sideways scrolling `src: Front-end specification, Layout across widths`
- [ ] `C-FE-20` `capability` The cart drawer keeps focus inside when open, with the page behind held still `src: Front-end specification, Global chrome`
- [ ] `C-FE-21` `ui` The cart drawer opens over a blurred, tinted underlay `src: Front-end specification, Global chrome`
- [ ] `C-FE-22` `literal` The footer carries the `Main menu` group with the `More Links` group, each with its links `src: Front-end specification, Global chrome`
- [ ] `C-FE-23` `literal` The footer cards read `Watch FAQs` with `Need Help?`, each over its line `src: Front-end specification, Global chrome`
- [ ] `C-FE-24` `capability` The drawer enters on the `slide-in` keyframes, leaving on `slide-back-out` `src: Front-end specification, Motion, moment by moment`
- [ ] `C-FE-25` `capability` Above-the-fold home headings fade up on the `heroFade` keyframes `src: Front-end specification, Motion, moment by moment`
- [ ] `C-FE-26` `capability` Jost with Cabin load under a swap font-display policy `src: Front-end specification, Type scale`
- [ ] `C-FE-27` `literal` The timer setter card carries its label, readout, `Run a tock` with `fast demo` `src: Core features, The dial demonstration, para 1`
- [ ] `C-FE-28` `literal` The hero carries its eyebrow, lede, four specification chips `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-29` `literal` The two range sections carry their headings with their lines `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-30` `literal` The comparison carries its eyebrow, lede, two card texts `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-31` `literal` The founder proof carries its kicker, pull quote, body, close `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-32` `literal` The duration walkthrough carries its overlay, three stage captions, footnote `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-33` `literal` The testimonials carry their eyebrow, heading, lede, six attributed quotes `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-34` `literal` The construction section carries its eyebrow, heading, lede, four card bodies `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-35` `literal` Product pages carry the `Materials & Care`, `Size & Fit`, `Shipping & Returns`, `Customer Reviews` blocks with the size fit text `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-36` `literal` The cart page carries `Your Cart`, its three columns, `Subtotal`, its trust rows `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-37` `literal` The checkout carries its seven address fields, its summary, `Place order` `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-38` `literal` The account page carries `Your account` with the Order, Placed, Status, Total columns `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-39` `literal` The sign-in page carries its link form, password form, `Create an account` link `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-40` `literal` The FAQ battery answer with the user guide closing step carry their pinned text `src: Front-end specification, Product, cart and content copy`
- [ ] `C-FE-41` `capability` Each range rail is a keyboard-focusable scroll region `src: Front-end specification, The home page, section by section`
- [ ] `C-FE-42` `capability` Loading the same product page twice draws the same product image `src: Front-end specification, Imagery drawn from code`
- [ ] `C-FE-43` `capability` The TOCK 33 range rail shows 1.5, 2, 3, 4 cards from small phone to desktop `src: Front-end specification, Layout across widths`
- [ ] `C-FE-44` `capability` From tablet width the header shows the full link row `src: Front-end specification, Layout across widths`
- [ ] `C-FE-45` `capability` From tablet width the hero sets the dial to the right of the copy `src: Front-end specification, Layout across widths`
- [ ] `C-FE-46` `capability` From tablet width the comparison sets the two dials side by side `src: Front-end specification, Layout across widths`
- [ ] `C-FE-47` `capability` On phones the walkthrough stacks its three stage dials `src: Front-end specification, Layout across widths`
- [ ] `C-FE-48` `capability` From tablet width the walkthrough sets its three stage dials across `src: Front-end specification, Layout across widths`
- [ ] `C-FE-49` `capability` From tablet width the buy box sits beside the product media `src: Front-end specification, Layout across widths`
- [ ] `C-FE-50` `capability` At tablet width the collection grid shows three columns `src: Front-end specification, Layout across widths`
- [ ] `C-FE-51` `ui` The drawn watch case sits on a soft, warm, low shadow `src: Front-end specification, The dial, drawn`
- [ ] `C-FE-52` `ui` A running tock fills a sector inside an outline of the whole tock, stopping at the tock end `src: Front-end specification, The dial, drawn`
- [ ] `C-FE-53` `ui` Lighting an hour swaps the zone fill with its numeral to the lit colours `src: Front-end specification, The dial, drawn`
- [ ] `C-FE-54` `ui` Numerals with hands stay legible against the zone fill in all four colourways `src: Front-end specification, The dial, drawn`
- [ ] `C-FE-55` `capability` Body text renders at 14.25px on phones, 16.15px on desktop with line height 1.5 `src: Front-end specification, Type scale`
- [ ] `C-FE-56` `capability` The header sticks to the top on scroll `src: Front-end specification, Global chrome`
- [ ] `C-FE-57` `ui` Rating stars draw fractional fills `src: Front-end specification, Global chrome`
- [ ] `C-FE-58` `ui` Each watch image draws a soft vertical ground, blurred contact shadow, gradient case, tapering straps with a faint weave, crystal highlight `src: Front-end specification, Imagery drawn from code`
- [ ] `C-FE-59` `capability` A dial root with no tock set carries an empty `data-segment-minutes` `src: Front-end specification, The dial's hooks`
- [ ] `C-FE-60` `capability` The hero lede renders at step 5: 17px on phones, 19px on tablets, 21px on desktop `src: Front-end specification, Type scale`
- [ ] `C-FE-61` `literal` Product pages carry `Read more` with `See all` `src: Front-end specification, Product, cart and content copy`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The storefront shows no pop-up overlay `src: Constraints; Overview para 4`
- [ ] `C-CN-02` `constraint` The checkout offers no discount code field `src: Constraints; Overview para 4`
- [ ] `C-CN-03` `constraint` The home page plays no video `src: Constraints; Overview para 4`
- [ ] `C-CN-04` `constraint` The checkout shows no tax or duty quote `src: Constraints`
- [ ] `C-CN-05` `constraint` The checkout offers no wallet payment button `src: Constraints`
- [ ] `C-CN-06` `constraint` The storefront offers no market, country or currency selector `src: Constraints`
- [ ] `C-CN-07` `constraint` Every catalogue price is in `usd` `src: Constraints`
- [ ] `C-CN-08` `constraint` No public page offers a newsletter signup `src: Constraints`
- [ ] `C-CN-09` `constraint` Product pages carry no recently viewed rail `src: Constraints`
- [ ] `C-CN-10` `constraint` Product pages carry no product structured data `src: Constraints`
- [ ] `C-CN-11` `constraint` No public page runs a press ticker `src: Constraints`
- [ ] `C-CN-12` `constraint` No public page offers a file upload, the review dialog included `src: Constraints`
- [ ] `C-CN-13` `constraint` An order page offers no refund action `src: Constraints`
- [ ] `C-CN-14` `constraint` The checkout carries no card or payment method field `src: Constraints`
- [ ] `C-CN-15` `constraint` Order pages offer no warranty claim, return request or tracking `src: Constraints`
- [ ] `C-CN-16` `constraint` The storefront sends no marketing email `src: Constraints`
- [ ] `C-CN-17` `constraint` No account role exists besides customer with owner `src: Constraints`
- [ ] `C-CN-18` `constraint` Product with collection pages play no video `src: Constraints`
- [ ] `C-CN-19` `constraint` No public page collects or shows a watch serial number `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at APP_PUBLIC_URL `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The container-internal port is `4173` `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served under the api prefix on the same origin `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `literal` The route `/api/health` returns 200 once ready `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The seeded logins are written to the user readme `src: Deployment contract bullet 5`
- [ ] `C-DC-06` `contract` The server outlives the session that started the process `src: Deployment contract bullet 8`
- [ ] `C-DC-07` `contract` The server binds every interface rather than loopback `src: Deployment contract bullet 9`
- [ ] `C-DC-08` `contract` List endpoints return a top-level JSON array `src: Deployment contract, API shapes`
- [ ] `C-DC-09` `contract` An invalid call is rejected as a client error, never a server error `src: Deployment contract, API shapes`
- [ ] `C-DC-10` `constraint` The cart holds live in the named datastore rather than the browser `src: Deployment contract, No mocks`
- [ ] `C-DC-11` `contract` A production server answers rather than a development server `src: Deployment contract, bullet 7`

## Declared but ungraded

Stated asks no grading channel can observe in one separate-mode run. Recorded per OPEN-DECISIONS
D-H (ISSUES D-4) and escalated to the kit owner rather than cited falsely or dropped.

- One JSON log line per request to standard output `src: Technical requirements` why: the verifier cannot read the app container's stdout
- Only the named libraries, no second database, cache, queue, object store, identity provider or mail vendor, no external network calls at runtime `src: Technical requirements; Constraints; Deployment contract` why: the verifier observes the running app, never its dependency tree, process list or egress
- `X-Killbill-CreatedBy` on every Kill Bill write `src: Technical requirements` why: reference K K.4 documents no audit-log route and the payments adapter reads invoices and accounts only
- The app starts with no manual steps, reserved `.browser_screenshots/` and `.downloads/` exist empty, no persistent volumes, fixed container names or custom networks `src: Deployment contract` why: harness deployment facts (G13, G15, G18) outside a separate-mode verifier's reach
- No native application, no automated agent checkout surface `src: Constraints` why: absences with no pinned surface to probe
- The owner queue shows `No reviews waiting.` when nothing is pending `src: Core features, The owner console` why: graded runs always leave pending fixtures, and no reset exists
- Images waiting to decode carry the `imgLoadingShimmer` placeholder `src: Front-end specification, Motion` why: a build that draws images inline never waits to decode, so a correct app can show no shimmer
- Product media shows a full-bleed carousel with dots on phones and a thumbnail rail from tablet `src: Front-end specification, Layout across widths` why: the brief pins no label or role for dots or thumbnails, so no binary observation separates them
- A lapsed hold is released after thirty idle minutes `src: Core features, Cart, rule 11` why: longer than a verifier run, and an env-injected TTL cannot reach the app under separate mode; the expiry itself is C-CF-212
- Labels run at 11.7px, 12.15px, 12.6px at weight 500 `src: Front-end specification, Type scale` why: the brief names no element class for labels, so no selector separates a label from other small text
- No child account or child profile exists, no subscription purchase, no carrier integration, no packing flow, no compliance certificates `src: Overview; User roles; Constraints` why: absences with no pinned surface or control name to probe
- The hero shows the watch illustration alone when the dial cannot be drawn `src: Core features, The dial demonstration, rule 8` why: no pinned way to make a correct build fail to draw its dial; the setter card removal is C-CF-31
- No order is placed without a Kill Bill invoice `src: Core features, Checkout, invoices and order mail, rule 7` why: Kill Bill cannot be made to fail inside one separate-mode run
- An expired sign-in link lands on the no-longer-valid page `src: User flow, Entry and redirects` why: link lifetime is unpinned, so no link can be made to expire within a run; the spent-link page is C-CF-11
- Mail credentials come from `SMTP_USER` with `SMTP_PASS`, the app hardcoding no host or port, using no edge functions, enhancing four islands with `Alpine.js` `src: Technical requirements; Deployment contract` why: environment reading, stack topology and hosting are invisible to a separate-mode verifier
- Each colourway defines the 26 named colour roles with a hand edge colour, over the pinned fifteen-step type scale, under the named easing characters `src: Front-end specification` why: internal tokens, unnamed scale steps and easing characters have no pinned DOM exposure
- Images load inside boxes that keep their shape, a media thumbnail moving its shape before its content fades in `src: User flow, States; Front-end specification, Motion` why: inline drawings never wait to decode, so a correct build shows no placeholder

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | password for every seeded account | C-RL-05 | User roles; Data model |
| `customer@example.com` | seeded customer | C-RL-06 | User roles table |
| `customer2@example.com` | second seeded customer | C-RL-07 | User roles table |
| `owner@example.com` | seeded owner | C-RL-08 | User roles table |
| `Your Tock sign-in link` | sign-in link email subject | C-CF-07 | Core features, Auth, rule 4 |
| `return_to` | sign-in return path field | C-CF-10 | Core features, Auth, rule 7 |
| `/account` | fallback return path | C-CF-10 | Core features, Auth, rule 7 |
| `0` | slider minimum, gift price | C-CF-32 | Core features, The dial comparison |
| `719` | slider maximum | C-CF-32 | Core features, The dial comparison |
| `158` | slider start value | C-CF-32 | Core features, The dial comparison |
| `20` | published product count of all | C-CF-51 | Core features, Catalogue, rule 1 |
| `in_stock` | counts reflect value | C-CF-59 | Core features, Catalogue, rule 4 |
| `sold_out` | counts reflect value | C-CF-59 | Core features, Catalogue, rule 4 |
| `Save $69.00` | black navy bundle saving | C-CF-94 | Core features, Bundles, rule 4 |
| `4.1` | aqua rating average | C-CF-97 | Core features, Reviews, rule 1 |
| `Gift with purchase` | gift line promotion | C-CF-128 | Core features, Cart, rule 7 |
| `$0.00` | empty cart total | C-CF-136 | Core features, Cart, rule 12 |
| `(0)` | empty cart count | C-CF-136 | Core features, Cart, rule 12 |
| `TK-` | order number prefix | C-CF-143 | Core features, Checkout, rule 5 |
| `1500` | flat shipping in cents | C-CF-144 | Core features, Checkout, rule 5 |
| `Tock order confirmed:` | confirmation subject prefix | C-CF-153 | Core features, Checkout, rule 9 |
| `Address needed:` | PO box email subject prefix | C-CF-157 | Core features, Checkout, rule 10 |
| `Back in stock:` | restock email subject prefix | C-CF-170 | Core features, Restock emails, rule 5 |
| `30` | returns window days | C-CF-174 | Core features, Content pages, rule 1 |
| `138` | user guide bezel rotation | C-CF-179 | Core features, Content pages, rule 4 |
| `Disallow: /owner/` | robots disallow line | C-CF-189 | Core features, The public surface, rule 3 |
| `You have no orders yet.` | empty order history copy | C-UF-17 | User flow, States |
| `Your cart is empty.` | empty cart copy | C-UF-18 | User flow, States |
| `TK33-AQUA` | aqua sku | C-DM-09 | Data model, Seed data |
| `18900` | aqua price in cents | C-DM-09 | Data model, Seed data |
| `TK-SEEDED01` | seeded order number | C-DM-11 | Data model, Seed data |
| `37.00` | seeded order invoice amount | C-DM-11 | Data model, Seed data |
| `Why Tock?` | footer statement opening | C-FE-06 | Front-end specification, Global chrome |
| `Nobody is born knowing` | hero headline first line | C-FE-08 | Front-end specification, home page |
| `Most of a clock's day is spent between the numbers.` | comparison heading | C-FE-09 | Front-end specification, home page |
| `Easy 30-Day Returns` | cart trust column heading | C-FE-11 | Front-end specification, cart copy |
| `4173` | container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `/api/health` | health route | C-DC-04 | Deployment contract bullet 3 |
| `Case, Bezel, Movement, Bezel Marquetry, Dial, Hands, Lens, Crown, Band, Buckle, Water Resistance, Theoretical Battery life, Accuracy, Warranty` | fourteen specification keys in order | C-CF-81 | Core features, Product pages, rule 6 |
| `Innovative Time System, Strap In, Lume Say What?, Case in Point, Dive! Dive! Dive!, The Swissness, Scratch That` | seven editorial headings | C-CF-86 | Core features, Product pages, rule 9 |
| `TOCK 33, TOCK 38, Bundles, Straps, About` | five header links | C-FE-05 | Front-end specification, Global chrome |
| `Sapphire crystal, 100m water resistance, Screw-down crown, Swiss ETA quartz movement` | four construction card titles | C-FE-10 | Front-end specification, home page |
| `This sign-in link is no longer valid.` | spent link page copy | C-CF-11 | Core features, Auth, rule 8 |
| `Tock complete` | run completion text | C-CF-23 | Core features, The dial demonstration, rule 3 |
| `No products match these filters.` | empty filtered grid copy | C-CF-63 | Core features, Catalogue, rule 6 |
| `Counts show in-stock items only` | grid note for in-stock counts | C-CF-60 | Core features, Catalogue, rule 4 |
| `in_stock, low_stock, out_of_stock, unavailable` | availability values | C-CF-74 | Core features, Product pages, rule 1 |
| `Thanks. Your review will appear after moderation.` | review submission copy | C-UF-12 | Core features, Reviews, rule 4 |
| `No reviews yet. Be the first to write one.` | empty reviews copy | C-CF-115 | Core features, Reviews, rule 13 |
| `promotion_removed, gift_unavailable` | cart notice kinds | C-CF-131 | Core features, Cart, rules 9 and 10 |
| `on_hold, po_box` | PO box order status and hold reason | C-CF-156 | Core features, Checkout, rule 10 |
| `SR-, orders, warranty, press, general` | support reference prefix and queues | C-CF-182 | Core features, Content pages, rule 7 |
| `tock-` | Kill Bill external key prefix | C-CF-148 | Core features, Checkout, rule 7 |
| `X-Cart-Token` | cart token header | C-CF-116 | Core features, Cart, para 1 |
| `Idempotency-Key` | checkout idempotency header | C-CF-139 | Core features, Checkout, para 1 |
| `1800` | hold seconds after a change | C-CF-133 | Core features, Cart, rule 11 |
| `Disallow: /account, Disallow: /checkout, Disallow: /cart` | robots disallow lines | C-CF-189 | Core features, The public surface, rule 3 |
| `<APP_PUBLIC_URL>/account/link/<token>` | sign-in link form | C-CF-201 | Core features, Auth, rule 4 |
| `slide-in, slide-back-out, heroFade` | named keyframes | C-FE-24 | Front-end specification, Motion |
| `Exceptional wristwatches for kids to learn time` | hero eyebrow | C-FE-28 | Front-end specification, home page |
| `TOCK 33. 33mm, a first watch for a small wrist.; TOCK 38 GMT: For older wrists featuring two time zones` | range headings | C-FE-29 | Front-end specification, home page |
| `The dial innovation; Conventional Dial; Tock Dial` | comparison eyebrow and card titles | C-FE-30 | Front-end specification, home page |
| `The co-founders first test with the prototype` | founder proof kicker | C-FE-31 | Front-end specification, home page |
| `Thirty minutes out. Fifteen gone. Half the tock still to run.` | walkthrough overlay | C-FE-32 | Front-end specification, home page |
| `What owners tell us; TIME CONFIDENCE - knowing how much longer.` | testimonials eyebrow and heading | C-FE-33 | Front-end specification, home page |
| `How it's built; Kids' watches usually fail at the bit you look through.` | construction eyebrow and heading | C-FE-34 | Front-end specification, home page |
| `Full name; Address line 1; Address line 2; City; State; ZIP code; Country; Place order` | checkout labels | C-FE-37 | Front-end specification, checkout copy |
| `Your account; Order; Placed; Status; Total` | account copy | C-FE-38 | Front-end specification, account copy |
| `Sign in; Email me a sign-in link; Send link; Create an account` | sign-in copy | C-FE-39 | Front-end specification, sign-in copy |
| `Up to 10 years..... Why isn't this exact?` | FAQ battery answer opening | C-FE-40 | Front-end specification, content copy |
| `Disallow: /account` | copy pinned for C-CF-189 | C-CF-189 | Core features, The public surface, rule 3 |
| `Disallow: /checkout` | copy pinned for C-CF-189 | C-CF-189 | Core features, The public surface, rule 3 |
| `Disallow: /cart` | copy pinned for C-CF-189 | C-CF-189 | Core features, The public surface, rule 3 |
| `4.5` | copy pinned for C-DM-16 | C-DM-16 | Data model, Seed data |
| `4.7` | copy pinned for C-DM-16 | C-DM-16 | Data model, Seed data |
| `Main menu` | copy pinned for C-FE-22 | C-FE-22 | Front-end specification, Global chrome |
| `More Links` | copy pinned for C-FE-22 | C-FE-22 | Front-end specification, Global chrome |
| `Watch FAQs` | copy pinned for C-FE-23 | C-FE-23 | Front-end specification, Global chrome |
| `Need Help?` | copy pinned for C-FE-23 | C-FE-23 | Front-end specification, Global chrome |
| `Run a tock` | copy pinned for C-FE-27 | C-FE-27 | Core features, The dial demonstration, para 1 |
| `fast demo` | copy pinned for C-FE-27 | C-FE-27 | Core features, The dial demonstration, para 1 |
| `Your Cart` | copy pinned for C-FE-36 | C-FE-36 | Front-end specification, Product, cart and content copy |
| `Subtotal` | copy pinned for C-FE-36 | C-FE-36 | Front-end specification, Product, cart and content copy |
| `Place order` | copy pinned for C-FE-37 | C-FE-37 | Front-end specification, Product, cart and content copy |
| `Your account` | copy pinned for C-FE-38 | C-FE-38 | Front-end specification, Product, cart and content copy |
| `Create an account` | copy pinned for C-FE-39 | C-FE-39 | Front-end specification, Product, cart and content copy |
| `Normal dials have the hour hand between two numerals for most of the hour.` | comparison lede opening | C-FE-30 | Front-end specification, home page |
| `"We're like...halfway there."` | founder proof pull quote | C-FE-31 | Front-end specification, home page |
| `You say a number, your child turns the ring to the start of that tock` | founder proof close opening | C-FE-31 | Front-end specification, home page |
| `We built Tock for the car, the countdown and the bedtime negotiation.` | testimonials lede opening | C-FE-33 | Front-end specification, home page |
| `Read the reviews under any children's watch and the same complaint comes back` | construction lede opening | C-FE-34 | Front-end specification, home page |
| `Mohs 9 on the hardness scale.` | construction card body opening | C-FE-34 | Front-end specification, home page |
| `Shop TOCK 33` | hero primary action | C-CF-217 | Core features, The home page, rule 1 |
| `Materials & Care` | product page block heading | C-FE-35 | Front-end specification, Product, cart and content copy |
| `Size & Fit` | product page block heading | C-FE-35 | Front-end specification, Product, cart and content copy |
| `Shipping & Returns` | product page block heading | C-FE-35 | Front-end specification, Product, cart and content copy |
| `Customer Reviews` | product page block heading | C-FE-35 | Front-end specification, Product, cart and content copy |
| `Swiftpost` | copy pinned for C-CF-221 | C-CF-221 | Core features, Content pages and shop policies, rule 5 |
| `$15` | copy pinned for C-CF-221 | C-CF-221 | Core features, Content pages and shop policies, rule 5 |
| `Policy clause` | copy pinned for C-CF-224 | C-CF-224 | Core features, The owner console, para 1 |
| `Adjust by` | copy pinned for C-CF-225 | C-CF-225 | Core features, The owner console, para 1 |
| `Reason` | copy pinned for C-CF-225 | C-CF-225 | Core features, The owner console, para 1 |
| `Save adjustment` | copy pinned for C-CF-225 | C-CF-225 | Core features, The owner console, para 1 |
| `/collections/all` | copy pinned for C-UF-17 | C-UF-17 | User flow, States |
| `Continue browsing` | copy pinned for C-UF-18 | C-UF-18 | User flow, States |
| `Home` | footer Main menu link | C-FE-22 | Front-end specification |
| `Shop All` | footer Main menu link | C-FE-22 | Front-end specification |
| `Contact` | footer Main menu link | C-FE-22 | Front-end specification |
| `Search` | footer More Links link | C-FE-22 | Front-end specification |
| `Terms of Use` | footer More Links link | C-FE-22 | Front-end specification |
| `Privacy` | footer More Links link | C-FE-22 | Front-end specification |
| `Shipping and Returns` | footer More Links link | C-FE-22 | Front-end specification |
| `User Guide` | footer More Links link | C-FE-22 | Front-end specification |
| `Your questions, answered.` | Watch FAQs footer card line | C-FE-23 | Front-end specification |
| `Email us at care@example.com` | Need Help? footer card line | C-FE-23 | Front-end specification |
| `Try it. Set a tock and watch closely` | timer setter card label | C-FE-27 | Front-end specification |
| `Price` | cart column | C-FE-36 | Front-end specification |
| `Quantity` | cart column | C-FE-36 | Front-end specification |
| `Total` | cart column | C-FE-36 | Front-end specification |
| `Somewhere between 2 and 3?` | conventional dial caption at 2:38 | C-CF-37 | Core features, The dial comparison, rule 4 |
| `It's in the 2. 2:38.` | Tock dial caption at 2:38 | C-CF-38 | Core features, The dial comparison, rule 4 |
| `BUY ANY TOCK, GET A TOTE AND BEANIE FOR FREE` | announcement bar copy | C-CF-48 | Core features, The home page, rule 7 |
| `Email me when it is back` | restock form copy | C-CF-78 | Core features, Product pages, rule 3 |
| `Mara and Joel Ellison` | about page signature | C-CF-176 | Core features, Content pages and shop policies, rule 2 |
| `Why Tock? We believe time management is a superpower and the tradition of analog is worth preserving.` | footer statement | C-FE-06 | Front-end specification, Global chrome |
| `We will email you when NATO Strap Navy is back.` | restock confirmation copy | C-CF-163 | Core features, Product pages, rule 3 |
| `1` | copy pinned for C-CF-32 | C-CF-32 | Core features, The dial comparison, para 1 |
| `all` | copy pinned for C-CF-59 | C-CF-59 | Core features, Catalogue and collections, rule 4 |
| `Specifications` | copy pinned for C-CF-81 | C-CF-81 | Core features, Product pages, rule 6 |
| `is_gift` | copy pinned for C-CF-128 | C-CF-128 | Core features, Cart, holds and the free gifts, rule 7 |
| `number` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `status` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `hold_reason` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `subtotal` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `shipping` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `total` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `currency` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `lines` | copy pinned for C-CF-143 | C-CF-143 | Core features, Checkout, rule 5 |
| `20400` | copy pinned for C-CF-144 | C-CF-144 | Core features, Checkout, rule 5 |
| `2` | copy pinned for C-CF-174 | C-CF-174 | Core features, Content pages and shop policies, rule 1 |
| `4` | copy pinned for C-CF-174 | C-CF-174 | Core features, Content pages and shop policies, rule 1 |
| `usd` | copy pinned for C-CF-174 | C-CF-174 | Core features, Content pages and shop policies, rule 1 |
| `Verified purchase` | copy pinned for C-CF-247 | C-CF-247 | Core features, Reviews and moderation, rule 6 |
| `placed` | copy pinned for C-DM-11 | C-DM-11 | Data model, Seed data |
| `how long fifteen minutes is.` | copy pinned for C-FE-08 | C-FE-08 | Front-end specification, The home page, section by section |
| `Read more` | copy pinned for C-FE-61 | C-FE-61 | Front-end specification, Product, cart and content copy |
| `See all` | copy pinned for C-FE-61 | C-FE-61 | Front-end specification, Product, cart and content copy |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 9 | 9 |
| Core features | 259 | 259 |
| User flow | 19 | 19 |
| UI and UX notes | 35 | 35 |
| Technical requirements | 9 | 9 |
| Data model | 30 | 30 |
| Front-end specification | 61 | 61 |
| Constraints | 19 | 19 |
| Deployment contract | 11 | 11 |
