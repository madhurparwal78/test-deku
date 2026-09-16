# Talent Roster Reel

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, move down a numbered index of twelve delivered films, open one into its
reel, follow a credit to the director who shot it, and mail the house from the
footer, without hitting an error page. A different stranger, signed in as a
visitor or signed in as nobody at all, must NOT be able to reach a talent the
house has signed but not published, by any means: not from the roster, not by
typing their address, and not by fetching their portrait. The media the producer
uploads must live as real objects in the `minio` bucket at their scheme's key; a
copy on the app container's own disk does not count.

## Overview

`VERITE` does three things, in this order of prominence.

It shows the work: a numbered index of delivered films and shoots, `001` through
`012`, each one a still that plays as a reel, each one opening into its own page.

It shows the roster: the directors and photographers the house represents,
presented one at a time as a full-window name in serif display type, filtered by
discipline.

It opens a conversation: one mail address, `prod@verite.example.com`, in the footer
of every route, labelled `WORK WITH US`.

Behind it sits the studio. A producer adds a work or a talent, attaches media,
orders the index and decides whether the public can see it. That decision is the
product's one consequential act: a talent the house has signed but not announced
must be absent from the public site entirely, not hidden behind a flag the
browser is trusted to honour.

There is no cart, no payment, no search field, no comment and no rating. The
only person who authenticates in order to do anything is the producer.

The site ships with no binary assets at all. Every still, every reel, every
mark, the grain and the social card are generated from the item's own
identifier, so the same item always produces the same field and the page is
stable across reloads.

## User roles

Two roles, and an anonymous reader who is neither.

**Anonymous reader.** Sees the entry cluster, the work index, a work, the
roster, a talent, the about route and the not-found route. Reads every published
work and every published talent. Needs no account and is never asked for one.
Cannot reach `/studio`, cannot reach `/preview`, and cannot read or write
anything that is not published.

**`visitor`.** What signup creates. Signing up and signing in grants nothing the
anonymous reader does not already have: no studio route, no write, no
unpublished item, no media belonging to one. A `visitor` who requests a studio
route or attempts a write is refused with a client error.

**`producer`.** The house. Signs in at `/login`. Creates works and talents,
attaches media and credits, sets the order of the works index, previews an
unpublished item at `/preview`, publishes it, and unpublishes it again. Reads
the page-view log. Producer accounts are seeded and are not created through
signup.

Seeded accounts, each with the password `deku-demo-pw-2026`:

| Email | Role |
|---|---|
| `producer@example.com` | `producer` |
| `producer2@example.com` | `producer` |
| `visitor@example.com` | `visitor` |

## Core features

**1. The publish boundary.** Every work and every talent is either published or
it is not. An item that is not published is **absent** from every public
response: absent from the work index, absent from the entry cluster, absent from
the roster, absent from the discipline set, and absent from a work's next and
previous. A direct request for its address returns a not-found status and a page
that reveals nothing about whether such an item exists. Its poster, its stills
and its reel are refused to everyone who is not a `producer`. Publishing makes
the listing, the address and the media readable in one act; unpublishing makes
all three unreachable again, immediately. The seeded unpublished talent
`Odile Marchand` at `/talents/odile-marchand` and the seeded unpublished work
`The Quiet Room` at `/works/the-quiet-room` are the cases to hold to.

**2. Ordinals close up.** The work index displays `001` through `012`, zero
padded to three digits, contiguous, in the producer's order. The displayed
number is computed over the published works at the moment of reading, not stored
as a label, so unpublishing the work showing `007` renumbers the rest and a
visitor never sees a gap or a duplicate. Reordering in the studio changes the
displayed numbers on the next read.

**3. The discipline filter is derived.** The roster's filter list is the
distinct disciplines of published talent, in the order the first talent carrying
each appears. It is never an authored list. Publishing a talent whose discipline
is new adds a filter; unpublishing the last talent of a discipline removes it.
There is no all state: one discipline is always active and the first is active
on arrival. Selecting a discipline narrows the set and does not navigate.

**4. Media lives in the object store.** Every poster, still and reel the producer
uploads is stored in `minio`, the S3-compatible object store, at the key
`items/{item_id}/{sha256_of_bytes}.{ext}`. The database row records where the
bytes are; the bucket is where they are. Every media row carries its intrinsic
dimensions, so a tile reserves its space before the image arrives, and a text
alternative written by the producer. An item whose media lacks a text
alternative cannot be published, and the refusal says which media is missing one.

**5. Slugs are stable.** A slug is assigned once and never changes when the
title changes. Slugs are unique within kind, so a work and a talent can share
one without colliding. If a slug is changed, the old address keeps resolving
permanently.

**6. The entry cluster.** `/` is a near-black window. A counter at the optical
centre reports real load progress and reaches `100%`; it must never reach
completion before the route is ready. The window then fills with a loose cluster
of published stills, overlapping at a range of sizes, dense toward the centre
and thinning toward the edges, leaving the four corners empty and the exact
centre clear for the centre mark. Positions are authored and stable across
loads, not scattered at random. Every still in the cluster is a real link to its
work, reachable by keyboard, carrying the work's title and its ordinal as its
accessible name, and showing a visible caption on focus in the same place the
pointer label would occupy. The route does not scroll at any width and no reel
plays on it.

**7. The work index.** `/works` opens on one sentence in the display face at the
foot of an otherwise empty first screen:
`Quiet decisions, made early, are the ones you notice last.` It arrives out of
focus and sharpens. Then twelve entries come down a long pale page in an
authored left, right and centre rhythm carried per work as data, never derived
from the index. Under each entry sits one row: a small filled square, the
ordinal at the still's left edge, and the title in the display face flush with
the still's right edge, so the gap between number and title changes with the
entry's width. Every still rests fully desaturated and returns to full colour
under the pointer. There are no filters, no sort, no categories, no years, no
pagination, no load-more and no search on this route.

**8. A work.** `/works/<slug>` carries the title, the ordinal, the credits as
role and name pairs, the reel playing full width, a vertical sequence of stills,
and the next work by ordinal, wrapping `012` back to `001`. Where a credit names
a published talent it links to that talent. That link is the reason this is a
directory of people and not only a portfolio.

**9. The roster.** `/talents` is the route the house is named for. At a wide
window one talent fills it and the route does not scroll: the name in large
serif display type across the upper third, the discipline as a small capital
label beneath it, the portrait below that, and the derived discipline list in
the left margin with a small square marking the active one. The set advances one
talent at a time by wheel, trackpad or arrow key, the name changing on a settle
that arrives and stops rather than gliding to a halt. At a phone width the route
becomes a scroll-driven sequence instead: one talent per screenful, the portrait
uncovered from its bottom edge upward, the name moving at a different rate from
its block, and a counter tracking position in the set.

