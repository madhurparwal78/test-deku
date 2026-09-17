# Waze Live Map

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
search a starting point and a destination on a full screen map, read the live road
conditions other drivers have coloured it with, open the leave time scheduler, pick an
arrival time, and be told when to set off, without hitting an error page. The hard part
is the departure window: one driver must never end up holding two planned drives whose
departure windows overlap, and that must hold when two requests for overlapping windows
arrive at the same instant. The window a driver holds must be a real row in the database
that a second request cannot claim; a message the app returns to itself does not count.

## Overview

Waze Live Map is the public web face of a community driven navigation product. The
defining idea is that the map and the traffic on it come from the people driving it.
Drivers report what they see, police, crashes, hazards, closures, gas prices, and
everyone else gets a truer picture of the road a moment later. The company's own words
are `Where drivers help drivers`.

The product is a full viewport map with a driving directions planner. A visitor opens
it, pans and zooms, searches a starting point and a destination, reads the live road
conditions, and plans a drive. Road conditions are coloured by severity, and that
severity is computed from what drivers have reported on each road segment, so the
colours are community sourced rather than published from a schedule.

The state changing heart of the product is the leave time scheduler. A `Leave now`
control opens it, and choosing an arrival time turns a lookup into a planned drive: the
app solves for the time to set off, holds that departure window for the driver, and
raises a reminder before it. That is what the rest of the product exists to serve.

Four real-time capabilities are load bearing, and none of them can be faked with
static data: ingesting what drivers report as they report it, holding a road graph
whose conditions update as those reports land, routing over that graph as it stands
right now, and a privacy safe community layer that shows what the crowd saw without
exposing any individual driver. Low connectivity is handled by holding what has
already been drawn rather than blanking the map.

The wider Waze product has four faces. This task builds one of them, the web Live Map.
It deliberately is not the others: no turn by turn navigation client, no voice or lane
guidance, no offline regions, no real time telemetry ingestion from phones, no map
matching, no machine learning traffic estimation, no map editor, no advertising, no
partner data exchange, no carpool matching and no chat. It has no comments, no likes,
no messaging and no leaderboard.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `visitor` | Open the map on any of its entry routes, pan, zoom, read the coordinate readout, search a starting point and a destination, swap them, read live road severities and report markers, calculate a route, open the leave time scheduler and solve for a leave time, read the marketing, privacy, terms and not found routes | **Cannot file a report, cannot vote on a report, cannot save a planned drive, cannot read any planned drive, any reminder or any page view record** |
| `driver` | Everything a visitor can do, plus file a report on a road segment, vote to confirm or dispute another driver's report, save a planned drive, list and cancel their own planned drives, and read their own reminders and their own page view records | **Cannot vote on their own report, cannot read, cancel or alter another driver's planned drive, cannot read another driver's reminders or page views** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button
in the UI is not authorization: a direct API call from a `visitor` session to any
`driver`-only endpoint must be rejected by the server (an unauthorized request is
denied, not served), leaving the protected state unchanged.

Signup is open: anyone can create a `driver` account with an email and a password. The
map, the place index, the live severities, the report markers and a route calculation
all answer without an account. Signing in gates reporting, voting, planned drives,
reminders and the page view record, and nothing else.

Three `driver` accounts are seeded: `driver@example.com`, `driver2@example.com` and
`driver3@example.com`.

## Core features

### Auth

Accounts are email and password, implemented by this app. Passwords are stored hashed,
never in clear text. A successful login returns the field `access_token`, a bearer credential the
client sends on every request that changes state or reads a driver's own rows. There is no external
identity provider.

1. Signing up with an email that is not already registered succeeds and returns a
   bearer token. Signing up with an email that is already registered is rejected as
   invalid, names the email as the reason, and creates no second account.
2. Signing in with a seeded email and the seeded password succeeds and returns a
   bearer token. Signing in with a wrong password is denied, and the response does not
   reveal whether the email exists.
3. A request to a `driver`-only endpoint with no token, an unparseable token or an
   expired token is denied and changes nothing.

### The live map surface

The map is a full viewport raster tile map. Tiles are square images requested by zoom,
column and row on a path shaped `/row-tiles/live/base/{z}/{x}/{y}`. Only the tiles
covering the current viewport at the current zoom, plus a small margin, are requested,
and a higher resolution variant is requested only where the display warrants it. Each
tile fades in as it resolves rather than popping, and while the map loads a placeholder
and a loader hold the space.

4. Dragging the map pans it and the tile grid resolves for the new viewport. Zooming in
   and out changes the zoom level and requests the tiles for it. A tile request outside
   the viewport and its margin is not made.
5. A vertical stack of circular controls sits bottom right over the map: an edit
   pencil tinted on the primary colour, a locate crosshair, and a jointed zoom pill
   whose plus and minus halves meet as one control. A live coordinate readout shows the
   map centre, in the shape `28.459 | 77.025`.
6. The meta row beside the readout carries the links `About Waze`, `Community`,
   `Partners`, `Support`, `Terms`, `Notices` and `How suggestions work`.
7. Incident and report markers draw on their own layer above the tiles. The visitor
   position marker carries a breathing halo. Traffic jams draw as dashed polylines in
   their severity colour.

### Endpoint search

The rail holds a starting point field with the placeholder `Choose starting point`,
marked by a hollow origin dot, and a destination field with the placeholder
`Choose destination`, marked by a pin. A vertical connector links them and a swap
control exchanges them.

8. Typing into either field opens a ranked suggestions list from the seeded place
   index, matching the place name on a case insensitive substring and ordering matches
   by name ascending. A search that matches no place says so rather than showing an
   empty list.
