# Orb Website Builder

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser and go from the long sales
page to a free account that already holds their own draft site, having searched a domain name on
the way, without hitting an error page.

A different stranger, with no account, must NOT be able to read a picture that belongs to a site
nobody has published yet, by any means: not through the owner's console, not through the public
address of a site, and not by guessing the object key. This cannot be arranged with a hidden
button. The uploaded bytes must live in the object store at their scheme's key and nowhere else;
a copy on the app container's own disk does not count, and a row holding the bytes in the
database does not count either.

---

## Overview

Orb is a hosted website building platform sold to small business owners and solo professionals
who have no technical background. This build is the public half of it: a marketing and sign-up
surface that moves a visitor from "I need a website" to "I have an account and a draft site". The
argument runs top to bottom on one very long home route, punctuated by a secondary point of sale
route that sells a card terminal, and a short not-found route for when a link is broken.

The visitor arrives from search or an advertisement, scrolls the home route without reading most
of it, and takes one of four exits: the pill in the fixed header, one of the in-page primary
buttons, the domain search field, or the login link. Only two of those touch state before a
visitor has an account. The domain search asks whether a name is free. The sign-up creates an
account, a workspace and an empty first site, in one transaction, and hands back a session.

Behind the sign-up sits a small owner console: a table of the owner's own sites, a way to add a
site, a way to upload a picture for a site, and a way to publish a site and roll that publish
back. A published site answers at a public address. A site nobody has published does not, and
neither do its pictures.

Orb is deliberately not a page editor, not a shop, and not an analytics product. The marketing
copy sells a drag-and-drop canvas, a site generator, a store, a booking calendar, a contact
database, an email sender, an automation builder, an advertising integration, a mobile owner
application and an in-person card terminal, because that is what the copy says. None of them is
built here. The genuinely hard part is the one that looks easy: a draft site's uploaded bytes
have to be in the object store, at a key anyone could guess, and still be unreadable to everyone
except the one owner who put them there.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Read every marketing route, search a domain name, list templates, read any site that has been published, sign up, sign in | **Cannot open the owner console. Cannot read a site nobody has published. Cannot read a picture belonging to an unpublished site. Cannot upload, publish or roll back anything.** |
| `owner` | Everything a visitor can do, plus list and open the sites in their own workspace, add a site, upload a picture with alternative text, publish a site, roll a publish back | **Cannot read, upload to, publish or roll back a site in another owner's workspace. Cannot move a site to a different workspace. Cannot read another owner's pictures.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a visitor session to any owner-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

**Sign-up is open.** Anyone can create an account from the sign-up form with no invitation and no
card, because the surface promises exactly that. Three accounts are seeded so the product has
something in it from the first start, and every one of them uses the same password.

| Email | Role | Workspace | Sites |
|---|---|---|---|
| `owner@example.com` | `owner` | `Kestrel Studio` | `Kestrel`, published; `Ivory and Interval`, draft |
| `owner2@example.com` | `owner` | `Cedar Workshop` | `Cedar and Sage`, draft |
| `visitor@example.com` | `visitor` | none | none |

## Core features

### Auth

Accounts are email and password, implemented by this app. There is no external identity provider.

1. `POST /api/auth/login` takes `{"email", "password"}` and returns `{"access_token": ...}` on a
   correct pair. Every later request carries that token as a bearer token.
2. A wrong password, an unknown address, or a missing token is denied, and the reply says nothing
   about which of the three it was.
3. Passwords are hashed. The stored value is never the literal the visitor typed.
4. A token that has expired is denied on the next request that carries it, and the caller is
   returned to the sign-in form with nothing half-written.
5. Sign-up is open to anyone. There is no invitation, no allowlist and no card.

### The long home route

The home route is seventeen bands stacked in one column, in this order: the hero over the drifting
colour field, the generation band, the solutions accordion, the template rail, the customisation
gallery, the assistant band, the foundations accordion, the domain search, the analytics marquee,
the operations accordion, the marketing gallery, the surfaces band, the six steps, the showcase,
the closing call to action, the frequently asked questions, and the footer. Every band's content,
geometry and copy is set out in `## Front-end specification`.

1. Nine bands repeat one arrangement, the standard band header: a large headline on the left, a
   short paragraph and a primary button on the right, and the band's own content underneath.
2. Four bands are accordions. Exactly one row of an accordion is open at a time, opening a row
   closes the row that was open, and the first row of the solutions accordion is open on load
   while every row of the questions accordion is closed on load.
3. Two bands are horizontal galleries that scroll sideways inside their own region. A gallery
   never captures the page's vertical scroll, and it is reachable and operable from the keyboard.
4. The template rail's seven category chips are one single-select group. The first chip is
   selected on load, arrow keys move between chips, and selecting a chip replaces the rail's
   content without a page navigation.
5. Every answer in the questions accordion is present in the document at first paint, not fetched
   when the row opens.
6. The assistant headline exists twice: once as a complete, stable heading that assistive
   technology and search engines read, and once as the visible version whose last two words
   cycle. The cycling copy is hidden from assistive technology, so the heading never changes
   under a screen reader.

### The point of sale route

`/pos` sells the card terminal. It is the only route where the design system runs on a dark
ground.

1. The route renders its own document with its own title and description, and is indexable.
2. Its headline is left aligned, where the home route centres its own. That difference is what
   separates a product page from a brand page in this system.
3. On a dark band the primary button inverts completely: a near-white ground with an ink label, at
   the same size and the same corner radius. It does not become an outline button and it does not
   keep the brand blue.
4. The feature grid shows its first rows and reveals the rest behind a `Show more` control.

### The not-found route and the campaign aliases

1. Any address the router does not know renders the product's own not-found page, carrying the
   same header and the same footer as every other route, one line of apology, one primary action
   back to `orb.com`, and a scatter of loose shapes.
2. That route answers with a not-found status, never with a success status. A page that says
   "not found" while answering `200` is the defect this rule exists to prevent.
3. The not-found route carries exactly two meta tags: the window declaration and a directive
   telling search engines not to index it. It carries no social sharing metadata at all, where the
   two indexable routes carry seventeen tags each.
4. The not-found route does not redirect and does not guess at what the visitor meant.
5. Nine campaign aliases exist: `/as`, `/gs`, `/v1`, `/v2`, `/412`, `/416`, `/417`, `/419` and
   `/md/`. Each serves the home document and rewrites the address bar to the origin root before
   first paint, so an alias never becomes a canonical address and never appears as a distinct
   route. An alias is not a redirect and costs no second round trip.

### The domain search

The domain band is the only part of the marketing surface that touches state before anyone has an
account. Its field is placeheld `Type the domain you want` and its button is labelled `Search`.

1. `GET /api/domains/availability` takes `query`, the label the visitor typed, and optionally
   `suggest`, how many alternatives to return, which defaults to `8` and is capped at `20`.
2. The reply carries `normalised`, `exact`, `suggestions` and `partial`. `normalised` is the
   label trimmed and lower-cased. `exact` is an object of `name`, `available`, `premium`, `price`,
   `currency` and `registry_status`. `suggestions` is a list of the same object, ranked and never
   shuffled. `partial` is a boolean, true only when the answer is incomplete.
3. A name the registry holds is answered `available: false` with `registry_status` of
   `registered`. A name the registry does not hold is answered `available: true` with
   `registry_status` of `available`, a `price` of `1200` minor units and a `currency` of `usd`.
   `1200` is `$12.00` per year, not `12.00` and not `12`.
4. Suggestions are generated from the query's own tokens crossed with the suffix set and are
   ranked stably, so two identical queries return the same list in the same order. A suggestion
   that turns out to be taken later is an acceptable outcome; a slow field is not.
5. The same query asked twice returns the same normalised label. `  ForkNFrame  ` and
   `forknframe` are the same query and both normalise to `forknframe`.
6. An empty or whitespace-only `query` is refused as invalid, naming the field, and nothing is
   recorded.
7. The search is rate limited to `20` queries a minute from one address. Past that limit the
   answer degrades to cached data with `partial` set to true, rather than becoming an error. The
   visitor is never shown a failure for asking twice.
8. A negative answer may be served from cache for `60` seconds. A positive answer is never served
   from cache, because an available name is the thing most likely to change under the visitor.
   Caching is asymmetric on purpose and the asymmetry is the requirement.
9. What the visitor typed is recorded without any identifier attached to it, because the name of a
   business nobody has announced yet is a strong signal and is nobody else's business.

### The template library

1. `GET /api/templates` is public and takes `category`, `cursor` and `limit`. `limit` defaults to
   `24` and is capped at `48`; a larger value is clamped to `48` rather than refused.
2. The library holds `33` distinct templates across `7` categories: `eCommerce`, `Portfolio`,
   `Business`, `Landing page`, `Blog`, `Real estate` and `Weddings`.
3. The reply carries `items`, `facets` and `next_cursor`. `facets` is a count per category, so the
   chips can show their numbers without a second request.
4. The default ordering is a stable ranking, never a random shuffle. A rail that reorders on every
   load makes the page feel broken.
5. A `category` outside the seven is refused as invalid, naming the field.
6. The rail on the home route shows `35` template links beside `7` category links, which is the
   `40` links the design calls for. Two template names appear twice in the source copy; the
   library deduplicates them, which is why `35` links resolve to `33` distinct templates.

### Opening a free account

1. `POST /api/accounts` takes `{"email", "password", "domain_query"}` and creates three things in
   one transaction: an account, a workspace and an empty first site carrying the default theme.
   It returns `{"access_token", "site_id"}`.
2. The new site is created with `status` of `draft`, a `live_revision` of null, a first revision
   numbered `1`, and a free address of the form `{slug}.orbsite.com`.
3. The operation is idempotent on the email address for `10` minutes. A second sign-up with the
   same address inside that window returns the first answer and creates no second account, no
   second workspace and no second site. After the window it is an ordinary conflict and is
   refused.
4. A full session is granted immediately, with no verification wall, because the page promises
   `Start for free. No credit card required.` and a wall would contradict the promise.
5. An email that is not an address, or a password shorter than `8` characters, is refused as
   invalid, the field is named inline, and nothing is written.
6. The sign-up form links to the terms page, and a visitor cannot submit without agreeing to
   them.
7. Success lands on a full-page confirmation naming the new site and its free address, with one
   primary action continuing to the console.
8. A form submitted by something that is not a person is refused: the form carries an unattended
   decoy field that a person never sees and never fills, and a submission that fills it is
   refused with nothing written.

### The owner console

1. `/dashboard` lists the signed-in owner's sites as a table, one row per site, showing the name,
   the free address, the status and the date it was created. A visitor opening `/dashboard` is
   denied.
2. `GET /api/sites` returns a top-level JSON array of the caller's own sites and nothing else. An
   owner never sees another owner's site in that array, and the array is empty rather than an
   error for an owner with no sites.
3. A site is added as a new row in the table itself. Pressing the control at the head of the table
   opens an empty row in place, the name and the address are typed into that row, and saving it
   never leaves the page.
4. A site name that is empty, or a slug already taken by any site anywhere in the product, is
   refused as invalid, the field is named in the row, and nothing is written.
