# Havenn

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, search a named place
for a set of dates and a party, open a listing, read the complete price before agreeing to it,
and confirm a reservation that holds those nights and authorises the money, without hitting an
error page. Two strangers who press confirm at the same instant for the same listing and the
same nights must not both succeed: exactly one reservation exists afterwards and the other
caller is told the nights have gone. The reservation and its authorisation must be real rows in
`postgres` that survive a restart, and the amount authorised must equal the total the guest was
shown; a receipt the app draws for itself does not count.

## Overview

Havenn is a two-sided marketplace for short-stay accommodation. Guests search by place and
dates, compare listings against a map, read a listing's terms and reviews, and reserve. Hosts
publish listings, control which nights are open and what each night costs, accept or decline
requests, and are paid after the guest arrives. The category bar carries `All`, `Homes`,
`Experiences` and `Services`, so one search, one booking flow, one payment path and one review
system serve three inventory types; only stays carry a full booking flow in this build, and the
other two carry inventory type and route.

Five audiences arrive and each wants something different. A guest with a place and dates
already in mind wants availability and price. A guest browsing wants inspiration and
inventory. A guest who has already booked wants trip details, messages and changes. A host
wants a calendar, a price and a payout. A search engine wants a crawlable link surface, which
is what the home route's link grid is for.

The visible product is a few dozen components. The product's real difficulty is underneath it:
a transaction across scarce inventory, money, time zones and two parties whose interests
oppose. Guests and hosts are fighting over the same night in the same room, and the system is
what arbitrates. Two guests can press confirm four milliseconds apart, both see the nights
free, and both be charged. Preventing that is the hardest single requirement here, and it
cannot be arranged by checking availability and then writing the reservation.

Three decisions in the shape of the data carry most of the risk. A stay's dates are local
calendar dates in the listing's own timezone, never the guest's and never UTC. A stay is a
half-open range, so the third to the fifth is two nights and a departure on the fifth does not
clash with an arrival on the fifth. Every amount is an integer in its currency's minor unit,
with the exponent read from a currency table, because not every currency has two minor digits.

Havenn deliberately is not: a native application, a photography host, a card acquirer, a map
tile vendor, a tax vendor or a foreign-exchange feed. It ships no photograph, no video and no
font file, and it makes no network call at run time. What would be a third-party service in a
larger product is an in-product component here, with the same observable contract.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Anonymous visitor | Browse the home route, run a search, open a listing, read published reviews, read the terms page, see a listing's approximate location | **Cannot reserve, message, review, wishlist, or read any exact address** |
| `guest` | Everything a visitor can, plus reserve, cancel, message a host about their own reservation or inquiry, keep wishlists, review a stay they completed, and read their own trips, receipts and exact addresses once confirmed | **Cannot read another guest's reservations, threads, wishlists or receipts. Cannot read or write any listing, calendar, reservation or payout belonging to a host. Cannot read a review that is not yet published unless they wrote it** |
| `host` | Everything a visitor can, plus create, edit, publish, snooze and unlist their own listings, set per-date availability and price, accept or decline requests for their own listings, message their own guests, and read their own reservations and earnings | **Cannot read or write another host's listings, calendars, reservations or payouts. Cannot read a guest's other trips or threads. Cannot see a guest's photograph or name on the accept-or-decline screen. Cannot cancel a confirmed reservation without stating a reason and confirming explicitly** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI
is not authorization: a direct API call from a `guest` session to any `host`-only endpoint must
be rejected by the server (an unauthorized request is denied, not served), leaving the
protected state unchanged. The same holds within a role: a request naming another user's
reservation, thread, wishlist, listing, calendar or payout is refused, and the refusal is
decided where the data is read rather than by the handler that happened to be written last.

Signup is open. Anyone can create a `guest` account, and any signed-in account can create a
host profile, which grants `host` on the listings it owns and on nothing else. A role is read
from the session, never from the request body.

Four accounts are seeded, every one with the password `deku-demo-pw-2026`:
`guest@example.com` and `guest2@example.com` as guests, `host@example.com` and
`host2@example.com` as hosts.

## Core features

### Auth

Email and password, hashed, with a bearer token returned at login and sent on every
authenticated request. Tokens expire; an expired token leaves the attempted action unperformed
and asks for sign-in again.

1. `POST /api/auth/signup` with `email` and `password` creates a guest account and returns a
   token. A signup reusing a seeded or existing address is rejected as invalid and creates no
   second account.
2. `POST /api/auth/login` with a seeded address and `deku-demo-pw-2026` returns a bearer token.
   A wrong password is denied and returns no token.
3. Every route below except signup, login, `GET /api/health` and the payment webhook receiver
   requires a bearer token. A request without one is denied.

### Search

The front door is one control in three segments over a submit: `Where` with the placeholder
`Search destinations`, `When` with `Add dates`, `Who` with `Add guests`. `Where` opens a
destination panel offering recent searches, nearby places and typeahead. `When` opens a
two-month calendar supporting a date range, flexible dates and a month-length mode. `Who`
opens a stepper counting adults, children, infants and pets separately.

4. The three segments produce one query and **that query is the address**. A search is fully
   reconstructible from its URL: `place`, `checkin`, `checkout`, `adults`, `children`,
   `infants`, `pets`, `min_price`, `max_price`, `room_type`, `amenities`, `instant_book`,
   `cursor` and `sort`. Copying the address into a fresh session reproduces the same results.
   A search whose state lives only in the page is a defect: it loses shareable searches, the
   back button and every organic entry point at once.
5. Guests are four classes, not one number. An adult and a child each count toward occupancy
   and each charge above the listing's included-guest threshold. An infant counts toward
   neither. A pet counts toward neither occupancy nor the guest threshold, charges its own fee
   once per stay, and is refused on a listing that does not allow pets. Booking two adults, two
   children, one infant and one pet against a listing of capacity `4` with `2` guests included
   succeeds, counts occupancy as `4`, charges the extra-guest fee for `2` guests per night, and
   charges the pet fee once.
6. `GET /api/listings` answers a conjunction of four filters: a geographic bounding box, real
   availability across the whole range, attributes (`room_type`, `amenities`, capacity,
   `instant_book`), and **the total for those dates**, not the nightly rate. It returns an
   object carrying `results`, `next_cursor`, `total_estimate` and `partial`. The bounding box
   is authoritative, not the place name: a guest who searches a city and then moves the map is
   no longer searching that city, and the address reflects the box. A box that crosses the
   antimeridian, running from a longitude near `+180` to one near `-180`, is two degrees wide
   and must return the listings inside it rather than none or all of them. Distances are
   computed on a sphere.
7. Availability is part of the answer to the query, never a filter applied to its result. In an
   area holding twenty thousand listings of which two hundred are available for the range, a
   request for twenty results returns twenty, in one round trip, within the response budget. A
   page that comes back sparse, or a result count that disagrees with what a guest can open, is
   the defect this rule names. The price filter compares against the real total for the
   queried dates, which depends on per-date rates, discounts, fees and taxes, so a bound
   sufficient to exclude a listing must never exclude one that would have qualified.
8. Pagination is by `cursor` and never by offset. The cursor carries the sort key of the last
   returned item, the listing id as a tiebreaker, a fingerprint of the query and the time the
   search was issued. Inventory changes while a guest browses, so an offset skips results and
   repeats others and the guest cannot know. Booking a listing that ranked above the page-one
   boundary and then requesting page two must neither hide a result nor repeat one. A cursor
   issued against a different query is rejected as invalid rather than reinterpreted.
9. Four search states are distinct and all four are built. No results for the query shows the
   query back and offers to relax the dates or widen the map. No results because a filter is
   too narrow names the filter that excluded the most and offers to drop it. The search
   component being unavailable says so, because an empty grid tells the guest there is no
   inventory at all. Partial results render what arrived and mark the set incomplete.
10. The map and the grid are two views of one result set and stay synchronised. Hovering a card
    highlights its pin; moving the map re-queries. Pins cluster below a zoom threshold. A pin's
    label carries the **total for the query's dates**, never the nightly rate: a low number on
    the map beside a higher one on the card is a bait-and-switch and is rejected here.

### Listing detail

`/rooms/<id>` carries, in this order: a photo grid of one large image plus four opening a
full-screen viewer; the title, then the place, then a rating summary; a host strip with name,
avatar, superhost marker and hosting duration; three to five highlight rows; a truncated
description with a `Show more` that opens a dialog; a truncated amenity grid with a full
dialog; a two-month availability view; the booking panel; reviews; the location circle; a host
section with response rate and response time; and a `Things to know` block carrying house
rules, safety and the exact cancellation policy.

