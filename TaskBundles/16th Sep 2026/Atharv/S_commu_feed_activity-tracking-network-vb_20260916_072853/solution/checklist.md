# Checklist: activity-tracking-network-vb

Items: 384
Unpinned values flagged: 0
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

---
## C-OV Overview

- [ ] `C-OV-01` `capability` A social network whose unit of content is a recorded athletic activity is served `src: Overview paragraph 1`
- [ ] `C-OV-02` `capability` An uploaded file recorded by a watch fans out across four subsystems `src: Overview paragraph 2`
- [ ] `C-OV-03` `capability` Numbers are derived from a noisy time-series rather than believed from the device `src: Overview paragraph 2`
- [ ] `C-OV-04` `capability` A track is matched against every segment the track crosses `src: Overview paragraph 2`
- [ ] `C-OV-05` `capability` Efforts enter ranked leaderboards, minting achievements `src: Overview paragraph 2`
- [ ] `C-OV-06` `capability` An activity lands in the feeds of the athletes following the uploader `src: Overview paragraph 2`
- [ ] `C-OV-07` `capability` Segment leaderboards, clubs, challenges, route planning, a subscription tier sit alongside the feed `src: Overview paragraph 4`
- [ ] `C-OV-08` `contract` Visibility is a property the data layer holds, with the interface only reporting `src: Overview paragraph 5`
- [ ] `C-OV-09` `constraint` No recording happens in the browser, so activities arrive as uploaded files or manual entries `src: Overview non-goals`
- [ ] `C-OV-10` `constraint` No payment capture exists, so the plan surface sells without charging `src: Overview non-goals`
- [ ] `C-OV-11` `constraint` No machine-learning type detection exists `src: Overview non-goals`
- [ ] `C-OV-12` `capability` The same leaderboard is a different list for different viewers `src: Overview final paragraph`
- [ ] `C-OV-13` `capability` Five audiences are served, from an athlete recording through to a prospective athlete `src: Overview audiences paragraph`

## C-RL User roles

- [ ] `C-RL-01` `role` One role named `athlete` exists, with open signup `src: User roles paragraph 1`
- [ ] `C-RL-02` `role` A block overrides every other rule, in both directions of reading `src: User roles boundary table`
- [ ] `C-RL-03` `role` An activity visibility of `everyone`, `followers`, `only_you` governs who reads the activity `src: User roles boundary table`
- [ ] `C-RL-04` `role` A `followers` activity is readable only through an `accepted` follow `src: User roles boundary table`
- [ ] `C-RL-05` `role` A `pending` follow request grants no access `src: User roles boundary table`
- [ ] `C-RL-06` `role` A plan of `free` or `subscriber` gates a named set of capabilities without being a role `src: User roles plan paragraph`
- [ ] `C-RL-07` `role` A `free` athlete reads the feed, activities, kudos, comments, clubs, challenges `src: User roles capability table`
- [ ] `C-RL-08` `role` A `free` athlete is refused the route builder, the heatmap, best-effort analysis, demographic leaderboard filters `src: User roles capability table`
- [ ] `C-RL-09` `role` A blocked athlete is refused the blocker's profile, activities, leaderboard rows, club posts, challenge standings, search results, kudos entries `src: User roles bullet 1`
- [ ] `C-RL-10` `role` A non-follower is refused a `followers` activity `src: User roles bullet 2`
- [ ] `C-RL-11` `role` A non-follower cannot infer a hidden activity from a rank gap, a row count, a total `src: User roles bullet 2`
- [ ] `C-RL-12` `role` Nobody reads another athlete's `only_you` activity at any plan by any path `src: User roles bullet 3`
- [ ] `C-RL-13` `role` Nobody reads a privacy zone through a profile, an export, a truncated activity `src: User roles bullet 4`
- [ ] `C-RL-14` `role` A `free` athlete calling a gated endpoint directly with a valid session is refused `src: User roles bullet 5`
- [ ] `C-RL-15` `contract` Authorization is enforced server-side on every read endpoint alongside every mutating endpoint `src: User roles closing paragraph`
- [ ] `C-RL-16` `contract` A direct call from a refused session is rejected by the server, leaving the protected state unchanged `src: User roles closing paragraph`
- [ ] `C-RL-17` `literal` Five accounts are seeded: `athlete@example.com`, `athlete2@example.com`, `athlete3@example.com`, `athlete4@example.com`, `athlete5@example.com` `src: User roles seeded table`
- [ ] `C-RL-18` `literal` Every seeded account signs in with `deku-demo-pw-2026` `src: User roles signup paragraph`
- [ ] `C-RL-19` `literal` The seeded athlete `Rowan Ellery` blocks `Mira Halloran` `src: User roles seeded table`
- [ ] `C-RL-20` `literal` The seeded athlete `Dorian Vance` defaults to `followers` with a profile flagged as not discoverable `src: User roles seeded table`
- [ ] `C-RL-21` `literal` The seeded athlete `Kit Bramwell` holds the plan `subscriber` `src: User roles seeded table`
- [ ] `C-RL-22` `capability` A newly created account is a `free` athlete defaulting to `everyone`, following nobody `src: User roles closing paragraph`

## C-CF Core features

