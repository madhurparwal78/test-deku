# Creative Studio Archive

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, read the studio's sequence end to
end, open a client case from the numbered stack, drag the archive wall until it wraps, and send a
work inquiry that the studio finds already queued in its own console, without hitting an error page.
A different stranger must NOT be able to read a case the studio has not published, the image bytes
behind it, or any case other than the one a review link was issued for, by any means, including a
direct request for it by its own path. The uploaded image bytes must live in the object store at
their scheme's key; a copy on the app's own disk does not count.

## Overview

Halftone is a small digital creative studio. It sells art direction, branding, product design and
the code that ships them, and its evidence is the work rather than a feature list. The public site
is therefore not a catalogue: it is one scroll driven sequence read in one order, opening on a
statement of who the studio is, passing a studio seal and a run of disciplines, arriving at a
numbered stack of client cases, then a board of the studio's recognitions, then the address a
prospective client writes to.

A second mode sits over the same document. The archive is everything the studio has made that did
not earn a case study, spread across a plane much larger than the window, which a visitor drags and
throws and which wraps rather than ending. A visitor also watches the studio's showreel, opens a
case and walks sideways through the stack from inside it.

Behind the site is a console the studio's own people work in. A writer drafts a case, uploads its
imagery and submits it. A lead approves it, publishes it, orders the stack, records each award win
as its own row, and works the inquiries the site produces as a queue with an owner and a clock. A
client reviewer is not a member of the studio at all: they hold a link that shows their own case at
one exact revision and reaches nothing else, and a case cannot go public until that link comes back
approved.

It deliberately is not a content platform. There is no email, no SMS and no push: an inquiry is
acknowledged on the screen and answered in the studio's own mail application. There is no payment,
no plan and no cart, because nothing is sold here. No comments, no likes, no follows, no messaging,
no public profiles, no site search, no second language, no second tenant and no scheduled
publication.

The genuinely hard part is that draft and published are the same records seen through different
eyes, and the boundary has to hold in four places at once: the public case route, the list that
feeds the stack, the object behind the cover image, and the review token that is deliberately let
through exactly one of them. An app that hides a draft in the interface while still serving its
path, its cover object, or a neighbouring case through a review token has painted the boundary
rather than built it.

## User roles

Two roles, both seeded. A client reviewer is not an account.

| Role | Can do | Cannot do |
|---|---|---|
| `writer` | Sign in to the console; read every case in any state; create and edit a draft; upload imagery; curate the archive; submit a case for review | **Cannot** publish, unpublish, approve, reorder the stack, record an award, issue a review link, read the inquiry queue or read the trail |
| `lead` | Everything a writer can do, plus approve a revision, publish, unpublish, reorder the stack, record and remove award records, issue and revoke review links, work and erase an inquiry, and read the trail | **Cannot** be created by signing up, and **cannot** be granted by any request the app serves |

Anyone at all, signed in or not, may read every published surface and may send one work inquiry. A
client reviewer holds a signed token in a link: it is bound to one case and one revision of it, it
carries no other capability, and it is accepted on no path outside the preview.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `writer` session to any `lead`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged. A destination the signed in role cannot use is absent from the console rail rather than
disabled, because a disabled control invites a request the server refuses anyway.

There is no signup. No route, form or field creates an account or changes an account's role, and the
studio's people are seeded.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Seeded state |
|---|---|---|
| `lead@example.com` | lead | holds `art-direction`, `branding` and `motion-design`; is the principal lead |
| `lead2@example.com` | lead | holds `web-design`, `front-end-development` and `back-end` |
| `writer@example.com` | writer | holds no disciplines |

## Core features

### Accounts and sessions

1. A member signs in with an email and a password and receives a bearer token, which every console
   request carries. Passwords are stored hashed; the literal above must work at login.
2. Signing out stops the token working immediately. A request carrying a stale or missing token to
   any console endpoint is denied, and the protected state is unchanged.
3. Repeated failed sign in attempts from one address are refused with a retry hint rather than
   answered forever.

### The home sequence

4. `/` renders eight blocks in this order and no other: the hero statement, the studio seal, the
   services run, the selected cases heading, the case stack, the awards board, the contact block and
   the footer. Each block carries the attribute `data-block` with, in order, the exact values
   `hero`, `seal`, `services`, `cases-heading`, `case-stack`, `awards`, `contact` and `footer`.
5. The block list is stored content, not markup. `GET /api/page` returns it, a lead can disable or
   reorder a block, and the page follows. A block naming a component the app does not have is
   skipped, the fault is recorded, and every other block still renders: a mistyped component name
   gives a page with a gap in it, never a blank screen.
6. The hero reads the four display words `Halftone`, `Digital`, `Creative` and `Studio`, one per
   line, and carries a control reading `Play` over `OUR SHOWREEL`. The seal reads `we`, `are`,
   `HALF`, `TONE`, `studio`, `all together` and a founding line reading `since '18`. The services
   run is prefixed `Just About` and then names the eight disciplines in their stored order: Art
   Direction, Branding, Web Design, Mobile Design, Content Production, Motion Design, Front-end
   Development, Back-end. The cases heading reads `Selected` over `cases`.
7. Five destinations sit in one fixed group, in this order, carrying `data-menu` with the exact
   values `about`, `work`, `recognition`, `contact` and `archive`: `ABOUT`, `WORK`, `RECOGNITION`,
   `CONTACT US` and `ARCHIVE`. The first four move the reader within the page and must not change
   the address. `ARCHIVE` changes the address, because the archive is a mode a visitor can link to.
8. The document element carries `data-mode`, which reads `sequence` on the home sequence and
   `archive` in the archive mode, and nothing else.

### The case stack

9. `GET /api/cases` returns only published cases, ordered by `stack_order` ascending, contiguous from
   `1`. Twelve are seeded. Each carries `slug`, `client`, `title`, `description`, `year`,
   `stack_order`, `veil`, `cover_url` and `disciplines`.
10. Every card carries `data-case-order`, its `stack_order` as a decimal string, and `data-veil`, its
    veil value. The veil is computed from the card's position in the published list and from the
    number of published cases, never typed by a writer: for a list of `n` cases the card at
    `stack_order` `k` has a veil of `0.55 + 0.45 * (n - k) / n`, reported to four decimal places, so
    the first card is the dimmest and the last is fully clear. With the twelve seeded cases that is:

    | `stack_order` | `veil` |
    |---|---|
    | `1` | `0.9625` |
    | `2` | `0.9250` |
    | `3` | `0.8875` |
    | `4` | `0.8500` |
    | `12` | `0.5500` |

11. Reordering regrades the whole stack. `POST /api/console/cases/reorder` takes the full list of
    published slugs in their new order, rewrites every affected row together, and returns each case
    with its new `stack_order` and its recomputed `veil`. Two published cases must never hold the
    same `stack_order`, and there must never be a gap in the run.
12. Adding a published case regrades the stack too: with thirteen published cases the card at
    `stack_order` `1` reads `0.9654`, because `n` changed.
13. The last item in the stack is not a case. It is a card carrying the word `Archive` and a four
    line description, styled as a case card is styled, and it is always last. It takes no
    `stack_order` and it never appears in `GET /api/cases`.
14. With no published case at all the heading and the archive card still render and the stack region
    collapses to nothing rather than showing a placeholder.

### The case study

15. `/case/<slug>` is a real address. `GET /api/cases/{slug}` returns one published case with its
    card fields plus `summary`, `credits`, `blocks`, `live_url`, `awards`, `previous_slug` and
    `next_slug`. `previous_slug` and `next_slug` follow the stack's own order, and the first and the
    last case carry `null` in the direction that has no neighbour.
16. A case body is an ordered list of blocks of seven kinds and only seven: `text`, `image_full`,
    `image_pair`, `video`, `quote`, `stat` and `gallery`. A `gallery` carries between three and
    twelve images. A `stat` carries at most four value and label pairs. A `quote` carries at most 240
    characters plus an attribution and a role. A block of an unknown kind is skipped, the fault is
    recorded, and the rest of the case renders.
