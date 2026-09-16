# Checklist: atlas.design

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 402
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves the portfolio of Rin Alvez as one public site. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The home page presents ten pieces of work as a browsable index. `src: Overview para 1`
- [ ] `C-OV-03` `capability` Case studies read as documentation with anchored headings. `src: Overview para 1`
- [ ] `C-OV-04` `capability` One article sits behind a four-digit passcode. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The studio sits behind a second four-digit passcode. `src: Overview para 2`
- [ ] `C-OV-06` `constraint` The site offers no comment system. `src: Overview para 3`
- [ ] `C-OV-07` `constraint` The site offers no newsletter signup. `src: Overview para 3`
- [ ] `C-OV-08` `constraint` The site offers no contact form. `src: Overview para 3`
- [ ] `C-OV-09` `constraint` The site offers no search box. `src: Overview para 3`
- [ ] `C-OV-10` `capability` Index placement comes from fields the owner sets. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor opens every public route with no account. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor reads a figure of a published case study. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A visitor holding the field notes grant reads the gated article. `src: User roles table row 1`
- [ ] `C-RL-04` `role` The app denies a visitor any draft case study by any address. `src: User roles table row 1`
- [ ] `C-RL-05` `role` The app denies a visitor any figure of a draft. `src: User roles table row 1`
- [ ] `C-RL-06` `role` The app denies a visitor the gated article without the matching grant. `src: User roles table row 1`
- [ ] `C-RL-07` `role` The app denies a visitor the studio API. `src: User roles table row 1`
- [ ] `C-RL-08` `role` The app denies a visitor the page-view record. `src: User roles table row 1`
- [ ] `C-RL-09` `role` The app refuses every write from a visitor. `src: User roles table row 1`
- [ ] `C-RL-10` `role` The owner creates a case study after unlocking the studio. `src: User roles table row 2`
- [ ] `C-RL-11` `role` The owner previews a draft with the studio grant. `src: User roles table row 2`
- [ ] `C-RL-12` `role` The owner reads the page-view record. `src: User roles table row 2`
- [ ] `C-RL-13` `role` The owner locks the studio again. `src: User roles table row 2`
- [ ] `C-RL-14` `role` A rejected visitor write leaves the protected state unchanged. `src: User roles, authorization paragraph`
- [ ] `C-RL-15` `constraint` The product offers no signup. `src: User roles, signup paragraph`
- [ ] `C-RL-16` `constraint` The product offers no sign-in form. `src: User roles, signup paragraph`
- [ ] `C-RL-17` `literal` The passcode `5093` opens the path `/studio`. `src: User roles, passcode table row 1`
- [ ] `C-RL-18` `literal` The passcode `2718` opens the path `/field-notes`. `src: User roles, passcode table row 2`

## C-CF Core features

