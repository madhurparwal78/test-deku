# VOLARI Official

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, filter a shelf of
watches down, open one, pick a colourway and a quantity, add it to a cart, and carry that
cart through to a checkout whose summary lists exactly the same lines at exactly the same
total, without hitting an error page.

The cart is one object seen in five places at once. A build in which the badge says three
and the checkout summary lists two is broken in the way that loses money, and it looks
completely fine in a screenshot. The billing account the checkout creates must exist as a
real record in `killbill` under the order's own reference, and the discount code a signup
earns must arrive as a real message in `mailpit`; a confirmation the app returns to itself
does not count.

---

## Overview

VOLARI Official is the public storefront of a one-operator watch seller whose whole
proposition is that a watch can look like an expensive one without costing what an expensive
one costs. The site is a catalogue with a till attached: one body of content, the catalogue,
and one action, a purchase.

Most visitors arrive from an advertisement, on a phone, with no loyalty to the maker and no
intention of researching it. They decide from photographs, a star rating, a struck-through
price and a returns promise, in about ninety seconds. That reader dictates the whole
information architecture: the struck-through original appears on every card, on every
product page and in the cart, the star row sits above the price rather than below it, and
seven separate reassurance devices run across the top of the page, under the hero, under the
buy control, in the footer and inside the cart. None of that is decoration; it is the
argument the shop is making, repeated until it is believed.

The product deliberately is not several things. There is no user-generated content and no
on-site review composer: star ratings are read-only. There is no wish list, no comparison
table, no recently-viewed rail, no stock countdown, no visitor counter, no urgency timer and
no chat widget. There is no infinite scroll: a collection pages by numbered controls. The
account area is a sign-in handoff and nothing behind it is part of this build.

The genuinely hard parts, in order. **Cart coherence**: one piece of state projected into
five surfaces that can never disagree. **The colourway grid**: a swatch carries its own
image, its own price and its own availability, and one unavailable swatch must be visibly
struck without disabling the rest of the grid. **Money**: amounts are held in one currency
and displayed in another, and the struck-through original must convert by the same rule as
the sale price, in the same pass. **The upsell line**: the cart contains a line the visitor
did not choose, priced and removable like any other, and it must reach the checkout summary.
**Page height**: routes run from one viewport for the sign-in handoff to eleven screens for
the terms page, and the chrome must hold that whole range without a minimum height that
strands the footer on a short page.

---

## User roles

| Role | Can do |
|---|---|
| `customer` | Read every storefront route without signing in, filter and sort a collection, open a product, select a colourway, set a quantity, add to and adjust a cart, apply a discount code, choose a display currency, sign up for the discount code, send a contact message, and complete a checkout as a guest. **Cannot create, change or delete a product, a variant, a collection or a page, by any route and by any means.** |

There is one role and it is anonymous. The storefront has no account system of its own: no
sign-up form, no session, no user token and no logged-in state. The masthead account control
and the empty cart's `Log in` link both lead to a sign-in handoff, and everything behind that
handoff is out of scope. `/app/USER_README.md` states in plain words that this application
has no credentials.

The catalogue is read-only, and that is enforced **server-side on every endpoint**, not by
the absence of a control in the interface. A direct request that would create, change or
delete a product, a variant, a collection or a page must be refused by the server as an
invalid request, and the stored row must be unchanged afterwards. Serving such a request, or
answering it with a server error, both count as failures.

Signing in must not disturb the cart. A guest cart merges into the account's cart and is
never discarded, and the storefront must be fully usable, and completable, without an
account.

---

## Core features

### The cart, which is the point

1. The cart is a single piece of session state projected into **five** surfaces, and no
   surface fetches it independently: the unit badge on the masthead cart control, the drawer
   that slides over any route, the cart page at `/cart`, the checkout summary, and the
   in-cart count beside the quantity label on a product page.
2. The cart object carries a `token`, the display `currency`, an ordered list of `lines`, a
   `unit_count`, a `subtotal`, an optional `note` and a nullable `discount_code`. Each line
   carries a `key`, a `variant_id`, the product `handle`, `title` and `maker`, the variant
   `option_name` and `option_value`, an `image`, a `unit_price`, a nullable `compare_at`, a
   `quantity` of at least one, a `line_total`, and a `removable` flag that is false only for
   a line a promotion owns.
3. **`unit_count` is the sum of quantities, never the count of lines.** Three lines totalling
   four units make the badge read `4`. This is the cheapest coherence bug to introduce and
   the easiest to catch.
4. **`key` is not `variant_id`.** The same variant occupies two lines when one carries a
   property the other does not, and a build that keys on the variant merges them and loses
   the property.
5. Every mutation goes through one path and returns the **whole cart**, never a delta, which
   is what makes five views reconcilable from one response. Adding appends or increments and
   then opens the drawer. A cart permalink merges into the existing cart rather than
   replacing it. Incrementing and decrementing update in place. Removing deletes the line and
   keeps the rest in order. Applying a discount attaches the code, re-prices and reports a
   rejection inline. Setting a note attaches without re-pricing. There is no single control
   that empties the cart: a cart is emptied by removing every line.
6. A mutation is optimistic in the view that caused it and authoritative everywhere. Press
   increment in the drawer and the drawer's number changes at once, the badge follows from
   the same state update, and a rejected change reverts the drawer to the value the server
   returned. A build in which the badge waits for a round trip while the drawer does not is
   the coherence failure in its most common form.
7. **Line order is insertion order and never changes.** A visitor who increments the second
   of three lines and watches it jump to the top will believe the shop has done something
   else as well.
8. The cart survives a reload, a navigation to any route, and a return after the tab has
   been closed.
9. The drawer opens on every successful add. It does **not** open on an increment from
   within itself and it does **not** open on a page load with a non-empty cart. Both of those
   turn a shop into a nag.
10. The drawer carries, in order: a heading reading `Cart • (0)` when empty and `Cart • (n)`
    when populated, where the number in parentheses is the unit count; the line
    `Your cart is empty` with a `Continue shopping` control when empty; one row per line when
    populated; an offer block for the upsell item; and a checkout control reading
    `Checkout •` followed by the subtotal.
11. A line renders at three densities. The drawer shows a small square image, the title, the
    variant caption, the unit price, a stepper and a bin control. The cart page shows a larger
    square image with a hairline border, the title at a heavier weight, the variant caption,
    the unit price under the title, a bordered stepper of three parts, a bin control as a
    separate dark square immediately to its right, and a right-aligned line total. The
    checkout summary shows a small square image carrying a count disc at its upper right, the
    title, the variant value alone, and a right-aligned line total, and offers no stepper and
    no remove.
12. **The variant caption is the option name, a colon, a space, and the value**, for example
    `Color: Green Black`. A line whose product has no options omits the caption entirely
    rather than rendering an empty one.

### The upsell line

1. The cart contains one line the visitor did not choose: `Shipping Protection`, described as
   `Protect your order from damage, loss, or theft during shipping.`, at `1000` in store minor
   units with a struck-through `2000`.
2. **It is a product record, not a checkout fee.** It has the handle `shipping-protection`, a
   price, a compare-at price, an image and a collection membership, it appears in the
   catch-all collection as an ordinary product with a `Sale` badge, and it behaves like every
   other line: removable, adjustable, and included in the subtotal.
3. It is added at most once per cart, it does not re-add itself after the visitor removes it
   in the same session, and it is never added to an empty cart.
4. **It must not be the only line in a cart.** A cart holding nothing but the upsell is an
   empty cart with a fee, and its checkout control is disabled.
5. It carries no variant caption, because it has no options.
6. Related products on a product page exclude both the product being viewed and this item.

### The home route

One long scroll in eleven bands with **no vertical gap at any boundary**: every boundary is a
hard edge between two grounds. The order is the argument the shop makes and it is fixed.

1. **The announcement bar**, the topmost band, full width, on a near-black neutral ground
   with pale text, rotating three messages in this order:
   `Limited 2-Watch Offer - Buy 1, Get 1 Free`,
   `Rated 4.8 / 5 by 1,800+ Verified Customers`,
   `30-Day Easy Returns - Shop with Confidence`.
   A previous and a next control sit at the left and right edges. The rotation pauses on
   pointer hover and on keyboard focus within the bar, and does not run at all under a
   reduced-motion preference, which shows one message. A message that slides away while it is
   being read is the single most common complaint about this pattern. Where a message carries a
   link, pointing at it drops the link's text colour and its border colour together to
   three-quarter alpha and adds an underline, and the same swap applies to the marks either side
   of it, so a build that colours only the element loses the underline's colour change.
2. **The masthead**, on a pale ground, sitting directly under the announcement bar with no
   gap, carrying three groups on one row: the wordmark at the left, nine navigation entries in
   the middle, and three utility controls at the right for search, account and cart. The
   navigation entries are `Home`, `Catalog`, `Watches`, `Men's`, `Women's`, `About us`,
   `Contact`, `Blog` and `Accessories`. Only `Watches` opens anything: a disclosure holding
   seven entries in this order, `Men's Watches`, `Quartz Watch`, `Mechanical Watch`,
   `Automatic Watch`, `Women's Watches`, `Couple Watches`, `Car Watches`. Three of those seven
   are singular where four are plural; that is the wording as it stands and it is not tidied.
   The current entry is marked and underlined.
3. **The cart badge** sits at the lower right of the cart control when the cart is not empty,
   a filled disc in a mid, vivid blue with pale text, reading the unit count.
4. **The hero banner**, full-bleed, edge to edge, running from the masthead to the benefits
   strip: one photographic band, dark, with the watch occupying the right two thirds and the
   left third dark enough to carry text. Two controls sit at the left, vertically centred,
   side by side: a primary reading `2-WATCH BUNDLE OFFER` on a pale ground with dark text,
   leading to `/collections/2-watch-bundle-offer`, and a secondary reading
   `VIEW BEST SELLERS` on a transparent ground with pale text and a pale hairline border,
   leading to `/collections/best-sellers`. **The hero is one photograph, not a slideshow.**
   The slideshow on this page is two thirds of the way down. A hero that pages changes what
   the page is for: the hero makes one offer, and the visitor either takes it or scrolls.
