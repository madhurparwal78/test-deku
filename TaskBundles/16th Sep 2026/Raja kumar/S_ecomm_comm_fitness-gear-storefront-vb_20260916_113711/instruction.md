# Peakfit

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, put a pair of running shoes in the bag, check out with a phone number and a postal code, choose to pay the courier on delivery, and follow that order to delivered, without hitting an error page.

The invoice for a cash on delivery order must exist as a real invoice in `killbill`, on the Kill Bill account for that phone, for the exact amount collected in `INR`, and it must appear only once the parcel is delivered. An invoice raised when the order is placed, a paid flag the app keeps for itself, or a second invoice when the same delivery is reported twice are all wrong, however the order page looks.

## Overview

Peakfit is a direct to consumer storefront for home fitness equipment, sports shoes, sneakers and apparel, selling into a market where most orders are paid in cash on delivery. It is one brand's own shop, not a marketplace. Four departments hold a catalogue from a `299` rupee resistance band to a `5,699` rupee vibration plate.

Three things shape everything: every price is a discount, shown as three numbers together; the promotional strip at the top is permanent furniture; and the department menu is a shop, rendering real products rather than links.

The hard part is the order after the click: stock held and sold once, totals recomputed on the server, payment on delivery re-checked and invoiced only when the courier collects, and carrier events that apply once and never move an order backwards.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Customer, as a guest | Browse, search, fill a bag, check out with a phone and an address, track an order with its number and the phone's last four digits | **Cannot read or cancel any order by number alone.** **Cannot reach a merchant route** |
| Customer, signed in | Everything a guest can; read and cancel their own orders, request returns, save addresses, write a review of a delivered product | **Cannot read, cancel or return another customer's order.** **Cannot reach a merchant route** |
| Merchant | Change prices and stock, pack, confirm and cancel orders with a reason, work the confirmation queue, moderate reviews, merchandise | **Cannot type a struck through price.** **Cannot see a confidence score** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a customer session to any merchant-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is **open**: a phone that has never verified a code becomes a customer when its first code is verified. There is no password. Seeded accounts are listed under `## Data model`.

## Core features

1. **An invoice exists on the Kill Bill account for the right amount, in `INR`.** A prepaid order is invoiced when it is placed. A cash on delivery order is invoiced only when delivered, and never if it is cancelled or refused. A partial advance is invoiced twice: the advance at placement, the rest at delivery. A repeated delivery report invoices nothing more.
2. **Sign in is a phone and a six digit code** sent by email. A code is used once, belongs to one phone, and for a known phone goes only to the email on file; any other code gets `401`.
3. **Checkout needs no account.** A cash on delivery order needs the phone verified by code before it is accepted, or gets `422`.
4. **Totals are recomputed on the server at placement.** A stale total or a changed price stops the order with `409` and names what changed; the client's total is never trusted.
5. **A unit is held or sold once.** Stock in a bag is held and counted as unavailable; two customers racing for the last unit never both get it; the other gets `409`.
6. **Cash on delivery is re-checked at placement** by postal code, cart value, product and delivery confidence; a failed check answers `422` with the reason; prepaid is always offered.
7. **Placing the same order twice with one idempotency key makes one order.** Another body under that key gets `409`.
8. **Carrier events apply once and never move an order backwards**; an unsigned event gets `401`; refused and returned to origin are separate states, and stock returns exactly once.
9. **A customer may cancel until the order is packed**, then gets `409`, and never cancels someone else's order.
10. **Tracking by order number and the phone's last four digits shows the timeline and nothing else**, and answers `429` after repeated wrong guesses.
11. **A return refunds what the line actually paid**, within seven days of delivery; later requests get `422`.
12. **A struck through price is a price the product was really sold at**, taken from its recorded price history, and a typed one gets `422`; a low stock badge counts units held in bags.
13. **Only a customer whose order of a product was delivered may review it**; anyone else gets `403`.
14. **An unknown address renders Peakfit's own not-found page**, with a search field and the best sellers, answering `404`.
15. **A privacy page, linked from every page's footer,** states what Peakfit records about a customer and how long it keeps it.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: marquee, hero, category row, shelves | public |
| `/collections/<handle>` | a department or collection grid | public |
| `/products/<handle>` | a product page | public |
| `/search` | results | public |
| `/cart` | the bag at length; the drawer slides over every page | public |
| `/checkout` | one page, three steps | public |
| `/orders/<number>/confirmation` | the full page confirmation | public |
| `/track` | tracking without an account | public |
| `/account` | sign in, orders, addresses, returns | customer |
| `/account/orders/<number>` | one order and its timeline | customer |
| `/build` | the goal kit builder | public |
| `/pages/<handle>` | policies and information | public |
| `/merchant` | orders, confirmation queue, catalogue, reviews | merchant |

**Entry.** Every storefront route is public. `/account` without a session shows sign in by phone. A merchant route without a merchant session renders the not-found page.

**Journeys.**
1. A guest opens `stridewell road runner`, picks UK 8, and the bag slides over from the right showing the line and how far the bag is from the next offer.
2. At `/checkout` the guest gives a phone, an email and an address in `560001`, chooses cash on delivery, enters the emailed code, and lands on a full page confirmation stating the amount due to the courier.
3. The guest opens `/track`, enters the order number and the phone's last four digits, and reads the timeline.
4. A signed in customer returns one line of a delivered order with a reason from the list.

**States.** Every screen has loading as a skeleton, empty with a title, a sentence and an action, populated, error with a retry, and not permitted as the not-found page.

## UI/UX notes

The north star is that a shopper always knows the price, the saving and whether they can pay on delivery.

**Voice.** Headings are very heavy, tightly tracked capitals in the display family; product names beneath them are lowercase `Inter`, which also sets body, captions and prices with aligned figures. That contrast is the design.

**Components.** Pills and the search field are fully rounded, cards softly rounded. Focused fields show a ring, labels sit above fields and errors below, a transient message confirms an outcome then dismisses itself, drawers and sheets close on Escape, and removing a bag line asks first.

**Colour.** Light mode only, designed fully. Photography carries colour on near-white grounds and warm surfaces, with near-black text, warm neutral muted text and hairline borders. One signature light, vivid amber, the brand yellow, sits behind a word of display type and inside promotional emphasis, never on a button. The primary action is near-black, lightening on hover; links are mid, vivid blue. Prices speak in near-black neutral, a mid warm neutral for the struck original, and a mid, vivid green for the saving. Success reads green, warning orange, danger red, each beside a word.

**Motion.** Movement is quick and eased on four curves: a house curve leaving fast and settling long for slides, drawers and panels, a symmetric one for hovers, a decelerate for entrances, and a longer one for the drawer. Under a reduced motion preference the marquee steps instead of scrolling, the carousel does not advance, and drawers open without travel.

**Accessibility.** Contrast meets WCAG AA against every ground, keyboard navigation reaches every control with a visible focus ring, state is never carried by colour alone, icon-only controls are labelled, and touch targets are comfortable. Every content image carries alternative text, and decorative images declare themselves decorative.

**Responsive.** Layouts hold at every viewport width: two columns of cards on a phone, three on a tablet, four on a desktop, with a sticky action bar on a phone product page.

Density is comfortable, and the layout archetype is a top navigation.

## Front-end specification

### The scheme

Light, with photography carrying the colour and a small utilitarian palette around it. Every colour is named by role; the exact shades are the builder's to choose, so long as each keeps its role and its relationships.

| Role | Carried as |
|---|---|
| primary text, used across the site | near-black neutral |
| secondary text | near-black neutral, a step lighter |
| captions and meta | mid warm neutral |
| disabled | mid warm neutral, lighter |
| page ground | near-white neutral, pure |
| section grounds, the warm off-white | near-white warm neutral |
| card ground | near-white neutral, a touch warmer |
| alternate section ground | near-white neutral, cool |
| hairlines on the warm ground | near-white warm neutral, darker |
| hairlines on the cool ground | near-white neutral, cool |
| the display accent, behind and inside display type | light, vivid amber, the brand yellow |
| its brighter twin | light, vivid amber, a brighter yellow |
| a neutral accent | light warm neutral |
| links and the secondary action | mid, vivid blue |
| its pressed state | mid, soft blue |

The yellow is the brand's signature and is used exactly twice on the home page: as a fill behind a word of display type in the hero, and as an emphasis inside promotional copy. It is never a button.

### Commerce colours

| Role | Carried as |
|---|---|
| the selling price | near-black neutral |
| the struck-through original, the price-compare colour | mid warm neutral |
| the saving badge | mid, vivid green |
| its ground | near-white neutral with a green cast |
| low stock warning | mid, vivid orange |
| out of stock | mid, vivid red |
| order placed, delivered | deep, vivid teal, read as a green |
| pending, in transit | light, vivid orange |
| cancelled, failed, returned | mid, vivid red |
| informational | mid, vivid blue |
| the messaging channel control | mid, vivid green |

**A saving is always shown three ways together:** the selling price, the struck through original, and the percentage saved. Two of the three is what most storefronts do and it makes the third ambiguous.

### Type

Three families. The heavy display family is licensed and not bundled, so the build uses its stated stack; the heavy fallback keeps the effect, because the effect is weight and tracking rather than letterforms.

| Family | Weight | Role | Stack |
|---|---|---|---|
| heavy display | `900` | hero overlays, section headings, the shop's voice | `"Arial Black", "Helvetica Neue", Impact, sans-serif` |
| rounded display | `400` | secondary headings | `Verdana, Tahoma, sans-serif` |
| `Inter` | `300` to `700` | everything else | `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif` |

