# Lumina

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser, read the home
page, cross to the developer portal, copy a text-to-video code sample, and create a free
account from the sign-up form, landing on a confirmation that names the account, without
hitting an error page.

A different stranger, signed out, must NOT be able to read a news item that is still a
draft, and must not be able to fetch that draft's poster image by any means, including by
asking the object store for the exact key the studio shows its author. Draft privacy cannot
be faked in the app itself: the uploaded bytes must live in the object store at their
scheme's key, and a copy on the app's own disk does not count.

## Overview

Lumina is the public presence of a generative-media company. It sells one platform to three
audiences at once: creators who want a browser studio, developers who want one interface
across many models, and enterprises who want both under governance.

Three surfaces are built, and a fourth is specified. The **marketing home** is a light
document that opens on a full-bleed dark video hero, runs a partner-logo marquee, presents
three products through a horizontal switcher, drops into a research band on a living green
field, lists news cards, and ends in a multi-column footer sitemap. The **developer portal**
is a dark document with its own slim chrome selling one generation interface: a four-column
capability bento, a model router, a language-tabbed code sample, and a catalog of model
cards that can be compared. The **agent connector** is a light document explaining how the
generation engine reaches a chat assistant, with a three-step setup, chat-styled
demonstrations, a model pill row and an accordion of questions. Behind all three sits the
**generation application**, which is not built here: its capabilities are stated as
requirements, and its public contract is pinned.

Between the public surfaces and the generation application sits the part this build owns
outright. The copy, the media references, the model specs, the news items and the menu
structure are editorial: somebody signs in and changes a model card or a news item without a
deploy. That means drafts exist, and it means the product has to be honest about them.

**The genuinely hard part is that an unpublished item has two bodies, and both have to stay
private.** The record is one of them, and hiding a record is ordinary. The uploaded poster
is the other, and it lives in an object store that does not know or care what the
application thinks about publication status. A draft whose record is hidden while its bytes
are fetchable from the store by key is not private; it is only quiet.

Lumina deliberately is not several things. It is not the studio: no timeline is built, no
model runs, no frame is generated. It is not a video encoder, a GPU scheduler or a billing
system, though each is specified. It has no native application, no desktop client and no
comment threads. It ships no image, no video and no font file: every one is produced from a
recipe.

## User roles

Signup is **open**. Anybody can create an account from the public form, and the seeded
accounts exist alongside the ones visitors make.

| Role | Can do | Cannot do |
|---|---|---|
| `author` | read every public surface, sign in, create a content item, edit an item they own, upload a poster to an item they own, publish and unpublish an item they own, read their own drafts and their own draft posters | **read or edit a content item owned by another account, read another account's draft poster, publish another account's item, or delete an item that has ever been published** |
| `reader` | read every public surface, sign in, read every published item, manage their own account | **read any unpublished item, fetch any private media object, reach any compose surface, or publish anything** |

An anonymous visitor is not a role. It reads every public surface, submits the sign-up form
and nothing else.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the
UI is not authorization: a direct API call from a `reader` session to any `author`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

Four rules bind every role above.

1. **An unpublished item is invisible, not merely unreadable.** To an anonymous caller, and
   to a signed-in caller who does not own it, a draft answers exactly as a slug that never
   existed answers. The response must not distinguish the two, because a distinguishable
   response tells an outsider that an unannounced item exists.
2. **A private media object is refused by key.** Ownership of the key is not authorization.
   Knowing `media/42/9f2a...d0.webp` is worth nothing without a session entitled to the item
   that owns it.
3. **Publication is one act.** The item's status and its poster's visibility change
   together, in one transaction. A published item whose poster is still private renders a
   broken page; a draft whose poster is already public is the leak this brief exists to
   prevent.
4. **A denial names its cause where naming it is safe.** A signed-in actor who lacks a
   permission is told which permission is required. An anonymous actor is told nothing that
   a missing item would not also have told them.

Seeded accounts, every one of them using the password `deku-demo-pw-2026`:

| Email | Role | What it owns |
|---|---|---|
| `author@example.com` | `author` | two published news items, one draft, one archived item |
| `author2@example.com` | `author` | one draft, which is the cross-author counterexample |
| `reader@example.com` | `reader` | nothing |

## Core features

### Editorial content and the draft boundary

This is the spine of the product and every other feature sits around it.

1. A content item has a `kind`, one of `news` or `model_card`, a `slug` unique per kind, a
   title, a dek, a body, an owning account, a poster, and a `status` of `draft`,
   `scheduled`, `published` or `archived`.
2. Creating an item leaves it `draft`. A draft appears in its owner's own list and on no
   public surface.
3. **An anonymous request for an unpublished item is refused, and the refusal is
   indistinguishable from the refusal for a slug that does not exist.** Requesting
   `/news/the-media-router-preview` while signed out answers exactly as
   `/news/no-such-item-at-all` answers: same status, same body, same headers. A different
   status, a different message or a different response time for the two is the leak.
4. The negative case: a `reader` session, signed in and holding no ownership, receives the
   same refusal for that draft, and the item's row is untouched by the attempt.
5. `author2@example.com` owns a second draft. An `author@example.com` session is refused it
   just as an anonymous caller is, so ownership is per item rather than per role.
6. Publishing an item sets its status to `published` and its poster's visibility to
   `public` **in one transaction**. One without the other is never observable, at any
   instant, by any caller.
7. Unpublishing reverses both in one transaction, and the item and its poster become
   unreadable again in the same act.
8. An item may not be published while its poster carries empty alternative text. The
   refusal names the field. This is a gate rather than a reminder.
9. An archived item is unreadable publicly and is still readable by its owner. Archiving is
   not deletion, and an item that has ever been published cannot be deleted at all.
10. A slug is unique per kind, lowercase kebab, and is immutable once the item has been
    published. A change before publication is permitted; the old slug is not reserved,
    because nothing ever linked to it.
11. Every status change writes an entry to the item's own history carrying the actor, the
    instant, the status before and the status after. The history is append-only.

### Media in the object store

1. **Every uploaded byte lives in `minio` and nowhere else.** Not on the application's
   filesystem, not in a database column, not in a cache the application controls. The
   application reads `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and
   `STORAGE_SECRET_KEY` from the environment and never hardcodes a host.
2. The object key follows a fixed scheme: `media/{item_id}/{sha256_of_bytes}.{ext}`. A
   worked example, for item `42`, a WebP poster:
   `media/42/9f2a1c7d4e8b6a0f3c5d2e1b8a7f6c5d4e3b2a1908f7e6d5c4b3a2918070605d.webp`.
   The checksum is of the bytes as uploaded, and re-uploading identical bytes to the same
   item is the same key and stores one object.
3. The extension follows the content type, which is **sniffed from the bytes** rather than
   trusted from the declared type or from the file name. A file named `poster.webp` whose
   bytes are something else is refused, and nothing is written.
4. A media object carries a visibility of `private` or `public`, which follows the owning
   item's status and is never set on its own.
5. **A private object is unreachable to anyone but the owning account, by every route and by
   every key.** The product serves objects through its own media route; a request there for
   a private object from an unentitled caller is refused, and the refusal is
   indistinguishable from the refusal for a key that does not exist.
6. Access to a public object uses one of two mechanisms: an authenticated streaming endpoint
   that reads the object and writes the bytes, or a presigned address valid for at most five
   minutes. **Pick one and be consistent.** A presigned address is never issued to a caller
   who is not entitled to the object, and never for a private object at all.
7. The negative case: fetching a draft poster's key directly, with the key copied verbatim
   from the studio, is refused for an anonymous caller and for a signed-in caller who does
   not own the item. The object is still present in the store afterwards, and the item is
   unchanged.
8. Alternative text is a property of the media object, is required before its item may be
   published, and is carried into the rendered page.
9. Deleting an item that was never published deletes its objects. Deleting is refused for an
   item that has ever been published, so no live page ever loses its poster.

### Accounts

1. Signup is open: the public form creates an account from an email address and a password.
2. An email address is unique case-insensitively. A second signup with the same address is
   refused, and the refusal does not confirm whether the address was already registered.
3. Every signup carries a client-generated idempotency key, so a double submit creates one
   account rather than two, and a repeat under the same key returns the first result.
4. The password is hashed with a memory-hard function whose parameters are stored beside the
   record. The minimum length is `8` with no composition rules.
5. Authentication is email and password, and the client sends a bearer token on every call
   that needs one. The token expires; an expired token on a mutating call is refused and the
   actor is returned to sign-in with their composed work preserved.
6. A session is an opaque server-side record. The cookie carries no claim and no role.
7. Signing out revokes the session on the server rather than clearing the cookie.
8. A signup records where it came from: the route and the label of the control that started
   it. That attribution is carried in the destination address or in a first-party mechanism
   and is discarded once the account exists.
9. The seeded accounts and the corpus password work at sign-in exactly as an account made
   through the form does.

### The media tile

The dominant surface on all three public routes is an autoplaying, streamed video presented
as a poster-first, muted, looping tile. It is specified once here and reused everywhere.

1. A tile is a rounded container holding three stacked layers.
2. The **poster layer** shows a still frame before and until playback is ready. A
   low-resolution copy sits behind the sharp one, blurred and very slightly scaled up so the
   blur bleeds past the frame edge rather than stopping at it.
3. The **video layer** is muted, looping, plays inline rather than taking over the screen,
   and autoplays only when it is in view.
4. The **overlay layer** carries a bottom-anchored gradient scrim, transparent for the top
   half and darkening towards the bottom, so a caption stays legible over any frame, and it
   carries the controls.
5. **The poster holds at full strength until the video's first frame is decoded, then fades
   away to reveal the video beneath.** The reverse, showing an empty rectangle and filling
   it later, is the failure this rule names.
6. Controls are small circular buttons pinned to a tile corner, each a full pill with a
   blurred backdrop and a layered ring. There are two: pause and mute. Each announces the
   action it will perform, and its announcement flips between pause and play, and between
   mute and unmute, as the state changes.
7. Below the fold a tile is lazy: the poster is a tiny blurred image and the stream attaches
   only as the tile approaches the viewport. Exactly one stream on a route is eager, and it
   is the hero's.
8. Under reduced motion the tile does not autoplay: the poster renders and the play control
   is present.

### The marketing home

1. The document is light. Its title reads `Lumina | Building Real-World Intelligence`.
2. It runs eleven sections in a fixed order: the hero, the partner marquee, the
   three-platform switcher, the research band, the news grid and the footer, with the
   switcher occupying the centre of the page.
3. The **hero** is a full-bleed dark media tile behind a bottom-left copy stack: a display
   heading reading `Building Real-World Intelligence`, a lead paragraph, and one filled
   light pill reading `Try Lumina for free` carrying a chevron. The heading and the lead
   carry a soft shadow so they survive an arbitrary frame behind them.
4. The **partner marquee** carries an eyebrow reading
   `We partner with the world's leading organizations to advance their industries:` above a
   horizontally drifting track of partner name-tiles under an edge-fade mask on both sides.
   The track is duplicated head to tail so the loop is seamless, and it runs on a timer
   rather than on scroll position.
