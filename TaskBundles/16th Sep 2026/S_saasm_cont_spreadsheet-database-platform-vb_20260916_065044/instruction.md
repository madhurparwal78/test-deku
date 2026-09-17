# Sheaf

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser, read
the home route end to end, open a sector route, a competitor comparison route and a case
study from the navigation, and start a free trial from the form, landing on a confirmation
route that names the team site created for them, without hitting an error page. A
different stranger, signed out or signed in as an ordinary reader, must NOT be able to
read a single unpublished route or a single unpublished image by any means, including a
direct request to the API for it by slug. Images belong in the object store at their
scheme's key: a copy kept on the app container's own filesystem does not count, and
neither does a row holding the bytes.

## Overview

Sheaf is a spreadsheet that is really a database. People put their data into a grid the
way they always have, and underneath each document is a relational store with typed
columns, formulas that recalculate themselves, and rules that can hide a single cell from
a single person. This brief is not that product. This brief is the marketing and content
site that sells it: the long home route, one route per industry, one route per competing
product, a template gallery, case studies, webinars and a blog, ending in a free trial.

Two things live on two origins and the build must treat them as two things. The marketing
and content site is what you are building, and it is a block based content system that
marketing people edit weekly without an engineer. The product is a separate application at
`https://app.sheaf.example`, and every sign in, sign up, template open and document link
leaves this site for it. The site never renders a signed in product state and holds no
product surface of its own. Merging the two would couple a headline change to an
application deploy, which is the one structural mistake this build must not make.

The information architecture is fixed, and the route families are the shape of it.
Documentation lives on its own documentation origin and the community forum on its own
discussion origin; this site links out to both and hosts neither, and it links out the same
way to the public source repository, a video channel, a chat platform and six social
profiles. On this origin the families are: product routes; capability routes; one sector
route for each of `nonprofit`, `marketing`, `legal`, `finance-accounting`, `construction`,
`project-management`, `higher-education`, `manufacturing`, `general-purpose` and
`spreadsheet-for-research-labs`; one comparison route for each competing product; content
routes for the blog, webinars, case studies and the newsletter; company routes for about,
our team, partners, work with us, contact and trademark; and two legal routes. That is at
least forty routes, and the shape is deliberate: one route per sector, one route per
competitor.

The content model is the hard part, and it is the reason the site is worth building at
all. The reference carries at least forty marketing routes and they are four templates
with content swapped, rather than forty bespoke pages: a sector template, a capability
template, a comparison template and a content template. A marketing editor must be able to
add a sector route or a competitor comparison route as a content operation with no deploy.
The second hard part is unpublished content. An editor works on drafts in the open, and a
draft route, a draft article and a draft image must be unreadable to everybody except an
author, including through the API, including when the slug is guessed correctly.

What this deliberately is not: there are no comments, no likes, no forum, no messaging, no
search, no localisation, no non-latin locale and no second language: the site appears in
one language only. There is no product surface here. There is
no payment, no invoice and no card: a trial is free and takes no money.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| visitor (signed out) | Read every `published` route, article, case study, template card and comparison table. Accept or decline non essential cookies. Start a free trial from the form. | **Cannot read any `draft` route, article or image, by any path, including a direct API request by slug.** **Cannot reach the authoring console.** **Cannot see another visitor's trial.** |
| reader | Everything a visitor can do, plus read their own trial and the team site address created for it. | **Cannot read a `draft` of anything.** **Cannot create, edit, publish or unpublish any route.** **Cannot upload an image.** **Cannot read another reader's trial, or the trial signup list.** |
| author | Everything a reader can do, plus create, edit, publish and unpublish every route and article, upload and replace images, write comparison claims with their source and their date, and read the trial signup list. | **Cannot delete another author's account.** **Cannot change another reader's trial.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from a reader session to any author-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged. The same holds for reads: a `draft` route requested
directly by a reader session, or with no session at all, is answered as not found, and the
answer is identical to the answer for a slug that was never created, so the response does
not confirm that the draft exists.

Signup is open. Anyone can create a `reader` account from the signup form, and starting a
free trial creates one for them if they do not have one.

Seeded accounts, which exist before the first request:

| Email | Role |
|---|---|
| `author@example.com` | author |
| `author2@example.com` | author |
| `reader@example.com` | reader |

Every seeded account uses the password `deku-demo-pw-2026`.

## Core features

### Auth

Accounts are email and password, implemented by the app. A successful login returns a
bearer token the client sends on every later request; an expired or absent token on a
protected endpoint is denied, not served. Passwords are stored hashed, never in clear text.
Signup is open and creates a `reader`. There is no password reset, no external identity
provider and no social sign in. `author@example.com`, `author2@example.com` and
`reader@example.com` all sign in with `deku-demo-pw-2026`.

### Content routes, drafts and publishing

1. Every public page on this site is a **route** record with a `slug`, a `template`, a
   `title`, a `status` of exactly `draft` or `published`, an ordered list of sections, and
   a `published_at` timestamp that is empty while the status is `draft`.