17. Rich text inside a `text` block is stored as a structured document, never as markup, and carries
    only bold, italic, links and lists. There is no route by which raw markup reaches a rendered
    page.
18. A case that is not published answers a stranger exactly as an unknown address does: the studio's
    own not-found page, and `GET /api/cases/{slug}` reports it as not found. The site must not
    confirm that the case exists, because a case being prepared for a client is commercially
    confidential. A signed in member, and a reader holding a valid review token for that exact case,
    see it.

### The archive

19. `GET /api/archive` returns one document describing the whole wall: `seed`, `plane` with its
    `width` and `height`, and `items`, each carrying `id`, `title`, `year`, `x`, `y`, `w`, `h`,
    `disciplines`, `case_slug` and `image_url`. Two hundred and forty items are seeded, one of them
    linked to the published case `isla-sereno`.
20. The wall's arrangement is generated from the item sizes and the stored seed `halftone-wall-2026`,
    never curated by hand. No two item rectangles overlap on the plane, every rectangle lies inside
    the plane, and two reads of the archive with nothing changed return byte-identical positions: an
    archive that reshuffles between reads loses the recognisability that makes people return to it.
21. Adding, removing or resizing an archive item regenerates the layout against the same stored seed,
    and the result still holds rule 20.
22. Every item carries `data-archive-item` with its own `id`. Pressing an item raises it out of the
    wall with its title, its year and its discipline tags; an item linked to a published case carries
    a control that leaves the archive and opens that case.
23. With an empty archive the mode is not offered at all: the `ARCHIVE` destination and the archive
    card are both omitted and a direct request for the archive mode returns the sequence.

### The showreel

24. `/showreel` is a real address and also opens over the sequence from the hero control and from the
    bottom band. `GET /api/showreel` returns `poster_url` and `renditions`, and both the poster and
    the reel are objects in the store rather than files shipped with the app.
25. The reel starts playing with sound muted and a visible unmute control is present from the first
    frame. Space toggles play and pause, a press anywhere on the film does the same, escape closes
    it, the arrow keys seek by five seconds and the `M` key toggles sound. A captions toggle exists
    and its state survives a reload.
26. Nothing about the reel is fetched until the visitor asks for it, so it costs nothing to everyone
    who never plays it.

### Awards and recognition

27. The board groups recognitions by the body that awarded them. Three bodies are seeded: `Prixel`,
    `Flux` and `Portfolia`. The heading reads `Awards and Recognitions`, and a three line uppercase
    note points at the studio's art director `Mira Lindqvist` above a control reading `Show me`.
28. A count is the number of award records of that type, computed on read, and is stored nowhere. A
    writer never types a total. `GET /api/awards` returns each body with its types and each type with
    its `count`. The seeded counts read:

    | Body | Award type | `count` |
    |---|---|---|
    | `Prixel` | `Studio of the Year` | `1` |
    | `Prixel` | `Site of the Day` | `24` |
    | `Prixel` | `Developer Award` | `23` |
    | `Prixel` | `Mobile Excellence` | `14` |
    | `Prixel` | `Site of the Year` | `2` |
    | `Flux` | `Site of the Day` | `6` |
    | `Portfolia` | `Gallery, Interaction` | `7` |
    | `Portfolia` | `Gallery, Experience Design` | `4` |
29. Recording one more win of a type through `POST /api/console/awards` moves that type's count up by
    exactly one on the next read of the board, and removing a record moves it down by one.
30. Two seeded types, `Portfolia` `Gallery, Graphic Design` and `Portfolia` `Gallery, Illustration`,
    carry no records. Each renders its name alone, at the same size, with no gap where the number
    would be. A body carrying no records at all is omitted, and with no records anywhere the whole
    block is omitted and the `RECOGNITION` destination with it.
31. Each record carries a verification address and an optional case it was won for, so a case can
    show its own awards and the board and the case can never disagree. A verification address that no
    longer resolves is flagged in the console and makes no public change at all: the studio won the
    award whether or not the awarding body still hosts the page.

### The work inquiry

32. The contact block leads with the studio's address `hey@halftone.studio`, under a heading reading
    `Don't hesitate` over `to say Hello` over `our team`, above the qualifier
    `WORK INQUIRIES AND PARTNERSHIPS`. A control reading `Or send us a brief` expands a form in place beside it. The
    address stays the primary action, because a prospective client with a brief already written
    should not be made to retype it into fields.
33. `POST /api/inquiries` takes `name`, `email`, `company`, `budget_band`, `timeline`,
    `disciplines`, `message`, `consent`, `source_block`, `submission_key`,
    `form_opened_at` and `company_website`, then returns `id`, `received_at` and `state`. Validation is enforced on the server and the server's rules are the
    definition: `name` is 2 to 120 characters after trimming, `email` is a syntactically valid
    address of at most 254 characters, `company` is at most 160 characters, `message` is 20 to 5000
    characters after trimming, `consent` must be true, `budget_band` is one of `under-25k`,
    `25k-75k`, `75k-200k`, `over-200k` and `not-sure`, `timeline` is one of `now`, `this-quarter`,
    `this-year` and `exploring`, and every value in `disciplines` is a current discipline slug.
34. An invalid submission is refused, writes nothing at all, and returns an error per field keyed by
    that field's own name. The message under a field says what to do rather than what is wrong: an
    empty reply address reads `Enter an address we can reply to` and a short message reads
    `A sentence or two is enough, but we need something`. The same rules govern every form in the
    product, including the console's: a field validates on first blur and on every change once it has
    been in error, its message sits directly under it, and pressing submit while invalid moves focus
    to the first invalid field and announces how many there are.
35. The submission carries a client generated `submission_key` and the server treats a repeat of that
    key as the same submission. Two requests carrying one key produce exactly one row, and the second
    request returns the first one's `id` rather than a refusal. This must hold under two simultaneous
    requests.
36. An accepted submission replaces the form in place with a confirmation reading
    `Thank you, it arrived` above
    `Somebody will reply within one working day. If it is urgent, write to us directly.`
    and repeating the studio's address. The consent checkbox is labelled
    `I agree that the studio may store this message and reply to it. It is kept for two years and never shared.`

### Automated submission defence

37. `company_website` is a decoy field that no person can see and no person fills.
    `form_opened_at` is the moment the visitor opened the form. A submission arriving with
    the decoy filled, or arriving less than three seconds after its own `form_opened_at`,
    is refused, is stored with its `spam_reason`, is never queued to a lead, and shows the
    sender exactly the confirmation in rule 36. A sender is never told they were
    classified.
38. The ceiling is five submissions per email address per hour and
    twenty per network origin per hour. Beyond it the submission is refused with a retry hint reading
    `That is a few too many in a short time. Try again shortly, or write to us directly.`
    and the studio's address stays available as the alternative.
39. A high scoring submission is written to the queue in the state `spam` rather than `new` and is
    visible in the console under that filter. No layer ever discards an inquiry irrecoverably: every
    refusal is stored with its reason, because losing one real brief costs far more than storing
    junk.

### The studio console

40. The console lists every case in any state at `GET /api/console/cases`, and every row carries
    `data-state` with one of the exact values `draft`, `in_review`, `approved`, `published`,
    `unpublished` and `archived`, written as a word and never signalled by colour alone.
41. Every save carries the `revision` the editor loaded. A save against a stale revision is refused,
    returns the current `revision` and the fields that differ, and the editor's own content is never
    discarded. Two edits from the same loaded revision must not both be accepted: exactly one is
    accepted and the other is refused.
42. A lead works the inquiry queue at `GET /api/console/inquiries`, newest first, filterable by
    `state` and by `assignee`. An inquiry moves between the exact states `new`, `assigned`,
    `replied`, `won`, `lost` and `spam`, a note is written in the row, and every one of those actions
    is recorded.
