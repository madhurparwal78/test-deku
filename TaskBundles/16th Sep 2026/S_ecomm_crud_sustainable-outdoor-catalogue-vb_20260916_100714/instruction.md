# Verdea Sustainable Outdoor Catalogue

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, filter the catalogue down to
the Golf signage, configure the `Tee Sign Heritage` in a size, a structure, a colour, a display and
a laminate colour, save it to a wishlist beside a second product, send that wishlist as a quotation
request, and read back a short quotable reference, without hitting an error page. The hard part is
that the request is a commercial record: every line must be stored exactly as the visitor
configured it, with the names the visitor saw, whatever happens to the catalogue afterwards, a
double click must never become two enquiries, and the saved list must only disappear once the
confirmation is really on screen. The quotation must exist as a real row in the `postgres`
database, and its confirmation must arrive as a real message in the `mailpit` inbox; a success
screen the app shows itself does not count.

## Overview

Verdea is the website of a Portuguese manufacturer, established in 2007, that makes signage,
benches, bins, bollards, bicycle parking, viewing platforms, boardwalks, picnic furniture and golf
course equipment from steel, high-pressure laminate and recycled plastic, and sells them to
municipalities, park and trail operators, golf clubs, landscape architects and contractors across
Europe. Portugal is home, Spain is the second operating market with its own establishment, and France is a target market. The site has two halves. The half a visitor sees is a slow, image-led catalogue and
editorial site in four languages (Portuguese, English, Spanish and French): five collections
(Urban, Nature, Repolymer, Golf, Details), a journal of case studies, an about story and a
sustainability story. The half a visitor does not see is the intake machinery that turns interest
into an enquiry a salesperson can act on: a contact form, a configured product wishlist submitted
as a quotation request, a gated technical-document library, a double opt-in newsletter, and a small
back office where two staff roles work what arrives.

The person the product exists for is the specifier: a landscape architect, a municipal buyer, a
park or trail manager, a golf superintendent or a contractor's buyer. They work to a budget somebody
else set, are comparing three suppliers (of whom Verdea is one), assemble a list rather than buy one thing, want a dimensioned
drawing before a price, and are going to send that list to a person and talk, not check out. Every
product decision below follows from that. Others come too: a sustainability officer
wants material provenance and end-of-life, not a slogan; a golf superintendent wants a collection
that is theirs; a journalist wants the case studies; a candidate wants the open positions.

What it deliberately is not. It is not a shop: there is no price on any page, no cart, no checkout,
no payment and no order, and so no billing, proration or dunning. Visitors never create an account, never sign in and never reset a
password; the wishlist lives in the visitor's own browser. There is no content editing interface,
no drafts, no previews, no approval chain and no tenants. There is no chat widget, no social embed,
no review widget, no analytics tracker and no third-party script in the page. Nobody applies for a
job on this site.

The genuinely hard part is the quotation: a wishlist entry is a configuration, not a product, and
the submitted request must carry every configured line faithfully, reconcile each against the
catalogue without ever rejecting the whole request, and be written once and only once however
often the visitor presses send.

## User roles

Visitors are anonymous and need no account for anything public: browsing, filtering, configuring,
saving to the wishlist, requesting a quotation, requesting technical documents, subscribing,
reading the journal. Two staff roles sign in to the back office. Signup does not exist anywhere:
staff accounts are seeded, and there is no way to create an account from inside the product.

| Role | Can do | Cannot do |
|---|---|---|
| visitor (no account) | every public action listed above | **cannot reach any back-office screen or `/api/office` endpoint** |
| `commercial` | read the enquiry list and any enquiry in full with its quotation lines; release a quarantined enquiry; read the subscriber list; read enquiry and subscriber counts; read the product list with its publish state | **cannot publish or unpublish a product** |
| `editor` | read enquiry and subscriber counts only (the role matrix gives it counts, never rows); read the product list; publish and unpublish a product in a locale | **cannot read any enquiry's contents, cannot open an enquiry, cannot release a quarantined enquiry, cannot read the subscriber list** |

The two roles are deliberately disjoint apart from the shared counts and the product list, so a
stolen session of one reaches nothing of the other's.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an `editor` session to any `commercial`-only endpoint must
be rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged. The same holds in the other direction for the editor's publish endpoints, and for
every read endpoint that exposes enquiry contents or subscriber addresses: authorization is deny by
default, a route with no explicit rule is refused, and every back-office request with no valid
token is denied.

Seeded accounts, all using the password `deku-demo-pw-2026`:

- `commercial@example.com`, role `commercial`, display name Carla Mendes
- `editor@example.com`, role `editor`, display name Rui Tavares
- `former@example.com`, role `commercial`, display name Nuno Pires, status `suspended` (a former
  employee whose account can no longer sign in)

## Core features

### Staff sign-in

1. `POST /api/auth/login` takes `email` and `password` and returns `access_token`, `role`,
   `issued_at` and `expires_at`, where `expires_at` is exactly seven days after `issued_at`. The token is sent as `Authorization: Bearer <token>` on every `/api/office` call.
2. A wrong password and an unknown address are denied with the same body and in comparable time,
   and neither returns a token.
3. A token lives at most seven days from sign-in and is never extended; `POST /api/auth/logout`
   revokes it at once, and a revoked or malformed token is denied.
4. Passwords are stored hashed. There is no signup, no password reset and no invitation route.
5. Account lifecycle: a staff account with no sign-in for ninety days is suspended and its tokens
   are revoked, a suspended account is denied at sign-in exactly like a wrong password, and only a re-seed or an operator reactivates it, so the ex-employee problem (a
   forgotten account of someone who left) cannot linger. A back-office page opened without a valid session goes to `/office/login` and, after signing
   in, returns to the page that was asked for, provided that path is local (it begins with a single
   slash and is not protocol-relative); any other return path is ignored.

### Localisation: four locales and their addresses

6. The locales are `pt` (the default and the fallback for everything), `en`, `es` and `fr`, and
   the locale is always the first path segment. There is no unprefixed page other than the root.
7. Path segments are localised: products `produtos` / `products` / `productos` / `produits`; about
   `sobre` / `about` / `nosotros` / `apropos`; sustainability `sustentabilidade` / `sustainability`
   / `sostenibilidad` / `durabilite`; journal `jornal` / `journal` / `periodico` / `journal`;
   wishlist `lista` / `wishlist` / `mi-lista` / `ma-liste`. The segments `careers`, `legal` and
   `newsletter` are the same in all four. Segments are configured per locale, and two routes
   colliding on one segment inside a locale stops the app at start-up rather than being suffixed.
8. Document slugs are localised independently: a product's Spanish slug is a Spanish phrase. Each
   product, collection, category and article carries a stable identifier shared by all its locale
   versions, and everything that resolves a document across locales resolves by that identifier,
   never by slug.
9. On first arrival, a request to `/` answers `302` (never `301`) with a `Location` of a locale home, chosen in this
   order: the `verdea_locale` cookie, only when the `verdea_consent` cookie lists `preferences`; else
   the best match of `Accept-Language` among the four; else `pt`. With preferences refused, the
   language cookie is neither written nor read.
10. Language headers never redirect anything but the root. A deep link such as `/en/products`
    answers in English whatever the browser prefers, and a language the visitor chose explicitly is
    never overridden later.
11. Every document has exactly one canonical address: lower case, no trailing slash, locale prefix.
    A path with upper case or a trailing slash answers `301` to the canonical form; a query string
    other than a recognised facet parameter never causes a redirect and is left out of the page's
    canonical link.
12. A product requested under the wrong collection segment with a valid slug answers `301` to its
    canonical path, for example `/en/products/nature/tee-sign-heritage` to
    `/en/products/golf/tee-sign-heritage`. A category segment from another locale redirects to the
    canonical segment in the same way, and so does a product slug from another locale when the product
    exists in the requested locale: `/es/productos/golf/tee-sign-heritage` answers `301` to
    `/es/productos/golf/senal-de-salida-heritage`.
13. A document that does not exist in the requested locale but exists in `pt` answers `302` to the
    Portuguese version, which shows a dismissible line saying the page is not available in the
    chosen language. The document is found by its slug in any locale: `/fr/produits/details/slim-room-sign`
    carries the English slug of a product with no French version, so it answers `302` to
    `/pt/produtos/detalhes/placa-de-sala-slim`. When no version exists anywhere, the requested
    locale's not-found page answers. A fallback document is never served under another locale's
    address.
14. The language switcher lists the four locales and, for each, links to the same document in that
    locale through its stable identifier and that locale's segment and slug. Where no equivalent
    exists, the item points at that locale's home and is marked as such before it is chosen. Chrome
    is never mixed: a French page carries no English label, and a missing label falls back to the
    component's own default text rather than to another locale's string.
15. Every public page declares `hreflang` alternate links for each locale in which the document
    exists, plus `x-default` pointing at the `pt` version, and the links are reciprocal.
16. Formatting follows the locale: numbers use the locale's grouping, and dates render per locale
    from a date, never from an instant, with the full month name (English reads `May 12, 2026`).
    Addresses and telephone numbers are content and are never reformatted. What is not translated is
    a content decision: collection, sub-collection and option names are authored per locale and may
    stay identical, and colour names often stay in one language because they are the manufacturer's
    own vocabulary on its drawings.

### The catalogue

17. `/en/products` lists every published product of the locale as cards. The seeded English
    catalogue holds 20 products: 6 Urban, 4 Nature, 3 Repolymer, 4 Golf and 3 Details. Portuguese
    also holds 20, Spanish 19 (it lacks `Slim Room Sign`) and French 18 (it lacks `Slim Room Sign`
    and `Golf Bag Stand`). Each locale's catalogue is its own set, and its total is honest.
18. Three facet groups exist: collection (`by Collections`: Urban, Golf, Details, Repolymer,
    Nature), product type (`by Products`: Signage, Construction, Furniture, Equipment) and
    sub-collection, which appears only when exactly one collection is active (Urban has `Frame`,
    `Plaza`, `Reuse`).
19. Groups combine as a conjunction and values within a group as a disjunction. In English, Urban
    plus Signage leaves 2 products, Golf plus Signage leaves 2, Urban or Golf leaves 10, Urban with
    the Plaza sub-collection leaves 2, Urban with Frame leaves 3, and Details plus Construction
    leaves 0.
20. Facet state lives in the address under the parameters `collection`, `productType` and
    `subCollection`, with a repeated parameter for each extra value, and the address round-trips
    exactly, never lossy: `/en/products?collection=urban&collection=golf` reproduces both selections when opened
    in a new window. An unknown value is ignored and removed from the address, never producing an
    empty grid.
21. The counter reads `Showing <n> of <total> Results` followed by a downward arrow mark, where the
    total is the locale's published product count and n is the number the facets leave. The
    catalogue card for a collection document never counts. The server-rendered page carries the
    counter already computed for the facets in the address, so `/en/products` arrives reading
    `Showing 20 of 20 Results` and `/en/products?collection=urban&productType=signage` arrives
    reading `Showing 2 of 20 Results`, while `/en/products?collection=urban&collection=golf` arrives reading `Showing 10 of 20 Results`.
22. A facet change filters the products already delivered with the page. It makes no request,
    shows no loading state, keeps each surviving card mounted with its decoded image, and updates
    the counter, which is announced politely to assistive technology.
23. A facet value with no products under the other active facets stays visible and unavailable,
    with its count. A combination that matches nothing shows the counter at zero, the active facets
    as removable chips, a control clearing them all, and three suggested products from the locale;
    the grid is never simply blank.
24. On wide screens the facet groups sit inline above the grid. On narrow screens, and on wide
    screens once the inline groups have scrolled away, a floating `FILTER` control pinned to the
    lower centre opens the facet panel and shows how many facets are active whenever any are.
25. Each card carries the product title (at most two lines, then truncated), the collection pill
    with its mark, the render on its ground shadow, a `Colors` strip and a `Sizes` strip, and the
    bookmark control. Each strip shows two items and then `+N`, where N is the number not shown:
    `Tee Sign Heritage` reads two swatches then `+6`.
26. Size chips render exactly as authored: not sorted, not parsed, not normalised. `Frame Bollard`
    reads `s` and `m`, `Reuse Litter Bin Duo` reads `All`, `Bottle` and `Pet`, and `Classic Ball Washer` reads `R900` and `Q600`.
27. A product with no colour renders no colour strip, and one with no size renders no size strip,
    rather than an empty one. `Line Door Plate` has neither.
28. The render's framing depends on its shape: wider than tall, taller than wide, or roughly
    square, each with its own arrangement inside the tile, so a bollard and a picnic table are not
    framed alike.
29. `GET /api/products?locale=en` returns the locale's published products as a top-level array of
    projections and accepts the same facet parameters, combined by the same rules.
30. The first two rows of cards load their images at once; every other card reserves its space and
    loads its image as it approaches the view, and the grid stays smooth when it is long.

### Collections

31. `/en/products/urban` is the catalogue with the collection fixed by the path. Its counter shows
    the collection's share of the whole locale (`Showing 6 of 20 Results`), and the other collection
    chips stay live.
32. Choosing a different collection on a collection route navigates to that collection's route;
    clearing the collection navigates to `/en/products` carrying the other facets. The sub-collection
    group is replaced on every such change.
33. A collection route carries its own document title, heading identity and social metadata naming
    the collection, while the visible heading is shared with the index.
34. Urban, Nature, Repolymer and Golf each have a catalogue document named `Urban Catalogue`,
    `Nature Catalogue`, `Repolymer Catalogue` and `Golf Catalogue`, shown as a catalogue card placed
    in the grid after a whole row. Details has no catalogue, so its route has no catalogue card.
    The catalogue card opens the file request in its collection-catalogue scope; it is never a
    direct link to the document.
35. An unknown collection segment answers the not-found page offering the five collections by name.
    A collection with no published products in the locale shows its header, its catalogue card and a
    line offering the Portuguese version, never a not-found page.

### The product route

36. `/en/products/golf/tee-sign-heritage` shows the product in a split: the object on one side and
    its specification on the other.
37. The object side shows a still render first, from the server-rendered document, at the exact
    size and place the live object will take. After first paint, a live object the visitor can turn
    replaces it with a cross-fade; when the live object is refused or fails, the still images stay and
    nothing is announced.
38. The specification side carries, in order: a `PRODUCTS` back control returning to the
    collection, the collection pill, the title, a `What is it` label beside the description, the
    compound primary control, a row of technical drawings, and a `Specs` cue leading down to the
    specification block.
39. The compound control is two controls in one shape with a visible division: a bookmark button
    that saves to the wishlist, and `REQUEST INFORMATION`, which opens the file request for this
    product. Each is separately focusable and separately named.