2. A route whose status is `published` is readable by anyone, signed in or not.
3. A route whose status is `draft` is readable only by an author. For a visitor or a
   reader the route is answered as not found, whether it is requested as a page or from
   `GET /api/pages/{slug}`, and the body carries no title, no section, no image key and no
   hint that the slug exists.
4. Publishing sets the status to `published` and stamps `published_at`. Unpublishing sets
   it back to `draft`, clears `published_at`, and the route stops being readable by anyone
   but an author from the very next request.
5. Only an author may create, edit, publish or unpublish a route. The same request from a
   reader session is denied and the stored route is not changed in any way.
6. A slug is unique across the whole site. Creating a second route with a slug that is
   already taken is rejected as invalid, and the existing route is left untouched.

### Four templates carry forty routes

7. Exactly four templates exist, and every route uses one of them: `sector`, `capability`,
   `comparison` and `content`. Adding a route is a content operation and never a deploy.
8. A `sector` route carries, in this order: a sector headline, an adaptability section
   reading `Custom <sector noun> that adapts to your workflow`, the shared core claim
   `The structure of a database, the flexibility of a spreadsheet` inherited from the
   content model and identical on every sector route, one sector specific control section
   naming that sector's own compliance concern, three template cards filtered to the
   sector, a cross link to `Sheaf Solutions`, a `Frequently asked questions` set, and a
   sector specific closing action. The shared core claim is stored once and inherited, so
   editing it changes every sector route at once.
9. A `capability` route carries the capability name, a value headline, **exactly three
   numbered steps** named `Build`, `Share` and `Analyze`, a `Why Sheaf?` differentiation
   section, and a closing action reading `Try it now!` that links into the product at
   `https://app.sheaf.example`. A capability that needs five steps is two capabilities, so
   a route submitted with any number of steps other than three is rejected as invalid.
10. A `comparison` route names one competing product and carries a claim, a neutral factual
    table, and a migration path. Every comparative claim is a stored field carrying its
    own `source` and its own `checked_on` date, and both are rendered on the page beside
    the claim, because a stale claim about a competitor's pricing is the highest risk
    content a company publishes. A claim saved without a source or without a date is
    rejected as invalid and nothing is written. The comparison table is a real table with
    real header cells, never a layout grid. A competitor's name is used only nominatively:
    it never appears in the site's own typeface, its own colours or its own lockup.
11. A `content` route is an index plus an article. The index has three tiers: one featured
    article with a large title, a set of highlighted articles below it, and a heading
    reading `All Posts` above a paginated grid of the remainder. An article of type
    `case_study` carries three extra structured fields, `sector`, `organisation_size` and
    `capability_demonstrated`, and the sector routes of rule 8 filter their proof cards on
    `sector`. There is exactly **one first-level heading per route**; every card title on
    the index is a third-level heading.

### The home route

12. The home route is one long scroll of thirteen full-width sections in this fixed order,
    because the order is the argument rather than a layout: hero; `Built for security
    conscious industries` on the brand gradient; a supporting section; `Who uses Sheaf?`
    with three named reference customers; `Built for the data you can't afford to lose`
    carrying six capabilities; `Sheaf Solutions` by sector; a second supporting section;
    `Ready-to-use templates`; `Power tools`; a wide supporting block; `We have your back`
    for support and community; the `Sheaf Workshop` offer; and the closing call to action
    `Unlock a better way to organize data.` The document title is
    `Spreadsheet Software to End Data Chaos | Sheaf`.
13. The hero carries the headline
    `Turn the spreadsheets running your business into secure applications`, the subtitle `No-code apps, self-hosted or fully managed. Cell-level
    access rules control who sees what, including the AI assistant.`, three actions at
    three weights, and a product demonstration with a poster frame. The three actions are a
    solid primary reading `Get started`, an outline secondary of equal prominence reading
    `Build with a prompt` which is the entry to the assistant, and a quieter arrow link
    reading `Security for regulated industries`.
14. The capability section is the longest on the page and carries these six capabilities as
    third-level headings, each with its supporting line and an illustrative figure:
    `AI Assistant`, reading `Chat with your data and have productive conversations.`;
    `Access rules`, reading `Collaborate with confidence and peace of mind, using a unique
    system of granular data permissions.`; `Forms & surveys`, reading `Collect and analyze
    data easily.`; `Flexible layout`, reading `Arrange your data on screen to maximize the
    productivity of you and your team.`; `Visualizations`, reading `See what matters at a glance,
    from big trends to small details.`; and `More features`, which links to the product
    overview route. Two measured copy defects in that block are corrected rather than
    reproduced: the access-rules line is missing an article before `unique`, and the layout
    line carries an awkward possessive, recast above.
15. The power tools section carries exactly three third-level headings:
    `Super-charged formulas`, `Extensible` and `Unprecedented control`, with a link reading
    `Sheaf for developers` and an inline link reading `open source`. The security section's
    cards are addressed to roles, the first reading `IT` with the line
    `Lock down insider risk by eliminating spreadsheet sprawl.`
