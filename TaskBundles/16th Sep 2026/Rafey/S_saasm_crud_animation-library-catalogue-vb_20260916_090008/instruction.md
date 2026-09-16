# Tempo

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
narrow the example gallery to one runtime and one category, copy the address of that
narrowed list into a second visit and get the same list back, open one example and
watch it run, then buy lifetime access and save that example to their own account,
without hitting an error page.

A different stranger, signed in as another member or not signed in at all, must NOT
be able to read a paid example's source by any means: not through the page, not by
asking the read surface for the example directly, not by asking for the raw file's
own address, and not from inside the framed preview that runs it. A paid example's
file source must be absent from the response body, not hidden by the interface. An
entitlement the app cannot resolve must refuse rather than allow, and must say so in
a way a reader can tell apart from never having bought.

## Overview

Tempo is an animation library for the web and this is the site around it: the manual,
the example catalogue, the pre-built interface sections, the paid tier, the member
profiles and the editorial record. It has three audiences and one funnel. A developer
looking something up arrives at the manual. A developer choosing between this library
and a paid incumbent arrives at the catalogue. A developer who has already chosen
arrives to buy. All three end at the same place: a list of finished, runnable pieces
they can watch move, narrow to their own runtime, read the source of, and take away.

Almost every page here is generated from a published catalogue rather than authored as
a page. The manual comes from versioned documentation records, the gallery and the
section library from a catalogue of examples and sections, the changelog and the
magazine from dated records. That is why every count the copy quotes is counted from
the catalogue rather than typed into the copy: a sales page that claims a number its
own catalogue cannot produce is a defect, and two paragraphs that disagree about how
many sections there are is the same defect twice.

The genuinely hard part is the boundary around paid material and around a member's own
material. A paid example's source is the product, so it must be absent from every
response that reaches a reader without the licence, including the raw file address.
A framed preview runs a stranger's animation next to a signed-in member's session, so
the frame must be unable to reach that session at all. And a project a member submits
is a stranger's content on the front page until a person has looked at it, so it stays
readable by its owner alone until the maintainer publishes it.

The non-goals are as firm as the goals. What this site deliberately is not: no team
plan and no seats, no performance audit service, no agent tool server, no refunds, no
moderation queue, no site-wide search overlay, no advertising and no consent banner.
It ships one colour mode, the laboratory dark, and no light theme.

## User roles

| Role | Can do |
|---|---|
| member | Read every public route: the manual at the current release and at any named release, the example gallery at every facet combination, a free example's source, the section library, the theme file, the paid route, any member's public profile, the changelog and the magazine. Buy lifetime access once. Save and unsave an example. Submit a showcase project. Read a paid example's source **only while holding the licence**. **Cannot read another member's saved rows, read another member's unpublished project, read a paid example's source without the licence, or publish their own project.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
control in the UI is not authorization: a direct API call from one member's session
to another member's saved rows, unpublished project or paid source must be rejected by
the server (an unauthorized request is denied, not served), leaving the protected
state unchanged.

Signup is open: anyone can create an account from `/signup` with an email, a name, a
handle and a password, and the footer of every page links the privacy page and the
terms page. Three accounts are seeded for grading, all with the password
`deku-demo-pw-2026`:

| Email | Name | Handle |
|---|---|---|
| `member@example.com` | Nova Reyes | `nova` |
| `member2@example.com` | Kit Alvarez | `kit` |
| `member3@example.com` | Sol Danner | `sol` |

`member@example.com` holds the licence `tempo-plus-nova`, has saved `scroll-velocity`
and `parallax`, has the published showcase project `Orbit Atlas` and the submitted
showcase project `Field Notes`. `member2@example.com` holds no licence, has saved
nothing and has submitted nothing. `member3@example.com` holds no licence and is the
account the purchase journey uses.

## Core features

### Auth

Accounts are email and password, implemented by the app. `POST /api/v1/auth/signup`
takes `email`, `name`, `handle` and `password` and creates a member.
`POST /api/v1/auth/login` takes `email` and `password` and returns a bearer `token`
plus the signed-in `member`. Every later call carries `Authorization: Bearer <token>`.
A token expires 24 hours after it is issued.

1. A wrong password and an unknown email are refused with the same message,
   `Sign in failed`, so neither answer reveals whether the account exists. A missing
   token, an unknown token and a token past its expiry are all refused as
   unauthenticated, and nothing they asked to change is changed.
2. Passwords are stored hashed. The literal `deku-demo-pw-2026` must work at login
   for every seeded account and must not appear in any stored record.
3. Signup refuses an email that already has an account and refuses a handle that
   already has an account, naming the field in each case, and writes no second row.
4. A handle is folded to one case before it is compared, so `Nova` and `nova` are the
   same handle and the second signup is refused.

### 1. Versioned reference documentation for three runtimes

The manual covers three runtimes: `react`, `js` and `vue`. `/docs` is the index.
`/docs/react` is a runtime index. `/docs/react/use-spring` is one page at the current
release. `/docs/13.0.4/react/use-spring` is the same page at a named release.

1. `/docs/react/use-spring` serves the current release and **names that release on
   the page**. The current release is `13.1.0`. An address without a version is
   never permanent: when a newer release is published, the same address serves the
   newer page.
2. `/docs/13.0.4/react/use-spring` is permanent. It serves the page as it stood at
   `13.0.4` and it does not move when the current release changes. The three retained
   releases are `13.1.0`, `13.0.4` and `12.8.2`.
3. A runnable block on a documentation page carries the release its source was last
   executed against, and that release is shown beside the block. A block whose last
   execution was against a release older than the page's own release is marked as
   such rather than presented as current.
4. An address that differs only by a trailing slash is not a second page, and serving
   both splits the cache surface in two. `/docs` and `/docs/` do not both serve a
   document. One of the two is canonical and
   the other answers with a permanent redirect to it, and the canonical link element
   on the served page names the canonical form.
5. A page for a runtime that does not exist, and a version that is not one of the
   three retained releases, both answer as not found rather than falling back to the
   current release. Silently serving a different version than the one asked for is
   worse than saying no.
6. Each page names the release it was introduced in. `use-spring` was introduced in
   `12.8.2`.

### 2. The filterable example gallery

`/examples` is a grid of cards, three across on the widest layout. The filter row sits
above the grid, set in the mono family, uppercase.

1. **Filtering is a change of address, not a change of state.** Every facet
   combination has its own address, is rendered on the server, and produces the same
   grid in the same order when that address is opened again in a second visit. Four
   facets: `runtime`, `category`, `access` and `saved`. Three orderings: `newest`,
   `most-saved` and `title`.
2. `/examples?runtime=react&category=hero-sections` serves only the examples that
   exist for `react` and sit in `hero-sections`. `access=paid` serves only the paid
   ones, `access=free` only the free ones, and `saved=1` only the signed-in member's
   saved ones. `saved=1` asked for by a visitor who is not signed in serves an empty
   grid and says why, rather than refusing the address.
3. The grid carries a count line stating how many examples matched. That numeral is
   counted from the catalogue for that address and is never typed.
4. A card has four states and the state is legible without opening it. A free
   example's card opens the source. A paid example's card, seen by a reader without
   the licence, carries a lock mark in the meta bar and its open action reads as an
   upgrade. A paid example's card, seen by a reader holding the licence, is
   indistinguishable from a free one. A saved card's save control is filled in the
   accent.
5. `/examples/<slug>` is one example: the framed stage running it, the source in one
   tab per file with a copy control on each, a meta bar naming the runtime, the
   category and whether it is free or paid, and a related rail. The bytes the copy
   control puts on the clipboard are the bytes in the panel.
6. Seven examples are seeded. `scroll-velocity` is free and exists for all three
   runtimes. `parallax` is free and exists for all three. `skeleton-shimmer` is free
   and exists for `react` and `vue`. `floating-action` is free and exists for `js`.
   `ios-app-folder` is paid and exists for `react`. `ios-pointer` is paid and exists
   for `react` and `js`. `ticker-marquee` is paid and exists for all three.
7. What has to be findable is an example's title, its category and its runtime, and
   the search trigger in the header narrows the gallery on those three. Ranking inside
   an ordering never depends on who is asking: the `title` ordering is alphabetical ignoring case,
   the `most-saved` ordering is by the saved count, and the `newest` ordering is the
   freshness rule, most recently published first.
8. An unknown facet value answers as not found rather than serving the unfiltered
   grid, because a list that quietly ignores half of what was asked for cannot be
   linked with any confidence.