9. Picking a suggestion resolves the field to that place's coordinate and closes the
   list. A coordinate can also be resolved the other way: the nearest seeded place to a
   given latitude and longitude is returned.
10. The swap control exchanges the two endpoints. With both endpoints resolved the
    route is recalculated after a swap and the drawn line changes accordingly.
11. Six places are seeded and searchable: `Connaught Place`, `Cyber Hub Gurugram`,
    `Noida Sector 18`, `Indira Gandhi Airport`, `Hauz Khas Village` and
    `Akshardham Temple`.

### Live road conditions, coloured by drivers

Five road segments are seeded: `Ring Road North`, `Outer Ring Road`,
`NH48 Delhi Gurugram`, `Barapullah Elevated` and `DND Flyway`. Each carries a free flow
driving time and a drawable path, and each carries a current severity that is computed
from the reports drivers have filed on it, never stored.

12. A segment reads `heavy` when it carries at least one active `closure` report or at
    least one active `crash` report, or two or more active `jam` reports. It reads
    `slowing` when it carries exactly one active `jam` report, or at least one active
    `hazard` report and no condition that would make it `heavy`. Otherwise it reads
    `clear`.
13. Severity is never carried by colour alone. `clear`, `slowing` and `heavy` each own
    a colour, and a jam additionally draws as a dashed line that crawls along its own
    length so the direction the traffic is trying to move is legible without reference
    to the colour.
14. A segment whose only report has expired reads `clear` again, and its dashed
    treatment is removed. A request for the live severities is answered without a
    token.

### Community reporting and crowd verification

15. A signed in driver files a report against one segment, choosing one of nine types:
    `police`, `jam`, `hazard`, `closure`, `crash`, `gas` for a gas station, `place`, `chat` or `carpool`.
    The report is created `active` and its freshness runs for 60 minutes from the moment
    it is filed. The segment's severity is recomputed at once and the marker appears.
    A report naming a segment that does not exist, or a type outside those nine, is
    rejected as invalid and creates no row.
16. A report whose freshness has run out reads `expired` and stops colouring its
    segment.
17. A driver votes `confirm` or `dispute` on another driver's report, once per report.
    A second vote from the same driver on the same report is rejected as invalid and
    does not change the report. A driver voting on their own report is denied.
18. A `confirm` extends the report's freshness to 60 minutes after the vote, capped at
    180 minutes after it was filed. A confirm arriving after the cap leaves the
    freshness at the cap.
19. A `dispute` carries weight 2 when the voting driver's reputation is 3 or more, and
    weight 1 otherwise. A driver's reputation is the number of their own reports that
    have ever received at least one confirm, computed on read and never stored. When a
    report's accumulated dispute weight reaches 2 it becomes `dismissed` at once and
    stops colouring its segment.

### Routing

20. With both endpoints resolved, a route is returned carrying its ordered segments,
    the drawable geometry of each, a per segment severity and a total travel time, and
    the map draws it in that live traffic colouring. A route request naming an endpoint
    that does not resolve is rejected as invalid and draws nothing.
21. Travel time is the sum of each segment's free flow time scaled by its severity:
    `clear` at 100 percent, `slowing` at 150 percent, `heavy` at 250 percent. Each
    segment's scaled time is rounded up to the next whole minute before the sum. A
    route over `Outer Ring Road`, free flow 12 minutes and `slowing`, then `DND Flyway`,
    free flow 9 minutes and `clear`, has a travel time of 27 minutes: 18 plus 9.
22. A route accepts either a departure time or an arrival time. Given an arrival time
    it solves backwards for the time to set off.
23. Routing is dynamic: the engine recalculates a drawn route instantly when conditions
    change under it, which happens when a report is filed, confirmed, dismissed or
    expires on one of its segments. The travel time, the optimal path and any solved
    leave time are all recomputed. Where a different path over the seeded segments is
    faster, that alternative is offered by name.
24. The offer does not flap. A faster alternative is offered only when it saves at
    least 3 minutes against the path currently drawn; an alternative that saves less is
    not offered, and the drawn route does not change. A recalculation that leaves the
    route unchanged does not redraw it or move the map.

### The leave time scheduler

A `Leave now` control, a clock glyph and a caret in a pill, opens the scheduler as a
panel that slides over the rail. The visitor departs now, or picks a specific arrival
time. A coaching tooltip introduces the control the first time the application loads,
titled `Edit your arrival time`, with the body `Find the best time to leave, so you get
to your destination on time` and a `Got it` dismiss.

25. Choosing an arrival time solves for the leave time: the arrival time minus the
    travel time minus a fixed 5 minute buffer. For an arrival time of
    `2026-09-17T09:00:00Z` on the 27 minute route above, the leave time is
    `2026-09-17T08:28:00Z`.
26. Choosing an arrival time that is already in the past is rejected as invalid, names
    the arrival time as the reason, and produces no planned drive.
27. The scheduler is open to a visitor: solving for a leave time needs no account. Only
    saving the result as a planned drive does.

### Planned drives and the set off reminder

28. A signed in driver saves the solved result as a planned drive. The drive stores its
    origin, its destination, the arrival time, the leave time and the travel time, and
    starts in the state `scheduled`. Saving lands on that drive's own page, which states
    all five values and when the reminder becomes due.
29. The reminder becomes due at the leave time minus a fixed 15 minute lead. For the
    leave time above, the reminder is due at `2026-09-17T08:13:00Z`. A planned drive
    reads `scheduled` before its reminder time and `reminded` from the moment that
    time has passed.
