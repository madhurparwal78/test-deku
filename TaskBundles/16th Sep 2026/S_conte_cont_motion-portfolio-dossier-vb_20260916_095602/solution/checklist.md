# Checklist: Motion Portfolio Dossier

Source: instruction.md
Sections present: overview, user roles, core features, user flow, ui and ux notes, front-end specification, technical requirements, data model, constraints, deployment contract
Sections absent: build plan
Items: 564
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The product holds one long dark home route introducing the designer. `src: Overview para 2`
- [ ] `C-OV-02` `capability` The product holds eleven long-form case studies, each on a route at the origin root. `src: Overview para 2`
- [ ] `C-OV-03` `capability` Eight case studies are articles with a chapter rail down the left. `src: Overview para 2`
- [ ] `C-OV-04` `capability` Three case studies are galleries. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The one action a visitor is asked to take is sending an email. `src: Overview para 1`
- [ ] `C-OV-06` `capability` A private studio lets the designer write, illustrate, publish, withdraw case studies. `src: Overview para 3`
- [ ] `C-OV-07` `constraint` The product has no search, no comment, no like, no sharing button. `src: Overview para 4`
- [ ] `C-OV-08` `constraint` The product has no contact form, no page transition, no light theme, no payment. `src: Overview para 4`
- [ ] `C-OV-09` `capability` Reading any published page needs no account. `src: Overview para 4`
- [ ] `C-OV-10` `constraint` The site ships with no binary assets. `src: Overview para 5`
- [ ] `C-OV-11` `capability` The same item always generates the same picture. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads the home page, every published case study, the work index, the privacy page. `src: User roles table row 1`
- [ ] `C-RL-02` `role` An anonymous visitor keeps reading positions plus a motion level in the visitor's own browser only. `src: User roles table row 1`
- [ ] `C-RL-03` `role` An anonymous visitor cannot save to a reading list. `src: User roles table row 1`
- [ ] `C-RL-04` `role` An anonymous visitor cannot reach the studio. `src: User roles table row 1`
- [ ] `C-RL-05` `role` Neither an anonymous visitor nor a `reader` reads anything unpublished. `src: User roles table rows 1, 2`
- [ ] `C-RL-06` `role` A `reader` keeps a reading list, reading positions, a motion level on the account across devices. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A `reader` cannot reach any studio route or studio endpoint. `src: User roles table row 2`
- [ ] `C-RL-08` `role` A `reader` cannot read or change another account's reading list or preferences. `src: User roles table row 2`
- [ ] `C-RL-09` `role` The `designer` signs in at `/login`. `src: User roles table row 3`
- [ ] `C-RL-10` `role` The `designer` creates case studies, writes chapters, uploads images, publishes, withdraws. `src: User roles table row 3`
- [ ] `C-RL-11` `role` The `designer` previews a draft through the public templates. `src: User roles table row 3`
- [ ] `C-RL-12` `role` The `designer` reads drafts plus the images of drafts. `src: User roles table row 3`
- [ ] `C-RL-13` `role` The `designer` account is seeded, never created through signup. `src: User roles table row 3`
- [ ] `C-RL-14` `role` Authorization is enforced server-side on every mutating endpoint. `src: User roles para 1`
- [ ] `C-RL-15` `role` A direct API call from a `reader` session to a `designer`-only endpoint is denied, leaving the protected state unchanged. `src: User roles para 1`
- [ ] `C-RL-16` `role` Signup always creates a `reader`, whatever the request body carries. `src: User roles para 2`
- [ ] `C-RL-17` `role` A reading list is reachable only with its owner's own session. `src: User roles para 2`
- [ ] `C-RL-18` `literal` The seeded account `designer@example.com` holds the role `designer`. `src: User roles table, seeded accounts row 1`
- [ ] `C-RL-19` `literal` The seeded account `reader@example.com` holds the role `reader`. `src: User roles table, seeded accounts row 2`
- [ ] `C-RL-20` `literal` The seeded account `reader2@example.com` holds the role `reader`. `src: User roles table, seeded accounts row 3`
- [ ] `C-RL-21` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles, seeded accounts`

## C-CF Core features

- [ ] `C-CF-01` `capability` A draft is absent from the home page's featured grid plus work list. `src: Core features rule 1`
- [ ] `C-CF-02` `capability` A draft is absent from `/work` plus the response of `GET /api/case-studies`. `src: Core features rule 1`
- [ ] `C-CF-03` `capability` A draft is absent from every suggestion pair. `src: Core features rule 1`
- [ ] `C-CF-04` `capability` A draft is absent from every reading list read. `src: Core features rule 1`
- [ ] `C-CF-05` `capability` A direct request for a draft's address answers a not-found status. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` The not-found page for a draft never names the draft. `src: Core features rule 1`
- [ ] `C-CF-07` `role` The images of a draft are refused to everyone who is not the `designer`. `src: Core features rule 1`
- [ ] `C-CF-08` `capability` Publishing makes the listings, the address, the images readable in one act. `src: Core features rule 1`
- [ ] `C-CF-09` `capability` Withdrawing makes the listings, the address, the images unreachable again at once. `src: Core features rule 1`
- [ ] `C-CF-10` `literal` The seeded draft `A Wearable That Knew When to Stay Quiet` sits at `/kestra-band`. `src: Core features rule 1`
- [ ] `C-CF-11` `constraint` The not-found answer for a draft address matches the answer for an address that never existed. `src: Core features rule 1`
- [ ] `C-CF-12` `capability` Saving a draft to a reading list is refused. `src: Core features rule 1`
- [ ] `C-CF-13` `capability` Every uploaded image or reel is stored in `minio`. `src: Core features rule 2`
- [ ] `C-CF-14` `literal` Each object is stored at the key `case-studies/{case_study_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 2`
- [ ] `C-CF-15` `data` The media row records where the bytes are stored. `src: Core features rule 2`
- [ ] `C-CF-16` `data` Every media row carries its intrinsic width plus height. `src: Core features rule 2`
- [ ] `C-CF-17` `data` Every media row carries a text alternative written by the designer. `src: Core features rule 2`
- [ ] `C-CF-18` `capability` Two uploads of identical bytes to one case study resolve to one object. `src: Core features rule 2`
- [ ] `C-CF-19` `literal` An image upload accepts `image/png`, `image/jpeg`, `image/webp`. `src: Core features rule 2`
- [ ] `C-CF-20` `literal` A reel upload accepts `video/mp4`. `src: Core features rule 2`
- [ ] `C-CF-21` `constraint` An upload of any other type is rejected as invalid with nothing stored. `src: Core features rule 2`
- [ ] `C-CF-22` `constraint` A case study has at most one `hero` image. `src: Core features rule 2`
- [ ] `C-CF-23` `constraint` A case study has at most one `reel`. `src: Core features rule 2`
- [ ] `C-CF-24` `capability` A new hero image replaces the old one. `src: Core features rule 2`
- [ ] `C-CF-25` `literal` The app serves media bytes at `GET /api/media/{id}`. `src: Core features rule 2`
- [ ] `C-CF-26` `constraint` Media bytes are never served from a publicly readable bucket. `src: Core features rule 2`
- [ ] `C-CF-27` `constraint` Publishing is refused for a case study with no `hero` image. `src: Core features rule 3`
- [ ] `C-CF-28` `constraint` Publishing is refused when any media of the case study has empty alternative text. `src: Core features rule 3`
- [ ] `C-CF-29` `constraint` Publishing is refused for a `product` case study with no chapter. `src: Core features rule 3`
- [ ] `C-CF-30` `capability` A refused publish leaves the case study a draft. `src: Core features rule 3`
- [ ] `C-CF-31` `capability` The publish refusal names the missing condition. `src: Core features rule 3`
- [ ] `C-CF-32` `capability` `/work` shows every published case study at once. `src: Core features rule 4`
- [ ] `C-CF-33` `literal` `/work` carries the label `Everything`. `src: Core features rule 4`
- [ ] `C-CF-34` `literal` `/work` carries the heading `All Work`. `src: Core features rule 4`
- [ ] `C-CF-35` `capability` `/work` shows the case studies in a grid or a list. `src: Core features rule 4`
- [ ] `C-CF-36` `capability` `/work` filters by client. `src: Core features rule 4`
- [ ] `C-CF-37` `capability` `/work` filters by discipline. `src: Core features rule 4`
- [ ] `C-CF-38` `capability` `/work` sorts by year or by name. `src: Core features rule 4`
- [ ] `C-CF-39` `capability` The whole work index state lives in the address query string. `src: Core features rule 4`
- [ ] `C-CF-40` `capability` A case study is listed only when carrying every selected client plus every selected discipline. `src: Core features rule 4`
- [ ] `C-CF-41` `literal` The work index address carries the parameters `client`, `discipline`, `sort`, `view`, with comma-separated tokens, as in `?client=kestra,quitkit&discipline=systems&sort=year-asc&view=list`. `src: Core features rule 4`
- [ ] `C-CF-42` `capability` Two clients selected together yield the empty state. `src: Core features rule 4`
- [ ] `C-CF-43` `literal` The client tokens are `verity-biotics`, `kestra`, `mirror-lab`, `dusk-ritual`, `quitkit`. `src: Core features rule 4`
- [ ] `C-CF-44` `literal` The discipline tokens are `strategy`, `product`, `brand-creative`, `systems`, `spatial-experience`. `src: Core features rule 4`
- [ ] `C-CF-45` `literal` The sort tokens are `year-desc`, `year-asc`, `title-asc`. `src: Core features rule 4`
- [ ] `C-CF-46` `literal` The default sort is `year-desc`. `src: Core features rule 4`
- [ ] `C-CF-47` `literal` The view tokens are `grid`, `list`. `src: Core features rule 4`
- [ ] `C-CF-48` `capability` Year ties order by index title from A to Z without regard to case. `src: Core features rule 4`
- [ ] `C-CF-49` `capability` The `title-asc` sort orders by index title from A to Z without regard to case. `src: Core features rule 4`
- [ ] `C-CF-50` `capability` An unrecognised filter value is dropped field by field, with the rest still applied. `src: Core features rule 4`
- [ ] `C-CF-51` `capability` The address is rewritten to the corrected work index state. `src: Core features rule 4`
- [ ] `C-CF-52` `capability` One line on `/work` says an unrecognised filter value was dropped. `src: Core features rule 4`
- [ ] `C-CF-53` `literal` A work index query string longer than `512` characters is ignored entirely. `src: Core features rule 4`
- [ ] `C-CF-54` `capability` Every filter change is a history entry that back or forward walks through. `src: Core features rule 4`
- [ ] `C-CF-55` `capability` A filter toggled twice in quick succession replaces its history entry. `src: Core features rule 4`
- [ ] `C-CF-56` `capability` Sort plus view are remembered as preferences. `src: Core features rule 4`
- [ ] `C-CF-57` `constraint` Filters are not remembered as preferences. `src: Core features rule 4`
- [ ] `C-CF-58` `literal` The two suggestions come from `GET /api/case-studies/{slug}/related`. `src: Core features rule 5`
- [ ] `C-CF-59` `capability` Suggestions are computed over the published case studies. `src: Core features rule 5`
- [ ] `C-CF-60` `capability` A case study's tags are the client plus the disciplines. `src: Core features rule 5`
- [ ] `C-CF-61` `capability` Similarity is 0.75 times overlap plus 0.25 times recency. `src: Core features rule 5`
- [ ] `C-CF-62` `capability` Recency is one divided by one plus the absolute difference of the two years. `src: Core features rule 5`
- [ ] `C-CF-63` `capability` Overlap is the count of shared tags divided by the count of combined tags. `src: Core features rule 5`
- [ ] `C-CF-64` `capability` Slot one is the most similar other case study. `src: Core features rule 5`
- [ ] `C-CF-65` `capability` Equal similarity to four decimal places goes to the alphabetically first slug. `src: Core features rule 5`
- [ ] `C-CF-66` `constraint` Slot two is never the current case study nor slot one. `src: Core features rule 5`
- [ ] `C-CF-67` `capability` No published case study goes unsuggested. `src: Core features rule 5`
- [ ] `C-CF-68` `capability` Every published case study is reachable from every other in at most four suggestion hops. `src: Core features rule 5`
- [ ] `C-CF-69` `capability` The four-hop reach still holds after any publish or withdrawal. `src: Core features rule 5`
- [ ] `C-CF-70` `capability` Every published case study stays suggested somewhere after any publish or withdrawal. `src: Core features rule 5`
- [ ] `C-CF-71` `literal` Slot one for `kestra-care` is `kestra-home` at `0.7917`. `src: Core features rule 5 table row 1`
- [ ] `C-CF-72` `literal` Slot one for `verity-biotics-product` is `aging-model` at `0.6250`. `src: Core features rule 5 table row 2`
- [ ] `C-CF-73` `literal` Slot one for `mirror-lab` is `dusk-ritual` at `0.3125`. `src: Core features rule 5 table row 3`
- [ ] `C-CF-74` `literal` Slot one for `quitkit` is `dusk-ritual` at `0.3750`, tied with `verity-biotics-brand`, winning on the alphabetical rule. `src: Core features rule 5 table row 4`
- [ ] `C-CF-75` `capability` A signed-in account saves a published case study to the account's reading list. `src: Core features rule 6`
- [ ] `C-CF-76` `capability` A signed-in account removes a case study from the account's reading list. `src: Core features rule 6`
- [ ] `C-CF-77` `constraint` Saving the same case study twice leaves exactly one entry. `src: Core features rule 6`
- [ ] `C-CF-78` `capability` The `max_fraction` of an entry never goes down. `src: Core features rule 6`
- [ ] `C-CF-79` `capability` The `last_fraction` of an entry records where the reader was on leaving, even when lower. `src: Core features rule 6`
- [ ] `C-CF-80` `capability` The `chapters_read` of an entry only ever grows. `src: Core features rule 6`
- [ ] `C-CF-81` `literal` The `completed` flag is true exactly when `max_fraction` reaches `0.95`. `src: Core features rule 6`
- [ ] `C-CF-82` `constraint` A progress write with a fraction outside 0 to 1 is rejected as invalid, changing nothing. `src: Core features rule 6`
- [ ] `C-CF-83` `constraint` A progress write naming a chapter the case study lacks is rejected, changing nothing. `src: Core features rule 6`
- [ ] `C-CF-84` `constraint` Progress for a case study not on the reading list is refused. `src: Core features rule 6`
- [ ] `C-CF-85` `capability` A chapter added or removed by the designer discards every stored position for that case study. `src: Core features rule 6`
- [ ] `C-CF-86` `literal` After a chapter change `last_fraction` is empty, `chapters_read` is empty, `max_fraction` is capped at `0.5`. `src: Core features rule 6`
- [ ] `C-CF-87` `capability` Withdrawing a case study removes the case study from every reading list read. `src: Core features rule 6`
- [ ] `C-CF-88` `ui` The chapter rail marks chapters as unread, current or read. `src: Core features rule 7`
- [ ] `C-CF-89` `ui` A return to a partly read case study offers `Take me back` in a small corner card. `src: Core features rule 7`
- [ ] `C-CF-90` `capability` The resume card appears only past the first twentieth, before completion, after ten minutes away, with unchanged chapters. `src: Core features rule 7`
- [ ] `C-CF-91` `capability` The resume card never appears after arrival at a chapter address or a browser-restored position. `src: Core features rule 7`
- [ ] `C-CF-92` `capability` The resume card dismisses itself after ten seconds, not returning that session. `src: Core features rule 7`
- [ ] `C-CF-93` `ui` The resume card title names the rail label of the furthest chapter in `chapters_read`. `src: Core features rule 7`
- [ ] `C-CF-94` `capability` `Take me back` returns the reader to the point where the reader stopped. `src: Core features rule 7`
- [ ] `C-CF-95` `ui` The home page grows a `Carry on` band listing up to three unfinished case studies. `src: Core features rule 7`
- [ ] `C-CF-96` `ui` Each `Carry on` row shows a thin rule filled to how far the reader got. `src: Core features rule 7`
- [ ] `C-CF-97` `capability` The `Carry on` band does not exist until something is partly read. `src: Core features rule 7`
- [ ] `C-CF-98` `capability` A chapter counts as read only after two seconds spent inside the chapter. `src: Core features rule 7`
- [ ] `C-CF-99` `ui` `/reading-list` lists the saved case studies with a progress rule plus a `Take me back` action. `src: Core features rule 7`
- [ ] `C-CF-100` `capability` For a signed-in reader the reading spine comes from the server. `src: Core features rule 7`
- [ ] `C-CF-101` `constraint` For an anonymous visitor the reading spine comes from the visitor's browser, sending nothing out. `src: Core features rule 7`
- [ ] `C-CF-102` `capability` A first-time visitor sees no reading spine surface. `src: Core features rule 7`
- [ ] `C-CF-103` `literal` The motion setting has three levels, `Everything`, `Less`, `Nothing`. `src: Core features rule 8`
- [ ] `C-CF-104` `literal` The levels are stored as `full`, `reduced`, `still`. `src: Core features rule 8`
- [ ] `C-CF-105` `capability` The motion level governs every moving thing on every route. `src: Core features rule 8`
- [ ] `C-CF-106` `capability` A motion level change takes effect without a reload. `src: Core features rule 8`
- [ ] `C-CF-107` `capability` The motion level starts from the operating system reduced-motion preference until the visitor chooses. `src: Core features rule 8`
- [ ] `C-CF-108` `capability` A system preference change applies at once until the visitor has chosen. `src: Core features rule 8`
- [ ] `C-CF-109` `ui` At `Nothing` the three lit passages render at full brightness. `src: Core features rule 8`
- [ ] `C-CF-110` `capability` At `Nothing` the three lit passages render unsplit. `src: Core features rule 8`
- [ ] `C-CF-111` `capability` A signed-in reader's motion level is kept on the account. `src: Core features rule 8`
- [ ] `C-CF-112` `capability` An anonymous visitor's motion level is kept in the visitor's browser. `src: Core features rule 8`
- [ ] `C-CF-113` `capability` The tilt permission question is asked once per device. `src: Core features rule 8`
- [ ] `C-CF-114` `capability` A declined tilt permission holds for as long as the browser may remember. `src: Core features rule 8`
- [ ] `C-CF-115` `capability` The preferences panel is the only way back to the tilt permission. `src: Core features rule 8`
- [ ] `C-CF-116` `literal` One frosted card component carries the kinds `place`, `mechanism`, `note`. `src: Core features rule 9`
- [ ] `C-CF-117` `ui` The city name in the about passage opens the `place` card. `src: Core features rule 9`
- [ ] `C-CF-118` `ui` The section heading opens the `mechanism` card. `src: Core features rule 9`
- [ ] `C-CF-119` `capability` A card explaining a number takes the number from the constant the animation reads. `src: Core features rule 9`
- [ ] `C-CF-120` `literal` The mechanism card's fourth line reads `startY(i) = -40 * curve(t)`. `src: Core features rule 9`
- [ ] `C-CF-121` `capability` Each card's content is present in the page as the trigger's description. `src: Core features rule 9`
- [ ] `C-CF-122` `ui` A reveal-all mode underlines every explained element. `src: Core features rule 9`
- [ ] `C-CF-123` `ui` The reveal-all mode lists the explanations above the footer under the pinned heading. `src: Core features rule 9`
- [ ] `C-CF-124` `capability` The reveal-all mode is off by default. `src: Core features rule 9`
- [ ] `C-CF-125` `capability` A visitor is asked the pinned question in a small corner card the first time the browser has something to keep. `src: Core features rule 10`
- [ ] `C-CF-126` `ui` The browser question offers `Remember my place` beside `Do not remember` at equal prominence. `src: Core features rule 10`
- [ ] `C-CF-127` `ui` The browser question never covers the page's content. `src: Core features rule 10`
- [ ] `C-CF-128` `literal` The answer is a cookie named `reading_memory` holding `yes` or `no`. `src: Core features rule 10`
- [ ] `C-CF-129` `literal` The `reading_memory` cookie lasts `180` days. `src: Core features rule 10`
- [ ] `C-CF-130` `literal` The `reading_memory` cookie is set by `POST /api/consent`. `src: Core features rule 10`
- [ ] `C-CF-131` `capability` Once the `reading_memory` cookie exists the browser question is not rendered again. `src: Core features rule 10`
- [ ] `C-CF-132` `capability` Until a visitor answers `yes`, the browser keeps positions, the motion level, the tilt answer, sort plus view for the session only. `src: Core features rule 10`
- [ ] `C-CF-133` `ui` A first visit with nothing kept shows no card, no `Carry on` band, no resume card, no read marks. `src: Core features rule 10`
- [ ] `C-CF-134` `capability` The page carries the browser question markup, hidden, until the `reading_memory` cookie exists. `src: Core features rule 10`
- [ ] `C-CF-135` `ui` The browser question card shows once a chapter is passed, a motion level chosen, or a sort or view changed. `src: Core features rule 10`
- [ ] `C-CF-136` `capability` A signed-in reader keeps the server-side reading list whatever the `reading_memory` answer. `src: Core features rule 10`
- [ ] `C-CF-137` `literal` A privacy page exists at `/privacy`. `src: Core features rule 11`
- [ ] `C-CF-138` `capability` The footer of every public page links to `/privacy`. `src: Core features rule 11`
- [ ] `C-CF-139` `capability` The privacy page lists, for a reader account, the email, a hashed password, the reading list with positions, the motion level. `src: Core features rule 11`
- [ ] `C-CF-140` `capability` The privacy page lists, for an allowing browser, reading positions, the motion level, the tilt answer, the work index sort plus view. `src: Core features rule 11`
- [ ] `C-CF-141` `capability` The privacy page carries the pinned sentence saying the site keeps no analytics. `src: Core features rule 11`
- [ ] `C-CF-142` `capability` Every internal link on every public page leads to a page that answers. `src: Core features rule 12`
- [ ] `C-CF-143` `capability` Every chapter anchor link on a public page resolves to a chapter. `src: Core features rule 12`
- [ ] `C-CF-144` `capability` An anonymous request for `/reading-list` lands on `/login`. `src: Core features rule 12`
- [ ] `C-CF-145` `ui` Signup, sign-in, the case-study form, the chapter form reject invalid input with an error directly under the field. `src: Core features rule 13`
- [ ] `C-CF-146` `constraint` A form rejecting invalid input writes nothing. `src: Core features rule 13`
- [ ] `C-CF-147` `literal` An invalid API request is rejected as a client error whose body carries `field`. `src: Core features rule 13`
- [ ] `C-CF-148` `ui` `/studio` lists every case study on the left with the word `Published` or `Draft`. `src: Core features rule 14`
- [ ] `C-CF-149` `ui` `/studio` shows the selected case study's detail on the right. `src: Core features rule 14`
- [ ] `C-CF-150` `ui` The studio previews a draft through the public templates. `src: Core features rule 14`
- [ ] `C-CF-151` `literal` Creating a case study opens the route `/studio/case-studies/new`. `src: Core features rule 14`
- [ ] `C-CF-152` `capability` A new case study is always created as a draft. `src: Core features rule 14`
- [ ] `C-CF-153` `ui` A save answers with the banner `Saved as a draft.` at the top of the detail pane. `src: Core features rule 14`
- [ ] `C-CF-154` `ui` A publish answers with the pinned published banner naming the case study's own slug. `src: Core features rule 14`
- [ ] `C-CF-155` `ui` A withdrawal answers with the pinned withdrawn banner naming the case study's own slug. `src: Core features rule 14`
- [ ] `C-CF-156` `role` Every studio route plus every studio write is refused to an anonymous visitor or a `reader`. `src: Core features rule 14`
- [ ] `C-CF-157` `capability` Every response carries a strict transport security header. `src: Core features rule 15`
- [ ] `C-CF-158` `literal` Every response carries the content-type options header set to `nosniff`. `src: Core features rule 15`
- [ ] `C-CF-159` `literal` A refused publish names `field` as `hero`, `alt_text` or `chapters`. `src: Core features rule 3`
- [ ] `C-CF-160` `ui` The refused publish banner reads the pinned sentence for the missing piece. `src: Core features rule 3`
- [ ] `C-CF-161` `ui` An inline form error names the offending field. `src: Core features rule 13`
- [ ] `C-CF-162` `literal` A new case study's `home_placement` defaults to `list`, with `position` after the last case study in that placement. `src: Core features rule 14`
- [ ] `C-CF-163` `literal` The studio top bar carries `Case studies`, `New case study`, `View site`, `Sign out`. `src: Core features rule 14`