### 3. The section library and its theme file

`/ui` is the section library: pre-built animated interface sections a buyer drops into
their own product. `/ui/<category>` is one category. `/ui/<category>/<slug>` is one
section.

1. Nine categories are seeded, each with its own address segment, its name and its
   blurb:

   | Segment | Name | Blurb |
   |---|---|---|
   | `hero-sections` | Hero sections | First impressions with editorial reveals and product-led motion. |
   | `pricing` | Pricing | Comparison, billing and usage surfaces that explain value clearly. |
   | `navigation` | Navigation | Mega menus, scroll-aware shrinking headers and command palettes. |
   | `testimonials` | Testimonials | Logo tickers, coverflow carousels and draggable testimonial card stacks. |
   | `page-transitions` | Page transitions | Full-page entrances and exits with a clear sense of direction. |
   | `bento-grids` | Bento grids | Staggered bento reveals, app-card expands and scroll-linked spotlights. |
   | `stats-sections` | Stats sections | Scroll-in counters and live engagement panels with animated trends and drawn graphs. |
   | `cta-sections` | CTA sections | Signup celebrations, copy-to-clipboard install blocks and magnetic banners. |
   | `footers` | Footers | Newsletter forms with live feedback, sticky under-page reveals and staggered mega-footer wordmarks. |

2. Each category card carries a count badge reading how many sections are filed under
   it, and that numeral is counted from the catalogue. The hero's own section total
   and the catalogue action's total are the same query, so the two numerals on the
   route can never disagree.
3. Six sections are seeded: `editorial-stagger-hero` in `hero-sections`, `border-beam`
   and `confetti` in `cta-sections`, `command-palette` in `navigation`, `coverflow` in
   `testimonials`, and `sheet` in `page-transitions`.
4. **The theme file is the most important artefact on this route.** One file holds
   twelve named values, and every section resolves its own timing from it rather than
   carrying a timing of its own, so a buyer retunes the whole set by editing twelve
   numbers. The twelve are shown as a source file with the active line marked:

   | Key | Value |
   |---|---|
   | `transitions.snap` | stiffness `1218`, damping `70` |
   | `transitions.ui` | stiffness `305`, damping `33` |
   | `transitions.gentle` | stiffness `110`, damping `20` |
   | `transitions.lively` | stiffness `622`, damping `17` |
   | `transitions.ambient` | stiffness `43`, damping `13` |
   | `stagger.tight` | `0.04` |
   | `stagger.base` | `0.08` |
   | `stagger.relaxed` | `0.15` |
   | `travel.hover` | `4` |
   | `travel.enter` | `24` |
   | `travel.section` | `48` |
   | `reducedMotion` | `"calm"` |

5. A section's own page names which of the twelve values it reads, and it names the
   style tokens it expects the buyer to have defined. A section that declares what it
   reads can be matched against a buyer's project before it is installed rather than
   after it looks wrong.
6. Beside the theme file sits a five-tab strip, one tab per named transition, over a
   plot. **The plot is drawn from the same solver the sections use, at the stiffness
   and damping in the table.** All five curves are drawn at once as thin lines with
   the selected one drawn thick, and a square beside the plot moves with the selected
   transition, so the reader sees and feels the same thing at the same time. A plot
   drawn from a hand-fitted curve would be a claim about the product that the product
   does not honour.
7. `/ui` and `/ui/` do not both serve a document. One is canonical and the other
   answers with a permanent redirect to it.
8. The section library carries its own version, `0.0.2`, which is not the library's
   version and is shown as its own numeral.

### 4. The live preview

Every example page and every section page carries a framed stage. The stage runs the
real thing rather than a recording.

1. The framed document is served from the app's own origin and is granted script
   execution and nothing else. Its content policy names the app's own origin as the
   only destination it may reach. Form submission, top-level navigation, popups and
   downloads are all denied.
2. **The framed document is served without the session cookie**, and script inside it
   cannot read a session, an account or a saved row. A read of the member surface
   attempted from inside the frame is refused the same way a request with no
   credential is refused, and the refusal is observable rather than silent.
3. The stage waits for the preview to report itself ready. A preview that has not
   reported ready within 5 seconds of wall clock is stopped and the well states that
   it did not start, leaving the rest of the page usable.
4. At most three previews run at once on one page. A preview that leaves the viewport
   is destroyed rather than left running, and its well keeps the size the media will
   be so nothing shifts when it returns.
5. The framed document is a nested browsing context with a title, and the keyboard
   can both enter it and leave it.
6. The section library's own preview well runs one section at a time and a shuffle
   control swaps a different section into the same well without the page moving.

### 5. Lifetime access

`/plus` is the paid route. One product: one payment, one perpetual licence, lifetime
updates, no renewal.

1. The proof strip on `/plus` carries `MIT-licensed code`, `Lifetime updates` and the
   example total counted from the catalogue, and the plan's action reads
   `Get instant access`.
2. The list price is `$249.00`, held as `24900` minor units with the currency `USD`.
   Money is integer minor units and a currency code everywhere it is stored or
   returned, never a decimal fraction.
3. Two price bands are seeded and a band is a table row, never a formula. The band
   `list` is `24900` with no reason. The band `ppp-south-asia` is `14900` with the
   reason `Local discount applied`. The band that applies to a request is resolved
   from the request header `X-Client-Region`: `US` resolves to `list` and `IN`
   resolves to `ppp-south-asia`. A region with no row resolves to `list`.
4. **The price banner appears only when a band other than `list` applies.** When it
   appears it carries the banded price and the list price struck through, in the same
   currency, and it carries the band's reason. When `list` applies there is no banner
   at all. A banner claiming a discount over a purchase that charges the list price
   is not a bug, it is a false statement about money.
5. The purchase panel opens over the pricing board and leaves the board in place
   behind it. It collects the buyer's display name and their email address. Submitting
   it writes, in one outcome:
   - a licence whose key is `tempo-plus-` followed by the buyer's handle, so the
     buyer `sol` receives the licence `tempo-plus-sol`
   - an order carrying the currency, the list amount, the discount amount, the total
     amount, the band code that was applied and the band's reason, so the banner the
     buyer saw can be reconciled against what was sold
   - a billing account in the billing platform, created under that same licence key
     as its external key, with the buyer's display name, the buyer's email address,
     the currency `USD` and the country `US`
   - one receipt, by mail, to the buyer's address

   The reconciliation between what the banner claimed and what was sold is the band
   code recorded on the order, which is why it is stored rather than recomputed.
6. **A repeated purchase for the same licence key is refused by that key's own
   uniqueness in the billing platform**, which answers with a conflict, and not by a
   guard in the application. The refusal leaves exactly one billing account, exactly
   one licence and exactly one order for that key, and sends no second receipt. The
   panel states that the licence already exists and names it.
7. A purchase requires an idempotency key and honours it for 24 hours: the same key
   submitted twice returns the first outcome and writes nothing the second time.
8. The receipt's subject begins `Tempo+ receipt ` followed by the licence key, it goes
   to the buyer's address and to nobody else, it carries no copied or blind-copied
   recipient, and it states the total amount, the currency and the band's reason where
   a band applied. A purchase that was refused sends no mail at all.
9. The total is computed on the server and the client mirrors it. On a mismatch the
   server total wins, the client re-renders from it, and the difference is logged,
   because this is the one place where an arithmetic slip becomes a billing dispute.
10. The panel closes onto a confirmation naming the licence key and the total amount.
   The board behind it now shows the member as holding the licence rather than offering
   the purchase again.

### 6. Entitlement

The licence unlocks the paid examples and the paid documentation pages. Nothing else
in the product checks it.

1. **A paid example's file source is absent from every response served to a reader
   without the licence.** That holds for the example's own read address, for the raw
   file's own address, for the gallery listing, and for the document the framed
   preview loads. Absent means not in the response body: a source field present but
   emptied is not enough, and neither is a source present in the markup and hidden by
   a style.
2. A reader without the licence still sees the stage run, the meta bar, the category,
   the runtimes and the description. The stage is the sales pitch and is not gated.
3. **An entitlement claim is resolved from the licence row on every request** and is
   never trusted from the bearer token, so a licence that has been revoked stops
   working on the next request rather than when a token expires.
4. **Entitlement fails closed.** If the licence cannot be resolved, the answer is
   refusal, not access. A licence row whose `entitlements` is empty or null is one the
   app cannot resolve into anything it unlocks, and it is answered that way. The refusal a reader gets when resolution failed is visibly
   distinct from the upgrade offer a reader gets when they have simply never bought:
   the first says the licence could not be confirmed and invites a retry, the second
   offers the purchase.
