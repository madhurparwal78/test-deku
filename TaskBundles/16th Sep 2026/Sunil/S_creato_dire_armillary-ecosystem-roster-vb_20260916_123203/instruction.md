# Halden

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the Halden site, watch it arrive, turn the
armillary on the front door onto one of Halden's four divisions and enter it, read the roster
of creators inside that division, open a creator's profile, and find anybody on the whole
roster by division, discipline or name. A creator must be able to apply to join, confirm
their address from the mail it sends, sign in, draft a roster profile with their disciplines,
links and portrait, submit it for the studio to publish, and later return to rewrite that
profile and move themselves into a different division, all without hitting an error page.
The hard part is what the public may see. A profile that is not live must answer not-found at
every public address and never appear in any list or in the sitemap; while a creator rewrites
a live profile, the public roster keeps showing the live copy until the change is published;
a creator can never read or change another creator's profile by any address; nothing that
still carries a placeholder can be submitted; and one email creates exactly one account and
one profile, also when the same application is sent twice at the same instant.

## Overview

Halden is the website of a holding company whose business is the creator economy. It owns
four divisions, and the whole site is organised around them: **Creator Media**, **Creator
Communities**, **Creator Products** and **Creator Tech**. Each division has a name, a colour, a
scene, a roster and a route, and those five belong together. The four division colours are
the site's whole colour system: a vivid red for Creator Media, a soft green for Creator
Communities, a vivid blue for Creator Products and a vivid amber yellow for Creator Tech, each
used only for its own division.

The front door is not a page you scroll. It is a single, live, three-dimensional object, an
armillary of four concentric rings around a glossy black sphere, filling one window on a
near-black ground, with the headline `The Operating System for the Creator Economy` set low on
the left, one `About Us` control beneath it, and the navigation reduced to a wordmark, a
three-city clock, a menu control and a light and dark toggle. The four rings are the four
divisions, and turning the object onto one and choosing it is how a visitor gets anywhere.
Every heading on the site is split into lines and characters and revealed line by line; nothing
fades in flat.

Each division route is a long scrolling page on one shared template: the company's mission
line, the division's one-sentence proposition, an uppercase kicker, a paragraph, whatever the
division consists of, and then the people, set in a three-column grid of portraits whose middle
column sits lower than the outer two. The site adds the thing its own pages are made of and the
reference it is modelled on could not maintain: a roster owned by the people in it. `/roster`
shows everybody on one filterable grid, `/creator/<slug>` shows one person, and every view has
its own address.

The information architecture is small and flat. Every surface has its own addressing, so a
filtered roster or a single profile can be sent to somebody and opens exactly as it was seen. On
reachability: any division is one action from the front door through the armillary, the menu is
one action, a roster card's profile and the roster are two, the application is three, and every
legal route is two through the footer or the menu.

Behind a sign in sit two small surfaces that look like the rest of the site. A **creator** owns
exactly one roster profile and edits it beside a live preview of how the public will see it. A
**curator**, a member of the studio, reads what creators send in and publishes it, sends it
back with a note, takes a profile down, moves somebody between divisions and sets the order the
roster is presented in. The roster console follows one principle: there is one roster and
everybody looks at it, a creator filtered to themselves, a curator filtered to what is waiting, on
the same surfaces with different controls. There is no separate administration area and no second
design language, and no real-time behaviour: every surface reads what is stored when it opens.

The graded workflow runs end to end: a visitor applies to a division, confirms their address,
fills the profile, is refused while anything is still a placeholder, submits, is sent back by
the curator, resubmits, is published and appears on the division route and the roster at once,
rewrites the live statement without the public seeing half of it, and finally moves themselves
to a second division, after which a fresh visitor with no session finds them on the second
division's route and not on the first, in the second division's colour.

This task builds the public site, the application, the creator's editor and the curator's
review queue. It deliberately is not the rest of a studio's tooling: no division content
editor, no discipline vocabulary editor, no legal notice editor, no invitations, role changes or
suspensions, no password reset, no live updates, no offline replay, no localisation, no uploads
of any kind, no third-party analytics and no payments.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Read every public route: the front door, the four division routes, `/about`, `/roster` with every filter, sort and search, every live creator profile, `/join-us`, the three legal routes, `/sitemap.xml` and `/robots.txt`; use the command palette; switch light and dark and sketch mode; answer the consent card; apply to join | **Cannot read any profile that is not live by any address, cannot see the review queue, cannot call any `/api/me` or studio endpoint, cannot change anything stored except by applying** |
| `creator` | Everything a visitor can do, plus sign in, read and edit their own profile at any state, replace its disciplines, links and credits, submit it for review once their address is confirmed, rewrite it while it is live, publish their own changes when the division is unchanged, and send a division change for review | **Cannot read or change another creator's profile by any address, cannot publish, send back, take down, move or reorder any profile, cannot see the review queue (a `state` filter from a creator is dropped), cannot submit before confirming their address, cannot edit while their profile is with the studio** |
| `curator` | Everything a visitor can do, plus sign in, read every submitted profile in the review queue, publish a submitted profile, send one back with a note, take a live profile down, move any profile between divisions, and set the curated order of the live roster | **Cannot change a single word a creator wrote about themselves (name, statement, disciplines, links, credits or portrait), cannot publish a profile that is not submitted, cannot create a curator account, cannot change a division's colour** |

The capability matrix above is the whole of the permissions model; authentication is the
app's own email and password, and the account's role is the only identity it carries.
Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `creator` session to any curator-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged. Enforcement follows one order on every request, stopping at
the first failure: signed in, then address confirmed, then role, then ownership, then state. An
anonymous call to any `/api/me` endpoint, any studio
endpoint or any profile write is denied the same way. The role and the owner are always read
from the session on the server, never from a value the request carries.

Signup is open, and applying is the only way in: submitting the application at
`/join-us/apply` creates one `creator` account and one profile in a single step. There is no
separate sign up form and no way to create a `curator` through the app.

Three accounts are seeded, every one of them with the password `deku-demo-pw-2026` and every one
with a confirmed address:

| Account | Role | Name | Profile |
|---|---|---|---|
| `curator@example.com` | `curator` | Ines Marlow | none |
| `creator@example.com` | `creator` | Juno Okafor | `juno-okafor`, live in Creator Media |
| `creator2@example.com` | `creator` | Ada Moreau | `ada-moreau`, a `draft` in Creator Tech, never live |

## Core features

### Sign in

1. `POST /api/auth/login` with an email and its password returns a bearer `access_token`, the
   account's `role` (`creator` or `curator`), its `name` and `verified` (whether the address is
   confirmed). The token authorises every later call as `Authorization: Bearer <token>`.
2. A wrong password, or an email with no account, returns no token and is rejected with `401`
   and the error token `not_authenticated`; the response never says which of the two was wrong,
   and the form shows `That combination is not one we know.`
3. **Repeated failures are limited.** When one email has repeatedly failed to sign in, five times within
   fifteen minutes, every further attempt for that email inside the window is refused with
   `429`, the error token `rate_limited` and a `retry_after` in seconds, even with the right
   password, and the form shows `Too many for now. Try again in a little while.` with its
   submit unavailable until the wait is over. A successful sign in does not count towards the
   limit.
4. Passwords are stored hashed. The literal `deku-demo-pw-2026` signs in every seeded account.
5. `/sign-in` is the one sign in surface, drawn as a layer over the front door's scene, with the
   heading `Sign in`, the fields `Email` and `Password`, a `Sign in` control and one link reading
   `Apply to join` that opens `/join-us/apply`. After signing in a creator lands on
   `/you/profile` and a curator lands on the review queue at `/roster?state=submitted`, unless a
   `next` path was carried, which wins. `next` is honoured only when it is a path on this origin
   beginning with a single `/` and not `//`.
6. `GET /api/me` returns the caller's `email`, `name`, `role`, `verified` and `profile_slug`
   (`null` for an account with no profile). Signing out forgets the token and returns to `/`.

### Divisions, disciplines and addresses

7. `GET /api/site` returns the `headline`, the `mission_line`, the four `divisions` in
   `position` order and the twelve `disciplines` in `position` order. Each division carries
   `slug`, `name`, `colour_token`, `proposition`, `kicker`, `body`, `roster_heading`, `scene` and
   `position`; each discipline carries `slug`, `name` and `position`.
8. The four divisions and their fixed colour tokens:

| Position | Name | Slug and route | `colour_token` |
|---|---|---|---|
| 1 | Creator Media | `creator-media` at `/creator-media` | `red` |
| 2 | Creator Communities | `creator-communities` at `/creator-communities` | `green` |
| 3 | Creator Products | `creator-products` at `/creator-products` | `blue` |
| 4 | Creator Tech | `creator-tech` at `/creator-tech` | `yellow` |

9. There are exactly four divisions and each colour token belongs to exactly one of them. No
   endpoint accepts a colour token, and the colour a division shows everywhere (its menu line,
   its roster card division line, its filter value, its loading line) comes from its token and
   nothing else.
10. The twelve disciplines, in order, as `slug` and name: `analytics` Analytics, `discovery`
    Discovery, `audience-insights` Audience Insights, `presenting` Presenting, `producing`
    Producing, `writing` Writing, `directing` Directing, `design` Design, `community` Community,
    `commerce` Commerce, `partnerships` Partnerships, `engineering` Engineering. A discipline
    name is at most 24 characters so a pill never wraps and never truncates.
11. The public addresses are `/`, the four division routes, `/about`, `/roster`,
    `/creator/<slug>`, `/find`, `/join-us`, `/join-us/apply`, `/verify`, `/sign-in`,
    `/legal/terms-and-conditions`, `/legal/privacy-policy`, `/legal/cookie-policy`,
    `/sitemap.xml` and `/robots.txt`. The signed-in addresses are `/you` and `/you/profile`,
    and the curator's review queue is the roster address `/roster?state=submitted`.
12. The armillary's own rotation is never part of an address and never remembered: `/` always
    opens with the object at rest on its first segment.

### Global chrome

13. The bar is built once and survives every navigation: it is never rebuilt when the route
    changes, so the clock never restarts and the wordmark never flashes. It holds exactly four
    things: the Halden wordmark at the left, the clock in the centre, the menu control at the
    right, and the light and dark toggle at the bottom right of the window.
14. **The wordmark and the menu control are never given a colour.** They are drawn as the
    difference against whatever is behind them, so over the near-black ground they read white,
    over a near-white scene near-black, and over a division colour its complement, at every
    scroll position, in both modes. Where a browser cannot composite them that way, both fall
    back to the text colour over a translucent ground scrim that keeps them readable. The
    wordmark is drawn, carries the accessible name `Halden`, and links to `/`.
15. The clock shows three cities and the current time in each: `L.A` in the Los Angeles zone,
    `LDN` in the London zone and `NYC` in the New York zone, as 24-hour zero-padded times such as
    `07:16`, set between brackets `(` and `)`. The three cities share one slot and cycle through
    it every few seconds with a one-line slide, so the bar never changes width. The cities stay
    those three whatever the reader's locale.
16. The menu control reads `Menu` and becomes `Close` while the menu is open. The two words sit
    one above the other in a clipped box one line tall, and the change slides the pair.
17. The menu overlay lists six links, each as one large line: `About Us`, `Creator Media`,
    `Creator Communities`, `Creator Products`, `Creator Tech` and `Join Us`. Each division link
    carries a line beneath it in that division's own colour, and those four lines are the only
    colour in the navigation. Pointing at a link draws a hand-drawn stroke across it from one end
    to the other. The current route's link is marked with a small dot inside a ring. Escape
    closes the overlay and returns focus to the menu control.
18. The light and dark toggle is the one control that stays above the open menu, so a visitor
    who opens the menu in the wrong mode can switch without closing it. Switching swaps the
    ground and text colours of the whole site over about a second, and the root element carries
    `data-mode="dark"` or `data-mode="light"`. The choice is kept in browser storage under the key
    `mode` and survives a reload. With nothing stored, the mode follows the system colour-scheme
    preference, and only with no preference either does it fall back to dark.