5. **The benefits strip**, a dark band of five equal columns edge to edge across the full
   viewport width, each a label over a sublabel:
   `Free International Shipping` over `On every order`;
   `30-Day Easy Returns` over `Hassle-free policy`;
   `1-Year Warranty` over `Quality guaranteed`;
   `Secure Checkout` over `256-bit SSL encryption`;
   `Rated 4.8 / 5` over `By 1,800+ customers`.
   All five survive at every width. Dropping two of them on a phone drops them for most of
   the shop's traffic.
6. **The category carousel**, six circular tiles in a row centred in the content column, each
   a watch on a dark circular ground with its name beneath: `Men's Watches`,
   `Women's Watches`, `Mechanical Watches`, `Car Watches`, `Quartz Watches`,
   `Couple Watches`, leading to their collections in that order. A previous and a next
   control sit outside the row at both ends. Six tiles fit the content column at a wide
   desktop width, so the controls are **present and unavailable** there rather than absent: a
   row that grows controls on resize reflows the section under the visitor. The tile is
   circular and the picture inside it is a square crop masked to a circle, with the caption
   outside the circle; rounding the picture container instead clips the strap on every tile.
7. **Featured products**, a heading reading `Featured products` left-aligned at the content
   column edge, then eight product cards in two rows of four.
8. A single control follows that grid, centred, reading `VIEW ALL`, leading to
   `/collections/all`.
9. **The editorial banner slideshow**, full-bleed and photographic and dark, carrying the
   wordmark and `1985` set at the left and the line
   `TIME IS  L U X U R Y   INVEST IN QUALITY.` running across, with the middle word
   letter-spaced far wider than the words either side of it. Beneath the image sits a control
   row on a pale ground: a previous control, the counter `1/4`, and a next control. **Four
   slides, an explicit numeric counter rather than dots, and no autoplay.** The slideshow is
   paged by hand.
10. **The second product row**, four cards on the same component, with a second `VIEW ALL`
    beneath them. Two product rows separated by a full-bleed banner, not one long row: the
    banner is load-bearing, because it is what stops twelve cards reading as an
    undifferentiated grid and it is why the second four register as a second offer.
11. **The warranty split panel**, a two-column band with no gutter between the columns. Left,
    a photograph filling the half exactly and bleeding to the left edge of the viewport.
    Right, a dark panel bleeding to the right edge, carrying an eyebrow reading
    `PEACE OF MIND`, a heading reading `1-Year Warranty - Confidence in Every Moment` set at
    a lighter weight than the section headings elsewhere, three lines of prose, and a control
    reading `VIEW WARRANTY POLICY` with a pale hairline border on a transparent ground,
    leading to `/pages/volari-warranty`. Neither half is inside the content column.
12. **The discount signup block**, on a pale ground, centred: the heading
    `Get 10% Off Your First Order`, the line
    `Receive early access to new releases, limited selections, and exclusive online availability.`,
    and a field labelled `Email` with an inline submit drawn as an arrow.
13. **The footer**, specified below under the global chrome.

### The product card

The single most repeated component in the build, used on the home route, on every collection
and on a product page's related rail. Stacked, left-aligned, with no border, no shadow and no
corner radius, carrying in order: a square image on a pale ground; badges overlaid on the
image's lower left; the title, up to three lines; a rating row of five stars, the score at a
heavier weight, a vertical bar and the review count; the struck-through compare-at price; and
the price.

1. **The badges are a list, not two slots.** `Sale` comes first on a dark ground with pale
   text at the capsule radius; a promotional badge such as `Buy 1 Get 1 Free` comes second on
   a mid, vivid green ground at the same radius. A product carrying no promotion shows one
   badge, a product carrying both shows two side by side in that order, and the layout does
   not shift when the second is absent. `Sold out` replaces the price line.
2. **The card survives a title that does not begin with `VOLARI`.** The catch-all carries
   watches under other maker names, measured as
   `ADDIESDIVE AD2503 Oceanmaster Automatic - Miyota 8215`,
   `CRRJU 2165 Grace Minimalist Quartz`,
   `LONGLUX 6269K2 Vanguard Skeleton Automatic`,
   `LONGLUX 8020P Heritage Open Heart Mechanical`,
   `LONGLUX 8057G Apex Skeleton Mechanical` and
   `LUMINOUS MILITARY Heritage Automatic`. The maker is its own field and is never parsed out
   of the title, because those titles share no shape a parser could rely on.
3. **The rating row is optional per product.** When it is absent the price moves up and
   nothing reserves its space.
4. **The price line takes one of three shapes**: a flat price; a flat price with a
   struck-through original above it; or `From ` followed by a price, with a struck-through
   original. The `From ` form is required whenever a product's variant prices differ, and the
   price it names is **the cheapest AVAILABLE variant, not the cheapest variant**. Showing a
   price for a colourway that is sold out is a promise the shop cannot keep.
5. Pointing at a card fades its image and does nothing else: no lift, no shadow, no scale.

### The twelve products the home route shows

Prices are in store minor units. Every one of these carries the `Sale` badge.

| # | Row | Title | compare_at | price | Promotional badge | Rating |
|---|---|---|---|---|---|---|
| 1 | featured | `VOLARI 2628 - Timeless Luxury Quartz Watch` | `37400` | `18700` | `Buy 1 Get 1 Free` | `4.6` from `154` |
| 2 | featured | `VOLARI 2653 Sport Silicone Watch` | `29000` | `14500` | `Buy 1 Get 1 Free` | `5.0` from `56` |
| 3 | featured | `VOLARI 2632 - Waterproof Stainless Steel Watch` | `16000` | `8000` | none | `4.9` from `35` |
| 4 | featured | `VOLARI 2627 - Diamond Scale Quartz Watch` | `14400` | `10400` | none | `4.3` from `142` |
| 5 | featured | `VOLARI 2309 - Luxury Quartz Chronograph Waterproof Watch` | `18600` | `9300` | none | `4.5` from `176` |
| 6 | featured | `VOLARI 2638 - Classic Fluted Men's Watch` | `20400` | `10200` | none | `4.9` from `8` |
| 7 | featured | `VOLARI 2506 - Rebel Face Watch` | `24800` | `12400` | none | `4.5` from `197` |
| 8 | featured | `VOLARI 2653 Steel - Classic Edition` | `24800` | `12400` | `Buy 1 Get 1 Free` | `4.9` from `11` |
| 9 | second | `VOLARI 2622 - Elegant Zircon Women's Quartz Watch` | `20600` | `9300` | none | `4.9` from `15` |
| 10 | second | `VOLARI 2697 - Women's Business Watch` | `13000` | `9200` | none | `4.9` from `22` |
| 11 | second | `VOLARI 2357 - Crystal Elegance Women's Watch` | `12600` | `10100` | none | `5.0` from `12` |
| 12 | second | `VOLARI 2675 - Dreamy Fish Tail Watch` | `10500` | `8400` | none | `4.8` from `12` |

Products 4 and 10 carry variants whose prices differ, so their cards show the `From ` form
over the cheapest available variant. The rest carry one price across every colourway.

### The collection route

`/collections/all` and the ten curated collections share one template: the collection title
as the page heading; a description, present on a curated collection and absent on the
catch-all; a control row; a four-column grid at desktop; and numbered pagination.

1. **The control row.** Left: the label `Filter:` then one disclosure reading `Availability`
   with a trailing caret. Right: the label `Sort by:`, a select, and the result count
   rendered as the number followed by a space and the word `products`. The facet panel also
   carries `0 selected`, a `Reset` control and a `Remove all` control.
2. The catch-all reports `174 products`. Its availability facet offers `In stock` at `(161)`
   and `Out of stock` at `(13)`. **The facet counts and the result count are computed over the
   same set, so the two facet counts sum to the heading's total.** A shopper who adds up two
   facet counts and gets a different number than the heading has caught the shop being
   careless, and it costs nothing to be right.
3. **The sort options, in this order**: `Featured`, `Most relevant`, `Best selling`,
   `Alphabetically, A-Z`, `Alphabetically, Z-A`, `Price, low to high`, `Price, high to low`,
   `Date, old to new`, `Date, new to old`.
4. **Sort, filter and page number are query parameters on the collection address** under the
   keys `sort_by`, `availability` and `page`, and all three survive a reload and can be
   pasted to somebody else. A build that holds sort state only in memory breaks the back
   button on the one page where a visitor most wants it.
5. **Changing a filter or a sort does not scroll the page.** The grid re-renders in place.
6. Below the narrow switch the control row collapses into a single `Filter` control opening a
   panel headed `Filter`, carrying the result count, the same facets, the same sort select, a
   `Remove all` control and an `Apply` control. **The panel commits on `Apply`; the desktop
   row commits on each change and has no `Apply`.** That asymmetry is deliberate: on a phone
   the panel covers the results, so committing per change would re-render something the
   visitor cannot see.
7. **The grid is four columns at desktop and two below the narrow switch, never one.** Rows
   are not height-matched: a three-line title makes its card taller and the next row starts
   below the tallest card in the previous one. Equalising card heights requires either
   truncating titles or reserving three lines on every card, and both destroy the density the
   hair-thin gutter exists to create.
8. **Pagination is numbered, sixteen products to a page, eleven pages for the catch-all**,
   with a next control. There is no infinite scroll and no load-more. The page number is part
   of the address, so a visitor on page seven who opens a product and presses back returns to
   page seven.

### The product route

1. **A two-column shell** above the fold inside the content column: the gallery on the left
   at roughly half, the information column on the right at roughly half. **The gallery holds
   position while the right column scrolls past it**, and the hold releases before the reviews
   band so the gallery does not follow the visitor into a section it has nothing to do with.