5. The **three-platform switcher** carries the section heading
   `Three platforms built on-top of the same Real-World Intelligence models` above a
   horizontal track of three panels, with tab labels above a rule along which the active
   underline slides. The panels are `Lumina Creative`, `Lumina Dev` and `Lumina Robotics`,
   and the track advances as the reader moves through the section.
6. The **research band** is a full-bleed panel over a living green field under a darkening
   overlay, carrying the eyebrow `Lumina Research`, a heading, a `Learn more` link, and
   three stacked research cards on the right, each a title, an up-right arrow and a one-line
   abstract.
7. The **news grid** carries the heading `See the latest from Lumina` above cards, each a
   poster, a title, a one-line dek and a `Learn more` link. **The grid renders published
   items only**, newest first, and it is the same records the studio edits.
8. Every one of those sections is content rather than markup: changing a news item, a
   research card or a partner tile is an editorial change with no deploy.

### The developer portal

1. The document is dark and wears its own slim chrome, taller than nothing and shorter than
   the marketing bar, carrying a `Lumina Dev` lockup at the inline start, `Explore` and
   `Docs` beside it, and `Log In` and `Sign Up` at the inline end. `Docs` opens in a new tab
   and says so. It carries no mega-menu and no marketing footer.
2. Its title reads `Lumina Developer Portal`.
3. The **hero** is a full-bleed dark media tile behind a title reading `The AI Media
   Platform` over `for Developers`, a subtitle reading
   `The best image, video, audio and real-time models. One enterprise-grade platform.`, and
   two actions: `Get API Key` filled and `Explore Models` ghosted.
4. A **trusted-by marquee** labelled `Trusted by` carries developer-audience partner tiles.
5. The **capability bento** carries the heading `One API for production` over
   `media generation.` and four columns, each a label, a title, a description and a call to
   action: `Access`, `Evaluate`, `Automate` carrying a `NEW` badge, and `Control`.
6. The **model router** section carries the heading `Model Routers for` over `Optimization`
   and the action `Set up a router`.
7. The **code sample** section carries the heading `Seamless Integration`, a category row of
   `Models`, `Workflows`, `Recipes` and `Characters`, and a language row of `Node`, `Python`
   and `cURL`, driving a dark code panel. Changing a tab fades the panel's content once and
   holds. **The panel carries a copy control that places the sample on the clipboard**, and
   the sample is selectable text rather than an image.
8. The **model catalog** carries the heading `State-of-the-art` over `Models`, the actions
   `View all models` and `View SDK docs`, and two presentations of one set of records: a
   horizontally scrolled rail of cards under a one-sided fade mask advanced by circular
   arrow buttons, and a comparison table.
9. **Both presentations read the same model records and render the same fields in the same
   order**: name, tagline, resolution, aspect ratios, inputs, maximum duration and price. A
   card and a table row that disagree is impossible by construction rather than by review.
10. Price is an integer in minor units per second of output, rendered in `usd`. `Nova-4.5`
    is `12` minor units per second; `Chisel-2.0` is `18`; `Worldscape-1` is `30`;
    `Perform-2` is `9`.
11. A model record is editorial: adding one is a record plus a spec, never a code change.

### The agent connector

1. The document is light. Its title reads
   `Lumina Agent Connector | Generate video from your assistant`.
2. The **hero** carries the heading `Lumina Agent Connector`, three stacked lines, the
   action `Connect`, and a row of agent buttons naming an assistant, a chat tool, an editor
   and a coding sandbox.
3. The **three-step setup** carries the heading `Connect Lumina in seconds` and three
   numbered steps. The second step shows the connector address in a monospace field beside a
   `Copy` control that places it on the clipboard.
4. The **capability showcase** carries the heading `A complete generation studio,` over
   `inside your agent.` and four alternating rows, each an eyebrow, a title, a body line and
   a chat-styled demonstration: a user prompt bubble on a near-white neutral, then a
   response tile.
5. The **model pill row** carries the heading
   `Access to the latest state-of-the-art models` above a wrapping row of model-name pills,
   read from the same model records the portal renders.
6. The **prompt gallery** carries the heading `Just tell your agent what you need.` over
   `Lumina handles the rest.` above a grid of example prompt cards, and below them a composed
   chat input showing an add affordance and a `Write a message...` field.
7. The **accordion** carries the heading `Frequently asked questions` and four independently
   expandable rows. Each answer is present in the document at first render, hidden by a style
   rule rather than absent, so an in-page find reaches it.

### The not-found shell and link integrity

1. Any unresolved address renders the product's own not-found shell, answering not-found,
   carrying the full marketing header and footer around a centred body: a heading reading
   `This page doesn't exist.` and a pill reading `Take me home` linking to the home route.
2. It is a real surface rather than an error: a lost visitor can reach every destination the
   site has from it.
3. **Every internal link on every public route resolves.** A link that leads nowhere is a
   defect. External links are out of scope for this rule, because their health is somebody
   else's business.
4. A link that opens in a new tab says so in its accessible name.

### The generation platform, as a contract

The studio, the inference cluster and the credit ledger are not built here. Their behaviour
is specified because the public surfaces sell it, and because the interface this build
exposes has to be shaped to fit them.

1. **Streamed inference.** Output reaches the browser progressively as it is produced rather
   than being withheld until the render finishes. The transport is an open, resumable stream
   per job carrying ordered chunks, each tagged with a job identifier, a rising sequence
   number and a media offset. A reconnect resumes from the last acknowledged sequence number
   rather than restarting. Backpressure is explicit: a slow reader cannot stall the
   accelerator, so the server holds a bounded window and drops intermediate preview frames,
   never final ones. Every stream ends in exactly one terminal event: completed, failed or
   cancelled, with a durable artifact reference on completion. A first meaningful preview
   arrives inside a stated budget even when the full render takes far longer.
2. **A responsive timeline editor.** The editing surface stays interactive at all times,
   including while clips on it are still being generated. Model work, encoding and heavy
   decode happen off the interaction path. A clip carries an explicit state: empty, queued,
   generating with a live preview, ready, or failed, and a generating clip shows its streamed
   preview inline and sharpens in place while the author keeps trimming and reordering
   around it. Edits are reversible across generation boundaries, and the document saves
   itself continuously so a reload restores the exact edit state.
3. **Fleet orchestration.** A shared pool of accelerators serves many concurrent jobs. A
   scheduler places each job by model type, memory, batch compatibility and queue depth, and
   reports a truthful wait before the requester commits. Compatible jobs batch without
   pushing any single job past its latency budget. The pool grows on queue depth under a
   spend ceiling and drains interruptible capacity gracefully, checkpointing and requeueing
   rather than losing a job. A per-account concurrency limit and a weighted-fair queue stop
   one heavy user starving others. Under saturation the system sheds to a smaller or faster
   model rather than refusing requests.
4. **Blended footage.** Generated clips and uploaded clips are first-class citizens of one
   document under one clip abstraction, carrying a common contract regardless of how the
   pixels were produced. A conforming layer reconciles frame rate, resolution, aspect and
   colour so a generated shot and a filmed shot read as one grade. Playback composites
   lightweight proxies and swaps to full resolution only where needed. Every clip resolves to
   one master timebase, so transitions, overlaps and audio alignment are exact across
   origins. Export renders the blended timeline to one file deterministically, and importing
   an export is stable.
