# Checklist: Agency Campaign Operations

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, front-end specification, technical requirements, data model, constraints, deployment contract
Sections absent: build plan
Items: 673
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` Every public route exists in Japanese at the root. `src: Overview para 2`
- [ ] `C-OV-02` `capability` Every public route exists in English under the `/en/` prefix. `src: Overview para 2`
- [ ] `C-OV-03` `capability` The operations platform lives under `/studio` behind a sign-in. `src: Overview para 3`
- [ ] `C-OV-04` `constraint` The product offers no client login. `src: Overview para 5`
- [ ] `C-OV-05` `constraint` The product offers no self-service signup. `src: Overview para 5`
- [ ] `C-OV-06` `constraint` The product has no executive dashboard, no global administrator. `src: Overview para 5`
- [ ] `C-OV-07` `constraint` The product has no payments, no invoicing, no mail delivery, no chat, no third-party analytics. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` An `account_director` opens briefs on accounts the account director owns. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An `account_director` approves estimates on the client's behalf. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An `account_director` converts a brief into a job. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An `account_director` records case-study permission for a campaign. `src: User roles table row 1`
- [ ] `C-RL-05` `role` An `account_director` grants clearances on owned accounts. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `producer` writes estimates. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A `producer` staffs crews on a job. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A `producer` publishes rate cards. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A `producer` records a departure in the people directory. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A `creative` uploads work versions. `src: User roles table row 3`
- [ ] `C-RL-11` `role` A `creative` sets the internal review status of a version. `src: User roles table row 3`
- [ ] `C-RL-12` `role` A `legal` user records rights clearances on a job. `src: User roles table row 4`
- [ ] `C-RL-13` `role` A `legal` user places a legal hold on a job. `src: User roles table row 4`
- [ ] `C-RL-14` `role` An `editor` publishes campaigns to the public site. `src: User roles table row 5`
- [ ] `C-RL-15` `role` An `editor` records award results on the awards desk. `src: User roles table row 5`
- [ ] `C-RL-16` `role` A `creative` session is denied an `editor`-only endpoint, leaving the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-17` `role` A `creative` session is denied approving an estimate. `src: User roles table row 3`
- [ ] `C-RL-18` `role` A `producer` session is denied lifting a legal hold. `src: User roles table row 2`
- [ ] `C-RL-19` `constraint` No account reads every job regardless of clearance. `src: User roles para 2`
- [ ] `C-RL-20` `constraint` Every platform account is seeded rather than created through signup. `src: User roles para 1`
- [ ] `C-RL-21` `literal` The seeded account `account_director@example.com` holds the role `account_director`. `src: User roles seeded table row 1`
- [ ] `C-RL-22` `literal` The seeded account `account_director2@example.com` holds the role `account_director`. `src: User roles seeded table row 2`
- [ ] `C-RL-23` `literal` The seeded account `producer@example.com` holds the role `producer`. `src: User roles seeded table row 3`
- [ ] `C-RL-24` `literal` The seeded account `producer2@example.com` holds the role `producer`. `src: User roles seeded table row 4`
- [ ] `C-RL-25` `literal` The seeded account `creative@example.com` holds the role `creative`. `src: User roles seeded table row 5`
- [ ] `C-RL-26` `literal` The seeded account `creative2@example.com` holds the role `creative`. `src: User roles seeded table row 6`
- [ ] `C-RL-27` `literal` The seeded account `legal@example.com` holds the role `legal`. `src: User roles seeded table row 7`
- [ ] `C-RL-28` `literal` The seeded account `editor@example.com` holds the role `editor`. `src: User roles seeded table row 8`
- [ ] `C-RL-29` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles para 4`
- [ ] `C-RL-30` `literal` The seeded creative `creative2@example.com` is cleared for `tsubame-automotive` only. `src: User roles seeded table row 6`
- [ ] `C-RL-31` `literal` The seeded producer `producer@example.com` is cleared for `hoshino-motors`, `kagerou-beverages`, `aozora-airlines`, `minato-rail`. `src: User roles seeded table row 3`
- [ ] `C-RL-32` `role` A `creative` session is denied a `producer`-only endpoint, leaving the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-33` `role` A `creative` session is denied a `legal`-only endpoint, leaving the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-34` `role` A `creative` session is denied an `account_director`-only endpoint, leaving the protected state unchanged. `src: User roles para 3`
- [ ] `C-RL-35` `role` An `account_director` is denied writing an estimate. `src: User roles table`
- [ ] `C-RL-36` `role` An `account_director` is denied staffing a crew. `src: User roles table`
- [ ] `C-RL-37` `role` An `account_director` is denied publishing a campaign. `src: User roles table`
- [ ] `C-RL-38` `role` A `producer` is denied approving an estimate. `src: User roles table`
- [ ] `C-RL-39` `role` A `producer` is denied recording rights. `src: User roles table`
- [ ] `C-RL-40` `role` A `producer` is denied publishing a campaign. `src: User roles table`
- [ ] `C-RL-41` `role` A `creative` is denied approving an estimate. `src: User roles table`
- [ ] `C-RL-42` `role` A `creative` is denied staffing a crew. `src: User roles table`
- [ ] `C-RL-43` `role` A `creative` is denied editing credits. `src: User roles table`
- [ ] `C-RL-44` `role` A `legal` session is denied publishing a campaign. `src: User roles table`
- [ ] `C-RL-45` `role` A `legal` session is denied editing credits. `src: User roles table`
- [ ] `C-RL-46` `role` An `editor` is denied granting a clearance. `src: User roles table`
- [ ] `C-RL-47` `role` An `editor` is denied recording rights. `src: User roles table`
- [ ] `C-RL-48` `role` An `account_director` revokes a clearance on an owned account. `src: User roles table`
- [ ] `C-RL-49` `role` An `account_director` records a client's approval of a work version. `src: User roles table`
- [ ] `C-RL-50` `role` A `producer` withdraws a work version not under hold. `src: User roles table`
- [ ] `C-RL-51` `role` A `producer` ends an assignment. `src: User roles table`
- [ ] `C-RL-52` `role` An `editor` creates a preview link, revokes a preview link. `src: User roles table`
- [ ] `C-RL-53` `role` An `editor` unpublishes a campaign. `src: User roles table`
- [ ] `C-RL-54` `role` An `editor` edits a campaign translation. `src: User roles table`
- [ ] `C-RL-55` `role` An `editor` uploads hero media. `src: User roles table`
- [ ] `C-RL-56` `literal` `account_director@example.com` owns `hoshino-motors`, `kagerou-beverages`. `src: User roles account owners`
- [ ] `C-RL-57` `literal` `account_director2@example.com` owns `tsubame-automotive`, `aozora-airlines`, `minato-rail`. `src: User roles account owners`

## C-CF Core features