16. Reference customers are **three named organisations with a sentence each**, never a
    wall of faded logos. The three are `Northgate Digital Service`, `Merrow Instruments`
    and `Halliwell Electrical`. Each is rendered as its name set in type at the height a
    logo would occupy, because a name set in type reads better at small sizes and
    reproduces nobody else's mark.
17. The three featured templates are `Investment Research Tracker`,
    `Class Enrolment Register` and `Customer Records Lite`. Opening any template card
    leaves this site for
    `https://app.sheaf.example`.

### The shared chrome

18. An announcement bar sits above the header on every route, full width, on the brand
    gradient, carrying one icon, one sentence and one inline link. It is a content managed
    slot with a single message and a single link. It **must be dismissible, and the
    dismissal must persist for that visitor across a reload and across routes**. Its copy
    is `Looking for a Latticework alternative? See how Sheaf compares.`
19. The header carries the mark, then the wordmark, then five menu triggers reading
    `Product`, `Solutions`, `Developers`, `Resources` and `Pricing`, then a star count
    control, then `Sign In`, then `Sign Up`. Each trigger opens a menu panel rather than
    navigating. Every panel holds a promotional aside, two or three columns of links, and a
    closing strip on the brand gradient carrying `Get started` and `Contact sales`. `Sign
    In` and `Sign Up` both leave for `https://app.sheaf.example`.
20. A closed menu panel is removed from the focus order and from the accessibility tree,
    and restored when it opens. Moving through the page with the keyboard alone must never
    land on a control inside a closed panel, and a panel parked out of sight is still a
    panel a reader can reach unless it is properly taken out of the running order.
21. The star count control reads a count from the app's own `GET /api/stars` endpoint. **It
    must degrade gracefully**: when the count is unavailable the control still renders its
    star glyph, still reads `Star`, and still links to the repository route, with no
    number. The space the number will occupy is reserved from first paint, so the header
    never shifts sideways when the number arrives, and the count never blocks the header
    from rendering.
22. Every route except the home route ends with a shared closing action band immediately
    above the footer, carrying one second-level heading reading `Create a free site` and
    one action. It is chrome, edited once, and the home route is the exception because its
    thirteenth section already is one.
23. The footer carries multiple link columns covering the product, the source repository
    and its roadmap, the newsletter, the company, support, content, the community and the
    comparison family, then a social row of six links, then a legal line. Every social link
    is rounded on one diagonal and square on the other, echoing the mark.

### The media library

24. Every image the site renders lives in the object store, and nowhere else. The key
    scheme is fixed: `media/{route_id}/{sha256_of_bytes}.{ext}`, for example
    `media/12/9f2a41c7e8b0d3a5f6c92e1470bd8a3c25e6f09b1d4a7c83e5210fb96d7c4a8e.webp`. The
    bytes must be in the bucket at that key. Bytes on the app container's filesystem, bytes
    in a database column, and a data URI inlined into the page are each a contract
    violation, however correct the page looks.
25. Uploading the identical bytes for the same route twice produces the same key, creates
    no second object and creates no second media row. The second attempt is a no-op that
    returns the existing key.
26. Only an author may upload or replace an image. The same request from a reader session
    is denied and no object is written to the bucket.
27. An image attached to a `draft` route is not publicly readable. A visitor requesting it,
    by its key or through the app, is denied; it becomes readable at the moment its route
    is published. Serve protected bytes through an authenticated streaming endpoint on the
    app's own origin, and never hand a reader a URL that would let them fetch the object
    directly.
28. Every content image carries alternative text, and an image saved without it is rejected
    as invalid, naming the field. An image that is purely decorative declares itself
    decorative instead, and is not read aloud.

### Starting a free trial

29. `POST /api/trials` takes `email`, `team_name` and `sector`, and creates a trial. The
    response and the confirmation route both carry the team site address, built from a
    fixed scheme: the team name lowercased, non alphanumeric runs collapsed to a single
    hyphen, trimmed of leading and trailing hyphens, placed as the first label of
    `https://{team_slug}.sheaf.example`. `Merrow Instruments` therefore becomes
    `https://merrow-instruments.sheaf.example`.
30. A team slug is unique. Two people submitting the same team name must not both get the
    same address: exactly one succeeds and the other is rejected as a conflict, naming the
    field, and no second trial row and no second team site are created.
31. Submitting the same email and the same team name twice creates no second trial. The
    second attempt returns the first trial's team site address unchanged.
32. Starting a trial signs the visitor in as a `reader` if they were signed out. A reader
    can read their own trial from `/trial/started/`. A reader requesting another reader's
    trial is denied, and the signup list at `GET /api/trials` is author only.
33. Every form on the site rejects invalid input inline, names the field it rejected, and
    writes nothing. A trial without an email, with an email carrying no `@`, without a team
    name, or with a sector outside the published sector list, is rejected and no row is
    created. The contact form and the newsletter form behave identically.

### Cookies, third-party scripts and link integrity

34. A first-time visitor is asked once about non essential cookies, in a bar offering
    accept and decline as two equally reachable controls. The answer survives a reload and
    every later route, and the visitor is not asked a second time.
