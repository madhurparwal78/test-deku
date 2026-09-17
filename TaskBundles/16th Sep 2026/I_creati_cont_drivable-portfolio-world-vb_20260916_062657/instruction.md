# Drivable Portfolio World

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
press once to start, drive a vehicle across a rendered outdoor world to the object
standing for the project `Lantern Run`, press interact, and read that project's panel
without hitting an error page. The hard part is the boundary around unpublished work: a
project the owner is holding as a draft must be unreachable by every route a stranger
has, including its own address and the address its poster bytes live at, and the poster
bytes themselves must really be in the object store rather than on the app's own disk,
because a picture the app serves from its own filesystem is not a stored object.

## Overview

This is one person's portfolio, published as a place instead of as a page. The owner is
`Marek Vance`, a creative developer, and the world is called `Marek`. A visitor arrives
at a dark patterned void with a glowing ring in the middle, the ring closes as the world
arrives, the ring resolves into a small lit island carrying a truck, and the words
`CLICK TO START` appear beside it. From the first press onward the visitor is driving.

Everything the owner wants to say is a physical object planted in the terrain. The
introduction is a sign. Each published project is an object carrying its title rendered
into the world, its poster, its facts and its awards. The career history is a board. The
outbound links are a place you drive to. There is no navigation bar anywhere on the
public surface: the only permanent controls are two small tabs at the right edge of the
window, and everything else is an overlay the visitor summons and dismisses without the
world ever stopping.

Behind a private studio the owner writes each project entry, uploads its poster image,
pins it to fixed world coordinates, assigns it to one of the world's zones, orders it by
naming the projects either side of it, and either publishes it into the world or holds
it as a draft. Two published projects may never occupy one set of coordinates, because
two objects overlapping in one world is a collision the scene cannot resolve and the
vehicle cannot drive through.

It is deliberately not a social product. There are no visitor accounts and no signup:
the only account in the whole product is the owner's. There are no comments, no likes,
no following and no messaging between visitors. There is no email, no payment and no
subscription. The genuinely hard part is that a draft must be unreachable four ways at
once, and that the refusal to place two published projects at one point is enforced
where the write happens rather than by hiding a control.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Open the world without signing in, drive, interact with any published object, open the menu, the map, the achievements, the circuit and the whisper composer, read the text route, run a timed lap, submit a lap, leave one whisper | **Cannot see, list, open or fetch anything belonging to an unpublished project, by any address.** **Cannot create, edit, publish or unpublish anything.** **Cannot read the page-view record.** **Cannot sign up: there is no visitor account to create.** |
| `owner` | Everything a visitor can do, plus sign in, write and edit projects, upload and remove posters, set world coordinates, zone and adjacency, publish and unpublish, edit areas, achievements, the introduction and the colophon, and read the page-view record | **Cannot place a second published project at coordinates a published project already holds.** **Cannot publish a project that has no poster image.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in
the UI is not authorization: a direct API call from a `visitor` session to any
`owner`-only endpoint must be rejected by the server (an unauthorized request is denied,
not served), leaving the protected state unchanged.

Signup is closed. There is exactly one account and it is seeded: `owner@example.com`
with the password `deku-demo-pw-2026`. A visitor is anonymous and is identified only by
an identifier the browser generates on first visit and keeps locally.

## Core features

### Auth

The owner signs in with email and password. `POST /api/auth/login` takes
`{ "email", "password" }` and returns the bearer token in a field named `access_token`,
which the client then sends as an `Authorization: Bearer` header on every owner request.
Passwords are stored hashed, never in plain text. There is no signup form and no public
route that creates an account. There is no password reset.

1. Signing in with `owner@example.com` and `deku-demo-pw-2026` succeeds and returns an
   `access_token`. Signing in with the right email and any other password is rejected as
   invalid, returns no token, and says the credentials did not match without saying
   which half was wrong.
2. An owner request carrying no token, an expired token or a malformed token is denied
   and the state it aimed at is unchanged.

### The private studio and the publish boundary

The owner writes a project entry, uploads its poster, pins it to fixed world
coordinates, assigns it to one of the authored zone names and names the projects either
side of it. A new project is a draft until it is published.

3. **A draft is unreachable, entirely.** It is not an object in the world and is absent
   from `GET /api/world`. It is absent from the text route listing. Its own address
   `/content/projects/{slug}` and `GET /api/projects/{slug}` answer as if it does not
   exist. Its poster bytes are not readable by a request that carries no owner token.
   All four hold for a request that guesses the slug exactly.
4. **Publishing is refused while another published project already occupies the same
   coordinates.** `POST /api/studio/projects/{id}/publish` for a project whose
   `world_x`, `world_y` and `world_z` match those of an already published project is
   rejected as a conflict with the error code `coordinates_occupied` and the message
   `Another published project already stands at those coordinates.`, naming the slug of
   the project already there.
5. The refused project stays a draft, its `published_at` stays empty, and the project
   already in place is untouched. Two publish requests arriving at the same moment for
   two different drafts at one set of coordinates do not both succeed: exactly one is
   published and the other is refused as a conflict.
6. The refusal is enforced where the write happens. Removing the control from the
   studio, disabling it, or filtering the list the owner chooses from does not satisfy
   this rule: a direct call to the publish endpoint must be refused the same way.
7. Unpublishing frees the coordinates. After `POST /api/studio/projects/{id}/unpublish`
   the project disappears from the world and from the text route, and a different draft
   at those coordinates can then be published.
8. Publishing a project that has no poster image is rejected as invalid with the error
   code `poster_required`, and the project stays a draft.

### Poster images

9. Poster bytes live in the object store and nowhere else. There are no image bytes on
   the app container's filesystem and no image bytes in a database column. The object
   key follows a fixed scheme, `projects/{project_id}/posters/{sha256_of_bytes}.{ext}`,
   for example
   `projects/2/posters/9f2a7c41d0b35e8a6f14c29b7d0e5a38c1b94f27e6a0d3f85b2c7194ae63d08f.png`.
10. The bucket is never handed out directly. Every poster is read through
    `GET /api/projects/{project_id}/images/{image_id}`, which streams the bytes from the
    store. That endpoint serves a published project's poster to anyone and serves an
    unpublished project's poster only to a request carrying the owner's bearer token;
    without one it is denied.
11. Uploading the same file twice for one project produces one stored object and one
    row, because the key is derived from the bytes. Every poster carries alternative
    text the owner writes, and that text travels with the image wherever it is shown.

### Projects in the world

12. A published project stands in the terrain at its stored coordinates and carries its
    title rendered into the world rather than floated over it in the interface layer,
    its poster on an in-world surface, its short factual attributes, its distinctions,
    and an outbound link.
13. Project order is the owner's, taken from the adjacency relation: each project names
    the project before it and the project after it. Order is never derived from a date
    field, and the position of a project within the set is computed by walking that
    relation rather than stored.
