# Norrgaard

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, scroll the whole
home route while its headings rise into place line by line, open the project index, switch it
between its three arrangements, open one project, press `Order design`, send an enquiry and
land on a confirmation address carrying its reference, without hitting an error page. A
project the studio has not published must stay invisible to that stranger, and so must its
pictures: every image the site shows is drawn by the app from a seed and its bytes must live
as real objects in the `minio` bucket at the key scheme below. An image the app keeps on its
own disk, or rebuilds on every request without ever storing it, is not a stored image.

## Overview

Norrgaard is the showcase site of an architecture bureau. It is not a shop and it does not
transact. Its job is to make a body of built work, and the thinking behind it, feel
considered and expensive, and then to collect one action: an enquiry.

The whole site is one continuous, smooth-scrolled surface. Text is set very large and
revealed line by line as it is scrolled into view. Pictures are full-bleed architectural
renders. The palette is monochrome. The effect is a gallery catalogue that happens to be a
website, and the type does all the work.

Four audiences arrive and each is served somewhere different: a prospective client wants the
buildings, the numbers and the offices; press and awards juries want the recognition and the
publications; an architect looking for work wants the philosophy and the faces; a returning
contact wants a phone number and an address. Behind all four audiences sits a studio editor
who keeps the content model current without a developer.

It deliberately is not several things. There is no payment, no subscription, no basket, no
comment, no rating, no newsletter, no notification of any kind, no search and no second
interface language. No photograph, font, audio or video file ships with the build: every
picture on the site is generated. The full scope-out list is in `## Constraints` and it is
part of the specification.

The genuinely hard part is that the site reads as one uninterrupted surface while three
different things drive it at once: a scroll controller that owns the whole document, a
picture layer under the upper half of the home route whose entire state is a function of
scroll offset, and a content model whose unpublished rows must be invisible in the pages,
in the API and in the object store at the same time.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `editor` | Read every project, published or not. Create, edit, publish and unpublish a project. Create and edit team members, offices, awards, publications, legal chapters and gallery photographs. Regenerate any image. Change the arc configuration. Read every enquiry received. | **Cannot delete an enquiry.** **Cannot read or change another account's password.** |
| `reader` | Read every published project, exactly as an anonymous visitor does. Read and change their own display name. Read the enquiries they themselves sent. | **Cannot read an unpublished project, its body, its images or its object keys, by any route.** **Cannot publish, unpublish, create or edit any content.** **Cannot read an enquiry sent by anybody else.** **Cannot read the arc configuration write surface.** |

An anonymous visitor has every `reader` read that concerns published content, and may send an
enquiry with no account at all. Nothing on this site requires a visitor to sign in.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `reader` session to any `editor`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

Signup is open. Anyone can create an account from the signup form and every signup creates a
`reader`. An `editor` account exists only by seed.

Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Display name | Role |
|---|---|---|
| `editor@example.com` | Anton Norrgaard | `editor` |
| `editor2@example.com` | Marta Eklund | `editor` |
| `reader@example.com` | Petra Lindqvist | `reader` |

## Core features

### Auth

The studio owns its own accounts. Each is an email, a password kept only as a hash that
leaves the service in no response on any route, and a role. Signing in mints a bearer token
that rides every later request for 24 hours. The public half of the site, signup, login,
health and the enquiry take no token at all, because a visitor has to be able to read the
whole showcase and write to the studio without an account.

1. An email that already belongs to an account cannot be signed up twice: the attempt is
   rejected as invalid, the form says which field is at fault, and the accounts table gains
   no row.
2. A correct email with a wrong password is rejected in the same words an unknown email
   gets, so the answer settles nothing about who has an account here.
3. A token that is missing, a token that has expired and a token that has been altered are
   each rejected as unauthorized, on every route outside that public half.
4. A signup always produces a `reader`. A request that asks for `editor` in its body is
   still a `reader` afterwards.

### The content model

Everything visible on the site is editorial content an `editor` maintains, and the front end
reads it rather than embedding it. Nothing on any page is hard-coded copy except the fixed
interface labels named in `## UI/UX notes`.

5. A project carries a slug, a title, a floor area in whole square metres, a category, a
   body, an order, and a published flag. The area renders with a thousands separator and a
   space before the unit: `58,079 m2`, never `58079 m2` and never `58,079m2`.
6. A team member carries a name, a role title, a portrait and an order. An office carries a
   label, a country, a city, a street and an order. An award carries a title, a detail and a
   year. A publication carries an outlet, a title and a detail. A legal chapter carries a
   two-digit number, a title and a body.
7. Every image in the model is an image reference carrying an accessible description, an
   aspect ratio and a generator seed. It carries no file path: the key is derived from the
   bytes once they exist.
8. Adding a project, a team member or an office is done entirely from `/studio`, with no code
   change and no restart.
9. The arc configuration is one editable record holding a frame count, a sweep angle, a
   radius ratio and a tilt step. Every parameter the fanned gallery uses comes from that one
   record.

### Published and draft

10. **A project that is not published is invisible to everybody but an `editor`.** It is
    absent from `/work` in all three view modes, absent from the home route, absent from
    every public API list, and its own address answers not-found rather than forbidden, so
    the index reveals nothing about what is being worked on.
11. **An unpublished project's image objects are not publicly readable.** Fetching the object
    key of a draft cover straight from the store, with no credential, must be refused by the
    store. A published project's cover must be readable the same way.
12. Publishing is an `editor` action and the only write that flips the flag. Publishing
    records when it happened. Unpublishing returns the project to invisible, including its
    objects.
13. A `reader` or an anonymous caller asking a public list endpoint for unpublished rows,
    by any query parameter, receives published rows only.

### Generated imagery in a real store

No photograph ships with the build. Every render, portrait and gallery photograph is drawn by
the application from its seed, at the aspect ratio its row records, and the resulting bytes
are put to the object store.