35. No third-party script, tag, pixel, advertising network or embed is requested before
    that answer is accept. The site's own origin is the only origin contacted on a first
    paint. The heavy video embed is facaded: the poster frame and a play control render
    immediately, and the real embed is fetched only when somebody presses play.
36. Every internal link on every published route resolves to a published route on this
    site. A link in the footer, in a menu panel, in a card or in body copy that points at a
    slug which is missing or still `draft` is a defect the site must not ship, and
    `GET /api/links` returns every internal link with the resolved status of each.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The thirteen-section home route | public |
| `/product/` | Product overview | public |
| `/product/self-hosted/` | The self-hosting argument | public |
| `/pricing/` | Plans and the free tier | public |
| `/security/` | Security for regulated industries | public |
| `/developers/` | Sheaf for developers | public |
| `/ai-assistant/` | Capability route for the assistant | public |
| `/automations/` | Capability route for automations | public |
| `/forms/` | Capability route for forms and surveys | public |
| `/csv-viewer/` | Capability route for the file viewer | public |
| `/templates/` | The template gallery | public |
| `/solutions/` | The sector index | public |
| `/solutions/nonprofit/` | Sector route | public |
| `/solutions/legal/` | Sector route | public |
| `/lookup/` | The general comparison route | public |
| `/lookup/latticework/` | Comparison route, one competitor | public |
| `/blog/` | Content index | public |
| `/case-studies/` | Content index, case study type | public |
| `/webinars/` | Content index, webinar type | public |
| `/newsletter/` | Newsletter signup | public |
| `/about/` | Company | public |
| `/our-team/` | Company | public |
| `/partners/` | Company | public |
| `/work-with-us/` | Company | public |
| `/trademark/` | Company | public |
| `/contact/` | Contact form | public |
| `/privacy/` | What the site stores about a visitor, and for how long | public |
| `/terms/` | Terms | public |
| `/trial/` | The free trial form | public |
| `/trial/started/` | Trial confirmation, carries the team site address | reader |
| `/login` | Sign in to this site | public |
| `/signup` | Create a reader account | public |
| `/studio/` | Authoring console: the route table | author |
| `/studio/routes/new/` | Create a route | author |
| `/studio/media/` | The media library | author |
| `/studio/signups/` | The trial signup list | author |

**Entry and redirects.** A signed out request for `/studio/` or any route under it
redirects to `/login` carrying the intended address, and a successful sign in lands on that
address rather than on a generic home. A reader who reaches `/studio/` is refused with a
page saying the console is for authors, offering a way back to `/`. Signing out returns to
`/` and the next request for `/studio/` redirects to `/login` again. A token that expires in
the middle of an edit leaves the editor open, says the session ended, and offers to sign in
again without losing the typed text. An unknown address renders the site's own not found
page with a way back, and so does a `draft` slug requested by anybody who is not an author.

**Journey 1, a visitor converts.** Open `/`. Read the hero. Follow `Solutions` in the
header to `/solutions/nonprofit/`. Read the three proof cards filtered to that sector.
Follow the closing action to `/trial/`. Type `Merrow Instruments` as the team name, choose
`nonprofit` as the sector, type an email with no `@`, and submit: the form refuses inline
and names the email field, and no trial exists. Correct the email and submit again: the
browser lands on `/trial/started/`, which reads back the team name and the address
`https://merrow-instruments.sheaf.example`.

**Journey 2, an author publishes.** Sign in at `/login` as `author@example.com` with
`deku-demo-pw-2026`. Open `/studio/`. The route table lists every route with its slug,
template, status and last edit. Create a comparison route for a second competitor at
`/studio/routes/new/`, add one comparative claim, and try to save it with no `checked_on`
date: the save is refused, the date field is named, and nothing is written. Add the date,
save, and leave the route as `draft`. Open a private window and request the new slug: the
site answers not found. Return to `/studio/`, publish the route, and request the slug in
the private window again: the route renders, and its claim shows its source and its date
beside it.

**Journey 3, a draft image stays private.** Signed in as `author2@example.com`, upload an
image to a `draft` sector route from `/studio/media/`. The media library shows its key
under `media/{route_id}/`. Sign out and request that key: the request is denied. Publish
the route and request it again: the image renders.

**States.** Every list has an empty state that says what would appear there and offers the
action that creates it: an empty route table, an empty media library, an empty signup list,
a content index with no published article, and a sector route whose proof filter matches
nothing. Every route has a loading state that reserves the space its content will occupy so
nothing jumps when the content arrives. Every error is caught and rendered as part of the
page, and no failure anywhere takes the app down or shows a stack trace.

## UI/UX notes

The north star is that a visitor who has never heard of Sheaf understands in the first
screenful that this is a spreadsheet with a database underneath, and trusts it enough to
keep scrolling. The register is consumer marketing addressed to an engineering audience:
the subject itself is seen first, atmosphere is allowed, and no screenful is decoration
standing in for content. The direction is considered, quiet and self-assured, with exactly
one colour that means a visitor can act on this. The confidence comes from restraint and
from evidence, never from ornament. It must not read as a consumer toy, and it must not
read as an enterprise brochure of stock photography and grey logo walls.

