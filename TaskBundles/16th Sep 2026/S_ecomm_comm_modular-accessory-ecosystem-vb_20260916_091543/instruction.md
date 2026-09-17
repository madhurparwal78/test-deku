# Modular Accessory Ecosystem

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, choose a phone model, open a Latch case cut for it, add that case and a compatible Latch module to the cart, and a signed in shopper must be able to place and pay for that order, without hitting an error page. Two shoppers buying the last unit of one colourway at the same instant must produce exactly one order and a stock count of zero, never below zero. A paid order must exist as a real invoice in Kill Bill on that shopper's account for the exact order total; a paid flag the app records for itself does not count.

## Overview

LatticeGoods is the direct to consumer storefront of a single accessories brand. One business owns every item in the catalogue: there are no other sellers, no bidding and no listings from outside the business. Its flagship line is Latch, a modular phone system. A repeating dot pattern on the back of every Latch case is also a mechanical lock, and every other Latch piece, grips, stands, wallet stands, lanyards and colour plates, locks into it.

Two things make this catalogue harder than an ordinary shop, and both are the product. **Fitment:** most items fit exactly one device. A phone case fits one phone model, so the same design exists once per model it is cut for, and a shopper on the wrong model switches device in one control and lands on the same design cut for theirs. **Modularity:** which module locks into which case is data, not marketing, and the product route offers only the modules that genuinely attach to the case being viewed.

Around those sit ordinary commerce, all of it exact: a live price with the higher list price struck through beside it, per colourway; a cart that survives the session; a checkout that creates the order, takes payment through Kill Bill and confirms it by email; and stock that can never go negative. The reading surfaces are a home route, category and listing routes with facets and sort, an ecosystem route that tells the Latch story, a deep product route, a store directory, an account area reached by a phone number and a one time code, and search.

It deliberately is not a marketplace. There is no second seller, no auction, no customer review, no live chat, no subscription plan and no loyalty points ledger; rewards are a named but empty surface. The genuinely hard part is correctness under pressure: the last unit sold exactly once, an unpublished product unreachable by every route including a direct variant reference, and each colourway priced as itself.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (not signed in) | Browse every public route; use search, the delivery check and the store directory; build a cart; read the whole help centre; subscribe to the newsletter; request a sign in code | **Cannot place an order.** **Cannot read any order.** **Cannot keep a wishlist.** **Cannot reach an unpublished product by any route** |
| Shopper (signed in) | Everything a visitor can do; place and pay for orders from their cart; read their own orders; keep a wishlist | **Cannot read or pay another shopper's order.** **Cannot reach an unpublished product by any route, including a direct link or a variant reference** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Visitor session to any Shopper-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds between two Shoppers: one shopper's session asking for another shopper's order is denied and changes nothing.

Signup is **open**: a phone number that has never signed in becomes a new shopper when its first code is verified. There is no password anywhere in this product. Two shoppers are seeded:

| Phone | Email | Name |
|---|---|---|
| `9876500001` | `shopper@example.com` | `Asha Rao` |
| `9876500002` | `shopper2@example.com` | `Bikram Sen` |

## Core features

### Sign in by phone and one time code

1. The one identity is a ten digit phone number. The dialling prefix `+91` is locked beside the field in the interface and is never part of the number the API takes. There is no password, no email sign in and no social sign in.
2. Requesting a code takes a `phone` and an `email`. When the phone already belongs to a shopper, the code is sent to the email already on file and the `email` in the request is ignored. When the phone is new, `email` is required, and it becomes that shopper's email once the code is verified.
3. The response to a code request is identical whether or not the phone already exists, so the endpoint never reveals who is a shopper.
4. The code is six digits, arrives as an email whose subject begins `Your LatticeGoods sign in code`, and whose body begins with the six digits. It is valid for `10` minutes.
5. A code works **once**. Verifying a code that has already been used is refused, and no session is issued. When several requests present the same code at the same instant, exactly one of them issues a session. A code is valid only for the phone it was requested for: presented with any other phone it is refused, and it stays valid for its own phone.
6. Requesting a new code cancels every earlier unused code for that phone. An earlier code is refused after a newer one has been requested.
7. A wrong code is refused and reports how many attempts remain. After the fourth wrong code the message reads `That code did not match. Two attempts left.`
8. Six wrong codes lock the phone for `15` minutes. While it is locked, even the correct code is refused, and the refusal says the number is locked rather than failing silently. Wrong codes are counted exactly however they arrive: six or more wrong codes sent at the same instant lock the phone just as six in a row do.
9. A form submitted repeatedly in quick succession is refused: a sixth code request for the same phone inside `10` minutes is refused as a client error and sends nothing. Simultaneous requests are counted the same way: however many arrive at once, at most five codes are sent inside `10` minutes, and every request beyond them is refused as a client error, never as a server error.
10. A verified code returns a bearer token. Signing out ends the session, and the old token stops working.

### Devices and fitment

1. The device tree is closed and owned by the catalogue: a device brand holds device families, and a family holds device models. `universal` is a real brand, not a missing value, and every module hangs off it so every product has a fitment edge.
2. A device model carries a rank, so newer models sort first, and a retired flag. A retired model leaves the navigation and every picker, but its products and its listing still resolve.
3. A product names exactly one device model. A case for two phones is two products.
4. Products that are the same design cut for different models share a `design`. That shared design is what the device picker navigates across.
5. The device options for a product list every non retired device model in the same family as the product's own model, in rank order. A model with a published product of the same design is available and names that product's handle. A model with no published product of that design is listed as unavailable, carries the caption `Not available for this model`, and is never hidden.
6. Choosing a different model **navigates** to that model's product. It keeps the chosen colourway when the target product has it, and otherwise falls back to the target's first colourway. Choosing a colour **never navigates**: a colourway is a variant of one product, a device cut is a different product.

### Listings, facets, sort and paging

1. A listing is a category plus zero or one device model plus zero or more facets. Its heading is generated, never authored: the device brand name, the model name and the category name, uppercased, for example `ARBOR ARBONE 16 PRO PHONE CASES`; with no model it is the category name alone, uppercased.
2. A listing only ever contains published products.
3. Facets are device model, single select; colour, multiple select and given by repeating the `colour` parameter, matching a product when any of its colourways is one of those chosen; material, multiple select; price band, single select; and feature, multiple select.
4. A feature facet matches only a product that carries that feature. A product that carries no features at all does not match any feature filter.
5. The five price bands, on a product's lowest live price, are `under-1000`, `1000-1499`, `1500-1999`, `2000-2999` and `3000-plus`, in rupees.
6. Sort has six options: `recommended`, the default and the only one with no stable order; `newest`, by sequence descending; `price-low-high` and `price-high-low`, both by a product's **lowest** live price across its colourways; `discount`, by the largest percentage off across its colourways, descending; and `best-selling`, by units sold descending. Every stable sort breaks ties by handle ascending.
7. Listings page twenty four products at a time, and `page` defaults to `1`. The page number is written into the link so a reload returns to the same depth, and a `Load more` button replaces automatic paging after the third page.
8. Clearing the model constraint widens the listing rather than emptying it, and the heading regenerates.
9. A listing for a retired model still returns its products and reports that the model is retired, shown as `This model is no longer stocked`.
10. A listing that matches nothing keeps its heading and says `Nothing here fits that combination`, names which facets are active, and offers `Clear all filters`.

### The product and its two selectors

1. A product has a handle, a title, a category, a line, a design, one device model, a badge or none, a list of features, a material, and one or more colourway variants in a fixed order.
2. Each variant has a SKU, a colourway name, a list price, a live price and a stock count. The live price is never above the list price; where the two are equal, no struck price is shown.
3. A title follows one pattern, and a product's own title and its listing card use its first colourway: the colourway, the product's title tail, then `for` and the model name, for example `Umber Latch Clear Phone Case Cover for Arbone 16 Pro`. A universal product has no `for` part, for example `Marigold Latch Phone Grip & Stand`.
4. Selecting a colour swaps the media, the title and both prices in place.

### Build your Latch

1. The compatibility graph is data. Each edge joins a case to a module, names the interface it is satisfied by, `lock` or `magnetic`, and carries a rank. An edge is stored once and read from both ends.
2. On a case, the panel `BUILD YOUR LATCH` offers the modules its edges reach, each in its first colourway; on a module it offers the cases, each in its first colourway. Only published products appear. Rows are ordered by edge rank ascending, ties by handle ascending, and there are **at most four**.
3. A case whose line lacks the lock pattern is never offered a module that needs `lock`, even though both would hold a magnet.
4. When the graph returns nothing, the whole block including its heading is absent. There is no empty state.
5. `ADD` adds the module in its currently selected colourway to the cart without leaving the route and becomes `ADDED`. A second activation adds nothing. Adding a module never adds the case.