14. `GET /api/world` returns every published project with its coordinates, its zone and
    its poster address, and every area. It returns nothing belonging to a draft.

### The text route

15. `/content` carries the substantive portfolio without driving: the introduction, the
    list of published projects with their outbound links, the career history and the
    contact routes, which are a public community invite and a direct-message destination.
    Each published project has its own page at
    `/content/projects/{slug}`. The route states plainly that it is a text alternative
    and not an equivalent experience of the world.
16. The text route lists published projects only, in the adjacency order, and every
    internal link on it and on every other public surface resolves rather than answering
    not-found.

### The world

17. The whole public world is served from one address, `/`. Opening the menu, the map,
    the whisper composer or an object's panel does not change the address, adds no
    history entry, and the browser's back control does not close any of them. Each
    overlay carries its own close control, and one consistent key closes whichever
    overlay is open.
18. Before the first press the root element carries `input-filter-intro` and does not
    carry `is-started`, and both edge triggers are off screen. After the first press the
    root element carries `is-started`, the two edge triggers are present, and the vehicle
    is drivable.
19. Exactly one consumer owns the keyboard at any moment, and the root element names
    which one. While the whisper composer has the keyboard, typing a letter that is also
    a driving key moves the caret and does not move the vehicle.
20. The vehicle is driven by keyboard, by touch and by gamepad, against the same
    simulation. It can be driven, boosted, braked, jumped and rolled onto its roof, and it
    recovers without losing progress. The active input family is reflected on the root
    element.
21. Two recoveries exist and both keep the visitor's progress. `I'm stuck!` with its
    `Respawn` control returns the vehicle to the nearest authored respawn point. `Reset`
    returns it to the world origin. Neither reloads the world and neither clears
    achievements.
22. The quality control cycles between at least two tiers, reading `High` at the top
    tier. Switching tiers does not reload the world and does not lose the vehicle's
    position. The renderer row reads `WebGL` when the preferred backend is available and
    is preceded by the words `not compatible` when it is not.

### Areas, zones and interactive points

23. The world is divided into named areas. Seven are the portfolio itself: `landing`,
    `projects`, `career`, `social`, `achievements`, `circuit` and `behind the scene`. At
    least three play areas ship alongside them, drawn from `altar`, `bowling`, `cookie`,
    `lab`, `time machine` and `toilet`.
24. Each area carries a position, a kind of `content`, `progress` or `play`, a display
    name and at most one interactive point. Driving within range of an interactive point
    raises the interact affordance; pressing interact opens that point's panel in place,
    and driving away closes it. An interactive point is recognisable in the world itself,
    and the on-screen prompt confirms it rather than being the only cue.
25. A zone is entered and left independently of being close enough to interact. Entering
    a zone is what updates the map's current-location readout and what advances the
    achievements that count places found.

### Achievements

26. Achievements are per visitor, survive a reload and are tied to no account. They are
    held in the visitor's own browser under the keys `uuid`, `achievements` and
    `achievementsTimeStart`. A missing key is a valid first visit and never an error.
27. Two progress modes exist and both work: a `count` mode that counts how many times
    something was done against a target, and a `set` mode that tracks which distinct
    members of a named group have been found. A single integer cannot express the second
    and must not be used for it.
28. Only groups with progress above zero are written, so a visitor who has done nothing
    stores nothing. Resetting achievements clears them and starts a new run.
29. A locked reward is shown rather than hidden. Completing an achievement changes its
    title, its progress figure and its bar together and reveals its check glyph. The
    completion time is not shown at all until every achievement is unlocked.

### The map

30. The map is a top-down view of the same world rendered at the moment it is asked for,
    never an authored picture. It fades in rather than appearing, because it may not be
    ready when the panel opens.
31. The map marks the visitor's current position and marks each area at its coordinates.
    A location's name is revealed on hover with a pointer and stands permanently on a
    touch device, because there is nothing to hover with. Every location name is authored
    with a line break already in it, and that break takes effect only on a narrow window.

### The circuit

32. A timed lap runs a marked course in the world. While a lap is in progress three
    controls appear, `Restart`, `End` and `Controls`, and `Controls` opens the controls
    content without ending the lap.
33. Every finisher sees their time, shown large and heavy, whether or not it placed. A
    lap that does not place shows the line `Sorry, you didn't make it to the top 10.` and
    still shows the time. A lap that places shows the submission form instead.
34. A submitted lap carries the visitor identifier, a short tag, a country code, the
    duration in whole milliseconds and the per-checkpoint split times. A lap whose splits
    do not sum to its stated duration is rejected as invalid and is not recorded.
35. The board holds the fastest lap per visitor for the current UTC day and states when
    it clears. With no laps recorded today it reads `No score yet today`.

### Whispers

36. A whisper is a message of at most 30 characters left by a visitor, standing in the
    world at the position the vehicle was in when it was written, not listed in a feed
    with a location attached. Placement is the point: it is an object planted at a point,
    and the three world coordinates travel with the message when it is written.
37. The composer prints its six rules before the visitor types, exactly:
    `Everyone can see them`, `New whispers remove old ones (max 30)`,
    `One whisper per user`, `Choose a flag`, `No slur!`, `Max 30 characters`.
38. All six are enforced where the write happens, not merely stated. The wall holds at
    most 30 whispers; the thirty-first evicts the oldest, and that eviction is one
    decision the server makes and every visitor sees, never a trim each browser performs
    for itself. A second whisper from the same visitor identifier replaces that
    visitor's existing whisper rather than adding one. A whisper with no country code, an
    empty message or a message over the limit is rejected as invalid and nothing is
    written.
39. The composer refuses a bot. It carries an unlabelled field no person is shown; a
    submission that fills it is refused and writes nothing. A submission that arrives
    repeatedly from the same visitor identifier within a short window is refused the same
    way, and the refusal says the message was not accepted without saying which check
    caught it.

### Shared world state, page views and the cookie choice

40. Two shared values exist alongside the whispers and the board: a shared tally the
    world keeps, and a shared world event every visitor sees in the same state. The tally
    carries an accumulated `amount` rather than incrementing by one, because a rapid
    action is throttled in the page and sent as a total.
41. The world is fully explorable while the shared endpoints are unreachable. In that
    state the root element carries `is-server-offline`, the circuit block and the result
    show `Server currently offline. Scores can't be saved.`, the composer shows
    `Server currently offline`, and no feature is hidden. A lap still runs, still times
    and still shows its result. A write attempted while unreachable does nothing, is not
    queued and is not replayed after the connection returns.
42. When the shared endpoints become reachable the root element carries
    `is-server-online` and a `Server connected` notice appears, except within the first
    ten seconds of a visit, when it is suppressed because nothing was restored. A
    `Server disconnected` notice appears when they become unreachable again.
