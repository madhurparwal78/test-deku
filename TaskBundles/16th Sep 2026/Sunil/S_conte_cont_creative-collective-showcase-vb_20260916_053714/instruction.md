# Kanso London Creative Collective Showcase

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
scroll the home route through its pinned recent-work reel, filter the work index
down to a single discipline, and send the studio an enquiry that the studio editor
can then read in the console, without hitting an error page. The hard part is the
protected half: one seeded project is an unpublished draft, and it must be absent
from the index, absent from every discipline filter, absent from the home reel and
absent at its own address, while its cover bytes are refused to anyone who is not
the studio editor. Its bytes must live in the MinIO bucket at their scheme's key;
a copy on the app's own disk does not count, and a page that merely declines to
draw a thumbnail while the object is still fetchable is not a boundary.

## Overview

Kanso London is a design-driven creative studio, born in Tokyo and based in
London. This is its showcase site. The studio does brand, spatial, campaign,
digital, video, photography and illustration work, and it treats each project as a
chance to do something for the first time. The site's job is not to transact. It
is to make that claim vivid through motion and craft, and then to collect exactly
one action: a visitor reaching out to start a conversation.

Four audiences arrive and each is served in a different stretch of the site.
Prospective clients ask whether this studio could make their brand feel like this,
and are answered by the hero, the pinned recent-work reel and the work index.
Peers and press ask what has shipped and who noticed, and are answered by the work
index, the press timeline and the featured series. Prospective hires ask who works
here, and are answered by the team story, the member grid and the founding
history. Returning visitors want the work directly, and are answered by the
persistent header, the world-clock strip and the footer sitemap.

Behind the public site there is a small studio console. A signed-in studio editor
creates a project, uploads its cover and its press kit, and publishes or
unpublishes it. A registered press contact can sign up and download the press kit
of a published project. Everything else the visitor sees is read-only.

The site deliberately is not: no customer account, no cart, no payment, no
invoice, no subscription, no comments, no likes, no sharing, no newsletter, no
search, no realtime channel, no email delivery. The three world clocks are
computed on the visitor's own device and never fetched.

The genuinely hard part is that the protected content must be protected at the
store and not merely in the page: a draft project's cover and every project's
press kit are objects in a bucket, and the only route by which either reaches a
browser is the app's own media endpoint, which decides entitlement before it
streams a byte.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Anonymous visitor | read every published route: home, work, press, team, services, contact, privacy; filter the work index and the press feed; accept or decline the cookie choice; submit one enquiry | **cannot see a draft project anywhere**, **cannot fetch a draft project's cover bytes**, **cannot download any press kit**, **cannot read any enquiry**, **cannot open the studio console** |
| `reader` | everything an anonymous visitor can do, plus download the press kit of any published project | **cannot see a draft project**, **cannot fetch a draft project's cover bytes**, **cannot read an enquiry**, **cannot open the studio console**, **cannot create, edit, publish or unpublish anything** |
| `author` | everything above, plus create a project through the studio console, upload its cover and its press kit, publish and unpublish it, and read every enquiry and every page-view record | **cannot be created by signing up** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `author`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged. The same
holds for reads of protected content: a direct request for a draft project's cover
object, made by a `reader` or by nobody at all, is denied and no bytes are
returned.

Signup is open. Registering at `/signup` creates a `reader` and nothing else;
there is no path by which signing up produces an `author`. The studio editor
exists only because the app seeds it.

Seeded accounts, both on the same password:

| Email | Role |
|---|---|
| `author@example.com` | `author`, the studio editor |
| `reader@example.com` | `reader`, a registered press contact |

## Core features

### Auth

Email and password, implemented by the app. Passwords are stored hashed, never in
plain text. A successful sign-in at `POST /api/auth/login` returns `access_token`, which the
client sends on every later request as an `Authorization: Bearer <token>` header; the token
expires, and an expired token on a mutating request is refused with the work left
unwritten. `/signup` creates a `reader`. There is no password reset and no
external identity provider.

1. Signing in with a seeded email and the correct password succeeds and returns a
   token. Signing in with a wrong password is rejected as invalid, no token is
   returned, and the failure names no detail that distinguishes a wrong password
   from an unknown address.
2. A request to any `author`-only endpoint carrying no token, an expired token, or
   a `reader`'s token is denied, and the state it targeted is unchanged.

### The persistent shell

The header, the world-clock strip, the custom cursor, the cookie rail and the
footer survive every route change. The main content is replaced behind a
full-bleed transition veil that carries the studio wordmark and releases the
header once the incoming route has mounted.

3. Moving between routes updates the address bar to the destination path, and the
   browser's back and forward controls restore the previous route and the scroll
   position it was left at.
4. A cold load of any deep path, `/work`, `/press`, `/team`, `/services`,
   `/contact` or `/privacy`, renders that route directly rather than the home
   route.
5. The header carries the wordmark on the left; the primary trio `Home`, `Work`,
   `Services`; the secondary set `team`, `contact` and `PRESS & NEWS`, whose
   casing is reproduced exactly as written here; and the world-clock strip on the
   right. At narrow widths the primary links collapse behind a burger that opens
   a full-screen overlay, and the clock strip is retained.
6. The three world clocks show the current wall time in London, Tokyo and New
   York, formatted twelve-hour with a meridiem, updating at least once a minute.
   They are computed from the visitor's own clock and fixed zone offsets, and are
   never fetched from anywhere.
7. Every internal link on every public route resolves. `Services`, `Contact` and
   `Privacy policy` are real routes with authored content, not dead labels.
