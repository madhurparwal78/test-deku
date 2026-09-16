# Spatial Studio Portfolio

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, read the studio's argument, open a numbered case study from the index
into its full write-up, and send the studio an enquiry from the contact route,
without hitting an error page. A different stranger, signed in as a reader or
signed in as nobody at all, must NOT be able to reach a case study the studio
has not published yet, by any means: not from a listing, not by typing its
address, and not by fetching its media. The media the studio uploads must live
as real objects in the `minio` bucket at their scheme's key; a copy on the app
container's own disk does not count.

## Overview

This is the showcase site for a small studio that researches and builds
interactive three-dimensional content for the web, sold into three markets:
industry, science and retail. It sells nothing and takes no payment. It states
what the studio does, presents three named product lines as long scrolling
arguments, sets out four service disciplines as long-form text, lists seven
numbered client cases from an index into full write-ups, and gives one email
address, one office address and two social profiles.

The visual proposition is unusual and it is the whole product. The site is not a
page with a three-dimensional element in it. It is a full-viewport
three-dimensional stage that runs behind every route for the entire visit, with
a thin, translucent, blurred layer of typography and panels floating in front of
it. Scrolling moves the stage, not only the page. The stage is on every route
without exception, including the three legal documents and the not-found page.

Behind the public site there is an editorial job. A studio editor drafts a case
study, uploads its cover media and its body media, and publishes it when the
client agrees. Visitors read what is published. Anyone can send an enquiry from
the contact route, and an editor reads it.

Five audiences arrive here. A prospective client with a brief wants proof the
studio can do the specific thing they need, and goes to a product line and then
to contact. A prospective client without a brief wants to know what is even
possible in a browser. Procurement and technical evaluators want evidence of
delivered work at scale, and go to the cases. Recruiters and peers want to see
what the studio's craft looks like, and any route serves them, because the stage
is the portfolio. Legal and compliance readers want the three policy documents.

The genuinely hard part is the draft boundary: an unpublished case study and
every byte of its media must be unreachable outside the studio, on every path
that could reach a published one.

Deliberately not here: no search, no filtering, no tagging, no pagination on the
index, no blog, no news, no comments, no likes, no messaging between visitors,
no language switch, no cart, no pricing, no native application.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| visitor (not signed in) | read every published route; copy the studio email and the office address; send an enquiry; accept or decline the cookie choice | **read a draft case study or its media**, **reach any studio address**, **read any enquiry** |
| `reader` | everything a visitor can, plus see their own submitted enquiries | **read a draft case study or its media**, **reach any studio address**, **read another account's enquiries**, **create, edit or publish anything** |
| `editor` | everything a reader can, plus create, edit, publish and unpublish case studies, solutions and services; upload and replace media; read every enquiry and mark it read; read the page-view log | **nothing further; there is no higher role** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `editor`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open and creates a `reader`. There is no way to sign up as an
`editor`; editor accounts are seeded.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `editor@example.com` | `editor` |
| `reader@example.com` | `reader` |
| `reader2@example.com` | `reader` |

## Core features

### Auth

Email and password, implemented by the app. A successful sign-in returns a
bearer token the client sends on every subsequent request. Passwords are stored
hashed, never in clear. A token expires; an expired token on a protected route
is rejected and the visitor is returned to the sign-in route with the contents
of any form they were filling still in place. Signup is open and always creates
a `reader`, whatever role the request body asks for.

1. Signing in with a seeded email and `deku-demo-pw-2026` succeeds.
2. Signing in with a correct email and a wrong password is denied, and the
   response says nothing about which of the two was wrong.
3. A request to any `/api` route other than sign-in, signup, health, the public
   read routes, the consent route and the enquiry route without a valid bearer
   token is denied.

### The stage

One drawing surface, sized to the viewport, fixed in place, painted behind all
page content, present exactly once per document and on every route.

1. The surface is present on every route listed in `## User flow`, including
   `/terms/`, `/privacy/`, `/cookies/` and the not-found page.
2. A route change swaps the scene inside the surface and does not tear the
   surface down and rebuild it.
3. Scene selection is declarative and readable from the document: the document
   root carries a scene class, and each route root carries its own route name as
   a class, so a route change and a scene change are the same event and cannot
   fall out of step.
4. The surface never receives keyboard focus.
5. Where the scene carries text, that text also exists in the document.

Each route's stage carries its own scene. The home route shows a dark city at
night seen from above and thrown far out of focus, so the lights read as soft
discs, with a polished chrome dome hanging in the upper third that recedes as
the page scrolls, and later a small lit platform with two soft blocks on it. The
first product line shows a dense dark field resolving into a point cloud: a
landscape rendered as fine dots with slender structures standing in it, and a
large word set in the theme ink at low opacity behind the pinned statements. The
second shows a fully lit interior, pale and photographic, with furniture, a
fireplace and a pendant lamp. The third shows a saturated violet field with a
wireframe product hovering in it, the wireframe reading as a mesh cage over a
solid form. The cases index shows the dark out-of-focus field with a saturated
full-bleed colour block arriving behind each case cluster. The case detail shows
the same dark field, with the case's own media playing inside panels rather than
on the stage. The contact route shows a dark globe with its continents drawn as
a fine dot matrix and warm arcs rising off its surface toward a small structure
above the horizon. Services, the legal routes and the not-found route show the
dark out-of-focus field alone.

Two properties hold across all of them. The scene is always thrown well out of
focus except where a single object is the subject. And the scene's own key
colour is allowed to be more saturated than anything the interface owns, because
the interface owns no colour but its one accent.

### Case studies and the draft boundary

A case study has a slug, a two-digit number, a client, a title, a cover clip, a
brief paragraph that opens with the client name as a link and continues in the
same paragraph, between eight and eleven body sections, and a result paragraph.
A body section is an optional media element, an optional media caption, a
heading and a paragraph. A case study is either `draft` or `published`.

1. `GET /api/cases` returns only `published` cases, newest published first, and
   `/cases/` lists exactly those.
2. A `published` case resolves at `/cases/<slug>` and at `/api/cases/<slug>` for
   anyone, signed in or not.
3. **A `draft` case is not readable outside the studio.** It appears in no
   public listing; `/cases/<slug>` and `GET /api/cases/<slug>` for a draft are
   denied to a visitor and to a `reader`; and every media object belonging to it
   is denied to both. An `editor` reads it normally. This is the rule the
   product turns on.
4. Publishing a draft makes all three visible in the same act: the listing, the
   address and the media.
5. Unpublishing a published case returns it to `draft` and makes all three
   unreachable again.
6. Only an `editor` may create, edit, publish or unpublish. A `reader` calling
   the publish endpoint directly is denied and the case's `status` is unchanged.
7. The number is two digits and unique across cases. The sequence runs over all
   cases, not per client: two clients appear twice in the seeded set, at numbers
   `02` and `05` and at numbers `04` and `06`.

### Media in the object store

Every uploaded byte lives in the `minio` bucket named by `STORAGE_BUCKET`,
reached at `STORAGE_ENDPOINT` with `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Bytes live nowhere else: not on the app container's
filesystem, not in a database column.

1. The object key is `cases/{case_id}/{sha256_of_bytes}.{ext}`, for example
   `cases/1/9f2a4c7e18b3d05fa6412c8907de35b1c04e97ab2f6d8130c5e7a94b2f0d63e8.webm`.
2. Uploading the same bytes twice for the same case resolves to one object, not
   two.
3. A media row records its object key, its content type, its byte size, its
   digest, its alternative text and whether it is decorative. The row records
   where the bytes are; the bucket is where they are.
4. Media belonging to a `draft` case is served only to an `editor`. Pick one of
   two mechanisms and be consistent: an authenticated streaming endpoint the app
   owns, or presigned links that expire within five minutes and are never issued
   to a signer who is not entitled to the case.
5. Deleting a case removes its objects from the bucket, not only its rows.

### The three product lines

Three instances of one template, at `/cirrus/`, `/emporium/` and `/facet/`.
`/solutions/` is a redirect to the first of them and is not a listing page.

Each instance carries, in this order: a cover of two short category lines and
the product name; a claim, which is a figure and a sentence or two sentences; a
three-part mechanism, exactly three of heading plus one-sentence body; a feature
run of between six and nine of heading plus paragraph; on two of the three
instances an interactive selector carrying a label, an instruction and three
options; a closing statement of two to four display lines; and the footer call
to action.

1. Each instance carries exactly three mechanism steps. Not two, not four.
2. Each instance carries at least six and at most nine features.
3. The interactive selector is present on the second and third instances only.
4. Selecting one of the three options changes the stage scene's material or
   environment, and the chosen option holds its selected state after the pointer
   leaves it.
5. `/solutions/` redirects to `/cirrus/`, which reports its own title and its
   own content. There is no product index page.

The seeded set: `Cirrus`, category `Data` over `3D Data Visualization`, dark
theme. `Emporium`, category `Retail` over `Virtual Showrooms`, pale theme.
`Facet`, category `Retail` over `Product Showcasing`, pale theme and its own
scene class.

### The four service disciplines

Four disciplines on one page at `/services/`, each reachable by its own anchor:
`/services/#graphics`, `/services/#ui`, `/services/#assets` and
`/services/#cloud`. They are anchors into one route, never four pages.

Each discipline carries an anchor, a heading, a navigation caption and a
navigation sub-caption distinct from the heading, two short promises, an opening
paragraph, exactly four bullets of label plus sentence, an argument paragraph
and a closing paragraph.

1. Each discipline carries exactly four bullets.
2. The heading on the page and the caption in the navigation are different
   wordings for the same thing, and both are kept: the navigation is indexing
   and the page is selling.

The seeded four: anchor `graphics`, heading `3D Web Graphics`, caption
`Real-Time Graphics`, sub-caption `Real-Time 3D Web Graphics`. Anchor `ui`,
heading `Dynamic User Interfaces`, caption `User Interface`, sub-caption
`UI Development`. Anchor `assets`, heading `3D Asset Pipelines`, caption
`Assets Pipeline`, sub-caption `Automated Asset Pipeline`. Anchor `cloud`,
heading `Kubernetes Deployments for Big Data`, caption `Cloud Infrastructure`,
sub-caption `Kubernetes for 3D Data`.

### The cases index

`/cases/` has no heading, no filter, no tags and no pagination. It opens
straight into the first case cluster and runs through them into the footer. That
absence is the design: the index is the work, not a page about the work.

The seeded published set, numbered in one sequence:

| Number | Client | Title |
|---|---|---|
| `01` | `Delta AI` | `Oil & Gas Data Visualization` |
| `02` | `Corvus Europe` | `Virtual Experience Center` |
| `03` | `Modellia` | `HD Point Cloud` |
| `04` | `Flowforge` | `CFD Data Visualization` |
| `05` | `Corvus Europe` | `3D Product Catalogue` |
| `06` | `Flowforge` | `CFD Geometry Pipeline` |
| `07` | `Kessel` | `CAD Viewer` |

An eighth case is seeded in `draft`: number `08`, client `Kessel`, title
`Substation Twin`. It is absent from `/cases/` and from `GET /api/cases`, denied
at `/cases/substation-twin`, and its cover object is denied to a visitor and to
a `reader`.

The home route features the first three of the published set.

### The contact route and the enquiry

`/contact/` opens with the studio's question set in three display lines, carries
the studio email address set at headline size, the office address, a maps link,
the business block, two social links, and the enquiry form.

