# Vesperi Spirits: The Nocturne Experience

Build and deploy a working web application from this brief. There is no starting codebase. When
you are done, a stranger must be able to open the app in a browser, confirm they are of legal age,
drive a hooded figure through an engraved, woodcut-style film with their own wheel or finger, hold
and drag to open the portal, hold to pour one of three flavours, reach the collection where every
bottle shows its tasting notes, its strength and its volume, and then keep a bottle on their own
shelf, ask to be told when it lands at a bar near them, and book a seat at a tasting, without
hitting an error page. The hard part is that the finite things are real: two visitors claiming the
last bottle of a release at the same moment must end with exactly one hold and one place in the
queue, a tasting's held and booked seats must never exceed its capacity however many requests
arrive together, and a confirmation must exist as a real message in Mailpit rather than as a green
tick the app shows itself. None of that can be arranged in the browser alone.

## Overview

Vesperi Spirits is a late-night cream liqueur house. Its range, the Nocturne Collection, is three
flavours of one bottle: `MARSHMALLOW COFFEE & CREAM`, `ORANGE CHOCOLATE & CREAM` and
`MINT CHOCOLATE & CREAM`, each `13% ABV` in a `700 ML` bottle. The house does not publish the range
as a product grid. It publishes it as a film the visitor drives: one page, one continuous rendered
scene filling the whole window, eighteen chapters long, advanced by the wheel, a trackpad, a touch
drag or the keyboard, while the ordinary document underneath never scrolls. A visitor who arrives
from social or from a search confirms their age, spends roughly two minutes walking a hooded
figure, the Saint, across an empty plain, up a stair to a monolith, through a portal their own held
drag opens, into a red temple, past an altar carrying three bottles, through a pour they perform
themselves, an ascent, the collapse of the temple and out into a bright colonnade that resolves into
the collection: the promise line, a poster, a carousel of the three bottles with their tasting
notes, the data strip, and the footer.

Everything is drawn as a woodcut. Every surface, figure, column and cloud carries engraved parallel
lines that stay stuck to the surface as it moves, so each frame reads as a printed plate that
happens to move. The palette is ink, paper and one saturated red, with the three flavour tints as
the only other colours in the film. The bottle and the cocktail glass are the only two objects drawn
realistically, so the product reads as something you could pick up inside a world that is plainly a
drawing.

The house's earlier site ended on a dead end: a line saying no house stocks it yet,
with nothing to buy, nothing to keep and no way to be told when that changes. Vesperi closes that
gap with four additions reachable only from the last quarter of the film, where the visitor already
has a reason to care, and none of which interrupts the film:

- **The Cellar**: a signed-in visitor keeps a shelf of bottles and can hold one numbered allocation
  of a limited release for seventy-two hours, joining a ranked waitlist when the release is gone.
- **Where to drink it**: venues near the visitor with what each has in right now, gated by what the
  region allows, plus a standing alert for an area that has nothing yet.
- **Tastings**: a booking flow for hosted tastings at those venues, with seats held for fifteen
  minutes, a capacity that is never exceeded and a forty-eight-hour cancellation window.
- **The Ritual**: a visitor builds a serve from one bottle plus mixers, ice and a garnish, pours it
  with the same held gesture as the film, names it and shares a short link that pours it again for
  whoever opens it.

The people who use it are visitors of legal drinking age and the hosts who run the stocking venues.
A host keeps their own venue's stock readings current and can cancel their own venue's tastings.

What it deliberately is not. It is not a shop: there is no cart, no checkout and no payment of any
kind. It is not a map service: venue search runs over a fixed set of places this product knows. It
does not track visitors for anyone else: there is no third-party analytics and no advertising. It
ships no image, model, font atlas or sound file: every picture and every sound is generated as it
runs. It is not a native application.

The genuinely hard part is that a two-minute, fully reversible, hand-driven film and a set of
finite, contended, time-limited reservations have to live in one product without either weakening
the other.

## User roles

Two roles. Signup is open: anybody can open a `visitor` account by asking for a sign-in link.

| Role | Can do |
|---|---|
| anonymous | Watch and drive the whole film, read the collection, the still page, the terms page, venues, regions, tastings, the ingredient sets and any shared ritual; record a cookie choice; ask for a sign-in link. **Cannot hold a bottle, set an alert, hold seats, book, join a waitlist or save a ritual.** |
| `visitor` | Everything anonymous can, plus: keep and release bottles on their own shelf, hold, confirm, accept and decline allocations, set and cancel their own landing alerts, hold seats, book, cancel and reschedule their own bookings, join a tasting waitlist, and save, edit and delete their own rituals. **Cannot read or change another visitor's shelf, alerts, holds, bookings or ritual ownership. Cannot change any venue's stock reading. Cannot cancel a tasting session.** |
| `host` | Everything anonymous can, plus: change the stock readings of the one venue they belong to, and cancel that venue's tasting sessions. **Cannot change another venue's readings or cancel another venue's sessions. Holds no visitor capability: cannot keep a bottle, hold seats, book or save a ritual.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is
not authorization: a direct API call from a `visitor` session to any `host`-only endpoint must be
rejected by the server (an unauthorized request is denied, not served), leaving the protected state
unchanged.

Two rules cut across the table and are not role checks:

- **Scope by relationship, not only by role.** A host acts only on the venue their account belongs
  to. The identical call against a different venue is denied and that venue's readings and sessions
  do not change.
- **A visitor's things are theirs.** An allocation, alert, seat hold, booking or ritual belonging to
  another visitor cannot be confirmed, released, accepted, declined, cancelled, rescheduled, edited
  or deleted by anyone else. Such a call is denied or answered as not found, and the row does not
  change.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | Detail |
|---|---|---|
| `visitor@example.com` | `visitor` | Ada Vale. An empty shelf, no alerts, no bookings |
| `visitor2@example.com` | `visitor` | Bram Okafor. One confirmed bottle, a full tasting booking, one shared ritual |
| `host@example.com` | `host` | Ines Marlow, host of `The Gilded Nave` |
| `host2@example.com` | `host` | Tomas Reyes, host of `Salt & Vesper` |

## Core features

### Auth

1. Seeded accounts sign in with a password. `POST /api/auth/login` takes `{"email", "password"}`
   and on success returns `{"access_token", "expiresAt", "user"}`. The client sends that token as a
   bearer token on every other call. A wrong password, or an address with no password, is denied with the reason `invalid_credentials`, and the refusal does not say which half was wrong or whether the address exists.
2. Everyone can sign in without a password. `POST /api/v1/auth/link` takes `{"email", "returnTo"}`
   and always answers `202`, whether or not an account exists, and sends one message to that
   address over SMTP through Mailpit. The message subject is exactly `Your Vesperi sign-in link`,
   it is addressed to that address only, with no cc and no bcc, and the first line of its body reads
   `Sign-in code: ` followed by the code, with the second line carrying the link
   `/sign-in/verify?token=` plus the code on the app's public address. The code is at least 24
   characters from letters, digits, hyphen and underscore.
3. `POST /api/v1/auth/session` takes `{"token"}` and exchanges a code for a session, returning
   `{"session", "expiresAt", "user"}`, where `session` is the bearer token. A code is valid for ten
   minutes and works once: a second exchange of the same code is denied with the reason `invalid_token` and creates no session. An
   unknown or expired code is denied with the reason `invalid_token`.
4. Signup is the first exchange. An address with no account becomes a `visitor` account the first
   time its code is exchanged. No account is ever created by merely asking for a link. An account
   opened this way has no password, and no password is ever stored for it.
5. `GET /api/v1/me` returns `{"id", "email", "role", "displayName", "venueId"}` for the bearer's
   account. A request with no token, an unknown token, a malformed token or a token after sign-out
   is denied. `POST /api/auth/logout` ends the session; the same token is denied afterwards.
6. Sessions last 14 days from creation. Every request resolves the role and, for a host, the venue,
   from the token on the server, never from anything the client sends.
7. A visitor who is signed out and presses a control that needs an account (keep, alert, hold
   seats, book, join a waitlist, save a ritual) is taken through sign-in and returned to the same
   place with the action completed: the same flavour in the carousel with the hold placed, the same
   venue with the alert set, the same session with the seats held, the same build with the ritual
   saved. The visitor does not lose their position in the story.

### The experience

8. The whole film lives on `/`. The document never scrolls at any window size: the page is exactly
   one window tall, and every wheel, trackpad, touch and key input that would scroll is captured,
   cancelled and turned into a single story position that runs from the first frame of the first
   chapter to the last frame of the footer. That position is the only thing the film reads.
9. The story position is continuous, reversible, damped and clamped. Every chapter positions
   everything it draws from the position alone and holds no playback state of its own. Driving the
   position backwards returns every chapter to exactly the frame it showed on the way forward. A
   flick keeps travelling and slows to a stop; a held, slow gesture tracks the hand one to one;
   stopping the input stops the picture within one frame. The position cannot go below the first
   frame or past the footer, and there is no rubber band at either end.
10. A full pass from the first frame to the footer takes roughly two minutes of steady scrolling on
    a trackpad. The eighteen chapters do not divide it evenly.
11. Inputs: the wheel and trackpad drive the position; a vertical touch drag drives it with momentum
    on release; the arrow and page keys step it; `Home` and `End` jump to either end. The input is
    counted as idle a short moment after the last meaningful movement, and idleness changes what the
    sound does and lets the figures breathe.
12. The eighteen chapters, in this fixed order, are: `wander`, `profile`, `approach`, `near`,
    `hand`, `target`, `transition`, `cathedral`, `drink-selection`, `drink-pour`, `anti-gravity`,
    `pillar-crumble`, `colosseum`, `taste`, `collection`, `products`, `retail`, `footer`. All
    eighteen are prepared from the start and stay ready for the whole visit, so moving between two
    chapters is a blend of their contributions, never a cut and never a pop-in.
13. The story, beat by beat: the title lockup `THE NOCTURNE EXPERIENCE` over broad grey brush
    strokes on ink with a pool of white rising from the bottom edge; the hooded figure walking left
    to right through mist on paper, told in three comic panels, one a close-up of the face; the
    monolith, with a hatched moon, a long stair and a dark red disc at the foot of a tall slab; the
    portal filling the frame, a deep red disc of concentric engraved rings with the figure small at
    its centre and hatched walls converging behind; a life-size hand reaching in from the right
    across a red hatched field; full-frame vertical hatching over dark domed silhouettes as the
    story passes inside; the temple interior with two rows of red columns, a wide screen high on the
    far wall carrying a pair of engraved eyes, and an altar at the base carrying three bottles; the
    figure beside a stone pedestal with the three bottles on it; the pour, liquid falling from a
    tilted bottle into a coupe glass; two stacked panels, the upper showing the figure's robe now
    saturated with the flavour colour and the lower a very wide close-up of the eyes; the figure
    lifting off the floor; the columns fracturing against flat red with debris and an inset panel
    of the figure in profile; the colonnade in paper white with deep rows of columns and red
    doorways beyond, the figure walking away in a flavour-coloured robe; then the collection act and
    the footer.
14. The header pill's two controls move the story: `EXPERIENCE` returns the position to the start of
    `wander` and `COLLECTION` moves it to the start of `products`. They are fragment destinations,
    `#experience` and `#collection`, and never load another document. The move is animated rather
    than a jump, the wheel interrupts it at any point, and passing a held gesture on the way does not
    stop the move: the gesture is marked satisfied because the visitor chose to skip it.
15. Reverse travel all the way to the start returns the first frame, the header state, the ground
    colour and the sound mix to exactly how they were. The age confirmation is not shown again on
    reverse travel. There is no replay control.

### Gates before the story

16. Before anything else on `/`, the app checks that the browser can draw the film: an accelerated
    drawing context exists and the engraved material compiles. A browser that fails is sent to
    `/unsupported`, which shows the house mark centred on ink with the line
    `Your browser is not supported` beneath it in the display face, and a link to the still page.
    `/?mode=still` skips the check deliberately and renders the still page in place of the film.
17. On a handset held upright, a panel reading `Please rotate your device.` covers everything,
    including the age panel, and the story does not move until the handset is turned. Each of the
    four words is its own element, and the whole line is also present once as continuous hidden text for a screen reader. The panel is part of every film page's HTML at every size and is shown only on an upright handset.
18. While the first chapter is being prepared, a small drawn loader shows real progress, never a
    timed fake. It does not dismiss until the first chapter can be driven backwards and forwards
    without stalling; later chapters keep preparing behind the story. A load that fails falls
    through to the still page instead of leaving the loader up.
19. The age confirmation is a hard gate. A full-window panel asks `Are you of legal age?` with two
    controls, `Yes` and `No`. The page's own text also carries the question once as the continuous line `Are you of legal age?`. Until `Yes` is chosen nothing behind it can be driven and no sound exists. The answer is never remembered: every full page load of every route asks again, except
    `/terms`, `/unsupported`, `/sign-in/verify` and `/alerts/cancel`. Moving between routes inside
    the app after answering does not ask again.
20. Choosing `No` replaces the panel in place with `ACCESS DENIED` and
    `You need to be of legal age to access.`, and a `GO BACK` control that returns to the question.
    Nothing behind the panel becomes reachable from the denied state.
21. After `Yes` the panel leaves, the header bar appears once the loader has finished, and the story position is released at the first frame, or at the place the visitor is being returned to when the page was opened for that (rules 7 and 99).

### The two held gestures

22. Twice the story stops and waits for the visitor. The position is held at the gate; pushing the
    wheel against it visibly resists and springs back rather than freezing. Neither gate ever
    completes on its own, however long the visitor waits: the prompt pulses and the scene idles.