### Publication

1. A product that is not published returns not found by handle for every caller, including a signed in shopper holding a direct link.
2. An unpublished product is absent from every listing, every search result and every build panel, in both directions.
3. An unpublished product's variant cannot be added to a cart, even by a request that names its SKU directly, and cannot be saved to a wishlist.

### Cart

1. The cart needs no sign in. It is identified by the `cart_token` cookie the app sets on the first cart write, and it survives the session: a later request carrying the same cookie sees the same lines.
2. A cart line names a variant by SKU, never a product, so a colourway is always pinned. It carries the unit live price and unit list price at the moment of adding.
3. The subtotal is the sum over lines of unit live price times quantity. Two colourways of one product at different live prices total to the sum of their own live prices, never to twice either one. The list total is the same sum over list prices, and the discount is the list total minus the subtotal.
4. Adding a SKU already in the cart increases that line. A quantity above the variant's stock is refused and the line keeps its previous quantity. A quantity below one is refused; removal is its own action.
5. A line reports its available stock, and the interface reads `Only N left` from three units down.
6. Where the cart holds a Latch module and no published case in the cart has an edge to it, that line carries the warning `This attaches to a Latch case. You may already have one.` with `See compatible cases`. It is a warning, never a block.

### Checkout and orders

1. Placing an order requires a signed in shopper, whose phone is the order's phone and is read only.
2. An order is created from the cart named by the request's `cart_token`, with a name, an email, an address and a delivery method. The address pincode must be served, and the delivery method must be one offered for that pincode.
3. **Creating the order and decrementing stock for every line happen together or not at all.** The order is created in state `pending`, and the cart is emptied. A refused order takes no stock from any of its lines, not even from a line whose own stock was enough.
4. Stock never goes negative. When two shoppers hold the last unit of one variant and both place orders at the same instant, exactly one order is created and stock ends at zero. The other request is refused with a conflict response naming the variant's SKU, and that shopper's cart line survives with its quantity reduced to the stock still available, marked sold out when that is zero.
5. An order line snapshots the title, the SKU and the unit prices at the moment of ordering; nothing later rewrites them. A price or title edited in the catalogue after the order was placed never changes that order's lines.
6. An order number reads `LG-` followed by six digits, for example `LG-100042`.
7. A shopper reads only their own orders. Another shopper's order is denied, and a visitor is denied every order.

### Paying an order in Kill Bill

1. Paying a `pending` order creates exactly one invoice in Kill Bill for the order total and then moves the order to `paid`.
2. The Kill Bill account belongs to the shopper and is identified by the external key `shopper-` followed by the ten digit phone, for example `shopper-9876500001`. It is created on that shopper's first payment, in currency `INR` and country `IN`, and reused for every later one.
3. The invoice carries one item per order line, with the line total in rupees, plus one item for delivery when delivery is not free. Every item description begins `Order ` followed by the order number, for example `Order LG-100042: latch-flex-stand-sage x 1`.
4. Paying an order that is already paid returns the same result, carrying the same `invoice_id`, and **must not create a second** invoice or send a second confirmation email. Pay requests for one order that arrive at the same instant create exactly one invoice and send one email; each is answered with that same `invoice_id` or refused with a `409` conflict response.
5. The order becomes `paid` only once its invoice has been read back from Kill Bill with the order total. The interface never shows a payment outcome the app has not read back.

### Order confirmation email

1. A paid order sends one email over SMTP to the order's email address, no cc and no bcc.
2. Its subject begins `Order confirmed:` followed by a space and the order number, for example `Order confirmed: LG-100042`, and its body names every line and the total.
3. Creating an order that is never paid sends nothing.

### Delivery check

1. A pincode is exactly six digits; anything else is refused as invalid.
2. A pincode is served when its first three digits are one of `110`, `302`, `400`, `411`, `500`, `560`, `600` or `700`. A served pincode offers `standard` delivery, free, reading `Delivers in 3 to 5 days`.
3. A served pincode whose first three digits are `110`, `400` or `560` also offers `express` delivery at `₹199`, reading `Delivers in 1 to 2 days`. The cheapest method is preselected.
4. Any other six digit pincode reads `We do not deliver to this pincode yet`.
5. A checked pincode is remembered for the session and reused on the cart and at checkout.

### Search

1. Search matches published products whose title or category name contains the query, case insensitively, in `newest` order, twenty four at a time.
2. A query that exactly matches a non retired device model's name, case insensitively after trimming, returns a redirect to that model's listing, for example `/list/arbor/arbone-16-pro`.
3. An empty result says `Nothing matched that` and `Try fewer words, or the name of your phone.`
4. Recent searches live in the browser only, until the shopper clears them.

### Wishlist

1. A signed in shopper saves and removes products; a visitor is denied. Saves survive signing out and signing in on another device.
2. An unpublished product cannot be saved. Removing a saved card fades it out and offers `Undo` for five seconds.

### Store directory

1. The directory lists active stores only, filterable by type, `all`, `brand_outlet`, `premium_partner` or `airport_outlet`, and searchable by city, state or pincode.
2. A store has a name, a type, an address, a city, a region, a pincode, a phone, an opening hours string per day group, a coordinate pair and an active flag.
3. Selecting a map pin scrolls the list to that store's card and outlines it; selecting a card centres the map on its pin. Where no map is available the route shows the list alone, grouped by region.

### Newsletter, cookie choice, privacy and the standing pages

1. Subscribing answers `You are on the list. Watch your inbox.` for a new address and for one already subscribed alike, so the form cannot reveal who is on the list. An invalid address is refused as invalid.
2. A first time visitor is asked once about non-essential cookies. The answer survives a reload and the question is not asked again.
3. A privacy page, `Privacy & Security Policy`, is reachable from the footer of every page and states what the shop stores about a shopper: the phone, the name, the email, delivery addresses, orders and saved products.
4. The standing pages are terms of use, warranty, shipping, cancellation, return and exchange, privacy and security, and about.
5. An unknown handle renders the not found route with the chrome intact. A route whose data call fails renders the error route, whose `RETRY` retries in place and, after three consecutive failures, is replaced by the four exits of the not found route.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home: hero carousel, category chips, line rails, press strip, newsletter | Public |
| `/category/:slug` | Category landing of circular tiles, no products | Public |
| `/list/:slug` | A listing of one category, with facets, sort and paging | Public |
| `/list/:brand/:slug` | A listing pinned to one device brand and model | Public |
| `/finder/:slug` | The device finder: pick a brand, then a model, then land on its listing | Public |
| `/collection/:name` | One ecosystem told as a story, with a rail per module family | Public |
| `/product/:handle` | One product in full | Public |
| `/cart` | The cart, including its empty state | Public |
| `/checkout` | Contact and address, delivery, payment | Shopper |
| `/stores` | The store directory | Public |
| `/search` | Search results | Public |
| `/offer/:slug` | Gift and price band landings over listings | Public |
| `/pages/:handle` | The standing pages | Public |
| `/login` | Phone sign in and code entry | Public |
| `/account` | The account overview | Shopper |
| `/account/help` | The help centre | Public |
| `/account/orders` | Order history | Shopper |
| `/account/orders/:number` | One order | Shopper, owner only |
| `/account/wishlist` | Saved products | Shopper |

**Entry and redirects.** A visitor who opens a Shopper route lands on `/login` with the intended route remembered, and signing in returns there. Signing out returns to `/` and the old token stops working. A token that has expired mid-action returns to `/login` with the reason stated, and the carried action is not performed. `/checkout` with an empty cart redirects to `/cart`. A shopper opening another shopper's order is denied and shown not found. An unknown handle renders the not found route; a handle that resolves but whose data call fails renders the error route.

**Journeys.**

1. *Fit, build and buy.* Open `/list/arbor/arbone-16-pro`: the heading names the model. Open `Latch Phone Case Cover for Arbone 16 Pro`, choose `Sage`, and the title and price change in place. In `BUILD YOUR LATCH` the rows read the grip, the flex stand, the wallet stand and the lanyard, in that order. Press `ADD` on the flex stand and it reads `ADDED`. Add the case, open `/cart`, and both lines are there with colourway and device named separately. Sign in as `9876500001`, check out to pincode `400050`, pay, and the confirmation shows the order number.
2. *Wrong phone.* On `Latch Phone Case Cover for Arbone 16 Pro` in `Amber`, open `SELECT DEVICE`. `Solarion S25 Ultra` is shown with `Not available for this model`. Choose `Arbone 17 Pro` and land on that model's case in `Basalt`, because `Amber` is not cut for it.
3. *Narrow and clear.* On `/list/arbor/arbone-16-pro`, filter by the magnetic feature: exactly four cases remain. Remove the model chip: the listing widens and the heading regenerates.
4. *Empty cart.* Open `/cart` with nothing added: `YOUR SHOPPING CART IS EMPTY`, `Fill it with LatticeGoods`, and `BROWSE PRODUCTS`, with no footer.
5. *Sign in.* Open `/login`: `CONTINUE` stays disabled until the field holds ten digits.

