# Northform Immersive Studio Showcase

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, watch the loader
hand off to the home route, open the published case study `Grand Opera of Verdal` from the
reel, and send a contact enquiry that is stored, without hitting an error page. A different
stranger must NOT be able to read the draft case `Harbour Line Rebrand` or fetch its hero
image, by any means, and neither must a signed-in reader. The uploaded bytes must live in
the MinIO bucket at their scheme's key; a copy on the app's own disk does not count, and a
green tick the app returns to itself does not count.

## Overview

Northform is a multidisciplinary creative studio at the intersection of art, design and
technology, and this is its own site. The site's job is not to transact. It is to prove, by
being one, that the studio can build an emotional and technically demanding web experience,
and then to collect exactly two actions: a contact enquiry and a newsletter subscription.

The proof is delivered as spectacle. A loading sequence in which a mascot runs inside a
filling ring, a full-viewport real-time three-dimensional layer composited behind the page, a
headline that assembles letter by letter out of depth, an ambient bed the visitor can mute,
and a portfolio whose colour temperature changes as you move through it, because every project
carries its own accent. Four audiences arrive: a company with a project, somebody
job-hunting, a journalist or peer, and a past contact looking for the right address.

Behind the spectacle sits an ordinary editorial product. Case studies, journal posts and open
roles are written, given media, and published. Northform deliberately is not a shop, a client
portal, a comment thread or a search engine: there is no commerce, no payment, no messaging,
no rating, no follower and no analytics vendor.

The genuinely hard part is that a piece of work is not public until it is published, and that
has to hold for the record and for the bytes. A draft case study's hero image sits in the same
bucket as a published one, and listing the bucket, guessing a key, or holding a link minted
while the case was published must not read it.

## User roles

| Role | Can do |
|---|---|
| `author` | Read every case, post and role in either state. Create, edit, publish and unpublish. Upload media. Read the page-view log. Everything a `reader` can do. |
| `reader` | Read every **published** case, post and role, exactly as an anonymous visitor does. Send an enquiry and subscribe. |
| anonymous visitor | Read every **published** case, post and role. Send an enquiry and subscribe. Sign up as a `reader`. |

**A `reader` cannot** read a draft record, fetch a draft record's media, reach the author's
desk, create or edit anything, publish or unpublish, upload, or read the page-view log. **An
anonymous visitor cannot** do any of those either, and gets the identical answer for each. **A
`reader` is not a lesser author:** the two accounts differ by grant, not by degree, and every
refusal a stranger receives a reader receives byte for byte.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `reader` session to any `author`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

Where a denial would reveal that something exists, it is **indistinguishable from absence**:
asking for a draft case, a draft post or the author's desk returns exactly what asking for a
slug that has never existed returns, in status, in body and in wording. Where the reader can
already see the resource and merely lacks the grant for the action, the refusal is explicit
and names what is missing.

Signup is **open**: anybody may create an account and it is always a `reader`. No route, no
field and no payload creates an `author`; the two author accounts exist only because they
were seeded. The seeded accounts are `author@example.com` (Mara Volt, `author`),
`author2@example.com` (Iris Kwan, `author`) and `reader@example.com` (Tom Bright, `reader`).

## Core features

### Auth

Email and password, implemented by the app. `POST /api/auth/signup` takes an email, a
password and a display name and creates a `reader`, returning a bearer token as
`access_token`. `POST /api/auth/login` takes an email and a password and returns the same
shape. Every other API call carries the token. Passwords are hashed with a slow modern hash
and never stored or logged in the clear. Tokens expire; an expired or forged token is
rejected as unauthorized rather than ignored. HTML routes carry a session cookie set at
login, host-only and not readable by script. Repeated wrong passwords against one address,
and repeated attempts from one source address, each attract their own progressive backoff;
neither ever produces a permanent lockout, because a permanent lock is a way to deny somebody
their own account.

1. Signing in with a seeded email and `deku-demo-pw-2026` succeeds and returns a token. An
   unknown email and a wrong password are refused with the same message and the same shape,
   so neither reveals whether the address exists.
2. A signup succeeds and the created account holds the role `reader`. A signup that asks for
   the role `author`, in any field of the payload, still creates a `reader`; the request is
   not rejected for asking, it is simply not obeyed.
3. A request to any endpoint other than signup, login, health, the public read endpoints, the
   two form endpoints, the sitemap and the robots file without a valid token is denied and
   changes nothing.

### The public site and its chrome

Ten public routes, listed in `## User flow`. Localization is two locales and a persisted
choice rather than a translation pipeline: every one of those routes also answers under a
locale prefix, `/en/` and `/es/`, and the bare form resolves to the visitor's persisted
choice, falling back to English. Two routes, the privacy policy and the not-found page, are
unlinked from the primary navigation and reachable by address alone, and an in-page fragment
link scrolls to its anchor rather than reloading the document. A fixed header carries the wordmark, the five primary links, a
showreel link, the sound control and the menu control. The menu control opens a full-screen
overlay carrying the full navigation, the four social links and the newsletter link. A footer
carries the three offices, the contact line and address, the social set, the newsletter form,
the language switch, the privacy link, the terms link. `/privacy` carries the privacy and
cookie policy plus the studio's legal identity, and `/terms` carries the terms of use. A
cookie banner asks once about functional and
analytical cookies and the answer survives a reload.

4. The primary navigation is exactly these five links, in this order: `The Studio`,
   `Our Cases`, `Careers`, `Our Values`, `Contact`.
