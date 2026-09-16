# Checklist: VOLARI Official

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract
Sections absent: buildplan
Items: 615
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The product is the public storefront of a one-operator watch seller. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The site holds one body of content, the catalogue, with one action, a purchase. `src: Overview para 1`
- [ ] `C-OV-03` `ui` The struck-through original appears on every card, on every product page, in the cart. `src: Overview para 2`
- [ ] `C-OV-04` `ui` The star row sits above the price rather than below. `src: Overview para 2`
- [ ] `C-OV-05` `ui` Seven reassurance devices repeat across the top, under the hero, under the buy control, in the footer, inside the cart. `src: Overview para 2`
- [ ] `C-OV-06` `constraint` No user-generated content ships, no on-site review composer. `src: Overview para 3`
- [ ] `C-OV-07` `constraint` Star ratings are read-only. `src: Overview para 3`
- [ ] `C-OV-08` `constraint` No infinite scroll ships; a collection pages by numbered controls. `src: Overview para 3`
- [ ] `C-OV-09` `constraint` The account area is a sign-in handoff, with nothing behind that handoff in the build. `src: Overview para 3`
- [ ] `C-OV-10` `constraint` The chrome holds a route of one viewport, a route of eleven screens, with no minimum height stranding the footer. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` One anonymous role named customer exists. `src: User roles table`
- [ ] `C-RL-02` `role` A customer reads every storefront route without signing in. `src: User roles table`
- [ ] `C-RL-03` `role` A customer filters a collection, sorts a collection, opens a product. `src: User roles table`
- [ ] `C-RL-04` `role` A customer selects a colourway, sets a quantity, adjusts a cart. `src: User roles table`
- [ ] `C-RL-05` `role` A customer applies a discount code, chooses a display currency. `src: User roles table`
- [ ] `C-RL-06` `role` A customer completes a checkout as a guest. `src: User roles table`
- [ ] `C-RL-07` `role` A customer cannot create a product, a variant, a collection or a page. `src: User roles table`
- [ ] `C-RL-08` `role` A customer cannot change a product, a variant, a collection or a page. `src: User roles table`
- [ ] `C-RL-09` `role` A customer cannot delete a product, a variant, a collection or a page. `src: User roles table`
- [ ] `C-RL-10` `constraint` The storefront carries no sign-up form, no session, no user token, no logged-in state. `src: User roles para 2`
- [ ] `C-RL-11` `contract` The file at /app/USER_README.md states in plain words that the application has no credentials. `src: User roles para 2`
- [ ] `C-RL-12` `role` A request that would write to the catalogue is refused by the server as an invalid request. `src: User roles para 3`
- [ ] `C-RL-13` `role` A refused catalogue write leaves the stored row unchanged. `src: User roles para 3`
- [ ] `C-RL-14` `role` A catalogue write answered with a server error is a failure. `src: User roles para 3`
- [ ] `C-RL-15` `capability` A guest cart merges into the account cart on signing in, never discarded. `src: User roles para 4`
- [ ] `C-RL-16` `capability` The storefront is usable, completable, without an account. `src: User roles para 4`

## C-CF Core features

- [ ] `C-CF-01` `capability` The cart is one piece of session state projected into five surfaces. `src: Core features, the cart rule 1`
- [ ] `C-CF-02` `constraint` No cart surface fetches the cart independently. `src: Core features, the cart rule 1`
- [ ] `C-CF-03` `data` The cart object carries token, currency, lines, unit_count, subtotal, note, discount_code. `src: Core features, the cart rule 2`
- [ ] `C-CF-04` `data` Each cart line carries key, variant_id, handle, title, maker, option_name, option_value, image, unit_price, compare_at, quantity, line_total, removable. `src: Core features, the cart rule 2`
- [ ] `C-CF-05` `constraint` The removable flag is false only for a line a promotion owns. `src: Core features, the cart rule 2`
- [ ] `C-CF-06` `constraint` The unit count is the sum of quantities, never the count of lines. `src: Core features, the cart rule 3`
- [ ] `C-CF-07` `literal` Three lines totalling four units make the badge read 4. `src: Core features, the cart rule 3`
- [ ] `C-CF-08` `constraint` The line key is its own value rather than the variant identifier. `src: Core features, the cart rule 4`
- [ ] `C-CF-09` `contract` Every cart mutation returns the whole cart rather than a delta. `src: Core features, the cart rule 5`
- [ ] `C-CF-10` `capability` Adding appends or increments, then opens the drawer. `src: Core features, the cart rule 5`
- [ ] `C-CF-11` `capability` A cart permalink merges into the existing cart rather than replacing. `src: Core features, the cart rule 5`
- [ ] `C-CF-12` `capability` Incrementing updates in place, decrementing updates in place. `src: Core features, the cart rule 5`
- [ ] `C-CF-13` `capability` Removing deletes the line, keeping the rest in order. `src: Core features, the cart rule 5`
- [ ] `C-CF-14` `capability` Applying a discount attaches the code, re-prices, reports a rejection inline. `src: Core features, the cart rule 5`
- [ ] `C-CF-15` `capability` Setting a note attaches without re-pricing. `src: Core features, the cart rule 5`
- [ ] `C-CF-16` `constraint` No single control empties the cart; a cart is emptied by removing every line. `src: Core features, the cart rule 5`
- [ ] `C-CF-17` `capability` A mutation is optimistic in the view that caused the change, authoritative everywhere. `src: Core features, the cart rule 6`
- [ ] `C-CF-18` `capability` A rejected change reverts the drawer to the value the server returned. `src: Core features, the cart rule 6`
- [ ] `C-CF-19` `constraint` Line order is insertion order, never changing. `src: Core features, the cart rule 7`
- [ ] `C-CF-20` `capability` The cart survives a reload, a navigation to any route, a return after the tab closed. `src: Core features, the cart rule 8`
- [ ] `C-CF-21` `capability` The drawer opens on every successful add. `src: Core features, the cart rule 9`
- [ ] `C-CF-22` `constraint` The drawer does not open on an increment from within itself. `src: Core features, the cart rule 9`
- [ ] `C-CF-23` `constraint` The drawer does not open on a page load with a non-empty cart. `src: Core features, the cart rule 9`
- [ ] `C-CF-24` `literal` The drawer heading reads Cart with a middle dot then the unit count in parentheses. `src: Core features, the cart rule 10`
- [ ] `C-CF-25` `literal` The empty drawer carries the line Your cart is empty with a Continue shopping control. `src: Core features, the cart rule 10`
- [ ] `C-CF-26` `literal` The drawer checkout control reads Checkout with a middle dot then the subtotal. `src: Core features, the cart rule 10`
- [ ] `C-CF-27` `ui` The drawer line shows a small square image, the title, the variant caption, the unit price, a stepper, a bin control. `src: Core features, the cart rule 11`
- [ ] `C-CF-28` `ui` The cart page line shows a larger square image with a hairline border, a heavier title, the variant caption, the unit price, a bordered stepper of three parts, a bin control on a dark square, a right-aligned line total. `src: Core features, the cart rule 11`
- [ ] `C-CF-29` `ui` The checkout summary line shows a small square image carrying a count disc, the title, the variant value alone, a right-aligned line total. `src: Core features, the cart rule 11`
- [ ] `C-CF-30` `constraint` The checkout summary line offers no stepper, no remove. `src: Core features, the cart rule 11`
- [ ] `C-CF-31` `literal` The variant caption is the option name, a colon, a space, the value. `src: Core features, the cart rule 12`
- [ ] `C-CF-32` `constraint` A line whose product has no options omits the variant caption entirely. `src: Core features, the cart rule 12`
- [ ] `C-CF-33` `literal` The upsell line is Shipping Protection at 1000 store minor units with a struck-through 2000. `src: Core features, the upsell rule 1`
- [ ] `C-CF-34` `literal` The upsell description reads Protect your order from damage, loss, or theft during shipping. `src: Core features, the upsell rule 1`
- [ ] `C-CF-35` `data` The upsell is a product record with the handle shipping-protection, a price, a compare-at price, an image, a collection membership. `src: Core features, the upsell rule 2`
- [ ] `C-CF-36` `ui` The upsell appears in the catch-all collection as an ordinary product with a Sale badge. `src: Core features, the upsell rule 2`
- [ ] `C-CF-37` `capability` The upsell line is removable, adjustable, included in the subtotal. `src: Core features, the upsell rule 2`
- [ ] `C-CF-38` `constraint` The upsell is added at most once per cart. `src: Core features, the upsell rule 3`
- [ ] `C-CF-39` `constraint` The upsell does not re-add itself after removal in the same session. `src: Core features, the upsell rule 3`
- [ ] `C-CF-40` `constraint` The upsell is never added to an empty cart. `src: Core features, the upsell rule 3`
- [ ] `C-CF-41` `constraint` A cart holding only the upsell has its checkout control disabled. `src: Core features, the upsell rule 4`
- [ ] `C-CF-42` `constraint` The upsell line carries no variant caption. `src: Core features, the upsell rule 5`
- [ ] `C-CF-43` `constraint` Related products exclude the product being viewed, exclude the upsell item. `src: Core features, the upsell rule 6`
- [ ] `C-CF-44` `ui` The home route is one long scroll in eleven bands. `src: Core features, the home route`
- [ ] `C-CF-45` `ui` Every band boundary on the home route is a hard edge between two grounds with no vertical gap. `src: Core features, the home route`
- [ ] `C-CF-46` `ui` The announcement bar is the topmost band, full width, on a near-black ground with pale text. `src: Core features, the home route rule 1`
- [ ] `C-CF-47` `literal` The first announcement message reads Limited 2-Watch Offer - Buy 1, Get 1 Free. `src: Core features, the home route rule 1`
- [ ] `C-CF-48` `literal` The second announcement message reads Rated 4.8 / 5 by 1,800+ Verified Customers. `src: Core features, the home route rule 1`
- [ ] `C-CF-49` `literal` The third announcement message reads 30-Day Easy Returns - Shop with Confidence. `src: Core features, the home route rule 1`
- [ ] `C-CF-50` `ui` A previous control, a next control sit at the announcement bar edges. `src: Core features, the home route rule 1`
- [ ] `C-CF-51` `capability` The announcement rotation pauses on pointer hover, on keyboard focus within the bar. `src: Core features, the home route rule 1`
- [ ] `C-CF-52` `capability` The announcement rotation does not run under a reduced-motion preference, showing one message. `src: Core features, the home route rule 1`
- [ ] `C-CF-53` `ui` Pointing at an announcement link drops its text colour, its border colour to three-quarter alpha, adding an underline. `src: Core features, the home route rule 1`
- [ ] `C-CF-54` `ui` The masthead sits directly under the announcement bar with no gap, on a pale ground. `src: Core features, the home route rule 2`
- [ ] `C-CF-55` `ui` The masthead carries the wordmark at the left, nine navigation entries in the middle, three utility controls at the right. `src: Core features, the home route rule 2`
- [ ] `C-CF-56` `literal` The nine navigation entries read Home, Catalog, Watches, Men's, Women's, About us, Contact, Blog, Accessories. `src: Core features, the home route rule 2`
- [ ] `C-CF-57` `literal` The Watches disclosure holds Men's Watches, Quartz Watch, Mechanical Watch, Automatic Watch, Women's Watches, Couple Watches, Car Watches in that order. `src: Core features, the home route rule 2`
- [ ] `C-CF-58` `constraint` Only the Watches entry opens anything. `src: Core features, the home route rule 2`
- [ ] `C-CF-59` `ui` The current navigation entry is marked, underlined. `src: Core features, the home route rule 2`
- [ ] `C-CF-60` `ui` The cart badge is a filled disc in a mid, vivid blue with pale text at the lower right of the cart control. `src: Core features, the home route rule 3`
- [ ] `C-CF-61` `constraint` The cart badge appears only when the cart is not empty. `src: Core features, the home route rule 3`
- [ ] `C-CF-62` `ui` The hero banner is full-bleed, running from the masthead to the benefits strip. `src: Core features, the home route rule 4`
- [ ] `C-CF-63` `ui` The hero holds the watch in the right two thirds with the left third dark enough to carry text. `src: Core features, the home route rule 4`
- [ ] `C-CF-64` `literal` The hero primary control reads 2-WATCH BUNDLE OFFER on a pale ground with dark text. `src: Core features, the home route rule 4`
- [ ] `C-CF-65` `literal` The hero secondary control reads VIEW BEST SELLERS on a transparent ground with pale text, a pale hairline border. `src: Core features, the home route rule 4`
- [ ] `C-CF-66` `capability` The hero controls lead to the bundle collection, to the best sellers collection. `src: Core features, the home route rule 4`
- [ ] `C-CF-67` `constraint` The hero is one photograph rather than a slideshow. `src: Core features, the home route rule 4`
- [ ] `C-CF-68` `ui` The benefits strip is a dark band of five equal columns edge to edge across the full viewport width. `src: Core features, the home route rule 5`
- [ ] `C-CF-69` `literal` The first benefit reads Free International Shipping over On every order. `src: Core features, the home route rule 5`
- [ ] `C-CF-70` `literal` The second benefit reads 30-Day Easy Returns over Hassle-free policy. `src: Core features, the home route rule 5`
- [ ] `C-CF-71` `literal` The third benefit reads 1-Year Warranty over Quality guaranteed. `src: Core features, the home route rule 5`
- [ ] `C-CF-72` `literal` The fourth benefit reads Secure Checkout over 256-bit SSL encryption. `src: Core features, the home route rule 5`
- [ ] `C-CF-73` `literal` The fifth benefit reads Rated 4.8 / 5 over By 1,800+ customers. `src: Core features, the home route rule 5`
- [ ] `C-CF-74` `constraint` All five benefits survive at every width. `src: Core features, the home route rule 5`
- [ ] `C-CF-75` `ui` The category carousel shows six circular tiles centred in the content column. `src: Core features, the home route rule 6`
- [ ] `C-CF-76` `literal` The six category tiles read Men's Watches, Women's Watches, Mechanical Watches, Car Watches, Quartz Watches, Couple Watches in that order. `src: Core features, the home route rule 6`
- [ ] `C-CF-77` `capability` Each category tile leads to its own collection. `src: Core features, the home route rule 6`
- [ ] `C-CF-78` `ui` The category carousel controls are present, unavailable, at a wide desktop width rather than absent. `src: Core features, the home route rule 6`
- [ ] `C-CF-79` `ui` The category tile is circular with a square crop masked to a circle, the caption outside the circle. `src: Core features, the home route rule 6`
- [ ] `C-CF-80` `literal` A heading reading Featured products sits left-aligned at the content column edge. `src: Core features, the home route rule 7`
- [ ] `C-CF-81` `ui` Eight product cards follow that heading in two rows of four. `src: Core features, the home route rule 7`
- [ ] `C-CF-82` `literal` A centred control reading VIEW ALL follows the featured grid, leading to the catch-all collection. `src: Core features, the home route rule 8`
- [ ] `C-CF-83` `ui` The editorial banner slideshow is full-bleed, photographic, dark. `src: Core features, the home route rule 9`
- [ ] `C-CF-84` `literal` The banner carries the wordmark with 1985 set at the left. `src: Core features, the home route rule 9`
- [ ] `C-CF-85` `literal` The banner line reads TIME IS  L U X U R Y   INVEST IN QUALITY. with the middle word letter-spaced far wider. `src: Core features, the home route rule 9`
- [ ] `C-CF-86` `literal` A control row beneath the banner carries a previous control, the counter 1/4, a next control. `src: Core features, the home route rule 9`
- [ ] `C-CF-87` `constraint` The banner slideshow holds four slides, an explicit numeric counter rather than dots, no autoplay. `src: Core features, the home route rule 9`
- [ ] `C-CF-88` `ui` The second product row shows four cards with a second VIEW ALL beneath. `src: Core features, the home route rule 10`
- [ ] `C-CF-89` `constraint` Two product rows are separated by the full-bleed banner rather than run as one row. `src: Core features, the home route rule 10`
- [ ] `C-CF-90` `ui` The warranty split panel is a two-column band with no gutter between the columns. `src: Core features, the home route rule 11`
- [ ] `C-CF-91` `ui` The warranty photograph bleeds to the left edge of the viewport, the dark panel bleeds to the right. `src: Core features, the home route rule 11`
- [ ] `C-CF-92` `literal` The warranty eyebrow reads PEACE OF MIND. `src: Core features, the home route rule 11`
- [ ] `C-CF-93` `literal` The warranty heading reads 1-Year Warranty - Confidence in Every Moment at a lighter face than the section headings. `src: Core features, the home route rule 11`
- [ ] `C-CF-94` `literal` The warranty control reads VIEW WARRANTY POLICY with a pale hairline border on a transparent ground. `src: Core features, the home route rule 11`
- [ ] `C-CF-95` `constraint` Neither half of the warranty panel sits inside the content column. `src: Core features, the home route rule 11`
- [ ] `C-CF-96` `literal` The discount signup heading reads Get 10% Off Your First Order. `src: Core features, the home route rule 12`
- [ ] `C-CF-97` `literal` The discount signup line is the early-access sentence pinned below. `src: Core features, the home route rule 12`
- [ ] `C-CF-98` `literal` The discount signup field is labelled Email with an inline submit drawn as an arrow. `src: Core features, the home route rule 12`
- [ ] `C-CF-99` `ui` The product card is stacked, left-aligned, with no border, no shadow, no corner radius. `src: Core features, the product card`
- [ ] `C-CF-100` `ui` The product card carries a square image, badges, the title, a rating row, the compare-at price, the price in that order. `src: Core features, the product card`
- [ ] `C-CF-101` `ui` Card badges are overlaid on the image lower left. `src: Core features, the product card`
- [ ] `C-CF-102` `literal` The Sale badge comes first on a dark ground with pale text at the capsule radius. `src: Core features, the product card rule 1`
- [ ] `C-CF-103` `literal` A promotional badge such as Buy 1 Get 1 Free comes second on a mid, vivid green ground. `src: Core features, the product card rule 1`
- [ ] `C-CF-104` `constraint` The card layout does not shift when the second badge is absent. `src: Core features, the product card rule 1`
- [ ] `C-CF-105` `literal` Sold out replaces the price line on an unavailable product. `src: Core features, the product card rule 1`
- [ ] `C-CF-106` `constraint` The card survives a title that does not begin with VOLARI. `src: Core features, the product card rule 2`
- [ ] `C-CF-107` `literal` The catch-all carries the titles ADDIESDIVE AD2503 Oceanmaster Automatic - Miyota 8215, CRRJU 2165 Grace Minimalist Quartz, LONGLUX 6269K2 Vanguard Skeleton Automatic, LONGLUX 8020P Heritage Open Heart Mechanical, LONGLUX 8057G Apex Skeleton Mechanical, LUMINOUS MILITARY Heritage Automatic. `src: Core features, the product card rule 2`
- [ ] `C-CF-108` `constraint` The maker is its own field, never parsed out of the title. `src: Core features, the product card rule 2`
- [ ] `C-CF-109` `constraint` The rating row is optional per product; the price moves up when absent, nothing reserving the space. `src: Core features, the product card rule 3`
- [ ] `C-CF-110` `constraint` The price line takes one of three shapes: a flat price, a flat price over a struck-through original, or From with a price over a struck-through original. `src: Core features, the product card rule 4`
- [ ] `C-CF-111` `constraint` The From form is required whenever a product's variant prices differ. `src: Core features, the product card rule 4`
- [ ] `C-CF-112` `constraint` The From price names the cheapest available variant rather than the cheapest variant. `src: Core features, the product card rule 4`
- [ ] `C-CF-113` `ui` Pointing at a card fades its image, doing nothing else: no lift, no shadow, no scale. `src: Core features, the product card rule 5`
- [ ] `C-CF-114` `literal` Product 1 is VOLARI 2628 - Timeless Luxury Quartz Watch at 37400 over 18700 with Buy 1 Get 1 Free, rated 4.6 from 154. `src: Core features, the twelve products`
- [ ] `C-CF-115` `literal` Product 2 is VOLARI 2653 Sport Silicone Watch at 29000 over 14500 with Buy 1 Get 1 Free, rated 5.0 from 56. `src: Core features, the twelve products`
- [ ] `C-CF-116` `literal` Product 3 is VOLARI 2632 - Waterproof Stainless Steel Watch at 16000 over 8000, rated 4.9 from 35. `src: Core features, the twelve products`
- [ ] `C-CF-117` `literal` Product 4 is VOLARI 2627 - Diamond Scale Quartz Watch at 14400 over 10400, rated 4.3 from 142. `src: Core features, the twelve products`
- [ ] `C-CF-118` `literal` Product 5 is VOLARI 2309 - Luxury Quartz Chronograph Waterproof Watch at 18600 over 9300, rated 4.5 from 176. `src: Core features, the twelve products`
- [ ] `C-CF-119` `literal` Product 6 is VOLARI 2638 - Classic Fluted Men's Watch at 20400 over 10200, rated 4.9 from 8. `src: Core features, the twelve products`
- [ ] `C-CF-120` `literal` Product 7 is VOLARI 2506 - Rebel Face Watch at 24800 over 12400, rated 4.5 from 197. `src: Core features, the twelve products`
- [ ] `C-CF-121` `literal` Product 8 is VOLARI 2653 Steel - Classic Edition at 24800 over 12400 with Buy 1 Get 1 Free, rated 4.9 from 11. `src: Core features, the twelve products`
- [ ] `C-CF-122` `literal` Product 9 is VOLARI 2622 - Elegant Zircon Women's Quartz Watch at 20600 over 9300, rated 4.9 from 15. `src: Core features, the twelve products`
- [ ] `C-CF-123` `literal` Product 10 is VOLARI 2697 - Women's Business Watch at 13000 over 9200, rated 4.9 from 22. `src: Core features, the twelve products`
- [ ] `C-CF-124` `literal` Product 11 is VOLARI 2357 - Crystal Elegance Women's Watch at 12600 over 10100, rated 5.0 from 12. `src: Core features, the twelve products`
- [ ] `C-CF-125` `literal` Product 12 is VOLARI 2675 - Dreamy Fish Tail Watch at 10500 over 8400, rated 4.8 from 12. `src: Core features, the twelve products`
- [ ] `C-CF-126` `constraint` Every one of the twelve home products carries the Sale badge. `src: Core features, the twelve products`
- [ ] `C-CF-127` `constraint` Products four, ten show the From form over their cheapest available colourway. `src: Core features, the twelve products`
- [ ] `C-CF-128` `ui` The collection template carries the title as the page heading, a description, a control row, a four-column grid, numbered pagination. `src: Core features, the collection route`
- [ ] `C-CF-129` `constraint` A curated collection carries a description where the catch-all carries none. `src: Core features, the collection route`
- [ ] `C-CF-130` `literal` The control row left side reads Filter: then one disclosure reading Availability with a trailing caret. `src: Core features, the collection route rule 1`
- [ ] `C-CF-131` `literal` The control row right side reads Sort by:, a select, then the result count as the number, a space, the word products. `src: Core features, the collection route rule 1`
- [ ] `C-CF-132` `literal` The facet panel carries 0 selected, a Reset control, a Remove all control. `src: Core features, the collection route rule 1`
- [ ] `C-CF-133` `literal` The catch-all reports 174 products with In stock at 161, Out of stock at 13. `src: Core features, the collection route rule 2`
- [ ] `C-CF-134` `constraint` The facet counts, the result count are computed over the same set, so the facet counts sum to the heading total. `src: Core features, the collection route rule 2`
- [ ] `C-CF-135` `literal` The sort options read Featured, Most relevant, Best selling, Alphabetically, A-Z, Alphabetically, Z-A, Price, low to high, Price, high to low, Date, old to new, Date, new to old in that order. `src: Core features, the collection route rule 3`
- [ ] `C-CF-136` `literal` Sort, filter, page number are query parameters under the keys sort_by, availability, page. `src: Core features, the collection route rule 4`
- [ ] `C-CF-137` `capability` All three query parameters survive a reload, can be pasted to somebody else. `src: Core features, the collection route rule 4`
- [ ] `C-CF-138` `constraint` Changing a filter or a sort does not scroll the page; the grid re-renders in place. `src: Core features, the collection route rule 5`
- [ ] `C-CF-139` `literal` Below the narrow switch the control row collapses into a Filter control opening a panel headed Filter. `src: Core features, the collection route rule 6`
- [ ] `C-CF-140` `literal` The mobile facet panel carries the result count, the same facets, the same sort select, a Remove all control, an Apply control. `src: Core features, the collection route rule 6`
- [ ] `C-CF-141` `constraint` The mobile panel commits on Apply where the desktop row commits on each change with no Apply. `src: Core features, the collection route rule 6`
- [ ] `C-CF-142` `ui` The grid is four columns at desktop, two below the narrow switch, never one. `src: Core features, the collection route rule 7`
- [ ] `C-CF-143` `constraint` Grid rows are not height-matched; a taller card pushes the next row down. `src: Core features, the collection route rule 7`
- [ ] `C-CF-144` `literal` Pagination is numbered at sixteen products a page, eleven pages for the catch-all, with a next control. `src: Core features, the collection route rule 8`
- [ ] `C-CF-145` `constraint` No infinite scroll, no load-more appears on a collection. `src: Core features, the collection route rule 8`
- [ ] `C-CF-146` `capability` The page number is part of the address, so a return from a product lands on the same page. `src: Core features, the collection route rule 8`
- [ ] `C-CF-147` `ui` The product route holds a two-column shell with the gallery at roughly half on the left, the information column at roughly half on the right. `src: Core features, the product route rule 1`
- [ ] `C-CF-148` `ui` The gallery holds position as the right column scrolls past. `src: Core features, the product route rule 1`
- [ ] `C-CF-149` `ui` The gallery hold releases before the reviews band. `src: Core features, the product route rule 1`
- [ ] `C-CF-150` `ui` The gallery is a main frame with a hairline border over a thumbnail strip of four visible frames with a previous control, a next control. `src: Core features, the product route rule 2`
- [ ] `C-CF-151` `literal` The deeply specified product carries eleven media, each frame opening a modal at full size, with a counter reading the current number, a slash, the total. `src: Core features, the product route rule 2`
- [ ] `C-CF-152` `ui` The thumbnail strip pages four at a time rather than scrolling freely. `src: Core features, the product route rule 2`
- [ ] `C-CF-153` `ui` The active thumbnail carries a solid border where the rest carry the hairline. `src: Core features, the product route rule 2`
- [ ] `C-CF-154` `constraint` The information column above the buy control runs breadcrumb, title, rating, offer line, price pair, shipping line in that order. `src: Core features, the product route rule 3`
- [ ] `C-CF-155` `literal` The breadcrumb is three levels separated by a right-pointing angle quotation mark in a span of its own. `src: Core features, the product route rule 4`
- [ ] `C-CF-156` `constraint` The breadcrumb middle level is derived from the arrival path rather than from a product field. `src: Core features, the product route rule 4`
- [ ] `C-CF-157` `capability` A visitor arriving cold sees the product's primary collection in the breadcrumb. `src: Core features, the product route rule 4`
- [ ] `C-CF-158` `literal` The rating renders as a star row, the label TrustScore, the value, a vertical bar, the count, the label Reviews. `src: Core features, the product route rule 5`
- [ ] `C-CF-159` `constraint` The rating value renders to one decimal place always, so a perfect rating renders as 5.0. `src: Core features, the product route rule 5`
- [ ] `C-CF-160` `literal` The offer line reads Exclusive Online Offer - Save then the percentage, uppercase, at a heavier face. `src: Core features, the product route rule 6`
- [ ] `C-CF-161` `constraint` The offer percentage is computed from the two prices after conversion rather than authored. `src: Core features, the product route rule 6`
- [ ] `C-CF-162` `literal` The shipping line reads FREE Shipping. `src: Core features, the product route rule 7`
- [ ] `C-CF-163` `literal` The colourway grid opens with a legend reading Color, a colon, a space, the selected value. `src: Core features, the product route rule 8`
- [ ] `C-CF-164` `ui` Each swatch is a bordered tile carrying a thumbnail, the colourway name, that colourway's own price. `src: Core features, the product route rule 8`
- [ ] `C-CF-165` `ui` The selected swatch tile carries a heavier border. `src: Core features, the product route rule 8`
- [ ] `C-CF-166` `ui` An unavailable swatch is struck by a single diagonal line in a mid, vivid red across its thumbnail. `src: Core features, the product route rule 8`
- [ ] `C-CF-167` `constraint` A swatch carries its own price, so prices may differ between swatches. `src: Core features, the product route rule 8`
- [ ] `C-CF-168` `constraint` An unavailable swatch remains selectable, showing its price, showing its image. `src: Core features, the product route rule 8`
- [ ] `C-CF-169` `capability` Selecting an unavailable swatch disables the buy control, replacing the stock line. `src: Core features, the product route rule 8`
- [ ] `C-CF-170` `capability` Selecting a swatch updates the gallery position, the price pair, the offer percentage, the stock line, the buy control state, the address in one pass. `src: Core features, the product route rule 8`
- [ ] `C-CF-171` `constraint` Selecting a swatch does not scroll the page, does not collapse the grid. `src: Core features, the product route rule 8`
- [ ] `C-CF-172` `constraint` Selecting a colourway moves the gallery to that colourway's first image without filtering the gallery down to that colourway alone. `src: Core features, the product route rule 8`
- [ ] `C-CF-173` `capability` A second option renders as a second legend over a second row, with availability computed over the combination. `src: Core features, the product route rule 8`
- [ ] `C-CF-174` `ui` The quantity stepper is a decrement, a value, an increment, bordered as one group. `src: Core features, the product route rule 9`
- [ ] `C-CF-175` `literal` The in-cart count renders as Quantity followed by an open parenthesis, a space, the count, the words in cart, a close parenthesis. `src: Core features, the product route rule 9`
- [ ] `C-CF-176` `capability` The in-cart count is a live projection of the cart for that colourway alone, changing when the drawer changes. `src: Core features, the product route rule 9`
- [ ] `C-CF-177` `literal` The stock line is a small filled disc then In stock - ready to ship. `src: Core features, the product route rule 10`
- [ ] `C-CF-178` `constraint` The stock line has three states: available, unavailable, unknown, never claiming availability unconfirmed. `src: Core features, the product route rule 10`
- [ ] `C-CF-179` `literal` On an unavailable colourway the buy control reads Sold out, disabled. `src: Core features, the product route rule 10`
- [ ] `C-CF-180` `literal` The buy control reads ADD TO CART on a dark ground with pale uppercase letter-spaced text. `src: Core features, the product route rule 11`
- [ ] `C-CF-181` `ui` A wallet control on a light, vivid indigo ground sits under the buy control. `src: Core features, the product route rule 11`
- [ ] `C-CF-182` `literal` A More payment options underlined link reveals the remaining accelerated paths. `src: Core features, the product route rule 11`
- [ ] `C-CF-183` `capability` The buy control is a submit remaining operable when scripting fails, landing on the cart page. `src: Core features, the product route rule 11`
- [ ] `C-CF-184` `capability` The buy control shows a pending state between press, confirmation, refusing a second press. `src: Core features, the product route rule 11`
- [ ] `C-CF-185` `constraint` An accelerated path carries the same cart object rather than a different set of lines. `src: Core features, the product route rule 11`
- [ ] `C-CF-186` `constraint` A wallet control unavailable in the browser is absent rather than disabled. `src: Core features, the product route rule 11`
- [ ] `C-CF-187` `literal` The trust strip reads Free Shipping on All Orders, 30-Day Easy Returns, Secure Checkout, 1-Year Warranty in one row of four separated by space. `src: Core features, the product route rule 12`
- [ ] `C-CF-188` `ui` The description column runs a lifestyle frame, a heading repeating the title, two paragraphs, a feature list heading over six leads, an inclusions heading over a list, a closing heading with one paragraph, a Share control. `src: Core features, the product route rule 13`
- [ ] `C-CF-189` `literal` The feature list heading is the appreciation heading pinned below. `src: Core features, the product route rule 13`
- [ ] `C-CF-190` `literal` The inclusions heading reads What's Included. `src: Core features, the product route rule 13`
- [ ] `C-CF-191` `literal` The closing heading reads A Watch with Attitude. `src: Core features, the product route rule 13`
- [ ] `C-CF-192` `literal` The six feature leads read Bold Graphic Dial, Precision Quartz Movement, Stainless Steel Case, Scratch-Resistant Mineral Crystal, Luminous Hands, Water-Resistant Construction (3ATM). `src: Core features, the product route rule 13`
- [ ] `C-CF-193` `literal` The inclusions read 1x VOLARI Watch, 1x Original VOLARI Presentation Box, 1x User Manual, 1x Bracelet Adjustment Tool, 1x Microfiber Cleaning Cloth. `src: Core features, the product route rule 13`
- [ ] `C-CF-194` `ui` Three collapsible panels follow, covering shipping, the warranty, returns, collapsed at rest. `src: Core features, the product route rule 14`
- [ ] `C-CF-195` `constraint` The three panels render the same source as the editorial pages covering the same ground. `src: Core features, the product route rule 14`
- [ ] `C-CF-196` `literal` A heading reading You may also like opens the related rail. `src: Core features, the product route rule 15`
- [ ] `C-CF-197` `ui` The reviews band is full-bleed on a pale ground, breaking out of the content column. `src: Core features, the product route rule 16`
- [ ] `C-CF-198` `literal` The reviews band carries a Write a review link, a centred line reading Trusted by Countless Customers, a carousel, a previous control, a next control. `src: Core features, the product route rule 16`
- [ ] `C-CF-199` `ui` A review card carries a customer photograph, a five-star row, the review text centred, the reviewer name at the foot at a heavier face. `src: Core features, the product route rule 16`
- [ ] `C-CF-200` `ui` The review carousel shows partial cards at both edges, so the row reads as continuing past the viewport. `src: Core features, the product route rule 16`
- [ ] `C-CF-201` `constraint` Write a review links out rather than opening a composer on the page. `src: Core features, the product route rule 16`
- [ ] `C-CF-202` `literal` The deeply specified product is at the handle volari-2506-rebel-face-watch, maker VOLARI, model 2506, compare-at 24800, rated 4.5 from 197, with eleven media. `src: Core features, the deeply specified product`
- [ ] `C-CF-203` `literal` Its five colourways are Green Black, Black Red, Green White, Red White, Red Black, all at 12400. `src: Core features, the deeply specified product`
- [ ] `C-CF-204` `literal` Its Black Red colourway is unavailable where the other four are available. `src: Core features, the deeply specified product`
- [ ] `C-CF-205` `literal` Its offer line reads Exclusive Online Offer - Save 50%. `src: Core features, the deeply specified product`
- [ ] `C-CF-206` `literal` VOLARI 2627 - Diamond Scale Quartz Watch carries Rose Gold at 9900 unavailable, Steel Silver at 10400 available, Gold at 11900 available. `src: Core features, the deeply specified product`
- [ ] `C-CF-207` `literal` VOLARI 2697 - Women's Business Watch carries Silver at 9200 available, Gold at 10600 available. `src: Core features, the deeply specified product`
- [ ] `C-CF-208` `constraint` The Diamond Scale card names 10400 rather than 9900, because its cheapest colourway is unavailable. `src: Core features, the deeply specified product`
- [ ] `C-CF-209` `literal` The empty cart page carries a centred heading Your cart is empty at the page-heading size. `src: Core features, the cart page rule 1`
- [ ] `C-CF-210` `literal` A CONTINUE SHOPPING control sits beneath on a dark ground with the thick outset ring. `src: Core features, the cart page rule 1`
- [ ] `C-CF-211` `literal` A centred heading Have an account? sits with the line Log in to check out faster. carrying an underlined Log in. `src: Core features, the cart page rule 1`
- [ ] `C-CF-212` `constraint` The footer follows the empty cart immediately, with no minimum height pushing the footer off screen. `src: Core features, the cart page rule 1`
- [ ] `C-CF-213` `literal` The populated cart page heading reads Your cart on the left with an underlined Continue shopping link on the right of the same row. `src: Core features, the cart page rule 2`
- [ ] `C-CF-214` `literal` The cart table carries three column headings, uppercase, subdued, reading PRODUCT, QUANTITY, TOTAL. `src: Core features, the cart page rule 2`
- [ ] `C-CF-215` `ui` A hairline rule closes the cart table. `src: Core features, the cart page rule 2`
- [ ] `C-CF-216` `literal` The totals block left group carries Estimated total with its value, the line Free shipping available at checkout!, a CHECKOUT SECURELY control, two wallet controls. `src: Core features, the cart page rule 3`
- [ ] `C-CF-217` `literal` The totals block centre group is a Discount code field with an APPLY control on a dark ground immediately to its right with no gap. `src: Core features, the cart page rule 3`
- [ ] `C-CF-218` `literal` The totals block right group is a two-by-two cluster reading Secure Checkout, Free International Shipping, 30-Day Returns, 1-Year Warranty under a hairline rule. `src: Core features, the cart page rule 3`
- [ ] `C-CF-219` `constraint` Estimated total is the cart subtotal, never labelled Total on the cart page. `src: Core features, the cart page rule 4`
- [ ] `C-CF-220` `capability` A rejected discount code reports inline beside the field without clearing the field, without reloading. `src: Core features, the cart page rule 5`
- [ ] `C-CF-221` `capability` An accepted discount code re-prices the lines, the estimated total, in place. `src: Core features, the cart page rule 5`
- [ ] `C-CF-222` `constraint` The checkout carries no announcement bar, no navigation, no footer, no currency selector, no cart drawer. `src: Core features, the checkout rule 1`
- [ ] `C-CF-223` `ui` The checkout masthead is the wordmark alone, centred, with a single cart mark on the right. `src: Core features, the checkout rule 1`
- [ ] `C-CF-224` `capability` The checkout is entered from the drawer control, the cart page control, either wallet control, a cart permalink. `src: Core features, the checkout rule 2`
- [ ] `C-CF-225` `constraint` The handoff carries the whole cart, the upsell line, any applied discount code. `src: Core features, the checkout rule 3`
- [ ] `C-CF-226` `constraint` The checkout line items, quantities, prices are the cart with no additions, no omissions, at the same total. `src: Core features, the checkout rule 3`
- [ ] `C-CF-227` `capability` Submitting the checkout creates the order with exactly one billing account in killbill. `src: Core features, the checkout rule 4`
- [ ] `C-CF-228` `contract` The billing account write carries name, externalKey, email, currency, country. `src: Core features, the checkout rule 4`
- [ ] `C-CF-229` `constraint` The externalKey is the order reference, the currency is the cart display currency code in uppercase. `src: Core features, the checkout rule 4`
- [ ] `C-CF-230` `constraint` The account is identified by its externalKey, never by the generated identifier killbill returns. `src: Core features, the checkout rule 4`
- [ ] `C-CF-231` `constraint` A re-submitted order creates no second billing account, refused by the store's own unique-key conflict. `src: Core features, the checkout rule 5`
- [ ] `C-CF-232` `capability` The app reports the existing order on a repeat rather than a failure. `src: Core features, the checkout rule 5`
- [ ] `C-CF-233` `constraint` The app never shows a billing outcome unread from the API. `src: Core features, the checkout rule 5`
- [ ] `C-CF-234` `capability` Cancelling the checkout returns to the cart page with the cart unchanged. `src: Core features, the checkout rule 6`
- [ ] `C-CF-235` `capability` A completed order clears the cart, returning the badge to zero without a reload. `src: Core features, the checkout rule 6`
- [ ] `C-CF-236` `capability` The checkout surface is reachable, completable, without the storefront scripting having run. `src: Core features, the checkout rule 7`
- [ ] `C-CF-237` `literal` The checkout summary renders Subtotal with a middle dot, the unit count, the word items, then Shipping with the line Enter shipping address, then Total with its figure, its currency code. `src: Core features, the checkout rule 8`
- [ ] `C-CF-238` `constraint` Every amount is stored in the store currency usd as an integer in minor units. `src: Core features, money rule 1`
- [ ] `C-CF-239` `constraint` A display currency is a presentation concern, never stored on a product. `src: Core features, money rule 1`
- [ ] `C-CF-240` `literal` Two display currencies exist: USD at a rate of 1.0, INR at a rate of 88.0. `src: Core features, money rule 2`
- [ ] `C-CF-241` `constraint` Every price in one response converts by the same rate in the same pass. `src: Core features, money rule 3`
- [ ] `C-CF-242` `constraint` One rate is resolved per request, used by every price in that response. `src: Core features, money rule 3`
- [ ] `C-CF-243` `literal` The rendered format is the currency prefix, a space, digits grouped by thousands, a decimal point, two decimals, a space, the currency code. `src: Core features, money rule 4`
- [ ] `C-CF-244` `literal` The prefix is a dollar sign for USD, the characters Rs. for INR. `src: Core features, money rule 4`
- [ ] `C-CF-245` `literal` A price of 12400 store minor units renders as $ 124.00 USD, as Rs. 10,912.00 INR. `src: Core features, money rule 4`
- [ ] `C-CF-246` `constraint` The same product shows the same price on the home route, on a collection route, at the same moment. `src: Core features, money rule 5`
- [ ] `C-CF-247` `ui` The currency selector is fixed to the lower left of the viewport on every storefront route, reading the active code with a trailing caret. `src: Core features, money rule 6`
- [ ] `C-CF-248` `ui` The currency selector sits on a pale ground with a hairline border, square corners. `src: Core features, money rule 6`
- [ ] `C-CF-249` `constraint` The currency selector stays in the lower left corner through every scroll position on every route, never overlapping the footer content. `src: Core features, money rule 6`
- [ ] `C-CF-250` `capability` The currency selector list is keyboard-navigable, closing on escape. `src: Core features, money rule 6`
- [ ] `C-CF-251` `constraint` The currency selector popover is the one element in the build that casts a shadow. `src: Core features, money rule 6`
- [ ] `C-CF-252` `ui` The footer is a dark band with pale text in five stacked blocks. `src: Core features, the footer rule 1`
- [ ] `C-CF-253` `literal` The brand block is a centred heading reading Volari Official in uppercase with wide letter-spacing over a hairline rule over a centred statement of four lines. `src: Core features, the footer rule 2`
- [ ] `C-CF-254` `literal` The three footer columns are headed MENU, FOOTER MENU, CONTACT US. `src: Core features, the footer rule 3`
- [ ] `C-CF-255` `constraint` The MENU column repeats the masthead nine entries exactly. `src: Core features, the footer rule 3`
- [ ] `C-CF-256` `literal` The FOOTER MENU column reads About Us, Terms of Service, Refund & Return Policy, Shipping Policy, Payment & Delivery, Privacy Policy, Contact Us, VOLARI Warranty, Contact Information, Legal Notice, Faq in that order. `src: Core features, the footer rule 3`
- [ ] `C-CF-257` `literal` The CONTACT US column carries the support address support@volariofficial.com with the support number +1 55 0100-0000. `src: Core features, the footer rule 3`
- [ ] `C-CF-258` `constraint` Faq stands in sentence case where its own page titles itself in capitals. `src: Core features, the footer rule 3`
- [ ] `C-CF-259` `literal` The newsletter block carries a NEWSLETTER heading, the signup line pinned below, a field labelled Email with an inline arrow submit. `src: Core features, the footer rule 4`
- [ ] `C-CF-260` `constraint` Both signup fields post to the same list. `src: Core features, the footer rule 4`
- [ ] `C-CF-261` `ui` The social block is right-aligned on the newsletter row, carrying a follow control on a light, vivid indigo ground then two social marks. `src: Core features, the footer rule 5`
- [ ] `C-CF-262` `ui` The payment strip carries thirteen payment marks, a line with the copyright, the store name, the platform credit, then six policy links separated by a middle dot. `src: Core features, the footer rule 6`
- [ ] `C-CF-263` `literal` The six strip links read Refund policy, Privacy policy, Terms of service, Shipping policy, Contact information, Legal notice. `src: Core features, the footer rule 6`
- [ ] `C-CF-264` `capability` Every policy page is linked twice from the footer, once from the column, once from the strip. `src: Core features, the footer rule 7`
- [ ] `C-CF-265` `constraint` The refund policy is linked a third time because the column, the strip use two different labels for one address. `src: Core features, the footer rule 7`
- [ ] `C-CF-266` `capability` Both signup fields report success, failure, inline, in place, without navigating. `src: Core features, the signup rule 1`
- [ ] `C-CF-267` `capability` A successful signup sends one email over real SMTP to the address typed, with no cc, no bcc. `src: Core features, the signup rule 2`
- [ ] `C-CF-268` `literal` The signup subject begins with Your 10% code: followed by the code, so the code VOLARI10 gives the subject Your 10% code: VOLARI10. `src: Core features, the signup rule 2`
- [ ] `C-CF-269` `constraint` The signup body is non-empty, naming the code, naming Volari Official. `src: Core features, the signup rule 2`
- [ ] `C-CF-270` `constraint` A malformed address, a repeat address, a bot refusal each report inline, sending no mail. `src: Core features, the signup rule 3`
- [ ] `C-CF-271` `capability` A form carrying a filled unattended decoy field is refused. `src: Core features, the signup rule 4`
- [ ] `C-CF-272` `capability` The same form submitted repeatedly in quick succession from one session is refused. `src: Core features, the signup rule 4`
- [ ] `C-CF-273` `constraint` A refused submission writes nothing, sends nothing. `src: Core features, the signup rule 4`
- [ ] `C-CF-274` `capability` The contact form validates on blur rather than on keystroke. `src: Core features, the signup rule 5`
- [ ] `C-CF-275` `capability` The contact form reports success, failure, in place without navigating, never clearing itself on a failed submit. `src: Core features, the signup rule 5`
- [ ] `C-CF-276` `constraint` The contact form records the message, sending no mail. `src: Core features, the signup rule 5`
- [ ] `C-CF-277` `ui` A first-time visitor is asked once about non-essential cookie storage in a panel with a short heading, one sentence, a link to the privacy page, two controls. `src: Core features, the cookie choice`
- [ ] `C-CF-278` `capability` The cookie answer survives a reload, so the panel does not return. `src: Core features, the cookie choice`
- [ ] `C-CF-279` `capability` The cookie panel traps the keyboard, returns focus to whatever opened the panel, closes on escape. `src: Core features, the cookie choice`
- [ ] `C-CF-280` `ui` Eleven pages share one single-column template of chrome, a page title, prose in the content column, the footer. `src: Core features, the editorial pages rule 1`
- [ ] `C-CF-281` `constraint` The editorial template has no sidebar, no vertical centring of short content, no maximum width narrower than the content column. `src: Core features, the editorial pages rule 1`
- [ ] `C-CF-282` `capability` The privacy page is reachable from the footer of every route, stating what the shop stores about a visitor, for how long. `src: Core features, the editorial pages rule 3`
- [ ] `C-CF-283` `constraint` The terms page is carried as unbroken prose without a contents list, without collapsing. `src: Core features, the editorial pages rule 4`
- [ ] `C-CF-284` `constraint` The contact-information page has no minimum height, with the footer where the content ends. `src: Core features, the editorial pages rule 5`
- [ ] `C-CF-285` `capability` Every questions-page panel is addressable, so one answer can be linked. `src: Core features, the editorial pages rule 6`
- [ ] `C-CF-286` `capability` An opened questions panel scrolls itself into view only when not already fully visible. `src: Core features, the editorial pages rule 6`
- [ ] `C-CF-287` `ui` The blog index is a grid of article cards, the product card with the price furniture removed. `src: Core features, the editorial pages rule 7`
- [ ] `C-CF-288` `constraint` The returns window, the warranty term, the shipping promise are each authored once, rendered everywhere. `src: Core features, the editorial pages rule 8`
- [ ] `C-CF-289` `constraint` The returns window appears in six places: the announcement bar, the benefits strip, the trust strip, a product panel, the cart reassurance cluster, the refund policy page. `src: Core features, the editorial pages rule 8`
- [ ] `C-CF-290` `capability` The account handoff is reached from the masthead account control on every storefront route, from the empty cart Log in link. `src: Core features, the account handoff`
- [ ] `C-CF-291` `capability` The account handoff returns the visitor to the route left behind rather than to the home route. `src: Core features, the account handoff`

## C-UF User flow

- [ ] `C-UF-01` `contract` The home route resolves at the site root. `src: User flow routes table`
- [ ] `C-UF-02` `contract` The cart page resolves at /cart. `src: User flow routes table`
- [ ] `C-UF-03` `contract` The catch-all resolves at /collections/all carrying 174 products over eleven pages. `src: User flow routes table`
- [ ] `C-UF-04` `contract` The ten curated collections resolve at mens-watches, womens-watches, couple-watches, car-watches, quartz-watches, mechanical-watches, automatic-watch, best-sellers, 2-watch-bundle-offer, watch-accessories under /collections. `src: User flow routes table`
- [ ] `C-UF-05` `contract` A product resolves at /products with its handle. `src: User flow routes table`
- [ ] `C-UF-06` `contract` The five authored pages resolve at about-us, contact, faq, volari-warranty, payment-delivery under /pages. `src: User flow routes table`
- [ ] `C-UF-07` `contract` The blog index resolves at /blogs/watch-guide. `src: User flow routes table`
- [ ] `C-UF-08` `contract` The six policy pages resolve at refund-policy, shipping-policy, privacy-policy, terms-of-service, legal-notice, contact-information under /policies. `src: User flow routes table`
- [ ] `C-UF-09` `contract` The sign-in handoff resolves at /customer_authentication/redirect. `src: User flow routes table`
- [ ] `C-UF-10` `contract` The cart permalink resolves at /cart with a variant reference, a colon, a quantity. `src: User flow routes table`
- [ ] `C-UF-11` `contract` The checkout boundary resolves at /checkout. `src: User flow routes table`
- [ ] `C-UF-12` `contract` A sitemap resolves at /sitemap.xml with a robots file at /robots.txt. `src: User flow routes table`
- [ ] `C-UF-13` `constraint` A product address carries no collection segment. `src: User flow, routes para 2`
- [ ] `C-UF-14` `constraint` No route redirects for authentication, no route is protected. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `constraint` The cart permalink is reachable from nothing on the site. `src: User flow, entry and redirects`
- [ ] `C-UF-16` `capability` The cart permalink builds a cart from the address, sending the visitor straight into the checkout. `src: User flow, entry and redirects`
- [ ] `C-UF-17` `capability` A malformed variant reference lands on the cart page with the existing cart untouched, starting no checkout. `src: User flow, entry and redirects`
- [ ] `C-UF-18` `capability` An unknown address renders the shop's own not-found page with the chrome intact, a link back to the home route. `src: User flow, entry and redirects`
- [ ] `C-UF-19` `capability` Four overlays are reachable from every storefront route: the cart drawer, search, the Watches submenu, the navigation drawer. `src: User flow, entry and redirects`
- [ ] `C-UF-20` `constraint` No overlay changes the address. `src: User flow, entry and redirects`
- [ ] `C-UF-21` `capability` Every overlay closes on the escape key. `src: User flow, entry and redirects`
- [ ] `C-UF-22` `constraint` Opening one overlay closes the other three, so no two overlays are open at once. `src: User flow, entry and redirects`
- [ ] `C-UF-23` `capability` Search opens a field taking focus immediately, offering suggestions as the visitor types without a submit. `src: User flow, entry and redirects`
- [ ] `C-UF-24` `capability` Search is dismissable on escape without changing the address, degrading to a plain submitted query when suggestions cannot be fetched. `src: User flow, entry and redirects`
- [ ] `C-UF-25` `capability` Search suggestions carry a thumbnail with a price, reachable by keyboard from the field. `src: User flow, entry and redirects`
- [ ] `C-UF-26` `capability` Scrolling back up the home route replays nothing that has already arrived. `src: User flow journey 1`
- [ ] `C-UF-27` `capability` Adding a second watch makes the badge read three rather than two. `src: User flow journey 5`
- [ ] `C-UF-28` `capability` A cart of two plus a cart permalink for a third watch arrives at three rather than one. `src: User flow journey 7`
- [ ] `C-UF-29` `constraint` Every list carries an empty state. `src: User flow states`
- [ ] `C-UF-30` `constraint` A collection matching no product states so in the result region. `src: User flow states`
- [ ] `C-UF-31` `constraint` Every route carries a loading state holding the layout the loaded route will have. `src: User flow states`
- [ ] `C-UF-32` `capability` A failed data request leaves the chrome standing, offering a retry. `src: User flow states`
- [ ] `C-UF-33` `constraint` A failed data request never blanks the page, never shows a stack trace. `src: User flow states`
- [ ] `C-UF-34` `constraint` Content a script failed to reveal is simply present. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product reads as a consumer retail storefront rather than an operational tool or an editorial showcase. `src: UI/UX notes para 2`
- [ ] `C-UX-02` `ui` The subject of every screen is a watch photographed against a pale ground. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` The shop holds repetition over novelty. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` The shop holds the argument over the ornament. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` The chrome carries no brand colour at all. `src: UI/UX notes, colour`
- [ ] `C-UX-06` `ui` Each colour job owns its colour exclusively. `src: UI/UX notes, colour`
- [ ] `C-UX-07` `ui` Subdued text is a near-black neutral at reduced alpha over the ground rather than a chosen grey. `src: UI/UX notes, colour`
- [ ] `C-UX-08` `ui` One family carries the whole shop in three faces, headings differing from body by face alone. `src: UI/UX notes, type`
- [ ] `C-UX-09` `ui` Line height splits generous for reading at length, tight for scanning. `src: UI/UX notes, type`
- [ ] `C-UX-10` `ui` The body size is the default, with every larger size a deliberate exception. `src: UI/UX notes, type`
- [ ] `C-UX-11` `ui` Buttons, fields, image frames, cards, panels, popovers all carry hard corners. `src: UI/UX notes, shape`
- [ ] `C-UX-12` `ui` Exactly two things are rounded as fully rounded capsules: the sale badge, the variant pill. `src: UI/UX notes, shape`
- [ ] `C-UX-13` `ui` The primary control carries a thick outset ring rather than a hairline. `src: UI/UX notes, shape`
- [ ] `C-UX-14` `ui` Cards are held apart from the ground by their edges, by the ground itself, never by elevation. `src: UI/UX notes, elevation`
- [ ] `C-UX-15` `ui` The shop holds space over rules, separating the trust strip items, the footer columns, without dividers. `src: UI/UX notes, elevation`
- [ ] `C-UX-16` `ui` The product grid gutter is a hair, so four watches read as one continuous shelf. `src: UI/UX notes, density`
- [ ] `C-UX-17` `ui` Sections carry their own internal padding, abutting exactly with no rhythm of vertical margin. `src: UI/UX notes, density`
- [ ] `C-UX-18` `ui` Four speeds carry the whole build with two curves. `src: UI/UX notes, motion`
- [ ] `C-UX-19` `ui` One curve eases both in, out, belonging to anything responding to a pointer. `src: UI/UX notes, motion`
- [ ] `C-UX-20` `ui` The other curve has no ease in, belonging to anything arriving on screen. `src: UI/UX notes, motion`
- [ ] `C-UX-21` `ui` Content below the fold arrives once on first entering view, then holds forever. `src: UI/UX notes, motion`
- [ ] `C-UX-22` `ui` Nothing in the build is tied to the scrollbar: nothing pins, nothing parallaxes. `src: UI/UX notes, motion`
- [ ] `C-UX-23` `ui` No index-based delay is added on top of the entrance a grid already staggers by itself. `src: UI/UX notes, motion`
- [ ] `C-UX-24` `ui` The cart badge incrementing is the one moment earning a damped bounce. `src: UI/UX notes, motion`
- [ ] `C-UX-25` `ui` Two loading treatments, a sweep with a pulse, belong to the product grid, the drawer. `src: UI/UX notes, motion`
- [ ] `C-UX-26` `ui` Body text meets WCAG AA contrast against its ground. `src: UI/UX notes, accessibility`
- [ ] `C-UX-27` `ui` The focus ring is drawn twice, a pale ring inside a soft dark one. `src: UI/UX notes, accessibility`
- [ ] `C-UX-28` `ui` Full keyboard navigation reaches every interactive element. `src: UI/UX notes, accessibility`
- [ ] `C-UX-29` `ui` Every overlay takes focus on open, traps focus, returns focus to whatever opened the overlay. `src: UI/UX notes, accessibility`
- [ ] `C-UX-30` `ui` Touch targets are comfortably sized, icon-only controls carry labels, meaning is never carried by colour alone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-31` `ui` Under forced colours every signal carried in colour alone survives. `src: UI/UX notes, accessibility`
- [ ] `C-UX-32` `ui` Under a reduced-motion preference nothing reveals, nothing rotates, nothing autoplays, every element present at load. `src: UI/UX notes, accessibility`
- [ ] `C-UX-33` `ui` Two breakpoints carry the site with every other breakpoint a nudge. `src: UI/UX notes, responsive`
- [ ] `C-UX-34` `ui` At the wider breakpoint the nine navigation entries fold into a menu control. `src: UI/UX notes, responsive`
- [ ] `C-UX-35` `ui` The wordmark, the three utility marks stay in the bar at every width. `src: UI/UX notes, responsive`
- [ ] `C-UX-36` `ui` The cart badge stays visible on a phone. `src: UI/UX notes, responsive`
- [ ] `C-UX-37` `ui` At the narrower breakpoint the product columns stack gallery first with the hold released. `src: UI/UX notes, responsive`
- [ ] `C-UX-38` `ui` At the narrower breakpoint the warranty panel stacks photograph above the dark half at full viewport width. `src: UI/UX notes, responsive`
- [ ] `C-UX-39` `ui` On a phone the buy control is reachable without scrolling past the whole gallery. `src: UI/UX notes, responsive`
- [ ] `C-UX-40` `ui` At a narrow viewport nothing overflows sideways. `src: UI/UX notes, responsive`
- [ ] `C-UX-41` `ui` The product route is taller at the middle width than at the widest. `src: UI/UX notes, responsive`
- [ ] `C-UX-42` `ui` The shop must not read as a grid of cards separated by borders, by drop shadows. `src: UI/UX notes, what this must not look like`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Three disjoint token registers exist: a storefront register, a cart register, a checkout register. `src: Front-end specification, the three registers`
- [ ] `C-FE-02` `constraint` A value from one register is never used to style another. `src: Front-end specification, the three registers`
- [ ] `C-FE-03` `ui` The page ground is a near-white neutral with body text a near-black neutral. `src: Front-end specification, colour by role`
- [ ] `C-FE-04` `ui` Link text is a near-black neutral at reduced alpha. `src: Front-end specification, colour by role`
- [ ] `C-FE-05` `ui` Hairlines, field borders take a near-white neutral one step darker than the media ground. `src: Front-end specification, colour by role`
- [ ] `C-FE-06` `ui` The primary button ground is a mid, vivid blue with near-white neutral text. `src: Front-end specification, colour by role`
- [ ] `C-FE-07` `ui` The badge ground is a near-white neutral with a near-black neutral border, near-black neutral text. `src: Front-end specification, colour by role`
- [ ] `C-FE-08` `ui` The dark bands take two near-black neutral values one step apart. `src: Front-end specification, colour by role`
- [ ] `C-FE-09` `ui` The announcement bar text rests at three-quarter alpha. `src: Front-end specification, colour by role`
- [ ] `C-FE-10` `ui` Slider controls rest at three-quarter alpha, reaching full strength on hover. `src: Front-end specification, colour by role`
- [ ] `C-FE-11` `ui` Colour tokens are declared as component triples, consumed through an alpha wrapper. `src: Front-end specification, colour by role`
- [ ] `C-FE-12` `ui` The generated photography draws metals from a near-white neutral through a mid, soft orange, a deep neutral. `src: Front-end specification, colour by role`
- [ ] `C-FE-13` `ui` Dial fills run from a near-black warm neutral through a deep, muted red to a near-white warm neutral. `src: Front-end specification, colour by role`
- [ ] `C-FE-14` `literal` The type family is Montserrat, a geometric sans named from a public font host. `src: Front-end specification, type`
- [ ] `C-FE-15` `constraint` The font is installed from a package rather than carried as a file. `src: Front-end specification, type`
- [ ] `C-FE-16` `ui` The fallback stack falls through a system interface sans, a platform sans, a generic sans-serif. `src: Front-end specification, type`
- [ ] `C-FE-17` `constraint` Three faces load rather than six. `src: Front-end specification, type`
- [ ] `C-FE-18` `literal` The body size is 14px over 25.2px, the most-used size in the shop. `src: Front-end specification, type`
- [ ] `C-FE-19` `literal` Product card titles, section body render at 16px over 28.8px. `src: Front-end specification, type`
- [ ] `C-FE-20` `literal` Navigation, footer links render at 15px over 27px. `src: Front-end specification, type`
- [ ] `C-FE-21` `literal` Dense captions render at 14px over 18.9px. `src: Front-end specification, type`
- [ ] `C-FE-22` `literal` The price line renders at 18px over 23.4px. `src: Front-end specification, type`
- [ ] `C-FE-23` `literal` Section headings render at 22px over 39.6px, the page heading at 24px over 43.2px. `src: Front-end specification, type`
- [ ] `C-FE-24` `literal` The product title renders at 24px over 31.2px. `src: Front-end specification, type`
- [ ] `C-FE-25` `literal` The badge renders at 12px over 21.6px, the benefits sublabel at 12px over 16.2px. `src: Front-end specification, type`
- [ ] `C-FE-26` `literal` The drawer labels render at 11.5px over 14.95px. `src: Front-end specification, type`
- [ ] `C-FE-27` `literal` The smallest legal text renders at 10px, the payment mark captions at 9px over 16.2px. `src: Front-end specification, type`
- [ ] `C-FE-28` `ui` The wordmark is set type in a heavy condensed face rather than a vector mark. `src: Front-end specification, type`
- [ ] `C-FE-29` `ui` The root font size is set so one root unit resolves to ten pixels, layout in root units, component detail in pixels. `src: Front-end specification, scaling`
- [ ] `C-FE-30` `ui` The content column is held to a fixed page width, centred, with a gutter each side. `src: Front-end specification, scaling`
- [ ] `C-FE-31` `literal` The grid gutter is 8px at desktop, 4px below the narrow switch. `src: Front-end specification, scaling`
- [ ] `C-FE-32` `constraint` Section spacing is zero, so sections own their internal padding, abutting exactly. `src: Front-end specification, scaling`
- [ ] `C-FE-33` `constraint` Every structural radius is zero on buttons, fields, image frames, text panels, popovers, product cards, collection cards, blog cards. `src: Front-end specification, radius`
- [ ] `C-FE-34` `ui` Every declared border is one hairline thickness except the primary button outset ring. `src: Front-end specification, radius`
- [ ] `C-FE-35` `ui` The image frame hairline sits at a very low alpha, the variant swatch outline at just over half strength. `src: Front-end specification, radius`
- [ ] `C-FE-36` `ui` A field label floats, rising above the field, shrinking, on focus or once the field carries a value. `src: Front-end specification, radius`
- [ ] `C-FE-37` `constraint` Every shadow token is defined with every one but the popover switched off. `src: Front-end specification, radius`
- [ ] `C-FE-38` `constraint` Exactly two shadows render: the currency selector popover cast, an inset hairline ring on the drawer controls. `src: Front-end specification, radius`
- [ ] `C-FE-39` `ui` The focus ring arrival is transitioned fast. `src: Front-end specification, radius`
- [ ] `C-FE-40` `ui` Sixteen marks are drawn by the build rather than fetched, inheriting the colour of the text around them. `src: Front-end specification, iconography`
- [ ] `C-FE-41` `ui` The masthead set is a magnifier, a person, a menu of three bars, a close, a caret. `src: Front-end specification, iconography`
- [ ] `C-FE-42` `ui` The menu bars carry rounded ends rather than square ones. `src: Front-end specification, iconography`
- [ ] `C-FE-43` `ui` The disclosure set is a chevron, a check, an arrow with a shaft, a ringed close, a left chevron. `src: Front-end specification, iconography`
- [ ] `C-FE-44` `constraint` The arrow carries a shaft rather than being a chevron. `src: Front-end specification, iconography`
- [ ] `C-FE-45` `constraint` The ringed close is drawn as two primitives, a circle with a cross of two separate subpaths. `src: Front-end specification, iconography`
- [ ] `C-FE-46` `ui` The cart set is a bag with a handle, a bin, a decrement drawn as one capsule bar with rounded ends. `src: Front-end specification, iconography`
- [ ] `C-FE-47` `ui` The increment mark is the decrement bar plus its vertical twin. `src: Front-end specification, iconography`
- [ ] `C-FE-48` `ui` The bin swaps to a pale mark on a near-black ground under a pointer, the softer remove control to a pale mark on a mid neutral ground. `src: Front-end specification, iconography`
- [ ] `C-FE-49` `constraint` The caret is the only mark the build rotates, carrying a small sideways correction with the rotation. `src: Front-end specification, iconography`
- [ ] `C-FE-50` `ui` One wrapper transform lifts an inline mark to a text baseline, another flips a wrapper through both axes. `src: Front-end specification, iconography`
- [ ] `C-FE-51` `ui` Round icon controls take the capsule radius with a frosted fill. `src: Front-end specification, iconography`
- [ ] `C-FE-52` `ui` Seven durations are declared with the shop using four of them. `src: Front-end specification, motion tokens`
- [ ] `C-FE-53` `ui` Two curves carry the storefront, a default used far more than everything else combined, an entrance curve with no ease in. `src: Front-end specification, motion tokens`
- [ ] `C-FE-54` `ui` A third curve paired with the fastest fade is the fade primitive for anything appearing or disappearing that is not an entrance. `src: Front-end specification, motion tokens`
- [ ] `C-FE-55` `constraint` Every transition the build writes names its properties rather than being blanket. `src: Front-end specification, motion tokens`
- [ ] `C-FE-56` `ui` The keyframe library carries four slide rules forming one paged family, a rise-and-fade entrance, a scale-in, a blur pair, a pulse, a spin, a damped bounce of four stops, a horizontal flip, a background sweep, a stroke reveal. `src: Front-end specification, motion tokens`
- [ ] `C-FE-57` `capability` A reveal trigger plays each element's entrance exactly once per page load, on first intersection. `src: Front-end specification, the reveal system`
- [ ] `C-FE-58` `constraint` A reveal never re-hides an element that has already played. `src: Front-end specification, the reveal system`
- [ ] `C-FE-59` `capability` A reveal shows an element already within the viewport at load without waiting for a scroll event. `src: Front-end specification, the reveal system`
- [ ] `C-FE-60` `capability` A reveal places every element in its final state when the trigger mechanism fails to initialise. `src: Front-end specification, the reveal system`
- [ ] `C-FE-61` `ui` Reveal targets are the product grid container, each grid item, the product information column, the contact form, a blog article card, a rich-text block, the three footer blocks. `src: Front-end specification, the reveal system`
- [ ] `C-FE-62` `constraint` The masthead, the announcement bar, the home hero, the benefits strip, the category row, the banner do not reveal. `src: Front-end specification, the reveal system`
- [ ] `C-FE-63` `capability` The reveal observer stops observing each element once that element has played. `src: Front-end specification, the reveal system`
- [ ] `C-FE-64` `constraint` The build uses a named stacking scale of no more than six levels, never a sentinel value. `src: Front-end specification, layering`
- [ ] `C-FE-65` `constraint` Five slideshows are one component with five configurations rather than five components. `src: Front-end specification, the inventory`
- [ ] `C-FE-66` `constraint` Four overlays are one component with four contents. `src: Front-end specification, the inventory`
- [ ] `C-FE-67` `constraint` Five stores hold state crossing components, no more: the cart, the display currency, the selected variant, the facet with the sort, the open overlay. `src: Front-end specification, the inventory`
- [ ] `C-FE-68` `ui` The product card image reserves a square at the card width before its content arrives. `src: Front-end specification, layout stability`
- [ ] `C-FE-69` `ui` The gallery main frame reserves a square at the column width. `src: Front-end specification, layout stability`
- [ ] `C-FE-70` `ui` The variant swatch grid reserves the full grid at its row count. `src: Front-end specification, layout stability`
- [ ] `C-FE-71` `ui` The review carousel reserves one card height. `src: Front-end specification, layout stability`
- [ ] `C-FE-72` `constraint` The rating row reserves its height when the product has a rating, reserving nothing otherwise. `src: Front-end specification, layout stability`
- [ ] `C-FE-73` `literal` The hidden text layer carries Regular price before every struck-through price. `src: Front-end specification, hidden text`
- [ ] `C-FE-74` `literal` The hidden text layer carries Sale price before every sale price. `src: Front-end specification, hidden text`
- [ ] `C-FE-75` `literal` Each gallery frame carries Open media then its number then in modal, running one through eleven. `src: Front-end specification, hidden text`
- [ ] `C-FE-76` `literal` The gallery counter carries the word of between its two numbers. `src: Front-end specification, hidden text`
- [ ] `C-FE-77` `literal` The struck swatch carries Variant sold out or unavailable. `src: Front-end specification, hidden text`
- [ ] `C-FE-78` `literal` Each stepper carries Decrease quantity for then the product title, Increase quantity for then the product title. `src: Front-end specification, hidden text`
- [ ] `C-FE-79` `literal` The stepper group carries Quantity. `src: Front-end specification, hidden text`
- [ ] `C-FE-80` `literal` Each facet option carries In stock (161 products), Out of stock (13 products). `src: Front-end specification, hidden text`
- [ ] `C-FE-81` `literal` A collection title carries Collection: before the title. `src: Front-end specification, hidden text`
- [ ] `C-FE-82` `literal` The account mark carries Log in, the cart mark carries Cart. `src: Front-end specification, hidden text`
- [ ] `C-FE-83` `constraint` The two quantity strings interpolate the product title. `src: Front-end specification, hidden text`
- [ ] `C-FE-84` `literal` The two skip links read Skip to content on every route, Skip to product information on a product route. `src: Front-end specification, hidden text`
- [ ] `C-FE-85` `constraint` The facet counts are announced as one string rather than as a label with a parenthesised number in two elements. `src: Front-end specification, hidden text`
- [ ] `C-FE-86` `ui` One first-level heading stands per route, with the heading order beneath descending without gaps. `src: Front-end specification, hidden text`
- [ ] `C-FE-87` `constraint` The product route carries its title twice, the second at a lower level. `src: Front-end specification, hidden text`
- [ ] `C-FE-88` `constraint` The build ships no binary of any kind, replacing every asset class by a procedure. `src: Front-end specification, generated imagery`
- [ ] `C-FE-89` `capability` One deterministic generator seeded on a handle draws every photograph as vector primitives on a pale ground at a square aspect. `src: Front-end specification, generated imagery`
- [ ] `C-FE-90` `constraint` The same handle produces the same watch forever, so one product matches across every surface. `src: Front-end specification, generated imagery`
- [ ] `C-FE-91` `ui` The generator draws a case as a circle or a cushion, a gradient case fill from a metal set of steel, gold, rose, black, a bezel annulus fluted or smooth, a dial from a set of eight, twelve indices as bars, roman numerals, arabic numerals or stones, three hands, a bracelet or strap, a contact shadow. `src: Front-end specification, generated imagery`
- [ ] `C-FE-92` `constraint` The generator produces visibly different watches for different handles at thumbnail size. `src: Front-end specification, generated imagery`
- [ ] `C-FE-93` `ui` Media beyond the first are the same watch at other framings, at most four distinct framings repeated. `src: Front-end specification, generated imagery`
- [ ] `C-FE-94` `ui` Category tiles use the generator on a near-black circular ground with a larger case, no contact shadow, seeded on the collection handle. `src: Front-end specification, generated imagery`
- [ ] `C-FE-95` `ui` Hero, banner bands use a gradient field with a soft elliptical light, the watch off centre at a larger scale, a mirrored reflection, the left third under a dark wash. `src: Front-end specification, generated imagery`
- [ ] `C-FE-96` `constraint` The banner type is set rather than drawn into the image. `src: Front-end specification, generated imagery`
- [ ] `C-FE-97` `ui` Review photographs use the generator small, off centre at a seeded tilt, over three overlapping pale blobs with a warm overlay across one corner. `src: Front-end specification, generated imagery`
- [ ] `C-FE-98` `constraint` Review photographs look worse than the catalogue photography, deliberately. `src: Front-end specification, generated imagery`
- [ ] `C-FE-99` `ui` The upsell mark is a square with a diagonal gradient from a mid, vivid green to a deep, vivid teal carrying a pale shield with an isometric cube of three rhombi. `src: Front-end specification, generated imagery`
- [ ] `C-FE-100` `ui` Payment, social marks are abstract geometry on a small rounded rectangle with a hairline, each a seeded arrangement of two to four primitives. `src: Front-end specification, generated imagery`
- [ ] `C-FE-101` `constraint` Real payment network marks are never reproduced; the slots stay abstract. `src: Front-end specification, generated imagery`
- [ ] `C-FE-102` `constraint` Product video is not substituted; the slot takes the generated banner field at the column aspect, static. `src: Front-end specification, generated imagery`
- [ ] `C-FE-103` `ui` Every content picture carries alternative text naming the product with its colourway. `src: Front-end specification, generated imagery`
- [ ] `C-FE-104` `ui` Scrims, gradients, decorative marks declare themselves decorative, carrying no alternative text. `src: Front-end specification, generated imagery`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The client is Astro with islands, built to a production bundle. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The server renders each route HTML complete with only the interactive parts hydrating. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The hydrated islands are the cart drawer, the variant grid, the facet row, the quantity steppers, the two slideshows, the currency selector. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The HTTP API is Express on Node 20 under /api on the same origin. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The store is PostgreSQL reached at DATABASE_URL read from the environment. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` Billing is killbill reached at PAYMENTS_API_URL. `src: Technical requirements para 2`
- [ ] `C-TR-07` `contract` Every call under the /1.0/kb/ prefix carries HTTP Basic credentials, the tenant key from PAYMENTS_API_KEY, the tenant secret from PAYMENTS_API_SECRET. `src: Technical requirements para 2`
- [ ] `C-TR-08` `literal` The Basic pair is the literal admin with the literal password. `src: Technical requirements para 2`
- [ ] `C-TR-09` `contract` Every billing write carries a header naming the writer. `src: Technical requirements para 2`
- [ ] `C-TR-10` `constraint` killbill holds accounts, catalogue plans, subscriptions, invoices, with no charge object, no card token, no decline semantics. `src: Technical requirements para 2`
- [ ] `C-TR-11` `contract` GET /1.0/healthcheck is the unauthenticated liveness route, never /1.0/kb/healthcheck. `src: Technical requirements para 2`
- [ ] `C-TR-12` `contract` The referenceable billing surface is the account lookup by externalKey, the account write, the account pagination, the catalogue base plans, the invoice pagination. `src: Technical requirements para 2`
- [ ] `C-TR-13` `contract` The account lookup answers with the account when present, as not found otherwise. `src: Technical requirements para 2`
- [ ] `C-TR-14` `contract` The account write refuses a taken externalKey as a conflict. `src: Technical requirements para 2`
- [ ] `C-TR-15` `contract` The invoice pagination reports an amount as a decimal rather than in minor units, a currency in uppercase. `src: Technical requirements para 2`
- [ ] `C-TR-16` `constraint` Refunds, payment methods, chargebacks are not part of the billing surface. `src: Technical requirements para 2`
- [ ] `C-TR-17` `contract` Mail leaves over real SMTP through mailpit at SMTP_HOST, SMTP_PORT, with SMTP_USER, SMTP_PASS read from the environment. `src: Technical requirements para 3`
- [ ] `C-TR-18` `constraint` No third-party mail vendor, no API key exists. `src: Technical requirements para 3`
- [ ] `C-TR-19` `constraint` The backing services are already running, so no copy of one is downloaded, installed, compiled, started. `src: Technical requirements para 4`
- [ ] `C-TR-20` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements para 5`
- [ ] `C-TR-21` `constraint` No authentication scheme, no session store, no user token exists in the product. `src: Technical requirements para 6`
- [ ] `C-TR-22` `constraint` The cart token is an opaque session identifier rather than a credential. `src: Technical requirements para 6`
- [ ] `C-TR-23` `contract` GET /api/health returns 200 once the app is ready. `src: Technical requirements para 7`
- [ ] `C-TR-24` `contract` The app writes one structured JSON record per HTTP request to /app/logs/requests.log carrying a method key with a path key. `src: Technical requirements para 7`
- [ ] `C-TR-25` `contract` Each page view is recorded with its route with a timestamp, readable at GET /api/page-views, newest first. `src: Technical requirements, page views`
- [ ] `C-TR-26` `constraint` Every internal link on every public route resolves. `src: Technical requirements, internal links`
- [ ] `C-TR-27` `contract` Every response carries the standard security headers with a strict transport policy, a nosniff content-type policy. `src: Technical requirements, security headers`
- [ ] `C-TR-28` `contract` The security headers stand on the HTML document, on every API response, on the two machine routes alike. `src: Technical requirements, security headers`
- [ ] `C-TR-29` `contract` A sitemap at /sitemap.xml lists every public route. `src: Technical requirements, sitemap`
- [ ] `C-TR-30` `contract` A robots file at /robots.txt names the sitemap. `src: Technical requirements, sitemap`
- [ ] `C-TR-31` `constraint` Both machine routes are served by the application rather than written by hand into a static directory. `src: Technical requirements, sitemap`
- [ ] `C-TR-32` `constraint` A presentation primitive renders identically on every route apart from the ground beneath. `src: Technical requirements, primitives`
- [ ] `C-TR-33` `literal` Script executed before first interaction stays within 250 kilobytes compressed. `src: Technical requirements, budgets`
- [ ] `C-TR-34` `literal` The stylesheet stays within 80 kilobytes compressed. `src: Technical requirements, budgets`
- [ ] `C-TR-35` `literal` Fonts are one family, three faces, within 120 kilobytes in total. `src: Technical requirements, budgets`
- [ ] `C-TR-36` `literal` One image loads above the fold, which may be large. `src: Technical requirements, budgets`
- [ ] `C-TR-37` `literal` Requests before first render stay within 20. `src: Technical requirements, budgets`
- [ ] `C-TR-38` `constraint` The one image above the fold loads eagerly with every other image deferring until approaching the viewport. `src: Technical requirements, loading order`
- [ ] `C-TR-39` `constraint` Images are served in a modern format with a fallback. `src: Technical requirements, loading order`

## C-DM Data model

- [ ] `C-DM-01` `data` Nine tables carry the shop: products, variants, collections, collection_products, carts, cart_lines, orders, newsletter_signups, page_views. `src: Data model para 1`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-03` `contract` The file at /app/USER_README.md states that no credentials exist rather than listing any. `src: Data model para 2`
- [ ] `C-DM-04` `data` The products table holds 174 rows carrying handle, title, maker, model, body, features, includes, rating_score, rating_count, badges, available, house_order. `src: Data model, products`
- [ ] `C-DM-05` `data` A product handle is unique, serving as the address segment. `src: Data model, products`
- [ ] `C-DM-06` `constraint` The maker field is never parsed out of the title. `src: Data model, products`
- [ ] `C-DM-07` `data` The catalogue carries at least five distinct makers with VOLARI among them. `src: Data model, products`
- [ ] `C-DM-08` `data` The rating value, the rating count are nullable together. `src: Data model, products`
- [ ] `C-DM-09` `literal` The rating value carries one decimal place over a measured range of 4.3 to 5.0. `src: Data model, products`
- [ ] `C-DM-10` `literal` The rating count is an integer over a measured range of 8 to 197. `src: Data model, products`
- [ ] `C-DM-11` `data` The variants table carries id, product_handle, option_name, option_value, price_minor, compare_at_minor, available, media_seed, house_order. `src: Data model, variants`
- [ ] `C-DM-12` `constraint` The price, the availability are per variant rather than per product. `src: Data model, variants`
- [ ] `C-DM-13` `data` Variant prices are integers in store minor units in the store currency usd. `src: Data model, variants`
- [ ] `C-DM-14` `data` The collections table holds eleven rows carrying handle, title, description, house_order. `src: Data model, collections`
- [ ] `C-DM-15` `literal` The catch-all is handled all, titled Products, carrying no description. `src: Data model, collections`
- [ ] `C-DM-16` `literal` The ten curated handles are mens-watches, womens-watches, couple-watches, car-watches, quartz-watches, mechanical-watches, automatic-watch, best-sellers, 2-watch-bundle-offer, watch-accessories. `src: Data model, collections`
- [ ] `C-DM-17` `data` Membership lives in collection_products carrying collection_handle, product_handle, position. `src: Data model, collections`
- [ ] `C-DM-18` `data` The carts table carries token, currency, discount_code, note, created_at. `src: Data model, carts`
- [ ] `C-DM-19` `data` The cart_lines table carries key, cart_token, variant_id, quantity, position, promotion_owned. `src: Data model, carts`
- [ ] `C-DM-20` `constraint` The line position is insertion order, never changing. `src: Data model, carts`
- [ ] `C-DM-21` `data` The orders table carries reference, cart_token, email, currency, total_minor, created_at. `src: Data model, orders`
- [ ] `C-DM-22` `data` The order reference is unique, carried as the billing account externalKey. `src: Data model, orders`
- [ ] `C-DM-23` `data` The newsletter_signups table carries email, code, created_at, unique on email. `src: Data model, signups`
- [ ] `C-DM-24` `data` The page_views table carries route, viewed_at. `src: Data model, signups`
- [ ] `C-DM-25` `constraint` A collection's stated product count equals the sum of its availability facet counts. `src: Data model, invariants`
- [ ] `C-DM-26` `literal` The catch-all reports 174 products with 161 in stock, 13 out of stock. `src: Data model, invariants`
- [ ] `C-DM-27` `constraint` Two identical requests for the same collection, facet selection, sort, page return the same products in the same order. `src: Data model, invariants`
- [ ] `C-DM-28` `constraint` A second order under an existing reference creates no second billing account. `src: Data model, invariants`
- [ ] `C-DM-29` `constraint` No endpoint writes to products, variants, collections or collection_products. `src: Data model, invariants`
- [ ] `C-DM-30` `constraint` A refused catalogue write leaves the row count, the row contents unchanged. `src: Data model, invariants`
- [ ] `C-DM-31` `data` The seed carries 174 products across 11 collections with at least five distinct makers. `src: Data model, seed data`
- [ ] `C-DM-32` `data` The seed carries the twelve home products, the three colourway sets, the shipping-protection product. `src: Data model, seed data`
- [ ] `C-DM-33` `data` Exactly 161 seeded products are available where 13 are not. `src: Data model, seed data`
- [ ] `C-DM-34` `constraint` Seeding is idempotent, so restarting the app duplicates no row, changes no count. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No wish list, no comparison table, no recently-viewed rail ships. `src: Constraints`
- [ ] `C-CN-02` `constraint` No stock countdown, no visitor counter, no urgency timer, no chat widget ships. `src: Constraints`
- [ ] `C-CN-03` `constraint` Nothing behind the sign-in handoff ships: no order history, no saved addresses, no profile editing, no order tracking. `src: Constraints`
- [ ] `C-CN-04` `constraint` No breadcrumb appears on any route except the product route. `src: Constraints`
- [ ] `C-CN-05` `constraint` The storefront implements no payment handling, no tax resolution, no address validation. `src: Constraints`
- [ ] `C-CN-06` `constraint` No sort control other than the nine named options, no facet other than availability. `src: Constraints`
- [ ] `C-CN-07` `constraint` No external network call happens at runtime beyond the three named backing services. `src: Constraints`
- [ ] `C-CN-08` `constraint` No third-party script, no analytics endpoint, no tracking pixel, no font fetched from another origin. `src: Constraints`
- [ ] `C-CN-09` `constraint` No binary asset is fetched from any origin outside the application on any route. `src: Constraints`
- [ ] `C-CN-10` `constraint` The only binaries the application carries are the three font faces from the build-time package. `src: Constraints`
- [ ] `C-CN-11` `constraint` No native application, no separate mobile site ships. `src: Constraints`
- [ ] `C-CN-12` `constraint` The shop stays responsive across 174 products, 11 collections, with the facet panel open. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at APP_PUBLIC_URL. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is APP_PUBLIC_PORT over 4173 with both values read from the environment. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the /api prefix. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The health route returns 200 once ready. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `contract` A reserved .browser_screenshots/ directory exists at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-07` `contract` A reserved .downloads/ directory exists at the app root, empty. `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server rather than a dev server. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, never a child of the shell. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds 0.0.0.0 rather than 127.0.0.1 or localhost. `src: Deployment contract`
- [ ] `C-DC-11` `contract` No edge functions are used. `src: Deployment contract`
- [ ] `C-DC-12` `contract` No persistent volumes, no fixed container names, no custom networks are declared. `src: Deployment contract`
- [ ] `C-DC-13` `contract` The collection endpoint takes sort_by, availability, page, currency, all optional. `src: Deployment contract, API shapes`
- [ ] `C-DC-14` `contract` The collection payload carries title, description, count, facets, products, page, pages. `src: Deployment contract, API shapes`
- [ ] `C-DC-15` `contract` The facets object carries availability mapping in_stock, out_of_stock to their counts. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` A served product carries handle, title, maker, badges, rating, price, compare_at. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `contract` A served price carries amount_minor, formatted, from. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `contract` A served rating is null or carries its value with its count. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `contract` The product endpoint returns handle, title, maker, model, body, features, includes, rating, badges, media, option_name, variants. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `contract` A served variant carries id, option_value, price, compare_at, available, media_seed. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `contract` The cart endpoints add with variant_id, quantity, set a quantity, remove a line, apply a code, each returning the whole cart. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `contract` The checkout endpoint takes email, returning reference, lines, unit_count, total, currency. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `contract` The checkout summary endpoint returns the same object for a reference. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `contract` The newsletter endpoint takes email, returning the accepted signup or the rejection. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `contract` The contact endpoint takes name, email, message, returning the accepted message or the rejection. `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `contract` The page-views endpoint returns a top-level JSON array, newest first, each entry carrying route with viewed_at. `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes`
- [ ] `C-DC-28` `contract` A catalogue write is rejected as a client error, never served, never answered with a server error. `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `contract` An invalid request is rejected as a client error with a reason rather than a server error or a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-30` `contract` The billing account exists as a real record in killbill under the order externalKey at the cart display currency. `src: Deployment contract, no mocks`
- [ ] `C-DC-31` `constraint` An in-memory orders array, a hardcoded success body, an order recorded without the account existing are each a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-32` `contract` The signup email exists as a real message delivered over SMTP to the address typed. `src: Deployment contract, no mocks`
- [ ] `C-DC-33` `constraint` A row in a table saying mail was sent is not mail. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Limited 2-Watch Offer - Buy 1, Get 1 Free` | announcement message one | C-CF-47 | Core features, the home route rule 1 |
| `Rated 4.8 / 5 by 1,800+ Verified Customers` | announcement message two | C-CF-48 | Core features, the home route rule 1 |
| `30-Day Easy Returns - Shop with Confidence` | announcement message three | C-CF-49 | Core features, the home route rule 1 |
| `Home` | navigation entry | C-CF-56 | Core features, the home route rule 2 |
| `Catalog` | navigation entry | C-CF-56 | Core features, the home route rule 2 |
| `Watches` | navigation entry | C-CF-56 | Core features, the home route rule 2 |
| `Accessories` | navigation entry | C-CF-56 | Core features, the home route rule 2 |
| `Quartz Watch` | submenu entry | C-CF-57 | Core features, the home route rule 2 |
| `Mechanical Watch` | submenu entry | C-CF-57 | Core features, the home route rule 2 |
| `Automatic Watch` | submenu entry | C-CF-57 | Core features, the home route rule 2 |
| `Couple Watches` | submenu entry | C-CF-57 | Core features, the home route rule 2 |
| `Car Watches` | submenu entry | C-CF-57 | Core features, the home route rule 2 |
| `2-WATCH BUNDLE OFFER` | hero primary control | C-CF-64 | Core features, the home route rule 4 |
| `VIEW BEST SELLERS` | hero secondary control | C-CF-65 | Core features, the home route rule 4 |
| `Free International Shipping` | benefit one label | C-CF-69 | Core features, the home route rule 5 |
| `On every order` | benefit one sublabel | C-CF-69 | Core features, the home route rule 5 |
| `Hassle-free policy` | benefit two sublabel | C-CF-70 | Core features, the home route rule 5 |
| `1-Year Warranty` | benefit three label | C-CF-71 | Core features, the home route rule 5 |
| `Quality guaranteed` | benefit three sublabel | C-CF-71 | Core features, the home route rule 5 |
| `Secure Checkout` | benefit four label | C-CF-72 | Core features, the home route rule 5 |
| `256-bit SSL encryption` | benefit four sublabel | C-CF-72 | Core features, the home route rule 5 |
| `Rated 4.8 / 5` | benefit five label | C-CF-73 | Core features, the home route rule 5 |
| `By 1,800+ customers` | benefit five sublabel | C-CF-73 | Core features, the home route rule 5 |
| `Men's Watches` | category tile | C-CF-76 | Core features, the home route rule 6 |
| `Women's Watches` | category tile | C-CF-76 | Core features, the home route rule 6 |
| `Mechanical Watches` | category tile | C-CF-76 | Core features, the home route rule 6 |
| `Quartz Watches` | category tile | C-CF-76 | Core features, the home route rule 6 |
| `Featured products` | featured heading | C-CF-80 | Core features, the home route rule 7 |
| `VIEW ALL` | the two view-all controls | C-CF-82 | Core features, the home route rule 8 |
| `1985` | founding year on the banner | C-CF-84 | Core features, the home route rule 9 |
| `1/4` | banner counter | C-CF-86 | Core features, the home route rule 9 |
| `PEACE OF MIND` | warranty eyebrow | C-CF-92 | Core features, the home route rule 11 |
| `1-Year Warranty - Confidence in Every Moment` | warranty heading | C-CF-93 | Core features, the home route rule 11 |
| `VIEW WARRANTY POLICY` | warranty control | C-CF-94 | Core features, the home route rule 11 |
| `Get 10% Off Your First Order` | signup heading | C-CF-96 | Core features, the home route rule 12 |
| `Email` | signup field label | C-CF-98 | Core features, the home route rule 12 |
| `Sale` | the sale badge | C-CF-102 | Core features, the product card rule 1 |
| `Buy 1 Get 1 Free` | the bundle badge | C-CF-103 | Core features, the product card rule 1 |
| `Sold out` | the unavailable price line | C-CF-105 | Core features, the product card rule 1 |
| `ADDIESDIVE AD2503 Oceanmaster Automatic - Miyota 8215` | other-maker title | C-CF-107 | Core features, the product card rule 2 |
| `CRRJU 2165 Grace Minimalist Quartz` | other-maker title | C-CF-107 | Core features, the product card rule 2 |
| `LONGLUX 6269K2 Vanguard Skeleton Automatic` | other-maker title | C-CF-107 | Core features, the product card rule 2 |
| `LONGLUX 8020P Heritage Open Heart Mechanical` | other-maker title | C-CF-107 | Core features, the product card rule 2 |
| `LONGLUX 8057G Apex Skeleton Mechanical` | other-maker title | C-CF-107 | Core features, the product card rule 2 |
| `LUMINOUS MILITARY Heritage Automatic` | other-maker title | C-CF-107 | Core features, the product card rule 2 |
| `VOLARI 2628 - Timeless Luxury Quartz Watch` | home product one | C-CF-114 | Core features, the twelve products |
| `VOLARI 2653 Sport Silicone Watch` | home product two | C-CF-115 | Core features, the twelve products |
| `VOLARI 2632 - Waterproof Stainless Steel Watch` | home product three | C-CF-116 | Core features, the twelve products |
| `VOLARI 2627 - Diamond Scale Quartz Watch` | home product four | C-CF-117 | Core features, the twelve products |
| `VOLARI 2309 - Luxury Quartz Chronograph Waterproof Watch` | home product five | C-CF-118 | Core features, the twelve products |
| `VOLARI 2638 - Classic Fluted Men's Watch` | home product six | C-CF-119 | Core features, the twelve products |
| `VOLARI 2506 - Rebel Face Watch` | home product seven | C-CF-120 | Core features, the twelve products |
| `VOLARI 2653 Steel - Classic Edition` | home product eight | C-CF-121 | Core features, the twelve products |
| `VOLARI 2622 - Elegant Zircon Women's Quartz Watch` | home product nine | C-CF-122 | Core features, the twelve products |
| `VOLARI 2697 - Women's Business Watch` | home product ten | C-CF-123 | Core features, the twelve products |
| `VOLARI 2357 - Crystal Elegance Women's Watch` | home product eleven | C-CF-124 | Core features, the twelve products |
| `VOLARI 2675 - Dreamy Fish Tail Watch` | home product twelve | C-CF-125 | Core features, the twelve products |
| `37400` | product one compare-at | C-CF-114 | Core features, the twelve products |
| `18700` | product one price | C-CF-114 | Core features, the twelve products |
| `29000` | product two compare-at | C-CF-115 | Core features, the twelve products |
| `14500` | product two price | C-CF-115 | Core features, the twelve products |
| `16000` | product three compare-at | C-CF-116 | Core features, the twelve products |
| `8000` | product three price | C-CF-116 | Core features, the twelve products |
| `14400` | product four compare-at | C-CF-117 | Core features, the twelve products |
| `18600` | product five compare-at | C-CF-118 | Core features, the twelve products |
| `9300` | product five price | C-CF-118 | Core features, the twelve products |
| `20400` | product six compare-at | C-CF-119 | Core features, the twelve products |
| `10200` | product six price | C-CF-119 | Core features, the twelve products |
| `24800` | product seven compare-at | C-CF-120 | Core features, the twelve products |
| `12400` | product seven price | C-CF-120 | Core features, the twelve products |
| `20600` | product nine compare-at | C-CF-122 | Core features, the twelve products |
| `13000` | product ten compare-at | C-CF-123 | Core features, the twelve products |
| `9200` | product ten cheapest colourway | C-CF-123 | Core features, the twelve products |
| `12600` | product eleven compare-at | C-CF-124 | Core features, the twelve products |
| `10100` | product eleven price | C-CF-124 | Core features, the twelve products |
| `10500` | product twelve compare-at | C-CF-125 | Core features, the twelve products |
| `8400` | product twelve price | C-CF-125 | Core features, the twelve products |
| `Filter:` | the facet row label | C-CF-130 | Core features, the collection route rule 1 |
| `Availability` | the one facet | C-CF-130 | Core features, the collection route rule 1 |
| `Sort by:` | the sort label | C-CF-131 | Core features, the collection route rule 1 |
| `0 selected` | facet panel state | C-CF-132 | Core features, the collection route rule 1 |
| `Reset` | facet panel control | C-CF-132 | Core features, the collection route rule 1 |
| `Remove all` | facet panel control | C-CF-132 | Core features, the collection route rule 1 |
| `174 products` | the catch-all result count | C-CF-133 | Core features, the collection route rule 2 |
| `In stock` | facet option | C-CF-133 | Core features, the collection route rule 2 |
| `Out of stock` | facet option | C-CF-133 | Core features, the collection route rule 2 |
| `161` | the in-stock facet count | C-CF-133 | Core features, the collection route rule 2 |
| `13` | the out-of-stock facet count | C-CF-133 | Core features, the collection route rule 2 |
| `Featured` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Most relevant` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Best selling` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Alphabetically, A-Z` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Alphabetically, Z-A` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Price, low to high` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Price, high to low` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Date, old to new` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `Date, new to old` | sort option | C-CF-135 | Core features, the collection route rule 3 |
| `sort_by` | the sort query key | C-CF-136 | Core features, the collection route rule 4 |
| `availability` | the facet query key | C-CF-136 | Core features, the collection route rule 4 |
| `page` | the page query key | C-CF-136 | Core features, the collection route rule 4 |
| `Filter` | the small-viewport control | C-CF-139 | Core features, the collection route rule 6 |
| `Apply` | the small-viewport commit | C-CF-140 | Core features, the collection route rule 6 |
| `TrustScore` | the rating label | C-CF-158 | Core features, the product route rule 5 |
| `Reviews` | the rating count label | C-CF-158 | Core features, the product route rule 5 |
| `FREE Shipping` | the shipping line | C-CF-162 | Core features, the product route rule 7 |
| `Color` | the option legend | C-CF-163 | Core features, the product route rule 8 |
| `In stock - ready to ship` | the stock line | C-CF-177 | Core features, the product route rule 10 |
| `Sold out` | the unavailable buy control | C-CF-179 | Core features, the product route rule 10 |
| `ADD TO CART` | the buy control | C-CF-180 | Core features, the product route rule 11 |
| `More payment options` | the accelerated paths link | C-CF-182 | Core features, the product route rule 11 |
| `Free Shipping on All Orders` | trust strip item | C-CF-187 | Core features, the product route rule 12 |
| `30-Day Easy Returns` | trust strip item | C-CF-187 | Core features, the product route rule 12 |
| `Why You'll Appreciate It` | feature list heading | C-CF-189 | Core features, the product route rule 13 |
| `What's Included` | inclusions heading | C-CF-190 | Core features, the product route rule 13 |
| `A Watch with Attitude` | closing heading | C-CF-191 | Core features, the product route rule 13 |
| `Bold Graphic Dial` | feature lead | C-CF-192 | Core features, the product route rule 13 |
| `Precision Quartz Movement` | feature lead | C-CF-192 | Core features, the product route rule 13 |
| `Stainless Steel Case` | feature lead | C-CF-192 | Core features, the product route rule 13 |
| `Scratch-Resistant Mineral Crystal` | feature lead | C-CF-192 | Core features, the product route rule 13 |
| `Luminous Hands` | feature lead | C-CF-192 | Core features, the product route rule 13 |
| `Water-Resistant Construction (3ATM)` | feature lead | C-CF-192 | Core features, the product route rule 13 |
| `1x VOLARI Watch` | inclusion | C-CF-193 | Core features, the product route rule 13 |
| `1x Original VOLARI Presentation Box` | inclusion | C-CF-193 | Core features, the product route rule 13 |
| `1x User Manual` | inclusion | C-CF-193 | Core features, the product route rule 13 |
| `1x Bracelet Adjustment Tool` | inclusion | C-CF-193 | Core features, the product route rule 13 |
| `1x Microfiber Cleaning Cloth` | inclusion | C-CF-193 | Core features, the product route rule 13 |
| `You may also like` | related rail heading | C-CF-196 | Core features, the product route rule 15 |
| `Write a review` | reviews band link | C-CF-198 | Core features, the product route rule 16 |
| `Trusted by Countless Customers` | reviews band line | C-CF-198 | Core features, the product route rule 16 |
| `volari-2506-rebel-face-watch` | the deeply specified handle | C-CF-202 | Core features, the deeply specified product |
| `Green Black` | colourway | C-CF-203 | Core features, the deeply specified product |
| `Black Red` | the unavailable colourway | C-CF-203 | Core features, the deeply specified product |
| `Green White` | colourway | C-CF-203 | Core features, the deeply specified product |
| `Red White` | colourway | C-CF-203 | Core features, the deeply specified product |
| `Red Black` | colourway | C-CF-203 | Core features, the deeply specified product |
| `Exclusive Online Offer - Save 50%` | the offer line on that product | C-CF-205 | Core features, the deeply specified product |
| `Rose Gold` | colourway | C-CF-206 | Core features, the deeply specified product |
| `Steel Silver` | colourway | C-CF-206 | Core features, the deeply specified product |
| `Gold` | colourway | C-CF-206 | Core features, the deeply specified product |
| `Silver` | colourway | C-CF-207 | Core features, the deeply specified product |
| `9900` | the unavailable cheapest colourway | C-CF-206 | Core features, the deeply specified product |
| `10400` | the cheapest available colourway | C-CF-206 | Core features, the deeply specified product |
| `11900` | the dearest Diamond Scale colourway | C-CF-206 | Core features, the deeply specified product |
| `10600` | the dearer Business Watch colourway | C-CF-207 | Core features, the deeply specified product |
| `Your cart is empty` | the empty cart heading | C-CF-209 | Core features, the cart page rule 1 |
| `CONTINUE SHOPPING` | the empty cart control | C-CF-210 | Core features, the cart page rule 1 |
| `Have an account?` | the empty cart sign-in heading | C-CF-211 | Core features, the cart page rule 1 |
| `Log in to check out faster.` | the empty cart sign-in line | C-CF-211 | Core features, the cart page rule 1 |
| `Your cart` | the populated cart heading | C-CF-213 | Core features, the cart page rule 2 |
| `Continue shopping` | the cart page link | C-CF-213 | Core features, the cart page rule 2 |
| `PRODUCT` | cart table heading | C-CF-214 | Core features, the cart page rule 2 |
| `QUANTITY` | cart table heading | C-CF-214 | Core features, the cart page rule 2 |
| `TOTAL` | cart table heading | C-CF-214 | Core features, the cart page rule 2 |
| `Estimated total` | the cart total label | C-CF-216 | Core features, the cart page rule 3 |
| `Free shipping available at checkout!` | the cart shipping note | C-CF-216 | Core features, the cart page rule 3 |
| `CHECKOUT SECURELY` | the cart primary control | C-CF-216 | Core features, the cart page rule 3 |
| `Discount code` | the discount field label | C-CF-217 | Core features, the cart page rule 3 |
| `APPLY` | the discount control | C-CF-217 | Core features, the cart page rule 3 |
| `30-Day Returns` | cart reassurance | C-CF-218 | Core features, the cart page rule 3 |
| `Shipping Protection` | the upsell product | C-CF-33 | Core features, the upsell rule 1 |
| `Protect your order from damage, loss, or theft during shipping.` | the upsell description | C-CF-34 | Core features, the upsell rule 1 |
| `shipping-protection` | the upsell handle | C-CF-35 | Core features, the upsell rule 2 |
| `1000` | the upsell price | C-CF-33 | Core features, the upsell rule 1 |
| `2000` | the upsell compare-at | C-CF-33 | Core features, the upsell rule 1 |
| `Enter shipping address` | the checkout shipping line | C-CF-237 | Core features, the checkout rule 8 |
| `externalKey` | the billing account key field | C-CF-228 | Core features, the checkout rule 4 |
| `usd` | the store currency | C-CF-238 | Core features, money rule 1 |
| `USD` | display currency | C-CF-240 | Core features, money rule 2 |
| `INR` | display currency | C-CF-240 | Core features, money rule 2 |
| `88.0` | the INR display rate | C-CF-240 | Core features, money rule 2 |
| `$ 124.00 USD` | the worked USD rendering | C-CF-245 | Core features, money rule 4 |
| `Rs. 10,912.00 INR` | the worked INR rendering | C-CF-245 | Core features, money rule 4 |
| `Volari Official` | the footer brand heading | C-CF-253 | Core features, the footer rule 2 |
| `MENU` | footer column heading | C-CF-254 | Core features, the footer rule 3 |
| `FOOTER MENU` | footer column heading | C-CF-254 | Core features, the footer rule 3 |
| `CONTACT US` | footer column heading | C-CF-254 | Core features, the footer rule 3 |
| `Refund & Return Policy` | footer menu entry | C-CF-256 | Core features, the footer rule 3 |
| `Payment & Delivery` | footer menu entry | C-CF-256 | Core features, the footer rule 3 |
| `VOLARI Warranty` | footer menu entry | C-CF-256 | Core features, the footer rule 3 |
| `Contact Information` | footer menu entry | C-CF-256 | Core features, the footer rule 3 |
| `Legal Notice` | footer menu entry | C-CF-256 | Core features, the footer rule 3 |
| `Faq` | footer menu entry in sentence case | C-CF-256 | Core features, the footer rule 3 |
| `support@volariofficial.com` | the support address | C-CF-257 | Core features, the footer rule 3 |
| `+1 55 0100-0000` | the support number | C-CF-257 | Core features, the footer rule 3 |
| `NEWSLETTER` | the footer signup heading | C-CF-259 | Core features, the footer rule 4 |
| `Sign up and receive 10% off your first order` | the footer signup line | C-CF-259 | Core features, the footer rule 4 |
| `Refund policy` | footer strip link | C-CF-263 | Core features, the footer rule 6 |
| `Privacy policy` | footer strip link | C-CF-263 | Core features, the footer rule 6 |
| `Terms of service` | footer strip link | C-CF-263 | Core features, the footer rule 6 |
| `Shipping policy` | footer strip link | C-CF-263 | Core features, the footer rule 6 |
| `Contact information` | footer strip link | C-CF-263 | Core features, the footer rule 6 |
| `Legal notice` | footer strip link | C-CF-263 | Core features, the footer rule 6 |
| `Your 10% code: VOLARI10` | the worked signup subject | C-CF-268 | Core features, the signup rule 2 |
| `VOLARI10` | the issued discount code | C-CF-268 | Core features, the signup rule 2 |
| `/cart` | the cart route | C-UF-02 | User flow routes table |
| `/collections/all` | the catch-all route | C-UF-03 | User flow routes table |
| `mens-watches` | collection handle | C-UF-04 | User flow routes table |
| `womens-watches` | collection handle | C-UF-04 | User flow routes table |
| `couple-watches` | collection handle | C-UF-04 | User flow routes table |
| `car-watches` | collection handle | C-UF-04 | User flow routes table |
| `quartz-watches` | collection handle | C-UF-04 | User flow routes table |
| `mechanical-watches` | collection handle | C-UF-04 | User flow routes table |
| `automatic-watch` | collection handle | C-UF-04 | User flow routes table |
| `best-sellers` | collection handle | C-UF-04 | User flow routes table |
| `2-watch-bundle-offer` | collection handle | C-UF-04 | User flow routes table |
| `watch-accessories` | collection handle | C-UF-04 | User flow routes table |
| `/pages/about-us` | authored page route | C-UF-06 | User flow routes table |
| `/pages/contact` | authored page route | C-UF-06 | User flow routes table |
| `/pages/faq` | authored page route | C-UF-06 | User flow routes table |
| `/pages/volari-warranty` | authored page route | C-UF-06 | User flow routes table |
| `/pages/payment-delivery` | authored page route | C-UF-06 | User flow routes table |
| `/blogs/watch-guide` | the blog index route | C-UF-07 | User flow routes table |
| `/policies/refund-policy` | policy route | C-UF-08 | User flow routes table |
| `/policies/shipping-policy` | policy route | C-UF-08 | User flow routes table |
| `/policies/privacy-policy` | policy route | C-UF-08 | User flow routes table |
| `/policies/terms-of-service` | policy route | C-UF-08 | User flow routes table |
| `/policies/legal-notice` | policy route | C-UF-08 | User flow routes table |
| `/policies/contact-information` | policy route | C-UF-08 | User flow routes table |
| `/customer_authentication/redirect` | the sign-in handoff route | C-UF-09 | User flow routes table |
| `/checkout` | the checkout route | C-UF-11 | User flow routes table |
| `/sitemap.xml` | the sitemap route | C-UF-12 | User flow routes table |
| `/robots.txt` | the robots route | C-UF-12 | User flow routes table |
| `Montserrat` | the type family | C-FE-14 | Front-end specification, type |
| `14px` | the body size | C-FE-18 | Front-end specification, type |
| `25.2px` | the body line height | C-FE-18 | Front-end specification, type |
| `16px` | the card title size | C-FE-19 | Front-end specification, type |
| `28.8px` | the card title line height | C-FE-19 | Front-end specification, type |
| `15px` | the navigation link size | C-FE-20 | Front-end specification, type |
| `27px` | the navigation link line height | C-FE-20 | Front-end specification, type |
| `18.9px` | the dense caption line height | C-FE-21 | Front-end specification, type |
| `18px` | the price line size | C-FE-22 | Front-end specification, type |
| `23.4px` | the price line height | C-FE-22 | Front-end specification, type |
| `22px` | the section heading size | C-FE-23 | Front-end specification, type |
| `39.6px` | the section heading line height | C-FE-23 | Front-end specification, type |
| `24px` | the page heading size | C-FE-23 | Front-end specification, type |
| `43.2px` | the page heading line height | C-FE-23 | Front-end specification, type |
| `31.2px` | the product title line height | C-FE-24 | Front-end specification, type |
| `12px` | the badge size | C-FE-25 | Front-end specification, type |
| `21.6px` | the badge line height | C-FE-25 | Front-end specification, type |
| `16.2px` | the benefits sublabel line height | C-FE-25 | Front-end specification, type |
| `11.5px` | the drawer label size | C-FE-26 | Front-end specification, type |
| `14.95px` | the drawer label line height | C-FE-26 | Front-end specification, type |
| `10px` | the smallest legal text size | C-FE-27 | Front-end specification, type |
| `9px` | the payment caption size | C-FE-27 | Front-end specification, type |
| `8px` | the desktop grid gutter | C-FE-31 | Front-end specification, scaling |
| `4px` | the small-viewport grid gutter | C-FE-31 | Front-end specification, scaling |
| `Regular price` | hidden string | C-FE-73 | Front-end specification, hidden text |
| `Sale price` | hidden string | C-FE-74 | Front-end specification, hidden text |
| `Variant sold out or unavailable` | hidden string | C-FE-77 | Front-end specification, hidden text |
| `Quantity` | hidden string on the stepper group | C-FE-79 | Front-end specification, hidden text |
| `In stock (161 products)` | hidden facet string | C-FE-80 | Front-end specification, hidden text |
| `Out of stock (13 products)` | hidden facet string | C-FE-80 | Front-end specification, hidden text |
| `Collection:` | hidden string | C-FE-81 | Front-end specification, hidden text |
| `Log in` | hidden string on the account mark | C-FE-82 | Front-end specification, hidden text |
| `Cart` | hidden string on the cart mark | C-FE-82 | Front-end specification, hidden text |
| `Skip to content` | the first skip link | C-FE-84 | Front-end specification, hidden text |
| `Skip to product information` | the second skip link | C-FE-84 | Front-end specification, hidden text |
| `DATABASE_URL` | the store connection variable | C-TR-05 | Technical requirements para 1 |
| `PAYMENTS_API_URL` | the billing base variable | C-TR-06 | Technical requirements para 2 |
| `PAYMENTS_API_KEY` | the billing tenant key variable | C-TR-07 | Technical requirements para 2 |
| `PAYMENTS_API_SECRET` | the billing tenant secret variable | C-TR-07 | Technical requirements para 2 |
| `admin` | the billing Basic user | C-TR-08 | Technical requirements para 2 |
| `password` | the billing Basic password | C-TR-08 | Technical requirements para 2 |
| `SMTP_HOST` | the mail host variable | C-TR-17 | Technical requirements para 3 |
| `SMTP_PORT` | the mail port variable | C-TR-17 | Technical requirements para 3 |
| `SMTP_USER` | the mail user variable | C-TR-17 | Technical requirements para 3 |
| `SMTP_PASS` | the mail password variable | C-TR-17 | Technical requirements para 3 |
| `200` | the health response | C-TR-23 | Technical requirements para 7 |
| `/app/logs/requests.log` | the structured request log | C-TR-24 | Technical requirements para 7 |
| `method` | request-log record key | C-TR-24 | Technical requirements para 7 |
| `path` | request-log record key | C-TR-24 | Technical requirements para 7 |
| `/api/page-views` | the page-view endpoint | C-TR-25 | Technical requirements, page views |
| `250 kilobytes` | the script budget | C-TR-33 | Technical requirements, budgets |
| `80 kilobytes` | the stylesheet budget | C-TR-34 | Technical requirements, budgets |
| `120 kilobytes` | the font budget | C-TR-35 | Technical requirements, budgets |
| `174` | the catalogue size | C-DM-04 | Data model, products |
| `APP_PUBLIC_URL` | the public address variable | C-DC-01 | Deployment contract |
| `APP_PUBLIC_PORT` | the published port variable | C-DC-02 | Deployment contract |
| `4173` | the container-internal port | C-DC-02 | Deployment contract |
| `/api` | the API prefix | C-DC-03 | Deployment contract |
| `/api/health` | the health route | C-DC-04 | Deployment contract |
| `/app/USER_README.md` | the credential statement file | C-DM-03 | Data model para 2 |
| `.browser_screenshots/` | reserved directory | C-DC-06 | Deployment contract |
| `.downloads/` | reserved directory | C-DC-07 | Deployment contract |
| `0.0.0.0` | the bind address | C-DC-10 | Deployment contract |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the one hundred and sixty-two products beyond the twelve the home route names | C-DM-31 | the count is pinned, the individual rows are the builder's to populate |
| the one or two sentences under each curated collection title | C-DM-14 | the presence is pinned, the wording is the builder's |
| the four lines of the footer brand statement | C-CF-253 | the shape is pinned, the wording is the builder's |
| the review text on a review card | C-CF-199 | the card structure is pinned, the wording is the builder's |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 8 | 10 |
| User roles | 12 | 16 |
| Core features | 240 | 291 |
| User flow | 28 | 34 |
| UI and UX notes | 36 | 42 |
| Front-end specification | 88 | 104 |
| Technical requirements | 33 | 39 |
| Data model | 29 | 34 |
| Constraints | 11 | 12 |
| Deployment contract | 28 | 33 |

Definition of done carries no block of its own: every clause in it restates an obligation
already itemised under Core features, Data model or Deployment contract, so filing it twice
would put one requirement in two places.