- [ ] `C-CF-01` `literal` `POST /api/passcode` takes a path with a code. `src: Core features, Auth para 1`
- [ ] `C-CF-02` `constraint` The passcode comparison happens on the server. `src: Core features, Auth para 1`
- [ ] `C-CF-03` `constraint` A passcode response carries a boolean alone, never the code. `src: Core features, Auth para 1`
- [ ] `C-CF-04` `contract` A correct code answers 200 with the submitted path mapped to true. `src: Core features rule 1`
- [ ] `C-CF-05` `contract` A wrong code answers 200 with the submitted path mapped to false. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` A wrong code sets no grant. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` A path with no gate answers like a wrong code. `src: Core features rule 2`
- [ ] `C-CF-08` `constraint` A code of any shape other than four digits is rejected as invalid. `src: Core features rule 3`
- [ ] `C-CF-09` `constraint` A body missing the path or the code is rejected as invalid. `src: Core features rule 3`
- [ ] `C-CF-10` `constraint` A malformed submission is never counted as an attempt. `src: Core features rule 3`
- [ ] `C-CF-11` `constraint` Five refused attempts within one minute lock further attempts for that path. `src: Core features rule 4`
- [ ] `C-CF-12` `literal` A locked attempt answers 429 with the error `rate_limited`. `src: Core features rule 4`
- [ ] `C-CF-13` `constraint` Attempts for an ungated path count toward the lock. `src: Core features rule 4`
- [ ] `C-CF-14` `constraint` The grant cookie is unreadable by page script. `src: Core features rule 5`
- [ ] `C-CF-15` `constraint` The grant cookie carries no expiry date or maximum age. `src: Core features rule 5`
- [ ] `C-CF-16` `constraint` The grant cookie works over a plain unencrypted connection. `src: Core features rule 5`
- [ ] `C-CF-17` `capability` The browser sends the grant back on later requests. `src: Core features rule 5`
- [ ] `C-CF-18` `constraint` A field notes grant leaves every studio endpoint denied. `src: Core features rule 6`
- [ ] `C-CF-19` `constraint` A field notes grant leaves every draft invisible. `src: Core features rule 6`
- [ ] `C-CF-20` `capability` The studio grant opens the gated article. `src: Core features rule 6`
- [ ] `C-CF-21` `literal` `POST /api/passcode/release` ends a grant for the browser. `src: Core features rule 7`
- [ ] `C-CF-22` `constraint` A released grant stays closed even when its cookie is sent again. `src: Core features rule 7`
- [ ] `C-CF-23` `constraint` A gated path without a grant shows the passcode screen in place of content. `src: Core features rule 8`
- [ ] `C-CF-24` `constraint` A denied read of the gated article carries no lead text. `src: Core features rule 8`
- [ ] `C-CF-25` `constraint` Every studio endpoint denies a request without the studio grant. `src: Core features rule 9`
- [ ] `C-CF-26` `literal` `GET /api/projects` returns the listed cards as a top-level array. `src: Core features rule 10`
- [ ] `C-CF-27` `data` Listed cards are ordered by position ascending. `src: Core features rule 10`
- [ ] `C-CF-28` `data` Each listed card carries both grid placements. `src: Core features rule 10`
- [ ] `C-CF-29` `constraint` A card linked to a draft never appears in the listing. `src: Core features rule 11`
- [ ] `C-CF-30` `capability` An outside card is listed when its own published flag is set. `src: Core features rule 11`
- [ ] `C-CF-31` `constraint` Two listed cards never share a position. `src: Core features rule 12`
- [ ] `C-CF-32` `literal` Publishing onto a taken position is refused with `position_taken`. `src: Core features rule 12`
- [ ] `C-CF-33` `constraint` Two simultaneous publishes claiming one free position do not both succeed. `src: Core features rule 12`
- [ ] `C-CF-34` `constraint` The losing publish stays a draft. `src: Core features rule 12`
- [ ] `C-CF-35` `constraint` A placement past the twelfth column is refused. `src: Core features rule 13`
- [ ] `C-CF-36` `literal` An invalid placement is refused with `invalid_placement`. `src: Core features rule 13`
- [ ] `C-CF-37` `literal` The aspect ratio is one of `16:9`, `1.54:1`, `0.71:1`, `1:1`. `src: Core features rule 13`
- [ ] `C-CF-38` `constraint` A refused placement writes nothing. `src: Core features rule 13`
- [ ] `C-CF-39` `literal` A single year reads `2025` as its year label. `src: Core features rule 14`
- [ ] `C-CF-40` `literal` A year range reads `2024-2026` as its year label. `src: Core features rule 14`
- [ ] `C-CF-41` `data` A media description is never empty. `src: Core features rule 15`
- [ ] `C-CF-42` `literal` A card with an empty media description is refused with `invalid_media_alt`. `src: Core features rule 15`
- [ ] `C-CF-43` `data` A media description never equals the card title. `src: Core features rule 15`
- [ ] `C-CF-44` `capability` At the widest layout each card starts on the column its record names. `src: Core features rule 16`
- [ ] `C-CF-45` `capability` A newly published card renders on the column its record names. `src: Core features rule 16`
- [ ] `C-CF-46` `ui` At mid widths each card uses its mid placement. `src: Core features rule 16`
- [ ] `C-CF-47` `literal` The seeded cards start on columns `5, 1, 7, 6, 10, 1, 5, 9, 6, 10` in order. `src: Core features rule 16`
- [ ] `C-CF-48` `literal` The first seeded card is `Kindling` at position 1. `src: Core features, seeded cards table row 1`
- [ ] `C-CF-49` `literal` The card `GlyphSymbols` links to `https://www.example.com/plugins/glyphsymbols`. `src: Core features, seeded cards table row 4`
- [ ] `C-CF-50` `literal` The card `DuskMode` carries the kind `tools`. `src: Core features, seeded cards table row 5`
- [ ] `C-CF-51` `literal` The card `nDrive` carries the aspect `0.71:1`. `src: Core features, seeded cards table row 6`
- [ ] `C-CF-52` `literal` The card `Loop: See Hear Touch` carries the kind `event`. `src: Core features, seeded cards table row 9`
- [ ] `C-CF-53` `literal` The card `DuskMode` links to `https://www.example.com/plugins/duskmode`. `src: Core features, seeded cards table row 5`
- [ ] `C-CF-54` `literal` The first Loop card links to `https://www.example.com/events/see-hear-touch`. `src: Core features, seeded cards table row 9`
- [ ] `C-CF-55` `literal` The second Loop card links to `https://www.example.com/events/system-design`. `src: Core features, seeded cards table row 10`
- [ ] `C-CF-56` `capability` An outside card opens its address in a new browsing context. `src: Core features, seeded cards paragraph`
- [ ] `C-CF-57` `literal` The first three cards carry the eyebrow `Coding Project`. `src: Core features, seeded cards table rows 1 to 3`
- [ ] `C-CF-58` `ui` An outside card shows a north-east arrow glyph after its kind label. `src: Core features, seeded cards paragraph`
- [ ] `C-CF-59` `ui` The Kindling title shows a raised trade mark sign. `src: Core features, seeded cards paragraph`
- [ ] `C-CF-60` `literal` `GET /api/case-studies/{slug}` returns one published or stub case study. `src: Core features rule 17`
- [ ] `C-CF-61` `data` A stub read carries an empty body with no headings. `src: Core features rule 17`
- [ ] `C-CF-62` `data` A stub read reports a character count of zero. `src: Core features rule 17`
- [ ] `C-CF-63` `capability` A stubbed case study keeps its stored body for a later publish. `src: Core features rule 17`
- [ ] `C-CF-64` `constraint` A draft read answers exactly as an unknown slug answers. `src: Core features rule 18`
- [ ] `C-CF-65` `constraint` A draft page carries no title, lead or body text. `src: Core features rule 18`
- [ ] `C-CF-66` `literal` The case study page for nDrive lives at `/ndrive`. `src: Core features rule 19`
- [ ] `C-CF-67` `literal` A slug of the wrong shape is refused with `invalid_slug`. `src: Core features rule 20`
- [ ] `C-CF-68` `literal` The slug `studio` is refused with `slug_reserved`. `src: Core features rule 20`
- [ ] `C-CF-69` `literal` A slug already held is refused with `slug_taken`. `src: Core features rule 20`
- [ ] `C-CF-70` `constraint` A refused slug writes nothing. `src: Core features rule 20`
- [ ] `C-CF-71` `capability` A slug change on a published case study leaves a permanent redirect. `src: Core features rule 21`
- [ ] `C-CF-72` `constraint` A retired slug stays unavailable to other case studies. `src: Core features rule 21`
- [ ] `C-CF-73` `capability` A body line starting with hashes becomes a heading of that level. `src: Core features rule 22`
- [ ] `C-CF-74` `literal` A body that skips a heading level is refused with `invalid_heading_levels`. `src: Core features rule 22`
- [ ] `C-CF-75` `capability` A figure marker line places the uploaded figure in the body. `src: Core features rule 22`
- [ ] `C-CF-76` `capability` A heading slug replaces each run of other characters with one hyphen. `src: Core features rule 23`
- [ ] `C-CF-77` `literal` The heading `Sync, conflicts & recovery` gets the slug `sync-conflicts-recovery`. `src: Core features rule 23`
- [ ] `C-CF-78` `literal` A repeated heading `Notes` gets the slug `notes-2`. `src: Core features rule 23`
- [ ] `C-CF-79` `capability` An edited heading yields the slug of its new text. `src: Core features rule 23`
- [ ] `C-CF-80` `capability` Each heading element on the page carries the heading slug as its id. `src: Core features rule 23`
- [ ] `C-CF-81` `data` The character count leaves out line breaks. `src: Core features rule 24`
- [ ] `C-CF-82` `literal` A count of 1602 reads `1,602` as its character label. `src: Core features rule 24`
- [ ] `C-CF-83` `literal` Dimensions read `1440x900` for the nDrive case study. `src: Core features rule 25`
- [ ] `C-CF-84` `literal` The date label reads `Jan 15, 2026` for the nDrive case study. `src: Core features rule 25`
- [ ] `C-CF-85` `data` The nDrive case study carries nine headings in the stated order. `src: Core features rule 26`
- [ ] `C-CF-86` `data` The Wasm design utils case study carries seven headings. `src: Core features rule 26`
- [ ] `C-CF-87` `data` The Coast Icon case study carries fifteen headings. `src: Core features rule 26`
- [ ] `C-CF-88` `data` The Coast Icon case study carries a code block. `src: Core features rule 26`
- [ ] `C-CF-89` `literal` The Almanac Mono page offers the link `Download Almanac Mono` to `https://www.example.com/almanac-mono/download`. `src: Core features rule 27`
- [ ] `C-CF-90` `literal` The stub page shows the pinned work-in-progress notice. `src: Core features rule 28`
- [ ] `C-CF-91` `constraint` A stub page renders no contents drawer. `src: Core features rule 28`
- [ ] `C-CF-92` `literal` The Teamharbor stub links to `https://www.example.com/teamharbor`. `src: Core features rule 28`
- [ ] `C-CF-93` `literal` The Field Notes lead reads `Notes I keep for myself, shared with the people who ask.` `src: Core features rule 29`
- [ ] `C-CF-94` `constraint` The Field Notes article never appears in the index. `src: Core features rule 29`
- [ ] `C-CF-95` `capability` A figure is stored in the bucket named by `STORAGE_BUCKET`. `src: Core features rule 30`
- [ ] `C-CF-96` `literal` A figure key matches `case-studies/{case_study_id}/figures/{sha256_of_bytes}.{ext}`. `src: Core features rule 30`
- [ ] `C-CF-97` `data` An upload records the content type with the byte size. `src: Core features rule 31`
- [ ] `C-CF-98` `data` An upload records the intrinsic width with the intrinsic height. `src: Core features rule 31`
- [ ] `C-CF-99` `literal` An upload without alternative text is refused with `alt_text_required`. `src: Core features rule 32`
- [ ] `C-CF-100` `literal` An upload with a bad size is refused with `invalid_dimensions`. `src: Core features rule 32`
- [ ] `C-CF-101` `constraint` A size that disagrees with the real image is refused. `src: Core features rule 32`
- [ ] `C-CF-102` `literal` An upload of another content type is refused with `unsupported_type`. `src: Core features rule 32`
- [ ] `C-CF-103` `literal` An upload over `5,242,880` bytes is refused with `file_too_large`. `src: Core features rule 32`
- [ ] `C-CF-104` `constraint` A refused upload stores no object. `src: Core features rule 32`
- [ ] `C-CF-105` `constraint` Uploading identical bytes twice creates one object. `src: Core features rule 33`
- [ ] `C-CF-106` `constraint` Uploading identical bytes twice creates one figure record. `src: Core features rule 33`
- [ ] `C-CF-107` `literal` `GET /api/figures/{id}` streams figure bytes from the bucket. `src: Core features rule 34`
- [ ] `C-CF-108` `constraint` A gated figure is served only with the matching grant. `src: Core features rule 34`
- [ ] `C-CF-109` `constraint` A draft figure is served only with the studio grant. `src: Core features rule 34`
- [ ] `C-CF-110` `constraint` An anonymous request straight to the bucket receives no figure bytes. `src: Core features rule 34`
- [ ] `C-CF-111` `ui` A placed figure spans the text column with its alternative text shown. `src: Core features rule 35`
- [ ] `C-CF-112` `capability` A placed figure reserves its box from its recorded size. `src: Core features rule 35`
- [ ] `C-CF-113` `literal` `GET /api/studio/case-studies` lists case studies in every status. `src: Core features rule 36`
- [ ] `C-CF-114` `capability` Creating a case study yields the status draft. `src: Core features rule 37`
- [ ] `C-CF-115` `literal` A create missing a required field is refused with `incomplete`. `src: Core features rule 37`
- [ ] `C-CF-116` `literal` A field of the wrong shape is refused with `invalid_field`. `src: Core features rule 37`
- [ ] `C-CF-117` `constraint` Moving a listed card onto a taken position is refused. `src: Core features rule 38`
- [ ] `C-CF-118` `capability` Publishing sets the status published with the card listed. `src: Core features rule 39`
- [ ] `C-CF-119` `data` The first publication sets the published time. `src: Core features rule 39`
- [ ] `C-CF-120` `capability` Marking a stub sets the status stub with the card listed. `src: Core features rule 39`
- [ ] `C-CF-121` `capability` Holding sets the status draft with the card unlisted. `src: Core features rule 39`
- [ ] `C-CF-122` `capability` Holding a case study already in draft returns the draft unchanged. `src: Core features rule 39`
- [ ] `C-CF-123` `capability` A case study with no card publishes as a readable page outside the index. `src: Core features rule 39`
- [ ] `C-CF-124` `constraint` A held case study closes its page to visitors at once. `src: Core features rule 39`
- [ ] `C-CF-125` `constraint` A held case study closes its figures to visitors at once. `src: Core features rule 39`
- [ ] `C-CF-126` `capability` The studio grant opens a draft page. `src: Core features rule 40`
- [ ] `C-CF-127` `ui` A draft preview shows a banner naming the page a draft preview. `src: Core features rule 40`
- [ ] `C-CF-128` `ui` The studio index preview shows every card on the twelve columns with the draft marked. `src: Core features rule 41`
- [ ] `C-CF-129` `literal` The wordmark reads `atlas` followed by `.design`. `src: Core features rule 42`
- [ ] `C-CF-130` `literal` The chrome carries the controls `Work` with `Contact`. `src: Core features rule 42`
- [ ] `C-CF-131` `capability` The Work control is a button rather than a link. `src: Core features rule 42`
- [ ] `C-CF-132` `ui` Work scrolls the home page to the index anchor. `src: Core features rule 42`
- [ ] `C-CF-133` `ui` Contact from a case study returns home before scrolling. `src: Core features rule 42`
- [ ] `C-CF-134` `literal` The theme control reads `THEME[A]` with its state in `aria-pressed`. `src: Core features rule 43`
- [ ] `C-CF-135` `literal` The root element carries the class `light` or `dark`. `src: Core features rule 43`
- [ ] `C-CF-136` `capability` Pressing the A key toggles the theme outside a text field. `src: Core features rule 43`
- [ ] `C-CF-137` `capability` The theme choice survives a reload. `src: Core features rule 43`
- [ ] `C-CF-138` `capability` The theme is applied before the first paint. `src: Core features rule 43`
- [ ] `C-CF-139` `capability` A first visit shows the light theme. `src: Core features rule 43`
- [ ] `C-CF-140` `literal` The sound control label opens with `SOUND[`. `src: Core features rule 44`
- [ ] `C-CF-141` `capability` Sound is off on a first visit. `src: Core features rule 44`
- [ ] `C-CF-142` `ui` Turning sound on fades an ambient bed in. `src: Core features rule 44`
- [ ] `C-CF-143` `ui` The bracketed spinner character cycles only during playback. `src: Core features rule 44`
- [ ] `C-CF-144` `ui` A reload with sound previously on waits for a press before playing. `src: Core features rule 44`
- [ ] `C-CF-145` `literal` The site profile carries the clock labels `GMT+8` with `CN`. `src: Core features rule 45`
- [ ] `C-CF-146` `literal` The pointer readout follows the shape `0720 X 0450 Y`. `src: Core features rule 45`
- [ ] `C-CF-147` `ui` The clock string keeps one width through every update. `src: Core features rule 45`
- [ ] `C-CF-148` `capability` An unknown address answers with a not-found status. `src: Core features rule 46`
- [ ] `C-CF-149` `literal` The not-found page shows the pinned nothing-filed line. `src: Core features rule 46`
- [ ] `C-CF-150` `literal` The not-found page offers `Back to the index` leading home. `src: Core features rule 46`
- [ ] `C-CF-151` `constraint` Every internal link on every public route resolves. `src: Core features rule 47`
- [ ] `C-CF-152` `capability` Each public page view stores its route with a UTC time. `src: Core features rule 48`
- [ ] `C-CF-153` `literal` `GET /api/studio/page-views` returns route with viewed_at pairs newest first. `src: Core features rule 48`
- [ ] `C-CF-154` `constraint` API requests leave no page-view row. `src: Core features rule 48`
- [ ] `C-CF-155` `capability` The home statement links to the Kindling, nDrive, Teamharbor case studies. `src: Core features rule 49`
- [ ] `C-CF-156` `ui` The clock shows the local UTC+8 time on a twenty-four hour clock. `src: Core features rule 45`
- [ ] `C-CF-157` `ui` The frame shows no temperature. `src: Core features rule 45`

