# Curated Box Subscription

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a
browser, sign in, build a box of three books from this month's reveal, place it,
and see the order confirmed, without hitting an error page.

A different stranger, signed in as somebody else, must NOT be able to read that
box or that order by any means, including a direct API call with their own
token. And the order's invoice must exist as a real record in `killbill` for the
exact computed total; a total the app renders back to itself does not count.

## Overview

Pangolin Books is a monthly book subscription in which the member builds the box.
Most clubs post a surprise. This one reveals a shortlist on the first of every
month and lets the member choose from it, under one rule:

```text
We drop new books on the 1st of every month.
The first of every month we reveal 6-7 new books.
Members can order up to 3 books per box.
At least one title must be from the current month's selections.
```

The people who use it are readers who want the curation without the surprise.
They browse a reveal, a full catalogue and a deliberately flat set of playful
tags, build a box, and place it. Once a year they vote on their favourite read
and the winner is reprinted as a new edition they can order. They can buy the
membership for somebody else as a gift, and the person who receives it picks
their own books.

Five things make it distinctive, and each is a requirement rather than a
flourish: the member chooses; the taxonomy is flat and puts `Includes a Dog`
beside `Fantasy`; an annual members' vote produces a reprint; the mascot's ears
twitch on the buttons; and the price is a formula per country rather than a plan
table.

What it deliberately is not: there are no comments, no likes, no messaging, no
member profiles, no reviews and no ratings. There is no native mobile
application. There is no second origin: one application serves the marketing
pages and the ordering surface together.

The genuinely hard part is that the composition rule is a property of the
finished set, not a filter on what may be browsed. Every edition stays addable at
every moment, and it is the box that becomes valid or invalid and says why. A
build that greys out ineligible books has misunderstood the product.

## User roles

| Role | Can do |
|---|---|
| Visitor (signed out) | Browse the home reveal, the catalogue, any edition page, the FAQ, the gifting page and the privacy page. Buy a gift subscription. Redeem a gift code. Sign up. **Cannot build or place a box, cannot vote, cannot read any account.** |
| Member (signed in) | Everything a visitor can do, plus build and place their own box, read their own orders, credit balance and credit ledger, cast one ballot per vote round, and manage their own subscription. **Cannot read or change another member's box, order, credit ledger, ballot or subscription. Cannot vote twice in one round. Cannot redeem their own gift code.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
button in the UI is not authorization: a direct API call from a Visitor session
to any Member-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged. The same
holds between two Members: a request from one member's session for another
member's box, order or credit ledger is denied, and the target row is unchanged.

Signup is open. Anybody can create a membership from `/signup`.

These accounts are seeded so the product can be exercised immediately. Every
seeded account uses the password `deku-demo-pw-2026`.

| Email | Country | Subscription | Credits |
|---|---|---|---|
| `member@example.com` | `US` | active | 0 |
| `member2@example.com` | `CA` | active | 1 |
| `member3@example.com` | `US` | active | 1 |

## Core features

### Auth

Email and password, implemented by the app. Passwords are stored hashed, never
in plain text. The JSON API authenticates with a bearer token issued at login and
sent on every request except login, signup and `GET /api/health`. Tokens expire;
an expired token on a member route returns the visitor to the sign-in page with
their destination preserved, and nothing they had in the box is lost. Signup is
open and takes an email, a password and a country of `US` or `CA`.

### The monthly cycle

1. A cycle has an open and a close. It opens at `00:00:00` UTC on the first of
   its month and closes at `00:00:00` UTC on the first of the next. That is the
   stated instant, and it is the same instant for every member in every country.
2. The reveal is atomic. The six or seven editions of a cycle become current
   together. A member must never see three of the new titles beside four of the
   old ones, at any moment, by any route.
3. Applying a reveal is idempotent. Running it a second time for a cycle that has
   already opened changes nothing: no edition moves, no edition is duplicated.
4. A box being built when the cycle turns is told, not silently invalidated. The
   page states `This month's selections closed on the 1st. Here's what's new.`
   and the box is re-tested against the cycle it now belongs to.

### The catalogue and the tags

1. `/allbooks` lists every orderable edition and filters by genre. The browse
   genres are `Horror`, `Science Fiction`, `Romance`, `Thriller`,
   `Literary Fiction`, `Fantasy`, `Gothic Fiction`, `Historical Fiction`,
   `Magical Realism` and `Contemporary Fiction`. The catalogue's own copy closes
   that list with `and more!`, which is copy and is never a genre a member can
   filter by.
2. An edition's own tags come from one flat list, and the list stays flat:
   `Fantasy`, `Mystery`, `Thriller`, `Historical`, `Horror`, `Romance`,
   `Literary`, `Satire`, `Award Worthy`, `LGBTQIA+`, `Pangolin Original`,
   `Includes a Dog`, `Includes a Cat`. Genres, a quality judgement, a
   representation marker, a publisher marker and whether there is a dog in it sit
   in one list as equals. A tag carries a kind so it can be filtered on, and it
   renders identically whatever its kind. Splitting the list into genres,
   content warnings and badges is a contract violation: `Includes a Dog` sitting
   beside `Fantasy` as an equal is the product's voice.
