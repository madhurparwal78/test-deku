# Immersive Portfolio Ascent

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, travel the portfolio of the interaction designer Elian Kais Brandtsteiner from its opening headline to its summit, and send a message from the contact form that the summit headline turns into, without hitting an error page. That message must exist as a real row in PostgreSQL that the owner reads in the console; a success animation the page plays to itself does not count. The hard part is what stays private: a draft case study, the images attached to it in MinIO and every review its writer has not confirmed must stay unreadable to the public by any direct request, while published work and its media are served from the real object store.

## Overview

Immersive Portfolio Ascent is the personal portfolio of Elian Kais Brandtsteiner (short form `Elian Kais`), an interaction designer and creative technologist who builds physical, interactive installations: a mirrored light box you put your head inside (`Lumenar`), water projected onto a hanging form that flows around your hand (`Tide`), a block game played with real cubes (`Stackr`), and a phone app that replays a recorded climb on the wall it was recorded against (`Ascent`). Its audiences are studios and hiring leads, curators and exhibition programmers who need to know a piece survives four days alone in a dark room, and peers and course collaborators who want the making detail.

The home route is not a page of thumbnails. It is one continuous real-time three-dimensional scene that a visitor travels through; the page itself never scrolls. Around it sit document routes in two other visual registers: case studies on dark full-bleed media, a playground and a highlights reel on white paper under a black masthead band, and a printable curriculum vitae. Behind the site sit five working services: a contact inbox, a case study composer that holds every project fact once, an invitation-only peer review workflow, installation telemetry that turns the visitor numbers into published evidence, and a ranked search.

Five of those parts are extensions the reference site argued for and did not have, the peer review workflow, the composer, the telemetry, the search and the plain version with its choice of motion; everything else that remains is carried from the reference as observed. The parts most worth looking at are the journey, the headline that becomes the contact form, and the plain version.

It is deliberately **not** a blog, a shop or a social site: no comments, no likes, no public review form, no testimonial carousel, no newsletter, no analytics on individual visitors, no outbound email. The genuinely hard part is integrity: published review text is the reviewer's own confirmed words and nobody else can change it, draft work and its uploaded images stay private until the owner publishes, and a telemetry figure refuses to publish when its sensors cannot be trusted.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (no account) | read every published route, travel the journey, send a contact message, search, read published reviews and published telemetry figures | **read a draft project, its preview, its media or its search entries; read any unconfirmed, confirmed-but-undecided, declined or withdrawn review; read any reviewer email; reach any console route** |
| `reviewer` | everything a visitor can, plus: write a review through an invitation issued to its own email, see its own reviews and their revision notes, confirm its own review, withdraw its own review at any time | **reach any `/api/admin/` endpoint or any composer endpoint; see or act on another reviewer's review; publish, decline or edit anything; open a draft project** |
| `owner` | everything, including the composer, media upload, previews, publishing, invitations, moderation (publish, decline, ask for a revision), devices and telemetry runs, contact messages and the page view log | **change the body of any review; confirm or withdraw a review on a reviewer's behalf; publish a review its writer has not confirmed; publish a telemetry run whose trusted proportion is below 0.9** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a `reviewer` session to any `owner`-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds for a signed-out caller on every reviewer or owner endpoint, and for a reviewer acting on another reviewer's review.

Signup is **open**: anyone can create an account at `/signup`, and every new account gets the role `reviewer`; a `role` sent in the signup body is ignored. The single `owner` account is seeded and cannot be created through signup. Seeded accounts, all with the password `deku-demo-pw-2026`:

| Email | Role | Name |
|---|---|---|
| `owner@example.com` | `owner` | `Elian Kais Brandtsteiner` |
| `reviewer@example.com` | `reviewer` | `Riya Anand` |
| `reviewer2@example.com` | `reviewer` | `Kit Fenwick` |

## Core features

### 1. Draft work and its media stay private; published media lives in MinIO

1. An image the owner attaches to a project through `POST /api/projects/{key}/media` is stored in MinIO, in the bucket named by `STORAGE_BUCKET`, at the key `projects/{project_key}/{sha256_of_bytes}.{ext}`, for example `projects/tide/9f2a...d0.png`, where the hash is the lowercase hex SHA-256 of the exact uploaded bytes and `ext` is `png`, `jpg` or `webp`. The bytes live nowhere else: not on the app's disk and not in a database column. Uploading bytes that are not PNG, JPEG or WebP is rejected as invalid (`unsupported_media`), and a file over 5242880 bytes is rejected (`media_too_large`); nothing is stored in either case.
2. Uploading the same bytes to the same project again, including two identical uploads sent at the same instant, leaves exactly one object and exactly one `project_media` row for that key, and both calls return the same `objectKey`.
3. While a project's `status` is `draft`, its record, its route `/case-study/{key}`, its media at `GET /api/media/{object_key}` and its search documents are readable only by the owner or by a request carrying a live preview token (`?preview={token}`). Any other request is answered as not found, exactly as for a key that does not exist. The seeded draft `vela` must stay unreadable this way.
4. Once the project is published, `GET /api/media/{object_key}` serves its media to anyone, byte-for-byte identical to the upload, read from MinIO.

### 2. The contact form

The summit headline of the journey becomes the contact form (the full visual treatment is under Front-end specification).

1. `POST /api/contact` with `name`, `email`, `message`, an empty `website` and an `elapsedMs` of at least `2000` stores the message and answers `{"ok": true}`. The owner sees it, newest first, in `GET /api/admin/messages` and on `/console/messages`.
2. A missing or blank `name`, `email` or `message` is rejected with code `missing_field`; a malformed email is rejected with `invalid_email`; a message over 4000 characters is rejected with `too_long`. Nothing is stored for any rejection.
3. `website` is a field real people never see. A submission with a non-empty `website`, or with `elapsedMs` below `2000` or absent, is answered `{"ok": true}` and silently discarded: nothing is stored.
4. At most `5` messages are accepted per sender email per rolling hour, and at most `20` per client network address per rolling hour. The next one is rejected with `rate_limited` and not stored.
5. The page maps each `code` to its own copy and never shows server text: missing email `Add your email.`, malformed email `That email doesn't look right.`, `rate_limited` or any failure `Couldn't send.`, no answer within 10 seconds `Timed out, try again.`, success `Thanks, I'll reply as soon as I can.` with the headline `I'LL BE IN TOUCH`. The send control reads `Say hi`, then `Send` while the form is open, then `Message sent`, and `Try again` after a failure. The send control stays unavailable until a name and a message are written.

### 3. The immersive journey

1. The home route `/` is exactly one viewport tall and never scrolls. Wheel, touch, the arrow keys, Page Up, Page Down, Home and End move one journey position between `0` (arrival) and `1` (the summit); Home reaches `0` and End reaches `1`. Scrolling backwards runs everything backwards exactly, stopping leaves the world where it stopped, and nothing replays.
2. Tabbing to a project tile, a summit control or the contact form travels the journey to that component, and travelling the journey moves keyboard focus along with it when focus was inside the component being left.
3. `GET /api/journey` returns the timing table and the tile bands the page runs on (shape under Deployment contract). The project band is divided into equal parts, one per published project in registry order; publishing another project reflows every band, and a draft never receives a band. The desktop project band runs from `42.5` to `87` and the mobile band from `35` to `96`, so the five seeded tiles on desktop occupy `42.5` to `51.4`, `51.4` to `60.3`, `60.3` to `69.2`, `69.2` to `78.1` and `78.1` to `87`, with menu targets `0.4695`, `0.5585`, `0.6475`, `0.7365` and `0.8255`.
4. The journey length is a constant distance, not a page count: `travel` is `max(1, (4.2 - 1) * 1110)`, which is `3552`, and `pages` is `min(6.5, max(4.2, 1 + 3552 / viewportHeight))` on desktop, so a 900-tall window runs `4.947` pages and a 1110-tall window runs `4.2`. The mobile branch always runs `5.8` pages.
5. Choosing a project from the Work menu travels the journey to the middle of that project's band; it never loads another page.
6. The sky has three stages driven by the journey: near-black below `0.42`, near-black with a faint cool cast from `0.42`, and near-white from `0.9`. Crossing `0.9` starts a timed flip that finishes on its own clock whatever the scrolling speed; the navigation ink flips with the sky's own eased value, not with the threshold.
7. Pointing at a project tile reveals that project's image through a real-time liquid simulation; the paint arrives at once, holds for about a second after the pointer leaves, then drains. The reveal is never switched off on a weaker device, only made coarser.
8. Scene audio is silent until the sound control is pressed, the choice survives a reload, turning it off fades the whole mix without restarting the birdsong, and it never starts on its own for a visitor who prefers reduced motion.

### 4. Case study hub and detail

1. `/case-study` shows exactly one cell per published case study, ordered by `hubOrder` (seeded: `Lumenar`, `Tide`, `Stackr`, `Ascent`), each cell one link to `/case-study/{key}` carrying the eyebrow `SELECTED WORK | <menu label>` and the project's two headline lines. There is no page heading, introduction or filter.
2. `/case-study/{key}` renders the project's headline, its three-column metadata rail (headings from the record, never stacked) and its body blocks in stored order. An unknown key, or a draft without a live preview token, renders the not-found page.
3. The foot of every case study carries a card for the next published project in registry `order`, eyebrow `VIEW NEXT PROJECT`; the last case study points at the playground with the eyebrow `VIEW PLAYGROUND`. Below it: `Top`, the heading `Get in Touch`, and the channels `Email`, `LinkedIn`, `Instagram`.
4. When published reviews are scoped to the project, at most two of them, newest decision first, appear after the closing statement and before the next-project card, under the heading `What people who were there said`; with none, the block is absent.
5. Every video carries a control bar beneath it (a play control and a range scrubber) and a text alternative; for a visitor who prefers reduced motion no video plays by itself.

### 5. Playground and highlights

1. `/lab` (masthead `OFF THE MAIN ROUTE`) and `/highlights` (masthead `PROJECT HIGHLIGHTS`) open on top of the journey. `← BACK` returns to the previous route; `× Close` dismisses the overlay and returns to `/` at the exact journey position it was opened from.
2. `/lab` carries the groups `Making`, `Creative coding` and `Motion, package, graphic, art`, the four making entries with prose and the labelled grids listed under Front-end specification. Its one outbound link opens elsewhere, says so in its accessible name, and carries `rel="noopener"`.
3. `/highlights` carries one entry per published case study in registry order: eyebrow and headline lines, the project's highlight heading and paragraph, the first curriculum vitae bullet of that project containing a numeral, and `Read full case study ↗`. A project with a published telemetry run also shows its stat row (feature 9).

### 6. Curriculum vitae

1. `/cv` is the only route that scrolls natively. It shows the name, role line, contact details, the facts `London, UK`, `relocation across Europe`, `German (native), English (fluent), Spanish (basic)` and `EU citizen (Austria). Eligible for UK Graduate Route`, the aside sections `Education`, `Skills`, `Recognition and Talks` and the main sections `Experience` and `Selected Work`.
2. `Selected Work` is generated from the published case study records, in registry order, never typed a second time; `GET /api/cv` returns the same content. Every bullet in it contains a numeral.
3. `Download PDF` produces this page's own print output. When printed, the fixed bar and the sheet shadow disappear and the teal headings stay.

### 7. Peer reviews

The property that makes this feature worth building, and the problem it solves, is that the published text is the reviewer's own confirmed words: the owner can publish it or decline it but never change it.

1. The owner issues an invitation with `POST /api/admin/invitations` (`email`, `scope`). It returns a 22-character token and the link `/review/{token}`, valid for 30 days. Nothing is emailed; the owner hands the link over.
2. A signed-in reviewer whose account email equals the invitation's email reads it with `GET /api/review/{token}` and submits with `POST /api/review/{token}`. An unknown token, an expired token, a token used more than 48 hours ago and a token issued to another email are all answered identically: not found, same body. A signed-out caller is denied whatever the token.
3. A submission needs `reviewerName` (1 to 60 characters), `reviewerRole` (1 to 80), `relationship` (`collaborator`, `tutor`, `exhibitor`, `client` or `peer`), `scope` (one or more published project keys or `practice`) and a `body` of 40 to 220 words; `organisation` (0 to 80) and `period` are optional. Violations are rejected with `missing_name`, `missing_role`, `invalid_relationship`, `missing_scope`, `invalid_scope`, `body_too_short`, `body_too_long` or `field_too_long`, and nothing is stored.
4. A new submission enters `awaiting_confirmation`. Submitting again through the same invitation while the review is still `awaiting_confirmation` replaces its text; while it is `submitted` after a revision request it creates a new review and the old one becomes `withdrawn`; in any other state it is rejected with `already_submitted`. However many submissions arrive at once, an invitation never carries more than one review that is not `withdrawn`.
5. Only the review's own writer confirms it (`POST /api/my/reviews/{review_id}/confirm`, from `awaiting_confirmation` to `confirmed`). From that moment its body never changes: no endpoint in any role edits a review body, and a request to one is rejected with the body unchanged.
6. The owner publishes only a `confirmed` review; publishing any other state is rejected and nothing changes. The owner may decline (`declined`, reason kept private) or ask for a revision (`submitted`, note shown only to the writer) a review that is `confirmed` or `submitted`.
7. The writer withdraws their own review at any time (`POST /api/my/reviews/{review_id}/withdraw`); it leaves every public surface immediately. Another reviewer attempting either action is denied and the review is unchanged.
8. Rate limiting keeps abuse out: invitation lookups that fail are limited to 10 per client address per hour, after which each further attempt waits two seconds, and a failed lookup takes the same time as a successful one; confirmations are limited to 5 attempts per review per hour. No endpoint accepts a review body without a valid invitation.
9. `GET /api/reviews` and `/peer-reviews` show only `published` reviews, never an email, a token, a decline reason or a revision note. `/peer-reviews` groups them by project in registry order with `the practice as a whole` last, newest decision first, each as plain text with the attribution line; with none published it shows `Nothing published yet`. The summit control reads `View feedback (<n>)` when `n` published reviews exist and plain `View feedback` when none do.