| Role | Size | Line height | Weight | Family |
|---|---|---|---|---|
| Hero overlay | `120px` | `104px` | 900 | heavy display |
| Section heading | `40px` | `44px` | 900 | heavy display |
| Collection banner name | `56px` | `56px` | 900 | heavy display, uppercase |
| Department tabs | `13px` | `18px` | 700 | heavy display, uppercase, wide tracking |
| Card title | `14px` | `20px` | 400 | Inter |
| Price | `16px` | `22px` | 600 | Inter |
| Compare price | `14px` | `20px` | 400 | Inter |
| Product page title | `24px` | `32px` | 600 | Inter |
| Product page price | `28px` | `34px` | 700 | Inter |
| Product page original | `18px` | `24px` | 400 | Inter |
| Body | `16px` | `24px` | 400 | Inter |
| Information page heading | `24px` | `32px` | 700 | Inter |
| Information page body | `16px` | `26px` | 400 | Inter |
| Small, and the product count | `13px` | `18px` | 400 | Inter |
| Marquee | `13px` | `18px` | 700 | Inter |
| Rating stars | `14px` | `14px` | - | glyph |

The hero overlay is `56px` below the phone width and `80px` on a tablet. Product titles are lowercase in all copy, consistently; it is a deliberate voice, not an accident of import.

### Radius, border, elevation and the grid

Pills and the search field are fully rounded; cards and images are softly rounded; inputs a little less; badges least of all. Borders are one hairline in the hairline colour. Elevation is used on the cart drawer, the sticky footer bar and the messaging control only, and nowhere else.

The content column has a generous maximum width with a comfortable gutter that tightens on a phone. Product shelves are horizontally scrolling rows that bleed past the column on both sides, with scrolling that snaps per card, which is what makes the home page feel like a shop rather than a brochure.

### Iconography

**The mark.** A stylised letterform, a single closed path suggesting a stroke rising to the right with a notch cut out of it, reversed out of the header and filled with the current text colour. On a `0 0 64 40` coordinate box its path is `M2 38 26 4a6 6 0 0 1 9.6 0L62 38H47L30 14 20 28h10l7 10Z`.

**Interface glyphs**, drawn as inline vector shapes on a twenty four unit grid with a light stroke, round caps and round joins:

| Glyph | Construction |
|---|---|
| Search | a circle and a short diagonal handle leaving it toward the lower right |
| Bag | a rounded rectangle with an arc handle peaking above it |
| Account | a small circle head over a wide arc of shoulders |
| Chevron left, right | a single angle pointing each way |
| Star, filled | the five point star, used for ratings |
| Truck | a cab, a box behind it, and two wheels |
| Return | a circular arrow of most of a turn with a head at its start |
| Shield | a shield outline pointed at the foot |
| Plus, minus | a cross and a bar, for quantity controls |

**Payment and channel marks.** The footer carries payment marks and the floating control carries the messaging channel mark; each uses its scheme's own published geometry.

**The rating display.** Five stars with the filled fraction clipped rather than rounded, the numeric average to one decimal beside them, and the review count after it. A half star is a clip, never a separate glyph, so a rating of four point three renders as four point three.

### The home page as a sequence

| Band | Contents |
|---|---|
| Marquee | three threshold offers, cycling |
| Header | department tabs, wordmark, search, account, bag |
| Hero carousel | full bleed slides with a display type overlay |
| Shop by category | a horizontally scrolling row of category tiles under `SHOP BY CATEGORY.` |
| Product shelves | several, each a heading and a horizontal row of product cards |
| Video reels | a row of short vertical videos; with no reels in the fixtures the shelf renders its empty state |
| Trust band | delivery, returns and support assurances |
| Footer | link columns, a newsletter field, payment marks, a messaging channel control and the legal row |

### Global chrome

**The marquee.** At the very top, above everything, full width, on a near-black neutral ground with near-white text, running three offers separated by an emoji either side, repeated to fill the strip and translating continuously with no seam, because its content is drawn twice. It pauses on hover. Under a reduced motion preference it becomes a static row that steps to the next offer every six seconds. The offers are content, not markup: they come from the active promotion list, so a merchandiser changes them without a deployment.

**The header.** Below the marquee and over the hero: a translucent dark ground with a blur behind it, becoming the solid near-black neutral once the hero has scrolled past. Left, the four department tabs `EQUIPMENTS`, `SPORTS SHOES`, `SNEAKERS`, `APPAREL`; centre, the wordmark; right, a fully rounded search field with the placeholder `Search For Apparels`, an account glyph and a bag glyph with a count badge.

**The department menu.** Hovering a department opens a full width panel holding, per sub-category, a heading and a row of two to four product cards, each with image, lowercase title, selling price and struck through original, and a `View More` link at the end of the row. Under `EQUIPMENTS` the sub-categories are `PULL UP BAR`, `RESISTANCE BANDS`, `MASSAGERS` and `YOGA`. The menu renders real products with live prices and stock, not a static list. It is merchandised: each sub-category names an ordered product set, falling back to best sellers when unset.

**The cart drawer.** Opens from the bag glyph, sliding over from the right, full height, over a scrim. It holds the lines with image, title, variant, a quantity stepper and the line total, then any gift lines marked free; a threshold progress meter; a subtotal; and a primary action. The drawer is the primary bag surface, and the meter reads the same promotion list as the marquee, showing how far the bag is from the next threshold with copy such as `Add 320 more for a free gift`.

**The floating controls.** A messaging channel control at the lower right on the messaging green, and a promotional prompt with a countdown. Both are dismissible, and a dismissal is remembered for the session.

**The footer.** Link columns, a newsletter field, payment marks, and the legal row. Every footer links the privacy page.

### Motion

**The hero carousel.** Full bleed slides, each a picture with display type overlaid, advancing every six seconds and by two chevron controls at the vertical centre, with a dot indicator at the lower right. It pauses on hover and on focus within. A slide leaves horizontally on the house curve. The overlay is the heavy display family at the hero size, with one word sitting on a solid block of the amber accent behind it. **The carousel stops permanently once a visitor uses a control**; auto-advance resuming after an interaction is the most disliked behaviour a carousel has.

**The four curves that carry the site**, as characters rather than values: the house curve, which leaves fast and settles long, for slides, drawers and panels; a symmetric standard curve for hovers and colour changes; a decelerate for entrances; and a longer decelerate for the drawer. The many other curves the reference declares, most used once, are not reproduced.

**The named moments worth keeping:** the marquee translating by its own content width; a panel sliding in from the bottom with a fade; a panel sliding in from the top with a fade; and `swipeHintBounce`, a small vertical bounce that tells a shopper a shelf scrolls sideways. Without that hint a horizontally scrolling row on a desktop looks like a truncated grid. The reference's hundred and one keyframe sets are mostly duplicates under obfuscated names and are not reproduced.

**The promotional prompt.** It rises into view, breathes a soft ring shadow outward in a light, muted orange, pings once in a second colour, and runs a countdown bar that shrinks from full width to nothing; it can be dismissed with a small pop and its button glows gently. **The countdown reflects a real promotion expiry, the same for every visitor, and it survives a reload.** A countdown that resets on reload is a dark pattern and the build has no way to make one.

**Reduced motion.** With the preference set the marquee becomes a stepped cycle, the carousel does not auto-advance, the swipe hint does not bounce, the promotional prompt appears without its ring and keeps its countdown as a static figure, and drawers open without travel.

### Collection

The composition is a banner, a sticky filter and sort bar, a product grid and pagination.

| Element | Specification |
|---|---|
| Banner | a full bleed picture with the collection name in the heavy display family, uppercase |
| Count | `<n> products` in the caption colour |
| Filter bar | sticky under the header, holding the filter control, the sort select and the active filter chips |
| Grid | four columns on a desktop, three on a tablet, two on a phone and below it |
| Pagination | more cards arrive on scroll, with a `Load more` control after the third page |

Two columns on a phone rather than one is correct for this catalogue: the products are visually distinct enough to be recognised small, and one column doubles the scroll.

**Filters.** Sub-category, multiple; price, a range with the catalogue's own bounds; size, multiple, only on shoes and apparel; colour, multiple, as swatches; rating, four and above or three and above; availability, in stock only; discount, above `30%` or above `50%`. The discount filter exists because every product carries a discount, which makes discount depth a real shopping axis. Filter state lives in the address, so a filtered view is shareable and survives a reload and the back button, and the count updates before the grid does.

**Sort.** `Featured`, `Price low to high`, `Price high to low`, `Newest`, `Best selling`, `Rating`. `Featured` is merchandised per collection and is the default.

**The product card**, the most repeated component:

| Element | Specification |
|---|---|
| Image | square, softly rounded, loading lazily below the fold, with a second image swapped in on hover |
| Badges | at the image's top left, stacked: a discount badge on the saving ground in the saving green, and where applicable `NEW` or `LOW STOCK` |
| Title | lowercase, clamped to two lines |
| Rating | the clipped stars, hidden when the review count is zero rather than showing an empty row |
| Price row | the selling price, the original struck through, and the saving as a percentage |
| Variant chips | up to four colour swatches, with a count for the remainder |
| Action | `Add to cart` on hover on a desktop, always visible on touch |

**The card never reflows when its badges or rating appear:** the badge row and the rating row hold their height whether occupied or not, because a grid that jitters as images load is the most common defect on a storefront like this. When variant prices differ the price reads `from` the lowest.

**States.** Loading is a skeleton grid of the same shape, never a spinner. Empty reads `Nothing here yet`, `Try removing a filter.`, with the action `Clear filters`. An error is an inline card with a retry that repeats the same query. An out of stock product stays listed, greyed, with `Notify me` replacing the action; hiding it loses the demand signal the fit and stock features depend on.

### Product

