# Checklist: Meridian Instrument Portfolio Console

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, contract
Sections absent: buildplan
Items: 335
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app presents one portfolio console whose public content is written by a signed-in owner. `src: Overview para 2`
- [ ] `C-OV-02` `capability` The app keeps an unpublished work entry out of every public read. `src: Overview para 3`
- [ ] `C-OV-03` `capability` The app keeps an unpublished work entry at the shelf position its owner left. `src: Overview para 3`
- [ ] `C-OV-04` `constraint` The app offers no public sign-up form. `src: Overview para 4`
- [ ] `C-OV-05` `constraint` The app offers no search on the public console. `src: Overview para 4`
- [ ] `C-OV-06` `constraint` The app offers no recognition editor. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor steers the console between five destinations with no session. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor opens a published work dossier. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A visitor sends one message from the contact form. `src: User roles table row 1`
- [ ] `C-RL-04` `constraint` A visitor reaches no route under `/studio`. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` A visitor reads no message. `src: User roles table row 1`
- [ ] `C-RL-06` `role` An editor signs in, then reads every work entry, drafts among them. `src: User roles table row 2`
- [ ] `C-RL-07` `role` An editor creates a work entry. `src: User roles table row 2`
- [ ] `C-RL-08` `role` An editor edits a work entry. `src: User roles table row 2`
- [ ] `C-RL-09` `constraint` An editor publishes no work entry. `src: User roles table row 2`
- [ ] `C-RL-10` `constraint` An editor unpublishes no work entry. `src: User roles table row 2`
- [ ] `C-RL-11` `constraint` An editor deletes no work entry. `src: User roles table row 2`
- [ ] `C-RL-12` `constraint` An editor reorders no shelf. `src: User roles table row 2`
- [ ] `C-RL-13` `constraint` An editor reads no message. `src: User roles table row 2`
- [ ] `C-RL-14` `constraint` An editor sees no unread count, a zero among them. `src: User roles table row 2`
- [ ] `C-RL-15` `constraint` An editor reads no page-view log. `src: User roles table row 2`
- [ ] `C-RL-16` `role` An owner publishes a work entry. `src: User roles table row 3`
- [ ] `C-RL-17` `role` An owner reorders the shelf. `src: User roles table row 3`
- [ ] `C-RL-18` `role` An owner reads the inbox. `src: User roles table row 3`
- [ ] `C-RL-19` `role` An owner invites an editor by address. `src: User roles para on invitation`
- [ ] `C-RL-20` `contract` The app rejects a direct API call from an editor session to an owner-only endpoint at the server. `src: User roles authorization paragraph`
- [ ] `C-RL-21` `contract` The app leaves the protected state unchanged after rejecting an editor call to an owner-only endpoint. `src: User roles authorization paragraph`
- [ ] `C-RL-22` `constraint` Exactly one account holds the owner role. `src: User roles para 2`
- [ ] `C-RL-23` `literal` The app seeds the account `owner@example.com` with the owner role. `src: User roles seeded accounts table`
- [ ] `C-RL-24` `literal` The app seeds the account `editor@example.com` with the editor role. `src: User roles seeded accounts table`
- [ ] `C-RL-25` `literal` The app accepts the password `deku-demo-pw-2026` for every seeded account. `src: User roles seeded accounts table`
- [ ] `C-RL-26` `capability` The app revokes every session an editor holds when the owner removes the editor. `src: User roles para on invitation`
- [ ] `C-RL-27` `capability` The app keeps a removed editor's work entries with the authorship unchanged. `src: User roles para on invitation`

## C-CF Core features

- [ ] `C-CF-01` `literal` The app answers `GET /api/console` with the profile, the published work, the published studies, the published recognitions, the cities. `src: Core features rule 1`
- [ ] `C-CF-02` `constraint` The app requires no session on the console read. `src: Core features rule 1`
- [ ] `C-CF-03` `capability` The app orders every list in the console read by shelf position. `src: Core features rule 1`
- [ ] `C-CF-04` `capability` The app makes no further request after the console read when a destination changes. `src: Core features rule 1`
- [ ] `C-CF-05` `capability` The app reloads no document when a destination changes. `src: Core features rule 1`
- [ ] `C-CF-06` `capability` The app keeps one drawing surface in place across every destination change. `src: Core features rule 2`
- [ ] `C-CF-07` `ui` The app fills the home destination with a point-built portrait, a drifting letter field, a biography panel, three callout annotations. `src: Core features rule 3`
- [ ] `C-CF-08` `ui` The app fills the work destination with work cards over a wireframe landscape carrying moving markers, trails, a travelling pulse ring. `src: Core features rule 3`
- [ ] `C-CF-09` `ui` The app fills the studies destination with a contour field carrying a selector at the bottom centre. `src: Core features rule 3`
- [ ] `C-CF-10` `literal` The app labels the studies selector items `01`, `02`, `03`, zero-padded to two digits. `src: Core features rule 3`
- [ ] `C-CF-11` `ui` The app fills the recognition destination with a point-built globe, city markers, a target reticle, the dated rows at the right. `src: Core features rule 3`
- [ ] `C-CF-12` `ui` The app fills the contact destination with three oversized wire letters under a panel carrying the message form. `src: Core features rule 3`
- [ ] `C-CF-13` `constraint` The app scrolls no public destination at any window size. `src: Core features rule 4`
- [ ] `C-CF-14` `ui` The app enlarges the interface rather than cropping when the window is short, up to a clamp. `src: Core features rule 4`
- [ ] `C-CF-15` `ui` The app draws the navigation diagram in the upper right as the only navigation the public console has. `src: Core features rule 5`
- [ ] `C-CF-16` `ui` The app settles the navigation plates to different positions on every destination. `src: Core features rule 5`
- [ ] `C-CF-17` `ui` The app moves the four child plates at twice the speed of the parent plate. `src: Core features rule 5`
- [ ] `C-CF-18` `capability` The app maintains a parallel structure carrying every string the scene draws, in reading order. `src: Core features rule 6`
- [ ] `C-CF-19` `capability` The app places the parallel structure immediately before the drawing surface. `src: Core features rule 6`
- [ ] `C-CF-20` `capability` The app keeps the parallel structure fully in the tab order. `src: Core features rule 6`
- [ ] `C-CF-21` `capability` The app replaces the parallel structure entirely on a destination change. `src: Core features rule 6`
- [ ] `C-CF-22` `literal` The app exposes the wordmark `MARLOW HENDRIKS` on every destination. `src: Core features rule 7`
- [ ] `C-CF-23` `literal` The app renders the footer line `COPYRIGHT 2026 MARLOW HENDRIKS. ALL RIGHTS RESERVED.` `src: Core features rule 7`
- [ ] `C-CF-24` `literal` The app answers `POST /api/auth/login` with an `access_token` for a correct address with a correct password. `src: Core features rule 8`
- [ ] `C-CF-25` `contract` The app sets an opaque session cookie no script can read on a successful sign-in. `src: Core features rule 8`
- [ ] `C-CF-26` `literal` The app expires a session `30` days from issue. `src: Core features rule 8`
- [ ] `C-CF-27` `literal` The app ends a session after `14` days without a request. `src: Core features rule 8`
- [ ] `C-CF-28` `contract` The app resolves a session to an account at the server, never from the request body. `src: Core features rule 8`
- [ ] `C-CF-29` `literal` The app answers a wrong password with the pinned sign-in failure sentence. `src: Core features rule 9`
- [ ] `C-CF-30` `constraint` The app names neither field as the wrong one on a failed sign-in. `src: Core features rule 9`
- [ ] `C-CF-31` `literal` The app locks an account for `15` minutes after `5` consecutive failed sign-ins. `src: Core features rule 10`
- [ ] `C-CF-32` `literal` The app answers a locked account with the pinned lockout sentence. `src: Core features rule 10`
- [ ] `C-CF-33` `capability` The app sends a signed-out request for a studio route to the sign-in route carrying the intended path. `src: Core features rule 11`
- [ ] `C-CF-34` `capability` The app sends the visitor onward to the intended path after a successful sign-in. `src: Core features rule 11`
- [ ] `C-CF-35` `constraint` The app discards an intended path beginning with two solidi, then lands the visitor on the dashboard. `src: Core features rule 11`
- [ ] `C-CF-36` `literal` The app bounds a work entry title at `1` to `120` characters after trimming. `src: Core features rule 12`
- [ ] `C-CF-37` `literal` The app bounds a work entry kind at `0` to `60` characters. `src: Core features rule 12`
- [ ] `C-CF-38` `literal` The app bounds a work entry year at `1970` to `2026`. `src: Core features rule 12`
- [ ] `C-CF-39` `literal` The app bounds a work entry summary at `0` to `280` characters. `src: Core features rule 12`
- [ ] `C-CF-40` `literal` The app bounds a work entry body at `0` to `8000` characters. `src: Core features rule 12`
- [ ] `C-CF-41` `literal` The app bounds a work entry grid seed at `0` to `999999`. `src: Core features rule 12`
- [ ] `C-CF-42` `literal` The app restricts a grid palette to `neutral`, `blue`, `coral`. `src: Core features rule 12`
- [ ] `C-CF-43` `literal` The app bounds a work entry at four links, each with a label of `1` to `40` characters. `src: Core features rule 12`
- [ ] `C-CF-44` `constraint` The app requires a link address that parses, beginning with a secure scheme. `src: Core features rule 12`
- [ ] `C-CF-45` `literal` The app refuses a missing title inline with `Give the entry a title.` `src: Core features rule 13`
- [ ] `C-CF-46` `literal` The app refuses an over-long kind inline with the pinned over-long-kind sentence. `src: Core features rule 13`
- [ ] `C-CF-47` `literal` The app refuses a year outside the band inline with `Use a four digit year up to 2026.` `src: Core features rule 13`
- [ ] `C-CF-48` `literal` The app refuses an over-long summary inline with `Keep the summary under 280 characters.` `src: Core features rule 13`
- [ ] `C-CF-49` `literal` The app refuses an over-long body inline with the pinned over-long-body sentence. `src: Core features rule 13`
- [ ] `C-CF-50` `literal` The app refuses a seed outside the band inline with `Use a whole number up to 999999.` `src: Core features rule 13`
- [ ] `C-CF-51` `literal` The app refuses a bad link inline with the pinned link sentence. `src: Core features rule 13`
- [ ] `C-CF-52` `constraint` The app writes nothing when a field constraint refuses the form. `src: Core features rule 13`
- [ ] `C-CF-53` `constraint` The app disables no submit control anywhere. `src: Core features rule 14`
- [ ] `C-CF-54` `ui` The app shows every error at once when a submit control is pressed on an invalid form. `src: Core features rule 14`
- [ ] `C-CF-55` `constraint` The app clears no form on a failure of any kind. `src: Core features rule 15`
- [ ] `C-CF-56` `contract` The app carries the version a work entry write was made from. `src: Core features rule 16`
- [ ] `C-CF-57` `contract` The app refuses a work entry write made from a version no longer current. `src: Core features rule 16`
- [ ] `C-CF-58` `literal` The app answers a refused stale write with the pinned conflict sentence. `src: Core features rule 16`
- [ ] `C-CF-59` `literal` The app offers two named controls on a refused stale write. `src: Core features rule 16`
- [ ] `C-CF-60` `contract` The app raises a work entry version by one on an accepted write. `src: Core features rule 16`
- [ ] `C-CF-61` `capability` The app writes a new work entry unpublished at the position at the end of the shelf. `src: Core features rule 17`
- [ ] `C-CF-62` `literal` The app answers a save with the pinned save banner sentence. `src: Core features rule 17`
- [ ] `C-CF-63` `constraint` The app permits publishing to an owner only. `src: Core features rule 17`
- [ ] `C-CF-64` `literal` The app answers a publish with the pinned publish banner sentence. `src: Core features rule 18`
- [ ] `C-CF-65` `literal` The app answers an unpublish with the pinned unpublish banner sentence. `src: Core features rule 18`
- [ ] `C-CF-66` `capability` The app places a published entry in the card row at its shelf position. `src: Core features rule 18`
- [ ] `C-CF-67` `constraint` The app omits an unpublished work entry from the console read. `src: Core features rule 19`
- [ ] `C-CF-68` `constraint` The app omits an unpublished work entry from the paging indicator. `src: Core features rule 19`
- [ ] `C-CF-69` `literal` The app answers `GET /api/work/{id}` for an unpublished entry as gone. `src: Core features rule 19`
- [ ] `C-CF-70` `literal` The app writes a work entry preview image to the bucket under the key scheme `previews/{entry_id}/{sha256_of_bytes}.png`. `src: Core features rule 20`
- [ ] `C-CF-71` `constraint` The app keeps preview bytes out of the app container filesystem. `src: Core features rule 20`
- [ ] `C-CF-72` `constraint` The app keeps preview bytes out of any database column. `src: Core features rule 20`
- [ ] `C-CF-73` `capability` The app serves a published entry preview image to a visitor with no session. `src: Core features rule 21`
- [ ] `C-CF-74` `constraint` The app denies an unauthenticated request for an unpublished entry preview image at its exact key. `src: Core features rule 21`
- [ ] `C-CF-75` `capability` The app produces the same preview bytes from the same seed with the same palette. `src: Core features rule 21`
- [ ] `C-CF-76` `capability` The app regenerates the preview image when the grid seed changes. `src: Core features rule 22`
- [ ] `C-CF-77` `capability` The app regenerates the preview image when the grid palette changes. `src: Core features rule 22`
- [ ] `C-CF-78` `capability` The app holds the work order beside the study order on one shelf page. `src: Core features rule 23`
- [ ] `C-CF-79` `constraint` The app permits a shelf read to an owner only. `src: Core features rule 23`
- [ ] `C-CF-80` `constraint` The app permits a shelf write to an owner only. `src: Core features rule 23`
- [ ] `C-CF-81` `ui` The app moves a shelf row by pointer drag from a six-dot handle at the row left. `src: Core features rule 24`
- [ ] `C-CF-82` `ui` The app lifts a focused shelf handle on the space key, then moves the row on the arrow keys. `src: Core features rule 24`
- [ ] `C-CF-83` `ui` The app commits a keyboard move on the space key, cancelling on the escape key. `src: Core features rule 24`
- [ ] `C-CF-84` `capability` The app writes the same order from the keyboard path as from the pointer path. `src: Core features rule 24`
- [ ] `C-CF-85` `contract` The app writes every affected shelf position in one transaction. `src: Core features rule 25`
- [ ] `C-CF-86` `literal` The app answers a committed order with the pinned order banner sentence. `src: Core features rule 25`
- [ ] `C-CF-87` `constraint` The app refuses a whole reorder naming an entry that does not exist. `src: Core features rule 25`
- [ ] `C-CF-88` `constraint` The app refuses a whole reorder naming one entry twice. `src: Core features rule 25`
- [ ] `C-CF-89` `constraint` The app writes no partial shelf order. `src: Core features rule 25`
- [ ] `C-CF-90` `data` The app keeps shelf positions dense from zero, unique across every entry. `src: Core features rule 26`
- [ ] `C-CF-91` `capability` The app skips an unpublished entry when building the public list. `src: Core features rule 26`
- [ ] `C-CF-92` `ui` The app re-settles every visible two-digit position label when an order is committed. `src: Core features rule 27`
- [ ] `C-CF-93` `literal` The app bounds a message sender name at `1` to `80` characters after trimming. `src: Core features rule 28`
- [ ] `C-CF-94` `literal` The app bounds a message sender address at `1` to `254` characters. `src: Core features rule 28`
- [ ] `C-CF-95` `literal` The app bounds a message body at `10` to `4000` characters after trimming. `src: Core features rule 28`
- [ ] `C-CF-96` `literal` The app refuses a missing sender name inline with `Tell me what to call you.` `src: Core features rule 28`
- [ ] `C-CF-97` `literal` The app refuses a malformed address inline with the pinned address sentence. `src: Core features rule 28`
- [ ] `C-CF-98` `literal` The app refuses a short message inline with `A few more words, please.` `src: Core features rule 28`
- [ ] `C-CF-99` `literal` The app answers a sent message with the pinned sent banner sentence. `src: Core features rule 29`
- [ ] `C-CF-100` `ui` The app clears all three contact fields after a sent message. `src: Core features rule 29`
- [ ] `C-CF-101` `literal` The app answers a refused message with the pinned failed-send sentence. `src: Core features rule 29`
- [ ] `C-CF-102` `constraint` The app refuses a contact submission whose decoy field is filled. `src: Core features rule 30`
- [ ] `C-CF-103` `literal` The app refuses a contact submission made under `2` seconds after the form was built. `src: Core features rule 30`
- [ ] `C-CF-104` `literal` The app refuses a message body carrying more than `2` addresses. `src: Core features rule 30`
- [ ] `C-CF-105` `literal` The app refuses a fourth message from one address inside `1` hour. `src: Core features rule 30`
- [ ] `C-CF-106` `constraint` The app writes no message when a contact submission is refused. `src: Core features rule 30`
- [ ] `C-CF-107` `constraint` The app presents no puzzle, no image challenge, no third-party gate on the contact form. `src: Core features rule 30`
- [ ] `C-CF-108` `data` The app stores a message with the sender name, the sender address, the body, the state, the source route, the arrival moment. `src: Core features rule 31`
- [ ] `C-CF-109` `literal` The app restricts a message state to `unread`, `read`, `archived`. `src: Core features rule 31`
- [ ] `C-CF-110` `capability` The app lists messages newest first. `src: Core features rule 31`
- [ ] `C-CF-111` `constraint` The app permits reading a message to an owner only. `src: Core features rule 31`
- [ ] `C-CF-112` `contract` The app renders a message body as text everywhere the body appears. `src: Core features rule 32`
- [ ] `C-CF-113` `constraint` The app interprets no markup in a message body. `src: Core features rule 32`
- [ ] `C-CF-114` `constraint` The app makes no address in a message body into a link. `src: Core features rule 32`
- [ ] `C-CF-115` `literal` The app marks an open message read after `1` second on screen. `src: Core features rule 33`
- [ ] `C-CF-116` `literal` The app offers the controls `ARCHIVE`, `MARK UNREAD`, `DELETE` on one message. `src: Core features rule 33`
- [ ] `C-CF-117` `literal` The app renders an unknown address as `404 NOT FOUND` on the failure route. `src: Core features rule 34`
- [ ] `C-CF-118` `literal` The app offers the control `RETURN HOME` on the not-found surface. `src: Core features rule 34`
- [ ] `C-CF-119` `contract` The app answers an unknown address as not found rather than as a success. `src: Core features rule 34`
- [ ] `C-CF-120` `contract` The app matches a failure code against its closed table before rendering. `src: Core features rule 35`
- [ ] `C-CF-121` `literal` The app renders a code outside the closed table as `500 SOMETHING BROKE`. `src: Core features rule 35`
- [ ] `C-CF-122` `constraint` The app echoes no message from the address on the failure surface. `src: Core features rule 35`
- [ ] `C-CF-123` `literal` The app renders an editor reaching an owner-only surface as `403 NOT PERMITTED`. `src: Core features rule 36`
- [ ] `C-CF-124` `literal` The app explains an inbox refusal with the pinned refusal sentence. `src: Core features rule 36`
- [ ] `C-CF-125` `literal` The app offers the control `BACK TO WORK` on a refusal surface. `src: Core features rule 36`
- [ ] `C-CF-126` `ui` The app keeps the rail present on a refusal surface, with the refused item absent. `src: Core features rule 36`
- [ ] `C-CF-127` `constraint` The app omits the unread tile entirely for an editor. `src: Core features rule 36`
- [ ] `C-CF-128` `data` The app records a public destination view with the route, with the moment. `src: Core features rule 37`
- [ ] `C-CF-129` `literal` The app lists page views newest first at `GET /api/studio/page-views`. `src: Core features rule 37`
- [ ] `C-CF-130` `constraint` The app records no full network address in a page view. `src: Core features rule 37`
- [ ] `C-CF-131` `constraint` The app denies an editor requesting the page-view log. `src: Core features rule 37`
- [ ] `C-CF-132` `ui` The app shows a loading counter reading three digits with a percent sign before a first scene. `src: Core features rule 38`
- [ ] `C-CF-133` `ui` The app draws the loading counter digits on a fixed pitch. `src: Core features rule 38`
- [ ] `C-CF-134` `ui` The app hands over from the loading surface to the scene by a fade. `src: Core features rule 39`
- [ ] `C-CF-135` `ui` The app returns the navigation diagram with the footer last after a handover. `src: Core features rule 39`
- [ ] `C-CF-136` `literal` The app holds a placeholder on screen at least `500` milliseconds. `src: Core features rule 40`
- [ ] `C-CF-137` `constraint` The app speaks only the sentences the brief pins, inventing none. `src: Core features rule 41`
- [ ] `C-CF-138` `constraint` The app writes no exclamation mark outside the crash surface. `src: Core features rule 41`
- [ ] `C-CF-139` `constraint` The app writes no typographic dash in any string. `src: Core features rule 41`

## C-UF User flow

- [ ] `C-UF-01` `contract` The app serves the home destination at `/` to a visitor with no session. `src: User flow route table`
- [ ] `C-UF-02` `contract` The app serves the work destination at `/product` to a visitor with no session. `src: User flow route table`
- [ ] `C-UF-03` `contract` The app serves the studies destination at `/sketch` to a visitor with no session. `src: User flow route table`
- [ ] `C-UF-04` `contract` The app serves one selected study at `/sketch/<id>`. `src: User flow route table`
- [ ] `C-UF-05` `contract` The app serves the recognition destination at `/award` to a visitor with no session. `src: User flow route table`
- [ ] `C-UF-06` `contract` The app serves the contact destination at `/contact` to a visitor with no session. `src: User flow route table`
- [ ] `C-UF-07` `contract` The app serves the failure surface at `/error`. `src: User flow route table`
- [ ] `C-UF-08` `contract` The app serves sign-in at `/sign-in` to a signed-out visitor only. `src: User flow route table`
- [ ] `C-UF-09` `contract` The app serves an invitation at `/invite/<token>` to a signed-out visitor only. `src: User flow route table`
- [ ] `C-UF-10` `contract` The app serves the dashboard at `/studio` to an owner, to an editor. `src: User flow route table`
- [ ] `C-UF-11` `contract` The app serves the entry list at `/studio/work` to an owner, to an editor. `src: User flow route table`
- [ ] `C-UF-12` `contract` The app serves an empty entry editor at `/studio/work/new`. `src: User flow route table`
- [ ] `C-UF-13` `contract` The app serves the shelf at `/studio/shelf` to an owner only. `src: User flow route table`
- [ ] `C-UF-14` `contract` The app serves the inbox at `/studio/inbox` to an owner only. `src: User flow route table`
- [ ] `C-UF-15` `contract` The app serves the account page at `/studio/account` to an owner, to an editor. `src: User flow route table`
- [ ] `C-UF-16` `contract` The app serves the page-view log at `/studio/log` to an owner only. `src: User flow route table`
- [ ] `C-UF-17` `capability` The app lands a signed-in visitor asking for sign-in on the dashboard. `src: User flow entry and redirects`
- [ ] `C-UF-18` `capability` The app ends the current session on sign out, then lands the visitor on the home destination. `src: User flow entry and redirects`
- [ ] `C-UF-19` `capability` The app preserves an open form when a session expires part way through an edit. `src: User flow entry and redirects`
- [ ] `C-UF-20` `ui` The app shows a loading state on every list. `src: User flow states`
- [ ] `C-UF-21` `ui` The app shows an empty state on every list. `src: User flow states`
- [ ] `C-UF-22` `ui` The app shows an error state on every list. `src: User flow states`
- [ ] `C-UF-23` `literal` The app shows the empty entry list as `Nothing here yet.` `src: User flow states`
- [ ] `C-UF-24` `literal` The app shows the empty shelf as `Nothing on the shelf yet.` `src: User flow states`
- [ ] `C-UF-25` `literal` The app shows a one-entry shelf with the pinned single-entry sentence. `src: User flow states`
- [ ] `C-UF-26` `literal` The app shows the empty inbox as `No messages.` `src: User flow states`
- [ ] `C-UF-27` `literal` The app shows the pinned inbox secondary sentence under the empty inbox line. `src: User flow states`
- [ ] `C-UF-28` `literal` The app shows the empty page-view log as `Nothing recorded yet.` `src: User flow states`
- [ ] `C-UF-29` `literal` The app labels an empty card row `Work coming soon.` `src: User flow states`
- [ ] `C-UF-30` `literal` The app labels an empty recognition list `Recognition coming soon.` `src: User flow states`
- [ ] `C-UF-31` `literal` The app shows a failed list load as `That did not load.` `src: User flow states`
- [ ] `C-UF-32` `constraint` The app crashes on no error. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app grounds every destination in a near-black neutral. `src: UI/UX notes palette`
- [ ] `C-UX-02` `ui` The app draws every scene string in a near-white neutral. `src: UI/UX notes palette`
- [ ] `C-UX-03` `ui` The app draws page-furniture text in a second near-white neutral, never swapping the two jobs. `src: UI/UX notes palette`
- [ ] `C-UX-04` `ui` The app draws every connector, bracket, marker in a light neutral. `src: UI/UX notes palette`
- [ ] `C-UX-05` `ui` The app draws the moving terrain markers in a light, soft red used nowhere else. `src: UI/UX notes palette`
- [ ] `C-UX-06` `ui` The app draws the letter field behind the portrait as a five-step blue ramp. `src: UI/UX notes palette`
- [ ] `C-UX-07` `ui` The app draws the shelf published marker in a deep, muted green used nowhere else. `src: UI/UX notes palette`
- [ ] `C-UX-08` `ui` The app draws every error in one soft warm red used nowhere but errors, the delete label. `src: UI/UX notes palette`
- [ ] `C-UX-09` `constraint` The app shows no vivid red, no vivid violet, no vivid amber on any surface. `src: UI/UX notes palette`
- [ ] `C-UX-10` `ui` The app sets every string in the declared technical sans family stack. `src: UI/UX notes type`
- [ ] `C-UX-11` `ui` The app renders correctly on the fallback family alone. `src: UI/UX notes type`
- [ ] `C-UX-12` `ui` The app eases every entrance, every exit, looping nothing. `src: UI/UX notes motion`
- [ ] `C-UX-13` `ui` The app resolves an arriving string from substitute characters into its own glyphs. `src: UI/UX notes motion`
- [ ] `C-UX-14` `ui` The app enters a control fill from the edge the pointer crossed. `src: UI/UX notes motion`
- [ ] `C-UX-15` `ui` The app parts the rows around a lifted shelf row to show the landing place. `src: UI/UX notes motion`
- [ ] `C-UX-16` `constraint` The app animates no placeholder. `src: UI/UX notes motion`
- [ ] `C-UX-17` `ui` The app substitutes a reduced-motion path landing the same end state without the transit. `src: UI/UX notes motion`
- [ ] `C-UX-18` `ui` The app meets the WCAG AA contrast bar on body text against its ground. `src: UI/UX notes accessibility`
- [ ] `C-UX-19` `ui` The app meets the WCAG AA contrast bar on every half-strength secondary line. `src: UI/UX notes accessibility`
- [ ] `C-UX-20` `constraint` The app carries meaning by more than colour on the shelf published marker. `src: UI/UX notes accessibility`
- [ ] `C-UX-21` `ui` The app shows a visible focus ring on every focusable thing. `src: UI/UX notes accessibility`
- [ ] `C-UX-22` `constraint` The app removes a focus ring in no state. `src: UI/UX notes accessibility`
- [ ] `C-UX-23` `ui` The app labels every icon-only control. `src: UI/UX notes accessibility`
- [ ] `C-UX-24` `ui` The app orders focus as the skip link, the destination region, the five destinations, the destination controls, the information control, the source link, the sound control. `src: UI/UX notes accessibility`
- [ ] `C-UX-25` `ui` The app keeps one arrangement between any two wide sizes, changing the size alone. `src: UI/UX notes responsive`
- [ ] `C-UX-26` `ui` The app renders the contact surface as ordinary page furniture below the breakpoint. `src: UI/UX notes responsive`
- [ ] `C-UX-27` `constraint` The app overflows nothing sideways at a narrow viewport. `src: UI/UX notes responsive`
- [ ] `C-UX-28` `ui` The app moves the entry editor preview panel above the fields at the narrow width. `src: UI/UX notes responsive`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app serves a single-page application against a JSON API on one origin. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The app reads its database connection from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The app reaches the object store at `STORAGE_ENDPOINT`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The app reads its bucket name from `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The app reads its object-store credentials from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The app stores a password only as a memory-hard hash. `src: Technical requirements para 1`
- [ ] `C-TR-07` `constraint` The app returns a password hash from no endpoint. `src: Technical requirements para 1`
- [ ] `C-TR-08` `contract` The app answers `GET /api/health` with status `200` once ready. `src: Technical requirements para 1`
- [ ] `C-TR-09` `contract` The app writes one structured log line per request to standard output. `src: Technical requirements para 1`
- [ ] `C-TR-10` `constraint` The app writes no full network address into a log line. `src: Technical requirements para 1`
- [ ] `C-TR-11` `constraint` The app introduces no second database, no cache, no queue, no second object store, no identity provider, no mail vendor. `src: Technical requirements para 2`
- [ ] `C-TR-12` `constraint` The app starts no copy of `postgres`, of `minio`. `src: Technical requirements para 2`
- [ ] `C-TR-13` `constraint` The app hardcodes no host, no port. `src: Technical requirements para 2`
- [ ] `C-TR-14` `capability` The app holds one drawing surface at the full window size across every destination change. `src: Technical requirements para 3`
- [ ] `C-TR-15` `capability` The app draws its scene text as geometry rather than as page text. `src: Technical requirements para 3`
- [ ] `C-TR-16` `capability` The app composites at least three post-processing passes over the rendered scene. `src: Technical requirements para 4`
- [ ] `C-TR-17` `capability` The app generates a signed distance field for text at run time. `src: Technical requirements para 4`
- [ ] `C-TR-18` `capability` The app resizes without reallocating the scene. `src: Technical requirements para 4`
- [ ] `C-TR-19` `capability` The app loads the studio surface separately from the console surface. `src: Technical requirements module separation`
- [ ] `C-TR-20` `capability` The app degrades one tier at a time when the frame rate falls. `src: Technical requirements performance`
- [ ] `C-TR-21` `constraint` The app degrades the parallel structure never. `src: Technical requirements performance`
- [ ] `C-TR-22` `contract` The app carries a strict transport policy on every response. `src: Technical requirements security header set`
- [ ] `C-TR-23` `contract` The app carries a nosniff content-type policy on every response. `src: Technical requirements security header set`
- [ ] `C-TR-24` `contract` The app carries a frame-denial policy on every response. `src: Technical requirements security header set`
- [ ] `C-TR-25` `contract` The app carries a same-origin referrer policy on every response. `src: Technical requirements security header set`
- [ ] `C-TR-26` `contract` The app marks the session cookie secure, same-site strict, unreadable by scripts. `src: Technical requirements security header set`
- [ ] `C-TR-27` `contract` The app declares a distinct title on every public destination. `src: Technical requirements social preview`
- [ ] `C-TR-28` `contract` The app declares a social preview title with a preview image on every public destination. `src: Technical requirements social preview`
- [ ] `C-TR-29` `contract` The app serves bytes for every declared preview image. `src: Technical requirements social preview`
- [ ] `C-TR-30` `constraint` The app exposes no credential, no access key, no session token in anything the browser downloads. `src: Technical requirements final para`
- [ ] `C-TR-31` `constraint` The app downloads no image file, no audio file, no scene binary, no font file from its own origin. `src: Technical requirements zero-asset rule`

