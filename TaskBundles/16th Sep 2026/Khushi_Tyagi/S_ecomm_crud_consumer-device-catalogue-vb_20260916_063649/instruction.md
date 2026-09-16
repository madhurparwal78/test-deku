# Halcyon

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, walk a product family, narrow
it by colourway and capacity, open one device, choose a colourway and a capacity that resolve to
exactly one variant, and follow whichever buy route that variant carries, without hitting an error
page. A signed in owner must be able to register a device by its serial number and file a support
request against that registration, and must receive exactly one acknowledgement for it however
many times the form is submitted. A second owner must not be able to register a serial that
already belongs to somebody else, and must not be able to open a request against a registration
they do not own; a refusal drawn in the interface does not count, because the same call made
directly must be refused too and the stored rows must be unchanged afterwards. The registration,
the request and its reference must be real rows in `postgres` that survive a restart, and the
acknowledgement must be a real message delivered over `SMTP_HOST` to that owner's own address; a
confirmation the app draws for itself does not count.

## Overview

Halcyon is the regional catalogue of a consumer electronics brand that designs and sells its own
phones, audio and wearables. One brand owns every item in it. There are no other sellers, no
bidding, and no listings submitted by anybody outside the business. The catalogue is one of
several country sites and the country it serves is a property of the deployment, surfaced in the
footer as a store selector paired with a language selector.

The catalogue is organised on one axis, the product family, and the families are phones, audio,
wearables and a second lower priced hardware line sold under its own name, Arc. A product belongs
to exactly one family. Every product exists in several variants, and a variant is defined by two
independent axes that cross each other: a named colourway, which carries its own media, and a
capacity, which is a memory and storage pair carried by phones and absent from audio. A variant is
the unit that carries media, availability and the buy route. It is not a badge painted over a
product card: two colourways of one phone are two rows and two cards.

Three mechanics carry the product. Variant resolution: choosing a colourway and a capacity
resolves to exactly one variant, and the buy panel, the media and the availability all follow that
resolution, while a capacity that does not exist in the chosen colourway becomes unselectable
rather than resolving to nothing. The per variant buy route: a variant is either sold direct, in
which case the buy control adds it to a cart the site holds, or handed off to a named third party
retailer, in which case the same control becomes an outbound link carrying the resolved variant,
and which of the two applies is a property of the variant resolved on the server rather than
inferred in the browser. Device registration and support: a signed in owner registers a device
against their account and files a support request against that registration, and this is the one
workflow on the site that durably changes state.

Around those sit reading surfaces that are unusually large relative to the commerce: a home route
that is a vertical stack of full viewport product panels rather than a merchandising grid, a family
listing, a product route built as a constellation of feature cards around one lifestyle image, an
operating system release route, a brand story route, a community grant programme route, and a
support centre that is a second application wearing the same brand.

The genuinely hard part is the buy route. It is per variant, it is resolved on the server, and the
seeded catalogue carries all three modes, so an app that implements only the direct route will
look right against this brief and behave wrongly against the data.

Halcyon deliberately is not: a second seller, an auction, a customer review surface with media
upload, a live chat, a subscription plan, a loyalty points ledger or a payment step. Trade in and
repair booking record an intent and return a reference; they do not price a device, schedule a
visit or move a unit. The app ships no photograph, no video and no font binary, and it makes no
network call to any other origin at run time.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Anonymous visitor | Browse the home route, every family listing, every product route, the brand story, the operating system release, the community programme, the support centre and its articles and the standing pages; filter and sort a listing; resolve a variant; add a `direct` variant to a cart held against an anonymous identifier; follow a `handoff` link; leave an article helpfulness vote; record a `notify`, `tradein` or `repair` intent | **Cannot register a device, cannot open or read a support request, cannot read anybody's registrations, and cannot read any account's email address** |
| `owner` | Everything a visitor can, plus register a device by serial number against their own account, read their own registrations, open a support request against a registration they own, read their own requests and their references, and reconcile their anonymous cart onto their account on sign in | **Cannot read or write another account's registrations, requests or cart. Cannot open a request against a registration owned by anybody else. Cannot register a serial already registered to another account. Cannot learn, from any refusal, which account holds a serial** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an anonymous session, or from a signed in `owner`
session naming another owner's registration or request, must be rejected by the server (an
unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone can create an `owner` account from the account surface, and the account a
row belongs to is read from the session, never from the request body.

Two accounts are seeded, both with the password `deku-demo-pw-2026`: `owner@example.com` and
`owner2@example.com`.

## Core features

### Auth

Accounts are email and password, held by this app. A successful login returns a bearer token the
client sends on every authenticated call. Passwords are stored hashed, never in clear. Signup is
open and creates an `owner`.

1. `POST /api/auth/signup` with an address that is already held is rejected as invalid, and no
   second account row is written.
2. `POST /api/auth/login` with the wrong password, or with an address that holds no account, is
   denied, and both cases answer with the same wording, `Incorrect email or password`. A refusal
   that says the address is unknown tells a stranger which addresses hold accounts here, so the
   two cases must not be distinguishable from outside.
3. A token that has expired is denied on every authenticated call rather than served, and the
   surface offers sign in again without discarding what the visitor had typed.
4. `GET /api/auth/me` returns the signed in account, and answers denied without a token.
5. `POST /api/auth/logout` ends the session; the same token afterwards is denied.
6. A password reset confirmation renders as a success message above the sign in heading, reading
   `Password successfully changed.`

### The catalogue and its families

The family slug set is closed and is a property of the catalogue rather than of the router:
`phones`, `audio`, `wearables` and `arc`.

1. `GET /api/families` returns the four families in catalogue order.
2. A family route for a family that holds no products renders the empty listing surface, not a
   not found. The route is valid and the catalogue is simply empty. `wearables` is seeded with no
   products so this surface is reachable.
3. A family slug outside the closed set is a not found.
4. Six products are seeded. In `phones`: `phone ( 5a ) pro` at slug `phone-5a-pro` and
   `phone ( 5a )` at slug `phone-5a`. In `audio`: `headphone ( 2 )` at slug `headphone-2` and
   `earbud ( 3a )` at slug `earbud-3a`. In `arc`: `arc buds ( 1 )` at slug `arc-buds-1` and
   `arc watch ( 2 )` at slug `arc-watch-2`.
5. Product names are lower case and are written with literal spaces inside the brackets. The
   spaces are characters in the stored string, not letter spacing applied over it, and they are
   what makes the name read as a readout rather than as a word.
6. Fourteen variants are seeded. A variant identifier is
   `<product-slug>--<colourway-slug>--<capacity-slug>`, with the capacity segment omitted when the
   product has no capacity axis; the colourway and capacity segments are lower case with spaces
   and punctuation reduced to single hyphens. Worked examples:
   `phone-5a-pro--midnight--12-256` and `headphone-2--black`.
7. The seeded matrix, which every later rule is asserted against:

| Variant | Product | Colourway | Capacity | Buy route | Price |
|---|---|---|---|---|---|
| `phone-5a-pro--chalk--8-128` | `phone-5a-pro` | `Chalk` | `8 GB / 128 GB` | `direct` | `79900` |
| `phone-5a-pro--chalk--12-256` | `phone-5a-pro` | `Chalk` | `12 GB / 256 GB` | `handoff` | none |
| `phone-5a-pro--slate--8-128` | `phone-5a-pro` | `Slate` | `8 GB / 128 GB` | `handoff` | none |
| `phone-5a-pro--slate--12-256` | `phone-5a-pro` | `Slate` | `12 GB / 256 GB` | `unavailable` | none |
| `phone-5a-pro--midnight--12-256` | `phone-5a-pro` | `Midnight` | `12 GB / 256 GB` | `direct` | `99900` |
| `phone-5a--chalk--8-128` | `phone-5a` | `Chalk` | `8 GB / 128 GB` | `handoff` | none |
| `phone-5a--slate--8-128` | `phone-5a` | `Slate` | `8 GB / 128 GB` | `handoff` | none |
| `headphone-2--black` | `headphone-2` | `Black` | none | `direct` | `29900` |
| `headphone-2--white` | `headphone-2` | `White` | none | `handoff` | none |
| `earbud-3a--white` | `earbud-3a` | `White` | none | `direct` | `14900` |
| `earbud-3a--black` | `earbud-3a` | `Black` | none | `unavailable` | none |
| `arc-buds-1--orange` | `arc-buds-1` | `Orange` | none | `handoff` | none |
| `arc-buds-1--grey` | `arc-buds-1` | `Grey` | none | `handoff` | none |
| `arc-watch-2--grey` | `arc-watch-2` | `Grey` | none | `direct` | `6900` |

8. `phone-5a-pro` is sold in three colourways and two capacities, which is six pairs, and only
   five of them exist. `Midnight` with `8 GB / 128 GB` is the hole, and rule 4 of the product
   route depends on it.
9. Money is an integer in the minor unit of `usd`. A price of `79900` is seven hundred and
   ninety nine dollars, not `799.00` and not `799`. Only a variant whose buy route is `direct`
   carries a price; every other variant carries none, and the catalogue neither stores nor
   displays one for it.
10. Release dates, used by the newest sort, are `2026-08-12` for `phone-5a-pro`, `2026-06-03` for
    `arc-watch-2`, `2026-04-21` for `headphone-2`, `2026-02-17` for `phone-5a`, `2025-11-05` for
    `earbud-3a` and `2025-09-30` for `arc-buds-1`.

### The family listing

One route per family, reached from the drawer and from the support centre bar.

1. The listing shows **one card per variant, never one per product**. A phone offered in four
   colourways takes four cards, so `/collections/phones` shows seven cards and `/collections/audio`
   shows four.
2. A card carries the variant media, the product name set in the label face, and the colourway
   name set in the mono face. **A card carries no price.** That follows from the buy route: a
   handed off variant has no price this site owns, and showing one for some cards and not others
   would be worse than showing none.
3. Three facets: family, which is the route itself; colourway, whose values are the union of the
   colourway names in the result set; and capacity, whose values are the union of the capacity
   pairs and which is offered on phone families only.
4. Facets are additive within an axis and intersective across axes. Choosing two colourways widens
   the result; choosing a colourway and a capacity narrows it. Choosing `Chalk` and
   `12 GB / 256 GB` on `/collections/phones` leaves exactly one card.
5. The facet and sort state lives in the query string, so a filtered listing is a link somebody
   can send, and the browser back button steps back through the facet changes one at a time rather
   than leaving the route.
6. Three sort orders: `Featured`, which is the catalogue order and is the default; `Newest`, by
   release date descending; and `Name`, alphabetical by product and then by colourway. There is no
   price sort, for the reason in rule 2.
7. An empty result set renders the family name, a one line message and a control that clears every
   facet at once. A family with no products at all renders the same surface. Neither is a not
   found.