**States.** Every list has an empty state: the listing, search, the wishlist, the order history and the cart. Every waiting grid, build panel and store list draws a skeleton at its final layout. A pressed control waiting on a write shows a spinner inside the control. Every refusal states its reason and names the field at fault. An error never leaves a route blank.

## UI/UX notes

The north star is that a shopper always knows the thing in front of them fits the thing in their pocket. The register is **consumer retail**, restrained: the products are seen first, and the page gets out of their way.

**The design system** is small and measured. The ground is white everywhere, a near-white neutral, with the header, the panel and the cards on it. A second near-white neutral, a shade darker, raises option rows, the select surface and the module rows in the build panel; a third sinks the product media pane, the store cards and the help topic strip; a fourth is a hairline ground used where a rule would be too hard. Primary text is a near-black neutral, secondary text a deep cool neutral, tertiary text a light neutral, and quiet legal and caption text a mid neutral. Hairlines are a near-white neutral, and the disabled sign in button is a light neutral.

**One accent carries every affirmative action and nothing else:** a mid, soft teal on the buy button, on links inside body copy, on the map pins, on the selected facet and on the back to top ring, with a translucent wash of the same teal for hover and focus over an accent control. A white label sits on the accent. Destructive actions are never red and never the accent: removing a cart line is plain primary text that underlines on hover. The only red is a mid, vivid red for field validation and a slightly stronger mid, vivid red for the error route heading and its retry. The wordmark and the selected category chip are a near-black neutral. The exact shades are yours, so long as the accent is the only saturated colour a shopper can act on.

**Prices come in pairs.** The live price comes first in primary text, the struck list price after it in tertiary text, at the **same size**, on one baseline.

**There is no dark mode.** The shop declares one light ground and does not respond to a system colour preference.

**Typography.** Two families do the work, and a third is reserved for one display use. Interface and body text are a neutral grotesque in regular and medium. Condensed headings are the same family's condensed cut. The display face is a wide, heavy grotesque in one weight, used **only** for the hero titles on the home route. The fallback stack is `system-ui, sans-serif`, and the display role falls back to the condensed cut before the system stack. Name the families and their licences in the build. The scale is exact: body `16px` at weight 400; card title `16px` at 400; card title strong `16px` at 500; section heading `22px` at 400; route heading `24px` at 400; meta `15px` at 400; caption `13px` at 400; caption strong `13px` at 500; legal `12px` at 400; micro `9px` at 400. The product title on the product route is `28px` at 400, its live and struck prices `24px`, the ecosystem statement title `56px` at desktop and `32px` at mobile, its body `20px`, the hero titles `40px` at desktop and `28px` at mobile, and the award and press wordmarks `18px`. Every uppercase string is uppercase in the markup, not by transform.

**Shape and elevation.** Text fields, chips, tabs and small buttons take a small radius; the outlined `ADD` pill and the sort and filter buttons are rounder; category chips are fully rounded; store cards and the sign in panel are softly rounded; icon buttons, swatches and category tiles are circles. Elevation appears only where one layer genuinely floats over another: a faint shadow under the navigation panel, a stronger one around the sign in panel, an edge on the carousel controls over photography, and a lift under the sticky buy bar at mobile. **A selected swatch is marked by a thin white ring drawn inside the circle**; nothing grows, nothing gains a border, nothing gets a tick.

**Layout archetype.** A top navigation rail runs across a full bleed header, and the product route is a split detail pane: media on one side, the buy panel on the other. Density is **comfortable**: grids of product cards with room to scan. There is one real cut point, at about the width of a large phone held upright, and everything else is fluid.

**Single primary action.** Each route leads with one clear primary action in the accent, and every secondary action is visibly quieter: on the product route that is `ADD TO CART`, on the cart it is the checkout button, on the empty cart it is `BROWSE PRODUCTS`.

**Motion character is `eased`,** restrained and in service of state changes. There is no scroll driven motion, no pinned section, no parallax and no page transition. Four curves cover everything: a standard curve for panels, accordions, tabs, fades and colour changes; a decelerating curve for anything entering; a sharp curve for anything leaving; and a long carousel curve for the one long move. Durations form a ladder, and nothing sits off it: colour changes are the quickest; hover states and the back to top fade are quick; the accordion is a little slower; the focused field border and raised surfaces slower again; the navigation panel and the rail step are a move; and the carousel slide is the one long move. Hover is almost nothing: a text action underlines, and the carousel arrows brighten. Cards do not lift, images do not zoom, titles do not change colour. Under a reduced motion preference every entrance, the carousel advance, the cycling placeholder and the looping films stop, each settling on its end state.

**Accessibility floors,** which do not vary: body text meets WCAG AA contrast against its ground; tertiary text is used only for information repeated elsewhere, such as the struck price; every touch target is at least `48px` at every size, including desktop; every interactive element shows a visible focus ring in the accent on keyboard focus; icon-only controls carry labels; and meaning is never carried by colour alone.

**Responsive.** The layout is responsive across every viewport width, with one breakpoint. Below the cut point the header centres the wordmark and drops the rail into a full height overlay, products run two to a row, the product route stacks with the media first and a sticky buy bar at the foot, rail arrows give way to a snapping native scroll, filters and sort slide up as bottom sheets, the store directory puts its list first with the map as a band above, the sign in panel goes full width without its photograph, the cart puts its summary last under a sticky total bar, and the footer columns become accordions. Above it, three then four products run to a row. Nothing reachable at one size is unreachable at another.

What it must not look like: a page where cards lift and images zoom on hover, a second accent colour, a dark theme, or a marketing composition where the product wall belongs.

## Front-end specification

**Observed implementation, informational.** The reference storefront was observed using a single page framework, a material design component library whose tokens are the source of the design system above, a text splitting utility for the hero titles, a public font host, a third party map service and two image transformation services. None of that is a requirement: what binds is the capability stated here, built on the stack named in `## Technical requirements`. The component library's habit of transitioning every property is specifically not to be reproduced: name the properties that transition.

**The information architecture.** One tree, wide at the top and shallow below, with a device axis crossing the category axis. Nothing public is more than three steps from home: rail, panel, listing, product. The rail carries seven entries: `TECH`, `BAGS & WALLETS`, `WORK ESSENTIALS`, `GIFTING`, `COLLECTIONS`, `SHOP BY ARBOR` and `NEW ARRIVALS`. The `TECH` panel groups by category, `Phone Cases`, `Watch Bands`, `Power Banks`, `Wireless Chargers`, `Stands` and `Notebooks`, and again by device, one entry per model carried. Both groups resolve to listings. `SHOP BY ARBOR` resolves to a category route of seven tiles, `Arbone`, `Arbook`, `Arbor Watch`, `MagLock`, `Arpad`, `Arbuds` and `ArbTag`. The catalogue carries two device manufacturers, Arbor and Solaris; Arbor's product families are the Arbone phone, the Arbook laptop, the Arpad tablet, the Arbor Watch, the Arbuds earbuds and the ArbTag location tag, and MagLock is the magnetic attachment standard cases are certified against. `COLLECTIONS` resolves to the ecosystem routes and `GIFTING` to the offer index. Every filtered listing state is addressable by a shareable link that survives a reload, and a crawler reaches a device filtered listing without running scripts.

**The header.** Full bleed, white, one hairline along its bottom edge, no shadow, and it **does not stick**. At desktop: the wordmark left, linked home; the seven rail entries centred in `13px` medium uppercase; search, account and bag icon buttons right. The active rail entry carries an accent underline with clearance below the baseline and changes nothing else. Below the cut point the rail is removed, the wordmark centres, and the rail moves into a full height overlay opened from the account glyph. The cart route drops the rail and the search and bag glyphs, keeping the wordmark and the account glyph.

**The category panel.** Pointing at a rail entry opens a white panel under the header with its faint shadow, arriving on a short fade from a little above its resting place. It holds columns of links under uppercase titles and up to two image cards naming a line. It closes on pointer exit, on `Escape` and on any navigation; it opens on hover at desktop and on tap below the cut point, and a tap on an already open parent navigates to that entry's own landing.

