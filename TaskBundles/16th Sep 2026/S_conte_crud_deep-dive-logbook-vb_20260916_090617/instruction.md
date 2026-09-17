# Sounding

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
enter the dive, sink to the works scene, save that moment, create an account, save two
more, reorder them, write a note, publish the logbook, and open the resulting address
in a browser that has never signed in, without hitting an error page. A different
stranger, signed in as another account, must NOT be able to read that logbook before it
is published, by any means, including a direct request for its address. The order the
diver left the rows in has to be a real order held by the service: it survives a reload, a
new tab and a restart, and an order the page remembers to itself does not count.

## Overview

Sounding is the portfolio of Ines Marlow, a creative software engineer who builds
three-dimensional work for the web, and it is built as the thing it advertises. The whole
product is one address that never navigates and never scrolls, inside which a visitor
sinks through six underwater scenes in a fixed order: a surface, an introduction, an
about, a works gallery, a four-panel message and a contact deck. There is no menu. There
is a wheel, a mark down the right edge, and a direction: down.

Three audiences: a studio asking whether this person can actually build it, a client who
wants scope and prior work, and a peer who wants to know how it was made. Every audience
gets the same one address.

The dive alone leaves one thing unanswered. A visitor sinks past a moment they liked and
has no way to keep it: there is no page to bookmark and no scroll position to send. So a
signed-in visitor keeps a logbook. They save any moment of the dive, write a note on it,
put the entries in their own order, and publish the whole thing as one link they attach
to an enquiry. A saved moment is not a picture. It is the scene it was taken in and how
deep the dive had travelled, so opening an entry returns the live dive to that exact
point.

It deliberately is not a content management system. There is no search box, no contact
form, no second logbook, no rich text, no notification centre, no theme switcher and no
admin console. Nothing is bought or sold and there is no currency anywhere.

The genuinely hard part is order and disclosure. A logbook's order is written as one
whole list rather than as a set of index updates, and it has to come back the way the
diver left it. And publishing is the only act that shares: a draft is readable by its
owner and by nobody else, including the portfolio owner whose site it is.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `diver` | Experience the whole dive, read any published logbook, keep exactly one logbook of their own, save a moment to it, annotate an entry, reorder entries, remove an entry, rename the logbook, publish it, unpublish it, and delete it | **Cannot read any other diver's logbook, published or not, through their own logbook route. Cannot read the dock queue. Cannot mark a logbook answered. Cannot read a draft logbook belonging to somebody else by its address.** |
| `host` | Everything a `diver` can do with their own logbook, and additionally: read the queue of published logbooks, open any published or answered logbook from it, mark one answered, and read the page view record | **Cannot read any logbook that is still a draft, including by its address and including their own site's. Cannot edit, reorder or remove another diver's entry. Cannot publish or unpublish another diver's logbook. Cannot delete anything a diver wrote.** |

A visitor with no account at all experiences the whole dive and reads any published
logbook. That is not a role and it grants nothing else. The table above is the whole
capability matrix; there is no other permission anywhere in the product.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a control in
the UI is not authorization: a direct API call from a `diver` session to any `host`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

The logbook a request acts on is resolved from the session and never from a parameter.
No diver-facing API path carries a logbook identifier, so there is no number for a diver to
change on any write.

A host asking for a draft logbook is answered as a missing record rather than as a
refusal, because a refusal confirms the draft exists, and an unpublished logbook is
somebody still thinking.

Signup is **open**. Anyone can create an account with an email address, a display name and
a password from `/sign-in?mode=create`, and the account is usable at once with no
verification step. Every account is a `diver`. The `host` role is assigned where the
accounts are and no route grants it.

Three accounts are seeded, and every seeded account uses the password
`deku-demo-pw-2026`.

| Email | Display name | Role | Their logbook |
|---|---|---|---|
| `host@example.com` | Ines Marlow | `host` | `Untitled dive`, state `empty`, no entries |
| `diver@example.com` | Coral Bevan | `diver` | `Reef pitch`, state `published`, four entries |
| `diver2@example.com` | Toma Oyelaran | `diver` | `Untitled dive`, state `draft`, two entries |

`diver2@example.com` exists so that isolation is observable: its draft logbook must read
as missing to the host and as forbidden to `diver@example.com`.
## Core features

### The logbook

Every account has exactly one logbook, created with the account, and there is no logbook
list, no create control and no default to choose. A logbook has a title, a state, and
between zero and twelve entries in an order its owner controls.

| State | Meaning |
|---|---|
| `empty` | The account exists and nothing is saved. Becomes `draft` on the first save |
| `draft` | Being built, and private to its owner |
| `published` | Readable by anybody holding its address, and in the dock queue |
| `answered` | The portfolio owner has picked it up |

The title defaults to `Untitled dive` and is between `1` and `80` characters after
trimming. It may be cleared while the logbook is a `draft`, because a diver renaming one
empties the field before typing; publishing is where a blank title is refused. An entry carries the scene it was taken in, how deep the dive had travelled as a
number from `0` to `1`, its position in the order, and an optional note of at most `280`
characters. Twelve entries is the ceiling and the thirteenth save is refused.

Only a logbook in `draft` accepts a write. Every other mutating request against it is
rejected as a conflict, and the surface reconciles to read-only rather than retrying.

A published logbook can be unpublished by its owner, which returns it to `draft`, removes
it from the queue, and makes its public address answer not found. A logbook that has been
answered can still be unpublished, and the answer is not undone.

### Saving a moment

A save control sits at the bottom left of the dive reading `[Log this moment]`. It
captures three things: the scene index the dive is in, the interpolated dive position as a
number from `0` to `1`, and the instant. It captures no image.

After a successful save the control reads `[Logged]` for two seconds and the new row is
appended at the end of the order. Saving while the logbook already holds twelve entries
changes nothing and puts `[Logbook full]` in the message strip.

Activating it while signed out opens `/sign-in` with `next` carrying the current depth and
the moment held. When the account is created or the sign-in succeeds, the held moment is
written and the dive resumes at the depth `next` named. The visitor never has to find the
moment again.

### Ordering entries

A row is reorderable three ways and all three produce the same write: dragging its index
cell with a pointer, dragging it after a long press on touch, and focusing the index cell
and pressing the up or down arrow, which moves it one position per press.

**The write is one ordered list of entry identifiers, not a set of index updates.** The
service rewrites each entry's position from that list's index. A partial reorder therefore
cannot leave a gap or a duplicate, and two tabs racing resolve as one winner on the whole
list rather than interleaving into an order neither asked for.

Positions are always `0` to one less than the entry count, contiguous and unique. Removing
an entry closes the gap.

A reorder is applied on screen at once and confirmed afterwards. If the write fails the
row travels back to the server's position and `[Could not reorder]` appears in the strip.

### Notes and renaming

A note autosaves when its field loses focus or after `800` milliseconds idle, whichever
comes first. A rename is written the same way. Both are applied on screen at
once.

If either write fails, **the field's value is left exactly as the diver typed it**,
`[Not saved]` appears in the strip with a `retry` control, and nothing is reverted. No
correctness argument justifies replacing text somebody is looking at with an older
version of it.

### Publishing and the public address

Publishing is checked in this order and stops at the first failure.

| # | Rule | The message |
|---|---|---|
| 1 | At least one entry | `Log at least one moment` |
| 2 | At most twelve entries | `A logbook holds twelve moments at most` |
| 3 | A title of `1` to `80` characters after trimming | `Give the logbook a name` |
| 4 | Every note at most `280` characters | `A note is too long` |
| 5 | Every entry's scene is one the dive still has | `One of your moments is no longer in the dive` |
| 6 | The logbook is in `draft` | `This logbook is already published` |

On a pass the logbook becomes `published`, the publish instant is written, and a public
address is minted and shown with a `copy` control. The public identifier is at least `128`
bits of entropy from a cryptographically secure source, encoded URL-safe, unrelated to the
logbook's own identifier, to the diver and to the publish time.

**It is minted once and is stable across unpublish and republish.** A diver who takes a
logbook down to fix a note and puts it back up must not invalidate a link they already
sent.

Publishing and unpublishing are never applied optimistically, because each changes what
somebody else can see. Everything a diver can undo alone is applied at once and confirmed
afterwards.

A published logbook renders at its address for anybody, including a visitor with no
account, identically for all three kinds of reader: every row, every note, the title and
the diver's display name, and nothing else about the diver. It is read-only for everybody
including its owner.