### 8. The case study composer

1. Every project is one record; the home tile, the hub cell, the detail route, the highlights entry, the curriculum vitae entry, the next-project card and the search documents are all generated from it. Publishing a change updates all of them.
2. `PUT /api/projects/{key}` (owner) validates the record and returns `{"valid": ..., "findings": [...]}`. A record with any `error` finding is rejected and nothing is stored; a record with only `warning` findings is stored. A new key is stored as a `draft` and receives the next two-digit creation `id`.
3. The body is a closed set of five block types, `standfirst`, `statement`, `stickyMedia`, `mediaPair` and `caption`, and statements carry a `kind` of `claim`, `method`, `failure`, `change`, `forward` or `close`. For a case study the composer enforces the rules named under Technical requirements, among them: exactly one standfirst and it comes first, at least one `failure`, at least one `forward`, every `failure` followed later by a `change`, exactly one `close` and it comes last.
4. `POST /api/projects/{key}/publish` makes a draft public; `POST /api/projects/{key}/preview` returns a preview link valid for 30 minutes that renders the draft through the real case study template, not an editor's version.

### 9. Installation telemetry

1. The owner provisions a device for a run (`POST /api/admin/devices`) and receives its key once; rotating the key (`POST /api/admin/devices/{device_id}/rotate`) makes the old key stop working immediately. A device key writes only its own device's events.
2. `POST /api/ingest` accepts a batch of at most 256 events. The triple `deviceId`, `bootId`, `seq` identifies an event: a replayed batch, or the same batch sent twice at the same instant, stores each event exactly once and reports only new events as `accepted`. A larger batch is rejected (`batch_too_large`) and nothing is stored; a missing or wrong key is denied (`device_unauthorized`).
3. Presence events fold into sessions, and sensor-health events decide which minutes can be trusted, by the rules under Technical requirements. Untrusted time is excluded from every figure and counted separately.
4. `POST /api/admin/runs/{run_id}/publish` refuses a run whose trusted proportion is below `0.9` (`untrusted_run`, with the proportion) and otherwise freezes its figures; later events never change a published run. `GET /api/runs/{run_id}` returns published figures and answers not found for a run that is not published.
5. The seeded run `lumenar-crosswire-2026` is published with `372` visits, `221` stays of at least 15 seconds, `67` complete viewings and a median stay of `20` seconds. The highlights entry for `Lumenar` shows its stat row: `372` `visits`, `67` `stayed the full 60 seconds`, `20 seconds` `median stay`, `4 days` `unattended`, and the dwell histogram titled `How long people stayed`.

### 10. Search

1. `/search` and `GET /api/search?q=` search every published project, case study section, playground entry and caption, curriculum vitae entry and skill, and published review. Drafts and unpublished reviews are never indexed.
2. Results are grouped by type in the fixed weight order `project`, `caseStudySection`, `cvEntry`, `review`, `labEntry`, `cvSkill`, `labCaption`, never interleaved; within a group, higher score first. A search for `TouchDesigner` therefore lists the `Tide` and `Lumenar` projects before any caption.
3. A document matching only some of the query's words scores the cube of the share it matched, so a document matching both words of a two-word query outranks one matching either. One typing error is forgiven on words of five or more letters, never on tool and material tags.
4. With nothing matched, the page shows `Nothing matched. Try one of these.` above the twelve most used tags.

### 11. The plain version, and choosing motion

1. The Reach me menu carries a `Motion` control with `Full`, `Reduced` and `None`. Choosing `None` swaps the page to the plain version in place without a reload, and the choice survives a reload.
2. `/flat` is the whole portfolio as a document: the name, the role line and the opening headline as static type; the five published registry entries with their headline lines, labels and category; the biography; the summit headline with the same contact form (every state and copy of feature 2, without the morph); and the route list as visible links. Its foot carries `This is the plain version of the site. Your browser or device could not run the moving one.` and `Try the moving version`.
3. A browser that cannot run the moving scene gets the plain version silently: no apology panel, no retry control, and no word of content missing.

### 12. Pages every visitor relies on

1. An unknown address renders the portfolio's own not-found page with the heading `Nothing lives at this address` and a link `Back to the portfolio` to `/`, and the response status is `404`.
2. Every internal link on every public route resolves; none leads to the not-found page.
3. Each public page view is recorded with its route and time only, whether the page was loaded directly or reached from inside the app, and the owner reads the log newest first at `/console/page-views` (`GET /api/admin/page-views`). Console, sign-in and reviewer pages are not recorded.

### Auth

Email and password accounts implemented by the app. `POST /api/auth/login` takes `email` and `password` and returns `access_token` and `user`; the client sends `Authorization: Bearer <access_token>`, and a token stops working 12 hours after it was issued. Passwords are stored hashed, never as plaintext. `POST /api/auth/signup` takes `email`, `password` (at least 10 characters) and `name`; an email already registered, compared without regard to letter case, is rejected (`email_taken`). There is no password reset and no social sign-in.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the immersive journey, summit and contact form | public |
| `/case-study` | case study hub | public |
| `/case-study/{key}` | case study detail; a draft only with `?preview={token}` | public |
| `/lab` | playground overlay | public |
| `/highlights` | highlights overlay | public |
| `/cv` | curriculum vitae | public |
| `/peer-reviews` | published peer reviews | public |
| `/search` | ranked search | public |
| `/flat` | the plain version | public |
| `/sitemap.xml` | sitemap | public |
| `/robots.txt` | robots file | public |
| `/login` | sign in | public |
| `/signup` | create a reviewer account | public |
| `/review/{token}` | write a review through an invitation | reviewer |
| `/my-reviews` | the reviewer's own reviews and revision notes | reviewer |
| `/my-reviews/{review_id}` | the review as it will be published, with `This is right`, `Let me change it` and `Withdraw` | reviewer |
| `/console` | goes to `/console/projects` | owner |
| `/console/projects` | card grid of every project record, draft and published | owner |
| `/console/projects/new` | create a project record | owner |
| `/console/projects/{key}` | the composer for one record | owner |
| `/console/reviews` | moderation queue | owner |
| `/console/invitations` | issue and list invitations | owner |
| `/console/runs` | telemetry runs, devices, health, publication | owner |
| `/console/messages` | contact messages | owner |
| `/console/page-views` | page view log | owner |

**Entry and redirects.** A signed-out visitor opening a `/console` or `/my-reviews` route goes to `/login` and returns there after signing in. After signing in, the owner lands on `/console/projects` and a reviewer on `/my-reviews`. `Sign out` sits in the console sidebar and on `/my-reviews` and returns to `/`. A token that stops working mid-action sends the person to `/login` while keeping their unsaved draft on the page. A reviewer opening a console route gets the not-found page. A signed-out visitor on `/review/{token}` sees the same sign-in or create-account prompt for every token. Closing an overlay returns to the journey position it was opened from.

**Journeys.**
1. Contact: open `/`, press End, press `Say hi`, type a name over `YOUR NAME` and an email over `YOUR EMAIL`, write a message, press `Send`, see `Message sent` and `Thanks, I'll reply as soon as I can.`; signed in as `owner@example.com`, the message tops `/console/messages`.
2. Case study: open `/case-study`, choose the `Tide` cell, read `An interactive installation of water that flows around your hand` with the rail `My Role`, `Built with`, `Shown`, and reach the `VIEW NEXT PROJECT` card for `Ascent`.
3. Review: signed in as `reviewer2@example.com`, open `/review/Rv7Kq2Lm9Xw4Tz8Bn3Hc5D`, fill `YOUR NAME`, `YOUR ROLE`, a relationship, `Stackr` under `Which projects is this about?` and a body, send, land on `/my-reviews/{review_id}`, press `This is right`; sign in as `owner@example.com`, publish it on `/console/reviews`; `/peer-reviews` shows it under `Stackr`.
4. Composer: as `owner@example.com`, open `/console/projects/new`, fill a record, save and read each finding next to the block it belongs to, attach an image, open the preview, publish; the project joins `/`, `/case-study`, `/highlights`, `/cv` and search.
5. Telemetry: on `/console/runs`, read the health strip of `Lumenar at Crosswire 2026`, whose icon and word read `trusted`; open `/highlights` and read its stat row.
6. Search: open `/search`, type `TouchDesigner`, and read the Projects group first.
7. Plain version: open the Reach me menu, choose `Motion`, then `None`, and read the plain version with its notice at the foot.

**States.** Every list has an empty state (`Nothing published yet`, `Nothing matched. Try one of these.`, an empty message list, an empty page view log, an empty run list). Every page has a loading state: the counting loader on `/`, a sweeping highlight across placeholder blocks elsewhere. A failed request never crashes a page: public pages show their status copy and the console shows an inline banner above the working area.

## UI/UX notes

**North star:** a stranger should feel they are travelling through one continuous place, then reading honest documents about how the work was made. **Register:** immersive and editorial at once, three registers switched abruptly on purpose: the immersive journey, the editorial dark case studies and the editorial light playground, highlights, curriculum vitae, search, peer reviews and plain version. The abruptness is part of the identity: stillness over decoration, content over chrome.

**Palette by role.** The page has almost no colour; colour is something the scene does and paper does not. Immersive ground: near-black neutral, taking a faint cool cast when the first project arrives, then near-white cool neutral at the summit. Editorial light ground: a near-white neutral paper, with near-white neutral raised cards. Ink: near-black neutral on paper, near-white neutral over media. Muted text: a mid cool neutral. The single accent is a deep, vivid blue; it is the only saturated colour any stylesheet may carry, and it marks matched search words and the histogram bars and nothing else. The only coloured type anywhere is the mid, muted teal of the curriculum vitae headings. The masthead band is pure near-black neutral over pure near-white neutral paper. Blue light, cyan glow, green-black rock and, above the sunrise only, orange and amber warmth belong to the three-dimensional scene, never to a panel. Failure, in-progress and success appear only in the owner console, on its near-black surface, as a light vivid red, a mid vivid amber and a light soft green, each always with an icon and a word. No page may be tinted, no card may carry a hue, and no highlight box may appear behind text. The exact shades are yours, so long as those rules hold.

**Type.** A condensed, heavy grotesque for every headline, set in uppercase, arriving soft and sharpening into place; a humanist sans for body copy; figures align wherever numbers stack. Display family `Arial Narrow`, body family `Segoe UI`, with the exact stacks and sizes under Front-end specification. The standfirst is the body size and differs only in being tighter.

**Shape and density.** Text controls barely rounded, cards gently rounded, the large media shell generously rounded, pill controls fully rounded. Exactly four soft shadows in the whole build, and only the curriculum vitae sheet's shadow carries a cool tint. Density is spacious: reading measure of fifty-five to seventy characters, sections read as separate without dividing lines.

**Motion.** The motion character is eased: one signature easing that covers most of its travel at once and then coasts, used almost everywhere, and one symmetric easing reserved for the sunrise and the navigation veil. On the journey every transition is bound to position and has no clock of its own; on document routes things move only when the visitor does something. Hovering changes faintness only, at three levels, and every hover state is also a focus state. There is no bounce, no overshoot, no staggered list reveal and no page transition. Respect the reduced-motion preference fully: no birds, no rain, no glow, no pointer tipping, one still frame of the world, an instant sunrise, no self-playing video.

**Components.** Controls have resting, pointed-at, pressed, focused and unavailable states, and unavailable is never shown by colour alone. Escape closes an overlay, then a dropdown, in that order. Menus drop their items down into view from behind a clipping edge rather than fading. The owner console confirms before anything irreversible and reports every action in an inline banner.