5. **The task lifecycle.** Every generation is a durable, addressable task. Submission
   returns a task identifier immediately; the task moves through queued, running and one
   terminal state of succeeded, failed or cancelled, observable by polling and by a push
   channel. Submission is idempotent under a client-supplied key, so a retry creates no
   second job. Tasks are cancellable, carry structured error detail, expose progress, and
   retain their artifact for a stated window. The client mirrors this: a create call returns
   a handle and a separate wait call resolves it.
6. **The preference router.** One endpoint accepts a request plus a declared preference,
   cost, latency or quality, and a price ceiling, and routes each call to the best-fitting
   model without the caller naming one. The router keeps a live scorecard per model and picks
   the model that maximises the chosen objective inside the ceiling, honours fleet state,
   falls back deterministically when its first choice is saturated, and records which model
   served each request. The preference and the ceiling are set once and apply until changed.
7. **Catalog and evaluation.** Many models, the platform's own and third parties', sit behind
   one interface, each described by the same uniform spec. An evaluation harness runs one
   prompt across a chosen set and returns their outputs side by side with per-model quality,
   speed and cost. **Adding a model is data rather than a code change**, and the catalog, the
   router and the metering all read that one spec.
8. **Metering and credits.** Every generation is metered by output unit and drawn from an
   account credit balance or billed against a plan. Cost is recorded per model, per endpoint
   and per team, shown in near-real-time, and billed on one consolidated invoice. Spend limits
   and alerts are enforced before a job runs rather than after. One balance serves the studio,
   the interface and the connector alike.
9. **Provenance.** Generated media carries a tamper-evident signed credential recording that
   the content is machine-generated, which model produced it and when, embedded in the export
   and verifiable by a public checker. Provenance survives the blended timeline at clip
   granularity, so a mixed export can declare which frames are synthetic, and removing the
   credential is detectable.
10. **The connector protocol.** The engine is reachable from external chat and coding agents
    through a standard connector: the user registers the connector address in their agent and
    signs in with their platform account, with no separate key, after which the agent invokes
    generation as tools and receives the streamed results inline. Generations invoked that way
    meter against the same balance and honour the same plan and model access.

## User flow

### Routes

The information architecture is one public marketing tree, one public developer tree and
one signed-in editorial tree, and the route table below is that architecture written out.

| Route | Purpose | Auth |
|---|---|---|
| `/` | Marketing home, eleven sections, light | public |
| `/api-platform` | Developer portal, dark, its own slim chrome | public |
| `/mcp` | Agent connector, light | public |
| `/news` | Published news items, newest first | public |
| `/news/{slug}` | One published news item | public |
| `/models` | The model catalog as a comparison table | public |
| `/models/{slug}` | One model record with its full spec | public |
| `/pricing` | Plans and the per-second model prices | public |
| `/privacy` | Privacy page, linked from every footer | public |
| `/terms` | Terms page, linked from every footer and from the sign-up form | public |
| `/signup` | The sign-up form, the one public action that touches state | public |
| `/login` | Sign-in | public |
| `/media/{key}` | The product's own media route, the only public path to a stored object | public for a public object |
| `/sitemap.xml` | Every public route | public |
| `/robots.txt` | Points at the sitemap | public |
| `/favicon.ico` | The site icon | public |
| `/studio` | The signed-in editorial home | any account |
| `/studio/news` | The author's own news items, drafts included | `author` |
| `/studio/news/{id}` | One item, with the compose panel over the list | `author`, owner only |
| `/studio/models` | The model records as an editable table | `author` |
| `/studio/models/{id}` | One model record | `author`, owner only |
| `/studio/account` | The signed-in account's own settings | any account |
| `/api/health` | Readiness | public |

### Entry and redirects

An unauthenticated request to any `/studio` route lands on `/login` with the intended route
preserved, and returns there after signing in. Signing out revokes the session on the server
and lands on `/`. A token that expires mid-compose returns the author to `/login` with the
composed work preserved and restores it after signing in again. A signed-in `reader`
requesting a compose route is told which permission is required and which role holds it. An
anonymous request for an unpublished item, or for a private object, answers exactly as a
request for something that does not exist. Any other unresolved address renders the
not-found shell and answers not-found.

### Journeys

**A visitor signs up.** Open `/`. The hero fills the viewport with a dark tile and the line
`Building Real-World Intelligence`. Open the `Dev` item in the top bar; a mega-menu drops a
panel of destinations and the chevron flips. Follow it to `/api-platform`. Read the four
capability columns, scan the model comparison table, and use the copy control on the code
panel; the text-to-video sample is now on the clipboard. Open `/signup`, enter an address
and a password, submit. The result is a full-page confirmation naming the account, and
signing in with those details works.

**An author drafts an item.** Sign in as `author@example.com`. Open `/studio/news`. The
list shows four items with their statuses. Choose the create action; a panel slides over the
list and the list stays on screen behind it. Enter a title, a dek, a body and alternative
text, attach a poster, save. The panel closes, an inline banner confirms the save, the item
appears in the list as `draft`, and `/news` does not show it.

**A draft stays private.** Sign out. Request `/news/the-media-router-preview`. The response
is exactly what `/news/no-such-item-at-all` returns. Copy the draft poster's key from the
studio and request it at `/media/{key}`. The response is exactly what a key that does not
exist returns. The object is still in the store, and the item is unchanged.

**Publication is one act.** Sign in as `author@example.com`, open the draft, publish. The
result is a full-page confirmation. `/news` now lists the item, `/news/the-media-router-preview`
reads, and the poster fetches. No other item changed status.

**Alternative text gates publication.** Create an item whose poster carries empty
alternative text and attempt to publish. The attempt is refused, the refusal names the
field, and the item is still `draft`.

**Cross-author isolation.** Signed in as `author@example.com`, request
`/news/partner-campaign-preview`, which `author2@example.com` owns and has not published.
The response is the same refusal an anonymous caller gets, and the poster is not fetchable.

**A reader reads.** Sign in as `reader@example.com`. `/news` lists the published items only.
`/studio/news` is refused with the permission named. The draft is unreadable and its poster
is unfetchable.

### States

Every list carries an empty state that names what to do next and offers the primary creating
action, and a separate filtered-to-empty state that names the active filter and offers to
clear it. Every route has a loading state: the document arrives complete and each media tile
holds its poster until its stream attaches. Denied and not-found are deliberately the same
response for an anonymous caller and deliberately different for a signed-in one. A degraded
dependency replaces its own region with a retry control naming what is unavailable while the
rest of the page works. Errors never crash the page: an error screen carries a copyable
correlation identifier, says whether retrying can succeed, and shows no stack trace, no
internal identifier and no hint that a hidden item exists.

## UI/UX notes

The north star is that somebody arriving on the home page understands in the first moment
that this company turns typed words into moving pictures, and that the work is cinematic
rather than technical. On the developer portal the north star changes: a reader should be
able to decide on that page whether the platform is worth calling, from what the models do,
what they cost and what the code looks like.

Two registers run off one token set, and the split is the design's structure. The marketing
surfaces are consumer and editorial: light, spacious, atmospheric, with the subject, a moving
image, seen first and largest. The developer portal is operational: dark, dense, comparative,
built for a reader checking numbers rather than being moved. The signed-in studio follows the
portal's register, because an author publishing late at night is doing repeated work. When
the two disagree, the image wins on a marketing surface and the number wins on the portal.

Colour is one token set with a light projection and a dark one, never two systems. On light
the page ground is a near-white neutral and primary text a near-black neutral; on dark those
two exchange places, the ground becoming a near-black neutral and the text a near-white
neutral. A raised panel sits one step off its ground on either projection. Borders and
dividers are a deep cool neutral in both. Muted body text is a light cool neutral, with a
second, lighter cool neutral above it for text that must recede further. Scrims are a
near-black neutral at low alpha.

The accents are one warm-to-cool spectrum shared by both projections: a light, soft magenta
and a light, soft indigo, which together make the signature gradient; a near-white, soft
blue as the soft violet; a light, soft orange as the warm accent; a light, muted green as
the positive accent; a light, vivid blue as the electric accent; a light, vivid red as the
alert, with a mid, vivid red for its pressed state. **The signature gradient is a
top-to-bottom wash from the magenta into the indigo, it appears on accent chips and highlight
strokes, and it appears nowhere else.** A state that is neither positive nor alert borrows
neither of their colours. A translucency ladder of white and black at fixed steps carries
every glass surface, every border on dark and every scrim: pick a step from the ladder, never
invent an alpha. The exact shades are yours, so long as every role stays separable in both
projections.

Three families carry the product, and each is named exactly because a font is an identity
rather than a value to echo. The interface and body face is a grotesque sans, `Inter`, at
`300`, `400`, `500` and `600`, falling back to `"Helvetica Neue", "Arial", sans-serif`. The
display accent is a high-contrast serif, `Playfair Display`, at one weight, falling back to
`Georgia, "Times New Roman", serif`, and it is reserved for display moments rather than used
as a second body face. Code is a monospace, `IBM Plex Mono`, at `400`, falling back to
`"Menlo", "Monaco", "Consolas", "Courier New", ui-monospace, monospace`.