8. The footer carries the call to action `WE WOULD LOVE TO HEAR FROM
   YOU.`, the supporting line `Feel free to reach out if you want to collaborate
   with us, or simply have a chat.`, the contact address `hello@kanso.studio` set
   at the display size with a trailing `→`, the address block `Our Address`,
   `Unit 4, Maker Yard`, `12 Ashfield Road`, `E1 7QT, London`, `United Kingdom`,
   the VAT registration `VAT: GB 000 0000 00`, the company number `Company no.
   00000000`, `Registered in England &
   Wales`; the socials `Follow us`, `Instagram`, `Linkedin`; the tertiary links
   `Kanso TKY`, `Kanso NYC`, `POWERED BY TOKYO`; the sitemap column `Home`,
   `Work`, `Services`, `Team`, `Contact`, `PRESS & NEWS`, `Privacy policy`; the
   copyright `© Kanso London LTD 2024 All rights reserved`; and a `top` control
   with an `↑` that returns to the top of the route.

### The home hero

9. The hero fills the first screen: a full-bleed colour field drifting over a
   near-black ground, a fine grain over the field, and a circular glass lens over
   the centre that magnifies and bends what sits beneath it and splits it into
   red, green and blue fringes that separate more toward the rim. The lens drifts
   on a slow path of its own and reacts to the pointer.
10. The headline is real selectable text composited over the field, not painted
    into it. It reads, on three lines, `We are a brand`, `of collective`,
    `creativity`, and a set of Japanese glyphs for the word "creativity" sits
    beneath the lens. A foot row carries three label pairs: `Based in London` over
    `Born in Tokyo`, `Design-driven` over `creative agency`, and `Branding,
    digital` over `and communications`.
11. The words are readable before the animated field starts. Where the field
    cannot run, or where reduced motion is requested, the hero renders a still
    frame of the field with the grain and the words in place and the lens becomes
    a static circular crop. No interaction is required for the words to be
    readable.

### The recent-work reel

12. Below the hero, an eyebrow reads `RECENT WORK` and a section pins to the
    screen while its content advances. As the reel's stretch of scroll passes,
    the active project title advances in place, the outgoing one fading and
    rising away, a tick travels down a vertical ruler tracking progress through
    the reel, and the background colour field shifts for each project. Scrolling
    back rewinds it.
13. The reel holds exactly the four projects seeded as home-reel projects, in
    their seeded order, each with its title, its discipline tags and its cover.
    An unpublished project is never one of them.
14. Below the reel a centred pill reads `Discover all projects` with a trailing
    `→` and routes to `/work`.

### The work index

15. The `/work` intro opens on a subtitle reading `We choose a different` `→`
    `starting point` over the paragraph `Every project is a chance to try
    something new. Look at something with a fresh perspective. Do something for
    the first time.`, and a scroll cue below it.
16. The filter bar carries exactly eight controls in this order: `All`,
    `SPATIAL`, `Campaign`, `Photography`, `Brand design`, `Video`, `Digital`,
    `Illustration`. Nothing outside that closed set is a filter. Inactive filters
    rest dimmed; the active one is at full strength.
17. Choosing a filter narrows the grid to the projects carrying that discipline
    with no route change and no page reload, animating the leaving items out and
    the arriving ones in. The active filter is reflected in the URL as a query so
    a filtered view is linkable, and loading that URL directly shows the same
    result. `All` clears the filter and shows every published project.
18. A filter matching no published project shows the index's empty state, never a
    blank page and never an error.
19. The grid is two columns of project cards that drift at reading pace against
    the scroll, each holding a cover, its discipline tags and its title with the
    `‣` marker between the client and the piece. A circular mask expands to
    uncover each cover.
20. Each cover plays its short film only while it is pointed at, or on a touch
    device while it is in view, and pauses otherwise, so a long grid never has
    many films running at once. A single shared play and pause control governs
    all of the site's media.

### The press route

21. The `/press` intro opens on the display title `PRESS & NEWS` over the label
    `CATEGORIES` and the filter set `all`, `Series`, `News`, `Events`,
    `Features`, `Articles`. Each category filter shows its own count beside its
    label, and every count is derived from the stored items on read, never stored
    alongside them. On the seeded collection they read `News [2]`, `Events [2]`,
    `Features [3]` and `Articles [0]`.
22. The feed lists items newest first, each carrying its category, its date
    written `DD.MM.YYYY`, its title with the `‣` marker, and a `Read more` link
    to the item's destination.
23. `Series` shows the featured block: the title `Series`, the tag `Designing for
    the future`, and three volumes, `Vol 01` `Creative is the powerful fuel
    to new energy`, `Vol 02` `Sustainability in Fashion` and `Vol 03`
    `Designing for the future of food`. Its images sit on a stage with
    real depth: the tiles tilt and settle at different distances as the scroll
    passes, a circular mask reveals each one, and each image arrives in two
    stages, a small blurred preview first and the full image once it has decoded,
    marked as loaded when it lands.
24. The press route repeats the contact invitation as three pill links of
    different widths, each sized to its own text and carrying a hairline ring set
    in from its edge. One of them carries the download glyph and downloads the
    press kit.

### The team route

25. The `/team` intro opens on a three-line heading that reveals line by line, reading
    `We seek`, `unique`, `perspectives`, over the footnote `[ a city-based
    global network ]` and the paragraph `We collaborate as a collective of
    individuals bringing their whole self to a project and, together, create work
    that none of us would be able to do on our own.`
26. A four-line banner draws in against the scroll rather than on entry, reading
    `We are a collective`, `for global`, `creative talent`, `seeking
    safe harbour.`, with the baseline note `[ A safe space for independent
    spirits. ]` over the paragraph `Our structure empowers creative minds to
    bring their whole selves to projects. We work in a flat hierarchy that
    encourages people to deepen their expertise and widen their interests.`
27. A heading `→` `Meet our london team` sits over a two-column member grid.
    Each card holds a generated portrait, the member's name and one or two role
    tags. The grid closes with a member count derived from the members shown, so
    on the seeded collection it reads `11 members`.