14. The object key is `projects/{project_id}/{sha256_of_bytes}.png` for a project cover or
    gallery frame, `team/{member_id}/{sha256_of_bytes}.png` for a portrait, and
    `gallery/{photo_id}/{sha256_of_bytes}.png` for an arc photograph. For example a project
    cover lands at `projects/7/3f9a1c...e0.png`.
15. The row records the object key and the digest of the bytes at that key, and the two
    agree: the digest in the row is the digest of the bytes the store holds.
16. Regenerating an image from the same seed produces the same bytes, so it lands at the same
    key and writes no second object.
17. The bytes live in `minio` and nowhere else. An image rebuilt on every request and never
    stored, a file on the app container's own disk, and a base64 column in PostgreSQL are
    each a contract violation however right the page looks.
18. An architectural render placeholder is a soft vertical value ramp from a light sky to a
    darker ground, a horizon band at roughly a third from the top, and one hard-edged
    rectangular block silhouette in a mid value, jittered by the seed so no two match. A
    portrait placeholder is a pale flat ground with a centred soft elliptical mass at the
    head-and-shoulders position. Both are monochrome: no hue enters a generated image.

### The home route

The long route, and the whole argument end to end. It runs as one continuous scroll from the
hero to the offices, with the picture layer behind its upper half and the line cascade
carrying the copy throughout.

19. The hero is a full-bleed architectural render filling the first screen, with the wordmark
    `Norrgaard Architectural Bureau` set bottom-left in the display serif at the top of the
    type scale. Its seven words `Norrgaard`, `Architectural`, `Bureau`, `Systematic`,
    `Clarity`, `&`, `Creativity` settle into place on first load, one word wrapper at a time.
20. A founding block pairs `Founded 2011` and `Founder Anton Norrgaard` with the services
    list and a paragraph of positioning copy, all delivered by the line cascade. The services
    list runs `Sustainability strategy, material efficiency, passive systems, energy
    modeling, lifecycle analysis` beside `Concept, facade and planning solutions, sketch
    project, working documentation, visualizations`, and the positioning paragraph reads
    `An architecture bureau rooted in precision and emotion. We design with a deep
    understanding of context, function, and timeless form, shaping environments that feel
    effortless, intuitive, and distinctly refined. From urban masterplans to boutique
    interiors, each project is tailored with vision and care.`
21. Two stacked lists follow. The awards list carries the `Kukha Design Award 2025` first
    place in the category `Public Building Architecture` and in
    `Completed Apartment Interior over 60 sq.m`, the `Addawards 2023` first places in the
    competition `Space` for `Garden Ring`, and ends on the summary line
    `Over 80+ awards in global competitions`. The publications list carries
    `Beautiful Apartments No. 5 (216) 2024`, `Archi.Ru Club House Little on Paveletskaya`,
    `Interior + Design Sales Office in a Historic Building from 1917`,
    `Lovethatdesign.Com A101 Office`, `Home & Garden Bolshevik Landscape Design` and
    `Fireplaces No. 2 (113) 2024, Fireplace in Modern Style`, and ends on
    `Over 20+ publications in the last year`.
22. A radial figure sits behind the large statement `Refined & Bold Essential`: eight fine
    lines radiating from the exact centre of a square box at forty-five degree intervals,
    each a straight run of points stepping outward, softened toward the rim by a radial fade
    so the burst reads as emerging from the centre. Eight numbered nodes, `01` through `08`,
    sit at the ends of the eight lines and name the eight chapters of the legal route. The
    figure fades in as the statement is reached and out as it leaves, tied to scroll offset.
23. A sketch section pairs a line drawing on white with the display statement
    `From Sketch to Strategy` and its supporting paragraph:
    `Early-stage ideas are distilled into precise frameworks, balancing intuition, analysis,
    and clarity. We begin with the essentials: sketches, diagrams, raw outlines. This is
    where we test the logic of space, the rhythm of circulation.`
24. **The arc history gallery.** Over a black ground, a set of studio photographs is arranged
    in a wide arc, a fan of tilted frames sweeping across the top of the section, with the
    large `15+ Years of experience` statement centred beneath. Frames are evenly spaced along
    the arc, individually tilted so each follows the tangent, and cast no shadow: the black
    ground does the separating. As the section scrolls the fan rotates and settles. Frame
    count, sweep angle, radius and tilt step all come from the arc configuration record, so
    the curve is adjustable in one place.
25. Three statistics follow over black, each a large sans numeral with a serif label, with
    photographs tumbling down one side in tilted frames: `490+ Completed projects`,
    `45+ Professionals on the team`, and the years-of-experience figure. The numeral is set
    in the sans and the label in the serif, and that pairing repeats for each figure.
26. A long two-column list of the studio's fifteen offices closes the route, each a role
    label, a city line and a street line, delivered by the line cascade.

### The reveal system

27. Every heading and paragraph that animates is split into per-line wrappers, each line
    clipped to its own box and set below its own baseline, and the lines rise into place.
    The largest display statements split one level finer, into per-word wrappers.
28. A section entrance plays the rise once, staggered line by line, when the block reaches
    the viewport, and never replays.
29. **In the long scroll regions the rise is tied to scroll offset, so scrolling back up
    returns the lines below their boxes rather than replaying them from the start.** Half way
    into such a block, the reveal is half done.
30. Splitting is idempotent and reversible. Leaving a route restores the original text nodes,
    and re-splitting after a width change neither nests wrappers nor counts a line twice.
31. Scrub weight follows the route: the home route is heavy, the about route is heavy, the
    contact route is moderate, the legal route animates only its line cascade, and the
    project index holds still with only its heading animating in.

### The picture layer

32. A full-viewport picture surface composites under the page content on the home route and
    the project detail route. It holds the large renders, the fanned arc frames and the
    circular-masked images, and it never paints its own opaque ground over the layout above
    it.