The rendered scale, most-used first: body at `16px` over `24px` at `400`; lead at `22px`
over `29.7px` at `400`; dense body at `16px` over `20.8px` at `400`; small at `14px` over
`22px` at `400`; label at `14px` over `17.5px` at `500`; micro at `13px` over `16.9px` at
`400`; badge at `11px` over `14.3px` at `450`; title at `24px` over `24px` at `400`. Above
them sit the display and heading steps, named rather than sized: a display medium, a display
large, a display extra-small, five heading levels, a large and a small paragraph, a caption,
an eyebrow, a body-copy variant and a call-to-action step. Text never disappears while a
face downloads: the fallback shows and is replaced.

Corners soften in a small ladder. The workhorse softening belongs to cards and inputs;
buttons and small chips sit one step tighter; the code panel and the hero tile take a step
looser than a card; and the call-to-action text buttons and the circular media controls are
full pills. Depth is layered rather than shadowed: the sticky header floats above the page,
menus and overlays above the header, modal surfaces above those. The one real shadow is the
soft drop beneath a developer capability column; dark cards take their depth from a radial
glow behind the art instead.

Density is spacious on the marketing surfaces, where the subject needs room around it, and
compact on the portal and in the studio, where a reader is comparing and an author is
repeating. The layout archetype is a top navigation: a sticky bar carrying the wordmark at
the inline start, seven items in the centre each opening a mega-menu, and three actions at
the inline end, transparent over the dark hero and opaque once scrolled. The portal wears
its own slimmer bar with no mega-menu. Inside the studio the model catalog is a table first:
one row per model with the same columns in the same order, so two models compare by eye
without either being opened, and the card rail survives beside it as the browsing view on
the portal. Composing an item opens a panel that slides over the list it belongs to, so the
list stays on screen. Two acts end a task rather than continuing one, and both land on a full
page: completing the sign-up form, and publishing an item. Everything else confirms inline.

Motion is quick and understated, and one house curve does almost all of it: a smooth start
and a smooth stop. A snappier curve carries colour and navigation changes, an ease-in
carries exits, and an expressive curve with a long tail carries the showier reveals.
Durations cluster into a fast state change, a default, and a deliberate one for anything
larger than a control. The named moments are a plain fade in; a paired enter and exit for
modals and popovers; a drawer that slides in from the inline end and back out; a popover that
drops a short distance while it fades; a centred toast that rises as it appears; a spin for
loading; a pulse for a pending state and a gentler one for a loading avatar; a first-run
intro that reaches full strength a third of the way through and then holds; the trusted-by
marquee, which drifts endlessly and linearly and takes well over a minute for a lap, run on
a timer rather than on scroll position; the code panel's linear one-shot fade-in when a language
tab changes, which holds its end state; and the mega-menu chevron flipping as its panel opens.
Only transform and opacity animate on the marquee and the carousels, so neither ever forces
the page to re-lay-out. **Under reduced motion the marquee holds still, every keyframe enter
collapses to its end state, and a video poster replaces autoplay**; nothing becomes
invisible and nothing is left mid-travel.

Accessibility is contract, not taste. Text and its background meet WCAG AA contrast in both
projections, and the muted tone is reserved for large or secondary text where it would not.
The whole product is operable by keyboard navigation with a visible focus ring, including
the mega-menu, the switcher tabs, the carousels, the accordion and the media controls.
Icon-only controls announce the action rather than the icon, so the pause control says pause
and play rather than naming a glyph. A link that opens a new tab says so. Landmarks are one
banner, one contentinfo and one main per route. **Every content image carries alternative
text, and a decorative image declares itself decorative rather than carrying an empty
description by accident.** Status carries a second signal beyond colour.

Responsive behaviour holds at every width between the tiers rather than only at them. At the
narrowest the sections stack to one column, the multi-column footer and the four-column bento
fold, and the switcher and the carousels become swipeable. **Whether a control responds to a
pointer hovering is decided by whether the device has a hover-capable pointer rather than by
viewport width**, and every hover affordance has a tap equivalent, so nothing depends on
hovering. The page never scrolls sideways at any width. The layout survives text scaled well
beyond its default without losing content or function.

What this must not look like: no page dominated by a single hue family with no second signal;
no decoration standing in for content; no developer portal that reads as a marketing page and
no marketing page that reads as a dashboard; no model card whose spec order differs from the
card beside it, which is what makes a catalog uncomparable; and no media tile that shows an
empty rectangle while it loads. **Atmosphere over density on the marketing surfaces,
comparability over atmosphere on the portal. Space over dividers. Stillness over feedback
while somebody is signing up.**

## Front-end specification

Everything in this section is front of house: how the product looks, moves, reads and is
laid out. Business rules live above.

### One token set, two projections

The product runs two palettes off one set of named tokens. Build the tokens once and project
them light and dark; do not build two systems that happen to agree.

The neutral roles, named by what they do rather than by a value. A near-white neutral is the
light page ground and is also the text colour on the dark projection, and it is the most-used
value in the whole system. A near-black neutral is the primary text on light and the fill of
the dark hero. A deep cool neutral is the secondary dark surface. A deep neutral is the
tertiary dark surface. A near-black neutral at full strength is the pure overlay. A second
near-black neutral, distinct from the text one, is the developer portal's page ground. A deep
cool neutral carries borders and dividers on dark. A light cool neutral is muted body text,
and a second, lighter cool neutral is the text that must recede further still. A near-black
cool neutral is the developer portal's raised panel. A deep neutral is the lowest interface
layer.

The accent roles: a light, soft magenta is the gradient's start; a light, soft indigo is its
end; a near-white, soft blue is the soft violet; a light, soft orange is the warm accent; a
light, muted green is the positive accent; a light, vivid blue is the electric accent; a
light, vivid red is the soft alert and a second, sharper light, vivid red is the alert
proper; a light, vivid red is destructive and a mid, vivid red is its pressed state; and the
focus ring is a mid, vivid blue at partial strength.

**The signature gradient** is a top-to-bottom wash from the magenta into the indigo. It is
the one thing a reader will remember of the palette, and rationing it is what makes it
memorable: accent chips and highlight strokes, and nothing else.

**The translucency ladder** is white at a rising series of fixed alphas and black at its own
rising series, and every glass surface, every border on dark and every scrim picks a step
from it. Inventing a new alpha instead of taking a step is how a system with one ladder ends
up with forty values.

### Type, in detail

Three families, named above with their fallbacks. The interface face carries four weights;
the display serif carries one; the monospace carries one.

The rendered scale is given in `## UI/UX notes` with its sizes, line heights and weights, and
it is exact. The named steps that sit over it are a display medium, a display large, a
display extra-small, five heading levels, a large paragraph, a small paragraph, a caption, an
eyebrow, a body-copy variant and a call-to-action text step. Map each onto the scale; do not
invent a step outside it.

The hero heading and its lead carry a soft, wide, low-opacity shadow so they stay legible
over an arbitrary video frame. It is the only text shadow in the product.

### Shape, spacing and layering

The radius ladder, by role rather than by value: the smallest step belongs to the tightest
chips; one step up is buttons and small chips; the workhorse is cards and inputs; above that
sit media tiles; above that the code panel; and at the top the full pill, worn by
call-to-action text buttons and by the circular media controls. Circular arrow buttons on the
carousel are true circles rather than pills.

Spacing comes off one rhythm rather than being chosen per section: a small step inside a
control, a larger one between controls, a larger one again between a heading and its body,
and the largest between one section and the next. Layout is a centred column. Marketing
sections run full-bleed with an inner measure; the portal's bento and the studio's lists
sit inside the same measure. The developer portal's own
chrome has a fixed height and the page below it starts at a fixed gap, so its bar and its
first section never crowd.

Layering is explicit and has four levels: page content, the sticky header above it, overlays
and menus above that, and modal surfaces at the top. A dialog that must sit above everything
has its own topmost level. Nothing invents a level between two of them.

### Easing and the animation catalogue

Four easings carry everything, named by character rather than by number: the house curve,
which starts smoothly and stops smoothly; a snappier one for colour and navigation; an
ease-in for exits; and an expressive one with a long tail for the showier reveals. The
runtime animation catalogue is the named list in `## UI/UX notes`, and every animation in
the product is one of those entries rather than a new one invented at the call site.

### Iconography

**Icons are drawn as geometry and never shipped as files.** Each is a small set of strokes at
a square box, painted with the current colour so the surrounding token decides the colour,
with round caps and joins and a consistent hairline stroke unless a mark says otherwise.

The interface set: a chevron pointing down and one pointing right; an arrow right, an arrow
left and an arrow pointing up and to the right; a copy mark of a square over a partial square;
a pause mark of two vertical bars; a globe of a circle crossed by one horizontal line and one
elliptical meridian; and a mute mark, a speaker with the sound arcs struck through by a
diagonal.

The brand and utility marks: a six-glyph lowercase wordmark on a wide short box, substituted
by your own six-letter mark at the same proportion; a three-bar menu mark of three stacked
rules on a wide short box; a social mark; a four-quadrant sign-in mark; and an application
mark of four squares in a two-by-two grid. **Partner logos are never reproduced**: each
becomes a name-tile carrying the partner's placeholder name.

