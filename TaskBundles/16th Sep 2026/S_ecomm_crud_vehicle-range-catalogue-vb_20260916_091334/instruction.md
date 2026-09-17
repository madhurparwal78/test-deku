# Vehicle Range Catalogue

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, read the six model families
on the home route, open one family's overview, narrow ninety two variants down to that family's
twenty two with a single control, tick two of them into a comparison set, and reopen that exact
filtered and ticked view in a fresh window from the address alone, without hitting an error page.

The hard part is the facet counts. Every value in the series facet carries the number of variants
it would yield, all seven are shown at all times, and the six family counts must sum to the count
on `All`. The counts are computed from the stored range, never authored: a count that disagrees
with the list it produces is wrong even when the list is right. A second stranger, signed in as a
different account, must not be able to read or change the first stranger's saved comparisons by
any means, including a direct API call naming the saved comparison by its identifier.

## Overview

Valdris is a car maker, and this is its international marketing and range-browsing site: a
public shop window, not a shop. One long video-led home route carries the whole range as picture
tiles. A second route lists every individual variant of a family with its power, its acceleration
and its top speed, and lets a visitor narrow that list by four facets and tick variants into a
comparison set. A market and language selector and three legal routes complete the site.

Two visitors read the same pages. One already knows which family they want and has come to find
the right version of it; they go straight to the model overview and filter. The other is browsing
the marque and does not yet know that the families differ by body, seats and drive; they scroll
the home route until a tile stops them. The site is arranged so that either can leave with an
opinion without reading all of it.

The product deliberately does not sell anything. There is no cart, no price, no configurator, no
stock search and no checkout anywhere in it. The one thing a visitor can accumulate is a
comparison set, and the one thing an account adds is the ability to save that set under a name and
come back to it. Everything else is reading.

The genuinely hard part is that the facet counts are derived rather than stored: each count is
computed against the other facets but not against the facet it is displayed in, which is exactly
why the seven series counts sum to the total rather than to something smaller.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Anonymous visitor | Read every route: the home route, the model overview for any family, the market and language selector, and the three legal routes. Narrow the overview by any facet, reset the facets, tick and untick variants into a comparison set, and share the resulting address. Accept or reject non-essential storage, and dismiss the local-market prompt. Pause the hero film. | **Cannot save a comparison set under a name. Cannot read, rename or delete any saved comparison, their own or anybody else's, because they have none. Cannot create, edit or retire any family, variant, market or promotion** |
| `owner` | Everything an anonymous visitor can, plus sign in, save the current comparison set under a name, read the list of their own saved comparisons, open one to restore its variants and facets, rename it, and delete it. | **Cannot read, open, rename or delete another owner's saved comparison, by any route or by any direct request naming its identifier. Cannot learn from any refusal whether another owner's saved comparison exists. Cannot create, edit or retire any family, variant, market or promotion: the range is reference data and no role in this product writes it** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from an anonymous session to any saved-comparison endpoint,
or from an `owner` session naming another owner's saved comparison, must be rejected by the server
(an unauthorized request is denied, not served), leaving the protected state unchanged.

A refusal to read another owner's saved comparison and a refusal for one that does not exist are
indistinguishable from the outside. Neither the body, nor the shape of the response, nor its
timing may reveal which of the two happened.

Signup is open. Anyone may create an `owner` account from the public sign-up form, and that is the
only way an account comes into being. The owner a saved comparison belongs to is read from the
session, never from the request body.

Two accounts are seeded, both with the password `deku-demo-pw-2026`: `owner@example.com` and
`owner2@example.com`. Each owns one saved comparison at first start, and the two are the isolation
boundary this product is measured against.

## Core features

### The range, and what drives every route

Six model families carry the whole site, and ninety two variants sit under them. Both the home
route and the model overview read the same stored range; neither holds a copy of it.

1. The six families are `900`, `700`, `Volten`, `Cardinal`, `Terra` and `Sierran`.
2. Each family carries a body description line, a set of powertrain availability values, an
   availability state, and two separate orderings: a house order for the home range grid and a
   different house order for the series facet list. Both orderings are stored per family and both
   are used. They are not the same order and neither is alphabetical; a build that sorts either
   one is wrong.
3. The home range grid renders the families in the home order: `900`, `700`, `Volten`, `Cardinal`,
   `Terra`, `Sierran`.
4. The series facet renders them in the facet order, under a leading `All` row: `All`, `700`,
   `900`, `Volten`, `Cardinal`, `Terra`, `Sierran`.
5. A family whose availability state is unavailable cannot be ordered. It carries a single wide
   chip reading `Model currently unavailable for order.` in place of its powertrain chips, and it
   carries no arrow control on its tile. `700` is seeded in that state.

### The model overview and its facets

The model overview is one route, not one per family. The family in the path pre-applies the series
facet; the page lists the range and the rail narrows it.

1. Four facets narrow the list: `Model series`, `Body Design`, `Seats` and `Drive`.
2. `Model series` is single-select and defaults to `All`. It is always expanded and is presented
   as a radio list, one row per family plus `All`.
3. `Body Design`, `Seats` and `Drive` are multi-select and default to empty. Each is a collapsed
   group that expands to a list built like the series list.
4. Values within one facet combine as alternatives. Separate facets combine as requirements. So
   two body designs widen the result and a body design plus a drive narrows it.
5. Every facet value carries the count of variants it would yield, in parentheses, shown at all
   times and not only when selected.
6. **A count is computed against the other facets but not against the facet it is displayed in.**
   This is the rule the whole route rests on. It is why the seven series counts sum to the count
   on `All` rather than to a smaller number, and it must hold for the other three facets too.
7. The seeded series counts are `All (92)`, `700 (10)`, `900 (22)`, `Volten (22)`,
   `Cardinal (9)`, `Terra (5)` and `Sierran (24)`. The six family counts sum to ninety two.
8. Selecting a family reduces the result list and updates every other facet's counts. The series
   counts themselves do not change, by rule 6.
9. Counts are derived from the stored range on every request. A count written into the range data
   as a field is wrong even when its value happens to be right.
10. There is no sort control anywhere on the route, and none may be added. Ordering within a group
    is the stored house order of the variants, never by any statistic.
11. An empty result is a valid response, not an error.

### Result grouping

1. Results are never one flat list. They are gathered into groups by body style, each group
   introduced by a heading naming the body.
2. The two seeded groups for the `900` family are headed `900 Corsa Model variants` and
   `900 Corsa Cabriolet Model variants`.
3. Groups follow one another down the page with the heading at the head of each group.
4. A group with no matching variants under the current facets is absent entirely, rather than
   present and empty.

### The variant card

Every variant in the result list renders as a card carrying, in this order: a cutout image of the
car in profile overhanging the top edge, the variant name, a chip row, three statistics, the
consumption paragraph, a technical-data link, two actions, and a compare checkbox.

1. The chip row carries the model year `2027` in a filled dark chip, then two to three quieter
   chips for powertrain, drive and transmission.
2. The three statistics are always the same three and always in this order: acceleration, power,
   top speed. Each renders as a value above its label.
3. The statistic label is stored per variant, not fixed per statistic, because the measured labels
   differ between variants. A variant whose acceleration figure assumes an optional package says
   so in its own label.
4. The six seeded variants of the `900` family carry these figures exactly:

| Variant | Chips | Acceleration | Power | Top speed |
|---|---|---|---|---|
| `Corsa` | `Gasoline`, `Rear-Wheel Drive`, `Automatic` | `3.9 s` | `290 kW / 394 PS` | `294 km/h` |
| `Corsa T` | `Gasoline`, `Rear-Wheel Drive`, `Manual` | `4.5 s` | `290 kW / 394 PS` | `295 km/h` |
| `Corsa S` | `Gasoline`, `Rear-Wheel Drive`, `Automatic` | `3.3 s` | `353 kW / 480 PS` | `308 km/h` |
| `Corsa 4S` | `Gasoline`, `All-Wheel Drive`, `Automatic` | `3.3 s` | `353 kW / 480 PS` | `308 km/h` |
| `Corsa GTS` | `Gasoline`, `Rear-Wheel Drive`, `Automatic` | `3.0 s` | `398 kW / 541 PS` | `312 km/h` |
| `Corsa 4 GTS` | `Gasoline`, `All-Wheel Drive`, `Automatic` | `3.0 s` | `398 kW / 541 PS` | `312 km/h` |

5. The acceleration label is `Acceleration 0 - 100 km/h with Sport Chrono Package` on every one of
   those six except `Corsa T`, which carries `Acceleration 0 - 100 km/h`.
6. The power label is `Power (kW) / Power (PS)` on `Corsa`, `Corsa T`, `Corsa S` and `Corsa 4S`,
   and `Power combined (kW) / Power combined (PS)` on `Corsa GTS` and `Corsa 4 GTS`.
7. The top-speed label is `Top speed` on all six.
8. Each variant carries its own consumption statement, rendered with the prefix
   `Fuel consumption combined (model range):` and the clause
   `CO2-emissions combined (model range):`. The six seeded statements are:

| Variant | Consumption | Emissions |
|---|---|---|
| `Corsa` | `10.4 - 9.9 l/100 km` | `237 - 227 g/km` |
| `Corsa T` | `10.9 - 10.4 l/100 km` | `248 - 237 g/km` |
| `Corsa S` | `10.6 - 10.1 l/100 km` | `242 - 230 g/km` |
| `Corsa 4S` | `11.0 - 10.4 l/100 km` | `249 - 237 g/km` |
| `Corsa GTS` | `10.6 - 10.1 l/100 km` | `242 - 230 g/km` |
| `Corsa 4 GTS` | `10.8 - 10.3 l/100 km` | `246 - 234 g/km` |

9. A variant belonging to a family that cannot be ordered carries the unavailable chip and no
   `Configure` action.

### The comparison set

The compare checkbox at the foot of each card is the one control that accumulates state across
cards, and it is the heart of the route.

1. Ticking a card adds that variant to the comparison set; unticking removes it.
2. **The set survives a facet change.** A variant that is ticked and then filtered out of view
   stays in the set, and is still ticked when a facet change brings it back into view. This is the
   rule most easily got wrong: the set belongs to the route, not to the rendered list.
3. The set is capped at four variants. The cap is stated in the interface. When the cap is
   reached, the unticked checkboxes are disabled rather than hidden, so a visitor can see why
   another cannot be ticked.
4. The set is carried in the query string alongside the facets, so a narrowed and ticked view can
   be linked. Opening that address in a fresh window with no prior session shows the same narrowed
   list with the same variants ticked.
5. A change to the set is announced to assistive technology, not only shown.
6. Resetting the facets does not clear the comparison set.

### Saving a comparison

Signed-in owners may keep a comparison set rather than only linking it.

1. A signed-in owner saves the current comparison set from its own route, giving it a name. The
   route is reached from the overview and has its own address.
2. A saved comparison stores the variants in the set and the facets in force when it was saved.
   Opening it restores both, and the restored view matches what was on screen when it was saved,
   after a reload and in a fresh session.
3. A name is required, is trimmed of surrounding whitespace, and must be at most eighty
   characters. An empty or whitespace-only name is rejected inline, naming the field, and nothing
   is written.
4. A name is unique per owner. Saving a second comparison under a name an owner already holds is
   rejected and nothing is written; two different owners may each hold the same name.
5. An owner may rename and delete their own saved comparisons.
6. Saving with an empty comparison set is rejected: there is nothing to save.
7. A saved comparison is readable, renameable and deletable only by the owner that created it.
   Any request naming another owner's saved comparison is denied and the stored row is unchanged.
8. Confirmation of a save, a rename or a delete arrives as a transient message that does not
   replace the page, and the saved-comparison list reflects the change without a reload.
9. Saving is idempotent in the sense that matters: submitting the same save twice produces one
   saved comparison, never two.

### The home route

One long scrolling route in five bands, in this order: the hero, the highlight row, the range
headline, the model range grid, and the discover row, followed by the footer.

1. The hero fills the viewport and plays a silent film of a car behind everything. The film plays
   inline, muted, and without the visitor asking for it.
2. **The hero headline and its call to action must be readable before any video byte is
   requested.** The poster image is the only image on the route that loads eagerly, and the film
   is requested only after the poster has painted.
3. The route is complete and usable if the film never plays at all. Blocking the video entirely
   leaves the hero readable, the headline present and every control working, with the poster in
   place of the film.
4. A single round control at the lower right of the hero pauses and resumes playback. It is
   reachable from the keyboard, and its state is announced rather than carried by its shape alone.
5. A visitor whose system asks for reduced motion gets the poster and no playback at all.
6. The range grid holds the six family tiles, two across on a wide screen and one on a narrow one.
   The whole tile is a single link to that family's model overview.
7. Each tile carries the family signature at its head, a row of one to three availability chips,
   a one-line body description, and a round arrow control at its foot. The six seeded tiles carry
   these chips and descriptions exactly:

| Family | Chips | Description |
|---|---|---|
| `900` | `Gasoline` | `Iconic sports car with rear engine: 2 doors, 2+2 seats.` |
| `700` | `Model currently unavailable for order.` | `Precise mid-engine sports car: 2 doors, 2 seats.` |
| `Volten` | `Electric` | `Electric sports car: 4 doors, 4/5 seats.` |
| `Cardinal` | `Hybrid`, `Gasoline` | `Luxury sedan with a high level of comfort: 4 doors, 4/5 seats.` |
| `Terra` | `Electric` | `Sporty compact SUV: 4 doors, 5 seats.` |
| `Sierran` | `Electric`, `Hybrid`, `Gasoline` | `Versatile SUV: 4 doors, up to 5 seats.` |

8. The `700` tile is the unavailable state: one wide chip instead of powertrain chips, and no
   arrow control, because there is nowhere for it to go.
9. The highlight row and the discover row are three promoted cards each, and they are the same
   component with different data.

### The market and language selector

1. One route, served outside the locale segment, because it is the one route that cannot assume a
   market.
2. It carries the heading `Select your market or region`, then seven region groups: `Africa`,
   `Asia`, `Australia/Oceania`, `Europe`, `Latin America`, `Middle East` and `North America`.
3. Each market entry names the market and the languages it is available in, and links to the home
   route under that locale.
4. The seven groups are rendered from a region key stored on each market record. The groups are
   not hard-coded, and adding a market with an existing region key places it in that group with no
   other change.
5. The route is reachable from the globe control in the header on every route and from the
   `Change` link in the footer, and both carry the current locale so the selector can mark the
   current market.

