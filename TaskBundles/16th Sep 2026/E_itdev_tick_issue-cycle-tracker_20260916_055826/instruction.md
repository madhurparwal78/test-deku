# Cadence

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, sign in as a lead, assign an unassigned inbox issue to a teammate, and have that teammate receive a real notification email, without hitting an error page. The notification is not a green tick the app shows itself: the email must actually arrive in the mail service named below, addressed to that one teammate, and the assignment must still be there after a reload. A different stranger signed in as an ordinary member must NOT be able to move an issue that belongs to someone else, by any means, including a direct API call.

## Overview

Cadence is an internal issue tracker for a single software team. Members file issues that each carry a priority, a label and a point estimate. Leads triage an unassigned inbox, hand each issue to an owner, and group work into time-boxed cycles. Work is shown as a board of named workflow states, and moving an issue from one state to the next is the action the whole product is arranged around. When an issue is handed to a member, or moved by someone other than its owner, that owner is notified by email. The product opens onto the cycle board as its main working surface.

The product is deliberately small. There is no public sign-up, no cross-team collaboration, no chat, no file attachments, no time tracking and no reporting dashboard. It serves one team at a time, and everything a person sees is scoped to their own team.

The genuinely hard part is authorization under a direct request: an ordinary member may change only the issues they own, and hiding a button is never the enforcement. The second hard part is that assigning an issue must both persist the new owner and deliver exactly one notification email to that owner, with neither happening without the other.

## User roles

Three roles, hierarchical. Signup is closed: every account is seeded, and there is no public registration form.

| Role | Can read | Can write | Cannot |
|---|---|---|---|
| `admin` | everything in its own team | everything below, plus team, member and label management | **cannot** read or write another team's data; **cannot** remove its own `admin` role |
| `lead` | the board, the inbox, every issue and cycle in its team | triage the inbox, assign owners, open and close cycles, move any issue in the team | **cannot** open the settings surface; **cannot** touch another team's data |
| `member` | the board, every issue and cycle in its team | file issues, comment, and move only issues where it is the assignee | **cannot** open the inbox; **cannot** move an issue it does not own; **cannot** touch another team's data |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `member` session to any `lead`-only or `admin`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. A request for an issue that belongs to another team is answered as not found rather than as forbidden, so the existence of other teams' work is never disclosed.

Seeded accounts, all in the team `Orbit`, every one using the password `deku-demo-pw-2026`:

- `admin@example.com` is the team `admin`.
- `lead@example.com` is a `lead`.
- `member@example.com` is a `member` and owns at least one seeded issue.
- `member2@example.com` is a second `member` and owns at least one seeded issue.

## Core features

### Auth

Accounts are email and password. Signing in is `POST /api/auth/login` with `{"email", "password"}`, which returns an `access_token`. The app hashes the password with a standard password hashing scheme; the plaintext is never stored. The client sends the returned bearer token on every later request; an expired or missing token on a protected route is rejected as unauthorized. There is no public sign-up and no password-reset flow. A refused sign-in does not reveal which of the email or the password was wrong.

### Filing an issue

1. Any signed-in member, lead or admin may file an issue with a title, an optional description, a priority from `none`, `low`, `med`, `high`, a single label, and an integer point estimate.
2. The server assigns the issue key: the team key, a hyphen, and a per-team counter, for example `ORB-1`, then `ORB-2`. A key is never reused, including after an issue is deleted.
3. A newly filed issue starts in the `backlog` state, with no assignee and no cycle, which places it in the inbox.
4. An issue filed with a blank title is rejected as invalid and no row is written.

### The inbox and triage

1. The inbox holds every issue in the team that has no assignee and no cycle.
2. Only a `lead` or an `admin` may read the inbox. A `member` that requests the inbox is denied.
3. A lead assigns an inbox issue to a member and, in the same action, may place it into the active cycle. Once an issue has an assignee it leaves the inbox.

### Assigning an issue notifies its owner

This is the rule the product is graded on hardest, and both halves must hold together.

1. When a `lead` or `admin` sets an issue's assignee to a member, the new assignee is stored and survives a reload, **and** exactly one notification email is delivered to that member's own address.
2. The email is addressed only to the assignee: no cc, no bcc, no other recipient. Its subject begins with `Assigned to you: ` followed by the issue key, a space, and the issue title, for example `Assigned to you: ORB-7 Fix login redirect loop`. Its body names the issue and the cycle it now belongs to.
3. When any issue that already has an assignee is moved to a new workflow state by someone who is **not** its assignee, one email is delivered to the assignee, with a subject that begins with `Issue updated: ` followed by the issue key and title.
4. No email is sent when: the actor is the assignee acting on their own issue; the issue has no assignee; the change touches only the priority, label, estimate, title or description; or an issue is unassigned. Filing an issue never sends an email.