- [ ] `C-CF-01` `capability` A person reads a job only when holding a current clearance for every account of the job. `src: Core features rule 1`
- [ ] `C-CF-02` `constraint` A walled job is absent from the job list. `src: Core features rule 1`
- [ ] `C-CF-03` `constraint` A walled job is absent from internal search. `src: Core features rule 1`
- [ ] `C-CF-04` `constraint` A walled job is absent from autocomplete. `src: Core features rule 1`
- [ ] `C-CF-05` `constraint` A walled job is absent from the jobs export. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` A walled job is absent from the burn report totals. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` A walled assignment is absent from a colleague's assignment history in the people directory. `src: Core features rule 1`
- [ ] `C-CF-08` `constraint` A walled job's audit trail answers exactly as a missing job's audit trail does. `src: Core features rule 1`
- [ ] `C-CF-09` `constraint` A direct fetch of a walled job returns the same not-found status as a missing job. `src: Core features rule 1`
- [ ] `C-CF-10` `constraint` A direct fetch of a walled job returns the same body shape as a missing job. `src: Core features rule 1`
- [ ] `C-CF-11` `literal` The walled creative `creative2@example.com` finds no trace of `Hoshino EV Launch`. `src: Core features rule 1`
- [ ] `C-CF-12` `literal` The cleared creative `creative@example.com` reads `Hoshino EV Launch` in full. `src: Core features rule 1`
- [ ] `C-CF-13` `constraint` A walled job's files are never served to a person outside the wall. `src: Core features rule 1`
- [ ] `C-CF-14` `literal` A split job's apportionment sums to exactly `10000` in basis-point shares. `src: Core features rule 2`
- [ ] `C-CF-15` `constraint` A conversion whose shares miss the whole is refused, writing nothing. `src: Core features rule 2`
- [ ] `C-CF-16` `capability` A split job's wall requires clearance for every one of the split job's accounts. `src: Core features rule 2`
- [ ] `C-CF-17` `literal` The split job `Sky Tea Partnership` gives `kagerou-beverages` a share of `6000`. `src: Core features rule 2`
- [ ] `C-CF-18` `literal` The cleared producer `producer@example.com` reads `Sky Tea Partnership`. `src: Core features rule 2`
- [ ] `C-CF-19` `literal` The creative `creative@example.com` receives a not-found for `Sky Tea Partnership`. `src: Core features rule 2`
- [ ] `C-CF-20` `constraint` A clearance for a competitor of a client the person currently holds is refused. `src: Core features rule 3`
- [ ] `C-CF-21` `literal` A clearance for a competitor held within the last `90` days is refused. `src: Core features rule 3`
- [ ] `C-CF-22` `capability` Membership of a client-dedicated unit derives a clearance for the unit's account. `src: Core features rule 3`
- [ ] `C-CF-23` `literal` The unit `Hoshino Unit` is dedicated to `hoshino-motors`. `src: Core features rule 3`
- [ ] `C-CF-24` `capability` A brief carries the problem, the convention, the deliverables, the deadline, the budget, the markets. `src: Core features rule 4`
- [ ] `C-CF-25` `constraint` A conversion without an approved estimate is refused, creating no job. `src: Core features rule 4`
- [ ] `C-CF-26` `constraint` A conversion without a named producer is refused, creating no job. `src: Core features rule 4`
- [ ] `C-CF-27` `capability` A converted job records the rate card version pinned to the job. `src: Core features rule 4`
- [ ] `C-CF-28` `constraint` A revised estimate needs approval again before conversion. `src: Core features rule 4`
- [ ] `C-CF-29` `capability` A job keeps the rate card version current at conversion for the job's life. `src: Core features rule 5`
- [ ] `C-CF-30` `constraint` Publishing a newer rate card changes no cost on an already converted job. `src: Core features rule 5`
- [ ] `C-CF-31` `literal` The seeded card `RC-2026` is current at first start. `src: Core features rule 5`
- [ ] `C-CF-32` `capability` A time entry costs the pinned hourly rate times the minutes divided by sixty, in whole yen rounded half up. `src: Core features rule 6`
- [ ] `C-CF-33` `literal` A time entry of `450` minutes as `Art Director` under `RC-2026` costs `90000`. `src: Core features rule 6`
- [ ] `C-CF-34` `capability` A third-party cost stores the original amount, currency, converted amount, exchange rate, rate date exactly as entered. `src: Core features rule 6`
- [ ] `C-CF-35` `literal` A cost of `125000` in `usd` at `148.50` on `2026-03-31` converts to `185625` yen. `src: Core features rule 6`
- [ ] `C-CF-36` `capability` A job's cost adds the converted third-party costs to the time cost. `src: Core features rule 6`
- [ ] `C-CF-37` `literal` The ledger currency is `jpy`. `src: Core features rule 6`
- [ ] `C-CF-38` `capability` A correction to a time entry in a closed month creates an adjusting entry referencing the original entry. `src: Core features rule 7`
- [ ] `C-CF-39` `constraint` A correction to a time entry in a closed month leaves the original entry unchanged. `src: Core features rule 7`
- [ ] `C-CF-40` `capability` An adjusting entry carries the difference in minutes. `src: Core features rule 7`
- [ ] `C-CF-41` `capability` Ending an assignment keeps the assignment in the job's assignment history. `src: Core features rule 8`
- [ ] `C-CF-42` `constraint` A request to delete an assignment is refused. `src: Core features rule 8`
- [ ] `C-CF-43` `constraint` Committed minutes per week across overlapping assignments never exceed a person's capacity. `src: Core features rule 8`
- [ ] `C-CF-44` `literal` A capacity refusal involving a walled job says exactly `That person is fully committed in the weeks you selected.` `src: Core features rule 8`
- [ ] `C-CF-45` `constraint` A capacity refusal involving a walled job names no job title, no identifier, no count. `src: Core features rule 8`
- [ ] `C-CF-46` `constraint` Staffing a person onto a job whose accounts the person is not cleared for is refused. `src: Core features rule 8`
- [ ] `C-CF-47` `capability` Each new upload creates the next numbered version, counted from `1`. `src: Core features rule 9`
- [ ] `C-CF-48` `constraint` A new upload never overwrites the bytes of an earlier version. `src: Core features rule 9`
- [ ] `C-CF-49` `literal` Version bytes are stored in `minio` at the key `jobs/{job_id}/versions/{version_number}/{sha256_of_bytes}.{ext}`. `src: Core features rule 9`
- [ ] `C-CF-50` `constraint` Version bytes are served only to people the wall admits. `src: Core features rule 9`
- [ ] `C-CF-51` `capability` Each version carries an internal review status of its own. `src: Core features rule 10`
- [ ] `C-CF-52` `capability` Each version carries a client review status of its own. `src: Core features rule 10`
- [ ] `C-CF-53` `constraint` Setting one review status never changes the other review status. `src: Core features rule 10`
- [ ] `C-CF-54` `capability` A comment attaches to one version with a timecode or a region. `src: Core features rule 11`
- [ ] `C-CF-55` `constraint` The client view of a version never carries an `internal` comment. `src: Core features rule 11`
- [ ] `C-CF-56` `capability` A comment on an earlier version still reads on that version after a later upload. `src: Core features rule 11`
- [ ] `C-CF-57` `capability` Restoring an earlier version creates a new version carrying the earlier digest. `src: Core features rule 12`
- [ ] `C-CF-58` `constraint` Restoring a version removes no intervening version. `src: Core features rule 12`
- [ ] `C-CF-59` `capability` A legal user records rights of the kinds music, talent, imagery, claims, trademark, festival exhibition. `src: Core features rule 13`
- [ ] `C-CF-60` `capability` Festival exhibition is recorded as a distinct right. `src: Core features rule 13`
- [ ] `C-CF-61` `capability` Clearance for a market is complete only when a right covers that market, every right covering that market being cleared on that day. `src: Core features rule 13`
- [ ] `C-CF-62` `capability` An expired right removes the campaign from public reads in the markets the right covered. `src: Core features rule 14`
- [ ] `C-CF-63` `constraint` An expired right leaves the campaign visible in markets whose rights still run. `src: Core features rule 14`
- [ ] `C-CF-64` `literal` The seeded campaign `Tide Clock` is absent for market `DE` but present for market `JP`. `src: Core features rule 14`
- [ ] `C-CF-65` `constraint` A version of a job under legal hold cannot be deleted. `src: Core features rule 15`
- [ ] `C-CF-66` `constraint` Lifting a legal hold without a reason is refused. `src: Core features rule 15`
- [ ] `C-CF-67` `capability` Lifting a legal hold writes an audit event carrying the actor, the time, the reason. `src: Core features rule 15`
- [ ] `C-CF-68` `constraint` Retention schedules are suspended for a job under legal hold. `src: Core features rule 15`
- [ ] `C-CF-69` `capability` A credit entry holds a role in both languages with one or more people. `src: Core features rule 16`
- [ ] `C-CF-70` `capability` A credit list keeps entries in the order the editor set. `src: Core features rule 16`
- [ ] `C-CF-71` `capability` A role may appear more than once in one credit list. `src: Core features rule 16`
- [ ] `C-CF-72` `literal` The `Night Signal` credits name `Yuto Baba`, `Riko Nishi`, `Sho Ota` together in one `Producer` entry. `src: Core features rule 16`
- [ ] `C-CF-73` `constraint` Crediting a person with no assignment on the campaign's job is refused. `src: Core features rule 17`
- [ ] `C-CF-74` `constraint` Crediting a person without current clearance for every job account is refused. `src: Core features rule 17`
- [ ] `C-CF-75` `capability` A departed person stays credited on every campaign the person made. `src: Core features rule 17`
- [ ] `C-CF-76` `capability` A renamed person appears under the new name on unpinned credit entries. `src: Core features rule 17`
- [ ] `C-CF-77` `capability` A pinned credit entry keeps the name under which the work was made. `src: Core features rule 17`
- [ ] `C-CF-78` `capability` Two credit saves from one revision admit exactly one save. `src: Core features rule 18`
- [ ] `C-CF-79` `constraint` A credit save from a stale revision is refused as a conflict, changing nothing. `src: Core features rule 18`
- [ ] `C-CF-80` `ui` The studio shows a person both the rejected credit version beside the current one. `src: Core features rule 18`
- [ ] `C-CF-81` `capability` A departure ends the person's assignments on the departure date. `src: Core features rule 19`
- [ ] `C-CF-82` `capability` A departure revokes the person's clearances. `src: Core features rule 19`
- [ ] `C-CF-83` `capability` A departure drops the person's capacity to zero. `src: Core features rule 19`
- [ ] `C-CF-84` `literal` A departure sets the person's status to `departed`. `src: Core features rule 19`
- [ ] `C-CF-85` `constraint` A departed person is never shown publicly as a profile. `src: Core features rule 19`
- [ ] `C-CF-86` `constraint` A returning person's clearances are never restored automatically. `src: Core features rule 19`
- [ ] `C-CF-87` `capability` A person record carries names in both scripts with a reading for collation. `src: Core features rule 20`
- [ ] `C-CF-88` `constraint` A colleague without clearance sees no count of hidden assignments. `src: Core features rule 20`
- [ ] `C-CF-89` `capability` Each award body carries its own ranks. `src: Core features rule 21`
- [ ] `C-CF-90` `literal` The rank `Jade Petal` exists at `Lotus Festival` only. `src: Core features rule 21`
- [ ] `C-CF-91` `literal` The rank `Grand Lotus` counts toward `Gold`. `src: Core features rule 21`
- [ ] `C-CF-92` `constraint` A second award entry with the same campaign, body, category, year is refused. `src: Core features rule 21`
- [ ] `C-CF-93` `capability` One campaign holds several results from one body in one year. `src: Core features rule 21`
- [ ] `C-CF-94` `constraint` A shortlisted result never reaches a public surface. `src: Core features rule 22`
- [ ] `C-CF-95` `capability` Only confirmed award results reach public surfaces. `src: Core features rule 22`
- [ ] `C-CF-96` `capability` An award entry records the client's permission as a reference. `src: Core features rule 22`
- [ ] `C-CF-97` `capability` Confirming a result moves the campaign award list, the article breakdown, the agency tally together. `src: Core features rule 23`
- [ ] `C-CF-98` `literal` The `Lotus Festival` `2025` headline reads `Gold` 3, `Silver` 2, `Bronze` 2, `Jade Petal` 2 over nine itemised results. `src: Core features rule 23`
- [ ] `C-CF-99` `constraint` Publishing a campaign without case-study permission is refused. `src: Core features rule 24`
- [ ] `C-CF-100` `constraint` Publishing a campaign with an empty credit list is refused. `src: Core features rule 24`
- [ ] `C-CF-101` `constraint` Publishing a campaign before clearance is complete for the markets is refused. `src: Core features rule 24`
- [ ] `C-CF-102` `capability` A refused publish names each failed condition in the `reasons` list. `src: Core features rule 24`
- [ ] `C-CF-103` `constraint` A refused publish changes nothing. `src: Core features rule 24`
- [ ] `C-CF-104` `constraint` A scheduled publish releasing after one of the campaign's rights ends is refused at scheduling time. `src: Core features rule 24`
- [ ] `C-CF-105` `capability` A publish meeting all four conditions makes the campaign public in the chosen markets. `src: Core features rule 24`
- [ ] `C-CF-106` `literal` The refusal notice at scheduling reads `The campaign cannot be published yet: clearance for one market expires before the scheduled date.` `src: Core features rule 24`
- [ ] `C-CF-107` `constraint` An embargoed campaign is absent from every public index. `src: Core features rule 25`
- [ ] `C-CF-108` `constraint` An embargoed campaign is absent from the sitemap. `src: Core features rule 25`
- [ ] `C-CF-109` `constraint` An embargoed campaign is absent from public search. `src: Core features rule 25`
- [ ] `C-CF-110` `constraint` An embargoed campaign's public address answers the same not-found status as an unknown address. `src: Core features rule 25`
- [ ] `C-CF-111` `constraint` An embargoed campaign's hero bytes are never served to the public. `src: Core features rule 25`
- [ ] `C-CF-112` `literal` The seeded campaign `Silent Aurora` stays embargoed until `2099-01-01T09:00:00+09:00`. `src: Core features rule 25`
- [ ] `C-CF-113` `capability` The seeded campaign `Harbour Lights` becomes public after release with nobody acting. `src: Core features rule 25`
- [ ] `C-CF-114` `capability` An editor creates a preview link for an unpublished or embargoed campaign. `src: Core features rule 26`
- [ ] `C-CF-115` `constraint` A revoked preview link answers not-found. `src: Core features rule 26`
- [ ] `C-CF-116` `constraint` A preview link response forbids indexing. `src: Core features rule 26`
- [ ] `C-CF-117` `capability` A field with no published translation falls back to the other locale's published text. `src: Core features rule 27`
- [ ] `C-CF-118` `capability` A fallback field reports the locale actually shown. `src: Core features rule 27`
- [ ] `C-CF-119` `literal` The English `Quiet Engine` shows an English title over a Japanese description marked `ja`. `src: Core features rule 27`
- [ ] `C-CF-120` `constraint` An item with no published translation in either locale is absent from public indexes. `src: Core features rule 27`
- [ ] `C-CF-121` `constraint` An item with no published translation answers not-found at the item's address. `src: Core features rule 27`
- [ ] `C-CF-122` `ui` Switching language on a campaign opens the same campaign in the other language. `src: Core features rule 28`
- [ ] `C-CF-123` `ui` Switching language on an untranslated campaign opens the target work index with an explanatory note. `src: Core features rule 28`
- [ ] `C-CF-124` `capability` The Japanese client register sorts clients by reading. `src: Core features rule 29`
- [ ] `C-CF-125` `literal` The Japanese client register lists `Aozora Airlines`, `Kagerou Beverages`, `Tsubame Automotive`, `Hoshino Motors`, `Minato Rail` in order. `src: Core features rule 29`
- [ ] `C-CF-126` `ui` English dates render in the long form, such as `21 June 2025`. `src: Core features rule 29`
- [ ] `C-CF-127` `capability` Public search finds a campaign by any run of characters inside the Japanese title. `src: Core features rule 30`
- [ ] `C-CF-128` `capability` Public search finds a campaign by the reading of the title. `src: Core features rule 30`
- [ ] `C-CF-129` `literal` Searching `信号` finds `Night Signal`. `src: Core features rule 30`
- [ ] `C-CF-130` `capability` The work index lists twelve campaigns per page. `src: Core features rule 31`
- [ ] `C-CF-131` `capability` The work index reports the total count of public campaigns. `src: Core features rule 31`
- [ ] `C-CF-132` `capability` The year facet lists the five most recent years holding published work. `src: Core features rule 31`
- [ ] `C-CF-133` `literal` The year facet ends with `before`, collecting everything older than the oldest listed year. `src: Core features rule 31`
- [ ] `C-CF-134` `capability` The year facet boundary is derived from the published work every time. `src: Core features rule 31`
- [ ] `C-CF-135` `ui` The chosen year appears in the address as a query parameter. `src: Core features rule 31`
- [ ] `C-CF-136` `constraint` A page number past the end falls back to the last page. `src: Core features rule 31`
- [ ] `C-CF-137` `capability` Only campaigns public in the requested market count toward the work index. `src: Core features rule 31`
- [ ] `C-CF-138` `ui` Campaign detail shows a fact block with clients, category, month, year. `src: Core features rule 32`
- [ ] `C-CF-139` `ui` Campaign detail collapses the outline behind a read-more control that expands in place. `src: Core features rule 32`
- [ ] `C-CF-140` `ui` Campaign detail groups awards by body with the year. `src: Core features rule 32`
- [ ] `C-CF-141` `ui` Campaign detail offers a copy-link control that confirms. `src: Core features rule 32`
- [ ] `C-CF-142` `ui` Campaign detail shows four related campaigns. `src: Core features rule 32`
- [ ] `C-CF-143` `capability` A campaign lists every client with one client marked primary. `src: Core features rule 32`
- [ ] `C-CF-144` `literal` The campaign `Night Signal` lists `Kagerou Beverages` as primary. `src: Core features rule 32`
- [ ] `C-CF-145` `capability` The newsroom lists nine articles per page. `src: Core features rule 33`
- [ ] `C-CF-146` `capability` The category facet matches an article carrying several categories. `src: Core features rule 33`
- [ ] `C-CF-147` `capability` The category facet composes with the year facet. `src: Core features rule 33`
- [ ] `C-CF-148` `capability` An award article shows a per-campaign breakdown read from the campaign results. `src: Core features rule 33`
- [ ] `C-CF-149` `literal` The article `Lotus Festival 2025 results` carries the categories `awards`, `news`. `src: Core features rule 33`
- [ ] `C-CF-150` `capability` The company record shows an officer's concurrent position apart from the officer's title. `src: Core features rule 34`
- [ ] `C-CF-151` `literal` The officer `Hiroshi Kudo` holds a concurrent position at `Meido Group`. `src: Core features rule 34`
- [ ] `C-CF-152` `capability` The company record lists ten organisational units, two dedicated to a single client. `src: Core features rule 34`
- [ ] `C-CF-153` `capability` A careers opening carries a track, a title, an external apply address. `src: Core features rule 34`
- [ ] `C-CF-154` `ui` A careers apply link is marked as leaving the site. `src: Core features rule 34`
- [ ] `C-CF-155` `literal` An unreachable openings list shows `We cannot reach the recruiting service right now. Here is how to contact us directly.` `src: Core features rule 34`
- [ ] `C-CF-156` `capability` A repeated submission of one idempotency key stores exactly one enquiry. `src: Core features rule 35`
- [ ] `C-CF-157` `constraint` A submission arriving less than one second after the key was issued is refused. `src: Core features rule 35`
- [ ] `C-CF-158` `literal` A submission with the decoy field `website` filled is refused. `src: Core features rule 35`
- [ ] `C-CF-159` `constraint` A submission without consent is refused, storing nothing. `src: Core features rule 35`
- [ ] `C-CF-160` `capability` Each enquiry type routes through a routing table held as data. `src: Core features rule 35`
- [ ] `C-CF-161` `literal` A `general` enquiry falls back to `desk@kuromeido.example.com` with a routing warning. `src: Core features rule 35`
- [ ] `C-CF-162` `literal` A `new_business` enquiry routes to `newbusiness@kuromeido.example.com`. `src: Core features rule 35`
- [ ] `C-CF-163` `constraint` The app sends no mail for an enquiry. `src: Core features rule 35`
- [ ] `C-CF-164` `ui` Contact form errors sit beside their field, announced to assistive technology. `src: Core features rule 35`
- [ ] `C-CF-165` `ui` Focus moves to the first contact form error. `src: Core features rule 35`
- [ ] `C-CF-166` `literal` The enquiry confirmation reads `Thank you. We will reply within two working days.` `src: Core features rule 35`
- [ ] `C-CF-167` `ui` The contact form consent box starts unticked. `src: Core features rule 35`
- [ ] `C-CF-168` `ui` Every public page footer links to the terms page. `src: Core features rule 36`
- [ ] `C-CF-169` `ui` The contact form links to the terms page beside the consent box. `src: Core features rule 36`
- [ ] `C-CF-170` `ui` The terms page carries numbered clauses with a table of contents deep-linking each clause. `src: Core features rule 36`
- [ ] `C-CF-171` `capability` An unresolved address returns a real not-found status. `src: Core features rule 37`
- [ ] `C-CF-172` `literal` The designed not-found screen shows `Sorry, nothing lives at that address.` `src: Core features rule 37`
- [ ] `C-CF-173` `constraint` The not-found screen never echoes the requested path. `src: Core features rule 37`
- [ ] `C-CF-174` `capability` Every public page view records one row carrying the route, the time. `src: Core features rule 38`
- [ ] `C-CF-175` `role` Only an `editor` reads the page-view log. `src: Core features rule 38`
- [ ] `C-CF-176` `capability` The sitemap lists every public route in both languages. `src: Core features rule 39`
- [ ] `C-CF-177` `capability` The robots file names the sitemap by the sitemap's full address. `src: Core features rule 39`
- [ ] `C-CF-178` `ui` Every content image on the public site carries alternative text in the page's language. `src: Core features rule 40`
- [ ] `C-CF-179` `ui` Decorative images on the public site declare themselves decorative. `src: Core features rule 40`
- [ ] `C-CF-180` `constraint` No endpoint edits or deletes an audit event. `src: Core features rule 41`
- [ ] `C-CF-181` `literal` Enquiries are kept for `24` months before deletion or anonymisation. `src: Technical requirements retention`
- [ ] `C-CF-182` `constraint` A client's deletion request never removes financial records or credit history. `src: Technical requirements retention`
- [ ] `C-CF-183` `literal` A refused publish names failed conditions with the tokens `clearance`, `case_study_permission`, `credits`, `embargo`. `src: Core features rule 24`
- [ ] `C-CF-184` `constraint` Publishing a campaign whose embargo has not lifted succeeds only as a scheduled publish. `src: Core features rule 24`
- [ ] `C-CF-185` `capability` Each rendering of the contact form fetches a fresh idempotency key. `src: Core features rule 35`
- [ ] `C-CF-186` `ui` The contact form submit control is disabled when a submission is in flight. `src: Core features rule 35`
- [ ] `C-CF-187` `constraint` Repeated submissions from one address slow down gradually rather than hitting a hard wall. `src: Core features rule 35`
- [ ] `C-CF-188` `constraint` The contact form never sends mail to an arbitrary address. `src: Core features rule 35`
- [ ] `C-CF-189` `ui` Contact form error messages exist in both languages. `src: Core features rule 35`
- [ ] `C-CF-190` `constraint` A contact form upload is checked by content, capped in size, handed out only through an authorising handler. `src: Core features rule 35`
- [ ] `C-CF-191` `literal` A `recruitment` enquiry routes to `careers@kuromeido.example.com`. `src: Core features rule 35`
- [ ] `C-CF-192` `literal` A `press` enquiry routes to `press@kuromeido.example.com`. `src: Core features rule 35`
- [ ] `C-CF-193` `capability` Contact form validation runs on the server. `src: Core features rule 35`
- [ ] `C-CF-194` `ui` Contact form validation is repeated in the browser. `src: Core features rule 35`
- [ ] `C-CF-195` `constraint` An expired preview link answers not-found. `src: Core features rule 26`
- [ ] `C-CF-196` `capability` A preview link expires after the minutes the link was created with. `src: Core features rule 26`
- [ ] `C-CF-197` `ui` Every public page footer links to the privacy page. `src: Core features rule 36`
- [ ] `C-CF-198` `ui` The privacy page carries numbered clauses with a table of contents deep-linking each clause. `src: Core features rule 36`
- [ ] `C-CF-199` `capability` The terms page, the privacy page exist in both languages. `src: Core features rule 36`
- [ ] `C-CF-200` `constraint` The sitemap never lists an unpublished or untranslated item. `src: Core features rule 39`
- [ ] `C-CF-201` `constraint` The robots file keeps `/studio` with `/preview/` out of indexing. `src: Core features rule 39`
- [ ] `C-CF-202` `capability` Placing a legal hold writes an audit event carrying the actor, the time, the reason. `src: Core features rule 15`
- [ ] `C-CF-203` `capability` A clearance grant or revocation writes an audit event. `src: Core features rule 41`
- [ ] `C-CF-204` `capability` A credit list change after publication writes an audit event with a reason. `src: Core features rule 41`
- [ ] `C-CF-205` `literal` Time entries are kept for `7` years before deletion or anonymisation. `src: Technical requirements retention`
- [ ] `C-CF-206` `literal` Work versions are kept for `5` years after the job closes. `src: Technical requirements retention`
- [ ] `C-CF-207` `literal` Audit events are kept for `10` years. `src: Technical requirements retention`
- [ ] `C-CF-208` `constraint` A refused part of a client deletion request says why rather than failing silently. `src: Technical requirements retention`
- [ ] `C-CF-209` `constraint` Altering an assignment on a job under legal hold is refused. `src: Core features rule 15`
- [ ] `C-CF-210` `constraint` Removing a comment on a job under legal hold is refused. `src: Core features rule 15`
- [ ] `C-CF-211` `capability` An adjusting entry sits in an open period, carrying the difference in cost. `src: Core features rule 7`
- [ ] `C-CF-212` `capability` Correcting a time entry in an open month updates the entry. `src: Core features rule 7`
- [ ] `C-CF-213` `role` A `producer` closes a calendar month. `src: Core features rule 7`
- [ ] `C-CF-214` `capability` A capacity refusal names the conflicting jobs when the producer reads every one of them. `src: Core features rule 8`
- [ ] `C-CF-215` `literal` The roles `Creative Director`, `Senior Creative Director` are different roles. `src: Core features rule 8`
- [ ] `C-CF-216` `constraint` A conversion without a pinned rate card is refused, creating no job. `src: Core features rule 4`
- [ ] `C-CF-217` `capability` The current rate card is the one with the latest effective start on or before today, range unended. `src: Core features rule 5`
- [ ] `C-CF-218` `literal` Hero films, stills are stored in `minio` at the key `campaigns/{campaign_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 9`
- [ ] `C-CF-219` `literal` An internal review status is one of `pending`, `approved`, `changes_requested`, `withdrawn`. `src: Core features rule 10`
- [ ] `C-CF-220` `literal` A client review status is one of `pending`, `approved`, `changes_requested`. `src: Core features rule 10`
- [ ] `C-CF-221` `literal` A right kind is one of `music`, `talent`, `imagery`, `claims`, `trademark`, `festival_exhibition`. `src: Core features rule 13`
- [ ] `C-CF-222` `capability` A restored version records the version number the restore came from. `src: Core features rule 12`
- [ ] `C-CF-223` `capability` An award entry fee is recorded as a third-party cost in yen on the campaign job. `src: Core features rule 22`
- [ ] `C-CF-224` `literal` An award entry status is one of `submitted`, `shortlisted`, `closed`. `src: Core features rule 22`
- [ ] `C-CF-225` `capability` Closing an award entry with no result sets the entry status to `closed`. `src: Core features rule 22`
- [ ] `C-CF-226` `capability` People already on a credit list, departed people included, stay on the list when the list is saved again. `src: Core features rule 17`
- [ ] `C-CF-227` `capability` A campaign published in only one language is listed in both languages with field-by-field fallback. `src: Core features rule 27`
- [ ] `C-CF-228` `constraint` Membership of a client-dedicated unit excludes the competitors of the unit's account. `src: Core features rule 3`
- [ ] `C-CF-229` `literal` The unit `Kagerou Studio` is dedicated to `kagerou-beverages`. `src: Core features rule 3`
- [ ] `C-CF-230` `capability` A departed person's record stays resolvable inside the studio. `src: Core features rule 19`
- [ ] `C-CF-231` `constraint` A departure cascades no deletion. `src: Core features rule 19`
- [ ] `C-CF-232` `constraint` A returning person moving between the rival car accounts serves the cooling-off period. `src: Core features rule 19`
- [ ] `C-CF-233` `literal` A translation status is one of `absent`, `drafted`, `in_translation`, `reviewed`, `published`. `src: Core features rule 27`
- [ ] `C-CF-234` `literal` The seeded campaign `Rice Field Radio`, published in Japanese only, is listed on the English work index. `src: Core features rule 27`
- [ ] `C-CF-235` `capability` Credit names fall back to the other locale name by name. `src: Core features rule 27`
- [ ] `C-CF-236` `constraint` A sentence is never finished in the other language. `src: Core features rule 27`
- [ ] `C-CF-237` `literal` The English client register lists `Aozora Airlines`, `Hoshino Motors`, `Kagerou Beverages`, `Minato Rail`, `Tsubame Automotive` in order. `src: Core features rule 29`
- [ ] `C-CF-238` `ui` Japanese dates render in the era-agnostic numeric form, such as `2025年6月21日`. `src: Core features rule 29`
- [ ] `C-CF-239` `literal` Searching the reading fragment `しんごう` finds `Night Signal`. `src: Core features rule 30`
- [ ] `C-CF-240` `capability` Public search finds a campaign by the English title. `src: Core features rule 30`
- [ ] `C-CF-241` `constraint` An embargoed article is absent from every public index before the embargo moment. `src: Core features rule 25`
- [ ] `C-CF-242` `constraint` An embargoed address never answers with a forbidden screen. `src: Core features rule 25`
- [ ] `C-CF-243` `literal` The seeded campaign `Harbour Lights` is scheduled for release ninety seconds after first start. `src: Core features rule 25`
- [ ] `C-CF-244` `literal` An opening on the `internship` track links to `https://careers.example.org/kuromeido/internships`. `src: Core features rule 34`
- [ ] `C-CF-245` `literal` The language switch note reads `That campaign is not yet available in English, so here is all of our work.` `src: Core features rule 28`
- [ ] `C-CF-246` `capability` A `producer` records a return, setting the record back to `active` with a weekly capacity of `2400` minutes. `src: Core features rule 19`
- [ ] `C-CF-247` `literal` An immediate publish of a campaign with an embargo moment still ahead is refused with the reason `embargo`. `src: Core features rule 24`
- [ ] `C-CF-248` `literal` A scheduled publish with a release moment after a right ends names the reason `rights_expire_before_release`. `src: Core features rule 24`
- [ ] `C-CF-249` `ui` A preview link opens at `/preview/<token>`. `src: Core features rule 26`
- [ ] `C-CF-250` `constraint` An address shaped like an old publishing platform endpoint such as `/wp-json/` answers the not-found status. `src: Core features rule 37`
- [ ] `C-CF-251` `ui` The not-found screen links back to the home page, to the work index. `src: Core features rule 37`
- [ ] `C-CF-252` `constraint` The not-found screen for a publishing-platform-shaped address never echoes that address. `src: Core features rule 37`
- [ ] `C-CF-253` `capability` The work index lists campaigns newest first. `src: Core features rule 31`
- [ ] `C-CF-254` `capability` Choosing a year on the work index resets to page one. `src: Core features rule 31`
- [ ] `C-CF-255` `capability` A page number that no longer exists after a change falls back to the last page that does. `src: Core features rule 31`
- [ ] `C-CF-256` `capability` The newsroom lists articles newest first. `src: Core features rule 33`
- [ ] `C-CF-257` `ui` An article shows its title, standfirst, date, category chips, a structured body. `src: Core features rule 33`
- [ ] `C-CF-258` `ui` An award article shows a per-campaign breakdown of body, category path, rank. `src: Core features rule 33`
- [ ] `C-CF-259` `capability` The page-view log lists rows newest first. `src: Core features rule 38`
- [ ] `C-CF-260` `literal` A new award entry has the status `submitted`. `src: Core features rule 22`
- [ ] `C-CF-261` `literal` Recording an unconfirmed result makes the entry `shortlisted`. `src: Core features rule 22`
- [ ] `C-CF-262` `literal` Confirming a result makes the entry `closed`. `src: Core features rule 22`
- [ ] `C-CF-263` `literal` Closing an entry with no result makes the entry `closed`. `src: Core features rule 22`
- [ ] `C-CF-264` `literal` `North Star Awards` awards `Gold`, `Silver`, `Bronze`, `Merit`. `src: Core features rule 21`
- [ ] `C-CF-265` `literal` The `Lotus Festival` `2025` itemised results are `Grand Lotus` 1, `Gold` 2, `Silver` 2, `Bronze` 2, `Jade Petal` 2. `src: Core features rule 23`
- [ ] `C-CF-266` `constraint` A shortlist is never shown as a win. `src: Core features rule 22`
- [ ] `C-CF-267` `ui` A fallback field's element carries a `lang` attribute matching the locale shown. `src: Core features rule 27`
- [ ] `C-CF-268` `ui` The campaign fact block shows the campaign's external site when one exists. `src: Core features rule 32`
- [ ] `C-CF-269` `ui` The campaign detail shows the campaign's hero film or still. `src: Core features rule 32`
- [ ] `C-CF-270` `ui` The campaign detail carries a share set. `src: Core features rule 32`
- [ ] `C-CF-271` `ui` A careers apply link opens in a new context. `src: Core features rule 34`
- [ ] `C-CF-272` `ui` The public footer is the page's footer landmark. `src: Core features rule 36`
- [ ] `C-CF-273` `constraint` An unpublished campaign's public address answers the not-found status. `src: Technical requirements para 1`