**The search overlay.** The search glyph opens a full width overlay with one field, placeholder `Search for products`. Result rows appear as the query settles, each a thumbnail, a title and a live price. Enter goes to `/search`. `Escape` closes it and returns focus to the search glyph.

**The reassurance strip, newsletter and footer.** Above the newsletter on every route except the cart and sign in: `Quick Delivery`, `Easy Returns`, `Quality Assured`, each a glyph over a caption, static. The newsletter block reads `GET EXCLUSIVE ACCESS TO NEW PRODUCTS, DEALS & SURPRISE TREATS` with an email field and `SUBSCRIBE`, a text button that underlines on hover, replaced in place by the confirmation. The footer has four link columns: `KNOW US` with `About LatticeGoods`, `Corporate Gifting`, `Find a Store` and `Blog`; `HELP DESK` with `Contact Us`, `FAQs`, `Terms Of Use`, `Warranty Policy`, `Shipping Policy`, `Cancellation Policy`, `Return & Exchange Policy` and `Privacy & Security Policy`; `MOST SEARCHED ON LATTICEGOODS`, a flat list of listing links; and `GIFTS` and `BLOGS`. Under them, `FOLLOW US ON` with five social glyphs and `DOWNLOAD OUR APP` with two store badges, then the legal bar, whose copyright line names the trading entity, `© 2012 - 2026 LatticeGoods Retail Private Limited`, left and `Terms of use | Privacy policy` right. The footer is the whole public tree written out.

**The back to top control.** A circle fixed near the lower right, white, with an accent ring and the arrow up glyph, appearing once the page has scrolled a screen height. It is absent on the cart, the sign in and the store directory, none of which scroll the page body.

**The product card.** The most repeated component: in the listing grid, every rail, search and the offer routes. Its anatomy, top to bottom: a square image on the sunken ground with the product centred and padded; a badge top left when there is one; the heart top right, always present; a row of up to five swatch circles when the product has more than one colourway; the title in `16px` regular, at most two lines with an ellipsis; and the live price then the struck price, the struck one omitted when equal. There is no outer radius; a hairline on the right and bottom edges draws the grid. The card is one link to the product route, laid as an overlay under the heart and swatches rather than around them, so a keyboard reaches the card, then the heart, then each swatch. One badge at a time, uppercase, `9px`, white on a filled ground: `NEW!` in the upper left, and award marks as small stacked labels in the lower left of the ecosystem products. A product with more than five colourways shows four and a counter such as `+2`. Selecting a swatch on a card swaps its media, title and prices in place without navigating and updates its link. A sold out card desaturates its media and replaces the badge with `SOLD OUT`, stays in its position and still links. A loading card is the skeleton at its exact layout.

**The horizontal rail.** A row of cards moved by translating the track, one card per step, with previous and next circles at desktop that brighten on hover, a thin progress bar with a dark thumb showing the visible fraction, and an uppercase heading with `View All` on the same line. Two cards per screen at mobile, three at tablet, four at desktop, trimmed so a partial card always shows at the trailing edge. At mobile the arrows are removed and the track is a native horizontal scroll with snap points.

**Home.** About three and a half screens. A full bleed hero carousel of nine slides, each a photograph with a lower left text block: a display face title, a one line subtitle and a black button with a white uppercase label. It advances about every five seconds with a slow slide, and its bullets double as a timer: the active one is a short bar filling across. Advance pauses on hover, on focus within and under reduced motion. Then `SHOP BY CATEGORY` with `View All`, three chips, `Tech`, `Bags` and `Work Essentials`, the selected one black with a white label, swapping the rail beneath without navigating; the rail holds `Phone Cases`, `Watch Bands`, `Power Banks` and `Wireless Chargers`. Then three rails, `NEW IN TECH`, `TRENDING COLLECTION` and one seasonal rail, of wide cards with a landscape image, a one line title and a quiet subtitle such as `Pick from 4 modules` instead of a price, the one place a card shows no price. Then `FEATURED IN` with monochrome publication wordmarks and `SEE MORE FEATURES`, then the reassurance strip, the newsletter and the footer.

**Category.** A centred uppercase heading over a full bleed rule, then a grid of circular tiles on the sunken ground, each with a medium uppercase caption, four across at desktop, three at tablet, two at mobile. No products, no filters, no sort. Each tile opens a listing.

**Listing.** A generated heading, then a circle strip of sibling listings led by an accent circle reading `All`, then a sticky filter bar: `Filters` outlined in the accent on the left, a circular sort button on the right, and under it the model chip, `Model:` in quiet text and the model in accent text with a chevron. `Filters` opens a panel at desktop and a bottom sheet at mobile, one accordion per facet; colour is drawn as named swatches. Active facets become removable chips, with `Clear all` once two or more are active. Sort, `Sort by`, is a bottom sheet at every size: `Recommended`, `Newest first`, `Price: low to high`, `Price: high to low`, `Discount` and `Best selling`. The circle strip reads `All`, `Basics`, `Clarity 3.0`, `Phone Bags`, `Phone Lanyards`, `Phone Wallets` and `Phone Grip`. Grid items enter with `slideUpFade`, staggered and capped so the last card of a page does not wait long. A skeleton page is drawn as soon as a request leaves.

**Ecosystem collection.** Roughly ten screens. A full bleed photograph with no headline and three award cards in its upper right, each a white card with a wordmark over a year, reading `Form Prize`, `Object Award` and `Good Craft Medal`. Then the statement block: `LATCH PHONE ECOSYSTEM` in the interface family at regular weight, the largest type in the product, over its body. Then two story blocks, a looping muted film beside a text column, alternating sides at desktop and stacked film first at mobile; films are muted, looping, without controls, play inline, and pause out of view and under reduced motion, showing their first frame. Then eight rails in assembly order, cases first, then what attaches, then what changes a case's look, with headings in tertiary text so eight in a row do not shout: `LATCH PHONE CASE` in five colourways, `LATCH CLEAR PHONE CASE` in two, `LATCH SIGNATURE PHONE CASE` in five, `LATCH PHONE GRIP & STAND` in four, `LATCH PHONE WALLET STAND` in four, `LATCH FLEX STAND` in five, `LATCH PHONE LANYARD` in five and `LATCH COLOUR PLATE` in four. Then the reassurance strip, the newsletter and the footer.

**Product.** Media and buy panel side by side at desktop, stacked with the media first at mobile. The media pane is square on the sunken ground, up to twelve images per variant, with chevrons, bullets whose active one is the accent, the badge upper left, and share and heart upper right; at mobile it gains a back chevron, moves the heart beside the bullets and is swipeable. The buy panel, top to bottom: the title; the price row with `MRP Inclusive of all taxes`; `SELECT DEVICE`, a full width raised field with the current model in accent text and a chevron, opening the model picker as a panel at desktop and a bottom sheet at mobile; `COLOR`, a row of swatches each named underneath; `ADD TO CART`, full width in the accent; the delivery check, a field reading `Enter Pincode To Check Delivery` beside `CHECK`, disabled until six digits are entered, replaced in place by the result and a `Change` button; `BUILD YOUR LATCH`, up to four rows each a white card with a thumbnail, a one line title, selectable swatches, prices and an outlined `ADD`; the gift strip, `Make it a gift` with `Learn more`; four attribute glyphs captioned `Latch Add-ons`, `MagLock-Ready`, `Lightweight` and `Raised Bezel`; the accordions `Product Details`, `Specifications` and `Delivery Time & Returns`, one open at a time, their chevrons turning; and a second `ADD TO CART`. At mobile a sticky bar carries `ADD TO CART` only while neither in-panel button is visible, so there are never two in view. Then `YOU MAY ALSO LIKE`, the reassurance strip, the newsletter and the footer.

**Cart.** Empty: no rail, no footer, no newsletter, no scroll; `YOUR SHOPPING CART IS EMPTY`, `Fill it with LatticeGoods` and `BROWSE PRODUCTS` centred. Filled: lines beside a sticky summary at desktop. Each line shows a thumbnail, the full title, a quiet line naming the colourway and the device cut separately, the live and struck prices, a stepper, and `Remove`. The stepper's minus is disabled at one rather than removing, its plus is disabled at the available stock, and a change appears at once and snaps back if the server refuses it. The summary reads `Subtotal`, `Discount` as a negative accent line, `Delivery`, reading `Calculated at checkout` until a pincode is known, `Order total`, and `CHECKOUT`.

**Checkout.** Three blocks on one route, each opening when the one above completes: `Contact and address`, with the phone read only, a name, an email, the address lines and the pincode prefilled from the delivery check with city and region derived and editable, or a saved address for a returning shopper; `Delivery`, the methods for the pincode each with a price and a window, the cheapest preselected; and `Payment`. The summary stays visible and read only; the cart cannot be edited from checkout. Confirmation shows `Order LG-100042 confirmed` in form, the delivery window, the address, read only lines, the totals, `Track this order` and `Continue shopping`, and is reachable again at the same layout from order history.

