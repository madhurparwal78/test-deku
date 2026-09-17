# Checklist: Naught'

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, techrequirements, datamodel, constraints, deployment
Sections absent: buildplan
Items: 281
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The public site is served to a visitor with no session. `src: Overview, Overview para 2`

## C-RL User roles

- [ ] `C-RL-01` `capability` Signup is open, so anyone creates an account from `/sign-up`. `src: User roles, User roles signup para`
- [ ] `C-RL-02` `role` A new account from `/sign-up` holds the `reader` role, usable at once. `src: User roles, User roles signup para`
- [ ] `C-RL-03` `role` A `reader` reads only the enquiries attached to the reader's own account. `src: User roles, User roles table row 2`
- [ ] `C-RL-04` `role` A `reader` is denied reading another reader's enquiries. `src: User roles, User roles table row 2`
- [ ] `C-RL-05` `role` A request for another reader's enquiry is answered as a missing record. `src: User roles, User roles para`
- [ ] `C-RL-06` `role` A `reader` is denied changing any enquiry's status. `src: User roles, User roles table row 2`
- [ ] `C-RL-07` `role` A reader's denied status change leaves the enquiry status unchanged. `src: User roles, User roles authorization para`
- [ ] `C-RL-08` `role` A `reader` is denied creating, publishing, uploading anything. `src: User roles, User roles table row 2`
- [ ] `C-RL-09` `role` No route grants the `author` role. `src: User roles, User roles signup para`
- [ ] `C-RL-10` `role` A visitor with no account is denied reading any enquiry. `src: User roles, User roles visitor para`
- [ ] `C-RL-11` `role` An `author` reads every enquiry. `src: User roles, User roles table row 1`
- [ ] `C-RL-12` `role` An `author` is denied deleting an enquiry. `src: User roles, User roles table row 1`
- [ ] `C-RL-13` `role` A `reader` is denied the page view record. `src: User roles, User roles table row 2`

## C-CF Core features

