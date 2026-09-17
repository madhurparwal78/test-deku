# Expertise Led Casebook

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, the studio's owner must be able to open the app in a
browser and publish a case study that then appears under its expertise on the
public site, without hitting an error page. A stranger, whether signed in as a `visitor` or signed in as nobody, must
NOT be able to read a draft case study or fetch its cover by any means: not from
a list, not by typing its address, and not by requesting the cover bytes. Every
cover must live as a real object in the `minio` bucket at its scheme's key; a
copy on the app container's own disk does not count.

## Overview

`Northform` is the website of a small design and development studio, arranged
around the four kinds of work it does: `Real Estate`, `Corporate`, `Startups` and
`eCommerce`. Each expertise has a band on the front page carrying two case
studies the owner picked by hand, and a landing page of its own. Beneath them sit
the full work index, the case studies themselves, a company page, a contact page
where a visitor sends the studio a brief, and the privacy notice.

Behind the public site sits the studio. The owner signs in, writes a case study,
files it under one expertise, tags it, gives it a cover, and publishes it. The
owner orders the shelf that every public list follows, decides which two case
studies lead each expertise on the front page, and reads the briefs visitors
send. An editor can write alongside the owner but cannot publish, order, feature,
delete or read a brief.

There is no blog, no article, no career page, no cart, no payment, no search box,
no comment thread on a case study and no rating. Nothing on the public site changes while a visitor is
looking at it.

The genuinely hard part is the boundary between a draft and the public, held at
the server for the case study, its address and its cover bytes alike, together
with the eight front-page slots: releasing a slot must never unpublish the case
study that held it.

## User roles

| Role | Can do |
|---|---|
| anonymous visitor | reads every published page, filters the work, sends a brief. **Cannot** reach any studio route, read a draft, or fetch a draft's cover. |
| `visitor` | what signup creates. Everything an anonymous visitor can do, and nothing more. **Cannot** reach any studio route or call any studio endpoint. |
| `editor` | signs in; reads every case study, draft or published; creates and edits case studies; sets a cover; sees their own sessions. **Cannot** publish or unpublish, delete, reorder the shelf, fill a feature slot, read or change a brief, read the page-view log, or see the unread brief count. |
| `owner` | everything an editor can do, and publishes, unpublishes, deletes, orders the shelf, fills the eight feature slots, reads, archives and deletes briefs, and reads the page-view log. There is exactly one owner. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from an `editor`
session to any `owner`-only endpoint must be rejected by the server (an
unauthorized request is denied, not served), leaving the protected state
unchanged. The same holds for a `visitor` session and for a caller with no
session at every studio endpoint.

Signup is open at `POST /api/auth/signup` and always creates a `visitor`, however
the request is shaped. The owner and the editor are seeded and are never created
through signup.

Seeded accounts, each with the password `deku-demo-pw-2026`:

| Email | Role | Display name |
|---|---|---|
| `owner@example.com` | `owner` | `Mara Lind` |
| `editor@example.com` | `editor` | `Jonas Weller` |
| `visitor@example.com` | `visitor` | none |

## Core features

**1. The publish boundary.** Every case study is a draft until the owner
publishes it. A draft is **absent** from every public response: from `/work`,
from every expertise landing, from the front page, from the sitemap, and from
every other case study's next link. A public request for a draft's address,
through the API or the page, is answered not found and the answer reveals nothing
about whether such a case study exists. A draft's cover bytes are refused to
everyone who is not signed in as the `owner` or an `editor`. Publishing makes the
listing, the address and the cover readable in one act. `Pinemark Mobile App`
is seeded as a draft, so `/work/pinemark-mobile-app` answers not found.

**2. Withdrawn is not the same as never published.** Unpublishing a case study
takes it off every public list at once and makes its cover private again. A case
study that was public and has been taken off answers with the gone status and
the surface `No longer here`, rather than not found. `Ostend Loyalty Store` is
seeded as withdrawn, so `/work/ostend-loyalty-store` answers gone.

**3. Publishing needs three things.** A case study is published only when it has
an expertise, at least one tag and a cover carrying alternative text. A publish
missing any of them is refused, nothing changes, and the refusal names what is
missing with exactly one of these lines, checked in this order so the first
missing thing is the one named: `Choose an expertise before publishing.`,
`Add at least one tag before publishing.`, `Add a cover before publishing.`.
Saving never publishes, and publishing is its own act.

**4. Covers live in the object store.** A cover is a PNG image the app draws and
stores in `minio`, the S3-compatible object store, at the key
`covers/{case_study_id}/{sha256_of_bytes}.{ext}`, for example
`covers/7/9f2a...d0.png`. There is no upload anywhere in the product: the studio
sets a cover only by pressing `Generate cover`, which draws a cover from the case
study's cover seed, a whole number from `0` to `999999`, in one of three
palettes, `mono`, `warm` or `cool`. The same seed and palette always draw the
same picture, byte for byte. `Generate cover` draws from the saved seed and
palette; changing either in the editor saves the case study first. The database row records where the bytes are; the
bucket is where they are. Every cover row carries its intrinsic width and height
and its alternative text, and a cover without alternative text is refused.
Generating twice from the same seed and palette for one case study resolves to
one object.

**5. Every write carries the version it read.** Each case study, each feature
slot and the shelf carries a whole-number `version`, `1` when created and one
higher after every accepted write to it; for a case study that includes setting a
cover, publishing and unpublishing. A write to a case study, a slot or the shelf
that sends an older version, or no version, is refused as a conflict with the message
`This changed somewhere else while you were working.`, and nothing changes.
Two simultaneous writes from the same version: exactly one is accepted and the
other is refused. Nothing is ever merged automatically; the studio shows the
conflict in place with `Keep mine` and `Take theirs`, and writes nothing until
the person chooses.

**6. Creating twice by accident creates once.** A request that creates a case
study or a brief may carry an `Idempotency-Key` header. Repeating it with the
same key within 24 hours returns the first answer and creates nothing new. This
is what makes a retry after a dropped connection safe.