## C-UF User flow

- [ ] `C-UF-01` `literal` The route `/wasm-design-utils` serves a case study. `src: User flow, routes table`
- [ ] `C-UF-02` `literal` The route `/teamharbor` serves the stub state. `src: User flow, routes table`
- [ ] `C-UF-03` `literal` The route `/coast-icon` serves a case study. `src: User flow, routes table`
- [ ] `C-UF-04` `literal` The route `/kindling` serves a case study. `src: User flow, routes table`
- [ ] `C-UF-05` `capability` Entering the right code reveals the content at the same address. `src: User flow, entry para 1`
- [ ] `C-UF-06` `capability` A wrong code leaves the passcode screen in place. `src: User flow, entry para 1`
- [ ] `C-UF-07` `ui` The home headline lines rise as the loader fills. `src: User flow, journey 1`
- [ ] `C-UF-08` `ui` The contents drawer glides the article to a chosen heading. `src: User flow, journey 2`
- [ ] `C-UF-09` `literal` Choosing a heading adds `#offline-then-online` to the address. `src: User flow, journey 2`
- [ ] `C-UF-10` `literal` The copy control reads `COPY` then `COPIED`. `src: User flow, journey 2`
- [ ] `C-UF-11` `capability` The fourth digit sends the code with no button. `src: User flow, journey 3`
- [ ] `C-UF-12` `capability` An unlocked article stays open after a reload. `src: User flow, journey 3`
- [ ] `C-UF-13` `literal` A wrong code shows `That code is not right. Try again.` `src: User flow, journey 4`
- [ ] `C-UF-14` `literal` A locked gate shows the pinned too-many-attempts message. `src: User flow, journey 4`
- [ ] `C-UF-15` `literal` The studio sidebar lists `Case studies`, `Index preview`, `Page views`, `Lock studio`. `src: User flow, journey 5`
- [ ] `C-UF-16` `literal` The studio offers the action `New case study`. `src: User flow, journey 5`
- [ ] `C-UF-17` `literal` The editor offers the actions `Publish`, `Mark as stub`, `Hold as draft`. `src: User flow, journey 5`
- [ ] `C-UF-18` `ui` A new case study opens as an inline row at the top of the table. `src: User flow, journey 5`
- [ ] `C-UF-19` `literal` Publishing raises the toast `Published to the index.` `src: User flow, journey 5`
- [ ] `C-UF-20` `literal` Holding raises the toast `Held as a draft.` `src: User flow, journey 5`
- [ ] `C-UF-21` `literal` Marking a stub raises the toast `Marked as a stub.` `src: User flow, journey 5`
- [ ] `C-UF-22` `literal` A position conflict raises the toast `Refused. Another card already holds that position.` `src: User flow, journey 6`
- [ ] `C-UF-23` `ui` The home page shows its centred loader before content settles. `src: User flow, states para 1`
- [ ] `C-UF-24` `ui` A failed studio request raises a toast naming the failure. `src: User flow, states para 1`
- [ ] `C-UF-25` `ui` A studio toast stays until dismissed or replaced. `src: UI/UX notes, components para`
- [ ] `C-UF-26` `ui` The hold prompt names the case study. `src: User flow, journey 5`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` Escape closes the contents drawer, the phone menu, the hold confirmation prompt. `src: UI/UX notes, components para`
- [ ] `C-UX-02` `ui` The home first screen reads complete before any decoration arrives. `src: UI/UX notes para 2`
- [ ] `C-UX-03` `ui` The whole site is warm off-white paper with one warm near-black ink. `src: UI/UX notes, paper para`
- [ ] `C-UX-04` `ui` Quieter tones are the same ink made partly transparent rather than a separate grey. `src: UI/UX notes, paper para`
- [ ] `C-UX-05` `ui` Raised surfaces read as separate from the ground with no shadow. `src: UI/UX notes, paper para`
- [ ] `C-UX-06` `ui` Absolute black appears only on the waiting passcode ring. `src: UI/UX notes, paper para`
- [ ] `C-UX-07` `ui` The light theme shows lime only on selected text plus the scribble. `src: UI/UX notes, colour para`
- [ ] `C-UX-08` `ui` The floating pointer object uses a vivid blue absent from the interface. `src: UI/UX notes, colour para`
- [ ] `C-UX-09` `ui` Code tokens use six hues at one shared lightness. `src: UI/UX notes, code colours para`
- [ ] `C-UX-10` `ui` The dark theme is a warm near-black ground with the ink ladder carried over. `src: UI/UX notes, dark theme para`
- [ ] `C-UX-11` `ui` The chrome except the wordmark is set in one monospace face. `src: UI/UX notes, type para`
- [ ] `C-UX-12` `ui` Display type scales with window width with lines set tight. `src: UI/UX notes, type para`
- [ ] `C-UX-13` `ui` The home headline shows in capitals. `src: UI/UX notes, type para`
- [ ] `C-UX-14` `ui` Heading levels two to four share one semibold style at stepped sizes. `src: UI/UX notes, type para`
- [ ] `C-UX-15` `ui` Grid cells touch with an equal inset as the only gap. `src: UI/UX notes, grid para`
- [ ] `C-UX-16` `ui` Rings are hard-edged inside the element with no blur. `src: UI/UX notes, shape para`
- [ ] `C-UX-17` `ui` Content arrives almost at once then drifts the last hair into place. `src: UI/UX notes, motion para`
- [ ] `C-UX-18` `ui` A fade out leaves faster than the matching fade in arrives. `src: UI/UX notes, motion para`
- [ ] `C-UX-19` `ui` The headline resolves from random characters left to right at a fixed width. `src: UI/UX notes, motion para`
- [ ] `C-UX-20` `ui` The wire globe turns by squashing its meridian arcs. `src: UI/UX notes, motion para`
- [ ] `C-UX-21` `ui` The passcode caret blinks as a hard on-off flicker. `src: UI/UX notes, motion para`
- [ ] `C-UX-22` `ui` The menu button crosses its bars as a staggered gesture. `src: UI/UX notes, motion para`
- [ ] `C-UX-23` `ui` Under reduced motion the scroll smoothing stops. `src: UI/UX notes, reduced motion para`
- [ ] `C-UX-24` `ui` Hover steps an element one strength up the ink ladder. `src: UI/UX notes, motion para`
- [ ] `C-UX-25` `ui` The first-screen hairlines fade in after a deliberate hold. `src: UI/UX notes, motion para`
- [ ] `C-UX-26` `ui` The passcode ring changes state with the settling character. `src: UI/UX notes, motion para`
- [ ] `C-UX-27` `ui` The drawing beside the home statement draws itself, holds, then clears on a loop. `src: UI/UX notes, motion para`
- [ ] `C-UX-28` `capability` Under reduced motion the held band collapses to one screen. `src: UI/UX notes, reduced motion para`
- [ ] `C-UX-29` `ui` Under reduced motion the scramble renders final strings at once. `src: UI/UX notes, reduced motion para`
- [ ] `C-UX-30` `ui` Under reduced motion the passcode caret keeps blinking. `src: UI/UX notes, reduced motion para`
- [ ] `C-UX-31` `ui` The confirming control of the hold prompt names the hold as its action. `src: UI/UX notes, components para`
- [ ] `C-UX-32` `capability` Backspace in the passcode field clears the last digit. `src: UI/UX notes, components para`
- [ ] `C-UX-33` `ui` Pasting four digits fills all four passcode slots at once. `src: UI/UX notes, components para`
- [ ] `C-UX-34` `ui` The waiting ring steps from slot to slot as digits arrive. `src: UI/UX notes, components para`
- [ ] `C-UX-35` `ui` Every control shows resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, components para`
- [ ] `C-UX-36` `ui` Chrome controls carry a hit area covering their whole box. `src: UI/UX notes, components para`
- [ ] `C-UX-37` `ui` Each page leads with one primary action in the strongest ink. `src: UI/UX notes, primary action para`
- [ ] `C-UX-38` `ui` Below the breakpoint the four chrome controls collapse into a menu button. `src: UI/UX notes, responsive para`
- [ ] `C-UX-39` `ui` The phone menu closes on choosing an item. `src: Front-end specification, frame para 2`
- [ ] `C-UX-40` `ui` Below the breakpoint the tall nDrive card spans the full width. `src: Front-end specification, index para 2`
- [ ] `C-UX-41` `ui` Below the breakpoint the clock drops its zone with its region. `src: UI/UX notes, responsive para`
- [ ] `C-UX-42` `ui` Below the breakpoint the discipline label with the tagline hides. `src: UI/UX notes, responsive para`
- [ ] `C-UX-43` `ui` Below the breakpoint card kind labels hide. `src: UI/UX notes, responsive para`
- [ ] `C-UX-44` `ui` Touch devices show no latched hover state. `src: UI/UX notes, responsive para`
- [ ] `C-UX-45` `capability` At a narrow viewport the document never scrolls sideways. `src: UI/UX notes, responsive para`
- [ ] `C-UX-46` `capability` At a narrow viewport the menu button stays reachable. `src: UI/UX notes, responsive para`
- [ ] `C-UX-47` `ui` Body text meets WCAG AA contrast in both themes. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-48` `ui` The passcode prompt uses the body-prose strength of ink. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-49` `ui` Every interactive element shows a visible focus ring in reading order. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-50` `capability` The inner scroller responds to page down. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-51` `ui` The home page scrolls with page up, home, end, space. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-52` `ui` The contents drawer leaves focus free to move past. `src: Front-end specification, case-study para 5`
- [ ] `C-UX-53` `ui` Decorative drawings are hidden from assistive technology. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-54` `ui` Every touch target is at least 44 by 44 CSS pixels. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-55` `ui` Readable text is never smaller than 12 CSS pixels. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-56` `ui` Forced colours turn rings into system borders with hairlines kept. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-57` `capability` Each route carries banner, main plus contentinfo landmarks. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-58` `capability` A case study carries exactly one level-one heading. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-59` `literal` Refusal toasts open with the word `Refused`. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-60` `literal` The menu button is named `Menu`. `src: UI/UX notes, accessibility para`
- [ ] `C-UX-61` `ui` The index shows no tidy rows of equal boxes. `src: UI/UX notes, must-not para`
- [ ] `C-UX-62` `ui` Corners soften in steps: inline code least, card media barely, frames, figures, the footer more. `src: UI/UX notes, shape para`