19. The footer, on every route except the front door, carries five items on one line: the
    copyright sign followed by the current UTC year and `Halden`; `Terms & Conditions`, linking to
    `/legal/terms-and-conditions`, with a non-breaking space before `Conditions`; `Privacy
    Policy`, linking to `/legal/privacy-policy`; `Cookies`, linking to `/legal/cookie-policy`;
    and `Site by FORM+FIELD.` with a non-breaking space before the studio name. The front door
    reaches the three legal routes through the menu overlay's own footer line.
20. The consent card appears at the foot of the window on a first visit and reads
    `Select 'Accept All' to agree to our use of cookies and similar technologies to enhance your
    browsing experience, security, analytics and customisation. Review our Cookie Policy here.`
    with `Cookie Policy` linking to `/legal/cookie-policy`, and two controls, `Accept All` and
    `No thanks`. The answer is kept in browser storage under the key `consent` as `accepted` or
    `declined`, and the card does not return once answered. It is the first thing keyboard focus
    reaches while it is showing.
21. The banner is a single line of small capitals at the window's foot, centred, with no ground,
    held for about two seconds and then faded. It carries only transient messages that need no
    answer: `SAVED`, `SENT BACK`, `PUBLISHED`, `TAKEN DOWN`, `MOVED`, `ORDER SAVED`,
    `NOT SAVED`, `ADDRESS CONFIRMED`, `OFFLINE`, `BACK ONLINE`, `REDUCED GRAPHICS`, `LIGHT` and
    `DARK`. Every banner string is at most 24 characters. There is no bell, no badge and no count
    anywhere in the product.
22. **One primary action per page.** Each page carries exactly one primary action, marked on its
    element with `data-primary-action`, and every other control on the page is visibly quieter:
    `About Us` on the front door, `Join us` on each division route and on `/roster` (opening the
    application pre-set to that division on a division route), `Apply` on `/join-us`, `See the
    roster` on a creator profile for a visitor and `Edit this` for its owner, `Sign in` on
    `/sign-in`, `Send` in the application, and the publication control in the editor.

### The command palette

23. The command palette is the first way to reach anything. `Control+K` (or `Command+K` on a Mac)
    opens it from every page, and `/find` opens the front door with the palette already open. It
    is a dialog named `Find` holding one search field and a list that narrows as the visitor
    types. It lists the four divisions, `The roster`, `Join us`, `About us` and every live creator
    by name; for a signed-in creator it also lists `Your profile`, and for a curator `Review
    queue`. Arrow keys move through the list, Enter opens the highlighted entry, and Escape
    closes the palette and returns focus to where it was.
24. The palette never lists a profile that is not live, and its creator entries come from the
    same live roster the public reads.

### The arrival screen and the page transition

25. The site opens on an arrival screen that is the inverse of everything after it: a white
    ground with near-black type. The Halden lettering is drawn in three passes, landing at a
    third, two thirds and completion of loading, while a hand-drawn stroke in the Creator Media
    red draws across a resting grey copy of itself. A counter counts from `0` to `100`.
26. The counter reports real progress against the bytes the front door actually loads, never a
    timed animation: if loading finishes early the counter finishes early, and if it stalls the
    counter stalls. After twenty seconds without completing, the arrival screen offers a control
    reading `Continue without the scene`, which proceeds to the site with the list fallback
    described under the armillary.
27. When loading completes, the white curtain clips away with the near-black site already behind
    it, and the wordmark, clock, menu control and toggle rise into view. While the arrival screen
    is showing the root element carries `data-arrival="loading"`, and once the site is usable it
    carries `data-arrival="done"`. A later navigation inside the site never shows the arrival
    screen again.
28. Choosing a division never produces a white flash, a blank frame or a scroll jump. A curtain
    comes across, the outgoing route's scene hands off to the incoming one, and the curtain lifts.
    The incoming route is scrolled to its top before the curtain lifts, and the bar, the clock and
    the toggle persist throughout.

### The front door and the armillary

29. `/` is exactly one window tall at every window size and never scrolls. It holds the armillary,
    the headline `The Operating System for the Creator Economy` set bottom left, one `About Us`
    pill beneath the headline at the same left edge linking to `/about`, and the navigation
    chrome. It has no picture, no video, no logo wall, no statistic, no sign-up prompt, no
    newsletter box, no second call to action and no heading larger than the headline.
30. The headline is a first-level heading whose accessible name is exactly
    `The Operating System for the Creator Economy` as one string: every character element the
    reveal animation uses is hidden from assistive technology, the containing heading carries the
    whole sentence, and copying it yields the sentence with its spaces. The same holds for every
    split heading on every route.
31. The armillary renders a single, continuously animated three-dimensional object filling the
    window at the screen's pixel density: four concentric rings around a glossy black sphere, the
    outermost ring cut into four arcs with small gaps whose boundaries are the four divisions.
32. The object carries four acquirable segments, one per division, in the order of the division
    positions. An unacquired segment sits slightly smaller and at half strength; the acquired one
    at full size and full strength. The armillary region is one keyboard-focusable element named
    `Halden ecosystem`, and it carries `data-acquired` set to the acquired division's slug, which
    is `creator-media` when the page opens.
33. Dragging anywhere on the front door turns the object with the pointer, and on release it keeps
    a little momentum and settles onto the nearest segment. The wheel turns it too: on a page with
    nothing to scroll a wheel event moves the acquired segment to the next one. The left and right
    arrow keys, and the `Previous division` and `Next division` controls, step it one segment,
    wrapping from the fourth back to the first.
34. When a segment is acquired, that division's name appears beside the object as a link, the
    small ring indicator in the bottom left sweeps to complete, and the name is announced politely
    to assistive technology. Activating the name, or pressing Enter on the focused region, runs the
    page transition into that division's route.
35. While the object loads, it is seen through a strong prismatic dispersion that splits the image
    into spectral fringes which converge as it settles; at rest the dispersion is gone and the
    object is legible.
36. Where three-dimensional rendering is unavailable, or the visitor chose `Continue without the
    scene`, or the scene fails, the front door falls back to the four division names as a list of
    large lines on the near-black ground, each with its coloured line, and the site stays fully
    usable: the region still carries `data-acquired`, the arrow keys and the two controls still
    step the acquired name, and Enter still enters it. The region carries `data-armillary="scene"`
    while the object renders and `data-armillary="fallback"` for the list, and the banner shows
    `REDUCED GRAPHICS` once per session when the scene is dropped.
37. On a narrow viewport, and only there, one line appears beneath the object:
    `Tap a section of our ecosystem to navigate.`

### A division

38. `GET /api/divisions/<slug>` returns one division with every field from `GET /api/site`, its
    `products` (for Creator Tech; an empty list elsewhere) and its `roster`: every live profile in
    that division as a summary, in curated order by default. It accepts `discipline` (a discipline
    slug) and `sort` (`curated`, `newest` or `name`) and nothing else. An unknown slug answers
    `404` with `not_found`.
39. Each division route renders, in order: a first-level heading reading `About us` whose strong
    line is the mission line `Our purpose is to shorten the road back to human.`; the site headline
    again, split, as a section; the division's own name; a `SKETCH MODE` control; the
    proposition; the kicker in uppercase; the body paragraph, held faint until it is revealed; for
    Creator Tech, a block headed `Our tool box` listing its four named products; the roster
    heading; and the roster grid.
40. The divisions' own content:

| Division | Proposition | Kicker | Roster heading |
|---|---|---|---|
| Creator Media | `The new media empires will start with a person.` | `PEOPLE ARE THE PLATFORM` | `The people behind the platform` |
| Creator Communities | `Audiences become communities when somebody gives them a home.` | `BELONGING AT SCALE` | `The people who host them` |
| Creator Products | `The best products start with the people who already use them.` | `MADE WITH CREATORS` | `The people who make them` |
| Creator Tech | `We build the engine that powers the person.` | `ENGINEERING THE ECOSYSTEM` | `The people who build it` |

41. The division bodies are, for Creator Media, `Media influence now organises around individuals.
    We build media brands around creators people choose to belong to.`; for Creator Communities,
    `We build the places where a creator's audience meets itself, and we keep those places worth
    returning to.`; for Creator Products, `We design, make and ship products with creators whose
    audiences asked for them first.`; and for Creator Tech, `We develop proprietary technology to
    replace guesswork with data-driven precision, building the infrastructure that scales human
    creativity.`
42. Creator Tech's `Our tool box` lists four named products, each with its name, its tagline, a
    label reading `About`, up to four discipline pills and a `Visit Site` link that leaves the site
    in a new context: `Signal Desk`, `Less Noise, Better Work.`, pills Analytics and Discovery;
    `Roster Graph`, `See who your audience already follows.`, pills Audience Insights and
    Discovery; `Brief Engine`, `One message in, one brief out.`, pills Writing and Commerce;
    `Payline`, `Paid the day the work is approved.`, pills Commerce and Engineering. Each product
    `url` is `https://www.example.com/` followed by the product name in kebab case.
43. The roster grid shows every live profile in the division as a card: the portrait filling the
    card, the name beneath it, the division line in the division's colour and up to four
    discipline pills. Each card links to `/creator/<slug>` and carries `data-division` set to the
    profile's division slug. Pointing at a card lifts it and fades its overlay in. The grid has
    three columns with the middle column set lower by about half a card.
44. A division route accepts `?discipline=<slug>` to narrow its roster, and when its roster is
    empty it shows the centred notice `Nobody here yet.` / `This part of the ecosystem is being
    built.` / `See the roster`.