### Non-essential storage, and the market prompt

1. A first-time visitor is asked once about non-essential storage, in a centred panel over a
   dimmed page, carrying a short heading, one paragraph naming the categories of storage in use, a
   link to the cookie policy route, and two controls: `Accept all` and `Only necessary cookies`.
2. The answer persists. The panel does not return on a later visit or after a reload, whichever
   control was used.
3. A separate, smaller prompt offers to move the visitor to their local market, with one control
   to go, one to stay, and a round dismiss control. It is dismissible independently of the storage
   panel and also does not return once dismissed.
4. Both panels hold keyboard focus while open, return focus to what opened them when they close,
   and close on the escape key.
5. Until they are dealt with, neither panel may be bypassed by scrolling the page behind it.

### The legal routes

1. Three legal routes ship: a legal notice, a privacy policy and a cookie policy. Each is
   reachable from the legal link row in the footer of every route.
2. The privacy policy states plainly what the product stores about a visitor, covering scope,
   the controller, the categories of personal data, the purposes, the recipients, where processing
   happens, how long data is kept, and how to make contact.
3. The legal notice is the shortest of the three. It carries a provider block naming
   `Valdris Motoren AG`, its registered postal address `Werkstrasse 1, 70000 Rheinstadt`, its
   published contact address `info@example-origin` and its published telephone number
   `(+00) 0000 000-0`; its executive board as a list of six named members, beginning
   `A. Halvorsen`; its registry court `District Court Rheinstadt`, its commercial register number
   `HRB no. 000000` and its VAT identification number `VAT ID No. XX 000 000 000`; a consumer
   dispute-resolution statement; and a copyright statement covering text, images, graphics,
   animation, video and audio.
4. The cookie policy covers scope, controllers, categories of personal data, categories of storage
   technologies, where processing happens, and consent and objection. It additionally embeds the
   live storage settings panel under its own heading, and that panel is the same one the
   first-visit dialog opens, which is why the dialog links to this route.