5. The three offices are `Detroit`, `Rotterdam` and `Lyon`, and the contact address is
   `hello@northform.co`. The footer line above it reads `We'd love to hear from you`.
6. Choosing `Español` sets the locale prefix and the choice persists: returning to the site
   with no prefix lands on Spanish. Choosing `English` returns it. A route that has no
   translation still renders, in English, rather than answering as missing.

### Case studies

A case study carries a slug, a title, a client, a year range, a discipline from `Web`,
`Strategy` and `Design`, a three-line headline, one accent, a hero image, ordered media bands
with captions, credits, a featured flag and a sort order. `/cases` lists them as a card grid,
newest first, filterable by discipline. `/cases/<slug>` is the long-form page, and on entry it
binds that project's accent, recolouring its links, rules, captions and caret marks.

7. `GET /api/cases` returns only published cases to an anonymous visitor and to a `reader`.
   An `author` may ask for drafts as well, and only an author's request is obeyed.
8. Filtering by discipline returns only cases of that discipline and never changes the
   ordering rule. Filtering to a discipline with no published case returns an empty top-level
   array, never an error.
9. The seven seeded published cases are `Lumenfest` (`2020 - Ongoing`, Web),
   `Tidewater Hall` (`2018 - Today`, Strategy), `Grand Museum of Science` (`2015 - Today`,
   Strategy), `This Was Mia's Phone` (`2016`, Design), `PRISM Festival 2018`
   (`2012 - Today`, Design), `The Whitfield Center` (`2017`, Design) and
   `Grand Opera of Verdal` (`2016 - Ongoing`, Design).

### Publication state and the protected boundary

Every case, post and role is in exactly one of two states, `draft` or `published`. This is the
rule the whole product turns on.

10. A published record and its media are readable by anybody, signed in or not.
11. A draft record is readable by an `author` alone. `GET /api/cases/harbour-line-rebrand`
    and the route `/cases/harbour-line-rebrand` both answer, to an anonymous visitor and to a
    signed-in `reader`, exactly as they would for a slug that has never existed: the same
    status, the same body, the same wording. Signed in as an `author`, both render in full.
12. Publishing stamps the publication time once and moves the state. Two simultaneous
    publishes of one case leave exactly one published row carrying one publication time; the
    other is refused and nothing is written twice. This must hold under real concurrent
    requests.
13. Unpublishing moves the state back to `draft` and its media becomes unreadable again on
    the next request, not at the next expiry. A link that was legitimate a moment ago stops
    working the moment the record leaves the published state.

### Media in the object store

Every image lives in the MinIO bucket and nowhere else. Not on the application's filesystem,
not in a database column, not inlined into a template.

14. The object key is fixed and derived from the owning record and the bytes:
    `cases/{case_slug}/{sha256_of_bytes}.{ext}` for a case asset and
    `posts/{post_slug}/{sha256_of_bytes}.{ext}` for a post asset, so uploading
    `hero.png` to `lumenfest` yields a key of the shape
    `cases/lumenfest/9f2a...d0.png`.
15. Because the key carries the digest, uploading the same bytes to the same case twice
    leaves exactly **one** object and **one** asset row. Two simultaneous uploads of those
    same bytes leave one object and one row as well; the second attempt is a no-op or a
    refusal, and either way nothing is stored a second time.
16. Protected reads use one of two mechanisms and only one, consistently across the whole
    product: an authenticated streaming endpoint that re-checks the owning record's state on
    every request, or presigned links that expire within five minutes and are never issued for
    a draft record. Whichever is chosen, a draft record's bytes are unreachable by object key,
    by listing the bucket, and by any link minted while the record was published.
17. Every asset carries alternative text, and it is stored with the asset rather than
    invented at render time.

### The journal and the careers list

18. `/news` lists published posts newest first, each with a date, a title and a summary, and
    `/news/<slug>` is the article. A draft post behaves exactly as a draft case does.
19. `/careers` lists open roles, each with a title, an office from `Detroit`, `Rotterdam` and
    `Lyon`, an employment type and a way to apply.

### The two conversions

20. `POST /api/enquiries` takes a name, an email, a company and a message, stores the
    enquiry, and the contact route replaces the form in place with a success banner without a
    reload. A submission missing a required field, or carrying a malformed address, is
    rejected as a client error, names the offending field inline, and stores nothing.
21. `POST /api/subscribers` takes an email address and stores the subscriber. Subscribing the
    same address twice leaves exactly one subscriber row, and the second attempt reports
    success rather than an error, because a visitor who subscribes twice has not made a
    mistake.
22. Both forms carry three pre-rendered states, idle, success and failure, toggled in place.
    The banner replaces the form where the form was; nothing appears in a corner of the screen
    and the page never reloads.

### The author's desk

23. `/desk` is one table with a row per case, post and role, carrying its title, its type, its
    state, its discipline or office, its accent and its publication date. It is reachable by
    an `author` alone; a `reader` and an anonymous visitor both receive the not-found page.
24. Creating a record spans a dedicated route rather than an overlay: `/desk/cases/new`,
    `/desk/posts/new` and `/desk/roles/new` are real addresses, each carrying its own form,
    and a browser back from one returns to the desk with the table as it was.
25. A slug is unique within its collection and is never reused after a delete. Creating a case
    with a slug already taken is rejected as a client error naming the conflict, and nothing is
    written.

### The set pieces

26. The site opens on a loading sequence: on a full-screen near-black ground, a mascot runs
    inside a ring whose progress stroke fills clockwise from twelve o'clock, bound to real load
    fraction rather than to a timer. When load completes the ring finishes, the ground clears,
    and the three-dimensional layer and the first letter title begin together. That handoff
    happens once per session and never replays on a later route.