## C-TR Technical requirements

- [ ] `C-TR-01` `ui` A wheel flick glides the page to a stop. `src: Technical requirements, browser para`
- [ ] `C-TR-02` `ui` At the smallest widths about a dozen flat sticker shapes float over the first screen. `src: Technical requirements, three-dimensional layer para`
- [ ] `C-TR-03` `capability` Every public page arrives as complete server-rendered HTML. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` `GET /api/health` returns 200 once ready. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` Passcodes are stored only as hashes. `src: Technical requirements para 1`
- [ ] `C-TR-06` `capability` The case study HTML carries the title, the headings plus the footer. `src: Technical requirements, browser para`
- [ ] `C-TR-07` `capability` The window stays still as the scroller element scrolls. `src: Technical requirements, browser para`
- [ ] `C-TR-08` `literal` The scroller carries the attribute `data-scroller`. `src: Technical requirements, browser para`
- [ ] `C-TR-09` `literal` The root carries `data-page` with the value `case-study` on a case study. `src: Technical requirements, browser para`
- [ ] `C-TR-10` `literal` The index container carries `data-index-grid`. `src: Technical requirements, browser para`
- [ ] `C-TR-11` `literal` Each card article carries `data-order` with its position. `src: Technical requirements, browser para`
- [ ] `C-TR-12` `literal` The held band carries `data-band` with the value `held`. `src: Technical requirements, browser para`
- [ ] `C-TR-13` `constraint` The site serves no image, audio or model file of its own. `src: Technical requirements, asset para`
- [ ] `C-TR-14` `constraint` Fonts ship in one web format with no desktop format. `src: Technical requirements, asset para`
- [ ] `C-TR-15` `literal` The home root carries `data-page` with the value `home`. `src: Technical requirements, browser para`
- [ ] `C-TR-16` `literal` The passcode screen root carries `data-page` with the value `gate`. `src: Technical requirements, browser para`
- [ ] `C-TR-17` `literal` The unlocked studio root carries `data-page` with the value `studio`. `src: Technical requirements, browser para`
- [ ] `C-TR-18` `literal` The not-found root carries `data-page` with the value `not-found`. `src: Technical requirements, browser para`
- [ ] `C-TR-19` `literal` The home bands carry `data-band` values `first-screen`, `statement`, `index`, `held`, `contact`. `src: Technical requirements, browser para`
- [ ] `C-TR-20` `ui` Card media are soft two-colour gradients with the title set faintly across. `src: Technical requirements, asset para`
- [ ] `C-TR-21` `ui` The scene arrival moves no text on the first screen. `src: Technical requirements, loading para`
- [ ] `C-TR-22` `ui` The rear surface shows a glossy hello tube over a pale blue field with drifting light streaks. `src: Technical requirements, scene para`
- [ ] `C-TR-23` `ui` Without the renderer the first screen still looks finished. `src: Technical requirements, scene para`
- [ ] `C-TR-24` `constraint` The gate response carries only the boolean. `src: Technical requirements, gate para`

## C-DM Data model