- [ ] `C-CF-01` `capability` Sign-in takes an email with a password, returning a bearer token `src: Core features Accounts and sign-in`
- [ ] `C-CF-02` `contract` Passwords are stored hashed, never in the clear `src: Core features Accounts and sign-in`
- [ ] `C-CF-03` `contract` Identity is resolved from the session, never read from a request body `src: Core features Accounts and sign-in`
- [ ] `C-CF-04` `capability` Signup by email collects an address, a password, a display name, nothing further `src: Core features rule 1`
- [ ] `C-CF-05` `capability` A signup against an already registered address is refused without confirming the registration `src: Core features rule 2`
- [ ] `C-CF-06` `capability` A sign-in with a seeded email plus `deku-demo-pw-2026` succeeds, returning a token `src: Core features rule 3`
- [ ] `C-CF-07` `capability` A sign-in with a wrong password is denied, returning no token `src: Core features rule 4`
- [ ] `C-CF-08` `contract` A sign-in against an unregistered address returns the same status, body, response-time band as a wrong password `src: Core features rule 5`
- [ ] `C-CF-09` `contract` A progressive sign-in discloses nothing at the address step about whether an account exists `src: Core features rule 6`
- [ ] `C-CF-10` `capability` A request to an athlete-scoped endpoint carrying no bearer token is denied `src: Core features rule 7`
- [ ] `C-CF-11` `capability` Repeated failed sign-ins for one address are refused for a period `src: Core features rule 8`
- [ ] `C-CF-12` `capability` A federated identity returns a verified address, which is not re-verified `src: Core features rule 9`
- [ ] `C-CF-13` `contract` Two providers carrying one verified address yield one account with the second identity linked `src: Core features rule 10`
- [ ] `C-CF-14` `capability` A remembered session is offered at sign-in, defaulting to on `src: Core features rule 11`
- [ ] `C-CF-15` `capability` Settings lists live sessions, each endable remotely `src: Core features rule 11`
- [ ] `C-CF-16` `data` Acceptance of the terms is recorded with the exact text shown at the time `src: Core features rule 12`
- [ ] `C-CF-17` `capability` A follow of a discoverable profile takes effect immediately at state `accepted` `src: Core features rule 13`
- [ ] `C-CF-18` `capability` A follow of a non-discoverable profile creates a request at state `pending` `src: Core features rule 14`
- [ ] `C-CF-19` `ui` The follow control reads Follow, Requested, Following as three distinct states `src: Core features rule 15`
- [ ] `C-CF-20` `capability` Unfollowing removes access to a `followers` activity immediately `src: Core features rule 16`
- [ ] `C-CF-21` `contract` A block in either direction stops both athletes reaching the other's content by any read path `src: Core features rule 17`
- [ ] `C-CF-22` `contract` A block covers the profile, the activity page, the feed, a club feed, a club roster, challenge standings, a leaderboard, search, a kudos list, a comment list, the public interface, a logged-out read `src: Core features rule 18`
- [ ] `C-CF-23` `contract` Blocking is enforced at the data layer, so the endpoint returns nothing rather than a list being trimmed `src: Core features rule 19`
- [ ] `C-CF-24` `capability` A block removes any existing follow edge in both directions `src: Core features rule 20`
- [ ] `C-CF-25` `contract` A blocked athlete receives the same not-found returned for content never existing `src: Core features rule 21`
- [ ] `C-CF-26` `capability` An upload returns an upload identifier immediately, with processing running afterwards `src: Core features rule 22`
- [ ] `C-CF-27` `contract` The raw file is retained byte for byte exactly as the file arrived `src: Core features rule 23`
- [ ] `C-CF-28` `capability` A parser fix is re-runnable against the retained file without a re-upload `src: Core features rule 23`
- [ ] `C-CF-29` `capability` An unknown field in a device file is ignored rather than fatal `src: Core features rule 24`
- [ ] `C-CF-30` `capability` A partially parsed file produces an activity carrying what was recoverable plus a recorded warning `src: Core features rule 24`
- [ ] `C-CF-31` `data` The timestamps inside the file are the authority for the start time, never the moment of upload `src: Core features rule 25`
- [ ] `C-CF-32` `data` A timezone carried by the file is preferred over inference from coordinates `src: Core features rule 26`
- [ ] `C-CF-33` `data` An upload moves through `received`, `parsing`, `matching`, `ready`, terminating at `failed` or `duplicate_suspected` `src: Core features rule 27`
- [ ] `C-CF-34` `capability` A `failed` upload is retryable from the retained raw file without re-uploading `src: Core features rule 28`
- [ ] `C-CF-35` `capability` A manual entry produces no stream, produces no segment effort, appears visibly distinguished `src: Core features rule 29`
- [ ] `C-CF-36` `capability` A partner push produces the same activity model as a device file `src: Core features rule 30`
- [ ] `C-CF-37` `contract` Duplicate detection completes before segment matching begins `src: Core features rule 31`
- [ ] `C-CF-38` `capability` Duplicate detection checks the file identifier first, then start time, duration, distance within a tolerance `src: Core features rule 32`
- [ ] `C-CF-39` `capability` A suspected duplicate is flagged for the athlete to resolve rather than silently discarded `src: Core features rule 33`
- [ ] `C-CF-40` `capability` Discarding one duplicate candidate removes that candidate's efforts `src: Core features rule 33`
- [ ] `C-CF-41` `contract` Re-uploading identical bytes returns the earlier upload, creating no second activity `src: Core features rule 34`
- [ ] `C-CF-42` `contract` Photograph location metadata is stripped on the server at ingest before storage `src: Core features rule 35`
- [ ] `C-CF-43` `data` Stream types are `time`, `latlng`, `distance`, `altitude`, `heartrate`, `cadence`, `watts`, `temp`, `moving`, `grade_smooth` `src: Core features Streams and derived metrics`
- [ ] `C-CF-44` `data` Streams are stored separately from the activity row, fetched on demand `src: Core features rule 36`
- [ ] `C-CF-45` `data` Every stream declares measured or derived, with a derived stream recording an algorithm version `src: Core features rule 37`
- [ ] `C-CF-46` `data` Measured power is distinguished from estimated power on the record `src: Core features rule 38`
- [ ] `C-CF-47` `capability` Streams of differing length are aligned on the time index rather than on array position `src: Core features rule 39`
- [ ] `C-CF-48` `capability` An average excludes a gap from the numerator alongside the denominator, stating the coverage `src: Core features rule 40`
- [ ] `C-CF-49` `data` Moving time differs from elapsed time on every activity `src: Core features rule 41`
- [ ] `C-CF-50` `data` Average speed is distance divided by moving time `src: Core features rule 42`
- [ ] `C-CF-51` `capability` Elevation gain comes from a smoothed altitude series above a threshold, never a sum of raw differences `src: Core features rule 43`
- [ ] `C-CF-52` `capability` A flat route reports elevation gain at or near zero `src: Core features rule 44`
- [ ] `C-CF-53` `capability` Distance between coordinates is computed on a spheroid `src: Core features rule 45`
- [ ] `C-CF-54` `capability` An average pace comes from averaging speed then inverting, never from averaging pace values `src: Core features rule 46`
- [ ] `C-CF-55` `data` Polylines are stored at several simplification levels, chosen by the zoom `src: Core features rule 47`
- [ ] `C-CF-56` `contract` Simplification preserves shape within a stated tolerance, never moving an endpoint `src: Core features rule 48`
- [ ] `C-CF-57` `data` Stored coordinates are bounded at six decimal places `src: Core features rule 49`
- [ ] `C-CF-58` `contract` A segment match is a curve-similarity comparison rather than a proximity comparison `src: Core features rule 50`
- [ ] `C-CF-59` `capability` Candidate segments are retrieved by a spatial index over the activity bounding box `src: Core features rule 51`
- [ ] `C-CF-60` `capability` The spatial index covers segment geometry rather than segment start locations `src: Core features rule 52`
- [ ] `C-CF-61` `contract` A match requires a sub-path following the segment geometry in order, in the correct direction `src: Core features rule 53`
- [ ] `C-CF-62` `capability` The matching tolerance is a corridor width, admitting a traverse drifting `25` metres laterally `src: Core features rule 54`
- [ ] `C-CF-63` `contract` Effort start times are interpolated between samples, never snapped to the nearest sample `src: Core features rule 55`
- [ ] `C-CF-64` `capability` An activity traversing a segment several times produces several efforts `src: Core features rule 56`
- [ ] `C-CF-65` `capability` A partial traversal produces no effort `src: Core features rule 57`
- [ ] `C-CF-66` `capability` An activity plus summary is visible before matching finishes `src: Core features rule 58`
- [ ] `C-CF-67` `ui` A running match reports matching in progress rather than reporting zero segments `src: Core features rule 59`
- [ ] `C-CF-68` `contract` A re-run of matching replaces an activity's efforts atomically rather than duplicating `src: Core features rule 60`
- [ ] `C-CF-69` `capability` A segment creator renames, marks hazardous, edits geometry, deletes `src: Core features rule 61`
- [ ] `C-CF-70` `capability` Renaming a segment recomputes nothing `src: Core features rule 62`
- [ ] `C-CF-71` `capability` A hazardous segment suppresses the leaderboard, retaining efforts `src: Core features rule 63`
- [ ] `C-CF-72` `contract` A segment geometry edit recomputes every effort, leaving no superseded effort ranked `src: Core features rule 64`
- [ ] `C-CF-73` `capability` Deleting a segment follows one stated policy applied everywhere `src: Core features rule 65`
- [ ] `C-CF-74` `data` The activity type drives expected streams, computed metrics, eligible segments, permitted leaderboards, summary formatting, available achievements `src: Core features rule 66`
- [ ] `C-CF-75` `contract` A run never shares a leaderboard with a ride `src: Core features rule 67`
- [ ] `C-CF-76` `contract` Changing an activity type re-runs matching, invalidating efforts, invalidating achievements, recomputing leaderboards `src: Core features rule 68`
- [ ] `C-CF-77` `capability` A leaderboard supports all-time, year-to-date, month-to-date, today, social, club, demographic, sex scopes `src: Core features rule 69`
- [ ] `C-CF-78` `contract` One effort per athlete per leaderboard is listed, being that athlete's best `src: Core features rule 70`
- [ ] `C-CF-79` `contract` Ranking uses elapsed time for the effort rather than moving time `src: Core features rule 71`
- [ ] `C-CF-80` `contract` Ties break deterministically by effort timestamp, earliest first `src: Core features rule 72`
- [ ] `C-CF-81` `capability` A flagged effort is excluded from a leaderboard rather than deleted, staying visible on the owning activity `src: Core features rule 73`
- [ ] `C-CF-82` `contract` Ranks are computed over the set the viewer sees, running contiguously from one `src: Core features rule 74`
- [ ] `C-CF-83` `contract` A row count shown to a viewer counts only rows that viewer sees `src: Core features rule 75`
- [ ] `C-CF-84` `contract` A leaderboard is never one cached list shared between viewers `src: Core features rule 76`
- [ ] `C-CF-85` `capability` A leaderboard is recomputed on effort insertion, on flagging, on a privacy change, on a geometry edit `src: Core features rule 77`
- [ ] `C-CF-86` `data` Achievement kinds are an overall top-three place, a segment personal record, a distance-class personal record `src: Core features rule 78`
- [ ] `C-CF-87` `contract` An achievement stores an earned date plus a superseded date, surviving the athlete being beaten `src: Core features rule 79`
- [ ] `C-CF-88` `capability` A time-windowed achievement expires rather than standing forever `src: Core features rule 80`
- [ ] `C-CF-89` `capability` A best effort is a sliding scan over the distance stream, so a fastest `5` kilometre beginning at `3200` metres reports that span `src: Core features rule 81`
- [ ] `C-CF-90` `capability` An implausible effort is flagged for review using speed, acceleration, activity-type plausibility `src: Core features rule 82`
- [ ] `C-CF-91` `capability` An athlete flagging another athlete's effort files a report rather than performing a removal `src: Core features rule 83`
- [ ] `C-CF-92` `data` Every flag records a reason with a disposition, remaining appealable `src: Core features rule 84`
- [ ] `C-CF-93` `capability` The following feed lists activities from followed athletes plus joined clubs, newest start time first `src: Core features rule 86`
- [ ] `C-CF-94` `contract` Fan-out is hybrid: written for ordinary accounts, read-assembled above a follower threshold, merged with ordering preserved `src: Core features rule 87`
- [ ] `C-CF-95` `contract` Visibility is applied at the moment of the read rather than only at the moment of the write `src: Core features rule 88`
- [ ] `C-CF-96` `capability` Club posts, challenge completions, achievements appear as feed items `src: Core features rule 89`
- [ ] `C-CF-97` `capability` Near-identical activities recorded together appear as one grouped item naming every athlete `src: Core features rule 90`
- [ ] `C-CF-98` `contract` The feed is cursor-paginated on a stable sort key, so an insertion between pages skips no row, repeats no row `src: Core features rule 91`
- [ ] `C-CF-99` `contract` A feed page fetches no stream, reading summaries plus the coarsest polyline `src: Core features rule 92`
- [ ] `C-CF-100` `contract` Kudos are one per athlete per activity, toggleable, counted once `src: Core features rule 93`
- [ ] `C-CF-101` `capability` A comment carries an author with a time, supports a mention, is deletable by the author or the activity owner `src: Core features rule 94`
- [ ] `C-CF-102` `contract` Repeated kudos on one activity inside the configured window produce one notification carrying a count `src: Core features rule 95`
- [ ] `C-CF-103` `data` Every activity carries a visibility of `everyone`, `followers`, `only_you` `src: Core features rule 96`
- [ ] `C-CF-104` `data` An athlete carries a default visibility plus a separate profile discoverability control `src: Core features rule 97`
- [ ] `C-CF-105` `contract` Visibility is enforced on the feed, the profile, the activity page, leaderboards, club feeds, challenge standings, search, the public interface, aggregates `src: Core features rule 98`
- [ ] `C-CF-106` `capability` A privacy zone hides the start of any activity beginning inside the zone `src: Core features rule 99`
- [ ] `C-CF-107` `contract` The stored polyline is truncated rather than hidden at render time `src: Core features rule 100`
- [ ] `C-CF-108` `contract` Truncation removes samples from every stream rather than from position alone `src: Core features rule 101`
- [ ] `C-CF-109` `contract` A truncated activity reports the full distance with the full time, stating that the map is partial `src: Core features rule 102`
- [ ] `C-CF-110` `contract` The truncation location is randomised within the zone rather than placed at the zone boundary `src: Core features rule 103`
- [ ] `C-CF-111` `contract` A segment effort beginning or ending inside a zone is suppressed `src: Core features rule 104`
- [ ] `C-CF-112` `contract` No read path returns a privacy zone to anyone `src: Core features rule 105`
- [ ] `C-CF-113` `contract` An aggregate cell contributes only above a minimum distinct-athlete threshold `src: Core features rule 106`
- [ ] `C-CF-114` `contract` An activity carrying non-public visibility is excluded from an aggregate entirely `src: Core features rule 107`
- [ ] `C-CF-115` `contract` A privacy-zone-truncated portion is excluded from every aggregate `src: Core features rule 108`
- [ ] `C-CF-116` `capability` An athlete opts out of aggregates independently of activity visibility `src: Core features rule 109`
- [ ] `C-CF-117` `capability` An athlete exports activities, streams, efforts, achievements, kudos, comments, clubs, routes `src: Core features rule 110`
- [ ] `C-CF-118` `capability` Account deletion removes activities, recomputes affected leaderboards, rebuilds aggregates `src: Core features rule 111`
- [ ] `C-CF-119` `capability` Kudos left by a deleted athlete are anonymised rather than removed `src: Core features rule 112`
- [ ] `C-CF-120` `data` A club carries a name, a sport type, a description, a roster, a feed, with roles of `member` or `admin` `src: Core features rule 113`
- [ ] `C-CF-121` `capability` A club feed shows only member activities the viewer is permitted to read `src: Core features rule 114`
- [ ] `C-CF-122` `data` A challenge carries a metric of `distance`, `elevation`, `activity_count`, a target, an activity type, a date window `src: Core features rule 115`
- [ ] `C-CF-123` `contract` A challenge counts an activity by the local date at the start location `src: Core features rule 116`
- [ ] `C-CF-124` `contract` Challenge standings respect visibility, blocking, rank contiguity `src: Core features rule 117`
- [ ] `C-CF-125` `capability` The route builder saves a route with a derived distance plus a derived elevation gain, for a `subscriber` `src: Core features rule 118`
- [ ] `C-CF-126` `capability` The heatmap renders aggregate popularity under the distinct-athlete threshold, for a `subscriber` `src: Core features rule 119`
- [ ] `C-CF-127` `contract` Every gated capability is refused at the data layer rather than hidden client-side `src: Core features rule 120`
- [ ] `C-CF-128` `contract` A gated endpoint called with a `free` session is refused, with a `subscriber` session succeeding `src: Core features rule 121`
- [ ] `C-CF-129` `ui` The plan surface states price, currency, period, renewal terms, the cancellation route before purchase `src: Core features rule 122`
- [ ] `C-CF-130` `capability` A gift purchase completes logged out, issuing a redemption code `src: Core features rule 123`
- [ ] `C-CF-131` `ui` A feature route describes a capability the product actually delivers `src: Core features rule 124`
- [ ] `C-CF-132` `ui` The not-found view carries a heading, a body denying the dead-end reading, five options ranked by likelihood `src: Core features rule 125`
- [ ] `C-CF-133` `ui` The server-error view is a separate page carrying different copy `src: Core features rule 126`
- [ ] `C-CF-134` `ui` Every route carries a title with a description, none shared between two routes `src: Core features rule 127`
- [ ] `C-CF-135` `contract` A public activity, segment, profile page is rendered on the server `src: Core features rule 128`
- [ ] `C-CF-136` `contract` Every internal link resolves, so no route leads to a missing page `src: Core features rule 129`
- [ ] `C-CF-137` `capability` An athlete authorises another application with separately grantable scopes `src: Core features rule 130`
- [ ] `C-CF-138` `capability` An athlete revokes each connected application individually `src: Core features rule 131`
- [ ] `C-CF-139` `contract` An application's reach into an activity is bounded by that activity's own visibility `src: Core features rule 132`
- [ ] `C-CF-140` `contract` A webhook is signed, delivered at least once, carrying resource state `src: Core features rule 133`
- [ ] `C-CF-141` `contract` Rate limits apply per application plus per athlete, stating a reset time `src: Core features rule 134`
- [ ] `C-CF-142` `contract` A retried upload, kudos, follow, join produces no second effect `src: Core features rule 135`