28. Two dated chapters close the route: `2011` `Founded in Tokyo by Yoshi &
    Shun` and `2019` `London office founded by Rei & Cal`, each with its
    paragraph and its named people.

### The not-found route

29. An unknown address renders the studio's own not-found page and answers not
    found. It carries the heading `Page not found`, the paragraph `Looks like
    you've followed a broken link or entered a URL that doesn't exist on this
    site.`, a second paragraph addressed to the site owner reading `If this is
    your site, and you weren't expecting a 404 for this path, please visit the
    host's` followed by a `"page not found" support guide` link and `for
    troubleshooting tips.`, and a way back into the site. It is a plain, static
    route and sits deliberately outside the site's motion system.

### The enquiry

30. The contact form takes a name, an email address, a message and the surface it
    was opened from, which is either the footer or the press route. A valid
    submission is stored and the form is replaced in place by its success state;
    the idle, submitting, success and error states are all pre-rendered and
    toggled, never inserted into the layout when they are needed.
31. An invalid submission is rejected inline, names the field that is wrong, does
    not reload the page, and writes nothing. An empty name, an empty message, and
    an address that is not an email address are each rejected this way.
32. An enquiry that looks automated is refused and nothing is written. Two things
    make it look automated, and the form applies both. The first is a decoy: the
    form carries a field named `company_website` that is hidden from sight and
    never presented to a person, and a submission arriving with anything in it is
    refused. The second is rate: when the same form is submitted repeatedly in
    quick succession a fourth submission from the same visitor inside `60`
    seconds is refused, so three in quick succession are accepted and the next
    is not. A refused submission leaves no row behind and is reported to the
    sender as a refusal, not as a success.
33. Every stored enquiry is readable at `/studio/enquiries`, newest first, and by
    an `author` alone. A `reader` or an anonymous request for that list is denied.

### The cookie choice

34. A first-time visitor is asked once, on a rail reading `This website uses
    cookies.` with a `Learn more.` link and an `ACCEPT` control. The choice
    survives a reload and every route change, and the visitor is not asked again.
35. No analytics or advertising tag loads until the choice has been accepted, and
    the rail never blocks the hero.
36. Each page view is recorded with its route and the moment it happened, and the
    record is readable by an `author` and by nobody else.

### The studio console

37. `/studio` and every path beneath it require an `author`. An anonymous request
    is sent to `/login` and returns to the requested path after a successful sign
    in; a `reader`'s request is denied outright rather than redirected.
38. Creating a project runs as three steps, each at its own address:
    `/studio/projects/new/details` takes the title, the client and the slug;
    `/studio/projects/new/disciplines` takes the disciplines from the closed set
    of seven; `/studio/projects/new/media` takes the cover and the press kit.
    Leaving a step and returning to it restores what was entered.
39. Finishing the wizard lands on a full-page confirmation at
    `/studio/projects/{project_id}/created` naming the project that was made. The
    new project is a draft.
40. Uploading a cover puts the bytes in the MinIO bucket at
    `projects/{project_id}/{sha256_of_bytes}.{ext}`, for example
    `projects/7/9f2a...d0.webp`. A press kit goes to
    `press-kits/{project_id}/{sha256_of_bytes}.{ext}`, for example
    `press-kits/7/4c81...aa.pdf`, and a team portrait to
    `team/{member_id}/{sha256_of_bytes}.{ext}`, for example
    `team/3/1b60...7e.webp`. Bytes live nowhere else: not on the app's own
    filesystem, not in a database column.
41. Publishing a project from `/studio/projects` makes it visible on the public
    site immediately. Unpublishing it removes it from the index, from every
    filter and from the home reel just as immediately. Publishing an
    already-published project changes nothing and creates no second project.

### The protected boundary

42. A project whose status is draft appears in no public response. It is absent
    from `/work`, absent under every one of the eight filters including `All`,
    absent from the home reel, and a direct request for it at its own public
    address answers not found rather than rendering it.
43. A draft project's cover object is served to an `author` and to nobody else. A
    request for it carrying a `reader`'s token, or no token at all, is denied and
    returns no bytes.
44. A press-kit object is served to a signed-in `reader` or `author`. An
    anonymous request for one is denied and returns no bytes.
45. Every object reaches a browser through the app's own media endpoint, which
    resolves entitlement before it streams anything. The app never makes a bucket
    or an object publicly readable and never hands out a public object URL, so a
    request made directly to the store for any of these keys, without the app in
    the path, returns no bytes.

### Discovery surface

46. `/sitemap.xml` lists every public route: `/`, `/work`, `/press`, `/team`,
    `/services`, `/contact` and `/privacy`. No draft project and no console path
    appears in it.
47. `/robots.txt` is served and points at the sitemap.

## User flow

The information architecture is a small number of long, richly built routes
rather than a deep tree.

| Route | Purpose | Auth |
|---|---|---|
| `/` | hero, recent-work reel, footer | public |
| `/work` | filterable project index, filter carried in the URL | public |
| `/press` | dated feed, category filters, featured series | public |
| `/team` | studio story, member grid, founding history | public |
| `/services` | what the studio does | public |
| `/contact` | the contact form and the studio address | public |
| `/privacy` | what the site stores and for how long | public |
| `/sitemap.xml` | every public route | public |
| `/robots.txt` | points at the sitemap | public |
| `/signup` | open registration, creates a `reader` | public |
| `/login` | sign in | public |
| `/studio` | console home | `author` |
| `/studio/projects` | every project, draft and published | `author` |
| `/studio/projects/new/details` | wizard step one | `author` |
| `/studio/projects/new/disciplines` | wizard step two | `author` |
| `/studio/projects/new/media` | wizard step three | `author` |
| `/studio/projects/{project_id}/created` | full-page confirmation | `author` |
| `/studio/enquiries` | every enquiry, newest first | `author` |
| anything else | the studio's own not-found page | public |