5. `member@example.com` holds `tempo-plus-nova` and can read the source of
   `ios-app-folder`, `ios-pointer` and `ticker-marquee`. `member2@example.com` holds
   no licence and cannot read any of the three, by any address.

### 7. Saved examples

A member saves an example from its card or from its page.

1. `POST /api/v1/saved` with the example's slug writes one row for that member and
   that example. The pair is unique, so **saving the same example twice leaves one
   row** and is not an error. `DELETE /api/v1/saved/<slug>` removes it.
2. **The row survives a reload.** After a save, opening the gallery again shows the
   card's save control still filled, and opening the member's own profile shows the
   example in the saved panel. The example in the panel is the example the gallery
   showed: the same slug, the same title, the same runtimes.
3. The save control fills at once when it is pressed and then reconciles against the answer.
   A save the server refuses returns the control to its previous state and
   states the reason on the card itself rather than in a banner elsewhere on the page.
   The result is announced politely.
4. **A save attempted while signed out completes after signing in.** Pressing save
   with no session takes the visitor to `/login?next=<the page>&save=<slug>`, and
   signing in from that address writes the row for `<slug>` before returning to
   `<the page>`, so the example is in the saved panel without the visitor pressing
   anything a second time.
5. An example's `save_count` is the count of its saved rows and is read from them.
   The `most-saved` ordering on the gallery reads the same count.
6. A member's saved rows are readable by that member alone. `/@nova` seen by anybody
   else carries the published showcase and no saved panel, and asking the read surface
   for another member's saved rows is refused.

### 8. The member showcase

`/@<handle>` is a member profile: a striped dossier header, the projects they have
published, and to the owner alone the saved panel.

1. The publish panel opens over the profile and collects a title, a source address and
   a description. That is the whole intake: no upload, no media and no second step.
   Submitting it writes a project in the state `submitted`, which appears in the
   owner's own list at once, marked as awaiting a decision.
2. **A submitted project is absent from every public response.** It is not on the
   public profile, not in the homepage showcase tape, and not returned when its own
   address is asked for by anybody but its owner. A project reaches the public list
   only in the state `published`.
3. A member cannot publish their own project. The transition from `submitted` to
   `published` is a human review by the maintainer, so nothing a stranger submits
   reaches the front page without a person having looked at it.
4. `nova` has one published project, `Orbit Atlas`, and one submitted project, `Field
   Notes`. `/@nova` asked for by anybody carries `Orbit Atlas` and does not carry
   `Field Notes`.
5. An unknown handle answers as not found. A handle is folded to one case before it is
   looked up, so `/@NOVA` and `/@nova` reach the same profile.
6. The dossier header carries the member's display name, their handle, the date they
   joined and their links. A member with no published project gets the header and an
   empty state, not a missing page.

### 9. The changelog and the magazine

Two dated feeds over one record shape. `/changelog` and `/magazine` are the indexes,
`/magazine/<slug>` is one article.

1. Both indexes are ordered newest first, by the published date, and both state that
   ordering.
2. A changelog entry names the release it belongs to and the kind of change it is.
   Four entries are seeded: `13.1.0` introducing the five named transitions, `13.0.4`
   correcting exit animations, `12.8.2` correcting pointer gestures, and `0.0.2` which
   belongs to the section library rather than to the library and carries its own badge
   saying so.
3. A changelog entry links to the documentation at the release it names, and that
   address is the permanent form, so following a changelog entry never lands on a page
   that has since moved.
4. Three articles are seeded: `springs-over-easing`, `the-all-problem` and
   `reduced-motion-is-not-no-motion`. Each carries a title, a standfirst, an author
   handle and a published date, and each is addressable on its own.
5. An article's own page carries its published date and its author, and an unknown
   article slug answers as not found.
6. `/about` is the maintainer's page, written in the first person, naming the earlier
   library the maintainer wrote and the incumbent this one is measured against.

### 10. The site's own surface

1. A route that does not exist serves the not-found document **rendered on the server
   and carried with the not-found status**, not with a success status and not after the
   client boots. The document carries the wordmark, a drawn figure, the label
   `PAGE_NOT_FOUND` and a link home.
2. A `favicon` is served and is referenced from every page.
3. Every route carries its own meta description, and no two routes share one. A
   description that describes the site rather than the route is the same defect as no
   description.
4. `/privacy` states what is collected, how long it is kept and that nothing is shared,
   and it is linked from the footer of every page.
5. `/terms` states the licence the code is under, that the paid licence is perpetual,
   and that there is no renewal. It is linked from the footer of every page.
6. Every response carries a security header set: a strict transport policy, a nosniff
   content type policy, a frame policy, a referrer policy and a content security
   policy. The framed preview's policy is the one described in feature 4.
7. No credential the server holds appears in anything the browser downloads: no
   database address, no billing key, no billing secret, no billing password, no mail
   host and no other member's token.

## User flow

| Path | Who | What |
|---|---|---|
| `/` | anyone | the hero, the proof strip, the feature atlas, six example cards, the showcase tape, the changelog column and the magazine column |
| `/docs` | anyone | the documentation index and the runtime chooser |
| `/docs/<runtime>` | anyone | one runtime's index for `react`, `js` or `vue` |
| `/docs/<runtime>/<slug>` | anyone | one page at the current release, naming it |
| `/docs/<version>/<runtime>/<slug>` | anyone | the same page at a named release, permanent |
| `/examples` | anyone | the gallery grid; every facet combination is its own address |
| `/examples/<slug>` | anyone | the stage, the source panel, the meta bar and the related rail |
| `/ui` | anyone | the section library landing, the preview well and the theme file |
| `/ui/<category>` | anyone | one category's sections |
| `/ui/<category>/<slug>` | anyone | one section, its source and the theme keys it reads |
| `/plus` | anyone | the proof strip, the price banner, the pricing board and the comparison table |
| `/@<handle>` | anyone | a profile: the dossier header, the published showcase, and the saved panel to its owner |
| `/login` | anyone | sign in |
| `/signup` | anyone | create an account |
| `/changelog` | anyone | the changelog, newest first |
| `/magazine` | anyone | the magazine index, newest first |
| `/magazine/<slug>` | anyone | one article |
| `/about` | anyone | the maintainer's page |
| `/privacy` | anyone | the privacy page |
| `/terms` | anyone | the terms page |

### Entry and redirects

The front door is `/` and it is readable with no account. Nothing a visitor reads is
behind a signup wall: not the manual, not the gallery grid, not a free example's
source, not the section library, not the changelog and not the magazine.

`/docs/` answers with a permanent redirect to `/docs`, and `/ui/` answers with a
permanent redirect to `/ui`. The canonical link element on the served page names the
canonical form. A visitor who is not signed in and asks for a member-only surface is
sent to `/login` with their destination carried, and arrives at that destination after
signing in rather than at the front door.

A signed-in member who asks for `/login` or `/signup` is sent to their own profile. A
member who asks for another member's saved rows is refused rather than redirected,
because a redirect would tell them the rows exist.

### Journeys

1. **Narrow the gallery.** Open `/examples`. The grid shows every seeded example and
   the count line states how many. Choose the runtime `react` and the category
   `hero-sections` from the filter row. The address changes to
   `/examples?runtime=react&category=hero-sections`, the grid is re-rendered for that
   address, and the count line states the smaller number. Open that address again in a
   second visit and the same grid comes back in the same order.
2. **Watch one run.** From the narrowed grid open `parallax`. The page carries the
   framed stage running it, one source tab per file, and a meta bar naming the runtime,
   the category and that the example is free. Press the copy control on a tab; the
   bytes taken are the bytes shown.
3. **Meet the gate.** Open `/examples/ios-app-folder` with no session. The stage runs.
   The source panel is replaced by the upgrade action. Ask the read surface for the
   example directly and the file source is not in the answer. Ask for the raw file's
   own address and the answer is a refusal, not the source.
4. **Buy once.** Sign in as `member3@example.com`. Open `/plus`. With the region `IN`
   the banner shows `$149.00` with `$249.00` struck through and the reason `Local
   discount applied`; with the region `US` there is no banner and the board shows
   `$249.00`. Open the purchase panel, submit it, and the confirmation names the
   licence `tempo-plus-sol` and the total. One receipt arrives at
   `member3@example.com` with the subject beginning `Tempo+ receipt `. Submit the same
   purchase again: it is refused because the licence key is taken, and there is still
   one order and one receipt.