## C-UF User flow

- [ ] `C-UF-01` `capability` Every public route also exists under `/en/` with the same trailing slash. `src: User flow para 2`
- [ ] `C-UF-02` `ui` A persistent top navigation bar runs across every studio route. `src: User flow studio shape`
- [ ] `C-UF-03` `ui` Every studio list is a table with sortable column headers. `src: User flow studio shape`
- [ ] `C-UF-04` `ui` Opening a new brief is a three-step wizard, each step at its own address. `src: User flow studio shape`
- [ ] `C-UF-05` `ui` Going back in the new-brief wizard keeps what was typed. `src: User flow studio shape`
- [ ] `C-UF-06` `ui` A successful studio write confirms with a toast at the foot of the screen. `src: User flow studio shape`
- [ ] `C-UF-07` `ui` A refused studio write shows a toast carrying the reason, with an inline message beside the field involved. `src: User flow studio shape`
- [ ] `C-UF-08` `capability` A signed-out visitor opening a `/studio` address is sent to `/login`. `src: User flow entry and redirects`
- [ ] `C-UF-09` `capability` Signing in returns the visitor to the requested studio address. `src: User flow entry and redirects`
- [ ] `C-UF-10` `ui` A session expiring mid-action keeps the unsaved input on screen. `src: User flow entry and redirects`
- [ ] `C-UF-11` `ui` A walled job's studio address shows the same not-found screen as a missing job. `src: User flow entry and redirects`
- [ ] `C-UF-12` `ui` The work index filtered to an empty year offers a control that clears the filter. `src: User flow states`
- [ ] `C-UF-13` `literal` The empty work index says `No campaigns in that year yet. Clear the filter to see everything.` `src: User flow states`
- [ ] `C-UF-14` `literal` The empty newsroom says `No articles match those filters.` `src: User flow states`
- [ ] `C-UF-15` `literal` The empty studio desk says `Nothing is waiting for your approval.` `src: User flow table`
- [ ] `C-UF-16` `ui` Loading views show skeletons in the final layout's shape. `src: User flow states`
- [ ] `C-UF-17` `literal` A studio save that fails says `That did not save. Your work is still here, so try again.` `src: User flow states`
- [ ] `C-UF-18` `ui` Offline, public pages already fetched stay readable. `src: User flow states`
- [ ] `C-UF-19` `ui` The editor publishes `Paper Lanterns` from `/studio/publishing`, seeing a toast. `src: User flow the editor`
- [ ] `C-UF-20` `ui` The account director walks the three wizard steps for `kagerou-beverages`. `src: User flow the account director`
- [ ] `C-UF-21` `ui` The visitor copies a campaign link, seeing the copy confirmed. `src: User flow the visitor`
- [ ] `C-UF-22` `literal` The new-brief wizard steps sit at `/studio/briefs/new/1`, `/studio/briefs/new/2`, `/studio/briefs/new/3`. `src: User flow table`
- [ ] `C-UF-23` `literal` The studio navigation reads `Desk`, `Accounts`, `Briefs`, `Jobs`, `Clearance`, `People`, `Rate cards`, `Awards`, `Publishing`, `Reports`. `src: User flow studio shape`
- [ ] `C-UF-24` `capability` Signing in without a destination lands on `/studio`. `src: User flow entry and redirects`
- [ ] `C-UF-25` `capability` Signing out returns to `/login`. `src: User flow entry and redirects`
- [ ] `C-UF-26` `ui` A session ending mid-action shows a toast saying the session ended. `src: User flow entry and redirects`
- [ ] `C-UF-27` `ui` A role that cannot write sees a studio page without the controls the role cannot use. `src: User flow entry and redirects`
- [ ] `C-UF-28` `ui` `/studio/briefs/<id>` shows one brief with its estimates, approval, conversion. `src: User flow route table`
- [ ] `C-UF-29` `ui` Step one of the new-brief wizard captures the title, picks the accounts with the markets. `src: User flow studio shape`
- [ ] `C-UF-30` `ui` `/preview/<token>` shows one unpublished or embargoed campaign to a holder of a live preview link. `src: User flow route table`
- [ ] `C-UF-31` `ui` A failed load says what failed, offers a retry, never shows a bare code. `src: User flow states`
- [ ] `C-UF-32` `ui` Offline, the studio says the last action did not save. `src: User flow states`
- [ ] `C-UF-33` `ui` Offline, the studio keeps the unsaved action rather than discarding the action. `src: User flow states`
- [ ] `C-UF-34` `ui` Errors never crash the app. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public site ground is a near-black neutral. `src: UI/UX notes palette public site`
- [ ] `C-UX-02` `ui` Public type on the ground is a near-white neutral. `src: UI/UX notes palette public site`
- [ ] `C-UX-03` `ui` A single acid yellow accent, leaning green, never orange (a mid, vivid amber), marks the diagonal rules, active states, highlights. `src: UI/UX notes palette public site`
- [ ] `C-UX-04` `ui` A mid, vivid red appears only on errors. `src: UI/UX notes palette public site`
- [ ] `C-UX-05` `ui` Studio screens reserve the amber for the one primary action on each screen. `src: UI/UX notes palette studio`
- [ ] `C-UX-06` `literal` Japanese copy is set in `Noto Sans JP`. `src: UI/UX notes type`
- [ ] `C-UX-07` `literal` The Latin display register is set in `Archivo` in wide-tracked capitals. `src: UI/UX notes type`
- [ ] `C-UX-08` `ui` Japanese with Latin never share one display line. `src: UI/UX notes type`
- [ ] `C-UX-09` `ui` Marquee lines are letterspaced until a phrase reads as texture from across the room. `src: UI/UX notes type`
- [ ] `C-UX-10` `literal` The full-bleed display type is set at `160px`. `src: UI/UX notes type`
- [ ] `C-UX-11` `ui` Studio figures use tabular numerals where amounts stack. `src: UI/UX notes type`
- [ ] `C-UX-12` `ui` The public site carries no rounded corners, no soft shadows, no centred column. `src: UI/UX notes shape and depth`
- [ ] `C-UX-13` `ui` Public motion is eased, never a bounce. `src: UI/UX notes motion`
- [ ] `C-UX-14` `ui` Stillness is the default under a reduced-motion preference. `src: UI/UX notes motion`
- [ ] `C-UX-15` `ui` The layout holds every width from a phone upward with no sideways scrolling. `src: UI/UX notes responsive`
- [ ] `C-UX-16` `ui` Hover effects fire only for a fine pointer that can hover. `src: UI/UX notes responsive`
- [ ] `C-UX-17` `ui` On a phone the floating menu never covers a form field. `src: UI/UX notes responsive`
- [ ] `C-UX-18` `ui` Body text meets the WCAG AA contrast ratio on every public route. `src: UI/UX notes accessibility`
- [ ] `C-UX-19` `ui` Focus is visible on every interactive element against the black ground. `src: UI/UX notes accessibility`
- [ ] `C-UX-20` `ui` Keyboard navigation reaches every control. `src: UI/UX notes accessibility`
- [ ] `C-UX-21` `ui` Studio status is carried by words beside colour, never by colour alone. `src: UI/UX notes palette studio`
- [ ] `C-UX-22` `ui` Studio status words carry a green for approved, cleared, published states. `src: UI/UX notes palette studio`
- [ ] `C-UX-23` `ui` Studio status words carry an orange for pending, changes requested, scheduled states. `src: UI/UX notes palette studio`
- [ ] `C-UX-24` `ui` The studio primary action brightens slightly under the pointer. `src: UI/UX notes palette studio`
- [ ] `C-UX-25` `ui` Destructive studio actions ask for confirmation before running. `src: UI/UX notes palette studio`
- [ ] `C-UX-26` `literal` Section heads are set at `56px`. `src: UI/UX notes type`
- [ ] `C-UX-27` `literal` Card titles are set at `24px`. `src: UI/UX notes type`
- [ ] `C-UX-28` `literal` Body text is set at `16px`. `src: UI/UX notes type`
- [ ] `C-UX-29` `literal` The micro label is set at `11px`. `src: UI/UX notes type`
- [ ] `C-UX-30` `literal` Studio body text is set at `14px`, with table figures at `13px`. `src: UI/UX notes type`
- [ ] `C-UX-31` `literal` Body text contrast reaches at least `4.5:1`. `src: UI/UX notes accessibility`
- [ ] `C-UX-32` `ui` The product is dark only, with no light theme. `src: UI/UX notes mode`
- [ ] `C-UX-33` `ui` Touch targets are at least `44` by `44` pixels. `src: UI/UX notes accessibility`
- [ ] `C-UX-34` `ui` The display type scales down with the window to stay full-bleed at every width. `src: UI/UX notes type`
- [ ] `C-UX-35` `ui` The type steps below the display hold their desktop sizes on a narrower window. `src: UI/UX notes type`
- [ ] `C-UX-36` `ui` Focus order follows reading order despite the layered motion. `src: UI/UX notes accessibility`
- [ ] `C-UX-37` `ui` Icon-only controls carry labels. `src: UI/UX notes accessibility`
- [ ] `C-UX-38` `ui` Studio tables scroll inside their own frame on a narrow viewport. `src: UI/UX notes responsive`
- [ ] `C-UX-39` `ui` On a phone the floating menu never covers a form field or a video control. `src: UI/UX notes responsive`
- [ ] `C-UX-40` `ui` The studio has no oversized heroes. `src: UI/UX notes north star`
- [ ] `C-UX-41` `literal` The Japanese face is known in the style layer as `notosansjp`. `src: UI/UX notes type`
- [ ] `C-UX-42` `ui` The studio primary action brightens slightly on focus. `src: UI/UX notes palette studio`
- [ ] `C-UX-43` `ui` The studio's only motion is the toast's arrival with its exit. `src: UI/UX notes motion`
- [ ] `C-UX-44` `ui` Destructive confirmation cancels on Escape. `src: UI/UX notes palette studio`
- [ ] `C-UX-45` `ui` Public pages never carry meaning by colour alone. `src: UI/UX notes accessibility`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The overlay sits above the floating control that opens the overlay. `src: Front-end specification layering`
- [ ] `C-FE-02` `ui` The consent banner is never trapped beneath the overlay. `src: Front-end specification layering`
- [ ] `C-FE-03` `ui` The seal is drawn geometry at three sizes. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-04` `ui` The lockup is live text in the Latin grotesk with wide tracking. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-05` `ui` A black floating menu pill with a clipped corner sits at the foot of every public page. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-06` `ui` The pirate flag is a drawn mark, never an emoji. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-07` `ui` Category chips are text, never icons. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-08` `ui` A split heading keeps the unsplit string as the parent's accessible name. `src: Front-end specification split text`
- [ ] `C-FE-09` `ui` Under reduced motion split text renders plain. `src: Front-end specification split text`
- [ ] `C-FE-10` `ui` Japanese text splits per character, never on whitespace. `src: Front-end specification split text`
- [ ] `C-FE-11` `ui` The menu overlay lists eight destinations with the language pair. `src: Front-end specification global chrome`
- [ ] `C-FE-12` `ui` The menu overlay traps focus, returning focus to the pill on close. `src: Front-end specification global chrome`
- [ ] `C-FE-13` `ui` The menu overlay closes on escape, closes on choosing a destination. `src: Front-end specification global chrome`
- [ ] `C-FE-14` `ui` The page behind the open menu overlay is inert. `src: Front-end specification global chrome`
- [ ] `C-FE-15` `ui` The current language code is marked as current rather than linked. `src: Front-end specification global chrome`
- [ ] `C-FE-16` `ui` The footer marquee carries the office line, the coordinates, the founding year, the pirate line. `src: Front-end specification global chrome`
- [ ] `C-FE-17` `ui` Each marquee band loops with no visible seam at any window width. `src: Front-end specification marquee system`
- [ ] `C-FE-18` `ui` Marquee reading pace stays the same on a wider window. `src: Front-end specification marquee system`
- [ ] `C-FE-19` `ui` Scrolling accelerates the marquee bands, scrolling up reverses them, then the bands settle to their own speed. `src: Front-end specification marquee system`
- [ ] `C-FE-20` `ui` Marquee bands pause off-screen. `src: Front-end specification marquee system`
- [ ] `C-FE-21` `ui` Under reduced motion marquee bands render as static letterspaced lines. `src: Front-end specification marquee system`
- [ ] `C-FE-22` `literal` The home hero answers `rupture is not destruction.` with `RUPTURE IS CREATION.` `src: Front-end specification home`
- [ ] `C-FE-23` `literal` The home statement band reads `CREATE. INVENT. HAVE IDEAS.` `src: Front-end specification home`
- [ ] `C-FE-24` `ui` The home work carousel advances with a numbered index under keyboard control. `src: Front-end specification home`
- [ ] `C-FE-25` `literal` The home closing marquee ends on `READY TO BREAK SOMETHING`. `src: Front-end specification home`
- [ ] `C-FE-26` `ui` The methodology diagram nodes are reachable by keyboard. `src: Front-end specification methodology`
- [ ] `C-FE-27` `ui` The methodology name carries a superscript registered-trademark sign. `src: Front-end specification methodology`
- [ ] `C-FE-28` `ui` The work index odometer lands on the real total without moving the layout. `src: Front-end specification work index`
- [ ] `C-FE-29` `ui` Campaign stills scale under the scrim on hover for fine pointers only. `src: Front-end specification work index`
- [ ] `C-FE-30` `literal` The careers culture statement reads `WHY JOIN THE NAVY WHEN YOU CAN BE A PIRATE`. `src: Front-end specification careers`
- [ ] `C-FE-31` `ui` The careers page shows five value cards, each with an English phrase over a Japanese rendering. `src: Front-end specification careers`
- [ ] `C-FE-32` `ui` The careers recruitment film carries captions. `src: Front-end specification careers`
- [ ] `C-FE-33` `literal` The fallback notice copy reads `The page is not yet available in English; showing the Japanese original.` `src: Front-end specification copy deck`
- [ ] `C-FE-34` `ui` The client wordmark wall shows invented wordmarks, never a real company's mark. `src: Front-end specification generating every asset`
- [ ] `C-FE-35` `ui` The liquid gradient renders as a single still frame under reduced motion. `src: Front-end specification generating every asset`
- [ ] `C-FE-36` `constraint` The build ships no binary asset copied from another site. `src: Front-end specification generating every asset`
- [ ] `C-FE-37` `capability` The company record carries the legal name `KURO\MEIDO Inc.` `src: Front-end specification company`
- [ ] `C-FE-38` `capability` The careers openings carry the `new_graduate` track with an external apply address. `src: Front-end specification careers`
- [ ] `C-FE-39` `literal` The consent line reads `I have read the privacy policy, which I accept.` `src: Front-end specification copy deck`
- [ ] `C-FE-40` `literal` The floating menu pill is labelled `MENU`. `src: Front-end specification global chrome`
- [ ] `C-FE-41` `literal` The menu overlay close control is labelled `Close menu`. `src: Front-end specification global chrome`
- [ ] `C-FE-42` `literal` The consent banner names the categories `Necessary`, `Analytics`, `Marketing`. `src: Front-end specification global chrome`
- [ ] `C-FE-43` `literal` The footer copyright reads `(c) KURO\MEIDO Inc.` `src: Front-end specification global chrome`
- [ ] `C-FE-44` `literal` The company record carries the last-updated date `2026-04-01`. `src: Front-end specification company`
- [ ] `C-FE-45` `literal` The company record carries the telephone `+81-3-5555-0100`. `src: Front-end specification company`
- [ ] `C-FE-46` `literal` The company record lists `Kaito Mizuno` first as `President & CEO`. `src: Front-end specification company`
- [ ] `C-FE-47` `literal` The careers value cards include `CREATIVITY COMES FROM DIVERSITY`. `src: Front-end specification careers`
- [ ] `C-FE-48` `literal` The company record carries the founding date `1 April 2006`. `src: Front-end specification company`
- [ ] `C-FE-49` `ui` The home hero sets the lowercase premise above a capitalised answer spanning the full window width. `src: Front-end specification home`
- [ ] `C-FE-50` `literal` The home hero shows `EST. 2006`, `TOKYO`, `35.6581 N 139.7561 E` in the micro register. `src: Front-end specification home`
- [ ] `C-FE-51` `literal` The home positioning copy opens `We use creativity to move business`. `src: Front-end specification home`
- [ ] `C-FE-52` `literal` The closing marquee carries `We are the method company.` `src: Front-end specification home`
- [ ] `C-FE-53` `ui` The home composition runs hero, positioning, statement band, work carousel, who we are, partners, news, closing marquee, in that order. `src: Front-end specification home`
- [ ] `C-FE-54` `ui` A banner strip above the home composition links to the current headline article. `src: Front-end specification home`
- [ ] `C-FE-55` `ui` The not-found numerals turn in three dimensions. `src: UI/UX notes motion`
- [ ] `C-FE-56` `ui` The menu overlay wipes in, wipes back out in reverse. `src: UI/UX notes motion`
- [ ] `C-FE-57` `ui` Display words rise with a fade, staggered, on the long settle. `src: UI/UX notes motion`
- [ ] `C-FE-58` `ui` Under reduced motion the carousel changes instantly. `src: Front-end specification marquee system`
- [ ] `C-FE-59` `ui` Under reduced motion the not-found numerals are still. `src: Front-end specification marquee system`
- [ ] `C-FE-60` `ui` Under reduced motion no film plays by itself. `src: Front-end specification marquee system`
- [ ] `C-FE-61` `ui` Under reduced motion display reveals are plain. `src: Front-end specification marquee system`
- [ ] `C-FE-62` `ui` The footer carries a back-to-top control. `src: Front-end specification global chrome`
- [ ] `C-FE-63` `ui` Campaign stills open in a lightbox. `src: Front-end specification global chrome`
- [ ] `C-FE-64` `literal` The company record address reads postal code `104-0061`, then `Kaigan Tower 14F, 1-2-3 Kaigan, Chuo-ku, Tokyo`. `src: Front-end specification company`
- [ ] `C-FE-65` `literal` The company record lists the auditor `Masato Ide`, `Auditor`, concurrently `Audit Partner, Meido Group`. `src: Front-end specification company`
- [ ] `C-FE-66` `literal` The officers run `Kaito Mizuno`, `Emi Hayashi`, `Ren Shibata`, `Hiroshi Kudo`, `Laura Chen`, in that order. `src: Front-end specification company`
- [ ] `C-FE-67` `literal` `Laura Chen` is `Non-executive Director`, concurrently `Regional President, KURO Worldwide`. `src: Front-end specification company`
- [ ] `C-FE-68` `literal` The opening `Creative, new graduates 2027` applies at `https://careers.example.org/kuromeido/new-graduates`. `src: Front-end specification careers`
- [ ] `C-FE-69` `literal` The opening `Summer internship 2027` sits on the `internship` track. `src: Front-end specification careers`
- [ ] `C-FE-70` `ui` The careers page opens with a positions control jumping to the openings. `src: Front-end specification careers`
- [ ] `C-FE-71` `ui` Marquee bands pause during a hidden tab. `src: Front-end specification marquee system`
- [ ] `C-FE-72` `ui` Award-body names are text, never icons. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-73` `ui` The menu overlay carries the social links. `src: Front-end specification global chrome`
- [ ] `C-FE-74` `ui` A sticky new-work chip above the footer promotes the latest campaign. `src: Front-end specification global chrome`
- [ ] `C-FE-75` `ui` Work index cards reveal on scroll. `src: Front-end specification work index`
- [ ] `C-FE-76` `ui` The campaign detail opens with a back-to-index control. `src: Front-end specification work index`
- [ ] `C-FE-77` `ui` The campaign detail title is split per character at display size. `src: Front-end specification work index`
- [ ] `C-FE-78` `literal` The who-we-are columns date the methodology's continuous use from `1992`. `src: Front-end specification home`
- [ ] `C-FE-79` `ui` The company page runs the office identity band, the positioning lines, the methodology statement, the company narrative set per character, the formal record, in that order. `src: Front-end specification company`
- [ ] `C-FE-80` `literal` The careers pirate line carries the Japanese half `海軍に入るな、海賊になれ。`. `src: Front-end specification careers`
- [ ] `C-FE-81` `literal` A careers value card carries the phrase `BE A PIRATE`. `src: Front-end specification careers`
- [ ] `C-FE-82` `literal` The careers value `BE A PIRATE` carries the Japanese rendering `海賊であれ`. `src: Front-end specification careers`
- [ ] `C-FE-83` `literal` The careers value `CREATIVITY COMES FROM DIVERSITY` carries the Japanese rendering `多様性が創造性を生む`. `src: Front-end specification careers`
- [ ] `C-FE-84` `literal` A careers value card carries the phrase `UNCOMMON HUMANITY`. `src: Front-end specification careers`
- [ ] `C-FE-85` `literal` The careers value `UNCOMMON HUMANITY` carries the Japanese rendering `並外れた人間らしさ`. `src: Front-end specification careers`
- [ ] `C-FE-86` `literal` A careers value card carries the phrase `GOOD ENOUGH IS NOT ENOUGH`. `src: Front-end specification careers`
- [ ] `C-FE-87` `literal` The careers value `GOOD ENOUGH IS NOT ENOUGH` carries the Japanese rendering `十分では足りない`. `src: Front-end specification careers`
- [ ] `C-FE-88` `literal` A careers value card carries the phrase `BE BRAVE`. `src: Front-end specification careers`
- [ ] `C-FE-89` `literal` The careers value `BE BRAVE` carries the Japanese rendering `勇敢であれ`. `src: Front-end specification careers`
- [ ] `C-FE-90` `ui` The third careers value's paragraph describes serving colleagues. `src: Front-end specification careers`
- [ ] `C-FE-91` `ui` The careers page lists the internal with the social-contribution programmes before the openings. `src: Front-end specification careers`
- [ ] `C-FE-92` `ui` The sustainability page states the agency's position on using its work for social change. `src: Front-end specification sustainability`
- [ ] `C-FE-93` `ui` The sustainability page lists the agency's programmes. `src: Front-end specification sustainability`
- [ ] `C-FE-94` `ui` The sustainability page lists the agency's commitments. `src: Front-end specification sustainability`
- [ ] `C-FE-95` `ui` Split text stays selectable. `src: Front-end specification split text`
- [ ] `C-FE-96` `ui` Split text stays findable with the browser's find. `src: Front-end specification split text`
- [ ] `C-FE-97` `ui` Split text stays translatable. `src: Front-end specification split text`
- [ ] `C-FE-98` `ui` Page titles split into single Latin letters. `src: Front-end specification split text`
- [ ] `C-FE-99` `ui` Body paragraphs split into single kana or kanji. `src: Front-end specification split text`
- [ ] `C-FE-100` `ui` The hatched block of repeating diagonal stripes serves as a spacer. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-101` `ui` The backslash appears alone at display size as a graphic. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-102` `ui` The smallest seal drops the founding line. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-103` `ui` Interface glyphs are a thin stroke set inheriting text colour. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-104` `ui` The client wordmark wall sits at reduced strength, brightening on hover. `src: Front-end specification generating every asset`
- [ ] `C-FE-105` `ui` The favicon with the social images are generated from the seal with the lockup. `src: Front-end specification generating every asset`
- [ ] `C-FE-106` `ui` `Noto Sans JP` loads as a variable face. `src: UI/UX notes type`
- [ ] `C-FE-107` `ui` `Archivo` is set at its widest width. `src: UI/UX notes type`
- [ ] `C-FE-108` `ui` `Noto Color Emoji` serves as a fallback face only. `src: UI/UX notes type`
- [ ] `C-FE-109` `ui` The liquid gradient flows. `src: UI/UX notes motion`
- [ ] `C-FE-110` `ui` The new-work chip slides in past a scroll threshold. `src: UI/UX notes motion`
- [ ] `C-FE-111` `ui` Marquee bands scroll at different speeds. `src: Front-end specification marquee system`
- [ ] `C-FE-112` `ui` Marquee bands scroll in opposite directions. `src: Front-end specification marquee system`
- [ ] `C-FE-113` `ui` The home work carousel is draggable. `src: Front-end specification home`
- [ ] `C-FE-114` `ui` Home carousel cards carry client, title, a one-line description, category chips. `src: Front-end specification home`
- [ ] `C-FE-115` `ui` The home news section shows the latest articles with date, category chip, title. `src: Front-end specification home`
- [ ] `C-FE-116` `ui` The careers film sits behind a poster frame with a play control. `src: Front-end specification careers`
- [ ] `C-FE-117` `ui` The careers play control opens a dialog explaining the local placeholder film. `src: Front-end specification careers`
- [ ] `C-FE-118` `ui` The footer holds three link columns: content, utility, social. `src: Front-end specification global chrome`
- [ ] `C-FE-119` `ui` The methodology page opens with a philosophy statement. `src: Front-end specification methodology`
- [ ] `C-FE-120` `ui` The methodology terms appear as a running statement. `src: Front-end specification methodology`
- [ ] `C-FE-121` `ui` The methodology diagram is drawn as geometry. `src: Front-end specification methodology`
- [ ] `C-FE-122` `ui` Each methodology diagram node carries its description as accessible text. `src: Front-end specification methodology`
- [ ] `C-FE-123` `literal` The methodology steps are `Convention`, `Vision`, `Method`. `src: Front-end specification methodology`
- [ ] `C-FE-124` `literal` The methodology is named `Rupture`. `src: Front-end specification methodology`
- [ ] `C-FE-125` `literal` The menu overlay destinations are `WORK`, `NEWS`, `METHODOLOGY`, `COMPANY`, `CAREERS`, `SUSTAINABILITY`, `CONTACT`, `HOME`. `src: Front-end specification global chrome`
- [ ] `C-FE-126` `literal` The language pair reads `JA`, `EN`. `src: Front-end specification global chrome`
- [ ] `C-FE-127` `literal` Category chips include `creative`, `innovation`. `src: Front-end specification surfaces and marks`
- [ ] `C-FE-128` `literal` `Emi Hayashi` is `Chief Operating Officer`. `src: Front-end specification company`
- [ ] `C-FE-129` `literal` `Ren Shibata` is `Chief Creative Officer`. `src: Front-end specification company`
- [ ] `C-FE-130` `literal` `Hiroshi Kudo` holds the concurrent position `Executive Officer, Meido Group`. `src: Front-end specification company`
- [ ] `C-FE-131` `literal` The units are `Planning`, `Media Experience Design`, `Corporate Strategy`, `Finance`, `Executive Management`, `Hoshino Unit`, `Kagerou Studio`, `Rupture Lab`, `Integrated Business Leadership`, `Minato Media Partners`. `src: Front-end specification company`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The front end is a `SolidJS` application built with `Vite`. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The backend is `Express`, serving the JSON API under `/api`. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The server answers an embargoed campaign address with a real `404` status. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The server serves `/sitemap.xml` with `/robots.txt` itself. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` Records live in `PostgreSQL` at `DATABASE_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-06` `contract` Uploaded bytes live in `minio` at `STORAGE_ENDPOINT`. `src: Technical requirements para 2`
- [ ] `C-TR-07` `contract` The bucket name comes from `STORAGE_BUCKET`. `src: Technical requirements para 2`
- [ ] `C-TR-08` `contract` The object store key pair comes from `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY`. `src: Technical requirements para 2`
- [ ] `C-TR-09` `contract` Passwords are stored hashed. `src: Technical requirements para 2`
- [ ] `C-TR-10` `contract` A successful login returns a bearer token as `access_token`. `src: Technical requirements para 2`
- [ ] `C-TR-11` `constraint` The role is read from the stored account, never from a request. `src: Technical requirements para 2`
- [ ] `C-TR-12` `contract` Each request writes one structured line to stdout. `src: Technical requirements para 2`
- [ ] `C-TR-13` `constraint` The app introduces no second database, cache, queue, object store, identity provider or mail vendor. `src: Technical requirements para 3`
- [ ] `C-TR-14` `capability` Changing one underlying record moves every surface showing the record on the next read. `src: Technical requirements authority principle`
- [ ] `C-TR-15` `capability` The burn report is computed over the viewer's readable jobs only. `src: Technical requirements aggregates`
- [ ] `C-TR-16` `literal` A partial aggregate sets `partial` to true. `src: Technical requirements aggregates`
- [ ] `C-TR-17` `capability` Embargo release happens at the embargo moment with nobody present. `src: Technical requirements time-based transitions`
- [ ] `C-TR-18` `capability` Every mutating endpoint is safe to retry. `src: Technical requirements conflicting saves`
- [ ] `C-TR-19` `contract` Every response carries a content-type options header refusing to sniff. `src: Technical requirements security headers`
- [ ] `C-TR-20` `contract` Every response carries a frame-ancestors restriction. `src: Technical requirements security headers`
- [ ] `C-TR-21` `contract` Every response carries a content security policy. `src: Technical requirements security headers`
- [ ] `C-TR-22` `literal` Preview link responses carry `X-Robots-Tag: noindex`. `src: Technical requirements security headers`
- [ ] `C-TR-23` `constraint` No script the browser downloads carries a secret. `src: Technical requirements secrets`
- [ ] `C-TR-24` `constraint` The Japanese face is split by character range for Latin-only pages. `src: Technical requirements performance`
- [ ] `C-TR-25` `constraint` Identifiers are opaque, never sequential. `src: Technical requirements identifiers`
- [ ] `C-TR-26` `constraint` The running app calls nothing outside the environment. `src: Technical requirements no external calls`
- [ ] `C-TR-27` `constraint` The product stays responsive with a few thousand page views. `src: Technical requirements volume`
- [ ] `C-TR-28` `constraint` A signed link the app issues never outlives the clearance or preview link that granted the link. `src: Technical requirements retention`
- [ ] `C-TR-29` `contract` Login tokens expire. `src: Technical requirements para 2`
- [ ] `C-TR-30` `contract` Sessions rotate when a privilege changes. `src: Technical requirements para 2`
- [ ] `C-TR-31` `contract` Every response carries a referrer policy. `src: Technical requirements security headers`
- [ ] `C-TR-32` `contract` Every mutating form carries cross-site request forgery protection. `src: Technical requirements security headers`
- [ ] `C-TR-33` `literal` Uploads are capped at `200` megabytes. `src: Technical requirements uploads`
- [ ] `C-TR-34` `constraint` Request log lines carry no personal data, no identifier of walled material. `src: Technical requirements para 2`
- [ ] `C-TR-35` `capability` A failed time-based transition is written to the log as an error. `src: Technical requirements time-based transitions`
- [ ] `C-TR-36` `capability` Rights expiry happens at the right's end with nobody present. `src: Technical requirements time-based transitions`
- [ ] `C-TR-37` `constraint` The largest content paints within two-and-a-half seconds on a mid-range phone. `src: Technical requirements performance`
- [ ] `C-TR-38` `capability` Backups are proved by restoring one. `src: Technical requirements operations`
- [ ] `C-TR-39` `constraint` Schema changes run forward-only, refusing any rewrite of historical cost or credit records. `src: Technical requirements operations`
- [ ] `C-TR-40` `data` Every stored record carries a schema version. `src: Technical requirements operations`
- [ ] `C-TR-41` `contract` Hosts, ports, keys, passwords come from environment variables, never from the code. `src: Technical requirements para 3`
- [ ] `C-TR-42` `capability` A bearer token expires `8` hours after issue. `src: Technical requirements auth`
- [ ] `C-TR-43` `capability` Interactions respond within two hundred milliseconds. `src: Technical requirements performance`
- [ ] `C-TR-44` `capability` Cumulative layout shift stays under one tenth. `src: Technical requirements performance`
- [ ] `C-TR-45` `capability` Scroll animation holds sixty frames a second on mid-range hardware. `src: Technical requirements performance`
- [ ] `C-TR-46` `capability` The largest content paints within the two-and-a-half-second budget on a throttled mid-range phone. `src: Technical requirements performance`
- [ ] `C-TR-47` `capability` The hero renders before films or below-fold images finish loading. `src: Technical requirements performance`
- [ ] `C-TR-48` `capability` Content images declare their dimensions. `src: Technical requirements performance`
- [ ] `C-TR-49` `capability` Below-fold media is deferred. `src: Technical requirements performance`