3. Each edition has its own page at `/books/<slug>` carrying a cover, a name, a
   description of two or three sentences, and its tags. Some carry a
   `SPECIAL EDITION` ribbon.
4. The same work can exist as several editions: an original, a reprint, a second
   reprint, a vote-winner edition. They are distinct products with distinct
   availability. `Salt and Static` and `Salt and Static (Reprint)` are one work
   and two editions, and every surface treats them as two.

### The box, and the rule that is the whole product

1. A box belongs to exactly one cycle and holds between one and three editions.
2. A box may be placed only when it holds at most three editions and at least one
   of them belongs to the box's own cycle. Validity is a property of the SET and
   is evaluated when the box is placed, never as items are added.
3. Every edition stays addable at every moment. No control is disabled, greyed
   out or hidden because adding it would leave the box invalid. What changes is
   whether the box may be placed, and the stated reason changes as editions are
   added and removed.
4. A box holding no edition from its own cycle is refused when placed, and the
   page states `Add at least one book from this month to complete your box.`
5. A fourth edition is refused, the box is unchanged, and the page states
   `Three books is the limit. Remove one to add another.`
6. The same edition is never added twice to one box.
7. `Salt and Static (Reprint)` is not `Salt and Static`. A box holding the
   reprint and nothing from the current cycle is refused: the two are separate
   records and the rule sees them as the member does not.
8. A box may be pre-seeded from a link: `/box?ids=<slug>,<slug>,<slug>`. The ids
   in that link are a suggestion from a stranger and never an instruction. The
   server reads the slugs in order, drops any that name an edition which is not
   orderable, keeps at most the first three, and rebuilds the box from what
   survives. The rebuilt box then faces the same validity test as any other, and
   the member is told what was dropped. A link carrying four ids, or three from
   last month, is handled; it is never accepted as given.
9. Placing a box is idempotent. Submitting the same box a second time creates no
   second order and no second invoice; the member is returned to the same
   confirmation.
10. A box placed and then cancelled against still ships: cancelling a membership
    takes effect at the close of the paid cycle and a box already placed is not
    withdrawn. A member cancels from their own account, and the subscription
    carries the instant it ends at rather than ending there and then.
11. Placing a box closes it and opens a new empty box for the same cycle, so a
    member always has a box they can build. A member may place more than one box
    in a cycle, and each placed box is priced on its own: every order carries the
    base charge plus one extra-book charge per book beyond the first. The
    promotional code is the exception, and it is already bound to a member's
    first order.

### Pricing

1. There is one membership, not a table of plans. Its price is a base that covers
   one book plus a charge for each extra book, both stored per country and
   computed from there. A stored matrix of totals is a contract violation: the
   same figures appear on the home page, the FAQ and the box.
2. The two countries served are `US` in `usd` and `CA` in `cad`, with the same
   membership on both:

   | Country | Base, covering one book | Each extra book |
   |---|---|---|
   | `US` | `1799` | `1099` |
   | `CA` | `2599` | `1599` |

   All money is integer minor units. `1799` is `$17.99`, not `17.99` and not
   `17`.
3. Worked totals, which the running app must reproduce exactly:

   | Country | 1 book | 2 books | 3 books |
   |---|---|---|---|
   | `US` | `1799` | `2898` | `3997` |
   | `CA` | `2599` | `4198` | `5797` |
4. The membership charges even at one book. The base covers one book whether or
   not one is picked, so a member who is charged and chooses nothing is still
   owed a book. When a cycle closes and a member with an active subscription
   placed no box in it, one credit is banked to that member with a ledger entry
   naming that cycle. This grant happens at most once per member per cycle,
   however many times it is applied.
5. The total charged equals the total shown. A box carries the base and the extra
   that applied when it was placed, so a later change to `US` or `CA` pricing
   does not move a total that has already been agreed.

### The promotion

1. `SUMMER` is a promotional code. It replaces the base charge with `400` for a
   member's first order only, it is valid in `US` only, and it expires at the
   close of the cycle that is current when the app first starts.
2. Worked example: a `US` member's first order of three books with `SUMMER` is
   `400` plus `1099` plus `1099`, which is `2598`.
3. A `CA` member who enters `SUMMER` is refused and the page states
   `That code is for USA orders only.`
4. A `US` member who has already placed an order is refused, as is a member who
   enters it after it has expired. The box is unchanged in both cases.

### Credits

1. A credit is a second currency with its own ledger, separate from the monthly
   entitlement. Credits are earned from the postcard challenge in each box and
   banked when a paid cycle closes unchosen, and they are spent against books.