### Real-time behaviour, and what is applied at once

Almost nothing here updates by itself, and that is correct: the dive is a program that runs
on the visitor's own machine rather than a feed. There is no real-time channel anywhere in
this product. The dock queue is the one surface that refreshes on its own, once a minute,
and it stops entirely while the document is hidden. A published logbook is not refreshed at
all, because it is read-only for everybody including its owner, and a diver's own logbook
is not either, because one logbook has one owner.

The line between what happens at once and what waits is: anything the diver could undo
alone appears immediately and is confirmed afterwards, and anything that changes what
somebody else can see waits for the service. Saving a moment, removing an entry,
reordering, renaming and writing a note are the first kind. Publishing, unpublishing,
marking answered and signing in or out are the second kind, and identity is never guessed.

When an optimistic change turns out to have failed it is undone visibly, at the speed it
happened, with a message in the strip and never a dialog. The one exception is text: a
failed note or title write leaves the field exactly as it was typed.

Reconciliation, when two tabs disagree: the service's ordering wins and the diver's text
wins. Two tabs that reordered the same logbook resolve to whichever order was written last,
because the write is one whole list, and the losing tab's next read shows the winner. Two
tabs that edited different fields both survive. A publish against an already-published
logbook is a conflict and the surface reconciles to read-only. Offline writes replayed
against a published logbook are dropped and the strip says so once rather than once per
write.

### Sorting and filtering

There is no search box anywhere in this product, and none is to be added: one address, six
scenes and four projects. A search that always returns everything is furniture.

Nothing is sortable by a visitor. The scene order is the argument the site is making, and a
sort control over it would be a control for destroying that argument. Projects are in their
authored order, the dock queue is in publish order newest first, and a logbook's entries are
in the diver's own order and can be resorted only by its owner. The dock's filtering is the
only filter in the product: one state or the other, never both, because the two states are
exclusive by definition. A logbook is never filtered, because twelve rows do not need one.

### Replay

Every entry carries a control reading `Dive to this`. Activating it places the dive at that
entry's scene and depth immediately, without animating the journey there, and it works
from a cold load of a public address as well as from inside a running dive.

The cold-load case is the one to get right: opening a shared logbook and activating an
entry must load the dive and arrive, in one action, without the visitor first watching the
introduction.

### The dock

The portfolio owner reads a queue of published logbooks at `/dock`, newest published
first, beside the one currently open. Each row carries the diver's display name, the
logbook title clipped to one line, the entry count and the published date written
`DD/MM/YY`. The queue filters to `published` or to `answered`, one or the other, and pages
by cursor rather than by offset, because new logbooks arrive at the top and an offset
second page would repeat rows.

Opening one and activating `Mark answered` sets the state to `answered` and writes the
instant. The diver's own logbook then carries a persistent `[Received]` notice above the
entries, which stays until the logbook is unpublished. It is a state rather than an alert,
so it does not dismiss.

The queue refreshes itself once a minute and stops entirely while the document is hidden.

### Identity

Email and password. `/sign-in` carries four modes in one surface, switching by rewriting
the query without navigating: sign in, create with an extra display-name field, request a
reset, and set a new password from a token.

A reset request always shows the same success surface whether or not the address is
registered, and a message is sent only when it is. Returning "no such account" would turn
the form into a way of asking who has an account here. The reset link is single use, lives
`60` minutes, and issuing a new one invalidates every earlier one for that address.
Setting a password destroys every session for that account and signs the diver in fresh.

A signed-in diver stays signed in across a reload, a new tab and a browser restart, and
signing out anywhere signs out everywhere.

### Messages

Four messages are sent by mail and no others.

| Trigger | To | Subject |
|---|---|---|
| An account is created | the new diver | `Sounding: your logbook` |
| A reset is requested for a registered address | that diver | `Sounding: reset your password` |
| A logbook becomes `published` | its diver | `Sounding: your logbook is live` |
| A logbook becomes `published` | `host@example.com` | `New logbook from ` followed by the diver's display name |

The published message carries the public address, because that address is the whole
product of the feature and the diver needs it somewhere durable. No other state change
sends anything: unpublishing sends nothing, marking answered sends nothing, reordering
sends nothing and signing in sends nothing. No message ever carries a note's text.

### The dive

Six scenes in a fixed order, indices `0` to `5`: `surface`, `introduction`, `about`,
`works`, `message`, `contact`. The page is exactly one viewport tall at every width, never
grows, and never exposes a native scroll.

**One number decides which scene is showing and every consumer reads that one number.**
The gesture writes a target; the dive chases that target by interpolation, closing a
fraction of the remaining distance every frame; and the scene text, the depth mark, the camera, the water
and the save control all read the chased value. Nothing reads the gesture directly. A
violent gesture moves the target a long way and the dive still travels at its own rate,
which is the entire feeling of the product.

Wheel and touch are tuned independently and the touch axis is inverted relative to the
wheel axis, because dragging a finger up the screen should take the visitor down. The
sensitivities change at the main breakpoint and are recomputed when the window crosses it.
Events originating on the depth mark itself are ignored by the gesture handler, so
dragging the mark does not also drive the dive.

The sequence does not wrap. Gesturing up at the surface leaves the dive at the surface and
gesturing down at the last scene leaves it at the last scene. The dive ends on an address
and does not return to the top.

The three header words jump the dive to the works, message and contact depths, travelling
there at the normal rate rather than cutting. A deep link parameter named `at`, a number
from `0` to `1`, places the dive at that depth on first paint; anything unparseable is
treated as absent and anything outside the range is clamped rather than refused, because a
value outside it is far more likely to be a truncated link than an attack.

The depth is written into the address only when a moment is logged or an entry is
replayed, replacing the history entry rather than pushing one. Writing it as the dive
moves would flood the history and destroy the back button.

Reloading returns the visitor to the surface rather than to where they were. This is a
narrative, and landing somebody in the middle of one with no idea how they got there is
worse than starting again. The deep link exists for when it is meant.

### The entry gate

The experience does not begin without an explicit gesture. A loading surface shows a
progress meter, and when loading completes it offers two controls: `Dive into the
experience`, which starts audio, and `Enter without audio`, which does not. Both enter and
they differ in exactly one respect. Audio never starts anywhere else.

### Works

Four projects live in the works scene, each with a title, a one-line description, a
slash-separated skills line and an outbound link. While the works layer is open the
gesture steps rather than glides: one ordinary gesture moves exactly one project, and a
touch swipe counts for three times its normal weight so that one swipe is still one step.
Gliding through a list of four things makes it impossible to land on the one you wanted.

Opening a project raises a detail surface over the dive, and while it is open the gesture
stops driving the dive completely.

`/works` enters the dive already at the works depth with the works layer open.

### The message scene

Four panels occupy the same rectangle and exactly one is readable at a time. Advancing is
a press and hold: a ring fills around its edge while the hold continues and drains
steadily on release rather than resetting, so getting through requires sustained intent
while briefly lifting a finger costs nothing.

A keyboard path advances one panel per press with no sustained press. It is required, not
optional, because the hold is otherwise the only route through the scene.

### Errors, refusals and the cookie choice

An unknown address renders the product's own not-found surface, with a way back to the
surface, and answers as not found rather than as anything else. A signed-in diver asking
for a logbook that is not theirs stays where they are and is told, with the address
unchanged, rather than being bounced somewhere else.

A first-time visitor is asked once, after the gate and never before it, for consent to
non-essential measurement. The consent answer survives a reload and a new tab, and nothing
is measured before it is recorded. Refusing
costs the visitor nothing: the dive, the logbook, publishing and the dock all work
identically either way. The question is asked in the message strip rather than in a dialog
and it does not block the dive.

### The page view record

Every page view is recorded with the route it was for and the instant it was served, and
that record is readable by the host and by nobody else. It is never keyed to a person, and
a logbook's public address never appears in it.

### The message strip

One thin strip along the bottom edge carries every transient message, one at a time,
dwelling five seconds, and a second message replaces the first rather than stacking under
it. Its whole vocabulary: `[Could not reorder]`, `[Could not log that]`, `[Not saved]`
with a `retry` control, `[Logbook full]`, `[Some changes were not saved]`, `[Removed]`,
`[Unpublished. The link is dead]`, `[Link copied]`, and `[Offline]`, which persists rather
than dwelling.