5. `GET /api/sites/{site_id}` returns one site to its own owner. The same call from the other
   seeded owner is denied and the row is left untouched.

### Media, and where the bytes live

1. `POST /api/sites/{site_id}/media` uploads one picture for one site. The caller must own the
   site; anyone else is denied.
2. The bytes go to the object store at `STORAGE_ENDPOINT` in the bucket named by
   `STORAGE_BUCKET`, under the fixed key scheme `sites/{site_id}/{sha256_of_bytes}.{ext}`. A site
   with identifier `3` uploading a picture whose contents hash to `9f2a...d0` stores it at
   `sites/3/9f2a...d0.png`.
3. Bytes live **only** in the object store. Not on the app container's filesystem, not in a
   database column, not in memory. The database row records the key, the content type, the byte
   size and the alternative text, and nothing else about the picture.
4. The content type is determined by inspecting the bytes, never by trusting the supplied file
   name or the request header.
5. Every uploaded picture carries alternative text, supplied by the owner. A picture that is
   purely decorative declares itself decorative instead, and an upload with neither is refused as
   invalid.
6. Uploading the same bytes to the same site twice produces one object and one row, because the
   key is derived from the bytes. The second upload is a no-op on the stored state.
7. Safety and rights travel with the picture. A vector upload is sanitised before it is stored:
   anything executable inside it is stripped, because a vector is a document and an unsanitised
   one would run on the owner's own address. An upload whose inspected bytes are not a picture at
   all is refused as invalid and nothing is written.

### Publishing, and what a draft keeps private

This is the rule the rest of the product is arranged around.

1. `POST /api/sites/{site_id}/publish` moves a site's `status` from `draft` to `published` and
   sets `live_revision` to the site's current revision number. It is refused for anyone who does
   not own the site, and the site's status is unchanged after a refusal.
2. A published site answers at `/s/{slug}` to anybody, signed in or not, and its pictures are
   readable there.
3. **A site whose `status` is `draft` is not publicly readable, and neither are its pictures.**
   `GET /api/published/{slug}` for a draft site is answered as not found, exactly as an address
   that was never used at all is. The existence of a draft is not disclosed.
4. `GET /api/sites/{site_id}/media/{media_id}` streams a picture's bytes. For a draft site it is
   served only to the owner of that site, over an authenticated request. An anonymous caller is
   denied, and so is a signed-in owner who does not own the site.
5. Choose one access-control mechanism for protected pictures and hold to it everywhere: either
   an authenticated streaming endpoint the app serves, or short-lived signed links that expire
   within five minutes and are never issued to someone not entitled to the picture. Pick one and
   be consistent.
6. The object key is not a secret and must not be treated as one. Knowing
   `sites/3/9f2a...d0.png` must not let anyone read those bytes while the site is a draft. The
   bucket is private and the app is the only door.
7. `POST /api/sites/{site_id}/publish/rollback` returns a published site to `draft` and clears
   `live_revision`. The draft revision is untouched, the public address stops answering, and the
   pictures go back to being private. Rollback is refused for anyone who does not own the site.
   Publishing and rolling back each cause an invalidation of anything the product was holding
   about that site's public address, so the next read of `/s/{slug}` reflects the new state
   immediately rather than a stale one.
8. Two simultaneous publishes of the same site must not both succeed in setting two different
   live revisions: exactly one wins, the other is rejected, and the site is left naming exactly
   one live revision.

### Terms, privacy and the legal row

1. A terms page at `/terms` states the terms of use and is reachable from the footer of every
   route, including the not-found route.
2. The sign-up form links to the same terms page, and agreeing to the terms is required before an
   account is created.
3. A privacy page at `/privacy` states what the product records about a visitor, names the domain
   search as the one thing a visitor can do before signing up, and says that a search is kept
   without an identifier attached.
4. The footer's legal row carries `Terms of Use`, `Privacy Policy` and the line
   `© 2006-2026 orb.com, Inc`.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the long home route, seventeen bands | public |
| `/pos` | the point of sale route | public |
| `/terms` | the terms of use | public |
| `/privacy` | the privacy policy | public |
| `/signup` | open a free account | public |
| `/login` | sign in | public |
| `/dashboard` | the owner's own sites, as a table | owner |
| `/sites/{site_id}` | one site: its pictures, publish, roll back | owner, own site only |
| `/s/{slug}` | a published site as the public sees it | public |
| `/as` `/gs` `/v1` `/v2` `/412` `/416` `/417` `/419` `/md/` | campaign aliases for the home document | public |
| any other address | the product's own not-found page | public |

**Entry and redirects.** An unauthenticated request for `/dashboard` or for any
`/sites/{site_id}` lands on `/login` with the intended address remembered, and signing in
continues to it. Signing in from `/login` with nothing remembered lands on `/dashboard`. Signing
out returns to `/` and clears the session. A token that expires part-way through an action
returns the caller to `/login`, writes nothing, and says the session ended. An owner opening
another owner's `/sites/{site_id}` is refused and sees the product's own refusal page rather than
a blank screen or somebody else's site. A visitor opening `/dashboard` is refused for the same
reason. An alias path serves the home document and rewrites the address to `/` before first
paint.

**Journeys.**

1. **Search a name, open an account.** Open `/`, scroll to the domain band, type `forknframe`
   into the field, press `Search`. The result names the normalised label, says the exact name is
   available at `$12.00` a year, and lists ranked alternatives. Press `Get Started`, land on
   `/signup`, enter an address and a password, follow the link to `/terms` and agree, submit. A
   full-page confirmation names the new site and its free address under `orbsite.com`. One
   primary action continues to `/dashboard`, where the new site stands in the table as a single
   `draft` row.
2. **Publish a draft.** Sign in at `/login` as `owner@example.com` with the seeded password, open
   `/dashboard`, open `Ivory and Interval`, upload a picture and give it alternative text, press
   publish. The row's status reads `published`, `/s/ivory-and-interval` answers to anybody, and
   the picture is readable there.
3. **Add a site.** On `/dashboard`, press the control at the head of the table. An empty row opens
   in the table itself. Type the name `Vela Tov` and the address `vela-tov`, save the row. The
   row is saved in place and the page is never left.
4. **Roll a publish back.** Open a published site, press roll back, and watch the status return to
   `draft`, the public address stop answering, and the draft revision stay exactly as it was.
5. **A stranger tries a draft's picture.** With no session at all, request the draft site's
   picture address. The request is denied and no bytes are served.
6. **Browse the templates.** On `/`, press the `Portfolio` chip in the template rail. The rail's
   content is replaced without a page navigation and the chip shows how many templates it holds.

**States.** Every list has an empty state: a brand-new owner's `/dashboard` says the table is
empty and offers the one primary action that adds a first site, rather than showing an error.
Every page has a loading state, and every deferred media block reserves its space so nothing moves
when it arrives. A failed request leaves the page usable and says what failed in the product's own
words. The domain result region announces itself politely when the answer arrives, and nothing
else on the marketing surface is live. Errors never crash the app.

## UI/UX notes

The design is measured from a real product and the character is its own, not a house style. The
north star: in the first moment a visitor should understand that this is a place where a business
gets a real website, and should feel unhurried about it. The register is consumer and editorial
rather than operational, so the subject is seen first, the page carries atmosphere, and the
argument runs top to bottom in one column. Four stances, each of which a competing product could
rationally invert: calm over expressive, light over shapes, continuity over steps, and one loud
thing over many.

**The mood is unhurried and daylit.** A near-white page, near-black headlines, mid-neutral body
copy, and exactly one mid, vivid blue that belongs to the pill in the top corner and to inline
links, and appears on nothing else. All the real colour on the page comes from behind the
headline rather than from any component. The product must not look like a page dominated by a
single hue with no second signal, and it must not put a marketing composition where a working
interface belongs.

**The signature is a field of light, not shapes.** Behind the hero sit seven enormous soft-edged
circles, most of them larger than the window and positioned so their edges are always off stage.
You never see a circle; you only ever see the middle of one, so what reaches the eye is a wash of
coloured light. They recolour together on a slow shared clock, and the way they recolour is the
whole trick: each colour is held for a long plateau and then swapped quickly, never blended, so
the page has three distinct moods rather than one muddy smear, and three loads a few seconds
apart look visibly different. Each circle also drifts on its own separate clock by an excursion
under two percent of its own size, quantised to a grid, so the pattern never repeats in a way
anyone could catch and the circles read as light shifting rather than as objects moving.

**Motion has two speeds and nothing between them.** Anything the visitor triggers resolves inside
a third of a second; anything the page does by itself takes at least three seconds. Section cards
arrive by being uncovered from below rather than by fading, and settle short of full strength so
they read as sitting slightly under the page. The assistant headline's last two words
step up one line at a time, through six phrases and back to the first. The analytics chips slide endlessly
past and pause on hover and on focus. No element may declare a transition on everything it owns:
every state change names the properties it will animate, which is also what stops a focus ring
animating. Under a reduced-motion preference the field holds at one phase with no rotation, no
drift and no recolour, the word cycle shows its first phrase and does not advance, the marquee
holds, and every reveal resolves instantly to its end state, while the short control transitions
stay, because a press is not what that preference is about.

**Type is an identity, so it is named exactly.** Two families and nothing else: a geometric
humanist sans with a single-storey lowercase `a` in its display cut and a true optical-size split
between display and text. Weights 400, 500, 700 and 800 in the display family, 400 and 700 in the
text family, both loaded with a swap policy so first paint is never blocked on a font. The exact
role-by-role scale is set out in `## Front-end specification` and is not negotiable. Two rules
hold across every row of it: letter-spacing is always a negative percentage of the size, never an
absolute length, and line-height is always a unitless ratio, never a length.

**Shape, density and elevation.** Corners are gently rounded in four sizes: fully round for the
pills and the ambient circles, generously rounded for the in-band primary buttons, softly rounded
for media cards, and barely rounded for the smallest floating chips. The density is spacious: the
content column is generous, the bands are tall, and the margin opens up only on the largest
window, which is where the field needs room to be seen. Shadows are cool-tinted rather than
black, which is what stops the page reading as a stock component library, and there are two: a
floating-panel shadow that reads as a soft pool a long way below the element rather than as an
outline around it, and a tighter, fainter card shadow. The exact shade of any of these is yours,
so long as it holds the relationships above.

**Every page leads with one primary action.** It is visually distinct from every secondary
control on the same page and there is never a second thing competing for it: `Get Started` on the
home route, `Talk to Sales` on the point of sale route, the one button back to `orb.com` on the
not-found route, and the one control that continues to the console on the sign-up confirmation.
On a dark band the primary button inverts completely to a near-white ground with an ink label at
the same size and radius; it never becomes an outline button and it never keeps the brand blue.

**Three colours carry meaning, and they carry nothing else.** One says a thing has gone wrong,
one says a thing succeeded, one says a thing is still in progress; each appears only in that
sense, and none of the three is the primary action's blue. A field that fails validation wears
the failure colour beside its message, never instead of it. Surfaces that sit above the page
ground are a shade nearer white than it, and a border is the muted rule colour, never the body
ink. The primary action darkens on hover rather than changing hue. The exact shade of any of
these is yours, so long as each keeps its one meaning.