43. Every public page view is recorded with its route and the moment it happened, and the
    owner can read that page view record at `/studio/page-views`. A visitor cannot read
    it.
44. A first-time visitor is asked once whether non-essential measurement is allowed. The
    answer is stored under `cookie-choice` as `accepted` or `declined`, survives a reload,
    and is not asked again. Nothing that measures a visitor runs before the answer is
    `accepted`, and no product behaviour depends on measurement being allowed.
## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the world, and every overlay summoned from inside it | none |
| `/content` | the text route: introduction, published projects, career, contact | none |
| `/content/projects/{slug}` | one published project as text | none |
| `/studio/login` | owner sign-in | none |
| `/studio` | the owner's project list | owner |
| `/studio/projects/new` | write a new project | owner |
| `/studio/projects/{id}` | edit a project, publish or unpublish it | owner |
| `/studio/projects/{id}/published` | the confirmation a publish lands on | owner |
| `/studio/world` | areas, zones and coordinates | owner |
| `/studio/achievements` | achievements and their progress modes | owner |
| `/studio/pages` | the introduction and the colophon | owner |
| `/studio/page-views` | the page view record | owner |

**Entry and redirects.** A visitor who opens `/` lands in the world with no sign-in
prompt anywhere. A request for any `/studio` route without a valid session goes to
`/studio/login` and, after a successful sign-in, continues to the route that was asked
for. Signing out returns to `/`. A token that expires mid-edit returns the owner to
`/studio/login` and the edit is not written. A visitor who reaches a `/studio` route by
typing it is sent to `/studio/login` and, having no account, gets no further. An unknown
address renders the product's own not-found page with a way back into the world.

**Journeys.**

1. A visitor opens `/`, watches the ring close into the island, presses once, drives
   toward the object for `Lantern Run`, sees the interact affordance rise, presses
   interact, and reads the project's title, poster, attributes and distinctions in the
   panel that opens in place. Driving away closes it.
2. A visitor presses the upper right-edge trigger, the menu opens over the still-running
   world, they move to the achievements content, watch the text change a beat before the
   picture does, and close the menu from its own close control.
3. A visitor presses the lower right-edge trigger, the map fades in, their marker
   double-pulses, they point at a location and its name springs up, and they close it.
4. The owner opens `/studio/login`, signs in as `owner@example.com` with
   `deku-demo-pw-2026`, lands on the project list, and opens the create panel, which
   slides in over the list from the right while the list stays visible behind it.
5. In that panel the owner types the title `Harbour Light`, uploads a poster, sets the
   coordinates, picks the zone `projects`, names the neighbours, and saves. The project
   appears in the list marked as a draft and appears nowhere in the world.
6. The owner sets `Harbour Light` to the coordinates `Paper Tide` already holds and
   presses publish. The publish is refused, the reason names `paper-tide` as the project
   already standing there, `Harbour Light` is still a draft, and `Paper Tide` is
   unchanged.
7. The owner changes `Harbour Light` to a free point and publishes again. The browser
   lands on a full confirmation page naming the project and its coordinates, with a link
   into the world and a link back to the list. `Harbour Light` is now an object in the
   world and a row in the text route.
8. A visitor opens the whisper composer, types a message, picks a flag, watches the
   submit control light up, and sends. The whisper stands where their vehicle was.
9. A visitor runs the circuit, crosses the line, and sees their time whether or not it
   placed.

**States.** Every list has an empty state that says what would be there: the project
list before anything is written, the board before any lap today, the wall before any
whisper, the page view record before any view. Every overlay has a loading state and
opens at once even while the world is still resolving. A failed request never blanks the
page: the world keeps rendering behind the overlay and the overlay states what failed
and offers the action again.

## UI/UX notes

The north star: somebody arriving should understand within one press that this is not a
page about a person's work but a place holding it, and should feel invited to break
something. The register is expressive and playful, and the subject is seen first: the
world is the content, and the interface is a hairline drawing laid over a rendered scene
rather than a stack of filled cards competing with it. Atmosphere over chrome, and the
world over the panel.

One design system covers the whole interface, and one colour scheme, and it is a night
scene: there is no light theme, and that is a
decision rather than an omission. The page and every panel sit on a deep, cool neutral
violet lit from one corner as though a lamp sat just off it, and every control is lit
from its own opposite corner so that a row of them never reads as one flat strip. The one
gradient that is not that violet is the alert surface behind a destructive or
attention-carrying control, which runs from a mid, vivid red into a deep, muted magenta
and appears on nothing else. Ink is
a near-white neutral and carries all body copy, all icon fills and every hairline. One
accent, a near-white muted red, carries panel headings, the achievement bar and the valid
state of an input, and appears roughly once for every fourteen appearances of ink: if the
accent reads as a background anywhere, it is being overused. Three colours mean something
and are used for nothing else: a light soft lime for something achieved or restored, a
light vivid red for something destructive or lost, and a light soft orange for the track
now playing. A state that is none of the three may not borrow any of them, and no state
is signalled by colour alone.

The signature decision is the hairline. A surface takes no border; it takes a child set a
hair inside its edge carrying one fine white line held faint, and that line roughly
doubles in strength when pointed at. It is the primary hover signal in the whole
interface, and the same brightening is what shows where the keyboard is. The missing edge
of a hairline is always the edge its control slides toward.

Type is exact where type is an identity. `Nunito` carries everything that is read and
`Amatic SC` carries every panel title and the large touch verbs, with the fallback stacks
`Nunito, sans-serif` and `Amatic SC, sans-serif`. Everything expressed against the root
size steps as a set when the root steps, so a heading and its body hold the same
relationship at every width, and figures line up in a column wherever times or counts
stack. Scaling is a property of the root and not of individual rules: a build that fixes
any one step of the scale will be right at exactly one window size.

Motion has two speeds and no third: one for answering a pointer, one for a panel arriving
or leaving. Reaching for a speed between them breaks the only rhythm the interface has.
Nothing moves in a straight line: every transition either overshoots its resting place
and settles back or winds backward before it goes, and the two directions of one movement
never share a curve. Under a reduced motion preference the interface stops springing and
simply changes state while the world keeps rendering, because that preference is a
request about interface animation and not a request to switch off a product whose content
is a moving place.

Each surface leads with one primary action, visually distinct from every secondary one,
and on the opening screen that action is the single instruction to press. Controls carry
resting, pointed-at, pressed, focused and unavailable states, and unavailable is drawn as
a dashed edge rather than a dimming, because dimming a hairline on a dark ground makes it
vanish. The accessibility floors are contract and do not bend to the mood: body text meets
WCAG AA contrast against its ground, touch targets are comfortably
sized, keyboard navigation reaches every overlay with a visible focus ring, focus stays
inside an open overlay and returns to the control that opened it, and every icon-only
control is named for its action rather than for its picture.