The email block and the office block are each a copy control: a label sits
invisible and fades in on hover, and activating the control copies the address.
The label is the affordance, and it is the only thing on the site that appears
rather than changing colour. On a touch device both labels are shown
unconditionally. Both controls announce the result of the copy.

The enquiry form takes a name, an email address, an optional organisation and a
message.

1. A submission with every required field present and an email address that
   parses is accepted, stored, and answered with a confirmation in place.
2. An invalid submission is rejected inline, the response names the field that
   failed, and **nothing is written**: a rejected enquiry leaves no row.
3. The form carries an unattended decoy field that a person never fills. A
   submission arriving with that field filled is refused and writes nothing.
4. The same form submitted repeatedly in quick succession from one origin is
   refused after the first, and the refused attempts write nothing.
5. An `editor` reads every enquiry at `/studio/enquiries`, newest first, and
   marks one read. A `reader` calling the enquiry list endpoint is denied. A
   `reader` sees only their own submitted enquiries.

### The legal documents, the cookie choice and the not-found page

Three legal routes on one template at `/terms/`, `/privacy/` and `/cookies/`.
They carry the full chrome, the full stage and the full motion system. A build
that renders these as plain documents on a flat ground has changed the product,
because a visitor who reaches the small print is still on this site.

1. `/privacy/` states what the product stores about a visitor and how long it is
   kept, and is reachable from the footer of every page.
2. `/terms/` is reachable from the footer of every page and is linked from the
   signup form.
3. A first-time visitor is asked once about non-essential cookies. The notice
   carries the studio's sentence about optimising website performance and
   functionality, a link reading `Cookie Policy`, and a button reading `OK`. The
   answer survives a reload and the notice does not return.
4. No page view is recorded before the visitor has answered. Each recorded page
   view carries its route and the time it happened, and only an `editor` can
   read the log.
5. Any address that matches no route renders the product's own not-found page,
   with a way back to the home route, and answers not-found rather than answering
   as though the page existed. Five different wrong addresses all reach the same
   catch-all page, not five special cases.
6. Every internal link on every public route resolves.

### Sitemap and robots

1. `/sitemap.xml` lists every public route, and only public routes: a `draft`
   case study is not in it.
2. `/robots.txt` points at the sitemap.
3. Publishing a case adds it to the sitemap; unpublishing removes it.

### The studio console

An `editor` works at `/studio/cases`, which is a two-pane arrangement above the
wide breakpoint: the list of every case, draft and published, on the left, and
the selected case's detail on the right, with the address changing to
`/studio/cases/<slug>` as the selection changes. Below the wide breakpoint the
panes stack and the list hands over to the detail.

Creating a case opens `/studio/cases/new`, its own address, not a panel over the
list.

Publishing or unpublishing updates the case's row in the list at once, and the
row returns to its previous state with a message shown in place if the save does
not land.

1. A `reader` who opens any `/studio` address is refused, not redirected into
   the console.
2. An unauthenticated visitor at any `/studio` address is sent to `/login` and
   returns to the requested address after signing in.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | home; the studio's argument end to end | none |
| `/solutions/` | redirect to the first product line | none |
| `/cirrus/` | the data-visualization product line | none |
| `/emporium/` | the virtual-space product line | none |
| `/facet/` | the product-configuration product line | none |
| `/services/` | the four disciplines, with anchors `#graphics`, `#ui`, `#assets`, `#cloud` | none |
| `/cases/` | the index of published cases | none |
| `/cases/<slug>` | one case write-up | none if published; editor only if draft |
| `/contact/` | the studio's address and the enquiry form | none |
| `/terms/` | terms and conditions | none |
| `/privacy/` | privacy policy | none |
| `/cookies/` | cookie policy | none |
| `/sitemap.xml` | every public route | none |
| `/robots.txt` | points at the sitemap | none |
| `/login` | sign in | none |
| `/signup` | create a reader account | none |
| `/studio/cases` | the case list beside the selected case | editor |
| `/studio/cases/new` | create a case | editor |
| `/studio/cases/<slug>` | edit, upload media, publish, unpublish | editor |
| `/studio/enquiries` | every enquiry, newest first | editor |
| anything else | the product's own not-found page | none |

That table is the whole information architecture. Every route answers on both
its bare and its trailing-slash form; the two serve the same page and neither
redirects to a dead end.

**Entry and redirects.** An unauthenticated visitor at a `/studio` address is
sent to `/login` and, after signing in, lands on the address they asked for. A
`reader` at a `/studio` address is refused outright. Signing in lands an
`editor` on `/studio/cases` and a `reader` on `/`. Signing out returns to `/`
and the bearer token stops working. A token that expires mid-action returns the
visitor to `/login` without losing what they had typed. `/solutions/` redirects
to `/cirrus/`.

**Journeys.**

1. **Read the argument.** Open `/`. The stage is already painted behind the
   first headline when the loader clears. Scroll: the studio states what it
   does; three statements pin in turn, one per product line, each holding the
   lower half of the screen while the scene behind it changes; a question and a
   card hand over to `/services/`; four more pinned blocks carry the three
   featured cases and a link to the rest; the footer softens the stage and
   offers `Explore our` / `Solutions`. Follow it and arrive at `/cirrus/`.
2. **Step through a product line.** At `/cirrus/`, read the cover, the claim,
   the three mechanism steps as they swing into view one after another, the
   feature run against the pinned stage, and the closing statement. Move to
   `/emporium/`: the whole page fades from the dark theme to the pale one rather
   than cutting, and the floating panels fade with it. Choose one of the three
   options on the selector and watch the scene behind it change; the chosen
   option stays chosen after the pointer leaves.
3. **Open a case.** From the navigation, open `/cases/`. Seven clusters run past
   with no heading and no filter. Open case `01`, `Oil & Gas Data
   Visualization` for `Delta AI`: the cover clip fills the opening, a back link
   sits at the left of the content column, then the client name, the title, the
   brief opening with the client as a link, eight to eleven body sections, and a
   section headed `Result`. Follow the back link to `/cases/`.
4. **Send an enquiry.** Open `/contact/`. Point at the email block and a label
   fades in; activate it and the address is copied and the result is announced.
   Fill the enquiry form with a name, an email address and a message, and submit
   it. A confirmation appears in place. Submit the same form again at once and
   it is refused.
5. **Be refused a draft.** Ask for `/cases/substation-twin` while signed out.
   The request is denied and the case appears in no listing. Ask for its cover
   object directly. Denied. Sign in as `reader@example.com`. Both are still
   denied.
6. **Publish.** Sign in as `editor@example.com`. `/studio/cases` shows every
   case with `08 Substation Twin` marked `draft`. Open `/studio/cases/new`,
   create a case, upload a cover clip, and publish it: its row updates at once,
   it appears at `/cases/`, its address resolves for a signed-out visitor, and
   it is in `/sitemap.xml`. Publish `08 Substation Twin` and step 5 now
   succeeds; unpublish it and step 5 fails again.

**States.** Every list has an empty state: a cases index with nothing published
says so rather than rendering nothing, and so does an enquiry list with nothing
in it. Every page has a loading state, and the waiting indicator appears only if
the stage is not ready within one frame of the document becoming interactive,
and not before. An error never crashes the app: the stage keeps rendering, the
chrome stays up, and the route reports what went wrong in place.

## UI/UX notes

The north star: in the first moment a visitor should understand that the
background is a real place rather than a picture, that it is moving, and that it
will not go away. Everything the interface owns is a thin translucent layer
floating in front of it.

The register is consumer and editorial on the public routes, where atmosphere is
the product and the subject is seen before the words. The studio console behind
the sign-in is operational: quiet, dense, organised for scanning and for
repeated action, with no oversized heroes and no editorial composition. Density
is spacious on the public site and compact in the console.

Six decisions carry the whole look, and dropping any one of them collapses the
site into an ordinary dark agency template. The drawing surface is the page's
background, permanently, on every route. Everything in front of it is
translucent and blurred, and three panel treatments are the only surfaces the
interface has. The page is drawn on a visible four-rule grid with crosshair
marks. Colour is a two-token theme swapped per route by a class on the document
root. Every reveal is a class flip, not a timeline. One accent, and it appears
only under the pointer.

**Colour, by role and by exclusivity.** The default theme sets a deep neutral
page ground with near-white neutral ink and icon fill, a mid cool neutral for
muted ink and for navigation at rest, an opaque panel on the same deep neutral
as the page, a translucent panel of the same colour at part alpha, a panel
border of the same near-white at a very low alpha, and a grid hairline of that
near-white at a few percent. The pale theme sets a light cool neutral ground
with deep, muted cyan ink, keeps the light cool neutral as its muted ink, and
inverts both filled panels to that deep, muted cyan with near-white ink, so the
pale route reads as pale ground with dark cards rather than as a light theme
throughout. The accent is a mid, vivid teal reading as pure cyan, and it is the
only saturated colour the interface owns: it appears on hover, on the active
state and on text selection, and nowhere else. Nothing on the page is coloured
until you point at it. In the pale theme, selection sets that teal as the ground
with the deep, muted cyan as ink. Inactive chart segments take the page ink at
part alpha and active ones take it at full, and inside the two config pagers
both stay near-white in either theme, because the pager sits on a dark panel
even on the pale route. The exact values are yours, so long as they hold those
relationships and that exclusivity.

**Type.** One family in two cuts: `DM Sans` at weights 300, 400, 500, 600 and
700 for everything, and `DM Mono` at 400 for exactly one two-word label on the
contact route. That single use is the only reason a second family is loaded at
all. Both are served with `font-display: swap`. The root is `DM Sans` at weight
400 and `16px` with `line-height: 100%`, stepping to `20px` at the tablet
breakpoint, so every relative measurement resolves against whichever root size
is in force, and any looser leading is an explicit override. Five display steps,
each weight 700 and set solid: `64px` stepping to `128px`, `48px` to `96px`,
`36px` to `72px`, `30px` to `48px`, and `24px` to `32px`. Body runs `16px` to
`20px` at weight 400 and the small label runs `12px` to `16px`. One leading
override sets `125%` and it is applied to running prose and not to list items,
so the bullets read tighter than the prose around them. Figures align wherever
amounts stack.

**Motion.** The motion character is eased: every state change in the interface
leaves quickly and arrives slowly, and there is exactly one interface duration
for all of them. Four things take twice as long, and they are the four that are
bigger than a state change: the navigation chevron's half turn, the footer
veil's fade, the case cluster's transform and opacity, and the second step of a
staggered group. Do not introduce a third duration or a second custom curve. The
one authored curve in the system belongs to the navigation chevron and is an
extreme ease: it reaches its destination almost immediately and then creeps, so
applied to a half turn the chevron snaps over and settles. Moving between routes
is slower still and starts slowly and finishes fast, which reads as the content
catching up with the stage rather than being presented to you.

Nothing here is animated by a script running a timeline. A block is marked as
reached when it comes into view and everything waiting inside it animates at
once. Waiting looks like one of two things. Either the element is invisible and
sitting one displacement step away, and it slides that distance while fading up,
in one of six directions. Or it is turned edge-on and swings around into view.
The swing is the distinctive half: the hinge sits behind the element rather than
on it, and the parent carries a perspective, so the element arrives from off to
one side along a shallow arc and settles flat, the way a hinged panel in a
display case swings shut. If it looks like a card flip, the hinge is in the
wrong place. When several things arrive together they arrive one after another,
and the gap between them equals each one's movement, so the second starts
exactly as the first finishes.