**Store directory.** A map on one side and a panel on the other at desktop; the panel first under a map band at mobile; the page body never scrolls. The panel reads `FIND A STORE`, a search field whose placeholder cycles slowly through `Search for "City"`, `Search for "State"` and `Search for "Pincode"`, stopping on focus, with text, and under reduced motion; then chips `All`, `Brand Outlets`, `Arbor Premium Partner` and `Airport Outlets`; then store cards on the sunken ground, each with a quiet type label such as `LatticeGoods Store` or `LatticeGoods Airport Store`, the name, the address, a phone row, an hours row and `Get Directions` in the accent. Pins are accent teardrops. The map is pannable, zoomable and fully keyboard operable, with arrow keys panning and plus and minus zooming.

**Account.** A centred `MY ACCOUNT` heading over a rule, then a left column and a content pane. The left column: the identity block, then `HELP CENTER`, `WISHLIST` and `REWARDS`, the active entry in primary text and the rest in tertiary, the only navigation that dims its inactive entries. Signed out, the identity block reads `SIGN UP/LOGIN` and `Sign up for exclusive discounts`; signed in, the name, the masked phone and `Sign out`. `REWARDS` is inert, captioned `Coming soon`. The help centre heading `HELP CENTER` sits over a photograph and an orders strip, `For order status, returns, exchanges, and cancellations visit here` with `My Orders`, then `HELP TOPICS`, `Get help with common questions or get in touch with our support team`, and topic rows led by `Orders`, each opening questions whose answers open inline. The empty wishlist reads `Nothing saved yet` with `Browse products`.

**Sign in.** A centred modal panel over the sunken ground, a photograph on one side and the form on the other at desktop, full width without the photograph at mobile: `SIGNUP OR LOGIN`, one field labelled `Mobile*` with `+91` locked in a prefix cell, the consent line `By continuing, I agree to the Terms of Use and Privacy Policy` with both documents as links, and `CONTINUE`, disabled with a quiet label until ten digits are entered. `CONTINUE` swaps the panel in place for `Enter the code we sent you`, a resend timer and `Change number`.

**Search, not found and error.** Search shows the query with its count, then the filter bar and grid unchanged; empty, it offers the four most popular listings. The standing pages are one narrow reading column with a table of contents above six headings. Not found shows `404`, then `OOPS - WE COULDN'T FIND THE PAGE YOU WERE LOOKING FOR`, then four exits, `Head Home`, `Discover New Collections`, `Contact Customer Service` and `Search Your Favorites`. The error route shows `UNEXPECTED ERROR OCCURED`, spelled as measured, `Sorry for the inconvenience`, the status as `Error Code: 403` in form, and `RETRY` with a spinner inside while it retries.

**Named motion moments.** `spin` rotates the progress ring for a pending write. `slideInFromBottom` carries every bottom sheet up from below its resting place and `slideOutToBottom` carries it back down, each filling forwards so the sheet does not flash back. `fadeInUp` brings each merchandising row and story block up from a little below, once, the first time it enters view, and never gates the content behind it. `slideUpFade` staggers listing grid items. A skeleton's pale band sweeps across grey shapes at the final layout and stops the moment content arrives. The category panel arrives from a short offset above. The accordion chevron turns as its answer unfolds. The carousel's active bullet fills like a timer.

**Iconography, drawn in code.** Every glyph is inline geometry and no icon font is requested. The chrome glyphs are single strokes with round caps and joins and no fill, on a square box: search is a circle with a short handle off one shoulder; account is a small head circle over a shoulder arc; the bag is a bucket with a handle over it; the heart is an outline that fills when a product is saved, never turns accent and never animates beyond that; share is three circles joined by two lines. The functional glyphs are a right chevron, a mirrored left chevron, an arrow up, a close cross, a plus, a filter of three shortening lines, a sort of two opposed arrows, a map pin teardrop with a hollow centre, a phone handset, a clock face with two hands, a gift box with a bow, and a parcel cube. The two progress rings are one circle at two rendered sizes. The accordion and select chevron is a down chevron. Four decorative attribute drawings sit under the buy panel, each labelled in text.

**Module and component architecture.** Twelve components carry the product, and anything else is a composition of them:

| Component | Owns |
|---|---|
| `Header` | the rail, the panel trigger, the three glyph buttons and the cart count |
| `CategoryPanel` | the grouped link columns and the image cards |
| `SearchOverlay` | the field, the settling query and the suggestion rows |
| `ProductCard` | media, badge, save, swatches, title, prices and every card state |
| `Rail` | the track, the step, the controls and the progress thumb |
| `SwatchRow` | the circles, the inset ring and the overflow counter |
| `DevicePicker` | the model tree, the unavailable state, and its panel and sheet forms |
| `BuyPanel` | title, prices, the two selectors, the buy action and the accordions |
| `BuildPanel` | the compatible rows and their add action |
| `FilterSheet` | the facet groups, the chips and the clear action |
| `Accordion` | the header, the chevron and the one open at a time rule |
| `StoreCard` | the type label, the address, the phone and hours rows, and directions |

**The route owns the device; the component owns the colourway.** The device cut lives in the link and changing it navigates. A colourway is component state and never navigates, so two cards side by side hold their own colourways independently. The one exception is the product route, which writes the colourway into the link as a replacement rather than a new history entry, so a copied link shows the chosen colour and the back button still returns to the listing. The reassurance strip, the newsletter and the footer are one shared layout rather than components; each component draws its own skeleton; the badge is a slot in `ProductCard`, not a component.

**Accessibility, structure.** One main heading per route. The rail and the labelled footer are navigation landmarks. The device control is a button opening a listbox with an expanded state and an active descendant, returning focus to itself on close, with unavailable models marked disabled so their count is announced. The colour swatches are a radio group named `Colour`, each labelled with its colourway. Focus is trapped inside the sign in panel, the filter sheet, the sort sheet, the device picker and the search overlay, returns to the opener on close, and `Escape` closes all five. Every field has a persistent visible label; the pincode field is numeric with a numeric keypad hint; validation is announced politely under its field with a leading glyph. Films are decorative and hidden from assistive technology.

**Performance.** The budget: first contentful paint under `1.8s` and largest contentful paint under `2.5s` on a mid range phone on a slow connection; interaction to next paint under `200ms` for the swatch swap and add to cart; cumulative layout shift under `0.1`; and under `250KB` compressed transferred on the home route, media excluded. Name transitioned properties rather than transitioning all of them. Stop skeleton loops once content is present. Load the first product image eagerly and the rest on demand. Pause films out of view. Ship glyph geometry inline rather than as a font. Every product image is square with its size set, so the grid never shifts, served in a modern format with a fallback. A listing request returns only the card fields; the full product document is fetched only on the product route; and the build panel is one request resolved on the server rather than by walking edges in the browser.

**The zero-asset substitution guide.** The build ships no binary; every asset class is replaced by a recipe. **Product images** are generated: a vertical light gradient ground with a soft elliptical highlight; a rounded rectangle at the phone case aspect filled with the colourway, carrying a camera cutout, a magnetic ring outline and the dot lock pattern slightly darker than the body; a thin specular bar down the left edge; and one soft contact shadow. A clear finish shows the ground through at reduced strength with the dot pattern at full strength; a textured finish lays a grained noise field over the body. Twelve images per variant are twelve rotations of one object. **Swatches** are a radial gradient from a lightened to a darkened colourway, and a two tone plate is a circle split on a diagonal. **Video.** Each looping film becomes a drawn loop of about ten seconds: two cases swapping, and the dot grid at a shallow angle with a travelling specular band, both showing a still first frame under reduced motion. **Press and award marks** are set as type in the condensed cut, spaced and uppercase. **Fonts** are named families from a public font host. **The map** is a vector outline of the trading region inlined at build time, and the list alone grouped by region is the required fallback in every case.

**Copy deck.** These strings are exact.