**10. A talent.** `/talents/<slug>` carries the name at exactly the size the
roster sets it, the discipline, the showreel, and the works the talent is
credited on, reusing the work index's entry and caption treatment including the
desaturation. The contact address on this route is the house address and never
the talent's own. No talent email, no phone, no direct social link: a
represented talent is reached through the house.

**11. About.** `/about` carries no photograph at all. It opens on a symmetrical
typographic figure: four lines, the house name repeated seven times down the
middle, then the same four lines in reverse order. Then two paragraphs in the
display face that arrive blurred and sharpen as the visitor scrolls, driven by
scroll position and reversible, so scrolling back up re-blurs. Then a closing
lockup in which small words sit nested into the negative space of large ones
rather than on lines of their own.

**12. The preview harness.** `/preview` resolves an unpublished item by its
identifier and renders it through the same route components its published
counterpart would use, so what the producer sees is what a visitor will see. It
requires a producer session; without one it renders nothing and reveals nothing
about what exists. It carries the marker `PREVIEW - NOT PUBLISHED` in capitals,
visibly and persistently. While it is fetching it shows `Loading preview...`
using the same counter component the entry route uses. Nothing on this route is
indexable and nothing may be held by a shared cache.

**13. The studio.** `/login` signs the producer in. `/studio` carries a sidebar
listing the two kinds and the page-view log, and each kind's list is a grid of
cards showing the poster, the title, the discipline or the ordinal, and whether
the item is published. Adding opens its own route, `/studio/talents/new` or
`/studio/works/new`, rather than a panel over the list. Publishing lands on a
confirmation screen that names what has just become public and what its public
address is. `/studio/works` reorders the index by moving a card. Every studio
route and every write is refused to an anonymous reader and to a `visitor`.

**14. The not-found route.** Any address that does not resolve returns a real
not-found status, in the site's own palette, inside the site's own frame, with
one line in the display face reading `That page is not here.` and nothing else.
No search box, no suggestion list, no sitemap and no illustration. The requested
path is never echoed back into the page.

**15. The page-view log.** Every public page view records one row carrying the
route and the time. Only a `producer` reads it, at `/studio/page-views`. Nothing
personal is recorded, because the public site has no accounts and no forms and
there is nothing to record.

**16. Metadata and sharing.** Every public route emits its own title, its own
description, its own canonical link and its own social preview title,
description and image, and no two routes share a title or a description. The
house description is `A production house for picture and its makers.` The roster
carries the suffix form `VERITE - Talents`, and the same form gives
`VERITE - Works` and `VERITE - About`. The social card is generated: the
near-black ground with the wordmark centred, and no photograph, because the
house's own front page puts no headline over its pictures and a card that
invents one has invented a design.

**17. Named for what it is.** Every still and every portrait carries a
meaningful text alternative: a work by its title and its ordinal, a talent by
their name and their discipline. The centre mark carries none and is hidden from
assistive technology. The wordmark's accessible name is the house name and its
destination, not the word logo. Every route has exactly one top-level heading,
and on the roster the talent's name is it.

**18. Readable at rest and under the pointer.** The near-black ink on the
near-white ground is the working pair and passes comfortably at every size the
site uses. The inactive discipline control rests faded, and its resting state
must still reach a contrast ratio of `4.5:1` against the ground; if it does not,
the resting strength is raised rather than the colour changed. The dimmed label
tone is decorative and is never used for text that has to be read, and the
supporting mid neutral is never used for a control label. Because two elements
composite against whatever is behind them, neither may be the only carrier of
any piece of information.

## User flow

| Route | Who reaches it | What is there |
|---|---|---|
| `/` | anyone | the counter, then the cluster of published stills |
| `/works` and `/works/` | anyone | the opening line, then twelve entries |
| `/works/<slug>` | anyone, published only | one work in full, and the next |
| `/talents` and `/talents/` | anyone | one talent per window, filtered by discipline |
| `/talents/<slug>` | anyone, published only | one talent, and their selected work |
| `/about` | anyone | the figure, the two paragraphs, the lockup |
| `/preview` | `producer` only | an unpublished item, through the real components |
| `/login` | anyone | the producer's sign-in |
| `/studio` | `producer` only | the sidebar and the two lists |
| `/studio/talents`, `/studio/talents/new`, `/studio/talents/<slug>` | `producer` only | the roster as a card grid |
| `/studio/works`, `/studio/works/new`, `/studio/works/<slug>` | `producer` only | the works as a reorderable card grid |
| `/studio/page-views` | `producer` only | the page-view log |

Both collection roots answer on either form of the address. `/works` and the
same address with a trailing slash, `/works/`, resolve to the same surface with
no redirect flash, and `/talents` and the same address with a trailing slash,
`/talents/`, do the same.

`CONTACT` sits in the top bar between `TALENTS` and `ABOUT` and looks exactly
like the other three. It is not a route. It opens a mail composition to
`prod@verite.example.com`, it carries no active state, and it is never marked as the
current route. Building it as a route is the most likely mistake here, because
every other item in that bar is one.

**The commissioner.** Lands on `/`, watches the counter reach `100%`, sees the
cluster. Points at a still: it fades to half and its title appears beside the
pointer. Opens `WORKS`, reads one sentence on an almost empty screen, scrolls,
and brings colour back to one still at a time. Opens `003` into its reel, reads
the credits, follows `Director / Rives` to `/talents/rives`, and mails the house
from the footer.

**The producer publishes.** Signs in at `/login`. Opens `/studio/talents/new`,
enters a name and a discipline, uploads a portrait with its text alternative and
a showreel. The talent is created unpublished. Opens `/preview` with that
item and sees exactly what a visitor would see, marked `PREVIEW - NOT PUBLISHED`.
Publishes. A confirmation names the talent and its new public address. `/talents`
now carries the name, and if the discipline was new a third control has appeared
in the left margin with nobody having edited a list.

**The producer reorders and withdraws.** Opens `/studio/works`, moves the work
numbered `007` above the one numbered `004`, and the public index renumbers on
the next read with no gap. Unpublishes `004`: the index now runs `001` to `011`,
still contiguous, the work's address returns a not-found, and its stills stop
being served.

**The refused reader.** Requests `/talents/odile-marchand` while signed out and
receives the site's own not-found route, which says nothing about whether that
person exists. Requests that talent's portrait bytes directly and is refused.
Signs up, which creates a `visitor`, signs in, requests `/studio`, and is
refused. Attempts to publish an item over the API and is refused, with nothing
written.