43. Routing is a default and never a lock, and any lead may take any inquiry. An inquiry at the
    budget band `over-200k` is assigned to `lead@example.com` whatever its disciplines. Otherwise an
    inquiry naming a discipline held by exactly one lead is assigned to that lead. An inquiry
    matching neither rule arrives unassigned.
44. Erasing an inquiry is a state and not a delete. `POST /api/console/inquiries/{id}/erase` is a
    lead action: the row keeps its identifier, its `received_at` and every one of its events, its
    `erased_at` is set, and `name`, `email`, `company` and `message` each read exactly `[erased]`. An
    erased inquiry is unreadable to every role afterwards.
45. The trail at `GET /api/console/audit` is append only. Its `sequence` values are strictly
    increasing with no gaps, each row's `prev_hash` equals the previous row's `hash`, and no route
    updates or removes a row. It records every case state change, every review link issued or
    revoked, every client decision, every inquiry state change, assignment and erasure, and every
    refusal at the request boundary, and it holds no personal data of its own: an inquiry is
    referenced by identifier rather than copied.
46. Deleting a media asset that is referenced anywhere is refused and the refusal lists the records
    that reference it, because a refusal that cannot be acted on is worse than none.

### Client preview and the publication gate

47. `POST /api/console/cases/{slug}/review-links` is a lead action. It takes one or more `emails` and
    an `expires_in_days` between `1` and `90`, default `14`, and issues a distinct token per address
    bound to that case and to its current `revision`. Issuing against a case that already has an
    outstanding link revokes the previous tokens, so there is never ambiguity about which revision a
    client approved.
48. `/preview/<token>` renders that one case revision through the same components the public site
    uses, with a bar across the top reading `You are looking at a draft of this project` beside the
    revision and the date it was sent, an approve control, a request changes control and a comment
    control on every body block. There is no menu, no archive, no other case and no route from it to
    one: a token that leaks must expose exactly one document.
49. `POST /api/preview/{token}/decision` records `approve` or `request_changes` against the exact
    revision the token names. A request for changes returns the case to `draft`. A comment through
    `POST /api/preview/{token}/comments` does neither on its own and is retained after publication as
    the record of what was agreed.
50. A case enters `published` only when every one of these holds, checked at the moment of the
    transition: a client approval is recorded against the exact `revision` being published, that
    approval has not been withdrawn, a `lead` has approved the same `revision`, every required field
    is present, and every referenced image has finished processing. `POST
    /api/console/cases/{slug}/publish` otherwise refuses and names every condition that is not met,
    and the stored state does not change.
51. Editing a case after approval writes a new `revision`, and the approval no longer matches, so
    publication is refused until the new revision is approved again. A lead may mark a correction a
    minor revision, which carries the existing client approval forward; a minor revision may not
    change `client`, `title`, `summary`, `description`, `year`, any credit or any `stat` value, and
    an attempt to change one of those inside a minor revision is refused.
52. An expired token, a revoked token, an unknown token and a malformed token all produce the same
    page, reading `This link has expired` above `Ask the person who sent it for a new one and they
    can issue it in a moment.`, and none of them says anything about the case. A token for a case
    that has since published redirects to the public case.
53. A case may be marked as not requiring client approval, which satisfies the first two conditions
    of rule 50. Only a lead may set it, the reason given is recorded, and it is per case and never a
    default.

### Imagery and the object store

54. Every uploaded image lives in the object store and nowhere else. A case cover is stored at
    `cases/{case_slug}/{sha256_of_bytes}.{ext}`, for example
    `cases/isla-sereno/9f2a4c1b7e0d3a86f5c2b90418de7a63c41f0b29d8e5a7346c0fb912de84a5c0.jpg`. An
    archive image is stored at `archive/{item_id}/{sha256_of_bytes}.{ext}` and the showreel and its
    poster at `showreel/{sha256_of_bytes}.{ext}`.
55. An object key is generated and never taken from the name the uploader gave. Content type is
    decided by inspecting the bytes rather than by the extension: a file renamed to a different
    extension is refused on inspection, and the refusal names the accepted kinds.
56. The bytes behind an unpublished case are as confidential as the case. `GET
    /api/cases/{slug}/cover` for a case that is not published is refused to an anonymous caller in
    exactly the way the case itself is, and is served to a signed in member and to a reader holding a
    valid review token for that case.
57. Every content image carries alternative text and a decorative image declares itself decorative.
    No image file ships with the app: where a photograph would be, a pattern is generated from that
    record's own identifier, so the same record always produces the same pattern and nothing jumps
    around between loads.

### The privacy page

58. `/legal/privacy` is reachable from the footer of every page. It states what the studio keeps
    about somebody who writes to it, which is their name, their address, their company and their
    message; that an inquiry is kept for two years from its last state change and then erased; that a
    stored inquiry can be erased on request; and that nothing is shared with anybody else. The footer
    link to it is present on every route, including the not-found page.

### When a page does not exist

59. An unknown address renders the studio's own not-found page and reports itself as not found rather
    than as a success. It reads `Page` over `not` over `found`, above the single uppercase line
    `MAKE SURE TO FIND YOUR WAY BACK TO THE HOMEPAGE TO ENJOY OUR WEBSITE`, above one control reading
    `GO HOME` that returns to `/`.
60. Every internal link on every public route resolves. The not-found page is what an unknown address
    reaches, never what a link the site printed reaches.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the home sequence, eight blocks in order | public |
| `/?archive=true` | the archive wall over the same document | public |
| `/case/<slug>` | one published case | public |
| `/showreel` | the showreel | public |
| `/legal/privacy` | the privacy page | public |
| `/preview/<token>` | one unpublished case revision, and nothing else | token |
| `/login` | sign in | public |
| `/console/cases` | the case list, the editor panel and the preview | writer, lead |
| `/console/archive` | archive curation | writer, lead |
| `/console/awards` | award records | writer, lead |
| `/console/media` | the media library | writer, lead |
| `/console/inquiries` | the inquiry queue | lead |
| `/console/audit` | the trail | lead |
| any other path | the studio's own not-found page | public |

**Entry and redirects.** An anonymous request for any console route lands on `/login` carrying the
destination as a relative return path; an absolute return path is refused and the reader lands on
`/console/cases`. A successful sign in lands on the return path when there is one, and on
`/console/cases` when there is not. A `writer` requesting `/console/inquiries` or `/console/audit` is
refused by the server and lands on `/console/cases`, and neither destination appears in their rail.
Signing out returns to `/` and the token stops working at once. A token that expires mid edit returns
the reader to `/login` with the form's values preserved and the save retried on success.
`/case/<slug>` for a case that is not published renders the not-found page for anybody who is neither
a signed in member nor the holder of a valid review token for that exact case.

**Journeys.**

1. A visitor opens `/`, lets the arrival sequence finish, presses `WORK` in the menu, scrolls the
   stack, presses the card whose `data-case-order` is `4`, reads the case, presses the control at the
   right edge, arrives at the case whose `previous_slug` names the one they left, presses escape, and
   lands back on the sequence at the reading position they left.
2. A visitor presses `ARCHIVE`, watches the address change, drags the wall far enough that it wraps,
   releases it and watches it carry on and stop, presses one item, reads its title and year, presses
   escape to return it to the wall, presses the close control, and lands back on the sequence.
3. A visitor presses `CONTACT US`, presses `Or send us a brief`, fills in everything but the reply
   address, presses send, reads `Enter an address we can reply to` under that field, fills it in,
   presses send, and reads `Thank you, it arrived` in place of the form.
4. A writer signs in as `writer@example.com`, opens `/console/cases`, creates a case in the panel that
   opens over the list, fills its client, title, summary, description and year, uploads a cover,
   submits it for review, and finds no publish control anywhere on the page.
5. A lead signs in as `lead@example.com`, opens the case `harbourline-freight`, issues a review link
   for it, opens that link as the client would, presses approve, returns to the console, approves the
   same revision internally, presses publish, and finds the case in the stack.