**7. The shelf is one order.** Every case study has a place on the shelf, and
`/work`, every expertise landing and every next link follow that order, never
recency. The owner reorders it at `/studio/shelf` by dragging a row or by putting
the keyboard on a row's handle and using the arrow keys; both work, and a reorder
is applied optimistically and saved with `Order saved.`. A reorder names every
case study once and carries the shelf `version` it read. A reorder sent with an
older or missing shelf version is refused as a conflict: the rows animate back
to the saved order, the shelf shows
`This changed somewhere else while you were working.` followed by
`The order changed. Yours was not saved.` with `Keep mine` and `Take theirs`, and
nothing changes until the owner chooses. An accepted reorder raises the shelf version by one and
leaves every case study's `version` as it was. A
case study taken off the public site **keeps its place**: publishing it again returns it to where the
owner left it, not to the end. A new case study joins the end of the shelf.

**8. Eight feature slots, filled by a person.** The front page shows exactly two
case studies under each expertise, and which two is the owner's choice, never the
two most recent. There are eight slots, two per expertise. A slot holds one
published case study of its own expertise, or nothing, and a case study holds at
most one slot. A slot offered anything else refuses it. Filling a slot shows
`Featured on the home page.`; emptying one shows
`No longer featured. Still published.`. **When a slot takes a new case study, the
case study that was there stays published and stays on `/work`**: it has been
moved off the front page, not withdrawn. Writing a slot never writes to a case
study.

**9. The front page.** `/` opens on the flat pale grey with the three-line
headline `Design.`, `Development.`, `Mastership.`, the third line set in white,
the circle cluster, and the statement
`We design and develop exceptional digital products & services, eCommerce, and brand communication solutions.`
Below it sit the full-width bar `Select an expertise`, which jumps down the page
and is not a filter, then the showreel panel labelled `Watch` and `Showreel`,
then four expertise bands, each with its number in a circle from `01` to `04`,
its name, its sentence, a `Learn More` control to its landing, and the two
featured case studies side by side. An empty slot shows nothing in its place,
and the band never fills the gap with a recent case study.
Then `Our Capabilities` with five items, the company band with the figure `20+`
over `Years of experience` and `More About Us`, the dark client strip of seven
names that a visitor drags sideways, with a paragraph revealed when a name is
pointed at, and the footer.

**10. The work index.** `/work` shows every published case study, in shelf order,
as two columns of cards, with no paging. Each card carries the cover at twice as
wide as it is tall, the title, and the case study's tags joined by a comma and a
space. Above the grid, a row of filter chips that scrolls sideways and never
wraps: `All Works` first, which clears every filter, then the four expertises,
then an `Industries` group holding the eleven tags. The filter lives in the
address as `?expertise=<slug>` and a repeatable `&tag=<slug>`. Two tags show case
studies carrying either tag; an expertise with a tag shows case studies carrying
both. A value the site does not know is dropped and the address is rewritten
without it. The back button undoes a filter and a reload keeps it. When nothing
matches, the grid is replaced by `Nothing matches that.`, a line naming the
active filters, and `Clear filters`. **An expertise and a tag are separate
things** even where the tag `Real Estate` shares a name with the expertise
`Real Estate`: filtering on one never filters on the other.

**11. A case study.** `/work/<slug>` opens with the title set very large, a
breadcrumb trail, the client and the year, then the cover running the full width,
then the body, then the next published case study in the whole shelf order,
whatever filter the visitor arrived from, wrapping from the last back to the
first. The body is built from six kinds of block and no seventh:
`paragraph`, `heading`, `image`, `image_pair`, `quote` and `facts`. A seventh kind
is refused when saved. Going back to `/work` returns the visitor to where they
were in the list rather than to the top.

**12. The expertise landings.** `/expertise/real-estate`,
`/expertise/corporate`, `/expertise/startups` and `/expertise/ecommerce` open like
the front page, on the pale grey with the expertise name set enormous and the
circle cluster, then the expertise sentence, then every published case study of
that expertise in shelf order, then an invitation to get in touch.

**13. The brief form.** `/contact` carries `We operate worldwide. Choose the office nearest to you`
over the two offices `Riga, Latvia` and `Oslo, Norway`, then the heading
`Get in touch` and a form with the fields, in order, `Your name`,
`Company name` marked `(optional)`, `Phone number`, `E-mail` and `Comment`, then an
optional choice of expertise, then an optional choice of budget whose
values are `under_25k`, `25k_to_75k`, `75k_to_150k` and `over_150k`, shown to
the visitor as `Under 25k`, `25k to 75k`, `75k to 150k` and `Over 150k`, then the
consent line
`By clicking the Submit button you agree to our Privacy Policy terms`, then the
large round `Submit` button. The phone field formats itself as it is typed, keeps
only the digits and a leading plus, and never moves the caret backwards.

Validation, stated per field and enforced by the server as well as the page:

| Field | Rule | Inline message |
|---|---|---|
| `name` | 1 to 80 characters after trimming | `Tell us what to call you.` |
| `company` | 0 to 120 characters | none |
| `phone` | optional; if present, 6 to 20 digits | `That number looks incomplete.` |
| `email` | 1 to 254 characters, one at sign with text either side, no spaces | `That address will not reach you.` |
| `comment` | 10 to 4000 characters after trimming | `A few more words, please.` |
| `comment` | at most two web addresses | `Fewer links, please.` |
| `expertise` | optional; if present, one of the four expertise slugs | `Choose one of the listed expertises.` |
| `budget` | optional; if present, one of the four budget values | `Choose one of the listed budgets.` |

A comment that breaks both comment rules shows only `A few more words, please.`.

Pressing `Submit` on an empty form shows every message under its field; the
button is never greyed out, anywhere in the product. A brief the server refuses
leaves every field holding what was typed. An accepted brief replaces the form in
place with `Thank you!`, `We'll be in touch soonest!` and a `Homepage` control,
and the page the visitor was on is recorded with the brief as its `source_path`.