### Global chrome

**The marketing header** is a sticky top bar on the header layer, transparent over the dark
hero and opaque once scrolled. At the inline start, the wordmark. In the centre, seven
top-level items, each a text label beside a downward chevron that opens a mega-menu:
`Creative`, `Dev`, `Robotics`, `Research`, `Resources`, `Enterprise`, `Pricing`. At the
inline end, three actions: `Enterprise Sales` and `Login` as text, and `Try Lumina` as a
filled dark pill. On the light document the wordmark and the links are the near-black
neutral; over the dark hero they invert to the near-white neutral.

**The mega-menu** drops a panel of destination columns when a top-level item is opened, and
the chevron flips as it does. Its links carry an underline on hover. The destinations are:

- `Creative`: `Overview`, `Agent`, `Android app`, `iOS app`, `MCP`, `Use Cases`, `Pricing`,
  `Login`.
- `Dev`: `Platform`, `Models`, `Model Router`, `Workflows`, `Recipes`, `Characters`,
  `Documentation`, `Pricing`.
- `Robotics`: `Overview`, `Policy Model`, `Offline Policy Evaluation`, `Data Augmentation`,
  `Video Model Licensing`, `Get Access`.
- `Enterprise`: `Overview`, `Data Security`, `Customer Stories`, `For Education`,
  `Contact Sales`.
- `Research`: `Research Hub`, `Research News`, `Publications`, `General World Models`,
  `Worldscape-1`, `Nova-4.5`, `Chisel-2.0`, `Perform-2`.
- `Resources`: `Academy`, `Help Center`, `Resource Hub`, `News`, `Changelog`, `Meetups`.
- `Events & Programs`: `AI Festival`, `AI Summit 2026`, `Gen:48`, `Studios`,
  `Creative Partners Program`, `Lumina Builders`, `Affiliate Program`, `Talent Network`.
- `Company`: `About Us`, `Careers`, `Safety`, `Verify Content Credentials`,
  `Brand Guidelines`, `Press`, `Partnerships`.

**The developer-portal header** is a separate, slimmer chrome at a fixed height. At the
inline start a `Lumina Dev` lockup, which carries that text as its accessible name even
where it renders as a mark. Beside it `Explore` and `Docs`, with `Docs` opening in a new tab
and marked by an up-right arrow. At the inline end `Log In` as a ghost button and `Sign Up`
as a filled one. It carries neither the mega-menu nor the marketing footer.

**The footer** is a large multi-column sitemap on every marketing route, grouped under eight
headings: `Creative`, `Dev`, `Robotics`, `Enterprise`, `Research`, `Resources`,
`Events & Programs`, `Company`, carrying the destinations listed above. Under a divider sit a
copyright eyebrow reading `(c) 2026 Lumina AI, Inc.` and a slash-separated legal row:
`Terms of Use`, `Privacy Policy`, `California Notices`, `Cookie Settings`,
`Code of Conduct`, `System Status`.

**The measured hover behaviour**, which is the chrome's whole craft:

- A marketing navigation link and a call-to-action text button ease their label from full
  strength to a soft light neutral, and the doubled-glyph layers behind the label ease with
  it, which is what makes the wipe read as crisp rather than as a fade. On the light document
  the same link runs from the near-black neutral to that same soft light neutral.
- A filled pill eases its background one step darker on the dark projection and one step
  cooler on the light one, over the fast duration.
- A developer navigation link raises its opacity from partial to full and warms its colour.
- A developer secondary button inverts outright: its label goes from the near-white neutral
  to a near-black one, its background from transparent to the near-white neutral, and its
  border from the deep cool neutral to the near-white neutral.
- A ghost button drops slightly in opacity rather than changing colour.

### The media surface, in detail

**The tile.** A rounded container clipped to its own radius, with hero tiles a step looser
than card tiles. Three stacked layers: a poster, a video and an overlay.

**The poster layer.** A sharp still frame, and behind it a low-resolution copy that is blurred
heavily and scaled up very slightly so the blur bleeds past the frame edge rather than
stopping at a visible line. That bleed is the detail worth keeping; without it the blurred
backing reads as a second rectangle.

**The video layer.** Muted, looping, playing inline, autoplaying only when the tile is in
view, and delivered in segments so it starts quickly rather than after a whole file arrives.

**The overlay layer.** A bottom-anchored gradient scrim, fully transparent for the top half
of the tile and darkening to a strong but not opaque black at the bottom edge, so a caption
survives any frame. The controls sit on this layer.

**The crossfade.** The sharp poster holds at full strength; the moment the video's first
frame is decoded, the poster eases away and the video is revealed beneath it. The tile is
never empty and never flashes.

**The controls.** Small circular buttons pinned to a tile corner on the overlay layer, each a
full pill with a blurred backdrop and a layered ring made of a hairline light stroke and a
soft dark drop. Two of them: pause and mute. Each announces what it will do, and the
announcement flips between pause and play, and between mute and unmute, with the state.

**The logo marquee.** A horizontally translating track under an edge-fade mask that is
transparent at both edges and opaque across the middle, with the track duplicated head to
tail so the loop never shows a seam. It is a linear, endless animation on a timer, taking
well over a minute for a lap, and it is not tied to scroll position.

**The model-card rail.** A horizontal rail under a one-sided fade mask, opaque until near the
trailing edge and transparent at it, advanced by circular arrow buttons that drop to a low
opacity when there is nothing further in that direction.

**The grain.** A tiling fractal-noise texture at low opacity in an overlay blend over the
connector page's dark panels, desaturated so it reads as tonal grain rather than colour
speckle.

**The card glow.** Developer cards take their depth from a radial wash behind the art,
running from a deep rose at the upper left through a darker rose to a near-black neutral,
rather than from a shadow.

### Route: the marketing home

Title: `Lumina | Building Real-World Intelligence`. Light document. Eleven sections.

The hero copy, exactly: the display heading `Building Real-World Intelligence`; the lead
paragraph `Lumina is building foundational Real-World Intelligence that can understand,
simulate and act in the world. We offer products and services built on-top of this
intelligence to empower individuals and organizations to do more in the world.`; and the
primary action `Try Lumina for free`.

The partner marquee's eyebrow, exactly:
`We partner with the world's leading organizations to advance their industries:`.

The switcher's section heading, exactly:
`Three platforms built on-top of the same Real-World Intelligence models`. Its three panels:

| Panel | Display line | Body | Actions |
|---|---|---|---|
| `Lumina Creative` | `Your complete Creative Suite with everything you need, to make anything you want.` | `An all-in-one cloud-based creative platform that offers endless ways to generate and edit video, images and audio in one workspace. Built for individuals and teams of all sizes.` | `Try now`, `Learn more`, `For Enterprise` |
| `Lumina Dev` | `The AI media platform for developers to build with the best models from Lumina and other labs.` | `The API platform with Lumina's expertise built in. Access the best models and the creative tooling to easily get production-ready output from them, at scale.` | `Get API Key`, `View documentation`, `For Enterprise` |
| `Lumina Robotics` | `A complete toolkit to run policy inference through photorealistic simulation.` | `From policy inference and evaluation to synthetic data generation, every component is powered by Worldscape-1, our state-of-the-art General World Model. Pick the surface you need, we'll work with you to fit it to your hardware.` | `Learn more`, `Contact Sales` |

Under the Creative panel a caption reads
`Used by 60m+ creatives around the world. Try free, cancel anytime.` The three tab labels sit
above a rule along which the active underline slides.

The research band carries the eyebrow `Lumina Research` and the heading
`We are building foundational General World Models that will be capable of simulating all
possible worlds and experiences. The next frontier of intelligence will come from models that
can understand, perceive, generate and act in the world.`, with a `Learn more` link, over a
living green field under a darkening overlay. Its three research cards:

- `Worldscape-1`: `A state-of-the-art General World Model built to interact with the real
  world. And a major step towards universal simulation.`
- `Nova-4.5`: `The world's best video model, featuring state-of-the-art motion quality,
  prompt adherence and visual fidelity.`
- `General World Models`: `Our long-term research effort to build AI systems that understand
  the visual world and its dynamics.`

The news grid carries the heading `See the latest from Lumina` and seeds four cards:

- `Introducing Lumina Media Router` / `Lumina Media Router is the first preference-optimized
  router for generative media, built into the Lumina Dev platform.`
- `How Partner 1 Used Lumina to Produce Their Latest National TV Spot` / `Partner 1 turned
  photos from nearly 100 real members into a broadcast-ready TV campaign using Lumina, saving
  $200K on a single clip.`
- `The AI Media Report: Cost, Speed and What Comes Next` / `Our findings from hundreds of
  enterprises using Lumina for media production: cost and speed gains and the creative shifts
  ahead.`
- `Lumina Opens London HQ, Bringing World Model Research Hub to the UK and Europe` /
  `Announcing London as Lumina's new European headquarters and world model research hub, with
  a planned $100M investment in the UK AI ecosystem and a new Head of Europe.`

### Route: the developer portal

Title: `Lumina Developer Portal`. Dark document. Its hero title reads `The AI Media Platform`
over `for Developers`, its subtitle `The best image, video, audio and real-time models. One
enterprise-grade platform.`, and its actions `Get API Key` and `Explore Models`. The
trusted-by marquee is labelled `Trusted by`.