40. The specification block is a list of labelled rows, each label with one or more values, in
    this order where present: `Dimensions`, `Structure Options`, `Structure Colors`, `Display Options`, `HPL+ Colors`, `Materials`, `Specifications`, `Advantages`, `References`. A product
    shows only the rows it has.
41. `Tee Sign Heritage` carries: `Dimensions` `190 x 100 x 1700 mm`; `Structure Options`
    `Metallised and painted steel` and `Galvanised steel`; `Structure Colors` `Pure white RAL9010`,
    `Anthracite grey RAL7016`, `Umbra grey RAL7022`, `Signal yellow RAL1003`, `Salmon pink RAL3022`,
    `Pastel blue RAL5024`, `Pastel green RAL6019` and `Personalised`; `Display Options` `HPL +` and
    `HPL Print`; `HPL+ Colors` `Sienna brown`, `Mid beige`, `Spring green`, `Turf green`, `Dark green`, `Dark brown`, `Dark blue` and `Black`; `Materials` `Reinforced, brown recycled plastic; HPL+ or HPL Print.`; `Advantages` `No maintenance required; Easy component replacement; Customizable; High resistance to shock, weather, and vandalism.`; `References` `HPL+ - GTEETTM010` and `HPL Print - GTEETTM011`. Its description reads: Where tradition meets function,
    this sign presents the key details players need to plan each shot. Its classic presence
    reinforces the course's heritage while enriching the tee experience.
42. A colour value renders as one string including its standard colour reference (`Anthracite grey RAL7016`), never split and never hidden behind a swatch; a value with no colour, such as
    `Personalised`, renders as text without a swatch.
43. Every reference code (`GTEETTM010`, `UBSCFE0000881`) is its own marked element with a copy
    control. Copying gives feedback that is visible and announced, and reverts after a short
    interval.
44. `Plaza Bench Long` carries sizes `1400`, `1900` and `2000` (the `2000` size measures `2000 x 554 x 465 mm`), structures `Galvanised steel` and `Metallised and painted steel`, colours `Anthracite grey RAL7016`, `Umbra grey RAL7022`, `Pure white RAL9010` and `Personalised`, no display and no
    laminate options, and the reference `Plaza Bench Long - UBSCFE0000881`.
45. A control for something the product does not have is absent, never disabled: `Slim Room Sign`
    has no technical documents, so it has no `REQUEST INFORMATION` control; a product with no
    reference codes has no references control; the related strip is absent when the collection has
    no other product in the locale.
46. `In the same Collection` shows up to six other published products of the same collection and
    locale, excluding the current one, in a stable order that does not reshuffle between visits.
47. Where a product appears in case studies, a strip of those articles follows; `Boardwalk Module`
    and `Viewpoint Platform Deck` both list `Ridge Viewpoint Boardwalk`. Where a product has
    installation photographs, a full-width band of them is the only photography on the route.
48. `GET /api/products/tee-sign-heritage?locale=en` returns the product in full: identity, title,
    description, collection, types, sub-collection, every option axis with its values, the
    specification rows, the reference codes, whether documents exist, the slug of every locale
    version under `alternates`, and the related products. The product page also carries a structured
    breadcrumb (`BreadcrumbList` metadata) derived from its path, although the visible breadcrumb is
    only the back control.

### The options modal

49. Pressing the bookmark on a product that has any option axis opens the options modal, headed
    `Personalise your product`, over the current page without changing the address. A product with
    no option axis, such as `Line Door Plate`, is added directly and the modal never opens.
50. The modal offers five independent axes in this order: size (chips), structure (named swatches),
    colour (round swatches with names), display (named chips) and laminate colour (round swatches
    with names). No axis constrains another.
51. An axis with no values is absent. An axis with exactly one value is shown already selected and
    is not interactive: `Reuse Litter Bin Duo` shows the single colour `Anthracite grey RAL7016`
    that way.
52. Choosing a size swaps the technical drawing beside the size axis for that size's own drawing,
    with a cross-fade, inside a reserved box so the modal never resizes.
53. A swatch shows its option's colour or, for a textured finish, its texture clipped to the
    circle, with the full name beside it as text. The chosen value is marked by a tick and a change
    of shape as well as colour.
54. Every axis is optional. Adding with nothing chosen is valid and means the product with its
    specification still to be agreed. The primary control is reachable with one key press as the
    modal opens, adds the configuration and closes the modal, returning focus to the control that
    opened it; its label says what it does and still reads as adding when the product is already
    saved in another configuration. Escape and the back gesture close without adding.
55. The references mode opens the same modal headed `References` with the product's rich text, in
    which every `REF-` token followed by upper-case letters and digits is shown as a reference-code
    element with its copy control. Tokens are found in the parsed rich text, never by assembling
    markup from a string.
56. A configuration cannot be linked to: the modal never writes the choice into the address. The
    wishlist and the quotation carry the configuration instead.

### The wishlist

57. The wishlist lives in the visitor's own browser, under one stored list, read once at start-up
    and written on every change. There is no server copy and no account. A stored value that cannot
    be read is treated as empty and overwritten on the next change; an entry missing a required
    field is dropped and the rest load; when browser storage is unavailable the list works in memory
    for the session without announcing anything.
58. An entry is a configuration, not a product: it holds a generated entry identifier, the
    product's stable identifier, the title and slug as displayed, the collection name, and the chosen
    `size`, `structure`, `color`, `display` and `hplColor` names (each absent when not chosen). The
    same product saved twice in two colours is two entries and two rows. Entry identifiers come from
    a strong random source, with a fallback composed of the product identifier, the time and a
    random suffix where that source is unavailable.
59. The card bookmark is product-scoped: empty when the product is not saved, filled when it is,
    and filled with a count when it is saved more than once. Pressing a filled bookmark removes one
    entry for that product. The control is a toggle that reports its pressed state, and its
    accessible name states the product, the action and the count.
60. Adding shows a confirmation with the product name, a control opening the wishlist, an undo
    control and a bar that drains across its lifetime. It dismisses itself, can be dismissed, is
    announced politely and never takes focus. Undo removes exactly the entry just added, by its
    entry identifier, never the first entry for that product.
61. The header shows a wishlist count beside the wishlist control, updated on every change and when
    another tab changes the list, and shows nothing at zero.
62. An empty wishlist shows the label `Your wishlist`, the heading `No picks yet? Explore, select, and help make the world greener.`, a `Start adding` control leading to the catalogue, and three
    decorative placeholder cards reading `Your next product` that assistive technology does not
    read. There is no quotation control on an empty wishlist.
63. A populated wishlist shows the count, a line inviting a quotation, a `Request a quotation`
    control, a secondary clear control that names the count and asks for confirmation before
    clearing, and one row per entry with the render, title, collection, the chosen option names as a
    labelled list, a remove control, and a link to the product. An axis the visitor did not choose is
    absent from the row, and the row offers to open the options modal to choose it there.
64. Rows resolve by product identifier in the current locale at render time. A product that exists
    only in another locale renders from the stored names, marked as not available in this language,
    linking to the locale where it exists. A product that no longer exists renders from the stored
    names, marked as no longer in the catalogue, without a link, and is still submitted.
65. The list survives a reload and a locale change. It is not rewritten on a locale change.
66. The list holds at most fifty entries: a fifty-first add is refused with a visible message naming
    the count, and an add that the browser's storage quota refuses is refused the same way. Adding
    and removing keep working with the network off.

### The quotation request

67. `Request a quotation` opens the contact modal in its quotation mode, headed by the three tabs
    `Contact`, `Wishlist` and `Files`, with the wishlist shown inline above the fields. The fields are
    `First Name`, `Last Name`, `Email`, `Role`, `Industry`, `Country`, `City`, an optional `NIF`
    (fiscal number), the checkbox `Some products have BIM/3D files available, are you interested?`,
    and the privacy consent.
68. `POST /api/lead/quotation` writes, in one step, one `lead` with kind `quotation`, one
    `quotation` and one `quotation_item` per entry, and answers `202` with the `reference`. Either
    all of it is written or none of it is.
69. The reference is `VQ-` followed by six characters drawn from `23456789ABCDEFGHJKMNPQRSTUVWXYZ`,
    so it never contains a character confusable when read aloud, for example `VQ-7K4M9P`. It is
    unique, not sequential and not the record's key, and it is shown on the confirmation and in the
    confirmation email.
70. The request carries entries as structured data: `entryId`, `productId`, `slug` and `options`
    with `size`, `structure`, `color`, `display` and `hplColor`. A title or collection sent by the
    client is an unknown property and the whole request is refused as invalid; the server resolves
    those itself.
71. For each entry, in order, the server stores a line with `position` counting from 1: when the
    product exists in the submitted locale, its current title, slug and collection name; when it
    exists only in the default locale `pt`, the Portuguese title, slug and collection name with
    `resolved_from_locale` set to `pt`; when it does not exist at all, the submitted slug as both
    title and slug, `No longer in the catalogue` as the collection name, and `unresolved` set to
    true. One unresolved line never refuses the request.
72. Option names are stored exactly as sent in `option_size`, `option_structure`, `option_color`,
    `option_display` and `option_hpl_color`, and are never checked against the current options; a
    name that was not chosen is stored empty. A line saved as `Tee Sign Heritage`, size `M`,
    structure `Galvanised steel`, colour `Anthracite grey RAL7016`, display `HPL +` and laminate
    `Dark green` reads back exactly so, and keeps reading so after the product or its options change.
73. The server renders the flat payload from the stored lines and keeps it as `payload_rendered`:
    one numbered block per line, blocks separated by a blank line, a first line of the title and the
    slug in brackets, then `Collection:`, `Structure:`, `Color:`, `Display:`, `HPL Color:` and, last,
    `Size:`, each indented, with `(not chosen)` for any option that was not chosen:

    ```
    1. Tee Sign Heritage (tee-sign-heritage)
       Collection: Golf
       Structure: Galvanised steel
       Color: Anthracite grey RAL7016
       Display: HPL +
       HPL Color: Dark green
       Size: M

    2. Plaza Bench Long (plaza-bench-long)
       Collection: Urban
       Structure: (not chosen)
       Color: (not chosen)
       Display: (not chosen)
       HPL Color: (not chosen)
       Size: 2000
    ```

74. `item_count` always equals the number of stored lines, and the payload always includes the size.
75. A request with no entries, or with more than fifty, is refused and nothing is written; an entry
    carrying an option key outside the five is refused as invalid.
76. Contact fields are validated on the server: `firstName` and `lastName` 1 to 80 characters after
    trimming with at least one non-space; `email` per rule 106; `country` free text of 2 to 60
    characters, never a picker; `city` 1 to 80 characters; `role` and `industry` each one value of a
    closed list, whose labels are translated per locale while the submitted value is always the
    English value below; `taxId` optional, 1 to 20 characters of digits and spaces only. The English
    role list is `Landscape architect`, `Municipal buyer`, `Park or trail operator`, `Golf course superintendent`, `Contractor` and `Other`; the English industry list is `Public administration`,
    `Landscape architecture`, `Construction`, `Golf and leisure`, `Hospitality` and `Other`.
77. The fiscal number field opens a numeric keypad on touch devices but is a text field, so leading
    zeros survive and nothing increments it.
78. `wantsTechnicalFiles` records the checkbox on the lead and never triggers a download.
79. Pressing send twice, or losing the connection after the request left, never makes two
    enquiries: the modal generates one idempotency key per form instance, and a repeat with the same
    key returns the first answer (rule 110).
80. The wishlist is cleared only after the confirmation has rendered, and only for a successful
    submission. It is never cleared while sending, and never when the request fails; a failed
    request leaves the form with every value in place.
81. When the last entry is removed while the quotation modal is open, the modal closes with a
    message and focus returns to the control that opened it. When a submission succeeds in another
    tab, this tab's list clears and an open modal closes with a message naming the reference. After a successful submission, in this tab or
    another, the wishlist route shows the empty state with a line naming the reference that was sent.
82. The confirmation replaces the form, receives focus, is announced, and shows the reference
    together with a line saying a copy of the full request is on its way by email.

### Gated file requests

83. The gate is offered in three places: `REQUEST INFORMATION` on a product, and the catalogue card or
    the chapter download control of a collection. Each opens the contact modal in its file mode, asking for `First Name`, `Last Name`, `Email`
    and the privacy consent. No account, no password, no confirmation step before the download.
84. `POST /api/lead/file-request` writes one `lead` with kind `file_request` and one `file_request`,
    and answers `202` with `documentName`, `downloadUrl` and `expiresAt`. The document is either a
    product's technical files (`Tee Sign Heritage technical files`) or a collection catalogue (`Urban Catalogue`). A request for a document that does not exist, such as technical files for `Slim Room Sign` or a catalogue for Details, is refused as not found and writes nothing.
85. The grant is an opaque token of at least 128 bits of randomness, bound to exactly one document,
    valid for seven days and for at most five redemptions.
86. `GET /api/files/<token>` answers `302` to a short-lived signed location on the app's own origin,
    valid for five minutes, which serves the document as a PDF with a readable file name,
    `tee-sign-heritage-technical-files-en.pdf` or `urban-catalogue-en.pdf`. Each call counts as one
    redemption.
87. A token that is unknown, expired or already redeemed five times answers `404`, never `403`, with
    nothing distinguishing the three. A signed location that does not verify or has expired also
    answers `404`.
88. The endpoint resolves the document from the token alone. It never accepts a document
    identifier, an asset key or a path as a parameter, and any such parameter is ignored.
89. The confirmation names the document, offers a download control, and says the same link has been
    emailed. When the download fails, the confirmation stays and the control retries.
90. Within one browser session, a document the visitor has already been granted skips the form and
    downloads directly; this never applies to a document not already granted.
91. The gate is not a paywall: the document is not personalised per requester, the grant is not tied
    to a network address, a repeat request from the same address simply issues a fresh grant, and
    nothing tries to stop the document being passed on.
92. Documents are generated by the app from its own content: a cover with the collection or product
    name, then one page per product with its render, its specification block and its reference codes.

### The newsletter

93. The newsletter form is one email field, a submit control and the sentence `By submitting your email you agree to our Privacy Policy.`; nothing else is collected. It appears in the footer of
    every route, on the journal index, and on the sustainability and about routes.
94. `POST /api/subscriber` answers `202` with `{"status": "check_inbox"}` in every accepted case, and
    the confirmation line tells the visitor to check their inbox and confirm; it never says they are
    subscribed.
95. A new address creates a `subscriber` in `pending` with a single-use confirm token valid for
    fourteen days, and sends exactly one confirmation message.