## C-UF User flow

- [ ] `C-UF-01` `literal` The route `/` serves the seven-band home page. `src: User flow table row 1`
- [ ] `C-UF-02` `literal` The home page carries the anchors `#hero`, `#featured`, `#about`, `#contact`. `src: User flow table row 1`
- [ ] `C-UF-03` `literal` The eleven published case studies answer at `/verity-biotics-product`, `/verity-biotics-brand`, `/aging-model`, `/kestra-care`, `/kestra-home`, `/foundry-campaign`, `/foundry-dashboard`, `/mirror-lab`, `/dusk-ritual`, `/quitkit` plus the scoring-feature slug. `src: User flow table row 2`
- [ ] `C-UF-04` `literal` The route `/work` serves the work index. `src: User flow table row 3`
- [ ] `C-UF-05` `literal` The route `/privacy` serves what the site keeps. `src: User flow table row 4`
- [ ] `C-UF-06` `literal` The route `/reading-list` serves saved case studies to a signed-in account. `src: User flow table row 5`
- [ ] `C-UF-07` `literal` The routes `/login` plus `/signup` serve sign-in plus reader creation. `src: User flow table row 6`
- [ ] `C-UF-08` `literal` The routes `/studio` plus `/studio/case-studies/{id}` serve the designer only. `src: User flow table rows 7, 9`
- [ ] `C-UF-09` `capability` Any unknown address answers the site's own not-found page with a not-found status. `src: User flow table row 10`
- [ ] `C-UF-10` `literal` The home top bar carries `Intro`, `Work`, `About`, `Contact`. `src: User flow, entry and redirects`
- [ ] `C-UF-11` `capability` The `Work` item targets `#featured`, not the work list. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `capability` An anonymous studio or reading-list request lands on `/login`, returning to the requested page after sign-in. `src: User flow, entry and redirects`
- [ ] `C-UF-13` `ui` A `reader` requesting a studio route sees a refusal with no studio content. `src: User flow, entry and redirects`
- [ ] `C-UF-14` `capability` Signing out returns to `/`. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `capability` A session expiring mid-action sends the visitor to `/login` without applying the action. `src: User flow, entry and redirects`
- [ ] `C-UF-16` `capability` Pressing `Save to reading list` when signed out goes to `/login`, saving nothing. `src: User flow, entry and redirects`
- [ ] `C-UF-17` `literal` A case-study slug may never be `work`, `reading-list`, `privacy`, `login`, `signup`, `studio`, `api`. `src: User flow, entry and redirects`
- [ ] `C-UF-18` `ui` The prospective client journey runs from the home page through `See all eleven` to a filtered case study. `src: User flow, the prospective client`
- [ ] `C-UF-19` `literal` The returning reader sees `You were in The platform.` on opening `/kestra-care`. `src: User flow, the returning reader`
- [ ] `C-UF-20` `ui` The saving reader finds a saved entry with progress on `/reading-list` from another device. `src: User flow, the reader who saves`
- [ ] `C-UF-21` `ui` Choosing `Nothing` from the slider icon holds the stillness across a reload. `src: User flow, the visitor who wants stillness`
- [ ] `C-UF-22` `ui` The designer's published case study appears on `/` plus at `/work`. `src: User flow, the designer publishes`
- [ ] `C-UF-23` `ui` After a withdrawal the home list renumbers from `01` with no gap. `src: User flow, the designer withdraws`
- [ ] `C-UF-24` `capability` The work index empty state shows the pinned sentence about two filters matching nothing. `src: User flow, states`
- [ ] `C-UF-25` `literal` The work index empty state offers a `Clear filters` chip. `src: User flow, states`
- [ ] `C-UF-26` `ui` The work index empty state keeps the heading plus the filter bar. `src: User flow, states`
- [ ] `C-UF-27` `capability` An ignored parameter shows the pinned sentence about a dropped filter. `src: User flow, states`
- [ ] `C-UF-28` `ui` The reading list empty state shows the pinned sentence about nothing saved yet. `src: User flow, states`
- [ ] `C-UF-29` `ui` A route with no annotations shows the pinned no-explanation sentence in the preferences panel. `src: User flow, states`
- [ ] `C-UF-30` `ui` Every error shows as a message on the page, never a crash. `src: User flow, states`
- [ ] `C-UF-31` `ui` Typing `work` as the slug shows the pinned message directly under the slug field. `src: User flow, the designer publishes`
- [ ] `C-UF-32` `ui` A `reader` requesting a studio route sees the pinned studio refusal. `src: User flow, entry and redirects`
- [ ] `C-UF-33` `ui` The work index shows no loading state, filtering immediately. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The site reads as an editorial reading room with the subject seen first. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` Every ground is a near-black neutral, with hierarchy carried by brightness alone. `src: UI/UX notes, palette by role`
- [ ] `C-UX-03` `ui` The hero, philosophy, about, punchline bands sit one step lighter than the page. `src: UI/UX notes, palette by role`
- [ ] `C-UX-04` `ui` The palette chips on brand routes sit a step darker than the page. `src: UI/UX notes, palette by role`
- [ ] `C-UX-05` `ui` The work band is the one surface with a trace of warmth. `src: UI/UX notes, palette by role`
- [ ] `C-UX-06` `ui` The home route's accent is a near-white warm neutral, warmer than the case-study accent. `src: UI/UX notes, palette by role`
- [ ] `C-UX-07` `ui` The light vivid green plus the near-white soft blue appear only inside the frosted cards. `src: UI/UX notes, palette by role`
- [ ] `C-UX-08` `ui` The chrome carries no accent, no brand hue, no success or error colour. `src: UI/UX notes, palette by role`
- [ ] `C-UX-09` `ui` No link shows the browser's default blue as text or border. `src: UI/UX notes, palette by role`
- [ ] `C-UX-10` `ui` A display serif carries the brand in italic, a neo-grotesque carries body, a mono carries labels. `src: UI/UX notes, type`
- [ ] `C-UX-11` `ui` Editorial type scales with the window; functional type holds its size. `src: UI/UX notes, type`
- [ ] `C-UX-12` `ui` The hero name is larger on a tablet than on a laptop. `src: UI/UX notes, type`
- [ ] `C-UX-13` `ui` Bands read spacious, with the punchline alone in the emptiest band. `src: UI/UX notes, density and shape`
- [ ] `C-UX-14` `ui` Nothing moves on its own except the five muted films carried by five of the nine hero tiles. `src: UI/UX notes, motion`
- [ ] `C-UX-15` `ui` Movement uses three curves: glide-in, a small overshoot for acknowledgements, slow-fast-slow for the fanning films. `src: UI/UX notes, motion`
- [ ] `C-UX-16` `ui` Durations form a ladder from pointer-following up to the portrait's warm-up. `src: UI/UX notes, motion`
- [ ] `C-UX-17` `ui` Pictures never rest at full brightness. `src: UI/UX notes, motion`
- [ ] `C-UX-18` `ui` The portrait is the only fully grey image, warming into colour on hover. `src: UI/UX notes, motion`
- [ ] `C-UX-19` `ui` The reel's play control is the only element growing under the pointer. `src: UI/UX notes, motion`
- [ ] `C-UX-20` `constraint` Navigation has no page transition. `src: UI/UX notes, motion`
- [ ] `C-UX-21` `ui` Case-study copy arrives already at full contrast. `src: UI/UX notes, motion`
- [ ] `C-UX-22` `ui` The layout holds at every viewport width across desktop, tablet, phone. `src: UI/UX notes, responsive`
- [ ] `C-UX-23` `ui` No hamburger, drawer or overflow menu appears at any width. `src: UI/UX notes, responsive`
- [ ] `C-UX-24` `ui` Every text that has to be read meets WCAG AA contrast against its ground. `src: UI/UX notes, accessibility`
- [ ] `C-UX-25` `ui` The rail labels at rest, the two corner links, the tilt decline are raised to a light neutral. `src: UI/UX notes, accessibility`
- [ ] `C-UX-26` `ui` Full keyboard navigation reaches every control with a visible focus ring in the primary ink. `src: UI/UX notes, accessibility`
- [ ] `C-UX-27` `ui` The icon-only links carry labels that exist for the keyboard even when unpainted. `src: UI/UX notes, accessibility`
- [ ] `C-UX-28` `ui` Split passages keep the whole sentence as accessible text, hiding the individual letters. `src: UI/UX notes, accessibility`
- [ ] `C-UX-29` `ui` Hero films are decorative, silent, with every player showing the poster first. `src: UI/UX notes, accessibility`
- [ ] `C-UX-30` `ui` Meaning is never carried by colour alone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-31` `ui` Hairlines plus dividers are a deep neutral. `src: UI/UX notes, palette by role`
- [ ] `C-UX-32` `ui` The mail link plus `[ EMAIL ]` rest at the primary ink, brightening to the pure near-white on hover. `src: UI/UX notes, palette by role`
- [ ] `C-UX-33` `ui` Corners across the site are almost square. `src: UI/UX notes, density and shape`
- [ ] `C-UX-34` `ui` Every control has a comfortable touch target on a phone. `src: UI/UX notes, accessibility`
- [ ] `C-UX-35` `ui` A field's error sits directly under the field. `src: UI/UX notes, components`
- [ ] `C-UX-36` `ui` Every frosted card plus the preferences panel close on `Escape`, returning focus. `src: UI/UX notes, components`
- [ ] `C-UX-37` `ui` `Withdraw` asks once before acting. `src: UI/UX notes, components`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` An annotation naming a missing record or constant renders nothing. `src: Front-end specification, overlays`
- [ ] `C-FE-02` `ui` On a phone the featured grid becomes four tall cards with pictures sliding inside their frames. `src: Front-end specification, the home page`
- [ ] `C-FE-03` `ui` On a phone the work list becomes a plain list with thumbnails. `src: Front-end specification, the home page`
- [ ] `C-FE-04` `ui` On a phone the chapter rail gives way to a filling hairline under the chrome. `src: Front-end specification, chrome`
- [ ] `C-FE-05` `ui` Ten grounds run from the palette chip ground up to the nav meter track. `src: Front-end specification, grounds`
- [ ] `C-FE-06` `ui` The frosted card carries a wide soft drop plus a hairline inset highlight along the top edge. `src: Front-end specification, grounds`
- [ ] `C-FE-07` `ui` The home route's accent plus heading stack differ from the case-study routes'. `src: Front-end specification, grounds`
- [ ] `C-FE-08` `constraint` No transition is declared on every property of every element. `src: Front-end specification, grounds`
- [ ] `C-FE-09` `literal` The display face is `PPEditorialNew` with fallback `"Times New Roman", Georgia, serif`. `src: Front-end specification, type`
- [ ] `C-FE-10` `literal` The heading plus body face is `PPNeueMontreal` with fallback `sans-serif`. `src: Front-end specification, type`
- [ ] `C-FE-11` `literal` Labels use `Courier New` with fallback `Courier, monospace`. `src: Front-end specification, type`
- [ ] `C-FE-12` `ui` Without the display face the italic serif fallback stands in at the same sizes. `src: Front-end specification, type`
- [ ] `C-FE-13` `literal` Section headings render at `800`. `src: Front-end specification, type`
- [ ] `C-FE-14` `literal` The hero name renders `72px` at desktop, `99px` at 990 wide. `src: Front-end specification, type`
- [ ] `C-FE-15` `literal` The article body renders `16px`, falling to `14.08px` on a phone. `src: Front-end specification, type`
- [ ] `C-FE-16` `literal` Body copy uses a `1.8` line ratio; the article body uses `1.85`. `src: Front-end specification, type`
- [ ] `C-FE-17` `ui` The type ladder follows the listed sizes with the listed viewport rates. `src: Front-end specification, type`
- [ ] `C-FE-18` `ui` Seven marks are inline drawings inheriting the text colour, with no icon font or file. `src: Front-end specification, iconography`
- [ ] `C-FE-19` `ui` Each discipline mark primitive carries its own strength, lit from above on the systems mark. `src: Front-end specification, iconography`
- [ ] `C-FE-20` `constraint` The `Product` card plus the `Spatial Experiences` card carry no mark. `src: Front-end specification, iconography`
- [ ] `C-FE-21` `ui` The name at the top left sits at seven tenths strength behind the nav items. `src: Front-end specification, chrome`
- [ ] `C-FE-22` `ui` Each nav item's track fills as the visitor moves through the item's section. `src: Front-end specification, chrome`
- [ ] `C-FE-23` `literal` The top bar marks carry the labels `Email`, `Network`, plus the preferences mark. `src: Front-end specification, chrome`
- [ ] `C-FE-24` `ui` On a phone the name leaves the top bar, with the nav moving to the left gutter. `src: Front-end specification, chrome`
- [ ] `C-FE-25` `literal` The case-study chrome carries `Back to portfolio`, `Case Study`, the save control, the preferences mark. `src: Front-end specification, chrome`
- [ ] `C-FE-26` `literal` The save control reads `Save to reading list`, then `Saved`. `src: Front-end specification, chrome`
- [ ] `C-FE-27` `ui` A small pale cursor dot follows fine pointers, absent on coarse pointers or at `Nothing`. `src: Front-end specification, chrome`
- [ ] `C-FE-28` `ui` Pointing at a work-list row lifts one preview image that follows the pointer. `src: Front-end specification, chrome`
- [ ] `C-FE-29` `literal` The case-study footer reads `All rights reserved` beside the `Privacy` link. `src: Front-end specification, chrome`
- [ ] `C-FE-30` `capability` One scroll source feeds every scroll-driven effect. `src: Front-end specification, motion runtime`
- [ ] `C-FE-31` `ui` At tablet plus desktop widths the scroll glides to a stop. `src: Front-end specification, motion runtime`
- [ ] `C-FE-32` `capability` Anchor jumps, restored positions, resume jumps all go through the smoothing layer. `src: Front-end specification, motion runtime`
- [ ] `C-FE-33` `constraint` No scroll handler writes to an element without a layout box. `src: Front-end specification, motion runtime`
- [ ] `C-FE-34` `ui` Every animated subsystem shows the listed still state at `Nothing`. `src: Front-end specification, still-state table`
- [ ] `C-FE-35` `ui` Each subsystem behaves as the level table lists at `Everything`, `Less`, `Nothing`. `src: Front-end specification, level table`
- [ ] `C-FE-36` `ui` The hero holds nine tiles, four cropped at rest by the window edges. `src: Front-end specification, the hero`
- [ ] `C-FE-37` `literal` The tile rates are middle centre `1.10`, middle left `0.90`, middle right `0.75`, top centre `0.60`, bottom centre `0.50`, bottom left `0.40`, top right `0.35`, top left `0.30`, bottom right `0.25`. `src: Front-end specification, the hero`
- [ ] `C-FE-38` `ui` Each tile chases the tile's target, settling a beat after scrolling stops. `src: Front-end specification, the hero`
- [ ] `C-FE-39` `ui` The hero name inverts as tiles pass behind the name. `src: Front-end specification, the hero`
- [ ] `C-FE-40` `literal` Under the hero name sit `Founder`, `Designer`, `Artist`. `src: Front-end specification, the hero`
- [ ] `C-FE-41` `literal` The first hero sub line reads `I build experiences at the intersection`. `src: Front-end specification, the hero`
- [ ] `C-FE-42` `ui` A transparent full-window rendering surface sits over the home bands, never needed for reading. `src: Front-end specification, the hero`
- [ ] `C-FE-43` `capability` On a phone the hero tiles are stills only. `src: Front-end specification, the hero`
- [ ] `C-FE-44` `ui` The tilt gate shows the pinned title about the site moving with the visitor. `src: Front-end specification, the hero`
- [ ] `C-FE-45` `literal` The tilt gate offers `Enable Motion` over `Skip` at equal legibility. `src: Front-end specification, the hero`
- [ ] `C-FE-46` `ui` The tilt gate footer names the preferences panel as the place to change the answer. `src: Front-end specification, the hero`
- [ ] `C-FE-47` `capability` The tilt gate renders only where device orientation exists behind a permission. `src: Front-end specification, the hero`
- [ ] `C-FE-48` `ui` Lit passage characters rest dim, lighting up by the squared progress law. `src: Front-end specification, lit passages`
- [ ] `C-FE-49` `literal` The philosophy window is `18.27` characters; the about window is `6.44`. `src: Front-end specification, lit passages`
- [ ] `C-FE-50` `ui` Highlighted words switch to the italic display serif as whole words. `src: Front-end specification, lit passages`
- [ ] `C-FE-51` `capability` Finding a phrase spanning two characters in a split passage still matches. `src: Front-end specification, lit passages`
- [ ] `C-FE-52` `literal` No more than `64` elements carry a compositing hint at any moment. `src: Front-end specification, lit passages`
- [ ] `C-FE-53` `ui` Section heading letters settle with the ends landing first. `src: Front-end specification, settling heading`
- [ ] `C-FE-54` `literal` The letter amplitude is `40`. `src: Front-end specification, settling heading`
- [ ] `C-FE-55` `literal` The philosophy band carries the label `What I Do`. `src: Front-end specification, the home page band 2`
- [ ] `C-FE-56` `literal` The five discipline cards are `Strategy`, `Product`, `Brand & Creative`, `Spatial Experiences`, `Systems`. `src: Front-end specification, the home page band 2`
- [ ] `C-FE-57` `ui` Each discipline card lists the items the brief gives for the card. `src: Front-end specification, the home page band 2`
- [ ] `C-FE-58` `ui` The discipline card hover is the only ground change on the home page. `src: Front-end specification, the home page band 2`
- [ ] `C-FE-59` `literal` The featured band carries `From Idea to Reality` over `Featured Work`. `src: Front-end specification, the home page band 3`
- [ ] `C-FE-60` `capability` The four published `featured` case studies fill the featured band in position order. `src: Front-end specification, the home page band 3`
- [ ] `C-FE-61` `ui` Each featured card shows a dimmed image, the index title, the client label, the years. `src: Front-end specification, the home page band 3`
- [ ] `C-FE-62` `literal` The work band carries `Selected work` with a trailing link reading `See all eleven` for the seeded set. `src: Front-end specification, the home page band 4`
- [ ] `C-FE-63` `capability` The work list numbers published `list` case studies from `01` in position order. `src: Front-end specification, the home page band 4`
- [ ] `C-FE-64` `ui` Each work row shows the index title large but dim beside a middle-dot tag line. `src: Front-end specification, the home page band 4`
- [ ] `C-FE-65` `ui` Work rows enter once, the first two in place, the rest following one after another. `src: Front-end specification, the home page band 4`
- [ ] `C-FE-66` `literal` The about band carries `Beyond the Brief` over `About Me`. `src: Front-end specification, the home page band 5`
- [ ] `C-FE-67` `literal` The first about paragraph names `Thanjavur` as the `place` card trigger. `src: Front-end specification, the home page band 5`
- [ ] `C-FE-68` `literal` The roles block lists `Verity Biotics` then `Kestra` under `What I've Been Building`. `src: Front-end specification, the home page band 5`
- [ ] `C-FE-69` `ui` Rendered date ranges use a typographic dash. `src: Front-end specification, the home page band 5`
- [ ] `C-FE-70` `ui` The punchline sits alone under a large faint open-quote glyph. `src: Front-end specification, the home page band 6`
- [ ] `C-FE-71` `literal` The contact band carries `Always curious about new ideas.` with `hello@marisol.example.com`. `src: Front-end specification, the home page band 7`
- [ ] `C-FE-72` `literal` The contact band stacks `[ EMAIL ]` over `[ NETWORK ]`. `src: Front-end specification, the home page band 7`
- [ ] `C-FE-73` `literal` The network action links to `https://network.example.com/in/marisol-andrade`. `src: Front-end specification, the home page band 7`
- [ ] `C-FE-74` `ui` The closing name is drawn wider than the window, cropped at both edges at every width. `src: Front-end specification, the home page band 7`
- [ ] `C-FE-75` `ui` The copyright line names `Marisol Andrade` with the year 2026. `src: Front-end specification, the home page band 7`
- [ ] `C-FE-76` `ui` The `Carry on` band sits between the featured band plus the work band. `src: Front-end specification, the home page`
- [ ] `C-FE-77` `literal` The `Carry on` band offers `Forget my place` to clear all reading state. `src: Front-end specification, the home page`
- [ ] `C-FE-78` `capability` The rail marks exactly one chapter current, the one whose top most recently passed a fixed line. `src: Front-end specification, case studies`
- [ ] `C-FE-79` `ui` The rail is absent on a phone. `src: Front-end specification, case studies`
- [ ] `C-FE-80` `capability` Rail labels plus article headings are different strings, both carried. `src: Front-end specification, case studies`
- [ ] `C-FE-81` `ui` A product case study hero shows a meta row of three label-value pairs. `src: Front-end specification, case studies`
- [ ] `C-FE-82` `literal` Callout labels are `The idea`, `The workflow`, `The insight`, `User response`, `The real output`, `The Experience`, `User Story`, `AI coach in action`. `src: Front-end specification, case studies`
- [ ] `C-FE-83` `ui` The evidence card shows seven slots with a rule between claim plus method. `src: Front-end specification, case studies`
- [ ] `C-FE-84` `ui` The insight card's outlined button inverts fully on hover. `src: Front-end specification, case studies`
- [ ] `C-FE-85` `ui` Inline image captions stay aligned to the image rather than the text column. `src: Front-end specification, case studies`
- [ ] `C-FE-86` `literal` The more block's `See all` link goes to `/work`. `src: Front-end specification, case studies`
- [ ] `C-FE-87` `ui` A brand case study shows story blocks, highlights, palette chips, a type specimen, full-bleed images. `src: Front-end specification, case studies`
- [ ] `C-FE-88` `literal` Brand story labels are `The foundation`, `The brief`, `The idea`. `src: Front-end specification, case studies`
- [ ] `C-FE-89` `ui` The reel shows only play at rest, revealing pause plus restart on playback. `src: Front-end specification, case studies media`
- [ ] `C-FE-90` `ui` The pointed trio item takes space from the other two, the row keeping the same width. `src: Front-end specification, case studies media`
- [ ] `C-FE-91` `capability` Each product route carries the anchors, rail labels, headings in the chapter table. `src: Front-end specification, chapter table`
- [ ] `C-FE-92` `literal` The first `/verity-biotics-product` chapter pairs the rail label `The belief` with `The belief we started with`. `src: Front-end specification, chapter table`
- [ ] `C-FE-93` `literal` `/foundry-campaign` starts at `s4`, reachable at `/foundry-campaign#s4`, with no `s1`. `src: Front-end specification, chapter table`
- [ ] `C-FE-94` `capability` Each case study carries the title, summary, opening quote of the titles table. `src: Front-end specification, titles table`
- [ ] `C-FE-95` `literal` The `/quitkit` highlights include `Bold type. Minimal colour. Maximum presence.` `src: Front-end specification, highlight statements`
- [ ] `C-FE-96` `capability` Each case study carries the catalogue values of the catalogue table. `src: Front-end specification, catalogue table`
- [ ] `C-FE-97` `literal` Client labels are `Verity Biotics`, `Kestra`, `Mirror Lab`, `Dusk Ritual`, `Quitkit`. `src: Front-end specification, catalogue`
- [ ] `C-FE-98` `literal` Discipline labels are `Strategy`, `Product`, `Brand & Creative`, `Systems`, `Spatial Experience`. `src: Front-end specification, catalogue`
- [ ] `C-FE-99` `capability` Filter chips show only values carried by at least one published case study. `src: Front-end specification, catalogue`
- [ ] `C-FE-100` `ui` The filter bar carries the pinned label over the pinned client group plus discipline group names. `src: Front-end specification, the work index`
- [ ] `C-FE-101` `literal` The sort chips read `Newest first`, `Oldest first`, `By name`. `src: Front-end specification, the work index`
- [ ] `C-FE-102` `literal` The view chips read `Grid`, `List`. `src: Front-end specification, the work index`
- [ ] `C-FE-103` `literal` The work index count reads `11 projects` for the seeded set, `1 project` for one. `src: Front-end specification, the work index`
- [ ] `C-FE-104` `ui` A pressed chip inverts fully with a small overshooting acknowledgement. `src: Front-end specification, the work index`
- [ ] `C-FE-105` `ui` The list view shows the year at the right in mono. `src: Front-end specification, the work index`
- [ ] `C-FE-106` `ui` All frosted cards share one shell, one open at a time. `src: Front-end specification, overlays`
- [ ] `C-FE-107` `literal` The `place` card shows `Pronounced as` over `City in Tirunelveli, Placeland`. `src: Front-end specification, overlays`
- [ ] `C-FE-108` `literal` The `place` card shows `11.0000 N` beside `76.0000 E`. `src: Front-end specification, overlays`
- [ ] `C-FE-109` `literal` The `mechanism` card eyebrow reads `// under the hood`. `src: Front-end specification, overlays`
- [ ] `C-FE-110` `ui` Cards open on hover intent, tap, focus, closing on leave, tap outside, blur, `Escape`. `src: Front-end specification, overlays`
- [ ] `C-FE-111` `ui` A card never covers its own trigger. `src: Front-end specification, overlays`
- [ ] `C-FE-112` `literal` The preferences panel asks `How much should move?` above `Everything`, `Less`, `Nothing`. `src: Front-end specification, preferences panel`
- [ ] `C-FE-113` `ui` The preferences panel footer says where the setting is kept. `src: Front-end specification, preferences panel`
- [ ] `C-FE-114` `literal` The reveal-all switch reads `Show what is explained`. `src: Front-end specification, preferences panel`
- [ ] `C-FE-115` `literal` The resume card offers `Take me back` beside `Start again`. `src: Front-end specification, resume card`
- [ ] `C-FE-116` `capability` The resume card takes focus only when the reader has not scrolled. `src: Front-end specification, resume card`
- [ ] `C-FE-117` `ui` The browser question card carries the pinned eyebrow, title, body, two buttons. `src: Front-end specification, browser question`
- [ ] `C-FE-118` `ui` `Back to portfolio`, `See all`, the rail labels rise to the light secondary tone. `src: Front-end specification, accessibility details`
- [ ] `C-FE-119` `ui` Every hover change has a keyboard-focus equivalent. `src: Front-end specification, accessibility details`
- [ ] `C-FE-120` `ui` Filter chips report the pressed state, with the count announced politely. `src: Front-end specification, accessibility details`
- [ ] `C-FE-121` `ui` The site shows each glossary effect as the glossary describes the effect. `src: Front-end specification, terms used in this brief`
- [ ] `C-FE-122` `ui` Each still is a seeded gradient with a soft highlight plus grain in the real image's box. `src: Front-end specification, generating every asset`
- [ ] `C-FE-123` `ui` Playing a player runs a twelve-second generated loop with full controls. `src: Front-end specification, generating every asset`
- [ ] `C-FE-124` `ui` The site reads correctly on the fallback font stacks alone. `src: Front-end specification, generating every asset`
- [ ] `C-FE-125` `capability` The app writes each seeded case study's generated `hero` to the bucket on first start. `src: Front-end specification, generating every asset`
- [ ] `C-FE-126` `capability` A generated hero's alternative text is the case study's index title. `src: Front-end specification, generating every asset`
- [ ] `C-FE-127` `ui` Inks step down from the pure near-white of the hero name to the decorative minimum in the listed order. `src: Front-end specification, grounds`
- [ ] `C-FE-128` `constraint` The frosted card shadow is the only shadow on the site. `src: Front-end specification, grounds`
- [ ] `C-FE-129` `literal` The home route font stack adds `Host Grotesk` before `sans-serif`. `src: Front-end specification, type`
- [ ] `C-FE-130` `literal` The hero name rates are `5vw`, `10vw`, `12vw`; the section heading rates are `5vw`, `5vw`, `8vw`. `src: Front-end specification, type`
- [ ] `C-FE-131` `literal` Functional sizes are `16px`, `13.6px`, `12.8px`, `10.4px`, `9.6px`, `9.92px`, `8.8px`, `8.32px`, `8px`, `7.2px`. `src: Front-end specification, type`
- [ ] `C-FE-132` `literal` Line ratios run `1.0`, `1.2`, `1.35`, `1.5`, `1.75`, `1.8`, `1.85`, `2.0` across the listed roles. `src: Front-end specification, type`
- [ ] `C-FE-133` `ui` Article emphasis steps one notch heavier plus one notch brighter, nothing else. `src: Front-end specification, type`
- [ ] `C-FE-134` `ui` Five hero tiles, top left, top centre, middle centre, bottom left, bottom right, are muted looping films; the other four are stills. `src: Front-end specification, the hero`
- [ ] `C-FE-135` `capability` Without device orientation the tiles follow the pointer. `src: Front-end specification, the hero`
- [ ] `C-FE-136` `ui` The work band link to `/work` reads `See all` followed by the published count in words. `src: Front-end specification, the home page band 4`
- [ ] `C-FE-137` `ui` A featured card picture held slightly grey plus dim warms, lifting when pointed at. `src: Front-end specification, the home page band 3`
- [ ] `C-FE-138` `ui` Each featured card writes the years as the start year plus the end year or `Active`, joined by a middle dot. `src: Front-end specification, the home page band 3`
- [ ] `C-FE-139` `literal` The product hero meta labels come from `Company` or `Brand`, `Role` or `Focus` or `Format`, `Year` or `Period`. `src: Front-end specification, case studies`
- [ ] `C-FE-140` `ui` Work index rows fade in on a result change, enter in sequence on first paint, move to new places on a sort change. `src: Front-end specification, the work index`
- [ ] `C-FE-141` `ui` At `Less` or `Nothing` work index row movement is instant. `src: Front-end specification, the work index`
- [ ] `C-FE-142` `literal` The `note` card eyebrow reads `// note`. `src: Front-end specification, overlays`
- [ ] `C-FE-143` `capability` A card closes at once when the trigger leaves the page. `src: Front-end specification, overlays`
- [ ] `C-FE-144` `ui` At `Nothing` cards appear without fade or travel. `src: Front-end specification, overlays`
- [ ] `C-FE-145` `ui` `Escape` dismisses the resume card, returning focus. `src: Front-end specification, resume card`
- [ ] `C-FE-146` `ui` The reveal-all switch announces the switch state. `src: Front-end specification, accessibility details`
- [ ] `C-FE-147` `ui` Any film with speech carries captions. `src: Front-end specification, accessibility details`
- [ ] `C-FE-148` `ui` Hover changes stay inert on a coarse pointer. `src: Front-end specification, accessibility details`
- [ ] `C-FE-149` `ui` Discipline marks are hidden from assistive technology. `src: Front-end specification, iconography`
- [ ] `C-FE-150` `literal` The `/verity-biotics-product` chapters run `s1` to `s5` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-151` `literal` The `/kestra-care` chapters run `s1` to `s6` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-152` `literal` The `/mirror-lab` chapters run `s1` to `s5` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-153` `literal` The `/aging-model` chapters run `s1` to `s3` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-154` `literal` The scoring-feature route chapters run `s1` to `s4` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-155` `literal` The `/kestra-home` chapters run `s1` to `s7` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-156` `literal` The `/foundry-campaign` chapters run `s4` to `s8` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-157` `literal` The `/foundry-dashboard` chapters run `s1` to `s7` with the pinned rail labels plus headings. `src: Front-end specification, chapter table`
- [ ] `C-FE-158` `literal` `verity-biotics-product` carries index title `Designing Trust in Preventive Health`, client `verity-biotics`, product `The Body Ledger`, disciplines `strategy`, `product`, from `2022`, `Active`, template product, placement featured 1. `src: Front-end specification, catalogue table`
- [ ] `C-FE-159` `literal` `kestra-care` carries index title `Turning Disconnected Health Data Into Daily Decisions`, client `kestra`, product `Kestra Care`, disciplines `strategy`, `product`, years `2020` to `2023`, template product, placement featured 2. `src: Front-end specification, catalogue table`
- [ ] `C-FE-160` `literal` `kestra-home` carries index title `The Smart Home Built For Placeland`, client `kestra`, product `Kestra Home`, disciplines `strategy`, `product`, years `2015` to `2021`, template product, placement featured 3. `src: Front-end specification, catalogue table`
- [ ] `C-FE-161` `literal` `mirror-lab` carries index title `A Retail Experience That Turns Health Into Action`, client `mirror-lab`, no product, disciplines `brand-creative`, `spatial-experience`, from `2025`, `Active`, template product, placement featured 4. `src: Front-end specification, catalogue table`
- [ ] `C-FE-162` `literal` `verity-biotics-brand` carries index title `Where Art Meets Science`, client `verity-biotics`, no product, disciplines `brand-creative`, year `2022`, template brand, placement list 1. `src: Front-end specification, catalogue table`
- [ ] `C-FE-163` `literal` `aging-model` carries index title `Beyond Biological Age`, client `verity-biotics`, product `The Body Ledger`, disciplines `product`, year `2023`, template product, placement list 2. `src: Front-end specification, catalogue table`
- [ ] `C-FE-164` `literal` `foundry-campaign` carries index title `Using AI to Build a Creative System`, client `verity-biotics`, product `Foundry`, disciplines `brand-creative`, `systems`, year `2024`, template product, placement list 3. `src: Front-end specification, catalogue table`
- [ ] `C-FE-165` `literal` `foundry-dashboard` carries index title `Using AI to Rethink the Way We Build`, client `verity-biotics`, product `Foundry`, disciplines `product`, `systems`, year `2025`, template product, placement list 4. `src: Front-end specification, catalogue table`
- [ ] `C-FE-166` `literal` The scoring-feature slug carries index title `Making Health Scores Work`, client `kestra`, the pinned scoring product, disciplines `product`, year `2021`, template product, placement list 5. `src: Front-end specification, catalogue table`
- [ ] `C-FE-167` `literal` `dusk-ritual` carries index title `Designing a Brand for Better Sleep`, client `dusk-ritual`, no product, disciplines `brand-creative`, year `2024`, template brand, placement list 6. `src: Front-end specification, catalogue table`
- [ ] `C-FE-168` `literal` `quitkit` carries index title `Quit Like a Badass. Not a Patient.`, client `quitkit`, no product, disciplines `brand-creative`, year `2023`, template brand, placement list 7. `src: Front-end specification, catalogue table`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every route leaves the server as finished markup. `src: Technical requirements para 1`
- [ ] `C-TR-02` `literal` The front end is `Alpine.js` over server-rendered templates. `src: Technical requirements para 1`
- [ ] `C-TR-03` `literal` The backend plus HTTP API are `Flask` with `Jinja`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `capability` Without scripting the home page plus `/work` still list every published case study. `src: Technical requirements para 1`
- [ ] `C-TR-05` `literal` Records go into `PostgreSQL` found at `DATABASE_URL`. `src: Technical requirements para 2`
- [ ] `C-TR-06` `literal` Images go into `minio` at `STORAGE_ENDPOINT`, bucket `STORAGE_BUCKET`. `src: Technical requirements para 2`
- [ ] `C-TR-07` `literal` The object store key pair comes from `STORAGE_ACCESS_KEY` plus `STORAGE_SECRET_KEY`. `src: Technical requirements para 2`
- [ ] `C-TR-08` `contract` Passwords are stored hashed. `src: Technical requirements para 2`
- [ ] `C-TR-09` `literal` Sign-in returns an `access_token`, also setting the same session as an HttpOnly, Secure cookie. `src: Technical requirements para 2`
- [ ] `C-TR-10` `contract` Each handled request writes a single line to stdout. `src: Technical requirements para 2`
- [ ] `C-TR-11` `constraint` No second database, cache, queue, object store, identity provider, mail vendor is introduced. `src: Technical requirements para 3`
- [ ] `C-TR-12` `contract` Hosts, ports, keys, passwords come from environment variables. `src: Technical requirements para 3`
- [ ] `C-TR-13` `literal` Every response carries `Strict-Transport-Security`. `src: Technical requirements, security headers`
- [ ] `C-TR-14` `literal` Every response carries `X-Content-Type-Options: nosniff`. `src: Technical requirements, security headers`
- [ ] `C-TR-15` `capability` Media bytes reach a browser only through the app, streamed to anyone for a published case study. `src: Technical requirements, media serving`
- [ ] `C-TR-16` `role` Draft media bytes stream only to the `designer`. `src: Technical requirements, media serving`
- [ ] `C-TR-17` `constraint` No presigned address for a draft's media is issued to anyone but the designer. `src: Technical requirements, media serving`
- [ ] `C-TR-18` `capability` Anonymous state lives under one stored envelope with one version number. `src: Technical requirements, nothing identifying`
- [ ] `C-TR-19` `capability` A version mismatch or parse failure discards the whole envelope. `src: Technical requirements, nothing identifying`
- [ ] `C-TR-20` `capability` Envelope writes are spaced at least half a second apart, flushed on page hide. `src: Technical requirements, nothing identifying`
- [ ] `C-TR-21` `constraint` No server credential, key or token appears in anything the browser downloads. `src: Technical requirements, nothing identifying`
- [ ] `C-TR-22` `constraint` The running site calls nothing outside the environment, carrying no analytics. `src: Technical requirements, nothing identifying`
- [ ] `C-TR-23` `capability` Every tile shows the tile's still at once, swapping to film only when ready. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-24` `constraint` A tile outside the window has no film attached. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-25` `constraint` Below the tablet edge or at `Less` or `Nothing` no film is attached. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-26` `capability` Every image plus film reserves the box before the bytes arrive. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-27` `capability` All scroll-driven work runs in one frame loop per page. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-28` `literal` Script on the home route stays under `805,638` bytes. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-29` `capability` The product stays responsive with a few thousand reading-list rows. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-30` `capability` Without scripting every case study still shows the chapters, headings, blocks. `src: Technical requirements para 1`
- [ ] `C-TR-31` `capability` Without scripting the three lit passages read as ordinary sentences. `src: Technical requirements para 1`
- [ ] `C-TR-32` `capability` Interactive pieces enhance the server markup rather than replacing the markup. `src: Technical requirements para 1`
- [ ] `C-TR-33` `contract` The server accepts either `Authorization: Bearer` or the session cookie. `src: Technical requirements para 2`
- [ ] `C-TR-34` `capability` Content below the first screen loads on approach. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-35` `constraint` No element carries a compositing hint at `Nothing`. `src: Technical requirements, the hero is the budget`
- [ ] `C-TR-36` `capability` A failed browser storage write lets the session carry on. `src: Technical requirements, nothing identifying`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds seven tables with UTC timestamps. `src: Data model para 1`
- [ ] `C-DM-02` `literal` Every seeded account with its password is written into `/app/USER_README.md`. `src: Data model para 2`
- [ ] `C-DM-03` `data` The `accounts` table records `id`, `email`, `password_hash`, `role`, `created_at`. `src: Data model, accounts`
- [ ] `C-DM-04` `data` An account email is unique without regard to case. `src: Data model, accounts`
- [ ] `C-DM-05` `literal` An account role is `designer` or `reader`. `src: Data model, accounts`
- [ ] `C-DM-06` `data` The `case_studies` table records `slug`, `title`, `index_title`, `template`, `client`, `year`, `published`, `published_at`. `src: Data model, case_studies`
- [ ] `C-DM-07` `data` A case study id is opaque, never derived from the title or slug. `src: Data model, case_studies`
- [ ] `C-DM-08` `data` A slug is unique, lowercase letters, digits, single hyphens, three to sixty characters. `src: Data model, case_studies`
- [ ] `C-DM-09` `data` A `year_end` is never before `year`, never set alongside `ongoing`. `src: Data model, case_studies`
- [ ] `C-DM-10` `literal` A `home_placement` is `featured` or `list`. `src: Data model, case_studies`
- [ ] `C-DM-11` `data` A `published_at` is empty before publishing, stamped on publishing. `src: Data model, case_studies`
- [ ] `C-DM-12` `constraint` The work-list number, tag line, year caption, suggestion pair are never stored. `src: Data model, case_studies`
- [ ] `C-DM-13` `data` The `case_study_disciplines` table holds at least one discipline per case study, none twice. `src: Data model, case_study_disciplines`
- [ ] `C-DM-14` `data` The `chapters` table records `anchor`, `rail_label`, `heading`, `body`, `position`. `src: Data model, chapters`
- [ ] `C-DM-15` `data` A chapter anchor is `s` followed by digits, unique within the case study. `src: Data model, chapters`
- [ ] `C-DM-16` `data` The `media` table records `role`, `object_key`, `content_type`, `byte_size`, `sha256`, `width`, `height`, `alt_text`. `src: Data model, media`
- [ ] `C-DM-17` `literal` A media role is `hero`, `still`, `poster` or `reel`. `src: Data model, media`
- [ ] `C-DM-18` `data` The `reading_list` table records `max_fraction`, `last_fraction`, `chapters_read`, `last_seen`, with `completed` computed on read. `src: Data model, reading_list`
- [ ] `C-DM-19` `data` The `reading_list` table holds one entry per account per case study. `src: Data model, reading_list`
- [ ] `C-DM-20` `data` The `preferences` table records `motion_level`, `level_source`, `reveal_all` per account. `src: Data model, preferences`
- [ ] `C-DM-21` `literal` A `level_source` is `system` or `chosen`. `src: Data model, preferences`
- [ ] `C-DM-22` `data` Choosing a motion level stores the level with `level_source` of `chosen`. `src: Data model, invariants`
- [ ] `C-DM-23` `data` Sending an empty level stores `level_source` of `system`. `src: Data model, invariants`
- [ ] `C-DM-24` `data` A reader who never chose reads back `level_source` of `system` with an empty `motion_level`. `src: Data model, invariants`
- [ ] `C-DM-25` `data` An object key is unique. `src: Data model, invariants`
- [ ] `C-DM-26` `constraint` A refused write writes no row, no partial row, no object. `src: Data model, invariants`
- [ ] `C-DM-27` `capability` The work-list numbers run from `01` with no gap, no repeat, before or after a publish. `src: Data model, invariants`
- [ ] `C-DM-28` `data` The eleven published case studies are seeded with the catalogue values. `src: Data model, seed data`
- [ ] `C-DM-29` `literal` The draft `kestra-band` is seeded with client `kestra`, discipline `product`, year `2019`, chapters `s1` to `s3`. `src: Data model, seed data`
- [ ] `C-DM-30` `data` Every seeded case study carries one generated `hero` image stored in the bucket. `src: Data model, seed data`
- [ ] `C-DM-31` `literal` The account `reader@example.com` has `kestra-care` saved with `max_fraction` of `0.4`, `last_fraction` of `0.35`. `src: Data model, seed data`
- [ ] `C-DM-32` `literal` The seeded `kestra-care` entry has `chapters_read` of `s1` plus `s2`. `src: Data model, seed data`
- [ ] `C-DM-33` `data` The account `reader2@example.com` has nothing saved. `src: Data model, seed data`
- [ ] `C-DM-34` `data` No preferences are seeded. `src: Data model, seed data`
- [ ] `C-DM-35` `constraint` Restarting the app never duplicates seeded rows. `src: Data model, seed data`
- [ ] `C-DM-36` `literal` A case study `template` is `product` or `brand`. `src: Data model, case_studies`
- [ ] `C-DM-37` `data` The `case_studies` table also records `id`, `summary`, `opening_quote`, `product`, `year_end`, `ongoing`, `home_placement`, `position`, `created_at`. `src: Data model, case_studies`
- [ ] `C-DM-38` `literal` The draft `kestra-band` is seeded with template `product`, placement `list` after the seven list case studies. `src: Data model, seed data`
- [ ] `C-DM-39` `literal` The draft `kestra-band` carries chapters `s1`, `s2`, `s3` with the pinned rail labels plus headings. `src: Data model, seed data`
- [ ] `C-DM-40` `literal` The seeded `kestra-care` entry has a `last_seen` one day before first start. `src: Data model, seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product has one designer, no team, no second tenant, no designer signup. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The product has no search, comments, likes, sharing, newsletter, chat, payment. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The product has no contact form of any kind. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` The product has no light theme, no theme switch. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` Navigating between routes is a full page load. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The product shows no cookie banner beyond the one browser question, no consent manager. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` The product has no third-party analytics, no tracking identifier, no external call at run time. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` The build ships zero binary assets, naming the licensed fonts without shipping them. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` Two discipline marks are absent rather than invented. `src: Constraints bullet 9`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `literal` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` The app serves a production build, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends, not a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-10` `literal` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-11` `contract` The app never downloads, installs, compiles or starts a copy of a backing service. `src: Deployment contract bullet 10`
- [ ] `C-DC-12` `contract` The app uses only the named providers with no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-13` `contract` The app uses no persistent volumes, no fixed container names, no custom networks. `src: Deployment contract bullet 12`
- [ ] `C-DC-14` `literal` `POST /api/auth/signup` takes `email` plus a `password` of at least `8` characters, returning the created `reader` with an `access_token`. `src: Deployment contract, API shapes row 1`
- [ ] `C-DC-15` `literal` `POST /api/auth/login` returns the account with an `access_token`. `src: Deployment contract, API shapes row 2`
- [ ] `C-DC-16` `literal` `GET /api/me` returns the signed-in account's `id`, `email`, `role`. `src: Deployment contract, API shapes row 3`
- [ ] `C-DC-17` `literal` `POST /api/consent` takes `choice` of `yes` or `no`. `src: Deployment contract, API shapes row 5`
- [ ] `C-DC-18` `literal` `GET /api/case-studies` returns `slug`, `title`, `index_title`, `client`, `product`, `disciplines`, `year`, `year_end`, `ongoing`, `template`, `home_placement` per published case study. `src: Deployment contract, API shapes row 6`
- [ ] `C-DC-19` `literal` `GET /api/case-studies/{slug}` returns `chapters` with `anchor`, `rail_label`, `heading`. `src: Deployment contract, API shapes row 7`
- [ ] `C-DC-20` `contract` The related endpoint returns exactly two published case studies, slot one first, whenever at least three are published. `src: Deployment contract, API shapes row 8`
- [ ] `C-DC-21` `literal` `GET /api/filters` returns `clients` plus `disciplines`, each entry carrying `token` with `label`. `src: Deployment contract, API shapes row 9`
- [ ] `C-DC-22` `literal` `GET /api/reading-list` returns the caller's entries newest first, each with `slug`, `title`, `saved_at`, `max_fraction`, `last_fraction`, `chapters_read`, `completed`, `last_seen`. `src: Deployment contract, API shapes row 11`
- [ ] `C-DC-23` `literal` `POST /api/reading-list` takes `slug`. `src: Deployment contract, API shapes row 12`
- [ ] `C-DC-24` `literal` `DELETE /api/reading-list/{slug}` removes the entry. `src: Deployment contract, API shapes row 13`
- [ ] `C-DC-25` `literal` `PUT /api/reading-list/{slug}/progress` takes `fraction` plus `chapters`. `src: Deployment contract, API shapes row 14`
- [ ] `C-DC-26` `literal` `PUT /api/preferences` takes `motion_level` or `reveal_all`. `src: Deployment contract, API shapes row 16`
- [ ] `C-DC-27` `literal` `GET /api/studio/case-studies` returns every case study with `id`, `slug`, `index_title`, `published`. `src: Deployment contract, API shapes row 17`
- [ ] `C-DC-28` `literal` `POST /api/studio/case-studies` returns the created case study unpublished with an `id`. `src: Deployment contract, API shapes row 18`
- [ ] `C-DC-29` `literal` `GET /api/studio/case-studies/{id}` returns a draft in full to the designer. `src: Deployment contract, API shapes row 19`
- [ ] `C-DC-30` `literal` `PATCH /api/studio/case-studies/{id}` updates an editable field. `src: Deployment contract, API shapes row 20`
- [ ] `C-DC-31` `literal` `POST /api/studio/case-studies/{id}/chapters` takes `anchor`, `rail_label`, `heading`, `body`, returning the created chapter. `src: Deployment contract, API shapes row 21`
- [ ] `C-DC-32` `literal` `DELETE /api/studio/chapters/{id}` removes a chapter. `src: Deployment contract, API shapes row 22`
- [ ] `C-DC-33` `literal` `POST /api/studio/case-studies/{id}/media` takes `file`, `role`, `alt_text`, `width`, `height`, returning the `object_key`. `src: Deployment contract, API shapes row 23`
- [ ] `C-DC-34` `literal` `POST /api/studio/case-studies/{id}/publish` publishes the case study. `src: Deployment contract, API shapes row 24`
- [ ] `C-DC-35` `literal` `POST /api/studio/case-studies/{id}/unpublish` returns the case study to draft. `src: Deployment contract, API shapes row 25`
- [ ] `C-DC-36` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes para 1`
- [ ] `C-DC-37` `contract` An invalid or unauthorized call is rejected as a client error, never a server error. `src: Deployment contract, API shapes para 1`
- [ ] `C-DC-38` `contract` A bearer token or the session cookie is required on every endpoint except signup, login, health, consent, public case-study reads, filters, media of published case studies. `src: Deployment contract, API shapes para 1`
- [ ] `C-DC-39` `contract` A draft's address plus data answer not-found to everyone but the designer. `src: Deployment contract, API shapes para 1`
- [ ] `C-DC-40` `constraint` Bytes held in memory, on the app disk, in a base64 column, or in a public bucket are a contract violation. `src: Deployment contract, No mocks para 1`
- [ ] `C-DC-41` `constraint` A signed-in reader's reading list lives in `PostgreSQL`, never in a browser-only copy. `src: Deployment contract, No mocks para 1`
- [ ] `C-DC-42` `contract` With fewer than three published case studies, the related endpoint returns every other published case study. `src: Deployment contract, API shapes row 8`
- [ ] `C-DC-43` `literal` `GET /api/case-studies` accepts optional `client`, `discipline` query parameters of comma-separated tokens, plus an optional `sort`. `src: Deployment contract, API shapes row 6`
- [ ] `C-DC-44` `literal` `GET /api/case-studies/{slug}` returns `summary`, `opening_quote`, plus `media` with `id`, `role`, `alt_text`, `width`, `height` per entry. `src: Deployment contract, API shapes row 7`
- [ ] `C-DC-45` `literal` `GET /api/preferences` returns `motion_level`, `level_source`, `reveal_all`. `src: Deployment contract, API shapes row 15`
- [ ] `C-DC-46` `literal` `POST /api/studio/case-studies` takes `slug`, `title`, `index_title`, `summary`, `template`, `client`, `disciplines`, `year`, with optional `product`, `opening_quote`, `year_end`, `ongoing`, `home_placement`, `position`. `src: Deployment contract, API shapes row 18`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `designer@example.com` | a value the brief pins | C-RL-18 | User roles table, seeded accounts row 1 |
| `designer` | a value the brief pins | C-RL-18 | User roles table, seeded accounts row 1 |
| `reader@example.com` | a value the brief pins | C-RL-19 | User roles table, seeded accounts row 2 |
| `reader` | a value the brief pins | C-RL-19 | User roles table, seeded accounts row 2 |
| `reader2@example.com` | a value the brief pins | C-RL-20 | User roles table, seeded accounts row 3 |
| `deku-demo-pw-2026` | a value the brief pins | C-RL-21 | User roles, seeded accounts |
| `A Wearable That Knew When to Stay Quiet` | a value the brief pins | C-CF-10 | Core features rule 1 |
| `/kestra-band` | a value the brief pins | C-CF-10 | Core features rule 1 |
| `case-studies/{case_study_id}/{sha256_of_bytes}.{ext}` | a value the brief pins | C-CF-14 | Core features rule 2 |
| `image/png` | a value the brief pins | C-CF-19 | Core features rule 2 |
| `image/jpeg` | a value the brief pins | C-CF-19 | Core features rule 2 |
| `image/webp` | a value the brief pins | C-CF-19 | Core features rule 2 |
| `video/mp4` | a value the brief pins | C-CF-20 | Core features rule 2 |
| `GET /api/media/{id}` | a value the brief pins | C-CF-25 | Core features rule 2 |
| `/work` | a value the brief pins | C-CF-33 | Core features rule 4 |
| `Everything` | a value the brief pins | C-CF-33 | Core features rule 4 |
| `All Work` | a value the brief pins | C-CF-34 | Core features rule 4 |
| `client` | a value the brief pins | C-CF-41 | Core features rule 4 |
| `discipline` | a value the brief pins | C-CF-41 | Core features rule 4 |
| `sort` | a value the brief pins | C-CF-41 | Core features rule 4 |
| `view` | a value the brief pins | C-CF-41 | Core features rule 4 |
| `?client=kestra,quitkit&discipline=systems&sort=year-asc&view=list` | a value the brief pins | C-CF-41 | Core features rule 4 |
| `verity-biotics` | a value the brief pins | C-CF-43 | Core features rule 4 |
| `kestra` | a value the brief pins | C-CF-43 | Core features rule 4 |
| `mirror-lab` | a value the brief pins | C-CF-43 | Core features rule 4 |
| `dusk-ritual` | a value the brief pins | C-CF-43 | Core features rule 4 |
| `quitkit` | a value the brief pins | C-CF-43 | Core features rule 4 |
| `strategy` | a value the brief pins | C-CF-44 | Core features rule 4 |
| `product` | a value the brief pins | C-CF-44 | Core features rule 4 |
| `brand-creative` | a value the brief pins | C-CF-44 | Core features rule 4 |
| `systems` | a value the brief pins | C-CF-44 | Core features rule 4 |
| `spatial-experience` | a value the brief pins | C-CF-44 | Core features rule 4 |
| `year-desc` | a value the brief pins | C-CF-45 | Core features rule 4 |
| `year-asc` | a value the brief pins | C-CF-45 | Core features rule 4 |
| `title-asc` | a value the brief pins | C-CF-45 | Core features rule 4 |
| `grid` | a value the brief pins | C-CF-47 | Core features rule 4 |
| `list` | a value the brief pins | C-CF-47 | Core features rule 4 |
| `512` | a value the brief pins | C-CF-53 | Core features rule 4 |
| `GET /api/case-studies/{slug}/related` | a value the brief pins | C-CF-58 | Core features rule 5 |
| `kestra-care` | a value the brief pins | C-CF-71 | Core features rule 5 table row 1 |
| `kestra-home` | a value the brief pins | C-CF-71 | Core features rule 5 table row 1 |
| `0.7917` | a value the brief pins | C-CF-71 | Core features rule 5 table row 1 |
| `verity-biotics-product` | a value the brief pins | C-CF-72 | Core features rule 5 table row 2 |
| `aging-model` | a value the brief pins | C-CF-72 | Core features rule 5 table row 2 |
| `0.6250` | a value the brief pins | C-CF-72 | Core features rule 5 table row 2 |
| `0.3125` | a value the brief pins | C-CF-73 | Core features rule 5 table row 3 |
| `0.3750` | a value the brief pins | C-CF-74 | Core features rule 5 table row 4 |
| `verity-biotics-brand` | a value the brief pins | C-CF-74 | Core features rule 5 table row 4 |
| `completed` | a value the brief pins | C-CF-81 | Core features rule 6 |
| `max_fraction` | a value the brief pins | C-CF-81 | Core features rule 6 |
| `0.95` | a value the brief pins | C-CF-81 | Core features rule 6 |
| `last_fraction` | a value the brief pins | C-CF-86 | Core features rule 6 |
| `chapters_read` | a value the brief pins | C-CF-86 | Core features rule 6 |
| `0.5` | a value the brief pins | C-CF-86 | Core features rule 6 |
| `Less` | a value the brief pins | C-CF-103 | Core features rule 8 |
| `Nothing` | a value the brief pins | C-CF-103 | Core features rule 8 |
| `full` | a value the brief pins | C-CF-104 | Core features rule 8 |
| `reduced` | a value the brief pins | C-CF-104 | Core features rule 8 |
| `still` | a value the brief pins | C-CF-104 | Core features rule 8 |
| `place` | a value the brief pins | C-CF-116 | Core features rule 9 |
| `mechanism` | a value the brief pins | C-CF-116 | Core features rule 9 |
| `note` | a value the brief pins | C-CF-116 | Core features rule 9 |
| `startY(i) = -40 * curve(t)` | a value the brief pins | C-CF-120 | Core features rule 9 |
| `reading_memory` | a value the brief pins | C-CF-128 | Core features rule 10 |
| `yes` | a value the brief pins | C-CF-128 | Core features rule 10 |
| `no` | a value the brief pins | C-CF-128 | Core features rule 10 |
| `180` | a value the brief pins | C-CF-129 | Core features rule 10 |
| `POST /api/consent` | a value the brief pins | C-CF-130 | Core features rule 10 |
| `/privacy` | a value the brief pins | C-CF-137 | Core features rule 11 |
| `field` | a value the brief pins | C-CF-147 | Core features rule 13 |
| `/studio/case-studies/new` | a value the brief pins | C-CF-151 | Core features rule 14 |
| `nosniff` | a value the brief pins | C-CF-158 | Core features rule 15 |
| `hero` | a value the brief pins | C-CF-159 | Core features rule 3 |
| `alt_text` | a value the brief pins | C-CF-159 | Core features rule 3 |
| `chapters` | a value the brief pins | C-CF-159 | Core features rule 3 |
| `home_placement` | a value the brief pins | C-CF-162 | Core features rule 14 |
| `position` | a value the brief pins | C-CF-162 | Core features rule 14 |
| `Case studies` | a value the brief pins | C-CF-163 | Core features rule 14 |
| `New case study` | a value the brief pins | C-CF-163 | Core features rule 14 |
| `View site` | a value the brief pins | C-CF-163 | Core features rule 14 |
| `Sign out` | a value the brief pins | C-CF-163 | Core features rule 14 |
| `/` | a value the brief pins | C-UF-01 | User flow table row 1 |
| `#hero` | a value the brief pins | C-UF-02 | User flow table row 1 |
| `#featured` | a value the brief pins | C-UF-02 | User flow table row 1 |
| `#about` | a value the brief pins | C-UF-02 | User flow table row 1 |
| `#contact` | a value the brief pins | C-UF-02 | User flow table row 1 |
| `/verity-biotics-product` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/verity-biotics-brand` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/aging-model` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/kestra-care` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/kestra-home` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/foundry-campaign` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/foundry-dashboard` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/mirror-lab` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/dusk-ritual` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/quitkit` | a value the brief pins | C-UF-03 | User flow table row 2 |
| `/reading-list` | a value the brief pins | C-UF-06 | User flow table row 5 |
| `/login` | a value the brief pins | C-UF-07 | User flow table row 6 |
| `/signup` | a value the brief pins | C-UF-07 | User flow table row 6 |
| `/studio` | a value the brief pins | C-UF-08 | User flow table rows 7, 9 |
| `/studio/case-studies/{id}` | a value the brief pins | C-UF-08 | User flow table rows 7, 9 |
| `Intro` | a value the brief pins | C-UF-10 | User flow, entry and redirects |
| `Work` | a value the brief pins | C-UF-10 | User flow, entry and redirects |
| `About` | a value the brief pins | C-UF-10 | User flow, entry and redirects |
| `Contact` | a value the brief pins | C-UF-10 | User flow, entry and redirects |
| `work` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `reading-list` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `privacy` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `login` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `signup` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `studio` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `api` | a value the brief pins | C-UF-17 | User flow, entry and redirects |
| `You were in The platform.` | a value the brief pins | C-UF-19 | User flow, the returning reader |
| `Clear filters` | a value the brief pins | C-UF-25 | User flow, states |
| `PPEditorialNew` | a value the brief pins | C-FE-09 | Front-end specification, type |
| `"Times New Roman", Georgia, serif` | a value the brief pins | C-FE-09 | Front-end specification, type |
| `PPNeueMontreal` | a value the brief pins | C-FE-10 | Front-end specification, type |
| `sans-serif` | a value the brief pins | C-FE-10 | Front-end specification, type |
| `Courier New` | a value the brief pins | C-FE-11 | Front-end specification, type |
| `Courier, monospace` | a value the brief pins | C-FE-11 | Front-end specification, type |
| `800` | a value the brief pins | C-FE-13 | Front-end specification, type |
| `72px` | a value the brief pins | C-FE-14 | Front-end specification, type |
| `99px` | a value the brief pins | C-FE-14 | Front-end specification, type |
| `16px` | a value the brief pins | C-FE-15 | Front-end specification, type |
| `14.08px` | a value the brief pins | C-FE-15 | Front-end specification, type |
| `1.8` | a value the brief pins | C-FE-16 | Front-end specification, type |
| `1.85` | a value the brief pins | C-FE-16 | Front-end specification, type |
| `Email` | a value the brief pins | C-FE-23 | Front-end specification, chrome |
| `Network` | a value the brief pins | C-FE-23 | Front-end specification, chrome |
| `Back to portfolio` | a value the brief pins | C-FE-25 | Front-end specification, chrome |
| `Case Study` | a value the brief pins | C-FE-25 | Front-end specification, chrome |
| `Save to reading list` | a value the brief pins | C-FE-26 | Front-end specification, chrome |
| `Saved` | a value the brief pins | C-FE-26 | Front-end specification, chrome |
| `All rights reserved` | a value the brief pins | C-FE-29 | Front-end specification, chrome |
| `Privacy` | a value the brief pins | C-FE-29 | Front-end specification, chrome |
| `1.10` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.90` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.75` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.60` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.50` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.40` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.35` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.30` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `0.25` | a value the brief pins | C-FE-37 | Front-end specification, the hero |
| `Founder` | a value the brief pins | C-FE-40 | Front-end specification, the hero |
| `Designer` | a value the brief pins | C-FE-40 | Front-end specification, the hero |
| `Artist` | a value the brief pins | C-FE-40 | Front-end specification, the hero |
| `I build experiences at the intersection` | a value the brief pins | C-FE-41 | Front-end specification, the hero |
| `Enable Motion` | a value the brief pins | C-FE-45 | Front-end specification, the hero |
| `Skip` | a value the brief pins | C-FE-45 | Front-end specification, the hero |
| `18.27` | a value the brief pins | C-FE-49 | Front-end specification, lit passages |
| `6.44` | a value the brief pins | C-FE-49 | Front-end specification, lit passages |
| `64` | a value the brief pins | C-FE-52 | Front-end specification, lit passages |
| `40` | a value the brief pins | C-FE-54 | Front-end specification, settling heading |
| `What I Do` | a value the brief pins | C-FE-55 | Front-end specification, the home page band 2 |
| `Strategy` | a value the brief pins | C-FE-56 | Front-end specification, the home page band 2 |
| `Product` | a value the brief pins | C-FE-56 | Front-end specification, the home page band 2 |
| `Brand & Creative` | a value the brief pins | C-FE-56 | Front-end specification, the home page band 2 |
| `Spatial Experiences` | a value the brief pins | C-FE-56 | Front-end specification, the home page band 2 |
| `Systems` | a value the brief pins | C-FE-56 | Front-end specification, the home page band 2 |
| `From Idea to Reality` | a value the brief pins | C-FE-59 | Front-end specification, the home page band 3 |
| `Featured Work` | a value the brief pins | C-FE-59 | Front-end specification, the home page band 3 |
| `Selected work` | a value the brief pins | C-FE-62 | Front-end specification, the home page band 4 |
| `See all eleven` | a value the brief pins | C-FE-62 | Front-end specification, the home page band 4 |
| `Beyond the Brief` | a value the brief pins | C-FE-66 | Front-end specification, the home page band 5 |
| `About Me` | a value the brief pins | C-FE-66 | Front-end specification, the home page band 5 |
| `Thanjavur` | a value the brief pins | C-FE-67 | Front-end specification, the home page band 5 |
| `Verity Biotics` | a value the brief pins | C-FE-68 | Front-end specification, the home page band 5 |
| `Kestra` | a value the brief pins | C-FE-68 | Front-end specification, the home page band 5 |
| `What I've Been Building` | a value the brief pins | C-FE-68 | Front-end specification, the home page band 5 |
| `Always curious about new ideas.` | a value the brief pins | C-FE-71 | Front-end specification, the home page band 7 |
| `hello@marisol.example.com` | a value the brief pins | C-FE-71 | Front-end specification, the home page band 7 |
| `[ EMAIL ]` | a value the brief pins | C-FE-72 | Front-end specification, the home page band 7 |
| `[ NETWORK ]` | a value the brief pins | C-FE-72 | Front-end specification, the home page band 7 |
| `https://network.example.com/in/marisol-andrade` | a value the brief pins | C-FE-73 | Front-end specification, the home page band 7 |
| `Carry on` | a value the brief pins | C-FE-77 | Front-end specification, the home page |
| `Forget my place` | a value the brief pins | C-FE-77 | Front-end specification, the home page |
| `The idea` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `The workflow` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `The insight` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `User response` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `The real output` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `The Experience` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `User Story` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `AI coach in action` | a value the brief pins | C-FE-82 | Front-end specification, case studies |
| `See all` | a value the brief pins | C-FE-86 | Front-end specification, case studies |
| `The foundation` | a value the brief pins | C-FE-88 | Front-end specification, case studies |
| `The brief` | a value the brief pins | C-FE-88 | Front-end specification, case studies |
| `The belief` | a value the brief pins | C-FE-92 | Front-end specification, chapter table |
| `The belief we started with` | a value the brief pins | C-FE-92 | Front-end specification, chapter table |
| `s4` | a value the brief pins | C-FE-93 | Front-end specification, chapter table |
| `/foundry-campaign#s4` | a value the brief pins | C-FE-93 | Front-end specification, chapter table |
| `s1` | a value the brief pins | C-FE-93 | Front-end specification, chapter table |
| `Bold type. Minimal colour. Maximum presence.` | a value the brief pins | C-FE-95 | Front-end specification, highlight statements |
| `Mirror Lab` | a value the brief pins | C-FE-97 | Front-end specification, catalogue |
| `Dusk Ritual` | a value the brief pins | C-FE-97 | Front-end specification, catalogue |
| `Quitkit` | a value the brief pins | C-FE-97 | Front-end specification, catalogue |
| `Spatial Experience` | a value the brief pins | C-FE-98 | Front-end specification, catalogue |
| `Newest first` | a value the brief pins | C-FE-101 | Front-end specification, the work index |
| `Oldest first` | a value the brief pins | C-FE-101 | Front-end specification, the work index |
| `By name` | a value the brief pins | C-FE-101 | Front-end specification, the work index |
| `Grid` | a value the brief pins | C-FE-102 | Front-end specification, the work index |
| `List` | a value the brief pins | C-FE-102 | Front-end specification, the work index |
| `11 projects` | a value the brief pins | C-FE-103 | Front-end specification, the work index |
| `1 project` | a value the brief pins | C-FE-103 | Front-end specification, the work index |
| `Pronounced as` | a value the brief pins | C-FE-107 | Front-end specification, overlays |
| `City in Tirunelveli, Placeland` | a value the brief pins | C-FE-107 | Front-end specification, overlays |
| `11.0000 N` | a value the brief pins | C-FE-108 | Front-end specification, overlays |
| `76.0000 E` | a value the brief pins | C-FE-108 | Front-end specification, overlays |
| `// under the hood` | a value the brief pins | C-FE-109 | Front-end specification, overlays |
| `How much should move?` | a value the brief pins | C-FE-112 | Front-end specification, preferences panel |
| `Show what is explained` | a value the brief pins | C-FE-114 | Front-end specification, preferences panel |
| `Take me back` | a value the brief pins | C-FE-115 | Front-end specification, resume card |
| `Start again` | a value the brief pins | C-FE-115 | Front-end specification, resume card |
| `Host Grotesk` | a value the brief pins | C-FE-129 | Front-end specification, type |
| `5vw` | a value the brief pins | C-FE-130 | Front-end specification, type |
| `10vw` | a value the brief pins | C-FE-130 | Front-end specification, type |
| `12vw` | a value the brief pins | C-FE-130 | Front-end specification, type |
| `8vw` | a value the brief pins | C-FE-130 | Front-end specification, type |
| `13.6px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `12.8px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `10.4px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `9.6px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `9.92px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `8.8px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `8.32px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `8px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `7.2px` | a value the brief pins | C-FE-131 | Front-end specification, type |
| `1.0` | a value the brief pins | C-FE-132 | Front-end specification, type |
| `1.2` | a value the brief pins | C-FE-132 | Front-end specification, type |
| `1.35` | a value the brief pins | C-FE-132 | Front-end specification, type |
| `1.5` | a value the brief pins | C-FE-132 | Front-end specification, type |
| `1.75` | a value the brief pins | C-FE-132 | Front-end specification, type |
| `2.0` | a value the brief pins | C-FE-132 | Front-end specification, type |
| `Company` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `Brand` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `Role` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `Focus` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `Format` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `Year` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `Period` | a value the brief pins | C-FE-139 | Front-end specification, case studies |
| `// note` | a value the brief pins | C-FE-142 | Front-end specification, overlays |
| `s5` | a value the brief pins | C-FE-150 | Front-end specification, chapter table |
| `s6` | a value the brief pins | C-FE-151 | Front-end specification, chapter table |
| `s3` | a value the brief pins | C-FE-153 | Front-end specification, chapter table |
| `s7` | a value the brief pins | C-FE-155 | Front-end specification, chapter table |
| `s8` | a value the brief pins | C-FE-156 | Front-end specification, chapter table |
| `Designing Trust in Preventive Health` | a value the brief pins | C-FE-158 | Front-end specification, catalogue table |
| `The Body Ledger` | a value the brief pins | C-FE-158 | Front-end specification, catalogue table |
| `2022` | a value the brief pins | C-FE-158 | Front-end specification, catalogue table |
| `Active` | a value the brief pins | C-FE-158 | Front-end specification, catalogue table |
| `Turning Disconnected Health Data Into Daily Decisions` | a value the brief pins | C-FE-159 | Front-end specification, catalogue table |
| `Kestra Care` | a value the brief pins | C-FE-159 | Front-end specification, catalogue table |
| `2020` | a value the brief pins | C-FE-159 | Front-end specification, catalogue table |
| `2023` | a value the brief pins | C-FE-159 | Front-end specification, catalogue table |
| `The Smart Home Built For Placeland` | a value the brief pins | C-FE-160 | Front-end specification, catalogue table |
| `Kestra Home` | a value the brief pins | C-FE-160 | Front-end specification, catalogue table |
| `2015` | a value the brief pins | C-FE-160 | Front-end specification, catalogue table |
| `2021` | a value the brief pins | C-FE-160 | Front-end specification, catalogue table |
| `A Retail Experience That Turns Health Into Action` | a value the brief pins | C-FE-161 | Front-end specification, catalogue table |
| `2025` | a value the brief pins | C-FE-161 | Front-end specification, catalogue table |
| `Where Art Meets Science` | a value the brief pins | C-FE-162 | Front-end specification, catalogue table |
| `Beyond Biological Age` | a value the brief pins | C-FE-163 | Front-end specification, catalogue table |
| `foundry-campaign` | a value the brief pins | C-FE-164 | Front-end specification, catalogue table |
| `Using AI to Build a Creative System` | a value the brief pins | C-FE-164 | Front-end specification, catalogue table |
| `Foundry` | a value the brief pins | C-FE-164 | Front-end specification, catalogue table |
| `2024` | a value the brief pins | C-FE-164 | Front-end specification, catalogue table |
| `foundry-dashboard` | a value the brief pins | C-FE-165 | Front-end specification, catalogue table |
| `Using AI to Rethink the Way We Build` | a value the brief pins | C-FE-165 | Front-end specification, catalogue table |
| `Making Health Scores Work` | a value the brief pins | C-FE-166 | Front-end specification, catalogue table |
| `Designing a Brand for Better Sleep` | a value the brief pins | C-FE-167 | Front-end specification, catalogue table |
| `Quit Like a Badass. Not a Patient.` | a value the brief pins | C-FE-168 | Front-end specification, catalogue table |
| `Alpine.js` | a value the brief pins | C-TR-02 | Technical requirements para 1 |
| `Flask` | a value the brief pins | C-TR-03 | Technical requirements para 1 |
| `Jinja` | a value the brief pins | C-TR-03 | Technical requirements para 1 |
| `PostgreSQL` | a value the brief pins | C-TR-05 | Technical requirements para 2 |
| `DATABASE_URL` | a value the brief pins | C-TR-05 | Technical requirements para 2 |
| `minio` | a value the brief pins | C-TR-06 | Technical requirements para 2 |
| `STORAGE_ENDPOINT` | a value the brief pins | C-TR-06 | Technical requirements para 2 |
| `STORAGE_BUCKET` | a value the brief pins | C-TR-06 | Technical requirements para 2 |
| `STORAGE_ACCESS_KEY` | a value the brief pins | C-TR-07 | Technical requirements para 2 |
| `STORAGE_SECRET_KEY` | a value the brief pins | C-TR-07 | Technical requirements para 2 |
| `access_token` | a value the brief pins | C-TR-09 | Technical requirements para 2 |
| `Strict-Transport-Security` | a value the brief pins | C-TR-13 | Technical requirements, security headers |
| `X-Content-Type-Options: nosniff` | a value the brief pins | C-TR-14 | Technical requirements, security headers |
| `805,638` | a value the brief pins | C-TR-28 | Technical requirements, the hero is the budget |
| `/app/USER_README.md` | a value the brief pins | C-DM-02 | Data model para 2 |
| `featured` | a value the brief pins | C-DM-10 | Data model, case_studies |
| `poster` | a value the brief pins | C-DM-17 | Data model, media |
| `reel` | a value the brief pins | C-DM-17 | Data model, media |
| `level_source` | a value the brief pins | C-DM-21 | Data model, preferences |
| `system` | a value the brief pins | C-DM-21 | Data model, preferences |
| `chosen` | a value the brief pins | C-DM-21 | Data model, preferences |
| `kestra-band` | a value the brief pins | C-DM-29 | Data model, seed data |
| `2019` | a value the brief pins | C-DM-29 | Data model, seed data |
| `0.4` | a value the brief pins | C-DM-31 | Data model, seed data |
| `s2` | a value the brief pins | C-DM-32 | Data model, seed data |
| `template` | a value the brief pins | C-DM-36 | Data model, case_studies |
| `brand` | a value the brief pins | C-DM-36 | Data model, case_studies |
| `last_seen` | a value the brief pins | C-DM-40 | Data model, seed data |
| `${APP_PUBLIC_PORT}:4173` | a value the brief pins | C-DC-02 | Deployment contract bullet 1 |
| `GET /api/health` | a value the brief pins | C-DC-04 | Deployment contract bullet 3 |
| `200` | a value the brief pins | C-DC-04 | Deployment contract bullet 3 |
| `.browser_screenshots/` | a value the brief pins | C-DC-07 | Deployment contract bullet 6 |
| `.downloads/` | a value the brief pins | C-DC-07 | Deployment contract bullet 6 |
| `0.0.0.0` | a value the brief pins | C-DC-10 | Deployment contract bullet 9 |
| `POST /api/auth/signup` | a value the brief pins | C-DC-14 | Deployment contract, API shapes row 1 |
| `email` | a value the brief pins | C-DC-14 | Deployment contract, API shapes row 1 |
| `password` | a value the brief pins | C-DC-14 | Deployment contract, API shapes row 1 |
| `8` | a value the brief pins | C-DC-14 | Deployment contract, API shapes row 1 |
| `POST /api/auth/login` | a value the brief pins | C-DC-15 | Deployment contract, API shapes row 2 |
| `GET /api/me` | a value the brief pins | C-DC-16 | Deployment contract, API shapes row 3 |
| `id` | a value the brief pins | C-DC-16 | Deployment contract, API shapes row 3 |
| `role` | a value the brief pins | C-DC-16 | Deployment contract, API shapes row 3 |
| `choice` | a value the brief pins | C-DC-17 | Deployment contract, API shapes row 5 |
| `GET /api/case-studies` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `slug` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `title` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `index_title` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `disciplines` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `year` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `year_end` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `ongoing` | a value the brief pins | C-DC-18 | Deployment contract, API shapes row 6 |
| `GET /api/case-studies/{slug}` | a value the brief pins | C-DC-19 | Deployment contract, API shapes row 7 |
| `anchor` | a value the brief pins | C-DC-19 | Deployment contract, API shapes row 7 |
| `rail_label` | a value the brief pins | C-DC-19 | Deployment contract, API shapes row 7 |
| `heading` | a value the brief pins | C-DC-19 | Deployment contract, API shapes row 7 |
| `GET /api/filters` | a value the brief pins | C-DC-21 | Deployment contract, API shapes row 9 |
| `clients` | a value the brief pins | C-DC-21 | Deployment contract, API shapes row 9 |
| `token` | a value the brief pins | C-DC-21 | Deployment contract, API shapes row 9 |
| `label` | a value the brief pins | C-DC-21 | Deployment contract, API shapes row 9 |
| `GET /api/reading-list` | a value the brief pins | C-DC-22 | Deployment contract, API shapes row 11 |
| `saved_at` | a value the brief pins | C-DC-22 | Deployment contract, API shapes row 11 |
| `POST /api/reading-list` | a value the brief pins | C-DC-23 | Deployment contract, API shapes row 12 |
| `DELETE /api/reading-list/{slug}` | a value the brief pins | C-DC-24 | Deployment contract, API shapes row 13 |
| `PUT /api/reading-list/{slug}/progress` | a value the brief pins | C-DC-25 | Deployment contract, API shapes row 14 |
| `fraction` | a value the brief pins | C-DC-25 | Deployment contract, API shapes row 14 |
| `PUT /api/preferences` | a value the brief pins | C-DC-26 | Deployment contract, API shapes row 16 |
| `motion_level` | a value the brief pins | C-DC-26 | Deployment contract, API shapes row 16 |
| `reveal_all` | a value the brief pins | C-DC-26 | Deployment contract, API shapes row 16 |
| `GET /api/studio/case-studies` | a value the brief pins | C-DC-27 | Deployment contract, API shapes row 17 |
| `published` | a value the brief pins | C-DC-27 | Deployment contract, API shapes row 17 |
| `POST /api/studio/case-studies` | a value the brief pins | C-DC-28 | Deployment contract, API shapes row 18 |
| `GET /api/studio/case-studies/{id}` | a value the brief pins | C-DC-29 | Deployment contract, API shapes row 19 |
| `PATCH /api/studio/case-studies/{id}` | a value the brief pins | C-DC-30 | Deployment contract, API shapes row 20 |
| `POST /api/studio/case-studies/{id}/chapters` | a value the brief pins | C-DC-31 | Deployment contract, API shapes row 21 |
| `body` | a value the brief pins | C-DC-31 | Deployment contract, API shapes row 21 |
| `DELETE /api/studio/chapters/{id}` | a value the brief pins | C-DC-32 | Deployment contract, API shapes row 22 |
| `POST /api/studio/case-studies/{id}/media` | a value the brief pins | C-DC-33 | Deployment contract, API shapes row 23 |
| `file` | a value the brief pins | C-DC-33 | Deployment contract, API shapes row 23 |
| `width` | a value the brief pins | C-DC-33 | Deployment contract, API shapes row 23 |
| `height` | a value the brief pins | C-DC-33 | Deployment contract, API shapes row 23 |
| `object_key` | a value the brief pins | C-DC-33 | Deployment contract, API shapes row 23 |
| `POST /api/studio/case-studies/{id}/publish` | a value the brief pins | C-DC-34 | Deployment contract, API shapes row 24 |
| `POST /api/studio/case-studies/{id}/unpublish` | a value the brief pins | C-DC-35 | Deployment contract, API shapes row 25 |
| `summary` | a value the brief pins | C-DC-44 | Deployment contract, API shapes row 7 |
| `opening_quote` | a value the brief pins | C-DC-44 | Deployment contract, API shapes row 7 |
| `media` | a value the brief pins | C-DC-44 | Deployment contract, API shapes row 7 |
| `GET /api/preferences` | a value the brief pins | C-DC-45 | Deployment contract, API shapes row 15 |
| `May this browser remember your place?` | the browser question title | C-CF-125 | Core features rule 10 |
| `Remember my place` | the accept answer to the browser question | C-CF-126 | Core features rule 10 |
| `Do not remember` | the decline answer to the browser question | C-CF-126 | Core features rule 10 |
| `This site keeps no analytics and sends nothing to anyone else.` | the privacy sentence | C-CF-141 | Core features rule 11 |
| `Explained on this page` | the reveal-all heading | C-CF-123 | Core features rule 9 |
| `Saved as a draft.` | the save banner | C-CF-153 | Core features rule 14 |
| `Published. It is live at /kestra-band.` | the publish banner, with the case study's own slug | C-CF-154 | Core features rule 14 |
| `Withdrawn. /kestra-band no longer answers.` | the withdrawal banner, with the case study's own slug | C-CF-155 | Core features rule 14 |
| `Published` | the studio list word for a published case study | C-CF-148 | Core features rule 14 |
| `Draft` | the studio list word for a draft | C-CF-148 | Core features rule 14 |
| `Nothing matches those two together. Clear the filters and start again.` | the work index empty state | C-UF-24 | User flow, states |
| `One filter in that link was not recognised and has been dropped.` | the ignored-parameter line | C-UF-27 | User flow, states |
| `Nothing saved yet. Save a case study from its page and it waits here.` | the reading list empty state | C-UF-28 | User flow, states |
| `Nothing on this page carries an explanation.` | the no-annotation line | C-UF-29 | User flow, states |
| `This site moves with you.` | the tilt gate title | C-FE-44 | Front-end specification, the hero |
| `You can change this any time in preferences.` | the tilt gate footer | C-FE-46 | Front-end specification, the hero |
| `of art, science and tech.` | the second hero sub line | C-FE-41 | Front-end specification, the hero |
| `©2026 All rights reserved. Marisol Andrade.` | the first copyright line | C-FE-75 | Front-end specification, the home page band 7 |
| `Kept in this browser only.` | the panel footer when stored | C-FE-113 | Front-end specification, preferences panel |
| `This browser will not let us remember. It applies for now.` | the panel footer when storage is refused | C-FE-113 | Front-end specification, preferences panel |
| `// this browser` | the browser question eyebrow | C-FE-117 | Front-end specification, browser question |
| `Only where you stopped reading and how much you want things to move, kept here and nowhere else.` | the browser question body | C-FE-117 | Front-end specification, browser question |
| `Narrow it down` | the filter bar label | C-FE-100 | Front-end specification, the work index |
| `Who it was for` | the client group name | C-FE-100 | Front-end specification, the work index |
| `What kind of work` | the discipline group name | C-FE-100 | Front-end specification, the work index |
| `// preferences` | the preferences panel eyebrow | C-FE-112 | Front-end specification, preferences panel |
| `// where you stopped` | the resume card eyebrow | C-FE-115 | Front-end specification, resume card |
| `Marisol Andrade` | the portfolio owner's name | C-FE-75 | Overview para 1 |
| `I believe great products are not just engineered or designed, they are carefully crafted experiences.` | the opening of the philosophy passage | C-FE-55 | Front-end specification, the home page band 2 |
| `Art taught me to see. Science taught me to question. Technology gave me a way to build. I have not stopped since.` | the punchline | C-FE-70 | Front-end specification, the home page band 6 |
| `/vitality-score` | the fifth product case-study route | C-UF-03 | User flow table row 2 |
| `vitality-score` | a catalogue slug | C-FE-166 | Front-end specification, catalogue table |
| `Vitality Score` | the scoring product label | C-FE-166 | Front-end specification, catalogue table |
| `Add a hero image before publishing.` | the banner for a publish with no hero | C-CF-160 | Core features rule 3 |
| `Every image needs alternative text before publishing.` | the banner for a publish with unlabelled media | C-CF-160 | Core features rule 3 |
| `Add at least one chapter before publishing.` | the banner for a product publish with no chapter | C-CF-160 | Core features rule 3 |
| `That address belongs to the site. Choose another.` | the reserved-slug message | C-UF-31 | User flow, the designer publishes |
| `Withdraw this case study? Its address stops answering at once.` | the one withdrawal confirmation | C-UX-37 | User flow, the designer withdraws |
| `// 0 to 1 across letters` | mechanism comment on line 2 | C-FE-109 | Front-end specification, overlays |
| `// U-shape` | mechanism comment on line 3 | C-FE-109 | Front-end specification, overlays |
| `// 0 to 1` | mechanism comment on line 6 | C-FE-109 | Front-end specification, overlays |
| `Art` | a highlighted punchline word | C-FE-50 | Front-end specification, lit passages |
| `to` | a highlighted punchline word | C-FE-50 | Front-end specification, lit passages |
| `see` | a highlighted punchline word | C-FE-50 | Front-end specification, lit passages |
| `Withdraw` | the studio withdrawal control | C-UX-37 | UI/UX notes, components |
| `The studio is for the designer.` | the studio refusal a reader sees | C-UF-32 | User flow, entry and redirects |
| `Device Motion` | the tilt gate eyebrow, first part | C-FE-44 | Front-end specification, the hero |
| `Permission Request` | the tilt gate eyebrow, second part | C-FE-44 | Front-end specification, the hero |
| `The hero images respond to how you hold and tilt your phone. Allow motion access to experience the full effect.` | the tilt gate body | C-FE-44 | Front-end specification, the hero |
| `I believe great products are not just engineered or designed, they are carefully crafted experiences. My work lives at the intersection of art, science, and technology, where art shapes form and emotion, science guides understanding, and technology quietly enables experiences that feel natural and alive.` | the full philosophy passage | C-FE-55 | Front-end specification, the home page band 2 |
| `carefully crafted experiences` | a highlighted philosophy phrase | C-FE-50 | Front-end specification, the lit passages |
| `natural and alive` | a highlighted philosophy phrase | C-FE-50 | Front-end specification, the lit passages |
| `part founder, part designer, part artist` | the highlighted about phrase | C-FE-50 | Front-end specification, the lit passages |
| `taught me` | a highlighted punchline phrase | C-FE-50 | Front-end specification, the lit passages |
| `From products to brands to moving image, every project begins with an idea and ends with something better than the brief.` | the work band line | C-FE-62 | Front-end specification, the home page band 4 |
| `Co-Founder & Chief Product Officer` | the first role title | C-FE-68 | Front-end specification, the home page band 5 |
| `APR 2022 - FEB 2026` | the first role period, typographic dash when rendered | C-FE-68 | Front-end specification, the home page band 5 |
| `~4 YEARS` | the first role length | C-FE-68 | Front-end specification, the home page band 5 |
| `Co-Founder & Chief Technology Officer` | the second role title | C-FE-68 | Front-end specification, the home page band 5 |
| `AUG 2015 - APR 2022` | the second role period, typographic dash when rendered | C-FE-68 | Front-end specification, the home page band 5 |
| `6 YEARS 8 MONTHS` | the second role length | C-FE-68 | Front-end specification, the home page band 5 |
| `Any reproduction, distribution, or use of the materials without permission is prohibited.` | the second copyright line | C-FE-75 | Front-end specification, the home page band 7 |
| `Location` | the place card pin | C-FE-107 | Front-end specification, overlays |
| `Than` | the first place syllable | C-FE-107 | Front-end specification, overlays |
| `ja` | the second place syllable | C-FE-107 | Front-end specification, overlays |
| `vur` | the third place syllable | C-FE-107 | Front-end specification, overlays |
| `I call it the city of entrepreneurs` | the place card line | C-FE-107 | Front-end specification, overlays |
| `This might look like a simple animation, here's what's actually going on.` | the mechanism card title | C-FE-109 | Front-end specification, overlays |
| `n = total letters in heading` | mechanism line 1 | C-FE-109 | Front-end specification, overlays |
| `t = i / (n - 1)` | mechanism line 2 | C-FE-109 | Front-end specification, overlays |
| `curve(t) = abs(cos(t * pi))` | mechanism line 3 | C-FE-109 | Front-end specification, overlays |
| `currentY(i) = startY(i) * (1 - p)` | mechanism line 5 | C-FE-109 | Front-end specification, overlays |
| `p = scroll progress` | mechanism line 6 | C-FE-109 | Front-end specification, overlays |
| `edges land first` | mechanism footer word group 1 | C-FE-109 | Front-end specification, overlays |
| `middle follows` | mechanism footer word group 2 | C-FE-109 | Front-end specification, overlays |
| `pure math` | mechanism footer word group 3 | C-FE-109 | Front-end specification, overlays |
| `The full site, as it was designed.` | help line for Everything | C-FE-112 | Front-end specification, preferences panel |
| `Things arrive without travelling. Scrolling is plain.` | help line for Less | C-FE-112 | Front-end specification, preferences panel |
| `Every page arrives finished. Films wait to be asked.` | help line for Nothing | C-FE-112 | Front-end specification, preferences panel |
| `Use device tilt` | the tilt button | C-FE-112 | Front-end specification, preferences panel |
| `Device tilt is on` | the tilt button once enabled | C-FE-112 | Front-end specification, preferences panel |
| `The quiet` | draft rail label s1 | C-DM-39 | Data model, seed data |
| `Designing for the hours nobody watches` | draft heading s1 | C-DM-39 | Data model, seed data |
| `The band` | draft rail label s2 | C-DM-39 | Data model, seed data |
| `A band that knew when to stay quiet` | draft heading s2 | C-DM-39 | Data model, seed data |
| `What it taught` | draft rail label s3 | C-DM-39 | Data model, seed data |
| `What the band taught us` | draft heading s3 | C-DM-39 | Data model, seed data |
| `What we built` | a `/verity-biotics-product` rail label | C-FE-150 | Front-end specification, chapter table |
| `What we were building` | a `/verity-biotics-product` article heading | C-FE-150 | Front-end specification, chapter table |
| `Design as strategy` | a `/verity-biotics-product` rail label | C-FE-150 | Front-end specification, chapter table |
| `Design as a strategic decision` | a `/verity-biotics-product` article heading | C-FE-150 | Front-end specification, chapter table |
| `When people held it` | a `/verity-biotics-product` rail label | C-FE-150 | Front-end specification, chapter table |
| `What happened when people held it` | a `/verity-biotics-product` article heading | C-FE-150 | Front-end specification, chapter table |
| `What we learned` | a `/verity-biotics-product` rail label | C-FE-150 | Front-end specification, chapter table |
| `What this taught us about trust` | a `/verity-biotics-product` article heading | C-FE-150 | Front-end specification, chapter table |
| `The pivot` | a `/kestra-care` rail label | C-FE-151 | Front-end specification, chapter table |
| `The pivot that set the direction` | a `/kestra-care` article heading | C-FE-151 | Front-end specification, chapter table |
| `The platform` | a `/kestra-care` rail label | C-FE-151 | Front-end specification, chapter table |
| `A platform, not a feature` | a `/kestra-care` article heading | C-FE-151 | Front-end specification, chapter table |
| `Track trace act` | a `/kestra-care` rail label | C-FE-151 | Front-end specification, chapter table |
| `Track, trace and act` | a `/kestra-care` article heading | C-FE-151 | Front-end specification, chapter table |
| `The AI coach` | a `/kestra-care` rail label | C-FE-151 | Front-end specification, chapter table |
| `An AI coach in the pocket` | a `/kestra-care` article heading | C-FE-151 | Front-end specification, chapter table |
| `One designer` | a `/kestra-care` rail label | C-FE-151 | Front-end specification, chapter table |
| `One designer across the whole stack` | a `/kestra-care` article heading | C-FE-151 | Front-end specification, chapter table |
| `What it became` | a `/kestra-care` rail label | C-FE-151 | Front-end specification, chapter table |
| `What it became in the end` | a `/kestra-care` article heading | C-FE-151 | Front-end specification, chapter table |
| `The concept` | a `/mirror-lab` rail label | C-FE-152 | Front-end specification, chapter table |
| `A shop that starts with a question` | a `/mirror-lab` article heading | C-FE-152 | Front-end specification, chapter table |
| `The experience` | a `/mirror-lab` rail label | C-FE-152 | Front-end specification, chapter table |
| `Ten minutes, start to finish` | a `/mirror-lab` article heading | C-FE-152 | Front-end specification, chapter table |
| `The diagnostics` | a `/mirror-lab` rail label | C-FE-152 | Front-end specification, chapter table |
| `Diagnostics without a clinic` | a `/mirror-lab` article heading | C-FE-152 | Front-end specification, chapter table |
| `What this proved` | a `/mirror-lab` rail label | C-FE-152 | Front-end specification, chapter table |
| `What the pilot proved` | a `/mirror-lab` article heading | C-FE-152 | Front-end specification, chapter table |
| `The model` | a `/mirror-lab` rail label | C-FE-152 | Front-end specification, chapter table |
| `A model other stores can run` | a `/mirror-lab` article heading | C-FE-152 | Front-end specification, chapter table |
| `The question` | a `/aging-model` rail label | C-FE-153 | Front-end specification, chapter table |
| `The question prevention cannot answer` | a `/aging-model` article heading | C-FE-153 | Front-end specification, chapter table |
| `Building a model that looks ahead` | a `/aging-model` article heading | C-FE-153 | Front-end specification, chapter table |
| `What it showed` | a `/aging-model` rail label | C-FE-153 | Front-end specification, chapter table |
| `What the model showed people` | a `/aging-model` article heading | C-FE-153 | Front-end specification, chapter table |
| `The noise` | a `/vitality-score` rail label | C-FE-154 | Front-end specification, chapter table |
| `Too many signals, not enough sense` | a `/vitality-score` article heading | C-FE-154 | Front-end specification, chapter table |
| `One number` | a `/vitality-score` rail label | C-FE-154 | Front-end specification, chapter table |
| `Designing one number worth checking` | a `/vitality-score` article heading | C-FE-154 | Front-end specification, chapter table |
| `Earning trust` | a `/vitality-score` rail label | C-FE-154 | Front-end specification, chapter table |
| `Earning trust in a score` | a `/vitality-score` article heading | C-FE-154 | Front-end specification, chapter table |
| `What moved` | a `/vitality-score` rail label | C-FE-154 | Front-end specification, chapter table |
| `What moved when people used it` | a `/vitality-score` article heading | C-FE-154 | Front-end specification, chapter table |
| `The house` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `A house that had never been wired` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `The hub` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `One hub for every room` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `The installers` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `Designing for the installers first` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `The app` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `An app for the whole household` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `The families` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `What families actually asked for` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `The scale` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `Growing to thousands of homes` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `What it left` | a `/kestra-home` rail label | C-FE-155 | Front-end specification, chapter table |
| `What it left behind` | a `/kestra-home` article heading | C-FE-155 | Front-end specification, chapter table |
| `Three audiences` | a `/foundry-campaign` rail label | C-FE-156 | Front-end specification, chapter table |
| `Three audiences, three anxieties` | a `/foundry-campaign` article heading | C-FE-156 | Front-end specification, chapter table |
| `The engine` | a `/foundry-campaign` rail label | C-FE-156 | Front-end specification, chapter table |
| `A lightweight creative engine` | a `/foundry-campaign` article heading | C-FE-156 | Front-end specification, chapter table |
| `The reel` | a `/foundry-campaign` rail label | C-FE-156 | Front-end specification, chapter table |
| `One reel for every channel` | a `/foundry-campaign` article heading | C-FE-156 | Front-end specification, chapter table |
| `The trio` | a `/foundry-campaign` rail label | C-FE-156 | Front-end specification, chapter table |
| `Three films, one system` | a `/foundry-campaign` article heading | C-FE-156 | Front-end specification, chapter table |
| `What it made` | a `/foundry-campaign` rail label | C-FE-156 | Front-end specification, chapter table |
| `What the engine made` | a `/foundry-campaign` article heading | C-FE-156 | Front-end specification, chapter table |
| `Six weeks and a blank page` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `An AI-assisted workflow` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `The guardrails` | a `/foundry-dashboard` rail label | C-FE-157 | Front-end specification, chapter table |
| `Guardrails that kept the quality` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `The build` | a `/foundry-dashboard` rail label | C-FE-157 | Front-end specification, chapter table |
| `Building in the open` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `The review` | a `/foundry-dashboard` rail label | C-FE-157 | Front-end specification, chapter table |
| `Review as a daily habit` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `The launch` | a `/foundry-dashboard` rail label | C-FE-157 | Front-end specification, chapter table |
| `Launching on schedule` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `What it changed` | a `/foundry-dashboard` rail label | C-FE-157 | Front-end specification, chapter table |
| `What it changed about how we build` | a `/foundry-dashboard` article heading | C-FE-157 | Front-end specification, chapter table |
| `Health data is fragmented and hard to interpret. We used design to make it coherent, understandable, and trusted.` | the `/verity-biotics-product` summary | C-FE-94 | Front-end specification, titles table |
| `The hardest thing about building in preventive health is that we had to prove the category exists before the product could even be considered.` | the `/verity-biotics-product` opening quote | C-FE-94 | Front-end specification, titles table |
| `The Verity Biotics brand identity was built on a single belief: that science and art are not opposites. One explains the world. The other makes it felt.` | the `/verity-biotics-brand` summary | C-FE-94 | Front-end specification, titles table |
| `Biology is beautiful. Most health brands forget that. We built one that did not.` | the `/verity-biotics-brand` opening quote | C-FE-94 | Front-end specification, titles table |
| `How we built a multimodal biological aging model that went beyond standard biomarkers to show users not just where they were, but where they were heading.` | the `/aging-model` summary | C-FE-94 | Front-end specification, titles table |
| `Prevention is a hard thing to quantify. How do you know you prevented a disease you never got?` | the `/aging-model` opening quote | C-FE-94 | Front-end specification, titles table |
| `How a single daily score turned a dozen health signals into one number people could act on.` | the `/vitality-score` summary | C-FE-94 | Front-end specification, titles table |
| `Turning disconnected health data into daily decisions` | the `/kestra-care` title | C-FE-94 | Front-end specification, titles table |
| `Kestra Care was a full-stack holistic wellness platform built by one designer, from biomathematical fatigue models to AI lifestyle coaching.` | the `/kestra-care` summary | C-FE-94 | Front-end specification, titles table |
| `Kestra Home was a connected home system designed from the wiring up for how families in Placeland actually live.` | the `/kestra-home` summary | C-FE-94 | Front-end specification, titles table |
| `Foundry needed to reach three different audiences with three different anxieties about their health. This is how we built the creative system that did it.` | the `/foundry-campaign` summary | C-FE-94 | Front-end specification, titles table |
| `Traditional content is slow and expensive. We built a lightweight creative engine instead.` | the `/foundry-campaign` opening quote | C-FE-94 | Front-end specification, titles table |
| `Using AI to rethink the way we build` | the `/foundry-dashboard` title | C-FE-94 | Front-end specification, titles table |
| `How the Foundry dashboard went from idea to production in six weeks, and the AI-assisted development workflow we built to make it possible.` | the `/foundry-dashboard` summary | C-FE-94 | Front-end specification, titles table |
| `The question was never whether AI could help us build faster. It was whether we could build a process that kept the quality intact.` | the `/foundry-dashboard` opening quote | C-FE-94 | Front-end specification, titles table |
| `Mirror Lab is a physical wellness experience that compresses diagnostics, insight, and personalised commerce into a single ten-minute visit.` | the `/mirror-lab` summary | C-FE-94 | Front-end specification, titles table |
| `Health decisions are not made in clinics. They are made where action is easy.` | the `/mirror-lab` opening quote | C-FE-94 | Front-end specification, titles table |
| `Designing a brand for better sleep through intentional rituals` | the `/dusk-ritual` title | C-FE-94 | Front-end specification, titles table |
| `Dusk Ritual is a premium wellness brand built around the idea that better sleep begins before you close your eyes, and that every part of the evening is part of it.` | the `/dusk-ritual` summary | C-FE-94 | Front-end specification, titles table |
| `Most sleep brands treat sleep as a problem to fix. We built one that treated it as a ritual to return to.` | the `/dusk-ritual` opening quote | C-FE-94 | Front-end specification, titles table |
| `Quitkit was built to make quitting look cool, sound cool, and feel like a choice you made for yourself, not one made for you by a doctor.` | the `/quitkit` summary | C-FE-94 | Front-end specification, titles table |
| `Quitting is not weakness. It is the hardest thing some people will ever do. We decided it should look like it.` | the `/quitkit` opening quote | C-FE-94 | Front-end specification, titles table |
| `We're here to empower the change makers.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `A System, Not Just a Symbol` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `Tech and luxury in the same breath.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `The Gene Art is the soul of the visual identity.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `No agency. No branding experience. Just the people who understood it most.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `Colour as context. Everything else as constant.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `A quiet invitation into a nightly journey.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `Dusk Ritual is a behaviour design system for sleep.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `The voice came from the culture, not above it.` | a brand highlight statement | C-FE-95 | Front-end specification, highlight statements |
| `Product Vision` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Market & User Insight` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Go-to-Market` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Strategic Narrative & Storytelling` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Concept to Product` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Product Design` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Design Systems & Operations` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Connected Hardware & IoT` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Brand Architecture` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Creative Direction` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Visual Identity & Design` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Motion & Video` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Retail Experiences` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Brand Activation Design` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Service Journey Design` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `AI-Native Workflow Design` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Process & Ops Design` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `Org and Team Building` | a discipline card item | C-FE-57 | Front-end specification, the home page band 2 |
| `I grew up in Thanjavur, a city that runs on the quiet ambition of people who build things. My father was one of them. I inherited the instinct.` | about paragraph 1 | C-FE-66 | Front-end specification, the home page band 5 |
| `Curiosity is how I move through the world. A decade of building companies, designing products, talking to customers, and occasionally overthinking everything has given me a lens that's part founder, part designer, part artist. It's not a job title. It's simply how I see.` | about paragraph 2 | C-FE-66 | Front-end specification, the home page band 5 |
| `I draw inspiration from unexpected places. A street market in an unfamiliar city. A painting that's going wrong. A small family business that has quietly outlasted every trend. I travel whenever I can, not for the destinations but for the movement. Newness is where I do my best thinking.` | about paragraph 3 | C-FE-66 | Front-end specification, the home page band 5 |
| `I don't spend much time pitching what I can do. I make things and let them speak.` | about paragraph 4 | C-FE-66 | Front-end specification, the home page band 5 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the length of the intent delay before a card opens on hover | C-FE-110 | named as a short delay with no value, under the brief's rule that motion values are words |
| the tablet edge where the phone layout takes over | C-UX-22 | named as a tier boundary with no width, under the brief's rule that breakpoints are arrangements |
| the chapter body copy | C-FE-91 | handed to the builder in the copy deck's voice rather than pinned |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 11 |
| User roles | 1 | 21 |
| Core features | 11 | 163 |
| User flow | 7 | 33 |
| UI and UX notes | 4 | 37 |
| Front-end specification | 15 | 168 |
| Technical requirements | 8 | 36 |
| Data model | 3 | 40 |
| Constraints | 0 | 9 |
| Deployment contract | 9 | 46 |