33. **Its entire motion is a function of scroll offset.** No independent timer drives any of
    it. Each element declares which span of the scroll drives it.
34. Certain gallery images are clipped to a full circle and drift and cross-fade past the
    viewer against the dark ground rather than sitting in a grid.
35. When the layer is scrolled out of range it stops drawing entirely rather than drawing
    cheaply, and it shares one animation frame callback with the scrubbed timeline instead of
    running a second loop.
36. The set of photographs bound into the layer, their order and their aspect ratios come
    from the content model, so the studio changes the gallery without a developer.
37. The layer does not switch layout at the breakpoint. It interpolates its arc parameters
    continuously with viewport width, so a resize reflows the fan smoothly rather than
    jumping, and it re-reads the mobile height correction on resize.

### The project index

38. `/work` lists every published project in a two-column offset grid where cards alternate
    left and right at staggered vertical positions, so the eye moves diagonally down the page
    rather than in tidy rows.
39. A small pill control floats at the bottom centre of the viewport with three options,
    `Grid`, `List` and `Gallery`, each carrying its own rectangle-built icon and its label.
    **The index opens in `List`.** Switching re-arranges one shared collection: `Grid` is the
    offset two-column grid, `List` is a single vertical column with the caption inline, and
    `Gallery` is a looser masonry of mixed-width frames.
40. The chosen mode is remembered for the session and survives a move to another route and
    back. A visitor who has chosen a mode gets that mode rather than the default.
41. Switching mode re-arranges the same rows client-side and preserves scroll context as far
    as the new arrangement allows. It fetches nothing and reloads no page.
42. A project card carries the full-bleed cover, the project name in the display serif as a
    real heading, the floor area in the secondary grey, and a `Visit` link with the diagonal
    arrow, carrying the same animated underline every other link has.
43. `Visit` opens that project's own address, carrying its title, its area, its body and its
    gallery photographs in the picture layer, under the same header, footer and entrance as
    every other route.

### The enquiry

The site's single state-changing action for a visitor. The footer's `Order design` and the
contact route both reach it.

44. The enquiry takes a name, an email address and a message, and needs no account. It opens
    as a modal over whatever route the visitor is on, and the contact route carries the same
    form inline.
45. **The three states are present in the markup and toggled, never injected**: idle, success
    and failure. Under no enhancement at all the form posts normally and the server answers
    with the confirmation page directly.
46. A sent enquiry is stored with a reference of twelve lowercase characters, unique across
    every enquiry, and the visitor lands on `/contact/sent/{reference}`, an address that can
    be bookmarked and reopened and that shows that reference.
47. **Every field rejects invalid input inline, names the field at fault, and writes
    nothing.** A missing name, an email address with no at-sign, and an empty message are
    each refused as invalid; the offending field carries the faint error tint and the
    enquiries table is unchanged.
48. **An enquiry submitted by a bot is refused.** The form carries an unattended decoy field
    that a person never sees and never fills, and a filled decoy is refused with nothing
    written. One origin that submits repeatedly, past `3` enquiries inside `3600` seconds,
    is refused the same way.
49. Sending the same enquiry twice, by a repeat of the submission, creates one row and
    returns the first reference. The visitor is not given a second reference for one message.
50. The whole action is completable by keyboard alone, and each of the three states is
    announced when it becomes the current one.
51. An `editor` reads every enquiry at `/studio/enquiries`, newest first, each with its
    reference and the time it arrived. A signed-in `reader` reads only the enquiries sent
    from their own account.

### The legal route

52. `/legal` carries a large display heading and eight numbered chapters, `01 Founding &
    Vision`, `02 Scope of Work`, `03 Design Philosophy`, `04 Sustainability`,
    `05 From Sketch to Strategy`, `06 Recognition & Reach`, `07 Global Presence` and
    `08 About This Site`, each a label that expands to a body of several paragraphs.
53. A chapter expands by growing its own height smoothly rather than appearing at once, and
    opens and closes on Enter and on Space as well as on a press, exposing whether it is open.
54. Each chapter carries real substance rather than a placeholder. `01` tells the founding
    in 2011 around three guiding values, systematic thinking, clarity and creativity, and the
    treatment of each commission as a dialogue between intuition and analysis. `02` sets out
    the scope of work across the full arc of a project, from concept development and facade
    and planning solutions through sketch projects to detailed working documentation and
    immersive visualizations. `03` describes a design philosophy rooted in precision and
    emotion, shaped by a deep understanding of context, function and timeless form, reaching
    from ambitious urban masterplans to carefully detailed boutique interiors, and designed
    to support the people who use a space rather than to impose on them. `04` puts
    sustainability at the heart of the practice rather than treating it as an afterthought,
    grounding every choice in passive design strategies, material efficiency, energy
    modeling and lifecycle analysis, aiming at architecture with lasting value and a lighter
    environmental footprint. `05` describes the method as a journey from sketch to strategy,
    beginning with sketches, diagrams and raw outlines that test the logic of space, the
    rhythm of circulation and the relationship between human behavior and built form, then
    refining each idea through dialogue into a grounded, adaptable and buildable direction.
    `06` records more than fifteen years of experience, over 490 completed projects and more
    than 45 professionals. `07` describes offices across Italy and the Netherlands.
    `08 About This Site` states plainly that the projects, awards, publications and offices
    shown are illustrative rather than strictly factual, and that the live client experience
    is at `norrgaard.pro`.
55. The legal route is the terms page: it is reachable from the footer of every route and is
    linked from the signup form itself.

### The public chrome

56. A fixed bar sits at the top of every route carrying the stacked wordmark
    `Norrgaard / Architectural / Bureau` on the left and a compact one-line index on the
    right: `Index`, `Work`, `About`, `Contact`, comma-separated. The bar does not hide on
    scroll.