With the network gone the dive carries on perfectly, because once it has loaded it needs
no network at all. Logbook edits made while offline keep their value in the field and are
replayed in order when the connection returns; a publish attempted while offline is
blocked before the request rather than half made.
## User flow

### Routes

| Route | What it is |
|---|---|
| `/` | The dive. Six scenes, one screen, no scroll. Accepts `at` |
| `/works` | The dive entered at the works depth with the works layer already open. Accepts `at` |
| `/sign-in` | Identity. Accepts `mode`, `next` and `token` |
| `/logbook` | The signed-in diver's own logbook |
| `/logbook/<publicId>` | A published logbook by its public identifier, readable with no account |
| `/logbook/<id>` | A logbook by its own identifier, which only its owner can read while it is a draft |
| `/dock` | The host's queue beside the logbook currently open. Accepts `state` |
| anything else | The product's own not-found surface |

| Parameter | Route | Values | Absent means |
|---|---|---|---|
| `mode` | `/sign-in` | `create`, `reset`, `set` | sign in |
| `next` | `/sign-in` | a path beginning with a single `/` and not with `//` | `/` |
| `token` | `/sign-in` with `mode=set` | a single-use reset token | invalid |
| `at` | `/` and `/works` | a number from `0` to `1`, clamped | start at the surface |
| `state` | `/dock` | `published` or `answered` | `published` |

The three header words are the only navigation the dive has. They stay three words at
every width and never collapse into a menu.

### Entry and redirects

| Route | Visitor | Diver | Host |
|---|---|---|---|
| `/` and `/works` | renders | renders, with the save control | renders, with the save control |
| `/sign-in` | renders | redirect to `/logbook` | redirect to `/dock` |
| `/logbook` | renders the signed-out surface | renders their own | renders their own |
| `/logbook/<publicId>`, published or answered | renders read-only | renders read-only | renders read-only |
| `/logbook/<publicId>`, draft | not found | not found | not found |
| `/logbook/<id>`, draft, theirs | redirect to `/sign-in` with `next` | renders read-only | not found |
| `/logbook/<id>`, draft, somebody else's | redirect to `/sign-in` with `next` | forbidden | not found |
| `/dock` | redirect to `/sign-in?next=/dock` | forbidden | renders the queue |
| anything else | not found | not found | not found |

A gated route redirects and a forbidden route renders. If signing in might legitimately
grant access, the visitor is sent to sign in and brought back by `next`; if they are
already signed in and still not allowed, the refusal renders where they are with the
address unchanged, because being bounced elsewhere reads as a typing mistake.

`next` is validated as a path. It must begin with a single `/` and must not begin with
`//`. Anything else becomes `/`.

### Journeys

**A visitor takes the dive.** They open `/` and the loader fills. The gate offers two ways
in and they choose to enter without audio. The surface scene carries the name across the
top and one line along the bottom telling them to descend. They gesture, and sink through
the introduction, the about, the works, the message and the contact deck, which ends on an
address. Gesturing further leaves them at the bottom.

**A visitor saves a moment and becomes a diver.** Level with a project in the works scene
they activate `[Log this moment]`. They are not signed in, so `/sign-in` opens with `next`
carrying the current depth. They switch to create, give a display name, an email and a
password, and submit. The session is established, the held moment is written as the first
entry of a logbook that moves from `empty` to `draft`, and the dive resumes at the depth
`next` named with the control reading `[Logged]`.

**A diver builds and publishes a logbook.** They save two more moments, open `/logbook`,
and find three rows in save order under `Untitled dive`. They rename it to `Pitch dive`.
They focus the third row's index cell and press the up arrow twice, and the row moves to
the top. They reload, and the order is still theirs. They write a note on the first row and
click away. They activate `Publish`, validation passes, and a public address appears with a
`copy` control.

**A stranger reads a published logbook.** With no account and no cookies they open that
address and read the title, the diver's display name, and every row with its scene, its
depth and its note. They activate `Dive to this` on the first row and the dive opens at
that entry's scene and depth.

**The host answers.** They sign in, are taken to `/dock`, and find `Pitch dive` at the top
of the queue. They open it beside the queue and activate `Mark answered`. The diver's own
logbook now carries `[Received]`. The diver activates `Unpublish`, the strip says
`[Unpublished. The link is dead]`, and the public address answers not found.

**A refusal.** `diver@example.com` signs in and opens `/dock`, and is told
`This logbook belongs to someone else` without moving. The same diver asks for
`Toma Oyelaran`'s draft logbook by its own identifier and is told the same thing. The host
asks for that draft by the same identifier and is told `That address does not exist`, and
the host's own queue carries `Reef pitch` and no row from `Toma Oyelaran`.

### States

| Surface | Loading | Empty | Error |
|---|---|---|---|
| The dive | the slash meter and the spinner | not reachable | `[Signal lost]`, with `try again` and no water |
| `/logbook` entries | skeleton rows the size of the row they replace | `[Empty log]`, `Nothing logged yet`, `back to the dive` | `[Signal lost]`, `Could not load this`, `try again` |
| `/logbook` signed out | none | `[No log]`, `Sign in to keep a logbook`, `sign in` | the same error block |
| A published logbook | skeleton rows | not reachable; a published logbook has at least one entry | the same error block |
| `/dock` | skeleton rows | `[Quiet]`, `No logbooks published yet`, no control | the same error block |

Offline is checked first, then loading, then error, then empty, and a surface never shows
two at once.

A machine with no usable graphics is **not** an error state and must never be presented as
one. The dive drops to a single still frame, the whole text of the site works normally, and
the visitor is told nothing, because nothing is wrong from their point of view.
## UI/UX notes

A visitor should understand within one screen that they are inside an instrument rather
than on a page, and that the only direction is down. The register is atmospheric rather
than operational: the water is seen first and almost nothing else is on screen at any
moment. Where a judgement is close, the tiebreak is that this product is a demonstration
of craft and the interface is instrumentation bolted to the window it is seen through.

**Two palettes that never mix.** The interface has five colours. The ground is a
near-black cool neutral and it is every surface, the loader's ground and the water's own
empty colour, which is why the loader dissolves into the scene with no seam. The ink is a
near-white neutral at full strength and it carries every primary word. Secondary copy is
the same near-white neutral one step quieter. The signal is a mid, vivid orange and it is
spent exactly once on the whole site; if a second thing needs emphasis it takes the ink at
full strength against the quieter ink around it. The void is a near-black neutral used
only inside a transparency. Three transparencies of the ink do the rest: a mark at half,
which is something the site draws to inform you and must stay legible over water; a state
at just under a third, which is something switched off and never carries text; and a
hairline at a tenth, which is every rule and every field ground. One shadow exists, the
void at a quarter.

The scene palette lives only inside the water and never touches an interface element: a
deep, soft teal as the water's own hue and the near end of the fog, a mid, muted cyan for
mid water, a mid cool neutral for deep water, a light cool neutral for silt and drifting
particulate, a mid, vivid cyan for caustics, a mid, muted red for rust, a near-white,
muted orange and a near-white warm neutral and a light, soft orange for anything that
emits, and a near-black neutral for occluded interiors. A mid neutral is recorded and not
used. No deep, soft green appears anywhere: a value of that kind in the source material is
a leftover default rather than a palette entry.

**Typography, and the scaling behind it.** Every size below is a multiple of one root
size, and the scaling of that root is tied continuously to the window width between a
laptop width and a large-monitor width, stopping outside both. Below the laptop width
nothing scales at all, which is why a phone and a tablet get identical text. Do not
implement this as a set of breakpoint font sizes.

`Inter` at weights 300 to 900 carries anything the site says:
titles, sentences, quotations. `IBM Plex Mono` at 400 carries anything the site reports:
labels, counters, statuses, credits. The steps are `2em` display, `2.1em` lead for the
introduction sentence alone, `1.55em` subhead, `1.4em` body, `1.25em` body small, `1em`
base, `0.8em` label, `0.7em` label small and `0.6em` micro, every one a multiple of a root
size tied to the window width rather than set per breakpoint. Line height is `1` at the
display steps and `1.5` at base and label. Every monospace run is uppercase, tracked and
bracketed, and the brackets are content rather than decoration. One exception: a form
field is monospace and is not uppercased, because an email address in capitals is hostile.
The fallback stacks are `Inter, "Helvetica Neue", Arial, system-ui, sans-serif` and
`"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace`, and each is chosen for
metric similarity to the face in front of it. The monospace fallback matters more than
usual: the loading meter is a character count fitted to a width, so a fallback with a
different advance changes the meter's length.