45. Behind its content each division route renders its own scene, driven by scroll position and
    never by a timer; the type, the roster and the navigation render and are usable before the
    scene's first frame, and a failed scene leaves the plain ground with the banner `REDUCED
    GRAPHICS`.
46. The menu marks the current division's link as active.

### Sketch mode

47. `SKETCH MODE` on any division route switches the whole site into a hand-drawn register and
    back. It is a document-level state: the root element carries `data-sketch="on"` or
    `data-sketch="off"`, and the choice is kept in browser storage under the key `sketch` and
    survives a reload. It starts `off`.
48. In sketch mode every heading in the display face is re-set in the hand-drawn lettering face,
    every drawn stroke renders at full strength rather than as an underline accent, and each scene
    is replaced by line art in the text colour on the ground, with no material and no reflection.
49. Sketch mode changes what things are drawn with and never where they sit: every layout, gap,
    type step and every piece of text is identical in both states. A sketch mode that cannot start
    refuses and leaves the site as it was.

### The roster

50. `GET /api/profiles` returns `{"total", "page", "items"}`: `items` is at most 24 live profile
    summaries for the requested page and `total` counts every match. It accepts `division` (a
    division slug or `all`), `discipline` (a discipline slug or `all`), `q` (free text), `sort`
    (`curated`, `newest` or `name`) and `page` (a positive integer, default `1`), plus `state` for
    a curator only.
51. A profile summary carries `slug`, `name`, `division` (the slug), `division_name`,
    `colour_token`, `disciplines` (an ordered list of `slug` and `name`), `portrait_url` and
    `position`.
52. **Public reads list exactly the live profiles.** For a visitor or a creator, `GET
    /api/profiles`, every division roster, the palette and the sitemap include a profile if and
    only if it is live, and always show its live copy. A `state` parameter from anybody who is not a
    curator is silently dropped and the live roster is answered, never an error.
53. Filters intersect and never union: `division` with `discipline` answers the people in that
    division with that discipline; `discipline` with `q` answers the people with that discipline
    whose text matches. A combination that matches nobody answers `total` `0` and an empty `items`.
54. `q` matches case-insensitively and accent-insensitively as a substring of the `name`, the
    `statement` and every credit line; below two characters it is ignored, and above 60 it is
    refused with `400`. Results rank a name prefix first, then a name substring, then a discipline
    name, then a statement match, then a credit match.
55. `curated` sorts by `position` ascending and is the default everywhere, because a holding
    company's roster is an editorial statement and the order is part of what it says; `newest` sorts
    by `published_at` descending; `name` sorts alphabetically by name, accent-insensitive and ignoring
    case.
56. For a curator, `state` narrows the list to profiles in that state, live or not, and
    `state=submitted` is the review queue.
57. The `/roster` page carries the heading `The roster`, a count line reading `<n> people`, a
    filter row and the grid. The filter row shows `division` (on the roster only), `discipline`,
    `sort` at the right, and `state` for a curator only; each filter is a grey label followed by its
    value in the text colour, and a selected division's value takes that division's colour. Every
    filter lives in the address: `/roster?division=creator-media`,
    `/roster?discipline=<slug>`, `/roster?division=creator-media&discipline=<slug>`,
    `/roster?q=<text>&sort=name`. A parameter at its default is left out of the address, and
    changing a filter replaces the history entry rather than adding one.
58. The search field on `/roster` settles for a moment after the last keystroke before it runs,
    rather than running on every keystroke, and a matched run of text is shown in a heavier weight,
    never in a colour.
59. A roster card on `/roster` carries the portrait, the name, the division name in uppercase in
    its division's colour and up to four pills, and is the only place in the product where all four
    division colours can appear at once. Scrolling past the last row loads the next page.
60. With no live profile at all the roster shows `Nobody yet.` / `The roster is being built.` /
    `Join us`; with filters that match nobody it shows `Nothing here.` / `No one matches that.` /
    `Clear filters`, and `Clear filters` resets every parameter at once and returns to `/roster`.

### A creator profile

61. `GET /api/profiles/<slug>` returns one live profile's full shape: every summary field plus
    `statement`, `links` (an ordered list of `kind`, `label` and `url`), `credits` (an ordered list
    of strings), `published_at` and `updated_at`. A slug that does not exist, or names a profile
    that is not live, answers `404` with `not_found`, identically for both, for every caller.
62. `/creator/<slug>` shows, in order, the portrait across the content column, the name set large
    in the display face, the division name in its colour linking to
    `/roster?division=<division-slug>`, the discipline pills each linking to
    `/roster?discipline=<slug>`, the statement, one row of links each beside its mark, and the
    credits one per line.
63. Link kinds map to fixed marks so a roster reads consistently, and a sixth kind is never added:
    `site` a globe, `photo` a camera, `network` a professional-network mark, `social` a short-form
    social mark, `audio` an audio mark, `document` a document mark. Every link leaves the site in a
    new context.
64. A portrait that has not loaded, or cannot, is replaced by a generated still keyed by the
    profile's slug: the profile's own division object, seen from an angle taken from the slug,
    with the person's initials centred on it in the display face. The public never sees a broken
    image.
65. An unknown or not-live slug renders `Not here.` / `This profile is not published, or it never
    was.` / `See the roster`.
66. The profile's owner sees an `Edit this` control that opens `/you/profile`. While the profile is
    `changes_requested`, the curator's note is pinned above the name for its owner in full size,
    with its label `Changes requested` in the error colour. A curator viewing a live profile sees
    `Take down` and a `Move to` choice of the other three divisions.

### Join us and the application

67. `/join-us` is the recruitment route, one window tall on a desktop, and carries the heading
    `Join us`, the statement `Halden backs people who make things for a living. Tell us who you are and where you fit, and the studio will read every word.`, one
    row of four controls, one per division in its own colour, each opening the application pre-set
    to that division, and one `Apply` pill. A signed-in creator sees `Edit your profile` in place of
    `Apply`, opening the editor.
68. **The application is a slide-over.** `/join-us/apply` shows the join-us page with the
    application panel slid over it from the side, and `/join-us/apply?division=<slug>` opens it with
    the division chosen. Closing the panel, or Escape, returns to `/join-us` and keeps what was
    typed.
69. The application's fields and labels are `Your address` (`email`), `Choose a password`
    (`password`), `Your name` (`name`), `Where do you fit` (`division`), `What do you do`
    (`disciplines`, one to four pills), `Tell us what you do` (`statement`), `Where can we see it`
    (`links`, at least one kind, label and address) and the consent box `You may keep my details to
    reply.` (`consent`). The submit reads `Send`.
70. `POST /api/applications` takes `email`, `password`, `name`, `division`, `disciplines` (a list
    of discipline slugs), `statement`, `links` (a list of `kind`, `label`, `url`) and `consent`. On
    success it answers `201` with `account` (`email`, `name`, `role`, `verified`) and `profile`
    (`slug`, `state`), and it creates one `creator` account with an unconfirmed address and one
    profile in state `applying` owned by that account, carrying the fields the application sent.
71. An application that fails validation answers `400` with `validation_failed`, a `fields` map of
    every field at fault to its message, and creates nothing: no account, no profile, no mail. The
    field rules and messages:

| Field | Rule | Message |
|---|---|---|
| `email` | required, one `@` with a dot after it, at most 254 characters | `That address does not look right.` |
| `password` | required, 12 to 128 characters | `Passwords are at least twelve characters.` |
| `name` | required, 2 to 60 characters | `Give us your name.` |
| `division` | one of the four division slugs | `Pick a part of the ecosystem.` |
| `disciplines` | one to four slugs, all from the vocabulary | `Pick between one and four.` |
| `statement` | required, 80 to 400 characters | `Eighty characters at least. Tell us what you do.` |
| `links` | at least one; each a known kind, a label of 2 to 40 characters and an `https` address | `Give us one place to see your work.` |
| `consent` | must be true | `We need this to be able to reply.` |

72. **One email, one account.** An application whose email already has an account answers `409`
    with `conflict` and the message `That address already has an account.`, the form offers a
    `Sign in` link, and nothing is created. Emails are compared case-insensitively. Two
    applications with the same email arriving at the same instant produce exactly one account and
    exactly one profile; the other is refused with `409`.
73. A successful application replaces the whole panel with a full-page confirmation reading
    `Check your email.` and `We have sent you a link. Open it and finish your entry.` The typed
    values are kept in browser storage under the key `application_draft` until the application
    succeeds, restored if the page reloads first, and cleared on success.
74. **The slug.** A profile's `slug` is derived from its name when the profile is created:
    lowercase, every run of characters that are not letters or digits replaced by a single hyphen,
    hyphens trimmed from both ends, then `-2`, `-3` and so on appended until it is unique. While a
    profile has never been live its slug follows its name; once it has been live its slug never
    changes again. No request may set a slug.

### Confirming the address

75. A successful application sends one mail to the applicant with the subject
    `Confirm your address`, whose body opens with the confirmation link
    `<APP_PUBLIC_URL>/verify?token=<token>` on its own line and names the applicant. The token is
    single use and expires seven days after it is issued.
76. `/verify?token=<token>` confirms the address through `POST /api/accounts/verifications` with
    `token`, which answers `204`, sets the account's confirmation time and moves a profile in state
    `applying` to `draft`. The page then opens `/you/profile` (through sign in when there is no
    session) with the banner `ADDRESS CONFIRMED`.
77. An unknown token answers `400` with `validation_failed`, and a token already used or past its
    expiry answers `410`; neither changes anything, and the page shows `That link no longer works.` /
    `Sign in to carry on, or apply again.` / `Sign in`.
78. A creator whose address is not confirmed can sign in and edit their own profile, and cannot
    submit it.

### The profile editor

79. `GET /api/me/profile` returns the caller's own profile at any state: `slug`, `state`,
    `is_live`, `version`, `name`, `division`, `disciplines`, `statement`, `portrait_url`, `links`,
    `credits`, `pending` (the held edit to a live profile, or `null`), `return_note`,
    `submitted_at`, `published_at` and `returned_at`. An account with no profile answers `404`.
80. `PATCH /api/me/profile` takes any of `name`, `statement`, `portrait_url` and `division`, plus
    the `version` the caller last read, and answers the updated profile with its new `version`.
    `PUT /api/me/profile/disciplines` takes the complete ordered `disciplines` list of slugs,
    `PUT /api/me/profile/links` the complete ordered `links` list, and `PUT /api/me/profile/credits`
    the complete ordered `credits` list, each with `version`. A list is always replaced whole;
    no route accepts a single move.
81. Every write carries `version`, and `version` increases by one on every successful write. A
    write whose `version` is older than the stored one is refused with `409` and
    `version_conflict`, changes nothing, and the editor fetches the whole profile again.
82. Saved values follow the same rules as the application, and a field that breaks one is refused
    with `400`, `validation_failed` and its message, and is not stored: `name` 2 to 60,
    `statement` at most 400, `division` one of four, `disciplines` one to four from the vocabulary,
    each link a known kind with a 2 to 40 character label and an `https` address of at most 2048
    characters (any other scheme, a script scheme included, is refused with
    `That link does not look right.`), at most five links, each credit 2 to 80 characters
    (`Credit <n> is too long.`), at most eight credits. `portrait_url` must be an `https` address
    beginning `https://media.example.com/portraits/`; any other address is refused with
    `We need a picture.` The server never fetches a link or portrait address.
83. While the profile is `submitted`, every editor write is refused with `422` and
    `state_not_allowed`, and the editor is read-only.
84. `/you/profile` is a split view: the field column on one side and a live preview of the public
    profile on the other, updating as the creator types. The fields are grouped as Identity (name,
    division, disciplines), Words (statement), Picture (the portrait address), Links (up to five,
    each a kind, a label and an address), Credits (up to eight lines) and Publication (the state and
    the publication control). Adding a link opens a small slide-over holding its three fields.
85. **Every field saves on blur; there is no save control anywhere.** A save reports through the
    banner `SAVED`. A field that fails to save keeps its value, marks its label in the error colour,
    tries again twice on its own, and then shows `Not saved. Your text is safe here.` and blocks
    submission until it saves. Adding or removing a discipline pill updates at once and, if the
    save fails, the pill returns to its previous state with the banner `NOT SAVED`.
86. The editor keeps unsaved typed values in browser storage until they save, so a reload or a
    dropped connection loses nothing. When the session has expired, the sign in layer opens over the
    editor with the typed text still visible behind it, and signing back in completes the save.
87. `/you` shows the creator's entry at a glance: the profile as the public sees it, its state in
    words (`Applying`, `Draft`, `With the studio`, `Changes requested`, `Live`, `Taken down`), and
    links to the editor and, when live, the public profile.

### Submitting for review

88. The publication control reads `Submit for review` while the profile is `draft` or
    `changes_requested`. `POST /api/me/profile/transitions` with `to` `submitted` and `version`
    moves the profile to `submitted` and sets `submitted_at`, once every rule below holds.
89. A creator whose address is not confirmed is refused with `403`, `not_verified` and
    `Confirm your address first.`, and nothing changes.
90. Submission checks all ten rules at once and, when any fails, answers `422` with
    `validation_failed`, a `fields` map naming every failing field, and `meta.placeholder_fields`
    listing every field that tripped the placeholder rule; nothing changes state, and the editor
    shows every failure as a numbered list.

| # | Rule | Message |
|---|---|---|
| 1 | the address is confirmed | `Confirm your address first.` |
| 2 | `name` is 2 to 60 characters | `Give us your name.` |
| 3 | `division` is one of the four | `Pick a part of the ecosystem.` |
| 4 | one to four disciplines, all from the vocabulary | `Pick between one and four.` |
| 5 | `statement` is 80 to 400 characters | `Eighty characters at least. Tell us what you do.` |
| 6 | `portrait_url` is set under `https://media.example.com/portraits/` | `We need a picture.` |
| 7 | at least one link, each with a kind and a valid address | `Give us one place to see your work.` |
| 8 | every credit line is 2 to 80 characters | `Credit <n> is too long.` |
| 9 | no field is a placeholder | `Something in there is still a placeholder.` |
| 10 | the slug is unique | `Somebody already has that address.` |