2. Each credit removes the charge for one book. Credits are applied to the base
   charge first, then to each extra-book charge in turn. The order is fixed and
   is the same on every surface that shows a total.
3. Worked example: a `US` member placing three books with one credit pays
   `0` plus `1099` plus `1099`, which is `2198`. With two credits they pay
   `1099`.
4. When a credit is applied the page states `One free credit applied. You have
   <n> left.` with `<n>` the balance that remains.
5. A member never spends more credits than their balance, and the balance is the
   sum of their ledger entries rather than a number kept beside them.
6. A credit and a promotional code are never applied to one order. Whichever is
   offered second is refused and the box is unchanged.
7. If an order does not complete, the credit is not spent: no ledger entry is
   written and the balance is what it was.

### Placing the box, and the invoice

1. Placing a valid box creates an order carrying the computed total and the
   currency of the member's country, and lands the member on its own
   confirmation route naming the order, the titles and the total.
2. The order's invoice must exist as a real record in `killbill`, on that
   member's billing account, for exactly the computed total in that currency.
   The app's own tables can only reflect what lives there; they never substitute
   for it.
3. `killbill` is Kill Bill 0.24.21 at `PAYMENTS_API_URL`. It is a billing
   platform: it holds accounts, catalog plans and invoices. It has no charge
   object, no card token and no decline code. Every call under `/1.0/kb/` carries
   HTTP Basic `admin` and `password`, the header `X-Killbill-ApiKey` set to
   `orbit-labs` and the header `X-Killbill-ApiSecret` set to
   `orbit-labs-secret-9f14c73e`, read from `PAYMENTS_ADMIN_USER`,
   `PAYMENTS_ADMIN_PASSWORD`, `PAYMENTS_API_KEY` and `PAYMENTS_API_SECRET`.
   Writes also carry `X-Killbill-CreatedBy`. The surface available is
   `GET /1.0/healthcheck` for liveness,
   `GET /1.0/kb/accounts?externalKey=<key>`, `POST /1.0/kb/accounts` with a body
   of `name`, `externalKey`, `email`, `currency` and `country`,
   `GET /1.0/kb/accounts/pagination`, `GET /1.0/kb/catalog/availableBasePlans`
   and `GET /1.0/kb/invoices/pagination`. `GET /1.0/kb/healthcheck` sits behind
   the tenant filter and never answers; do not use it as a probe.
4. An `externalKey` is unique within the tenant, so the store itself refuses a
   second account for one member. A member has exactly one billing account
   however many times their signup is submitted.
5. Kill Bill reports an invoice `amount` as a decimal such as `39.97` and its
   `currency` in upper case. A `US` three-book order therefore appears there as
   `39.97` and `USD`; the app's own order row holds `3997` and `usd`.
6. A failed order leaves nothing behind: no box moved to `placed`, no order row,
   no credit spent and no invoice.

### The confirmation email

1. Placing a box sends one email over SMTP at `SMTP_HOST` and `SMTP_PORT` to the
   member who placed it, with no cc and no bcc.
2. Its subject begins with `Box confirmed: ` followed by a space and the cycle's
   label, for example `Box confirmed: September 2026`.
3. Its body is not empty and names every title in the box and the total that was
   charged.
4. Nothing else in the box's life sends an email. Adding an edition, removing
   one, applying a credit, entering a code and having a box refused all send
   nothing. Only a box that becomes `placed` sends.

### Gift subscriptions

1. A gift is a subscription the recipient controls, not a box the giver
   assembles. Buying one on `/gifting` issues an e-gift card to the buyer
   immediately, with a code shown on screen and emailed to them. The subject
   begins with `Your e-gift card: ` followed by a space and the code, for example
   `Your e-gift card: PANGOLIN-GIFT-7K42`, and the body names the code.
2. The gift is transferable: it is the code that carries the value, and whoever
   holds it may redeem it.
3. A gift creates a membership only when it is redeemed, at `/redeem`. Until
   then no membership exists for the recipient.
4. The buyer never sees what the recipient chooses. A request from the buyer's
   session for the recipient's box, order or credit ledger is denied and the row
   is unchanged. This is the promise the gifting page makes when it says
   `No spying on shelves needed.`
5. A code is redeemed at most once. A second redemption is refused and creates no
   second membership.
6. A member may not redeem a code they bought themselves.
7. When a gift is redeemed by somebody who is already a member, the existing
   membership is extended. A second subscription is never created for one
   account.

### The annual vote

1. The vote is annual and member-only, and it produces exactly one winner.
2. One ballot per member per round. A second ballot in the same round is refused
   and the first is unchanged.
3. A round has an open and a close, and `/vote` states
   `Voting closes <date>. One vote each.`
4. A winner becomes a new orderable edition, not a flag on the original.
   `Saltmarsh` and `The Paper Wife` are the two past winners and each carries an
   author portrait, which no other edition does.