**Accessibility and responsive.** Text and its background meet WCAG AA contrast, including white type over moving media, which carries a faint dark halo. Full keyboard navigation with a two-tone focus ring visible over light and dark media, comfortably sized touch targets of at least 44 by 44 CSS pixels, labels on every icon-only control, meaning never carried by colour alone, and one level-one heading per route. The layout is responsive and holds at every width between a phone and a wide desktop, with one layout breakpoint at portrait-tablet width. At a narrow viewport nothing overflows sideways and every navigation target stays reachable.

**Mode.** Both registers are designed fully as they are; the system dark-scheme preference changes nothing.

**What it must not look like:** a grid of thumbnails on the home route, a header bar or footer bar, tinted panels, a yellow search highlight, a testimonial carousel with quotation marks, photographs or star ratings, or a marketing composition where the work belongs.

## Technical requirements

**Stack.** The rendering model is server-rendered pages with interactive islands: every route's HTML, including its headings, copy, links and the crawlable route list, is produced on the server and reaches the browser complete on first paint; the scene, the liquid reveal, the liquid type, the composer, the search box and the contact form hydrate as islands on top.
- Frontend: SvelteKit on Node 20, served from its production Node build.
- Backend: FastAPI on Python 3.12, serving the JSON API under `/api`.
- Real-time graphics: Three.js (WebGL) for both drawing surfaces and the liquid simulation.
- Audio: the browser's built-in Web Audio API; every sound is synthesised, no audio file exists.
- Database: PostgreSQL, the `postgres` service, at `DATABASE_URL`.
- Object store: MinIO, the `minio` service, at `STORAGE_ENDPOINT` with bucket `STORAGE_BUCKET` and credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`.
- One public listener on container port `4173` fronts both the SvelteKit server and FastAPI on the same origin.
- Health: `GET /api/health` returns `200` once PostgreSQL and the bucket are reachable.
- Logging: one line per request to stdout with method, path, status and duration.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are `postgres` (PostgreSQL) and `minio` (MinIO), and reaching for anything else is a contract violation. No request leaves the container at runtime.

**Architecture.** Module layout and architecture are yours, as long as every tunable value of the journey lives in one configuration that the page and `GET /api/journey` both read; that single configuration is what gives the timing its testability without drawing the scene.

**Environment.** Read `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`, `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` from the environment and hardcode none of them. PostgreSQL and MinIO are already running at those variables, and the bucket already exists.

**Nothing secret reaches the browser.** No credential, storage key, database URL or token of another person appears in any HTML, script, style or JSON the browser downloads.

**No shipped binary asset.** The build carries no image, video, audio, three-dimensional model or font file: no image in a modern or photographic format, no model file, no binary module format and no compressed-mesh decoder. Every placeholder image and video, the scene geometry, the textures and the sounds are generated in the browser; the type uses installed fonts only. The only binary responses the app ever sends are owner-uploaded media from `GET /api/media/{object_key}`.

**Sitemap and robots.** `/sitemap.xml` lists the absolute URL, under `APP_PUBLIC_URL`, of every public route: `/`, `/case-study`, each published `/case-study/{key}`, `/lab`, `/highlights`, `/cv`, `/peer-reviews`, `/search` and `/flat`. It never lists a draft, a console, sign-in, review or preview route. `/robots.txt` names that sitemap on a `Sitemap:` line.

**The journey contract.** Every visual state on the home route is a pure function of one journey position read from one source; no component derives its own progress from a second clock. The timing table, in whole percent of the journey:

| Component | `name` | Desktop | Mobile |
|---|---|---|---|
| Scroll indicator | `scrollIndicator` | `0` to `8` | `0` to `8` |
| Opening headline | `openingHeadline` | `0` to `42` | `0` to `34` |
| Project tiles | `projectTiles` | `42.5` to `87` | `35` to `96` |
| Summit headline | `summitHeadline` | `90` to `100` | `96.5` to `100` |
| Contact call to action | `contactCta` | `92` to `100` | `97` to `100` |
| Biography panel | `biographyPanel` | `86` to `100` | `93` to `100` |
| Case study preview card | `caseStudyPreview` | `90` to `100` | `96.5` to `100` |

Global fade in `0.7` and fade out `0.2` on desktop, `0.86` and `0.1` on mobile. Tile band `i` of `n` runs from `start + i * width` to `start + (i + 1) * width` with `width = (end - start) / n`; its menu target is `(start + end) / 200`. Band edges and menu targets are rounded to four decimals, `pages` to three, `travelPx` to a whole number, where `travelPx = round((pages - 1) * viewportHeight)`. The desktop scene branch versus the mobile branch is a capability decision, not a window width.

**Composer validation.** Every finding is `{"rule", "severity", "blockIndex", "message"}` with `severity` `error` or `warning` and `blockIndex` null for record-level rules. The rule identifiers:

| `rule` | Severity | Fires when |
|---|---|---|
| `block_type` | error | a block's `type` is not one of the five |
| `standfirst_first` | error | a case study does not have exactly one `standfirst`, first |
| `failure_required` | error | a case study has no `failure` statement |
| `forward_required` | error | a case study has no `forward` statement |
| `close_last` | error | a case study does not have exactly one `close` statement, last |
| `failure_resolved` | error | a `failure` statement has no `change` statement anywhere after it |
| `heading_length` | error | a statement heading is longer than 64 characters |
| `heading_verb` | warning | a statement heading reads as a label with no verb |
| `paragraph_length` | error | a body paragraph is under 20 or over 120 words, or a standfirst lead is over 60 words |
| `media_caption` | error | a `stickyMedia` or `mediaPair` block has neither `caption` nor `captionReason` |
| `media_ref` | error | a media reference names an object not uploaded for this project |
| `meta_shape` | error | `meta` is not exactly three columns of one to four rows, or a heading is not `My Role`, `Built with`, `Shown` or `Focus` |
| `lines_shape` | error | `lines` is not exactly two non-empty strings |
| `menu_label_length` | error | `menuLabel` is not 1 to 12 characters |
| `note_length` | error | `note` is not three to five words |
| `note_imperative` | warning | `note` does not open with a verb |
| `category` | error | `category` is not `CREATIVE COMPUTING`, `AR DEVELOPMENT`, `PHYSICAL COMPUTING`, `CREATIVE CODING` or `LAB` |
| `cv_bullet_numeral` | error | a curriculum vitae bullet contains no numeral |

Body rules apply to records whose `opens` is `caseStudy`; a `lab` or `none` record may have an empty body. A stored record never carries an `error` finding.

**Telemetry rules.** Within one boot of one device, events are ordered by `seq`. A `presence_start` opens a session and the next `presence_end` closes it; its duration is the difference of their `uptimeMs`. A second start while a session is open, and an end with none open, are ignored. When any event arrives for a newer boot of the same device, a session still open in an older boot ends as `truncated`. A closed session is `completed` when it lasts at least the project's `sequenceSeconds` (`60` for `lumenar`), `partial` when it lasts at least its `floorSeconds` (`3`) but less, and `discarded` when shorter. Each `sensor_health` event describes the 60 seconds of uptime ending at its `uptimeMs`, and that window is untrusted when `longestHighMs` is above `600000`, when `triggersInWindow` is above `120`, when it belongs to a run of 8 or more consecutive health windows with `triggersInWindow` of `0` inside the run's opening hours (`openFrom` `00:00` to `openTo` `24:00` means always open), or when `ambientReference` differs by more than 25 percent from the first health window of that boot. A session overlapping an untrusted window is `discarded` and untrusted. The trusted proportion is trusted windows over all windows of the run's devices, and is `0` with no windows. The server anchors a boot to wall-clock time once, at the first batch it receives for that boot, and applies that one offset to the whole boot. Batches arrive at most once per 30 seconds; every ingest response carries `nextIntervalMs` of at least `30000`, and the device obeys a longer one.

Published figures: `visits` counts trusted `completed` and `partial` sessions; `staysBeyond15` counts those lasting at least 15 seconds; `completeViewings` counts the `completed` ones; `medianDwellSeconds` is their median duration in seconds, rounded half up (the mean of the middle two for an even count); `completionRate` is `completeViewings / visits` to four decimals (`0` with no visits); `trustedProportion` to four decimals; `unattendedSeconds` is the longest single boot's largest `uptimeMs`, in whole seconds; `dwellHistogram` counts visits into the bins `0-5`, `5-10`, `10-15`, `15-20`, `20-30`, `30-45`, `45-60` and `60+` seconds, each including its lower edge. A run's health `status` is `trusted` at a proportion of at least `0.9`, `degraded` from `0.5`, and `untrusted` below. `unattended` is shown in whole days when at least a day, otherwise in whole hours.

**Search rules.** The index is built from the records whenever something is published, and fetched by the page the first time the search field gains focus; `GET /api/search` gives the same ranking on the server. Type weights: `project` `1.0`, `caseStudySection` `0.85` (one document per body block), `cvEntry` `0.7`, `review` `0.6`, `labEntry` `0.5`, `cvSkill` `0.35`, `labCaption` `0.25`. The weights are an editorial judgement: a project is what the site is about; a case study section is the substance but a fragment of a larger argument; a curriculum vitae entry is the same facts compressed; a review is corroboration, valuable but secondary to the work; a playground entry is real but deliberately minor; a skill list matches almost everything; a caption is one line of thirty. A project document's tags are its three labels and the rows of its `Built with` column. Scoring: `weight * (3.0 * phraseHitsInTitle + 1.8 * tokenHitsInTitle + 1.4 * exactTagHits + 0.7 * prefixTagHits + 1.0 * phraseHitsInBody + 0.4 * tokenHitsInBody * idf) * recency * coverage`, where `recency` is `1.0` for the current and previous year, falling by `0.05` per further year to a floor of `0.7`, and `coverage` is the fraction of query words the document matches at all, cubed. Body words are stemmed; tags never are. Typo tolerance: one edit on words of five or more letters, never on tags. The search box settles for a moment after typing before it runs, then announces `<n> results` politely.

**The capability ladder.** Four rungs, each carrying every route and every word: `full` (two drawing surfaces, pointer drift, the glow, seven birds, three rain planes, full liquid type, audio), `lean` (one surface, no pointer effects, five birds, one rain plane, liquid type on entry only), `still` (one frozen frame, no birds or rain, instant sunrise, no audio) and `flat` (no real-time graphics, native scrolling). The reference site's four quality tiers, `low`, `mid`, `high` and `ultra`, map onto these rungs; what they teach is the priority order: the fluid reveal is never sacrificed, only its resolution falls, the birds survive every tier, the cursor glow is the first thing cut, rain is a luxury, and antialiasing, smoothing the stepped edges of diagonal geometry at a real cost, is the last thing added, on `ultra` only. A software rasteriser counts as no graphics adapter; a discrete or Apple silicon adapter counts as a strong one. The rung is chosen by measurement, never by reading a browser identification string: a failed real-time context means `flat`; a small maximum texture, less than 4 gigabytes of memory, fewer than 4 logical processors or a coarse pointer cap it at `lean`; a reduced-motion preference caps it at `still`; the visitor's saved `Motion` choice wins over all of them. While running, a rolling window of 90 frames against the 60 frames per second budget demotes one rung when more than a quarter of frames miss for two consecutive windows, and promotes at most once per session after six consecutive windows under a twentieth. Two lost contexts in one session force `flat` for the rest of it.

**Performance.** Largest contentful paint (the moment the biggest thing in the first screenful has appeared) under 2.5 seconds on `full`, 2.0 on `lean`, 1.5 on `still` and 1.0 on `flat`; no layout shift after the loader hands over; the first scene movement within a tenth of a second of input; the page's code before media under 900 kilobytes on `full`. Idle loops stop themselves, and fewer than 160 elements carry promotion hints.

## Data model

Ten tables below are pinned by name and field; every one has an integer `id` primary key, and any further storage you need is yours to design. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### users
`email` (unique without regard to letter case), `name`, `role` (`owner` or `reviewer`), `password_hash` (never the plaintext password), `created_at`.

### projects
`key` (unique, lowercase kebab-case), `creation_id` (two-digit string, returned as `id`), `display_order` (returned as `order`), `hub_order` (`hubOrder`), `menu_label` (`menuLabel`), `lines`, `lines_mobile` (`linesMobile`), `category`, `labels`, `note`, `opens` (`caseStudy`, `lab` or `none`), `status` (`draft` or `published`), `headline`, `meta`, `body`, `cv`, `highlight`, `hero`, `telemetry`, `created_at`, `updated_at`, `published_at`. `eyebrow` (`SELECTED WORK | ` followed by the menu label, and `OFF ROUTE | PLAYGROUND` for the playground), `path` (`/case-study/{key}` for a case study, `/lab` for the lab record), the next-project card and the journey bands are derived on read and never stored. Two projects never share a key.

### project_media
`project_key`, `object_key`, `sha256`, `content_type`, `size_bytes`, `created_at`. One row per object key, also when identical uploads arrive together.

### invitations
`token` (22 characters from the base62 alphabet, drawn from a cryptographic source), `email`, `scope`, `issued_at`, `expires_at` (30 days after issue), `used_at` (the first successful submission). An invitation is usable while it has not expired and either has never been used or was first used less than 48 hours ago.

### reviews
`public_id` (22 opaque characters, returned as `id`), `invitation_id`, `reviewer_user_id`, `reviewer_name`, `reviewer_role`, `relationship`, `organisation`, `scope`, `period`, `body`, `state` (`submitted`, `awaiting_confirmation`, `confirmed`, `published`, `declined` or `withdrawn`), `submitted_at`, `confirmed_at`, `decided_at`, `withdrawn_at`, `decline_reason`, `revision_note`. The `attribution` returned by the API is derived. An invitation carries at most one review whose state is not `withdrawn`, even when two submissions arrive at the same instant. A review body never changes once `confirmed_at` is set. A review never confirmed within 30 days of submission is removed.

### contact_messages
`name`, `email`, `message`, `created_at`. Discarded submissions are never written.

### page_views
`route` (the path only, no query string), `viewed_at`. No address, device, agent string or cookie is kept.

### devices
`device_id` (unique), `run_id`, `key_hash` (the key is never stored in plain form), `created_at`, `rotated_at`.

### runs
`run_id` (unique), `project_key`, `title`, `starts_on`, `ends_on`, `open_from`, `open_to`, `state` (`open` or `published`), `published_at`, `figures` (frozen at publication, empty while open).

### telemetry_events
`device_id`, `boot_id`, `seq`, `uptime_ms`, `kind` (`presence_start`, `presence_end`, `heartbeat` or `sensor_health`), `payload`, `received_at`. The triple `device_id`, `boot_id`, `seq` is unique: however many times, and however simultaneously, one event arrives, it is stored once. Sessions, windows, health and the figures of an open run are derived on read.

### Seed data

Seeding runs on first start and is idempotent: restarting the app must not duplicate rows.

**Accounts:** the three in User roles.

**Projects** (registry `order` and `hubOrder` decide every surface):

| `key` | `id` | `order` | `hubOrder` | `status` | `opens` | `menuLabel` | `lines` | `category` | `note` |
|---|---|---|---|---|---|---|---|---|---|
| `lumenar` | `03` | 1 | 1 | `published` | `caseStudy` | `Lumenar` | `A MIRRORED LED BOX` / `THAT FEELS INFINITE` | `CREATIVE COMPUTING` | `Work the problem` |
| `stackr` | `02` | 2 | 3 | `published` | `caseStudy` | `Stackr` | `PLAYFUL BLOCK GAME` / `WITH SPLIT CONTROL` | `CREATIVE COMPUTING` | `Build it in time` |
| `tide` | `01` | 3 | 2 | `published` | `caseStudy` | `Tide` | `WATER THAT FLOWS` / `AROUND YOUR HAND` | `CREATIVE COMPUTING` | `Touch finds the line` |
| `ascent` | `04` | 4 | 4 | `published` | `caseStudy` | `Ascent` | `ELIAN KAIS THE APP` / `READS THE CLIMB` | `AR DEVELOPMENT` | `The full pitch` |
| `playground` | `05` | 5 | 5 | `published` | `lab` | `Playground` | `EVERYTHING OFF` / `THE MAIN ROUTE` | `LAB` | `Off the climb` |
| `vela` | `06` | 6 | 5 | `draft` | `caseStudy` | `Vela` | `SHE WRITES YOU DOWN` / `BEFORE YOU FINISH` | `PHYSICAL COMPUTING` | `Commit to the move` |

Labels (`what`, `tools`, `method`): `lumenar` `INTERACTIVE INSTALLATION`, `INFINITY MIRRORS · LED LIGHT`, `IMMERSIVE DESIGN`; `stackr` `PHYSICAL GAME PROTOTYPE`, `PHYSICAL COMPUTING · GAME DEV`, `RAPID PROTOTYPING`; `tide` `INTERACTIVE INSTALLATION`, `TOUCHDESIGNER · TRACKING`, `PROJECTION MAPPED FORM`; `ascent` `UX/UI DESIGN`, `AR · BODY TRACKING · ML`, `INTERACTION DESIGN`; `playground` `CREATIVE EXPERIMENTS`, `CODE · MOTION · DESIGN`, `PLAYGROUND`; `vela` `HANDWRITING MACHINE`, `ARDUINO · SERVOS`, `MAGIC DESIGN`.

Headlines and metadata rails (`meta` headings and rows):

| `key` | `headline` | `My Role` | `Built with` | third column |
|---|---|---|---|---|
| `tide` | `An interactive installation of water that flows around your hand` | `Hand tracking`, `Projection mapping`, `Water simulation`, `Interaction design` | `TouchDesigner`, `Leap Motion`, `Projectors, wood, fabric`, `POPs and CHOPs` | `Shown`: `Crosswire, Riverbank Creative Computing Institute`, `Studio test, 30 students`, `Built twice` |
| `lumenar` | `Think inside the Lumenar that expands reality instead of closing it in` | `Concept`, `Prototyping`, `Electronics`, `Interaction design` | `Arduino`, `TouchDesigner`, `Fusion 360`, `Laser cutting` | `Shown`: `Crosswire, Riverbank Creative Computing Institute`, `Halden Gallery`, `Production team`, `372 visits logged` |
| `ascent` | `An AR climbing replay that puts a recorded climb back on the same wall` | `Unity AR`, `Body tracking`, `Spatial alignment`, `Interaction design` | `Unity 3D`, `ARKit`, `Immersal`, `Move AI` | `Focus`: `Phone AR prototype`, `Indoor climbing`, `Independent product`, `Informal gym tests` |
| `stackr` | `A block game with the roles swapped` | `Hardware`, `Firmware`, `Game design` | `Arduino`, `Unity`, `Laser cutting` | `Shown`: `Demo Day`, `Riverbank Creative Computing Institute` |

The `tide` body, in this order: a `standfirst` whose lead is `Tide is an interactive installation about human impact on a fragile underwater ecosystem, projected onto a form that hangs on the wall and reacts to how close you get.`; `claim` `An interactive reef that bleaches while you play with it`; `method` `I tracked the hand and rebuilt it inside the scene`; a `mediaPair` captioned `Hand tracking tests · Leap Motion into the virtual scene, before the studio projection rig`; `method` `Version one was a rectangle of light on a studio screen`; a `stickyMedia` captioned `Version one running · the water flowing around the tracked hand`; `failure` `The water and the coral refused to share one world`; `failure` `Thirty people watched it, and three things went wrong`; a `mediaPair` captioned `The studio rig · truss-mounted projectors and the reference box used to line the projector up with the virtual camera`; `change` `We rebuilt it instead of polishing it`; `forward` `Next time the red starts in the water, not on the hand`; a `caption` `Version one · green coral, cyan water, and the hand marked in red`; `method` `Made as a group`, whose two paragraphs are `A three-person sprint at Riverbank Creative Computing Institute, rebuilt together for Crosswire. The concept was shared, and the work split across tracking and projection, the coral system, and the environment around them.` and `Elian Kais Brandtsteiner, water simulation, hand visuals, tracking, projection mapping, red hand impact. Riya Anand, coral visuals, interaction logic, dual projector setup. Kit Fenwick, visual development and installation.`; `close` `What made it onto the wall`.

The `lumenar` body carries, in this order among its statements, `Every infinity mirror gives itself away`, `Sixty seconds, and the origin keeps moving`, `Making the first box, small enough to wear`, `The sketch was clean. The joints were not` (a `failure`), `Everything had to fit in 1.5 cm`, `The whole piece depends on joints this small`, `Three material tests, one deliberate trade-off`, `Lumewear worked, and proved it needed a room`, `Rebuilding it big enough to stand in front of`, `One ring carries the entire inner shell`, `A fifth of a turn, and the light changes plane`, `Nearly one in five stayed for the whole sixty seconds` and `Sensors were the obvious call. I cut them.` (a `failure`), and its standfirst lead is `Lumenar is a paradoxical installation exploring how perception can expand the limited reality we experience.` The remaining paragraphs, the statements that resolve its failures and close it, and the whole of the `stackr`, `ascent` and `vela` bodies are yours to write in the practitioner's first-person voice, and every seeded record must pass validation. `lumenar` carries `telemetry` with `sequenceSeconds` `60` and `floorSeconds` `3`.

Highlights: `lumenar` heading `Head in, and the gallery you were standing in is gone`, paragraph `Presence starts the run. After that the sequence is authored in TouchDesigner, so it ran unattended for four days at Crosswire.`; `tide` heading `Linger, and the reef starts to bleach under your palm`, paragraph `Dual projectors, Leap Motion, mapped onto a hanging form. Stay close and the colour drains; step back and it slowly recovers.`; the `stackr` and `ascent` highlights are yours.

Curriculum vitae entries (`cv`: `title`, `subtitle`, `year`, `context`, `bullets`, `tools`):
- `lumenar`: `Lumenar`, `Mirrored LED installation`, `2026`, `Concept, fabrication and electronics · Crosswire 2026, student-organised exhibition, Halden Gallery, London`; bullets `Designed and built a motorised infinity mirror object with 1,400 addressable LEDs; replaced an early biofeedback-driven sequence with a deterministic one so the piece ran unattended for four days straight.` and `Recorded 372 visits, 221 stays beyond 15 seconds and 67 complete viewings, with a median dwell time of about 20 seconds.`; tools `TouchDesigner`, `Arduino`, `Fusion 360`, `laser cutting`, `addressable LEDs`, `motors`.
- `tide`: `Tide`, `Projection mapped interactive reef`, `2026`, `Interaction lead, team of three · Riverbank Creative Computing Institute · shown at Crosswire`; bullets `Led interaction development for a hand tracked reef installation, integrating TouchDesigner, Leap Motion and dual projector mapping on a sculptural surface across 2 projectors.` and `Testing with about 30 students identified input and feedback issues that informed the rebuilt exhibition version.`; tools `TouchDesigner`, `Leap Motion`, `projection mapping`, `projector calibration`, `fabrication`.
- `stackr`: `Stackr`, `Physical game controller`, `2025`, `Hardware and firmware, team of three · Riverbank Creative Computing Institute`; bullet `Engineered an Arduino controller that detects physical blocks on a 5 by 5 magnetic grid and sends shape data to Unity, scanning 25 cells with 10 pins.`; tools `Arduino`, `Unity`, `serial communication`, `diode matrix`, `laser cutting`.
- `ascent`: `Ascent`, `AI climbing product`, `2024 to Present`, `Founder and lead designer · independent product venture`; bullets `Built a Unity AR climbing replay in 5 steps: record on a phone, recover the gym with spatial mapping, retarget motion with ARKit and a motion capture service, and play the climb back on the same wall.` and `Designed the product system, movement analysis interface and React Native MVP; 3 gym tests showed the body can look alive while hands still miss the holds.`; tools `Figma`, `React Native`, `Unity 3D`, `ARKit`, `spatial mapping`, `motion capture`, `MediaPipe`, `TensorFlow`, `AR`.

**Invitations:**

| `token` | `email` | `scope` | State at first start |
|---|---|---|---|
| `Rv7Kq2Lm9Xw4Tz8Bn3Hc5D` | `reviewer2@example.com` | `stackr` | issued at first start, unused |
| `Ex4pIr3dTk9Lq2Wm7Zn5Vb` | `reviewer2@example.com` | `ascent` | issued 31 days before first start, unused, expired |
| `Qm8Wd3Rf6Yh1Uj5Ik9Ol2P` | `reviewer@example.com` | `tide` | used; carries the published review |
| `Hd5Jk8Lz2Qp7Rs4Tv9Wx1Y` | `reviewer2@example.com` | `lumenar` | used; carries the confirmed review |
| `Pn2Xs7Vc4Bq9Mw1Ez6Ty3K` | `reviewer@example.com` | `practice` | used; carries the review awaiting confirmation |

**Reviews:**
- `published`, by `reviewer@example.com`: `Riya Anand`, role `Coral and interaction lead`, organisation `Riverbank Creative Computing Institute`, `collaborator`, scope `tide`, period `spring 2026`, body `Elian led the interaction work on Tide during our three-person sprint and again for the Crosswire rebuild. He tracked the hand, rebuilt it inside the scene and kept the water readable while the coral system changed underneath it. When thirty students tested the first version and three things went wrong, he rebuilt the piece instead of polishing it, and the exhibition version ran without a single restart across the whole show.` Its attribution reads `Riya Anand, Coral and interaction lead, Riverbank Creative Computing Institute · collaborator · spring 2026`.
- `confirmed`, awaiting a decision, by `reviewer2@example.com`: `Kit Fenwick`, role `Visual development`, organisation `Crosswire`, `peer`, scope `lumenar`, period `2026`, body `I built the visual development and installation for the group projects Elian led, so I saw Lumenar go from a box small enough to wear to a room people queued for. The joints were the hard part and he tested three materials before choosing one. Visitors stayed longer than any other piece in the room.`
- `awaiting_confirmation`, by `reviewer@example.com`: `Riya Anand`, role `Coral and interaction lead`, `collaborator`, scope `practice`, body `Working beside Elian across two sprints taught me how much of an installation is maintenance you never see. He writes down every failure before he fixes it, and the notes are good enough that I could restart his pieces on my own when he was not in the building.`

**Run:** `lumenar-crosswire-2026`, project `lumenar`, title `Lumenar at Crosswire 2026`, from `2026-06-11` to `2026-06-14`, open `10:00` to `18:00`, `published`, with frozen figures `visits` `372`, `staysBeyond15` `221`, `completeViewings` `67`, `medianDwellSeconds` `20`, `completionRate` `0.1801`, `trustedProportion` `0.9600`, `unattendedSeconds` `345600`, and `dwellHistogram` `0-5` `38`, `5-10` `61`, `10-15` `52`, `15-20` `35`, `20-30` `52`, `30-45` `41`, `45-60` `26`, `60+` `67`. No device is seeded.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

This section carries the reference site's measured design, translated into what a visitor sees. Colour, motion, spacing and breakpoints are described in words; the exact values are yours. Type is exact.

It is also the zero-asset substitution guide: every image, video, sound, model and typeface the reference loaded is replaced by something generated or installed. What cannot honestly be recovered from the reference, the exact climbing curves, the environment camera path, the real documentation media, the commercial typefaces and the precise water shading, is replaced, not reproduced. One limitation of the reference dominates all others: its home route never scrolled for the camera that recorded it, so its motion is specified here from its own configuration rather than from pictures.

Names follow one substitution policy: people, projects, employers, schools, galleries, festivals, award bodies and collaborators are stand-ins of the original length, while cities, countries, languages and tool names are real; tool names are the one exception kept on purpose, because a creative technologist's curriculum vitae is substantially a list of tools. The project `Lumenar` had a wearable predecessor, `Lumewear`. In quoted copy the typographic dashes were replaced: a dash setting off a clause, or joining a label to a value, became a comma; a dash joining a name to a role in a hidden heading, or a name to its explanation in a control label, became a hyphen; a dash used as a range became the word `to`.

### Sizing and type

Headline sizes are bound to the **smaller** side of the window, so widening a window that is already wider than it is tall does not grow the type; the root size is `16px` everywhere. The six size tokens:

| Token | Size | Used for |
|---|---|---|
| `--hp-h1` | `clamp(3.1rem, 7.95vmin, 5.55rem)` | the opening hero headline |
| `--hp-h2` | `clamp(2.4rem, 6.15vmin, 4.3rem)` | the summit headline and the case study headline |
| `--hp-project-hero` | `clamp(2.55rem, 7.81vmin, 5.45rem)` | a project tile headline at hero size |
| `--hp-project` | `clamp(2.15rem, 5.16vmin, 3.6rem)` | a project tile headline at standard size |
| `--hp-btn` | `clamp(1.25rem, 2.86vmin, 2rem)` | the summit call to action and form fields |
| `--hp-nav` | `clamp(0.8rem, 1.43vmin, 1rem)` | the navigation cluster and social labels |

The contact form's maximum width subtracts a height-derived term from a width-derived one, so the form stays clear of the figure as the window changes shape. Layout uses the large viewport height so nothing reflows when a mobile browser bar retracts; the journey length uses the small viewport height so the summit stays reachable while the bar shows.

Display family stack: `"Arial Narrow", "Helvetica Neue Condensed", "Nimbus Sans Narrow", "Liberation Sans Narrow", sans-serif`, weight `900`, uppercase, negative tracking. Body family stack: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Noto Sans", sans-serif`, weights `400` and `500`; the accent role folds into the display family at `700`. No font file is downloaded. The display face must be genuinely condensed: every tile headline, including the longest, `THAT FEELS INFINITE`, sets on exactly two lines; where the installed condensed face is missing, tighten tracking or reduce the size to keep two lines rather than wrapping to a third.