91. **The placeholder rule is the one this product exists for.** A field is a placeholder when it
    is empty, when it consists only of punctuation and spaces, or when it contains any of the
    authoring placeholders `INSERT NAME`, `Pill Text` or `Lorem ipsum` anywhere, or `TODO` or `TBD`
    as a whole word, compared without regard to case. The rule applies to `name`, `statement`, every
    link label and every credit line. A profile tripping it cannot be submitted, and no live profile
    ever matches it.
92. A successful submission replaces the editor with a full-page confirmation reading
    `WITH THE STUDIO` and `A curator reads every entry before it goes live.`, with a link
    `See your entry` to `/you`. The publication control then stays unavailable and reads
    `WITH THE STUDIO` until the studio answers. Submitting sends no mail to anybody.
93. A creator may only move their own profile from `draft` to `submitted`, from
    `changes_requested` to `submitted`, and the two live-copy moves below; any other `to` answers
    `422` with `state_not_allowed`.

### The review queue

94. For a curator, `/roster?state=submitted` is the review queue, a split view: the list of
    submitted profiles on one side, oldest submission first, each with its name, its division in
    colour and how long ago it arrived; and on the other side the selected profile exactly as the
    public will see it once published, with its pending changes applied, and two controls,
    `PUBLISH` and `SEND BACK`. With nothing waiting it shows `Nothing waiting.` /
    `Nobody has sent anything in.` / `See the roster`. The queue is read when it is opened.
95. `POST /api/profiles/<slug>/transitions` is the curator's route: `to` with `version`, and a
    `note` when sending back. A creator or any non-curator calling it is refused with `403` and
    `not_authorised`; an anonymous call with `401` and `not_authenticated`; an unknown slug with
    `404`.
96. **Publish.** `to` `published` on a `submitted` profile makes it live at once, with no rebuild
    and no cache to clear: its pending changes, if any, are copied over the live copy and cleared,
    `state` becomes `published`, `is_live` becomes true, `reviewed_by` records the curator, and
    `published_at` is set the first time it goes live and never changes after. A profile going live
    for the first time takes the next curated position after every live profile. The banner reads
    `PUBLISHED`.
97. **Send back.** `SEND BACK` opens a slide-over holding one `Note` field and a `Send back` control.
    `to` `changes_requested` with a `note` of 10 to 500 characters stores the note as `return_note`,
    sets `returned_at` and moves the profile to `changes_requested`; the card leaves the queue and
    the banner reads `SENT BACK`. A missing, shorter or longer note is refused with `400`,
    `validation_failed` and `Say what needs changing.`, and nothing changes. A profile sent back
    while live stays live with its live copy.
98. **Take down.** `to` `unpublished` on a `published` profile removes it from every public
    surface at once: `is_live` becomes false and `state` becomes `unpublished`. When its owner next
    edits it, the profile returns to `draft`. The banner reads `TAKEN DOWN`, and a division left
    with no live profile shows its empty notice.
99. Any other transition, such as publishing a `draft`, answers `422` with `state_not_allowed`.
    Two curators publishing the same profile with the same `version` produce one publication; the
    second is refused with `409` and `version_conflict`, and its queue card is removed with the
    banner-free line `Already handled.`
100. **Move between divisions.** `PATCH /api/profiles/<slug>` with `division` and `version` moves
     a profile to another division at once, live copy included, records a `moved` event, and the
     banner reads `MOVED`. The same route refuses any other field (`name`, `statement`,
     `portrait_url`, `disciplines`, `links` or `credits`) with `403` and `not_authorised` and
     changes nothing: the studio decides where somebody belongs and never touches a word they wrote.
101. **Curated order.** `PUT /api/studio/roster-order` takes `slugs`, the complete list of live
     profile slugs in their new order, and sets `position` to match, starting at `1`. A list that
     leaves out a live profile, names one twice, or names one that is not live is refused with
     `400` and `validation_failed`, and nothing changes. On `/roster` a curator reorders cards with a
     `Reorder` mode, by dragging or by the keyboard, and the banner reads `ORDER SAVED`.

### Rewriting a live profile

102. **A live profile stays live while its owner edits it.** When the owner saves any field or list
     of a profile that is live, the change is written to `pending` alongside the live copy; `state`
     stays as it was, every public surface keeps showing the live copy, and the editor and its
     preview show the pending version.
103. When the pending change leaves the division unchanged, the publication control reads
     `Publish changes`. `POST /api/me/profile/transitions` with `to` `published` checks rules 2 to 10,
     copies the pending change over the live copy, clears `pending`, sets `updated_at` and leaves
     `published_at` unchanged, without a second review and without mail. The editor is replaced by a
     full-page confirmation reading `PUBLISHED` and `Your changes are on the roster now.`, with a link
     `See your profile` to `/creator/<slug>`.
104. Publishing when there is nothing pending answers `422` with `state_not_allowed`.
105. If the live copy changed underneath the pending change, the editor shows the two side by side
     and the owner chooses; neither is discarded until they do.

### Moving to a different division

106. **A division change goes back through the studio.** When the pending change moves the profile
     to a different division, the publication control reads `Send changes for review` instead, and
     `to` `published` from the owner is refused with `422` and `state_not_allowed`.
     `POST /api/me/profile/transitions` with `to` `submitted` moves the profile to `submitted` with its
     pending change intact, shows the `WITH THE STUDIO` confirmation, and the profile stays live on its
     old division with its live copy until the studio answers.
107. When a curator publishes it, the pending change is copied over the live copy: the profile
     leaves the old division's route and roster and appears on the new one's, its roster card shows
     the new division's name and colour, a `moved` event records both divisions, `/creator/<slug>`
     shows the rewritten profile, and a fresh visitor with no session sees all of that at once.

### Mail

108. Notifications are deliberately few: the banner, the inline notice and the pinned note are the
     only in-app surfaces, and transactional mail is limited to the four messages below. The app sends
     mail over SMTP at `SMTP_HOST` and `SMTP_PORT` from `roster@example.com`, as plain
     text, each message addressed to one owner's account email with no cc and no bcc, and each
     naming the profile. Exactly four kinds exist:

| Trigger | Subject | Body |
|---|---|---|
| an application succeeds | `Confirm your address` | opens with the confirmation link on its own line, names the applicant |
| a curator sends a profile back | `Your entry needs a change` | names the profile and carries the curator's note in full |
| a curator publishes a profile (first time or reviewed changes) | `You are on the roster` | names the profile and carries `<APP_PUBLIC_URL>/creator/<slug>` |
| a curator takes a profile down | `Your entry has been taken down` | names the profile |

109. Nothing else sends mail: not a submission, not a field save, not an owner publishing their own
     changes, not a curator moving or reordering a profile, and nothing ever goes to a curator. A
     seeded example profile with no account sends nothing. No message carries a password or a token
     other than the confirmation token.

### About, legal notices, sitemap and robots

110. `/about` carries the heading `About us`, the mission line, the site headline, and the four
     divisions as links to their routes, each with its proposition.
111. `GET /api/notices/<kind>` with `kind` `terms`, `privacy` or `cookies` returns `kind`, `title`,
     `body` and `updated_at`; none of the three bodies is ever empty. The **terms** page lives at
     `/legal/terms-and-conditions` with the title `Terms & Conditions`, the privacy notice at
     `/legal/privacy-policy` titled `Privacy Policy`, and the cookie notice at
     `/legal/cookie-policy` titled `Cookies`. Each page shows its title, a last-updated line, a
     contents list of its sections, and the body. The privacy and cookie notices describe the site
     events recorded after consent and the consent card's two choices.
112. `/sitemap.xml` is an XML sitemap listing the absolute address of `/`, the four division
     routes, `/about`, `/roster`, `/join-us`, the three legal routes, and `/creator/<slug>` for
     every live profile and for no other profile. It changes as soon as a profile goes live, is
     taken down or moves.
113. `/robots.txt` allows the public site, disallows `/you`, `/sign-in` and `/api/`, and names the
     sitemap on a line reading `Sitemap: <APP_PUBLIC_URL>/sitemap.xml`.

### Consent and site events

114. `POST /api/events` takes `name` and `properties` and answers `204`, recording the event.
     `name` is one of `site_opened`, `division_entered`, `roster_filtered`, `profile_opened`,
     `apply_submitted`, `profile_submitted`, `profile_published`, `profile_moved`, `mode_toggled`
     and `sketch_toggled`; any other name is refused with `400`. `properties` carries only
     division slugs, counts, lengths banded into ranges and the chosen mode, never a name, an email
     address, a statement, a note, a link address or an account identifier.