27. A full-viewport real-time three-dimensional scene composites behind the page content with
    a transparent ground, holding the studio's mascot as a lit model, and its pose and framing
    track scroll progress on the home route in step with the headline above it.
28. Display headlines assemble letter by letter: each letter starts tilted away from the
    reader and pushed back in depth, then turns flat and settles into line, one after the next
    on a short stagger.
29. An ambient bed plays under the experience. Its invocation waits for the first
    interaction, because the browser's autoplay policy forbids sound before one, and a
    control in the header mutes it. The choice
    persists across routes, and the control pulses while sound is live.
30. A showreel opens as a full-screen takeover from the header and from the hero, carrying
    play and pause, a scrubbable progress bar, a current-time readout, mute, captions and a
    settings menu with Captions, Quality and Speed, and closes back to the page.

### The launch surface

31. An unknown address renders Northform's own **not-found** page, carrying the full chrome,
    the heading `Ooh shit!`, the line `You're lost...` and a `Back to homepage` link, and
    answers as not found rather than as success. The same page, byte for byte, is what a
    draft record returns.
32. `/terms` carries the studio's terms of use, covering what a visitor may do with the
    work shown, what an enquiry commits either side to, what the newsletter list is used
    for, which office holds the contract, which law governs the terms. The footer links to
    it alongside the privacy policy. The site also serves a favicon at `/favicon.ico` or at
    `/favicon.svg`, declared in the document head of every route.
33. Every public route carries its own title and its own meta **description**, and no two
    public routes share either.
34. `/sitemap.xml` lists every published public route and `/robots.txt` names the **sitemap**
    address. A draft case's route never appears in the sitemap; publishing it adds it.
35. Every page leads with exactly one **primary action**, visually distinct from every
    secondary one on that page.
36. Each page view is recorded with its route, its locale and the time it happened, and an
    `author` can read that log. A `reader` and an anonymous visitor calling the same endpoint
    are denied.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the loader, the hero, the featured reel, the studio pitch | public |
| `/studio` | the manifesto, the disciplines, the three offices | public |
| `/cases` | the portfolio as a card grid, filterable by discipline | public |
| `/cases/<slug>` | one case study, long-form, accent-bound | public if published |
| `/values` | what the studio believes | public |
| `/careers` | open roles | public |
| `/news` | the journal index | public |
| `/news/<slug>` | one journal post | public if published |
| `/contact` | the enquiry form and the addresses | public |
| `/privacy` | privacy and cookie policy | public |
| `/terms` | the studio's terms of use | public |
| `/login` | sign in | public |
| `/signup` | create a reader account | public |
| `/desk` | the author's table of every record | `author` |
| `/desk/cases/new` | create a case | `author` |
| `/desk/posts/new` | create a journal post | `author` |
| `/desk/roles/new` | create an open role | `author` |
| `/sitemap.xml` | every published public route | public |
| `/robots.txt` | names the sitemap | public |

**Entry and redirects.** An unauthenticated request for `/desk` lands on `/login` with the
intended address remembered and returns there after signing in. A signed-in `reader`
requesting `/desk` receives the not-found page, identical to the page for an address that
never existed. Signing out clears the session and returns to `/`. A token that expires
mid-action is rejected as unauthorized and the half-filled form is preserved so nothing is
retyped. The locale switch sets the prefix and persists the choice.

**Journeys.**

1. *The first ten seconds.* Open `/`. The loader holds on a near-black ground with the mascot
   running inside a filling ring. When it completes, the ring finishes, the ground clears, the
   three-dimensional layer composites behind the page and the hero headline assembles letter
   by letter. The sound control offers to unmute the ambient bed.
2. *Browse the work.* Scroll the reel past the seven featured projects, open `/cases`, filter
   to `Design`, and open `Grand Opera of Verdal`. The page takes that project's accent and its
   hero and bands are served from the bucket.
3. *The protected boundary.* Without signing in, request `/cases/harbour-line-rebrand` and
   read the not-found page. Sign in as `reader@example.com` and get the same page. Sign in as
   `author@example.com` and the case renders in full.
4. *Publish.* As `author@example.com`, open `/desk`, read the table with one row per record
   and its state, open `Harbour Line Rebrand`, and publish it. Its card appears in `/cases`
   and its hero becomes readable by anybody.
5. *Create through the dedicated route.* From `/desk`, open `/desk/cases/new`, give a slug, a
   title, a discipline and an accent, save, then upload a hero image and read the object key
   back.
6. *The two conversions.* Open `/contact`, submit the enquiry form, and watch the success
   banner replace the form in place. Submit the footer newsletter form with a malformed
   address and read the failure banner name the field.
7. *Careers and the journal.* Open `/careers` and read the three open roles with their
   offices, then `/news` and open a published post.

**States.** Every list carries an empty state naming the filter that produced it and offering
one action. Every route has a loading state in which the chrome stays and only the content
region is replaced. An error replaces the failed region, keeps the chrome, offers a retry and
carries the request identifier; an error in one region never takes the rest of the site down.
Forbidden is indistinguishable from not found.

## UI/UX notes

Somebody arriving should understand, before they have read a word, that the people who made
this can build anything they are asked for, and should want to stay and watch. The register is
consumer and editorial with a point of view: the work is the first thing seen and the loudest
thing on every screen. This is the one register where atmosphere is the product, because the
site is the portfolio's best entry, so restraint here is a failure rather than taste.
Spectacle over economy. Continuity over sections. One unbroken descent over a stack of
independent blocks. A competing product could rationally invert all three and be right for its
context; this one does not.