5. **Read what was bought.** Still signed in as `member3@example.com`, open
   `/examples/ios-app-folder`. The source panel now carries the source. Open
   `/examples?access=paid` and the paid cards no longer carry the lock mark.
6. **Save it.** Press the save control on the `ios-app-folder` card. The control fills
   at once. Reload the page: it is still filled. Open `/@sol`: the saved panel lists
   `ios-app-folder`.
7. **Save while signed out.** Sign out. Open `/examples` and press save on
   `scroll-velocity`. Arrive at `/login`, sign in as `member2@example.com`, and land
   back where the save was pressed with `scroll-velocity` already saved. Open `/@kit`
   and the saved panel lists it.
8. **Publish something.** Signed in as `member2@example.com`, open `/@kit`, open the
   publish panel and submit a project. It is in the owner's own list at once, marked
   as awaiting a decision. Open `/@kit` in a session belonging to somebody else and
   the project is not there.
9. **Follow the record.** Open `/changelog`. The newest entry names `13.1.0`. Follow
   it to the documentation at that release and the address carries the version.
10. **Land nowhere.** Ask for `/div`. The not-found document comes back with the
    not-found status, rendered on the server, carrying `PAGE_NOT_FOUND` and a link
    home.

### States

Every surface that can be empty, loading, refused or broken says which. An empty
gallery for a facet combination that matches nothing says so and offers to clear the
facets, and does not look like a page that failed to load. A preview well that has not
started yet holds exactly the size the media will be. A preview that did not start
says it did not start. A save that was refused returns its control and states why on
the card. A purchase that was refused states which licence key is taken. An entitlement
that could not be resolved says the licence could not be confirmed, which is not the
same page as the upgrade offer. A member's own empty saved panel and a member's own
empty showcase both carry their headings and an empty state rather than vanishing.

## UI/UX notes

This site looks like a technical drawing rather than a landing page, and the whole
look rests on four decisions: one dark ground, one accent set by a single switch, two
typefaces with a hard division of labour, and gaps instead of borders.

**Colour.** The page ground is a near-black with green in it. Below it sit two deeper
recesses with the green taken out. The ink is a warm off-white; the secondary ink is a
neutral warm grey; a half-strength off-white carries tab labels and captions. A card
sits one step above the ground and a card's border one step above that. There are two
colour systems and they are resolved into one: a declared set of tokens on the root
element is the source, the resolved values are what components read, and nothing
reaches for a third value.

The accent is set by **one attribute on the root element** and every accented surface
reads it. Nothing anywhere hard-codes a colour. The free library resolves the accent
to amber. The paid route, the account routes and the member profiles resolve it to
green. A periwinkle blue is the tertiary accent and carries the not-found figure.
Failure is an orange-tinted red. Behind all of that sits a ramp of six saturated
colours named after fruit, declared on every route, and every badge drawn from the ramp
takes a one-tenth wash of its own colour as its ground.

**Type.** Two families, and the division between them matters more than any colour.
The mono family carries every label, kicker, numeral, code fragment, badge and control
on this site. The sans family carries only what is read as a sentence. A label set in
the sans family reads as a mistake here. Both families are named with a fallback stack
and neither ships as a file; the fallback is metric matched so the swap moves no line.

Sizes, from the measured scale: labels and kickers at `10px` and `11px`; prose at
`12px`, `13px`, `14px` and `15px`, each at its own line height; lead prose at `17px`;
headings at `19px` and `23px` at the bold cut. The display roles carry their own
negative tracking: an article card title at `22px`, a version numeral and a newsletter
lead at `30px`, an account heading at `32px`, a hero title at `44px`, a dossier title
at `56px`. Uppercase mono labels are tracked out and the amount varies with the
label's job, tightest on a preview control and loosest on the trust label. Sans
headings track the other way, negative and proportional to size.

**Surface.** The site is square. Cards, buttons, inputs, thumbnails and panels carry
no radius at all; the handful of radii that exist live only on dots, pills, terminal
chrome and a tab strip. Hairline grids are the signature: a grid container takes a
one-pixel gap over a border-coloured ground, the cells are painted with the card
ground, and the gap itself becomes the rule, so no border is drawn anywhere on the
feature atlas or the pricing board. Diagonal hatching at one consistent odd angle is
stamped behind the primary action, the reading-route headers, the account frame, the
catalogue thumbnails and the changelog version plate, in four variants that differ
only in colour, stroke and period. A dot field, a ruler down the inside edges of a
showcase plate, four blur radii each bound to one role, and two shadows are the entire
rest of the surface vocabulary. Depth is a closed set: seven stacking values exist
across the whole site, the header takes the highest, and no new one is introduced.

**Motion.** One house curve carries the wipes and every clip reveal: it rises almost at once and lands flat,
which is why the site reads as machinery rather than jelly. A
press curve, a colour curve and one symmetric curve are the only others. Nothing under
a pointer moves for longer than half a second and most things move in about a fifth of
one. **No transition is ever declared on every property at once**: each one names the
properties it animates. That is the single largest performance problem in a site of
this kind, because one class change anywhere then interpolates a dozen properties
nobody intended.

Six hover moves exist and a seventh would be a mistake: fade, invert ink against
ground, wipe, brighten the border, underline, and lift. Three infinite linear loops run
on the homepage diagram layer at three lengths deliberately chosen not to be multiples
of one another, so the loops drift against each other and the grid never resynchronises.
One shared timeline animates the three stacked homepage cards between two computed
layouts without animating layout itself, so the three cannot desynchronise. One frame
loop exists in the whole document, and every drawn canvas stops drawing when it leaves
the viewport.

Under reduced motion the three loops stop at their resting frame, every scroll-linked
effect snaps to its end state, the wipe becomes a colour change with no travel, and
entrances become opacity alone. **Nothing that carries information is removed**: a bar
that fills still fills, it fills at once.

**Responsive.** Four width thresholds ship and no more: `600px`, `760px`, `900px` and
`1200px`. The capability queries stay: hover, pointer, reduced motion and colour
scheme. There is no light colour scheme; the partial one is deleted rather than half
kept, because half a theme is a tax on every component written afterwards. Below
`1200px` the content column follows the viewport and the gutters narrow. Below `900px`
the two-column bands stack and the feature atlas halves its columns. Below `760px` the
pricing board stacks and the comparison table becomes one column. Below `600px` the
navigation labels switch to their short forms, which are **both present in the document
with one hidden** rather than swapped by script; the hero actions go full width and
stack; the showcase tape becomes a swipeable rail; and the footer columns halve. Every
breakpoint is a layout change and none of them removes a control. Every control a
touch pointer can reach is at least the platform's own minimum touch target, and no
behaviour anywhere depends on hover alone.

**Accessibility.** Every text and ground pairing is measured against the contrast
standard for its own size and raised where it fails, and the measurement is recorded
rather than eyeballed. The two to watch hardest are the
muted warm grey on the ground at the small prose sizes, which carries real sentences in
the feature atlas, and the half-strength off-white on the card ground at the tab-label
size. Every interactive element has a visible focus indicator that is **not** its hover
treatment; the wipe is a hover effect and never a focus indicator. Keyboard navigation
reaches every control in source order, the header is first in source order on every
route, and the framed preview can be both entered and left. Every field has a real
label element and no placeholder stands in for one. Every drawn figure carries a text
alternative saying what it demonstrates rather than what it looks like. The save result
is announced politely. Every classification is carried as its own letter as well as its
ramp colour, so the colour is reinforcement and never the information.

## Front-end specification

### The three route families

Three families, and the chrome differs between them on purpose.

1. **Product routes** carry the full navigation, a coloured hero band and a numbered
   section sequence: `/`, `/docs`, `/ui`, `/plus`.
2. **Reading routes** carry the compact navigation and a striped dossier header:
   `/about`, `/@<handle>`, `/magazine/<slug>`, `/changelog`, `/privacy`, `/terms` and
   the not-found page.
3. **Account routes** carry no navigation at all, only the wordmark, so there is
   nothing to click except the form: `/login` and `/signup`.

### Global chrome

**One header ships, not two.** The full navigation is the one to keep, and the
compact variant is a shorter arrangement of the same component rather than a second
component with its own treatment. The header is sticky, takes the highest stacking
value, sits inset from each side and from the top, and overlays the hero on the
routes that have one. Its ground is the accent and its ink is the dark page ink.
Inside it: the brand lockup at the left, then the link cluster, then the action
cluster. Five labels: Docs, Examples, UI, Magazine, and the paid action. Labels are
mono, uppercase, tracked out.