115. The browser sends no event at all before the consent card is answered. After `Accept All` it
     sends the events above as they happen. After `No thanks` it sends, queues and keeps nothing,
     on that visit and every later one.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/` | the front door and the armillary | none |
| `/creator-media`, `/creator-communities`, `/creator-products`, `/creator-tech` | a division and its roster | none |
| `/about` | the company, its mission and its four divisions | none |
| `/roster` | every live profile, filterable, sortable, searchable | none |
| `/roster?state=submitted` | the review queue | `curator` (anybody else sees the live roster) |
| `/creator/<slug>` | one live profile | none |
| `/find` | the front door with the command palette open | none |
| `/join-us` | joining, with the four division controls | none |
| `/join-us/apply` | the application slide-over | none |
| `/verify` | confirming an address from its link | none |
| `/sign-in` | the sign in layer | none |
| `/you` | the creator's own entry at a glance | `creator` |
| `/you/profile` | the profile editor and its live preview | `creator` |
| `/legal/terms-and-conditions`, `/legal/privacy-policy`, `/legal/cookie-policy` | the three notices | none |
| `/sitemap.xml`, `/robots.txt` | discovery files | none |

### Entry and redirects

1. A signed-out visitor opening `/you` or `/you/profile` is sent to `/sign-in?next=<path>` and,
   after signing in, returns to the address they asked for.
2. A curator opening `/you` or `/you/profile` sees the surface `Not for you` / `This part of the
   site belongs to the people on the roster. The roster itself is open to everybody.` /
   `See the roster`.
3. A creator or a visitor opening `/roster?state=submitted` sees the live roster with the `state`
   filter dropped, never an error and never a denial.
4. A session that expires in the middle of an edit opens the sign in layer over the editor with
   the text still visible behind it; signing back in finishes the save.
5. Opening `/join-us/apply` while signed in as a creator who already has a profile opens
   `/you/profile` instead.
6. An unknown address renders `Not here.` / `Nothing lives at this address.` / `See the roster`.

### Journeys

1. **Enter through the armillary.** Open `/`. Watch the arrival counter reach `100` and the white
   curtain clip away. Press the right arrow once and read `Creator Communities` beside the object,
   press it three more times and read `Creator Media` again, press Enter, and land on
   `/creator-media` without a white flash. Scroll to `The people behind the platform` and read the
   first card, `Juno Okafor`.
2. **Read a person.** From the Creator Media roster open `Juno Okafor`, read the statement, follow
   the division name to `/roster?division=creator-media`, clear the filter, filter to the
   discipline `Partnerships`, read `Nothing here.`, press `Clear filters`, and search `night trains`
   to find `Amara Voss`.
3. **Find anything.** Press `Control+K` on any page, type `mara`, and open `Mara Oyelaran`.
4. **Apply.** Open `/join-us`, press the Creator Media control, and the application slides over
   with `Where do you fit` set to Creator Media. Press `Send` empty and read every field message.
   Fill every field and press `Send`, and read `Check your email.` Open the confirmation link from
   the mail and land in the editor with `ADDRESS CONFIRMED`.
5. **Draft and submit.** Open the palette, choose `Your profile`, set the statement to
   `** INSERT NAME ** writes here.`, press `Submit for review` and read the numbered list with
   `Something in there is still a placeholder.` Replace the statement with real words, add a
   portrait address and a link, press `Submit for review`, and read `WITH THE STUDIO`.
6. **Review.** Sign in as `curator@example.com`, land on the review queue, select the new entry,
   press `SEND BACK`, write a note in the slide-over and send it, and read `SENT BACK`. As the
   creator, open the profile and read the pinned note under `Changes requested`, change the
   statement and submit again. As the curator, press `PUBLISH` and read `PUBLISHED`.
7. **See it live.** In a fresh browser with no session, open `/creator-media` and find the new name
   on the roster, then open its profile and read the statement.
8. **Rewrite.** As the creator published in journey 6, open `/you/profile`, change the statement
   and leave the field, read `SAVED`, and confirm in the fresh browser that the profile still shows
   the old statement. Press `Publish changes`, read `PUBLISHED`, and reload the fresh browser to read
   the new statement.
9. **Move.** As the same creator, change the division to Creator Communities, press
   `Send changes for review`, and read `WITH THE STUDIO`. As the curator, publish it. In the fresh
   browser, `/creator-communities` lists the creator, `/creator-media` does not, and the roster card
   reads `CREATOR COMMUNITIES` in the Creator Communities colour.
10. **Choose how it looks.** Switch to light mode from the toggle while the menu is open, reload and
    stay in light mode; on a division route turn on `SKETCH MODE`, reload, and read the same
    proposition drawn by hand.

### States

1. Every collection has four faces besides its normal one: loading, empty, error and offline, each
   written out in the front-end specification. Loading keeps the space the content will take so
   nothing jumps, and never shimmers or pulses.
2. An empty or failed collection shows one centred notice: a heading, one line of explanation and at
   most one control. No illustration, and never a status code or an error token.
3. A form that is refused keeps every value the person entered, marks each field at fault with its
   message beneath it, and moves focus to the first. A form-level refusal shows one line above the
   submit. A network failure shows `That did not send. Your text is safe here.` and leaves the
   submit live.
4. A submit control is unavailable only while its request is in flight, never because the form is
   incomplete: pressing it on an incomplete form is how somebody asks what is missing.
5. Validation never runs on a keystroke. It runs when a field has been left non-empty once, on every
   submit for every field, and always again on the server.
6. With the connection lost the banner reads `OFFLINE`, what was already fetched stays readable, the
   editor and the application stay writable and keep their values, and `BACK ONLINE` follows when it
   returns.

## UI/UX notes

**The north star.** Somebody arriving should understand within the first screen that this company
is four businesses serving people who make things for a living, and that turning the object in
front of them is how they choose one; once inside, the people are the point.

**The register.** The public site is consumer and editorial, carrying atmosphere and a point of
view, with the object and the people always the first thing seen. The editor and the review queue
are working tools that wear the same type, ground and spacing, quiet and built for repeated use,
with no hero and no decoration.

**Palette by role.** The ground is a near-black neutral on every route, and the text of headings and
strong lines is white. One mid neutral grey carries almost every sentence a visitor actually reads,
more than the ground and the white together, so a build that sets body copy in white is wrong on
every page at once. A lighter neutral marks hairlines; a darker neutral is only for a field's resting
underline, a skeleton block and an unavailable control, and is never used for readable text. Four
colours exist and each belongs to exactly one division: a light, vivid red for Creator Media, a mid,
soft green for Creator Communities, a light, vivid blue for Creator Products and a light, vivid amber
yellow for Creator Tech. They appear on a division's menu line, its roster card division line, its
filter value, its loading line and its application control, and nowhere else. A soft green that
means a form was accepted and a red mixed back toward the ground that means a form was refused are the
only other colours, and neither is used for anything else. The arrival screen is the one inversion:
white ground, near-black type. The exact shades are yours, so long as the grey stays the reading
colour and no fifth accent ever appears.

**Mode.** Light and dark are both designed, and neither is a filter over the other. Switching swaps
the ground and text roles and every grey inverts with them, so each surface is legible in both modes
and every contrast relationship holds in both. The division colours do not change between modes.

**Type.** Two faces do two jobs. A condensed display face, set in capitals, carries the headline,
every division title and every large figure; a grotesk at a light, a regular and a bold weight carries
every sentence, label and control. A third, hand-drawn face exists only for sketch mode. Every type
step slides continuously with the window width between a small screen and a wide one, and no
breakpoint changes a type step. The headline is the largest type on the front door, and a matched
search run is shown by weight, never by colour. Every face has a fallback of matching proportions and
the first paint never waits for a face to arrive.

**Shape and depth.** Elevation, radius and rules are almost absent. There is no shadow and no border
anywhere: every edge is a change of colour or a
line somebody drew. Every control is a pill; the consent card and the toggle's track are the only
other rounded surfaces. A field is an underline, never a box. Space separates blocks, gaps are
multiples of one base unit that also slides with the window, and a larger gap separates one block
from the next than separates rows within a block.

**Components.** One main pill style and one quieter one. Pointing at a pill grows a filled ellipse
outward from its centre until it fills the pill, and the label crosses from light to dark as the fill
passes it; it is never a background sliding in from an edge. Every control has resting, pointed-at,
pressed, focused, pending and unavailable states; pending replaces the label with a small turning
ring, and unavailable is never signalled by colour alone. Escape closes the menu, the palette, a
slide-over and the sign in layer.

**Motion.** Motion is the one loud gesture, and it must be deliberate. Every heading is split into
lines and each line rises into a clipped box from one line-height below, a twentieth of a second after
the one above, up to six lines; nothing on the site fades in flat. Two curves exist: a sharp-leaving,
long-settling one for anything the pointer caused, and a symmetric ease for anything the page caused.
Nearly every movement shares one slightly unround duration of about three quarters of a second; a
control's colour change takes about a third of a second, the mode swap about a second, and the arrival
exit and the indicator sweep about a second and a half. A link's text changes colour faster than the
mark beside it, so the two deliberately do not arrive together. The hand-drawn strokes are drawn from
one end to the other, never faded. Scroll-driven movement tracks the scroll and never animates on its
own. Under a reduced-motion preference every one of these moments keeps a substitute that arrives
without travelling: lines appear at rest with no stagger, strokes appear complete, the curtain is
skipped, the armillary steps one segment at a time instead of turning, and the scenes hold still.
Nothing becomes unreachable.

**Accessibility.** Text contrast meets WCAG AA for its size in both modes, measured per colour pair
rather than by eye; the four division colours each meet it as text against the ground. Every split
heading exposes its whole sentence as one accessible name. Full keyboard navigation reaches every
control in visual order, including the armillary as one focusable region stepped by the arrow keys,
and focus is visibly outlined in the text colour in both modes, including over the inverting wordmark
and menu control. No interactive target is smaller than 44 CSS pixels in either direction, so the
small bar controls are padded out to that size. Each route has one first-level heading; the bar is a
banner landmark, the menu a navigation landmark, the route content a main landmark and the footer a
content-info landmark. Focus is held inside an open menu, palette, slide-over or sign in layer and
returns to its opener when it closes. The scenes are decorative and hidden from assistive technology.
The document reflows at twice the zoom with nothing scrolling sideways.

**Responsive.** The layout holds at every viewport width between a phone and a wide monitor, across
four ranges: narrow, mid, wide and full. The front door is exactly one window tall at every width and
never becomes scrollable; on a narrow viewport the armillary sits smaller and higher with the headline
beneath it and the instruction line below, and nothing on any route scrolls sideways at any width. The
roster grid runs three columns with the middle one lower on a wide screen, two with the second lower
on a mid screen and one with no offset on a narrow one, keeping the offset wherever there is more than
one column. On a narrow viewport the clock moves into the menu overlay, the toggle moves into the menu
overlay, and the menu links stack without their sketch lines. The armillary is never hidden or
replaced by a still because of window size. Where each range begins is yours, so long as the front door
stays one window tall across all of them.

**What it must not look like.** No page dominated by a single colour family with no second signal, no
drop shadows, no bordered cards or boxed fields, no stock imagery or fetched artwork standing in for
the object and the people, no generic dashboard composition in the editor or the review queue, and no
heading that simply fades in.

## Technical requirements

- **Rendering model.** A single-page application talking to a JSON API. The browser receives one
  application shell and the built front-end bundle, and every route renders in the browser from API
  data. `/sitemap.xml` and `/robots.txt` are answered by the server as files.
- **Front end.** React, built with Vite as a production bundle and served from the app's own origin.
- **Back end.** FastAPI, served by Uvicorn, on the same origin as the front end, with the API under
  `/api`. The FastAPI app serves the built bundle, the shell, `/sitemap.xml` and `/robots.txt`.
- **Database.** PostgreSQL, reachable at `DATABASE_URL`, already running. Use psycopg to reach it.
- **Mail.** Mailpit, a real SMTP server reachable at `SMTP_HOST` and `SMTP_PORT` with `SMTP_USER`
  and `SMTP_PASS` (both empty), already running. Send with the Python standard library's SMTP client.
- **Auth.** Email and password. Passwords are hashed with bcrypt. A successful sign in returns a
  bearer token signed with PyJWT, sent as `Authorization: Bearer <token>`, valid for 12 hours.
- **Health.** `GET /api/health` answers `200` once the app can reach both the database and the mail
  server, and its body reports the database and the mail server separately.
- **Logging.** One line per request to standard output carrying the method, the path, the status and
  the duration, and never a password, a token, a statement or an email address.
- **Errors.** Every error answers JSON shaped `{"error", "message", "fields", "meta", "retry_after"}`:
  `error` is one of `validation_failed`, `not_authenticated`, `not_authorised`, `not_verified`,
  `not_found`, `conflict`, `version_conflict`, `state_not_allowed`, `rate_limited` and `server_error`
  and is never shown to a person; `message` is the form-level copy; `fields` maps each field at fault
  to its message; `meta` carries route extras such as `placeholder_fields`; `retry_after` is a number
  of seconds on a `429` and `null` otherwise. An invalid or unauthorized call is never answered as a
  server error or a silent success.
- **Integrity.** A failed operation leaves no partial state: a refused application writes neither an
  account nor a profile, a refused save stores no field, and a refused transition leaves the state and
  the live copy as they were.
- **One email, one account.** Two applications with the same email arriving at the same instant
  produce exactly one account and exactly one profile; the other is refused with `409`. This holds
  under real concurrency, and so does slug uniqueness: two profiles named alike at the same instant
  never share a slug.
- **Versions.** Every profile write carries the `version` last read, and a stale version is refused
  with `409`; two writers never silently overwrite each other.
- **Input.** Every text value is trimmed, stripped of control characters, length-checked and stored
  as text, never as markup, and every string is escaped where it is rendered, so markup typed into a
  name shows as visible text. Link and portrait addresses must parse with an `https` scheme and are
  never fetched by the server.
- **Transport and headers.** Every response carries `X-Frame-Options: DENY`,
  `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin` and a
  `Strict-Transport-Security` header whose value includes `includeSubDomains`, so the site is never
  framed, never sniffed and asks for a strict secure transport including subdomains.
- **Abuse the design invites.** A roster entry is a public claim about a person, so nothing becomes
  public until a curator publishes it and an application carries at least one link the studio can
  check; the application hands strangers a way to write into the studio's queue, so every value is
  plain text and no address an applicant supplies is ever fetched by the server; and repeated sign-in
  failures are limited as stated under Sign in.
- **Times and formatting.** Stored and returned in UTC as ISO 8601. Absolute dates display as day,
  month name and year, relative times as `just now`, whole minutes, hours or days, and counts are
  grouped by thousands.
- **No secrets in the browser.** No database address, signing secret or mail credential appears in
  anything the browser downloads.

Use only the libraries named here plus their direct dependencies, and whatever the front end needs to
render three-dimensional scenes and split headings. Do not introduce a second database, cache, queue,
object store, identity provider or mail vendor. The only backing services available in this
environment are PostgreSQL and Mailpit, and reaching for anything else is a contract violation.

## Data model

Eleven tables, the entities behind every surface. All timestamps are UTC. Persistence is the
database alone: browser storage holds only conveniences (`mode`, `sketch`, `consent`,
`application_draft` and unsaved editor values), read defensively so a missing, unreadable or
malformed key resolves to the default without an error, and a private window with storage blocked
renders the whole site in its default mode with sketch mode off. Schema migration is forward-only
and applied before the code that needs it.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

### `accounts`

`id`, `email` (unique, stored lowercase), `name`, `password_hash`, `role` (`creator` or `curator`),
`email_verified_at` (null until the address is confirmed), `created_at`, `updated_at`. Two
simultaneous applications with one email leave exactly one row.

### `verification_tokens`

`id`, `account_id`, `token_hash`, `expires_at` (seven days after issue), `used_at` (null until used),
`created_at`. A token is used at most once.

### `divisions`

`id`, `slug` (unique, never changes), `name`, `colour_token` (`red`, `green`, `blue` or `yellow`,
unique across divisions), `proposition`, `kicker`, `body`, `roster_heading`, `products` (an ordered
list of `name`, `tagline`, `url` and `pills`), `scene` (`disc-stack`, `sphere-ring`, `nested-boxes` or
`rippled-sphere`), `position` (unique). Exactly four rows.

### `disciplines`

`id`, `slug` (unique), `name` (at most 24 characters), `position` (unique). Twelve rows.

### `profiles`

`id`, `account_id` (the owning account, unique when set; null only for a seeded example), `slug`
(unique), `name`, `division_id`, `statement`, `portrait_url`, `state` (`applying`, `draft`,
`submitted`, `changes_requested`, `published` or `unpublished`), `is_live` (true exactly while the
profile shows on the public site), `position` (unique among live profiles), `pending_payload` (the
owner's held edit to a live profile, or null), `return_note`, `reviewed_by`, `seeded`, `version`,
`created_at`, `updated_at`, `submitted_at`, `published_at`, `returned_at`.

### `profile_disciplines`

`profile_id`, `discipline_id`, `position` (one to four within a profile).

### `profile_links`

`id`, `profile_id`, `kind` (`site`, `photo`, `network`, `social`, `audio` or `document`), `label`,
`url`, `position` (one to five within a profile).

### `profile_credits`

`id`, `profile_id`, `line`, `position` (one to eight within a profile).

### `profile_events`

`id`, `profile_id`, `kind` (`applied`, `submitted`, `returned`, `published`, `unpublished` or
`moved`), `to_state`, `from_division_id`, `to_division_id` (both set when `kind` is `moved`),
`actor_id`, `body` (the note, when there is one), `created_at`. Append-only: one row for every
application, submission, send back, publication, take down and move.

### `notices`

`kind` (`terms`, `privacy` or `cookies`, unique), `title`, `body` (never empty), `updated_at`. Three
rows.

### `site_events`

`id`, `name`, `properties`, `created_at`. Append-only; a row exists only for an event a consenting
browser sent.

### Seed data

- Accounts: `curator@example.com` (`curator`, `Ines Marlow`), `creator@example.com` (`creator`,
  `Juno Okafor`) and `creator2@example.com` (`creator`, `Ada Moreau`), all with confirmed addresses.
- Divisions: the four divisions with the names, slugs, colour tokens, propositions, kickers, bodies
  and roster headings stated under A division, scenes `disc-stack`, `sphere-ring`, `nested-boxes` and
  `rippled-sphere` in position order, and Creator Tech's four products.
- Disciplines: the twelve disciplines in the stated order.
- Profiles, all with `published` state and live, in this curated position order, every portrait
  address `https://media.example.com/portraits/<slug>.jpg`:

| Position | Slug | Name | Division | Disciplines | Statement |
|---|---|---|---|---|---|
| 1 | `juno-okafor` | Juno Okafor (owned by `creator@example.com`) | `creator-media` | presenting, writing | `Juno hosts Backstage Hours, a weekly long-form interview show about the working lives of independent musicians, and writes the letter that follows every episode.` |
| 2 | `amara-voss` | Amara Voss | `creator-media` | presenting, producing | `Amara presents a travel series filmed entirely on night trains and produces the companion podcast with the crews who keep them running.` |
| 3 | `theo-lindqvist` | Theo Lindqvist | `creator-media` | writing, directing | `Theo writes and directs short documentaries about small workshops that still make things by hand, released one film at a time each month.` |
| 4 | `priya-castellano` | Priya Castellano | `creator-media` | presenting, community | `Priya presents a cooking channel built around recipes her viewers send in, and runs the community that tests every one of them first.` |
| 5 | `sol-ferreira` | Sol Ferreira | `creator-communities` | community, producing | `Sol runs a members club for amateur astronomers that meets under dark skies every new moon, and produces its live observing nights.` |
| 6 | `hana-petrova` | Hana Petrova | `creator-communities` | community, writing | `Hana moderates a reading circle of forty thousand members and writes the monthly guide that decides what the circle reads next.` |
| 7 | `remy-achebe` | Remy Achebe | `creator-products` | design, commerce | `Remy designs limited runs of field notebooks with the illustrators his audience follows, and sells out every run before it ships.` |
| 8 | `kenji-aldana` | Kenji Aldana | `creator-tech` | engineering, analytics | `Kenji builds the scheduling engine behind Signal Desk and measures how every release changes the hours creators spend on admin.` |
| 9 | `mara-oyelaran` | Mara Oyelaran | `creator-tech` | analytics, audience-insights, discovery | `Mara leads audience research for Roster Graph, turning listening habits into the discovery maps creators use to plan a season.` |
| 10 | `felix-brandt` | Felix Brandt | `creator-tech` | engineering, design | `Felix designs and engineers Brief Engine, the tool that turns a brand's first message into a brief a creator can accept in one reading.` |

- Every seeded live profile carries one link of kind `site` labelled `Work` at
  `https://www.example.com/<slug>` and one credit line naming its show or product, and every one
  except `juno-okafor` has no account and is marked `seeded`.
- `ada-moreau`: name `Ada Moreau`, owned by `creator2@example.com`, division `creator-tech`,
  discipline engineering, state `draft`, never live, statement `Ada builds the payment rails inside
  Payline so creators are paid on the day a partner signs off on the work they delivered.`, portrait
  address `https://media.example.com/portraits/ada-moreau.jpg`, one `site` link labelled `Work`.
- No live profile carries the discipline `partnerships`.
- Notices: the three notices, each with a title and a written body of at least one paragraph that
  describes, for privacy and cookies, the site events recorded after consent and the two consent
  choices.

Seeding must be idempotent: restarting the app must not duplicate a row, must not reset a profile a
creator has changed, and must not send any mail.

## Front-end specification

This section carries the visual system in full. It states intent, relationships and the states each
surface has; the exact values that are taste are yours.

### Module and component architecture

The product separates cleanly into modules whose dependencies point one way: the tokens at the bottom
with no dependencies, then the marks, then the motion vocabulary with its single reduced-motion
resolution, then the heading splitter that owns both the per-character elements and the single
accessible sentence, then the scene, the transition, the chrome, the routes, the roster surfaces, the
forms, the state layouts, the API contract and the consent-gated instrumentation, which is the only
module that reads the consent answer. Two costs are specific to this design and shape that
architecture: the scene never unloads across the routes that hold it, and the heading stagger runs on
every heading on every route, so where the frame budget is at risk the stagger keeps its rhythm and
gives up its length.

### Design tokens as the single source

The whole design is declared as named design tokens in one place: the colour roles, every type step,
the base gap and its multiples, the component measurements, the two curves and the durations. Nothing
else in the product carries a literal colour, size, gap or timing; a component that needs the Creator
Media colour names that division's token. Type steps and gaps are fluid expressions between a small
window and a wide one rather than fixed values, the root size itself slides with the window inside a
central band and holds steady above and below it, and the expressions are kept whole rather than
simplified into a handful of fixed sizes. One type system is used everywhere; a second, fixed ramp
never coexists with the fluid one.

### Colour roles and the light and dark swap

The colour tokens are the ground, a dark and a light end, the text, the four division colours, the
accepted colour, the rejected colour, three greys mixed from the two ends (a light grey for hairlines
and disabled labels, the reading grey, and a dark grey for lifted surfaces, resting underlines and
skeleton fills), and the inverted pair the arrival screen uses. Because every grey is a mix of the
ground and the text, swapping the two ends in light mode inverts every grey with them, and every
contrast relationship holds in both modes. The division colours do not change between modes. There
is one gradient that fades the foot of a division's scene into the ground, one soft darkening laid over
a scene's corners, and one blur on a single overlay path; nothing else in the product is a gradient or
a blur.

### The gap scale and the choosing rule

One base gap and a ladder of multiples from about a third of it up to about nine times it. Gaps below
about one and a half times the base are spacing inside a control; two to three times the base separate
rows within one block; five times and above separate one block from the next; the largest gap appears
once per route, above the first heading. The page's horizontal padding is one fluid token and the only
horizontal page padding in the product.

### Stacking order

Layers stack in a fixed order from back to front: a division's scene behind its content; the ordinary
content; a card's own inner layers; a division's sticky heading; a roster card's pointing overlay; the
bar's three layers; the menu overlay, the palette and the sign in layer; the mode toggle and the
banner, which stay above the menu; the consent card; the page transition curtain; and the arrival
screen in front of everything.

### Iconography

About twenty marks, all drawn inline from coordinates, none fetched, and none carrying a colour of its
own: every mark takes the colour of whatever holds it, which is what lets the whole set invert with the
mode and with the wordmark's blend. Four families:

- **The wordmark.** A solid lettered mark for Halden whose full box is filled in the current colour,
  so the whole mark inverts. The arrival screen carries a larger lettering of the name in three stacked
  groups: a filled dot, a first lettering pass and a second pass.
- **The interface set.** Thin outlines on one small square: a dot inside a ring (the active mark), a
  chevron pointing right, a close cross, a ring, a globe (a circle crossed by a horizontal diameter and a
  vertical ellipse), a camera (a rounded square with a lens circle and two small dots), a document (a
  rounded rectangle open at its foot) and a professional-network mark. The audio mark and the social
  mark are framed marks: a glyph inside a square frame inset by half a unit, so the frame's own stroke
  sits inside the box. Every social mark in the product is drawn that way.
- **The armillary indicator.** A filled centre disc, a full ring and three arc segments around it,
  drawn filled at the front door's size and as strokes at two smaller sizes. It reports loading progress
  and the acquired segment, and completes on a steady, linear sweep, the only linear timing in the
  product.
- **The sketch lines.** Three long, loose, heavy hand-drawn strokes, each one continuous stroke with a
  deliberate hitch about a third of the way along, on boxes roughly four times as wide as they are tall.
  They are drawn on by their dash offset, never faded, and they are used directly as the reveal shape
  wherever the reference used a picture of a stroke.

A new mark follows the drawing rule: interface marks are thin strokes on the small square, framed marks
use the square frame inset by half a unit, everything takes the current colour, and a sketch mark is one
continuous heavy stroke with one hitch. `chevron-right` is the only mark that points a direction.

### The bar, the clock and the menu

The bar is a thin strip over the content holding the wordmark at the left, the clock at the centre and
the menu control at the right, padded so each control is a comfortable target although it looks small.
The wordmark and the menu control are composited as the difference against what is behind them; no mode
switch and no scroll position touches their colour, and focus is drawn around them in the text colour
because the blend alone cannot be relied on to show it.

The clock group is set in the reading grey between two brackets. Each city label and each time is one of
three siblings sharing a single fixed slot as wide as the widest of the three, and the slot slides from
one to the next on the page curve every few seconds, so the bar never reflows. Under reduced motion the
slot shows the first city only.