11. The booking panel shows the **complete breakdown before the guest commits**, itemised as
    `nightly_subtotal`, `length_of_stay_discount`, `cleaning_fee`, `extra_guest_fee`,
    `pet_fee`, `guest_service_fee`, `taxes` and the total. A panel showing a nightly rate and
    revealing fees at checkout is the defining dark pattern of this category and is not built
    here.
12. With no dates in the query the panel shows the nightly rate labelled as a from-price and
    **no total**. A total without dates is a lie, because the cleaning fee is charged once per
    stay while the nightly rate is not. The total appears the moment dates exist.
13. The availability view shows three states per date, not two: available; unavailable; and
    available but not as a check-in. The third is real and is the one usually missed. The view
    renders the result of the availability rules, never the raw diary.
14. Two reservation modes exist and the page says without ambiguity which applies. Under
    instant book a reservation is created and confirmed on payment authorisation. Under request
    to book a reservation is created `pending`, the nights are held, payment is authorised and
    **not captured**, and the host has a bounded window to accept.
15. Before the booking control, and not after it, the page carries the cancellation policy in
    plain words with its real dates computed for this query, the house rules, the total price,
    and the review count with its rating.

### Pricing

16. The nightly subtotal is the sum of each date's own price across `[checkin, checkout)`,
    taking the calendar day's `price_minor` where the host set one and the listing's base price
    otherwise. It is never nights multiplied by a base price: hosts price weekends, holidays
    and seasons differently, and a stay crossing a price change is then wrong.
17. The length-of-stay discount applies **to the nightly subtotal alone**, never to fees and
    never to taxes. Twenty-eight nights or more take the monthly rate, seven or more take the
    weekly rate, fewer take none.
18. Fees: the cleaning fee is a **per-stay fee**, charged once per stay and identically on a
    two-night and a thirty-night booking. Folding it into the nightly rate breaks it, because a
    month-long stay then carries it thirty times over and the monthly discount compounds the
    error. The extra-guest fee is charged per extra guest per night, where extra
    guests are adults plus children above the included threshold and exclude infants and pets.
    The pet fee is charged once per stay when the party carries a pet.
19. The guest service fee is a rate over the accommodation total, which is the discounted
    nightly subtotal plus the cleaning fee plus the extra-guest fee plus the pet fee.
20. Lodging tax is a calculation with a jurisdiction in it. Taxes come from a
    jurisdiction-aware component holding a stored table, never a hard-coded rate. A hard-coded
    percentage produces systematic under-collection or over-collection, with the liability
    attaching to the platform. Jurisdictions differ in what they tax, in form (a percentage, a flat amount per night,
    or a flat amount per person per night), in whether they cap after a number of nights, in
    whether long stays are exempt, and in who remits. Taxes are returned as itemised lines with
    names and are stored on the quote. A jurisdiction exempting stays of thirty nights and over
    charges tax on a twenty-nine-night stay and none on a thirty-night one, which is exactly
    where a hard-coded rate is most wrong and most expensive.
21. **Pricing is not commutative and the order is fixed.** Compute, in this order: the nightly
    subtotal; the discount; the discounted subtotal; the cleaning fee; the extra-guest fee; the
    pet fee; the accommodation total, being the discounted subtotal plus those three fees; the
    guest service fee over that accommodation total; the taxes; and the total, being the
    accommodation total plus the service fee plus the taxes. The discounted subtotal and the
    accommodation total are not displayed and must still exist as named values, because the
    later lines depend on them.
22. Rounding is half up, away from zero, to a whole minor unit, at **every** multiplication and
    immediately. Lines are summed after rounding, never summed unrounded and rounded once. The
    displayed total equals the sum of the displayed lines exactly: a guest who adds the lines up
    by hand gets the total. Where they disagree it is the breakdown that is wrong, not the
    total.
23. A quote is created at entry to checkout and for display on the listing page. It carries
    `quote_id`, the echoed inputs, every line item, `total_minor_units`, `currency`, `fx_rate`,
    `fx_pinned_at`, `expires_at` and `policy_snapshot`. Its rate inputs and its exchange rate
    are pinned at creation and honoured for its lifetime, which is read from `QUOTE_TTL_SEC`
    and is short, typically minutes: long enough to finish checkout and short enough that the
    price stays honest. The same
    inputs within that lifetime return the same quote. An expired quote is recomputed, and where
    the total changed the guest is told and consents again. A quote is consumed on reservation
    creation and is never reusable.

### Availability and reservations

24. **A stay is a half-open interval of local calendar dates,** `[checkin, checkout)`. The
    checkout day is not occupied. Nights are `checkout - checkin`, so the third to the fifth is
    two nights. Ranges may touch: a departure on the fifth and an arrival on the fifth are both
    legal on one listing and must not be refused. An overlap is refused. Getting this wrong in
    one direction costs the host a booking on every turnover day; in the other it puts two
    parties in one house.
25. **Exactly one reservation wins.** Fifty simultaneous confirm requests for one listing and
    one identical range produce exactly one reservation and forty-nine refusals naming the
    conflict, every time, and the refusals leave no partial state behind: no orphaned row, no
    night left marked taken, no authorisation held. This must hold under real concurrency, and
    reading availability and then writing the reservation does not achieve it, because another
    caller commits between the two.
26. Six availability rules are all evaluated, and a date being free satisfies only the first:
    `is_available`, the host has not blocked it; `min_stay`, a range starting here shorter than
    this is invalid; `max_stay`, a range longer than this is invalid; `closed_to_arrival`, the
    date is bookable but may not start a stay; `closed_to_departure`, the date may not end one;
    and `preparation_days`, the nights blocked after each checkout. Two further rules bound the
    calendar: `advance_notice`, the minimum lead time before check-in, evaluated against the
    listing's own current local time; and `availability_window`, how far ahead the calendar is
    open, beyond which dates do not exist yet. A listing with one preparation day forbids the
    back-to-back arrival that rule 24 otherwise permits, and which behaviour applies is that
    listing's setting rather than a product-wide choice.
27. A `pending` reservation holds inventory exactly as a `confirmed` one does. It expires at a
    bounded deadline read from `PENDING_HOLD_TTL_SEC`, or at check-in, whichever comes sooner.
    **An expired hold never counts against availability**, including when nothing has read that
    reservation since it expired: a guest querying those nights afterwards finds them free.
    `POST /api/maintenance/release-expired-holds` sweeps them, is idempotent, is safe to run
    twice at once, and releases each authorisation it releases. Both parties are notified. An
    expiry evaluated only when somebody happens to read the reservation blocks a host's calendar
    with requests nobody completed, and the host never learns why the bookings stopped.
28. A reservation stores a **copy** of the cancellation policy in force when it was created, as
    `policy_snapshot`, and a copy of its priced quote as `quote_snapshot`. A host who changes
    their policy from flexible to strict does not thereby change the terms of a stay already
    sold. A reservation booked under a flexible policy whose listing then moves to strict is
    refunded under flexible. Storing a pointer to the listing's current policy rewrites history,
    and the guest discovers it only when they try to cancel. What was sold is what was sold.
29. A cancellation policy is an ordered schedule of refund tiers, each a threshold relative to
    check-in **in the listing's timezone**: a grace period giving a full refund within a number
    of hours of booking when check-in is far enough away; a tier giving a full refund of the
    accommodation total before a threshold; a tier giving a partial refund between thresholds; a
    tier giving none after the final threshold; and the service fee, treated separately and
    retained after the grace period. `GET /api/reservations/{id}/refund-quote` computes the
    refund from the stored snapshot against the listing's local time, stores its inputs
    alongside its result, and **is shown to the guest before they confirm the cancellation**. A
    cancellation after the host has been paid records a recovery against future payouts.

### Checkout

`/book/stays/<id>` is a route of its own, reached with a listing, dates and a party already
chosen.

30. On arrival the system **re-prices and re-checks availability**. What the guest saw on the
    listing page may be hours old. Where the new quote differs from the old one the difference
    is surfaced and the guest consents again. Charging a number other than the one displayed is
    not an option.
31. `POST /api/reservations` carries an `Idempotency-Key` header generated by the client and
    scoped to the user. The same key replayed, whether at the same instant or an hour later,
    returns the original result byte for byte and creates no second reservation and no second
    authorisation. Without this, a double tap, a retried request or a browser resubmit produces
    two reservations and two charges. Keys are retained at least as long as any retry may
    arrive.
32. Five failures are handled explicitly, each on its own path rather than by one error
    handler. The nights were taken between quote and confirm: fail cleanly, hold nothing, say
    so, offer alternatives. Authorisation declined: no reservation, hold released at once.
    Authorisation succeeded but the reservation write failed: **the authorisation is voided**,
    because money held against a booking that does not exist is the worst outcome available.
    The payment component answered with an unknown outcome: do not retry blindly, reconcile by
    the idempotency key and void anything that succeeded. The guest abandoned: the quote
    expires and any hold is released.