The composition is two columns on a desktop, a gallery and a buy column; below the desktop width the gallery is full width, the buy column follows, and a sticky action bar carrying the price and `Add to cart` appears at the foot once the column's own button scrolls out of view.

**The gallery.** Images and short videos in one media list, a large viewer with pinch and wheel zoom, thumbnails down the left on a desktop and a swipe strip with dots on a phone. Media is per variant: choosing a colour changes the gallery.

**The buy column.**

| Element | Specification |
|---|---|
| Title | lowercase |
| Rating | stars, average, and a link to the reviews |
| Price block | selling price, original struck through, saving percentage in the saving green, and the tax line beneath in the caption colour |
| Variant selectors | colour as swatches, size as chips, each showing unavailable combinations as struck through rather than hidden, disabled with a reason |
| Size guidance | a control opening the product family's size table |
| Quantity | a stepper from `1` to the per-order limit of `5` |
| Primary action | `Add to cart`, full width |
| Secondary action | `Buy now`, going straight to checkout with this item alone |
| Delivery check | a postal code field returning an estimated delivery date and whether payment on delivery is available there |
| Assurances | the returns window, the warranty, and payment on delivery availability, each with its glyph |

The delivery check matters most in this market: a shopper who cannot find out whether a parcel reaches their postal code, and whether they can pay on arrival, does not buy. It is a first class element of the buy column, not a link to a policy page. It reads `Delivering to 560001 by Thursday, 12 March` in that shape, then `Cash on delivery available here` or `This postal code is prepaid only.`

**Below the fold.** Description, specification table, what is in the box, an assembly or usage section for equipment, reviews with photographs and a rating histogram, questions and answers, and two shelves: frequently bought together, and similar products.

**Size and fit.** For shoes and apparel: a size table per product family with the brand's own measurements, a conversion row, and a fit note.

**Reviews.** A rating histogram, filters by star and by whether a review has a photograph, sorting by recency and by helpfulness, and a verified purchase mark. Reviews belong to the product family rather than the variant, and each review names the variant it was written for.

### Search

A search field in the header opens a panel with recent searches and, after two characters, suggestions: products with thumbnail and price, then collections, then query completions, in that order. Results use the collection grid with the same filters. Zero results read `Nothing matched "<query>"`, offer a spelling suggestion where one exists, and show a shelf of best sellers. A maintained synonym list serves this catalogue's specific vocabulary. Searching from inside a department searches within it first and says so, with a control to search everything; the placeholder naming a department is that scope.

### Information pages

Delivery, returns and refunds, warranty, terms, privacy, contact and about, each one reading column with a last updated line, at `/pages/delivery`, `/pages/returns`, `/pages/warranty`, `/pages/terms`, `/pages/privacy`, `/pages/contact` and `/pages/about`. The returns page states, in this order and above any prose: the seven day window, what is excluded, who pays return shipping, and how long a refund takes.

### The account area

| Screen | Contents |
|---|---|
| Orders | a list with state, date, total and thumbnails, and the action the state permits: track, cancel, return, or reorder |
| One order | items with prices as paid, the address, the payment method, the tracking timeline as a vertical list of carrier events with timestamps, the invoice, and the actions the state permits |
| Addresses | a list with a default, each checked against the postal code table |
| Returns | open and past returns with their state |
| Wishlist | saved products with a price drop notice |
| Notifications | channel preferences |
| Profile | name, phone, email, date of birth for offers |
| Size profile | editable, with what it is based on and a control to clear it |

Reorder is one action adding every still available line to the bag at current prices and naming what changed or is gone.

### The goal kit builder screen

At `/build`: three questions, then the kit. One card per slot with its role, the chosen product, its price, a swap control offering the other candidates, and a remove control on optional slots; a running total against the budget, the bundle saving, and one action adding the whole kit to the bag. A kit in the bag is one line with its components listed beneath, expandable. Removing a component breaks the kit into its parts at individual prices, and the bag says so before it happens.

### The merchant console

At `/merchant`: orders by state, the confirmation queue with each order's band and contributing signals, the refusal dashboard by postal code, by product and by band, the catalogue with price and stock, review moderation, and the promotion, shelf, menu, hero and badge schedule with a start, an end and a preview.

### Copy

| Element | Copy |
|---|---|
| Skip link | `Skip to content` |
| Departments | `EQUIPMENTS`, `SPORTS SHOES`, `SNEAKERS`, `APPAREL` |
| Search placeholder | `Search For Apparels` |
| Menu sub-categories | `PULL UP BAR`, `RESISTANCE BANDS`, `MASSAGERS`, `YOGA` |
| Menu action | `View More` |
| Home heading | `SHOP BY CATEGORY.` |
| Price saving | `You save 43%` in that shape |
| Low stock | `Only 3 left` in that shape |
| Out of stock | `Sold out` and `Notify me` |
| Add to cart confirmation | `Added to your bag` |
| Checkout verification | `We sent a 6-digit code to <phone>.` |
| Fit question | `How did it fit?` with `Too small`, `Just right`, `Too large` |
| Fit recommendation | `Most people your size take a 9 in this.` in that shape |
| Kit shortfall | `We could not fill the <role> slot within your budget. Raise it by <amount> or remove the slot.` |
| Not found | `404`, `That page does not exist.`, a search field and the best sellers |
| Stock changed at checkout | `<title> just sold out. Remove it to continue.` |
| Price changed at checkout | `Prices changed while you were shopping. Here is what is different.` |
| Payment failed | `That payment did not go through. Your bag is exactly as you left it.` |
| Code did not arrive | `Not received? Resend in 30s` then `Call me with the code` |
| Generic | `That did not work. Try again.` with a retry |

Nothing says error; it says what happened and what to do, and every message about money states the exact amount.

### Visual fidelity

The visual outcomes this specification adds up to: a strip at the very top scrolling three offers continuously and pausing when pointed at; a header translucent over the opening picture and solid once scrolled past; a department tab opening a panel of real products with pictures and current prices; every price anywhere showing the selling price, the struck-through original and the percentage saved; lowercase product titles; heavy display headings over plain product names; a carousel that advances every six seconds and stops for good once a control is used; shelves that scroll sideways with a bouncing hint; cards that never shift as images, badges and ratings load; the bag opening as a drawer from the right showing how far it is from the next offer; and, with reduced motion set, a stepping strip and a still carousel.

### The zero-asset substitution guide

What is being replaced: the wordmark files, product and hero photography, category tile images, video reels, the payment and channel mark files, and font files. The build ships no image file of its own. Product photography is content that a merchant uploads; everything the fixtures need is generated deterministically from the handle, so the same product always gets the same picture:

| Slot | Construction |
|---|---|
| Product image | a square on the warm off-white, a large soft radial in a palette colour chosen by hashing the handle at low alpha, a geometric silhouette from the sub-category's glyph in the secondary text colour, and the product's initials in the heavy display family at the lower left in the disabled colour |
| Second image | the same seed rotated a little with the radial moved, so the hover swap has something to swap to |
| Hero slide | a full bleed gradient between two palette colours at a seeded angle, a fine desaturated grain overlay, and the display overlay |
| Category tile | the sub-category glyph centred on a palette tinted ground |
| Review avatar | initials on a hash chosen ground |

Video reels are omitted from fixtures and their shelf renders its empty state. The wordmark, payment marks and fonts are geometry or stacks, never files. Invoices, credit notes and return labels are generated from the order record when requested, never stored as rendered files, so a document cannot disagree with the order it describes.

## Technical requirements

### The stack

The backend is **Litestar** on Python 3.12. The frontend is **Angular**, served as a production build. The rendering model is a **single page application over a JSON API**: the browser receives an application shell on first paint, and every route after that is painted from JSON the API returns. The one exception is the document head: every public route's HTML is served with its own title, description and social preview tags already in it, so a link unfurls without running script.

There is no separate asset host: the app serves its own scripts, styles and generated images. The shipping aggregator is the carrier behind the signed carrier events, the logistics side of the shop. No third-party analytics identifier is used; page views are recorded by the app itself.

Persistent state lives in **PostgreSQL** (`postgres`), reached through `DATABASE_URL`. Invoices live in **Kill Bill** (`killbill`), reached through `PAYMENTS_API_URL` with `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`, `PAYMENTS_API_USER` and `PAYMENTS_API_PASSWORD`. Email is sent over real SMTP to **Mailpit** (`mailpit`) at `SMTP_HOST` and `SMTP_PORT`, authenticating with `SMTP_USER` and `SMTP_PASS`. The carrier signs its events with `CARRIER_WEBHOOK_SECRET`. A bag hold lasts fifteen minutes; its length in seconds is read from `CART_HOLD_SECONDS`, which this environment sets to `45`, and `900` applies when it is unset. The app reads its own address from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host, a port or a secret.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are `postgres`, `mailpit` and `killbill`, and reaching for anything else is a contract violation.

### Kill Bill, the invoice record

The storefront has its own Kill Bill user, already provisioned with account and invoice permissions and nothing more. Every call to `/1.0/kb/*` carries that user's HTTP Basic credentials, the `X-Killbill-ApiKey` and `X-Killbill-ApiSecret` headers, and `X-Killbill-CreatedBy` on every write.

- `GET /1.0/healthcheck` is unauthenticated liveness.
- `GET /1.0/kb/accounts?externalKey={externalKey}` finds an account: `200` when it exists, `404` when not.
- `POST /1.0/kb/accounts` with `{"name", "externalKey", "email", "currency", "country"}` creates one; a second create with a used external key is refused with `409`, so the external key, not an application check, keeps one account per phone.
- `POST /1.0/kb/invoices/charges/{accountId}?autoCommit=true` with a list of `{"amount", "currency", "description"}` items creates one committed invoice carrying them.
- `GET /1.0/kb/invoices/{invoiceId}?withItems=true` reads an invoice back with its `amount`, `currency` and items.