The menu control is a clipped box one line tall holding `Menu` above `Close`; its state change slides the
pair by one line. The same two-line swap is the site's universal text swap for any control whose label
changes.

The menu overlay covers the page. Each of its six links holds a bracket pair in the navigation type
size, the active mark, the link text set large with a second overlay copy for the swap, a line in the
division's colour and a hand-drawn sketch stroke that draws itself across when the link is pointed at.
Under the overlay sits an underlay that is hidden while the menu is closed. At a narrow width the links
stack at a smaller step without sketch lines, the clock and the toggle move into the overlay, and the
overlay's foot carries the three legal links.

The mode toggle is a small dot inside a rounded track, above the menu overlay, at the window's bottom
right on a wide screen and inside the menu overlay on a narrow one.

### The consent card

The consent card is the only rounded card in the product: a compact panel at the window's foot, as wide
as its own token on a wide screen and the full width less the page padding on a narrow one, holding the
consent paragraph with its two emphasis runs on `'Accept All'` and `Cookie Policy`, and the two controls,
each with a thin line beneath it. It is the only thing in the product that ever covers a scene, and it is
reachable by keyboard before any other control while it is showing.

### Motion vocabulary

The named moments, each with its trigger and its reduced-motion substitute:

- **Arrival count.** The counter runs with real loading; under reduced motion it is unchanged, since it
  is a progress report.
- **Arrival letters.** Each lettering pass draws on as loading passes each third; reduced motion shows the
  lettering complete.
- **Arrival exit.** The curtain clips away over the longest duration in the product; reduced motion
  removes it in one step.
- **Chrome enter.** The wordmark, clock, menu and toggle rise from invisible as the arrival completes;
  reduced motion applies it in one step.
- **Heading reveal.** Per line, a one line-height offset and fade on the stagger ladder; reduced motion
  sets every line at rest with no stagger.
- **Clock cycle.** The slot slides every few seconds; reduced motion shows the first city only.
- **Text swap.** A two-line pair slides by one line; reduced motion replaces the first line with the
  second.
- **Link colour.** The text colour and the mark's fill change out of step, the colour first; reduced
  motion applies both in one step.
- **Sketch draw.** A menu link's stroke draws from full length to nothing; reduced motion shows it
  complete.
- **Ellipse fill.** A pill's fill grows from an ellipse of nothing at its centre; reduced motion shows the
  fill in one step.
- **Arm rotate and arm settle.** The armillary tracks the pointer drag, then settles to the nearest
  segment on the pointer curve; reduced motion steps one segment per arrow control.
- **Arm indicate.** The indicator sweeps to complete on its linear timing; reduced motion jumps to
  complete.
- **Mode swap.** Every colour token changes together over about a second; reduced motion applies it in one
  step.
- **Page exit and page enter.** The curtain comes in and goes out on the page curve; reduced motion skips
  the curtain.
- **Card lift.** A roster card lifts and its overlay fades over about a third of a second; reduced motion
  shows the overlay in one step.
- **Spin.** The ring mark turns steadily for anything pending; reduced motion shows a still ring in the
  reading grey.
- **Scene parallax.** A division scene's camera tracks the scroll; reduced motion holds one position.

Four rules hold everywhere: nothing fades in flat; only the two curves exist, the pointer one for
anything the pointer caused and the page one for anything the page caused; the shared unround duration
applies unless a moment above says otherwise; and scroll-driven movement tracks and never animates on a
timer. The one repeating keyframe in the product is the ring's full turn. The many other easing curves
a heavy animation library brings are never used.

### The arrival screen

A full-window layer in front of everything with the inverted ground and type. The lettering block is
centred and offset slightly left of centre by a fixed share of its own width; the sketch block beneath it
is about one and a half times as wide and offset by a share of its own width; the two sketch strokes,
one red and one grey, share one stroke shape. The counter sits near the foot of the window in a small
fixed-width slot, with a line beneath it. The root element carries `data-arrival` as stated under Core
features, and the chrome stays invisible until the exit.

### The armillary

The object fills the window on the near-black ground and is rendered live at the screen's pixel
density. Its four rings are generated from a lathed profile rather than a modelled mesh, each ring
slimmer and closer to the centre than the last, with a chamfer along both front edges; the outer ring is
cut into four arcs with narrow gaps and the inner three are continuous. The centre is a glossy sphere
about a fifth of the object's diameter.

Two materials make everything and no third is introduced anywhere in the product: a dark brushed metal,
anodised near-black, whose highlight runs along each ring's tangent with a soft specular roll along its
upper edge; and a high-gloss black glass with a single sharp highlight and a visible reflection of the
rings. The lighting is generated rather than fetched: a small environment rendered once from a vertical
gradient between the ground and the dark grey with one bright band standing in for a studio strip light,
which is what produces the roll of light along each ring. A single soft contact shadow sits under the
object, generated as a radial falloff.

The intro dispersion is made by rendering the settled scene several times with the camera's projection
scaled very slightly apart and taking one colour channel from each, with the scale drawing back together
as the object settles, so the fringes converge and never persist into the settled state.

The front door's controls: the arm link beside the object, hidden until a segment is acquired; the
previous and next pills; the indicator at the bottom left; the headline block and the `About Us` pill
at the bottom left at the page padding. The rotation is never remembered and the object always opens at
rest. The scene is one long-lived layer told which station and which segment to hold; it is built once
when somebody arrives and never re-created per route, and the bar likewise is built once.

### The division scenes

Each division route shows its own object behind its content, made of the same two materials as the
armillary, which is what makes the four routes read as four rooms in one building:

- **Creator Media:** a stack of seven thin discs on a common axis, each fanned a few degrees from the
  last, in the metal.
- **Creator Communities:** a ring of twelve small spheres connected by fine rods.
- **Creator Products:** four nested rounded boxes, each turned a little from the one inside it.
- **Creator Tech:** a single sphere in the glass with a gentle rippled displacement.

The scene's foot fades into the ground and a soft vignette darkens its corners, so the type over it
never gets lost. A division's loading line takes the division's colour. The division thumbnails used in
the menu are rendered from each division's own object once per mode and never fetched, and only the set
for the current mode is ever produced. A division may carry up to four animated figures, each a line
drawing that builds itself by its dash offset, paused until it enters the window and carrying a text
alternative naming what it depicts.

### Sketch mode

A second register for the whole site. Headings move from the condensed display face to the hand-drawn
lettering face at the sketch title step; every drawn stroke comes forward at full strength; scenes become
line art in the text colour on the ground from two drawing plates of the division objects, with no
material and no reflection. Layout, gaps, type positions and every string are unchanged, so any view of a
route reads the same text in both registers. The sketch face and its plates load only when sketch mode is
first entered.

### A division route and the roster grid

The division template runs in document order: the mission heading, the headline echo, the division name,
the `SKETCH MODE` text control, the proposition, the kicker as one uppercase navigation-size line, the
body at the largest body step, held faint until revealed, any credits one per line, the named products
(each an `About` label in grey, a name, a tagline, pills and `Visit Site`), the roster heading and the
grid. The grid has three columns with a column gap and a larger row gap; the middle column is shifted down
by half a card plus half a row gap, a constant, so no cascading layout library is needed. Each card is a
fixed fluid height with its portrait filling it and its caption beneath: the name at a large body step in
the text colour, the division line in small uppercase in the division colour, and up to four pills a
small gap apart.

### The roster, a profile and the palette

The roster route is built only from the same tokens: the heading at the subpage title step in the display
face with the largest gap above it, the count in the reading grey beneath, the filter row a row gap below
that, each filter opening a small list above the page, then the grid exactly as on a division route. A
profile route runs one column on a narrow screen and two on a wide one with the portrait beside the text:
the name at the large subpage title step, the division at the sans subtitle step in its colour, the pills,
the statement at the largest body step in the reading grey, the link row, the credits and a kicker, a
block gap apart. The command palette is a centred panel on a lifted surface in the dark grey with one
underline field and a list of entries in the navigation type, the highlighted entry in the text colour and
the rest in the reading grey, grouped as Divisions, Pages and People.

### Forms, fields and controls

A field at rest has no fill and no box: one thin line in the dark grey beneath it, a little padding, text
at the regular body step in the text colour, and its label above it in small uppercase navigation type in
the reading grey. A placeholder is the dark grey. Focus brightens the line to the text colour on the
short pointer timing and draws a thin outline in the text colour just outside the field. Invalid turns the
line to the rejected colour with the message beneath it in the smallest body step in the rejected colour.
Disabled sets line and text in the dark grey. A multi-line field is the same, at least a few lines tall,
resizing only vertically.

Every control is the pill. At rest it is a thin line in the dark grey with no fill and text in the text
colour. Pointed at, an ellipse overlay grows from nothing at its centre until it covers the pill, filling
with the text colour, and the label crosses to the ground colour. Focused, the fill completes at once and
the outline is drawn. Pending, the label becomes the turning ring. Disabled, line and text sit in the dark
grey with no pointing change.

### Surfaces for the creator and the curator

The editor is a two-column split on a wide screen with the field column beside the live preview, and the
preview beneath the fields below that width; the preview is skipped by keyboard focus. Its publication
block names the state in words and holds the one publication control. The review queue is a split pane:
a narrow list of waiting entries and a wide preview of the selected one, with `PUBLISH` and `SEND BACK` in
uppercase navigation type with the ellipse fill. Slide-overs enter from the right edge over a dimmed page
and leave the same way. Full-page confirmations use the centred notice layout with the heading at the
subpage title step. The denied surface `Not for you` uses the same centred layout in the legal column
width. The pinned note sits above the profile name at the regular body step in the text colour with its
label in the rejected colour, and stays until the profile is submitted again.

### The four state layouts

- **The centred notice.** In the surface's own column: a heading at the subpage title step in the display
  face in the text colour; beneath it a line at the large body step in the reading grey of at most sixty
  characters; beneath that at most one pill. No illustration and no mark.
- **The inline notice.** One line at the smallest body step in the reading grey inside the block's own
  column, with a row gap above and below.
- **The skeleton.** The collection's own layout with each item replaced by a block of the item's size
  filled in the dark grey, with no shimmer and no pulse, held for at least the short duration once shown.
- **The banner.** A fixed strip at the window's foot at the toggle's level, small uppercase navigation
  type in the reading grey, centred, with no ground, held about two seconds and faded on the short timing.

| Surface | Loading | Empty | Error | Offline |
|---|---|---|---|---|
| The front door | the arrival screen | not possible | the list fallback with `REDUCED GRAPHICS` | the object keeps turning |
| A division | skeleton of the heading block and six cards | `Nobody here yet.` / `This part of the ecosystem is being built.` / `See the roster` | `That did not load.` / `We could not fetch this part.` / `Try again` | `You are offline.` / `What you already opened still works.` |
| A division's scene | the content renders first | not possible | the scene is left out on the plain ground | as error |
| The roster | skeleton of nine cards | `Nobody yet.` / `The roster is being built.` / `Join us` | centred with `Try again` | what was already fetched, banner `OFFLINE` |
| The roster, filtered | skeleton | `Nothing here.` / `No one matches that.` / `Clear filters` | centred | centred |
| A profile | skeleton of the portrait block and three lines | not possible | `That did not load.` / `We could not fetch this profile.` / `See the roster` | centred |
| A profile, not found | none | `Not here.` / `This profile is not published, or it never was.` / `See the roster` | as empty | as empty |
| The application | none, it is local until sent | not possible | per field | stays writable and keeps its values |
| The profile editor | skeleton over the field column | not possible | inline per field | stays writable and keeps its values |
| The review queue | skeleton of four cards | `Nothing waiting.` / `Nobody has sent anything in.` / `See the roster` | centred | centred |
| The legal routes | skeleton over four paragraph blocks | `This notice is being rewritten.` | centred with `Try again` | centred |
| Sketch mode | the strokes render complete at once | not possible | the mode refuses and nothing changes | unchanged, it is local |