8. While a listing is loading it shows card shaped placeholders at the card width carrying the
   indeterminate pulse, never a spinner.

### The product route and variant resolution

1. The route renders a full bleed lifestyle image with a buy panel anchored over it and a
   constellation of feature cards positioned around it. Between six and nine cards are authored per
   product, and their positions are content rather than computed, which is why two products look
   genuinely different rather than like one template with different pictures.
2. The buy panel carries one selector per axis the product actually has: a colourway selector
   always, and a capacity selector only where the product has a capacity axis. `headphone ( 2 )`
   renders one selector; `phone ( 5a ) pro` renders two.
3. Changing a selector resolves the new variant on the server, swaps the thumbnail and the
   gallery to that variant's media, re-resolves the buy route, which may change the action label,
   and rewrites the address so the resolved variant is a link somebody can send, without a full
   navigation and without losing scroll position.
4. **A capacity that does not exist in the chosen colourway renders unselectable rather than
   resolving to nothing.** With `Midnight` chosen on `phone ( 5a ) pro`, `8 GB / 128 GB` is
   offered and is not choosable; it is not silently removed from the list, because a missing
   option and a dead option say different things. Choosing an impossible pair by any direct means
   is rejected as invalid and resolves to no variant.
5. `GET /api/variants/{variant_id}` returns exactly one variant, carrying its colourway, its
   capacity where it has one, its buy route, its availability, its media set and its price where
   it has one. An identifier that names no seeded variant answers not found.
6. The gallery opens from the magnify control beside the thumbnail, shows the resolved variant's
   media one image at a time with previous and next controls and a close control, keeps keyboard
   focus inside itself while it is open, returns focus to the magnify control on close, and closes
   on the escape key.
7. The specification surface is reached from the specification card in the constellation and is a
   route of its own at `/products/phone-5a-pro/specifications` and its siblings, carrying grouped
   rows with the labels in the mono face and the values in the display serif. It is a route, not
   an accordion on the product route.
8. What the UI displayed and what the database holds must agree: after a variant is resolved and
   the page is reloaded at the resulting address, the same variant, the same media, the same
   availability, the same buy route and the same price are shown, because the address carries the
   resolution and the resolution is read from the stored row rather than rebuilt in the browser.

### The buy route

The single most important mechanic here. Each variant carries one of three fulfilment modes,
resolved on the server and never inferred in the browser.

1. `direct`: the action reads `ADD TO CART`, adds the resolved variant to the cart and opens the
   cart drawer.
2. `handoff`: the action reads `SHOP ON Bazaario` and is a real anchor with a real address at
   the retailer's own origin, `https://www.bazaario.example`, carrying the resolved variant
   identifier. It is not a scripted
   navigation, so it can be opened in a new tab and its destination previewed before it is
   followed. It carries a no opener relationship and an indication for assistive technology that
   the destination is an external site. The label names the retailer inside the button because
   that is the honest treatment: the label tells a person they are about to leave.
3. `unavailable`: the action reads `NOTIFY ME` and records a `notify` intent against the variant
   and an email address.
4. **A handoff is recorded as an outbound click and never as a conversion.** Following a handoff
   writes one row to the outbound click record naming the variant, the destination and the
   anonymous identifier. The catalogue cannot observe what happens at the retailer and must not
   report an outcome; counting a handoff as a sale would report revenue the business did not
   make, so no order, no invoice and no revenue row may be written by a handoff. No identifier the
   retailer could join back to a person is attached to the outbound address.
5. The mode is a column on the variant. A client that posts a cart line for a variant whose mode
   is not `direct` is rejected as invalid, whatever the interface showed.

### Cart and the checkout handover

The cart serves `direct` variants only.

1. The cart is reachable at `/cart` and also renders as a right hand drawer opened by an add. The
   route and the drawer share one state and one set of contents; the route is the drawer laid out
   full width.
2. The empty cart is a centred heading and one full width action reading `CONTINUE SHOPPING`, on
   the flat ground under the floating pill and the dot grid. There is no illustration, no
   suggested product and no recently viewed row.
3. A populated line carries the variant media, the product name in the label face, the colourway
   and the capacity in the mono face, a quantity stepper and the line total. The summary carries
   the subtotal, a discount row when one is present, and the total.
4. The summary block holds one fixed height and swaps to a second, taller fixed height when a
   discount row is present, rather than sizing to its contents. The action beneath it must not
   move when a discount is applied.
5. The cart survives a page reload and a browser restart. Persistence here is a requirement
   rather than an optimisation: the cart is keyed to an anonymous identifier held in a first
   party cookie, and it is reconciled onto the account on sign in, so a visitor who filled a cart
   before signing in still has it afterwards.
6. A line whose variant has since left `direct` is **retained, marked and excluded from the
   total**, never silently dropped. The visitor is told which line it is.
7. Checkout is a handover. The action is a real anchor to the separate payment origin carrying the
   cart identifier, the region and the language. The payment step is not part of this application:
   the app clears nothing when the visitor leaves, and reconciles the cart only when the checkout
   webhook arrives or when the cart is next read and found converted.
8. `POST /api/webhooks/checkout` receives that outcome and authenticates by signature rather than
   by a visitor's token. A body whose signature does not verify is denied and changes nothing.

### Device registration

1. A signed in owner registers a device by serial number from a slide over panel on the support
   centre, and the panel names the product the serial resolves to before the registration is
   confirmed.
2. A serial is `HLC-` followed by eight upper case letters and digits. Worked example:
   `HLC-7K42QD19`. A serial that does not match the shape is rejected as invalid with the field
   named, and nothing is written.
3. A well formed serial that names no product in the catalogue is rejected as invalid.
   `HLC-0000ZZZZ` is seeded as exactly that case.
4. **A serial is registered to at most one account.** A serial already registered to a different
   account is rejected with wording that names neither the other account nor its address, because
   a refusal that identifies the holder turns the form into a lookup. `HLC-9P61BW73` is seeded
   against `owner2@example.com` for this case.
5. `HLC-7K42QD19` is seeded as a registration of `phone-5a-pro` belonging to `owner@example.com`,
   and `HLC-3M08XT55` is seeded as an unregistered serial resolving to `headphone-2`.
6. `GET /api/registrations` returns only the signed in account's registrations. An anonymous call
   is denied.
7. Registering a device sends no mail.

### The support request

The one workflow here that durably changes state.

1. An owner opens a request at `/pages/contact-support` against one of their own registrations,
   choosing a category from the closed set `Setup`, `Battery`, `Connectivity`, `Software` and
   `Physical damage`, writing a body and optionally naming an attachment.
2. **A request may be opened only against a registration the signed in account owns.** A request
   naming a registration belonging to another account is rejected on the server, not merely
   hidden in the interface, and no request row is written.
3. A successful request returns a reference. A reference is `SR-` followed by eight digits.
   Worked example: `SR-40028117`.
4. **The acknowledgement is sent once.** The request form carries an idempotency key issued when
   the form is opened and sent back with the submission. A second submission carrying the same key
   returns the original reference, writes no second request row, and sends no second
   acknowledgement.
5. The acknowledgement is a real message sent over SMTP at `SMTP_HOST` and `SMTP_PORT`, addressed
   to the signed in owner's own address and to nobody else, with no cc and no bcc. Its subject
   begins with `Support request ` followed by the reference, so a request numbered `SR-40028117`
   carries the subject `Support request SR-40028117`. Its body is not empty and names the product,
   the serial and the reference.
6. No other transition sends mail. Registering a device sends none, voting on an article sends
   none, recording an intent sends none, and a rejected request sends none.
7. `GET /api/support-requests` returns only the signed in account's requests. A call naming
   another account's request is denied and the stored row is unchanged.
8. A request with an empty body, or with a category outside the closed set, is rejected as invalid
   with the field named, and nothing is written and nothing is sent.

### The support centre, its categories and article feedback

1. The support centre is a second application inside this deployment with its own chrome. It
   carries a full width bar pinned to the top holding the wordmark at the left and six links: the
   four product families, the community forum and support itself. **This is the only surface where
   the product families are exposed as visible navigation**, so it must not be replaced by the
   catalogue's floating pill.
2. The landing route carries an angled device image on a pale vertical gradient ground, a title
   reading `Support Centre`, a two line standfirst, and a fully rounded search field whose
   placeholder reads `Search` with a magnifier mark inset at its left.
3. Seven categories lead off the landing route: `Product guide`, `Troubleshooting`, `FAQs`,
   `Software download`, `Service centres`, `Product status` and `Accessibility`. Product guide
   holds per device setup and feature articles; troubleshooting holds symptom led articles;
   software download holds per device firmware and release notes; service centres is a searchable
   directory of physical locations; product status is a serial number lookup; accessibility holds
   the accessibility statement and the assistive features.
4. An article body carries ordered steps, inline device imagery and cross links to related
   articles. Three articles are seeded: `battery-drains-overnight` under `Troubleshooting`,
   `set-up-your-new-phone` under `Product guide`, and `check-your-serial-number` under
   `Product status`.
5. Every article ends with a helpfulness question reading `Was this page helpful?` and two
   controls reading `Yes` and `No`. Choosing one records a vote against the article and the
   anonymous identifier and replaces both controls with an acknowledgement in place.
6. **One vote per article per anonymous identifier.** A second vote from the same identifier
   updates the stored answer rather than inserting a second row, so the count never doubles.
7. Trade in and repair booking are stubs. Each presents a form, validates it, records an intent
   against an address and a device, and returns a reference. Neither prices a device, schedules a
   visit nor moves a unit.
8. `POST /api/intents` carries a kind of `notify`, `tradein` or `repair`, an address, and the
   variant or product it concerns. An invalid address is rejected with the field named and nothing
   is written.

### The reading routes

1. **Home** is four full viewport product panels stacked, then the footer. It is not a
   merchandising grid: it carries no product card, no price, no availability, no promotional
   ticker, no countdown, no sale banner and no video that starts by itself. Panel one is the
   flagship phone with the eyebrow `phone ( 5a ) pro` and the headline
   `Stay with the moment, not the screen`. Panel two is the second phone with the eyebrow
   `phone ( 5a )` and the headline `Watch your delivery arrive on the back of it`. Panel three is
   the headphones with the eyebrow `headphone ( 2 )` and the headline `Sound shaped with Vox`.
   Panel four is the operating system release with the eyebrow `HalcyonOS 4.1`, the headline
   `Open beta, out now` and the body
   `Try HalcyonOS 4.1 early and help us settle it before the general release.` The first three
   actions read `DISCOVER` and lead to that device's product route; the fourth reads `LEARN MORE`
   and leads to the operating system release route.