### The cycle board and moving issues

1. The board shows the active cycle's issues arranged in five columns, one per workflow state, in the fixed order `backlog`, `unstarted`, `in_progress`, `done`, `cancelled`.
2. Moving an issue from one column to the next changes its state. A `member` may move only issues where it is the assignee; a `lead` or `admin` may move any issue in the team. A member's attempt to move an issue it does not own is denied and the issue's state is unchanged.
3. Every state change writes the new state and one activity record together, in one unit of work. If either the state write or the activity record cannot be written, neither is, and the issue keeps its previous state. An issue whose state changed with no matching activity record is the exact defect this rule exists to prevent.
4. The board reflects a move immediately for the person who made it; a move the server refuses is rolled back in the interface and the reason is shown.

### Cycles

1. A cycle has a name, a start date, an end date and a status from `planned`, `active`, `closed`. At most one cycle per team is `active` at any time.
2. Only a `lead` or `admin` may open a cycle (move it to `active`) or close one. A `member` that requests either is denied.
3. Closing a cycle sets it to `closed` and, in the same unit of work, returns every issue in it whose state is not `done` and not `cancelled` to the inbox by clearing that issue's cycle and leaving its assignee unchanged. The close response reports the exact count of issues it returned.
4. A `closed` cycle is read-only: its issues cannot be moved and no issue can be filed into it.

### Comments and activity

1. Any member, lead or admin in the team may comment on any issue in the team. A comment carries its author and the time it was written.
2. The issue view shows comments and state-change activity together in one thread, oldest first.

### Labels

1. An `admin` manages the team's labels. Each label has a name and a colour chosen from the product's fixed palette; a free-form colour is rejected as invalid.
2. Every issue carries exactly one label.

### Page-view log

1. Each page view is recorded with the route that was viewed and the time it was viewed.
2. Only an `admin` may read the page-view log, and it is scoped to the admin's own team. A `lead` or `member` that requests it is denied.

## User flow

### Routes

| Route | Purpose | Auth |
|---|---|---|
| `/login` | credential entry | public |
| `/board` | the active cycle, issues by workflow state | required |
| `/inbox` | untriaged issues | lead and admin only |
| `/issues/ORB-1` | one issue, its properties, comments and activity (`/issues/<key>`) | required |
| `/cycles` | cycle list, past and planned | required |
| `/cycles/1` | one cycle, read-only when closed (`/cycles/<id>`) | required |
| `/settings` | team, member and label management | admin only |

### Entry and redirects

- An unauthenticated visitor on any protected route is sent to `/login`.
- A successful sign-in lands on `/board`.
- Signing out returns to `/login` and invalidates the client's token for later requests.
- A token that expires mid-action causes the next request to be rejected as unauthorized, and the interface returns the visitor to `/login`.
- A `member` that opens `/inbox`, or an `admin`-only route while signed in as a lead, is returned to `/board`; the redirect is a courtesy and the underlying endpoint denies the request regardless.

### Journeys

1. **Triage and assign.** `lead@example.com` signs in, opens `/inbox`, picks an unassigned issue, assigns it to `member@example.com` and places it in the active cycle. The inbox row disappears, the issue appears on `/board`, and `member@example.com` receives one `Assigned to you: ` email.
2. **Move an owned issue.** `member@example.com` signs in, opens `/board`, and drags an issue it owns from `unstarted` to `in_progress`. The card settles in the new column, the change survives a reload, and an activity record is added to the issue.
3. **Denied move.** `member2@example.com` signs in and attempts, by a direct request, to move an issue owned by `member@example.com`. The request is denied and the issue's state is unchanged.
4. **Close a cycle.** `lead@example.com` opens `/cycles`, closes the active cycle, and is shown the exact count of unfinished issues returned to the inbox; those issues now appear in `/inbox` with no cycle.

### States

Every list has an empty state: an inbox with nothing to triage, a board column with no issues, a cycle list with no cycles. Every page has a loading state while its data is in flight. A failed panel replaces only that panel, with a way to retry, and never takes down the rest of the screen. A sign-in failure shows a message and clears the password field while keeping the email, and does not say which of the two was wrong. Access to the settings surface is limited to an admin, and every route beneath it refuses a lower role regardless of how it was reached.