Because the site must convey capability, it needs one thing dominant per view, space around
the subject, and craft visible in the smallest transition. Because it must convey rarity, the
work is given room and the surroundings stay quiet and dark. And because it must reassure at
the two moments that matter, the enquiry and the subscription go still: plain wording, nothing
moving, no surprise.

**Mode and surface.** Commit to dark and design it fully; no second theme is graded. The
ground is a near-black neutral with three sibling variants within a hair of it, one a touch
cooler and one a touch warmer, so a long scroll reads as a series of rooms rather than one
flat wall. Light panels exist and are an off-white neutral rather than pure paper, used where
a section wants to invert.

**Palette by role.** Two palettes, and the second is why the site feels alive. The system
palette is fixed: a near-black neutral ground; pure white carrying almost all the reading; an
off-white neutral for inverted panels; a mid cool neutral for labels and metadata; a light,
muted indigo for the lavender-grey secondary lines, used at reduced strength rather than as a
second solid; a near-white muted indigo at low strength as the only colour a divider is ever
drawn in; a deep, vivid blue for links and for the focus ring and nothing else; and a light,
vivid red for the studio's own mark and the loader ring. The per-project accent palette is the
other half: each case binds exactly one accent for the length of its page, drawn from nine
families, coral and red, gold and amber reading as a vivid orange, pink and magenta, violet
and indigo, blue and cyan, teal and green, and earth and clay reading as a muted orange. One
accent is active at a time, which is what makes the site warm and cool as you move through the
work. Three colours carry meaning in the chrome and appear nowhere else: the blue that means a
link or a focus, the red that means the studio's own mark, and the active accent that means
"this project". A state that is none of the three borrows none of them. The exact members are
yours so long as each stays recognisably inside its family and holds the contrast floor
against the ground.