6. A lead opens `/console/inquiries`, assigns the unassigned inquiry to themselves, moves it to
   `replied`, writes a note in the row, and watches the age stop counting.
7. A lead opens an inquiry, erases it on request, and finds the row still present, still carrying its
   events, with every personal field reading `[erased]`.

**States.** Every list carries an empty state that says in one line what would be there and offers
the one control that creates the first, never an illustration. Every list carries a loading state at
the real row height, so nothing moves when it resolves. A failed save keeps the form's values, names
the reason beside the field and offers a retry. A failed image renders the generated pattern at the
record's own shape rather than a broken box. A block naming a component that does not exist leaves a
gap and the rest of the page renders. No error takes a page down.

## UI/UX notes

**North star.** Somebody arriving should understand within one screen that this is a studio whose
craft is motion and typography, and should feel that the site itself is the portfolio piece.
**Register.** The public sequence is editorial: it carries weather, the work is the first thing seen, and the reader is meant to stay a while. The console carries none of that; what it is for is reading a queue and acting on it again. Two stances run through the whole product, either of which a rival studio could invert and be right: **sequence over navigation** on the public site, because it is read in one order rather than browsed, and **atmosphere over immediacy**, because arrival here is paid for in real seconds before the first case appears.

**Mode.** Committed to dark and designed fully in dark. There is no light mode to grade, and the one
inversion in the whole product is the case card, which is a light ground sitting on the dark page.

**Palette by role.** The ground is a near-black neutral and it is the only background under the
sequence; nothing else is ever painted behind a block. Display type, headings and the case card's own
ground are a near-white neutral. Body copy and menu labels at rest sit one step below that, still
near-white, so a label reads as quieter than a heading without reading as disabled. Captions,
secondary lines and the dimmed half of a stacked card are a light neutral, and rules and hairlines are
a light neutral one step above them. One signal colour exists: a pale, low chroma green, near-white in
weight. It appears on exactly two things, the state change on anything a pointer or a key can act on,
and the studio's contact address, which is itself the primary action on the page. If a second thing
wears it the site has stopped saying what it means. Every fade into the ground reaches true black
rather than the ground colour, because those fades sit over a moving surface and a fade that stops at
the ground shows its own edge. There is no fourth colour and no hue in any gradient in this design: a
build that reaches for a coloured gradient has misread the palette. Generated placeholder imagery is
drawn from deep and light neutrals only, because a placeholder carrying colour would be the only
colour on the site and would read as a fault. Pick the exact values yourself. The one condition is that each meaning keeps its own colour and nothing else borrows it, with the ratios further down still met.

**Type.** Four families do four jobs and are named by role because the build supplies its own. The
interface family is a neutral grotesque with a tall x height that has to stay legible in uppercase at
caption size with wide letter spacing, and it carries every label, caption and menu item. The display
family is a high contrast serif with condensed capitals and a strong vertical stress, and it is the
single element carrying the studio's voice: case titles, the contact address and the footer list. The
condensed family is a narrow uppercase grotesque and carries the section headings and the services
run. The numeral family carries the arrival counter and nothing else, and needs only digits and a
percent sign. Every family declares a fallback stack, and the fallback is a requirement rather than a
courtesy because the first paint happens in it. Nothing is sized to a fixed step: every size is a
ratio applied to one base, so changing the base moves the whole page together, and body copy sits at
`16px` with a `24px` line height, body medium at `18px` over `27px`, body large at `20px` over
`30px`, captions at `15.2px`, `13.68px` and `12.16px`, micro at `12px`, section headings at `72px`,
`81px` and `90px`, and the display sizes at `158.4px` and `230.4px`. Three rules fall out of that and
they are the look. Display and heading sizes set their line height to four fifths of their size, so
display lines cut into each other, and that overlap is what makes the hero read as a poster rather
than as a document. Caption sizes set their line height equal to their size, or a tenth above it, so
captions read as tight blocks of capitals rather than as running text. Body copy alone sits at one and
a half and is the only text in the product set for continuous reading. Figures line up on tabular
numerals wherever counts stack, which here means the award board and every console column.

**Motion.** One speed does almost all of the work: every colour change and every state change on
every control moves at the same rate on one curve, and a second rate introduced for one element is
the fastest way to make this design look assembled. Four other rates exist and each has one job: a
quicker one for a background swap under an already moving element, a delayed one for a fade that has
to wait for something else to finish, a longer one for a size or position change on a large element,
and the longest for the trailing pointer and for a mode change. Three things never stop while the page
is open: the starburst turns, and both text bands slide. Every starburst instance turns at the same
rate in the same direction and they are deliberately out of phase with each other, so a viewer seeing
the largest and the smallest at once does not read them as one mechanism. Everything else waits until
it is scrolled into view and then arrives once, through one of four named entrances: a `rise`, where
the block resolves a vertical offset to nothing while it fades in; a `line-wipe`, where a paragraph is
revealed line by line from behind a moving edge; a `char-cascade`, where display type is revealed one
character at a time from the left, as a hand setting type rather than a machine; and a `settle`, where
a large element arrives from a slight scale and offset and overshoots once before it lands. A block
reveals when its top crosses a line set a configurable distance above the bottom of the window, and it
reveals exactly once: scrolling back up does not reverse it and scrolling back down does not replay
it, so the page does not flicker at a reader who is reading. One observer decides that a block is on
screen and three things read it, the entrance, the menu's current label and the recorded impression;
three separate observers over the same elements is the defect this rule prevents. Display headings in
the sequence are cut into four vertical parts by angled edges that follow the same crack drawn
during the arrival sequence, so the two read as one gesture, and the cut positions are computed from
that crack rather than authored. Under a reduced motion preference every entrance resolves at once
to its end state with no movement and no stagger, all continuous movement stops on its first frame,
the trailing pointer is not mounted, the moving background renders one still frame, the custom scroll
takes no part and the platform scrolls the document, and the arrival sequence shortens to a single
progress reading. Nothing is lost but the theatre, and no content is ever hidden behind an animation
that did not run. The console borrows none of this: nothing there overshoots, and a transition that
draws attention to itself while somebody is working a queue has failed.

**Density and layout.** The public sequence is spacious and exactly one thing dominates each view.
Sections are separated by space rather than by rules, and a hairline appears only where two sections
share a ground. The gap between two blocks is roughly three times the gap under a heading and roughly
halves on a narrow screen, and every gap is a multiple of one base unit that is yours to choose. The
case stack sits in a centred column a little under half the window wide, and the empty ground either
side of it is load bearing: it is what makes the column read as objects laid on a table rather than as
a page of results. There is no shadow anywhere in this design, and depth is carried by the graded veil
over a stacked card and by the lit surface behind everything. Corners are square, with exactly three
radii in the whole product: the circular badges inside the studio seal, the circular outline around a
single word, and the scroll thumb, which is barely softened. Nothing is drawn as a bordered box; where
a rule is needed it is one hairline in the rule tone or in a half transparent near-white, and nowhere
else. The stacking order is part of the design rather than an implementation detail, because several
of these layers are siblings: the moving surface sits behind every block, the sequence content above
it, the isolating fades above that, the fixed chrome and the two text bands above those, the mode and
case overlays above those, the trailing pointer above those, and the arrival sequence above everything
until it leaves. The console inverts all of it: a persistent rail down the
left, a grid of cards as the working surface, rows tight enough that a full queue is read without
scrolling, creation in a panel that slides over the list so the queue never disappears while it is
being worked, and a brief message over the working surface for every outcome, which retires itself.