5. The forthcoming round is shown as a placeholder in the same row as the
   winners, so the timeline shows its own future.

### Addresses and special shipping

1. Three destinations the ordinary flow cannot serve are recognised at address
   entry and named as what they are: Puerto Rico, an APO or FPO address, and a PO
   box. The member is told `We ship there, but we'll need to set it up by hand.
   Email support@example.com.` and routed to support from there.
2. An address the club cannot serve is identified before the member reaches
   payment, never after.

### The exclusive title

`The Pangolin Anthology` is published by the club itself: an original anthology
by authors previously featured, tagged `Pangolin Original` and `Horror`. It is
the one product whose availability the club fully controls, and the claim that it
is available nowhere else must remain true of it.

### The supporting surfaces

1. `/faq` carries every question; the home page surfaces three of them and links
   to the rest. Each question is a panel in one of six hues.
2. `/gifting` carries the gifting copy: `A gift outside of the box`, and
   `Gift a subscription and they can pick their own books. No spying on shelves
   needed. Order today and instantly receive an e-gift card to print out or
   forward. If you're lucky, they might let you borrow a copy.`
3. A privacy page at `/privacy-policy`, linked from the footer of every page, states
   what the club records about a member: their email, their country, the boxes
   they have built, the orders they have placed, their credit ledger and their
   ballots, and how long each is kept.
4. The footer carries a mailing-list form headed `Join our mailing list` with an
   `Email Address` field and a `Subscribe` control. Both of its result states
   exist before they are needed: `Thank you, you joined us!` on success and
   `Oops! Something went wrong while submitting the form.` on failure. It also
   carries both application-store buttons, two social links, the two legal links
   to `/terms-of-service` and `/privacy-policy`, the credit line
   `(C)2026 Pangolin Books. All rights reserved.`, and the line naming the
   designer and the development studio credited with the work:
   `Design by Rill Studio` and `Development by Nine Yards`.
5. The join band recurs down the home page between sections, reading
   `Want to join the Club?` and `Sign-up now!`. It is one component placed by the
   content model, never several copies with the same words.
6. A first-time visitor is asked once whether non-essential cookies are allowed.
   The answer is remembered and survives a reload: a visitor who has answered is
   never asked again in the same browser.
7. Every form in the product rejects invalid input before it writes anything. The
   message names the field it is about and appears beside it, and the record that
   was being created does not exist afterwards. This holds for signup, sign-in,
   the mailing list, the address form, the gift purchase and the promotional
   code.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The home page: the month's reveal, how it works, three questions, the join band, the footer | Public |
| `/allbooks` | The full catalogue, filtered by genre | Public |
| `/books/<slug>` | One edition | Public |
| `/gifting` | Buy a gift subscription | Public |
| `/faq` | Every question | Public |
| `/privacy-policy` | What the club records | Public |
| `/terms-of-service` | The terms of membership | Public |
| `/signup` | Create a membership | Public |
| `/login` | Sign in | Public |
| `/redeem` | Redeem a gift code | Public |
| `/box` | The box builder: the catalogue beside the box | Member |
| `/box/placed/<order_id>` | The confirmation | Member |
| `/account` | Subscription, credit balance and ledger, past orders | Member |
| `/vote` | The open ballot and the past winners | Member |

**Entry and redirects.** An unauthenticated visitor who opens `/box`,
`/account` or `/vote` is sent to `/login` with their destination preserved and
arrives on it after signing in. Signing in with no destination lands on `/box`.
Signing out returns to `/`. A token that expires mid-action returns the member to
`/login` with the destination preserved, and the box they were building is still
there when they return. A member who opens another member's confirmation route is
denied, not redirected to their own.

**Journeys.**

1. **Build and place a box.** Sign in as `member@example.com` with
   `deku-demo-pw-2026`. Land on `/box`, where the current cycle's editions sit
   beside the box. Add `The Orrery Thief` from its own row without leaving the
   page; it appears in the box and the total reads `1799`. Add `Salt and Static`;
   the total reads `2898`. Add `A Quiet Inventory`; the total reads `3997`. Place
   the box. The confirmation route names the order, the three titles and `3997`,
   an invoice for `39.97` in `USD` exists on that member's billing account, and
   one email whose subject begins `Box confirmed: ` arrives for
   `member@example.com` alone.
2. **A box that is not valid yet.** Sign in as `member2@example.com`. Add
   `The Glass Cartographer` and `Salt and Static (Reprint)`. Both go into the
   box and neither control is disabled. Placing it is refused, the box is
   unchanged, and the page states `Add at least one book from this month to
   complete your box.` Add `Every Third Tuesday` and the box places.
3. **The limit.** With `The Orrery Thief`, `Salt and Static` and
   `Nine Yards of Night` in the box, adding `Every Third Tuesday` is refused, the
   box still holds three, and the page states `Three books is the limit. Remove
   one to add another.`