30. A driver lists only their own planned drives, reads only their own reminders, and
    cancels only their own drives. A request for another driver's drive is denied and
    the row is not changed. A cancelled drive reads `canceled` and holds no departure
    window.
31. **A driver holds at most one planned drive whose departure window overlaps
    another.** A departure window runs from the leave time to the arrival time, and two
    windows overlap when one starts strictly before the other ends and ends strictly
    after the other starts; windows that touch end to start do not overlap. A request
    whose window would overlap a window the same driver already holds is rejected, the
    reason names the conflicting drive, and no second row is created. **Two simultaneous
    requests for overlapping windows must not both succeed: exactly one is accepted and
    the other is rejected. This must hold at the database level.** A rejected request
    leaves no partial state: no orphaned drive row and no reminder.
32. One planned drive is seeded so this boundary exists from first start:
    `driver@example.com` holds a `scheduled` drive from `Connaught Place` to
    `Cyber Hub Gurugram` arriving `2026-09-17T09:00:00Z`.

### Global chrome

33. On the map routes the header condenses: a nine dot app launcher and a three dot
    overflow menu replace the navigation, and `Log In` becomes a filled button on the
    brand colour. The launcher opens a floating panel listing `Live map`, `Map editor`,
    `Forums`, `Wazeopedia`, `Academy` and `Partner hub`. The overflow menu lists
    `Help center` and `Report an issue`. Escape closes either.
34. On the content routes the full marketing header renders: the Waze smiley mark as a
    home link, then `Waze`, `Waze for Cities` with the sub links `Case Studies`,
    `Traffic Events` and `Waze Beacons`, `Partners` with the sub link
    `Product Partners`, a `Map editors community` link, and right aligned `Live Map`,
    `Download` and a pill shaped `Log In`.
35. The footer carries four link columns. `Support`: `Help Center`,
    `Fix a map issue`, `Community forums`, `Community wiki`, `Waze Academy`.
    `Live Map`: `Plan a drive`, `Major events`, `Edit the map`. `About`: `About us`,
    `Contact Us`, `Waze blog`, `Communities`, `Press`, `Suggestion Box`. `Partners`:
    `Waze for Cities`, `Transport SDK`, `Developers`. Below them the Waze wordmark, the
    tagline `Where drivers help drivers`, four circular social links, a language
    selector defaulting to `English`, the legal row `Terms of Use`, `Privacy Policy`
    and `Copyright Notice`, and the line
    `© 2006 - 2026 Waze Mobile. All Rights Reserved.`
36. An app download bar is pinned to the bottom of the live map: a close control, the
    app tile, the label `waze` with a five star row, the sub label
    `Navigation & Live Traffic`, a `Send to your phone` control, and App Store and
    Google Play badges. The marketing variant shows a `Get` button instead.

### Content routes

37. The conversion route renders inside the marketing chrome and leads with
    `Don't have Waze yet?` and `Join other drivers already avoiding traffic and hazards
    with Waze.` alongside the store affordances.
38. An unknown address renders the product's own not-found page, inside the marketing
    chrome, and answers not found. It centres a bold block on a light, vivid indigo
    field, a large `404`, the Waze face mascot looping a red thread through the zero,
    the heading `Page not found`, the subhead
    `The page you were looking for is out of reach`, and a way back to the map.
39. A privacy page and a terms page are each reachable from the footer of every page.
    The privacy page states what Waze Live Map records about a driver, which is their
    email, the reports they file, the drives they plan and the routes they view, and
    how long each is kept.

### The record of what was viewed

40. Every view of a public route is recorded with the route and the moment it was
    viewed. A signed in driver reads their own records; a view taken without an account
    is recorded against no driver and is readable by nobody. A request for another
    driver's records is denied.

### Refusing a bot

41. Every form on the site carries an unattended decoy field. A submission that arrives
    with that field filled is refused and writes nothing. A submission of the same form
    repeated more than three times inside one minute from the same origin is refused and
    writes nothing.

## User flow

The information architecture is a small set of routes. Three of them render the same
live map application and differ only by entry context; the rest are ordinary content
pages in the marketing chrome.

| Route | Purpose | Auth |
|---|---|---|
| `/` | Live Map application, default entry | none |
| `/as` | Live Map application, alternate entry context | none |
| `/gs` | Live Map application, alternate entry context | none |
| `/scheduler` | the leave time scheduler, sliding over the rail | none |
| `/report` | the report panel, sliding over the rail | `driver` |
| `/drives` | the driver's planned drives, in the rail | `driver` |
| `/drives/{id}` | one planned drive, full page | `driver` |
| `/ul` | conversion route, download prompt | none |
| `/412`, `/416`, `/417`, `/419` | content routes in the marketing chrome | none |
| `/privacy` | privacy page | none |
| `/terms` | terms page | none |
| `/login` | sign in | none |
| `/signup` | create a driver account | none |

`/`, `/as` and `/gs` mount the same application and render identically. They differ
only by entry context.

**Entry and redirects.** A visitor opening `/`, `/as` or `/gs` gets the map, the empty
rail and the download bar, with no sign in prompt. An unauthenticated request for
`/report`, `/drives` or `/drives/{id}` is sent to `/login`, and signing in returns to
the route that was asked for. Signing in from the header lands on `/`. Signing out
returns to `/` and the rail drops back to its unauthenticated state. A token that has
expired mid action leaves the request denied rather than served, and the browser is
returned to `/login` with the reason named. A driver asking for another driver's
`/drives/{id}` is denied and the row is not changed. Any unknown address renders the
product's own not found page.