2. **The gallery**: a main frame with a hairline border, and a thumbnail strip of four visible
   frames beneath it with a previous and a next control. Eleven media on the deeply specified
   product, each frame opening a modal at full size, with a counter reading the current number,
   a slash and the total. The strip pages four at a time rather than scrolling freely. The
   active thumbnail carries a solid border and the rest carry the hairline.
3. **The information column above the buy control, in this order**: the breadcrumb; the title;
   the rating; the offer line; the price pair; the shipping line. **The order is rating, then
   offer, then price**: the visitor is given a reason to trust the shop, then a reason to
   believe the discount, and only then the number. Reordering these is a business decision,
   not a layout one.
4. The breadcrumb is three levels separated by a right-pointing angle quotation mark in a
   span of its own, for example `Home  ›  Men's Watches  ›  VOLARI 2506 - Rebel Face Watch`.
   **The middle level is derived from the arrival path, not from a product field.** A product
   reachable from four collections shows whichever one the visitor came through, and shows
   the product's primary collection when the visitor arrived cold. A build that hard-codes one
   collection per product produces a breadcrumb that lies to three quarters of its visitors.
5. The rating renders as a star row, then the label `TrustScore`, the score, a vertical bar,
   the count and the label `Reviews`. The score renders to one decimal place always, so a
   perfect score renders as `5.0` and not as `5`.
6. The offer line reads `Exclusive Online Offer - Save ` followed by the percentage and `%`,
   uppercase, at a heavier weight. **The percentage is computed from the two prices after
   conversion, never authored.** A hard-coded percentage disagrees with the prices the moment
   either changes, and it does so in the most legible place on the page.
7. The shipping line reads `FREE Shipping`.
8. **The colourway grid**, the hardest component in the build. A legend reading `Color`, a
   colon, a space and the selected value, then a row of swatches. Each swatch is a bordered
   tile carrying three things stacked: a thumbnail of the product in that colourway, the
   colourway name, and that colourway's own price. The selected tile carries a heavier border.
   An unavailable tile is struck by a single diagonal line in a mid, vivid red across its
   thumbnail.
   - A swatch carries its own price, and prices may differ between swatches.
   - **An unavailable swatch remains selectable** so its price and image can be seen, and
     selecting it disables the buy control and replaces the stock line. It is not removed and
     it is not made inert.
   - Selecting a swatch updates, in one pass: the gallery position, the price pair, the offer
     percentage, the stock line, the buy control's state, and the address, so a chosen
     colourway can be shared as a link.
   - Selecting a swatch does not scroll the page and does not collapse the grid.
   - Selecting a colourway moves the gallery to that colourway's first image. It does **not**
     filter the gallery down to that colourway's images alone: the gallery carries lifestyle
     and detail frames that belong to no single variant, and losing them on selection loses
     most of the page's persuasion.
   - A second option renders as a second legend and a second row, and availability is computed
     over the combination rather than over either option alone.
9. **The quantity stepper**: a decrement, a value, an increment, bordered as one group. Beside
   its label the page shows how many of this colourway are already in the cart, rendered as
   `Quantity` followed by `( ` the count ` in cart)`. **That count is a live projection of the
   cart for this variant only and changes when the drawer changes.** It is the fifth view of
   the cart object and it must not be the one that disagrees.
10. **The stock line** sits under the stepper: a small filled disc then
    `In stock - ready to ship`. It has three states, available, unavailable and unknown, and
    it never claims availability it has not confirmed. On an unavailable variant it is
    replaced and the buy control reads `Sold out` and is disabled.
11. **The buy controls**, stacked, full width of the information column: `ADD TO CART` on a
    dark ground with pale uppercase letter-spaced text, which adds and opens the drawer; a
    wallet control on a light, vivid indigo ground; and a `More payment options` underlined
    link revealing the remaining accelerated paths.
    - **The buy control is a submit and remains operable when scripting fails**: a plain
      submitted form that lands on `/cart` is the required fallback, and it is the difference
      between a degraded shop and a broken one.
    - **The control shows a pending state between press and confirmation and cannot be pressed
      twice.** Double-adding is the most common cart bug in this category and it is invisible
      until the drawer opens with two lines.
    - The accelerated paths are shortcuts past the checkout, not past the cart. They carry the
      same cart object. A build in which a wallet control submits a different set of lines
      than the ones on screen is the worst version of the coherence failure, because it is the
      one the customer only discovers on their statement.
    - If no wallet is available in the visitor's browser the controls are **absent, not
      disabled**. A dead payment control is worse than no payment control.
12. **The trust strip**, immediately under the payment options, one row of four separated by
    space rather than by rules: `Free Shipping on All Orders`, `30-Day Easy Returns`,
    `Secure Checkout`, `1-Year Warranty`.
13. **The description column**, below the trust strip, in this order: a lifestyle frame, a
    heading repeating the product title, two paragraphs of prose, a heading reading
    `Why You'll Appreciate It` over a six-item feature list with bolded leads, a heading
    reading `What's Included` over an inclusions list, a closing heading reading
    `A Watch with Attitude` with one paragraph, and a `Share` control. The feature leads on
    the deeply specified product are `Bold Graphic Dial`, `Precision Quartz Movement`,
    `Stainless Steel Case`, `Scratch-Resistant Mineral Crystal`, `Luminous Hands` and
    `Water-Resistant Construction (3ATM)`, and its inclusions are `1x VOLARI Watch`,
    `1x Original VOLARI Presentation Box`, `1x User Manual`, `1x Bracelet Adjustment Tool` and
    `1x Microfiber Cleaning Cloth`.
14. Three collapsible panels follow, covering shipping and delivery, the warranty and
    returns. They are collapsed at rest and **render the same source as the editorial pages
    that cover the same ground**, never a second copy.
15. **Related products** under a heading reading `You may also like`, on the card component,
    excluding the product being viewed and the upsell item.
16. **The reviews band**, full-bleed on a pale ground, breaking out of the content column: a
    `Write a review` link, a centred line reading `Trusted by Countless Customers`, a
    horizontally paged carousel of review cards, and a previous and a next control. Each card
    carries a customer photograph of the watch on a wrist, a five-star row, the review text
    centred, and the reviewer's name at the foot at a heavier weight. **The carousel shows
    partial cards at both edges** so it reads as continuing past the viewport in both
    directions; that bleed is the whole reason the band breaks out of the content column.
    `Write a review` links out; there is no composer on this page.

### The deeply specified product

`/products/volari-2506-rebel-face-watch`, title `VOLARI 2506 - Rebel Face Watch`, maker
`VOLARI`, model `2506`, compare-at `24800`, rating `4.5` from `197`, eleven media, carrying
one option named `Color` with five colourways:

| Colourway | Price | Available |
|---|---|---|
| `Green Black` | `12400` | yes |
| `Black Red` | `12400` | **no** |
| `Green White` | `12400` | yes |
| `Red White` | `12400` | yes |
| `Red Black` | `12400` | yes |

Its offer line therefore reads `Exclusive Online Offer - Save 50%`.

Two further products carry colourways whose prices differ:

| Product | Colourway | Price | Available |
|---|---|---|---|
| `VOLARI 2627 - Diamond Scale Quartz Watch` | `Rose Gold` | `9900` | **no** |
| `VOLARI 2627 - Diamond Scale Quartz Watch` | `Steel Silver` | `10400` | yes |
| `VOLARI 2627 - Diamond Scale Quartz Watch` | `Gold` | `11900` | yes |
| `VOLARI 2697 - Women's Business Watch` | `Silver` | `9200` | yes |
| `VOLARI 2697 - Women's Business Watch` | `Gold` | `10600` | yes |

The first of those is the case that separates a correct `From ` form from a plausible one:
its cheapest colourway is unavailable, so its card names `10400` and not `9900`.

### The cart page

1. **The empty state**: a centred heading `Your cart is empty` at the page-heading size, a
   `CONTINUE SHOPPING` control beneath it on a dark ground with the thick outset ring, then a
   centred heading `Have an account?` and the line `Log in to check out faster.` with
   `Log in` underlined. The footer follows immediately: **the empty cart page is chrome and
   one sentence, and no minimum height pushes the footer off screen.**
2. **The populated state**: a heading `Your cart` on the left and a `Continue shopping` link
   underlined on the right of the same row, then a table with three column headings, uppercase
   and subdued: `PRODUCT`, `QUANTITY`, `TOTAL`. Line rows follow, then a hairline rule.
3. **The totals block**, three groups on one row beneath the rule. Left: the label
   `Estimated total` and its value, the line `Free shipping available at checkout!`, a primary
   control reading `CHECKOUT SECURELY` on a dark ground with the thick outset ring, and two
   wallet controls side by side. Centre: a `Discount code` field with an `APPLY` control on a
   dark ground immediately to its right, with no gap. Right: a two-by-two cluster of four
   reassurances under a hairline rule, reading `Secure Checkout`,
   `Free International Shipping`, `30-Day Returns` and `1-Year Warranty`.
4. **`Estimated total` is the cart subtotal and is labelled as an estimate** because shipping
   and tax are resolved in the checkout. **It is never labelled `Total` on this page.** Calling
   it a total here and then showing a different number at the till is how a shop loses somebody
   at the last step.
5. **A rejected discount code reports inline beside the field, without clearing the field and
   without reloading.** An accepted one re-prices the lines and the estimated total in place.

### The checkout

1. **The checkout is a separate surface with its own chrome and none of the storefront's.** It
   carries no announcement bar, no navigation, no footer, no currency selector and no cart
   drawer. Its masthead is the wordmark alone, centred, with a single cart mark on the right.
   Every link offered at the payment stage is a link away from paying.
2. It is entered from four places: the drawer's checkout control, the cart page's
   `CHECKOUT SECURELY`, either wallet control, and a cart permalink.
3. **The handoff carries the whole cart**, including the upsell line and any applied discount
   code. **The line items, quantities and prices the checkout shows are the cart, with no
   additions and no omissions, at the same total.** This is the single most important
   behaviour in the build.