**Palette by role, described rather than pinned.** The accent, which is also every solid
button, is a mid, vivid teal, and it is the only thing on a page wearing it: nothing
decorative borrows it. Headings are a deep, muted blue. Body text is a mid neutral, and
navigation text on both desktop and mobile is a deep neutral, one step darker than body
text so the chrome reads as chrome. The navigation background is a near-white neutral, and
so is the light section background that carries the large pattern. The footer is a
near-black cool neutral carrying light neutral text. Solid button text is a near-white
neutral; outline button text is a near-black neutral. The colour that means a form was
refused is a mid, vivid red and it appears nowhere else. Input borders and separators are a
light neutral at low opacity, and an input border on focus is that same colour at a
stronger opacity. The underline that grows under a link is a mid neutral by default. The
mark also carries a mid, soft teal, a mid, vivid orange and a light, vivid orange, and
those three exist in the mark and in nothing else. The exact shades are yours, so long as
each holds the rule stated beside it.

**One gradient carries the brand and there is no second one.** It runs teal on the left to
green on the right, horizontally, and it is used for full-width section backgrounds, for
the announcement bar and for the closing strip inside every menu panel. A second gradient
anywhere is a regression. Only theme-authored tokens are the design system: a publishing
system ships a preset palette of named colours, a gradient library and editor furniture
that nobody chose, and binding a component to one of those looks correct on the day it is
built and wrong forever afterwards, so discard the preset group rather than treating it as
a palette.

Every colour, size and rhythm described below was measured from the reference, and where a
value could not be measured the intent is stated in its place. Nothing here is a spec sheet.

**Typography is carried exactly, because a type family is an identity rather than a taste.** One text
family in four weights, declared as a single token resolving to a stack of families already
present on the target platforms and metric compatible, so nothing reflows when the fallback
swaps. Ship no font file. The scale is six heading steps and one body step and nothing
else: heading 1 at `60` in weight 500 with a line height of `1.1`; heading 2 at `36` in
weight 500 at `1.2`; heading 3 at `24` in weight 500 at `1.3`; heading 4 at `18` in weight
500; heading 5 at `14` in weight 500, uppercase, with its letter spacing opened to
`0.075em`; heading 6 at `14` in weight 700; body at `16` in weight 400 at `1.5`; and the
button at `1em` in weight 500. The fifth step is the only uppercase role and the only one
that opens its letter spacing, which makes it an eyebrow label rather than a heading, and
it is named that way in the build. The scale gains one step so that no two roles share a
size: heading 5 and heading 6 differ only in weight and case, and a scale with two roles at
one size has run out of room at the bottom. The first-level heading has one size per
breakpoint, taken from the scale; a route that wants a smaller title uses a different role
rather than setting a size of its own.

**Shape, space and density.** Buttons are softened just enough to read as controls and no
more. Social links are rounded on one diagonal and square on the other, which is the mark's
own geometry applied to a control, and both come from one definition so they cannot drift
apart. Four shadow presets were measured: a crisp flat one, a sharp flat one at lower
opacity, a natural blurred one and a deep blurred one. Only the two flat ones read as
deliberate, so carry exactly one shadow, crisp, flat and offset, with no blur, and discard
the natural and the deep blurred pair. Keep two rhythms and express both in a single unit: one rhythm inside a
component and a larger one between full-width sections, because one scale serving both
gives either cramped sections or bloated components. There are two container widths and no
third, a narrow one for the hero and for any section that is mostly words, and a wider one
for card rows, feature grids and logo rows; sections are full bleed and only the inner
container is constrained. Density is comfortable: the home route is a long read, so
sections breathe and the eye is carried down by hierarchy rather than by rules and
dividers. Space over dividers, evidence over adjectives.

**Motion is small, and its character is eased: movement leaves quickly and arrives slowly,
and nothing on this site moves for longer than a beat.** Every transition on the site's own
elements is short: link and menu colour settles into its new colour, button fill settles the
same way, fades are fades, and controls lift by a hair when pointed at under one compound
transition covering transform, border and colour together. Declare two easing
tokens, one for entering and one for leaving, and use only those; the long catalogue of
curves and named animations that arrives with an embedded video player, a lightbox or a
carousel belongs to those components and is not this site's own vocabulary. The site has one
characteristic effect and it must survive: hovering a link grows an underline from one side
rather than switching it on, driven by the width of a painted bar behind the text rather
than by a border so that it can animate, **and it must appear on keyboard focus exactly as
it does on hover**. A menu panel slides into view when its trigger is opened. Nothing is
scroll driven and nothing moves in response to scroll position. Under a reduced motion
preference every animation has a defined behaviour, the product demonstration does not
autoplay, and any looping figure stops advancing on its own, stays manually operable, and
offers a pause control.