2. **Brand story** at `/about` opens with one large statement paragraph preceded by a small filled
   square in the brand red, reading
   `Halcyon builds phones, audio products and small tools that look good and make the day easier.
   With a community of over six million people, we are building the most loved technology brand
   for the next generation of makers.` Four numbered movements follow, headed
   `Arguing with the default`, `A life with fewer interruptions`, `Different on purpose` and
   `Made with the people who use it`. The first carries a three item list reading
   `Work with the outsiders`, `Let the people who buy it shape it` and
   `Do the things a large company cannot`. The second carries a figure pair, `30+` over
   `Product releases` and `60+` over `Countries`. The third carries a pull quote reading
   `'A window left open' , Argus`. The fourth carries paragraphs and an image. A position readout
   of eight segments sits at the right edge, the segment for the movement occupying most of the
   viewport filled in the brand red; it is a readout and not a control, so it does not respond to
   a click and offers no pointer cursor.
3. **Operating system release** at `/halcyonos-4-1` is the only route that ships the dark theme
   and the only route that uses the interface sans for body copy. It carries a hero with the
   product name, one line of body and a play control; three movements, each with a heading, a line
   of body and two or three feature cards; and a feature grid. A feature card carries a device
   screenshot on a fine ruled ground, a heading and a paragraph. Movements two and three carry
   previous and next controls. The play control starts a video: nothing on this route plays by
   itself, nothing plays with sound until it is asked to, and captions are available.
4. **Community grant programme** at `/lower-ground` is a grant programme for music collectives,
   titled `Lower Ground`, and is the one route that leaves the greyscale entirely. It carries a
   title, eight centred paragraphs, a status line, a terms list of four questions and a three item
   criteria list. The opening paragraph reads
   `This summer we are picking the electronic music disruptors we like best and putting them in
   the strangest rooms we can find.` and the second reads
   `Expect the artists you wish you had seen, and the crowd you will want to know.` The offer
   reads
   `We are giving four collectives ten thousand each to put on the biggest night they have ever
   run.` The disclaimer reads `This is not a corporate function.` and the invitation reads
   `Surprise us.` The status line reads `Applications closed.` and appears twice, once ending the
   manifesto and once ending the terms, because it is content rather than a component. The four
   questions read `How do I apply?`, `What do I get if I win?`, `How will you choose?` and
   `Is this open everywhere?`; the three criteria read `Inventive`, `Loud` and
   `Built on a community`. Applications are taken by an outside form service, so the catalogue
   stores no application record and holds no table for one. The application panel is mounted only
   when the route is reached, never blocks the route from rendering, falls back to a plain link
   when scripting is unavailable, and receives no identifier this app holds about the visitor.
5. **Standing pages** are the privacy policy, the warranty policy, the user agreement, the
   acceptable use policy and the terms of sale. One template: an effective date in the mono face
   above the title, the title, and an editorial body held to a single narrow column rather than
   filling the width, because legal copy runs long and a full width measure is unreadable.

### Not found, and the ladder of failures above it

1. An address that matches no route renders this product's own not found surface **and answers
   not found**. It must not render an empty application shell with the correct status, because an
   empty shell served for every address is what makes addresses that do not exist look real.
2. The surface carries the numeral `404` set in the label face at display size, centred, above a
   card carrying the heading `Page Not Found`, a small mark at its top right inheriting the text
   colour, one sentence of body reading
   `This page may have been removed, or you typed in the wrong address.` and a full width action
   reading `BACK TO HOME` that returns to the home route.
3. A family that exists and holds no products renders the empty listing surface, not a not found.
   A product that exists and holds no variants renders the same empty surface.
4. A family slug outside the closed set renders the not found surface.
5. **When editorial content is unavailable the product route still renders its catalogue data and
   omits the editorial block.** The catalogue data and the editorial content come from two
   different sources, and one being unavailable must not take the other down.
6. When catalogue data is unavailable the route renders a retry surface using the same card
   treatment as the rest of the product, and nothing crashes.

### What the browser downloads

1. Every public route carries its own title and its own description, and no two public routes
   share either.
2. Every public route declares a social preview title and a social preview image, and the image
   resolves.
3. The site serves a favicon at `/favicon.ico` and declares it in the document head.
4. `/sitemap.xml` lists every public route, and `/robots.txt` points at it.
5. No credential, API key, database address or administrative token appears in anything the
   browser downloads: not in a page, not in a script, not in a style sheet, not in a comment and
   not in an inline data block.

## User flow

Navigation is not a bar. There is exactly one persistent control on every catalogue route, a
floating pill in the top centre of the viewport carrying a menu toggle on the left and the
wordmark in the centre. Every destination below is reached from the drawer that toggle opens, from
the footer, or from the support centre's own bar.

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home, four full viewport product panels | public |
| `/collections/phones` | Phones family listing | public |
| `/collections/audio` | Audio family listing | public |
| `/collections/wearables` | Wearables family listing, seeded empty | public |
| `/collections/arc` | Arc family listing | public |
| `/products/phone-5a-pro` | Product route | public |
| `/products/phone-5a` | Product route | public |
| `/products/headphone-2` | Product route | public |
| `/products/earbud-3a` | Product route | public |
| `/products/arc-buds-1` | Product route | public |
| `/products/arc-watch-2` | Product route | public |
| `/products/phone-5a-pro/specifications` | Grouped specification table, one per product | public |
| `/cart` | Cart route, the drawer laid out full width | public |
| `/about` | Brand story | public |
| `/halcyonos-4-1` | Operating system release, the one dark route | public |
| `/lower-ground` | Community grant programme | public |
| `/pages/support-centre` | Support centre landing, its own chrome | public |
| `/pages/support-centre/articles/battery-drains-overnight` | A seeded article, with `set-up-your-new-phone` and `check-your-serial-number` | public |
| `/pages/contact-support` | Support request form | `owner` |
| `/pages/my-devices` | The owner's registrations and their requests | `owner` |
| `/pages/privacy-policy` | Standing page | public |
| `/pages/warranty-policy` | Standing page | public |
| `/pages/user-agreement` | Standing page | public |
| `/pages/acceptable-use` | Standing page | public |
| `/pages/terms-of-sale` | Standing page | public |
| `/account` | Sign in and registration, its own shell | public |
| `/sitemap.xml` | Every public route | public |
| `/robots.txt` | Points at the sitemap | public |
| `/favicon.ico` | The site icon | public |
| anything unmatched | Not found, answering not found | public |

Four destinations are owned by other origins, linked to and never rendered here: the payment step
that the cart hands over to, the community forum, the careers site and the experiments site. Each
is a real anchor to a fixed address, opened by the visitor, and this app never calls any of them.

**Entry and redirects.** An anonymous visitor reaching `/pages/contact-support` or
`/pages/my-devices` is sent to `/account` and returned to the route they asked for once signed in.
Signing out returns to `/`. A token that expires part way through the request form leaves the
typed body in place and offers sign in again rather than discarding it. An `owner` reaching a
registration or a request that belongs to somebody else is refused, not redirected into a blank
version of that surface. `/account` signed in shows the account rather than the sign in card.

**Journeys.**

1. **Resolve a variant.** Open `/`. The first panel names `phone ( 5a ) pro`; press `DISCOVER`.
   On `/products/phone-5a-pro`, open the colourway selector and choose `Midnight`. The capacity
   `8 GB / 128 GB` is shown and is not choosable. Choose `12 GB / 256 GB`. The thumbnail and the
   gallery swap to that colourway's media, the address now carries
   `phone-5a-pro--midnight--12-256`, and the action reads `ADD TO CART` because that variant is
   `direct`. Reload the page: the same colourway, the same capacity, the same media and the same
   action come back.
2. **Follow a handoff.** Open `/products/phone-5a`. Choose the colourway `Chalk`. The action reads
   `SHOP ON Bazaario` and is an anchor whose destination can be previewed before it is followed.
   Follow it: one outbound click row exists for `phone-5a--chalk--8-128`, and no order, no invoice
   and no revenue row was written.
3. **Filter a family.** Open `/collections/phones`. Seven cards, one per variant, and none of them
   shows a price. Choose the colourway `Chalk` and the capacity `12 GB / 256 GB`: one card
   remains and the address carries both choices. Press the browser back button: the capacity
   choice is undone and six cards return, and the route has not been left.
4. **Fill a cart.** Open `/products/headphone-2`, choose `Black`, press `ADD TO CART`. The cart
   drawer slides in from the right carrying one line. Close it, reload the page, open `/cart`: the
   line is still there with the same total. Press the checkout action: it is an anchor to the
   payment origin carrying the cart identifier, the region and the language, and nothing in the
   cart is cleared by leaving.
5. **Register a device and ask for help.** Open `/account`, sign in as `owner@example.com` with
   `deku-demo-pw-2026`. Open `/pages/support-centre` and open the registration panel. Enter
   `HLC-3M08XT55`: the panel names `headphone ( 2 )` before the registration is confirmed.
   Confirm it, and no mail is sent. Open `/pages/contact-support`, choose that registration,
   choose the category `Battery`, write a body and submit. A reference in the `SR-` form is shown,
   and one message arrives at `owner@example.com` whose subject begins `Support request ` followed
   by that reference. Submit the identical form a second time: the same reference comes back, no
   second request exists, and no second message arrives.
6. **Be refused.** Still signed in as the first owner, try to register `HLC-9P61BW73`, which
   belongs to `owner2@example.com`. The attempt is refused and the wording names neither that
   account nor its address. Try `HLC-0000ZZZZ`, which is well formed and names no product: refused
   as invalid. Try a serial too short to match the shape: refused as invalid, with the field named.
7. **Vote on an article.** Open any article from `/pages/support-centre`, answer
   `Was this page helpful?` with `Yes`. Both controls give way to an acknowledgement in place.
   Reload and answer `No`: the stored answer changes and no second vote exists.
8. **Miss.** Open an address that matches no route. The not found surface renders with the numeral
   `404`, the heading `Page Not Found` and the action `BACK TO HOME`, and the response says not
   found rather than serving an empty shell.

**States.** Every listing has an empty state that names the family, says in one line that there is
nothing here, and offers a control clearing every facet. Every listing has a loading state built
from card shaped placeholders at the card width. The cart has an empty state that is a heading and
one action. The registration panel and the request form each show their errors beside the field
that caused them, in words rather than by a change of border colour alone, and keep everything
else the visitor had typed. A refusal never leaves a half written row behind: a rejected
registration writes nothing, and a rejected request writes nothing and sends nothing. No failure
of any kind renders a blank page or an unhandled error.

## UI/UX notes

**North star.** Somebody arriving should understand within one screen that this is one brand
showing its own few devices, and should feel that the emptiness around each device is deliberate
rather than unfinished.

**Register.** Consumer and editorial, with one exception. The device itself is the first thing
seen and the interface around it is almost silent: one product to a screen, a great deal of space,
and no decoration standing in for content. The exception is the support centre, which inverts the
register on purpose, because when something is broken a person wants signposts rather than
restraint. Build both, and do not unify them.