4. Submitting the checkout creates the order and, for it, **exactly one billing account in
   `killbill`**: a write to `/1.0/kb/accounts` carrying `name`, `externalKey`, `email`,
   `currency` and `country`, where `externalKey` is the order reference and `currency` is the
   cart's display currency code in uppercase. The account must be identified by its
   `externalKey` and never by the generated identifier `killbill` returns.
5. **A re-submitted order creates no second account.** `externalKey` is unique per tenant, so
   a repeat is refused by the billing store's own conflict rather than by a guard in the
   application, and the app reports the existing order rather than a failure. The app must
   never show a billing outcome it has not read back from the API.
6. **Cancelling returns to `/cart` with the cart unchanged.** A completed order clears the
   cart, and the badge returns to zero without a reload.
7. The checkout surface is reachable and completable without the storefront's scripting having
   run.
8. The checkout summary renders `Subtotal · ` followed by the unit count and ` items`,
   `Shipping` with the line `Enter shipping address`, and `Total` with its figure and its
   currency code.

### Money

1. Every amount is stored in one store currency, `usd`, as an **integer in minor units**. A
   display currency is a presentation concern and is never stored on a product.
2. Two display currencies exist and the selector offers both: `USD` at a rate of `1.0` and
   `INR` at a rate of `88.0`.
3. **Every price in one response converts by the same rate in the same pass**: the sale price,
   the struck-through original, the swatch prices, the line totals and the estimated total.
   One rate is resolved per request and every price in that response uses it. A build in which
   the sale price converts and the struck-through original does not displays a discount that
   is arithmetically impossible, and it does so on a hundred and seventy-four cards at once.
4. **The rendered format is the currency prefix, a space, the digits grouped by thousands, a
   decimal point, two decimals, a space, and the currency code.** The prefix is `$` for `USD`
   and `Rs.` for `INR`. A price of `12400` store minor units therefore renders as
   `$ 124.00 USD` and as `Rs. 10,912.00 INR`.
5. **The same product shows the same price on the home route and on a collection route at the
   same moment.** Two prices for one product on two surfaces of the same shop is the money
   version of the cart coherence failure.
6. The currency selector is a control fixed to the lower left of the viewport on every
   storefront route, reading the active currency code with a trailing caret, on a pale ground
   with a hairline border and square corners. It is fixed rather than sticky: it stays in the
   lower left corner through every scroll position on every route, including over the dark
   bands, and it must not overlap the footer's own content at the bottom of a page. Its list
   is keyboard-navigable and closes on escape, and it is the one element in the build that
   casts a shadow.

### The global chrome and the footer

1. The footer is a dark band with pale text in five stacked blocks.
2. **The brand block**: a centred heading reading `Volari Official` in uppercase with wide
   letter-spacing, a hairline rule beneath it running the width of the content column, and a
   centred statement of four lines.
3. **Three link columns**, headed `MENU`, `FOOTER MENU` and `CONTACT US`. The `MENU`
   column repeats the masthead's nine entries exactly. The `FOOTER MENU` column carries, in
   this order: `About Us`, `Terms of Service`, `Refund & Return Policy`, `Shipping Policy`,
   `Payment & Delivery`, `Privacy Policy`, `Contact Us`, `VOLARI Warranty`,
   `Contact Information`, `Legal Notice`, `Faq`. The `CONTACT US` column carries two entries
   only, the support address `support@volariofficial.com` and the support number
   `+1 55 0100-0000`.
   Note `Faq` in sentence case where the page it points at titles itself in capitals. That is
   the wording as it stands and it is reproduced.
4. **The newsletter block**: a `NEWSLETTER` heading, the line
   `Sign up and receive 10% off your first order`, and a field labelled `Email` with an inline
   submit drawn as an arrow. This is the second signup field in the build and both post to the
   same list.
5. **The social block**, right-aligned on the same row: a wallet-provider follow control on a
   light, vivid indigo ground, then two social marks.
6. **The payment strip**: thirteen payment marks, then a line carrying the copyright, the
   store name and the platform credit, then six policy links separated by a middle dot,
   reading `Refund policy`, `Privacy policy`, `Terms of service`, `Shipping policy`,
   `Contact information` and `Legal notice`.
7. **Every policy page is linked twice from the footer**, once from the `FOOTER MENU`
   column and once from the strip, so each is reachable two ways from the bottom of any route,
   and the refund policy is linked a third time because the column and the strip use two
   different labels for it. **Two labels for one address is
   deliberate**: the column is written for a shopper and the strip is written for a regulator,
   and they are allowed to use different words.

### The two signup fields, the contact form and the bot refusal

1. Both signup fields post to the same list and both report success and failure **inline, in
   place, without navigating**. A build that navigates on submit loses the visitor's scroll
   position two sections from the bottom of a very long page.
2. A successful signup sends **one email over real SMTP** at `SMTP_HOST` and `SMTP_PORT`,
   addressed to the address the visitor typed, with **no cc and no bcc**. Its subject **begins
   with `Your 10% code: ` followed by the code**, so a signup issued the code `VOLARI10`
   carries the subject `Your 10% code: VOLARI10`. Its body is non-empty and names both the
   code and `Volari Official`.
3. **A rejected signup sends nothing.** A malformed address, a repeat of an address already on
   the list, and a submission refused as a bot each report inline and send no mail.
4. **Every form in the build refuses a bot**: a form carrying a filled unattended decoy field
   is refused, and so is the same form submitted **repeatedly** in quick succession from one
   session. A refused submission writes nothing and sends nothing.
5. The contact form validates its fields **on blur, not on keystroke**, and reports success
   and failure in place without navigating. A contact form that clears itself on a failed
   submit is the worst outcome available to it. It records the message and sends no mail.

### The cookie choice

A first-time visitor is asked once about non-essential **cookie** storage, in a panel carrying
a short heading, one sentence, a link to the privacy page and two controls, one accepting and
one refusing. **The answer survives a reload** and the panel does not return. It is dismissible
before anything behind it is read, it traps the keyboard while open, it returns focus to
whatever opened it, and it closes on the escape key.

### The editorial and policy pages

1. Eleven pages share one single-column template: chrome, a page title, prose in the content
   column, and the footer. **One column, no sidebar, no vertical centring of short content,
   and no maximum width narrower than the content column**, because the brand statement runs
   nearly six screens and reads as a document rather than as a card.
2. The five authored pages are `/pages/about-us`, `/pages/contact`, `/pages/faq`,
   `/pages/volari-warranty` and `/pages/payment-delivery`, and the blog index sits at
   `/blogs/watch-guide`.
3. The six policy pages sit at `/policies/refund-policy`, `/policies/shipping-policy`,
   `/policies/privacy-policy`, `/policies/terms-of-service`, `/policies/legal-notice` and
   `/policies/contact-information`. **The privacy page is reachable from the footer of every
   route and states what the shop stores about a visitor and for how long.**
4. The terms page is the longest document in the build by a wide margin and is unbroken prose.
   **The template carries it without a contents list and without collapsing it**, because a
   legal document that hides its own clauses behind disclosures is worse, not better.
5. `/policies/contact-information` is the shortest and is mostly chrome. Same rule as the
   empty cart: no minimum height, and the footer sits where the content ends.
6. The questions page is a stack of collapsible panels. **Every panel is addressable**, so a
   support agent can link to one answer, and an opened panel scrolls itself into view only if
   it is not already fully visible.
7. The blog index is a grid of article cards. The card is the product card with the price
   furniture removed.
8. **The returns window, the warranty term and the shipping promise are each authored once and
   rendered everywhere they appear.** The returns window appears in six places across this
   build: the announcement bar, the benefits strip, the product trust strip, a product
   collapsible panel, the cart page's reassurance cluster and the refund policy page. The day
   somebody shortens the window, they will change one of the six, and the shop will spend a
   year promising two different things depending on where a visitor looked.

### The account handoff

`/customer_authentication/redirect` is a handoff, not a page. It is reached from the masthead
account control on every storefront route and from the `Log in` link in the empty cart, it
hands off to an authentication surface, and it returns the visitor to the route they left
rather than to `/`.

---

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home, eleven bands | none |
| `/cart` | The cart page | none |
| `/collections/all` | The catch-all, 174 products, eleven pages | none |
| `/collections/mens-watches` | Men's watches | none |
| `/collections/womens-watches` | Women's watches | none |
| `/collections/couple-watches` | Couple watches | none |
| `/collections/car-watches` | Car watches | none |
| `/collections/quartz-watches` | Quartz watches | none |
| `/collections/mechanical-watches` | Mechanical watches | none |
| `/collections/automatic-watch` | Automatic watches | none |
| `/collections/best-sellers` | Best sellers | none |
| `/collections/2-watch-bundle-offer` | The bundle collection | none |
| `/collections/watch-accessories` | Accessories | none |
| `/products/<handle>` | Product detail | none |
| `/pages/about-us` | The brand statement | none |
| `/pages/contact` | The contact form | none |
| `/pages/faq` | The questions page | none |
| `/pages/volari-warranty` | Warranty terms | none |
| `/pages/payment-delivery` | Payment and delivery terms | none |
| `/blogs/watch-guide` | The blog index | none |
| `/policies/refund-policy` | Refunds | none |
| `/policies/shipping-policy` | Shipping | none |
| `/policies/privacy-policy` | Privacy | none |
| `/policies/terms-of-service` | Terms | none |
| `/policies/legal-notice` | Legal notice | none |
| `/policies/contact-information` | Contact information | none |
| `/customer_authentication/redirect` | Sign-in handoff | none |
| `/cart/<variant>:<qty>[,<variant>:<qty>]` | Cart permalink, redirects into the checkout | none |
| `/checkout` | The checkout boundary | none |
| `/sitemap.xml` | Every public route | none |
| `/robots.txt` | Names the sitemap | none |

Filters, sorts and page numbers are query parameters on a collection address under the keys
`sort_by`, `availability` and `page`, never new paths. A product address carries no collection
segment, which is why the breadcrumb's middle level is derived from the arrival path.