Kill Bill reports amounts as decimal rupees, `1020.00`, and currency in upper case, `INR`. A customer's account has the external key `peakfit-` followed by the ten digit phone, the currency `INR` and the country `IN`. Every invoice this storefront creates carries exactly one item whose description begins `Order ` followed by the order number, as in `Order PF-100021 cash collected on delivery`.

| Payment method | Invoices, and when |
|---|---|
| `prepaid` | one, for `total_minor`, when the order is placed |
| `on_delivery` | one, for `total_minor`, when the order becomes `delivered`; none if it is cancelled, refused or never delivered |
| `partial_advance` | one for `advance_minor` when placed, and one for `amount_due_on_delivery_minor` when it becomes `delivered` |

A placement replayed, a delivered event reported twice, or two requests arriving together never produce a second invoice for the same payment.

### Mail

Every message goes over SMTP to Mailpit, one message per recipient, no cc and no bcc. In this build the message channel of the product is email: everything the product sends "by message" arrives as an email to the email on the order or on file.

| When | To | Subject | First line of the body |
|---|---|---|---|
| a sign in or checkout code is requested | the email on file for the phone, or for a phone never seen, the email given with the request | `Your Peakfit code` | the six digits alone |
| an order is placed | the order's email | `Peakfit order <number> placed` | for cash on delivery and partial advance, `Order <number> placed. Have <amount> ready for the courier.`; for prepaid, `Order <number> placed. It is paid in full.` |
| a medium or low band order needs confirming | the order's email | `Please confirm Peakfit order <number>` | `Please confirm your order <number> for <amount>, arriving <date>. Reply YES to confirm or NO to cancel.` |
| an order is out for delivery | the order's email | `Peakfit order <number> arrives today` | `Your order arrives today between <window>. Amount due: <amount>.` |
| a low band order is cancelled unconfirmed | the order's email | `Peakfit order <number> cancelled` | `We could not confirm order <number>, so we have cancelled it. You can order again and pay in advance, and it will ship straight away.` |
| a return is requested | the order's email | `Peakfit return for order <number>` | `We will collect it within 3 working days. Your refund arrives 5 to 7 days after it reaches us.` |

`<amount>` is written as the rupee sign and whole rupees with Indian digit grouping, and paise only when they are not zero: `₹4,078`, `₹1,23,450`, `₹559.80`. `<date>` is written `Thursday, 12 March`. The confirmation message stays under `160` characters, names the shop, states the amount and the date, and implies no suspicion. The email for a confirmation carries a confirm link and a cancel link in place of the two replies.

The notification table, with email standing for the message column:

| Event | Message | Email | In-app | Suppressible |
|---|---|---|---|---|
| Order placed | yes | yes | yes | no |
| Verification code | yes | no | no | no |
| Order confirmed | yes | yes | yes | no |
| Shipped, with tracking | yes | yes | yes | no |
| Out for delivery, with the amount due | yes | no | yes | no |
| Delivered | yes | yes | yes | no |
| Refused or undelivered | yes | yes | yes | no |
| Return received and refunded | yes | yes | yes | no |
| Back in stock | yes | yes | yes | yes |
| Price drop on a saved product | yes | yes | yes | yes |
| Cart reminder | yes | yes | no | yes |
| Promotional | yes | yes | no | yes |

The unsuppressible rows all concern an order the shopper placed. The rest is marketing and obeys consent per channel, collected explicitly, never bundled into the order action, and revocable from the message itself.

### Accounts and codes

Identity is a verified ten digit phone. Email is optional for receipts and becomes required only because codes travel by email in this build. There is no password anywhere. A federated sign in may be offered, mapped to a verified phone on the first order.

- `POST /api/auth/code` with `{"phone", "email"}` answers `202` with `{}` and sends a six digit code. A phone that is not ten digits is refused with `422` and `invalid_phone`. For a phone that already has an email on file, **the code goes to the email on file and never to the email in the request.** For a phone never seen, `email` is required, refused with `422` and `email_required` when missing, and the code goes there.
- A code is valid for ten minutes, is used once, and belongs to the phone it was sent for: presented with any other phone it is refused. Five wrong codes for a phone void its current code.
- A second code request for the same phone inside thirty seconds of the last is refused with `429` and `resend_too_soon`, the error object carrying `retry_after_seconds` as a whole number from `1` to `30`.
- `POST /api/auth/verify` with `{"phone", "code"}` answers `200` with `{"token", "customer"}`, the customer as `{"id", "phone", "email", "name", "role"}`. A wrong, expired, used or other phone's code is refused with `401` and `invalid_code`. The token is presented as `Authorization: Bearer <token>`. Verifying a phone that placed guest orders claims those orders: they appear in that customer's order list from then on.

**Guest checkout.** A shopper may complete an order with a phone, an email and an address and no account. A customer record is created silently, unverified, and is claimed the first time that phone verifies a code. Forcing account creation before a first purchase is the single most expensive requirement a storefront can impose.

### The catalogue, stock and prices

A product is the family (title, description, media, specification, size table, reviews); a variant is the buyable thing (colour, size, weight or length), each with its own price, stock and SKU; a collection is a merchandised set, manual or rule based; a kit is a set sold as one line. **Every price and every stock figure lives on the variant.**

**Stock.** `on_hand` is physical units. A variant's `available` is `on_hand` less the units held in live bags, is computed rather than stored, and never goes below zero. Adding a line to a bag, or changing its quantity, holds those units until `reservation_expires_at`, which is the moment of the bag's last change plus `CART_HOLD_SECONDS`. From that instant the units are available again, exactly once, and the bag keeps its lines without holding them: placed after that, it can buy only what is available at that moment, never a unit another live bag now holds. Placing an order turns its holds into sold stock: `on_hand` falls by the quantities ordered. A merchant recount may set `on_hand` below what bags hold; placements then take stock in the order they are placed, and the rest are refused.

A request to hold more than is available is refused with `409` and `insufficient_stock`, carrying `available`. When two bags ask for the last unit at the same moment, exactly one holds it and the other is refused; when two placements would together need more than `on_hand`, exactly one succeeds and the stock left is what the winner did not take. Overselling here is worse than in a prepaid market, because the cancellation arrives after the courier has left.

**Badges.** A variant carries `LOW STOCK` when it is not backorderable and `available` is above zero and at or below its `low_threshold`; `SOLD OUT` when `available` is zero and it is not backorderable; `NEW` for a product created within thirty days. A low stock badge is never a fixed message, never randomised, and never shown on a backorderable variant.

**Pricing and the struck-through original.** `price_minor` is what the shopper pays, tax inclusive. Every price change is recorded in the variant's price history with the moment it took effect. **`compare_at_minor` is derived from that history, never typed:** it is the highest price the variant carried at any moment in the ninety days before now, when that is higher than the current price, and absent otherwise. A merchant request carrying `compare_at_minor` is refused with `422` and `compare_at_not_settable` and changes nothing. `saving_percent` is `(compare_at_minor - price_minor) * 100 / compare_at_minor` rounded down to a whole number, and absent when there is no compare price. `cost` is recorded for margin reporting and never exposed. A struck through price that never existed is a legal problem as well as a dishonest one.

| Price history of one variant, oldest first | `compare_at_minor` | `saving_percent` |
|---|---|---|
| created at `299900` | absent | absent |
| then `199900` | `299900` | `33` |
| then `249900` | `299900` | `16` |
| then `349900` | absent | absent |
| then `249900` | `349900` | `28` |

**Rendering never shows a stale figure.** A collection or product page shows the price and stock as they are at the moment of the request; the cart, the checkout and the account are never cached anywhere.

### The bag

A bag belongs to a device and, once the shopper signs in, to the account; the two merge on claim **by summing quantities, never by replacing**, each merged line capped at the per-order limit and at what is available.

A line records the variant, the quantity, `unit_price_at_add_minor` and the `current_price_minor`. When the two differ the line carries `price_changed` and shows `The price of this item changed from 1,899 to 1,999.` in that shape, at the line, rather than folding the change silently into the total. A shopper who sees a total change without explanation abandons.

**Promotions**, from the active promotion list that feeds the marquee and the meter:

| Key | Kind | Rule |
|---|---|---|
| `free-gift-1999` | threshold gift | a merchandise subtotal of `199900` or more adds one `PF-GIFT-SHAKER` at no charge |
| `flat-200-2999` | threshold discount | a merchandise subtotal of `299900` or more takes `20000` off |
| `flat-500-4999` | threshold discount | a merchandise subtotal of `499900` or more takes `50000` off |
| `STRIDE10` | code | ten per cent off the lines in `SPORTS SHOES` and `APPAREL`, rounded down to the paisa |

**Precedence, exactly.** The merchandise subtotal is the sum of quantity times current price over every line except gift lines, before any discount. Thresholds are measured against that subtotal and nothing else, so a code never lowers a bag below a threshold it reached. The two threshold discounts never stack: only the highest reached applies. The gift stacks with either. A code applies to its eligible lines and stacks with the threshold discount; once applied it stays on the bag through later changes. `discount_minor` is the code amount plus the threshold amount. The bag shows which promotions applied and, for the lowest threshold above the subtotal, how far away it is as `remaining_minor`. Shipping is free when the merchandise subtotal is `99900` or more and `9900` otherwise. `total_minor` is the merchandise subtotal less the discount plus shipping. `tax_minor` is the tax already inside the total at eighteen per cent: `total_minor * 18 / 118` rounded half up.