**Journeys.**

1. *Read the road.* Open `/`. The header condenses to the launcher and the overflow
   menu with a filled `Log In`. The rail mounts titled `Driving directions` with two
   empty fields. The map centres and starts requesting tiles, which fade in. Segments
   draw in their live severity colouring, `Ring Road North` heavy and `DND Flyway`
   clear. Report markers draw above the tiles. The coordinate readout shows the centre.
   The download bar mounts.
2. *Plan a drive for an arrival time.* Type into the starting point field, pick
   `Connaught Place`. Type into the destination field, pick `Cyber Hub Gurugram`. The
   route draws on the map in its traffic colouring and the rail gains a stronger
   shadow. Open `Leave now`; the scheduler slides over and the tooltip
   `Edit your arrival time` shows once. Choose an arrival time. The rail states the
   leave time the app solved for.
3. *Save it and be reminded.* Signed in as `driver2@example.com`, save the planned
   drive. The app lands on that drive's own page stating the origin, the destination,
   the arrival time, the leave time, the travel time and when the reminder becomes due.
   `/drives` lists it.
4. *The overlap is refused.* Signed in as `driver@example.com`, who already holds a
   scheduled drive arriving `2026-09-17T09:00:00Z`, save a second drive whose departure
   window overlaps it. The request is refused, the reason names the conflicting drive,
   and no second row exists.
5. *Colour the road.* Signed in, open `/report`. The report panel slides over. Pick
   `Ring Road North` and the type `jam`. The report is filed, its marker appears, and
   the segment's severity is recomputed at once.
6. *Verify somebody else.* Signed in as `driver3@example.com`, confirm an active
   report; its freshness extends. Signed in as `driver@example.com`, whose reputation
   is 3, dispute one instead; it is dismissed at once and stops colouring its segment.
7. *Swap the endpoints.* With both fields filled, use the swap control. The endpoints
   exchange and the route is recalculated.
8. *Miss the road.* Ask for an address that does not exist. The product's own not found
   page renders inside the marketing chrome and answers not found.

**States.** Every list has an empty state: the rail before either endpoint resolves
shows its two placeholders and no route, `/drives` with nothing scheduled says so and
points at the scheduler, and a search with no match says so rather than showing an empty
list. Every page has a loading state: the map holds a placeholder and a loader until
tiles arrive, a route being calculated shows a spinner in the rail, and a suggestions
list being fetched shows a spinner in the field. Errors never crash the app: a failed
route calculation names the reason in the rail and leaves the previous route drawn, and
a refused report or drive names the reason and changes nothing.

## UI/UX notes

In the first moment a visitor should see the road they are about to drive, already
coloured by the people on it, and understand that those colours came from drivers
rather than from a published schedule. This is a consumer utility read at a glance and
often in a hurry, so the map is the subject and everything else is chrome that gets out
of its way. Atmosphere belongs to the marketing and not found routes; on the map the
tiebreak is always legibility over expression. Two stances govern the rest: live truth
over polish, and subject over chrome, which is why the map takes the whole window and
every control floats over it rather than boxing it in.

The interface palette and the report palette are two visibly separate systems, and
keeping them apart is a requirement rather than a preference: a report colour must never
be mistakable for a control. The interface runs on near white surfaces with deep neutral
text, and the primary action is a mid, vivid cyan that is the only thing on a page
wearing it. Road conditions and driver reports own the second system: clear in a mid,
vivid green, slowing in a mid, vivid amber, heavy in a light, vivid red, each report type
holding its own colour and its own glyph. The exact shades are yours, so long as each
holds the family, tone and role named here.

Type is the product's identity and is carried exactly. The display face is the rounded
brand family `Waze Boing`, also named `Boing` and `Waze Boing HB`, and the text face is
`Noto Sans`, with `Rubik` and `Gotham Rounded` also present. Every face loads with a
swap fallback so words paint immediately and reflow when the web font arrives.

Motion is functional and short, and every moment that moves is reporting something
real. The visitor position marker breathes so it can be found at a glance. A marker
ready to report pings a ring outward like a drop in water. A jam crawls its dashes along
its own length so the direction of flow is legible. Tiles fade in rather than popping,
panels slide up, things fade rather than snap, and on the marketing routes a group
drifts up one just after another. Nothing animates on the map that is not a real
condition. Every animation and every transition respects a reduced motion preference,
and under it the breathing, the pinging and the crawling stop while the tile fade is
preserved rather than removed, because the fade is what stops the map snapping into
place.

Density is comfortable on the map and compact in the rail, because the rail is read
repeatedly and the map is looked at. Shape is soft without being round: panels carry a
gentle corner, pills are fully rounded, the footer's social links are circles, and where
a title bar and the sheet beneath it must read as one surface only the outer corners
round. The layout is a persistent left rail over a map pane: the rail carries the
planner, the saved drives and the report control, and the map is the pane beside it.
That arrangement is responsive. Below the mobile ceiling the live map stacks top to
bottom, with the download call to action riding the top, the condensed header under it,
the rail spanning the full width as a sheet, and the map filling the rest. From the
tablet breakpoint upward the rail detaches into its floating top left position over the
map and the header expands, and at the wider steps the marketing header reaches its full
navigation and the footer lays four columns side by side.

The accessibility floors are contract. Body text meets WCAG AA contrast against its
background in both the light interface and the dark map theme. Every control is reachable
by keyboard navigation with a visible focus ring, and map control touch targets are
comfortably sized. Icon only controls carry a visually hidden text label. Meaning is
never carried by colour alone. A forced colours dark preference is honoured and remaps
surfaces, text and separators to system colours.