Pointing at something turns it the accent and does nothing else: nothing scales,
nothing lifts, nothing is underlined. Pressing does not move anything either; it
acquires a soft inner shading, as if pushed into the surface. There is exactly
one exception and it is the copy label on the contact route, which fades in
rather than changing colour. Two things move on their own and only two: the
waiting dots and the scroll arrow.

**Reduced motion is honoured under every part of this, and it is not the same as
switching the reveals off.** Content that starts invisible must never be able to
stay invisible, so the reveal classes are neutralised and everything arrives
already in place; the two idle animations stop; the route transition becomes
instant; and the stage keeps rendering but holds its framing instead of moving
its camera, because it is the content and removing it would change the product.
The colour transitions may remain: they carry meaning and they move nothing.

**Accessibility floors.** Body text and its ground meet WCAG AA contrast in both
themes. Text over a translucent panel meets that bar against the lightest frame
the stage can produce behind it, not against the panel's nominal colour; raise
the panel's alpha where text sits on it and bound the stage's luminance behind
text regions. The navigation ink at rest is the specific case to fix, and it
costs the design little, because it is a rest state for a control that goes
accent on hover and full ink when active. Every content image carries
alternative text describing what it shows, and a decorative image declares
itself decorative rather than carrying a description nobody needs. Icon-only
controls carry labels. Meaning is never carried by colour alone. Touch targets
are comfortably sized. Full keyboard navigation with a visible focus ring
throughout: the two navigation panels open on focus as well as on hover, or two
of the five entries become unreachable; the selector's three options are
focusable, operable by arrow keys and by space, and expose which one is chosen;
and because focus has to be visible over a moving background the ring cannot
rely on a single colour, so it pairs the accent with an outer dark halo. Each
route carries exactly one first-level heading, and the display lines that
visually form it are one heading element with line breaks inside it rather than
several stacked siblings, which changes nothing on screen and changes everything
for someone listening.

**Responsive.** Four tiers, unevenly spaced on purpose, and only one of them
changes the design's character: at the tablet breakpoint the type scale doubles,
the root size steps up, the navigation bar replaces the toggle, the shield
appears on the legal routes and the footer chevron doubles. The smallest tier
adjusts layout twelfths only. At the wide breakpoint the page gutter widens, the
case card moves from near the left edge to the centre, and the services index
appears in the left column. At the ultra-wide breakpoint the navigation bar
narrows to half the grid. The pinned blocks are half the viewport height at
every width because they are authored as a fraction of the viewport rather than
as a fixed measure, and the home document is taller on a phone than on a tablet
because the type scale halves while the content does not shorten. At a narrow
viewport nothing overflows sideways and every navigation target stays reachable.
The viewport declaration is `width=device-width, initial-scale=1.0` and nothing
else: blocking pinch zoom on a text-heavy site is an accessibility regression.
Hover has no touch equivalent, so the selector responds to the first tap as a
selection rather than requiring a hover-then-tap sequence, and the copy labels
are shown unconditionally.

**One primary action per page.** Each page leads with exactly one primary
action, visually distinct from every secondary one. On the public routes it is
the footer call to action, the only oversized link on the page. On the contact
route it is the enquiry form's submit control. In the console it is the publish
control on the selected case. Two competing primary actions on one page is the
failure to avoid.

Stances, each of which a competing product could rationally invert: atmosphere
over density on the public routes, and density over atmosphere in the console.
Space over dividers. One accent over a palette.

What this must not look like: not a dark agency template with a video header;
not a page whose background is a still image or a clip stretched behind the
content; not a marketing composition where the working interface belongs; not a
page dominated by one hue family with no second signal; and no decoration
standing in for content.

## Front-end specification

This section is the visual contract in full. It is long because the product is a
design, and the class names in it are machine-readable hooks: the exact strings
matter, because the whole utility layer depends on them.

### The one namespace

Every rule is scoped under a single class on the application root, `site-root`,
which carries the base type contract and nothing else: the family, weight 400,
the root size, `line-height: 100%`, and `display: block`, with the root size
stepping up at the tablet breakpoint.

Two consequences the build must preserve. Solid leading is the default
everywhere, so any looser leading is an explicit override. And the root size
steps at the tablet breakpoint, so every relative measurement resolves against
whichever root size is in force.

The per-route colour class carrying a product name is `color-<solution-slug>`,
so `color-facet` is the class for the third product line.

### Theme tokens and the root transition

The theme is a class on the document root, not a set of custom properties: the
reference declares no custom properties on the root at all. The roles are page
ground, page ink and icon fill, muted ink and navigation at rest, opaque panel
ground, translucent panel ground, panel border, grid hairline, inactive chart
segment and active chart segment. Each has a default-theme value and a
`color-light` value, described by family and tone in `## UI/UX notes`.

The document element itself carries the theme transition on background colour,
colour and fill, which is why a route change fades the whole page rather than
cutting it, and why the floating panels fade with it.

Theme assignment per route: the home route, the first product line, services,
the cases index, a case detail, contact, the three legal routes and the
not-found route carry no theme class, so they are the dark default. The second
product line carries `color-light`. The third carries `color-light` plus its own
scene class. That second class on the third route selects a scene, not a
stylesheet: no rule anywhere matches it, and it is read by the stage code to
choose which environment to load. Keep that pattern; it lets a designer change a
route's colour scheme without changing what is in the scene behind it.

A third theme class, `color-alt`, exists in the stylesheet and affects exactly
one property, the cover caption opacity. It was never observed applied. Build
it, leave it unused.

### The three panel treatments

The interface has exactly three surfaces and everything a visitor reads sits on
one of them. All three are blurred against the stage behind them and all three
transition their ground colour, so a theme swap carries them with it.

| Class | Ground | Blur | Border |
|---|---|---|---|
| `.panel-blurred` | none of its own | the heaviest | a hairline of the theme ink at very low alpha |
| `.panel-translucent` | the panel colour at part alpha | the middle | none |
| `.panel-opaque` | the panel colour at full | the middle | none |

`.panel-blurred` is a pure frosting with a hairline edge, used for the
full-viewport veils. `.panel-opaque` still declares a backdrop blur even though
its ground is opaque, which costs nothing and is what makes it behave
identically to its translucent sibling when its alpha is animated. In the pale
theme both filled panels invert.

The three blur strengths are the whole surface language and they appear nowhere
except these three classes. Do not let a backdrop filter reach a component that
repeats per list item.

### Spacing, the sizing rule and the utility layer

The step scale is eight steps: zero, then three small fractional steps which are
the base unit divided by seven and doubled twice, then the base unit and its
plain multiples up to four times it. Do not round the three fractional steps:
they are the reference's own literals and they are what makes the small paddings
of the navigation and the panels sit where they sit. The scale is exposed as
`p-N` and `m-N` for all sides, with the single-axis and single-side variants
`pt-`, `pb-`, `pl-`, `pr-`, `px-`, `py-` and the matching margins.

The content inset is one class, `cop`, used on every page container: the base
unit of padding each side, doubling at the wide breakpoint. That is the whole
page gutter.

Widths are twelfths of the parent as `w-1` to `w-12`, with `h-N` for heights,
`wh-12` for both at full, and a viewport-height variant `vh-N`. Three responsive
prefixes map onto the tablet, wide and ultra-wide breakpoints: `m_`, `w_` and
`uw_`. So `w-9 w_w-8 uw_w-6` on the navigation bar reads three-quarters of the
parent below the wide breakpoint, two-thirds from it, and half from the
ultra-wide one.

The site is built almost entirely from utilities, and reproducing it means
reproducing the vocabulary, because every selector below is written against it.

| Group | Members |
|---|---|
| Position | `rlt` relative, `abs` absolute at top left, `fxd` fixed at top left, `sticky` pinned to the top |
| Display | `d-none`, `d-block`, `d-inline`, `d-inline-block`, and `d-hide` and `d-show`, the last two being opacity transitions |
| Flex container | `fl-row`, `fl-col`, their `-rev` and `fl-inl-` variants |
| Flex alignment | `fl-jc-`, `fl-ac-` and `fl-ai-` with `start`, `end`, `center`, `between`, `around`, `evenly`, `baseline` and `stretch` as applicable |
| Flex item | `fl-grow-0`, `fl-grow-1`, `fl-shrink-0` |
| Radius | `br-2`, `br-4`, `br-8`, `br-16` and `br-32`, each also setting `overflow: hidden` |
| Type | `mono`, `t-right`, `t-center`, `t-lower`, `t-high` |

`t-high` is the only leading override in the system. Every radius utility sets
`overflow: hidden` alongside the radius, and that is not incidental: the media
panels rely on it to clip video to the corner radius without a second rule.

### Repeating patterns

Three tiled backgrounds on a small square tile, repeating and centred, each with
a `pattern-strong` variant that triples the alpha. `.pattern-dots` is a radial
gradient reading as a fine perforation. `.pattern-lines` is a linear gradient
reading as fine horizontal rules. `.pattern-stripes` is the same lines on a
diagonal. They are the site's only texture and they are drawn, not loaded. In
the pale theme all three swap the near-white for the deep, muted cyan at the
same alphas. The dot pattern is the one that carries the look: it is the faint
perforation visible across the case media and the footer ground.

### Shadows and radii

Every shadow in the system is a zero-offset, zero-spread glow. There is no
directional lighting anywhere in the interface, because the lighting is in the
stage behind it. A wide soft black glow sits on the floating arrow controls and
on the case link button; a smaller one keeps the two bars of the menu toggle
legible against a bright frame of the stage; the heaviest glow in the system
sits on the case media panel and is a vignette that sinks the panel's edges into
the dark stage, which is what stops a full-saturation colour block looking
pasted on. The inset pair is the entire pressed-state language: a button does
not move when pressed, it acquires an inner shadow, with a deeper variant on the
menu toggle.

Four radii in strict proportion: the smallest on the grid marks and the menu
toggle bars, the next on the loading dots, the next on the navigation bar and
the arrow controls, the next on the large cards and media panels, and one larger
value available and unused.

### Iconography

Every mark in the interface is inline vector geometry. No icon font, no sprite,
no image file. Eleven distinct drawings in four families.

**The chevron family.** One drawing at four rotations, in a coordinate box whose
negative origin must be preserved because the path data is written against it. A
chevron up is used by the back-to-top control and by the navigation dropdown at
rest. A chevron right is the workhorse: the navigation panel entries, the case
cards, the footer call to action and the case detail back link. There is no
separate chevron-down and no separate chevron-left drawing. Down is the up path
rotated half a turn, which is exactly what the navigation dropdown does on
hover, and left is the right path mirrored the same way. The case detail back
link is the only element on the site that uses the chevron pointing left.

**The monogram.** The logotype mark is a faceted kite drawn twice: once as a
filled body and once as the outline that reads as its far edge. It exists in two
coordinate boxes, a small one with two paths and a wider navigation one with
three, the two re-fitted into the wider box.

**The shield.** Used on the legal routes and appearing only from the tablet
breakpoint up.

**The arc gauge.** Generated as segments rather than drawn once, and used by the
two config pagers.

Icons inherit their fill from the element around them, so a mark takes the theme
ink, the accent on hover, and the muted ink where the logotype recedes.