**Space over dividers.** Sections and panels read as separate because of the air around them and
because of one step of surface separation, never because a rule was drawn between them. **Stillness
over expression.** The feeling of movement comes from the weight of the scrolling rather than from
anything on the page performing. **One statement per screen over density**, everywhere except the
support centre and the owner's own device list, which are the two places a person is scanning for
something specific and where rows may sit tight enough that a full list fits one screen.

**Colour.** The ground is a near-white neutral, not white, and cards on it are the near-white
neutral at the top of the same ramp. That single step of separation is the whole elevation model:
a default card carries no shadow, and if a build needs a shadow to tell a card from its ground the
two steps are wrong. Between those ends sits one ramp of neutrals carrying hairline rules,
disabled fills and text, placeholder text, captions, labels, body copy and headings, in that order
of emphasis. Three colours carry meaning and are rationed almost to nothing: a deep, vivid red
that appears only as the square opening the brand statement, as the filled segment of the position
readout and as a small marker cluster on device art; a vivid amber that appears once, as a single
dot on an editorial image card; and a deep, vivid blue reserved for something purely
informational. Nothing else on a default page is coloured, and a build that spreads either of the
first two across buttons or links has reproduced the palette and missed the system. The exact
values are yours, so long as body text clears WCAG AA contrast against whatever it sits on in both
themes, the ramp steps stay distinguishable from one another, and the red is never used as text at
body size on the light ground.

**Type.** Four families, each with exactly one job, and consolidating them is the single fastest
way to make a correct build look wrong. `Domine` sets every headline and every paragraph of body
copy. `Doto`, a face whose letterforms are built from discrete dots, sets the wordmark, every
label, every section numeral and every button, always in capitals and never as running copy.
`IBM Plex Mono` sets figure captions, pull quotes and small print. `Geist`, with its monospace
companion, sets interface text on the operating system release route and nowhere else. Headline
and body carry real contrast in weight and scale so a headline reads as a title, the label face is
tracked loose enough to read as a readout rather than as a word, and figures line up in a column
wherever amounts stack. The one deliberate exception is the community grant route, which sets its
running copy in the label face because it is a poster rather than a page; that exception is scoped
to that route and nowhere else.

**Shape.** Three softness levels and no fourth: the grid dots and the support centre's search
field are fully round, a card or a panel is gently softened, and a button inside a card is
softened slightly less than the card that holds it. The difference between the last two is small
and it is the point: a build using one value for both looks nearly right and is wrong at the
corner where a full width button meets a card edge.

**Mode.** Light is the committed mode and is designed fully. Dark is designed fully too, but it
is scoped to one route, the operating system release, because that route describes a product
whose own interface is dark; the account surface offers a control that switches the whole
deployment and persists the choice. Every other route ships light, and a build that leaves the
light mode half finished because the dark one exists has inverted the commitment.

**Components and their states.** One main action style and one quieter alternative, and the main
one carries the strongest contrast on the page. Every control has a resting, a pointed-at, a
pressed, a focused and an unavailable state, and unavailable is never signalled by colour alone.
A field carries its label above it and its error beside it, in words. An overlay closes on the
escape key and returns focus to whatever opened it. Nothing here is destructive enough to need a
confirmation step, and none is invented for the sake of having one.

**Colour that carries meaning.** There is deliberately no danger colour, no success colour and no
in-progress colour in this palette. A failure is carried by the wording beside the field it
belongs to, a success by the acknowledgement that replaces the control that caused it, and
progress by the indeterminate pulse on a placeholder. That absence is the point: the three
accents are rationed to three places, and adding a fourth semantic hue would undo the restraint
the whole product is built on.

**Motion.** Small, fast and almost entirely a change of opacity. Two hover states exist across the
whole catalogue and that is the complete set: a primary button whose fill becomes slightly
transparent, letting whatever is behind it show through, and any link or footer row whose opacity
drops a little. Nothing underlines, scales, shifts colour or translates. Every state change a
person caused moves on one shared easing character, quick enough to read as a material response
rather than as an animation; anything that arrives on its own decelerates into place instead.
Exactly three things move without being touched, and naming them is what keeps the rest still: one
small square before the brand statement breathes in and out continuously, the segments of the
position readout fill as the route is read, and two editorial containers drift very slightly with
the scroll. The scroll itself carries weight, so a flick continues and settles rather than
stopping with the fingers. The exact speeds and curves are yours, so long as everything a person
caused shares one character and nothing uses a different speed to feel special.

**Accessibility.** This design is unusually hostile to a careless build and the reasons are
specific. Every icon is a field of dots and conveys nothing to somebody listening, so every one
carries an accessible name. All navigation hides behind one toggle, so that toggle is the first
focusable element on the page and it says what it is. Links that leave the site look exactly like
links that do not, so leaving must be announced, and the handoff action matters most because it
leaves in the middle of a purchase. The grid layer is thousands of elements, so it is hidden from
assistive technology entirely and never takes focus. The label face runs small, so it must survive
a text size increase without clipping. Every field carries a visible persistent label rather than
a placeholder doing that job, errors are stated in words and tied to their field, keyboard
navigation reaches everything with a visible focus ring, touch targets are comfortably sized, and
meaning is never carried by colour alone. When reduced motion is asked for, the weighted scrolling
is switched off and the native behaviour returns, the breathing square stops at full opacity, and
transitions become instant rather than disappearing; the position readout keeps updating, because
it is information rather than decoration.

**Responsive.** The layout holds at every width between the named tiers and nothing overflows
sideways on a phone. Three changes are structural and may not be collapsed into a fluid scale: the
width at which the chrome goes narrow, the width at which the floating pill and every anchored
card snap from their wide fixed width to their narrow one rather than interpolating between them,
and the width at which the product route abandons its scattered constellation and stacks every
card in a single column in authored order. Everything else is type and spacing and may be made
fluid. The grid dots keep the same spacing at every viewport, so a narrow screen shows fewer of
them rather than smaller ones, which keeps them reading as a printed texture rather than as a
pattern that stretches.

**What it must not look like.** Not a conventional shop: no persistent cart badge, no search field
in the catalogue chrome, no breadcrumb, no sticky add to cart bar, no back to top control, no
suggested products in an empty cart. Not a marketing landing page: no hero carousel, no
testimonial band, no countdown, no interstitial. And not a house style wearing this palette: if
the dot field, the label face and the one statement per screen were removed and the result still
read as this product, the character was never built.

## Technical requirements

The application is server rendered. Catalogue routes produce their product and editorial content
on the server, so a route that does not exist answers not found rather than handing back an
application shell that a crawler and a person both read as real, and every product route is
legible to a search engine without running a script.