**The product commits to a light mode and designs it fully.** A dark mode is optional and is not
part of what the product owes; the dark bands on the point of sale route are a band treatment
inside the light mode rather than a second theme.

**Components carry states, not measurements.** Resting, pointed-at, pressed, focused and
unavailable, on everything interactive. A text field shows its label above it and its error
message below it, in the failure colour, without the field jumping as the message arrives.
Escape closes the mega panel and returns focus to the item that opened it. A destructive action,
rolling a publish back among them, asks for confirmation before it runs. Unavailable is never
signalled by colour alone.

**Accessibility floors, which are contract rather than taste.** Body text and its ground meet WCAG
AA contrast, and the small caption on the product route moves to a darker ink because it sits
below the body size. Full keyboard navigation in document order reaches every control, including
both horizontal galleries and the chip filter, which is one group with one tab stop and arrow keys
between chips. A visible focus indicator sits on every focusable element and holds against the
white bands and the dark bands alike. Every icon-only control carries a name and every content
image carries alternative text, while decorative images declare themselves decorative and a
decorative arrow inside a button is hidden from assistive technology. Meaning is never carried by
colour alone. The skip control is the first focusable element on every route. One hard case
follows from the field: the headline's contrast has to hold at every colour phase the field passes
through and at both drift extremes, not only at the moment the page loaded.

**Responsive behaviour holds at every width between the named tiers.** The layout is drawn three
times, once for a phone, once for a tablet and once for a computer, and inside each the whole
drawing scales with the window rather than stepping at a breakpoint. The seven navigation items
and the language control collapse behind one control below the largest tier while the primary
pill stays visible. At a narrow viewport nothing overflows sideways and every navigation target
stays reachable. The tablet tier is the tallest document of the three, because four-across rows
become two-across before they become one-across, so it is the width to check cost at. Below the
tablet tier the field renders four circles rather than seven: the look survives and the cost does
not. In landscape on a narrow window the hero collapses to the headline, the button and the
caption, and the collage is suppressed. The six numbered steps stay two across even at the
narrowest window.

## Front-end specification

This section is the visual and content specification in full. It is unbudgeted on purpose: the
detail here is what makes the built product the same product rather than a similar one.

### The scaling model

The page does not use a fluid type scale and does not step sizes at breakpoints. It is designed
on a **fixed canvas per breakpoint** and every scaled value is multiplied by
`window width / canvas width`.

| Breakpoint | Canvas width | Window measured | Scale factor |
|---|---|---|---|
| Small | 360 | 390 | 1.0833333 |
| Medium | 768 | 990 | 1.2890625 |
| Large | 1920 | 1440 | 0.75 |

The proof is the hero headline, exact in all three:

| Window | Measured size | Measured line-height | Measured letter-spacing | Canvas size |
|---|---|---|---|---|
| 390 | 41.1667px | 45.2833px | -0.823334px | 38px, 1.1, -2% |
| 990 | 72.1875px | 72.1875px | -1.44375px | 56px, 1.0, -2% |
| 1440 | 82.5px | 99.0001px | -1.65px | 110px, 1.2, -2% |

Within a breakpoint band every scaled value moves linearly with window width and nothing steps.
Two windows forty units apart inside one band differ by exactly `40 / canvas` times the canvas
value on every scaled property. A build that rounds to whole units at render time disagrees with
this table in the fourth decimal.

Three classes of value are identical at all three window widths and are therefore fixed rather
than scaled: the legal caption at `12px / 15.6px`, the chrome type, and the corner radii.
Everything inside a content band scales; the fixed chrome around it does not.

### Breakpoint boundaries

Five queries carry the layout: a small band below `768`, a medium band from `768` to `1182`, a
large band from `1183` up, a negative of the large band covering everything below `1183`, and a
second large step from `1280` used by the chrome only. Four narrower queries at `749`, `590`,
`400` and `380` are honoured as refinements rather than as breakpoints. Two orientation cases
exist for the small band: portrait, and landscape capped at a `1600` window.

### The type scale

| Role | Size | Line-height | Weight | Letter-spacing | Canvas value |
|---|---|---|---|---|---|
| Hero headline | 82.5px | 99.0001px | 400 | -1.65px | 110 / 1.2 / -2% |
| Section headline, large | 48px | 54.72px | 400 | -0.48px | 64 / 1.14 / -1% |
| Section headline, product route | 48px | 57.5999px | 400 | not set | 64 / 1.2 |
| Section headline, product route, dark | 48px | 52.7999px | 400 | not set | 64 / 1.1 |
| Sub-headline | 42px | 54.6001px | 400 | not set | 56 / 1.3 |
| Group heading | 21px | 23.9399px | 500 | -0.21px | 28 / 1.14 / -1% |
| Card heading | 24px | 36px | 400 | not set | 32 / 1.5 |
| Statistic numeral | 30px | 30px | 500 | -0.599999px | 40 / 1.0 / -2% |
| Statistic caption | 21px | 33.5999px | 400 | -0.419999px | 28 / 1.6 / -2% |
| Hero sub-headline | 18px | 23.4px | 400 | not set | 24 / 1.3 |
| Feature heading | 18px | 23.4px | 400 | not set | 24 / 1.3 |
| Button label, large | 20px | normal | 400 | not set | fixed |
| Button label, standard | 16px | 24px | 400 | not set | fixed |
| Body, standard | 13.5px | 18.9px | 400 | not set | 18 / 1.4 |
| Body, roomy | 13.5px | 21.6px | 400 | not set | 18 / 1.6 |
| Body, product route | 15px | 24.0001px | 400 | not set | 20 / 1.2 |
| Caption | 12px | 19.2px | 400 | not set | 16 / 1.2 |
| Legal | 12px | 15.6px | 400 | not set | fixed |

Two families are needed and nothing else: a geometric humanist sans with a single-storey `a` in
its display cut and a true optical size split between display and text. Weights 400, 500, 700 and
800 must be available in the display family; 400 and 700 in the text family. Both load with a swap
policy so first paint is never blocked. Name a family, do not ship one: naming an openly licensed
family is not an asset dependency, shipping a proprietary one is. The normative fallback stack, in
order, is the display family, then `Segoe UI`, `Roboto`, `Helvetica Neue`, `Arial`, and a generic
sans-serif. Do not reproduce a serif fallback; the reference resolved to one on the nodes rendered
before its variable faces arrived, and that is a bug in its fallback chain rather than a design
decision.

### The working colour set, by role

Colours are carried as family, tone and shade. No value appears anywhere in this brief; the exact
shade is yours so long as each role keeps its relationship and its exclusivity.

| Role | Colour | Where it is |
|---|---|---|
| Page ground | near-white neutral | body, header, most bands |
| Ink | near-black neutral | every headline, the dark buttons |
| Body ink | mid neutral | the most common colour on the site |
| Muted rule | light neutral | hairlines between accordion rows |
| Primary action | mid, vivid blue | the header pill only |
| Statistic ink | mid, vivid blue | the two hero numerals and their captions |
| Panel ground | near-white cool neutral | the mega menu right rail |
| Promo strip | light, soft indigo at low strength | the strip under each mega menu panel |
| Statistic divider | mid, muted indigo | the one-unit vertical rule between the two statistics |
| Hairline | near-white neutral | band separators |
| Cool tint | light, muted blue | the pale blue band grounds |
| Field ground | near-white neutral | the domain field |
| Ink, soft | deep neutral | secondary copy |
| Ink, softer | deep neutral | the smallest secondary copy |
| Link, blue | mid, vivid blue | inline links inside body copy |
| Accent, cyan | light, vivid cyan | the field's cool phase |
| Accent, lime | light, vivid lime | one loose shape on the not-found route |
| Accent, orange | mid, soft orange | one loose shape on the not-found route |
| Accent, violet | mid, muted violet | one loose shape on the not-found route |
| Tint, blue | near-white cool neutral | the cool placeholder gradient pair |
| Neutral, warm | light neutral | the warm placeholder gradient pair |
| Neutral, cool | light cool neutral | product photograph grounds |

The theme is a palette of **59 numbered slots** published on the root element, not a set of named
colours, and that is why one write recolours a whole site. Slots 0 to 5 are the brand primitives,
10 to 15 are a neutral ramp, and slots 16 to 20, 21 to 25, 26 to 30 and 31 to 35 are four
five-step accent ramps. Slots 36 upward are semantic aliases pointing back into the first two
groups; four of them repeat the primitives and the neutral ramp exactly. A theme editor changes a
ramp and every component reads an alias. Three further colours drive the hero and are declared
separately, because they are consumed by the field rather than by any component: a mid, muted blue
inner, a mid, muted blue outer, and a light, vivid cyan. A stacking ceiling and a zoom
compensation factor are published as custom properties too, and only three stacking levels are
ever used in the document.

### Radius, elevation and blur

| Value | What carries it |
|---|---|
| fully round | the ambient circles, the header pill and the login pill |
| generously rounded | every in-section primary button |
| softly rounded | media cards, the mega menu promo image, the statistics card |
| barely rounded | the small floating chips in the hero collage |
| a wide, soft round | the skip-to-content control |

**Elevation.** Four shadows, all cool-tinted rather than black, which is what stops the page
looking like a stock component library. The first two are the floating-panel shadow: a very large
blur with a very large negative spread, so the shadow reads as a soft pool a long way below the
element rather than as an outline around it. The third and fourth are the card shadow.

**Blur.** Two distinct uses that must not be confused. **Layer blur** softens the ambient circles
in the field. **Backdrop blur** frosts the statistics card and the floating chips over whatever is
behind them. One drop shadow is applied as a filter rather than as elevation, on the two
audio-state icons.

### Gradients

Four carry the design and are normative; every other gradient on the page is a per-instance
variation of one of them.

- **The page-length warm wash**, painted behind the hero on one of the field's phases: a vertical
  ramp through near-white warm neutrals with a light, soft amber band at its middle, returning to
  near-white at both ends.
- **The frosted card fill**, used on the statistics card and every floating chip: a diagonal ramp
  from a near-white cool neutral at low strength to a near-white neutral at high strength. Both
  start their first stop at a negative percentage, which is not a mistake; it pushes the darkest
  part of the gradient off the top-left corner so the card never shows a hard corner value.
- **The ambient circle fill**, which is the whole of the field: a radial ramp holding a mid, muted
  blue core, stepping to a slightly deeper mid, muted blue, then dissolving to the page ground; and
  a second radial ramp holding a light, vivid cyan core and dissolving the same way.
- **The multi-source mesh**, painted on the full-bleed call to action band near the foot of the
  home route: four stacked off-centre radial gradients in light, muted blues, the only place on
  the site where four colour sources are composited at once.

Three fade masks are declared as gradients rather than as masks, and are used to dissolve the
bottom or top edge of a media block into the page.

### Blend modes and masks

Two blend modes are in use, both on vector groups inside the hero collage and both rare: an
exclusion blend on sixty groups and a hue blend on sixty paths. Two mask references are attached
to vector groups. They are the only compositing on the site that is not plain alpha, and a build
that omits them loses the metallic edge on two of the collage chips. They are optional.

### Layout grid