- [ ] `C-DM-01` `data` The site profile holds the brand `atlas` with the suffix `.design`. `src: Data model, site_profile`
- [ ] `C-DM-02` `literal` The contact email is `studio.rin@example.com`. `src: Data model, site_profile`
- [ ] `C-DM-03` `literal` The site profile names the person `Rin Alvez`. `src: Data model, site_profile`
- [ ] `C-DM-04` `literal` The first social link leads to `https://www.example.com/rin/x`. `src: Data model, social_link`
- [ ] `C-DM-05` `literal` The other social links lead to `https://www.example.com/rin/community` then `https://www.example.com/rin/github`. `src: Data model, social_link`
- [ ] `C-DM-06` `data` The redaction length is six. `src: Data model, site_profile`
- [ ] `C-DM-07` `literal` The social links read `Twitter/X`, `Community`, `GitHub` in order. `src: Data model, social_link`
- [ ] `C-DM-08` `data` The case_study slug is unique across every case study. `src: Data model, case_study`
- [ ] `C-DM-09` `literal` The case_study status is one of `draft`, `stub`, `published`. `src: Data model, case_study`
- [ ] `C-DM-10` `data` No two project_card rows share one case_study_id. `src: Data model, project_card`
- [ ] `C-DM-11` `data` Listed project_card rows never share a position. `src: Data model, project_card`
- [ ] `C-DM-12` `data` A figure row records the object key of the stored bytes. `src: Data model, figure`
- [ ] `C-DM-13` `data` One case study never holds two figures with one content hash. `src: Data model, figure`
- [ ] `C-DM-14` `data` A slug_redirect row exists for every retired slug. `src: Data model, slug_redirect`
- [ ] `C-DM-15` `data` Two passcode_gate rows exist for the two gated paths. `src: Data model, passcode_gate`
- [ ] `C-DM-16` `data` A page_view row stores the route with the time. `src: Data model, page_view`
- [ ] `C-DM-17` `data` A page_view row holds no visitor identifier. `src: Data model, page_view`
- [ ] `C-DM-18` `data` A released grant leaves its passcode_grant row marked released. `src: Data model, passcode_grant`
- [ ] `C-DM-19` `data` The year label is computed on read. `src: Data model, derived para`
- [ ] `C-DM-20` `literal` The seeded draft `tidewater` is titled `Tidewater Sketchbook`. `src: Data model, seed table row 8`
- [ ] `C-DM-21` `literal` The seeded stub is `teamharbor`. `src: Data model, seed table row 6`
- [ ] `C-DM-22` `literal` The seeded Coast Icon case study was composed at `390x844`. `src: Data model, seed table row 5`
- [ ] `C-DM-23` `constraint` Each seeded row exists exactly once. `src: Data model, seed para`
- [ ] `C-DM-24` `literal` The credential file states there are no login accounts, listing `/studio` beside `5093` with `/field-notes` beside `2718`. `src: Data model, passcode paragraph`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` The contact band mail link leads to `mailto:studio.rin@example.com`. `src: Front-end specification, contact para`
- [ ] `C-FE-02` `ui` The frame keeps a top bar with a bottom bar pinned over every route. `src: Front-end specification, frame para 1`
- [ ] `C-FE-03` `ui` The globe draws one ellipse, one horizontal line, six meridian arcs. `src: Front-end specification, frame para 3`
- [ ] `C-FE-04` `ui` A small ring beside the sound control fills as the bed loads. `src: Front-end specification, frame para 3`
- [ ] `C-FE-05` `ui` The centred loader grows its capsule fill from the left end. `src: Front-end specification, loader para`
- [ ] `C-FE-06` `literal` The discipline label reads `Design &` over `Engineering`. `src: Front-end specification, first screen para 1`
- [ ] `C-FE-07` `literal` The tagline reads `Thinking in systems.` over `Designing with care.` `src: Front-end specification, first screen para 1`
- [ ] `C-FE-08` `literal` The redaction run carries the attribute `data-redacted`. `src: Front-end specification, first screen para 1`
- [ ] `C-FE-09` `capability` The redaction run is announced once as redacted. `src: Front-end specification, first screen para 1`
- [ ] `C-FE-10` `literal` The headline lines read `I bring`, `craft & taste`, `to digital work`. `src: Front-end specification, first screen para 2`
- [ ] `C-FE-11` `capability` The headline is one level-one heading. `src: Front-end specification, first screen para 2`
- [ ] `C-FE-12` `ui` Hairlines with a dotted field sit over the first screen only. `src: Front-end specification, first screen para 2`
- [ ] `C-FE-13` `ui` A lime scribble overhangs the square figure beside the statement. `src: Front-end specification, statement para`
- [ ] `C-FE-14` `literal` The primary statement opens `I explore how to shape AI-era workflows`. `src: Front-end specification, statement para`
- [ ] `C-FE-15` `literal` The secondary statement reads the pinned building-Kindling sentence. `src: Front-end specification, statement para`
- [ ] `C-FE-16` `literal` The introduction carries the pinned leading-design-engineering phrase before the redaction run. `src: Front-end specification, first screen para 1`
- [ ] `C-FE-17` `literal` The introduction closes `Outside work, I build design tools for team efficiency.` `src: Front-end specification, first screen para 1`
- [ ] `C-FE-18` `literal` The index band carries the hidden heading `Selected work`. `src: Front-end specification, index para 1`
- [ ] `C-FE-19` `ui` A card title truncates with an ellipsis rather than wrapping. `src: Front-end specification, index para 1`
- [ ] `C-FE-20` `ui` Below the breakpoint a card spanning five or more columns spans the full width with the rest two to a row. `src: Front-end specification, index para 2`
- [ ] `C-FE-21` `literal` The held band shows `Innovate`, `with`, `purpose`. `src: Front-end specification, held statement para`
- [ ] `C-FE-22` `ui` The held band pins one screen as its ground colour changes. `src: Front-end specification, held statement para`
- [ ] `C-FE-23` `literal` The contact band shows `Let's`, `Create`, `Something`, `Extraordinary`. `src: Front-end specification, contact para`
- [ ] `C-FE-24` `ui` The contact words alternate their alignment down the block. `src: Front-end specification, contact para`
- [ ] `C-FE-25` `literal` The contact band carries the anchor `#contact`. `src: Front-end specification, contact para`
- [ ] `C-FE-26` `literal` The index band carries the anchor `#selected-work`. `src: Front-end specification, index para 1`
- [ ] `C-FE-27` `literal` Code line numbers carry `data-line-number`. `src: Front-end specification, case-study para 2`
- [ ] `C-FE-28` `capability` Code line numbers cannot be selected. `src: Front-end specification, case-study para 2`
- [ ] `C-FE-29` `ui` A hash glyph sits in the left margin beside every heading. `src: Front-end specification, case-study para 3`
- [ ] `C-FE-30` `ui` The reading rail fades in during scrolling then fills from the top. `src: Front-end specification, case-study para 4`
- [ ] `C-FE-31` `literal` The reading rail carries `data-reading-rail`. `src: Front-end specification, case-study para 4`
- [ ] `C-FE-32` `literal` The contents drawer is a navigation landmark named `Contents`. `src: Front-end specification, case-study para 5`
- [ ] `C-FE-33` `ui` The contents drawer opens by growing sideways from the left edge. `src: Front-end specification, case-study para 5`
- [ ] `C-FE-34` `ui` The contents drawer marks the heading in view. `src: Front-end specification, case-study para 5`
- [ ] `C-FE-35` `ui` Drawer rows indent by heading level. `src: Front-end specification, case-study para 5`
- [ ] `C-FE-36` `ui` Inline code sits on a faint wash. `src: Front-end specification, case-study para 1`
- [ ] `C-FE-37` `ui` Inline links are underlined. `src: Front-end specification, case-study para 1`
- [ ] `C-FE-38` `ui` A code block header bar carries the language word on the left. `src: Front-end specification, case-study para 2`
- [ ] `C-FE-39` `ui` The COPY label change keeps the header bar at one size. `src: Front-end specification, case-study para 2`
- [ ] `C-FE-40` `literal` The drawer opener is named `Contents`. `src: Front-end specification, case-study para 5`
- [ ] `C-FE-41` `constraint` A case study with no headings shows no drawer opener. `src: Front-end specification, case-study para 5`
- [ ] `C-FE-42` `ui` Clicking a heading hash glides to the heading with its slug in the address. `src: Front-end specification, case-study para 3`
- [ ] `C-FE-43` `ui` Opening a case-study address with a fragment lands on that heading. `src: Front-end specification, case-study para 3`
- [ ] `C-FE-44` `ui` Dragging the reading rail scrubs through the article. `src: Front-end specification, case-study para 4`
- [ ] `C-FE-45` `ui` Below the breakpoint the case-study title steps down with a slimmer rail. `src: UI/UX notes, responsive para`
- [ ] `C-FE-46` `ui` Below the breakpoint the case-study footer shows a Links group. `src: Front-end specification, case-study para 6`
- [ ] `C-FE-47` `capability` The case study document title is its title. `src: Front-end specification, case-study para 7`
- [ ] `C-FE-48` `literal` The home document title is `atlas`, a space, a copyright sign, a space, the four-digit current year. `src: Front-end specification, case-study para 7`
- [ ] `C-FE-49` `capability` The passcode screen shares the home document title format. `src: Front-end specification, case-study para 7`
- [ ] `C-FE-50` `literal` The footer lists `Metadata`, `Last Updated`, `Dimensions`, `Characters`. `src: Front-end specification, case-study para 6`
- [ ] `C-FE-51` `literal` The passcode screen reads `Please enter passcode`. `src: Front-end specification, passcode para`
- [ ] `C-FE-52` `literal` The hidden input label opens with `Passcode for`. `src: Front-end specification, passcode para`
- [ ] `C-FE-53` `literal` Each slot carries `data-slot-state` of `empty`, `next` or `filled`. `src: Front-end specification, passcode para`
- [ ] `C-FE-54` `ui` Four round slots sit centred beneath the prompt. `src: Front-end specification, passcode para`
- [ ] `C-FE-55` `literal` Each studio row carries `data-status` with its status. `src: Front-end specification, studio para`
- [ ] `C-FE-56` `ui` Studio statuses read as words rather than colour. `src: Front-end specification, studio para`
- [ ] `C-FE-57` `ui` The studio editor lists the headings with their slugs as the body is typed. `src: Front-end specification, studio para`
- [ ] `C-FE-58` `ui` Each figure thumbnail in the studio shows its intrinsic size. `src: Front-end specification, studio para`
- [ ] `C-FE-59` `ui` The not-found page centres its line above one primary action. `src: Front-end specification, not-found para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product loads no third-party analytics. `src: Constraints para 2`
- [ ] `C-CN-02` `constraint` Public pages set no cookie before a passcode is accepted. `src: Constraints para 2`
- [ ] `C-CN-03` `constraint` Outside links point at `www.example.com` addresses. `src: Constraints para 3`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The API is served on the same origin under the api prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-03` `literal` The container port `4173` sits behind `APP_PUBLIC_PORT`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The server binds every interface so the app answers from outside its container. `src: Deployment contract bullet 9`
- [ ] `C-DC-05` `contract` The app keeps answering after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-06` `contract` The credential file sits at `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` Reserved directories `.browser_screenshots/` with `.downloads/` exist empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-08` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract, API shapes para`
- [ ] `C-DC-09` `contract` A refusal carries a JSON body naming its error code. `src: Deployment contract, API shapes para`
- [ ] `C-DC-10` `contract` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract, API shapes para`
- [ ] `C-DC-11` `literal` `GET /api/site` returns the profile with its socials. `src: Deployment contract, API shapes table`
- [ ] `C-DC-12` `literal` `POST /api/studio/case-studies/{id}/figures` accepts a multipart upload. `src: Deployment contract, API shapes table`
- [ ] `C-DC-13` `literal` `PATCH /api/studio/case-studies/{id}` updates a case study. `src: Deployment contract, API shapes table`
- [ ] `C-DC-14` `literal` `POST /api/studio/case-studies/{id}/hold` returns status draft. `src: Deployment contract, API shapes table`
- [ ] `C-DC-15` `literal` `POST /api/studio/case-studies` creates a case study. `src: Deployment contract, API shapes table`
- [ ] `C-DC-16` `literal` `GET /api/studio/case-studies/{id}` returns one case study. `src: Deployment contract, API shapes table`
- [ ] `C-DC-17` `literal` `POST /api/studio/case-studies/{id}/publish` returns status published. `src: Deployment contract, API shapes table`
- [ ] `C-DC-18` `literal` `POST /api/studio/case-studies/{id}/stub` returns status stub. `src: Deployment contract, API shapes table`
- [ ] `C-DC-19` `constraint` A figure endpoint never reports success without an object in the bucket. `src: Deployment contract, no mocks para`