## UI/UX notes

The north star: in the first moment a visitor should understand that they are
looking at the work itself and at nothing else, and that the house is confident
enough to put twenty pictures and four small words on its front door and no
sentence explaining them.

The register is print-like and unhurried. Density is spacious on the public site
and comfortable in the studio. The whole site is two colours and everything else
is a state of those two: a near-black neutral warmed toward red, which is the
entry route's ground and all body ink on the pale ground, and a near-white
neutral warmed toward green, which is the ground of every other route. Neither
is a pure value, and building this in pure black and pure white gives a site
that looks right in a screenshot and wrong in a window, because the pure values
have no temperature and these two are a matched warm pair. Four supporting tones
have one job each and none of them is an accent: a deep neutral for the footer
scrim and nowhere else, a near-white neutral for dimmed decorative label text, a
mid neutral for the resting state of an inactive filter control, and a second
deep neutral as a secondary text tone. There is no accent, no brand hue, no
success or error colour and no link colour: a link is distinguished by position
and by its hover, never by colour.

**Restraint is the product, and it is subtractive.** Every hover on the site
resolves to exactly one change, from full strength to half, and nothing else: no
underline, no lift, no scale, no shadow, no colour shift. The only hover that
touches colour removes it, on the work index stills. The one exception is the
inactive discipline control, which rests faded and moves toward full under the
pointer rather than away from it, because its resting state is already faded. A
build that adds a hover lift, a drop shadow or an accent colour has failed this
section even if every other rule is met.

**Motion.** Nothing moves on its own. There is no keyframe animation anywhere,
nothing loops, nothing pulses, nothing drifts, and there is no arrival animation
except the entry counter. Everything that moves does so because the visitor
pointed, clicked or scrolled. There are exactly two durations and the difference
between them must be felt: fast for anything answering the cursor, and slow,
about the length of a deep breath, for exactly two effects, the about route's
blur and the work index's desaturation. Those two are the moments the site wants
noticed and giving them their own duration is how it says so. There is no third,
middle duration, and adding one makes the motion read as inconsistent even
though every individual value is plausible. There are two movement curves: one
leaves quickly and arrives slowly with no overshoot, the other holds, moves late
and settles hard. Nothing bounces and nothing springs back. A name changing on
the roster uses a third curve of its own, which rises slowly, accelerates hard
through the middle and then flattens completely, so the name arrives and settles
rather than sliding into place. Three curves in total, and the whole motion
vocabulary is a closed set of eight declared transitions: no ninth is added. On navigation the
persistent frame and the outgoing content fade together as one thing, not as a
stagger of parts, the new content mounts, the centre mark swaps to the new
route's variant, and everything fades back. The pointer's own marker sits above
that veil and stays visible throughout, so the visitor never loses track of what
they are pointing at.

**Responsive.** There is one real breakpoint and no second one: above it the
wide layout, below it the narrow one. A tablet-width window behaves as the
desktop layout throughout, with one exception, the contact overlay's close
control. Orientation does not get its own rule beyond the breakpoint: a phone
held in landscape is still a phone and gets the narrow layout. Three things
change below the breakpoint. The wordmark
and the top bar retract on scroll on the work index and the about route, and
return, as a threshold and not as a continuous drive. The roster becomes a
different page, a scroll-driven sequence rather than a set that is switched
through. The about route's authored line breaks are dropped and its text arrives
sharp, because a phone reader scrolls faster and holds the device closer, and a
scrubbed blur at that speed reads as a rendering fault rather than as an effect.
On a touch device the work index stills render in full colour, because the hover
that reveals colour cannot be performed there, and the cursor marker is absent
entirely.

**Accessibility.** The near-black ink on the near-white ground is the working
pair and holds a comfortable contrast ratio at every size the site uses, and any
faded resting state that carries meaning is raised until it reaches the same bar
rather than being left to sit under it. Focus is visible on every interactive
element and is not the same treatment as hover: an outline in the ink colour, offset from the element,
on pale grounds, and in the pale colour on the near-black ground. Focus order
follows visual order, and on the roster the discipline controls come before the
talent. A skip link is the first focusable element and moves focus past the
persistent frame to the route's content. The discipline controls are real
buttons in the tab order, operable by enter and space, with their selected state
exposed rather than conveyed only by strength and a small square, and the roster
advances by arrow key with the current name announced on change. Labels set with
letter-splitting, one element per character, expose the whole word as their
accessible name and hide the individual characters from assistive technology and
from selection; this is the most common failure of that technique and it is why
the split is specified as invisible to anything but the eye. Smoothed scrolling must never
intercept keyboard scrolling, anchor navigation or find-in-page. When a reduced
motion preference is set, smoothing is off and native scrolling returns, the
about text resolves to **sharp**, which is its end state and not its start,
roster entries appear in place with no wipe and no drift, reels do not play and
the still remains with a control to start it, the pointer marker is hidden, route
transitions cut rather than fade, and the desaturation still applies on hover but
nearly instantly. That last exception is deliberate: the desaturation is a colour
change carrying information rather than a motion, and deleting it would tell a
reduced-motion visitor less about the work than everyone else sees.

## Front-end specification

### The two grounds and the ink

The entry route's ground is the near-black neutral warmed toward red. Every
other route's ground is the near-white neutral warmed toward green, with the
near-black as ink. No colour outside the two grounds and the four supporting
tones appears anywhere in the build. In particular, the four colours a framework
error page brings with it, a near-black cool neutral, a mid cool neutral, a mid
vivid teal and a pure near-white, appear nowhere, and neither does the colour
scheme preference query that arrives with them: that stylesheet is not part of
this build.

One measured supporting tone, a desaturated deep neutral, could not be placed
against any surface in the source material and is deliberately not shipped.
Finding its carrier is a tuning pass, not a build task.

### Type

Typography carries this site, because two colours and no ornament leave it
nothing else to carry the design. Two typefaces, both variable, both with a
continuous weight axis covering at least `100` to `500`, both loaded with
`swap`.

- **display**: a serif. Fallback `"Times New Roman", Times, serif`.
- **interface**: a neo-grotesque. Fallback
  `"Helvetica Neue", Helvetica, Arial, sans-serif`.

The display fallback must be a serif and the interface fallback must not be,
because `swap` means a visitor on a slow connection sees the fallback render
first and the two roles have to stay distinguishable while they do. A continuous
weight axis is a requirement and not a convenience: the design uses weights
`100`, `200`, `300`, `400` and `500` across both families, and static cuts would
be ten files instead of two.