4. **A pre-seeded link.** Open `/box?ids=the-orrery-thief,salt-and-static,every-third-tuesday,a-quiet-inventory`.
   Three survive in order, the fourth is dropped, the member is told, and the box
   is valid.
5. **Gift and redeem.** As `member@example.com`, buy a gift on `/gifting` for
   `reader@example.com`. A code appears on screen and one email whose subject
   begins `Your e-gift card: ` arrives for `member@example.com`. Sign out, sign
   up as `reader@example.com`, redeem the code at `/redeem`, and the membership
   starts. Back as `member@example.com`, a request for the recipient's box is
   denied.
6. **Vote.** Sign in as `member3@example.com`, open `/vote`, cast a ballot for
   `A Quiet Inventory`. A second ballot in the same round is refused and the
   first stands.

**States.** Every list has an empty state: `/allbooks` filtered to a genre with
no editions names the filter, `/box` with nothing in it shows the rule, and
`/account` with no orders says so. Every page has a loading state and never
renders as a bare white page. A rejected action leaves the page standing and
states its reason; nothing crashes the app.

## UI/UX notes

The north star: a visitor should understand in the first moment that this club
lets them choose, and that choosing is the fun part. The register is consumer
retail, warm and playful, with the books themselves seen first. Pages are white
with candy accents: this is not a dark design and not a neutral one, and a build
that reaches for a quiet operational grey has built a different product.

**Palette by role.** The page ground is white throughout. The brand carries three
marks: a light, vivid violet, a mid, vivid teal and a black, and those three are
the brand and appear nowhere else as ordinary decoration. The buttons are
deliberately not the brand colours: the primary fill is a light, soft amber, the
alternate fill is a mid, vivid magenta, and the social fill is black. Beyond
white, the surfaces that carry the most of the product are a pale pink panel, a
deep indigo for text that must be read at length, a hot magenta for the action
that matters most on a page, and a peach for the second surface. The primary
action wears the amber and nothing else on a page wears it. Failure, success and
in-progress each carry their own distinct meaning colour, and none of them is a
brand mark. The exact shades are yours, so long as each role above is filled by
one colour and no two roles share one.

**The FAQ palette is paired, and the pairing is the point.** Six hues named
Cyan, Green, Orange, Periwinkle, Pink and Yellow, each with a solid and a soft
twin. Cyan is a near-white, soft teal against a near-white cool neutral.
Green is a light, soft green against a near-white, muted green.
Orange is a light, vivid orange against a near-white, soft orange.
Periwinkle is a near-white, muted indigo against a near-white cool neutral.
Pink is a near-white, muted violet against a near-white neutral.
Yellow is a light, vivid amber against a light, soft amber.
The solid closes the panel and the soft twin opens it,
so a question keeps its identity and changes only its weight.
Twelve values for one component is deliberate.

**Typography.** Three font families, three jobs. `Recoleta` at weight 700 for headings.
`Public Sans` at weights 500, 600 and 700 for everything that is read. `Caveat`
at weight 400 as a handwritten accent, with its own two sizes, `2em` and `2.5em`,
used on nothing else. A handwritten face with its own scale is a deliberate
voice and is part of the product's warmth. Content type is fluid: it grows and
shrinks with the window between a minimum and a maximum. Interface labels do not
scale; they hold at `12px` at weight 600. Figures align wherever amounts stack.

**Shape, and the corner radius that carries it.** The primary button is a
full pill. The alternate button has a small radius and is barely rounded. Two shapes
carrying two different jobs, and a third variant is added by publishing a set of
tokens rather than by writing new rules: a button variant is a token set, not a
colour override.

**Global chrome.** Three things are global and appear on every route: the
floating header, the recurring join band between sections, and the footer.

**Density is spacious.** Pages breathe and the book is the subject. This is not a
dense console, and nothing is packed to fit more of it on one screen.

**Layout.** A floating pill group sits over the content at the top: four
navigation pills, then the sign-in control as a wider pill with a circular arrow
appended. A second circular arrow pair sits at the right to drive the home
carousel. The box builder puts the
catalogue on one side and the box on the other, both visible at once,
and a book is added from its own row without leaving
the page. Placing a box lands on its own confirmation route rather than a panel
over the builder.

**The card.** A rounded card, the cover inset at the top, a ribbon over its
corner where the edition carries one, then the tags as coloured pills, then the
name in the display face, then the description truncated with an ellipsis, then
`Read more`. Its background colour is drawn from its own cover rather than
chosen: every card sits on a colour that matches its cover, which is why the row
reads as a shelf rather than a spreadsheet. Carousel cards sit at slightly
different vertical offsets so the row reads as scattered rather than aligned.