At the large window the content column is **1305 units wide with a 68-unit left margin and a
67-unit right margin**, which is a canvas value of 1740 in a 1920 canvas with 90-unit margins; the
one-unit asymmetry is a rounding artefact of the scale factor rather than a design decision.
Section padding at the large window: the generation band is `75px 67.5px 0px`, the solutions band
is `93px 67.5px 90px`, and the header inner is `0px 20px`. The horizontal card gallery uses a
531-unit card at a 553.5-unit pitch, giving a 22.5-unit gutter, and the fourth card starts beyond
the right edge of the window, which is how the gallery advertises that it scrolls.

### Iconography

Every icon on the site is inline vector geometry drawn in the page, not a font and not a file,
which is why they stay crisp at any zoom and why the page has so little to download. Thirty-one
distinct vector groups are needed. The chrome set is a menu chevron, an accordion chevron that
rotates when its row opens, an inline right arrow and its tighter alternate, a long right arrow, a
long left arrow, a diagonal out arrow, an arrow into a line, a plus that rotates into a close
mark, a close mark, an open-in-new mark, a bookmark and a language globe. The media set is a
pause mark, a circled play mark and a solid play mark; the play and pause pair sit at the same
coordinates and cross-fade, so only one is ever at full strength.

The wordmark occupies a 75 by 30 box on the large and medium windows and a 75 by 27 box on the
small one, and is built as the three-letter word `ORB` set in the display family at weight 800,
optically fitted to that box, over a solid ground rectangle of exactly the box dimensions. The
knockout construction is what lets the mark sit on any band ground without needing a light variant
and a dark variant.

The footer's social row is seven link slots, twenty units tall on a thirty-two unit pitch, ink
coloured, each carrying the destination platform's own mark supplied by the implementer and each
with an accessible name that names the platform.

Three captured vector groups are illustrations rather than icons: a 727 by 622 hero collage of
nine primitives, a 998 by 580 browser-window illustration of 70 primitives, and a 246 by 517
phone illustration of 32 primitives. They are drawn procedurally, per the substitution recipes
below.

### The fixed chrome

**The header** is fixed to the top of every route, above everything, on a solid near-white ground
with no shadow and no border.

| Property | Large window | Medium window | Small window |
|---|---|---|---|
| Height | `72px` | `72px` | `54px` |
| Inner padding | `0px 20px` | `0px 20px` | `0px 20px` |
| Wordmark box | 75 by 30 | 75 by 30 | 75 by 27 |
| Navigation | full, seven items | collapsed to a menu control | collapsed to a menu control |
| Right cluster | globe, rule, Log In, pill | pill and menu control | pill and menu control |

The header type does not scale. It is `16px` at weight 400 for every first-level item at every
window, which is why the header looks slightly larger relative to the page on a small window and
is meant to. The navigation carries `Product`, `Solutions`, `Resources`, `Domains`, `Pricing`,
`Orb Studio` and `Enterprise`, in that order; a one-unit vertical rule sits between `Pricing` and
`Orb Studio` and is the only divider in the header, separating the self-serve products from the
professional tier. The right cluster ends with the primary pill, `156 by 40`, fully round, on the
mid, vivid blue, with a near-white label at `16px / 24px`. The login link beside it carries the
same radius with a transparent ground and an underlined label, so the two read as a pair.

**The mega menu.** Three of the seven first-level items open a full-width panel, `1440 by 611` at
the large window, anchored below the header. Each panel is a four-column link region occupying the
first 936 units, a right rail of 504 units on the panel ground, and a promotional strip across the
bottom. Each column carries an eyebrow, a one-unit rule below it, and a list of link groups; each
group is a link over a description in body ink. The vertical rhythm inside a column is exact:
group tops at a 137-unit pitch when the column holds three groups, and at a 113-unit pitch when
the descriptions are shorter.

The Product panel has four columns. CREATION carries `Website templates`, `Website design` and
`Landing page builder`. AI carries `AI website builder`, `AI features` and `Vexel`. BUSINESS
carries `eCommerce site`, `Online portfolio`, `Restaurant website`, `Blog website` and
`Event website`. ESSENTIALS carries `Domain registration`, `Web hosting` and `Business email`.

The Solutions panel has four columns. MANAGEMENT carries `Payment solutions`, `POS`, `Mobile app`,
`Orb Headless`, `CRM system` and `Scheduling system`. GROWTH carries `Email marketing`,
`SEO tools` and `Website analytics`. BRANDING carries `Logo Maker`, `Business Name Generator` and
`More free tools`.

The Resources panel has four columns. EXPLORE carries `Orb Blog` and `Web design inspiration`.
SUPPORT carries `Help Center` and `Hire a professional`. WHAT'S NEW? carries
`Releases and updates`. FEATURED ARTICLE carries one image card, 360 by 245, softly rounded.

The promotional strip is the full panel width, 74 units tall, on the promo strip colour. It
carries a bold title, a right arrow eight units after it, and a description in body ink. On the
Product panel it reads `Business website` with
`Launch a professional site for any type of business.`; on the Solutions panel it reads
`Business management tools` with `Explore all business management and software features.`

All three panels are present in the document at first paint and are hidden by state, not by
absence. They must not be fetched on hover: the panel has to be able to open within one frame of
the pointer arriving. Opening a panel does not lock the page. A panel closes on pointer leave, on
the Escape key, and on focus leaving its subtree. On the medium and small windows the whole
navigation collapses behind one control and the panels become a stacked accordion.

**The skip control** is a button labelled `Skip to Main Content`, 48 units tall, on a near-white
ground with a label in the primary blue, rendered at zero height and zero strength until it takes
focus. It is the first focusable element in the document on every route.

**The footer** is six columns across the full content width, above a legal row.

| Column | Heading | Links |
|---|---|---|
| 1 | `Product` | `Website Builder`; `AI Website Builder`; `Website Templates`; `Website Design`; `Web Hosting`; `Landing Page Builder`; `Domain Names`; `WHOIS Lookup`; `Domain Name Search`; `TLD List`; `Vexel`; `Orb Studio`; `Mobile App Builder` |
| 2 | `Solutions` | `Business website`; `Online Store Builder`; `eCommerce Website`; `Portfolio Website`; `Blog Website`; `Business Software`; `Business email`; `Free Business Tools`; `Point of Sale`; `Online Booking`; `Logo Maker`; `Orb University` |
| 3 | `Resources` | `Orb Blog`; `Privacy and Security Hub`; `SEO Learning Hub`; `Orb Website Features`; `App Market`; `Website Accessibility` |
| 4 | `Support` | `Help Center`; `Hire a Professional`; `Report Abuse`; `System Status` |
| 5 | `Company` | `Channel Partnerships`; `Press & Media`; `Investor Relations`; `Orb Ventures`; `Accessibility Statement`; `Patent Notice`; `Sitemap`; `Careers` |
| 6 | the wordmark and the company blurb | `About`; `Contact Us` |

The company blurb reads: `Orb is a website builder that lets any business or individual build
their own professional website. By combining design tools and business solutions in one AI-powered
platform, Orb makes it easy for anyone to create without limits and scale confidently online.`
The legal row carries the seven social slots on the left and `Terms of Use`, `Privacy Policy` and
`© 2006-2026 orb.com, Inc` on the right. Column headings read as the group heading role and links
as body standard, both in ink, with the blurb in body ink. The footer collapses to three columns
at the medium tier and to one column of collapsible groups at the small tier.

**Chrome behaviour.** The header is fixed and stays at full strength at every scroll position:
no shrink, no hide-on-scroll and no ground change. Do not add one.

### Motion, moment by moment

Every animation is built from a keyframe list at runtime; the page declares no keyframe block. The
named moments:

- **The ambient rotation**, on the outermost circle group: three fast sweeps separated by two slow
  settles and one very slight settle, once per cycle. It reads as a wheel turned by hand and let
  go, three times a cycle, rather than as a motor.
- **The colour cycle**, shared by every circle on one clock: hold a colour for a long plateau,
  step to the next in a fraction of that, hold again, step again, and return to the first. Keep
  the plateau-to-step ratio at roughly seven to one. A build that interpolates smoothly between
  three colours produces a muddy wash; the plateaus are what produce three distinct moods.
- **The soft drift** and **the strong drift**, at four different durations across the seven
  circles so no two are ever in phase. Every excursion is a multiple of one grid step, which is
  why the movement never looks random.
- **The reveal from below**: a clip opens upward while the element travels up into place.
- **The reveal fade**, in a long variant and a short one.
- **The reveal wipe**: strength snaps on, then a clip rectangle wipes from zero width to full.
- **The word cycle**: a masked stack steps up one line at a time through seven entries, the first
  and last identical so the loop is seamless.
- **The breathe**: the outer collage chips travel a little sideways and back.
- **The marquee**: the content is duplicated once and slides by exactly half its width, so the
  halfway point is seamless.
- **The gradient drift**: a painted gradient travels sideways and back.
- **The flip**: a card turns a full revolution on one axis.
- **The gallery card entry**: a card grows from about a third of its size to full.

Seven durations account for everything the stylesheet declares, and the runtime timelines add
their own. The rule that matters is the two-speed rule: anything a visitor triggers resolves
within `300ms`, and anything the page does by itself runs at `3000ms` or slower. There is nothing
in between, and that gap is what makes the page feel responsive and calm at the same time.

The dominant declared transition in the reference is `all`, on thirty thousand elements. That is a
platform default rather than a design decision and must **not** be reproduced: it is the single
largest avoidable cost on the page, and naming the properties instead is also what stops focus
rings animating. Four declarations carry every state change that is actually visible: the standard
control press, which moves a transform quickly and a strength more slowly; the image and chip
hover, which moves strength and a filter together; the delayed panel fade; and the panel itself.
Three more are plain: a visibility pair, a maximum-height change for the accordion rows, and a
background colour change with and without a delay.

No reduced-motion handling exists in the reference. That is a defect, not a design, and this build
fixes it under the rule stated in `## UI/UX notes`.

### Scroll and viewport behaviour

Very little on this page reacts to scrolling, which is why it feels solid rather than gimmicky.
Exactly three groups change with scroll position: the ambient field's circles change their blur,
their painted fill, their strength, their backdrop blur and their shadow; the vector collage
changes its clip, its filter and its mask; and six section cards change their transform and their
strength. Nothing else moves. There is no pinned band, no scrubbed timeline, no progress custom
property and no root class that changes with scroll.

**The section reveal** is sampled at two discrete states, not as a continuum: the card travels
down by a small offset while its strength changes from zero to roughly three quarters. The end
state is deliberately short of full strength, so the cards sit at about three quarters and the
band ground shows through them. The reveal is triggered by intersection, runs once, and uses the
reveal from below or the reveal fade.

**Scroll mechanics.** Native scrolling only: no smoothing layer, no transform-based scroller and
no scroll hijack. Anchor navigation from the skip control lands its target below the fixed header,
which needs a scroll margin equal to the header height on every anchor target. The horizontal
gallery scrolls horizontally inside its own region and never propagates that scroll to the
document.

**Document heights**, for the record: the home route is 14640 units tall at the small window,
20056 at the medium and 17749 at the large; the point of sale route is 12662 at the large. The
medium window is the tallest by a wide margin, because the four-across card gallery becomes
two-across before it becomes one-across.

