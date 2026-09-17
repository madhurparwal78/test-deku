# Checklist: Sovereign Hosting Studio

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, front-end specification, technical requirements, data model, constraints, deployment contract
Sections absent: build plan
Items: 818
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `literal` The site presents `Vela Studio` as a one-person software studio in Marburg. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The home page reveals a philosophy statement word by word as the reader scrolls. `src: Overview para 2`
- [ ] `C-OV-03` `capability` The home page shows four pinned capability cards whose line diagrams draw themselves. `src: Overview para 2`
- [ ] `C-OV-04` `capability` The site offers a public status board for every system the studio runs. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The site offers a library of finished builds whose numbers each carry the day of measurement. `src: Overview para 2`
- [ ] `C-OV-06` `capability` A visitor starts a job by sending a scoped build request. `src: Overview para 2`
- [ ] `C-OV-07` `constraint` The site carries no payment, no checkout, no comment, no chat, no newsletter, no search. `src: Overview para 4`
- [ ] `C-OV-08` `constraint` The public site carries no menu bar. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads every public route without an account. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An anonymous visitor submits a build request without an account. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An anonymous visitor is denied every submitted request. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An anonymous visitor is denied every attached brief. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An anonymous visitor cannot reach `/account` or any `/studio` route. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `client` lists at `/account` the requests sent during a signed-in session. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A `client` downloads the brief attached to a request the same client sent. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A `client` is denied the request of another client. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A `client` is denied the attached brief of another client. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A `client` is denied every status change. `src: User roles table row 2`
- [ ] `C-RL-11` `role` A `client` is refused every studio endpoint. `src: User roles table row 2`
- [ ] `C-RL-12` `role` Signup creates an account with the role `client` whatever role the body claims. `src: User roles para 2`
- [ ] `C-RL-13` `role` The `founder` reads every request with every attached brief. `src: User roles table row 3`
- [ ] `C-RL-14` `role` The `founder` moves a request through the review statuses. `src: User roles table row 3`
- [ ] `C-RL-15` `role` The `founder` creates systems. `src: User roles table row 3`
- [ ] `C-RL-16` `role` The `founder` records checks for a system. `src: User roles table row 3`
- [ ] `C-RL-17` `role` The `founder` appends notes to incidents. `src: User roles table row 3`
- [ ] `C-RL-18` `role` The `founder` creates build records. `src: User roles table row 3`
- [ ] `C-RL-19` `role` The `founder` publishes or unpublishes build records. `src: User roles table row 3`
- [ ] `C-RL-20` `role` The `founder` adds measurements to build records. `src: User roles table row 3`
- [ ] `C-RL-21` `role` The `founder` uploads the portrait. `src: User roles table row 3`
- [ ] `C-RL-22` `role` The `founder` reads the page-view log. `src: User roles table row 3`
- [ ] `C-RL-23` `role` No account with the role `founder` is created through signup. `src: User roles table row 3`
- [ ] `C-RL-24` `constraint` A denied call from a `client` session leaves the protected state unchanged. `src: User roles para 1`
- [ ] `C-RL-25` `role` An anonymous call to an endpoint needing a session is denied. `src: User roles para 1`
- [ ] `C-RL-26` `literal` The seeded account `founder@example.com` holds the role `founder`. `src: User roles seeded accounts row 1`
- [ ] `C-RL-27` `literal` The seeded account `client@example.com` holds the role `client`. `src: User roles seeded accounts row 2`
- [ ] `C-RL-28` `literal` The seeded account `client2@example.com` holds the role `client`. `src: User roles seeded accounts row 3`
- [ ] `C-RL-29` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles para 2`
- [ ] `C-RL-30` `role` A `client` asking for the full request list is refused. `src: Core features rule 1`

## C-CF Core features

- [ ] `C-CF-01` `role` A request read by reference succeeds only for the `founder` or the owning `client`. `src: Core features rule 1`
- [ ] `C-CF-02` `role` An attached brief is readable only by the `founder` or the owning `client`. `src: Core features rule 1`
- [ ] `C-CF-03` `constraint` A refused read of a request reveals nothing about the request. `src: Core features rule 1`
- [ ] `C-CF-04` `constraint` The stored brief object is refused to a caller holding no storage credentials. `src: Core features rule 1`
- [ ] `C-CF-05` `constraint` A request submitted without a session appears in no client list. `src: Core features rule 1`
- [ ] `C-CF-06` `literal` The seeded request `VS-2026-0001` belongs to `client@example.com` with an attached brief. `src: Core features rule 1`
- [ ] `C-CF-07` `role` The account `client2@example.com` is denied `VS-2026-0001`. `src: Core features rule 1`
- [ ] `C-CF-08` `role` The account `client2@example.com` is denied the brief attached to `VS-2026-0001`. `src: Core features rule 1`
- [ ] `C-CF-09` `constraint` A build request carries at most one attached brief. `src: Core features rule 2`
- [ ] `C-CF-10` `literal` An attached brief is a PDF, PNG or JPEG file of at most `5 MB`. `src: Core features rule 2`
- [ ] `C-CF-11` `capability` The bytes of an attached brief are stored in `minio`. `src: Core features rule 2`
- [ ] `C-CF-12` `literal` An attached brief is stored at the key `requests/{reference}/{sha256_of_bytes}.{ext}`. `src: Core features rule 2`
- [ ] `C-CF-13` `constraint` A file of another type is rejected as invalid. `src: Core features rule 2`
- [ ] `C-CF-14` `constraint` A file over the size limit is rejected as invalid. `src: Core features rule 2`
- [ ] `C-CF-15` `constraint` A submission rejected for its file writes no request row, no attachment row, no object. `src: Core features rule 2`
- [ ] `C-CF-16` `capability` The owner reads an attached brief through the app. `src: Core features rule 2`
- [ ] `C-CF-17` `constraint` A presigned link, where used, expires within five minutes. `src: Core features rule 2`
- [ ] `C-CF-18` `literal` The composer at `/build-request` carries the heading `Describe the build`. `src: Core features rule 3`
- [ ] `C-CF-19` `constraint` The composer requires at least one capability from `software`, `website`, `hosting`. `src: Core features rule 3`
- [ ] `C-CF-20` `literal` The hosting posture is `managed` or `handover`. `src: Core features rule 3`
- [ ] `C-CF-21` `literal` The data residency is `eu` or `de`. `src: Core features rule 3`
- [ ] `C-CF-22` `literal` The timeline is `flexible`, `standard` or `accelerated`. `src: Core features rule 3`
- [ ] `C-CF-23` `literal` The budget band is `under-10k`, `10k-25k`, `25k-60k` or `over-60k`. `src: Core features rule 3`
- [ ] `C-CF-24` `literal` The description runs from `20` to `4000` characters. `src: Core features rule 3`
- [ ] `C-CF-25` `capability` The composer asks for a contact name. `src: Core features rule 3`
- [ ] `C-CF-26` `capability` The composer asks for a contact email. `src: Core features rule 3`
- [ ] `C-CF-27` `ui` The indicative figure updates as composer fields change. `src: Core features rule 3`
- [ ] `C-CF-28` `literal` The composer address carries `cap`, `posture`, `residency`, `timeline`, `budget`, `desc`, `v` in that order. `src: Core features rule 3`
- [ ] `C-CF-29` `literal` The `cap` value lists capabilities comma-separated in the order `software`, `website`, `hosting`. `src: Core features rule 3`
- [ ] `C-CF-30` `capability` Two copies of one composed state produce byte-identical addresses. `src: Core features rule 3`
- [ ] `C-CF-31` `capability` Opening a composed address restores every composer field with the same figure. `src: Core features rule 3`
- [ ] `C-CF-32` `capability` Composer edits replace the address rather than adding history entries. `src: Core features rule 3`
- [ ] `C-CF-33` `literal` The figure is stored in integer euro cents with the currency `eur`. `src: Core features rule 4`
- [ ] `C-CF-34` `literal` The current rule table `2026-09` sets `software` to `1200000`, `website` to `600000`, `hosting` to `300000`. `src: Core features rule 4`
- [ ] `C-CF-35` `capability` The capability amounts are summed over the chosen capabilities. `src: Core features rule 4`
- [ ] `C-CF-36` `literal` Posture `handover` adds `150000`. `src: Core features rule 4`
- [ ] `C-CF-37` `capability` Residency `de` adds ten percent of the capability sum. `src: Core features rule 4`
- [ ] `C-CF-38` `literal` Timeline `flexible`, `standard`, `accelerated` multiplies the subtotal by `90`, `100`, `125` percent. `src: Core features rule 4`
- [ ] `C-CF-39` `literal` The result rounds to the nearest `50000`, an exact half rounding up. `src: Core features rule 4`
- [ ] `C-CF-40` `literal` The figure displays as whole euros after `EUR`, for example `EUR 12,000`. `src: Core features rule 4`
- [ ] `C-CF-41` `literal` Software, managed, eu, standard gives `1200000`. `src: Core features rule 4 table row 1`
- [ ] `C-CF-42` `literal` Website, managed, eu, flexible gives `550000`. `src: Core features rule 4 table row 2`
- [ ] `C-CF-43` `literal` Hosting, managed, de, standard gives `350000`. `src: Core features rule 4 table row 3`
- [ ] `C-CF-44` `literal` Website, managed, de, accelerated gives `850000`. `src: Core features rule 4 table row 4`
- [ ] `C-CF-45` `literal` Software plus website, handover, de, accelerated gives `2650000`. `src: Core features rule 4 table row 5`
- [ ] `C-CF-46` `constraint` The budget band never changes the figure. `src: Core features rule 4`
- [ ] `C-CF-47` `literal` The retired table `2026-03` sets `software` to `1000000`, `website` to `500000`, `hosting` to `250000`, keeping every other `2026-09` rule. `src: Core features rule 5`
- [ ] `C-CF-48` `capability` A composed address naming the retired version shows the figure quoted under that version. `src: Core features rule 5`
- [ ] `C-CF-49` `ui` A figure quoted under a retired version is labelled with the version. `src: Core features rule 5`
- [ ] `C-CF-50` `constraint` A submission naming a retired or unknown version is rejected, naming `rules_version`. `src: Core features rule 5`
- [ ] `C-CF-51` `literal` `GET /api/pricing-rules` returns the current table with the field `version`. `src: Core features rule 5`
- [ ] `C-CF-52` `literal` `GET /api/pricing-rules/{version}` returns a current or retired table. `src: Core features rule 5`
- [ ] `C-CF-53` `capability` The server recomputes the submitted figure from the server copy of the table. `src: Core features rule 6`
- [ ] `C-CF-54` `constraint` A figure mismatch is rejected as invalid, naming `indicative_minor`. `src: Core features rule 6`
- [ ] `C-CF-55` `constraint` A submission rejected for its figure or version writes nothing. `src: Core features rule 6`
- [ ] `C-CF-56` `constraint` A stored request keeps the stored figure plus the stored rules version after the table changes. `src: Core features rule 6`
- [ ] `C-CF-57` `literal` Each accepted request receives a reference shaped `VS-<year>-<NNNN>`. `src: Core features rule 7`
- [ ] `C-CF-58` `capability` The reference sequence runs within the UTC year of submission, starting at 0001. `src: Core features rule 7`
- [ ] `C-CF-59` `literal` The next request accepted in 2026 is `VS-2026-0003`. `src: Core features rule 7`
- [ ] `C-CF-60` `constraint` No two requests share a reference. `src: Core features rule 7`
- [ ] `C-CF-61` `capability` A later request carries a higher reference number. `src: Core features rule 7`
- [ ] `C-CF-62` `capability` With scripts off, the composer posts as a plain form to `/build-request`. `src: Core features rule 8`
- [ ] `C-CF-63` `literal` The no-script response is a rendered summary page headed `Request received`. `src: Core features rule 8`
- [ ] `C-CF-64` `capability` The summary page shows the reference, the figure, the rule table version, the status `new`. `src: Core features rule 8`
- [ ] `C-CF-65` `capability` The server computes the figure when a submission carries none. `src: Core features rule 8`
- [ ] `C-CF-66` `capability` A no-script reference comes from the same sequence as a scripted reference. `src: Core features rule 8`
- [ ] `C-CF-67` `capability` A form submission accepts `capabilities` repeated or comma-separated. `src: Core features rule 8`
- [ ] `C-CF-68` `literal` The form carries a decoy field `contact_fax` that a person never sees. `src: Core features rule 9`
- [ ] `C-CF-69` `constraint` A submission with any value in the decoy field is refused, writing nothing. `src: Core features rule 9`
- [ ] `C-CF-70` `constraint` The same contact email with the same description from one network address within ten minutes is refused as a duplicate. `src: Core features rule 9`
- [ ] `C-CF-71` `constraint` A refused duplicate writes nothing. `src: Core features rule 9`
- [ ] `C-CF-72` `constraint` The request form uses no third-party challenge. `src: Core features rule 9`
- [ ] `C-CF-73` `literal` A request starts with the status `new`. `src: Core features rule 10`
- [ ] `C-CF-74` `literal` The founder moves a request along `new`, `reviewing`, `quoted`, then `accepted` or `declined`. `src: Core features rule 10`
- [ ] `C-CF-75` `literal` A `new` or `reviewing` request may go straight to `declined`. `src: Core features rule 10`
- [ ] `C-CF-76` `constraint` A request marked accepted or declined never changes status again. `src: Core features rule 10`
- [ ] `C-CF-77` `constraint` Any other status move is rejected, leaving the request unchanged. `src: Core features rule 10`
- [ ] `C-CF-78` `role` A `client` status change is denied, leaving the request unchanged. `src: Core features rule 10`
- [ ] `C-CF-79` `capability` The `/account` list shows each own request with reference, figure, current status. `src: Core features rule 10`
- [ ] `C-CF-80` `capability` `GET /api/uptime/projects` answers without a session. `src: Core features rule 11`
- [ ] `C-CF-81` `literal` The feed envelope holds `data` containing `nextCheckAt` plus `projects`. `src: Core features rule 11`
- [ ] `C-CF-82` `literal` Each project carries `id`, `slug`, `name`, `position`, `currentStatus`, `uptimePercent`, `latestResponseMs`, `latestCheckedAt`, `lastStatusChangeAt`, `bars`. `src: Core features rule 11`
- [ ] `C-CF-83` `literal` Each bar carries `status` with `checkedAt`. `src: Core features rule 11`
- [ ] `C-CF-84` `literal` A feed failure answers with `error` holding `message`. `src: Core features rule 11`
- [ ] `C-CF-85` `capability` The `projects` list is sorted by `position`. `src: Core features rule 11`
- [ ] `C-CF-86` `literal` The `currentStatus` value is one of `up`, `slow`, `degraded`, `down`, `unknown`. `src: Core features rule 11`
- [ ] `C-CF-87` `capability` The `currentStatus` value equals the status of the latest check. `src: Core features rule 11`
- [ ] `C-CF-88` `capability` A system with no check reports `currentStatus` as `unknown` with a null `latestCheckedAt`. `src: Core features rule 11`
- [ ] `C-CF-89` `capability` The `latestResponseMs` plus `latestCheckedAt` values come from the latest check. `src: Core features rule 11`
- [ ] `C-CF-90` `capability` The `lastStatusChangeAt` value is the first check of the current unbroken run of the current status. `src: Core features rule 11`
- [ ] `C-CF-91` `capability` The `nextCheckAt` value is the earliest latest check plus interval across systems. `src: Core features rule 11`
- [ ] `C-CF-92` `ui` The `Next check` tile counts down to `nextCheckAt`. `src: Core features rule 11`
- [ ] `C-CF-93` `constraint` The feed carries no client name, no address, no identifier beyond an opaque system id. `src: Core features rule 11`
- [ ] `C-CF-94` `capability` The founder records a check with `POST /api/systems/{slug}/checks`. `src: Core features rule 12`
- [ ] `C-CF-95` `constraint` A check posted with the status `unknown` is rejected as invalid. `src: Core features rule 12`
- [ ] `C-CF-96` `constraint` The `response_ms` value is a non-negative whole number or null. `src: Core features rule 12`
- [ ] `C-CF-97` `capability` An exact repeat of a check is accepted, changing nothing. `src: Core features rule 12`
- [ ] `C-CF-98` `constraint` A different status for an already recorded time is rejected. `src: Core features rule 12`
- [ ] `C-CF-99` `constraint` A check older than the latest recorded check, other than an exact repeat, is rejected. `src: Core features rule 12`
- [ ] `C-CF-100` `literal` A system check interval defaults to `300` seconds. `src: Core features rule 12`
- [ ] `C-CF-101` `capability` Missed intervals between two checks become unknown slots. `src: Core features rule 13`
- [ ] `C-CF-102` `capability` The unknown slot count is the gap over the interval, rounded, minus one, never below zero. `src: Core features rule 13`
- [ ] `C-CF-103` `literal` The `bars` list holds the most recent `90` slots, oldest first, ending with the latest check. `src: Core features rule 13`
- [ ] `C-CF-104` `capability` The `uptimePercent` value is the share of the real checks inside the `bars` slots marked up or slow, to two decimals. `src: Core features rule 13`
- [ ] `C-CF-105` `constraint` Unknown slots count neither for nor against `uptimePercent`. `src: Core features rule 13`
- [ ] `C-CF-106` `capability` A system with no check reports `uptimePercent` as null. `src: Core features rule 13`
- [ ] `C-CF-107` `literal` Checks up, up, down, then up after a gap give two unknown slots with `75.00`. `src: Core features rule 13 table row 1`
- [ ] `C-CF-108` `literal` Checks up, slow, degraded, up give `75.00`. `src: Core features rule 13 table row 2`
- [ ] `C-CF-109` `literal` Checks up, up, down give `66.67`. `src: Core features rule 13 table row 3`
- [ ] `C-CF-110` `literal` Each system stores `open_after` defaulting to `3` with `close_after` defaulting to `2`. `src: Core features rule 14`
- [ ] `C-CF-111` `capability` A degraded or down check counts as failing; an up or slow check counts as available. `src: Core features rule 14`
- [ ] `C-CF-112` `capability` An incident opens at the first of `open_after` consecutive failing checks. `src: Core features rule 14`
- [ ] `C-CF-113` `capability` An incident resolves at the check completing `close_after` consecutive available checks. `src: Core features rule 14`
- [ ] `C-CF-114` `constraint` A system holds at most one open incident. `src: Core features rule 14`
- [ ] `C-CF-115` `constraint` A flapping system produces one incident, not one per flap. `src: Core features rule 14`
- [ ] `C-CF-116` `literal` An incident reference joins the system slug with the opening date, hour, minute, as in `vela-studio-console-20260901-1420`. `src: Core features rule 14`
- [ ] `C-CF-117` `constraint` Replaying a check stream keeps the same references with no new incident. `src: Core features rule 14`
- [ ] `C-CF-118` `literal` Each incident entry carries `seq`, `kind`, a body, a time. `src: Core features rule 15`
- [ ] `C-CF-119` `literal` An entry `kind` is `opened`, `note` or `resolved`. `src: Core features rule 15`
- [ ] `C-CF-120` `capability` The `seq` value rises by one across every entry of one system, starting at 1. `src: Core features rule 15`
- [ ] `C-CF-121` `capability` Opening or resolving an incident writes one entry each. `src: Core features rule 15`
- [ ] `C-CF-122` `capability` The founder appends a note with `POST /api/uptime/incidents/{ref}/notes`. `src: Core features rule 15`
- [ ] `C-CF-123` `constraint` A note leaves every earlier entry unchanged. `src: Core features rule 15`
- [ ] `C-CF-124` `constraint` A request to edit or delete an entry is rejected, leaving the log unchanged. `src: Core features rule 15`
- [ ] `C-CF-125` `capability` Anyone reads `GET /api/uptime/incidents` newest first. `src: Core features rule 15`
- [ ] `C-CF-126` `capability` Anyone reads `GET /api/uptime/incidents/{ref}`. `src: Core features rule 15`
- [ ] `C-CF-127` `literal` The seeded incident opened at `2026-09-01T14:20:00Z`. `src: Core features rule 15`
- [ ] `C-CF-128` `literal` The seeded incident resolved at `2026-09-01T14:40:00Z`. `src: Core features rule 15`
- [ ] `C-CF-129` `literal` The seeded incident carries entries `opened`, `resolved`, then a `note`. `src: Core features rule 15`
- [ ] `C-CF-130` `literal` The seeded note begins `Disk pressure on the Frankfurt node`. `src: Core features rule 15`
- [ ] `C-CF-131` `ui` The board lists every system as a card in feed order. `src: Core features rule 16`
- [ ] `C-CF-132` `literal` Four tiles read `Systems`, `Operational`, `Average uptime`, `Next check`. `src: Core features rule 16`
- [ ] `C-CF-133` `ui` The four tiles are worked out in the page from the feed. `src: Core features rule 16`
- [ ] `C-CF-134` `capability` The `Operational` tile shows the up count, a slash with no surrounding space, the total, as in `6/7`. `src: Core features rule 16`
- [ ] `C-CF-135` `capability` The `Average uptime` tile shows the mean of every numeric system uptime to two decimals. `src: Core features rule 16`
- [ ] `C-CF-136` `ui` The `Next check` tile recomputes every second. `src: Core features rule 16`
- [ ] `C-CF-137` `ui` The tiles appear only when there is data. `src: Core features rule 16`
- [ ] `C-CF-138` `ui` Each card shows a pill with the status in words beside a dot. `src: Core features rule 16`
- [ ] `C-CF-139` `literal` Each card shows `Uptime`, `Response time`, `Last checked`, `Last status change`. `src: Core features rule 16`
- [ ] `C-CF-140` `ui` Each card shows a strip of the most recent bars that fit the card width. `src: Core features rule 16`
- [ ] `C-CF-141` `ui` A null response time shows a single dash on the card. `src: Core features rule 16`
- [ ] `C-CF-142` `literal` A null check time shows `Awaiting checks`. `src: Core features rule 16`
- [ ] `C-CF-143` `ui` The first load shows a shimmering skeleton. `src: Core features rule 16`
- [ ] `C-CF-144` `ui` Later refreshes swap values in place with no skeleton, no spinner. `src: Core features rule 16`
- [ ] `C-CF-145` `ui` The page refreshes every thirty seconds, only with the tab visible. `src: Core features rule 16`
- [ ] `C-CF-146` `ui` The page never starts a refresh before the previous refresh settles. `src: Core features rule 16`
- [ ] `C-CF-147` `capability` A failed refresh replaces the list with the failure block, removing the tiles. `src: Core features rule 16`
- [ ] `C-CF-148` `capability` An empty project list shows the empty block. `src: Core features rule 16`
- [ ] `C-CF-149` `literal` An `Incident history` section lists incidents newest first below the cards. `src: Core features rule 16`
- [ ] `C-CF-150` `literal` An unresolved incident shows `Ongoing` in the incident history. `src: Core features rule 16`
- [ ] `C-CF-151` `literal` Each incident opens a page at `/uptime/incidents/<ref>` listing entries in `seq` order. `src: Core features rule 16`
- [ ] `C-CF-152` `literal` An empty incident history reads `No incidents recorded.` `src: Core features rule 16`
- [ ] `C-CF-153` `literal` With scripts off the board shows `Live status needs JavaScript to load.` `src: Core features rule 16`
- [ ] `C-CF-154` `capability` With scripts off the board still renders the heading, lede, incident history, notice. `src: Core features rule 16`
- [ ] `C-CF-155` `capability` The `/builds` page lists published build records newest delivery first. `src: Core features rule 17`
- [ ] `C-CF-156` `ui` Choosing a capability narrows `/builds` without a full page load. `src: Core features rule 17`
- [ ] `C-CF-157` `literal` A capability filter writes an address such as `/builds?capability=software`. `src: Core features rule 17`
- [ ] `C-CF-158` `ui` The back button walks back through the build filters. `src: Core features rule 17`
- [ ] `C-CF-159` `capability` With scripts off the build filters are plain links. `src: Core features rule 17`
- [ ] `C-CF-160` `capability` A record page shows title, capability, summary, body, stack, dates, client, measurements, diagram. `src: Core features rule 17`
- [ ] `C-CF-161` `literal` A withheld client shows `Client withheld`. `src: Core features rule 17`
- [ ] `C-CF-162` `capability` Every figure on a record shows the date the figure was measured. `src: Core features rule 17`
- [ ] `C-CF-163` `literal` A record with no measurement shows `Not yet measured`. `src: Core features rule 17`
- [ ] `C-CF-164` `capability` An unpublished record is absent from every public list. `src: Core features rule 17`
- [ ] `C-CF-165` `capability` An unpublished record address answers not-found, revealing nothing. `src: Core features rule 17`
- [ ] `C-CF-166` `capability` Publishing a record makes the record listed plus readable in one act. `src: Core features rule 17`
- [ ] `C-CF-167` `capability` Unpublishing a record withdraws listing plus address at once. `src: Core features rule 17`
- [ ] `C-CF-168` `literal` A diagram primitive carries `kind` of `rect`, `path` or `circle` with `role` of `accent`, `structure` or `faint`. `src: Core features rule 18`
- [ ] `C-CF-169` `capability` The record page draws diagram primitives in list order under the home diagram drawing rules. `src: Core features rule 18`
- [ ] `C-CF-170` `literal` The record drawing is labelled `Diagram:` followed by the record title. `src: Core features rule 18`
- [ ] `C-CF-171` `constraint` A record with an unknown primitive kind or a missing role is rejected, saving nothing. `src: Core features rule 18`
- [ ] `C-CF-172` `literal` The card link `Scope a build` opens the latest delivered published `software` record. `src: Core features rule 19`
- [ ] `C-CF-173` `literal` The card link `See a build` opens the latest delivered published `website` record. `src: Core features rule 19`
- [ ] `C-CF-174` `literal` The card link `See the stack` opens the latest delivered published `hosting` record. `src: Core features rule 19`
- [ ] `C-CF-175` `constraint` An unpublished record is never a capability link target. `src: Core features rule 19`
- [ ] `C-CF-176` `literal` A capability with no published record links to `/builds?capability=` for that capability. `src: Core features rule 19`
- [ ] `C-CF-177` `literal` The seeded capability links open `/builds/harbour-ledger`, `/builds/kestrel-storefront`, `/builds/lahn-clinic-hosting`. `src: Core features rule 19`
- [ ] `C-CF-178` `literal` The draft `/builds/aurora-payroll-portal` is never a capability link target. `src: Core features rule 19`
- [ ] `C-CF-179` `literal` The card link `Status & uptime` opens `/uptime`. `src: Core features rule 19`
- [ ] `C-CF-180` `literal` The hero button `Talk to an engineer` opens `/build-request`. `src: Core features rule 19`
- [ ] `C-CF-181` `literal` The contact prompt `talk to an engineer_` opens `/build-request`. `src: Core features rule 19`
- [ ] `C-CF-182` `ui` The home argument runs in six numbered beats with the teaser below. `src: Core features rule 20`
- [ ] `C-CF-183` `ui` A pinned section holds still as the content advances with the scroll. `src: Core features rule 20`
- [ ] `C-CF-184` `ui` Words reveal one at a time from a grey blur into white. `src: Core features rule 20`
- [ ] `C-CF-185` `ui` Words the studio marks reveal into the amber accent. `src: Core features rule 20`
- [ ] `C-CF-186` `ui` A soft reveal edge a little over two words wide travels along the sentence. `src: Core features rule 20`
- [ ] `C-CF-187` `ui` The reveal follows scroll progress through the section, never a timer. `src: Core features rule 20`
- [ ] `C-CF-188` `ui` Scrolling back up un-reveals the words in exactly the reverse order. `src: Core features rule 20`
- [ ] `C-CF-189` `ui` Each card diagram draws one line at a time in the listed order. `src: Core features rule 20`
- [ ] `C-CF-190` `ui` Each card diagram finishes about two thirds of the way through the card hold. `src: Core features rule 20`
- [ ] `C-CF-191` `ui` A hairline under the philosophy statement fills from the left as progress. `src: Core features rule 20`
- [ ] `C-CF-192` `ui` The hero drifts upward more slowly than the page, fading as the reader leaves. `src: Core features rule 20`
- [ ] `C-CF-193` `ui` In-page links glide to the target, taking longer for longer distances. `src: Core features rule 20`
- [ ] `C-CF-194` `capability` A click with a modifier key on an in-page link opens a new tab. `src: Core features rule 20`
- [ ] `C-CF-195` `ui` The link `See what we build` lands where card `02` has finished drawing. `src: Core features rule 20`
- [ ] `C-CF-196` `literal` The address records a reading position as `at=<section>-<percent>`. `src: Core features rule 21`
- [ ] `C-CF-197` `literal` The home sections are `philosophy`, `software-platforms`, `websites`, `managed-hosting`, `infrastructure`. `src: Core features rule 21`
- [ ] `C-CF-198` `literal` The about sections are `craft`, `principle`. `src: Core features rule 21`
- [ ] `C-CF-199` `literal` The percent is a whole number from `0` to `100`, as in `/?at=managed-hosting-80`. `src: Core features rule 21`
- [ ] `C-CF-200` `capability` The position address is replaced as the reader settles, never added to history. `src: Core features rule 21`
- [ ] `C-CF-201` `capability` Two shares of one moment produce byte-identical addresses. `src: Core features rule 21`
- [ ] `C-CF-202` `capability` A shared address opened in a fresh window lands on the named section. `src: Core features rule 21`
- [ ] `C-CF-203` `ui` A shared address opened in a fresh window at a different width, with fonts not yet loaded, lands within one word of the same reveal. `src: Core features rule 21`
- [ ] `C-CF-204` `capability` Under reduced motion a shared address lands at the top of the named section fully revealed. `src: Core features rule 21`
- [ ] `C-CF-205` `constraint` Under reduced motion no scroll effect loads, leaving native scrolling. `src: Core features rule 22`
- [ ] `C-CF-206` `capability` Under reduced motion every word shows the finished colour at full strength. `src: Core features rule 22`
- [ ] `C-CF-207` `constraint` Under reduced motion no animation loops. `src: Core features rule 22`
- [ ] `C-CF-208` `capability` With scripts off every public route renders complete copy from the server. `src: Core features rule 22`
- [ ] `C-CF-209` `capability` With scripts off or reduced motion every diagram is complete. `src: Core features rule 22`
- [ ] `C-CF-210` `constraint` The reveal never inserts or removes a word. `src: Core features rule 22`
- [ ] `C-CF-211` `capability` A revealed paragraph keeps the spaces between words. `src: Core features rule 22`
- [ ] `C-CF-212` `ui` The founder page opens with the round portrait beside the headline inside a soft amber halo. `src: Core features rule 23`
- [ ] `C-CF-213` `ui` The founder page holds two pinned statements revealed like the home statement. `src: Core features rule 23`
- [ ] `C-CF-214` `literal` The personal contact prompt on the founder page reads `about me_`. `src: Core features rule 23`
- [ ] `C-CF-215` `literal` An uploaded portrait is stored in `minio` at `portrait/{sha256_of_bytes}.{ext}`. `src: Core features rule 23`
- [ ] `C-CF-216` `capability` `GET /api/portrait` serves the uploaded portrait to anyone. `src: Core features rule 23`
- [ ] `C-CF-217` `literal` The portrait carries the alternative text `Anton Ferber, founder of Vela Studio`. `src: Core features rule 23`
- [ ] `C-CF-218` `literal` With no portrait the drawn stand-in carries the accessible name `Portrait placeholder`. `src: Core features rule 23`
- [ ] `C-CF-219` `ui` The portrait stand-in is a lit dark shape with a warm rim of light, never a face. `src: Core features rule 23`
- [ ] `C-CF-220` `capability` With no portrait `GET /api/portrait` answers not-found. `src: Core features rule 23`
- [ ] `C-CF-221` `ui` The legal documents set one clause per block with a fine line above each block. `src: Core features rule 24`
- [ ] `C-CF-222` `literal` The legal back link reads `Back to Vela Studio`. `src: Core features rule 24`
- [ ] `C-CF-223` `constraint` The legal routes carry no script element. `src: Core features rule 24`
- [ ] `C-CF-224` `constraint` The legal routes load no script resource. `src: Core features rule 24`
- [ ] `C-CF-225` `constraint` The legal routes carry no grain, no glow, no fixed chrome. `src: Core features rule 24`
- [ ] `C-CF-226` `constraint` The studio phone number appears on no page except the legal pages. `src: Core features rule 24`
- [ ] `C-CF-227` `literal` The footer list is `Home`, `About`, `Legal Notice`, `Terms`, `Status/Uptime`. `src: Core features rule 25`
- [ ] `C-CF-228` `constraint` The footer never links to the page the reader is on. `src: Core features rule 25`
- [ ] `C-CF-229` `literal` The founder page plus the status board carry a fixed back pill reading `Back`. `src: Core features rule 25`
- [ ] `C-CF-230` `capability` The back pill returns to `/`. `src: Core features rule 25`
- [ ] `C-CF-231` `capability` Every internal link on every public route opens a page that exists. `src: Core features rule 26`
- [ ] `C-CF-232` `capability` Each public page view records one row carrying the route with the time. `src: Core features rule 27`
- [ ] `C-CF-233` `constraint` A page view row holds nothing that identifies a person. `src: Core features rule 27`
- [ ] `C-CF-234` `role` Only the `founder` reads the page-view log at `/studio/page-views`. `src: Core features rule 27`
- [ ] `C-CF-235` `constraint` No response on any route sets a cookie, sign-in included. `src: Core features rule 28`
- [ ] `C-CF-236` `constraint` The running site loads nothing from another origin. `src: Core features rule 28`
- [ ] `C-CF-237` `constraint` The running site sends nothing to another origin. `src: Core features rule 28`
- [ ] `C-CF-238` `constraint` The site carries no analytics script, no tag manager, no consent banner. `src: Core features rule 28`
- [ ] `C-CF-239` `literal` The founder lands on `/studio` after sign-in at `/login`. `src: Core features rule 29`
- [ ] `C-CF-240` `literal` A client lands on `/account` after sign-in at `/login`. `src: Core features rule 29`
- [ ] `C-CF-241` `literal` The studio top bar reads `Requests`, `Builds`, `Systems`, `Portrait`, `Page views`. `src: Core features rule 29`
- [ ] `C-CF-242` `ui` The request inbox is a grid of cards, newest first. `src: Core features rule 29`
- [ ] `C-CF-243` `ui` Each inbox card shows the reference, contact name, capabilities, figure, status. `src: Core features rule 29`
- [ ] `C-CF-244` `ui` Opening an inbox card slides a panel in from the side over the inbox, showing the full request with the attached brief. `src: Core features rule 29`
- [ ] `C-CF-245` `literal` A studio status change confirms with a brief toast reading `Status updated`. `src: Core features rule 29`
- [ ] `C-CF-246` `ui` The studio record list is a grid of every record, published or not. `src: Core features rule 29`
- [ ] `C-CF-247` `ui` Adding a record or adding a system opens a side panel. `src: Core features rule 29`
- [ ] `C-CF-248` `role` Every studio route is refused to a `client`. `src: Core features rule 29`
- [ ] `C-CF-249` `literal` Interactive text reaches a contrast ratio of at least `4.5:1` against the page ground. `src: Core features rule 30`
- [ ] `C-CF-250` `capability` The faintest grey is raised one step wherever the grey marks a link, every footer link among them. `src: Core features rule 30`
- [ ] `C-CF-251` `literal` The attachment size limit of `5 MB` is `5242880` bytes. `src: Core features rule 2`
- [ ] `C-CF-252` `constraint` The attachment type is decided by the file bytes, not the name or declared type. `src: Core features rule 2`
- [ ] `C-CF-253` `literal` The attachment key extension is `pdf`, `png` or `jpg`. `src: Core features rule 2`
- [ ] `C-CF-254` `capability` A submission carrying no figure is stored with the server figure. `src: Core features rule 6`
- [ ] `C-CF-255` `capability` A JSON submission lists `capabilities` as an array with repeated keys counted once. `src: Core features rule 6`
- [ ] `C-CF-256` `capability` The stored capability list follows the order software, website, hosting. `src: Core features rule 6`
- [ ] `C-CF-257` `constraint` Two requests accepted at the same moment receive two different references. `src: Core features rule 7`
- [ ] `C-CF-258` `capability` An exact repeat means the same `checked_at` with the same `status`, whatever the `response_ms`. `src: Core features rule 12`
- [ ] `C-CF-259` `constraint` The same check sent twice at the same moment leaves one row. `src: Core features rule 12`
- [ ] `C-CF-260` `capability` A check for an unknown slug answers not-found. `src: Core features rule 12`
- [ ] `C-CF-261` `capability` The founder creates a system with `POST /api/systems`. `src: Core features rule 12`
- [ ] `C-CF-262` `literal` A system interval is a whole number of at least `60` seconds. `src: Core features rule 12`
- [ ] `C-CF-263` `constraint` A taken slug, a short interval, or a threshold below 1 is rejected, creating nothing. `src: Core features rule 12`
- [ ] `C-CF-264` `capability` Unknown slots never break or start a run for `lastStatusChangeAt`. `src: Core features rule 11`
- [ ] `C-CF-265` `literal` With `open_after` `2`, `close_after` `3`, checks down, down, up, down, up, down, up, up, up, up from `11:00` open at `11:00`, resolving at `11:40`. `src: Core features rule 14`
- [ ] `C-CF-266` `constraint` Two notes appended at the same moment receive two consecutive `seq` values. `src: Core features rule 15`
- [ ] `C-CF-267` `literal` Each listed incident names the system by slug in `system`. `src: Core features rule 15`
- [ ] `C-CF-268` `role` A note from anybody but the `founder` is denied. `src: Core features rule 15`
- [ ] `C-CF-269` `constraint` An empty note is rejected as invalid. `src: Core features rule 15`
- [ ] `C-CF-270` `literal` The `Next check` tile shows whole seconds rounded up with an `s`, as in `27s`. `src: Core features rule 16`
- [ ] `C-CF-271` `literal` The `Next check` tile reads `Due now` once the moment has passed. `src: Core features rule 16`
- [ ] `C-CF-272` `capability` The founder adds a measurement with `POST /api/builds/{slug}/measurements`. `src: Core features rule 17`
- [ ] `C-CF-273` `constraint` A measurement with an unknown metric, a negative value or a non-date is rejected, saving nothing. `src: Core features rule 17`
- [ ] `C-CF-274` `constraint` A build record with a taken slug is rejected as invalid. `src: Core features rule 17`
- [ ] `C-CF-275` `ui` The founder page shows the one stored portrait at two display sizes. `src: Core features rule 23`
- [ ] `C-CF-276` `literal` The founder uploads the portrait at `/studio/portrait`. `src: Core features rule 23`
- [ ] `C-CF-277` `constraint` A portrait upload whose bytes are neither PNG nor JPEG, or over 5 MB, is rejected, storing nothing. `src: Core features rule 23`
- [ ] `C-CF-278` `literal` The portrait key extension is `png` or `jpg`. `src: Core features rule 23`
- [ ] `C-CF-279` `capability` A later portrait upload replaces the portrait shown. `src: Core features rule 23`
- [ ] `C-CF-280` `capability` Rendering a public route records one page view row, legal pages included. `src: Core features rule 27`
- [ ] `C-CF-281` `capability` The route `POST /api/page-views` records one row for a named public route. `src: Core features rule 27`
- [ ] `C-CF-282` `constraint` A page never posts a view the server already recorded. `src: Core features rule 27`
- [ ] `C-CF-283` `capability` A sign-in lasts for the browser tab, until sign-out or the tab closes. `src: Core features rule 29`
- [ ] `C-CF-284` `constraint` The signed-in pages carry no private data in the markup. `src: Core features rule 29`
- [ ] `C-CF-285` `ui` A studio side panel closes with the Escape key. `src: Core features rule 29`
- [ ] `C-CF-286` `ui` Declining a request asks for confirmation first. `src: Core features rule 29`
- [ ] `C-CF-287` `ui` Unpublishing a record asks for confirmation first. `src: Core features rule 29`
- [ ] `C-CF-288` `constraint` Concurrent accepted requests leave no reference number skipped. `src: Core features rule 7`
- [ ] `C-CF-289` `capability` Feed timestamps are ISO 8601 in UTC. `src: Core features rule 11`
- [ ] `C-CF-290` `capability` A system with no check reports a null `lastStatusChangeAt`. `src: Core features rule 11`
- [ ] `C-CF-291` `capability` A system with no check reports a null `latestResponseMs`. `src: Core features rule 11`
- [ ] `C-CF-292` `capability` Each unknown slot carries the time the slot should have been checked. `src: Core features rule 13`
- [ ] `C-CF-293` `constraint` Replaying a check stream adds no incident entry. `src: Core features rule 14`
- [ ] `C-CF-294` `capability` The budget band is stored with the request, shown beside the figure. `src: Core features rule 4`
- [ ] `C-CF-295` `capability` Each incident history row shows the system name beside the opening time. `src: Core features rule 16`
- [ ] `C-CF-296` `constraint` The app reads an attached brief by one mechanism everywhere. `src: Core features rule 2`
- [ ] `C-CF-297` `literal` A `rect` carries `x`, `y`, `width`, `height`, optional `rx`; a `path` carries `d`; a `circle` carries `cx`, `cy`, `r`. `src: Core features rule 18`
- [ ] `C-CF-298` `capability` Beneath the composer form a `Sign in` link opens `/login` carrying the composer address as the return page. `src: Core features rule 3`
- [ ] `C-CF-299` `capability` A resolved incident shows the resolution time in the incident history. `src: Core features rule 16`
- [ ] `C-CF-300` `capability` The scripted composer submission carries the page figure as `indicative_minor`. `src: Core features rule 6`
- [ ] `C-CF-301` `literal` Under `2026-03`, software, managed, eu, standard gives `1000000`, shown `EUR 10,000`. `src: Core features rule 5`
- [ ] `C-CF-302` `constraint` The network address used for repeat refusal is written to no table. `src: Core features rule 9`
- [ ] `C-CF-303` `constraint` No identifier about a visitor is generated, stored or transmitted. `src: Core features rule 28`
- [ ] `C-CF-304` `capability` The composer capability choices read `Software & Platforms`, `High-performing websites`, `Managed hosting, privacy-first`. `src: Core features rule 3`
- [ ] `C-CF-305` `literal` A recorded check status is `up`, `slow`, `degraded` or `down`. `src: Core features rule 12`
- [ ] `C-CF-306` `capability` The `Systems` tile shows the count of systems. `src: Core features rule 16`
- [ ] `C-CF-307` `capability` Every public route ends with the same footer. `src: Core features rule 25`
- [ ] `C-CF-308` `capability` With scripts off every public route is legible, styled. `src: Core features rule 22`
- [ ] `C-CF-309` `capability` A revealed paragraph reads in full with styles switched off. `src: Core features rule 22`
- [ ] `C-CF-310` `capability` The legal documents set a centred column of text. `src: Core features rule 24`
- [ ] `C-CF-311` `capability` The legal back link sits in flow at the top of the page. `src: Core features rule 24`
- [ ] `C-CF-312` `capability` The founder adds a build record from the side panel on `/studio/builds`. `src: Core features rule 29`
- [ ] `C-CF-313` `capability` The founder unpublishes a build record from `/studio/builds`, the record then leaving `/builds`. `src: Core features rule 29`

## C-UF User flow

- [ ] `C-UF-01` `literal` The route `/builds/<slug>` shows one published build record without a session. `src: User flow route table`
- [ ] `C-UF-02` `literal` The route `/signup` creates a `client`. `src: User flow route table`
- [ ] `C-UF-03` `role` The routes `/studio/builds`, `/studio/systems`, `/studio/page-views` require the `founder` role. `src: User flow route table`
- [ ] `C-UF-04` `capability` A signed-out visitor opening `/account` or a `/studio` route is sent to `/login`. `src: User flow entry and redirects`
- [ ] `C-UF-05` `capability` Signing out returns to `/`. `src: User flow entry and redirects`
- [ ] `C-UF-06` `capability` Any action sent with a session that has gone missing, a build request among them, is refused with `401`, writing nothing. `src: User flow entry and redirects`
- [ ] `C-UF-07` `capability` A sign-in started from the composer's `Sign in` link returns to that exact composer address with every field restored. `src: User flow entry and redirects`
- [ ] `C-UF-08` `ui` A client opening a studio route is told the page belongs to the studio. `src: User flow entry and redirects`
- [ ] `C-UF-09` `literal` The board lists `Vela Studio` first with `Anton Ferber Portfolio` last. `src: User flow watcher journey`
- [ ] `C-UF-10` `literal` The seeded card for `Anton Ferber Portfolio` reads `Awaiting checks`. `src: User flow watcher journey`
- [ ] `C-UF-11` `literal` Software, handover, de, standard shows the figure `EUR 14,500`. `src: User flow buyer journey`
- [ ] `C-UF-12` `capability` A client finds a request sent during a signed-in session on `/account` with the status `new`. `src: User flow client journey`
- [ ] `C-UF-13` `capability` The founder downloads an attached brief from the side panel. `src: User flow founder journey`
- [ ] `C-UF-14` `capability` A record the founder publishes in `/studio/builds` appears on `/builds`. `src: User flow founder journey`
- [ ] `C-UF-15` `capability` A portrait the founder uploads appears on `/about`. `src: User flow founder journey`
- [ ] `C-UF-16` `literal` The address `/builds/aurora-payroll-portal` answers not-found. `src: User flow refused journey`
- [ ] `C-UF-17` `literal` The board empty state reads `No systems available`. `src: User flow states`
- [ ] `C-UF-18` `literal` The library empty state reads `No build records yet.` `src: User flow states`
- [ ] `C-UF-19` `literal` An empty request list reads `No requests yet.` `src: User flow states`
- [ ] `C-UF-20` `ui` Every page that fetches shows a loading state. `src: User flow states`
- [ ] `C-UF-21` `ui` The composer marks each invalid field inline, naming the field. `src: User flow states`
- [ ] `C-UF-22` `constraint` No error ever shows a raw server page. `src: User flow states`
- [ ] `C-UF-23` `literal` The route `/studio/portrait` holds the portrait upload for the `founder`. `src: User flow route table`
- [ ] `C-UF-24` `literal` An overdue check shows `Due now` on the `Next check` tile. `src: User flow watcher journey`
- [ ] `C-UF-25` `capability` The studio top bar ends at the right with a `Sign out` button. `src: Core features rule 29`
- [ ] `C-UF-26` `capability` The `/account` page carries a `Sign out` button above the request list. `src: Core features rule 29`
- [ ] `C-UF-27` `capability` After a missing-session refusal the page goes to `/login`, from a composer page returning after sign-in to the same composer address. `src: User flow entry and redirects`
- [ ] `C-UF-28` `literal` A scripted submission shows `Request received` with the new reference. `src: User flow buyer journey`
- [ ] `C-UF-29` `literal` The route `/impressum` serves the legal notice without a session. `src: User flow route table`
- [ ] `C-UF-30` `literal` The route `/agb` serves the terms without a session. `src: User flow route table`
- [ ] `C-UF-31` `capability` The signed-in founder appends a note to an incident from the site, the note then showing last on the incident page. `src: User flow founder journey`
- [ ] `C-UF-32` `capability` The founder records checks for a system from `/studio/systems`. `src: User flow founder journey`
- [ ] `C-UF-33` `capability` The `/account` list offers a download of the brief attached to each own request. `src: User flow client journey`
- [ ] `C-UF-34` `capability` A brief attached in the composer is stored as the attachment of the new request, with scripts running or switched off. `src: User flow buyer journey`
- [ ] `C-UF-35` `capability` The founder adds a system from the side panel on `/studio/systems`. `src: User flow founder journey`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The whole site reads as one near-black sheet with darkness over decoration. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The landing blocks plus the status blocks sit on a ground one step warmer than the page ground. `src: UI/UX notes palette`
- [ ] `C-UX-03` `ui` A warm amber marks every link, every label that matters, every drawn accent stroke, nothing decorative. `src: UI/UX notes palette`
- [ ] `C-UX-04` `ui` A lighter amber marks the hover of a solid amber fill. `src: UI/UX notes palette`
- [ ] `C-UX-05` `ui` Ledes, notes, the back pill label use a mid neutral text colour. `src: UI/UX notes palette`
- [ ] `C-UX-06` `ui` A word not yet revealed starts as a deep neutral. `src: UI/UX notes palette`
- [ ] `C-UX-07` `ui` Status colours run amber for operational, lighter amber for slow, amber toward red for degraded, soft red for down, the deep neutral for unknown. `src: UI/UX notes palette`
- [ ] `C-UX-08` `ui` An edge is one hairline of translucent white. `src: UI/UX notes palette`
- [ ] `C-UX-09` `ui` A raised surface is a faint white wash over the ground, never an opaque grey panel. `src: UI/UX notes palette`
- [ ] `C-UX-10` `literal` Sentences, headings, the underlined hero link, the legal back link use `Geist`. `src: UI/UX notes type and shape`
- [ ] `C-UX-11` `literal` Eyebrows, the hero meta line, the hero foot, the back pill, the card links, the notice link, the status tile labels, card labels, pill use `Geist Mono` in capitals with wide tracking. `src: UI/UX notes type and shape`
- [ ] `C-UX-12` `capability` Changing status board numbers use figures of equal width. `src: UI/UX notes type and shape`
- [ ] `C-UX-13` `capability` Display type stretches with the window; small type never does. `src: UI/UX notes type and shape`
- [ ] `C-UX-14` `ui` On load the opening block lines rise one after another from slightly below, sharpening as the lines arrive. `src: UI/UX notes motion`
- [ ] `C-UX-15` `ui` The back pill dot breathes. `src: UI/UX notes motion`
- [ ] `C-UX-16` `ui` The teaser arrow nudges sideways, stopping the moment the arrow is pointed at. `src: UI/UX notes motion`
- [ ] `C-UX-17` `ui` A solid amber block cursor blinks at the end of the contact line. `src: UI/UX notes motion`
- [ ] `C-UX-18` `ui` The status skeleton shimmers until the first numbers load. `src: UI/UX notes motion`
- [ ] `C-UX-19` `ui` Amber things turn white on hover; white or grey things turn amber. `src: UI/UX notes motion`
- [ ] `C-UX-20` `capability` No hover transition takes longer than a fifth of a second. `src: UI/UX notes motion`
- [ ] `C-UX-21` `ui` On hover only the main button lifts, only an uptime bar grows taller. `src: UI/UX notes motion`
- [ ] `C-UX-22` `ui` The dot beside a healthy system pulses gently; every other status dot sits still. `src: UI/UX notes motion`
- [ ] `C-UX-23` `ui` Nothing bounces. `src: UI/UX notes motion`
- [ ] `C-UX-24` `capability` A reduced motion preference stops every loop plus the entrance. `src: UI/UX notes motion`
- [ ] `C-UX-25` `ui` The story routes are spacious with one proportional side gutter. `src: UI/UX notes density and layout`
- [ ] `C-UX-26` `ui` The legal routes hold a fixed comfortable reading width. `src: UI/UX notes density and layout`
- [ ] `C-UX-27` `ui` The studio has a top bar over card grids with side panels. `src: UI/UX notes density and layout`
- [ ] `C-UX-28` `ui` Each capability card puts the drawing below the text a little below a small laptop width. `src: UI/UX notes responsive`
- [ ] `C-UX-29` `ui` The founder page gains a second column for the portrait at a wider width. `src: UI/UX notes responsive`
- [ ] `C-UX-30` `ui` At a phone width the headline wraps, with fewer, wider uptime bars. `src: UI/UX notes responsive`
- [ ] `C-UX-31` `capability` On any route at any viewport nothing scrolls sideways. `src: UI/UX notes responsive`
- [ ] `C-UX-32` `capability` At a narrow viewport every footer link stays reachable. `src: UI/UX notes responsive`
- [ ] `C-UX-33` `ui` On a phone the first screen plus each pinned panel fill what is visible with the address bar showing. `src: UI/UX notes responsive`
- [ ] `C-UX-34` `capability` Every interactive element shows a visible amber focus ring on keyboard focus. `src: UI/UX notes accessibility`
- [ ] `C-UX-35` `ui` The focus ring on the amber button turns dark. `src: UI/UX notes accessibility`
- [ ] `C-UX-36` `capability` Keyboard navigation reaches every interactive element. `src: UI/UX notes accessibility`
- [ ] `C-UX-37` `ui` Every genuine target is comfortably sized for a finger. `src: UI/UX notes accessibility`
- [ ] `C-UX-38` `capability` Every drawing carries a sentence of description. `src: UI/UX notes accessibility`
- [ ] `C-UX-39` `capability` Every decorative layer is hidden from assistive technology. `src: UI/UX notes accessibility`
- [ ] `C-UX-40` `capability` Every content image carries alternative text. `src: UI/UX notes accessibility`
- [ ] `C-UX-41` `capability` Every status pill states the status in words. `src: UI/UX notes accessibility`
- [ ] `C-UX-42` `capability` The board announces loading. `src: UI/UX notes accessibility`
- [ ] `C-UX-43` `capability` The status page places a heading level under the page title above each system name. `src: UI/UX notes accessibility`
- [ ] `C-UX-44` `capability` In forced colours the drawings keep their strokes. `src: UI/UX notes accessibility`
- [ ] `C-UX-45` `capability` The site is dark only, with no light mode. `src: UI/UX notes palette`
- [ ] `C-UX-46` `capability` Every icon-only control carries a label. `src: UI/UX notes accessibility`
- [ ] `C-UX-47` `ui` Pills are fully rounded; cards, tiles, panels have soft generous corners. `src: UI/UX notes type and shape`
- [ ] `C-UX-48` `ui` Exactly five things move on their own after load. `src: UI/UX notes motion`
- [ ] `C-UX-49` `capability` The board announces a failure. `src: UI/UX notes accessibility`
- [ ] `C-UX-50` `capability` Focus order follows the page, text before drawing. `src: UI/UX notes accessibility`
- [ ] `C-UX-51` `capability` Focusing an element below the fold scrolls to the element without snapping back. `src: UI/UX notes accessibility`
- [ ] `C-UX-52` `capability` Every section is labelled by its heading. `src: UI/UX notes accessibility`
- [ ] `C-UX-53` `constraint` Nothing loops quickly. `src: UI/UX notes motion`
- [ ] `C-UX-54` `capability` Legal body text is a near-white warm neutral. `src: UI/UX notes palette`
- [ ] `C-UX-55` `capability` Eyebrows plus small labels use a fainter mid neutral. `src: UI/UX notes palette`
- [ ] `C-UX-56` `capability` The status tiles plus the card values fill rows by a minimum width. `src: UI/UX notes responsive`
- [ ] `C-UX-57` `capability` A wider founder page swaps the small avatar for the large portrait. `src: UI/UX notes responsive`
- [ ] `C-UX-58` `capability` The pinned sections keep their timing when the address bar hides. `src: UI/UX notes responsive`
- [ ] `C-UX-59` `capability` Buttons are fully rounded. `src: UI/UX notes type and shape`
- [ ] `C-UX-60` `capability` Target size comes from padding rather than a bigger visual box; the uptime bars are no targets. `src: UI/UX notes accessibility`
- [ ] `C-UX-61` `capability` Sentences use a near-white neutral. `src: UI/UX notes palette`
- [ ] `C-UX-62` `capability` Grotesk headings are tracked tight. `src: UI/UX notes type and shape`
- [ ] `C-UX-63` `capability` The uptime bars are barely rounded. `src: UI/UX notes type and shape`
- [ ] `C-UX-64` `capability` A hover changing a background or a border takes a touch longer than a hover changing a colour. `src: UI/UX notes motion`
- [ ] `C-UX-65` `capability` The light wash ends in a near-black neutral at the foot of the page. `src: UI/UX notes palette`
- [ ] `C-UX-66` `capability` Every label, number, link outside `Geist` is set in the mono face. `src: UI/UX notes type and shape`
- [ ] `C-UX-67` `capability` The card number keeps its digits with wide tracking. `src: UI/UX notes type and shape`
- [ ] `C-UX-68` `capability` The footer links, the teaser, the mail link keep their written case with slight tracking. `src: UI/UX notes type and shape`
- [ ] `C-UX-69` `capability` The contact line keeps its written case with tight tracking. `src: UI/UX notes type and shape`
- [ ] `C-UX-70` `capability` The portal host inside the notice link keeps its written case with no added tracking. `src: UI/UX notes type and shape`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Three faint pools of warm light sit behind the page. `src: Front-end specification chrome`
- [ ] `C-FE-02` `ui` A dot grid fades out before the window corners. `src: Front-end specification chrome`
- [ ] `C-FE-03` `ui` A fine grain film covers only `/` plus `/about`. `src: Front-end specification chrome`
- [ ] `C-FE-04` `constraint` The wash, the grid, the grain are drawn by the page, never fetched. `src: Front-end specification chrome`
- [ ] `C-FE-05` `ui` The footer is a centred row of small mono links under a hairline. `src: Front-end specification chrome`
- [ ] `C-FE-06` `ui` The back pill is a frosted rounded tab at the top left holding a breathing amber dot beside a left arrow. `src: Front-end specification chrome`
- [ ] `C-FE-07` `ui` Selected text sits on the amber. `src: Front-end specification chrome`
- [ ] `C-FE-08` `literal` Body copy is `16px`; every eyebrow is `11px`. `src: Front-end specification type sizes`
- [ ] `C-FE-09` `literal` The hero title is `100.8px` wide, `69.3px` at tablet width, `32.76px` on a phone. `src: Front-end specification type sizes`
- [ ] `C-FE-10` `literal` The pinned statement is `66.24px`, `45.54px`, `32px` at the three widths. `src: Front-end specification type sizes`
- [ ] `C-FE-11` `literal` A card heading is `48px` on a wide window; a card body is `23.04px` wide, `16.8px` below. `src: Front-end specification type sizes`
- [ ] `C-FE-12` `literal` The mono contact line is `70.4px`, `51.48px`, `22.4px`. `src: Front-end specification type sizes`
- [ ] `C-FE-13` `literal` A status system name is `19px`; a status tile value is `26px`. `src: Front-end specification type sizes`
- [ ] `C-FE-14` `literal` Legal body text is `15px` under a `20px` clause heading. `src: Front-end specification type sizes`
- [ ] `C-FE-15` `ui` The hero stays still when the real font arrives. `src: Front-end specification type sizes`
- [ ] `C-FE-16` `ui` The primary button is a solid amber pill with near-black text, one per page at most. `src: Front-end specification controls`
- [ ] `C-FE-17` `literal` Card `02` drawing carries a description beginning `Diagram: interface, API`. `src: Front-end specification home diagrams`
- [ ] `C-FE-18` `literal` Card `03` drawing carries the description `Diagram: a browser window with Core Web Vitals scores`. `src: Front-end specification home diagrams`
- [ ] `C-FE-19` `literal` Card `04` drawing carries the description `Diagram: a server rack with encrypted uplinks`. `src: Front-end specification home diagrams`
- [ ] `C-FE-20` `literal` Card `05` drawing carries a description beginning `Diagram: four interconnected nodes across Falkenstein`. `src: Front-end specification home diagrams`
- [ ] `C-FE-21` `literal` Card `02` drawing words are `interface`, `api`, `workers`, `postgres`. `src: Front-end specification home diagrams`
- [ ] `C-FE-22` `literal` Card `03` drawing words are `LCP 0.6s`, `CLS 0.00`, `100 / 100`. `src: Front-end specification home diagrams`
- [ ] `C-FE-23` `literal` Card `04` drawing words are `uplink`, `encrypted`. `src: Front-end specification home diagrams`
- [ ] `C-FE-24` `literal` Card `05` drawing words are `FSN`, `FRA`, `EYG-1`, `EYG-2`. `src: Front-end specification home diagrams`
- [ ] `C-FE-25` `ui` The card `03` drawing fills the first fifth of the progress track in amber. `src: Front-end specification home diagrams`
- [ ] `C-FE-26` `ui` The card `04` drawing shows a small amber padlock. `src: Front-end specification home diagrams`
- [ ] `C-FE-27` `ui` The card `05` drawing shows four amber rounded squares at the corners of a square with two faint diagonals. `src: Front-end specification home diagrams`
- [ ] `C-FE-28` `ui` A drawing extends past the drawing box without clipping. `src: Front-end specification home diagrams`
- [ ] `C-FE-29` `ui` The next card slides over the previous card with a leading hairline under an upward shadow. `src: Front-end specification pinned card`
- [ ] `C-FE-30` `literal` Cards `02` to `04` carry the eyebrow `Capability`; card `05` carries `Infrastructure`. `src: Front-end specification pinned card`
- [ ] `C-FE-31` `ui` Wheel plus keyboard scrolling glide; touch scrolling stays with the device. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-32` `ui` Find-in-page repaints the reveal for where the page lands. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-33` `ui` The status board fades each block into place once on entry, cards arriving after the first paint among them. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-34` `literal` The hero meta line reads a small amber dot, `Vela Studio`, a slash, `Marburg, DE`. `src: Front-end specification home route`
- [ ] `C-FE-35` `literal` The hero title reads `Software built in Germany.` over `Hosted in Europe.` `src: Front-end specification home route`
- [ ] `C-FE-36` `literal` The hero lede begins `We write production software`. `src: Front-end specification home route`
- [ ] `C-FE-37` `literal` The hero foot names `Frankfurt`, `Falkenstein`, `Eygelshoven` beside `Scroll`. `src: Front-end specification home route`
- [ ] `C-FE-38` `literal` The philosophy eyebrow reads `01 - Philosophy`. `src: Front-end specification home route`
- [ ] `C-FE-39` `literal` The philosophy statement begins `We build privacy-first software`. `src: Front-end specification home route`
- [ ] `C-FE-40` `literal` The philosophy amber words are `reliable`, `transparent`, `entirely yours`, `never a black box`. `src: Front-end specification home route`
- [ ] `C-FE-41` `literal` The heading row reads `What we build` beside the eyebrow `Capabilities`. `src: Front-end specification home route`
- [ ] `C-FE-42` `literal` The in-page anchors are `#leistungen` for the heading row, `#kontakt` for contact. `src: Front-end specification home route`
- [ ] `C-FE-43` `literal` The card headings read `Software & Platforms`, `High-performing websites`, `Managed hosting, privacy-first`, `Four nodes. One jurisdiction.` `src: Front-end specification home route table`
- [ ] `C-FE-44` `literal` The card bodies begin `SaaS products`, `Marketing sites`, `Your workload runs`, `Falkenstein, Frankfurt`. `src: Front-end specification home route table`
- [ ] `C-FE-45` `literal` The contact eyebrow reads `06 - Contact`. `src: Front-end specification home route`
- [ ] `C-FE-46` `literal` The contact note begins `Reply within one working day`. `src: Front-end specification home route`
- [ ] `C-FE-47` `literal` The contact mail link is `hello@vela.example.com`. `src: Front-end specification home route`
- [ ] `C-FE-48` `literal` The teaser reads `Curious who's actually behind the racks?` over `(a real human)`. `src: Front-end specification home route`
- [ ] `C-FE-49` `literal` The founder page meta line reads `About`, a slash, `Anton Ferber`. `src: Front-end specification founder page`
- [ ] `C-FE-50` `literal` The founder page title reads `Why I build` over `Vela Studio.` `src: Front-end specification founder page`
- [ ] `C-FE-51` `literal` The founder page lede begins `I'm Anton.` `src: Front-end specification founder page`
- [ ] `C-FE-52` `literal` Statement `01 - The craft` begins `I build software the way`. `src: Front-end specification founder page`
- [ ] `C-FE-53` `literal` Statement `02 - The principle` begins `Privacy isn't a feature`. `src: Front-end specification founder page`
- [ ] `C-FE-54` `literal` The founder contact reads `03 - Elsewhere` with the link `anton-ferber.example.com`. `src: Front-end specification founder page`
- [ ] `C-FE-55` `ui` The founder page prompt line rests white, turning amber on hover. `src: Front-end specification founder page`
- [ ] `C-FE-56` `literal` The status eyebrow reads `System status` in amber. `src: Front-end specification status board`
- [ ] `C-FE-57` `literal` The status heading reads `Live reliability, shown in public.` `src: Front-end specification status board`
- [ ] `C-FE-58` `literal` The status words read `Operational`, `Slow`, `Degraded`, `Down`, `Unknown`. `src: Front-end specification status board`
- [ ] `C-FE-59` `literal` Each bar carries the `title` attribute `<status word> at <time>`, as in `Operational at 1 Sept 2026, 15:38`. `src: Front-end specification status board`
- [ ] `C-FE-60` `literal` Each bar strip carries the `aria-label` `Recent uptime history for <system name>`. `src: Front-end specification status board`
- [ ] `C-FE-61` `literal` The failure block reads `Status temporarily unavailable` with the feed's own message, falling back to `The uptime feed is unavailable.` `src: Front-end specification status board`
- [ ] `C-FE-62` `literal` The empty block reads `No monitored systems are currently visible.` `src: Front-end specification status board`
- [ ] `C-FE-63` `literal` The seven systems in order are `Vela Studio`, `Vela Studio Finance`, `Vela Studio Analytics`, `Vela Studio Console`, `Vela Studio DB Controller`, `Vela Studio Tickets`, `Anton Ferber Portfolio`. `src: Front-end specification status board table`
- [ ] `C-FE-64` `literal` The notice link reads `Open customer portal` with the host `portal.vela.example.com`. `src: Front-end specification status board`
- [ ] `C-FE-65` `constraint` The notice link opens a new tab, passing no referrer. `src: Front-end specification status board`
- [ ] `C-FE-66` `literal` The legal notice carries the eyebrow `LEGAL NOTICE` over a heading beginning `Information pursuant to`. `src: Front-end specification legal documents`
- [ ] `C-FE-67` `literal` The provider block reads `Ketzerbach 21` over `35037 Marburg`. `src: Front-end specification legal documents`
- [ ] `C-FE-68` `literal` The legal notice lists the phone number `+49 6421 555 0142`. `src: Front-end specification legal documents`
- [ ] `C-FE-69` `literal` The VAT line reads `VAT identification number: DE123456789`. `src: Front-end specification legal documents`
- [ ] `C-FE-70` `literal` The legal notice holds nine blocks from `Provider` to `Copyright`. `src: Front-end specification legal documents`
- [ ] `C-FE-71` `capability` German legal terms inside the English text are marked as German. `src: Front-end specification legal documents`
- [ ] `C-FE-72` `literal` The terms carry the eyebrow `TERMS` over a heading beginning `General Terms`. `src: Front-end specification legal documents`
- [ ] `C-FE-73` `literal` The terms hold eight numbered clauses from `1. Scope` to `8. Final provisions`. `src: Front-end specification legal documents`
- [ ] `C-FE-74` `capability` Clause 5 says the site claims describe the technical approach, not a guaranteed service level. `src: Front-end specification legal documents`
- [ ] `C-FE-75` `literal` The library heading reads `Builds`. `src: Front-end specification build library`
- [ ] `C-FE-76` `literal` The library filters read `All`, `Software & Platforms`, `High-performing websites`, `Managed hosting, privacy-first`. `src: Front-end specification build library`
- [ ] `C-FE-77` `literal` The residency choices read `Anywhere in the EU`, `Germany only`. `src: Front-end specification build library`
- [ ] `C-FE-78` `literal` The timeline choices read `Flexible`, `Standard`, `Accelerated`. `src: Front-end specification build library`
- [ ] `C-FE-79` `literal` The budget choices read `Under EUR 10,000`, `EUR 10,000 to 25,000`, `EUR 25,000 to 60,000`, `Over EUR 60,000`. `src: Front-end specification build library`
- [ ] `C-FE-80` `literal` The managed posture label ends `on our racks`; the handover posture label ends `to run yourself`. `src: Front-end specification build library`
- [ ] `C-FE-81` `literal` The figure is labelled `Indicative figure`; the send button reads `Send build request`. `src: Front-end specification build library`
- [ ] `C-FE-82` `literal` The form controls are named `capabilities`, `posture`, `residency`, `timeline`, `budget_band`, `description`, `contact_name`, `contact_email`, `contact_fax`, `rules_version`, `indicative_minor`, `attachment`. `src: Front-end specification build library`
- [ ] `C-FE-83` `literal` The account page heading reads `Your build requests`. `src: Front-end specification build library`
- [ ] `C-FE-84` `literal` The home title joins the studio name to `Software Made in Germany, Hosted in Europe` with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-85` `literal` The founder page title joins `About` to the studio name with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-86` `literal` The status board title joins `System Status` to the studio name with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-87` `literal` The legal notice title joins `Legal Notice` to the studio name with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-88` `literal` The terms title joins `Terms & Conditions` to the studio name with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-89` `literal` The library title joins `Builds` to the studio name with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-90` `literal` The composer title joins `Build request` to the studio name with a bar. `src: Front-end specification metadata`
- [ ] `C-FE-91` `capability` No two public routes share a title or a description. `src: Front-end specification metadata`
- [ ] `C-FE-92` `literal` The home description mentions `hosted in Europe on privacy-first infrastructure`. `src: Front-end specification metadata`
- [ ] `C-FE-93` `capability` Every public route declares a canonical address. `src: Front-end specification metadata`
- [ ] `C-FE-94` `capability` Every public route declares a social card whose large preview image resolves. `src: Front-end specification metadata`
- [ ] `C-FE-95` `literal` The preview image alternative text reads `Vela Studio - Software that scales`. `src: Front-end specification metadata`
- [ ] `C-FE-96` `constraint` No header menu, comparison table, questions-and-answers block, large multi-column footer, animated map or founder-notes panel is built. `src: Front-end specification not built`
- [ ] `C-FE-97` `constraint` The status shell carries no grain. `src: Front-end specification architecture`
- [ ] `C-FE-98` `ui` The scroll reveal adds nothing visible of the reveal's own to the page. `src: Front-end specification architecture`
- [ ] `C-FE-99` `constraint` The public routes remember nothing about the visitor from one page to the next. `src: Front-end specification architecture`
- [ ] `C-FE-100` `ui` The portrait stand-in is drawn in the page with an open amber arc of light. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-101` `capability` The social card is generated from the ground, wash, wordmark, one amber dot, tagline rather than drawn by hand. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-102` `ui` The home prompt line rests white, turning amber on hover. `src: Front-end specification home route`
- [ ] `C-FE-103` `ui` The home mail link rests amber, turning white on hover. `src: Front-end specification home route`
- [ ] `C-FE-104` `ui` The founder page link under the prompt rests white, turning amber on hover. `src: Front-end specification founder page`
- [ ] `C-FE-105` `capability` Text appears at once in a fallback face, replaced by the real face without moving a line. `src: Front-end specification type sizes`
- [ ] `C-FE-106` `capability` The smoothed scrolling, the grain, the reveals never appear on a route whose shell lacks them. `src: Front-end specification architecture`
- [ ] `C-FE-107` `literal` The type sizes are measured at windows `1440`, `990`, `390` pixels wide. `src: Front-end specification type sizes`
- [ ] `C-FE-108` `capability` Apostrophes in the copy are plain straight apostrophes. `src: Front-end specification home route`
- [ ] `C-FE-109` `literal` Card `02` marks `maintainable`, `entirely yours` in amber. `src: Front-end specification home route table`
- [ ] `C-FE-110` `literal` Card `03` marks `under a second`, `no tracking scripts` in amber. `src: Front-end specification home route table`
- [ ] `C-FE-111` `literal` Card `04` marks `our own hardware`, `GDPR is the floor` in amber. `src: Front-end specification home route table`
- [ ] `C-FE-112` `literal` Card `05` marks `Our racks, our keys` in amber. `src: Front-end specification home route table`
- [ ] `C-FE-113` `literal` Statement `01 - The craft` marks `owned outright`, `documented`, `hardware I can point to` in amber. `src: Front-end specification founder page`
- [ ] `C-FE-114` `literal` Statement `02 - The principle` marks `the starting condition`, `answerable to you` in amber. `src: Front-end specification founder page`
- [ ] `C-FE-115` `literal` The document head names the site `Vela Studio`. `src: Front-end specification metadata`
- [ ] `C-FE-116` `literal` The document head gives the category `Software development`. `src: Front-end specification metadata`
- [ ] `C-FE-117` `capability` Every public page allows indexing plus following. `src: Front-end specification metadata`
- [ ] `C-FE-118` `literal` The status lede begins `Every Vela Studio system, monitored continuously.` `src: Front-end specification status board`
- [ ] `C-FE-119` `literal` The status notice reads `Looking for incident history, deeper diagnostics, or want to open a ticket? Full detail lives in the customer portal.` `src: Front-end specification status board`
- [ ] `C-FE-120` `literal` The failure block states `The live status feed could not be loaded right now.` `src: Front-end specification status board`
- [ ] `C-FE-121` `literal` The empty block heading reads `No systems available`. `src: Front-end specification status board`
- [ ] `C-FE-122` `literal` The empty block adds `The monitoring feed returned an empty project scope.` `src: Front-end specification status board`
- [ ] `C-FE-123` `literal` The legal notice names the blocks `Contact`, `Registered office`, `VAT`, `Responsible for content`, `Liability for content`, `Liability for links`. `src: Front-end specification legal documents`
- [ ] `C-FE-124` `capability` The legal contact block links the phone number, the email address, the `WhatsApp Business:` number. `src: Front-end specification legal documents`
- [ ] `C-FE-125` `literal` The terms name the clauses `2. Services`, `3. Client cooperation`, `4. Fees`, `5. Operations`, `6. Rights of use`, `7. Liability`. `src: Front-end specification legal documents`
- [ ] `C-FE-126` `literal` The hero lede is `18px` on a wide window, `16px` below. `src: Front-end specification type sizes`
- [ ] `C-FE-127` `literal` The section heading `What we build` is `48px` on a wide window. `src: Front-end specification type sizes`
- [ ] `C-FE-128` `literal` The status heading is at most `64px`. `src: Front-end specification type sizes`
- [ ] `C-FE-129` `literal` Legal body text drops to `14px` on a phone. `src: Front-end specification type sizes`
- [ ] `C-FE-130` `literal` A legal clause heading drops to `17px` on a phone. `src: Front-end specification type sizes`
- [ ] `C-FE-131` `literal` A status card value is `16px`. `src: Front-end specification type sizes`
- [ ] `C-FE-132` `literal` A status feedback heading is `20px`. `src: Front-end specification type sizes`
- [ ] `C-FE-133` `constraint` The chrome layers never intercept the pointer. `src: Front-end specification chrome`
- [ ] `C-FE-134` `constraint` The chrome layers never repaint on scroll. `src: Front-end specification chrome`
- [ ] `C-FE-135` `constraint` The grain never shows colour. `src: Front-end specification chrome`
- [ ] `C-FE-136` `capability` Where the browser cannot fade or blend, the dot grid is hidden, the grain shown fainter. `src: Front-end specification chrome`
- [ ] `C-FE-137` `capability` Selected text sits on two-thirds amber. `src: Front-end specification chrome`
- [ ] `C-FE-138` `constraint` The overscroll area is never white. `src: Front-end specification chrome`
- [ ] `C-FE-139` `capability` Each capability card is three windows tall around a one-window panel. `src: Front-end specification pinned card`
- [ ] `C-FE-140` `capability` The outgoing card's text stays selectable. `src: Front-end specification pinned card`
- [ ] `C-FE-141` `capability` A card body reveal finishes with a little over a fifth of the hold to spare. `src: Front-end specification pinned card`
- [ ] `C-FE-142` `capability` The philosophy statement reveal finishes with a seventh of the hold to spare. `src: Front-end specification pinned card`
- [ ] `C-FE-143` `constraint` Native scrolling is never disabled. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-144` `constraint` No wrapper is moved to imitate scrolling. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-145` `capability` Keyboard focus, scroll-into-view, back, forward, scrollbar drag, resize, rotation, font arrival each update the reveal. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-146` `capability` The punctuation after an amber phrase lights as a step of its own. `src: Front-end specification home route`
- [ ] `C-FE-147` `capability` The long dash reveals as a word of its own. `src: Front-end specification home route`
- [ ] `C-FE-148` `capability` Structural strokes are translucent white. `src: Front-end specification home diagrams`
- [ ] `C-FE-149` `capability` A filled dot appears rather than draws. `src: Front-end specification home diagrams`
- [ ] `C-FE-150` `capability` A shape that reports no length fades in instead of drawing. `src: Front-end specification home diagrams`
- [ ] `C-FE-151` `capability` The card `05` city names sit in the fainter neutral. `src: Front-end specification home diagrams`
- [ ] `C-FE-152` `capability` The underlined text link is a mid neutral sentence-case link turning white on hover. `src: Front-end specification controls`
- [ ] `C-FE-153` `capability` The teaser is the only link on `/` to the founder page. `src: Front-end specification home route`
- [ ] `C-FE-154` `literal` The founder page foot reads `Marburg`, a middle dot, `Germany`, with `Scroll` on the right. `src: Front-end specification founder page`
- [ ] `C-FE-155` `constraint` Only one of the portrait or the avatar is ever shown. `src: Front-end specification founder page`
- [ ] `C-FE-156` `capability` The portrait rises into place a moment after the text. `src: Front-end specification founder page`
- [ ] `C-FE-157` `capability` The status skeleton is three placeholder cards, each with two shimmering lines over a row of bars. `src: Front-end specification status board`
- [ ] `C-FE-158` `literal` A status tile label is `10px`. `src: Front-end specification type sizes`
- [ ] `C-FE-159` `literal` A footer link is `12px`. `src: Front-end specification type sizes`
- [ ] `C-FE-160` `capability` The legal page heading is the tightest-tracked text on the site. `src: Front-end specification type sizes`
- [ ] `C-FE-161` `constraint` Both font families are variable. `src: Front-end specification type sizes`
- [ ] `C-FE-162` `capability` Text is antialiased in greyscale on every route. `src: Front-end specification type sizes`
- [ ] `C-FE-163` `capability` The pinned statement holds a narrow measure of about twenty characters. `src: Front-end specification type sizes`
- [ ] `C-FE-164` `capability` Each hero line is held on one line on wider windows, the second in the mid neutral. `src: Front-end specification type sizes`
- [ ] `C-FE-165` `capability` The page shows softly through the frosted back pill. `src: Front-end specification chrome`
- [ ] `C-FE-166` `capability` Where frosting is unavailable the back pill ground simply darkens. `src: Front-end specification chrome`
- [ ] `C-FE-167` `capability` The back pill sits above the grain. `src: Front-end specification chrome`
- [ ] `C-FE-168` `capability` Each section glow sits behind the content of its own section. `src: Front-end specification chrome`
- [ ] `C-FE-169` `capability` The mono arrow link is amber capitals followed by an arrow, link plus arrow turning white on hover. `src: Front-end specification controls`
- [ ] `C-FE-170` `capability` The card `02` drawing shows an amber box above two boxes over a fainter box, joined by four elbow lines, with an amber dot in the top box. `src: Front-end specification home diagrams`
- [ ] `C-FE-171` `capability` The card `03` drawing shows a window frame with a title bar rule, three dots, three rounded text bars, an amber pill. `src: Front-end specification home diagrams`
- [ ] `C-FE-172` `capability` The card `04` drawing shows six slots, the top slot amber, three status dots, brackets running off each side. `src: Front-end specification home diagrams`
- [ ] `C-FE-173` `capability` The card `05` perimeter is one continuous stroke with an amber dot at each corner. `src: Front-end specification home diagrams`
- [ ] `C-FE-174` `capability` The status notice link carries a drawn arrow of two strokes in the link colour. `src: Front-end specification home diagrams`
- [ ] `C-FE-175` `capability` The slightly wider left side of a pinned card holds a tag row of amber number plus eyebrow, the heading, the body, the arrow link; the drawing sits on the right. `src: Front-end specification pinned card`
- [ ] `C-FE-176` `capability` Words, drawings, hairline, hero are painted together in one frame. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-177` `constraint` Only paragraphs near the window are marked for animation. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-178` `constraint` The painted properties carry no transition of their own. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-179` `constraint` Smoothed scrolling runs on `/`, `/about`, `/uptime` only. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-180` `capability` The hero foot separates the city names by a middle dot with a space either side. `src: Front-end specification home route`
- [ ] `C-FE-181` `capability` The word `Scroll` on the hero foot sits beside a short vertical line fading downward. `src: Front-end specification home route`
- [ ] `C-FE-182` `capability` Soft amber pools of light sit behind the hero, the philosophy section, the contact section. `src: Front-end specification home route`
- [ ] `C-FE-183` `capability` An amber chevron leads the contact prompt. `src: Front-end specification home route`
- [ ] `C-FE-184` `constraint` The document head carries no keyword list. `src: Front-end specification metadata`
- [ ] `C-FE-185` `capability` Each studio side panel reserves the amber for the one action in the panel. `src: Front-end specification build library`
- [ ] `C-FE-186` `literal` The founder page note begins `More of what I make, write`. `src: Front-end specification founder page`
- [ ] `C-FE-187` `literal` A card value label plus the status pill are `10px`. `src: Front-end specification type sizes`
- [ ] `C-FE-188` `literal` The hero foot plus the back pill label are `11px`. `src: Front-end specification type sizes`
- [ ] `C-FE-189` `literal` The hero meta line, the card number, the card links, the notice link are `12px`. `src: Front-end specification type sizes`
- [ ] `C-FE-190` `capability` Each mono label size is the same at every width. `src: Front-end specification type sizes`
- [ ] `C-FE-191` `capability` The legal routes use native scrolling, which glides for an in-page jump. `src: Front-end specification scroll behaviour`
- [ ] `C-FE-192` `capability` The teaser first row is mid neutral, `(a real human)` fainter neutral beside an amber arrow. `src: Front-end specification home route`
- [ ] `C-FE-193` `capability` On teaser hover the link turns white, the parenthetical turning amber. `src: Front-end specification home route`
- [ ] `C-FE-194` `literal` In card `02` `interface` is white; `api`, `workers`, `postgres` are mid neutral. `src: Front-end specification home diagrams`
- [ ] `C-FE-195` `capability` The card `03` progress fill is drawn at twice the track stroke. `src: Front-end specification home diagrams`
- [ ] `C-FE-196` `literal` In card `03` `LCP 0.6s` is amber; `CLS 0.00`, `100 / 100` are mid neutral. `src: Front-end specification home diagrams`
- [ ] `C-FE-197` `capability` Below the amber top slot the card `04` slots fade downward. `src: Front-end specification home diagrams`
- [ ] `C-FE-198` `capability` The card `04` padlock is a body with a curved shackle. `src: Front-end specification home diagrams`
- [ ] `C-FE-199` `capability` Card `05` is the widest of the four drawings. `src: Front-end specification home diagrams`
- [ ] `C-FE-200` `capability` The card `05` diagonals are drawn at a quarter of the perimeter strength. `src: Front-end specification home diagrams`
- [ ] `C-FE-201` `literal` The card `05` city names read `Falkenstein`, `Frankfurt`, `Eygelshoven`, `Eygelshoven`. `src: Front-end specification home diagrams`
- [ ] `C-FE-202` `capability` Each pinned card panel has an opaque ground. `src: Front-end specification pinned card`
- [ ] `C-FE-203` `capability` Below the collapse width a card keeps its timing. `src: Front-end specification pinned card`
- [ ] `C-FE-204` `capability` A card body starts revealing a little way into the hold; the philosophy statement starts later, in a longer hold. `src: Front-end specification pinned card`
- [ ] `C-FE-205` `capability` The board announces the empty block. `src: Front-end specification status board`
- [ ] `C-FE-206` `literal` Board times read like `1 Sept 2026, 15:38`. `src: Front-end specification status board`
- [ ] `C-FE-207` `literal` The provider block reads `Vela Studio`, `Anton Ferber`, `Ketzerbach 21`, `35037 Marburg`, `Germany`, one line each. `src: Front-end specification legal documents`
- [ ] `C-FE-208` `literal` The contact block labels read `Phone:`, `Email:`, `WhatsApp Business:`. `src: Front-end specification legal documents`
- [ ] `C-FE-209` `capability` `Registered office` repeats the address; `Responsible for content` names the founder beside the address. `src: Front-end specification legal documents`
- [ ] `C-FE-210` `capability` Both legal pages carry an amber eyebrow. `src: Front-end specification legal documents`
- [ ] `C-FE-211` `capability` The skeleton shimmer travels along the row of bars. `src: Front-end specification status board`
- [ ] `C-FE-212` `capability` The portal host sits in the fainter neutral. `src: Front-end specification status board`
- [ ] `C-FE-213` `capability` The portrait stand-in holds a soft dark silhouette clipped to a circle. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-214` `capability` The social card plus the square tile are generated at build time from the site tokens. `src: Front-end specification zero-asset substitution`
- [ ] `C-FE-215` `capability` The contact section fills most of a screen. `src: Front-end specification home route`
- [ ] `C-FE-216` `capability` The founder page title wraps within its column. `src: Front-end specification founder page`
- [ ] `C-FE-217` `constraint` The grain sits in the image rather than on top, at a strength that breaks banding, no more. `src: Front-end specification chrome`
- [ ] `C-FE-218` `literal` The composer capability choices are three checkboxes named `capabilities` with the values `software`, `website`, `hosting`. `src: Front-end specification build library`
- [ ] `C-FE-219` `capability` The hero fills the first screen. `src: Front-end specification home route`
- [ ] `C-FE-220` `capability` The four pinned cards run back to back, with nothing stacked as moving layers. `src: Front-end specification pinned card`
- [ ] `C-FE-221` `literal` The seven system slugs in order are `vela-studio`, `vela-studio-finance`, `vela-studio-analytics`, `vela-studio-console`, `vela-studio-db-controller`, `vela-studio-tickets`, `anton-ferber-portfolio`. `src: Front-end specification status board table`