| Bag | Subtotal | Applied | Discount | Shipping | Total | Next |
|---|---|---|---|---|---|---|
| one line at `199800` | `199800` | none | `0` | `0` | `199800` | `free-gift-1999`, `100` away |
| two lines at `279900`, code `STRIDE10`, both in `SPORTS SHOES` | `559800` | gift, `STRIDE10` `55980`, `flat-500-4999` `50000` | `105980` | `0` | `453820` | none |
| one shoe line at `279900` and one band at `29900`, code `STRIDE10` | `309800` | gift, `STRIDE10` `27990`, `flat-200-2999` `20000` | `47990` | `0` | `261810` | `flat-500-4999`, `190100` away |

A code that applies to no line of the bag is refused with `422` and `not_applicable`. Silent non-application of a promotion a shopper believes they qualified for is the main cause of checkout support contacts.

**Splitting a discount across lines, to the paisa.** Each discount is allocated separately across the lines it applies to: a threshold discount across every merchandise line, a code across its eligible lines. Each line first receives its share in proportion to its line total, rounded down to the paisa; the paise left over go one at a time to the lines with the largest fraction discarded, ties to the earlier line. A line's `allocated_discount_minor` is the sum of its shares, and its `paid_minor` is its line total less that. The allocations of a discount always add up to the discount exactly.

| Lines, in order | Line totals | `flat-200-2999` shares |
|---|---|---|
| A, B, C | `100000`, `100000`, `100000` | `6667`, `6667`, `6666` |

### Checkout and placement

One page, three steps, no account required: contact (phone, email), delivery (name, address with postal code, landmark, and the delivery estimate), and payment (prepaid methods, and payment on delivery where the postal code, the bag and the band permit). A prepaid method in this build is recorded as paid when the order is placed; there is no card form.

**The postal code table** decides delivery:

| Postal code | Deliverable | Cash on delivery | Days to deliver | Refusal history |
|---|---|---|---|---|
| `560001` | yes | yes | `3` | ordinary |
| `400050` | yes | yes | `4` | high |
| `110001` | yes | no | `5` | ordinary |
| `799001` | no | no | - | - |

`GET /api/delivery-check?postal_code=<code>&sku=<sku>` answers `{"postal_code", "serviceable", "estimated_delivery_date", "cod_available"}`, where the date is today in UTC plus the days, as `YYYY-MM-DD`, and `cod_available` also accounts for the variant's product.

**Payment on delivery**, the market defining path, is available only when all hold, and each is re-checked at placement: the postal code allows it; the order total is at most `999900`; no line's product is marked not eligible (the `kinetra vibration plate` is not); and the delivery confidence band is not blocked. When one fails, placement answers `422` with `cod_unavailable` and a `reason` of `postal_code`, `cart_value`, `product` or `delivery_confidence`, and the same bag placed as prepaid is accepted. The phone of a cash on delivery order is verified by a code before the order is accepted, unless the order comes from a signed in customer placing it with their own verified phone. A cash on delivery order whose total is above `499900` becomes `partial_advance`: an advance of twenty per cent of the total, rounded up to the whole rupee, is paid at placement, and the rest is due to the courier. For a total of `509800` the advance is `102000` and `407800` is due on delivery. The confirmation screen and the placed email state the amount due once.

**Placement is one step.** `POST /api/orders` validates stock against holds, recomputes every price and promotion on the server, creates the order, turns holds into sold stock, and records the payment or the amount due, all together or not at all. A new order answers `201` with the order. The request carries an `Idempotency-Key` header, required, and a body of `{"cart_token", "contact": {"name", "phone", "email"}, "address": {"name", "line1", "landmark", "city", "postal_code"}, "payment_method", "expected_total_minor", "verification_code"}`, where a signed in customer may send `"address_id"` in place of `"address"`, `payment_method` is `prepaid` or `on_delivery`, and `verification_code` is needed only for payment on delivery.

- **The client's total is never trusted.** When a line's current price differs from its price at add, or `expected_total_minor` differs from the total the server computes, placement answers `409` with `price_changed`, carrying `changes` as `{"sku", "old_minor", "new_minor"}` and the server's `total_minor`, and creates nothing. That answer counts as showing the shopper the difference: each line's price at add becomes its current price, so placing again with the new total succeeds.
- When a line can no longer be sold, placement answers `409` with `stock_changed`, carrying `lines` as `{"sku", "title", "available"}`, creates nothing and takes no stock.
- The same `Idempotency-Key` with the same body returns the same order with `200` and creates nothing more: no second order, no second invoice, no second email, no second hold taken. Two such requests arriving at the same moment make exactly one order. The same key with a different body is refused with `409` and `idempotency_key_reused`. A bag that has become an order is closed, and placing it again under a new key is refused with `409` and `cart_closed`.
- A missing code for payment on delivery is refused with `422` and `verification_required`; a wrong, expired, used or other phone's code with `422` and `invalid_code`. Neither creates an order or holds stock beyond what the bag already held.
- **The order's address is a copy, never a reference.** Editing a saved address afterwards never changes where a past order was sent.

| Case | Behaviour |
|---|---|
| A line went out of stock | the order stops, names the line, and offers to remove it and continue |
| A price changed | the order stops and shows the difference for confirmation |
| Payment failed | the bag is kept exactly and the failure is stated in plain words |
| The code did not arrive | a resend after thirty seconds, and a voice call offered after two failures |

### Delivery confidence

A proposal the PRD adds, pinned here so that it behaves the same everywhere. Every cash on delivery or partial advance order is given a band at placement from signals the shop already holds; prepaid orders are not banded and are `confirmed` at once. The history counted is every order of the last twelve months on the same phone or to the same normalised address, where the normalised address is the address line and postal code lowercased with runs of spaces and punctuation collapsed, unit included.

| Band | When | Response |
|---|---|---|
| `blocked` | two or more of those orders reached `refused` or `undelivered` | payment on delivery is not offered; prepaid is, with the reason in plain words |
| `low` | exactly one reached `refused` or `undelivered`; or three or more orders went to the same address in the last twenty four hours and fewer than three orders there were delivered | placed, and confirmation is required before packing; unanswered after forty eight hours it is cancelled with a message saying why and inviting a prepaid order |
| `high` | two or more reached `delivered`, and the postal code's refusal history is ordinary | placed and `confirmed` immediately |
| `medium` | anything else, including two delivered orders in a postal code with high refusal history | placed, and confirmation is requested; unanswered after twelve hours it ships anyway |

An order that reached `delivered` counts as delivered even if part of it was later returned. **Postal refusal history alone never makes a band lower than `medium`**, because that is punishing somebody for their neighbours. The signals are `verified_phone`, `delivered_history`, `refusal_history`, `address_completeness`, `postal_refusal_rate`, `order_value_above_history`, `address_velocity` and `account_age`. The rules:

- No order is ever silently cancelled; every cancellation carries a reason and an alternative.
- The reason shown to a shopper is honest and specific and never implies dishonesty.
- A shopper can always reach the prepaid path, at every band.
- **No numeric score exists in any response.** A customer never sees a band or a signal. The merchant sees the band and the contributing signals, never a number.
- A refusal's effect decays: only the last twelve months count.
- A shopper who confirms and then still refuses has the confirmation recorded and weighed in the next order's signals. When mail is unavailable, medium orders ship after the timeout and low band orders move to a phone call queue rather than cancelling. A merchant override in either direction records a reason and is excluded from any evaluation of the bands.

The merchant surface is the confirmation queue, a manual override in both directions with a reason, and the refusal dashboard. A low band order cannot be packed until it is confirmed: `packed` is refused with `409` and `confirmation_required`.

Acceptance criteria for delivery confidence:

- An order from a number with two delivered orders is confirmed immediately.
- A first order from a high refusal postal code is never placed in the low band on that signal alone.
- A low band order unanswered for forty eight hours is cancelled with a plain language reason and an invitation to pay in advance.
- The prepaid path is available at every band, including blocked.
- No score is shown to a shopper or to support; support sees the band and the signals.
- A refusal's effect on an address decays over twelve months.
- Every automatic cancellation appears in the merchant queue with its reason.

### The order lifecycle

| State | Meaning |
|---|---|
| `placed` | accepted, stock sold |
| `confirmed` | verified, at once for prepaid and high band, otherwise by confirmation |
| `packed` | picked and packed |
| `shipped` | handed to the carrier, tracking issued |
| `out_for_delivery` | on the vehicle |
| `delivered` | received, and paid if on delivery |
| `refused` | the customer declined it at the door |
| `undelivered` | attempts exhausted |
| `returning` | on its way back |
| `returned_to_origin` | back in the warehouse |
| `cancelled` | before dispatch |
| `return_requested`, `return_picked`, `refunded` | the returns path after delivery |

`refused` and `returned_to_origin` are separate states with separate costs and separate follow up; a build that collapses them into `cancelled` cannot measure what delivery confidence exists to reduce.

| From | To | Fired by |
|---|---|---|
| `placed` | `confirmed` | confirmation, or a merchant override |
| `placed` or `confirmed` | `cancelled` | the customer before packing, or the merchant with a reason |
| `confirmed` | `packed` | the merchant |
| `packed` | `shipped` | the carrier's first scan |
| `shipped` | `out_for_delivery` | a carrier event |
| `out_for_delivery` | `delivered`, `refused`, `undelivered`, or a further attempt | a carrier event |
| `refused` or `undelivered` | `returning` | the carrier |
| `returning` | `returned_to_origin` | receipt at the warehouse, stock restored |