**14. Spam and abuse are refused without asking anything of a person.** The form carries a
field named `website` that people never see and that must stay empty, and a
`form_token` taken from `GET /api/briefs/token` when the form is built. Tokens are issued by the server and each is good for one brief. A brief whose
`website` is filled, or whose `form_token` is missing, was not issued by the
server, has already been used, or is less than two seconds old, is spam: it gets
the same answer an accepted brief gets, and nothing is stored. A
fourth brief from the same e-mail address within one hour is refused without
saying what the limit is. There is no puzzle and no image challenge.

**15. The brief inbox.** Every accepted brief lands at `/studio/inbox` as
`unread`. Only the `owner` reaches it. The list shows the sender's name, company,
the expertise and budget they chose, the first line of the comment, and when it
arrived, newest first, with unread rows at full strength and read rows faded. At
a wide window the list and the opened brief sit side by side, and the opened brief
also has its own address, `/studio/inbox/<id>`. The opened brief shows the whole
comment, the phone and address as label and value pairs, and the page it was sent
from, with `Archive`, `Mark unread`, `Delete` and `Reply`, which opens a mail
composition to the sender. Opening a brief in the inbox marks it `read`, by the
same state change the API offers; `GET /api/studio/briefs/{id}` on its own changes
nothing. Archiving makes a brief `archived`. **A brief's text is shown exactly as typed and nothing in it is
ever treated as markup**: no link comes alive, no picture loads, and a tag typed
into a comment appears as its characters. The seeded brief from `Ines Duval`
carries such a comment. The rail shows the unread count beside `Inbox`, and a
brief arriving while the inbox is open appears at the top without the list
scrolling under the reader. The unread count and the inbox list are the only
real-time parts of the product.

**16. The dashboard.** `/studio` shows tiles: `Published work` and `Drafts` for
everyone who signs in, and `Unread briefs` for the owner only. For an editor that
tile is **absent**, not zero, and the dashboard's data carries no unread count at
all. Under the tiles, the ten most recently changed case studies and briefs,
newest first, each row a link to what it names; an editor's list carries case
studies only. Each `recent` row carries `kind` (`case_study` or `brief`), `id`,
`title` and `changed_at`.

**17. The case study editor.** `/studio/work/new` and `/studio/work/<id>` are
their own routes. Fields: `Title` (1 to 120 characters), a slug derived from the
title when the case study is created and editable in the editor (lowercase words
joined by hyphens, unique), `Client` (0 to 80),
`Year` (four digits from `1990` to the current year), one expertise, any of the
eleven tags, `Summary` (0 to 280), the cover seed with a shuffle control, the
cover palette, the body, and the cover with its alternative text. A block is added
by pressing a plus between two blocks and choosing one of the six kinds from a
list, never by dragging from a palette, so the whole editor works from the
keyboard. `Save` writes and leaves the published state alone, and the status line
reads `Saved just now.`. `Publish` and `Unpublish` appear for the owner only and
report `Published. It is on the site now.` and
`Unpublished. It is off the site.`. A server refusal puts the server's message
under the failing field and moves focus there. A slug is assigned once and a
later title change leaves it alone; a slug already in use is refused with
`That address is already used by another case study.`.

**18. Signing in.** `/sign-in` takes an address and a password. A wrong address
or a wrong password is refused with the same line,
`That did not match. Check both fields and try again.`, never naming which half
was wrong. Five failed sign-ins in a row lock the account for fifteen minutes,
and during that time even the right password is refused with a line beginning
`Too many attempts.`. A signed-out request for any `/studio` route is sent to
`/sign-in?next=` followed by the intended path, and after signing in the person
lands on that path; a return path that is not a single leading slash followed by a studio
route is discarded and the person lands on `/studio` instead.

**19. Sessions.** `/studio/account` lists every live session of the signed-in
account with a short description of the browser, when it started and when it was
last used, marks the current one, and says
`A revoked session ends the next time it is used.`. `GET /api/sessions` returns each
session with `id`, `user_agent_summary`, `created_at`, `last_seen_at` and
`current`, which is true for the session making the request. `Sign out
everywhere`, the one control in the product that asks the person to type to confirm, ends every session
of the account, including the current one: every token the account held is
refused from then on.

**20. The refusal page.** A signed-in person reaching a studio route their role
does not allow sees a designed page inside the site's own frame, not a redirect
and not a blank: the code `403` set at display size, `Not permitted`, and a
`Back to studio` control, with the rail still present minus what the role cannot
reach. On the inbox the page adds `Briefs are visible to the owner only.`.

**21. Not found, gone, and the privacy notice.** An unknown address answers
not found, inside the site's own frame, with `404` set as large as the front
page headline, `Not found`, and `Back to work`. The requested path is never
printed back into the page. The gone surface reads `410`, `No longer here` and
`Back to work`. `/privacy-policy` states that the site records each public page
view as its route and its time, keeps what a brief's sender typed, and keeps the
cookie choice in the visitor's own browser; it is the only page that ends without
an invitation to get in touch.

**22. The page-view log.** Every view of a public route records one row carrying
the route and the time. A page view reported for a studio route is accepted and stored nowhere. Only the `owner` reads
the log, newest first, at `/studio/page-views`. Nothing about the visitor is
recorded beyond the route and the time: no address, no identifier, no cookie.

**23. Titles, descriptions and the sitemap.** Every public route sets its own
title and its own description, and no two public routes share either. The titles
are `Digital Product Design & Development Agency | Northform` for `/`,
`Work | Northform`, the case study title followed by ` | Northform`, the expertise
name followed by ` | Northform`, `Company | Northform`,
`Northform's Contact Details | Northform` and `Privacy Policy | Northform`; the
studio is `Studio | Northform`. `/sitemap.xml` lists every public route, including
every published case study and every expertise landing, and no draft or withdrawn
case study. `/robots.txt` names the sitemap and keeps crawlers out of `/studio`.

**24. Every picture is named.** Every content image carries alternative text:
a cover by the text its author wrote, a client name by the client. Decorative
marks, the circle cluster, and the generated loops declare themselves decorative
and are hidden from assistive technology.