### The ambient colour field

This is the one expensive thing on the site and the only reason it looks different from every
other builder's marketing page.

**Seven oversized boxes with fully rounded corners, layered behind the hero, each carrying either
a flat colour or a radial gradient, each heavily blurred, each running two independent timelines:
a slow colour and rotation cycle and a faster positional drift.** Four of the seven start above
the top of the document, two start left of the origin, and the largest is very nearly the whole
window. The field is much larger than what can be seen, which is the point: only the middle of
each circle is ever visible, so no edge is ever shown and the whole thing reads as light rather
than as shapes. Three of the seven carry a radial fill with a layer blur; four carry a flat ground
at four-fifths strength with no blur. The group sits behind a warm or cool full-bleed wash and the
hero text sits on top of it at full contrast against the page ground.

**The cycle.** Every circle shares one clock. The two timelines that carry a ground move through
three phases: phase A is a light, vivid cyan on both; phase B is a light, soft amber on one and a
light, soft magenta on the other; phase C is a light, muted green on one and a light, vivid green
on the other. Both start and end on the same cool phase, which is why every transition passes
through a common colour and the page never looks like two unrelated designs.

**The drift** is quantised to a grid and its maximum excursion stays under two percent of the
element's own size. Above that the circles read as objects moving; below it they read as light
shifting.

**Cost control.** The field is composited on its own layer and never triggers layout. Only
transform, strength and the two paint properties are animated; no geometry property is animated.
The field pauses entirely when the hero leaves the window and resumes on re-entry, because nothing
behind the fold has any reason to keep drawing, and it pauses when the document is hidden. Below
the medium breakpoint it renders four circles rather than seven and keeps the total blurred area
under one and a half window areas. If the field costs more than a third of a frame on a mid-range
device at the medium tier, reduce the count before reducing the blur: fewer circles at the same
blur looks identical, and the same circles at less blur does not.

**It needs no accelerated pipeline.** Seven absolutely positioned rounded boxes inside a clipped
container spanning the hero, layered largest at the back, with a full-bleed wash over the group at
low strength and the page ground behind everything, produce the same result. Every feature of the
field is a gradient, a blur or a transform, and all three are native. Where an accelerated
drawing surface is available it is an optimisation; where it is not, the box-based version must be
visually interchangeable at a glance, which is achievable precisely because the field has no sharp
features.

### The home route, band by band

**Band 1, the hero.** A centred headline `Create your future on the leading website builder`,
whose box is exactly eighty percent of the window and which wraps to two lines at the large and
medium windows and three at the small. Below it the centred sub-headline
`Orb Cadence is where you create a site that means business.`, then the primary button
`Get Started` on the ink ground, generously rounded, with asymmetric padding, 34 on the left and
10 on the right, because the label is optically centred against a trailing chevron slot that is
empty on this button and filled on others. Below that the legal caption
`Start for free. No credit card required.` Then the collage, full bleed, then the media control,
then the statistics card.

**Band 1, the collage.** A fixed composition of overlapping product screenshots, floating chips
and one video, not a carousel and not a scroll effect. Its members carry the barely-rounded, the
softly-rounded and the smallest radii, the frosted fill and the backdrop blur, and the breathe
timeline on the outer chips. One member is a muted, non-looping video with a play and pause
control that cross-fades between the two marks.

**Band 1, the statistics card.** A frosted card floating over the collage, softly rounded, with a
backdrop blur, the diagonal frosted fill and the card shadow. It carries `300M+` over
`Sites built on Orb` and `90K+` over `Sites created daily`, separated by a one-unit vertical rule
in the statistic divider colour. The two numerals sit one unit apart vertically. That is optical
alignment for two different glyph sets, not sloppiness, and a build that aligns them
mathematically will look very slightly wrong.

**Band 2, the generation band.** Standard band header. Headline
`Website creation, as natural as thinking`. Right rail: `Experience Orb Cadence, the ` then the
link `AI website builder` then ` that lets you flow between instant generation and hand-crafted
design.` Button `Get Started`. Two ambient blobs of the same size are mirrored about the window
centre, both running off the edge, both carrying the page-length warm wash. This left-headline,
right-rail-with-button arrangement is the standard band header and recurs in nine bands.

**Band 3, the solutions accordion.** Group heading, a lede
`Tap into a stack of ready-to-go business tools so your vision can grow and evolve in any which
way.`, headline `Solutions to fuel every business move`, and a `Get Started` button. Below it
eight rows separated by one-unit hairlines in the muted rule colour, with exactly one open at a
time and the first open on load. Each closed row shows its title and a right arrow at the far
right of the content column; the open row grows to fit a media block, softly rounded, and each
row's media block carries a `Send` control.

| Row | Title | Body | Link |
|---|---|---|---|
| 1 | `eCommerce` | `Sell products, services and memberships from one dashboard, zero plugins. And keep your business growing with specialized AI agents.` | `Create an eCommerce Website` |
| 2 | `Scheduling` | `Manage appointments, staff and client memberships from one central scheduling hub and turn every open slot into a confirmed booking.` | `Get Booked Online` |
| 3 | `Lead management` | `Capture every inquiry and manage your entire sales pipeline, from price proposals to paid invoices, so you never miss a chance to close a deal.` | `Manage Your Sales Pipeline` |
| 4 | `Portfolio` | `Display your work with a polished, easy-to-manage portfolio, making a website that wins clients and establishes your credibility.` | `Build A Portfolio Website` |
| 5 | `Blog` | `Turn your expertise into a blog that grows your community, with AI to help you plan, write and publish every post.` | `Start Your Blog` |
| 6 | `Online courses` | `Sell your own online programs and easily manage participants to boost your professional image and build a new income stream.` | `Create Your Own Course` |
| 7 | `Events` | `Promote and manage any online or in-person event. Sell tickets, track RSVPs, manage your staff and always give your guests a smooth experience.` | `Sell Event Tickets Online` |
| 8 | `Payments` | `Get paid right on your site through leading payment methods, and offer subscriptions and pricing plans to fit your business goals.` | `Accept Payments Online` |

Each row heading is a real heading element at the card heading role and the control is that
heading's own button, so assistive technology gets both the structure and the state. The height
change animates.

**Band 4, the template rail.** Headline `Website templates for any industry`, supporting line
`Orb's free website builder offers 2000+ business ready website templates that you can customize
manually or with AI.`, button `Get Started`, category link `All eCommerce Templates`, and one
preview card reading `T- Shirt Store` with a `View` control. Seven category chips: `eCommerce`,
`Portfolio`, `Business`, `Landing page`, `Blog`, `Real estate`, `Weddings`.

Seven category links: `eCommerce website templates`, `Portfolio website templates`,
`Business website templates`, `Landing page website templates`, `Blog website templates`,
`Real estate website templates`, `Weddings website templates`.

Thirty-five template links: `T- Shirt Store eCommerce website template`,
`Pottery Store eCommerce website template`, `Home Goods Store eCommerce website template`,
`Beauty Store eCommerce website template`, `Toy Store eCommerce website template`,
`Digital Artist Portfolio website template`, `Photographer Portfolio website template`,
`Architecture Firm Portfolio website template`, `Content Writer Portfolio website template`,
`Interior Design Company Portfolio website template`,
`Cooking School Business website template`,
`Life Insurance Agency Business website template`, `Consulting Firm Business website template`,
`Dentist Business website template`, `Business Consultant Business website template`,
`Personal Blog Blog website template`, `Running Blog Blog website template`,
`Travel Blog Blog website template`, `Food Blogger Blog website template`,
`Swimming Trainer Landing page website template`, `Start Up Landing page website template`,
`App Landing Page Landing page website template`,
`Product Landing Page Landing page website template`, `Lead Gen Landing page website template`,
`Wedding Invitation Weddings website template`, `Wedding Venue Weddings website template`,
`Wedding Photographer Weddings website template`, `Wedding Planner Weddings website template`,
`Real Estate Agent Real estate website template`,
`Real Estate Project Landing Page Real estate website template`,
`Real Estate Consultant Real estate website template`,
`Real Estate Landing Page Real estate website template`,
`Property Manager Real estate website template`.

`Personal Blog Blog website template` and `Wedding Invitation Weddings website template` each
appear twice in the source copy. Reproduce both links in the rail, because they are in the
measured copy, and treat them as a content bug in the source data by deduplicating them in the
library, which is why `35` links resolve to `33` distinct templates.

**Band 5, the customisation gallery.** Headline `Radical customization, remarkably simple`, lede
`Combine the power of AI with hands-on creative control, so every choice is yours and every detail
feels like you.`, button `Get Started`. Four cards in a horizontal gallery, each a full-bleed media
block above a heading and a paragraph. The fourth card begins beyond the right edge of the window,
which is how the gallery advertises that it scrolls, and the rail advances as the page scrolls
past it.

| Card | Heading | Body |
|---|---|---|
| 1 | `Vibe-style creation` | `Describe what you want in your own words and watch it instantly take shape.` |
| 2 | `Drag and drop freedom` | `Move and adjust any element with pixel-level precision on a totally fluid canvas, no limits, just your vision.` |
| 3 | `A library of possibilities` | `Explore 1000s of free components, graphics and animations to make your website unique.` |
| 4 | `Define your brand` | `Choose fonts, colors and styles and watch them ripple through your site, so you always stay on brand.` |

**Band 6, the assistant band.** A field of sixteen floating prompt chips over the ambient wash,
carrying the frosted fill, a backdrop blur and the softly-rounded radius, floating on the soft and
strong drift timelines. The chips read: `How do I get more traffic?`,
`Set up a new shipping option`, `Set up a welcome email series`, `Create a pay link`,
`Match image to the page design`, `Improve the site's SEO`, `How can I connect my domain?`,
`Add a page for a pop-up`, `Automate booking confirmation emails`, `Draft a new blog post`,
`Draft a new blog post`, `Create a $250 pay link`, `Create a new membership plan`,
`Make my site look more modern`, `Make my site look more modern`,
`Fix the spacing in this section`. `Draft a new blog post` and `Make my site look more modern`
each appear twice, and unlike the template names those duplicates are intentional: the chips are a
drifting field and repetition at different positions reads as volume rather than as error. Keep
them.

The heading is set twice. The accessible heading reads `Meet Iris, your unfair advantage.` The
visible stem reads `Meet Iris, your` followed by a masked stack cycling seven entries in order:
`unfair advantage`, `personal AI agent`, `expert web designer`, `business strategist`,
`hands-on collaborator`, `intuitive guide`, `unfair advantage`. Seven entries, six visible
transitions, the first and last identical so the loop is seamless. The cycling stack is hidden
from assistive technology and the static heading is exposed; a build that animates the accessible
name produces a heading that changes six times a cycle in a screen reader, which is the defect the
two-copy construction exists to avoid. Button `Get Started`.

**Band 7, the foundations accordion.** A pale blue band. Headline
`Build your website on unshakeable foundations`, lede `Our free website builder handles the heavy
lifting so your site stays fast, smooth and always at peak performance.`, button `Get Started`.
Four rows, in the same accordion pattern:

| Row | Copy |
|---|---|
| `Reliability` | link `Multi-cloud hosting` then `that guarantees 99.99% uptime and lightning-fast load times give your site visitors a consistently smooth experience.` |
| `Security` | link `Enterprise-grade security` then `, data encryption and full-time threat monitoring keep your site, and your customers, safe around the clock.` |
| `Expert core` | link `Tech SEO` then `and accessibility standards are engineered into your site's DNA so you get seen by search engines and users more easily.` |
| `Functionality` | link `Built-in features` then `work together seamlessly, so your business runs uninterrupted without the hassle of configuring everything yourself.` |

The open row carries a media block on the right showing a numeric readout over a green and blue
wash.

**Band 8, the domain search.** Headline `Create a website, get the perfect domain to match`. A
fully round field on a near-white ground, placeheld `Type the domain you want`. A fully round
button labelled `Search` with a trailing long right arrow, on a mid, vivid blue that is a
different blue from the header pill; this is the one place on the site where two different blues
are used deliberately. Caption: `Get a ` then the link `custom domain` then ` free for one year
with the initial purchase of an annual ` then the link `Premium plan` then `.` The field and the
button stack on the small window and sit side by side above it.

**Band 9, the analytics band.** Standard band header. Headline
`Spot the gaps, grab the opportunities`, lede `Get website analytics and actionable insights to
optimize your business, and track behavioral trends of first time visitors and returning
customers.`, button `Get Started`. Then a marquee of eight capability chips, duplicated once and
translated by exactly half its width: `Subscriptions`, `Marketing performance`,
`Traffic & behavior analysis`, `Sales tracking`, `Customer insights`, `Real-time analytics`,
`Benchmarks report`, `Booking analytics`. The duplicate is the same eight chips in the same order,
hidden from assistive technology, and the marquee pauses on hover and on focus within it.

**Band 10, the operations accordion.** A pale blue band. Headline
`A better way to run your day-to-day`, lede `Streamline workflows, manage customers with built-in
CRM and keep your business moving, without missing a beat.`, button `Get Started`. Three rows:
`Custom automations` with `Automate tasks across every area of your business, so you can focus on
strategy instead of busywork.`; `Contact management` with `Capture visitor and customer data into
one database, manage new leads, and use smart segmentation to target the right people.`;
`Unified inbox` with `Unify site chat, forms, email and social media into a single messaging hub
so you never miss an opportunity.` The open row shows the browser-window illustration on the
right.

**Band 11, the marketing gallery.** Standard band header. Headline
`Turn first click into repeat visits`, lede `Increase your online visibility, drive traffic and
fuel growth with integrated SEO and marketing tools, built for every stage of your business.`,
button `Get Started`. Five cards in the same geometry as the customisation gallery:

| Card | Body |
|---|---|
| `GEO and AI visibility` | `Track where and how LLMs mention your brand, and get actionable insights to increase your reach across today's leading AI platforms.` |
| `Social media` | `Manage your socials without bouncing between platforms. Use AI to plan, create and publish content that keeps your audience engaged and your brand consistent.` |
| `Google and Meta ads` | `Run your Google, Facebook and Instagram ads from one place. Grow your business with cross-channel campaigns, driven by AI insights.` |
| `Email marketing` | `Create, send and track polished email campaigns effortlessly with AI-powered creation and total custom control.` |
| `SEO` | `Rank higher on search engines with an SEO assistant that pinpoints what's holding you back and delivers ongoing recommendations.` |

**Band 12, the surfaces band.** Standard band header. Headline `Manage it all, wherever you are`,
lede `From big picture to finest detail, get total visibility and control of your business on any
device, at any time.`, button `Get Started`. Two unequal cards side by side: a tall portrait card
carrying the phone illustration, headed `Owner App` with `Stay connected to every moving part and
act on what matters most, in real time, right from your phone.`; and a wide landscape card
carrying the browser-window illustration, headed `Dashboard` with `One central hub that brings
everything into focus so you always know what's happening and what to do next.`

**Band 13, the six steps.** Standard band header with two controls, the primary button
`Get Started` and a secondary `Learn more` link. Headline `How to create a website for free`,
lede `Follow these 6 simple steps to create a website today.` Then six numbered steps labelled
`(01)` to `(06)`, each a title at the feature heading role over a paragraph with inline links.

| Step | Title | Body |
|---|---|---|
| `(01)` | `Define your website goals` | `Identify your needs and map out your audience. Whether you're launching an ` + link `eCommerce store` + ` or ` + link `starting a blog` + `, your goals shape your site structure, pages, and the message` |
| `(02)` | `Choose a free website builder` | `Find an all-in-one web creation platform that combines AI tools, ` + link `templates` + `, design features and ` + link `free hosting` + ` so you can create, manage and launch your site faster, no technical skills required.` |
| `(03)` | `Pick a domain name` | `Choose a ` + link `domain name` + ` that reflects your brand and is easy for people to remember. You can start with a free Orb domain and upgrade to a custom one when you're ready to take the next step.` |
| `(04)` | `Create and customize` | `Start with a prompt or a template on an ` + link `AI website builder` + `, then customize using drag and drop or vibe-coding. Adjust layouts, colors, fonts, images and content to match your brand.` |
| `(05)` | `Optimize for SEO and mobile` | `Make your site mobile-friendly and easy to find. Good ` + link `SEO` + ` starts with page titles, meta descriptions and alt text, structured so both visitors and search engines understand your site.` |
| `(06)` | `Publish and grow your website` | `Once your site looks good, publish it and go live. Then use built-in marketing tools, integrations and analytics to drive traffic, engage visitors and grow your online presence.` |

At the small window the steps are two per row, with `(01)` and `(02)` on the same line at the left
and right edges of the content column. Do not stack them.

**Band 14, the showcase.** Eight named customer sites as chips over a field of scattered
photographic tiles at varied sizes and radii, one of them circular, floating on the drift
timelines. The eight names: `Kestrel`, `Marielle Aveline Dance`, `Ivory & Interval`, `Vela Tov`,
`Fork n' Frame`, `Cedar and Sage`, `Camille Paulsen`, `Devin Roche`. Centred over them: the
headline `You're in good company`, the lede `Millions of sites already run on Orb.`, and a
secondary button `Explore Sites`.

**Band 15, the closing call to action.** A full-bleed band carrying the multi-source mesh gradient
and nothing else but a centred headline at the sub-headline role,
`This is what ready feels like.`, and the primary button `Get Started`. The mesh is the visual
bookend to the hero: the page opens on a wash of coloured light and closes on one.

**Band 16, the frequently asked questions.** Headline `Website builder FAQs`. Eight rows in the
accordion pattern, all closed on load, with a plus mark rotating to a close mark:
`What is a website builder?`, `Is it easy to build a website?`,
`How do I choose the best website builder?`, `What types of websites can you build on Orb?`,
`How much does it cost to build a website?`, `Does my free website come with hosting?`,
`How can I connect a domain to my website?`, `How can I optimize my site for SEO on Orb?`

The first answer reads: `A website builder is a platform that allows anyone to create a website
without any coding knowledge. The best website builders offer drag and drop editing, AI-powered
tools and customizable ` then the link `website templates` then `, handling everything you need
from design to hosting and even securing a domain. Orb offers an intuitive website builder that
combines vibe coding with freeform drag and drop, and ready-to-use business solutions.` The other
seven answers were never captured and must be written; each is a real answer to its own question
and each is present in the document at first paint.

**Band 17, the footer.** As specified in the fixed chrome above.

### The point of sale route, block by block

**The hero.** Headline `One omnichannel point of sale solution`, left aligned, at `67.5px / 81px`.
Right rail `Run and grow your entire business, from taking payments in person and online, to
managing inventory, bookings and more, all with Orb's powerful POS.` Primary button
`Talk to Sales` on the ink ground, secondary link `Shop POS` with a trailing arrow. A product
image runs the full content width below, and an availability caption runs the whole content width,
centred: `Orb POS is currently available to U.S.-, Canada-, and U.K.-based users (except Northern
Ireland) connected to Orb Payments. To accept payments, get an Orb Premium plan that supports
payments.`

**The dark band.** A near-black ground with the product photograph bled into it. Headline
`Unify in-person and online sales with Orb POS software` in near-white. Paragraph `Control all
your sales seamlessly with our powerful Point of Sale solution, every online and in-person sale
you make automatically syncs with your Orb dashboard in real time. Keep track of in-person and
online transactions easily with analytics, tax reports, order history and more, from one
dashboard.` The primary button here is on a near-white ground with an ink label; the secondary
link is transparent with a near-white label.

**The feature grid.** Headline `Succeed with our advanced Point of Sale features`. Eight features,
each a heading over a paragraph, with a `Show more` control revealing the last rows. The paragraph
type here is one step below the home route's body standard: the product route sets its supporting
copy a step smaller than the marketing route does, throughout.

| Feature | Body |
|---|---|
| `Omnichannel solution` | `Sell wherever is best for you, in-person, online via your ` + link `eCommerce site` + ` or social media. ` + link `Take payments` + ` in your store, salon or gym and on the go at your next pop-up.` |
| `Integrated payments dashboard` | `Control your business transactions right from your dashboard with Orb Payments. Review payments, handle refunds, schedule payouts and more.` |
| `Ready-to-go software` | `Orb POS hardware comes with its software pre-installed. Just plug it in, log in to your Orb account and start selling, no need for any third-party setup.` |
| `Synced inventory` | `Manage your inventory for both your online and in-person sales from one place. Each sale you make automatically syncs with your dashboard.` |
| `Unified reporting` | `Track your sales, taxes, employee reports and more for online and in-person sales, conveniently from one place.` |
| `Built-in marketing tools` | `Attract new customers with built-in tools and third-party apps. Encourage return customers with a personalized checkout, discounts and loyalty rewards.` |
| `Robust infrastructure` | `Set your business up for growth with the technology that powers over 282 million Orb users. Help protect your business with our best-in-class security.` |
| `Orb customer support` | `Get POS support from Orb experts. Contact Customer Care from your POS tablet, computer or mobile.` |

**The three hardware blocks.** Section headline `POS systems tailored to your business`. Three
full-width blocks, each a large product name, a paragraph and two controls. `POS Register`:
`Accept in-person payments for your products and services with our ` + link `POS Register` + `.
Manage a unified product catalog, calendar, appointments and reporting for both your in-person and
online sales right from your Orb dashboard. For sales on the go, simply grab our ` + link
`Mobile Card Reader` + `.` `Orb POS Go`: `Effortlessly sell products and services in your business
or on the go. Our easy-to-use handheld device offers the convenience of a stand-alone device as
well as the option to connect to a laptop or POS register. Start offering a suite of payment
options and easily manage your sales.` `Mobile Card Reader`: `Sell in person at pop-ups, markets,
festivals and more with our compact ` + link `Mobile Card Reader` + `. Offer secure, contactless
sales for event tickets, products and services no matter where you are with this sleek device.
Together with our Orb app, your phone will transform into a mobile point of sale you can use on
the go. Every in-person and online sale automatically syncs with your dashboard so it's seamless
to track from one place.` The third block sits inside a pale green card on a black ground, inset
from each side with the black band running behind it.