**Motion character: springy.** Movement overshoots and settles visibly. The
product publishes a vocabulary of easings rather than one curve: a smooth
easing, a click easing, three overshoots at three strengths, and one true spring
that overshoots and settles through two visible rebounds. Every button variant
publishes its own easing set alongside its click scale, focus inset, height and
padding, and a pressed button squashes more than it narrows, the way a physical
button does. The mascot's ears twitch behind every primary and alternate button,
and again on the subscription box: two separately animated ears, the right
travelling about four times as far as the left and starting slightly earlier, on
two different clocks, with the button ears slower than the box ears. Mirroring
one ear to make the other, or running both on one clock, produces a mechanical
twitch instead of a living one. Page changes move content
upward in both directions: arriving content rises from below and leaving content rises away
above, with a scale-and-rotate whose direction follows the navigation. An
arriving element is solid for most of its travel and a leaving one is gone before
it stops. Transitions are declared per property and named; a blanket rule
animating everything is a defect, not a shortcut.

**Reduced motion is guarded by three questions at once**, and this is the part to
get right: before a hover effect plays, the product asks whether there is a
pointer, whether it is a precise one, and whether the visitor has asked for less
animation. Under reduced motion the ears hold still, page transitions become a
plain cross-fade, and the scroll-driven sequence holds one frame. The fade is
preserved rather than removed: reduced motion means less movement, not a bare
change of state. That scroll-driven sequence is a scrubbed video the browser
decodes natively, never a run of a hundred and twenty still frames requested one
by one; it loads nothing until it is near the viewport and holds its first frame
as a poster until it does.

**Responsive behaviour** holds at four widths and at every width between them.
The header is a four-item pill group when there is room, collapses as the window
narrows, and becomes the mark plus a `Menu` control at the narrowest. The book
carousel is horizontal with arrows at the two wider widths and swipes at the
narrowest. Card offsets are staggered vertically when wide, reduced in the
middle, and aligned at the narrowest. The step illustrations run four across,
then two, then stacked. At a narrow viewport nothing overflows sideways and every
navigation target stays reachable. One boundary is written once in one syntax:
the same width is never expressed two ways, one modern media-query form is used
throughout rather than mixed with an older one, and no rule overlaps another by a
hair.

**Accessibility floors**, which are contract rather than taste: contrast meeting
WCAG AA, comfortably sized touch targets, full keyboard navigation with visible
focus rings, labels on icon-only controls, and meaning never carried by colour
alone. The carousel is operable three ways, by pointer drag, by its arrow
controls and by the keyboard, each card reachable in order; its arrows disable at
the ends rather than vanishing; a card is one link rather than a card containing
one, so the whole card is the target and is announced once; and the position in
the row is announced, because a scrolling row that does not say how many items it
holds is unusable without sight. A tag's colour carries no meaning and must not:
`Fantasy` and `Includes a Dog` differ in kind and never in treatment, and the
text on the pale soft variants is dark enough to meet the contrast bar. The
looping ear animations stop under reduced motion. The scroll sequence carries a
text alternative and is never the only way any information is presented.

What this must not look like: a page dominated by one hue family with no second
signal, decoration standing in for content, or a marketing composition where the
working box builder belongs.

## Technical requirements