**Almost nothing moves, and what does, fades.** The entire transition vocabulary is
opacity: a scene layer is present, laid out, and at zero. Exactly one element visibly
travels and it is the depth mark down the right edge. Four motion characters, each with a
job: a workhorse that is slow in and hard out, for something arriving or leaving on its
own; a replacement that holds at both ends and moves almost instantly between, used only
when one thing replaces another, which here means a scene change; an answer that
overshoots and settles, reserved for something a visitor pressed; and one plain quick
curve for a colour change on hover. Scene text does not animate in: it is hidden until it
is ready and then it is there, and it is restored even if whatever prepares it fails.

The scene change drives the water rather than the reverse. The distortion surges hardest
exactly halfway through a transition and returns to nothing at both ends, so it is
strongest at the moment neither scene is legible and it hides the crossfade.

**Reduced motion** stops everything that plays on its own and keeps everything that
answers a gesture. The water, the spinner, the pulse and the camera travel hold still and
the dive cuts between scenes instead of swimming; scene text is applied at once. The
unlock ring, the depth mark, the audio bars and the announcements continue, because each
is a readout of something the visitor is doing. The drawn pointer is the explicit
exception: it is removed entirely and the system pointer restored, because a pointer that
trails behind the hand is exactly the class of motion that causes discomfort and a frozen
one is a broken one. Vestibular safety is the reason the whole policy exists, and the dive
stays completable under it.

**The pointer.** The browser's pointer is hidden from the moment the dive starts and the
site draws its own, tracking at the display's refresh rate, never lagging far enough to be
lost, and showing two states: over water, and over something activatable. The site follows
the pointer twice and the two jobs stay separate: one chase draws the site's pointer, and
a second value, the pointer's velocity, is derived from the difference between consecutive
smoothed positions and smoothed again, and it is that velocity which feeds the water's
local distortion. Collapse them and the water stops
responding to gesture. Whenever a surface with a text field is open the system pointer is
restored, because caret placement depends on the real pointer's hotspot being where the
visitor believes it is.

**Shape and spacing.** The gutter is the same at every width and only the type inside it
grows, which is what makes the interface read as instrumentation rather than as a page.
Two radii exist and nothing else is rounded: the depth mark is a full round and the audio
control is a circle. Every panel, every field and every rule is square. Rows are separated
by a hairline; there is no card, no ground and no radius on any list surface.

**Accessibility, with numbers, because these are requirements.** Against the ground the
ink is about 18:1, the secondary near-white about 11.6:1, the signal about 8.2:1, the ink
at 60 percent about 6.6:1 and the mark about 4.9:1, and those carry text. The state colour
is about 2.6:1, carries nothing readable, and is a hairline and a ground only, so a
disabled control keeps the mark colour for its text and signals its state by the spinner
replacing its label. Body text and its background meet the WCAG AA contrast bar on every
surface. The difference-blended introduction sentence is a stated exception with its
reason: by construction it can never approach its background, it cannot be measured, and
it must not be "fixed" with a scrim.

Every focusable element has a visible focus treatment distinguishable from its hover
treatment and nothing removes focus visibility without replacing it. That carries more
weight here than usual, because a visitor who loses the drawn pointer has no system
pointer to fall back on and focus is the only remaining position indicator. Keyboard
navigation reaches every control: page down and page up descend and ascend one scene per
press, left and right step a project while works is open, enter or space advances a
message panel, and escape closes a panel. Scene layers that are not current are removed
from the tab order entirely rather than merely faded, because five invisible scenes' worth
of links in the tab order is the worst thing this architecture could do. One polite live
region announces a scene change, loading progress at quarters only, a row's new position,
the strip's text once, and a publish state change, and nothing continuous.

**Responsive.** Only one breakpoint does real work, roughly where a tablet becomes a
laptop. There the gesture sensitivities change, the progress ring shrinks, the spinner
shrinks, and the smallest footer text grows rather than shrinks, because at its desktop
step it would be below readable on a phone. Nothing overflows sideways at a narrow
viewport and every navigation target stays reachable. Below the breakpoint an entry row
stacks into four lines and pointer dragging is not offered at all, because a stacked row
has no obvious grab point; two arrow controls become permanently visible instead, and they
are the same controls the keyboard path already uses, so nothing new is built. The gutter,
the three header words, the scene count and order, the one-screen constraint and the
single theme never change at any width.
## Front-end specification

### Layer order

Seven layers, from the back forward: the canvas holding the water; the scene container
that wraps it; the content panel that dims the water while a project record is read; the
user interface layer carrying all six scene layers; the unlock ring; the project detail
panel; and, sharing the very front, the entry loader and the audio control.

The audio control sharing the loader's layer is deliberate: a visitor who wants the sound
off must be able to reach that control from any state of the page, including while a panel
is open.

### Global chrome

There is no header bar, no footer and no navigation in the ordinary sense. The chrome is
four corners and an edge, and none of it is present on arrival. All of it fades in once
the introduction completes and fades away again whenever a panel opens. The site is empty
by default and produces its controls when they become relevant.

| Corner | What is there |
|---|---|
| Top left | The monogram, which returns the dive to the surface, with the full name beside it readable only by assistive technology |
| Top right | Three words, `Works`, `Message` and `Contact`, each jumping the dive to that depth. Uppercase monospace at the label step, no border and no ground: words, not buttons |
| Bottom right | The audio control: a circle with a ring one step heavier than a hairline, holding three bars driven from the sound itself |
| Bottom left | The save control, in the same treatment as the three header words |
| Right edge | The depth mark: a small full-round pill on the mark colour that travels its track as the dive moves and fades when the dive stops |

Every text control on the dive shares one hover behaviour on a device with a real pointer:
the three header words, the monogram, the save control, the status line and the eight contact
destinations. The run's characters are replaced by random characters from the same set,
uppercase letters plus the site's own bracket and slash marks, and settle back to the true
word one character at a time, left to right, over a short interval. Colour changes with it,
quickly. A device with no hover gets none of this.

The save control is deliberately not in the header. The header's three controls navigate
and this one writes, and a control that changes state among three that do not is one a
visitor presses by accident. When the message strip is showing, the save control steps up
out of its way, so that the one control that writes state is not covered by the messages
about writing state.

### Iconography: the four glyphs

Four, all drawn from coordinates rather than loaded, and the set has no fifth.

| Glyph | Construction |
|---|---|
| Spinner | A three-quarter ring with square-cut terminals, filled in the ink. It rotates continuously while loading and it is the only thing on the site that rotates |
| Monogram | `IM` as outlines with a detached square counter at the upper right and a hairline frame drawn around that same square. The doubling is what makes the mark read as a readout rather than as a letter |
| Progress ring | Two identical circles on one square canvas, a track and a fill, the fill driven by dash offset and rotated a quarter turn anticlockwise so it starts at twelve o'clock. The stroke sits exactly inside the canvas edge with no clipping |
| Close mark | Three strokes, not two. Two lines make a cross; the third makes it read as a struck-through record rather than as a dismissal. Reproduce all three |

There is one spinner and no second variant of it, one close mark and one ring. If a fifth
glyph is ever needed: canvases are square and sized to the geometry rather than to a
shared grid; strokes are stroked and fills are filled and the two are never mixed in one
glyph; stroke weight scales with the canvas rather than with the rendered size; terminals
are square everywhere; every glyph is the ink, so one that must read as inactive takes the
state colour on its container rather than a second fill.

### The loader and the gate

The loader is a full-screen layer on the ground carrying four things: a bracketed status
label reading `[Please wait]` at the mark colour, a live status line reading
`Loading 3D experience`, the meter, and the spinner.

**The meter is the progress bar and it is made of text.** Two runs of slash characters, a
filled run at full strength and a remainder run at the state colour, with progress
expressed by moving characters from one run to the other. Reproduce it as text and never
as a filled rectangle: a progress bar drawn as slashes in a monospace face reports
progress, establishes the instrument register before any other copy appears, and needs no
geometry at all. Its length is the container width divided by the character advance, so it
is recomputed on resize; a fixed character count overflows on a phone and stops short on a
wide monitor.