### The navigation bar

The bar sits proportionally within the grid container, right-aligned so its
right edge lands on the grid's fourth rule. Do not hard-code its width;
reproduce the rule and the measurement falls out at any width. Its height is its
line box plus its own padding and is not authored.

Its composition is `nav-bar w-9 w_w-8 uw_w-6 br-8 p-all`, containing
`nav-entries rlt fl-row`, containing five `nav-entry fl-grow-1 mini`, each
containing one `nav-bar-button p-3 rlt`. The bar carries the heaviest backdrop
blur and the navigation radius. The five entries are content-sized, not equal:
`Home`, `Solutions`, `Services`, `Cases`, `Contact`.

The button is the site's whole interaction language, so the full state table
matters:

| State | Ground | Ink | Shadow |
|---|---|---|---|
| Rest | the translucent panel colour | the muted ink | none |
| Hover | the opaque panel colour | the accent | the inset glow set to transparent, so the transition has a destination |
| Active, meaning the current route | the panel colour at zero alpha | the full page ink | a soft inner shadow |
| Hover while active | the opaque panel colour | the accent | the inset glow cleared |

All of it transitions on background colour, colour and fill. The active entry is
therefore the one that looks like a hole in the bar rather than a highlight in
it: its ground goes fully transparent and it acquires an inner shadow, so the
frosted bar appears punched through at the current route.

### The dropdown panels

Two of the five entries, `Solutions` and `Services`, carry a chevron and open a
panel. The panel does not float over the bar; it grows out of it.

`.nav-panel-frame` is a zero-height clipping window directly under the bar, at
the bar's own left edge and width. The panel inside it is positioned against the
frame's bottom edge, so as the frame's height animates from nothing to its
content height the panel appears to slide down out of the bar rather than to
unfold from its own top. Both the height and the ground colour transition, and
the ground goes from the translucent panel colour to the fully opaque one as it
opens, so the panel becomes readable exactly as it becomes visible. Its open
state is `.deployed`.

The chevron on `.nav-bar-button` is positioned at the button's right edge,
vertically centred, and on hover it lifts slightly and rotates a half turn on
the one authored curve in the system.

Each panel entry is `nav-panel-button rlt fl-col fl-jc-center px-3 py-2 w_py-3`
carrying a title and a `description` beneath it. The description is set at a
relative size, uppercase, at slightly looser leading, at half opacity. The panel
itself takes the muted ink; the category label above each group carries the same
half opacity as the descriptions, so the panel reads as one dim field with the
entry titles as the only bright things in it. An active entry takes the full
page ink.

The dropdown contents are identical on both navigation surfaces and are the
site's real table of contents:

| Group | Entry | Sub-caption |
|---|---|---|
| Solutions, category `Data` | `Cirrus` | `3D Data Visualization` |
| Solutions, category `Retail` | `Emporium` | `Virtual Showrooms` |
| Solutions, category `Retail` | `Facet` | `Product Showcasing` |
| Services, category `3D` | `Real-Time Graphics` | `Real-Time 3D Web Graphics` |
| Services, category `3D` | `Assets Pipeline` | `Automated Asset Pipeline` |
| Services, category `Web` | `User Interface` | `UI Development` |
| Services, category `Web` | `Cloud Infrastructure` | `Kubernetes for 3D Data` |

The four Services entries are anchors into the single services route, not
separate pages.

### The menu toggle and the mobile menu

Below the tablet breakpoint the bar is replaced by one square control,
`nav-menu-toggle`, inset from the top and from the right gutter, holding two
`line` bars. Each bar is a short rounded rectangle centred on the control and
offset up and down through its transform, and each carries a small black glow at
part alpha, which is what keeps them legible against a bright frame of the stage
behind them.

The change to a cross is four named keyframe animations, not a transform toggle,
and the choice matters: a keyframe can move through an intermediate state, and
these do. The four are `line-top-open`, `line-top-close`, `line-bot-open` and
`line-bot-close`. Each bar first travels to the centre, then rotates. The
midpoint stop is the whole effect: the two bars meet in the middle as a single
line before splitting into the cross, and the same happens in reverse. An
implementation that interpolates straight from the offsets to the rotations
produces a different, worse animation. The closing pair carries a forwards fill
so the cross persists; the opening pair does not, because its end state is the
resting state.

Toggle states: at rest the translucent panel colour; deployed, the panel colour
at zero alpha, so the control's own ground disappears once the full panel behind
it is showing; on hover the opaque panel colour with accent bars; pressed, the
panel colour at zero alpha with a deeper inner shadow and full-ink bars.

The panel is `nav-menu br-8`, carrying the heaviest backdrop blur and a hairline
border, sitting pointer-transparent and invisible until its `.deployed` state
turns pointer events on and fades it in. Inside it `.filler` and `.nav-panel`
both take the translucent panel colour and an active panel goes to a low-alpha
variant. Entry titles are the same muted ink as the bar.

### The logotype

A mark of fixed proportions whose box sits on the page gutter and on the grid's
mark row, then is pulled left and up by two negative margins. The pull is
optical: the kite's leftmost point and its apex both sit inside its box, so the
negative margins put the drawn edges, not the box edges, on the grid. At the
tablet capture the same rule resolves against the narrower gutter.

The mark inherits its fill from the link around it, so it is the page ink in the
dark theme, the pale theme's ink in the pale one, and the accent on hover. When
the mobile panel is deployed it takes a `.deployed` class and drops to the muted
ink, so the mark recedes while the menu is open.

### The footer

Present on every route, pointer-transparent until it is reached, at which point
an `.active` class turns it on. Three parts.

**The veil.** A full-viewport gradient that fades the stage out behind the
footer content, from fully transparent at the top to the page ground at the
bottom, carrying the gentlest of the three blurs, which is what makes the stage
go soft rather than dark as the footer arrives. The veil fades over the double
duration while the content beneath it fades over the standard one. The slower
veil is deliberate: the background softens first and the words arrive into an
already-quiet field. In the pale theme the same gradient runs to the pale
ground.

**The call to action.** One oversized link whose wording changes per route, with
a chevron that sits outside the text box and slides on hover. The chevron is
positioned past the end of the phrase and pulled back so it overlaps the last
letter rather than following it; on hover it slides right by exactly the amount
it was pulled back, which is to say it moves to where it would naturally sit,
and it slides further at desktop sizes than below the tablet breakpoint, where
it is also drawn at half the size. A negative bottom margin on the block above
lets the descenders of the display type run into the row beneath.

The six calls to action, one per route family:

| Route | Lead-in | Line 1 | Line 2 | Line 3 |
|---|---|---|---|---|
| Home | `Next up` | `Explore our` | `Solutions` | |
| `Cirrus` | `Visualize` / `your data today` | `Let's` | `Talk` | |
| `Emporium` | `Let's make your vision a reality` | `Get In` | `Touch` | |
| `Facet` | `Convert your products today!` | `Let's` | `Discuss` | `How` |
| Services | `Explore` | `Our` | `Cases` | |
| Cases and case detail | `Have a project in mind?` | `Let's` | `Talk` | |

Nobody is asked the same question twice: someone reading the whole site straight
through is walked from curiosity to a conversation without being sold to twice.

**The small print.** Three lowercase links, `contact`, `terms` and `privacy`,
each an inline block; a copyright line reading the copyright sign, the year and
the studio name; and a back-to-top control pairing the chevron up with the label
`Back to top` set small.

The footer is not a link farm and it is the site's second index.

### The drawn grid

The most easily lost part of the design and the cheapest to build.

**The rules.** A container `lines fl-row fl-jc-between wh-12 abs` inset by the
page gutter, holding five `.line` children of which the first four are
displayed. Each is a hairline of full viewport height at a few percent of the
theme ink, and the container distributes them evenly across its width. The fifth
child is present in the markup and collapses to nothing, so the count is a
content decision rather than a layout one. The same rule produces four rules at
every width against the gutter in force. The alpha is close enough to invisible
that a poorly calibrated display will lose it entirely, which is correct: the
grid is for the people who can see it. They are structure, not decoration.

**The marks.** Two rows of crosshairs, one near the top and one the same
distance off the bottom, each row a `marks fl-row fl-jc-between w-12 abs`
holding five `.mark` children distributed on the same interval as the rules, so
every mark sits on a rule. Each mark is a zero-sized point carrying two rounded
bars that centre on it, one horizontal and one vertical, each pulled back by
half its own size, so the result is a small plus sign whose centre is exactly on
the grid intersection, like the registration marks on a printer's proof. Below
the tablet breakpoint the top mark row moves to the very top of the viewport,
because on a phone there is no navigation bar for it to register against; the
bottom row keeps its distance from the bottom at every width.

**The clipping frame.** One fixed element, `frame fxd wh-12`, unclipped by
default, whose `.framed` state insets the stage to the page gutter at the
current breakpoint and gives it the card radius, animated rather than cut. This
is the one control that makes the stage look like a window rather than a
wallpaper. The inset matches the gutter exactly, so the stage's edge lands on
the outer grid rules.

### The loader, the pending dots, the cookie notice and the scroll arrow

The loader covers the first paint until the stage is ready. The pending dots are
three small round dots that fade in turn on an endless linear cycle; they exist
because the stage takes measurably longer than the document, so they appear only
if the stage is not ready within one frame of the document becoming interactive,
and not before.

The cookie notice sits low on the first screen and carries a text line reading
that the studio uses cookies to optimize website performance and functionality
and that by continuing to use this website you agree to its policy, an
underlined link reading `Cookie Policy`, and a button reading `OK`. It is
dismissed once and the answer survives a reload. It overlaps the scroll arrow on
the first screen, which is acceptable because it is dismissed once.

The scroll arrow is a small `arrow panel-translucent p-2 br-8` control that
bounces on an endless linear cycle, above the label `Scroll down` set small. It
sits on every route that has a first screen.

Every video element carries the fallback text `Your browser does not support the
video tag.`

### The scroll system

Four selectors change across frames on every route and they are the site's
permanent scroll machinery: the pending dots' opacity, the reveal system's
transforms, the scroll arrow's transform, and the footer veil's opacity. A fifth
appears only on the routes that have a pinned stage.

**The sticky stage.** `.sticky` is one declaration, pinned to the top, and it is
the mechanism behind every long-form section on the home route and the three
product routes. The pattern is a stack of half-viewport-height blocks that pin
in turn as the page scrolls past them, so the reader holds one statement in
place while the stage behind it changes. Each block occupies the lower half of
the screen while pinned and the stage owns the upper half. The home route
carries two groups, of three and of four. Below the wide breakpoint the block is
full content width. The block is half the viewport height at every width because
it is authored as a fraction of the viewport.

While a block is pinned it is being blurred and unblurred as it hands over to
the next one. That filtering is the important half and it is what a static
screenshot cannot show: a statement does not simply disappear when its turn is
over, it goes gently out of focus first, continuously, tied to scroll position
rather than to a single fade.

**The scroll progress bar.** `.solution-scroll-progress` is unique to the
product routes: a thin track at a low alpha of the page ink with a solid fill
over it, inside a clipping panel. It does not invert in the pale theme, because
the indicator sits on a dark opaque panel in both themes.

**The veil.** Two veils exist and they do different jobs. The footer veil fires
on every route. A second is used as a section veil, carrying the gentlest blur
and the same fade to the page ground, in both theme forms.