- [ ] `C-CF-01` `ui` The home route ground is white for the first band, black for every band after the hero. `src: Core features, The home route para`
- [ ] `C-CF-02` `literal` The featured rail `View all` control shows the published count, `( 07 )` with the seed. `src: Core features, The home route para`
- [ ] `C-CF-03` `constraint` The featured rail count reads the catalogue length rather than the rail length. `src: Core features, The home route para`
- [ ] `C-CF-04` `data` The home route carries thirteen bands in one scrolling document. `src: Core features, The home route para`
- [ ] `C-CF-05` `literal` The works index masthead shows `Works` beside `©24 . 26` at the same size. `src: Core features, The works index para`
- [ ] `C-CF-06` `capability` The whole works index card is the link to the card's case study. `src: Core features, The works index para`
- [ ] `C-CF-07` `data` Seven case studies are published, listed in ordinal order. `src: Core features, Drafts and publication para`
- [ ] `C-CF-08` `constraint` The works index lists published case studies only. `src: Core features, The works index para`
- [ ] `C-CF-09` `ui` The case study renders the gallery bands in stored order. `src: Core features, The case study route para`
- [ ] `C-CF-10` `ui` The next published case study's masthead closes the case study as a link. `src: Core features, The case study route para`
- [ ] `C-CF-11` `constraint` The next-subject row wraps from the last ordinal to the first. `src: Core features, The case study route para`
- [ ] `C-CF-12` `constraint` The compact list omits the current case study. `src: Core features, The case study route para`
- [ ] `C-CF-13` `constraint` A case study with no gallery images renders no gallery, no placeholder text. `src: Core features, The case study route para`
- [ ] `C-CF-14` `ui` `book a call` opens a panel sliding over the current route from the right, without leaving the route. `src: Core features, Booking a call para`
- [ ] `C-CF-15` `ui` The booking panel asks for a name, an email, an optional company, the service, a preferred date, a time window, a message. `src: Core features, Booking a call para`
- [ ] `C-CF-16` `literal` A filed enquiry replaces the form with `Thanks. We'll be in touch within one working day.`. `src: Core features, Booking a call para`
- [ ] `C-CF-17` `literal` `drop us an email` is a mail link to `studio@example.com`, filing nothing. `src: Core features, Booking a call para`
- [ ] `C-CF-18` `capability` Anyone files an enquiry by booking a call, no session needed. `src: Core features, Booking a call para`
- [ ] `C-CF-19` `data` A new enquiry's status is `new`. `src: Core features, Booking a call para`
- [ ] `C-CF-20` `constraint` The enquiry email is trimmed, lowercased. `src: Core features, Booking a call table row 2`
- [ ] `C-CF-21` `literal` An empty name answers `Tell us your name`. `src: Core features, Booking a call table row 1`
- [ ] `C-CF-22` `constraint` A rejected booking keeps every value typed, showing each message beside the field. `src: Core features, Booking a call para`
- [ ] `C-CF-23` `literal` An invalid email answers `We need an email to reply to`. `src: Core features, Booking a call table row 2`
- [ ] `C-CF-24` `literal` A past preferred date answers `Pick a date from today on`. `src: Core features, Booking a call table row 5`
- [ ] `C-CF-25` `constraint` An empty booking name is refused; a name holds `1` to `80` characters after trimming. `src: Core features, Booking a call table row 1`
- [ ] `C-CF-26` `literal` A service outside the five answers `Pick what you have in mind`. `src: Core features, Booking a call table row 4`
- [ ] `C-CF-27` `constraint` A preferred date must be today or later. `src: Core features, Booking a call table row 5`
- [ ] `C-CF-28` `literal` A time window other than `morning` or `afternoon` answers `Pick a time of day`. `src: Core features, Booking a call table row 6`
- [ ] `C-CF-29` `literal` A message beyond `1000` characters answers `Say a little about the project`. `src: Core features, Booking a call table row 7`
- [ ] `C-CF-30` `literal` A company name beyond `80` characters answers `That company name is too long`. `src: Core features, Booking a call table row 3`
- [ ] `C-CF-31` `ui` A signed-in reader's enquiry appears at `/account` with the enquiry status. `src: Core features, Booking a call para`
- [ ] `C-CF-32` `literal` A registered address signing up again answers `That email is already registered`. `src: Core features, Identity para`
- [ ] `C-CF-33` `literal` A wrong password, an unknown address answer the same pinned credential mismatch message. `src: Core features, Identity para`
- [ ] `C-CF-34` `constraint` A display name holds `1` to `60` characters. `src: Core features, Identity para`
- [ ] `C-CF-35` `constraint` A password holds `8` to `200` characters. `src: Core features, Identity para`
- [ ] `C-CF-36` `data` A signed-in reader's enquiry is attached to the reader's account. `src: Core features, Booking a call para`
- [ ] `C-CF-37` `ui` `/studio` lists every case study as a card labelled `Draft` or `Published`. `src: Core features, The studio console para`
- [ ] `C-CF-38` `ui` `New case study` opens the slide-over panel; saving creates a draft card. `src: Core features, The studio console para`
- [ ] `C-CF-39` `ui` Opening a studio card shows the case study, the images, an upload control. `src: Core features, The studio console para`
- [ ] `C-CF-40` `ui` `Publish` waits for the service before the card changes. `src: Core features, The studio console para`
- [ ] `C-CF-41` `data` A case study is created as a draft. `src: Core features, Drafts and publication para`
- [ ] `C-CF-42` `contract` A stored image key follows the key scheme `works/{work_id}/{sha256_of_bytes}.{ext}`. `src: Core features, Media in the object store para`
- [ ] `C-CF-43` `constraint` A cover or gallery image is an object in the store. `src: Core features, Media in the object store para`
- [ ] `C-CF-44` `constraint` The key's digest is the lowercase hex sha256 of the uploaded bytes. `src: Core features, Media in the object store para`
- [ ] `C-CF-45` `constraint` Uploading the same bytes twice to one case study stores one object. `src: Core features, Media in the object store para`
- [ ] `C-CF-46` `capability` Publishing exposes the route, the record, the card, every image at once. `src: Core features, Drafts and publication rule 2`
- [ ] `C-CF-47` `constraint` Removing an image removes the image record, the stored object. `src: Core features, Media in the object store para`
- [ ] `C-CF-48` `ui` A draft's route renders the not-found template to anyone but a studio author. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-49` `ui` Signed in as an author, a draft's route renders the case study as the case study will look. `src: Core features, Drafts and publication rule 4`
- [ ] `C-CF-50` `literal` The draft is `Veloce`, ordinal `W'08`. `src: Core features, Drafts and publication para`
- [ ] `C-CF-51` `ui` A draft is absent from the works index, the featured rail, every next-subject row, every compact list. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-52` `contract` A draft's route `/works/<slug>` answers `404` to anyone but an author. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-53` `contract` `GET /api/works/<slug>` answers `404` for a draft to anyone but an author. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-54` `constraint` A draft is absent from `GET /api/works` for anyone but an author. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-55` `constraint` A request for a draft's image by the image's exact storage key answers `404`. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-56` `data` A draft image's object stays in the store, untouched. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-57` `capability` A studio author reads a draft record, the draft's images. `src: Core features, Drafts and publication rule 4`
- [ ] `C-CF-58` `constraint` The bucket is private, so an anonymous request straight to the store is refused. `src: Core features, Media in the object store para`
- [ ] `C-CF-59` `constraint` A draft never appears in a next-subject row. `src: Core features, Drafts and publication rule 1`
- [ ] `C-CF-60` `ui` `Unpublish` waits for the service before the studio card changes. `src: Core features, The studio console para`
- [ ] `C-CF-61` `ui` An unpublished case study's route renders the not-found template. `src: Core features, Drafts and publication rule 3`
- [ ] `C-CF-62` `capability` Unpublishing withdraws the route, the record, every image at once. `src: Core features, Drafts and publication rule 3`
- [ ] `C-CF-63` `constraint` Unpublishing leaves every stored object in place, so republishing needs no re-upload. `src: Core features, Drafts and publication rule 3`
- [ ] `C-CF-64` `constraint` Unpublishing one case study renumbers no other ordinal. `src: Core features, Drafts and publication rule 5`
- [ ] `C-CF-65` `data` Every case study stores an ordinal from `1` to `99`, printed `W'` with two digits. `src: Core features, Drafts and publication rule 5`
- [ ] `C-CF-66` `ui` `/studio/enquiries` lists every enquiry newest first with a status control. `src: Core features, The studio console para`
- [ ] `C-CF-67` `ui` Changing an enquiry status changes the inbox row at once. `src: Core features, The studio console para`
- [ ] `C-CF-68` `ui` The featured switch changes the studio card at once. `src: Core features, The studio console para`
- [ ] `C-CF-69` `constraint` An author moves an enquiry from `new` to `contacted`, then `closed`. `src: Core features, Booking a call para`
- [ ] `C-CF-70` `constraint` The featured rail shows published case studies marked featured, at most five. `src: Core features, The studio console para`
- [ ] `C-CF-71` `literal` The not-found document title is `Naught' to see here...`. `src: Core features, The not-found route para`
- [ ] `C-CF-72` `literal` The not-found route offers one pill reading `Homepage` returning to `/`. `src: Core features, The not-found route para`
- [ ] `C-CF-73` `contract` Any unmatched path renders the not-found template answering `404`. `src: Core features, The not-found route para`
- [ ] `C-CF-74` `constraint` The not-found route keeps the full chrome, the overlay, a visually hidden heading `ERROR 404`. `src: Core features, The not-found route para`
- [ ] `C-CF-75` `constraint` `/privacy` is linked from the footer of every public route. `src: Core features, The privacy page para`
- [ ] `C-CF-76` `ui` A `SOUND` toggle appears at the top centre of the window only during a film's time on screen. `src: Core features, Films and sound para`
- [ ] `C-CF-77` `ui` Every film plays without a gesture, muted, looping, with no controls. `src: Core features, Films and sound para`
- [ ] `C-CF-78` `constraint` The `SOUND` toggle is the only way sound is ever turned on. `src: Core features, Films and sound para`
- [ ] `C-CF-79` `constraint` The sound toggle announces the toggle's state to assistive technology. `src: Core features, Films and sound para`
- [ ] `C-CF-80` `constraint` Every film starts muted again on every route change. `src: Core features, Films and sound para`
- [ ] `C-CF-81` `constraint` No film is fetched until the film's band is within two window heights of the window. `src: Core features, Films and sound para`
- [ ] `C-CF-82` `ui` `/privacy` states what a booking keeps, why, for how long, the page view record, where to ask for deletion. `src: Core features, The privacy page para`
- [ ] `C-CF-83` `literal` The privacy page states `twelve months` after the enquiry is closed, naming `studio@example.com` for deletion. `src: Core features, The privacy page para`
- [ ] `C-CF-84` `constraint` Every public route declares a social preview title, an image answering `200` with an image. `src: Core features, Links and previews para`
- [ ] `C-CF-85` `constraint` Every internal link on every public route resolves to a page answering `200`. `src: Core features, Links and previews para`
- [ ] `C-CF-86` `data` Every public page view is recorded with the route, the instant served. `src: Core features, Page views para`
- [ ] `C-CF-87` `constraint` The page view record carries nothing identifying a visitor. `src: Core features, Page views para`
- [ ] `C-CF-88` `capability` A studio author reads the page view record at `GET /api/page-views`, filtered by route. `src: Core features, Page views para`
- [ ] `C-CF-89` `constraint` No third-party analytics runs anywhere, with no consent banner. `src: Core features, Page views para`
- [ ] `C-CF-90` `data` Seeding uploads generated stand-in images into the store as objects. `src: Core features, Media in the object store para`
- [ ] `C-CF-91` `constraint` A stored image description becomes the image's alternative text. `src: Core features, Media in the object store para`

