# Kaiyo Interactive Studio Site

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser and travel from the home route through a project case and an editorial
post into the enquiry form, submit it, and land on a confirmation that names
what they sent, without hitting an error page. A different stranger, signed in
as a reader or signed in as nobody at all, must NOT be able to read a project or
a topic that is still a draft, or fetch its hero image, by any means. The draft
rule is a fact about the store, not about the page: the hero bytes of an
unpublished record must not be retrievable from the object store by an
unentitled request, and a page that merely declines to render a link does not
satisfy it.

## Overview

Kaiyo Interactive is a fifteen-person creative studio in Yokohama working across
four named disciplines: digital, film, spatial and branding. This is its site.
It sells nothing. It states what the studio is, sets out the four disciplines,
shows client work as cases with an index and a full write-up each, introduces
every member of the team by face and job title, publishes an editorial strand of
interviews and announcements, prints the company registration facts, and takes a
detailed project enquiry through one long form.

Four audiences arrive with four different questions and the site answers each in
a different place. Marketing and brand leads ask whether this studio can make
the thing they need, and the service route answers them. Prospective clients
comparing studios ask what it has actually shipped, and the project index and a
case write-up answer them. Candidates ask who works here and what it is like,
and the team route and the editorial strand answer them. Press and procurement
ask for the registration facts and the address, and the company route answers
them. Every one of those answers ends at the same enquiry form.

The site exists in two language editions, Japanese and English, at separate
paths. The Japanese edition is not monolingual: its display headings are already
English, and only the body copy changes between editions.

Behind every route, at every scroll position, floats one living object: a
full-viewport canvas holding a small number of soft spheres that merge into a
single continuous mass, tinted by a gradient and drifting continuously. A panel
in the left margin hands the visitor nine of that simulation's parameters. That
object and that panel are the product. A studio site without them is an ordinary
agency template, and this one is not.

What this deliberately is not: there is no shop, no cart, no pricing, no
comments, no likes, no ratings, no search, no newsletter, no chat widget, no
social feed embedded from anywhere, and no account for a visitor who only wants
to read. The only visitor action that touches persisted state anywhere on the
site is submitting the enquiry form.

The genuinely hard part is that the simulation is continuous and the site is
not: the mass must keep running, at its current settings, across a route change,
while the document under it is replaced.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor, not signed in | Read every published project, topic, member and company fact in either edition; retune the simulation from the settings panel; submit the enquiry form; answer the cookie choice | **Cannot read a draft project or a draft topic, or fetch its hero image.** **Cannot create, edit, publish or delete any record.** **Cannot read a stored enquiry.** |
| `reader` | Everything a visitor can do, signed in, and see their own account | **Cannot read a draft project or a draft topic, or fetch its hero image.** **Cannot create, edit, publish or delete any record.** **Cannot read a stored enquiry.** |
| `editor` | Everything above, plus create, edit, publish and unpublish projects, topics and members; upload a hero still or a portrait; read every stored enquiry | **Cannot delete a stored enquiry.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a `reader` session
to any `editor`-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

Signup is open. Anyone may create a `reader` account; nobody may create an
`editor` account through signup, and a signup request that asks for one is
accepted as a `reader` or rejected, never honoured. The draft rule binds the
same way for a signed-in `reader` as for a visitor who never signed in, so
signing up buys no reading privilege at all.

Two accounts are seeded:

| Email | Role |
|---|---|
| `editor@example.com` | `editor` |
| `reader@example.com` | `reader` |

## Core features

### The persistent simulation

1. One canvas sits behind all document content on every route, sized to the
   viewport, and renders a small number of soft-bodied spheres whose surfaces
   merge into a single continuous mass as they approach rather than
   intersecting as hard shapes. Where two lobes meet there is a neck, never a
   crease and never a visible intersection, and the silhouette is lobed and
   irregular rather than a circle or an ellipse.
2. The mass is shaded by at least one movable light with separately
   controllable intensity and diffuse falloff, and tinted by a gradient
   interpolating between two colours over a settable ground colour. All three
   colours are settable while the page is open.
3. The simulation runs continuously and does not restart on a route change.
   Moving from the home route to any other route and back leaves the mass in a
   different position from where it was, because it never stopped.
4. Every parameter change takes effect within one frame, with no flash, no
   reinitialisation and no restart of the scene.
5. The simulation pauses entirely while the document is hidden, and resumes
   where it left off when the document is shown again.
6. When sustained frame times exceed the budget the simulation degrades rather
   than stalling: it reduces its resolution scale first, then its sphere count,
   and only as a last resort falls back to a still gradient in the same two
   colours. It renders at the device pixel ratio capped at two, because a
   soft-bodied mass gains nothing visible above that and costs three times the
   fragment work.

### The settings panel

1. A control in the left margin opens a translucent panel, present on every
   route, carrying nine labelled controls in three groups: three colour wells
   labelled `Background`, `Sphere colour one` and `Sphere colour two`; four
   ranges labelled `Angular damping`, `Linear damping`, `Return force` and
   `Movement range`; and two ranges labelled `Strength` and `Diffuse` under a
   `Light` separator. A `Metaball` separator divides the colour group from the
   physics group.
2. Dragging any range changes the mass within one frame. Changing any colour
   well changes the mass, and the change survives a route change.
3. Reloading the page restores every default. Nothing about the simulation is
   persisted, sent anywhere, or remembered between visits.
4. The panel is a dialog. Opening it moves focus into it, `Escape` closes it,
   focus returns to the control that opened it, and focus is trapped while it is
   open. Each colour well is a labelled colour input whose label is
   programmatically associated with it, not merely adjacent. Each range is a
   labelled slider with a stated minimum, maximum and current value, operable by
   arrow key. The opening control exposes its own state and its accessible name
   changes with it.
5. The panel's control list scrolls, and it dissolves into the panel's own
   ground at the top and bottom edges rather than being cut off by them.

### Projects

1. A project carries a title, a one-line subtitle, a free-text year label, one
   or more discipline tags drawn from `digital`, `movie`, `spatial` and `brand`,
   a client name, an optional outbound link, a hero still, an introduction, an
   ordered gallery and an ordered credit list.
2. The project index lists every published project newest first, as a card grid
   of case rows beside one large still pinned alongside them. The still
   cross-fades between cases on a slow loop while no row is pointed at, swaps to
   a row's own hero within one frame when that row is pointed at, and returns to
   its idle cycle where it left off when the pointer leaves, never restarting
   from the first frame.
3. The index does not filter. The discipline tags on a row are labels, not
   controls.
4. A project detail route is addressed by an opaque numeric id, never by a slug.
5. A project whose status is `draft` is absent from the index, and a request for
   its detail route by a visitor or by a `reader` is denied. A request for its
   hero image is denied by the same rule. Publishing it makes both readable;
   unpublishing it makes both denied again.
6. `year_label` is free text and is not a date. `2025-26` is a legal value and
   must not be tidied into a number.
7. A project detail route carries the case title, the label `Client` followed by
   the client name, an outbound `Visit site` link when the case has one, an
   introduction, the gallery, the credits, and a two-way pagination block
   offering the previous and next case and a return to the index.

### Topics

