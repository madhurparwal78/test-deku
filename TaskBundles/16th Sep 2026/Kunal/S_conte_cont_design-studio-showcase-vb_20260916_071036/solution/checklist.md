# Checklist: deku/design-studio-showcase-vb

Items: 356
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The product is the public site of a digital agency named Sable. `src: Overview`
- [ ] `C-OV-02` `capability` A prospective client can judge the studio within two screens of the home route. `src: Overview`
- [ ] `C-OV-03` `capability` A procurement lead obtains a capabilities deck without waiting for an email. `src: Overview`
- [ ] `C-OV-04` `capability` An existing client reaches the engagement portal, no other authenticated surface. `src: Overview`
- [ ] `C-OV-05` `capability` Submitting a staged project brief is the one action that changes stored state. `src: Overview`
- [ ] `C-OV-06` `capability` Six commissioned surfaces extend the measured site. `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` Two roles exist, `studio` plus `client`. `src: User roles`
- [ ] `C-RL-02` `role` A `studio` account publishes a case. `src: User roles`
- [ ] `C-RL-03` `role` A `studio` account unpublishes a case. `src: User roles`
- [ ] `C-RL-04` `role` A `studio` account reads every submitted brief. `src: User roles`
- [ ] `C-RL-05` `role` A `studio` account manages engagements, milestones, deliverables, versions. `src: User roles`
- [ ] `C-RL-06` `role` A `studio` account reads deck read-telemetry. `src: User roles`
- [ ] `C-RL-07` `role` A `studio` account cannot approve a deliverable for a client. `src: User roles`
- [ ] `C-RL-08` `role` A `client` account reads only engagements the account is attached to. `src: User roles`
- [ ] `C-RL-09` `role` A `client` account comments on a version. `src: User roles`
- [ ] `C-RL-10` `role` A `client` account approves only when carrying the approval right. `src: User roles`
- [ ] `C-RL-11` `role` A `client` account cannot read an unpublished case. `src: User roles`
- [ ] `C-RL-12` `role` A `client` account cannot read another visitor's brief. `src: User roles`
- [ ] `C-RL-13` `role` A `client` account cannot publish anything. `src: User roles`
- [ ] `C-RL-14` `role` The portal registers `viewer`, `approver`, `owner` are an approval right. `src: User roles`
- [ ] `C-RL-15` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles`
- [ ] `C-RL-16` `contract` A direct call from a `client` session to a `studio` endpoint is denied. `src: User roles`
- [ ] `C-RL-17` `contract` A denied call leaves the protected state unchanged. `src: User roles`
- [ ] `C-RL-18` `capability` Signup is open, a new account attached to no engagement. `src: User roles`
- [ ] `C-RL-19` `literal` Three accounts are seeded: `studio@example.com`, `client@example.com`, `client2@example.com`. `src: User roles`
- [ ] `C-RL-20` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Accounts are email plus password, held by the application. `src: Core features`
- [ ] `C-CF-02` `contract` A successful sign in returns a bearer token. `src: Core features`
- [ ] `C-CF-03` `contract` Passwords are stored hashed. `src: Core features`
- [ ] `C-CF-04` `capability` A portal sign-in link is single use, expiring fifteen minutes after issue. `src: Core features`
- [ ] `C-CF-05` `contract` A portal request carrying no bearer token is denied. `src: Core features`
- [ ] `C-CF-06` `contract` A denied portal response body carries no engagement data. `src: Core features`
- [ ] `C-CF-07` `capability` Signing out clears the session, offering to clear every device. `src: Core features`
- [ ] `C-CF-08` `contract` Uploaded bytes live in the MinIO bucket, nowhere else. `src: Core features`
- [ ] `C-CF-09` `contract` No uploaded byte is written to the application container filesystem. `src: Core features`
- [ ] `C-CF-10` `contract` No uploaded byte is stored in a database column. `src: Core features`
- [ ] `C-CF-11` `literal` A brief attachment key follows `briefs/{brief_token}/{sha256_of_bytes}.{ext}`. `src: Core features`
- [ ] `C-CF-12` `literal` A deliverable key follows `deliverables/{engagement_id}/{version_id}/{sha256_of_bytes}.{ext}`. `src: Core features`
- [ ] `C-CF-13` `contract` A protected object is reached through an authenticated streaming endpoint. `src: Core features`
- [ ] `C-CF-14` `contract` An unscanned upload is readable by nobody, the studio included. `src: Core features`
- [ ] `C-CF-15` `contract` A brief attachment request carrying a different token is denied. `src: Core features`
- [ ] `C-CF-16` `capability` The home route runs nine bands in a fixed order. `src: Core features`
- [ ] `C-CF-17` `capability` Following `Projects` from the contact route navigates home, settling at the projects band. `src: Core features`
- [ ] `C-CF-18` `ui` `Contact` renders struck through on the contact route. `src: Core features`
- [ ] `C-CF-19` `capability` A route change swaps the main region without reloading the document. `src: Core features`
- [ ] `C-CF-20` `contract` Every scroll-linked binding is destroyed before the next route initialises. `src: Core features`
- [ ] `C-CF-21` `capability` After twenty navigations the home route scrolls as on first load. `src: Core features`
- [ ] `C-CF-22` `capability` Browser history restores scroll position without replaying the loader. `src: Core features`
- [ ] `C-CF-23` `ui` The loader covers the viewport with a dark field carrying one light bar. `src: Core features`
- [ ] `C-CF-24` `literal` The loader label reads `LOADING...` in upper case. `src: Core features`
- [ ] `C-CF-25` `capability` The loader bar grows from nothing to the full frame width. `src: Core features`
- [ ] `C-CF-26` `ui` The loader label rises at a constant rate, never eased. `src: Core features`
- [ ] `C-CF-27` `capability` The loader runs on a first document load alone. `src: Core features`
- [ ] `C-CF-28` `capability` The loader element is removed from the document, never merely hidden. `src: Core features`
- [ ] `C-CF-29` `constraint` The slow-load simulation switch is disabled in the built output. `src: Core features`
- [ ] `C-CF-30` `data` Twenty service names render in four columns of five. `src: Core features`
- [ ] `C-CF-31` `literal` The service index heading pairs `WE DO` with `What`. `src: Core features`
- [ ] `C-CF-32` `literal` Four tone words fade in sequence: `Vision.`, `Clarity.`, `Flow.`, `Execution.` `src: Core features`
- [ ] `C-CF-33` `capability` Every dot in the field carries a home position never drawn on screen. `src: Core features`
- [ ] `C-CF-34` `capability` Scroll displaces a dot per dot, after which the dot returns towards home. `src: Core features`
- [ ] `C-CF-35` `capability` Reversing the scroll runs every driven property backwards with the input. `src: Core features`
- [ ] `C-CF-36` `data` Four numbered capabilities render on the dark ground. `src: Core features`
- [ ] `C-CF-37` `capability` The capability band holds still as the four items advance. `src: Core features`
- [ ] `C-CF-38` `capability` The capability band does not pin on a phone. `src: Core features`
- [ ] `C-CF-39` `data` Thirteen cases render in a staggered three-column arrangement. `src: Core features`
- [ ] `C-CF-40` `literal` The archive heading reads `Selected Cases`. `src: Core features`
- [ ] `C-CF-41` `capability` Case media is wiped in from a corner, never faded in. `src: Core features`
- [ ] `C-CF-42` `constraint` The wipe corner alternates so two adjacent cases never share one. `src: Core features`
- [ ] `C-CF-43` `data` The wipe corner is derived from archive position, never stored. `src: Core features`
- [ ] `C-CF-44` `ui` A case name rises into place beneath the panel as the panel wipes in. `src: Core features`
- [ ] `C-CF-45` `ui` On a phone a case panel fades rather than wiping. `src: Core features`
- [ ] `C-CF-46` `capability` Selecting a case in the home archive opens an overlay, no navigation. `src: Core features`
- [ ] `C-CF-47` `data` Twenty-four discipline tags are normalised to upper case. `src: Core features`
- [ ] `C-CF-48` `capability` An open case overlay traps focus inside itself. `src: Core features`
- [ ] `C-CF-49` `capability` Closing the case overlay returns focus to the case that opened the overlay. `src: Core features`
- [ ] `C-CF-50` `capability` The escape key closes the case overlay. `src: Core features`
- [ ] `C-CF-51` `capability` Every case is addressable at a full route of its own. `src: Core features`
- [ ] `C-CF-52` `data` A case slug is the lower-case hyphenated case name, stable, never reused. `src: Core features`
- [ ] `C-CF-53` `capability` A renamed case keeps the original slug, gaining a redirect. `src: Core features`
- [ ] `C-CF-54` `data` Ten chapter types exist, the renderer choosing layout from the type. `src: Core features`
- [ ] `C-CF-55` `constraint` A case opens with a `cover` chapter, closing with an `outcome` chapter. `src: Core features`
- [ ] `C-CF-56` `contract` A case carrying fewer than four chapters is refused publication as invalid. `src: Core features`
- [ ] `C-CF-57` `ui` A chapter rail marks the current chapter with an accent dot paired with text. `src: Core features`
- [ ] `C-CF-58` `ui` The comparison chapter shows both labels plus half of each image at rest. `src: Core features`
- [ ] `C-CF-59` `capability` Arrow keys move the comparison divider, home plus end jumping to the extremes. `src: Core features`
- [ ] `C-CF-60` `capability` A pinned sequence chapter advances a horizontal track from vertical scroll. `src: Core features`
- [ ] `C-CF-61` `capability` Under reduced motion the sequence pin releases into a scrollable region. `src: Core features`
- [ ] `C-CF-62` `contract` An unpublished case is not readable at the case route by anyone but `studio`. `src: Core features`
- [ ] `C-CF-63` `literal` The archive heading reads `The Archive`. `src: Core features`
- [ ] `C-CF-64` `data` Three facets narrow the archive: sector, discipline, kind. `src: Core features`
- [ ] `C-CF-65` `capability` Every facet value shows a live count. `src: Core features`
- [ ] `C-CF-66` `ui` A facet value whose count is zero is disabled, never hidden. `src: Core features`
- [ ] `C-CF-67` `capability` The active filter is carried in the address, reopening elsewhere. `src: Core features`
- [ ] `C-CF-68` `literal` An empty archive result names the nearest non-empty filter. `src: Core features`
- [ ] `C-CF-69` `capability` Up to three cases are held in a comparison tray. `src: Core features`
- [ ] `C-CF-70` `literal` A measure a case does not publish reads `not published`. `src: Core features`
- [ ] `C-CF-71` `data` Similarity orders by discipline overlap, then sector, then recency. `src: Core features`
- [ ] `C-CF-72` `capability` A similarity suggestion states the shared disciplines in one line. `src: Core features`
- [ ] `C-CF-73` `capability` One search field filters the archive in place, never navigating away. `src: Core features`
- [ ] `C-CF-74` `constraint` Changing a filter does not replay the corner wipe on cases already on screen. `src: Core features`
- [ ] `C-CF-75` `ui` The contact route is one screen tall, never scrolling. `src: Core features`
- [ ] `C-CF-76` `ui` The contact form is six panels with one full-bleed submit bar. `src: Core features`
- [ ] `C-CF-77` `capability` Every form rejects invalid input inline, naming the field. `src: Core features`
- [ ] `C-CF-78` `contract` A rejected form writes nothing. `src: Core features`
- [ ] `C-CF-79` `capability` The verification guard degrades to a usable state when unreachable. `src: Core features`
- [ ] `C-CF-80` `capability` Spam protection refuses a form carrying a filled decoy field. `src: Core features`
- [ ] `C-CF-81` `data` Five form failures are distinguished by their own messages. `src: Core features`
- [ ] `C-CF-82` `contract` An attachment above two megabytes is refused alone, the limit stated. `src: Core features`
- [ ] `C-CF-83` `capability` A success block replaces the form, announced with focus moved inside. `src: Core features`
- [ ] `C-CF-84` `literal` The deck control reads `GET CAPABILITIES DECK`. `src: Core features`
- [ ] `C-CF-85` `constraint` The published email address is absent as plain text from the served document. `src: Core features`
- [ ] `C-CF-86` `constraint` The short contact form is never removed in favour of the staged brief. `src: Core features`
- [ ] `C-CF-87` `capability` The staged brief runs six independently addressable stages. `src: Core features`
- [ ] `C-CF-88` `capability` Brief stage three proposes a shape derived from the discipline selection. `src: Core features`
- [ ] `C-CF-89` `capability` Brief stage three states the reason, offering an override. `src: Core features`
- [ ] `C-CF-90` `data` Four engagement shapes exist: `identity`, `product`, `build`, `full-cycle`. `src: Core features`
- [ ] `C-CF-91` `data` Budget is a band, never a free number. `src: Core features`
- [ ] `C-CF-92` `constraint` The undecided budget band is a first-class answer, never styled as lesser. `src: Core features`
- [ ] `C-CF-93` `capability` The brief record is saved after every completed stage. `src: Core features`
- [ ] `C-CF-94` `capability` The first save issues an opaque unguessable resume token. `src: Core features`
- [ ] `C-CF-95` `constraint` A resume link is not indexable, expiring thirty days from the last edit. `src: Core features`
- [ ] `C-CF-96` `constraint` A resume link never carries the visitor email address in the path. `src: Core features`
- [ ] `C-CF-97` `capability` A resumed brief returns every answer at the furthest stage reached. `src: Core features`
- [ ] `C-CF-98` `constraint` No failure at any stage returns the visitor to stage one. `src: Core features`
- [ ] `C-CF-99` `capability` An oversized attachment is refused alone, the brief intact. `src: Core features`
- [ ] `C-CF-100` `literal` The booking confirmation names the time in both zones. `src: Core features`
- [ ] `C-CF-101` `data` Slots come from a published availability document, never a live calendar. `src: Core features`
- [ ] `C-CF-102` `data` A slot is thirty minutes, the horizon fourteen days forward. `src: Core features`
- [ ] `C-CF-103` `capability` The visitor time zone is named before any slot is drawn. `src: Core features`
- [ ] `C-CF-104` `capability` The visitor time zone is overridable before any slot is drawn. `src: Core features`
- [ ] `C-CF-105` `capability` Selecting a slot places a soft hold released after fifteen minutes. `src: Core features`
- [ ] `C-CF-106` `constraint` A second visitor is refused at submission, never at selection. `src: Core features`
- [ ] `C-CF-107` `contract` Exactly one of two simultaneous submissions for one slot is booked. `src: Core features`
- [ ] `C-CF-108` `contract` The losing submission is rejected, the two nearest free slots offered. `src: Core features`
- [ ] `C-CF-109` `constraint` A refused submission loses neither the narrative nor the attachment. `src: Core features`
- [ ] `C-CF-110` `capability` The slot picker is fully operable by keyboard. `src: Core features`
- [ ] `C-CF-111` `ui` The tone board is a square field carrying two labelled axes. `src: Core features`
- [ ] `C-CF-112` `literal` The tone axes run `restrained` to `expressive`, `classical` to `contemporary`. `src: Core features`
- [ ] `C-CF-113` `data` Thirty word tiles sit in a tray beneath the tone board. `src: Core features`
- [ ] `C-CF-114` `ui` A released tile carries inertia, settling just past the drop point. `src: Core features`
- [ ] `C-CF-115` `constraint` Eight tiles is the board limit, a ninth prompting a swap. `src: Core features`
- [ ] `C-CF-116` `capability` A picked tile is moved by arrow keys, dropped by the enter key. `src: Core features`
- [ ] `C-CF-117` `data` The tone signature carries two axis values plus the chosen words. `src: Core features`
- [ ] `C-CF-118` `constraint` Skipping the tone board never presents the brief as incomplete. `src: Core features`
- [ ] `C-CF-119` `contract` The list view produces an output identical to the board. `src: Core features`
- [ ] `C-CF-120` `capability` A tile position is announced as two named regions, never as coordinates. `src: Core features`
- [ ] `C-CF-121` `capability` The composer asks three questions on one screen, no stages. `src: Core features`
- [ ] `C-CF-122` `data` Detail options `Overview`, `Standard`, `Deep` set roughly six, twelve, twenty pages. `src: Core features`
- [ ] `C-CF-123` `data` A deck is assembled from typed blocks, never a template per permutation. `src: Core features`
- [ ] `C-CF-124` `data` Case blocks are selected by sector, then shape, then recency. `src: Core features`
- [ ] `C-CF-125` `capability` The closing deck block links into the brief carrying the composer answers. `src: Core features`
- [ ] `C-CF-126` `capability` A composed deck is a read-only paginated route. `src: Core features`
- [ ] `C-CF-127` `constraint` No downloadable deck file exists. `src: Core features`
- [ ] `C-CF-128` `constraint` A deck token is opaque, unguessable, not indexable, living ninety days. `src: Core features`
- [ ] `C-CF-129` `capability` Printing a deck produces one deck page per sheet with no cropped media. `src: Core features`
- [ ] `C-CF-130` `data` Deck telemetry records first open, furthest page, pages viewed, per-case seconds. `src: Core features`
- [ ] `C-CF-131` `constraint` Deck telemetry identifies no forwarded reader, recording no location beyond a zone. `src: Core features`
- [ ] `C-CF-132` `literal` Every deck first page carries the telemetry notice. `src: Core features`
- [ ] `C-CF-133` `contract` An expired deck token produces a response identical to a revoked one. `src: Core features`
- [ ] `C-CF-134` `constraint` The portal is the only authenticated surface, unlinked from the header. `src: Core features`
- [ ] `C-CF-135` `data` The portal shows six panels. `src: Core features`
- [ ] `C-CF-136` `literal` The first portal panel is `Right now`, one line. `src: Core features`
- [ ] `C-CF-137` `literal` The actionable portal panel is `Waiting on you`. `src: Core features`
- [ ] `C-CF-138` `contract` Every portal record is scoped to one engagement. `src: Core features`
- [ ] `C-CF-139` `contract` No portal query is satisfiable without an attached engagement identifier. `src: Core features`
- [ ] `C-CF-140` `contract` Portal access control is enforced where the data lives. `src: Core features`
- [ ] `C-CF-141` `contract` A cross-engagement request is denied, the response carrying no part of the record. `src: Core features`
- [ ] `C-CF-142` `ui` A version preview renders in the browser, never download-only. `src: Core features`
- [ ] `C-CF-143` `capability` Comments are threaded per version, resolvable, pinnable to a point. `src: Core features`
- [ ] `C-CF-144` `literal` The two decisions are `Approve` plus `Request changes`. `src: Core features`
- [ ] `C-CF-145` `contract` A rejection without a note is refused, recording nothing. `src: Core features`
- [ ] `C-CF-146` `contract` Only an account carrying the approval right may approve. `src: Core features`
- [ ] `C-CF-147` `contract` A denied approve request leaves the version state unchanged. `src: Core features`
- [ ] `C-CF-148` `contract` An approved version is frozen, a change creating a new version. `src: Core features`
- [ ] `C-CF-149` `contract` Every approval records actor plus time, appended, never deleted. `src: Core features`
- [ ] `C-CF-150` `literal` Digest settings are `Daily`, `Weekly`, `Off`, defaulting to `Daily`. `src: Core features`
- [ ] `C-CF-151` `constraint` Nothing in the portal is pinned, nothing driven by scroll. `src: Core features`
- [ ] `C-CF-152` `constraint` A second factor is required for any account carrying approval rights. `src: Core features`
- [ ] `C-CF-153` `capability` A privacy page is reachable from the footer of every page. `src: Core features`
- [ ] `C-CF-154` `data` The privacy page carries an effective date plus eight numbered sections. `src: Core features`
- [ ] `C-CF-155` `data` The privacy collection list names seven collected things. `src: Core features`
- [ ] `C-CF-156` `constraint` The privacy page names every collection point the newer surfaces introduce. `src: Core features`
- [ ] `C-CF-157` `capability` A terms page is reachable from the footer, linked from the signup form. `src: Core features`
- [ ] `C-CF-158` `capability` A first-time visitor is asked once about non-essential cookies. `src: Core features`
- [ ] `C-CF-159` `capability` A cookie answer survives a reload. `src: Core features`
- [ ] `C-CF-160` `capability` An unknown address renders the studio not-found page with a way back. `src: Core features`
- [ ] `C-CF-161` `contract` An unknown address answers not-found. `src: Core features`
- [ ] `C-CF-162` `data` Each page view is recorded with route plus timestamp, readable by `studio` alone. `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `literal` The home route is `/`. `src: User flow`
- [ ] `C-UF-02` `literal` The enquiry route is `/contact/`. `src: User flow`
- [ ] `C-UF-03` `literal` The privacy route is `/privacy-policy/`. `src: User flow`
- [ ] `C-UF-04` `literal` The terms route is `/terms/`. `src: User flow`
- [ ] `C-UF-05` `literal` The archive route is `/work/`. `src: User flow`
- [ ] `C-UF-06` `literal` The staged brief route is `/brief/`. `src: User flow`
- [ ] `C-UF-07` `literal` The deck composer route is `/deck/`. `src: User flow`
- [ ] `C-UF-08` `literal` The portal route is `/portal/`. `src: User flow`
- [ ] `C-UF-09` `literal` The sign-in route is `/login`. `src: User flow`
- [ ] `C-UF-10` `literal` The account creation route is `/signup`. `src: User flow`
- [ ] `C-UF-11` `contract` Trailing slashes are significant, `/contact` permanently redirecting. `src: User flow`
- [ ] `C-UF-12` `capability` An unauthenticated portal request lands on the sign-in route. `src: User flow`
- [ ] `C-UF-13` `capability` A successful sign in continues to the portal, never the home route. `src: User flow`
- [ ] `C-UF-14` `contract` An expired token mid-action leaves the record untouched. `src: User flow`
- [ ] `C-UF-15` `capability` An expired brief token offers a control starting again. `src: User flow`
- [ ] `C-UF-16` `capability` A renamed case old slug permanently redirects to the current slug. `src: User flow`
- [ ] `C-UF-17` `capability` Every list carries an empty state naming what would fill the list. `src: User flow`
- [ ] `C-UF-18` `capability` Every route carries a loading state. `src: User flow`
- [ ] `C-UF-19` `constraint` No error leaves a blank page. `src: User flow`
- [ ] `C-UF-20` `capability` A revealing element releases content after a deadline regardless. `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The register is editorial on public routes, operational inside the portal. `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Exactly two grounds exist, cutting at a full-bleed edge rather than blending. `src: UI/UX notes`
- [ ] `C-UX-03` `ui` The dark ground is a near-black neutral, the light ground a near-white neutral. `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Text is pure on both grounds, no softened near-black, no off-white. `src: UI/UX notes`
- [ ] `C-UX-05` `ui` One accent exists, a mid vivid teal. `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` The accent is never a fill, never a button, never a heading colour. `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Form errors carry the only light muted red on the site. `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Four type voices carry four jobs. `src: UI/UX notes`
- [ ] `C-UX-09` `ui` Display line boxes sit below the font size. `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Every major heading pairs a roman span with an italic span. `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Controls are stadiums, panels softly rounded, tags barely rounded. `src: UI/UX notes`
- [ ] `C-UX-12` `constraint` No drop shadow exists anywhere. `src: UI/UX notes`
- [ ] `C-UX-13` `ui` The motion character is eased, everything arriving late then settling. `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The fixed chrome renders as the inverse of whatever passes beneath. `src: UI/UX notes`
- [ ] `C-UX-15` `constraint` The chrome never swaps colour at a ground boundary. `src: UI/UX notes`
- [ ] `C-UX-16` `capability` Reduced motion resolves every reveal to the end state. `src: UI/UX notes`
- [ ] `C-UX-17` `constraint` Reduced motion leaves the site recognisably itself. `src: UI/UX notes`
- [ ] `C-UX-18` `capability` Every overlay traps focus, returning focus on close. `src: UI/UX notes`
- [ ] `C-UX-19` `constraint` Text meets WCAG AA contrast on both grounds. `src: UI/UX notes`
- [ ] `C-UX-20` `constraint` Every control carries a comfortably sized touch target. `src: UI/UX notes`
- [ ] `C-UX-21` `constraint` Keyboard navigation reaches everything with a visible focus ring. `src: UI/UX notes`
- [ ] `C-UX-22` `constraint` The focus ring survives the inverting chrome. `src: UI/UX notes`
- [ ] `C-UX-23` `constraint` Focus order follows reading order at every width. `src: UI/UX notes`
- [ ] `C-UX-24` `constraint` Meaning is never carried by the accent alone. `src: UI/UX notes`
- [ ] `C-UX-25` `capability` The type scale grows from the reader root size preference. `src: UI/UX notes`
- [ ] `C-UX-26` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Each page leads with one primary action, distinct from every secondary one. `src: UI/UX notes`
- [ ] `C-UX-28` `constraint` Every content image carries alternative text. `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The rendering model is server-rendered HTML with hydrated islands. `src: Technical requirements`
- [ ] `C-TR-02` `contract` The front end is built with SvelteKit. `src: Technical requirements`
- [ ] `C-TR-03` `contract` The HTTP API is built with Express. `src: Technical requirements`
- [ ] `C-TR-04` `contract` Persistence is PostgreSQL. `src: Technical requirements`
- [ ] `C-TR-05` `contract` Object storage is MinIO. `src: Technical requirements`
- [ ] `C-TR-06` `literal` The database is reached at `DATABASE_URL`. `src: Technical requirements`
- [ ] `C-TR-07` `literal` The object store is reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`. `src: Technical requirements`
- [ ] `C-TR-08` `literal` Store credentials are read from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements`
- [ ] `C-TR-09` `literal` The public address is read from `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. `src: Technical requirements`
- [ ] `C-TR-10` `constraint` No host is hardcoded, no port is hardcoded. `src: Technical requirements`
- [ ] `C-TR-11` `constraint` Backing services are already running, never installed by the application. `src: Technical requirements`
- [ ] `C-TR-12` `constraint` No second database, cache, queue, object store, identity provider is introduced. `src: Technical requirements`
- [ ] `C-TR-13` `contract` `GET /api/health` returns `200` once ready. `src: Technical requirements`
- [ ] `C-TR-14` `contract` Request logs go to standard output, one line per request. `src: Technical requirements`
- [ ] `C-TR-15` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements`
- [ ] `C-TR-16` `capability` Every public route carries a title of its own. `src: Technical requirements`
- [ ] `C-TR-17` `capability` Every public route carries a description of its own. `src: Technical requirements`
- [ ] `C-TR-18` `constraint` No two public routes share a title. `src: Technical requirements`
- [ ] `C-TR-19` `capability` A case route declares a social preview image plus an article record. `src: Technical requirements`
- [ ] `C-TR-20` `capability` Video begins loading two viewport heights out, playing one viewport height out. `src: Technical requirements`
- [ ] `C-TR-21` `constraint` Under reduced motion no video loads, the generated poster standing. `src: Technical requirements`
- [ ] `C-TR-22` `constraint` The portal loads nothing that binds to scroll. `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are UTC. `src: Data model`
- [ ] `C-DM-02` `contract` The seeded password literal works at login. `src: Data model`
- [ ] `C-DM-03` `contract` The seeded password is written into `/app/USER_README.md` beside each account. `src: Data model`
- [ ] `C-DM-04` `data` An `account` row carries email, password hash, display name, role. `src: Data model`
- [ ] `C-DM-05` `data` A `session` row expires thirty days from issue. `src: Data model`
- [ ] `C-DM-06` `data` A `signin_link` row expires fifteen minutes from issue, single use. `src: Data model`
- [ ] `C-DM-07` `data` A `case` row carries slug, name, sector, kind, year, positioning line. `src: Data model`
- [ ] `C-DM-08` `data` A case sector is one of five values, a case kind one of three. `src: Data model`
- [ ] `C-DM-09` `data` A `case_chapter` row carries case reference, ordinal, type, body, media key. `src: Data model`
- [ ] `C-DM-10` `data` A `brief` row carries a unique opaque token. `src: Data model`
- [ ] `C-DM-11` `constraint` A brief token is never derived from an email address. `src: Data model`
- [ ] `C-DM-12` `data` A brief row records whether the derived shape was overridden. `src: Data model`
- [ ] `C-DM-13` `data` A `brief_tone_word` row carries a keyword with two coordinates. `src: Data model`
- [ ] `C-DM-14` `data` An `attachment` row carries object key, byte size, content type, scanned. `src: Data model`
- [ ] `C-DM-15` `data` An `availability_slot` row state is `free`, `held`, `booked`. `src: Data model`
- [ ] `C-DM-16` `contract` A slot reaches the `booked` state at most once. `src: Data model`
- [ ] `C-DM-17` `data` A `booking` row carries the studio zone rendering plus the visitor zone rendering. `src: Data model`
- [ ] `C-DM-18` `data` A `deck` row carries a unique opaque token expiring ninety days out. `src: Data model`
- [ ] `C-DM-19` `data` A `deck_read` row carries no reader identity. `src: Data model`
- [ ] `C-DM-20` `data` An `engagement_account` row carries engagement, account, approval right. `src: Data model`
- [ ] `C-DM-21` `contract` Every portal read resolves through the engagement account join. `src: Data model`
- [ ] `C-DM-22` `data` A `version` row carries deliverable, number, date, preview key, frozen. `src: Data model`
- [ ] `C-DM-23` `data` An `approval` row carries version, account, decision, note, timestamp. `src: Data model`
- [ ] `C-DM-24` `data` Facet counts, similarity ordering, deck page count are derived, never stored. `src: Data model`
- [ ] `C-DM-25` `data` Three accounts are seeded, `client@example.com` carrying the approval right. `src: Data model`
- [ ] `C-DM-26` `data` Thirteen cases are seeded with sectors. `src: Data model`
- [ ] `C-DM-27` `literal` `Token Market` is seeded unpublished. `src: Data model`
- [ ] `C-DM-28` `data` Exactly one free slot remains on the first availability day. `src: Data model`
- [ ] `C-DM-29` `data` Two engagements are seeded, each with one deliverable at two versions. `src: Data model`
- [ ] `C-DM-30` `contract` Seeding is idempotent, restarting the application duplicating no row. `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The frame is gutter, content column, gutter. `src: Front-end specification`
- [ ] `C-FE-02` `ui` The header is a fixed band across the full viewport width. `src: Front-end specification`
- [ ] `C-FE-03` `constraint` Nothing inside the header sets a blend or a background of its own. `src: Front-end specification`
- [ ] `C-FE-04` `ui` The wordmark renders dark over the light ground, light over the dark ground. `src: Front-end specification`
- [ ] `C-FE-05` `ui` The wordmark renders as a negative over the brushed metal band. `src: Front-end specification`
- [ ] `C-FE-06` `constraint` No scroll listener changes a header class. `src: Front-end specification`
- [ ] `C-FE-07` `ui` Two pointer layers follow the pointer where the pointer is fine. `src: Front-end specification`
- [ ] `C-FE-08` `constraint` Neither pointer layer renders without a fine pointer. `src: Front-end specification`
- [ ] `C-FE-09` `ui` The pointer ring trails, arriving late with a slight overshoot. `src: Front-end specification`
- [ ] `C-FE-10` `ui` Three rule strengths are used structurally. `src: Front-end specification`
- [ ] `C-FE-11` `constraint` Every mark is drawn geometry inheriting the current colour. `src: Front-end specification`
- [ ] `C-FE-12` `ui` The attachment mark swaps between an empty state, a completed state. `src: Front-end specification`
- [ ] `C-FE-13` `ui` The close control rotates a half turn when pointed at. `src: Front-end specification`
- [ ] `C-FE-14` `data` The dot field pairs forty-two dots with twenty-one unfilled home circles. `src: Front-end specification`
- [ ] `C-FE-15` `capability` Scroll position is smoothed so an impulse decays. `src: Front-end specification`
- [ ] `C-FE-16` `constraint` Every scroll-linked animation reads the smoothed position. `src: Front-end specification`
- [ ] `C-FE-17` `contract` A reveal fires regardless after a safety deadline. `src: Front-end specification`
- [ ] `C-FE-18` `capability` The positioning line is broken per character, per word, per line at once. `src: Front-end specification`
- [ ] `C-FE-19` `constraint` The positioning line split is reversible. `src: Front-end specification`
- [ ] `C-FE-20` `literal` The studio strip reads `FULL-CYCLE DIGITAL AGENCY`, `EST. 2023`, `Canada`. `src: Front-end specification`
- [ ] `C-FE-21` `ui` Each client sector count is circled by an irregular ellipse that crosses itself. `src: Front-end specification`
- [ ] `C-FE-22` `literal` The footer year mark reads `23-26`. `src: Front-end specification`
- [ ] `C-FE-23` `constraint` No binary asset ships, the build succeeding with an empty asset directory. `src: Front-end specification`
- [ ] `C-FE-24` `capability` A case still is generated from a seed derived from the case slug. `src: Front-end specification`
- [ ] `C-FE-25` `contract` One case slug always produces one identical image. `src: Front-end specification`
- [ ] `C-FE-26` `ui` The brushed metal band carries one soft specular streak across the upper third. `src: Front-end specification`
- [ ] `C-FE-27` `ui` The rotating wordmark mark counter-rotates so the mark reads as no spinner. `src: Front-end specification`
- [ ] `C-FE-28` `constraint` Generated stills stay abstract so nobody mistakes one for a case. `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One studio exists, the portal tenancy unit being the engagement. `src: Constraints`
- [ ] `C-CN-02` `constraint` Nothing on a marketing route waits on a query. `src: Constraints`
- [ ] `C-CN-03` `constraint` Everything read without identifying is published, cacheable. `src: Constraints`
- [ ] `C-CN-04` `constraint` Everything else is a record behind a token or a session. `src: Constraints`
- [ ] `C-CN-05` `constraint` No project management tooling is built. `src: Constraints`
- [ ] `C-CN-06` `constraint` No chat is built. `src: Constraints`
- [ ] `C-CN-07` `constraint` No folder-based file store is built. `src: Constraints`
- [ ] `C-CN-08` `constraint` No live calendar integration is built. `src: Constraints`
- [ ] `C-CN-09` `constraint` No payments, invoicing, subscriptions, pricing page exist. `src: Constraints`
- [ ] `C-CN-10` `constraint` No comments, likes, follows, messaging exist on public routes. `src: Constraints`
- [ ] `C-CN-11` `constraint` No external network call happens at run time. `src: Constraints`
- [ ] `C-CN-12` `constraint` No third-party analytics endpoint is called. `src: Constraints`
- [ ] `C-CN-13` `constraint` No fingerprinting happens. `src: Constraints`
- [ ] `C-CN-14` `constraint` No native application is built. `src: Constraints`
- [ ] `C-CN-15` `constraint` The four licensed typefaces are never shipped. `src: Constraints`
- [ ] `C-CN-16` `data` A fallback stack is named for each of the four voices. `src: Constraints`
- [ ] `C-CN-17` `capability` Reduced motion is honoured rather than ignored. `src: Constraints`
- [ ] `C-CN-18` `capability` The desktop class is keyed to pointer capability. `src: Constraints`
- [ ] `C-CN-19` `capability` The root type size derives from the reader preference. `src: Constraints`
- [ ] `C-CN-20` `constraint` The reference brand appears nowhere in the built output. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The application is reachable at `APP_PUBLIC_URL`. `src: Deployment contract`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under `/api`. `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the application is ready. `src: Deployment contract`
- [ ] `C-DC-05` `contract` The application starts from the environment image with no manual steps. `src: Deployment contract`
- [ ] `C-DC-06` `contract` Credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/` exists at the application root, empty. `src: Deployment contract`
- [ ] `C-DC-08` `contract` Reserved `.downloads/` exists at the application root, empty. `src: Deployment contract`
- [ ] `C-DC-09` `contract` A production build is served behind a static server, never a dev server. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends. `src: Deployment contract`
- [ ] `C-DC-11` `contract` The server is not a child of the shell. `src: Deployment contract`
- [ ] `C-DC-12` `contract` The server binds `0.0.0.0`. `src: Deployment contract`
- [ ] `C-DC-13` `constraint` No edge function is used. `src: Deployment contract`
- [ ] `C-DC-14` `constraint` No persistent volume, fixed container name, custom network is declared. `src: Deployment contract`
- [ ] `C-DC-15` `contract` Field names in the API shapes are exact. `src: Deployment contract`
- [ ] `C-DC-16` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract`
- [ ] `C-DC-17` `contract` An invalid call is rejected as a client error, never a server error. `src: Deployment contract`
- [ ] `C-DC-18` `contract` An unauthorized call is rejected, never silently succeeding. `src: Deployment contract`
- [ ] `C-DC-19` `constraint` An in-memory store never substitutes for PostgreSQL. `src: Deployment contract`
- [ ] `C-DC-20` `constraint` A portal query never reads every engagement, filtering in the view. `src: Deployment contract`

## Pinned literals

| Value | Section | Item |
|---|---|---|
| `studio@example.com` | User roles | `C-RL-19` |
| `client@example.com` | User roles | `C-RL-19` |
| `client2@example.com` | User roles | `C-RL-19` |
| `deku-demo-pw-2026` | User roles | `C-RL-20` |
| `briefs/{brief_token}/{sha256_of_bytes}.{ext}` | Core features | `C-CF-11` |
| `deliverables/{engagement_id}/{version_id}/{sha256_of_bytes}.{ext}` | Core features | `C-CF-12` |
| `LOADING...` | Core features | `C-CF-24` |
| `WE DO` | Core features | `C-CF-31` |
| `What` | Core features | `C-CF-31` |
| `Vision.` | Core features | `C-CF-32` |
| `Clarity.` | Core features | `C-CF-32` |
| `Flow.` | Core features | `C-CF-32` |
| `Execution.` | Core features | `C-CF-32` |
| `Selected Cases` | Core features | `C-CF-40` |
| `The Archive` | Core features | `C-CF-63` |
| `Nothing matches all of those. The nearest is:` | Core features | `C-CF-68` |
| `not published` | Core features | `C-CF-70` |
| `GET CAPABILITIES DECK` | Core features | `C-CF-84` |
| `Still working it out` | Core features | `C-CF-92` |
| `Booked. We will see you then.` | Core features | `C-CF-100` |
| `restrained` | Core features | `C-CF-112` |
| `expressive` | Core features | `C-CF-112` |
| `classical` | Core features | `C-CF-112` |
| `contemporary` | Core features | `C-CF-112` |
| `Eight is plenty. Swap one out?` | Core features | `C-CF-115` |
| `Skip this` | Core features | `C-CF-118` |
| `Use the list instead` | Core features | `C-CF-119` |
| `Start a brief from this` | Core features | `C-CF-125` |
| `Whoever sent you this deck can see which pages were read.` | Core features | `C-CF-132` |
| `This deck has expired. Ask for a fresh link.` | Core features | `C-CF-133` |
| `Right now` | Core features | `C-CF-136` |
| `Waiting on you` | Core features | `C-CF-137` |
| `Approve` | Core features | `C-CF-144` |
| `Request changes` | Core features | `C-CF-144` |
| `What needs to change?` | Core features | `C-CF-145` |
| `Approved <DATE> by <ACTOR>. Changes create a new version.` | Core features | `C-CF-148` |
| `Daily` | Core features | `C-CF-150` |
| `Weekly` | Core features | `C-CF-150` |
| `Off` | Core features | `C-CF-150` |
| `/` | User flow | `C-UF-01` |
| `/contact/` | User flow | `C-UF-02` |
| `/privacy-policy/` | User flow | `C-UF-03` |
| `/terms/` | User flow | `C-UF-04` |
| `/work/` | User flow | `C-UF-05` |
| `/brief/` | User flow | `C-UF-06` |
| `/deck/` | User flow | `C-UF-07` |
| `/portal/` | User flow | `C-UF-08` |
| `/login` | User flow | `C-UF-09` |
| `/signup` | User flow | `C-UF-10` |
| `DATABASE_URL` | Technical requirements | `C-TR-06` |
| `STORAGE_ENDPOINT` | Technical requirements | `C-TR-07` |
| `STORAGE_BUCKET` | Technical requirements | `C-TR-07` |
| `STORAGE_ACCESS_KEY` | Technical requirements | `C-TR-08` |
| `STORAGE_SECRET_KEY` | Technical requirements | `C-TR-08` |
| `APP_PUBLIC_URL` | Technical requirements | `C-TR-09` |
| `APP_PUBLIC_PORT` | Technical requirements | `C-TR-09` |
| `Token Market` | Data model | `C-DM-27` |
| `FULL-CYCLE DIGITAL AGENCY` | Front-end specification | `C-FE-20` |
| `EST. 2023` | Front-end specification | `C-FE-20` |
| `Canada` | Front-end specification | `C-FE-20` |
| `23-26` | Front-end specification | `C-FE-22` |
| `4173` | Deployment contract | `C-DC-02` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| The exact colour value behind each named family, tone, shade | `C-UX-05` |
| The exact easing curve behind the eased motion character | `C-UX-13` |
| The exact gutter, radius, breakpoint measurement | `C-FE-01` |
| The budget band thresholds, held as content | `C-CF-95` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 4 | 6 |
| User roles | 1 | 20 |
| Core features | 52 | 162 |
| User flow | 6 | 20 |
| UI and UX notes | 15 | 28 |
| Technical requirements | 9 | 22 |
| Data model | 8 | 30 |
| Front-end specification | 14 | 28 |
| Constraints | 4 | 20 |
| Deployment contract | 10 | 20 |