57. **The navigation stays legible over every background it crosses by compositing against
    what passes behind it, never by swapping its own colour value at a section boundary.**
    Over the white hero sky it reads dark; over the black gallery section it reads pale; its
    own declared colour never changes.
58. Every text link carries an underline that wipes in from one edge on hover **and on
    keyboard focus**. The link of the route the visitor is already on has its underline
    already drawn and wipes it out on hover, which is how the site says "you are here".
59. The footer is a dark full-width block on every route holding the studio identity
    `Norrgaard Architectural Bureau`, a navigation column reading `Index`, `About`, `Work`,
    `Team`, `Contact`, `Order design`, a media column reading `Behance`, `Pinterest`,
    `Telegram`, `WhatsApp`, `Phone`, `Email`, `Channel`, the two office addresses
    `Via Giacomo Leopardi 14, 20123, Milano Italia` and
    `Keizersgracht 421, 1016, Amsterdam Netherlands`, the opening hours
    `Mon to Fri 10:00 AM, 7:00 PM` and `Sat to Sun 12:00 PM, 5:00 PM`, and a legal row
    carrying the licence numbers `IT-AR-2023-15847` and `NL-BA-08576321`, the credits
    `Visual Design Luca Serrano` and `Development Kai Andersen`, a link to the legal
    documents and the copyright year. The seven media entries are text rather than links:
    nothing on this site reaches an address outside it.
60. The `Team` entry in the footer is not a route of its own: it reaches the team section of
    the about route.
61. **Every internal link on every public route resolves.** A footer entry, a navigation
    link or a `Visit` link that answers not-found is a defect of the page that carries it.
62. On first load a full-screen cover holds until the fonts and the first screen are ready
    and then clears. Moving between routes wipes a brief cover across the swap so content
    never pops.
63. **A route change re-runs the incoming route's entrance sequence, updates which navigation
    link is marked active, and puts scroll back at the top of the incoming route.** Every
    route is also a real address: opening one cold in a fresh browser answers with the
    finished page rather than a shell that fills itself in afterwards.

### The about and contact routes

64. `/about` opens on an intro: the heading
    `Architects, designers, engineers, a team built on ideas and precision`, then
    `Our Philosophy` and the same positioning paragraph the home route carries, then the
    sustainability line `Our sustainable design principles combine material efficiency and
    life analysis with innovative concepts. We connect architectural ideas and final forms
    through clear visualization and coordination.`, all delivered by the line cascade over a
    dark ground. It closes on the studio's awards: the `Kukha Design Award 2025` first place
    in the nomination `Realized interior of an apartment from 60 sq.m.`, the
    `Beautiful Homes Press Fireplace Design 2024` first place in the nomination
    `Modern fireplace` for `Pevchee`, the `Kukha Design Award 2025` first place in the
    category `Public Building Architecture` for `Riverside`, and the
    `Best Interior Festival 2023`.
65. The team grid holds the twenty seeded members, four across on desktop and staggered
    vertically so rows interleave, each a portrait on a pale studio backdrop with the name in
    the display serif and the role beneath it in the secondary grey.
66. `/contact` opens on an intro, the display statement
    `Norrgaard Architectural Bureau is an architecture bureau driven by clarity, context, and
    craft, shaping thoughtful spaces at every scale.` and carries three labelled contact
    groups, `Technical` at `support@norrgaard.com` on `+39 06 87654321`, `General` at
    `info@norrgaard.com` on `+31 6 23456789` and `Sales` at `sales@norrgaard.com` on
    `+39 06 12345678`, each set large in the serif, with the two office addresses beneath
    them: `Via Giacomo Leopardi 14, 20123, Milano Italia` and
    `Keizersgracht 421, 1016, Amsterdam Netherlands`.

### The not-found route

67. An address that is not found answers not-found and renders the studio's own page: the display
    statement `Page doesn't exist`, the line `please return to the home page`, a `home page`
    link, and the paragraph `Even in architecture, not every path leads to the right place,
    so please return to the home page and let's create something meaningful.` It wears the
    same header and footer as every other route.
68. The document title of a not-found response says so. A page that answers not-found while
    the browser tab still claims to be a real route is a defect.

### Page views

69. Every page view is recorded with its route and the time it happened, and an `editor`
    reads them back. No view is sent anywhere outside this application.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the home route, hero to offices | public |
| `/work` | the project index in three modes | public |
| `/work/{slug}` | one project, its body and its gallery | public |
| `/about` | philosophy, sustainability, the team grid, awards | public |
| `/contact` | the contact groups and the enquiry form | public |
| `/contact/sent/{reference}` | the enquiry confirmation | public |
| `/legal` | the eight expanding chapters | public |
| `/signup` | create a reader account | public |
| `/login` | sign in | public |
| `/account` | the signed-in account and its own enquiries | reader |
| `/studio` | the editor's content index | editor |
| `/studio/projects/{id}` | edit one project | editor |
| `/studio/enquiries` | every enquiry received | editor |

**Entry and redirects.** An unauthenticated request for `/studio` or `/account` goes to
`/login` with the destination remembered and lands there after signing in. A `reader` opening
`/studio` is refused rather than redirected, because the route exists and the account may not
have it. Signing out returns to `/`. A signed-in visitor opening `/login` is sent to `/`. An
expired token mid-action returns the visitor to `/login` with nothing written. An unknown
address renders the not-found page with a not-found response. An unpublished project's slug
answers not-found to anybody but an `editor`.

**Journeys.**

1. A visitor opens `/`, scrolls the whole route and watches the headings rise line by line,
   the radial figure fade in behind `Refined & Bold Essential`, the arc of photographs rotate
   and settle over `15+ Years of experience`, and the offices list close the page.
2. The visitor scrolls back up through the arc section and the lines drop back below their
   boxes rather than replaying.