Four interface size tokens: `24px`, `12px`, `10px` and `8px`.

Three facts the build is held to.

The interface face is set at one size, `12px` at weight `500` with a line height
of `14.4px`, and that single setting carries the top bar, the footer, the
captions and the filter controls. Hierarchy comes from position and from the
display face, never from nudging the interface face up two points.

Line height is a ratio. `1.2` in the interface face. `1.1` in the display face
at its two largest content steps. `0.96` at the figure and lockup steps, where
the display face sets tighter than its own size so a block of it closes up into
a solid shape rather than reading as a list.

Weight falls as size rises: `500` at `12px`, `300` at `18px` and `24px`, `200`
at `40px`, `100` at `36px` and at the lockup's small steps.

The display ladder in use: `125px` at weight `300` with a line height of
`137.5px` for a talent's name; `58px` at weight `400` with a line height of
`40.6px` for the lockup's large words; `56px` at weight `300` with a line height
of `61.6px` for a work's title; `40px` at weight `200` for secondary display;
`36px` at weight `100` with a line height of `34.56px` for the about figure;
`27px` at weight `400` for mid display; `24.75px` at weight `100` with a line
height of `23.76px` and `9.75px` at weight `100` with a line height of `9.36px`
for the lockup's nested words; `24px` at weight `300` with a line height of
`25.2px` for a work index caption; `19px` at weight `500` for numeral labels;
`18px` at weight `300` with a line height of `21.6px` for the about body, which
is the only body-sized text on the site, and the same size at a tightened
leading of `18.9px` where a block of it needs to close up. No size exists
between `24px` and `36px` and none is added. One further setting exists and is
not a type step: a character carrying a letter-split label has its leading
collapsed to zero, because it is positioned rather than typeset.

Case is a hard rule. Every interface-face string renders in capitals. Every
display-face string renders in capitals except talent names and work titles,
which are title case. The interface face speaks in capitals and the display face
speaks in sentences, and the two exceptions are both content rather than chrome.
Capitals in the interface face carry tracking, and the smaller the label the
more of it.

### The persistent frame

Eight elements exist once, mount before the first route renders, and survive
every navigation without remounting: a fixed full-window frame; the wordmark at
the top left; the top bar; the centre mark at the optical centre; the pointer
pair; the studio credit at the bottom right; the footer and its scrim; and the
counter well. Everything else belongs to a route and is replaced on navigation.
The persistent frame must not be a child of the route outlet in any form,
including a shared layout that re-renders, because every transition depends on
it being the same nodes throughout.

**The wordmark** is the house name set in the display face, lowercase, at the top
left. It composites against whatever is behind it by difference rather than
being painted in a fixed colour, which is what lets one wordmark sit legibly over
the near-black entry route and the pale work index without a script switching its
colour. A difference-blended element over the pale ground renders as its own
inverse, and over the near-black ground it renders near-white, which is why the
wordmark is authored once, in the dark ink, and never in a light and a dark
version. Difference blending forces its own compositing layer, which is the
reason there are exactly two blended elements on the site and no more. It links to `/` and it suppresses the pointer's square.

**The top bar** carries four items in the interface face, in capitals: `WORKS`,
`TALENTS`, `CONTACT`, `ABOUT`. It is asymmetric, and this is the easiest thing
here to get wrong: `WORKS` sits at the horizontal centre of the window on its
own, and the other three are grouped at the right. Four evenly spaced items is a
different design.

**The centre mark** sits at the optical centre, slightly above true vertical
centre, and changes with the route: one variant for the entry, one for the work
index, one circled-letter variant for the roster, and one for about, which is
the only route carrying a second mark, part of its opening block's composition
rather than part of the frame. Every variant is the same height. The mark is not
interactive, carries no link and is hidden from assistive technology.

**The pointer pair** is a small square that follows the pointer and a text label
beside it. It composites by difference. When inactive it is parked far off the
top left rather than hidden, which keeps it composited and avoids a stutter on
first move. It follows the pointer with a frame-rate independent lag so that it
arrives a moment after the pointer rather than locked to it. Any element may
carry an opt-out flag to suppress the square, and a directional variant places
the label above the pointer instead of beside it. The pair is hidden entirely on
pointer-coarse devices.

**The studio credit** at the bottom right links to the design studio's own site
and opens in a new context. On hover one arrow travels up and to the right while
a second enters from below and left. It must remain legible on the near-black
entry route: painting it in flat dark ink there makes it invisible, which is a
fault to fix rather than a design to reproduce.

**The footer** carries four columns in the interface face, in capitals: the
premises, with the street line `9 PASSAGE BELLEVUE` over the city `PARIS` and
the district `11` right-aligned in its own column; the two-line house line `FOR PICTURE` over `AND ITS MAKERS`; then
`WORK WITH US` over `prod@verite.example.com`; then `INSTAGRAM` over `LINKEDIN`,
right-aligned. The two-line house line is the one string that appears in three
places, here, in the about lockup and in the document description, and its second
line is always the longer of the two because the lockup's composition depends on
it. Behind the footer sits a scrim: a gradient rising from the deep neutral at
full strength just below the bottom edge, to half transparency around two fifths
of the way up, to fully transparent at the top. It is scaled beyond its own box
so its top edge never shows. Its job is to keep the footer's capitals legible
over whatever the route has put behind them.

**The counter well** is one component with two jobs: it counts load progress on
the entry route, and it counts position in the set on the roster at a phone
width. It suppresses the pointer square.

**The contact overlay** is a panel whose items are parked below their resting
position and rise into place in a stagger with a fade. At a narrow width it is a
full-screen panel with an explicit close control. It traps focus while open,
returns focus to the control that opened it on close, and closes on the escape
key. It is not a route.

### Depth

Build to this ladder rather than inventing one: the pointer pair above
everything, then the loading overlay and the transition veil, then the top bar,
then the wordmark and the studio credit, then the fixed frame generally, then
the footer and its scrim, then the centre mark, then route-level pinned
elements, then content in document order. Two values are worth defending: the
pointer pair sits above the transition veil so the pointer never disappears
mid-navigation, and the centre mark sits below the fixed frame but above
content, so a name in the roster passes in front of the wordmark and behind
nothing else.

### Iconography

Nine distinct vector marks. There is no icon font, no sprite sheet and no
image-based icon anywhere: every mark is inline vector geometry in the markup.
Three are standard symbols and six are the house's own artwork, which means six
of them are slots with a fixed box, position and fill, sized so that real
artwork drops into a correctly proportioned hole.

Four rules fall out of the mark inventory and all four are requirements.