The app is server-rendered. Django produces complete HTML for every route, so the
browser receives a finished page on first paint rather than an empty shell it
must fill; Alpine.js layers the interactive behaviour onto that markup - the box
panel, the carousel, the accordion and the cookie choice - rather than replacing
it. The datastore is PostgreSQL at `DATABASE_URL`. Billing is `killbill` at
`PAYMENTS_API_URL` with `PAYMENTS_API_KEY`, `PAYMENTS_API_SECRET`,
`PAYMENTS_ADMIN_USER` and `PAYMENTS_ADMIN_PASSWORD`. Mail goes over SMTP to
`mailpit` at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`.
Authentication is email and password implemented by the app, with bearer tokens
on the JSON API. `GET /api/health` returns `200` once the app is ready. Request
lines go to standard output.

Use only the libraries named here plus their direct dependencies. Do not
introduce a second database, cache, queue, object store, identity provider or
mail vendor - the only backing services available in this environment are
`postgres`, `killbill` and `mailpit`, and reaching for anything else is a
contract violation.

Read every host, port and credential from the environment. Never hardcode one.

The composition rule is settled by the server. Whatever the browser shows, a box
is accepted or refused by the application, and a request that bypasses the
interface entirely gets the same answer.

Every public route carries its own social preview: a preview title declared in
the document head as `og:title` and a preview image declared there as `og:image`,
with that preview image resolving to real bytes the product serves. No two public
routes declare the same preview title.

## Data model

Eighteen tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a secret. Hash it as normal; the exact literal must work at
login, and it must be written into `/app/USER_README.md` alongside each account
so a grader can sign in.

**`members`** - `id`, `email` unique, `password_hash`, `country` which is `US` or
`CA`, `created_at`. A member's credit balance is derived from `credit_ledger`
rather than stored beside them.

**`subscriptions`** - `id`, `member_id`, `state` which is `active`, `paused` or
`canceled`, `started_at`, `ends_at`, `billing_external_key` unique. A failed
payment moves a subscription to `paused` and says so; it never deletes the
account. Cancelling sets `ends_at` to the close of the paid cycle, and the state
becomes `canceled` at that instant, not before.

**`cycles`** - `id`, `label`, `opens_at`, `closes_at`. Exactly one cycle is
current at any instant, and the cycle a box belongs to is the one current when
the box was created.

**`works`** - `id`, `title`, `author_name`.

**`editions`** - `id`, `slug` unique, `work_id`, `title`, `description`,
`cover_hue`, `publisher`, `special_edition`, `availability`, `cycle_id` which may
be empty, `author_portrait_url` which may be empty. An edition belongs to at most
one cycle. `cover_hue` is derived from the cover when the edition is created and
stored, so every response for one edition carries the same value; it is not
recomputed for each render. `author_portrait_url` is set only on a vote-winner
edition.

**`tags`** - `id`, `name` unique, `kind`. **`edition_tags`** - `edition_id`,
`tag_id`. A tag's `kind` exists for filtering and never changes how the tag
renders.

**`boxes`** - `id`, `member_id`, `cycle_id`, `state` which is `building`,
`placed` or `shipped`, `placed_at`, `base_minor`, `extra_minor`, `currency`. A
member has at most one box in `building` per cycle. `base_minor` and
`extra_minor` are written when the box is placed and are what its total was
computed from, so a later pricing change cannot move an agreed total.

**`box_items`** - `id`, `box_id`, `edition_id`, `position`. At most three rows
per box, and one edition never appears twice in one box.

**`orders`** - `id`, `box_id`, `member_id`, `total_minor`, `currency`,
`promotion_code`, `credits_applied`, `invoice_external_key` unique, `placed_at`.
One box produces at most one order, however many times it is submitted.

**`credit_ledger`** - `id`, `member_id`, `delta`, `reason`, `cycle_id`,
`order_id`, `created_at`. `reason` is `postcard_challenge`, `unchosen_cycle` or
`spent_on_order`. A member's balance is the sum of their deltas and is never
negative. At most one `unchosen_cycle` entry exists per member per cycle.

**`gifts`** - `id`, `code` unique, `purchaser_member_id`, `recipient_email`,
`value_minor`, `currency`, `redeemed_by_member_id`, `redeemed_at`. A code is
redeemed at most once, and never by its purchaser.

**`promotions`** - `code` unique, `country`, `first_order_only`, `base_minor`,
`expires_at`.

**`country_pricing`** - `country` unique, `currency`, `base_minor`,
`extra_minor`. This is the only place a price lives; every total is computed from
it.

**`vote_rounds`** - `id`, `year` unique, `opens_at`, `closes_at`,
`winner_edition_id`. **`ballots`** - `id`, `round_id`, `member_id`,
`edition_id`, `cast_at`. A member has at most one ballot per round. Two ballots
submitted at the same instant by one member for one round: exactly one is
accepted and the other is rejected.

**`faq_entries`** - `id`, `question`, `answer`, `hue`, `position`.
**`press_mentions`** - `id`, `outlet`, `url`.

**Concurrency invariants**, stated as properties of the running system. Two
simultaneous attempts to place the same box must not both produce an order:
exactly one wins, the other is rejected, and exactly one invoice exists
afterwards. Two simultaneous attempts to add a fourth edition to a box already
holding three must both be refused, and the box must still hold three. Two
simultaneous redemptions of one gift code must not both succeed. A member's
credit balance never goes negative under any interleaving of spends.

**Seed data.** Seeding is idempotent: restarting the app must not duplicate rows.

Three members, each with an active subscription and the password
`deku-demo-pw-2026`: `member@example.com` in `US` with no credits,
`member2@example.com` in `CA` with one credit from a `postcard_challenge`, and
`member3@example.com` in `US` with one credit from an `unchosen_cycle` for the
previous cycle.

Two cycles: the current cycle is the UTC calendar month in which the app first
starts, and the previous cycle is the month before it, closed.

Thirteen editions:

| Slug | Title | Cycle | Tags |
|---|---|---|---|
| `the-lamplighters-daughter` | The Lamplighter's Daughter | current | Historical, Award Worthy |
| `salt-and-static` | Salt and Static | current | Horror, Includes a Cat |
| `nine-yards-of-night` | Nine Yards of Night | current | Thriller |
| `the-orrery-thief` | The Orrery Thief | current | Fantasy, Includes a Dog |
| `a-quiet-inventory` | A Quiet Inventory | current | Literary, LGBTQIA+ |
| `the-marmalade-conspiracy` | The Marmalade Conspiracy | current | Satire, Includes a Cat |
| `every-third-tuesday` | Every Third Tuesday | current | Romance |
| `the-glass-cartographer` | The Glass Cartographer | previous | Mystery |
| `feral-arithmetic` | Feral Arithmetic | previous | Horror, LGBTQIA+ |
| `salt-and-static-reprint` | Salt and Static (Reprint) | none | Horror, Includes a Cat |
| `saltmarsh-2024-members-choice-winner` | Saltmarsh | none | Literary, Award Worthy |
| `the-paper-wife-2025-members-choice-winner` | The Paper Wife | none | Historical, Award Worthy |
| `the-pangolin-anthology` | The Pangolin Anthology | none | Pangolin Original, Horror |

`salt-and-static` and `salt-and-static-reprint` share one `works` row and are two
`editions` rows. The two winners carry an author portrait; no other edition does.
`the-pangolin-anthology` carries the club itself as its `publisher`.

The thirteen tags are seeded by name and kind. Country pricing is seeded as `US`
with `usd`, `1799` and `1099`, and `CA` with `cad`, `2599` and `1599`. One
promotion is seeded: `SUMMER`, country `US`, first order only, base `400`,
expiring at the close of the current cycle. One unredeemed gift is seeded with
the code `PANGOLIN-GIFT-7K42`, purchased by `member@example.com`. Three vote
rounds are seeded: `2024` won by `saltmarsh-2024-members-choice-winner`, `2025`
won by `the-paper-wife-2025-members-choice-winner`, and one open round for the
current UTC year which opens at first start and closes sixty days later. Six FAQ
entries are seeded, one per hue, in order. Four press mentions are seeded.

## Constraints

- One membership tier. No plan table, no annual tier, no pause-and-skip tier.
- Two countries only, `US` and `CA`. No other country may be selected at signup.
- Web only. There is no native mobile application and no application-store build,
  although the footer carries their buttons as the reference does.
- One origin. The marketing pages and the box builder are served by the same
  application.
- No comments, no likes, no messaging, no member profiles, no reviews, no
  ratings, no reading progress.
- No shipping integration, no carrier, no parcel tracking beyond the `shipped`
  box state.
- No refunds, no payment methods and no chargebacks as member-facing flows.
- No real book titles, authors, imprints or press outlets. Every name in this
  brief is invented and must stay invented.
- No external network calls at run time beyond the three named backing services.
- No search engine, no recommendation engine, no personalisation.
- The app must stay responsive with a few thousand editions, a few thousand
  members and tens of thousands of ledger entries.

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
- Serve a production build behind a static or preview server - never a dev
  server.
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
| `POST /api/auth/signup` | `email`, `password`, `country` | the member and a bearer token |
| `POST /api/auth/login` | `email`, `password` | the member and a bearer token |
| `GET /api/health` | none | a health object |
| `GET /api/cycles/current` | none | `label`, `opens_at`, `closes_at`, `editions` |
| `GET /api/editions` | optional `genre` | a top-level JSON array of editions |
| `GET /api/editions/<slug>` | none | one edition with its tags |
| `GET /api/box` | optional `ids` | the member's box for the current cycle, its items, its running total and its validity with a reason |
| `POST /api/box/items` | `slug` | the updated box |
| `DELETE /api/box/items/<slug>` | none | the updated box |
| `POST /api/box/place` | optional `promotion_code`, optional `use_credits` | the order |
| `GET /api/orders` | none | a top-level JSON array of the member's own orders |
| `GET /api/credits` | none | the balance and a top-level JSON array of ledger entries |
| `POST /api/gifts` | `recipient_email` | the gift with its `code` |
| `POST /api/gifts/redeem` | `code` | the membership |
| `GET /api/vote` | none | the open round, the member's ballot if any, and the past winners |
| `POST /api/vote` | `slug` | the ballot |
| `POST /api/addresses/check` | `line1`, `city`, `region`, `postal_code`, `country` | whether the address is servable and, if not, which of the three kinds it is |
| `POST /api/account/cancel` | none | the subscription with the cycle close it now ends at |

Field names are exact. A successful call returns the named resource or shape. An
invalid or unauthorized call is rejected as a client error, never a `5xx` and
never a silent success, and carries a reason. Bearer auth is required on
everything except `POST /api/auth/signup`, `POST /api/auth/login` and
`GET /api/health`.

**No mocks.** An in-memory list of invoices, a hardcoded response the app returns
to itself, an order row written with an invoice reference that names nothing, a
mail log on the app's own disk instead of a message sent over SMTP, a stubbed
`killbill` client that answers its own calls: each is a contract violation
however good the interface looks. The named provider is the fact - the app's UI
and its own tables can only reflect what lives in `killbill` and in `mailpit`,
never substitute for it.

## Definition of done

A member can sign in, build a box of up to three books with at least one from the
month that is current, and place it: the order appears with the right total, an
invoice for that total exists on their billing account, and a confirmation email
reaches them and nobody else. A box that breaks the rule is refused and says
which rule, while every book stays addable. A gift bought by one member creates a
membership only when its code is redeemed, and the buyer never sees what the
recipient chose.