**The rolling label.** Each navigation label is two stacked copies of the same word
in a container clipped to one line height, the incoming copy parked one line above
the resting one. On hover the pair translates by that one line so the outgoing word
leaves upward as the incoming word arrives. Both copies carry identical text, so the
effect is a mechanical roll and never a change of word. The compact arrangement does
not roll; its links fade instead.

**The search trigger** is a square button holding the magnifier glyph, with no visible
label and no painted shortcut hint. It is reachable by keyboard and it opens the
gallery filtered by the text typed into it. Hover takes it to a lower opacity.

**The wipe** is the site's one signature interaction and it belongs to the primary
action. The action carries a second full copy of itself in inverted ink, parked
entirely off its left edge as a degenerate parallelogram. On hover that copy's clip
expands to a parallelogram wider than the button, so the fill arrives as a diagonal
edge travelling left to right at the same slant as the bars in the wordmark. **Both
label copies swap ink at the moment the diagonal edge passes them**, so the text is
never caught half inverted. The action isolates itself so the wipe clips to it. There
are two variants of the action: a compact solid one in the header, and a striped one
on the reading routes and on the account form whose ground is the hatch and which
rests slightly under full opacity.

**The footer** is light rather than dark, which is the one place the ground inverts.
It opens with the sponsor band: a mono uppercase heading, a sans lead, an action with
an arrow that moves on its own, and a grid of six sponsor rows, each an index
numeral, a mark, a dotted leader and the leaves-the-site glyph. Six sponsors are
named: Prism, Caret, Vector, Keyed, Figment and Verity. Then the newsletter band,
whose field carries a real label even though the label is visually hidden. Then the
column set, which carries the privacy page and the terms page, and which halves its
columns on the narrowest layout.

**The section heading** is one component used on every numbered band: a two-digit mono
index, a kicker in the accent, a sans heading and a lead.

### Components

- **The example card.** A flush thumbnail at a four-to-three ratio over the hatch
  wash, a runtime mark chipped into its top left over a blurred plate, a meta bar
  carrying the title and the save control, and a lock mark in the meta bar when the
  example is paid and the reader has no licence. The save control is the only write
  action on the homepage, which is why an anonymous visitor pressing it gets the
  sign-in path rather than a silent failure. The thumbnail plays on hover in all four
  card states, including the locked one.
- **The category card.** A media well at a four-to-three ratio, a title row with the
  name at the left and a mono count badge at the right, and a two-line blurb.
- **The preview shell.** A framed stage with a mono control row: a runtime selector, a
  shuffle control using the shuffle glyph, and a reset. The well holds exactly the
  size the media will be, so nothing shifts while it loads.
- **The source panel.** Terminal chrome with three dots, a mono filename, and the
  source at mono with one tab per file and a copy control on each tab.
- **The theme panel.** The same terminal chrome over a syntax-coloured source file with
  one highlighted active line, the highlight drawn as an inset left border in the
  accent over a faint wash.
- **The spring strip and plot.** Five mono uppercase tabs over a drawn plot with a tick
  column at the left and a tick row underneath. The plot draws all five curves as thin
  lines and the selected one thick. An accent square beside it runs the selected
  transition. A caret in the accent opens the label row, and the active transition's
  stiffness and damping sit at the right of it.
- **The pricing board.** A hairline grid, the recommended plan on the accent ground
  with the dark ink, a two-digit mono index, a right-aligned flag, a sans display
  name, a one-line blurb, the price over a bottom hairline, a feature list one line
  per feature each prefixed with a plus glyph, and a full-width action.
- **The questions band** closes the paid route: two columns headed `QUESTION` and
  `ANSWER`, one row per frequently asked question, covering pricing, licensing,
  updates and access.
- **The dossier header.** A striped frame carrying a mono kicker, a sans display title,
  the handle, the joined date and the member's links.
- **The account frame.** The striped frame again, a sans heading, a sub line, mono
  uppercase field labels, a forgotten-password link at the right of the password
  label, the striped action, and a switch line to the other account route.

### Iconography

Every icon is inline geometry drawn on its own view box with no fill and the stroke
set to the current ink. Nothing is a font and nothing is a file. The set is
deliberately small: a magnifier, an arrow right, a chevron right, an arrow down, a
leaves-the-site box, a tick, a feed, a shuffle, a split-panes pair, a three-dot more,
and a window. Rendered sizes run from `11px` to `18px`.

The wordmark is one path with two subpaths: three slanted bars and a dot. **The slant
of those bars and the angle of the diagonal hatch are the same angle**, and if either
is redrawn both are. A second mark, the wordmark's glyph alone as a single closed
path, renders as a section device and as the account badge.

Three runtime marks identify the three documented runtimes, each with a full-colour
variant whose colours belong to the runtime's own owner and carried on the mark's own
primitives rather than by any token in this brief, and a single-colour variant that
sets every fill to the current ink. **Only the single-colour variant may be
recoloured.** The component runtime's mark is one ellipse drawn three times under
rotation about a shared origin, not three authored ellipses.

### The not-found figure

The not-found page is designed rather than defaulted, because two of the three
addresses that reach it are addresses a developer types by hand. Its figure is two
drawn canvases side by side on one frame. The left is a wireframe torus, sampled as
rings of points and projected through a simple perspective divide, rotating about two
axes at rates that are not multiples of one another so the figure never repeats; the
back half is drawn first at half alpha, and the visible cusps are a property of the
sampling rather than an added highlight. The right is a histogram strip: sixty-four
horizontal bars stacked down the strip, each one pixel tall on a four-pixel pitch,
extending leftward from the right edge, their lengths a smoothed noise series seeded
once per page load and drifting upward slowly, with two or three bars per screen at
full alpha as accents. Both stop drawing when off screen.

### The homepage

Ten numbered bands under the header and the hero.

The hero is a full-bleed band on the amber ground with a dark card starting in from
the left holding everything. A kicker row carries `Open source / MIT License` at the
left and `v13.1.0` at the right. The title is four lines at the display size with the
brand word set in the accent and followed by a full stop: `Tempo.` then
`Production-grade` then `animation library` then `for the web.` **The title carries a
clip that wipes it in from the left, played once on load**, on the house curve, and it
is the same shutter as the action's wipe. Two actions, `Get started` and
`Browse examples`. Then a runtime row: a caret in the accent, the label
`Prev Loom Studio Motion. Available for:`, and three chips reading `React`,
`JavaScript` and `Vue`.

The proof strip sits directly under the hero, still on the accent ground, carrying
the three runtime names spread evenly and `Tempo 13.1.0` pushed right. Below it, five
claim cells on the dark ground, each a mono uppercase term in the accent and a sans
description: `Free` with `Completely free to use, MIT licensed and open source.`,
`Production ready`, `Hybrid engine` with
`JavaScript and hardware-accelerated browser APIs in one library.`, `Built for AI`,
and `Tiny footprint`.

The feature atlas is the most characteristic layout on the site: a hairline grid of
eight cells, four across and two down. Each cell has a stage in its upper portion
holding one drawn figure, then a two-digit mono index in the accent, a sans heading
with an arrow that moves on hover, a two-line blurb, and a mono readout that is a
syntax-coloured fragment of the thing being demonstrated. The eight, in order:
`Independent transforms`, `Scroll animation`, `Native gestures`, `Layout animation`,
`Spring physics`, `Exit animation`, `Timeline sequences`, `Motion values`. Two of the
eight invert: their stage takes the accent as its ground and the readout ink flips to
the dark ink. The atlas closes with `AVAILABLE FOR`, the three runtime chips, and
`ALL DOCUMENTATION`.

Then the examples grid of six cards, the showcase tape as a single row of published
member projects that runs wider than the viewport and moves horizontally under
scroll, the workflow fork, the changelog column, the magazine column, and the
documentation directory.

### The scrubbed timeline

One band on the paid route is a pinned stage held across a long scroll track with
four stages passing through it. **It scrubs both ways**: scrolling back up
un-reveals exactly what scrolling down revealed, rather than snapping to a resting
state. The curtain over it clears in the same scroll distance at every width. No
scroll-linked effect changes a layout property. Below the tablet threshold the pinned
track shortens with its stages, and below the next threshold down the pinned stage is
replaced by a progress readout. **The one structural risk on this route is that pinned stage**, because it holds four
full screens of content inside a sticky frame across a very long track. **Each pinned
stage therefore has its own heading in the document outline at its own address, and a
skip control visible on focus**, so
somebody moving by keyboard or by heading can get past four screens of content
without scrolling through them.