### The legal routes

One template for all three: the ground and the chrome with no scene, one centred reading column at the
narrowest container width with the page padding, the title at the subpage title step with the largest gap
above, the last-updated line at the smallest body step in the reading grey, a contents list one line per
section, section headings at the sans subtitle step a block gap apart, paragraphs at the regular body step
in the reading grey a row gap apart, and indented lists.

### Every surface at every width

| Surface | Narrow | Mid | Wide | Full |
|---|---|---|---|---|
| The front door | the armillary smaller and high, headline beneath, the instruction line, the control full width | as narrow without the instruction line | the wide layout | the wide layout |
| The bar | wordmark and menu control only; clock inside the menu | as narrow | the clock returns showing one city | all three cities cycling |
| The menu overlay | links stacked at a smaller step, no sketch lines | links at full size with sketch lines | as full | as full |
| The mode toggle | inside the menu overlay | as narrow | fixed at the window's foot | fixed at the window's foot |
| A division | one column, the scene holding one position | one column, the scene tracking | two columns where the template has two | the full template |
| The roster grid | one column, no offset | two columns, the second lower | three columns, the middle lower | three columns, the middle lower |
| A profile | one column, portrait full width | as narrow | two columns, portrait beside the text | as wide |
| The application slide-over | full width, labels above fields | as narrow | a side panel | a side panel |
| The legal routes | one column at the page padding | as narrow | as narrow | the centred reading column |
| The consent card | full width less the page padding, at the foot | as narrow | its own width | its own width |

At every width: the armillary is never hidden or swapped for a still; the front door is one window tall;
the type ramp is the same set of fluid steps; nothing scrolls sideways; and the roster grid keeps its
column offset wherever there is more than one column.

### Accessibility detail

Focus order on the front door runs the wordmark, the menu control, the mode toggle, the primary control,
the armillary region, then previous and next. In the menu overlay it runs the six links and then the
close control; on a division route the bar, each block in document order, then each roster card in grid
order; on a profile the bar, the division link, each pill, then each outbound link; on the roster the bar,
the filter row, then each card; in the application every field in order then the submit; in the editor the
field column in order with the preview skipped.

Reordering links, credits or roster cards by keyboard: focus the row, `Space` lifts it, the arrow keys move
it, `Space` drops it and `Escape` cancels, and a lifted row announces `<label>, lifted, position <n> of
<m>`. Choosing disciplines: focus the pill group, arrows move, `Space` toggles, at most four.

Polite announcements: arrival progress at each quarter as `<n> percent`, a route's own heading when it
opens, every banner text, `Saved` on a field save, `Sent to the studio` on a submission, `<n> people` when a
filter changes, `Loading` once when a skeleton shows, `Light` or `Dark` on a mode change,
`Reduced graphics` when the scene degrades, and a division's name when its segment is acquired. Assertive
announcements: `Not saved. Your text is safe here.` when a save fails and `Changes requested` followed by
the note when a profile is returned.

The darker grey never carries readable text; a disabled control carries its state in its accessible name
as well. Where the blend cannot composite, the wordmark and the menu control sit over a translucent ground
scrim that keeps them well above the contrast floor. Text selection is on everywhere.

### Resilience and the narrow-window addition

Resilience is part of the design rather than a late fix: a scene that fails never takes the page with it,
a request that fails keeps what somebody typed, a lost connection leaves what was fetched readable, and the
real-time parts of the studio simply read again when opened. The one narrow-window addition is the
instruction line beneath the armillary, because on a touch screen the object does not invite a drag the
way it does under a pointer.

### Performance and loading

The front door's first paint and usable chrome arrive well before the armillary's first frame, which the
arrival screen covers; a division route, the roster, a profile and the application paint quickly with the
scene held; a legal route renders no scene at all. The scene keeps a smooth frame rate while the armillary
is dragged and may halve its update rate after a couple of seconds with no input; a division scene tracks
scroll without dropping a frame during a heading reveal; the roster, a profile and the forms add no
continuous rendering beyond the held scene.

Most things are deferred: a division's object until the transition into it begins, its surface detail
until the object is ready, portraits until their card enters the window, the animated figures until they
enter the window, the sketch face and plates until sketch mode is first entered, a legal notice until its
route opens, and site events until consent is given and the arrival is complete. Preloaded with the
document: the two reading weights and the display face, declared once each in one stylesheet and served
from the app's own origin, the inline mark geometry, the tokens and the chrome, and the armillary against
the counter.

When a machine cannot keep up, quality drops in a fixed order measured over a couple of seconds of frame
times and never climbs back within a visit: fewer dispersion passes, then coarser surface detail, then a
simpler ring profile, then no dispersion with the banner `REDUCED GRAPHICS`, then scenes that hold one
position instead of tracking scroll, and finally no scene at all with the front door's list fallback, the
site still fully usable.

### Zero-asset build

The product ships no binary of any kind and fetches none of its own: no model, texture, mask, thumbnail,
font file from another origin, video or vector-animation document. The rings, the materials, the lighting,
the shadow, the noise that breaks up large surfaces, the division objects, the thumbnails and the figures
are generated; the sketch strokes are drawn from their own coordinates; the three open-licence typefaces
are named in the build's own notice and self-hosted. People's portraits are the one photographic input,
and an absent one becomes the generated still described under A creator profile.

### Copy deck

Strings not already quoted above, carried verbatim:

| Where | String |
|---|---|
| menu control | `Menu`, `Close` |
| clock brackets | `(`, `)` |
| front door primary control | `About Us` |
| narrow instruction | `Tap a section of our ecosystem to navigate.` |
| division | `About us`, `SKETCH MODE`, `Visit Site`, `About`, `Our tool box` |
| mission | `Our purpose is to shorten the road back to human.` |
| roster | `The roster`, `<n> people` |
| profile owner | `Edit this` |
| profile states | `Applying`, `Draft`, `With the studio`, `Changes requested`, `Live`, `Taken down` |
| join us | `Join us`, `Apply`, `Edit your profile` |
| application | `Your address`, `Choose a password`, `Your name`, `Where do you fit`, `What do you do`, `Tell us what you do`, `Where can we see it`, `You may keep my details to reply.`, `Send` |
| sign in | `Sign in`, `Apply to join`, `That combination is not one we know.` |
| forms | `Which kind of link is this?`, `That did not send. Your text is safe here.`, `Too many for now. Try again in a little while.` |
| editor | `Submit for review`, `WITH THE STUDIO`, `Publish changes`, `Send changes for review`, `Not saved. Your text is safe here.` |
| review | `PUBLISH`, `SEND BACK`, `Note`, `Send back`, `Say what needs changing.`, `Already handled.` |
| curator on a profile | `Take down`, `Move to`, `Reorder` |
| denied | `Not for you` |
| arrival | `Continue without the scene` |
| states | `That did not load.`, `Try again`, `You are offline.`, `What you already opened still works.` |

### Corrections carried as requirements

These faults exist in the site this product is modelled on and none of them may come back: headings split
into loose characters with no accessible sentence; a roster entry reading `** INSERT NAME **` and pills
reading `Pill Text` on the public site; two division names in title case and two in sentence case (all four
are title case); font faces declared several times over across separate stylesheets; eight division
thumbnails fetched to show four; pictures of strokes fetched when the strokes exist as coordinates; a
developer control panel shipped in the public build; dozens of unused easing curves carried in the bundle;
a front door that swallows the wheel and does nothing; bar controls far smaller than a finger; and a join
page with no way to join.

## Constraints

- Only the providers named in this brief exist: PostgreSQL for the database and Mailpit for mail. Do
  not add a cache, a queue, a search engine, an object store, a second database or another mail sender,
  and do not call out to the public internet at request time.
- One deployment, one origin. The site, the API, the sitemap and the robots file are served together.
- No uploads of any kind: a portrait is an address under `https://media.example.com/portraits/`, and the
  server never fetches a portrait or link address.
- No third-party script, analytics collector, consent vendor, font host, video host or model host. The
  only event log is the app's own, behind the consent card.
- No live connection from the browser to the server for updates; every surface reads when it opens.
- No localisation and no internationalisation beyond the fixed formatting stated under Technical
  requirements. All text is English and every layout reads left to right.
- No rich text anywhere a creator writes: a statement, a note, a link label and a credit are plain text.
- No bulk publish: each profile is a person and is published one at a time.
- The four divisions, their colour tokens, the six states, the six link kinds, the ten error tokens, the
  ten site event names (recorded in full, with no sampling, as the only instrumentation) and the twelve
  seeded disciplines are closed sets. Do not add a member to any of
  them.
- The site stays responsive with a few thousand live profiles and a site event log of tens of thousands
  of rows.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, `4173`
  is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from
  the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | readiness, reporting the database and the mail server |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `role`, `name`, `verified` |
| `GET /api/me` | none | `email`, `name`, `role`, `verified`, `profile_slug` |
| `GET /api/site` | none | `headline`, `mission_line`, `divisions`, `disciplines` |
| `GET /api/divisions/{slug}` | optional `discipline`, `sort` | the division with `products` and `roster` |
| `GET /api/profiles` | optional `division`, `discipline`, `q`, `sort`, `page`, and `state` for a curator | `total`, `page`, `items` |
| `GET /api/profiles/{slug}` | none | one live profile's full shape |
| `POST /api/applications` | `email`, `password`, `name`, `division`, `disciplines`, `statement`, `links`, `consent` | `account`, `profile` |
| `POST /api/accounts/verifications` | `token` | nothing, `204` |
| `GET /api/me/profile` | none | the caller's profile at any state with `pending` and `version` |
| `PATCH /api/me/profile` | any of `name`, `statement`, `portrait_url`, `division`, plus `version` | the profile |
| `PUT /api/me/profile/disciplines` | `disciplines`, `version` | the profile |
| `PUT /api/me/profile/links` | `links`, `version` | the profile |
| `PUT /api/me/profile/credits` | `credits`, `version` | the profile |
| `POST /api/me/profile/transitions` | `to`, `version` | the profile |
| `POST /api/profiles/{slug}/transitions` | `to`, `version`, and `note` when `to` is `changes_requested` | the profile |
| `PATCH /api/profiles/{slug}` | `division`, `version` | the profile |
| `PUT /api/studio/roster-order` | `slugs` | the live roster in its new order |
| `GET /api/notices/{kind}` | none | `kind`, `title`, `body`, `updated_at` |
| `POST /api/events` | `name`, `properties` | nothing, `204` |

A successful call returns the named resource or shape. An invalid or unauthorized call is rejected as a
client error with the error body, never as a server error and never as a silent success. Bearer auth is
required on `GET /api/me`, every `/api/me/...` endpoint, `POST /api/profiles/{slug}/transitions`,
`PATCH /api/profiles/{slug}` and `PUT /api/studio/roster-order`; every other endpoint answers without a
token, and `GET /api/profiles` honours `state` only with a curator's token.

**No mocks.** A confirmation link written to the log instead of mailed, mail kept in a database table
instead of sent over SMTP, a roster kept in browser storage, a live flag kept only in the browser, or an
application that pretends to create an account are each a contract violation. The named providers are the
fact: the app's pages can only reflect what is stored in PostgreSQL and what was delivered to Mailpit, never
substitute for either.

## Definition of done

A visitor can turn the armillary into any of the four divisions, read its roster and a creator's profile,
and find anybody on the roster by division, discipline or name, in light or dark and in sketch mode. A
creator can apply, confirm their address from its mail, fill their profile, be refused while anything is a
placeholder, submit, be sent back and published by a curator, rewrite their live profile without the public
seeing a half-finished change, and move themselves to a different division through review, after which a
fresh visitor finds them on the new division's route and not the old one. A profile that is not live cannot
be reached at any public address.