**Components by state and behaviour.** Every control has a resting, pointed at, pressed,
focused and unavailable state, and unavailable is never signalled by colour alone. Escape
closes an open menu panel and returns focus to its trigger. Destructive actions, which here
means unpublishing a route and replacing an image, confirm first and say what will stop
being visible. Icons that sit beside a word may be drawn from one shared set; any control
whose only content is a symbol is an inline vector carrying a programmatic name, so a person
listening rather than looking does not hear an empty button.

**Accessibility floors, which are contract rather than taste.** Text contrast meets WCAG AA
and is verified per token pair, and the two pairs that must be checked explicitly are the
light neutral footer text on the near-black cool neutral footer, and any text set on the
accent teal. Every control has a programmatic name. Full keyboard navigation reaches every
interactive element in an order matching the visual order, focus is always visible, and no
focus stop exists inside a closed menu panel. Touch targets are comfortably sized at the two
narrower widths. Landmarks for the header, the navigation, the main region and the footer
exist on every route, heading order runs without skipping a level, and decorative vectors
are marked as decoration so they are not read aloud pointlessly. Meaning is never carried by
colour alone.

**Responsive behaviour.** Declare four breakpoints as tokens and use only those, matched to
the two container widths rather than inherited from a publishing system's own editor
boundary. The layout holds at every viewport between them, with no horizontal overflow at
any width down to a small phone. The heading scale is responsive and the first-level heading
steps down at the narrow widths: a headline rendering at its widest-window size on a phone
wraps to roughly six lines and eats a third of the screen before anything else is drawn,
which is the single most visible defect available here and it must not be reproduced. The
header halves in height at the narrowest width, the inner container is fixed at the widest
width and fluid below it, and the product demonstration scales in proportion rather than
cropping. The five menu panels collapse to a single accordion below the narrow breakpoint,
never to a sideways scroll.

**Commit to one mode.** Design the light mode fully. A dark mode is optional and, if built,
must hold the same contrast bar.

## Front-end specification

**Section styles are an enumerated set rather than free properties.** A section chooses
exactly one of: default, light, dark, brand gradient, large pattern, small pattern. The
large pattern sits on the light grey background and the small pattern on the dark blue one,
both at low contrast against their own background, and both are drawn procedurally rather
than fetched.

**Iconography arrives by two mechanisms.** Interface glyphs sitting through the body of the
page come from one shared set, and the mark and the two section background patterns are
drawn as inline vector encoded directly into the stylesheet rather than fetched. The
reference serves its glyphs from a variable icon family carrying fill, grade, optical size
and weight axes, which is economical for one file but leaves every glyph without an
accessible name; here every glyph is inline vector, so an icon accompanied by text stays
decorative and an icon that is the sole content of a control carries a name.

**Module and component architecture: four first-party blocks build every section.** A section block, which is a full-bleed band
carrying a background style and a spacing size; a container block, which is the inner width
constraint; a content block, which is a titled unit with an optional image, a body and a
link; and a content block group, which is a row of content blocks used for the card rows.
Thirteen visibly different sections on the home route are assembled from those four plus
generic blocks for headings, paragraphs, buttons, columns, spacers, video and social links.
Keep the vocabulary this small: it is the reason a marketing team builds forty routes
without an engineer. The theme's own blocks are visible in the markup and carry a shared
block-name prefix on every section, container and content block, which is what makes a
template a template rather than a page.

**The mega-menu mechanism.** Each of the five primary navigation items opens a mega-menu
panel of a fixed width, holding a promotional aside, two or three columns of links, and the
closing strip on the brand gradient. A closed panel may be parked out of view rather than
removed from the document, which keeps it measurable and lets it slide, but a panel parked
out of view is still present: it stays in document order, it stays in the focus order, and
its content is still there for any reader that ignores position. A closed panel is therefore
removed from the focus order and from the accessibility tree, and restored when it opens.

**The star-count widget.** The star-count widget is the one piece of chrome whose content
arrives at runtime rather than being authored, and in the reference it renders inside an
isolated frame fed by a third party under a permissive two-clause licence, which is exactly
what makes its degraded state both
necessary and achievable. Here the count comes from the app's own endpoint and the degraded
state is unchanged.

**The mark.** A three-by-three arrangement of rounded squares with cells omitted, drawn in
four brand colours: the accent teal, the soft teal, the vivid orange and the light orange.
Each square carries the same asymmetric rounding as the footer social links, scaled, and
both are generated from one definition.

**Zero-asset substitution: ship no binary.** Every asset class the reference carries is
replaced rather than reproduced, and nothing is faked. No image file, no video file, no icon
font file, no text font file.
Every illustration is generated: card artwork is a rounded rectangle at the container width
filled with a low contrast two-stop gradient seeded from the card's own title, with the
title set in the type scale and a grid motif taken from the mark's geometry. The six
capability figures stand in for screen recordings of the product, which the build does not
have and must not fake, so each is a static generated diagram of the capability, a grid of
cells drawn from the palette with the relevant affordance highlighted in the accent, and a
caption describing what a real recording would show; each is flagged in the site as a
placeholder awaiting a genuine recording before launch. The three customer logos become the
organisation's name set in type, in the footer text colour, at the height the logo occupied.
**Every generated substitute is deterministic from its seed**, identical on every load and
on every machine, or the page shimmers between visits and no visual check is ever stable.