Every centre mark is the same height and sits at the same vertical position;
only the width varies, and the horizontal origin moves to compensate so all four
stay centred on the window's horizontal midpoint. That is one slot with four
occupants, not four independently placed icons.

**Icon sizing.** Marks are sized by their **height**, never their width, because
the centre slot varies by nearly a factor of three in width at a constant
height. A build that constrains marks by width makes the entry route's mark
small and the work index's mark large, which is the exact inverse of the design.
Four sizes exist and nothing between them: the smallest for the two outbound
arrows beside the studio credit; the centre-mark height for the four route
marks; a slightly smaller height for the studio credit; and a slightly larger
one for the wordmark glyph and the about route's second mark, both of which sit
inline with display type.

**Optical centring.** The centre mark is positioned at half the window's height
minus a small optical correction, not at half exactly, and the correction is
applied as a transform offset rather than by changing the top value, so the mark
stays centred when the window is resized. It reads as centred precisely because
it measurably is not. Horizontal centring is true centring, with no correction.

**The circled letter.** The roster's centre mark and the about route's second
mark are the same construction at two sizes: three concentric contours in a
single path, the counter cut by the winding rule, with the letterform inside the
ring. The outer contour spans the full width of the box horizontally and its
full height vertically; the inner contour is inset evenly from it on every side. The ring's thickness is a little under a tenth of the mark's width. The
roster's is a true circle and the about route's is an ellipse, wider than it is
tall, and that difference is not a bug to correct: the elliptical one sits beside
the lockup's large display type and was optically widened to match its
proportions.

**The outbound arrow** beside the studio credit is a square corner bracket
occupying the upper right of its box with a diagonal stroke running from the
lower left corner up into it. It is the one genuinely generic mark on the site
and it appears twice, the same path at two positions offset down and to the
left, which is the resting and arrived pair of the credit's hover.

**What is not an icon**, and each of these will be mistaken for one. The four
elements named after the routes are not icons: they are the centring transforms
of the four centre marks, each carrying a vertical offset equal to half the
mark's height plus the optical correction, and a horizontal offset of exactly
half its own width. The pointer's square is a square, not a mark. And the
wordmark itself is display type rather than vector artwork, with the single
exception of the one glyph set as a superior inside the about route's lockup.

### Module and component architecture

Two trees, one of which never unmounts.

The persistent tree holds the fixed frame, the wordmark, the top bar, the centre
mark slot, the cursor pair, the studio credit, the footer with its scrim and
list, the counter well and the contact overlay. It mounts once and never
unmounts. The route tree swaps beneath it and is what drives the transition
state class. It holds the entry cluster, the work index, a work, the roster, a
talent, about, the preview harness and the not-found route.

Six units are used by more than one route and each is built once, not three
times: the media tile, which is one component with a variant rather than three
components, since the index's three entry widths share one base and one hover
behaviour and differ only in geometry; the caption row, shared by the work
index, a work and a talent; the reveal layer, shared by the roster portrait and
the work index entries; the counter well, shared by the entry route, the preview
harness and the roster at a phone width; the blur block, shared by the about
body and the work index's opening line; and the display line, wherever the
display face is set.

Four naming conventions are worth adopting wholesale, because they are what keeps
the markup readable. A container or wrapper around a thing carries a wrapper
suffix. An element that is a transform or clip target carries an animation
prefix. An element that opts out of a global behaviour carries an opt-out
suffix. And a transient state, such as the one driving a route transition, is a
class added and removed rather than a permanent one. Keep the opt-out convention
in particular: a class any element can carry to suppress the cursor square is a
better design than a list of exceptions held inside the cursor component, and it
is why that logic stays small.

### The scroll system

The entry route, the roster at a wide window and the preview harness do not
scroll. The work index and the about route do, and both are long.

One scroll-position source feeds every scrubbed property on the site. Three
components must not each attach their own listener. The source publishes
position once per frame; scrubbed effects register a range and a callback
against it; and it writes a class to the document root while a scroll is in
flight, so styling can respond to "a scroll is in progress" without a script
touching style. Wheel and trackpad input is smoothed and the position is
available to the effect system as a continuous value.

Three effects are registered against it. The footer arrival: over the last third
of both long routes the footer travels up into place while its scrim fades in,
with the list inside it held below its resting position and closing that
distance across the same range. This is the site's only scroll-driven positional
move, and it is what makes the bottom of a page feel arrived at rather than run
out. The about blur, specified below. The roster sequence at a phone width. On
the work index and the about route at a phone width, the wordmark and the top
bar retract and return on a threshold.

A reduced-motion preference disables the source, and every effect registered
against it falls to its **end** state and not its start state. That is the one
built backwards most often: the blur is the start state and sharp is the end
state, so disabling the effect must resolve to sharp.

### The media layer

Whatever renders the media must do six things. Hold an arbitrary number of
quadrilaterals in a plane, each carrying one image, each independently
positioned, scaled and depth-ordered. Play a reel into a quadrilateral in place
of its still, without a visible reload and without changing the quadrilateral's
geometry. Apply a per-quadrilateral colour transform, at minimum a desaturation
amount drivable from full to none. Apply a per-quadrilateral reveal that clips
from the bottom edge upward. Hold a steady frame rate with a dozen quadrilaterals
on screen at once on a three-year-old laptop on integrated graphics. And degrade
to plainly composited images when the rendering layer is unavailable, with the
same layout, the same reveals and the same hover behaviour, losing only the
smoothness.

The layout is flat. No perspective, no three-dimensional transform.

The fallback is not optional and it is a requirement rather than a nicety: with
the rendering layer unavailable, every work must remain reachable and captioned,
every talent reachable and labelled, every reveal completing and every hover
responding. The rendering layer carries smoothness, not content. If a
post-processing pass is built, it is a very slight grain and a vignette at an
intensity that is barely visible; if it is visible, it is wrong, and it is
cheaper to delete an invisible pass than to justify a visible one.

Reveals are wipes from the bottom edge, never fades and never scales: the top
inset drives from fully clipped to not clipped at all, with a lateral slide
running alongside it. Stills are overscaled very slightly inside their clip so
that a reveal never exposes a sub-pixel edge, and that scale is never animated.

### Reels

A work's reel plays in place of its still, muted, looping, without controls, and
only while it is in view. The still must be visible before the reel is ready and
must never be replaced by a blank frame at any point; this is the failure most
likely to survive into production. One rendition, progressive, at a low size.

### Route compositions