The world layer fills whatever viewport it is given and no responsive rule touches it,
while the interface layer steps down twice as the window narrows. Orientation is a
first-class axis rather than a width: the menu reorients by
the shape of its frame rather than by a pixel count, so a landscape phone gets the
side-by-side arrangement a portrait one does not, and touch is decided by the device
having a touchscreen rather than by how wide it is. Density is comfortable in the panels
and spacious in the world. The studio carries a top navigation; the public world carries
none at all. Exact shades, spacing, radii and timings are yours, so long as they hold the
rules above.

The failure to avoid: a page dominated by one hue with no second signal, decoration
standing in for content, a marketing composition where a working interface belongs, or an
interface so heavy that it reads as the product with the world as its wallpaper.
## Technical requirements

The stack is FastAPI with Jinja templates on the server and HTMX over server-rendered
templates in the browser, with progressive enhancement. The server produces the HTML for
every address, so the browser receives a rendered document on first paint rather than an
empty shell it has to fill; the world address serves one such document whose scene is
then drawn continuously in a canvas surface inside it, and every studio surface works
from a plain form post before any enhancement runs. PostgreSQL is the datastore, reached
at `DATABASE_URL`. MinIO is the object store, reached at `STORAGE_ENDPOINT` with
`STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`. Auth is app-implemented
email and password with bearer tokens. `GET /api/health` returns `200` once the app is
ready. Request logging goes to stdout.

Use only the libraries named here plus their direct dependencies. Do not introduce a
second database, cache, queue, object store, identity provider or mail vendor: the only
backing services available in this environment are PostgreSQL and MinIO, and reaching
for anything else is a contract violation.

The backing services are already running at those environment variables and must not be
downloaded, installed, compiled or started. Never hardcode a host or a port; read
`APP_PUBLIC_URL` and `APP_PUBLIC_PORT` from the environment as well.

**The root element carries the product's state, and the exact class names are a
contract.** Six independent families live there. Lifecycle: `is-started`, present once
the visitor has pressed to start. Connection: `is-server-offline` and `is-server-online`,
mutually exclusive. Input mode: `is-mode-mouse-keyboard`, `is-mode-touch` and
`is-mode-gamepad`. Gamepad family: `is-gamepad-default`, `is-gamepad-playstation` and
`is-gamepad-xbox`. Input filter: `input-filter-intro`, `input-filter-wandering`,
`input-filter-menu`, `input-filter-modal` and `input-filter-cinematic`, exactly one of
which is present at any moment and which names the single consumer that owns the
keyboard. Audio: `is-audio-muted`. Every appearance is two phase: an element takes
`is-displayed` first and `is-visible` on the following frame, and closing removes
`is-visible` first and `is-displayed` after the fade, so nothing appears without it.

Behaviour hooks are separate from styling names. The names code holds on to are prefixed
`js-` and the names the stylesheet targets are not, and neither depends on the other:
`js-close`, `js-content`, `js-tabs-navigation-item`, `js-flag-select`,
`js-global-progress`, `js-button-reset`, `js-respawn` and `js-audio-toggle`. Tab identity
rides on `data-tabs-name`, and the tab that opens by default is the one carrying
`data-tabs-default`.

**Rendering capability.** The world layer must render a continuous outdoor scene at
interactive frame rates in a surface that never scrolls and consumes pointer and touch
events itself, simulate a driven four-wheeled vehicle with suspension against static
collision geometry so that it can climb, jump, tip over and be recovered, accept keyboard
touch and gamepad against that same vehicle, detect the vehicle entering and leaving
named regions and raise an event when it does, render text into the scene at runtime so
that titles and results are part of the world, degrade to a lower cost path on a device
that cannot sustain the full one and expose that choice as a setting, and fall back
rather than fail when the preferred rendering backend is absent, reporting the outcome to
the visitor in plain words.

Collision geometry is simplified geometry authored separately from the geometry that is
drawn, never the drawn geometry reused. Repeated objects are instanced from named
anchors rather than stored one per instance, and a named anchor is also what a positional
sound is pinned to. Sounds that belong to a place are positional with an explicit fade
distance, so a visitor hears a thing before they see it.

**Performance behaviour.** Something is on screen immediately, and the first frame is a
rendered frame rather than a spinner on a blank ground. Loading progress is honest: the
ring closes with real progress and does not complete and then wait. The interface layer
never waits on the world, so the menu, the map and the composer open at once while the
world is still resolving. The world degrades before it stutters: frame rate is the fixed
quantity and fidelity is the variable one. Sound is deferred until the first press. The
shared endpoints are never on the critical path: the product starts in the offline state
before it has tried to reach them, retries for as long as they are unreachable, and
nothing in the first paint depends on them.

Every animated property is a transform or an opacity rather than a layout property, and
the compositor hint that promises an element is about to move appears exactly once, on
the one element that moves continuously while the world is also rendering. Nothing in the
build declares a blanket transition on all properties.

**Module and component architecture.** Four boundaries are requirements rather than
taste, because within one frame a simulation step, a render step, an interface transition
and an arriving shared value all have to agree about the same state. Every unit reaches
its collaborators through one composition root, reached the same way from everywhere.
Materials, geometries, textures, objects and references are shared registries rather than
per-area state: an area asks for a material by name and never constructs one. A generic
event bus carries what the clock, the shared endpoints and the achievement ledger publish,
which is what keeps the achievement ledger from needing to know what a simulation tick is.
And exactly one unit owns closing whatever is open, so that the question of what the close
key does right now has one answer; that unit is also where the input-filter transitions
live. The platform layer that sits under all of this carries the shared-state client, the
quality setting, performance measurement, a profiler, a debug flag, a console, an info
readout and the event emitter, and the profiler and debug surfaces never render for a
visitor.

**The information architecture is one address for the public product.** Opening a surface
is a state of that address and not a new one, so there is no fragment routing and no
history entry, and the only addresses beyond it are the text route and the studio.
`GET /api/world` is the full state snapshot the page retains on load, and every later
response is an incremental update applied to what the page already holds rather than a
replacement of it. Shared values appear without reloading the page. The canonical address
of the public product is declared in the document head alongside its title, its
description, its social title, its social description and its social card type.

**Persistence.** Server-side persistence is PostgreSQL and the object store, and nothing
else. Local persistence is the visitor's own browser and is never synchronised anywhere:
three keys only, holding the visitor identifier, the achievement progress and the moment
the run began. Analytics is optional, loads after first paint, runs only once the cookie
choice is `accepted`, and no product behaviour depends on it.

## Data model

Eleven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must
be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**owner_account** - id, email (unique), password_hash, created_at. Exactly one row.