## C-DM Data model

- [ ] `C-DM-01` `data` The table `users` stores an `email` unique without regard to case. `src: Data model users`
- [ ] `C-DM-02` `data` The table `users` stores the `role` of each account. `src: Data model users`
- [ ] `C-DM-03` `data` The table `clients` stores a unique `slug`. `src: Data model clients`
- [ ] `C-DM-04` `data` The table `campaigns` stores a unique `slug`. `src: Data model campaigns`
- [ ] `C-DM-05` `data` The table `enquiries` stores a unique `idempotency_key`. `src: Data model enquiries`
- [ ] `C-DM-06` `data` The table `page_views` stores the `route` of each view. `src: Data model page_views`
- [ ] `C-DM-07` `data` The table `work_versions` stores the `object_key` of each version. `src: Data model work_versions`
- [ ] `C-DM-08` `data` The table `audit_events` stores the `action` of each event. `src: Data model audit_events`
- [ ] `C-DM-09` `data` Translations are stored per field, never per item. `src: Data model translations`
- [ ] `C-DM-10` `data` An award entry is unique on campaign, body, category, year. `src: Data model award_entries`
- [ ] `C-DM-11` `data` A job stores the pinned rate card version. `src: Data model jobs`
- [ ] `C-DM-12` `constraint` A refused write leaves no row, no partial row, no object. `src: Data model invariants`
- [ ] `C-DM-13` `literal` The seeded clients carry the slugs `hoshino-motors`, `tsubame-automotive`, `kagerou-beverages`, `aozora-airlines`, `minato-rail`. `src: Data model clients table`
- [ ] `C-DM-14` `literal` The client `hoshino-motors` competes with `tsubame-automotive`. `src: Data model clients table`
- [ ] `C-DM-15` `literal` Every active person has a weekly capacity of `2400` minutes. `src: Data model seed data`
- [ ] `C-DM-16` `literal` The card `RC-2026` rates `Art Director` at `12000` yen per hour. `src: Data model rate cards table`
- [ ] `C-DM-17` `literal` Thirty seeded campaigns are public, each in the markets `JP`, `US` except `tide-clock` in `JP`, `DE`. `src: Data model campaigns table`
- [ ] `C-DM-18` `capability` The seeded `night-signal` also holds one shortlisted, unconfirmed entry. `src: Data model award results`
- [ ] `C-DM-19` `literal` The article `lotus-festival-2025-results` reports `Lotus Festival` for `2025`. `src: Data model articles`
- [ ] `C-DM-20` `literal` The credited person `Shun Kaneda` departed on `2026-02-27`. `src: Data model credit list`
- [ ] `C-DM-21` `literal` The campaign `paper-lanterns` is a draft with every gate condition met. `src: Data model further campaigns`
- [ ] `C-DM-22` `literal` The campaign `winter-kite` has translations published in neither language. `src: Data model further campaigns`
- [ ] `C-DM-23` `capability` Seeding is idempotent, so a restart duplicates no row. `src: Data model seed data`
- [ ] `C-DM-24` `literal` The seeded card `RC-2025` runs from `2025-01-01` to `2025-12-31`. `src: Data model rate cards`
- [ ] `C-DM-25` `literal` Seeded assignments on the open jobs run from `2026-01-05` to `2026-12-27` at `1200` minutes per week. `src: Data model seed data`
- [ ] `C-DM-26` `capability` At first start the work index lists thirty campaigns in both languages. `src: Data model further campaigns`
- [ ] `C-DM-27` `literal` The campaign `paper-lanterns` carries case-study permission `PERM-PAPER-LANTERNS`. `src: Data model further campaigns`
- [ ] `C-DM-28` `literal` The seeded job `Sky Tea Partnership` has the producer `Kenji Mori`. `src: Data model seed data`
- [ ] `C-DM-29` `literal` A brief's status is `open` or `converted`. `src: Data model tables`
- [ ] `C-DM-30` `literal` A job's status is `open` or `closed`. `src: Data model tables`
- [ ] `C-DM-31` `literal` `harbour-lights` sits on its own `minato-rail` job with case-study permission `PERM-HARBOUR-LIGHTS`. `src: Data model further campaigns`
- [ ] `C-DM-32` `literal` The `harbour-lights` credit list holds one entry, `Producer` Kenji Mori. `src: Data model further campaigns`
- [ ] `C-DM-33` `literal` After the release of `harbour-lights` the work index lists thirty-one campaigns. `src: Data model further campaigns`
- [ ] `C-DM-34` `literal` The seed holds twenty published articles, none tagged `stories` dated `2019`. `src: Data model articles`
- [ ] `C-DM-35` `literal` `night-signal` carries the Japanese reading `よるのしんごう`. `src: Data model public campaigns`
- [ ] `C-DM-36` `literal` The `night-signal` credit list opens `Chief Creative Officer` Ren Shibata, then `Head of Innovation` Takumi Aoki. `src: Data model credit list`
- [ ] `C-DM-37` `literal` The thirteen active people credited on `night-signal` hold `kagerou-beverages` clearances. `src: Data model people`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product has no second tenant. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` A client sees work through preview links only. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The product offers no password reset by mail. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The consent banner is the app's own, with no consent-platform vendor. `src: Constraints bullet 7`
- [ ] `C-CN-05` `constraint` The product carries no applicant tracking integration beyond an outbound apply link. `src: Constraints bullet 8`
- [ ] `C-CN-06` `capability` The indexes stay correct at hundreds of campaigns, hundreds of articles. `src: Constraints bullet 11`
- [ ] `C-CN-07` `constraint` The product stays responsive with a few thousand time entries. `src: Technical requirements volume`
- [ ] `C-CN-08` `constraint` The product offers no single sign-on. `src: Constraints bullet 3`
- [ ] `C-CN-09` `constraint` Costs are recorded, never charged. `src: Constraints bullet 5`
- [ ] `C-CN-10` `constraint` The product sends no notification of any kind. `src: Constraints no notifications`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under `/api`. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist empty at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` A production build is served, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `contract` The app uses the already running backing services, never starting a copy. `src: Deployment contract bullet 10`
- [ ] `C-DC-12` `contract` The app uses no persistent volumes, no fixed container names, no custom networks. `src: Deployment contract bullet 12`
- [ ] `C-DC-13` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` An invalid or unauthorized call is rejected as a client error, never a server error. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` The signup endpoint `POST /api/auth/signup` is refused, creating no account. `src: Deployment contract API shapes table`
- [ ] `C-DC-16` `contract` The login endpoint `POST /api/auth/login` accepts `email` with `password`. `src: Deployment contract API shapes table`
- [ ] `C-DC-17` `contract` Bearer authentication guards every studio endpoint. `src: Deployment contract API shapes`
- [ ] `C-DC-18` `contract` The public campaign index returns `total`, `page`, `page_count`, `year_buckets`, `items`. `src: Deployment contract API shapes table`
- [ ] `C-DC-19` `contract` The public tally returns `total`, `itemised`, `headline`. `src: Deployment contract API shapes table`
- [ ] `C-DC-20` `contract` The enquiry endpoint returns `routed_to` with `routing_warning`. `src: Deployment contract API shapes table`
- [ ] `C-DC-21` `constraint` An in-memory buffer or a local file standing in for `minio` is a contract violation. `src: Deployment contract no mocks`
- [ ] `C-DC-22` `contract` A refusal body carries a `message`. `src: Deployment contract API shapes`
- [ ] `C-DC-23` `contract` Public read endpoints default to `locale` `ja` with `market` `JP`. `src: Deployment contract API shapes`
- [ ] `C-DC-24` `contract` The public campaign detail returns `lang` naming the locale shown for each translatable field. `src: Deployment contract API shapes table`
- [ ] `C-DC-25` `contract` The endpoint `DELETE /api/audit-events/{id}` is refused, leaving the event. `src: Deployment contract API shapes table`
- [ ] `C-DC-26` `contract` The endpoint `GET /api/auth/me` returns `email`, `role`, `person_id`. `src: Deployment contract API shapes table`
- [ ] `C-DC-27` `contract` The port is read from `APP_PUBLIC_PORT`, never hardcoded. `src: Deployment contract bullet 1`
- [ ] `C-DC-28` `contract` The server is never a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-29` `contract` The app uses no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-30` `contract` `POST /api/people/{id}/return` takes `returned_on`, returns the person with `status` `active`. `src: Deployment contract API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `account_director@example.com` | seeded account director | C-RL-21 | User roles seeded table row 1 |
| `account_director` | the account director role | C-RL-21 | User roles table |
| `account_director2@example.com` | second seeded account director | C-RL-22 | User roles seeded table row 2 |
| `producer@example.com` | seeded producer | C-RL-23 | User roles seeded table row 3 |
| `producer` | the producer role | C-RL-23 | User roles table |
| `producer2@example.com` | second seeded producer | C-RL-24 | User roles seeded table row 4 |
| `creative@example.com` | seeded creative | C-RL-25 | User roles seeded table row 5 |
| `creative` | the creative role | C-RL-25 | User roles table |
| `creative2@example.com` | second seeded creative | C-RL-26 | User roles seeded table row 6 |
| `legal@example.com` | seeded legal user | C-RL-27 | User roles seeded table row 7 |
| `legal` | the legal role | C-RL-27 | User roles table |
| `editor@example.com` | seeded editor | C-RL-28 | User roles seeded table row 8 |
| `editor` | the editor role | C-RL-28 | User roles table |
| `deku-demo-pw-2026` | password for every seeded account | C-RL-29 | User roles |
| `tsubame-automotive` | rival car account | C-RL-30 | User roles seeded table |
| `aozora-airlines` | airline account | C-RL-31 | User roles seeded table |
| `kagerou-beverages` | beverage account | C-RL-31 | User roles seeded table |
| `Hoshino EV Launch` | walled job | C-CF-11 | Core features rule 1 |
| `10000` | apportionment whole in basis points | C-CF-14 | Core features rule 2 |
| `Sky Tea Partnership` | seeded split job | C-CF-17 | Core features rule 2 |
| `6000` | kagerou share of the split job | C-CF-17 | Core features rule 2 |
| `90` | cooling-off days | C-CF-21 | Core features rule 3 |
| `Hoshino Unit` | client-dedicated unit | C-CF-23 | Core features rule 3 |
| `hoshino-motors` | rival car account | C-CF-23 | Core features rule 3 |
| `RC-2026` | current rate card | C-CF-31 | Core features rule 5 |
| `450` | worked example minutes | C-CF-33 | Core features rule 6 |
| `Art Director` | worked example role | C-CF-33 | Core features rule 6 |
| `90000` | worked example cost | C-CF-33 | Core features rule 6 |
| `125000` | worked example foreign amount | C-CF-35 | Core features rule 6 |
| `usd` | worked example currency | C-CF-35 | Core features rule 6 |
| `148.50` | worked example exchange rate | C-CF-35 | Core features rule 6 |
| `2026-03-31` | worked example rate date | C-CF-35 | Core features rule 6 |
| `185625` | worked example converted amount | C-CF-35 | Core features rule 6 |
| `jpy` | ledger currency | C-CF-37 | Core features rule 6 |
| `That person is fully committed in the weeks you selected.` | capacity refusal copy | C-CF-44 | Core features rule 8 |
| `minio` | the object store | C-CF-49 | Core features rule 9 |
| `jobs/{job_id}/versions/{version_number}/{sha256_of_bytes}.{ext}` | version key scheme | C-CF-49 | Core features rule 9 |
| `Tide Clock` | campaign with an expired market | C-CF-64 | Core features rule 14 |
| `DE` | expired market | C-CF-64 | Core features rule 14 |
| `JP` | default market | C-CF-64 | Core features rule 14 |
| `Night Signal` | seeded award-winning campaign | C-CF-72 | Core features rule 16 |
| `Yuto Baba` | jointly credited producer | C-CF-72 | Core features rule 16 |
| `Riko Nishi` | jointly credited producer | C-CF-72 | Core features rule 16 |
| `Sho Ota` | jointly credited producer | C-CF-72 | Core features rule 16 |
| `Producer` | joint credit role | C-CF-72 | Core features rule 16 |
| `departed` | departed status | C-CF-84 | Core features rule 19 |
| `Jade Petal` | body-specific rank | C-CF-90 | Core features rule 21 |
| `Lotus Festival` | seeded award body | C-CF-90 | Core features rule 21 |
| `Grand Lotus` | supreme rank | C-CF-91 | Core features rule 21 |
| `Gold` | top rank | C-CF-91 | Core features rule 21 |
| `2025` | tallied festival year | C-CF-98 | Core features rule 23 |
| `The campaign cannot be published yet: clearance for one market expires before the scheduled date.` | scheduling refusal copy | C-CF-106 | Core features rule 24 |
| `Silent Aurora` | embargoed campaign | C-CF-112 | Core features rule 25 |
| `2099-01-01T09:00:00+09:00` | embargo moment | C-CF-112 | Core features rule 25 |
| `Quiet Engine` | campaign with a partial English translation | C-CF-119 | Core features rule 27 |
| `ja` | Japanese locale marker | C-CF-119 | Core features rule 27 |
| `Aozora Airlines` | first client by reading | C-CF-125 | Core features rule 29 |
| `Kagerou Beverages` | second client by reading | C-CF-125 | Core features rule 29 |
| `Tsubame Automotive` | third client by reading | C-CF-125 | Core features rule 29 |
| `Hoshino Motors` | fourth client by reading | C-CF-125 | Core features rule 29 |
| `Minato Rail` | fifth client by reading | C-CF-125 | Core features rule 29 |
| `信号` | Japanese search fragment | C-CF-129 | Core features rule 30 |
| `before` | older-years bucket | C-CF-133 | Core features rule 31 |
| `Lotus Festival 2025 results` | seeded award article | C-CF-149 | Core features rule 33 |
| `awards` | article category | C-CF-149 | Core features rule 33 |
| `news` | article category | C-CF-149 | Core features rule 33 |
| `Hiroshi Kudo` | officer with a concurrent position | C-CF-151 | Core features rule 34 |
| `Meido Group` | domestic parent group | C-CF-151 | Core features rule 34 |
| `We cannot reach the recruiting service right now. Here is how to contact us directly.` | recruiting fallback copy | C-CF-155 | Core features rule 34 |
| `website` | enquiry decoy field | C-CF-158 | Core features rule 35 |
| `general` | enquiry type with no recipient | C-CF-161 | Core features rule 35 |
| `desk@kuromeido.example.com` | default desk | C-CF-161 | Core features rule 35 |
| `new_business` | enquiry type | C-CF-162 | Core features rule 35 |
| `newbusiness@kuromeido.example.com` | new business desk | C-CF-162 | Core features rule 35 |
| `Thank you. We will reply within two working days.` | enquiry confirmation | C-CF-166 | Core features rule 35 |
| `Sorry, nothing lives at that address.` | not-found apology | C-CF-172 | Core features rule 37 |
| `24` | enquiry retention in months | C-CF-181 | Technical requirements retention |
| `No campaigns in that year yet. Clear the filter to see everything.` | empty work index copy | C-UF-13 | User flow states |
| `No articles match those filters.` | empty newsroom copy | C-UF-14 | User flow states |
| `Nothing is waiting for your approval.` | empty studio desk copy | C-UF-15 | User flow table |
| `That did not save. Your work is still here, so try again.` | failed save copy | C-UF-17 | User flow states |
| `Noto Sans JP` | Japanese typeface | C-UX-06 | UI/UX notes type |
| `Archivo` | Latin display typeface | C-UX-07 | UI/UX notes type |
| `160px` | display type size | C-UX-10 | UI/UX notes type |
| `rupture is not destruction.` | hero premise | C-FE-22 | Front-end specification home |
| `RUPTURE IS CREATION.` | hero answer | C-FE-22 | Front-end specification home |
| `CREATE. INVENT. HAVE IDEAS.` | statement triplet | C-FE-23 | Front-end specification home |
| `READY TO BREAK SOMETHING` | closing marquee line | C-FE-25 | Front-end specification home |
| `WHY JOIN THE NAVY WHEN YOU CAN BE A PIRATE` | culture statement | C-FE-30 | Front-end specification careers |
| `The page is not yet available in English; showing the Japanese original.` | fallback notice | C-FE-33 | Front-end specification copy deck |
| `X-Robots-Tag: noindex` | preview indexing header | C-TR-22 | Technical requirements security headers |
| `partial` | partial aggregate flag | C-TR-16 | Technical requirements aggregates |
| `minato-rail` | rail account | C-DM-13 | Data model clients table |
| `2400` | weekly capacity in minutes | C-DM-15 | Data model seed data |
| `12000` | Art Director hourly rate | C-DM-16 | Data model rate cards table |
| `US` | second default market | C-DM-17 | Data model campaigns table |
| `lotus-festival-2025-results` | award article slug | C-DM-19 | Data model articles |
| `Shun Kaneda` | departed credited person | C-DM-20 | Data model credit list |
| `2026-02-27` | departure date | C-DM-20 | Data model credit list |
| `paper-lanterns` | ready draft campaign | C-DM-21 | Data model further campaigns |
| `winter-kite` | untranslated campaign | C-DM-22 | Data model further campaigns |
| `RC-2025` | previous rate card | C-DM-24 | Data model rate cards |
| `2025-01-01` | previous card start | C-DM-24 | Data model rate cards |
| `2025-12-31` | previous card end | C-DM-24 | Data model rate cards |
| `${APP_PUBLIC_PORT}:4173` | port mapping | C-DC-02 | Deployment contract bullet 1 |
| `/app/USER_README.md` | credentials file | C-DC-06 | Deployment contract bullet 5 |
| `0.0.0.0` | bind address | C-DC-10 | Deployment contract bullet 9 |
| `clearance` | a value the brief pins | C-CF-183 | Core features rule 24 |
| `case_study_permission` | a value the brief pins | C-CF-183 | Core features rule 24 |
| `credits` | a value the brief pins | C-CF-183 | Core features rule 24 |
| `rights_expire_before_release` | a value the brief pins | C-CF-183 | Core features rule 24 |
| `recruitment` | a value the brief pins | C-CF-191 | Core features rule 35 |
| `careers@kuromeido.example.com` | a value the brief pins | C-CF-191 | Core features rule 35 |
| `press` | a value the brief pins | C-CF-192 | Core features rule 35 |
| `press@kuromeido.example.com` | a value the brief pins | C-CF-192 | Core features rule 35 |
| `7` | a value the brief pins | C-CF-205 | Technical requirements retention |
| `5` | a value the brief pins | C-CF-206 | Technical requirements retention |
| `10` | a value the brief pins | C-CF-207 | Technical requirements retention |
| `Creative Director` | a value the brief pins | C-CF-215 | Core features rule 8 |
| `Senior Creative Director` | a value the brief pins | C-CF-215 | Core features rule 8 |
| `campaigns/{campaign_id}/{sha256_of_bytes}.{ext}` | a value the brief pins | C-CF-218 | Core features rule 9 |
| `pending` | a value the brief pins | C-CF-219 | Core features rule 10 |
| `approved` | a value the brief pins | C-CF-219 | Core features rule 10 |
| `changes_requested` | a value the brief pins | C-CF-219 | Core features rule 10 |
| `withdrawn` | a value the brief pins | C-CF-219 | Core features rule 10 |
| `music` | a value the brief pins | C-CF-221 | Core features rule 13 |
| `talent` | a value the brief pins | C-CF-221 | Core features rule 13 |
| `imagery` | a value the brief pins | C-CF-221 | Core features rule 13 |
| `claims` | a value the brief pins | C-CF-221 | Core features rule 13 |
| `trademark` | a value the brief pins | C-CF-221 | Core features rule 13 |
| `festival_exhibition` | a value the brief pins | C-CF-221 | Core features rule 13 |
| `submitted` | a value the brief pins | C-CF-224 | Core features rule 22 |
| `shortlisted` | a value the brief pins | C-CF-224 | Core features rule 22 |
| `closed` | a value the brief pins | C-CF-224 | Core features rule 22 |
| `Kagerou Studio` | a value the brief pins | C-CF-229 | Core features rule 3 |
| `absent` | a value the brief pins | C-CF-233 | Core features rule 27 |
| `drafted` | a value the brief pins | C-CF-233 | Core features rule 27 |
| `in_translation` | a value the brief pins | C-CF-233 | Core features rule 27 |
| `reviewed` | a value the brief pins | C-CF-233 | Core features rule 27 |
| `published` | a value the brief pins | C-CF-233 | Core features rule 27 |
| `Rice Field Radio` | a value the brief pins | C-CF-234 | Core features rule 27 |
| `しんごう` | a value the brief pins | C-CF-239 | Core features rule 30 |
| `Harbour Lights` | a value the brief pins | C-CF-243 | Core features rule 25 |
| `internship` | a value the brief pins | C-CF-244 | Core features rule 34 |
| `https://careers.example.org/kuromeido/internships` | a value the brief pins | C-CF-244 | Core features rule 34 |
| `That campaign is not yet available in English, so here is all of our work.` | a value the brief pins | C-CF-245 | Core features rule 28 |
| `/studio/briefs/new/1` | a value the brief pins | C-UF-22 | User flow table |
| `/studio/briefs/new/2` | a value the brief pins | C-UF-22 | User flow table |
| `/studio/briefs/new/3` | a value the brief pins | C-UF-22 | User flow table |
| `Desk` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Accounts` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Briefs` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Jobs` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Clearance` | a value the brief pins | C-UF-23 | User flow studio shape |
| `People` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Rate cards` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Awards` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Publishing` | a value the brief pins | C-UF-23 | User flow studio shape |
| `Reports` | a value the brief pins | C-UF-23 | User flow studio shape |
| `56px` | a value the brief pins | C-UX-26 | UI/UX notes type |
| `24px` | a value the brief pins | C-UX-27 | UI/UX notes type |
| `16px` | a value the brief pins | C-UX-28 | UI/UX notes type |
| `11px` | a value the brief pins | C-UX-29 | UI/UX notes type |
| `14px` | a value the brief pins | C-UX-30 | UI/UX notes type |
| `13px` | a value the brief pins | C-UX-30 | UI/UX notes type |
| `4.5:1` | a value the brief pins | C-UX-31 | UI/UX notes accessibility |
| `I have read the privacy policy, which I accept.` | a value the brief pins | C-FE-39 | Front-end specification copy deck |
| `MENU` | a value the brief pins | C-FE-40 | Front-end specification global chrome |
| `Close menu` | a value the brief pins | C-FE-41 | Front-end specification global chrome |
| `Necessary` | a value the brief pins | C-FE-42 | Front-end specification global chrome |
| `Analytics` | a value the brief pins | C-FE-42 | Front-end specification global chrome |
| `Marketing` | a value the brief pins | C-FE-42 | Front-end specification global chrome |
| `(c) KURO\MEIDO Inc.` | a value the brief pins | C-FE-43 | Front-end specification global chrome |
| `2026-04-01` | a value the brief pins | C-FE-44 | Front-end specification company |
| `+81-3-5555-0100` | a value the brief pins | C-FE-45 | Front-end specification company |
| `Kaito Mizuno` | a value the brief pins | C-FE-46 | Front-end specification company |
| `President & CEO` | a value the brief pins | C-FE-46 | Front-end specification company |
| `CREATIVITY COMES FROM DIVERSITY` | a value the brief pins | C-FE-47 | Front-end specification careers |
| `1 April 2006` | a value the brief pins | C-FE-48 | Front-end specification company |
| `200` | a value the brief pins | C-TR-33 | Technical requirements uploads |
| `tide-clock` | a value the brief pins | C-DM-17 | Data model campaigns table |
| `2026-01-05` | a value the brief pins | C-DM-25 | Data model seed data |
| `2026-12-27` | a value the brief pins | C-DM-25 | Data model seed data |
| `1200` | a value the brief pins | C-DM-25 | Data model seed data |
| `PERM-PAPER-LANTERNS` | a value the brief pins | C-DM-27 | Data model further campaigns |
| `Kenji Mori` | a value the brief pins | C-DM-28 | Data model seed data |
| `active` | a value the brief pins | C-CF-246 | Core features rule 19 |
| `embargo` | a value the brief pins | C-CF-247 | Core features rule 24 |
| `/preview/<token>` | a value the brief pins | C-CF-249 | Core features rule 26 |
| `/wp-json/` | a value the brief pins | C-CF-250 | Core features rule 37 |
| `North Star Awards` | a value the brief pins | C-CF-264 | Core features rule 21 |
| `Silver` | a value the brief pins | C-CF-264 | Core features rule 21 |
| `Bronze` | a value the brief pins | C-CF-264 | Core features rule 21 |
| `Merit` | a value the brief pins | C-CF-264 | Core features rule 21 |
| `/studio/briefs/<id>` | a value the brief pins | C-UF-28 | User flow route table |
| `notosansjp` | a value the brief pins | C-UX-41 | UI/UX notes type |
| `EST. 2006` | a value the brief pins | C-FE-50 | Front-end specification home |
| `TOKYO` | a value the brief pins | C-FE-50 | Front-end specification home |
| `35.6581 N 139.7561 E` | a value the brief pins | C-FE-50 | Front-end specification home |
| `We use creativity to move business` | a value the brief pins | C-FE-51 | Front-end specification home |
| `We are the method company.` | a value the brief pins | C-FE-52 | Front-end specification home |
| `104-0061` | a value the brief pins | C-FE-64 | Front-end specification company |
| `Kaigan Tower 14F, 1-2-3 Kaigan, Chuo-ku, Tokyo` | a value the brief pins | C-FE-64 | Front-end specification company |
| `Masato Ide` | a value the brief pins | C-FE-65 | Front-end specification company |
| `Auditor` | a value the brief pins | C-FE-65 | Front-end specification company |
| `Audit Partner, Meido Group` | a value the brief pins | C-FE-65 | Front-end specification company |
| `Emi Hayashi` | a value the brief pins | C-FE-66 | Front-end specification company |
| `Ren Shibata` | a value the brief pins | C-FE-66 | Front-end specification company |
| `Laura Chen` | a value the brief pins | C-FE-66 | Front-end specification company |
| `Non-executive Director` | a value the brief pins | C-FE-67 | Front-end specification company |
| `Regional President, KURO Worldwide` | a value the brief pins | C-FE-67 | Front-end specification company |
| `Creative, new graduates 2027` | a value the brief pins | C-FE-68 | Front-end specification careers |
| `https://careers.example.org/kuromeido/new-graduates` | a value the brief pins | C-FE-68 | Front-end specification careers |
| `Summer internship 2027` | a value the brief pins | C-FE-69 | Front-end specification careers |
| `8` | a value the brief pins | C-TR-42 | Technical requirements auth |
| `open` | a value the brief pins | C-DM-29 | Data model tables |
| `converted` | a value the brief pins | C-DM-29 | Data model tables |
| `harbour-lights` | a value the brief pins | C-DM-31 | Data model further campaigns |
| `PERM-HARBOUR-LIGHTS` | a value the brief pins | C-DM-31 | Data model further campaigns |
| `stories` | a value the brief pins | C-DM-34 | Data model articles |
| `2019` | a value the brief pins | C-DM-34 | Data model articles |
| `night-signal` | a value the brief pins | C-DM-35 | Data model public campaigns |
| `よるのしんごう` | a value the brief pins | C-DM-35 | Data model public campaigns |
| `Chief Creative Officer` | a value the brief pins | C-DM-36 | Data model credit list |
| `Head of Innovation` | a value the brief pins | C-DM-36 | Data model credit list |
| `POST /api/people/{id}/return` | a value the brief pins | C-DC-30 | Deployment contract API shapes |
| `returned_on` | a value the brief pins | C-DC-30 | Deployment contract API shapes |
| `status` | a value the brief pins | C-DC-30 | Deployment contract API shapes |
| `1992` | a value the brief pins | C-FE-78 | Front-end specification home |
| `海軍に入るな、海賊になれ。` | a value the brief pins | C-FE-80 | Front-end specification careers |
| `BE A PIRATE` | a value the brief pins | C-FE-81 | Front-end specification careers |
| `海賊であれ` | a value the brief pins | C-FE-82 | Front-end specification careers |
| `多様性が創造性を生む` | a value the brief pins | C-FE-83 | Front-end specification careers |
| `UNCOMMON HUMANITY` | a value the brief pins | C-FE-84 | Front-end specification careers |
| `並外れた人間らしさ` | a value the brief pins | C-FE-85 | Front-end specification careers |
| `GOOD ENOUGH IS NOT ENOUGH` | a value the brief pins | C-FE-86 | Front-end specification careers |
| `十分では足りない` | a value the brief pins | C-FE-87 | Front-end specification careers |
| `BE BRAVE` | a value the brief pins | C-FE-88 | Front-end specification careers |
| `勇敢であれ` | a value the brief pins | C-FE-89 | Front-end specification careers |
| `Convention` | a value the brief pins | C-FE-123 | Front-end specification methodology |
| `Vision` | a value the brief pins | C-FE-123 | Front-end specification methodology |
| `Method` | a value the brief pins | C-FE-123 | Front-end specification methodology |
| `Rupture` | a value the brief pins | C-FE-124 | Front-end specification methodology |
| `WORK` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `NEWS` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `METHODOLOGY` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `COMPANY` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `CAREERS` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `SUSTAINABILITY` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `CONTACT` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `HOME` | a value the brief pins | C-FE-125 | Front-end specification global chrome |
| `JA` | a value the brief pins | C-FE-126 | Front-end specification global chrome |
| `EN` | a value the brief pins | C-FE-126 | Front-end specification global chrome |
| `innovation` | a value the brief pins | C-FE-127 | Front-end specification surfaces and marks |
| `Chief Operating Officer` | a value the brief pins | C-FE-128 | Front-end specification company |
| `Executive Officer, Meido Group` | a value the brief pins | C-FE-130 | Front-end specification company |
| `Planning` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Media Experience Design` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Corporate Strategy` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Finance` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Executive Management` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Rupture Lab` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Integrated Business Leadership` | a value the brief pins | C-FE-131 | Front-end specification company |
| `Minato Media Partners` | a value the brief pins | C-FE-131 | Front-end specification company |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the lifetime of a signed file link | C-CF-13 | bounded by the clearance that granted the link, with no duration given |
| the rate at which repeated enquiries slow down | C-CF-187 | described as gradual, with no threshold given |
| the marquee speed per band | C-FE-18 | described as distance per second, with the constants left to tuning |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 7 |
| User roles | 1 | 57 |
| Core features | 30 | 273 |
| User flow | 9 | 34 |
| UI and UX notes | 2 | 45 |
| Front-end specification | 3 | 131 |
| Technical requirements | 8 | 49 |
| Data model | 3 | 37 |
| Constraints | 1 | 10 |
| Deployment contract | 11 | 30 |

Definition of done carries no obligation-bearing sentence of its own: its lines restate items already listed, C-OV-02 with C-CF-72 and C-CF-144 for the bilingual Night Signal read, C-DM-21 for Paper Lanterns, C-CF-11 for the wall.
