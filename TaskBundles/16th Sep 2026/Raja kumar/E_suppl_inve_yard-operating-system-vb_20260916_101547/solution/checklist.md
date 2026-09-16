# Checklist: Junction

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Items: 177
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` Two writers arriving together for one finite resource never both win `src: Overview, two writers arriving together must never both win`
- [ ] `C-OV-02` `capability` Outside haulage companies book their own arrival slots in the haulier portal `src: Overview, the haulier portal where outside companies book their own arrival slots`

## C-RL User roles

- [ ] `C-RL-01` `role` A role counts only in the scope of the resource touched `src: User roles, A role counts only in the scope of the resource it touches`
- [ ] `C-RL-02` `role` A gate operator session calling a site manager endpoint is denied by the server `src: User roles, a direct API call from a gate operator session to any site manager-only endpoint must be rejected by the server`
- [ ] `C-RL-03` `constraint` A denied call leaves the protected state unchanged `src: User roles, leaving the protected state unchanged`
- [ ] `C-RL-04` `role` Haulier or customer users sign in to a separate portal identity space `src: User roles, Haulier and customer users sign in to the portal, a separate identity space`
- [ ] `C-RL-05` `role` A site manager holds approvals at one site `src: User roles, every operational action at one site, approvals`
- [ ] `C-RL-06` `role` A spotter acts only on moves assigned to that spotter `src: User roles, their own assigned moves and issue reports`
- [ ] `C-RL-07` `role` A dispatcher is refused a release approval decision `src: User roles, moves, the map, exceptions, shifts, dock read`
- [ ] `C-RL-08` `constraint` Signup creates no account in either identity space `src: User roles, Signup is closed`
- [ ] `C-RL-09` `role` A security administrator is refused an operational write `src: User roles, watchlists, footage, cases, audit read`
- [ ] `C-RL-10` `role` An analyst is refused an operational write `src: User roles, reports and exports`

## C-CF Core features

- [ ] `C-CF-01` `constraint` A door holds at most one confirmed appointment for any overlapping moment `src: Core features, A door holds at most one confirmed appointment for any overlapping moment`
- [ ] `C-CF-02` `capability` Bookings for one window arriving together confirm only as many as there are capable free doors `src: Core features, Bookings for one window arriving together confirm as many as there are capable free doors`
- [ ] `C-CF-03` `capability` Every booking beyond the free doors is refused with alternatives `src: Core features, every other one is refused with alternatives`
- [ ] `C-CF-04` `constraint` A window merely touching another window's end is not an overlap `src: Core features, a window that merely touches another's end is not an overlap`
- [ ] `C-CF-05` `constraint` Two moves arriving together for one asset leave exactly one `src: Core features, Two moves for one asset, or two moves into one free spot, arriving together leave exactly one`
- [ ] `C-CF-06` `constraint` Two moves arriving together into one free spot leave exactly one `src: Core features, or two moves into one free spot, arriving together leave exactly one`
- [ ] `C-CF-07` `capability` A cancelled move frees its destination `src: Core features, a cancelled or completed move frees its destination`
- [ ] `C-CF-08` `constraint` A move for an asset past the staleness threshold is refused `src: Core features, A move for an asset not confirmed within the site's staleness threshold is refused`
- [ ] `C-CF-09` `capability` A refused stale move raises a confirmation task `src: Core features, a confirmation task is raised instead`
- [ ] `C-CF-10` `constraint` Only an observation at the destination verifies a placed move `src: Core features, only the observation verifies`
- [ ] `C-CF-11` `constraint` The requester never approves their own release request `src: Core features, the requester never approves their own request`
- [ ] `C-CF-12` `capability` An eligible site manager at the site releases a held visit through approval `src: Core features, A held visit is released only by an approval decided by an eligible site manager at that site`
- [ ] `C-CF-13` `constraint` A revoked grant stops working on the same session at once `src: Core features, A revoked grant stops working on the same session at once`
- [ ] `C-CF-14` `constraint` Another company's booking answers exactly as a booking that does not exist `src: Core features, Another company's booking and a site the haulier is not authorised at answer exactly as something that does not exist`
- [ ] `C-CF-15` `constraint` A site the haulier holds no authorisation at answers exactly as a missing site `src: Core features, a site the haulier is not authorised at answer exactly as something that does not exist`
- [ ] `C-CF-16` `constraint` Availability states only whether a window can be had `src: Core features, availability states only whether a window can be had`
- [ ] `C-CF-17` `constraint` A customer with fewer than five loads in a period sees suppression rather than a number `src: Core features, A customer with fewer than five loads in a period sees suppression, not a number`
- [ ] `C-CF-18` `capability` Custody events form a verifiable chain `src: Core features, Custody events form a verifiable chain`
- [ ] `C-CF-19` `capability` A custody correction is recorded as a new event `src: Core features, a correction is a new event`
- [ ] `C-CF-20` `constraint` No connection rewrites a custody event `src: Core features, no connection can rewrite one`
- [ ] `C-CF-21` `constraint` A booking confirmation is sent once per booking `src: Core features, A booking confirmation is sent once per booking`
- [ ] `C-CF-22` `constraint` A booking confirmation names no load or customer `src: Core features, names no load or customer`
- [ ] `C-CF-23` `capability` A visit link dies on cancellation `src: Core features, a visit link dies on cancellation`
- [ ] `C-CF-24` `constraint` A shift crossing a daylight saving change lasts its real elapsed time `src: Core features, A shift crossing a daylight saving change lasts the time that really elapsed`
- [ ] `C-CF-25` `capability` A terms page appears in every footer `src: Core features, A terms page in every footer`
- [ ] `C-CF-26` `capability` The product's own not-found page answers an unknown address `src: Core features, the product's own not-found page`
- [ ] `C-CF-27` `capability` A publisher reads a page view log `src: Core features, a page view log a publisher reads`
- [ ] `C-CF-28` `capability` Security headers accompany every response `src: Core features, security headers on every response`
- [ ] `C-CF-29` `constraint` The contact form refuses a bot `src: Core features, a contact form that refuses a bot`
- [ ] `C-CF-30` `capability` A completed move frees its destination `src: Core features, a cancelled or completed move frees its destination`
- [ ] `C-CF-31` `constraint` Approver eligibility is read when the decision is made `src: Core features, eligibility is read when the decision is made`