5. Each legal route carries an in-page contents list at the top, above the first heading, linking
   to each numbered heading in the document body.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/:locale` | The home route: hero film, highlight row, range headline, range grid, discover row | Public |
| `/:locale/models/:family` | The model overview: filter rail, grouped variant cards, comparison set | Public |
| `/countries` | The market and language selector, outside the locale segment | Public |
| `/:locale/legal-notice` | Provider and copyright statement | Public |
| `/:locale/privacy` | Privacy statement | Public |
| `/:locale/cookie-policy` | Cookie statement, with the live settings panel | Public |
| `/:locale/sign-up` | Create an `owner` account | Public |
| `/:locale/sign-in` | Sign in | Public |
| `/:locale/comparisons` | The signed-in owner's saved comparisons | `owner` |
| `/:locale/comparisons/new` | Save the current comparison set under a name | `owner` |
| `/:locale/comparisons/:id` | Open, rename or delete one saved comparison | `owner`, and only its own |

`:locale` is a single segment naming a market and a language. The seeded default is
`international-en`, and it is one value among many rather than a hard-coded default.

### Entry and redirects

- An anonymous request for `/:locale/comparisons`, `/:locale/comparisons/new` or any
  `/:locale/comparisons/:id` is redirected to `/:locale/sign-in`, and after a successful sign-in
  the visitor lands on the route they originally asked for, not on the home route.
- Signing out returns the visitor to the home route for the current locale, and the saved
  comparisons become unreachable again.
- A session that has expired mid-action is treated as anonymous: the action is refused, nothing is
  written, and the visitor is sent to sign in with the route they were on preserved.
- An `owner` asking for another owner's saved comparison is refused exactly as though it did not
  exist, and is not redirected to sign in, because they are already signed in.
- An unknown address under any locale renders the product's own not-found page, carrying a way
  back to the home route, and answers not found rather than rendering an empty layout.
- A route carrying an unknown facet key in its query string ignores that key and renders normally,
  rather than failing.

### Journeys

1. **Narrow the range.** Open `/international-en`, scroll past the hero to the range grid, and
   read the six family tiles. Follow the `Sierran` tile. The overview opens with the series facet
   already set to `Sierran`, the result list showing that family's twenty four variants grouped by
   body style, and the series rows still reading `All (92)`, `700 (10)`, `900 (22)`,
   `Volten (22)`, `Cardinal (9)`, `Terra (5)` and `Sierran (24)`.
2. **Filter and compare.** From the overview, select `900` in the series facet. The result list
   becomes the twenty two `900` variants, grouped under `900 Corsa Model variants` and
   `900 Corsa Cabriolet Model variants`. Tick `Corsa GTS` and `Corsa 4 GTS`. Copy the address,
   open it in a fresh window with no prior session, and see the same two variants ticked in the
   same filtered list.
3. **The set survives a filter.** With `Corsa GTS` ticked, change the series facet to `Terra`. The
   card disappears from view. Change it back to `900`. `Corsa GTS` is still ticked.
4. **Filter to nothing.** Combine facets until no variant matches. The result region states that
   no variant matches the current filters and shows the reset control inside the result region
   rather than only in the rail. Using it returns every facet to its default, empties the facet
   part of the query string, and returns the counts to their unfiltered values, leaving the
   comparison set untouched.
5. **Save a comparison.** Sign in as `owner@example.com` with the password `deku-demo-pw-2026`.
   With two variants ticked, open the save route, enter the name `Weekend coupes`, and save. A
   transient confirmation appears, and the saved comparison is listed at `/:locale/comparisons`
   without a reload. Reload the page: it is still there, still carrying both variants and the
   facets in force when it was saved.
6. **Isolation.** Signed in as `owner2@example.com`, ask for the saved comparison that
   `owner@example.com` owns, by its identifier and by a direct API call. The request is denied,
   the response says nothing about whether it exists, and the stored row is unchanged.
7. **Choose a market.** From any route, open the globe control in the header. The selector lists
   every market under its seven region headings. Picking one opens the home route under that
   locale.
8. **First visit.** Open the home route with no stored answer. The storage panel is present over a
   dimmed page. Choose `Only necessary cookies`. It closes, focus returns to where it was, and it
   does not return after a reload. Dismiss the local-market prompt separately; it also does not
   return.

### States

- Every list has an empty state. The overview result region states that no variant matches and
  promotes the reset control; the saved-comparison list tells an owner they have saved none yet
  and points at the overview.
- Every route has a loading state while its data arrives, and the hero shows its poster rather
  than an empty rectangle.
- A failed request states what failed in the interface and leaves the page usable. Nothing throws
  a blank page.
- A form that rejects input says so inline, names the field at fault, keeps what was typed, and
  writes nothing.

## UI/UX notes

**North star.** Somebody arriving here should understand within one screen that this is a maker of
fast, expensive cars that takes itself seriously, and should be able to reach a specific version of
a specific family, with its real figures in front of them, in two steps from the top of the home
route.

**Register.** This is a premium product site in the editorial register. The subject of every
screen is a photograph or a film of a car and it is the first thing seen: the imagery is full-bleed
or close to it, the type sits on top of it, and the chrome is thin enough to disappear against it.
Because a visitor must be able to compare, the six family tiles and every variant card are built as
repeating units that differ only in content, so they are read at a glance rather than one at a
time. Because the interface must convey confidence, it holds still once content has arrived.

Two stances, and a maker selling breadth could rationally invert both. **One subject per screen
over a page of offers**: a competitor would fill the same space with finance rates and a stock
search, and this product gives six tiles a great deal of room each. **Figures over adjectives**:
the numbers that decide a choice are on the second route, stated plainly, rather than replaced with
praise on the first.

**Theme.** Every colour is declared once as a light and dark pair, and a band of the page chooses
which half applies by declaring its scheme rather than by restating colours. This is the mechanism
the whole look rests on, and it is what lets a dark band sit inside a light page without a single
colour being repeated. Commit to both schemes and design both fully; neither is an afterthought.

**Palette by role.** The page ground is a near-white neutral in the light scheme and a near-black
neutral in the dark one, and that near-black carries a trace of blue rather than being a true
black: it is the colour of a night sky just after the last light goes, and rounding it to a pure
value drains the temperature out of every dark band on the site. The near-white used for text on
dark leans the same way. Body text and headings take the primary neutral against the ground, and
nothing quieter. Cards, rails and inset panels sit on a light neutral surface in the light scheme
and a deep neutral one in the dark scheme. Quieter labels are the primary colour carried at a
reduced strength rather than a separate grey chosen to look right against white, because the same
token has to survive the scheme flip.

Four colours carry meaning and appear nowhere else: one vivid blue for something informational, one
green for something that worked, one vivid orange for something still in progress, and one vivid
red for something gone wrong. The success colour is the one that shifts most between the schemes,
reading as a deep, soft green on the near-white ground and as a mid, vivid teal on the near-black
one, and it is still the same token rather than two. A state that is none of the four may not
borrow any of them. The focus ring is a single vivid blue that is identical in both schemes, and that is
deliberate: one ring has to work against the near-white ground and the near-black one alike. A
greyscale ramp exists for exactly one purpose, the family signature transition described below,
and it is not a general-purpose grey scale. The exact values are yours, so long as they hold the
roles and the exclusivity above.

**What it must not look like.** No page dominated by a single hue family with no second signal. No
decoration standing in for content. No marketing composition where the working interface belongs,
and nothing borrowed from a template unrelated to cars. The cards must not be separated from the
ground by drop shadows: exactly one shadow exists in the whole build, on a single floating
control, and the cards are held apart by their corner softness and by their scheme instead. Adding
shadows to make the cards read is a different design.

**Type.** The typography is one family in three weights, `400`, `600` and `700`. The family is a narrow humanist
grotesque with a tall x-height and lining figures, because the three statistics on a variant card
are set beside each other and their figures must align in a column. Name a freely licensed family
and load it from a package rather than shipping a file; a narrow grotesque stands in while it
loads, chosen close in width so a headline does not visibly reflow when the real face arrives.

The three smallest sizes are fixed: body is `16px` over `24px` and carries the site, secondary
labels are `14px`, and legal and consumption text is `12px`. Every size above them is fluid,
computed from the viewport width and clamped at both ends rather than stepping between fixed
values. At a wide desktop width the rendered sizes are `72.512px` for the hero headline,
`56.402px` down to `44.979px` for a section headline, `43.104px` for a route headline, `36.084px`
and `34.922px` for a group headline, `30.519px` for a card headline, `25.904px` and `23.609px` for
a statistic value, and `20.304px`, `19.359px` and `18.099px` for a card title. Line height rises
with size in a fixed band, roughly one and a half times the size at body size and falling toward
one and a fifth at the largest headline. **Headlines are set at the normal weight, never bold**,
which is what keeps a very large word reading calm rather than shouted; the bold weight is
reserved for the wordmark and for defined terms inside legal prose.

**Shape, spacing and density.** The corner radius ladder has five rungs and they are a ladder
rather than a set of values: controls and inline links are barely softened, promoted cards and
floating link buttons a little more, the body-type flyout panel more again, the six range tiles the
most of anything on the site, and chips and round icon buttons carry a pill radius that keeps their
ends circular whatever their width. Inline anchors inside prose take the smallest hairline
softening of all. Express each rung once as a token and do not repeat the value. Every declared
border on the site is a single hairline, one weight, no exceptions.

Density is comfortable rather than tight, and the spacing is what carries it: the range grid and
the overview results run to the page gutter rather than to a container, while legal prose is held
to a narrow measure because long text is only readable in a narrow column. Containers come in three
widths, narrow for prose, medium, and wide for everything that is not full-bleed. The gap between
bands is several times the gap beneath a heading and roughly halves on a narrow screen, and every
gap is a multiple of one base unit which is yours to choose.

**Motion.** Four durations and three easing curves are declared once and used everywhere, which is
what makes unrelated parts of the page feel made by one hand. The four durations are a quick one
for a small change, two middle ones, and one appreciably longer one reserved for the opening
headline. Of the three curves, one is the site curve and carries an order of magnitude more of the
work than the other two combined: anything without a stated reason to differ uses it at the quick
duration. The second is a decelerating curve, entering fast and settling slowly, for content
arriving. The third is symmetric, even at both ends, for a change that is neither an entrance nor
an exit. Name them by the shape they have rather than by the moment they were first used for.

The character is **eased**: things leave and arrive on a considered curve rather than snapping or
overshooting. Nothing springs, nothing bounces, and nothing uses a different duration to feel
special.

Content arrives rather than appearing. A headline fades in while rising; a tile does the same over
a shorter distance; a small control over a shorter distance again. **The travel distance encodes
importance**, so larger things travel further and read as heavier, and on a narrow screen every
travel distance roughly halves, because the same distance on a short screen reads as a much larger
move. The range tiles are an exception worth building deliberately: they begin faintly visible
rather than fully transparent, so they feel like they were always on the page and the visitor
simply had not reached them yet.

**Every reveal plays once and holds.** Nothing replays when a visitor scrolls back to it. Within a
group, each item waits a fixed step longer than the one before, indexed by its position and capped
after a handful of steps, which is what makes a row of three read as dealt out rather than dropped
as a block. The range grid reveals per tile, not per row. If a visitor scrolls past a group before
it has finished, the reveal is cancelled rather than queued and the group is simply already in its
final state when they come back.

**Nothing on this site is scrubbed against scroll position.** No effect plays forward as the page
scrolls down and rewinds as it scrolls up, no progress value tracks the scroll offset, and there is
no timeline to scrub. What looks continuous is a set of one-shot reveals triggered as elements
enter, plus the band change below, plus a film playing at its own rate underneath. Building a
scroll-linked timeline here is wrong even if it looks similar, and it is also the thing most likely
to go jerky on a slow machine.

**The band change is the signature motion of the home route**, and it is not a movement. As the
range grid scrolls, whole bands of the page change scheme, and they do it as a timed colour
transition rather than as a swap: the text colour, the background, the borders and the outlines all
change on one clock, so the words never arrive before the ground they sit on. It reads as a light
being dimmed in a room rather than as parts being repainted one after another.

The family signature on each tile cannot cross-fade the same way, because it is a shape filled
through a single property rather than text. It steps instead through a ramp of greys from white to
black, and back the other way, so it stays legible against whatever the band has become. Reproduce
the ramp rather than interpolating between two ends: a straight two-stop blend passes through a
different set of greys and reads as a dimmer rather than as a change of ink.

**One element loops, and only one**: a small arrow under the hero drifting down its axis and back
to say there is more below. Everything else in the build plays once.

**Hover and focus.** Every interactive element transitions its background on the site curve at the
quick speed. Round icon buttons raise the strength of their frosted fill when pointed at; they do
not scale and they do not move. The whole range tile is the link, so its hover state is carried by
the tile rather than by the control inside it. Inline anchors in prose are underlined at rest, not
on hover. Hover effects are suppressed entirely where the pointer is coarse, so a touch visitor
never gets a state they cannot leave.

**Accessibility, and these are floors rather than preferences.** Body text meets WCAG AA contrast
against its ground in both schemes, and it uses the primary token rather than anything quieter to
get there. Chip labels sit over photography behind a frosted blur, and the blur is what makes them
legible: a build that drops the blur must add a solid fill instead, never lower the text contrast.
Touch targets are comfortably sized. Full keyboard navigation reaches every interactive element in
document order with a visible focus ring on all of them, and icon-only controls carry text labels
for assistive technology. Meaning is never carried by colour alone.

Each range tile is one tab stop and not two: the arrow control inside it is decorative and is out
of the tab order, so tabbing through the six families takes six presses rather than twelve. The
compare controls are real checkboxes and work with the space key. The facet groups are expandable
regions whose expanded state is exposed, and their chevron turns on the same clock as everything
else. One main region and one page heading per route, with heading order descending without gaps.
The header, the main region and the footer are landmarks on every route, and the filter rail is a
complementary region on the overview. The three statistics on a variant card are marked up as a
description list, a term and its value per statistic, so a screen reader says the label with the
figure rather than reading two loose numbers. Every content image carries a description naming the
family and the setting, and the decorative scrims and gradients carry none.

**Reduced motion completes the page, it does not empty it.** A visitor who has asked their system
to reduce motion gets every reveal's end state applied immediately, the looping arrow still, the
film unplayed and the poster in its place. The page must be complete, static and readable in that
state, never half-arrived.

**Responsive.** Six width tiers, and one of them does nearly all the work: at about a tablet width
everything that was a single column becomes two or three. Below it the six range tiles stack, the
two rows of three become three stacked cards each, the filter rail folds away behind a sticky
`Filter` button, the three statistics on a variant card stack one above another and its two actions
run full width, and the footer columns stack. A tablet is treated as its own case rather than as a
small desktop. The layout holds at every width between the named tiers, nothing overflows sideways
at a narrow viewport, and every navigation target stays reachable there. The exact breakpoint
widths are yours, so long as the tablet tier carries the major change and the arrangement above
holds.

## Technical requirements

The frontend is Angular, built with Vite and served as a production build. The backend is Flask,
serving a JSON API on the same origin under the `/api` prefix. The rendering model is a
single-page application against that JSON API: the browser receives an application shell on first
paint and every route's content arrives as JSON, so the server renders no page markup. Storage is
PostgreSQL, reached at `DATABASE_URL`, which is read from the environment and never hardcoded.
Authentication is app-implemented email and password with bearer tokens; there is no external
identity provider. `GET /api/health` returns `200` once the app is ready. Application logs go to
standard output as one line per request.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor. The only backing service
available in this environment is PostgreSQL, and reaching for anything else is a contract
violation.

PostgreSQL is already running and reachable at `DATABASE_URL`. Do not download, install, compile
or start a copy of it.

**The typeface.** Name a freely licensed narrow humanist grotesque available at weights `400`,
`600` and `700` with lining figures, and load it from a package rather than committing a font
file. Two faces are loaded before first paint, the normal weight and one heavier; the third is
loaded only if a route uses it. Every face loads with swap behaviour, and both preloaded faces are
preloaded. The fallback stack is not decoration: it is what renders during the swap, and its first
fallback is a narrow grotesque chosen close in width to the real face so headlines do not reflow
when it arrives.

**Performance budgets, as requirements.** Script delivered before the hero is interactive stays
under 150 kilobytes compressed. Stylesheet delivered before first paint stays under 40 kilobytes
compressed. Two font files load before first paint. One image loads before first paint, the hero
poster. **Zero video bytes are requested before the headline is readable**, which is the budget the
others serve.

**Media strategy.** The hero poster is the only image that loads eagerly anywhere in the product;
every other image on every route loads as it approaches the viewport, and the six range tiles are
below the fold on every width so none of them may load eagerly. Images are served in a modern
format with a fallback, at the two densities the layout needs and no more. The film is requested
only after the poster has painted, never on a connection the browser reports as constrained, and
never when reduced motion has been asked for. The variant cutouts on the overview are the heaviest
content on that route and load per group as each group approaches. Never preload the film, at any
priority.

**Security headers.** Every response carries the standard security headers, including a strict
transport policy and a content-type policy that refuses to sniff, and they are present on document
responses and API responses alike.

**Discoverability.** A sitemap lists every public route in the product, and a robots file points at
the sitemap. Both are served from the site root and both stay correct as routes are added.

**No credential, API key, token or database URL may appear in anything the browser downloads.**

## Data model

Eight tables. Four of them are the entities that carry the whole site, families, variants, markets
and promotions, and everything else on it is copy. All timestamps are UTC.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
> not a secret. Hash it as normal; the exact literal must work at login, and it must be written
> into `/app/USER_README.md` alongside each account so a grader can sign in.

**`families`** - the six model families. Fields: `id`, `key` (unique, kebab-case), `display_name`,
`home_order` (integer, unique), `facet_order` (integer, unique), `body_description`,
`powertrains` (the set of availability values carried as chips), `availability_state` (one of
`orderable` and `unavailable`), `tile_media_ref`, `signature_ref`. `home_order` and `facet_order`
are two independent orderings and both are stored; neither is derived from the other.

**`variants`** - the ninety two. Fields: `id`, `key` (unique), `display_name`, `family_id`
(references `families`), `body_style` (the value results are grouped by), `model_year`,
`powertrain`, `drive`, `transmission`, `house_order` (integer, the order within a group),
`availability_state`, `cutout_media_ref`, and the consumption statement as `consumption_combined`
and `emissions_combined`. The three statistics are stored as three pairs, each a value and its own
label: `acceleration_value` with `acceleration_label`, `power_value` with `power_label`, and
`top_speed_value` with `top_speed_label`. **The label is a field on the variant, not a constant**,
because the measured labels differ between variants of one family.

**`markets`** - one row per market in the selector. Fields: `id`, `display_name`, `locale_segment`
(unique), `region_key` (one of the seven region values), `languages`. The seven region groups in
the selector are derived from `region_key`; they are not a stored list.

**`promotions`** - the three highlight cards and the three discover cards. Fields: `id`, `title`,
`media_ref`, `destination`, `row_key` (one of `highlight` and `discover`), `display_order`. The
consumption disclaimer that sits beneath the highlight row is a field on the row rather than on any
card, because the figures are only meaningful as a set.

**`owners`** - accounts. Fields: `id`, `email` (unique, case-insensitive), `password_hash`,
`created_at`.

**`saved_comparisons`** - Fields: `id`, `owner_id` (references `owners`), `name`, `facet_state`,
`created_at`, `updated_at`. `name` is unique per owner and not globally: two owners may each hold
a saved comparison called the same thing, and one owner may not hold two. A saved comparison always
belongs to exactly one owner, and that owner is taken from the session.

**`saved_comparison_variants`** - the variants inside a saved comparison. Fields: `id`,
`saved_comparison_id` (references `saved_comparisons`), `variant_id` (references `variants`),
`position`. A variant appears at most once in one saved comparison.

**`consent_choices`** - the answer to the storage question and the market prompt dismissal, held
against a visitor identifier. Fields: `id`, `visitor_key` (unique), `storage_choice` (one of
`all` and `necessary`), `market_prompt_dismissed` (boolean), `decided_at`.

**Derived rather than stored.** Every facet count is computed from `variants` on each request and
is never a column. The seven series counts are computed against the other three facets and not
against the series facet itself, which is why they sum to the count on `All`. The result grouping
is computed from `body_style`. The comparison set held by an anonymous visitor is not stored at all:
it lives in the query string.

**Seed data.** Six families in the two orderings above, with `700` seeded `unavailable`. Ninety two
variants distributed `700` ten, `900` twenty two, `Volten` twenty two, `Cardinal` nine, `Terra`
five and `Sierran` twenty four, so the counts are true of the data rather than asserted over it.
The `900` family's variants include the six named in Core features with exactly the figures and
labels given there, split across the body styles `900 Corsa` and `900 Corsa Cabriolet`. Markets
cover all seven regions, with `international-en` among them and marked as the default locale.
Six promotions, three in each row. Two owners, `owner@example.com` and `owner2@example.com`, each
holding one saved comparison of two variants at first start, with different names.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and structural detail the product is measured on. Nothing here
overrides `## UI/UX notes`; it is the same direction at the level of individual surfaces.