**25. A new site is not blank.** A fresh installation already knows the four
expertises in their order, carries the eight slots, and lays the front page out
properly, so the first thing a new owner sees is a working site. Everything the
studio writes has persistence on the server and follows the person to any
machine; only the cookie choice, an unsent brief and a list's filters live in the
browser. A fifth expertise would take a database migration; the studio offers no way to
add one.

**26. Nothing typed is thrown away.** A timeout, a refusal or a dropped connection
never clears a form. With the network off, the brief form says
`You are offline. Your brief is saved here and will send when you reconnect.`,
holds the brief in the browser, and sends it once when the connection returns. A
case study form whose session has expired keeps its fields and offers a sign-in.

## User flow

| Route | Who reaches it | What is there |
|---|---|---|
| `/` | anyone | headline, expertise bar, showreel, four expertise bands, capabilities, company, clients |
| `/work` | anyone | every published case study, filterable in the address |
| `/work/<slug>` | anyone, published only | one case study and the next |
| `/expertise/<slug>` | anyone | one of the four landings |
| `/company` | anyone | statement, figures, capabilities, clients |
| `/contact` | anyone | the offices and the brief form |
| `/privacy-policy` | anyone | the privacy notice |
| `/sign-in` | signed out | the sign-in form |
| `/studio` | `owner`, `editor` | the dashboard |
| `/studio/work` | `owner`, `editor` | every case study, draft or published |
| `/studio/work/new`, `/studio/work/<id>` | `owner`, `editor` | the case study editor |
| `/studio/shelf` | `owner` | the order and the eight slots |
| `/studio/inbox`, `/studio/inbox/<id>` | `owner` | the briefs, list beside detail |
| `/studio/page-views` | `owner` | the page-view log |
| `/studio/account` | `owner`, `editor` | sessions and sign out everywhere |

**Entry and redirects.** A signed-out request for a studio route goes to
`/sign-in` with the intended path, and signing in lands there. A signed-in person
opening `/sign-in` lands on `/studio`. An `editor` or a `visitor` opening a route
their role does not allow sees the refusal page. A session that has ended
mid-edit refuses the next write, keeps the form, and offers sign-in. The header's
`Expertise` control is a button that opens a panel of the four expertises, not a
link; the panel closes on the same control, on the Escape key, and on any
navigation.

**The owner publishes and features.** Opens `/studio/shelf` signed out and is
sent to `/sign-in`, signs in as `owner@example.com`, and lands on
`/studio/shelf`. Goes to `/studio` and presses `New case study`. Types the title
`Aster Row Residences`, the client `Halden`, the year `2025` and a summary,
chooses `Real Estate` and the tag `Real Estate`, and presses `Save`: the status
reads `Saved just now.` and nothing is public yet. Chooses the palette `warm`,
writes the cover's alternative text, presses `Generate cover`, then `Publish`:
`Published. It is on the site now.`. Opens `/work` and finds it last. Opens
`/expertise/real-estate` and finds it in the work band. Opens `/studio/shelf`,
puts `Aster Row Residences` into the second `Real Estate` slot, and reloads `/`
to see it under `Real Estate`. `Harbour Quarter`, which held that slot, is still
on `/work`.

**The visitor narrows the work and sends a brief.** Lands on `/`, presses
`Select an expertise`, opens `/work`, chooses `Corporate` and the address gains
`?expertise=corporate`, adds the tag `Banking`, opens `Kestrel Annual Review`,
reads it, follows the next case study, and goes to `/contact`. Presses `Submit`
on the empty form and reads a message under each required field. Fills the form
and submits: `Thank you!` replaces the form where it stood.

**The owner reads a brief.** Signs in, opens `/studio/inbox`, opens the brief
from `Ines Duval`, sees the markup in her comment as plain characters, and
archives it.

**The owner withdraws and republishes.** Opens `Northline Self Care`, presses
`Unpublish`, and sees it gone from `/work`. Presses `Publish` again and sees it
back on `/work` in the same place.

**A wrong address.** `/work/pinemark-mobile-app` shows `Not found`,
`/work/ostend-loyalty-store` shows `No longer here`, and an address that was never
a page shows `Not found`.

**The editor is refused.** Signs in as `editor@example.com`. The dashboard shows
`Published work` and `Drafts` and no `Unread briefs`. Opening `/studio/inbox`
shows `Not permitted` and `Briefs are visible to the owner only.`. The editor's
case study editor carries `Save` and no `Publish`.

**States.** Every list and page has a loading state that carries words, an error
state that offers a way forward, and an offline state; a region never goes blank,
and nothing changes size when its state changes. A loading placeholder does not
shimmer or pulse.

## UI/UX notes

The north star: a visitor should understand in the first moment that this is a
studio with a point of view, stated in three enormous words and nothing else, and
that the work beneath is sorted by what the studio is good at. The register is
editorial for the public site and quiet and operational for the studio, which
uses the same header, the same type and the same greys so an editor never feels
they have left the product.

**Colour is three values and their strengths.** A near-black neutral with the
faintest cool cast is the ink, and a near-white neutral is the ground; a second
near-white neutral, a flat pale grey, is the ground of the opening screen and of
the grey bands. Everything else on screen is the ink or the white at a lower
strength, and the pale strengths over the ink are not a mirror of the dark
strengths over the white. The one alarm colour, a light, soft red, marks a failed
field and nothing else; the error sentence itself is set in the ink so it stays
readable. True black exists only in the print stylesheet. Covers are the only
place colour is loud, and nothing ever tints them. The exact shades are yours, so
long as the ink reads as ink rather than as a hole in the page and the site holds
those three values. Ink over pale must meet WCAG AA contrast, and a raised
contrast setting darkens the faint captions and switches on when the system asks
for more contrast.

**Panels decide their own ink.** A heading is told it is a heading, never what
colour to be; the panel it sits in decides dark on pale or pale on dark, so the
page alternates white, grey and near-black bands with every component existing
once. The one deliberate exception is the opening headline's third line, white on
the grey. When a band boundary passes under the header, the header's words fade
across rather than flipping.