## C-UF User flow

- [ ] `C-UF-01` `ui` The route map covers the signup landing, log in, signup, features, maps, challenges, subscription, gift, stories, help, search `src: User flow Routes`
- [ ] `C-UF-02` `ui` The athlete route map covers the feed, upload, activity detail, activity edit, profile, following, followers, best efforts `src: User flow Routes`
- [ ] `C-UF-03` `ui` The comparison route map covers segment explore, segment detail, clubs, club detail, challenge detail `src: User flow Routes`
- [ ] `C-UF-04` `ui` The account route map covers settings, privacy, applications, export `src: User flow Routes`
- [ ] `C-UF-05` `ui` A single top navigation bar is carried on every surface with one item order `src: User flow Routes`
- [ ] `C-UF-06` `capability` An unauthenticated request for an athlete route redirects to `/login`, landing afterwards on the route asked for `src: User flow Entry and redirects`
- [ ] `C-UF-07` `capability` A sign-in with no pending destination lands on `/feed` `src: User flow Entry and redirects`
- [ ] `C-UF-08` `capability` A logged-in visitor arriving at the signup landing is redirected to `/feed` `src: User flow Entry and redirects`
- [ ] `C-UF-09` `capability` The gift route is reachable logged out, never redirecting to `/login` `src: User flow Entry and redirects`
- [ ] `C-UF-10` `capability` A request for content the viewer may not read returns the not-found view rather than a refusal `src: User flow Entry and redirects`
- [ ] `C-UF-11` `capability` A `free` athlete requesting a subscriber route sees the subscription offer, staying signed in `src: User flow Entry and redirects`
- [ ] `C-UF-12` `ui` The signup landing shows three panels, with the card offering federated controls first, the email control last `src: User flow journey 1`
- [ ] `C-UF-13` `ui` A feed card carries the athlete, the activity name, the type in text, a route picture, a statistic block `src: User flow journey 2`
- [ ] `C-UF-14` `ui` Kudos toggles, so a second press lowers the count, a third press raises the count `src: User flow journey 3`
- [ ] `C-UF-15` `capability` A viewer who is not an accepted follower of `Dorian Vance` reads ranks one through four `src: User flow journey 4`
- [ ] `C-UF-16` `capability` A viewer accepted by `Dorian Vance` reads ranks one through five `src: User flow journey 4`
- [ ] `C-UF-17` `capability` `Mira Halloran` finds `Rowan Ellery` absent from every read path `src: User flow journey 5`
- [ ] `C-UF-18` `ui` The upload wizard runs ordered steps: choose the file, confirm type with name, set visibility, submit `src: User flow journey 6`
- [ ] `C-UF-19` `capability` A repeat upload of one file reaches `duplicate_suspected`, creating no second activity `src: User flow journey 7`
- [ ] `C-UF-20` `capability` Retyping an activity from `run` to `ride` clears running efforts, creating riding efforts `src: User flow journey 8`
- [ ] `C-UF-21` `capability` A logged-out reader of a truncated activity sees a route beginning away from the zone `src: User flow journey 9`
- [ ] `C-UF-22` `capability` A viewer preferring imperial reads miles where a viewer preferring metric reads kilometres `src: User flow journey 11`
- [ ] `C-UF-23` `capability` A logged-out gift purchase completes, issuing a redemption code `src: User flow journey 12`
- [ ] `C-UF-24` `ui` Every list surface carries loading, empty, populated, failed states `src: User flow States`
- [ ] `C-UF-25` `ui` A failed list offers a retry preserving the query with the filters `src: User flow States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` A mid, vivid orange is the only saturated hue in the core palette `src: UI/UX notes The character, in four decisions`
- [ ] `C-UX-02` `ui` The brand hue sits at the third step of a nine-step ramp with four darker steps above `src: UI/UX notes The character, in four decisions`
- [ ] `C-UX-03` `ui` Three named podium colours carry first, second, third place `src: UI/UX notes The character, in four decisions`
- [ ] `C-UX-04` `ui` The second-place colour is a light cool neutral rather than a plain grey `src: UI/UX notes The character, in four decisions`
- [ ] `C-UX-05` `ui` One display family ships in two widths at three weights with a true italic `src: UI/UX notes The character, in four decisions`
- [ ] `C-UX-06` `ui` The interface size is `15px` on a `24px` line at weights `400`, `600`, `700` `src: UI/UX notes The character, in four decisions`
- [ ] `C-UX-07` `ui` The podium colours are reserved for achievement, used nowhere else `src: UI/UX notes Palette by role`
- [ ] `C-UX-08` `ui` A warning uses the mid, vivid amber rather than the first-place colour `src: UI/UX notes Palette by role`
- [ ] `C-UX-09` `ui` Ink is a near-black neutral over a near-white neutral page ground `src: UI/UX notes Palette by role`
- [ ] `C-UX-10` `ui` Dark panels use a near-black cool neutral `src: UI/UX notes Palette by role`
- [ ] `C-UX-11` `ui` The spacing ladder is named, expressed in `rem`, dense at the small end `src: UI/UX notes Ramps, spacing, radius, borders, layering`
- [ ] `C-UX-12` `ui` Four border styles ship: none, solid, dashed, dotted `src: UI/UX notes Ramps, spacing, radius, borders, layering`
- [ ] `C-UX-13` `ui` Layering keeps a five-band scale, refusing the consent vendor's maximum value `src: UI/UX notes Ramps, spacing, radius, borders, layering`
- [ ] `C-UX-14` `ui` Four duplicate token pairs collapse to one token each `src: UI/UX notes Ramps, spacing, radius, borders, layering`
- [ ] `C-UX-15` `ui` Numerals use a condensed width with tabular figures so columns align `src: UI/UX notes Typography`
- [ ] `C-UX-16` `ui` The condensed width is never used for prose `src: UI/UX notes Typography`
- [ ] `C-UX-17` `ui` The mark is an ascending elevation trace of two nested chevron forms `src: UI/UX notes Iconography`
- [ ] `C-UX-18` `ui` The kudos glyph renders one step below the text beside the glyph `src: UI/UX notes Iconography`
- [ ] `C-UX-19` `ui` Activity-type glyphs form a closed set with a generic fallback `src: UI/UX notes Iconography`
- [ ] `C-UX-20` `ui` The loading indicator turns in five accelerating then easing stops `src: UI/UX notes Motion`
- [ ] `C-UX-21` `ui` Easing ships as named tokens rather than loose curves `src: UI/UX notes Motion`
- [ ] `C-UX-22` `ui` Under reduced motion the indicator becomes static, feed items appear without entrance animation `src: UI/UX notes Motion`
- [ ] `C-UX-23` `ui` An animated route replay never autoplays `src: UI/UX notes Motion`
- [ ] `C-UX-24` `ui` Four breakpoints are expressed in `rem`, written mobile-first in one spelling `src: UI/UX notes Responsive, print and forced colours`
- [ ] `C-UX-25` `ui` An activity page prints the route, the summary, the splits without feed chrome `src: UI/UX notes Responsive, print and forced colours`
- [ ] `C-UX-26` `ui` Under forced colours a route line carries a non-colour distinction `src: UI/UX notes Responsive, print and forced colours`
- [ ] `C-UX-27` `ui` Under forced colours a podium place is stated in text `src: UI/UX notes Responsive, print and forced colours`
- [ ] `C-UX-28` `ui` One `h1` per route, a skip link, landmarks for banner, navigation, main, contentinfo `src: UI/UX notes Accessibility`
- [ ] `C-UX-29` `ui` The consent bar is keyboard-operable with a one-action reject path `src: UI/UX notes Accessibility`
- [ ] `C-UX-30` `ui` A federated control names the provider in the accessible name `src: UI/UX notes Accessibility`
- [ ] `C-UX-31` `ui` Every statistic is announced with a unit `src: UI/UX notes Accessibility`
- [ ] `C-UX-32` `ui` A route exists as text giving distance, elevation, location rather than as a map alone `src: UI/UX notes Accessibility`
- [ ] `C-UX-33` `ui` A leaderboard is a real table carrying headers `src: UI/UX notes Accessibility`
- [ ] `C-UX-34` `ui` The brand hue steps down the ramp for body text on white `src: UI/UX notes Accessibility`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Routes are rendered on the server with interactive regions hydrating in the browser `src: Technical requirements Stack`
- [ ] `C-TR-02` `constraint` One interface framework runs, never two generations side by side `src: Technical requirements Stack`
- [ ] `C-TR-03` `contract` The app reads `DATABASE_URL` alongside `DB_URL` for the database `src: Technical requirements Services`
- [ ] `C-TR-04` `contract` The app reads `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` `src: Technical requirements Services`
- [ ] `C-TR-05` `constraint` Neither backing service is downloaded, installed, compiled, started by the app `src: Technical requirements Services`
- [ ] `C-TR-06` `contract` Bytes live in the object store, never on the container filesystem, never as a database blob `src: Technical requirements Object storage`
- [ ] `C-TR-07` `literal` A raw upload is stored at `uploads/{athlete_id}/{upload_id}/{sha256_of_bytes}.{ext}` `src: Technical requirements Object storage`
- [ ] `C-TR-08` `literal` A decoded series is stored at `streams/{activity_id}/{stream_type}.json` `src: Technical requirements Object storage`
- [ ] `C-TR-09` `contract` An object read back hashes to the value the app recorded, with no re-encoding `src: Technical requirements Object storage`
- [ ] `C-TR-10` `contract` Protected bytes are reached through an authenticated streaming endpoint applying the same visibility rules `src: Technical requirements Object storage`
- [ ] `C-TR-11` `constraint` The bucket is never made public `src: Technical requirements Object storage`
- [ ] `C-TR-12` `contract` `KUDOS_BATCH_WINDOW_SEC` is read from the environment on every use `src: Technical requirements Environment-injected behaviour`
- [ ] `C-TR-13` `contract` `FANOUT_FOLLOWER_THRESHOLD` is read from the environment on every use `src: Technical requirements Environment-injected behaviour`
- [ ] `C-TR-14` `constraint` Neither injected value is hardcoded in the app `src: Technical requirements Environment-injected behaviour`
- [ ] `C-TR-15` `contract` Parsing, deduplication, derivation, matching, achievement computation, fan-out, projection run outside the triggering request `src: Technical requirements Asynchronous processing`
- [ ] `C-TR-16` `constraint` No queue service exists, so asynchronous work is driven from the app's own process `src: Technical requirements Asynchronous processing`
- [ ] `C-TR-17` `contract` Every asynchronous stage is idempotent, so a repeat produces the same result `src: Technical requirements Asynchronous processing`
- [ ] `C-TR-18` `contract` Measurements are stored in canonical SI, converted at the presentation boundary alone `src: Technical requirements Units and quantities`
- [ ] `C-TR-19` `contract` The viewer's unit preference governs rather than the recorder's `src: Technical requirements Units and quantities`
- [ ] `C-TR-20` `data` Elevation, distance, temperature carry independent viewer preferences `src: Technical requirements Units and quantities`
- [ ] `C-TR-21` `data` The start instant is stored in UTC `src: Technical requirements Time and place`
- [ ] `C-TR-22` `data` The timezone identifier of the start location is stored rather than the athlete's home timezone `src: Technical requirements Time and place`
- [ ] `C-TR-23` `data` A derived local date is stored `src: Technical requirements Time and place`
- [ ] `C-TR-24` `data` An activity crossing midnight belongs to the start date `src: Technical requirements Time and place`
- [ ] `C-TR-25` `data` Streams are offsets from the start instant rather than absolute timestamps `src: Technical requirements Time and place`
- [ ] `C-TR-26` `contract` A spatial query is answered by a spatial index rather than by a bounding-box scan in app code `src: Technical requirements Geometry`
- [ ] `C-TR-27` `contract` Every derived quantity records the algorithm version producing the quantity `src: Technical requirements Determinism and versioning`
- [ ] `C-TR-28` `contract` Two runs of one algorithm over one set of streams produce identical results `src: Technical requirements Determinism and versioning`
- [ ] `C-TR-29` `contract` Recomputation is a deliberate operation stating a scope `src: Technical requirements Determinism and versioning`
- [ ] `C-TR-30` `contract` The signup landing paints first content inside a second-and-a-half budget `src: Technical requirements Performance`
- [ ] `C-TR-31` `contract` The signup landing transfers under nine hundred kilobytes `src: Technical requirements Performance`
- [ ] `C-TR-32` `contract` The feed first render completes under two seconds `src: Technical requirements Performance`
- [ ] `C-TR-33` `contract` An error view ships no application script `src: Technical requirements Performance`
- [ ] `C-TR-34` `contract` A map surface is never on the render-blocking path `src: Technical requirements Performance`
- [ ] `C-TR-35` `contract` Every log record is structured, carrying an athlete identifier plus a correlation identifier `src: Technical requirements Logging`
- [ ] `C-TR-36` `contract` No coordinate pair, privacy-zone centre, access token, password appears in a log record `src: Technical requirements Logging`
- [ ] `C-TR-37` `contract` `GET /api/health` returns `200` once the app, the database, the bucket answer `src: Technical requirements Health`
- [ ] `C-TR-38` `contract` Idempotency covers every retryable write through a key or through the write's own nature `src: Technical requirements Idempotency`
- [ ] `C-TR-39` `ui` The public half serves content routes, auth flows, the subscription surface, the gift flow, server-rendered public pages `src: Technical requirements The site's own backend`
- [ ] `C-TR-40` `constraint` No mapping vendor is contacted for tiles, geocoding, routing `src: Technical requirements The site's own backend`