**project** - id, slug (unique), title, summary, link, world_x, world_y, world_z, zone,
previous_slug, next_slug, published (boolean, default false), published_at (empty until
published), created_at, updated_at. `zone` holds one of the authored area keys. The
project's position within the ordered set is derived by walking the adjacency relation
and is never stored. Invariant, and it must hold under simultaneous requests: at most one
project with `published` true exists for any one combination of `world_x`, `world_y` and
`world_z`. Two publish requests arriving together for two drafts at one point do not both
succeed; exactly one is published and the other is refused as a conflict, and no partial
state is left behind. A project may not name itself as its own previous or next.

**project_attribute** - id, project_id, label, value, position.

**project_distinction** - id, project_id, kind, name, year.

**project_image** - id, project_id, object_key (unique), byte_sha256, content_type,
alt_text, position. The bytes live only in the object store; this row holds the key.

**area** - id, key (unique), kind (`content`, `progress` or `play`), display_name
carrying its authored line break, world_x, world_y, world_z, interactive (boolean).

**achievement** - id, key (unique), title, description, mode (`count` or `set`), target
(used by `count`), members (a list, used by `set`), reward_key.

**whisper** - id, visitor_uuid, message, country_code, world_x, world_y, world_z,
created_at. At most 30 rows exist; inserting the thirty-first removes the oldest in the
same operation, and at most one row exists per `visitor_uuid`.

**lap** - id, visitor_uuid, tag, country_code, duration_ms (whole milliseconds),
checkpoint_splits (a list), created_at.

**page_view** - id, route, viewed_at.

**site_page** - id, key (`introduction` or `colophon`), body, updated_at.

Those eleven names are the table names: `owner_account`, `project`,
`project_attribute`, `project_distinction`, `project_image`, `area`, `achievement`,
`whisper`, `lap`, `page_view`, `site_page`. Each carries an integer `id` primary key.

### Seed data

- One account: `owner@example.com`, password `deku-demo-pw-2026`, owner of everything.
- Four projects. `Lantern Run` (`lantern-run`), `Paper Tide` (`paper-tide`) and
  `Copper Garden` (`copper-garden`) are published at three distinct sets of coordinates
  and each carries one poster in the object store. `Night Ferry` (`night-ferry`) is a
  draft, carries one poster, and holds the same coordinates as `Paper Tide`, so
  publishing it is refused until its coordinates change. Adjacency runs
  `lantern-run` to `paper-tide` to `copper-garden`.
- Ten areas: the seven content and progress areas `landing`, `projects`, `career`,
  `social`, `achievements`, `circuit` and `behind the scene`, plus the three play areas
  `altar`, `bowling` and `lab`.
- Six achievements, at least one in each mode: `set` mode over the named areas, `count`
  mode over repeated actions.
- One introduction and one colophon, with the colophon headed `Behind the scene`.
- No whispers, no laps and no page views. The empty states are what a first visit sees.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Front-end specification

Every value below is a description, not a measurement. Choose the exact shades, spacings,
radii and durations yourself; what is written here is what must be true of them.

**The type scale, carried exactly.** `Nunito` at 400, 700 and 900, and `Amatic SC` at
700. A panel title is `2.5rem`, a colophon heading `2rem`, a section heading `1.7rem`,
body copy `1rem` and fine print `.8rem`, all expressed against a root size that steps
down twice as the window narrows. Fixed against that stepping: a tab caption at `13px`, a
tooltip and a notification body at `16px`, a name tag at `25px`, a finished lap time at
`30px`, and a touch verb at `64px` dropping to `48px` on a narrow window. A build that
hard-codes one column of that scale will be correct at exactly one window size.

**The named motion moments.** Build these and no others: the notification that drops in
from above its slot with an overshoot and leaves by dipping and collapsing to nothing, on
two different curves; the map label that springs up past full size when pointed at and
crushes below nothing on the way out, again on two different curves; the map marker that
double-pulses shortly after the map opens, so the eye finds it before it starts reading
names; the menu whose words change a beat before its picture does; and the edge trigger
that leaves at once and returns late. Every appearance uses the two-phase
display-then-visible sequence, so nothing arrives without its fade, and the easing of a
movement leaving is never the easing of the same movement arriving.

**Two layers.** The world layer is full bleed and fixed and never scrolls; the interface
layer is fixed above it. Nothing scrolls the document itself, and the only scrolling
regions are inside panels. The world surface consumes touch gestures itself, so a finger
drag aims the camera and never pans a page.

**The opening.** Before anything has loaded the window is already showing the world: a
very dark violet ground receding to a horizon above the top edge, patterned with a
regular grid of small cross glyphs in a lighter violet whose spacing shrinks with
distance, and two faint pale hairlines ruled diagonally across it. A glowing blue-white
ellipse sits at the centre and is the only bright thing. That ellipse is the loading
progress and the only loading progress: an arc that closes into a complete ellipse, with
no percentage, no bar and no word anywhere, because the ellipse is the footprint of the
island about to appear inside it and what the visitor is watching is ground being drawn.

The ring then fills with a small circular island floating in the void: a pale paved disc
with a bright rim of light continuous with the ring, a boxy four-wheeled truck with a
deep red body and glowing amber lamps front and rear sitting on the disc facing a fence,
a slim pale lamp post with a warm amber lantern head at the left, a plank fence panel
behind the truck in the same pale material as the disc, three dense-canopied trees
overhanging from behind, a clump of tall grass at the foot of the lamp and one small
rounded rock. The island is lit by a key light that cycles in temperature, warm red
orange one moment and cool blue violet the next, and the ground pattern shifts colour
with it. It holds indefinitely and is not a fixed hero image.

Beside the island, ranged left in the display face, the words `CLICK TO START` sit on two
lines with a hand-drawn curved arrow below the first line hooking left and down toward
the island, and a small speaker outline with two arcs centred under the second line. The
speaker is not a control: it is notice that pressing will produce sound, and the mute
control lives in the options content. On the narrowest window the island stays centred
and the call to action is allowed to run off the edge, because the island is the subject.
The scene can be orbited with a drag before the first press, and the world surface takes
a grab cursor while it does.

**The two edge triggers.** Two identical square controls stacked at the right edge, the
upper opening the menu and the lower opening the map, both absent until the visitor has
started. Each carries the alert gradient and a hairline missing its right edge, because
the right edge is where it slides. Pointed at, the control nudges left by a hair; it is
built wider than its slot by exactly that amount and anchored so nothing gaps open behind
it. When an overlay takes the keyboard, both slide fully off the right edge rather than
dimming. Leaving is immediate and returning waits a beat, so an overlay opening reads as
having pushed the tab off the edge and the tab returning reads as having taken a moment
to notice.