3. The visitor opens `/work`, reads it in `List`, switches to `Gallery`, presses `Visit` on
   `Almaty Hotel Ornament Stone`, and reads its body and its gallery.
4. The visitor presses `Order design` in the footer, fills the modal with a name, an email
   and a message, sends it, and lands on `/contact/sent/{reference}` showing the reference.
5. The visitor submits the form again with the message empty and the email missing its
   at-sign: both fields are named, both carry the error tint, and nothing is written.
6. `editor@example.com` signs in, opens `/studio`, publishes `Vantaa Timber Pavilion`, and
   the project appears in `/work` with its cover readable from the store.
7. `reader@example.com` signs in, opens `/account`, reads their own enquiries, and is refused
   at `/studio`.

**States.** Every list has an empty state written in the studio's own words: a project index
with nothing published, a studio enquiry list with nothing received, an account with nothing
sent. Every route has a loading cover on first paint rather than a flash of unstyled text.
The enquiry form carries its three states in the markup at all times. An error never blanks
the page: it is shown in place, on the surface the visitor was already on.

## UI/UX notes

The site should read as a gallery catalogue that happens to be a website, not as an interface
with content in it. Somebody should understand in the first screen that this studio is
expensive and considered and that the buildings are the point. The register is editorial: the
type does all the work, the pictures carry all the warmth, and nothing shouts except the size
of the display face. The motion character is `eased`, one house curve everywhere, quick to
leave and long to arrive, which is what gives the whole site its unhurried feel.

**Colour, by role.** There is no brand colour and none may be introduced. Primary text on
dark grounds and the light section grounds are the lightest near-white neutral in the set,
and that value dominates the page by roughly four times the next. Text on light grounds, the
gallery grounds and every icon fill are a near-black neutral. Secondary and de-emphasised
text, captions and role lines are a single light neutral grey, and that grey stays secondary:
it is the second most used value and it never carries a primary message. The page ground is a
near-white neutral one step off the lightest; hairlines and light fills, borders and
dividers, raised light surfaces and faint strokes are further near-white neutrals shading
toward the grey end of that band; the picture layer clears to a near-black neutral just off
black. Four values carry transparency and are washes rather than fills: two scrim blacks
under shadows and underlays, a near-black lower stop for the gradient that darkens the bottom
of a photograph so white text stays readable on it, and a faint red tint that appears on a
form field needing attention and on nothing else in the entire build. No fifth grey and no
hue may enter. The exact values are yours so long as every rule above holds, including the
rank.

**Type.** No font binary ships and naming a family is not a dependency. The interface role is
`"Neue Haas Grotesk", "Helvetica Neue", Arial, system-ui, sans-serif` and the display role is
`"Playfair Display", "Times New Roman", Georgia, serif`, both at weight `400`, both loaded
with a swap fallback so text paints immediately in a system face and reflows when the web
font arrives. Root sizing is viewport-derived: one scaling rule ties the root size continuously to
viewport width, which is why the rendered scale is fractional. Reproduce the scaling rule and
the fractions follow, rather than transcribing the sizes as fixed values. The scale in rank of use is body and interface at `14.56px` on
`17.472px`; small labels, captions and footer at `12px` on `14.4px`; the smallest legal and
credit text at `8.25px` on `9.9px`; an intermediate at `20.625px` on `22.6875px`; sub-heads at
`27.04px` on `29.744px`; section labels at `30px` on `33px`; small display at `37.44px` on
`33.696px`; mid display at `60px` on `48px` and `60.8438px` on `54.7594px`; large display at
`88.5px` on `79.65px` and `91.2656px` on `77.5758px`; and the hero wordmark and the largest
statements at `132.75px` on `112.838px`. At the narrowest width the top of the scale
compresses toward `131.25px` and `90.2344px` with body around `14.25px`. Three tracking
values, `0.75px`, `1.04px` and `0.515625px`, apply only above the mid-display size. The ratio
of the largest display to the body approaches ten to one, and that ratio is the design.
Figures use tabular forms wherever amounts stack, which is the statistics and the floor areas.

**Depth, shape and space.** There is almost no depth here and that is the point. One raised
control group carries small radii and lifts on the y axis as it settles; the circular gallery
images are clipped to a full circle; everything else is square, and a rounded corner
appearing anywhere outside that one control group is the first sign the design has drifted.
Spacing is three tokens expressed in ems so they scale with the viewport-derived root: a
standard block gap, a tighter gap under a heading, and a small offset used by the underline
and the chip insets. Space over dividers, throughout: sections read as separate because of
the room between them, not because of a rule drawn across them.

**Components and their states.** Every control has a resting, pointed-at, pressed, focused
and unavailable state, and unavailable is never signalled by colour alone. Every text link
carries an underline drawn by a pseudo element that scales from one edge; a non-active link
sits with it collapsed and wipes it in on hover and on focus, and the active route's link
sits with it drawn and wipes it out on hover. The `Visit` link on a project card is the same
component wearing the diagonal arrow. Escape closes the enquiry modal and returns focus to
the control that opened it. The view-mode pill is one tab stop with arrow keys moving between
its three options.

**Motion.** Every movement on the site is one of three mechanisms, and only three: a declared
transition that runs on hover, focus or a state change; a trigger-once reveal that plays
forward when an element enters the viewport and never replays; and a scroll-scrubbed timeline
whose progress is a function of scroll offset, so scrolling back un-plays it. Nothing else
drives anything. Motion here is continuous rather than incidental, and it is one idea done
very well: text arrives a line at a time. Every heading and paragraph is split into per-line
wrappers, each clipped to its own box and set just below its own baseline, and the lines rise
into place a beat apart like cards being dealt; the largest statements split one level finer
into per-word wrappers and settle on first load. In the long scroll regions the rise is tied
to scroll position rather than to a timer, so scrolling back up drops the lines back out of
sight instead of replaying them. Beyond that the movement is small and physical: underlines
that wipe in, a chapter that grows open like a well-made drawer, one section that inverts its
ground and its text together, a button that settles rather than reacting, and a cover that
wipes across on load and between routes. Everything shares the one house curve. Under a
request for reduced motion, smooth scrolling falls back to the browser's own scrolling, every
cascade resolves to its end state and simply appears, every scrubbed timeline is set to its
end and unbound, the picture layer renders one static frame and stops drawing, and both
covers become an instant cut rather than being removed and leaving a jump.