23. The portal gate, `HOLD & MOVE`, sits where the hand reaches the portal. Pressing anywhere in the
    frame and moving while held accumulates movement; the portal disc brightens and its rings widen
    as the movement builds, and once it passes the threshold the gate releases and the wheel drives
    the story again. Letting go early drains the accumulated movement back to nothing over about a
    second and the prompt returns. Touch works the same way, with a drag in any direction. Holding
    the confirm key while pressing arrow keys accumulates movement in the same way.
24. Before the pour, at the pedestal holding the three bottles, the visitor picks one flavour by pressing its bottle, or with the arrow keys and the confirm key; that choice decides the liquid poured, the robe's tint in the chapters after, and the flavour the carousel opens on. Moving on without choosing, or arriving by a header move, chooses `MARSHMALLOW COFFEE & CREAM`. The pour gate, `HOLD & POUR`, sits at the lip of the empty glass under the already tilted bottle.
    Pressing and holding fills the glass; movement is not required. The liquid surface tilts as it
    fills and the falling stream is drawn continuously. Letting go keeps the glass exactly as full
    as it was, so the pour can be resumed. The glass never overfills and there is no spill. Holding
    the confirm key fills at the same rate. When the glass is full the gate releases.
25. The prompt is a label on something the scene has already set up, never the only sign of it:
    with the prompt hidden, the reaching hand and the tilted bottle still say what to do.
26. Driving the story backwards past a completed gate and forwards again does not ask for the
    gesture a second time.
27. Every held gate also exists in the hidden text of the page as a control named by its prompt, `HOLD & MOVE` and `HOLD & POUR`, and activating that control satisfies the gate. Under a reduced-motion preference each gate becomes a single
    press.

### Sound

28. The sound is a layered mix that follows the story position, not the clock. Scrubbing backwards
    scrubs the mix backwards. No sound exists and nothing that makes sound is even created before the
    visitor presses the audio control, `Toggle audio`, in the lower right corner. Pressing it again
    silences everything at once at the master rather than fading voice by voice, and the silence
    survives chapter changes.
29. The bed underneath is five low drones tuned to a minor chord, a thread of late-night jazz mixed
    well below the drones, and wind over the outdoor chapters. It crossfades between chapters, and
    at the ascent and at the tasting chapter the crossfade begins before the boundary is reached, so
    the next chapter is heard before it is seen.
30. Over the bed sit the sounds the visitor causes: the portal hums, and its movement layer, the
    loudest interaction sound in the mix, rises with the accumulated drag, with a single contact
    sound when the portal opens; pouring starts, runs while held and stops on release, with a
    drinking sound in the chapter after; sparks in the ascent are placed left or right to follow
    the pointer; the bottles have a glass tap and a levitation glide; the temple collapse cracks;
    each narration box ticks as it appears, picked from five variants; footsteps change between an
    outdoor set and an indoor set; interface clicks are short and bright.
31. One-off sounds are never retriggered by small back-and-forth movement around a boundary. When
    the input goes idle, the interaction sounds duck and the bed comes forward. A narrated line
    queued for a chapter the story has already left is dropped rather than played late.
32. Every sound is synthesised in the browser as the page runs. Nothing is a recording.
33. The audio control is a four-bar level meter that dances to the live output while sound is on and
    rests as a static two-bar glyph while it is off. It is the first interactive element reached
    after the age panel closes.

### The collection act

34. The last chapters sell rather than tell, and every word in them is legible and comparable. The
    promise chapter sets `INDULGE NOW` over `ATONE LATER` across the top of a flat red field, three
    short capitalised lines across the middle, one paragraph of light long-form copy centred, and
    four single words at the outer corners, `VESPERI` and `SPIRITS` on one diagonal and `NOCTURNE` and `COLLECTION` on the other.
35. The poster chapter sets a solid block of display capitals on paper, `CHILL YOUR SPIRIT.` through
    `IS UP TO YOU.`, with a photographic coupe glass of flavour-coloured liquid composited over its
    centre. The type reads through the liquid and is bent by it; the glass is not cut out of the
    type. Side labels sit left and right, and a pale subtitle sits beneath.
36. The product carousel shows one photographic bottle, centred and about two thirds of the frame
    tall, with a dark cap, a cork and a printed label carrying the bottle's pour line. Behind it the
    flavour name is set in outlined display capitals, cropped by the frame at both sides. The two
    neighbouring flavour names sit left and right as quieter side labels. Next and previous
    controls step one flavour; each side label jumps to its flavour. Changing flavour slides the
    names across while the bottle stays in place, turns, and refills in the new colour.
37. Each flavour shows its tasting notes beneath its name, exactly:
    `MARSHMALLOW COFFEE & CREAM`: `Toasted marshmallow and cold brew over vanilla cream, finishing on bitter cocoa.`
    `ORANGE CHOCOLATE & CREAM`: `Candied orange peel folded into milk chocolate and cream, with a warm clove finish.`
    `MINT CHOCOLATE & CREAM`: `Garden mint over dark chocolate and sweet cream, cool and long.`
    The carousel order is marshmallow, orange, mint. The marshmallow bottle carries the light, vivid cyan tint, the orange bottle the light, soft amber tint and the mint bottle the light, soft green tint; in the content document their tint tokens are `flavour-a` for marshmallow, `flavour-c` for orange and `flavour-b` for mint.
38. Beneath the bottle, the data strip reads `NOCTURNE N.02`, then the standing-figure ornament,
    then `13% ABV` and `700 ML`: the collection name and number aligned towards the ornament, the
    ornament centred, the strength and volume aligned towards it from the other side, so both groups sit tight against the ornament. Beneath the data strip sits the
    hold control, `KEEP THIS ONE`, for the flavour on show.
39. The retail chapter, on paper, shows the red standing-figure ornament above
    `Select Houses Forthcoming` in display capitals over two lines, with `Vesperi Spirits` and
    `Nocturne Collection` as red side labels. It is the empty state of Where to drink it: when the
    visitor's location or a typed place is known and venues are near, the chapter shows the nearest
    venues with their reading for the flavour on show and a way into `/where`; when none are near,
    it keeps the line and offers `TELL ME WHEN IT LANDS`. The collection chapters and the footer carry links to `/cellar`, `/where`, `/tastings` and `/ritual`.
40. `GET /api/v1/content` returns the whole content document: `releases`, `flavours`, `chapters`,
    `credits` and `legal`. A flavour carries `id`, `name`, `tintToken`, `tastingNotes` and
    `releaseId`. A chapter carries `position`, `key`, `groundToken` and `lines`, and each line
    carries `text`, `emphasis` (the emphasised words) and `timingRef`. A tint or ground token is the
    name of a design role, such as `flavour-a` or `blood`, and the document never carries a colour
    value, so editing copy can never change the palette. The flavour ids are `marshmallow-coffee`,
    `orange-chocolate` and `mint-chocolate`.
41. If the network fails after the first load, the story still renders from the content document it
    already has.

### The Cellar

42. `/cellar` is a signed-in visitor's shelf. It renders as a scene in the same engraved style:
    bottles standing on a stone ledge, lit like the product bottle, one bottle per kept allocation,
    each turning slowly on its own rhythm. An empty shelf is the ledge alone with the standing-figure
    ornament centred on it and the line `AN EMPTY SHELF IS A KIND OF PATIENCE`. The header pill shows how many bottles are on the shelf, counting held, expiring, offered and confirmed bottles. Beneath the ledge, the shelf lists every release with its name, its remaining count and its own hold control for a chosen flavour, in the same states as the hold control beneath the data strip, so a visitor can claim, queue for or read the closed state of any release.
43. A release is a finite, numbered run: `GET /api/v1/releases/{releaseId}` returns
    `{"id", "name", "total", "claimed", "remaining", "opensAt", "closesAt"}`, and
    `GET /api/v1/releases` lists them all. `claimed` counts allocations that are held, offered or
    confirmed. `remaining` is `total` minus `claimed` and is advisory: it may be stale by the time a
    claim lands.
44. `POST /api/v1/cellar/holds` takes `{"releaseId", "flavour"}` and is the only call that consumes
    stock. On success it answers `201` with the new item in state `held` and an `expiresAt`
    seventy-two hours after the claim, issued by the server as an absolute instant, and the button
    beneath the data strip changes to `YOURS FOR 72 HOURS`.
45. `flavour` must be one of the three flavour ids; anything else is rejected as invalid with the
    reason `invalid_flavour` and nothing is written. A claim before a release opens or after it
    closes is refused with `409` and the reason `closed`.
46. One live claim per visitor per release. A claim against a release the visitor already holds,
    has been offered, has confirmed or is waiting for is refused with the reason `already_held`
    rather than stacked, and nothing is written.
47. A claim against an exhausted release answers `409` with `{"reason": "exhausted", "position"}`,
    and the visitor is now on that release's waitlist at that position, counted from one. Their shelf
    item reads `waitlisted` with that `position`, and the interface says
    `YOU ARE NUMBER {n} IN LINE` with the number filled in.
48. **Exactly one winner for the last bottle.** Two visitors claiming the last allocation of a
    release at the same moment produce exactly one `held` and one `waitlisted`, and the release's
    held, offered and confirmed allocations never exceed its total. This must hold under real
    concurrency, with any number of simultaneous claims.
49. Claims are idempotent. A claim sent with an `Idempotency-Key` header that repeats an earlier
    claim's key returns the earlier claim's item and consumes nothing further. Reloading or retrying
    while a claim is in flight never produces two allocations. While a claim is waiting for the
    server the control shows it is claiming and never shows the bottle as held; a network failure
    leaves it claiming with a retry that carries the same key.
50. `GET /api/v1/cellar` returns `{"items": [...]}` for the signed-in visitor, each item carrying
    `allocationId`, `releaseId`, `flavour`, `state`, `expiresAt` and `position`, where `position` is
    present only while `waitlisted` and `offerExpiresAt` is present only while `offered`. An item
    whose hold has less than six hours left reads `expiring`, and only then does the shelf show a countdown under that bottle. Everything on a shelf lives on the server: after a reload, or signed in on another browser, the same bottles appear in the same states.
51. A hold that is left alone expires at exactly its `expiresAt`: its item reads `expired`, the
    shelf says `IT WENT BACK. CLAIM ANOTHER`, and the allocation passes to the first waitlisted visitor within one minute as an offer, exactly as in rule 52, with the offer message. There is no path from `expired` back to `held` without a new claim.
52. `DELETE /api/v1/cellar/holds/{allocationId}` releases a held allocation at once and answers
    `204`. The allocation goes straight to the head of the waitlist: the first waitlisted visitor's
    item becomes `offered` with an offer that lapses twelve hours later, and that visitor is sent one
    message whose subject begins `A bottle came back for you:` followed by a space and the release
    name, for example `A bottle came back for you: Nocturne N.02 Salon Pour`, addressed to them only.
    Releasing a waitlisted item simply leaves the queue, and everyone behind moves up one.
53. `POST /api/v1/cellar/holds/{allocationId}/accept` turns an offer into a hold with a fresh
    seventy-two-hour expiry. `POST /api/v1/cellar/holds/{allocationId}/decline` gives the offer up
    and offers it to the next visitor in line. Accepting an item that is not `offered` is refused
    with the reason `not_offered`. An offer not accepted within twelve hours lapses within one minute of its `offerExpiresAt`, reading `lapsed`, and passes to the next visitor in line with the offer message of rule 52, or back to `remaining` when nobody waits. A lapsed item reads `IT WENT BACK. CLAIM ANOTHER` on the shelf, like an expired one, with no countdown.
54. `POST /api/v1/cellar/holds/{allocationId}/confirm` turns a hold into `confirmed`, which is
    final for that allocation. Confirming an already confirmed item returns it unchanged.
55. No message is sent when a hold is granted, when a visitor joins a waitlist, when a hold is
    confirmed or released by its owner, or when an offer is declined. The offer message is the only
    Cellar message.
56. With the connection cut, the shelf still renders from the last copy it had, marked as possibly
    out of date, and the hold control is unavailable with the reason stated in words.
57. The shelf renders correctly with zero, one and three bottles, and with a bottle in each of
    `held`, `expiring` and `confirmed` at once. A hold that expired in another tab, a release that
    closed while the visitor was reading, and an offer that arrived while signed out each show
    their true state on the next load.
58. Seeded releases: `N02`, Nocturne N.02, number 2, `13% ABV`, `700 ML`, total `240`, open since the
    day before first start and closing sixty days after; `N02-CASK`, Nocturne N.02 Cask Hold, total
    `1`, open; `N02-SALON`, Nocturne N.02 Salon Pour, total `1`, open; `N02-VESTRY`, Nocturne N.02 Vestry Pour, total `1`, open; `N02-EMBER`, Nocturne N.02 Ember Pour, total `1`, open; `N01`, Nocturne N.01, total `120`, closed since ten days before first start; `N04`, Nocturne N.04, total `60`, opening thirty days after first start.
    `visitor2@example.com` already has one `confirmed` allocation of `N02` in `marshmallow-coffee`, so `N02` starts with `239` remaining, and one `expired` allocation of `N01` in `mint-chocolate`, whose hold ran out before that release closed, and one `offered` allocation of `N02-EMBER` in `orange-chocolate`, offered thirteen hours before first start and never accepted, so it reads `lapsed` and, with nobody in line, its bottle is back in `remaining`.

### Where to drink it

59. `/where` shows venues near the visitor beside a drawn plan. The list sits on one side and the
    plan on the other; choosing a venue opens its detail in place. The plan is drawn by the film's
    own engraved line work, never by a mapping service: a hatched plan view, each venue marked by the
    small standing-figure ornament, the visitor's own position marked by the drawn pointer, and every venue that has the selected flavour picked out in red. The selected flavour comes from a flavour picker on the page, which starts on the flavour last shown in the carousel.