What this must not look like: a page dominated by one hue family with no second signal,
decoration standing in for content, or a marketing composition where the working
interface belongs. The map routes carry no hero, no oversized type and no editorial
layout.

## Technical requirements

The HTML for every route is produced on the server and arrives complete on first paint;
the browser receives a rendered page rather than an empty shell it has to fill. Search
suggestions, the scheduler panel, the report panel and the live severity refresh are
fragment requests that replace a region of the page in place. Map tile loading, panning
and zooming are progressive enhancement layered over markup that already renders without
them.

Backend: **FastAPI** serving **Jinja** templates. Frontend: **HTMX** over those server
templates. Datastore: **PostgreSQL**, reached at `DATABASE_URL`. Auth: app implemented
email and password with bearer tokens, passwords stored hashed. Health: `GET /api/health`
returns `200` once the app is ready and its database is reachable. Logging: one line per
request to stdout carrying the method, the path and the response status, and no log line
carries a password, a token or a password hash.

Use only the libraries named here plus their direct dependencies. Do not introduce a
second database, cache, queue, object store, identity provider or mail vendor, the only
backing service available in this environment is **PostgreSQL**, and reaching for
anything else is a contract violation. PostgreSQL is already running and reachable at
`DATABASE_URL`; do not download, install, compile or start a copy of it.

Map tiles are generated at request time or proxied from an open source by this app.
No tile image is bundled with the app and no request leaves the environment at runtime.

First paint does not wait on the map: the header, the empty driving directions rail and
a map placeholder render before any tile arrives, and tiles stream in afterwards. Tile
requests cover the viewport at the current zoom plus a small margin and nothing more.
Fonts load with a swap strategy. Motion stays on properties that stay smooth on modest
hardware, and the interface is usable within a couple of seconds of the map beginning to
load. Performance, responsive reflow and the accessibility floors are cross cutting:
they apply to every route, not only to the map.

Every response carries the standard security headers, including a strict transport
policy and a nosniff content type policy. Nothing the browser downloads carries a
credential, an API key or an admin token. Every public route declares a social preview
title and a social preview image, no two routes share a preview title, and every declared
preview image resolves.

## Data model

Seven tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture
data, not a secret. Hash it as normal; the exact literal must work at login, and it must
be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### `drivers`

`id`, `email` unique, `password_hash`, `display_name`, `created_at`. `reputation` is
derived on read and never stored: the number of this driver's own reports that have ever
received at least one `confirm` vote.

### `places`

`id`, `name` unique, `latitude`, `longitude`, `created_at`. The searchable place index.

### `segments`

`id`, `name` unique, `base_minutes`, `path`, `created_at`. `base_minutes` is the free
flow driving time across the segment. `path` is the polyline the map draws, a string of
`latitude,longitude` pairs separated by spaces. `severity` is derived on read and never
stored, by the rule in `## Core features`.

### `reports`

`id`, `segment_id`, `driver_id`, `type`, `latitude`, `longitude`, `status`,
`created_at`, `expires_at`. `type` is one of `police`, `jam`, `hazard`, `closure`,
`crash`, `gas`, `place`, `chat`, `carpool`. `status` is one of `active`, `expired`,
`dismissed`. A report counts as active while its `status` is `active` and its
`expires_at` is still in the future.

### `report_votes`

`id`, `report_id`, `driver_id`, `vote`, `created_at`. `vote` is `confirm` or `dispute`.
A driver casts at most one vote on any one report, and never on their own report.

### `planned_drives`

`id`, `driver_id`, `origin_place_id`, `destination_place_id`, `arrival_at`, `leave_at`,
`travel_minutes`, `status`, `reminder_at`, `created_at`. `status` is one of `scheduled`,
`reminded`, `completed`, `canceled`.

The invariant: a driver holds at most one planned drive whose departure window overlaps
another. A departure window runs from `leave_at` to `arrival_at`, and two windows overlap
when one starts strictly before the other ends and ends strictly after the other starts.
Windows that touch end to start do not overlap, and a `canceled` drive holds no window.
Two simultaneous requests for overlapping windows must not both succeed: exactly one is
accepted, the other is rejected, and no second row exists afterwards. This must hold at
the database level.

### `page_views`

`id`, `driver_id` nullable, `route`, `viewed_at`. One row per view of a public route.

### Seed data

Three drivers, all with the password `deku-demo-pw-2026`: `driver@example.com`
(`Amrita Bose`, seeded so its reputation reads 3), `driver2@example.com`
(`Ravi Menon`, reputation 0) and `driver3@example.com` (`Lena Fischer`, reputation 1).

Six places: `Connaught Place`, `Cyber Hub Gurugram`, `Noida Sector 18`,
`Indira Gandhi Airport`, `Hauz Khas Village`, `Akshardham Temple`.

Five segments with their free flow times: `Ring Road North` 14 minutes,
`Outer Ring Road` 12 minutes, `NH48 Delhi Gurugram` 21 minutes, `Barapullah Elevated`
7 minutes, `DND Flyway` 9 minutes.

Reports, seeded active and fresh, producing exactly these severities: two `jam` reports
on `Ring Road North`, which reads `heavy`; one `jam` on `Outer Ring Road`, which reads
`slowing`; one `closure` on `NH48 Delhi Gurugram`, which reads `heavy`; one `hazard` on
`Barapullah Elevated`, which reads `slowing`. `DND Flyway` carries none and reads
`clear`.