The capability bento carries the heading `One API for production` over `media generation.`
and the subtitle `Deploy the best media models, generation workflows and interactive avatars
through a single integration, with the visibility and controls to build at scale.` Its four
columns:

| Label | Title | Description | Action |
|---|---|---|---|
| `Access` | `Every capability, one integration` | `Models, Workflows, Recipes and Characters, all accessible through a single API.` | `Get API Key` |
| `Evaluate` | `Compare before you ship` | `Run the same prompt across models. Score by quality, speed and cost before committing to production.` | `Evaluate models` |
| `Automate` | `Let the platform pick` | `Set a preference for cost, latency or quality. The platform routes every request to the best model automatically.` | `Set up a Router` |
| `Control` | `Monitor spend across models and teams` | `Full visibility into cost per model, per endpoint, per team. One invoice for everything.` | `View usage` |

The `Automate` column carries a `NEW` badge. A column's action inverts on hover: its label to
the near-black neutral, its background to the near-white neutral, its border from the deep
cool neutral to the near-white neutral.

The router section carries the heading `Model Routers for` over `Optimization`, the
description `Set a priority for cost, latency or quality and a price ceiling once. Call one
endpoint and Model Router picks the right model for every request.`, and the action
`Set up a router`.

The integration section carries the heading `Seamless Integration`, a category row of
`Models`, `Workflows`, `Recipes` and `Characters`, and a language row of `Node`, `Python`
and `cURL`. The Node sample, verbatim, is selectable text beside a copy control:

```js
import LuminaClient from '@lumina/sdk';

const client = new LuminaClient();

const task = await client.textToVideo.create({
  promptText: "A cinematic slow push-in across a sunlit kitchen as steam curls from a fresh cup of coffee, soft morning light, gentle natural motion.",
  model: "Nova-4.5",
  ratio: "1280:720",
  duration: 5,
  seed: 692126734
}).waitForTaskOutput();
```

The create-then-wait shape is the task lifecycle stated in `## Core features`, and the sample
is the contract's own documentation.

The catalog section carries the heading `State-of-the-art` over `Models`, the description
`Serving models from providers across the industry, including Lumina's own foundational
models.`, and the actions `View all models` and `View SDK docs`. Each model card and each
table row carries a name, a tagline and a spec list in one fixed order:

| Model | Tagline | Resolution | Aspect ratios | Inputs | Max duration | Price |
|---|---|---|---|---|---|---|
| `Nova-4.5` | `Balanced everyday video generation` | `720p` | `16:9, 9:16, 4:3, 1:1, 3:4, 21:9` | `Text, Image` | `Up to 10s` | `$0.12/sec` |
| `Chisel-2.0` | `Precise video editing` | `Matches input` | `16:9, 4:3, 3:2, 1:1, 2:3, 3:4, 9:16, 21:9` | `Text, Video` | `Up to 10s` | `$0.18/sec` |
| `Worldscape-1` | `General world simulation` | `720p` | `16:9, 1:1` | `Text, Image` | `Up to 10s` | `$0.30/sec` |
| `Perform-2` | `Performance capture` | `Matches input` | `16:9, 9:16, 1:1` | `Video` | `Up to 10s` | `$0.09/sec` |

Each card carries the links `View documentation` and `Try in Playground`.

### Route: the agent connector

Title: `Lumina Agent Connector | Generate video from your assistant`. Light document.

Its hero heading reads `Lumina Agent Connector` over three stacked lines: `Generate
high-quality images and videos right from where you're already working.`, `Use Lumina in your
assistant, coding tools and other compatible agents.`, and `Access Partner model, Nova-4.5
and more right from your conversation.` Its action is `Connect`, above a row of agent buttons
naming an assistant, a chat tool, an editor and a coding sandbox.

The setup section carries the heading `Connect Lumina in seconds` and the subhead `Setting up
the Lumina connector is simple and takes just a few moments.`, over three numbered steps:

1. `Go to your assistant, Customize` / `In the desktop or web app, go to Customize, then
   Connectors.`
2. `Add custom connector` / `Name it Lumina and paste the link:` beside a monospace field and
   a `Copy` control.
3. `Connect and sign in` / `Click Add, then Connect, sign in with your Lumina account. Then
   ask your assistant to make an ad video.`, with a `View setup guide` link.

The showcase carries the heading `A complete generation studio,` over `inside your agent.`
and four alternating rows, each an eyebrow, a title, a body line and a chat demonstration
whose prompt bubble sits on a near-white neutral:

- `Image and video` / `Generate images and videos` / `Explore ideas, restyle product shots and
  turn early concepts into images or videos without leaving the conversation.` Prompt:
  `Generate 2 product images for this chocolate.`
- `Product marketing` / `Create marketing content from a link` / `Send your agent a link to
  your product and ask Lumina to create a polished marketing video.` Prompt: `Use this product
  URL to create a polished marketing video for launch:`.
- `Multi-shot storytelling` / `Make dialogue-driven ads` / `Write the line, set the scene and
  let Lumina build a character-led product ad.` Prompt: `Make a playful dialogue-driven
  product spot with two crabs and a can of Fizz. One crab says 'don't be so shellfish.'`
- `Product sites` / `Add stunning product imagery to your site` / `Give your agent an image of
  your product and ask Lumina to create the images and videos you need for your marketing
  site.` Prompt: `Can you use Lumina to generate a hero video for these jewelry products, and
  make a shopping website?`

The pill row carries the heading `Access to the latest state-of-the-art models` above a
wrapping row of model-name pills. The prompt gallery carries the heading `Just tell your agent
what you need.` over `Lumina handles the rest.` and four prompt cards labelled
`Product URL to marketing video`, `Creative Product ad`, `Image to product ad` and
`Product image to dialogue ad`, below which sits a composed chat input showing an add
affordance and a `Write a message...` field.

The accordion carries the heading `Frequently asked questions` and four independently
expandable rows. Each answer sits in the document at first render, hidden by a style rule:

- `What agents can connect to Lumina Connector?` / `You can use the Lumina Connector in your
  assistant's web and desktop apps, coding tools and other apps that support the connector
  protocol.`
- `Which models can agents use?` / `Your agent can use models like Nova-4.5 and several
  partner models based on your Lumina account plan. It can pick a model for you, or you can
  ask for a specific one.`
- `How are connector generations billed?` / `It uses your Lumina credits, just like the app.
  The cost depends on the model, resolution and other settings. You can manage everything from
  your Lumina account.`
- `Is an API key required?` / `No. Add the Lumina connector link to your agent settings, then
  sign in with your Lumina account.`

### Route: the not-found shell

The full marketing header and footer around a centred body: a heading reading
`This page doesn't exist.` and a pill reading `Take me home` linking to the home route. It is
a real surface rather than an error page, and every destination the site has is reachable
from it.

### Component and module architecture

The component architecture is one library of presentation modules over the token set, with
the page routes as thin modules that compose them. A component library over the tokens, themed light and dark from one source: a header in
marketing and developer variants, a mega-menu, a footer, a media tile carrying its poster,
video, overlay and controls, a logo marquee, a card carousel with arrow buttons, the platform
switcher, a research card, a news card, a capability column, a code sample with language and
category tabs, a model card, a chat demonstration, a step list, an accordion, buttons in
filled, ghost, secondary and pill forms, badges for `NEW` and `Enterprise`, and the not-found
shell. Build the kit once and assemble the pages from it; three pages built separately end up
with three headers.

### Responsive, in detail

The width tiers cluster at a phone width, a small-tablet width, a tablet width and a desktop
width, with a wide-desktop tier above them and a floor for very small devices. Documents grow
substantially at the narrowest tier because sections stack rather than sitting side by side,
and that growth is expected rather than a defect.

At the narrowest tier the sections stack to one column, the eight-column footer and the
four-column bento fold to one, and the switcher and the carousels become swipeable. Pointer
capability rather than width decides whether hover affordances apply, and every one of them
has a tap equivalent.

### Accessibility, in detail

Landmarks are one banner, one contentinfo and one main per route. The focus ring is visible
on every control and is never suppressed. Every custom control is keyboard operable: the
mega-menu opens and closes and its items are reachable; the switcher tabs move by arrow keys
with only the active tab in the tab order; the carousel arrows are buttons; the accordion
rows toggle independently on enter and space; and the media controls are buttons carrying
their action as their name.

Icon-only controls announce the action: `Pause`, `Unmute`, and the developer lockup carries a
visually hidden `Lumina Dev`. A link that opens a new tab carries `(opens in new tab)` in its
accessible name. Contrast holds in both projections: the near-black text on the near-white
ground and the near-white text on the near-black ground both clear the threshold, and the
muted light cool neutral is reserved for large or secondary text. Motion respects the
reduced-motion preference in every place that moves.

### The zero-asset substitution guide

**No binary ships.** Each entry below is a substitution: what the reference would have
shipped as a file, and what is generated in its place. No image, no video, no font file, no icon file. Every one is produced
from a recipe, and the recipes are part of the build rather than a fallback.