### Entry and redirects

Nothing redirects for authentication and no route is protected. **The cart permalink is
reachable from nothing on the site**: it builds a cart from the address itself and sends the
visitor straight into the checkout, skipping every storefront surface between, and it exists
so an advertisement or a support agent can hand a customer a link that skips the shelf. It
merges into whatever cart the session already holds rather than replacing it, and **a
malformed variant reference lands on `/cart` with the existing cart untouched and starts no
checkout for nothing**. An unknown address renders the shop's own not-found page with the
chrome intact and a link back to the home route.

**Four surfaces have no address of their own** and are reachable from every storefront route:
the cart drawer, opened by the masthead cart control and by any successful add; search, opened
by the masthead search control; the `Watches` submenu; and, below the wide switch, the
navigation drawer. **None of them changes the address, all four close on the escape key, and
opening any one closes the other three.** There is no state in which two overlays are open at
once, and a build that allows it produces a cart drawer sliding in behind an open search field.

Search opens a field that takes focus immediately, offers suggestions as the visitor types
without a submit, is dismissable on escape without changing the address, and degrades to a
plain submitted query when suggestions cannot be fetched. Suggestions carry a product's
thumbnail and price and are reachable by keyboard from the field.

### Journeys

1. **Land and browse.** Open `/`. Read the rotating announcement, the hero's two controls,
   the five promises, the six category tiles, the eight cards with their stars and struck
   prices, the wide banner with its `1/4` counter, four more cards, the warranty panel and
   the signup. Scroll back up: nothing that has already arrived plays again.
2. **Filter a shelf.** Open `/collections/all`. The heading reads the collection title and the
   row reads `174 products`. Open the `Availability` facet: `In stock` reads `(161)` and
   `Out of stock` reads `(13)`, which sum to the heading's total. Select `In stock`: the
   address carries it, the grid re-renders in place and the page does not scroll. Choose
   `Price, low to high`: the address carries that too. Reload, and both survive.
3. **Read a watch.** Click the card for `VOLARI 2506 - Rebel Face Watch`. The breadcrumb names
   the collection arrived through. The gallery holds while the description scrolls past it.
   Select `Black Red`: it is struck, it is still selectable, its price and image still show,
   the stock line is replaced and the buy control goes dead. Select `Green Black` again: the
   gallery, the price pair, the offer percentage, the stock line, the buy control and the
   address all change in one pass.
4. **Buy.** Set the quantity to two and press `ADD TO CART` once. It goes busy and refuses a
   second press. The drawer slides over carrying one line at quantity two, the badge reads
   `2`, and the in-cart count beside the quantity label reads `( 2 in cart)`.
5. **Adjust.** Increment in the drawer: the drawer's number and the badge change in the same
   frame. Add a second watch: the badge reads `3`, not `2`. Open `/cart`: the same lines in
   the same order at the same quantities, plus the `Shipping Protection` line. Remove that
   line: it does not come back this session. Reload, and everything is unchanged. Close the
   tab and reopen the shop, and everything is still unchanged.
6. **Check out.** Press `CHECKOUT SECURELY`. The summary lists exactly the lines `/cart`
   listed, at the same prices, at the same total. Cancel: the cart is unchanged. Submit: the
   order exists, one billing account exists under its reference, the cart empties and the
   badge returns to zero without a reload. Submit the same order again: no second account is
   created.
7. **Follow an advertisement.** Holding a cart of two, open a cart permalink for a third
   watch. Arrive with three, not one.
8. **Switch currency.** Press the selector in the lower left corner and choose `INR`. Every
   price on the page changes in one pass, including every struck-through original and every
   swatch price.
9. **Sign up.** Give an address to either signup field. The field reports success in place and
   the code arrives by mail. Submit the same form repeatedly in quick succession: it is
   refused and nothing is sent.

### States

Every list has an empty state: the empty cart is a heading, a control and the footer, and a
collection that matches no product states so in the result region. Every route has a loading
state that holds the layout it will have once loaded, so nothing jumps when content arrives. A
failed data request leaves the chrome standing and states that the catalogue could not be
loaded, with a way to retry; it never blanks the page and never shows a stack trace. **Content
that a script failed to reveal is simply present**: an element that is invisible because a
script did not run is the worst outcome the reveal system can produce, and on a shop what
stays invisible is the products.

---

## UI/UX notes

A stranger arriving from an advertisement should understand within one screen that this shop
sells watches which look expensive and are not, and should be able to get from a photograph to
owning one in as few presses as possible. That sentence is the tiebreak for every judgement
below.

This is a consumer retail storefront, not an operational tool and not an editorial showcase.
The subject of every screen is a watch photographed against a pale ground, and the furniture
gets out of its way. Two stances a competing shop could rationally invert, and this one holds:
**repetition over novelty**, and **the argument over the ornament**. The five promises, the
struck-through price and the star row are repeated until they are believed, and nothing
decorative is allowed to compete with them.

**Colour is almost absent and that is the identity.** The ground is a near-white neutral, text
is a near-black neutral, and the shop has no brand colour in its chrome at all: what a reader
remembers as its look is the photography against white and a black wordmark. Colour appears
only where it carries a job, and each job owns its colour exclusively. A mid, vivid green
carries the bundle badge, deepening toward a vivid teal across the upsell mark's gradient. A
mid, vivid blue carries the cart badge and the primary control, and a deep, vivid blue is that
control under a pointer. A light, vivid indigo carries the wallet control. A mid, vivid red
carries the diagonal across an unavailable swatch and a rejected field, and a deep, muted red
is a dial colour in the generated photography and appears nowhere in the furniture. Subdued
text is a near-black neutral at reduced alpha over the ground rather than a grey chosen to look
right against white. The generated watch metals run through a mid, soft orange for gold and a
near-white neutral for steel. The exact values are yours, so long as each holds its role and
its exclusivity.

**Type is one family in three faces.** Headings and body share the family and differ by weight.
Line height splits in two and that split, not the sizes, is what makes the shop feel airy:
generous for everything a visitor reads at length, tight for everything they scan. The body
size is the default and every larger size is a deliberate exception; eight sizes render the
entire catalogue, six editorial pages and a checkout summary. A build that sets a single line
height across the scale will be legible and will not look like this shop.

**The shop is square.** Buttons, fields, image frames, cards, panels and popovers all carry
hard corners. **Exactly two things are rounded and both are fully rounded capsules**: the sale
badge and the variant pill. That contrast is deliberate and it is most of the personality the
furniture has. The primary control carries a thick outset ring rather than a hairline, which
with square corners gives it a blunt, stamped look.

**Almost nothing casts a shadow.** Every shadow the theme knows how to draw is turned down to
nothing except one, under the currency selector's popover, and that is the only element in the
build that casts one. Cards are held apart from the ground by their edges and by the ground
itself, never by elevation. The depth a reader perceives is the photography, not the design.
**Space over rules**: the trust strip separates its four items by space rather than by
dividers, and the footer's columns sit apart without a line between them.

**Density is tight, deliberately.** The product grid's gutter is a hair, which is what makes
four watches on white read as one continuous shelf rather than as four separate cards. Sections
carry their own internal padding and abut exactly, with no rhythm of vertical margin between
them, so every one of the eleven band boundaries on the home route is a hard edge between two
grounds. A build that adds a section rhythm produces visible pale bands the shop does not have,
at every boundary at once.

**Motion character.** Four speeds and two curves carry the whole build. One curve eases both in
and out and belongs to anything responding to a pointer, so a hover feels like an answer. The
other has no ease in at all and belongs to anything arriving on screen, so an element reads as
already moving and the visitor simply caught up with it. They are the same length and they feel
completely different; swapping them makes hovers twitchy and entrances sluggish, and it is a
one-character mistake to make. Content below the fold **arrives once as it first enters view
and then holds forever**: it does not replay on scrolling back up, and it does not track scroll
position at any point. **Nothing in this build is tied to the scrollbar**: nothing pins, nothing
parallaxes, and no section's progress is bound to how far the page has moved. A build that adds
a scroll-driven effect is not embellishing this shop, it is building a different product. Each
card in a grid arrives on its own as it crosses the viewport edge, which already reads as a row
dealing itself out; **no index-based delay is added on top of that**, because with a
hundred-and-seventy-four-product collection a compounding stagger means the last row arrives
long after the visitor has scrolled past where it was. Staggering by hand on top of an entrance
that already staggers itself is the one embellishment this build refuses. The announcement bar crossfades its
messages with an overlap rather than a sequence. The one moment that earns a damped bounce is
the cart badge incrementing, because that is the confirmation an add worked and it happens off
to the side of where the visitor is looking. Two loading treatments exist, a sweep and a pulse,
and they belong to the product grid and the drawer, the two surfaces that fetch; a shop that
draws a skeleton of itself on every navigation feels slower than one that shows the previous
page for the same duration.

**Accessibility floors, which do not vary with anything above.** Body text meets WCAG AA
contrast against its ground. A layer of text that is present for a screen reader and hidden
from sight carries every meaning the shop draws in visual form alone: a strike-through, a
diagonal across a swatch, a slash between two numbers, an unlabelled mark. **The focus ring is
drawn twice, a pale ring inside a soft dark one**, because most focusable controls on this shop
sit on a photograph and a single dark ring vanishes against one; verify it against the hero
controls, a card image and a category tile, which are the three worst cases. Full keyboard
navigation reaches every interactive element. Two skip links, and the second matters: a keyboard
visitor on a product page otherwise passes eleven gallery frames and four thumbnails before
reaching the price. Every overlay takes focus on open, traps it while open, returns it to the
control that opened it, and closes on escape. Touch targets are comfortably sized, icon-only
controls carry labels, and meaning is never carried by colour alone. Under forced colours every
signal the shop carries in colour alone survives, and the struck swatch is the one that fails
silently, because a diagonal drawn as a background disappears and the hidden text becomes the
only remaining signal. Under a reduced-motion preference nothing reveals, nothing rotates,
nothing autoplays, the badge simply changes number, and every element is present at load; state
changes under a pointer or a key may remain, because those are responses to a deliberate act.

