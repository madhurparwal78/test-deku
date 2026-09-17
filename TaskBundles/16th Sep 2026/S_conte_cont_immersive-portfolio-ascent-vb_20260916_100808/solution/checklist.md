# Checklist: Immersive Portfolio Ascent

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 436
Unpinned values flagged: 1

## C-OV Overview

- [ ] `C-OV-01` `capability` The home route delivers the portfolio as one continuous real-time three-dimensional scene the visitor travels through. `src: Overview para 2`
- [ ] `C-OV-02` `constraint` The home route page itself never scrolls. `src: Overview para 2`
- [ ] `C-OV-03` `constraint` The product carries no comments, likes, public review form, testimonial carousel, newsletter or visitor analytics. `src: Overview para 4`
- [ ] `C-OV-04` `constraint` The product sends no outbound email. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads every published route without an account. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor cannot read a draft project record, preview, media file or search entry. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A signed-out visitor cannot read an unpublished review or any reviewer email. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A reviewer reads the reviewer's own reviews with their revision notes. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A reviewer is denied every `/api/admin/` endpoint. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A reviewer is denied every composer endpoint. `src: User roles table row 2`
- [ ] `C-RL-07` `role` A reviewer cannot act on another reviewer's review. `src: User roles table row 2`
- [ ] `C-RL-08` `role` The owner reaches every console endpoint. `src: User roles table row 3`
- [ ] `C-RL-09` `role` The owner cannot confirm a review on a reviewer's behalf. `src: User roles table row 3`
- [ ] `C-RL-10` `role` The owner cannot publish a review whose writer has not confirmed the text. `src: User roles table row 3`
- [ ] `C-RL-11` `role` A denied mutating request leaves the protected state unchanged. `src: User roles para 1`
- [ ] `C-RL-12` `role` A signed-out caller is denied every reviewer endpoint. `src: User roles para 1`
- [ ] `C-RL-13` `role` Signup at `/signup` is open to anyone. `src: User roles para 2`
- [ ] `C-RL-14` `role` Every account created through signup gets the role `reviewer`. `src: User roles para 2`
- [ ] `C-RL-15` `role` A `role` value sent in the signup body is ignored. `src: User roles para 2`
- [ ] `C-RL-16` `literal` The seeded owner account `owner@example.com` signs in with `deku-demo-pw-2026`. `src: User roles seeded accounts table row 1`
- [ ] `C-RL-17` `literal` The seeded reviewer account `reviewer@example.com` signs in with `deku-demo-pw-2026`. `src: User roles seeded accounts table row 2`
- [ ] `C-RL-18` `literal` The seeded reviewer account `reviewer2@example.com` signs in with `deku-demo-pw-2026`. `src: User roles seeded accounts table row 3`

## C-CF Core features