**Typography.** Three families, named exactly, because a family is an identity nobody can derive.
**GT Sectra Display** carries editorial headings, a high-contrast serif, at weights 400, 500
and 700; it is licensed, so until it is the stack is `"GT Sectra Display", "Playfair Display",
Georgia, "Times New Roman", serif`. **Gilroy** carries the loudest display words, a soft
geometric sans, at weights 400, 500 and 700; also licensed, with the stack `"Gilroy",
"Poppins", "Century Gothic", system-ui, sans-serif`. **Heebo** does every interface, body and
caption at weights 200, 300, 400, 500 and 700, is freely available, and carries the stack
`"Heebo", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. The rendered scale, in
the fixed pixel sizes the studio set: primary display headline `120px` at 700 over `107px`;
secondary display headline `80px` at 700 over `71.3333px`; oversized light numeral `80px` at
200 over `60px`; large light heading `70px` at 200 over `60px`; serif section heading `50px`
at 400 over `50px`; serif sub-heading `45px` at 400 over `45px`; card heading `40px` at 700
over `40px`; lead line `22px` at 300 over `18px`; intro paragraph `20px` at 300 over `27px`;
emphasised body `16px` at 500 over `27.2px`; body `14px` at 400 over `29.4px`; interface label
`14px` at 500 over `23.8px`; small label `13px` at 500 over `13px`; eyebrow `11px` at 400 and
at 700 over `11px`, uppercase; smallest caps `9px` at 700 over `9px`. Body at `14px` over a
`29.4px` line is the signature long-measure look and is what gives the site its gallery calm;
a tighter body leading changes the whole temperament and is the one substitution that must not
be made.

**Shape, spacing and rules.** Corners are barely softened: a small radius on buttons, inputs
and small controls, a full circle on circular controls and the mascot ring, a slightly larger
softening on the player surface and the cookie banner, and a fully rounded pill on the scrub
bar. Nothing is sharp and nothing is heavily rounded. Dividers are the hairline colour at low
strength, never a solid line. Desktop is a twelve-column grid inside a generous container
inset; below the tablet boundary it collapses to one column. Space over dividers: sections
separate by air, and a rule appears only where air alone would read as a mistake.

**Motion.** Motion is the product rather than a finish, and the character is eased: quick to
leave, long to settle, so every response feels unhurried and expensive rather than snappy. An
easing catalogue of ten curves is in use, and they are not interchangeable. One house curve carries everything a
visitor can trigger, hover, colour, transform and fill. A gentler companion carries paired
opacity and slow transforms. A third, very fast out with a very long tail, carries large
element reveals and media parallax. A fourth, smooth out, carries the entrance cascade. A
fifth, slow in and sharp to finish, carries exits. Four more exist for rare generic,
accelerating, symmetric and emphatic moves. A tenth, fast out to a hard settle, belongs to the
letter titles alone. Three durations recur across the whole product: a fast one for opacity
and small state changes, a base one for colour, transform and fill, and a slow one for large
reveals and the letter titles. The exact curves and the exact speeds are yours; what is fixed
is that one house curve exists, that the reveal curve and the letter-title curve are distinct
from it, and that everything resolves on one of the three speeds. Transitions are declared per
property; a catch-all transition on every property makes a revealed element animate its own
layout.

The named moments, each of which must be recognisable by sight. **The appear-fade-up cascade**
is the workhorse entrance: an element starts a short way below its rest position at zero
opacity and settles up into place, and siblings follow one after another on a short stagger,
like cards being dealt; footer blocks and menu items travel a little further than body
elements. **The large reveal** pairs a slow transform with a quicker fade, so media slides
into place while the opacity has already arrived. **The letter titles** are the showpiece: a
display headline is split into its individual letters, each resting on its own plane inside a
perspective parent, and each starts tilted about thirty-five degrees away from the reader and
pushed back in depth before turning flat and clicking into line, one after the next; it reads
as type being set rather than as text fading in. **The reveal wipes** drive masked line
reveals and loader bars: a band travels in from one edge, or out to the other, or sweeps
through from one side to the far side. **The menu-bar morph**: the three bars of the menu
control are not a static icon, and on pointing and on opening the top bar lifts, the middle
bar narrows and the bottom bar drops before the overlay arrives. **The pulsing ripple** on the
sound control grows a ring from nothing to full while fading to transparent, over and over,
and never stops while sound is live. **The running gait** of the loader mascot is a real
cycle, legs reaching, about once per blink, for the whole load. **The duplicate-glyph hover**
gives navigation links an underline or caret built from a shadow copy of the glyph rather than
a drawn rule, and is the single most-used hover in the product. **The showreel open and close**
arrives scaling down a little into place and leaves scaling down further away, with opacity.

Every always-on animation is pausable and the platform's reduced-motion preference is
honoured by default. Under it the cascade becomes an instant set, the letter titles set flat with no
swing, parallax pins, the scrubbed elements hold their finished state, and the
three-dimensional layer falls back to a static framing. Nothing becomes unusable and nothing
becomes invisible: a reveal built as "start invisible, then animate in" leaves a blank page
the moment it is suppressed, which is why every moment above has a defined resting state that
is the finished one.

**Scroll.** The page is smooth-scrolled: input drives a virtual position that eased-follows
the target with a little weight and momentum, and that position, not the native bar, feeds
every reveal and every parallax. Because the reveals are bound to position rather than to a
timer they are reversible, so scrolling back un-plays them and tucks each element away again.
Two things scrub continuously rather than toggling, the header and the caret marks, and the
home background image both fades in and parallaxes as it arrives.

**The three-dimensional layer.** A full-viewport real-time scene sits behind the page at the
back of the stack, transparent cleared, compositing under every other layer and holding the
mascot as a lit model. Its material and its lighting are read from a small spherical reference
image rather than computed from a lamp rig, which is what gives it a polished, studio-lit look
with no lamps at all, and a gentle surface-detail map sits over it; the whole composites
through at least one post-processing pass with a subtle lift on the highlights. As the home
route scrolls, the mascot's pose, rotation and framing track scroll progress in step with the
letter titles above it, so the words and the sculpture read as one performance. That binding
is to scroll position rather than to a clock, so it reverses when the visitor scrolls back. It
keeps no timer of its own beyond the render clock, and it lowers its pixel ratio and drops its
post-processing pass under load rather than grinding. A tuning panel may exist behind a debug flag and
must never ship enabled.

**The loader.** On a full-screen near-black ground, a circular mark holds two concentric
rings: a thin ground ring in the lavender-grey at low strength, and a progress stroke in the
signal red drawn over it, filling clockwise from twelve o'clock as real load progresses.
Inside the ring the mascot runs as a signal-red silhouette with a soft radial shadow beneath
it. It is part of the show rather than a wait.

**The chrome.** The header is fixed on every route, transparent over the hero and gaining the
ground colour on scroll, and it translates with scroll progress rather than snapping. The menu
overlay takes the full screen and carries the full navigation, the four social links, the
newsletter link and a small credit mark low in the panel, its items entering on the cascade
with a longer travel. The footer carries the three offices as headings, the warm contact line,
the social set, the newsletter form, the language switch, the privacy link, the terms link, its blocks
entering staggered. The cookie banner rises from the bottom as a softly rounded panel and,
once answered, stays gone. Layering is a set of decisions: content at the bottom, the header
above it, the cookie banner and menu overlay well above that, full-screen takeovers above
everything, and the three-dimensional layer behind all of it.

**Iconography.** Every mark is inline vector geometry: the wordmark, the mascot ring, the
credit mark, the menu bars, the sound mark, the caret, the four social marks and the player
control set. No icon file, no icon font, no sprite sheet. Icons inherit the current text colour
and carry a small soft drop shadow when they sit over media so they stay readable on any
frame. The wordmark keeps its box ratio whatever glyphs replace it, and the mascot ring keeps
its concentric two-circle construction because the progress stroke depends on it.

**Components and states.** Every control has resting, pointed-at, pressed, focused and
unavailable states, and unavailable is never signalled by colour alone. `Escape` closes one
level of an overlay and then the overlay itself. Inputs carry the small radius and settle on
the house curve when focused. A hover-built effect always has a tap or an arrives-on-scroll
equivalent, because a touch device cannot hover and a stuck hover state is the most common
defect of this kind.

**Responsive.** Three breakpoint bands anchor the matrix: desktop, tablet, and mobile below
the tablet boundary, with three finer phone ceilings below that for component-local
corrections. Desktop
is the multi-column grid; below the tablet boundary everything collapses to one column, the
header's primary links move into the menu overlay, and the footer's three offices stack. The
home route grows taller on a phone than on a desktop, which simply gives the cascade more
travel. At the narrowest viewport nothing overflows sideways and every navigation target stays
reachable.

**Accessibility floors, which are contract rather than taste.** Text meets a contrast ratio of
at least `4.5:1`; large text and any border or state that carries information meets at least
`3:1`, and a per-project accent used for text is checked against its ground before it ships.
Every control is reachable and operable from the keyboard with a visible focus state in the
brand blue that is never removed. Every icon-only control carries a visually hidden label
naming it, including `Toggle menu`, `Toggle sound` and `Close showreel`. The showreel player
is keyboard-operable and carries captions. Meaning is never carried by colour alone. Every
interactive target is at least `44px` on touch. One first-level heading per route, no skipped
levels, a unique page title per route, and a skip link as the first thing on every page. Every
content image carries alternative text and a decorative image declares itself decorative.

**What it must not look like.** No page dominated by a single hue family with no second
signal. No decoration standing in for work. No stock-template composition where the studio's
own argument belongs. No page where the subject is smaller than the furniture around it.

## Technical requirements

The frontend is **Alpine.js over server templates**: no client-side router, no component
compiler, no framework beyond the small declarative layer Alpine adds to markup the server
already produced. Alpine drives the menu overlay, the locale switch, the discipline filter,
the form state toggle and the sound control; the loader, the reveal engine, the letter
splitter, the smooth-scroll engine and the three-dimensional layer are plain modules sharing
one animation-frame loop. The backend is **NestJS with Handlebars views** on Node 20, serving
the HTML routes and the JSON API on one origin. The rendering model is multi-page and
progressively enhanced: every route is a real address the server answers with a complete
document, so the browser receives rendered markup on first paint rather than an empty shell
that fetches its own content, and with script disabled every route still renders and both
forms still submit. Storage is **PostgreSQL**, read from `DATABASE_URL`, and **MinIO**, read
from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. The
public address and port are read from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a
host or a port. Both backing services are **already running** at those variables and must not
be downloaded, installed, compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything
else is a contract violation.

`GET /api/health` returns `200` once the app can reach PostgreSQL and the bucket. One
structured log line per request carries a request identifier, the route, the locale, the
principal and the outcome, and the same identifier appears on every error a person is shown.
No password, password hash, bearer token or storage credential ever reaches a log line or
anything the browser downloads: nothing the browser can fetch contains a credential or a key.

`/sitemap.xml` lists every published public route and `/robots.txt` names the **sitemap**
address. Every response carries the standard security headers, including a strict transport
policy and a nosniff content-type policy. Static assets are served with a versioned filename
and a long cache lifetime, so a deploy never serves a stale mixture.

Input is validated at the boundary and an invalid value is rejected as a client error naming
the offending field. Rate limiting is the app's whole answer to abuse: the signup, login,
enquiry and subscriber endpoints are limited per source address and per target, so a caller
that submits repeatedly from one address is slowed rather than served, a limited caller is
told plainly rather than silently dropped, and no limit is ever a permanent block. The two
public forms carry the same protection as the credential endpoints, because an enquiry form
open to the internet is the surface that gets abused first.
Every state-changing request carries a token a plain cross-site navigation cannot supply, so
no state-changing operation is reachable by navigation alone.

**Privileges.** Nothing carries a system-level privilege invisible from the interface: no
service account, no support login and no back door. Every capability an operator needs is an
ordinary grant held by an ordinary principal.

**Delivery and degradation.** A performance budget governs delivery, and the techniques that
hold it are these. The three-dimensional layer lowers its pixel ratio and drops its
post-processing pass under load, and falls back to a static framing on weak hardware. Media decodes off
the critical path. The loader covers first load so the heavy engines initialise behind it
rather than blocking first paint. If the object store is unreachable, the pages still render
and the image slots report their own failure rather than taking the route down.

Four error shapes exist and no others: an inline field error saying what is wrong and what to
do; a region error that leaves the surrounding chrome and offers a retry; a route error that
leaves the chrome and carries the message and a retry in the content region; and a full-page
failure carrying the request identifier and a reload. None of them shows a stack trace, an
internal service name or a raw error string.

## Data model

Twelve tables, and all timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data,
not a secret. Hash it as normal; the exact literal must work at login, and it must be written
into `/app/USER_README.md` alongside each account so a grader can sign in.

- **`account`**: `id`, `email` unique, `display_name`, `password_hash`, `role` in `author` and
  `reader`, `created_at`.
- **`case_study`**: `id`, `slug` unique, `title`, `client`, `year_range`, `discipline`,
  `headline`, `accent`, `state`, `featured`, `sort_order`, `author_id`, `published_at`
  nullable, `created_at`, `updated_at`. `state` is `draft` or `published` and nothing else.
- **`case_band`**: `id`, `case_id`, `position`, `caption`, `asset_id`. Ordered by `position`.
- **`post`**: `id`, `slug` unique, `title`, `summary`, `body`, `state`, `author_id`,
  `published_at` nullable, `created_at`.
- **`role_opening`**: `id`, `slug` unique, `title`, `office`, `employment_type`, `apply_url`,
  `state`, `posted_at`.
- **`asset`**: `id`, `owner_type`, `owner_id`, `object_key` unique, `content_type`,
  `byte_size`, `digest`, `alt_text`, `uploaded_by`, `created_at`. `object_key` carries the
  digest, which is what makes the uniqueness rule the deduplication rule.
- **`enquiry`**: `id`, `name`, `email`, `company`, `message`, `received_at`.
- **`subscriber`**: `id`, `email` unique, `locale`, `subscribed_at`.
- **`office`**: `id`, `city`, `line`, `position`.
- **`locale`**: `id`, `code`, `label`, `prefix`.
- **`social_link`**: `id`, `network`, `url`, `position`.
- **`page_view`**: `id`, `route`, `locale`, `account_id` nullable, `occurred_at`.

**Invariants, stated as properties of the running system.**

- **Object-key uniqueness.** `object_key` is unique across the whole asset table. Because the
  key is derived from the owning record and the digest of the bytes, the same bytes uploaded
  to one case twice leave exactly one object and one row, and two simultaneous uploads of
  those bytes leave one object and one row as well.
- **Draft invisibility.** A record in `draft` is readable by an account holding the `author`
  role and by nobody else, and the refusal is byte-identical to the answer for a slug that
  never existed. Its assets are unreadable by object key, by bucket listing, and by any link
  minted while the record was published.
- **Publish once.** Publishing stamps `published_at` once and moves `state`. Two simultaneous
  publishes of one record leave exactly one published row carrying one publication time.
- **Unpublish is immediate.** Moving back to `draft` makes the record and its media
  unreadable on the next request rather than at the next expiry.
- **Slug uniqueness.** A slug is unique within its collection and is never reused after a
  delete.
- **Closed enums.** `discipline` is `Web`, `Strategy` or `Design`. `office` is `Detroit`,
  `Rotterdam` or `Lyon`. `state` is `draft` or `published`. `role` is `author` or `reader`.
- **Bytes live in one place.** An image is in the bucket and nowhere else: not on the
  application's filesystem, not in a database column, not inlined into a template.
- **Idempotent seeding.** Restarting the app must not duplicate rows or re-upload objects.

**Seed data.** Studio `Northform`, contact address `hello@northform.co`, offices `Detroit`,
`Rotterdam` and `Lyon`, locales `en` labelled `English` and `es` labelled `Español`, social
set `Facebook`, `Instagram`, `Dribbble` and `Twitter`. Accounts as listed in `## User roles`.
Eight case studies:

| Slug | Title | Year range | Discipline | Accent | State |
|---|---|---|---|---|---|
| `lumenfest` | Lumenfest | `2020 - Ongoing` | `Web` | coral | `published` |
| `tidewater-hall` | Tidewater Hall | `2018 - Today` | `Strategy` | teal | `published` |
| `grand-museum-of-science` | Grand Museum of Science | `2015 - Today` | `Strategy` | gold | `published` |
| `this-was-mias-phone` | This Was Mia's Phone | `2016` | `Design` | pink | `published` |
| `prism-festival-2018` | PRISM Festival 2018 | `2012 - Today` | `Design` | indigo | `published` |
| `the-whitfield-center` | The Whitfield Center | `2017` | `Design` | clay | `published` |
| `grand-opera-of-verdal` | Grand Opera of Verdal | `2016 - Ongoing` | `Design` | violet | `published` |
| `harbour-line-rebrand` | Harbour Line Rebrand | `2026` | `Web` | blue | `draft` |

Each published case carries a hero asset and two ordered bands, all real objects in the
bucket. `harbour-line-rebrand` carries a hero asset too: a real object in the same bucket that
no reader and no stranger may fetch. Journal posts `studio-turns-ten` and
`on-motion-as-argument` are published and `the-quiet-rebrand` is a draft. Open roles
`senior-creative-developer` in `Detroit`, `motion-designer` in `Rotterdam` and `producer` in
`Lyon` are published. The enquiry and subscriber tables seed empty, because both are what a
visitor creates.