**Responsive behaviour.** Two breakpoints carry the site and every other breakpoint in it is a
nudge: one near a small tablet width and one near a large one. At the wider of the two the nine
navigation entries fold into a menu control, while the wordmark and the
three utility marks stay in the bar at every width; **the cart badge in particular stays visible
on a phone**, because on a phone the drawer is the only cart view a visitor sees before the cart
page. At the narrower one the two-column layouts become one: the product route's columns stack
with the gallery first and its hold released, the warranty panel stacks with the photograph
above the dark half at full viewport width, and the facet row collapses into its panel. **The
product grid is two columns below the narrower switch and never one**: two narrow cards side by
side is what makes a phone shopper scroll a shelf, and one card per row turns a
hundred-and-seventy-four-product collection into a list nobody reaches the bottom of. **On a
phone the buy control is reachable without scrolling past the whole gallery**: either the
gallery collapses to a single frame with a counter, or the buy controls are duplicated in a
persistent bar, and the choice is yours. At a narrow viewport nothing overflows sideways. One
result is worth knowing because it is easy to get wrong: **the product route is taller at the
middle width than at the widest**, because its two columns have already stacked while the grid
has not, so nothing may assume that a narrower viewport always means a shorter page.

**What this must not look like.** Not a shop that animates: motion on a page this dense makes it
feel slow, and on a storefront that is measured in abandoned carts rather than in taste. Not a
page dominated by one hue family with no second signal. Not decoration standing in for content.
Not a grid of cards separated by borders and drop shadows, which is the default a builder
reaches for and is the opposite of the shelf this shop is. And nothing borrowed wholesale from a
layout built for a subject unrelated to retail.

---

## Front-end specification

This section carries the measured visual detail. It is the specification of what must be true on
screen; the exact values behind it are the builder's unless stated.

### The three token registers

The reference this shop is drawn from is three products stacked on one another, and the capture
recorded three disjoint sets of design tokens: a storefront register owning every route, a cart
register owning the drawer and its upsell, and a checkout register owning the till.

**A value from one register is never used to style another.** The checkout rounds its corners
and the shop does not; the drawer rounds its own and the shop does not. Mixing them is the
single easiest way to end up with something subtly wrong everywhere and obviously wrong nowhere.
The build owns the first register outright, reproduces the second as ordinary components of its
own, and treats the third as a boundary.

### Colour, by role

| Role | Treatment |
|---|---|
| page ground | near-white neutral |
| ground contrast partner | near-white neutral, one step darker |
| body and heading text | near-black neutral |
| link text | near-black neutral at reduced alpha |
| subdued text | near-black neutral at reduced alpha over the ground, never a chosen grey |
| the subdued ground behind media | near-white neutral, one step off the page ground |
| hairlines and field borders | near-white neutral, one step darker again |
| primary button ground | mid, vivid blue |
| primary button text | near-white neutral |
| secondary button ground | near-white neutral |
| badge ground | near-white neutral |
| badge border and text | near-black neutral |
| the dark bands | near-black neutral, two values one step apart |
| the announcement bar at rest | near-black neutral at three-quarter alpha |
| slider controls at rest | near-white neutral at three-quarter alpha, full strength on hover |

Colour tokens are declared as component triples and consumed through an alpha wrapper, which is
what makes the contrast steps possible; the alpha form outnumbers the solid form by more than
two to one. The generated photography draws from its own set: a near-white neutral through a
mid, soft orange for gold metal, a deep neutral for black metal, and dial fills running from a
near-black warm neutral through a deep, muted red to a near-white warm neutral.

### Type

One family carries the whole shop at three weights, a regular, a semibold and a bold, loading
with a swap so a fallback renders while the real face arrives. The family is **Montserrat**, a
geometric sans named from a public font host; naming a freely licensed typeface is not an asset
dependency, and the build installs it from a package rather than carrying a file. The stack falls
back through a system interface sans, a platform sans, and a generic `sans-serif`. Both the body
family and the heading family are that same stack, differing only by weight. Three faces, not six:
the reference loaded fifteen faces across three typeface families and rendered from three of
them, at a per-load cost larger than its entire stylesheet budget.

The rendered scale, in order of how much of the page each accounts for:

| Size | Weight | Line height | Role |
|---|---|---|---|
| `14px` | `400` | `25.2px` | the body size of the whole shop |
| `16px` | `400` | `28.8px` | product card titles, section body |
| `15px` | `400` | `27px` | navigation and footer links |
| `14px` | `400` | `18.9px` | dense captions |
| `18px` | `400` | `23.4px` | the price line |
| `16px` | `600` | `28.8px` | the sale price, and card titles that carry weight |
| `22px` | `700` | `39.6px` | section headings |
| `24px` | `700` | `43.2px` | the page heading |
| `24px` | `600` | `31.2px` | the product title |
| `12px` | `700` | `21.6px` | the badge |
| `12px` | `400` | `16.2px` | the benefits strip sublabel |
| `11.5px` | `600` | `14.95px` | the drawer's own labels |
| `10px` | `400` | normal | the smallest legal text in the footer strip |
| `9px` | `400` | `16.2px` | the payment mark captions |

The ratio is generous for everything read at length and tight for everything scanned, and that
split is the whole airiness of the shop. The wordmark is set type in a heavy condensed face, not
a vector mark.

### Scaling, grid and spacing

The root font size is set so that one root unit resolves to ten pixels, layout is expressed in
root units and component detail in pixels, and reproducing that stepping rule reproduces the
scale. Hard-coding one column of pixel values does not, and drifts the moment the type scale is
adjusted.

The content column is held to a fixed page width, centred, with a gutter each side. The grid
gutter is a hair, `8px` at desktop and `4px` below the narrow switch. **Section spacing is
zero**: sections own their internal padding and abut exactly.

### Radius, borders, shadow and focus

Every structural radius is zero: buttons, fields, image frames, text panels, popovers, product
cards, collection cards and blog cards. **Two exceptions, both fully rounded capsules**: the
sale and bundle badges, and the variant pill. The drawer's own register rounds everything
slightly; the checkout's rounds more; neither belongs to the shop.

A field label floats: at rest it sits inside the field, and on focus or once the field carries a
value it rises above the field as it shrinks, both movements running together at the fastest
duration so the label reads as one object moving rather than two swapping.

Every declared border is one hairline weight, except the primary button's outset ring, which is
a thick ring at full strength and flush to the edge. The image frame's hairline sits at a very
low alpha, which is why it is barely visible. The variant swatch outline sits at just over half
strength.

Every shadow token is defined and every one but the popover is switched off, at a zero
horizontal offset, a small vertical offset and a small blur, so turning the opacities up yields
the intended shadow rather than a guess. Exactly two shadows render in the whole build: a soft
low-opacity cast under the currency selector's popover, and an inset hairline ring on the
drawer's own checkboxes and controls.

The focus ring is two layers: a pale ring first, then a soft dark halo outside it. **This is
two-layer on purpose**: the pale layer is what keeps the focus state visible when the focused
control sits on a photograph, which on this shop is most of them. Its arrival is transitioned
fast.

### Iconography

Sixteen marks are drawn by the build rather than fetched, all inheriting the colour of the text
around them, all drawn as filled paths on their own coordinate space and scaled at use.

The masthead set is five: a magnifier with a handle running down and to the right; a person as a
circle above an arc of shoulders; a menu of three horizontal capsule bars of equal length,
evenly spaced, **with rounded ends rather than square ones**, which is visible at the rendered
size; a close as two lines crossing; and a caret as a shallow downward chevron.

The disclosure and confirmation set is five: a chevron; a check drawn as a short down stroke and
a long up stroke; an **arrow with a shaft rather than a chevron**, whose shaft runs most of the
width at the vertical centre and which is the one place a control points somewhere; a ringed
close drawn as **two primitives that stay two**, a circle and a cross of two separate subpaths,
because drawing it as one path with a stroked ring changes how it scales; and a left chevron.

The cart set is three: a bag with a handle, a bin, and a decrement drawn as a single capsule bar
with rounded ends centred on its field. Its increment partner is the same bar plus its vertical
twin. The bin swaps to a pale mark on a near-black ground under a pointer, and the softer remove
control swaps to a pale mark on a mid neutral ground.

**The caret is the only mark the build rotates**, a quarter turn in each direction, **and the
rotation carries a small sideways correction**. A caret rotated about the centre of a wide short
box does not land where a caret rotated about the centre of a square box lands, and without the
correction every disclosure arrow on the site sits slightly off its label, everywhere at once,
in a way that reads as sloppiness without anybody being able to say why. Two further transforms
belong to the wrapper rather than the mark: one lifting an inline mark to sit on a text
baseline, and one flipping a wrapper through both axes to make a previous control out of a next
one.

Round icon controls take the capsule radius and a frosted fill.

### Motion tokens and the reveal system

Seven durations are declared and the shop uses four of them: the fastest for state swaps and
transform nudges, a default for colour, ground and border swaps, one slightly longer for the
announcement crossfade, and one longer again for a disclosure's height and for a ground and
shadow changing together. The entrance runs at the longest of the four. Three further durations
are declared and unused, and are part of the token contract rather than anything that runs.

Two curves carry the storefront. The default is symmetric and gentle at both ends and is used an
order of magnitude more than everything else combined; anything without a stated reason to
differ uses it at the default duration. The entrance curve has no ease in at all, so an element
is at full speed from the first frame and settles at the end. A third curve, paired with the
fastest fade, is the fade primitive and is the single most-declared intentional transition in
the build; use it for anything appearing or disappearing that is not an entrance. A fourth, the
disclosure curve, pairs with the disclosure's height and opacity.

**Every transition the build writes names its properties.** A blanket transition on every
property is a measurable cost on a page carrying a hundred and seventy-four cards, and it is not
copied however often it appears in the reference.