**Mode and meaning.** The site is designed light-first, with the dark bands as
part of that one design; there is no separate dark mode to switch to. Success and
in-progress are said in words on the status line, in the ink, never by colour
alone, and borders are the ink at a low strength. The primary action is the solid
dark pill, and its hover is the rolling label described below. Touch targets are
comfortably sized, and every icon-only control carries a text label for assistive
technology.

**Stance.** Space over dividers. Stillness over decoration. Links never underline
and never move: pointing at one fades it to half strength and that is all. There
is exactly one drop shadow in the product, on the cookie bar; a card with a shadow
has left the design. Each page leads with one primary action, set apart from every
secondary control: on `/contact` it is the large round `Submit`, on the studio
dashboard it is `New case study`.

**Motion.** The motion character is eased and long-tailed: almost everything
that moves uses one curve that starts quickly and takes a long time to settle, so
nothing seems to stop abruptly. A second, sharper curve is kept for what sits over
the page, the header arriving from just above the screen on load and the cookie
bar sliding in sideways. Headings animate in letter by letter, each letter rising
from just below the line slightly after the one before, which reads as type being
set rather than as a fade. The circle cluster draws itself on, each circle
starting from a different point of its own outline, and is the slowest thing on
the page. A pill button's label rolls upward on hover, the old word leaving
through the top as the same word arrives from below. Nothing slides sideways as
the page scrolls, nothing loops except the loading spinner, pages do not fade on
navigation, and no control grows when pointed at. A reduced-motion preference
removes the letter rise, the draw-on and the smooth scrolling.

**Density.** Spacious and rhythmic: the vertical rhythm is generous and every gap
belongs to one scale, so bands read as separate without a dividing line. Forms
have no boxes: a field at rest is its label and some space; focusing it lifts and
shrinks the label and draws a thin rule across from the left.

**Responsive.** The layout is decided by the window's shape, not its width alone,
so a phone held sideways never receives a tablet layout that does not fit its
height, and the larger layouts need enough height before they appear. There are
five sizes. Type scales smoothly between the two wide sizes and steps down on a
phone, and the body text on a medium window is slightly smaller than on a phone,
which is intended. At a phone viewport the header collapses to the wordmark and a
two-line menu glyph, the work grid keeps two columns, and nothing scrolls
sideways except the filter row. A print stylesheet sets text in true black.

**Accessibility.** Keyboard navigation reaches every control with a visible focus
outline that is managed, never removed. A heading split into letters for its
animation is read by assistive technology as one piece of text, with the letters
hidden, and the component that splits it is the one that provides the whole text.
Icons are hidden from assistive technology. Reordering the shelf works entirely
from the keyboard and announces each new position. A reduced-motion preference
hands scrolling back to the browser.

## Front-end specification

### Type

One family, `Inter Tight`, in two weights: `400` for body, interface and
captions, `500` for headings and for the navigation item of the current page.
There is no third weight. Sizes at a wide window: display `180px` (the opening
headline, the company figure, a failure code), first heading `90px`, third heading
`38px`, body `22px`, interface `16px`, small `14px`, caption `12px`, and `10px`
for the breadcrumb and the consent line, which never scale and never track.
Tracking is negative everywhere and tightens as type grows, tightest at the
display size. Fallback: `"Helvetica Neue", Helvetica, Arial, system-ui, sans-serif`,
adjusted so the swap does not reflow the headline.

### Global chrome

The header is thin and sticky: the wordmark `Northform` on the left, the
`Expertise` control, and the links `Work`, `Company`, `Contact` on the right. The
expertise panel lists the four expertises; pointing at one plays a short silent
generated loop beside the list, created the first time the panel opens and
stopped when it closes, and it never delays the panel. Four button roles: a pale
pill, a solid dark pill, a small square on a card holding a plus, and a small
square in the header. The footer carries `Get In Touch`, the five social links
`Network One`, `Network Two`, `Network Three`, `Network Four`, `Network Five`
stacked with thin rules between them, the copyright sign followed by
`1998` and the current year joined by a hyphen, and `Privacy Policy`. The cookie
bar reads `This website uses cookies` with `Accept`, remembers the choice in the
browser, and is the one element with a shadow. The skip link reads
`Skip to content`.

### Iconography

Nine marks drawn inline: a small down arrow, a down arrow, a left arrow, a right
arrow, a plus, a close cross taller than it is wide, a two-line menu glyph of two
long thin rules, a close glyph for the phone menu, and the studio's mark. Every
mark is straight lines, right angles, exact diagonals or circles, unfilled, with
square ends and never rounded ones. The circle cluster is a set of overlapping
outlined circles, each drawn as a dashed line with one long gap turned to its own
angle, which is why they start drawing from different places.

### Cards, covers and other media

A card is the cover at two to one, then the title, then the tags. A small square
block is notched into the cover's bottom right corner in the opposite panel colour,
holding the plus button. On the work index the corner block alternates in a
checker; on the front page the two cards of a band alternate. Covers keep their
full colour. A generated cover is drawn on a twelve-by-six grid with three to
seven rectangles, circles or quarter arcs, at most one filled, over the palette's
ground: `mono` is a white ground with ink marks, `warm` is the pale grey ground
with ink marks and the alarm colour on at most one shape, `cool` is an ink ground
with white marks. A faint grain lies over every generated cover. The site's only loud imagery is
its covers. Generated covers are a substitution for photography, not its equal:
they are consistent and plainer than real client work, and this build is the
evidence-free starting point the studio later dresses.

### Zero-asset substitution

The build ships no photograph, no video and no image file of its own. Every
cover, the showreel and the four expertise loops are generated, and the only files
shipped beside the code are the font files for `Inter Tight`.

### The cursor and the showreel

On a laptop, pointing at the showreel shows a small round label beside the pointer
reading `Watch showreel`, and pointing at the client strip shows one reading
`Drag`; the label trails the pointer a moment behind and never replaces it. It
does not exist on touch devices. The showreel is a generated loop of the circle
mark drawing itself on a dark ground, played in the page's own player, and nothing
loads until it is pressed.

### The scroll system