**Layout and scroll.** One real breakpoint, around the width of a large phone, with the
desktop layout above it and a rebuilt single-column layout below it; almost all the
responsive work lives on the narrow side. At the narrowest **viewport** the bar shrinks, the
display type is dialled back so it still fits, and the project grid, the team grid, the
offices list and the statistics each stack into one column, carrying the same content rather
than a reduced set. One smooth-scroll controller owns scroll position for the whole document,
exposes a normalised progress for every scrubbed element, and stops while any cover or modal
is open. Layering uses a named scale rather than ad hoc numbers: content low, the raised picture band
above it, sticky chrome above that, and one top band reserved for the loader and any
full-screen cover. Nothing may sit above that top band, and no element may invent a layering
value outside the scale.

**Iconography and generated imagery: the zero-asset substitution guide.** The site is almost
iconless by design and every mark is inline geometry rather than a file: there is no icon
font and no image request anywhere in the build. The substitution is total, and it is the
same one everywhere: where a binary would have been fetched, a generator draws a stand-in. The set is the studio wordmark, one fine hairline diagonal arrow pointing up and
to the right that means "go", three rectangle-built view-mode glyphs drawn as little diagrams
of their own arrangement (staggered bars for the list, a neat field of squares for the grid,
uneven bars for the looser gallery), and the radial figure. The arrow reads pale on dark
grounds and dark on light ones. The radial figure is the one graphic that is a picture rather
than a control: eight fine lines radiating from the exact centre of a square box at
forty-five degree intervals, every stroke inheriting the current text colour, over a
three-stop radial gradient that fades them toward the rim. Render and portrait placeholders
are drawn from their seeds as described in `## Core features` and stay monochrome.

**Accessibility.** One heading per route. The bar is a banner landmark, the footer a
content-info landmark, the navigation a labelled navigation landmark, and headings descend
without skipping a level; a giant display statement that is not the route's true heading is
typography and belongs in a non-heading element, so a screen reader is not handed a wall of
oversized headings. A project title stays a heading. Every link, every view-mode option,
every legal chapter and every enquiry field is reachable in a sensible order with a visible
focus ring, and the underline feedback fires on focus and not on hover alone. **Body text and
its background meet the WCAG AA contrast bar**, and the one grey is checked specifically at
the two smallest sizes and raised wherever it carries meaning rather than left as it is
because it looks calmer. **Every generated project photograph and every team portrait carries
its own alternative text** from the content model, describing what the image shows; the
picture layer and the radial figure are decorative and are hidden from assistive technology
entirely. Meaning is never carried by colour alone, and full keyboard navigation reaches
every control on every route.

**Copy that is pinned.** The navigation reads `Index`, `Work`, `About`, `Contact`. The
footer identity reads `Norrgaard Architectural Bureau` and its navigation column reads
`Index`, `About`, `Work`, `Team`, `Contact`, `Order design`. The view modes read `Grid`,
`List`, `Gallery` and the card action reads `Visit`. The hero words are `Norrgaard`,
`Architectural`, `Bureau`, `Systematic`, `Clarity`, `&`, `Creativity`. The home statements
read `Refined & Bold Essential`, `From Sketch to Strategy` and `15+ Years of experience`, and
the statistics read `490+ Completed projects` and `45+ Professionals on the team`. The
not-found route reads `Page doesn't exist` and `please return to the home page`.

**What it must not be.** This is a catalogue, so it is none of the shapes a studio site
usually defaults to: a dashboard, or an agency landing page with a hero and three cards
below it. No page dominated by a single hue family with no second
signal. No decoration standing in for content. No soft shadow scale creeping in beside the
one raised control group. The failure to design against is a site that looks like a content
management system wearing a serif.

## Technical requirements

Every route is produced on the server: the app is a server-rendered multi-page application
built with **Django** and its template layer, so a browser opening any address cold receives
finished markup with no client framework and no client router. The front end is **vanilla
progressive enhancement**: hand-written JavaScript layered over markup that already works
without it. The smooth-scroll controller, the line splitter, the scrubbed timeline, the
picture layer, the view-mode pill, the legal accordion and the enquiry modal are each an
enhancement over a page that is already correct when the enhancement is absent.

The datastore is **PostgreSQL**, reached at `DATABASE_URL`. Generated image bytes live in
**MinIO**, reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Every one of these is read from the environment and never hardcoded.
Both services are already running.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor. The only backing
services available in this environment are `postgres` and `minio`, and reaching for anything
else is a contract violation.

Auth is implemented by the app: email and password, passwords stored hashed, a bearer token
returned on login and required on every write and on every editorial read, expiring after 24
hours. The enquiry path takes no token.

`GET /api/health` returns `200` once the app can reach both PostgreSQL and the object store.
Request logging is structured, one line per request, and never carries a password, a token or
an email address.

**Every public route carries its own title and its own description, and no two public routes
share either.** A route that answers not-found says so in its title as well as its status.

No credential, no token and nothing usable to sign in appears in anything the browser
downloads, and no address outside this application is referenced anywhere in the build: no
font service, no content delivery host, no analytics endpoint, no social widget, no map.