**The framed state.** The clipping frame is scroll-driven: the build must be
able to inset and un-inset the stage against scroll position, with the inset
matching the page gutter at the current breakpoint and the radius matching the
card radius, and the change must animate rather than cut.

Reveals are driven by intersection with the viewport, never from a scroll offset
table, so the document height can change without retuning. The reference's own
trigger points were not recoverable and must not be hard-coded; expect a tuning
pass by eye against a running build.

### The reveal vocabulary

A container carries `.scroll-trigger`, gains `.enabled` when it comes into view,
and every descendant carrying a `tr-` class animates from its offset to rest.
The base is `.tr-on-enabled`, which starts invisible and transitions its
opacity; `.p-all-on-enabled` turns pointer events on when the container is
enabled.

The offsets, each extending the transition to include the transform and giving
the element a resting displacement of exactly one step, the only displacement
value in the system:

| Class | Reads as |
|---|---|
| `tr-slide-top` | rises into place |
| `tr-slide-bottom` | drops into place |
| `tr-slide-left` | slides in from the right |
| `tr-slide-right` | slides in from the left |
| `tr-slide-front` | comes forward out of depth |
| `tr-slide-back` | identical to `tr-slide-top` in the reference |

The pivots are the more distinctive half: `tr-pivot-top`, `tr-pivot-right`,
`tr-pivot-bottom` and `tr-pivot-left`, each a quarter turn about a horizontal or
vertical axis, inside a `tr-pivot-container` that carries the perspective. The
load-bearing part is that the transform origin sits behind the element rather
than on its face, so a quarter turn swings the element in along an arc rather
than flipping it about itself. Combined with the perspective on the parent, the
element appears to arrive from off to one side and swing flat. Change either and
the effect becomes an ordinary card flip.

The stagger is six delay classes, `tr-delay-0` to `tr-delay-5`, in steps equal
to the interface duration, so a staggered group hands over cleanly: each element
starts exactly as the one before it finishes.

The identical rule set is declared a second time scoped under `.layer` instead
of `.scroll-trigger`, so the same reveal vocabulary works for content pinned to
the viewport as well as for content that scrolls. Build both scopes.

### The stage, its layers and depth

The DOM around the drawing surface is four nested full-viewport elements:
`layer fxd wh-12 enabled`, the fixed overlay that content is drawn into;
`viewer wh-12 wh-12`, the stage's own root, which owns the frame and the veils;
`frame fxd wh-12`, the clipping frame; and `canvas wh-12`, the positioning
wrapper holding one drawing element.

The layer is fixed, full-viewport and pointer-transparent, and it fades in.
Pointer-transparency is the default and it is important: the layer must not eat
pointer events destined for the stage beneath it, and individual children opt
back in.

The interface layer is not flat, and three things prove it and must be
reproduced: preserved three-dimensional transforms on a set of elements; a
perspective on both the pivot containers and on one ordinary layout content
column, which means a layout column is acting as a perspective root; and a
handful of elements tipped from the page plane into the floor plane by a quarter
turn about the horizontal axis plus a translation, positioned at the centres of
three columns across the content width.

**Video inside the interface.** Clips sit inside `.ui-media` panels, not on the
stage. They are silent, looping and autoplaying, with their source set at
runtime. A panel is either `cover`, filling and cropping, or `original`, centred
and cropped from the middle, and four position modifiers, `left`, `right`, `top`
and `bottom`, move the crop to the corresponding edge.

Each media panel can carry a caption hidden until asked for: an `info-button`
that is pointer-active and carries a wide glow, and an `info-text` that is
invisible and pointer-transparent until a `show-info` state fades it in. The
captions in the case write-ups are technical asides in the studio's own voice,
saying things like this is the detail system in its debugging mode, or this is
the same view with the ground made see-through and some layers cut away. They
are not marketing and they must not be rewritten into marketing.

### Route compositions

**Home.** One long scroll in six movements. The first screen carries the stage
at full bleed, the chrome, and one text block low and left of centre: a small
line reading `Adding`, then two display lines reading `Dimension` and
`to the web`. Every display line is its own element so it can carry its own
reveal class and its own delay, which is the pattern throughout. The scroll
arrow sits low, with the cookie notice overlapping it.

The cover caption is a display-scale word set at a very low opacity behind the
content, naming the current section; it holds the same faintness in every theme,
so both theme rules restate the same value rather than overriding it. It is a
shadow of a word, not a heading.

The second screen carries a small line reading `We specialize in`, a display
line reading `3D web solutions for industry, science and retail`, and a
paragraph reading `Our solutions allow users to interact with vast spatial data,
captivating virtual spaces and highly detailed products.` The display line wraps
to two lines and takes the leading override.

Then the first run of three pinned blocks, one per product line, each carrying
two display lines of what the product does, a `Discover` control, the product
name, and a trailing caption. The product name is set smaller than its own
description, which inverts the expected hierarchy and is deliberate: what the
product does is the headline and what it is called is the caption. The three
read `3D Data` / `Visualization`, `Virtual` / `Showrooms`, and `Product` /
`Showcasing`, with trailing captions `3D Data Visualization`,
`Virtual Showrooms & Experiences` and `Product Showcasing & Configuration`.

A stylesheet rule sets the `Discover` control to a red that is not a token in
the palette and was never observed applied. Treat it as debugging residue and do
not build it.

Then the services handoff: a question reading `Eager to transform your ideas
into captivating 3D web content?`, followed by a card containing
`Take a look at our` and `Services` with a chevron at its right edge. The card
is a `button br-16 rlt` and it rises into place under the reveal system.

Then the second run of four pinned blocks carrying three case clusters, each
with its own clip, its number, its client and its title, and one closing link
reading `View All Featured` above `Cases`.

Then the footer, with the home route's call to action.

**Solution.** Each route's entrance is the fade described above. One template,
three instances, in seven movements: cover, claim,
the three-part mechanism, the feature run, the interactive demonstration on two
of the three, the closing statement, and the footer. The claim on the first
instance splits a figure and a sentence across two display steps and is the
largest single contrast on the site. The three mechanism steps are the elements
carrying the pivot reveals, and they swing in from the side one after another.
The feature run is the bulk of the route and the section the sticky mechanism
exists for.

The interactive demonstration is built from the arc gauge inside a
`pager-product-config` or a `pager-room-config`. The two are the same component
with different inner names: the first names its rotating halves `chart-strap`
and `chart-cover`, the second names its single rotating element `chart-style`.
Build one component with a variant, not two. The `donut-chart` is
pointer-transparent until enabled and only then do its segments become targets;
a segment goes solid on hover and the chosen one holds that state. Both
instances carry a label reading `Give it a try` and a sentence naming what the
wheel changes.

The gauge does not fade in. Two half-rings hinged along their shared bottom edge
are lying face down, one rotated each way, and both return to rest when the
pager becomes active, so the dial rotates up out of the floor of its own panel
from both directions at once. The container clips, and a soft gradient along the
bottom edge is the shadow it comes out of. If it fades in, or if it slides up,
that is not it.

**Services.** One heading pair, a small line reading `Explore our specialized`
over a display line reading `Services to amplify your next web project`, then
four discipline blocks, then the footer. Each block is the discipline name as a
display step and as the anchor target, a short promise, a longer promise, an
opening paragraph, four labelled bullets each reading label then sentence, an
argument paragraph and a closing line. Above the wide breakpoint a persistent
index of the four sits in the left column with the current one in full ink and
the other three at reduced opacity, each showing its caption over its
sub-caption in the same small uppercase descriptor the navigation panel uses, so
the reader always knows which of the four they are inside; below that breakpoint
the left column collapses and the four blocks simply follow one another. This is
the site's only long-form reading route and it is deliberately the least
animated. The prose takes the leading override and the bullets do not, so the
bullets read tighter than the prose around them; reproduce that difference.

**Cases index.** No heading, no filter, no tags, no pagination. Each case is a
full-width `case-cluster`, which is one of only four places in the site that
uses the double duration, because the clusters are large and they move further
than an interface element. The media panel carries the heaviest glow in the
system. The info card carrying the number, the client and the title is a
`.panel-opaque` at the large radius with a chevron at its right, positioned
against the media panel's bottom edge and then pushed down by half its own
height so it straddles the boundary; its horizontal origin moves from near the
left edge of the cluster to the centre at the wide breakpoint. Behind each
cluster a saturated full-bleed colour block arrives, keyed to that case, with
the dot pattern visible across it. The number is set in the small style with a
slashed zero glyph, so it reads like something from a technical drawing; that is
a font feature, not a different character.

**Case detail.** In order: a clip in a full-bleed panel carrying the cover
media; a back link reading `View` over `All cases` with the chevron rotated to
point left, sitting in a `.panel-translucent` card at the far left of the
content column; the client name; the case title; the brief, which opens with the
client name as a link and continues in the same paragraph; then the repeating
body of media, an optional caption, a heading and a paragraph, eight to eleven
times; then a heading reading `Result` and its paragraph; then the footer.

`.ui-title` and `.ui-paragraph` are the case body's own classes and they are the
only content-specific type classes on the site. Keep them: they mark the
boundary between the site's chrome and its editorial content, and they are what
a content system would target. On each body media panel the link positioner sits
two-thirds across the panel, on its bottom edge, pushed down by half its own
height, the same straddling rule as the index card at a different horizontal
origin, and its button carries a wide glow that lightens in the pale theme.

Above the wide breakpoint the route runs a two-column arrangement, media in the
left two-thirds of the content column and text in the right third, with the
title breaking out above the media; below it the two stack, media first. This is
the one long route with no pinning: it is a document and it scrolls like one.
That contrast is the point, because the routes that sell hold you in place and
the route that explains lets you read at your own pace.

**Contact.** A small line reading `Hello`, then three display lines reading
`How can`, `we assist` and `you today?`, set solid, one element per line,
occupying the left half of the content column, with the stage's globe on the
right half positioned so the question's ragged right edge and the globe's left
limb interlock without overlapping.

Then the two copy blocks. The first is a small line reading `Send us an email`,
a hover label reading `Copy email`, and the studio address set at the third
display step, which makes it the second largest thing on the page after the
question; that is the whole design of the route, in that the studio asks one
question and then sets its address at headline size. The second is a small line
reading `Visit our office`, a hover label reading `Copy address`, the office
address, which is a street line, a line carrying the postcode and the town
`2200 Herentals`, and a country line reading `Belgium`, and then a label reading
`Maps` linking out to a map.
Two lines of the office block carry a non-breaking space between the street
number and the postcode groups, so the address never breaks mid-token.

Then the business block: a label reading `Business Info` in the mono cut, which
is the site's only use of the second family, then the trading company
`Meridian Comm. V.`, then the tax identifier, then a second copyright line in
the page rather than in the footer carrying the copyright symbol, the year and
the studio brand name.
Then two social links under a small label reading `Follow us`, set as text with
no icons.

Then the enquiry form, which is the one thing on this route the reference did
not have, and the one primary action on the page.

**Legal documents.** Three routes on one template, carrying the shield from the
tablet breakpoint up, and carrying the full chrome, the full stage and the full
motion system.

**Not found.** Two display lines reading `Page Not` and `Found`, then a small
line reading `Take me` over a line reading `Home` in the same lead-in-over-target
form the footer call to action uses, then the scroll arrow with its label. It is
exactly two viewport heights: one screen of content and one screen of footer,
because the footer is a full-viewport component and this is the clearest place
to see it. It is the least animated route on the site and it still carries the
stage. Build it properly rather than as an afterthought, because it is the page
that proves the background really is on every route.