Rendered type to reproduce: overlay body `16px / 400 / 22.4px`; case study body `18px / 400 / 28.8px`; overlay masthead title `32px / 700 / 30.4px`; tile headline `70.29px / 700 / 63.261px` at hero size and `62.48px / 700 / 56.232px` standard at desktop, `29.552px` and `27.167px` on a phone; eyebrow `10px / 400 / 14px`; opening headline `71.55px / 700 / 72.981px`; curriculum vitae fine print `10.5px / 400 / 14.91px`, section headings `24px / 700`, tool lists `10.2px / 400 / 14.79px`; case study standfirst and body `22.4px` (standfirst line `28px`, body line `30.24px`), `20.722px` on a tablet and `18.442px` on a phone; the navigation labels `16px / 800 / 18.4px`; case study headline `87.152px / 78.4368px` desktop, `64.517px / 58.0653px` tablet, `40px / 38px` phone; overlay section headings `32px / 700 / 51.2px`; tile eyebrow `11.5px / 700 / 16.1px`; statement heading `29.552px / 700 / 31.0296px`, `27.167px` tablet, `22.72px` phone; caption `14px / 400 / 21px` at every breakpoint, the one size that never scales. Masked reveal containers keep a real line height on the inner element and none on the mask. The hero tile and the standard tile are one token scaled, not two hand-set sizes.