### Layout and stacking

The page is a twelve-region grid with a gutter that grows with the viewport. The range grid is two
columns from the tablet tier upward and one below it. The highlight row and the discover row are
three columns from the tablet tier upward and one below.

Stacking is shallow and explicit. Two elements establish an isolated stacking context, the
application root and the main region, and that is what keeps the header and the dialogs above
content without anything climbing high. Nothing in the build may stack above the ceiling those two
contexts establish, and the set of stacking values in use stays small and documented rather than
growing ad hoc.

### The header

A fixed header on every route holding four things and nothing else: a menu control at the left, the
wordmark centred, and a globe control and an account control at the right.

The wordmark is centred in the viewport, not in the space between the two control groups, so on a
wide screen it stands alone and is nowhere near either. The menu control is a word and an icon
rather than an icon alone, and the word `Menu` sits to the right of the three lines. Keep the word.

The header has two states. Over the hero it carries no fill and no border, and its contents take
the dark scheme so they read pale against the film. Off the hero it takes the page ground and grows
a hairline bottom border. The change between the two uses the same band transition as everything
else.

### The footer

A dark-scheme region on every route, whatever the scheme of the band above it, which is what makes
the hard edge between the last content band and the footer read as the end of the page. Five
stacked bands, in this order:

1. a scroll-up control, centred, an upward arrow above the words `Scroll up`
2. a region and language row: the label `Current Region / Language`, a globe mark, the current
   market and language reading `International / English`, and a `Change` link