**The entry route.** Near-black ground. The counter renders at the optical
centre in the display face and is re-centred by measured offset on each change,
so the string stays optically centred as it widens from one digit to three; a
static centre drifts by about half a character. A veil covers the cluster while
loading and fades out as the counter completes. The cluster's stills range from
small to roughly twice that on their long edge, overlap freely with no grid and
no consistent gutter, and their overlap order is authored and stable. Pointing
at one fades it to half; it does not lift, scale, brighten or gain a caption in
place, because the caption is the pointer label. The front page does not label
its own contents, and that is deliberate.

**The work index.** Pale ground. The opening line sits with its baseline near
the bottom of the first screen, running nearly the full width at a wide window
and breaking to two lines. The first screen is otherwise empty ground with the
centre mark in the middle, and that emptiness is the route's opening gesture and
what makes the first entry land when it arrives on scroll: do not fill it. The
three entry variants are a wide one flush left, a narrow one flush right, and a
centred one that is nearly full width and breaks the left-right rhythm. Vertical
gaps between entries are large. The caption row spans the still's own width, so
the number sits at the still's left edge and the title at its right and the gap
between them varies with the variant; that variance is the design. Every still
rests fully desaturated and returns to full colour under the pointer, slowly
enough to watch it happen, and drains again on leaving.

**A work.** Pale ground. Title in the display face at the second step, ordinal
and credits in the interface face, the reel full width, then a vertical sequence
of stills in the same three variants the index uses, then next and previous
following the ordinal and wrapping at both ends, each labelled with the
neighbouring work's title in the display face. No breadcrumb and no back-to-index
link: the top bar already carries one.

**The roster.** Pale ground. At a wide window: the name centred in the upper
third at the largest display step, in title case, the discipline label centred
beneath it in interface capitals, the centre mark, then the portrait centred
below. The discipline controls sit in the left margin at the same margin the
work index uses for its flush-left entries, one margin serving both routes, with
a small square marker level with the active one. A name that will not fit the
window at the largest step reduces to fit rather than wrapping, because the
label, the mark and the portrait are all positioned from fixed offsets and none
of them moves to accommodate a second line. At a phone width the name and the
portrait are sized from the window's height as well as its width, so name,
label, mark and portrait always compose to one screenful.

**A talent.** Pale ground. The name at exactly the roster's size, which makes
arriving here read as the roster opening rather than as landing on a different
page. Discipline, showreel, then the credited work using the index's own entry
and caption components; do not build a second, smaller card for this route.

**About.** Pale ground, no media of any kind. The opening figure is symmetrical
about its horizontal midline and the line order above the centre is reversed
below it; setting it as a plain list or breaking the symmetry loses the whole
gesture. The long lines run to roughly the same length as each other with the
longest in the middle of the group, which is what gives the figure its taper.
The body's first paragraph is broken into seven short lines by explicit markup,
each its own element: those breaks are content, not layout, and must not be
re-wrapped to the container at a wide window. The second paragraph is one long
line running nearly the full width. The closing lockup is one typographic figure
and not a heading with subheadings: three sizes, all capitals, weights falling as
size rises, the large step's line height well under its own size so the small
words nest into the negative space beside the large ones rather than sitting on
their own lines. Build it as a positioned composition; it will not survive
reflow. At a narrow width it stacks to two sizes, keeps the ratio and abandons
the nesting, the figure keeps its mirror at a reduced size, and the body's
authored breaks are dropped.

### The copy deck

Every string below is exact.

Navigation: `WORKS`, `TALENTS`, `CONTACT`, `ABOUT`.

Footer: `9 PASSAGE BELLEVUE`, `PARIS`, `11`, `FOR PICTURE`, `AND ITS MAKERS`,
`WORK WITH US`, `prod@verite.example.com`, `INSTAGRAM`, `LINKEDIN`.

Work index opening line:
`Quiet decisions, made early, are the ones you notice last.`

The twelve works, in seeded order, with the ordinal they display when all twelve
are published:

| Ordinal | Title | Slug |
|---|---|---|
| `001` | `The Halo` | `the-halo` |
| `002` | `Sonder` | `sonder` |
| `003` | `BINARY` | `binary` |
| `004` | `Common Ground` | `common-ground` |
| `005` | `NVE` | `nve` |
| `006` | `The Absolute Shelter` | `the-absolute-shelter` |
| `007` | `MAISON DE LUMIERE` | `maison-de-lumiere` |
| `008` | `LORIS` | `loris` |
| `009` | `MDL Serie Extreme` | `mdl-serie-extreme` |
| `010` | `AK` | `ak` |
| `011` | `Loris Shoot Studio` | `loris-shoot-studio` |
| `012` | `The Radiant` | `the-radiant` |

The roster, published:

| Name | Discipline | Slug |
|---|---|---|
| `Rives` | `director` | `rives` |
| `Halcyon` | `director` | `halcyon` |
| `Camille Ferrand` | `photographer` | `camille-ferrand` |

Filter labels, in interface capitals: `DIRECTOR` and `PHOTOGRAPHER`. They and the
discipline labels beneath a name come from the same source and are not authored
twice.

About, the opening figure. Four lines, the house name seven times, then the same
four lines in reverse:

```
PICTURES PATIENTLY MADE
PRACTISED HANDS, PLAIN PURPOSE
PEOPLE WORTH PUTTING FORWARD
PICTURE AND ITS MAKERS
VERITE
VERITE
VERITE
VERITE
VERITE
VERITE
VERITE
PICTURE AND ITS MAKERS
PEOPLE WORTH PUTTING FORWARD
PRACTISED HANDS, PLAIN PURPOSE
PICTURES PATIENTLY MADE
```

About, the first paragraph, seven authored lines:

```
We build, we bend,
we break and rebuild,
making things that last
while asking what
comes next. VERITE is a
production house working
between the settled and the untried.
```

About, the second paragraph, one line:

```
Founded in PARIS, working wider. We support brands, agencies and artists with picture, from first idea to final delivery: production, casting, studio and post.
```

About, the closing lockup. Largest step: `VERITE`, `PICTURE`, `MAKERS`. Middle
step: `PROD`, `FOR`, `AND`. Smallest step: `ITS`. Reading order is `VERITE` with
the house mark set as a superior after it and `PROD` tucked beneath, then
`FOR PICTURE AND ITS MAKERS` with `FOR`, `AND` and `ITS` nested into the gaps
beside `PICTURE` and `MAKERS`.

Preview harness: `Loading preview...` while fetching, and the persistent marker
`PREVIEW - NOT PUBLISHED`.

Not found: `That page is not here.` and nothing else.

Document description: `A production house for picture and its makers.`

Accessible names that never render: the wordmark is `VERITE, home`; the skip
link is `Skip to content`; a work's still is its title then its ordinal; a
talent's portrait is their name then their discipline; the studio credit is
`Site by AUBE, opens in a new tab`; the centre mark has none.