| Where | String |
|---|---|
| hero 1 | `WANDER COLLECTION` / `Comfort carry inspired by nostalgia` |
| hero 2 | `LATCH CLEAR PHONE CASE` / `Clearly Playful, Clearly Latch` |
| hero 3 | `FLUX WIRELESS CHARGING ECOSYSTEM` / `Power that moves when you do` |
| hero 4 | `TIDY DESK ORGANISER` / `Slide into order` |
| hero 5 | `LATCH ECOSYSTEM` / `Your phone, your ecosystem, your way` |
| hero 6 | `HOLLOW TECH KIT` / `Home for your everyday tech` |
| hero 7 | `KINETIC CHARGING STATION 65W` / `Sculpted to power your everyday` |
| hero 8 | `SURGE POWER BANKS` / `Fast, future-ready, Qi-2 certified` |
| hero actions | `SHOP NOW`, and `EXPLORE NOW` on ecosystem slides |
| wide card subtitles | `Pick from 4 modules`, `Available in 4 Colours`, `Available in Multiple Variants` |
| ecosystem statement | `Latch is a modular system of phone accessories, a platform of possibilities. Built on our lock and release mechanism, every piece is modular by design: cases, grips, wallets, stands and colour plates. They click into place, switch in seconds, and work as one fluid system. Innovation here is about making everything coexist seamlessly. Quick to adapt, effortless to swap, always ready to play your way.` |
| story block one | `With self expression at its core, Latch slips into small moments to make them simply better. From the morning scroll, the quick call, to the coffee run, Latch accessories switch gears seamlessly. With over a thousand combinations to mix and match, it slips into every moment of work, play and rest.` |
| story block two | `Winner of the Form Prize, Object Award, and Good Craft Medal, Latch is built on precision. Thousands of hours of design iteration and testing go into every case, plate, and grip, refining each detail to look sharp, feel intuitive, and protect your phone. The Signature Dot Pattern defines its identity, powering the integrated lock mechanism and elevated through an iconic monogram.` |
| build panel rows, on `Latch Phone Case Cover for Arbone 16 Pro` | `Marigold Latch Phone Grip & Stand`, `Sage Latch Flex Stand`, `Cypress Latch Phone Wallet Stand`, `Amber Latch Phone Lanyard` |
| delivery results | `Delivers in 3 to 5 days`, `We do not deliver to this pincode yet` |
| cart stock | `Only 2 left`, and `Only 3 left` on `basics-clear-case-60-arbone-16-pro`, which holds three units |
| confirmation | `Order LG-100042 confirmed` |
| code entry error | `That code did not match. Two attempts left.` |
| store hours | `Monday - Sunday : 11:00 AM - 10:00 PM`, `Monday - Sunday : 24 hours`, `Monday - Friday: 11:00 AM - 9:30 PM` |

Every other exact string appears in the section that uses it above.

## Technical requirements

The backend is **Flask** on Python. The frontend is **React** built with **Vite**, served as a production build. The rendering model is a **single page application over a JSON API**: the browser receives an application shell on first paint and every route after that is painted from JSON the API returns. Persistent state lives in **PostgreSQL**, reached through `DATABASE_URL`. Payment invoices live in **Kill Bill** (`killbill`), reached through `PAYMENTS_API_URL` with `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`, `PAYMENTS_API_USER` and `PAYMENTS_API_PASSWORD`. Email is sent over SMTP to **Mailpit** (`mailpit`) at `SMTP_HOST` and `SMTP_PORT`, with `SMTP_USER` and `SMTP_PASS`. The app reads its own address from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port. `GET /api/health` returns `200` once the app is ready.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL (`postgres`), Kill Bill (`killbill`) and Mailpit (`mailpit`), and reaching for anything else is a contract violation. All three are **already running** and reachable at the variables above. Do not download, install, compile or start a copy of any of them.

**Kill Bill surface.** The storefront has its own Kill Bill user, already provisioned with account and invoice permissions and nothing more. Every call to `/1.0/kb/*` carries that user's HTTP Basic credentials from `PAYMENTS_API_USER` and `PAYMENTS_API_PASSWORD`, the `X-Killbill-ApiKey` and `X-Killbill-ApiSecret` headers from `PAYMENTS_API_KEY` and `PAYMENTS_API_SECRET`, and `X-Killbill-CreatedBy` on every write. `GET /1.0/healthcheck` is unauthenticated liveness. `GET /1.0/kb/accounts?externalKey={externalKey}` finds an account, `200` when it exists and `404` when it does not. `POST /1.0/kb/accounts` with `{"name", "externalKey", "email", "currency", "country"}` creates one, and a second create with a used external key is refused with `409`, so the external key, not an application check, is what keeps one account per shopper. `POST /1.0/kb/invoices/charges/{accountId}?autoCommit=true` with a list of `{"amount", "currency", "description"}` items creates one committed invoice carrying those items, and `GET /1.0/kb/invoices/{invoiceId}?withItems=true` reads an invoice back with its `amount`, its `currency` and its items. Kill Bill reports amounts as decimal rupees, `1599.00`, and currency in upper case, `INR`.

**Money.** Prices are shown with the currency symbol `₹`. Every amount the app's own API returns is integer paise with currency `inr`: `₹1599` is `159900`, never `1599` and never `1599.00`.

**Stock and orders under simultaneous requests and on replay.** When two order requests would each take the last unit of one variant, **exactly one** of them creates an order and the other is refused with a `409` conflict response naming the variant's SKU. Afterwards that variant's stock is zero, never below it, however the two requests interleave. When two requests together ask for more units than exist, the same holds: exactly one succeeds, and the stock left is what the winner did not take. A replayed payment for an order that is already paid returns the same invoice and **must not create a second** invoice in Kill Bill or a second confirmation email. The same holds for sign in codes and payments: a code's single use, the wrong code count, the code request limit and an order's single invoice each hold when the requests arrive at the same instant. Application-level checks alone are not enough to hold any of this. Choose any mechanism.

**Reading lists at scale.** A listing is addressed by its page number, which is an offset cursor over a stable sort, and every listing page holds twenty four products. An offset cursor is safe here because a listing's membership does not change while a shopper pages it. A listing response carries `items`, `page`, `page_size`, `total_count`, `has_more` and `next_page`: `total_count` counts every published product matching the filters, not the rows on this page; `has_more` is true only when a further page genuinely exists; and `next_page` is null on the last page. **Every filter, including publication, selects before the page is taken**, so a page is full whenever enough matching products exist. Order history takes `limit=` between `1` and `50`, defaulting to `10`, and a `limit=` outside that range is refused as invalid.

**Favicon.** The shell declares a favicon in its document head, and the path it declares answers `200`.

Every business-rule violation is rejected as a client error with a reason, never as a server error and never as a silent success. A failed operation leaves no partial state.

## Data model

Fifteen tables, one per entity below, and the invariants stated with each. All timestamps are UTC. The three critical behaviours, the last unit sold once, an unpublished product unreachable and each colourway priced as itself, rest on these invariants. There is no password anywhere: the seeded shoppers sign in with a code sent to their email in Mailpit, and `/app/USER_README.md` states each seeded phone and email and says so.

### `device_brands`

`slug`, `name`, `rank`, `active`. Seeded: `arbor` `Arbor` rank 1; `solaris` `Solaris` rank 2; `universal` `Universal` rank 3.

### `device_families`

`slug`, `name`, `brand`, `rank`. Seeded: `phone` under `arbor` and under `solaris`, and `accessory` under `universal`. A family is identified by its slug across brands, so every phone model, Arbor or Solaris, is in family `phone`.

### `device_models`

`slug`, `name`, `brand`, `family`, `rank`, `retired`.

| `slug` | `name` | brand | family | rank | retired |
|---|---|---|---|---|---|
| `arbone-17-pro-max` | `Arbone 17 Pro Max` | `arbor` | phone | 1 | false |
| `arbone-17-pro` | `Arbone 17 Pro` | `arbor` | phone | 2 | false |
| `arbone-17` | `Arbone 17` | `arbor` | phone | 3 | false |
| `arbone-16-pro` | `Arbone 16 Pro` | `arbor` | phone | 4 | false |
| `arbone-16` | `Arbone 16` | `arbor` | phone | 5 | false |
| `solarion-s26-ultra` | `Solarion S26 Ultra` | `solaris` | phone | 6 | false |
| `solarion-s25-ultra` | `Solarion S25 Ultra` | `solaris` | phone | 7 | false |
| `arbone-15` | `Arbone 15` | `arbor` | phone | 8 | **true** |
| `universal` | `Universal` | `universal` | accessory | 9 | false |

### `categories`

`slug`, `name`, `parent`, `rank`, `tile_media`. Seeded: `phone-cases` `Phone Cases`; `phone-grips` `Phone Grip`; `phone-stands` `Stands`; `phone-wallets` `Phone Wallets`; `phone-lanyards` `Phone Lanyards`; `colour-plates` `Colour Plates`.

### `products`

`handle` (unique), `title_tail`, `category`, `line`, `design`, `device_model`, `badge`, `features`, `material`, `sequence`, `published`. `newest` sorts by `sequence` descending. A product's lowest live price, largest discount and units sold are **derived on read** from its variants and paid orders, never stored.

### `variants`

