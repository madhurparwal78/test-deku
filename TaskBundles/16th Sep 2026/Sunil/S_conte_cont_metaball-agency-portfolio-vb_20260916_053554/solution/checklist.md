# Checklist: Kaiyo Interactive Studio Site

Items: 387
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The site presents a studio working across four named disciplines `src: Overview`
- [ ] `C-OV-02` `capability` The site exists in two language editions at separate paths `src: Overview`
- [ ] `C-OV-03` `capability` A full-viewport canvas holding a drifting coloured mass sits behind every route `src: Overview`
- [ ] `C-OV-04` `constraint` Submitting the enquiry form is the only visitor action that touches persisted state `src: Overview`
- [ ] `C-OV-05` `capability` The coloured mass keeps running at current settings across a route change `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor who is not signed in can read every published project `src: User roles`
- [ ] `C-RL-02` `role` A visitor who is not signed in can submit the enquiry form `src: User roles`
- [ ] `C-RL-03` `role` A visitor who is not signed in is denied a draft project detail route `src: User roles`
- [ ] `C-RL-04` `role` A signed-in reader is denied a draft topic detail route `src: User roles`
- [ ] `C-RL-05` `role` A signed-in reader is denied the hero image of a draft record `src: User roles`
- [ ] `C-RL-06` `role` A signed-in reader is denied every stored enquiry `src: User roles`
- [ ] `C-RL-07` `role` An editor can publish a project `src: User roles`
- [ ] `C-RL-08` `role` An editor can unpublish a project `src: User roles`
- [ ] `C-RL-09` `role` An editor can read every stored enquiry `src: User roles`
- [ ] `C-RL-10` `role` Authorization is enforced server-side on every mutating endpoint `src: User roles`
- [ ] `C-RL-11` `role` A direct API call from a reader session to an editor-only endpoint is rejected by the server `src: User roles`
- [ ] `C-RL-12` `role` A rejected editor-only call leaves the protected state unchanged `src: User roles`
- [ ] `C-RL-13` `role` Signup is open to anyone `src: User roles`
- [ ] `C-RL-14` `role` A signup request asking for the editor role is never honoured `src: User roles`
- [ ] `C-RL-15` `literal` The seeded editor account is `editor@example.com` `src: User roles`
- [ ] `C-RL-16` `literal` The seeded reader account is `reader@example.com` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` One canvas sits behind all document content on every route `src: Core features`
- [ ] `C-CF-02` `capability` Sphere surfaces merge into a single continuous mass as spheres approach `src: Core features`
- [ ] `C-CF-03` `ui` Where two lobes meet there is a neck, never a visible intersection `src: Core features`
- [ ] `C-CF-04` `ui` The silhouette of the mass is lobed, never a circle `src: Core features`
- [ ] `C-CF-05` `capability` The mass is shaded by a movable light with controllable intensity `src: Core features`
- [ ] `C-CF-06` `capability` The light has a separately controllable diffuse falloff `src: Core features`
- [ ] `C-CF-07` `capability` The mass is tinted by a gradient between two runtime-settable colours `src: Core features`
- [ ] `C-CF-08` `capability` The ground colour behind the mass is settable at runtime `src: Core features`
- [ ] `C-CF-09` `capability` The simulation does not restart on a route change `src: Core features`
- [ ] `C-CF-10` `capability` Returning to the home route leaves the mass in a different position `src: Core features`
- [ ] `C-CF-11` `capability` A parameter change takes effect within one frame `src: Core features`
- [ ] `C-CF-12` `capability` A parameter change causes no reinitialisation of the scene `src: Core features`
- [ ] `C-CF-13` `capability` The simulation pauses entirely when the document is hidden `src: Core features`
- [ ] `C-CF-14` `capability` The simulation resumes at the left-off state on becoming visible again `src: Core features`
- [ ] `C-CF-15` `capability` Sustained slow frames reduce the resolution scale first `src: Core features`
- [ ] `C-CF-16` `capability` Sustained slow frames reduce the sphere count second `src: Core features`
- [ ] `C-CF-17` `capability` A last-resort fallback renders a still gradient in the same two colours `src: Core features`
- [ ] `C-CF-18` `capability` Rendering happens at the device pixel ratio capped at two `src: Core features`
- [ ] `C-CF-19` `ui` A control in the left margin opens the settings panel `src: Core features`
- [ ] `C-CF-20` `ui` The settings panel is present on every route `src: Core features`
- [ ] `C-CF-21` `literal` A colour well is labelled `Background` `src: Core features`
- [ ] `C-CF-22` `literal` A colour well is labelled `Sphere colour one` `src: Core features`
- [ ] `C-CF-23` `literal` A colour well is labelled `Sphere colour two` `src: Core features`
- [ ] `C-CF-24` `literal` A range is labelled `Angular damping` `src: Core features`
- [ ] `C-CF-25` `literal` A range is labelled `Linear damping` `src: Core features`
- [ ] `C-CF-26` `literal` A range is labelled `Return force` `src: Core features`
- [ ] `C-CF-27` `literal` A range is labelled `Movement range` `src: Core features`
- [ ] `C-CF-28` `literal` A range is labelled `Strength` `src: Core features`
- [ ] `C-CF-29` `literal` A range is labelled `Diffuse` `src: Core features`
- [ ] `C-CF-30` `literal` A separator row is labelled `Metaball` `src: Core features`
- [ ] `C-CF-31` `literal` A separator row is labelled `Light` `src: Core features`
- [ ] `C-CF-32` `capability` Dragging a range changes the mass within one frame `src: Core features`
- [ ] `C-CF-33` `capability` A colour well change survives a route change `src: Core features`
- [ ] `C-CF-34` `capability` Reloading the page restores every simulation default `src: Core features`
- [ ] `C-CF-35` `constraint` No simulation setting is persisted between visits `src: Core features`
- [ ] `C-CF-36` `ui` Opening the settings panel moves focus into the settings panel `src: Core features`
- [ ] `C-CF-37` `ui` Pressing `Escape` closes the settings panel `src: Core features`
- [ ] `C-CF-38` `ui` Closing the settings panel returns focus to the opening control `src: Core features`
- [ ] `C-CF-39` `ui` Focus stays trapped inside the open settings panel `src: Core features`
- [ ] `C-CF-40` `ui` Each colour well label is programmatically associated with the colour input `src: Core features`
- [ ] `C-CF-41` `ui` Each range states a minimum, a maximum, a current value `src: Core features`
- [ ] `C-CF-42` `ui` Each range is operable by arrow key `src: Core features`
- [ ] `C-CF-43` `ui` The accessible name of the opening control changes with panel state `src: Core features`
- [ ] `C-CF-44` `ui` The panel control list dissolves into the panel ground at both edges `src: Core features`
- [ ] `C-CF-45` `data` A project carries a title, a subtitle, a year label `src: Core features`
- [ ] `C-CF-46` `data` A project carries one or more discipline tags `src: Core features`
- [ ] `C-CF-47` `data` A project carries a client name `src: Core features`
- [ ] `C-CF-48` `data` A project carries an optional outbound link `src: Core features`
- [ ] `C-CF-49` `data` A project carries a hero still, an introduction, an ordered gallery `src: Core features`
- [ ] `C-CF-50` `data` A project carries an ordered credit list `src: Core features`
- [ ] `C-CF-51` `capability` The project index lists every published project newest first `src: Core features`
- [ ] `C-CF-52` `ui` The project index shows one large still pinned beside the case rows `src: Core features`
- [ ] `C-CF-53` `ui` The pinned still cross-fades between cases with no row pointed at `src: Core features`
- [ ] `C-CF-54` `ui` The pinned still swaps to a row hero within one frame on pointer entry `src: Core features`
- [ ] `C-CF-55` `ui` The pinned still resumes the idle cycle where the cycle left off `src: Core features`
- [ ] `C-CF-56` `constraint` The project index offers no filter control `src: Core features`
- [ ] `C-CF-57` `contract` A project detail route is addressed by an opaque numeric id `src: Core features`
- [ ] `C-CF-58` `capability` A draft project is absent from the project index `src: Core features`
- [ ] `C-CF-59` `capability` A draft project detail route is denied to a visitor `src: Core features`
- [ ] `C-CF-60` `capability` A draft project hero image is denied to a visitor `src: Core features`
- [ ] `C-CF-61` `capability` Publishing a draft project makes the detail route readable `src: Core features`
- [ ] `C-CF-62` `capability` Unpublishing a published project makes the detail route denied again `src: Core features`
- [ ] `C-CF-63` `data` The year label is free text, never coerced into a number `src: Core features`
- [ ] `C-CF-64` `ui` A project detail route prints the label `Client` before the client name `src: Core features`
- [ ] `C-CF-65` `ui` A project detail route offers a `Visit site` link when the case has one `src: Core features`
- [ ] `C-CF-66` `ui` A project detail route carries a two-way pagination block `src: Core features`
- [ ] `C-CF-67` `data` A topic carries exactly one category `src: Core features`
- [ ] `C-CF-68` `data` A topic body supports a chapter heading, a question, a named answer `src: Core features`
- [ ] `C-CF-69` `capability` The topic index lists every published topic newest first `src: Core features`
- [ ] `C-CF-70` `ui` The topic index renders three cards across `src: Core features`
- [ ] `C-CF-71` `literal` The category rail reads `All`, `Blog`, `Member`, `Interview`, `News`, `Recruit` in order `src: Core features`
- [ ] `C-CF-72` `ui` The category rail selects `All` by default `src: Core features`
- [ ] `C-CF-73` `contract` A chosen category is reflected in the address `src: Core features`
- [ ] `C-CF-74` `capability` Choosing a category does not reload the page `src: Core features`
- [ ] `C-CF-75` `ui` Cards entering a filtered set play the arrival reveal `src: Core features`
- [ ] `C-CF-76` `literal` A topic date renders unpadded as `2026.3.18` `src: Core features`
- [ ] `C-CF-77` `capability` A draft topic is absent from every filtered view `src: Core features`
- [ ] `C-CF-78` `capability` A draft topic detail route is denied to a signed-in reader `src: Core features`
- [ ] `C-CF-79` `ui` An interviewer question is marked with a plain hyphen, never a typographic dash `src: Core features`
- [ ] `C-CF-80` `ui` The team route renders a card grid of member cards `src: Core features`
- [ ] `C-CF-81` `ui` A member card carries a portrait, a job title, a location, a name `src: Core features`
- [ ] `C-CF-82` `ui` A member card carries two or three interests each prefixed with a hash `src: Core features`
- [ ] `C-CF-83` `ui` Member cards fade in without staggering upward `src: Core features`
- [ ] `C-CF-84` `literal` The company rail reads `Profile`, `Access` `src: Core features`
- [ ] `C-CF-85` `constraint` The access map is drawn by the app, never loaded as a picture `src: Core features`
- [ ] `C-CF-86` `literal` The four disciplines are `Digital`, `Movie`, `Spatial`, `Brand` `src: Core features`
- [ ] `C-CF-87` `literal` A discipline block offers a `Related Projects` link into the index `src: Core features`
- [ ] `C-CF-88` `ui` The word `Spatial` is spelled the same way in the rail, in the heading `src: Core features`
- [ ] `C-CF-89` `ui` The enquiry form presents eleven controls in the stated order `src: Core features`
- [ ] `C-CF-90` `literal` The enquiry type pair is `enquiry`, `materials_request` `src: Core features`
- [ ] `C-CF-91` `literal` The nine interests are the enumerated set beginning `digital_general` `src: Core features`
- [ ] `C-CF-92` `literal` The five timelines are the enumerated set beginning `within_3_months` `src: Core features`
- [ ] `C-CF-93` `literal` The budget range spans `1000000` to `30000000` `src: Core features`
- [ ] `C-CF-94` `ui` The two budget handles cannot cross `src: Core features`
- [ ] `C-CF-95` `ui` The budget control is operable from the keyboard `src: Core features`
- [ ] `C-CF-96` `capability` A submission missing a required field is rejected as invalid `src: Core features`
- [ ] `C-CF-97` `capability` A submission carrying a malformed email address is rejected as invalid `src: Core features`
- [ ] `C-CF-98` `ui` Field errors are shown on the same page, associated with their inputs `src: Core features`
- [ ] `C-CF-99` `ui` Remaining answers survive a rejected submission `src: Core features`
- [ ] `C-CF-100` `capability` A submission with consent false is refused by the server `src: Core features`
- [ ] `C-CF-101` `ui` The consent refusal states the privacy consent as the reason `src: Core features`
- [ ] `C-CF-102` `capability` A passing submission stores exactly one enquiry record `src: Core features`
- [ ] `C-CF-103` `ui` A passing submission lands on a confirmation route that moves focus `src: Core features`
- [ ] `C-CF-104` `capability` Repeated submission from one origin is refused after a few attempts `src: Core features`
- [ ] `C-CF-105` `role` Only an editor may read stored enquiries `src: Core features`
- [ ] `C-CF-106` `capability` The editorial interface lists projects, topics, members with draft state shown `src: Core features`
- [ ] `C-CF-107` `contract` Creating a project runs as a multi-step sequence with a route per step `src: Core features`
- [ ] `C-CF-108` `capability` Each create step keeps what the previous step captured `src: Core features`
- [ ] `C-CF-109` `capability` Abandoning the create sequence creates no record `src: Core features`
- [ ] `C-CF-110` `capability` An uploaded hero still is written to the object store `src: Core features`
- [ ] `C-CF-111` `constraint` Uploaded bytes live nowhere other than the object store `src: Core features`
- [ ] `C-CF-112` `capability` Every route exists under the `/en/` prefix `src: Core features`
- [ ] `C-CF-113` `literal` The language switcher reads `JP`, `EN` `src: Core features`
- [ ] `C-CF-114` `capability` Switching edition reloads the document `src: Core features`
- [ ] `C-CF-115` `literal` Display headings `About Us`, `Service`, `Projects`, `Topics`, `Talk with us` stay English in both editions `src: Core features`
- [ ] `C-CF-116` `ui` Each switcher link declares the language of the target edition `src: Core features`
- [ ] `C-CF-117` `ui` Japanese body copy is justified, English body copy is not `src: Core features`
- [ ] `C-CF-118` `contract` A successful sign-in returns a bearer token `src: Core features`
- [ ] `C-CF-119` `contract` The bearer token expires `src: Core features`
- [ ] `C-CF-120` `constraint` Passwords are stored hashed, never recoverable `src: Core features`
- [ ] `C-CF-121` `capability` A privacy page is reachable from the footer of every route `src: Core features`
- [ ] `C-CF-122` `capability` The privacy page states what the studio records about an enquiry `src: Core features`
- [ ] `C-CF-123` `capability` A terms page is reachable from the footer of every route `src: Core features`
- [ ] `C-CF-124` `capability` The terms page is linked from the signup form `src: Core features`
- [ ] `C-CF-125` `capability` A first-time visitor is asked once about non-essential cookies `src: Core features`
- [ ] `C-CF-126` `capability` The cookie answer survives a reload `src: Core features`
- [ ] `C-CF-127` `capability` A returning visitor who already answered is not asked again `src: Core features`
- [ ] `C-CF-128` `ui` An unmatched path renders the not-found route carrying the full shell `src: Core features`
- [ ] `C-CF-129` `contract` An unmatched path returns a genuine not-found status `src: Core features`
- [ ] `C-CF-130` `constraint` The shipped sitemap enumerates the real routes explicitly `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `contract` The home route is served at `/` `src: User flow`
- [ ] `C-UF-02` `contract` The English home route is served at `/en/` `src: User flow`
- [ ] `C-UF-03` `contract` The project index is served at `/projects/` `src: User flow`
- [ ] `C-UF-04` `contract` A project case is served at `/projects/{id}/` `src: User flow`
- [ ] `C-UF-05` `contract` The topic index is served at `/topics/` `src: User flow`
- [ ] `C-UF-06` `contract` A topic post is served at `/topics/{id}/` `src: User flow`
- [ ] `C-UF-07` `contract` The enquiry form is served at `/talk-with-us/` `src: User flow`
- [ ] `C-UF-08` `contract` The enquiry confirmation is served at `/talk-with-us/sent/` `src: User flow`
- [ ] `C-UF-09` `contract` The privacy page is served at `/privacy/` `src: User flow`
- [ ] `C-UF-10` `contract` The terms page is served at `/terms/` `src: User flow`
- [ ] `C-UF-11` `contract` The editorial interface is served at `/studio/` `src: User flow`
- [ ] `C-UF-12` `contract` Stored enquiries are served at `/studio/enquiries/` `src: User flow`
- [ ] `C-UF-13` `contract` The studio route requires the editor role `src: User flow`
- [ ] `C-UF-14` `capability` An unauthenticated request for a studio route lands on `/signin/` `src: User flow`
- [ ] `C-UF-15` `capability` Signing in as the seeded editor lands on the editorial interface `src: User flow`
- [ ] `C-UF-16` `capability` Signing in as the seeded reader lands on the home route `src: User flow`
- [ ] `C-UF-17` `capability` Signing out returns to the home route, ending the session `src: User flow`
- [ ] `C-UF-18` `capability` A signed-in reader asking for a studio route is denied, never redirected `src: User flow`
- [ ] `C-UF-19` `capability` A draft project detail request is answered as not found for every unentitled caller `src: User flow`
- [ ] `C-UF-20` `ui` Every list surface carries an empty state saying what is missing `src: User flow`
- [ ] `C-UF-21` `ui` Every route carries a loading state until content arrives `src: User flow`
- [ ] `C-UF-22` `ui` A failed request leaves the rest of the page usable `src: User flow`
- [ ] `C-UF-23` `ui` No surface ever replaces the page with a stack trace `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The ground is a near-white neutral `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Body copy, display text sit in a mid neutral `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Filled buttons, arrow discs at rest sit in a deep cool neutral `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Secondary metadata sits in a mid cool neutral `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Hairlines, the loader ground sit in a light cool neutral `src: UI/UX notes`
- [ ] `C-UX-06` `constraint` No near-black neutral appears on any of the site own surfaces `src: UI/UX notes`
- [ ] `C-UX-07` `constraint` A third-party player palette stays inside the player frame `src: UI/UX notes`
- [ ] `C-UX-08` `literal` The Latin family is `Satoshi` with a normative fallback stack `src: UI/UX notes`
- [ ] `C-UX-09` `literal` The Japanese family is `Noto Sans JP` with a normative fallback stack `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Display headings are enormous, thin, grey, never heavy `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Loader numerals use tabular figures so the counter does not jitter sideways `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Button labels never break a word in half `src: UI/UX notes`
- [ ] `C-UX-13` `ui` Density is spacious, with strands separated by air rather than rules `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The motion character is eased, with one overshooting exception `src: UI/UX notes`
- [ ] `C-UX-15` `ui` A line reveal fades in faster than the reveal moves `src: UI/UX notes`
- [ ] `C-UX-16` `ui` Scrolling backwards un-reveals text that had already arrived `src: UI/UX notes`
- [ ] `C-UX-17` `ui` A picture is uncovered by a plate sweeping across, never by a fade `src: UI/UX notes`
- [ ] `C-UX-18` `ui` Alternate gallery cells are delayed so the grid uncovers as a diagonal `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Sibling filled shapes blend into a visible neck as the shapes approach `src: UI/UX notes`
- [ ] `C-UX-20` `ui` The paired arrow discs on the contact rail read as one shape at rest `src: UI/UX notes`
- [ ] `C-UX-21` `ui` The navigation overlay is revealed by a wipe travelling up the screen `src: UI/UX notes`
- [ ] `C-UX-22` `ui` The overlay continues upward when closing, taking far less time `src: UI/UX notes`
- [ ] `C-UX-23` `ui` The two marquee bands move exactly as far as the scroll `src: UI/UX notes`
- [ ] `C-UX-24` `ui` The pointer disc arrives late, never quite catching up `src: UI/UX notes`
- [ ] `C-UX-25` `ui` Under reduced motion the line reveals render already revealed `src: UI/UX notes`
- [ ] `C-UX-26` `ui` Under reduced motion the marquee stops `src: UI/UX notes`
- [ ] `C-UX-27` `ui` Under reduced motion the simulation continues at reduced amplitude `src: UI/UX notes`
- [ ] `C-UX-28` `ui` Text meets WCAG AA contrast against the ground at every size used `src: UI/UX notes`
- [ ] `C-UX-29` `ui` The inactive switcher half meets the same contrast bar `src: UI/UX notes`
- [ ] `C-UX-30` `ui` Meaning is never carried by colour alone `src: UI/UX notes`
- [ ] `C-UX-31` `ui` Full keyboard navigation reaches every control with a visible focus ring `src: UI/UX notes`
- [ ] `C-UX-32` `ui` Icon-only controls carry accessible names `src: UI/UX notes`
- [ ] `C-UX-33` `ui` The `Show Reel` label exists as real text on the block the label names `src: UI/UX notes`
- [ ] `C-UX-34` `ui` The layout archetype is top navigation with no persistent sidebar `src: UI/UX notes`
- [ ] `C-UX-35` `ui` There is exactly one structural breakpoint, at tablet width `src: UI/UX notes`
- [ ] `C-UX-36` `ui` At a narrow viewport nothing overflows sideways `src: UI/UX notes`
- [ ] `C-UX-37` `ui` At a narrow viewport every navigation target stays reachable `src: UI/UX notes`
- [ ] `C-UX-38` `ui` A short window moves the settings panel to the bottom corner `src: UI/UX notes`
- [ ] `C-UX-39` `constraint` The mode is light, with no dark edition in the build `src: UI/UX notes`
- [ ] `C-UX-40` `constraint` No card border, no shadow, no hover tint appears on an index row `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server produces the HTML for every route `src: Technical requirements`
- [ ] `C-TR-02` `literal` The backend is `Flask` with `Jinja` templates `src: Technical requirements`
- [ ] `C-TR-03` `constraint` No client-side framework is introduced `src: Technical requirements`
- [ ] `C-TR-04` `literal` The datastore is `PostgreSQL`, read from `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-05` `literal` Binary content lives in `MinIO` `src: Technical requirements`
- [ ] `C-TR-06` `literal` The object store endpoint is read from `STORAGE_ENDPOINT` `src: Technical requirements`
- [ ] `C-TR-07` `literal` The bucket name is read from `STORAGE_BUCKET` `src: Technical requirements`
- [ ] `C-TR-08` `literal` The object store keys are read from `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` `src: Technical requirements`
- [ ] `C-TR-09` `contract` `GET /api/health` returns `200` once the app is ready `src: Technical requirements`
- [ ] `C-TR-10` `capability` The app logs one structured line per request `src: Technical requirements`
- [ ] `C-TR-11` `constraint` No second database, cache, queue, object store, identity provider is introduced `src: Technical requirements`
- [ ] `C-TR-12` `constraint` Every host, port, credential is read from the environment `src: Technical requirements`
- [ ] `C-TR-13` `constraint` No credential appears in anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-14` `constraint` No secret appears in a served document, a script, a stylesheet `src: Technical requirements`
- [ ] `C-TR-15` `literal` Object keys follow `media/{collection}/{record_id}/{sha256_of_bytes}.{ext}` `src: Technical requirements`
- [ ] `C-TR-16` `constraint` Bytes live in the bucket, never on the container filesystem `src: Technical requirements`
- [ ] `C-TR-17` `capability` Protected content is reached through an authenticated streaming endpoint `src: Technical requirements`
- [ ] `C-TR-18` `constraint` No pre-signed URL is issued for an unpublished record `src: Technical requirements`
- [ ] `C-TR-19` `capability` The streaming endpoint applies the same draft rule the detail route applies `src: Technical requirements`
- [ ] `C-TR-20` `constraint` The site ships no binary asset of any kind `src: Technical requirements`
- [ ] `C-TR-21` `constraint` Every icon is inline vector geometry, never an icon font `src: Technical requirements`
- [ ] `C-TR-22` `capability` A third-party video embed loads only after entering the viewport `src: Technical requirements`
- [ ] `C-TR-23` `constraint` A third-party embed does not set the page own type, colour `src: Technical requirements`
- [ ] `C-TR-24` `capability` Cumulative layout shift stays at zero `src: Technical requirements`
- [ ] `C-TR-25` `capability` Every media box declares an aspect ratio before content arrives `src: Technical requirements`
- [ ] `C-TR-26` `capability` One reveal observer serves the whole document `src: Technical requirements`
- [ ] `C-TR-27` `capability` Fonts are subset to the character inventory the site uses `src: Technical requirements`
- [ ] `C-TR-28` `capability` The app reconnects after a backing service restarts `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `data` Six tables carry the whole model `src: Data model`
- [ ] `C-DM-02` `data` All timestamps are UTC `src: Data model`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: Data model`
- [ ] `C-DM-04` `contract` The seeded credentials are written to `/app/USER_README.md` `src: Data model`
- [ ] `C-DM-05` `data` The `accounts` table carries a unique case-insensitive email `src: Data model`
- [ ] `C-DM-06` `data` The `accounts` role is one of `reader`, `editor` `src: Data model`
- [ ] `C-DM-07` `data` The `projects` id is an integer, serving as the route segment `src: Data model`
- [ ] `C-DM-08` `data` The `projects` disciplines set is non-empty `src: Data model`
- [ ] `C-DM-09` `data` The `projects` status is one of `draft`, `published` `src: Data model`
- [ ] `C-DM-10` `data` The `projects` hero_key names the stored hero object `src: Data model`
- [ ] `C-DM-11` `data` The `project_media` row is the only record of a stored object `src: Data model`
- [ ] `C-DM-12` `data` The `project_credits` rows are ordered by position `src: Data model`
- [ ] `C-DM-13` `data` The `topics` category is exactly one of the five enumerated values `src: Data model`
- [ ] `C-DM-14` `data` The `members` interests are an ordered list of short strings `src: Data model`
- [ ] `C-DM-15` `data` The `enquiries` row is written only when consent is true `src: Data model`
- [ ] `C-DM-16` `data` A refused enquiry submission writes nothing at all `src: Data model`
- [ ] `C-DM-17` `data` The `enquiries` locale is one of `ja`, `en` `src: Data model`
- [ ] `C-DM-18` `capability` An unpublished record hero object is readable only by an editor `src: Data model`
- [ ] `C-DM-19` `constraint` Seeding is idempotent, so restarting duplicates no rows `src: Data model`
- [ ] `C-DM-20` `literal` The seeded published project `1396` is titled `Forest Economy Recruit` `src: Data model`
- [ ] `C-DM-21` `literal` The seeded project `1396` client is `Midori Holdings` `src: Data model`
- [ ] `C-DM-22` `literal` The seeded project `1402` carries the year label `2025-26` `src: Data model`
- [ ] `C-DM-23` `literal` The seeded draft project is `1435`, titled `Shoegaze Debut Night` `src: Data model`
- [ ] `C-DM-24` `literal` The seeded published topic `1358` is titled `Continuing Is What Showed Us` `src: Data model`
- [ ] `C-DM-25` `literal` The seeded draft topic is `1364`, titled `Starting From Cannot` `src: Data model`
- [ ] `C-DM-26` `literal` Four members are seeded, beginning with `Naoki Morishita` as `CEO` `src: Data model`
- [ ] `C-DM-27` `literal` Every seeded member location is `Yokohama` `src: Data model`
- [ ] `C-DM-28` `capability` Each seeded record has a hero object already in the bucket `src: Data model`
- [ ] `C-DM-29` `capability` The draft records have hero objects too, so denial is about entitlement `src: Data model`
- [ ] `C-DM-30` `literal` The seeded legal name is `Kaiyo Interactive Co.,Ltd.` `src: Data model`
- [ ] `C-DM-31` `literal` The seeded telephone number is `045-548-6865` `src: Data model`
- [ ] `C-DM-32` `literal` The seeded postcode is `231-0003` `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Eleven real routes carry the site, plus the detail routes `src: Front-end specification`
- [ ] `C-FE-02` `ui` The overlay opened from the header rail is the complete map `src: Front-end specification`
- [ ] `C-FE-03` `ui` The footer repeats the same three route columns as the overlay `src: Front-end specification`
- [ ] `C-FE-04` `ui` Each home strand ends at a `View more` control pointing at an index `src: Front-end specification`
- [ ] `C-FE-05` `ui` Four type classes are carried per element rather than per document `src: Front-end specification`
- [ ] `C-FE-06` `ui` Both collections order newest first by published date `src: Front-end specification`
- [ ] `C-FE-07` `constraint` Neither index carries a paging control `src: Front-end specification`
- [ ] `C-FE-08` `capability` The persistent shell is shared by every route without remounting `src: Front-end specification`
- [ ] `C-FE-09` `capability` The canvas is part of the shell, keeping position across a route change `src: Front-end specification`
- [ ] `C-FE-10` `ui` Sizes scale continuously with viewport width, freezing above the design width `src: Front-end specification`
- [ ] `C-FE-11` `ui` The canvas sits behind everything in the stacking order `src: Front-end specification`
- [ ] `C-FE-12` `ui` The header rail sits above the open overlay so the rail stays legible `src: Front-end specification`
- [ ] `C-FE-13` `ui` The loader sits at the top of the stacking order `src: Front-end specification`
- [ ] `C-FE-14` `literal` The strapline reads `digital communication service with branding design` `src: Front-end specification`
- [ ] `C-FE-15` `ui` The logotype hides whenever the overlay is open `src: Front-end specification`
- [ ] `C-FE-16` `literal` The menu control label reads `Menu` at rest, `Close` when open `src: Front-end specification`
- [ ] `C-FE-17` `ui` The menu control collapses to a disc on a narrow viewport `src: Front-end specification`
- [ ] `C-FE-18` `ui` The contact rail is fixed to the bottom of the viewport on every route `src: Front-end specification`
- [ ] `C-FE-19` `literal` The contact rail repeats the phrase `Talk with us` `src: Front-end specification`
- [ ] `C-FE-20` `ui` The footer reveals on scroll as one unit `src: Front-end specification`
- [ ] `C-FE-21` `ui` The labelled pill shows a visible neck between disc, plate at rest `src: Front-end specification`
- [ ] `C-FE-22` `ui` Pointing at the labelled pill closes the neck into one lozenge `src: Front-end specification`
- [ ] `C-FE-23` `ui` A paired-arrow link label rolls upward to a duplicate on a pointer `src: Front-end specification`
- [ ] `C-FE-24` `ui` Six glyphs are drawn as inline vector geometry `src: Front-end specification`
- [ ] `C-FE-25` `ui` The paper-plane glyph carries a fold crease as a second subpath `src: Front-end specification`
- [ ] `C-FE-26` `ui` The location pin is built from a circle, a line `src: Front-end specification`
- [ ] `C-FE-27` `ui` The loader counts `000` to `100`, zero padded `src: Front-end specification`
- [ ] `C-FE-28` `ui` The loader ground pales from a light cool neutral to a near-white neutral `src: Front-end specification`
- [ ] `C-FE-29` `ui` A state class is added on crossing a threshold, removed on leaving `src: Front-end specification`
- [ ] `C-FE-30` `ui` The line reveal starts slightly more than a line height below the clip edge `src: Front-end specification`
- [ ] `C-FE-31` `ui` The ruled subheading draws a hairline growing from no width `src: Front-end specification`
- [ ] `C-FE-32` `ui` The dotted subheading carries a square bullet, a dashed underline `src: Front-end specification`
- [ ] `C-FE-33` `ui` The image wipe grows from the left, then shrinks away to the right `src: Front-end specification`
- [ ] `C-FE-34` `ui` The plain fade is the fallback for elements that must not move `src: Front-end specification`
- [ ] `C-FE-35` `ui` The marquee offset is scrubbed against scroll position `src: Front-end specification`
- [ ] `C-FE-36` `ui` The canvas opacity is scrubbed against scroll position `src: Front-end specification`
- [ ] `C-FE-37` `constraint` Nothing is keyed off a user-agent string `src: Front-end specification`
- [ ] `C-FE-38` `ui` The settings panel shadow is almost invisible by intent `src: Front-end specification`
- [ ] `C-FE-39` `ui` The settings panel grows from the control rather than fading in `src: Front-end specification`
- [ ] `C-FE-40` `ui` The page goes soft behind the settings panel as the panel grows `src: Front-end specification`
- [ ] `C-FE-41` `ui` The panel scrollbar is the site own overlay scrollbar `src: Front-end specification`
- [ ] `C-FE-42` `ui` A full-viewport catcher closes the panel on an outside click `src: Front-end specification`
- [ ] `C-FE-43` `ui` The catcher is pointer-transparent whenever the panel is shut `src: Front-end specification`
- [ ] `C-FE-44` `literal` The hero headline rows read `Interactive`, `Experiences with Us`, `for Active Growth.` `src: Front-end specification`
- [ ] `C-FE-45` `ui` The first hero row, the third hero row are indented `src: Front-end specification`
- [ ] `C-FE-46` `ui` The hero standfirst sits past the right margin on a wide window `src: Front-end specification`
- [ ] `C-FE-47` `ui` The show reel content is twice the frame width, panning across `src: Front-end specification`
- [ ] `C-FE-48` `ui` The projects strand heading is right aligned `src: Front-end specification`
- [ ] `C-FE-49` `ui` The topics strand heading is clipped by the strand top edge `src: Front-end specification`
- [ ] `C-FE-50` `ui` The four-discipline diagram stacks four silhouettes at descending opacity `src: Front-end specification`
- [ ] `C-FE-51` `literal` The studio rail reads `Group Philosophy`, `Mission`, `Vision`, `Our DNA`, `Culture` `src: Front-end specification`
- [ ] `C-FE-52` `capability` The studio rail marks the strand occupying the viewport `src: Front-end specification`
- [ ] `C-FE-53` `capability` The studio rail updates on a scroll in either direction `src: Front-end specification`
- [ ] `C-FE-54` `capability` Each studio rail entry scrolls its strand into view `src: Front-end specification`
- [ ] `C-FE-55` `ui` The studio route ground moves through three values on descent `src: Front-end specification`
- [ ] `C-FE-56` `ui` A studio strand figure holds a rendered soft-bodied form `src: Front-end specification`
- [ ] `C-FE-57` `ui` A discipline figure is a large circle clipped from moving footage `src: Front-end specification`
- [ ] `C-FE-58` `constraint` A discipline figure carries no frame, no border, no shadow `src: Front-end specification`
- [ ] `C-FE-59` `ui` A case row carries a title, a truncated subtitle, a metadata row `src: Front-end specification`
- [ ] `C-FE-60` `ui` The whole case row is the link `src: Front-end specification`
- [ ] `C-FE-61` `ui` A project hero still runs full bleed with no container `src: Front-end specification`
- [ ] `C-FE-62` `ui` The gallery is a full-bleed grid at mixed spans with a hairline gutter `src: Front-end specification`
- [ ] `C-FE-63` `ui` The credit block is a two-column list with dotted rules between rows `src: Front-end specification`
- [ ] `C-FE-64` `ui` The company profile rows are separated by hairlines above, below `src: Front-end specification`
- [ ] `C-FE-65` `ui` The business content bullets are literal characters, never list markers `src: Front-end specification`
- [ ] `C-FE-66` `ui` The topic detail column is centred at about half the viewport width `src: Front-end specification`
- [ ] `C-FE-67` `ui` A topic chapter heading is preceded by a hairline across the column `src: Front-end specification`
- [ ] `C-FE-68` `ui` The paragraph gap is clearly larger than the line gap `src: Front-end specification`
- [ ] `C-FE-69` `ui` No enquiry field is boxed, each being a label above a ruled input `src: Front-end specification`
- [ ] `C-FE-70` `ui` The first enquiry field sits on a white plate, the only card on the route `src: Front-end specification`
- [ ] `C-FE-71` `ui` The budget control reads as a thick dark bar with two pale notches `src: Front-end specification`
- [ ] `C-FE-72` `ui` Both budget notches stay inside the bar at the extremes `src: Front-end specification`
- [ ] `C-FE-73` `ui` The privacy block scrolls inside a fixed-height container `src: Front-end specification`
- [ ] `C-FE-74` `literal` The submit control carries the label `Submit` `src: Front-end specification`
- [ ] `C-FE-75` `literal` The not-found route carries `404`, `Back to TOP` `src: Front-end specification`
- [ ] `C-FE-76` `ui` The not-found route renders the full persistent shell `src: Front-end specification`
- [ ] `C-FE-77` `literal` The copyright line reads `Copyright Kaiyo Interactive Co.,Ltd. All Rights Reserved.` `src: Front-end specification`
- [ ] `C-FE-78` `literal` An index handoff control is labelled `View more` `src: Front-end specification`
- [ ] `C-FE-79` `constraint` No image, video, font, model, texture is in the delivered build directory `src: Front-end specification`
- [ ] `C-FE-80` `capability` Switching away from the tab pauses the simulation `src: Front-end specification`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` There is a single studio tenant, with no organisation model `src: Constraints`
- [ ] `C-CN-02` `constraint` There is no shop, no cart, no pricing, no payments `src: Constraints`
- [ ] `C-CN-03` `constraint` There are no comments, no likes, no ratings, no sharing widgets `src: Constraints`
- [ ] `C-CN-04` `constraint` There is no search across the site `src: Constraints`
- [ ] `C-CN-05` `constraint` There is no newsletter, no mailing list, no chat widget `src: Constraints`
- [ ] `C-CN-06` `constraint` No notification is sent to anybody `src: Constraints`
- [ ] `C-CN-07` `constraint` There is no password reset, no third-party identity provider `src: Constraints`
- [ ] `C-CN-08` `constraint` No external network call is made at run time beyond the named services `src: Constraints`
- [ ] `C-CN-09` `constraint` There is no native application, no installable app shell `src: Constraints`
- [ ] `C-CN-10` `constraint` The app stays responsive with two hundred projects `src: Constraints`
- [ ] `C-CN-11` `constraint` The app stays responsive with fifty thousand stored enquiries `src: Constraints`
- [ ] `C-CN-12` `constraint` The app stays responsive with a gallery of sixty items on one case `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The port mapping is `${APP_PUBLIC_PORT}:4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps `src: Deployment contract`
- [ ] `C-DC-05` `contract` Reserved `.browser_screenshots/` directory exists at the app root, empty `src: Deployment contract`
- [ ] `C-DC-06` `contract` Reserved `.downloads/` directory exists at the app root, empty `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served behind a static or preview server `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0`, never `127.0.0.1` `src: Deployment contract`
- [ ] `C-DC-10` `contract` The backing services are already running, so none is started by the app `src: Deployment contract`
- [ ] `C-DC-11` `contract` No persistent volumes, no fixed container names, no custom networks `src: Deployment contract`
- [ ] `C-DC-12` `contract` `GET /api/projects` returns a top-level JSON array newest first `src: Deployment contract`
- [ ] `C-DC-13` `contract` `GET /api/topics` accepts an optional category query `src: Deployment contract`
- [ ] `C-DC-14` `contract` `GET /api/members` returns a top-level JSON array in display order `src: Deployment contract`
- [ ] `C-DC-15` `contract` `POST /api/enquiries` accepts the eleven form fields `src: Deployment contract`
- [ ] `C-DC-16` `contract` `GET /api/enquiries` is restricted to the editor role `src: Deployment contract`
- [ ] `C-DC-17` `contract` `POST /api/auth/login` returns a bearer token, the account role `src: Deployment contract`
- [ ] `C-DC-18` `contract` `GET /api/media/{key}` streams the stored object bytes `src: Deployment contract`
- [ ] `C-DC-19` `contract` An invalid call is rejected as a client error, never a server error `src: Deployment contract`
- [ ] `C-DC-20` `constraint` A hero still existing only as a filesystem file is not a stored object `src: Deployment contract`
- [ ] `C-DC-21` `constraint` An enquiry existing only in a confirmation page is not a stored enquiry `src: Deployment contract`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `editor@example.com` | the seeded editor account | `C-RL-15` |
| `reader@example.com` | the seeded reader account | `C-RL-16` |
| `deku-demo-pw-2026` | the seeded password | `C-DM-03` |
| `Background` | the ground colour well label | `C-CF-21` |
| `Sphere colour one` | the first sphere colour well label | `C-CF-22` |
| `Sphere colour two` | the second sphere colour well label | `C-CF-23` |
| `Angular damping` | a physics range label | `C-CF-24` |
| `Linear damping` | a physics range label | `C-CF-25` |
| `Return force` | a physics range label | `C-CF-26` |
| `Movement range` | a physics range label | `C-CF-27` |
| `Strength` | a lighting range label | `C-CF-28` |
| `Diffuse` | a lighting range label | `C-CF-29` |
| `Metaball` | the physics separator label | `C-CF-30` |
| `Light` | the lighting separator label | `C-CF-31` |
| `All` | the default category rail entry | `C-CF-71` |
| `Blog` | a category rail entry | `C-CF-71` |
| `Member` | a category rail entry | `C-CF-71` |
| `Interview` | a category rail entry | `C-CF-71` |
| `News` | a category rail entry | `C-CF-71` |
| `Recruit` | a category rail entry | `C-CF-71` |
| `2026.3.18` | the unpadded topic date | `C-CF-76` |
| `Profile` | a company rail entry | `C-CF-84` |
| `Access` | a company rail entry | `C-CF-84` |
| `Digital` | a discipline name | `C-CF-86` |
| `Movie` | a discipline name | `C-CF-86` |
| `Spatial` | a discipline name | `C-CF-86` |
| `Brand` | a discipline name | `C-CF-86` |
| `Related Projects` | the discipline handoff label | `C-CF-87` |
| `enquiry` | an enquiry type value | `C-CF-90` |
| `materials_request` | an enquiry type value | `C-CF-90` |
| `digital_general` | the first interest value | `C-CF-91` |
| `within_3_months` | the first timeline value | `C-CF-92` |
| `1000000` | the budget floor in yen | `C-CF-93` |
| `30000000` | the budget ceiling in yen | `C-CF-93` |
| `JP` | a language switcher label | `C-CF-113` |
| `EN` | a language switcher label | `C-CF-113` |
| `About Us` | a display heading | `C-CF-115` |
| `Service` | a display heading | `C-CF-115` |
| `Projects` | a display heading | `C-CF-115` |
| `Topics` | a display heading | `C-CF-115` |
| `Talk with us` | a display heading | `C-CF-115` |
| `/en/` | the English edition prefix | `C-CF-112` |
| `/` | the home route | `C-UF-01` |
| `/projects/` | the project index route | `C-UF-03` |
| `/projects/{id}/` | the project case route | `C-UF-04` |
| `/topics/` | the topic index route | `C-UF-05` |
| `/topics/{id}/` | the topic post route | `C-UF-06` |
| `/talk-with-us/` | the enquiry route | `C-UF-07` |
| `/talk-with-us/sent/` | the confirmation route | `C-UF-08` |
| `/privacy/` | the privacy route | `C-UF-09` |
| `/terms/` | the terms route | `C-UF-10` |
| `/studio/` | the editorial route | `C-UF-11` |
| `/studio/enquiries/` | the stored enquiry route | `C-UF-12` |
| `/signin/` | the sign-in route | `C-UF-14` |
| `Satoshi` | the Latin family | `C-UX-08` |
| `Noto Sans JP` | the Japanese family | `C-UX-09` |
| `Show Reel` | the show reel label | `C-UX-33` |
| `Flask` | the backend framework | `C-TR-02` |
| `Jinja` | the template layer | `C-TR-02` |
| `PostgreSQL` | the datastore | `C-TR-04` |
| `DATABASE_URL` | the datastore variable | `C-TR-04` |
| `MinIO` | the object store | `C-TR-05` |
| `STORAGE_ENDPOINT` | the object store endpoint variable | `C-TR-06` |
| `STORAGE_BUCKET` | the bucket variable | `C-TR-07` |
| `STORAGE_ACCESS_KEY` | an object store credential variable | `C-TR-08` |
| `STORAGE_SECRET_KEY` | an object store credential variable | `C-TR-08` |
| `GET /api/health` | the readiness endpoint | `C-TR-09` |
| `200` | the readiness status | `C-TR-09` |
| `media/{collection}/{record_id}/{sha256_of_bytes}.{ext}` | the object key scheme | `C-TR-15` |
| `/app/USER_README.md` | the credential file | `C-DM-04` |
| `reader` | an account role value | `C-DM-06` |
| `editor` | an account role value | `C-DM-06` |
| `draft` | a record status value | `C-DM-09` |
| `published` | a record status value | `C-DM-09` |
| `ja` | a locale value | `C-DM-17` |
| `en` | a locale value | `C-DM-17` |
| `1396` | the first seeded project id | `C-DM-20` |
| `Forest Economy Recruit` | the first seeded project title | `C-DM-20` |
| `Midori Holdings` | the first seeded project client | `C-DM-21` |
| `1402` | the second seeded project id | `C-DM-22` |
| `2025-26` | the free-text year label | `C-DM-22` |
| `1435` | the seeded draft project id | `C-DM-23` |
| `Shoegaze Debut Night` | the seeded draft project title | `C-DM-23` |
| `1358` | the first seeded topic id | `C-DM-24` |
| `Continuing Is What Showed Us` | the first seeded topic title | `C-DM-24` |
| `1364` | the seeded draft topic id | `C-DM-25` |
| `Starting From Cannot` | the seeded draft topic title | `C-DM-25` |
| `Naoki Morishita` | the seeded representative | `C-DM-26` |
| `CEO` | the seeded representative job title | `C-DM-26` |
| `Yokohama` | the seeded member location | `C-DM-27` |
| `Kaiyo Interactive Co.,Ltd.` | the seeded legal name | `C-DM-30` |
| `045-548-6865` | the seeded telephone number | `C-DM-31` |
| `231-0003` | the seeded postcode | `C-DM-32` |
| `digital communication service with branding design` | the strapline | `C-FE-14` |
| `Menu` | the menu control resting label | `C-FE-16` |
| `Close` | the menu control open label | `C-FE-16` |
| `000` | the loader start count | `C-FE-27` |
| `100` | the loader end count | `C-FE-27` |
| `Interactive` | the first hero row | `C-FE-44` |
| `Experiences with Us` | the second hero row | `C-FE-44` |
| `for Active Growth.` | the third hero row | `C-FE-44` |
| `Group Philosophy` | a studio rail entry | `C-FE-51` |
| `Mission` | a studio rail entry | `C-FE-51` |
| `Vision` | a studio rail entry | `C-FE-51` |
| `Our DNA` | a studio rail entry | `C-FE-51` |
| `Culture` | a studio rail entry | `C-FE-51` |
| `Submit` | the submit control label | `C-FE-74` |
| `404` | the not-found title | `C-FE-75` |
| `Back to TOP` | the not-found control label | `C-FE-75` |
| `Copyright Kaiyo Interactive Co.,Ltd. All Rights Reserved.` | the copyright line | `C-FE-77` |
| `View more` | the index handoff label | `C-FE-78` |
| `Client` | the client label | `C-CF-64` |
| `Visit site` | the outbound case link label | `C-CF-65` |
| `APP_PUBLIC_URL` | the public app variable | `C-DC-01` |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | `C-DC-02` |
| `/api` | the API prefix | `C-DC-03` |
| `.browser_screenshots/` | a reserved directory | `C-DC-05` |
| `.downloads/` | a reserved directory | `C-DC-06` |
| `0.0.0.0` | the bind address | `C-DC-09` |
| `127.0.0.1` | the forbidden bind address | `C-DC-09` |
| `GET /api/projects` | the project list endpoint | `C-DC-12` |
| `GET /api/topics` | the topic list endpoint | `C-DC-13` |
| `GET /api/members` | the member list endpoint | `C-DC-14` |
| `POST /api/enquiries` | the enquiry submit endpoint | `C-DC-15` |
| `GET /api/enquiries` | the stored enquiry endpoint | `C-DC-16` |
| `POST /api/auth/login` | the sign-in endpoint | `C-DC-17` |
| `GET /api/media/{key}` | the object streaming endpoint | `C-DC-18` |
| `Menu` | the collapsed control label | `C-FE-17` |
| `Talk with us` | the contact rail phrase | `C-FE-19` |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the two default sphere colours of the mass | `C-CF-07` |
| the minimum of each physics range | `C-CF-41` |
| the maximum of each physics range | `C-CF-41` |
| the number of attempts before an enquiry origin is refused | `C-CF-104` |
| the window in which repeated enquiry attempts are counted | `C-CF-104` |
| the bearer token expiry interval | `C-CF-119` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 2 | 5 |
| User roles | 2 | 16 |
| Core features | 10 | 130 |
| User flow | 8 | 23 |
| UI and UX notes | 14 | 40 |
| Technical requirements | 5 | 28 |
| Data model | 3 | 32 |
| Front-end specification | 8 | 80 |
| Constraints | 1 | 12 |
| Deployment contract | 11 | 21 |