## Pinned literals

| Value | Why pinned | Item | Citation |
|---|---|---|---|
| `5093` | pinned by the brief at the citation beside it | C-RL-17 | User roles, passcode table row 1 |
| `/studio` | pinned by the brief at the citation beside it | C-RL-17 | User roles, passcode table row 1 |
| `2718` | pinned by the brief at the citation beside it | C-RL-18 | User roles, passcode table row 2 |
| `/field-notes` | pinned by the brief at the citation beside it | C-RL-18 | User roles, passcode table row 2 |
| `POST /api/passcode` | pinned by the brief at the citation beside it | C-CF-01 | Core features, Auth para 1 |
| `rate_limited` | pinned by the brief at the citation beside it | C-CF-12 | Core features rule 4 |
| `POST /api/passcode/release` | pinned by the brief at the citation beside it | C-CF-21 | Core features rule 7 |
| `GET /api/projects` | pinned by the brief at the citation beside it | C-CF-26 | Core features rule 10 |
| `position_taken` | pinned by the brief at the citation beside it | C-CF-32 | Core features rule 12 |
| `invalid_placement` | pinned by the brief at the citation beside it | C-CF-36 | Core features rule 13 |
| `16:9` | pinned by the brief at the citation beside it | C-CF-37 | Core features rule 13 |
| `1.54:1` | pinned by the brief at the citation beside it | C-CF-37 | Core features rule 13 |
| `0.71:1` | pinned by the brief at the citation beside it | C-CF-37 | Core features rule 13 |
| `1:1` | pinned by the brief at the citation beside it | C-CF-37 | Core features rule 13 |
| `2025` | pinned by the brief at the citation beside it | C-CF-39 | Core features rule 14 |
| `2024-2026` | pinned by the brief at the citation beside it | C-CF-40 | Core features rule 14 |
| `invalid_media_alt` | pinned by the brief at the citation beside it | C-CF-42 | Core features rule 15 |
| `5, 1, 7, 6, 10, 1, 5, 9, 6, 10` | pinned by the brief at the citation beside it | C-CF-47 | Core features rule 16 |
| `Kindling` | pinned by the brief at the citation beside it | C-CF-48 | Core features, seeded cards table row 1 |
| `GlyphSymbols` | pinned by the brief at the citation beside it | C-CF-49 | Core features, seeded cards table row 4 |
| `https://www.example.com/plugins/glyphsymbols` | pinned by the brief at the citation beside it | C-CF-49 | Core features, seeded cards table row 4 |
| `DuskMode` | pinned by the brief at the citation beside it | C-CF-50 | Core features, seeded cards table row 5 |
| `tools` | pinned by the brief at the citation beside it | C-CF-50 | Core features, seeded cards table row 5 |
| `nDrive` | pinned by the brief at the citation beside it | C-CF-51 | Core features, seeded cards table row 6 |
| `0.71:1` | pinned by the brief at the citation beside it | C-CF-51 | Core features, seeded cards table row 6 |
| `Loop: See Hear Touch` | pinned by the brief at the citation beside it | C-CF-52 | Core features, seeded cards table row 9 |
| `event` | pinned by the brief at the citation beside it | C-CF-52 | Core features, seeded cards table row 9 |
| `DuskMode` | pinned by the brief at the citation beside it | C-CF-53 | Core features, seeded cards table row 5 |
| `https://www.example.com/plugins/duskmode` | pinned by the brief at the citation beside it | C-CF-53 | Core features, seeded cards table row 5 |
| `https://www.example.com/events/see-hear-touch` | pinned by the brief at the citation beside it | C-CF-54 | Core features, seeded cards table row 9 |
| `https://www.example.com/events/system-design` | pinned by the brief at the citation beside it | C-CF-55 | Core features, seeded cards table row 10 |
| `Coding Project` | pinned by the brief at the citation beside it | C-CF-57 | Core features, seeded cards table rows 1 to 3 |
| `GET /api/case-studies/{slug}` | pinned by the brief at the citation beside it | C-CF-60 | Core features rule 17 |
| `/ndrive` | pinned by the brief at the citation beside it | C-CF-66 | Core features rule 19 |
| `invalid_slug` | pinned by the brief at the citation beside it | C-CF-67 | Core features rule 20 |
| `studio` | pinned by the brief at the citation beside it | C-CF-68 | Core features rule 20 |
| `slug_reserved` | pinned by the brief at the citation beside it | C-CF-68 | Core features rule 20 |
| `slug_taken` | pinned by the brief at the citation beside it | C-CF-69 | Core features rule 20 |
| `invalid_heading_levels` | pinned by the brief at the citation beside it | C-CF-74 | Core features rule 22 |
| `Sync, conflicts & recovery` | pinned by the brief at the citation beside it | C-CF-77 | Core features rule 23 |
| `sync-conflicts-recovery` | pinned by the brief at the citation beside it | C-CF-77 | Core features rule 23 |
| `Notes` | pinned by the brief at the citation beside it | C-CF-78 | Core features rule 23 |
| `notes-2` | pinned by the brief at the citation beside it | C-CF-78 | Core features rule 23 |
| `1,602` | pinned by the brief at the citation beside it | C-CF-82 | Core features rule 24 |
| `1440x900` | pinned by the brief at the citation beside it | C-CF-83 | Core features rule 25 |
| `Jan 15, 2026` | pinned by the brief at the citation beside it | C-CF-84 | Core features rule 25 |
| `Download Almanac Mono` | pinned by the brief at the citation beside it | C-CF-89 | Core features rule 27 |
| `https://www.example.com/almanac-mono/download` | pinned by the brief at the citation beside it | C-CF-89 | Core features rule 27 |
| `Work in progress - this page is not finished yet.` | pinned by the brief at the citation beside it | C-CF-90 | Core features rule 28 |
| `https://www.example.com/teamharbor` | pinned by the brief at the citation beside it | C-CF-92 | Core features rule 28 |
| `Notes I keep for myself, shared with the people who ask.` | pinned by the brief at the citation beside it | C-CF-93 | Core features rule 29 |
| `case-studies/{case_study_id}/figures/{sha256_of_bytes}.{ext}` | pinned by the brief at the citation beside it | C-CF-96 | Core features rule 30 |
| `alt_text_required` | pinned by the brief at the citation beside it | C-CF-99 | Core features rule 32 |
| `invalid_dimensions` | pinned by the brief at the citation beside it | C-CF-100 | Core features rule 32 |
| `unsupported_type` | pinned by the brief at the citation beside it | C-CF-102 | Core features rule 32 |
| `5,242,880` | pinned by the brief at the citation beside it | C-CF-103 | Core features rule 32 |
| `file_too_large` | pinned by the brief at the citation beside it | C-CF-103 | Core features rule 32 |
| `GET /api/figures/{id}` | pinned by the brief at the citation beside it | C-CF-107 | Core features rule 34 |
| `GET /api/studio/case-studies` | pinned by the brief at the citation beside it | C-CF-113 | Core features rule 36 |
| `incomplete` | pinned by the brief at the citation beside it | C-CF-115 | Core features rule 37 |
| `invalid_field` | pinned by the brief at the citation beside it | C-CF-116 | Core features rule 37 |
| `atlas` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 42 |
| `.design` | pinned by the brief at the citation beside it | C-CF-129 | Core features rule 42 |
| `Work` | pinned by the brief at the citation beside it | C-CF-130 | Core features rule 42 |
| `Contact` | pinned by the brief at the citation beside it | C-CF-130 | Core features rule 42 |
| `THEME[A]` | pinned by the brief at the citation beside it | C-CF-134 | Core features rule 43 |
| `aria-pressed` | pinned by the brief at the citation beside it | C-CF-134 | Core features rule 43 |
| `light` | pinned by the brief at the citation beside it | C-CF-135 | Core features rule 43 |
| `dark` | pinned by the brief at the citation beside it | C-CF-135 | Core features rule 43 |
| `SOUND[` | pinned by the brief at the citation beside it | C-CF-140 | Core features rule 44 |
| `GMT+8` | pinned by the brief at the citation beside it | C-CF-145 | Core features rule 45 |
| `CN` | pinned by the brief at the citation beside it | C-CF-145 | Core features rule 45 |
| `0720 X 0450 Y` | pinned by the brief at the citation beside it | C-CF-146 | Core features rule 45 |
| `Nothing is filed at this address.` | pinned by the brief at the citation beside it | C-CF-149 | Core features rule 46 |
| `Back to the index` | pinned by the brief at the citation beside it | C-CF-150 | Core features rule 46 |
| `GET /api/studio/page-views` | pinned by the brief at the citation beside it | C-CF-153 | Core features rule 48 |
| `/wasm-design-utils` | pinned by the brief at the citation beside it | C-UF-01 | User flow, routes table |
| `/teamharbor` | pinned by the brief at the citation beside it | C-UF-02 | User flow, routes table |
| `/coast-icon` | pinned by the brief at the citation beside it | C-UF-03 | User flow, routes table |
| `/kindling` | pinned by the brief at the citation beside it | C-UF-04 | User flow, routes table |
| `#offline-then-online` | pinned by the brief at the citation beside it | C-UF-09 | User flow, journey 2 |
| `COPY` | pinned by the brief at the citation beside it | C-UF-10 | User flow, journey 2 |
| `COPIED` | pinned by the brief at the citation beside it | C-UF-10 | User flow, journey 2 |
| `That code is not right. Try again.` | pinned by the brief at the citation beside it | C-UF-13 | User flow, journey 4 |
| `Too many attempts. Wait a minute and try again.` | pinned by the brief at the citation beside it | C-UF-14 | User flow, journey 4 |
| `Case studies` | pinned by the brief at the citation beside it | C-UF-15 | User flow, journey 5 |
| `Index preview` | pinned by the brief at the citation beside it | C-UF-15 | User flow, journey 5 |
| `Page views` | pinned by the brief at the citation beside it | C-UF-15 | User flow, journey 5 |
| `Lock studio` | pinned by the brief at the citation beside it | C-UF-15 | User flow, journey 5 |
| `New case study` | pinned by the brief at the citation beside it | C-UF-16 | User flow, journey 5 |
| `Publish` | pinned by the brief at the citation beside it | C-UF-17 | User flow, journey 5 |
| `Mark as stub` | pinned by the brief at the citation beside it | C-UF-17 | User flow, journey 5 |
| `Hold as draft` | pinned by the brief at the citation beside it | C-UF-17 | User flow, journey 5 |
| `Published to the index.` | pinned by the brief at the citation beside it | C-UF-19 | User flow, journey 5 |
| `Held as a draft.` | pinned by the brief at the citation beside it | C-UF-20 | User flow, journey 5 |
| `Marked as a stub.` | pinned by the brief at the citation beside it | C-UF-21 | User flow, journey 5 |
| `Refused. Another card already holds that position.` | pinned by the brief at the citation beside it | C-UF-22 | User flow, journey 6 |
| `Refused` | pinned by the brief at the citation beside it | C-UX-59 | UI/UX notes, accessibility para |
| `Menu` | pinned by the brief at the citation beside it | C-UX-60 | UI/UX notes, accessibility para |
| `data-scroller` | pinned by the brief at the citation beside it | C-TR-08 | Technical requirements, browser para |
| `data-page` | pinned by the brief at the citation beside it | C-TR-09 | Technical requirements, browser para |
| `case-study` | pinned by the brief at the citation beside it | C-TR-09 | Technical requirements, browser para |
| `data-index-grid` | pinned by the brief at the citation beside it | C-TR-10 | Technical requirements, browser para |
| `data-order` | pinned by the brief at the citation beside it | C-TR-11 | Technical requirements, browser para |
| `data-band` | pinned by the brief at the citation beside it | C-TR-12 | Technical requirements, browser para |
| `held` | pinned by the brief at the citation beside it | C-TR-12 | Technical requirements, browser para |
| `data-page` | pinned by the brief at the citation beside it | C-TR-15 | Technical requirements, browser para |
| `home` | pinned by the brief at the citation beside it | C-TR-15 | Technical requirements, browser para |
| `data-page` | pinned by the brief at the citation beside it | C-TR-16 | Technical requirements, browser para |
| `gate` | pinned by the brief at the citation beside it | C-TR-16 | Technical requirements, browser para |
| `data-page` | pinned by the brief at the citation beside it | C-TR-17 | Technical requirements, browser para |
| `studio` | pinned by the brief at the citation beside it | C-TR-17 | Technical requirements, browser para |
| `data-page` | pinned by the brief at the citation beside it | C-TR-18 | Technical requirements, browser para |
| `not-found` | pinned by the brief at the citation beside it | C-TR-18 | Technical requirements, browser para |
| `data-band` | pinned by the brief at the citation beside it | C-TR-19 | Technical requirements, browser para |
| `first-screen` | pinned by the brief at the citation beside it | C-TR-19 | Technical requirements, browser para |
| `statement` | pinned by the brief at the citation beside it | C-TR-19 | Technical requirements, browser para |
| `index` | pinned by the brief at the citation beside it | C-TR-19 | Technical requirements, browser para |
| `held` | pinned by the brief at the citation beside it | C-TR-19 | Technical requirements, browser para |
| `contact` | pinned by the brief at the citation beside it | C-TR-19 | Technical requirements, browser para |
| `studio.rin@example.com` | pinned by the brief at the citation beside it | C-DM-02 | Data model, site_profile |
| `Rin Alvez` | pinned by the brief at the citation beside it | C-DM-03 | Data model, site_profile |
| `https://www.example.com/rin/x` | pinned by the brief at the citation beside it | C-DM-04 | Data model, social_link |
| `https://www.example.com/rin/community` | pinned by the brief at the citation beside it | C-DM-05 | Data model, social_link |
| `https://www.example.com/rin/github` | pinned by the brief at the citation beside it | C-DM-05 | Data model, social_link |
| `Twitter/X` | pinned by the brief at the citation beside it | C-DM-07 | Data model, social_link |
| `Community` | pinned by the brief at the citation beside it | C-DM-07 | Data model, social_link |
| `GitHub` | pinned by the brief at the citation beside it | C-DM-07 | Data model, social_link |
| `draft` | pinned by the brief at the citation beside it | C-DM-09 | Data model, case_study |
| `stub` | pinned by the brief at the citation beside it | C-DM-09 | Data model, case_study |
| `published` | pinned by the brief at the citation beside it | C-DM-09 | Data model, case_study |
| `tidewater` | pinned by the brief at the citation beside it | C-DM-20 | Data model, seed table row 8 |
| `Tidewater Sketchbook` | pinned by the brief at the citation beside it | C-DM-20 | Data model, seed table row 8 |
| `teamharbor` | pinned by the brief at the citation beside it | C-DM-21 | Data model, seed table row 6 |
| `390x844` | pinned by the brief at the citation beside it | C-DM-22 | Data model, seed table row 5 |
| `/studio` | pinned by the brief at the citation beside it | C-DM-24 | Data model, passcode paragraph |
| `5093` | pinned by the brief at the citation beside it | C-DM-24 | Data model, passcode paragraph |
| `/field-notes` | pinned by the brief at the citation beside it | C-DM-24 | Data model, passcode paragraph |
| `2718` | pinned by the brief at the citation beside it | C-DM-24 | Data model, passcode paragraph |
| `mailto:studio.rin@example.com` | pinned by the brief at the citation beside it | C-FE-01 | Front-end specification, contact para |
| `Design &` | pinned by the brief at the citation beside it | C-FE-06 | Front-end specification, first screen para 1 |
| `Engineering` | pinned by the brief at the citation beside it | C-FE-06 | Front-end specification, first screen para 1 |
| `Thinking in systems.` | pinned by the brief at the citation beside it | C-FE-07 | Front-end specification, first screen para 1 |
| `Designing with care.` | pinned by the brief at the citation beside it | C-FE-07 | Front-end specification, first screen para 1 |
| `data-redacted` | pinned by the brief at the citation beside it | C-FE-08 | Front-end specification, first screen para 1 |
| `I bring` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, first screen para 2 |
| `craft & taste` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, first screen para 2 |
| `to digital work` | pinned by the brief at the citation beside it | C-FE-10 | Front-end specification, first screen para 2 |
| `I explore how to shape AI-era workflows` | pinned by the brief at the citation beside it | C-FE-14 | Front-end specification, statement para |
| `I'm building Kindling, and previously worked on Orchard nDrive, Teamharbor, and Hirebase.` | pinned by the brief at the citation beside it | C-FE-15 | Front-end specification, statement para |
| `leading Design Engineering and AI exploration at` | pinned by the brief at the citation beside it | C-FE-16 | Front-end specification, first screen para 1 |
| `Outside work, I build design tools for team efficiency.` | pinned by the brief at the citation beside it | C-FE-17 | Front-end specification, first screen para 1 |
| `Selected work` | pinned by the brief at the citation beside it | C-FE-18 | Front-end specification, index para 1 |
| `Innovate` | pinned by the brief at the citation beside it | C-FE-21 | Front-end specification, held statement para |
| `with` | pinned by the brief at the citation beside it | C-FE-21 | Front-end specification, held statement para |
| `purpose` | pinned by the brief at the citation beside it | C-FE-21 | Front-end specification, held statement para |
| `Let's` | pinned by the brief at the citation beside it | C-FE-23 | Front-end specification, contact para |
| `Create` | pinned by the brief at the citation beside it | C-FE-23 | Front-end specification, contact para |
| `Something` | pinned by the brief at the citation beside it | C-FE-23 | Front-end specification, contact para |
| `Extraordinary` | pinned by the brief at the citation beside it | C-FE-23 | Front-end specification, contact para |
| `#contact` | pinned by the brief at the citation beside it | C-FE-25 | Front-end specification, contact para |
| `#selected-work` | pinned by the brief at the citation beside it | C-FE-26 | Front-end specification, index para 1 |
| `data-line-number` | pinned by the brief at the citation beside it | C-FE-27 | Front-end specification, case-study para 2 |
| `data-reading-rail` | pinned by the brief at the citation beside it | C-FE-31 | Front-end specification, case-study para 4 |
| `Contents` | pinned by the brief at the citation beside it | C-FE-32 | Front-end specification, case-study para 5 |
| `Contents` | pinned by the brief at the citation beside it | C-FE-40 | Front-end specification, case-study para 5 |
| `atlas` | pinned by the brief at the citation beside it | C-FE-48 | Front-end specification, case-study para 7 |
| `Metadata` | pinned by the brief at the citation beside it | C-FE-50 | Front-end specification, case-study para 6 |
| `Last Updated` | pinned by the brief at the citation beside it | C-FE-50 | Front-end specification, case-study para 6 |
| `Dimensions` | pinned by the brief at the citation beside it | C-FE-50 | Front-end specification, case-study para 6 |
| `Characters` | pinned by the brief at the citation beside it | C-FE-50 | Front-end specification, case-study para 6 |
| `Please enter passcode` | pinned by the brief at the citation beside it | C-FE-51 | Front-end specification, passcode para |
| `Passcode for` | pinned by the brief at the citation beside it | C-FE-52 | Front-end specification, passcode para |
| `data-slot-state` | pinned by the brief at the citation beside it | C-FE-53 | Front-end specification, passcode para |
| `empty` | pinned by the brief at the citation beside it | C-FE-53 | Front-end specification, passcode para |
| `next` | pinned by the brief at the citation beside it | C-FE-53 | Front-end specification, passcode para |
| `filled` | pinned by the brief at the citation beside it | C-FE-53 | Front-end specification, passcode para |
| `data-status` | pinned by the brief at the citation beside it | C-FE-55 | Front-end specification, studio para |
| `4173` | pinned by the brief at the citation beside it | C-DC-03 | Deployment contract bullet 1 |
| `APP_PUBLIC_PORT` | pinned by the brief at the citation beside it | C-DC-03 | Deployment contract bullet 1 |
| `GET /api/site` | pinned by the brief at the citation beside it | C-DC-11 | Deployment contract, API shapes table |
| `POST /api/studio/case-studies/{id}/figures` | pinned by the brief at the citation beside it | C-DC-12 | Deployment contract, API shapes table |
| `PATCH /api/studio/case-studies/{id}` | pinned by the brief at the citation beside it | C-DC-13 | Deployment contract, API shapes table |
| `POST /api/studio/case-studies/{id}/hold` | pinned by the brief at the citation beside it | C-DC-14 | Deployment contract, API shapes table |
| `POST /api/studio/case-studies` | pinned by the brief at the citation beside it | C-DC-15 | Deployment contract, API shapes table |
| `GET /api/studio/case-studies/{id}` | pinned by the brief at the citation beside it | C-DC-16 | Deployment contract, API shapes table |
| `POST /api/studio/case-studies/{id}/publish` | pinned by the brief at the citation beside it | C-DC-17 | Deployment contract, API shapes table |
| `POST /api/studio/case-studies/{id}/stub` | pinned by the brief at the citation beside it | C-DC-18 | Deployment contract, API shapes table |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact colour value behind every named role | C-UX-03 | carried as family, tone and shade by design, so no value exists to match |
| the three type families, left to the builder by character | C-UX-11 | the brief describes each family by character and leaves the choice open |
| the exact durations and curves of every motion | C-UX-17 | the brief describes the motion character and hands the values to the builder |
| the media description text of each seeded card | C-CF-41 | the brief requires a description per card without giving the words |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 10 | 10 |
| User roles | 18 | 18 |
| Core features | 157 | 157 |
| User flow | 26 | 26 |
| UI and UX notes | 62 | 62 |
| Technical requirements | 24 | 24 |
| Data model | 24 | 24 |
| Front-end specification | 59 | 59 |
| Constraints | 3 | 3 |
| Deployment contract | 19 | 19 |

`## Definition of done` produces no items. Every clause in it restates an ask already
carried by `## Core features`, and a restatement folds into the item it restates.

The sentence column counts carried asks, one per item: a design ask that spans several
sentences of `## UI/UX notes` or `## Front-end specification` is counted once, and every
ask not carried is listed below with its reason.

Asks withdrawn because no channel can observe them, recorded rather than carried:
the named server libraries and the rendering library choice, the structured log
destination, the constant-time comparison and the equal response time of a refusal
and a success, a success never counting toward the lock, the salted form of the
stored hash, figure bytes never touching the container disk, the device pixel cap
and refresh-rate budget of the scene, the scene loop stopping off screen, the first
contentful paint budget, zero font and scene layout shift, the metric match of the
font fallbacks, the named scene objects, the audio synthesis recipe, the scale
targets, the absence of mail sending and outbound calls, the placeholder nature of
the seeded prose, the studio keeping typing when a grant ends mid-edit, and the
empty states of the index, the studio table and the page-view list and the fallback of a
figure that fails to load, which a seeded
app never shows. Each is a real requirement of the brief and none of them is graded.