`sku` (unique), `product`, `position`, `colourway`, `list_price`, `live_price`, `stock`. `stock` is never negative and `live_price` is never above `list_price`. The first colourway is `position` 1. A variant's SKU is its product handle, a hyphen, and the colourway in lower case, for example `latch-clear-phone-case-arbone-16-pro-umber`.

**Hand-seeded products.** Prices are in rupees here and in paise in the API. Features `add-on-compatible,magnetic` is abbreviated `lock+mag`.

| `handle` | `title_tail` | category | line | design | model | features | material | sequence | published | badge | colourways, in position order: live / list / stock |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `latch-phone-case-arbone-16-pro` | `Latch Phone Case Cover` | `phone-cases` | `latch` | `latch-phone-case` | `arbone-16-pro` | lock+mag | `silicone` | 904 | true | none | `Basalt` 1599/1799/20; `Sage` 1599/1799/20; `Amber` 1599/1799/20; `Violet` 1599/1799/20; `Fern` 1599/1799/0 |
| `latch-clear-phone-case-arbone-16-pro` | `Latch Clear Phone Case Cover` | `phone-cases` | `latch` | `latch-clear-phone-case` | `arbone-16-pro` | lock+mag | `polycarbonate` | 903 | true | `NEW!` | `Umber` 1799/2299/12; `Cinnabar` 1599/2299/12 |
| `latch-signature-phone-case-arbone-16-pro` | `Latch Signature Phone Case Cover` | `phone-cases` | `latch` | `latch-signature-phone-case` | `arbone-16-pro` | lock+mag | `vegan-leather` | 902 | true | none | `Sage` 1799/1999/15; `Ochre` 1799/1999/1; `Cerise` 1799/1999/3; `Umber` 1799/1999/15; `Marigold` 1799/1999/15 |
| `clarity-maglock-case-arbone-16-pro` | `Clarity 3.0 Clear MagLock Phone Case Cover` | `phone-cases` | `clarity` | `clarity-maglock-case` | `arbone-16-pro` | `magnetic` | `polycarbonate` | 901 | true | none | `Umber` 999/1999/30 |
| `latch-phone-case-arbone-17-pro` | `Latch Phone Case Cover` | `phone-cases` | `latch` | `latch-phone-case` | `arbone-17-pro` | lock+mag | `silicone` | 905 | true | none | `Basalt` 1599/1799/20; `Sage` 1599/1799/20; `Cypress` 1599/1799/20 |
| `latch-phone-case-arbone-17` | `Latch Phone Case Cover` | `phone-cases` | `latch` | `latch-phone-case` | `arbone-17` | lock+mag | `silicone` | 906 | **false** | none | `Basalt` 1599/1799/20 |
| `latch-phone-case-solarion-s26-ultra` | `Latch Phone Case Cover` | `phone-cases` | `latch` | `latch-phone-case` | `solarion-s26-ultra` | lock+mag | `silicone` | 907 | true | none | `Amber` 1599/1799/20; `Basalt` 1599/1799/20 |
| `latch-phone-case-arbone-15` | `Latch Phone Case Cover` | `phone-cases` | `latch` | `latch-phone-case` | `arbone-15` | lock+mag | `silicone` | 800 | true | none | `Basalt` 1599/1799/5 |
| `latch-phone-grip-stand` | `Latch Phone Grip & Stand` | `phone-grips` | `latch` | `latch-phone-grip-stand` | `universal` | `add-on-compatible` | `aluminium` | 951 | true | none | `Marigold` 1499/1999/25; `Basalt` 1499/1999/25; `Sage` 1499/1999/25; `Cerise` 1499/1999/25 |
| `latch-flex-stand` | `Latch Flex Stand` | `phone-stands` | `latch` | `latch-flex-stand` | `universal` | lock+mag | `aluminium` | 952 | true | none | `Sage` 999/1299/25; `Basalt` 999/1299/25; `Amber` 999/1299/25; `Fern` 999/1299/25; `Violet` 999/1299/25 |
| `latch-phone-wallet-stand` | `Latch Phone Wallet Stand` | `phone-wallets` | `latch` | `latch-phone-wallet-stand` | `universal` | `add-on-compatible` | `vegan-leather` | 953 | true | none | `Cypress` 2999/3499/25; `Basalt` 2999/3499/25; `Umber` 2999/3499/25; `Amber` 2999/3499/25 |
| `latch-phone-lanyard` | `Latch Phone Lanyard` | `phone-lanyards` | `latch` | `latch-phone-lanyard` | `universal` | `add-on-compatible` | `nylon` | 954 | true | none | `Amber` 2499/2999/25; `Basalt` 2499/2999/25; `Sage` 2499/2999/25; `Ochre` 2499/2999/25; `Cerise` 2499/2999/25 |
| `latch-colour-plate` | `Latch Colour Plate` | `colour-plates` | `latch` | `latch-colour-plate` | `universal` | `add-on-compatible` | `polycarbonate` | 955 | true | none | `Violet` 799/999/25; `Ochre` 799/999/25; `Fern` 799/999/25; `Cypress` 799/999/25 |
| `latch-ring-mount` | `Latch Ring Mount` | `phone-grips` | `latch` | `latch-ring-mount` | `universal` | lock+mag | `aluminium` | 956 | **false** | none | `Basalt` 1299/1499/25 |

**Generated Basics range.** For every non retired phone model and each whole number `n` from `1` to `60`, exactly one product exists, where `NN` is `n` written with two digits and the eleven colourways are, in order from zero, `Amber`, `Violet`, `Sage`, `Basalt`, `Ochre`, `Cinnabar`, `Umber`, `Cerise`, `Fern`, `Marigold` and `Cypress`:

| Field | Value |
|---|---|
| `handle` | `basics-clear-case-NN-` followed by the model slug |
| `title_tail` | `Basics Clear Case Cover No. NN` |
| `category`, `line`, `design`, `features`, `material`, `badge` | `phone-cases`, `basics`, `basics-clear-case-NN`, none, `polycarbonate`, none |
| `sequence` | the model's rank times `100`, plus `n` |
| `published` | false when `n` is a multiple of `13`, otherwise true |
| the one variant's colourway | the colourway at position `(n * 7) mod 11` |
| its `list_price`, rupees | `999 + ((n * 37) mod 11) * 100` |
| its `live_price`, rupees | `list_price - ((n * 13) mod 6) * 100` |
| its `stock` | `(n * 5) mod 9` |

Worked rows for `arbone-16-pro`, which must match exactly:

| `n` | handle | colourway | list | live | stock | published | sequence |
|---|---|---|---|---|---|---|---|
| 1 | `basics-clear-case-01-arbone-16-pro` | `Cerise` | 1399 | 1299 | 5 | true | 401 |
| 7 | `basics-clear-case-07-arbone-16-pro` | `Cinnabar` | 1599 | 1499 | 8 | true | 407 |
| 13 | `basics-clear-case-13-arbone-16-pro` | `Basalt` | 1799 | 1699 | 2 | false | 413 |
| 60 | `basics-clear-case-60-arbone-16-pro` | `Sage` | 1899 | 1899 | 3 | true | 460 |

Counts that follow and must hold: `434` products carrying `463` variants, `404` of the products published, and `12` stores. The `phone-cases` listing for `arbone-16-pro` holds `60` published products across three pages of `24`, `24` and `12`. Filtered to the `magnetic` feature it holds exactly `4`. The unconstrained `phone-cases` listing holds `399`.

### `compatibility`

`case_product`, `module_product`, `interface` (`lock` or `magnetic`), `rank`, unique on the pair. Every product whose line is `latch` and whose category is `phone-cases`, published or not, has six edges: to `latch-ring-mount`, `lock`, rank 1; `latch-phone-grip-stand`, `lock`, rank 2; `latch-flex-stand`, `magnetic`, rank 3; `latch-phone-wallet-stand`, `lock`, rank 4; `latch-phone-lanyard`, `lock`, rank 5; and `latch-colour-plate`, `lock`, rank 6. `clarity-maglock-case-arbone-16-pro` has one edge, to `latch-flex-stand`, `magnetic`, rank 1.

### `shoppers`

`id`, `phone` (unique, ten digits), `name`, `email`, `created_at`. Seeded as in User roles.

### `sign_in_codes`

`phone`, `code_hash`, `created_at`, `expires_at`, `used_at`, `cancelled_at`. The failure count and the lock that governs a phone are recorded against the phone.

### `carts` and `cart_lines`

`carts`: `token` (unique), `created_at`, `updated_at`. `cart_lines`: `cart`, `sku`, `quantity`, `unit_live_price`, `unit_list_price`, unique on cart and SKU.

### `orders` and `order_lines`