96. A repeat sign-up for an address already `pending` creates no second row and sends no second
    message within twenty-four hours of the first. A repeat sign-up for a `confirmed` address sends
    nothing and answers exactly as a new sign-up, so the list is never disclosed. A sign-up for an
    `unsubscribed` address returns it to `pending` and sends a confirmation; it is never silently
    reactivated.
97. The confirmation link `/api/subscriber/confirm?token=<token>` answers `303` to
    `/<locale>/newsletter/confirmed`, moves the subscriber to `confirmed`, records `confirmed_at` and
    clears the confirm token. A used, unknown or expired token answers `303` to
    `/<locale>/newsletter/expired`, which offers to sign up again with the address prefilled where it
    can still be resolved.
98. Every message to a subscriber carries a working unsubscribe link and the one-click list headers
    `List-Unsubscribe` and `List-Unsubscribe-Post`. The unsubscribe token is created with the
    subscriber, never rotated and never derived from the address.
99. `GET /api/subscriber/unsubscribe?token=<token>` unsubscribes at once, without sign-in or a
    confirmation step, and answers `303` to `/<locale>/newsletter/unsubscribed`;
    `POST /api/subscriber/unsubscribe` with `{"token": "<token>"}` does the same and answers `204`.
    This link is the only state-changing `GET` in the product.
100. Unconfirmed subscribers older than fourteen days are deleted.
101. The site only collects and confirms subscribers; it never composes or sends campaigns.

### Contact enquiries and abuse controls

102. Anti-abuse starts from the form itself. The contact modal in its contact mode asks for `First Name`, `Last Name`, `Email`, `Country`,
     `Message` (1 to 4000 characters) and the privacy consent, and opens from `Get in contact` and
     from any contact control on any route.
103. `POST /api/lead/contact` writes one `lead` with kind `contact` and answers `202` with a
     `requestId`.
104. The privacy consent box of the contact, quotation and file forms sits beside the sentence `I have read and understood the Privacy Policy.`, starts unticked, is never combined with another
     agreement, and is required: a submission without it is refused on the client and on the server.
105. Each accepted lead stores `consent_privacy`, the moment of consent and `consent_text_hash`,
     the lowercase hexadecimal SHA-256 of the exact privacy sentence shown with that form in that
     locale. The request carries the same hash in `consent.textHash`; a hash that does not match the
     sentence the server holds for that form and locale is refused as invalid, because the visitor
     saw a different sentence.
106. An email address is accepted when it has a non-empty local part, a single `@`, a domain with
     at least one dot and a final label of at least two characters, no whitespace, and at most 254
     characters in total. Only the domain part is lower-cased, and addresses compare
     case-insensitively.
107. Every form rejects invalid input inline, naming the field, and writes nothing. The server
     refuses an invalid body with `422` and an `error.fields` map keyed by the request field names
     (`firstName`, `lastName`, `email`, `country`, `city`, `role`, `industry`, `taxId`, `message`,
     `consent`, `entries`), and refuses an unknown property, malformed JSON or an oversized body with
     `400`. The client validates a touched field on leaving it and thereafter on every keystroke,
     never marks an untouched field before the first submit, validates everything on submit, moves
     focus to the first invalid control without scrolling past it, and never disables the submit
     control because of invalid input.
108. Every lead form carries a decoy field named `website`, sent as `meta.website`, placed off
     screen, out of the tab order and with autocomplete off. A submission with it filled answers
     exactly as a success but writes nothing and sends nothing.
109. Every form fetches `GET /api/form-token` when it renders and sends the token as
     `meta.formToken`. A token is signed by the app, lasts twenty-four hours and may be reused within
     that time. A submission made less than one and a half seconds after its token was issued is
     treated like a filled decoy: a success answer, nothing written. A missing or forged token is
     refused as invalid.
110. Every lead endpoint requires `idempotencyKey` of at least 16 characters. The first answer is
     kept for twenty-four hours: a repeat with the same key and the same body returns it again with
     the header `Idempotent-Replayed: true` and writes nothing new; the same key with a different
     body answers `409` with the code `idempotency_conflict`; a missing or short key is refused as
     invalid. Two simultaneous requests with the same key and body produce exactly one lead.
111. An address that submits repeatedly is limited: at most five accepted lead submissions per
     address per hour across the three lead endpoints, and at most three newsletter sign-ups per
     address per twenty-four hours. A submission over the limit answers `429` with a `Retry-After`
     header, `error.retryAfterSeconds` above zero, a message naming the wait in whole minutes, and
     the enquiry address as an alternative. If the counter store cannot be reached, lead and sign-up
     submissions are refused while browsing and search keep working.
112. A contact message containing more than two links, or whose letters are more than sixty per
     cent outside the Latin script, is accepted and stored in `quarantined` rather than refused. A
     quarantined enquiry sends no email until a `commercial` user releases it, which moves it to
     `received` and lets it proceed like any other.
113. No abuse control may silently lose a real enquiry: quarantine is visible in the back office,
     rate limiting states its wait, and only the decoy path discards.
114. Validation, rate limiting, a failed save and a success each show different wording. A failed
     save (the database cannot be reached) answers `503`, says the message was not sent, gives the
     enquiry address and keeps the form intact; a visitor is told to try again only when trying again
     can help.

### Delivery and mail, for two audiences (the visitor and the staff)

115. All mail goes over real SMTP to `mailpit` at `SMTP_HOST` and `SMTP_PORT`, from `Verdea <hello@verdea-outdoor.com>`, addressed to exactly one recipient, with no cc and no bcc, in the
     locale of the submission, in both a rich and a plain form, readable with images blocked, with no
     tracking pixel and no rewritten link.
116. A lead moves `received`, then `queued`, then `delivered`. Work that depends on other work is a
     chain: the confirmation is enqueued by the delivery that succeeded, never scheduled beside it. Delivery is the new-enquiry
     notification to the commercial inbox `commercial@example.com` being accepted by SMTP; the lead's
     `delivered_at` is set then and only then. A lead whose notification keeps failing is retried with
     exponential backoff and jitter, so a downstream outage never retries everything at once, and ends `failed` after its last attempt, still stored and visible in the back
     office. Nothing that talks to SMTP runs inside the request that accepted the lead.
117. The staff notification subject is `New enquiry received` for a contact, `New quotation: `
     followed by the reference for a quotation, and `New file request: ` followed by the document name
     for a file request. A contact notification carries a link to `/office/leads/<id>` and never the
     message, the visitor's address or the visitor's email. A quotation notification lists the
     configured lines and never the fiscal number, the message or the city.
118. The visitor's confirmation for a contact or a quotation is sent on the lead's transition into
     `delivered`, exactly once, however many delivery attempts ran. The contact confirmation has the
     subject `Verdea enquiry received` and restates the message, the enquiry address and the expected
     response time. The quotation confirmation has the subject `Quotation request received: `
     followed by the reference, for example `Quotation request received: VQ-7K4M9P`, and lists every
     configured line with every chosen option, because it is the visitor's only copy of the request.
119. The file grant email has the subject `Your Verdea download: ` followed by the document name,
     for example `Your Verdea download: Tee Sign Heritage technical files`, carries the full
     `/api/files/<token>` link and states the expiry. It is sent once the file request is stored and
     does not wait for delivery.
120. The newsletter confirmation has the subject `Confirm your Verdea newsletter subscription`,
     carries the full confirmation link with its fourteen-day expiry stated, and carries the
     unsubscribe link and headers.
121. A decoy submission, a too-fresh submission, a refused submission and a quarantined enquiry send
     no mail. A repeat of an idempotent request sends no second mail.
122. The server-to-SMTP call has an explicit timeout, and a failure there never turns an accepted
     submission into a visitor-facing error. For deliverability, transactional and newsletter mail use
     different sending subdomains of the sending domain, so a complaint against one never harms the
     other.

### Search

123. One search control lives in the header. `GET /api/search?q=<query>&locale=<locale>` answers
     `{"products": [...], "pages": [...]}`, where products are matching products of the locale (with
     slug, title and collection) and pages are matching articles and pages (with kind, slug, title and
     summary). `type` restricts to `product`, `article` or `page`, and `limit` caps each group at no
     more than eight.
124. The query is trimmed and cut to 100 characters; fewer than two characters is refused as
     invalid. Matching is prefix-aware on the last word, so `tee sig` already finds `Tee Sign Heritage`.
125. Accents fold on both sides: `praca` in `pt` finds `Banco Praça Longo`, `salida` in `es` finds
     `Señal de Salida Heritage`, and `depart` in `fr` finds `Panneau de Départ Heritage`. A document
     is matched in its own language and never through another language's stemming.
126. The query is text, never a pattern and never markup: `(bench` answers normally, and a query
     containing angle brackets comes back as plain text in the results and is shown as text.
127. In the dropdown, results appear once at least two characters are typed and the typing has
     settled; the previous results stay, dimmed, while a new query is in flight, and never blank out.
     Groups with no results are absent; no results at all shows one announced message naming the query
     and offering the catalogue. A failed search says the results may be incomplete or that search is
     unavailable, and is never indistinguishable from no results.
128. The matched part of each result is emphasised by splitting the text, never by building markup.
     A result without an image shows a placeholder chosen deterministically from a small set by its
     stable key, so it never flickers.
129. Arrow keys move the highlight without wrapping, Enter opens the highlighted result or the first
     one, a first Escape closes the dropdown and a second collapses the field and returns focus to the
     search control, Tab leaves and closes, and leaving without choosing collapses after a short
     delay so a click on a result is never lost.
130. Unpublishing a product removes it from search at once.

### Journal, careers and pages