## C-TR Technical requirements

- [ ] `C-TR-01` `literal` The front end is `Alpine.js` layered over server-rendered templates. `src: Technical requirements para 1`
- [ ] `C-TR-02` `literal` The backend with the HTTP API is `Flask` with `Jinja`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `capability` Every route leaves the server as finished markup. `src: Technical requirements para 1`
- [ ] `C-TR-04` `constraint` No animation or smoothing library is added. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` Records live in `PostgreSQL` at `DATABASE_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-06` `literal` Briefs with the portrait live in `minio` at `STORAGE_ENDPOINT`. `src: Technical requirements para 2`
- [ ] `C-TR-07` `literal` The bucket name comes from `STORAGE_BUCKET`. `src: Technical requirements para 2`
- [ ] `C-TR-08` `literal` The storage key pair comes from `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY`. `src: Technical requirements para 2`
- [ ] `C-TR-09` `constraint` Passwords are stored hashed; the app itself checks the password at sign-in, refusing a wrong one. `src: Technical requirements para 2`
- [ ] `C-TR-10` `literal` A successful sign-in returns the account with an `access_token`. `src: Technical requirements para 2`
- [ ] `C-TR-11` `capability` The client sends the token as a bearer token. `src: Technical requirements para 2`
- [ ] `C-TR-12` `capability` Each handled request writes one line to stdout. `src: Technical requirements para 2`
- [ ] `C-TR-13` `constraint` No second database, cache, queue, object store, identity provider or mail vendor is introduced. `src: Technical requirements para 3`
- [ ] `C-TR-14` `constraint` Hosts, ports, keys, passwords come from environment variables. `src: Technical requirements para 3`
- [ ] `C-TR-15` `capability` The board fetches the feed with the browser cache bypassed. `src: Technical requirements feed paragraph`
- [ ] `C-TR-16` `ui` The countdown ticking never makes a card flicker, lose the hover, or jump. `src: Technical requirements feed paragraph`
- [ ] `C-TR-17` `capability` The feed is servable from a short-lived cache without a session. `src: Technical requirements feed paragraph`
- [ ] `C-TR-18` `capability` Each font family loads one Latin subset at first paint. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-19` `constraint` The uploaded portrait is the only photograph, shown with declared dimensions. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-20` `ui` The words beside the drawing on one screen never drift apart during scrolling. `src: Technical requirements smooth scrolling paragraph`
- [ ] `C-TR-21` `ui` A slow frame never makes the reveal jump or skip. `src: Technical requirements smooth scrolling paragraph`
- [ ] `C-TR-22` `constraint` The build request with the page-view record are the only anonymous writes. `src: Technical requirements write paragraph`
- [ ] `C-TR-23` `constraint` Repeat refusal never uses a stored identifier, a cookie, browser storage. `src: Technical requirements write paragraph`
- [ ] `C-TR-24` `constraint` No downloadable asset carries a storage secret or database password. `src: Technical requirements credential paragraph`
- [ ] `C-TR-25` `ui` A long page of revealed paragraphs scrolls as smoothly at the bottom as at the top. `src: Technical requirements smooth scrolling paragraph`
- [ ] `C-TR-26` `capability` The social card with the tile image is generated rather than drawn. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-27` `constraint` Only the libraries named in Technical requirements plus their direct dependencies are used. `src: Technical requirements para 3`
- [ ] `C-TR-28` `capability` The largest paint lands well inside a second plus a quarter. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-29` `capability` Content shifts after appearing by almost nothing. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-30` `capability` The scroll reveal is deferred. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-31` `constraint` No script runs before first paint on the legal routes. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-32` `capability` The status board applies new values without blocking input. `src: Technical requirements feed paragraph`
- [ ] `C-TR-33` `constraint` No bearer token of anybody but the viewer appears in any document, script, stylesheet or source map. `src: Technical requirements credential paragraph`
- [ ] `C-TR-34` `constraint` The document plus the first-paint stylesheet each stay small, with very little script before first paint off the legal routes. `src: Technical requirements budgets paragraph`
- [ ] `C-TR-35` `constraint` A hover or a style change elsewhere on the page never fights the reveal. `src: Technical requirements smooth scrolling paragraph`