One planned drive: `driver@example.com` holds a `scheduled` drive from `Connaught Place`
to `Cyber Hub Gurugram` arriving `2026-09-17T09:00:00Z`.

Seeding must be idempotent, restarting the app must not duplicate rows.

## Front-end specification

The visual system measured from the product, carried in full.

### Colour tokens

Every colour is a named token read off the document root, and every component colour
references a token rather than a raw value. The exact values are yours so long as each
holds the family, tone, shade and role named here.

| Token role | Carried as |
|---|---|
| brand | a light, vivid cyan, the mark and the filled sign in button on the map |
| primary | a mid, vivid cyan, the only thing on a page wearing it |
| primary variant | the same family one step deeper, for the pressed state |
| on primary | a near-white neutral |
| content default | a deep neutral |
| content, second emphasis | a deep neutral one step lighter |
| content, third and fourth emphasis | two mid cool neutrals |
| hint text | a mid cool neutral |
| disabled text | a light cool neutral |
| background default | a near-white neutral |
| background variant | a second near-white neutral, very slightly cooler |
| surface default | that second near-white neutral |
| surface variant | a near-white neutral one step deeper |
| surface alt | a near-white cool neutral |
| separator default | a near-white neutral |
| hairline | a near-white neutral |
| hairline strong | a light cool neutral |
| handle | a near-white neutral, the lightest surface in the system |
| safe | a mid, vivid green, meaning good, clear, go |
| safe variant | a deep, soft green, for the pressed state |
| cautious | a mid, vivid amber, meaning warning |
| cautious variant | a mid, vivid orange, for the pressed state |
| alarming | a light, vivid red, meaning danger or heavy |
| alarming variant | a mid, vivid red, for the pressed state |
| promotion variant | a light, vivid indigo, the promotional accent |

Tinted surfaces, one very pale wash per semantic family: a near-white cool neutral for
blue, a near-white neutral for green, a near-white warm neutral for orange, a near-white
cool neutral for purple, a near-white warm neutral for red, a near-white warm neutral
for yellow.

Scrims and interaction ink. The modal background is the deep neutral of default text at
a little over half opacity, and a table overlay is the mid cool neutral at the same
opacity. Interaction ink over the primary colour is that deep neutral at a barely there
opacity when hovered, a little stronger when pressed and a little stronger again when
focused. The dark map theme reuses the always dark tokens: a deep neutral surface, a deep
neutral background one step darker, and a near-white neutral for content.

### Report and traffic colour system

A system of its own, deliberately separate from the interface palette. Each report type
owns one colour and one distinct glyph, and the glyph is what carries the meaning when
colour cannot.

| Report type | Carried as |
|---|---|
| `police` | a light, vivid cyan |
| `jam` | a light, vivid red |
| `hazard` | a mid, vivid amber |
| `closure` | a light, soft orange |
| `crash` | a near-white neutral |
| `gas` | a mid, vivid green |
| `place` | a light, soft indigo |
| `chat` | a mid, vivid teal |
| `carpool` | a mid, vivid teal |

Traffic severity on the road follows the status semantics: clear roads in the safe mid,
vivid green, slowing in the cautious mid, vivid amber, heavy or standstill in the
alarming light, vivid red, with the heavy case drawn as crawling stripes so flow
direction reads as well as severity.

### Typography

The display face is the rounded brand family `Waze Boing`, also named `Boing` and
`Waze Boing HB`, in weights 300, 400, 500 and 600. The text face is `Noto Sans` in
weights 300 through 700. A neutral `Rubik` at 400 and 500 and `Gotham Rounded` at 500
also appear. All faces load with a swap fallback. The rendered scale, most used first:

| Size | Weight | Line height | Use |
|---|---|---|---|
| `16px` | 400 | `18.4px` | body, controls |
| `13px` | 400 | `20px` | secondary, footer |
| `11px` | 400 | `13px` | fine print |
| `24px` | 400 | `24px` | card titles |
| `16px` | 500 | `20.8px` | emphasised labels |
| `20px` | 400 | `23px` | subheadings |
| `28px` | 500 | `33.6px` | large headings |
| `24px` | 700 | `30px` | bold display |

### Layout and stacking

Three principal breakpoints drive the reflow: a mobile ceiling, a tablet floor, a
desktop step and a wide step. Retina tiles are gated on a high resolution display. A
forced colours dark query is honoured. Stacking is a fixed ladder and no value sits
outside it: map panes at the base, floating cards and controls above them, menus and
dropdowns above those, full screen overlays and tour steps at the top.

### Iconography

Icons are drawn as vector geometry rather than image files, so they can be redrawn
sharp at any size without the originals.

- **Waze wordmark.** A single filled path in the default content colour, in a wide
  short view box.
- **Waze smiley mark.** Five primitives in a near square view box: a face body path
  filled near white, a face outline path, a right eye circle, a left eye circle and a
  smile path. It is a white rounded blob with two dot eyes and a smile.
- **Social marks**, in the footer, filled in the default content colour: an X mark as
  one path, and an Instagram mark as two paths plus a dot circle.
- **Interface and report glyphs** (menu, search, swap, clock, zoom, pencil, locate, and
  one per report type) are redrawn as simple vector primitives at the `16px` and `24px`
  steps. They carry no measured geometry and are reconstructions.

### Global chrome detail

The marketing header is a slim bar over white carrying the smiley mark as a home link,
the primary navigation, and right aligned `Live Map`, `Download` and a pill shaped
`Log In` with a hairline border and a primary label. On live map routes it condenses to
the nine dot launcher and the overflow menu, and `Log In` becomes a filled button on the
brand colour.