**The menu.** A rectangle centred in the window, split into a preview pane and a content
pane of equal width side by side, stacking into a shallow preview above a taller content
in portrait. Six contents live behind that one shell, named `home`, `options`,
`controls`, `achievements`, `circuit` and `behindTheScene`, and switching between them
never remounts the shell: the shell fades once when the menu opens and the contents cross
fade inside it. The sequencing is that the words lead and the picture follows, so the
outgoing content fades at once, the incoming content waits a moment, and the preview
waits longer still before it changes at all. A scrolling content is made wider than its
clipping frame by about a scrollbar so the scrollbar sits outside the visible area and
the text does not reflow when a scrolling content replaces one that does not scroll.

The tab strip sits above the shell rather than inside it, like tabs on a folder, with a
close control at the other end carrying the alert gradient. A tab is built taller than its
slot and nudges upward when pointed at; the active tab drops its gradient for a flat fill,
which reads as having been pressed into the panel. On the narrowest window there is no
room for both the strip and the close control, so the close control turns a quarter turn
and moves to the right edge to join the two triggers already there.

The `options` content carries six rows: `Audio` as a toggle whose glyph swaps with the
muted state, `Quality` as a cycling control reading `High`, `I'm stuck!` with a `Respawn`
control, `Reset` with a `Reset` control, `Renderer` as a read-only status reading `WebGL`,
and `Server` as a read-only status reading `Offline`. Two of the six are read-only status
on purpose: the panel that holds the settings is also the panel that answers why
something is not working, and both answers are one word. The `controls` content is three
tabs labelled `Mouse Keyboard`, `Mobile Tablet` and `Gamepad`. The keyboard table reads
`WASD` or `ARROWS` for Move around, `SHIFT` for Boost, `CTRL LEFT` or `B` for Brake,
`SPACE` for Jump, `ENTER` for Interact, `M` for Map, `L` for Mute, `T` for Post a
whisper, `R` for Respawn, `NUM KEYS` or `NUM PAD` for Activate hydraulics,
`LEFT CLICK (DRAG)` for Move camera and `H` for Honk. The touch table reads One finger
for Move the car, Two fingers for Move camera and zoom, and Tap on the car for Jump. The
gamepad table reads face buttons for Boost, Jump, Brake and Interact or Exit, `L2` for
Accelerate, `R2` for Backward accelerate, `L1 / R1` for Hydraulics, `Joystick Left` for
Turn wheels, `Joystick Left (press)` for Honk, `Joystick Right` for Move camera,
`Joystick Right (press)` for Zoom in and out, `Select` for Reset and `Start` for Pause.
The controls content is the one surface that answers window height: as the window
shortens its row spacing tightens and then closes entirely, because a control reference
you have to scroll is worthless.

**The notification stack.** Small cards arriving at top centre, each carrying a thin timer
line pinned to its top edge that shrinks away as its time runs out and is drawn in that
card's own colour, so the kind is legible once learned without reading the words. Four
kinds: an achievement, in the success colour, the only one that is interactive and whose
open glyph fades in at its corner faster than anything else in the product because the
pointer is already resting on it; a track starting, in the song colour with the track name
in ink; `Server connected` in the success colour; and `Server disconnected` in the danger
colour. The card drops in from above its slot with an overshoot and leaves by dipping and
collapsing to nothing, on two different curves.

**The touch action bar.** On a touch device only, pinned to the bottom over a soft dark
fade, carrying the useful verbs set large in the display face with generous thumb targets,
and passing pointer events through around the buttons so the world stays drivable. This is
the one place the interface is allowed to be louder than the world, and on a device with
no hover it should be.

**Tooltips** are hover only and pass pointer events through, which makes them decorative
by construction: nothing in the product may exist only in a tooltip, and every tooltip
restates something already available as text.

**Iconography.** Five drawn icons and no icon files: a three-quarter restart ring opening at
the top right closed by a solid triangular arrowhead that overhangs the ring; an outlined
flag on a pole drawn as an outline rather than a fill; an outlined game controller whose
face buttons and directional pad are picked out as small axis-aligned rectangles on a
grid, which is what keeps them crisp at small size; a four-pointed sparkle with a small
plus at its upper right, the only icon drawn in the accent colour and the only one stroked
rather than filled, which is what makes it read as the one control meant to be pressed;
and a speaker outline with two arcs. The menu glyph is not a drawing at all but three
independent bars, kept as three elements so they can move independently. Ring glyphs are
nudged up a hair from their geometric centre, because the optical centre of a ring sits
above the geometric one and a row of controls reads crooked otherwise.

The remaining interface glyphs are drawn the same way rather than fetched: the
control-family glyphs, a pointer glyph pairing key shapes with a small mouse outline, a
touch glyph of a finger outline with a tap arc, the gamepad glyph, the four gamepad face
buttons as a stroked circle, triangle, square and cross, an achievement check as a
two-segment polyline with round line caps, touch action arrows as a single chevron with
the second instance rotated to face the other way, a touch close as two crossed lines, a
touch open and a notification open as a square whose top-right corner is replaced by an
outbound arrow, a music note as a filled ellipse with a stem and a flag, an audio-on
speaker with two arcs and an audio-off speaker with a cross, a map player marker as a
filled circle with a directional wedge that stays legible when the marker halves in size,
and a reward lock as a padlock outline. A country flag is drawn from a small declarative
record of bands with an orientation and a proportion plus an optional canton, and a flag
that cannot be expressed that way falls back to its two-letter code set in the body face
on a neutral field rather than being approximated.

**What stands in the world.** The scene is built from named groups rather than from one
monolithic model, and the groups are the ground itself with its terrain, playground,
floor, grid, water and water surface; planting made of oak trees, birch trees, cherry
trees, bushes, flowers, grass, foliage and leaves; built objects made of fences, bricks,
benches, lanterns, pole lights, explosive crates and general scenery; regions, meaning
the areas and the respawn points; weather and time, meaning a day cycle, a year cycle,
wind and its wind lines, snow, rain lines and lightning; set pieces, meaning a tornado
with its own path, explosions, fireballs, confetti, trails and bubbles; and the vehicle,
meaning a physics vehicle, four wheels and a visual vehicle. A code-sequence listener sits
behind the easter eggs.

Each group ships in up to three parts and the split is required. The visual part is the
geometry that is drawn. The physical part is simplified geometry the simulation collides
against, and the visual geometry is never reused for it. The references part is named
empty transforms marking where instances go and where named anchors are, which is what
lets one heavy tree be drawn once and instanced across the world, collided against a
cylinder, and still carry a named anchor a positional sound is pinned to.