## C-DM Data model

- [ ] `C-DM-01` `data` The `accounts` table holds an `email` unique without regard to case beside a `role`. `src: Data model accounts`
- [ ] `C-DM-02` `data` The `systems` table holds a unique `slug`, `name`, a unique `position`, `interval_seconds`, `open_after`, `close_after`. `src: Data model systems`
- [ ] `C-DM-03` `capability` A system created later takes the next position. `src: Data model systems`
- [ ] `C-DM-04` `data` The `checks` table holds `checked_at`, `status`, `response_ms` for the owning system. `src: Data model checks`
- [ ] `C-DM-05` `constraint` The `checks` table never stores `unknown`. `src: Data model checks`
- [ ] `C-DM-06` `data` The `incidents` table holds a unique `ref`, `opened_at`, a `resolved_at` that stays null until the incident resolves. `src: Data model incidents`
- [ ] `C-DM-07` `data` The `incident_entries` table holds `seq`, `kind`, `body`, `recorded_at`. `src: Data model incident_entries`
- [ ] `C-DM-08` `constraint` Rows of `incident_entries` are only ever added. `src: Data model incident_entries`
- [ ] `C-DM-09` `data` The `build_records` table holds `slug`, `title`, `capability`, `stack`, `delivered_on`, `client_visible`, `diagram`, `published`, `published_at`. `src: Data model build_records`
- [ ] `C-DM-10` `data` The `published_at` value is null for an unpublished record. `src: Data model build_records`
- [ ] `C-DM-11` `literal` A measurement `metric` is `lcp_ms`, `cls`, `p95_api_ms` or `uptime_percent`. `src: Data model measurements`
- [ ] `C-DM-12` `data` The `measurements` table holds `metric`, `value`, `measured_on`, `source`. `src: Data model measurements`
- [ ] `C-DM-13` `data` The `build_requests` table holds `reference`, `contact_email`, `capabilities`, `rules_version`, `indicative_minor`, `currency`, `status`, `status_changed_at`. `src: Data model build_requests`
- [ ] `C-DM-14` `constraint` No `build_requests` column holds a network address, browser signature or cookie value. `src: Data model build_requests`
- [ ] `C-DM-15` `data` The `attachments` table holds a unique `object_key`, `content_type`, `byte_size`, `sha256`, `original_name`. `src: Data model attachments`
- [ ] `C-DM-16` `literal` An attachment `content_type` is `application/pdf`, `image/png` or `image/jpeg`. `src: Data model attachments`
- [ ] `C-DM-17` `data` The `page_views` table holds only `route` with `viewed_at`. `src: Data model page_views`
- [ ] `C-DM-18` `data` The `portraits` table holds `object_key`, `content_type`, `uploaded_at`, the newest row shown. `src: Data model portraits`
- [ ] `C-DM-19` `literal` The seed holds seven systems at interval `300` with `open_after` `3`, `close_after` `2`. `src: Data model seed data`
- [ ] `C-DM-20` `capability` The first five seeded systems each hold twelve up checks five minutes apart. `src: Data model seed data`
- [ ] `C-DM-21` `capability` The seeded tickets system has two missing intervals. `src: Data model seed data`
- [ ] `C-DM-22` `capability` The seeded portfolio system has no check. `src: Data model seed data`
- [ ] `C-DM-23` `literal` The console system holds seeded checks on `2026-09-01` behind the seeded incident. `src: Data model seed data`
- [ ] `C-DM-24` `literal` The record `harbour-ledger` is a published `software` record delivered `2026-06-30`. `src: Data model seed data`
- [ ] `C-DM-25` `literal` The record `harbour-ledger` holds `p95_api_ms` `180` measured `2026-07-14`. `src: Data model seed data`
- [ ] `C-DM-26` `literal` The record `kestrel-storefront` is a published `website` record delivered `2026-08-12`. `src: Data model seed data`
- [ ] `C-DM-27` `literal` The record `kestrel-storefront` holds `lcp_ms` `640` beside `cls` `0.01`, measured `2026-08-20`. `src: Data model seed data`
- [ ] `C-DM-28` `literal` The record `lahn-clinic-hosting` is a published `hosting` record delivered `2026-05-02`, client withheld, no measurement. `src: Data model seed data`
- [ ] `C-DM-29` `literal` The record `aurora-payroll-portal` is an unpublished `software` record delivered `2026-09-05`. `src: Data model seed data`
- [ ] `C-DM-30` `capability` Every seeded record carries a diagram. `src: Data model seed data`
- [ ] `C-DM-31` `literal` The request `VS-2026-0001` holds `software`, `handover`, `de`, `standard`, `25k-60k`, figure `1450000`, status `reviewing`. `src: Data model seed data`
- [ ] `C-DM-32` `literal` The request `VS-2026-0002` from `client2@example.com` holds `website`, `managed`, `eu`, `flexible`, `under-10k`, figure `550000`, status `new`, with no attachment. `src: Data model seed data`
- [ ] `C-DM-33` `literal` Both seeded requests use rule table `2026-09`. `src: Data model seed data`
- [ ] `C-DM-34` `constraint` The seed holds no page view, no portrait. `src: Data model seed data`
- [ ] `C-DM-35` `constraint` Seeding is idempotent across restarts. `src: Data model seed data`
- [ ] `C-DM-36` `constraint` A stored figure always equals the rule table result for the stored version. `src: Data model invariants`
- [ ] `C-DM-37` `constraint` A refused write writes no row, no partial row, no object. `src: Data model invariants`
- [ ] `C-DM-38` `contract` The seeded password `deku-demo-pw-2026` is written into `/app/USER_README.md` beside each account. `src: Data model para 2`
- [ ] `C-DM-39` `literal` Each of the first five seeded systems holds twelve checks at a `response_ms` of `48`. `src: Data model seed data`
- [ ] `C-DM-40` `literal` The seeded tickets system holds ten `up` checks of `48` ms over the same twelve slots as the first five, the seventh with the eighth missed. `src: Data model seed data`
- [ ] `C-DM-41` `literal` The record `harbour-ledger` started `2026-02-02` for the shown client `Lahnhafen Logistik`. `src: Data model seed data`
- [ ] `C-DM-42` `literal` The record `kestrel-storefront` started `2026-05-11` for the shown client `Kestrel Outdoor`. `src: Data model seed data`
- [ ] `C-DM-43` `literal` The record `lahn-clinic-hosting` started `2026-03-16`. `src: Data model seed data`
- [ ] `C-DM-44` `literal` The record `aurora-payroll-portal` started `2026-07-01` for the client `Aurora Personal`. `src: Data model seed data`
- [ ] `C-DM-45` `literal` The brief of `VS-2026-0001` is named `billing-brief.pdf` under `requests/VS-2026-0001/`. `src: Data model seed data`
- [ ] `C-DM-46` `capability` Every seeded record carries a one-sentence summary, a short body, a diagram of at least four primitives. `src: Data model seed data`
- [ ] `C-DM-47` `literal` The seeded record titles are `Harbour Ledger`, `Kestrel Storefront`, `Lahn Clinic Hosting`, `Aurora Payroll Portal`. `src: Data model seed data`
- [ ] `C-DM-48` `literal` The seeded stacks are `Python`, `PostgreSQL` for harbour; `Python`, `Alpine.js` for kestrel; `PostgreSQL` for lahn. `src: Data model seed data`
- [ ] `C-DM-49` `literal` The console seed holds checks at `14:15` up, `14:20` down, `14:25` down, `14:30` down, `14:35` up, `14:40` up. `src: Data model seed data`
- [ ] `C-DM-50` `capability` The last seeded check of each healthy system falls at first start. `src: Data model seed data`
- [ ] `C-DM-51` `constraint` Every stored timestamp is UTC. `src: Data model para 1`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product serves one studio with one founder, no second tenant. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The board offers no incident email subscription. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The product collects no field performance data from visitors. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The product carries one language with no locale switch. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` The product offers no third-party scheduling page, no external booking link. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The public routes carry no cookie banner. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` The product fetches no external font at run time. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` The product stays responsive with a few thousand checks, requests, page-view rows. `src: Constraints bullet 10`
- [ ] `C-CN-09` `constraint` No bitmap ships except the portrait the founder uploads. `src: Constraints bullet 8`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`, read from the environment. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under `/api`. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` The route `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Empty `.browser_screenshots/` with `.downloads/` directories exist at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` A production build is served, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, detached from the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `contract` The app never downloads, installs, compiles or starts a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-12` `contract` The app uses no edge functions, no persistent volumes, no fixed container names, no custom networks. `src: Deployment contract bullets 11, 12`
- [ ] `C-DC-13` `contract` A list endpoint returns a top-level JSON array, the status envelope aside. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` An invalid call is rejected as a client error naming the field at fault. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` An unauthorized call is rejected as a client error, never a server error, never a silent success. `src: Deployment contract API shapes`
- [ ] `C-DC-16` `contract` Bearer authentication guards every endpoint outside the public set. `src: Deployment contract API shapes`
- [ ] `C-DC-17` `literal` The route `POST /api/auth/login` takes `email`, `password`, returning the account `role` with an `access_token`. `src: Deployment contract API shapes row 2`
- [ ] `C-DC-18` `literal` The route `GET /api/build-requests/mine` returns only the requests of the calling client, to a `client` only. `src: Deployment contract API shapes row 21`
- [ ] `C-DC-19` `literal` The route `GET /api/build-requests` returns every request, newest first, only to the `founder`. `src: Deployment contract API shapes row 20`
- [ ] `C-DC-20` `literal` The route `POST /api/build-requests/{reference}/status` takes `status`. `src: Deployment contract API shapes row 24`
- [ ] `C-DC-21` `literal` The route `POST /api/builds` takes `slug`, `title`, `capability`, `summary`, `body`, `stack`, `started_on`, `delivered_on`, `client_name`, `client_visible`, `diagram`. `src: Deployment contract API shapes row 13`
- [ ] `C-DC-22` `literal` The route `POST /api/builds/{slug}/measurements` takes `metric`, `value`, `measured_on`, `source`. `src: Deployment contract API shapes row 16`
- [ ] `C-DC-23` `literal` The route `POST /api/studio/portrait` takes the file part `portrait`, returning the stored portrait with its `object_key`. `src: Deployment contract API shapes row 25`
- [ ] `C-DC-24` `literal` The route `POST /api/systems` takes `slug`, `name`, optional `interval_seconds`, `open_after`, `close_after`. `src: Deployment contract API shapes row 8`
- [ ] `C-DC-25` `literal` The route `GET /api/studio/builds` returns every record to the `founder`. `src: Deployment contract API shapes row 12`
- [ ] `C-DC-26` `literal` The route `POST /api/page-views` takes `route`. `src: Deployment contract API shapes row 27`
- [ ] `C-DC-27` `literal` The route `GET /api/page-views` returns views newest first to the `founder`. `src: Deployment contract API shapes row 28`
- [ ] `C-DC-28` `literal` The route `GET /api/builds` returns published records newest delivery first, an optional `capability` narrowing the list to that capability. `src: Deployment contract API shapes row 10`
- [ ] `C-DC-29` `literal` The route `GET /api/builds/{slug}` returns `measurements` beside `diagram`. `src: Deployment contract API shapes row 11`
- [ ] `C-DC-30` `literal` The incident detail returns `entries` carrying `seq`, `kind`, `body`, `recorded_at`. `src: Deployment contract API shapes row 6`
- [ ] `C-DC-31` `literal` The incident list rows carry `ref`, `system`, `opened_at`, `resolved_at`. `src: Deployment contract API shapes row 5`
- [ ] `C-DC-32` `literal` The route `POST /api/build-requests` takes a JSON body or a multipart form with an optional file part `attachment`, carrying `capabilities`, `posture`, `residency`, `timeline`, `budget_band`, `description`, `contact_name`, `contact_email`, `rules_version`, `indicative_minor`, `contact_fax`. `src: Deployment contract API shapes row 19`
- [ ] `C-DC-33` `literal` A created request returns `reference`, `status`, `indicative_minor`, `currency`, `rules_version`. `src: Deployment contract API shapes row 19`
- [ ] `C-DC-34` `capability` A signed-in `client` becomes the owner of a submitted request. `src: Deployment contract API shapes row 19`
- [ ] `C-DC-35` `literal` The route `GET /api/build-requests/{reference}` returns the request with the `attachment`. `src: Deployment contract API shapes row 22`
- [ ] `C-DC-36` `constraint` Bytes never live in memory, on local disk, in a base64 column, behind an open bucket, or under a stored object key pointing at nothing. `src: Deployment contract no mocks`
- [ ] `C-DC-37` `constraint` Board numbers come from recorded checks, never template values. `src: Deployment contract no mocks`
- [ ] `C-DC-38` `constraint` The indicative figure comes from the server rule table, never the page value. `src: Deployment contract no mocks`
- [ ] `C-DC-39` `literal` The route `POST /api/builds/{slug}/publish` is `founder` only. `src: Deployment contract API shapes row 14`
- [ ] `C-DC-40` `literal` The route `POST /api/builds/{slug}/unpublish` is `founder` only. `src: Deployment contract API shapes row 15`
- [ ] `C-DC-41` `literal` The route `GET /api/build-requests/{reference}/attachment` answers only the `founder` or the owning `client`. `src: Deployment contract API shapes row 23`
- [ ] `C-DC-42` `literal` The route `POST /api/auth/signup` takes `email`, `password`. `src: Deployment contract API shapes row 1`
- [ ] `C-DC-43` `literal` A signup returns the created `client` account with an `access_token`. `src: Deployment contract API shapes row 1`
- [ ] `C-DC-44` `literal` The route `POST /api/builds` returns the created record unpublished, to the `founder` only. `src: Deployment contract API shapes row 13`
- [ ] `C-DC-45` `literal` The route `POST /api/uptime/incidents/{ref}/notes` takes `body`, returning the appended entry. `src: Deployment contract API shapes row 7`
- [ ] `C-DC-46` `contract` A successful API call returns the resource or shape the API shapes table names. `src: Deployment contract API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Vela Studio` | The site presents Vela Studio as a one-person software studio in Marburg | C-OV-01 | Overview para 1 |
| `founder@example.com` | The seeded account founder@example.com holds the role founder | C-RL-26 | User roles seeded accounts row 1 |
| `founder` | The seeded account founder@example.com holds the role founder | C-RL-26 | User roles seeded accounts row 1 |
| `client@example.com` | The seeded account client@example.com holds the role client | C-RL-27 | User roles seeded accounts row 2 |
| `client` | The seeded account client@example.com holds the role client | C-RL-27 | User roles seeded accounts row 2 |
| `client2@example.com` | The seeded account client2@example.com holds the role client | C-RL-28 | User roles seeded accounts row 3 |
| `deku-demo-pw-2026` | Every seeded account signs in with the password deku-demo-pw-2026 | C-RL-29 | User roles para 2 |
| `VS-2026-0001` | The seeded request VS-2026-0001 belongs to client@example.com with an attached brief | C-CF-06 | Core features rule 1 |
| `5 MB` | An attached brief is a PDF, PNG or JPEG file of at most 5 MB | C-CF-10 | Core features rule 2 |
| `requests/{reference}/{sha256_of_bytes}.{ext}` | An attached brief is stored at the key requests/{reference}/{sha256_of_bytes}.{ext} | C-CF-12 | Core features rule 2 |
| `/build-request` | The composer at /build-request carries the heading Describe the build | C-CF-18 | Core features rule 3 |
| `Describe the build` | The composer at /build-request carries the heading Describe the build | C-CF-18 | Core features rule 3 |
| `managed` | The hosting posture is managed or handover | C-CF-20 | Core features rule 3 |
| `handover` | The hosting posture is managed or handover | C-CF-20 | Core features rule 3 |
| `eu` | The data residency is eu or de | C-CF-21 | Core features rule 3 |
| `de` | The data residency is eu or de | C-CF-21 | Core features rule 3 |
| `flexible` | The timeline is flexible, standard or accelerated | C-CF-22 | Core features rule 3 |
| `standard` | The timeline is flexible, standard or accelerated | C-CF-22 | Core features rule 3 |
| `accelerated` | The timeline is flexible, standard or accelerated | C-CF-22 | Core features rule 3 |
| `under-10k` | The budget band is under-10k, 10k-25k, 25k-60k or over-60k | C-CF-23 | Core features rule 3 |
| `10k-25k` | The budget band is under-10k, 10k-25k, 25k-60k or over-60k | C-CF-23 | Core features rule 3 |
| `25k-60k` | The budget band is under-10k, 10k-25k, 25k-60k or over-60k | C-CF-23 | Core features rule 3 |
| `over-60k` | The budget band is under-10k, 10k-25k, 25k-60k or over-60k | C-CF-23 | Core features rule 3 |
| `20` | The description runs from 20 to 4000 characters | C-CF-24 | Core features rule 3 |
| `4000` | The description runs from 20 to 4000 characters | C-CF-24 | Core features rule 3 |
| `cap` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `posture` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `residency` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `timeline` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `budget` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `desc` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `v` | The composer address carries cap, posture, residency, timeline, budget, desc, v in that or | C-CF-28 | Core features rule 3 |
| `software` | The cap value lists capabilities comma-separated in the order software, website, hosting | C-CF-29 | Core features rule 3 |
| `website` | The cap value lists capabilities comma-separated in the order software, website, hosting | C-CF-29 | Core features rule 3 |
| `hosting` | The cap value lists capabilities comma-separated in the order software, website, hosting | C-CF-29 | Core features rule 3 |
| `eur` | The figure is stored in integer euro cents with the currency eur | C-CF-33 | Core features rule 4 |
| `2026-09` | The current rule table 2026-09 sets software to 1200000, website to 600000, hosting to 300 | C-CF-34 | Core features rule 4 |
| `1200000` | The current rule table 2026-09 sets software to 1200000, website to 600000, hosting to 300 | C-CF-34 | Core features rule 4 |
| `600000` | The current rule table 2026-09 sets software to 1200000, website to 600000, hosting to 300 | C-CF-34 | Core features rule 4 |
| `300000` | The current rule table 2026-09 sets software to 1200000, website to 600000, hosting to 300 | C-CF-34 | Core features rule 4 |
| `150000` | Posture handover adds 150000 | C-CF-36 | Core features rule 4 |
| `90` | Timeline flexible, standard, accelerated multiplies the subtotal by 90, 100, 125 percent | C-CF-38 | Core features rule 4 |
| `100` | Timeline flexible, standard, accelerated multiplies the subtotal by 90, 100, 125 percent | C-CF-38 | Core features rule 4 |
| `125` | Timeline flexible, standard, accelerated multiplies the subtotal by 90, 100, 125 percent | C-CF-38 | Core features rule 4 |
| `50000` | The result rounds to the nearest 50000, an exact half rounding up | C-CF-39 | Core features rule 4 |
| `EUR` | The figure displays as whole euros after EUR, for example EUR 12,000 | C-CF-40 | Core features rule 4 |
| `EUR 12,000` | The figure displays as whole euros after EUR, for example EUR 12,000 | C-CF-40 | Core features rule 4 |
| `550000` | Website, managed, eu, flexible gives 550000 | C-CF-42 | Core features rule 4 table row 2 |
| `350000` | Hosting, managed, de, standard gives 350000 | C-CF-43 | Core features rule 4 table row 3 |
| `850000` | Website, managed, de, accelerated gives 850000 | C-CF-44 | Core features rule 4 table row 4 |
| `2650000` | Software plus website, handover, de, accelerated gives 2650000 | C-CF-45 | Core features rule 4 table row 5 |
| `2026-03` | The retired table 2026-03 sets software to 1000000, website to 500000, hosting to 250000,  | C-CF-47 | Core features rule 5 |
| `1000000` | The retired table 2026-03 sets software to 1000000, website to 500000, hosting to 250000,  | C-CF-47 | Core features rule 5 |
| `500000` | The retired table 2026-03 sets software to 1000000, website to 500000, hosting to 250000,  | C-CF-47 | Core features rule 5 |
| `250000` | The retired table 2026-03 sets software to 1000000, website to 500000, hosting to 250000,  | C-CF-47 | Core features rule 5 |
| `GET /api/pricing-rules` | GET /api/pricing-rules returns the current table with the field version | C-CF-51 | Core features rule 5 |
| `version` | GET /api/pricing-rules returns the current table with the field version | C-CF-51 | Core features rule 5 |
| `GET /api/pricing-rules/{version}` | GET /api/pricing-rules/{version} returns a current or retired table | C-CF-52 | Core features rule 5 |
| `VS-<year>-<NNNN>` | Each accepted request receives a reference shaped VS-<year>-<NNNN> | C-CF-57 | Core features rule 7 |
| `VS-2026-0003` | The next request accepted in 2026 is VS-2026-0003 | C-CF-59 | Core features rule 7 |
| `Request received` | The no-script response is a rendered summary page headed Request received | C-CF-63 | Core features rule 8 |
| `contact_fax` | The form carries a decoy field contact_fax that a person never sees | C-CF-68 | Core features rule 9 |
| `new` | A request starts with the status new | C-CF-73 | Core features rule 10 |
| `reviewing` | The founder moves a request along new, reviewing, quoted, then accepted or declined | C-CF-74 | Core features rule 10 |
| `quoted` | The founder moves a request along new, reviewing, quoted, then accepted or declined | C-CF-74 | Core features rule 10 |
| `accepted` | The founder moves a request along new, reviewing, quoted, then accepted or declined | C-CF-74 | Core features rule 10 |
| `declined` | The founder moves a request along new, reviewing, quoted, then accepted or declined | C-CF-74 | Core features rule 10 |
| `data` | The feed envelope holds data containing nextCheckAt plus projects | C-CF-81 | Core features rule 11 |
| `nextCheckAt` | The feed envelope holds data containing nextCheckAt plus projects | C-CF-81 | Core features rule 11 |
| `projects` | The feed envelope holds data containing nextCheckAt plus projects | C-CF-81 | Core features rule 11 |
| `id` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `slug` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `name` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `position` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `currentStatus` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `uptimePercent` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `latestResponseMs` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `latestCheckedAt` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `lastStatusChangeAt` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `bars` | Each project carries id, slug, name, position, currentStatus, uptimePercent, latestRespons | C-CF-82 | Core features rule 11 |
| `status` | Each bar carries status with checkedAt | C-CF-83 | Core features rule 11 |
| `checkedAt` | Each bar carries status with checkedAt | C-CF-83 | Core features rule 11 |
| `error` | A feed failure answers with error holding message | C-CF-84 | Core features rule 11 |
| `message` | A feed failure answers with error holding message | C-CF-84 | Core features rule 11 |
| `up` | The currentStatus value is one of up, slow, degraded, down, unknown | C-CF-86 | Core features rule 11 |
| `slow` | The currentStatus value is one of up, slow, degraded, down, unknown | C-CF-86 | Core features rule 11 |
| `degraded` | The currentStatus value is one of up, slow, degraded, down, unknown | C-CF-86 | Core features rule 11 |
| `down` | The currentStatus value is one of up, slow, degraded, down, unknown | C-CF-86 | Core features rule 11 |
| `unknown` | The currentStatus value is one of up, slow, degraded, down, unknown | C-CF-86 | Core features rule 11 |
| `300` | A system check interval defaults to 300 seconds | C-CF-100 | Core features rule 12 |
| `75.00` | Checks up, up, down, then up after a gap give two unknown slots with 75.00 | C-CF-107 | Core features rule 13 table row 1 |
| `66.67` | Checks up, up, down give 66.67 | C-CF-109 | Core features rule 13 table row 3 |
| `open_after` | Each system stores open_after defaulting to 3 with close_after defaulting to 2 | C-CF-110 | Core features rule 14 |
| `3` | Each system stores open_after defaulting to 3 with close_after defaulting to 2 | C-CF-110 | Core features rule 14 |
| `close_after` | Each system stores open_after defaulting to 3 with close_after defaulting to 2 | C-CF-110 | Core features rule 14 |
| `2` | Each system stores open_after defaulting to 3 with close_after defaulting to 2 | C-CF-110 | Core features rule 14 |
| `vela-studio-console-20260901-1420` | An incident reference joins the system slug with the opening date, hour, minute, as in vel | C-CF-116 | Core features rule 14 |
| `seq` | Each incident entry carries seq, kind, a body, a time | C-CF-118 | Core features rule 15 |
| `kind` | Each incident entry carries seq, kind, a body, a time | C-CF-118 | Core features rule 15 |
| `opened` | An entry kind is opened, note or resolved | C-CF-119 | Core features rule 15 |
| `note` | An entry kind is opened, note or resolved | C-CF-119 | Core features rule 15 |
| `resolved` | An entry kind is opened, note or resolved | C-CF-119 | Core features rule 15 |
| `2026-09-01T14:20:00Z` | The seeded incident opened at 2026-09-01T14:20:00Z | C-CF-127 | Core features rule 15 |
| `2026-09-01T14:40:00Z` | The seeded incident resolved at 2026-09-01T14:40:00Z | C-CF-128 | Core features rule 15 |
| `Disk pressure on the Frankfurt node` | The seeded note begins Disk pressure on the Frankfurt node | C-CF-130 | Core features rule 15 |
| `Systems` | Four tiles read Systems, Operational, Average uptime, Next check | C-CF-132 | Core features rule 16 |
| `Operational` | Four tiles read Systems, Operational, Average uptime, Next check | C-CF-132 | Core features rule 16 |
| `Average uptime` | Four tiles read Systems, Operational, Average uptime, Next check | C-CF-132 | Core features rule 16 |
| `Next check` | Four tiles read Systems, Operational, Average uptime, Next check | C-CF-132 | Core features rule 16 |
| `Uptime` | Each card shows Uptime, Response time, Last checked, Last status change | C-CF-139 | Core features rule 16 |
| `Response time` | Each card shows Uptime, Response time, Last checked, Last status change | C-CF-139 | Core features rule 16 |
| `Last checked` | Each card shows Uptime, Response time, Last checked, Last status change | C-CF-139 | Core features rule 16 |
| `Last status change` | Each card shows Uptime, Response time, Last checked, Last status change | C-CF-139 | Core features rule 16 |
| `Awaiting checks` | A null check time shows Awaiting checks | C-CF-142 | Core features rule 16 |
| `Incident history` | An Incident history section lists incidents newest first below the cards | C-CF-149 | Core features rule 16 |
| `Ongoing` | An unresolved incident shows Ongoing in the incident history | C-CF-150 | Core features rule 16 |
| `/uptime/incidents/<ref>` | Each incident opens a page at /uptime/incidents/<ref> listing entries in seq order | C-CF-151 | Core features rule 16 |
| `No incidents recorded.` | An empty incident history reads No incidents recorded | C-CF-152 | Core features rule 16 |
| `Live status needs JavaScript to load.` | With scripts off the board shows Live status needs JavaScript to load | C-CF-153 | Core features rule 16 |
| `/builds?capability=software` | A capability filter writes an address such as /builds?capability=software | C-CF-157 | Core features rule 17 |
| `Client withheld` | A withheld client shows Client withheld | C-CF-161 | Core features rule 17 |
| `Not yet measured` | A record with no measurement shows Not yet measured | C-CF-163 | Core features rule 17 |
| `rect` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `path` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `circle` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `role` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `accent` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `structure` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `faint` | A diagram primitive carries kind of rect, path or circle with role of accent, structure or | C-CF-168 | Core features rule 18 |
| `Diagram:` | The record drawing is labelled Diagram: followed by the record title | C-CF-170 | Core features rule 18 |
| `Scope a build` | The card link Scope a build opens the latest delivered published software record | C-CF-172 | Core features rule 19 |
| `See a build` | The card link See a build opens the latest delivered published website record | C-CF-173 | Core features rule 19 |
| `See the stack` | The card link See the stack opens the latest delivered published hosting record | C-CF-174 | Core features rule 19 |
| `/builds?capability=` | A capability with no published record links to /builds?capability= for that capability | C-CF-176 | Core features rule 19 |
| `/builds/harbour-ledger` | The seeded capability links open /builds/harbour-ledger, /builds/kestrel-storefront, /buil | C-CF-177 | Core features rule 19 |
| `/builds/kestrel-storefront` | The seeded capability links open /builds/harbour-ledger, /builds/kestrel-storefront, /buil | C-CF-177 | Core features rule 19 |
| `/builds/lahn-clinic-hosting` | The seeded capability links open /builds/harbour-ledger, /builds/kestrel-storefront, /buil | C-CF-177 | Core features rule 19 |
| `/builds/aurora-payroll-portal` | The draft /builds/aurora-payroll-portal is never a capability link target | C-CF-178 | Core features rule 19 |
| `Status & uptime` | The card link Status & uptime opens /uptime | C-CF-179 | Core features rule 19 |
| `/uptime` | The card link Status & uptime opens /uptime | C-CF-179 | Core features rule 19 |
| `Talk to an engineer` | The hero button Talk to an engineer opens /build-request | C-CF-180 | Core features rule 19 |
| `talk to an engineer_` | The contact prompt talk to an engineer_ opens /build-request | C-CF-181 | Core features rule 19 |
| `at=<section>-<percent>` | The address records a reading position as at=<section>-<percent> | C-CF-196 | Core features rule 21 |
| `philosophy` | The home sections are philosophy, software-platforms, websites, managed-hosting, infrastru | C-CF-197 | Core features rule 21 |
| `software-platforms` | The home sections are philosophy, software-platforms, websites, managed-hosting, infrastru | C-CF-197 | Core features rule 21 |
| `websites` | The home sections are philosophy, software-platforms, websites, managed-hosting, infrastru | C-CF-197 | Core features rule 21 |
| `managed-hosting` | The home sections are philosophy, software-platforms, websites, managed-hosting, infrastru | C-CF-197 | Core features rule 21 |
| `infrastructure` | The home sections are philosophy, software-platforms, websites, managed-hosting, infrastru | C-CF-197 | Core features rule 21 |
| `craft` | The about sections are craft, principle | C-CF-198 | Core features rule 21 |
| `principle` | The about sections are craft, principle | C-CF-198 | Core features rule 21 |
| `0` | The percent is a whole number from 0 to 100, as in /?at=managed-hosting-80 | C-CF-199 | Core features rule 21 |
| `/?at=managed-hosting-80` | The percent is a whole number from 0 to 100, as in /?at=managed-hosting-80 | C-CF-199 | Core features rule 21 |
| `about me_` | The personal contact prompt on the founder page reads about me_ | C-CF-214 | Core features rule 23 |
| `minio` | An uploaded portrait is stored in minio at portrait/{sha256_of_bytes}.{ext} | C-CF-215 | Core features rule 23 |
| `portrait/{sha256_of_bytes}.{ext}` | An uploaded portrait is stored in minio at portrait/{sha256_of_bytes}.{ext} | C-CF-215 | Core features rule 23 |
| `Anton Ferber, founder of Vela Studio` | The portrait carries the alternative text Anton Ferber, founder of Vela Studio | C-CF-217 | Core features rule 23 |
| `Portrait placeholder` | With no portrait the drawn stand-in carries the accessible name Portrait placeholder | C-CF-218 | Core features rule 23 |
| `Back to Vela Studio` | The legal back link reads Back to Vela Studio | C-CF-222 | Core features rule 24 |
| `Home` | The footer list is Home, About, Legal Notice, Terms, Status/Uptime | C-CF-227 | Core features rule 25 |
| `About` | The footer list is Home, About, Legal Notice, Terms, Status/Uptime | C-CF-227 | Core features rule 25 |
| `Legal Notice` | The footer list is Home, About, Legal Notice, Terms, Status/Uptime | C-CF-227 | Core features rule 25 |
| `Terms` | The footer list is Home, About, Legal Notice, Terms, Status/Uptime | C-CF-227 | Core features rule 25 |
| `Status/Uptime` | The footer list is Home, About, Legal Notice, Terms, Status/Uptime | C-CF-227 | Core features rule 25 |
| `Back` | The founder page plus the status board carry a fixed back pill reading Back | C-CF-229 | Core features rule 25 |
| `/studio` | The founder lands on /studio after sign-in at /login | C-CF-239 | Core features rule 29 |
| `/login` | The founder lands on /studio after sign-in at /login | C-CF-239 | Core features rule 29 |
| `/account` | A client lands on /account after sign-in at /login | C-CF-240 | Core features rule 29 |
| `Requests` | The studio top bar reads Requests, Builds, Systems, Portrait, Page views | C-CF-241 | Core features rule 29 |
| `Builds` | The studio top bar reads Requests, Builds, Systems, Portrait, Page views | C-CF-241 | Core features rule 29 |
| `Portrait` | The studio top bar reads Requests, Builds, Systems, Portrait, Page views | C-CF-241 | Core features rule 29 |
| `Page views` | The studio top bar reads Requests, Builds, Systems, Portrait, Page views | C-CF-241 | Core features rule 29 |
| `Status updated` | A studio status change confirms with a brief toast reading Status updated | C-CF-245 | Core features rule 29 |
| `4.5:1` | Interactive text reaches a contrast ratio of at least 4.5:1 against the page ground | C-CF-249 | Core features rule 30 |
| `5242880` | The attachment size limit of 5 MB is 5242880 bytes | C-CF-251 | Core features rule 2 |
| `pdf` | The attachment key extension is pdf, png or jpg | C-CF-253 | Core features rule 2 |
| `png` | The attachment key extension is pdf, png or jpg | C-CF-253 | Core features rule 2 |
| `jpg` | The attachment key extension is pdf, png or jpg | C-CF-253 | Core features rule 2 |
| `60` | A system interval is a whole number of at least 60 seconds | C-CF-262 | Core features rule 12 |
| `11:00` | With open_after 2, close_after 3, checks down, down, up, down, up, down, up, up, up, up fr | C-CF-265 | Core features rule 14 |
| `11:40` | With open_after 2, close_after 3, checks down, down, up, down, up, down, up, up, up, up fr | C-CF-265 | Core features rule 14 |
| `system` | Each listed incident names the system by slug in system | C-CF-267 | Core features rule 15 |
| `s` | The Next check tile shows whole seconds rounded up with an s, as in 27s | C-CF-270 | Core features rule 16 |
| `27s` | The Next check tile shows whole seconds rounded up with an s, as in 27s | C-CF-270 | Core features rule 16 |
| `Due now` | The Next check tile reads Due now once the moment has passed | C-CF-271 | Core features rule 16 |
| `/studio/portrait` | The founder uploads the portrait at /studio/portrait | C-CF-276 | Core features rule 23 |
| `x` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `y` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `width` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `height` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `rx` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `d` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `cx` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `cy` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `r` | A rect carries x, y, width, height, optional rx; a path carries d; a circle carries cx, cy | C-CF-297 | Core features rule 18 |
| `EUR 10,000` | Under 2026-03, software, managed, eu, standard gives 1000000, shown EUR 10,000 | C-CF-301 | Core features rule 5 |
| `/builds/<slug>` | The route /builds/<slug> shows one published build record without a session | C-UF-01 | User flow route table |
| `/signup` | The route /signup creates a client | C-UF-02 | User flow route table |
| `Anton Ferber Portfolio` | The board lists Vela Studio first with Anton Ferber Portfolio last | C-UF-09 | User flow watcher journey |
| `EUR 14,500` | Software, handover, de, standard shows the figure EUR 14,500 | C-UF-11 | User flow buyer journey |
| `No systems available` | The board empty state reads No systems available | C-UF-17 | User flow states |
| `No build records yet.` | The library empty state reads No build records yet | C-UF-18 | User flow states |
| `No requests yet.` | An empty request list reads No requests yet | C-UF-19 | User flow states |
| `/impressum` | The route /impressum serves the legal notice without a session | C-UF-29 | User flow route table |
| `/agb` | The route /agb serves the terms without a session | C-UF-30 | User flow route table |
| `Geist` | Sentences, headings, the underlined hero link, the legal back link use Geist | C-UX-10 | UI/UX notes type and shape |
| `Geist Mono` | Eyebrows, the hero meta line, the hero foot, the back pill, the card links, the notice lin | C-UX-11 | UI/UX notes type and shape |
| `16px` | Body copy is 16px; every eyebrow is 11px | C-FE-08 | Front-end specification type sizes |
| `11px` | Body copy is 16px; every eyebrow is 11px | C-FE-08 | Front-end specification type sizes |
| `100.8px` | The hero title is 100.8px wide, 69.3px at tablet width, 32.76px on a phone | C-FE-09 | Front-end specification type sizes |
| `69.3px` | The hero title is 100.8px wide, 69.3px at tablet width, 32.76px on a phone | C-FE-09 | Front-end specification type sizes |
| `32.76px` | The hero title is 100.8px wide, 69.3px at tablet width, 32.76px on a phone | C-FE-09 | Front-end specification type sizes |
| `66.24px` | The pinned statement is 66.24px, 45.54px, 32px at the three widths | C-FE-10 | Front-end specification type sizes |
| `45.54px` | The pinned statement is 66.24px, 45.54px, 32px at the three widths | C-FE-10 | Front-end specification type sizes |
| `32px` | The pinned statement is 66.24px, 45.54px, 32px at the three widths | C-FE-10 | Front-end specification type sizes |
| `48px` | A card heading is 48px on a wide window; a card body is 23.04px wide, 16.8px below | C-FE-11 | Front-end specification type sizes |
| `23.04px` | A card heading is 48px on a wide window; a card body is 23.04px wide, 16.8px below | C-FE-11 | Front-end specification type sizes |
| `16.8px` | A card heading is 48px on a wide window; a card body is 23.04px wide, 16.8px below | C-FE-11 | Front-end specification type sizes |
| `70.4px` | The mono contact line is 70.4px, 51.48px, 22.4px | C-FE-12 | Front-end specification type sizes |
| `51.48px` | The mono contact line is 70.4px, 51.48px, 22.4px | C-FE-12 | Front-end specification type sizes |
| `22.4px` | The mono contact line is 70.4px, 51.48px, 22.4px | C-FE-12 | Front-end specification type sizes |
| `19px` | A status system name is 19px; a status tile value is 26px | C-FE-13 | Front-end specification type sizes |
| `26px` | A status system name is 19px; a status tile value is 26px | C-FE-13 | Front-end specification type sizes |
| `15px` | Legal body text is 15px under a 20px clause heading | C-FE-14 | Front-end specification type sizes |
| `20px` | Legal body text is 15px under a 20px clause heading | C-FE-14 | Front-end specification type sizes |
| `02` | Card 02 drawing carries a description beginning Diagram: interface, API | C-FE-17 | Front-end specification home diagrams |
| `Diagram: interface, API` | Card 02 drawing carries a description beginning Diagram: interface, API | C-FE-17 | Front-end specification home diagrams |
| `03` | Card 03 drawing carries the description Diagram: a browser window with Core Web Vitals sco | C-FE-18 | Front-end specification home diagrams |
| `Diagram: a browser window with Core Web Vitals scores` | Card 03 drawing carries the description Diagram: a browser window with Core Web Vitals sco | C-FE-18 | Front-end specification home diagrams |
| `04` | Card 04 drawing carries the description Diagram: a server rack with encrypted uplinks | C-FE-19 | Front-end specification home diagrams |
| `Diagram: a server rack with encrypted uplinks` | Card 04 drawing carries the description Diagram: a server rack with encrypted uplinks | C-FE-19 | Front-end specification home diagrams |
| `05` | Card 05 drawing carries a description beginning Diagram: four interconnected nodes across  | C-FE-20 | Front-end specification home diagrams |
| `Diagram: four interconnected nodes across Falkenstein` | Card 05 drawing carries a description beginning Diagram: four interconnected nodes across  | C-FE-20 | Front-end specification home diagrams |
| `interface` | Card 02 drawing words are interface, api, workers, postgres | C-FE-21 | Front-end specification home diagrams |
| `api` | Card 02 drawing words are interface, api, workers, postgres | C-FE-21 | Front-end specification home diagrams |
| `workers` | Card 02 drawing words are interface, api, workers, postgres | C-FE-21 | Front-end specification home diagrams |
| `postgres` | Card 02 drawing words are interface, api, workers, postgres | C-FE-21 | Front-end specification home diagrams |
| `LCP 0.6s` | Card 03 drawing words are LCP 0.6s, CLS 0.00, 100 / 100 | C-FE-22 | Front-end specification home diagrams |
| `CLS 0.00` | Card 03 drawing words are LCP 0.6s, CLS 0.00, 100 / 100 | C-FE-22 | Front-end specification home diagrams |
| `100 / 100` | Card 03 drawing words are LCP 0.6s, CLS 0.00, 100 / 100 | C-FE-22 | Front-end specification home diagrams |
| `uplink` | Card 04 drawing words are uplink, encrypted | C-FE-23 | Front-end specification home diagrams |
| `encrypted` | Card 04 drawing words are uplink, encrypted | C-FE-23 | Front-end specification home diagrams |
| `FSN` | Card 05 drawing words are FSN, FRA, EYG-1, EYG-2 | C-FE-24 | Front-end specification home diagrams |
| `FRA` | Card 05 drawing words are FSN, FRA, EYG-1, EYG-2 | C-FE-24 | Front-end specification home diagrams |
| `EYG-1` | Card 05 drawing words are FSN, FRA, EYG-1, EYG-2 | C-FE-24 | Front-end specification home diagrams |
| `EYG-2` | Card 05 drawing words are FSN, FRA, EYG-1, EYG-2 | C-FE-24 | Front-end specification home diagrams |
| `Capability` | Cards 02 to 04 carry the eyebrow Capability; card 05 carries Infrastructure | C-FE-30 | Front-end specification pinned card |
| `Infrastructure` | Cards 02 to 04 carry the eyebrow Capability; card 05 carries Infrastructure | C-FE-30 | Front-end specification pinned card |
| `Marburg, DE` | The hero meta line reads a small amber dot, Vela Studio, a slash, Marburg, DE | C-FE-34 | Front-end specification home route |
| `Software built in Germany.` | The hero title reads Software built in Germany. over Hosted in Europe | C-FE-35 | Front-end specification home route |
| `Hosted in Europe.` | The hero title reads Software built in Germany. over Hosted in Europe | C-FE-35 | Front-end specification home route |
| `We write production software` | The hero lede begins We write production software | C-FE-36 | Front-end specification home route |
| `Frankfurt` | The hero foot names Frankfurt, Falkenstein, Eygelshoven beside Scroll | C-FE-37 | Front-end specification home route |
| `Falkenstein` | The hero foot names Frankfurt, Falkenstein, Eygelshoven beside Scroll | C-FE-37 | Front-end specification home route |
| `Eygelshoven` | The hero foot names Frankfurt, Falkenstein, Eygelshoven beside Scroll | C-FE-37 | Front-end specification home route |
| `Scroll` | The hero foot names Frankfurt, Falkenstein, Eygelshoven beside Scroll | C-FE-37 | Front-end specification home route |
| `01 - Philosophy` | The philosophy eyebrow reads 01 - Philosophy | C-FE-38 | Front-end specification home route |
| `We build privacy-first software` | The philosophy statement begins We build privacy-first software | C-FE-39 | Front-end specification home route |
| `reliable` | The philosophy amber words are reliable, transparent, entirely yours, never a black box | C-FE-40 | Front-end specification home route |
| `transparent` | The philosophy amber words are reliable, transparent, entirely yours, never a black box | C-FE-40 | Front-end specification home route |
| `entirely yours` | The philosophy amber words are reliable, transparent, entirely yours, never a black box | C-FE-40 | Front-end specification home route |
| `never a black box` | The philosophy amber words are reliable, transparent, entirely yours, never a black box | C-FE-40 | Front-end specification home route |
| `What we build` | The heading row reads What we build beside the eyebrow Capabilities | C-FE-41 | Front-end specification home route |
| `Capabilities` | The heading row reads What we build beside the eyebrow Capabilities | C-FE-41 | Front-end specification home route |
| `#leistungen` | The in-page anchors are #leistungen for the heading row, #kontakt for contact | C-FE-42 | Front-end specification home route |
| `#kontakt` | The in-page anchors are #leistungen for the heading row, #kontakt for contact | C-FE-42 | Front-end specification home route |
| `Software & Platforms` | The card headings read Software & Platforms, High-performing websites, Managed hosting, pr | C-FE-43 | Front-end specification home route table |
| `High-performing websites` | The card headings read Software & Platforms, High-performing websites, Managed hosting, pr | C-FE-43 | Front-end specification home route table |
| `Managed hosting, privacy-first` | The card headings read Software & Platforms, High-performing websites, Managed hosting, pr | C-FE-43 | Front-end specification home route table |
| `Four nodes. One jurisdiction.` | The card headings read Software & Platforms, High-performing websites, Managed hosting, pr | C-FE-43 | Front-end specification home route table |
| `SaaS products` | The card bodies begin SaaS products, Marketing sites, Your workload runs, Falkenstein, Fra | C-FE-44 | Front-end specification home route table |
| `Marketing sites` | The card bodies begin SaaS products, Marketing sites, Your workload runs, Falkenstein, Fra | C-FE-44 | Front-end specification home route table |
| `Your workload runs` | The card bodies begin SaaS products, Marketing sites, Your workload runs, Falkenstein, Fra | C-FE-44 | Front-end specification home route table |
| `Falkenstein, Frankfurt` | The card bodies begin SaaS products, Marketing sites, Your workload runs, Falkenstein, Fra | C-FE-44 | Front-end specification home route table |
| `06 - Contact` | The contact eyebrow reads 06 - Contact | C-FE-45 | Front-end specification home route |
| `Reply within one working day` | The contact note begins Reply within one working day | C-FE-46 | Front-end specification home route |
| `hello@vela.example.com` | The contact mail link is hello@vela.example.com | C-FE-47 | Front-end specification home route |
| `Curious who's actually behind the racks?` | The teaser reads Curious who's actually behind the racks? over (a real human) | C-FE-48 | Front-end specification home route |
| `(a real human)` | The teaser reads Curious who's actually behind the racks? over (a real human) | C-FE-48 | Front-end specification home route |
| `Anton Ferber` | The founder page meta line reads About, a slash, Anton Ferber | C-FE-49 | Front-end specification founder page |
| `Why I build` | The founder page title reads Why I build over Vela Studio | C-FE-50 | Front-end specification founder page |
| `Vela Studio.` | The founder page title reads Why I build over Vela Studio | C-FE-50 | Front-end specification founder page |
| `I'm Anton.` | The founder page lede begins I'm Anton | C-FE-51 | Front-end specification founder page |
| `01 - The craft` | Statement 01 - The craft begins I build software the way | C-FE-52 | Front-end specification founder page |
| `I build software the way` | Statement 01 - The craft begins I build software the way | C-FE-52 | Front-end specification founder page |
| `02 - The principle` | Statement 02 - The principle begins Privacy isn't a feature | C-FE-53 | Front-end specification founder page |
| `Privacy isn't a feature` | Statement 02 - The principle begins Privacy isn't a feature | C-FE-53 | Front-end specification founder page |
| `03 - Elsewhere` | The founder contact reads 03 - Elsewhere with the link anton-ferber.example.com | C-FE-54 | Front-end specification founder page |
| `anton-ferber.example.com` | The founder contact reads 03 - Elsewhere with the link anton-ferber.example.com | C-FE-54 | Front-end specification founder page |
| `System status` | The status eyebrow reads System status in amber | C-FE-56 | Front-end specification status board |
| `Live reliability, shown in public.` | The status heading reads Live reliability, shown in public | C-FE-57 | Front-end specification status board |
| `Slow` | The status words read Operational, Slow, Degraded, Down, Unknown | C-FE-58 | Front-end specification status board |
| `Degraded` | The status words read Operational, Slow, Degraded, Down, Unknown | C-FE-58 | Front-end specification status board |
| `Down` | The status words read Operational, Slow, Degraded, Down, Unknown | C-FE-58 | Front-end specification status board |
| `Unknown` | The status words read Operational, Slow, Degraded, Down, Unknown | C-FE-58 | Front-end specification status board |
| `title` | Each bar carries the title attribute <status word> at <time>, as in Operational at 1 Sept  | C-FE-59 | Front-end specification status board |
| `<status word> at <time>` | Each bar carries the title attribute <status word> at <time>, as in Operational at 1 Sept  | C-FE-59 | Front-end specification status board |
| `Operational at 1 Sept 2026, 15:38` | Each bar carries the title attribute <status word> at <time>, as in Operational at 1 Sept  | C-FE-59 | Front-end specification status board |
| `aria-label` | Each bar strip carries the aria-label Recent uptime history for <system name> | C-FE-60 | Front-end specification status board |
| `Recent uptime history for <system name>` | Each bar strip carries the aria-label Recent uptime history for <system name> | C-FE-60 | Front-end specification status board |
| `Status temporarily unavailable` | The failure block reads Status temporarily unavailable with the feed's own message, fallin | C-FE-61 | Front-end specification status board |
| `The uptime feed is unavailable.` | The failure block reads Status temporarily unavailable with the feed's own message, fallin | C-FE-61 | Front-end specification status board |
| `No monitored systems are currently visible.` | The empty block reads No monitored systems are currently visible | C-FE-62 | Front-end specification status board |
| `Vela Studio Finance` | The seven systems in order are Vela Studio, Vela Studio Finance, Vela Studio Analytics, Ve | C-FE-63 | Front-end specification status board table |
| `Vela Studio Analytics` | The seven systems in order are Vela Studio, Vela Studio Finance, Vela Studio Analytics, Ve | C-FE-63 | Front-end specification status board table |
| `Vela Studio Console` | The seven systems in order are Vela Studio, Vela Studio Finance, Vela Studio Analytics, Ve | C-FE-63 | Front-end specification status board table |
| `Vela Studio DB Controller` | The seven systems in order are Vela Studio, Vela Studio Finance, Vela Studio Analytics, Ve | C-FE-63 | Front-end specification status board table |
| `Vela Studio Tickets` | The seven systems in order are Vela Studio, Vela Studio Finance, Vela Studio Analytics, Ve | C-FE-63 | Front-end specification status board table |
| `Open customer portal` | The notice link reads Open customer portal with the host portal.vela.example.com | C-FE-64 | Front-end specification status board |
| `portal.vela.example.com` | The notice link reads Open customer portal with the host portal.vela.example.com | C-FE-64 | Front-end specification status board |
| `LEGAL NOTICE` | The legal notice carries the eyebrow LEGAL NOTICE over a heading beginning Information pur | C-FE-66 | Front-end specification legal documents |
| `Information pursuant to` | The legal notice carries the eyebrow LEGAL NOTICE over a heading beginning Information pur | C-FE-66 | Front-end specification legal documents |
| `Ketzerbach 21` | The provider block reads Ketzerbach 21 over 35037 Marburg | C-FE-67 | Front-end specification legal documents |
| `35037 Marburg` | The provider block reads Ketzerbach 21 over 35037 Marburg | C-FE-67 | Front-end specification legal documents |
| `+49 6421 555 0142` | The legal notice lists the phone number +49 6421 555 0142 | C-FE-68 | Front-end specification legal documents |
| `VAT identification number: DE123456789` | The VAT line reads VAT identification number: DE123456789 | C-FE-69 | Front-end specification legal documents |
| `Provider` | The legal notice holds nine blocks from Provider to Copyright | C-FE-70 | Front-end specification legal documents |
| `Copyright` | The legal notice holds nine blocks from Provider to Copyright | C-FE-70 | Front-end specification legal documents |
| `TERMS` | The terms carry the eyebrow TERMS over a heading beginning General Terms | C-FE-72 | Front-end specification legal documents |
| `General Terms` | The terms carry the eyebrow TERMS over a heading beginning General Terms | C-FE-72 | Front-end specification legal documents |
| `1. Scope` | The terms hold eight numbered clauses from 1. Scope to 8. Final provisions | C-FE-73 | Front-end specification legal documents |
| `8. Final provisions` | The terms hold eight numbered clauses from 1. Scope to 8. Final provisions | C-FE-73 | Front-end specification legal documents |
| `All` | The library filters read All, Software & Platforms, High-performing websites, Managed host | C-FE-76 | Front-end specification build library |
| `Anywhere in the EU` | The residency choices read Anywhere in the EU, Germany only | C-FE-77 | Front-end specification build library |
| `Germany only` | The residency choices read Anywhere in the EU, Germany only | C-FE-77 | Front-end specification build library |
| `Flexible` | The timeline choices read Flexible, Standard, Accelerated | C-FE-78 | Front-end specification build library |
| `Standard` | The timeline choices read Flexible, Standard, Accelerated | C-FE-78 | Front-end specification build library |
| `Accelerated` | The timeline choices read Flexible, Standard, Accelerated | C-FE-78 | Front-end specification build library |
| `Under EUR 10,000` | The budget choices read Under EUR 10,000, EUR 10,000 to 25,000, EUR 25,000 to 60,000, Over | C-FE-79 | Front-end specification build library |
| `EUR 10,000 to 25,000` | The budget choices read Under EUR 10,000, EUR 10,000 to 25,000, EUR 25,000 to 60,000, Over | C-FE-79 | Front-end specification build library |
| `EUR 25,000 to 60,000` | The budget choices read Under EUR 10,000, EUR 10,000 to 25,000, EUR 25,000 to 60,000, Over | C-FE-79 | Front-end specification build library |
| `Over EUR 60,000` | The budget choices read Under EUR 10,000, EUR 10,000 to 25,000, EUR 25,000 to 60,000, Over | C-FE-79 | Front-end specification build library |
| `on our racks` | The managed posture label ends on our racks; the handover posture label ends to run yourse | C-FE-80 | Front-end specification build library |
| `to run yourself` | The managed posture label ends on our racks; the handover posture label ends to run yourse | C-FE-80 | Front-end specification build library |
| `Indicative figure` | The figure is labelled Indicative figure; the send button reads Send build request | C-FE-81 | Front-end specification build library |
| `Send build request` | The figure is labelled Indicative figure; the send button reads Send build request | C-FE-81 | Front-end specification build library |
| `capabilities` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `budget_band` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `description` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `contact_name` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `contact_email` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `rules_version` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `indicative_minor` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `attachment` | The form controls are named capabilities, posture, residency, timeline, budget_band, descr | C-FE-82 | Front-end specification build library |
| `Your build requests` | The account page heading reads Your build requests | C-FE-83 | Front-end specification build library |
| `Software Made in Germany, Hosted in Europe` | The home title joins the studio name to Software Made in Germany, Hosted in Europe with a  | C-FE-84 | Front-end specification metadata |
| `System Status` | The status board title joins System Status to the studio name with a bar | C-FE-86 | Front-end specification metadata |
| `Terms & Conditions` | The terms title joins Terms & Conditions to the studio name with a bar | C-FE-88 | Front-end specification metadata |
| `Build request` | The composer title joins Build request to the studio name with a bar | C-FE-90 | Front-end specification metadata |
| `hosted in Europe on privacy-first infrastructure` | The home description mentions hosted in Europe on privacy-first infrastructure | C-FE-92 | Front-end specification metadata |
| `Vela Studio - Software that scales` | The preview image alternative text reads Vela Studio - Software that scales | C-FE-95 | Front-end specification metadata |
| `1440` | The type sizes are measured at windows 1440, 990, 390 pixels wide | C-FE-107 | Front-end specification type sizes |
| `990` | The type sizes are measured at windows 1440, 990, 390 pixels wide | C-FE-107 | Front-end specification type sizes |
| `390` | The type sizes are measured at windows 1440, 990, 390 pixels wide | C-FE-107 | Front-end specification type sizes |
| `maintainable` | Card 02 marks maintainable, entirely yours in amber | C-FE-109 | Front-end specification home route table |
| `under a second` | Card 03 marks under a second, no tracking scripts in amber | C-FE-110 | Front-end specification home route table |
| `no tracking scripts` | Card 03 marks under a second, no tracking scripts in amber | C-FE-110 | Front-end specification home route table |
| `our own hardware` | Card 04 marks our own hardware, GDPR is the floor in amber | C-FE-111 | Front-end specification home route table |
| `GDPR is the floor` | Card 04 marks our own hardware, GDPR is the floor in amber | C-FE-111 | Front-end specification home route table |
| `Our racks, our keys` | Card 05 marks Our racks, our keys in amber | C-FE-112 | Front-end specification home route table |
| `owned outright` | Statement 01 - The craft marks owned outright, documented, hardware I can point to in ambe | C-FE-113 | Front-end specification founder page |
| `documented` | Statement 01 - The craft marks owned outright, documented, hardware I can point to in ambe | C-FE-113 | Front-end specification founder page |
| `hardware I can point to` | Statement 01 - The craft marks owned outright, documented, hardware I can point to in ambe | C-FE-113 | Front-end specification founder page |
| `the starting condition` | Statement 02 - The principle marks the starting condition, answerable to you in amber | C-FE-114 | Front-end specification founder page |
| `answerable to you` | Statement 02 - The principle marks the starting condition, answerable to you in amber | C-FE-114 | Front-end specification founder page |
| `Software development` | The document head gives the category Software development | C-FE-116 | Front-end specification metadata |
| `Every Vela Studio system, monitored continuously.` | The status lede begins Every Vela Studio system, monitored continuously | C-FE-118 | Front-end specification status board |
| `Looking for incident history, deeper diagnostics, or want to open a ticket? Full detail lives in the customer portal.` | The status notice reads Looking for incident history, deeper diagnostics, or want to open  | C-FE-119 | Front-end specification status board |
| `The live status feed could not be loaded right now.` | The failure block states The live status feed could not be loaded right now | C-FE-120 | Front-end specification status board |
| `The monitoring feed returned an empty project scope.` | The empty block adds The monitoring feed returned an empty project scope | C-FE-122 | Front-end specification status board |
| `Contact` | The legal notice names the blocks Contact, Registered office, VAT, Responsible for content | C-FE-123 | Front-end specification legal documents |
| `Registered office` | The legal notice names the blocks Contact, Registered office, VAT, Responsible for content | C-FE-123 | Front-end specification legal documents |
| `VAT` | The legal notice names the blocks Contact, Registered office, VAT, Responsible for content | C-FE-123 | Front-end specification legal documents |
| `Responsible for content` | The legal notice names the blocks Contact, Registered office, VAT, Responsible for content | C-FE-123 | Front-end specification legal documents |
| `Liability for content` | The legal notice names the blocks Contact, Registered office, VAT, Responsible for content | C-FE-123 | Front-end specification legal documents |
| `Liability for links` | The legal notice names the blocks Contact, Registered office, VAT, Responsible for content | C-FE-123 | Front-end specification legal documents |
| `2. Services` | The terms name the clauses 2. Services, 3. Client cooperation, 4. Fees, 5. Operations, 6.  | C-FE-125 | Front-end specification legal documents |
| `3. Client cooperation` | The terms name the clauses 2. Services, 3. Client cooperation, 4. Fees, 5. Operations, 6.  | C-FE-125 | Front-end specification legal documents |
| `4. Fees` | The terms name the clauses 2. Services, 3. Client cooperation, 4. Fees, 5. Operations, 6.  | C-FE-125 | Front-end specification legal documents |
| `5. Operations` | The terms name the clauses 2. Services, 3. Client cooperation, 4. Fees, 5. Operations, 6.  | C-FE-125 | Front-end specification legal documents |
| `6. Rights of use` | The terms name the clauses 2. Services, 3. Client cooperation, 4. Fees, 5. Operations, 6.  | C-FE-125 | Front-end specification legal documents |
| `7. Liability` | The terms name the clauses 2. Services, 3. Client cooperation, 4. Fees, 5. Operations, 6.  | C-FE-125 | Front-end specification legal documents |
| `18px` | The hero lede is 18px on a wide window, 16px below | C-FE-126 | Front-end specification type sizes |
| `64px` | The status heading is at most 64px | C-FE-128 | Front-end specification type sizes |
| `14px` | Legal body text drops to 14px on a phone | C-FE-129 | Front-end specification type sizes |
| `17px` | A legal clause heading drops to 17px on a phone | C-FE-130 | Front-end specification type sizes |
| `Marburg` | The founder page foot reads Marburg, a middle dot, Germany, with Scroll on the right | C-FE-154 | Front-end specification founder page |
| `Germany` | The founder page foot reads Marburg, a middle dot, Germany, with Scroll on the right | C-FE-154 | Front-end specification founder page |
| `10px` | A status tile label is 10px | C-FE-158 | Front-end specification type sizes |
| `12px` | A footer link is 12px | C-FE-159 | Front-end specification type sizes |
| `More of what I make, write` | The founder page note begins More of what I make, write | C-FE-186 | Front-end specification founder page |
| `1 Sept 2026, 15:38` | Board times read like 1 Sept 2026, 15:38 | C-FE-206 | Front-end specification status board |
| `Phone:` | The contact block labels read Phone:, Email:, WhatsApp Business: | C-FE-208 | Front-end specification legal documents |
| `Email:` | The contact block labels read Phone:, Email:, WhatsApp Business: | C-FE-208 | Front-end specification legal documents |
| `WhatsApp Business:` | The contact block labels read Phone:, Email:, WhatsApp Business: | C-FE-208 | Front-end specification legal documents |
| `vela-studio` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `vela-studio-finance` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `vela-studio-analytics` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `vela-studio-console` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `vela-studio-db-controller` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `vela-studio-tickets` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `anton-ferber-portfolio` | The seven system slugs in order are vela-studio, vela-studio-finance, vela-studio-analytic | C-FE-221 | Front-end specification status board table |
| `Alpine.js` | The front end is Alpine.js layered over server-rendered templates | C-TR-01 | Technical requirements para 1 |
| `Flask` | The backend with the HTTP API is Flask with Jinja | C-TR-02 | Technical requirements para 1 |
| `Jinja` | The backend with the HTTP API is Flask with Jinja | C-TR-02 | Technical requirements para 1 |
| `PostgreSQL` | Records live in PostgreSQL at DATABASE_URL | C-TR-05 | Technical requirements para 2 |
| `DATABASE_URL` | Records live in PostgreSQL at DATABASE_URL | C-TR-05 | Technical requirements para 2 |
| `STORAGE_ENDPOINT` | Briefs with the portrait live in minio at STORAGE_ENDPOINT | C-TR-06 | Technical requirements para 2 |
| `STORAGE_BUCKET` | The bucket name comes from STORAGE_BUCKET | C-TR-07 | Technical requirements para 2 |
| `STORAGE_ACCESS_KEY` | The storage key pair comes from STORAGE_ACCESS_KEY with STORAGE_SECRET_KEY | C-TR-08 | Technical requirements para 2 |
| `STORAGE_SECRET_KEY` | The storage key pair comes from STORAGE_ACCESS_KEY with STORAGE_SECRET_KEY | C-TR-08 | Technical requirements para 2 |
| `access_token` | A successful sign-in returns the account with an access_token | C-TR-10 | Technical requirements para 2 |
| `metric` | A measurement metric is lcp_ms, cls, p95_api_ms or uptime_percent | C-DM-11 | Data model measurements |
| `lcp_ms` | A measurement metric is lcp_ms, cls, p95_api_ms or uptime_percent | C-DM-11 | Data model measurements |
| `cls` | A measurement metric is lcp_ms, cls, p95_api_ms or uptime_percent | C-DM-11 | Data model measurements |
| `p95_api_ms` | A measurement metric is lcp_ms, cls, p95_api_ms or uptime_percent | C-DM-11 | Data model measurements |
| `uptime_percent` | A measurement metric is lcp_ms, cls, p95_api_ms or uptime_percent | C-DM-11 | Data model measurements |
| `content_type` | An attachment content_type is application/pdf, image/png or image/jpeg | C-DM-16 | Data model attachments |
| `application/pdf` | An attachment content_type is application/pdf, image/png or image/jpeg | C-DM-16 | Data model attachments |
| `image/png` | An attachment content_type is application/pdf, image/png or image/jpeg | C-DM-16 | Data model attachments |
| `image/jpeg` | An attachment content_type is application/pdf, image/png or image/jpeg | C-DM-16 | Data model attachments |
| `2026-09-01` | The console system holds seeded checks on 2026-09-01 behind the seeded incident | C-DM-23 | Data model seed data |
| `harbour-ledger` | The record harbour-ledger is a published software record delivered 2026-06-30 | C-DM-24 | Data model seed data |
| `2026-06-30` | The record harbour-ledger is a published software record delivered 2026-06-30 | C-DM-24 | Data model seed data |
| `180` | The record harbour-ledger holds p95_api_ms 180 measured 2026-07-14 | C-DM-25 | Data model seed data |
| `2026-07-14` | The record harbour-ledger holds p95_api_ms 180 measured 2026-07-14 | C-DM-25 | Data model seed data |
| `kestrel-storefront` | The record kestrel-storefront is a published website record delivered 2026-08-12 | C-DM-26 | Data model seed data |
| `2026-08-12` | The record kestrel-storefront is a published website record delivered 2026-08-12 | C-DM-26 | Data model seed data |
| `640` | The record kestrel-storefront holds lcp_ms 640 beside cls 0.01, measured 2026-08-20 | C-DM-27 | Data model seed data |
| `0.01` | The record kestrel-storefront holds lcp_ms 640 beside cls 0.01, measured 2026-08-20 | C-DM-27 | Data model seed data |
| `2026-08-20` | The record kestrel-storefront holds lcp_ms 640 beside cls 0.01, measured 2026-08-20 | C-DM-27 | Data model seed data |
| `lahn-clinic-hosting` | The record lahn-clinic-hosting is a published hosting record delivered 2026-05-02, client  | C-DM-28 | Data model seed data |
| `2026-05-02` | The record lahn-clinic-hosting is a published hosting record delivered 2026-05-02, client  | C-DM-28 | Data model seed data |
| `aurora-payroll-portal` | The record aurora-payroll-portal is an unpublished software record delivered 2026-09-05 | C-DM-29 | Data model seed data |
| `2026-09-05` | The record aurora-payroll-portal is an unpublished software record delivered 2026-09-05 | C-DM-29 | Data model seed data |
| `1450000` | The request VS-2026-0001 holds software, handover, de, standard, 25k-60k, figure 1450000,  | C-DM-31 | Data model seed data |
| `VS-2026-0002` | The request VS-2026-0002 from client2@example.com holds website, managed, eu, flexible, un | C-DM-32 | Data model seed data |
| `response_ms` | Each of the first five seeded systems holds twelve checks at a response_ms of 48 | C-DM-39 | Data model seed data |
| `48` | Each of the first five seeded systems holds twelve checks at a response_ms of 48 | C-DM-39 | Data model seed data |
| `2026-02-02` | The record harbour-ledger started 2026-02-02 for the shown client Lahnhafen Logistik | C-DM-41 | Data model seed data |
| `Lahnhafen Logistik` | The record harbour-ledger started 2026-02-02 for the shown client Lahnhafen Logistik | C-DM-41 | Data model seed data |
| `2026-05-11` | The record kestrel-storefront started 2026-05-11 for the shown client Kestrel Outdoor | C-DM-42 | Data model seed data |
| `Kestrel Outdoor` | The record kestrel-storefront started 2026-05-11 for the shown client Kestrel Outdoor | C-DM-42 | Data model seed data |
| `2026-03-16` | The record lahn-clinic-hosting started 2026-03-16 | C-DM-43 | Data model seed data |
| `2026-07-01` | The record aurora-payroll-portal started 2026-07-01 for the client Aurora Personal | C-DM-44 | Data model seed data |
| `Aurora Personal` | The record aurora-payroll-portal started 2026-07-01 for the client Aurora Personal | C-DM-44 | Data model seed data |
| `billing-brief.pdf` | The brief of VS-2026-0001 is named billing-brief.pdf under requests/VS-2026-0001/ | C-DM-45 | Data model seed data |
| `requests/VS-2026-0001/` | The brief of VS-2026-0001 is named billing-brief.pdf under requests/VS-2026-0001/ | C-DM-45 | Data model seed data |
| `Harbour Ledger` | The seeded record titles are Harbour Ledger, Kestrel Storefront, Lahn Clinic Hosting, Auro | C-DM-47 | Data model seed data |
| `Kestrel Storefront` | The seeded record titles are Harbour Ledger, Kestrel Storefront, Lahn Clinic Hosting, Auro | C-DM-47 | Data model seed data |
| `Lahn Clinic Hosting` | The seeded record titles are Harbour Ledger, Kestrel Storefront, Lahn Clinic Hosting, Auro | C-DM-47 | Data model seed data |
| `Aurora Payroll Portal` | The seeded record titles are Harbour Ledger, Kestrel Storefront, Lahn Clinic Hosting, Auro | C-DM-47 | Data model seed data |
| `Python` | The seeded stacks are Python, PostgreSQL for harbour; Python, Alpine.js for kestrel; Postg | C-DM-48 | Data model seed data |
| `14:15` | The console seed holds checks at 14:15 up, 14:20 down, 14:25 down, 14:30 down, 14:35 up, 1 | C-DM-49 | Data model seed data |
| `14:20` | The console seed holds checks at 14:15 up, 14:20 down, 14:25 down, 14:30 down, 14:35 up, 1 | C-DM-49 | Data model seed data |
| `14:25` | The console seed holds checks at 14:15 up, 14:20 down, 14:25 down, 14:30 down, 14:35 up, 1 | C-DM-49 | Data model seed data |
| `14:30` | The console seed holds checks at 14:15 up, 14:20 down, 14:25 down, 14:30 down, 14:35 up, 1 | C-DM-49 | Data model seed data |
| `14:35` | The console seed holds checks at 14:15 up, 14:20 down, 14:25 down, 14:30 down, 14:35 up, 1 | C-DM-49 | Data model seed data |
| `14:40` | The console seed holds checks at 14:15 up, 14:20 down, 14:25 down, 14:30 down, 14:35 up, 1 | C-DM-49 | Data model seed data |
| `POST /api/auth/login` | The route POST /api/auth/login takes email, password, returning the account role with an a | C-DC-17 | Deployment contract API shapes row 2 |
| `email` | The route POST /api/auth/login takes email, password, returning the account role with an a | C-DC-17 | Deployment contract API shapes row 2 |
| `password` | The route POST /api/auth/login takes email, password, returning the account role with an a | C-DC-17 | Deployment contract API shapes row 2 |
| `GET /api/build-requests/mine` | The route GET /api/build-requests/mine returns only the requests of the calling client, to | C-DC-18 | Deployment contract API shapes row 21 |
| `GET /api/build-requests` | The route GET /api/build-requests returns every request, newest first, only to the founder | C-DC-19 | Deployment contract API shapes row 20 |
| `POST /api/build-requests/{reference}/status` | The route POST /api/build-requests/{reference}/status takes status | C-DC-20 | Deployment contract API shapes row 24 |
| `POST /api/builds` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `capability` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `summary` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `body` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `stack` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `started_on` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `delivered_on` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `client_name` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `client_visible` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `diagram` | The route POST /api/builds takes slug, title, capability, summary, body, stack, started_on | C-DC-21 | Deployment contract API shapes row 13 |
| `POST /api/builds/{slug}/measurements` | The route POST /api/builds/{slug}/measurements takes metric, value, measured_on, source | C-DC-22 | Deployment contract API shapes row 16 |
| `value` | The route POST /api/builds/{slug}/measurements takes metric, value, measured_on, source | C-DC-22 | Deployment contract API shapes row 16 |
| `measured_on` | The route POST /api/builds/{slug}/measurements takes metric, value, measured_on, source | C-DC-22 | Deployment contract API shapes row 16 |
| `source` | The route POST /api/builds/{slug}/measurements takes metric, value, measured_on, source | C-DC-22 | Deployment contract API shapes row 16 |
| `POST /api/studio/portrait` | The route POST /api/studio/portrait takes the file part portrait, returning the stored por | C-DC-23 | Deployment contract API shapes row 25 |
| `portrait` | The route POST /api/studio/portrait takes the file part portrait, returning the stored por | C-DC-23 | Deployment contract API shapes row 25 |
| `object_key` | The route POST /api/studio/portrait takes the file part portrait, returning the stored por | C-DC-23 | Deployment contract API shapes row 25 |
| `POST /api/systems` | The route POST /api/systems takes slug, name, optional interval_seconds, open_after, close | C-DC-24 | Deployment contract API shapes row 8 |
| `interval_seconds` | The route POST /api/systems takes slug, name, optional interval_seconds, open_after, close | C-DC-24 | Deployment contract API shapes row 8 |
| `GET /api/studio/builds` | The route GET /api/studio/builds returns every record to the founder | C-DC-25 | Deployment contract API shapes row 12 |
| `POST /api/page-views` | The route POST /api/page-views takes route | C-DC-26 | Deployment contract API shapes row 27 |
| `route` | The route POST /api/page-views takes route | C-DC-26 | Deployment contract API shapes row 27 |
| `GET /api/page-views` | The route GET /api/page-views returns views newest first to the founder | C-DC-27 | Deployment contract API shapes row 28 |
| `GET /api/builds` | The route GET /api/builds returns published records newest delivery first, an optional cap | C-DC-28 | Deployment contract API shapes row 10 |
| `GET /api/builds/{slug}` | The route GET /api/builds/{slug} returns measurements beside diagram | C-DC-29 | Deployment contract API shapes row 11 |
| `measurements` | The route GET /api/builds/{slug} returns measurements beside diagram | C-DC-29 | Deployment contract API shapes row 11 |
| `entries` | The incident detail returns entries carrying seq, kind, body, recorded_at | C-DC-30 | Deployment contract API shapes row 6 |
| `recorded_at` | The incident detail returns entries carrying seq, kind, body, recorded_at | C-DC-30 | Deployment contract API shapes row 6 |
| `ref` | The incident list rows carry ref, system, opened_at, resolved_at | C-DC-31 | Deployment contract API shapes row 5 |
| `opened_at` | The incident list rows carry ref, system, opened_at, resolved_at | C-DC-31 | Deployment contract API shapes row 5 |
| `resolved_at` | The incident list rows carry ref, system, opened_at, resolved_at | C-DC-31 | Deployment contract API shapes row 5 |
| `POST /api/build-requests` | The route POST /api/build-requests takes a JSON body or a multipart form with an optional  | C-DC-32 | Deployment contract API shapes row 19 |
| `reference` | A created request returns reference, status, indicative_minor, currency, rules_version | C-DC-33 | Deployment contract API shapes row 19 |
| `currency` | A created request returns reference, status, indicative_minor, currency, rules_version | C-DC-33 | Deployment contract API shapes row 19 |
| `GET /api/build-requests/{reference}` | The route GET /api/build-requests/{reference} returns the request with the attachment | C-DC-35 | Deployment contract API shapes row 22 |
| `POST /api/builds/{slug}/publish` | The route POST /api/builds/{slug}/publish is founder only | C-DC-39 | Deployment contract API shapes row 14 |
| `POST /api/builds/{slug}/unpublish` | The route POST /api/builds/{slug}/unpublish is founder only | C-DC-40 | Deployment contract API shapes row 15 |
| `GET /api/build-requests/{reference}/attachment` | The route GET /api/build-requests/{reference}/attachment answers only the founder or the o | C-DC-41 | Deployment contract API shapes row 23 |
| `POST /api/auth/signup` | The route POST /api/auth/signup takes email, password | C-DC-42 | Deployment contract API shapes row 1 |
| `POST /api/uptime/incidents/{ref}/notes` | The route POST /api/uptime/incidents/{ref}/notes takes body, returning the appended entry | C-DC-45 | Deployment contract API shapes row 7 |
| `GET /api/uptime/projects` | GET /api/uptime/projects answers without a session | C-CF-80 | Core features rule 11 |
| `POST /api/systems/{slug}/checks` | The founder records a check with POST /api/systems/{slug}/checks | C-CF-94 | Core features rule 12 |
| `GET /api/uptime/incidents` | Anyone reads GET /api/uptime/incidents newest first | C-CF-125 | Core features rule 15 |
| `GET /api/uptime/incidents/{ref}` | Anyone reads GET /api/uptime/incidents/{ref} | C-CF-126 | Core features rule 15 |
| `6/7` | The Operational tile shows the up count, a slash with no surrounding space, the total, as  | C-CF-134 | Core features rule 16 |
| `/builds` | The /builds page lists published build records newest delivery first | C-CF-155 | Core features rule 17 |
| `See what we build` | The link See what we build lands where card 02 has finished drawing | C-CF-195 | Core features rule 20 |
| `GET /api/portrait` | GET /api/portrait serves the uploaded portrait to anyone | C-CF-216 | Core features rule 23 |
| `/` | The back pill returns to / | C-CF-230 | Core features rule 25 |
| `/studio/page-views` | Only the founder reads the page-view log at /studio/page-views | C-CF-234 | Core features rule 27 |
| `checked_at` | An exact repeat means the same checked_at with the same status, whatever the response_ms | C-CF-258 | Core features rule 12 |
| `Sign in` | Beneath the composer form a Sign in link opens /login carrying the composer address as the | C-CF-298 | Core features rule 3 |
| `/studio/builds` | The founder adds a build record from the side panel on /studio/builds | C-CF-312 | Core features rule 29 |
| `/studio/systems` | The routes /studio/builds, /studio/systems, /studio/page-views require the founder role | C-UF-03 | User flow route table |
| `401` | Any action sent with a session that has gone missing, a build request among them, is refus | C-UF-06 | User flow entry and redirects |
| `/about` | A portrait the founder uploads appears on /about | C-UF-15 | User flow founder journey |
| `Sign out` | The studio top bar ends at the right with a Sign out button | C-UF-25 | Core features rule 29 |
| `accounts` | The accounts table holds an email unique without regard to case beside a role | C-DM-01 | Data model accounts |
| `systems` | The systems table holds a unique slug, name, a unique position, interval_seconds, open_aft | C-DM-02 | Data model systems |
| `checks` | The checks table holds checked_at, status, response_ms for the owning system | C-DM-04 | Data model checks |
| `incidents` | The incidents table holds a unique ref, opened_at, a resolved_at that stays null until the | C-DM-06 | Data model incidents |
| `incident_entries` | The incident_entries table holds seq, kind, body, recorded_at | C-DM-07 | Data model incident_entries |
| `build_records` | The build_records table holds slug, title, capability, stack, delivered_on, client_visible | C-DM-09 | Data model build_records |
| `published` | The build_records table holds slug, title, capability, stack, delivered_on, client_visible | C-DM-09 | Data model build_records |
| `published_at` | The build_records table holds slug, title, capability, stack, delivered_on, client_visible | C-DM-09 | Data model build_records |
| `build_requests` | The build_requests table holds reference, contact_email, capabilities, rules_version, indi | C-DM-13 | Data model build_requests |
| `status_changed_at` | The build_requests table holds reference, contact_email, capabilities, rules_version, indi | C-DM-13 | Data model build_requests |
| `attachments` | The attachments table holds a unique object_key, content_type, byte_size, sha256, original | C-DM-15 | Data model attachments |
| `byte_size` | The attachments table holds a unique object_key, content_type, byte_size, sha256, original | C-DM-15 | Data model attachments |
| `sha256` | The attachments table holds a unique object_key, content_type, byte_size, sha256, original | C-DM-15 | Data model attachments |
| `original_name` | The attachments table holds a unique object_key, content_type, byte_size, sha256, original | C-DM-15 | Data model attachments |
| `page_views` | The page_views table holds only route with viewed_at | C-DM-17 | Data model page_views |
| `viewed_at` | The page_views table holds only route with viewed_at | C-DM-17 | Data model page_views |
| `portraits` | The portraits table holds object_key, content_type, uploaded_at, the newest row shown | C-DM-18 | Data model portraits |
| `uploaded_at` | The portraits table holds object_key, content_type, uploaded_at, the newest row shown | C-DM-18 | Data model portraits |
| `/app/USER_README.md` | The seeded password deku-demo-pw-2026 is written into /app/USER_README.md beside each acco | C-DM-38 | Data model para 2 |
| `APP_PUBLIC_URL` | The app is reachable at APP_PUBLIC_URL | C-DC-01 | Deployment contract bullet 1 |
| `${APP_PUBLIC_PORT}:4173` | The port mapping is ${APP_PUBLIC_PORT}:4173, read from the environment | C-DC-02 | Deployment contract bullet 1 |
| `/api` | The HTTP API is served on the same origin under /api | C-DC-03 | Deployment contract bullet 2 |
| `GET /api/health` | The route GET /api/health returns 200 once the app is ready | C-DC-04 | Deployment contract bullet 3 |
| `200` | The route GET /api/health returns 200 once the app is ready | C-DC-04 | Deployment contract bullet 3 |
| `.browser_screenshots/` | Empty .browser_screenshots/ with .downloads/ directories exist at the app root | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | Empty .browser_screenshots/ with .downloads/ directories exist at the app root | C-DC-07 | Deployment contract bullet 6 |
| `0.0.0.0` | The server binds 0.0.0.0 | C-DC-10 | Deployment contract bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the feed's short-lived cache lifetime | C-TR-17 | UNPINNED: the brief gives no duration, so any short lifetime conforms |
| the document and critical stylesheet budgets that each stay small | C-TR-34 | UNPINNED: the brief gives no byte size |
| the four layout breakpoints named by description only | C-UX-29 | UNPINNED: the brief gives no pixel widths |
| a target comfortably sized for a finger | C-UX-37 | UNPINNED: the brief gives no pixel size |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 8 |
| User roles | 1 | 30 |
| Core features | 28 | 313 |
| User flow | 11 | 35 |
| UI/UX notes | 3 | 70 |
| Front-end specification | 6 | 221 |
| Technical requirements | 6 | 35 |
| Data model | 6 | 51 |
| Constraints | 1 | 9 |
| Deployment contract | 9 | 46 |

Definition of done carries 2 obligation-bearing sentences; both restate Core features rules 1, 2, 6, 7 and 8 and produce no separate item.