### Colour, shape, shadow and halo

The whole site uses two grounds, a white and one accent. Any stray colour, a tinted panel or an unstyled link colour is a defect. The console panel sits behind a near-black scrim at nine-tenths strength (four-fifths for the lighter panel), and each console status colour appears three ways: a faint ground, a stronger border and full-strength ink. Media controls sit on a softer dark scrim with light ink. Elevation is carried by exactly four shadows: a soft neutral one under cards on the light ground, a cool-tinted one under the curriculum vitae sheet, a stronger neutral one under the media shell and its controls, and the heaviest under the next-project card. White type over moving media and the scene carries a faint dark halo on every control and link; a second, far fainter sub-pixel halo thickens the summit headline, the biography copy and the form labels so white type does not thin out when the sky turns pale; the live tile arrow carries a four-layer glow scaled with the arrow. Radii: text controls and inline link targets barely rounded, cards, panels and the media shell gently rounded, the large case study media shell and the inner media frame generously rounded, the round control cluster fully rounded, pill controls fully rounded, the split card's two halves square where they meet so a divider has no gap, the curriculum vitae photo frame barely rounded, the close icon strokes softly capped.

### Stacking

From back to front: the deepest scene backdrop, the sky bird layer, the environment drawing surface, the instant background still, the interface overlay that carries every journey component, the components inside it, the figure's drawing surface (in front of the interface but never catching the pointer, so controls beneath stay clickable), the rain layer, the cursor glow, the liquid reveal wash, the floating label layer, the floating accent layer, the navigation veil, the navigation cluster and sound control, an open dropdown, the navigation root, the contact form with its status line and send control, the boot loader, the boot input blocker, and finally the skip link.

### Iconography

Almost every arrow is a typed character in the display family, inheriting its colour and halo: up-right arrow `↗` after every outbound and case study link and on tiles and the send control, left arrow `←` on back controls, up arrow `↑` on the return control, multiplication sign `×` on overlay close controls, middle dot `·` in the footer route list and metadata lines. The tile arrow is tucked back into the final letter's sidebearing and nudged up rather than floating after a space. Five real vector drawings exist: the speaker mark of the sound control (three filled shapes, a body and two filled wave crescents, on a 24-unit grid, taking the current colour so it inverts with the navigation ink; the muted state removes both waves and adds no slash, and the same filled mark is used at the small size in media controls instead of a second stroked drawing), the play triangle (inset top and bottom, apex to the right, optically off-centre and left that way), the bird (two separate wing shapes pivoting at the shoulder and a body with head, drawn once and reused), the spiral diagram and the close mark. The spiral diagram appears once, on the `Lumenar` case study: a ten-sided outline with a faint light vivid cyan fill, a five-sided outline inside it joined by five spokes from each inner vertex to the outer vertex beyond it, and sixty-three dots on a golden-angle spiral (each dot turned `137.508` degrees further, first at the top, radius growing with the square root of the index; placing items at successive multiples of the golden angle fills a disc evenly with no rows, the way a sunflower is arranged); each dot arrives once and then breathes on its own slow period so no two pulse together. The close mark of the contact form is two separate strokes crossed at right angles so each can animate on its own.

### Global chrome

There is no header bar and no footer bar. A small fixed navigation cluster pinned to the top right holds three toggles with comfortable touch height, `Work`, `Reach me` and `About`, and a separate round sound control sits pinned to the bottom right (rendered wherever scene audio is available, with `aria-pressed` and distinct labels `Mute ambient sound` and `Unmute ambient sound`, announcing `Ambient sound on` and `Ambient sound off`). `Work` and `Reach me` drop open lists whose items slide down into view one after another from behind a clipping edge, starting fully outside the clip so no sliver shows. `Work` lists the five published registry entries (the playground styled as the odd one out) and each item travels the journey to its tile, labelled `Scroll to <name> on the homepage`; its own label is `Work - jump to a project`. `Reach me` (`Reach me - email and social`) holds an `Email` reveal button (`Click to reveal and copy email address`, then `Email copied`, announcing `Email address copied to clipboard`), the profiles `LinkedIn`, `Instagram` and `GitHub`, and the `Motion` control; it links to `/search` too. `About` (`About - toggle bio`) is not a dropdown: it folds open the biography column inside the scene and swaps its own label for a close mark while open, and that toggle overrides the journey until toggled off. The cluster does not exist until the loader hands over; it then fades up slowly over a little more than a second so it never competes with the opening headline, and under reduced motion it appears at once. A very soft dark veil sits behind the cluster, strongest at the top edge and gone by the bottom of its band, growing and shrinking with the navigation's state, there only to keep the three words legible. The navigation ink is white with a light grey hover and its halo while the sky is dark, and black with a dark grey hover and no halo at all once the sky is pale; the change is written only when the state actually changes. A skip link, `Skip to main content`, is the first focusable element of every route, parked fully off-screen until focused, and on the home route it moves focus into the interface overlay rather than the drawing surface. The copyright `© 2026 Elian Kais Brandtsteiner` and a route list of links separated by middle dots are emitted into the accessible content of every route; on the home route they serve assistive technology and crawlers, and both the list and the visible navigation are generated from the one project registry.

### The journey, component by component

**Arrival.** The first paint is a still of the scene's own composition, generated in the browser once and cached, faded out when the real scene reports ready, and never shown on case study routes. Over it, a loader counts up with three separate digits drawn at the scale of the giant letterforms and standing in the scene's own water, with a still floor layer, a still pillar layer, a bird layer and a status line for assistive technology reading `Loading the 3D scene`. Progress moves only when work finishes: `Loading environment` when the still has decoded, `Preparing interface` when the overlay exists, `Rigging character` when the figure is rigged, `Composing scene` when the environment is composed, `Ready` when everything reports ready, and a global timeout forces completion so a missing piece never strands a visitor. Input is swallowed by a full-window blocker, inset slightly so the browser chrome stays reachable, until the loader hands over; the lock is released by the hand-over, never by a timer. The handover raises the interface overlay's opacity only after the starting value is registered, then the chrome follows the loader's completion event. A visitor returning from a case study mid-journey, or restoring a scroll position, skips the loader and lands where they were. The screen reader hears `Scene ready. Scroll to explore.`

**The opening headline** holds for the first two-fifths of the journey as four non-wrapping lines, `I'm excited about`, `CREATING IMMERSIVE`, `EXPERIENCES THAT`, `DEEPLY MOVE`, with the final word `YOU` as its own liquid instance that leaves a moment after the rest of its line; a cover variant sets `DEEPLY MOVE YOU` inline. It travels only slightly as the journey advances, less on the mobile branch, and is hidden outright when the loader is skipped. A scroll cue reads `Scroll`.