131. `/en/journal` shows the label `Journal`, the headline, the category chips (`All`, `Press releases`, `Sustainability`, `Case Studies`, `Products`, `Educational`, `Institutional`), the
     `Latest Articles` strip, the featured case study rail, one block per category that has articles
     (up to three cards and a `View All` control, in the categories' authored order), the closing
     statement and the newsletter. A category with no articles in the locale stays visible as an
     unavailable chip; `Institutional` has none in English.
132. Selecting a category navigates to its own route, `/en/journal/case-studies`. The English
     journal holds 19 articles: 13 Case Studies, 2 Sustainability, 2 Products, 1 Educational, 1 Press
     releases and 0 Institutional. Portuguese and Spanish hold the same 19; French lacks the press
     release. The Portuguese Case Studies route is `/pt/jornal/casos-de-estudo`.
133. Ordering and pagination on a category route: its articles are listed newest first by the
     article's own authored date, ties broken by identifier, twelve per page. Page one is the bare category address and is canonical; later pages
     add `?page=2` and carry a canonical link to themselves with previous and next relations. The
     paginator is absent when there is one page. Infinite scrolling is not used, so the footer stays
     reachable.
134. `GET /api/articles?locale=en&category=case-studies&page=2` answers a top-level array of at most
     twelve article projections (slug, title, date, category, summary) with the total in the header
     `X-Total-Count`; page one holds 12 Case Studies and page two holds 1. `GET /api/categories?locale=en` answers the six categories with their article counts.
135. A category route in a locale where it has no articles shows an empty state offering the
     Portuguese version, never a not-found page; an unknown category segment answers the not-found
     page offering the category list.
136. `Ridge Viewpoint Boardwalk` (`/en/journal/case-studies/ridge-viewpoint-boardwalk`, dated
     2026-05-12) is the newest article in every locale. The next newest English articles are `Recycled Plastic, Explained` (`recycled-plastic-explained`, 2026-03-02), `HPL in the Open Air`
     (`hpl-in-the-open-air`, 2026-02-10) and the press release `Verdea Opens Its Spanish Establishment` (`verdea-opens-spanish-establishment`, 2026-01-15); every other article is dated
     before 2026. `Why Galvanised Steel Lasts` (`why-galvanised-steel-lasts`) is the Educational
     article.
137. An article's composition: its category (linking to the category route), its title, its reading time as
     `<n>min Read`, a gallery affordance with the count beyond the first three images and `View gallery`, the opening figure, the `Keep Reading` cue, the body, and structured credits (`Client:`
     and `Design:`). Reading time is the plain-text length divided by five, divided by 180, rounded,
     and never below one. `Ridge Viewpoint Boardwalk` has a five-image gallery (showing `+2`) and the
     credits `Client: Municipality of Alvora` and `Design: Atra`.
138. `GET /api/articles/ridge-viewpoint-boardwalk?locale=en` answers the article with
     `readingMinutes`, `galleryCount`, `credits`, `relatedArticles` (up to three newer-first others in
     the category) and `relatedProducts` (the products listing it, here `Boardwalk Module` and
     `Viewpoint Platform Deck`).
139. A figure set of one image renders as a figure, not a gallery; a missing gallery removes the
     affordance; an empty related strip is absent.
140. Article bodies are rendered through a serialiser mapping each rich-text node type to an element,
     never inserted as raw markup. Links are allowed only for `https`, `mailto` and `tel`; any other
     link renders as plain text. Internal links resolve by slug.
141. Mixed-language text in a body is rendered exactly as authored; nothing tries to detect or strip
     a language.
142. `/en/careers` lists the four open positions `CNC Operator`, `Serralheiro Civil`, `Project Manager` and `Installation Technician`, each with its location, employment type and an apply
     control opening the external recruitment site in a new context. `Serralheiro Civil` is written
     in Portuguese and its row declares that language. `GET /api/jobs?locale=en` answers the four as a
     top-level array. With no positions, the heading, the standing invitation and a speculative
     application link appear instead, never an empty list or a zero. There is no application form and
     no upload.
143. `/en/careers/<id>` shows one position with its description and the apply control.
144. The home route shows three most recent articles in the locale in `Recent News`; the about route
     shows three in `Never miss an update` with `More News`. Fewer articles render fewer cards, never
     placeholders.
145. Every public route is also available as plain markdown at its address followed by `.md` (for
     example `/en/products/golf/tee-sign-heritage.md`), generated from the same content, carrying the
     page's substance and none of its navigation chrome, and listed in `/llms.txt`.

### Consent, privacy and legal pages (one privacy regime: the EU general data protection regulation)

146. A first-time visitor sees a consent banner offering `Accept all`, `Reject all` and `Choose`,
     with equal prominence, over the four categories necessary, preferences, statistics and marketing.
     Reject is one action. Nothing but necessary storage is written before a choice, and closing the
     banner is not consent.
147. A choice is stored in the `verdea_consent` cookie as the comma-separated granted categories
     (for example `necessary,preferences`), is remembered across reloads so the banner does not return,
     and writes an append-only `consent_receipt` through `POST /api/consent` with the visitor key, the
     categories, the policy version, a truncated and hashed network address and the browser family.
     A changed choice writes a new receipt.
148. A persistent consent control in the lower corner of every route, the error pages included,
     reopens the banner. Withdrawing a category deletes what was stored under it.
149. The site is fully usable with every optional category refused. The chosen language is then
     carried by the address alone and simply not remembered on return.
150. Data minimisation, applied: no full network address is written anywhere: an address is truncated (last octet, or the last
     eighty bits) and then hashed with a key that rotates every thirty days.
151. The legal pages are `/en/legal/privacy-policy`, `/en/legal/cookie-policy` and
     `/en/legal/terms-of-use`, each showing its title, effective date and version. The privacy policy
     is linked from the footer, from every form's consent sentence and from the banner; the cookie
     policy from the banner and the privacy policy; the terms from the footer.
152. Publishing a new version never overwrites an old one: `/en/legal/privacy-policy/v/1` stays
     addressable, carries the banner `This version has been superseded.` linking to the current page,
     and the current page links back to it. A version that never existed answers not-found.
153. A legal page's composition: every heading carries a stable anchor derived from its text, a contents list is generated
     when a page has more than four second-level headings (the privacy policy does), and a legal page
     missing in a locale redirects to the Portuguese version with a line saying the binding text is in
     that language.

### Not-found and error pages

154. An unknown address, an unpublished document or a bad slug answers `404` with the product's own
     not-found page in the visitor's locale: the full chrome, a designed image, an editable heading
     and sentence, the search control, and links to the catalogue (`/en/products`), the journal
     (`/en/journal`) and the home (`/en`). There is no automatic redirect and no countdown.
155. Where the requested path is one segment away from a real route (a mistyped slug or segment), the
     not-found page names that destination first.
156. A slug that is not lower-case letters, digits and single hyphens of at most 120 characters is
     answered with the not-found page without any content lookup.
157. A failure on the app's side answers `500` with a different page saying something went wrong on
     our side, the request identifier as a short quotable string, and the enquiry address. No page ever
     shows a stack trace, a query fragment, `undefined`, `null`, `NaN` or an empty bracket pair.
158. The not-found and error pages carry no live object, no sound and no scroll-driven motion.

### The back office

159. `/office/login` signs a staff member in; `/office/leads`, `/office/leads/<id>`,
     `/office/subscribers` and `/office/products` are the screens. They are not localised.
160. `GET /api/office/me` answers the signed-in `email`, `role` and `displayName`.
161. `GET /api/office/leads/summary` answers enquiry counts by kind and by status, for both roles.
162. `GET /api/office/leads` (filterable by `kind` and `status`) answers a top-level array of
     enquiries for `commercial` and is denied to `editor`.
163. `GET /api/office/leads/<id>` answers one enquiry in full, including its message, its fiscal
     number and, for a quotation, the reference, the stored lines with their option names, and the
     rendered payload, for `commercial` only; each read writes an audit event `lead.read`. `editor`
     is denied and nothing is recorded as read.
164. `POST /api/office/leads/<id>/release` moves a `quarantined` enquiry to `received`, for
     `commercial` only, and writes `lead.release`; releasing an enquiry that is not quarantined is
     refused and changes nothing.
165. `GET /api/office/subscribers/summary` answers subscriber counts by status for both roles;
     `GET /api/office/subscribers` answers the subscriber list for `commercial` only and writes
     `subscriber.list`.
166. `GET /api/office/products?locale=<locale>` answers every product of the locale with its publish
     state for both roles.
167. `POST /api/office/products/<id>/unpublish` and `POST /api/office/products/<id>/publish`, each
     with `{"locale": "<locale>"}`, change one product's publish state in one locale, for `editor`
     only, and write `product.unpublish` or `product.publish`. `commercial` is denied and the state is
     unchanged.
168. An unpublished product disappears at once from its locale's catalogue, total, collection counts,
     search and sitemap, and its route answers not-found; republishing restores all of it. Existing
     quotation lines keep their stored names.
169. Every audit event records the actor, the action, the subject and the request identifier, and the
     app never edits or deletes one.
170. The enquiry screen shows kind, status, locale, name and date in a filterable table with headers
     tied to their cells; quarantined and failed enquiries are marked by a word as well as a colour;
     the enquiry detail offers a control that copies the rendered payload.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | redirect to a locale home | none |
| `/en` | home | none |
| `/en/products` | catalogue index with facets | none |
| `/en/products/urban` | a collection | none |
| `/en/products/golf/tee-sign-heritage` | a product | none |
| `/en/wishlist` | the wishlist | none |
| `/en/journal` | journal index | none |
| `/en/journal/case-studies` | a journal category, paged with `?page=2` | none |
| `/en/journal/case-studies/ridge-viewpoint-boardwalk` | an article | none |
| `/en/about` | the company story | none |
| `/en/sustainability` | the materials story | none |
| `/en/careers` | open positions | none |
| `/en/careers/<id>` | one position | none |
| `/en/legal/privacy-policy` | a legal page | none |
| `/en/legal/privacy-policy/v/1` | a superseded version | none |
| `/en/newsletter/confirmed` | subscription confirmed | none |
| `/en/newsletter/expired` | confirmation link expired | none |
| `/en/newsletter/unsubscribed` | unsubscribed | none |
| `/pt/produtos`, `/es/productos`, `/fr/produits` | the catalogue in the other locales | none |
| `/pt/produtos/detalhes/placa-de-sala-slim` | a Portuguese product | none |
| `/llms.txt` | index of the markdown pages | none |
| `/sitemap.xml` | sitemap index listing `/sitemap-pt.xml`, `/sitemap-en.xml`, `/sitemap-es.xml`, `/sitemap-fr.xml` | none |
| `/robots.txt` | crawler rules | none |
| `/office/login` | staff sign-in | none |
| `/office/leads` | enquiry list | `commercial` for contents, `editor` sees counts |
| `/office/leads/<id>` | one enquiry | `commercial` |
| `/office/subscribers` | subscriber list | `commercial` for addresses, `editor` sees counts |
| `/office/products` | product publish states | both; `editor` changes them |

Every route above exists in all four locales with its localised segment and slug.

**Entry and redirects.**

- `/` answers `302` to a locale home by rule 9; a deep link is never redirected by language.
- Upper case or a trailing slash answers `301` to the canonical address; a product under the wrong
  collection answers `301` to its canonical path; a document missing in a locale answers `302` to
  the Portuguese version with the notice.
- Every modal (contact, quotation, file request, options, references, gallery, mobile menu, the
  narrow-screen filter panel) opens over the current route without changing the path, pushes a
  history entry so the back gesture closes it, and closes on Escape with focus returned to its
  opener.
- A back-office screen without a session goes to `/office/login` and returns afterwards; a session
  that expires mid-action returns to `/office/login` with the pending page remembered; a staff
  member on a screen their role may not use sees a denial naming the action instead of the data.
- Signing out on `/office/leads` returns to `/office/login` and the old token is refused.
- The client takes over navigation after the first document; if that fails, every link is a real
  link and navigation falls back to a full page load.

**Journeys.**

1. Specifier. Open `/en/products`; choose Golf in `by Collections` and Signage in `by Products`;
   see `Showing 2 of 20 Results` and the address carry both facets; open `Tee Sign Heritage`;
   press the bookmark; in `Personalise your product` choose `M` (the drawing changes), `Galvanised steel`, `Anthracite grey RAL7016`, `HPL +` and `Dark green`; add; see the confirmation with the
   product name, undo and the draining bar; open `Plaza Bench Long` and save it in size `2000`; open
   `/en/wishlist` and see two rows with their chosen names; press `Request a quotation`; fill `First Name`, `Last Name`, `Email`, `Role`, `Industry`, `Country` and `City`, tick the privacy box; send;
   see the confirmation with a `VQ-` reference; see the wishlist empty afterwards.
2. Wishlist editing. Save `Frame Bollard` twice in two colours; see two rows and a bookmark count on
   its card; press undo on the second confirmation and see only that entry go; reload and see the
   list unchanged; switch to Português and see the same rows resolved in Portuguese.
3. Document hunter. Open `Tee Sign Heritage`; press `REQUEST INFORMATION`; give a name and an email
   and tick the privacy box; send; see `Tee Sign Heritage technical files` with a download control
   and a line saying it was emailed; download the PDF.
4. Collection catalogue. Open `/en/products/urban`; see `Showing 6 of 20 Results` and the `Urban Catalogue` card in the grid; open it; request it; download `Urban Catalogue`.
5. Language. On `Tee Sign Heritage`, open the language selector, choose `es`, and land on
   `/es/productos/golf/senal-de-salida-heritage`; open `Slim Room Sign` in English and see the Spanish
   item marked as leading to the Spanish home.
6. Reader. Open `/en/journal`; see `Institutional` unavailable; choose `Case Studies`; go to page 2;
   open `Ridge Viewpoint Boardwalk` from page one; open the gallery, move with the arrow keys, close
   with Escape; follow a related product to `Boardwalk Module`.
7. Newsletter. Enter an address in the footer form; see the check-your-inbox line; follow the link in
   the message; land on the confirmed page.
8. Search. Open the search control; type `tee sig`; see the grouped results with the match
   emphasised; press Enter; land on `Tee Sign Heritage`.
9. Commercial. Sign in at `/office/login` as `commercial@example.com`; open `/office/leads`; filter
   to quotations; open one and see its reference, its lines and its rendered payload; release a
   quarantined contact.
10. Editor. Sign in as `editor@example.com`; see counts but no enquiry rows; open `/office/products`;
    unpublish `Golf Bag Stand` in `pt`, see `/pt/produtos` drop to 19, then publish it again.

**States.** The catalogue with nothing matching, the empty wishlist, a journal category empty in a
locale, a search with no results, careers with no positions, and the back-office lists with nothing
in them each have a designed empty state. Every page reserves space for images and shows a flat
placeholder tone while they load, never a blank or a spinner without end. Every loading state
resolves into a result or a message. An error never crashes the app: a failing section removes
itself and the rest of the page keeps working.

## UI/UX notes

**North star.** Somebody arriving should understand at once that this is a maker of durable outdoor
objects, shown as real things resting on a table, and should feel invited to take their time.

**Register.** Consumer and editorial, with the product itself the first thing seen; the wishlist,
the forms and the back office switch to a quiet working register: plain, still and dense enough to
scan. The design direction is the one the reference site was measured to have, described below in
words; its exact values are yours to choose within these rules.

**Stances.** Objects over photographs: products are renders on the page ground, and photography is
reserved for places, projects and people. Space over boxes: nothing is boxed unless it is a control.
Slow over busy: scrolling is the main interaction and movement settles rather than snaps. Honest
over flattering: counters, empty states and error messages say exactly what is true.

**Palette by role.** The page ground is a warm off-white, nearer paper than white. Surfaces that sit
above it (the header capsules, cards on a dark field) are a plainer, lighter near-white neutral. The
product card tile is a warm neutral one step deeper than the page, and a card placed on the page
ground uses a tile a step warmer again, so the two stay visibly separate with no shadow. Hairlines
are a light warm neutral; a lighter near-white neutral rule is used inside cards. Placeholder marks,
disabled ink and secondary ink step down through light warm neutrals to a mid warm neutral for
tertiary text and a deep warm neutral just short of the ink. All text, every icon and the dark fill
is one ink: an almost-black neutral with a warm cast. White is used only for text and pills over
photography. One fluorescent yellow (a light, soft amber that reads as yellow) is the brand signal:
the footer field, the third theme and a loud accent, and it appears rarely and loudly, never as a
background for body copy in the main catalogue. A whisper of that yellow is a section ground. A deep
green that reads almost black is the ground behind sustainability material. The five collections
each carry an accent used only on their own pill and chapter: a light muted orange (sand), a pale
sage green that reads nearly neutral (leaf), a light muted blue (sky), a light vivid red leaning
orange (flame), and, for the fifth collection, the warm tile neutral itself. One mid, vivid red means
something has gone wrong in a form and appears nowhere else; its pressed state is a deeper red.
Black appears only as a scrim over photography. The page must never be dominated by a single hue
family with no second signal; the yellow and the collection accents are the second signals. The
exact shades are yours, so long as every role above stays distinct and every pairing meets the
contrast floors below.

**Themes.** The header carries one of three themes and cross-fades between them rather than swapping:
`dark` (ink on the paper ground, the default everywhere), `light` (white over photography and over
the deep green), and `fluor` (ink on the yellow, the sustainability route's default and the footer).
The theme follows whichever section currently sits under the header. The naming is deliberately
inverted (`dark` means dark ink) and is kept.

**Typography.** One licensed geometric sans typeface carries the whole site at one regular weight; nothing is ever
bold. Hierarchy comes from size and space alone, which is why pages feel calm. Sizes interpolate
smoothly with the viewport width between a floor and a ceiling and stop growing on very wide
screens. Display lines set nearly solid, body text sets loose, and long-form article text sets
loosest of all. Small labels are upper-cased and letter-spaced. Where the licensed face is
unavailable, a metric-matched fallback sans stands in so no headline reflows when the face arrives.
The family and every size are yours, within these relationships.

**Shape and depth.** The corner radii describe exactly two shapes: a fully rounded pill (tags, collection chips, header
navigation items) and a softly rounded rectangle (buttons, cards, inputs), plus circles for swatches
and round icon buttons, and a noticeably rounder panel for modals. Only two shadows exist: a soft
short one under the floating filter control and one under the consent badge. Products never carry a
box shadow; their long soft ground shadow is part of the render, and a card with both reads as two
light sources. Every fade at the bottom of a scrolling panel is a vertical gradient that runs a colour into its own
transparent form, never into a generic transparent that leaves a dirty band on the warm ground.

**Density and space.** Spacious on public routes: sections read as separate at a glance without a
dividing line, and the gap between sections is several times the gap beneath a heading. Spacing
comes from one fluid gutter and one fluid page margin defined once and read everywhere, on a
column grid fine enough that the product split and the article measure need no half-columns. The
back office is comfortable and compact enough to scan a full table.

**Motion.** Everything that moves shares one signature transition curve that leaves fast and settles
for a long time, so an element reads as an object arriving rather than a value changing, and one
default speed of about half a second. Slower drifts are reserved for surfaces the size of the
viewport. Three overshoot curves are held in reserve and used at most once per surface; the only
overshoot a visitor meets on a product route is the rotate control arriving. Entrances rise a short
distance while fading in, once, on first entry, and never reverse on scroll up. Nothing's visible
state depends on an animation: every element is visible by default, so a page whose motion never
starts is complete. With reduced motion requested, every reveal, wipe, parallax, drift, pulse, bob,
curtain and idle rotation stops and the smooth scrolling is disabled entirely; only the header's
colour cross-fade remains, because it is colour, not motion. The preference is read at start-up and
followed live.

**Mode.** Light only, in the three themes above. There is no separate dark mode.

**Page composition.** Pages are prerendered on the server and arrive complete; the composition of each
route is an ordered list of sections, permitted and ordered rather than guaranteed present.

**Primary action.** Each page leads with one clear primary action, visually distinct from every
secondary one: the ink-filled pill (`REQUEST INFORMATION`, `Request a quotation`, `Start adding`, a
form's send control). Secondary actions are outlined or text.

**Responsive.** The layout is responsive across the whole width range with two real turning points
and a ceiling: one just above tablet width (the header pills become a menu mark opening a full-screen
menu, the facets move behind the floating filter control, the catalogue drops from four across to
two, the product split stacks with the object first, the footer bands stack), one at phone width (the
catalogue drops to one across, specification labels sit above their values, the article loses its
label rail, category rails become one card with sideways scrolling, the type bottoms out), and a
ceiling on very wide screens (type and content width stop growing and centre, full-bleed media keeps
running to the edges, the catalogue gains a fifth card across, the home field spreads). Every width
between those points holds without breaking, and nothing scrolls sideways at a narrow viewport.
Full-height chapters are sized from the height captured at first load, so a mobile address bar
collapsing never resizes a photograph mid-scroll. Hover treatments exist only on devices that can
hover; on touch, the card bookmark and the rotate control are always visible.

**Accessibility.** The site and the back office meet WCAG 2.2 AA. Body text contrast is at least
4.5:1, large text at least 3:1, and interface components and focus indicators at least 3:1, in every
theme and over every photograph the header sits on, which is why text over photography always sits
on a scrim. Focus is never removed: a visible focus ring of at least 2 pixels with 3:1 contrast
against both neighbouring surfaces, drawn outside capsules so it shows on both fills. Every
interactive target is at least 44 by 44 CSS pixels on touch, including the swatches, whose hit area
is larger than their drawing. Full keyboard navigation covers every route, the search, the filter
panel, the options modal, the timeline, the rails and all four forms, and the smooth scrolling never
breaks arrow keys, page keys, Home and End, find-in-page or anchor jumps. Every icon-only control has
a label, meaning is never carried by colour alone, every content image has alternative text and
decorative images declare themselves decorative, and a split headline is read as one sentence.

## Technical requirements

**Stack.** TypeScript on Node.js 20, in one production build.

- Backend: NestJS. It serves the JSON API under `/api` and every public route as a complete HTML
  document on the same origin. A request made without running any script receives the page's
  headings, copy, images, navigation, footer and working links; the catalogue arrives with its cards
  and its counter already computed.
- Frontend: Lit web components bundled with Vite. The components are rendered on the server for the
  first paint and then take over in the browser, which handles navigation between routes from then
  on; every navigation control stays a real link.
- Database: PostgreSQL, the `postgres` service, read from `DATABASE_URL`.
- Mail: the `mailpit` SMTP service, read from `SMTP_HOST` and `SMTP_PORT`; `SMTP_USER` and
  `SMTP_PASS` are provided and empty, because the server takes no authentication.
- Public address: `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`.

Beyond NestJS and Lit, choose the libraries you need (database access, SMTP sending, PDF
generation, motion, smooth scrolling, real-time 3D rendering) from the public npm registry, installed
when the image is built; nothing is fetched at runtime. Do not introduce a second database, cache,
queue, object store, identity provider or mail vendor: the only backing services available in this
environment are PostgreSQL (`postgres`) and Mailpit (`mailpit`), and reaching for anything else is a
contract violation. Any signing key the app needs is generated by the app on first start and kept in
its own database, never read from the environment.

**Health.** `GET /api/health` answers `200` with `{"status": "ok"}` once the database is reachable.
It does not depend on SMTP.

**Content.** The catalogue, the journal, the page copy and the form option lists are seeded by the
app into its own database on first start, one document per locale joined by a stable identifier. A
page is composed from an ordered list of sections, any of which may be absent, and a missing section
renders nothing rather than an error. No user-facing string is hard-coded in a component without a
per-locale source. Media follows a zero-asset substitution: it is generated by the app rather than shipped as files: product renders and
live objects are composed from simple primitive shapes at the right silhouette with the long soft
ground shadow beneath them, photographs are visibly placeholder landscapes built from the palette
with a fine grain, the environment light is generated (a bright elliptical specular highlight high in the upper hemisphere and a broad, dimmer fill opposite it, over a pale sky and a warm ground bounce), the confirmation and transition sounds are
synthesised, and the gated PDFs are generated from the product and collection content.

**Background work.** A write endpoint commits the record and returns, so concurrency between a request and its follow-up work never matters to the visitor; every SMTP call happens
afterwards in a worker inside the app process, with an explicit timeout, retries that back off with
jitter, and a final `failed` state. Each lead status change is an assignment from a named current
state to a named next state, so two workers acting on one lead produce one transition. The visitor
confirmation is tied to the transition into `delivered`, not to a delivery attempt.

**Security.** Every response carries these security headers: `Strict-Transport-Security` with a
`max-age` of at least one year and `includeSubDomains`; `X-Content-Type-Options: nosniff`;
`Referrer-Policy: strict-origin-when-cross-origin`; a `Permissions-Policy` denying camera,
microphone, geolocation and payment; `Cross-Origin-Opener-Policy: same-origin`; and an enforcing
`Content-Security-Policy` with a per-response nonce, `frame-ancestors 'none'`, `object-src 'none'`,
`base-uri 'self'`, `form-action 'self'`, `connect-src 'self'`, and a `script-src` that allows only
the site itself and the nonce, with no `'unsafe-inline'` and no `'unsafe-eval'`. Styles written by the
motion system go through element style properties, so no inline style allowance is needed. No
secret reaches the browser: no database address, database password, SMTP setting, signing key,
staff password or form-signing key appears in any HTML, script, style or map file the browser can
download. Every route slug is validated before it is used, and content lookups bind route values as
parameters, so a path can never alter a query. Search input is escaped before any pattern is built
from it. Rich text is rendered node by node with the link scheme allow list. Unknown request
properties are refused, not ignored.

**Privacy.** The personal-data inventory is closed: the only personal data held is what the forms collect (names, email, country, city,
company, fiscal number, message, the configured list), truncated and hashed network addresses, the
browser family, consent choices and the two staff accounts. No telephone number is collected, no
visitor identifier persists across sessions, and no third party receives a visitor's network address.

**Observability: logging and tracing.** Each request writes one structured log record with the time, level, request
identifier, route, status, duration and operation name. No log record contains an email address, a
name, a message, a token, a grant, a session value, a credential or an unmodified network address,
and a redaction step drops known sensitive keys before anything is written. Every response carries
the request identifier in `X-Request-Id` (echoed when the request supplies one), and the same
identifier appears in error bodies and in the work that request enqueued.

**Generated documents.** `/sitemap.xml` lists the four per-locale sitemaps, each listing every
published public route with its last change and its `hreflang` alternates. `/robots.txt` allows
everything except `/api/` and `/office`, written as the lines `Disallow: /api/` and
`Disallow: /office`, and names the sitemap on a `Sitemap:` line. `/llms.txt` lists every per-route
markdown page. All three reflect publish changes immediately.

**Failure order.** When something fails, the site sheds its layers in this order and keeps
everything beneath the failing one: sound first, then the live object, then the scroll-driven
motion, then the client-side page transitions, then search, then the forms, and the catalogue and its
pages last. A browser that runs no script still reads every public route in full. A failure inside
one section removes that section only. The database being unreachable leaves pages that are already
rendered readable and makes every form answer the failed-save message.

**Offline.** The site keeps a minimal offline copy of its shell, its type, its styles, its wordmark
and a dedicated offline page, and nothing containing personal data. With the network off, a
previously visited route opens with a persistent dismissible line saying the connection is gone; an
unvisited route shows the offline page with the enquiry address, the telephone number and the
wishlist count; a form submission is refused with its values kept and is never queued to send later;
the wishlist keeps working. When the network returns the line disappears.

## Data model

The invariants below hold whatever the code does, and referential integrity is enforced by the app
because content references are checked on read: a reference that resolves to nothing renders the
element absent, never a dead card. Nine pinned tables plus the content tables, which are yours to name. All timestamps are UTC.
Identifiers are opaque values the app generates, sortable by creation time; no sequential integer is
ever exposed in a route or a payload.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

**`lead`**: `id`, `kind` (`contact`, `quotation`, `file_request`, `newsletter`), `locale` (`pt`,
`en`, `es`, `fr`), `first_name`, `last_name`, `email`, `country`, `city`, `company`, `tax_id`,
`role`, `industry`, `message`, `wants_technical_files` (boolean, false by default), `source_route`,
`consent_privacy` (boolean, never empty), `consent_text_hash` (never empty),
`consent_recorded_at`, `status` (`received`, `queued`, `delivered`, `failed`, `quarantined`),
`delivered_at`, `attempts`, `last_error`, `created_at`, `updated_at`. A `delivered` lead has a
`delivered_at` and no other status has one. No lead exists without a true `consent_privacy`, a
consent moment and a text hash.

**`quotation`**: `id`, `lead_id` (exactly one lead, of kind `quotation`, and one quotation per
lead), `reference` (unique), `item_count`, `payload_rendered`, `payload_hash`, `submitted_at`,
`created_at`. `item_count` always equals the number of its lines. `payload_rendered` is kept even
though it could be recomputed, because it is what was sent.

**`quotation_item`**: `id`, `quotation_id`, `position` (1, 2, 3 and onward without gaps, unique
within a quotation), `product_id`, `product_slug`, `product_title`, `collection_name`,
`option_size`, `option_structure`, `option_color`, `option_display`, `option_hpl_color`,
`resolved_from_locale` (empty, or the locale the line was resolved in), `unresolved` (boolean,
false by default), `created_at`. `product_title`, `product_slug` and `collection_name` are never
empty. Every option column holds a displayed name, never a reference to an option. A quotation and
its lines exist together or not at all.

**`file_request`**: `id`, `lead_id`, `scope` (`product` or `collection_catalogue`), `product_id`,
`collection_id`, `document_name`, `asset_key`, `token` (unique), `token_expires_at` (seven days after
creation), `download_count` (0 at first), `downloaded_at`, `created_at`.

**`subscriber`**: `id`, `email` (unique regardless of case), `locale`, `status` (`pending`,
`confirmed`, `unsubscribed`, `bounced`, `complained`), `confirm_token`, `confirm_token_expires_at`,
`confirmed_at`, `unsubscribed_at`, `unsubscribe_token` (unique, never derived from the address),
`consent_recorded_at`, `consent_text_hash`, `source_route`, `created_at`, `updated_at`. A
`confirmed` subscriber has a `confirmed_at` and an empty `confirm_token`.

**`consent_receipt`**: `id`, `visitor_key`, `categories` (a JSON object with `necessary`,
`preferences`, `statistics` and `marketing` booleans), `policy_version`, `ip_hash`,
`user_agent_family`, `recorded_at`. Rows are only ever added.

**`staff_account`**: `id`, `email` (unique), `display_name`, `role` (`commercial` or `editor`),
`status` (`active`, `suspended`, `removed`), `last_seen_at`, `created_at`, `updated_at`.

**`audit_event`**: `id`, `actor_type` (`staff` or `system`), `actor_id`, `action`, `subject_type`,
`subject_id`, `request_id`, `occurred_at`. Actions written: `lead.read`, `lead.release`,
`product.publish`, `product.unpublish`, `subscriber.list`. The app only ever adds rows.

**`idempotency_record`**: the key, the endpoint, a hash of the body, the stored answer and its
creation time, kept for twenty-four hours.

**Content (your tables).** A product carries its stable identifier, per-locale title, slug and
description, one collection, a set of product types, an optional sub-collection, sizes as inline
records (name, label, dimensions text and its own drawing), references to shared option records for
structures, colours, displays and laminate colours (each a name and a swatch colour or texture), its
specification rows, its reference codes, whether it has technical documents, its installation
photographs, the case studies that feature it, an optional hand-picked related list, and a publish
state per locale. Size labels and dimensions are opaque text: never parsed, sorted as numbers or
compared. A collection carries its stable identifier (its English slug), per-locale name and slug,
its mark, its accent, its sub-collections, its product types and its optional catalogue document.
Articles carry a per-locale slug, title, summary, date (a date, not an instant), category, opening
figure, body, gallery and credits. Legal documents carry a slug, a version number, an effective date
and their body, and every version is kept.

**Seed data.**

- Staff: `commercial@example.com` (`commercial`, Carla Mendes), `editor@example.com` (`editor`,
  Rui Tavares) and `former@example.com` (`commercial`, Nuno Pires, `suspended`).
- Collections, with English name and stable identifier: Urban `urban`, Nature `nature`, Repolymer
  `repolymer`, Golf `golf`, Details `details`. Localised names and slugs: Portuguese Urbano `urbano`,
  Natureza `natureza`, Repolymer `repolymer`, Golfe `golfe`, Detalhes `detalhes`; Spanish Urbano
  `urbano`, Naturaleza `naturaleza`, Repolymer `repolymer`, Golf `golf`, Detalles `detalles`;
  French Urbain `urbain`, Nature `nature`, Repolymer `repolymer`, Golf `golf`, Details `details`.
- Product types, English name and slug: Signage `signage`, Construction `construction`, Furniture
  `furniture`, Equipment `equipment`. Urban sub-collections in every locale: Frame `frame`, Plaza
  `plaza`, Reuse `reuse`.
- Products, as stable identifier, English title and English slug, grouped by collection and type:
  - Urban: `vd-plaza-bench-long` `Plaza Bench Long` `plaza-bench-long` (Furniture, Plaza);
    `vd-frame-bollard` `Frame Bollard` `frame-bollard` (Equipment, Frame);
    `vd-frame-wayfinding-totem` `Frame Wayfinding Totem` `frame-wayfinding-totem` (Signage, Frame);
    `vd-reuse-litter-bin-duo` `Reuse Litter Bin Duo` `reuse-litter-bin-duo` (Equipment, Reuse);
    `vd-plaza-bike-rack-arc` `Plaza Bike Rack Arc` `plaza-bike-rack-arc` (Equipment, Plaza);
    `vd-bike-parking-totem` `Bike Parking Totem` `bike-parking-totem` (Equipment and Signage, Frame).
  - Nature: `vd-trail-directional-sign` `Trail Directional Sign` `trail-directional-sign` (Signage);
    `vd-ridge-interpretive-panel` `Ridge Interpretive Panel` `ridge-interpretive-panel` (Signage);
    `vd-boardwalk-module` `Boardwalk Module` `boardwalk-module` (Construction);
    `vd-viewpoint-platform-deck` `Viewpoint Platform Deck` `viewpoint-platform-deck` (Construction).
  - Repolymer: `vd-cove-picnic-table` `Cove Picnic Table` `cove-picnic-table` (Furniture);
    `vd-dune-recycled-bench` `Dune Recycled Bench` `dune-recycled-bench` (Furniture);
    `vd-terra-planter-box` `Terra Planter Box` `terra-planter-box` (Equipment).
  - Golf: `vd-tee-sign-heritage` `Tee Sign Heritage` `tee-sign-heritage` (Signage);
    `vd-classic-ball-washer` `Classic Ball Washer` `classic-ball-washer` (Equipment);
    `vd-course-distance-marker` `Course Distance Marker` `course-distance-marker` (Signage);
    `vd-golf-bag-stand` `Golf Bag Stand` `golf-bag-stand` (Furniture).
  - Details: `vd-line-door-plate` `Line Door Plate` `line-door-plate` (Signage);
    `vd-floor-directory-board` `Floor Directory Board` `floor-directory-board` (Signage);
    `vd-slim-room-sign` `Slim Room Sign` `slim-room-sign` (Signage).
- Locale coverage: Portuguese and English carry all 20; Spanish lacks `vd-slim-room-sign`; French
  lacks `vd-slim-room-sign` and `vd-golf-bag-stand`. Pinned localised titles and slugs:
  `vd-plaza-bench-long` is `Banco Praça Longo` `banco-praca-longo` in Portuguese, `Banco Plaza Largo` `banco-plaza-largo` in Spanish and `Banc Plaza Long` `banc-plaza-long` in French;
  `vd-tee-sign-heritage` is `Placa de Saída Heritage` `placa-de-saida-heritage`, `Señal de Salida Heritage` `senal-de-salida-heritage` and `Panneau de Départ Heritage` `panneau-de-depart-heritage`;
  `vd-slim-room-sign` is `Placa de Sala Slim` `placa-de-sala-slim` in Portuguese. Every other
  localised title and slug is yours, written in that language.
- Options: `Tee Sign Heritage` and `Plaza Bench Long` as rules 41 and 44 state, with `Tee Sign Heritage` sizes `S` (`190 x 100 x 1700 mm`) and `M` (`240 x 120 x 1900 mm`) each with its own
  drawing and its technical documents named `Tee Sign Heritage technical files`; `Reuse Litter Bin Duo` sizes `All`, `Bottle`, `Pet` and the single colour `Anthracite grey RAL7016`; `Frame Bollard`
  sizes `s`, `m`; `Plaza Bike Rack Arc` sizes `3`, `4`; `Boardwalk Module` sizes `25`, `50`, `100`;
  `Classic Ball Washer` sizes `R900`, `Q600`; `Course Distance Marker` sizes `110`, `1500`; `Line Door Plate` no option on any axis; `Slim Room Sign` no technical documents. Every other product has
  at least one option axis drawn from the shared option names above and has technical documents.
- `Bike Parking Totem` is the annotated product on the sustainability route, with the callouts `2 Schuko Plugs` (`230 V, max. 2.5 A and 500 W`), `Shimano Standard Charger` (`Output 40 V DC 4A`) and
  `Bosch Standard Charger` (`Output 36 V`).
- Journal categories, English name and slug, in this order: Press releases `press-releases`,
  Sustainability `sustainability`, Case Studies `case-studies`, Products `products`, Educational
  `educational`, Institutional `institutional`; counts and pinned articles as rules 132 and 136
  state; the other twelve case studies and the second Sustainability and Products articles are
  yours to write.
- Legal documents: `privacy-policy` version 1 (effective 2025-01-01) and version 2 (current,
  effective 2026-01-01, with more than four second-level headings); `cookie-policy` version 1;
  `terms-of-use` version 1.
- Careers: the four positions of rule 142.

Schema changes ship as ordered, forward-only migrations that run before the new version serves
requests; enumerated status values only ever gain members.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and interaction detail for every surface. The rules in the UI/UX
notes govern every sentence here: values are yours, relationships and behaviours are not.

### Global chrome

**Header.** Fixed over the content at the top of every route and never scrolling away, shrinking,
hiding or changing height; the only thing about it that changes is its theme. From left to right: the
wordmark linking to the locale home; a thin vertical hairline; the search control; the four
navigation destinations right-aligned; the wishlist control with its count; the sound control; and
the language selector at the far edge. The header element carries the attribute `data-theme`, whose
value is `dark`, `light` or `fluor` at every moment and is already correct in the server-rendered
document (`fluor` on the sustainability route, `dark` elsewhere), so the header never starts in the
wrong colours and corrects itself.

**Navigation pills.** `Products`, `About`, `Sustainability`, `Journal`, in that order, in every
locale, in the header and in the footer. Each sits in its own pill filled with the raised surface,
set small, upper-cased and letter-spaced; the pills abut so the row reads as a segmented control, not
a row of links with a shared background. The current route's pill takes the ink fill with the page
ground as its text, permanently. On devices that hover, a pill fills toward the ink as the pointer
arrives; on touch there is no hover state, so a tapped pill never looks active by mistake. In the
`light` theme the pills become a faint white with a white edge and white text; in `fluor` they
become ink with yellow text. There is no dropdown on the navigation: collections are reached from
the catalogue and the home sequence.

**Theme changes.** As a section boundary passes under the header, the pills and their text
cross-fade to the new theme on the signature curve over about half a second, so the header feels lit
by the page rather than repainted. A section can declare different themes for entering and leaving,
and the about timeline does.

**Search control.** Collapsed, it is the search mark alone, a button with an accessible name, and its
field cannot receive typing. Activated, the field widens sideways to its natural width over roughly
a second while its placeholder fades out, is replaced, and fades back in slightly after the widening
starts, so the text never stretches; focus moves into the field as the widening begins. The natural
width is measured once and remeasured when the window resizes. Escape handling exists only while the
field is open.

**Language selector.** The current locale in lower case (`en`) with a small downward chevron that is
its own shape, not a rotated arrow, and is used nowhere else. On hover it dims slightly, the most
consistent hover on the site. Open, it is a real menu listing the four locales, with the current one
marked as current, not merely styled.

**Mobile menu.** At or below the first turning point, a menu mark made of three parallel bars
offset into a slant replaces the pills and opens a full-screen menu on a near-opaque ink ground,
with the search already expanded inside it. The menu is a modal.

**Modal shell.** One shell serves contact, quotation, file request and product options. It opens
over a dimmed ink backdrop, as a panel with generous corner rounding and a width derived from the
grid, with its own smooth scrolling region. While any modal is open the page beneath is locked
without jumping, and the lock is counted, so closing one modal over another never unlocks the page.
The panel measures its content once and keeps that minimum height, so switching between the
`Contact`, `Wishlist` and `Files` tabs never collapses and re-expands it. The send area sits over a
fade of the panel's own colour so content scrolls out beneath it. Focus is trapped, the rest of the
page is inert, Escape and the back gesture close it, and focus returns to the opener.

**Footer.** A full-screen field of the fluorescent yellow at the end of every route, in bands: the
newsletter (`Join our community`, `Sign up for news, updates and more.`); three address blocks
(`Headquarters`, `Production`, `Verdea Spain`) each a heading and an address, with the email, the
telephone number and the line `Call to a national landline` on the first; the wordmark set enormous
and cropped by the left edge, with its registered mark as a large outlined ring; fine line drawings
of products along the right edge; the links `Products`, `About`, `Sustainability`, `Journal`,
`Careers`, `Complaints Book` and `Privacy Policy`; three round social buttons; and the credit `Made by Atra` at the right. Beneath the yellow field, a separate band on the page ground carries the
public co-funding marks, each at no less than its funder's minimum size and clear space; when they
cannot fit, the band wraps to two rows and then scrolls sideways rather than shrinking them.
`Complaints Book` is an external link and is kept in every locale; `Call to a national landline` is
a regulatory disclosure and is never dropped at any width. Addresses: Headquarters `Rua das Oliveiras 118, 3750-102 Agueda, Portugal`, `hello@verdea-outdoor.com`, `+351 234 600 118`; Production `Zona Industrial de Casarinhos, Lote 7, 3750-301 Agueda, Portugal`; Verdea Spain `Calle del Pinar 24, 36202 Vigo, Spain`, `espana@verdea-outdoor.com`. The enquiry address used across the site is
`hello@verdea-outdoor.com`.

**Consent badge.** A small round badge pinned to a lower corner, yellow with an ink mark, inside a
comfortably large target, carrying the second of the site's two shadows. It reopens the consent
banner, is in the tab order with a name saying what it does, and never overlaps a primary control at
any width. The banner itself presents its three choices at equal visual weight.

**Outbound links.** Carry an external-arrow mark and an accessible suffix saying they open elsewhere,
open without passing the opener, and, when they are partner or funder marks, carry alternative text
naming the organisation rather than the word logo. They dim slightly on hover.

**Sound control.** A persistent control in the header on every route, reachable by keyboard and not
last in the tab order, showing on or off as a shape as well as a colour, with an accessible name
saying what pressing it will do.

### Iconography

Every icon is inline vector drawing in the current text colour, so a theme change recolours it with
no second asset; none is a picture file, a sprite or a font. Directional arrows are filled outlines
with a slight waist in the shaft, never a stroked line with a triangle; down and up arrows are the
right arrow turned. The search mark is two nested chevrons with rounded joins. The menu mark is three
equal bars offset into a slant. Outline marks use one consistent medium stroke. The selection mark
is a filled circle with a light tick. The pull-quote mark is a pair of heavy filled commas. Each
collection has its own small mark drawn on one shared square grid at one weight so the five sit
together without one reading heavier: a building elevation with window bars (Urban), a signpost on a
slope (Nature), a recycling triangle (Repolymer), a flag on a pole (Golf) and a magnifier over a page
(Details). The wordmark is the site name set in the site's sans, preceded by its mark: a rectangle
open on its right side with a diagonal arm folded out of its lower left, and a small registered ring;
the same mark appears alone as a watermark in a light warm neutral. A decorative icon is hidden from
assistive technology; an icon that is a control's only content names the control. No icon carries a
tooltip title. Only the scroll cue, the loading indicator and the play and pause switch animate.

### Motion moments

Each moment below is named in words; its timing is yours within the motion rules.

- **Headline assembly.** Display headlines arrive a word at a time, each word starting a slightly
  different short distance below its place and a fraction after the one before, so the line
  assembles rather than slides. The whole headline stays one string for assistive technology, and
  the split is redone when the window resizes.
- **Entrances.** Blocks rise a short distance while fading in, once, the first time they enter the
  view, on a ladder where headings travel furthest, links a little less and cards least. Sequences of
  blocks (the three workflow steps, the three sustainability assertions) arrive one after another.
- **Media windows.** Photographs are revealed by a window opening from one edge, most often from the
  bottom upward, over an image already at full strength; the photograph itself never fades or scales
  in. On rounded cards the window keeps its rounded corners as it opens. A yellow block wipes in from
  below behind a phrase to emphasise it.
- **Depth.** Inside each window the image is slightly oversized and drifts more slowly than its
  frame as the page scrolls, never far enough to expose an edge. Beneath floating products, the
  ground shadow moves at yet another rate, so objects look lifted off the page.
- **Leaf shadow.** Over some photographs a dappled leaf-shadow overlay, multiplied into the image,
  drifts so slowly and so little, with brightness nudged by a hair, that it reads as light changing
  through trees rather than movement.
- **Scroll cue.** `Scroll to Explore` with a downward arrow that bobs gently, shown only on a route's
  first screen and gone once the visitor scrolls; elsewhere a round yellow-ringed cue with an arrow
  inside.
- **Rotate control.** The round control over the live object arrives with a small overshoot, carries
  a rotate hint mark and a ring that pulses outward from it.
- **Swatch choice.** A chosen swatch swells slightly and settles.
- **Save confirmation.** A thin bar drains across the confirmation over its lifetime; the same
  draining bar marks the revert of a copied reference code.
- **Page transition.** A pale panel wipes across from the left, stops most of the way across and
  waits there while the next page gets ready, then completes and fades away; the header takes the
  new page's theme at the moment the panel is widest, hidden behind it. The leaving page stays pinned
  where the visitor left it rather than jumping to the top under the panel, and the entering page is
  placed at its top before it is revealed. A finer loading bar beneath does the same stalling gesture
  at its own pace and never reaches its end before the page is really ready. On a genuine first load
  only, the site waits for its type to be ready before opening, but never longer than about two
  seconds, and the page ground is already the paper colour so there is no flash; internal and back
  navigations never show that first-load wait. With reduced motion, or if the transition system
  fails, the new page simply replaces the old one.
- **Card filtering.** Cards leaving and arriving on a facet change do so on the entrance ladder,
  staggered by position, and the whole change completes within the default speed however many cards
  moved.

### Scrolling and restoration

The page is a scroll instrument: the catalogue runs well over twenty screens and the home page close
to sixteen. The smooth-scroll layer interpolates wheel input toward its target with a short settle after the
input stops; the native scrollbar is hidden and its width is compensated so nothing shifts. On touch,
scrolling stays native and follows the finger exactly. Four mechanisms exist and are kept distinct:
triggered headline assembly and entrances (which play once and complete), and scroll-scrubbed media
windows and depth (whose progress follows the scroll position). A triggered reveal is never scrubbed,
so nothing plays backwards on the way up. Opening a modal stops the page scrolling without moving it;
the modal's own region keeps scrolling. On a back navigation the previous position is restored after
the content is present and set directly rather than animated; on a forward navigation the new page
starts at the top; an incoming anchor lands clear of the header without animating through the page.
Keyboard scrolling, focus-driven scrolling, find-in-page and anchor jumps all keep working. Scroll
work reads layout once and writes once per frame, and a sustained scroll stays fluid on a mid-range
laptop. Three gestures are never captured by any component: a vertical swipe, a pinch, and the
browser's back gesture at the screen edge.

### Home

In this order, each section optional:

1. **The floating field.** On the page ground, about twenty product renders scattered across the full
   width at varied small scales, each nudged very slightly in brightness and contrast so they do not
   read as copies, drifting a little with the pointer (the smallest least) and, on touch, with the
   scroll instead of the device's tilt. They are decorative and hidden from assistive technology. The
   headline `Spaces for people, made for life.` sits centred over them and assembles word by word.
   `Made to Last` sits at the lower left and `Scroll to Explore` with its bobbing arrow at the lower
   centre. If the renders fail, the headline stands on the empty paper and the route is intact.
2. **The five chapters.** Five full-screen chapters, one per collection, in the order the home
   content sets (independent of the catalogue order): a full-bleed photograph revealed by a window
   opening upward with the inner image drifting, a dark scrim rising from the lower edge, and on it
   the collection pill (mark and name in the collection's accent), the headline in white, and a white
   pill control with the collection mark (`See Urban Products`). Headlines, in order: `Signage, furniture, and equipment for welcoming urban spaces` (Urban); `Signage and equipment for all facets of the great outdoors` (Nature); `Custom projects and furniture crafted out of 100% recyclable plastic` (Repolymer); `Revamp your course with best practices golf equipment and signage` (Golf); `People and environment-friendly custom signage` (Details). The first chapter also
   carries `Urban Catalogue` with a `Download Now` control, which opens the file request; a collection
   with no catalogue shows no download control. Throughout the five, the left margin holds a
   persistent chapter index (`01` to `05`), a thin rule beneath it filling as the visitor moves
   through the sequence, and the standing label `Made to Last`, present at every scroll position. The
   header is in its `light` theme for the whole sequence. A chapter with no photograph sits on the
   page ground filled with its accent, with an ink headline and the `dark` theme.
3. **Manifesto and recent news.** Back on the paper: the label `Verdea` with `Est. 2007`, the
   paragraph `Going beyond the expected is our calling. True sustainability demands creativity to be aligned with strict principles and answer to the highest standards. It keeps us on a journey of innovation, meticulously crafting each project to keep the environment on our side.` assembling at
   display size, and beside it `Recent News` with three article cards (title, date, figure). With no
   articles the strip is absent and the manifesto stays.
4. **Recent additions.** `Recent Additions` with a few product cards identical to the catalogue
   card, including `Explore`, the `Colors` and `Sizes` strips. Absent when there are none.
5. **Leadership.** A portrait, `Joana Ferraz`, `Managing Partner`, the statement `Verdea produces sustainable signage and equipment and offers durable, low maintenance solutions that integrate perfectly into the landscape, based on ecological raw materials.`, the pull-quote mark and the
   quotation `"We think outdoor furniture should look and feel good while doing good for our planet"`
   assembling at display size, and `More on sustainability`. Absent when unset; never a stand-in
   portrait.
6. **Workflow.** The caption `Alvora, Portugal` over its photograph and three blocks arriving in
   turn: `We design` (`Our products are designed to guarantee functionality and viability`), `We build` (`Ensuring the technical and aesthetic aspects stay unaltered`), `We implement` (`Every solution is crafted to endure, with minimal environmental impact`).
7. **Newsletter.**
8. **Closing line.** `Made to last, designed to endure.` at a large display size before the footer.

The chapters are addressable: each carries a stable anchor and an incoming anchor lands on it.

### Catalogue index and collection routes

The header area on the paper carries the collections label `The Collections` where relevant and the
heading `Our products are made to last. Take your time exploring.` assembling word by word, with the
collection name above it as a small category label on a collection route. Below it, the facet
groups: `Filter` `by Collections`, `Filter` `by Products`, and `Sub-filter Urban` (with `Frame`,
`Plaza`, `Reuse`) when Urban alone is active. Chips are pills; selected chips take the ink fill with
a tick; unavailable chips show their count and read as unavailable by a word or a mark as well as by
tone. The counter `Showing <n> of <total> Results` with its downward arrow sits above the grid.

The grid shows four cards across on a wide screen, two on a tablet and one on a phone, with a gap
that never collapses. Each card is a warm tile with softened corners: the title at the top left, the
collection pill at the top right, the render centred on its long soft ground shadow, and along the
bottom the `Colors` strip (a small label, two round swatches, then `+N`) and the `Sizes` strip (a
small label, two pill chips, then `+N`). The bookmark sits in a corner, appearing on hover on devices
that hover and always shown on touch. The card links to the product and says `Explore` where the home
route shows it.

On a collection route, a catalogue card sits in the grid in its own cell after a whole row: `PDF`,
the collection label, and `Download Urban Catalogue` (with the collection's name), styled as a tile
rather than a product.

The floating `FILTER` control is a small pill with the gallery mark and the first of the two
shadows, pinned to the lower centre. It opens the facet panel: a modal on narrow screens and a
popover on wide ones, both closing on Escape and returning focus.

Empty result: the counter at zero, removable chips for each active facet, a clear control, and three
suggested products. A missing render keeps the tile with its title, pills and strips, and fills the
render's reserved box with a flat tone. If the product list fails to arrive in the browser, the
server-rendered first rows stay and a message offers a reload.

Deliberately absent from collection routes: a collection story, a hero photograph and case studies.
A collection route is a working surface for someone assembling a list.

### Product route

A vertical split roughly in halves on wide screens, separated by a full-height hairline; stacked with
the object first below the first turning point.

**Object side.** The object sits centred on the paper ground with its long soft shadow falling to one
side, identical in light to its catalogue render so nothing appears to change when the visitor
arrives from the grid. The live object is a real-time scene: one object per product framed
automatically from its bounds with a fixed margin (a bollard and a picnic table are both framed
correctly without per-product tuning), a ground plane matching the page ground exactly (a viewer
whose background is a slightly different cream is the most visible possible failure), a soft
contact shadow computed once rather than every frame, image-based light from a generated environment
plus one key light that gives metal a readable edge. Dragging orbits the view horizontally, with the
vertical angle held to a narrow band so the object is never seen from directly above or below, and
releasing carries a little momentum that settles. The mouse wheel over the object scrolls the page
and never zooms; a pinch does nothing but the page's own zoom; a swipe scrolls the page unless it
starts clearly sideways on the object. When idle the object turns very slowly, and stops on
interaction and under reduced motion. The object is not focusable by default and carries a text
alternative describing it; where rotation buttons exist they are real buttons usable by keyboard.

Its geometry is quantised and compressed, with the decoder fetched lazily and cached. The loading order is fixed: the still render appears from the document at the object's exact place;
after first paint the renderer starts; decoders and the model arrive only then; one frame renders
off screen; the still cross-fades to the live object; the rotate control arrives with its overshoot.
The live object is never started when the route is out of view, when the device reports little
memory, when rendering would fall back to software, or when the visitor asks for reduced data; a
refusal leaves the still image set, a lost rendering context keeps the last frame or returns to the
still and tries once more after a pause, and a failed model load leaves the stills with no control.
Only one live renderer exists across the whole app, so moving between products never leaks one. The
still image set beside the object is always present, with gallery controls.

**Specification side.** The `PRODUCTS` back pill with the left arrow at the top of the page; the
collection pill in its accent; the title at display size; the small `What is it` label in the column's
gutter beside the description set as a lead paragraph; the compound control (a square bookmark button
at its left, then `REQUEST INFORMATION` filled with ink and paper text, with a visible division); the
row of technical drawings (line elevations with dimension lines, their alternative text describing
the elevation and pointing to the `Dimensions` row); and `Specs` with a downward arrow at the lower
right. The specification block lists labels in a small style beside their values in body style, and
below the phone turning point each label sits above its values. Reference codes are compact marked
elements with a copy control. Below: `In the same Collection` with six cards, the case-study strip
where present, and a full-width installation photograph band where present, revealed by the media
window.

States: no drawings removes the row and the `Dimensions` row carries the information; no description
removes the `What is it` label with its paragraph; a product unpublished while someone reads it
changes nothing on their screen.

### Options modal

The panel heading `Personalise your product`. The size axis is a row of pill chips with the chosen
size's technical drawing in a reserved box beside it, cross-fading on change. Structures are named
swatches; colours and laminate colours are round swatches with their full names as text beside them;
displays are named chips. The chosen value on each axis carries the tick and a shape change, and a
chosen swatch swells slightly. A single-value axis shows its value as chosen and inert. The primary
add control is at the bottom over the panel's fade, focused or one key press away as the panel opens.
In its references mode the heading is `References` and the body is the product's rich text with each
code as a marked element and a copy control.

### Wishlist route

The empty state: the small label `Your wishlist`, the two-line heading `No picks yet? Explore, select, and help make the world greener.`, the ink-filled `Start adding` pill, a full-width hairline,
and three decorative placeholder cards each reading `Your next product` with a faint line drawing of
a product outline on the tile ground, hidden from assistive technology. The populated state: the
label, a heading with the count and an invitation to request a quotation, the primary `Request a quotation` pill, the secondary clear control naming the count, and the list, where each row shows the
render, the title, the collection and the chosen names as a labelled list so two rows of one product
read as visibly different at a glance, with a remove control and, for any unchosen axis, a control to
choose it. Rows marked not available in this language or no longer in the catalogue carry that mark
in words. A list emptied by a successful submission, in this tab or another, shows the empty state with
a line naming the reference.

### Forms

Every control has a visible label associated with it; a placeholder is never the only label, and the
reference's practice of repeating the label as placeholder is only acceptable because the label is
also shown. Required fields say so in their accessible name as well as visually. An error sits under
its field, is tied to it as its description, is announced when it appears, and is marked by the
failure colour together with a mark and words. The privacy checkbox's label contains the `Privacy Policy` link, and following the link never toggles the box. Autocomplete tokens are set: given name,
family name, email, country name, address level 2 for the city, organisation for a company. While
sending, the send control shows progress, every control is unavailable, and an assertive status line
says the message is being sent; further presses are ignored. The success state replaces the form,
takes focus and is announced; the error state keeps every value and announces a message that fits
the cause. Nothing is kept across a page reload except the wishlist itself, which is why the
quotation form shows the wishlist inline above its fields rather than on an earlier step. Measured
wording the site keeps for the newsletter consent is `By submitting your email you agree to our Privacy Policy.`; the reference's single shared status strings (`Message sent successfully.`,
`Something went wrong. Please try again.`, `Please accept the privacy policy.`) are replaced by
wording specific to each condition, and the newsletter never says a subscription is active. Copy
reproduces the reference's punctuation except typographic dashes, which become a comma or a new
clause.

### About route

Ten sections in order, each optional: a seasonal hero whose opening photograph is the same landscape
in four lights (spring, summer, autumn, winter) chosen on the server from the server date with
editorially configured boundaries, falling back to the next configured season and then to the
header's own image, with the title `Rethinking spaces beyond expectations`, `Here's how we do it`, a
video card, and the standing invitation `We're looking for passionate minds to be part of our journey.` with `Work with us`; the positioning statement `The nature of what endures is the only track we follow.` with `Public and private entities partner with us to develop safe communities and responsible spaces.` and a captioned image `Bike Parking Totem`; the origin statement `We want the environment on our side. All our signage and equipment are produced using strictly ecological and durable materials. And everything we design is meant to complement its surroundings.` with a longer
origin paragraph and a video card `Verdea living, made for life.` with `Play Video`; the history,
headed `A trail of hard work and enthusiasm, the perfect ground for craftsmanship.` with the label
`Our history` and a `Drag` affordance, sixteen entries from 2007 to 2026 each a large year and a short
description, alternating above and below a horizontal axis; the process, three blocks `We Design`
(`Rooted thinking`, `Designing solutions requires a great deal of imagination, testing, and problem-solving, especially when sustainability is the priority.`, `Guided by innovation`), `We Build` (`Solutions for life`, `As we turn projects into products, environmental responsibility and longevity remain at the centre of our processes.`, `Focusing on durability`) and `We Implement`
(`Spaces to enjoy`, `We oversee the deployment process from start to finish. We ensure each solution is implemented as designed. We cut no corners.`, `Adding longevity`); the pillars on the yellow
(`fluor` theme), labelled `Take the Verdea stand`, with the statement `When signage, furniture, and equipment don't need replacing, resources are conserved. Timeless designs blend effortlessly with changing surroundings.`, the heading `Creating products that fit right in, require very little to no maintenance, and last several generations, that's what makes us tick.` and four numbered pillars
`01. Environmental Awareness` (`We prioritize using ecological raw materials to create products that minimize environmental impact and support a sustainable future.`), `02. Innovation` (`Our commitment to innovation ensures we develop cutting-edge, eco-friendly solutions that set new standards in design and functionality.`), `03. Quality` (`We uphold the highest standards, ensuring every product is meticulously crafted to provide lasting value and exceed expectations.`) and `04. Durability`
(`Our products are built to last, reducing waste and offering reliable performance over time.`), with
`More on sustainability`; the team, `Verdea's team`, `Meet some of the minds committed to doing good`,
three partners (Joana Ferraz, Miguel Couto, Ines Barata) with portrait, name and role, the statement
`We are a multidisciplinary team of engineers, designers, locksmiths, carpenters, and specialised technicians.` with `68 members` and eight departments `Production` (`Manufactures products, ensuring quality and efficiency.`), `Sales & Marketing` (`Promoting and driving sales through marketing strategies.`), `Finance` (`Management Budgeting, financial planning, and expenses.`),
`Human Resources` (`Hiring, employee relations, and workplace policies.`), `Installation`
(`Assembles and installs products at client locations.`), `Design` (`Creates visual and functional product designs.`), `Project Management` (`Plans and oversees project execution.`) and `System Management` (`IT infrastructure and system functionality.`), and the culture line `Each person has their own type of talent. At Verdea, there is a place for everyone.`; the featured interview in the
`light` theme, whose quotation and profile read without playing the video, and whose video waits
behind an explicit play control and is not preloaded; `Careers in Verdea` with the open positions
(`4 open positions`); and `Never miss an update` with three articles and `More News`. The section
themes are `dark` except the pillars (`fluor`) and the interview (`light`), and the history declares
`dark` on entering and `light` on leaving. A team member with no portrait shows the flat placeholder
tone, never a generic avatar; a history with one entry is a single dated block without the drag
affordance.

The history is a horizontal drag with momentum and a settle on a vertical page. It claims a gesture
only once the gesture is clearly sideways, so a vertical swipe scrolls the page; the wheel over it
scrolls the page; arrow keys move between entries and bring the focused one into view; under reduced
motion the drag follows the pointer exactly with no momentum. Its position is driven by the visitor
alone, never by the page's scroll.

The yearly figures (the founding year, `68 members`, the offices claimed (over fifteen), the
nationalities (almost twenty seven), the share of women in the team (over thirty five per cent) and in
management (over twenty two per cent), and the open positions count) are content fields reviewed annually, never computed, except the
catalogue count.

### Sustainability route

The only route whose header starts in `fluor`, set on the yellow from top to bottom. In order: the
intro, with the headline `Built in Portugal. Made for life.` assembling at display size (the claim of origin is kept
in every locale, never softened), the line `True sustainability demands timeless design as well as enduring materials.`, and three assertions arriving in turn: `We design, build, and implement products that are functional, viable in the long term, and aesthetically pleasing.`, `Built to resist adverse conditions, seasonal changes, constant use, and harsh surroundings.`, `Requiring little to no maintenance, making them both weather and future-proof`. The external quotation `Cities have the ability to offer something for everyone, just because, and only when, they are created by everyone.`
attributed to Jane Jacobs, urbanist and writer, with its source kept in the content. The annotated
product `Bike Parking Totem` with its collection label, name, `View Product`, and its callouts placed
against the image by coordinates from the content yet read in order beside the image, localised with
the route. The materials, the heart of the route, on the deep green ground in the `light` theme:
`Recycled plastic` (`A material made from single-use plastics. Waste that would otherwise end up in landfills is transformed into a durable material for outdoor use.`), `High-pressure laminate` and
`Steel`, each with a large crop of the actual surface texture (at drawing quality, large enough to
see the grain rather than a colour chip), a `CHARACTERISTICS` label and a `LEARN MORE` control
leading to `Recycled Plastic, Explained`, `HPL in the Open Air` and `Why Galvanised Steel Lasts`
respectively, with the partner quotation `"We carefully select our raw materials to ensure the future viability and functionality of our solutions, even when severely exposed to the elements or lacking maintenance."`. The highlighted project `Ecodesign that empowers`, naming `Ridge Viewpoint Boardwalk`
and its location `Alvora, Portugal` as text (no map), with `View project`. The origin story (the
company began on Portugal's hiking trails and placed its first directional signs for natural areas in
2010) with `Get in contact` opening the contact modal, `Our three pillars` with `Sustainable materials` (`Our products are designed to guarantee functionality and viability`), `Integration into spaces` (`Seamlessly integrates into environments, enhancing functionality and visual appeal`) and
`Easy component replacement` (`Quick and simple component swaps for hassle-free maintenance`), the
closing `Designed with intention, to keep the environment on our side.`, and the newsletter. These
three pillars are a different list from the about route's four and are never merged. A material
without a texture keeps its description on the placeholder tone; a material whose article is
unpublished loses its `LEARN MORE`; an unset project or annotated product removes its section with no
orphaned callouts.

### Journal routes

Index: `Journal`, the headline `Exploring ideas, insights, and stories that inspire conversation and shape the future.` assembling; the chips; `Latest Articles` with cards (title, date, figure);
`Featured Verdea case study` with a sideways rail of case-study cards (a large title, the category, a
summary, `Learn More`) that loops with no visible join by repeating its items, with the repeats hidden from
assistive technology, draggable under the same gesture rules as the history and movable with arrow
keys; the per-category blocks (`Sustainability`, `Products`, `Educational` and the others that have
articles), each a heading, up to three cards and `View All`; the closing `Created with purpose, sparking discussion.`; and the newsletter headed `Get the latest updates, straight to your inbox`.
On phones the category blocks become one card with sideways scrolling. Every card, on every journal
surface and in every related strip, is the same card.

Category route: the category name at display size with its description where one exists, the chips
with the current one marked as current, the grid newest first, the paginator with page numbers and
previous and next controls, and the newsletter.

Article: the category, the title assembling word by word, `4min Read` style reading time, the gallery
trigger (three small overlapping thumbnails with slightly softened corners, the `+2` count and `View gallery`), the opening figure revealed by the media window, `Keep Reading` with its arrow, then the
body on a comfortable measure with a label rail beside it (labels above the text on phones), figures
at the measure or full bleed, links marked inline, and the structured credits. The gallery is a
full-screen modal on the dimmed ink backdrop with previous and next controls, arrow keys and swipe,
a `current of total` counter, close by control, Escape or back gesture; it loads only the
neighbouring image ahead. Below the body, up to three further articles in the category and the
products featured in the article, as cards. Articles publish structured metadata naming the headline,
date, author organisation and opening image, and a social preview image; there is no share widget: the address bar is the sharing mechanism, and the structured metadata is the citation.

### Careers and legal routes

Careers: a label, a heading with the count, the list (title, location, employment type in the
locale's words where a mapping exists and as written otherwise, the apply control with its
external-link mark), the standing invitation with a speculative application link, and a link back to
the about route's team section.

Legal pages are deliberately plain in composition: no live object, no sound, no scroll-driven reveal and only the
plain page change, with reduced-motion behaviour as the default. The header shows the title, the
effective date and the version; a sticky left-hand label; the body; the contents list for long
documents; and the version note with a link to the previous version. The cookie policy shows the
declaration of what the site stores under each category and when it was last reviewed.

### Not-found, error and offline pages

The not-found page is designed: a dedicated image (one arrangement for wide screens, another for
narrow), the editable heading and sentence, the search control, the named nearest destination when
one exists, and the three destinations. The error page uses different words and carries the request
identifier and the enquiry address. The offline page carries the wordmark, the message, the enquiry
address, the telephone number and the wishlist count. None of these three carries the live object,
sound or scroll motion.

### Media

Imagery is product information, not decoration. Every image declares its shape before it arrives so
nothing on the page moves as images load; while loading, its box shows a flat tone of the image's own
dominant colour and the image fades in once decoded. There is no shimmer, no skeleton animation and
no blurred preview. Technical drawings keep a higher quality than photographs so no dimension line is
lost. Each image component declares the width it is shown at in each layout, and only a few
renderings are produced per declaration. Autoplaying decorative video is muted, plays inline, loops,
has a poster that fills its frame first, and does not play under reduced motion; feature video waits
for its play control. Alternative text describes a product photograph's object and setting rather than
repeating the adjacent name, describes a technical drawing as an elevation that refers the reader to
the dimensions, and marks decorative renders in the home field as decorative. Documents download with
a readable file name.

### Sound

The site carries a small sound layer that is off by default and opted into, never out of. Its audio graph is initialised on first use, with a master level, a per-source level, stereo panning and low-pass and high-pass filtering, each set instantly or interpolated. Nothing
plays before the visitor interacts, and nothing about sound is loaded until the sound control is
pressed or a stored preference says sound is on, so a muted visitor never downloads anything for it.
The preference is kept in the visitor's browser, survives navigation and reloads, is not a consent
category, and falls back to muted when browser storage is unavailable. Three sounds exist, all
synthesised: a quiet outdoor bed of wind and leaves on the home and sustainability routes that opens
and pans gently as chapters come into view, a short soft cue after a wishlist addition or a form
confirmation renders, and a brief filtered sweep under the page transition. Every sound has a visible
counterpart and conveys nothing on its own. When the window loses focus every sound pauses, and it
resumes on return unless muted meanwhile; the bed continues across page changes without restarting
and cross-fades when it changes between routes; an open modal makes the bed recede slightly; reduced
motion does not affect sound. The overall level stays quiet enough for an office.

### Back office

A quiet working surface in the site's palette and type: a top bar with the signed-in name, role and
sign-out; the enquiry table with kind, status, locale, name, date and, for quotations, the reference,
filterable by kind and status; the enquiry detail with the fields, the quotation lines as a table of
product, collection and each option, the rendered payload in a monospaced block with a copy control,
and the release control on quarantined enquiries; the subscriber table; the product table with a
publish switch per locale for editors and a read-only state for commercial users. For an editor, the
enquiry and subscriber screens show only the counts, with a line saying contents are not available to
the role. Status words carry their meaning in text, not only colour. Every action is reachable by
keyboard and every table header is associated with its cells.

## Constraints

- One organisation, no tenants, no organisation model, no approvals, no delegated or time-bound
  access, and no federated sign-on.
- No prices, no cart, no checkout, no payments, no orders, no invoices.
- No visitor accounts, no visitor sign-in, no password reset, no staff signup.
- No content editing interface, drafts, previews, translation tooling, scheduled publishing or
  revision history; the editor's only write is publish and unpublish.
- No sales platform, recruitment platform, consent vendor, analytics processor, map provider, font
  host or other third-party service; no third-party script in any page; no external network call at
  runtime.
- No inbound webhooks, no bounce processing, no campaign sending, no digest emails, no staff
  escalation messages.
- No privacy access, portability or erasure tooling, no data export, no metrics dashboard and no
  alert routing.
- No job application form, no file upload of any kind.
- No linkable product configuration, no option compatibility rules.
- No native app and no separate dark mode.
- Media is generated; no photograph, model, font file, audio file or document ships as a binary
  asset.
- A newsletter sign-up form lets a visitor subscribe with nothing but an email address.
- The app stays responsive with 229 products per locale and a few hundred articles; the first
  meaningful paint of every route never waits for a script, the live object, sound or motion.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`:
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

**API shapes.** Conventions: requests and responses are JSON unless stated, and times are transmitted as instants in coordinated universal time with an offset. Every write endpoint answers `202`,
never `201`. Every refusal uses one body:
`{"error": {"code": "...", "message": "...", "requestId": "...", "fields": {...}, "retryAfterSeconds": 0}}`,
where `code` is one of `validation_failed`, `invalid_request`, `rate_limited`,
`idempotency_conflict`, `invalid_state`, `not_found`, `unauthorized`, `forbidden` and `unavailable`,
`message` is already in the request's locale, `fields` appears only on `422` and
`retryAfterSeconds` only on `429`. No error body ever contains a stack trace, a query, a host name, a
table name or another service's raw answer. An invalid or unauthorized call is a client error, never
a `5xx` and never a silent success.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `200` `{"status": "ok"}` |
| `GET /api/form-token` | none | `{"formToken": "..."}` |
| `GET /api/products` | `locale`, repeatable `collection`, `productType`, `subCollection` | array of `{id, slug, title, collection: {id, slug, name}, productTypes: [slug], subCollection, colors: [name], sizes: [label], hasOptions, hasDocuments}` |
| `GET /api/products/{slug}` | `locale` | `{id, slug, title, description, collection, productTypes, subCollection, options: {sizes: [{name, label, dimensions}], structures: [{name}], colors: [{name}], displays: [{name}], hplColors: [{name}]}, specifications: [{label, values}], references: [{variant, code}], hasDocuments, alternates: {pt: {slug, url}, ...}, related: [product]}`; unknown or malformed slug `404` |
| `GET /api/collections` | `locale` | array of `{id, slug, name, productCount, subCollections: [{slug, name}], catalogue: {documentName} or null}` |
| `GET /api/categories` | `locale` | array of `{slug, name, articleCount}` in authored order |
| `GET /api/articles` | `locale`, optional `category`, optional `page` | array of at most 12 `{slug, title, date, category: {slug, name}, summary}`, header `X-Total-Count` |
| `GET /api/articles/{slug}` | `locale` | `{slug, title, date, category, readingMinutes, galleryCount, credits: {client, design}, relatedArticles, relatedProducts}` |
| `GET /api/search` | `q`, `locale`, optional `type`, optional `limit` | `{products: [{id, slug, title, collection}], pages: [{kind, slug, title, summary}]}` |
| `GET /api/jobs` | `locale` | array of `{id, title, location, employmentType, lang}` |
| `POST /api/lead/contact` | `{locale, idempotencyKey, contact: {firstName, lastName, email, country}, message, consent: {privacy, textHash}, meta: {route, formToken, website}}` | `202` `{requestId}` |
| `POST /api/lead/quotation` | `{locale, idempotencyKey, contact: {firstName, lastName, email, role, industry, country, city, taxId}, wantsTechnicalFiles, consent: {privacy, textHash}, entries: [{entryId, productId, slug, options: {size, structure, color, display, hplColor}}], meta: {route, formToken, website}}` | `202` `{reference, itemCount}` |
| `POST /api/lead/file-request` | `{locale, idempotencyKey, contact: {firstName, lastName, email}, document: {scope: "product", productId} or {scope: "collection_catalogue", collectionId}, consent: {privacy, textHash}, meta: {route, formToken, website}}` | `202` `{documentName, downloadUrl, expiresAt}` |
| `GET /api/files/{token}` | none | `302` to the signed location, or `404` |
| `POST /api/subscriber` | `{email, locale, consent: {privacy, textHash}, meta: {route, formToken, website}}` | `202` `{"status": "check_inbox"}` |
| `GET /api/subscriber/confirm` | `token` | `303` to `/<locale>/newsletter/confirmed` or `/<locale>/newsletter/expired` |
| `GET /api/subscriber/unsubscribe` | `token` | `303` to `/<locale>/newsletter/unsubscribed` |
| `POST /api/subscriber/unsubscribe` | `{token}` | `204` |
| `POST /api/consent` | `{visitorKey, categories: {necessary, preferences, statistics, marketing}, policyVersion}` | `202` |
| `POST /api/auth/login` | `{email, password}` | `{access_token, role, issued_at, expires_at}` |
| `POST /api/auth/logout` | none | `204`; revocation is immediate |
| `GET /api/office/me` | none | `{email, role, displayName}` |
| `GET /api/office/leads/summary` | none | `{total, byKind, byStatus}` |
| `GET /api/office/leads` | optional `kind`, `status` | array of `{id, kind, status, locale, firstName, lastName, email, reference, createdAt}` (`commercial`) |
| `GET /api/office/leads/{id}` | none | the lead with `message`, `taxId` and, for a quotation, `quotation: {reference, itemCount, payloadRendered, items: [{position, productTitle, productSlug, collectionName, options, unresolved, resolvedFromLocale}]}` (`commercial`) |
| `POST /api/office/leads/{id}/release` | none | the lead, now `received` (`commercial`) |
| `GET /api/office/subscribers/summary` | none | `{pending, confirmed, unsubscribed}` |
| `GET /api/office/subscribers` | none | array of `{email, locale, status, confirmedAt}` (`commercial`) |
| `GET /api/office/products` | `locale` | array of `{id, slug, title, published}` |
| `POST /api/office/products/{id}/unpublish` | `{locale}` | `{id, locale, published: false}` (`editor`) |
| `POST /api/office/products/{id}/publish` | `{locale}` | `{id, locale, published: true}` (`editor`) |

List endpoints return a top-level JSON array. Bearer authentication applies to every `/api/office`
endpoint and to logout; every other endpoint is public.

**No mocks.** Each of these is a contract violation, however good the UI looks: quotations or leads
held in memory or in a file instead of the `postgres` tables; a confirmation, notification or grant
email written to a log, a file or an in-app outbox instead of being sent to `mailpit`; a `delivered`
status set without the staff notification having been accepted by SMTP; a wishlist or quotation
reference invented in the browser and never stored; a download grant checked in the browser; a
catalogue count computed from a hard-coded number. The named services are the fact: the app's pages
can only reflect what lives in `postgres` and what `mailpit` accepted, never substitute for it.

## Definition of done

A specifier can filter the catalogue in any of the four languages, configure a product, save it
beside others in a wishlist that survives a reload, and send the list as a quotation request that is
stored line by line with the names they chose, answered with a quotable reference and confirmed by an
email listing every line; pressing send twice still makes one enquiry. A requested document arrives
at once and by email and cannot be reached without its grant. Enquiry contents stay out of reach of
anyone but the commercial role.