The loader does not cut when loading finishes. It dissolves, and because its ground and
the water's empty colour are the same value, nothing changes colour at the handover:
geometry simply appears.

The gate then replaces the loader's content with three centred elements: a bracketed
salutation reading `[Welcome aboard]` at the mark colour; a primary control reading
`Dive into the experience` on the ink with the ground as its text, a hairline border and
generous padding; and a secondary control reading `Enter without audio` with no ground and
a hairline underneath only.

The secondary is pinned to the bottom of the screen rather than tucked underneath the
primary, and that distance is deliberate: it stops the pair reading as a button with a
disclaimer. Both are real choices and both enter.

### The six scene layers

**Surface.** The name `Ines Marlow` across the top, set one character per element so it
can be revealed character by character and so each letter can be addressed. Along the
bottom, one line of uppercase tracked monospace at the label step reading
`[Scroll to descend]`. That line is the only instruction on the entire site: everything
else has to be discovered, so a first-time visitor must read it once and know what to do.

**Introduction.** One sentence, centred, at the lead step, and it is the only use of that
step: `Ines Marlow is a Software Engineer`. It is drawn in a difference blend so it
inverts against whatever is behind it, per pixel, every frame. Over dark water it renders
light; under a bright caustic it renders dark; it is never invisible and it never needs a
box behind it. Two consequences a build must accept: the text's colour is not chooseable,
because the water picks it; and fading it has to be quick, because halfway through a fade
it reads as a colour cast rather than as words.

**About.** Four runs and no photograph, no biography paragraph and no résumé. Its thinness
is the argument: the claim is that the work speaks.

| Run | Step | Copy |
|---|---|---|
| Disciplines | `1.55em` | `WebGL & Three.js, GSAP` at full strength, `Animations, AI Systems Integrations,` and `Mobile Applications, 3D Compositions` at half, `& Beyond.` at full strength |
| Location | `0.8em` monospace | `based in Portugal` |
| Affiliation | `0.8em` monospace | `/// Creative Developer at [Kelp Studio]` |
| Standing | `0.8em` monospace, three lines | `Working worldwide since 2016`, `+9 years of experience (+40 projects/works)` |

The alternating emphasis is the scene's whole typographic idea: one size, one weight, and
emphasis carried entirely by how solid the ink is. That is forced by spending the signal
colour once, because emphasis here cannot be made of colour.

The triple slash before the affiliation is a motif rather than a typo. It appears again in
the footer credit and it is the same character the loader's meter is built from. Treat the
slash as a punctuation mark belonging to the design system.

**Works.** The layer carries the record for whichever project the dive is in front of,
aligned to the bottom: a close control reading `Close` near the middle of the top edge
rather than in a corner, a title at the display step given exactly one line and clipped
rather than wrapped, a one-line description, a slash-separated skills line, and a link
reading `Visit Project`.

| Project | Description | Skills |
|---|---|---|
| `Tidal Atlas` | A navigable chart of a coastline that redraws itself with the tide | `HTML / CSS / JS / WEBGL` |
| `Kelp Forest` | A canopy that grows toward whatever the visitor is looking at | `HTML / CSS / JS / SHADERS` |
| `Sonar Room` | A room you map by listening rather than by looking | `HTML / CSS / JS / WEB AUDIO` |
| `Drift Table` | A table of objects that settle differently every time it loads | `HTML / CSS / JS / CANVAS` |

The close control sitting near the centre rather than in a corner is consistent with the
rest of the site: this is an instrument panel, and its controls sit where the eye already
is, not where conventions put them.

**Message.** Four panels in one rectangle, three at zero and one at full strength. Each
carries a bracketed index, `[1]` to `[4]`, then one sentence of direct address at the
body-small step, then two or three authored lines of quotation at the body step, then an
attribution at the label-small step, uppercase, at seven tenths, and explicitly not
italic, because an italic citation would be the only italic on the site. The bracketed
index is the same idiom as the loader's status: the site indexes its own argument the way
it indexes its own state.

| Panel | Address | Quotation | Attribution |
|---|---|---|---|
| `[1]` | `On what a portfolio is for` | `A list of work asks to be believed. / A piece of work asks nothing.` | `NOTEBOOK, LISBON, 2019` |
| `[2]` | `On the cost of a good idea` | `Every effect that survives the cut / paid for itself in frames.` | `NOTEBOOK, PORTO, 2021` |
| `[3]` | `On building for somebody else's machine` | `The floor matters more than the ceiling. / Build the still frame first.` | `NOTEBOOK, LISBON, 2022` |
| `[4]` | `On finishing` | `Something unfinished is a promise. / Something finished is an address.` | `NOTEBOOK, FARO, 2024` |

The same four panels' text is also present once as a flat run, sized to nothing and not
visible, so the content is in the document for assistive technology and for indexing.
Exactly one of the two copies is exposed: the flat run is, and the visible stacked panels
are hidden from assistive technology, or every word is announced twice.

The hold control sits centred above the panels, resting hidden and slightly small and
arriving at full size as it arms. The ring fills from twelve o'clock clockwise while the
hold continues and drains steadily on release, taking several seconds to reach empty
rather than snapping back. That asymmetry is the design: filling requires sustained
intent, and briefly lifting a finger does not start you again.

**Contact.** Eight destinations, all external, all text runs rather than buttons, each a
row with its own name as its label, in this order.

| # | Label | Destination |
|---|---|---|
| 1 | `Email` | `host@example.com` |
| 2 | `WhatsApp` | a messaging destination carrying a prefilled enquiry |
| 3 | `LinkedIn` | a professional network profile |
| 4 | `GitHub` | a code host profile |
| 5 | `Awwwards` | a design publication profile |
| 6 | `CodePen` | a code playground profile |
| 7 | `Instagram` | an image network profile |
| 8 | `X` | a short-post network profile |

They are a list, not a row of icons: every one is its name in words, and no social glyphs
are added, because the icon set has no room for six more marks without becoming a
different family. The messaging destination carries a prefilled message, which removes the
hardest part of making contact.

The footer carries three monospace runs: a sign-off reading `Thanks for visiting` and a
credit reading `Development & 3D Design by Ines Marlow`; a live frame counter in brackets,
spaced inside them, which must read the real rate including while the scene is degraded,
because a counter that hides degradation is worse than no counter; and a two-line rights
block, right aligned, reading
`/// 2026 © Ines Marlow. All 3D scenes, environments, media, and core code built from scratch by Ines Marlow.`
and
`Unauthorized use or distribution is prohibited. External micro-assets are credited to their awesome creators.`

The rights block gets larger on a small screen rather than smaller, which is the opposite
of the usual instinct and is correct: at its desktop step against the clamped root it
would be below readable. It is also the only place on the site where the register relaxes;
keep the warmer sentence, because a credit line is the one place a portfolio should sound
like a person.

### The project detail panel

A full surface over the dive, and the only scrolling region in the entire product.
Document scroll is removed globally and this panel restores it locally, because a case
study is reading matter and reading matter scrolls. It arrives with a small vertical rise
alongside its fade, in the one direction the scene layers do not use, so it reads as
arriving over the dive rather than as part of it.

Two consequences the build must handle. The gesture handler stands down entirely while it
is open; without that, reading a case study also drives the dive underneath it and closing
the panel drops the visitor somewhere they did not choose. And the panel contains its own
overscroll, so reaching the bottom of a case study does not chain into the page behind it.

While it is open it is a modal region: focus moves into it, focus does not leave it,
escape closes it, and closing returns focus to the control that opened it.

### Refusal and not-found surfaces

One shell, three messages, on the ground with no water behind them, because a visitor who
has already hit a problem should not then wait for a three-dimensional scene to load
before being told about it. Each carries a bracketed label at the label step in the mark
colour, one line at the display step, and one control in the gate's secondary treatment.

| Surface | Label | Line | Control |
|---|---|---|---|
| Not found | `[No such depth]` | `That address does not exist` | `back to the surface`, to `/` |
| Forbidden | `[Not your logbook]` | `This logbook belongs to someone else` | `back to yours`, to `/logbook` |
| Failed | `[Signal lost]` | `Something went wrong down here` | `try again`, refiring the request |

Keeping the bracketed labels is what stops an error page feeling like a different website.

### Forms

Every form is built from the entry gate's two control treatments and the type steps above.
The sign-in surface uses the refusal shell: a bracketed label reading `[Surface log]` at
the mark colour, the mode's own heading at the display step, the fields, a primary control
and a secondary control.