**Performance is a budget, not an aspiration.** The largest contentful paint arrives under
`2500` milliseconds on a mid-tier laptop over a home connection. The picture layer holds a
steady `60` frames per second on a three-year-old laptop, and so does every other route.
Layout shift after the loading cover hands over is zero. The build meets those budgets by
construction rather than by tuning: the reference this site is modelled on spent over one
hundred megabytes on photographs and packed textures, and the zero-asset substitution guide
of `## UI/UX notes` removes that entire budget by generating every picture instead of
downloading one.

Only transform and opacity are animated during a scroll. The two exceptions are the clip on
the reveal wrapper and the height on the legal accordion, and the hint that a property will
change is declared on those elements and nowhere else: hinting everything is worse than
hinting nothing. The line splitter batches its per-line writes rather than reading layout
back mid-write.

The module boundaries are chrome, footer, reveal, scroll, media, figure, work, statistics,
accordion, forms and router, and each owns its own setup and teardown. Teardown is not
optional: anything that survives a route change leaks, and the site gets slower the longer
somebody browses.

A full-height section at the narrow width sizes from a script-maintained height that accounts
for the collapsing browser chrome, not from a raw viewport-height unit, so a section does not
jump as the bar slides away. That height is re-read on a resize.

**Scene behaviour across a resize.** The picture layer does not switch layout at the
breakpoint. Its arc parameters interpolate continuously with viewport width, so the scene
behaviour under a slow window drag is a smooth re-spread of the fanned frames rather than a
jump from one arrangement to another.

## Data model

Twelve tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

### accounts

`id`, `email` (unique, stored lowercased), `password_hash`, `display_name`, `role`
(`editor` or `reader`), `created_at`. No endpoint ever returns `password_hash`.

### projects

`id`, `slug` (unique), `title`, `area_sqm` (integer), `category`, `body`, `order`,
`is_published` (boolean), `published_at`, `created_by`, `updated_at`.

### project_images

`id`, `project_id`, `kind` (`cover` or `gallery`), `object_key`, `byte_digest`, `ratio`,
`alt_text`, `seed`, `order`. Unique on `(project_id, kind, order)`.

### team_members

`id`, `name`, `role_title`, `portrait_object_key`, `portrait_digest`, `portrait_alt`, `seed`,
`order`.

### offices

`id`, `label`, `country`, `city`, `street`, `order`.

### awards

`id`, `title`, `detail`, `year`, `order`.

### publications

`id`, `outlet`, `title`, `detail`, `order`.

### legal_sections

`id`, `number`, `title`, `body`, `order`. Eight rows, numbered `01` through `08`.

### gallery_photos

`id`, `object_key`, `byte_digest`, `ratio`, `alt_text`, `seed`, `order`.

### enquiries

`id`, `reference` (unique), `name`, `email`, `message`, `account_id` (null for an anonymous
sender), `origin_fingerprint`, `created_at`.

### arc_settings

`id`, `frame_count`, `sweep_degrees`, `radius_ratio`, `tilt_step_degrees`, `updated_at`. One
row.

### page_views

`id`, `route`, `account_id`, `viewed_at`.

### Invariants

1. An unpublished project is readable by an `editor` alone. Its rows, its body, its image
   rows and its object keys are absent from every public read, and its objects are not
   readable from the store without a credential.
2. Every published project's cover bytes exist in the object store at the key its row
   records, and the digest the row records is the digest of those bytes.
3. An enquiry reference is unique across the table, and one submitted message produces one
   row however many times the submission is repeated.
4. `is_published` changes only through the publish and unpublish actions, and only for an
   `editor`.
5. A refused enquiry, whether refused for invalid input or as a bot, writes no row.
6. Seeding is idempotent.

### Seed data

Three accounts, as listed in `## User roles`, each with the password `deku-demo-pw-2026`.

Twelve `projects` rows. Ten are published, with these titles and areas:
`Pokrovskoe Private House` at `611 m2`, `Millenium Private Park` at `1,360 m2`,
`Bolshevik Residential` at `8,200 m2`, `KNS Stolbovo` at `3,345 m2`,
`Kotelnaya Kinetics` at `16,488 m2`, `Vision Mansion` at `991 m2`,
`Almaty Hotel Ornament Stone` at `58,079 m2`, `Eli House Corner Plot` at `435 m2`,
`Riverside Restaurant` at `1,226 m2` and `Peredelki Mansion` at `334 m2`. Two are
unpublished: `Vantaa Timber Pavilion` at `2,140 m2` and `Ostuni Cliff House` at `780 m2`.
Every project carries one cover image row and three gallery image rows.

Twenty `team_members` rows, the first `Anton Norrgaard`, `Art director`, then
`Marta Eklund`, `Petra Lindqvist`, `Jonas Vidal`, `Sofia Marchetti`, `Lena Halvorsen`,
`Rafael Costa`, `Nadia Berger`, `Clara Fontaine`, `Ines Moreau`, `Greta Solberg`,
`Mattis Roux`, `Viktor Aalto`, `Mira Castellano`, `Elin Dubois`, `Hanna Vogel`,
`Elena Ferrari`, `Nora Persson`, `Alba Romano` and `Livia Novak`.

Fifteen `offices` rows, the first `Head office`, `Italy`, `Rome`,
`45 Casa di Maydwell Via Thomas`, the rest across Milan, Amsterdam, Rotterdam, Florence,
Utrecht, Venice, The Hague, Bologna, Eindhoven, Turin, Groningen, Naples and Tilburg.

Nine `gallery_photos` rows for the arc. Eight `legal_sections` rows. One `arc_settings` row
holding a frame count of `9`, a sweep of `120` degrees, a radius ratio of `1.4` and a tilt
step of `7` degrees.

Seeding must be idempotent: restarting the app must not duplicate rows, and it must not write
a second object for an image whose bytes are already in the store.

## Front-end specification

### The chrome