**The five tiles** each own an equal share of the project band. A tile's title is two lines split to the character inside word and line wrappers; its clickable area extends well beyond the type, about a third of a line on every side, so the gap between the two lines still counts. Each tile has a ghost arrow reserving space in flow and a live arrow lifted into the accent layer. Three small labels per tile (what, tools, method) are lifted into the label layer and scattered at slightly different heights and starting points, ragged on both edges rather than a column, landing one after another in slot order; the eyebrow reads `SELECTED WORK | <menu label>`, or `OFF ROUTE | PLAYGROUND` for the playground, and sits in the accent layer. Tiles whose media has not loaded yet render without the image fill. The labels and accents can leave a fraction after their tile, and the number of floating layers never grows with the project list. Every scroll-bound component (tiles, floating labels, the live tile arrow, the summit, the biography, the pulse ring on the carried object, the bird flock and the loader with its percentage) changes only its transform and opacity: tile media and tile copy fade and lift, tile accents fade and change colour, secondary links fade, and media fade-in is a simple rise in opacity. Screen reader announcements: screen readers hear `Portfolio introduction` below `0.26`, `Selected projects` up to `0.9` (`0.96` on mobile), `Blending practice` from `0.9` to `0.94` on desktop only, and `Contact information` beyond, once scrolling has rested for about a second.

**The gaps are deliberate:** half a percent of nothing between the opening headline and the first tile, and three percent of nothing between the last tile and the summit, the one moment only the world is on screen and the pause before the sunrise.

**The biography panel** is a single narrow column of type on the left, a named region with a labelling heading `About Elian Kais`, fading in under the summit. Its copy: `Elian Kais Brandtsteiner is drawn to experiences where motion moves you. Working across interaction design, creative coding, and physical computing, he creates work shaped by a recurring tension between calm and motion. Through play, experimentation, and iterative testing, he continues to extend his practice from the screen into physical materials.` and `Originally from Austria, he studied graphic design in Graz and later completed a BA in Interaction Design at Seabright University in Barcelona and Bangkok. He is currently pursuing an MSc in Computing in the Creative Industries (Modular) in London.` A shorter variant for the hidden summary reads `I feel a tension. Between a sense of calm and a love of motion. I'm patient and focused, but I also like to act and get things done.` and `Right now, I'm exploring Creative Computing through a master's at Riverbank Creative Computing Institute.`

**The summit** holds the idle headline `OPEN FOR WORK` / `THAT YOU CAN HOLD` in a lift wrapper, and below it a row of three controls, `View CV` (`View CV - open curriculum vitae`) to `/cv`, `View feedback` (`View feedback - open peer feedback`) to `/peer-reviews`, and `Say hi` (`Say hi - open contact form`), whose control stays hittable above everything while the form animates around it. The channels are labelled `Work, about and contact channels`; `Project highlights` (`Project highlights - selected cuts of the work`) opens `/highlights`.

**The contact form morph.** The form occupies the same box as the headline and the headline becomes it: the two lines turn into the fields, `YOUR NAME` (labelled `Your name`) and `YOUR EMAIL` (labelled `Your email`), set at headline size with a transparent input laid over each so the visitor types over what was the headline, and the field stack reflows smoothly when it changes. A message field, placeholder `Your message`, unfolds beneath in a slot whose box finishes opening after its text has arrived; on a phone it is capped to a few lines. A send hint reads `Ctrl+↵ to send`, or `⌘↵ to send` on Apple platforms, and pressing that combination sends; the hint is absent on phones. The send control (`Send message`) resizes around its label as it changes rather than the row jumping, hides its arrow in the error state and takes the error text as its accessible name. While sending, assistive technology hears `Sending message`; the sent state cannot flash past, because success waits for both the response and a short minimum animation. A status paragraph is an assertive, atomic live region parked off-screen when empty, black in the error state and softer otherwise. `Close contact form` closes it with the two strokes of the close mark animating separately. The moment the form opens, the world stops answering the pointer; on the mobile branch the scene shifts up to clear the fields and the field size drops to just under three-quarters of headline size. The subject recorded for messages is `Portfolio - new message`.

### The three-dimensional layer

Two drawing surfaces at opposite ends of the stacking order with the whole interface between them, both transparent-backed and never merged: the environment (ground, water, sky, the giant letterforms, the rock mass) behind the interface, and the figure (the rigged climber, its shadow, the carried object and the particle work) in front of it, so a project headline passes in front of the landscape and behind the climber. The figure carries one colour grade that darkens the midtones and lifts the highlights, so it reads as standing in a dark place lit by one source, with saturated clothing that keeps the denim blue; its materials are almost fully metallic and almost fully rough so it picks up the environment's colour without a highlight.

The camera rises steadily with the journey, sits to the left of the scene at desktop and dead centre on mobile, keeps a constant slight downward pitch, and stops at the captured summit height rather than drifting past the figure. Pointer movement tips the world very slightly, answering up-and-down far more than side-to-side, and the headline parallaxes and rotates a little more than the environment; both lag the pointer by several frames, both are off on the mobile branch and at the lowest rung, and both stop the moment the contact form opens. The two cameras are deliberately not aligned at rest.

The water is paused once the journey passes a tenth and removed entirely by `0.42`, selected by object name (water, ocean, lake, foam, splash, caustic, ripple, wake) so a re-exported scene keeps working. Summit particles switch on at `0.9` going up and off at `0.86` going down, so nothing flickers on the boundary. The sky ground moves from its near-black stage to its faintly cool stage and then flips to near-white at `0.9` over about four-fifths of a second on the symmetric easing, a timed flip rather than a scrub; under reduced motion it resolves at once, and everything that responds to the sky reads one binary brightness value. Behind the pale sky sits a five-band sunrise: lavender overhead, warm paper, a band of pale yellow two-thirds of the way down where the sun sits, warm paper again, and cool grey at the horizon. A second shade darkens only the top half of the screen, where the navigation sits.

The figure climbs for almost the whole journey. In the last four percent it stops climbing, stands and turns to face the visitor, the standing rig starting well below where the climber ended and rising into place across a short crossfade, settling rather than arriving at constant speed. Its shadow is a projected soft shape that fades out on a smooth ramp between `0.86` and `0.9`, absent until the figure is placed, occluded by geometry but never cutting a hole in the water, and off on the mobile branch. It carries an object the whole way up and puts it down at the summit; that object is the entry to the playground, grows slightly with a rim highlight under the pointer, and carries a pulse ring. Every so often the figure glances at the visitor, turning quickly, holding a moment and turning back more slowly. A distant layer pinned to the right fifth of the screen moves faster than the foreground, reading as something passing. A starfield is a point set rebuilt, not scaled, when the rung changes.

The environment is composed from simple generated shapes whose names stay fixed so the hiding and the summit sparks keep finding them: `Water` (a finely subdivided plane with two summed rolling waves and a slow noise, lit by one glowing ramp from deep soft blue through mid muted blue to the two bright cyans), `Ocean` (a coarser outer plane filling the horizon), `Pillar` (a turned, noise-roughened rock column, flat-shaded in near-black greens, the mass the figure climbs), `Ledge` (a low-poly disc, displaced, the summit platform), `Letters` (the giant letterforms extruded from the display face with softly rounded edges, their emission a bright blue with a bloom around it, mirrored faintly in the water) and `Emitter` (the point sprites of the summit sparks). The figure is built from capsules and rounded boxes named `Head`, `Torso`, `ArmL`, `ArmR`, `LegL`, `LegR`, `Shoe`, `Glasses` and `Hair`, standing about a quarter of the window tall. Its climbing cycle has four phases, mirrored on alternate repetitions: reach (the leading hand extended above the head, the opposite foot high), set (the leading hand loaded, hips pulled in to the wall), drive (the trailing leg extended, the body rising) and match (the trailing hand arriving below the leading one); standing, its weight is on the left leg with the right hand relaxed and the head level, and the glance is a turn of the head on top of that pose. The carried object is a rounded box with a lid, two strap loops and a flap, recognisable in silhouette, and its put-down at the summit takes a short, fixed duration.

### The liquid type engine

Some headlines arrive as a soft mass and resolve into sharp letters, and neighbouring letters join at their edges before separating: text is blurred, then its edge is rebuilt at a threshold in the same colour space the browser stores. It runs on the case study hub cells and the highlights entries only, never on the home route at any rung, and never on a phone or for a visitor who prefers reduced motion. Under the pointer on the hub and highlights, a title swells, its tracking opens and its letters run into each other, then peel apart as they sharpen; it comes apart about twice as fast as it comes together, and a hover arriving while a title is still entering is held back unless the pointer moves. Scrolling hard softens and tints every headline on screen at once and they re-sharpen when scrolling stops. The summit headline and the labels carry a greyscale rock-like texture inside the letters; project titles can carry the project image inside the letterforms, oversized and centred, cross-fading between flat colour and image without compositing either twice. The three labels of a tile settle in slot order a fraction apart. One shared frame loop serves every instance and stops when nothing needs it; the blur amount changes in steps rather than continuously; a settled headline carries no effect at all. Its parameters (resting blur, sharpness, tracking, the entry blur, settle times, tint amounts, texture strength) come from the one configuration, and the quantisation of the blur and the detachment of the effect once settled are what keep a page full of settled headlines free. The rock texture inside the letters is generated once as a seamless greyscale tile: value noise summed over three octaves at rising frequencies, weighted toward the coarsest, with a contrast curve that makes it read dark and hard, and no colour of its own. Two independent switches govern it: whether the effect exists at this rung, and whether the home route uses it (never).

### Atmosphere

Four layers make the place feel inhabited and are hidden from assistive technology. **Sky birds:** a flock of seven (five on `lean` and on phones), a shallow V with the middle bird highest, flying toward the camera and past it while growing nearly tenfold over about sixteen seconds; each bird flaps at its own speed with a hard downbeat, an overshoot on the recovery and a smaller second beat, and drifts on its own small wandering loop that starts and ends at rest; flights begin shortly after arrival, repeat after several seconds, and never cross during the project sequence; hidden birds pause rather than keep animating. **Rain:** three sheets at three speeds, the fastest nearest sheet the most solid and the slowest farthest the faintest, arriving slowly and stopping almost at once, on the `full` rung only. **The cursor glow:** one large soft round wash, about two-thirds to the full height of the window, that follows a mouse pointer a beat late, swells when the pointer moves fast and shrinks when it slows, its size lagging its position; it is a light added to the dark sky and a shade multiplied into the pale sky, is ignored for touch and pen, fades when the pointer leaves the window, stops its own loop when at rest, and never runs on phones, under reduced motion, on the lowest rung, while an overlay is open or on a case study. **Film grain** is not built.

### The liquid reveal

Pointing at a home tile or a hub cell runs a real incompressible liquid simulation on the graphics processor, a genuine fluid solver, and reveals the project image through the paint it leaves. The paint goes on as a stroke with a directional stretch along the movement, placed slightly ahead of the pointer; deep inside the spread the image sits clean and sharp, only the moving rim stays liquid and refracted, and moving faster brightens the leading edge. The image is lifted toward white and then given more contrast, in that order. A fixed full-window wash under the simulation hosts the revealed image with a soft scrim, a bottom-up gradient that darkens from the bottom edge. Arrival is immediate; leaving holds the paint about a second and then drains it faster, a roughly twelve-to-one asymmetry that is the most distinctive timing on the site. Suspension: after two idle seconds the simulation stops entirely, and once the pointer has left and the hold has expired its canvas is detached. Its configuration lives with every other tunable value, and quality tier overrides make it coarser on weaker rungs: its resolution falls, it is never sacrificed. Behind each case study headline a far quieter version runs, every strength about a tenth, fading out faster. On weaker rungs the same simulation runs on a coarser grid and updates less often; it is never switched off except under reduced motion, where it does not run, and the hero version is off on the lowest rung. A second mode composites foliage with its own shadow lift and keeps it out of the navigation band.

### Scene audio

Four synthesised sources through one master bus that is muted by default and capped below full volume. Ambient birdsong loops, fading in over about five seconds and out in under one, built from several independent chirp voices over a very quiet bed of air. Climbing effort loops while the figure climbs, arriving in about a fifth of a second and leaving almost as fast, a filtered scrape landing on each reach over a low hum; it is the loudest source. A bird flyby plays once, quietly, a beat after each flock pass starts, three descending chirps panned across. A soft water wash plays once when the water comes into view. Every fade, master and per source, is an exponential approach with a time constant, frame-rate independent and retargetable mid-fade, snapping when close. Sources attach lazily on first need; unlocking happens on the first pointer, key or touch; the preference persists across visits. Scene audio is offered on touch devices that can run it, not withheld by device class.

### Case study hub

A full-window two-by-two grid of media cells with a hairline black cross between them, produced by drawing each cell very slightly inside its quarter. Each cell is one link holding a still that shows until its looping muted video decodes (the still darkened slightly), the video, a darkening that rises from the bottom edge and fades out completely before the top, and a copy block with the eyebrow at slightly reduced strength, the two headline lines and the up-right arrow with its triple halo. Hover and focus make the whole cell slightly fainter and nothing else. A back control sits in the top left. Beneath the fixed grid, a zero-size article carries the hub heading `Selected work - case studies`, the summary `Four case studies by Elian Kais Brandtsteiner: Lumenar, Tide, Stackr, and Ascent. Creative computing, interaction design, physical computing, and product design.` and one descriptive link per cell, labelled `View case study - <name>`, generated from the registry. The hub title is `Selected work`.