Stack: Django serving its own templates on the backend, with progressive enhancement in the
browser and no client side framework. Storage is `postgres`, reached at `DATABASE_URL`, which is
also published as `DB_URL` with the same value. Mail is `mailpit`, reached over real SMTP at
`SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. Authentication is email and password held
by this app, with a bearer token the client sends on authenticated calls, and passwords stored
hashed. `GET /api/health` returns `200` once the app is ready. Requests are logged to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are `postgres` and `mailpit`, and reaching for anything else is a
contract violation.

Read every address and port from the environment. Never hardcode a host or a port for any backing
service, and never hardcode `APP_PUBLIC_URL` or `APP_PUBLIC_PORT`.

Four shells share this deployment and are deliberately not one layout tree. The catalogue shell
carries the dot grid, the floating pill and the weighted scroll. The support centre shell carries
a full width top bar, visible links and a search field, and carries no dot grid. The account shell
carries neither the grid nor the pill, sets the wordmark vertically at the left edge, and offers a
theme control. The payment step is not in this deployment at all. Merging the three that are here
into one shell destroys differences this brief requires, so keep them separate.

Three pieces are written once and shared by everything that needs them: the centring utility used
by both the floating pill and every anchored panel card, which is why the two share their measured
offsets; the dot mark generator, which turns a list of centres into a mark; and the card, which
owns one softness, one fill and one frosted variant. An icon is a row in a registry mapping a name
to a list of centres. No icon is a file and no icon is a component of its own. Those primitives
carry the two riskiest parts of the build, the dot system and the buy route, so the honest order
is to prove them against a light ground, a dark ground and a saturated ground before anything
expensive is built on top, and to seed both fulfilment modes from the moment product routes exist
rather than after.

Facet selection, sort selection and variant selection all live in the address. That is what makes
a filtered listing and a chosen colourway into links somebody can send, and the product route
depends on it. Cart contents live on the server keyed by an anonymous identifier in a first party
cookie. Drawer state, gallery state and the gallery index are local to the page and do not survive
a navigation. The theme is a class on the root element and persists in the browser.

Modules load per route rather than per site. The video substitute loads on the operating system
release route only. The cart client loads on routes that carry a cart affordance and not on
editorial routes. The scroll driven work loads on the brand story and product routes only. The
community route's application panel loads only when that route is reached. The not found surface
loads the grid, the pill and nothing else.

Performance obligations. Scrolling any route drops no frame on an ordinary three year old laptop.
The dot grid layer is built once when the window opens and again on resize, is excluded from hit
testing, carries no filter and no transition of its own, and is never rebuilt while scrolling; if
that cannot hold the frame budget with elements, a single canvas or a tiling pattern may be
substituted provided the circular apertures survive the substitution. The first panel image is
prioritised and preloaded; every later one loads lazily. Images reserve their space before they
arrive so nothing shifts after first paint, and arrive faded rather than partially painted. Only
two families load before first paint, the display serif and the label face, both subset to the
characters actually used, each declaring a metrically compatible fallback so the swap does not
reflow; the interface sans loads on the operating system release route only.

Every public route carries its own title and its own description, and no two public routes share
either. Every public route declares a social preview title and a social preview image, and the
image resolves. A favicon is served at `/favicon.ico` and declared in the document head.
`/sitemap.xml` lists every public route and `/robots.txt` points at it. Nothing the browser
downloads carries a credential, an API key, a database address or an administrative token, in any
page, script, style sheet, comment or inline data block.

The app makes no network call to any other origin while it is running. Outbound destinations, the
retailer, the payment step, the community forum, the careers site and the experiments site, are
rendered as real anchors carrying real addresses and are followed by the visitor, never fetched by
the server.

## Data model

Fifteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`families`** - `slug` unique and drawn from the closed set `phones`, `audio`, `wearables`, `arc`;
`name`; `order`. Four rows.

**`products`** - `slug` unique; `family_slug` referencing `families`; `name`, which is the lower
case bracketed form with its literal inner spaces; `order`, which is the featured order;
`release_date`; `has_capacity_axis`. Six rows.

**`variants`** - `variant_id` unique, formed as `<product-slug>--<colourway-slug>--<capacity-slug>`
with the capacity segment omitted where the product has no capacity axis; `product_slug`;
`colourway`; `capacity`, null where the product has no capacity axis; `buy_route`, one of
`direct`, `handoff`, `unavailable`; `available`; `unit_price_minor`, an integer in the minor unit
of `usd` and null on every variant whose `buy_route` is not `direct`; `media_seed`, the value the
procedural media recipe is seeded from so the same variant always produces the same image.
Fourteen rows. A colourway and a capacity together identify at most one row for a product, and the
pair `Midnight` with `8 GB / 128 GB` on `phone-5a-pro` has no row at all.

**`panels`** - `slug`; `family_slug`; `eyebrow`; `headline`; `body`, nullable and present only on
the operating system panel; `action_label`; `action_href`; `order`. Four rows for the home route.

**`constellation_cards`** - `product_slug`; `kind`, one of `film`, `spec`, `image`; `caption`;
`kicker`, nullable; `x_percent` and `y_percent`, which are positions expressed as a share of the
route box and are authored per product rather than computed; `size`, drawn from a small closed set
rather than being a free measurement; `order`, which is the order the cards stack in when the
scatter is abandoned at narrow widths.

**`movements`** - `route`; `index`; `heading`; `blocks`, ordered; `theme`. The brand story route's
four movements and the operating system release route's three.

**`articles`** - `slug` unique; `category`, drawn from the seven support categories; `title`;
`body`; `steps`, ordered; `related`, a list of article slugs.

**`accounts`** - `email` unique and compared without regard to case; `password_hash`; `created_at`.
Two seeded rows, `owner@example.com` and `owner2@example.com`.

**`carts`** - `id`; `anonymous_id`; `account_id`, null until the cart is reconciled onto an
account; `state`; `updated_at`.

**`cart_lines`** - `cart_id`; `variant_id`; `quantity`; `unit_price_minor`; `line_total_minor`;
`excluded`, true once the variant it names has left `direct`. A line always names a variant that
exists. An excluded line is kept and is left out of the total.

**`registrations`** - `id`; `account_id`; `product_slug`; `serial`; `registered_at`. A serial
appears at most once in this table, so a second attempt to register the same serial does not
create a second row whichever account makes it, and the refusal that comes back names neither the
holding account nor its address.

**`support_requests`** - `id`; `registration_id`; `category`, drawn from the closed set `Setup`,
`Battery`, `Connectivity`, `Software`, `Physical damage`; `body`; `attachment_key`, nullable;
`reference`, unique and formed as `SR-` followed by eight digits; `idempotency_key`, unique;
`created_at`. The `registration_id` must belong to the account making the request. An
`idempotency_key` appears at most once, so a repeated submission carrying the same key returns the
reference already stored against it and produces no second row and no second message.

**`intents`** - `kind`, one of `notify`, `tradein`, `repair`; `variant_id`, nullable;
`product_slug`, nullable; `email`; `payload`; `reference`; `created_at`.

**`article_votes`** - `article_slug`; `anonymous_id`; `helpful`; `updated_at`. The pair
`article_slug` and `anonymous_id` appears at most once, so a second answer from the same visitor
replaces the stored one and the count does not double.

**`outbound_clicks`** - `variant_id`; `destination`; `anonymous_id`; `created_at`. Written when a
handoff is followed. Nothing in this table is an order, an invoice or revenue, and nothing else
writes a row here.

Derived rather than stored: a line total, which is the quantity times the unit price read back;
the cart subtotal and total, which exclude every marked line; the facet value lists on a listing,
which are the union of what the result set actually holds; and the resolved variant on a product
route, which is read from the stored rows rather than assembled in the browser.

Seed data is exactly the matrix in Core features, plus four serials: `HLC-7K42QD19`, registered to
`owner@example.com` against `phone-5a-pro`; `HLC-9P61BW73`, registered to `owner2@example.com`
against `phone-5a`; `HLC-3M08XT55`, unregistered and resolving to `headphone-2`; and
`HLC-0000ZZZZ`, well formed and resolving to no product at all.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

### The colour system

The palette is a greyscale ramp plus three accents, and it is declared once on the root element in
a form that lets every consumer apply its own transparency, so a single ramp step can be used at
full strength as a fill and at partial strength as a wash without a second declaration.

The ramp has thirteen roles, in order from lightest to darkest, and each one has exactly one job:
card fill and reversed text at the top; then the page ground in the light theme; then hairline
rules; then the fill of a disabled control; then the text inside a disabled control; then the
midpoint of the ramp, which is placeholder text; then the secondary caption; then the tertiary
label; then low emphasis body on the light ground; then body copy; then headings on the light
ground; then the near-black that fills the primary action and sets text on the light ground. Two
further roles carry the dark theme: its page ground, which is the same near-black, and its raised
surface, which is a step lighter. Two absolute ends of the ramp are also declared for consumers
that cannot take the transparency form: a pure near-white neutral and a pure near-black neutral.

Three accents, and they are rationed. The brand red is a deep, vivid red and appears in exactly
three places on the whole site: the filled square before the brand statement headline, the filled
segment of the position readout, and a small marker cluster on device art. The secondary accent is
a vivid amber and appears in exactly one place: a single dot at the top right of an editorial
image card. The tertiary accent is a deep, vivid blue and is informational only. Nothing else on a
default page is coloured. A build that spreads either of the first two across buttons or links has
reproduced the tokens and not the system.

Normative: the page ground in the light theme is the off-white ramp step, not white, and cards on
it are the white step. That one step of separation is the entire elevation model, and there is no
shadow on a default card.

### Theme

Two themes, selected by a class on the root element rather than by a media query. The body carries
the light ground unconditionally and the dark ground under that class, so a route opts in by
setting the class on the server rather than by shipping a second style sheet. The operating system
release route ships dark; every other route ships light. A control at the top right of the account
surface toggles the class, and the choice persists. The operating system preference is honoured on
first load and an explicit choice overrides it thereafter.

### Typography

Four families, each with exactly one job. This is the part of the system a build is most likely to
get wrong by consolidating.

| Family | Job |
|---|---|
| `Domine` | every headline and every paragraph of body copy |
| `Doto` | the wordmark, every label, every section marker numeral, every button |
| `IBM Plex Mono` | figure captions, pull quotes, small print |
| `Geist`, with its monospace companion | interface text on the operating system release route only |

The dot matrix family declares two unusual weights of its own, a regular and a bold that are not
the conventional pair, and a build that maps them onto the conventional pair selects the wrong
face. Reproduce the two the family declares.

The scale carries two dominant rows and a handful of specials. Body copy is the default and its
line height is a little under one and a half times its size, which is what keeps a long editorial
paragraph readable. The dot matrix label is much smaller than body copy and its line height is
barely above its size, which is what makes a row of labels read as a readout. Above those sit the
panel headline, whose line height equals its size so that two lines read as one block; the brand
statement headline, which is the largest thing on the site and is set lighter than body copy; the
secondary headline used for movement headings and card headings; the caption; the legal small
print, which is the smallest thing on the site; and the form label. The wordmark sits in its own
row, set in the dot matrix face with a line height well under its size.

Normative: the dot matrix face is never set smaller than the label size and never larger than the
section marker size, outside a page title. Letter spacing on that face is loose, and that is what
makes it read as a label rather than as text. The wordmark is tracked so that its characters span
twice the offset the pill is pulled back by at the narrow layout, which is what makes it fill the
pill rather than float in it.

Fallback stacks are normative, because the families are the one asset class this brief does not
replace procedurally. Each of the four names an open family and a generic fallback: a serif for
the display role, a monospace for the dot matrix role and for the mono role, and a system sans for
the interface role.

### Softness, spacing and stacking

Three levels of softness and no more. The grid dots and the support centre search field are fully
round. Every card and every panel is gently softened. Every button is softened slightly less than
the card that holds it. A card and the button inside it are close enough that a build using one
value for both looks nearly right and is wrong at the corner where a full width button meets a
card edge.

Six spacing roles carry names because other things are measured against them: the height of the
floating pill, which is also the offset an anchor scrolls to; the dot grid cell; the product card
width in a family listing; the cart drawer width; the fixed height of that drawer's summary block;
and the taller fixed height the same block takes when a discount row is present. Two further
properties drive the grid layer's top and bottom edge fades, both at full strength at rest.

Stacking is four levels and no more: the grid layer behind everything, page content above it, the
anchored panel card above that, and the floating pill and any overlay above all of them. A build
that introduces a fifth has a layering bug it has papered over.

### Iconography: there are no icon shapes, only dots

Every icon on this site is a field of identical circles placed on a square grid of sixteen units
by sixteen, drawn as filled paths that take their colour from the text around them. A circle sits
on an integer centre and adjacent circles at a two unit pitch touch without overlapping, so a
diagonal run reads as a dotted line rather than as a stroke. Every icon has no stroke of its own
and no colour of its own.

This is not a stylistic note. It is why the icon set needs no font and no binary: an icon in this
system is a list of centres, and one generator turns a list of centres into the mark. The registry
is a map from a name to a centre list, and adding an icon is adding a row to that map. A build may
emit the circles as paths or as circle elements; the two are equivalent.

Six marks are specified by their centre lists, and the centre list is the entire specification:

- **Menu toggle.** Twelve dots in two rows of six. The upper row sits near the top of the grid and
  the lower row near the bottom, and the gap between them is wider than a conventional menu mark.
  That gap is deliberate: at the size it renders, the mark reads as two rules rather than three,
  and the missing middle row is a large part of why the brand looks like itself. It is carried in
  the floating pill at the left, inset from the pill edge by about a quarter of the pill's height.
- **Caret.** Five dots forming a shallow chevron whose apex is at the bottom, so the mark points
  down at rest. It is used on every selector in a buy panel and on every accordion row. The open
  state rotates the whole group by half a turn rather than swapping in a second mark.
- **Help.** Ten dots tracing a question mark, used on the support entry in the drawer and in the
  footer. One dot is detached and sits below the stem: it is the full stop of the question mark,
  and it is what keeps the mark legible at label size.
- **Newsletter.** Twenty three dots, of which twelve were recovered whole; the remainder are
  completed by the reconstruction rule below.
- **Store selector.** Twenty one dots, of which twelve were recovered whole; the remainder are
  completed by the same rule.
- **Account.** One dot recovered near the top of the mark; the remainder is a reconstruction.

**The reconstruction rule.** Where a centre list is incomplete the build does not invent a
different mark. It completes the list under three constraints, all of which the fully recovered
marks satisfy: every centre is an integer coordinate inside the grid; no two centres are closer
than the two unit pitch; and the mark is symmetric about the vertical middle unless the recovered
dots already break that symmetry, which for the newsletter and store marks they do not. The
recovered store selector dots along its top row are symmetric about the middle, so the missing
dots complete a symmetric figure.

Normative: icons inherit colour from their parent and are never given a colour of their own. That
is what lets the same menu toggle sit on a white pill on the home route and on a saturated pink
pill on the community route without a second asset.

### The dot grid layer

The dominant surface of the site and the thing every screen has in common. It is a full viewport
field of small dots, fixed behind the content, painted in a mode that inverts against whatever is
under it.

It is positioned fixed and covers the viewport; it receives no pointer events; it sits at the
bottom of the stacking order; it is drawn at low opacity; and it is blended by difference against
what is behind it. A dot is a tiny square with a full radius, pulled back by half its own size on
both axes so it straddles a cell boundary rather than sitting inside it.

**The blend mode is the whole effect.** A dot blended by difference against the off-white ground
resolves to a light grey; the same dot against a dark photograph resolves to a light dot; against
a mid grey it nearly vanishes. The grid therefore reads as printed onto the page in every context
with no per route colour specified anywhere, and it is why the community route can be saturated
pink and the operating system route near black with one single layer over both.

Normative: the layer is one fixed element and does not scroll. Content moves under a stationary
grid. A build that attaches the grid to the document instead of the viewport produces a subtly
different and much busier page.

**Structure.** Each cell is a positioned container carrying dots at three of its corners, at its
top left, its bottom left and its top right, each pulled back on both axes. That corner sharing is
what keeps the count finite: a grid of cells produces one more dot than cells in each direction
rather than four dots per cell. The build generates the grid from the viewport size and the cell
size and regenerates it on resize. It must not be a repeating background image, because the
apertures below need individual dots to be addressable.

**The masked apertures.** Two circular holes are punched in the layer, a smaller and a larger,
both centred above the visual middle of the viewport, so that a product photographed against the
ground sits in clean space rather than in a field of dots. The two sizes correspond to the two
product panel scales. Two linear fades run on the same layer at the top and bottom edges, at full
strength at rest, so a route can fade the grid out against a full bleed image without removing it.

**Registration marks.** On the brand story route the grid gains four small plus marks, one at each
corner of the content column, set in the mono face. They are content rather than part of the grid
layer, and each registration mark marks a column edge the way a print registration mark does. They
appear on that route only.

**Performance.** The layer must not cost a frame. On a large viewport it is several thousand
elements, so it is built once, marked as non interactive, excluded from hit testing, and left
alone until a resize. It is never rebuilt on scroll. If a build cannot hold the frame budget with
elements it may substitute a single canvas or an inline tiling pattern, provided the apertures
survive the substitution.

### Global chrome

Three pieces, and only the first is visible at rest.

**The floating pill.** The single persistent control on every catalogue route. It is fixed,
horizontally centred by being pinned to the middle of the viewport and pulled back by half its own
width, and it carries the menu toggle at its left and the wordmark at its centre. It has one
width at the wide layout and a narrower one below the structural width where they swap, and it
snaps between the two rather than scaling fluidly; a build that centres it by a proportional
transform lands correctly at those two widths and diverges at every width between them.

There is no cart count, no search field and no account link in the pill. Every one of those lives
in the drawer. This is the most distinctive structural decision on the site and the one a build is
most likely to undo. The pill does not hide on scroll, does not shrink, and does not change fill.
It is the same object at every scroll position on every catalogue route. The only thing that
changes is its fill on a themed route, where it takes a lightened tint of the route ground rather
than white.

**The drawer.** Opened by the menu toggle, occupying the full viewport, above everything. It
carries every destination in two groups. The primary group is set in the display serif at the
panel headline size and holds: About, leading to the brand story route; the operating system name
and version, leading to that route; Community, an outbound link to the forum; the community grant
programme name, leading to that route; and Playground, an outbound link to the experiments site.
The utility group is set in the dot matrix face at label size and holds: Support, leading to the
support centre; Newsletter, opening the subscribe form; a store readout; a language readout; and
Consent Preferences, opening the consent manager.

The readout rows set the label, the colon and the value as three separate inline elements, so the
colon keeps the label's tracking rather than the value's. Reproduce that, or the row reads as a
sentence instead of a readout. The store readout reads `Store` then a colon then `India`, and the
language readout reads `Language` then a colon then `EN`.

Outbound rows carry no visual difference from internal rows. That is deliberate, and the
obligation it creates is in the accessibility section below. A scroll that reaches the end of the
drawer does not continue into the page beneath it.

**The footer.** A single band at the foot of every route carrying the utility rows above plus:
Account, an outbound row in the account shell; Contact, which names the support address
`support@halcyon.in`; Careers, outbound; Legal, leading to the standing pages; and the four social
destinations, all outbound. Every footer link fades a little when it is pointed at.

**What the chrome deliberately does not have**, recorded because a build will otherwise supply
these by habit: no breadcrumb on any route; no sticky add to cart bar on the product route; no
cookie banner in the default state, because consent is a drawer row; no back to top control; and
no search field anywhere in the catalogue chrome. The support centre is a separate application
with its own chrome and its own search, and the two must not be unified.

### Motion

The motion here is small, fast and almost entirely a change of opacity. There is no long scroll
scrubbed timeline and no entrance choreography on the commercial routes.

Three easings carry every movement here and there is no fourth. Anything that changes because a
person did something moves on the default easing. Anything that arrives on its own uses a second
easing that decelerates into place and does not accelerate out of rest. One looping pulse has a
third easing of its own and appears nowhere else. Several further easing curves were measured on
the surfaces this deployment links out to rather than on the catalogue itself, and none of them
belongs here: a build must not adopt an easing by copying it from a neighbouring style sheet.

The complete hover catalogue is two entries, and that is the measured total rather than a summary.
A primary button's fill becomes slightly transparent when it is pointed at. Any link or footer row
drops a little in opacity when it is pointed at. Both land on the same idea: the element gets
slightly lighter and nothing moves. There is no underline wipe, no scale, no shadow, no colour
shift and no translation anywhere in the catalogue, and a build that adds one has added a house
style that is not this one. Normative: the button hover changes the transparency of the fill, not
the fill colour, because the button sits on a white card in some places and on a photograph in
others, and a transparency change lets the ground show through in the second case. A disabled
control drops to a low opacity.

Durations are ordered rather than measured here. The fastest and by far the most common change is
the link and label opacity change; it is fast enough to read as a material response rather than as
an animation, and getting it right is most of what makes a build feel like this product. A button
changing its fill, its border and its colour, and the caret rotating, take a little longer than
that. Colour only changes and small entrances sit between them. A panel's opacity takes longer
still, an image's opacity and a panel's transform longer again, and the determinate progress width
is the longest thing on the site. Nothing in the catalogue takes longer than that progress bar,
and it is a progress bar rather than a transition.

Seven moments carry keyframes of their own and they are the complete set. Many more keyframes were
measured across the wider capture and they belong to the account surface, to loading states and to
embedded players rather than to this catalogue, so a build defines these seven and no others:

- a pulse that halves opacity at its midpoint, used on the accent square and on indeterminate
  loading;
- a spin, used on the determinate spinner, running evenly and without end;
- a marquee that translates a duplicated track by exactly one copy width, in each direction, which
  is why the distance is a proportion rather than a measurement;
- a ticker in which a single element crosses the viewport from off one edge to off the other;
- a determinate progress fill that grows from nothing to full width;
- one hero entrance that starts enlarged, passes through a middle state that is smaller and pushed
  downward, and settles at rest, so the element settles rather than simply shrinking. Reproduce
  all three stops; a two stop approximation reads as a zoom.

**The scroll engine.** Every catalogue route replaces the browser's native scroll response with an
inertial one, damping wheel and trackpad input so that a flick continues and settles rather than
stopping with the fingers. The page must remain at the browser's own scroll position for anchors,
for the browser's find, and for restoration on back navigation. Overscroll chaining is off, so a
scroll that reaches the end of the drawer does not continue into the page beneath it. The inertial
response is disabled outright when reduced motion is asked for.

**The measured exceptions.** Three, and only three, places move on their own or with the scroll,
and they are listed exhaustively because the rest of this section otherwise reads as a promise
that nothing moves. On the brand story route the accent square before the opening statement pulses
continuously; it is the only continuously running animation on the site and it runs on a mark the
size of a label. On the same route the position readout segments rotate and fill as the route is
read, and two editorial image containers drift very slightly. On the product route one circular
element transforms with the scroll.

### The product panel

One module accounts for most of the site. It appears four times on the home route, once per
product route, and in a reduced form on the family listing.

**Anatomy.** A panel is a full viewport section containing exactly two things: a product image
occupying the whole section, and a card anchored near its bottom. The section fills the viewport
height at minimum and takes the page ground. The image is centred and contained rather than
cropped, and sits inside the circular aperture cut in the grid. The card is anchored bottom
centre, pinned to the middle and pulled back by half its own width, above page content but below
the pill. The card takes the card fill or the frosted treatment, the card softness, and a fixed
width at each of the two layouts. The card and the pill share one centring utility and the same
pair of offsets, and a build should implement it once.

**The frosted variant.** Where a card sits over a photograph rather than over the flat ground it
takes a heavy backdrop blur with white at partial transparency over it. The blur is deliberately
large: it turns the photograph behind the card into a field of colour rather than a blurred image,
which is why text stays readable over an arbitrary product shot without a scrim. Where a backdrop
blur is unavailable or would cost the frame budget, the fallback is a flat fill at the average
colour of the region behind the card, never a semi transparent white, which fails contrast over a
light photograph.

**Card contents**, top to bottom, in the same order on every panel: an eyebrow carrying the
product name in the dot matrix face with the spaced bracket convention; a headline in the display
serif, at most two lines, whose line height equals its size so the two lines read as a block; an
optional body paragraph in the display serif, present only on the operating system panel; optional
feature rows, present on the product route only, each a dot mark followed by an all capitals dot
matrix label; optional selectors, present on the product route only; and a single full width
action. On the product route a product thumbnail sits at the right of the card with a magnify
control at its lower right that opens the gallery.

**The action button.** One button style exists on this site: a near-black fill, text in the dot
matrix face in capitals on the card fill colour, the button softness, the full width of the card,
and a transition on its background, border and colour on the default character. Its label is a
verb in capitals and is never sentence case.

**Panel sequencing on the home route.** Panels stack vertically and are separated by nothing: no
rule, no gap, no parallax offset. The transition between two panels is the panel edge itself. They
do not fade or scale into place; they simply arrive as the page moves. Do not add an entrance
animation to them. The stillness is the design and the weight of the scrolling supplies the sense
of motion.

### Route surfaces

**Home.** Four stacked panels and the footer, nothing else. The document carries a single top
level heading holding the wordmark, and each panel's headline is the heading beneath it while the
eyebrow is marked up as a label attached to that heading rather than as a heading of its own. That
preserves the visual result and removes the level skip a literal reading would produce. Each panel
image is a product rendered against the flat ground with a soft reflection beneath it, occupying
roughly the upper two thirds of the panel with the card overlapping its lower edge. The first
panel shows three colourways of one device standing side by side and slightly overlapping, back
faces to camera.

**Family listing.** A grid on the page ground whose item width is a fixed token rather than a
fraction. The grid fills the available width with whole items, left aligned and not stretched, and
leaves the remainder as trailing space rather than growing the items; that is what keeps a product
photograph at a consistent scale between a phone listing and an audio listing. Each card takes the
card fill and the card softness and carries three slots: the variant image on the flat ground, the
product name in the dot matrix face with the spaced bracket convention, and the colourway name in
the mono face. The facet controls and the sort control sit above the grid.

**Product.** A full bleed lifestyle photograph of a person using the device, bled to the top of
the viewport behind the floating pill and cropped at the sides. It is the only place on the site
where an image goes under the chrome, and the pill sits over it with its fill intact rather than
turning transparent. Feature cards are positioned around the central image rather than stacked
under it, and each is a small media tile with a caption beneath. A media tile takes the card
softness and sits somewhere between a thumbnail and a small card in size; its caption is display
serif and centred beneath it; an optional kicker in the mono face in capitals sits under the
caption. Two tile variants carry extra furniture: a film tile carries a play label at its top left
and a duration at its top right, both dot matrix on a translucent fill; a specification tile
carries a dot mark on a white ground rather than a photograph, and its caption is the word for
specifications. The scatter is authored per product, which is why two product routes look
genuinely different rather than like one template with different pictures.

The buy panel is the frosted card anchored bottom centre. It carries the product name, three
feature rows, the thumbnail with its magnify control, one selector per axis the product has, and
the action. Each selector shows its current value in capitals in the dot matrix face with the
caret to its right.

The gallery is a full viewport overlay above everything, showing the resolved variant's media one
image at a time, with the caret used as the previous and next controls and a close control at the
top right. It keeps focus inside itself, restores focus on close, and closes on the escape key.

The specification surface is a route of its own carrying grouped rows, labels in the mono face in
capitals and values in the display serif.

**Cart.** The empty state is a centred heading in the display serif on the flat ground with one
full width action beneath it in a column the width of a panel card. There is no illustration, no
suggested product and no recently viewed row: the route is two elements on an empty page under the
floating pill and the grid. The populated state carries lines and a summary. A line shows the
variant media at thumbnail size, the product name in dot matrix, the colourway and capacity in
mono, a quantity stepper and the line total. The summary is a block of one fixed height that swaps
to a second, taller fixed height when a discount row is present; it does not size to its content,
because a summary that grows moves the action beneath it when a discount is applied. The cart also
renders as a right hand drawer opened by an add, and the drawer and the route share one component
and one state. The drawer's outer width is the wider of the two measured values and the declared
token is the content column inside it.

**Account.** A separate shell, and its visual language deliberately differs from the catalogue's;
a build will otherwise unify them by accident. It carries a flat ground with no dot grid, no
floating pill, and the wordmark set vertically at the far left edge of the viewport, reading
bottom to top, vertically centred. That rotated wordmark is the identifying mark of this surface
and appears in only one other place, the brand story route. Headings are the display serif and
controls are the system sans. A theme control sits at the top right.

The sign in card is centred, narrow, softened, on the card fill, and carries in order: a heading
in the display serif at the panel headline size; an email field at full width with the button
softness and a hairline border; a password field the same, with a reveal control at its right; a
centred link for a forgotten password in the small print size; the submit control and two
federated identity controls in one row, the federated pair being circular and sitting on the page
ground; a consent line in the small print size, centred, carrying two inline legal links; and a
full width create account control on the page ground. The submit control renders disabled until
both fields carry something, filled with the disabled fill and set in the disabled text colour.

Three states must all be reachable: an unknown address, a wrong password, and both wrong. All
three show the same combined wording, because disclosing that an address is unknown turns the form
into a way of discovering which addresses hold accounts.

**Brand story.** A single opening statement paragraph in the display serif at the largest size on
the site, set lighter than body copy, indented from the left edge, preceded by a filled square in
the brand red sitting on the first line's baseline. The square is the only coloured element above
the fold, and it pulses continuously. Below it, at the far left of the viewport, the wordmark set
vertically in the dot matrix face reading bottom to top.

Four numbered movements follow, each opening with a dot matrix marker set as a spaced bracketed
numeral. Movement headings are display serif at the secondary headline size and are pulled up
slightly against their marker, which is what binds the numeral to the heading rather than letting
it float. The first movement carries two paragraphs and a three item list. The second carries two
paragraphs and a figure pair, each figure a large numeral in the display serif over a mono caption.
The third carries three paragraphs and a pull quote, a single line in the mono face in capitals
attributing a press quotation to its publication, with generous space above and below and no
quotation marks beyond the ones in the copy itself. The fourth carries paragraphs and an image.

Editorial images on this route are cards with the card softness carrying a single amber dot at
their top right. That dot is the only use of the amber accent anywhere on the site.

The position readout is a vertical stack of eight small segments at the right edge of the
viewport, in the hairline rule colour, with the segment for the current movement filled in the
brand red. It is a readout and not a control: it does not respond to a click and carries no
pointer cursor. It tracks the movement occupying the majority of the viewport and updates without
running work on every scroll frame.

**Operating system release.** The one dark route. The root carries the dark class, so the ground is
the dark page ground and raised surfaces are the dark raised surface. The dot grid persists
unchanged and, because it is painted in the inverting mode, resolves to light dots on the dark
ground with no second definition. This route is the proof that the grid layer is built correctly:
if a build has hard coded the grid colour, it disappears here.

Type on this route is the one exception to the four family rule: headings stay in the display
serif, body copy is set in the interface sans rather than the display serif, labels and captions
are set in its monospace companion, and section markers are the dot matrix bold. The route
describes a software product whose own interface uses that sans, so the page adopts it to speak in
the product's voice; reproduce it as a route level override, not as a global change.

Structure is a hero, then three movements, then a feature grid. The hero carries the product name
at the extra large heading size, one line of body and a play control labelled in the monospace
companion. Each movement carries a heading, a line of body and two or three feature cards. A
feature card carries a device screenshot on a fine ruled ground, a heading and a paragraph, and is
clipped to the card softness. That ruled ground is the dot grid's sibling at a much smaller pitch,
generated the same way. Movements two and three carry previous and next controls. Section markers
are set as three separate inline elements, the opening bracket, the numeral and the closing
bracket.

Video on this route is the only moving image on the site. It is streamed adaptively rather than
downloaded whole, never plays with sound unasked, carries captions, and can be replaced by the
procedural substitute without changing the surrounding layout.

**Community grant programme.** The one route that abandons the greyscale entirely, and it is here
to prove the theming model: a route can take an arbitrary ground and every global component
continues to work without a variant. The ground is a saturated brand pink, set as a route level
override rather than as a palette role, because it appears here and nowhere else, and body copy on
it is near-black.

On this route the floating pill's fill becomes a lightened tint of the route ground rather than
white; the menu toggle is unchanged and inherits the route text colour; the dot grid is unchanged
and resolves against the pink through the inverting mode; and the footer is unchanged. No
component needs a pink variant, and if a build has hard coded the pill fill to white or the icon
fill to a grey, this route is where it breaks.

The entire route is set in the dot matrix face, including running body copy, which happens nowhere
else. The page title is the programme name at the extra large heading size in the dot matrix bold;
paragraphs are the dot matrix regular at the section marker size with a line height barely above
it, centred, in a single column with a generous gap between paragraphs. This is the one route
where the rule that the dot matrix face is never used for running copy is deliberately broken. It
is a poster, not a page, and the exception is scoped here.

Structure is a title, a manifesto of eight centred paragraphs, a status line, a terms list of
questions and answers, and a three item criteria list. The status line is content rather than a
component: the same string appears twice, once ending the manifesto and once ending the terms.

**Support centre.** A separate shell that shares the brand's type and colour but none of its
layout system. Its header is a full width bar pinned to the top rather than a floating pill; the
wordmark sits at the left of that bar rather than centred in it; navigation is a set of visible
links rather than a drawer; there is no dot grid; and there is a search field, which is a primary
control on the landing route. The landing route carries an angled device image on a pale vertical
gradient ground, a title in the display serif left aligned over the hero, a two line standfirst in
the display serif, and a fully rounded search field with a magnifier mark inset at its left. Below
the hero sits a set of category cards. Article bodies carry ordered steps, inline device imagery
and cross links.

Form fields on the request route are fully rounded for single line inputs, and the message body is
the one place on the site where a multi line field is softened rather than left rectangular.

**Standing pages.** One template: an effective date in the mono face above the title, a title in
the display serif at the panel headline size, a body in the display serif at body size in a single
column held to a narrow maximum measure, and headings at the secondary headline size with a
generous top margin. The measure is the important value: legal copy runs long and it is held to
one narrow column rather than filling the viewport.

**Not found.** The numeral is set in the dot matrix face at display size, centred, and is the
largest appearance of that face anywhere on the site. Below it sits the standard card at the panel
card width with the card softness, carrying a heading in the display serif at the secondary
headline size, a small mark at the card's top right inheriting the text colour, one sentence of
body in the display serif, and a full width action returning to the home route.

### Responsive behaviour

Eleven widths are reacted to and they are not eleven layouts. Most carry type or spacing only, and
three carry structure: the width at which the chrome goes narrow, the width at which the pill and
every anchored card swap widths, and the width at which the constellation collapses. A build may
collapse the type only widths into a fluid scale; it may not collapse those three.

At the pill width the floating pill and every anchored card swap from their wide fixed width to
their narrow one, and their centring offsets swap correspondingly. This is a snap rather than an
interpolation.

Below the constellation width the authored coordinates are ignored and the feature cards render as
a single column in authored order at full measure, with the buy panel moving from anchored to
inline after the central image. This is the single largest layout change on the site: the product
route is the only route whose structure genuinely differs between wide and narrow, and a build
that tries to preserve the scatter on a phone will produce overlapping cards.

Per route: home keeps four full viewport panels and narrows the card; the family listing goes from
as many fixed width columns as fit, to two, to one at the narrow chrome width; the product route
collapses as above; the cart drawer becomes full width; the brand story route hides the position
readout rather than repositioning it, because it is a wide layout affordance with no narrow
equivalent, and takes the full measure; the operating system release route goes from rows of two
or three feature cards to one per row; the community route is already a single centred column and
is unchanged; and the support centre's six links collapse behind a control.

The dot grid cell stays the same at every width. It does not scale, so a narrow screen shows fewer
dots rather than smaller ones, which keeps the dot reading as a physical mark rather than as a
proportion of the screen.

### Accessibility obligations this design creates

Each obligation below exists because of a specific decision above, and a build that treats them
generically will miss them.

Navigation is behind one toggle, so that toggle is the first focusable element on the page and
carries a name. Icons are fields of dots, so every icon carries an accessible name; a field of
circles conveys nothing on its own. The wordmark is the page heading, so the heading order must
still be navigable, which is why the panel eyebrow is a label attached to its headline rather than
a heading of its own. Outbound links are styled identically to internal ones, so the accessible
name of an outbound link states that it opens an external site, and a link that opens a new
context says so before it is activated rather than after; this applies to the drawer rows, the
footer social rows, and above all to the handoff action, which leaves the site in the middle of a
purchase. The dot grid sits over everything, so it is hidden from assistive technology entirely,
receives no pointer events, holds no focusable descendant, and is excluded from the accessibility
tree; it is thousands of elements and would otherwise be thousands of announcements. The label
face runs small, so it must survive a text size increase without clipping.

Several adjacent steps of the greyscale ramp do not meet contrast requirements against each other,
so the pairings are normative. Near-black on the page ground passes. Body copy on the card fill
passes. Reversed text on near-black passes. The ramp midpoint on the page ground is for
placeholder text only and never for body. The disabled text colour on the disabled fill is for
disabled controls only. The brand red must not be used as text on the light ground at body size:
every one of its uses is non textual and must stay that way. The frosted card sits over arbitrary
photographs so its contrast cannot be checked statically, and the build must either constrain the
imagery behind it or apply the flat fallback fill.

When reduced motion is requested the inertial scrolling is disabled entirely and native scrolling
is restored; the continuous pulse stops at full opacity; the marquee and the ticker render static;
and transitions are reduced to no duration rather than removed, so state changes remain instant
rather than absent. The position readout continues to update, because it is information rather
than decoration.

Every field on the account surface and on the support request carries a visible persistent label
rather than a placeholder acting as one. Errors are associated with their field, announced, and
stated in words rather than by a border colour alone.

### Copy

**Voice.** Four rules. Headlines are sentences rather than slogans: they begin with a verb or a
noun phrase and they finish. Body copy carries one fact and then says what that fact does for the
reader, and where it compares, the comparison is footnoted with an asterisk. Labels are upper case
and terse: anything set in the dot matrix face is two or three words and takes no punctuation. The
brand refers to itself in the third person everywhere and says "we" only on the brand story route.

**The bracket convention.** Product names and section numerals are set with literal spaces inside
their brackets, as in `phone ( 5a )` and `headphone ( 2 )`, and a bare bracketed numeral for a
section marker. The spaces are characters in the string, not letter spacing applied over it, and
they are what makes the dot matrix face read as a readout. Product names are lower case; section
numerals stand alone.

**Button labels**, the complete set, upper case, dot matrix face: `DISCOVER` on the home panels
leading to a product route; `LEARN MORE` on the home panel leading to the operating system release
route; `CONTINUE SHOPPING` on the empty cart; `BACK TO HOME` on the not found surface;
`SHOP ON Bazaario` on the handoff buy route; `ADD TO CART` on the direct buy route; `NOTIFY ME` on
the unavailable buy route; and `PLAY` on the film tile and the video control. The handoff label
names the retailer inside the button, which is the honest treatment: the label tells a person they
are about to leave.

**Product route copy.** The three feature rows on the flagship phone read `UP TO 70X ULTRA ZOOM`,
`3 CAMERA SYSTEM` and `HalcyonOS WITH Companion`. The rear notification light is named `Pulse`
and the capture and recall surface inside the assistant family is named `Memory Notebook`; both
appear as constellation card kickers on the flagship phone and nowhere else. Its constellation captions read
`Built different`, `Photography`, `Take better photos`, `Specs`, `It is clear` and
`Advanced 3 camera system`. Kickers read `FILM` on a film tile, `HARDWARE` on a hardware tile and
`TECHNICAL` on a specification tile. Audio products carry a shorter set, one selector and three
rows reading `UP TO 80 HOURS OF PLAYBACK`, `SOUND BY Vox` and
`REAL-TIME ADAPTIVE NOISE CANCELLING`.

**Support centre copy.** The title is `Support Centre` and the standfirst reads
`Learn about your Halcyon products, find answers, work through problems and ask for help.` The
search placeholder is `Search`. The feedback question is `Was this page helpful?` and its two
controls read `Yes` and `No`.

**Account copy.** The heading is `Sign in`. The fields are labelled `Email address` and
`Password`. The forgotten link reads `Forgot your password?` and the submit reads `Sign in`. The
consent line reads `By signing in, you agree to our Privacy Policy and User Agreement.` The create
control reads `Create an account`. The failure wording is `Incorrect email or password` in all
three cases, and a completed reset reads `Password successfully changed.`

### Zero asset substitution

This build ships no binary. Every asset class is replaced by a recipe.

**Product photography**, the largest class and the one the design depends on most. Every panel
image and every variant image is a device rendered in clear space with a soft reflection. Compose
the device from rounded rectangles, in a canvas or as layered boxes: a body whose corner softness
is about a tenth of its width, a raised camera plate as a smaller rounded rectangle, two or three
circles for lenses, and a rectangle for a side control. Fill the body with a vertical gradient
between two steps of the greyscale ramp, choosing the pair by colourway so a pale colourway runs
between the page ground and the card fill and a dark colourway runs between the near-black and the
heading step. Add a single specular highlight as a narrow, low opacity white shape running down
one edge, slightly off vertical. Add the reflection by drawing the same shape flipped vertically
beneath the original at low opacity, masked by a gradient fading to nothing over its own height.
Seed the composition from the variant identifier, so the same variant always produces the same
image. This is a placeholder that occupies the right space with the right weight and the right
palette; it is explicitly not a photorealistic device.

**Lifestyle photography**, the full bleed images on the product route and the editorial cards.
Replace with a seeded field: two or three radial gradients at seeded positions in colours drawn
from the greyscale ramp with at most one drawn from an accent; a grain overlay; and four
directional fades applied at the edges so the card and the chrome stay readable over it.

**The fine ruled ground** behind the operating system route's feature cards is the dot grid's
sibling at a much smaller pitch, generated the same way: a repeating linear gradient in each axis
at the hairline rule colour, at low opacity, clipped to the card softness.

**Video.** Replace with a canvas loop driving the same hero entrance over a seeded gradient field,
at the same length as the duration shown on the film tile. The play control, the duration readout
and the caption track remain, with the captions authored as text. The substitute occupies the
identical box so the responsive behaviour is unaffected.

**Fonts.** The one class not replaced procedurally. Name an open family for each of the four roles
and give each a fallback stack: a transitional serif with a tall x height for the display role, a
face whose letterforms are built from discrete dots for the label role, any monospace for the mono
role, and a variable grotesque with a monospace companion for the interface role. Because the icon
generator already draws arbitrary dot figures from centre lists, the wordmark and the section
numerals may be rendered as generated marks rather than as text, which removes the hardest font
dependency in the design.

**Grain.** A tiling noise texture over the lifestyle substitutes: an inline turbulence filter at a
fine base frequency with several octaves, desaturated, at low opacity, on a tile large enough that
it does not read as a pattern.

## Constraints

Single tenant: one brand owns every product, and there is no seller account, no second vendor and
no listing submitted from outside the business. No auction and no bidding. No customer review
surface and no media upload by a visitor. No live chat. No subscription plan and no loyalty points
ledger. No payment step, no card handling and no order fulfilment: the cart hands over to a
separate origin and this app learns the outcome only from the checkout webhook. No order history
surface, because the identity this app holds is used only to reconcile a cart and to authorise a
registration. Trade in and repair record an intent and return a reference; they do not price a
device, schedule a visit or move a unit. No forum and no careers surface: both are outbound links.
No native application. No third party analytics, consent management or tag stack, and no
conversion reporting of any kind. No external network call at run time. No binary asset: no
photograph, no video file and no font file ships with this build. The catalogue holds at most a
few hundred products and a few thousand variants, and every listing, facet and sort must stay
responsive at that size.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
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
| `GET /api/health` | none | readiness |
| `POST /api/auth/signup` | `email`, `password` | the created account and a token |
| `POST /api/auth/login` | `email`, `password` | the account and a bearer token under the key `access_token` |
| `POST /api/auth/logout` | none | acknowledgement |
| `GET /api/auth/me` | none | the signed in account |
| `GET /api/families` | none | a top-level array of families in catalogue order |
| `GET /api/collections/{family}` | `colourway`, `capacity`, `sort` | a top-level array of variant cards |
| `GET /api/products/{product}` | none | the product, its axes and its constellation |
| `GET /api/products/{product}/variants` | none | a top-level array of that product's variants |
| `GET /api/variants/{variant_id}` | none | one variant with `buy_route`, media, availability, price |
| `GET /api/cart` | none | the cart, its lines, its totals and its checkout address |
| `POST /api/cart/lines` | `variant_id`, `quantity` | the updated cart |
| `DELETE /api/cart/lines/{line_id}` | none | the updated cart |
| `POST /api/outbound-clicks` | `variant_id`, `destination` | acknowledgement |
| `POST /api/intents` | `kind`, `email`, `variant_id` or `product_slug`, `payload` | the intent and its reference |
| `GET /api/registrations` | none | a top-level array of the signed in account's registrations |
| `POST /api/registrations` | `serial` | the created registration |
| `GET /api/support-requests` | none | a top-level array of the signed in account's requests |
| `POST /api/support-requests` | `registration_id`, `category`, `body`, `idempotency_key`, optional `attachment_key` | the request and its `reference` |
| `POST /api/articles/{article}/vote` | `helpful` | the stored vote |
| `POST /api/webhooks/checkout` | the checkout outcome, signed | acknowledgement |

Field names are exact. A successful login answers with the bearer token under the key
`access_token`, and the client sends it as a bearer credential on every authenticated call. A list
endpoint returns a top-level JSON array. Bearer auth is required on everything except login,
signup, health and the webhook receiver, which authenticates by signature rather than by a
visitor's token. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never as a server error and never as a
silent success.

### No mocks

`postgres` and `mailpit` are the fact. An in-memory list of registrations, a JSON file of support
requests, a `sent` flag the app sets on itself, a log line standing in for a message, a stubbed
SMTP client that returns success without connecting, or a hardcoded acknowledgement the app
returns to itself, are each a contract violation however good the interface looks. The
registration and the request must exist as real rows in `postgres` and survive a restart, and the
acknowledgement must exist as a real message delivered over SMTP to that owner's own address. The
named provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can walk a family, filter it by colourway and capacity, open a device, choose a
colourway and a capacity that resolve to exactly one variant, and follow the buy route that
variant carries: into the cart for one sold direct, out to the named retailer by a real link for
one handed off, and into a notify intent for one that is unavailable. A combination nobody makes
is offered and cannot be chosen. A signed in owner registers a device by its serial number and
files a support request against it, receives a reference and exactly one acknowledgement at their
own address, and gets the same reference back with no second message if the form is sent again. A
serial belonging to somebody else cannot be registered, and a request cannot be opened against
anybody else's registration.