60. Location is asked for, never assumed. Granted, the visitor's coordinates are used. Refused, or
    not answered in good time, the page offers a place field instead and never falls back to a
    default city. `GET /api/v1/places?q=` returns every seeded place whose name starts with the typed
    text, ignoring letter case, as `[{"id", "name", "detail", "regionCode", "lat", "lng"}]`. A name
    that matches more than one place lists each with its `detail` so the visitor can choose:
    `Newport` returns both `Newport, Wales` and `Newport, Isle of Wight`.
61. `GET /api/v1/venues?lat=&lng=&radius=&flavour=` answers `{"region": {...}, "venues": [...]}`, where `region` is the region record of rule 65 for the given coordinate. `radius` is in kilometres from `1` to `50` inclusive;
    anything else is rejected as invalid with the reason `invalid_radius`. `flavour` is optional and,
    when present, one of the three ids. Each venue carries `id`, `name`, `kind`, `distance`, `stock`,
    `updatedAt` and `hours`, and the list is sorted nearest first.
62. Distance is the great-circle distance in kilometres on a sphere of radius 6371 km, rounded to one
    decimal place. Worked example: from Soho at `51.5136, -0.1340` with a radius of `5`, the list is
    `The Gilded Nave` at `0.2` then `Salt & Vesper` at `4.1`; with a radius of `3` it is
    `The Gilded Nave` alone.
63. `stock` is one of `in`, `low`, `out` and `unknown`. With a flavour, it is that flavour's reading
    at the venue. Without one, it is `in` if any flavour reads `in`, otherwise `low` if any reads
    `low`, otherwise `out` if every known reading is `out`, otherwise `unknown`. **A reading more than
    seventy-two hours old is `unknown`, never the old value**, and the interface says
    `LAST SEEN {n} DAYS AGO` beside it. A venue with no reading for a flavour is `unknown` for it.
64. `GET /api/v1/venues/{id}` returns the venue with `address`, `hours`, `timezone`, `lat`, `lng` and
    a `stock` object keyed by flavour id, each value `{"reading", "updatedAt"}` with the same
    seventy-two-hour rule. A venue whose hours have already closed today says so beside its hours.
    A venue removed while open in the detail says it is gone and returns to the list.
65. A coordinate's region is the region of the nearest seeded place. `GET /api/v1/regions/{code}`
    returns `{"code", "name", "listingAllowed", "ageFloor", "notice"}`. The decision is made on the
    server and never inferred in the browser. In a region whose `listingAllowed` is false, the venues
    call answers with that region and an empty `venues` list whatever lies nearby, the page shows
    the region's `notice` and `WE CANNOT LIST HOUSES WHERE YOU ARE` in place of the list and the plan,
    and the page shows no venue list or plan for that region at all.
66. With no venue inside the radius, the page says `NOTHING NEAR YOU YET` and offers exactly two
    actions: widen the radius, and `TELL ME WHEN IT LANDS`. Both work.
67. Venue marks arrive nearest first, one after another. Opening a venue does not change page: the
    plan moves in on it and the detail opens beside the list.
68. `POST /api/v1/alerts` takes `{"place", "radius", "flavour"}`, where `place` is a place id,
    `radius` follows the same `1` to `50` rule and `flavour` is optional: absent or `null` both mean any flavour. It answers `201` with
    `{"id", "place", "radius", "flavour", "state"}` in state `active`. A visitor has at most one
    active alert per place per flavour: setting the same alert again answers with the existing alert
    and creates nothing. An alert for a place in a region where listing is not allowed is refused
    with `409` and the reason `restricted`.
69. Setting an alert sends one message to the visitor whose subject begins `Alert set:` followed by a
    space and the place name, for example `Alert set: Soho`. The first line of every alert message
    reads `Cancel this alert: ` followed by the app's public address, `/alerts/cancel?token=` and the
    alert's cancellation code, which is at least 24 characters drawn from letters, digits, hyphen and underscore. Opening that link, signed in or not, cancels the alert in one click and
    shows `THAT ALERT IS OFF`; the link keeps showing that line if opened again. An unknown code changes nothing and shows a sentence saying the link is not recognised, with a way to `/where`.
70. An alert fires every time a host sets a reading of `in` or `low`, whether or not the reading changed, at a venue within the alert's radius of the alert's place, for the alert's flavour, or for any flavour when the alert has none. Firing sends one
    message whose subject begins `It has landed near you:` followed by a space and the venue name, for
    example `It has landed near you: Salt & Vesper`, and the alert becomes `fired`. A fired or
    cancelled alert never sends again.
71. `GET /api/v1/alerts` lists the visitor's own alerts. `DELETE /api/v1/alerts/{id}` cancels one of
    them and answers `204`.
72. With the connection cut, the last successful list renders stamped with how old it is, and alerts
    cannot be created, with the reason in words.
73. Seeded places: `Soho` at `51.5136, -0.1340`; `Shoreditch` at `51.5265, -0.0798`; `Ancoats` at
    `53.4855, -2.2254`; `Leith` at `55.9755, -3.1665`; `Newport` (`Wales`) at `51.5842, -2.9977`;
    `Newport` (`Isle of Wight`) at `50.7010, -1.2883`; `Le Marais` at `48.8590, 2.3620`; `Bergen` at
    `60.3913, 5.3221`. The first six are in region `GB`, `Le Marais` in `FR` and `Bergen` in `NO`.
    Regions: `GB` United Kingdom and `FR` France allow listing with an age floor of `18`; `NO` Norway
    does not, age floor `18`, notice `Listing where drink is sold is not permitted in this region.`
74. Seeded venues: `The Gilded Nave`, a bar in Soho at `51.5129, -0.1312`; `Salt & Vesper`, a bar in
    Shoreditch at `51.5246, -0.0776`; `The Chapel Cellar`, a restaurant in Ancoats at
    `53.4849, -2.2311`; `Le Confessionnal`, a bar in Le Marais at `48.8579, 2.3589`, zone
    `Europe/Paris`; `Nordlys Bar`, a bar in Bergen at `60.3930, 5.3242`, zone `Europe/Oslo`. The three in the United Kingdom are in zone `Europe/London`. Each venue's `address` is a single line naming its street and district, and every venue's `hours` read `17:00 to 01:00` in its own zone. Readings, relative to first start:
    The Gilded Nave has marshmallow `in` from one day before, orange `low` from twelve hours before and
    mint `in` from five days before, which therefore reads `unknown`; Salt & Vesper has marshmallow
    `out` and orange `in`, both from three hours before, and no mint reading; The Chapel Cellar has
    all three `in` from one day before; Le Confessionnal has orange `in` from one day before; Nordlys
    Bar has all three `in` from one day before.

### Tastings

75. `/tastings` lists hosted tastings beside the chosen session's detail. It is an ordinary document
    and behaves like a form: pick a session, say how many are coming, hold the seats, give a name and
    an address, confirm. Each step has a way back out that keeps what was already chosen. It is
    reachable from a venue on `/where` and from the footer.
76. `GET /api/v1/tastings?venue=&from=&to=` lists sessions as
    `[{"id", "venueId", "venueName", "title", "startsAt", "timezone", "capacity", "remaining",
    "price", "currency", "state"}]`, where `startsAt` is an instant, `timezone` is the
    venue's zone and `price` is in integer minor units of `usd`: `3500` is `$35.00`, never `35` and
    never `35.00`. With no query, every `scheduled` session is listed, one that has already started included, however far ahead or behind; `venue` is a venue id, and `from` and `to` are instants in the same format as `startsAt`.
77. Every time is stored as an absolute instant and shown in the venue's own zone. When the visitor's
    zone differs, the visitor's time is shown beside it and both are labelled. A visitor is never
    shown only their own time.
78. `POST /api/v1/tastings/{id}/holds` takes `{"partySize"}` and holds that many seats for fifteen
    minutes, answering `201` with `{"holdId", "expiresAt"}`. `partySize` is a whole number from `1`
    to `8`; anything else is rejected as invalid with the reason `invalid_party_size`. A party larger
    than `remaining` is refused outright with `409` and `{"reason": "insufficient", "remaining"}`,
    never partly granted. A visitor already holding seats at another session is refused with the reason `hold_elsewhere`. A session that has already started takes no new holds, with the reason `session_started`. `DELETE /api/v1/tastings/holds/{holdId}` gives held seats back.
79. **Capacity is never exceeded.** Held seats plus booked seats of a session never exceed its
    capacity and `remaining` never goes below zero, under real concurrency: two visitors asking for
    the last seats at the same moment produce one hold and one refusal.
80. While seats are held the page shows `SEATS HELD FOR {n}` counting down. A hold that expires while
    the form is open returns the visitor to the party size step with the session and the size still
    chosen, and says why.
81. `POST /api/v1/bookings` takes `{"holdId", "name", "email", "notes"}` and converts an active hold
    into a booking, answering `201` with `{"id", "sessionId", "partySize", "state", "name",
    "email"}` in state `booked`. A hold that has expired is refused with `409` and the reason
    `expired`. A booking sent with an `Idempotency-Key` header that repeats an earlier booking's key
    returns that same booking, so pressing confirm twice or retrying after a dropped connection
    produces exactly one booking.
82. Booking sends one message to the booking's `email` whose subject begins `Tasting booked:`
    followed by a space and the session title, for example
    `Tasting booked: Nocturne Night at The Gilded Nave`, and whose body names the venue and the
    time in the venue's zone. The confirmation then returns the visitor to the film's poster
    composition carrying their session details.
83. `GET /api/v1/bookings` lists the visitor's own bookings. `DELETE /api/v1/bookings/{id}` cancels a
    booking and answers `204` when the session starts more than forty-eight hours from now. Inside
    forty-eight hours it is refused with `409` and the reason `late`, the booking stays `booked`, and
    the page says `TOO LATE TO CANCEL. MOVE IT INSTEAD` and offers a reschedule. Cancelling at
    forty-seven hours is refused; at forty-nine it succeeds.
84. `POST /api/v1/bookings/{id}/reschedule` takes `{"sessionId"}` and moves the booking to another
    session with enough remaining seats, answering with the moved booking. A booking can be moved
    once; a second move is refused with the reason `already_rescheduled`. A target without room is
    refused with the reason `insufficient`, a target that has already started with `session_started`, and a cancelled target with `closed`.
85. A full session says `FULL. JOIN THE LINE`. `POST /api/v1/tastings/{id}/waitlist` takes
    `{"partySize"}` and answers `201` with `{"position"}`; an invalid party size is refused with `invalid_party_size`, joining the same list twice answers with the existing position, and joining the list of a session that still has room is refused with `409` and the reason `not_full`. Seats freed by a cancellation or an expired hold return to `remaining`; the list is kept in join order for the host to see, and nobody is moved into a session automatically.
86. A host cancelling a session (rule 105) moves every booking on it to `session_cancelled`, which
    offers a reschedule, and sends each booking's `email` one message whose subject begins
    `Tasting cancelled:` followed by a space and the session title.
87. No message is sent when seats are held, when a visitor cancels or reschedules, or when a visitor
    joins a waitlist.
88. With the connection cut, the page renders the visitor's existing bookings from the last copy it
    had and refuses new holds, saying why.
89. Seeded sessions, times relative to first start: `Nocturne Night at The Gilded Nave`, ten days
    later at `19:00` venue time, capacity `12`, price `3500`; `Late Pour at Salt & Vesper`, thirty
    hours later on the hour, capacity `8`, price `2500`; `Last Call at Salt & Vesper`, eight days
    later at `21:00`, capacity `6`, price `2500`; `Cellar Tasting at The Chapel Cellar`, fourteen days
    later at `18:00`, capacity `2`, price `4000`; `Sold Out Supper at The Gilded Nave`, twelve days
    later at `20:00`, capacity `4`, price `4500`, fully booked by `visitor2@example.com` for a party
    of `4`; `Soiree Nocturne at Le Confessionnal`, twenty days later at `20:00` in `Europe/Paris`, capacity `10`, price `3000`; `Early Pour at Salt & Vesper`, which started one hour before first start, capacity `8`, price `2500`.

### The Ritual

90. `/ritual` is the builder. The visitor chooses one of the three bottles using the carousel
    composition, then adds up to four mixers, one ice and one garnish, then pours it with the same
    `HOLD & POUR` gesture as the film, then names it, then saves it with `NAME IT`. The glass answers
    every choice at once: each added ingredient tints the liquid towards its own colour. Every step
    can be undone without losing the steps before it, and a visitor who leaves mid-build finds the draft again while the visit lasts, and on later visits too once non-essential storage has been accepted (rule 108). The builder uses a red ground with paper type.
91. `GET /api/v1/ingredients` returns `{"mixers", "ices", "garnishes"}`, each a list of
    `{"id", "name"}`. These are closed sets and the builder never offers anything outside them.
    Mixers: `cold-brew` Cold brew, `tonic` Tonic water, `oat-milk` Oat milk, `soda` Soda water,
    `espresso` Espresso, `ginger-ale` Ginger ale. Ices: `no-ice` No ice, `cubed` Cubed, `crushed`
    Crushed, `single-block` Single block. Garnishes: `no-garnish` No garnish, `orange-twist` Orange
    twist, `mint-sprig` Mint sprig, `grated-nutmeg` Grated nutmeg, `cocoa-dust` Cocoa dust. The
    garnish `gold-leaf`, Gold leaf, has been withdrawn: it is not offered and not accepted in a new
    save, and rituals that already use it keep rendering it.
92. `POST /api/v1/rituals` takes `{"flavour", "mixers", "ice", "garnish", "name"}` and answers `201`
    with `{"slug"}`. `flavour` is one of the three ids, `mixers` a list of at most four mixer ids
    (more is refused with the reason `too_many_mixers`), `ice` and `garnish` single ids from their
    sets (anything outside, or withdrawn, is refused with the reason `invalid_ingredient`), and
    `name` between `3` and `40` characters after trimming (otherwise the reason `invalid_name`).
    Every refusal writes nothing.