33. Before the confirm control the guest is shown the total, the currency that will actually be
    charged named **in words as well as in symbol** where it differs from the display currency,
    the cancellation policy with real dates, the check-in and check-out times in the listing's
    timezone, and what happens next in each of the two booking modes.

### Payment, payouts and money

Havenn holds no card number, no security code and no bank detail. Payment instruments are
represented by an opaque `provider_reference` minted by the in-product payment component, and a
request carrying a card number anywhere is rejected as invalid. The component accepts four
deterministic instrument references: `pm-ok-4242` authorises then captures cleanly;
`pm-decline-0002` is declined at authorisation; `pm-challenge-3184` authorises only after an
interactive challenge, answering `requires_action` first; `pm-capture-fail-0005` authorises
cleanly then fails at capture. Each reference behaves the same way on every call.

34. Authorising is not charging. Under instant book the authorisation and the capture both
    occur at confirmation. Under request to book the authorisation occurs at confirmation and
    the capture occurs **on host acceptance and never before**. A declined or expired request
    voids the authorisation and captures nothing. An authorisation has a lifetime; a request
    window longer than it requires re-authorisation, and that path exists.
35. **Inventory is arbitrated first and money second.** The reservation is written and the
    conflict decided before any authorisation is attempted; where the nights are gone no money
    has moved. On authorisation success the reservation is committed. On failure nothing
    remains: no reservation and no hold. On an unknown outcome the reservation does not remain
    either, and a reconciliation records itself against the idempotency key and voids any
    authorisation that did succeed. The reverse ordering takes money and then discovers the room
    is gone.
36. Three currencies exist and conflating any two is a defect. The listing currency is what the
    host prices in and is authoritative for their pricing. The display currency is what the
    guest chose to see. The settlement currency is what is actually charged. Conversion uses a
    rate pinned on the quote with `fx_pinned_at` and honoured for its lifetime. A search of
    forty results uses one rate, not forty. The rate and its timestamp are stored on the
    reservation permanently, because a refund months later reconstructs the original conversion.
37. A payment may require an interactive challenge, so `POST /api/reservations` may answer
    `requires_action` rather than success or failure. The reservation exists holding inventory
    while the challenge is outstanding, under a short deadline, and the hold is released if the
    challenge is abandoned. A checkout that assumes confirm returns a final answer does not work
    at all where a challenge is required, rather than working less well.
38. `POST /api/payments/webhook` receives payment events. Events arrive out of order, arrive
    more than once, and sometimes do not arrive. State is never derived from arrival order:
    handlers read the event's own timestamp and the component's current object state, are
    idempotent on the event id, and a scheduled reconciliation exists because webhooks are not
    the only path. Delivering `succeeded`, then `refunded`, then `succeeded` again with their
    original timestamps leaves the payment refunded. Delivering each twice changes nothing. The
    receiver authenticates by signature and never by a user token.
39. Payouts follow the check-in date **in the listing's timezone**. Nothing is paid at
    confirmation. A payout becomes eligible after a hold period following check-in, is released
    to the host minus the host service fee, is cancelled where the guest cancels first, and is
    recovered where the guest cancels after release. A payout released early because of a
    timezone error is a real loss.
40. Refunds run against the captured amount in the settlement currency. A partial refund is
    computed from the policy snapshot, itemised and stored. A chargeback is never silently
    absorbed: it freezes the related payout, records the dispute and notifies. Where exchange
    rates moved, a refund may not equal the original charge in the guest's currency and the
    product says so rather than hiding it.

### Trips, messaging, wishlists, reviews and account

41. `/trips` lists reservations in three groups: upcoming, current and past. A trip detail
    carries the itinerary, the address released per rule 47, check-in instructions, the host
    contact, the receipt, and the cancellation control with its live refund quote.
42. A thread is scoped to one reservation or one inquiry, **never to a pair of users**. Contact
    details typed into a message before a booking is confirmed, phone numbers and email
    addresses alike, are redacted **server-side, on write and on read**. Client-side redaction
    is decoration. Attachments are typed and scanned. Threads carry delivery and read state,
    honour quiet hours in the recipient's timezone, are rate limited, and retain full history,
    because disputes depend on it. Redaction is an anti-circumvention control with a trust-and-safety purpose rather than a
    commercial one: moving a booking off-platform removes the payment protection, the
    cancellation terms, the record of what was agreed and the ability to intervene in a safety
    incident. Off-platform circumvention is what the rule exists to prevent, and describing it
    that way in the interface is more honest than silence.
43. A wishlist is a named collection of listings, private by default and shareable by link. A
    wishlist entry stores the listing **and the dates it was saved under**, because a price
    without dates means nothing.
44. **Reviews are double-blind.** Only a party to a completed stay may review it. A guest
    reviews the host and the listing; a host reviews the guest; the two are separate records.
    One review per reservation per direction. The window is bounded after checkout. **Neither
    review is visible to anyone until both are submitted or the window closes.** Editing closes
    at publication, and one public response per review is allowed afterwards. The gate belongs
    where reviews are fetched, not where they are drawn: a review with no `published_at` must
    not leave the server to anyone but its author, and hiding it in the page while still
    sending it is not implementing this at all. Its purpose is to stop retaliation, because a
    host who can read a guest's review before writing their own makes honesty cost the guest
    their reputation.
45. Rating aggregates count published reviews only, are recomputed on publication rather than
    on submission, average each subrating independently across `cleanliness`, `accuracy`,
    `checkin`, `communication`, `location` and `value`, are withheld below a minimum count
    because one review is not a rating, and are stored rather than computed on every read.
46. `/account` carries the profile, payment methods, payout methods, notification preferences,
    privacy and data export, and login security. Language, region and display currency are
    **three independent settings**. Language drives interface strings and date and number
    formatting and never prices. Region drives tax treatment, legal notices and the default
    currency and never language. Display currency drives the amounts shown and never the
    settlement currency. A guest reading Japanese, resident in Germany and paying in dollars is
    an ordinary customer and must be able to say so.

### Trust, location and fairness

47. Before confirmation a listing discloses an approximate circle, offset from the true point
    by a vector that is **stable per listing** and **stored**, not derived at read time. A
    circle that moves between visits lets anyone average a few visits and find the house. Exact
    coordinates and the exact address are released only after confirmation, and only to that
    reservation's guest and host. Exact coordinates are never sent to an unauthorised client in
    any field, including one the interface does not draw, because anything sent to a browser can
    be read.
48. The accept-or-decline screen does not show a guest's photograph or name. Ranking uses no
    protected characteristic and no proxy for one. Declines are logged with their reasons and
    the pattern is queryable. The footer carries an `Anti-discrimination` link, so the policy is
    a named surface of the product and not only a document.
49. Ranking is versioned and logged per query, so an experiment is measurable and a complaint
    is answerable, and any paid placement is labelled where it exists.
50. Auditability is a product requirement here rather than an operational nicety.
    Reservations, payments, payouts, refunds, policy snapshots and cancellations are
    append-only. A correction is a new record, never an update in place, and the state of any
    reservation at any past instant is reconstructible.

### Host surfaces

51. A listing has a lifecycle: `draft`, `in_review`, `listed`, `snoozed`, `unlisted`.
    **Unpublishing a listing does not cancel its existing reservations.** Taking a listing off
    the market and cancelling its bookings are two different actions, and the obvious
    implementation of the first performs the second, leaving people with flights nowhere to
    stay.
52. `/host/calendar/<id>` edits per-date availability and per-date price, the base price, the
    per-date minimum and maximum stay, the advance notice, the preparation time, the
    availability window, and the weekly and monthly discounts. A change appears in its row
    immediately and is reverted with a message naming the field if the save fails.
53. A host may import an external calendar feed, whose blocks are stored as imported blocks and
    are authoritative where present. The last successful synchronisation time is shown to the
    host. Feeds are polled rather than pushed, so there is always a window in which two
    platforms both believe a night is free; that window cannot be closed. Where a late block
    arrives covering nights already confirmed, the system raises a conflict for a person to
    resolve and **never auto-cancels a confirmed booking**.
54. `/host/reservations` lists reservations ordered by check-in. A host accepts or declines a
    request within the response window, messages the guest, and may cancel with a stated reason.
    Accepting captures the authorisation; declining voids it and frees the nights. Cancelling a
    confirmed reservation requires an explicit confirmation and records its consequence.
55. `/host/earnings` shows scheduled and released payouts with the reservation each belongs to,
    the host service fee deducted, and any recovery outstanding.

### Public surfaces