### Assets

**No binary asset ships.** Every icon, texture, figure and mark is drawn from
coordinates or from a gradient.

- a catalogue card's still frame is rendered at build time from the item's own preview
  bundle at the first frame of its animation, so it is regenerated whenever the
  example changes and can never drift from what the example now does
- while it loads, its place is held by a gradient generated from the item's own
  identifier, so the same item always gets the same two colours, rendered inline
  rather than fetched
- a member portrait that has not been supplied is a flat tile at a colour derived
  from the handle with the first two characters of the handle set in the mono family
- a sponsor mark that has not been supplied is the sponsor's name set in the mono
  family, uppercase and tracked out, which is a legitimate final treatment as well as
  a stand-in
- the hatch, the dot field and the ruler are gradients, which is why the site needs no
  texture file at all
- both families are named rather than shipped, and at most four font files load

### Structure

- one header component ships, not two
- four width thresholds ship, not the twenty-five the reference measured
- the light colour scheme is removed rather than left half finished
- the not-found document is rendered on the server and carries the not-found status
- exactly one of `/docs` and `/docs/` is canonical, and exactly one of `/ui` and `/ui/`

### Performance

- no video plays on its own above the fold, and every media well has intrinsic
  dimensions so nothing shifts
- at most three previews run at once and an off-screen preview is destroyed
- the drawn canvases stop drawing when off screen and cap their pixel density at twice
  the device's own
- one frame loop exists in the whole document
- a route's content is the document the server sent, not a skeleton filled in by a
  second request

## Technical requirements

Serve this site as server-rendered pages with hydrated islands, not as a client-side
application that fetches its own HTML. The frontend framework is **Nuxt 3** and the
read and write surface under `/api` is **Hono**, mounted inside Nuxt's own server so
one process serves both on one origin and one port. The first paint a browser
receives is the complete document for the route, rendered on the server from the
published catalogue, the release records and the signed-in member's own rows. Only
the islands that need a client hydrate: the gallery's filter row, the preview stage,
the theme file's tab strip and its plot, the save control and the purchase panel. A
route's content is never a skeleton that JavaScript fills in from a second request,
and **a facet combination is a server-rendered address rather than a client-side
re-sort of a list already in the browser**.

**The backend architecture is one process and three trust boundaries.** The process
serves the rendered pages and the read and write surface. The first boundary is the
session: a request either carries a valid bearer token or it does not, and nothing
below that line guesses. The second is the licence: paid bytes leave the process only
for a request whose licence row resolved. The third is the preview frame, which is
treated as hostile code running next to a signed-in session. Every behaviour in this
brief that matters is a behaviour at one of those three boundaries.

**The module architecture is five primitives and nothing below them.** A surface, a
frame, a control, a plate and a well: every component on the site is built from those
five, and a component that needs a sixth is a component that has not been thought
through. State that outlives a component lives outside it: the session, the resolved
entitlement, the preferred runtime and the reduced-motion preference are read once per
request and passed down, never re-derived inside a leaf.

**The rendering strategy is stated per route, not per component.** A product route is
rendered on the server and hydrates its named islands. A reading route is rendered on
the server and hydrates nothing. An account route is rendered on the server and
hydrates only its form. No route renders itself twice.

The datastore is **PostgreSQL**, read from `DATABASE_URL`, which the environment
also injects as `DB_URL` carrying the same value. Billing lives in **Kill
Bill**, a subscription-billing platform, read from `PAYMENTS_API_URL`,
`PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`, `PAYMENTS_BASIC_USER` and
`PAYMENTS_BASIC_PASSWORD`. Mail is sent over SMTP to `SMTP_HOST`. The app's own
address and port come from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a
host or a port; read every one of them from the environment. All three backing
services are **already running** and reachable at those variables and must not be
downloaded, installed, compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, cache, queue, object store, identity provider or mail vendor: the
only backing services available in this environment are PostgreSQL, Kill Bill and
Mailpit, and reaching for anything else is a contract violation.

**Kill Bill is a billing platform and not a card processor.** It holds accounts, a
catalog, subscriptions and invoices. It has no charge object, no card token and no
decline code, and this app never sees a card number. What the app does with it is
narrow and complete: on a completed purchase it creates one account under the
licence's own external key, and it reads that account back by that key. It refers to
a billing account by the external key and never by the identifier Kill Bill
generates, because a generated identifier is not a thing the app can state in
advance. It names no plan and creates no subscription. Every call carries the API
key, the API secret, the admin basic credential and a header naming the writer.

**Identity, and the principle behind it.** No account is required to read anything.
An account exists for exactly two jobs here: to hold what somebody bought, and to
hold what somebody saved or submitted. It holds an identifier, a handle, an
authentication method, a display name, the links on their profile, a preferred
runtime and the list of things it owns, and nothing else: no history of what was
read and no stored analytics.

Authentication is app-implemented email and password with bearer tokens, as described
under `### Auth`. Passwords are stored hashed and never in a recoverable form.
Authorisation is by ownership and by entitlement, and nothing else in the product
checks a role at all.

**The entitlement claim is resolved per request from the licence row**, never carried
inside the bearer token and never cached past the request that read it. A licence with
a revocation date stops unlocking anything on the next request. If the licence cannot
be read, the claim is refused: entitlement fails closed.

**Rate limiting and abuse.** Per-address rate limiting applies to sign-in and to
account creation with a low burst and a low sustained rate, because a failed sign-in
is cheap for the caller and expensive for everyone else. Saves and showcase
submissions are limited per account rather than per address. Reading the manual is
**not** limited beyond ordinary network protection and never carries a challenge: a
documentation site that challenges its readers has chosen the wrong threat model.
Every limited response states the limit, the remaining allowance and when it resets,
and a limited response carries the same body shape as a validation failure so no
client needs a second error path for it.

**The bot and automation policy is identification, not exclusion.** An automated
reader is welcome here. A sitemap is served at `/sitemap.xml` listing every public
route, `/robots.txt` points at it, and **no challenge is ever placed in front of the
manual**. Friction belongs on account creation alone.

**Secrets and the supply chain.** Every credential the app uses is read from the
environment, is scoped to the one service it belongs to, and is never written to a
file the app serves. Every dependency is pinned to an exact version, and the pinned
set the preview frame loads is the same pinned set the published example names, so a
visitor's preview and a buyer's copy cannot diverge.

**Every write accepts an idempotency key and honours it for 24 hours.** A purchase
requires one. The second request with the same key returns the first outcome and
writes nothing.

`GET /api/health` returns `200` once the app is ready to serve. Log each request as
one structured line carrying the method, the path, the status and the elapsed
milliseconds, to standard output.

**Headers on every response.** Every response carries a strict transport policy, a
nosniff content-type policy, a frame policy, a referrer policy and a content security
policy. The content security policy for the framed document that runs an example or a
section names the app's own origin as the only destination it may reach, and it denies
form submission, top-level navigation, popups and downloads for that frame. **That
document is served without the session cookie**, so script inside it has no session to
read.

**Nothing the browser downloads carries a credential.** No database URL, no billing
API key, no billing API secret, no billing admin password, no mail host and no bearer
token belonging to another account appears in any document, script, stylesheet or
JSON the browser can fetch.

**A favicon** is served at `/favicon.ico` and declared in the document head of every
route.

**Every public route declares its own title and description**, and no two routes share
either. `/docs/react/use-spring` and `/docs/13.0.4/react/use-spring` differ, because
the release is part of what the route is about, and a faceted gallery address
describes the facets it was narrowed by.

**Money is integer minor units and a currency code**, everywhere it is stored,
returned or compared. A decimal fraction is never the stored form of an amount. A
displayed price is formatted from the minor units at the moment it is rendered.

**Dates are one format in one timezone**, everywhere. Collections are cursor
paginated with a stated maximum page size and never offset paginated, because a list
paginated by offset skips or repeats rows while it is changing underneath the reader.

**The two stores are separated by rule.** Content is immutable, versioned, built from
source and published as a generation, and nothing writes to it at runtime.
Application data is everything a person creates. **No foreign key crosses from
application data to content data**: an application row references content by its
stable identifier and the generation it was read at. Content rows are replaced
wholesale on every release, so a foreign key would either block the release or cascade
a deletion through a member's saved rows.

**Versioning and invalidation.** Content is published as one numbered generation.
Versioning is by release: a documentation page exists once per retained release and
the rows for a release are never edited after it is published. Invalidation has
exactly one path, and that is publishing a newer generation; there is no second way to
expire a content row, and nothing invalidates a row in place.