**Components.** A control in this product answers to five states: at rest, pointed at, pressed,
focused, out of reach. A control that is out of reach says so in a word beside it as well as in its
tone, because a change of colour is not a message to a reader who cannot see the change. One link treatment is used across the whole
product, on the menu, on the contact address, on the footer list and on the not-found control: the
label carries two copies of its own text offset by a fraction of a character in opposite directions
and normally invisible, and on the pointed-at state the copies separate and re-converge so the word
appears to tear and reset as it turns to the signal colour. The tear is driven from the element's own
text, so a re-worded label distorts correctly with no extra markup, and the separation lands before the
colour finishes. The whole case card is one control and one focusable element with one accessible name
built from the client and the discipline: a card that exposes its image, its title and its description
as three separate stops is the defect this rule prevents. Pointing at a card lifts its veil to fully
clear. The system pointer is replaced by three concentric rings at descending opacity that chase the
pointer and arrive after it has stopped, and the rings change form to say what is possible here: an
open hand over the archive wall and a closed hand while it is being dragged, a play or pause form over
the showreel, and the word that opens a case inside the ring over a card. The replacement pointer is
decoration and nothing may depend on it: it is not mounted for a coarse pointer or under a reduced
motion preference, and every control stays usable without it. Escape closes any overlay and returns
focus to whatever opened it. A form field keeps its label visible at all times, and a placeholder is never the label. A field the server rejected carries the reason in words beside the field, never a red edge on its own.

**The accessibility floors are contract, not taste.** Both surfaces meet WCAG 2.1 level AA, the console included: a back office is where this gets dropped, and it is where the studio's own people spend the day. Running copy holds at least `4.5:1` against whatever sits behind it. Display type, the edge of any control, the focus ring and any graphic carrying meaning hold at least `3:1`. Against this ground the
light neutral used for captions is the darkest text colour permitted anywhere and no value darker than
it may be introduced. Touch targets are at least `44px` by `44px` including the space around them, and
no text is smaller than `12px`. Keyboard navigation reaches every control, including the archive wall,
and the visible focus ring is never removed anywhere: the arrow, page, home and end keys move the
sequence; tab and enter open a case; the left and right arrows move between cases from inside one;
escape closes any overlay; the arrow keys pan the wall by a window third and the page keys by a full
window; space plays and pauses the reel, the arrow keys seek it and the `M` key mutes it. Each
sequence block is a landmark region whose accessible name matches its menu label, the four hero
display lines are one heading rather than four, and any heading split into characters for its entrance
also exists once as a single string for assistive technology, or a quarter of this site's headings
become a stream of disconnected letters. One polite live region announces the current section on a
menu jump, the number of errors on a failed submit, the state of the reel and the outcome of an
inquiry, and it announces nothing on scroll, because a region that speaks continuously is worse than
one that never speaks. The moving background, the starburst, the crack, the trailing pointer, the
grain and both text bands carry no accessible name and are hidden from assistive technology; the bands
are the exception worth stating, because they carry text and they are controls, so each is exposed
with its purpose as its name while the moving text itself is hidden.

**Responsive.** There are two layouts and a handful of refinements, and the composition changes once,
around the width of a tablet held upright; where the other breakpoints sit is yours, but the layout
must hold at every width between them and not only at them. Above that width the hero display lines
overlap at their largest size with the statement set in the gaps between them, the menu carries its
five labels in a column, the services run wraps as a paragraph with mixed faces, a case card puts its
image left and its title right at its most generous padding, the awards groups sit in a row, the
contact address is one line at display size, the moving background runs its full chain, the archive
wall carries its full set of effects, the replacement pointer is mounted and the custom scroll is in
charge. Below it everything stacks into one column: the hero lines stop overlapping and drop to
heading size with the statement beneath them, the menu collapses to the contact label with the rest
reachable from the studio mark, the services run sets one discipline per line, a case card puts its
image above its title at one tight padding step, the awards groups stack, the contact address wraps
over two lines, the background becomes one still image with no light and no grain, the wall keeps only
its desaturation, the replacement pointer is not mounted and the platform scrolls the document. Height
matters as much as width, because the hero is composed against the bottom of the window: below a short
window height the hero lines reduce a step and the statement moves below them at any width. Layout
follows width but behaviour follows input, and the two are decided separately, because a touch laptop
is wide and a desktop window can be narrow: where the pointer is coarse there is no replacement
pointer and no hover state, and tap targets still reach the floor above. At the narrowest viewport the
page reflows to one column and no route scrolls sideways, nothing overflows horizontally and every
navigation target stays reachable; at a narrow viewport nothing is missing that a wide screen has, the
collapsed menu labels are reachable rather than removed, and text zoomed to twice its size clips no
block.

**What it must not look like.** Not a page dominated by one hue family with no second signal. Not
decoration standing in for content. Not a marketing composition where the console belongs, and not the
console's density where the sequence belongs. Not a product whose state has to be inferred from a
coloured swatch with no word beside it. Not a wall of imagery that is fully coloured at rest, which
loses the structure that makes it a surface rather than a slideshow.

## Technical requirements

Front end: vanilla progressive enhancement over server rendered documents. There is no client
framework and no client router. Every route is a complete document produced on the server, so the
hero is text before any script runs, and the scroll engine, the moving background, the archive wall,
the overlays and the replacement pointer are layers added on top of a page that already works
without them. With scripting switched off entirely, every word, every image and every link is still
present and still in order on every public route.

Back end: Express on Node 20, written in TypeScript, rendering documents through Nunjucks
templates and serving the JSON API on the same origin under `/api`. The accelerated surfaces are drawn with the platform's own
canvas; where it is unavailable the ground is flat and the archive falls back to a plain paged grid
of the same imagery with the same open behaviour.