At the two wide sizes the site smooths scrolling itself; at a phone size the
browser scrolls natively. The takeover keeps every browser behaviour working:
arrow keys, page keys, jumping to an in-page link, find-on-page, and the back
button returning to the previous position. When the smoothing cannot keep up on a slow machine it hands
scrolling back to the browser for the rest of the visit, and that plain version is
fully correct.

### Architecture of the front end

The public site and the studio are two separately loaded parts that never load
together. Four shared pieces carry the whole design: the type, the buttons, the
form fields and the case study card.

### The copy deck

Every string below is exact.

Expertise sentences, in order:

| Number | Name | Slug | Sentence |
|---|---|---|---|
| `01` | `Real Estate` | `real-estate` | `Luxury real estate website design - iconic websites for iconic properties.` |
| `02` | `Corporate` | `corporate` | `Inspiring, functional, and result-oriented websites for enterprises. Full-cycle award-winning solutions from strategy to launch.` |
| `03` | `Startups` | `startups` | `From idea to a product: creating successful digital services for innovative startups and established businesses.` |
| `04` | `eCommerce` | `ecommerce` | `High-class eCommerce solutions with research-grounded UX design, award-class UI design and top-grade front-end.` |

Capabilities, under `Our Capabilities`:

| Heading | Body |
|---|---|
| `Web & mobile apps` | `Services, self-care, eCommerce, payments, custom apps for enterprises and startups.` |
| `UX & product design` | `User research, journey maps, prototyping, value proposition validation, design iterations, design systems and interface kits.` |
| `Product development` | `Minimum viable and lovable products, fast prototyping, agile development, modern front-end frameworks, a mature back-end framework, cloud infrastructure, support, maintenance, scaling.` |
| `Award-class web design` | `World-class advanced promotional and corporate creative websites.` |
| `Communication design` | `Naming, branding, communication strategy, 3D, print, copywriting.` |

Company: `Company`,
`We are a strategic partner to our clients. We will help you to ideate, design and implement your product from beginning to end.`,
`20+`, `Years of experience`, `More About Us`.

Clients, in order: `Meridian Air`, `Halden`, `Northline`, `Kestrel Bank`,
`Ostend Credit`, `Vantage`, `Pinemark`.

Tags, name and slug: `Promo Website` `promo-website`, `Corporate Website`
`corporate-website`, `Online Store` `online-store`, `Self-Service`
`self-service`, `SaaS` `saas`, `Banking` `banking`, `Customer Portal`
`customer-portal`, `Trading Platform` `trading-platform`, `Branding` `branding`,
`3D & Visualisation` `3d-visualisation`, `Real Estate` `real-estate`.

Studio rail: `Work`, `Shelf`, `Inbox`, `Page views`, `Account`, with the owner-only
items absent for an editor. Studio controls: `New case study`, `Save`, `Publish`,
`Unpublish`, `Delete`, `Generate cover`, `Archive`, `Mark unread`, `Reply`,
`Keep mine`, `Take theirs`, `Sign in`, `Sign out everywhere`, `Back to studio`,
`Back to work`.

An empty slot on the shelf reads `Nothing featured.`.

## Technical requirements

The browser receives a single-page application built with `Angular`, and the
server is `Express`, both written in TypeScript; the server answers the HTTP API under `/api` on the site's own
origin and hands the production build to every other path, so a deep link such as
`/work/harbour-quarter` opens that route directly. Titles and descriptions are set
per route as each route renders.

Case studies, tags, expertises, slots, briefs, sessions, accounts and page views
live in `PostgreSQL`, reached at `DATABASE_URL`. Every cover lives in `minio`, the
S3-compatible object store at `STORAGE_ENDPOINT`, in the bucket named by
`STORAGE_BUCKET`, with the key pair from `STORAGE_ACCESS_KEY` and
`STORAGE_SECRET_KEY`. Cover bytes reach a browser through the app's own
`GET /api/covers/{id}` route, which checks the case study's state on every
request: a published case study's cover is public, and any other cover needs the
bearer token of an owner or editor. The bucket is never exposed directly. People sign in with an email and a
password the app checks itself; passwords are stored hashed; `POST
/api/auth/login` returns an `access_token` that the API accepts as a bearer
token, and the browser may carry the same token in a cookie that scripts cannot
read. `GET /api/health` answers `200` once the app is ready, and each request the
server handles writes one line to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, cache, queue, object store, identity provider or mail vendor:
the only backing services available in this environment are `PostgreSQL` and
`minio`, and reaching for anything else is a contract violation. Hosts, ports,
keys and passwords come from environment variables and none is written into the
code.

**Nothing the browser downloads carries a credential.** No object-store key, no
database password and no token belonging to anyone other than the person signed in
appears in any script, stylesheet, document or source map.

**Security headers.** Every response carries a content-type options header that
refuses sniffing, a frame restriction that denies framing, a referrer policy, and
a content security policy permitting scripts and styles from the site's own origin
only.

**Rejections have one shape.** A refused request answers with a client error and
the body `{"error": {"code": "...", "message": "...", "fields": {...}}}`, where
`code` is one of `bad_request`, `unauthenticated`, `forbidden`, `not_found`,
`gone`, `conflict`, `unprocessable`, `rate_limited` and `locked`, `message` is the
line the product shows, and `fields`, present only for `unprocessable`, maps each
failing field name to its inline message. A refusal is never a server error and
never a silent success.

**Performance.** The first page appears quickly and is usable soon after on an
ordinary three-year-old laptop. The showreel downloads nothing until it is
pressed, and the expertise loops are drawn rather than fetched. On a slow machine an
animation takes the same time as on a fast one.

**The running site calls nothing outside this environment.** The page-view log is
the app's own and replaces any analytics service.

## Data model

Eleven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account.

**accounts.** `id`, `email` (unique, compared without regard to case),
`password_hash`, `display_name`, `role` (one of `owner`, `editor`, `visitor`),
`failed_attempts`, `locked_until`, `created_at`.