**Responses have one shape.** A success carries the resource plus the release stamp it
was read at. A failure carries a stable machine code, a human message and the address
of the page that explains it. A validation failure carries a field-keyed map. A
rate-limited response carries that same shape. Responses never differ in shape between
two failures of the same kind.

**Every count in the copy is a query.** The example total, the tutorial total, the
section total, the category total and every per-category count are read from the
published generation when the page is rendered. No numeral describing the size of the
catalogue is typed into a template, and two places quoting the same count read the
same query.

**Determinism where the site makes a promise.** A catalogue card's still frame for
one example at one generation is the same bytes every time, on any machine and after
a restart, which is what lets it be addressed by the digest of those bytes. The
holding gradient for one identifier is likewise the same two colours every time.

**Budgets are enforced from outside the thing being budgeted.** A preview that has not
reported itself ready is stopped by the page around it at 5 seconds of wall clock,
and no more than three previews run at once. Code that never yields cannot be stopped
by code inside it.

**The preview frame reaches nothing.** It is served from the app's own origin, with no
session cookie, with a policy naming that origin as its only destination. A request
from inside it for a member surface is refused exactly as a request with no credential
is refused. That refusal is observable: the frame reports it and the page states it,
rather than failing silently.

## Data model

Fifteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a credential to protect. Hash it as normal; the exact literal must
work at login, and it must be written into `/app/USER_README.md` alongside each
account so a grader can sign in.

### Content, immutable and versioned

**`releases`** - `version` unique, `released_on`, `channel`, `is_current`. Three rows
are seeded and exactly one carries `is_current`:

| version | released_on | is_current |
|---|---|---|
| `13.1.0` | `2026-09-02` | true |
| `13.0.4` | `2026-07-19` | false |
| `12.8.2` | `2026-04-08` | false |

The section library carries its own version, `0.0.2`, which is not one of these and
is shown as its own numeral wherever the section library is named.

**`categories`** - `path` unique, `name`, `blurb`, `position`. Nine rows, exactly as
tabled under core feature 3, in that order.

**`examples`** - `id`, `slug` unique, `title`, `category_path`, `tier` in `free` or
`paid`, `runtimes`, `published_at`, `save_count`, `generation`. Seven rows:

| slug | title | category_path | tier | runtimes | published_at |
|---|---|---|---|---|---|
| `scroll-velocity` | Scroll velocity | `stats-sections` | `free` | `react`, `js`, `vue` | `2026-09-01` |
| `parallax` | Parallax | `hero-sections` | `free` | `react`, `js`, `vue` | `2026-08-22` |
| `skeleton-shimmer` | Skeleton Shimmer | `bento-grids` | `free` | `react`, `vue` | `2026-08-14` |
| `floating-action` | Floating Action | `cta-sections` | `free` | `js` | `2026-07-30` |
| `ios-app-folder` | iOS App Folder | `page-transitions` | `paid` | `react` | `2026-08-27` |
| `ios-pointer` | iOS Pointer | `navigation` | `paid` | `react`, `js` | `2026-08-05` |
| `ticker-marquee` | Ticker | `testimonials` | `paid` | `react`, `js`, `vue` | `2026-06-11` |

`save_count` is the count of that example's own `saved_items` rows, read from them
rather than kept in step by hand.

**`example_files`** - `id`, `example_id`, `path`, `language`, `source`. At least one
row per example. The `source` of a `paid` example's files is the thing the licence
protects, and it is what must be absent from a response served without the licence.

**`sections`** - everything an example has, plus `registry_name`, `theme_keys` and
`token_contract`. Six rows:

| slug | title | category_path | theme_keys |
|---|---|---|---|
| `editorial-stagger-hero` | Editorial stagger hero | `hero-sections` | `transitions.gentle`, `stagger.relaxed`, `travel.enter` |
| `border-beam` | Border beam | `cta-sections` | `transitions.ambient` |
| `confetti` | Confetti | `cta-sections` | `transitions.lively`, `travel.enter` |
| `command-palette` | Command palette | `navigation` | `transitions.snap`, `stagger.tight` |
| `coverflow` | Coverflow | `testimonials` | `transitions.ui`, `travel.hover` |
| `sheet` | Sheet | `page-transitions` | `transitions.ui`, `travel.section` |

`token_contract` names the style tokens the section expects the buyer to have
defined, which is what makes the claim on the category grid checkable before a
section is installed rather than after it looks wrong.

**`theme_values`** - `key` unique, `value`, `kind` in `transition`, `stagger`,
`travel` or `preference`, `position`. Twelve rows, exactly as tabled under core
feature 3. The five `transition` rows carry a stiffness and a damping; the three
`stagger` rows and the three `travel` rows carry one number each; `reducedMotion`
carries `"calm"`.

**`doc_pages`** - `id`, `slug`, `runtime` in `react`, `js`, `vue` or `shared`,
`title`, `summary`, `body`, `since_version`, `deprecated_version`, `tier`,
`generation`, unique on runtime, slug and generation. Seven rows per retained
release:

| runtime | slug | title | since_version | tier |
|---|---|---|---|---|
| `shared` | `installation` | Installation | `12.8.2` | `free` |
| `react` | `use-spring` | useSpring | `12.8.2` | `free` |
| `react` | `animate-presence` | AnimatePresence | `13.0.4` | `free` |
| `react` | `layout-animation` | Layout animation | `13.1.0` | `paid` |
| `js` | `animate` | animate | `12.8.2` | `free` |
| `js` | `scroll` | scroll | `13.0.4` | `free` |
| `vue` | `motion-component` | Motion component | `12.8.2` | `free` |

**`doc_code_blocks`** - `id`, `doc_page_id`, `position`, `language`, `runtime`,
`is_runnable`, `source`, `executed_against_version`. The last column is what lets a
page state that its runnable blocks ran against the release the page is serving, and
lets a block whose last execution was older be marked rather than presented as
current.

**`changelog_entries`** - `id`, `slug` unique, `version`, `kind`, `title`, `body`,
`published_at`. Four rows:

| slug | version | kind | title | published_at |
|---|---|---|---|---|
| `spring-presets` | `13.1.0` | `feature` | Five named spring presets | `2026-09-02` |
| `exit-animation-fix` | `13.0.4` | `fix` | Exit animations no longer skip their last frame | `2026-07-19` |
| `pointer-gesture-fix` | `12.8.2` | `fix` | Pointer gestures respect a cancelled press | `2026-04-08` |
| `ui-registry-install` | `0.0.2` | `release` | Sections install from the registry | `2026-08-30` |

The last row belongs to the section library rather than to the library and carries
its own badge saying so.

**`articles`** - `id`, `slug` unique, `title`, `standfirst`, `body`, `author_handle`,
`published_at`. Three rows:

| slug | title | author_handle | published_at |
|---|---|---|---|
| `springs-over-easing` | Springs over easing curves | `alex` | `2026-08-28` |
| `the-all-problem` | The cost of animating everything | `alex` | `2026-07-15` |
| `reduced-motion-is-not-no-motion` | Reduced motion is not no motion | `alex` | `2026-06-04` |

`author_handle` is content and is not a reference to an account row, which is the
no-crossing rule in practice: an article outlives whoever wrote it.

**`price_bands`** - `code` unique, `region`, `amount_minor`, `reason`. Two rows:

| code | region | amount_minor | reason |
|---|---|---|---|
| `list` | `US` | `24900` | |
| `ppp-south-asia` | `IN` | `14900` | `Local discount applied` |

A band is a row in this table and never a formula. A region with no row here resolves
to `list`.

### Application

**`accounts`** - `id`, `handle` unique and case folded, `email` unique and case
folded, `display_name`, `links`, `password_hash`, `preferred_runtime`, `joined_at`.
Three rows are seeded, as listed in `## User roles`:

| email | handle | display_name | joined_at |
|---|---|---|---|
| `member@example.com` | `nova` | Nova Reyes | `2026-03-11` |
| `member2@example.com` | `kit` | Kit Alvarez | `2026-06-02` |
| `member3@example.com` | `sol` | Sol Danner | `2026-09-10` |

**`sessions`** - `token`, `account_id`, `issued_at`, `expires_at`. A token expires 24
hours after it is issued.