- [ ] `C-CF-01` `literal` An uploaded project image is stored in MinIO at `projects/{project_key}/{sha256_of_bytes}.{ext}`. `src: Core features 1.1`
- [ ] `C-CF-02` `constraint` Uploaded image bytes are stored nowhere except the MinIO bucket. `src: Core features 1.1`
- [ ] `C-CF-03` `literal` An upload that is not PNG, JPEG or WebP is rejected with `unsupported_media`. `src: Core features 1.1`
- [ ] `C-CF-04` `literal` An upload over 5242880 bytes is rejected with `media_too_large`. `src: Core features 1.1`
- [ ] `C-CF-05` `constraint` A rejected upload writes no object to the bucket. `src: Core features 1.1`
- [ ] `C-CF-06` `constraint` Two identical uploads to one project leave exactly one object with one `project_media` row. `src: Core features 1.2`
- [ ] `C-CF-07` `constraint` Two identical uploads sent at the same instant still leave exactly one object. `src: Core features 1.2`
- [ ] `C-CF-08` `constraint` A draft project record is answered as not found for a signed-out caller. `src: Core features 1.3`
- [ ] `C-CF-09` `constraint` A draft project's media is answered as not found for a signed-out caller. `src: Core features 1.3`
- [ ] `C-CF-10` `capability` A live preview token opens a draft case study route. `src: Core features 1.3`
- [ ] `C-CF-11` `constraint` The seeded draft `vela` stays unreadable to the public. `src: Core features 1.3`
- [ ] `C-CF-12` `capability` A published project's media is served to anyone byte for byte from MinIO. `src: Core features 1.4`
- [ ] `C-CF-13` `capability` A valid contact submission is stored in PostgreSQL. `src: Core features 2.1`
- [ ] `C-CF-14` `capability` A valid contact submission is answered with `ok` true. `src: Core features 2.1`
- [ ] `C-CF-15` `capability` The owner reads contact messages newest first. `src: Core features 2.1`
- [ ] `C-CF-16` `literal` A contact submission missing a name, email or message is rejected with `missing_field`. `src: Core features 2.2`
- [ ] `C-CF-17` `literal` A contact submission with a malformed email is rejected with `invalid_email`. `src: Core features 2.2`
- [ ] `C-CF-18` `literal` A contact message over 4000 characters is rejected with `too_long`. `src: Core features 2.2`
- [ ] `C-CF-19` `constraint` A rejected contact submission stores nothing. `src: Core features 2.2`
- [ ] `C-CF-20` `constraint` A contact submission with a filled `website` field is answered with `ok` true but not stored. `src: Core features 2.3`
- [ ] `C-CF-21` `constraint` A contact submission with `elapsedMs` below 2000 is answered with `ok` true but not stored. `src: Core features 2.3`
- [ ] `C-CF-22` `literal` A sixth contact message from one sender email within an hour is rejected with `rate_limited`. `src: Core features 2.4`
- [ ] `C-CF-23` `constraint` A client address sends at most 20 accepted contact messages per rolling hour. `src: Core features 2.4`
- [ ] `C-CF-24` `ui` The contact form shows the pinned copy for a missing email. `src: Core features 2.5`
- [ ] `C-CF-25` `ui` The contact form shows the pinned copy for a malformed email. `src: Core features 2.5`
- [ ] `C-CF-26` `ui` The contact form shows the pinned send failure copy. `src: Core features 2.5`
- [ ] `C-CF-27` `ui` The contact form shows the pinned timeout copy after 10 seconds without an answer. `src: Core features 2.5`
- [ ] `C-CF-28` `ui` A sent contact message shows the pinned thanks status line. `src: Core features 2.5`
- [ ] `C-CF-29` `ui` A sent contact message turns the headline into the pinned success headline. `src: Core features 2.5`
- [ ] `C-CF-30` `ui` The contact send control label moves from Say hi to Send to Message sent. `src: Core features 2.5`
- [ ] `C-CF-31` `ui` The contact send control stays unavailable until a name with a message are written. `src: Core features 2.5`
- [ ] `C-CF-32` `capability` Wheel, touch, arrow, Page Up, Page Down, Home or End input moves one journey position from 0 to 1. `src: Core features 3.1`
- [ ] `C-CF-33` `capability` The End key takes the journey to the summit. `src: Core features 3.1`
- [ ] `C-CF-34` `ui` Scrolling backwards runs the journey backwards with nothing replayed. `src: Core features 3.1`
- [ ] `C-CF-35` `capability` Tabbing to a tile, summit control or contact field travels the journey to that component. `src: Core features 3.2`
- [ ] `C-CF-36` `capability` `GET /api/journey` returns the timing table with the tile bands. `src: Core features 3.3`
- [ ] `C-CF-37` `capability` The project band is divided equally among the published projects in registry order. `src: Core features 3.3`
- [ ] `C-CF-38` `constraint` A draft project never receives a journey band. `src: Core features 3.3`
- [ ] `C-CF-39` `literal` The five seeded desktop tile bands start at `42.5`, `51.4`, `60.3`, `69.2` with `78.1`. `src: Core features 3.3`
- [ ] `C-CF-40` `literal` The five seeded menu targets are `0.4695`, `0.5585`, `0.6475`, `0.7365` with `0.8255`. `src: Core features 3.3`
- [ ] `C-CF-41` `literal` A 900 tall desktop window runs `4.947` pages over a travel of `3552`. `src: Core features 3.4`
- [ ] `C-CF-42` `literal` A 1110 tall desktop window runs `4.2` pages. `src: Core features 3.4`
- [ ] `C-CF-43` `literal` The mobile branch always runs `5.8` pages. `src: Core features 3.4`
- [ ] `C-CF-44` `ui` Choosing a project from the Work menu travels the journey to the project tile without loading a page. `src: Core features 3.5`
- [ ] `C-CF-45` `ui` The sky turns from near-black to near-white at the summit on a timed flip. `src: Core features 3.6`
- [ ] `C-CF-46` `ui` The navigation ink flips with the sky's eased value. `src: Core features 3.6`
- [ ] `C-CF-47` `ui` Pointing at a project tile reveals the project image through a liquid simulation. `src: Core features 3.7`
- [ ] `C-CF-48` `ui` Scene audio stays silent until the sound control is pressed. `src: Core features 3.8`
- [ ] `C-CF-49` `ui` The sound choice survives a reload. `src: Core features 3.8`
- [ ] `C-CF-50` `capability` The hub at `/case-study` lists one cell per published case study ordered by `hubOrder`. `src: Core features 4.1`
- [ ] `C-CF-51` `literal` The seeded hub cells run `Lumenar`, `Tide`, `Stackr`, `Ascent`. `src: Core features 4.1`
- [ ] `C-CF-52` `ui` Each hub cell shows the eyebrow with the two headline lines of the project. `src: Core features 4.1`
- [ ] `C-CF-53` `capability` A case study route renders the project headline, metadata rail with body blocks in stored order. `src: Core features 4.2`
- [ ] `C-CF-54` `constraint` An unknown case study key renders the not-found page. `src: Core features 4.2`
- [ ] `C-CF-55` `ui` Each case study foot carries a next-project card eyebrowed `VIEW NEXT PROJECT`. `src: Core features 4.3`
- [ ] `C-CF-56` `ui` The last case study card leads to the playground eyebrowed `VIEW PLAYGROUND`. `src: Core features 4.3`
- [ ] `C-CF-57` `ui` A case study shows at most two scoped published reviews under `What people who were there said`. `src: Core features 4.4`
- [ ] `C-CF-58` `ui` Every case study video carries a play control with a range scrubber beneath the picture. `src: Core features 4.5`
- [ ] `C-CF-59` `capability` `/lab` closes back to the journey position the overlay opened from. `src: Core features 5.1`
- [ ] `C-CF-60` `ui` The `/lab` masthead reads `OFF THE MAIN ROUTE`. `src: Core features 5.1`
- [ ] `C-CF-61` `ui` The `/highlights` masthead reads `PROJECT HIGHLIGHTS`. `src: Core features 5.1`
- [ ] `C-CF-62` `ui` `/lab` carries the three pinned groups with their entries. `src: Core features 5.2`
- [ ] `C-CF-63` `ui` The one outbound playground link carries `rel="noopener"` with an accessible name saying the link opens elsewhere. `src: Core features 5.2`
- [ ] `C-CF-64` `ui` `/highlights` carries one entry per published case study in registry order. `src: Core features 5.3`
- [ ] `C-CF-65` `ui` Each highlights entry links to the full case study. `src: Core features 5.3`
- [ ] `C-CF-66` `capability` `/cv` is the only route that scrolls natively. `src: Core features 6.1`
- [ ] `C-CF-67` `ui` `/cv` shows the name, role line, contact details with the four pinned facts. `src: Core features 6.1`
- [ ] `C-CF-68` `capability` `GET /api/cv` returns Selected Work generated from the published case study records in registry order. `src: Core features 6.2`
- [ ] `C-CF-69` `constraint` Every Selected Work bullet contains a numeral. `src: Core features 6.2`
- [ ] `C-CF-70` `ui` Printing `/cv` hides the fixed bar with the sheet shadow. `src: Core features 6.3`
- [ ] `C-CF-71` `capability` The owner issues an invitation returning a 22 character token with the link `/review/{token}`. `src: Core features 7.1`
- [ ] `C-CF-72` `literal` An invitation expires 30 days after issue. `src: Core features 7.1`
- [ ] `C-CF-73` `capability` A signed-in reviewer whose email matches the invitation reads the invitation. `src: Core features 7.2`
- [ ] `C-CF-74` `constraint` An unknown invitation token gets the same not-found answer as an expired token. `src: Core features 7.2`
- [ ] `C-CF-75` `constraint` An invitation issued to another email answers the same as an unknown token. `src: Core features 7.2`
- [ ] `C-CF-76` `constraint` A signed-out caller is denied an invitation whatever the token. `src: Core features 7.2`
- [ ] `C-CF-77` `literal` A review submission without a name is rejected with `missing_name`. `src: Core features 7.3`
- [ ] `C-CF-78` `literal` A review submission without a role is rejected with `missing_role`. `src: Core features 7.3`
- [ ] `C-CF-79` `literal` A review submission with an unknown relationship is rejected with `invalid_relationship`. `src: Core features 7.3`
- [ ] `C-CF-80` `literal` A review submission without a scope is rejected with `missing_scope`. `src: Core features 7.3`
- [ ] `C-CF-81` `literal` A review body under 40 words is rejected with `body_too_short`. `src: Core features 7.3`
- [ ] `C-CF-82` `literal` A review body over 220 words is rejected with `body_too_long`. `src: Core features 7.3`
- [ ] `C-CF-83` `literal` A new review submission enters `awaiting_confirmation`. `src: Core features 7.4`
- [ ] `C-CF-84` `capability` A resubmission on an unconfirmed review replaces the review text. `src: Core features 7.4`
- [ ] `C-CF-85` `literal` A resubmission on a confirmed review is rejected with `already_submitted`. `src: Core features 7.4`
- [ ] `C-CF-86` `constraint` Simultaneous submissions on one invitation leave at most one review that is not withdrawn. `src: Core features 7.4`
- [ ] `C-CF-87` `literal` Only the writer confirms a review, moving the review to `confirmed`. `src: Core features 7.5`
- [ ] `C-CF-88` `constraint` No endpoint in any role edits a review body. `src: Core features 7.5`
- [ ] `C-CF-89` `constraint` The owner publishing a review that is not confirmed is rejected with the review unchanged. `src: Core features 7.6`
- [ ] `C-CF-90` `literal` The owner declines a confirmed review, moving the review to `declined`. `src: Core features 7.6`
- [ ] `C-CF-91` `literal` The owner asks for a revision, moving the review to `submitted` with a note shown only to the writer. `src: Core features 7.6`
- [ ] `C-CF-92` `literal` The writer withdraws a published review, moving the review to `withdrawn`. `src: Core features 7.7`
- [ ] `C-CF-93` `constraint` A withdrawn review leaves every public surface at once. `src: Core features 7.7`
- [ ] `C-CF-94` `constraint` Failed invitation lookups are limited to 10 per client address per hour. `src: Core features 7.8`
- [ ] `C-CF-95` `constraint` `GET /api/reviews` returns only published reviews. `src: Core features 7.9`
- [ ] `C-CF-96` `constraint` Public review output never carries an email, token, decline reason or revision note. `src: Core features 7.9`
- [ ] `C-CF-97` `ui` `/peer-reviews` groups published reviews by project in registry order. `src: Core features 7.9`
- [ ] `C-CF-98` `ui` The summit feedback control shows the published review count only when above zero. `src: Core features 7.9`
- [ ] `C-CF-99` `capability` Publishing a project updates the tile, hub cell, detail route, highlights entry, curriculum vitae entry with search. `src: Core features 8.1`
- [ ] `C-CF-100` `capability` `PUT /api/projects/{key}` returns `valid` with `findings`. `src: Core features 8.2`
- [ ] `C-CF-101` `constraint` A project record with an error finding is rejected with nothing stored. `src: Core features 8.2`
- [ ] `C-CF-102` `literal` A new project key is stored as a `draft`. `src: Core features 8.2`
- [ ] `C-CF-103` `constraint` A case study without a failure statement is refused. `src: Core features 8.3`
- [ ] `C-CF-104` `constraint` A case study without a forward statement is refused. `src: Core features 8.3`
- [ ] `C-CF-105` `capability` `POST /api/projects/{key}/publish` makes a draft public. `src: Core features 8.4`
- [ ] `C-CF-106` `capability` `POST /api/projects/{key}/preview` returns a preview link valid for 30 minutes. `src: Core features 8.4`
- [ ] `C-CF-107` `ui` The preview link renders the draft through the real case study template. `src: Core features 8.4`
- [ ] `C-CF-108` `capability` The owner provisions a device receiving a device key once. `src: Core features 9.1`
- [ ] `C-CF-109` `constraint` A rotated device key stops the old key from writing events. `src: Core features 9.1`
- [ ] `C-CF-110` `constraint` A device key writes only the events of the device the key belongs to. `src: Core features 9.1`
- [ ] `C-CF-111` `constraint` A replayed ingest batch stores each event exactly once. `src: Core features 9.2`
- [ ] `C-CF-112` `constraint` The same ingest batch sent twice at one instant stores each event exactly once. `src: Core features 9.2`
- [ ] `C-CF-113` `literal` An ingest batch over 256 events is rejected with `batch_too_large`. `src: Core features 9.2`
- [ ] `C-CF-114` `literal` An ingest call with a missing key is denied with `device_unauthorized`. `src: Core features 9.2`
- [ ] `C-CF-115` `constraint` Untrusted time is excluded from every telemetry figure. `src: Core features 9.3`
- [ ] `C-CF-116` `literal` Publishing a run with a trusted proportion below 0.9 is refused with `untrusted_run`. `src: Core features 9.4`
- [ ] `C-CF-117` `constraint` A published run keeps frozen figures after later events. `src: Core features 9.4`
- [ ] `C-CF-118` `constraint` An unpublished run is answered as not found publicly. `src: Core features 9.4`
- [ ] `C-CF-119` `literal` The seeded run `lumenar-crosswire-2026` publishes 372 visits, 221 stays, 67 complete viewings with a 20 second median. `src: Core features 9.5`
- [ ] `C-CF-120` `ui` The Lumenar highlights entry shows the four stat row values with the dwell histogram. `src: Core features 9.5`
- [ ] `C-CF-121` `capability` Search covers published projects, case study sections, playground entries, captions, curriculum vitae entries, skills with published reviews. `src: Core features 10.1`
- [ ] `C-CF-122` `constraint` Search never returns a draft project. `src: Core features 10.1`
- [ ] `C-CF-123` `constraint` Search groups results by type in the pinned order without interleaving. `src: Core features 10.2`
- [ ] `C-CF-124` `capability` A search for TouchDesigner lists the Tide project before any caption. `src: Core features 10.2`
- [ ] `C-CF-125` `capability` A document matching both words of a two word query ranks above a document matching one. `src: Core features 10.3`
- [ ] `C-CF-126` `capability` Search forgives one typing error on words of five or more letters. `src: Core features 10.3`
- [ ] `C-CF-127` `ui` An empty search shows the pinned no-match line above twelve tags. `src: Core features 10.4`
- [ ] `C-CF-128` `ui` The Reach me menu carries a `Motion` control offering `Full`, `Reduced`, `None`. `src: Core features 11.1`
- [ ] `C-CF-129` `ui` Choosing `None` swaps to the plain version without a reload. `src: Core features 11.1`
- [ ] `C-CF-130` `ui` `/flat` shows the five published registry entries with their lines, labels with category. `src: Core features 11.2`
- [ ] `C-CF-131` `ui` `/flat` carries the contact form with every contact outcome. `src: Core features 11.2`
- [ ] `C-CF-132` `ui` The foot of `/flat` carries the plain version notice with the pinned control. `src: Core features 11.2`
- [ ] `C-CF-133` `constraint` A browser without real-time graphics gets the plain version with no apology panel. `src: Core features 11.3`
- [ ] `C-CF-134` `literal` An unknown address answers status `404`. `src: Core features 12.1`
- [ ] `C-CF-135` `ui` The not-found page shows the pinned not-found heading. `src: Core features 12.1`
- [ ] `C-CF-136` `ui` The not-found page links back to `/` labelled `Back to the portfolio`. `src: Core features 12.1`
- [ ] `C-CF-137` `constraint` Every internal link on every public route resolves. `src: Core features 12.2`
- [ ] `C-CF-138` `capability` Each public page view is recorded with the route. `src: Core features 12.3`
- [ ] `C-CF-139` `constraint` A page view record keeps only the route with the time. `src: Core features 12.3`
- [ ] `C-CF-140` `capability` The owner reads the page view log newest first. `src: Core features 12.3`
- [ ] `C-CF-141` `constraint` Console, sign-in or reviewer pages are not recorded as page views. `src: Core features 12.3`
- [ ] `C-CF-142` `capability` `POST /api/auth/login` returns `access_token` for a valid email with password. `src: Core features Auth`
- [ ] `C-CF-143` `constraint` A bearer token stops working 12 hours after issue. `src: Core features Auth`
- [ ] `C-CF-144` `constraint` Passwords are stored hashed, never as plaintext. `src: Core features Auth`
- [ ] `C-CF-145` `literal` A signup with an already registered email in any letter case is rejected with `email_taken`. `src: Core features Auth`
- [ ] `C-CF-146` `constraint` A signup password under 10 characters is rejected. `src: Core features Auth`