93. Names are checked before a link is made. A name containing a web address (`http`, `www.` or
    `.com`) or any of the words `casino`, `crypto`, `loan` or `viagra`, in any letter case, is refused
    with the reason `name_refused`; the builder returns to naming with the reason shown and the build
    intact.
94. The same ritual saved twice by the same visitor (same flavour, mixers in the same order, ice,
    garnish and name) answers with the existing `slug` and creates nothing. A save sent with an
    `Idempotency-Key` header that repeats an earlier save's key returns that save's `slug`.
95. A visitor may save at most five new rituals in any rolling hour. The sixth is refused with `429`
    and `{"reason": "rate_limited", "cooldownSeconds"}`, the builder enters its cooling-down state
    and says `ENOUGH FOR NOW. TRY AGAIN IN {n}` with the wait filled in, and the fifth save is never
    refused for this reason. A save that answers with an existing slug does not count.
96. The slug is the name in lower case with every run of other characters turned into one hyphen,
    with leading and trailing hyphens removed, then a hyphen and four lower-case letters or digits: `Velvet Hour` becomes something like
    `velvet-hour-7k2q`. `/ritual/{slug}` is the ritual's public page.
97. `GET /api/v1/rituals/{slug}` is public and returns `{"slug", "name", "flavour", "mixers", "ice",
    "garnish", "createdAt"}`, and nothing about who made it: no account id, no email, no display
    name. An unknown or deleted slug answers `404`.
98. `PATCH /api/v1/rituals/{slug}` takes the same body and changes a ritual for twenty-four hours
    after it was saved, for its owner only, checked exactly as a save with the same reasons; an edit does not count towards the hourly save limit. Anyone else is denied with the reason `forbidden` and the ritual does not change.
    After twenty-four hours the owner is refused with the reason `edit_window_closed`.
    `DELETE /api/v1/rituals/{slug}` deletes it for its owner and answers `204`.
99. Opening `/ritual/{slug}` enters the experience at the pour chapter with the ritual already
    loaded: the age panel comes first for a visitor who has not answered, then the visitor watches
    the ritual poured before anything else, under the line `SOMEONE POURED THIS FOR YOU` with the
    ritual's name, and is then released into the whole story from there. The page's own HTML
    already carries the ritual's name, bottle, mixers, ice and garnish as readable text, each ingredient by its name from rule 91 and the bottle by its flavour name, so a device
    that cannot draw the film still shows the recipe. A deleted or unknown slug shows the builder
    with `THAT ONE IS GONE. POUR YOUR OWN`, never an error page.
100. With the connection cut, the builder still works and the pour still renders, and saving is
     refused with the reason in words rather than queued silently.
101. The finished ritual card uses the poster composition and arrives with the only overshoot in
     the whole product, because it is the only celebration in it.
102. Seeded ritual: `midnight-confession-a1b2`, `Midnight Confession`, by `visitor2@example.com`,
     flavour `mint-chocolate`, mixers `espresso` then `oat-milk`, ice `crushed`, garnish `gold-leaf`, saved two days before first start, so its edit window has already closed.

### The host's venue

103. `/host` is a signed-in host's page for their own venue: its stock readings per flavour with the
     age of each, and its upcoming sessions with seats booked and held. It is a plain document on a
     paper ground, and it is not reachable from the film.
104. `GET /api/v1/host/venue` returns the host's own venue as `{"id", "name", "stock", "sessions"}`, with `stock` shaped as in rule 64.
     `PUT /api/v1/venues/{id}/stock` takes `{"flavour", "reading"}`, where `reading` is `in`, `low`
     or `out`, sets that reading with the current instant as `updatedAt`, and answers
     `{"flavour", "reading", "updatedAt"}`. An unknown reading is rejected with the reason `invalid_reading`, and an unknown flavour with `invalid_flavour`.
105. `POST /api/v1/tastings/{id}/cancel` cancels a session of the host's own venue and answers with
     the session in state `cancelled`. A cancelled session takes no new holds: a hold on it is refused with `409` and the reason `closed`. A session that has already started cannot be cancelled, with the reason `session_started`.
106. A visitor calling any of the three host endpoints is denied with the reason `forbidden`, and a host calling a visitor-only endpoint, such as a hold or a booking, is denied the same way. A host calling either for another venue is
     denied. In both cases the reading, the session and every booking are unchanged.

### The rest of the product

107. A terms page lives at `/terms`. The `Legal` link in the footer of every page leads to it, the
     sign-in form links to it, and it states the conditions of use, the legal drinking age
     requirement and what the product keeps about a visitor.
108. A first-time visitor is asked once about non-essential cookies, after the age panel has gone,
     by a small notice that never covers the centre of the film. Non-essential here means remembering
     the sound preference and a ritual draft between visits. The answer is recorded with
     `POST /api/v1/cookie-choice`, which takes `{"nonEssentialAccepted"}` and answers
     `{"visitorToken", "nonEssentialAccepted", "decidedAt"}`, and it survives a reload: the response sets a cookie that recognises the browser, and `GET /api/v1/cookie-choice` returns the recorded choice for that browser and the question is not
     asked again.
109. The site serves a favicon at `/favicon.ico`, generated by the server from the standing-figure ornament's geometry, and every page declares it in its document head with a `rel="icon"` link.
110. `/sitemap.xml` lists every public route: `/`, `/where`, `/tastings`, `/ritual` and `/terms`.
     `/robots.txt` points at the sitemap with a `Sitemap:` line.
111. Every page declares a social preview title and image with `og:title` and `og:image` meta properties. `/og/default.png` is a PNG generated on
     the server at request time from the poster composition; a ritual's page points at
     `/og/ritual/{slug}.png`, generated the same way with the ritual's name.
112. The still page, at `/?mode=still` and wherever the film cannot run, is an ordinary document: a
     still picture of each chapter's composition generated by the same recipes the film uses, the
     whole copy of the story as text, the product data as a description list carrying the name,
     `13% ABV` and `700 ML` of each flavour with its tasting notes, and every extension fully
     working from it.
113. The HTML of `/` and of the still page, as the server sends it, already contains the full text of the story
     in reading order as headings and paragraphs: the narration, the collection copy, the flavour
     names with their tasting notes, `13% ABV`, `700 ML` and every control's name. A screen reader
     or a search engine gets the whole story without driving anything.

## User flow

The information architecture is one film route plus the additions' routes. Everything inside the film is reached by moving the story, never by loading a document.

| Route | Purpose | Auth |
|---|---|---|
| `/` | The experience: the film over the page's full hidden text | public |
| `/?mode=still` | The still page in place of the film | public |
| `/unsupported` | Refusal for a browser that cannot draw the film, linking to the still page | public |
| `/sign-in` | Ask for a sign-in link; seeded accounts may also use their password | public |
| `/sign-in/verify` | Exchanges `?token=` for a session and returns the visitor to where they were | public |
| `/cellar` | The visitor's shelf | `visitor` |
| `/where` | Venues beside the drawn plan, alerts | public; alerts need `visitor` |
| `/tastings` | Sessions beside the chosen session, holds and bookings | public; holding and booking need `visitor` |
| `/ritual` | The ritual builder | public; saving needs `visitor` |
| `/ritual/{slug}` | A shared ritual, poured before anything else | public |
| `/alerts/cancel` | One-click alert cancellation from a message, `?token=` | public |
| `/host` | A host's own venue: readings and sessions | `host` |
| `/terms` | Terms and legal | public |
| `/sitemap.xml`, `/robots.txt`, `/favicon.ico`, `/og/default.png` | Crawl, icon and preview files | public |

Inside `/` the header pill moves the story to `#experience` or `#collection` without loading a
document. The footer's `INSTAGRAM` link leaves the site for the house's social page, `vesperi.spirits`;
`hello@example.com` opens a mail client; `Legal` opens `/terms`; `Tastings` opens `/tastings`.

**Entry and redirects.** Every full page load of `/`, `/cellar`, `/where`, `/tastings`, `/ritual`,
`/ritual/{slug}`, `/sign-in` and `/host` asks the age question first; the film routes run the
drawing check and the loader before it. A signed-out request for `/cellar` or `/host` goes to
`/sign-in` and returns to the requested page after sign-in. A password sign-in by a host lands on
`/host`; any other sign-in returns to where the visitor started. A `visitor` requesting `/host` gets
the product's own permission surface, naming what is required, never a blank page. A session that
expires part-way through an action leaves the action unapplied, returns the visitor to `/sign-in`,
and restores the page, the flavour and the choices they had once they are back. A handset held
upright on a film route gets the rotate panel; on the extension routes it gets the page itself,
laid out for the upright handset.

**Journeys.**

1. *Drive the film.* A visitor opens `/`. The loader draws, the age panel asks
   `Are you of legal age?`, they choose `Yes`, and the panel splits and tips away. The header bar
   unrolls and its two words rise into it one after the other. They press `Toggle audio`, and the
   drones come up. They scroll: the title lockup gives way to the hooded figure in the mist, the
   narration boxes tick in, the monolith rises. At the hand the story stops, `HOLD & MOVE` pulses at
   the fingertips, they press and drag, the portal brightens and opens. Inside the temple they reach
   the pour, `HOLD & POUR` sits at the glass, they press and hold and the glass fills. The robe takes
   the flavour colour, the columns fracture, the colonnade opens, and the collection arrives:
   `INDULGE NOW`, the poster, the carousel. They step to `ORANGE CHOCOLATE & CREAM` and read its
   tasting notes, then the data strip reads `NOCTURNE N.02`, `13% ABV`, `700 ML`. They press
   `EXPERIENCE` and the story glides back to the first frame with the sound and the ground restored.
2. *Keep a bottle.* Signed out, at the carousel on `MINT CHOCOLATE & CREAM`, they press
   `KEEP THIS ONE`. They are asked for their address, a message titled `Your Vesperi sign-in link`
   arrives, they open the link, and they land back on the mint bottle with the button reading
   `YOURS FOR 72 HOURS`. The header pill now shows one bottle on the shelf. On `/cellar` the bottle
   stands on the ledge, turning.
3. *The empty shelf.* `visitor@example.com` signs in with `deku-demo-pw-2026` and opens `/cellar`:
   the ledge stands alone with the ornament and `AN EMPTY SHELF IS A KIND OF PATIENCE`.
4. *The queue.* A visitor claims `Nocturne N.02 Vestry Pour` and holds its only bottle. A second
   visitor claims it and reads `YOU ARE NUMBER 1 IN LINE`. The first visitor releases it from their
   shelf. The second visitor receives `A bottle came back for you: Nocturne N.02 Vestry Pour`, opens
   `/cellar`, sees the offer with its twelve-hour window and accepts it; the bottle now reads held.
5. *Where, without location.* A visitor opens `/where` and refuses location. They type `Sou`, choose
   `Soho`, and set the radius to 5. The list shows `The Gilded Nave` at 0.2 km then `Salt & Vesper`
   at 4.1 km, and the plan marks both, nearest first. They pick `MINT CHOCOLATE & CREAM`: The Gilded
   Nave reads unknown with `LAST SEEN 5 DAYS AGO`. They choose `Leith` instead: `NOTHING NEAR YOU YET`
   with two actions. They press `TELL ME WHEN IT LANDS`, sign in, and a message titled
   `Alert set: Leith` arrives. They open its cancellation link and read `THAT ALERT IS OFF`.
6. *A restricted region.* A visitor types `Bergen`. The page shows the region's notice and
   `WE CANNOT LIST HOUSES WHERE YOU ARE`, with no list and no plan.
7. *Book a tasting.* `visitor@example.com` opens `/tastings`, chooses
   `Nocturne Night at The Gilded Nave`, sees the time in `Europe/London` with their own time beside it
   if they are elsewhere, sets a party of 2 and holds the seats. `SEATS HELD FOR` counts down. They
   give their name and address and confirm. A message titled
   `Tasting booked: Nocturne Night at The Gilded Nave` arrives, and the confirmation returns them to
   the poster composition carrying the session. They book `Late Pour at Salt & Vesper` too, try to
   cancel it, read `TOO LATE TO CANCEL. MOVE IT INSTEAD`, and move it to `Soiree Nocturne at Le Confessionnal`.
8. *A full session.* `Sold Out Supper at The Gilded Nave` reads `FULL. JOIN THE LINE`; they join and
   are told their position.
9. *Pour a ritual.* On `/ritual` a visitor chooses the marshmallow bottle, adds cold brew and oat milk,
   crushed ice and cocoa dust, holds to pour while the glass tints with each choice, names it
   `Velvet Hour` and presses `NAME IT`. The card arrives with its short link. In another browser,
   signed out, the link opens: the age question, then `SOMEONE POURED THIS FOR YOU`, the pour, then
   the story from the pour onward. They open `/ritual/midnight-confession-a1b2` and see
   `Midnight Confession` with its gold leaf garnish.
10. *A host updates a reading.* `host2@example.com` signs in and lands on `/host` for
    `Salt & Vesper`. They set orange to `in`. A visitor with an alert on Shoreditch for that flavour receives `It has landed near you: Salt & Vesper`. The host opens `Last Call at Salt & Vesper` and sees its booked and held seats. Cancelling a session there sends every booking on it `Tasting cancelled:` with the title and offers each a move.
11. *No second chance at the wrong age.* A visitor chooses `No`, reads `ACCESS DENIED`, presses
    `GO BACK` and is asked again.

**States.** Every list has an empty state that says what would fill it and how, distinct from its
loading state. Every loading state is laid out at the shape of the content it stands in for. No
spinner outlives a request, and no request fails silently: every failure names what failed, why,
and the one next action, in words, and the page stays usable. All four additions render a correct
empty state, because an empty state is what most visitors see first. A surface the visitor may not
see says so rather than pretending to be empty.