### Module and component architecture

Every route is the same five-deep stack, and building it once is most of the
build: the viewer, which owns the stage, the frame and the section veils; the
fixed clipping frame; the canvas and its one drawing element; the fixed overlay
layer for pinned content; and then the page for the route, plus the navigation,
the footer, the loader and the cookie notice.

Twenty-four reusable components: the navigation bar, the navigation dropdown,
the menu toggle, the menu panel, the logotype, the footer, the grid rules, the
grid marks, the loader, the pending dots, the cookie notice, the scroll arrow,
the reveal container, the sticky stage block, the progress bar, the section
veil, the media panel, the case cluster, the case button, the arc gauge, the
config pager, the copy button, the button, and the three panels. The three
panels and the button account for most of the surface area; the rest are each
used on one or two routes.

**State ownership.** The current route, the theme class and the scene class on
the document root, the enabled state on each reveal container, the active state
on the current navigation entry, the deployed state on a navigation panel, the
framed state on the stage frame, the active state on the footer, the shown state
on a media caption, and the chosen state on a gauge segment are all derived from
the route, the scroll position or the pointer, and none of them is persisted.
Exactly one piece of client state outlives the page, and it is the cookie
choice.

### The zero-asset substitution guide

The build ships no binary asset of any kind: no photograph, no video file, no
font file, no texture, no model and no vector file. Every asset class is
generated, replacing every placeholder with something the build draws for
itself. Two things are deliberately not substituted, because they are not
assets: the copy deck above, which is content, and the interface geometry, which
is drawn inline. The three repeating textures are drawn as gradients. The monogram and
the favicon are drawn as geometry. The type falls back to a metric-compatible
stack when the named families are not available, and the swap is not a visible
reflow. The stage scenes are generated rather than loaded, and they are built from
primitives: a room from primitives means a floor, three walls and a ceiling
plane with one opening for light; a product-shaped object from primitives means
a rounded box with a capsule strap on it; a slow constant rotation is enough
motion for either. The dark city is a field of emissive points thrown out of
focus, the point cloud is a sampled height field drawn as dots, and the globe is
a sphere with its continents picked out as a dot matrix. The case and cover
media are generated stand-ins: a silent, looping, autoplaying clip or a still,
either way produced by the build rather than shipped with it. The social card is
a single generated image shared across the site unless a route supplies its own.

### The copy deck

Every string below is seed content and is pinned. Set the long dash character
where this deck writes a spaced hyphen, set curly quotation marks where it
writes straight ones, and set the copyright symbol where it writes `(c)`. Four
typographic errors in the source material are corrected here and the correction
is deliberate: `unforgettable`, `legion`, `tracks` and `see-through`.

**Home.**

| Block | Class | String |
|---|---|---|
| Opening | `.mini` | `Adding` |
| Opening | `.h2` | `Dimension` |
| Opening | `.h2` | `to the web` |
| Proposition | `.mini` | `We specialize in` |
| Proposition | `.h2` | `3D web solutions for industry, science and retail` |
| Proposition | `.h3` | `Our solutions allow users to interact with vast spatial data, captivating virtual spaces and highly detailed products.` |
| Product 1 | `.h1` | `3D Data` / `Visualization` |
| Product 1 | `.discover` | `Discover` |
| Product 1 | `.h3` | `Cirrus` |
| Product 1 | `p` | `3D Data` / `Visualization` |
| Product 2 | `.h1` | `Virtual` / `Showrooms` |
| Product 2 | `.h3` | `Emporium` |
| Product 2 | `p` | `Virtual Showrooms` / `& Experiences` |
| Product 3 | `.h1` | `Product` / `Showcasing` |
| Product 3 | `.h3` | `Facet` |
| Product 3 | `p` | `Product Showcasing` / `& Configuration` |
| Services handoff | `.h3` | `Eager to transform your ideas into captivating 3D web content?` |
| Services handoff | `div` | `Take a look at our` |
| Services handoff | `.h3` | `Services` |
| Cases handoff | `span` | `View All Featured` |
| Cases handoff | `.h3` | `Cases` |
| Scroll cue | `.mini` | `Scroll down` |
| Media fallback | `video` | `Your browser does not support the video tag.` |

**Cirrus.**

| Block | Class | String |
|---|---|---|
| Cover | `.mini` | `3D Data` / `Visualization` |
| Cover | `.h1` | `Cirrus` |
| Claim | `div` | `An astonishing` |
| Claim | `.h0` | `80%` |
| Claim | `.h2` | `of all data is spatial - most of it is still underused` |
| Mechanism | `.t-high` | `Cirrus Streamlines` |
| Mechanism | `.h3` | `Data to` / `3D Graphics` |
| Mechanism 1 | `.h4` | `Spatial Data` |
| Mechanism 1 | `p.mt-3` | `The original data remains safely on-site.` |
| Mechanism 2 | `.h4` | `Data Proxies` |
| Mechanism 2 | `p.mt-3` | `Automated pipeline extracts data proxies for online use.` |
| Mechanism 3 | `.h4` | `Web Viewer` |
| Mechanism 3 | `p.mt-3` | `Interactive WebGL viewer with intuitive interface.` |
| Transition | `div` | `Activate` |
| Transition | `.h1` | `Your` / `Data` |
| Transition | `div` | `with` |
| Transition | `.h0` | `Cirrus` |
| Feature 1 | `.h3` | `Online Digital Twins...` |
| Feature 1 | `p` | `Transform intricate technical plans, projects, and systems into intuitive webviews, bridging the gap between complexity and clarity.` |
| Feature 2 | `.h3` | `...at Scale` |
| Feature 3 | `.h3` | `Dynamic Content` |
| Feature 3 | `p` | `Fully interactive components allow for seamless exploration and manipulation of content, providing an immersive experience tailored to your needs.` |
| Feature 4 | `.h3` | `Optimal performance` |
| Feature 4 | `p` | `Our cutting-edge infrastructure ensures large datasets are loaded, processed, and displayed efficiently for a smooth, responsive user experience.` |
| Feature 5 | `.h3` | `Simulation` |
| Feature 5 | `p` | `Harness the power of simulations with clear, visual interpretations of results to support insightful, impactful steps forward.` |
| Feature 6 | `.h3` | `Layered Data` |
| Feature 6 | `p` | `Unite historical and real-time data into a cohesive view, enabling trend analysis and a responsive strategy.` |
| Feature 7 | `.h3` | `Indicators` |
| Feature 7 | `p` | `Display, annotate, and monitor real-time operational data to ensure intuitive and actionable situational awareness.` |
| Feature 8 | `.h3` | `Focus on the Work` |
| Feature 8 | `p` | `Align all stakeholders with a unified visualization platform, enabling quick, confident, and informed decisions.` |
| Feature 9 | `.h3` | `Advanced Lighting` |
| Feature 9 | `p` | `With precise control over lighting and atmosphere, advanced visualization solutions are available to elevate your experience.` |
| Feature 10 | `.h3` | `& Shaders` |
| Feature 10 | `p` | `Custom shaders and effects are the final ingredient to perfect data interpretation and aesthetic appeal.` |
| Closing | `div` | `Displaying` |
| Closing | `.h1` | `Complex` / `Data` |
| Closing | `div` | `is where Cirrus` |
| Closing | `.h0` | `Shines` |
| Caption | `div` | `Turbine Construction` |

**Emporium.**

| Block | Class | String |
|---|---|---|
| Cover | `.mini` | `Virtual Showrooms` / `& Experiences` |
| Cover | `.h1` | `Emporium` |
| Claim | `.mb-3` | `Traditional` |
| Claim | `.h2` | `Virtual` / `Experiences` |
| Claim | `.h4` | `require complex setup and are a hassle to access - limiting their potential` |
| Mechanism | `.t-high` | `Emporium enables accessible` |
| Mechanism | `.h3` | `Virtual Experiences` / `on the Web` |
| Mechanism 1 | `.h4` | `Content` |
| Mechanism 1 | `p.mt-3` | `Expertly crafted 3D content and materials.` |
| Mechanism 2 | `.h4` | `Cloud` |
| Mechanism 2 | `p.mt-3` | `Hosts assets, logic and precomputes lighting.` |
| Mechanism 3 | `.h4` | `Web App` |
| Mechanism 3 | `p.mt-3` | `Interactive 3D view, always up-to-date, accessible anywhere.` |
| Feature 1 | `.h3` | `Scene` |
| Feature 1 | `p` | `Captivating environments that put users in dynamic, interactive 3D spaces tailored to their needs.` |
| Feature 2 | `.h3` | `Materials` |
| Feature 2 | `p` | `Bring realism and add depth, texture, and authenticity to every object in the scene.` |
| Feature 3 | `.h3` | `Lighting` |
| Feature 3 | `p` | `Enhances the atmosphere with high dynamic range lighting, creating visually stunning and mood-enhancing effects.` |
| Feature 4 | `.h3` | `Action!` |
| Feature 4 | `p` | `Intuitive controls and animations provide fluid interaction and movement for an engaging 3D experience.` |
| Feature 5 | `.h3` | `Personalize` |
| Feature 5 | `p` | `Customizable styling options for objects and materials in the scene create opportunity for a unique and memorable 3D experience for every visitor.` |
| Selector | `.h4` | `Give it a try` |
| Selector | `p` | `Select a color on the wheel above to change the interior style` |
| Transition | `.h2` | `Go` / `Beyond...` |
| Feature 6 | `.h3` | `...Beyond Reality` |
| Feature 6 | `p` | `Advanced techniques can go beyond reality and make products more accessible and comprehensive.` |
| Feature 7 | `.h3` | `WebVR Supported` |
| Feature 7 | `p` | `Emporium scenes can be viewed in VR straight into the web browser. No downloads or installs required.` |
| Feature 8 | `.h3` | `AI Characters` |
| Feature 8 | `p` | `Animated characters, combined with large language model AI technology, can assist visitors and create a more intuitive and personalized user experience.` |
| Gauge labels | `div` | `Materials`, `Lighting`, `X-Ray vision` |

The three gauge labels are the three segments of the arc gauge on this instance,
and they confirm that the selector changes more than colour here: one of the
three is a rendering mode, not a style.

**Facet.**