## UI/UX notes

Cadence is a dark, operator-facing product for a team that lives in it all day, and its design is carried over from the reference product this brief was built against. The north star is comprehension at a glance: a person scanning a full board should read state, priority and ownership without stopping. The register is operational, so surfaces stay quiet and dense-but-organised, and calm is chosen over decoration everywhere the two compete. Motion is present but restrained, and every animation belongs to one of two speeds so the whole interface feels like one machine responding.

**Palette by role, stated in words, never as a colour code.** The exact shade is yours as long as each role reads as described and holds its meaning. The page ground and the panels that sit on it are all a near-black neutral, separated from each other by a hairline and a soft shadow rather than by a brightness jump, so surfaces feel layered without a hard step. Primary text is a near-white neutral; secondary labels and metadata step down to a mid cool neutral, and the very quietest hints to a light cool neutral, used only where the same information is also carried some other way. The single interactive accent, worn by the primary action and the focus ring and by nothing else on a page, is a light, soft blue. Destructive and overdue markers wear a light, vivid red, and that red appears nowhere else. In-review and blocked states carry a light cool neutral so the one thing in flight is distinguishable at a glance. No page is dominated by a single hue family with no second signal, and no workflow state is ever distinguished by colour alone.

**Type is exact, because a typeface is an identity rather than a value to echo.** The interface family is `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`; identifiers, keys and estimates use the monospace family `ui-monospace, "Cascadia Mono", Menlo, monospace` with tabular figures so numbers align wherever they stack. Body and issue titles are `16px`; secondary body is `15px`; metadata, counts and timestamps are `13px`; control labels are `14px`; the one page heading is `24px`, and the sign-in heading, the largest type in the product, is `32px`.

**Typography, shape, spacing and elevation.** Typography follows the two families above with a consistent set of sizes and weights, figures aligning wherever amounts stack. Shape uses one corner-radius scale, gentle on cards and panels and fully rounded on small status chips and avatars; hold to that radius scale rather than mixing arbitrary corners. Spacing follows a single regular rhythm built on one base unit, so gutters and padding read as one system. Elevation is carried by a soft shadow and a hairline rather than a brightness jump: a floating surface such as a menu or dialog sits in a pool of shadow, while a board card takes only a slight shadow.

**Iconography.** Every icon is drawn on one small square grid with a single consistent stroke weight, round caps and joins, inheriting the current text colour, so the whole set reads as one family; larger placements scale the same geometry and keep the stroke.

**Global chrome.** A slim top bar runs across the top carrying the current cycle name, a search control and the account avatar, and a fixed sidebar rail runs down the left holding team and cycle navigation; both stay put while the middle scrolls. The rail folds away behind a control at the medium breakpoint.

**Motion.** Motion character is eased: small confirmations such as a hover or a press land almost immediately, while larger rearrangements such as a card moving to another column ease in and settle rather than snapping. State a single transition family and reuse it; do not animate more than one thing at a time on the board. Every motion respects a reduced-motion preference, dropping the larger rearrangements while keeping the instant confirmations, because those carry information.

Density is comfortable: rows sit close enough that a full queue fits one screen without feeling cramped.

**Components and states.** Every interactive element has a resting, pointed-at, pressed, focused and unavailable state, and an unavailable control is never signalled by colour alone. Escape closes any open menu or dialog; a destructive action such as closing a cycle confirms first and states the count it will move. Icon-only controls carry text labels for assistive technology. Every glyph in the product, including each workflow-state icon and each priority indicator, is drawn as inline vector geometry rather than loaded from an image or icon font, so the set stays sharp at any size.

**The board card and its states.** Each card on the board shows the issue key, the title wrapping to at most three lines, its single label, its priority icon, and the assignee's avatar. Hovering a card only brightens its edge; picking it up is what makes it lift, so pointing at a card and holding it are never confused. Each workflow state carries its own distinct glyph as well as its colour, and each priority carries its own ascending-bar indicator, so state and priority are both readable without colour.

**Drag, and its feedback.** Dragging a card lifts it and it follows the pointer without lag; on drop it briefly flashes in its new column so you can see where it went. A refused drop returns the card to where it came from and shows the reason. There are two motion speeds only: a fast acknowledgement for the small confirmations such as a hover, a press or a row highlight, so interactive feedback lands almost immediately, and a slower, eased composition speed for the larger rearrangements such as a card settling into another column.