**sessions.** `id`, `account_id`, `token_hash` (a hash of the token, never the token itself),
`user_agent_summary`, `created_at`, `last_seen_at`, `expires_at`, `revoked_at`.

**expertises.** `id`, `slug` (unique), `name`, `sentence`, `position` from `0` to
`3`. Exactly four exist, seeded, and the studio offers no way to add a fifth.

**tags.** `id`, `slug` (unique), `name`. Exactly the eleven in the copy deck.

**case_studies.** `id`, `slug` (unique), `title`, `client`, `year`,
`expertise_id` (empty until chosen), `summary`, `cover_seed`, `cover_palette`
(one of `mono`, `warm`, `cool`), `cover_id` (empty until a cover is set), `blocks`
(the ordered body blocks), `position` (the shelf place, unique across every case study
whether published or not), `published`, `published_at` (empty while unpublished),
`withdrawn_at` (set when a published case study is taken off, cleared when it is
published again), `author_id` (kept when the author's account is removed),
`version`, `created_at`, `updated_at`.

**case_study_tags.** `id`, `case_study_id`, `tag_id`; a pair appears once.

**covers.** `id`, `case_study_id`, `object_key` (unique), `content_type`,
`byte_size`, `sha256`, `width`, `height` (never empty), `alt_text` (never
empty), `created_at`.

**shelf.** `id`, `version`. One row; its `version` is the shelf version that every
reorder carries.

**feature_slots.** `id`, `expertise_id`, `position` (`0` or `1`),
`case_study_id` (empty when the slot is empty), `version`. Eight rows, one per
expertise and position. A slot is its own record so that emptying it writes
nothing to a case study.

**briefs.** `id`, `name`, `company`, `phone` (digits and a leading plus only),
`email`, `comment`, `expertise`, `budget`, `state` (one of `unread`, `read`,
`archived`), `source_path`, `received_at`.

**page_views.** `id`, `route`, `viewed_at`.

Derived on read and never stored: a case study's `next`, the dashboard counts and
the unread count, and whether a case study is visible to the public.

**Invariants, as properties of the running system.**

- A case study that is not published is absent from every public read and every
  public list, its public address answers not found or gone, and its cover bytes
  are refused to anyone not signed in as `owner` or `editor`.
- A publish without an expertise, a tag, or a cover carrying alternative text is
  refused and changes nothing.
- Shelf places are unique and gap-free across all case studies, and unpublishing
  never changes a place. A reorder changes places only, never a case study's
  `version`.
- A feature slot holds only a published case study of its own expertise, a case
  study holds at most one slot, and a slot write leaves every case study row as
  it was.
- A write carrying a stale or missing `version` changes nothing; an accepted write
  raises `version` by one. Two simultaneous writes from one version: exactly one is
  accepted.
- A repeated create with the same `Idempotency-Key` within 24 hours creates one
  row.
- A brief treated as spam stores no row. A refused write writes nothing at all: no
  row, no partial row, no object.
- An object key is unique, and identical cover bytes for one case study are one
  object.

**Seed data.** The three accounts in `## User roles`. The four expertises and
eleven tags in `## Front-end specification`. Twelve case studies, in this shelf
order:

| Place | Title | Slug | Client | Year | Expertise | Tags | State |
|---|---|---|---|---|---|---|---|
| 1 | `Cliffside Residences` | `cliffside-residences` | `Halden` | `2024` | `real-estate` | `promo-website`, `real-estate` | published |
| 2 | `Kestrel Annual Review` | `kestrel-annual-review` | `Kestrel Bank` | `2024` | `corporate` | `corporate-website`, `banking` | published |
| 3 | `Vantage Onboarding` | `vantage-onboarding` | `Vantage` | `2025` | `startups` | `saas`, `self-service` | published |
| 4 | `Meridian Duty Free` | `meridian-duty-free` | `Meridian Air` | `2024` | `ecommerce` | `online-store`, `branding` | published |
| 5 | `Harbour Quarter` | `harbour-quarter` | `Northline` | `2023` | `real-estate` | `real-estate`, `3d-visualisation` | published |
| 6 | `Ostend Loyalty Store` | `ostend-loyalty-store` | `Ostend Credit` | `2021` | `ecommerce` | `online-store` | withdrawn |
| 7 | `Ostend Investor Portal` | `ostend-investor-portal` | `Ostend Credit` | `2022` | `corporate` | `customer-portal`, `banking` | published |
| 8 | `Pinemark Trading Desk` | `pinemark-trading-desk` | `Pinemark` | `2023` | `startups` | `trading-platform`, `saas` | published |
| 9 | `Halden Home Store` | `halden-home-store` | `Halden` | `2022` | `ecommerce` | `online-store` | published |
| 10 | `Northline Self Care` | `northline-self-care` | `Northline` | `2021` | `corporate` | `self-service`, `customer-portal` | published |
| 11 | `Vantage Pitch Site` | `vantage-pitch-site` | `Vantage` | `2025` | `startups` | `promo-website` | published |
| 12 | `Pinemark Mobile App` | `pinemark-mobile-app` | `Pinemark` | `2025` | `startups` | `saas` | draft |

Every seeded case study carries a generated cover stored in the bucket with
alternative text, and a body of at least one `paragraph` block. A seeded case
study's cover seed is its place number, `1` to `12`, and its palette is `mono`.
The shelf row starts at `version` `1`. The eight slots
start filled: `Real Estate` holds `Cliffside Residences` then `Harbour Quarter`;
`Corporate` holds `Kestrel Annual Review` then `Ostend Investor Portal`;
`Startups` holds `Vantage Onboarding` then `Pinemark Trading Desk`; `eCommerce`
holds `Meridian Duty Free` then `Halden Home Store`. Three briefs: from
`Ines Duval`, `ines.duval@example.com`, company `Halden`, expertise
`real-estate`, budget `75k_to_150k`, `unread`, comment
`A site for our coastal tower. <b>Launch before March</b>`; from `Tomas Berg`,
`tomas.berg@example.com`, company `Vantage`, expertise `startups`, budget
`25k_to_75k`, `unread`, comment `We need an onboarding flow for a savings app.`;
from `Lea Park`, `lea.park@example.com`, company `Pinemark`, expertise
`ecommerce`, budget `under_25k`, `read`, comment
`Could you quote for a small online store refresh?`. No page views are seeded.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One studio. No organisation, no team workspace and no second tenant.
- No blog index, no article route, no article editor and no career page in this
  build, so the header carries `Work`, `Company` and `Contact`.
- No email of any kind: no transactional messages and no notifications leave the
  product, no password reset link, no editor invitation, no address change. The
  product tells people things in three places only: a line under the control that
  was pressed, a line at the top of a list, and the count beside `Inbox`. It never
  asks the browser for permission to notify.
- No search box on the public site, no sort, and no paging on `/work`.
- The public site does not update while open; a publish appears on the next load.
- No automatic merge anywhere.
- No third-party analytics, no tracking cookie, and no external network call at
  run time. Nothing a visitor types is counted.
- One language ships, with no second locale. Date formatting is UTC in one fixed
  format. No long dash appears anywhere,
  including the footer year range and the first expertise sentence, which use a
  plain hyphen.
- No embedded third-party video player and no colour borrowed from one.
- The product must stay responsive with the seeded content and with a few thousand
  page-view rows and a few hundred briefs.

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
| `POST /api/auth/signup` | `email`, `password`, optional `display_name` | the created account with its `role` and an `access_token` |
| `POST /api/auth/login` | `email`, `password` | the account with its `role` and an `access_token` |
| `GET /api/auth/me` | none | the signed-in account with its `role` |
| `GET /api/sessions` | none | a top-level array of the account's live sessions, each with `id`, `user_agent_summary`, `created_at`, `last_seen_at` and `current` |
| `DELETE /api/sessions` | none | nothing; every session of the account has ended |
| `GET /api/health` | none | a health object |
| `GET /api/site` | none | `expertises` in order, `tags`, `clients`, and `featured`: for each expertise its two slots, each a published case study or `null` |
| `GET /api/work` | optional `expertise`, repeatable `tag` | a top-level array of published case studies in shelf order |
| `GET /api/work/{slug}` | none | one published case study with `blocks`, `tags`, `expertise`, `cover` and `next` |
| `GET /api/expertise/{slug}` | none | one expertise with `work`, its published case studies in shelf order |
| `GET /api/covers/{id}` | none | the cover's bytes |
| `GET /api/briefs/token` | none | a `form_token` |
| `POST /api/briefs` | `name`, `company`, `phone`, `email`, `comment`, `expertise`, `budget`, `source_path`, `form_token`, `website`; optional `Idempotency-Key` header | `id` |
| `POST /api/page-views` | `route` | the recorded view for a public route; for a `/studio` route an empty acknowledgement and no row |
| `GET /api/studio/dashboard` | none | `published_count`, `draft_count`, `recent`, and `unread_briefs` for the owner only |
| `GET /api/studio/work` | none | a top-level array of every case study in shelf order |
| `POST /api/studio/work` | `title`, and optionally `slug`, `client`, `year`, `expertise`, `tags`, `summary`, `cover_seed`, `cover_palette`, `blocks`; optional `Idempotency-Key` header | the created case study, unpublished, with `version` `1` and its `position` |
| `GET /api/studio/work/{id}` | none | one case study with `version`, `position`, `published` and `cover` |
| `PATCH /api/studio/work/{id}` | the changed fields and `version` | the updated case study |
| `DELETE /api/studio/work/{id}` | `version` | nothing |
| `POST /api/studio/work/{id}/cover` | `generate` set to `true`, `alt_text` and `version` | the cover with its `object_key` |
| `POST /api/studio/work/{id}/publish` | `version` | the published case study |
| `DELETE /api/studio/work/{id}/publish` | `version` | the unpublished case study |
| `GET /api/studio/shelf` | none | the shelf `version` and `work`, every case study in shelf order |
| `PUT /api/studio/shelf` | `order`, every case study id in the new order, and the shelf `version` | the shelf `version` and `work`, every case study in the new order |
| `GET /api/studio/slots` | none | a top-level array of the eight slots, each with `id`, `expertise`, `position`, `case_study_id` and `version` |
| `PUT /api/studio/slots/{id}` | `case_study_id` (or `null`) and `version` | the slot |
| `GET /api/studio/briefs` | optional `state` | a top-level array of briefs, newest first |
| `GET /api/studio/briefs/{id}` | none | one brief |
| `PATCH /api/studio/briefs/{id}` | `state` | the brief |
| `DELETE /api/studio/briefs/{id}` | none | nothing |
| `GET /api/studio/page-views` | none | a top-level array of page views, newest first |

`expertise` is always an expertise slug and `tags` is always an array of tag
slugs. A case study carries `id`, `slug`, `title`, `client`, `year`, `expertise`,
`tags`, `summary`, `cover_seed`, `cover_palette`, `cover`, `blocks`, `position`,
`published` and `version`; a cover carries `id`, `object_key`, `alt_text`,
`width` and `height`; a brief carries every field it was sent with plus `id`,
`state` and `received_at`. Field names are exact. A list endpoint returns a
top-level JSON array. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never as a server
error and never as a silent success. Bearer authentication is required on every
`/api/studio` endpoint and on `/api/sessions` and `/api/auth/me`, and on
`GET /api/covers/{id}` for any cover whose case study is not published;
everything else listed is public.

### No mocks

`minio` is where every cover's bytes live. An in-memory buffer the app hands back
to itself, a file on the app container's own filesystem, a base64 column in
`PostgreSQL`, or an object key pointing at nothing are each a contract violation
however right the editor looks. The named provider is the fact: the app's UI and
its own tables can only reflect what lives in the provider, never substitute for
it.

## Definition of done

A visitor filters `/work` to one expertise, reads a case study, and sends a brief
that the owner then reads in the inbox as plain text. The owner writes a case
study, generates its cover into the bucket, publishes it, sees it under its
expertise, and features it on the front page while the case study it replaced
stays published. A draft and its cover are unreachable to everyone outside the
studio.