1. A topic carries a title, exactly one category from `blog`, `member`,
   `interview`, `news` and `recruit`, a publication date, a hero still and a
   long-form body that supports a chapter heading, an interviewer question, a
   named answer, a paragraph and a full-width image.
2. The topic index lists every published topic newest first as a card grid of
   three across, each card a still above a title above its category and its
   date.
3. A category rail beside the grid carries `All`, `Blog`, `Member`, `Interview`,
   `News` and `Recruit` in that order, with `All` selected by default.
   Selecting one filters the grid.
4. The filter is reflected in the address so a filtered view is linkable, and it
   does not reload the page. Cards entering the filtered set play their arrival
   rather than appearing already revealed.
5. Dates render unpadded on both month and day: `2026.3.18`, never
   `2026.03.18`.
6. A topic whose status is `draft` is absent from the index and from every
   filtered view, and a request for its detail route or its hero image by a
   visitor or by a `reader` is denied.
7. An interviewer question in a topic body is marked with a plain hyphen and a
   space, never with a typographic dash, and an answer is marked with the
   speaker's family name and a colon.

### Team and company

1. The team route is a card grid of member cards, each carrying a portrait, an
   English job title, a location, a name and two or three interests each
   prefixed with a hash. Cards fade in; they do not stagger upward.
2. The company route carries a two-entry rail reading `Profile` and `Access`, a
   definition table of the registration facts separated by hairline rules, and
   an access block giving the address and how to reach it.
3. The access map is drawn by the app, not loaded as a picture and not embedded
   from a third party that fetches a bundle when the page loads.

### The four disciplines

1. The service route names four disciplines and their sub-services, identical in
   both editions: `Digital` covering `UI/UX Design`, `Web App`, `Digital Craft`,
   `3DCG` and `Motion Graphic`; `Movie` covering `MV`, `Promotion/CM`,
   `Brand Movie`, `Video/Photograph` and `Drone`; `Spatial` covering
   `Spatial Design`, `VR/AR`, `Installation`, `Contents Design` and
   `Experience Design`; and `Brand` covering `Inner Branding`,
   `Recruit Strategy` and `Brand Communication`.
2. Each discipline block carries its name, a paragraph about it, a
   `Related Projects` link into the index, and a large circular figure holding
   moving footage.
3. The word `Spatial` is spelled the same way in the route's own rail and in the
   discipline heading below it.

### The enquiry form

1. The enquiry route carries one long form of eleven controls in this order:
   enquiry type as a required radio pair of `enquiry` and `materials_request`;
   required name; required company; required job title; required email; optional
   address; an optional multiple-choice group of nine interests; a required
   timeline chosen from five options; an optional budget range; a required
   message; and a required consent checkbox beneath a scrolling privacy policy.
2. The nine interests are `digital_general`, `website`, `branding`, `film`,
   `photography`, `sns_pr`, `digital_marketing`, `recruitment` and `other`. Any
   number of them may be chosen, including none.
3. The five timelines are `within_3_months`, `within_6_months`,
   `within_1_year`, `over_1_year` and `undecided`.
4. The budget control is a two-handle range over yen whose handles cannot cross,
   spanning `1000000` to `30000000`, where the upper value is an open ended
   ceiling. Both chosen values are printed above the track. It is operable from
   the keyboard and announces its values.
5. A submission that is missing a required field, or carries an address that is
   not an email address, is rejected as invalid. The errors are shown on the
   same page, associated with the inputs that caused them, and announced. The
   rest of the visitor's answers survive the rejection.
6. A submission with `consent` false is refused by the server, not only by the
   browser, and the refusal states that the privacy consent is the reason.
7. A submission that passes stores exactly one enquiry record and sends the
   visitor to a confirmation route that names what was sent and moves focus to
   it. This is the only visitor action on the site that touches persisted state.
8. Repeated submission from one origin is refused after a small number of
   attempts in a short window, and the refusal says so rather than failing
   silently.
9. Only an `editor` may read stored enquiries. A `reader` asking for them is
   denied.

### The editorial interface

1. An `editor` signs in and reaches an editorial interface that lists projects,
   topics and members, each showing whether it is published or still a draft.
2. Creating a project runs as a multi-step sequence with a route of its own per
   step: first the case facts, then the hero still, then the gallery and the
   credits. Each step is reachable by its own address, each step keeps what the
   previous step captured, and the record is not created until the last step is
   committed. Leaving halfway creates nothing.
3. Uploading a hero still or a portrait puts the bytes in the object store under
   a fixed key scheme and nowhere else. The stored object is the fact; a copy on
   the app's own disk or a row of image bytes in the database does not count.
4. Publishing a record makes it readable to everyone; unpublishing it makes it
   denied to everyone but an `editor` again, and the same rule reaches its hero
   object.

### Language editions

1. Every route exists at a Japanese path and at an English path under the `/en/`
   prefix, and the two are the same site in two editions.
2. A switcher reading `JP` and `EN` sits in the header rail and moves between
   the current route's two editions. Switching reloads the document rather than
   swapping words in place, because the interface strings and the type stack
   both change.
3. The display headings `About Us`, `Service`, `Projects`, `Topics` and
   `Talk with us` are English in both editions. Only body copy changes.
4. The document's language is declared correctly per edition, and each switcher
   link declares the language of the edition it leads to, not the one it sits
   in.
5. Japanese body copy is justified and sets as clean rectangles; English body
   copy is not justified. The two treatments are applied per element, so a Latin
   word inside a Japanese sentence still sets in the Latin family.

### Accounts

1. Accounts are email and password. A successful sign-in returns a bearer token
   that the client sends on every request needing one, and the token expires.
   Passwords are stored hashed, never in a recoverable form.
2. Signup is open and creates a `reader`. There is no password reset in this
   build.

### The site's own pages

1. A privacy page, reachable from the footer of every route in both editions,
   states what the studio records about an enquiry, who reads it, and how long
   it is kept.
2. A terms page, reachable from the footer of every route in both editions, is
   also linked from the signup form.
3. A first-time visitor is asked once about non-essential cookies, in one
   dismissible choice that does not block the page, and the answer survives a
   reload. A returning visitor who already answered is not asked again.
4. Any unmatched path renders the studio's own not-found route, carrying the
   full persistent shell, one very large numeral, one line saying the page was
   not found, and a control back to the home route. The response also carries a
   genuine not-found status, so a machine reading it is told the same thing a
   person is.
5. The sitemap the build ships enumerates the real routes explicitly rather than
   deriving them from a scan of its own bundle, because such a scan returns
   fragments of an embedded video player and reports them as routes.
6. Every route carries its own title and its own meta description, written for
   that route rather than repeated from the home route, so a link to a case or a
   post carries a description of that case or that post.
7. A terms page, reachable from the same footer, is also linked from the signup
   form, and no credential or access key appears in anything the browser
   downloads.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home, Japanese edition | public |