3. three link columns under the headings `Locations & Contacts`, `Company` and `Valdris on the web`
4. a row of six social marks, then two application-store badges
5. a copyright line, a legal link row, two disclaimer paragraphs, and the wordmark at large size,
   centred

The first column carries the link `Get in touch`. The second carries `Investor Relations`,
`Career`, `Global Partnership Council`, `Compliance`, `Newsroom & Press` and
`Information Security`. The third carries `Valdris Homepage`, `Valdris Configurator` and
`Valdris Connect`.

The copyright line reads `(c) 2027 Valdris Motoren AG.` The legal link row carries
`Legal Notice.`, `Privacy Policy.`, `Cookie Policy.`, `Consumption/Emissions.`,
`Open Source Software Notice.`, `Whistleblower System.` and `Accessibility.` **Every one of those
carries a terminal full stop inside the link text**, not after it. That is deliberate and is not a
typo to be tidied.

The two disclaimer paragraphs are legally load-bearing and are reproduced exactly:

`If the values are given as ranges, these do not relate to a single, individual vehicle and do not constitute part of the offer. They are intended solely as a means of comparing different vehicle models and refer to the product portfolio that is available on the domestic market. Extra features and accessories (attachments, tyre formats etc.) can change relevant vehicle parameters such as weight, rolling resistance and aerodynamics and, in addition to weather and traffic conditions, as well as individual handling, can affect the fuel consumption, energy consumption, CO2 emissions, range and performance values of a car.`

`Important information about the all-electric Valdris models can be found here.`

### The interstitials

The storage dialog is a centred panel on a dimmed ground, carrying the heading
`Your cookie settings.`, the subheading `Personalised experiences at full control.`, one paragraph
naming the categories of storage in use, a `Cookie Policy` link to the cookie route, and two
controls: `Accept all` as the filled dark action and `Only necessary cookies` as the quiet one.

The market prompt is a smaller panel at the top right reading
`Do you want to switch to your local market for correct content and pricing?`, with
`Go to Local Market` and `International` as its two controls and a round close control.

### The home route, band by band

**Hero.** Full-viewport, dark scheme, the film behind everything. In reading order: the family name
as the page heading at the largest size, bottom-left aligned rather than centred and followed by a
full stop, reading `Sierran.`; a call to action reading `Discover more`; the looping scroll
indicator centred at the foot; the playback control at the lower right; and the consumption
disclaimer centred below the indicator, at the legal size, in the dark scheme, belonging to the
hero rather than to the band below it. The hero disclaimer reads
`Fuel consumption combined (model range): 11.7 - 10.6 l/100 km, CO2-emissions combined (model range): 266 - 242 g/km`.

The terminal full stop on the hero heading is a house style that recurs on every card title in the
route. The call to action is a filled frosted button at the promoted-card softness, not a pill and
not a plain link. The heading arrives with the headline reveal over the longest of the four speeds;
the call to action follows with the control reveal.

**Highlight row.** Light scheme. Three promoted cards in one row, each a photograph at the
promoted-card softness with a title in white at the lower left and a round arrow control at the
lower right. The three titles are `Volten Turbo Cross Tourer.`, `The new 900 GTX S/C.` and
`Cardinal 4.` Beneath the row sits one consumption disclaimer covering all three cards at once, at
the legal size, its three clauses separated by a vertical bar. **It is a single paragraph and must
stay one**, because the figures are only meaningful as a set:

`Volten Turbo Cross Tourer: Electric energy consumption combined (model range): 21.4 - 18.9 kWh/100 km, CO2-emissions combined (model range): 0 g/km | 900 GTX S/C: Fuel consumption combined (model range): 13.7 l/100 km, CO2-emissions combined (model range): 310 g/km | Cardinal 4: Fuel consumption combined (model range): 11.0 - 10.1 l/100 km (preliminary value), CO2-emissions combined (model range): 250 - 230 g/km (preliminary value)`

The three cards reveal with the tile reveal and the indexed stagger.

**Range headline.** Light scheme. One line at a section headline size, left-aligned and running
close to the full page width: `Your Valdris journey starts now.`