**Performance.** Three findings govern the weight of this site, and they are the clearest
wins available. The feature demonstrations are the heaviest thing on the reference and they
are animated raster images of screen recordings. The icon payload is a complete library
shipped to draw a handful of glyphs. And the reference contacts advertising and analytics
networks roughly eight times for every one request it makes to its own origin, which on a
product whose stated differentiators are self-hosting and granular permissions is worth a
conversation, so none of it loads before consent. A feature demonstration is never an
animated raster image; where a real
recording lands later it is a muted, looping video element with a poster frame and a pause
control, in a modern codec. Screen recordings of software are the worst possible content for
an animated raster format: large flat areas, many frames, and a palette the format cannot
represent well. The icon payload stays tiny, which inline vectors achieve for nothing.
Images below the fold are deferred. Text is subset and preloaded. The home route stays under
a strict transfer budget before consent and before any video plays, and at most one
third-party origin may be contacted before consent.

**Stacking.** The build's own stacking order is a small token scale whose largest value has
no more than four digits. A third party that claims a value above it is contained in its own
stacking context rather than competed with.

## Technical requirements

The rendering model is server-rendered pages with interactive islands: the browser receives
complete HTML for every public route on first paint, and only the pieces that need behaviour
hydrate afterwards. The front end is **Remix (React Router 7)**, the HTTP API is
**Fastify**, and both are served from one origin as a single production build. The datastore
is **PostgreSQL**, read from `DATABASE_URL`. Images live in **MinIO**, the S3-compatible
object store, read from `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. The public address and port are read from `APP_PUBLIC_URL` and
`APP_PUBLIC_PORT`. Never hardcode a host, a port or a credential; read every one from the
environment. Both backing services are already running and reachable at those variables, and
must not be downloaded, installed, compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything
else is a contract violation.

`GET /api/health` returns `200` once the app is ready, and it must not require a token.
Logging is structured to standard output, one line per request, carrying the method, the
path and the outcome, and it never carries a password, a token or an object store secret.

Every response the app serves carries the standard security headers, including a strict
transport policy and a nosniff content-type policy, and they are present on a page response,
on an API response and on the not-found response alike. Nothing the browser downloads
contains a credential, an API key, an object store secret or an admin token: the object
store keys are read on the server and never reach the client bundle, and a protected object
is served through the app rather than by handing the browser an address that fetches it
directly.

Read access to unpublished content is decided on the server for every request, on the page
path and on the API path alike, from the requester's session rather than from anything the
client sends about itself. A response for an unpublished slug is indistinguishable from the
response for a slug that does not exist. Sorting, pagination, counts and any index listing
must not reveal that a draft exists: a content index shows the published count, never the
total.

Team site addresses are unique across the whole site. Two people submitting the same team
name at the same moment must not both be given the same address: exactly one succeeds, the
other is rejected as a conflict, and no second team site and no orphaned trial row is left
behind. Replaying an identical trial submission produces no second write and no second team
site, and returns the address the first submission produced.

The app makes no outbound network request at runtime. The star count is served from the
app's own endpoint, the video is facaded until somebody presses play, and no analytics,
advertising, chat or video vendor is contacted before consent, which in this environment
means never.

## Data model

Seven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must be
written into `/app/USER_README.md` alongside each account so a grader can sign in.

**`users`** carries `id`, `email` which is unique and lowercased, `password_hash`, `role`
which is one of `author` or `reader`, and `created_at`. Nothing stores the clear password.

**`routes`** carries `id`, `slug` which is unique across the whole table, `template` which
is one of `sector`, `capability`, `comparison` or `content`, `title`, `status` which is one
of `draft` or `published`, `published_at` which is null while the status is `draft`,
`sector` which is null except on a sector route, `created_by` referencing `users`, and
`updated_at`. The uniqueness of `slug`, and the uniqueness of a team site address, are
properties of the stored data rather than of a request handler: two writers racing for the
same value leave exactly one row behind, and the loser is rejected.

**`sections`** carries `id`, `route_id` referencing `routes`, `position` which is an integer
unique within a route, `style` which is one of `default`, `light`, `dark`, `brand-gradient`,
`large-pattern` or `small-pattern`, `heading`, `body`, and `media_id` which may be null.
Reading a route reads its sections in `position` order.

**`claims`** carries `id`, `route_id` referencing a `comparison` route, `competitor`,
`statement`, `source`, and `checked_on` which is a date. `source` and `checked_on` are both
required; a claim missing either is never written.

**`articles`** carries `id`, `route_id`, `kind` which is one of `post`, `webinar` or
`case_study`, `title`, `excerpt`, `tier` which is one of `featured`, `highlighted` or
`rest`, `published_at`, and for a `case_study` the three extra fields `sector`,
`organisation_size` and `capability_demonstrated`. Exactly one article per content index
carries `tier` of `featured`.

**`media`** carries `id`, `route_id`, `object_key`, `sha256` of the bytes, `ext`,
`alt_text` which is required unless `decorative` is true, `decorative`, and `uploaded_by`.
`object_key` is derived rather than stored twice: it is always
`media/{route_id}/{sha256}.{ext}`. The pair `(route_id, sha256)` occurs at most once, so the
same bytes uploaded twice for one route leave one row and one object.

**`trials`** carries `id`, `email`, `team_name`, `team_slug` which is unique across the
whole table, `sector`, `user_id` referencing the reader it created or signed in, and
`created_at`. `team_slug` is derived from `team_name` by the scheme in Core features, and
the team site address is computed on read rather than stored.

**Seed data.** Three accounts as listed in User roles. Nine `published` routes: `/`,
`/pricing/`, `/solutions/`, `/solutions/nonprofit/`, `/lookup/latticework/`, `/blog/`,
`/case-studies/`, `/privacy/` and `/terms/`. Exactly two `draft` routes, a sector route at
`/solutions/legal/` and a comparison route at `/lookup/rowbase/`, which exist so the
boundary is real before anybody edits anything. Three articles under `/case-studies/`, one
per reference customer, each carrying its `sector`, `organisation_size` and
`capability_demonstrated`, and exactly one of them at `tier` `featured`. One comparison
claim on each comparison route, each carrying its source and its `checked_on` date. Two
media rows on the published home route and one on the `draft` legal route. One trial for
`reader@example.com` with team name `Merrow Instruments`. Seeding must be idempotent:
restarting the app must not duplicate rows.

## Constraints

Single tenant: one site, one set of authors, no customer accounts beyond the reader role and
no per-customer branding. No product surface of any kind lives here: no document, no grid,
no formula editor, no access-rule editor, no form builder, no assistant, no interface
console, no billing screen. No payment, no invoice and no card: a trial is free. No email is
sent and no mail vendor exists. No comments, no likes, no forum, no messaging, no full-text
search, no localisation and no second language. No native or mobile application. No external
network call at runtime of any kind, which includes analytics, advertising, chat and video
vendors, so the star count comes from the app itself. No third-party mark, logo or artwork
appears anywhere, and no binary asset ships. The site must stay responsive with roughly
forty routes, three hundred sections, two hundred articles and one thousand trials.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never
  hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root,
  empty.
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
| `POST /api/auth/signup` | `{ "email", "password" }` | the created reader and `{ "access_token" }` |
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token" }`, the bearer token every later request sends |
| `GET /api/health` | none | `200` |
| `GET /api/stars` | none | `{ "count" }` from the app's own store |
| `GET /api/pages` | `?status=` `?template=` `?sector=` | a top-level JSON array of route summaries |
| `GET /api/pages/{slug}` | none | the route with `sections` in `position` order, its `claims` and its `articles` |
| `POST /api/pages` | `{ "slug", "template", "title", "sections" }` | the created route at `status` `draft`, author only |
| `PATCH /api/pages/{slug}` | `{ "title", "sections", "status" }` | the updated route, author only |
| `GET /api/media` | `?route_id=` | a top-level JSON array of `{ "object_key", "alt_text", "decorative" }`, author only |
| `POST /api/media` | the bytes, `route_id`, `alt_text` or `decorative` | `{ "object_key" }`, author only |
| `GET /api/media/{object_key}` | none | the bytes, authenticated when the route is `draft` |
| `POST /api/trials` | `{ "email", "team_name", "sector" }` | `{ "team_slug", "team_site_url" }` |
| `GET /api/trials` | none | a top-level JSON array of trials, author only |
| `GET /api/trials/mine` | none | the caller's own trial |
| `POST /api/consent` | `{ "choice" }`, one of `accept` or `decline` | the stored choice |
| `GET /api/links` | none | a top-level JSON array of `{ "from", "to", "resolved" }` |

Every endpoint except `GET /api/health`, `GET /api/stars`, the two auth endpoints and the
public read endpoints requires a bearer token. A successful call returns the named resource
or shape. An invalid or unauthorized call is rejected as a client error, never as a server
error and never as a silent success; the exact code is yours, so long as it is a
conventional one. List endpoints return a top-level JSON array.

**No mocks.** The image bytes must be in the MinIO bucket at the key the scheme produces,
and the route, section, claim, article, media and trial rows must be real rows in
PostgreSQL. An in-memory array of media objects, a hardcoded key string the app returns to
itself, bytes written to the app container's filesystem, a data URI inlined into the HTML,
and a JSON file on disk standing in for a table are each a contract violation, however good
the page looks. The named provider is the fact: the app's UI and its own tables can only
reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can read the whole home route, reach a sector route, a competitor comparison and
a case study from the navigation, and start a free trial that ends on a confirmation naming
the team site address created for them. No unpublished route and no unpublished image is
readable by anyone who is not an author, whether they ask for a page or ask the API
directly. Every image the site shows exists in the object store at its scheme's key, and
every comparative claim shows its source and the date it was checked.