**Procedural recipes, because no binary asset ships.** The terrain is a displaced plane
whose height comes from summed value noise at three octaves, flattened to level ground
inside each area's footprint and skirted downward at its edge so the world reads as an
island rather than as a clipped plane. The playground's visual part is extruded boxes and
cylinders on a grid with their top faces inset to make kerbs, and its physical part is the
same footprints as boxes and cylinders only. A tree is a trunk from a lathe profile with a
slight taper and a canopy of three to five overlapping low-detail spheres displaced per
vertex by hashed noise and flat-shaded, so no two read alike; a cherry differs by canopy
colour and by a lighter, wider silhouette. Bushes, flowers and grass are crossed
camera-facing quads instanced from anchors, with per-instance rotation and scale hashed
from the instance index. Fences, benches, bricks and crates are assembled rounded boxes,
and a fence panel is three horizontal boards and two posts. A lantern or pole light is a
cylinder post, a tapered four-sided head, an emissive quad inside it, and one point light
per instance budgeted by distance. The vehicle is a rounded box body, a smaller rounded
box for the cabin, four cylinders for wheels and two emissive quads front and rear, tall
and boxy with the wheels proud of the body. The tornado path is a curve through authored
control points and its visual is a stack of rotated rings whose radius is a function of
height. A level-of-detail step chooses which version of a group is drawn at distance.

Most surfaces need no texture at all: flat shading and vertex colour carry them. The
ground's receding pattern of cross glyphs is generated in the material from the surface
coordinates, taking the fractional part of the scaled coordinate, drawing two crossing
bars with a smoothed step, and fading with distance so it does not alias at the horizon.
One generated environment lookup is written once into an offscreen surface as a radial
gradient with a brighter upper half, a darker lower half, a soft horizon between them and
one small hot specular highlight up and to the left; on a flat-shaded world that single
lookup decides most of what every surface looks like, so it is worth real effort. A
voronoi noise source is generated once into an offscreen surface by scattering seeded
feature points on a grid and writing the distance to the nearest one, then sampled at two
differently scaled and differently drifting offsets with the minimum of the two taken,
which is what makes flowing water read as two currents rather than as one scrolling
texture.

**Sound is synthesised, positional and deferred.** Every world sound is registered as a
positional source with an explicit fade distance, because sound is how a visitor finds
something they cannot see yet and a non-positional bed cannot do that job. The ambient bed
is two or three detuned oscillators through a low-pass filter whose cutoff is driven by a
slow oscillator well below a hertz, looping indefinitely at a low volume. Positional
chimes are short enveloped sine bursts at a random member of a pentatonic set, triggered
on a slow randomised interval and positioned on the area's anchor. Fire is filtered noise
with a fast attack and a long decay for the ignition and a continuous low-gain
filtered-noise loop for the flicker. The engine is a sawtooth whose frequency tracks wheel
speed through a band-pass filter, with a second detuned copy for body. An impact is a
short noise burst under a tenth of a second with its pitch varied by impact strength. A
reveal is a rising filtered-noise sweep of about a second with its gain enveloped, played
once. Interface cues are short enveloped blips with a stated waveform, frequency sweep and
duration each.

**Generated media.** A project with no poster of its own gets a generated placeholder
seeded from its id: a two-stop gradient between two palette colours, a soft diagonal band,
and the project title set in the display face. Because these are drawn onto surfaces
inside the world they are generated at a power-of-two size and marked for upload once
rather than regenerated per frame. The social share image is generated at build time from
the panel gradient, the brand set in the display face and the hairline motif, rather than
fetched.

**The map.** A square panel showing the world from above, stepping down in size twice as
the window narrows. It fades in rather than appearing. The visitor's position is a marker
that double-pulses shortly after the panel opens so the eye finds it before it starts
reading names. A location is a white diamond with a thick ground-coloured edge and a soft
matching shadow, which is what keeps it separated from light ground and dark ground
alike. Its name sits in a zero-width container above it so the label centres on the pin
whatever its length and never displaces anything; it springs up past full size on one
curve when pointed at and crushes below nothing on another when it leaves. On a touch
device every label stands permanently, so the map is a labelled map on touch and a clean
map that labels on demand with a pointer.

**Achievements.** Three stacked blocks: one line of global progress, a row of small square
rewards, then the list. A locked reward is shown behind a scrim with a lock glyph and is
not clickable, because the whole mechanic depends on seeing what has not been earned. An
achievement carries its title, a description, a progress figure and a bar whose fill is
driven by a horizontal scale from its left edge rather than by width, so the fill can move
while the world is still rendering behind it. On completion the title, the figure and the
bar all move to the success colour together and a check glyph appears. The completion
time appears only when everything is unlocked, reading as a sentence rather than as two
fields, because it is a reward and not a running clock. The reset control is drawn in the
danger colour.

**The circuit.** A leaderboard of three columns: rank, who, and time. The rank column is
deliberately the quietest thing in the table, because it is a scoreboard and not a ladder.
The reset time is stated. With nothing to show it reads `No score yet today`. The result
shows `Your time` above the value, set large and heavy, with `00:00:000` as its empty
form: minutes, seconds and milliseconds to three places, zero padded and colon separated,
because on a short lap the difference between two visitors is in the third place. A lap
that placed reveals the submission group; one that did not shows
`Sorry, you didn't make it to the top 10.` and the time just as large. `Submit` and
`Restart` sit below.

**The whisper composer.** Headed `Leave a whisper`, opening with the line
`Whispers are messages left by visitors.` and then the six rules as a list. The field is
not a form field at all: it is a live preview of the object about to stand in the world,
set at the size and on the ground colour it will have there, which is why it carries no
visible field affordance. Its placeholder reads `Your message here`. Choosing a country
pins a small flag to the card's top corner at a jaunty angle, reading as a pennant rather
than as a form control. The input group is three segments sharing one row: a flag picker,
the text field, and a submit control. The submit control starts visibly inert in the field
line colour and lights up in the accent colour only when the message can actually be sent,
rather than looking alive and then refusing. The flag picker opens upward out of the
field, fused to it by a missing bottom edge and matching upward corners, and carries a
search field, a clear control and a close control, with a stated empty state. A country
whose flag cannot be drawn from bands and a canton falls back to its two-letter code set
in the body face on a neutral field, and that fallback is stated rather than approximated.

**Modals.** A modal may carry a preview above its content, and the preview is lifted so
the content overlaps its lower edge rather than sitting neatly beneath it. The community
modal is headed `Community` and holds two cards side by side, stacking in portrait. Each
card's border is drawn by omission rather than by layering: the heading sits exactly on
the top edge with a short rule running out to either side of it so the outline appears to
pass behind the words, and the card's action sits on the bottom edge filled with the panel
colour so it punches a hole in the line it sits on. The first card reads `Public server` /
`Come hang out with the community, show us your projects and ask us anything.` /
`Join server`; the second reads `Private messages` /
`Contact me directly. I have to warn you, I try to answer everyone, but it might take a
while.` / `Start chatting`. When the window narrows the card does not squash: one clause
of each body line, marked in advance as optional, is dropped instead, so both sentences
must read correctly when they stop halfway.