56. Four strings are global and appear on every route that carries chrome: the wordmark's
    alternative text reads `Havenn`, the home route's heading reads `Havenn homepage`, the skip
    link reads `Skip to content`, and the home route's title reads `Havenn | Holiday rentals,
    cabins, beach houses & more`. The home route carries the search control over the page
    ground, then several horizontally
    scrolling inventory carousels of listing cards, then the link grid, then the footer. Each
    carousel is titled, shows between two and six cards depending on width, is keyboard
    scrollable, does not trap focus, announces its position, and fetches lazily beyond the first
    screen.
57. The link grid is headed `Inspiration for future getaways` and carries six tabs: `Popular`,
    `Arts & culture`, `Beach`, `Mountains`, `Outdoors` and `Things to do`, with a `Show more`
    control that expands it. Each cell is a place name over a rental type, drawn from `House
    rentals`, `Villa rentals`, `Cabin rentals`, `Cottage rentals`, `Flat rentals`, `Apartment
    rentals`, `Holiday rentals` and `Monthly Rentals`, and every cell links to a pre-applied
    search. Measured pairs include `Dallas / House rentals`, `North Myrtle Beach / Villa
    rentals`, `Portland / Cabin rentals`, `Nice / House rentals`, `Galveston / Cabin rentals`,
    `Amsterdam / Cottage rentals`, `Barcelona / Flat rentals`, `Kauai / Flat rentals`,
    `Minneapolis / Holiday rentals`, `Raleigh / Villa rentals`, `Gulf Shores / Monthly Rentals`,
    `Philadelphia / Flat rentals`, `Orange Beach / House rentals`, `Tokyo / Villa rentals`,
    `Cleveland / Holiday rentals`, `St. Petersburg / Cottage rentals`, `London / Cabin rentals`,
    `Kyoto / Apartment rentals`, `Charleston / House rentals`, `Key West / Flat rentals`,
    `Oahu / Holiday rentals`, `Brooklyn / Apartment rentals`, `Madrid / Holiday rentals`,
    `Savannah / Cottage rentals`, `Manhattan / Monthly Rentals`, `Pocono Mountains / Villa
    rentals`, `Milan / House rentals`, `Athens / Apartment rentals` and
    `Nashville / Monthly Rentals`. `Monthly Rentals` is title-cased where every sibling is
    sentence-cased, and it stays that way. **The grid is present in the markup the server
    sends**: it is the product's organic search surface, and a grid that only appears after the
    page runs in a browser is worth nothing.
58. An unknown address renders Havenn's own **not-found** view and answers not found. It carries
    the wordmark, the display line `Oops!`, the subtitle
    `We can't seem to find the page you're looking for.`,
    the code `Error code: 404`,
    the lead-in `Here are some helpful links instead:`,
    and the links `Home`, `Search`, `Help`, `Traveling on Havenn`,
    `Hosting on Havenn`, `Trust & Safety` and `Sitemap`. A failure inside the product renders the
    server-error view: `Oops!`, the subtitle `Well, this is unexpected...`, the code
    `Error code: 500`, the body
    `An error has occurred and we're working to fix the problem! We'll be up and running shortly.`, and the escalation `If you need immediate help from our
    customer service team about an ongoing reservation, please contact us. If it isn't an urgent
    matter, please visit our Help Center for additional information. Thanks for your patience!`.
    That escalation is kept: a generic error page on a product where people have travel booked
    is a failure of duty, and naming the ongoing-reservation case and routing it to a person is
    the right behaviour. Neither error route carries the header or the footer.
59. A **terms** page at `/terms` states the agreement between Havenn, its guests and its hosts,
    is reachable from the footer of every page, and is linked from the signup form. A help
    centre at `/help` and a sitemap at `/sitemap` exist alongside it. The footer carries three
    columns: `Support` with `Help Centre`, `Get help with a safety issue`, `HostShield`,
    `Anti-discrimination`, `Disability support`, `Cancellation options`
    and `Report neighbourhood concern`; `Hosting` with `Havenn your home`, `Havenn your experience`,
    `Havenn your service`, `HostShield for Hosts`, `Hosting resources` and `Community forum`;
    and `Havenn` with `2026 Summer Release`, `Newsroom`, `Careers`, `Investors` and
    `Havenn.org emergency stays`, the last naming the affiliated relief nonprofit that runs
    them.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home: the search control, inventory carousels, the link grid, the footer | Public |
| `/s/<place>/homes` | Search results for stays, grid and map | Public |
| `/s/<place>/experiences` | Search results for experiences | Public |
| `/rooms/<id>` | Listing detail and the booking panel | Public |
| `/book/stays/<id>` | Booking and checkout | `guest` |
| `/trips` and `/trips/<id>` | Trips in three groups, and one itinerary | `guest` |
| `/messages` and `/messages/<thread>` | Threads and one thread | `guest` or `host` |
| `/wishlists` and `/wishlists/<id>` | Saved listings and one collection | `guest` |
| `/reviews/<reservation>` | Review submission for a completed stay | `guest` or `host` |
| `/account` | Profile, payment and payout methods, notifications, privacy, security | `guest` or `host` |
| `/host/listings` and `/host/listings/<id>` | Listing management and one listing | `host` |
| `/host/calendar/<id>` | Availability and pricing for one listing | `host` |
| `/host/reservations` | Reservations ordered by check-in | `host` |
| `/host/earnings` | Scheduled and released payouts | `host` |
| `/help`, `/sitemap`, `/terms` | Static pages | Public |
| `/404`, `/500` | Not-found and server-error views | Public |

The service prefixes a bundle scan turns up are not pages and no route is built for them.

**Entry and redirects.** An anonymous visitor who opens a `guest` or `host` route is sent to
sign-in and returned to the route they asked for once signed in. Signing in with no pending
destination lands on `/`. Signing out returns to `/`. A token that expires mid-action leaves
the action unperformed, says so, and asks for sign-in again; the guest does not lose what they
had entered. A `guest` who opens a `host` route, or a `host` who opens another host's listing,
calendar, reservation or payout, is refused by the server and shown a refusal rather than an
empty page.

**Journeys.**

1. *Search and reserve.* Open `/`. Type `Portland` into `Where`, pick a two-night range in
   `When`, set two adults in `Who`, submit. Land on `/s/portland/homes` with every parameter in
   the address. Move the map; the address follows the box. Open `Cedar Loft`. Read the
   breakdown: the nightly line, the cleaning fee, the service fee, the taxes and the total.
   Press reserve, land on `/book/stays/<id>`, see the re-priced quote, confirm. The reservation
   appears under `/trips` as upcoming, its receipt shows the same total, and the nights are gone
   from the listing's availability.
2. *Request to book.* The same up to confirm on `Harbour Cottage`, which is request to book. The
   reservation appears as pending, the nights are held, and the receipt shows the money
   authorised and not taken. Sign in as `host@example.com`, open `/host/reservations`, accept.
   The reservation becomes confirmed and the capture follows.
3. *Two guests, one room.* `guest@example.com` and `guest2@example.com` confirm the same range
   on `Salt Marsh Cabin` at the same moment. One lands on a confirmed reservation. The other is
   told the nights have gone and is offered alternatives, with nothing held and nothing charged.
4. *A host day.* Sign in as `host2@example.com`, open `/host/calendar/<id>` for `Kite House`,
   block a date and set a nightly override on another; both rows change as they are pressed.
   Open `/host/listings`, snooze `Kite House`; its confirmed reservations survive untouched.
5. *Cancel.* Open a trip under `/trips`, press cancel, read the refund quote computed against
   the policy stored on the reservation and the listing's local time, then confirm. The refund
   is itemised and stored, and the nights return to the calendar.

**States.** Every list has an empty state that says what would fill it: no trips yet, no
messages yet, no wishlists yet, no reservations yet, no payouts yet. Every route has a loading
state, and the results grid keeps its place and its focus while more results arrive. Search
carries the four states of rule 9 rather than one blank grid. A failure anywhere renders the
server-error view rather than crashing, and a bad address renders the not-found view.

## UI/UX notes

The north star: somebody arriving should understand within a moment that this is a place to
find somewhere to stay, and should be able to say where, when and how many without reading
anything first. The register is consumer marketplace, so the subject, a place to stay, is the
first thing seen, and atmosphere is carried by photography and by space rather than by
decoration. Because the product asks for money from strangers it also has to reassure: the
surfaces where a guest is deciding are still, generously spaced and free of anything that moves
during the decision. **Calm over expressive, and space over dividers.** A competing product
could rationally invert both and be right; this one does not.

The palette is stated by role and the exact values are yours, so long as each role's rule
holds. One ink carries all primary text and all icons. A lighter grey carries secondary text,
inactive tabs and every piece of listing metadata. A third grey, between the two, carries
tertiary text. White carries card faces and reversed text. One legacy teal survives on the
error pages' links and appears nowhere else and is never extended. Three colours carry meaning
and are used for nothing else: one for something that has gone wrong and for a destructive
action, one mid, soft green for something that worked, and one warm orange for the review
star. Beyond those
there is a hairline, a border, a hover ground, a page ground and a disabled grey, and overlay
scrims are the neutral black at low opacity. Photographic overlays are a single transparent to
near-opaque vertical wash.

**One brand colour, and it is almost never seen.** It belongs to the search submit and to
nothing else in the product, and it should appear roughly two orders of magnitude less often
than the ink. On that one control it is not a flat fill but a six-stop radial glow running from
a light, vivid red at the centre out through mid, vivid magenta stops to a deep, soft violet at
the rim, and pressing it shifts the whole ramp two stops darker while keeping the same six-stop
structure. That is one definition with two palettes, not two definitions. Wide brand surfaces
carry the same ramp as a left-to-right run, mirrored rather than rotated for right-to-left
reading. A page dominated by the brand hue is the failure to avoid: restraint with it is the
design.

Type is one size for the whole interface, at three weights and three leadings, one step up for
form fields, and two display steps for section headings. That single size is the interface, and
this product's density comes from weight and from colour rather than from size variation, so
resist adding steps. Set the leadings as ratios rather than as fixed measures. Figures line up
in a column wherever amounts stack, which is every price breakdown, every receipt and every
payout row. The error pages are allowed the one register change in the product and carry the
largest type in it.

Corners are softened on one ladder of eight radii, from tiny through small, medium, large,
xlarge, xxlarge to xxxlarge; the only shapes outside it are the two round controls, the
category tab and the app-style pill. Elevation is six steps, and it grows in spread and never
in darkness: the flattest step is an inset hairline rather than a shadow, so a flat surface
gets an edge without changing its box, and every raised step opens with that same hairline. A
build that darkens a shadow to signal height reads wrong at every level. Five translucent
materials exist, named extra-thin, thin, regular, thick and extra-thick, and thickness means
the opacity of the ground rather than the strength of the blur: the thin one blurs the world
behind it the most and the thick one the least. Build them that way even though the ramp that
feels obvious is the other one, and give every material an opaque fallback ground that still carries
text. Layering is a small, disciplined set: a local band for in-component stacking, one step
for the header, one for its dropdowns, and one for modals.

Motion is physical, and springs rather than curves are what carry it. Anything a person
triggers settles the way a weighted object settles, and
the product shares one small family of these settles: three that arrive without overshoot and
three that overshoot once, all three by the same small amount, so the overshoot reads as one
house character rather than three. Everything else shares four easing shapes, one standard for
almost everything and a deliberately asymmetric pair for entering and leaving, where entering
leaves fast and settles long while leaving starts slow and accelerates away. The most repeated
transition in the product is the link hover, and what it animates is the thickness of the
underline rather than its colour: text-decoration-thickness, box-shadow and background-color
move together on the standard shape, and the height of an opening panel moves with them. Nothing animates because the page scrolled, with one
exception: the search control collapses into a compact pill once the page leaves the top and
expands again on click or on return to the top, and it is one component in two states rather
than two components that swap. Movement is generated rather than written out: adding a new
settle should take naming a weight, a stiffness and a damping and nothing else, and a product
where adding one means pasting a list of numbers has been built the wrong way round. A request
for reduced motion, grouped with slow-updating and non-updating displays, collapses every
settle to an instant state change, plays no entrance, stops carousels auto-advancing and cuts
map transitions rather than flying them.

Components carry states rather than measurements. Every control has a resting, pointed-at,
pressed, focused and unavailable state, and unavailable is never signalled by colour alone. The
one hover in the product is a background moving from nothing to the hover ground, and it is
applied only where a pointer exists so a tap does not leave a control stuck looking hovered.
Escape closes any panel without committing. A destructive action confirms first and states what
it will cost. Each page leads with one clear **primary action**, visually distinct from every
secondary one, and the search submit is that action on the home route.

Accessibility here is a floor rather than a finish, and it is stated as one. The product
commits to a light mode and designs it fully. Body text and its background meet the **WCAG** AA
contrast bar, and the greys are the risk: the lighter grey carries listing metadata and the
entire link grid and must not be used below the body size, where it fails. White on the brand
glow is checked against the lightest stop at the centre rather than against the average. Every
route has full **keyboard navigation** with a visible focus ring, labels on icon-only controls,
and meaning never carried by colour alone. Touch targets are comfortably sized. A skip link
reading `Skip to content` comes first in the document. The home route carries one real heading
reading `Havenn homepage`, and every route carries one heading naming itself. Landmarks are
present for the banner, the navigation, the search, the main region and the footer. The results
grid is a list rather than a table, filter chips are toggles carrying a pressed state, and the
category tabs are a tab list carrying selection state. Modals trap focus while open, restore it
on close, and close from the keyboard. The date picker moves by day with the arrow keys, by
month with the page keys, and to the ends of a week with home and end; it announces the
selected range as it changes and announces why an unavailable date is unavailable rather than
only styling it. The map is declared decorative and everything on it is reachable from the grid
beside it, because a map holding information that exists nowhere else is not acceptable. Result
count changes are announced and focus survives pagination. Listing photographs carry the
listing title once per card, gallery images are decorative with a count, host avatars carry the
host's name, category tab icons are decorative because the label carries the meaning, the
wordmark carries the brand name, ratings are read as their number rather than as stars alone,
and map pins carry price and listing name. Every field is labelled persistently, errors are
associated and announced, the price breakdown is a description list rather than a layout table,
the total is announced when it changes, and the currency is stated in words as well as in
symbol at the point of commitment.

The layout holds at every width between three tiers, narrow, middle and wide, and where the
two breakpoints between them sit is yours. Wide carries the full right cluster, the three search segments inline, the
category tabs inline and centred, up to four result columns, a persistent map panel, a booking
panel sticky beside the content and a six-column link grid. Middle keeps the right cluster and
the inline segments, drops to two result columns and three link-grid columns, and makes the map
a toggle. **At a narrow viewport** nothing overflows sideways and every navigation target stays
reachable: the right cluster becomes a fixed bottom bar carrying `Explore`, `Wishlists` and
`Log in` with the active item in the brand colour and the rest in the ink, the category tabs
become horizontally scrollable pills, results become one column, the map becomes a full-screen
toggle, the booking panel becomes a fixed bottom bar, and the link grid becomes one column. The
search control at that width is **a different interaction rather than a reflow**: a single pill
that opens a full-screen panel asking one question at a time and ending in an explicit search
action, which is the largest responsive difference in the product. Short viewports, such as a
phone held sideways, adapt rather than pushing the calendar off the screen. The scrollbar's
width is reserved at all times so content never shifts sideways when a page becomes long enough
to scroll. Print styles exist and matter here, because a trip itinerary is a document people
print and carry.

What this must not look like: a page dominated by a single hue family with no second signal; a
marketing composition where the working surface belongs; decoration standing in for content; or
a results grid animating each card as it arrives, which is what makes a long list unusable.

## Technical requirements

The rendering model is server-rendered HTML with hydrated interactive islands. The home route,
the search results and the listing detail arrive as finished markup in the first response, and
the browser receives content rather than an empty shell it then fills. The frontend is Remix on
React Router 7. The HTTP API is Hono, serving both the Remix handler and the JSON API from one
origin. The runtime is Node 20. The datastore is PostgreSQL, reached at `DATABASE_URL`, which
is read from the environment and never hardcoded.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
service available in this environment is `postgres`, and reaching for anything else is a
contract violation. `postgres` is already running and reachable at its environment variable and
must not be downloaded, installed, compiled or started.

Authentication is email and password implemented in the app, with hashed passwords and bearer
tokens. `GET /api/health` returns `200` once the app is ready. Requests are logged as one
structured line each to standard output.

Every public route carries its own title and its own **description**, and no two routes share
either. `Havenn | Holiday rentals, cabins, beach houses & more` is the home route's title. A
sitemap lists every public route. No credential, key or admin token appears in anything the
browser downloads.

Timed behaviour is read from the environment rather than compiled in. `PENDING_HOLD_TTL_SEC`
carries the lifetime of a pending hold and `QUOTE_TTL_SEC` the lifetime of a quote. Both are
read from the environment at run time; a literal compiled into the app is a contract violation,
because the whole point of the seam is that the durations can be changed without touching the
app.

Performance is budgeted rather than hoped for, and the budgets below are the requirement.
On a mid-range machine over a slow connection: the home route paints
its first content under one and a half seconds; search results become interactive under two and
a half seconds; under 170 kilobytes of script runs before first paint; the home route transfers
under 900 kilobytes on a first visit and the search results under 1.4 megabytes; the results
grid holds a 16 millisecond frame budget while scrolling a thousand results and the map holds
the same while panning and zooming; a search query answers server-side under 400 milliseconds
at the 95th percentile and a quote computes under 200 milliseconds at the same percentile.

This product's weight is script rather than pictures, which inverts the usual shape, so
aggressive code splitting is right in principle and wrong past the point where the cost of
asking for each piece exceeds what it saved. Any measurement the product takes is budgeted
explicitly: a reference build spent more on tracking beacons than on its fonts and its
structured data together, and this one ships no tracking beacon at all.

Loading order follows those budgets: critical styles, the token layer and the subset font
first; then the server-rendered markup for the route; then the search control's interactive
layer; then inventory or results, progressively; then the map, only when asked for; and any
measurement last of all. The map is the heaviest thing in the product and never blocks first
paint. The results grid renders a window of its rows with a stable key per row rather than all
of them, and attaches no per-row scroll animation. Only transform and opacity are animated.
Keyframes and settles are generated from the token layer rather than written out one at a time.
One font family ships, variable and subset; no icon font ships at all, because an icon-font
glyph is read aloud as the character underneath it and comes out as nonsense. Quotes are cached
by their inputs for their lifetime, because pricing is expensive and repeated. Any measurement
the product takes is held to an explicit budget.

Amounts are integers in the currency's minor unit throughout, with the exponent read from a
currency table: zero for the yen, two for most, three for the dinar. No price field anywhere is
a floating-point type, and no price arithmetic happens in the browser. The price breakdown
component receives a priced quote and renders it; it never computes. Two calculators eventually
disagree, and the number the guest sees stops being the number the guest is charged.

Availability filtering is the hard part of search and it happens inside the query rather than
after it. Price filtering compounds it, because the total for a range depends on per-date
rates, discounts, fees and taxes and so cannot be precomputed for every possible range; a
precomputed nightly summary sufficient to bound the total is what the query filters on, and the
exact totals are computed only for the page returned. A bound that excludes a listing which
would have qualified hides inventory silently and nobody ever notices.

Geography is stored as coordinates at a bounded precision, and a place name resolves to a
bounding box which is then stored, because place names are ambiguous and there are many places
called Portland.

Every operation reachable by a retry carries a key and replaying it returns the original
outcome: creating a reservation by a client-generated key scoped to the user; a capture, a
refund or a payout by a key derived from the reservation and the operation; a webhook by the
event id; and any other retryable operation by a natural key. Keys are retained at least as
long as any retry may arrive.

The search index is a derived view and is not the source of truth. A listing booked seconds ago
may still appear in results; opening it re-validates and says plainly that it has just gone
rather than failing at checkout. Reindexing lags, and the lag is measured and alarmed on,
because a stalled indexer looks exactly like low inventory. Nothing that affects money is read
from the index: a price in results is indicative and the quote is authoritative, and where they
differ the product says so.

## Data model

Twenty-three tables. All timestamps are UTC; all stay dates are local calendar dates in the
listing's timezone. Every table's primary key column is named `id`, and where an API field
names a row of another table it carries that `id` value under the name the table gives it, so
`reservation_id` in a response is the `id` of a row in `reservation`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

`user`: id, email, hashed password, phone, language, region, display currency, created at.
Email is unique.

`host_profile`: user, response rate, response time, superhost flag, verification state. One per
user at most.

`listing`: id, host, `inventory_type` one of `stay`, `experience` or `service`, title,
description, room type one of `entire_place`, `private_room` or `shared_room`, capacity,
timezone as an IANA identifier, currency, status one of `draft`, `in_review`, `listed`,
`snoozed` or `unlisted`, exact coordinates, approximate coordinates, and the stored offset
vector that produces the second from the first. The approximate pair is stored rather than
derived when read.

`listing_photo`: listing, ordinal, alternative text.

`amenity` and `listing_amenity`: a closed vocabulary of amenities, joined to listings.

`calendar_day`: listing, `local_date`, `is_available`, `price_minor`, `min_stay`, `max_stay`,
`closed_to_arrival`, `closed_to_departure`. **One row per listing per open local date**, within
the availability window. Availability and price are rows, not rules evaluated when read: hosts
set per-date prices and per-date minimum stays, search filters on availability across every
listing, and a value computed at read time cannot be constrained by the store. The table is
large and it is the right one.

`pricing_rule`: listing, base price in minor units, weekly discount, monthly discount, cleaning
fee, extra guest fee, guests included, pet fee, advance notice, preparation days, availability
window.

`tax_jurisdiction`: id, name, the base it applies to, its form, its rate or per-night or
per-person-per-night amount, its cap in nights where it has one, and its exemption threshold in
nights where it has one.

`cancellation_policy`: id, name, and its ordered tiers.

`quote`: `quote_id`, listing, `checkin`, `checkout`, the four guest counts, the line items,
each carrying a `code`, a `label` and an `amount_minor_units`,
`total_minor_units`, `currency`, `fx_rate`, `fx_pinned_at`, `expires_at`, `policy_snapshot`.
Single use.

`reservation`: `reservation_id`, listing, guest, `checkin`, `checkout`, the four guest counts,
`status` one of `pending`, `confirmed`, `cancelled`, `declined` or `expired`, `quote_snapshot`,
`policy_snapshot`, created at. **At most one reservation whose status is `pending` or
`confirmed` covers any night of any listing.** This is a property of the stored data rather
than of the code that writes it: two confirm requests arriving together for overlapping nights
on one listing end with exactly one reservation stored and the other caller refused, and the
refusal leaves nothing behind.

`payment`: `payment_id`, reservation, `provider_reference`, `authorised_minor_units`,
`captured_minor_units`, `refunded_minor_units`, `currency`, `idempotency_key`, `status` one of
`requires_action`, `authorised`, `captured`, `voided`, `refunded` or `declined`. The
idempotency key is unique per user, so a replay finds the original rather than writing a second
row. No card number, security code or bank detail is stored in any column.

`payment_event`: payment, the event id from the component, the event type, the event's own
timestamp, and whether it has been applied. An event id appears once.

`payout`: reservation, host, amount, scheduled for, released at, `provider_reference`,
recovery outstanding.

`review`: `review_id`, reservation, `direction` one of `guest_to_host` or `host_to_guest`,
rating, subratings for `cleanliness`, `accuracy`, `checkin`, `communication`, `location` and
`value`, body, `submitted_at`, `published_at`. One row per reservation per direction. A row
whose `published_at` is empty is readable only by its author.

`thread` and `message`: a thread is scoped to a reservation or an inquiry; a message carries
its author, its body as stored after redaction, its attachments, and its delivery and read
state.

`wishlist` and `wishlist_item`: a named collection owned by a guest; an item carries the
listing and the dates it was saved under.

`imported_block`: listing, the local dates blocked, the feed it came from, the instant it
arrived, and the last successful synchronisation time for that feed.

`audit_record`: the actor, the subject, the instant, the reason, and the record it concerns.
Every access by a support actor to another party's personal data writes one, and the log is
queryable.

**Seed data.** Two guests, `guest@example.com` and `guest2@example.com`. Two hosts,
`host@example.com` and `host2@example.com`. Four listings. `Cedar Loft` in Portland, owned by
`host@example.com`, priced in `usd` with a base of `18000` minor units a night, capacity `4`,
`2` guests included, an extra guest fee of `2500`, a cleaning fee of `9000`, a pet fee of
`4000`, a weekly discount and a monthly discount, timezone `America/Los_Angeles`, instant book,
pets allowed. `Harbour Cottage` in Amsterdam, owned by `host@example.com`, priced in `usd`,
request to book, one preparation day, one date in its window closed to arrival, timezone
`Europe/Amsterdam`. `Kite House` in Kyoto, owned by `host2@example.com`, priced in `jpy`, which
has no minor digits, with a base of `24000` a night, timezone `Asia/Tokyo`, instant book. `Salt Marsh Cabin` in Gulf Shores,
owned by `host2@example.com`, priced in `usd`, timezone `America/Chicago`, with exactly one
bookable window open in its whole calendar and every other night blocked: it is the listing two
guests are made to fight over. Three tax jurisdictions cover the three shapes: Portland taxes
the accommodation total as a percentage with no cap; Amsterdam taxes a wider base including the
service fee and exempts stays of thirty nights and over; Kyoto charges a flat amount per person
per night. Each listing's calendar is open for the coming year in its own local time, with the
blocks above applied. Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the measured design in full. Nothing in it is a number the builder must
type; every value below is stated as a relationship, a role or a behaviour, and the exact
values are yours so long as the relationships hold.

**The token layer is real, not decorative.** Radii, elevations, materials and motion are
declared once at the root and every surface reads them. Changing one radius token must move
every surface that uses it; if it does not, the tokens are documentation rather than a system.
Ship the eight radii as one ladder and do not add a ninth without adding it to the ladder. The
census of a correctly built page should show the small end of the ladder dominating, with the
larger steps rare, and the pill and circle forms outside the ladder by intention.

**Colour census.** The ink should outnumber the brand colour by roughly two orders of
magnitude. The secondary grey is the second most used value in the product because it carries
all metadata. The teal is a legacy surface at a small share and must not grow. Two inks, one
secondary, one tertiary, one brand, one error, one success, one star, one hairline, one hover
ground: that is the whole palette, and anything outside it needs a reason.

**Gradients.** Four brand gradients exist and they are two definitions each in two palettes.
The resting radial runs from the brand red at the centre through five stops, mid vivid magenta
through mid soft magenta, to a deep soft violet at the rim. The active radial shifts that whole
ramp two stops darker and keeps the six-stop structure. The wide linear form runs left to right
across three of the same stops, and its darkened twin does the same two stops down. Both linear
forms also exist mirrored for right-to-left reading, where the gradient direction reverses
rather than the element. One further gradient carries every photographic overlay: transparent
at the top to near-opaque black at the bottom.

**Elevation.** Six steps, named elevation-elevation0 through elevation-elevation5. The
flattest is an inset hairline in the near-white border grey, so a
flat surface gets an edge without a border property and without changing its box. Every step
from the first upward opens with the same very faint black hairline, so a raised surface keeps
its edge. The ramp grows in blur and in offset while its opacity stays in a narrow, low band,
so elevation reads as spread rather than as darkness. Five further legacy elevations named
primary, secondary, tertiary, high and sharp-edge exist and are not extended.

**Materials.** Five translucent surfaces, each a blur, a saturation and a translucent ground.
Extra-thin is the least opaque over a light blur. Thin blurs the most of any of them over a
moderately opaque ground. Regular sits between. Thick blurs the least while saturating the most
and sits over a nearly opaque ground. Extra-thick is almost opaque white. Thickness is the
opacity of the ground, not the strength of the blur, and the ramp that feels obvious is
wrong.
Every material has an opaque fallback for contexts with no backdrop blur.

**Modules.** Twelve pieces of machinery make up this product's component architecture, and
naming the module boundaries is worth doing before any of them is written: the token layer; the
settle generator; the search-entry control; the date range picker; the guest stepper; the
listing card; the result grid; the map surface; the price breakdown renderer; the booking
panel; the thread; and the calendar editor. Three of them carry the risk. The settle generator
takes a mass, a stiffness and a damping and returns a duration and a sampled easing, so adding
a seventh settle takes three physical numbers and nothing else, and the resolved easings are
its output rather than its input. The date range picker is **one** component in four contexts,
the search entry, the listing detail, a checkout amendment and the host calendar editor, and
the contexts differ only in what each disables; forking it per context is the temptation to
resist, because the half-open range and the local-date handling are exactly what goes subtly
different in a copy and the divergence then surfaces as an off-by-one in one flow only. The
host context is the one that permits selecting blocked dates, since that is how they get
unblocked. The price breakdown renderer is one component in four contexts, the listing panel,
checkout, the receipt and the host payout view, and it never computes: it receives a priced
quote and displays it.

**Typography.** The type scale below is the whole typographic system, and this product's
density comes from weight and colour rather than from size. The workhorse size carries body
text at its regular weight with a comfortable
leading, the same size at a tighter leading for dense body, and the same size a weight up for
labels and tab text. Form fields sit one step above it. Section headings sit at a display step
set solid, with an alternate slightly looser leading, and a sub-heading step just below it set
solid. Card titles sit between the interface size and the sub-heading, a weight up. Dialog
titles sit just above the interface size, a weight up again. Fine print sits one step below the
interface size. The error-page display is far above everything else and appears only there, and
its subtitle is the second largest thing in the product. Author the leadings as ratios of their
sizes rather than as fixed measures. One family ships: a freely licensed geometric grotesque
with a variable weight axis covering the range from body weight to heavy, behind a fallback
stack of -apple-system, Segoe UI, Roboto, Helvetica, Arial and a generic sans-serif. A variable
axis rather than three static cuts, because the weight is load-bearing and one file carries it.
Subset it aggressively to the shipped locales. The reference's own commercially licensed
typeface is not available and is not needed.

**The settles.** Six named settles carry every triggered movement: fast, fast-bounce,
standard, medium-bounce, slow and slow-bounce. Each is declared as a mass, a stiffness and a
damping, and whether it bounces is decided by where its damping sits against critical damping
for that stiffness. Fast is just over critical and arrives without overshoot. Standard sits
fractionally under it, so it peaks a hair above its target and settles. Slow sits exactly on
it, the precise value at which a spring stops bouncing at all. Fast-bounce, medium-bounce and
slow-bounce are all clearly underdamped and, although their stiffnesses differ, all three
overshoot by the same small amount, so the overshoot reads as one house character rather than
three. Keep that relationship: it is tuned, not incidental. Do not paste resolved easings; they
are outputs of the generator, and a product where adding a settle means copying a list of
samples has been built the wrong way round. Every runtime keyframe runs linearly with its curve
baked into its own value samples, which is the same technique and is why a real build has
hundreds of generated keyframes rather than a dozen hand-written ones.

**Scroll.** There is barely a scroll system here, and that is the engineering rather than an
omission: a results grid that can hold thousands of rows is exactly where per-row scroll motion
makes a product unusable on an ordinary laptop. The only scrubbed movement in the product is
the header's compact transition, which transforms the search control and the container around
it as the page leaves the top, and, at narrow widths, a sticky control gaining elevation. The
results grid must not be scroll-driven and attaches no per-item animation. Reserve the
scrollbar's width at all times so content never shifts sideways when a page becomes long enough
to scroll.

**Breakpoints.** Three bands: narrow, up to a max-width you choose; middle, between a min-width
and a max-width you choose; and wide, from a min-width you choose upward, with a maximum
container width above it. The narrow band carries the most declarations, which is the honest
shape for this product. Two further query families are worth copying: hover styles apply only
where a pointer exists, gated on hover-capable devices, which is what stops a tap leaving a
control stuck looking hovered; and short viewports, including a phone in landscape, adapt the
search panels rather than pushing a full-height calendar off the screen. Print styles exist.

**Hidden text and contrast.** A single visually-hidden idiom, used consistently, carries every
description that should be announced and not seen, clipping the element rather than moving it
off-screen. Contrast is checked in pairs: the ink on white is comfortable; the secondary grey
on white passes at body size and fails below it, which matters because that grey carries all
listing metadata and the entire link grid; the placeholder grey on white is marginal and is
used for placeholders only; white on the brand glow varies across the ramp and is checked
against its lightest stop; and the legacy teal on white passes.

**Iconography.** Every icon is drawn in the page. The set is: arrow, search, globe, menu,
close, heart, star, map pin, calendar, guest, filter, share, a chevron in four rotations, and
one glyph per amenity category. The arrow is a full-width shaft meeting a chevron head whose
apex is rounded by a single unit rather than mitred, which is what stops it reading as spiky at
small sizes. The search glyph is a circle with a handle that starts inside the circle's edge
rather than touching it, which is what makes the join read solid. The globe is a circle with
interior latitude and longitude curves and opens the language, region and currency control. The
wordmark is a mark beside the lowercase word `havenn`, optically centred, the mark near square and the
lockup a little over three times as wide as it is tall, the mark one closed looping figure with
a single interior counter, drawn in the brand colour with the word in the ink or the brand
colour. The four category icons are a globe, a house, a balloon and a service bell, drawn
inline rather than downloaded: four image requests for four small icons is the most wasteful
thing a home route can do.

**Header.** Three regions left to right: the wordmark; the four category tabs, centred; and a
right cluster carrying `Become a host` as a bare text link, a circular globe control and a
circular menu control carrying three bars. Both circular controls carry the one hover in the
product, a background moving from nothing to the hover ground. Below the tabs sits the
search-entry control, centred, overlapping the header's lower edge. The header sits above the
page, its dropdowns just below it, and modals above both.

**Category tabs.** Four, labelled `All`, `Homes`, `Experiences` and `Services`, in a generously
rounded pill form outside the radius ladder. The label sits at the interface size a weight up,
inactive in the secondary grey, active in the ink with a rule beneath it. Each tab enters with
a short linear keyframe, staggered across the group so the leftmost arrives a fraction ahead of
the rest. The second tab reads `Homes` on screen and is identified internally as the stay
inventory type: the internal vocabulary and the presented vocabulary are allowed to diverge, so
the label can be renamed without touching the data.

**The globe control** opens three independent settings, never one: language, region and display
currency, as rule 46 requires.

**Search-entry control.** One rounded container carrying three segments over a submit, the
segments separated by hairline dividers, the container raised. Each segment carries its label
at the interface size a weight up in the ink, and its placeholder at the same size at the
regular weight in the placeholder grey. The submit is a circle carrying the search glyph in
white on the brand glow. The control is one component in two states, expanded at the top of a
scrolling route and collapsed into a single pill summarising the query once scrolled, moving
between them on the standard settle. It is three grouped inputs and a submit rather than a
search box: it needs a search landmark, a label per segment, a calendar fully operable by
keyboard announcing its selected range, a stepper announcing its value on change, and a submit
reachable without traversing the calendar. Descriptions for the inputs are provided and hidden
visually by clipping rather than by moving them off-screen.

**Listing card**, shared by search, the home carousels and wishlists. A photo carousel with
dots at a medium radius; a heart-shaped wishlist control overlaid top right; the place and the
listing name at the interface size a weight up in the ink; the distance or type at the same
size at the regular weight in the secondary grey; the query's dates when it has them; the total
for the query when dates are set and otherwise the nightly from-price, labelled as such; and
the star glyph in the warm orange beside the numeric rating.

**Footer.** Three columns on the wide layout, carrying the items named in rule 59, with the
link grid above them. Cell and tab hover moves the colour and the border colour from the
secondary grey to the ink.

**Mobile chrome.** Below the narrow width the right cluster is replaced by a fixed bottom bar
of three items, each an icon over a small label, the active item in the brand colour and the
rest in the ink. The category tabs become horizontally scrollable pills. No app-promotion
banner ships: inserting one first in the document pushes the whole page down on every narrow
visit, and whether to carry one is a decision rather than an inheritance.

**Error pages.** No header, no footer, no chrome, and no scroll at any width. The wordmark sits
top left, the display line is the largest type in the product at a heavy weight, the subtitle
sits well below it at a heavy weight, the code is small and heavy, and the links run in the
legacy teal. A flat vector figure sits beside the text, composed from circles, rounded
rectangles and a triangle in a limited palette of the teal, the brand red, a warm orange and a
warm skin tone, with a spilled shape at its feet. It carries no information and is hidden from
assistive technology.

**Asset manifest.** The reference this design was measured from shipped a variable font, two
icon fonts, four raster category icons, an error-page illustration, profile imagery, listing
photography and hundreds of tracking beacons. This build ships none of them. The guide below is
the zero-asset substitution for each class.

**Generated imagery.** Nothing binary ships: no image file, no video file and no font file is
in the build tree. Listing photography is a deterministic architectural abstraction generated
from the listing id, a warm ground under two or three light massing rectangles with a soft
horizon and a sky wash; at card size under the photographic overlay it reads correctly and
holds the layout exactly. Avatars are generated from the user id as a two-tone geometric mark on
a ground from the neutral palette, never a photograph of a person. Map tiles do not exist here,
so the map renders a plain ground with pins positioned by projected coordinates. Every generated
image is deterministic: rebuilding twice produces identical bytes. This substitution produces a
complete and correct system and it will not sell a stay, because a marketplace for places to
stay is a photography product and real photographs remain outstanding.

## Constraints

Single tenancy: one Havenn, one set of listings, no organisations. No native application. No
external network call at run time, so map tiles, card acquiring, foreign-exchange rates, tax
determination, transactional mail and any measurement vendor are in-product components with the
same observable contracts rather than third-party services. No second datastore, no cache, no
queue, no object store, no identity provider. No background scheduler: anything that must
happen on a deadline is either evaluated when the affected data is read or reachable through
the maintenance endpoint rule 27 names. No file uploads: every image in the product is
generated. No email is sent; notifications are records the recipient reads in the product.
Experiences and services carry an inventory type, a route and search results, and no booking
flow of their own beyond the stay flow. Co-host and support actors exist in the authorization
model and have no surfaces of their own. No paid placement exists, so nothing needs the label.
The legacy teal is not extended beyond the error pages. No icon font and no downloaded icon. The build is zero-asset: the build tree contains no
image file, no video file and no font file, and every asset class the design would otherwise
need is substituted procedurally.
The app must stay responsive with four listings seeded and with a thousand listings and ten
thousand calendar days loaded.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world
  uses. Read both from the environment; never hardcode either.
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
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A plain list endpoint returns a top-level JSON array; the
search endpoint returns an object because it carries a cursor. A successful call returns the
named resource or shape. An invalid, unauthorized or conflicting call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason. Bearer auth is required on everything except `POST /api/auth/signup`,
`POST /api/auth/login`, `GET /api/health` and `POST /api/payments/webhook`, which authenticates
by signature and never by a user token.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password` | the created user and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token |
| `GET /api/health` | none | `200` |
| `GET /api/listings` | `place`, `checkin`, `checkout`, `adults`, `children`, `infants`, `pets`, `min_price`, `max_price`, `room_type`, `amenities`, `instant_book`, `cursor`, `sort`; with no parameters at all it returns the first page of every listed listing | an object carrying `results`, `next_cursor`, `total_estimate`, `partial`, each result carrying `listing_id`, `title`, `currency` |
| `GET /api/listings/{id}` | none | the listing, with approximate coordinates only |
| `GET /api/listings/{id}/availability` | `from`, `to` | an array of `local_date`, `is_available`, `price_minor`, `min_stay`, `max_stay`, `closed_to_arrival`, `closed_to_departure`, `bookable_as_checkin` |
| `GET /api/listings/{id}/reviews` | none | an array of published reviews only |
| `POST /api/quotes` | `listing_id`, `checkin`, `checkout`, `adults`, `children`, `infants`, `pets` | the quote, with `lines`, `total_minor_units`, `currency`, `expires_at`, `policy_snapshot` |
| `GET /api/quotes/{id}` | none | the same quote while it lives |
| `POST /api/reservations` | `quote_id`, `payment_method_reference`, header `Idempotency-Key` | the reservation and its payment, or a conflict naming the taken nights, or `requires_action` |
| `GET /api/reservations` | none | an array of the caller's own reservations |
| `GET /api/reservations/{id}` | none | one reservation with its receipt and, once confirmed, the exact address |
| `GET /api/reservations/{id}/refund-quote` | none | the itemised refund computed from `policy_snapshot` |
| `POST /api/reservations/{id}/cancel` | `reason` | the cancelled reservation and the stored refund |
| `POST /api/reservations/{id}/accept` | none | the confirmed reservation and the captured payment |
| `POST /api/reservations/{id}/decline` | `reason` | the declined reservation and the voided payment |
| `POST /api/reservations/{id}/complete-challenge` | none | the confirmed reservation once the outstanding challenge is answered |
| `POST /api/maintenance/release-expired-holds` | none | the count released |
| `POST /api/payments/webhook` | the event, signed | `200` once applied or recognised as already applied |
| `GET /api/host/listings` | none | an array of the caller's own listings |
| `POST /api/host/listings` | the listing fields | the created listing |
| `PATCH /api/host/listings/{id}` | any listing field, including `status` | the updated listing |
| `GET /api/host/listings/{id}/calendar` | `from`, `to` | an array of `calendar_day` rows |
| `PATCH /api/host/listings/{id}/calendar` | an array of per-date changes | the updated rows |
| `POST /api/host/listings/{id}/calendar/import` | the feed text | the imported blocks and any conflict raised |
| `GET /api/host/reservations` | none | an array of reservations on the caller's own listings, ordered by check-in |
| `GET /api/host/earnings` | none | an array of payouts with amounts, schedules and recoveries |
| `GET /api/trips` | none | an array of the caller's reservations grouped upcoming, current, past |
| `GET /api/threads` | none | an array of the caller's own threads |
| `POST /api/threads` | `listing_id`, `body`, optionally `reservation_id` | the created thread, scoped to that reservation or inquiry |
| `GET /api/threads/{id}` | none | one thread with its messages as stored after redaction |
| `POST /api/threads/{id}/messages` | `body`, optional attachments | the stored message, redacted |
| `GET /api/wishlists` | none | an array of the caller's own wishlists |
| `POST /api/wishlists` | `name` | the created wishlist |
| `POST /api/wishlists/{id}/items` | `listing_id`, `checkin`, `checkout` | the created item |
| `POST /api/reviews` | `reservation_id`, `direction`, `rating`, `subratings`, `body` | the submitted review, unpublished until its pair or the window |

**No mocks.** The reservation, its payment, its payout and its review must be real rows in
`postgres`. An in-memory list of reservations, a hardcoded success response the app returns to
itself, a price computed in the browser, a review filtered out of a template while still present
in the response body, or an exact coordinate sent in a field the interface does not draw are all
contract violations however good the interface looks. `postgres` is the fact: the app's UI and
its own caches can only reflect what lives there, never substitute for it.

## Definition of done

A traveller can search a place and dates, open a listing, read the whole price before agreeing
to it, and confirm a reservation that holds the nights and authorises the money, and the
receipt shows the same total that was authorised. Two travellers confirming the same nights on
the same listing at the same moment end with one reservation between them, and the one who lost
is told and holds nothing. A host can open a calendar, price a night, accept a request, and see
the payout it earns. What was sold stays sold: changing a policy afterwards does not change the
terms of a stay already booked.