| `/en/` | Home, English edition | public |
| `/about-us/` | The studio story, five strands | public |
| `/service/` | The four disciplines | public |
| `/projects/` | Project index | public |
| `/projects/{id}/` | Project case write-up | public when published |
| `/team/` | The team grid | public |
| `/company/` | Registration facts and access | public |
| `/topics/` | Editorial index, filterable | public |
| `/topics/{id}/` | Editorial post | public when published |
| `/talk-with-us/` | The enquiry form | public |
| `/talk-with-us/sent/` | Enquiry confirmation | public |
| `/privacy/` | What the studio records and keeps | public |
| `/terms/` | Terms of use | public |
| `/signin/` | Sign in | public |
| `/signup/` | Create a reader account | public |
| `/studio/` | Editorial interface, record lists | `editor` |
| `/studio/projects/new/facts/` | Create a project, step one | `editor` |
| `/studio/projects/new/hero/` | Create a project, step two | `editor` |
| `/studio/projects/new/gallery/` | Create a project, step three | `editor` |
| `/studio/enquiries/` | Stored enquiries | `editor` |
| any unmatched path | Not found | public |

Every route above also exists under the `/en/` prefix.

**Entry and redirects.** A request for `/studio/` or any route beneath it
without a session lands on `/signin/` and returns there afterwards, not to the
home route. Signing in as `editor@example.com` lands on `/studio/`; signing in
as `reader@example.com` lands on the home route, because there is no editorial
surface for a reader. Signing out returns to the home route and ends the
session. A token that expires while an editor is midway through the create
sequence sends the next step to `/signin/` and, once signed in again, back to
the step that was interrupted with its captured answers intact. A signed-in
`reader` who asks for `/studio/` or `/studio/enquiries/` is denied rather than
redirected, because the route exists and the account may not have it. A request
for a draft project's detail route is answered as not found whether the caller
is a visitor, a `reader`, or not signed in at all.

**Journeys.**

1. *Read the home route end to end.* Open `/`. The loader counts up and hands
   over to a headline already in place over a moving coloured mass. Scroll
   through the studio strand, the four disciplines, the five featured cases,
   the three featured topics, and the closing invitation. Each strand ends at a
   `View more` control pointing at its own index.
2. *Retune the simulation.* Open the settings control in the left margin. The
   panel grows from it and the page goes soft behind it. Drag `Movement range`
   and watch the mass respond while the drag is still happening. Change
   `Sphere colour one`. Press `Escape`. Focus returns to the control. Navigate
   to `/projects/`: the mass is still in the new colour and has kept moving.
   Reload: the defaults are back.
3. *Open a case.* From `/projects/`, point at the row for `Forest Economy
   Recruit`. The large still becomes that case's hero. Click the row, arrive at
   `/projects/1396/`, read the client `Midori Holdings`, follow `Visit site`,
   return, and page to the next case and back to the index.
4. *Filter the editorial index.* Open `/topics/`, select `Interview` in the
   category rail. The address now names the filter, the page did not reload, and
   the cards that entered the set played their arrival. Open
   `/topics/1358/` and read it.
5. *Send an enquiry.* Open `/talk-with-us/`. Choose `enquiry`, fill the name,
   company, job title and email, pick three of the nine interests, choose
   `within_6_months`, drag the budget handles, write a message, and submit
   without ticking consent. The submission is refused and the refusal says the
   consent is why, with every other answer still in place. Tick consent and
   submit. Arrive at `/talk-with-us/sent/`, which names what was sent and holds
   focus.
6. *Switch edition.* From any route, choose `EN`. The document reloads at the
   `/en/` twin of the same route with English body copy under the same English
   display headings.
7. *Publish a case.* Sign in as `editor@example.com`, open `/studio/`, walk the
   three create steps, commit, and confirm the new case is absent from
   `/projects/` while it is a draft and present once published. A visitor asking
   for it in between is told it is not there.

**States.** The project index, the topic index, every filtered view, the team
grid, the editorial record lists and the stored-enquiry list each carry an empty
state that says what is missing rather than showing a blank panel. Every route
carries a loading state while its content is on the way, and the loader appears
once per document rather than between client-side route changes. A failed
request shows a message on the surface that asked for it and leaves the rest of
the page usable; nothing anywhere replaces the page with a stack trace or a
blank screen. A route whose record does not exist, or exists as a draft for this
caller, renders the not-found route rather than an empty detail page.

## UI/UX notes

The design direction comes from the studio's own specification rather than from
a house style, and it is best described as a quiet near-monochrome office
document with one living object in it. The north star: in the first moment a
visitor should understand that this is a serious studio that made something they
have not seen before, and the only thing carrying that is the moving mass.
Everything else is deliberately still so the mass has room. The register is
editorial rather than operational: this is a piece of publishing, the subject is
seen before the interface, and a visitor is reading rather than working.

The mood is calm, spacious and almost entirely grey, with the one saturated
thing on the page being the mass itself. Space over dividers: strands separate
because of the air between them, not because a rule was drawn. Restraint over
expression: if anything other than the mass reads as busy or colourful,
something has gone wrong. Calm over motion everywhere except the one object that
never stops.

**Palette by role.** The ground is a near-white neutral, and the tinted ground
used on index and form routes is a second near-white neutral a shade cooler
than it. Every piece of body and display text is a mid neutral, and that same
mid neutral is the dark ground of the service band, the navigation overlay and
the footer, where the text inverts to the near-white neutral. Filled buttons and
arrow discs at rest are a deep cool neutral, one step darker than the text.
Secondary metadata, the scroll glyph and the muted half of any pair are a mid
cool neutral. Hairlines, the loader ground and the scrollbar thumb are a light
cool neutral; the dashed underline beneath a subheading is a light neutral;
table row separators are a near-white neutral; the scrollbar track and the
midpoint of the loader ramp are a near-white cool neutral. The only two
transparencies in the system are the mid neutral at half strength for an
inactive switcher link and the same mid neutral at one per cent for the settings
panel's shadow.

There is no near-black neutral anywhere in the site's own surfaces, and that is
the single most important palette rule here. A build that substitutes a
near-black neutral for the mid neutral will look correct in a screenshot and
cheap on a real screen. The one exception is the simulation's own clear and
shadow values, which are a near-black neutral by necessity and are never
visible as a surface, and a deep, soft blue that belongs to the same set.

Where a third-party video player is embedded, its own palette, a mid, vivid
blue, a mid, vivid cyan, a light, vivid cyan, a light, muted green and a light,
soft magenta, stays inside its own frame and must not reach the page around it.
That player ships a preset palette, a preset type scale and a preset shadow set,
and none of them belong to this design.

The mass itself is the only place colour lives, and its defaults are the
studio's to choose: it must read as a smooth gradient running warm through to
cool with no banding and no hard edge, and it must never be mistaken for the
flat greys around it.

**Type.** One geometric grotesque carries everything Latin, at weights four
hundred for display headings, English body copy, numerals and button labels, and
five hundred for job titles and category labels. `Satoshi` is the family, with a
normative fallback to any installed geometric grotesque and then to the system
sans stack. One Japanese family carries Japanese copy at weight four hundred for
body, five hundred for subheadings and lead paragraphs, and six hundred for
member names and article titles. `Noto Sans JP` is the family, with a fallback to
the installed Japanese system stack. Both are named because a typeface is an
identity the builder cannot derive from a description; neither ships as a file.