- **Fonts.** Each family is named with a normative fallback stack and loaded so the fallback
  shows rather than leaving text invisible. Naming an open substitute is not an asset
  dependency; shipping a font file is.
- **Video.** Placeholder clips are generated: a looping canvas or animated wash of the
  signature gradient drifting over the near-black neutral field, either exported to a short
  muted loop or rendered live behind the tile. The poster-first, swap-when-ready contract is
  unchanged; the placeholder plays a gradient loop rather than footage. **Say plainly in the
  build that the placeholder communicates the tile's behaviour rather than its content.**
- **Posters and imagery.** Canvas-generated gradient placeholders keyed by a seed, so the same
  record always yields the same image. A card uses the radial rose-to-near-black wash with a
  soft grain over it; a background poster is the same at low resolution behind a heavy blur.
- **Logos.** Partner and customer marks become name-tiles: the placeholder name set in the
  interface face on a neutral chip at the card softening, greyscale on the light surface and
  the near-white neutral at reduced opacity on the dark. The real marks are never reproduced.
- **Grain.** An inline fractal-noise texture at low opacity in an overlay blend, desaturated
  so it reads as tonal grain.
- **The favicon** is generated from the same wordmark geometry rather than shipped, and is
  declared in the document head.

## Technical requirements

This is the one section that names the stack. Everything below is a requirement on
the running system rather than a recipe for reaching it; how the code is arranged is
yours.

### The stack

The application is rendered on the server with hydrated islands: the document arrives
complete from the server, and only the parts that genuinely need behaviour become
interactive in the browser. The mega-menu, the platform switcher, the carousels, the
accordion, the code panel's tabs and the media tiles are islands. The hero copy, the
capability bento's text, the model table, the footer sitemap and the not-found shell
are not, and they must read with scripting unavailable.

- **Back end:** `FastAPI` on `Python 3.11+`, served by `uvicorn`. The same process
  serves the rendered documents, the JSON endpoints and the media route.
- **Front end:** `Astro` with islands, styled with a utility-class system over the
  token set described above, and built to static output that the back end serves.
- **Database:** `PostgreSQL 16`, reached at the connection string in `DATABASE_URL`,
  which is also supplied as `DB_URL` with the same value. Every record in
  `## Data model` lives here.
- **Object store:** the S3-compatible `minio` instance, reached through its HTTP API.
  Every uploaded byte lives here.
- **Sessions:** server-side, with an opaque cookie that is HTTP-only, same-site and
  marked secure behind TLS. A signed-in session is revocable from the server, and
  signing out revokes it rather than only clearing the browser's copy.

Naming a framework here does not license naming one anywhere else: the reader of
`## Core features` is being told what the product does, not what library does it.

### The server rendering contract

The first document for every route in `## User flow` arrives from the server already
carrying its content. A view-source of `/` shows the hero heading, the switcher's
three panel bodies and the footer's destinations as text. A view-source of
`/api-platform` shows all four capability columns and every model row with its specs.
A view-source of `/news` shows the published items' titles and deks. An empty shell
that fills in after a round trip to a JSON endpoint does not satisfy this, and a
crawler that executes no scripts must still see the content.

Islands hydrate after the document is readable, never before. The accordion's answers
are in the document at first render and hidden by a style rule, so a reader without
scripting can still reach them and a crawler can still index them.

### The media route and the object store

The store is reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`
and `STORAGE_SECRET_KEY`. The bucket holds no anonymous read policy, and a reader
reaches an object only through one of the two mechanisms named in `## Core features`:
the product's own media route, or a presigned address valid for at most five minutes
that is never issued for a private object. Pick one and hold to it.

A request to the media route resolves the key to the item that owns it, then decides.
A public object streams back with a content type matching the stored object and a
caching header appropriate to something that never changes at that key. A private
object answers exactly as a key that does not exist answers, and the decision is made
before any byte is read from the store. The bytes must be in the store: a copy kept on
the application's own disk, or a record holding the image inline, does not count.

### Endpoints

Every mutating endpoint is authorized on the server against the calling session, and
the check happens before the work rather than after it. The read endpoints filter by
what the caller is entitled to see, which is what makes the draft-versus-missing
responses identical without any special-casing at the edge.

| Endpoint | Method | Who | Effect |
|---|---|---|---|
| `/api/health` | read | anyone | reports readiness, naming the database and the object store separately |
| `/api/auth/signup` | write | anyone | creates an account and starts a session |
| `/api/auth/login` | write | anyone | starts a session |
| `/api/auth/logout` | write | a session | revokes the session on the server |
| `/api/news` | read | anyone | published items, newest first, paginated |
| `/api/news/{slug}` | read | anyone | one published item |
| `/api/studio/news` | read | `author` | that author's own items, drafts included |
| `/api/studio/news` | write | `author` | creates a draft |
| `/api/studio/news/{id}` | write | owner | edits a draft the caller owns |
| `/api/studio/news/{id}/media` | write | owner | uploads a poster and returns its key |
| `/api/studio/news/{id}/publish` | write | owner | publishes, in one transaction |
| `/api/studio/news/{id}/unpublish` | write | owner | returns an item to draft, in one transaction |
| `/api/models` | read | anyone | the model catalog with full specs |
| `/api/studio/models/{id}` | write | owner | edits a model record |
| `/media/{key}` | read | depends on the object | streams a public object, refuses a private one |

Responses carry the right status: a created record answers created, a refused write
from an unentitled session answers forbidden with the required permission named, an
unauthenticated write answers unauthorized, a malformed body answers unprocessable
with the offending field named, and an unpublished item answers not-found to anyone
not entitled to it. An error body carries a stable correlation identifier and no stack
trace, no internal identifier and no hint that a hidden record exists.

### Validation

Validation lives on the server and is the authority. The browser may check the same
things first for courtesy, but a request that bypasses the browser entirely is subject
to exactly the same rules, and an endpoint that trusts a client-side check is a
contract violation.

The sign-up form requires an address shaped like an address and unique across accounts,
and a password meeting a stated minimum length; a duplicate address is refused in a way
that does not reveal whether the existing account belongs to somebody, and the refusal
names the field. An item requires a title, a slug unique across items, a dek and a body.
A slug is lowercase words separated by hyphens. Alternative text is required on a poster
before the item that owns it can be published, and the refusal names that field. A model
record requires its name, tagline, resolution, aspect ratio list, input list, maximum
duration and price, because a catalog with a hole in one row is not comparable.

An upload is refused unless its declared type is one of the accepted image types and its
size is within the stated ceiling, and the refusal says which limit was exceeded. The
declared type is not trusted on its own: the stored object's type is decided from the
bytes.

### Publication as one act

Publishing changes the item's status and its poster's visibility together. If either
half fails, neither half happened, and the item is still exactly what it was. The same
holds in reverse for unpublishing. A reader who fetches the poster the instant before
publication is refused and the instant after is served; there is no window in which one
half is true and the other is not.

### Configuration and secrets