### Generating every asset: the zero-asset substitution

No binary ships, and every class of asset the site would normally carry has a
generated substitution instead. Stills are served in a modern image format with
a fallback, at the widths the three entry variants require and no more. Each
still is generated from its item's own identifier used as
a seed, so the same item always produces the same field: a gradient between two
of the supporting tones at an angle derived from the seed, a second gradient
over it at a different angle and low strength so the field is not a flat ramp,
and grain over the whole thing. Nothing else is drawn on it: no text, no
dimensions, no diagonal cross. A placeholder that announces itself makes every
review about the placeholder.

Two of the supporting tones carry real saturation, and that matters: the work
index's whole effect is colour draining out and flooding back, and on a fully
grey placeholder that effect is invisible and would ship unverified.

Each reel is a generated looping motion field drawn each frame rather than
decoded: the still as its base, displaced slowly along one axis with the phase
from elapsed time and the direction from the seed over a cycle of about twelve
seconds, the overall brightness varying by a few percent on a second slower
cycle so the loop point is not visible, and the grain redrawn fresh each frame,
which is what makes it read as film rather than as a moving picture. The
generated reel obeys every reel rule exactly as a real file would; building the
placeholder outside the budget rules means the budget rules are untested until
the day real footage arrives, which is the day they matter.

The grain is one tiling monochrome noise field generated once at build time and
reused, fine, over several octaves so it has tonal variation, fully desaturated
so it does not speckle in colour against a near-monochrome design, and
composited at very low strength: enough to break the gradient banding and no
more. It is a tile, not a per-element generation.

The wordmark stands in as the house name set in the display face, lowercase,
composited by difference. The four centre marks stand in as drawn geometry: a
horizontal ellipse for the entry, three filled rectangles for the work index, a
circled letter for the roster, and two overlapping circled letters for about. The
social card is generated at build time: the near-black ground with the wordmark
centred and optically raised, at the conventional social card proportion.

## Technical requirements

Every route leaves the server as finished markup, and the interactive pieces
enhance that markup rather than replacing it. The front end is `Alpine.js` layered
over server-rendered templates. The backend and the HTTP API are `Flask` with
`Jinja`, answering on the site's own origin under `/api`.

Records for works, talents, credits, media and page views go into `PostgreSQL`,
found at `DATABASE_URL`. Every poster, still and reel goes into `minio`, the
S3-compatible object store at `STORAGE_ENDPOINT`: the bucket name comes from
`STORAGE_BUCKET`, and the key pair from `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. The producer signs in with an email and a password the app
itself checks; passwords are stored hashed and sessions travel as bearer tokens.
Once the house is ready to serve, `GET /api/health` answers `200`. Each request
the server handles writes a single line to stdout.

Because the server renders first, a route reached with scripting unavailable
still lists every published work with its ordinal and its caption and every
published talent with their discipline, which is the same obligation the media
layer's fallback carries.

The dependency list is the libraries named above and what they pull in, nothing
more. `PostgreSQL` and `minio` are the only backing services this house runs on;
standing up another database, a cache, a queue, a second object store, an
identity service or a mail vendor is a contract violation. Hosts, ports, keys and
passwords all come from environment variables and none is written into the code.
Both services are up before the app starts, so they are never fetched, installed,
built or launched by it.

**Reels are the whole performance story.** In the material this site is built
from, video was three quarters of every byte transferred, against everything
else on the site put together. So: no reel has a source until its still is
within one window height of the viewport. A reel more than one window height
outside the viewport is paused and its buffer released. Never more than two
reels play at once, however many are on screen. On the entry route the answer is
none, because that route is stills only. A save-data hint, a metered connection
or a reduced-motion preference suppresses reels entirely and leaves the stills.

**The frame rate during any scrubbed effect is the primary quality bar.** Hint
only what is currently animating and remove the hint when the effect ends; a
hundred permanent hints are a hundred permanent layers. Only compositing
properties are animated, and nothing animates a property that triggers layout.
The two elements that composite by difference are permanent layers by necessity
and there are exactly two of them, which is the correct number. There is no
blanket transition on every property: the motion vocabulary is the closed set
described in `## UI/UX notes` and nothing watches every animatable property for
change.

**No layout shift.** Every media reference carries its intrinsic dimensions so a
tile reserves its space before the image arrives. The work index is a long
scroll of large images and layout shift on it is disqualifying.

**Fonts.** Both families are preloaded, since both render above the fold on
every route, and both are subset to the characters actually used: Latin,
capitals-heavy, with numerals. The fallback stacks must not visibly reflow the
roster's name at its largest step, where a swap-induced reflow is the height of
the name itself.

**The counter reports real progress** against a defined set: the two font files,
the frame and the entry cluster's stills. It does not include reels, which are
not fetched at that point, and it is never a fixed-duration animation dressed up
as a measurement. A counter that reaches `100%` before the route is ready is
worse than no counter, because it teaches the visitor not to believe it.

**Metadata and sharing.** Each public route declares a title, a description, a
canonical address and a share card of its own, and a title or description used on
one route is used on no other. The share card declares the type as a
website, the route's own address, a title, a description and an image that
resolves, with the large-image card form. No locale alternate is declared,
because there is one language and one origin.

**Nothing the browser downloads carries a credential.** No object-store secret,
no database password, no bearer token belonging to a producer and no API key
appears in any document, script, stylesheet or source map the browser can fetch.

**Security headers.** Every response carries a content-type options header
refusing to sniff, a frame-ancestors restriction, a referrer policy, and a
content security policy that permits only this origin. Responses from `/preview`
additionally forbid storage by a shared cache and forbid indexing.

**The running site calls nothing outside this environment.** The page-view log is the app's own and is read only by a
`producer`.

## Data model

Six tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account.

**accounts.** An id, an email that is unique and compared without regard to
case, a password hash, a role that is one of `producer` or `visitor`, and a
creation time.

**items.** The one resource shape, because a work and a talent are almost the
same object. An id that is stable and opaque and is never derived from the
title; a kind that is one of `work` or `talent`; a slug that is unique within
kind; a title, which for a talent is their name; a sort key, works only, which
fixes the producer's order; a discipline, talents only, a lowercase token; a
variant, works only, one of `left`, `right` or `centre`; a summary paragraph; a
published flag; a published time that is null while the item is unpublished; and
a creation time.

There is no ordinal column. The displayed `001` through `012` is computed at
read time over the published works in sort-key order, so it is contiguous by
construction and a visitor can never see a gap.