`orders`: `number` (unique), `shopper`, `name`, `email`, `address`, `pincode`, `delivery_method`, `state` (`pending` or `paid`), `subtotal`, `discount`, `delivery`, `total`, `killbill_invoice_id`, `created_at`, `paid_at`. `order_lines`: `order`, `sku`, `title`, `colourway`, `device_model`, `quantity`, `unit_price`, `list_price`. An order line is written once and never updated.

### `wishlist_items`

`shopper`, `product`, `created_at`, unique on the pair.

### `newsletter_subscribers`

`email` (unique), `created_at`.

### `stores`

`name`, `type`, `address`, `city`, `region`, `pincode`, `phone`, `hours`, `latitude`, `longitude`, `active`.

| name | type | city | region | pincode | hours | active |
|---|---|---|---|---|---|---|
| `LatticeGoods Store Linking Road` | `brand_outlet` | `Mumbai` | `Maharashtra` | `400050` | `Monday - Sunday : 11:00 AM - 10:00 PM` | true |
| `LatticeGoods Airport Store Terminal 2` | `airport_outlet` | `Mumbai` | `Maharashtra` | `400099` | `Monday - Sunday : 24 hours` | true |
| `LatticeGoods Store Colaba` | `brand_outlet` | `Mumbai` | `Maharashtra` | `400005` | `Monday - Sunday : 11:00 AM - 10:00 PM` | **false** |
| `LatticeGoods Store Select Citywalk` | `brand_outlet` | `Delhi` | `Delhi` | `110017` | `Monday - Sunday : 11:00 AM - 10:00 PM` | true |
| `LatticeGoods Airport Store Terminal 3` | `airport_outlet` | `Delhi` | `Delhi` | `110037` | `Monday - Sunday : 24 hours` | true |
| `Arbor Premium Partner Indiranagar` | `premium_partner` | `Bengaluru` | `Karnataka` | `560038` | `Monday - Friday: 11:00 AM - 9:30 PM` | true |
| `LatticeGoods Airport Store Kempegowda` | `airport_outlet` | `Bengaluru` | `Karnataka` | `560300` | `Monday - Sunday : 24 hours` | true |
| `LatticeGoods Store Phoenix Marketcity` | `brand_outlet` | `Pune` | `Maharashtra` | `411014` | `Monday - Sunday : 11:00 AM - 10:00 PM` | true |
| `LatticeGoods Store Express Avenue` | `brand_outlet` | `Chennai` | `Tamil Nadu` | `600002` | `Monday - Sunday : 11:00 AM - 10:00 PM` | true |
| `Arbor Premium Partner Banjara Hills` | `premium_partner` | `Hyderabad` | `Telangana` | `500034` | `Monday - Friday: 11:00 AM - 9:30 PM` | true |
| `LatticeGoods Store Park Street` | `brand_outlet` | `Kolkata` | `West Bengal` | `700016` | `Monday - Sunday : 11:00 AM - 10:00 PM` | true |
| `LatticeGoods Store MI Road` | `brand_outlet` | `Jaipur` | `Rajasthan` | `302001` | `Monday - Sunday : 11:00 AM - 10:00 PM` | true |

Each store's address is its name's place followed by its city, its phone is `+91 22 4000` followed by a four digit number, and its coordinates place it in its city. Nothing grades those three fields.

There is no merchandising screen. The catalogue is edited directly in the `products` and `variants` rows while the app runs, and the storefront shows an edited title tail or price on its next read.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- These are deliberate scope cuts, recorded rather than invented. One selling business: no second seller, no marketplace listing, no auction.
- No customer reviews, no live chat, no subscription plan and no loyalty points ledger. Rewards is a named, inert entry reading `Coming soon`.
- No password, no email sign in and no social sign in.
- No payment method, card, refund or chargeback surface. Payment is an invoice in Kill Bill.
- The gift wrapping choice is recorded as a single cart level flag; no wrapping options are specified. Personalisation and engraving are absent.
- The corporate gifting entry resolves to a standing page, the blog is an external link, and the mobile application exists only as two store badge links.
- No external network call at runtime, and no analytics measurement identifier: the default is none.
- No dark theme.
- The shop must stay responsive with the full seeded catalogue of `434` products and a cart of at least `50` lines.

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

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status"}` |
| `POST /api/auth/request-code` | `{"phone", "email"}` | `{"sent": true}` |
| `POST /api/auth/verify-code` | `{"phone", "code"}` | `{"access_token", "shopper": {"phone", "name", "email"}}`; a refusal carries `{"error", "attempts_left"}` |
| `POST /api/auth/sign-out` | none | `{"signed_out": true}` |
| `GET /api/device-models` | none | `{"items": [{"slug", "name", "brand", "family", "rank"}]}`, non retired only |
| `GET /api/products` | `category`, `model`, `colour`, `material`, `feature`, `price_band`, `sort`, `page` | `{"heading", "retired_model", "items": [{"handle", "title", "badge", "sold_out", "swatches", "extra_count", "live_price", "list_price"}], "page", "page_size", "total_count", "has_more", "next_page"}` |
| `GET /api/products/{handle}` | none | `{"handle", "title", "category", "line", "design", "device_model": {"slug", "name", "retired"}, "badge", "features", "material", "variants": [{"sku", "colourway", "live_price", "list_price", "stock", "sold_out"}]}` |
| `GET /api/products/{handle}/device-options` | `colourway` | `{"current", "options": [{"slug", "name", "available", "handle", "colourway"}]}`; `handle` and `colourway` are null when unavailable |
| `GET /api/products/{handle}/compatible` | none | `{"items": [{"handle", "title", "sku", "colourway", "live_price", "list_price"}]}` |
| `GET /api/search` | `q`, `page` | `{"redirect", "items", "page", "page_size", "total_count", "has_more", "next_page"}` |
| `GET /api/delivery` | `pincode` | `{"pincode", "serviceable", "message", "methods": [{"code", "price", "window"}]}` |
| `GET /api/cart` | none | `{"lines": [{"sku", "title", "colourway", "device_model", "quantity", "unit_live_price", "unit_list_price", "available_stock", "sold_out", "warning"}], "subtotal", "list_total", "discount", "currency"}` |
| `POST /api/cart/lines` | `{"sku", "quantity"}` | the cart |
| `PATCH /api/cart/lines/{sku}` | `{"quantity"}` | the cart |
| `DELETE /api/cart/lines/{sku}` | none | the cart |
| `POST /api/orders` | `{"name", "email", "address": {"line1", "line2", "city", "region", "pincode"}, "delivery_method"}` | `{"number", "state", "lines": [{"sku", "title", "colourway", "device_model", "quantity", "unit_price", "list_price"}], "subtotal", "discount", "delivery", "total", "currency"}`; a stock conflict carries `{"error", "sku", "available"}` |
| `POST /api/orders/{number}/pay` | none | `{"number", "state", "invoice_id"}` |
| `GET /api/orders` | `limit`, `page` | `{"items", "page", "total_count", "has_more", "next_page"}` |
| `GET /api/orders/{number}` | none | the order |
| `GET /api/wishlist` | none | `{"items": [{"handle", "title"}]}` |
| `POST /api/wishlist` | `{"handle"}` | `{"items": [{"handle", "title"}]}` |
| `DELETE /api/wishlist/{handle}` | none | `{"items": [{"handle", "title"}]}` |
| `GET /api/stores` | `q`, `type` | `{"items": [{"name", "type", "address", "city", "region", "pincode", "phone", "hours", "latitude", "longitude"}]}` |
| `POST /api/newsletter` | `{"email"}` | `{"message"}` |

List endpoints return their rows under `items`. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a `5xx` and never as a silent success. Bearer auth is required on `POST /api/auth/sign-out`, every `/api/orders` endpoint and every `/api/wishlist` endpoint, and nowhere else. The cart is identified by the `cart_token` cookie, not by the bearer token.

**No mocks.** A paid order's invoice must exist as a real invoice in Kill Bill, on the account whose external key is `shopper-` followed by the shopper's phone, for the exact order total in `INR`. A `paid` column the app sets for itself, an invoice number the app invents, or an email the app writes to its own log are all violations however convincing the confirmation page looks. Likewise a sign in code or a confirmation must be delivered as a real email through Mailpit. Kill Bill and Mailpit are the facts: the app's own tables and interface can only reflect what lives there, never substitute for it.

## Definition of done

A shopper picks a phone, opens a Latch case cut for it, adds a compatible module from the build panel, signs in with a code from their inbox and pays, and the order exists as one Kill Bill invoice for its exact total with one confirmation email. Two shoppers racing for the last unit produce one order and a stock of zero. An unpublished product cannot be reached, listed or bought by any route.