The keyframe library the shop uses: four slide rules forming one family, a panel entering from
the right, leaving to the left, entering from the left and leaving to the right, which is a
paged carousel's four movements and is what the banner slideshow consumes; a rise-and-fade
entrance; a scale-in; a blur in and a blur out; a pulse at a single midpoint stop; a spin; a
damped bounce that overshoots, undershoots, overshoots again and settles in four stops; a
horizontal flip; a background sweep across a doubled width; and a stroke reveal.

**The reveal system.** An element marked as a trigger starts invisible and offset; when it first
enters the viewport it plays one entrance and then holds its final state forever. Its four
requirements are all failures of default rather than of animation:

- It plays each element's entrance exactly once per page load, on first intersection.
- It never re-hides an element that has already played, including on scrolling up past it and
  back down.
- It reveals an element already within the viewport at load **without waiting for a scroll
  event**, which is the failure that leaves a short page's content permanently invisible.
- It places every element in its final state **if the trigger mechanism fails to initialise for
  any reason**, and under a reduced-motion preference.

Its targets are the product grid container, each product grid item, the product information
column, the contact form, a blog article card, a rich-text block, and the three footer blocks.
**Note what is not in that list.** The masthead does not reveal, the announcement bar does not
reveal, and the home route's hero, benefits strip, category row and banner do not reveal: they
carry their own one-shot entrances instead. Applying the reveal system to chrome produces a shop
whose header fades in on every navigation. The observer stops observing each element once it has
played; an observer retaining every target on a long phone page is the largest avoidable cost in
the build.

### Layering

Stacking is shallow and explicit. **The build uses a named scale of no more than six levels and
never a sentinel value.** If a component genuinely must sit above the overlays, it belongs in
the overlay system rather than above it. A third-party in the reference pins itself above
everything with the largest integer its platform holds, eighty-one times over, which is how a
shop ends up unable to raise its own cart drawer above a widget.

### The component inventory

Chrome: the announcement bar, the masthead, the navigation disclosure, the navigation drawer,
the search overlay, the cart badge, the cart drawer, the benefits strip, the currency selector
and the footer.

Catalogue: the product card, the rating row, the badge, the price pair, the product grid, the
facet disclosure, the mobile facet panel, the sort select, pagination and the category tile.

Product: the gallery with its thumbnail strip, the media modal, the variant swatch grid, the
quantity stepper, the stock line, the buy controls, the trust strip, the disclosure panel, the
review carousel and the related rail.

Cart: the cart line, the upsell block, the discount field, the totals block and the wallet
controls.

**Five slideshows exist and they are one component with five configurations**, not five
components: the home banner, the category row, the review carousel, the gallery and the
thumbnail strip. They differ in whether they show a counter, dots or nothing, in whether they
page by one or by a viewport, and in whether the edges bleed. All five share the four slide
rules.

**Four overlays exist and they are one component with four contents**, sharing the
mutual-exclusion rule and the escape handling. Building them separately is how a build ends up
with two backdrops stacked.

**Five stores hold state that crosses components, and only five**: the cart, the display
currency, the selected variant on a product route, the facet and sort which live in the address,
and which overlay is open. Everything else is component-local.

### Layout stability

Five elements reserve space before their content arrives, because all five are places where a
page can shift under a visitor mid-read: the product card image reserves a square at the card's
width; the gallery main frame reserves a square at the column's width; the variant swatch grid
reserves the full grid at its row count; the review carousel reserves one card's height; and
**the rating row reserves its height when the product has a rating and reserves nothing when it
does not**. That last asymmetry requires knowing at render time rather than at fetch time. A
build that reserves it unconditionally leaves a gap on every unrated card, and one that reserves
it never shifts the price down on every rated one.

### The hidden text layer

Thirteen strings are present for a screen reader and hidden from sight. Four of them exist
because a purely visual signal carries meaning a non-visual reader would otherwise lose
entirely. **Reproduce all thirteen:**

`Regular price` before every struck-through price; `Sale price` before every sale price;
`Open media 1 in modal` through `Open media 11 in modal` on each gallery frame; `of` between the
gallery counter's two numbers, so `1` `/` `11` reads as one of eleven;
`Variant sold out or unavailable` on the struck swatch;
`Decrease quantity for ` followed by the product title, and `Increase quantity for ` followed by
the product title, on each stepper; `Quantity` on the stepper group; `In stock (161 products)`
and `Out of stock (13 products)` on each facet option, where the visible form is the label and
the parenthesised number in two elements; `Collection:` before a collection title; `Log in` on
the account mark; and `Cart` on the cart mark.

**The two quantity strings interpolate the product title.** On a cart page with three lines
there are three decrement controls, and six identical labels would make them indistinguishable.
The interpolation is the point.

The two skip links read `Skip to content` on every route and `Skip to product information` on a
product route. The facet counts are announced as one string rather than as a label and a
parenthesised number in two elements, which otherwise reads as the label followed by a bare
number.

**Heading structure: one first-level heading per route**, and the heading order under it
descends without gaps. The product route carries its title twice, once as the page heading and
once opening the description column; the second is a lower level, not a second first-level
heading.

### Generated imagery: the zero-asset substitution guide

This build ships with no binary of any kind, which on a shop that is almost entirely photographs
of the thing it sells is a large claim, and every asset class is replaced by a procedure rather
than by a file.

**The watch generator.** Every photograph in the build comes from one deterministic generator
seeded on a handle, drawing a watch as vector primitives on a pale ground at a square aspect.
The same handle produces the same watch forever, which matters because one product appears on
the home route, on up to four collections, in the related rail and in the cart, and it would be
alarming if it changed on the way. Hash the handle, then draw each choice from a different field
of it: a case that is a circle or a cushion, occupying a little over half the frame height and
sitting slightly above centre; a case fill that is a gradient across the case between two stops
drawn from a metal set of steel, gold, rose and black; a bezel as an annulus just inside the
case, fluted with radial notches or smooth; a dial as a circle inside the bezel, filled from a
set of eight; twelve indices at even intervals as bars, roman numerals, arabic numerals or
stones; three hands in the metal's lighter stop at a fixed pose; a bracelet or strap as two
tapered strips from the case to the frame edge; and a contact shadow as a soft blurred ellipse
beneath the case, which belongs to the photograph rather than to the design and is the one
shadow exempt from the rule above.

**The generator must produce visibly different watches for different handles at thumbnail size.**
Metal and dial variation carry almost all of the distinguishability at that size; case shape and
index style carry very little. Media beyond the first are the same watch at other framings: a
detail crop on the dial, a three-quarter view with the case rotated, and a wrist context frame.
Generate at most four distinct framings and repeat them.

**Four reuses of the same generator.** The category tiles use it on a near-black circular ground
with the case filling more of the frame and the contact shadow omitted, seeded on the collection
handle. The hero and banner bands use a gradient field, dark at the top through two deeper
neutrals, with a soft elliptical light from the upper right, the watch placed off centre at a
larger scale with its contact shadow replaced by a mirrored copy beneath it at low alpha, and the
left third held under a dark wash so the controls hold contrast. **The type in the banner is set,
not drawn into the image**, because baking it in loses it to search, to translation and to a
screen reader. The review photographs use it small, off centre at a seeded tilt, over three
overlapping soft-edged pale blobs with a single warm overlay across one corner, and **they must
look worse than the catalogue photography, deliberately**: a review photograph that looks like a
catalogue shot reads as fabricated, which defeats the entire purpose of the band.

**The upsell mark** is a square filled with a diagonal gradient from a mid, vivid green to a deep,
vivid teal, carrying a centred pale shield with an isometric cube inside it drawn as three rhombi
in the gradient's lighter stop.

**The payment and social marks** are drawn as abstract geometry on a small rounded rectangle with
a hairline, each carrying a seeded arrangement of two to four primitives. **Real payment network
marks are not reproduced.** They are trademarks, they are the one asset class a build legitimately
cannot generate a lookalike of, and the correct behaviour is to leave the slots abstract until
whoever owns the shop supplies the real ones.

**Product video is not substituted.** The slot in the description column takes the generated
banner field at the column's aspect, static. A generated film is not worth building and a real one
is not worth several megabytes in a column below the buy control.

Every content picture carries alternative text naming the product and its colourway. The scrims,
the gradients and the decorative marks declare themselves decorative and carry none.

---

## Technical requirements

The client is **Astro** with islands, built to a production bundle: the server renders each
route's HTML complete and only the interactive parts hydrate, which are the cart drawer, the
variant grid, the facet row, the quantity steppers, the two slideshows and the currency selector.
The HTTP API is **Express** on Node 20, served on the same origin under `/api`. The store is
**PostgreSQL**, reached at `DATABASE_URL`, which is read from the environment and never hardcoded.

Billing is **killbill**, reached at `PAYMENTS_API_URL`. Every call under the `/1.0/kb/` prefix
carries three things: HTTP Basic credentials, the tenant key read from `PAYMENTS_API_KEY`, and
the tenant secret read from `PAYMENTS_API_SECRET`. The Basic pair is the provider's own built-in
pair rather than a value this environment issues, and it is the literal `admin` with the literal
`password`. Every write also carries a header naming the writer. `killbill` is a billing platform and not a card
processor: it holds accounts, catalogue plans, subscriptions and invoices, and it has no charge
object, no card token and no decline semantics. `GET /1.0/healthcheck` is the unauthenticated
liveness route; `/1.0/kb/healthcheck` sits behind the tenant filter and answers with a client
error forever, so it can never be used as a probe. The referenceable surface is exactly:
`GET /1.0/kb/accounts?externalKey=<key>`, which answers with the account when it exists and as
not found when it does not; `POST /1.0/kb/accounts`, taking `name`, `externalKey`, `email`,
`currency` and `country`, which creates and refuses a taken `externalKey` as a conflict;
`GET /1.0/kb/accounts/pagination`; `GET /1.0/kb/catalog/availableBasePlans`; and
`GET /1.0/kb/invoices/pagination`, which reports an amount as a decimal rather than in minor
units and a currency in uppercase. Refunds, payment methods and chargebacks are not part of that
surface.