**`licences`** - `id`, `external_key` unique, `order_id`, `owner_account_id`, `kind`,
`entitlements`, `valid_from`, `valid_until`, `revoked_at`. One row is seeded:
`external_key` `tempo-plus-nova`, owned by `member@example.com`, `kind`
`personal-perpetual`, `valid_until` null because a perpetual licence does not expire,
`revoked_at` null. A licence is never mutated: a change is a new row.

**`orders`** - `id`, `account_id`, `licence_id`, `currency`, `list_amount_minor`,
`discount_amount_minor`, `total_amount_minor`, `price_band_code`, `discount_reason`,
`state`, `created_at`. One row is seeded, against `tempo-plus-nova`: currency `USD`,
`list_amount_minor` `24900`, `discount_amount_minor` `0`, `total_amount_minor`
`24900`, `price_band_code` `list`, `state` `paid`. An order is never deleted.

**`saved_items`** - `id`, `account_id`, `example_id`, `generation`, `saved_at`,
unique on `account_id` and `example_id`. Two rows are seeded, both for
`member@example.com`: `scroll-velocity` and `parallax`. The unique pair is what makes
a repeated save leave one row without an application-level guard.

**`pending_saves`** - `id`, `session_hint`, `example_slug`, `created_at`. One row per
save attempted while signed out, consumed when that visitor signs in. None are
seeded.

**`showcase_projects`** - `id`, `account_id`, `title`, `source_url`, `description`,
`state` in `submitted`, `published` or `rejected`, `submitted_at`, `reviewed_at`,
`rejection_reason`. Two rows are seeded, both for `member@example.com`:

| title | source_url | state |
|---|---|---|
| Orbit Atlas | `https://orbit-atlas.example.com` | `published` |
| Field Notes | `https://field-notes.example.com` | `submitted` |

Only a `published` row reaches a public response.

**`idempotency_records`** - `key`, `account_id`, `endpoint`, `response_body`,
`created_at`. Honoured for 24 hours.

### Retention

| Row | Kept |
|---|---|
| a pending save | 24 hours, then dropped |
| an idempotency record | 24 hours, then dropped |
| a session | until its expiry, then dropped |
| a rejected showcase project | 30 days, then dropped |
| an order and its licence | kept, never deleted |
| a published showcase project of a deleted account | kept and anonymised rather than removed |

### What the app writes to the billing platform

One call per completed purchase, creating a billing account whose external key is the
licence's own `external_key`, whose name is the buyer's display name, whose email is
the buyer's email address, whose currency is `USD` and whose country is `US`. The app
reads it back by that external key and never by the identifier the platform
generates. The platform already holds three accounts of its own from its bootstrap,
`orbit-amelia`, `orbit-acme` and `orbit-northwind`, and this app neither reads nor
writes them: a purchase adds one account and leaves every other account untouched.

## Constraints

- One site, no tenancy: every reader sees the same published generation.
- One product: no per-seat team plan, no seat stepper, no seat transfer, no renewal
  cycle and no annual billing. The licence is bought once and does not expire.
- No refunds, no dunning, no stored payment method and no card of any kind: the
  billing platform holds accounts and invoices, not charges.
- No tax calculation and no tax record.
- No animation performance audit service: no grade, no report, no worker fleet, no
  continuous-integration gate and no audit table.
- No agent context service: no tool server, no skills, no editor bridge and no
  machine-readable twin of a page.
- No moderation worker, no automated screening, no transcoding, no takedown queue and
  no uploaded media anywhere: a showcase project carries a title, an address and a
  description.
- No external code sandbox handoff and no third-party editor link.
- No site-wide search overlay and no machine search endpoint: narrowing happens on
  the gallery's own address.
- No book, no sponsor route, no advertise route and no troubleshooting route.
- No private package registry and no members-only chat platform.
- No second language: every route is served in one language and there is no language
  segment, no language switch and no translation record.
- No consent banner, no third-party script and no product analytics, because nothing
  recorded carries an identifier.
- No external network call at runtime: the site answers every route from PostgreSQL,
  the billing platform, and its own published source.
- No native application and no installable app shell.
- One colour mode, the laboratory dark. No light scheme for the product chrome; the
  footer is the one surface that inverts, and it does so by design rather than by a
  scheme switch.
- The site stays responsive with three retained releases of seven documentation pages
  each, seven examples, six sections, nine categories, four changelog entries and
  three articles.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not be
  running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy of
  any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every list endpoint returns a top-level JSON array. Bearer auth is carried on
everything except `GET /api/health`, `POST /api/v1/auth/login` and
`POST /api/v1/auth/signup`. A successful call returns the named resource or shape; an
invalid or unauthorized call is rejected as a client error, never with a `5xx` and
never with a silent success.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/v1/auth/signup` | `email`, `name`, `handle`, `password` | `token`, `member` with `id`, `email`, `name`, `handle` |
| `POST /api/v1/auth/login` | `email`, `password` | `token`, `member` |
| `POST /api/v1/auth/logout` | none | `{}`, and the token is retired |
| `GET /api/v1/me` | none | `member`, plus `entitled` resolved from the licence row |
| `GET /api/v1/releases` | none | array of `version`, `released_on`, `is_current` |
| `GET /api/v1/docs/{runtime}/{slug}` | none | one page with `title`, `summary`, `body`, `since_version`, `tier`, `release` naming the current release, and `code_blocks` each with `source`, `is_runnable` and `executed_against_version` |
| `GET /api/v1/docs/{version}/{runtime}/{slug}` | none | the same shape with `release` naming that version |
| `GET /api/v1/examples` | `runtime`, `category`, `access`, `saved`, `sort`, `cursor`, `limit` | `items` array of `slug`, `title`, `category`, `tier`, `runtimes`, `save_count`, `saved`, `locked`, `poster`; plus `total` and `next_cursor` |
| `GET /api/v1/examples/{slug}` | none | one example with `files` when the reader may read them, and `locked` true with no `files` key when they may not |
| `GET /api/v1/examples/{slug}/files/{path}` | none | the file source, or a refusal when the reader holds no licence |
| `GET /api/v1/categories` | none | array of `path`, `name`, `blurb`, `section_count` |
| `GET /api/v1/sections` | `category` | array of `slug`, `title`, `category`, `theme_keys`, `token_contract` |
| `GET /api/v1/theme` | none | array of `key`, `value`, `kind` |
| `GET /api/v1/pricing` | none | `list_amount_minor`, `currency`, `band` with `code`, `amount_minor` and `reason`, and `banner` true only when the band is not `list` |
| `POST /api/v1/purchases` | `display_name`, `email`, `idempotency_key` | `licence_key`, `order` with `total_amount_minor`, `currency`, `price_band_code`, `discount_reason`; or a refusal naming the licence key that is taken |
| `GET /api/v1/saved` | none | array of the caller's own saved examples |
| `POST /api/v1/saved` | `example_slug` | the saved row; the same call twice returns the same row |
| `DELETE /api/v1/saved/{example_slug}` | none | `{}`, and the row is gone |
| `GET /api/v1/members/{handle}` | none | `member`, `joined_at`, `links`, `projects` holding published rows only |
| `POST /api/v1/showcase` | `title`, `source_url`, `description` | the project with `state` `submitted` |
| `GET /api/v1/showcase/{id}` | none | the project to its owner; a refusal to anybody else while it is not published |
| `GET /api/v1/changelog` | `cursor`, `limit` | `items` newest first, each with `slug`, `version`, `kind`, `title`, `published_at`; plus `next_cursor` |
| `GET /api/v1/magazine` | `cursor`, `limit` | `items` newest first, each with `slug`, `title`, `standfirst`, `author_handle`, `published_at` |
| `GET /api/v1/magazine/{slug}` | none | one article |

### No mocks

PostgreSQL, the billing platform and the mail transport are the facts. A licence the
app holds in a module-level dictionary, a billing account the app records in its own
table and never creates in the platform, a receipt the app logs instead of sending, a
`locked` flag the app computes from a hardcoded list rather than from the licence row,
a `total` the client calculates and the server trusts, a paid file's source served
from a route the entitlement check does not cover: each of these is a contract
violation however good the page looks. The named provider is the fact - the app's UI
and its own tables can only reflect what lives in the provider, never substitute for
it.

## Definition of done

A developer can narrow the gallery to their own runtime and category, send that
address to a colleague and get the same list back, open one example and watch it run,
read a free example's source and be refused a paid one's by every address, buy
lifetime access once and get one receipt for the amount the banner showed, save an
example and find it still saved after a reload and listed on their own profile, and
save one while signed out and find it saved when they sign in. A paid example's source
never reaches a reader without the licence, and an entitlement the app cannot resolve
refuses rather than allows.