**media.** An id, the owning item, a role that is one of `poster`, `still` or
`reel`, a unique object key, a content type, a byte size, a digest of the bytes,
the intrinsic width and height which are never null, alternative text which is
never null, a position that orders a gallery, and a creation time. The object key
is `items/{item_id}/{sha256_of_bytes}.{ext}`. The row records where the bytes
are; the bucket is where they are. Exactly one `poster` per item, and at most one
`reel` per item.

**credits.** An id, the owning work, a role such as `Director`, a name, an
optional talent reference, and a position. The talent reference is optional
because a credit commonly names someone the house does not represent, which is
the common case. A talent's selected work is derived by reading credits and is
never stored on the talent: one relation, in one place.

**slug_redirects.** An id, a kind, an old slug that is unique within kind, the
item it now points at, and a creation time.

**page_views.** An id, the public route viewed, and the time of the view. One row
per public page view.

**Invariants, as properties of the running system.**

- An item that is not published is absent from every public listing, is answered
  with a not-found on a direct public read by its slug, and its media bytes are
  refused to anyone who is not a `producer`. Publishing makes listing, address
  and media readable in one act; unpublishing makes all three unreachable again.
- The displayed ordinals over the published works are contiguous from `001` with
  no gap and no duplicate, before and after any publish, unpublish or reorder.
- A slug is unique within kind, and a title change never changes a slug. A slug
  change writes a redirect row and the old address keeps resolving.
- Every media row carries non-empty alternative text, and publishing an item
  whose media lacks one is refused.
- An object key is unique. Two uploads of identical bytes for one item resolve to
  one object, never two.
- The discipline set a visitor sees is the distinct disciplines of published
  talent, in first-appearance order, and is never an authored list.
- A refused write writes nothing at all: no row, no partial row, no object.

**Seed data.** Three accounts, as listed in `## User roles`. Twelve published
works, the table in `## Front-end specification`, with sort keys in that order
and variants following the authored rhythm. Three published talents: `Rives` and
`Halcyon` as `director`, `Camille Ferrand` as `photographer`. One unpublished
talent, `Odile Marchand`, discipline `director`, slug `odile-marchand`. One
unpublished work, `The Quiet Room`, slug `the-quiet-room`, sorting after the
twelve. Every item carries a poster with alternative text; a subset also carry a
reel and stills. Every work carries credits, and at least one credit per work
refers to a published talent. No page views are seeded.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One house. There is no organisation, no team, no workspace and no second
  tenant.
- No search, no sort, no tag, no category, no year and no pagination on the work
  index. That absence is a design decision: twelve works in one authored order
  are the route.
- No contact form of any kind. The house gives one mail address. Enquiries to a
  production company are long messages with a brief and attachments, and a form
  with three boxes makes that worse for everybody.
- No cart, no payment, no pricing, no subscription. The product sells nothing.
- No blog, no news, no comments, no likes, no ratings, no messaging.
- No talent email, no talent phone number and no direct social link for a
  represented talent, on any route.
- No language switch and no second locale.
- No third-party analytics and no external network call at run time.
- The build ships zero binary assets. Every still, reel, mark, font fallback,
  grain tile and social card is generated.
- The source material has honest gaps, and where the evidence ran out the
  requirement is stated as a behaviour rather than as a geometry. One measured
  supporting tone could not be placed against any surface and is not shipped
  until its carrier is found. The blur radius endpoints on the about route were
  never recovered: set them by eye against a running build, which is why the
  effect is specified as driven by scroll position rather than by fixed offsets.
  What matters there is the mapping, full blur when a block is a screen away and
  none when its centre reaches the window's centre, not the radius.
- The advance mechanism on the roster at a wide window, the layouts of the two
  detail routes, the contact overlay and the letter-splitting motion are
  reconstructions rather than measurements. Each is specified by what it must do,
  and a build that satisfies the behaviour has satisfied the reconstruction.
- Two typefaces must be substituted, because the originals are licensed and no
  licence ships here. Any variable serif and any variable grotesque will do so
  long as each carries a continuous weight axis; static cuts are not an
  acceptable substitution, because they would either cost eight extra files or
  force the design to abandon the rule that weight falls as size rises. Verify
  the substitute at the roster's largest step, which is the most exposed setting
  on the site.
- The product must stay responsive with the seeded content and with a few
  thousand page-view rows.

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
| `GET /api/works` | none | a top-level array of published works in order, each with its computed ordinal |
| `GET /api/works/{slug}` | none | one published work with its credits, media and neighbours |
| `GET /api/talents` | optional `discipline` | a top-level array of published talent |
| `GET /api/talents/{slug}` | none | one published talent with their media and derived credited work |
| `GET /api/disciplines` | none | a top-level array of the derived discipline set, in first-appearance order |
| `GET /api/items` | optional `kind` | a top-level array of every item, published or not |
| `POST /api/items` | `kind`, `slug`, `title`, and `discipline` or `variant` | the created item, unpublished |
| `PATCH /api/items/{id}` | any editable field | the updated item |
| `POST /api/items/{id}/media` | the bytes, `role`, `alt_text`, `width`, `height` | the created media row with its object key |
| `POST /api/items/{id}/publish` | none | the published item |
| `POST /api/items/{id}/unpublish` | none | the unpublished item |
| `POST /api/works/order` | an ordered array of work ids | the works in their new order |
| `POST /api/items/{id}/credits` | `role`, `name`, optional `talent_id` | the created credit |
| `GET /api/preview/{id}` | none | one unpublished item in full |
| `GET /api/media/{id}` | none | the object's bytes, or a link to them |
| `POST /api/page-views` | `route` | the recorded view |
| `GET /api/page-views` | none | a top-level array, newest first |

Field names are exact. A list endpoint returns a top-level JSON array. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a
silent success. Bearer authentication is required on everything except signup,
login, health, the public read routes and the page-view record.

### No mocks

`minio` is where the bytes live. An in-memory buffer the app hands back to
itself, a file written to the app container's own filesystem, a base64 column in
`PostgreSQL`, or a hardcoded object key pointing at nothing are each a contract
violation however good the upload interface looks. The named provider is the
fact: the app's own tables can only reflect what lives in the provider, never
substitute for it.

## Definition of done

A stranger moves down the index of twelve films, opens `003` into its reel,
follows a credit to `/talents/rives`, and mails the house from the footer,
passing ordinals that run `001` to `012` with nothing missing. A talent the
producer has signed but not published is reachable by nobody outside the studio,
on any path, and their portrait is never served; publishing makes the roster
entry, the address and the media readable in one act. Every uploaded byte lives
in the `minio` bucket at its scheme's key.