Every address, credential and endpoint arrives from the environment: `DATABASE_URL`,
`STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, the
session signing secret, `APP_PUBLIC_PORT` and `APP_PUBLIC_URL`. **No secret is
present in any file that reaches the browser**, and no secret is baked into an image at
build time. The front end receives only the public base address; anything else it needs
it asks the server for.

A missing required variable stops the process at start with a message naming the
variable, rather than starting and failing on the first request.

### Observability and resilience

Structured logs carry a request identifier, the route, the status and the duration, and
never carry a password, a token, a session identifier or a secret. The readiness endpoint
reports the database and the object store separately, so a degraded dependency is
attributable. A slow or unavailable object store degrades the media region of a page to
a retry control naming what is unavailable, while the rest of the page still works.

### Performance and search

Documents are served compressed. Static output is fingerprinted and served with long-
lived caching, while documents themselves are not cached in a way that serves one
account's page to another. A listing endpoint is paginated rather than returning every
record. Image and video elements below the first viewport load lazily and carry their
intrinsic proportions so nothing on the page jumps as they arrive.

Every route carries a title and a description, a canonical address, and the social
preview tags a link unfurl needs. The sitemap lists every public route and no private
one; a draft's address never appears in it. Structured data describes the organisation
on the home route and the article on a published news route.

### Security floors

Every response carries the same set of security headers: a content security policy, a
referrer policy, a frame policy and a no-sniff declaration. A missing security header is
a defect rather than a hardening nicety. Mutating requests carry a cross-site request forgery defence.
Passwords are stored only as a salted, computationally expensive hash, never
recoverable. Authentication and account-creation endpoints are rate limited per address
and per caller, and the refusal says when to retry rather than staying silent. Every
rendered value that came from an account is escaped where it lands.

### Testability

The running application must be inspectable from outside without any special mode. The
readiness endpoint is the liveness signal. Seeded accounts sign in with the stated
password. Interactive elements carry stable, meaningful accessible names, and the
identifiers a test would attach to are semantic rather than positional, so a test does
not depend on a thing being the third child of something.

## Data model

What the records hold and what must stay true of them. Table names, column names and
types are yours; the properties below are not.

### Conventions

Primary keys are opaque and sortable. Money is an integer in minor units beside a
lowercase currency code, `usd`, never a decimal and never a floating-point number;
a model's price is minor units per second of output. Instants are UTC and assigned by
the database rather than by the application, so two processes agree. Enumerated values
are constrained by the database rather than being free text. A reference between records
declares what happens when its target goes away, and restricts by default. Uploaded
bytes are never held in a database column and never on the application's own disk.

### The records

**`account`** - an email address unique without regard to case, a display name, a role
of `author` or `reader`, a plan, a credit balance in minor units, and a created instant.
Signup is open, so the public form creates these as well as the seed does.

**`session`** - an opaque token, the account it belongs to, an issued instant and an
expiry, and a revoked instant that is empty until signing out fills it. Revocation is
the server's, which is why a copied cookie stops working.

**`content_item`** - a kind of `news` or `model_card`; a slug unique within its kind; a
title; a dek; a body; a status of `draft`, `scheduled`, `published` or `archived`; the
author account that owns it; a published instant that is empty until publication; the
poster media object it displays; and its created and updated instants. **Status is the
axis the whole critical rule turns on**, and it is the only thing that decides whether
an anonymous caller may read the record.

**`media_object`** - the store key, a content type decided from the bytes rather than
from what the uploader declared, a byte length, a checksum of the bytes, alternative
text, a visibility of `private` or `public`, and the content item that owns it.
Visibility follows the owning item's status and is never set on its own.

**`model_spec`** - a name, a tagline, a resolution, an aspect-ratio list, an input list,
a maximum duration in seconds, a price in minor units per second, a provider, and a
documentation destination. One record read by the catalog table, the carousel card, the
router copy and the pricing page, so a change lands everywhere at once.

**`menu_section`** and **`menu_destination`** - the navigation's own records: a section
carries its label and its position, a destination carries its label, its address, its
position within a section, and whether it opens in a new tab. The mega-menu, the footer
sitemap and the not-found shell all read these, which is what makes link integrity a
property rather than a hand-maintained list.

**`signup_lead`** - an email address, the route it came from, the label of the control
that submitted it, a created instant and an idempotency key.

### The object key scheme

`media/{item_id}/{sha256_of_bytes}.{ext}`, for example
`media/42/9f2a1c7d4e8b6a0f3c5d2e1b8a7f6c5d4e3b2a1908f7e6d5c4b3a2918070605d.webp`.

The key is derived rather than chosen: the item that owns the bytes, then the checksum
of the bytes, then the extension matching the sniffed type. The same bytes uploaded to
the same item land at the same key, so re-uploading does not accumulate copies.

### What must stay true

- An item that is `draft`, `scheduled` or `archived` is unreadable to an anonymous
  caller, and its response is the same one a slug that never existed produces.
- The media object owned by an item that is not `published` is unreadable to an
  anonymous caller, by any route and with any key.
- Publishing changes the item's status and its poster's visibility together, and either
  both changes are durable or neither is.
- An uploaded byte exists in the object store and in no other place.
- A published content image carries non-empty alternative text; an item whose poster
  lacks it cannot be published.
- A model's price is an integer in minor units per second, and every model record
  carries every spec field, so a catalog row never has a hole in it.
- An account's email is unique without regard to case.
- Seeding is repeatable: restarting the application does not duplicate a row.
- A signup arriving twice under one idempotency key creates one account.

### Seed data

Three accounts, each with the password `deku-demo-pw-2026`: `author@example.com` and
`author2@example.com` as `author`, `reader@example.com` as `reader`.

Four model specs: `Nova-4.5` at `12` minor units per second, `Chisel-2.0` at `18`,
`Worldscape-1` at `30`, `Perform-2` at `9`, each carrying the full spec row printed in
`## Front-end specification`.

Four news items owned by `author@example.com`: two `published`, one `draft` whose slug is
`the-media-router-preview`, one `archived`. One further draft, `partner-campaign-preview`,
owned by `author2@example.com`, which is what gives cross-author isolation a subject.
Every news item carries one poster media object, and a draft's poster is `private`.

The menu records carry every section and destination printed in
`## Front-end specification`, so the mega-menu, the footer and the sitemap agree.

---

## Constraints

- No generation. No model runs, no frame is produced, no timeline is built, no GPU is
  scheduled. The generation platform is specified as a contract and is not implemented.
- No billing. Plans and prices are displayed; nothing is charged and no payment
  instrument is collected.
- No third-party identity provider. Accounts and sessions belong to this application.
- No email. Signing up does not send a message, and there is no password-reset flow; the
  seeded passwords are the only credentials this environment carries.
- No external network calls at runtime beyond the PostgreSQL database and the object
  store. No analytics vendor, no font service, no image host, no partner logo fetched
  from anywhere.
- No binary asset of any kind ships: no image file, no video file, no font file, no icon
  file. Every one is produced from a recipe.
- No real partner or customer brand is reproduced. Partner names are placeholders and
  partner marks are name-tiles.
- No comment threads, no search across the site, no newsletter, no localisation beyond a
  single language, no native application and no desktop client.
- Responsive web only.

---

## Deployment contract

Non-negotiable. The application is reached through an ordinary browser and over plain
HTTP by a client that has never seen the code, so the following must hold exactly.

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world
  uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix. The developer portal at
  `/api-platform` is a rendered marketing route rather than an API.
- `GET /api/health` returns `200` once the app is ready, naming the database state and the
  object-store state separately.
- The app starts from the environment image with no manual steps, and the healthcheck goes
  green on its own.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`. For this product they are the three seeded accounts with their
  shared password.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened. Start it fully detached, for example
  `setsid nohup <command> > /tmp/app.log 2>&1 < /dev/null &`, then confirm the listening
  process survives with a parent that is not the shell.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable
  from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
  Never substitute a local file, an embedded database, or a private instance of the same
  product: the state that counts is the state at that address.
- The only backing services are the PostgreSQL instance at `DATABASE_URL`, supplied again as
  `DB_URL` with the same value, and the S3-compatible object store at `STORAGE_ENDPOINT` with
  `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. No other backend, no
  identity provider, no email service, no cache, no queue.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Everything internal is a free choice. These request and response shapes are not: they
are the public interface other software depends on. Field names are exact.

| Endpoint | Request body | Success | On success returns |
|---|---|---|---|
| `POST /api/auth/signup` | `{"email": str, "password": str}` | `201` | `{"id": str, "email": str, "role": "author"\|"reader"}` |
| `POST /api/auth/login` | `{"email": str, "password": str}` | `200` | `{"access_token": str, ...}` - the app's own session bearer token |
| `POST /api/auth/logout` | - | `200` or `204` | - |
| `GET /api/me` | - | `200` | `{"id": str, "email": str, "role": "author"\|"reader"}` |
| `GET /api/news` | query: `limit`, `offset` | `200` | a JSON array of published items, newest first |
| `GET /api/news/{slug}` | - | `200` | the published item; `404` when it is not published, whoever asks |
| `GET /api/studio/news` | query: `status` | `200` | a JSON array of the caller's own items; `403` for a `reader` |
| `POST /api/studio/news` | `{"title": str, "dek": str, "body": str, "slug": str}` | `201` | the created item including `id` and `status = "draft"` |
| `PATCH /api/studio/news/{id}` | any subset of the create fields | `200` | the updated item; `403` when the caller is not the owner |
| `POST /api/studio/news/{id}/media` | the file, with `{"alt_text": str}` | `201` | `{"key": str, "visibility": "private"}` |
| `POST /api/studio/news/{id}/publish` | - | `200` | the item with `status = "published"`; `403` when not the owner; `409` when it is already published; `422` when the poster carries no alternative text |
| `POST /api/studio/news/{id}/unpublish` | - | `200` | the item with `status = "draft"` |
| `GET /api/models` | - | `200` | a JSON array of model specs, each carrying every spec field |
| `GET /media/{key}` | - | `200` | the object's bytes with its stored content type; `404` when the object is private to the caller |
| `GET /api/health` | - | `200` | `{"status": "ok", "database": "ok", "storage": "ok"}` |

Rules:

- Every business-rule violation returns a `4xx` naming the reason. Never a `5xx`, never a
  silent `200`.
- Every endpoint under `/api/studio` requires a valid session; an anonymous caller gets
  `401`, and a signed-in caller who lacks the permission gets `403` with the required
  permission named.
- **An unpublished item and a slug that never existed return the identical response to a
  caller not entitled to it** - same status, same body, same headers. So does a private
  object's key.
- Authorization on every item-scoped endpoint is enforced against the caller's session
  and the caller's ownership of the item. A hidden button is not authorization.
- List endpoints return a JSON array at the top level.

---

## Definition of done

The app is deployed and healthy; every feature above works through the browser; the home
page, the developer portal and the agent connector all render their content in the first
document from the server; the code sample copies to the clipboard; the sign-up form
creates an account that can then sign in, landing on a full page that names it; an author
drafts an item with a poster, publishes it in one act, and sees it appear on the public
listing; a draft and its poster are both unreachable to a signed-out caller and to the
other author, and answer exactly as something that never existed; alternative text is
required before publication; uploaded bytes are in the object store at the stated key
scheme and nowhere else; a `reader` session cannot reach any compose endpoint through a
direct API call; every destination in the mega-menu, the footer and the not-found shell
resolves; and no image, video or font file ships with the build.

Test your own work in a browser before you finish.