## C-UF User flow

- [ ] `C-UF-01` `ui` The carrier booking page shows only open windows for the chosen site `src: User flow, opens /carrier/book, picks Dallas Crossdock, an inbound dry van and a date, sees only open windows`
- [ ] `C-UF-02` `ui` A toast confirms a completed carrier booking `src: User flow, books one; a toast confirms it`
- [ ] `C-UF-03` `ui` The Dallas lane board shows the held Oakridge lorry with a pending release request `src: User flow, finds the held Oakridge lorry with its release request pending`
- [ ] `C-UF-04` `ui` Approving the release leaves the visit reading admitted `src: User flow, opens that approval and approves it; the visit reads admitted`
- [ ] `C-UF-05` `ui` The map draws stale trailers faded with a dashed edge `src: User flow, sees stale trailers drawn faded with a dashed edge`
- [ ] `C-UF-06` `ui` A loading surface is shaped like its content `src: User flow, Every surface has loading shaped like its content`
- [ ] `C-UF-07` `ui` An error state carries the request identifier `src: User flow, error with the request identifier`
- [ ] `C-UF-08` `ui` An empty surface offers the action that ends the emptiness `src: User flow, empty with the action that ends it`
- [ ] `C-UF-09` `contract` A console call without a session is refused with unauthenticated `src: User flow, Every console and portal route needs a session`
- [ ] `C-UF-10` `ui` An unauthenticated console visit renders a sign in panel in place `src: User flow, an unauthenticated visit renders a sign in panel in place and never serves data`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The lime marks emphasis only: the primary action, the active item, a hover, a live dot `src: UI/UX notes, spends one mid, vivid lime on emphasis only`
- [ ] `C-UX-02` `ui` The lime is never a section ground `src: UI/UX notes, The lime is never a section ground`
- [ ] `C-UX-03` `ui` Public sections alternate whole grounds of near-white neutral, near-black cool neutral, near-black neutral `src: UI/UX notes, alternates whole sections of near-white neutral, near-black cool neutral and near-black neutral grounds`
- [ ] `C-UX-04` `ui` Sentences are set in Junction Grotesk `src: UI/UX notes, Type is Junction Grotesk for sentences`
- [ ] `C-UX-05` `ui` Small upper case labels are set in Junction Mono `src: UI/UX notes, Junction Mono for small upper case labels`
- [ ] `C-UX-06` `ui` Headings arrive a character at a time through a band of lime `src: UI/UX notes, headings arrive a character at a time through a band of lime`
- [ ] `C-UX-07` `ui` The console is designed dark, dense, built for scanning `src: UI/UX notes, The console is designed dark, dense, built for scanning`
- [ ] `C-UX-08` `ui` Every surface shows a visible focus ring under keyboard navigation `src: UI/UX notes, every surface has full keyboard navigation with a visible focus ring`
- [ ] `C-UX-09` `ui` No state is signalled by colour or motion alone `src: UI/UX notes, no state is signalled by colour or motion alone`
- [ ] `C-UX-10` `ui` Each responsive breakpoint changes structure, never size `src: UI/UX notes, each responsive breakpoint changes structure, never size`
- [ ] `C-UX-11` `ui` Structural hairlines fade at their ends `src: UI/UX notes, draws structure with hairlines that fade at their ends`
- [ ] `C-UX-12` `ui` Danger reads light vivid red, caution reads amber, success reads muted green `src: UI/UX notes, a light, vivid red warns, an amber cautions and a muted green marks success`
- [ ] `C-UX-13` `ui` Aligned figures use tabular digits `src: UI/UX notes, aligned figures use tabular digits`
- [ ] `C-UX-14` `ui` Controls are slightly rounded, panels more `src: UI/UX notes, Controls are slightly rounded, panels more`
- [ ] `C-UX-15` `ui` The console light theme follows the operating system until a member chooses `src: UI/UX notes, its required light theme follows the operating system until a member chooses`
- [ ] `C-UX-16` `ui` Panels are raised deep neutral, secondary text muted neutral, borders faint hairlines `src: UI/UX notes, Panels are raised deep neutral, secondary text is muted neutral and borders are faint hairlines`
- [ ] `C-UX-17` `ui` Inputs take the lime rule on focus `src: UI/UX notes, Inputs take the lime rule on focus`
- [ ] `C-UX-18` `ui` Labels sit above fields with errors beneath `src: UI/UX notes, labels sit above fields with errors beneath`
- [ ] `C-UX-19` `ui` A toast confirms a completed write `src: UI/UX notes, a toast confirms a completed write`
- [ ] `C-UX-20` `ui` Overlays close on Escape, returning focus `src: UI/UX notes, overlays close on Escape and return focus`
- [ ] `C-UX-21` `ui` A destructive action asks for confirmation first `src: UI/UX notes, a destructive action asks first`
- [ ] `C-UX-22` `ui` Icon-only controls carry labels `src: UI/UX notes, icon-only controls carry labels`
- [ ] `C-UX-23` `ui` Touch targets are generous `src: UI/UX notes, touch targets are generous`
- [ ] `C-UX-24` `ui` The console surface rail sits on the left `src: UI/UX notes, the console is a rail on the left`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` POST /api/auth/login returns an access_token for a seeded member `src: Technical requirements, POST /api/auth/login takes {"email", "password"}, exchanges them with Keycloak`
- [ ] `C-TR-02` `contract` A member token on a portal route is refused with principal_kind_mismatch `src: Technical requirements, A member token presented to any /api/portal/ route`
- [ ] `C-TR-03` `contract` A site belonging to another organisation answers 404 not_found `src: Technical requirements, A site belonging to another organisation answers exactly as a site that does not exist`
- [ ] `C-TR-04` `contract` An elevated role grant without an expiry is refused with expiry_required `src: Technical requirements, a grant of an elevated role without an expiry is refused with 422 and code expiry_required`
- [ ] `C-TR-05` `contract` A call into an unentitled module is refused with module_not_entitled `src: Technical requirements, a call into an unentitled module at a site is refused with 403 and code module_not_entitled`
- [ ] `C-TR-06` `contract` An overlapping booking on one door is refused with door_unavailable `src: Technical requirements, door_unavailable, or door_out_of_service`
- [ ] `C-TR-07` `contract` A booking on an out of service door is refused with door_out_of_service `src: Technical requirements, the door is in service and holds no confirmed booking overlapping any moment of the window`
- [ ] `C-TR-08` `contract` A booking on a door lacking the asset type is refused with door_incapable `src: Technical requirements, the door permits the asset type and has the equipment`
- [ ] `C-TR-09` `contract` A capacity refusal carries alternatives listing starts_at plus ends_at `src: Technical requirements, "alternatives": [{"starts_at", "ends_at"}]`
- [ ] `C-TR-10` `contract` An update naming an older version is refused with version_conflict carrying current_version `src: Technical requirements, an update based on an older version is refused with 409, code version_conflict`
- [ ] `C-TR-11` `contract` A second move for an asset is refused with asset_has_open_move naming the open move `src: Technical requirements, code asset_has_open_move, with {"move_id"} naming the open move`
- [ ] `C-TR-12` `contract` A move into a reserved destination is refused with destination_reserved `src: Technical requirements, the destination is reserved by another open move`
- [ ] `C-TR-13` `contract` A move for a stale asset position is refused with position_stale `src: Technical requirements, code position_stale, and a position confirmation task is raised for that asset`
- [ ] `C-TR-14` `contract` A destination refusing the asset type is refused with destination_incompatible `src: Technical requirements, code destination_incompatible`
- [ ] `C-TR-15` `contract` A request to reach verified directly is refused with illegal_transition `src: Technical requirements, no request moves it to verified directly`
- [ ] `C-TR-16` `contract` Assigning a spotter without a covering shift is refused with spotter_not_on_shift `src: Technical requirements, code spotter_not_on_shift`
- [ ] `C-TR-17` `contract` A requester deciding their own request is refused with self_approval_forbidden `src: Technical requirements, The requester deciding their own request is refused with 403 and code self_approval_forbidden`
- [ ] `C-TR-18` `contract` A member ineligible at the request's site is refused with forbidden `src: Technical requirements, a member not eligible for that request at that request's site is refused with 403 and code forbidden`
- [ ] `C-TR-19` `contract` A decision on a request no longer pending is refused with already_decided `src: Technical requirements, a decision on a request that is no longer pending is refused with 409 and code already_decided`
- [ ] `C-TR-20` `capability` A refused approval decision is recorded with outcome denied `src: Technical requirements, a refused approval decision is recorded with action approval.decide and outcome denied`
- [ ] `C-TR-21` `contract` An active watchlist plate leaves the visit refused `src: Technical requirements, no active entry matches the plate`
- [ ] `C-TR-22` `constraint` An expired watchlist entry matches nothing `src: Technical requirements, An entry past its expiry matches nothing, from the instant it expires`
- [ ] `C-TR-23` `contract` A suspended haulier's visit is held on haulier authorisation `src: Technical requirements, the haulier is authorised for this site and direction and not suspended`
- [ ] `C-TR-24` `contract` A cancelled booking's visit link answers 410 visit_link_revoked `src: Technical requirements, A token for a cancelled booking is refused from the instant of cancellation with 410 and code visit_link_revoked`
- [ ] `C-TR-25` `constraint` A visit view never carries the load detail `src: Technical requirements, never the load detail, the customer name`
- [ ] `C-TR-26` `contract` An Idempotency-Key reused with a different body is refused with idempotency_key_reused `src: Technical requirements, the same key with a different body is refused with 409 and code idempotency_key_reused`
- [ ] `C-TR-27` `contract` A replay of one key with one body returns the original response `src: Technical requirements, returns the original response for a replay of the same key and the same body within twenty four hours`
- [ ] `C-TR-28` `contract` A booking confirmation subject begins Junction booking confirmed followed by the booking reference `src: Technical requirements, Junction booking confirmed: followed by the booking reference`
- [ ] `C-TR-29` `contract` Approval request mail reaches every eligible member except the requester `src: Technical requirements, every member eligible to decide it except the requester`
- [ ] `C-TR-30` `constraint` A member ineligible for the request receives no approval request mail `src: Technical requirements, every eligible approver except the requester is told`
- [ ] `C-TR-31` `contract` Every console API response carries Cache-Control: no-store `src: Technical requirements, Every console and portal API response carries Cache-Control: no-store`
- [ ] `C-TR-32` `contract` Every response carries X-Content-Type-Options: nosniff `src: Technical requirements, carries X-Content-Type-Options: nosniff`
- [ ] `C-TR-33` `contract` Every response carries a Strict-Transport-Security policy with a positive max-age `src: Technical requirements, a Strict-Transport-Security policy with a positive max-age`
- [ ] `C-TR-34` `contract` A contact submission filling the decoy field is refused with rejected_submission `src: Technical requirements, A submission whose decoy field is filled is refused with 422 and code rejected_submission`
- [ ] `C-TR-35` `contract` A fourth same email contact submission inside sixty seconds is refused with rate_limited `src: Technical requirements, A fourth submission carrying the same email inside sixty seconds is refused with 429 and code rate_limited`
- [ ] `C-TR-36` `data` A valid contact submission is stored in the form_submission table with its email `src: Technical requirements, is stored in the form_submission table with its email`
- [ ] `C-TR-37` `contract` A non-publisher reading the page view log is refused with forbidden `src: Technical requirements, any other principal is refused with 403 and code forbidden`
- [ ] `C-TR-38` `contract` The security report endpoint recomputes the result from the answers alone `src: Technical requirements, computed from the answers alone, ignoring any score supplied`
- [ ] `C-TR-39` `contract` A weakest L03 layer leads to /modules/load-verification `src: Technical requirements, L03 to /modules/load-verification`
- [ ] `C-TR-40` `contract` A full answer set leads to /yard-security `src: Technical requirements, a full score leads to /yard-security`
- [ ] `C-TR-41` `contract` The customer report below five loads answers loads null with suppressed true `src: Technical requirements, receives loads and median_dwell_seconds as null and suppressed as true`
- [ ] `C-TR-42` `capability` A customer loads list names only the caller's own loads `src: Technical requirements, lists only the caller's own loads`
- [ ] `C-TR-43` `contract` A shift response carries duration_seconds `src: Technical requirements, returns its instants and its duration_seconds`
- [ ] `C-TR-44` `contract` Site scoped instants carry the site's offset `src: Technical requirements, Site scoped instants carry the site's offset`
- [ ] `C-TR-45` `contract` An unknown path under /api/ answers 404 with not_found `src: Technical requirements, An unknown path under /api/ answers 404 with code not_found in the error shape`
- [ ] `C-TR-46` `contract` A fresh position observation reads staleness fresh `src: Technical requirements, An asset's reading carries staleness of fresh or stale against the site's threshold`
- [ ] `C-TR-47` `capability` A portal booking is readable as an appointment carrying its door `src: Technical requirements, for a portal booking as much as a console one`
- [ ] `C-TR-48` `contract` The not-found document carries the heading Page not found `src: Technical requirements, the heading Page not found`
- [ ] `C-TR-49` `contract` The terms document's first heading reads Terms of use `src: Technical requirements, whose first heading is Terms of use`
- [ ] `C-TR-50` `data` Seeded Everwear holds six loads at Dallas in September 2026 `src: Technical requirements, Everwear has the customer user reports@everwear.example.com and six loads at DAL1 in September 2026`
- [ ] `C-TR-51` `contract` A portal token on a console route is refused with principal_kind_mismatch `src: Technical requirements, a portal token presented to any other /api/ route, is refused with 401`
- [ ] `C-TR-52` `contract` A site the member holds no grant on answers 404 not_found `src: Technical requirements, that sits at a site the caller holds no grant on, answers 404 with code not_found`
- [ ] `C-TR-53` `contract` The page view log returns route, status, viewed_at newest first `src: Technical requirements, GET /api/page-views returns them newest first`
- [ ] `C-TR-54` `capability` A document request for a public content route is recorded as a page view `src: Technical requirements, Every document request the server answers for a public content route is recorded`
- [ ] `C-TR-55` `contract` The security report names the band Sealed yard from eighty upward `src: Technical requirements, 80 to 100 is Sealed yard in the lime`
- [ ] `C-TR-56` `contract` A layer below forty percent reads Exposed `src: Technical requirements, Exposed below forty`
- [ ] `C-TR-57` `constraint` A capacity refusal writes no booking `src: Technical requirements, bookings for the same resource arriving at the same moment never confirm more than the resource can hold`
- [ ] `C-TR-58` `contract` Seeded Dallas door D05 accepts reefer only `src: Technical requirements, D05 accepts reefer only`
- [ ] `C-TR-59` `contract` Seeded Dallas door D06 is out of service `src: Technical requirements, D06 accepts dry_van and is out of service`
- [ ] `C-TR-60` `literal` Seeded watchlist plate `TX-9KR-221` is active at Dallas `src: Technical requirements, An active entry for the plate TX-9KR-221`
- [ ] `C-TR-61` `literal` Seeded watchlist plate `TX-4LM-870` expired at the end of January 2026 `src: Technical requirements, an entry for the plate TX-4LM-870`
- [ ] `C-TR-62` `literal` Halvard Transport holds registration `MC-400932` suspended at Dallas `src: Technical requirements, Halvard Transport | MC-400932 | DAL1, suspended`
- [ ] `C-TR-63` `literal` Oakridge Carriers holds registration `MC-300771` authorised at Atlanta only `src: Technical requirements, Oakridge Carriers | MC-300771 | ATL1 only`
- [ ] `C-TR-64` `literal` Dallas Crossdock runs site code `DAL1` in `America/Chicago` `src: Technical requirements, DAL1 | Dallas Crossdock | Tidewater | America/Chicago`
- [ ] `C-TR-65` `literal` Reno Distribution runs site code `RNO2` without haulier appointments `src: Technical requirements, RNO2 | Reno Distribution | Tidewater | America/Los_Angeles | gate_management, yard_visibility, dispatch`
- [ ] `C-TR-66` `literal` The member `dual@tidewater.example.com` manages Reno, operating a Dallas gate `src: Technical requirements, dual@tidewater.example.com | Tidewater | site_manager at RNO2 and gate_operator at DAL1`
- [ ] `C-TR-67` `literal` The Keycloak realm is `junction` `src: Technical requirements, realm junction`
- [ ] `C-TR-68` `ui` With default inputs the calculator shows Labor Savings of 255,528 `src: Technical requirements, With every input at its default the calculator shows exactly: Labor Savings 255,528`
- [ ] `C-TR-69` `ui` With default inputs the calculator shows Spotter Savings of 193,248 `src: Technical requirements, Spotter Savings 193,248`
- [ ] `C-TR-70` `ui` With default inputs the calculator shows Detention plus Demurrage Savings of 192,850 `src: Technical requirements, Detention & Demurrage Savings 192,850`
- [ ] `C-TR-71` `ui` With default inputs the calculator shows a total of 641,626 `src: Technical requirements, a total of 641,626`
- [ ] `C-TR-72` `ui` With default inputs the calculator shows Est. Savings of 23% `src: Technical requirements, Est. Savings of 23%`
- [ ] `C-TR-73` `ui` Labour savings follow check-ins per day at thirty nine minutes saved per check-in `src: Technical requirements, Minutes saved per check-in is 39`
- [ ] `C-TR-74` `ui` A held visit rises to the top of its lane on the lane board `src: Technical requirements, A held visit rises to the top of its lane`
- [ ] `C-TR-75` `ui` The dispatch board shows unassigned, in flight, attention columns beside a map `src: Technical requirements, three columns and a map in one screen`
- [ ] `C-TR-76` `ui` The door calendar renders closed periods as unavailable rather than empty `src: Technical requirements, Closed periods render as unavailable, not empty`
- [ ] `C-TR-77` `ui` Every site home panel states the age of its data `src: Technical requirements, Every panel states its own data age`
- [ ] `C-TR-78` `ui` The exception inbox lists open exceptions most serious first, oldest first within a level `src: Technical requirements, ordered by severity then age`
- [ ] `C-TR-79` `data` A replayed contact submission_id stores one row, answering the original id `src: Technical requirements, answers 201 with the original {"id"} and produces one record`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: Data model, Every seeded account uses the password deku-demo-pw-2026`
- [ ] `C-DM-02` `data` A custody_event row holds its sequence, seal_number, prior_hash plus hash `src: Data model, custody_event - id, organisation_id, site_id, asset_number, sequence, kind`
- [ ] `C-DM-03` `constraint` No connection the application holds changes a custody_event row `src: Data model, neither can be changed or have a row removed by any connection the application holds`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The not-found document shows 404 in lime with a BACK TO HOME action `src: Front-end specification, the code 404 at display-1 in lime with its zero set as a slashed glyph`
- [ ] `C-FE-02` `ui` The header pill never changes height, collapses or hides on scroll `src: Front-end specification, It never changes height, never collapses and never hides on scroll`
- [ ] `C-FE-03` `ui` Connector figures draw themselves as their section enters, un-drawing on the way back `src: Front-end specification, Connectors draw themselves`
- [ ] `C-FE-04` `ui` Under reduced motion headings render as plain text on first paint `src: Front-end specification, Under a reduced motion preference the split is not performed`
- [ ] `C-FE-05` `ui` The security questionnaire's fix action for a weak Load Verification layer opens its module route `src: Front-end specification, the grader's second action goes to the route for the weakest layer`
- [ ] `C-FE-06` `ui` Every security layer row states Exposed, Partial or Covered beside its colour `src: Front-end specification, The grader's layer statuses carry Exposed, Partial and Covered`
- [ ] `C-FE-07` `ui` Below laptop width the console map becomes a spot list grouped by row `src: Front-end specification, the map becomes a spot list grouped by row`
- [ ] `C-FE-08` `ui` The home route opens on the pinned lorry sequence under the hero statement `src: Front-end specification, The home route opens on one full viewport canvas`
- [ ] `C-FE-09` `ui` Calculator values roll through digit stacks as inputs change `src: Front-end specification, A changing numeral is not re-rendered`
- [ ] `C-FE-10` `ui` Each security layer badge carries its own hue identifying the layer `src: Front-end specification, A layer badge is a tightly rounded rectangle with the tight label step in one of five layer hues`
- [ ] `C-FE-11` `ui` At phone width the content site header holds only the mark beside a menu trigger `src: Front-end specification, the mark with the trigger alone on mobile`
- [ ] `C-FE-12` `ui` Map asset states differ by shape or hatch, not by fill alone `src: Front-end specification, each map asset state is distinguishable from its neighbours by shape or hatch as well as fill`
- [ ] `C-FE-13` `ui` Section edges carry a shallow notch only where a new subject starts `src: Front-end specification, it marks the top of a section that introduces a new subject`
- [ ] `C-FE-14` `ui` The not-found description is set in the monospace face `src: Front-end specification, the one place body copy is monospaced`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No row of a site without a grant is readable `src: Constraints, no row of a site a principal holds no grant on, is ever readable`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` GET /api/health returns 200 once the app is ready `src: Deployment contract, GET /api/health returns 200 once the app is ready`
- [ ] `C-DC-02` `contract` The HTTP API is served on the app's origin under /api `src: Deployment contract, The HTTP API is served on that same origin under the /api prefix`
- [ ] `C-DC-03` `contract` The app is reachable at APP_PUBLIC_URL `src: Deployment contract, The app must be reachable at APP_PUBLIC_URL`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | the password of every seeded account | C-DM-01 | Data model, opening paragraph |
| `TX-9KR-221` | the active watchlist plate at Dallas | C-TR-60 | Technical requirements, seeded fixtures |
| `TX-4LM-870` | the expired watchlist plate at Dallas | C-TR-61 | Technical requirements, seeded fixtures |
| `MC-400932` | the suspended haulier's registration | C-TR-62 | Technical requirements, seeded fixtures |
| `MC-300771` | the haulier authorised at Atlanta only | C-TR-63 | Technical requirements, seeded fixtures |
| `DAL1` | the Dallas Crossdock site code | C-TR-64 | Technical requirements, seeded fixtures |
| `America/Chicago` | the Dallas time zone | C-TR-64 | Technical requirements, seeded fixtures |
| `RNO2` | the Reno Distribution site code | C-TR-65 | Technical requirements, seeded fixtures |
| `dual@tidewater.example.com` | the member holding two roles at two sites | C-TR-66 | Technical requirements, seeded fixtures |
| `junction` | the Keycloak realm | C-TR-67 | Technical requirements, the stack |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 2 |
| User roles | 10 | 10 |
| Core features | 31 | 31 |
| User flow | 10 | 10 |
| UI and UX notes | 24 | 24 |
| Technical requirements | 79 | 79 |
| Data model | 3 | 3 |
| Front-end specification | 14 | 14 |
| Constraints | 1 | 1 |
| Deployment contract | 3 | 3 |

The obligation-bearing sentences counted here are the graded asks this checklist pairs to a
grading channel. The brief carries the companion product requirements in full, and the machine
proposal in the QC report counts every obligation-bearing sentence it contains; the balance is
carried for fidelity to the source and declared ungraded below rather than cited falsely.

- Declared but ungraded: `/app/USER_README.md` carrying every seeded address, the reserved
  `.browser_screenshots/` and `.downloads/` directories, the production build behind a static or
  preview server, the server outliving its session, binding `0.0.0.0`, and the absence of persistent
  volumes, fixed container names, custom networks and edge functions are Deployment contract
  obligations no separately running grader can observe.
- Declared but ungraded: the remaining obligations of Technical requirements, Data model and
  Front-end specification not listed above are carried from the companion in full so the build is
  specified completely, and no channel grades them.
- Declared but ungraded, window sections: the stale state that dims a surface and disables its
  writes needs a live channel failure no outside request can induce; the network manager row has no
  seeded member to exercise; automatic assignment by cost,
  the console staying responsive with two thousand assets, the absence of a native application and
  money in integer minor units have no pinned observable; the public motion and scroll character
  beyond the judged criteria is carried for fidelity.