**Model range grid.** The centrepiece. Six tiles, two columns from the tablet tier upward and one
below, each tile a photograph or a short silent film of one family. Every tile carries, in this
order: the family signature centred at its head in script; the top scrim; the media filling the
tile at the tile softness; the bottom scrim; a row of one to three availability chips at the lower
left, fully rounded and frosted; a one-line body description in the primary colour of the tile's
scheme; and a round arrow control at the lower right carrying a label for assistive technology.
The tile action label is `Explore`.

The whole tile is one link. The arrow control is decorative rather than separately focusable, so a
keyboard visitor reaches each tile once rather than twice.

This grid is where the scheme alternation happens: as it scrolls, the band behind the tiles changes
between the light and the dark ground, and each family signature runs its ramp in the opposite
direction so it stays legible against whatever the band has become. Tiles reveal individually,
starting faintly visible rather than fully transparent.

**Discover row.** Light scheme. Three cards in one row, the same component as the highlight row
with different data, pointing at programmes rather than vehicles, under a centred heading reading
`Discover`. The three titles are `Valdris Experience.`, `E-Performance - Sustainable mobility` and
`Valdris Finder.` Note that the second is the one title without a terminal full stop, and note that
`Discover` is centred whereas the range headline is left-aligned. Both differences are deliberate.

After this row the page cuts hard to the dark footer with no transition band between them.

### The scrim

Every range tile carries a gradient over its media so the caption stays legible, and it is not a
two-stop ramp. The darkening accelerates toward the caption rather than climbing evenly, through
many eased stops, and it caps short of fully opaque and holds there, so the darkest part of the
tile still shows the photograph under the text. Two instances exist per tile, one running to the
top and one to the bottom, so a tile can carry the family signature at its head and the caption at
its foot with the middle of the image untouched. This is the most important single effect on the
home route and it must read as an accelerating fall rather than a linear one.

A second, simpler gradient fades the sticky `Filter` control on the model overview into the page,
from the surface colour at full strength to the same colour at none, over the height of the
control, so content scrolls out beneath it rather than being clipped by a hard edge.

### The model overview

**Page head.** Light scheme throughout, sitting on the surface colour rather than the page ground,
which is what makes the white variant cards read as raised without a shadow. The head carries the
route heading `Model overview` at the route headline size, left-aligned, and at the far right of
the same band a two-line offer to resume: the question `Do you already have a configuration?` above
a filled dark button reading `Load saved configuration`.

**Filter rail.** A left rail, sticky within the page, holding the four facet groups. `Model series`
is always expanded, a radio list, each row a label and a count in parentheses in a quieter colour.
Between the series list and the collapsed groups sits an aside: the question
`What are the differences in body types and model designations?` above a filled dark button reading
`Understand the differences`. `Body Design`, `Seats` and `Drive` follow as three collapsed groups,
each a heading with a downward chevron. At the foot of the rail sits a `Reset Filter` control.

Below the tablet tier the rail collapses behind a single `Filter` button that opens the whole rail
as a panel. That button is sticky and carries the fade gradient described above.

**Variant card.** The densest component in the build. On the surface-coloured page it is a white
card at the promoted-card softness carrying, top to bottom: a cutout image of the car in profile
overflowing the top edge so the wheels sit on the card boundary rather than inside it; the variant
name at the card headline size; the chip row; the three statistics, each a value above its label
with the value at a statistic size and the label at the secondary size in a quieter colour; the
consumption paragraph at the legal size; an underlined text link reading
`Technical data and standard equipment`; two buttons side by side, a filled dark `Explore in Detail`
and a quiet grey `Configure`; and a `Compare` checkbox, unfilled, at the card foot.

**The cutout breaking the top edge is the detail that makes the component.** The card is a white
panel and the car is not inside it but resting on it. A build that contains the image within the
card has built a different component.

### The legal routes

One shared layout: a heading, then long prose held to the narrowest measure, in the light scheme,
with the standard chrome above and below. Body prose is at the body size over its body line height.
Numbered top-level headings sit inside the document body rather than acting as route structure.
Inline anchors are underlined at rest at the smallest corner softening. Bold marks defined terms
inside a paragraph rather than marking headings. These routes are the only ones where reading
length is the design problem, so each carries an in-page contents list above the first heading.

### Responsive behaviour, per module

| Module | Below the tablet tier | Tablet tier | Wide desktop |
|---|---|---|---|
| header | menu word retained, controls unchanged | unchanged | unchanged |
| hero | media offset recalculated for portrait, headline at the reduced size | as desktop | as desktop |
| hero reveal | travel roughly halved | full travel | full travel |
| highlight row | one column, cards stacked | three columns | three columns |
| range grid | one column | two columns | two columns |
| range tile | separate poster element with its own opacity handling | shared with desktop | shared with desktop |
| discover row | one column | three columns | three columns |
| overview rail | collapsed behind a sticky `Filter` button | beside results | beside results |
| overview results | one column | two columns | two columns |
| variant card | statistics stacked, buttons full width | as desktop | as desktop |
| legal prose | full width less gutter | narrow measure | narrow measure |
| footer columns | stacked | three columns | three columns |

The range tile is genuinely a different implementation below the tablet tier rather than a restyled
one: it carries a distinct poster element with its own opacity handling and its own signature
transition. Build it as a variant of the module, not as a media query over the desktop one.

### The primitive layer

Presentation primitives are defined once and consumed identically on every route. Each carries its
own styles and depends on the page it sits in for nothing except the colour scheme.

| Primitive | Role |
|---|---|
| display | the very large headline, hero and section |
| heading | structural headings inside a route |
| text | body copy at any of the three fixed sizes |
| link | a styled anchor, filled or quiet |
| link, plain | an anchor with an arrow and no fill |
| button | an action, filled or quiet |
| icon | one of the ten figures below |
| tag | the model-year chip |
| flag | the availability chip |
| model signature | the masked script wordmark |
| scroll indicator | the looping arrow under the hero |
| background video | the covering media layer behind the hero |
| grid, grid item | the twelve-region layout |

Choose one prefix for every primitive element and every module class and apply it consistently.

**Composition rules.** A route composes modules; a module composes primitives; a primitive composes
nothing. A module owns its scheme declaration and nothing else about its colour. The range tile,
the promoted card and the variant card are three separate modules rather than one card with three
modes, because their internal structure differs and not only their content. The highlight row and
the discover row are the same module with different data and must be built once. No module may
reach into another to position it.

**State ownership.** The colour scheme of a band belongs to the module and is declarative. Reveal
state belongs to the element and lasts the page lifetime once set. Video playback and pause belong
to the hero module. The storage choice and the market-prompt dismissal belong to the application
and are durable per visitor. Facet selections and the anonymous comparison set belong to the route
and live in the query string. The open state of the filter panel belongs to the rail module. A
saved comparison belongs to its owner and is durable. No module holds a copy of the range data.

### Iconography

Ten icons appear across the routes: `menu` in the header beside the menu label; `globe` and
`account` at the header right; `arrow-right` inside the round control on every card; `arrow-down`
in the scroll hint under the hero; `arrow-up` in the scroll-up control above the footer;
`chevron-down` on the collapsed facet groups; `pause` on the hero playback control; `close` on the
market prompt dismiss control; and `check` for the compare tick and the selected filter radio.