Mail leaves over **real SMTP** through **mailpit** at `SMTP_HOST` and `SMTP_PORT`, with
`SMTP_USER` and `SMTP_PASS` read from the environment. There is no third-party mail vendor and no
API key.

The backing services named here are **already running** and reachable at their environment
variables. Do not download, install, compile or start a copy of any of them.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are `postgres`, `killbill` and `mailpit`, and reaching for anything
else is a contract violation.

There is no authentication scheme, no session store and no user token anywhere in this product.
The cart token is an opaque session identifier and is not a credential.

`GET /api/health` returns `200` once the app is ready. The app writes one structured JSON record
per HTTP request to `/app/logs/requests.log`, each record carrying at least the request method
under the key `method` and the request path under the key `path`.

**Each page view is recorded** with its route and a timestamp, and the record is readable by the
shop's owner at `GET /api/page-views`, newest first.

**Every internal link on every public route resolves.** No link in the masthead, the footer, the
category row, a card, a breadcrumb or a policy strip may answer as not found.

**Every response carries the standard security headers**, including a strict transport policy and
a nosniff content-type policy, on the HTML document, on every API response and on the two machine
routes alike.

A sitemap at `/sitemap.xml` lists every public route and a robots file at `/robots.txt` names the
sitemap. Both are served by the application rather than written by hand into a static directory,
so a route added later appears in the sitemap without a second edit.

**Presentation primitives are defined once and consumed identically on every route.** A primitive
carries its own styles and depends on the page it is placed in for nothing except the ground it
sits on, so the same button, chip or heading placed on the home route and inside a variant card
renders identically.

**Performance budgets**, stated as ceilings rather than as targets. Script executed before first
interaction: 250 kilobytes compressed. Stylesheet: 80 kilobytes compressed. Fonts: one family,
three faces, 120 kilobytes in total. Images above the fold: one, and it may be large. Requests
before first render: 20.

**Loading order.** The one image above the fold loads eagerly and every other image on every route
defers until it approaches the viewport. Images are served in a modern format with a fallback.

---

## Data model

Nine tables carry the shop: `products`, `variants`, `collections`, `collection_products`,
`carts`, `cart_lines`, `orders`, `newsletter_signups` and `page_views`. All timestamps are UTC.

This application has no accounts and no credentials. `/app/USER_README.md` states that there are
none rather than listing any.

### products

One hundred and seventy-four rows. Fields: `handle`, `title`, `maker`, `model`, `body`,
`features`, `includes`, `rating_score`, `rating_count`, `badges`, `available`, `house_order`.
`handle` is unique and is the address segment.

`maker` is its own field. It is never parsed out of `title`, because the six measured titles share
no shape a parser could rely on. The catalogue carries at least five distinct makers, `VOLARI`
among them.

`rating_score` and `rating_count` are nullable together. `rating_score` carries one decimal place
and its measured range is `4.3` to `5.0`; `rating_count` is an integer and its measured range is
`8` to `197`.

### variants

One or more rows per product. Fields: `id`, `product_handle`, `option_name`, `option_value`,
`price_minor`, `compare_at_minor`, `available`, `media_seed`, `house_order`.

**`price_minor` and `available` are per variant, never per product.** A schema that hangs one
price off the product can express neither the `From ` form on a card nor the struck swatch on a
product page.

`price_minor` and `compare_at_minor` are integers in store minor units in the store currency,
`usd`.

### collections

Eleven rows. Fields: `handle`, `title`, `description`, `house_order`. The catch-all is `all`,
titled `Products`, carrying no description. The ten curated collections are `mens-watches`,
`womens-watches`, `couple-watches`, `car-watches`, `quartz-watches`, `mechanical-watches`,
`automatic-watch`, `best-sellers`, `2-watch-bundle-offer` and `watch-accessories`, each carrying
one or two sentences under its title.

Membership lives in `collection_products`, carrying `collection_handle`, `product_handle` and
`position`.

### carts and cart_lines

`carts` carries `token`, `currency`, `discount_code`, `note` and `created_at`. `cart_lines`
carries `key`, `cart_token`, `variant_id`, `quantity`, `position` and `promotion_owned`.

`key` is its own value and is not `variant_id`. `position` is insertion order and never changes.

### orders

Fields: `reference`, `cart_token`, `email`, `currency`, `total_minor`, `created_at`.
`reference` is unique and is the value the billing account's `externalKey` carries.

### newsletter_signups and page_views

`newsletter_signups` carries `email`, `code` and `created_at`, unique on `email`. `page_views`
carries `route` and `viewed_at`.

### Invariants

- The cart's unit count is the sum of its line quantities, never the count of its lines.
- A collection's stated product count equals the sum of its availability facet counts. The
  catch-all reports `174 products` with `161` in stock and `13` out of stock.
- A product whose variant prices differ displays the price of its cheapest **available** variant.
- Every amount is stored once, in `usd`, as an integer in minor units, and a display currency is
  never stored on a product.
- Two identical requests for the same collection, facet selection, sort and page return the same
  products in the same order.
- The order reference is unique, and a second order under an existing reference creates no second
  billing account.
- No endpoint writes to `products`, `variants`, `collections` or `collection_products`. A request
  that would create, change or delete one of those rows is refused as an invalid request and the
  row count and the row contents are unchanged afterwards.

### Seed data

The seed carries 174 products across 11 collections, at least five distinct makers, the twelve
products the home route shows with the values pinned in Core features, the three colourway sets
pinned there, and the `shipping-protection` product. Exactly 161 products are available and 13
are not. Seeding must be idempotent: restarting the app must not duplicate rows and must not
change a count.

---

## Constraints

- No user-generated content, no on-site review composer, no wish list, no comparison table, no
  recently-viewed rail, no stock countdown, no visitor counter, no urgency timer and no chat
  widget.
- No infinite scroll and no load-more; a collection pages by numbered controls.
- No account system of the storefront's own, and nothing behind the sign-in handoff: no order
  history, no saved addresses, no profile editing and no order tracking.
- No breadcrumb on any route except the product route.
- The storefront renders nothing inside the checkout beyond the summary the cart supplies, and it
  implements no payment handling, no tax resolution and no address validation.
- No sort control other than the nine named options, and no facet other than availability.
- No external network call at runtime beyond the three named backing services. No third-party
  script, no analytics endpoint, no tracking pixel and no font fetched from another origin.
- No binary asset is fetched from any origin outside the application on any route. Every
  photograph, every category tile, every banner, every review picture, every icon, every payment
  mark and the upsell mark are generated by the build. The only binaries the application carries
  are the three font faces, which come from the font package installed at build time.
- No product video. The slot takes a generated static band.
- No real payment network marks; the slots stay abstract.
- No native application and no separate mobile site.
- The catalogue is 174 products across 11 collections and the shop must stay responsive across
  the whole of it with the facet panel open.

---

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what
  the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | a readiness object |
| `GET /api/collections/:handle` | `sort_by`, `availability`, `page`, `currency`, all optional | an object carrying `title`, `description`, `count`, `facets`, `products`, `page` and `pages`. `facets` carries `availability`, mapping `in_stock` and `out_of_stock` to their counts. Each product carries `handle`, `title`, `maker`, `badges`, `rating`, `price` and `compare_at`, where `price` carries `amount_minor`, `formatted` and `from`, and `rating` is null or carries `score` and `count` |
| `GET /api/products/:handle` | `currency` optional | an object carrying `handle`, `title`, `maker`, `model`, `body`, `features`, `includes`, `rating`, `badges`, `media`, `option_name` and `variants`. Each variant carries `id`, `option_value`, `price`, `compare_at`, `available` and `media_seed` |
| `GET /api/cart` | `currency` optional | the whole cart |
| `POST /api/cart/lines` | `variant_id` and `quantity` | the whole cart |
| `PATCH /api/cart/lines/:key` | `quantity` | the whole cart |
| `DELETE /api/cart/lines/:key` | none | the whole cart |
| `POST /api/cart/discount` | `code` | the whole cart, with the rejection reported in the body when the code is refused |
| `POST /api/checkout` | `email` | an object carrying `reference`, `lines`, `unit_count`, `total` and `currency` |
| `GET /api/checkout/:reference` | none | the same object |
| `POST /api/newsletter` | `email` | the accepted signup, or the rejection |
| `POST /api/contact` | `name`, `email` and `message` | the accepted message, or the rejection |
| `GET /api/page-views` | none | a top-level JSON array, newest first, each entry carrying `route` and `viewed_at` |

A list endpoint returns a top-level JSON array. Every endpoint is public. A request that would
create, change or delete a catalogue row is rejected as a client error, never served and never
answered with a server error. An invalid request is rejected as a client error with a reason; it
is never a server error and never a silent success.

### No mocks

The cart is server-authoritative and every mutation returns the whole cart. **The billing account
must exist as a real record in `killbill`** under the order's own `externalKey`, at the cart's
display currency, reachable at `GET /1.0/kb/accounts?externalKey=<reference>`; an in-memory
orders array, a hardcoded success body the app returns to itself, or an order the app records
without the account existing is a contract violation however good the interface looks. **The
signup email must exist as a real message delivered over SMTP** to the address the visitor typed;
a row in a table saying mail was sent is not mail. `killbill` and `mailpit` are the fact, and the
app's own interface and its own tables can only reflect what lives in them, never substitute for
them.

---

## Definition of done

A visitor can filter a shelf of watches, open one, pick a colourway whose neighbour is sold out,
set a quantity and add it to a cart, and the badge, the drawer, the cart page, the checkout
summary and the in-cart count beside the quantity all agree on what is in it and what it costs,
including the shipping-protection line the visitor did not choose. Completing that checkout
leaves exactly one billing account under the order's reference in `killbill`, and submitting it
again leaves exactly one. Signing up for the discount delivers the code as a real message.
Changing the display currency re-prices every figure on the page together, including every
struck-through original.