| Block | Class | String |
|---|---|---|
| Cover | `.mini` | `Product Showcasing` / `& Configuration` |
| Cover | `.h1` | `Facet` |
| Claim | `.mb-3` | `Your product is amazing... now let's` |
| Claim | `.h2` | `Make your product unforgettable.` |
| Claim | `.h4` | `Rally customers around your product and let them explore every detail with ease.` |
| Mechanism | `.t-high` | `Facet is the solution for` |
| Mechanism | `.h3` | `Product` / `Showcasing &` / `Configuration` |
| Mechanism 1 | `.h4` | `Production` |
| Mechanism 1 | `p.mt-3` | `We provide 3D assets, converted from CAD, scanned or modelled by hand.` |
| Mechanism 2 | `.h4` | `Web App` |
| Mechanism 2 | `p.mt-3` | `Interactive WebGL viewer with backend platform, always up-to-date, accessible anywhere.` |
| Mechanism 3 | `.h4` | `Engagement` |
| Mechanism 3 | `p.mt-3` | `Collect leads, track analytics & trends, share and amplify on socials.` |
| Feature 1 | `.h3` | `Lifelike Products` |
| Feature 1 | `p` | `Realistic creations from detailed shapes to beautiful materials, meticulously crafted to mirror the real world. Whether it's a car, sofa, or any item in your catalog, they are brought to life with unparalleled realism.` |
| Feature 2 | `.h3` | `Granular Detail` |
| Feature 2 | `p` | `Every minute detail gets attention. From stitching on upholstery to the gleam of metal parts. Our solution showcases your product in stunning clarity, allowing customers to appreciate its craftsmanship and quality.` |
| Feature 3 | `.h3` | `Configurable` |
| Feature 3 | `p` | `Customers are more and more demanding. Treat them to an experience where they can fully personalize your creation down to the finest specifications.` |
| Selector | `.h4` | `Give it a try` |
| Selector | `p` | `Select a color on the wheel above to change the product` |
| Feature 4 | `.h3` | `Animated` |
| Feature 4 | `p` | `Dynamic features are no problem, smooth, interactive animations, lets customers see how your product functions in real-time. Whether it's a sofa reclining or a lamp's light dimming, the possibilities are legion.` |
| Feature 5 | `.h3` | `Full Control` |
| Feature 5 | `p` | `Allow users to get close and personal with your product to get familiar with every single aspect of your amazing creation. The best way to showcase everything from functional info to clever design elements.` |
| Feature 6 | `.h3` | `WebAR Ready` |
| Feature 6 | `p` | `Let's get physical, as physical as possible. Treat your customers to the power of WebAR, they can visualize your product in their space. Blending the virtual and physical worlds sets up a deeper connection with your product.` |
| Feature 7 | `.h3` | `Seamless Integration` |
| Feature 7 | `p` | `Your website or webshop is all set with our viewer in mere minutes. Embed or inject the configurator anywhere you like, effortlessly. It's a plug-and-play solution that integrates smoothly, ensuring your store looks as polished as your products.` |
| Feature 8 | `.h3` | `Leads & Tracking` |
| Feature 8 | `p` | `Capture valuable insights. Our system not only tracks engagement but also helps you gather leads and data from their interactions. Gain deeper understanding into customer preferences and behaviors, all while optimizing your sales strategy.` |
| Closing | `.h0` | `Parade` / `Your` / `Product` |

**Services.** Heading pair: `.mini` `Explore our specialized`, `.h2`
`Services to amplify your next web project`.

| Anchor | Class | String |
|---|---|---|
| `#graphics` | `.h3` | `3D Web Graphics` |
| `#graphics` | `.h4` | `Bring Your Website to Life` |
| `#graphics` | `.h4` | `Transform Your Website with Next-Level 3D Graphics` |
| `#graphics` | `p.mt-4` | `Adding 3D images, videos or real-time graphics to your website is like adding special effects to a movie - it turns a functional project into an unforgettable experience. These dynamic visuals capture attention, engage users, and convey complex ideas in seconds, all while ensuring your website stands out in an increasingly crowded digital space.` |
| `#graphics` | `li.mt-3` | `Interactive 3D Models: Let your users explore products or concepts from every angle in real time.` |
| `#graphics` | `li.mt-3` | `Dynamic Animations: Add fluid, interactive animations that respond to user input.` |
| `#graphics` | `li.mt-3` | `Performance-Optimized: Real-time graphics without sacrificing loading speed or user experience.` |
| `#graphics` | `li.mt-3` | `Web-Ready: Compatible across devices and browsers, ensuring accessibility for all users.` |
| `#graphics` | `p.mt-4` | `We combine technical expertise with creative vision to build interactive 3D solutions tailored to your brand. From product configurators to immersive virtual showrooms, we'll make your website as captivating as a cinematic masterpiece.` |
| `#graphics` | `p.mt-4` | `Let your website make a lasting impact with real-time interactive 3D graphics - the special effects that turn browsing into an immersive journey.` |
| `#ui` | `.h3` | `Dynamic User Interfaces` |
| `#ui` | `.h4` | `The Secret Sauce to User Engagement` |
| `#ui` | `.h4` | `UI That Feels Natural, Works Beautifully` |
| `#ui` | `p.mt-4` | `A great user interface is like the perfect condiment on your favorite dish - it's the subtle addition that elevates the entire experience. We craft dynamic, intuitive UIs that guide users effortlessly through your digital product, making interactions smooth, logical, and even enjoyable.` |
| `#ui` | `li.mt-3` | `Dynamic UI Elements: Adaptable buttons, sliders, and forms that respond to user behavior.` |
| `#ui` | `li.mt-3` | `Responsive Design: Seamless experiences across devices, from desktop to mobile.` |
| `#ui` | `li.mt-3` | `Accessibility-First Approach: Ensuring all users, including those with disabilities, can engage fully.` |
| `#ui` | `li.mt-3` | `Tailored Interactions: Interfaces that reflect your brand and product needs, enhancing usability.` |
| `#ui` | `p.mt-4` | `We don't just design interfaces; we engineer experiences that users will remember. Our dynamic UIs reduce friction, boost conversions, and increase customer satisfaction.` |
| `#ui` | `p.mt-4` | `Think of our UI solutions as the secret sauce that enhances your digital product's flavor - making your users come back for more.` |
| `#assets` | `.h3` | `3D Asset Pipelines` |
| `#assets` | `.h4` | `Efficiency at Scale` |
| `#assets` | `.h4` | `Streamline Your 3D Asset Management` |
| `#assets` | `p.mt-4` | `Managing 3D assets can be time-consuming and resource-intensive. That's why we establish automated pipelines to handle asset conversion, optimization, and deployment seamlessly. With our solutions, your 3D content is always ready for real-time web applications, saving time and reducing errors.` |
| `#assets` | `li.mt-3` | `Automated Conversion: Convert CAD files, meshes, or other 3D formats into web-ready assets effortlessly.` |
| `#assets` | `li.mt-3` | `Optimization at Scale: Automatically reduce file sizes while maintaining visual quality.` |
| `#assets` | `li.mt-3` | `Version Control: Keep track of changes and updates across all assets.` |
| `#assets` | `li.mt-3` | `Integration with Existing Systems: Plug into your current workflow with minimal disruption.` |
| `#assets` | `p.mt-4` | `Our automated pipelines ensure your 3D assets are always optimized and ready for use. No more manual adjustments or delays - just efficient, scalable asset management.` |
| `#assets` | `p.mt-4` | `Let automation do the heavy lifting for your 3D assets, freeing you to focus on what matters most - delivering stunning 3D experiences to your users.` |
| `#cloud` | `.h3` | `Kubernetes Deployments for Big Data` |
| `#cloud` | `.h4` | `Scaling Made Simple` |
| `#cloud` | `.h4` | `Power Your Digital Infrastructure with Kubernetes` |
| `#cloud` | `p.mt-4` | `Handling big data requires robust, scalable infrastructure. Our Kubernetes deployments are designed to handle large-scale data processing with ease, ensuring your applications remain fast, reliable, and future-proof. Whether you're managing complex workflows or processing real-time data streams, Kubernetes keeps your system running smoothly.` |
| `#cloud` | `li.mt-3` | `Scalable Architecture: Automatically scale your infrastructure up or down based on demand.` |
| `#cloud` | `li.mt-3` | `Fault-Tolerant Systems: Ensure high availability and reliability for mission-critical applications.` |
| `#cloud` | `li.mt-3` | `Containerized Workflows: Manage applications and services in isolated containers for maximum flexibility.` |
| `#cloud` | `li.mt-3` | `Cost Efficiency: Optimize resource usage to keep operational costs under control.` |
| `#cloud` | `p.mt-4` | `We have deep expertise in deploying and managing Kubernetes environments tailored to your business needs. From data-intensive applications to real-time analytics, our solutions handle it all.` |
| `#cloud` | `p.mt-4` | `Embrace Kubernetes to power your big data workflows - ensuring scalability, reliability, and efficiency every step of the way.` |

Every discipline follows the same rhetorical shape: a simile in the first
paragraph, four capability bullets, a competence claim, and a closing line that
repeats the simile. Preserve that shape if the copy is ever rewritten; it is
what makes four long blocks readable in sequence.

**Case detail, the first instance.** Back link `.mini` `View` over `All cases`.

| Class | String |
|---|---|
| `h4.mb-4` | `Delta AI` |
| `h2.h2` | `Oil & Gas Data Visualization` |
| `a` then `p.ui-paragraph` | `Delta AI`, `, an Aberdeen based Oil & Gas analytics company with offices in the US and Canada, was looking for a powerful, user-friendly tool to visualize extensive oil and gas datasets at a planetary scale. The solution needed to integrate seamlessly with their browser-based analytics platform, enabling real-time exploration and deep analysis of subsurface data to support decision-making in resource management.` |
| `h3.ui-title` | `A Subterranean World` |
| `p.ui-paragraph` | `Our approach brings the power of subsurface data directly to users' screens, transforming complex datasets into an intuitive, interactive experience. Acting as a "subterranean Google Earth," the module lets users explore geological formations, well structures, and resource concentrations in real time.` |
| `h3.ui-title` | `Advanced Level of Detail (LOD) System` |
| `p.ui-paragraph` | `Built on a custom KD-tree-based LOD system, the app efficiently organizes terrain and geological data across massive areas. As users navigate, it dynamically loads data at the appropriate level of detail, supporting smooth, high-performance interaction, even at a global scale.` |
| `h3.ui-title` | `Optimized Oil and Gas Data Structuring` |
| `p.ui-paragraph` | `Delta AI's geological and well data is carefully partitioned to match the app's KD-tree, allowing swift access and clear visualization. By structuring data into 3D tiles, the app seamlessly displays construction data, volumetric geological information, layer and surface data, well and bore details, fracture points, and more, organized for swift exploration.` |
| `h3.ui-title` | `Comprehensive Data Layers and Color Mapping` |
| `p.ui-paragraph` | `The module integrates diverse data types and visualizations, from soil density to oil and gas concentrations. With customizable color gradients and layer options, users can adjust views to highlight specific data points, offering deep, contextual insights at a glance.` |
| `h3.ui-title` | `Intuitive 3D Controls and Interactive Navigation` |
| `p.ui-paragraph` | `Custom designed controls ensure users can intuitively explore this extensive subsurface data. Smooth zoom, pan, and rotation features make it easy to view intricate details or broad landscapes, helping users efficiently analyze and interpret complex structures and values.` |
| `h3.ui-title` | `Annotation and Collaboration Tools` |
| `p.ui-paragraph` | `With built-in annotation capabilities, the module allows users to mark specific areas, add comments, and share insights with their teams, creating a collaborative environment where findings and decisions can be easily documented and communicated.` |
| `h3.ui-title` | `Flexible Layering for Contextual Data` |
| `p.ui-paragraph` | `The app includes layering options, such as territorial overlays, restricted areas,... enabling users to add relevant context like political boundaries or environmental zones over the geological terrain. This flexibility helps users tailor the visualization to their specific analysis needs.` |
| `h3.ui-title` | `Strategic Well Management Features` |
| `p.ui-paragraph` | `Users can select and inspect individual wells, analyze detailed well bore and fracture data, and plan future well placements or maintenance strategies. Allowing users to optimize well operations with precision and foresight.` |
| `h3.ui-title` | `Seamless Integration with Delta AI's Analytics Platform` |
| `p.ui-paragraph` | `The viewer acts as a direct window into Delta AI's analytics platform, connecting visual data with in-depth analytics. This integration enables users to explore geological and well data visually while accessing sophisticated analytics tools, making the app a vital resource for strategic decisions across exploration, extraction, and resource management.` |
| `h3.ui-title` | `Result` |
| `p.ui-paragraph` | `The resulting 3D Visualization module strengthens Delta AI's bold vision to unify oil and gas data in a single platform and redefines how Delta AI's clients visualize, analyze, and interact with subsurface data. With a fully browser-based, real-time interface, users gain unprecedented insight into oil and gas resources, enhancing both accessibility and depth of analysis.` |