## UI/UX notes

The north star: in the first moment a visitor should feel they are holding the controls of a
printed film rather than reading a web page, and by the end they should know the three flavours
well enough to keep one. The register is consumer and editorial with atmosphere: the subject, first
the story and then the bottle, is always the first thing seen. The four additions switch register
on purpose and read as plain documents that behave like forms, while still wearing the same ink,
paper, red and type, so they feel like the same house rather than a form bolted onto the side.

Three stances, each of which a competing product could rationally invert. **Hand over clock**: almost
nothing moves on its own; the story moves exactly as far and as fast as the visitor's wheel or
finger, and stops the instant they stop. **Print over render**: tone is made of engraved lines rather
than smooth shading, and anything that would look computer-generated, from a soft blur shadow to a
gliding portal, is a defect. **Legibility over spectacle at the point of sale**: from the promise
chapter onward, every word the visitor needs to decide is readable, comparable and still.

Because the film must convey rarity and value, one thing dominates each frame and its surroundings
are quiet: the figure, then the portal, then the glass, then the bottle. Because the additions must
reassure while a visitor commits, nothing moves on the surface they are reading while they decide. Because the booking flow must
guide, each step has one obvious next action and everything else is quieter.

**Colour, by role.** The whole product is drawn from a small, strict kit, and every colour here has
one job. Ink is a near-black neutral: the dark ground and the ink of every engraved line, and the
most used colour in the product. Beside it sit two further near-black neutral steps and two deep
neutral greys, used for the first chapter's sky, the grey brush strokes behind the title and
shadowed stone. Paper is a near-white warm neutral, the off-white plate the woodcut is printed on,
with a second, barely different near-white warm neutral sheet used only where two papers overlap.
Bone is a near-white neutral, reserved for display type on dark and for the age panel. Blood is a
mid, vivid red and is the one saturated colour in the world: the temple, the red sky, the emphasis
words in the narration, the header ornament, the footer accents and the hold control. It has four
close relatives, never used as separate meanings: a mid, vivid red for red under hatching, a slightly
shaded mid, vivid red, a lit mid, vivid red for rim light on columns, and a deep, soft red for the
portal's core and the tint of the drawn pointer. The figure's robe is a light, muted orange in three
close steps for base, shade and light, with a mid warm neutral for belt and trim and a light warm
neutral for the stair and the monolith.

The three flavour tints are the only other colours anywhere, and each means its flavour and nothing
else. Marshmallow Coffee is a light, vivid cyan, with a light, soft cyan lit face and a light, vivid
cyan seen through glass. Mint Chocolate is a light, soft green, with a light, soft green lit face.
Orange Chocolate is a pale yellow, a light, soft amber, with a light, soft amber lit face and a mid, vivid amber core. A tint travels with its flavour through the robe, the liquid, the contact shadow and the
label; it never decorates anything else. No blue appears anywhere except the cyan of Marshmallow Coffee; no saturated red other than blood and no saturated green other than the mint tint may appear as a design colour. One further colour carries meaning in the additions only: a failure colour taken from blood; success and progress are shown in ink with a word and a drawn mark, never by a colour of their own; the failure colour is always paired with a word, never used alone.
The ground itself changes with the chapter, between ink, paper and blood, and the house mark
inverts with it. The additions use paper grounds with ink type and red for the one thing that
matters on each surface; the ritual builder alone uses a red ground with paper type. Type on a red ground is always paper or bone, and red type on ink is used only at large display sizes or as the brief hover of the age panel controls, so every reading pair meets the contrast floor below. The product is committed to its own grounds and offers no separate light or dark mode. The exact
shades are yours, so long as each role above stays distinct, the flavour tints stay the only
non-house colours, and no state is ever carried by colour alone.

Against defaults: no surface dominated by one hue family with no second signal, no gradient-washed
hero, no photographic background, no decoration standing in for content, no marketing card grid for
the bottles, and nothing borrowed from a template whose subject is not a printed, engraved world.

**Type.** Four faces, each with one job and a clear personality. The display face is tall, very
high-contrast and sharp, with hairline serifs and vertical stress, like the display faces of late eighteenth-century printing; it carries every
large headline, every chapter title and the flavour names, always in capitals, never hyphenated, and
it is drawn inside the film so it grows and shrinks continuously rather than snapping between sizes.
The interface face is a heavy, rounded geometric sans with soft terminals, set in letterspaced
capitals; it carries the header controls, labels, the narration boxes and the data strip. A regular
weight of the same family carries secondary labels. The long-form face is a light, open text sans
with an oblique, used for the one paragraph of body copy in the promise chapter, for footer copy and
for session detail in the additions. The display face is the one that carries the identity; the
other three must stay recognisably rounded and light respectively. The families are yours.

The scale carries relationships rather than values. The largest chapter title is the largest thing
in the product; a second chapter-title step sits a little below it; the standing display size is
roughly half the largest; the age question and the product name sit a step below that; sub-headings
are roughly a quarter of the largest. Display lines are set tight, at roughly four fifths to one times
their size, and the poster and the largest titles are set solid so lines touch. Interface text sits
a little looser. The base text, the narration and the header controls are about a fifth of the standing display size, and the smallest interface labels a step below those; figures line up in columns wherever counts, prices or times stack. Interface
sizes stay fixed across screen sizes; display type scales with the film. The exact sizes are yours,
so long as those relationships hold and no text a visitor must read to act is smaller than the base text.

**Space, shape and texture.** One base spacing unit, yours to choose, and every gap in the additions is a multiple of it; sections read as separate at a glance without a drawn divider. Corners are square throughout
the film. The only fully rounded shapes are the header pill, the circular held-gesture prompts, the
loader bar's ends and the handset carousel arrows. Comic panels have hand-drawn edges that are four
separate slightly wobbly strokes, never parallel and never meeting cleanly at the corners, and the
ink weight of those edges stays the same however large the panel grows. Every rendered surface
carries a fine paper grain and engraved hatching; the hatching is tighter on faces and cloth, medium
on stone, and wide and open in the sky, and it never crawls across a surface. Space and density in
the additions are comfortable: a session list shows several sessions per screen without crowding.

**Motion.** The exact durations and curves are yours, so long as the characters and orderings below hold. The motion character is eased, and it is scoped: only the furniture plays on its own
clock, and it always eases rather than snapping. Everything in the story is attached to the hand.
Everything that does animate on its own uses a small closed set of characters and nothing invents a
new one: a symmetrical ease in and out as the default; a gentler symmetrical ease for the loader and
the age panel; a settling ease with no overshoot for the header reveal, the hold grant and venue
marks; an ease that arrives almost at once and then creeps; a long-tailed ease for chapter-level
entrances such as the shelf and the booking confirmation; and one curve with overshoot, used exactly
once, for the finished ritual card. The quickest movement in the product is the age panel controls'
hover; the slowest is the header bar unrolling. Staggers run left to right and nearest first, a
fixed short beat apart. The named moments, each described fully under `## Front-end specification`,
are: the header unroll and stagger, the gate split and dismiss, the gate heading rise and the
actions falling, the action hover and label hover, the panel wipe, the portal pulse and the column
fracture on stepped time, the lagging pointer, the breathing light beams, the karaoke lighting, the
letter-by-letter reveal with jitter, the carousel slide with the bottle's repour, the cellar grant
and the shelf entrance, the venue marks arriving nearest first and the plan moving in on a venue,
the booking confirmation entrance and the ritual card's overshoot.

A reduced-motion preference is honoured properly rather than switched off: the film becomes a
sequence of still compositions stepped by scroll, with no camera movement, no idle breathing and no
parallax; both held gestures become single presses; the furniture's transitions shorten to the
quickest tier instead of disappearing, so state changes stay visible. Nothing flashes: moving
between ink, blood and paper at full frame always takes at least as long as the age panel's exit,
and nothing changes brightness more than three times a second.

**Accessibility floors, which are contract rather than taste.** Text meets WCAG 2.2 AA contrast
against its ground: at least 4.5:1 for body text and 3:1 for large display text and for non-text
indicators, on every ground the chapter passes through, including text laid over the film. Every
interactive target meets the WCAG 2.2 AA target size. Keyboard navigation reaches every control,
including the whole story position, both held gestures, the carousel's previous, next and side
controls, the age panel and the audio control, with a visible focus ring on every one. The age panel
keeps focus inside itself while it is open and hands focus back to the page when it closes. Every
control has a name, and icon-only controls always do: `Toggle audio`, `previous slide`,
`next slide`, `left text` and `right text` are those names. Meaning is never carried by colour
alone: a stock reading is a word, a held bottle is a word, a waitlist place is a number. The film's
drawing surface is hidden from assistive technology and never takes focus. Every content image
carries alternative text that says what it shows.

**Layout, scaling and responsive behaviour.** Scaling is done by the camera, not by the layout: the film does not reflow; its camera reframes. The vertical
extent of every composed shot is preserved at every window size and the sides widen or narrow, so a
composition never crops at the top or bottom and comic panels never squash. On a desktop the full
composition shows; on a tablet the same composition shows narrower; on a handset held sideways the
whole film runs, with circular previous and next arrows either side of the bottle in place of hover
targets, and the flavour names travel further and for longer. On a handset held upright the film is
refused by the rotate panel, and that refusal is the only thing on screen. The pointer-only touches,
the hover lift on the header and the drawn pointer, are simply absent on touch, and their absence
changes nothing else. The four additions are the only parts that reflow like documents, and they
must work on a handset held upright: at a narrow viewport nothing overflows sideways, the list and
the plan on `/where` stack, the session list and detail on `/tastings` stack, the shelf keeps every
bottle and action reachable, and every navigation target stays reachable. Every page declares a
responsive viewport. The arrangement at every width between is yours, so long as it holds.

**One primary action per surface.** The hold control beneath the data strip, the alert control on an
empty venue list, the hold and confirm steps on a session, and `NAME IT` on the builder each lead
their surface and carry the strongest contrast on it; everything else is quieter.

## Technical requirements

Frontend: **SolidStart** with Solid and its router, built as a production server-rendered bundle.
Backend: **Fastify** on **Node 20**, in TypeScript, running in the same process and serving both the
SolidStart request handler and the JSON API under `/api` on one origin. Datastore: **PostgreSQL**,
reached at `DATABASE_URL`, through the `pg` driver. Mail: **Mailpit** over SMTP, reached at
`SMTP_HOST` and `SMTP_PORT` with `SMTP_USER` and `SMTP_PASS`, through **Nodemailer**. Passwords are
hashed with **argon2**. Social preview images are rasterised on the server with
**@resvg/resvg-js** from a generated vector composition. The rendering model is a server-rendered
shell with islands: the browser's first response for every route is complete HTML, including the
whole text of the story on `/`, the still page, the terms page and a shared ritual's recipe, and the
film, the furniture's motion, the held gestures, the sound and the additions' interactivity hydrate
as islands afterwards. That is the right trade here because the hidden text is the document search
engines, link previews, screen readers and locked-down machines all read, and it must exist before
any script runs.

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing services
available in this environment are **PostgreSQL** and **Mailpit**, and reaching for anything else is a
contract violation. The one carve-out is in the browser: the libraries that draw the film in real
time, synthesise its sound and drive its motion are yours to choose, provided they install from the
public npm registry at build time and ship inside the production bundle.

**The film's machinery, stated as properties.** The film renders in real time into the browser's
accelerated drawing context, full window, at the device's pixel density, under a transparent layer
of interface. A second-generation drawing context is used where it exists and a first-generation one
remains a working fallback. The frame is drawn to an off-screen surface first so the engraved and
paper passes can read the whole finished frame, and tone mapping is applied once, at the final
composite, so the paper white never drifts between chapters. Edge smoothing can be switched off on a
device that cannot afford it without changing the composition, and one pixel-density value is
authoritative for every surface. If the browser takes the drawing context away, the film rebuilds
and returns to the visitor's current story position rather than to the start.

**Module and component architecture, as observable properties.** Four parts never reach into each other: the
part that turns input into the story position and owns the held gestures; the part that draws a
frame for a given position and holds no state the position does not determine; the interface layer
of furniture, overlays and forms, which never moves the story position directly; and the data part
that talks to the API, caches and retries and knows nothing about chapters. Removing the four
additions leaves the film working exactly as before; nothing in the film depends on them. None of
the authoring tools a production build of this kind sometimes carries (a font editor, a render
statistics panel, a live surface editor, a save control) exists in this product.

**Zero shipped assets.** The product ships no image file, no model, no font atlas and no sound file
for the film. Paper grain and cloud fields are generated as noise when the page loads, and the fine dither that keeps gradients from banding is generated the same way; the hatching is
drawn by the surfaces themselves; figures, stair, monolith, columns, altar, debris and frames are composed from simple generated shapes, the hand built from a rounded palm with tapering fingers and an offset thumb, hair from a handful of flat strands shaded by the hatching, and drifting leaves drawn once and scattered; the bottle, its liquid, its label and the coupe glass are
generated, with the label printed at load from the bottle's own copy and grained so it reads as paper;
the reflection that makes the bottle look photographic comes from a generated surrounding with one
small hot highlight placed high to one side and a broad dim fill opposite; distance-field type is
generated at load from whichever display face resolves; every sound is synthesised. Where a face must
be licensed and is not, a free face of the same classification stands in. Total generated asset
weight stays under four megabytes, of which sound is under one.

**Where the cost is.** Eighteen prepared chapters are cheap only if chapters far from the story position genuinely let go of what they hold; the hatching runs on every drawn pixel, so pixel density is the main lever on a weak machine; the colonnade is the deepest scene and the one most likely to drop frames; the sound graph runs its buses, effect chains and analysis for the whole visit.