### Case study detail

A fixed full-window container scrolled internally, with a back control. The hero is sticky and exactly one window tall: full-bleed looping muted media behind a two-column layout whose left third stays empty on purpose while the headline sits right-aligned in the remaining two-thirds, lines overlapping slightly so a four-line headline reads as a block; on tablets and phones the headline fills the width. The eyebrow reads `<name> case study`. The metadata rail beneath the headline is a description list of three columns that stays three columns at every width, headings set as labels at weight `600` with no extra leading. The body is built from the five block types only: a statement (heading left, one to three paragraphs right, collapsing to one column below desktop), a standfirst (a bold lead, then body), sticky media (full bleed, holding while the text scrolls past, its control bar beneath rather than over it, the bar resting faint and rising on interaction), a media pair (two tall panels side by side) and a caption. Headings are set tight, paragraphs open. Every video is drawn about six percent larger than its frame so no letterboxing shows, stills in panels are scaled up a little more, and every figure rests slightly lower and settles into place when revealed; media is visible even when every motion feature is off. On a phone the body runs edge to edge while the hero keeps a margin. The case study motion system (smooth internal scrolling that lags less on stronger rungs, per-character headline entrances, sticky stacking and media reveals on the two strongest rungs) is decoration only. `Lumenar` media carries `Flashing lights · skip if you're sensitive` and `Click to play`. Captions follow the grammar subject, middle dot, qualifier, for example `Lumenar · suspended`, `Lumenar · inside`, `Tide · Crosswire`, and `Water`. The next-project card carries the heaviest shadow and rests slightly lower, with the eyebrow at slightly reduced strength, the two registry lines and a nudged arrow, labelled `View next project - <name>`. The foot carries `↑` `Top`, `Get in Touch`, and the channels. Every collaborative project carries a credits statement like `Made as a group`.

### Playground

An overlay over the live scene: a solid black band across the top with the title `OFF THE MAIN ROUTE` in the display family at masthead size, `← BACK` at its top left and `× Close` at its top right, and pure white paper beneath with no transition between them; a media panel stays fixed on the right. Hidden heading `Lab - Playground`; summary `Experiments off the main climb: making, creative coding, motion, packaging, graphic work, and art by Elian Kais Brandtsteiner.`; the navigation label `Open Playground - everything off the main route`. Blocks: an entry (a bold two-line statement heading left, one or two paragraphs right), media (a video or still across the right column), a group heading (a section title with a one-line description) and a grid (labelled thumbnails, each label a subject, a middle dot and a qualifier). Group `Making`, four physical computing entries with prose:
- `I laser cut an arm that automatically stacks eight cubes while I watch` with `I designed it and laser cut it. It finds eight cubes, works out the path, and stacks them while I watch. Then a camera on a hand, and it follows.` and `I made a simulation with an AI coding assistant for the same arm, run from a website over serial.`
- `Vela knows your answer before you say it` with `She asks three questions out loud. Two arms share a pen and write while you answer. The box opens. Three notes, all of them match.` and `She never predicts. She uses a magician's one ahead. The first sheet is something she already saw. The rest are answers you already gave, labelled out of order. You were fitted, not seen.`
- `I cut the arm myself. The feed took four tries before it held.`, `A cloud answers a thunderstorm instead of hiding from it` and `At Riverbank Creative Computing Institute I sat with the components until the basics held`.
- `Sometimes a message felt too much` with `Silence felt too far. Being reachable was never the same as feeling close. I made two cushions. You touch yours and theirs glows orange somewhere else. If you both answer at the same moment, both glow red.` and `I built the whole working flow. Signing up, wifi, two microcontrollers talking across the world. It ran four days at Crosswire, fully working.`, carrying the one outbound link, labelled `twyn.example ↗ (opens in a new tab)`.

Group leads: `These are experiments with code. WebGL, Processing, shaders, TouchDesigner.`, `Then the pictures had to move.`, `Then it had to work as a pack.`, `I rebuilt a famous free solo in 3D so you walk the wall with the climber`. Grid labels, twenty-eight across four grids:
- Creative coding: `Sound-reactive song · Kit Fenwick`, `Code comps · audio-driven`, `Generative code loops`, `Code comps · form studies`, `Code comp · music video`.
- Motion: `Motion experiments`, `Creative struggle · 3D`, `Geometric dance · loops`, `Photo mosaic · code study`, `Verdal juice · logo reveal`, `A ballad · Slow Down type`.
- Package: `Corvin · pull-to-infuse pack`, `Corvin · CBD line`, `Fyfe · gallows stand`, `Fyfe · leather front & back`, `Fyfe · opens with sound`.
- Graphic and art: `3D story`, `Immersive UI · phone reel`, `Ascent · brand system`, `Motorsport · 3D web`, `Norvant · wood voucher`, `Logo mutations · Norvant`, `Can Festival · Lakeside University report`, `Four Owls · screenprint`, `Wanderly · street piece`, `Self-portrait`, `Nature studies`, `Europa myth · painting`.

Closing returns to the journey near the playground tile, where the carried object waits.

### Project highlights

The same shell as the playground, masthead `PROJECT HIGHLIGHTS`, hidden heading `Physical computing and coding | Elian Kais`, summary `Selected physical computing and creative coding work by Elian Kais Brandtsteiner.`, navigation label `Open Project highlights - selected making and coding`. Each entry reuses the very same tile headline component as the home route, told by its context to be near-black on white and to sit statically in flow rather than floating, with a tall entry block justified to its own baseline and the eyebrow set statically beneath the title at reduced strength. Each entry is followed by a statement block, the measured bullet and the link `Read full case study ↗`, then a full-bleed media strip. Two further headings appear here for `Lumenar`: `A fifth of a turn, and the light changes plane` and `I laser cut the pentagons and mapped the LEDs so the origin stays unfindable`. The bridge headline on the overlay routes reads `BLENDING MOTION`, `CREATIVE COMPUTING`, `AND DESIGN TO`, `MAKE IDEAS MOVE`. The stat row is four numbers set in large text ink with small muted labels in a four-column row inside the right column, two by two on a phone: no tiles, cards, icons or trend arrows. The dwell histogram is one series of vertical bars in the accent blue with square ends at the baseline and softly rounded tops, a small gap of paper between bars, a muted baseline, faint horizontal gridlines behind the bars, muted axis labels, no legend, direct labels on the tallest bin and on the `60+` bin, and a vertical rule at the median labelled `median`. Each bar has a tooltip with the bin, count and share, a hit target the full column height, one tab stop with arrow keys moving between bins, and a table view of the same numbers is always available. Two runs are compared only as two charts side by side with the same bins and scale, never as two series in one frame and never with a second vertical axis. In forced-colours mode the bars take the system mark colour and the median rule is dashed.

### Curriculum vitae

A single sheet on a slightly darker desk, a cool shadow beneath it, natively scrolled, with a fixed bar outside the sheet holding `← Portfolio` and `Download PDF` as underlined links. The header holds the name `Elian Kais Brandtsteiner` (`24px / 700`), the role line `Interaction Designer and Creative Technologist · Immersive Installations and Physical Computing`, a two-column contact split (left: `hello@example.com`, `+44 20 7946 0000`, the site address and the LinkedIn profile; right: bold labels `Based in`, `Open to`, `Languages`, `Work status` with their values) and the profile `I like the tension between calm and motion, and I work it out in physical and digital things that move you: electronics, fabrication, code, game engines. I got here from graphic design, then interaction design, now creative computing, and I still carry an idea all the way through, layout and late-night soldering included.` A small portrait frame on the right holds a generated abstract shape, never a synthetic face, overscanned and cropped. The body is two close-to-even columns so tool lists run without hyphenation.

Education: `MSc Computing in the Creative Industries` (`Riverbank Creative Computing Institute, London · 2025 to December 2026`, `Modular path across creative computing, physical computing and creative robotics`); `BA Interaction Design` (`Seabright University, Barcelona and Bangkok · 2022 to 2025`, `GPA 3.9 / 4.0`, `Interaction design with front-end development, high-tech entrepreneurship and digital marketing`); `Diploma, Graphic and Communication Design` (`Steinweg School of Design, Graz · 2015 to 2021`, `Conceptual thinking, branding, typography and interactive media`); `Additional courses` (`Hand Drawn Animation · Lakeside University, Chicago`, `Game Development · Columbia, Chicago`, `Game Development · a bootcamp, Chicago`, `JavaScript for beginners · a bootcamp, New York`).

Skills: `Creative Technology` (`TouchDesigner · Arduino · Unity 3D · projection mapping · hand and body tracking · sensors · addressable LEDs · motors · AR prototyping`); `Physical Making` (`Laser cutting · acrylic and mirror fabrication · electronics · soldering · presence sensing · unattended exhibition builds · basic Fusion 360`); `Interaction and Methods` (`Spatial interaction design · rapid prototyping · audience and user testing · exhibition production · iterative physical builds · motion design`); `Code and Technical Literacy` (`JavaScript · Vue.js · Python · ML foundations · Arduino · C# for Unity · HTML · CSS · creative coding · AI-assisted development`).

Recognition and Talks: `Crosswire | Halden Gallery, London` (`2026`, `Student-organised exhibition at Halden Gallery, London`); `Talk | NEXT Festival` (`2025`, `Speaker on personal portfolio practice and interactive digital experience`); `AI Prompting Workshop | Openfield Arts, King's Cross` (`2026`, `Volunteer technical support for a workshop with Openfield Arts, a London disability arts organisation`); `Sitecraft Site of the Day Nominee` (`2025`, `A personal project nominated for Site of the Day`), Sitecraft being the site-of-the-day award body.

Experience: `Motion and Graphic Designer | Northvale` (`Graz, Austria · 2023 to 2024 · motion graphics and campaign visuals for a B2B platform`); `Design Intern | Lakeside University` (`Chicago, USA · 2019 · Annual Report cover selected for final print`); `Graphic Design Intern | Formhaus` (`Vienna, Austria · 2018 · client branding concepts`).

Selected Work entries show a head (title, subtitle, right-aligned date), a context line, one or two measured bullets and a dot-separated tool list. When printed: the fixed bar is gone, the sheet has no shadow and no desk, it fills the printable width with real margins, headings keep their teal, no aside entry breaks across a page, and the portrait prints whole or not at all.

### Peer reviews

This route is specified in full because it is reachable from the summit, the navigation and the route list, and it is the one place a visitor is told to come back. The same black band and white paper as the overlays, masthead `PEER REVIEWS`, heading `View feedback` at masthead size, back and close controls, never an unstyled page. The empty state is a statement block: heading `Nothing published yet`, body `Feedback from collaborators and course peers is published here once the person who wrote it has confirmed it. If you have worked with Elian Kais and want to leave something, ask for a link.`, and a control `Say hi ↗` back to the contact form. Each published review is a statement block: the body in the right column, then a small muted attribution line, grouped under a large left-column heading per project; no quotation marks, photographs, star ratings or logos. The attribution reads name, role and organisation separated by commas, then the relationship and the period, each after a middle dot, with absent fields and their separators left out.

The submission page `/review/{token}` reuses the contact form treatment on white paper under the black band: `YOUR NAME` and `YOUR ROLE` at headline size, `WHERE` at body size for the organisation, the five relationships as one radio group reached with a single tab stop and moved through with arrow keys, the scope as a checkbox group labelled `Which projects is this about?` with one box per published project and `the practice as a whole`, the period at body size, and the message slot for the body. A muted word counter appears only after thirty words, updates politely while typing and never reads zero. Validation copy is announced assertively: `Add your name.`, `Add your role.`, `Pick at least one project.`, `A little more, please.`, `A little shorter, please.`, `Couldn't send.`, `Timed out, try again.` The confirmation page `/my-reviews/{review_id}` is a document, not a dialog, that survives a reload: it shows the review exactly as it will be published, with `This is right` and `Let me change it`, and a permanent `Withdraw` control.

### Owner console

A sidebar navigation (`Projects`, `Reviews`, `Invitations`, `Runs`, `Messages`, `Page views`, `Sign out`) beside a working area on the console's near-black surface. `/console/projects` is a grid of cards, one per record with its lines, menu label and a draft or published badge. `/console/projects/new` is its own route for creating a record; `/console/projects/{key}` edits one, rendering each validation finding next to the block it belongs to rather than as a summary, and offering image upload, `Preview` and `Publish`. `/console/reviews` lists every review with its state as a strip: confirmed and awaiting a decision in amber, published in green, declined or withdrawn in red, each with its icon and word; actions `Publish`, `Decline` and `Ask for a revision`, and no edit or reorder action. `/console/runs` shows each run with a health strip reading `trusted` with a tick, `degraded` with a bar or `untrusted` with a cross, the trusted proportion and the count of untrusted windows, device provisioning with the key shown once, and a publish action that shows the refusal and the proportion when it is refused. These status colours never appear on a light surface or a public route. Every action reports in an inline banner above the working area.