**Entry and redirects.** An anonymous request to `/studio` or any path beneath it
goes to `/login`, and a successful sign-in lands on the path that was originally
asked for. A `reader` signing in and then requesting a console path is denied, not
redirected into the console. Signing out returns to `/` and the session no longer
opens the console. A token that expires mid-action leaves the action unwritten and
returns the visitor to `/login`. An unknown path renders the not-found route.

**Journeys.**

1. *The argument.* Open `/`. The three hero lines are readable before the field
   animates. Scroll: the reel pins, and `HANWA RUNNER ‣ HARBOUR CAFE - POP-UP`,
   `NKALA COFFEE ‣ BRAND IDENTITY`, `FELDGREN x MEADOW & MOSS ‣ WINTER
   ACTIVATION` and `SEABRIGHT ‣ KOREAN FRIED CHICKEN ‣ BRANDING`
   advance one at a time while the ruler tick tracks progress. Press `Discover all
   projects` and land on `/work`.
2. *Filtering.* On `/work`, choose `SPATIAL`: the grid narrows without reloading
   and the URL carries the filter. Reload that URL: the same set. Choose
   `Illustration`: one project, `QUEST PORTAL ‣ BRAND UNIVERSE`. Choose `All`:
   eight projects, and `AMBERLINE ‣ STUDIO REBRAND` is not among them.
3. *The enquiry.* From any content route's footer, open the contact form and
   submit with the email left empty. The field is named, the page does not reload,
   nothing is stored. Correct it and submit: the success state replaces the form.
4. *Press.* Open `/press`. The category counts read `News [2]`, `Events [2]`,
   `Features [3]`, `Articles [0]`. Choose `Articles`: the empty state. Choose
   `Series`: the three volumes tilt and settle in depth as the scroll passes.
5. *The press kit.* Anonymously, ask for the press kit of `NKALA COFFEE ‣ BRAND
   IDENTITY`: denied, no bytes. Sign up at `/signup`, sign in, ask again: the
   bytes arrive.
6. *The editor.* Sign in as `author@example.com`. Walk the three wizard steps,
   upload a cover, finish on the confirmation page. The new project is a draft: it
   is absent from `/work` under every filter, absent from the reel, and its cover
   bytes are refused to a signed-out requester. Publish it from
   `/studio/projects`: it appears on the index at once.

**States.** Each wizard step makes clear which of the three steps is open and
which remain, so the editor can see the position in the sequence at a glance.
Every list has an empty state: the work grid under a filter that
matches nothing, the press feed under `Articles`, the console's enquiry list
before the first enquiry, the console's project list before the first project.
Every route has a loading state that reserves its layout rather than collapsing
it, so nothing jumps when content lands. An error never takes the app down: the
route still renders, the region that failed says what failed, and the header and
footer stay usable.

## UI/UX notes

In the first moment a visitor should feel that this studio can make something
alive, before reading a word of proof. The register is editorial and cinematic
rather than operational: the work is seen first and atmosphere is the argument.
The console behind the sign-in is deliberately the opposite, plain and quiet,
because nothing about an editor's afternoon is improved by drama.

**Colour, by role.** The paper ground of the work and team routes is a near-white
neutral and it dominates the site by an order of magnitude. Body ink on that
ground is a deep cool neutral and it is the only colour body text takes there. The
home and press routes invert to a near-black cool neutral ground, where the colour
field and the project films do the talking. Hairlines and light fills are a
near-white neutral; secondary text is a mid cool neutral and is reserved for
larger sizes; the workhorse grey beside it is a mid neutral. The primary control's
hover ink is a near-black neutral. Exactly one colour has a job, a deep, soft teal, and it points at things that can be acted on; a light, muted green may
appear beside it but never instead of it. A scrim over media is a near-black
neutral at half strength. The shader surface clears to a near-black neutral, and
one channel of the lens pass is sampled at a wider offset than the others, which
is what produces the mid, vivid red fringe at the rim. The browser's own unstyled
mid, vivid blue link shows through only on the not-found route's support link and
must never be adopted as a brand colour. Keep that weighting: the accent must stay
rare or the page stops reading as restrained, and it never appears on body-size
text on the paper ground. The exact shades are yours, so long as those
relationships hold.

**Meaning-carrying colour.** Three states need a colour that means something and
means only that. Failure, which is what a rejected form field and a refused
download wear, is a colour that appears nowhere except when something has gone
wrong. Success, which is what the enquiry's confirmation wears, is a distinct
colour that never doubles as the action accent. In-progress, which is what the
submitting state and the second stage of an image wear, is a third and quieter
one. None of the three may be the teal: the accent means "you can act on this",
and a colour that also means "this failed" means neither. Each is paired with a
word or a mark, because meaning is never carried by colour alone.

**Mode.** The site commits to one designed scheme and builds it fully: the paper
ground on the work and team routes, the near-black ground on the home and press
routes, both belonging to the same light-mode design. There is no second theme,
no toggle and no separate dark mode; the near-black routes are a designed
register, not an inversion of the paper ones.

**What it must not look like.** Not a page dominated by a single hue family with
no second signal. Not a marketing composition where the working index belongs. Not
an accent used decoratively, which is the one failure that would undo the
restraint the whole palette is built on.

**Type.** The typography is one neutral grotesque, `Inter`, doing everything from
micro-label to display line, at weights 400, 600, 700 and 800, with a system
fallback stack declared so text is never invisible while the family loads. `Noto
Sans JP` carries the Japanese glyphs set beneath the lens. Body and interface text
is `16px` at weight 400 over `18.4px`; eyebrows and small bold labels are `12px`
at weight 800 over `14.76px`; the display line is `45px` at weight 400 over
`48.915px`. The full ramp is in the front-end specification, and it is one fluid
ramp sampled at three widths rather than a set of fixed steps, so the fractional
line heights follow from the ramp rather than being hand-set. Figures align
wherever amounts or counts stack.