## Front-end specification

This section carries the visual detail that `## UI/UX notes` states in summary, giving each
route its structure in the order a visitor meets it. Nothing here contradicts it; where a
reading differs, `## UI/UX notes` wins.

**The home route as one descent.** It is a single continuous scene, not a stack of blocks: the
loader, then the hero over the three-dimensional layer carrying the display headline, a
three-line studio statement and a social row, then the featured-projects band, then the studio
pitch, then the footer. Nothing between them reads as a boundary; the ground shifts by a hair
between rooms rather than by a rule.

**The hero.** The display headline is the letter-title mechanism at its largest. Beneath it a
three-line statement in the interface family sets the studio's position, and beside it a link
into the showreel. A social row of four networks plus the newsletter sits within the hero
rather than below it.

**The featured band.** Seven projects, each carrying a year range, a title, a discipline tag
and a three-line headline, with its media parallaxing on the large-reveal curve and a caret
link reading `Discover` into its case. The tag is one of `Web`, `Strategy` or `Design`.

**The cases index.** A card grid, newest first, with a discipline filter above it. A card
carries media, title, year range and discipline tag. It reveals on the large-reveal curve as
it enters view, and when pointed at its media scales gently while that project's accent tints
the card, on the house curve. An empty filter result shows a titled explanation naming the
discipline and one action to clear it.

**The case study.** Full-bleed hero with the title, client, year and discipline; a
challenge-and-approach narrative in the serif register; a sequence of full-width media bands
that parallax as they arrive, each with its caption; pull quotes and credits; and previous and
next links to sibling cases. Every accent-bound element on the page moves together when the
accent binds, so the page never shows two temperatures at once.

**The privacy and terms routes.** Both are long-form reading set in the interface family on
the near-black ground at the body measure, with numbered clauses, a last-updated line, one
primary action back to the home route. Neither carries the three-dimensional layer.

**The values route.** Value statements, each a large serif line over a short paragraph,
revealed one at a time on scroll and numbered with the oversized light numerals.

**The careers list.** A row per role carrying the title, the office and a way to apply, rising
into view on the cascade and lifting on hover.

**The desk.** A table, one row per record, with columns for the title, the type, the state,
the discipline or office, the accent and the publication date. The state column reads as a
word rather than a colour alone. The create control is the one primary action on the page.

**Empty, loading, error and forbidden.** An empty list carries a title, one sentence of
explanation and exactly one primary action. A loading region keeps the chrome and occupies the
space the content will, so nothing jumps when it arrives. An error replaces only the failed
region and offers a retry. The not-found page carries the chrome, the heading, the lost line
and one way home, and it is what a draft record renders too, indistinguishably.