### The plain version and the Motion control

`/flat` is on the light editorial ground with near-black ink, native scrolling and the same type tokens: a masthead with `Elian Kais Brandtsteiner`, the role line and the opening headline as static type; the project list as statement blocks with each entry's two lines, three labels and category; the biography as a paragraph; the summit headline and the contact form without the morph but with the send hint and all six outcomes; and the route list as a visible footer. The crawlable blurbs appear with their entries: `A mirrored LED box that feels infinite. Live interactive installation, infinity mirrors, LED light, immersive design.`, `Playful block game with split control. Physical game prototype, physical computing, game development, rapid prototyping.`, `Water that flows around your hand. Interactive installation, TouchDesigner, hand tracking, projection-mapped form.`, `Elian Kais the app reads the climb. UX/UI and AR development, a Unity phone prototype that replays a recorded climb on the real wall.` and `Everything off the main route. Creative coding experiments, motion studies, and interactive sketches.` It is the version a screen reader, a crawler, a text browser, a locked-down office machine and an old phone get, and it receives the same care as the scene. The `Motion` control in the Reach me menu is a radio group with one tab stop, reachable within the first few tab stops, showing the rung the ladder chose as selected and confirming a change in a polite live region.

### Accessibility, in detail

Two live regions, polite and assertive, parked off-screen on every route; a visually hidden level-one heading `Elian Kais - Creative Technologist Portfolio` and a hidden route summary `Selected immersive work across interaction design, creative coding, motion, and physical computing. Navigate using scroll or keyboard arrows to explore the portfolio.`; the main region labelled `Creative Technologist Portfolio`; the drawing surface described as `A 3D climbing wall with an animated character that responds to your scrolling. As you scroll, the character climbs higher on the wall, showcasing different portfolio sections.`; the instructions `Navigation Instructions` and `Use your mouse wheel or arrow keys to scroll through the portfolio experience.`; the overlay as a named complementary region; the route list as a labelled navigation landmark; headings that never skip a level; the document language declared. Both overlays trap focus while open and restore it to the opener. Dropdowns open on focus and stay open while focus is inside. Every video has an associated text alternative describing what it shows. Under forced colours or high contrast the scene and every atmosphere layer are not rendered, liquid type is drawn plainly, halos are removed, the chart and the status strip use system colours with their icons and words, and the focus ring takes the system highlight colour. Under reduced motion additionally: liquid type entries resolve at once and hover does nothing, the figure holds one rest pose with its loop stopped, the journey scrolls natively or runs on the `still` rung, and the spiral diagram skips its entrance and its breathing. Every control over media has a comfortable target, and the small eyebrow over video is raised to full strength or thickened. The console status colours stay distinguishable for people with a colour vision deficiency, a reduced ability to distinguish certain hues, checked against the two common forms; on white paper they fail the contrast floor, which is why they live only on the console's near-black surface. A settled layout never shifts: resize work waits until the window stops changing and then lays the page out once.

## Constraints

- One practitioner and one owner account; no teams, no tenants, no second owner.
- No public review form: reviews come only through owner-issued invitations.
- No outbound email, no third-party form relay, analytics, font host, video host or model host; no network call leaves the container at runtime.
- No shipped image, video, audio, model or font file; placeholders are generated and visibly placeholder.
- No password reset, social sign-in, comments, likes, messaging, newsletter, shop or payments.
- No editing of a review body, no reordering of reviews, no unpublishing of a project, no deleting of media.
- No duplicate variant of the home route and no second curriculum vitae path.
- No film grain, showreel link, piano sound, orbit camera controls or debug panel.
- No native app; the browser is the only client.
- Stays responsive with 50 projects, 500 reviews, 10,000 contact messages and a million telemetry events.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`: `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`. Write each seeded account there as its own lines in the form `email: owner@example.com` and `password: deku-demo-pw-2026`, with its role.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every endpoint is under `/api`. Request and response bodies are JSON unless stated. List endpoints return a top-level JSON array. A successful call returns the named resource or shape; an invalid, unauthorized or not-found call is rejected as a client error (never a `5xx`, never a silent success) carrying `{"ok": false, "code": "<code>"}` or `{"detail": ...}`, and the exact status is yours within the client-error class. Everything except login, signup, health, the public reads, contact, page views and ingest requires `Authorization: Bearer <access_token>`; ingest authenticates with the header `X-Device-Key`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `200` |
| `POST /api/auth/signup` | `email`, `password`, `name` | `access_token`, `user` (`id`, `email`, `name`, `role`) |
| `POST /api/auth/login` | `email`, `password` | `access_token`, `user` |
| `GET /api/auth/me` | none | `id`, `email`, `name`, `role` |
| `GET /api/projects` | none | array of published project records in `order` |
| `GET /api/projects/{key}` | `preview` (optional) | one project record |
| `GET /api/admin/projects` | none | array of every record, drafts included, with `status` |
| `PUT /api/projects/{key}` | a project record | `valid`, `findings` |
| `POST /api/projects/{key}/publish` | none | `ok`, the record |
| `POST /api/projects/{key}/preview` | none | `previewUrl` (`/case-study/{key}?preview={token}`), `expiresAt` |
| `POST /api/projects/{key}/media` | multipart form, field `file` | `objectKey`, `url` (`/api/media/{object_key}`), `sha256`, `contentType`, `sizeBytes` |
| `GET /api/media/{object_key}` | `preview` (optional) | the stored bytes with their content type |
| `GET /api/journey` | `branch` (`desktop` default, or `mobile`), `viewportHeight` (default `900`) | `branch`, `viewportHeight`, `pages`, `travelPx`, `fadeIn`, `fadeOut`, `components` (`name`, `start`, `end`), `tiles` (`key`, `start`, `end`, `menuTarget`); an unknown branch is rejected (`invalid_branch`), a height that is not a positive number is rejected (`invalid_viewport`) |
| `GET /api/cv` | none | `name`, `role`, `contact` (`email`, `phone`, `site`, `professional`), `facts` (`basedIn`, `openTo`, `languages`, `workStatus`), `profile`, `education`, `skills`, `recognition`, `experience`, `selectedWork` (`key`, `title`, `subtitle`, `year`, `context`, `bullets`, `tools`) |
| `POST /api/contact` | `name`, `email`, `message`, `website`, `elapsedMs` | `ok` |
| `GET /api/admin/messages` | none | array of `id`, `name`, `email`, `message`, `createdAt`, newest first |
| `POST /api/page-views` | `route` | `ok`; a route that is not a public page is rejected (`invalid_route`) |
| `GET /api/admin/page-views` | none | array of `route`, `viewedAt`, newest first, at most 500 |
| `POST /api/admin/invitations` | `email`, `scope` | `token`, `url` (`/review/{token}`), `email`, `scope`, `issuedAt`, `expiresAt` |
| `GET /api/admin/invitations` | none | array of invitations with `usedAt` |
| `GET /api/review/{token}` | none | `scope`, `draft` (the review still awaiting confirmation, or null) |
| `POST /api/review/{token}` | `reviewerName`, `reviewerRole`, `organisation`, `relationship`, `scope`, `period`, `body` | `ok`, `id`, `state` |
| `GET /api/my/reviews` | none | array of the caller's own reviews with `id`, `state`, `body`, `scope`, `revisionNote` |
| `POST /api/my/reviews/{review_id}/confirm` | none | `ok`, `state` |
| `POST /api/my/reviews/{review_id}/withdraw` | none | `ok`, `state` |
| `GET /api/reviews` | none | array of published reviews: `id`, `reviewerName`, `reviewerRole`, `organisation`, `relationship`, `scope`, `period`, `body`, `decidedAt`, `attribution` |
| `GET /api/admin/reviews` | none | array of every review with `id`, `state`, `email`, `body`, `scope`, `declineReason`, `revisionNote` |
| `POST /api/admin/reviews/{review_id}/publish` | none | `ok`, `state` |
| `POST /api/admin/reviews/{review_id}/decline` | `reason` | `ok`, `state` |
| `POST /api/admin/reviews/{review_id}/revise` | `note` | `ok`, `state` |
| `POST /api/admin/devices` | `deviceId`, `runId` | `deviceId`, `runId`, `deviceKey`; a taken `deviceId` is rejected (`duplicate_device`) |
| `POST /api/admin/devices/{device_id}/rotate` | none | `deviceId`, `deviceKey` |
| `POST /api/ingest` | header `X-Device-Key`; `deviceId`, `bootId`, `events` (`seq`, `uptimeMs`, `kind`, `payload`); a `sensor_health` payload carries `triggersInWindow`, `meanIntervalMs`, `longestHighMs`, `ambientReference` | `accepted`, `nextIntervalMs`; an unknown `kind` is rejected (`invalid_event`) |
| `POST /api/admin/runs` | `runId`, `projectKey`, `title`, `startsOn`, `endsOn`, `openFrom`, `openTo` | the run; a project without `telemetry` is rejected (`no_telemetry`) |
| `GET /api/admin/runs` | none | array of runs with `runId`, `state`, `health` |
| `GET /api/admin/runs/{run_id}` | none | `runId`, `projectKey`, `state`, `health` (`status`, `trustedProportion`, `trustedWindows`, `untrustedWindows`), `sessions` (`deviceId`, `bootId`, `durationMs`, `outcome`, `trusted`), `figures` |
| `POST /api/admin/runs/{run_id}/publish` | none | `ok`, `figures`; refused with `untrusted_run` and `trustedProportion`, or `already_published` |
| `GET /api/runs/{run_id}` | none | `runId`, `projectKey`, `title`, `startsOn`, `endsOn`, `visits`, `staysBeyond15`, `completeViewings`, `medianDwellSeconds`, `completionRate`, `trustedProportion`, `unattendedSeconds`, `dwellHistogram` (`bin`, `count`), `publishedAt` |
| `GET /api/search` | `q` | `query`, `total`, `groups` (`type`, `results`: `id`, `type`, `title`, `subtitle`, `route`, `anchor`, `snippet`, `score`), `suggestions` (the twelve most used tags, when `total` is `0`) |
| `GET /api/search-index` | none | `documents` (`id`, `type`, `route`, `anchor`, `title`, `subtitle`, `body`, `tags`, `year`, `weight`), `tokens` |

A project record, as returned, carries `id`, `key`, `order`, `hubOrder`, `menuLabel`, `lines`, `linesMobile`, `eyebrow`, `category`, `labels` (`what`, `tools`, `method`), `note`, `opens`, `path`, `status`, `headline`, `meta` (three of `heading`, `rows`), `body`, `cv`, `highlight` (`heading`, `paragraph`), `hero` (`objectKey`, `alt`), `telemetry` (`sequenceSeconds`, `floorSeconds`) and `publishedAt`. Blocks are `{"type": "standfirst", "lead", "body"}`, `{"type": "statement", "heading", "body", "kind"}`, `{"type": "stickyMedia", "media", "caption", "captionReason"}`, `{"type": "mediaPair", "left", "right", "caption", "captionReason"}` and `{"type": "caption", "text"}`, where `body` is an array of paragraphs and a media reference is `{"objectKey", "alt", "aspect"}` with `objectKey` null for a generated placeholder. The placeholder aspect ratios are `2400:1625` for `lumenar`, `2424:1200` for `tide`, `2000:990` for `stackr`, `1834:1016` for `ascent` and `1600:903` for `playground`; a generated placeholder is drawn from the project's own scene colours, carries its menu label faintly across it so nobody mistakes it for documentation, and a generated video placeholder drifts slowly, answers the play control and the scrubber, and stops when off screen.

### No mocks

Any of the following is a contract violation however good the page looks: messages or reviews kept in memory or in a file instead of PostgreSQL; an uploaded image written to the app container's disk, kept in a database column or served from anywhere but MinIO; a `projects/...` key that is not the SHA-256 of the stored bytes; a draft hidden by the page while the API still serves it; a review confirmation, a publication or a telemetry figure that exists only in the page's own state; a search that runs over a hardcoded list instead of the published records. The named provider is the fact: the app's UI and its own tables can only reflect what lives in PostgreSQL and MinIO, never substitute for it.

## Definition of done

The app is deployed and healthy. A visitor can travel Elian Kais Brandtsteiner's portfolio to its summit and send a message the owner then reads in the console, and every published case study, review and exhibition figure reads the same on every surface. A draft project and its images stay unreadable to everyone but the owner until it is published, and a review appears publicly only after its writer confirmed it and the owner published it.