**Performance budgets.** The loader is on screen within one and a half seconds on a mid-range laptop
over an ordinary connection. The age panel is dismissable and the first chapter live within six
seconds. The film holds sixty frames a second through the first seven chapters on integrated laptop
graphics and never falls below thirty through the temple collapse. Nothing is allocated inside the
per-frame draw. Memory after a full forward and backward pass is within five percent of memory at the
start. When the measured frame time says the device is struggling, the film makes itself simpler on
its own, in this order and without asking: it lowers the pixel density, then switches off edge
smoothing, then reduces hatching to a single line frequency, then reduces the sound analysis to one
band, and only as a last resort falls to the still page. The decision is made from measured frame
time, never from the device's name.

**Health.** `GET /api/health` returns `200` with `{"status", "checks"}` once the app holds a
PostgreSQL connection and the SMTP host accepts a connection. It answers before any session exists.

**Logging.** One structured JSON object per line, carrying a timestamp, a level, a stable event name
and a request identifier. No log line carries an email address, a sign-in code, a session token or a
password.

**Concurrency and repeat safety, stated as properties of the running system.** Two simultaneous
claims on the last allocation of a release leave exactly one hold and one waitlist entry, and the
loser is told its position; held, offered and confirmed allocations of a release never exceed its
total. Two simultaneous seat holds that together exceed a session's remaining seats leave exactly one
hold and one refusal, and held plus booked seats never exceed capacity. A repeated claim, booking or
ritual save that carries the same `Idempotency-Key` as an earlier one returns the earlier result and
creates nothing new. A failed request leaves no partial state: no allocation without an owner, no
seats held by nobody, no booking without its hold. These guarantees hold when the requests genuinely
arrive together, not merely when they arrive one after another.

**Security.** No credential, SMTP password, database address or session secret appears in anything
the browser downloads. Every response carries the standard security headers, including a nosniff
content-type policy.

**Launch files.** `/favicon.ico` is served and declared in every page head; `/sitemap.xml` and
`/robots.txt` are served as described in rule 110; every page carries its own title and description; and every page's head carries a viewport declaration of `width=device-width`.

## Data model

Twenty-two tables. All timestamps are UTC, and calendar-day logic uses the server's UTC day. Every `id` an endpoint returns is the `id` of the row it names.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

`app_user`: `id`, `email`, `role` (`visitor`, `host`), `display_name`, `password_hash`, `venue_id`,
`created_at`. `email` is unique and stored lower case. `password_hash` is empty for an account opened
by a sign-in link and never holds a readable password. `venue_id` is set for a host only.

`app_session`: `id`, `user_id`, `token_hash`, `created_at`, `expires_at`, `revoked_at`. A session is
valid until `expires_at`, fourteen days after creation, unless revoked.

`sign_in_link`: `id`, `email`, `token_hash`, `created_at`, `expires_at`, `used_at`. A code is usable
once and for ten minutes.

`release`: `id`, `name`, `number`, `abv`, `volume_ml`, `opens_at`, `closes_at`, `total`. `id` is the
short key (`N02`). `claimed` and `remaining` are derived on read, never stored.

`flavour`: `id`, `name`, `tint_token`, `tasting_notes`, `release_id`, `position`. `tint_token` is
one of `flavour-a`, `flavour-b`, `flavour-c`.

`chapter`: `id`, `position`, `key`, `ground_token`. Eighteen rows, positions `0` to `17`.

`narration_line`: `id`, `chapter_id`, `position`, `text`, `emphasis`, `timing_ref`.

`credit`: `id`, `role`, `name`, `link`. `legal_link`: `id`, `label`, `href`.

`allocation`: `id`, `release_id`, `user_id`, `flavour_id`, `state` (`held`, `waitlisted`, `offered`, `confirmed`, `released`, `expired`, `declined`, `lapsed`), `idempotency_key`,
`created_at`, `expires_at`, `offered_at`, `offer_expires_at`, `confirmed_at`, `released_at`. For every
release, the allocations in `held`, `offered` or `confirmed` never outnumber `release.total`, under
concurrent claims. A user has at most one allocation in `held`, `offered`, `confirmed` or
`waitlisted` per release. `expiring` is derived on read for a `held` row with under six hours left
and is never stored. `position` is not a stored value: it is derived on read, counting from one among the release's waitlisted rows in claim order.

`region`: `id`, `code`, `name`, `listing_allowed`, `age_floor`, `notice`. `code` is unique.

`place`: `id`, `name`, `detail`, `region_code`, `lat`, `lng`.

`venue`: `id`, `name`, `kind` (`bar`, `restaurant`, `shop`), `address`, `lat`, `lng`, `timezone`,
`hours`, `place_id`.

`venue_stock`: `id`, `venue_id`, `flavour_id`, `reading` (`in`, `low`, `out`), `updated_at`. One row per venue and flavour. `unknown` is derived on read for a missing row or one older than seventy-two hours.

`landing_alert`: `id`, `user_id`, `place_id`, `radius_km`, `flavour_id`, `state` (`active`, `fired`,
`cancelled`), `cancel_token`, `created_at`, `fired_at`, `cancelled_at`. A user has at most one
`active` alert per place and flavour, with an absent flavour counting as its own value.

`tasting_session`: `id`, `venue_id`, `title`, `starts_at`, `timezone`, `capacity`, `price_minor`,
`currency`, `state` (`scheduled`, `cancelled`). `remaining` is derived on read.

`seat_hold`: `id`, `session_id`, `user_id`, `party_size`, `state` (`active`, `converted`,
`released`, `expired`), `expires_at`, `created_at`. A hold lasts fifteen minutes. A user has at most
one `active` hold. For every session, active held seats plus booked seats never exceed `capacity`,
under concurrent holds.

`booking`: `id`, `session_id`, `user_id`, `hold_id`, `name`, `email`, `notes`, `party_size`,
`state` (`booked`, `cancelled`, `session_cancelled`), `reschedule_count`, `idempotency_key`,
`created_at`, `cancelled_at`. `reschedule_count` never exceeds one.

`tasting_waitlist`: `id`, `session_id`, `user_id`, `party_size`, `created_at`. The position is derived on read from join order.

`ingredient`: `id`, `kind` (`mixer`, `ice`, `garnish`), `name`, `withdrawn`.

`ritual`: `id`, `slug`, `user_id`, `flavour_id`, `mixer_ids`, `ice_id`, `garnish_id`, `name`,
`idempotency_key`, `created_at`, `updated_at`, `deleted_at`. `slug` is unique. A deleted ritual keeps
its row with `deleted_at` set and is never served.

`cookie_choice`: `id`, `visitor_token`, `non_essential_accepted`, `decided_at`. `visitor_token` is
unique, and the recorded choice is what stops the question being asked again.

**Seed data.** Everything in the seeded-record rules of `## Core features` is present after first
start: the four accounts with their names and, for the hosts, their venues; the seven releases and
`visitor2@example.com`'s confirmed allocation; the three flavours with their tint tokens and tasting
notes; the eighteen chapters in order with their ground tokens (`wander` ink turning to paper,
`profile` and `approach` paper, `near` paper turning to blood, `hand` and `target` blood,
`transition` ink, `cathedral` blood on ink, `drink-selection` and `drink-pour` blood, `anti-gravity`
ink and paper, `pillar-crumble` blood, `colosseum` paper, `taste` and `collection` blood, `products`
blood turning to paper, `retail` paper, `footer` ink) and their narration lines; the credits
`Lanternfish Studio` for design and `Low Hum Audio` for sound; the legal link `Legal` to `/terms`;
the three regions; the eight places; the five venues with their readings dated relative to first
start; the seven tasting sessions and `visitor2@example.com`'s booking of four; the ingredient sets
with `gold-leaf` withdrawn; and the ritual `midnight-confession-a1b2`.

Seeding must be idempotent: restarting the app must not duplicate rows, and must not move any seeded
date.

## Front-end specification

This section carries the visual and interaction detail of the film and the additions. It adds
nothing that contradicts `## UI/UX notes`, and every value it leaves out is yours.

**The stack of layers.** The chrome, meaning the mark, the header pill, the audio meter and the footer, persists across every chapter; everything else belongs to a chapter. From back to front: the film's drawing surface; the hidden text of the page;
each chapter's own transparent overlay of panels, narration and labels; the furniture (mark, header
pill, audio meter); the age panel; and on top of everything the rotate panel. Nothing in the
interface layer paints an opaque background except the age panel, the rotate panel and the header
pill. All eighteen chapter overlays exist from the start and stay present, each nudged continuously
by the story position rather than shown and hidden.

**The mark, upper left.** A circular line drawing of a haloed figure holding a cup, beside a two-line
wordmark reading `Vesperi` over `Spirits` in the display face, with a long descending swash on the
first letter of the second line. It is white on dark chapters and ink on paper chapters, and it swaps
exactly at the chapter boundary, never through a blend. It is a link to the start of the story.

**The header pill, upper right.** A rounded paper bar holding `EXPERIENCE`, then a small red flourish
ornament, then `COLLECTION`, in the interface face, letterspaced capitals. The word matching where the
visitor is sits at full ink strength and the other is quieter: `EXPERIENCE` from the first chapter
through the collapse, `COLLECTION` from the colonnade onward. The pill carries the shelf count once a
visitor has kept a bottle. Its entrance is the *header unroll* and *header stagger*: nothing of it
appears until the loader has finished; then its paper background grows from a flat sliver to full
width, unrolling sideways, and after it the first word, the ornament and the second word each rise a
short distance while fading in, one after another, a short fixed beat apart, left to right, like
cards being dealt. Hovering the active word is the *label hover*: it lifts slightly and brightens on
the same settling character as the reveal. The red flourish is the only red in the header and the
only part of it with motion of its own.

**The audio meter, lower right.** Four vertical bars drawn as geometry that move with the live output
of the mix while sound is on, updating at a steady, slightly film-like cadence rather than at the
display's full rate, and resting as a static two-bar glyph while sound is off. It is a button named
`Toggle audio`.

**The footer.** The one conventional layout in the film, on ink: the mark again, larger, in bone; an
`INSTAGRAM` link in the heavy interface weight; `hello@example.com` in the regular weight; a line
`Made by Lanternfish Studio and Low Hum Audio` with both names underlined as links, in the light
long-form face at the small interface size; `Legal`; and `Tastings`. A bordered ink tile in the footer
responds to hover.

**The age panel.** A full-window panel in bone type on ink with real depth behind it, built as an
upper half and a lower half. The question is set in the display face over two lines, `Are you of`
over `legal age?`, and the two controls, `Yes` and `No`, are boxed words in the heavy interface
face. Hovering a control is the *action hover*, the quickest movement in the product: its frame and
its text turn blood red together. Its entrance is the *gate heading rise*: the question rises into
place from just below its own height, fading in, so it reads as rising out of the lower half. Its
exit is the *gate split* and *gate dismiss*: the two halves slide apart vertically like a pair of
shutters, each travelling exactly its own height, with the world already visible behind; the panel
itself begins fading only a moment after the halves start moving, tipping away into the screen with
perspective rather than fading flat; and the *gate actions fall*, so the two controls are still
visibly leaving after the panel has gone. The whole exit reads as a trapdoor, never a dissolve. The
panel may exit through more than one route; the shutter split described here is the required one.
The denied state replaces the panel's content in place with `ACCESS` over `DENIED` in the display
face, the line `You need to be of legal age to access.` beneath, and `GO BACK`.

**The rotate panel.** On a handset held upright: `Please rotate your device.` as four words, each
its own element, centred on ink, above everything else, plus the whole line once as hidden text.

**The loader.** A small drawn mark, the standing-figure ornament drawn once and mirrored rather than
drawn twice, over a fully rounded progress bar whose unfilled track is drawn at half strength. It
reports real progress and sweeps as the first chapter prepares. It is itself drawn by the film, and
the world beneath already knows whether the loader has finished.

**Iconography: the six drawn marks.** Every mark in the product is geometry drawn in the page, never an image file
or a font: the standing-figure ornament, a robed figure abstracted to a column, used as the chapter
marker (white on dark inside the film and red on paper further down), on the retail chapter, as the
venue marks on the plan, at the heart of the loader and as the favicon; the comic panel frame of four
separate hand-drawn edges; the red flourish between the header words; a small single-stroke arrow and
a two-stroke compound arrow, both ink, used as the carousel's previous and next controls. None of the six changes colour with state, with one exception: a venue mark on the plan turns red when that venue has the selected flavour. Otherwise the only colour difference is the ornament's white and red placements.
All six scale with the frame, never with the text around them. The panel frame keeps its ink weight
constant as panels grow: frames that fatten as they scale read as vector art rather than print, which
is the most visible way to get this wrong. The two arrows are present at all times and laid out only in
the collection chapter; their hit areas belong to the hidden text as well.

**The engraved material.** One material underlies almost every surface in the film, and getting it
right is most of the look. Tone is quantised into a small number of line densities rather than shaded
smoothly: below one threshold a surface is open hatching, between two thresholds it is closed
hatching, above the second it goes solid. Figures keep a wider band of in-between tone than stone
does, so people look drawn and buildings look carved. Hatching is laid in the surface's own space so
it sticks to the object as the camera moves, slightly off vertical, projected along a tilted axis so
it wraps rather than sitting flat on the screen, and its line weight is compensated for distance, so a
column fifty deep in the colonnade reads as separate drawn lines rather than clogging into black.
The hatch angle is biased a little off vertical, and the hatch never crawls. There is a single key light in the whole film. Hatch frequency and stroke weight run in opposite
directions on purpose: the floating rocks are the coarsest hatch with the heaviest few strokes; the
portal next; then the first chapter's ground and frames; then the sky; the characters, walls, bottles
and frames in the middle; floors and ground a little finer; the profile background finer again; and
the coupe glass is the finest mesh in the film with the lightest strokes. Each surface moves through three tones from the chapter's set.

