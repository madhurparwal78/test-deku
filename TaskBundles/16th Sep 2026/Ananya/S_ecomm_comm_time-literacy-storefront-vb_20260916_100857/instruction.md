# Tock: Time Literacy Storefront

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, set a fifteen minute tock on a
watch face they can watch run, add a children's watch to the cart, sign in, and place an order
that lands on its own order page, without hitting an error page. The order total must exist as a
real invoice in `killbill` on the account whose external key is `tock-` followed by the buyer's
email, for exactly that amount in `USD`, and the confirmation must arrive as real mail in the
`mailpit` inbox: an order the app records only in its own tables, or a green banner it shows to
itself, is not a sale.

## Overview

Tock sells analog wristwatches for children aged four and up. The watch has no screen and makes no
sound. Around its dial is a ring the child can turn, marked with four segments of five, ten,
fifteen and thirty minutes. Tock calls one timed segment a tock. A parent says "fifteen minutes",
the child turns the ring so the fifteen minute tock starts under the minute hand, and from then on
the child can see how much of that time is left without asking anyone. The second idea is the dial
itself: instead of numbers at twelve points, each hour is a wedge-shaped zone, so the hour hand sits
inside an hour rather than between two numerals.

This storefront has to teach that mechanism before it sells the watch. The home page carries a working watch
face the visitor can set and run, and a side-by-side comparison of a conventional dial and the Tock
dial driven by one slider. The catalogue holds two watch families in two case sizes, TOCK 33 (the
children's watch, four colourways) and TOCK 38 (the grown-up watch with a second time zone), a
discontinued TOCK 31, four parent-and-child bundles, straps, and a tote and a beanie that also come
free with any watch. Owners review what they bought, the shop owner moderates those reviews, and a
buyer checks out into a real invoice.

The people who use it are visitors who browse and fill a cart without an account, customers who
sign in to check out, and one shop owner who moderates reviews and adjusts stock. A child never
holds an account and never appears as a record.

It is deliberately **not** a marketplace, not a subscription, not a multi-currency or
multi-country shop, not a warranty or returns desk, and not a newsletter. There are no pop-up
overlays, no discount codes, no shoppable video and no press ticker.

The genuinely hard parts are three. The timer ring's four segments are unequal and tile the hour
end to end, so setting a tock is a subtraction that an evenly quartered dial gets silently wrong. A
bundle is two physical watches and owns no stock of its own, so its availability must always agree
with the two watches inside it. And the last unit of anything can be wanted by two carts at the
same instant, while every placed order must be backed by exactly one real invoice.

## User roles

Two signed-in roles plus the anonymous visitor. There is no role hierarchy and no staff role other
than the owner.

| Role | Can do | Cannot do |
|---|---|---|
| visitor (not signed in) | browse every public page, set and run the demo dial, fill a cart, ask for a restock email, send a support request, request a sign-in link, sign up | **check out, write a review, see any order, reach the owner console** |
| `customer` | everything a visitor can, plus check out, list and open their own orders, write one review per product, change their own name | **see another customer's order (it answers exactly as a missing one), publish or reject a review, adjust stock, reach the owner console** |
| `owner` | everything a customer can, plus publish, reject and reply to reviews in the moderation queue, read stock levels and adjust stock | **read a customer's order: the owner, like every account, sees only its own orders** |

The account holder is always the purchasing adult. No field anywhere in the product collects a
child's name, age or birthday, and no child-facing profile exists.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `customer` session to any `owner`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Signup is open: anyone may create a `customer` account at `/account/signup` with a password, or by
asking for a sign-in link at `/account/login`. The following accounts are seeded, all with the
password `deku-demo-pw-2026`:

| Email | Name | Role |
|---|---|---|
| `customer@example.com` | Casey Rivera | `customer` |
| `customer2@example.com` | Jordan Lee | `customer` |
| `owner@example.com` | Mara Ellison | `owner` |

`customer2@example.com` owns the seeded order `TK-SEEDED01`.

## Core features

### Auth

Accounts are email and password with bearer tokens, implemented by the app, plus a passwordless
emailed link. `POST /api/auth/signup` takes `{"email", "password", "name"}` and returns
`{"access_token": "..."}`. `POST /api/auth/login` takes `{"email", "password"}` and returns
`{"access_token": "..."}`. Every JSON call that needs an account carries that token as a bearer
token; the server-rendered pages keep the same sign-in in a session cookie. Passwords are stored
hashed, never in readable form. Email addresses are compared without regard to letter case.

1. A signup with an email that already has an account is rejected as invalid and writes no second
   `accounts` row.
2. A signup password shorter than 10 characters is rejected as invalid.
3. A login with a wrong password is denied, and the response does not say which half was wrong.
4. `POST /api/auth/link` with `{"email", "return_to"}` answers `{"status": "sent"}` with the same
   body whether or not that address has an account, and sends one message to that address with the
   subject exactly `Your Tock sign-in link`, whose plain-text body opens with a link of the form
   `<APP_PUBLIC_URL>/account/link/<token>`.
5. `POST /api/auth/link/consume` with `{"token"}` returns `{"access_token", "return_to"}`. The
   first use of a link for an address with no account creates a `customer` account for it.
6. A sign-in link is single-use and bound to the requesting address: consuming it invalidates it,
   so consuming the same token a second time is rejected and issues no token.
7. `return_to` is honoured only when it is a relative path starting with a single `/`. An absolute
   address such as `https://elsewhere.example/` or a path starting with `//` comes back as
   `/account` instead, so the sign-in route never sends anyone off the site.
8. Opening a spent link at `/account/link/<token>` shows `This sign-in link is no longer valid.`
   with a `Send a new link` control. `POST /api/auth/link/resend` with the spent token sends a
   fresh link to the same address without asking for the address again; a token the shop never issued
   is rejected as invalid and sends nothing.
9. `GET /api/account` returns `{"email", "name", "role"}`. `PATCH /api/account` accepts only
   `name`: a body carrying any other field, for example `child_name` or `child_birthday`, is
   rejected as invalid and nothing is written.
10. A call to an account, order, checkout, review-writing or owner endpoint with no bearer token is
    denied.

### The dial demonstration

The home page opens on the hero: copy on the left and, on the right, a drawn Tock watch in the
selected colourway with a working dial. Beneath the copy sits the timer setter, a bordered card
with the label `Try it. Set a tock and watch closely`, four chips, the readout
`No gimmicks, no alarms, just a simple visual timer to help with the passage of time`, and the
action `Run a tock` with `fast demo` in a lighter weight. Beneath the dial sit four colourway
swatches.

The ring carries four tocks. **They are not equal and they are not evenly spaced.** They tile the
hour end to end, in ascending length clockwise from the top:

| Tock | Length in minutes | Starts at minute |
|---|---|---|
| `5 min` | 5 | 0 |
| `10 min` | 10 | 5 |
| `15 min` | 15 | 15 |
| `30 min` | 30 | 30 |

Setting a tock is one subtraction. To start a tock of a given length at a given minute, the ring
turns by `(start minute - the tock's starting minute) * 6` degrees, six degrees being one minute,
written as a whole number from 0 to 359 (a negative turn wraps round). The dial's root element
carries that turn in `data-bezel-rotation`:

| Tock | Start minute | Offset in minutes | `data-bezel-rotation` |
|---|---|---|---|
| `15 min` | 38 | 23 | `138` |
| `30 min` | 10 | -20 | `240` |
| `5 min` | 0 | 0 | `0` |
| `10 min` | 59 | 54 | `324` |
| `30 min` | 30 | 0 | `0` |

1. The setter is a single-choice group of four options labelled `5 min`, `10 min`, `15 min` and
   `30 min`. `15 min` is selected when the page loads. Arrow keys move the selection, and the group
   is a single tab stop.
2. Selecting an option sets that tock at the visitor's current minute. The hero dial
   (`data-dial="hero"`) then carries the tock length in `data-segment-minutes`, the start minute
   from 0 to 59 in `data-start-minute`, and the turn in `data-bezel-rotation`, and all three always
   agree with the table above. A ring turned by the start minute alone, or cut into four equal
   quarters, is wrong.
3. `Run a tock` runs an accelerated pass through the selected tock: `data-elapsed-minutes` climbs
   from `0` to the tock length within ten seconds, never exceeds the tock length, and then the text
   `Tock complete` appears in a polite live region.
4. When the visitor's device asks for reduced motion, selecting an option moves the ring straight
   to its final turn, and `Run a tock` sets `data-elapsed-minutes` to the full tock length at once
   and shows `Tock complete` immediately.
5. The demonstration never makes a sound and never asks for permission to show notifications. It
   is a demonstration, not a kitchen timer.
6. The swatches `Aqua`, `Navy`, `Fuchsia` and `Glow` are toggle buttons with visible names. Pressing
   one recolours the whole dial and sets the hero dial's `data-colourway` to `aqua`, `navy`,
   `fuchsia` or `glow`. Exactly one swatch shows as pressed. When the page loads, `Aqua` is pressed,
   the hero dial carries `data-colourway` `aqua`, and a `15 min` tock is already set at the visitor's
   current minute, so `data-segment-minutes` reads `15`.
7. The hero dial is an image with a text alternative that follows the pattern
   `<Colourway> dial at <h:mm> with a <length> minute tock set`, for example
   `Aqua dial at 2:38 with a 15 minute tock set`, and it changes as the state changes.
8. If the dial cannot be drawn, the hero shows the watch illustration alone and the setter card is
   removed rather than left inert.

### The dial comparison

Further down the home page, the argument section compares a conventional dial with the Tock dial.
Both are driven by one slider labelled `Move the time`, a range whose value is the number of minutes
after 12:00, from `0` to `719` in steps of `1`, starting at `158` (which is 2:38). Its readout shows
the time as `h:mm` and is a polite live region. The left card renders a conventional dial
(`data-dial="plain"`: twelve numerals and sixty minute ticks) and the right card renders the Tock
dial (`data-dial="zoned"`) with the hour's zone lit.

1. ArrowRight and ArrowLeft move the slider one minute; PageUp and PageDown move it one hour.
2. Both dials always show the slider's time. The hour hand moves continuously through the hour:
   both dials carry `data-hour-rotation` equal to `(hour mod 12) * 30 + minute * 0.5` degrees,
   written with at most one decimal place.
3. The Tock dial lights the zone of the current hour and carries that hour, from 1 to 12, in
   `data-lit-hour`.
4. Both captions are generated from the slider's time, never fixed strings. The left caption reads
   `"Somewhere between H and N?"` where N is the next hour (after 12 comes 1), and the right caption
   reads `"It's in the H. H:MM."`:

| Slider time | `data-hour-rotation` | `data-lit-hour` | Left caption | Right caption |
|---|---|---|---|---|
| 2:38 | `79` | `2` | `"Somewhere between 2 and 3?"` | `"It's in the 2. 2:38."` |
| 9:04 | `272` | `9` | `"Somewhere between 9 and 10?"` | `"It's in the 9. 9:04."` |
| 12:15 | `7.5` | `12` | `"Somewhere between 12 and 1?"` | `"It's in the 12. 12:15."` |
| 11:59 | `359.5` | `11` | `"Somewhere between 11 and 12?"` | `"It's in the 11. 11:59."` |
| 3:00 | `90` | `3` | `"Somewhere between 3 and 4?"` | `"It's in the 3. 3:00."` |

5. The comparison dials carry text alternatives `Conventional dial at h:mm` and
   `Tock dial at h:mm with the H zone lit`, updated with the slider.

### The home page

The home page is one long argument in nine sections, in this order: the hero, the TOCK 33 range,
the TOCK 38 range, the comparison, the founder proof, the duration walkthrough, the testimonials,
the construction section, and the bundle band. The hero headline is the page's only level-one
heading and every other section opens at level two.

1. The TOCK 33 range eyebrow reads `Premium kids' watch - From $189.00`, where the price is the
   lowest price among TOCK 33 watches that are in stock or low on stock. When TOCK 33 Aqua has sold
   out it reads `From $229.00`. The TOCK 38 eyebrow `The grown-up one - From $379.00` follows the
   same rule, and so does the price beside `Shop TOCK 33` in the hero, which drops the cents.
2. Each range card shows the watch title and either its price or `Sold out`. A sold-out card
   carries no add control.
3. The duration walkthrough shows three small dials (`data-dial="stage"`) for one thirty minute
   tock, captioned `Set`, `Halfway` and `Done`, with `data-elapsed-minutes` of `0`, `15` and `30`.
   The three are drawn in their final states and never animate between them.
4. The testimonials section shows six quotes with their attributions, and the disclaimer
   `Quotes are reproduced from verified reviews and public forum posts, attributed to their source. They are individual experiences, not results we have tested for.`
   sits inside that same section, directly after the quotes, never in the footer.
5. The bundle band, headed `ONE FOR YOU, ONE FOR MINI-YOU`, shows the Grey and Aqua Bundle card
   with its price and an add control.
6. The reassurance row carries `30 day returns` over `Any reason`, `2 year warranty` over
   `Movement and build`, and `4+` over `Ages 4 and up` and `No reading needed`.
7. An announcement bar reading `BUY ANY TOCK, GET A TOTE AND BEANIE FOR FREE` runs across the top of
   every page while both gift items have stock available, and is absent from every page while
   either the tote or the beanie has none.

### Catalogue and collections

Six collections hold the catalogue: `tock-33` (`TOCK 33`), `tock-38` (`TOCK 38`), `tock-31`
(`TOCK 31`), `bundles` (`Bundles`), `straps` (`Straps`) and `all` (`Shop All`). Each renders at
`/collections/<handle>` as a product card grid and answers as JSON at
`GET /api/collections/<handle>` with `handle`, `title`, `notice`, `count`, `counts_reflect`,
`facets`, `sort_options` and `products`. Every collection page shares one structure: the heading,
the filter and sort controls with their faceting counts, the product grid, and the density control.
Each element of `products` carries `handle`, `title`, `family`,
`colourway`, `case_size`, `price`, `compare_at_price`, `currency`, `availability`,
`rating_average`, `review_count` and `siblings`. A card shows the product image, title, price or
`Sold out`, the rating summary, and colourway dots when the product has siblings in other
colourways.

1. Only published products ever appear in a collection, a search result, a page or the sitemap.
   `count` is the number of published products in the collection before any filter: `20` for
   `all`. The unpublished TOCK 33 Lilac never appears: `/products/tock-33-lilac` answers with the
   shop's not-found page, `GET /api/products/tock-33-lilac` answers not found, and reviews or restock
   requests on that handle answer not found and write nothing.
2. Five filters narrow a collection, each a query parameter: `family`, `colourway`, `case_size`,
   `availability` (`in_stock` or `sold_out`, where low stock counts as in stock and an unavailable
   bundle as sold out) and `price_band` (`under-100`, `100-299`, `300-499`, `500-plus`, in whole
   dollars), and `sort` picks the order. An unknown filter name, `availability` value, `price_band` value or
   `sort` value is rejected as invalid naming the parameter. A `family`, `colourway` or `case_size`
   value is known when any published product carries it and rejected the same way when none does;
   a known value that matches nothing in the collection leaves `products` empty. The page keeps the engaged filters and the sort in its
   own address, so a filtered grid can be shared and reopened.
3. `facets` maps each filter name to a list of `{"value", "count"}`, counting the products left
   after every engaged filter. A filter whose remaining products share a single value is left out
   of `facets`, unless that filter is engaged: `/api/collections/tock-33` offers `colourway` and
   `availability` and no `family`, `case_size` or `price_band`.
4. `counts_reflect` equals the engaged `availability` value (`in_stock` or `sold_out`) and is `all`
   while that filter is not engaged, and the grid says which with `Counts show in-stock items only`,
   `Counts show sold-out items only` or `Counts include sold-out items`.
5. `sort_options` holds `featured`, `price-asc`, `price-desc` and `newest`, plus `best-rated` only
   when at least two of the products shown have three or more published reviews. `price-asc` and
   `price-desc` order by price and then by title; `newest` orders by publication, newest first;
   `best-rated` orders by average rating, with products under three published reviews after the
   rest.
6. When filters leave nothing, the grid says `No products match these filters.` and offers one
   `Clear <Filter>` control per engaged filter (for example `Clear Colourway`), each clearing only
   its own filter.
7. `/collections/tock-31` carries the notice `TOCK 31 is discontinued. Every watch in this family has sold out.`
   at the top of the grid, and the same text in `notice`.
8. The filter and sort controls carry the visible words `Filter` and `Sort` at every width.
9. A density control offers `1 column`, `2 columns`, `3 columns` and `4 columns` on desktop, and
   choosing one sets the grid to that many columns.
10. Colourway dots on a card are links to the sibling product's own page, never an in-place image
    swap.
11. Two superseded product addresses answer with a permanent redirect: `/products/tock-38-grey-copy`
    to `/products/tock-38-grey`, and `/products/tock-33-shark` to `/products/tock-38-shark`.
12. `GET /api/search` with `q` returns the published products whose title contains `q`, ignoring
    case, as a top-level JSON array whose elements have the same fields as a collection's `products`;
    an empty `q` returns an empty array. `/search?q=aqua` lists the
    same products.

### Product pages

`/products/<handle>` is the page for one product. A product's sellability depends on three things:
it is published, it has a price, and it has units available; only a sellable product shows an add
control. `GET /api/products/<handle>` returns
`handle`, `title`, `kind`, `family`, `colourway`, `case_size`, `price`, `compare_at_price`,
`currency`, `availability`, `variants` (each with `sku`, `option`, `price`, `availability`),
`specifications` (each with `key`, `value`), `rating_average`, `review_count`, `rating_histogram`,
`siblings` (each with `handle`, `colourway`), and for a bundle `components`, `missing_components`
and `saving`. Money is in integer cents with `currency` `usd`.

1. `availability` is `in_stock` when four or more units are available, `low_stock` from one to
   three, `out_of_stock` at none, and `unavailable` for a bundle missing a watch; a strap that comes
   in sizes takes the availability of its best-stocked size. The page shows
   `Item is in stock`, `Only a few left`, `Item is out of stock` or `Item is unavailable`. No page and
   no public response states how many units are left.
2. The add control reads `Add to Cart`, then `Adding to Cart` while the request is in flight, and
   `Added to Cart` only after the server has confirmed the hold. A refused add returns the control to
   `Add to Cart` and shows an inline banner naming the reason.
3. An out-of-stock product replaces its add control with a restock form headed
   `Email me when it is back`, and still shows its price.
4. Straps that come in sizes show a size control with `Small` and `Large`; a size with no stock is
   shown as unavailable rather than removed. Watches, bundles, NATO straps and soft goods show no
   size control.
5. A product with a `compare_at_price` shows it struck through beside the price with a `Sale`
   badge and `Save $40.00` (for TOCK 31 Mint); `compare_at_price` is always greater than `price`.
6. Watch pages show a `Specifications` block as a definition list with exactly these fourteen keys
   in this order: `Case`, `Bezel`, `Movement`, `Bezel Marquetry`, `Dial`, `Hands`, `Lens`, `Crown`,
   `Band`, `Buckle`, `Water Resistance`, `Theoretical Battery life`, `Accuracy`, `Warranty`.
7. The reassurance row under the add control carries `Swiftpost 2 day in the US` over `Flat $15`,
   `30 day returns` over `Any reason`, and `2 year warranty` over `Movement and build`; TOCK 33 and
   bundle pages add `4+` over `Ages 4 and up` and `No reading needed`.
8. Watch pages carry four product images (front view, side view, on the wrist, crown detail) in a
   carousel that is a labelled group with previous and next controls, arrow-key navigation, and a
   position text such as `1 of 4`. The zoom control opens the image in a modal dialog that takes
   focus, closes on Escape and returns focus to the zoom control.
9. Watch pages carry seven short editorial blocks headed `Innovative Time System`, `Strap In`,
   `Lume Say What?`, `Case in Point`, `Dive! Dive! Dive!`, `The Swissness` and `Scratch That`, and a
   `Related products` cross-sell rail listing the other colourways of the same family.

### Bundles

A bundle is two physical watches, one TOCK 38 and one TOCK 33, sold as one line. It owns no stock
of its own, and its contents are disclosed as first-class information on its page.

1. A bundle's `availability` is derived from its two watches: it can be sold only while both are
   available, and the number of bundles available is the smaller of the two watches' available
   counts. A bundle is `unavailable` while either watch has none.
2. `components` lists both watches with `handle`, `title`, `availability` and `quantity`, and the
   page names both and links each to its own product page.
3. While a watch is missing, `missing_components` lists its title (a list of product titles, empty
   while both watches are available) and the page says
   `This bundle is unavailable because TOCK 33 Navy is out of stock.` (naming the missing watch), and
   offers the restock form for that watch.
4. `compare_at_price` is the sum of the two watches' current prices, and `saving` is that sum minus
   the bundle price; the Black and Navy Bundle shows `Save $69.00`. Both are computed, never typed.
5. The buy box shows the notice
   `This is a two-watch set and can only be returned complete. Individual watches from a set cannot be returned separately.`

### Reviews and moderation

1. A product page renders its published reviews in the page's first HTML, newest first, with the
   average to one decimal place and the count, shown as `4.1` and `Based on 7 reviews` for TOCK 33
   Aqua. Pending and rejected reviews are neither shown nor counted, and in every response
   `rating_average` is `null` while `review_count` is `0`.
2. `rating_histogram` maps `"5"` down to `"1"` to the number of published reviews at each rating. The
   histogram is a labelled figure whose text alternative gives the counts, for example
   `5 stars: 4, 4 stars: 2, 3 stars: 0, 2 stars: 0, 1 star: 1`.
3. `GET /api/products/<handle>/reviews` returns the published reviews as a top-level JSON array,
   each with `id`, `rating`, `title`, `body`, `author_name`, `status`, `verified_purchase` and
   `reply` (the reply's `body`, or null); with
   `rating` it returns only reviews at that rating. Each histogram row links to
   `/products/<handle>?rating=<n>`, which shows only reviews at that rating, so the one-star reviews
   are one click away.
4. A signed-in customer writes a review through `Write a review`, which opens a modal dialog, or
   `POST /api/products/<handle>/reviews` with `{"rating", "title", "body", "mentions_minor"}`. The
   review is stored as `pending` and the page says
   `Thanks. Your review will appear after moderation.` No review is ever auto-published: every
   published review has a named moderator, the owner.
5. An account may review a product once; a second review of the same product is rejected as a
   duplicate and writes nothing. A rating outside 1 to 5 is rejected as invalid.
6. `verified_purchase` is true only when the reviewing account has an order containing that
   product, on its own or inside a bundle, and such a review shows `Verified purchase`. The
   verified-purchase marker is resolved from order history, never asserted by the reviewer.
7. The owner publishes a pending review with `POST /api/owner/reviews/<id>/publish`, after which it
   is listed and counted. Publishing or rejecting a review that is not `pending` is rejected, and the
   review is unchanged.
8. The owner rejects a pending review with `POST /api/owner/reviews/<id>/reject` and a
   `policy_clause` of `profanity`, `personal-data`, `off-topic` or `spam`. A reject with any other
   clause, or none, is rejected and the review stays `pending`. A low rating is never a clause, so a
   critical review cannot be suppressed for being critical.
9. A review submitted with `mentions_minor` true (written by a child, or showing one) cannot be
   published without a non-empty `basis`: a publish without one is rejected and the review stays
   `pending`; a publish with one publishes it and records the basis.
10. The owner replies with `POST /api/owner/reviews/<id>/reply` and `{"body"}`, and the reply shows
    beneath the review labelled `Reply from Tock`, a merchant reply visually distinguished and
    labelled as from the seller. A review takes one reply: a second reply, or a reply with an empty
    `body`, is rejected and the first reply is unchanged.
11. A customer calling any `/api/owner/*` endpoint is denied, and the review is unchanged.
12. Review titles and bodies are shown as text, never as markup: a body containing `<b>` shows those
    characters.
13. A product with no published reviews shows `No reviews yet. Be the first to write one.`

### Cart, holds and the free gifts

A cart is identified by a token. `POST /api/cart` creates an empty cart and returns it with its
`token`; every other cart call carries it in the `X-Cart-Token` header. In the browser the cart
follows the visitor from page to page and survives signing in. `GET /api/cart` returns `token`,
`lines` (each with `id`, `sku`, `title`, `quantity`, `unit_price`, `line_total`, `is_gift`,
`promotion`), `notices` (each with `kind` and `message`), `subtotal`, `item_count` (the sum of the
non-gift quantities) and `hold_seconds_remaining`.

1. `POST /api/cart/lines` with `{"sku", "quantity"}` adds a line and holds that stock for this cart
   straight away. Adding a sku already in the cart raises that line's non-gift quantity instead of
   adding a second line; buying `TOTE-BONE` or `BEANIE-NAVY` while its free gift line is present adds a
   separate paid line. Adding the sku of an unpublished product, such as `TK33-LILAC`, or an unknown
   sku, is rejected as invalid and holds nothing.
2. A line's quantity is between 1 and 5. A quantity of 0 or 6 is rejected as invalid and nothing
   changes. `PATCH /api/cart/lines/<id>` with `{"quantity"}` changes it and moves the hold with it.
3. A bundle line holds one of each of its two watches for every bundle on the line.
4. An add that needs more than is available, for the product or for either watch in a bundle, is
   rejected whole: nothing is held for any part of it.
5. Two carts adding the last available unit of a product at the same instant: exactly one add
   succeeds and the other is rejected, and the units held never exceed the units on hand. This must
   hold under real concurrency.
6. Removing a line with `DELETE /api/cart/lines/<id>`, or lowering its quantity, releases that
   stock at once.
7. While the cart holds at least one watch or bundle, it carries exactly one gift `Tock Tote` line and one
   gift `Tock Beanie` line at a price of `0`, with `is_gift` true and `promotion` `Gift with purchase`,
   each holding one unit. More watches do not add more gifts.
8. Gift lines cannot be changed or removed: a `PATCH` or `DELETE` on one is rejected and the line is
   unchanged, and the page shows no quantity control and no remove control on it.
9. Removing the last watch or bundle removes both gift lines, releases their holds, and adds the
   notice of kind `promotion_removed` with the message
   `The free tote and beanie were removed because your cart no longer holds a watch.`
10. If the tote or the beanie has no stock available when a gift would be added, that gift is left
    out and the cart carries a notice of kind `gift_unavailable` naming it, for example
    `The free Tock Tote is out of stock.`
11. A hold lasts thirty minutes from the cart's last activity. `hold_seconds_remaining` reports the
    seconds left, is `1800` or just under straight after any change to the cart, and every change
    to the cart starts the thirty minutes again. A lapsed hold no longer counts against the stock
    available to other carts.
12. `subtotal` is the sum of the non-gift lines, and the header's cart control shows the cart total
    and the item count, reading `$0.00` and `(0)` when the cart is empty.
13. The `/cart` page and the cart drawer show every line; a bundle line lists its two watches
    beneath it and repeats the complete-set returns notice.

### Checkout, invoices and order mail

`POST /api/checkout` takes a bearer token, the `X-Cart-Token` header, an `Idempotency-Key` header,
and `{"shipping_address": {"name", "line1", "line2", "city", "region", "postcode", "country"}}`. It
returns the order: `number`, `status`, `hold_reason` (`po_box` or null), `subtotal`, `shipping`,
`total`, `currency` and `lines`, where each line carries `sku`, `title`, `quantity`, `unit_price`,
`is_gift` and `parent_sku` (the bundle's sku on a watch line that came inside a bundle, otherwise
null).

1. Checkout needs a signed-in account. An anonymous visitor opening `/checkout` is sent to
   `/account/login?return_to=/checkout`.
2. A checkout without an `Idempotency-Key` header is rejected as invalid and writes nothing.
3. A cart with no line other than gifts is rejected, and no order and no invoice are created.
4. `name`, `line1`, `city`, `region` and `postcode` are required and `country` must be `US`. A
   missing field or any other country is rejected as invalid naming the field, nothing is written,
   and the cart keeps its holds.
5. A successful checkout creates an order whose `number` is `TK-` followed by eight uppercase
   letters or digits, for example `TK-7Q2M9XKD`, with `status` `placed`, `subtotal` the sum of the
   non-gift lines, `shipping` `1500` on every order, `total` equal to `subtotal` plus `shipping`, and
   `currency` `usd`. TOCK 33 Aqua alone totals `20400`. The gift lines are on the order at `0`, and a
   bundle line is followed by its two watches as lines of their own at `0`, each naming the bundle in
   `parent_sku`.
6. The held stock becomes sold: each unit leaves both the on-hand and the held counts, the stock
   ledger records a `sale` entry noting the order number, and the cart is closed, so a further add to
   that cart token is rejected.
7. The order total must exist as a real invoice in `killbill`. The shop's Kill Bill account for a
   buyer has the `externalKey` `tock-` followed by the account's email in lowercase, for example
   `tock-customer@example.com`, with currency `USD`; it is created on the buyer's first order and
   reused on every later one, never duplicated. Every order gets its own invoice on that account whose
   amount is that order's total in dollars, `204.00` for the example above, in `USD`, so a buyer with
   three orders has three invoices there. No order is ever placed without its invoice.
8. Sending the same checkout again with the same `Idempotency-Key` returns the same order `number`
   and creates nothing new. Two simultaneous checkouts with one key produce exactly one order, one
   invoice and one confirmation email.
9. A placed order sends one confirmation email to the account's email address, with no cc and no
   bcc, whose subject begins with `Tock order confirmed:` followed by a space and the order number,
   for example `Tock order confirmed: TK-7Q2M9XKD`, and whose body opens with the order number and
   the total written as `$204.00` before listing the items.
10. An order whose address line 1 or line 2 contains `PO Box` or `P.O. Box`, in any letter case, is
    placed with `status` `on_hold` and `hold_reason` `po_box`, is invoiced like any other, and also
    sends an email whose subject begins with `Address needed:` followed by a space and the order
    number. An order with a street address never receives that email.
11. `GET /api/orders` returns the account's own orders, newest first, as a top-level JSON array, and
    `GET /api/orders/<number>` returns one of them. Another customer's order is a foreign resource on
    an authenticated route: its number answers not found, `404`, exactly as a number that does not
    exist, and `/orders/<number>` shows the not-found page for it.
12. Adding to a cart, writing a review, subscribing to a restock email and sending a support request
    send no order mail.

### Restock emails and the owner's stock

1. `POST /api/products/<handle>/restock-subscriptions` with `{"email"}` records a subscription with
   `status` `waiting` for a product that is `out_of_stock` and returns
   `{"product": "<handle>", "email": "<email>", "status": "waiting"}`. A product that is in stock or low on stock
   rejects it as invalid, and a bundle takes none (its page subscribes the visitor to the missing
   watch instead). The product page then shows `We will email you when NATO Strap Navy is back.`
   naming the product.
2. Asking again with the same email for the same product while a subscription is waiting creates no
   second subscription.
3. `GET /api/owner/stock` returns one row per sku with `sku`, `title`, `on_hand`, `reserved` and
   `available`. Bundles have no row.
4. `POST /api/owner/stock-adjustments` with `{"sku", "delta", "reason"}` moves `on_hand` by `delta`,
   records an `adjustment` entry in the stock ledger, and returns `sku`, `on_hand`, `reserved` and
   `available`. A `delta` of 0, an unknown sku, or a change that would leave `on_hand` below
   `reserved` is rejected and nothing changes.
5. When an adjustment takes a product from no units available to at least one, every waiting
   subscriber for that product receives exactly one email whose subject begins with `Back in stock:`
   followed by a space and the product title, for example `Back in stock: NATO Strap Navy`, and each
   of those subscriptions becomes `notified`. An adjustment to a product that already had stock, or
   that leaves it with none, sends no mail, and a notified subscriber is not mailed again unless they
   subscribe again.
6. A customer calling `/api/owner/stock` or `/api/owner/stock-adjustments` is denied and no stock
   changes.

### Content pages and shop policies

1. `GET /api/policies` returns `returns_window_days` `30`, `warranty_years` `2`,
   `minimum_age_years` `4`, `flat_shipping` `1500` and `currency` `usd`. Every surface that states a
   policy reads it from this one place: the home reassurance row (`30 day returns`), the product
   reassurance row, the cart trust column (`Easy 30-Day Returns`) and the shipping page all state the
   same thirty days.
2. `/pages/about` tells the founders' story in four paragraphs and ends with
   `We trust that you will find our products to be accurate, handsome, useful and, most importantly, indestructible.`
   signed by Mara and Joel Ellison.
3. `/pages/faq` carries six questions, each its own answer block with its own anchor:
   `When will I need to service my Tock timepiece?` (`#service`),
   `How waterproof is a Tock watch?` (`#waterproof`), `How long does my battery last?` (`#battery`),
   `What is the best way to clean my watch + band?` (`#cleaning`),
   `How long is my Tock watch warranty?` (`#warranty`) and `Are the materials safe?` (`#materials`).
4. `/pages/user-guide` carries three procedures as ordered lists, headed
   `How do I set the time on my Tock?`, `How do I change the band on my Tock?` and
   `How do I use the timing bezel on my Tock watch?`. The bezel procedure embeds a live dial
   (`data-dial="guide"`) set to its own example, a `15 min` tock starting at minute 38, so it carries
   `data-segment-minutes` `15`, `data-start-minute` `38` and `data-bezel-rotation` `138`.
5. `/pages/shipping-and-returns`, headed `Shipping & Returns`, states that orders ship within the
   United States only, by `Swiftpost` in two days, for a flat `$15`; carries the PO box rule
   `We do not ship to PO Boxes. If an order is placed to a PO Box, a customer service liaison will reach out to receive an alternative address. If we cannot confirm a new address within 5 business days, your order will be canceled and fully refunded.`;
   states thirty day returns for any reason and the complete-set rule for bundles; and states the two
   year warranty.
6. `/pages/contact-us` shows `Customer care and general inquiries: care@example.com`,
   `Press inquiries: press@example.com` and
   `We are available Monday through Friday, 10am - 5pm EST`, and a support form with `Name`,
   `Email`, `Subject` and `Message`.
7. `POST /api/support-requests` with `{"name", "email", "subject", "message"}` records the request
   and returns `{"reference", "queue"}`, where `reference` is `SR-` followed by eight uppercase
   letters or digits and `queue` follows the subject: `Order question` to `orders`,
   `Warranty or repair` to `warranty`, `Press` to `press`, `Something else` to `general`. A missing
   field, an invalid email or any other subject is rejected as invalid naming the field, and nothing
   is written. The page then shows `Thanks. Your reference is SR-XXXXXXXX.` with the real reference.
8. `/pages/terms` carries the terms of use and is linked from the footer.

### The public surface

1. A privacy page at `/pages/privacy`, linked from the footer of every page, states that the shop
   records an account's email and name, shipping addresses, orders and reviews; that it never
   records a child's name, age or birthday; and that it never holds card details.
2. `/sitemap.xml` lists the absolute address of every public route: `/`, the six collections, every
   published product page, the seven pages under `/pages/`, and `/search`. It never lists the
   account, cart, checkout, order or owner pages, or an unpublished product.
3. `/robots.txt` points at the sitemap with the line `Sitemap: <APP_PUBLIC_URL>/sitemap.xml` and
   carries `Disallow: /owner/`, `Disallow: /account`, `Disallow: /checkout` and `Disallow: /cart`.
4. Every internal link on every public route resolves to a real page, never to the not-found page.
5. Every content image carries alternative text saying what it shows, such as
   `TOCK 33 Aqua, front view`; decorative images and the reassurance illustrations carry empty
   alternative text or are hidden from assistive technology.
6. At a narrow viewport 390 CSS pixels wide, the home page, a collection, a product page and the cart
   never scroll sideways, and the menu control reveals every navigation link.

### The owner console

`/owner/reviews` lists pending reviews under the heading `Reviews waiting`, each with `Publish`,
`Reject` and `Reply` controls; publishing a review that mentions a child first asks for
`Basis for publishing`, and rejecting asks for a `Policy clause`. With nothing pending it says
`No reviews waiting.` `/owner/stock` shows a table with the columns `SKU`, `On hand`, `Held` and
`Available`, and each row takes an adjustment through `Adjust by`, `Reason` and `Save adjustment`.
A signed-in customer opening either page sees the not-found page, and an anonymous visitor is
sent to `/account/login?return_to=` followed by the page's path.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home: hero dial and setter, two range rails, comparison, founder proof, walkthrough, testimonials, construction, bundle band | public |
| `/collections/tock-33` | TOCK 33 grid | public |
| `/collections/tock-38` | TOCK 38 grid | public |
| `/collections/tock-31` | discontinued TOCK 31 grid with its notice | public |
| `/collections/bundles` | bundle grid | public |
| `/collections/straps` | strap grid | public |
| `/collections/all` | Shop All grid | public |
| `/products/<handle>` | product or bundle page | public |
| `/search` | search results for `q` | public |
| `/cart` | full cart page | public |
| `/checkout` | shipping address and `Place order` | customer |
| `/orders/<number>` | one order, and the confirmation after checkout | customer, own orders only |
| `/account` | name, order history table, `Sign out` | customer |
| `/account/login` | `Email me a sign-in link` form and password form | public |
| `/account/signup` | password signup | public |
| `/account/link/<token>` | signs the visitor in from an emailed link | public |
| `/owner/reviews` | moderation queue | owner |
| `/owner/stock` | stock table and adjustments | owner |
| `/pages/about` | founders' story | public |
| `/pages/faq` | six anchored questions | public |
| `/pages/user-guide` | three procedures and a live dial | public |
| `/pages/shipping-and-returns` | shipping and returns | public |
| `/pages/contact-us` | mailboxes, hours, support form | public |
| `/pages/privacy` | what the shop records | public |
| `/pages/terms` | terms of use | public |
| `/sitemap.xml` | every public route | public |
| `/robots.txt` | points at the sitemap | public |

**Entry and redirects.** An anonymous request for `/account`, `/checkout` or `/orders/<number>`
redirects to `/account/login?return_to=` followed by the requested path, and signing in lands on
that path. A password sign-in with no valid `return_to` lands on `/account`. `Sign out` on
`/account` ends the session and lands on `/`. A spent or expired sign-in link lands on the
`This sign-in link is no longer valid.` page. An unknown address, an unpublished product, another
customer's order, or an owner page opened by a customer shows the shop's own not-found page with a
link back to `/`, answering `404`.

**Journeys.**

1. Set a tock. Open `/`; `15 min` is selected. Select `30 min`: the hero dial now reads a thirty
   minute tock started at the current minute. Press `Run a tock`: the elapsed sector fills and
   `Tock complete` appears.
2. Recolour. On `/`, press `Navy`: the swatch shows pressed and the dial turns navy.
3. Compare. On `/`, focus `Move the time` (readout `2:38`): the captions read
   `"Somewhere between 2 and 3?"` and `"It's in the 2. 2:38."`. Press ArrowRight 26 times: the
   readout shows `3:04` and the captions read `"Somewhere between 3 and 4?"` and
   `"It's in the 3. 3:04."`.
4. Filter. Open `/collections/tock-33`, choose `In stock` under Availability: the grid shows TOCK 33
   Aqua and TOCK 33 Glow, the address carries `availability=in_stock`, and the grid note reads
   `Counts show in-stock items only`.
5. Bundle truth. Open `/products/bundle-black-navy`: it reads `Item is unavailable`, names TOCK 33 Navy
   as the missing watch, and offers the restock form for TOCK 33 Navy.
6. Buy. Sign in as `customer@example.com`, open `/products/tock-33-aqua`, press `Add to Cart` (the
   label passes through `Adding to Cart` to `Added to Cart`), and open the cart drawer: TOCK 33 Aqua
   at `$189.00`, then `Tock Tote` and `Tock Beanie` at `$0.00` labelled `Gift with purchase` with no
   quantity control. Press `Check Out`, fill the shipping address, press `Place order`, and land on
   `/orders/<number>` with the inline banner `Order placed` and a total of `$204.00`.
7. Sign in by email. On `/account/login`, enter a new address under `Email me a sign-in link`; the
   banner reads `If that address can receive mail, a sign-in link is on its way.` Open the link from
   that email and land on `/account`, signed in.
8. Write a review. As `customer@example.com` on `/products/tock-33-glow`, press `Write a review`, fill
   the dialog and press `Submit review`: the banner reads
   `Thanks. Your review will appear after moderation.` and the review is not listed.
9. Moderate. Sign in as `owner@example.com` and open `/owner/reviews`: publish Ravi's `Good but heavy`
   and see it listed on `/products/tock-38-black`; publishing Nora's `My daughter wrote this one`
   asks for `Basis for publishing` first.
10. Read the critical reviews. On `/products/tock-33-aqua`, choose the one-star row of the histogram:
    only Dana's review shows, with `Reply from Tock` beneath it.
11. Ask for a restock. On `/products/strap-nato-navy` (`Item is out of stock`), enter an email under
    `Email me when it is back`: the page shows `We will email you when NATO Strap Navy is back.`
12. Contact. On `/pages/contact-us`, send the form with the subject `Warranty or repair`: the page
    shows `Thanks. Your reference is ` followed by the new reference.

**States.** Every list has an empty state: the account with no orders shows `You have no orders yet.`
with a link to `/collections/all`; the cart shows `Your cart is empty.` with `Continue browsing`; a
filtered grid with no match names its filters and offers to clear each; a product with no reviews
invites the first; the owner queue says `No reviews waiting.` Every page shows its text at once while
images load inside boxes that keep their shape and shimmer softly. A refused action never replaces
the page: it shows an inline banner naming the reason, and nothing crashes.

## UI/UX notes

The character is calm, warm and demonstrative: the page reads like good paper, the watch face is the first thing seen, and nothing
moves unless it is explaining something. The north star is that a parent sees, in the first screen,
a watch face they can set and watch run. The register is consumer retail, and the subject comes
before any decoration.

**Palette, by role.** The page canvas is a near-white warm neutral, a warm bone rather than white,
and the header shares it exactly; the body ink is a near-black neutral, soft rather than hard, with a
pure near-black kept for maximum-contrast headings and a mid neutral for secondary text. There is one
blue: a mid, soft blue carries every primary action and the small capitalised kicker above each
section heading, and a deeper blue is its hover, with near-white text on it. A mid, vivid red is
reserved for sale prices and urgency and appears nowhere else in the interface (the drawn watches
keep their own colourway colours). The announcement bar is a near-black
cool neutral band with white text. Raised cards sit on a near-white neutral surface, and the header
is separated from content by a near-white neutral hairline, never a shadow. The light-ground
secondary action is a near-white, soft orange, so the secondary channel is never a copy of the
primary, and every translucent tint in the product steps along one shared set of eight strengths. Dark bands, such as the testimonials, invert to a near-black ground with warm bone text. Messages carry their own meaning colours, each distinct from the sale red and
from one another: failure is a deep, muted red darker than the sale red, success a deep, muted green,
and work in progress the primary blue beside a moving indicator. The exact shades are yours, so long
as body text and its background meet WCAG AA contrast on both the bone ground and the dark band.

**Typography.** Headings are set in `Jost`, a geometric sans, at weights 600 and 700; body and accent text
in `Cabin`, a humanist sans, at 400, 500 and 600 with italics. The kicker is the only uppercase,
tracked-out text in the system. Figures align in tabular columns wherever amounts or counts stack,
such as the cart table and the owner's stock table. Headline sizes step up sharply on larger screens; the exact scale
is in the front-end specification.

**Shape and density.** Buttons are full pills, and that is the brand's shape rather than a value to
tune; setter chips are pills too. Form inputs have barely rounded corners, review cards are softly
rounded, and the timer setter card is noticeably rounder. Density is comfortable, with the most room
around the dial. Space over dividers: sections read as separate without ruled lines, and the section rhythm follows
one six-step spacing scale, so no two gaps sit a hair apart.

**Components.** Every control has resting, pointed-at, pressed, focused and unavailable states, and
unavailable is never shown by colour alone. The cart drawer and every modal dialog close on Escape
and hand focus back to the control that opened them. Notices are inline banners beside what they
concern, never a floating message the visitor must catch. The hamburger's three bars are of unequal
length and stay that way, and the cart control's pointed-at state is a very faint circular wash
growing in behind the icon.

**Motion.** Motion is decelerating and considered: things start quickly and settle softly, like
something heavy coming to rest, and every transition that has no reason to differ shares that one
governing curve. Nothing bounces except the check that confirms an item was added. Movement is brief,
between a fifth and half a second, with the largest reveals a little longer. Headings, ledes and
buttons fade up as they arrive; the cart drawer slides in from the right and back out; images waiting
to decode carry a soft shimmer. Calm over expressive. When a device asks for reduced motion, no
decorative animation runs and content appears in its final place, the dial is placed rather than
swept, and state changes such as the drawer opening become a short cross-fade rather than vanishing.

**Mode.** Light only, designed fully. There is no dark theme.

**Responsive.** The layout is responsive across four widths: small phones, large phones, tablets and
desktops, with no other breakpoint. On phones the menu folds behind the hamburger with the wordmark
centred, the hero stacks with the dial below the copy, and the comparison stacks with the slider
between the two dials; from tablet up they sit side by side. At a narrow viewport nothing scrolls
sideways, the watch face never shrinks below legible numerals, and every navigation link stays
reachable.

**Accessibility.** The shop meets WCAG 2.2 AA. Keyboard navigation reaches every control in visual
order, starting from a `Skip to content` link, with a visible focus ring on the bone ground and on
dark bands. Touch targets are comfortably sized, including swatches and chips. Icon-only controls
carry the hidden labels `My Account`, `Search` and `Cart`. Every content image carries alternative
text saying what it shows, and every page declares its language. Meaning never rests on colour alone: a sale says `Sale` and a sold-out
item says `Sold out`.

## Technical requirements

The backend is `Flask` 3 on Python 3.12, rendering every page on the server with `Jinja2` templates
and serving JSON under the `/api` prefix on the same origin, run by `gunicorn`. This is a
multi-page, progressively enhanced application: the browser receives complete HTML on first paint,
including product copy, prices, availability and reviews, and `Alpine.js` 3 enhances four
isolated interactive islands on top of it (the dial, the cart drawer, the collection filter panel
and the product image carousel), never as whole-page rehydration. Scripts and styles are bundled with `esbuild` when the image is built. The
datastore is `postgres`, reached through `SQLAlchemy` 2 with the `psycopg` 3 driver at
`DATABASE_URL`. Billing is `killbill`, reached over HTTP with `httpx`. Mail is sent over real SMTP to
`mailpit` with Python's standard `smtplib`, at `SMTP_HOST` and `SMTP_PORT`, with `SMTP_USER` and
`SMTP_PASS` read from the environment beside them. The typefaces `Jost` and `Cabin` come from the
`@fontsource/jost` and `@fontsource/cabin` packages and are served from the app's own origin. The app
reads `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` from the environment and hardcodes no host and no port.
Authentication is email and password with bearer tokens for the JSON API and a session cookie for
pages, plus emailed sign-in links, all implemented by the app; passwords are hashed with
`werkzeug.security`.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are `postgres`, `killbill` and `mailpit`, and reaching for anything
else is a contract violation. All three are already running and reachable at their environment
variables, and must not be downloaded, installed, compiled or started.

`GET /api/health` returns `200` once the app is ready and needs no token.

Kill Bill is a billing platform, not a card processor: there is no card, no charge and no decline
in this product. The app reaches it at `PAYMENTS_API_URL` and authenticates every `/1.0/kb/`
request with Kill Bill's built-in HTTP Basic login, user `admin` with password `password`, the
`X-Killbill-ApiKey` header from `PAYMENTS_API_KEY` and the `X-Killbill-ApiSecret` header from
`PAYMENTS_API_SECRET`, adding an `X-Killbill-CreatedBy` header naming the shop on every write. The
tenant and its credentials already exist. A buyer's account is looked up with
`GET /1.0/kb/accounts?externalKey=` and created with `POST /1.0/kb/accounts` taking `name`,
`externalKey`, `email`, `currency` and `country`; Kill Bill answers a conflict when the external key
is already taken, so a second account for one buyer is refused by Kill Bill itself.
`GET /1.0/kb/invoices/pagination` lists every invoice, with `amount` as a decimal such as `204.00`
and `currency` uppercase, and an order's invoice must be one of them.

Logging is structured: every request writes one JSON log line to standard output carrying `request_id`, `method`, `path`,
`status` and `duration_ms`.

Two conventions hold everywhere. Money is an integer count of cents paired with the currency code
`usd` in the API and in the tables; it is formatted as dollars only on the page. All times are stored and compared in UTC.

Stock is contended between carts, and these properties must hold under simultaneous requests. Two
adds of the last available unit admit exactly one, and the loser is told why. A bundle add holds both
of its watches or neither. The units held for a product never exceed its units on hand, whichever
carts and checkouts are running at the same moment. Two checkouts carrying one `Idempotency-Key`
for one account produce one order, one invoice and one email, and the second caller receives that
same order.

Order numbers the shop issues and support references are unguessable rather than sequential, so
holding one reveals nothing about how many others exist; the seeded fixture number `TK-SEEDED01` is
the one exception.

## Data model

Eighteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

### `accounts`
`id`, `email` (unique, compared without letter case), `name`, `password_hash` (empty for an account
that has only ever signed in by link), `role` (`customer` or `owner`), `created_at`. No column holds
a child's name, age or birthday.

### `sign_in_links`
`id`, `email`, `token_hash`, `return_to`, `used_at`, `expires_at`, `created_at`. A link is usable
once.

### `products`
`id`, `handle` (unique), `title`, `kind` (`watch`, `strap`, `bundle` or `accessory`), `family`
(`tock-33`, `tock-38`, `tock-31`, `bundle`, `strap` or `soft-goods`), `colourway`, `case_size`
(millimetres), `status` (`active`, `discontinued` or `draft`), `description`, `position` (the
featured order), `published_at`. A product is published when its `status` is `active` or
`discontinued` and it has a `published_at`.

### `product_handle_aliases`
`alias` (unique), `product_id`, `reason`.

### `variants`
`id`, `product_id`, `sku` (unique, always present), `option` (`Small`, `Large`, or empty), `price`,
`compare_at_price` (empty, or greater than `price`), `grams` (greater than zero).

### `product_specifications`
`product_id`, `position`, `key`, `value`, holding the fourteen keys in their fixed order for each
watch.

### `inventory_items`
`id`, `variant_id` (unique), `on_hand`, `reserved`. `reserved` is never greater than `on_hand` and
neither is ever negative. A bundle variant never has a row: its availability is derived from its
components on every read.

### `bundle_components`
`bundle_variant_id`, `component_variant_id`, `quantity`, one row per watch in a bundle.

### `stock_ledger`
`id`, `inventory_item_id`, `delta`, `reason` (`seed`, `adjustment` or `sale`), `note`, `created_at`.
Rows are only ever added. For every inventory item, the sum of its ledger `delta` values equals its
`on_hand`.

### `carts`
`id`, `token` (unique), `account_id`, `status` (`open` or `checked_out`), `last_activity_at`,
`created_at`.

### `cart_lines`
`id`, `cart_id`, `variant_id`, `quantity` (1 to 5), `unit_price`, `is_gift`, `promotion`.

### `reservations`
`id`, `cart_id`, `cart_line_id`, `inventory_item_id`, `quantity`, `status` (`held`, `released` or
`converted`), `expires_at`, `created_at`. For every inventory item, the quantities of its `held`
reservations add up to its `reserved`.

### `orders`
`id`, `number` (unique), `account_id`, `status` (`placed` or `on_hold`), `hold_reason`, `subtotal`,
`shipping`, `total`, `currency`, `shipping_name`, `shipping_line1`, `shipping_line2`,
`shipping_city`, `shipping_region`, `shipping_postcode`, `shipping_country`, `idempotency_key`,
`billing_external_key`, `placed_at`. One order per account and `idempotency_key`. `total` is always
`subtotal` plus `shipping`.

### `order_lines`
`id`, `order_id`, `variant_id`, `parent_line_id`, `quantity`, `unit_price`, `is_gift`,
`title_snapshot`, `sku_snapshot`. A bundle line has two child lines, one per watch, with a
`unit_price` of `0`. An order's `subtotal` is the sum of `unit_price` times `quantity` over its lines
with no parent.

### `reviews`
`id`, `product_id`, `account_id` (empty for imported reviews), `author_name`, `rating` (1 to 5),
`title`, `body`, `status` (`pending`, `published` or `rejected`), `verified_purchase`,
`mentions_minor`, `minor_basis`, `rejection_clause`, `created_at`, `published_at`. One review per
account per product.

### `review_replies`
`id`, `review_id` (unique), `body`, `created_at`.

### `restock_subscriptions`
`id`, `product_id`, `email`, `status` (`waiting` or `notified`), `created_at`, `notified_at`. At most
one `waiting` subscription per product and email.

### `support_requests`
`id`, `reference` (unique), `name`, `email`, `subject`, `queue`, `message`, `created_at`.

**Derived, never stored:** a bundle's availability, `compare_at_price` and `saving`; every
product's `availability`; `rating_average`, `review_count` and `rating_histogram`; a collection's
`count`; the range and hero from-prices; a cart's `subtotal`, `item_count` and
`hold_seconds_remaining`.

### Seed data

Products, with price in cents and units on hand per sku:

| Handle | Title | Family | Colourway | Case | Price | Sku | On hand |
|---|---|---|---|---|---|---|---|
| `tock-33-aqua` | TOCK 33 Aqua | `tock-33` | `aqua` | 33 | 18900 | `TK33-AQUA` | 12 |
| `tock-33-navy` | TOCK 33 Navy | `tock-33` | `navy` | 33 | 18900 | `TK33-NAVY` | 0 |
| `tock-33-fuchsia` | TOCK 33 Fuchsia | `tock-33` | `fuchsia` | 33 | 18900 | `TK33-FUCHSIA` | 0 |
| `tock-33-glow` | TOCK 33 Glow | `tock-33` | `glow` | 33 | 22900 | `TK33-GLOW` | 6 |
| `tock-38-grey` | TOCK 38 Grey | `tock-38` | `grey` | 38 | 37900 | `TK38-GREY` | 5 |
| `tock-38-black` | TOCK 38 Black | `tock-38` | `black` | 38 | 37900 | `TK38-BLACK` | 5 |
| `tock-38-glow` | TOCK 38 Glow | `tock-38` | `glow` | 38 | 42900 | `TK38-GLOW` | 3 |
| `tock-38-shark` | TOCK 38 Shark | `tock-38` | `shark` | 38 | 39900 | `TK38-SHARK` | 4 |
| `tock-31-mint` | TOCK 31 Mint | `tock-31` | `mint` | 31 | 5900, compare at 9900 | `TK31-MINT` | 0 |
| `bundle-black-navy` | Black and Navy Bundle | `bundle` | | | 49900 | `BNDL-BLACK-NAVY` | none |
| `bundle-grey-aqua` | Grey and Aqua Bundle | `bundle` | | | 46900 | `BNDL-GREY-AQUA` | none |
| `bundle-glow-glow` | Glow and Glow Bundle | `bundle` | | | 54900 | `BNDL-GLOW-GLOW` | none |
| `bundle-shark-fuchsia` | Shark and Fuchsia Bundle | `bundle` | | | 51900 | `BNDL-SHARK-FUCHSIA` | none |
| `strap-woven-sand` | Woven Strap Sand | `strap` | `sand` | | 2400 | `STRAP-WOVEN-SAND-S`, `STRAP-WOVEN-SAND-L` | 20, 0 |
| `strap-rubber-navy` | Rubber Strap Navy | `strap` | `navy` | | 2900 | `STRAP-RUBBER-NAVY-S`, `STRAP-RUBBER-NAVY-L` | 15, 15 |
| `strap-rubber-fuchsia` | Rubber Strap Fuchsia | `strap` | `fuchsia` | | 2900 | `STRAP-RUBBER-FUCHSIA-S`, `STRAP-RUBBER-FUCHSIA-L` | 10, 1 |
| `strap-nato-aqua` | NATO Strap Aqua | `strap` | `aqua` | | 2200 | `STRAP-NATO-AQUA` | 30 |
| `strap-nato-navy` | NATO Strap Navy | `strap` | `navy` | | 2200 | `STRAP-NATO-NAVY` | 0 |
| `tote-bone` | Tock Tote | `soft-goods` | `bone` | | 2000 | `TOTE-BONE` | 5000 |
| `beanie-navy` | Tock Beanie | `soft-goods` | `navy` | | 2200 | `BEANIE-NAVY` | 5000 |
| `tock-33-lilac` | TOCK 33 Lilac (status `draft`, never published) | `tock-33` | `lilac` | 33 | 18900 | `TK33-LILAC` | 8 |

TOCK 31 Mint has `status` `discontinued`; every other product except TOCK 33 Lilac is `active` and
published. The bundles pair a TOCK 38 with a TOCK 33: Black and Navy is `TK38-BLACK` with
`TK33-NAVY`, Grey and Aqua is `TK38-GREY` with `TK33-AQUA`, Glow and Glow is `TK38-GLOW` with
`TK33-GLOW`, and Shark and Fuchsia is `TK38-SHARK` with `TK33-FUCHSIA`. At seed time the Black and
Navy and the Shark and Fuchsia bundles are `unavailable`, Glow and Glow is `low_stock`, and Grey and
Aqua is `in_stock`. Every inventory item's seed quantity is written to the stock ledger as a `seed`
entry.


One order is seeded: `TK-SEEDED01`, owned by `customer2@example.com`, `status` `placed`, for one
NATO Strap Aqua shipped to a street address in `US`, with `subtotal` `2200`, `shipping` `1500` and
`total` `3700`. Seeding it also raises its invoice, once, on the Kill Bill account
`tock-customer2@example.com` for `37.00` `USD`, and writes no stock ledger entry.

Product handle aliases: `tock-38-grey-copy` points at `tock-38-grey`, and `tock-33-shark` points at
`tock-38-shark`.

Watch specifications, TOCK 33 (all colourways): `Case` 33mm Swiss nylon polymer; `Bezel`
Bidirectional rotating bezel with timer function and lume; `Movement` Swiss Made 3-jewel quartz with
anti-shock; `Bezel Marquetry` Contrast lume fill; `Dial` Embossed brass with pad-printed indexes and
appliques; `Hands` Brass dauphine hands with lume; `Lens` Scratch-resistant sapphire crystal;
`Crown` Screw-down 316L stainless steel; `Band` 17mm recycled woven polyester; `Buckle` 316L
stainless steel; `Water Resistance` 10 ATM; `Theoretical Battery life` 10 years; `Accuracy` Plus or
minus 10 seconds per month; `Warranty` 2 years. TOCK 38 differs only in `Case` 38mm Swiss nylon
polymer over a steel core, `Movement` Swiss Made Ronda GMT quartz and `Dial` Brass with a second time
zone hand. TOCK 31 differs only in `Case` 31mm Swiss nylon polymer.

Imported reviews, each with its `author_name`:

| Product | Author | Rating | Title | Verified | Status |
|---|---|---|---|---|---|
| `tock-33-aqua` | Priya | 5 | Fewer questions in the car | yes | `published` |
| `tock-33-aqua` | Tom | 5 | Survived the playground | yes | `published` |
| `tock-33-aqua` | Lena | 5 | She reads the hour now | yes | `published` |
| `tock-33-aqua` | Marco | 5 | A proper first watch | yes | `published` |
| `tock-33-aqua` | Ada | 4 | Bezel is stiff at first | yes | `published` |
| `tock-33-aqua` | Sam | 4 | Lovely, not cheap | no | `published` |
| `tock-33-aqua` | Dana | 1 | Strap tore at the buckle holes | yes | `published` |
| `tock-33-glow` | Iris | 5 | Glows all night | yes | `published` |
| `tock-33-glow` | Ben | 5 | Our second Tock | yes | `published` |
| `tock-33-glow` | Kofi | 4 | Pale in daylight | yes | `published` |
| `tock-38-grey` | Hana | 5 | Matching watches | yes | `published` |
| `tock-38-grey` | Luis | 4 | Handy second time zone | no | `published` |
| `tock-38-black` | Ravi | 3 | Good but heavy | no | `pending` |
| `tock-33-glow` | Nora | 5 | My daughter wrote this one | no | `pending`, `mentions_minor` true |

Dana's review reads: "The strap tore at the buckle holes within two months, the dial is hard to read
in low light, the lume only covers the bezel, and we paid import charges nobody warned us about." It
carries the reply "Sorry, Dana. A replacement strap is on its way under the warranty, and our shipping
page now explains import charges." Every other imported review carries one or two sentences of its
own in the same plain voice. At seed time TOCK 33 Aqua shows `4.1` from 7 reviews, TOCK 33 Glow `4.7`
from 3, and TOCK 38 Grey `4.5` from 2.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the exact design detail behind the notes above.

### The dial's hooks

Every drawn dial's root element has an image role, a text alternative, and these attributes:
`data-dial` (`hero`, `plain`, `zoned`, `stage` or `guide`), `data-colourway`, `data-segment-minutes`
(`5`, `10`, `15`, `30`, or empty when no tock is set), `data-start-minute`, `data-bezel-rotation`,
`data-elapsed-minutes`, `data-hour-rotation`, and on the zoned dial `data-lit-hour`. The dial is drawn
from geometry at any size, so one drawing serves a large hero dial, a medium comparison dial and small
walkthrough dials without redrawing.

### The dial, drawn

The minute hand turns six degrees a minute and the hour hand half a degree a minute, both
continuously. A soft, warm, low shadow sits under the case so the watch reads as an object on a
surface rather than a diagram. The standard dial shows the colourway, the bezel and the three hands;
the plain dial is a conventional face with twelve numerals and sixty minute ticks, every fifth tick
heavier, and no bezel; the hero dial sits inside a drawn watch body. The elapsed part of a running
tock is a filled sector inside an outline of the whole tock, and the fill stops at the end of the tock
rather than wrapping past it. Lighting an hour swaps that zone's fill and numeral to the colourway's
lit colours.

Each colourway is a complete set of 26 named colour roles (`case`, `caseDark`, `strap`, `bezel`,
`bezelEdge`, `line`, `engrave`, `dial`, `segment`, `num`, `tick`, `tickNum`, `print`, `handHour`,
`handHourIn`, `handMin`, `handMinIn`, `handSec`, `handSecIn`, `cap`, `accent`, `accentText`, `ink`,
`segmentEdge`, `segmentLit`, `segmentLitNum`), plus a hand edge colour, and a missing role never
falls back to black.

- **Aqua:** a light, soft cyan case with a darker soft cyan edge, a light muted cyan strap, a
  near-white neutral bezel and near-white cool neutral dial, light soft cyan tocks, deep cool neutral
  numerals, mid, vivid cyan ticks and accent with a mid, soft cyan accent text, and a deep, soft cyan
  lit zone with a near-white numeral.
- **Navy:** a deep, muted blue case and bezel, a deeper muted blue strap edge, a near-white neutral
  dial, light muted blue tocks, mid, vivid red ticks and accent, a mid, soft red accent text, and a
  mid, vivid red lit zone.
- **Fuchsia:** a light, vivid magenta case with a mid, vivid magenta edge, a light, soft magenta strap,
  a near-white neutral bezel and dial, light soft magenta tocks, mid, vivid magenta ticks, and a mid,
  soft magenta lit zone.
- **Glow:** a near-white neutral, pale luminous case with a light neutral edge, near-white neutral
  strap, bezel and dial, light, muted lime tocks, mid, muted lime ticks and accent, and a deep, muted
  lime accent text and lit zone.

Numerals and hands stay legible against their zone fill in all four colourways, and Glow, the palest,
is where that is hardest.

### Type scale

Fifteen steps, each with a phone, tablet and desktop size; the eight largest scale fluidly between the
phone and desktop sizes and the seven smallest step at breakpoints. Step 1 is 10px at every width;
step 2 is 11px, 11.5px and 11.5px; step 3 is 13px, 13.5px and 14px; step 4 is 15px, 16px and 17px;
step 5 is 17px, 19px and 21px; step 10 is 37px, 42px and 56px; step 11 is 43px, 49px and 68px; step 12
is 49px, 58px and 83px; step 13 is 57px, 68px and 102px; step 14 is 67px, 80px and 124px; step 15 is
77px, 94px and 151px. The hero headline is step 10 on two hard-wrapped lines and the lede is step 5.
Body text runs at 14.25px, 15.2px and 16.15px with a line height of 1.5; labels run at 11.7px, 12.15px
and 12.6px at weight 500. Fonts load with a swap policy.

### Global chrome

- **Announcement bar:** one centred line in the smallest uppercase label size.
- **Header:** the bone ground and a hairline beneath; the wordmark on the left; the five links
  `TOCK 33`, `TOCK 38`, `Bundles`, `Straps` and `About`, then the account, search and cart icon
  controls. It sticks to the top on scroll with the hairline as its only separation. The cart control
  shows the running total and the item count in brackets.
- **Cart drawer:** a dialog sliding in from the right over a blurred, tinted underlay; focus moves in,
  stays inside while open and returns on close; Escape closes it; the page behind does not scroll.
- **Footer:** an upper white band with the reassurance row, the statement
  `Why Tock? We believe time management is a superpower and the tradition of analog is worth preserving.`,
  the group `Main menu` (`Home`, `Shop All`, `Contact`) and the group `More Links` (`Search`,
  `Terms of Use`, `Privacy`, `Shipping and Returns`, `User Guide`, `Watch FAQs`); a lower near-black
  band with the wordmark, the year and the same links repeated. The footer cards read `Watch FAQs`
  over `Your questions, answered.` and `Need Help?` over `Email us at care@example.com`.
- **Iconography:** one inline sprite of line icons that inherit the text colour and share one stroke
  width: a hamburger of three bars of unequal length, a bag, a user, a search glass, a close cross, a
  check, three chevrons, a long arrow, a sync icon, a filter icon with a symmetric taper and a sort
  icon with a left-aligned taper (each always beside its word), grid-density squares, and stars with
  fractional fills for ratings.

### Motion, moment by moment

One governing curve that starts fast and settles softly carries drawers, reveals, staggered content
and media. A symmetric standard easing serves state toggles that reverse, a pure deceleration serves
entrances that have no exit, an acceleration serves exits, and an overshoot past its endpoint is
reserved for the add-to-cart confirmation. A slow start with a hard finish, a gentler default
alternative, and symmetric curves eased at both ends are the only other characters in use; easings
that third-party widgets bring with them are not adopted. The durations are few: the fastest
acknowledgements on media thumbnails, colour and opacity changes on small controls, a workhorse
duration for transform, opacity and backdrop treatment changes on drawer chrome, a slightly longer one
for buttons and cards, drawer and filter-panel travel, and one longest duration for large content reveals.
The named keyframes are `slide-in` (the drawer entering from the right), `slide-back-out` (the drawer
leaving to the right), `heroFade` (every above-the-fold heading, lede and button fading up as it arrives) and
`imgLoadingShimmer` (the placeholder shimmer before an image decodes), so a drawer's enter and exit
run on `slide-in` and `slide-back-out`. A content reveal staggers three steps so closely that they
read as one movement with texture, and a media thumbnail moves its shape first and fades its content
in after it has settled. Under reduced motion none of these runs except the short cross-fade that
keeps a state change visible.

### The home page, section by section

- **Hero:** eyebrow `Exceptional wristwatches for kids to learn time`; headline
  `Nobody is born knowing` over `how long fifteen minutes is.`; lede
  `Rotate the bezel and align the start of a tock with the minute hand to learn the fundamentals of time management`;
  primary action `Shop TOCK 33` with the from-price; four chips of specification marked with blue
  bullets: `2mm sapphire crystal`, `100m water resistance`, `Japanese LumiNova`,
  `Swiss ETA quartz movement`.
- **TOCK 33 range:** heading `TOCK 33. 33mm, a first watch for a small wrist.` and line
  `Four colourways, one size. The run-thru strap fits any wrist.`
- **TOCK 38 range:** heading `TOCK 38 GMT: For older wrists featuring two time zones` and line
  `Swiss nylon polymer over a steel core. Swiss Made Ronda GMT movement. 2mm sapphire crystal. Rotating timer bezel with lume. Screw-down crown and case back, 100m water resistance.`
  Each range rail scrolls sideways as a keyboard-scrollable region with a visible focus ring.
- **Comparison:** eyebrow `The dial innovation`; heading
  `Most of a clock's day is spent between the numbers.`; lede
  `Normal dials have the hour hand between two numerals for most of the hour. An adult reads through that without noticing. A child asked what it says will often tell you "somewhere between two and three." We call that gap no man's land - we solved that design flaw.`;
  left card `Conventional Dial` with
  `The hour hand spends almost all of its time between two numerals, not clearly indicating which hour it currently is.`;
  right card `Tock Dial` with
  `We moved every hour off a point and into a tock. The hand sits inside the hour's own zone rather than between two numerals.`
- **Founder proof:** kicker `The co-founders first test with the prototype`; pull quote
  `"We're like...halfway there."`; body
  `Thirty minutes from their grandparents' house, my kids set a thirty minute tock on an early prototype. Fifteen minutes in, the youngest said that ^ out loud to nobody in particular. No "are we there yet" just confidence - the moment we knew that tocks were a thing - Mara.`;
  close
  `You say a number, your child turns the ring to the start of that tock, and from then on the watch is the one being asked how much longer. It is a simple concept, but infinitely empowering.`
- **Duration walkthrough:** overlay `Thirty minutes out. Fifteen gone. Half the tock still to run.`;
  each stage dial carrying its short caption `Set`, `Halfway` or `Done` above a description, in
  order `The bezel is turned to the start of the 30 minute tock`,
  `15 minutes have passed, the hand is half way through the tock` and
  `The 30 minute tock has elapsed, time to...build a dinosaur fort?`; footnote
  `The bezel is marked in 5, 10, 15 and 30 minute "tocks". Each number is the length of time for the minute hand to pass.`
- **Testimonials:** a dark band; eyebrow `What owners tell us`; heading
  `TIME CONFIDENCE - knowing how much longer.`; lede
  `We built Tock for the car, the countdown and the bedtime negotiation. Owners keep putting it to new uses - we've been shocked but the number of ADHD messages we get...`;
  the six quotes and attributions are "The car ride question stopped. She just looks at her wrist
  now." (`Verified owner`), "Fifteen minutes finally means something to my son." (`Public forum post`),
  "Bedtime negotiations went from ten rounds to one." (`Verified review`), "Our ADHD kiddo uses the
  bezel to pace homework breaks." (`Public forum post`), "My teacher asked how I knew there were five
  minutes left." (`Owner, age 8`) and "It helps our autistic son see transitions coming."
  (`Verified review`); then the disclaimer.
- **Construction:** eyebrow `How it's built`; heading
  `Kids' watches usually fail at the bit you look through.`; lede
  `Read the reviews under any children's watch and the same complaint comes back: the crystal scratches until the dial can't be read. So that is the part we spent the money on.`;
  four cards: `Sapphire crystal` with
  `Mohs 9 on the hardness scale. Chosen because a scratched crystal is the most common complaint in this category.`,
  `100m water resistance` with
  `Rated to 100m. Showers, baths and swimming are fine. Care guidance ships with the watch.`,
  `Screw-down crown` with
  `The crown threads shut rather than pushing in, so it stays secured when it is closed.`, and
  `Swiss ETA quartz movement` with
  `The same movement family used across Swiss quartz watches. Battery, not charging.`

### Product, cart and content copy

- Product: `Add to Cart`, `Adding to Cart`, `Added to Cart`; `Sale` and `Save`; `Read more`; blocks
  `Specifications`, `Materials & Care`, `Size & Fit` and `Shipping & Returns`; `Customer Reviews`,
  `Based on N reviews` and `Write a review`; rails `Related products` and `See all` with a label naming
  the rail; size and fit text
  `Our straps have infinite size adjustability with a reliable steel buckle designed to fit a wide range of ages and sizes.`
- Cart: `Your Cart`; `Continue browsing`; columns `Price`, `Quantity` and `Total`; `Subtotal`;
  `Shipping & taxes calculated at checkout`; `Check Out` and `Update Cart` (the latter only matters
  without scripts, since quantity changes apply at once); a trust row of `Parent approved` over
  `Founded and designed by real parents for real kids.`, `Easy 30-Day Returns` over
  `Not the right fit? No problem. See our return information below.`, and `Secure Checkout` over
  `Your payment information is encrypted and secure.`
- Checkout: fields `Full name`, `Address line 1`, `Address line 2`, `City`, `State`, `ZIP code` and
  `Country` (United States), a summary of `Subtotal`, `Shipping` and `Total`, and `Place order`.
- Account: heading `Your account`; the order table's columns `Order`, `Placed`, `Status` and `Total`.
- Sign-in: heading `Sign in`; `Email me a sign-in link` with `Email` and `Send link`; a password form
  with `Email`, `Password` and `Sign in`; `Create an account` linking to `/account/signup`.
- FAQ battery answer:
  `Up to 10 years..... Why isn't this exact? Batteries are weird. Temperature changes, the amount of aggressive jiggling and indeed, interplanetary travel can affect this as well.`
- User guide closing step for setting the time:
  `The most important part! Screw the crown clockwise back into the case until it's a snug tight fit, this means it's fully sealed and back up to dive grade water resistance.`

### Layout across widths

| Region | Small phone | Large phone | Tablet | Desktop |
|---|---|---|---|---|
| Header | hamburger, centred wordmark, three icons | as small phone | full link row | full link row |
| Hero | stacked, dial below the copy | stacked | two columns, dial right | two columns, wider gutter |
| Timer setter | full width, chips wrap to two rows | full width | inline in the left column | inline |
| Range rail | one and a half cards | two cards | three cards | four cards |
| Comparison | stacked, slider between the dials | stacked | side by side | side by side |
| Walkthrough | three stacked | stacked | three across | three across |
| Product media | full-bleed carousel, dots below | as small phone | carousel with thumbnail rail | carousel with thumbnail rail |
| Buy box | below media, sticky action bar | as small phone | beside media | beside media |
| Collection grid | one or two columns | two | three | up to four, chosen by the visitor |
| Cart | stacked cards per line | stacked | table | table |
| Footer | accordion groups | accordion | columns | columns |

The sticky action bar on phones never covers the end of the page. When the hero is too narrow for
the dial's numerals to stay legible, the watch illustration shows alone and the interactive dial moves
to its own full-width block beneath the copy. Everything reflows to one column at 400 percent zoom
without sideways scrolling.

### Imagery drawn from code

This is a zero-asset build: the shop ships no product photography, no ghost plate images, no video and
no font files from elsewhere, and each is a substitution drawn or served by the app itself. No tiling
noise or grain texture is added. Each watch image is drawn per colourway: a soft vertical ground in the
case's family, a blurred warm contact shadow, a rounded case with a gradient from its case tone to its
darker case tone, tapering straps above and below with a faint weave, the crown on the **left** edge
with fine knurling, and a soft highlight across the crystal, with the drawn dial composited into the
case. Straps, the tote, the beanie and bundles get a drawn silhouette on a soft ground in a palette
colour, seeded from the product so the same product always yields the same picture.

## Constraints

One shop, one currency (`usd`), one shipping country (`US`). No market or country selector, no
presentment currencies, no tax or duty quotes and no landed-cost estimate. No card handling, no
wallet button, no refunds, no payment methods and no discount codes; the only promotion is the gift
with purchase. No warranty claims, no returns desk, no serial numbers, no fulfilment or tracking, no
carrier integration and no packing. No compliance certificates. No staff role besides the owner and no
approval chain. No newsletter, no marketing email, no pop-up overlays, no shoppable or lifestyle
video, no press ticker, no recently viewed rail and no product structured data. No child account, no
child profile and no field for a child's name, age or birthday. No photo uploads with reviews and no
file uploads anywhere. No automated agent checkout surface. No external network calls at runtime
beyond the three named backing services. No native application.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`.
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
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

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "name"}` | `{"access_token"}` |
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `POST /api/auth/link` | `{"email", "return_to"}` | `{"status": "sent"}` |
| `POST /api/auth/link/consume` | `{"token"}` | `{"access_token", "return_to"}` |
| `POST /api/auth/link/resend` | `{"token"}` | `{"status": "sent"}` |
| `GET /api/account` | none | `{"email", "name", "role"}` |
| `PATCH /api/account` | `{"name"}` | the account |
| `GET /api/policies` | none | `returns_window_days`, `warranty_years`, `minimum_age_years`, `flat_shipping`, `currency` |
| `GET /api/collections/<handle>` | `family`, `colourway`, `case_size`, `availability`, `price_band`, `sort` | `handle`, `title`, `notice`, `count`, `counts_reflect`, `facets`, `sort_options`, `products` |
| `GET /api/products/<handle>` | none | one product |
| `GET /api/search` | `q` | a top-level JSON array of products |
| `GET /api/products/<handle>/reviews` | `rating` | a top-level JSON array of published reviews |
| `POST /api/products/<handle>/reviews` | `{"rating", "title", "body", "mentions_minor"}` | the review, `pending` |
| `POST /api/products/<handle>/restock-subscriptions` | `{"email"}` | `{"product": "<handle>", "email", "status": "waiting"}` |
| `POST /api/cart` | none | the cart with its `token` |
| `GET /api/cart` | `X-Cart-Token` header | the cart |
| `POST /api/cart/lines` | `X-Cart-Token` header, `{"sku", "quantity"}` | the cart |
| `PATCH /api/cart/lines/<id>` | `X-Cart-Token` header, `{"quantity"}` | the cart |
| `DELETE /api/cart/lines/<id>` | `X-Cart-Token` header | the cart |
| `POST /api/checkout` | `X-Cart-Token` and `Idempotency-Key` headers, `{"shipping_address"}` | the order |
| `GET /api/orders` | none | a top-level JSON array of the account's orders |
| `GET /api/orders/<number>` | none | one of the account's orders |
| `GET /api/owner/reviews` | `status` | a top-level JSON array of reviews |
| `POST /api/owner/reviews/<id>/publish` | `{"basis"}` | the review |
| `POST /api/owner/reviews/<id>/reject` | `{"policy_clause"}` | the review |
| `POST /api/owner/reviews/<id>/reply` | `{"body"}` | the review with its `reply` |
| `GET /api/owner/stock` | none | a top-level JSON array of stock rows |
| `POST /api/owner/stock-adjustments` | `{"sku", "delta", "reason"}` | `sku`, `on_hand`, `reserved`, `available` |
| `POST /api/support-requests` | `{"name", "email", "subject", "message"}` | `{"reference", "queue"}` |
| `GET /api/health` | none | `200` |

Bearer authentication is carried on the account, order, checkout, review-writing and owner
endpoints. The catalogue, cart, restock, support, policy, search and health endpoints need no token.
A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as
a client error, never as a server error and never as a silent success. The one exact status the shop
pins is `404` for an order the account cannot see.

**No mocks.** An in-memory stock counter, a cart held only in the browser, an order number the app
prints without writing an order, an invoice total kept in the app's own table instead of raised in
Kill Bill, a hardcoded confirmation the app hands back to itself, or an email written to a file on
the app container instead of handed to the mail server: each of those is a contract violation. The
named providers are the fact. The app's pages and its own tables can only reflect what lives in
`postgres`, what was billed in `killbill` and what was handed to `mailpit`, never substitute for it.

## Definition of done

A visitor can set and run a tock on a working dial, compare the two dials with one slider, choose a
watch or a bundle, and check out as a signed-in customer, receiving an order page and a confirmation
email while that order's own invoice, for its total, exists on the buyer's Kill Bill account.