**The introduction**, carried by the `home` content and by the text route, reads:
`Welcome!`, then `My name is Marek Vance, and I'm a creative developer (mostly for the
web).`, then `This is my portfolio. Please drive around to learn more about me and
discover the many secrets of this world.`, then `And don't break anything!`. The owner's
name and role are emphasised inline within that sentence rather than set on their own
lines. That is the entire introduction and expanding it changes the product: the argument
is that the world does the explaining. The voice is warm and slightly silly and it uses
exclamation marks, and that voice is the thing to protect when this copy is rewritten.

**The colophon**, headed `Behind the scene`, opens
`Thank you for visiting my portfolio!` and
`If you are curious about the stack and how I built this project, here's everything you
need to know.`, runs six headed sections covering the rendering library and its author
`Ilse Renwick`, the owner's teaching product `Fieldcraft`, the devlogs, the source code
and its licence, the music credited to `Solane`, and a short list of further links set as
a label, a right-pointing double arrow and a link. It closes with the owner's name on its
own line. It is the one long-form reading surface in the product and is set looser than
the rest: larger headings, more space under each paragraph and bolder links. It states
plainly that the shared half of the product is not open and that the rest works without
it.

**Document metadata.** The title is `Marek's` and nothing else, a possessive with nothing
after it, because it reads as a place rather than as a site. The description and the
social description are both `Marek Vance's creative portfolio`, the social title is
`Marek Vance`, the site name is `Marek`, the social card type is `summary_large_image`,
and the share image is generated at build time from the panel gradient, the brand set in
the display face and the hairline motif, rather than fetched.

**The studio.** A top navigation carrying the project list, the world, the achievements,
the pages and the page view record. The project list is a grid of cards, one per project,
each showing its poster, its title, its coordinates, its zone and whether it is published
or a draft, with the draft state stated in words and not only by colour. Writing or
editing a project opens a panel that slides in from the right edge over the list while the
list stays visible behind it, and closing it returns to the list unchanged. Publishing
does not toast: it lands on a full confirmation page naming what was published and where
it now stands, with a way into the world and a way back to the list. A refused publish
returns to the panel with the reason stated against the coordinate fields, naming the
project already standing there, and nothing written.

## Constraints

- One tenant, one account. No visitor accounts, no signup, no invitations and no password
  reset for anyone.
- No comments, no likes, no following, no visitor-to-visitor messaging and no presence.
  No shared vehicles and no voice.
- No email of any kind, no payments, no subscriptions and no second language.
- No native application and no installable package.
- No external network calls at runtime beyond the two backing services and the public
  font host. Measurement is optional, loads after first paint, and no product behaviour
  depends on it.
- **This is a zero-asset build: no binary asset ships in the deployed build**, meaning no
  image file, no audio file, no three-dimensional model, no texture container and no
  video. Geometry, textures, noise, sound and interface glyphs are generated by code, and
  the substitution recipes for each class are stated above rather than left to guesswork.
  The two typeface families are the only external files and the build degrades legibly
  without them, the display face falling back to a plain one.
- Project posters are the one exception and they are uploaded content, not shipped
  assets: they live in the object store and are generated placeholders only when the
  owner supplies none.
- The product cannot be made equivalent for every visitor and does not pretend to be.
  Driving to content is spatial and has no keyboard-only equivalent that is not a second
  product; a timed lap cannot be made time-neutral without ceasing to be a lap; and a
  description of the scene cannot substitute for the scene. The text route is the
  mitigation and is presented as what it is.
- The app must stay responsive with 200 published projects, 30 whispers, 500 laps
  recorded for the current day and 50,000 page view rows.

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
- The server must keep running after this session ends and must not be a child of the
  shell. An ordinary background job dies with its shell, and the app will not be running
  when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `{ "email", "password" }` | `{ "access_token" }` |
| `GET /api/health` | none | `{ "status" }` |
| `GET /api/world` | none | `{ "projects": [...], "areas": [...] }`, published projects only |
| `GET /api/projects` | none | a top-level JSON array of published projects |
| `GET /api/projects/{slug}` | none | one published project; a draft slug is answered as not found |
| `GET /api/projects/{project_id}/images/{image_id}` | none | the poster bytes streamed from the store |
| `POST /api/studio/projects` | `{ "slug", "title", "summary", "link", "world_x", "world_y", "world_z", "zone", "previous_slug", "next_slug" }` | the created project, `published` false |
| `PATCH /api/studio/projects/{id}` | any writable field | the updated project |
| `POST /api/studio/projects/{id}/images` | the file, plus `{ "alt_text" }` | `{ "id", "object_key", "byte_sha256", "alt_text" }` |
| `POST /api/studio/projects/{id}/publish` | none | the published project, or a refusal carrying `{ "error", "message", "occupied_by" }` |
| `POST /api/studio/projects/{id}/unpublish` | none | the project, `published` false |
| `GET /api/areas` | none | a top-level JSON array of areas |
| `GET /api/achievements` | none | a top-level JSON array of achievements |
| `GET /api/whispers` | none | a top-level JSON array of at most 30 whispers |
| `POST /api/whispers` | `{ "uuid", "message", "country_code", "x", "y", "z" }` | the created whisper |
| `POST /api/laps` | `{ "uuid", "tag", "country_code", "duration_ms", "checkpoint_splits" }` | the recorded lap |
| `GET /api/leaderboard` | none | today's board, fastest lap per visitor |
| `GET /api/page-views` | none | the page view record, owner only |
| `POST /api/cookie-choice` | `{ "choice" }`, `accepted` or `declined` | the stored choice |

Every endpoint except `POST /api/auth/login`, `GET /api/health` and the public read
endpoints requires the bearer token. A successful call returns the named resource or
shape; an invalid or unauthorized call is rejected as a client error, never as a server
error and never as a silent success, and the response says why. List endpoints return a
top-level JSON array.

**No mocks.** The poster bytes must exist as real objects in the MinIO bucket at their
scheme's key. Image bytes written to the app container's filesystem, base64 held in a
database column, an in-memory dictionary standing in for the bucket, or a hardcoded
success response the app returns to itself are all violations, however correct the page
looks. The object store is the fact: the app's UI and its own tables can only reflect
what lives in the provider, never substitute for it. The same holds for PostgreSQL: the
publish refusal must be a property of the stored data, not of one request handler's
memory.

## Definition of done

A stranger opens the app, presses once, and drives to any published project to read its
title, poster, facts and awards without leaving the vehicle, and can read the same
content as text without driving at all. The owner signs in, writes a project, uploads its
poster, pins it to a point in the world and publishes it, and it is standing there. A
project held as a draft cannot be seen, listed, opened or have its poster fetched by
anyone who is not the owner, including by its own address. Publishing onto a point a
published project already holds is refused with a reason, and the project already there
is untouched.