Display headings are enormous, thin and grey, never heavy and never black: the
hero headline and every section heading set at `117px` at the desktop design
width, falling to about a tenth of the viewport width on a phone, on a line
height of one hundred and twenty per cent with a very slight negative tracking.
The loader counter sets at the same `117px` with its percent sign at `52px`.
Body copy sets between `14px` and `16px` across the range, a ruled subheading
between `16px` and `22px`, and a button label at a flat `15px`. Three
typographic settings are load bearing: the loader numerals use tabular figures
so the counter does not jitter sideways as it climbs, Japanese body copy uses
proportional-width punctuation with justification so the paragraphs sit as clean
rectangles, and button and cursor labels never break a word in half.

**Shape and density.** Density is spacious: strands are separated by a great
deal of air, headings are the height of a hand, and nothing is packed. Radii are
a fixed vocabulary and each one means something rather than being chosen per
component: a full circle for anything that must read as a disc, a large pill for
the menu control and every pill-shaped button, a softer rounding for the opened
settings panel, a tighter one for the closed panel and its control, a small
rounding for a framed video block and a colour swatch, and the smallest for a
range track and its handle. A shape that is neither a disc nor one of those
roundings does not belong.

**Motion.** The motion character is eased: nothing snaps and nothing springs,
except one control that is allowed to overshoot. Movement leaves quickly and
arrives slowly, and the whole site animates on one small family of speeds rather
than a different one per component. The signature moment is the line reveal:
every heading and every paragraph is clipped and slides up from below its own
edge while fading in, and the fade finishes noticeably before the movement does,
so text settles into place rather than flying in. Scrolling backwards
un-reveals what has already arrived, which is the detail people notice.

Pictures do not fade in: a blank plate sweeps across from the left, then anchors
to the right and shrinks away, uncovering the image as it goes, and on a gallery
alternate cells are delayed so the grid uncovers as a diagonal rather than all
at once. Where several stills share one frame they cross-fade on a slow loop of
between twelve and twenty-two seconds so two are always partly present.

Round things merge instead of touching: sibling filled shapes inside a filtered
container blend into one another as they approach, forming a visible neck, and
separate again as they part. Three places carry it and all three must. The three
dots beside the menu control are absorbed into the middle one on a pointer and
stretch into a cross when the overlay opens. A labelled pill button sits as a
disc and a plate with a permanent neck between them, and the neck closes into a
single lozenge when it is pointed at. The paired arrow discs on the contact rail
read as one peanut at rest and pull apart into a dumbbell before they separate.
The effect applies to solid fills only, never softens the container's text, and
never visibly blurs a shape that is alone.

The navigation overlay is a wipe, not a fade. It is revealed by clipping upward
from the bottom edge over about a second on a curve that is almost flat at both
ends and violent in the middle, and closing does not reverse it: the panel
continues upward and off the top in well under half the time, so closing feels
decisive rather than undone. That asymmetry is deliberate and must be kept.

One control overshoots and nothing else does: opening the settings panel turns
its button a quarter and springs slightly past before settling, while the two
faders on its face scissor into a cross and their handles shrink away. Using
that overshoot anywhere else breaks the register.

Two things follow the scroll directly rather than being triggered by it: the two
marquee bands move exactly as far as the scroll and stop the instant it stops,
and the canvas layer fades as the visitor leaves the first screen. If either
ever plays at its own speed the motion is wired wrong.

The pointer carries a large soft disc that arrives late and never quite catches
up, and it uses a blend that keeps it legible over both the near-white and the
mid neutral grounds without a second variant. Over the show reel it carries the
words `Show Reel`.

Under a reduced-motion preference the line reveals render already revealed with
no transform and no fade, images render uncovered, the looping cross-fades hold
their first still, the marquee stops, the overlay shows and hides instantly, the
loader shortens to the count alone, and the pointer disc is suppressed. The
simulation is the one thing that does not stop, because it is content rather
than decoration; it continues at reduced amplitude and wanders less.

**Accessibility.** Text meets WCAG AA contrast against its ground at every size
it is used, and the muted mid cool neutral is never pushed below body size
because it does not hold the ratio there. The inactive half of the language
switcher is raised to meet the same bar rather than relying on a half-strength
ink, and in any case the active edition is marked by an underline as well as by
colour, because meaning is never carried by colour alone. The settings panel and
the navigation overlay are both dialogs and behave as dialogs. Full keyboard
navigation reaches every control with a visible focus ring, icon-only controls
carry accessible names, touch targets are comfortably sized, and the
`Show Reel` label is real text on the block it labels rather than existing only
inside a pointer follower that a keyboard user never sees.

**Layout and responsive behaviour.** The layout archetype is top navigation: a
fixed rail across the top carrying the studio mark and one control that opens
the full map, with no persistent sidebar anywhere. There is exactly one
structural breakpoint, at tablet width. Above it there is one layout that scales
continuously with the window and stops scaling at the desktop design width, so
dragging the window wider grows everything smoothly until it reaches a
comfortable maximum. Below it there is a second layout in which every two-column
strand stacks, the menu control loses its label and becomes a disc of dots, the
language switcher leaves the rail and appears only inside the open overlay, the
settings panel moves to the bottom corner, the pointer disc disappears
altogether, the team grid and the topic grid each become a single column, and
the gallery runs full bleed in one column. At a narrow viewport nothing
overflows sideways and every navigation target stays reachable. One more case is
easy to forget and must be built: a short window on a laptop with several
toolbars open moves the settings panel to the bottom corner and reduces its
maximum height, which is the only place the site responds to height rather than
width.

The mode is light and it is designed fully. A dark edition is not part of this
build.

**What it must not look like.** Not a page dominated by a single hue family with
no second signal. Not a marketing composition where the working interface
belongs. Not a grid of bordered, shadowed cards: this site has no card borders,
no hover highlights, no background changes on a row, and no boxes around form
fields. On the project index the entire pointer response is the still swapping
and the label rolling, and that restraint is the design. A build that adds a
border, a shadow or a hover tint has replaced the design with a template.

## Technical requirements