**Text and images.** A long title truncates to one line and reveals the full text only when it
is genuinely truncated. Every content image carries alternative text describing what it shows;
a purely decorative image declares itself decorative and is skipped by assistive technology.

**The zero-asset rule.** No binary ships: no image, no video, no font file, no
three-dimensional model, no audio file and no sprite sheet. The mascot is composed from
primitives, keeping its object names so the scene code is unchanged; its shine is a generated
spherical reference image tinted toward the active accent, and its surface detail a generated
low-amplitude noise field. The ambient bed is generated live from a few detuned tones under a
slowly modulated low-pass filter, so it never repeats exactly, and any interface cue is a short
enveloped blip. The loader gait is a generated strip of silhouette poses laid out horizontally
so the strip cycles, with a generated radial shadow beneath. Every photographic slot is a
seeded gradient in the owning project's accent with a little generated grain, seeded by slug so
it is stable between builds; the showreel poster is the same on the ground colour with a
centred play mark. The grain is generated fine noise desaturated to kill the colour speckle and
laid over grounds at low strength. The locale marks are simple vector bands or are dropped in
favour of the text labels already in the switch.

## Constraints

**One studio, one site.** A single tenant, a single workspace, two locales and nothing else.

**Not built, and nothing here is to be inferred from the vocabulary above.** No analytics, no
measurement vendor and no third-party tag of any kind. No video hosting or upload: the showreel
plays from a source the environment already provides. No font licensing, no font file, and no
binary asset of any class. No comments, likes, ratings, follows or any social graph. No
payments, subscriptions, invoices, seats or commerce surface. No client portal, no project
management and no file sharing with clients. No email delivery: the two forms persist what
they receive and no message leaves the application. No content approval workflow beyond the
two publication states, no scheduled publication and no revision history. No search. No
tagging beyond the fixed discipline enum. No third language. No mobile application. No
server-side rendering of the three-dimensional layer. No outbound network call at runtime to
anything other than PostgreSQL and MinIO.

**Scale.** The site stays responsive at the volume it is built for: tens of case studies, a few
hundred assets in the bucket, and a card grid that renders incrementally rather than all at
once when it runs past a screenful. It holds a smooth frame rate with the three-dimensional
layer running on a three-year-old laptop, and the layer simplifies itself rather than grinding
when it cannot.

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
- The server must keep running after this session ends and must not be a child of the shell.
  An ordinary background job dies with its shell, and the app will not be running when it is
  next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ "email", "password", "display_name" }` | `{ "access_token", "account": { "id", "email", "display_name", "role" } }` |
| `POST /api/auth/login` | `{ "email", "password" }` | the same shape |
| `GET /api/me` | bearer token | the signed-in account with its role |
| `GET /api/health` | none | a readiness body |
| `GET /api/cases` | `discipline`, `state`, `featured` | a top-level JSON array of readable cases |
| `POST /api/cases` | `{ "slug", "title", "client", "year_range", "discipline", "headline", "accent" }` | the created case |
| `GET /api/cases/<slug>` | bearer token optional | the case with its ordered bands and credits |
| `PATCH /api/cases/<slug>` | any editable field | the updated case |
| `POST /api/cases/<slug>/publish` | `{ "state" }` | the updated case |
| `POST /api/cases/<slug>/assets` | the bytes, a content type and `alt_text` | `{ "object_key", "digest", "byte_size", "alt_text" }` |
| `GET /api/assets/<object_key>` | bearer token optional | the object bytes, subject to the owning record's state |
| `GET /api/posts` | `state` | a top-level JSON array of readable posts |
| `GET /api/posts/<slug>` | bearer token optional | one post |
| `POST /api/posts` | `{ "slug", "title", "summary", "body" }` | the created post |
| `GET /api/roles` | none | a top-level JSON array of open roles |
| `POST /api/enquiries` | `{ "name", "email", "company", "message" }` | the stored enquiry |
| `POST /api/subscribers` | `{ "email", "locale" }` | the stored subscriber |
| `GET /api/config` | none | the locales, offices and social links |
| `GET /api/page-views` | `author` bearer token | a top-level JSON array of recorded page views |

Bearer authentication is required on everything except `POST /api/auth/signup`,
`POST /api/auth/login`, `GET /api/health`, the public read endpoints, `POST /api/enquiries`,
`POST /api/subscribers`, `GET /api/config`, `/sitemap.xml` and `/robots.txt`. A successful call
returns the named resource or the named shape. An invalid, unauthorized or forbidden call is
rejected as a client error, never as a server error and never as a silent success, and a
resource whose existence must not be revealed is rejected exactly as an absent one.

**No mocks.** The following are contract violations however good the interface looks: an
in-memory list of cases that disappears on restart; a file on the app's own disk standing in
for the object store; image bytes inlined into a template or stored in a database column; a
hardcoded success response the app returns to itself instead of writing to the bucket; an
image slot the interface draws from a data address it generated rather than from a stored
object. PostgreSQL and MinIO are the fact, and the app's own screens and tables can only
reflect what lives in them, never substitute for them.

## Definition of done

This is the acceptance checklist, and every line of it is observable from outside the app.

A visitor watches the loader hand off, browses the reel, opens a published case study whose
media is served from the object store, and sends an enquiry that is stored. A draft case study
is unreadable to that visitor and to a signed-in reader, and so are its bytes, whichever way
they are asked for; an author publishes it and both become readable. The same image uploaded
twice to one case leaves one object, not two. The app is deployed, healthy and still running
on its public address.