**The swash device.** Inside otherwise upright words a single letter, almost
always an `i` or an `o`, is set in the same family's own italic and leans, so a
headline reads with one leaning letter mid-word. It is an inline `<i>` element
around that one glyph, never a font change on the whole word, and it is content
rather than decoration: it stays in reading order, it survives selection, and a
screen reader says `creativity` as one word rather than spelling it in pieces.
Every title and heading in this brief is written in its plain reading form; the
stored value carries the marker, so `NKALA COFFEE ‣ BRAND IDENTITY` is stored as
`NKALA C<i>O</i>FFEE ‣ BRAND <i>I</i>DENT<i>I</i>TY` and renders with those three
letters leaning. The letters that lean are the `o` and `i` vowels, chosen per
title, and they are part of the stored copy rather than something the page
computes.

**Shape and density.** Radii come in four registers and no more: fully circular
for the burger, the cursor's info disc and the link icon discs; a gently rounded
standard card; a full pill for the primary call to action and the cookie accept; a
softer pill for the press-series tag; and the three press contact links, each
sized to its own text with a hairline ring set in from its edge. There is one
resting shadow, soft and low in the ink's own colour, and it appears on the card
and nowhere else. Density is spacious on the public routes: the display line is
given room and a project is allowed a whole frame. Layering is three stacking bands and no intermediate values: in-flow raised content, the fixed chrome, and
the top-most overlays, which are the transition veil and the cookie rail.

**Motion.** Motion is this studio's primary tool and the character is eased:
things arrive by rising a short way while they fade in, quickly at first and then
settling long, and the same hand is visible everywhere so the whole site reads as
one piece. Six easing curves carry all of it and a seventh is never introduced: a
house curve that leaves fast and settles long, carrying nearly every transform and
fade; a symmetric ease-in-out for balanced moves; a strong in-out for the veil and
for visibility swaps; a gentle out for soft settles; a strong ease-in for exits
that accelerate away; and an ease-in for quick departures. The named moments, each
of which must exist: the house reveal, where title lines rise and fade into place
staggered one after another; the exit, where a leaving element accelerates away
harder than it arrived; the delayed entrance, where the hero words hold for a beat
and then scale in slowly so the field is established first; the wipe, where a
clipped edge sweeps across to uncover content; the link underline settle, the
smallest and quickest hover on the site; the primary button hover, where the
pill's arrow and both of its duplicate glyph layers move together from light to
near-black ink in one motion, which is the move that makes the control read as
crafted rather than ordinary; the icon settle, a fractional nudge on the press
route's tertiary icon; the route veil, which covers the screen with the wordmark
during a navigation and releases the chrome on ready; the burger, whose two bars
invert against whatever sits behind them and which scales slightly on press; and
the overlay, which enters from the top-right corner rather than fading in place.
Durations and curve values are yours; the character and the uniformity are not.

**Reduced motion preserves, it never strips.** When a visitor asks for reduced
motion the hero holds a still frame with no lens travel and no field drift, every
reveal resolves to its end state at once, the reel's scrub is released so the
projects read as a plain list, the parallax and the collage tilt stop, and the
route veil cross-fades without travel. The fade is kept where the movement is
removed, and every word, link and control keeps working.

**Scrolling.** Scrolling is smoothed, so wheel and touch drive an eased
interpolated position rather than the native step, and every scroll-linked effect
reads that one position so nothing drifts out of step with anything else. The
footer parallaxes into view on every content route, rising at its own rate as the
last screen closes.

**Responsive.** Three breakpoint widths are designed rather than derived, and
type and spacing are expressed in a scaling unit against the root size rather than
in fixed steps: a phone single column, a distinct tablet column model that is not
a squeezed desktop, and the dominant desktop layout. The work and team grids run
two columns at the wider two
and one on the phone; the home reel stays full-bleed at every width and keeps its
side ruler on the tablet; the press collage keeps its sense of depth because the
perspective is dialled to the viewport width rather than left fixed, so it does
not flatten on a small screen. The primary links collapse behind the burger at
narrow widths while the clock strip is retained, and the eight work filters swap
from an inline button list to a native select control, both driving the same
filter state. Full-height sections are sized to the currently visible viewport
height rather than a fixed tallest height, so a phone browser's chrome collapsing
does not jump the layout. Because sections stack, the phone's scroll runs much
longer, and the pinned reel and every parallax range are computed from live
section heights rather than fixed constants so they hold at every width. At the
narrow viewport nothing overflows sideways and every navigation target stays
reachable.

**Accessibility.** Text meets the WCAG AA contrast bar against its own ground, in
both the paper and near-black registers, and the subdued grey stays on larger
secondary text where it clears the bar. Every interactive element is reachable and
operable by keyboard navigation in a logical order with a visible focus ring:
header links, the burger and its overlay, the work filters, the press filters, the
read-more links, the contact links, the media toggle and the cookie rail. The
overlay traps focus while it is open and restores focus to the control that opened
it on close. The custom cursor is decorative and never the only carrier of
anything: hiding the system pointer must not remove a hover or focus affordance,
and every interactive element keeps its own visible state. Touch targets are
comfortably sized, icon-only controls carry labels, and meaning is never carried
by colour alone. The clocks update politely so they never interrupt, and the
filtered result count on the work and press routes is announced so a non-visual
visitor learns that the grid changed. Every content image carries alternative text
and every decorative one declares itself decorative.

## Technical requirements

Build the app as a server-rendered multi-page application. The backend is
**Django** serving HTML from server-side templates for every route, and the
front-end layer is **HTMX** driving in-page exchanges against those same
server-rendered fragments: the work filter, the press filter, the enquiry form and
the console wizard each replace a fragment and push the new address, so the
browser receives finished HTML on first paint for every route and a cold load of
any deep path renders that route directly without waiting for a client-side
router.