**The hardware chooser.** Headline `Create your bespoke POS hardware solution`, right rail
`Choose the hardware that works best for your business. With Orb POS Register, sell in store and
online, then manage all sales from one dashboard. For services, you can opt for our Orb POS Go.
When on the go, simply grab our Mobile Card Reader.`, primary button `Explore POS Hardware`, and
four product cards in a row on a warm neutral ground: `POS Register`, `Mobile Card Reader`,
`POS Go`, `POS Accessories`.

**The six connection steps.** Headline `How to connect POS to your business with Orb`, lede
`Follow these 6 steps to connect Orb POS. Orb Point of Sale is currently available to users based
in the U.S., Canada and U.K. (except Northern Ireland) who are connected to Orb Payments. To
receive payouts from Orb, complete your Orb ` + link `Payments verification.` Six numbered steps
in the same construction as the home route's, but with the numeral rendered as a separate element
above the title rather than beside it: `Get started with Orb`, `Set up Orb Payments`,
`Buy your POS system`, `Get a POS Plan`, `Set up Orb POS`, `Start selling`.

**The tap-to-pay band, the learn-more row and the questions.** Headline
`Accept payments quickly with your phone`, lede `Start getting paid immediately by activating Tap
to Pay on your mobile phone with the Orb app, no extra hardware is needed.` Two cards:
`Tap to Pay on iPhone` with `Once you're connected to Orb Payments, use your iPhone to accept
contactless payments from debit and credit cards, Apple Pay, Google Pay and other digital wallets,
no additional hardware needed.`; and `Tap to Pay on Android` with `Take swift payments on Android
phones with Tap to Pay. Simply connect your account to ` + link `Orb Payments` + ` to offer this
convenient payment solution.` Controls `Connect Tap to Pay` and `Discover more`. A three-link row
headed `Learn more about POS for your business` carrying `How much does a POS cost?`,
`How to start a business` and `eCommerce payment processing options`. A questions accordion headed
`POS system FAQ`, whose first question is `What is a POS (point of sale)?` answered `POS is a
system that allows you to accept payments from your customers when they are making a purchase. Orb
POS offers multiple combinations of POS hardware and software, ranging from our ` + link
`POS Register` + ` to our compact ` + link `Mobile Card Reader` + ` that connects to our mobile
app. Therefore, you get full freedom to manage your business by selecting a POS system tailored to
you.` The second question is `Which POS system should I choose for my business?`

This route shares everything above with the home route unchanged: the same chrome, the same
scaling model, the same type scale, the same radii and the same motion vocabulary. **Two ambient
boxes are present but the full field is not.** A product route gets the design system and not the
signature effect, which is a deliberate hierarchy and must be kept: if every page had the field,
no page would feel special.

### The not-found route

One window tall. An eyebrow reading `ERROR: PAGE NOT FOUND` at the group heading role, in ink,
all capitals, left aligned at the content margin. Below it a display numeral `404`, roughly 230
units tall at weight 400. Below that the line `This page isn't available.` at the sub-headline
role. Then a generously rounded button on the ink ground with a near-white label reading
`Go to orb.com`. On the right half, six loose primitives, unaligned to any grid: a rounded square
rotated slightly, a long rounded capsule on a diagonal, two circles of different sizes, a small
rounded square with a glyph in it, and a large arrow cursor. Fill them from the four accent ramps,
one primitive per ramp plus two neutrals. This is the one place on the site where saturated flat
colour is correct.

### Component inventory and client state

Every one of the seventeen bands is assembled from these seventeen components and nothing else. A
marketing site of this size should not have a hundred components.

| Component | Used by | Key properties |
|---|---|---|
| `AmbientField` | the hero | phase, palette set, paused |
| `SiteHeader` | every route | active panel, collapsed |
| `MegaPanel` | the three panels | columns, promo |
| `BandHeader` | nine bands | headline, lede, primary control, secondary control |
| `PrimaryButton` | everywhere | tone, size, trailing icon |
| `Accordion` | four bands | rows, open index, single-select |
| `HorizontalGallery` | two bands | cards, pitch, gutter |
| `MediaCard` | three bands and the chooser | media, heading, body, ratio |
| `FrostedCard` | the statistics card and the chip field | fill, backdrop blur, shadow |
| `ChipField` | the assistant band and the showcase | chips, drift set |
| `WordCycle` | the assistant band | phrases, period, static label |
| `Marquee` | the analytics band | items, period, paused |
| `FilterRail` | the template rail | categories, items, selected |
| `DomainSearch` | the domain band | value, state, result |
| `StepList` | both step bands | steps, numeral placement, columns |
| `Collage` | the hero and the not-found route | members, drift set, media control |
| `SiteFooter` | every route | columns, social, legal |

Six pieces of client state exist on the marketing surface and everything else is static: the open
mega panel, the open accordion row (one per accordion), the selected template category, the
gallery scroll offset (one per gallery), the domain query and its result, and the field's phase
and paused flag. None of them is persisted. There is no global state container and no client-side
store; a marketing surface that needs a state library has been over-built. The one decision that
outlives a navigation is the visitor's answer about non-essential measurement, and it lives in its
own storage.

One generated class per styled element, plus one stable semantic class of the form `ui-<role>` for
anything an automated integration needs to select. The reference emits four class names per node
across thirty thousand nodes, which is the single largest contributor to its document size; do not
reproduce that.

### Responsive reflow

| Band | Large | Medium | Small |
|---|---|---|---|
| Standard band header | headline left, rail right | headline over rail, both left | stacked, full width |
| Solutions accordion | row title left, body and media right | row title over body, media below | stacked, media full width |
| Template rail | four across | two across | one across, swipeable |
| Customisation gallery | four across, fourth off-screen | two across | one across |
| Six steps | three across, two rows | two across, three rows | two across, three rows |
| Surfaces band | two unequal cards side by side | stacked | stacked |
| Footer | six columns | three columns | one column, each group collapsible |

The hero's headline is 87 percent of the window at the small band, 87 percent at the medium and 80
percent at the large; the margin opens up only on the largest band, which is where the field needs
room to be seen. The line-height ratio changes across bands and is not a scaling artefact: `1.1`,
`1.0`, `1.2`. The medium band sets the headline solid, because at that canvas size over three
lines a looser setting would push the button below the fold. The wordmark shrinks only at the
small band and moves four units left.

### Drawing everything from code

No image, video, vector or font file is shipped other than the two font files.

- **The field.** Seven absolutely positioned boxes inside a clipped container spanning the hero,
  at the rectangles given above, each with its radius, fill, blur and timelines. Four carry a flat
  ground at four-fifths strength; three carry the radial gradients with a layer blur. Layer them
  largest at the back, put a full-bleed wash over the group at low strength to unify them, and put
  the page ground behind everything. Below the medium breakpoint use four boxes.
- **Grain and tonal texture.** Where the reference used a photographic ground for a card, use a
  generated grain: an inline vector filter as a data reference, turbulence with four octaves for a
  fine grain, a colour matrix with saturation removed to kill the colour speckle, and the result
  composited at a few percent strength over the flat ground, tiled.
- **Photographic media.** A canvas generator keyed by a seed derived from the node identifier. For
  each placeholder: fill with a two-stop linear gradient between two palette slots chosen by
  hashing the seed, overlay two off-centre radial gradients at low strength using the mesh
  construction, apply the grain, and round the corners to the radius the slot declares. For the
  product screenshots specifically, which read as small interface mock-ups, draw a chrome bar with
  three dots, a content area with three or four rounded rectangles at the neutral slots, and one
  accent rectangle. Four palette pairs drive the generator: a cool pair, a warm pair, a fresh pair
  and a bold pair.
- **The three illustrations.** The browser window is a rounded outer rectangle, a title bar in a
  dark neutral, a left sidebar with a vertical gradient, and content rows drawn as short rounded
  bars in a light neutral. The phone is a rounded outer rectangle, a screen inset, a circular
  element at the upper third, and a grid of rounded bars below it. The hero collage is nine
  primitives: a rotated square, two circles of different radii, and six rounded paths, each filled
  from the palette slots. These are reconstructions from the primitive lists rather than
  reproductions: the result reads as the same composition rather than as the same drawing.
- **The not-found illustration.** The six loose primitives described above, positioned unaligned
  in the right half of the window and filled from the four accent ramps.
- **The social preview image.** Generate it rather than storing one: the page ground, the field
  rendered at a single phase, the wordmark at the measured proportions, and the page title set in
  the display family at a size that fits two lines. Store it as a media derivative so it is cached
  like any other.
- **Video.** The hero video is replaced entirely by the collage and the field. Keep the play
  control: it becomes the trigger for an optional video that is fetched only on interaction. A
  build that ships no video at all satisfies every requirement here.

### Above the fold, and below it

The largest element painted first is the hero headline, not an image and not the field. The field
is painted second and must not delay it. The collage loads after the headline is painted, and its
video loads only on an interaction with the media control, which is why that control exists. Every
media block below the first window is deferred with an explicit intrinsic size, so deferring it
costs no layout movement. The two horizontal galleries render their first two cards and defer the
rest.

## Technical requirements

Serve the whole product from one Node process. Render the routes on the server with
**Remix (React Router 7)** route modules and hydrate them in the browser without re-rendering the
tree, so the document arrives complete and the hero headline, the sub-headline, the primary button
and the first phase of the ambient field are all in the first response. Mount the HTTP API on the
same origin under the `/api` prefix with **Express**. Only the interactive regions carry client
code: the mega panel, the four accordions, the two galleries, the chip filter, the word cycle, the
marquee, the field and the domain search. Persist everything in **PostgreSQL**, reached through
`DATABASE_URL`. Keep every uploaded byte in **MinIO**, the S3-compatible object store, reached
through `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`.
Accounts are email and password implemented by this app, with bearer tokens and hashed passwords;
there is no external identity provider. `GET /api/health` returns `200` once the app is ready.
Log one structured line per request, carrying a request identifier that appears on every line that
request produced, to standard output.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor, and the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything else is
a contract violation.

Read `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`,
`STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` from the environment. Never hardcode a host, a port
or a credential. Both backing services are **already running** and reachable at those variables;
do not download, install, compile or start a copy of either.

**Head metadata.** Every public route carries its own title and its own description, and no two
routes share them. The home route's title is
`Website Builder - Create a Free Website In Minutes | Orb` and its description is
`Get everything you need to build a website your way. Orb's free, easy-to-use website builder
offers 2,000+ templates, built-in AI tools and a custom domain.` The point of sale route's title
is `Point of Sale | Complete POS solution for business | Orb POS` and its description is
`Accept secure in-person payments and manage your entire business with Orb POS systems. Unify
online and in-person sales with our point of sale solution.` The not-found route's title is
`404 Error: Page Not Found | Orb`.

An indexable route carries seventeen head tags: the window declaration
`width=device-width, initial-scale=1`; a generator tag reading `Orb Website Builder`; a
format-detection tag reading `telephone=no`; a toolbar-compatibility tag; the description; the
sharing title and description, repeating the document title and the description; the sharing
image; its width and height, `1200` and `630`; the canonical address; the site name; a type of
`website`; and the three summary-card tags repeating the same title, description and image. The
format-detection and toolbar tags are not decoration: the first stops a phone number in the copy
being auto-linked and restyled, which would break the type scale. Keep both. The not-found route
carries exactly two: the window declaration and the no-index directive, and no sharing metadata at
all.