Datastore: PostgreSQL, read from `DATABASE_URL`. Object store: MinIO, read from `STORAGE_ENDPOINT`,
`STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Both are already running and
reachable at those variables. The app's public origin and port come from `APP_PUBLIC_URL` and
`APP_PUBLIC_PORT`; never hardcode a host or a port.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor - the only backing services
available in this environment are `postgres` and `minio`, and reaching for anything else is a
contract violation.

Auth is implemented by this app: email and password, hashed at rest, exchanged for a bearer token
that every console request carries in its `Authorization` header. There is no external identity
provider, no signup route and no password reset. A client reviewer never authenticates: the token in
the preview link is the credential, it is compared without leaking how far the comparison got, it is
scoped to one case and one revision, and it is accepted on no path outside the preview.

`GET /api/health` returns `200` with a `status` field once the app can reach both backing services.

Every response carries the standard security headers: a strict transport security header, a header
denying framing, a header refusing content type sniffing, and a referrer policy. No credential, key
or token appears in anything the browser downloads. No state change ever happens on a read request.

Rate limits are enforced on the server and a limited response carries a retry hint: the inquiry
submission at five per email address per hour and twenty per network origin per hour, sign in
attempts per address per hour, and a preview token at sixty requests per minute.

Uploads are the highest risk surface in this product. Content type is decided by inspecting the
bytes and never by the name given, a size ceiling is enforced, the object key is generated rather
than taken from the uploaded name, and the bytes are served with a download disposition.

Logging is one structured line per request carrying the method, the route pattern, the status and
the duration. A log line must never carry an inquiry's message text, a password, a bearer token or
the object key of an unpublished case.

## Data model

Sixteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

- `members` - `id`, `email` unique and compared case insensitively, `display_name`, `role` of
  `writer` or `lead`, `disciplines`, `password_hash`, `created_at`.
- `disciplines` - `id`, `name`, `slug` unique, `menu_order`.
- `cases` - `id`, `slug` unique and immutable once the case has published, `client`, `title` of at
  most 60 characters, `summary` of 120 to 400 characters, `description` of 80 to 240 characters,
  `year` between `1990` and next year, `cover_key`, `cover_alt`, `live_url`, `stack_order` unique
  among published cases and contiguous from `1`, `has_big_title`, `client_approval_required`
  defaulting to true, `state`, `current_revision`, `published_revision`, `created_at`, `updated_at`.
  `veil` is derived on read from `stack_order` and the published count and is stored nowhere.
- `case_revisions` - `id`, `case_id`, `revision`, `snapshot`, `author_id`, `is_minor`, `created_at`.
  A revision is immutable once written, and the current draft and the published version are two
  pointers into this history that are frequently different revisions.
- `case_blocks` - `id`, `case_id`, `position`, `kind`, `payload`.
- `case_credits` - `id`, `case_id`, `credit_role`, `name`, `position`.
- `case_disciplines` - `case_id`, `discipline_id`.
- `archive_items` - `id`, `title`, `year`, `image_key`, `image_alt`, `intrinsic_width`,
  `intrinsic_height`, `case_slug`, `is_published`, `curator_order`, `plane_x`, `plane_y`, `plane_w`,
  `plane_h`.
- `archive_layout` - `id`, `seed`, `plane_width`, `plane_height`, `generated_at`. Exactly one row.
- `award_bodies` - `id`, `name`, `slug` unique, `site_url`, `display_order`.
- `award_types` - `id`, `award_body_id`, `name`, `display_order`. A count is never a column here.
- `awards` - `id`, `award_type_id`, `won_on` never in the future, `verification_url` absolute,
  `case_id`, `link_state`, `link_checked_at`.
- `inquiries` - `id`, `received_at`, `name`, `email`, `company`, `budget_band`, `timeline`,
  `disciplines`, `message`, `state`, `assignee_id`, `spam_score`, `spam_reason`, `source_block`,
  `submission_key` unique, `erased_at`.
- `inquiry_events` - `id`, `inquiry_id`, `actor_id`, `kind`, `from_state`, `to_state`, `note`,
  `created_at`.
- `review_tokens` - `id`, `case_id`, `revision`, `email`, `token_hash`, `issued_by`, `issued_at`,
  `expires_at` between one and ninety days ahead, `revoked_at`, `decision`, `decided_at`.
- `review_comments` - `id`, `review_token_id`, `block_id`, `body`, `created_at`.
- `audit_events` - `id`, `sequence`, `actor_id`, `actor_kind`, `action`, `subject_type`,
  `subject_id`, `created_at`, `prev_hash`, `hash`. Append only: nothing updates a row and nothing
  removes one.
- `media_assets` - `id`, `object_key` unique, `content_type`, `byte_size`, `width`, `height`,
  `alt_text`, `is_decorative`, `state` of `processing`, `ready` or `failed`, `created_at`.
- `page_blocks` - `id`, `component`, `position`, `is_enabled`.

Invariants, each of them a property of the running system rather than a way of achieving one. A
`submission_key` belongs to exactly one inquiry: two simultaneous submissions carrying one key must
not both create a row, exactly one is stored and the other returns the first one's `id`. Two
simultaneous saves of one case from the same loaded revision must not both be accepted, exactly one
wins and the other is refused with the current revision. A reorder that would leave two published
cases at one `stack_order`, or leave a gap in the run, must not be accepted at all, and a refused
reorder leaves every row exactly as it was. An erased inquiry keeps its row, its identifier and
every event that ever referenced it. The trail's `sequence` values are strictly increasing with no
gaps and each row's `prev_hash` equals the previous row's `hash`.

**Seed data.** Three members as listed above. Eight disciplines in their stored order, with the slugs
`art-direction`, `branding`, `web-design`, `mobile-design`, `content-production`, `motion-design`,
`front-end-development` and `back-end`. Twelve
published cases at `stack_order` `1` to `12`, in this order: `northline-ventures`, `isla-sereno`,
`halcyon-frozen`, `hero-assembly`, `playful-works`, `marlow-field`, `verrine`, `essence-atelier`,
`kasper-wend`, `aurelio-sant`, `cure-studio`, `wildberry-care`. Two more cases are not published:
`harbourline-freight` is `in_review` and already carries a recorded client approval against its
current revision but no lead approval, and `quiet-hours` is `draft` with no approvals at all. Three
award bodies, ten award types and eighty-one award records distributed to give the counts in the
Core features table, with two Portfolia types carrying no records. Two hundred and forty archive
items laid out against the seed `halftone-wall-2026`, one of them linked to `isla-sereno`. Two
inquiries: one `new` and unassigned from `casper.reid@example.com`, and one already `assigned` to
`lead@example.com` from `tilda.moor@example.com`. Seeding must be idempotent - restarting the
app must not duplicate rows.

## Front-end specification

This section carries the visual and interaction detail the sequence needs. Nothing in it is
behaviour the product does not already own; it says what the surfaces look like and how they move.

### The five marks

Every mark in this product is drawn from coordinates. There is not one icon file in the build, and
blocking every image request must leave all five intact and sharp at any size.

The studio mark is a single closed outline of an intertwined paperclip form, sitting top left in the
fixed chrome at a resting opacity below half, in a light neutral one step brighter than the caption
tone. The starburst is a radial burst of thin ragged spikes drawn as one closed outline, its spike
lengths varying so the silhouette is ragged rather than regular, and it inherits whatever colour it
sits in. It recurs at five sizes: largest behind a section heading, smaller on a narrow screen,
smaller again above the footer, small beside a caption, and smallest inside the studio seal. The home
arrow is a right pointing arrow with a rounded shaft and appears only on the control that leaves the
not-found page. The diagonal arrow is the one mark that says a control leaves the current mode: it
sits after the `ARCHIVE` label and nowhere else, and its stroke is inherited from the label so it
turns to the signal colour with it. The smile is a circular outline holding two dots and an open arc,
bottom left of the footer, stroked at the same weight as the diagonal arrow.

### The fixed chrome

A band of repeating text crosses the very top of the document, moving steadily right to left and
alternating the studio name with the word archive. It is built from two tracks inside one wrapper,
both carrying the same content and starting at offset positions, so the band never shows a seam over
a long observation; seamlessness comes from the offset rather than from repeating the content enough
times to be safe. The whole band is a control: pointing at it turns it to the signal colour and
pressing it enters the archive. It does not begin moving until the arrival sequence has finished.

A second band runs along the bottom edge reading `Watch Showreel /` on the same two track mechanism
and the same cycle. It is a control that opens the showreel, it appears only once the sequence has
passed the first case, and it hides while any overlay is open.

The studio mark sits top left with two lines of uppercase caption beside it reading the studio name
and its descriptor. The group returns the reader to the top of the sequence and is the first item in
the keyboard order after the skip control. The five menu labels sit top right in one column,
uppercase, at the tight caption size, with `ARCHIVE` separated from the first four by one blank line.
A label at rest is the dim near-white tone, turns to the signal colour when pointed at, and holds the
full near-white tone while its own block is on screen. That current state is driven from the same
observer that fires the block entrances, so the menu and the animation can never disagree about which
block is on screen. While an overlay is open the whole group dims and stops responding, and the
overlay's own close control takes over. A thin scroll thumb, the one barely softened corner in the
product, appears along the right edge while the sequence is moving and fades when it stops; on a
narrow screen it indicates position only, and at desktop width it is a control.

The chrome sits at the same inset from the top and from each side so that the mark and the menu read
as one frame, and it holds that inset without shrinking or fading as the page moves under it. That
stillness is the design.

### The scroll system

The sequence does not scroll natively. The content is moved under a fixed window and the position is
a number the application owns, because four things read it: the line that fires a block's entrance,
the drift of the moving background, the veil over the case stack, and the menu's current label. A
design where each of those reads the platform's own scrolling independently drifts by a frame and
looks broken.

Input accumulates into a target position and the rendered position eases toward that target on every
frame, and the gap between the two is what gives the page its weight. Wheel and trackpad deltas are
normalised so a mouse and a trackpad feel like one device. A touch drag is one to one with momentum
that decays on the same curve as the wheel smoothing. The page and arrow keys move the target by
fixed amounts and the same smoothing carries them, and a menu jump sets the target directly and is
carried by the same smoothing, so a jump and a drag are the same motion rather than two. On a touch
device and under a reduced motion preference the smoothing is bypassed entirely and the platform
scrolls the document, because ordinary scrolling on a handset is better than anything invented here.
A menu jump lands on the top of its block less the height of the fixed chrome, so the block's first
line is never under the frame.

The sequence stops moving in five situations, and in every one of them the hold is the same
mechanism: while the arrival sequence runs, while an overlay is open, while the archive mode is
active, for the duration of a resize recalculation, and while a route transition runs. The hold
counts rather than toggling: two overlays opened and closed in an overlapping order must leave the
page still held while one of them is open, and scrollable the moment the last one closes. This is the
single most common defect in a page built this way.

Leaving and returning restores the exact rendered position rather than merely the target, and the
restored value survives a switch into the archive and back, an overlay opening and closing, and a
browser back that returns to the sequence.

### The moving background

A full window surface sits behind every block, and it is the thing that makes this read as the
studio's own work rather than as a template. It composites a near black cloth with soft folds, a
second copy of the same cloth that is never visible on its own and describes which way each fold
faces, one moving light that reads the second copy and lights the folds, a fine animated grain, and a
soft dark edge. The light follows the pointer where there is one and follows a slow automatic path
where there is not. The grain advances by a tiny amount every frame rather than cycling through
prepared frames, and it must not visibly repeat over a two minute observation.

The surface is not a backdrop. Both layers drift against the sequence at a small fraction of the
scroll distance, so the cloth reads as a wall a long way behind the page rather than as wallpaper
stuck to it. The whole surface fades out before the case stack arrives and fades back in after it,
because the stack's light cards need a quiet ground. A second pair of images takes over for the lower
half of the sequence, and only one region is mounted at a time: mounting both doubles the memory for
no visual gain, because they are never on screen together. A blur rises briefly while a case
transition runs and returns to nothing at rest.

Six effects are applied in order and each one can be switched off independently, because those
switches are the quality ladder: the parallax drift, a twist, a bulge under the pointer on the archive
wall, the blur raised during a case transition, the grain and its edge, and the scroll driven fade. A
single generated greyscale field is sampled to push the cloth around under the pointer and during a
case transition, and it is generated rather than shipped as a file.

Lifecycle. The surface's images load during the arrival sequence and count toward its progress. A
switch into the archive pauses and hides it rather than tearing it down. It keeps rendering behind an
overlay's scrim at reduced quality. It stops entirely while the tab is hidden and resumes on the next
visible frame. A lost rendering context remounts once and falls back permanently to one still frame
on a second loss. Under a reduced motion preference one frame renders and the loop never starts.
Every block of content is readable with the surface absent: it failing is a visual downgrade and
never an error state.

### The arrival sequence

The first seconds of the site, and the part most likely to be built as an afterthought. A full window
black state above every other layer holds four things: a progress numeral left of centre in the
numeral family at the largest display size, which travels toward the centre as it counts; a small
uppercase percentage reading beside it at caption size; a jagged hairline crack drawn downward
from the top whose lower end tracks the numeral; and the first two lines of the site's copy, already
set in the positions they will hold afterwards.

The numeral counts from `0` to `100` and the percentage matches it at every frame. The count is bound
to real progress and reports the proportion of the arrival manifest that has loaded, never a timer,
and it is monotonic and never runs backwards even if the manifest grows during the load. A counter
that runs on a fixed duration while assets are still arriving is the defect this rule exists to
prevent, and it is visible: the site becomes usable a beat after the counter says it is ready. The
manifest holds the four type faces, the moving background's two images for the upper region, the
generated field, and the first two case cover images; every other case image, all of the archive
imagery and the showreel sit outside it.

The crack's points are generated at run time rather than authored: it starts near the top, steps
downward in short segments, and offsets each step horizontally by a bounded random amount, so the
line reads as a crack rather than as a scribble. The same generated path is reused for the display
heading cuts, so it is generated once and stored rather than regenerated per consumer.

At `100`, in order: the numeral and the percentage fade; the crack completes to the bottom of the
window and holds for one beat; the black state lifts to reveal the hero already in place; the hero
display lines arrive one character at a time while the moving background begins rendering; and the
scroll hold releases as the two bands begin to move. The two lines at the bottom do not move at any
point during the exit. They are the fixed point the whole transition turns around, which is what
makes it read as an arrival rather than as a page load.

The sequence is never a hard gate. A repeat visit within the same session skips it entirely. A cached
repeat visit across sessions runs it to completion quickly and adds no artificial minimum duration. A
key press or a click during it completes it at once against whatever has loaded, and the rest arrives
behind the page. Under a reduced motion preference the crack is not drawn and the numeral does not
travel, but the count and the wait remain. A visitor arriving on a case address or on the archive runs
the sequence against a manifest that includes that destination's imagery. If loading runs past twenty
seconds the sequence exits regardless and the visitor reaches a usable page.

### The sequence blocks

The hero is four display lines stacked and overlapping at the largest display size, so the lines cut
into each other, each arriving one character at a time a beat behind the line above it. A short
statement is set small and centred in the gap between the display lines and arrives line by line
behind a moving edge, followed by a quieter statement in the caption tone that arrives the same way
after it. The showreel control sits to the right.

The studio seal is one circular composition that rises as a single group, reading in short runs around
a starburst at its smallest size, with the founding line in the caption tone.

The services run is a vertical list of the eight disciplines set in the condensed face, uppercase and
centred, with alternating words set in the display serif italic so the run reads as a sentence rather
than as a menu. Below the medium width it sets one discipline per line.

A case card is a light ground with square corners carrying its number top right in the display serif
at section heading size, its cover image top left filling roughly half the card's width in portrait,
its title in the display serif on the card's right half over two lines, and four lines of uppercase
caption beneath the title. The graded veil lies over the whole card and lifts to fully clear when the
card is pointed at. Below the medium width the image sits above the title and the card drops straight
from its most generous padding to its tightest, with nothing in between.

The awards board sets its heading across three display lines with the last part sitting alone, each
group name in the condensed uppercase face at section heading size, and each award row as the award
name at caption size in uppercase with its count in the same size, right aligned against it. A type
with no count renders its name alone at the same size and leaves no gap where the number would be.

The contact block leads with the studio's address at the largest display size in the signal colour,
underlined, using the tearing link treatment, above the uppercase qualifier in the caption tone. A
small circular seal reads in four short runs around a starburst. The footer carries four uppercase
lines, the outbound list in the display serif, a signing line, the copyright line naming the legal
entity, the smile, and the link to the privacy page.

### The case study surface

Opening a case from the stack grows the pressed card to fill the window while the background smears
behind it, over the longest of the shared speeds, and that transition is the one place the
background's blur and displacement are raised. Arriving cold on the address renders the same content
as a full page with a control that returns to the sequence and lands on that card.

The page carries a full bleed cover, the client and the year top left at caption size in uppercase,
the title in the display serif as the largest thing on the page, the summary in body copy at the dim
near-white tone, a two column list of credits by role and name, a wrapped run of small uppercase
discipline tags, and the body blocks in their stored order. Fixed controls at the left and right edges
carry the neighbouring cases' titles. The overlay walks the same ordered list the stack rendered
rather than fetching its own, so it can never present a case in a different order from the page behind
it.

### The archive wall

The wall clears to true black and fills the window. Items vary in size and are not aligned to a common
baseline. The plane repeats in both axes, so dragging far enough in any direction wraps and there is
always more; when the plane passes a wrap boundary its position jumps by exactly one plane width or
height and the jump must be invisible, which means it happens at a boundary where no item is mid
transition. Only items whose bounds intersect the window plus one window of margin are given an image;
everything else is a placed rectangle with no image, and that is what keeps a wall of several hundred
affordable.

Pressing and dragging moves the plane one to one and turns the pointer to the closed hand. Releasing
with velocity carries the plane on and decays it to a stop. A wheel pans vertically, and horizontally
on a two axis device. A pinch is ignored: the wall does not zoom. The wall is desaturated at rest and
returns to colour under the pointer, which swells the region slightly; a radial blur rises while the
plane is moving fast, and items smear along the drag direction while a drag is in progress. The
desaturation is the resting state rather than an effect, because a wall fully coloured at rest loses
its structure.

Entering fades the wall up from black while its first screen of imagery loads, and it is draggable
from the first frame even while imagery is still arriving; an item with no image yet is a flat
rectangle at the ground colour that fades its image in when it arrives. Pressing an item raises it out
of the wall to the centre of the window at its natural size with the rest of the wall dimming behind
it. Escape returns it to the wall, animating back to the position it came from. With fewer than nine
items the wall does not wrap and clamps at its bounds with a rubber band at the edge. A position
within the wall is deliberately not addressable: the wall is a place to wander, not a document to
cite.

### The quality ladder

Adaptive quality is a performance requirement here rather than a preference, because the moving
surfaces are the expensive part of this product. The product measures its own frame rate and steps
down through four steps, and a step taken downward
is held for the rest of the session so the page cannot oscillate between settings. At the top
everything runs. One step down the blur and the bulge are off while the light and the grain remain. A
step below that the twist, the light and the displacement are off, leaving a drifting image with a
grain. At the lowest step one frame renders and the loop stops. The decision is made over a rolling
window of frame durations rather than on a single slow frame, and never in the moments just after a
mode change, when a stall is expected. Where the connection reports itself slow or data saving is
requested, the lowest step applies from the start and the smallest imagery is loaded.

### Degradation

With the object store unreachable the generated patterns appear wherever an image would be and every
word stays in place. With the datastore unreachable the console is read only and says so, and no
console form loses what was typed into it. With the inquiry endpoint unreachable the form holds its
values and offers the studio's address as the way through. None of these is an error page.

## Constraints

- One studio, one site, one console. No second tenant, no client workspace and no account for
  anybody outside the studio.
- No email, no SMS and no push. An inquiry is acknowledged on the screen and answered in the studio's
  own mail application; a review link is issued in the console and handed over by the lead.
- No payments, no invoicing, no plans, no subscriptions and no cart. Nothing is sold here, and an
  inquiry carries a budget band rather than a price.
- No third party analytics, tag manager, bot-defence service, content platform, image transform
  service or font service. Nothing on any route calls out to another service at runtime.
- No scheduled publication and no background worker. Publication, the verification address check and
  the retention sweep are actions somebody takes in the console.
- No comments, no likes, no follows, no messaging, no public profiles and no site search.
- One language, English. No currency anywhere.
- No native app and no offline mode.
- The app stays responsive with the seeded estate plus a few hundred archive items, a few thousand
  stored inquiries with their events, and a few hundred award records.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
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

**API shapes.** Field names are exact. A list endpoint returns a top-level JSON array. A successful
call returns the named resource or shape; an invalid or unauthorized call is rejected as a client
error, never as a server error and never as a silent success, and carries a message naming the
reason.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | - | `status` |
| `GET /api/page` | - | the enabled sequence blocks in order: `component`, `position` |
| `GET /api/services` | - | the eight disciplines: `name`, `slug`, `menu_order` |
| `GET /api/cases` | - | published cases in `stack_order`: `slug`, `client`, `title`, `description`, `year`, `stack_order`, `veil`, `cover_url`, `disciplines` |
| `GET /api/cases/{slug}` | - | one published case with `summary`, `credits`, `blocks`, `live_url`, `awards`, `previous_slug`, `next_slug`; not found when it is not published and the caller is neither a member nor holding a valid review token for it |
| `GET /api/cases/{slug}/cover` | - | the stored bytes, under the same rule as the case itself |
| `GET /api/archive` | - | `seed`, `plane`, `items` each with `id`, `title`, `year`, `x`, `y`, `w`, `h`, `disciplines`, `case_slug`, `image_url` |
| `GET /api/archive/{id}/image` | - | the stored bytes |
| `GET /api/awards` | - | `bodies` each with `name` and `types`, each type with `name` and `count` |
| `GET /api/showreel` | - | `poster_url`, `renditions` |
| `GET /api/footer` | - | `lines`, `links`, `sign_off`, `copyright` |
| `POST /api/inquiries` | `name`, `email`, `company`, `budget_band`, `timeline`, `disciplines`, `message`, `consent`, `source_block`, `submission_key`, `form_opened_at`, `company_website` | `id`, `received_at`, `state`, or per-field errors |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `email`, `role` |
| `POST /api/auth/logout` | - | nothing |
| `GET /api/console/cases` | `state` | every case in any state: `slug`, `client`, `title`, `state`, `stack_order`, `current_revision`, `published_revision` |
| `POST /api/console/cases` | `slug`, `client`, `title`, `summary`, `description`, `year`, `disciplines` | the created case at `draft` |
| `PATCH /api/console/cases/{slug}` | any editable field plus `revision` | the case at its new revision, or a refusal carrying `current_revision` and the differing fields |
| `POST /api/console/cases/{slug}/blocks` | `kind`, `position`, `payload` | the created block |
| `POST /api/console/cases/{slug}/cover` | the image bytes, `alt_text` or `is_decorative` | `object_key`, `content_type`, `byte_size` |
| `POST /api/console/cases/{slug}/submit` | - | the case at `in_review` |
| `POST /api/console/cases/{slug}/approve` | `revision` | the recorded internal approval |
| `POST /api/console/cases/{slug}/publish` | - | the published case, or a refusal naming every condition that is not met |
| `POST /api/console/cases/{slug}/unpublish` | - | the case at `unpublished` |
| `POST /api/console/cases/reorder` | `order`, the full list of published slugs | each case with its new `stack_order` and recomputed `veil` |
| `POST /api/console/cases/{slug}/review-links` | `emails`, `expires_in_days` | one `token` per address with its `expires_at` |
| `DELETE /api/console/review-links/{id}` | - | nothing |
| `GET /api/console/archive` | - | every archive item with its plane rectangle |
| `POST /api/console/archive` | `title`, `year`, `intrinsic_width`, `intrinsic_height`, `disciplines`, `case_slug` | the created item and the regenerated layout |
| `POST /api/console/archive/{id}/image` | the image bytes, `alt_text` | `object_key` |
| `GET /api/console/awards` | - | every award record with its type and body |
| `POST /api/console/awards` | `award_type`, `won_on`, `verification_url`, `case_slug` | the created record |
| `DELETE /api/console/awards/{id}` | - | nothing |
| `GET /api/console/inquiries` | `state`, `assignee` | the queue newest first: `id`, `received_at`, `name`, `company`, `budget_band`, `state`, `assignee`, `spam_reason` |
| `PATCH /api/console/inquiries/{id}` | `state`, `assignee` | the updated inquiry |
| `POST /api/console/inquiries/{id}/notes` | `body` | the created note with its author and time |
| `POST /api/console/inquiries/{id}/erase` | - | the erased inquiry |
| `GET /api/console/audit` | - | the trail oldest first: `sequence`, `action`, `subject_type`, `subject_id`, `actor`, `created_at`, `prev_hash`, `hash` |
| `GET /api/console/media` | - | every media asset with its `object_key` and `state` |
| `GET /api/preview/{token}` | - | the one case revision the token names, or the expired shape |
| `POST /api/preview/{token}/decision` | `decision` of `approve` or `request_changes` | the recorded decision |
| `POST /api/preview/{token}/comments` | `block_id`, `body` | the created comment |

Bearer auth is required on every `/api/console` endpoint and on `POST /api/auth/logout`. The preview
endpoints authenticate by the token in the path and by nothing else, and a member's bearer token is
never accepted as a review credential.

**No mocks.** MinIO is the only place an uploaded image exists. An in-memory list of uploads, a
base64 string in a database column, a file written under the app's own directory, a placeholder image
shipped with the app, or a cover route that answers with bytes it generated itself are all the same
failure wearing different clothes. The named provider is the fact - the app's UI and its own tables
can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger reads the studio's sequence end to end, opens a case from the numbered stack and walks
sideways through it, drags the archive until it wraps, and sends a brief that lands in the console
queue already carrying its own state. A case the studio has not published stays unreadable to that
stranger, at its own address and at the address of the image behind it. A lead cannot publish a case
until the client has approved the exact revision being published, and every award count on the board
is the number of wins recorded against it.