| Field | Where | Constraints |
|---|---|---|
| Email | `/sign-in` | required, trimmed, lowercased, at most `254` |
| Password | `/sign-in` | required, `8` to `200` |
| Display name | `/sign-in` with `mode=create` | required, `1` to `60` after trimming |
| Reset email | `/sign-in` with `mode=reset` | required, trimmed |
| New password | `/sign-in` with `mode=set` | required, `8` to `200`, entered twice, must match |
| Logbook title | `/logbook` | required on publish, `1` to `80` after trimming |
| Entry note | `/logbook` | optional, at most `280` |

A field is a hairline-strength ground with the ink as its text, the mark colour as its
placeholder, no border except a hairline underneath in the state colour, no radius, and
the same height and padding as the gate's primary control. On focus that underline doubles
in weight and goes to the ink.

Two rules matter more than the styling.

**A submit control is disabled when, and only when, a request is in flight.** It is never
disabled because a field is empty or invalid: an empty required field produces a message
on submit, not a dead control. A disabled button with no explanation is the most common
way a form becomes unusable for somebody who cannot see which field is at fault.

**The error slot is reserved under every form whether or not there is a message**, so the
form never jumps under the visitor's hands. It costs one line of height.

The pending, success and recovery phases are all specified. While a request is pending the
control's label is replaced by the spinner, inline, and every field is disabled. On a
success that ends the task the form is replaced by a bracketed confirmation line at the
label step in the mark colour; on a success that continues it, the confirmation appears in
the error slot and the form stays. On a rejection the message renders in the slot, every field keeps
its value, and focus moves to the field the response names or to the first field. On a
network failure the slot reads `Something went wrong down here`, values are kept, and the
control returns to rest.

The primary controls read `Sign in`, `Start a logbook`, `Send reset link` and
`Set password` in their four modes, and the secondary controls read `Forgot password`,
`Show` and `Sign out`. Every message is a short declarative sentence with no exclamation
mark, no apology and no emoji.

| Message | When |
|---|---|
| `That email and password do not match` | A wrong password, or an unknown address |
| `That email is already registered` | Creating an account on a taken address |

### The logbook surfaces

An entry row carries, in order: a bracketed two-digit index from `[01]` to `[12]` at the
label step in the mark colour; a generated thumbnail; the scene name and the depth as a
percentage with no decimal at the label step; the diver's note on its own line at the
body-small step; a control reading `Dive to this`; and the close mark, to remove the row.
Rows are separated by a hairline, and there is no card, no ground and no radius.

The drag handle is the index cell rather than a separate grip glyph: the bracketed index
is already there and already reads as an ordinal, and the icon set has four glyphs.

Above the rows sit the title field and, once the logbook is `published`, its public
address with a `copy` control, which puts `[Link copied]` in the strip. Once the logbook is
`answered` a persistent notice sits above the entries: a bracketed label reading
`[Received]` at the label step in the mark colour, and one line at the body-small step.
The publish control reads `Publish` and becomes `Unpublish`.

A published logbook at its own address renders the same rows read-only, with the title,
the diver's display name and every note, and with only the replay control on each row.

The dock is the queue beside the logbook currently open. Each row carries the diver's
display name at the label step, the title at the display step clipped to one line, the
entry count, the published date written `DD/MM/YY`, and a control reading `Open`. Rows are
separated by a hairline.

### Empty, loading and error blocks

The empty block is a centred column: a bracketed label at the label step in the mark
colour, a line at the body-small step below it, and a control below that in the secondary
treatment. The error block is the same layout with `[Signal lost]`, `Could not load this`
and `try again`.

A skeleton is a block the exact size of the row it replaces, on the hairline ground, square
cornered, carrying the loader's own pulse between faint and full rather than a sweep. There
is no gradient sweep anywhere in this design and adding one here would be the only
instance. Under reduced motion a skeleton holds at its faint end.

### The message strip

Fixed to the bottom edge, full width, on the hairline ground, in bracketed uppercase
monospace at the label step in the ink, the same height as the audio control's diameter.
It fades in and out and never travels, because visible travel is reserved for the depth
mark alone. It dwells five seconds and is single-slot: it shows one message at a time and a
second message replaces the first without re-animating, rather than queueing beneath it. It carries an optional control at its right, for
`retry`. It is full width at every viewport and never becomes a corner card.

### Dates and numbers

There is no currency on this site and none is added. A date is written `DD/MM/YY`,
zero-padded and slash-separated, because the slash is already this site's own punctuation
mark, so a date set that way reads as part of the instrument. Nothing anywhere says
`2 days ago`: a relative date is wrong the moment a page is cached.

A message panel index is unpadded, `[1]` to `[4]`, and a logbook entry index is zero-padded
to two digits, `[01]` to `[12]`. That distinction is real: four panels are an argument in
steps and twelve entries are a list that must align down a column.

### Zero-asset construction: the substitution for every missing asset

Nothing binary is fetched from anywhere, including this origin. No image file, no model
file, no video, no font file and no audio file.

**The water** is a shader over geometry and needs no texture. It clears to the ground
colour. A linear depth fog runs from the deep, soft teal near the camera to the ground
colour far from it, and that single term does more for the underwater read than anything
else, because distant geometry dissolves rather than shrinking. Caustics are two
overlapping scrolling gradients differenced against each other and sharpened to bring out
the filaments, tinted the mid, vivid cyan at low intensity. Particulate is an instanced
draw of small points at three depth bands in the light cool neutral, drifting at three
different rates, the nearest largest and most transparent, halving in density as the
degradation ladder descends. Surface distortion is a two-octave noise offset scaled by the
pointer's speed and by the transition surge, and those two inputs are what make the water
respond both to gesture and to scene changes.

The water must move on its own clock and also react to the pointer's speed, and the two
must stay separable. A scene whose motion is entirely pointer-driven is dead when the
pointer is still; one with no pointer term does not feel touchable.

**Each scene is one form plus its environment**, composed from primitives, normalised to a
unit bounding sphere and scaled per scene.

| Scene | Form |
|---|---|
| Surface | None. Open water: fog, caustics and particulate only |
| Introduction | A single swept basin far below, subdivided and vertex-displaced, in the mid cool neutral |
| About | A partial room of six boxes opened on two faces, in the light cool neutral |
| Works | Four rounded panels on an arc, each carrying its project's generated media |
| Message | A swept volume with four equally spaced stations |
| Contact | Two concentric rings, counter-rotating slowly |

The camera's field of view differs per scene and is held as a value per scene rather than
as a constant. It is the strongest compositional lever in the build and it costs nothing:
it is why six scenes read as six different places rather than one room redressed.

**A logbook thumbnail is generated from the entry's two numbers, never captured.** Fill
with the ground; draw a vertical gradient from that scene's near water colour down to the
ground; draw three horizontal bands of the light cool neutral at low alpha, positioned from
the progress value, so two moments in the same scene at different depths look different;
draw the scene's form as a filled silhouette in the near-black neutral at a size derived
from progress; overlay six to ten dots in the mid, vivid cyan at low alpha, positioned
from a hash of the two numbers.

**Determinism is the requirement, not fidelity.** The same moment must always generate the
same image, or a logbook reshuffles its own appearance every time it is opened. Capturing
the real frame is forbidden: it would mean loading the whole scene on every route that
lists a logbook, and only the dive loads the scene.

**Project media** is a generated still at a wide aspect, seeded from the project's slug so
each is stable: the ground, then two radial gradients, one the deep, soft teal at full
strength and one the mid, vivid cyan at low alpha, then one linear gradient across a
seeded angle in the ink at very low alpha, then the project's index as two digits in the
display face at low alpha, centred.

**Audio** is generated in the browser: three detuned oscillators through a low-pass filter
with a slow modulation on the cutoff, plus a filtered noise source at low gain for the
water. The graph is source, analyser, filter, gain, destination. It never starts without a
gesture; it fades rather than cuts in every direction; it fades out near its own end
rather than stopping, because a track that ends abruptly in an experience like this reads
as a fault; it fades faster when the window loses focus than it fades anywhere else,
because somebody switching windows wants it gone quickly and back gently; it muffles when
the experience is obscured; and it exposes its state visually through the three bars, so a
visitor who cannot hear can still see whether audio is on.

### The degradation ladder