**Carrier events.** `POST /api/webhooks/carrier` takes `{"event_id", "order_number", "status", "occurred_at", "window"}`, where `status` is one of `shipped`, `out_for_delivery`, `delivered`, `refused`, `undelivered`, `returning`, `returned_to_origin`, and `window` is present on `out_for_delivery`. It is signed: the `X-Carrier-Signature` header reads `t=<unix seconds>,v1=<lowercase hex HMAC-SHA256>`, computed with `CARRIER_WEBHOOK_SECRET` over the string `<t>.<raw body>`. An event that is applied answers `204`.

- An event with a missing or wrong signature, or a `t` more than three hundred seconds from now, is refused with `401` and changes nothing.
- An event is applied at most once, by its `event_id`: a repeat answers `204` and changes nothing, not the state, not the timeline, not the stock, not the invoices, not the mail.
- **A state never moves backwards.** An event whose status is at or before the order's current place in the table above answers `204` and changes nothing, with one exception: a new `out_for_delivery` event on an order already out for delivery is a further attempt, added to the timeline with its own out for delivery message. An event that skips ahead to a status the current state cannot reach answers `409` and `illegal_transition`.
- `delivered` sets `delivered_at` to the event's `occurred_at`. `returned_to_origin` puts the order's units back into `on_hand`, exactly once.

A correction that moves a state backwards is a merchant action only, and it is audited. Carrier polling runs hourly as a backstop to the webhook.

**Cancellation.** A customer may cancel their own order in `placed` or `confirmed` with `POST /api/orders/{number}/cancel` and `{"reason"}`, answered `200` with the order; its units return to `on_hand`. From `packed` onward the same request is refused with `409` and `already_packed`, the order is unchanged, and the interface says at the moment of asking that the request is now a return. A merchant cancellation needs a reason, refused with `422` and `reason_required` without one.

**Communication.** Every transition sends its message on the shopper's channel with the tracking link and, for payment on delivery, the amount due. The out for delivery message carries the courier's window and a control to reschedule.

### After the order

**Confirmation.** The full page confirmation at `/orders/<number>/confirmation` shows the order number, the items, the total, the amount due on delivery where it applies, the delivery estimate, and one action to track.

**Tracking without an account.** `GET /api/track?number=<number>&phone_last4=<digits>` answers `{"number", "state", "timeline"}` and nothing else: no address, no name, no phone, no lines, no other orders, where `timeline` is a list of `{"status", "occurred_at"}`. A wrong pair of digits answers exactly as an unknown order number does, `404` with `not_found` and the same message. After five wrong attempts on one order number within fifteen minutes, every attempt on that number, right or wrong, answers `429` with `too_many_attempts` until fifteen minutes after the first wrong attempt. Guest orders are the majority, which is why this exists and why the number is not a key to somebody's address.

**Returns, and requesting one.** `POST /api/returns` with `{"order_number", "line_ids", "reason", "exchange_sku"}` requests a return of whole lines of a delivered order, within seven days of `delivered_at`. The reason is one of `too_small`, `too_large`, `not_as_described`, `damaged`, `changed_mind`, `wrong_item`; anything else is refused with `422` and `invalid_reason`. An order not yet delivered is refused with `422` and `not_delivered`; a request after the window with `422` and `outside_window`, and the interface reads `The 7-day return window for this order closed on <date>.`; a line already in a return with `409` and `already_returned`. Each returned line refunds its own `paid_minor`, never its list price, and a kit line refunds its apportioned price. The return answers `201` with `{"id", "order_number", "state", "reason", "refund_method", "lines", "refund_minor"}` with `lines` as `{"line_id", "refund_minor"}`, state `return_requested`, and `refund_method` of `original` for prepaid orders and `store_credit` for payment on delivery and partial advance orders. The expected duration is stated at the request. The path is `return_requested`, `approved`, `pickup_scheduled`, `picked`, `received`, `inspected`, `refunded` or `rejected`, each with a timestamp and a responsible party.

A size exchange is offered before a refund on shoes and apparel: `exchange_sku`, another size of the same product, holds one unit of that size from the moment of the request until the return is received or the hold ends. Equipment offers no exchange and `exchange_sku` there is refused with `422` and `exchange_not_offered`.

**Reviews.** `POST /api/products/{handle}/reviews` with `{"sku", "rating", "body"}`. Only a customer with an order of that product that reached `delivered` may review it; anyone else is refused with `403` and `not_eligible`. A second review of one product by one customer is refused with `409` and `already_reviewed`. A new review answers `201` with `{"id", "sku", "rating", "body", "state", "verified_purchase"}`; it is `held`, visible to its author, until a merchant publishes it with `POST /api/merchant/reviews/{id}/publish`. The verified purchase mark is derived, never set by hand. A product's `rating_average` and `review_count` count published reviews only, and a merchant never edits a review, only publishes, holds or removes it with a reason. Automatic filtering holds abusive reviews.

### Merchandising

A merchandiser controls collections and their order, the department menu's sub-categories and product sets, the home page shelves, the hero slides, the promotion list that feeds the marquee and the threshold meter, and the badges. Scheduling: every one of those is scheduled with a start, an end and a preview, so a campaign never needs a deployment at midnight.

### The goal kit builder

A proposal the PRD adds. A builder takes a goal, a budget and a space and assembles a kit from the live catalogue, priced as one line with a bundle discount. Kit templates hold slots with a `role` such as `pull`, `press`, `legs`, `mobility`, `recovery` or `flooring`, whether the slot is required, a priority, and a candidate rule selecting eligible variants by sub-category, price band and stock. Assembly:

- take the template for the goal and space, and order its slots by priority;
- for each slot choose the highest rated in stock candidate that fits the remaining budget;
- if a required slot cannot be filled, widen the price band once, then report the shortfall;
- price the kit from live variant prices, apply the bundle rule, and show the saving against buying separately.

The kit is priced when shown and re-priced when added to the bag. A kit's discount is apportioned across its lines at purchase by the same split rule as any other discount, so returning one component refunds what that component actually cost inside the kit. A component going out of stock between building and checkout re-assembles that slot and names the change before checkout. A shortfall is a populated state that names the gap and the budget shortfall. Swapping a component recomputes the total and the saving at once, which may reduce the saving. A bundle discount that would exceed a stacking limit applies the higher discount and shows the other as not applied with the reason. A kit saved and revisited later re-prices and reports every change before anything is added.

Acceptance criteria for the kit builder:

- Three answers produce a complete kit from live, in stock products.
- The kit's price equals the sum of its lines less the stated bundle saving.
- A component going out of stock re-assembles that slot and names the change before checkout.
- Swapping a component recomputes the total and the saving immediately.
- Removing a component from the bag breaks the kit into individually priced lines, with a warning first.
- Returning one line of a kit refunds that line's apportioned price, not its list price.

### Fit confidence

A proposal the PRD adds. A per-shopper size profile and a per-product fit model combine into a size recommendation with a stated confidence, fed by returns and by one question.

- A product family's `runs` (`small`, `true` or `large`, with a magnitude in half sizes) is the most common verdict across its fit feedback, shown only when the sample is `25` or more.
- A shopper's size profile is the size they kept, per category, weighted toward recent orders; kept means delivered and not returned.
- The recommendation is that profile adjusted by the product's `runs` and the shopper's fit preference.
- Confidence is high with three or more kept orders in the category and a sample of `50` or more; medium when one of those holds; low otherwise, and at low no size is recommended and only the size chart shows.
- The recommendation always appears beside the size chart, never instead of it.
- After delivery the delivery message and the order ask `How did it fit?`, answerable in one tap; a size return with `too_small` or `too_large` feeds the model without asking anything extra; a `Not for me` control excludes a line bought for someone else.
- A new shopper is asked nothing; a shopper who returns everything has no inferred profile; a product whose sizing changes follows recent feedback and can be reset; two accounts sharing a household keep separate profiles.
- A sample that is thin but consistent keeps confidence low until the sample floor is met, regardless of how consistent it is.

Acceptance criteria for fit confidence:

- A shopper with no history sees the size chart and no recommendation.
- A product with fewer than `25` fit responses shows no runs small or runs large line.
- A shopper with three kept orders in a category sees a recommendation marked high confidence.
- Answering the fit question takes one tap from the delivery message.
- A size return updates the product's fit model without any extra question.
- The recommendation always appears beside the size chart, never instead of it.

### Merchant surface

Every route under `/api/merchant/` needs a merchant session; a customer session is refused with `403` and `forbidden` and changes nothing.

| Endpoint | Body | Answer |
|---|---|---|
| `POST /api/merchant/products` | `{"handle", "title", "department", "sub_category", "cod_eligible", "variants": [{"sku", "options", "price_minor", "on_hand", "low_threshold", "backorderable"}]}` | `201`, the product as the storefront reads it |
| `PATCH /api/merchant/variants/{sku}` | any of `{"price_minor", "on_hand", "low_threshold", "backorderable"}` | `200`, the variant |
| `POST /api/merchant/collections` | `{"handle", "title", "product_handles"}` | `201` |
| `GET /api/merchant/variants/{sku}` | none | `200` `{"sku", "price_minor", "compare_at_minor", "on_hand", "available", "low_threshold", "backorderable"}` |
| `GET /api/merchant/orders/{number}` | none | `200`, the order plus `band` and `signals`; `band` is null for a prepaid order |
| `POST /api/merchant/orders/{number}/transitions` | `{"to", "reason"}`, `to` one of `confirmed`, `packed`, `cancelled` | `200`, the order |
| `GET /api/merchant/confirmation-queue` | none | `{"items": [{"number", "band", "signals"}]}` for placed orders in `medium` or `low` |
| `POST /api/merchant/reviews/{id}/publish` | none | `200`, the review |

A product created by a merchant starts with each variant's first price in its history and no compare price. `department` carries a department's name as the tabs read it, such as `SPORTS SHOES`, and `sub_category` is a short lowercase handle.