The site is delivered as a multi-page progressively-enhanced application: the
server produces the HTML for every route, the browser receives a complete
document on first paint, and the interactive layers are added on top of markup
that already works without them. The backend is `Flask` with `Jinja` templates.
The front end is vanilla progressive enhancement: no client-side framework, no
build-time component compiler, and the simulation, the settings panel, the
overlay and the reveal system are authored directly against the platform. The
datastore is `PostgreSQL`, read from `DATABASE_URL`. Binary content lives in
`MinIO`, an S3-compatible object store, read from `STORAGE_ENDPOINT`,
`STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Authentication
is app-implemented email and password issuing bearer tokens. `GET /api/health`
returns `200` once the app is ready. The app logs one structured line per
request carrying the method, the path and the outcome.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor: the only backing services available in this environment are
`PostgreSQL` and `MinIO`, and reaching for anything else is a contract
violation. Both are already running and reachable at the environment variables
above, and neither is to be downloaded, installed, compiled or started.

Read every host, port and credential from the environment. Never hardcode one.

No credential, API key, object-store access key or admin token appears in
anything the browser downloads: not in a served document, not in a script, not
in a stylesheet, not in a JSON response, and not in a comment inside any of
them. Every secret stays on the server side of the boundary, and the browser is
given signed or proxied access instead.

Object keys follow one fixed scheme and no other:
`media/{collection}/{record_id}/{sha256_of_bytes}.{ext}`. A hero still for
project `1396` therefore lands at
`media/projects/1396/9f2a4b1c8d3e6f507a9b2c4d6e8f0a1b2c3d4e5f60718293a4b5c6d7e8f90a1b.png`,
and a portrait for member `7` lands under `media/members/7/`. Bytes live in the
bucket and nowhere else: not on the app container's filesystem, not in a
database column, not inlined into a document. Protected content is reached
through an authenticated streaming endpoint on the app's own origin, which is
the one mechanism this build uses and uses consistently. No pre-signed URL is
ever issued for an unpublished record, and the streaming endpoint applies the
same draft rule the detail route applies.

The site ships no binary asset of any kind. No photograph, video, font file,
texture, model or vector file is part of the build. Every still, portrait,
illustration, map and icon is drawn by the app at run time or described
procedurally, and every icon is inline vector geometry rather than an icon font,
a sprite sheet or a shipped file.

A third-party video embed does not load its player until the visitor scrolls it
into view, and until then it is represented by a poster frame and a play control
that are part of the build. That embed does not set the page's own type or
colour, and its stylesheet does not reach the document around it.

The home route reaches its largest contentful paint in under two seconds on a
cable connection and becomes interactive in under three and a half. Cumulative
layout shift is zero: every reveal moves only compositor properties, and every
media box declares its aspect ratio before its content arrives. Total transfer
for the home route, excluding media, stays under four hundred kilobytes
compressed. One reveal observer serves the whole document rather than one per
element.

Fonts are subset to the character inventory the site actually uses, the Latin
family swaps rather than blocking, and the Japanese family, which is the
expensive one, is subset rather than served whole from a third party.

The application server survives a restart of either backing service and
reconnects rather than exiting.

## Data model

Six tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

### `accounts`

`id` integer, `email` unique and case-insensitive, `password_hash`, `role` one
of `reader` or `editor`, `created_at`. Nothing else. An account owns no content.

### `projects`

`id` integer and opaque, and it is the detail route's own segment. `title` and
`subtitle` are per-edition strings. `year_label` is free text and is not a date.
`client` is a string. `visit_url` is an optional absolute URL. `disciplines` is
a non-empty set drawn from `digital`, `movie`, `spatial` and `brand`. `status`
is one of `draft` or `published`. `hero_key` is the object key of the hero
still. `body` is per-edition rich text. `published_at` is a timestamp and orders
the index newest first. Whether a project appears anywhere a visitor can see is
derived from `status`, never stored twice.

### `project_media`

`id`, `project_id`, `object_key`, `kind` one of `image` or `embed`, `span` for
its width in the gallery grid, and `position` for its order. A row is the only
record of a stored object; there is no second copy of the bytes.

### `project_credits`

`id`, `project_id`, `role_label`, `name`, `position`. Ordered by `position`.

### `topics`

`id` integer and opaque. `title` per edition. `category` is exactly one of
`blog`, `member`, `interview`, `news` and `recruit`. `published_at` is a date
and renders unpadded. `hero_key` is an object key. `body` is per-edition rich
text carrying chapter headings, questions, answers, paragraphs and full-width
images. `status` is one of `draft` or `published`.

### `members`

`id`, `position_title` in English, `name` per edition, `location`, `interests`
as an ordered list of short strings, `portrait_key`, `display_order`.

### `enquiries`

`id`, `enquiry_type` one of `enquiry` or `materials_request`, `name`, `company`,
`job_title`, `email`, `address` optional, `interests` a possibly empty subset of
the nine, `timeline` one of the five, `budget_min` and `budget_max` optional
integers in yen, `message`, `consent` boolean, `locale` one of `ja` or `en`,
`created_at`. A row is written only when `consent` is true; a refused submission
writes nothing at all.

An unpublished project or topic, and the object named by its `hero_key`, are
readable only by an `editor`. Two simultaneous requests for an unpublished
record, one from an `editor` and one from a `reader`, resolve independently:
exactly one is served and exactly one is denied, and neither changes the record.

**Seed data.** Seeding is idempotent: restarting the app must not duplicate
rows.

Two accounts, `editor@example.com` as `editor` and `reader@example.com` as
`reader`.

Five projects, newest first, four published and one left as a draft so the
boundary exists without any editorial action:

| id | Title | Client | Year | Disciplines | Status |
|---|---|---|---|---|---|
| `1396` | `Forest Economy Recruit` | `Midori Holdings` | `2026` | `digital`, `movie` | `published` |
| `1402` | `Sound Harbour Festival` | `Sound Harbour` | `2025-26` | `digital` | `published` |
| `1411` | `Talent Futures Opening` | `Jinji Lab` | `2025` | `movie` | `published` |
| `1428` | `Unkai Sunrise Session` | `Hokkaido Skyline` | `2025` | `movie` | `published` |
| `1435` | `Shoegaze Debut Night` | `Nova Records` | `2026` | `movie` | `draft` |

Three topics, newest first, two published and one left as a draft:

| id | Title | Category | Date | Status |
|---|---|---|---|---|
| `1358` | `Continuing Is What Showed Us` | `interview` | `2026.3.18` | `published` |
| `1361` | `Hiring Page Published` | `recruit` | `2026.3.17` | `published` |
| `1364` | `Starting From Cannot` | `blog` | `2026.3.17` | `draft` |

Four members in display order: `Naoki Morishita` as `CEO`, `Rin Takada` as
`Art Director, Videographer`, `Aya Kubo` as `Designer`, and `Sho Tanabe` as
`Developer`. Every member's location is `Yokohama`.

Each published project and each published topic is seeded with a hero object
already in the bucket at its scheme's key, and each member with a portrait. The
draft project `1435` and the draft topic `1364` each have one too, so the denial
is about entitlement and not about absence.

The company profile is seeded as fixed facts: the legal name
`Kaiyo Interactive Co.,Ltd.`, the postcode `231-0003`, the telephone number
`045-548-6865`, the representative `Naoki Morishita`, founded April 2019,
capital nine million yen, and fifteen staff.

## Front-end specification

This section carries the visual and behavioural detail the studio's own
specification pins. It is unbudgeted and exhaustive on purpose.

### Information architecture

Eleven real routes carry the site, plus a detail route per project and per
topic, plus the not-found route, plus the twin of every one of them under the
English prefix. Three surfaces move a visitor between them and they carry the
same map: the overlay opened from the header rail, which is the complete map;
the footer, which repeats the same three route columns and the same outbound
list on a different ground; and the persistent contact rail, which carries one
destination only. In-page handoffs are the fourth path: each home strand ends at
a `View more` control pointing at its own index, and each detail route carries a
two-way pagination block, one half for sibling records and one half for the
return to the index.

### Typography

Four type classes are the whole system and elements carry them explicitly rather
than inheriting them from a document-level rule: the Latin grotesque at weight
four hundred for display headings, English body copy, numerals and button
labels; the same family at five hundred for member job titles and category
labels; the Japanese family at four hundred for Japanese body copy, at five
hundred for Japanese subheadings and lead paragraphs, and at six hundred for
member names and article titles. Because the classes are per element rather than
per document, a Latin word inside a Japanese sentence sets in the Latin face
correctly, and that granularity is part of the typography rather than an
accident of it.

### Ordering and paging

Both collections order newest first by their published date. The project index
carries every case on one route with no paging control and no filter. The topic
index carries every post on one route with no paging control and a category
filter. Where a list is empty, or a filter selects nothing, the surface says so
rather than rendering a blank panel.

### Module inventory

The component architecture is only visible to a visitor in one way, and that way
is normative: the logotype block, the header rail, the menu control, the
navigation overlay, the contact rail, the footer and the settings panel are one
persistent shell shared by every route, and a route change replaces the document
beneath them without remounting any of them. The canvas is part of that shell,
which is why the simulation keeps its position and its settings across a route
change. Every other module is the builder's to organise.

### Scaling and breakpoints

Sizes, spacing and offsets scale continuously with viewport width between the
mobile and desktop design widths, and stop scaling above the wide breakpoint,
where the desktop values freeze. There is one structural fork, at tablet width;
there is no third tablet design, and at a width between the fork and the desktop
design width the page is simply the desktop layout scaled down. Type that must
not scale linearly interpolates between its two ends across the same range
rather than tracking the window directly. Two further conditional cases exist: a
pointer-capable affordance set that only applies where a real pointer is
present, and a short-window case that repositions the settings panel.

### Stacking order

Low to high: the canvas holding the moving mass sits behind everything, then
document content in flow, then the settings panel's own top and bottom fade
masks, then the contact rail, then the settings panel and its button, then the
navigation overlay, then the header rail so it stays legible over the open
overlay, then the logotype block, then the video modal's close control, and at
the very top the loader.

### The persistent shell

Six elements sit outside the document flow on every route, including the
not-found route, and survive a route change.

1. **The logotype block**, top left: a script wordmark reading the studio name
   in lower case with the strapline
   `digital communication service with branding design` set beneath it in small
   caps at roughly a fifth of the wordmark's height. It fades in with the header
   and hides while the overlay is open, because the overlay carries its own
   reversed copy. It is drawn as text, not loaded as a vector file.
2. **The header rail**, fixed near the top, its inner block a zero-height flex
   row aligned to the right so the rail contributes nothing to layout and its
   children hang off it.
3. **The menu control**, a dark pill carrying the label `Menu` and three dots to
   its left. At rest the label reads `Menu`; when the overlay is open it reads
   `Close` and the outer two dots become short bars rotated into a cross while
   the middle one fades. On a pointer at rest the outer two converge on the
   middle one and are absorbed. On a narrow viewport and inside the video modal
   the pill collapses to a disc and drops the label.
4. **The navigation overlay**, the complete map. It carries `About Us`, `Team`,
   and an external `Recruit` link that opens in a new tab in the first row;
   `Projects` and `Company` in the second; `Service` and `Topics` in the third;
   and a second column of outbound links to two sister studios and three social
   profiles, the first two carrying a trailing outbound-arrow glyph. Its ground
   is a full-viewport plane in the mid neutral, and its link items stagger in
   behind the wipe, with the second column arriving after the first.
5. **The contact rail**, fixed to the bottom of the viewport on every route: a
   horizontally scrolling band of the phrase `Talk with us` repeated at display
   size with a paired-arrow disc between each repetition, pointing at the
   enquiry route. Pointing at it spreads the two discs apart into a dumbbell
   while the label rolls up and its duplicate arrives from below. It fades out
   where it would collide with content.
6. **The footer**, on the mid neutral ground with reversed text, in four
   columns: the reversed logotype block with the legal name, the venue line and
   the address; the same three route columns as the overlay; the outbound list
   with its arrow glyphs; and the copyright line right aligned. It reveals on
   scroll as one unit, more slowly than anything else on the site.

### The two button patterns

**The labelled pill** carries every `View more` and the enquiry form's submit
control. A disc sits at its left and a rounded plate carries the label, the two
overlapping such that a visible neck already joins them at rest. Pointing at it
grows both toward each other until the neck disappears and they read as one
lozenge. The label is white, never breaks a word in half, and does not move.

**The paired-arrow link** carries the contact rail and index rows. Its label is
duplicated, the copy sitting just below the original, and on a pointer both roll
upward together so the label appears to turn over. Two arrow discs sit
overlapping to its right, reading as one peanut at rest and pulling apart into a
dumbbell on a pointer. This roll is the site's single most repeated interaction
and appears on every text link that is not a plain paragraph link.

### Iconography

Six glyphs, all inline vector geometry, no icon font, no sprite sheet, no file:
a forward arrow drawn at three sizes because it is optically corrected rather
than scaled; a back arrow inside a square hit area, carried by the return
control of a pagination block; a diagonal outbound arrow with a return stroke,
carried by every link that leaves the site, drawn in a near-white grey because
it only ever sits on the mid neutral; a downward arrow in the muted mid cool
neutral for the hero's scroll cue, because it sits on the near-white ground
rather than inside a disc; a paper-plane outline drawn as a stroke on the
submit control, which carries a second subpath forming the fold crease inside
the plane, and dropping that crease turns the icon into a plain triangle; and a
location pin built from a circle and a line rather than a path, on every member
card.

Two things that look like icons are not, and are specified as geometry because
they move. The menu control's three dots are small squares rounded to circles,
stacked vertically and drawn through the merge filter so they join as they
converge. The settings control's glyph is two thin horizontal bars, each
carrying a small disc riding along it, so it reads as a two-channel mixing desk.

### The loader

Full viewport, above everything, pointer-events off, on a light cool neutral
ground with a counter in the lower left. The count runs from `000` to `100`,
three digits and zero padded, in tabular figures so it does not jitter
horizontally on every tick, with a percent sign set smaller and offset up and
right of the numerals. While it counts, the ground pales from the light cool
neutral through the near-white cool neutral to the near-white neutral. At the
end the ground pins to the near-white neutral and the counter slides down out of
sight, clipped by its own parent.

### The reveal system

A state class is added to an element when it crosses a threshold in the
viewport and removed again when it leaves, so scrolling backwards visibly
reverses every reveal. Four reveal families carry the whole site.

1. **The line reveal** carries every heading and every paragraph. Each line sits
   in a clipping box and starts slightly more than its own height below the clip
   edge, so descenders are fully hidden before it moves, then slides up and
   fades in with the fade finishing well before the movement. A variant takes an
   explicit stagger in tenths of a second, expressed as a step index rather than
   a duration.
2. **The ruled subheading** draws a hairline above the text, growing from no
   width to about a third of the content width, with the text sitting just
   beneath it.
3. **The dotted subheading** carries a small square bullet at its left and a
   dashed underline that draws from no width to full width.
4. **The image wipe** runs two halves back to back: a plate grows from the left
   edge to full width, then anchors to the right and shrinks away, uncovering
   the image left to right. A delayed variant offsets alternate cells.
5. **The plain fade** is the fallback for elements that must not move: member
   cards, credit blocks, pagination and category rails.

Two values are scrubbed against scroll position rather than triggered by it: the
horizontal offset of the two marquee tracks, and the opacity of the canvas
layer. Everything else is class-driven and plays at its own speed.

The page keeps a small amount of state on the document itself: whether loading
has finished, and whether the settings panel is open. Both drive styling
directly. Nothing is keyed off a user-agent string; the three things such a
string would be used for are better expressed as a pointer capability query, a
reduced-motion query and the site's own overlay scrollbar.

### The settings panel in detail

Closed, it is a small rounded square in the left margin on the tinted near-white
neutral, with a shadow at one per cent alpha that is almost invisible by intent:
it stops the panel's edge vibrating against the page rather than making it look
raised. Raising that alpha until a developer can see it in isolation makes the
panel look like it is floating on a card, which is wrong.

Open, it is a tall translucent panel. Six properties change together on one
speed: its width, its height, its ground, its rounding, its backdrop blur and
its transform. It does not fade in and expand; it grows from the control it was,
and the blur arrives with the growth so the page visibly goes soft behind it.
It sits vertically centred in the left margin on a tall window, moves to the
bottom corner on a short one, and moves to the bottom corner again on a narrow
viewport where it is also smaller.

Its control list has fade masks at the top and bottom, so scrolling dissolves
the list into the panel's own ground rather than cutting it off. Its scrollbar
is the site's own overlay scrollbar, not the browser's: a thumb in the light
cool neutral on a track in the near-white cool neutral, invisible at rest and
fading in shortly after the panel finishes growing rather than during it. A
full-viewport catcher closes the panel on a click outside it, and that catcher
is pointer-transparent whenever the panel is shut.

Labels are set in the mid neutral at a small size in the five-hundred weight
with slightly negative tracking. A colour well is a small rounded square with
the native colour input inside it scaled up and clipped, which is what removes
the browser's own chrome from the swatch and leaves a clean tile of colour. A
range control is a thin rounded track in the near-white cool neutral with a
square rounded handle in the light cool neutral, authored for both major engine
families so the two look identical.

### The routes

Each route below states its own structure: its ground, what sits in it, and in
what order. Where a route says nothing about an element of the shell, the shell
renders normally.

**Home.** Six strands. A full-viewport hero whose headline is three rows,
`Interactive`, `Experiences with Us` and `for Active Growth.`, the first and
third indented so the block reads as a hanging shape rather than a centred
stack, vertically centred by an offset that uses the small viewport unit so it
survives mobile browser chrome resizing. A standfirst sits out past the right
margin on a wide window and drops below the headline on a narrow one; its rest
state is very slightly above zero opacity rather than zero, deliberately, so
the element stays composited and justified Japanese text does not re-lay out
mid-transition. Then the show reel, a framed video block whose inner content is
twice the frame's width and pans across it, scaling up as the visitor arrives,
carrying the `Show Reel` label. Then the studio strand on the near-white ground
with three stills scattered over the copy's whitespace. Then the service strand
on the mid neutral ground with the four-discipline figure. Then the projects
strand on the tinted ground with its heading right aligned, unlike every other
strand. Then the topics strand, continuous with it, its heading left aligned and
deliberately clipped by the strand's top edge so the enormous type does not read
as a banner. The route closes with two centred lines of invitation and the
contact marquee at heading scale, bleeding off both edges.

**The four-discipline diagram** is four near-identical organic silhouettes
stacked at slightly different scales and rotations at descending opacity, which
gives the shape a soft laminated edge and makes it look thick without any shadow
being drawn. The four discipline names and their sub-services sit inside the
topmost shape, each in its own clipped line so they reveal on the line stagger
rather than appearing with the shape.

**About Us.** Five strands: `Group Philosophy`, `Mission`, `Vision`, `Our DNA`
and `Culture`. A fixed left rail lists all five, marks the one occupying the
viewport in the full ink with an underline, updates as the visitor scrolls in
both directions, and each entry scrolls its strand into view. This is the only
place on the site where scroll position drives a persistent navigational state.
Each strand is a ruled label, a two-line display heading, a body of eight to
eleven short lines each revealing on the stagger, and a large circular figure on
the right holding a rendered soft-bodied form: a single lobed mass for one
strand, a two-lobed form caught mid-separation for another, a cluster of five
distinct spheres in contact for a third. Those are the same simulation posed and
rendered, not three separate illustrations, which is why they are generated
rather than shipped. `Our DNA` and `Culture` each carry a horizontal carousel
driven by paired arrow controls set above its right edge; the cards rotate
slightly in depth as they advance, which is the only use of perspective on the
site, and a ring of dots rotates while a carousel is initialising. The route's
ground moves through three values as the visitor descends, from a near-white at
the top through a mid grey to a near-black at `Culture`, and it moves roughly
twice as slowly as anything else on the site, so it feels like walking from a
bright room into a dark one rather than a light being switched.

**Service.** A rail listing `Our Service` and the four disciplines, then the
same four-discipline figure at the top of the page, a ruled `Our Service`
subheading and an opening paragraph, then four identical discipline blocks, all
four with copy left and figure right. Each figure is a large circle clipped from
moving footage, bleeding off the right edge, with no frame, no border and no
shadow: a circular window onto work in motion.

**Projects index.** The tinted ground, the heading right aligned, and the
two-column index at full length: one large still pinned on the left, and every
case as a row on the right. A row is a title wrapping to two lines with the
second indented to the first, a one-line subtitle truncated rather than
wrapped, a metadata row of year label and discipline tags separated by a rule,
and a forward arrow on its own baseline. The whole row is the link.

**Project detail.** A full-bleed hero still at the top with no container, the
header and logotype legible over it. Then two columns on the near-white ground:
left the title, the `Client` label and name, and the outbound `Visit site` link
with its diagonal glyph; right an introduction paragraph. Then the gallery, a
full-bleed grid of stills at mixed spans interleaved with an embedded player at
full container width, with a hairline gutter, revealing on the image wipe with
alternate cells delayed. Then the credit block, a two-column list of role
against name with dotted rules between rows. Then the two pagination blocks.

**Team.** The near-white ground and a four-across grid of member cards filling
the standard content block. A card is a portrait in portrait orientation with no
radius and no border, an English job title in the muted tone at the five-hundred
weight, a location preceded by the pin glyph and right aligned on the same
baseline, a name in the six-hundred weight, and two or three interests each
prefixed with a hash. All four text elements fade in independently and none of
them slide: a grid of faces arriving in sequence reads as a product listing, and
the restraint is deliberate. Every portrait holds one convention, a still figure
against blurred movement, and holding it across the whole team is the route's
entire art direction.

**Company.** The tinted ground, a two-entry rail, and each section opening with
a hairline drawn across about a third of the content width followed by its name.
The profile is a two-column definition table whose rows are separated by
hairlines running the full table width, including above the first row and below
the last, carrying the company name, the address block, the telephone number,
the representative, the founding date, the capital, the headcount and the
business content. The business-content cell is the tall one and carries a
bracketed group label followed by a list, repeated per business area; its
bullets are literal characters rather than list markers so wrapped lines hang
under the first character of the text. The access section carries a drawn
schematic map, the address, the postcode and travel directions. This is
deliberately the plainest route on the site.

**Topics index.** The tinted ground, the heading left aligned and clipped at the
content area's top edge exactly as on the home route, the category rail aligned
with the first row of cards rather than with the heading, and a three-across
grid to its right. A card is a landscape still with no radius, a title wrapping
to two lines, and a metadata row of category and date in the muted tone.

**Topic detail.** The tinted ground and a single centred column at about half
the viewport width, with no sidebar, no sticky rail and no reading-progress
indicator, which is the right call for the longest route on the site. The head
is the category, the date, the title and a full-column hero. The body follows
one fixed pattern: a chapter heading preceded by a hairline across the full
column; a question prefixed by a plain hyphen and a space, set in the muted
tone, with no name; an answer prefixed by the speaker's family name and a colon,
set in the full ink; paragraphs justified with proportional-width punctuation;
and inline images at full column width with no caption and no radius. The gap
between paragraphs is clearly larger than the gap between lines, which is the
single thing that makes a very long article comfortable rather than exhausting.

**Talk with us.** The tinted ground, the display heading, three lines of
introduction, and the form in a centred column. Fields are not boxed: each is a
label above an input with a hairline beneath it running the full column width,
and nothing else, and each label carries a small square bullet at its left.
Placeholders repeat the label as an instruction in a tone lighter than the muted
ink. The first field is the only exception and the only card on the route: the
radio pair sits on a white plate running the full column width, because it
changes what everything below it means. A required-field legend sits above the
first field in the muted tone, and the multiple-choice group carries its own
note that more than one may be chosen. The nine checkboxes lay out three across
on a wide window and one per row on a narrow one.

The budget control reads as a thick dark bar in the deep cool neutral with two
thin pale notches cut into it, rather than two knobs sitting on a thin line. The
two chosen values are printed above the track with a separator between them, and
the track's own end labels are printed below it. The two handles are offset
asymmetrically so both notches stay inside the bar at the extremes, and the
library's own second grip line is suppressed.

The privacy block is a long scrolling policy inside a fixed-height container
ending with a link to the studio's contact address, followed by a single consent
checkbox. Submission is blocked until it is ticked. The submit control is the
labelled pill carrying `Submit` and the paper-plane glyph.

**Not found.** The full persistent shell renders normally and the simulation
runs behind it; only the content area differs. It carries `404` at display
scale, one line beneath it saying the page was not found, and a
`Back to TOP` control. Because the shell is complete, a visitor who lands here
by accident is one click from anywhere rather than at a dead end.

### Performance and delivery

This is a zero-asset build and the substitution of a drawn form for a shipped
file is the guide to every asset class it needs: a still is a generated
composition, a portrait is a generated composition holding the same convention,
the discipline diagram is drawn geometry, the access map is drawn geometry, and
every glyph is drawn geometry. Nothing in the delivered build directory is an
image, a video, a font, a model or a texture.

Performance is a requirement rather than an aspiration here, because the canvas
runs on every route. Scrolling any route holds sixty frames per second on
integrated graphics at the desktop design width with the mass running. Switching
away from the tab pauses the simulation. A project detail route does not fetch
its third-party player until the visitor reaches it. Nothing on any route shifts
position while it loads.

### Interface strings

`Menu` and `Close` on the menu control. `JP` and `EN` on the switcher.
`View more` for every index handoff. `Related Projects` from a discipline.
`Visit site` on a case. `404` and `Back to TOP` on the not-found route.
`Show Reel` in the pointer disc and as real text on the block it labels.
`Submit` on the form. `Talk with us` on the contact rail. `Client` before a
client name. `Profile` and `Access` on the company rail. `Group Philosophy`,
`Mission`, `Vision`, `Our DNA` and `Culture` on the studio rail. `All`, `Blog`,
`Member`, `Interview`, `News` and `Recruit` on the category rail. The copyright
line reads `Copyright Kaiyo Interactive Co.,Ltd. All Rights Reserved.`

## Constraints

- Single studio, single tenant. There is no organisation model, no workspace
  switcher and no per-client login.
- No shop, no cart, no pricing, no payments and no subscriptions.
- No comments, no likes, no ratings, no sharing widgets and no embedded social
  feed.
- No search across the site, and no full-text index.
- No newsletter, no mailing list and no chat widget.
- No notification of any kind is sent to anybody. The enquiry is stored and read
  from the editorial interface.
- No password reset and no third-party identity provider.
- No external network call at run time other than to the two named backing
  services. A third-party video embed loads only after the visitor scrolls it
  into view, and nothing else reaches the network unprompted.
- No native application and no installable app shell.
- No binary asset is part of the build.
- The sitemap enumerates the real routes explicitly rather than deriving them
  from a scan.
- The app must stay responsive with two hundred projects, five hundred topics
  and fifty thousand stored enquiries, and with a gallery of sixty items on a
  single case.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the
  environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written
  to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the
  app root, empty.
- Serve a production build behind a static or preview server, never a dev
  server.
- The server must keep running after this session ends and must not be a child
  of the shell. An ordinary background job dies with its shell, and the app will
  not be running when it is next opened.
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
| `GET /api/health` | none | readiness |
| `POST /api/auth/signup` | `email`, `password` | the created account and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token and the account's role |
| `GET /api/projects` | optional `locale` | a top-level JSON array of published projects, newest first |
| `GET /api/projects/{id}` | none | one project with its gallery and credits |
| `POST /api/projects` | the case facts | the created project |
| `PATCH /api/projects/{id}` | any subset of the case facts, including `status` | the updated project |
| `POST /api/projects/{id}/media` | the bytes and a `kind` | the stored object's key |
| `GET /api/topics` | optional `category`, optional `locale` | a top-level JSON array of published topics, newest first |
| `GET /api/topics/{id}` | none | one topic with its body |
| `POST /api/topics` | the post facts | the created topic |
| `PATCH /api/topics/{id}` | any subset, including `status` | the updated topic |
| `GET /api/members` | none | a top-level JSON array in display order |
| `GET /api/media/{key}` | none | the object's bytes, streamed |
| `POST /api/enquiries` | the eleven fields of the form | the stored enquiry |
| `POST /api/cookie-choice` | `accepted` | the recorded cookie choice |
| `GET /api/enquiries` | none | a top-level JSON array, newest first, `editor` only |

Field names are exactly as written in `## Data model`. Bearer auth is carried on
everything except `GET /api/health`, `POST /api/auth/signup`,
`POST /api/auth/login`, `POST /api/enquiries` and the public read endpoints. A
successful call returns the named resource or shape; an invalid or unauthorized
call is rejected as a client error, never as a server error and never as a
silent success.

### No mocks

The object store is the fact. A hero still that exists only as a row of bytes in
`PostgreSQL`, only as a file on the app container's filesystem, only as a data
URL inlined into a document, or only as a key in an in-memory dictionary, is not
a stored object. A response the app returns to itself saying an upload
succeeded, without an object under the key scheme in the bucket, is not an
upload. `MinIO` is the fact: the app's pages and its own tables can only reflect
what lives in the object store, never substitute for it. The same holds of
`PostgreSQL` for every record: an enquiry that exists only in a confirmation
page is not a stored enquiry.

## Definition of done

A visitor can read the studio's work and its writing in either language edition,
retune the coloured mass from the settings panel and watch it keep running
across a route change, and send a project enquiry that is stored and confirmed
back to them. A submission without the privacy consent is refused and says so.
A project or topic still in draft is invisible to everyone but an editor,
including its hero image in the object store, and an editor can publish one and
make both appear.