Six rungs. From comfortably inside budget the resolution multiplier is high; the default is
one step lower; outside budget it drops once more; then post-processing goes off; then
particle and volume density halve; then the frame loop stops at a single static frame per
scene. A machine with no hardware acceleration, or a visitor who has asked for reduced
motion, starts at that floor from the first frame.

**The floor is not a failure state.** A still frame of this water is a dark blue-green
field, which is exactly what every white word on the site is designed to sit on, so the
layer is never removed. The frame loop also stops entirely when the document is hidden,
which is a listener rather than a heuristic, and the same discipline the audio and the
dock queue both follow.

## Technical requirements

Server-rendered pages with interactive islands, and a JSON contract on the same origin.
Every route's HTML is produced on the server; only the parts that move are made interactive
in the browser: the dive's canvas and gesture layer, the logbook's ordering and note fields,
and the dock's queue. Moving between the dive and a client-area route loads a new page rather
than transitioning inside the dive.

| Layer | What to use |
|---|---|
| Server | Fastify on Node 22, serving the pages and the JSON API on the same origin |
| Pages | Nuxt 3, rendered on the server, with interactive islands hydrated in the browser |
| Three-dimensional layer | WebGL through the browser's own context, with hand-written shaders |
| Sound | The browser's own audio graph |
| Datastore | PostgreSQL, reached at `DATABASE_URL` |
| Mail | Mailpit, reached over SMTP at `SMTP_HOST` on `SMTP_PORT`, authenticating with `SMTP_USER` and `SMTP_PASS` when they are set |

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and Mailpit, and reaching for
anything else is a contract violation.

The browser receives finished HTML on first paint for every route. The dive's own scene is
built in the browser after that HTML has painted, and the loading surface is part of the
first paint rather than something the scene draws once it is ready.

**Identity and session.** Email and password, implemented by this application, with no
external identity provider. A session's lifetime is `30` days, sliding: it renews on any
authenticated request older than `24` hours. It travels in an HTTP-only, secure,
same-site-strict cookie, and no identity state is readable by the page: the page asks the
service who it is on first paint. The session check must not block the dive. The experience
starts while that request is in flight and the save control appears when the answer
arrives, so a visitor who is not signed in never notices it happened. A password is stored
only as a salted one-way hash and is never returned by any response. Signing in takes the
same amount of time whether or not the account exists.

**The shareable secret.** A logbook's public identifier is generated from a
cryptographically secure source with at least `128` bits of entropy, encoded in a URL-safe
alphabet. It must never appear in a log line, in a measurement event or in a referrer. The
public logbook route therefore declares a no-referrer policy on its own responses, so that
following an outbound project link from inside a shared logbook does not hand the secret
address to a third-party site. Every other route declares a same-origin referrer policy.

**Headers.** Every response carries a content security policy whose default source is this
origin, whose worker source is this origin and blob, and which declares no frame ancestors;
a strict transport policy of one year including subdomains; and a nosniff content-type
policy. The worker source allowance is not optional: a compressed texture is decoded off
the main thread, and a policy that omits it produces a scene that works on the developer's
machine and shows an empty ocean everywhere else.

**Input handling.** Every string field is trimmed and length-checked and stored as text,
and no markup is parsed anywhere. A note and a title render as text nodes and never as
markup: pasting `<img src=x onerror=alert(1)>` into a note, saving it, publishing it and
opening the public address in another browser must show those literal characters and run
nothing, and must not silently strip or rewrite them either. `next` must match a path
beginning with a single `/` and not `//`, and anything else becomes `/`. `at` and a saved
progress value are parsed as numbers and clamped to `0` and `1`, with anything unparseable
treated as absent. A scene index is range-checked against the six scenes. A reset token and
a public identifier are compared in constant time.

**Rate limits.**

| Path | Limit | Keyed on | Answer |
|---|---|---|---|
| Sign in | `10` per `15` minutes | source | `429` |
| Sign in | `5` consecutive failures | email | `429`, cleared on success or after `15` minutes |
| Sign up | `3` per hour | source | `429` |
| Reset request | `1` per `15` minutes | email | `202` regardless |
| Publish | `10` per hour | diver | `429` |
| Public logbook read | `60` per minute | source | `429` |
| Every other authenticated write | `120` per minute | diver | `429` |

The reset limit answers success rather than `429` on purpose: a `429` would reveal that the
address is known to the system.

**Titles, descriptions and the favicon.** Every public route carries its own title and its
own description, and no two routes share either. The dive is
`Ines Marlow // Creative Software Engineer & UI/UX Designer`, the works address is
`Works // Ines Marlow`, sign-in is `Sign in - Ines Marlow`, the logbook is
`Your logbook - Ines Marlow`, a published logbook is its own title followed by
` - Ines Marlow`, the dock is `Dock - Ines Marlow`, and an unknown address is
`Not found - Ines Marlow`. The site serves a favicon at its own address and declares it in
every document's head.

**Health and the page view record.** `GET /api/health` answers `200` once the datastore is
reachable and the six scenes and four projects are loaded. Every page view is recorded with
its route and the instant it was served, and only the host can read that record.

**Performance.** The dive paints its loading surface in under `1.0s` and responds in under
`1.5s`, with under `400KB` transferred before the scene's own content. Every other route
paints faster and carries no three-dimensional content at all: sign-in in `0.6s` and
`120KB`, the logbook, a published logbook and the dock in `0.8s` and `160KB`, and an error
surface in `0.4s` and `80KB`. A sign-in form behind an eight-second underwater load would be
indefensible. The scene itself is ready in under `8s` on a first visit and under `2s` from
cache, and the frame loop keeps main-thread work under `4ms` by reading no geometry and
allocating nothing per frame.

## Data model

Two kinds of entity meet in one place: the dive's own content, which is built in and never
written by a visitor, and the account state. A logbook entry is where they meet, because it
names a scene by index and a depth by number.

**Built in.**

`scene` carries an `index` from `0` to `5`, a `slug`, a `name`, a field of view and the
identifier of the layer that carries its words. The six, in order: `surface`,
`introduction`, `about`, `works`, `message`, `contact`.

`project` carries an `id`, a `slug`, a `title`, a `description`, an ordered list of skills,
an outbound `url`, the `scene_index` it belongs to, and its `position`. Four rows, every one
at scene `3`, in the order `tidal-atlas`, `kelp-forest`, `sonar-room`, `drift-table`.

**Account state.**

`diver` carries an `id`, an `email`, a `display_name`, a password hash, a `role` of `diver`
or `host`, and the instants it was created and last seen.

`logbook` carries an `id`, a `public_id`, the `diver_id` that owns it, a `title`, a `state`
of `empty`, `draft`, `published` or `answered`, the instants it was published and answered,
and the instant it last changed.

`logbook_entry` carries an `id`, the `logbook_id` it belongs to, a `scene_index`, a
`progress`, a `position`, an optional `note` and the instant it was saved.

`reset_token` carries an `id`, the `diver_id` it is for, a hash of the token, an expiry and
the instant it was used.

`page_view` carries an `id`, the `route` and the instant it was served.

**Field rules.**

| Field | Rule |
|---|---|
| Every identifier | opaque and never sequential. A sequential logbook identifier would make the queue countable from outside |
| `logbook.public_id` | distinct from `id`, at least `128` bits of entropy, URL-safe, unrelated to `id`, to the diver or to the publish time, minted on first publish and stable across unpublish and republish |
| `diver.email` | unique, trimmed, lowercased, at most `254` |
| `diver.display_name` | `1` to `60` after trimming |
| `logbook.title` | `1` to `80` after trimming, defaulting to `Untitled dive` |
| `logbook_entry.scene_index` | an integer from `0` to `5` |
| `logbook_entry.progress` | a number from `0` to `1` inclusive |
| `logbook_entry.position` | a `0`-based integer, contiguous and unique within its logbook |
| `logbook_entry.note` | at most `280`, optional |
| Every instant | stored in UTC and rendered at the edge |

**Relationships.** A `diver` has exactly one `logbook`, created with the account in state
`empty`, and deleting the diver deletes it. A `logbook` has between zero and twelve
entries, and deleting it deletes them. An entry names a `scene` by index, which the store
does not enforce and publishing does. A `scene` has many `project` rows.

One logbook per diver removes an entire class of question: there is no logbook list, no
create control and no default to choose.

**Invariants.**