The launcher opens a floating panel with a soft wide shadow listing the six app
destinations; the overflow menu lists `Help center` and `Report an issue`. Both carry a
gentle corner and sit in the menu band of the stacking ladder.

The footer carries its four link columns as a heading plus small links, then the
wordmark, the tagline, four circular social links, the language selector, the legal row
and the copyright line. Social links animate a focus ring outward from a wide
transparent ring to nothing.

The app download bar is pinned to the bottom of the live map over white: a close
control, the app tile, the label `waze` with a five star row and the sub label
`Navigation & Live Traffic`, a `Send to your phone` control, and the two store badges
with a gentle corner. The marketing variant shows a `Get` button on the brand colour as
a fully rounded pill.

### The map surface in detail

The map pane is positioned by a transform and pans by translating that pane; zoom
animates smoothly rather than stepping. Each tile carries a hint that its fade is cheap
to composite and transitions its opacity, so the grid resolves smoothly rather than
popping. While the map loads, a flat fill on the surface colour and a centred vector
spinner hold the space.

The bottom right control stack sits over white, each control circular with a soft
double shadow: the edit pencil tinted on the primary colour, the locate crosshair, and
the jointed zoom pill whose plus half rounds only at the top and whose minus half rounds
only at the bottom. The coordinate readout and the meta row links sit beside them.

Incident and report markers draw on their own layer above the tiles. The visitor
position and event markers carry the breathing halo. Traffic jams draw as dashed
polylines animated so the dashes crawl, coloured by severity.

### The driving directions rail in detail

A card anchored top left over the map, with a gentle corner, titled
`Driving directions` at the card title step. It holds the starting point field marked by
a hollow origin dot on the brand colour, the destination field marked by a red pin, a
vertical connector between them and a swap control. Each field opens a suggestions list
whose panel casts an inset shadow from its top edge so it reads as sliding up from under
the field.

The `Leave now` control is a clock glyph and a caret in a fully rounded pill. The
coaching tooltip that introduces it sits over a hard light overlay and carries the title
`Edit your arrival time`, the body `Find the best time to leave, so you get to your
destination on time` and a `Got it` dismiss.

When both endpoints resolve the card gains a strong wide shadow and the map draws the
route with live traffic colouring. A title bar rounds only its top corners and the
schedule reducer beneath rounds only its bottom, so the two read as one sheet.

### Motion detail

The default ease carries almost everything: a gentle acceleration and a longer settle.
A quicker settle is used where something lands, a long reveal on the marketing fades,
and an anticipation, an overshoot and a pull back exist for the few moments that need
them. The named moments:

| Moment | What it does |
|---|---|
| `location-pulse`, `map-marker-pulse`, `events-user-location-pulse` | grow the position marker slightly while a halo in a mid, vivid cyan breathes around it |
| `sd-pulse`, `pulse` | ring a report ready marker outward like a drop in water, with a mid, vivid teal shadow |
| `wzGeoPulse` | the same ring in a red defined inside the animation itself |
| `jam-dash-animation-1` through `jam-dash-animation-7` | crawl a dashed line along its own length so a jam appears to flow |
| `slide-up` | a panel arriving |
| `fade-in`, `fade-out` | things appearing and leaving |
| `spin`, `spinner-spin`, `overlay-spin` | waiting |
| `rcTriggerZoomIn`, `rcTriggerZoomOut` | the zoom control responding |

The marketing reveal drifts a group up one just after another rather than all at once.
Everything else is quick and quiet.

### Accessibility and internationalization detail

Meaningful icons carry a visually hidden text label, following the access text pattern
that also gives the hidden `Home` and `Waze` labels. Colour is never the only carrier of
meaning: report types pair colour with a distinct glyph and traffic severity pairs colour
with the dashed animation. The forced colours dark preference remaps surfaces, text and
separators to system colours. All controls are keyboard reachable with a visible focus
affordance, and map control touch targets meet a comfortable minimum.

The language selector defaults to `English` and offers the wider set: `العربية`,
`Čeština`, `Deutsch`, `Español`, `Español-América Latina`, `Français`, `עברית`,
`Magyar`, `Bahasa Indonesia`, `Italiano`, `Melayu`, `Nederlands`,
`Português (Brasil)`, `Română`, `Русский`. Right to left layouts are supported for
Arabic and Hebrew. Localised numerals, address formats, distance units in miles or
kilometres, and driving side on the left or the right all flow through the planner.

### Copy deck

All user facing strings, verbatim.

**Header and navigation:** `Waze`, `Map editors community`, `Waze for Cities`,
`Case Studies`, `Traffic Events`, `Waze Beacons`, `Partners`, `Product Partners`,
`Live Map`, `Download`, `Log In`, `Home` as a hidden label.

**App launcher:** `Live map`, `Map editor`, `Forums`, `Wazeopedia`, `Academy`,
`Partner hub`. **Overflow menu:** `Help center`, `Report an issue`.

**Routing card:** `Driving directions`, `Choose starting point`, `Choose destination`,
`Leave now`. **Scheduler tooltip:** `Edit your arrival time`, `Find the best time to
leave, so you get to your destination on time`, `Got it`.

**Download bar:** `waze`, `Navigation & Live Traffic`, `Send to your phone`, `Get`.

**Map meta row:** `About Waze`, `Community`, `Partners`, `Support`, `Terms`, `Notices`,
`How suggestions work`.