All ten are drawn rather than fetched, on one shared square grid, stroked rather than filled, with
round caps and round joins, and they inherit the current text colour so they flip with the scheme
without a second declaration. Round icon buttons take the fully rounded softness and a frosted
fill, and they are larger on the hero control than on the cards.

### The family signature

Each of the six families is titled on its tile not by text but by a script wordmark, and it must be
built as a mask over a colour-filled element, with the fill coming from one property, so the
transition described in `## UI/UX notes` has something to animate. **A coloured picture cannot be
animated this way and must not be substituted for it.**

Draw each wordmark as a single continuous path in a connected italic script at a shared skew, from
the family name. Build each glyph from two curved segments, an upstroke and a downstroke, with the
downstroke about twice the width of the upstroke, joining at the baseline so the word is one
unbroken path, and give the last glyph a flourish extending to the right at the cap line. Two of
the six families are numerals rather than words, and those are set in the same script with the same
construction. This is an honest substitute for a wordmark rather than a reproduction of one: what
it must do is occupy the same space, at the same weight, and change colour the same way.

### Zero-asset substitution guide

The build ships with no binary file of any kind. Every asset class the design depends on is
replaced by a procedure below, and this guide is the whole of it. Where a substitution is a drawn
stand-in rather than a fair equivalent, it says so: an honest placeholder is worth more than a
near-miss of something trademarked.

**Tile and card photography.** Canvas-generated gradient placeholders keyed by a seed derived from
the family key, using only colours from the palette. For each tile, compose a three-stop vertical
gradient from the dark ground through a mid grey to a lighter grey, then overlay a single soft
elliptical highlight offset from centre at a low strength to suggest a lit body. Apply the scrim
over the result unchanged: the scrim is specified, not substituted.

**Variant cutouts.** The card needs a car-shaped silhouette overhanging the card edge, and a
rectangle will not do because the overhang is the point. Compose the silhouette from primitives: a
body as a rounded rectangle more softened at the front than at the rear, a cabin as a clipped
ellipse set back from the nose, and two wheels as circles near each end. Fill it with a vertical
gradient from a mid grey to the dark ground and place a soft shadow ellipse beneath it at low
strength. Keep the wheels on the card boundary.

**The hero poster.** The same generator as the tile photography, at the hero aspect, seeded from
the family on the hero.

**The hero film.** There is no procedural substitute for a film of a car. Ship the poster and a
short generated loop composed as a slow vertical pan across the poster gradient with a single
specular highlight travelling left to right, delivered as an adaptive segmented stream so the
delivery path is exercised for real. Where a real film exists it drops into the same slot and
nothing else changes. This is honestly a placeholder and will look like one.

**Application-store badges and social marks.** Drawn as geometry, in monochrome, taking the current
text colour. Do not reproduce the store badges as supplied by their owners; draw a neutral
equivalent.

**The crest.** A neutral roundel: a circle at the fully rounded softness with a stroke in the
current text colour, quartered by one vertical and one horizontal line, with two opposite quarters
filled faintly. It occupies the same box as a heraldic crest would and deliberately carries no
resemblance to one.

## Constraints

- Single locale content. The site ships one language and one market-neutral international locale,
  and the selector lists the others without implementing them.
- No account features beyond sign-up, sign-in and saved comparisons. No profile, no preferences,
  no password reset, no email of any kind.
- These systems are linked from the reference site and **none of them is built here**: the
  configurator, the stock finder, the connected-services product, the saved-configuration system,
  the newsroom, the careers site, the investor-relations site, the per-market sites reachable
  through the selector, and the four legal documents in the footer that are not among the three
  that ship. The `Load saved configuration`, `Understand the differences`, `Explore in Detail`,
  `Configure` and `Technical data and standard equipment` controls are present and styled because
  they are part of the design, and they lead nowhere in this build.
- The comparison view itself is out of scope. What ships is the selection, its persistence, its
  addressability and the ability for an owner to save it.
- No price is quoted anywhere, and there is no cart and no checkout.
- No sort control on the overview, by any statistic or by name.
- No breadcrumb anywhere. The graph is two levels deep and a breadcrumb would imply a third.
- No binary asset of any kind is loaded, on any route. Every image, mark, icon and the film itself
  are generated or drawn.
- No third-party tracking pixel and no consent vendor. The storage choice is recorded by the
  product itself.
- No external network calls at runtime. Everything the product needs is in the environment.
- No native app. The product does not work with the network off, and is not expected to.
- The product must stay responsive with ninety two variants across six families and around two
  hundred markets, which is the volume it is built for.

**Latitude, granted deliberately.** Several areas carry no evidence behind them, and each is a
reconstruction rather than a measurement, so the build is not expected to match anything there and
a reasonable interpretation is correct.

- The hover states are a reconstruction from the declared transitions rather than an observation.
- The values inside `Body Design`, `Seats` and `Drive` were never seen expanded, so their contents
  are yours to choose, as multi-select lists built like the series list and consistent with the
  seeded variants.
- The six script wordmarks and the ten icons are drawn rather than traced, and a faithful drawing
  is not the goal.
- The narrowest width tier carries only small-phone adjustments, chiefly chip wrapping when a
  family offers three powertrains, and the exact behaviour there is yours.
- The trim vocabulary is fixed: `Corsa` is the core trim name inside a family and `GTX S/C` is the
  track-focused trim name, and they are used consistently wherever a trim is named.

Acceptance of this build rests on what a person can see in a browser without reading any source,
so where this brief grants latitude it grants it fully.

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
| `POST /api/auth/signup` | `{email, password}` | the created owner and a bearer token |
| `POST /api/auth/login` | `{email, password}` | a bearer token |
| `GET /api/home` | `locale` | families in home order, and promotions by row key |
| `GET /api/families` | none | a top-level JSON array of families in facet order |
| `GET /api/variants` | `series`, `body`, `seats`, `drive`, `compare` | variants matching the facet set, grouped by body style, with a count for every value of every facet |
| `GET /api/markets` | none | a top-level JSON array of markets, each carrying its region key |
| `GET /api/comparisons` | none | a top-level JSON array of the calling owner's saved comparisons |
| `POST /api/comparisons` | `{name, variant_keys, facet_state}` | the created saved comparison |
| `GET /api/comparisons/{id}` | none | one saved comparison with its variants and facet state |
| `PATCH /api/comparisons/{id}` | `{name}` | the updated saved comparison |
| `DELETE /api/comparisons/{id}` | none | an empty success |
| `POST /api/consent` | `{storage_choice}` | the recorded choice |
| `POST /api/market-prompt/dismiss` | none | the recorded dismissal |

Field names are exact. List endpoints return a top-level JSON array. A successful call returns the
named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a
server error and never as a silent success. Bearer auth is required on everything under
`/api/comparisons` and on nothing else except where stated; the public read endpoints and health
take no token.

`GET /api/variants` returns counts for every facet value under the current selection and not only
for the selected one, because every count is displayed at all times. A count for a value inside the
series facet is computed against the other three facets only.

## Definition of done

A visitor can open the home route, read the six families, follow one tile to its overview, narrow
ninety two variants to that family's own with a single control, and see every facet count agree
with the list it produced. Ticking variants into a comparison set survives a facet change, and the
resulting address reopens the same filtered and ticked view in a fresh window. A signed-in owner
can save that set under a name and find it unchanged after a reload, and no other account can read
or alter it. The home route stays complete and readable when the film never plays.