## C-UF User flow

- [ ] `C-UF-01` `ui` A public route loads with the studio initial beside the initial's apostrophe, centred alone. `src: User flow, States table row 1`
- [ ] `C-UF-02` `contract` The route `/` serves the home route with the title `Naught' | Home`. `src: User flow, Routes table row 1`
- [ ] `C-UF-03` `contract` The route `/works` carries the title `Naught' | Works`. `src: User flow, Routes table row 2`
- [ ] `C-UF-04` `constraint` A route title separator is a space, a vertical bar, a space. `src: User flow, Routes para`
- [ ] `C-UF-05` `capability` `All Works` on a case study returns to `/works`. `src: User flow, Routes para`
- [ ] `C-UF-06` `contract` A case study route title is `Naught' | ` followed by the case study title. `src: User flow, Routes table row 3`
- [ ] `C-UF-07` `literal` During a booking send, the submit control reads `Sending` with every field disabled. `src: User flow, States table row 2`
- [ ] `C-UF-08` `ui` A signed-in reader reaching `/sign-up` is redirected to `/account`. `src: User flow, Entry table row 3`
- [ ] `C-UF-09` `literal` An account with no enquiries shows `No enquiries yet.` with a `book a call` pill. `src: User flow, States table row 3`
- [ ] `C-UF-10` `ui` `/account` lists the enquiry with the service, the preferred date, the time window, the status `new`. `src: User flow, Journeys para 2`
- [ ] `C-UF-11` `ui` `/account` shows the signed-in reader's own enquiries only. `src: User flow, Routes table`
- [ ] `C-UF-12` `ui` A reader asking for `/studio` gets the not-found template. `src: User flow, Entry table row 5`
- [ ] `C-UF-13` `contract` A visitor reaching `/studio` is redirected to `/sign-in?next=/studio`. `src: User flow, Entry table row 5`
- [ ] `C-UF-14` `contract` A reader asking for `/studio` answers `404`. `src: User flow, Entry table row 5`
- [ ] `C-UF-15` `ui` A signed-in author reaching `/sign-in` is redirected to `/studio`. `src: User flow, Entry table row 3`
- [ ] `C-UF-16` `ui` A published case study appears in `/works` at the case study's ordinal. `src: User flow, Journeys para 3`
- [ ] `C-UF-17` `contract` A reader asking for a draft's `/works/<slug>` answers `404`. `src: User flow, Entry table row 2`
- [ ] `C-UF-18` `contract` Anything unmatched carries the title `Naught' to see here...`, answering `404`. `src: User flow, Routes table row 10`
- [ ] `C-UF-19` `ui` The menu overlay's first row reads `home` on every route except `/`, where the row reads `works`. `src: User flow, Routes para`
- [ ] `C-UF-20` `contract` The route `/privacy` carries the title `Naught' | Privacy`. `src: User flow, Routes table`
- [ ] `C-UF-21` `ui` The menu overlay's `contact` row opens the booking panel. `src: User flow, Routes para`
- [ ] `C-UF-22` `ui` Signing in from a protected route returns the reader to the route first asked for. `src: User flow, Entry table para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The home route opens on a white ground for the hero band. `src: UI/UX notes, two grounds para`
- [ ] `C-UX-02` `ui` The home route ground turns black after the hero band, never switching back. `src: UI/UX notes, two grounds para`
- [ ] `C-UX-03` `ui` Body text rises line by line from behind the text's own edge. `src: UI/UX notes, motion para`
- [ ] `C-UX-04` `ui` Every image uncovers diagonally from a bottom corner alternating between columns. `src: UI/UX notes, motion para`
- [ ] `C-UX-05` `ui` Scrolling up plays every scroll-driven value backwards exactly. `src: UI/UX notes, motion para`
- [ ] `C-UX-06` `ui` Stopping the scroll leaves every scroll-driven effect stopped where the scroll stops. `src: UI/UX notes, motion para`
- [ ] `C-UX-07` `ui` The works index ground is black throughout. `src: UI/UX notes, two grounds para`
- [ ] `C-UX-08` `ui` Pointer feedback grows a short label at the pointer over a work card. `src: UI/UX notes, pointer para`
- [ ] `C-UX-09` `ui` A case study ground is white throughout. `src: UI/UX notes, two grounds para`
- [ ] `C-UX-10` `ui` The not-found route ground is black throughout. `src: UI/UX notes, two grounds para`
- [ ] `C-UX-11` `ui` The menu overlay closes on escape, returning focus to the `MENU` control. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-12` `constraint` The menu overlay traps focus for as long as the overlay stays open. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-13` `ui` With reduced motion, every reveal sits at the end state, the word assembled. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-14` `ui` With reduced motion, films show a still frame with a play control rather than autoplaying. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-15` `constraint` With reduced motion, the followers, drifting objects, flicker are not rendered. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-16` `constraint` The followers, the work label, the not-found letters are hidden from assistive technology. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-17` `data` Each film carries a caption track with a short text description. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-18` `ui` A skip link to the main content comes first in keyboard order on every route. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-19` `ui` Focus shows a visible outline in the ground's opposite colour on both grounds. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-20` `ui` Below the laptop breakpoint the staggered columns become one column. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-21` `ui` Below the tablet breakpoint the word `MENU` is dropped, leaving the four-dot mark. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-22` `ui` Below the phone breakpoint gallery bands go full bleed single, the footer stacks. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-23` `constraint` Body text meets the WCAG AA contrast bar of 4.5:1 on every surface. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-24` `constraint` The eyebrow on the dark ground meets the 4.5:1 contrast bar. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-25` `literal` The full-width masthead renders `Inter` at `100px`, medium. `src: UI/UX notes, type table row 1`
- [ ] `C-UX-26` `literal` The eyebrow renders `IBM Plex Mono` at `12px`, bold. `src: UI/UX notes, type table`
- [ ] `C-UX-27` `constraint` Below the laptop breakpoint the masthead drops from `100px` to `90px`. `src: UI/UX notes, type para`
- [ ] `C-UX-28` `constraint` The skip link is the first focusable element of every public route. `src: UI/UX notes, Accessibility para`
- [ ] `C-UX-29` `constraint` Nothing overflows sideways at a narrow viewport. `src: UI/UX notes, Responsive para`
- [ ] `C-UX-30` `ui` The home route shows the work beside the studio name first, with almost nothing sitting on top of them. `src: UI/UX notes, UI/UX notes para 1`
- [ ] `C-UX-31` `ui` The menu overlay opens decelerating, then closes accelerating away. `src: UI/UX notes, easing para`
- [ ] `C-UX-32` `ui` A focused booking panel service pill shows a visible focus outline distinct from the chosen pill. `src: UI/UX notes, Accessibility para`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The loading state shows the studio initial beside the initial's apostrophe, centred alone on the route's opening ground. `src: Front-end specification, loading state table`
- [ ] `C-FE-02` `literal` The hero headline reads `Not a style, a perspective.` over `Because Naught' is Everythin'.`. `src: Front-end specification, Route home band 1`
- [ ] `C-FE-03` `ui` The hero carries the one filled black pill on the site, labelled `book a call`. `src: Front-end specification, Route home band 1`
- [ ] `C-FE-04` `ui` The hero wordmark shows all seven glyphs of Naught' filling the width. `src: Front-end specification, wordmark para`
- [ ] `C-FE-05` `ui` The header mark inverts against the ground passing under the mark rather than being recoloured. `src: Front-end specification, difference composite para`
- [ ] `C-FE-06` `literal` Band 2 reads `Most brands produce content.` over `We prefer ideas.`. `src: Front-end specification, Route home band table row 2`
- [ ] `C-FE-07` `literal` Band 5 reads `Good brands communicate.` over `Great brands surprise.`. `src: Front-end specification, Route home band table row 5`
- [ ] `C-FE-08` `literal` The step aside band label reads `( The step aside )`. `src: Front-end specification, band 3 para`
- [ ] `C-FE-09` `literal` The step aside prose opens `In a world of infinite images, the rare thing is`. `src: Front-end specification, band 3 para`
- [ ] `C-FE-10` `ui` The step aside media panel runs full bleed to the right edge. `src: Front-end specification, band 3 para`
- [ ] `C-FE-11` `ui` The word `works` assembles out of five scattered letters converging into one word. `src: Front-end specification, assembling word para`
- [ ] `C-FE-12` `ui` The five assembling letters start at about a fifth of final size. `src: Front-end specification, assembling word para`
- [ ] `C-FE-13` `ui` A featured rail card shows an uppercase monospace eyebrow, a tagline, a cover. `src: Front-end specification, band 6 para`
- [ ] `C-FE-14` `ui` The featured rail cards sit in two staggered columns, the right column lower. `src: Front-end specification, band 6 para`
- [ ] `C-FE-15` `ui` The showreel grows from a framed picture on a rendered room's wall to beyond full bleed. `src: Front-end specification, scale stage para`
- [ ] `C-FE-16` `ui` The showreel band carries no caption, title or credit. `src: Front-end specification, band 7 para`
- [ ] `C-FE-17` `literal` The studio band label reads `( The Studio )`. `src: Front-end specification, band 8 para`
- [ ] `C-FE-18` `literal` The studio prose continues `an empty space open enough to become anything:`. `src: Front-end specification, band 8 para`
- [ ] `C-FE-19` `ui` The two-line block `or something` over `unexpected.` arrives late, apart from the studio prose. `src: Front-end specification, band 8 para`
- [ ] `C-FE-20` `literal` Band 9 reads `Forms follow` over `perspective.` filling the window width. `src: Front-end specification, band 9 para`
- [ ] `C-FE-21` `ui` Each of the five services sits after a circular bullet popping in as the service line reveals. `src: Front-end specification, band 9 para`
- [ ] `C-FE-22` `literal` The people heading reads `Naught' without people :`. `src: Front-end specification, band 10 para`
- [ ] `C-FE-23` `literal` The home closing line reads `Let's start` over `from naught'`. `src: Front-end specification, band 13 para`
- [ ] `C-FE-24` `ui` The home route ends on the white wordmark cropped by the document's bottom edge. `src: Front-end specification, band 13 para`
- [ ] `C-FE-25` `literal` The closing panel lists `Linkedin`, `Instagram`, `Behance` one per line. `src: Front-end specification, band 13 para`
- [ ] `C-FE-26` `constraint` A scroll-driven effect has no start event, replaying nothing on the way back. `src: Front-end specification, scrub contract para`
- [ ] `C-FE-27` `ui` The works index masthead reveals one glyph at a time, every digit, space, point included. `src: Front-end specification, Route works index para`
- [ ] `C-FE-28` `ui` The works index cards sit in two staggered columns with the gap opening down the page. `src: Front-end specification, Route works index para`
- [ ] `C-FE-29` `ui` The works index card is the same card as the home rail card. `src: Front-end specification, Route works index para`
- [ ] `C-FE-30` `ui` Over a work card the label `VIEW` grows from nothing centred on the pointer. `src: Front-end specification, work cursor para`
- [ ] `C-FE-31` `ui` A card image drifts a few pixels inside the card frame against the page. `src: Front-end specification, differential rate para`
- [ ] `C-FE-32` `ui` A route change closes a cover in the leaving route's ground, so no white flash shows. `src: Front-end specification, route cover table`
- [ ] `C-FE-33` `ui` A case study masthead shows the title on the left, `W'` with the two-digit ordinal on the right. `src: Front-end specification, Route case study table`
- [ ] `C-FE-34` `ui` The case study meta row shows the year range, then the disciplines joined by a spaced solidus. `src: Front-end specification, Route case study table`
- [ ] `C-FE-35` `literal` The concept label reads `( Concept )`. `src: Front-end specification, Route case study table`
- [ ] `C-FE-36` `constraint` A concept opens with the word `So`, closing on a short declarative line. `src: Front-end specification, Route case study table`
- [ ] `C-FE-37` `ui` The gallery bands rotate full bleed, coloured band, split, gradient band layouts. `src: Front-end specification, Route case study table`
- [ ] `C-FE-38` `literal` The all-works control reads `All Works` with a corner arrow turning right then up. `src: Front-end specification, Route case study table`
- [ ] `C-FE-39` `literal` The credits begin `Crédits :`. `src: Front-end specification, Route case study table`
- [ ] `C-FE-40` `ui` The case study closing panel centres the one-line `Let's start from naught'` above both pills. `src: Front-end specification, Route case study table`
- [ ] `C-FE-41` `ui` The compact list shows every other published case study, the current one omitted. `src: Front-end specification, Route case study table`
- [ ] `C-FE-42` `ui` The booking panel slides over the route from the right edge at the overlay layer. `src: Front-end specification, booking panel para`
- [ ] `C-FE-43` `ui` The booking panel chooses the service from five outlined pills, submitting with a `Send` pill. `src: Front-end specification, booking panel para`
- [ ] `C-FE-44` `ui` Escape closes the booking panel, returning focus to the control that opened the panel. `src: Front-end specification, booking panel para`
- [ ] `C-FE-45` `ui` The `@` after `drop us an email` is set as a mark of its own outside the label. `src: Front-end specification, closing call to action para`
- [ ] `C-FE-46` `ui` The not-found route scatters the letters of `ERROR 404` among five drifting objects. `src: Front-end specification, Route not found para`
- [ ] `C-FE-47` `ui` The not-found letters follow the pointer, reading as `ERROR 404` once the pointer moves. `src: Front-end specification, Route not found para`
- [ ] `C-FE-48` `ui` An outlined pill's border goes from partial to full strength under the pointer. `src: Front-end specification, pointer layer para`
- [ ] `C-FE-49` `ui` The menu overlay rows run works, studio, contact, the two pills, the byline, the social rail with the language chip. `src: Front-end specification, menu overlay table`
- [ ] `C-FE-50` `ui` The three large overlay rows render uppercase whatever the source case. `src: Front-end specification, menu overlay para`
- [ ] `C-FE-51` `literal` The standing byline reads `Creative studio in Milan`. `src: Front-end specification, byline para`
- [ ] `C-FE-52` `literal` The social rail short forms `LKDN`, `insta`, `BHNC` swap to `Linkedin`, `Instagram`, `Behance` on pointer entry. `src: Front-end specification, social rail para`
- [ ] `C-FE-53` `literal` The footer cells read `©24 . 26 - Founded by Lena March`, `Site by Antoine Marlet & Julien Mercer`, `Visuals by Frederic Delorme`. `src: Front-end specification, footer para`
- [ ] `C-FE-54` `ui` The footer's three cells sit on one row followed by a `Privacy` link. `src: Front-end specification, footer para`
- [ ] `C-FE-55` `literal` Menu overlay row 1 reads `works` on `/`, `home` on every other route. `src: Front-end specification, menu overlay table row 1`
- [ ] `C-FE-56` `constraint` The header mark, the menu control, the language chip, the footer are present on every route. `src: Front-end specification, chrome para`
- [ ] `C-FE-57` `literal` The language chip reads `EN`, a real control with a single option. `src: Front-end specification, language chip para`
- [ ] `C-FE-58` `constraint` The footer copyright range is stored, never computed from the clock. `src: Front-end specification, footer para`
- [ ] `C-FE-59` `ui` The sound toggle's indicator fills when sound is on, the only fill on the site signalling a state. `src: Front-end specification, sound toggle para`
- [ ] `C-FE-60` `data` Two films exist: the showreel, the manifesto film. `src: Front-end specification, Films and sound para`
- [ ] `C-FE-61` `constraint` Nothing inside the work label may be focusable. `src: Front-end specification, work cursor para`
- [ ] `C-FE-62` `ui` The header mark collapses to the `N` beside the apostrophe on the first home scroll, expanding again back at the top. `src: Front-end specification, wordmark para`
- [ ] `C-FE-63` `ui` The hero apostrophe grows from a point about the apostrophe's own position once the six letters resolve. `src: Front-end specification, wordmark para`
- [ ] `C-FE-64` `ui` On the home object field single letters follow the pointer at five rates, stringing out under a fast sweep. `src: Front-end specification, pointer layer para`
- [ ] `C-FE-65` `ui` The manifesto film band repeats `we are naught'` at the film's edges, decaying toward noise, around the centre line `We create from nothing.` `src: Front-end specification, band 12 para`
- [ ] `C-FE-66` `ui` Each drifting object on the home route grows as the object travels with the scroll. `src: Front-end specification, drifting object field para`
- [ ] `C-FE-67` `ui` A fine-grained noise overlay over the showreel band strengthens across the scale stage. `src: Front-end specification, interference overlay para`
- [ ] `C-FE-68` `ui` A studio console card reuses the works index card, adding a state label with a featured switch. `src: Front-end specification, identity routes para`
- [ ] `C-FE-69` `ui` At a narrow viewport the not-found letters tighten toward the centre. `src: Front-end specification, Route not found para`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` Signing out revokes the bearer token, ending the session. `src: Technical requirements, identity para`
- [ ] `C-TR-02` `contract` Signing in returns a bearer token, setting an HTTP-only session cookie. `src: Technical requirements, identity para`
- [ ] `C-TR-03` `constraint` Uploads accept `image/png`, `image/jpeg`, `image/webp` only. `src: Technical requirements, media para`
- [ ] `C-TR-04` `contract` A draft image requested by anyone but an author answers `404`. `src: Technical requirements, status codes para`
- [ ] `C-TR-05` `constraint` The bucket carries no anonymous read policy. `src: Technical requirements, media para`
- [ ] `C-TR-06` `contract` An unmatched path answers `404` with the not-found template as the body. `src: Technical requirements, status codes para`
- [ ] `C-TR-07` `contract` Every public route declares `og:title`, `og:image` in the head. `src: Technical requirements, social previews para`
- [ ] `C-TR-08` `contract` A case study's `og:image` is the cover's `/media/` address. `src: Technical requirements, social previews para`
- [ ] `C-TR-09` `contract` Every other route's `og:image` is `/og/<route name>.png`, generated by the application. `src: Technical requirements, social previews para`
- [ ] `C-TR-10` `constraint` Starting twice leaves one copy of every seeded row, every seeded object. `src: Technical requirements, seeding para`
- [ ] `C-TR-11` `contract` `GET /media/<storage key>` streams the object with the object's content type. `src: Technical requirements, media para`

## C-DM Data model

- [ ] `C-DM-01` `literal` The seeded services in order are `Brand identities`, `Campaigns`, `Digital experiences`, `Events`, `Visual systems`. `src: Data model, seed para`
- [ ] `C-DM-02` `literal` The seeded people are four in `founders & management`, three in `creative partners`. `src: Data model, seed para`
- [ ] `C-DM-03` `literal` The seeded settings carry the byline `Creative studio in Milan`, the contact `studio@example.com`. `src: Data model, seed para`
- [ ] `C-DM-04` `literal` The seeded case studies are `Solace`, `Urbana`, `Un_Charted`, `Kwm`, `Tactify`, `Kine`, `Chemie Union`, ordinals `1` to `7`. `src: Data model, seed table`
- [ ] `C-DM-05` `literal` The seeded `Solace` case study tagline reads `Where taste meets meaning.`. `src: Data model, seed table row 1`
- [ ] `C-DM-06` `literal` The `Solace` disciplines are `Branding`, `Packaging`, `Space design`, years `25` to `26`. `src: Data model, seed table row 1`
- [ ] `C-DM-07` `constraint` Every stored discipline of a published case study comes from `Branding`, `Webdesign`, `Development`, `Digital`, `Packaging`, `Space design`. `src: Data model, field rules table`
- [ ] `C-DM-08` `literal` The `Solace` brief opens `A Swiss specialty coffee house`. `src: Data model, seed para`
- [ ] `C-DM-09` `literal` The `Solace` concept opens `So we built taste education into the brand itself`. `src: Data model, seed para`
- [ ] `C-DM-10` `data` Each case study has one cover, four gallery images in stored order. `src: Data model, seed para`
- [ ] `C-DM-11` `literal` The `Urbana` credit carries the role `Motion & development by` before `Amelie Ronsard`. `src: Data model, credits para`
- [ ] `C-DM-12` `constraint` A gallery image layout is `full-bleed`, `coloured-band`, `split` or `gradient-band`. `src: Data model, entities para`
- [ ] `C-DM-13` `data` A stored enquiry row carries the name, the email, the company, the service, the preferred date, the time window, the message. `src: Data model, entities para`
- [ ] `C-DM-14` `data` A visitor's enquiry belongs to no account. `src: Data model, entities para`
- [ ] `C-DM-15` `constraint` An enquiry service is one of the five service labels. `src: Data model, field rules table`
- [ ] `C-DM-16` `constraint` An enquiry message holds `1` to `1000` characters. `src: Data model, field rules table`
- [ ] `C-DM-17` `constraint` A reader reads only the enquiries whose account is the reader's. `src: Data model, invariants`
- [ ] `C-DM-18` `constraint` An upload without a media description is refused; a description holds `1` to `200` characters. `src: Data model, field rules table`
- [ ] `C-DM-19` `constraint` A case study slug, ordinal are each unique. `src: Data model, field rules table`
- [ ] `C-DM-20` `constraint` The featured rail shows published, featured works in ordinal order, at most five. `src: Data model, invariants`
- [ ] `C-DM-21` `constraint` An ordinal is never reassigned by unpublishing another work. `src: Data model, invariants`
- [ ] `C-DM-22` `constraint` An enquiry status is `new`, `contacted` or `closed`. `src: Data model, entities para`
- [ ] `C-DM-23` `data` A `page_view` carries `id`, `route`, `viewed_at`. `src: Data model, entities para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The editor leftovers appear nowhere, neither a bare `000` nor an empty-collection message. `src: Constraints, constraints bullet`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` `GET /api/services` returns the services in order. `src: Deployment contract, API table`
- [ ] `C-DC-02` `contract` `GET /api/people` returns names with the group in order. `src: Deployment contract, API table`
- [ ] `C-DC-03` `contract` `GET /api/settings` returns the byline, the contact email, the stored copyright range. `src: Deployment contract, API table`
- [ ] `C-DC-04` `contract` `GET /api/health` answers `200` once the app is ready. `src: Deployment contract, contract bullet 3`
- [ ] `C-DC-05` `contract` `GET /api/works` returns published works in ordinal order to a visitor. `src: Deployment contract, API table`
- [ ] `C-DC-06` `contract` `GET /api/works/<slug>` returns the brief, the concept, the credits, the cover, the gallery. `src: Deployment contract, API table`
- [ ] `C-DC-07` `constraint` An enquiry kept in memory rather than stored is a contract violation. `src: Deployment contract, no mocks para`
- [ ] `C-DC-08` `contract` Every error body carries `error`, `field`. `src: Deployment contract, API para`
- [ ] `C-DC-09` `contract` `POST /api/auth/sign-up` creates the account, returning `role`, `token`. `src: Deployment contract, API table`
- [ ] `C-DC-10` `contract` `GET /api/enquiries` returns each reader enquiry attached to the account, newest first. `src: Deployment contract, API table`
- [ ] `C-DC-11` `contract` `POST /api/works` creates a case study as a draft, `published` false. `src: Deployment contract, API table`
- [ ] `C-DC-12` `contract` `POST /api/works/{id}/media` stores the uploaded object, returning `storage_key`, `sha256`, `url`. `src: Deployment contract, API table`
- [ ] `C-DC-13` `contract` `POST /api/works/{id}/publish` exposes the draft, returning `published` true. `src: Deployment contract, API table`
- [ ] `C-DC-14` `contract` A slug or ordinal already in use is refused with `409`. `src: Deployment contract, API table`
- [ ] `C-DC-15` `contract` `GET /api/works` includes drafts for an author, each carrying `published`. `src: Deployment contract, API table`
- [ ] `C-DC-16` `contract` `POST /api/works/{id}/unpublish` withdraws the work, returning `published` false. `src: Deployment contract, API table`
- [ ] `C-DC-17` `contract` `GET /api/enquiries` returns every enquiry newest first for an author. `src: Deployment contract, API table`
- [ ] `C-DC-18` `contract` `PATCH /api/enquiries/{id}` moves the enquiry status to `contacted` or `closed`. `src: Deployment contract, API table`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `View all` | pinned value | C-CF-02 | Core features, The home route para |
| `( 07 )` | pinned value | C-CF-02 | Core features, The home route para |
| `Works` | pinned value | C-CF-05 | Core features, The works index para |
| `©24 . 26` | pinned value | C-CF-05 | Core features, The works index para |
| `Thanks. We'll be in touch within one working day.` | pinned value | C-CF-16 | Core features, Booking a call para |
| `drop us an email` | pinned value | C-CF-17 | Core features, Booking a call para |
| `studio@example.com` | seeded account email | C-CF-17 | Core features, Booking a call para |
| `Tell us your name` | pinned value | C-CF-21 | Core features, Booking a call table row 1 |
| `We need an email to reply to` | pinned value | C-CF-23 | Core features, Booking a call table row 2 |
| `Pick a date from today on` | pinned value | C-CF-24 | Core features, Booking a call table row 5 |
| `Pick what you have in mind` | pinned value | C-CF-26 | Core features, Booking a call table row 4 |
| `morning` | pinned value | C-CF-28 | Core features, Booking a call table row 6 |
| `afternoon` | pinned value | C-CF-28 | Core features, Booking a call table row 6 |
| `Pick a time of day` | pinned value | C-CF-28 | Core features, Booking a call table row 6 |
| `1000` | pinned measure | C-CF-29 | Core features, Booking a call table row 7 |
| `Say a little about the project` | pinned value | C-CF-29 | Core features, Booking a call table row 7 |
| `80` | pinned measure | C-CF-30 | Core features, Booking a call table row 3 |
| `That company name is too long` | pinned value | C-CF-30 | Core features, Booking a call table row 3 |
| `That email is already registered` | pinned value | C-CF-32 | Core features, Identity para |
| `Veloce` | pinned value | C-CF-50 | Core features, Drafts and publication para |
| `W'08` | pinned value | C-CF-50 | Core features, Drafts and publication para |
| `Naught' to see here...` | pinned value | C-CF-71 | Core features, The not-found route para |
| `Homepage` | pinned value | C-CF-72 | Core features, The not-found route para |
| `/` | route | C-CF-72 | Core features, The not-found route para |
| `twelve months` | pinned value | C-CF-83 | Core features, The privacy page para |
| `Sending` | pinned value | C-UF-07 | User flow, States table row 2 |
| `No enquiries yet.` | pinned value | C-UF-09 | User flow, States table row 3 |
| `book a call` | pinned value | C-UF-09 | User flow, States table row 3 |
| `Inter` | pinned value | C-UX-25 | UI/UX notes, type table row 1 |
| `100px` | pinned measure | C-UX-25 | UI/UX notes, type table row 1 |
| `IBM Plex Mono` | pinned value | C-UX-26 | UI/UX notes, type table |
| `12px` | pinned measure | C-UX-26 | UI/UX notes, type table |
| `Not a style, a perspective.` | pinned value | C-FE-02 | Front-end specification, Route home band 1 |
| `Because Naught' is Everythin'.` | pinned value | C-FE-02 | Front-end specification, Route home band 1 |
| `Most brands produce content.` | pinned value | C-FE-06 | Front-end specification, Route home band table row 2 |
| `We prefer ideas.` | pinned value | C-FE-06 | Front-end specification, Route home band table row 2 |
| `Good brands communicate.` | pinned value | C-FE-07 | Front-end specification, Route home band table row 5 |
| `Great brands surprise.` | pinned value | C-FE-07 | Front-end specification, Route home band table row 5 |
| `( The step aside )` | pinned value | C-FE-08 | Front-end specification, band 3 para |
| `In a world of infinite images, the rare thing is` | pinned value | C-FE-09 | Front-end specification, band 3 para |
| `( The Studio )` | pinned value | C-FE-17 | Front-end specification, band 8 para |
| `an empty space open enough to become anything:` | pinned value | C-FE-18 | Front-end specification, band 8 para |
| `Forms follow` | pinned value | C-FE-20 | Front-end specification, band 9 para |
| `perspective.` | pinned value | C-FE-20 | Front-end specification, band 9 para |
| `Naught' without people :` | pinned value | C-FE-22 | Front-end specification, band 10 para |
| `Let's start` | pinned value | C-FE-23 | Front-end specification, band 13 para |
| `from naught'` | pinned value | C-FE-23 | Front-end specification, band 13 para |
| `Linkedin` | pinned value | C-FE-25 | Front-end specification, band 13 para |
| `Instagram` | pinned value | C-FE-25 | Front-end specification, band 13 para |
| `Behance` | pinned value | C-FE-25 | Front-end specification, band 13 para |
| `( Concept )` | pinned value | C-FE-35 | Front-end specification, Route case study table |
| `All Works` | pinned value | C-FE-38 | Front-end specification, Route case study table |
| `Crédits :` | pinned value | C-FE-39 | Front-end specification, Route case study table |
| `Creative studio in Milan` | pinned value | C-FE-51 | Front-end specification, byline para |
| `LKDN` | pinned value | C-FE-52 | Front-end specification, social rail para |
| `insta` | pinned value | C-FE-52 | Front-end specification, social rail para |
| `BHNC` | pinned value | C-FE-52 | Front-end specification, social rail para |
| `©24 . 26 - Founded by Lena March` | pinned value | C-FE-53 | Front-end specification, footer para |
| `Site by Antoine Marlet & Julien Mercer` | pinned value | C-FE-53 | Front-end specification, footer para |
| `Visuals by Frederic Delorme` | pinned value | C-FE-53 | Front-end specification, footer para |
| `works` | pinned value | C-FE-55 | Front-end specification, menu overlay table row 1 |
| `home` | pinned value | C-FE-55 | Front-end specification, menu overlay table row 1 |
| `EN` | pinned value | C-FE-57 | Front-end specification, language chip para |
| `Brand identities` | pinned value | C-DM-01 | Data model, seed para |
| `Campaigns` | pinned value | C-DM-01 | Data model, seed para |
| `Digital experiences` | pinned value | C-DM-01 | Data model, seed para |
| `Events` | pinned value | C-DM-01 | Data model, seed para |
| `Visual systems` | pinned value | C-DM-01 | Data model, seed para |
| `founders & management` | pinned value | C-DM-02 | Data model, seed para |
| `creative partners` | pinned value | C-DM-02 | Data model, seed para |
| `Solace` | pinned value | C-DM-04 | Data model, seed table |
| `Urbana` | pinned value | C-DM-04 | Data model, seed table |
| `Un_Charted` | pinned value | C-DM-04 | Data model, seed table |
| `Kwm` | pinned value | C-DM-04 | Data model, seed table |
| `Tactify` | pinned value | C-DM-04 | Data model, seed table |
| `Kine` | pinned value | C-DM-04 | Data model, seed table |
| `Chemie Union` | pinned value | C-DM-04 | Data model, seed table |
| `1` | pinned measure | C-DM-04 | Data model, seed table |
| `7` | pinned measure | C-DM-04 | Data model, seed table |
| `Where taste meets meaning.` | pinned value | C-DM-05 | Data model, seed table row 1 |
| `Branding` | pinned value | C-DM-06 | Data model, seed table row 1 |
| `Packaging` | pinned value | C-DM-06 | Data model, seed table row 1 |
| `Space design` | pinned value | C-DM-06 | Data model, seed table row 1 |
| `25` | pinned measure | C-DM-06 | Data model, seed table row 1 |
| `26` | pinned measure | C-DM-06 | Data model, seed table row 1 |
| `A Swiss specialty coffee house` | pinned value | C-DM-08 | Data model, seed para |
| `So we built taste education into the brand itself` | pinned value | C-DM-09 | Data model, seed para |
| `Motion & development by` | pinned value | C-DM-11 | Data model, credits para |
| `Amelie Ronsard` | pinned value | C-DM-11 | Data model, credits para |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the bearer token | C-TR-02 | named as the API credential with no literal format given |
| the generated stand-in images | C-CF-90 | named as generated with no literal bytes given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 1 | 1 |
| User roles | 3 | 13 |
| Core features | 21 | 91 |
| User flow | 7 | 22 |
| UI and UX notes | 2 | 32 |
| Front-end specification | 12 | 69 |
| Technical requirements | 6 | 11 |
| Data model | 5 | 23 |
| Constraints | 1 | 1 |
| Deployment contract | 9 | 18 |