## C-DM Data model

- [ ] `C-DM-01` `data` An athlete record carries a display name, a plan, a unit preference, a timezone, privacy defaults `src: Data model Entities`
- [ ] `C-DM-02` `data` An athlete identity record carries a provider, a provider subject, a verified address `src: Data model Entities`
- [ ] `C-DM-03` `data` An athlete setting history record carries a field, a value, the date taking effect `src: Data model Entities`
- [ ] `C-DM-04` `data` A follow record carries a follower, a followee, a state `src: Data model Entities`
- [ ] `C-DM-05` `data` An upload record carries a source, an object key, a byte hash, a status, an error code `src: Data model Entities`
- [ ] `C-DM-06` `data` An activity record carries a type, a name, a visibility, a start instant, a start timezone, a local start date `src: Data model Entities`
- [ ] `C-DM-07` `data` An activity summary carries distance, moving time, elapsed time, elevation gain, averages, an algorithm version `src: Data model Entities`
- [ ] `C-DM-08` `data` A stream record carries a type, a sample rate, an object key, a measured flag `src: Data model Entities`
- [ ] `C-DM-09` `data` A segment record carries a geometry, a bounding box, an activity type, a geometry version `src: Data model Entities`
- [ ] `C-DM-10` `data` A segment effort record carries sample indices, an interpolated start instant, an elapsed time, a flag state `src: Data model Entities`
- [ ] `C-DM-11` `data` An achievement record carries a kind, a rank, an earned date, a superseded date `src: Data model Entities`
- [ ] `C-DM-12` `data` A feed entry record carries an athlete with an activity plus the activity start instant `src: Data model Entities`
- [ ] `C-DM-13` `data` An api application record carries granted scopes plus a token hash `src: Data model Entities`
- [ ] `C-DM-14` `data` A gift purchase record carries a buyer address as a string rather than an account `src: Data model Entities`
- [ ] `C-DM-15` `data` Visibility values are exactly `everyone`, `followers`, `only_you` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-16` `data` Activity type values are exactly `run`, `ride`, `swim`, `hike`, `ski`, `walk` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-17` `data` Follow state values are exactly `pending`, `accepted`, `blocked` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-18` `data` Upload status values are exactly `received`, `parsing`, `matching`, `ready`, `failed`, `duplicate_suspected` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-19` `data` Effort flag state values are exactly `clear`, `flagged`, `excluded` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-20` `data` Achievement kind values are exactly `overall_top_three`, `segment_pr`, `distance_pr` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-21` `data` Plan values are exactly `free`, `subscriber` `src: Data model Enumerations, exact casing`
- [ ] `C-DM-22` `contract` Elapsed time is greater than or equal to moving time on every summary `src: Data model Invariants`
- [ ] `C-DM-23` `contract` An upload at `duplicate_suspected` has produced no effort anywhere `src: Data model Invariants`
- [ ] `C-DM-24` `contract` An effort count for one activity on one segment does not grow from a re-run finding the same traversals `src: Data model Invariants`
- [ ] `C-DM-25` `contract` One athlete's kudos on one activity counts once however many submissions arrive `src: Data model Invariants`
- [ ] `C-DM-26` `literal` The seeded segment is `Ridgeway Climb`, type `ride`, `1800` metres long, `95` metres of gain `src: Data model Seed data`
- [ ] `C-DM-27` `literal` The seeded corridor tolerance is `30` metres `src: Data model Seed data`
- [ ] `C-DM-28` `literal` The seeded privacy zone radius is `400` metres `src: Data model Seed data`
- [ ] `C-DM-29` `literal` The reference activity `Ridgeway long loop` reports `5400` seconds elapsed `src: Data model Seed data`
- [ ] `C-DM-30` `literal` The reference activity reports `4200` seconds moving, the difference being a `1200` second stationary period `src: Data model Seed data`
- [ ] `C-DM-31` `literal` The reference activity reports `32000` metres of distance `src: Data model Seed data`
- [ ] `C-DM-32` `literal` The reference activity reports `480` metres of elevation gain `src: Data model Seed data`
- [ ] `C-DM-33` `literal` Fixture tracks are synthesised at a `3` second sample rate `src: Data model Seed data`
- [ ] `C-DM-34` `literal` A `10000` metre due-east track at latitude `55` measures `10000` metres `src: Data model Seed data`
- [ ] `C-DM-35` `literal` A flat fixture route reports elevation gain at or below `10` metres `src: Data model Seed data`
- [ ] `C-DM-36` `literal` A two-kilometre fixture at `4:00` then `6:00` reports an average pace of `5:00` `src: Data model Seed data`
- [ ] `C-DM-37` `literal` The seeded club is `Dawn Patrol`, sport `ride` `src: Data model Seed data`
- [ ] `C-DM-38` `literal` The seeded challenge is `April Ascent`, metric `elevation`, target `4000` metres `src: Data model Seed data`
- [ ] `C-DM-39` `literal` The seeded route is `Loch Circuit`, `24000` metres, `310` metres of gain `src: Data model Seed data`
- [ ] `C-DM-40` `literal` The seeded plans are `Free` alongside `Ridgeline Premium` at `1200` monthly, `8000` annual `src: Data model Seed data`
- [ ] `C-DM-41` `literal` An aggregate cell contributes only above `3` distinct athletes `src: Data model Seed data`
- [ ] `C-DM-42` `literal` The feed page size is `30` `src: Data model Seed data`
- [ ] `C-DM-43` `constraint` Seeding is idempotent, so restarting duplicates no row `src: Data model Seed data`
- [ ] `C-DM-44` `literal` The seeded athlete `Sena Okafor` follows `Rowan Ellery` at state `accepted` `src: Data model Seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The header carries the mark, the wordmark, five centre items, a right cluster `src: Front-end specification Global chrome`
- [ ] `C-FE-02` `ui` The header shadow sits near a two-and-a-half percent alpha `src: Front-end specification Global chrome`
- [ ] `C-FE-03` `ui` The footer carries four columns headed `Features`, `Subscription`, `Support`, `Privacy` `src: Front-end specification Global chrome`
- [ ] `C-FE-04` `ui` The consent bar carries a heading naming cookies plainly `src: Front-end specification Global chrome`
- [ ] `C-FE-05` `ui` The consent bar carries `Accept All`, `Customize`, `Reject Non-Essential`, `Show details` `src: Front-end specification Global chrome`
- [ ] `C-FE-06` `ui` The reject control matches the accept control in size, reachable in one action `src: Front-end specification Global chrome`
- [ ] `C-FE-07` `ui` The consent bar sits below the content rather than over the content `src: Front-end specification Global chrome`
- [ ] `C-FE-08` `ui` A skip link sits first in the document, visible on focus `src: Front-end specification Global chrome`
- [ ] `C-FE-09` `ui` The signup landing shows a generated panel, the card on white, a second generated panel with a device composite `src: Front-end specification The signup landing`
- [ ] `C-FE-10` `literal` The signup heading reads `Community-Powered Motivation` `src: Front-end specification The signup landing`
- [ ] `C-FE-11` `literal` The signup controls read `Sign Up With Google`, `Sign Up With Apple`, `Sign Up With Email` `src: Front-end specification The signup landing`
- [ ] `C-FE-12` `ui` The email control carries the brand orange with the federated controls outlined `src: Front-end specification The signup landing`
- [ ] `C-FE-13` `literal` The log-in heading reads `Log In`, with a divider reading `or` `src: Front-end specification Log in`
- [ ] `C-FE-14` `literal` The log-in field carries the label `Email` above the placeholder `Your Email` `src: Front-end specification Log in`
- [ ] `C-FE-15` `ui` The remember-me control is checked by default `src: Front-end specification Log in`
- [ ] `C-FE-16` `ui` The not-found heading is a joke in the product's own language about a red light `src: Front-end specification The not-found view`
- [ ] `C-FE-17` `ui` The not-found view lists five options ranked by likelihood, beginning with a typo `src: Front-end specification The not-found view`
- [ ] `C-FE-18` `ui` The not-found illustration is drawn from strokes, circles, three filled discs `src: Front-end specification The not-found view`
- [ ] `C-FE-19` `ui` A statistic block receives a canonical value with a quantity type rather than a formatted string `src: Front-end specification The statistic block`
- [ ] `C-FE-20` `ui` A statistic block performs no arithmetic `src: Front-end specification The statistic block`
- [ ] `C-FE-21` `ui` A missing statistic renders as absent rather than as zero `src: Front-end specification The statistic block`
- [ ] `C-FE-22` `ui` An activity card carries a kudos control with a count plus a comment count `src: Front-end specification The activity card`
- [ ] `C-FE-23` `ui` A grouped card names every athlete in the group, carrying one route picture `src: Front-end specification The activity card`
- [ ] `C-FE-24` `ui` A manual-entry card is visibly distinguished, carrying no route picture `src: Front-end specification The activity card`
- [ ] `C-FE-25` `ui` The activity page shows the route, the statistics, an elevation chart, a splits table, the efforts `src: Front-end specification The activity page`
- [ ] `C-FE-26` `ui` The elevation chart is keyboard-navigable or paired with a data table `src: Front-end specification The activity page`
- [ ] `C-FE-27` `ui` The segment page states rank in text in the row rather than through colour alone `src: Front-end specification The segment page and its leaderboard`
- [ ] `C-FE-28` `ui` A hazardous segment shows no leaderboard, stating the reason `src: Front-end specification The segment page and its leaderboard`
- [ ] `C-FE-29` `ui` The upload wizard states the current step, keeping earlier steps revisitable `src: Front-end specification The upload wizard`
- [ ] `C-FE-30` `ui` A suspected duplicate shows both candidates side by side with distinguishing numbers `src: Front-end specification The upload wizard`
- [ ] `C-FE-31` `ui` Feedback arrives as a transient message anchored to one corner, never stealing focus `src: Front-end specification Feedback`
- [ ] `C-FE-32` `ui` An empty feed states the emptiness, offering the next action `src: Front-end specification Empty states`
- [ ] `C-FE-33` `ui` A generated region carries intrinsic dimensions so nothing shifts as the page settles `src: Front-end specification Assets, and the zero-asset substitution guide`
- [ ] `C-FE-34` `ui` Ten modules build the product, from the token layer through to the chart `src: Front-end specification Modules and component architecture`
- [ ] `C-FE-35` `ui` The activity page states that the map is partial where a privacy zone truncated the route `src: Front-end specification The activity card`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No email of any kind is sent `src: Constraints bullet 2`
- [ ] `C-CN-02` `constraint` No payment capture exists, so neither the plan surface nor the gift surface charges `src: Constraints bullet 3`
- [ ] `C-CN-03` `constraint` No third-party analytics, consent vendor, error reporter, map tile vendor is contacted at run time `src: Constraints bullet 4`
- [ ] `C-CN-04` `constraint` No second database, cache, queue, object store, identity provider exists `src: Constraints bullet 5`
- [ ] `C-CN-05` `constraint` No browser recording, device pairing, live position sharing exists `src: Constraints bullet 6`
- [ ] `C-CN-06` `constraint` No native application, desktop client, browser extension ships `src: Constraints bullet 7`
- [ ] `C-CN-07` `constraint` No binary asset ships: no image file, no video file, no font file `src: Constraints bullet 10`
- [ ] `C-CN-08` `constraint` The app stays responsive with up to 500 activities carrying up to 10 streams each `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173` with `4173` as the container-internal port `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` Neither the public port nor the public address is hardcoded `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The HTTP interface is served on the same origin under the `/api` prefix `src: Deployment contract bullet 2`
- [ ] `C-DC-05` `contract` `GET /api/health` returns `200` once the app is ready `src: Deployment contract bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual steps `src: Deployment contract bullet 4`
- [ ] `C-DC-07` `literal` Login credentials are written to `/app/USER_README.md` `src: Deployment contract bullet 5`
- [ ] `C-DC-08` `literal` Reserved `.browser_screenshots/` alongside `.downloads/` directories exist at the app root `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `constraint` A production build is served behind a static or preview server rather than a dev server `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The server keeps running after the session ends, detached from the shell `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The listener binds `0.0.0.0` rather than a loopback address `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `constraint` No persistent volume, fixed container name, custom network is declared `src: Deployment contract bullet 12`
- [ ] `C-DC-13` `contract` `POST /api/auth/login` takes an email with a password, returning `{"access_token"}` `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` `POST /api/uploads` returns `{"upload_id", "status"}` `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` `GET /api/feed` returns `{"items", "next_cursor"}` `src: Deployment contract API shapes`
- [ ] `C-DC-16` `contract` `GET /api/segments/{id}/leaderboard` returns `{"total", "entries"}` with a rank per entry `src: Deployment contract API shapes`
- [ ] `C-DC-17` `contract` `GET /api/privacy-zones` returns a radius without a centre `src: Deployment contract API shapes`
- [ ] `C-DC-18` `contract` `POST /api/gifts` accepts no bearer token `src: Deployment contract API shapes`
- [ ] `C-DC-19` `contract` An invalid or unauthorized call is rejected as a client error rather than a server error `src: Deployment contract API shapes`
- [ ] `C-DC-20` `constraint` No in-memory list, hardcoded payload, module-level dictionary substitutes for the named provider `src: Deployment contract No mocks`
- [ ] `C-DC-21` `constraint` A raw upload is never written to the container filesystem nor held as a database blob `src: Deployment contract No mocks`

---

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `athlete@example.com` | the first seeded athlete, who blocks another | `C-RL-17` |
| `athlete2@example.com` | the second seeded athlete, an accepted follower | `C-RL-17` |
| `athlete3@example.com` | the third seeded athlete, whose profile is hidden | `C-RL-17` |
| `athlete4@example.com` | the fourth seeded athlete, the blocked one | `C-RL-17` |
| `athlete5@example.com` | the fifth seeded athlete, the subscriber | `C-RL-17` |
| `deku-demo-pw-2026` | the corpus password | `C-RL-18` |
| `Rowan Ellery` | the first seeded athlete's display name | `C-RL-19` |
| `Mira Halloran` | the blocked athlete's display name | `C-RL-19` |
| `Dorian Vance` | the hidden athlete's display name | `C-RL-20` |
| `followers` | the middle visibility level | `C-RL-20` |
| `Kit Bramwell` | the subscriber's display name | `C-RL-21` |
| `subscriber` | the paid plan value | `C-RL-21` |
| `uploads/{athlete_id}/{upload_id}/{sha256_of_bytes}.{ext}` | the raw-upload object key scheme | `C-TR-07` |
| `streams/{activity_id}/{stream_type}.json` | the decoded-series object key scheme | `C-TR-08` |
| `Ridgeway Climb` | the seeded segment | `C-DM-26` |
| `ride` | the seeded segment's activity type | `C-DM-26` |
| `1800` | the seeded segment length in metres | `C-DM-26` |
| `95` | the seeded segment elevation gain in metres | `C-DM-26` |
| `30` | the seeded corridor tolerance in metres | `C-DM-27` |
| `400` | the seeded privacy-zone radius in metres | `C-DM-28` |
| `Ridgeway long loop` | the reference activity | `C-DM-29` |
| `5400` | the reference elapsed time in seconds | `C-DM-29` |
| `4200` | the reference moving time in seconds | `C-DM-30` |
| `1200` | the reference stationary period in seconds | `C-DM-30` |
| `32000` | the reference distance in metres | `C-DM-31` |
| `480` | the reference elevation gain in metres | `C-DM-32` |
| `3` | the fixture sample rate in seconds, also the aggregate athlete floor | `C-DM-33` |
| `10000` | the eastward fixture length in metres | `C-DM-34` |
| `55` | the eastward fixture latitude in degrees | `C-DM-34` |
| `10` | the flat-route elevation ceiling in metres | `C-DM-35` |
| `4:00` | the first pace-fixture kilometre | `C-DM-36` |
| `6:00` | the second pace-fixture kilometre | `C-DM-36` |
| `5:00` | the pace-fixture average | `C-DM-36` |
| `Dawn Patrol` | the seeded club | `C-DM-37` |
| `April Ascent` | the seeded challenge | `C-DM-38` |
| `elevation` | the seeded challenge metric | `C-DM-38` |
| `4000` | the seeded challenge target in metres | `C-DM-38` |
| `Loch Circuit` | the seeded route | `C-DM-39` |
| `24000` | the seeded route distance in metres | `C-DM-39` |
| `310` | the seeded route elevation gain in metres | `C-DM-39` |
| `Free` | the first plan | `C-DM-40` |
| `Ridgeline Premium` | the second plan | `C-DM-40` |
| `8000` | the second plan annual price in minor units | `C-DM-40` |
| `Sena Okafor` | the accepted follower's display name | `C-DM-44` |
| `accepted` | the granted follow state | `C-DM-44` |
| `Community-Powered Motivation` | the signup heading | `C-FE-10` |
| `Sign Up With Google` | the first federated signup control | `C-FE-11` |
| `Sign Up With Apple` | the second federated signup control | `C-FE-11` |
| `Sign Up With Email` | the emphasised signup control | `C-FE-11` |
| `Log In` | the log-in heading | `C-FE-13` |
| `or` | the log-in divider | `C-FE-13` |
| `Email` | the log-in field label | `C-FE-14` |
| `Your Email` | the log-in field placeholder | `C-FE-14` |
| `${APP_PUBLIC_PORT}:4173` |  | `C-DC-02` |
| `4173` |  | `C-DC-02` |
| `/app/USER_README.md` | where the seeded logins are written | `C-DC-07` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-08` |
| `.downloads/` | the reserved download directory | `C-DC-08` |

---

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 13 | 13 |
| User roles | 22 | 22 |
| Core features | 142 | 142 |
| User flow | 25 | 25 |
| UI and UX notes | 34 | 34 |
| Technical requirements | 40 | 40 |
| Data model | 44 | 44 |
| Front-end specification | 35 | 35 |
| Constraints | 8 | 8 |
| Deployment contract | 21 | 21 |