- Positions over a logbook's entries are always `0` to one less than the count, with no
  gap and no duplicate. The only write that changes them takes the complete ordered list
  of entry identifiers and rewrites each position from that list's index.
- A thirteenth entry is impossible.
- `public_id` is minted once and never regenerated.
- A logbook leaves `empty` on its first save and never returns to it.
- Only a logbook in `draft` accepts a write; every other mutating request against it is a
  conflict.
- Only the owning diver reads a logbook that is not `published` or `answered`. The host
  cannot, on any path, and asks in vain by address.
- The logbook a request acts on is resolved from the session and never from a parameter.
- The answered instant, once written, is never cleared. Unpublishing an answered logbook
  returns it to `draft` and leaves that instant alone.
- No visitor-supplied string ever reaches a markup-parsing sink.

**Seed data.** Six scenes, four projects, three accounts sharing the password
`deku-demo-pw-2026`, and one logbook per account. `host@example.com` holds an `empty`
logbook. `diver2@example.com` holds a `draft` titled `Untitled dive` with two entries, at
scene `0` progress `0.05` and scene `4` progress `0.78`, both with no note.
`diver@example.com` holds a `published` logbook titled `Reef pitch` with four entries, in
position order:

| position | scene | progress | note |
|---|---|---|---|
| `0` | `3` | `0.62` | `The works arc is the whole argument` |
| `1` | `1` | `0.24` | `Read this line against the bright water` |
| `2` | `5` | `0.94` | `Ends on an address, not a loop` |
| `3` | `2` | `0.41` | `Thin on purpose` |

The page view record starts empty and accrues rows as routes are served. Seeding is
idempotent: starting the app a second time leaves exactly one copy of every seeded row.

The fields above are named in snake case where they are stored; every API response carries
the same fields in camel case, so `scene_index` travels as `sceneIndex`, `public_id` as
`publicId` and `field_of_view` as `fieldOfView`.

## Constraints

- No binary asset is fetched from any origin, including this one: no image file, no model
  file, no video, no font file and no audio file. Every image on the site is generated in
  the browser from values this brief pins, and the sound is generated too.
- The dive is exactly one viewport tall at every width, never changes height when mobile
  browser chrome collapses, and never exposes a native scroll. The project detail panel is
  the only scrolling region in the product.
- Only `/` and `/works` load the three-dimensional layer. Sign-in, the logbook, a published
  logbook, the dock and every error surface load none of it.
- No surface polls while the document is hidden, and the frame loop stops while it is
  hidden too.
- A logbook is never kept in the browser. It exists on the service, keyed to the account,
  and follows a diver to another machine. The cost is that a moment cannot be saved without
  an account, and that cost is paid openly by carrying the held moment across the sign-in.
- Only two things are remembered per device: whether the last entry was with or without
  audio, and whether the cookie choice has been answered. Both are device preferences
  rather than account state.
- Nothing a diver typed is ever discarded by a failure. A failed write leaves the edit in
  the field, and the page never replaces something somebody is looking at with an older
  version of it.
- Removing one entry asks no confirmation, because it is one press to undo. Emptying the
  whole logbook needs the same control pressed twice within three seconds, its label
  changing to `[Press again]`. Deleting the account needs the account's own address typed
  in, which is a fact somebody has to know, rather than a word, which is a reflex.
- Internationalisation: there is one locale, declared on the document, and every string a
  visitor reads comes from it, with no surface mixing two. If a second locale is ever added
  it gets its own path prefix rather than being negotiated from a header, because a link
  shared in one language must open in that language. Formatting follows the locale: a date
  is `DD/MM/YY` and nothing is written as a relative time.
- Persistence and migration: the logbook is service state and survives a reload, a new tab,
  a restart and a move to another machine. The dive's own depth deliberately does not
  survive a reload. Schema changes carry existing logbooks forward; an entry whose scene a
  later deployment removed fails loudly on publish rather than replaying to the wrong
  place.
- Seeded accounts must be refused by a production configuration rather than merely omitted.
## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
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

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status": "ok"}` |
| `GET /api/scenes` | none | `scenes`, the six in `index` order, each with `index`, `slug`, `name`, `fieldOfView` |
| `GET /api/projects` | none | `projects`, the four in `position` order, each with `id`, `slug`, `title`, `description`, `skills`, `url`, `sceneIndex`, `position` |
| `POST /api/auth/sign-up` | `displayName`, `email`, `password` | `diver` with `id`, `displayName`, `email`, `role`, and sets the session cookie |
| `POST /api/auth/sign-in` | `email`, `password` | `diver`, and sets the session cookie |
| `POST /api/auth/sign-out` | none | an empty body, and revokes every session for that account |
| `GET /api/auth/me` | none | `diver` |
| `POST /api/auth/reset` | `email` | `{"ok": true}`, always, whether or not the address is registered |
| `POST /api/auth/reset/confirm` | `token`, `password` | an empty body, and destroys every session for that account |
| `GET /api/logbook` | none | `logbook` and `entries` in `position` order |
| `PATCH /api/logbook` | `title` | `logbook` |
| `POST /api/logbook/entries` | `sceneIndex`, `progress`, optional `note` | `entry` with `id`, `sceneIndex`, `progress`, `position`, `note`, `savedAt` |
| `PATCH /api/logbook/entries/<entryId>` | `note` | `entry` |
| `DELETE /api/logbook/entries/<entryId>` | none | an empty body, and the remaining positions close the gap |
| `PUT /api/logbook/order` | `order`, the complete array of entry identifiers in their new order | `entries` in the new order |
| `POST /api/logbook/publish` | none | `logbook` carrying `publicId` and `publishedAt` |
| `POST /api/logbook/unpublish` | none | `logbook`, back in `draft`, with `publicId` unchanged |
| `GET /api/logbook/public/<publicId>` | none | `logbook`, `entries` in `position` order, and `diver` carrying `displayName` and nothing else |
| `GET /api/dock` | `state`, `cursor` | `logbooks` newest published first, each with `id`, `title`, `entryCount`, `publishedAt`, `answeredAt` and the diver's `displayName`, plus `cursor` |
| `GET /api/dock/<logbookId>` | none | `logbook`, `entries` and `diver` |
| `POST /api/dock/<logbookId>/answer` | none | `logbook` in `answered` with `answeredAt` |
| `GET /api/page-views` | `route` | `views`, each with `route` and `viewedAt`, and `total` |

Field names are exact. A successful call returns the named resource or shape, and an
invalid or unauthorized call is rejected as a client error, never as a server error and
never as a silent success, carrying the one error body below.

| Field | Use |
|---|---|
| `error` | human-readable, rendered straight into the form's error slot |
| `code` | stable, for branching, and never rendered |
| `field` | which field to move focus to, or nothing |

| `code` | Status | Meaning |
|---|---|---|
| `unauthenticated` | `401` | no session, or expired |
| `forbidden` | `403` | session present, not permitted |
| `not_found` | `404` | including a draft logbook asked for by the host |
| `wrong_state` | `409` | the logbook is not in `draft` |
| `already_published` | `409` | a publish against a published logbook |
| `logbook_full` | `422` | the twelfth moment is already saved |
| `scene_missing` | `422` | an entry names a scene the dive no longer has |
| `invalid` | `422` | any other validation failure, with `field` naming it |
| `rate_limited` | `429` | a limit named in `## Technical requirements` was reached |

Session authentication applies to everything except the health route, the scenes and
projects reads, the public logbook read, and the sign-up, sign-in and reset paths.

### No mocks

The rows this product reports on have to exist in PostgreSQL. An in-memory list of entries
that resets when the process restarts, an order held in a variable rather than read back
from rows, a public address computed at read time rather than written at publish time, a
seeded logbook typed into a template rather than loaded from the store, and a page view
total counted in the page rather than summed from rows are each a contract violation
however convincing the page looks. PostgreSQL is the fact: the app's own screens can only
reflect what lives in it, never substitute for it.

## Definition of done

A stranger enters the dive, sinks to the works scene, saves that moment, creates an
account, and is returned to the depth they left with the moment already saved. They save
two more, move the third row to the top, reload, and the order is the one they left. They
write a note, publish, and get an address. A browser with no account opens that address and
reads every row and every note, and activating an entry opens the dive at that scene and
depth. The host finds it in the queue and marks it answered. The diver unpublishes and the
address answers as not found. A different diver asking for that logbook while it was a
draft was told it belongs to somebody else, and the host asking was told it does not exist.