**Footer:** `Support` (`Help Center`, `Fix a map issue`, `Community forums`,
`Community wiki`, `Waze Academy`), `Live Map` (`Plan a drive`, `Major events`,
`Edit the map`), `About` (`About us`, `Contact Us`, `Waze blog`, `Communities`, `Press`,
`Suggestion Box`), `Partners` (`Waze for Cities`, `Transport SDK`, `Developers`),
`Terms of Use`, `Privacy Policy`, `Copyright Notice`,
`Where drivers help drivers`, `© 2006 - 2026 Waze Mobile. All Rights Reserved.`

**Not found route:** `Page not found`, `The page you were looking for is out of reach`.
**Conversion route:** `Don't have Waze yet?`, `Join other drivers already avoiding
traffic and hazards with Waze.` **Language default:** `English`.

### Generating every asset: the zero-asset substitution guide

No binary from the original product is available, so every asset is generated.

| Original asset | Build instead |
|---|---|
| the brand display font | a rounded geometric fallback stack, `Baloo 2`, then `Quicksand`, then `system-ui`, then `sans-serif`, all free web fonts, no binary copied |
| the text font, `Noto Sans` and `Rubik` | load by name from the web font provider; fall back to `system-ui`, `Segoe UI`, `Roboto`, `sans-serif` |
| the icon font | redraw each glyph as an inline vector primitive at the `16px` and `24px` steps |
| map tile images | generate a calm base map style at request time, or proxy an open tile source; never bundle tiles. Match the muted grey land and soft green feel |
| the map placeholder image | a flat fill on the surface colour with a centred loader until tiles arrive |
| the loader animation | a vector spinner driven by the `spinner-spin` moment over white |
| the store badges | rebuild as vector badges with the standard store lockups and a gentle corner |
| the mascot and the star row | redraw from the smiley geometry above, and a five point star filled in the cautious mid, vivid amber |
| the human verification badge | reserve the space and mount whichever widget the deployment chooses; do not hardcode a vendor |

## Constraints

- One tenant. Every driver sees the same map, the same places, the same segments and
  the same reports; only planned drives, reminders and page view records are private to
  their owner.
- No mobile navigation client, no turn by turn guidance, no voice, no lane guidance, no
  offline regions and no in car experience.
- No telemetry ingestion from phones, no map matching, no machine learning traffic
  estimation, no map data platform and no map editor tool. Road conditions come only
  from reports filed in this app.
- No ads, no monetization, no advertising partner, no partner data exchange, no
  carpool matching, no chat, no social graph, no gamification and no leaderboard.
- No embedded map widget for another site and no companion surface for another device.
- No analytics measurement is wired, so nothing on any route reports a view to a third
  party. The record of what was viewed stays in this app's own table.
- No comments, no likes, no messaging, no file upload and no email delivery.
- No payments and no subscriptions.
- No external network calls at runtime. Tiles are generated or proxied by the app
  itself, and every font, icon and image is generated rather than fetched from a third
  party at run time.
- No binary from the original product is present anywhere in the build.
- Outbound destinations named in the navigation, the map editor, the forums, Wazeopedia,
  the academy, the partner hub and the help center, exist as labels and link
  affordances only. The pages behind them are out of scope.
- The app stays responsive with 5 road segments, 6 places, a few hundred reports and a
  few hundred planned drives.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173`, `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
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
  environment variables. Do not download, install, compile or start a copy of any of
  them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `display_name` | the new driver plus an `access_token` |
| `POST /api/auth/login` | `email`, `password` | the driver plus an `access_token` |
| `GET /api/health` | none | readiness |
| `GET /api/places` | `q` | a top-level JSON array of places, each with `id`, `name`, `latitude`, `longitude` |
| `GET /api/places/reverse` | `latitude`, `longitude` | the nearest place |
| `GET /api/segments` | none | a top-level JSON array of segments, each with `id`, `name`, `base_minutes`, `path`, `severity` |
| `GET /api/reports` | optional `segment_id` | a top-level JSON array of reports, each with `id`, `segment_id`, `type`, `status`, `latitude`, `longitude`, `created_at`, `expires_at` |
| `POST /api/reports` | `segment_id`, `type`, `latitude`, `longitude` | the created report |
| `POST /api/reports/{id}/votes` | `vote` | the updated report |
| `POST /api/routes` | `origin_place_id`, `destination_place_id`, and one of `depart_at` or `arrival_at` | `segments`, `travel_minutes`, `leave_at`, `arrival_at` |
| `POST /api/drives` | `origin_place_id`, `destination_place_id`, `arrival_at` | the planned drive with `leave_at`, `travel_minutes`, `reminder_at`, `status` |
| `GET /api/drives` | none | a top-level JSON array of the caller's own planned drives |
| `GET /api/drives/{id}` | none | one of the caller's own planned drives |
| `DELETE /api/drives/{id}` | none | the cancelled drive |
| `GET /api/reminders` | none | a top-level JSON array of the caller's own due reminders |
| `POST /api/page-views` | `route` | the recorded view |
| `GET /api/page-views` | none | a top-level JSON array of the caller's own recorded views |

A successful call returns the named resource or shape. An invalid or unauthorized call
is rejected as a client error, never as a server error and never as a silent success.
Bearer auth is required on everything except signup, login, health, the place index, the
segment list, the report list, a route calculation and recording a page view.

## Definition of done

A stranger can open the map, search a start and a destination, see the roads coloured by
what drivers have reported on them, pick an arrival time and be told when to set off. A
signed in driver can file a report and watch the segment recolour, and can save a planned
drive that carries a reminder. A driver never holds two planned drives whose departure
windows overlap, even when both are requested at the same instant. An unknown address
lands on the product's own not found page.