**Mechanisms every surface shares, as what the visitor sees.** A comic panel genuinely cuts the world
at its edge, so a column stops at the frame instead of being covered, and overlapping panels still
show correct depth; the ascent's floor is the one surface that is never cut, because it runs past every
frame. A panel can be a trapezoid in perspective and still carry undistorted hatching. Five effects
advance in visible discrete jerks rather than smoothly, the way hand-drawn animation is shot on
twos: the portal, the three surfaces of the hand-and-portal composition, and the column fracture;
nothing else in the film judders, and making these smooth makes the temple act look computer
generated. One single wind bends the robe, the grass, the floating rocks, the background and the light
beams, so nothing in a frame ever blows the wrong way; the wind is a function of position rather than
of time. The world holds still behind the open age panel and wakes once the loader has finished.

**The effect catalogue, chapter by chapter.** The first chapter's sky is a four-tone vertical ramp from
deep grey through near-black into red that scrolls with the story. Its ground is a displaced field of
white cloud brush strokes over flat black. The title lockup, `THE` over `NOCTURNE` over `EXPERIENCE`
with the middle line at the largest size in the product, fills with a four-tone type fill as the story
advances, and the chapter's panel frames carry a padded, warm robe-coloured border. The profile chapter
sits on the finer paper sheet with the finest hatch of the outdoor act and a slight bend. The approach
chapter uses a three-tone ramp of paper, robe shade and dark grey projected through four points. The
near chapter lays wind-driven ground curves under a flat field. Contact shadows under figures are
hatched and stippled, never a soft blur, and they take the flavour tint once the robe has it. The portal
is concentric rings stepping between black and white on stepped time. The reaching hand is a four-tone
fluid field of black, white and reds that moves with the story. The hand-and-portal composition shares
stepped time and a circular cut-out, in shaded red and white. The passage inside is a repeating field of
vertical lines scrolled through the frame. The temple's walls and floor use the material in its red set.
The light beams in the temple are volumes, not glows: each is about four times taller than wide, with a
cross-section that is deliberately not circular, narrowing on a curve rather than a cone, with a lateral lean a little off vertical, able to turn through a full rotation, softly masked across its body, fading unevenly at both ends so it
never stops cleanly, and filled with two slow noise fields of almost the same scale drifting together so
the beam breathes without ever visibly repeating; the wind may disturb it only past a threshold. The bottles in the world use the material at a much finer stroke than anything around them. The refracting glass has a clipping plane with a feathered edge. The pour chapter
uses the red set with the flavour tint in the glass, and the glass refracts with the finest hatch in the
product and a feathered clipping edge. The ascent's floor is the material in robe tone with wind-driven
displacement and no clipping. The pillar fracture reacts to the pointer's influence and breaks on stepped time.
The floating rocks each keep their own rotation in the shared wind with the coarsest hatch, and the anti gravity floor beneath them is never clipped. The colonnade's floor
and title use the paper set with a deep red tint. The drawn pointer is a small tinted mark in deep red
and white that follows the real pointer a beat behind and reads its velocity; the native pointer stays
visible and the drawn mark is additional; on touch it does not exist. The footer tile is ink with a
bone border and a hover response. Display type uses a per-letter reveal with stagger, red emphasis and
karaoke; carousel type uses the same at a tighter stagger. The loader is sharpened vector animation.
The bottle and the glass are the only physically based, realistically lit objects, with tone mapping and a reflected surrounding: a generated surrounding gives the reflection in the glass and turns with the bottle.

**The chapters, in order, as compositions.** `wander`: the title lockup over brush strokes, then the
figure walking through mist on paper in three overlapping panels, one a close-up of the hooded face,
one carrying narration. `profile`: the figure hears something and pulls back the hood, eyes unsure.
`approach`: the monolith under a hatched moon upper right, a long stair, a dark red disc at the base of
the slab, the figure seated at the bottom of the frame, one wide narration panel. `near`: the ground
turns from paper to blood as the figure approaches and the hum grows. `hand`: a life-size hand reaches
from the right across a red hatched field; the portal gate waits at its fingertips. `target`: the portal
fills the frame, rings expanding, the figure small and centred, one narration panel lower left, hatched
walls converging. `transition`: full-frame vertical hatching, dark domed silhouettes below and white
above. `cathedral`: red columns in two rows, the wide screen high on the far wall with the engraved eyes,
the altar with three bottles, light beams breathing. `drink-selection`: the figure beside the stone
pedestal with the three bottles; the figure picks up the bottle the visitor chose. `drink-pour`: the tilted bottle, the empty
coupe glass, the pour gate at the lip. `anti-gravity`: two stacked panels, the robed figure in the
flavour colour above and the wide close-up of the eyes below; the figure rises, sparks spawn and
release. `pillar-crumble`: shattered shafts against flat red, debris, one inset panel of the figure in
profile, two narration panels. `colosseum`: the paper-white colonnade, deep rows of columns, red
doorways, the figure walking away. `taste`: the promise chapter. `collection`: the poster. `products`:
the carousel and the data strip. `retail`: the ornament and `Select Houses Forthcoming`, or the nearest
venues. `footer`: the footer on ink. Chapter boundaries are overlaps where one chapter's contribution
falls as the next rises; the ground colour is a property of each chapter, never a global.

**Comic panels.** Six chapters compose in panels. A panel is a rectangle with the hand-drawn frame and a
slightly torn, deckled paper edge with a thin hatched shadow beneath. Panels enter by the *panel wipe*, opening
from fully inset to full size with the edge cutting the world, never by fading. Panels overlap and are
allowed to break the frame; most panel chapters have one crossing the window's edge. A narration box is
a white box with an ink border and heavy capitals, ranged left with a first-line indent, pinned to a
corner of its panel and allowed to overhang, never centred on it. Emphasis inside narration is blood
red, on `IMMENSE LAND` and on `BACK TO THE FLOOR`.

**Drawn type.** All display typography is drawn inside the film letter by letter from distance-field
fonts, so it stays sharp from thumbnail size to full frame and grows continuously. A run of text can
reveal per letter, per word or per line; its reveal position follows the story; a little per-letter
jitter keeps it from reading as a wipe; letters can be displaced as they arrive or masked into view; a
run can hold unrendered until its copy arrives; and narration boxes indent their first line. Where a
line is narrated, its words light in time with the voice: the *karaoke lighting*. With sound off,
karaoke drops away entirely and the words light from the story position instead, so no text ever
waits for a voice that is not coming. In the carousel, the flavour names either side of the centred one
sit a fixed distance away and slide across by that distance when the flavour changes.

**The hidden text.** Every drawn run has a counterpart in the page's own text, visually hidden rather
than removed, in story order, as headings and paragraphs. Narration is joined into continuous prose
rather than split into the drawn fragments: the poster's nine drawn lines are one sentence sequence,
`Chill your spirit. The night starts after dinner. Shake your spirit. Let the night play on. Pour your spirit. What happens next is up to you.`
The two held gates appear here as named controls. The header controls also carry the hidden names
`experience` and `collection`.

**The sound, bus by bus, as what is heard.** Three drones share the base level and a warm filtered
echo; a fourth routes through a sweeping resonant focus; a fifth sits at a tenth of the base level. The
jazz thread, brushed noise on a swung eighth-note grid with a muted three-note upright bass and
occasional damped piano tones, sits at just under half the drone level. Wind is pink noise through a
slowly drifting band. The portal base is two tones a fifth apart, beating slowly, with a metallic
ringing third; the portal movement layer is the same sound pushed well above everything else, its
beating and ringing driven by the drag, through a modulated echo; the portal contact is one sharp
resonant burst. The pour is filtered noise whose pitch rises as the glass fills, with short bubble
blips rising in pitch, and short start and stop transients. The ascent is an upward saw sweep for the
speed-up, bright blips for spawns and a falling sweep for the release, the spawns and releases panned to
the pointer and brought back up after heavy attenuation. The bottle tap is three high partials; the
levitation a slow glide; drinking three falling bursts; the interface click one short high sine tone with a hard envelope; the
crack white noise through a closing filter with a low thump. Every parameter change is smoothed just
enough to follow a gesture without clicking. Four frequency bands from low to high are measured from the
master output, the highest weighted most, and the level meter reads them.