## C-DM Data model

- [ ] `C-DM-01` `data` The app keeps an accounts table carrying a unique lowercased address. `src: Data model accounts`
- [ ] `C-DM-02` `data` The app keeps a sessions table storing a token hash rather than the cookie value. `src: Data model sessions`
- [ ] `C-DM-03` `data` The app keeps exactly one profile row. `src: Data model profile`
- [ ] `C-DM-04` `data` The app keeps a work entries table carrying a position, a published flag, a preview key, a version. `src: Data model work_entries`
- [ ] `C-DM-05` `data` The app keeps an entry links table bounded at four rows per entry. `src: Data model entry_links`
- [ ] `C-DM-06` `data` The app keeps a studies table carrying a field seed with a position. `src: Data model studies`
- [ ] `C-DM-07` `data` The app keeps a recognitions table naming exactly one city per row. `src: Data model recognitions`
- [ ] `C-DM-08` `data` The app keeps a cities table carrying a coordinate pair. `src: Data model cities`
- [ ] `C-DM-09` `data` The app keeps a messages table carrying a state with a source route. `src: Data model messages`
- [ ] `C-DM-10` `data` The app keeps a page views table carrying a route with a moment, nothing else. `src: Data model page_views`
- [ ] `C-DM-11` `data` The app stores every timestamp in UTC. `src: Data model opening line`
- [ ] `C-DM-12` `contract` The app accepts exactly one of two writes to one entry made from the same version. `src: Data model invariants`
- [ ] `C-DM-13` `contract` The app stores exactly one whole order when two reorders arrive at once. `src: Data model invariants`
- [ ] `C-DM-14` `literal` The app seeds the study `Ridge Survey` published at the first position. `src: Data model seed data`
- [ ] `C-DM-15` `literal` The app seeds the study `Tide Table` published at the second position. `src: Data model seed data`
- [ ] `C-DM-16` `literal` The app seeds the study `Lantern Field` published at the third position. `src: Data model seed data`
- [ ] `C-DM-17` `literal` The app seeds the recognition `Northlight Prize` in the city `Oslo`. `src: Data model seed data`
- [ ] `C-DM-18` `literal` The app seeds the recognition `Meridian Review` in the city `Lisbon`. `src: Data model seed data`
- [ ] `C-DM-19` `literal` The app seeds the recognition `Halden Biennale` in the city `Kyoto`. `src: Data model seed data`
- [ ] `C-DM-20` `literal` The app seeds the profile full name `MARLOW HENDRIKS`. `src: Data model seed data`
- [ ] `C-DM-21` `constraint` The app seeds no work entry. `src: Data model seed data`
- [ ] `C-DM-22` `constraint` The app seeds no message. `src: Data model seed data`
- [ ] `C-DM-23` `contract` The app duplicates no row when the app restarts. `src: Data model closing line`
- [ ] `C-DM-24` `contract` The app writes the seeded credentials into `/app/USER_README.md`. `src: Data model password paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app sets annotation bodies at `11px` on a line box of `13.2px`. `src: Front-end specification type ramp`
- [ ] `C-FE-02` `ui` The app sets inline errors at `11px` on a line box of `13.2px`. `src: Front-end specification type ramp`
- [ ] `C-FE-03` `ui` The app sets footer copy at `12px` on a line box of `14.4px`. `src: Front-end specification type ramp`
- [ ] `C-FE-04` `ui` The app sets field labels at `12px` on a line box of `12px`. `src: Front-end specification type ramp`
- [ ] `C-FE-05` `ui` The app sets the status banner at `12px` on a line box of `15.6px`. `src: Front-end specification type ramp`
- [ ] `C-FE-06` `ui` The app sets input text at `16px` on a line box of `22.4px`. `src: Front-end specification type ramp`
- [ ] `C-FE-07` `ui` The app sets the wordmark at `18px` on a line box of `21.6px`. `src: Front-end specification type ramp`
- [ ] `C-FE-08` `ui` The app sets bracketed controls at `20px` on a line box of `20px`. `src: Front-end specification type ramp`
- [ ] `C-FE-09` `ui` The app sets panel titles at `28px` on a line box of `28px`. `src: Front-end specification type ramp`
- [ ] `C-FE-10` `ui` The app sets a navigation plate label at ten scene units. `src: Front-end specification scene ramp`
- [ ] `C-FE-11` `ui` The app draws seven symbols, no eighth, each on a whole-unit grid. `src: Front-end specification iconography`
- [ ] `C-FE-12` `ui` The app rounds no corner but the circular inbox state dot. `src: Front-end specification radii`
- [ ] `C-FE-13` `ui` The app carries depth by overlap with strength rather than by a drop shadow. `src: Front-end specification depth`
- [ ] `C-FE-14` `ui` The app blurs behind the message panel alone. `src: Front-end specification radii`
- [ ] `C-FE-15` `ui` The app presents base geometry at once, the destination marker next, the annotations last. `src: Front-end specification arrival sequence`
- [ ] `C-FE-16` `ui` The app draws the compass over the terrain when the work destination has anything published. `src: Front-end specification compass`
- [ ] `C-FE-17` `ui` The app fills a shelf row under the pointer, darkening the fill under a drag. `src: Front-end specification shelf interaction`
- [ ] `C-FE-18` `ui` The app snaps a shelf drop position to a row boundary. `src: Front-end specification shelf interaction`
- [ ] `C-FE-19` `constraint` The app writes nothing when the escape key ends a shelf drag. `src: Front-end specification shelf interaction`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app serves one portfolio for one owner, with no second profile. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` The app offers no recognition editor. `src: Constraints para 2`
- [ ] `C-CN-03` `constraint` The app offers no audio bed, no cue, no gain node, no oscillator. `src: Constraints para 2`
- [ ] `C-CN-04` `constraint` The app opens no real-time channel. `src: Constraints para 2`
- [ ] `C-CN-05` `constraint` The app refreshes the unread count on a read rather than on a push. `src: Constraints para 2`
- [ ] `C-CN-06` `constraint` The app offers no data export. `src: Constraints para 2`
- [ ] `C-CN-07` `constraint` The app translates no string, resolving no locale. `src: Constraints para 2`
- [ ] `C-CN-08` `constraint` The app records no event but the page view. `src: Constraints para 2`
- [ ] `C-CN-09` `constraint` The app holds no unsent message offline. `src: Constraints para 2`
- [ ] `C-CN-10` `constraint` The app offers no comment, no like, no follow. `src: Constraints para 2`
- [ ] `C-CN-11` `constraint` The app handles no payment, no price, no currency. `src: Constraints para 2`
- [ ] `C-CN-12` `constraint` The app calls no external service to satisfy a request at run time. `src: Constraints para 3`
- [ ] `C-CN-13` `capability` The app stays responsive at `200` work entries with `5000` messages, `50000` page views. `src: Constraints para 4`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app reads its outside port from `APP_PUBLIC_PORT`, serving container port `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The app serves the HTTP API on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual step. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` The app writes login credentials to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` The app creates an empty `.browser_screenshots/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The app creates an empty `.downloads/` directory at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-09` `contract` The app serves a production build behind a static server, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-10` `contract` The app keeps its server running after the session ends, never as a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-11` `contract` The app binds `0.0.0.0`, never `127.0.0.1`. `src: Deployment contract bullet 9`
- [ ] `C-DC-12` `contract` The app uses no persistent volume, no fixed container name, no custom network. `src: Deployment contract bullet 12`
- [ ] `C-DC-13` `contract` The app answers an invalid request as a client error, never as a server failure. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` The app answers an unauthorized request as a client error, never as a silent success. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `literal` The app carries a `code` from the closed error set on every non-success response. `src: Deployment contract API shapes`
- [ ] `C-DC-16` `contract` The app carries a `fields` map on an unprocessable response alone. `src: Deployment contract API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `owner@example.com` | the seeded owner address | C-RL-23 | User roles seeded accounts table |
| `editor@example.com` | the seeded editor address | C-RL-24 | User roles seeded accounts table |
| `deku-demo-pw-2026` | the password for every seeded account | C-RL-25 | User roles seeded accounts table |
| `GET /api/console` | the one public console read | C-CF-01 | Core features rule 1 |
| `01` | the first studies selector label | C-CF-10 | Core features rule 3 |
| `02` | the second studies selector label | C-CF-10 | Core features rule 3 |
| `03` | the third studies selector label | C-CF-10 | Core features rule 3 |
| `MARLOW HENDRIKS` | the wordmark | C-CF-22 | Core features rule 7 |
| `COPYRIGHT 2026 MARLOW HENDRIKS. ALL RIGHTS RESERVED.` | the footer line | C-CF-23 | Core features rule 7 |
| `POST /api/auth/login` | the sign-in route | C-CF-24 | Core features rule 8 |
| `access_token` | the bearer credential the sign-in returns | C-CF-24 | Core features rule 8 |
| `30` | the session lifetime in days | C-CF-26 | Core features rule 8 |
| `14` | the session idle cap in days | C-CF-27 | Core features rule 8 |
| `That did not match. Check both fields and try again.` | the sign-in failure line | C-CF-29 | Core features rule 9 |
| `5` | the consecutive failures before a lockout | C-CF-31 | Core features rule 10 |
| `15` | the lockout length in minutes | C-CF-31 | Core features rule 10 |
| `Too many attempts. Try again after <time>.` | the lockout line | C-CF-32 | Core features rule 10 |
| `1` | the lower bound on a work entry title | C-CF-36 | Core features rule 12 |
| `120` | the upper bound on a work entry title | C-CF-36 | Core features rule 12 |
| `0` | the lower bound on a work entry kind | C-CF-37 | Core features rule 12 |
| `60` | the upper bound on a work entry kind | C-CF-37 | Core features rule 12 |
| `1970` | the lower bound on a work entry year | C-CF-38 | Core features rule 12 |
| `2026` | the upper bound on a work entry year | C-CF-38 | Core features rule 12 |
| `280` | the upper bound on a work entry summary | C-CF-39 | Core features rule 12 |
| `8000` | the upper bound on a work entry body | C-CF-40 | Core features rule 12 |
| `999999` | the upper bound on a work entry grid seed | C-CF-41 | Core features rule 12 |
| `neutral` | a grid palette value | C-CF-42 | Core features rule 12 |
| `blue` | a grid palette value | C-CF-42 | Core features rule 12 |
| `coral` | a grid palette value | C-CF-42 | Core features rule 12 |
| `40` | the upper bound on a link label | C-CF-43 | Core features rule 12 |
| `Give the entry a title.` | the missing-title error | C-CF-45 | Core features rule 13 |
| `Keep this under 60 characters.` | the over-long kind error | C-CF-46 | Core features rule 13 |
| `Use a four digit year up to 2026.` | the year error | C-CF-47 | Core features rule 13 |
| `Keep the summary under 280 characters.` | the over-long summary error | C-CF-48 | Core features rule 13 |
| `This is longer than the editor will keep.` | the over-long body error | C-CF-49 | Core features rule 13 |
| `Use a whole number up to 999999.` | the grid seed error | C-CF-50 | Core features rule 13 |
| `Give this link a label and a secure address.` | the link error | C-CF-51 | Core features rule 13 |
| `This changed somewhere else while you were working.` | the conflict line | C-CF-58 | Core features rule 16 |
| `KEEP MINE` | the keep-mine control | C-CF-59 | Core features rule 16 |
| `TAKE THEIRS` | the take-theirs control | C-CF-59 | Core features rule 16 |
| `Saved just now.` | the save banner | C-CF-62 | Core features rule 17 |
| `Published. It is on the site now.` | the publish banner | C-CF-64 | Core features rule 18 |
| `Unpublished. It is off the site.` | the unpublish banner | C-CF-65 | Core features rule 18 |
| `GET /api/work/{id}` | the published-entry read | C-CF-69 | Core features rule 19 |
| `previews/{entry_id}/{sha256_of_bytes}.png` | the preview object key scheme | C-CF-70 | Core features rule 20 |
| `Order saved.` | the order banner | C-CF-86 | Core features rule 25 |
| `80` | the upper bound on a sender name | C-CF-93 | Core features rule 28 |
| `254` | the upper bound on a sender address | C-CF-94 | Core features rule 28 |
| `10` | the lower bound on a message body | C-CF-95 | Core features rule 28 |
| `4000` | the upper bound on a message body | C-CF-95 | Core features rule 28 |
| `Tell me what to call you.` | the sender-name error | C-CF-96 | Core features rule 28 |
| `That address will not reach you.` | the address error | C-CF-97 | Core features rule 28 |
| `A few more words, please.` | the short-message error | C-CF-98 | Core features rule 28 |
| `Sent. I will read it.` | the sent banner | C-CF-99 | Core features rule 29 |
| `That did not send. Your text is still here.` | the failed-send banner | C-CF-101 | Core features rule 29 |
| `2` | the seconds floor on a contact submission | C-CF-103 | Core features rule 30 |
| `unread` | a message state | C-CF-109 | Core features rule 31 |
| `read` | a message state | C-CF-109 | Core features rule 31 |
| `archived` | a message state | C-CF-109 | Core features rule 31 |
| `ARCHIVE` | a message control | C-CF-116 | Core features rule 33 |
| `MARK UNREAD` | a message control | C-CF-116 | Core features rule 33 |
| `DELETE` | a message control | C-CF-116 | Core features rule 33 |
| `404 NOT FOUND` | the not-found surface copy | C-CF-117 | Core features rule 34 |
| `RETURN HOME` | the not-found control | C-CF-118 | Core features rule 34 |
| `500 SOMETHING BROKE` | the generic failure copy | C-CF-121 | Core features rule 35 |
| `403 NOT PERMITTED` | the refusal surface copy | C-CF-123 | Core features rule 36 |
| `Messages are visible to the owner only.` | the inbox refusal explanation | C-CF-124 | Core features rule 36 |
| `BACK TO WORK` | the refusal control | C-CF-125 | Core features rule 36 |
| `GET /api/studio/page-views` | the page-view log read | C-CF-129 | Core features rule 37 |
| `500` | the placeholder floor in milliseconds | C-CF-136 | Core features rule 40 |
| `Nothing here yet.` | the empty entry list line | C-UF-23 | User flow states |
| `Nothing on the shelf yet.` | the empty shelf line | C-UF-24 | User flow states |
| `One entry. Nothing to order yet.` | the single-entry shelf line | C-UF-25 | User flow states |
| `No messages.` | the empty inbox line | C-UF-26 | User flow states |
| `The contact form on the public site sends here.` | the empty inbox secondary line | C-UF-27 | User flow states |
| `Nothing recorded yet.` | the empty page-view log line | C-UF-28 | User flow states |
| `Work coming soon.` | the empty card row label | C-UF-29 | User flow states |
| `Recognition coming soon.` | the empty recognition list label | C-UF-30 | User flow states |
| `That did not load.` | the failed list load line | C-UF-31 | User flow states |
| `DATABASE_URL` | the database connection variable | C-TR-02 | Technical requirements para 1 |
| `STORAGE_ENDPOINT` | the object-store endpoint variable | C-TR-03 | Technical requirements para 1 |
| `STORAGE_BUCKET` | the bucket-name variable | C-TR-04 | Technical requirements para 1 |
| `STORAGE_ACCESS_KEY` | the object-store access key variable | C-TR-05 | Technical requirements para 1 |
| `STORAGE_SECRET_KEY` | the object-store secret key variable | C-TR-05 | Technical requirements para 1 |
| `GET /api/health` | the health route | C-TR-08 | Technical requirements para 1 |
| `200` | the health status | C-TR-08 | Technical requirements para 1 |
| `Ridge Survey` | the first seeded study | C-DM-14 | Data model seed data |
| `Tide Table` | the second seeded study | C-DM-15 | Data model seed data |
| `Lantern Field` | the third seeded study | C-DM-16 | Data model seed data |
| `Northlight Prize` | a seeded recognition body | C-DM-17 | Data model seed data |
| `Oslo` | a seeded city | C-DM-17 | Data model seed data |
| `Meridian Review` | a seeded recognition body | C-DM-18 | Data model seed data |
| `Lisbon` | a seeded city | C-DM-18 | Data model seed data |
| `Halden Biennale` | a seeded recognition body | C-DM-19 | Data model seed data |
| `Kyoto` | a seeded city | C-DM-19 | Data model seed data |
| `/app/USER_README.md` | the credentials file | C-DM-24 | Data model password paragraph |
| `11px` | the smallest type step | C-FE-01 | Front-end specification type ramp |
| `13.2px` | the smallest line box | C-FE-01 | Front-end specification type ramp |
| `12px` | the label type step | C-FE-04 | Front-end specification type ramp |
| `14.4px` | the footer line box | C-FE-03 | Front-end specification type ramp |
| `15.6px` | the status banner line box | C-FE-05 | Front-end specification type ramp |
| `16px` | the input type step | C-FE-06 | Front-end specification type ramp |
| `22.4px` | the input line box | C-FE-06 | Front-end specification type ramp |
| `18px` | the wordmark type step | C-FE-07 | Front-end specification type ramp |
| `21.6px` | the wordmark line box | C-FE-07 | Front-end specification type ramp |
| `20px` | the control type step | C-FE-08 | Front-end specification type ramp |
| `28px` | the panel title type step | C-FE-09 | Front-end specification type ramp |
| `5000` | the message volume the app stays responsive at | C-CN-13 | Constraints para 4 |
| `50000` | the page-view volume the app stays responsive at | C-CN-13 | Constraints para 4 |
| `APP_PUBLIC_URL` | the public address variable | C-DC-01 | Deployment contract bullet 1 |
| `APP_PUBLIC_PORT` | the public port variable | C-DC-02 | Deployment contract bullet 1 |
| `4173` | the container-internal port | C-DC-02 | Deployment contract bullet 1 |
| `/api` | the API prefix | C-DC-03 | Deployment contract bullet 2 |
| `.browser_screenshots/` | a reserved directory | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | a reserved directory | C-DC-08 | Deployment contract bullet 6 |
| `0.0.0.0` | the bind address | C-DC-11 | Deployment contract bullet 9 |
| `127.0.0.1` | the forbidden bind address | C-DC-11 | Deployment contract bullet 9 |
| `code` | the error body key naming the condition | C-DC-15 | Deployment contract API shapes |
| `fields` | the error body key naming the field errors | C-DC-16 | Deployment contract API shapes |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the invitation token in the invite route | C-UF-09 | the token format is not given |
| the one real breakpoint | C-UX-25 | the width is named but not valued |
| the sound control state | C-UX-23 | the persistence rule is not pinned |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 6 |
| User roles | 2 | 27 |
| Core features | 27 | 139 |
| User flow | 7 | 32 |
| UI and UX notes | 7 | 28 |
| Technical requirements | 12 | 31 |
| Data model | 6 | 24 |
| Front-end specification | 8 | 19 |
| Constraints | 0 | 13 |
| Deployment contract | 9 | 16 |