### The storefront surface

| Endpoint | Query or body | Answer |
|---|---|---|
| `GET /api/products` | `department`, `sub_category`, `collection`, `q`, `min_price_minor`, `max_price_minor`, `size`, `colour`, `rating` (`3` or `4`), `in_stock` (`true`), `discount` (`30` or `50`), `sort`, `cursor` | `{"items", "next_cursor", "count"}` |
| `GET /api/products/{handle}` | none | `{"handle", "title", "description", "department", "sub_category", "cod_eligible", "rating_average", "review_count", "variants"}` |
| `GET /api/promotions` | none | `{"items": [{"key", "kind", "threshold_minor", "amount_minor", "ends_at", "message"}]}` |
| `GET /api/delivery-check` | `postal_code`, `sku` | as above |
| `POST /api/carts` | none | `201`, a bag |
| `GET /api/carts/{token}` | none | the bag |
| `POST /api/carts/{token}/lines` | `{"sku", "quantity"}` | the bag; a quantity already in the bag is added to |
| `PATCH /api/carts/{token}/lines/{sku}` | `{"quantity"}`, `0` removes the line | the bag |
| `POST /api/carts/{token}/promotions` | `{"code"}` | the bag |
| `POST /api/carts/{token}/claim` | bearer | the account's bag, with this bag merged into it |
| `GET /api/account/cart` | bearer | the account's bag |
| `POST /api/account/addresses` | `{"name", "line1", "landmark", "city", "postal_code"}` | `201` `{"id", ...}` |
| `PATCH /api/account/addresses/{id}` | any address field | `200` |
| `GET /api/orders` | bearer | `{"items"}`, the customer's own orders |
| `GET /api/orders/{number}` | bearer | the order; another customer's order answers `404` |

A product list item is `{"handle", "title", "department", "sub_category", "price_minor", "compare_at_minor", "saving_percent", "price_from", "rating_average", "review_count", "badges", "in_stock"}`, where the price fields describe the product's lowest priced active variant and `price_from` is true when its variants' prices differ. A variant is `{"sku", "options", "price_minor", "compare_at_minor", "saving_percent", "available", "badges", "backorderable"}`.

A bag is `{"token", "lines", "gift_lines", "merchandise_subtotal_minor", "discounts", "discount_minor", "shipping_minor", "total_minor", "next_promotion", "reservation_expires_at"}`, with `lines` as `{"sku", "title", "quantity", "unit_price_at_add_minor", "current_price_minor", "price_changed", "line_total_minor"}`, `gift_lines` as `{"sku", "quantity"}`, `discounts` as `{"promotion", "amount_minor"}` listing only the code and threshold discounts that take money off, never the gift, and `next_promotion` as `{"promotion", "threshold_minor", "remaining_minor"}` or null.

An order is `{"number", "state", "payment_method", "contact", "address", "lines", "gift_lines", "merchandise_subtotal_minor", "discount_minor", "shipping_minor", "tax_minor", "total_minor", "advance_minor", "amount_due_on_delivery_minor", "placed_at", "delivered_at", "timeline"}`, with `lines` as `{"id", "sku", "title", "quantity", "unit_price_minor", "unit_compare_at_minor", "line_total_minor", "allocated_discount_minor", "paid_minor"}`. Lines keep the order they were added to the bag. `advance_minor` is `0` unless the order is `partial_advance`; `amount_due_on_delivery_minor` is `0` for prepaid. Order numbers read `PF-` and six digits, are issued in increasing order, and are never reused.

**Listing.** Filters apply before paging, so every page carries only matching products and `count` is the number of matching products. A page holds `24` products, walked with `next_cursor` until it is null. Sorts are `featured`, `price_asc`, `price_desc`, `newest`, `best_selling` and `rating`; the price sorts order by `price_minor` and then by handle. The discount filter keeps a product whose `saving_percent` is at or above the value. Out of stock products stay listed with `in_stock` false unless `in_stock=true` is asked for.

### Conventions

- **Money** is an integer in paise with its currency, never a decimal. Every total is stored rather than derived when shown, so a historical order cannot change when a tax rule does.
- **Statuses.** A call that creates answers `201` where this brief says so, an applied carrier event answers `204`, and every other successful call answers `200`.
- **Idempotency** is required on order placement, keyed by the client, and on carrier events, keyed by the carrier's own event identifier.
- **Pagination** walks with a cursor, `24` products to a storefront page.
- **Errors.** Every refusal answers `{"error": {"code", "message", "field"}}`, `field` present only for a problem with one field. No raw exception text reaches anyone.

### The launch surface

- **Not found.** Every unmatched path renders Peakfit's own not-found page, carrying `404`, `That page does not exist.`, a search field and the best sellers, and answers with status `404`. It is never a redirect to the home page. Route resolution runs static routes first, then collections, then products, then pages; then the legacy numeric identifier paths, which resolve to the product or collection carrying that legacy identifier; then a redirect table for retired handles, so a shared link survives a rename; and only then the not-found page.
- **Social preview.** Every public route's HTML declares its own `og:title`, `og:description` and `og:image`, no two routes share a title, and the preview image is served from the app's own origin and resolves.
- **No credential in anything the browser downloads.** No secret key, database address, Kill Bill credential, mail credential or carrier secret appears in any script, style or document the browser receives.
- **Privacy.** A privacy page at `/pages/privacy` is linked from the footer of every page and states what Peakfit records about a customer (phone, email, addresses, orders, returns, reviews, size profile, delivery history) and how long it keeps each.
- **Page views** of public routes are recorded with the route and the instant, readable by the merchant.

### Accessibility and quality

One main heading per route, inside header, main and footer landmarks, the footer being the page's content information landmark. The marquee is decorative and hidden from assistive technology; its offers are also present in the bag's threshold meter, which is not. **Every price block announces itself as one sentence**, carried as its accessible name: `₹1,899, reduced from ₹3,499, saving 45%` in that shape, and the selling price alone when there is no compare price. Variant selectors are grouped and labelled, with unavailable combinations marked disabled with a reason. The carousel exposes its controls, pauses on focus and never traps the keyboard. Focus is a clear ring in the link blue, offset from the control. Every state of an order or of stock is carried as text.

Performance targets on a mid-range phone and a slow connection: the home page's largest paint, the first hero slide, in about two and a half seconds; the first collection page in about one and a half; add to cart confirmed to the shopper at once, ahead of the server's answer; shelf scrolling smooth; the drawer opening at once; a checkout step changing with no full page load. Hero images are served at the rendered size for the width in a modern format with a small placeholder.

**Layering.** Tokens, then primitives (button, field, chip, badge, card, drawer, sheet, stepper, skeleton, empty state, transient message), then commerce components (price block, product card, variant selector, rating, threshold meter, cart line, order timeline), then surfaces. The price block is built first and exactly right, because it appears on the card, the product page, the bag line, the checkout summary and the order.

**Responsive matrix.**

| Surface | Phone | Tablet | Desktop |
|---|---|---|---|
| Header | departments behind a menu control, search as a glyph opening a sheet | departments visible, search inline | full, with the department panels |
| Department menu | a full height sheet with accordions per sub-category, products two to a row | as desktop, narrower | the full product panel |
| Hero | one slide at the phone hero size | the tablet hero size | the full hero size |
| Shelves | horizontal scroll with the swipe hint | horizontal scroll | horizontal scroll with arrow controls |
| Collection grid | two columns | three | four |
| Product page | gallery full width, buy column beneath, sticky action bar | as the phone | two columns |
| Cart | a full screen sheet | drawer | drawer |
| Checkout | one column, one step visible at a time | one column | one column, centred, with the summary beside it |

### Background work

| Job | Trigger |
|---|---|
| Hold expiry | holds end at their own moment; a sweep every minute tidies them |
| Carrier polling and reconciliation | hourly |
| Delivery confidence | at placement |
| Fit model recomputation | nightly |
| Postal refusal statistics | weekly |
| Back in stock notice | on a stock change |
| Abandoned bag reminder | at one hour and at twenty four hours, once each |
| Price history | on every price change |

### The inference boundary, evidence gaps and risks

The payment on delivery model is an inference from the market and the price architecture rather than something observed, and it is the largest one: if it were wrong, checkout, the lifecycle and delivery confidence would all change. On one side of the inference boundary sit the fixed facts: four departments and their sub-categories, a comparison price on every product, a menu that renders products, threshold promotions that cycle, the currency and the price points, and a messaging control. On the other sit the design decisions: the collection and product page layouts, the price history rule, the merchandising model, the promotion model and the threshold meter, and the whole payment on delivery model. The evidence gaps are the pages nobody could open on the reference: the product page, the collection page, the cart, the checkout, the account, the not-found page, hover states and the video reels. The enum substitutions place fitness equipment and sportswear retail in the `ecommerce-retail` domain, the exact member, and place Peakfit, a direct-to-consumer brand's own shop, in the solo founder category of the taxonomy rather than enterprise, which covers internal business functions, with a central flow that ends in a paid order. The known risks: the promotion precedence will need extending as real promotion rules accumulate, the type scale is a proposal, and the collection and product pages are reconstructions.

### Structured logs

Every request writes one JSON line to stdout carrying the route, the status and the elapsed milliseconds, and every response carries an `X-Request-Id` header.

## Data model

Twenty seven tables; the entities and the invariants are stated with each. Every invariant holds in the database itself under simultaneous requests; a check made in application code before a write is not enough. All timestamps are UTC. Money is integer paise with the currency `INR`, never a decimal. There is no password anywhere: the seeded accounts sign in with a code sent to their email in Mailpit, and `/app/USER_README.md` lists each seeded phone and email and says there is no password.