The media captions attached to the body panels of that case: `The level of
detail system in debug mode`; `Example of making the terrain see-through and
some surface layers being clipped`; `Example of some color gradient
configurations`; `Example of a cluster of highlighted areas and a bounded
subterranean volume`. They are the studio's own engineering notes and the most
distinctive copy on the site. Do not rewrite them into marketing. The remaining
six cases follow the same template and their bodies are yours to write in the
same voice.

**The contact route.** `.mini` `Hello`; `.h2` `How can` / `we assist` /
`you today?`; `.mini` `Send us an email` with the hover label `Copy email` over
the studio address `studio@prismlabs.co` set at `.h3`; `.mini`
`Visit our office` with the hover label `Copy address` over `Ridderstraat 118`,
`2200 Herentals` and the country line `Belgium`, beside a `Maps` label linking
out; `.mono` `Business Info` over the trading company `Meridian Comm. V.`, the
tax identifier `BE 0000 000 000`, and a second copyright line; and `.mini`
`Follow us` over two social profile links set as text.

**Shared strings.** The footer carries `contact`, `terms` and `privacy` as
lowercase links, a `div` reading the copyright symbol, the year and the studio
brand name, and a `.mini` reading `Back to top`. The navigation bar carries
`Home`, `Solutions`, `Services`, `Cases` and `Contact`, and its panels carry the
group categories `Data`, `Retail`, `3D` and `Web`. The cookie notice carries the
`.text` line, an underlined `Cookie Policy` and a `.button` reading `OK`. The
not-found route carries `.h1` `Page Not` / `Found` and `.mini` `Take me` over
`Home`.

## Technical requirements

The server produces the document for every public route and the interactive
pieces hydrate as islands over it, so the browser receives rendered markup on
first paint rather than an empty root and a script that fills it. Build the
front end with `SvelteKit`. Build the backend and its HTTP API with `Hono`, served on the same origin under
the `/api` prefix. Store data in `PostgreSQL`, reached at
`DATABASE_URL`. Store uploaded bytes in `minio`, the S3-compatible object store,
reached at `STORAGE_ENDPOINT` with the bucket named by `STORAGE_BUCKET` and the
credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Authentication is
email and password implemented by the app, with bearer tokens and hashed
passwords. `GET /api/health` returns `200` once the app is ready. Log one line
per request to stdout.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
`PostgreSQL` and `minio`, and reaching for anything else is a contract
violation.

Read every host, port and credential from the environment. Never hardcode one.
The backing services are already running at those variables and must not be
downloaded, installed, compiled or started.

**Metadata and sharing.** Every public route emits its own title, its own
description, its own canonical link and its own social preview title,
description and image, and no two routes share a title or a description. The
home route's title is the studio name followed by its positioning line, and its
description is `Researching and developing 3D web solutions for industry,
science and retail.` The three product routes carry a positioning phrase in
their titles and the utility routes carry their own subject. A case detail's
title is the case title with the studio name appended. The social preview
declares `og:type` as a website, `og:url` and `twitter:url` as the route's own
address, `og:title` and `twitter:title`, `og:description` and
`twitter:description`, and `og:image` and `twitter:image` as a preview image
that resolves, with `twitter:card` set to the large-image summary form. No
locale alternate is declared, because there is one language and one origin.

**Sitemap and robots.** `/sitemap.xml` lists every public route and only public
routes. `/robots.txt` points at it. Both are machine documents, not pages in the
navigation.

**Nothing the browser downloads carries a credential.** No API key, no admin
token, no database password and no object-store secret appears in any document,
script, stylesheet or source map the browser can fetch.

**The frame budget is the primary quality bar and nothing here outranks it.**
Every route holds sixty frames per second while scrolling on a three-year-old
laptop with the stage running. The first meaningful frame includes the stage: a
page that draws its typography first and its scene second has reversed the
product. A route change must not tear down and rebuild the drawing surface. Only
compositing properties change during scroll, and no scroll handler reads a
layout property, because the moment one does the frame budget is gone. Reveals
are class flips driven by intersection, the pinned blocks use the platform's own
sticky positioning, and the backdrop filter appears only on the three panel
classes.

**No external network call at run time.** Everything the product needs is inside
this environment.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

**accounts.** An id, an email that is unique and compared without regard to
case, a password hash, a role that is one of `editor` or `reader`, and a
creation time.

**solutions.** The three product lines. An id, a unique slug, a name, two
category lines, a theme that is one of `default` or `light`, a scene key
matching the class the document root carries, a claim figure and a claim
sentence, two closing display lines, the four parts of the footer call to action,
and a position that fixes the order.

**solution_sections.** An id, the owning solution, a kind that is one of
`mechanism` or `feature`, a heading, a body and a position. Exactly three
`mechanism` rows per solution; between six and nine `feature` rows per solution.

**services.** The four disciplines. An id, a unique anchor, a heading, a
navigation caption, a navigation sub-caption, a short promise, a long promise,
an opening paragraph, an argument paragraph, a closing paragraph and a position.

**service_bullets.** An id, the owning service, a label, a sentence and a
position. Exactly four rows per service.

**cases.** An id, a unique slug, a two-digit number that is unique across all
cases, a client, a title, a brief paragraph, a result paragraph, a status that is
one of `draft` or `published`, a published time that is null while the case is a
draft, a featured flag, and the cover media. Whether a case is publicly readable
is derived from `status`, never stored twice.

**case_sections.** An id, the owning case, an optional media element, an
optional media caption, a heading, a body and a position. Between eight and
eleven rows per case.

**media.** An id, the owning case, a kind that is one of `cover` or `body`, a
unique object key, a content type, a byte size, a digest of the bytes,
alternative text that is never null, a decorative flag and a creation time. The
object key is `cases/{case_id}/{sha256_of_bytes}.{ext}`. The row records where
the bytes are; the bucket is where they are. A decorative row carries the empty
string as its alternative text and sets the flag.

**enquiries.** An id, a name, an email address, an optional organisation, a
message, a submission time, the route it was sent from, and a read time that is
null until an editor marks it read.

**page_views.** An id, a route and the time of the view. One row per public page
view. Only an editor reads them.

**consents.** An id, a visitor token, whether analytics are allowed and when it
was decided. One row per visitor token.

**Invariants, as properties of the running system.**

- A case whose `status` is `draft` is absent from every public listing, denied on
  a direct read by slug to anyone who is not an `editor`, and its media objects
  are denied to the same people. Publishing makes all three readable in one act
  and unpublishing makes all three unreachable again.
- An object key is unique. Two uploads of identical bytes for one case resolve to
  one object, never two.
- A case number is unique across cases.
- Every media row carries alternative text; a decorative row carries the empty
  string and sets the decorative flag.
- A rejected enquiry writes nothing at all: no row, no partial row, no object.
- No page view is recorded before the visitor has answered the cookie choice.

**Seed data.** Three accounts, as listed in `## User roles`. Three solutions:
`Cirrus`, `Emporium` and `Facet`, in that order, each with exactly three
mechanism rows and at least six feature rows. Four services: `graphics`, `ui`,
`assets` and `cloud`, each with exactly four bullets. Eight cases: the seven
published ones listed in `## Core features`, numbered `01` to `07` in one
sequence, three of them featured, plus one draft numbered `08`, client `Kessel`,
title `Substation Twin`, slug `substation-twin`. Every case carries a cover
media row and between eight and eleven body sections. No enquiries and no page
views are seeded.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One tenant. There is no organisation, no team and no workspace.
- No search, no filter, no tag and no pagination anywhere, including on the
  cases index. That absence is a design decision: the index is the work.
- No blog, no news, no comments, no likes and no messaging between visitors.
- No language switch and no second locale.
- No cart, no payment, no pricing and no subscription. The product sells nothing
  and takes no money.
- No third-party analytics and no external network call at run time. The page
  view log is the app's own and is read only by an editor.
- No native application and no offline mode.
- No sitemap page in the navigation. The sitemap is a machine document.
- The build ships zero binary assets. Every texture, mark, font fallback, scene
  and media stand-in is generated.
- The stage's exact scroll trigger points were not recoverable from the source
  material and must not be hard-coded; they are set by eye against a running
  build, which is why reveals are driven by intersection rather than by offsets.
- The product must stay responsive with the seeded content and with a few
  hundred enquiries and a few thousand page-view rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not
  be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy
  of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password` | the created account and a bearer token |
| `POST /api/auth/login` | `email`, `password` | the account and a bearer token |
| `GET /api/health` | none | a health object |
| `GET /api/solutions` | none | a top-level array of solutions in position order |
| `GET /api/solutions/{slug}` | none | one solution with its mechanism and feature sections |
| `GET /api/services` | none | a top-level array of services with their bullets |
| `GET /api/cases` | none | a top-level array of published cases, newest published first |
| `GET /api/cases/{slug}` | none | one case with its sections and its result |
| `POST /api/cases` | `slug`, `number`, `client`, `title`, `brief`, `result` | the created case, in `draft` |
| `PATCH /api/cases/{slug}` | any editable field, or `status` | the updated case |
| `POST /api/cases/{slug}/media` | the bytes, `kind`, `alt_text`, `decorative` | the created media row with its object key |
| `GET /api/media/{id}` | none | the object's bytes, or a link to them |
| `POST /api/enquiries` | `name`, `email`, `organisation`, `message`, and the decoy field | the created enquiry |
| `GET /api/enquiries` | none | a top-level array, newest first |
| `PATCH /api/enquiries/{id}` | `read` | the updated enquiry |
| `POST /api/consent` | `analytics_allowed` | the recorded choice |
| `POST /api/page-views` | `route` | the recorded view |
| `GET /api/page-views` | none | a top-level array, newest first |

Field names are exact. A list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a
silent success. Bearer authentication is required on everything except signup,
login, health, the public read routes, the consent route and the enquiry
submission.

### No mocks

`minio` is where the bytes live. An in-memory buffer the app hands back to
itself, a file written to the app container's own filesystem, a base64 column in
`PostgreSQL`, or a hardcoded object key pointing at nothing are each a contract
violation however good the upload interface looks. The named provider is the
fact: the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A stranger can open the site, read the studio's argument across the home route
and a product line, open case `01` from the index into its full write-up, and
send an enquiry from the contact route that an editor then reads in the studio
console. A case the studio has not published is reachable by nobody outside the
studio, on any path, and its media is not served; publishing it makes the
listing, the address and the media readable in one act. Every uploaded byte
lives in the `minio` bucket at its scheme's key. The stage is painted behind the
first headline when the loader clears and keeps running on every route, and
navigating between a dark route and the pale one fades rather than cuts.