**Optimism and rollback.** A drag, an assignment and a property change take effect immediately in the interface and reconcile with the server afterwards. If the server refuses, the optimistic change is rolled back with the return motion and a short message explains why. Creating a new issue is the one exception: its card waits for the server to return its real key rather than showing a provisional one.

**Structure and announcements, for assistive technology.** Each route has exactly one top-level heading naming its subject, and the board and its columns are labelled regions so the structure is legible without sight. Moving an issue announces the issue and its new state, and a refused move announces the reason, so a screen-reader user follows the same events a sighted user sees.

**Pointer versus touch.** Hover treatments apply only where there is a real pointer; on a touch device the row actions that a pointer reveals on hover are always visible instead, because there is no hover to reveal them.

**Accessibility floors, which are contract and not taste.** Body text and its background meet WCAG AA contrast at a ratio of at least `4.5:1`, and this holds for the dark surface the product commits to. Every workflow state and every priority is distinguishable without colour, by a distinct glyph as well as its colour. The product is fully operable by keyboard, with a visible focus ring on every control and keyboard navigation across the board and its cards. Every content image carries alternative text.

**Responsive behaviour that holds at every width between the named tiers.** On a wide viewport the left rail is fixed and open and the board scrolls horizontally; at a medium breakpoint the rail folds away behind a control; on a narrow viewport the board shows one workflow state at a time with a switcher above it, so the finished work is never an enormous scroll below the unstarted work. At a narrow viewport nothing overflows sideways and every navigation target stays reachable. The layout is a fixed left sidebar for team and cycle navigation with the board or issue detail beside it; on the issue view the properties sit in a side panel that drops below the description on a narrow viewport.

## Technical requirements

The application is a server-rendered multi-page app: HTML is produced on the server with Flask and Jinja templates, and the browser receives complete pages on first paint, progressively enhanced in place with HTMX for partial updates such as moving a card or assigning an issue. The same server also exposes a JSON HTTP API on the same origin under the `/api` prefix, which is the contract the rest of this brief pins. Serve a production build behind a production server, never a development server. Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are `PostgreSQL` and `Mailpit`, and reaching for anything else is a contract violation.