**The social preview image** is generated rather than stored, at `1200` by `630`, and it must
resolve: a request for the address the sharing image tag declares returns image bytes, on every
public route. The three summary-card tags are named exactly: `twitter:card`, whose value is
`summary_large_image`, `twitter:title` and `twitter:description`, beside `twitter:image`.

**A favicon** is served and declared in the document head on every route.

**No credential, API key or admin token appears in anything the browser downloads.** The object
store's keys, the database connection string and every other secret stay on the server.

**Budgets**, per route, at the medium band, on a cold cache: the document at most 60 kilobytes
compressed; blocking script at most 40 kilobytes compressed; total script to interactive at most
120 kilobytes compressed; the stylesheet at most 30 kilobytes compressed; two font files totalling
at most 90 kilobytes, subset to the Latin range; zero image bytes above the fold, because every
image is drawn from code; and zero video bytes before an interaction. Ship three bundles and no
more: a blocking shell carrying the chrome, the tokens, the router and the field; a route bundle
carrying the bands of the current route; and a deferred bundle carrying the video control, the
galleries' inertia behaviour and the measurement client, loaded after first paint when the browser
is idle.

**Measurement and consent.** No measurement that sets a persistent identifier on the visitor's
device runs before the visitor has answered. The container may load; what it fires may not. That
answer is the one piece of state that survives a navigation.

**Interface conventions**, and they hold on every endpoint without exception. Paths are resource
oriented and identifiers sit in the path. Every request that changes something carries a tenant
scope derived from the caller's own credential, never from the body. Every response carries a
request identifier that appears in every log line that request produced. Lists are cursor
paginated and offsets are not offered at any size. An error is a stable machine code, a human
message, a field path where one applies and a retry hint; no stack trace ever reaches a client.
Time is a timestamp with an offset, never a local time and never a naive string. Money is an
integer of minor units plus a currency code, and there are no floating-point amounts anywhere in
this product.

## Data model

Eight tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not
a secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

### `accounts`

`id`, `email` (unique, lower-cased on write), `password_hash`, `role` (`owner` or `visitor`),
`created_at`.

### `workspaces`

`id`, `account_id` (the owning account), `name`, `region` (fixed at creation and never changed
afterwards), `created_at`. A workspace belongs to exactly one account.

### `sites`

`id`, `workspace_id` (immutable for the life of the site), `name`, `slug` (unique across the whole
product, kebab-case, the label of the free address), `status` (`draft` or `published`),
`template_id` (the template the site was instantiated from, or empty), `domain_query` (the label
the visitor searched at sign-up, or empty), `head_revision`, `live_revision` (empty until the
first publish), `created_at`. The free address is derived rather than stored: it is the slug
followed by `.orbsite.com`.

### `revisions`

`id`, `site_id`, `number` (monotonic per site, starting at `1`), `label` (set on publish, empty
otherwise), `created_at`.

### `media`

`id`, `site_id`, `object_key` (unique), `content_type`, `byte_size`, `alt_text`, `created_at`.
This row records where the bytes are. It never holds the bytes.

### `templates`

`id`, `name`, `slug` (unique), `category` (one of the seven), `rank` (the stable ordering the rail
and the public listing use).

### `domain_registry`

`name` (the fully qualified name, unique), `registry_status` (`available` or `registered`),
`premium`, `price` (minor units per year), `currency`.

### `domain_queries`

`id`, `normalised`, `created_at`. No identifier is attached to a stored query.

### Invariants, stated as properties of the running product

- No two sites anywhere in the product share a slug. Two simultaneous attempts to take the same
  slug must not both succeed: exactly one wins and the other is rejected.
- A site's `live_revision` is empty while its `status` is `draft`, and names a real revision of
  that same site once its `status` is `published`. It never names a revision of another site.
- Two simultaneous publishes of one site must not both succeed in setting a live revision: exactly
  one wins, the other is rejected, and the site ends naming exactly one live revision.
- Two sign-ups with the same email address inside the ten-minute window produce exactly one
  account, exactly one workspace and exactly one site. The second returns the first answer.
- A media row's `object_key` is unique and is exactly the key scheme
  `sites/{site_id}/{sha256_of_bytes}.{ext}`. Uploading the same bytes to the same site twice
  leaves one object and one row.
- Every byte a visitor is served comes from the object store. No byte of an uploaded picture is
  ever read from the app container's filesystem or from a database column.
- A picture belonging to a site whose `status` is `draft` is readable only by the owner of that
  site's workspace. Everyone else, signed in or not, is refused, and the refusal does not disclose
  whether the picture exists.

### Seed data

Three accounts, all with the corpus password. `owner@example.com` owns the workspace
`Kestrel Studio`, which holds two sites: `Kestrel`, slug `kestrel`, `published`, with one picture
whose alternative text reads `Kestrel storefront`; and `Ivory and Interval`, slug
`ivory-and-interval`, `draft`, with one picture whose alternative text reads
`Ivory and Interval studio`. `owner2@example.com` owns the workspace `Cedar Workshop`, which holds
one site: `Cedar and Sage`, slug `cedar-and-sage`, `draft`. `visitor@example.com` owns no
workspace and no sites.

Thirty-three templates across the seven categories, each with a stable rank.

Four registry rows: `orb.com` and `cedarandsage.com` are `registered`; `forknframe.com` and
`velatov.com` are `available` at `1200` minor units in `usd` per year.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

These are the non-goals, stated plainly, so that nobody mistakes an absence for an oversight. The
marketing copy sells every one of them and the build implements none of them.

- **No page editor.** No node tree, no layout object, no fractional sibling ordering, no
  operation set, no session protocol, no presence, no soft locks, no convergence of two people's
  concurrent edits, no persistence of an operation log and no compaction of one, and no undo.
- **No site generation.** No intake, no plan, no compose stage, no streamed build. The whole
  engineering problem of constraining a model to closed sets, and of grounding every fact about a
  business in what its owner actually supplied rather than in what a model recalls, is out of
  scope here.
- **No commerce.** No catalogue, no variants, no inventory and therefore no reservation problem,
  no cart, no order, no payment, no refund, no payout, no double-entry ledger, no tax calculation
  and no dispute handling.
- **No automation.** No triggers, no conditions, no actions, no delays, no durable runs, and no
  per-tenant observability over them.
- **No analytics.** No event collector, no session store, no rollups, no funnels, no attribution,
  no live visitor count, no benchmark reports, and none of the counting problems that go with
  them.
- **No extension runtime.** No third-party code, no manifest, no grant, no server sandbox and no
  browser-side isolation of somebody else's code inside a tenant's own origin.
- **No platform operations programme.** No availability objectives, no error budgets, no
  degradation ladder, no observability stack, no staged rollout, no backup and no recovery
  drill. There is no audit log and no support impersonation session.
- **No published interface versioning.** One current interface, no second major version running
  beside it, and no deprecation window.
- **No asynchronous work of any kind.** Every operation in this product is synchronous: there is
  no job queue, no progress stream, no background worker and no scheduled task.

- One product, many workspaces. A site belongs to exactly one workspace forever; there is no
  transfer operation.
- No page editor and no drag-and-drop canvas. A site is created, named, given pictures, published
  and rolled back, and nothing else. There is no node tree, no layout object, no binding to a
  collection, no theme editor and no collaborative editing session.
- No site generation. The copy sells describing a site in your own words and watching it take
  shape; nothing here generates one.
- No commerce. No catalogue, no variants, no inventory, no cart, no order, no payment, no refund,
  no payout, no double-entry ledger, no tax calculation and no dispute handling. The point of sale
  route sells a card terminal and the product does not have one.
- No automation engine, no triggers, no conditions, no actions, no delays and no durable runs.
- No analytics ingestion, no event collector, no session store, no rollups, no funnels, no
  attribution, no live visitor count and no benchmark reports.
- No extension runtime, no third-party code, no sandbox, no manifest and no application market.
- No custom domain connection. The domain search answers whether a name is free; it does not
  register anything, does not delegate name servers, does not point records, does not verify
  ownership and does not issue a certificate. Every site lives at its free address.
- No outbound email, no verification message, no password reset message and no notification of any
  kind.
- No multi-cloud delivery, no edge cache, no artifact store, no incremental publish and no
  provider failover.
- No native mobile application.
- No external network call at run time. Everything the product needs is inside this environment.
- Every destination in the header and the footer that is not one of the routes named here must
  resolve to an honest placeholder page carrying the chrome and saying plainly that the page is
  not built. A footer of dead links is a worse artifact than a footer of honest placeholders.
- The product must stay responsive with `33` templates, `200` sites and `500` pictures in the
  store.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
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

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{"email", "password"}` | `{"access_token"}` |
| `GET /api/health` | none | a readiness body |
| `GET /api/domains/availability` | `query`, `suggest` | `{"normalised", "exact", "suggestions", "partial"}` |
| `GET /api/templates` | `category`, `cursor`, `limit` | `{"items", "facets", "next_cursor"}` |
| `POST /api/accounts` | `{"email", "password", "domain_query"}` | `{"access_token", "site_id"}` |
| `GET /api/sites` | none | a top-level JSON array of the caller's own sites |
| `POST /api/sites` | `{"name", "slug"}` | the created site |
| `GET /api/sites/{site_id}` | none | one site |
| `POST /api/sites/{site_id}/media` | the picture bytes and `alt_text` | `{"id", "object_key", "content_type", "byte_size", "alt_text"}` |
| `GET /api/sites/{site_id}/media/{media_id}` | none | the picture bytes |
| `POST /api/sites/{site_id}/publish` | none | the site with `status` of `published` |
| `POST /api/sites/{site_id}/publish/rollback` | none | the site with `status` of `draft` |
| `GET /api/published/{slug}` | none | one published site and its pictures |

Field names are exact. A list endpoint returns a top-level JSON array unless the table above says
otherwise. A successful call returns the named resource or shape. An invalid or unauthorized call
is rejected as a client error, never as a server error and never as a silent success. Bearer auth
is carried on everything except login, health, the domain availability query, the template listing,
account creation and the public published-site read.

### No mocks

The named providers are the fact, and the app's own tables and screens can only reflect what lives
in them, never substitute for them. Each of the following is a contract violation:

- an in-memory `media` array, or any picture held in a process variable
- picture bytes written to the app container's filesystem, including a `public/` or `uploads/`
  directory
- picture bytes stored in a database column
- a hardcoded availability answer the app returns to itself instead of reading its registry
- a site that reports `published` without a live revision behind it

The uploaded bytes must live in the object store at their scheme's key for exactly the site that
owns them, and the site's status must be a real stored value, not a screen state.

## Definition of done

A visitor can open the long sales page, search a domain name, see whether it is free, and open a
free account that immediately holds their own named draft site at its own free address. The owner
of that site can sign in, upload a picture, and publish, after which the site and its picture
answer to anybody at the public address. Until they publish, nobody but that owner can read the
picture, whatever address they try. An unknown address renders the product's own not-found page
and says so honestly.