The fixed bar carries the stacked wordmark on the left and the four comma-separated links on
the right. It does not hide on scroll and it does not grow. It is painted so that it inverts
whatever passes behind it, which is what keeps one declared colour legible over both the
white hero sky and the black gallery ground. Its height at the narrow width is smaller than
at the wide width, and that height is published as a single value every in-page anchor reads
rather than repeated.

### The home route

Seven movements in one continuous scroll: the hero render with the wordmark bottom-left; the
founding and services block; the awards and publications lists; the radial figure behind
`Refined & Bold Essential`; the sketch section; the black arc gallery over
`15+ Years of experience`; the statistics; the offices list. The picture layer sits behind
the upper half and there is no visible seam where it meets the layout above it.

### The project index

The mode pill floats at the bottom centre, three options with their glyphs and labels, the
active one marked. Cards in `Grid` and `Gallery` sit at staggered offsets; `List` is a plain
single column with the caption inline. Every card is a full-bleed cover with the title, the
area and the `Visit` link beneath it.

### The enquiry modal

`Order design` opens the form over the current route, with the route behind it inert and the
smooth-scroll controller stopped. The three states live in the markup. A field needing
attention carries the faint tint and names itself. Escape closes the modal and returns focus
to the control that opened it. Sending takes the visitor to the confirmation address.

### The legal accordion

Eight numbered labels, each opening to its body by growing its own height. Only one needs to
be open at a time but more than one may be. Each exposes whether it is open, and each opens
from the keyboard.

### Generated assets only

No image file, font binary, audio file or video file is referenced anywhere in the build, and
no address outside this application is fetched at run time. Every mark, figure, render
placeholder and portrait placeholder is drawn by the application from its own seed.

## Constraints

Single studio: there is one bureau, one content model and one set of enquiries. There is no
tenancy and no second organisation.

Not in this product, and not to be built:

**Commerce.** No payment, no subscription, no basket, no price, no quote and no transaction
of any kind. The enquiry is a message, not an order.

**Visitor-written content.** No comment, no rating, no review, no forum and no text one
visitor can read from another. The enquiry is visible to its sender and to an `editor` alone.

**Messaging.** No email is sent, no notification is pushed and no reminder is scheduled. An
enquiry is stored and read in the studio surface; nothing leaves the application.

**Search and filtering.** No search box, no faceted filter and no sort control. The project
index shows one ordered collection in three arrangements.

**Internationalization.** One interface language, left to right. No locale switch, no
translated content model and no currency.

**Everything external.** No third-party script, no analytics vendor, no social widget, no
embedded map, no font service, no content delivery host and no external network call at run
time. No native application. The media entries in the footer are text, not links to another
site.

**Scale and operations.** One region, one database, one object store, no read replica, no
cache layer, no queue and no background worker. Image generation happens in the request that
needs it.

The app must stay responsive with `12` projects, `48` project images, `20` team members,
`15` offices, `9` gallery photographs, `500` accounts and `5000` enquiries.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
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
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{"email", "password", "display_name"}` | the account and a bearer token |
| `POST /api/auth/login` | `{"email", "password"}` | the account and a bearer token |
| `GET /api/auth/me` | none | the signed-in account |
| `GET /api/projects` | optional `mode` | a top-level JSON array of published projects in order |
| `GET /api/projects/{slug}` | none | the project, its body and its image rows |
| `POST /api/projects` | `{"slug", "title", "area_sqm", "category", "body", "order"}` | the created project, unpublished |
| `PATCH /api/projects/{id}` | any writable project field | the updated project |
| `POST /api/projects/{id}/publish` | none | the published project with `published_at` set |
| `POST /api/projects/{id}/unpublish` | none | the project, no longer published |
| `POST /api/projects/{id}/images` | `{"kind", "ratio", "alt_text", "seed", "order"}` | the image row with its `object_key` and `byte_digest` |
| `GET /api/team` | none | a top-level JSON array of team members in order |
| `GET /api/offices` | none | a top-level JSON array of offices in order |
| `GET /api/awards` | none | a top-level JSON array of awards |
| `GET /api/publications` | none | a top-level JSON array of publications |
| `GET /api/legal` | none | a top-level JSON array of the eight chapters in order |
| `GET /api/gallery` | none | a top-level JSON array of the arc photographs in order |
| `GET /api/arc-settings` | none | the one arc configuration record |
| `PATCH /api/arc-settings` | any of `{"frame_count", "sweep_degrees", "radius_ratio", "tilt_step_degrees"}` | the updated record |
| `POST /api/enquiries` | `{"name", "email", "message", "company"}` | the stored enquiry and its `reference` |
| `GET /api/enquiries` | none | a top-level JSON array of enquiries, newest first |
| `GET /api/page-views` | none | a top-level JSON array of recorded views |
| `GET /api/health` | none | `200` |

Field names are exact. `company` on the enquiry is the unattended decoy of rule 48 and is
expected to be empty. Every list endpoint returns a top-level JSON array. A successful call
returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason. Bearer auth is required on every endpoint except signup, login, health, the public
content reads and the enquiry write.

### No mocks

`minio` is the only place a generated image's bytes live, and `postgres` is the only place the
content model lives. An in-memory dictionary of image bytes, a directory of PNG files on the
app container's own disk, a base64 column in PostgreSQL, an image endpoint that redraws from
the seed on every request without ever having written the object, and a stubbed success
response the app returns to itself are all contract violations, however right the site looks.
The named provider is the fact: the app's pages and its own tables can only reflect what lives
in the provider, never substitute for it.

## Definition of done

A stranger can scroll the whole home route watching the headings rise and the fanned arc
settle, read the project index in any of its three arrangements, open a building and send an
enquiry that lands on its own confirmation address. A project the studio has not published is
invisible to that stranger everywhere, its pictures included. Every picture on the site was
drawn by the app from a seed and its bytes are real objects in the store at the key the row
records.