Persist all application data in `PostgreSQL`, read from the `DATABASE_URL` environment variable. Send every notification over real SMTP through `Mailpit`, read from `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. These backing services are already running and reachable at those variables; do not download, install, compile or start a copy of either. Never hardcode a host or a port; read them from the environment. Authentication is app-implemented email and password with bearer tokens. `GET /api/health` returns `200` once the app is ready.

Cadence must stay correct when two people act at once. Every issue in a team gets a distinct key from the per-team counter: two members filing at the same moment each receive their own key, exactly one key is allocated per issue, and a number is never reused. Two requests that both try to make a cycle active in one team must not both succeed: exactly one wins and the other is rejected as a `409 Conflict`, so at most one cycle in a team is ever active. If the same create-issue request is submitted twice carrying the same client request id, the second returns the first issue and must not create a second issue: there is no second write and no second key. Guarantees like these must hold under real simultaneous requests, not only in application-level checks.

No credential, API key, bearer token or admin secret appears in anything the browser downloads: not in a page, a script, a template or an API response body meant for the client. Every HTTP response carries the standard security headers, including a strict transport policy and a content-type nosniff policy, so a response is never interpreted as a type it did not declare.

Log each request as a structured line so an operator can follow what happened; write logs to standard output.

## Data model

Nine entities. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

- **team** - id, name, key. The seeded team is `Orbit` with key `ORB`. A team's key prefixes every issue key in that team.
- **member** - id, team id, email, name, role in `admin`, `lead`, `member`, password hash. A member belongs to exactly one team.
- **cycle** - id, team id, name, starts on, ends on, status in `planned`, `active`, `closed`. At most one cycle per team is `active` at any time; this is an invariant of the stored data, true even when two requests race to open a cycle, not merely a check in the request handler.
- **label** - id, team id, name, colour. Colour is one of the product's fixed palette values; a value outside it is rejected.
- **issue** - id, team id, key, title, description, state in `backlog`, `unstarted`, `in_progress`, `done`, `cancelled`, priority in `none`, `low`, `med`, `high`, estimate as an integer, assignee (a member or none), cycle (a cycle or none), created at, updated at. The key is unique within the team and never reused. An issue with no assignee and no cycle is in the inbox.
- **issue_label** - issue id, label id. Each issue carries exactly one label.
- **comment** - id, issue id, author id, body, created at.
- **activity** - id, issue id, actor id, field, from value, to value, created at. A state change writes the issue and its activity record as one unit of work; neither exists without the other.
- **page_view** - id, team id, member id, route, viewed at. Readable only by an admin of the same team.

Derived rather than stored: whether an issue is in the inbox (it has no assignee and no cycle); the count of issues a cycle close returns (computed as it runs).

**Seed data.** One team `Orbit` (key `ORB`) with four members: `admin@example.com`, `lead@example.com`, `member@example.com`, `member2@example.com`. Three labels: `bug`, `feature`, `chore`. Two cycles: `Cycle 24` is `active` and `Cycle 23` is `closed`. At least one issue is assigned to `member@example.com` and at least one to `member2@example.com`, each sitting in the active cycle with a distinctive title such as `Fix login redirect loop` and `Add dark mode toggle`. The active cycle also holds at least two issues that are neither `done` nor `cancelled`, so closing it returns a known count to the inbox. At least three issues have no assignee and no cycle and so sit in the inbox. The closed cycle `Cycle 23` holds at least one issue, so its read-only rule is observable. A second team owns one issue with the key `OTR-1` that no `Orbit` account may read. Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One team per signed-in person; nothing crosses team boundaries, and another team's data is answered as not found.
- No public sign-up, no password reset, no external identity provider.
- No comments threading, no reactions, no chat, no file attachments, no time tracking, no reporting dashboard, no export.
- No external network calls at runtime beyond the named backing services; no third-party mail vendor and no analytics endpoint.
- No native application; the product is a web app only.
- No font file, image file or video file is served; all icons are drawn as inline vector geometry in the markup, and avatars are rendered as initials on a coloured disc rather than fetched as images.
- Performance: the board must stay responsive, with no dropped frames while a card is dragged, when a cycle holds a few hundred issues.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | email, password | an `access_token` and the signed-in member |
| `POST /api/auth/logout` | (bearer) | the session is ended |
| `GET /api/board` | (bearer) | the active cycle and its issues grouped by state |
| `GET /api/inbox` | (bearer, lead or admin) | a top-level array of unassigned, uncycled issues |
| `POST /api/issues` | title, priority, label, estimate, optional description, optional client request id | the created issue with its key |
| `PATCH /api/issues/<key>` | any of state, assignee, priority, label, estimate | the updated issue |
| `POST /api/issues/<key>/comments` | body | the created comment |
| `GET /api/cycles` | (bearer) | a top-level array of cycles |
| `POST /api/cycles` | name, starts on, ends on | the created cycle |
| `POST /api/cycles/<id>/open` | (bearer, lead or admin) | the cycle, now active |
| `POST /api/cycles/<id>/close` | (bearer, lead or admin) | the cycle, now closed, and the count of issues returned to the inbox |
| `GET /api/members` | (bearer, admin) | a top-level array of the team's members |
| `PATCH /api/members/<id>` | role | the updated member |
| `POST /api/labels` | name, colour | the created label |
| `GET /api/page-views` | (bearer, admin) | a top-level array of the team's page views |

Every list endpoint returns a top-level JSON array. A successful call returns the named resource; an invalid or unauthorized call is rejected as a client error, never as a server error and never as a silent success; the agent chooses conventional status codes and the graders accept the class. Bearer auth is required on everything except `POST /api/auth/login` and `GET /api/health`.

**No mocks.** The notification email must exist as a real message in `Mailpit`, addressed to the one assignee; an in-memory list of "sent" emails, or a `{"sent": true}` the app returns to itself, does not count. Application data must live in `PostgreSQL`; an in-memory array of issues or cycles does not count. The named provider is the fact: the app's UI and its own tables can only reflect what lives in the provider, never substitute for it.

## Definition of done

A stranger can sign in, and a lead can hand an inbox issue to a teammate who then receives one real notification email while the new owner sticks after a reload. An ordinary member can move the issues they own across the board and is refused, by the server, on any issue they do not own or in any other team. Closing a cycle sends its unfinished work back to the inbox and reports how many issues moved, and at most one cycle in a team is ever active. The app is deployed, healthy, and reachable in a browser with every list showing an empty, loading and populated state.