The datastore is **PostgreSQL**, read from `DATABASE_URL`. Object storage is
**MinIO**, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`
and `STORAGE_SECRET_KEY`. The app's own address and port come from
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port; read
every one of them from the environment. Both backing services are already running
and reachable at those variables, and must not be downloaded, installed, compiled
or started by the app.

Auth is email and password implemented by the app, with bearer tokens on the
requests that follow a sign-in and passwords stored hashed. `GET /api/health`
returns `200` once the app is ready. Requests log to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, cache, queue, object store, identity provider or mail vendor -
the only backing services available in this environment are PostgreSQL and MinIO,
and reaching for anything else is a contract violation.

No credential, API key or admin token may appear in anything the browser
downloads: not in a served document, not in a script, not in a style sheet, not in
a response body. The storage keys in particular stay on the server.

Every public route carries its own title and description, and no two public routes
share either. `/sitemap.xml` lists every public route and `/robots.txt` points at
it; neither names a draft project or a console path.

No third-party analytics measurement identifier is configured and no advertising
tag is loaded from anywhere; the page-view record the studio reads is the app's
own. The social links point at the studio's Instagram and Linkedin profiles.

The build is zero-asset: it ships no binary. No image file, no video file, no font
file, no displacement map, no texture. Every asset class the design calls for has
a generated substitution instead, and each substitution is listed here. The hero
grain is generated as fine monochrome noise
sampled per pixel and overlaid at low strength, refreshed slowly so it shimmers
rather than sits dead. The lens is driven by three generated fields: a radial
height field that is flat at the centre and steepens toward the rim, so content
magnifies at the middle and compresses at the edge; a soft-edged circular mask
that confines the effect to the disc; and a smooth low-frequency field that
wobbles the lens edge so it is never a perfect circle. The drifting colour field
is a small set of warm and cool stops, with an olive variant for the reel frames,
carried across a slowly evolving flow so it folds and stirs without ever repeating
on a visible loop. Each project cover is a seeded generated loop keyed to the
project's discipline, so a spatial cover reads differently from a brand-design
one, drawn in the site's own neutral palette, and it keeps a poster frame and a
play state so the shared media control and the in-view play behaviour work on it
unchanged. Every cover and portrait loads as a two-stage progressive image: the first
stage is a generated blurred gradient placeholder keyed by a per-image seed,
standing in for a shipped thumbnail, and the full stage it swaps to is the
generated cover. Each team portrait is a seeded
colour abstract placeholder in the card's ratio, shaped so a real photograph can
drop straight into its place later. Both type families are openly licensed and
installed by the build, with a normative fallback stack and reserved metrics so
the italic swap does not reflow a line.

Performance is a requirement on the running product. The hero holds a smooth frame
rate on a three-year-old laptop: it renders at a capped device pixel ratio, it
pauses its loop when it is scrolled out of view or the tab is hidden, and it never
blocks first paint, so the words and a still field are readable before the
animated field starts. Cover films decode only while pointed at or in view and
off-screen media is released, so no more than the visible reel frame and at most
one pointed-at grid film are running at once. Images arrive in two stages, a tiny
preview first and the full asset after it decodes, and the layout never reflows
when the full asset lands.

## Data model

Nine tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account so
a grader can sign in.

**users** - `id`, `email` (unique), `password_hash`, `role` (one of `author`,
`reader`), `created_at`.

**projects** - `id`, `title` (carries the swash markup), `client`, `slug`
(unique, kebab-case), `status` (one of `draft`, `published`), `featured_home`,
`position`, `cover_key`, `cover_poster_key`, `press_kit_key`, `created_at`. The
disciplines a project carries are rows in **project_disciplines**
(`project_id`, `discipline`), and `discipline` is one of the seven real filters:
`SPATIAL`, `Campaign`, `Photography`, `Brand design`, `Video`, `Digital`,
`Illustration`. `All` is the reset, never a stored value.

**press_items** - `id`, `category` (one of `News`, `Events`, `Features`,
`Articles`), `published_on`, `title` (swash markup), `href`, `created_at`. The
count beside each category filter is computed on read from these rows and is not
stored anywhere.

**series** - `id`, `index_label`, `title`, `tag`, `position`, with its tiles in
**series_images** (`series_id`, `object_key`, `position`).

**team_members** - `id`, `name` (swash markup), `portrait_key`, `position`, with
role tags in **team_member_roles** (`member_id`, `role_label`). The member count
the grid shows is computed on read from these rows and is not stored.

**studio_chapters** - `id`, `year`, `title` (swash markup), `body`, `people`.

**enquiries** - `id`, `name`, `email`, `message`, `source` (one of `footer`,
`press`), `created_at`.

**consents** - `id`, `visitor_token`, `accepted`, `accepted_at`.

**page_views** - `id`, `route`, `viewed_at`.

**Invariants, as properties of the running app.**

- A project whose `status` is `draft` appears in no public response: not in the
  index, not under any discipline filter, not in the home reel, not at its own
  public address.
- Object bytes reach a browser only through the app's own media endpoint. No
  bucket and no object is made publicly readable, and no public object address is
  ever handed out, so a request made straight to the store for a key returns
  nothing.
- A draft project's cover object is returned to an `author` and to no one else. A
  press-kit object is returned to a signed-in account and to no one else.
- Every uploaded object lands at its scheme's key in the bucket. Bytes never live
  on the app's own filesystem and never inside a database column.
- An enquiry row exists only when every field passed validation and the
  submission was not refused as automated. A rejected submission leaves nothing
  behind.
- Publishing a project that is already published changes nothing and creates no
  second project.

**Seed data.** Two accounts: `author@example.com` as `author` and
`reader@example.com` as `reader`.

Eight published projects and one draft. In home-reel order, the four carrying
`featured_home`: `HANWA RUNNER ‣ HARBOUR CAFE - POP-UP` for client `HANWA
RUNNER`, discipline `SPATIAL`; `NKALA COFFEE ‣ BRAND IDENTITY` for client
`NKALA COFFEE`, disciplines `Brand design`, `SPATIAL`, `Video`, `Photography`;
`FELDGREN x MEADOW & MOSS ‣ WINTER ACTIVATION` for client `FELDGREN`,
disciplines `SPATIAL`, `Campaign`; `SEABRIGHT ‣ KOREAN FRIED CHICKEN ‣
BRANDING` for client `SEABRIGHT`, discipline `Brand design`. Then the four
published projects that are not in the reel: `RONIX ASTROX 88 ‣ Launch Campaign` for client `RONIX`, disciplines `Brand design`, `Digital`;
`PARIS WORLD CHAMPIONSHIPS ‣ RONIX PLAYERS LOUNGE` for client `RONIX`,
disciplines `Campaign`, `Video`; `HANWA RUNNER ‣ FINISH LINE CAFE - POP-UP` for client `HANWA RUNNER`, disciplines `SPATIAL`, `Photography`;
`QUEST PORTAL ‣ BRAND UNIVERSE` for client `QUEST PORTAL`, disciplines `Brand
design`, `Campaign`, `Illustration`. And one draft, never published:
`AMBERLINE ‣ STUDIO REBRAND` for client `AMBERLINE`, disciplines `Digital`,
`Illustration`.

Seven press items, newest first: `Features` `26.11.2025` `FEATURED ON DESIGN WEEK ‣ NKALA COFFEE`; `Features` `27.10.2025` `FEATURED ON THE BRAND IDENTITY ‣
NKALA COFFEE`; `News` `03.09.2025` `NEW KANSO MERCH ‣ LE CABARET`; `News`
`07.08.2025` `NEW KANSO MEMBER ‣ IBU HYUGA, ACCOUNT MANAGER & PRODUCER`; `Events`
`10.07.2025` `KANSO LONDON VISITS ‣ US BY NIGHT`; `Events` `30.05.2025` `KANSO
NIGHT VOL.11 ‣ 'BEACH PLEASE'`; `Features` `27.11.2024` `FEATURED ON CREATIVE
REVIEW ‣ SEABRIGHT BRAND IDENTITY`.

Three series volumes under the tag `Designing for the future`: `Vol 01`
`Creative is the powerful fuel to new energy`; `Vol 02`
`Sustainability in Fashion`; `Vol 03` `Designing for the future of
food`.

Eleven team members, in grid order, with their role tags: `Melina Hubert-Croft`,
Creative director; `Marnix Develt`, Managing director and Strategic planning
director; `Stella Grotti`, Art Director and Designer; `Maud Deleau`, Sr Creative
Producer; `Luna Gooriah`, Art Director and Creative; `Karim Kadi`, Art
Director and Designer; `Keeo Lu`, Graphic Designer and 3D/Motion Designer;
`Sam Beaton`, Graphic Designer; `Josh Gan`, Creative Producer; `Kai Sato
Laughlin`, Account Manager and Producer; `Ibu Hyuga`, Assistant Producer.

Two studio chapters. `2011`, titled `Founded in Tokyo by Yoshi & Shun`,
people Yoshi Arakawa and Shun Meguro, body: `Kanso was founded in Tokyo in 2011 as
a digital design agency. Yoshi and Shun, both bass players, felt that the digital
space was losing its groove. It was creating characterless brands. Anonymous
businesses. A sea of sameness. Together with a collective of artists and
engineers, they set up Kanso to bring personality back to brands.` And `2019`,
titled `London office founded by Rei & Cal`, people Rei Nakamura and Cal
Brennan, body: `The London office was founded in 2019 by Rei and Cal. Their
combined backgrounds in digital design and advertising strategy allowed Kanso
London to attract a diverse range of projects from the start. Both have spent
several years living and working in Tokyo as well as London and are always looking
to create a bridge between the two cities.`

No enquiries, no consent record and no page view exist before the site is first
opened.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual detail the design register needs and states no
rule that is not already stated above.

**The token layer.** Expose the palette as custom properties on the document root
and build every surface against the semantic name rather than against a literal.
Each one holds a space-separated channel triple, so a property can be consumed at
an arbitrary alpha as `rgb(<triple> / <alpha>)`, and none of them is ever declared
as a hex value. The names, and the role each one fills:
`--color-paper`, the bright page ground of the work and team routes; `--colorText`,
the body ink, consumed as an opaque triple; `--colorGrayDarkest`, the darkest
neutral, sharing the ink's channels; `--colorRgbFacetsNeutralLight700`, the ink's
alias in the facet scale; `--colorRgbFacetsNeutralDark900`, the deepest near-black
and the ground of the home and press routes; `--colorGrayLighter`, hairlines and
light fills; `--colorHr`, the horizontal-rule colour, sharing those channels;
`--colorRgbFacetsNeutralLight200`, the light alias in the facet scale;
`--colorTealAction`, the one accent; and `--colorRgbFacetsTeal600`, the teal's
alias in the facet scale. The subdued secondary grey, the mid workhorse grey, the
hover ink and the media scrim are computed rather than tokenised.

**The type ramp.** One fluid ramp, sampled at the three designed widths, resolving
to these rendered points. Body and interface `16px` / 400 / `18.4px`. Small bold
labels and eyebrows `12px` / 800 / `14.76px`; the medium label `12px` / 600 /
`14.76px`; the bold micro-label `12px` / 700 / `14.76px`; the plain micro-label
`12px` / 400 / `14.76px`. The mid strong label `13.52px` / 800 / `16.6296px`.
Secondary body `14px` / 400 / `20.125px` and its fluid sibling `14.56px` / 400 /
`20.93px`. The subheading trio `26.25px` / `29.2425px`, `23.92px` / `26.6469px`
and `23px` / `25.622px`, all at 400. The heading trio `26px` / `28.262px`,
`30.9375px` / `33.6291px` and `24px` / `28.8px`, all at 400. The large heading
`33.75px` / `40.5px` with siblings `24.96px` / `29.952px`. The display line `45px`
/ 400 / `48.915px`. The near-identical siblings at one use count are the same
ramp at another width, not separate steps: build the ramp and the fractional line
heights follow.

**Iconography.** Every mark is drawn by the app, never loaded. The wordmark is
a three-part path set on a wide flat canvas reading `Kanso` `|` `London`, whose
third part is the thin tall divider bar between the studio name and the city; it
appears identically in the header and inside the route-transition veil. The cursor
arrow is a long vertical shaft with a chevron head at its foot, sitting inside the
cursor's info circle as a scroll-down cue. The download arrow is a downward arrow
above a tray line and sits on the press route's contact pill. The circle-arrow
mark is an open stroked ring with a small arrowhead breaking its top edge, and it
means open or explore. All four are stroked or filled shapes with no fill beyond
their own ink.

**Marks that stay typed characters.** The right arrow `→` on primary buttons and
press links, the up-right arrow `↗` on tertiary and social links, the up arrow `↑`
on the footer's top control, and the triangular marker `‣` between a client and
the piece inside a project title are set as text characters so they inherit the
type ramp. They are not redrawn as vectors.

**The hero composition.** The field sits behind everything, the grain sits over
the field, the lens sits over the centre of both, and the word layer is composited
on top as real text rather than drawn into the surface. The foot row animates in
underneath. The lens reveals the Japanese setting of the word "creativity"
beneath the headline.

**The reel.** A pinned frame holds a full-bleed cover, a large project title with
its swash letters, one or two discipline tags, and a vertical ruler at the side
carrying a tick that tracks progress. The call to action below it rests slightly
left of centre and reads `Discover all projects`.

**The press collage.** Three volumes on a stage with real depth; the tiles carry
their own depth so they tilt rather than skew, and the stage's perspective is set
per width so the depth reads correctly on a phone instead of collapsing.

**The cookie rail.** It sits at the foot of the viewport on load, in the top
overlay band, and its accept control is the outline variant of the pill.

**The not-found route.** Plain and still: heading, paragraph, owner-facing line
with its support-guide link, and a way back. No reveal, no parallax, no veil
theatre.

## Constraints

- Single studio, single tenant. There is no organisation, no workspace and no
  second studio.
- No customer account, no cart, no payment, no invoice, no subscription, no
  refund.
- No comments, no likes, no sharing, no follows, no newsletter and no search.
- No realtime channel. Nothing on the page updates without a request.
- No email is sent by the app. An enquiry is stored and read in the console.
- No external network call at run time. Analytics is a record the app keeps
  itself, readable by the studio, and no third-party tag loads before the cookie
  choice is accepted.
- No native app, no offline mode and no background sync.
- No binary asset ships with the build: no image, no video, no font file, no map.
- No second datastore and no second object store.
- The site must stay responsive with tens of projects, a few hundred press items,
  a few dozen team members and a few thousand stored enquiries.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev server.
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

**API shapes.**

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `{ email, password }` | the created `reader` |
| `POST /api/auth/login` | `{ email, password }` | `{ access_token, role }` |
| `GET /api/projects` | `?discipline=<one of the seven>` | a top-level JSON array of published projects, each with `id`, `title`, `client`, `slug`, `disciplines`, `cover_key`, `featured_home`, `position` |
| `GET /api/projects/{slug}` | - | the published project, or not found when it is a draft |
| `GET /api/press` | `?category=<one of the four>` | a top-level JSON array of press items, newest first |
| `GET /api/press/categories` | - | a top-level JSON array of `{ category, count }`, counts computed on read |
| `GET /api/series` | - | a top-level JSON array of volumes with their tiles |
| `GET /api/team` | - | a top-level JSON array of members with their role tags, and the derived count |
| `GET /api/chapters` | - | a top-level JSON array of studio chapters |
| `POST /api/enquiries` | `{ name, email, message, source }` where `source` is `footer` or `press` | the stored enquiry |
| `GET /api/enquiries` | - | a top-level JSON array of enquiries, newest first, `author` only |
| `POST /api/projects` | `{ title, client, slug, disciplines }` | the created draft project, `author` only |
| `POST /api/projects/{project_id}/media` | the cover or press-kit bytes | the stored object key, `author` only |
| `POST /api/projects/{project_id}/publish` | - | the published project, `author` only |
| `POST /api/projects/{project_id}/unpublish` | - | the draft project, `author` only |
| `GET /api/media/{object_key}` | - | the object bytes when the requester is entitled to them |
| `POST /api/consent` | `{ accepted }` | the recorded choice |
| `GET /api/page-views` | - | a top-level JSON array of route and timestamp records, `author` only |

Bearer auth on everything except signup, login, health and the public read
endpoints. A successful call returns the named resource or shape; an invalid or
unauthorized call is rejected as a client error, never as a server error and never
as a silent success.

**No mocks.** The uploaded bytes must be in the MinIO bucket at their scheme's
key. An in-memory dictionary of objects, a hardcoded response the app returns to
itself, image bytes written to the app container's filesystem, a base64 column in
PostgreSQL, or a directory of files beside the source are each a contract
violation however convincing the page looks. The named provider is the fact - the
app's UI and its own tables can only reflect what lives in the provider, never
substitute for it.

## Definition of done

A visitor can scroll the reel project by project, narrow the work to one
discipline, share that filtered address, and send an enquiry the studio editor
later reads. Ask for reduced motion and the same site holds still, every word and
link intact. The unpublished project is nowhere on the public site and its cover
bytes reach nobody but the editor. Nothing ships with the build but code.