- **`product`**: handle unique, title, description, department, sub-category, `cod_eligible`, legacy identifier, created at.
- **`variant`**: `sku` unique, product, `options` (colour, size, weight or length), `price_minor`, `currency`, `on_hand`, `low_threshold`, `backorderable`, `cost`, `weight_grams`, dimensions, `state` of `active`, `draft` or `archived`. `available`, `compare_at_minor`, `saving_percent` and badges are derived, never stored.
- **`price_history`**: variant, `price_minor`, effective from. Every live compare price is supported by a row here.
- **`collection`**, **`media`**, **`size_chart`**, **`question`**.
- **`review`**: product, variant, customer, rating, body, state `held`, `published` or `removed`, verified purchase derived. Exists only against a delivered order line.
- **`customer`**: phone unique, email, name, role `customer` or `merchant`, verified, created at. Present even for guest orders.
- **`address`**: customer, name, line1, landmark, city, postal code, default.
- **`sign_in_code`**: phone, code, sent to, expires at, used at, wrong attempts.
- **`cart`** and **`cart_line`**: token unique, customer, closed; line sku, quantity, unit price at add, last change, reservation expires at.
- **`order`**: `number` unique and never reused, customer, `state`, `payment_method` of `prepaid`, `on_delivery` or `partial_advance`, `subtotal_minor`, `discount_minor`, `shipping_minor`, `tax_minor`, `total_minor`, `advance_minor`, `amount_due_on_delivery_minor`, the contact and the address copied as they were at placement, `placed_at`, `confirmed_at`, `delivered_at`, band, idempotency key and request fingerprint. Stored totals equal the sum of the lines, less the discounts, plus shipping, and are never recomputed for display.
- **`order_line`**: order, variant, quantity, `unit_price_minor`, `unit_compare_at_minor`, `allocated_discount_minor`, `paid_minor`, kit instance.
- **`shipment`** and **`shipment_event`**: order, carrier `event_id` unique, status, occurred at, window. A carrier event is applied at most once.
- **`payment`**: order, kind, amount, Kill Bill invoice identifier.
- **`refund`**, **`return`** and **`return_line`**: a refund never exceeds what was paid for the lines it covers, including apportioned discounts.
- **`promotion`** and **`promotion_usage`**: key, kind, threshold, amount, gift SKU, starts at, ends at, message.
- **`inventory_movement`**: variant, change, reason, order. A hold returns its stock exactly once.
- **`notification_delivery`** and **`audit_entry`**.
- **`order_confidence`**: order, band, signals, computed at, override by, override reason. No score column.
- **`address_history`**: normalised address hash, delivered, refused, undelivered, last event at. The hash is not the address, so the history is not a second copy of the customer database.
- **`postal_stats`**: postal code, refusal rate, sample, computed at.
- **`size_profile`**: customer, category, usual size, foot length in millimetres, chest and waist in centimetres, fit preference, updated at.
- **`product_fit`**, **`fit_feedback`** and **`fit_recommendation`**: family, runs, confidence, sample, computed at; order line, verdict `too_small`, `right` or `too_large`, source `return_reason`, `review` or `asked`; customer, variant, recommended size, confidence, basis.
- **`kit_template`**, **`kit_slot`**, **`kit_instance`** and **`bundle_rule`**: goal, space, slots, budget band; template, role, required, candidate rule, priority; customer, template, budget, lines, total, state; scope, discount kind, value, stacks with.

### Seed data

Seeding runs on first start and is idempotent: restarting the app never duplicates a row.

**Accounts.** Every account signs in by code; there is no password.

| Phone | Email | Name | Role | History |
|---|---|---|---|---|
| `9000000001` | `merchant@example.com` | `Mira Kapoor` | merchant | none |
| `9000000011` | `customer@example.com` | `Arjun Mehta` | customer | orders `PF-100001` and `PF-100002`, both delivered to `560001` |
| `9000000012` | `customer2@example.com` | `Kavya Iyer` | customer | order `PF-100003`, refused, in `560001` |
| `9000000013` | `customer3@example.com` | `Rohan Das` | customer | order `PF-100004` refused and order `PF-100005` undelivered, both in `560001` |
| `9000000014` | `customer4@example.com` | `Neha Joshi` | customer | three delivered and kept orders of `stridewell road runner` in UK 8 |
| `9000000015` | `customer5@example.com` | `Vikram Rao` | customer | none |
| `9000000016` | `guest@example.com` | `Sana Qureshi` | customer, guest only, never verified | order `PF-100006`, returned to origin |

Every seeded order was placed within the last twelve months.

**Products** named here exist exactly as stated; the catalogue holds `120` products and `380` variants in all across the four departments, the rest of them the builder's to name, each with a price history supporting its compare price.

| Handle | Title | Department | Sub-category | SKUs and options | Price | Compare price from history | On hand | Low threshold |
|---|---|---|---|---|---|---|---|---|
| `kinetra-compact-mini-massage-gun` | kinetra compact mini massage gun | `EQUIPMENTS` | `massagers` | `KIN-MG-GRAPHITE`, colour graphite | `189900` | `349900` | `40` | `5` |
| `ascendo-scalp-massager` | ascendo scalp massager - nordic teal | `EQUIPMENTS` | `massagers` | `ASC-SM-TEAL`, colour nordic teal | `29900` | `49800` | `120` | `10` |
| `ironleaf-doorway-pull-up-bar` | ironleaf doorway pull-up bar | `EQUIPMENTS` | `pull-up-bars` | `IRL-PUB-STD` | `129900` | `249900` | `25` | `5` |
| `tempo-resistance-bands` | tempo resistance bands | `EQUIPMENTS` | `resistance-bands` | `TMP-RB-10`, `TMP-RB-20`, `TMP-RB-30`, resistance 10, 20 and 30 kg | `49900`, `69900`, `89900` | `99900`, `129900`, `159900` | `60` each | `8` |
| `kinetra-vibration-plate` | kinetra vibration plate | `EQUIPMENTS` | `massagers` | `KIN-VP-PRO` | `569900` | `999900` | `12` | `3` |
| `ascendo-yoga-block` | ascendo yoga block for exercise | `EQUIPMENTS` | `yoga` | `ASC-YB-CORK` | `39900` | `79900` | `80` | `10` |
| `stridewell-road-runner` | stridewell road runner | `SPORTS SHOES` | `running` | `STW-RR-7` to `STW-RR-11`, sizes UK 7 to 11 | `279900` | `599900` | `10` each, `0` for UK 11 | `3` |
| `tempo-court-sneaker` | tempo court sneaker | `SNEAKERS` | `lifestyle` | `TMP-CS-7` to `TMP-CS-10`, sizes UK 7 to 10 | `229900` | `399900` | `8` each | `2` |
| `ironleaf-training-tee` | ironleaf training tee | `APPAREL` | `tops` | `IRL-TT-S`, `IRL-TT-M`, `IRL-TT-L` | `69900` | `119900` | `30` each | `5` |
| `peakfit-shaker-bottle` | peakfit shaker bottle | `EQUIPMENTS` | `accessories` | `PF-GIFT-SHAKER` | `49900` | `79900` | `200` | `10` |

The `kinetra compact mini massage gun` carried `399900` from two hundred days ago, `349900` from one hundred and twenty days ago and `189900` from sixty days ago, which is why its compare price is `349900` and not `399900`. `kinetra vibration plate` is not eligible for payment on delivery; every other seeded product is. Department handles are `equipments`, `sports-shoes`, `sneakers` and `apparel`, and the `department` field carries the department's name exactly as the tabs read. Prices across the catalogue run from `29900` to `569900` with compare prices from `49800` to `999900`.

**Collections**, eight: `bestsellers`, `home-gym-starter`, `recovery`, `running`, `new-arrivals`, `under-999`, `sneaker-drop`, `apparel-essentials`.

**Promotions**: the four in the promotion table, all active, ending thirty days after first start, with marquee messages naming the free gift above `1,999`, `200` off above `2,999` and `500` off above `4,999`.

**Orders**, twenty, `PF-100001` to `PF-100020`, across every state in the lifecycle table, including the refused `PF-100003` and `PF-100004`, the undelivered `PF-100005` and the returned to origin `PF-100006`; `4` returns at different stages; `40` products with published reviews and a rating histogram; `2` kit templates, `home-strength` and `mobility`; and fit feedback sufficient for `stridewell road runner` to show a runs small line and for `9000000014` to receive a high confidence recommendation.

## Constraints

- One brand's own shop: no marketplace, no second seller, no subscriptions.
- No password, no email-only sign in; identity is a verified phone.
- No card form and no payment processor; prepaid is recorded as paid, invoices live in Kill Bill.
- No SMS or chat vendor; messages travel as email through Mailpit.
- No image file ships with the build; fixtures generate their pictures.
- No per-visitor countdown, no randomised scarcity, no typed compare price.
- No confidence score shown to anyone.
- Stays responsive at `120` products, `380` variants and a year of orders.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`: `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
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

**No mocks.** An invoice must exist as a real invoice in Kill Bill, on the account whose external key is `peakfit-` followed by the phone, for the exact amount in `INR`. A paid column the app sets for itself, an invoice number it invents, or an order email it writes to its own log are all violations, however convincing the order page looks. A code or an order message must be delivered as a real email through Mailpit. Kill Bill and Mailpit are the facts: the app's own tables and interface can only reflect what lives there, never substitute for it.

## Definition of done

Peakfit is done when the app is deployed and healthy and a shopper can find a product, fill a bag, and check out as a guest with a verified phone, paying the courier on delivery. That order is invoiced in Kill Bill for the exact rupees collected only once it is delivered, and every stock unit, total, discount and refund on the way is decided by the server and counted exactly once.