**The collection act, as compositions.** The promise chapter: `INDULGE NOW` over `ATONE LATER`, cropped
by the top edge, with the compound arrow flourish left and right of the second line; three short lines
in heavy interface capitals across thirds, `THE NOCTURNE COLLECTION` over `IS AN ODE TO THE NIGHT` at the
left, `A TASTE` over `OF POSSIBILITY` in the centre and `INSPIRED BY THE QUIET GLAMOUR` over
`OF THE LATE HOURS` at the right; one justified paragraph in the light long-form face, centred at about a
third of the frame's width: `True devotion requires a little indulgence. Vesperi Spirits is crafted for
the saints and the sinners alike. The Nocturne Collection blends heavenly cream and earthly decadence to
unwind your soul and elevate your evenings.`; and four single words at the outer corners. The poster:
nine drawn lines set solid, `CHILL YOUR SPIRIT.`, `THE NIGHT STARTS`, `AFTER DINNER.`,
`SHAKE YOUR SPIRIT.`, `LET THE NIGHT`, `PLAY ON. POUR`, `YOUR SPIRIT. WHAT`, `HAPPENS NEXT`,
`IS UP TO YOU.`; side labels `THE NIGHT STARTS` over `AFTER DINNER` and `WHAT HAPPENS` over
`NEXT IS UP TO YOU`; and the subtitle `AN ODE TO THE NIGHT, YOUR NIGHT`. The chapter titles are paired
lockups split to opposite corners: `Vesperi` with `Spirits`, and `Nocturne` with `Collection`. The
bottle label reads `Chill your spirit,` over `shake your spirit,` over `pour your spirit.` in the
interface face, wrapped around the bottle and grained. The carousel's *slide and repour*: the names
travel sideways while the bottle turns in place and its liquid changes to the new tint. Hit areas are
named `previous slide`, `next slide`, `left text` and `right text`. The retail chapter's side labels are
`Vesperi Spirits` and `Nocturne Collection` in red.

**Narration, in story order.** The line breaks shown are art direction, not wrapping. Emphasised words
are blood red; everything else is ink; all narration is in heavy interface capitals.

`IN AN IMMENSE LAND OF NOTHINGNESS.` / `A LONELY FIGURE WANDERS THROUGH THE MIST.` (emphasis on
`IMMENSE LAND`)

`DISTANT WHISPERS ALERT THE TRAVELER. THE SAINT REMOVES HIS HOOD` / `TO LOOK AROUND EYES UNSURE AND FEARFUL.`

`AN OMINOUS STRUCTURE STANDS BEFORE THE SAINT. THE HUMMING SOUND SEEMS TO` / `COME FROM ITS DIRECTION. A
VIVID LIGHT SHINES THROUGH THE CIRCULAR PORTAL AT THE` / `BASE OF THE GREAT MONOLITH. NOT COMPLETELY
BELIEVING IT, THE SAINT PAUSES FOR A` / `MOMENT TO GET HIS SENSES BACK.`

`AS HE APPROACHES THE PORTAL, THE HOLY SOUND GROWS STRONGER,` / `CALLING HIM TO THE CORE.` /
`IT BEGINS TO PULSATE, INVITING HIM CLOSER.`

`INSTANTLY, HIS HAND DRAWS FORWARD.`

`THE SAINT GENTLY FLOATS BACK TO THE FLOOR, ONE FOOT AFTER THE OTHER. HIS ROBE` / `NOW SATURATED WITH THE
COLOR OF THE MYSTERIOUS LIQUID` (emphasis on `BACK TO THE FLOOR`)

`THE SUDDEN ROAR OF SHATTERING STONE FILLS THE AIR. THE COLUMNS AND ROOF BEGIN` / `BREAK APART AND LIFT
AWAY, REVEALING A DEEP RED SKY.` The missing word in `BEGIN BREAK APART` is reproduced exactly as
written; it is a copy decision, not a build one.

The prompts are `HOLD &` over `MOVE`, and `HOLD &` over `POUR`, in ink on a circular paper badge placed
at the point of contact rather than centred in the frame.

**Idle life.** Figures breathe and sway slightly on the clock while the story is still, each on its own
phase so two figures never breathe in step; the breathing fades out while the story is moving and
returns when it stops. It is the only clock-driven movement inside the film besides the stepped effects.

**Figure movement, a keyframe contract to adjust against the look.** The walk is a two-beat cycle with a
hip swing, an opposing shoulder and a small foot lift. The hood comes off with both hands and the head
lifts at the end. The reach extends the arm and spreads then curls the fingers, and holds at the portal
gate. The pour rotates the wrist from level to steeply tilted over the gesture. The float rises and
turns. The landing sets one foot then the other with a knee dip.

**The additions, component by component.**

- *The hold control.* Blood on paper in the heavy interface face, beneath the data strip. States:
  resting `KEEP THIS ONE`; pointed-at; pressed; focused; claiming, which shows work in progress and never
  a granted look; held, `YOURS FOR 72 HOURS`, arriving as the *cellar grant* on the settling character;
  waitlisted, `YOU ARE NUMBER {n} IN LINE`; closed, naming why; and unavailable offline, naming why in
  words. Unavailable is never signalled by colour alone.
- *The shelf.* The engraved stone ledge, bottles turning slowly on their own phases, arriving as the
  *shelf entrance* on the long-tailed character, matching the header's unroll so the shelf reads as part
  of the same furniture. Each bottle carries its flavour name, its state as a word and, only while
  expiring, a countdown in blood in the heavy interface face. An offer shows its twelve-hour window with
  accept and decline. An expired bottle says `IT WENT BACK. CLAIM ANOTHER`. A possibly stale shelf says
  so.
- *The venue plan.* Paper ground, ink line work, blood for venues holding the selected flavour, the
  small ornament as each venue mark, the drawn pointer as the visitor. Marks arrive nearest first a short
  beat apart; opening a venue moves the plan in on it over the age panel's pace, without changing page.
  The list beside it gives each venue's name, kind, distance in kilometres, reading as a word and hours.
  A stale reading reads `unknown` with `LAST SEEN {n} DAYS AGO`. The empty state is
  `NOTHING NEAR YOU YET` with widen and `TELL ME WHEN IT LANDS`. The restricted state is the notice and
  `WE CANNOT LIST HOUSES WHERE YOU ARE`. The place field lists every match and each match's detail.
- *The session picker.* Paper ground, ink type, labels in the heavy interface face at the small size and
  session detail in the long-form face. Each session shows its title, venue, date and time in the venue's
  zone with the visitor's own time beside it when different, seats remaining and price in dollars. A held
  session shows `SEATS HELD FOR {n}` in blood, counting down. The confirmation arrives on the long-tailed
  character and returns the visitor to the poster composition carrying the session. Full sessions read
  `FULL. JOIN THE LINE`. A late cancel reads `TOO LATE TO CANCEL. MOVE IT INSTEAD` with the move offered.
- *The ritual builder.* Blood ground, paper type. Steps: choose a bottle, add mixers, choose ice, choose a
  garnish, pour, name, save. The glass tints towards each ingredient as it is added. `NAME IT` leads the
  naming step. A refused name returns to naming with the reason and the build intact. The cooling-down
  state reads `ENOUGH FOR NOW. TRY AGAIN IN {n}`. The finished card uses the poster composition and
  arrives with the product's one overshoot. A shared page opens with `SOMEONE POURED THIS FOR YOU`; a gone
  one with `THAT ONE IS GONE. POUR YOUR OWN`.
- *Forms everywhere.* Fields have resting, focused, filled, invalid, disabled and validating states. An
  invalid field is named inline with the reason, what was typed is kept, and nothing is written. Escape
  closes the topmost transient surface. Every control reachable by pointer is reachable by keyboard in a
  sensible order.

**Voice and copy.** Imperative, short, second person, no exclamation marks, slightly stern, the same
register as the film. Every error names what failed, why and the one next action. Placeholders written
`{n}` are replaced by the number they stand for. The fixed strings of the additions are exactly
`KEEP THIS ONE`, `YOURS FOR 72 HOURS`, `YOU ARE NUMBER {n} IN LINE`,
`AN EMPTY SHELF IS A KIND OF PATIENCE`, `IT WENT BACK. CLAIM ANOTHER`, `NOTHING NEAR YOU YET`,
`TELL ME WHEN IT LANDS`, `WE CANNOT LIST HOUSES WHERE YOU ARE`, `LAST SEEN {n} DAYS AGO`,
`SEATS HELD FOR {n}`, `FULL. JOIN THE LINE`, `TOO LATE TO CANCEL. MOVE IT INSTEAD`, `NAME IT`,
`ENOUGH FOR NOW. TRY AGAIN IN {n}`, `SOMEONE POURED THIS FOR YOU`, `THAT ONE IS GONE. POUR YOUR OWN`, `THAT ALERT IS OFF` and `GO BACK`. The `{n}` in `SEATS HELD FOR {n}` is the time left as minutes and seconds, in `TRY AGAIN IN {n}` whole minutes, in `LAST SEEN {n} DAYS AGO` whole days, and in `YOU ARE NUMBER {n} IN LINE` the waitlist position.

**The plain surfaces.** The sign-in page, the host page, the terms page and the permission surface are single-column paper documents with ink type, the house mark at the top and the footer at the bottom; the sign-in page leads with its address field and send action, the host page with its reading controls, and the permission surface names what is required and offers a way back. Destructive actions, such as releasing a bottle, cancelling a booking, deleting a ritual or cancelling a session, ask for confirmation first and say what will happen. The cookie notice sits at the lower left, clear of the audio meter. On a handset held sideways the red flourish between the header words is dropped.

**Glossary of terms used in this brief.** The *story position* is the one number the film reads, and the story timeline is that number drawn out over the eighteen chapters. A *traverse* is
one pass of it from start to footer. A *chapter* is one of the eighteen compositions. A *held gate* is
a point where the story waits for a held gesture, and a *soft clamp* is the way it resists and springs
back rather than freezing. *Idle* is the short quiet after the last meaningful input. The *bed* is the
continuous drones, jazz and wind; a *one-shot* is a sound played once on an event. A *release* is a
finite numbered run of the bottle; an *allocation* is one unit of it; a *hold* is a time-limited claim
on an allocation or on seats; an *offer* is an allocation handed to the first waitlisted visitor; a
*stale* reading is one over seventy-two hours old; a *landing alert* is a standing request to be told
when a flavour reaches a venue within a chosen distance; the *cancellation window* is the forty-eight
hours before a session; a *ritual* is a saved, public serve; a *closed set* is a list the client can
never add to; the *empty state* is what a surface shows a visitor who has done nothing yet.

## Constraints

- Two roles only, `visitor` and `host`. No administrator surface, no venue onboarding, no host with
  more than one venue, no host signup: hosts exist only because they are seeded.
- No buying anything: no cart, no checkout, no payment provider, no prices other than a tasting's.
- No third-party analytics, no advertising pixels, no tracking beyond the cookie choice this brief
  asks for.
- No external network calls at run time: no geocoding, no map tiles, no routing, no fonts or scripts
  from another origin. Everything the product needs is built into it or in this environment.
- No shipped image, model, font atlas or sound file for the film; everything is generated as it runs.
- No authoring tools in the product: no font editor, no render statistics panel, no live surface
  editor, no save control for the film.
- No replay control; reverse travel is the replay.
- No chapters beyond the eighteen listed, and no chapter the visitor cannot reach.
- The age answer is never stored, on the server or in the browser.
- No native application. No offline mode beyond what the rules above describe: the last-known shelf,
  venue list and bookings render when the connection drops, and nothing that changes stock, seats or
  rituals is queued for later.
- No messaging, no comments, no reviews, no ratings, no social feed.
- The app stays responsive with at least 5,000 allocations, 2,000 venues, 1,000 tasting sessions and
  10,000 rituals stored.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses.
  Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**Environment variables the app reads.** `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`; `DATABASE_URL` for
PostgreSQL; and `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS` for Mailpit. Mailpit takes no
authentication, so `SMTP_USER` and `SMTP_PASS` may be empty. There are no others.

**API shapes.** Field names are exact. A successful call returns the named resource or shape, and a
list endpoint returns a top-level JSON array unless the table shows a wrapping object. An invalid,
unauthenticated or unauthorized call is rejected as a client error, never as a server error and never as
a silent success, and its body is `{"reason": "...", "message": "..."}` plus any extra field named
below, where `reason` is one of the stable strings this brief names and `message` is a sentence a person
can read and the interface shows. Every instant in a request or response, such as `expiresAt`, `offerExpiresAt`, `startsAt`, `opensAt`, `closesAt`, `updatedAt`, `createdAt` and `decidedAt`, is an ISO 8601 string in UTC ending in `Z`. Every call except the ones marked public carries the bearer token.

| Endpoint | Request body or query | Returns |
|---|---|---|
| `GET /api/health` | none | `{status, checks}` (public) |
| `POST /api/auth/login` | `{email, password}` | `{access_token, expiresAt, user}` (public) |
| `POST /api/auth/logout` | none | no content |
| `POST /api/v1/auth/link` | `{email, returnTo}` | `202`, `{sent}` (public) |
| `POST /api/v1/auth/session` | `{token}` | `{session, expiresAt, user}` (public) |
| `GET /api/v1/me` | none | `{id, email, role, displayName, venueId}` |
| `GET /api/v1/content` | none | `{releases, flavours, chapters, credits, legal}` (public) |
| `GET /api/v1/releases` | none | releases with `claimed` and `remaining` (public) |
| `GET /api/v1/releases/{releaseId}` | none | `{id, name, total, claimed, remaining, opensAt, closesAt}` (public) |
| `GET /api/v1/cellar` | none | `{items: [{allocationId, releaseId, flavour, state, expiresAt, position, offerExpiresAt}]}` |
| `POST /api/v1/cellar/holds` | `{releaseId, flavour}`, optional `Idempotency-Key` header | `201` item, or `409` `{reason: "exhausted", position}` |
| `DELETE /api/v1/cellar/holds/{allocationId}` | none | `204` |
| `POST /api/v1/cellar/holds/{allocationId}/confirm` | none | item in `confirmed` |
| `POST /api/v1/cellar/holds/{allocationId}/accept` | none | item in `held` |
| `POST /api/v1/cellar/holds/{allocationId}/decline` | none | item in `declined` |
| `GET /api/v1/places` | `?q=` | `[{id, name, detail, regionCode, lat, lng}]` (public) |
| `GET /api/v1/regions/{code}` | none | `{code, name, listingAllowed, ageFloor, notice}` (public) |
| `GET /api/v1/venues` | `?lat=&lng=&radius=&flavour=` | `{region, venues: [{id, name, kind, distance, stock, updatedAt, hours}]}` (public) |
| `GET /api/v1/venues/{id}` | none | venue with `address`, `hours`, `timezone` and per-flavour `stock` (public) |
| `PUT /api/v1/venues/{id}/stock` | `{flavour, reading}` | `{flavour, reading, updatedAt}` (host of that venue) |
| `GET /api/v1/host/venue` | none | the host's venue with readings and sessions (host) |
| `POST /api/v1/alerts` | `{place, radius, flavour}` | `201` `{id, place, radius, flavour, state}` |
| `GET /api/v1/alerts` | none | the visitor's alerts |
| `DELETE /api/v1/alerts/{id}` | none | `204` |
| `GET /api/v1/tastings` | `?venue=&from=&to=` | `[{id, venueId, venueName, title, startsAt, timezone, capacity, remaining, price, currency, state}]` (public) |
| `POST /api/v1/tastings/{id}/holds` | `{partySize}` | `201` `{holdId, expiresAt}`, or `409` `{reason: "insufficient", remaining}` |
| `DELETE /api/v1/tastings/holds/{holdId}` | none | `204` |
| `POST /api/v1/tastings/{id}/waitlist` | `{partySize}` | `201` `{position}` |
| `POST /api/v1/tastings/{id}/cancel` | none | session in `cancelled` (host of that venue) |
| `POST /api/v1/bookings` | `{holdId, name, email, notes}`, optional `Idempotency-Key` header | `201` `{id, sessionId, partySize, state, name, email}` |
| `GET /api/v1/bookings` | none | the visitor's bookings |
| `DELETE /api/v1/bookings/{id}` | none | `204`, or `409` `{reason: "late"}` |
| `POST /api/v1/bookings/{id}/reschedule` | `{sessionId}` | the moved booking |
| `GET /api/v1/ingredients` | none | `{mixers, ices, garnishes}` (public) |
| `POST /api/v1/rituals` | `{flavour, mixers, ice, garnish, name}`, optional `Idempotency-Key` header | `201` `{slug}`, or `429` `{reason: "rate_limited", cooldownSeconds}` |
| `GET /api/v1/rituals/{slug}` | none | `{slug, name, flavour, mixers, ice, garnish, createdAt}`, or `404` (public) |
| `PATCH /api/v1/rituals/{slug}` | `{flavour, mixers, ice, garnish, name}` | the ritual (owner) |
| `DELETE /api/v1/rituals/{slug}` | none | `204` (owner) |
| `POST /api/v1/cookie-choice` | `{nonEssentialAccepted}` | `{visitorToken, nonEssentialAccepted, decidedAt}` (public) |
| `GET /api/v1/cookie-choice` | none | the recorded choice for this browser (public) |

The stable `reason` strings this brief names are `invalid_token`, `invalid_flavour`, `closed`,
`already_held`, `exhausted`, `not_offered`, `invalid_radius`, `restricted`, `invalid_party_size`,
`insufficient`, `hold_elsewhere`, `expired`, `late`, `already_rescheduled`, `too_many_mixers`,
`invalid_ingredient`, `invalid_name`, `name_refused`, `rate_limited`, `edit_window_closed`, `invalid_credentials`, `invalid_reading`, `session_started`, `unauthenticated`, `forbidden`, `not_found`, `invalid_place`, `invalid_request` and `not_full`. A call without a valid session answers `unauthenticated`; a call the caller's role or ownership does not allow answers `forbidden`; a missing row answers `not_found`; an unknown place id answers `invalid_place`; any other malformed body answers `invalid_request`. A call without a valid session, and a sign-in with wrong credentials, answer `401`; a call the caller's role or ownership does not allow answers `403`; a missing row answers `404`; every other refusal answers `400`, `409` or `422` as the rules above say, `409` wherever a rule names it.

**No stand-ins.** PostgreSQL is where this product's records live and Mailpit is where its messages
go. Any of the following is a contract violation however good the interface looks: an allocation
count kept in memory, a shelf or booking kept only in the browser, a sign-in code shown on screen
instead of sent, a confirmation the app reports as sent without a real message reaching Mailpit, a
stock reading computed in the browser, a ritual rendered from data the browser invented, or a hold
granted by the interface before the server granted it. The named provider is the fact, and the app's
own screens can only reflect what lives in PostgreSQL and Mailpit, never substitute for it.

## Definition of done

A visitor confirms their age, drives the woodcut film through both held gestures, picks a flavour, reads every bottle's tasting notes with `13% ABV` and `700 ML`, and runs the story back to its first frame. They keep a bottle after a mailed sign-in link, set an alert a venue update fires, and book a tasting confirmed by mail. The last bottle and the last seats never go to two people.