## C-UF User flow

- [ ] `C-UF-01` `capability` Every public route in the route table answers without sign-in. `src: User flow route table`
- [ ] `C-UF-02` `capability` Every reviewer route in the route table requires a reviewer session. `src: User flow route table`
- [ ] `C-UF-03` `capability` Every console route in the route table requires the owner session. `src: User flow route table`
- [ ] `C-UF-04` `ui` `/console` goes to `/console/projects`. `src: User flow route table`
- [ ] `C-UF-05` `ui` A signed-out visitor opening a console route lands on `/login`. `src: User flow entry and redirects`
- [ ] `C-UF-06` `ui` After sign-in the owner lands on `/console/projects`. `src: User flow entry and redirects`
- [ ] `C-UF-07` `ui` After sign-in a reviewer lands on `/my-reviews`. `src: User flow entry and redirects`
- [ ] `C-UF-08` `ui` Sign out returns to `/`. `src: User flow entry and redirects`
- [ ] `C-UF-09` `ui` A reviewer opening a console route gets the not-found page. `src: User flow entry and redirects`
- [ ] `C-UF-10` `ui` A signed-out visitor on an invitation route sees the same sign-in prompt for every token. `src: User flow entry and redirects`
- [ ] `C-UF-11` `ui` The contact journey ends with the sent message on top of `/console/messages`. `src: User flow journey 1`
- [ ] `C-UF-12` `ui` The case study journey reaches the Tide rail headings with the next card for Ascent. `src: User flow journey 2`
- [ ] `C-UF-13` `ui` The review journey ends with the published review shown under Stackr on `/peer-reviews`. `src: User flow journey 3`
- [ ] `C-UF-14` `ui` The composer journey shows each finding next to the block the finding belongs to. `src: User flow journey 4`
- [ ] `C-UF-15` `ui` The telemetry journey shows the seeded run's health strip reading `trusted`. `src: User flow journey 5`
- [ ] `C-UF-16` `ui` The search journey shows the Projects group first. `src: User flow journey 6`
- [ ] `C-UF-17` `ui` The plain version journey shows the notice at the foot. `src: User flow journey 7`
- [ ] `C-UF-18` `ui` Every list shows an empty state. `src: User flow states`
- [ ] `C-UF-19` `ui` A failed request never crashes a page. `src: User flow states`
- [ ] `C-UF-20` `ui` A failed console action shows an inline banner above the working area. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The journey, the dark case studies with the light document routes switch registers abruptly. `src: UI/UX notes register`
- [ ] `C-UX-02` `ui` The single accent is a deep vivid blue used only for matched search words with histogram bars. `src: UI/UX notes palette`
- [ ] `C-UX-03` `ui` The only coloured type is the muted teal of the curriculum vitae headings. `src: UI/UX notes palette`
- [ ] `C-UX-04` `ui` No page is tinted, no card carries a hue, no highlight box sits behind text. `src: UI/UX notes palette`
- [ ] `C-UX-05` `ui` Console status colours appear only on the console near-black surface with an icon plus a word. `src: UI/UX notes palette`
- [ ] `C-UX-06` `ui` Headlines are set in a condensed heavy uppercase grotesque. `src: UI/UX notes type`
- [ ] `C-UX-07` `ui` Headline elements declare the display family `Arial Narrow`. `src: UI/UX notes type`
- [ ] `C-UX-08` `ui` Body copy declares the body family `Segoe UI`. `src: UI/UX notes type`
- [ ] `C-UX-09` `ui` The build carries exactly four soft shadows. `src: UI/UX notes shape`
- [ ] `C-UX-10` `ui` Hover changes faintness only. `src: UI/UX notes motion`
- [ ] `C-UX-11` `ui` Every hover state is also a focus state. `src: UI/UX notes motion`
- [ ] `C-UX-12` `ui` Document routes show no bounce, overshoot, staggered reveal or page transition. `src: UI/UX notes motion`
- [ ] `C-UX-13` `ui` A reduced motion preference removes birds, rain, glow, pointer tipping with self-playing video. `src: UI/UX notes motion`
- [ ] `C-UX-14` `ui` Escape closes an overlay before a dropdown. `src: UI/UX notes components`
- [ ] `C-UX-15` `ui` Menu items drop into view from behind a clipping edge. `src: UI/UX notes components`
- [ ] `C-UX-16` `ui` The console confirms before any irreversible action. `src: UI/UX notes components`
- [ ] `C-UX-17` `ui` Text contrast meets WCAG AA. `src: UI/UX notes accessibility`
- [ ] `C-UX-18` `ui` A two-tone focus ring stays visible over light or dark media. `src: UI/UX notes accessibility`
- [ ] `C-UX-19` `ui` Every icon-only control carries a label. `src: UI/UX notes accessibility`
- [ ] `C-UX-20` `ui` Each public route carries exactly one level-one heading. `src: UI/UX notes accessibility`
- [ ] `C-UX-21` `ui` At a narrow viewport no public route overflows sideways. `src: UI/UX notes accessibility`
- [ ] `C-UX-22` `ui` The system dark-scheme preference changes nothing. `src: UI/UX notes mode`
- [ ] `C-UX-23` `ui` The home route shows no thumbnail grid, header bar or footer bar. `src: UI/UX notes what it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `capability` Every public route's HTML reaches the browser with the headings, copy with links already rendered by the server. `src: Technical requirements stack`
- [ ] `C-TR-02` `capability` The JSON API is served under `/api` on the same origin as the pages. `src: Technical requirements stack`
- [ ] `C-TR-03` `literal` `GET /api/health` returns `200` once PostgreSQL with the bucket are reachable. `src: Technical requirements stack`
- [ ] `C-TR-04` `constraint` The only backing services used are `postgres` with `minio`. `src: Technical requirements stack`
- [ ] `C-TR-05` `contract` The app reads `DATABASE_URL`. `src: Technical requirements environment`
- [ ] `C-TR-06` `contract` The app reads `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` with `STORAGE_SECRET_KEY`. `src: Technical requirements environment`
- [ ] `C-TR-07` `constraint` No credential, storage key or database URL appears in anything the browser downloads. `src: Technical requirements nothing secret`
- [ ] `C-TR-08` `constraint` The app serves no image, video, audio, model or font file of the build. `src: Technical requirements no shipped binary asset`
- [ ] `C-TR-09` `constraint` The only binary responses are owner uploads from `GET /api/media/{object_key}`. `src: Technical requirements no shipped binary asset`
- [ ] `C-TR-10` `capability` `/sitemap.xml` lists the absolute URL of every public route. `src: Technical requirements sitemap`
- [ ] `C-TR-11` `constraint` `/sitemap.xml` never lists a draft, console, sign-in, review or preview route. `src: Technical requirements sitemap`
- [ ] `C-TR-12` `capability` `/robots.txt` names the sitemap on a `Sitemap:` line. `src: Technical requirements sitemap`
- [ ] `C-TR-13` `literal` The journey components carry the pinned desktop bands. `src: Technical requirements journey contract`
- [ ] `C-TR-14` `literal` The journey components carry the pinned mobile bands. `src: Technical requirements journey contract`
- [ ] `C-TR-15` `literal` The desktop fade values are `0.7` with `0.2`, the mobile values `0.86` with `0.1`. `src: Technical requirements journey contract`
- [ ] `C-TR-16` `literal` Band edges round to four decimals, pages to three, `travelPx` to a whole number. `src: Technical requirements journey contract`
- [ ] `C-TR-17` `data` A composer finding carries `rule`, `blockIndex`, `message` with an error or warning level. `src: Technical requirements composer validation`
- [ ] `C-TR-18` `literal` A block of an unknown type yields the error rule `block_type`. `src: Technical requirements composer validation`
- [ ] `C-TR-19` `literal` A case study not opening with exactly one standfirst yields `standfirst_first`. `src: Technical requirements composer validation`
- [ ] `C-TR-20` `literal` A case study with no failure statement yields `failure_required`. `src: Technical requirements composer validation`
- [ ] `C-TR-21` `literal` A case study with no forward statement yields `forward_required`. `src: Technical requirements composer validation`
- [ ] `C-TR-22` `literal` A case study not closing with exactly one close statement yields `close_last`. `src: Technical requirements composer validation`
- [ ] `C-TR-23` `literal` A failure statement with no later change statement yields `failure_resolved`. `src: Technical requirements composer validation`
- [ ] `C-TR-24` `literal` A statement heading over 64 characters yields `heading_length`. `src: Technical requirements composer validation`
- [ ] `C-TR-25` `literal` A body paragraph under 20 words yields `paragraph_length`. `src: Technical requirements composer validation`
- [ ] `C-TR-26` `literal` A media block with no caption or caption reason yields `media_caption`. `src: Technical requirements composer validation`
- [ ] `C-TR-27` `literal` A media reference to an object not uploaded for the project yields `media_ref`. `src: Technical requirements composer validation`
- [ ] `C-TR-28` `literal` A record whose `meta` is not three columns yields `meta_shape`. `src: Technical requirements composer validation`
- [ ] `C-TR-29` `literal` A record whose `lines` is not two strings yields `lines_shape`. `src: Technical requirements composer validation`
- [ ] `C-TR-30` `literal` A `menuLabel` over 12 characters yields `menu_label_length`. `src: Technical requirements composer validation`
- [ ] `C-TR-31` `literal` A `note` outside three to five words yields `note_length`. `src: Technical requirements composer validation`
- [ ] `C-TR-32` `literal` A category outside the five pinned values yields `category`. `src: Technical requirements composer validation`
- [ ] `C-TR-33` `literal` A curriculum vitae bullet without a numeral yields `cv_bullet_numeral`. `src: Technical requirements composer validation`
- [ ] `C-TR-34` `literal` A heading reading as a label yields the warning `heading_verb` without blocking the save. `src: Technical requirements composer validation`
- [ ] `C-TR-35` `literal` A presence session lasting at least `60` seconds is `completed`. `src: Technical requirements telemetry rules`
- [ ] `C-TR-36` `literal` A presence session lasting 3 to 60 seconds is `partial`. `src: Technical requirements telemetry rules`
- [ ] `C-TR-37` `literal` A presence session shorter than 3 seconds is `discarded`. `src: Technical requirements telemetry rules`
- [ ] `C-TR-38` `literal` A session still open when a newer boot reports ends as `truncated`. `src: Technical requirements telemetry rules`
- [ ] `C-TR-39` `literal` A health window with `longestHighMs` above `600000` is untrusted. `src: Technical requirements telemetry rules`
- [ ] `C-TR-40` `literal` A health window with `triggersInWindow` above `120` is untrusted. `src: Technical requirements telemetry rules`
- [ ] `C-TR-41` `constraint` Eight consecutive health windows with zero triggers inside opening hours are untrusted. `src: Technical requirements telemetry rules`
- [ ] `C-TR-42` `constraint` A health window whose ambient reference drifts over 25 percent from the boot's first window is untrusted. `src: Technical requirements telemetry rules`
- [ ] `C-TR-43` `constraint` A session overlapping an untrusted window is discarded. `src: Technical requirements telemetry rules`
- [ ] `C-TR-44` `constraint` The trusted proportion is trusted windows over all windows of the run. `src: Technical requirements telemetry rules`
- [ ] `C-TR-45` `literal` Every ingest answer carries `nextIntervalMs` of at least `30000`. `src: Technical requirements telemetry rules`
- [ ] `C-TR-46` `literal` Published `visits` counts trusted completed or partial sessions. `src: Technical requirements telemetry rules`
- [ ] `C-TR-47` `literal` Published `medianDwellSeconds` is the median visit duration rounded half up. `src: Technical requirements telemetry rules`
- [ ] `C-TR-48` `literal` Published `dwellHistogram` counts visits into the eight pinned bins. `src: Technical requirements telemetry rules`
- [ ] `C-TR-49` `literal` A run's health reads `trusted` at 0.9, `degraded` from 0.5, `untrusted` below. `src: Technical requirements telemetry rules`
- [ ] `C-TR-50` `capability` `GET /api/search` gives the same ranking as the page. `src: Technical requirements search rules`
- [ ] `C-TR-51` `literal` Search type weights run `project` 1.0 down to `labCaption` 0.25. `src: Technical requirements search rules`
- [ ] `C-TR-52` `capability` A project search document carries tags from the project labels with the `Built with` rows. `src: Technical requirements search rules`
- [ ] `C-TR-53` `constraint` Typo tolerance never applies to tags. `src: Technical requirements search rules`
- [ ] `C-TR-54` `capability` The rung is chosen by measurement, never by a browser identification string. `src: Technical requirements capability ladder`
- [ ] `C-TR-55` `capability` Every rung carries every route with every word. `src: Technical requirements capability ladder`
- [ ] `C-TR-56` `capability` The saved Motion choice wins over the measured rung. `src: Technical requirements capability ladder`
- [ ] `C-TR-57` `constraint` The flat rung loads its largest content within one second. `src: Technical requirements performance`

## C-DM Data model

- [ ] `C-DM-01` `data` The `users` table stores `email`, `name`, `role` with `password_hash`. `src: Data model users`
- [ ] `C-DM-02` `data` The `projects` table stores `key`, `status`, `display_order` with `hub_order`. `src: Data model projects`
- [ ] `C-DM-03` `data` Two projects never share a key. `src: Data model projects`
- [ ] `C-DM-04` `data` The `project_media` table stores `project_key`, `object_key` with `sha256`. `src: Data model project_media`
- [ ] `C-DM-05` `data` The `invitations` table stores `token`, `email` with `used_at`. `src: Data model invitations`
- [ ] `C-DM-06` `data` The `reviews` table stores `state`, `body` with `confirmed_at`. `src: Data model reviews`
- [ ] `C-DM-07` `data` A review body never changes once `confirmed_at` is set. `src: Data model reviews`
- [ ] `C-DM-08` `data` The `contact_messages` table stores `name`, `email` with `message`. `src: Data model contact_messages`
- [ ] `C-DM-09` `data` The `page_views` table stores `route` with `viewed_at` only. `src: Data model page_views`
- [ ] `C-DM-10` `data` The `devices` table stores `device_id` with `key_hash`, never the plain key. `src: Data model devices`
- [ ] `C-DM-11` `data` The `runs` table stores `run_id`, `state` with frozen `figures`. `src: Data model runs`
- [ ] `C-DM-12` `data` The `telemetry_events` table holds one row per `device_id`, `boot_id`, `seq` triple. `src: Data model telemetry_events`
- [ ] `C-DM-13` `data` Seeding on restart adds no duplicate rows. `src: Data model seed data`
- [ ] `C-DM-14` `data` The six seeded projects carry the pinned keys, ids, orders, statuses with menu labels. `src: Data model seed data projects table`
- [ ] `C-DM-15` `data` The seeded project lines, categories with notes match the seed table. `src: Data model seed data projects table`
- [ ] `C-DM-16` `data` The seeded project labels match the pinned label triples. `src: Data model seed data labels`
- [ ] `C-DM-17` `data` The seeded headlines with metadata rails match the pinned table. `src: Data model seed data headlines`
- [ ] `C-DM-18` `data` The seeded Tide body carries the pinned blocks in the pinned order with the pinned kinds. `src: Data model seed data tide body`
- [ ] `C-DM-19` `data` The seeded Lumenar body carries the thirteen pinned headings in order. `src: Data model seed data lumenar body`
- [ ] `C-DM-20` `data` Every seeded project record passes validation. `src: Data model seed data lumenar body`
- [ ] `C-DM-21` `data` The seeded Lumenar record carries telemetry of `60` with `3` seconds. `src: Data model seed data lumenar body`
- [ ] `C-DM-22` `data` The seeded highlights for Lumenar with Tide match the pinned headings. `src: Data model seed data highlights`
- [ ] `C-DM-23` `data` The seeded curriculum vitae entries match the pinned titles, bullets with tools. `src: Data model seed data curriculum vitae entries`
- [ ] `C-DM-24` `data` The five seeded invitations carry the pinned tokens, emails, scopes with states. `src: Data model seed data invitations`
- [ ] `C-DM-25` `data` The seeded published review by Riya Anand carries the pinned attribution line. `src: Data model seed data reviews`
- [ ] `C-DM-26` `data` The seeded confirmed review by Kit Fenwick stays unpublished. `src: Data model seed data reviews`
- [ ] `C-DM-27` `data` The seeded review awaiting confirmation stays unpublished. `src: Data model seed data reviews`
- [ ] `C-DM-28` `data` The seeded run carries the pinned frozen figures with histogram counts. `src: Data model seed data run`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Headline sizes grow with the smaller window side. `src: Front-end specification sizing`
- [ ] `C-FE-02` `ui` The root font size is 16px. `src: Front-end specification sizing`
- [ ] `C-FE-03` `ui` The display family stack starts with `Arial Narrow` on headlines. `src: Front-end specification sizing`
- [ ] `C-FE-04` `ui` The body family stack starts with `-apple-system` ahead of `Segoe UI`. `src: Front-end specification sizing`
- [ ] `C-FE-05` `constraint` No font file is downloaded. `src: Front-end specification sizing`
- [ ] `C-FE-06` `ui` Every tile headline sets on exactly two lines. `src: Front-end specification sizing`
- [ ] `C-FE-07` `ui` Case study captions keep the 14px size at every breakpoint. `src: Front-end specification sizing`
- [ ] `C-FE-08` `ui` White type over media carries a faint dark halo. `src: Front-end specification colour`
- [ ] `C-FE-09` `ui` The figure surface draws in front of the interface without catching the pointer. `src: Front-end specification stacking`
- [ ] `C-FE-10` `ui` Arrows are typed characters in the display family. `src: Front-end specification iconography`
- [ ] `C-FE-11` `ui` The spiral diagram appears once, on the Lumenar case study. `src: Front-end specification iconography`
- [ ] `C-FE-12` `ui` The muted sound mark removes both waves without adding a slash. `src: Front-end specification iconography`
- [ ] `C-FE-13` `ui` A fixed navigation cluster at the top right holds Work, Reach me with About. `src: Front-end specification global chrome`
- [ ] `C-FE-14` `ui` The Work menu lists the five published registry entries. `src: Front-end specification global chrome`
- [ ] `C-FE-15` `ui` The Reach me menu holds the email reveal, three profiles with the Motion control. `src: Front-end specification global chrome`
- [ ] `C-FE-16` `ui` About folds open the biography column instead of a dropdown. `src: Front-end specification global chrome`
- [ ] `C-FE-17` `ui` The sound control carries `aria-pressed` with distinct mute labels. `src: Front-end specification global chrome`
- [ ] `C-FE-18` `ui` A skip link labelled `Skip to main content` is the first focusable element of every route. `src: Front-end specification global chrome`
- [ ] `C-FE-19` `ui` Every route carries the copyright line `© 2026 Elian Kais Brandtsteiner`. `src: Front-end specification global chrome`
- [ ] `C-FE-20` `ui` The navigation fades up only after the loader hands over. `src: Front-end specification global chrome`
- [ ] `C-FE-21` `ui` The loader counts up with three separate digits reporting the pinned status milestones. `src: Front-end specification journey arrival`
- [ ] `C-FE-22` `ui` A visitor returning from a case study skips the loader. `src: Front-end specification journey arrival`
- [ ] `C-FE-23` `ui` The opening headline shows the four pinned lines with the separate final word. `src: Front-end specification journey opening headline`
- [ ] `C-FE-24` `ui` Each tile shows three scattered labels with the pinned eyebrow. `src: Front-end specification journey tiles`
- [ ] `C-FE-25` `ui` Screen readers hear the pinned journey announcements after scrolling rests. `src: Front-end specification journey tiles`
- [ ] `C-FE-26` `ui` Only the world is on screen between the last tile with the summit. `src: Front-end specification journey gaps`
- [ ] `C-FE-27` `ui` The biography panel shows the pinned copy in a narrow column. `src: Front-end specification journey biography`
- [ ] `C-FE-28` `ui` The summit shows the pinned idle headline above View CV, View feedback with Say hi. `src: Front-end specification journey summit`
- [ ] `C-FE-29` `ui` The summit headline lines become the name field with the email field at headline size. `src: Front-end specification contact form morph`
- [ ] `C-FE-30` `ui` The contact form shows the platform send hint, absent on phones. `src: Front-end specification contact form morph`
- [ ] `C-FE-31` `ui` Ctrl or Cmd with Enter sends the contact form. `src: Front-end specification contact form morph`
- [ ] `C-FE-32` `ui` The world stops answering the pointer once the contact form opens. `src: Front-end specification contact form morph`
- [ ] `C-FE-33` `ui` A project headline passes in front of the landscape behind the figure. `src: Front-end specification three-dimensional layer`
- [ ] `C-FE-34` `ui` The water is gone by the time the first project arrives. `src: Front-end specification three-dimensional layer`
- [ ] `C-FE-35` `ui` The figure stops climbing, stands then turns to face the visitor in the last four percent. `src: Front-end specification three-dimensional layer`
- [ ] `C-FE-36` `ui` The figure shadow is gone once the sky turns pale. `src: Front-end specification three-dimensional layer`
- [ ] `C-FE-37` `ui` The carried object is put down at the summit to open the playground. `src: Front-end specification three-dimensional layer`
- [ ] `C-FE-38` `ui` Hub titles swell into each other under the pointer, then peel apart. `src: Front-end specification liquid type engine`
- [ ] `C-FE-39` `constraint` The liquid type effect never runs on the home route. `src: Front-end specification liquid type engine`
- [ ] `C-FE-40` `ui` A bird flock flies toward the camera only outside the project sequence. `src: Front-end specification atmosphere`
- [ ] `C-FE-41` `ui` The cursor glow follows a mouse pointer a beat late. `src: Front-end specification atmosphere`
- [ ] `C-FE-42` `constraint` The cursor glow never runs on a case study or an open overlay. `src: Front-end specification atmosphere`
- [ ] `C-FE-43` `constraint` No film grain appears anywhere. `src: Front-end specification atmosphere`
- [ ] `C-FE-44` `ui` The liquid reveal paint holds about a second after the pointer leaves before draining. `src: Front-end specification liquid reveal`
- [ ] `C-FE-45` `ui` The birdsong fades in slowly, the climbing sound almost at once. `src: Front-end specification scene audio`
- [ ] `C-FE-46` `ui` Turning sound off with on again keeps the birdsong position. `src: Front-end specification scene audio`
- [ ] `C-FE-47` `ui` The hub is a full-window two by two grid with a hairline black cross. `src: Front-end specification case study hub`
- [ ] `C-FE-48` `ui` Hub cell hover or focus only makes the cell fainter. `src: Front-end specification case study hub`
- [ ] `C-FE-49` `ui` The hub carries the pinned hidden heading with the pinned summary. `src: Front-end specification case study hub`
- [ ] `C-FE-50` `ui` The case study hero leaves the left third empty with the headline on the right. `src: Front-end specification case study detail`
- [ ] `C-FE-51` `ui` The case study eyebrow reads the project name followed by case study. `src: Front-end specification case study detail`
- [ ] `C-FE-52` `ui` The metadata rail stays three columns at every width. `src: Front-end specification case study detail`
- [ ] `C-FE-53` `ui` Media stays visible with every motion feature off. `src: Front-end specification case study detail`
- [ ] `C-FE-54` `ui` Lumenar media carries the pinned flashing lights warning. `src: Front-end specification case study detail`
- [ ] `C-FE-55` `ui` The overlays show a black band over pure white paper with no transition between. `src: Front-end specification playground`
- [ ] `C-FE-56` `ui` `/lab` carries the four making entries with the pinned headings. `src: Front-end specification playground`
- [ ] `C-FE-57` `ui` `/lab` carries the twenty-eight pinned grid labels. `src: Front-end specification playground`
- [ ] `C-FE-58` `ui` Highlights titles use the home tile component in near-black on white. `src: Front-end specification project highlights`
- [ ] `C-FE-59` `ui` The stat row shows four numbers with no tiles, cards, icons or arrows. `src: Front-end specification project highlights`
- [ ] `C-FE-60` `ui` The dwell histogram is one accent series labelled on the tallest bin with the `60+` bin. `src: Front-end specification project highlights`
- [ ] `C-FE-61` `ui` The dwell histogram offers a table view of the same numbers. `src: Front-end specification project highlights`
- [ ] `C-FE-62` `ui` `/cv` shows a single sheet on a darker desk with a fixed bar outside the sheet. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-63` `ui` The `/cv` bar carries `Download PDF`. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-64` `ui` The `/cv` header shows the pinned role line with the profile paragraph. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-65` `ui` The `/cv` portrait is a generated abstract shape, never a synthetic face. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-66` `ui` The `/cv` education entries match the pinned titles. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-67` `ui` The `/cv` skills clusters match the four pinned clusters. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-68` `ui` The `/cv` experience entries match the three pinned roles. `src: Front-end specification curriculum vitae`
- [ ] `C-FE-69` `ui` `/peer-reviews` shows the masthead `PEER REVIEWS` with the heading `View feedback`. `src: Front-end specification peer reviews`
- [ ] `C-FE-70` `ui` `/peer-reviews` shows the pinned empty state with no review published. `src: Front-end specification peer reviews`
- [ ] `C-FE-71` `ui` Published reviews show as plain text without quotation marks, photographs, ratings or logos. `src: Front-end specification peer reviews`
- [ ] `C-FE-72` `ui` The review form carries `YOUR NAME`, `YOUR ROLE` with `WHERE` fields. `src: Front-end specification peer reviews`
- [ ] `C-FE-73` `ui` The review form scope group carries the pinned group label. `src: Front-end specification peer reviews`
- [ ] `C-FE-74` `ui` The review word counter appears only after thirty words. `src: Front-end specification peer reviews`
- [ ] `C-FE-75` `ui` The review form shows the pinned validation copy. `src: Front-end specification peer reviews`
- [ ] `C-FE-76` `ui` The confirmation page shows the review as published with the confirm control, the change control with `Withdraw`. `src: Front-end specification peer reviews`
- [ ] `C-FE-77` `ui` The console sidebar lists Projects, Reviews, Invitations, Runs, Messages, Page views with Sign out. `src: Front-end specification owner console`
- [ ] `C-FE-78` `ui` `/console/projects` shows one card per record with a draft or published badge. `src: Front-end specification owner console`
- [ ] `C-FE-79` `ui` `/console/reviews` offers Publish, Decline, Ask for a revision with no edit action. `src: Front-end specification owner console`
- [ ] `C-FE-80` `ui` `/console/runs` shows a health strip with the tick, bar or cross icon plus the word. `src: Front-end specification owner console`
- [ ] `C-FE-81` `ui` `/console/runs` shows a publish refusal with the trusted proportion. `src: Front-end specification owner console`
- [ ] `C-FE-82` `ui` `/flat` shows the masthead name, the project list, the biography, the summit with the route list. `src: Front-end specification plain version`
- [ ] `C-FE-83` `ui` `/flat` shows the five pinned crawlable blurbs. `src: Front-end specification plain version`
- [ ] `C-FE-84` `ui` The Motion control is a radio group reached with one tab stop. `src: Front-end specification plain version`
- [ ] `C-FE-85` `ui` Each route carries the pinned hidden level-one heading. `src: Front-end specification accessibility`
- [ ] `C-FE-86` `ui` Overlays trap focus then restore focus to the opener. `src: Front-end specification accessibility`
- [ ] `C-FE-87` `ui` Every video carries an associated text alternative. `src: Front-end specification accessibility`
- [ ] `C-FE-88` `ui` Forced colours mode drops the scene with every atmosphere layer. `src: Front-end specification accessibility`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product has one owner account, no teams, no tenants. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` Reviews arrive only through owner-issued invitations. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` No network call leaves the container at runtime. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` Placeholders are generated, visibly placeholder. `src: Constraints bullet 4`
- [ ] `C-CN-05` `constraint` The product offers no password reset or social sign-in. `src: Constraints bullet 5`
- [ ] `C-CN-06` `constraint` The product offers no review body editing, review reordering, project unpublishing or media deletion. `src: Constraints bullet 6`
- [ ] `C-CN-07` `constraint` The product serves no duplicate home route or second curriculum vitae path. `src: Constraints bullet 7`
- [ ] `C-CN-08` `constraint` The product shows no showreel link, piano sound, orbit camera control or debug panel. `src: Constraints bullet 8`
- [ ] `C-CN-09` `constraint` The browser is the only client. `src: Constraints bullet 9`
- [ ] `C-CN-10` `constraint` The app stays responsive with 50 projects, 500 reviews, 10,000 messages with a million telemetry events. `src: Constraints bullet 10`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The app maps `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-06` `contract` Seeded credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-07` `contract` The app serves a production build, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-08` `contract` The server keeps running after the build session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-10` `contract` The app uses the already running backing services without starting copies. `src: Deployment contract bullet 10`
- [ ] `C-DC-11` `contract` A list endpoint returns a top-level JSON array. `src: Deployment contract API shapes`
- [ ] `C-DC-12` `contract` An invalid or unauthorized call is rejected as a client error, never a server error. `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` Protected endpoints require `Authorization: Bearer` with the access token. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` Ingest authenticates with the `X-Device-Key` header. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` `GET /api/auth/me` returns the caller's `id`, `email`, `name` with `role`. `src: Deployment contract API shapes`
- [ ] `C-DC-16` `contract` `GET /api/projects` returns published records in `order`. `src: Deployment contract API shapes`
- [ ] `C-DC-17` `contract` `GET /api/admin/projects` returns every record with drafts. `src: Deployment contract API shapes`
- [ ] `C-DC-18` `contract` A media upload returns `objectKey`, `url`, `sha256`, `contentType` with `sizeBytes`. `src: Deployment contract API shapes`
- [ ] `C-DC-19` `contract` `GET /api/journey` defaults to the desktop branch at a height of 900. `src: Deployment contract API shapes`
- [ ] `C-DC-20` `contract` `GET /api/journey` rejects an unknown branch with `invalid_branch`. `src: Deployment contract API shapes`
- [ ] `C-DC-21` `contract` `GET /api/journey` rejects a height that is not positive with `invalid_viewport`. `src: Deployment contract API shapes`
- [ ] `C-DC-22` `contract` `GET /api/cv` returns `name`, `role`, `contact`, `facts`, `profile` with `selectedWork`. `src: Deployment contract API shapes`
- [ ] `C-DC-23` `contract` `POST /api/page-views` rejects a route that is not a public page with `invalid_route`. `src: Deployment contract API shapes`
- [ ] `C-DC-24` `contract` `GET /api/admin/page-views` returns at most 500 rows newest first. `src: Deployment contract API shapes`
- [ ] `C-DC-25` `contract` An invitation response carries `token`, `url`, `email`, `scope`, `issuedAt` with `expiresAt`. `src: Deployment contract API shapes`
- [ ] `C-DC-26` `contract` `GET /api/review/{token}` returns `scope` with `draft`. `src: Deployment contract API shapes`
- [ ] `C-DC-27` `contract` `GET /api/my/reviews` returns only the caller's own reviews. `src: Deployment contract API shapes`
- [ ] `C-DC-28` `contract` A published review carries the pinned public fields with `attribution`. `src: Deployment contract API shapes`
- [ ] `C-DC-29` `contract` `GET /api/admin/reviews` returns reviews in every state with `email`. `src: Deployment contract API shapes`
- [ ] `C-DC-30` `contract` A duplicate device id is rejected with `duplicate_device`. `src: Deployment contract API shapes`
- [ ] `C-DC-31` `contract` An ingest event of unknown kind is rejected with `invalid_event`. `src: Deployment contract API shapes`
- [ ] `C-DC-32` `contract` A run for a project without telemetry is rejected with `no_telemetry`. `src: Deployment contract API shapes`
- [ ] `C-DC-33` `contract` `GET /api/admin/runs/{run_id}` returns `health`, `sessions` with `figures`. `src: Deployment contract API shapes`
- [ ] `C-DC-34` `contract` Publishing a published run again is rejected with `already_published`. `src: Deployment contract API shapes`
- [ ] `C-DC-35` `contract` `GET /api/runs/{run_id}` returns the pinned published figure fields. `src: Deployment contract API shapes`
- [ ] `C-DC-36` `contract` `GET /api/search` returns `query`, `total`, `groups` with `suggestions` when nothing matched. `src: Deployment contract API shapes`
- [ ] `C-DC-37` `contract` `GET /api/search-index` returns `documents` with `tokens`. `src: Deployment contract API shapes`
- [ ] `C-DC-38` `contract` A returned project record carries `eyebrow`, `path`, `status` with the pinned fields. `src: Deployment contract API shapes`
- [ ] `C-DC-39` `contract` A generated placeholder carries the project menu label faintly across the image. `src: Deployment contract API shapes`
- [ ] `C-DC-40` `contract` A contact message exists only as a PostgreSQL row, never in memory or a file. `src: Deployment contract no mocks`
- [ ] `C-DC-41` `contract` A draft hidden by the page is also refused by the API. `src: Deployment contract no mocks`
- [ ] `C-DC-42` `contract` Search runs over the published records, never a hardcoded list. `src: Deployment contract no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `owner@example.com` | seeded owner email | C-RL-16 | User roles, seeded accounts |
| `deku-demo-pw-2026` | password for every seeded account | C-RL-16 | User roles, seeded accounts; Data model |
| `reviewer@example.com` | seeded reviewer email | C-RL-17 | User roles, seeded accounts |
| `reviewer2@example.com` | second seeded reviewer email | C-RL-18 | User roles, seeded accounts |
| `projects/{project_key}/{sha256_of_bytes}.{ext}` | media object key scheme | C-CF-01 | Core features 1.1 |
| `unsupported_media` | rejection code for a non-image upload | C-CF-03 | Core features 1.1 |
| `media_too_large` | rejection code for an oversize upload | C-CF-04 | Core features 1.1 |
| `missing_field` | contact rejection code | C-CF-16 | Core features 2.2 |
| `invalid_email` | contact rejection code | C-CF-17 | Core features 2.2 |
| `too_long` | contact rejection code | C-CF-18 | Core features 2.2 |
| `rate_limited` | contact rejection code | C-CF-22 | Core features 2.4 |
| `42.5` | first desktop tile band start | C-CF-39 | Core features 3.3 |
| `51.4` | second desktop tile band start | C-CF-39 | Core features 3.3 |
| `60.3` | third desktop tile band start | C-CF-39 | Core features 3.3 |
| `69.2` | fourth desktop tile band start | C-CF-39 | Core features 3.3 |
| `78.1` | fifth desktop tile band start | C-CF-39 | Core features 3.3 |
| `0.4695` | first menu target | C-CF-40 | Core features 3.3 |
| `0.5585` | second menu target | C-CF-40 | Core features 3.3 |
| `0.6475` | third menu target | C-CF-40 | Core features 3.3 |
| `0.7365` | fourth menu target | C-CF-40 | Core features 3.3 |
| `0.8255` | fifth menu target | C-CF-40 | Core features 3.3 |
| `4.947` | desktop pages at a 900 tall window | C-CF-41 | Core features 3.4 |
| `3552` | journey travel | C-CF-41 | Core features 3.4 |
| `4.2` | desktop pages at a 1110 tall window | C-CF-42 | Core features 3.4 |
| `5.8` | mobile pages | C-CF-43 | Core features 3.4 |
| `Lumenar` | first hub cell | C-CF-51 | Core features 4.1 |
| `Tide` | second hub cell | C-CF-51 | Core features 4.1 |
| `Stackr` | third hub cell | C-CF-51 | Core features 4.1 |
| `Ascent` | fourth hub cell | C-CF-51 | Core features 4.1 |
| `awaiting_confirmation` | state of a new review | C-CF-83 | Core features 7.4 |
| `already_submitted` | resubmission rejection code | C-CF-85 | Core features 7.4 |
| `confirmed` | state after the writer confirms | C-CF-87 | Core features 7.5 |
| `declined` | state after the owner declines | C-CF-90 | Core features 7.6 |
| `submitted` | state after a revision request | C-CF-91 | Core features 7.6 |
| `withdrawn` | state after the writer withdraws | C-CF-92 | Core features 7.7 |
| `missing_name` | review rejection code | C-CF-77 | Core features 7.3 |
| `missing_role` | review rejection code | C-CF-78 | Core features 7.3 |
| `invalid_relationship` | review rejection code | C-CF-79 | Core features 7.3 |
| `missing_scope` | review rejection code | C-CF-80 | Core features 7.3 |
| `body_too_short` | review rejection code | C-CF-81 | Core features 7.3 |
| `body_too_long` | review rejection code | C-CF-82 | Core features 7.3 |
| `draft` | status of a new project | C-CF-102 | Core features 8.2 |
| `batch_too_large` | ingest rejection code | C-CF-113 | Core features 9.2 |
| `device_unauthorized` | ingest denial code | C-CF-114 | Core features 9.2 |
| `untrusted_run` | publication refusal code | C-CF-116 | Core features 9.4 |
| `lumenar-crosswire-2026` | seeded run id | C-CF-119 | Core features 9.5 |
| `404` | not-found status | C-CF-134 | Core features 12.1 |
| `Nothing lives at this address` | not-found heading | C-CF-135 | Core features 12.1 |
| `Back to the portfolio` | not-found link label | C-CF-136 | Core features 12.1 |
| `access_token` | login response field | C-CF-142 | Core features Auth |
| `email_taken` | signup rejection code | C-CF-145 | Core features Auth |
| `200` | health status | C-TR-03 | Technical requirements; Deployment contract |
| `0.7` | desktop fade in | C-TR-15 | Technical requirements journey contract |
| `0.2` | desktop fade out | C-TR-15 | Technical requirements journey contract |
| `0.86` | mobile fade in | C-TR-15 | Technical requirements journey contract |
| `0.1` | mobile fade out | C-TR-15 | Technical requirements journey contract |
| `block_type` | composer rule id | C-TR-18 | Technical requirements composer validation |
| `standfirst_first` | composer rule id | C-TR-19 | Technical requirements composer validation |
| `failure_required` | composer rule id | C-TR-20 | Technical requirements composer validation |
| `forward_required` | composer rule id | C-TR-21 | Technical requirements composer validation |
| `close_last` | composer rule id | C-TR-22 | Technical requirements composer validation |
| `failure_resolved` | composer rule id | C-TR-23 | Technical requirements composer validation |
| `heading_length` | composer rule id | C-TR-24 | Technical requirements composer validation |
| `paragraph_length` | composer rule id | C-TR-25 | Technical requirements composer validation |
| `media_caption` | composer rule id | C-TR-26 | Technical requirements composer validation |
| `media_ref` | composer rule id | C-TR-27 | Technical requirements composer validation |
| `meta_shape` | composer rule id | C-TR-28 | Technical requirements composer validation |
| `lines_shape` | composer rule id | C-TR-29 | Technical requirements composer validation |
| `menu_label_length` | composer rule id | C-TR-30 | Technical requirements composer validation |
| `note_length` | composer rule id | C-TR-31 | Technical requirements composer validation |
| `category` | composer rule id | C-TR-32 | Technical requirements composer validation |
| `cv_bullet_numeral` | composer rule id | C-TR-33 | Technical requirements composer validation |
| `heading_verb` | composer warning rule id | C-TR-34 | Technical requirements composer validation |
| `60` | Lumenar sequence length in seconds | C-TR-35 | Technical requirements telemetry rules |
| `completed` | session outcome | C-TR-35 | Technical requirements telemetry rules |
| `partial` | session outcome | C-TR-36 | Technical requirements telemetry rules |
| `discarded` | session outcome | C-TR-37 | Technical requirements telemetry rules |
| `truncated` | session outcome | C-TR-38 | Technical requirements telemetry rules |
| `longestHighMs` | health payload field | C-TR-39 | Technical requirements telemetry rules |
| `600000` | stuck-high threshold | C-TR-39 | Technical requirements telemetry rules |
| `triggersInWindow` | health payload field | C-TR-40 | Technical requirements telemetry rules |
| `120` | chatter threshold | C-TR-40 | Technical requirements telemetry rules |
| `nextIntervalMs` | ingest response field | C-TR-45 | Technical requirements telemetry rules |
| `30000` | minimum ingest interval | C-TR-45 | Technical requirements telemetry rules |
| `visits` | published figure field | C-TR-46 | Technical requirements telemetry rules |
| `medianDwellSeconds` | published figure field | C-TR-47 | Technical requirements telemetry rules |
| `dwellHistogram` | published figure field | C-TR-48 | Technical requirements telemetry rules |
| `trusted` | health status | C-TR-49 | Technical requirements telemetry rules |
| `degraded` | health status | C-TR-49 | Technical requirements telemetry rules |
| `untrusted` | health status | C-TR-49 | Technical requirements telemetry rules |
| `project` | highest search type | C-TR-51 | Technical requirements search rules |
| `labCaption` | lowest search type | C-TR-51 | Technical requirements search rules |
| `Built with` | metadata column feeding search tags | C-TR-52 | Technical requirements search rules |
| `GET /api/health` | health route | C-TR-03 | Technical requirements stack |
| `travelPx` | journey travel field | C-TR-16 | Technical requirements journey contract |
| `meta` | metadata rail field | C-TR-28 | Technical requirements composer validation |
| `lines` | headline lines field | C-TR-29 | Technical requirements composer validation |
| `menuLabel` | menu label field | C-TR-30 | Technical requirements composer validation |
| `note` | four-word note field | C-TR-31 | Technical requirements composer validation |
| `Which projects is this about?` | review scope group label | C-FE-73 | Front-end specification peer reviews |
| `Arial Narrow` | display family | C-UX-07 | UI/UX notes type |
| `Segoe UI` | body family | C-UX-08 | UI/UX notes type |
| `3` | Lumenar qualifying floor in seconds | C-DM-21 | Data model seed data |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the Stackr, Ascent and Vela bodies, and the Stackr and Ascent highlights | C-DM-20 | left to the builder; only their validity is required |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 4 |
| User roles | 12 | 18 |
| Core features | 120 | 146 |
| User flow | 20 | 20 |
| UI/UX notes | 22 | 23 |
| Technical requirements | 50 | 57 |
| Data model | 25 | 28 |
| Front-end specification | 85 | 88 |
| Constraints | 10 | 10 |
| Deployment contract | 40 | 42 |
