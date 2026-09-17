# Checklist: Doudou Fever

Source: instruction.md
Sections present: preamble, overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment, done
Sections absent: buildplan
Items: 1411
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` Readers pick a chapter from the record rack. `src: Overview para 2, restating the brief preamble`
- [ ] `C-OV-02` `capability` Readers read a chapter panel by panel inside one full-window drawn scene. `src: Overview para 2, restating the brief preamble`
- [ ] `C-OV-03` `capability` A verified tip lets the tipper read the next chapter before its release moment. `src: Overview para 5, restating the brief preamble`
- [ ] `C-OV-04` `constraint` An untipped reader session gets no manifest for an unreleased scheduled chapter. `src: Overview para 5, restating the brief preamble`
- [ ] `C-OV-05` `constraint` An untipped caller gets no image of an unreleased scheduled chapter. `src: Overview para 5, restating the brief preamble`
- [ ] `C-OV-06` `constraint` Early access comes only from a Tipbox notification whose signature matches the received bytes. `src: Overview para 5, restating the brief preamble`
- [ ] `C-OV-07` `contract` Every panel image lives in the object store at its key. `src: Overview para 2, restating the brief preamble`
- [ ] `C-OV-08` `capability` The comic ships in English with a French edition. `src: Overview para 1`
- [ ] `C-OV-09` `capability` The studio console lets authors create volumes holding chapters. `src: Overview para 2`
- [ ] `C-OV-10` `capability` Tips arrive in the studio supporter list. `src: Overview para 2`
- [ ] `C-OV-11` `literal` At launch the first volume `Vol. I` holds six chapters, three published, two scheduled, one draft. `src: Overview para 4`
- [ ] `C-OV-12` `literal` Every layer identifier joins chapter, board, panel numbers with a role name, as in `c1b1p1-back`. `src: Overview para 3`
- [ ] `C-OV-13` `constraint` A tip counts once when Tipbox sends the same notification twice. `src: Overview para 5`
- [ ] `C-OV-14` `constraint` A refunded tip no longer counts toward early access. `src: Overview para 5`
- [ ] `C-OV-15` `capability` Readers travel a chapter by arrow keys, the mouse wheel, dragging or the arrow controls. `src: Overview para 2`
- [ ] `C-OV-16` `constraint` No public page offers comments, a social feed, a store, a checkout, advertising or audio. `src: Overview para 6`
- [ ] `C-OV-17` `constraint` No page offers to mail a visitor a link or a notification. `src: Overview para 6`
- [ ] `C-OV-18` `constraint` The studio sign-in asks for no second factor code. `src: Overview para 6`
- [ ] `C-OV-19` `constraint` No measurement request leaves the app's own origin. `src: Overview para 6`
- [ ] `C-OV-20` `constraint` No measured event is sent about a visitor before the visitor accepts. `src: Overview para 6`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads every published chapter. `src: User roles table row 1; restated in Definition of done`
- [ ] `C-RL-02` `role` A visitor sees locked chapters with their release moments in the volume list. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A visitor opens the Tipbox page from the `support us` control. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A visitor keeps reading progress in the visitor's own browser. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` A visitor reads no scheduled chapter. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` Nobody on the public surface reads a draft chapter. `src: User roles table row 2`
- [ ] `C-RL-07` `constraint` An anonymous visitor call to a reader endpoint or a studio endpoint is denied. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A reader syncs reading progress between devices. `src: User roles table row 2`
- [ ] `C-RL-09` `role` A reader holding active early access reads a scheduled chapter inside its window. `src: User roles table row 2`
- [ ] `C-RL-10` `constraint` A reader with early access reads no scheduled chapter outside its window. `src: User roles table row 2`
- [ ] `C-RL-11` `role` A reader sets a notification preference. `src: User roles table row 2`
- [ ] `C-RL-12` `role` A reader exports the reader's own data. `src: User roles table row 2`
- [ ] `C-RL-13` `role` A reader deletes the reader's own account. `src: User roles table row 2`
- [ ] `C-RL-14` `constraint` A reader reads no other reader's progress or data. `src: User roles table row 2`
- [ ] `C-RL-15` `role` Authors import layered panel artwork into a chapter. `src: User roles table row 3`
- [ ] `C-RL-16` `role` Authors read supporter records carrying the supporter address. `src: User roles table row 3`
- [ ] `C-RL-17` `role` Authors preview any chapter, drafts included. `src: User roles table row 3`
- [ ] `C-RL-18` `constraint` No studio endpoint returns an individual reader's progress. `src: User roles table row 3`
- [ ] `C-RL-19` `constraint` A studio account cannot sign in on the reader surface. `src: User roles table row 3`
- [ ] `C-RL-20` `constraint` A reader token grants nothing on the studio surface. `src: User roles para 3`
- [ ] `C-RL-21` `constraint` An author token grants nothing on the reader `/api/me` surface. `src: User roles para 3`
- [ ] `C-RL-22` `constraint` A reader session calling an author-only endpoint is denied, leaving the protected state unchanged. `src: User roles para 2`
- [ ] `C-RL-23` `constraint` Studio content changes only through an author session. `src: User roles para 3`
- [ ] `C-RL-24` `constraint` A reader's progress, entitlements, account belong to that reader alone. `src: User roles para 3`
- [ ] `C-RL-25` `literal` Reader signup at `POST /api/auth/register` is open to anyone. `src: User roles para 3`
- [ ] `C-RL-26` `constraint` Author accounts exist only as seeded, with no author signup. `src: User roles para 3`
- [ ] `C-RL-27` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles seeded accounts`
- [ ] `C-RL-28` `literal` The seeded author accounts are `author@example.com`, Camille Rouyer, with `author2@example.com`, Damien Lorca. `src: User roles seeded accounts`
- [ ] `C-RL-29` `literal` The seeded reader accounts are `reader@example.com` with `reader2@example.com`. `src: User roles seeded accounts`
- [ ] `C-RL-30` `literal` The reader `reader@example.com` holds active early access granted by the seeded tip `tbx_seed_001`. `src: User roles seeded accounts`
- [ ] `C-RL-31` `literal` The reader `reader2@example.com` holds no entitlement, with stored progress on chapter 1 of `Vol. I`. `src: User roles seeded accounts`
- [ ] `C-RL-32` `literal` Author sign-in happens at `POST /api/studio/auth/login`, apart from reader sign-in at `POST /api/auth/login`. `src: User roles para 3`

## C-CF Core features

- [ ] `C-CF-01` `literal` `POST /api/auth/register` creates a reader account returning an `access_token`. `src: Core features, Authentication and account lifecycle rule 1`
- [ ] `C-CF-02` `literal` A new reader's `notifications` preference starts at `drops`. `src: Core features, Authentication and account lifecycle rule 1`
- [ ] `C-CF-03` `capability` Reader signup stores the optional `locale` of `en` or `fr` on the reader. `src: Core features, Authentication and account lifecycle rule 1`
- [ ] `C-CF-04` `constraint` A registration with a non-empty decoy `website` field is refused as a bot. `src: Core features, Authentication and account lifecycle rule 2`
- [ ] `C-CF-05` `constraint` A registration refused as a bot creates no account. `src: Core features, Authentication and account lifecycle rule 2`
- [ ] `C-CF-06` `constraint` The reader signup form keeps the decoy `website` field out of sight. `src: Core features, Authentication and account lifecycle rule 2`
- [ ] `C-CF-07` `literal` Signup rejects a password shorter than 12 characters naming the `password` field. `src: Core features, Authentication and account lifecycle rule 3`
- [ ] `C-CF-08` `literal` Signup rejects a malformed address naming the `email` field. `src: Core features, Authentication and account lifecycle rule 3`
- [ ] `C-CF-09` `constraint` A signup rejected for a short password or a malformed address creates nothing. `src: Core features, Authentication and account lifecycle rule 3`
- [ ] `C-CF-10` `literal` A duplicate signup address is rejected with `That address cannot be used.` `src: Core features, Authentication and account lifecycle rule 4`
- [ ] `C-CF-11` `constraint` The duplicate-address rejection never says another account holds the address. `src: Core features, Authentication and account lifecycle rule 4`
- [ ] `C-CF-12` `constraint` Signup address comparison ignores letter case. `src: Core features, Authentication and account lifecycle rule 4`
- [ ] `C-CF-13` `constraint` Changing a reader's address to an address in use gets the same rejection message. `src: Core features, Authentication and account lifecycle rule 4`
- [ ] `C-CF-14` `literal` `POST /api/auth/login` returns an `access_token` for the right password. `src: Core features, Authentication and account lifecycle rule 5`
- [ ] `C-CF-15` `constraint` A wrong password gets the same status, error code with message as an unknown address. `src: Core features, Authentication and account lifecycle rule 5`
- [ ] `C-CF-16` `literal` After `10` consecutive failed sign-ins for one address within an hour, sign-in keeps failing for `15` minutes. `src: Core features, Authentication and account lifecycle rule 6`
- [ ] `C-CF-17` `constraint` A locked-out address fails sign-in even with the right password. `src: Core features, Authentication and account lifecycle rule 6`
- [ ] `C-CF-18` `constraint` A locked-out sign-in gets the same response as a wrong password. `src: Core features, Authentication and account lifecycle rule 6`
- [ ] `C-CF-19` `constraint` Author sign-in follows the same lockout rule as reader sign-in. `src: Core features, Authentication and account lifecycle rule 6`
- [ ] `C-CF-20` `literal` `POST /api/auth/logout` ends the session so the token no longer works on any endpoint. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-21` `constraint` A reader session ends 90 days after the most recent authenticated request. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-22` `constraint` An author session ends 2 hours after the most recent authenticated request. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-23` `constraint` An author session never lasts past 12 hours after sign-in. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-24` `literal` During a live session, the session row's `expires_at` holds the moment the session ends. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-25` `constraint` After a session ends, an endpoint that needs a session denies the session token. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-26` `constraint` After a session ends, an endpoint open to visitors answers a request carrying the session token as a visitor request. `src: Core features, Authentication and account lifecycle rule 7`
- [ ] `C-CF-27` `constraint` Passwords are stored hashed, never as the typed text. `src: Core features, Authentication and account lifecycle rule 8`
- [ ] `C-CF-28` `constraint` A session token is never stored as issued. `src: Core features, Authentication and account lifecycle rule 8`
- [ ] `C-CF-29` `literal` An author signs in at `POST /api/studio/auth/login`. `src: Core features, Authentication and account lifecycle rule 9`
- [ ] `C-CF-30` `constraint` A reader token is refused on every `/api/studio` endpoint. `src: Core features, Authentication and account lifecycle rule 9`
- [ ] `C-CF-31` `constraint` An author token is refused on every `/api/me` endpoint. `src: Core features, Authentication and account lifecycle rule 9`
- [ ] `C-CF-32` `constraint` An anonymous call to any `/api/me` or `/api/studio` endpoint is denied. `src: Core features, Authentication and account lifecycle rule 9`
- [ ] `C-CF-33` `constraint` The app offers no password reset. `src: Core features, Authentication and account lifecycle rule 10`
- [ ] `C-CF-34` `constraint` The app offers no passwordless link. `src: Core features, Authentication and account lifecycle rule 10`
- [ ] `C-CF-35` `literal` The reader signup form has `email` with `password` fields plus a `create account` button. `src: Core features, Authentication and account lifecycle rule 11`
- [ ] `C-CF-36` `constraint` The reader sign-in dialog asks for no second factor code. `src: Core features, Authentication and account lifecycle rule 10`
- [ ] `C-CF-37` `literal` The reader sign-in dialog is named `sign in`. `src: Core features, Authentication and account lifecycle rule 11`
- [ ] `C-CF-38` `literal` The reader sign-in dialog has an `email` field, a `password` field with a `sign in` button. `src: Core features, Authentication and account lifecycle rule 11`
- [ ] `C-CF-39` `capability` The `create an account` control turns the sign-in dialog into the signup form. `src: Core features, Authentication and account lifecycle rule 11`
- [ ] `C-CF-40` `literal` The studio sign-in page at `/studio/sign-in` has `email` with `password` fields plus a `sign in` button. `src: Core features, Authentication and account lifecycle rule 11`
- [ ] `C-CF-41` `literal` The public routes `/`, `/chapters`, `/chapter/:id`, `/about`, `/legal`, `/support/return`, `/account` answer. `src: Core features, The reading surface rule 1`
- [ ] `C-CF-42` `literal` Every public route repeats for French under `/fr` with the same untranslated path segments. `src: Core features, The reading surface rule 1`
- [ ] `C-CF-43` `literal` Chapters of the first volume live at `/chapter/:id`. `src: Core features, The reading surface rule 1`
- [ ] `C-CF-44` `literal` Chapters of a later volume live at `/volumes/:volume/chapter/:id`, where `:volume` is the volume order. `src: Core features, The reading surface rule 1`
- [ ] `C-CF-45` `capability` Every public route renders inside one persistent shell with one canvas filling the window. `src: Core features, The reading surface rule 2`
- [ ] `C-CF-46` `capability` The shell around the canvas carries the header, footer link, language selector, fullscreen control, consent strip. `src: Core features, The reading surface rule 2`
- [ ] `C-CF-47` `capability` The canvas is created once for the life of the page, surviving every in-app navigation. `src: Core features, The reading surface rule 2`
- [ ] `C-CF-48` `constraint` In-app navigation never reloads the document. `src: Core features, The reading surface rule 2; restated in Definition of done`
- [ ] `C-CF-49` `capability` The first HTML response of every public route carries the route's own title element. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-50` `capability` The first HTML response of every public route carries the route's own meta description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-51` `literal` The first HTML response carries an `<html lang>` of `en` or `fr` naming the route's locale. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-52` `constraint` No two routes in one locale share a title or a description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-53` `capability` The `/` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-54` `capability` The `/` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-55` `capability` The `/chapters` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-56` `capability` The `/chapters` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-57` `capability` The `/chapter/1` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-58` `capability` The `/chapter/1` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-59` `capability` The `/about` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-60` `capability` The `/about` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-61` `capability` The `/legal` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-62` `capability` The `/legal` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-63` `capability` The `/support/return` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-64` `capability` The `/support/return` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-65` `capability` The `/account` document carries the pinned English title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-66` `capability` The `/account` document carries the pinned English description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-67` `capability` The English not-found document carries the pinned title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-68` `capability` The English not-found document carries the pinned description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-69` `literal` English chapter documents follow the title pattern `Chapter #<n>: <Title With Each Word Capitalised> - Doudou Fever - Interactive Comic`. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-70` `literal` English chapter documents follow the description pattern `Read chapter <n>, <title>, of the Doudou Fever interactive comic.` `src: Core features, The reading surface rule 3`
- [ ] `C-CF-71` `capability` The `/fr` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-72` `capability` The `/fr` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-73` `capability` The `/fr/chapters` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-74` `capability` The `/fr/chapters` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-75` `capability` The `/fr/chapter/1` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-76` `capability` The `/fr/chapter/1` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-77` `capability` The `/fr/about` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-78` `capability` The `/fr/about` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-79` `capability` The `/fr/legal` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-80` `capability` The `/fr/legal` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-81` `capability` The `/fr/support/return` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-82` `capability` The `/fr/support/return` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-83` `capability` The `/fr/account` document carries the pinned French title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-84` `capability` The `/fr/account` document carries the pinned French description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-85` `capability` The French not-found document carries the pinned title. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-86` `capability` The French not-found document carries the pinned description. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-87` `literal` French chapter documents follow the title pattern `Chapitre #<n> : <Titre Avec Chaque Mot En Capitale> - Doudou Fever - BD interactive`. `src: Core features, The reading surface rule 3`
- [ ] `C-CF-88` `literal` French chapter documents follow the description pattern `Lis le chapitre <n>, <titre>, de la BD interactive Doudou Fever.` `src: Core features, The reading surface rule 3`
- [ ] `C-CF-89` `literal` The title screen at `/` shows one entry button `read now`. `src: Core features, The reading surface rule 4`
- [ ] `C-CF-90` `capability` The `read now` button opens `/chapters`. `src: Core features, The reading surface rule 4`
- [ ] `C-CF-91` `literal` The title screen carries the heading `Doudou Fever` for assistive technology. `src: Core features, The reading surface rule 4`
- [ ] `C-CF-92` `literal` The title screen carries the credit line `By Damien Lorca & Camille Rouyer` for assistive technology. `src: Core features, The reading surface rule 4`
- [ ] `C-CF-93` `ui` A slowly spinning record sits above the centre of the title screen. `src: Core features, The reading surface rule 4`
- [ ] `C-CF-94` `capability` Clicking the title-screen record starts the surprise. `src: Core features, The reading surface rule 4`
- [ ] `C-CF-95` `literal` The rack at `/chapters` carries the heading `select a chapter`. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-96` `capability` The rack shows one sleeve per published, scheduled or unpublished chapter of every volume. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-97` `constraint` A draft chapter has no sleeve on the rack. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-98` `literal` An open sleeve title joins the two-digit number, a full stop, the title with no space, as in `01.welcome to Varny`. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-99` `literal` A sleeve subtitle joins the brand to the volume label with no space, as in `Doudou FeverVol. I`. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-100` `literal` A sleeve timecode shows the two-digit chapter number beside the two-digit chapter count of its volume, as in `01:06`. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-101` `constraint` The sleeve timecode count includes every chapter that exists, drafts included. `src: Core features, The reading surface rule 5`
- [ ] `C-CF-102` `literal` An open sleeve timecode is announced as `chapter 1 of 6`. `src: Core features, The reading surface rule 6`
- [ ] `C-CF-103` `capability` A sleeve the caller may not read shows a padlock in place of the play symbol. `src: Core features, The reading surface rule 6`
- [ ] `C-CF-104` `constraint` Neither the icon nor the text of a locked sleeve is a link. `src: Core features, The reading surface rule 6`
- [ ] `C-CF-105` `capability` A locked sleeve with a release moment is named by the `chapters.locked_name` pattern, the title, the word locked, then when the chapter opens. `src: Core features, The reading surface rule 6`
- [ ] `C-CF-106` `literal` An unpublished chapter's sleeve is named `<title>, locked`. `src: Core features, The reading surface rule 6`
- [ ] `C-CF-107` `capability` The rack is a keyboard listbox where arrow keys move the selection. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-108` `capability` Enter opens the selected chapter from the rack. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-109` `capability` Home or End jumps to the matching end of the rack. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-110` `capability` The mouse wheel moves the rack selection. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-111` `capability` Dragging the rack moves the rack selection. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-112` `capability` The two small arrows on a sleeve move the rack selection. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-113` `capability` The rack settles on the nearest sleeve. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-114` `capability` The rack opens with the last opened chapter's sleeve selected. `src: Core features, The reading surface rule 7`
- [ ] `C-CF-115` `capability` A chapter the caller may read opens the reader. `src: Core features, The reading surface rule 8`
- [ ] `C-CF-116` `literal` During chapter loading the caption `Next track is loading...` sits over a slow charcoal gradient. `src: Core features, The reading surface rule 8`
- [ ] `C-CF-117` `literal` The loading name line reads `01. welcome to Varny`, with a space after the full stop. `src: Core features, The reading surface rule 8`
- [ ] `C-CF-118` `capability` The reader draws each panel in the canvas from the panel's layers at their depths. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-119` `literal` The reader canvas carries `role="img"` with an accessible name naming the chapter. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-120` `capability` The right or up arrow key moves the reader view forward one panel. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-121` `capability` The left or down arrow key moves the reader view back one panel. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-122` `capability` Scrolling the mouse wheel down moves the reader forward along the chapter. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-123` `capability` Dragging moves the reader along the chapter. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-124` `data` Each manifest layer carries a base `opacity` property. `src: Core features, The reading surface rule 9`
- [ ] `C-CF-125` `capability` A timeline capsule at the bottom of the reader shows the chapter cover. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-126` `capability` The timeline capsule shows the chapter title. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-127` `literal` The timeline capsule shows the subtitle `Doudou FeverVol. I`. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-128` `literal` The capsule timecode joins the two-digit chapter number to the two-digit panel number across the whole chapter, as in `01:01`. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-129` `literal` The capsule timecode is announced as `panel 1`. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-130` `literal` The capsule progress track is a slider named `chapter progress` running from `0` to `100`. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-131` `capability` Pressing a point on the progress slider moves the reader view there. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-132` `capability` The progress slider's arrow or page keys move the reader view. `src: Core features, The reading surface rule 10`
- [ ] `C-CF-133` `literal` Controls named `previous panel` with `next panel` step the reader view. `src: Core features, The reading surface rule 11`
- [ ] `C-CF-134` `constraint` On the first panel the `previous panel` control is disabled. `src: Core features, The reading surface rule 11`
- [ ] `C-CF-135` `capability` Reaching the last panel slides a next-track face across the capsule. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-136` `literal` The next-track face shows the label `next track`. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-137` `literal` The next-track face repeats the next chapter title four times, each copy followed by ` _ `. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-138` `capability` The next-track face is a link to the next chapter. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-139` `constraint` Following the next-track face changes chapter without reloading the document. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-140` `constraint` The last chapter of a volume shows no next-track face. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-141` `capability` The last chapter of a volume offers the one line `last track of the volume, back to chapters`, leading to the rack. `src: Core features, The reading surface rule 12`
- [ ] `C-CF-142` `literal` A `read as text` control switches the reader to text mode. `src: Core features, The reading surface rule 13`
- [ ] `C-CF-143` `capability` Text mode shows the chapter as an ordered list of panel descriptions in reading order. `src: Core features, The reading surface rule 13`
- [ ] `C-CF-144` `capability` Text mode uses the current page language. `src: Core features, The reading surface rule 13`
- [ ] `C-CF-145` `literal` Local storage key `dd-last-chapter` holds the volume order with chapter number, as in `1/2`. `src: Core features, The reading surface rule 14`
- [ ] `C-CF-146` `literal` Local storage key `dd-progress-<volume>-<chapter>` holds a fraction from `0` to `1`, as in `0.400`. `src: Core features, The reading surface rule 14`
- [ ] `C-CF-147` `constraint` The local storage progress fraction has at most three decimals. `src: Core features, The reading surface rule 14`
- [ ] `C-CF-148` `constraint` Reading progress is written to local storage at most once per second. `src: Core features, The reading surface rule 14`
- [ ] `C-CF-149` `literal` A chapter that exists but is not readable renders the locked state at status `200`. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-150` `literal` The locked state shows the name line, as in `04. scratch that !`. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-151` `capability` The locked state shows the `locked.timing` opening line with the release date as day, month name, year. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-152` `literal` The locked state offers a `notify me` control. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-153` `literal` The locked state offers a `support us` control. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-154` `capability` The locked state shows the `locked.support` supporters line beside the `support us` control. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-155` `capability` The locked state shows the previous chapter's sleeve as a way back. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-156` `capability` The locked release date follows the page language in the reader's own time zone. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-157` `capability` A draft chapter's locked state shows the `locked.drawing` still-being-drawn line in place of the opening line. `src: Core features, The reading surface rule 15`
- [ ] `C-CF-158` `capability` The `notify me` control opens the reader sign-in dialog. `src: Core features, The reading surface rule 16`
- [ ] `C-CF-159` `literal` Once signed in, `notify me` records the drop wish through `POST /api/me/notify`. `src: Core features, The reading surface rule 16`
- [ ] `C-CF-160` `literal` `POST /api/me/notify` leaves `notifications` at `drops` or `all`. `src: Core features, The reading surface rule 16`
- [ ] `C-CF-161` `capability` When the signed-in reader may now read the chapter, the reader opens in place. `src: Core features, The reading surface rule 16`
- [ ] `C-CF-162` `literal` A chapter id that is not a positive integer renders the not-found page with `404`. `src: Core features, The reading surface rule 17`
- [ ] `C-CF-163` `literal` A chapter id above the chapter count of its volume renders the not-found page with `404`. `src: Core features, The reading surface rule 17`
- [ ] `C-CF-164` `literal` A volume order that does not exist renders the not-found page with `404`. `src: Core features, The reading surface rule 17`
- [ ] `C-CF-165` `literal` An unpublished chapter's page answers a temporary redirect to `/chapters`, or `/fr/chapters` in French. `src: Core features, The reading surface rule 17`
- [ ] `C-CF-166` `literal` A readable chapter renders the reader with `200`. `src: Core features, The reading surface rule 17`
- [ ] `C-CF-167` `constraint` The chapter route ladder applies not-found first, then redirect, then locked, then the reader. `src: Core features, The reading surface rule 17`
- [ ] `C-CF-168` `literal` Any other path renders the not-found page with `404`. `src: Core features, The reading surface rule 18`
- [ ] `C-CF-169` `literal` The not-found page shows the line `Oopsy, page not found`. `src: Core features, The reading surface rule 18`
- [ ] `C-CF-170` `literal` The not-found page offers a `Go back to home` control leading to `/`. `src: Core features, The reading surface rule 18`
- [ ] `C-CF-171` `constraint` The not-found page requests no chapter manifest, no panel image. `src: Core features, The reading surface rule 18`
- [ ] `C-CF-172` `constraint` The not-found page draws no scene. `src: Core features, The reading surface rule 18`
- [ ] `C-CF-173` `capability` A panel whose layer image fails to load renders without that layer, reading on. `src: Core features, The reading surface rule 19`
- [ ] `C-CF-174` `literal` A chapter that fails to load shows `Something went missing. Try again?`. `src: Core features, The reading surface rule 19`
- [ ] `C-CF-175` `literal` The failed-load state offers `try again`, which retries without reloading the document. `src: Core features, The reading surface rule 19`
- [ ] `C-CF-176` `literal` The failed-load state offers `back to chapters`. `src: Core features, The reading surface rule 19`
- [ ] `C-CF-177` `capability` Without a canvas drawing context every route still works as a plain readable site. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-178` `capability` Without a drawing context the title screen shows the heading with the credit line. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-179` `capability` Without a drawing context the rack lists every readable chapter as an ordinary link. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-180` `capability` Without a drawing context the rack lists every locked chapter as plain text. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-181` `capability` Without a drawing context a chapter opens in text mode. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-182` `capability` Without a drawing context the about page shows the about text. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-183` `capability` Without a drawing context the legal page shows the legal text. `src: Core features, The reading surface rule 20`
- [ ] `C-CF-184` `literal` The persistent tip control `support us` sits on the rack. `src: Core features, The reading surface rule 21`
- [ ] `C-CF-185` `capability` The `support us` tip link sits in the reader. `src: Core features, The reading surface rule 21`
- [ ] `C-CF-186` `literal` The tip control links to `https://tipbox.example/doudou-fever`. `src: Core features, The reading surface rule 21`
- [ ] `C-CF-187` `literal` The tip link carries a `return_token` query parameter issued for the visit. `src: Core features, The reading surface rule 21`
- [ ] `C-CF-188` `literal` The support tip link opens with `target="_blank"`. `src: Core features, The reading surface rule 21`
- [ ] `C-CF-189` `literal` The support tip link `rel` holds both `noopener` plus `noreferrer`. `src: Core features, The reading surface rule 21`
- [ ] `C-CF-190` `capability` The `/account` page shows a signed-in reader's address, language, notification preference. `src: Core features, The reading surface rule 22`
- [ ] `C-CF-191` `capability` The `/account` page changes the reader's address, language or notification preference. `src: Core features, The reading surface rule 22`
- [ ] `C-CF-192` `literal` The `/account` page offers the export control `download my data`. `src: Core features, The reading surface rule 22`
- [ ] `C-CF-193` `literal` The `/account` page offers `delete my account`. `src: Core features, The reading surface rule 22`
- [ ] `C-CF-194` `capability` A signed-out visitor opening `/account` gets the reader sign-in dialog over the rack. `src: Core features, The reading surface rule 22`
- [ ] `C-CF-195` `capability` A published chapter is readable by every caller. `src: Core features, Who may read a chapter rule 1`
- [ ] `C-CF-196` `literal` A scheduled chapter is readable from its release moment minus `early_access_days` by a reader holding active early access. `src: Core features, Who may read a chapter rule 1`
- [ ] `C-CF-197` `constraint` An expired early access opens no scheduled chapter. `src: Core features, Who may read a chapter rule 1`
- [ ] `C-CF-198` `constraint` A revoked early access opens no scheduled chapter. `src: Core features, Who may read a chapter rule 1`
- [ ] `C-CF-199` `constraint` A revoked or expired early access takes effect on the reader's very next request. `src: Core features, Who may read a chapter rule 2`
- [ ] `C-CF-200` `constraint` No other state or caller makes a chapter readable on the public surface. `src: Core features, Who may read a chapter rule 1`
- [ ] `C-CF-201` `constraint` Readability is evaluated on the server from the chapter's current state on every request. `src: Core features, Who may read a chapter rule 2`
- [ ] `C-CF-202` `literal` `GET /api/volumes/{order}/chapters/{number}` returns the manifest of a readable chapter. `src: Core features, Who may read a chapter rule 3`
- [ ] `C-CF-203` `literal` The manifest endpoint answers `404` for a chapter the caller may not read. `src: Core features, Who may read a chapter rule 3; restated in Definition of done`
- [ ] `C-CF-204` `constraint` The manifest endpoint never answers `403` for an unreadable chapter. `src: Core features, Who may read a chapter rule 3`
- [ ] `C-CF-205` `literal` The manifest endpoint answers `404` for a chapter that does not exist. `src: Core features, Who may read a chapter rule 3`
- [ ] `C-CF-206` `data` A manifest `total` is the number of chapters in the chapter's volume. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-207` `data` Each manifest panel `index` is the panel's 1-based position across the whole chapter. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-208` `literal` A published manifest gives each layer image the address `/api/textures/v<asset_version>/<volume order>/<chapter number>/<file identifier>.png?tag=<content tag>`. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-209` `data` A `sprite` manifest layer carries `frame_table_url` at `/api/textures/v<asset_version>/<volume order>/<chapter number>/<file identifier>.json?tag=<content tag>`. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-210` `constraint` A frame table address follows the same signing rules as the layer image address, with `expires` plus `sig` when unpublished. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-211` `data` Every other manifest layer carries `frame_table_url` as null. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-212` `literal` A readable unpublished chapter's image addresses carry `expires` with `sig` query parameters. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-213` `literal` A signed image address stays valid for `15` minutes. `src: Core features, Who may read a chapter rule 4`
- [ ] `C-CF-214` `literal` An unpublished chapter's image requested without `sig` answers `404`. `src: Core features, Who may read a chapter rule 5; restated in Definition of done`
- [ ] `C-CF-215` `literal` An unpublished chapter's image requested with a mismatched `sig` answers `404`. `src: Core features, Who may read a chapter rule 5`
- [ ] `C-CF-216` `literal` An unpublished chapter's image requested after `expires` answers `404`. `src: Core features, Who may read a chapter rule 5`
- [ ] `C-CF-217` `constraint` An image of a published chapter needs no signature. `src: Core features, Who may read a chapter rule 5`
- [ ] `C-CF-218` `literal` `GET /api/volumes` lists every volume with the volume's chapters for the caller. `src: Core features, Who may read a chapter rule 6`
- [ ] `C-CF-219` `literal` The volume list marks each chapter `locked` or open from the readability rule. `src: Core features, Who may read a chapter rule 6`
- [ ] `C-CF-220` `constraint` A draft chapter is never listed in the volume list. `src: Core features, Who may read a chapter rule 6`
- [ ] `C-CF-221` `capability` The volume list shows each chapter title with release moment publicly. `src: Core features, Who may read a chapter rule 6`
- [ ] `C-CF-222` `literal` Covers at `/api/covers/<volume order>/<chapter number>.png` are public for published chapters. `src: Core features, Who may read a chapter rule 7`
- [ ] `C-CF-223` `capability` Covers are public for scheduled chapters. `src: Core features, Who may read a chapter rule 7`
- [ ] `C-CF-224` `literal` A draft chapter's cover answers `404`. `src: Core features, Who may read a chapter rule 7`
- [ ] `C-CF-225` `literal` `/sitemap.xml` lists the English static public routes with every published chapter address. `src: Core features, Who may read a chapter rule 8`
- [ ] `C-CF-226` `literal` `/fr/sitemap.xml` lists the French static public routes with every published chapter address. `src: Core features, Who may read a chapter rule 8`
- [ ] `C-CF-227` `constraint` The sitemaps never list a scheduled, draft or unpublished chapter. `src: Core features, Who may read a chapter rule 8`
- [ ] `C-CF-228` `constraint` Every image object in the bucket refuses a request made without credentials. `src: Core features, Who may read a chapter rule 9`
- [ ] `C-CF-229` `constraint` Readers receive image objects only through the app, never anonymously from the store. `src: Core features, Who may read a chapter rule 9`
- [ ] `C-CF-230` `literal` `POST /api/tips/return-tokens` issues a return token valid for `24` hours. `src: Core features, Tips and early access rule 1`
- [ ] `C-CF-231` `constraint` A return token is claimed by one reader only. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-232` `constraint` Another reader's claim of an already claimed return token is rejected. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-233` `literal` Without a reader session `POST /api/tips/return` answers the status `sign_in_required`. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-234` `literal` The tip return status is `granted` when a tip carrying the token arrived granting early access. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-235` `literal` The tip return status is `below_threshold` when a tip carrying the token arrived below the threshold. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-236` `literal` The tip return status is `pending` when no tip carrying the token has arrived. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-237` `literal` The tip return page reads the return token from `/support/return?token=<token>`. `src: Core features, Tips and early access rule 1`
- [ ] `C-CF-238` `capability` Without a reader session the return page shows the `support.sign_in` thank-you line with the sign-in dialog. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-239` `capability` The return page shows the `support.granted`, `support.below_threshold` or `support.pending` thank-you line matching each tip return status. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-240` `constraint` An unknown return token is rejected. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-241` `constraint` An expired return token is rejected. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-242` `capability` For a rejected return token the return page shows the `support.expired` expired-link line. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-243` `constraint` A return token never grants anything by itself. `src: Core features, Tips and early access rule 2`
- [ ] `C-CF-244` `literal` Tipbox notifications arrive at `POST /api/webhooks/tipbox`. `src: Core features, Tips and early access rule 3`
- [ ] `C-CF-245` `literal` The studio's Tipbox signing secret is `tbx_whsec_5f3a9c2e81d7`. `src: Core features, Tips and early access rule 3`
- [ ] `C-CF-246` `literal` The `Tipbox-Signature` header carries `t=<unix seconds>,v1=<signature>`. `src: Core features, Tips and early access rule 3`
- [ ] `C-CF-247` `capability` The Tipbox signature is the lowercase hexadecimal HMAC-SHA256 of the timestamp, a full stop, the raw body bytes. `src: Core features, Tips and early access rule 3`
- [ ] `C-CF-248` `literal` A Tipbox notification whose signature does not match the exact bytes answers `401`. `src: Core features, Tips and early access rule 4`
- [ ] `C-CF-249` `constraint` A notification body changed by a single space after signing fails the signature. `src: Core features, Tips and early access rule 4`
- [ ] `C-CF-250` `literal` A notification timestamp more than `300` seconds from the server clock answers `401`. `src: Core features, Tips and early access rule 4`
- [ ] `C-CF-251` `data` A refused notification is recorded with `signature_verified` false. `src: Core features, Tips and early access rule 4`
- [ ] `C-CF-252` `constraint` A refused notification changes nothing else. `src: Core features, Tips and early access rule 4`
- [ ] `C-CF-253` `literal` A verified notification is recorded, then answered `200`. `src: Core features, Tips and early access rule 5`
- [ ] `C-CF-254` `constraint` A notification whose event `id` was already verified answers `200`, doing nothing a second time. `src: Core features, Tips and early access rule 5`
- [ ] `C-CF-255` `literal` A verified notification's effects appear within `30` seconds of the `200`. `src: Core features, Tips and early access rule 5`
- [ ] `C-CF-256` `data` A notification body carries `id`, `type`, `created` with `data`. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-257` `literal` A notification `type` is `tip.received`, `tip.refunded` or `tip.disputed`. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-258` `constraint` A verified notification of any other `type` answers `200`, changing nothing. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-259` `data` A `tip.received` notification's `data` carries `tip_id`, `amount`, `currency`, `settled_amount`, `rate`, `supporter_email`, `message`, `return_token`. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-260` `literal` A tip's currency arrives lowercase, as in `eur`, with the settled amount already in `usd`. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-261` `literal` A received tip's rate arrives as decimal text, as in `1.087500`. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-262` `data` A tip keeps the original amount with currency exactly as received. `src: Core features, Tips and early access rule 7`
- [ ] `C-CF-263` `data` A tip keeps the settled amount with rate exactly as received. `src: Core features, Tips and early access rule 7`
- [ ] `C-CF-264` `constraint` The settled amount is never recomputed. `src: Core features, Tips and early access rule 7`
- [ ] `C-CF-265` `constraint` Each tip is stored as one row per Tipbox `tip_id`, however many deliveries arrive. `src: Core features, Tips and early access rule 7`
- [ ] `C-CF-266` `constraint` Concurrent deliveries of one `tip_id` store one tip. `src: Core features, Tips and early access rule 7`
- [ ] `C-CF-267` `literal` A tip matches first the reader who claimed the tip's `return_token`, with method `token`. `src: Core features, Tips and early access rule 8`
- [ ] `C-CF-268` `constraint` Token matching holds whether the claim came before or after the tip. `src: Core features, Tips and early access rule 8`
- [ ] `C-CF-269` `literal` Failing a token match, a tip matches a reader whose address equals `supporter_email` ignoring case, with method `address`. `src: Core features, Tips and early access rule 8`
- [ ] `C-CF-270` `constraint` An address match grants nothing until an author confirms the match. `src: Core features, Tips and early access rule 8`
- [ ] `C-CF-271` `literal` A tip matched by address then confirmed by an author grants `early_access` at or above the `early_access_threshold`, seeded `500`. `src: Core features, Tips and early access rule 9`
- [ ] `C-CF-272` `literal` A tip matching nobody has method `none`. `src: Core features, Tips and early access rule 8`
- [ ] `C-CF-273` `literal` A token-matched tip settling at or above the `early_access_threshold`, seeded `500`, grants an `early_access` entitlement. `src: Core features, Tips and early access rule 9; restated in Definition of done`
- [ ] `C-CF-274` `literal` A tip settling at or above the `credit_threshold`, seeded `2000`, also grants a `credits` entitlement with no expiry. `src: Core features, Tips and early access rule 9`
- [ ] `C-CF-275` `constraint` A tip settling below the `early_access_threshold`, seeded `500`, grants nothing. `src: Core features, Tips and early access rule 9`
- [ ] `C-CF-276` `literal` An `early_access` entitlement expires `12` calendar months after the grant. `src: Core features, Tips and early access rule 9`
- [ ] `C-CF-277` `literal` A refund notification `tip.refunded` sets the tip state to `refunded`. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-278` `constraint` A refund revokes the entitlements the tip granted. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-279` `constraint` A refund or dispute revocation closes early access from the next request on. `src: Core features, Tips and early access rule 10; restated in Definition of done`
- [ ] `C-CF-280` `constraint` A refund or dispute revocation never removes what was already read, keeping reading progress. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-281` `literal` A dispute notification `tip.disputed` sets the tip state to `disputed`. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-282` `constraint` A dispute revokes the entitlements the tip granted. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-283` `data` A `tip.refunded` or `tip.disputed` notification's `data` carries `tip_id`. `src: Core features, Tips and early access rule 6`
- [ ] `C-CF-284` `constraint` Early access stands after a refund or dispute when the reader holds another received tip at or above the threshold. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-285` `capability` Each revocation appears on the studio overview. `src: Core features, Tips and early access rule 10`
- [ ] `C-CF-286` `constraint` A refund for a `tip_id` that has not arrived creates that tip in the refunded state. `src: Core features, Tips and early access rule 11`
- [ ] `C-CF-287` `constraint` A dispute for a `tip_id` that has not arrived creates that tip in the disputed state. `src: Core features, Tips and early access rule 11`
- [ ] `C-CF-288` `constraint` A tip arriving after its refund or dispute fills in the amounts, granting nothing. `src: Core features, Tips and early access rule 11`
- [ ] `C-CF-289` `capability` Every seeded or received tip appears in the studio supporter list. `src: Core features, Tips and early access rule 12`
- [ ] `C-CF-290` `literal` The seeded tip `tbx_seed_001`, settled `800`, grants the early access of `reader@example.com`. `src: Core features, Tips and early access rule 12`
- [ ] `C-CF-291` `literal` `GET /api/me/progress` returns the signed-in reader's whole progress document. `src: Core features, Reading progress synchronisation across devices rule 1`
- [ ] `C-CF-292` `literal` `PUT /api/me/progress` takes one whole progress document. `src: Core features, Reading progress synchronisation across devices rule 1`
- [ ] `C-CF-293` `data` The progress document carries `last_chapter`, a volume with chapter, or null. `src: Core features, Reading progress synchronisation across devices rule 1`
- [ ] `C-CF-294` `data` The progress document carries `last_chapter_at`. `src: Core features, Reading progress synchronisation across devices rule 1`
- [ ] `C-CF-295` `data` Each progress `chapters` entry carries `volume`, `chapter`, `fraction`, `last_panel`. `src: Core features, Reading progress synchronisation across devices rule 1`
- [ ] `C-CF-296` `capability` A progress `PUT` merges with the stored progress, returning the merged document. `src: Core features, Reading progress synchronisation across devices rule 2`
- [ ] `C-CF-297` `constraint` For each chapter the greater progress `fraction` wins. `src: Core features, Reading progress synchronisation across devices rule 2`
- [ ] `C-CF-298` `constraint` Where progress fractions are equal the greater `last_panel` wins. `src: Core features, Reading progress synchronisation across devices rule 2`
- [ ] `C-CF-299` `constraint` The merged `last_chapter` comes from the progress document with the later `last_chapter_at`. `src: Core features, Reading progress synchronisation across devices rule 2`
- [ ] `C-CF-300` `constraint` A progress entry for a chapter that does not exist is dropped. `src: Core features, Reading progress synchronisation across devices rule 2`
- [ ] `C-CF-301` `constraint` Two devices syncing progress in either order end with the same progress document. `src: Core features, Reading progress synchronisation across devices rule 3`
- [ ] `C-CF-302` `constraint` Sending the same progress document twice changes nothing. `src: Core features, Reading progress synchronisation across devices rule 3`
- [ ] `C-CF-303` `constraint` A reader never loses a progress position by syncing. `src: Core features, Reading progress synchronisation across devices rule 3`
- [ ] `C-CF-304` `constraint` A progress `fraction` outside `0` to `1` rejects the whole request, writing nothing. `src: Core features, Reading progress synchronisation across devices rule 4`
- [ ] `C-CF-305` `constraint` A progress `fraction` with more than three decimals rejects the whole request. `src: Core features, Reading progress synchronisation across devices rule 4`
- [ ] `C-CF-306` `capability` When a visitor signs in, the browser progress is uploaded then merged, never discarded. `src: Core features, Reading progress synchronisation across devices rule 5`
- [ ] `C-CF-307` `constraint` Signing out keeps the browser progress. `src: Core features, Reading progress synchronisation across devices rule 5`
- [ ] `C-CF-308` `constraint` No studio endpoint returns an individual reader's sessions. `src: Core features, Reading progress synchronisation across devices rule 6`
- [ ] `C-CF-309` `constraint` A reader's address reaches the studio only as the `matched_reader_email` of a tip matched to that reader. `src: Core features, Reading progress synchronisation across devices rule 6`
- [ ] `C-CF-310` `constraint` The studio sees reader progress as counts only. `src: Core features, Reading progress synchronisation across devices rule 6`
- [ ] `C-CF-311` `literal` `GET /api/me/export` returns the reader's own data as a JSON attachment. `src: Core features, Reader data rights rule 1`
- [ ] `C-CF-312` `data` The reader export carries `reader`, `progress`, `entitlements` with `tips` matched to the reader. `src: Core features, Reader data rights rule 1`
- [ ] `C-CF-313` `literal` `DELETE /api/me` with the reader's `password` deletes the reader account. `src: Core features, Reader data rights rule 2`
- [ ] `C-CF-314` `constraint` Reader account deletion removes the reader's sessions, progress with entitlements. `src: Core features, Reader data rights rule 2`
- [ ] `C-CF-315` `constraint` Tips a deleted reader sent are kept with the matched reader cleared. `src: Core features, Reader data rights rule 2`
- [ ] `C-CF-316` `constraint` Tips a deleted reader sent keep no `supporter_email`. `src: Core features, Reader data rights rule 2`
- [ ] `C-CF-317` `constraint` A reader account deletion with a wrong password deletes nothing. `src: Core features, Reader data rights rule 2`
- [ ] `C-CF-318` `literal` `PATCH /api/me` changes `locale` to `en` or `fr`. `src: Core features, Reader data rights rule 3`
- [ ] `C-CF-319` `literal` `PATCH /api/me` changes `notifications` to `all`, `drops` or `none`. `src: Core features, Reader data rights rule 3`
- [ ] `C-CF-320` `capability` `PATCH /api/me` changes `email`, validated as at signup. `src: Core features, Reader data rights rule 3`
- [ ] `C-CF-321` `literal` Two locales exist, `en` as the unprefixed default with `fr` under the `/fr` prefix. `src: Core features, Languages and localisation rule 1`
- [ ] `C-CF-322` `literal` Path segments are never translated, a translated segment such as `/fr/chapitres` being a `404` not-found page. `src: Core features, Languages and localisation rule 1`
- [ ] `C-CF-323` `literal` The language selector shows `EN` with `FR`, a divider between them. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-324` `ui` A coloured curtain sweeps over the window during a language switch, then lifts. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-325` `capability` Pressing the inactive language switches language without reloading the document. `src: Core features, Languages and localisation rule 2; restated in Definition of done`
- [ ] `C-CF-326` `capability` A language switch adds or removes `/fr` on the same path. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-327` `capability` A language switch changes every interface string to the new language. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-328` `capability` A language switch changes every lettered layer image to the new language. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-329` `capability` A language switch changes the `<html lang>` value. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-330` `literal` The switched language is remembered in local storage under `dd-language` as `en` or `fr`. `src: Core features, Languages and localisation rule 2`
- [ ] `C-CF-331` `constraint` Adding a third locale needs locale data plus translations, not a code change. `src: Core features, Languages and localisation rule 3`
- [ ] `C-CF-332` `literal` `GET /api/catalogue/<locale>` returns every interface string for the locale as a flat object of dotted keys. `src: Core features, Languages and localisation rule 4`
- [ ] `C-CF-333` `literal` A catalogue key whose translation is `untranslated` serves the default-locale value. `src: Core features, Languages and localisation rule 4`
- [ ] `C-CF-334` `constraint` A reader never sees a catalogue key path. `src: Core features, Languages and localisation rule 4`
- [ ] `C-CF-335` `literal` The catalogue key `chrome.chapters` holds the English value `chapters`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-336` `literal` The catalogue key `chrome.about` holds the English value `about`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-337` `literal` The catalogue key `chrome.legal` holds the English value `legal notice & terms of use`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-338` `capability` The catalogue key `chrome.byline` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-339` `literal` The catalogue key `chrome.fullscreen_enter` holds the English value `enter fullscreen`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-340` `literal` The catalogue key `chrome.fullscreen_exit` holds the English value `exit fullscreen`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-341` `literal` The catalogue key `index.button` holds the English value `read now`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-342` `literal` The catalogue key `index.credit` holds the English value `By Damien Lorca & Camille Rouyer`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-343` `literal` The catalogue key `chapters.heading` holds the English value `select a chapter`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-344` `literal` The catalogue key `chapters.tip` holds the English value `support us`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-345` `literal` The catalogue key `chapters.next_track` holds the English value `next track`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-346` `literal` The catalogue key `reader.loading` holds the English value `Next track is loading...`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-347` `literal` The catalogue key `reader.text_mode` holds the English value `read as text`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-348` `literal` The catalogue key `reader.previous_panel` holds the English value `previous panel`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-349` `literal` The catalogue key `reader.next_panel` holds the English value `next panel`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-350` `literal` The catalogue key `reader.progress` holds the English value `chapter progress`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-351` `literal` The catalogue key `reader.load_failed` holds the English value `Something went missing. Try again?`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-352` `literal` The catalogue key `reader.retry` holds the English value `try again`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-353` `literal` The catalogue key `reader.back` holds the English value `back to chapters`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-354` `capability` The catalogue key `locked.timing` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-355` `capability` The catalogue key `locked.drawing` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-356` `literal` The catalogue key `locked.notify` holds the English value `notify me`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-357` `capability` The catalogue key `locked.support` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-358` `capability` The catalogue key `consent.message` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-359` `literal` The catalogue key `consent.accept` holds the English value `Accept`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-360` `literal` The catalogue key `consent.decline` holds the English value `Decline`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-361` `literal` The catalogue key `support.granted` holds the English value `Thank you. Your early access is active.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-362` `capability` The catalogue key `support.sign_in` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-363` `capability` The catalogue key `support.below_threshold` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-364` `literal` The catalogue key `support.pending` holds the English value `Thank you. Your tip is on its way to us.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-365` `capability` The catalogue key `support.expired` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-366` `capability` The catalogue key `support.chip_tip` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-367` `literal` The catalogue key `support.entitlement` holds the English value `Tips of {amount} or more read new chapters up to {days} days early.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-368` `literal` The catalogue key `about.nav_intro` holds the English value `intro`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-369` `literal` The catalogue key `about.nav_legend` holds the English value `the legend`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-370` `literal` The catalogue key `about.nav_team` holds the English value `the team`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-371` `literal` The catalogue key `about.nav_support` holds the English value `support us`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-372` `literal` The catalogue key `about.scroll` holds the English value `Scroll down`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-373` `literal` The catalogue key `about.intro_title` holds the English value `the interactive adventure of a megalomaniac sheep who wants to make the world dance.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-374` `literal` The catalogue key `about.legend_title_1` holds the English value `yes the legend,`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-375` `literal` The catalogue key `about.legend_title_2` holds the English value `is {hero}!`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-376` `literal` The catalogue key `about.team_title_1` holds the English value `behind`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-377` `literal` The catalogue key `about.team_title_2` holds the English value `the legend`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-378` `literal` The catalogue key `about.support_title_1` holds the English value `i love you too`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-379` `literal` The catalogue key `about.support_title_2` holds the English value `my friend!`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-380` `literal` The catalogue key `about.chip_contact` holds the English value `email us`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-381` `literal` The catalogue key `legal.title` holds the English value `Legal Notice & Terms of Use`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-382` `literal` The catalogue key `legal.publisher` holds the English value `Website Publisher`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-383` `literal` The catalogue key `legal.hosting` holds the English value `Hosting`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-384` `literal` The catalogue key `legal.domains` holds the English value `Domains`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-385` `literal` The catalogue key `legal.property` holds the English value `Intellectual Property`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-386` `literal` The catalogue key `legal.terms` holds the English value `Terms of Use`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-387` `literal` The catalogue key `legal.data` holds the English value `Personal Data & Privacy`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-388` `literal` The catalogue key `legal.cookies` holds the English value `Cookies & Trackers`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-389` `literal` The catalogue key `legal.law` holds the English value `Applicable Law & Jurisdiction`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-390` `literal` The catalogue key `not-found.text` holds the English value `Oopsy, page not found`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-391` `literal` The catalogue key `not-found.cta` holds the English value `Go back to home`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-392` `literal` The catalogue key `account.heading` holds the English value `Your account`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-393` `literal` The catalogue key `account.export` holds the English value `download my data`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-394` `literal` The catalogue key `account.delete` holds the English value `delete my account`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-395` `literal` The catalogue key `account.sign_in` holds the English value `sign in`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-396` `literal` The catalogue key `account.create` holds the English value `create an account`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-397` `literal` The catalogue key `account.email` holds the English value `email`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-398` `literal` The catalogue key `account.password` holds the English value `password`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-399` `literal` The catalogue key `chrome.surprise` holds the English value `surprise`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-400` `literal` The catalogue key `chapters.locked_name` holds the English value `{title}, locked, opens {date}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-401` `literal` The catalogue key `chapters.locked_plain` holds the English value `{title}, locked`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-402` `literal` The catalogue key `chapters.timecode_label` holds the English value `chapter {number} of {count}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-403` `literal` The catalogue key `reader.timecode_label` holds the English value `panel {number}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-404` `literal` The catalogue key `reader.announce_loading` holds the English value `Chapter {number} is loading.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-405` `literal` The catalogue key `reader.announce_ready` holds the English value `Chapter {number} is ready.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-406` `literal` The catalogue key `reader.announce_failed` holds the English value `Chapter {number} could not be loaded.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-407` `literal` The catalogue key `reader.end_of_volume` holds the English value `last track of the volume, back to chapters`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-408` `literal` The catalogue key `chrome.announce_locale` holds the English value `The page is now in English.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-409` `capability` The catalogue key `about.legend_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-410` `literal` The catalogue key `about.team_dam_title` holds the English value `Dam`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-411` `capability` The catalogue key `about.team_dam_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-412` `literal` The catalogue key `about.team_ca_title` holds the English value `Ca`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-413` `capability` The catalogue key `about.team_ca_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-414` `capability` The catalogue key `about.support_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-415` `capability` The catalogue key `about.support_hidden` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-416` `literal` The catalogue key `about.chip_photogram` holds the English value `photogram`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-417` `literal` The catalogue key `about.chip_clipclop` holds the English value `clipclop`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-418` `capability` The catalogue key `legal.publisher_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-419` `literal` The catalogue key `legal.contact_label` holds the English value `Contact email`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-420` `literal` The catalogue key `legal.hosting_body` holds the English value `Hosted by Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-421` `capability` The catalogue key `legal.domains_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-422` `capability` The catalogue key `legal.property_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-423` `capability` The catalogue key `legal.terms_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-424` `capability` The catalogue key `legal.data_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-425` `capability` The catalogue key `legal.cookies_body` holds the pinned English value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-426` `literal` The catalogue key `legal.law_body` holds the English value `These terms are governed by French law. Any dispute falls under the courts of Paris.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-427` `literal` The catalogue key `chrome.chapters` holds the French value `chapitres`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-428` `literal` The catalogue key `chrome.about` holds the French value `a propos`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-429` `literal` The catalogue key `chrome.legal` holds the French value `mentions legales & conditions d'utilisation`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-430` `literal` The catalogue key `chrome.byline` holds the French value `par Camille Rouyer et Damien Lorca`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-431` `literal` The catalogue key `chrome.fullscreen_enter` holds the French value `plein ecran`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-432` `literal` The catalogue key `chrome.fullscreen_exit` holds the French value `quitter le plein ecran`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-433` `literal` The catalogue key `index.button` holds the French value `lire maintenant`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-434` `literal` The catalogue key `index.credit` holds the French value `Par Damien Lorca & Camille Rouyer`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-435` `literal` The catalogue key `chapters.heading` holds the French value `choisis un chapitre`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-436` `literal` The catalogue key `chapters.tip` holds the French value `soutiens-nous`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-437` `literal` The catalogue key `chapters.next_track` holds the French value `piste suivante`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-438` `literal` The catalogue key `reader.loading` holds the French value `La piste suivante arrive...`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-439` `literal` The catalogue key `reader.text_mode` holds the French value `lire en texte`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-440` `literal` The catalogue key `reader.previous_panel` holds the French value `case precedente`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-441` `literal` The catalogue key `reader.next_panel` holds the French value `case suivante`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-442` `literal` The catalogue key `reader.progress` holds the French value `progression du chapitre`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-443` `literal` The catalogue key `reader.load_failed` holds the French value `Il manque quelque chose. On reessaie ?`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-444` `literal` The catalogue key `reader.retry` holds the French value `reessayer`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-445` `literal` The catalogue key `reader.back` holds the French value `retour aux chapitres`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-446` `literal` The catalogue key `locked.timing` holds the French value `Ce chapitre sort le {date}.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-447` `literal` The catalogue key `locked.drawing` holds the French value `Ce chapitre est encore en dessin.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-448` `literal` The catalogue key `locked.notify` holds the French value `previens-moi`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-449` `literal` The catalogue key `locked.support` holds the French value `Les soutiens le lisent des qu'il est fini.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-450` `capability` The catalogue key `consent.message` holds the pinned French value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-451` `literal` The catalogue key `consent.accept` holds the French value `Accepter`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-452` `literal` The catalogue key `consent.decline` holds the French value `Refuser`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-453` `literal` The catalogue key `support.granted` holds the French value `Merci. Ton acces anticipe est actif.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-454` `literal` The catalogue key `support.sign_in` holds the French value `Merci. Connecte-toi et nous l'ajouterons a ton compte.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-455` `literal` The catalogue key `support.below_threshold` holds the French value `Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-456` `literal` The catalogue key `support.pending` holds the French value `Merci. Ton pourboire est en route.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-457` `literal` The catalogue key `support.expired` holds the French value `Ce lien de remerciement a expire.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-458` `capability` The catalogue key `support.chip_tip` holds the pinned French value. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-459` `literal` The catalogue key `support.entitlement` holds the French value `Les pourboires de {amount} ou plus lisent les nouveaux chapitres jusqu'a {days} jours plus tot.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-460` `literal` The catalogue key `about.nav_intro` holds the French value `intro`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-461` `literal` The catalogue key `about.nav_legend` holds the French value `la legende`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-462` `literal` The catalogue key `about.nav_team` holds the French value `l'equipe`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-463` `literal` The catalogue key `about.nav_support` holds the French value `soutiens-nous`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-464` `literal` The catalogue key `about.scroll` holds the French value `Descends`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-465` `literal` The catalogue key `about.intro_title` holds the French value `l'aventure interactive d'un mouton megalomane qui veut faire danser le monde.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-466` `literal` The catalogue key `about.legend_title_1` holds the French value `oui la legende,`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-467` `literal` The catalogue key `about.legend_title_2` holds the French value `c'est {hero} !`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-468` `literal` The catalogue key `about.team_title_1` holds the French value `derriere`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-469` `literal` The catalogue key `about.team_title_2` holds the French value `la legende`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-470` `literal` The catalogue key `about.support_title_1` holds the French value `moi aussi je t'aime`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-471` `literal` The catalogue key `about.support_title_2` holds the French value `mon ami !`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-472` `literal` The catalogue key `about.chip_contact` holds the French value `ecris-nous`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-473` `literal` The catalogue key `legal.title` holds the French value `Mentions legales & conditions d'utilisation`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-474` `literal` The catalogue key `legal.publisher` holds the French value `Editeur du site`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-475` `literal` The catalogue key `legal.hosting` holds the French value `Hebergement`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-476` `literal` The catalogue key `legal.domains` holds the French value `Domaines`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-477` `literal` The catalogue key `legal.property` holds the French value `Propriete intellectuelle`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-478` `literal` The catalogue key `legal.terms` holds the French value `Conditions d'utilisation`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-479` `literal` The catalogue key `legal.data` holds the French value `Donnees personnelles & vie privee`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-480` `literal` The catalogue key `legal.cookies` holds the French value `Cookies & traceurs`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-481` `literal` The catalogue key `legal.law` holds the French value `Droit applicable & juridiction`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-482` `literal` The catalogue key `not-found.text` holds the French value `Oups, page introuvable`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-483` `literal` The catalogue key `not-found.cta` holds the French value `Retour a l'accueil`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-484` `literal` The catalogue key `account.heading` holds the French value `Ton compte`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-485` `literal` The catalogue key `account.export` holds the French value `telecharger mes donnees`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-486` `literal` The catalogue key `account.delete` holds the French value `supprimer mon compte`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-487` `literal` The catalogue key `account.sign_in` holds the French value `se connecter`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-488` `literal` The catalogue key `account.create` holds the French value `creer un compte`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-489` `literal` The catalogue key `account.email` holds the French value `e-mail`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-490` `literal` The catalogue key `account.password` holds the French value `mot de passe`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-491` `literal` The catalogue key `chrome.surprise` holds the French value `surprise`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-492` `literal` The catalogue key `chapters.locked_name` holds the French value `{title}, verrouille, sort le {date}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-493` `literal` The catalogue key `chapters.locked_plain` holds the French value `{title}, verrouille`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-494` `literal` The catalogue key `chapters.timecode_label` holds the French value `chapitre {number} sur {count}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-495` `literal` The catalogue key `reader.timecode_label` holds the French value `case {number}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-496` `literal` The catalogue key `reader.announce_loading` holds the French value `Le chapitre {number} arrive.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-497` `literal` The catalogue key `reader.announce_ready` holds the French value `Le chapitre {number} est pret.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-498` `literal` The catalogue key `reader.announce_failed` holds the French value `Le chapitre {number} n'a pas pu etre charge.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-499` `literal` The catalogue key `reader.end_of_volume` holds the French value `derniere piste du volume, retour aux chapitres`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-500` `literal` The catalogue key `chrome.announce_locale` holds the French value `La page est maintenant en francais.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-501` `literal` The catalogue key `about.legend_body` holds the French value `Doudou est un mouton megalomane, tendre et bien decide a devenir DJ. Avec Jean-Loic, un barman dechaine, et Milan, future star de la cuisine sur les reseaux, il melange chaos et grands reves dans un appart plein de rires et de bruit tard le soir. C'est cool, c'est drole, c'est Doudou Fever.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-502` `literal` The catalogue key `about.team_dam_title` holds the French value `Dam`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-503` `literal` The catalogue key `about.team_dam_body` holds the French value `Developpeur creatif et animateur, moitie codeur moitie sorcier. Il anime les images, fait bouger les pixels et transforme des lignes de code en experiences cool et magiques.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-504` `literal` The catalogue key `about.team_ca_title` holds the French value `Ca`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-505` `literal` The catalogue key `about.team_ca_body` holds the French value `Directrice artistique, illustratrice et maitresse du pinceau numerique. Elle dessine plus vite que son ombre et donne vie a chaque personnage avec style, emotion...`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-506` `literal` The catalogue key `about.support_body` holds the French value `Soutiens Doudou sur le chemin de la gloire et aide-le a devenir une legende. Un jour, peut-etre : une edition imprimee, du merch trop mignon, et Doudou sous les projecteurs !`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-507` `literal` The catalogue key `about.support_hidden` holds the French value `Fais partie de l'aventure, ou vis pour toujours avec cette question "Et si j'avais aide Doudou a devenir une legende ?"`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-508` `literal` The catalogue key `about.chip_photogram` holds the French value `photogram`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-509` `literal` The catalogue key `about.chip_clipclop` holds the French value `clipclop`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-510` `literal` The catalogue key `legal.publisher_body` holds the French value `Le site Doudou Fever est cree et publie par Damien Lorca et Camille Rouyer.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-511` `literal` The catalogue key `legal.contact_label` holds the French value `E-mail de contact`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-512` `literal` The catalogue key `legal.hosting_body` holds the French value `Heberge par Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-513` `literal` The catalogue key `legal.domains_body` holds the French value `Les domaines doudoufever.example, www.doudoufever.example, doudou-fever.example et doudoufever-comic.example sont enregistres aupres de Registre Clair SARL, 4 quai du Port, 13002 Marseille, France.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-514` `literal` The catalogue key `legal.property_body` holds the French value `Tout le contenu de ce site est protege. Aucune licence n'est accordee, et toute reproduction, diffusion, modification ou exploitation sans autorisation prealable est interdite.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-515` `literal` The catalogue key `legal.terms_body` holds the French value `L'utilisation de ce site est personnelle. Les utilisateurs s'engagent a ne pas perturber le site. Les liens externes comme Tipbox ne relevent pas de la responsabilite de l'editeur, y compris pour les incidents de paiement. Le site peut etre modifie ou suspendu sans preavis.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-516` `literal` The catalogue key `legal.data_body` holds the French value `L'adresse, la progression et les pourboires rattaches d'un lecteur sont collectes uniquement pour faire fonctionner le compte lecteur. Ils ne sont jamais revendus et peuvent etre exportes, corriges ou supprimes depuis la page du compte.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-517` `literal` The catalogue key `legal.cookies_body` holds the French value `Les cles fonctionnelles dd-consent, dd-language, dd-last-chapter, les cles dd-progress-, dd-session et dd-studio-session sont posees quel que soit le choix de consentement car elles retiennent seulement la place, la langue et la session du lecteur. La mesure ne demarre qu'apres Accepter.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-518` `literal` The catalogue key `legal.law_body` holds the French value `Ces conditions sont regies par le droit francais. Tout litige releve des tribunaux de Paris.`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-519` `capability` Page titles are catalogue keys `index.meta_title`, `chapters.meta_title`, `reader.meta_title`, `about.meta_title`, `legal.meta_title`, `support.meta_title`, `account.meta_title`, `not-found.meta_title`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-520` `capability` Each page `meta_title` key has a matching `meta_description` catalogue key holding the page description. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-521` `literal` The catalogue key `reader.meta_title` carries the placeholders `{number}` with `{title}`. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-522` `capability` Every other interface string shown or announced is a catalogue key in both languages, in the page's namespace. `src: Core features, Languages and localisation rule 5`
- [ ] `C-CF-523` `literal` The chapter title `welcome to Varny` is transcreated in French as `bonjour Varny`. `src: Core features, Languages and localisation rule 6`
- [ ] `C-CF-524` `literal` The chapter title `under pressure` is transcreated in French as `sous pression`. `src: Core features, Languages and localisation rule 6`
- [ ] `C-CF-525` `literal` The chapter title `sheep don't sleep` is transcreated in French as `moutons insomniaques`. `src: Core features, Languages and localisation rule 6`
- [ ] `C-CF-526` `literal` The chapter title `scratch that !` is transcreated in French as `on efface tout !`. `src: Core features, Languages and localisation rule 6`
- [ ] `C-CF-527` `literal` The chapter title `wow ...` is transcreated in French as `ouf ...`. `src: Core features, Languages and localisation rule 6`
- [ ] `C-CF-528` `literal` The chapter title `the big mix` is transcreated in French as `le grand mix`. `src: Core features, Languages and localisation rule 6`
- [ ] `C-CF-529` `capability` Every date shown is formatted for the page's language. `src: Core features, Languages and localisation rule 7`
- [ ] `C-CF-530` `capability` Every number shown is formatted for the page's language. `src: Core features, Languages and localisation rule 7`
- [ ] `C-CF-531` `capability` On a first visit a consent strip slides up along the bottom with the pinned `consent.message` line. `src: Core features, Consent, measurement and page views rule 1`
- [ ] `C-CF-532` `literal` The consent strip offers `Accept` with `Decline`. `src: Core features, Consent, measurement and page views rule 1`
- [ ] `C-CF-533` `capability` The consent strip takes keyboard focus when the strip appears. `src: Core features, Consent, measurement and page views rule 1`
- [ ] `C-CF-534` `capability` The consent strip keeps keyboard focus inside the strip until answered. `src: Core features, Consent, measurement and page views rule 1`
- [ ] `C-CF-535` `ui` An answered consent strip slides away. `src: Core features, Consent, measurement and page views rule 2`
- [ ] `C-CF-536` `literal` A consent answer is written to `dd-consent` in local storage as `accepted` or `declined`. `src: Core features, Consent, measurement and page views rule 2`
- [ ] `C-CF-537` `capability` A consent answer releases the footer, language selector, fullscreen control with tip control into place. `src: Core features, Consent, measurement and page views rule 2`
- [ ] `C-CF-538` `constraint` A reload with a stored consent answer shows no consent strip. `src: Core features, Consent, measurement and page views rule 2`
- [ ] `C-CF-539` `literal` The legal cookies section names `dd-consent`, `dd-language`, `dd-last-chapter`, the `dd-progress-` keys, `dd-session`, `dd-studio-session`. `src: Core features, Consent, measurement and page views rule 3`
- [ ] `C-CF-540` `capability` The legal cookies section states the functional keys are set whatever the consent decision. `src: Core features, Consent, measurement and page views rule 3`
- [ ] `C-CF-541` `constraint` After a decline, cookies, local storage with session storage hold no key beyond `dd-consent`, `dd-language`, `dd-last-chapter`, `dd-progress-` keys. `src: Core features, Consent, measurement and page views rule 4`
- [ ] `C-CF-542` `constraint` After a decline the visitor sends no request to `/api/events`, however much the visitor reads. `src: Core features, Consent, measurement and page views rule 4`
- [ ] `C-CF-543` `constraint` The storage session keys `dd-session` with `dd-studio-session` are the only further keys, present only when signed in. `src: Core features, Consent, measurement and page views rule 4`
- [ ] `C-CF-544` `literal` After an accept the app records reading events through `POST /api/events` with a `name` with `params`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-545` `constraint` `panel_reached` is sent at most once per panel per visit. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-546` `literal` The measured event `chapter_opened` carries params `volume`, `chapter`, `locale`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-547` `literal` The measured event `panel_reached` carries params `volume`, `chapter`, `panel`, `elapsed_seconds`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-548` `literal` The measured event `chapter_completed` carries params `volume`, `chapter`, `elapsed_seconds`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-549` `literal` The measured event `chapter_abandoned` carries params `volume`, `chapter`, `last_panel`, `elapsed_seconds`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-550` `literal` The measured event `tip_control_pressed` carries params `route`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-551` `literal` The measured event `chapter_load_failed` carries params `volume`, `chapter`, `failure`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-552` `literal` The measured event `language_switched` carries params `locale`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-553` `literal` The measured event `fullscreen_toggled` carries params `state`. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-554` `constraint` A measured event with any other name is rejected as invalid, stored nowhere. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-555` `constraint` A measured event with any other parameter key is rejected as invalid, stored nowhere. `src: Core features, Consent, measurement and page views rule 5`
- [ ] `C-CF-556` `literal` Every public page view is recorded through `POST /api/page-views` with the route name. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-557` `constraint` Page views reached by in-app navigation are recorded too. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-558` `constraint` Page views are recorded whatever the consent decision. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-559` `literal` The page-view route name `chapter-id` covers both chapter address forms. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-560` `literal` Page-view route names are `index`, `chapters`, `chapter-id`, `about`, `legal`, `support-return`, `account`, `not-found`. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-561` `constraint` A page-view route name outside the list is rejected. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-562` `constraint` A page view carries no visitor, reader, address or query value. `src: Core features, Consent, measurement and page views rule 6`
- [ ] `C-CF-563` `capability` Every manifest served counts one chapter open for the chapter in the hour. `src: Core features, Consent, measurement and page views rule 7`
- [ ] `C-CF-564` `constraint` A counted chapter open carries no identifier. `src: Core features, Consent, measurement and page views rule 7`
- [ ] `C-CF-565` `literal` Authors read page views newest first at `GET /api/studio/page-views`. `src: Core features, Consent, measurement and page views rule 8`
- [ ] `C-CF-566` `literal` The studio page-view list filters by `route`. `src: Core features, Consent, measurement and page views rule 8`
- [ ] `C-CF-567` `literal` `GET /api/studio/insights` keeps server counts beside measured events. `src: Core features, Consent, measurement and page views rule 8`
- [ ] `C-CF-568` `data` Insights server counts carry `page_views` with `chapter_opens` by hour. `src: Core features, Consent, measurement and page views rule 8`
- [ ] `C-CF-569` `data` Insights measured `events` are counted by name. `src: Core features, Consent, measurement and page views rule 8`
- [ ] `C-CF-570` `constraint` Insights never add measured events to server counts. `src: Core features, Consent, measurement and page views rule 8`
- [ ] `C-CF-571` `capability` `/about` is the only public page that scrolls. `src: Core features, About and legal rule 1`
- [ ] `C-CF-572` `literal` The about page has four sections named `intro`, `the legend`, `the team`, `support us`. `src: Core features, About and legal rule 1`
- [ ] `C-CF-573` `capability` A rail of four dots on the right edge of the about page names each section on hover. `src: Core features, About and legal rule 1`
- [ ] `C-CF-574` `capability` Pressing an about rail dot jumps to the matching section. `src: Core features, About and legal rule 1`
- [ ] `C-CF-575` `constraint` The about rail disappears at the width step where the language selector moves to the bottom left. `src: Core features, About and legal rule 1`
- [ ] `C-CF-576` `literal` The about intro heading reads `the interactive adventure of a megalomaniac sheep who wants to make the world dance.` `src: Core features, About and legal rule 2`
- [ ] `C-CF-577` `literal` The about intro shows the prompt `Scroll down`. `src: Core features, About and legal rule 2`
- [ ] `C-CF-578` `ui` Characters fall into the about intro frame under gravity, piling up along the bottom. `src: Core features, About and legal rule 2`
- [ ] `C-CF-579` `capability` Piled intro characters can be picked up then thrown with the pointer. `src: Core features, About and legal rule 2`
- [ ] `C-CF-580` `literal` The about legend heading reads `yes the legend,` then `is Doudou!`. `src: Core features, About and legal rule 3`
- [ ] `C-CF-581` `ui` The legend body arrives word by word as the legend section scrolls into view. `src: Core features, About and legal rule 3`
- [ ] `C-CF-582` `capability` The legend body shows the pinned `about.legend_body` text. `src: Core features, About and legal rule 3`
- [ ] `C-CF-583` `capability` The `Dam` team card sits on a near-black card showing the pinned `about.team_dam_body` text. `src: Core features, About and legal rule 4`
- [ ] `C-CF-584` `capability` The `Ca` team card sits on a cream card showing the pinned `about.team_ca_body` text. `src: Core features, About and legal rule 4`
- [ ] `C-CF-585` `capability` The support body shows the pinned `about.support_body` text. `src: Core features, About and legal rule 5`
- [ ] `C-CF-586` `constraint` The second support paragraph `about.support_hidden` is present but hidden. `src: Core features, About and legal rule 5`
- [ ] `C-CF-587` `capability` The give-a-tip chip on the about support section links to the Tipbox page. `src: Core features, About and legal rule 5`
- [ ] `C-CF-588` `literal` The about team heading reads `behind` then `the legend`. `src: Core features, About and legal rule 4`
- [ ] `C-CF-589` `ui` The two team cards begin tilted away, then swing round to face the reader as the team section scrolls. `src: Core features, About and legal rule 4`
- [ ] `C-CF-590` `capability` Pressing a team card flips the card. `src: Core features, About and legal rule 4`
- [ ] `C-CF-591` `literal` The about support heading reads `i love you too` then `my friend!`. `src: Core features, About and legal rule 5`
- [ ] `C-CF-592` `literal` Four chips follow the support body, `support.chip_tip`, `photogram`, `clipclop`, `email us`. `src: Core features, About and legal rule 5`
- [ ] `C-CF-593` `capability` A line under the about chips states what a tip buys, filling `{amount}` from the early-access threshold as money. `src: Core features, About and legal rule 5`
- [ ] `C-CF-594` `capability` The about tip line fills `{days}` from the default `early_access_days`. `src: Core features, About and legal rule 5`
- [ ] `C-CF-595` `literal` English money shows a leading `$` with a full stop before two decimals, as in `$5.00`. `src: Core features, About and legal rule 5`
- [ ] `C-CF-596` `literal` French money shows a comma before two decimals, one space, a trailing `$`, as in `5,00 $`. `src: Core features, About and legal rule 5`
- [ ] `C-CF-597` `literal` With the seeded settings the English about tip line reads `Tips of $5.00 or more read new chapters up to 7 days early.` `src: Core features, About and legal rule 5`
- [ ] `C-CF-598` `literal` With the seeded settings the French about tip line reads `Les pourboires de 5,00 $ ou plus lisent les nouveaux chapitres jusqu'a 7 jours plus tot.` `src: Core features, About and legal rule 5`
- [ ] `C-CF-599` `literal` The fragment `#doudou` opens the about page at the legend section in either language. `src: Core features, About and legal rule 6`
- [ ] `C-CF-600` `literal` The fragment `#team` or `#equipe` opens the about page at the team section. `src: Core features, About and legal rule 6`
- [ ] `C-CF-601` `literal` The fragment `#support` opens the about page at the support section. `src: Core features, About and legal rule 6`
- [ ] `C-CF-602` `constraint` Any other fragment opens the about page at the intro. `src: Core features, About and legal rule 6`
- [ ] `C-CF-603` `capability` `/legal` is plain prose the reader can select in one sweep. `src: Core features, About and legal rule 7`
- [ ] `C-CF-604` `literal` The legal page is headed `Legal Notice & Terms of Use`. `src: Core features, About and legal rule 7`
- [ ] `C-CF-605` `literal` The legal page has eight sections headed `Website Publisher`, `Hosting`, `Domains`, `Intellectual Property`, `Terms of Use`, `Personal Data & Privacy`, `Cookies & Trackers`, `Applicable Law & Jurisdiction`. `src: Core features, About and legal rule 7`
- [ ] `C-CF-606` `literal` The legal Website Publisher section names the two creators with `Contact email` `hello@example.com`. `src: Core features, About and legal rule 8`
- [ ] `C-CF-607` `literal` The legal Hosting section names `Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France`. `src: Core features, About and legal rule 8`
- [ ] `C-CF-608` `literal` The legal Domains section lists `doudoufever.example`, `www.doudoufever.example`, `doudou-fever.example`, `doudoufever-comic.example`. `src: Core features, About and legal rule 8`
- [ ] `C-CF-609` `literal` The legal Domains section names the registrar `Registre Clair SARL, 4 quai du Port, 13002 Marseille, France`. `src: Core features, About and legal rule 8`
- [ ] `C-CF-610` `capability` The legal Intellectual Property section states all content is protected with no licence granted. `src: Core features, About and legal rule 9`
- [ ] `C-CF-611` `capability` The legal Intellectual Property section states reproduction without prior authorisation is prohibited. `src: Core features, About and legal rule 9`
- [ ] `C-CF-612` `capability` The legal Terms of Use section states use is personal, with users agreeing not to disrupt the site. `src: Core features, About and legal rule 9`
- [ ] `C-CF-613` `capability` The legal Terms of Use section states external links such as Tipbox are outside the publisher's responsibility. `src: Core features, About and legal rule 9`
- [ ] `C-CF-614` `capability` The legal Terms of Use section states the site may be modified or suspended without notice. `src: Core features, About and legal rule 9`
- [ ] `C-CF-615` `capability` The legal Personal Data section states reader data is collected only to run the reader account, never resold. `src: Core features, About and legal rule 9`
- [ ] `C-CF-616` `capability` The legal Personal Data section states reader data can be exported, corrected or deleted from the account page. `src: Core features, About and legal rule 9`
- [ ] `C-CF-617` `literal` The legal Cookies section says measurement runs only after `Accept`. `src: Core features, About and legal rule 9`
- [ ] `C-CF-618` `capability` The legal Applicable Law section names French law with the courts of Paris. `src: Core features, About and legal rule 9`
- [ ] `C-CF-619` `capability` Typing up, up, down, down, left, right, left, right, `b`, `a` on any public page opens the surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 1`
- [ ] `C-CF-620` `constraint` A wrong key resets the surprise key sequence. `src: Core features, Delight surfaces: the surprise easter egg rule 1`
- [ ] `C-CF-621` `literal` The surprise is a dialog named `surprise` over a half-black overlay. `src: Core features, Delight surfaces: the surprise easter egg rule 1`
- [ ] `C-CF-622` `ui` Fifty-five spinning copies of Doudou's head scatter across the window under the surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 1`
- [ ] `C-CF-623` `ui` A wobbling centre frame plays a looping animation inside the surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 1`
- [ ] `C-CF-624` `constraint` The surprise never plays sound. `src: Core features, Delight surfaces: the surprise easter egg rule 2`
- [ ] `C-CF-625` `capability` Escape closes the surprise, returning focus to where focus was. `src: Core features, Delight surfaces: the surprise easter egg rule 2`
- [ ] `C-CF-626` `capability` Pressing the overlay closes the surprise, returning focus to where focus was. `src: Core features, Delight surfaces: the surprise easter egg rule 2`
- [ ] `C-CF-627` `capability` Navigation away closes the surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 2`
- [ ] `C-CF-628` `capability` Focus stays inside the open surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 2`
- [ ] `C-CF-629` `constraint` Under reduced motion the key sequence does not open the surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 3`
- [ ] `C-CF-630` `constraint` Under reduced motion clicking the record does not open the surprise. `src: Core features, Delight surfaces: the surprise easter egg rule 3`
- [ ] `C-CF-631` `literal` Authors list volumes at `GET /api/studio/volumes`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 1`
- [ ] `C-CF-632` `literal` Authors create a volume with a `label` of 1 to 40 characters at `POST /api/studio/volumes`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 1`
- [ ] `C-CF-633` `capability` A new volume takes the next volume `order`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 1`
- [ ] `C-CF-634` `literal` The seeded volume `Vol. I` has order `1`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 1`
- [ ] `C-CF-635` `constraint` A volume label outside 1 to 40 characters is rejected naming the field, creating nothing. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 1`
- [ ] `C-CF-636` `literal` `POST /api/studio/volumes/{id}/chapters` creates the next chapter number of the volume as a `draft`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 2`
- [ ] `C-CF-637` `data` A new chapter carries `titles` with `descriptions` per locale. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 2`
- [ ] `C-CF-638` `constraint` Chapter numbers are contiguous from 1 within each volume. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 2`
- [ ] `C-CF-639` `constraint` A chapter title outside 1 to 60 characters is rejected naming the field, creating nothing. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 2`
- [ ] `C-CF-640` `constraint` A chapter description over 200 characters is rejected naming the field, creating nothing. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 2`
- [ ] `C-CF-641` `literal` `GET /api/studio/volumes/{id}/chapters` returns one row per chapter ordered by number. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 3`
- [ ] `C-CF-642` `data` Each studio chapter row carries `titles`, `state`, `release_at`, `published_at`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 3`
- [ ] `C-CF-643` `data` Each studio chapter row carries `boards_ready` over `boards_total`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 3`
- [ ] `C-CF-644` `data` Each studio chapter row carries `image_bytes`, the stored bytes of all the chapter's images. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 3`
- [ ] `C-CF-645` `capability` A board counts as ready when the board has a panel, every panel has a layer, every panel has descriptions in every active locale, every layer image is stored. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 3`
- [ ] `C-CF-646` `literal` `POST /api/studio/chapters/{id}/boards` adds the next board number. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 4`
- [ ] `C-CF-647` `literal` `PUT /api/studio/chapters/{id}/cover` stores the chapter cover image. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 4`
- [ ] `C-CF-648` `literal` `POST /api/studio/boards/{id}/imports` takes one multipart request of `files`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 5; restated in Definition of done`
- [ ] `C-CF-649` `capability` An imported file naming a panel that does not exist creates that panel. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 7`
- [ ] `C-CF-650` `constraint` An import is one transaction, every file imported or none. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 5`
- [ ] `C-CF-651` `literal` An import rejection names the failing `file`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 5`
- [ ] `C-CF-652` `constraint` A rejected import leaves no new panel, layer or bucket object. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 5`
- [ ] `C-CF-653` `literal` A layer identifier file name follows `c<chapter>b<board>p<panel>-<role>` plus an extension, as in `c1b1p1-back.png`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-654` `constraint` Layer identifier chapter with board numbers have 1 to 3 digits, with no leading zero. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-655` `constraint` A layer identifier panel number has 1 to 2 digits, with no leading zero. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-656` `constraint` A layer identifier role is one or more segments of 1 to 24 lowercase letters or digits joined by single hyphens. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-657` `constraint` A layer identifier's chapter with board numbers must be the importing board's own. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-658` `constraint` A layer identifier holding an uppercase letter, space, underscore or any other character is rejected. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-659` `constraint` A layer identifier rejection names the offending character. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-660` `constraint` A layer file name is never tidied. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 6`
- [ ] `C-CF-661` `capability` A reimported file naming an existing role replaces the layer image, keeping depth, offset, scale, opacity, draw order. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 7`
- [ ] `C-CF-662` `constraint` Two files naming the same role in one import are rejected. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 7`
- [ ] `C-CF-663` `constraint` A `sprite` file must arrive with the matching `sprite-data` JSON frame table, neither accepted alone. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 8`
- [ ] `C-CF-664` `constraint` A locale role segment marks a localised layer needing a file for every active locale in the same import. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 8`
- [ ] `C-CF-665` `capability` A trailing `depth` or `map` role segment adds a greyscale map layer attached as the displacement source of the named layer. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 8`
- [ ] `C-CF-666` `constraint` A map layer's named layer must exist in the panel or the same import. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 8`
- [ ] `C-CF-667` `data` A frame table carries `width`, `height`, `fps`, `frames`, `clips`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 9`
- [ ] `C-CF-668` `data` Each frame table frame carries `x`, `y`, `w`, `h`, `pivot_x`, `pivot_y`, `duration_ms`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 9`
- [ ] `C-CF-669` `data` Each frame table clip carries `name`, `first`, `last`, `loop` of `once`, `loop` or `ping-pong`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 9`
- [ ] `C-CF-670` `constraint` A frame table missing any field is rejected. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 9`
- [ ] `C-CF-671` `constraint` Imported image content is recognised from the bytes, never from the file name. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 10`
- [ ] `C-CF-672` `capability` Imported PNG, WebP or JPEG image bytes are accepted. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 10`
- [ ] `C-CF-673` `constraint` Imported files other than PNG, WebP or JPEG images are rejected even when named `.png`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 10`
- [ ] `C-CF-674` `constraint` An import accepts at most 200 files. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 10`
- [ ] `C-CF-675` `constraint` An import accepts at most 40 megabytes per file. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 10`
- [ ] `C-CF-676` `constraint` An imported layer image is re-encoded as PNG with every metadata chunk removed before being stored. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-677` `literal` An imported image is stored in the bucket at `chapters/{volume_order}/{chapter_number}/{file_identifier}/{sha256_of_bytes}.png`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-678` `constraint` The stored image key hash is the lowercase hexadecimal SHA-256 of the stored bytes. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-679` `constraint` The storage key file identifier keeps any locale segment. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-680` `literal` A frame table is stored at the same key scheme ending `.json`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-681` `literal` A cover is stored at `covers/{volume_order}/{chapter_number}/{sha256_of_bytes}.png`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-682` `constraint` Nothing is written to the app's own disk. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 11`
- [ ] `C-CF-683` `constraint` Adding or replacing any chapter image changes the chapter's `content_tag`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 12`
- [ ] `C-CF-684` `constraint` Only an image change alters a chapter's `content_tag`, the content tag changing for nothing else. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 12`
- [ ] `C-CF-685` `literal` `PATCH /api/studio/layers/{id}` edits a layer. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-686` `constraint` Layer `depth` runs from -10 to 10. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-687` `constraint` Layer `offset_x` with `offset_y` run from -10 to 10. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-688` `constraint` Layer `scale` runs from 0.1 to 4. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-689` `constraint` Layer `opacity` runs from 0 to 1. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-690` `literal` Layer `blend` is `normal` or `additive`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-691` `constraint` A layer value outside the value's range is rejected naming the field, changing nothing. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-692` `constraint` Layer `draw_order` runs from 0 to 63, unique within the panel. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-693` `constraint` Layer `displacement_source` names a map layer in the same panel. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-694` `constraint` Layer `displacement_strength` runs from 0 to 1. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-695` `constraint` Layer `clip` names a clip of the layer's frame table. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-696` `literal` Layer `loop_mode` is `once`, `loop` or `ping-pong`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-697` `data` A layer edit sets `retain`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 13`
- [ ] `C-CF-698` `literal` `PATCH /api/studio/panels/{id}` edits panel `descriptions` per locale of 1 to 300 characters. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 14`
- [ ] `C-CF-699` `data` A panel edit sets `selectable`, `hold`, `wide`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 14`
- [ ] `C-CF-700` `constraint` Panel `entry_duration` runs from 0.1 to 3.0 seconds. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 14`
- [ ] `C-CF-701` `constraint` Panel `camera_x` with `camera_y` run from -10 to 10. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 14`
- [ ] `C-CF-702` `constraint` A panel value outside the value's range is rejected naming the field, changing nothing. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 14`
- [ ] `C-CF-703` `capability` A console edit shows at once, then is saved. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-704` `data` Every chapter, board, panel with layer carries a `version`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-705` `constraint` Every edit sends the `version` last read. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-706` `literal` An edit carrying a stale version answers `409` with the error code `version_conflict`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-707` `data` A `version_conflict` answer carries the current row under `current`, changing nothing. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-708` `data` A successful edit returns the new version. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-709` `capability` When a save is rejected as invalid the console puts back the last saved value, stating why beneath the field. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-710` `capability` On a `version_conflict` the console shows the author's value beside the `current` value, asking which to keep. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 15`
- [ ] `C-CF-711` `constraint` Any edit to a `ready` chapter's titles, descriptions, boards, panels or layers returns the chapter to `draft`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 16`
- [ ] `C-CF-712` `constraint` An edit to a `scheduled` chapter's content is refused until the release is cancelled. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 16`
- [ ] `C-CF-713` `literal` `GET /api/studio/search?q=` searches chapter titles, panel identifiers, layer identifiers, translation keys, ranked in that order. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 17`
- [ ] `C-CF-714` `literal` Each studio search result carries a `type` of `chapter`, `panel`, `layer` or `translation`. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 17`
- [ ] `C-CF-715` `capability` A search query that is a full layer identifier returns the layer's panel composer address first. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 17`
- [ ] `C-CF-716` `literal` `GET /api/studio/chapters/{id}/manifest` previews any chapter, drafts included. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 18`
- [ ] `C-CF-717` `capability` The studio preview manifest carries signed image addresses. `src: Core features, Studio content: volumes, chapters, boards, panels and layers rule 18`
- [ ] `C-CF-718` `literal` A chapter `state` is one of `draft`, `ready`, `scheduled`, `published`, `unpublished`. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-719` `capability` The chapter state moves from `draft` to `ready` through `POST /api/studio/chapters/{id}/ready`. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-720` `capability` Any content edit moves the chapter state from `ready` back to `draft`. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-721` `capability` The chapter state moves from `ready` to `scheduled` through `POST /api/studio/chapters/{id}/schedule`. `src: Core features, Release scheduling rule 1; restated in Definition of done`
- [ ] `C-CF-722` `capability` The chapter state moves from `scheduled` to `ready` through `POST /api/studio/chapters/{id}/cancel`. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-723` `capability` The chapter state moves from `ready` to `published` through `POST /api/studio/chapters/{id}/publish`. `src: Core features, Release scheduling rule 1; restated in Definition of done`
- [ ] `C-CF-724` `capability` The chapter state moves from `published` to `unpublished` through `POST /api/studio/chapters/{id}/unpublish`. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-725` `capability` The chapter state moves from `unpublished` to `ready` through `POST /api/studio/chapters/{id}/ready`. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-726` `constraint` Any other chapter state transition request is rejected, leaving the state unchanged. `src: Core features, Release scheduling rule 1`
- [ ] `C-CF-727` `literal` `POST /api/studio/chapters/{id}/preflight` returns `passed` with `failures` listing each failing `rule` number with a `message`. `src: Core features, Release scheduling rule 2; restated in Definition of done`
- [ ] `C-CF-728` `constraint` Preflight rule 1 needs at least one board, a panel in every board, a layer in every panel. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-729` `constraint` Preflight rule 2 needs every layer image object in the bucket at the object's key. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-730` `constraint` Preflight rule 3 needs every localised layer to have an image for every active locale. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-731` `constraint` Preflight rule 4 needs a chapter title with panel descriptions in every active locale lacking a live waiver. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-732` `literal` Preflight rule 5 needs the chapter's stored image bytes within `24000000`. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-733` `literal` Preflight rule 6 needs the first board's stored image bytes within `3000000`. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-734` `constraint` Preflight rule 7 needs chapter numbers 1 up to the chapter to exist in the volume. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-735` `constraint` Preflight rule 8 needs a chapter cover. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-736` `constraint` Preflight rule 9 needs the previous chapter published, or scheduled earlier for a chapter being or already scheduled. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-737` `constraint` Preflight rule 10 needs the first layer image of the first board to be readable from the bucket. `src: Core features, Release scheduling rule 2`
- [ ] `C-CF-738` `constraint` Marking a chapter `ready` requires preflight rules 1, 2, 3, 4, 5, 6, 8 to pass. `src: Core features, Release scheduling rule 3`
- [ ] `C-CF-739` `constraint` Scheduling a chapter requires all ten preflight rules. `src: Core features, Release scheduling rule 3`
- [ ] `C-CF-740` `constraint` Publishing a chapter immediately requires all ten preflight rules with the previous chapter published. `src: Core features, Release scheduling rule 3`
- [ ] `C-CF-741` `literal` A failed ready, schedule or publish request answers the error code `preflight_failed` with the failing rules under `failures`, changing nothing. `src: Core features, Release scheduling rule 3`
- [ ] `C-CF-742` `constraint` Scheduling requires a `release_at` in the future at most 5 years ahead. `src: Core features, Release scheduling rule 3`
- [ ] `C-CF-743` `constraint` A `release_at` without a UTC offset, in the past or over 5 years ahead is rejected naming the `release_at` field, changing nothing. `src: Core features, Release scheduling rule 3`
- [ ] `C-CF-744` `constraint` A `release_at` with any UTC offset is accepted, stored as an instant. `src: Core features, Release scheduling rule 4`
- [ ] `C-CF-745` `literal` A scheduled `release_at` offset of `2027-03-28T20:00:00+02:00` reads back as the instant `2027-03-28T18:00:00Z`. `src: Core features, Release scheduling rule 4`
- [ ] `C-CF-746` `literal` The studio console shows moments in the studio time zone `Europe/Paris`. `src: Core features, Release scheduling rule 4`
- [ ] `C-CF-747` `capability` Readers see release moments in the reader's own time zone. `src: Core features, Release scheduling rule 4`
- [ ] `C-CF-748` `constraint` A scheduled chapter becomes `published` no more than 60 seconds after the release moment, with nobody asking. `src: Core features, Release scheduling rule 5; restated in Definition of done`
- [ ] `C-CF-749` `constraint` At the release moment preflight re-runs, returning a failing chapter to `ready`. `src: Core features, Release scheduling rule 5`
- [ ] `C-CF-750` `literal` A chapter failing preflight at release raises an overview alert of kind `preflight_failed_at_release`. `src: Core features, Release scheduling rule 5`
- [ ] `C-CF-751` `constraint` Publishing stamps `published_at` once. `src: Core features, Release scheduling rule 6`
- [ ] `C-CF-752` `constraint` Publishing an already published chapter succeeds with the same `published_at` with no second audit record. `src: Core features, Release scheduling rule 6`
- [ ] `C-CF-753` `literal` Unpublishing sets the chapter state to `unpublished`. `src: Core features, Release scheduling rule 7`
- [ ] `C-CF-754` `constraint` Unpublishing removes the chapter from the sitemaps. `src: Core features, Release scheduling rule 7`
- [ ] `C-CF-755` `constraint` Unpublishing removes the chapter from readers. `src: Core features, Release scheduling rule 7`
- [ ] `C-CF-756` `capability` Unpublishing makes the chapter page answer a temporary redirect to `/chapters`. `src: Core features, Release scheduling rule 7`
- [ ] `C-CF-757` `literal` A chapter's `early_access_days` runs from 0 to 30, defaulting to `7`. `src: Core features, Release scheduling rule 8`
- [ ] `C-CF-758` `constraint` An `early_access_days` value outside 0 to 30 is rejected naming the field, changing nothing. `src: Core features, Release scheduling rule 8`
- [ ] `C-CF-759` `literal` A per-locale waiver is set through `waivers` with a required `reason` of 1 to 200 characters. `src: Core features, Release scheduling rule 9`
- [ ] `C-CF-760` `literal` A locale waiver lasts `30` days. `src: Core features, Release scheduling rule 9`
- [ ] `C-CF-761` `constraint` A live locale waiver lets preflight rule 4 skip the waived locale. `src: Core features, Release scheduling rule 9`
- [ ] `C-CF-762` `constraint` A locale waiver without a reason is rejected. `src: Core features, Release scheduling rule 9`
- [ ] `C-CF-763` `constraint` Every studio mutation writes one audit record carrying the author's address, the action, the subject, the `request_id`. `src: Core features, Release scheduling rule 10`
- [ ] `C-CF-764` `literal` Publication writes the audit action `chapter.published`. `src: Core features, Release scheduling rule 10`
- [ ] `C-CF-765` `literal` Scheduling writes the audit action `chapter.scheduled`. `src: Core features, Release scheduling rule 10`
- [ ] `C-CF-766` `literal` Unpublishing writes the audit action `chapter.unpublished`. `src: Core features, Release scheduling rule 10`
- [ ] `C-CF-767` `literal` A layer import writes the audit action `layer.imported`. `src: Core features, Release scheduling rule 10`
- [ ] `C-CF-768` `constraint` Audit records are only ever added, never changed or removed. `src: Core features, Release scheduling rule 10`
- [ ] `C-CF-769` `capability` Scheduling in the console ends on a full-page confirmation naming what changed. `src: Core features, Release scheduling rule 11`
- [ ] `C-CF-770` `capability` Publishing in the console ends on a full-page confirmation naming what changed. `src: Core features, Release scheduling rule 11`
- [ ] `C-CF-771` `capability` Unpublishing in the console ends on a full-page confirmation naming what changed. `src: Core features, Release scheduling rule 11`
- [ ] `C-CF-772` `capability` Raising the asset version in the console ends on a full-page confirmation naming what changed. `src: Core features, Release scheduling rule 11`
- [ ] `C-CF-773` `literal` Every interface string exists per locale with a state of `untranslated`, `translated` or `reviewed`. `src: Core features, Translations rule 1`
- [ ] `C-CF-774` `literal` Interface strings sit in the namespaces `chrome`, `index`, `chapters`, `reader`, `locked`, `about`, `legal`, `consent`, `not-found`, `support`, `account`. `src: Core features, Translations rule 1`
- [ ] `C-CF-775` `literal` `GET /api/studio/translations/coverage` returns per namespace with locale `total`, `translated`, `reviewed`, `percent`. `src: Core features, Translations rule 2`
- [ ] `C-CF-776` `constraint` In the `legal` namespace only `reviewed` strings count toward translation coverage. `src: Core features, Translations rule 2`
- [ ] `C-CF-777` `constraint` In every other namespace `translated` with `reviewed` strings both count toward translation coverage. `src: Core features, Translations rule 2`
- [ ] `C-CF-778` `literal` `GET /api/studio/translations/{locale}?namespace=` lists each `key` with `source`, `value`, `state`, `note`. `src: Core features, Translations rule 3`
- [ ] `C-CF-779` `literal` `PUT /api/studio/translations/{locale}/{key}` saves `value`, `state`, `note`. `src: Core features, Translations rule 3`
- [ ] `C-CF-780` `constraint` Every named placeholder in a translation source must appear in the translated value exactly once. `src: Core features, Translations rule 4`
- [ ] `C-CF-781` `constraint` A translated value missing or repeating a placeholder is rejected. `src: Core features, Translations rule 4`
- [ ] `C-CF-782` `constraint` A translated value containing `<` or `>` is rejected. `src: Core features, Translations rule 4`
- [ ] `C-CF-783` `constraint` A rejected translation save saves nothing. `src: Core features, Translations rule 4`
- [ ] `C-CF-784` `ui` The console translation screen is a grid with namespaces down the side, locales across the top, coverage in each cell. `src: Core features, Translations rule 5`
- [ ] `C-CF-785` `capability` A translation grid cell below 100 percent opens the cell's missing keys. `src: Core features, Translations rule 5`
- [ ] `C-CF-786` `capability` Chapter titles are edited as transcreations with the previous chapters' titles in both languages beside them. `src: Core features, Translations rule 5`
- [ ] `C-CF-787` `literal` `GET /api/studio/tips` lists tips newest first, `50` per page by default, never more than `200`. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-788` `literal` The studio tip list pages by `next_cursor`. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-789` `data` Each studio tip row carries `id`, `tip_id`, `received_at`, `source`, `amount`, `currency`, `settled_amount`, `rate`, `message`, `supporter_email`, `matched_reader_email`, `match_method`, `entitlement`, `state`. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-790` `literal` Manual tips carry a null `tip_id` in the tip list. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-791` `literal` A tip row `source` is `tipbox` or `manual`. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-792` `literal` `POST /api/studio/tips` records a manual tip with `amount` in `usd`, `received_at`, `reason`. `src: Core features, Supporters, insights and settings rule 3`
- [ ] `C-CF-793` `constraint` A manual tip has `source` `manual`, counts in tip totals, grants nothing. `src: Core features, Supporters, insights and settings rule 3`
- [ ] `C-CF-794` `literal` A tip list row `entitlement` is `granted`, `below_threshold`, `unmatched`, `awaiting_confirmation` or `revoked`. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-795` `literal` A tip list row `state` is `received`, `refunded` or `disputed`. `src: Core features, Supporters, insights and settings rule 1`
- [ ] `C-CF-796` `literal` `POST /api/studio/tips/{id}/confirm-match` confirms an `address` match, applying the entitlement rule. `src: Core features, Supporters, insights and settings rule 2`
- [ ] `C-CF-797` `constraint` Match confirmation is rejected for any other match method. `src: Core features, Supporters, insights and settings rule 2`
- [ ] `C-CF-798` `constraint` A manual tip `amount` that is not a whole number above 0 is rejected naming the field, recording nothing. `src: Core features, Supporters, insights and settings rule 3`
- [ ] `C-CF-799` `constraint` A manual tip with a missing or malformed `received_at` is rejected naming the field. `src: Core features, Supporters, insights and settings rule 3`
- [ ] `C-CF-800` `constraint` A manual tip missing a `reason` is rejected naming the field. `src: Core features, Supporters, insights and settings rule 3`
- [ ] `C-CF-801` `literal` `GET /api/studio/tips/totals` sums `settled_amount` with a count of `received` tips by calendar month `YYYY-MM` in UTC. `src: Core features, Supporters, insights and settings rule 4`
- [ ] `C-CF-802` `capability` Tip totals also group received tips by source. `src: Core features, Supporters, insights and settings rule 4`
- [ ] `C-CF-803` `constraint` Refunded or disputed tips are excluded from tip totals. `src: Core features, Supporters, insights and settings rule 4`
- [ ] `C-CF-804` `literal` `GET /api/studio/overview` returns the four cards `next_drop`, `unready`, `support`, `reading`. `src: Core features, Supporters, insights and settings rule 5`
- [ ] `C-CF-805` `data` The overview `next_drop` card names the next scheduled chapter, the release moment, whether the chapter's preflight passes. `src: Core features, Supporters, insights and settings rule 5`
- [ ] `C-CF-806` `data` The overview `unready` card lists failing preflight rules of every draft, ready or scheduled chapter. `src: Core features, Supporters, insights and settings rule 5`
- [ ] `C-CF-807` `data` The overview `support` card compares the count with total of received tips over the last 30 days against the 30 days before, beside entitlements granted. `src: Core features, Supporters, insights and settings rule 5`
- [ ] `C-CF-808` `constraint` The overview `reading` card shows server chapter opens beside measured completions with abandonments, never summed. `src: Core features, Supporters, insights and settings rule 5`
- [ ] `C-CF-809` `data` The overview carries `alerts` with `revocations`. `src: Core features, Supporters, insights and settings rule 5`
- [ ] `C-CF-810` `literal` `GET /api/studio/settings` reads `name`, `contact_email`, `time_zone`, `early_access_threshold`, `credit_threshold`. `src: Core features, Supporters, insights and settings rule 6`
- [ ] `C-CF-811` `literal` `PATCH /api/studio/settings` changes `name`, `contact_email`, `time_zone`, `early_access_threshold`, `credit_threshold`. `src: Core features, Supporters, insights and settings rule 6`
- [ ] `C-CF-812` `literal` Studio settings show `currency` `usd`, `default_locale` `en`, the `asset_version`. `src: Core features, Supporters, insights and settings rule 6`
- [ ] `C-CF-813` `constraint` A settings threshold that is not a whole number of at least 0 is rejected, changing nothing. `src: Core features, Supporters, insights and settings rule 6`
- [ ] `C-CF-814` `constraint` A settings credit threshold below the early-access threshold is rejected, changing nothing. `src: Core features, Supporters, insights and settings rule 6`
- [ ] `C-CF-815` `constraint` A settings time zone that is not a real zone name is rejected, changing nothing. `src: Core features, Supporters, insights and settings rule 6`
- [ ] `C-CF-816` `literal` `GET /api/studio/integrations/tipbox` returns `page_url`, `secret_last_four`, `secret_created_at`, `secret_last_used_at`. `src: Core features, Supporters, insights and settings rule 7`
- [ ] `C-CF-817` `literal` The seeded Tipbox secret's `secret_last_four` is `81d7`. `src: Core features, Supporters, insights and settings rule 7`
- [ ] `C-CF-818` `constraint` No endpoint ever returns the full Tipbox signing secret. `src: Core features, Supporters, insights and settings rule 7`
- [ ] `C-CF-819` `literal` `PUT /api/studio/integrations/tipbox/secret` rotates the Tipbox signing secret to a new `secret` of at least 16 characters. `src: Core features, Supporters, insights and settings rule 7`
- [ ] `C-CF-820` `literal` After a secret rotation a notification signed with the previous secret answers `401`. `src: Core features, Supporters, insights and settings rule 7`
- [ ] `C-CF-821` `constraint` A rotated secret shorter than 16 characters is rejected naming the field. `src: Core features, Supporters, insights and settings rule 7`
- [ ] `C-CF-822` `literal` `POST /api/studio/asset-version` raises the global asset version by one. `src: Core features, Supporters, insights and settings rule 8`
- [ ] `C-CF-823` `capability` After an asset version raise every manifest gives the new version's image addresses. `src: Core features, Supporters, insights and settings rule 8`
- [ ] `C-CF-824` `literal` After an asset version raise the old version's image addresses answer `404`. `src: Core features, Supporters, insights and settings rule 8`
- [ ] `C-CF-825` `literal` The seeded asset version is `66`. `src: Core features, Supporters, insights and settings rule 8`

## C-UF User flow

- [ ] `C-UF-01` `capability` `/studio/sign-in` serves the author sign-in page. `src: User flow, Routes table`
- [ ] `C-UF-02` `literal` `/studio` shows the overview with `Next drop`, `Unready work`, `Support`, `Reading` cards. `src: User flow, Routes table`
- [ ] `C-UF-03` `literal` `/studio/volumes` shows volume cards with a `New volume` control. `src: User flow, Routes table`
- [ ] `C-UF-04` `literal` `/studio/volumes/:volumeId` shows the chapter table with a `New chapter` control. `src: User flow, Routes table`
- [ ] `C-UF-05` `capability` `/studio/chapters/:chapterId` is the chapter editor for titles, descriptions, cover, boards, waivers, release state. `src: User flow, Routes table`
- [ ] `C-UF-06` `capability` `/studio/chapters/:chapterId/boards/:boardId` is the board editor with a panel filmstrip with a file drop. `src: User flow, Routes table`
- [ ] `C-UF-07` `capability` `/studio/chapters/:chapterId/panels/:panelId` is the panel composer. `src: User flow, Routes table`
- [ ] `C-UF-08` `capability` `/studio/translations` shows the translation coverage grid. `src: User flow, Routes table`
- [ ] `C-UF-09` `capability` `/studio/translations/:locale` is one locale's translation editor. `src: User flow, Routes table`
- [ ] `C-UF-10` `capability` `/studio/releases` shows the release calendar with preflight. `src: User flow, Routes table`
- [ ] `C-UF-11` `capability` `/studio/supporters` shows the tip list with totals. `src: User flow, Routes table`
- [ ] `C-UF-12` `capability` `/studio/insights` shows server counts beside measured events. `src: User flow, Routes table`
- [ ] `C-UF-13` `capability` `/studio/settings` shows studio settings with the asset version. `src: User flow, Routes table`
- [ ] `C-UF-14` `capability` `/studio/settings/integrations` shows the Tipbox page with the signing secret. `src: User flow, Routes table`
- [ ] `C-UF-15` `constraint` `/` with `/fr` are title screens, the root never redirecting by browser language. `src: User flow, Entry and redirects bullet 1`
- [ ] `C-UF-16` `capability` A signed-out visitor opening a `/studio` route other than `/studio/sign-in` is sent to `/studio/sign-in`. `src: User flow, Entry and redirects bullet 2`
- [ ] `C-UF-17` `capability` After studio sign-in the author returns to the studio route first opened. `src: User flow, Entry and redirects bullet 2`
- [ ] `C-UF-18` `capability` Signing out of the studio returns to `/studio/sign-in`. `src: User flow, Entry and redirects bullet 2`
- [ ] `C-UF-19` `capability` A signed-out visitor opening `/account` gets the sign-in dialog over `/chapters`, then the account page after signing in. `src: User flow, Entry and redirects bullet 3`
- [ ] `C-UF-20` `constraint` Apart from `/account` or an expired session, the reader sign-in dialog is offered in exactly three places. `src: User flow, Entry and redirects bullet 4`
- [ ] `C-UF-21` `capability` The reader sign-in dialog is offered by `notify me` on a locked chapter, the end of the last readable chapter, the tip return page. `src: User flow, Entry and redirects bullet 4`
- [ ] `C-UF-22` `constraint` There is no sign-in link in the header. `src: User flow, Entry and redirects bullet 4`
- [ ] `C-UF-23` `capability` Signing in keeps the reader on the page the reader was on. `src: User flow, Entry and redirects bullet 4`
- [ ] `C-UF-24` `capability` When a session expired or was revoked mid-action, the next request is denied. `src: User flow, Entry and redirects bullet 5`
- [ ] `C-UF-25` `capability` After a denied session request the app forgets the session, offering sign-in again without losing the page. `src: User flow, Entry and redirects bullet 5`
- [ ] `C-UF-26` `constraint` A reader whose early access lapsed mid-read sees the locked state on the next chapter request. `src: User flow, Entry and redirects bullet 6`
- [ ] `C-UF-27` `literal` An unpublished chapter's address redirects temporarily to `/chapters`. `src: User flow, Entry and redirects bullet 7`
- [ ] `C-UF-28` `constraint` A locked chapter never reveals a manifest or image, yet the rack shows the chapter's sleeve. `src: User flow, Entry and redirects bullet 8`
- [ ] `C-UF-29` `capability` Journey 1 declines consent, presses `read now`, opens chapter 1 from the rack, reaching `01:05` with four right arrow presses. `src: User flow, Journeys journey 1`
- [ ] `C-UF-30` `capability` Journey 1 shows the next-track face with `under pressure` at `01:05`, opening `/chapter/2` at `02:01`. `src: User flow, Journeys journey 1`
- [ ] `C-UF-31` `capability` Journey 2 reopens `/chapters` with the chapter 2 sleeve selected after chapter 2 was opened. `src: User flow, Journeys journey 2`
- [ ] `C-UF-32` `capability` Journey 3 shows chapter 4 locked to a signed-out visitor with the name line, opening line, `notify me`, `support us`, the chapter 3 sleeve. `src: User flow, Journeys journey 3`
- [ ] `C-UF-33` `capability` Journey 4 signs in as `reader@example.com` from `notify me`, opening chapter 4 in place at `04:01`. `src: User flow, Journeys journey 4`
- [ ] `C-UF-34` `capability` Journey 5 shows the `support us` link to Tipbox carrying a `return_token`. `src: User flow, Journeys journey 5`
- [ ] `C-UF-35` `capability` Journey 5 return page, after sign-in, states the tip status, early access active, pending or not granted. `src: User flow, Journeys journey 5`
- [ ] `C-UF-36` `literal` Journey 6 text mode for chapter 1 lists first `Doudou steps off the night bus into Varny.` `src: User flow, Journeys journey 6`
- [ ] `C-UF-37` `capability` Journey 7 on `/about` presses `FR`, the curtain sweeps, the address becomes `/fr/about` with header links `chapitres` with `a propos`. `src: User flow, Journeys journey 7`
- [ ] `C-UF-38` `literal` Journey 8 creates volume `Vol. II` in the modal, then a chapter titled `the night shift` with `le service de nuit`, then a board. `src: User flow, Journeys journey 8`
- [ ] `C-UF-39` `literal` Journey 8 presses `New board` in the chapter to add a board. `src: User flow, Journeys journey 8`
- [ ] `C-UF-40` `literal` Journey 8 drops `c1b1p1-back.png` with `c1b1p1-stage.png`, the filmstrip showing panel 1 with two layers. `src: User flow, Journeys journey 8`
- [ ] `C-UF-41` `literal` Journey 8 sets the `stage` layer depth to `3`, moving the layer mark on the depth ruler. `src: User flow, Journeys journey 8`
- [ ] `C-UF-42` `capability` Journey 9 adds both panel descriptions with a cover, presses `Mark ready`, then `Run preflight` shows every rule passing. `src: User flow, Journeys journey 9`
- [ ] `C-UF-43` `capability` Journey 9 presses `Publish now`, ending on a full-page confirmation naming the published chapter. `src: User flow, Journeys journey 9`
- [ ] `C-UF-44` `capability` Journey 10 shows the newest tip first on `/studio/supporters` with amount, source, message, match, entitlement beside totals. `src: User flow, Journeys journey 10`
- [ ] `C-UF-45` `literal` Journey 10 shows `Server counts` beside `Measured events` on `/studio/insights`. `src: User flow, Journeys journey 10`
- [ ] `C-UF-46` `capability` Journey 11 changes `consent.accept` in the `fr` consent cell, the cell still reading 100 percent after saving. `src: User flow, Journeys journey 11`
- [ ] `C-UF-47` `capability` Every public route shows the first-load screen on a first visit as the loading state. `src: User flow, States bullet 1`
- [ ] `C-UF-48` `capability` After the first visit the public loading state is a thin bar along the bottom. `src: User flow, States bullet 1`
- [ ] `C-UF-49` `constraint` Nothing but the loading state shows before the scene arrives. `src: User flow, States bullet 1`
- [ ] `C-UF-50` `capability` A rack whose volume list comes back empty shows the recoverable error with a retry. `src: User flow, States bullet 2`
- [ ] `C-UF-51` `constraint` A failed request shows a named, recoverable state with a retry. `src: User flow, States bullet 4`
- [ ] `C-UF-52` `capability` The studio supporter list with no tips shows an empty state saying so. `src: User flow, States bullet 3`
- [ ] `C-UF-53` `capability` The studio page-view list with no views shows an empty state saying so. `src: User flow, States bullet 3`
- [ ] `C-UF-54` `capability` A studio volume with no chapters shows an empty state saying so. `src: User flow, States bullet 3`
- [ ] `C-UF-55` `constraint` No route ever shows a raw error, a stack trace or a key path. `src: User flow, States bullet 4`
- [ ] `C-UF-56` `capability` The studio shows skeleton rows during loading, never a layout-reflowing spinner. `src: User flow, States bullet 5`
- [ ] `C-UF-57` `capability` An empty studio offers the guided path of volume, chapter, board, panel import. `src: User flow, States bullet 5`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The first moment feels like stepping inside a drawn night-time world with the interface almost out of the way. `src: UI/UX notes, North star paragraph`
- [ ] `C-UX-02` `ui` The public site reads as consumer with editorial, the scene seen first, the chrome quiet. `src: UI/UX notes, North star paragraph`
- [ ] `C-UX-03` `ui` The studio console is a plain, fast document application with no scene, no physics, no heavy motion. `src: UI/UX notes, North star paragraph`
- [ ] `C-UX-04` `ui` The language divider with the inactive language buttons are deep neutrals. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-05` `ui` A near-black neutral carries text on light ground, the header, the footer, the wordmark, the entry button. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-06` `ui` A near-white warm neutral with a faint pink tint carries text on dark ground, the entry button label, icons, the page ground. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-07` `ui` The header, footer with fullscreen control turn cream on the title screen, during chapter loading, over the dark about support section. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-08` `ui` On the title screen the language selector alone stays a deep neutral. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-09` `ui` During chapter loading the language selector turns cream. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-10` `ui` Chapter sleeves with the timeline capsule are near-black capsules with white text. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-11` `ui` A locked sleeve is one step lighter, a deep neutral. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-12` `ui` A mid, vivid amber is the one saturated public colour, spent only on the thin loading bar. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-13` `ui` The first-load progress line is a light, soft orange on a near-white warm paper ground. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-14` `ui` The language curtain is a near-white, muted red over a paper-coloured curtain. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-15` `ui` A near-white soft orange appears only as a chip tint. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-16` `constraint` The product offers no dark mode or theme switch. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-17` `constraint` A locked sleeve shows a padlock with the word locked, meaning never carried by colour alone. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-18` `ui` The studio shows failure, warning, success in deep muted red, amber, green, each with an icon with a word. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-19` `ui` The public site wears none of the studio failure, warning or success colours. `src: UI/UX notes, Palette by role paragraph`
- [ ] `C-UX-20` `literal` One type family, `Inter`, variable from 100 to 900, sets all text. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-21` `constraint` The type scale is flat with no ladder of ever larger headings. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-22` `literal` The reader timecode type size is 9.5px in Inter 700. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-23` `literal` The language button type size is 10px in Inter 600. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-24` `literal` The sleeve timecode type size is 12px in Inter 700. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-25` `literal` The sleeve subtitle type size is 14px. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-26` `literal` The header link with footer type size is 15px. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-27` `literal` The tip label type size is 15px in Inter 700. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-28` `literal` The about body type size is 16px. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-29` `literal` The sleeve title type size is 17px in Inter 800 on one line. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-30` `literal` The team card body type size is 18px. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-31` `literal` The reader loading caption with legal paragraph type size is 20px. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-32` `literal` The entry button label type size is 35px in Inter 600. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-33` `literal` The legal page heading type size is 60px with section headings at 30px. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-34` `literal` The four about heading type sizes follow the window width in Inter 900. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-35` `ui` Figures line up in every studio table. `src: UI/UX notes, Typeface and type paragraph`
- [ ] `C-UX-36` `constraint` Spacing is placed by feel against the scene with no grid of spacing constants. `src: UI/UX notes, Shape, spacing and density paragraph`
- [ ] `C-UX-37` `ui` Corners are very round with small language pills, big soft sleeve with timeline capsules, fully round chips, a fully round entry button. `src: UI/UX notes, Shape, spacing and density paragraph`
- [ ] `C-UX-38` `ui` The public site is spacious, almost empty around the scene. `src: UI/UX notes, Shape, spacing and density paragraph`
- [ ] `C-UX-39` `ui` The studio is dense enough that a chapter table fits one screen. `src: UI/UX notes, Shape, spacing and density paragraph`
- [ ] `C-UX-40` `ui` Chrome moves with the browser's own simple transitions, working before the scene has loaded. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-41` `ui` The consent strip slides up, then slides away. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-42` `ui` The four corner controls wait just off screen until consent is answered, then rise together. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-43` `ui` Hovering a header link tips the link a few degrees, the two links in opposite directions, drawing a rounded outline. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-44` `ui` Hovering the consent buttons tips the buttons in opposite directions, decline further than accept. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-45` `ui` Text arrives word by word, rising from behind an invisible edge. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-46` `ui` Sleeves pop in from nothing on the rack. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-47` `ui` Buttons pop in from nothing. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-48` `ui` Leaving the rack shrinks every sleeve before the next page appears. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-49` `ui` Leaving a chapter tips the timeline back, away. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-50` `ui` Leaving the legal page fades the page on a linear curve, leaving the title screen or about page on an ease-out curve. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-51` `ui` Chrome recolouring between grounds is a short colour transition. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-52` `ui` The reader's animated backdrop is a slow, eased charcoal gradient drifting forever. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-53` `constraint` Nothing animates on hover on a touch device. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-54` `constraint` Under reduced motion the camera jumps between panels instead of flying. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-55` `constraint` Under reduced motion the title-screen record stops spinning. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-56` `constraint` Under reduced motion reveals become instant. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-57` `constraint` Under reduced motion the physics pile lies still yet stays draggable. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-58` `constraint` Under reduced motion the team cards face front. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-59` `constraint` Under reduced motion the next-track marquee stops. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-60` `constraint` Under reduced motion the consent strip simply appears. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-61` `constraint` Under reduced motion the surprise is suppressed with the surprise trigger. `src: UI/UX notes, Motion character paragraph`
- [ ] `C-UX-62` `ui` Every control has a resting, pointed-at, pressed, focused, unavailable state. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-63` `constraint` An unavailable control such as `previous panel` on the first panel is dimmed, inert, never signalled by colour alone. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-64` `capability` Every form field has a visible label above the field with the error directly beneath, naming the problem. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-65` `capability` Modal dialogs close on Escape. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-66` `capability` Unpublishing in the studio confirms first, saying what will happen. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-67` `capability` Raising the asset version in the studio confirms first, saying what will happen. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-68` `capability` Rotating the Tipbox signing secret in the studio confirms first, saying what will happen. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-69` `ui` The primary action on each page is the one visually loudest element. `src: UI/UX notes, Components and states paragraph`
- [ ] `C-UX-70` `constraint` All text meets WCAG 2.2 AA contrast, white on the near-black sleeves included. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-71` `ui` Text drawn over the scene carries a thin outline or a solid ground. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-72` `constraint` Full keyboard navigation reaches every control. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-73` `constraint` A visible focus ring has at least 3 to 1 contrast on light with dark grounds. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-74` `constraint` Every icon-only control has a label. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-75` `constraint` Touch targets are at least 44 by 44 pixels of hit area. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-76` `constraint` Assistive-only text is hidden by clipping, never by zero opacity or `display: none`. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-77` `constraint` Every route has one level-one heading. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-78` `capability` A polite live region announces chapter loading, chapter ready, a reached panel's description, a completed language switch. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-79` `capability` An assertive live region announces a failed chapter load. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-80` `capability` An assertive live region announces a rejected studio save. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-81` `constraint` At 200 percent text size the product stays usable, sleeve with timeline titles truncating with an ellipsis, keeping the full title as accessible name. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-82` `constraint` Public pages stay usable without sideways scrolling at a 320 pixel wide viewport. `src: UI/UX notes, Accessibility paragraph`
- [ ] `C-UX-83` `constraint` The layout holds from the narrowest small phone width to a wide desktop with nothing overflowing sideways. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-84` `capability` On a wide desktop the header links sit either side of the centred wordmark with both arrow pairs shown. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-85` `constraint` The responsive layout takes three separate steps, never one mobile layout. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-86` `capability` At tablet width the arrow pairs disappear, reading by drag, keys, slider. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-87` `capability` Slightly narrower, the fullscreen control lifts with the language selector moving to the bottom left. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-88` `capability` At phone width the header links move to the two edges around a smaller wordmark. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-89` `capability` At phone width the tip control moves to the top centre. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-90` `capability` At phone width the rack with the timeline scale down. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-91` `ui` The about page's full-height intro keeps the `Scroll down` prompt inside the visible window. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-92` `constraint` Full-height surfaces follow the window's real visible height as a phone browser bar retracts. `src: UI/UX notes, Responsive paragraph`
- [ ] `C-UX-93` `capability` In portrait orientation the about headings grow to fill more of the width. `src: UI/UX notes, Responsive paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The server answers every page route with an HTML document carrying the route's title, description, `lang`, HTTP status. `src: Technical requirements rendering model`
- [ ] `C-TR-02` `contract` The Preact application renders pages in the browser from the JSON API under `/api` on the same origin. `src: Technical requirements rendering model`
- [ ] `C-TR-03` `contract` The backend is Litestar on Python 3.12 in one server process serving the API, front end, sitemaps, page documents. `src: Technical requirements backend`
- [ ] `C-TR-04` `contract` The front end is served as a production build by the same process as the API. `src: Technical requirements frontend`
- [ ] `C-TR-05` `contract` The front end is Preact with Vite with TypeScript. `src: Technical requirements frontend`
- [ ] `C-TR-06` `contract` Studio data is stored in the PostgreSQL database at `DATABASE_URL`. `src: Technical requirements database`
- [ ] `C-TR-07` `contract` Panel images live in the MinIO object store at `STORAGE_ENDPOINT` in the bucket named by `STORAGE_BUCKET`. `src: Technical requirements object storage`
- [ ] `C-TR-08` `constraint` The storage bucket refuses anonymous requests, staying private. `src: Technical requirements object storage`
- [ ] `C-TR-09` `contract` Auth uses bearer tokens sent as `Authorization: Bearer <token>` from app-implemented email with password sign-in. `src: Technical requirements auth`
- [ ] `C-TR-10` `contract` Readers with authors authenticate in two separate systems. `src: Technical requirements auth`
- [ ] `C-TR-11` `literal` The console keeps a signed-in author's token in local storage under `dd-studio-session`. `src: Technical requirements auth`
- [ ] `C-TR-12` `literal` `GET /api/health` returns `200` with `{"status": "ok"}` once the database with the bucket answer. `src: Technical requirements health`
- [ ] `C-TR-13` `contract` Structured logging writes one JSON line per request on stdout with `request_id`, method, route, status, duration. `src: Technical requirements observability`
- [ ] `C-TR-14` `constraint` Request log lines never carry an address, password, token or signature. `src: Technical requirements observability`
- [ ] `C-TR-15` `contract` The app reads `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`, `DATABASE_URL`, `STORAGE_ENDPOINT`, `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY` from the environment. `src: Technical requirements environment`
- [ ] `C-TR-16` `constraint` The app hardcodes no host, port or credential. `src: Technical requirements environment`
- [ ] `C-TR-17` `constraint` The app uses only the named libraries plus direct dependencies. `src: Technical requirements paragraph 2`
- [ ] `C-TR-18` `constraint` The app introduces no second database, cache, queue, object store, identity provider or mail vendor. `src: Technical requirements paragraph 2`
- [ ] `C-TR-19` `literal` Every `/api` response header carries a request identifier as `X-Request-Id`. `src: Technical requirements bullet 1`
- [ ] `C-TR-20` `literal` Every error body repeats the request identifier as `request_id`. `src: Technical requirements bullet 1`
- [ ] `C-TR-21` `literal` Every rejection answers a client error with the body `{"error": {"code": ..., "message": ..., "field": ..., "request_id": ...}}`. `src: Technical requirements bullet 2`
- [ ] `C-TR-22` `constraint` Business-rule or validation rejections are never a server error or a silent success. `src: Technical requirements bullet 2`
- [ ] `C-TR-23` `data` A version conflict error body adds `current`. `src: Technical requirements bullet 2`
- [ ] `C-TR-24` `data` A preflight rejection error body adds `failures`. `src: Technical requirements bullet 2`
- [ ] `C-TR-25` `data` An import rejection error body adds `file`. `src: Technical requirements bullet 2`
- [ ] `C-TR-26` `data` Every API identifier is a 26-character opaque sortable string. `src: Technical requirements bullet 3`
- [ ] `C-TR-27` `constraint` Chapter, board, panel numbers are small integers, not identifiers. `src: Technical requirements bullet 3`
- [ ] `C-TR-28` `literal` Every response carries `Strict-Transport-Security`. `src: Technical requirements security`
- [ ] `C-TR-29` `literal` Every response carries a `Content-Security-Policy` whose directives hold `frame-ancestors 'none'`. `src: Technical requirements security`
- [ ] `C-TR-30` `literal` Every response carries `X-Frame-Options: DENY`. `src: Technical requirements security`
- [ ] `C-TR-31` `literal` Every response carries `X-Content-Type-Options: nosniff`. `src: Technical requirements security`
- [ ] `C-TR-32` `literal` Every response carries `Referrer-Policy: strict-origin-when-cross-origin`. `src: Technical requirements security`
- [ ] `C-TR-33` `literal` Every response carries a `Permissions-Policy` allowing `fullscreen`, denying everything else unused. `src: Technical requirements security`
- [ ] `C-TR-34` `literal` A published chapter image answers `Cache-Control: public, max-age=31536000, immutable`. `src: Technical requirements caching`
- [ ] `C-TR-35` `literal` A published chapter manifest answers `public` Cache-Control with a one-hour `max-age`. `src: Technical requirements caching`
- [ ] `C-TR-36` `literal` An unpublished chapter manifest answers Cache-Control with both `private` with `no-store`. `src: Technical requirements caching`
- [ ] `C-TR-37` `literal` Every signed image answers Cache-Control with both `private` with `no-store`. `src: Technical requirements caching`
- [ ] `C-TR-38` `literal` Every response depending on a reader token answers Cache-Control with both `private` with `no-store`. `src: Technical requirements caching`
- [ ] `C-TR-39` `literal` Every `/api/me` response answers Cache-Control with both `private` with `no-store`. `src: Technical requirements caching`
- [ ] `C-TR-40` `constraint` The scheduler works on absolute instants, never wall-clock comparisons. `src: Technical requirements scheduler`
- [ ] `C-TR-41` `constraint` A scheduled chapter is published by the app itself within 60 seconds after the release moment, unprompted. `src: Technical requirements scheduler`
- [ ] `C-TR-42` `literal` An image `sig` is the lowercase hexadecimal HMAC-SHA256 of the address with `expires`, keyed with the studio's `image_signing_key`. `src: Technical requirements signatures`
- [ ] `C-TR-43` `constraint` A signature for one image does not open another image. `src: Technical requirements signatures`
- [ ] `C-TR-44` `constraint` No binary asset ships with the build. `src: Technical requirements zero-asset substitution`
- [ ] `C-TR-45` `ui` Seeded panel layers, covers, placeholders are drawn by the app in a flat role colour with a role silhouette, the layer identifier stamped in a corner. `src: Technical requirements zero-asset substitution`
- [ ] `C-TR-46` `literal` The `Inter` font files are bundled into the build, served from the app's own origin. `src: Technical requirements fonts`
- [ ] `C-TR-47` `literal` The font fallback stack is `"Helvetica Neue", Helvetica, Arial, "Liberation Sans", system-ui, sans-serif`. `src: Technical requirements fonts`
- [ ] `C-TR-48` `constraint` Public pages request nothing from another origin such as an analytics host, font service or video embed. `src: Technical requirements network`
- [ ] `C-TR-49` `constraint` The app makes no outbound network call at runtime. `src: Technical requirements network`
- [ ] `C-TR-50` `constraint` The app makes no call to Tipbox at runtime. `src: Technical requirements network`
- [ ] `C-TR-51` `constraint` Seeding never duplicates a row or object across starts. `src: Technical requirements seeding`

## C-DM Data model

- [ ] `C-DM-01` `data` All stored timestamps are UTC instants. `src: Data model paragraph 1`
- [ ] `C-DM-02` `data` Money amounts are integer minor units. `src: Data model paragraph 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`, hashed yet working at login. `src: Data model seed password`
- [ ] `C-DM-04` `contract` `/app/USER_README.md` lists each seeded account with the password. `src: Data model seed password`
- [ ] `C-DM-05` `literal` The seeded studio row holds name `Doudou Fever`, contact `hello@example.com`, time zone `Europe/Paris`. `src: Data model studios`
- [ ] `C-DM-06` `literal` The studio row holds currency `usd` with default locale `en`. `src: Data model studios`
- [ ] `C-DM-07` `literal` The studio row holds `early_access_threshold` `500`, `credit_threshold` `2000`, `asset_version` `66`. `src: Data model studios`
- [ ] `C-DM-08` `constraint` One studio row exists. `src: Data model studios`
- [ ] `C-DM-09` `constraint` The studio `image_signing_key` is 32 random bytes, generated on first start, never returned by any endpoint. `src: Data model studios`
- [ ] `C-DM-10` `constraint` The studio `image_signing_key` is kept across restarts. `src: Data model studios`
- [ ] `C-DM-11` `literal` The seeded locales are `en` `en-GB` `English` with `fr` `fr-FR` `Francais`. `src: Data model locales`
- [ ] `C-DM-12` `data` The `studios` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-13` `data` The `locales` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-14` `data` The `volumes` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-15` `data` The `chapters` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-16` `data` The `chapter_texts` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-17` `data` The `chapter_waivers` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-18` `data` The `boards` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-19` `data` The `panels` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-20` `data` The `panel_descriptions` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-21` `data` The `layers` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-22` `data` The `layer_images` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-23` `data` The `frame_tables` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-24` `data` The `messages` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-25` `data` The `members` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-26` `data` The `studio_sessions` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-27` `data` The `readers` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-28` `data` The `reader_sessions` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-29` `data` The `progress` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-30` `data` The `entitlements` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-31` `data` The `tips` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-32` `data` The `return_tokens` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-33` `data` The `webhook_events` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-34` `data` The `page_views` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-35` `data` The `chapter_opens` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-36` `data` The `measured_events` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-37` `data` The `audit_records` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-38` `data` The `integrations` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-39` `data` The `alerts` table carries every named column of the data model. `src: Data model tables`
- [ ] `C-DM-40` `constraint` Volume `position`, the API `order`, is unique from 1 upward. `src: Data model volumes`
- [ ] `C-DM-41` `constraint` Within a volume two chapters never share a number. `src: Data model invariants`
- [ ] `C-DM-42` `constraint` Within a panel two layers never share a role or draw order. `src: Data model invariants`
- [ ] `C-DM-43` `constraint` Reader email is unique ignoring case. `src: Data model readers`
- [ ] `C-DM-44` `constraint` Within a chapter two boards never share a number. `src: Data model boards`
- [ ] `C-DM-45` `constraint` Within a board two panels never share a number. `src: Data model panels`
- [ ] `C-DM-46` `constraint` Chapter texts hold one row per chapter with locale. `src: Data model chapter_texts`
- [ ] `C-DM-47` `constraint` Panel descriptions hold one row per panel with locale. `src: Data model panel_descriptions`
- [ ] `C-DM-48` `constraint` Layer images hold one row per layer with locale. `src: Data model layer_images`
- [ ] `C-DM-49` `constraint` Messages hold one row per key with locale. `src: Data model messages`
- [ ] `C-DM-50` `literal` A layer `kind` is `image`, `map` or `sprite`. `src: Data model layers`
- [ ] `C-DM-51` `literal` A layer image `locale` is `all` or the locale code of a localised layer image. `src: Data model layer_images`
- [ ] `C-DM-52` `literal` An entitlement `revoked_reason` is `refunded` or `disputed`. `src: Data model entitlements`
- [ ] `C-DM-53` `literal` An entitlement `kind` is `early_access` or `credits`. `src: Data model entitlements`
- [ ] `C-DM-54` `data` No column stores a derived value such as a chapter count, locked flag, hourly open count, byte total, coverage percentage, tip entitlement or panel position. `src: Data model derived`
- [ ] `C-DM-55` `constraint` Two simultaneous deliveries of one Tipbox `tip_id` store exactly one tip row with at most one grant. `src: Data model invariants`
- [ ] `C-DM-56` `constraint` Two deliveries of one verified event `id` record the event once, applying the event once. `src: Data model invariants`
- [ ] `C-DM-57` `constraint` A reader has at most one progress row per chapter, however many writes arrive. `src: Data model invariants`
- [ ] `C-DM-58` `constraint` Two simultaneous progress writes from two devices end in one row holding the merge of both. `src: Data model invariants`
- [ ] `C-DM-59` `constraint` `published_at` never changes once publishing has written the value. `src: Data model invariants`
- [ ] `C-DM-60` `constraint` Two simultaneous publish requests leave exactly one `chapter.published` audit record. `src: Data model invariants`
- [ ] `C-DM-61` `constraint` Two edits to one row carrying the same `version` at the same moment accept exactly one, the other answering `409`. `src: Data model invariants`
- [ ] `C-DM-62` `constraint` Two readers claiming one return token at the same moment leave exactly one successful claim. `src: Data model invariants`
- [ ] `C-DM-63` `constraint` A tip grants each entitlement kind at most once. `src: Data model invariants`
- [ ] `C-DM-64` `literal` The seeded Tipbox integration holds `tbx_whsec_5f3a9c2e81d7` with page `https://tipbox.example/doudou-fever`. `src: Data model seed data`
- [ ] `C-DM-65` `literal` Seeded volume `Vol. I`, order `1`, holds six chapters with the pinned English titles with French titles. `src: Data model seed table`
- [ ] `C-DM-66` `literal` Seeded chapters 1, 2, 3 are `published` with release moments 60, 40, 20 days before first start at `18:00` UTC. `src: Data model seed table`
- [ ] `C-DM-67` `literal` Seeded chapter 4 is `scheduled` 3 days after first start at `18:00` UTC. `src: Data model seed table`
- [ ] `C-DM-68` `literal` Seeded chapter 5 is `scheduled` 20 days after first start at `18:00` UTC. `src: Data model seed table`
- [ ] `C-DM-69` `literal` Seeded chapter 6 is a `draft` with no release moment. `src: Data model seed table`
- [ ] `C-DM-70` `literal` Every seeded chapter's `early_access_days` is `7`. `src: Data model seed data`
- [ ] `C-DM-71` `capability` Seeded chapter 4 is inside the early-access window from the start, chapter 5 outside. `src: Data model seed data`
- [ ] `C-DM-72` `constraint` Seeded chapters 1 to 5 each have a cover, descriptions in both languages, passing all ten preflight rules. `src: Data model seed data`
- [ ] `C-DM-73` `literal` Seeded chapter 6 has one board, one panel, one `back` layer at depth `-4` at draw order `0`, descriptions, no cover. `src: Data model seed data`
- [ ] `C-DM-74` `literal` Seeded chapter 1 has board 1 with panels 1, 2, 3 plus board 2 with panels 1, 2. `src: Data model seed data`
- [ ] `C-DM-75` `literal` Seeded chapters 2 to 5 each have board 1 with panels 1, 2, 3. `src: Data model seed data`
- [ ] `C-DM-76` `literal` Every seeded panel of chapters 1 to 5 has layers `back` at depth `-4` order `0`, `stage` at `0` order `1`, `characters` at `2` order `2`. `src: Data model seed data`
- [ ] `C-DM-77` `literal` Seeded panel 1 of board 1 of chapter 1 also has a localised `sign` layer at depth `1` order `3` with English with French images. `src: Data model seed data`
- [ ] `C-DM-78` `literal` Every seeded layer has kind `image`, offsets `0`, scale `1`, opacity `1`, blend `normal`. `src: Data model seed data`
- [ ] `C-DM-79` `literal` Every seeded panel is `selectable`, with hold with wide false, `entry_duration` `0.6`, camera position `0`. `src: Data model seed data`
- [ ] `C-DM-80` `constraint` Every seeded image is stored in the bucket at the image's key. `src: Data model seed data`
- [ ] `C-DM-81` `literal` Seeded chapter 1 description reads `Doudou arrives in Varny with a suitcase full of records.` in English. `src: Data model chapter descriptions table`
- [ ] `C-DM-82` `literal` Seeded chapter 1 description reads `Doudou arrive a Varny avec une valise pleine de disques.` in French. `src: Data model chapter descriptions table`
- [ ] `C-DM-83` `literal` Seeded chapter 2 description reads `The first gig goes wrong in every possible way.` in English. `src: Data model chapter descriptions table`
- [ ] `C-DM-84` `literal` Seeded chapter 2 description reads `Le premier concert tourne mal de toutes les facons.` in French. `src: Data model chapter descriptions table`
- [ ] `C-DM-85` `literal` Seeded chapter 3 description reads `A night without sleep before the big audition.` in English. `src: Data model chapter descriptions table`
- [ ] `C-DM-86` `literal` Seeded chapter 3 description reads `Une nuit blanche avant la grande audition.` in French. `src: Data model chapter descriptions table`
- [ ] `C-DM-87` `capability` Seeded chapter 4 description holds the pinned English text. `src: Data model chapter descriptions table`
- [ ] `C-DM-88` `literal` Seeded chapter 4 description reads `Doudou efface tout le set et recommence.` in French. `src: Data model chapter descriptions table`
- [ ] `C-DM-89` `literal` Seeded chapter 5 description reads `The crowd finally dances.` in English. `src: Data model chapter descriptions table`
- [ ] `C-DM-90` `literal` Seeded chapter 5 description reads `La foule danse enfin.` in French. `src: Data model chapter descriptions table`
- [ ] `C-DM-91` `capability` Seeded chapter 6 description holds the pinned English text. `src: Data model chapter descriptions table`
- [ ] `C-DM-92` `literal` Seeded chapter 6 description reads `Jean-Loic et Milan preparent la plus grande fete de Varny.` in French. `src: Data model chapter descriptions table`
- [ ] `C-DM-93` `literal` Seeded panel description for chapter 1, board 1, panel 1 reads `Doudou steps off the night bus into Varny.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-94` `literal` Seeded panel description for chapter 1, board 1, panel 1 reads `Doudou descend du bus de nuit a Varny.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-95` `capability` Seeded panel description for chapter 1, board 1, panel 2 holds the pinned English text. `src: Data model panel descriptions table`
- [ ] `C-DM-96` `literal` Seeded panel description for chapter 1, board 1, panel 2 reads `L'appartement au-dessus du bar est petit et bruyant.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-97` `capability` Seeded panel description for chapter 1, board 1, panel 3 holds the pinned English text. `src: Data model panel descriptions table`
- [ ] `C-DM-98` `literal` Seeded panel description for chapter 1, board 1, panel 3 reads `Jean-Loic donne a Doudou une cle et un avertissement.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-99` `literal` Seeded panel description for chapter 1, board 2, panel 1 reads `Milan films dinner for her followers.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-100` `literal` Seeded panel description for chapter 1, board 2, panel 1 reads `Milan filme le diner pour ses abonnes.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-101` `literal` Seeded panel description for chapter 1, board 2, panel 2 reads `Doudou unpacks the turntables on the kitchen table.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-102` `literal` Seeded panel description for chapter 1, board 2, panel 2 reads `Doudou deballe les platines sur la table de la cuisine.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-103` `literal` Seeded panel description for chapter 2, board 1, panel 1 reads `The speakers crackle before the first song.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-104` `literal` Seeded panel description for chapter 2, board 1, panel 1 reads `Les enceintes gresillent avant le premier morceau.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-105` `literal` Seeded panel description for chapter 2, board 1, panel 2 reads `Nobody on the dance floor moves.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-106` `literal` Seeded panel description for chapter 2, board 1, panel 2 reads `Personne ne bouge sur la piste.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-107` `literal` Seeded panel description for chapter 2, board 1, panel 3 reads `Doudou pulls the plug in a panic.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-108` `literal` Seeded panel description for chapter 2, board 1, panel 3 reads `Doudou debranche tout en panique.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-109` `literal` Seeded panel description for chapter 3, board 1, panel 1 reads `Doudou counts beats instead of sheep.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-110` `literal` Seeded panel description for chapter 3, board 1, panel 1 reads `Doudou compte des temps au lieu des moutons.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-111` `literal` Seeded panel description for chapter 3, board 1, panel 2 reads `Milan brings midnight pancakes.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-112` `literal` Seeded panel description for chapter 3, board 1, panel 2 reads `Milan apporte des crepes de minuit.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-113` `literal` Seeded panel description for chapter 3, board 1, panel 3 reads `The sun rises over an unfinished mix.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-114` `literal` Seeded panel description for chapter 3, board 1, panel 3 reads `Le soleil se leve sur un mix inacheve.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-115` `literal` Seeded panel description for chapter 4, board 1, panel 1 reads `Doudou deletes every track on the laptop.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-116` `literal` Seeded panel description for chapter 4, board 1, panel 1 reads `Doudou efface chaque morceau de l'ordinateur.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-117` `literal` Seeded panel description for chapter 4, board 1, panel 2 reads `Jean-Loic hums a tune from the bar.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-118` `literal` Seeded panel description for chapter 4, board 1, panel 2 reads `Jean-Loic fredonne un air du bar.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-119` `literal` Seeded panel description for chapter 4, board 1, panel 3 reads `A new beat starts with that tune.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-120` `literal` Seeded panel description for chapter 4, board 1, panel 3 reads `Un nouveau rythme nait de cet air.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-121` `literal` Seeded panel description for chapter 5, board 1, panel 1 reads `The whole town queues outside the bar.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-122` `literal` Seeded panel description for chapter 5, board 1, panel 1 reads `Toute la ville fait la queue devant le bar.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-123` `literal` Seeded panel description for chapter 5, board 1, panel 2 reads `Doudou drops the first beat.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-124` `literal` Seeded panel description for chapter 5, board 1, panel 2 reads `Doudou lance le premier rythme.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-125` `literal` Seeded panel description for chapter 5, board 1, panel 3 reads `Varny dances until morning.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-126` `literal` Seeded panel description for chapter 5, board 1, panel 3 reads `Varny danse jusqu'au matin.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-127` `literal` Seeded panel description for chapter 6, board 1, panel 1 reads `Posters for the big mix cover the flat.` in English. `src: Data model panel descriptions table`
- [ ] `C-DM-128` `literal` Seeded panel description for chapter 6, board 1, panel 1 reads `Les affiches du grand mix couvrent l'appartement.` in French. `src: Data model panel descriptions table`
- [ ] `C-DM-129` `literal` Seeded tip `tbx_seed_001` came from `reader@example.com` 2 days before first start, amount `800` `usd`, settled `800`, rate `1.000000`, message `go doudou go`, matched by token, `received`. `src: Data model seed tips`
- [ ] `C-DM-130` `literal` Seeded tip `tbx_seed_002` came from `friend@example.com` 1 day before first start, amount `300` `usd`, settled `300`, rate `1.000000`, message `for the bus scene`, match `none`, `received`, granting nothing. `src: Data model seed tips`
- [ ] `C-DM-131` `literal` Seeded reader `reader2@example.com` has progress `0.400` with last panel `2` on chapter 1, the last chapter 1 day before first start. `src: Data model seed tips`
- [ ] `C-DM-132` `literal` Every seeded interface string exists in both languages as `reviewed`. `src: Data model seed tips`
- [ ] `C-DM-133` `constraint` Seeding is idempotent, a restart never duplicating rows or objects. `src: Data model seed tips`

## C-FE Front-end specification

- [ ] `C-FE-01` `capability` The fixed header centres the `Doudou Fever` wordmark. `src: Front-end specification header`
- [ ] `C-FE-02` `literal` The byline `chrome.byline` sits beneath the wordmark for machines with selection. `src: Front-end specification header`
- [ ] `C-FE-03` `literal` The header link `chapters` sits left of the wordmark with `about` to the right. `src: Front-end specification header`
- [ ] `C-FE-04` `capability` The active header link is heavier. `src: Front-end specification header`
- [ ] `C-FE-05` `capability` The wordmark links to `/` except on the title screen, where the wordmark does not navigate. `src: Front-end specification header`
- [ ] `C-FE-06` `capability` At phone width the two header links move to the two edges. `src: Front-end specification header`
- [ ] `C-FE-07` `ui` The wordmark is two lines of heavy lowercase lettering. `src: Front-end specification header`
- [ ] `C-FE-08` `literal` The footer is one link, `legal notice & terms of use`, in the bottom right corner. `src: Front-end specification footer`
- [ ] `C-FE-09` `ui` The footer link underline grows from the link centre on hover. `src: Front-end specification footer`
- [ ] `C-FE-10` `literal` The language selector shows `EN` then a divider then `FR`, uppercase. `src: Front-end specification corner controls`
- [ ] `C-FE-11` `literal` The fullscreen control is named `enter fullscreen` or `exit fullscreen`. `src: Front-end specification corner controls`
- [ ] `C-FE-12` `constraint` All four corner controls wait off screen until the consent strip is answered. `src: Front-end specification corner controls`
- [ ] `C-FE-13` `constraint` The fullscreen control is absent where the browser offers no fullscreen. `src: Front-end specification corner controls`
- [ ] `C-FE-14` `ui` The fullscreen control is drawn as four arrowheads pointing into or out of the corners. `src: Front-end specification corner controls`
- [ ] `C-FE-15` `capability` Two invisible edge strips swallow a drag starting right at the left or right edge. `src: Front-end specification edge strips`
- [ ] `C-FE-16` `constraint` A sideways drag through a chapter is never taken by the browser as back or forward. `src: Front-end specification edge strips`
- [ ] `C-FE-17` `capability` Every icon is drawn inline, taking the current colour. `src: Front-end specification iconography`
- [ ] `C-FE-18` `ui` The sleeve play icon is a triangle with the back edge pinched inward, reused squeezed as the next-panel icon. `src: Front-end specification iconography`
- [ ] `C-FE-19` `ui` The arrows are a double chevron with a leading bar, mirrored for previous. `src: Front-end specification iconography`
- [ ] `C-FE-20` `ui` Locked sleeves show a padlock with a round shackle. `src: Front-end specification iconography`
- [ ] `C-FE-21` `ui` The about scroll prompt is a rounded down arrow with the loading line a thin rule with one small step. `src: Front-end specification iconography`
- [ ] `C-FE-22` `ui` The first-load screen shows a ghost wordmark, the hero's head pulling faces, a stepped rule filling from the left in soft orange. `src: Front-end specification first-load screen`
- [ ] `C-FE-23` `capability` After the first load the in-page loader is only a thin amber bar along the bottom edge. `src: Front-end specification first-load screen`
- [ ] `C-FE-24` `ui` The title-screen record spins slowly above the centre. `src: Front-end specification title screen composition`
- [ ] `C-FE-25` `capability` The title-screen record is hidden at narrow widths. `src: Front-end specification title screen composition`
- [ ] `C-FE-26` `ui` `read now` is a large near-black capsule button with a cream label near the bottom. `src: Front-end specification title screen composition`
- [ ] `C-FE-27` `ui` Behind the title screen a night scene shows a looping sky, a moon, a city silhouette, a vegetable field, a stage with speakers, fireflies, Doudou with two flatmates. `src: Front-end specification title screen composition`
- [ ] `C-FE-28` `ui` The rack is a curved carousel under gentle perspective, the centred sleeve facing the reader, the others turned slightly away. `src: Front-end specification rack composition`
- [ ] `C-FE-29` `ui` Each sleeve is a near-black capsule with the play icon on the left beside a text column of title, subtitle, timecode. `src: Front-end specification rack composition`
- [ ] `C-FE-30` `capability` On wide screens each sleeve carries two small arrows on the right, the first disabled on the first sleeve, the second on the last. `src: Front-end specification rack composition`
- [ ] `C-FE-31` `capability` A locked sleeve shows a not-allowed cursor. `src: Front-end specification rack composition`
- [ ] `C-FE-32` `ui` The tip control is a pill with a thin cream border brightening toward white on hover. `src: Front-end specification rack composition`
- [ ] `C-FE-33` `ui` The tip label rolls up on hover to reveal a larger cream second copy like a departure board. `src: Front-end specification rack composition`
- [ ] `C-FE-34` `constraint` The tip label roll never happens on touch. `src: Front-end specification rack composition`
- [ ] `C-FE-35` `capability` Reader wheel input on both axes maps continuously to the single horizontal position. `src: Front-end specification reader`
- [ ] `C-FE-36` `capability` Settling on a rack sleeve snaps the sleeve into place. `src: Front-end specification reader`
- [ ] `C-FE-37` `ui` The reader capsule looks like a music player with the cover, title, subtitle, white progress line. `src: Front-end specification reader`
- [ ] `C-FE-38` `ui` The reader capsule pulses gently during streaming. `src: Front-end specification reader`
- [ ] `C-FE-39` `capability` On wide screens the two arrow controls sit just right of the capsule. `src: Front-end specification reader`
- [ ] `C-FE-40` `capability` Clicking a panel flies the camera to frame the panel, Escape flying back out. `src: Front-end specification reader`
- [ ] `C-FE-41` `constraint` Panel selection is refused during the chapter's first with last tenth. `src: Front-end specification reader`
- [ ] `C-FE-42` `constraint` A second input within a moment of a selection is swallowed, so mashing an arrow key never skips panels. `src: Front-end specification reader`
- [ ] `C-FE-43` `ui` Near layers slide past faster than far layers continuously, with no jump when a panel becomes selected. `src: Front-end specification reader`
- [ ] `C-FE-44` `ui` About headings carry a thin cream outline so black lettering stays readable over the drawings. `src: Front-end specification about`
- [ ] `C-FE-45` `ui` The team cards are rotated rounded title pills over body text with two social icons, the second card mirroring the first. `src: Front-end specification about`
- [ ] `C-FE-46` `ui` The about support section is dark. `src: Front-end specification about`
- [ ] `C-FE-47` `ui` Everything in the chrome turns cream when the dark support section is in view. `src: Front-end specification about`
- [ ] `C-FE-48` `ui` Each about chip is a pill with the same rolling label as the tip control. `src: Front-end specification about`
- [ ] `C-FE-49` `ui` The not-found page shows a dark gradient from near-black to deep neutral with one drawing behind the text. `src: Front-end specification not-found composition`
- [ ] `C-FE-50` `ui` The not-found line is cream with `Go back to home` as a cream pill turning inside out on hover. `src: Front-end specification not-found composition`
- [ ] `C-FE-51` `literal` The studio console has a left rail of seven destinations `overview`, `volumes`, `translations`, `releases`, `supporters`, `insights`, `settings`. `src: Front-end specification studio console`
- [ ] `C-FE-52` `capability` The studio header bar shows the studio name `Doudou Fever`, a search field, the signed-in author's initials. `src: Front-end specification studio console`
- [ ] `C-FE-53` `literal` The studio chapter table columns are `Number`, `Title`, `State`, `Release`, `Readiness`, `Image bytes`. `src: Front-end specification studio console`
- [ ] `C-FE-54` `capability` The board editor is a filmstrip of panel thumbnails each showing a layer count. `src: Front-end specification studio console`
- [ ] `C-FE-55` `capability` A board editor panel thumbnail carries a warning mark for any failing preflight rule. `src: Front-end specification studio console`
- [ ] `C-FE-56` `capability` The panel composer shows a live preview of the real panel across two thirds of the width. `src: Front-end specification studio console`
- [ ] `C-FE-57` `capability` The panel composer lists layers back to front on the right with role, thumbnail, depth, visibility, solo, lock toggles. `src: Front-end specification studio console`
- [ ] `C-FE-58` `capability` The panel composer shows the selected layer's properties below the layer list. `src: Front-end specification studio console`
- [ ] `C-FE-59` `capability` The panel composer shows a depth ruler under the preview with every layer as a draggable mark at the layer depth. `src: Front-end specification studio console`
- [ ] `C-FE-60` `capability` The panel composer carries a parallax scrubber sweeping the camera across the panel. `src: Front-end specification studio console`
- [ ] `C-FE-61` `capability` The releases screen is a month calendar with a list beneath. `src: Front-end specification studio console`
- [ ] `C-FE-62` `literal` The insights screen shows `Server counts` with `Measured events` in two columns. `src: Front-end specification studio console`
- [ ] `C-FE-63` `capability` Creating a volume, chapter or board, recording a manual tip, adding a waiver each open a modal dialog. `src: Front-end specification studio console`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` One studio row exists with two languages, `en` with `fr`. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` A third language is addable as data. `src: Constraints bullet 1`
- [ ] `C-CN-03` `constraint` The app sends no outbound mail of any kind. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` `notify me` only records the drop preference. `src: Constraints bullet 2`
- [ ] `C-CN-05` `constraint` The studio offers no second factor, recovery codes, invitations or team management. `src: Constraints bullet 3`
- [ ] `C-CN-06` `constraint` No page offers comments, a social graph, user-generated content, a store, a checkout, a native app, animation authoring, advertising or audio. `src: Constraints bullet 4`
- [ ] `C-CN-07` `constraint` No page offers a payment form inside the app. `src: Constraints bullet 5`
- [ ] `C-CN-08` `constraint` Money arrives only as Tipbox notifications or manual tips. `src: Constraints bullet 5`
- [ ] `C-CN-09` `constraint` The app makes no outbound Tipbox call, reconciliation pull or outbound studio webhook. `src: Constraints bullet 6`
- [ ] `C-CN-10` `constraint` The studio offers no deletion of chapters, boards or panels. `src: Constraints bullet 7`
- [ ] `C-CN-11` `constraint` The studio offers no chapter renumbering. `src: Constraints bullet 7`
- [ ] `C-CN-12` `constraint` The app accepts no debug query parameters. `src: Constraints bullet 8`
- [ ] `C-CN-13` `constraint` No rate limiting or quota applies beyond the sign-in lockout. `src: Constraints bullet 9`
- [ ] `C-CN-14` `constraint` Abuse control is the signup decoy field with the sign-in lockout. `src: Constraints bullet 9`
- [ ] `C-CN-15` `constraint` Pages use no third-party analytics, font service or video embed. `src: Constraints bullet 10`
- [ ] `C-CN-16` `constraint` Images are stored as PNGs with no texture compression formats, reduced variants or hardware classes. `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `contract` The HTTP API is served on the same origin under the `/api` prefix, reachable with the app. `src: Deployment contract bullet 2`
- [ ] `C-DC-03` `literal` The server is reachable from outside the container, bound to `0.0.0.0`, never `127.0.0.1` or `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-04` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173` with `4173` the container-internal port. `src: Deployment contract bullet 1`
- [ ] `C-DC-05` `contract` Both ports are read from the environment, never hardcoded. `src: Deployment contract bullet 1`
- [ ] `C-DC-06` `literal` `GET /api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-07` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-08` `contract` `/app/USER_README.md` holds the login credentials. `src: Deployment contract bullet 5`
- [ ] `C-DC-09` `contract` Reserved `.browser_screenshots/` with `.downloads/` directories exist at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `contract` A production build is served behind a static or preview server, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-11` `contract` The server keeps running after the session ends, not a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-12` `contract` The backing services are used where already running, never downloaded, installed, compiled or started. `src: Deployment contract bullet 10`
- [ ] `C-DC-13` `contract` Only the providers named in the brief are used, with no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-14` `contract` No persistent volumes, fixed container names or custom networks are used. `src: Deployment contract bullet 12`
- [ ] `C-DC-15` `constraint` API response field names are exact. `src: Deployment contract API shapes`
- [ ] `C-DC-16` `constraint` An invalid or unauthorized call is rejected as a client error, never a server error or silent success. `src: Deployment contract API shapes`
- [ ] `C-DC-17` `constraint` An anonymous call lacking bearer auth is denied on every `/api/me` with `/api/studio` endpoint except the two sign-in endpoints. `src: Deployment contract API shapes`
- [ ] `C-DC-18` `constraint` The Tipbox webhook authenticates by signature, never by a token. `src: Deployment contract API shapes`
- [ ] `C-DC-19` `literal` A paged list returns `{"items": [...], "next_cursor": ...}`, with `cursor` fetching the next page. `src: Deployment contract API shapes`
- [ ] `C-DC-20` `constraint` API response shapes are stable, a field never renamed or removed. `src: Deployment contract API shapes`
- [ ] `C-DC-21` `constraint` Panel images are stored in the bucket, not on the container filesystem or in database blobs. `src: Deployment contract No mocks`
- [ ] `C-DC-22` `constraint` A manifest endpoint serving every chapter, hiding locked ones only in the page, is refused as a design. `src: Deployment contract No mocks`
- [ ] `C-DC-23` `constraint` An unsigned guessed image address for an unreleased chapter is refused. `src: Deployment contract No mocks`
- [ ] `C-DC-24` `constraint` Visiting a return page grants no early access. `src: Deployment contract No mocks`
- [ ] `C-DC-25` `constraint` No tip is recorded from a body whose signature was never checked. `src: Deployment contract No mocks`
- [ ] `C-DC-26` `constraint` A signature checked against re-serialised JSON rather than the received bytes is refused. `src: Deployment contract No mocks`
- [ ] `C-DC-27` `constraint` A replayed or duplicate delivery stores no second tip row. `src: Deployment contract No mocks`
- [ ] `C-DC-28` `constraint` A published chapter is published on the server, the chapter manifest served to every visitor. `src: Deployment contract No mocks`
- [ ] `C-DC-29` `data` The `GET /api/health` API response shape is `{"status": "ok"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-30` `data` The `GET /api/volumes` API request fields are `locale`, optional reader bearer. `src: Deployment contract, API shapes table`
- [ ] `C-DC-31` `data` The `GET /api/volumes` API response shape is an array of `{"id", "label", "order", "chapter_count", "chapters": [{"number", "title", "locked", "release_at", "cover_url"}]}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-32` `data` The `GET /api/volumes/{order}/chapters/{number}` API request fields are `locale`, optional reader bearer. `src: Deployment contract, API shapes table`
- [ ] `C-DC-33` `data` The `GET /api/volumes/{order}/chapters/{number}` API response shape is `{"volume", "number", "title", "description", "total", "content_tag", "boards": [{"number", "panels": [{"number", "index", "description", "selectable", "layers": [{"role", "identifier", "kind", "depth", "offset_x", "offset_y", "scale", "opacity", "blend", "draw_order", "image_url", "frame_table_url"}]}]}]}`, or `404`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-34` `data` The `GET /api/textures/v{asset_version}/{order}/{number}/{file_identifier}.png` API request fields are `tag`, `expires` plus `sig` when not published. `src: Deployment contract, API shapes table`
- [ ] `C-DC-35` `data` The `GET /api/textures/v{asset_version}/{order}/{number}/{file_identifier}.png` API response shape is PNG bytes, or `404`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-36` `data` The `GET /api/textures/v{asset_version}/{order}/{number}/{file_identifier}.json` API request fields are `tag`, `expires` plus `sig` when not published. `src: Deployment contract, API shapes table`
- [ ] `C-DC-37` `data` The `GET /api/textures/v{asset_version}/{order}/{number}/{file_identifier}.json` API response shape is frame table JSON, or `404`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-38` `data` The `GET /api/covers/{order}/{number}.png` API response shape is PNG bytes, or `404`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-39` `data` The `GET /api/catalogue/{locale}` API response shape is flat object of dotted keys to strings. `src: Deployment contract, API shapes table`
- [ ] `C-DC-40` `data` The `POST /api/page-views` API request fields are `{"route"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-41` `data` The `POST /api/page-views` API response shape is created. `src: Deployment contract, API shapes table`
- [ ] `C-DC-42` `data` The `POST /api/events` API request fields are `{"name", "params"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-43` `data` The `POST /api/events` API response shape is created. `src: Deployment contract, API shapes table`
- [ ] `C-DC-44` `data` The `POST /api/tips/return-tokens` API response shape is `{"token", "expires_at"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-45` `data` The `POST /api/tips/return` API request fields are `{"token"}`, optional reader bearer. `src: Deployment contract, API shapes table`
- [ ] `C-DC-46` `data` The `POST /api/tips/return` API response shape is `{"status"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-47` `data` The `POST /api/webhooks/tipbox` API request fields are raw body, `Tipbox-Signature` header. `src: Deployment contract, API shapes table`
- [ ] `C-DC-48` `data` The `POST /api/webhooks/tipbox` API response shape is `200`, or `401`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-49` `data` The `POST /api/auth/register` API request fields are `{"email", "password", "locale", "website"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-50` `data` The `POST /api/auth/register` API response shape is `{"access_token"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-51` `data` The `POST /api/auth/login` API request fields are `{"email", "password"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-52` `data` The `POST /api/auth/login` API response shape is `{"access_token"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-53` `data` The `POST /api/auth/logout` API response shape is no content. `src: Deployment contract, API shapes table`
- [ ] `C-DC-54` `data` The `GET /api/me` API response shape is `{"email", "locale", "notifications", "created_at"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-55` `data` The `PATCH /api/me` API request fields are `{"email", "locale", "notifications"}`, any subset. `src: Deployment contract, API shapes table`
- [ ] `C-DC-56` `data` The `PATCH /api/me` API response shape is the reader. `src: Deployment contract, API shapes table`
- [ ] `C-DC-57` `data` The `GET /api/me/progress` API response shape is `{"last_chapter", "last_chapter_at", "chapters": [{"volume", "chapter", "fraction", "last_panel", "updated_at"}]}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-58` `data` The `PUT /api/me/progress` API request fields are the progress document. `src: Deployment contract, API shapes table`
- [ ] `C-DC-59` `data` The `PUT /api/me/progress` API response shape is the merged document. `src: Deployment contract, API shapes table`
- [ ] `C-DC-60` `data` The `GET /api/me/entitlements` API response shape is an array of `{"kind", "granted_at", "expires_at", "revoked_at", "active"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-61` `data` The `POST /api/me/notify` API request fields are `{"volume", "chapter"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-62` `data` The `POST /api/me/notify` API response shape is the reader. `src: Deployment contract, API shapes table`
- [ ] `C-DC-63` `data` The `GET /api/me/export` API response shape is attachment `{"reader", "progress", "entitlements", "tips"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-64` `data` The `DELETE /api/me` API request fields are `{"password"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-65` `data` The `DELETE /api/me` API response shape is no content. `src: Deployment contract, API shapes table`
- [ ] `C-DC-66` `data` The `POST /api/studio/auth/login` API request fields are `{"email", "password"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-67` `data` The `POST /api/studio/auth/login` API response shape is `{"access_token", "member": {"email", "name"}}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-68` `data` The `POST /api/studio/auth/logout` API response shape is no content. `src: Deployment contract, API shapes table`
- [ ] `C-DC-69` `data` The `GET /api/studio/overview` API response shape is `{"next_drop", "unready", "support", "reading", "alerts", "revocations"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-70` `data` The `GET /api/studio/search` API request fields are `q`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-71` `data` The `GET /api/studio/search` API response shape is an array of `{"type", "label", "href"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-72` `data` The `GET /api/studio/volumes` API response shape is an array of `{"id", "label", "order", "chapter_count"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-73` `data` The `POST /api/studio/volumes` API request fields are `{"label"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-74` `data` The `POST /api/studio/volumes` API response shape is the volume. `src: Deployment contract, API shapes table`
- [ ] `C-DC-75` `data` The `GET /api/studio/volumes/{id}/chapters` API response shape is an array of `{"id", "number", "titles", "state", "release_at", "published_at", "boards_ready", "boards_total", "image_bytes", "version"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-76` `data` The `POST /api/studio/volumes/{id}/chapters` API request fields are `{"titles": {"en", "fr"}, "descriptions": {"en", "fr"}}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-77` `data` The `POST /api/studio/volumes/{id}/chapters` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-78` `data` The `GET /api/studio/chapters/{id}` API response shape is the chapter with `boards`, `waivers`, `early_access_days`, `content_tag`, `has_cover`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-79` `data` The `PATCH /api/studio/chapters/{id}` API request fields are `{"version", "titles", "descriptions", "early_access_days", "waivers"}`, `version` plus any subset. `src: Deployment contract, API shapes table`
- [ ] `C-DC-80` `data` The `PATCH /api/studio/chapters/{id}` API response shape is the chapter, or `409`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-81` `data` The `PUT /api/studio/chapters/{id}/cover` API request fields are multipart `file`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-82` `data` The `PUT /api/studio/chapters/{id}/cover` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-83` `data` The `POST /api/studio/chapters/{id}/boards` API request fields are `{"name"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-84` `data` The `POST /api/studio/chapters/{id}/boards` API response shape is `{"id", "number"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-85` `data` The `GET /api/studio/boards/{id}` API response shape is the board with `panels` plus their `layers`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-86` `data` The `POST /api/studio/boards/{id}/imports` API request fields are multipart `files`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-87` `data` The `POST /api/studio/boards/{id}/imports` API response shape is `{"panels_created", "layers"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-88` `data` The `PATCH /api/studio/panels/{id}` API request fields are `version` plus any panel field. `src: Deployment contract, API shapes table`
- [ ] `C-DC-89` `data` The `PATCH /api/studio/panels/{id}` API response shape is the panel, or `409`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-90` `data` The `PATCH /api/studio/layers/{id}` API request fields are `version` plus any layer field. `src: Deployment contract, API shapes table`
- [ ] `C-DC-91` `data` The `PATCH /api/studio/layers/{id}` API response shape is the layer, or `409`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-92` `data` The `GET /api/studio/chapters/{id}/manifest` API request fields are `locale`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-93` `data` The `GET /api/studio/chapters/{id}/manifest` API response shape is the manifest, drafts included. `src: Deployment contract, API shapes table`
- [ ] `C-DC-94` `data` The `POST /api/studio/chapters/{id}/preflight` API response shape is `{"passed", "failures": [{"rule", "message"}]}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-95` `data` The `POST /api/studio/chapters/{id}/ready` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-96` `data` The `POST /api/studio/chapters/{id}/schedule` API request fields are `{"release_at"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-97` `data` The `POST /api/studio/chapters/{id}/schedule` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-98` `data` The `POST /api/studio/chapters/{id}/cancel` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-99` `data` The `POST /api/studio/chapters/{id}/publish` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-100` `data` The `POST /api/studio/chapters/{id}/unpublish` API response shape is the chapter. `src: Deployment contract, API shapes table`
- [ ] `C-DC-101` `data` The `GET /api/studio/translations/coverage` API response shape is an array of `{"namespace", "locale", "total", "translated", "reviewed", "percent"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-102` `data` The `GET /api/studio/translations/{locale}` API request fields are `namespace`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-103` `data` The `GET /api/studio/translations/{locale}` API response shape is an array of `{"key", "source", "value", "state", "note"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-104` `data` The `PUT /api/studio/translations/{locale}/{key}` API request fields are `{"value", "state", "note"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-105` `data` The `PUT /api/studio/translations/{locale}/{key}` API response shape is the entry. `src: Deployment contract, API shapes table`
- [ ] `C-DC-106` `data` The `GET /api/studio/tips` API request fields are `limit`, `cursor`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-107` `data` The `GET /api/studio/tips` API response shape is `{"items": [{"id", "tip_id", "received_at", "source", "amount", "currency", "settled_amount", "rate", "message", "supporter_email", "matched_reader_email", "match_method", "entitlement", "state"}], "next_cursor"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-108` `data` The `POST /api/studio/tips` API request fields are `{"amount", "received_at", "reason"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-109` `data` The `POST /api/studio/tips` API response shape is the tip. `src: Deployment contract, API shapes table`
- [ ] `C-DC-110` `data` The `POST /api/studio/tips/{id}/confirm-match` API response shape is the tip. `src: Deployment contract, API shapes table`
- [ ] `C-DC-111` `data` The `GET /api/studio/tips/totals` API response shape is `{"by_month": [{"month", "count", "total"}], "by_source": [{"source", "count", "total"}]}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-112` `data` The `GET /api/studio/insights` API response shape is `{"server": {"page_views": [{"route", "hour", "count"}], "chapter_opens": [{"volume", "chapter", "hour", "count"}]}, "measured": {"events": [{"name", "count"}]}}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-113` `data` The `GET /api/studio/page-views` API request fields are `route`, `limit`, `cursor`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-114` `data` The `GET /api/studio/page-views` API response shape is `{"items": [{"route", "viewed_at"}], "next_cursor"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-115` `data` The `GET /api/studio/settings` API response shape is `{"name", "contact_email", "time_zone", "currency", "default_locale", "early_access_threshold", "credit_threshold", "asset_version"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-116` `data` The `PATCH /api/studio/settings` API request fields are any subset of the changeable fields. `src: Deployment contract, API shapes table`
- [ ] `C-DC-117` `data` The `PATCH /api/studio/settings` API response shape is the settings. `src: Deployment contract, API shapes table`
- [ ] `C-DC-118` `data` The `GET /api/studio/integrations/tipbox` API response shape is `{"page_url", "secret_last_four", "secret_created_at", "secret_last_used_at"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-119` `data` The `PUT /api/studio/integrations/tipbox/secret` API request fields are `{"secret"}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-120` `data` The `PUT /api/studio/integrations/tipbox/secret` API response shape is the integration, without the secret. `src: Deployment contract, API shapes table`
- [ ] `C-DC-121` `data` The `POST /api/studio/asset-version` API response shape is `{"asset_version"}`. `src: Deployment contract, API shapes table`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `Vol. I` | value pinned in the brief | C-OV-11 | Overview para 4 |
| `c1b1p1-back` | value pinned in the brief | C-OV-12 | Overview para 3 |
| `POST /api/auth/register` | value pinned in the brief | C-RL-25 | User roles para 3 |
| `deku-demo-pw-2026` | value pinned in the brief | C-RL-27 | User roles seeded accounts |
| `author@example.com` | value pinned in the brief | C-RL-28 | User roles seeded accounts |
| `author2@example.com` | value pinned in the brief | C-RL-28 | User roles seeded accounts |
| `reader@example.com` | value pinned in the brief | C-RL-29 | User roles seeded accounts |
| `reader2@example.com` | value pinned in the brief | C-RL-29 | User roles seeded accounts |
| `tbx_seed_001` | value pinned in the brief | C-RL-30 | User roles seeded accounts |
| `POST /api/studio/auth/login` | value pinned in the brief | C-RL-32 | User roles para 3 |
| `POST /api/auth/login` | value pinned in the brief | C-RL-32 | User roles para 3 |
| `access_token` | value pinned in the brief | C-CF-01 | Core features, Authentication and account lifecycle rule 1 |
| `notifications` | value pinned in the brief | C-CF-02 | Core features, Authentication and account lifecycle rule 1 |
| `drops` | value pinned in the brief | C-CF-02 | Core features, Authentication and account lifecycle rule 1 |
| `password` | value pinned in the brief | C-CF-07 | Core features, Authentication and account lifecycle rule 3 |
| `email` | value pinned in the brief | C-CF-08 | Core features, Authentication and account lifecycle rule 3 |
| `That address cannot be used.` | value pinned in the brief | C-CF-10 | Core features, Authentication and account lifecycle rule 4 |
| `10` | value pinned in the brief | C-CF-16 | Core features, Authentication and account lifecycle rule 6 |
| `15` | value pinned in the brief | C-CF-16 | Core features, Authentication and account lifecycle rule 6 |
| `POST /api/auth/logout` | value pinned in the brief | C-CF-20 | Core features, Authentication and account lifecycle rule 7 |
| `expires_at` | value pinned in the brief | C-CF-24 | Core features, Authentication and account lifecycle rule 7 |
| `create account` | value pinned in the brief | C-CF-35 | Core features, Authentication and account lifecycle rule 11 |
| `sign in` | value pinned in the brief | C-CF-37 | Core features, Authentication and account lifecycle rule 11 |
| `/studio/sign-in` | value pinned in the brief | C-CF-40 | Core features, Authentication and account lifecycle rule 11 |
| `/` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/chapters` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/chapter/:id` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/about` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/legal` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/support/return` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/account` | value pinned in the brief | C-CF-41 | Core features, The reading surface rule 1 |
| `/fr` | value pinned in the brief | C-CF-42 | Core features, The reading surface rule 1 |
| `/volumes/:volume/chapter/:id` | value pinned in the brief | C-CF-44 | Core features, The reading surface rule 1 |
| `:volume` | value pinned in the brief | C-CF-44 | Core features, The reading surface rule 1 |
| `<html lang>` | value pinned in the brief | C-CF-51 | Core features, The reading surface rule 3 |
| `en` | value pinned in the brief | C-CF-51 | Core features, The reading surface rule 3 |
| `fr` | value pinned in the brief | C-CF-51 | Core features, The reading surface rule 3 |
| `Chapter #<n>: <Title With Each Word Capitalised> - Doudou Fever - Interactive Comic` | value pinned in the brief | C-CF-69 | Core features, The reading surface rule 3 |
| `Read chapter <n>, <title>, of the Doudou Fever interactive comic.` | value pinned in the brief | C-CF-70 | Core features, The reading surface rule 3 |
| `Chapitre #<n> : <Titre Avec Chaque Mot En Capitale> - Doudou Fever - BD interactive` | value pinned in the brief | C-CF-87 | Core features, The reading surface rule 3 |
| `Lis le chapitre <n>, <titre>, de la BD interactive Doudou Fever.` | value pinned in the brief | C-CF-88 | Core features, The reading surface rule 3 |
| `read now` | value pinned in the brief | C-CF-89 | Core features, The reading surface rule 4 |
| `Doudou Fever` | value pinned in the brief | C-CF-91 | Core features, The reading surface rule 4 |
| `By Damien Lorca & Camille Rouyer` | value pinned in the brief | C-CF-92 | Core features, The reading surface rule 4 |
| `select a chapter` | value pinned in the brief | C-CF-95 | Core features, The reading surface rule 5 |
| `01.welcome to Varny` | value pinned in the brief | C-CF-98 | Core features, The reading surface rule 5 |
| `Doudou FeverVol. I` | value pinned in the brief | C-CF-99 | Core features, The reading surface rule 5 |
| `01:06` | value pinned in the brief | C-CF-100 | Core features, The reading surface rule 5 |
| `chapter 1 of 6` | value pinned in the brief | C-CF-102 | Core features, The reading surface rule 6 |
| `<title>, locked` | value pinned in the brief | C-CF-106 | Core features, The reading surface rule 6 |
| `Next track is loading...` | value pinned in the brief | C-CF-116 | Core features, The reading surface rule 8 |
| `01. welcome to Varny` | value pinned in the brief | C-CF-117 | Core features, The reading surface rule 8 |
| `role="img"` | value pinned in the brief | C-CF-119 | Core features, The reading surface rule 9 |
| `01:01` | value pinned in the brief | C-CF-128 | Core features, The reading surface rule 10 |
| `panel 1` | value pinned in the brief | C-CF-129 | Core features, The reading surface rule 10 |
| `chapter progress` | value pinned in the brief | C-CF-130 | Core features, The reading surface rule 10 |
| `0` | value pinned in the brief | C-CF-130 | Core features, The reading surface rule 10 |
| `100` | value pinned in the brief | C-CF-130 | Core features, The reading surface rule 10 |
| `previous panel` | value pinned in the brief | C-CF-133 | Core features, The reading surface rule 11 |
| `next panel` | value pinned in the brief | C-CF-133 | Core features, The reading surface rule 11 |
| `next track` | value pinned in the brief | C-CF-136 | Core features, The reading surface rule 12 |
| ` _ ` | value pinned in the brief | C-CF-137 | Core features, The reading surface rule 12 |
| `read as text` | value pinned in the brief | C-CF-142 | Core features, The reading surface rule 13 |
| `dd-last-chapter` | value pinned in the brief | C-CF-145 | Core features, The reading surface rule 14 |
| `1/2` | value pinned in the brief | C-CF-145 | Core features, The reading surface rule 14 |
| `dd-progress-<volume>-<chapter>` | value pinned in the brief | C-CF-146 | Core features, The reading surface rule 14 |
| `1` | value pinned in the brief | C-CF-146 | Core features, The reading surface rule 14 |
| `0.400` | value pinned in the brief | C-CF-146 | Core features, The reading surface rule 14 |
| `200` | value pinned in the brief | C-CF-149 | Core features, The reading surface rule 15 |
| `04. scratch that !` | value pinned in the brief | C-CF-150 | Core features, The reading surface rule 15 |
| `notify me` | value pinned in the brief | C-CF-152 | Core features, The reading surface rule 15 |
| `support us` | value pinned in the brief | C-CF-153 | Core features, The reading surface rule 15 |
| `POST /api/me/notify` | value pinned in the brief | C-CF-159 | Core features, The reading surface rule 16 |
| `all` | value pinned in the brief | C-CF-160 | Core features, The reading surface rule 16 |
| `404` | value pinned in the brief | C-CF-162 | Core features, The reading surface rule 17 |
| `/fr/chapters` | value pinned in the brief | C-CF-165 | Core features, The reading surface rule 17 |
| `Oopsy, page not found` | value pinned in the brief | C-CF-169 | Core features, The reading surface rule 18 |
| `Go back to home` | value pinned in the brief | C-CF-170 | Core features, The reading surface rule 18 |
| `Something went missing. Try again?` | value pinned in the brief | C-CF-174 | Core features, The reading surface rule 19 |
| `try again` | value pinned in the brief | C-CF-175 | Core features, The reading surface rule 19 |
| `back to chapters` | value pinned in the brief | C-CF-176 | Core features, The reading surface rule 19 |
| `https://tipbox.example/doudou-fever` | value pinned in the brief | C-CF-186 | Core features, The reading surface rule 21 |
| `return_token` | value pinned in the brief | C-CF-187 | Core features, The reading surface rule 21 |
| `target="_blank"` | value pinned in the brief | C-CF-188 | Core features, The reading surface rule 21 |
| `rel` | value pinned in the brief | C-CF-189 | Core features, The reading surface rule 21 |
| `noopener` | value pinned in the brief | C-CF-189 | Core features, The reading surface rule 21 |
| `noreferrer` | value pinned in the brief | C-CF-189 | Core features, The reading surface rule 21 |
| `download my data` | value pinned in the brief | C-CF-192 | Core features, The reading surface rule 22 |
| `delete my account` | value pinned in the brief | C-CF-193 | Core features, The reading surface rule 22 |
| `early_access_days` | value pinned in the brief | C-CF-196 | Core features, Who may read a chapter rule 1 |
| `GET /api/volumes/{order}/chapters/{number}` | value pinned in the brief | C-CF-202 | Core features, Who may read a chapter rule 3 |
| `/api/textures/v<asset_version>/<volume order>/<chapter number>/<file identifier>.png?tag=<content tag>` | value pinned in the brief | C-CF-208 | Core features, Who may read a chapter rule 4 |
| `expires` | value pinned in the brief | C-CF-212 | Core features, Who may read a chapter rule 4 |
| `sig` | value pinned in the brief | C-CF-212 | Core features, Who may read a chapter rule 4 |
| `GET /api/volumes` | value pinned in the brief | C-CF-218 | Core features, Who may read a chapter rule 6 |
| `locked` | value pinned in the brief | C-CF-219 | Core features, Who may read a chapter rule 6 |
| `/api/covers/<volume order>/<chapter number>.png` | value pinned in the brief | C-CF-222 | Core features, Who may read a chapter rule 7 |
| `/sitemap.xml` | value pinned in the brief | C-CF-225 | Core features, Who may read a chapter rule 8 |
| `/fr/sitemap.xml` | value pinned in the brief | C-CF-226 | Core features, Who may read a chapter rule 8 |
| `POST /api/tips/return-tokens` | value pinned in the brief | C-CF-230 | Core features, Tips and early access rule 1 |
| `24` | value pinned in the brief | C-CF-230 | Core features, Tips and early access rule 1 |
| `POST /api/tips/return` | value pinned in the brief | C-CF-233 | Core features, Tips and early access rule 2 |
| `sign_in_required` | value pinned in the brief | C-CF-233 | Core features, Tips and early access rule 2 |
| `granted` | value pinned in the brief | C-CF-234 | Core features, Tips and early access rule 2 |
| `below_threshold` | value pinned in the brief | C-CF-235 | Core features, Tips and early access rule 2 |
| `pending` | value pinned in the brief | C-CF-236 | Core features, Tips and early access rule 2 |
| `/support/return?token=<token>` | value pinned in the brief | C-CF-237 | Core features, Tips and early access rule 1 |
| `POST /api/webhooks/tipbox` | value pinned in the brief | C-CF-244 | Core features, Tips and early access rule 3 |
| `tbx_whsec_5f3a9c2e81d7` | value pinned in the brief | C-CF-245 | Core features, Tips and early access rule 3 |
| `Tipbox-Signature` | value pinned in the brief | C-CF-246 | Core features, Tips and early access rule 3 |
| `t=<unix seconds>,v1=<signature>` | value pinned in the brief | C-CF-246 | Core features, Tips and early access rule 3 |
| `401` | value pinned in the brief | C-CF-248 | Core features, Tips and early access rule 4 |
| `300` | value pinned in the brief | C-CF-250 | Core features, Tips and early access rule 4 |
| `30` | value pinned in the brief | C-CF-255 | Core features, Tips and early access rule 5 |
| `type` | value pinned in the brief | C-CF-257 | Core features, Tips and early access rule 6 |
| `tip.received` | value pinned in the brief | C-CF-257 | Core features, Tips and early access rule 6 |
| `tip.refunded` | value pinned in the brief | C-CF-257 | Core features, Tips and early access rule 6 |
| `tip.disputed` | value pinned in the brief | C-CF-257 | Core features, Tips and early access rule 6 |
| `eur` | value pinned in the brief | C-CF-260 | Core features, Tips and early access rule 6 |
| `usd` | value pinned in the brief | C-CF-260 | Core features, Tips and early access rule 6 |
| `1.087500` | value pinned in the brief | C-CF-261 | Core features, Tips and early access rule 6 |
| `token` | value pinned in the brief | C-CF-267 | Core features, Tips and early access rule 8 |
| `supporter_email` | value pinned in the brief | C-CF-269 | Core features, Tips and early access rule 8 |
| `address` | value pinned in the brief | C-CF-269 | Core features, Tips and early access rule 8 |
| `early_access` | value pinned in the brief | C-CF-271 | Core features, Tips and early access rule 9 |
| `early_access_threshold` | value pinned in the brief | C-CF-271 | Core features, Tips and early access rule 9 |
| `500` | value pinned in the brief | C-CF-271 | Core features, Tips and early access rule 9 |
| `none` | value pinned in the brief | C-CF-272 | Core features, Tips and early access rule 8 |
| `credit_threshold` | value pinned in the brief | C-CF-274 | Core features, Tips and early access rule 9 |
| `2000` | value pinned in the brief | C-CF-274 | Core features, Tips and early access rule 9 |
| `credits` | value pinned in the brief | C-CF-274 | Core features, Tips and early access rule 9 |
| `12` | value pinned in the brief | C-CF-276 | Core features, Tips and early access rule 9 |
| `refunded` | value pinned in the brief | C-CF-277 | Core features, Tips and early access rule 10 |
| `disputed` | value pinned in the brief | C-CF-281 | Core features, Tips and early access rule 10 |
| `800` | value pinned in the brief | C-CF-290 | Core features, Tips and early access rule 12 |
| `GET /api/me/progress` | value pinned in the brief | C-CF-291 | Core features, Reading progress synchronisation across devices rule 1 |
| `PUT /api/me/progress` | value pinned in the brief | C-CF-292 | Core features, Reading progress synchronisation across devices rule 1 |
| `GET /api/me/export` | value pinned in the brief | C-CF-311 | Core features, Reader data rights rule 1 |
| `DELETE /api/me` | value pinned in the brief | C-CF-313 | Core features, Reader data rights rule 2 |
| `PATCH /api/me` | value pinned in the brief | C-CF-318 | Core features, Reader data rights rule 3 |
| `locale` | value pinned in the brief | C-CF-318 | Core features, Reader data rights rule 3 |
| `/fr/chapitres` | value pinned in the brief | C-CF-322 | Core features, Languages and localisation rule 1 |
| `EN` | value pinned in the brief | C-CF-323 | Core features, Languages and localisation rule 2 |
| `FR` | value pinned in the brief | C-CF-323 | Core features, Languages and localisation rule 2 |
| `dd-language` | value pinned in the brief | C-CF-330 | Core features, Languages and localisation rule 2 |
| `GET /api/catalogue/<locale>` | value pinned in the brief | C-CF-332 | Core features, Languages and localisation rule 4 |
| `untranslated` | value pinned in the brief | C-CF-333 | Core features, Languages and localisation rule 4 |
| `chrome.chapters` | value pinned in the brief | C-CF-335 | Core features, Languages and localisation rule 5 |
| `chapters` | value pinned in the brief | C-CF-335 | Core features, Languages and localisation rule 5 |
| `chrome.about` | value pinned in the brief | C-CF-336 | Core features, Languages and localisation rule 5 |
| `about` | value pinned in the brief | C-CF-336 | Core features, Languages and localisation rule 5 |
| `chrome.legal` | value pinned in the brief | C-CF-337 | Core features, Languages and localisation rule 5 |
| `legal notice & terms of use` | value pinned in the brief | C-CF-337 | Core features, Languages and localisation rule 5 |
| `chrome.fullscreen_enter` | value pinned in the brief | C-CF-339 | Core features, Languages and localisation rule 5 |
| `enter fullscreen` | value pinned in the brief | C-CF-339 | Core features, Languages and localisation rule 5 |
| `chrome.fullscreen_exit` | value pinned in the brief | C-CF-340 | Core features, Languages and localisation rule 5 |
| `exit fullscreen` | value pinned in the brief | C-CF-340 | Core features, Languages and localisation rule 5 |
| `index.button` | value pinned in the brief | C-CF-341 | Core features, Languages and localisation rule 5 |
| `index.credit` | value pinned in the brief | C-CF-342 | Core features, Languages and localisation rule 5 |
| `chapters.heading` | value pinned in the brief | C-CF-343 | Core features, Languages and localisation rule 5 |
| `chapters.tip` | value pinned in the brief | C-CF-344 | Core features, Languages and localisation rule 5 |
| `chapters.next_track` | value pinned in the brief | C-CF-345 | Core features, Languages and localisation rule 5 |
| `reader.loading` | value pinned in the brief | C-CF-346 | Core features, Languages and localisation rule 5 |
| `reader.text_mode` | value pinned in the brief | C-CF-347 | Core features, Languages and localisation rule 5 |
| `reader.previous_panel` | value pinned in the brief | C-CF-348 | Core features, Languages and localisation rule 5 |
| `reader.next_panel` | value pinned in the brief | C-CF-349 | Core features, Languages and localisation rule 5 |
| `reader.progress` | value pinned in the brief | C-CF-350 | Core features, Languages and localisation rule 5 |
| `reader.load_failed` | value pinned in the brief | C-CF-351 | Core features, Languages and localisation rule 5 |
| `reader.retry` | value pinned in the brief | C-CF-352 | Core features, Languages and localisation rule 5 |
| `reader.back` | value pinned in the brief | C-CF-353 | Core features, Languages and localisation rule 5 |
| `locked.notify` | value pinned in the brief | C-CF-356 | Core features, Languages and localisation rule 5 |
| `consent.accept` | value pinned in the brief | C-CF-359 | Core features, Languages and localisation rule 5 |
| `Accept` | value pinned in the brief | C-CF-359 | Core features, Languages and localisation rule 5 |
| `consent.decline` | value pinned in the brief | C-CF-360 | Core features, Languages and localisation rule 5 |
| `Decline` | value pinned in the brief | C-CF-360 | Core features, Languages and localisation rule 5 |
| `support.granted` | value pinned in the brief | C-CF-361 | Core features, Languages and localisation rule 5 |
| `Thank you. Your early access is active.` | value pinned in the brief | C-CF-361 | Core features, Languages and localisation rule 5 |
| `support.pending` | value pinned in the brief | C-CF-364 | Core features, Languages and localisation rule 5 |
| `Thank you. Your tip is on its way to us.` | value pinned in the brief | C-CF-364 | Core features, Languages and localisation rule 5 |
| `support.entitlement` | value pinned in the brief | C-CF-367 | Core features, Languages and localisation rule 5 |
| `Tips of {amount} or more read new chapters up to {days} days early.` | value pinned in the brief | C-CF-367 | Core features, Languages and localisation rule 5 |
| `about.nav_intro` | value pinned in the brief | C-CF-368 | Core features, Languages and localisation rule 5 |
| `intro` | value pinned in the brief | C-CF-368 | Core features, Languages and localisation rule 5 |
| `about.nav_legend` | value pinned in the brief | C-CF-369 | Core features, Languages and localisation rule 5 |
| `the legend` | value pinned in the brief | C-CF-369 | Core features, Languages and localisation rule 5 |
| `about.nav_team` | value pinned in the brief | C-CF-370 | Core features, Languages and localisation rule 5 |
| `the team` | value pinned in the brief | C-CF-370 | Core features, Languages and localisation rule 5 |
| `about.nav_support` | value pinned in the brief | C-CF-371 | Core features, Languages and localisation rule 5 |
| `about.scroll` | value pinned in the brief | C-CF-372 | Core features, Languages and localisation rule 5 |
| `Scroll down` | value pinned in the brief | C-CF-372 | Core features, Languages and localisation rule 5 |
| `about.intro_title` | value pinned in the brief | C-CF-373 | Core features, Languages and localisation rule 5 |
| `the interactive adventure of a megalomaniac sheep who wants to make the world dance.` | value pinned in the brief | C-CF-373 | Core features, Languages and localisation rule 5 |
| `about.legend_title_1` | value pinned in the brief | C-CF-374 | Core features, Languages and localisation rule 5 |
| `yes the legend,` | value pinned in the brief | C-CF-374 | Core features, Languages and localisation rule 5 |
| `about.legend_title_2` | value pinned in the brief | C-CF-375 | Core features, Languages and localisation rule 5 |
| `is {hero}!` | value pinned in the brief | C-CF-375 | Core features, Languages and localisation rule 5 |
| `about.team_title_1` | value pinned in the brief | C-CF-376 | Core features, Languages and localisation rule 5 |
| `behind` | value pinned in the brief | C-CF-376 | Core features, Languages and localisation rule 5 |
| `about.team_title_2` | value pinned in the brief | C-CF-377 | Core features, Languages and localisation rule 5 |
| `about.support_title_1` | value pinned in the brief | C-CF-378 | Core features, Languages and localisation rule 5 |
| `i love you too` | value pinned in the brief | C-CF-378 | Core features, Languages and localisation rule 5 |
| `about.support_title_2` | value pinned in the brief | C-CF-379 | Core features, Languages and localisation rule 5 |
| `my friend!` | value pinned in the brief | C-CF-379 | Core features, Languages and localisation rule 5 |
| `about.chip_contact` | value pinned in the brief | C-CF-380 | Core features, Languages and localisation rule 5 |
| `email us` | value pinned in the brief | C-CF-380 | Core features, Languages and localisation rule 5 |
| `legal.title` | value pinned in the brief | C-CF-381 | Core features, Languages and localisation rule 5 |
| `Legal Notice & Terms of Use` | value pinned in the brief | C-CF-381 | Core features, Languages and localisation rule 5 |
| `legal.publisher` | value pinned in the brief | C-CF-382 | Core features, Languages and localisation rule 5 |
| `Website Publisher` | value pinned in the brief | C-CF-382 | Core features, Languages and localisation rule 5 |
| `legal.hosting` | value pinned in the brief | C-CF-383 | Core features, Languages and localisation rule 5 |
| `Hosting` | value pinned in the brief | C-CF-383 | Core features, Languages and localisation rule 5 |
| `legal.domains` | value pinned in the brief | C-CF-384 | Core features, Languages and localisation rule 5 |
| `Domains` | value pinned in the brief | C-CF-384 | Core features, Languages and localisation rule 5 |
| `legal.property` | value pinned in the brief | C-CF-385 | Core features, Languages and localisation rule 5 |
| `Intellectual Property` | value pinned in the brief | C-CF-385 | Core features, Languages and localisation rule 5 |
| `legal.terms` | value pinned in the brief | C-CF-386 | Core features, Languages and localisation rule 5 |
| `Terms of Use` | value pinned in the brief | C-CF-386 | Core features, Languages and localisation rule 5 |
| `legal.data` | value pinned in the brief | C-CF-387 | Core features, Languages and localisation rule 5 |
| `Personal Data & Privacy` | value pinned in the brief | C-CF-387 | Core features, Languages and localisation rule 5 |
| `legal.cookies` | value pinned in the brief | C-CF-388 | Core features, Languages and localisation rule 5 |
| `Cookies & Trackers` | value pinned in the brief | C-CF-388 | Core features, Languages and localisation rule 5 |
| `legal.law` | value pinned in the brief | C-CF-389 | Core features, Languages and localisation rule 5 |
| `Applicable Law & Jurisdiction` | value pinned in the brief | C-CF-389 | Core features, Languages and localisation rule 5 |
| `not-found.text` | value pinned in the brief | C-CF-390 | Core features, Languages and localisation rule 5 |
| `not-found.cta` | value pinned in the brief | C-CF-391 | Core features, Languages and localisation rule 5 |
| `account.heading` | value pinned in the brief | C-CF-392 | Core features, Languages and localisation rule 5 |
| `Your account` | value pinned in the brief | C-CF-392 | Core features, Languages and localisation rule 5 |
| `account.export` | value pinned in the brief | C-CF-393 | Core features, Languages and localisation rule 5 |
| `account.delete` | value pinned in the brief | C-CF-394 | Core features, Languages and localisation rule 5 |
| `account.sign_in` | value pinned in the brief | C-CF-395 | Core features, Languages and localisation rule 5 |
| `account.create` | value pinned in the brief | C-CF-396 | Core features, Languages and localisation rule 5 |
| `create an account` | value pinned in the brief | C-CF-396 | Core features, Languages and localisation rule 5 |
| `account.email` | value pinned in the brief | C-CF-397 | Core features, Languages and localisation rule 5 |
| `account.password` | value pinned in the brief | C-CF-398 | Core features, Languages and localisation rule 5 |
| `chrome.surprise` | value pinned in the brief | C-CF-399 | Core features, Languages and localisation rule 5 |
| `surprise` | value pinned in the brief | C-CF-399 | Core features, Languages and localisation rule 5 |
| `chapters.locked_name` | value pinned in the brief | C-CF-400 | Core features, Languages and localisation rule 5 |
| `{title}, locked, opens {date}` | value pinned in the brief | C-CF-400 | Core features, Languages and localisation rule 5 |
| `chapters.locked_plain` | value pinned in the brief | C-CF-401 | Core features, Languages and localisation rule 5 |
| `{title}, locked` | value pinned in the brief | C-CF-401 | Core features, Languages and localisation rule 5 |
| `chapters.timecode_label` | value pinned in the brief | C-CF-402 | Core features, Languages and localisation rule 5 |
| `chapter {number} of {count}` | value pinned in the brief | C-CF-402 | Core features, Languages and localisation rule 5 |
| `reader.timecode_label` | value pinned in the brief | C-CF-403 | Core features, Languages and localisation rule 5 |
| `panel {number}` | value pinned in the brief | C-CF-403 | Core features, Languages and localisation rule 5 |
| `reader.announce_loading` | value pinned in the brief | C-CF-404 | Core features, Languages and localisation rule 5 |
| `Chapter {number} is loading.` | value pinned in the brief | C-CF-404 | Core features, Languages and localisation rule 5 |
| `reader.announce_ready` | value pinned in the brief | C-CF-405 | Core features, Languages and localisation rule 5 |
| `Chapter {number} is ready.` | value pinned in the brief | C-CF-405 | Core features, Languages and localisation rule 5 |
| `reader.announce_failed` | value pinned in the brief | C-CF-406 | Core features, Languages and localisation rule 5 |
| `Chapter {number} could not be loaded.` | value pinned in the brief | C-CF-406 | Core features, Languages and localisation rule 5 |
| `reader.end_of_volume` | value pinned in the brief | C-CF-407 | Core features, Languages and localisation rule 5 |
| `last track of the volume, back to chapters` | value pinned in the brief | C-CF-407 | Core features, Languages and localisation rule 5 |
| `chrome.announce_locale` | value pinned in the brief | C-CF-408 | Core features, Languages and localisation rule 5 |
| `The page is now in English.` | value pinned in the brief | C-CF-408 | Core features, Languages and localisation rule 5 |
| `about.team_dam_title` | value pinned in the brief | C-CF-410 | Core features, Languages and localisation rule 5 |
| `Dam` | value pinned in the brief | C-CF-410 | Core features, Languages and localisation rule 5 |
| `about.team_ca_title` | value pinned in the brief | C-CF-412 | Core features, Languages and localisation rule 5 |
| `Ca` | value pinned in the brief | C-CF-412 | Core features, Languages and localisation rule 5 |
| `about.chip_photogram` | value pinned in the brief | C-CF-416 | Core features, Languages and localisation rule 5 |
| `photogram` | value pinned in the brief | C-CF-416 | Core features, Languages and localisation rule 5 |
| `about.chip_clipclop` | value pinned in the brief | C-CF-417 | Core features, Languages and localisation rule 5 |
| `clipclop` | value pinned in the brief | C-CF-417 | Core features, Languages and localisation rule 5 |
| `legal.contact_label` | value pinned in the brief | C-CF-419 | Core features, Languages and localisation rule 5 |
| `Contact email` | value pinned in the brief | C-CF-419 | Core features, Languages and localisation rule 5 |
| `legal.hosting_body` | value pinned in the brief | C-CF-420 | Core features, Languages and localisation rule 5 |
| `Hosted by Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.` | value pinned in the brief | C-CF-420 | Core features, Languages and localisation rule 5 |
| `legal.law_body` | value pinned in the brief | C-CF-426 | Core features, Languages and localisation rule 5 |
| `These terms are governed by French law. Any dispute falls under the courts of Paris.` | value pinned in the brief | C-CF-426 | Core features, Languages and localisation rule 5 |
| `chapitres` | value pinned in the brief | C-CF-427 | Core features, Languages and localisation rule 5 |
| `a propos` | value pinned in the brief | C-CF-428 | Core features, Languages and localisation rule 5 |
| `mentions legales & conditions d'utilisation` | value pinned in the brief | C-CF-429 | Core features, Languages and localisation rule 5 |
| `chrome.byline` | value pinned in the brief | C-CF-430 | Core features, Languages and localisation rule 5 |
| `par Camille Rouyer et Damien Lorca` | value pinned in the brief | C-CF-430 | Core features, Languages and localisation rule 5 |
| `plein ecran` | value pinned in the brief | C-CF-431 | Core features, Languages and localisation rule 5 |
| `quitter le plein ecran` | value pinned in the brief | C-CF-432 | Core features, Languages and localisation rule 5 |
| `lire maintenant` | value pinned in the brief | C-CF-433 | Core features, Languages and localisation rule 5 |
| `Par Damien Lorca & Camille Rouyer` | value pinned in the brief | C-CF-434 | Core features, Languages and localisation rule 5 |
| `choisis un chapitre` | value pinned in the brief | C-CF-435 | Core features, Languages and localisation rule 5 |
| `soutiens-nous` | value pinned in the brief | C-CF-436 | Core features, Languages and localisation rule 5 |
| `piste suivante` | value pinned in the brief | C-CF-437 | Core features, Languages and localisation rule 5 |
| `La piste suivante arrive...` | value pinned in the brief | C-CF-438 | Core features, Languages and localisation rule 5 |
| `lire en texte` | value pinned in the brief | C-CF-439 | Core features, Languages and localisation rule 5 |
| `case precedente` | value pinned in the brief | C-CF-440 | Core features, Languages and localisation rule 5 |
| `case suivante` | value pinned in the brief | C-CF-441 | Core features, Languages and localisation rule 5 |
| `progression du chapitre` | value pinned in the brief | C-CF-442 | Core features, Languages and localisation rule 5 |
| `Il manque quelque chose. On reessaie ?` | value pinned in the brief | C-CF-443 | Core features, Languages and localisation rule 5 |
| `reessayer` | value pinned in the brief | C-CF-444 | Core features, Languages and localisation rule 5 |
| `retour aux chapitres` | value pinned in the brief | C-CF-445 | Core features, Languages and localisation rule 5 |
| `locked.timing` | value pinned in the brief | C-CF-446 | Core features, Languages and localisation rule 5 |
| `Ce chapitre sort le {date}.` | value pinned in the brief | C-CF-446 | Core features, Languages and localisation rule 5 |
| `locked.drawing` | value pinned in the brief | C-CF-447 | Core features, Languages and localisation rule 5 |
| `Ce chapitre est encore en dessin.` | value pinned in the brief | C-CF-447 | Core features, Languages and localisation rule 5 |
| `previens-moi` | value pinned in the brief | C-CF-448 | Core features, Languages and localisation rule 5 |
| `locked.support` | value pinned in the brief | C-CF-449 | Core features, Languages and localisation rule 5 |
| `Les soutiens le lisent des qu'il est fini.` | value pinned in the brief | C-CF-449 | Core features, Languages and localisation rule 5 |
| `Accepter` | value pinned in the brief | C-CF-451 | Core features, Languages and localisation rule 5 |
| `Refuser` | value pinned in the brief | C-CF-452 | Core features, Languages and localisation rule 5 |
| `Merci. Ton acces anticipe est actif.` | value pinned in the brief | C-CF-453 | Core features, Languages and localisation rule 5 |
| `support.sign_in` | value pinned in the brief | C-CF-454 | Core features, Languages and localisation rule 5 |
| `Merci. Connecte-toi et nous l'ajouterons a ton compte.` | value pinned in the brief | C-CF-454 | Core features, Languages and localisation rule 5 |
| `support.below_threshold` | value pinned in the brief | C-CF-455 | Core features, Languages and localisation rule 5 |
| `Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.` | value pinned in the brief | C-CF-455 | Core features, Languages and localisation rule 5 |
| `Merci. Ton pourboire est en route.` | value pinned in the brief | C-CF-456 | Core features, Languages and localisation rule 5 |
| `support.expired` | value pinned in the brief | C-CF-457 | Core features, Languages and localisation rule 5 |
| `Ce lien de remerciement a expire.` | value pinned in the brief | C-CF-457 | Core features, Languages and localisation rule 5 |
| `Les pourboires de {amount} ou plus lisent les nouveaux chapitres jusqu'a {days} jours plus tot.` | value pinned in the brief | C-CF-459 | Core features, Languages and localisation rule 5 |
| `la legende` | value pinned in the brief | C-CF-461 | Core features, Languages and localisation rule 5 |
| `l'equipe` | value pinned in the brief | C-CF-462 | Core features, Languages and localisation rule 5 |
| `Descends` | value pinned in the brief | C-CF-464 | Core features, Languages and localisation rule 5 |
| `l'aventure interactive d'un mouton megalomane qui veut faire danser le monde.` | value pinned in the brief | C-CF-465 | Core features, Languages and localisation rule 5 |
| `oui la legende,` | value pinned in the brief | C-CF-466 | Core features, Languages and localisation rule 5 |
| `c'est {hero} !` | value pinned in the brief | C-CF-467 | Core features, Languages and localisation rule 5 |
| `derriere` | value pinned in the brief | C-CF-468 | Core features, Languages and localisation rule 5 |
| `moi aussi je t'aime` | value pinned in the brief | C-CF-470 | Core features, Languages and localisation rule 5 |
| `mon ami !` | value pinned in the brief | C-CF-471 | Core features, Languages and localisation rule 5 |
| `ecris-nous` | value pinned in the brief | C-CF-472 | Core features, Languages and localisation rule 5 |
| `Mentions legales & conditions d'utilisation` | value pinned in the brief | C-CF-473 | Core features, Languages and localisation rule 5 |
| `Editeur du site` | value pinned in the brief | C-CF-474 | Core features, Languages and localisation rule 5 |
| `Hebergement` | value pinned in the brief | C-CF-475 | Core features, Languages and localisation rule 5 |
| `Domaines` | value pinned in the brief | C-CF-476 | Core features, Languages and localisation rule 5 |
| `Propriete intellectuelle` | value pinned in the brief | C-CF-477 | Core features, Languages and localisation rule 5 |
| `Conditions d'utilisation` | value pinned in the brief | C-CF-478 | Core features, Languages and localisation rule 5 |
| `Donnees personnelles & vie privee` | value pinned in the brief | C-CF-479 | Core features, Languages and localisation rule 5 |
| `Cookies & traceurs` | value pinned in the brief | C-CF-480 | Core features, Languages and localisation rule 5 |
| `Droit applicable & juridiction` | value pinned in the brief | C-CF-481 | Core features, Languages and localisation rule 5 |
| `Oups, page introuvable` | value pinned in the brief | C-CF-482 | Core features, Languages and localisation rule 5 |
| `Retour a l'accueil` | value pinned in the brief | C-CF-483 | Core features, Languages and localisation rule 5 |
| `Ton compte` | value pinned in the brief | C-CF-484 | Core features, Languages and localisation rule 5 |
| `telecharger mes donnees` | value pinned in the brief | C-CF-485 | Core features, Languages and localisation rule 5 |
| `supprimer mon compte` | value pinned in the brief | C-CF-486 | Core features, Languages and localisation rule 5 |
| `se connecter` | value pinned in the brief | C-CF-487 | Core features, Languages and localisation rule 5 |
| `creer un compte` | value pinned in the brief | C-CF-488 | Core features, Languages and localisation rule 5 |
| `e-mail` | value pinned in the brief | C-CF-489 | Core features, Languages and localisation rule 5 |
| `mot de passe` | value pinned in the brief | C-CF-490 | Core features, Languages and localisation rule 5 |
| `{title}, verrouille, sort le {date}` | value pinned in the brief | C-CF-492 | Core features, Languages and localisation rule 5 |
| `{title}, verrouille` | value pinned in the brief | C-CF-493 | Core features, Languages and localisation rule 5 |
| `chapitre {number} sur {count}` | value pinned in the brief | C-CF-494 | Core features, Languages and localisation rule 5 |
| `case {number}` | value pinned in the brief | C-CF-495 | Core features, Languages and localisation rule 5 |
| `Le chapitre {number} arrive.` | value pinned in the brief | C-CF-496 | Core features, Languages and localisation rule 5 |
| `Le chapitre {number} est pret.` | value pinned in the brief | C-CF-497 | Core features, Languages and localisation rule 5 |
| `Le chapitre {number} n'a pas pu etre charge.` | value pinned in the brief | C-CF-498 | Core features, Languages and localisation rule 5 |
| `derniere piste du volume, retour aux chapitres` | value pinned in the brief | C-CF-499 | Core features, Languages and localisation rule 5 |
| `La page est maintenant en francais.` | value pinned in the brief | C-CF-500 | Core features, Languages and localisation rule 5 |
| `about.legend_body` | value pinned in the brief | C-CF-501 | Core features, Languages and localisation rule 5 |
| `Doudou est un mouton megalomane, tendre et bien decide a devenir DJ. Avec Jean-Loic, un barman dechaine, et Milan, future star de la cuisine sur les reseaux, il melange chaos et grands reves dans un appart plein de rires et de bruit tard le soir. C'est cool, c'est drole, c'est Doudou Fever.` | value pinned in the brief | C-CF-501 | Core features, Languages and localisation rule 5 |
| `about.team_dam_body` | value pinned in the brief | C-CF-503 | Core features, Languages and localisation rule 5 |
| `Developpeur creatif et animateur, moitie codeur moitie sorcier. Il anime les images, fait bouger les pixels et transforme des lignes de code en experiences cool et magiques.` | value pinned in the brief | C-CF-503 | Core features, Languages and localisation rule 5 |
| `about.team_ca_body` | value pinned in the brief | C-CF-505 | Core features, Languages and localisation rule 5 |
| `Directrice artistique, illustratrice et maitresse du pinceau numerique. Elle dessine plus vite que son ombre et donne vie a chaque personnage avec style, emotion...` | value pinned in the brief | C-CF-505 | Core features, Languages and localisation rule 5 |
| `about.support_body` | value pinned in the brief | C-CF-506 | Core features, Languages and localisation rule 5 |
| `Soutiens Doudou sur le chemin de la gloire et aide-le a devenir une legende. Un jour, peut-etre : une edition imprimee, du merch trop mignon, et Doudou sous les projecteurs !` | value pinned in the brief | C-CF-506 | Core features, Languages and localisation rule 5 |
| `about.support_hidden` | value pinned in the brief | C-CF-507 | Core features, Languages and localisation rule 5 |
| `Fais partie de l'aventure, ou vis pour toujours avec cette question "Et si j'avais aide Doudou a devenir une legende ?"` | value pinned in the brief | C-CF-507 | Core features, Languages and localisation rule 5 |
| `legal.publisher_body` | value pinned in the brief | C-CF-510 | Core features, Languages and localisation rule 5 |
| `Le site Doudou Fever est cree et publie par Damien Lorca et Camille Rouyer.` | value pinned in the brief | C-CF-510 | Core features, Languages and localisation rule 5 |
| `E-mail de contact` | value pinned in the brief | C-CF-511 | Core features, Languages and localisation rule 5 |
| `Heberge par Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France.` | value pinned in the brief | C-CF-512 | Core features, Languages and localisation rule 5 |
| `legal.domains_body` | value pinned in the brief | C-CF-513 | Core features, Languages and localisation rule 5 |
| `Les domaines doudoufever.example, www.doudoufever.example, doudou-fever.example et doudoufever-comic.example sont enregistres aupres de Registre Clair SARL, 4 quai du Port, 13002 Marseille, France.` | value pinned in the brief | C-CF-513 | Core features, Languages and localisation rule 5 |
| `legal.property_body` | value pinned in the brief | C-CF-514 | Core features, Languages and localisation rule 5 |
| `Tout le contenu de ce site est protege. Aucune licence n'est accordee, et toute reproduction, diffusion, modification ou exploitation sans autorisation prealable est interdite.` | value pinned in the brief | C-CF-514 | Core features, Languages and localisation rule 5 |
| `legal.terms_body` | value pinned in the brief | C-CF-515 | Core features, Languages and localisation rule 5 |
| `L'utilisation de ce site est personnelle. Les utilisateurs s'engagent a ne pas perturber le site. Les liens externes comme Tipbox ne relevent pas de la responsabilite de l'editeur, y compris pour les incidents de paiement. Le site peut etre modifie ou suspendu sans preavis.` | value pinned in the brief | C-CF-515 | Core features, Languages and localisation rule 5 |
| `legal.data_body` | value pinned in the brief | C-CF-516 | Core features, Languages and localisation rule 5 |
| `L'adresse, la progression et les pourboires rattaches d'un lecteur sont collectes uniquement pour faire fonctionner le compte lecteur. Ils ne sont jamais revendus et peuvent etre exportes, corriges ou supprimes depuis la page du compte.` | value pinned in the brief | C-CF-516 | Core features, Languages and localisation rule 5 |
| `legal.cookies_body` | value pinned in the brief | C-CF-517 | Core features, Languages and localisation rule 5 |
| `Les cles fonctionnelles dd-consent, dd-language, dd-last-chapter, les cles dd-progress-, dd-session et dd-studio-session sont posees quel que soit le choix de consentement car elles retiennent seulement la place, la langue et la session du lecteur. La mesure ne demarre qu'apres Accepter.` | value pinned in the brief | C-CF-517 | Core features, Languages and localisation rule 5 |
| `Ces conditions sont regies par le droit francais. Tout litige releve des tribunaux de Paris.` | value pinned in the brief | C-CF-518 | Core features, Languages and localisation rule 5 |
| `reader.meta_title` | value pinned in the brief | C-CF-521 | Core features, Languages and localisation rule 5 |
| `{number}` | value pinned in the brief | C-CF-521 | Core features, Languages and localisation rule 5 |
| `{title}` | value pinned in the brief | C-CF-521 | Core features, Languages and localisation rule 5 |
| `welcome to Varny` | value pinned in the brief | C-CF-523 | Core features, Languages and localisation rule 6 |
| `bonjour Varny` | value pinned in the brief | C-CF-523 | Core features, Languages and localisation rule 6 |
| `under pressure` | value pinned in the brief | C-CF-524 | Core features, Languages and localisation rule 6 |
| `sous pression` | value pinned in the brief | C-CF-524 | Core features, Languages and localisation rule 6 |
| `sheep don't sleep` | value pinned in the brief | C-CF-525 | Core features, Languages and localisation rule 6 |
| `moutons insomniaques` | value pinned in the brief | C-CF-525 | Core features, Languages and localisation rule 6 |
| `scratch that !` | value pinned in the brief | C-CF-526 | Core features, Languages and localisation rule 6 |
| `on efface tout !` | value pinned in the brief | C-CF-526 | Core features, Languages and localisation rule 6 |
| `wow ...` | value pinned in the brief | C-CF-527 | Core features, Languages and localisation rule 6 |
| `ouf ...` | value pinned in the brief | C-CF-527 | Core features, Languages and localisation rule 6 |
| `the big mix` | value pinned in the brief | C-CF-528 | Core features, Languages and localisation rule 6 |
| `le grand mix` | value pinned in the brief | C-CF-528 | Core features, Languages and localisation rule 6 |
| `dd-consent` | value pinned in the brief | C-CF-536 | Core features, Consent, measurement and page views rule 2 |
| `accepted` | value pinned in the brief | C-CF-536 | Core features, Consent, measurement and page views rule 2 |
| `declined` | value pinned in the brief | C-CF-536 | Core features, Consent, measurement and page views rule 2 |
| `dd-progress-` | value pinned in the brief | C-CF-539 | Core features, Consent, measurement and page views rule 3 |
| `dd-session` | value pinned in the brief | C-CF-539 | Core features, Consent, measurement and page views rule 3 |
| `dd-studio-session` | value pinned in the brief | C-CF-539 | Core features, Consent, measurement and page views rule 3 |
| `POST /api/events` | value pinned in the brief | C-CF-544 | Core features, Consent, measurement and page views rule 5 |
| `name` | value pinned in the brief | C-CF-544 | Core features, Consent, measurement and page views rule 5 |
| `params` | value pinned in the brief | C-CF-544 | Core features, Consent, measurement and page views rule 5 |
| `chapter_opened` | value pinned in the brief | C-CF-546 | Core features, Consent, measurement and page views rule 5 |
| `volume` | value pinned in the brief | C-CF-546 | Core features, Consent, measurement and page views rule 5 |
| `chapter` | value pinned in the brief | C-CF-546 | Core features, Consent, measurement and page views rule 5 |
| `panel_reached` | value pinned in the brief | C-CF-547 | Core features, Consent, measurement and page views rule 5 |
| `panel` | value pinned in the brief | C-CF-547 | Core features, Consent, measurement and page views rule 5 |
| `elapsed_seconds` | value pinned in the brief | C-CF-547 | Core features, Consent, measurement and page views rule 5 |
| `chapter_completed` | value pinned in the brief | C-CF-548 | Core features, Consent, measurement and page views rule 5 |
| `chapter_abandoned` | value pinned in the brief | C-CF-549 | Core features, Consent, measurement and page views rule 5 |
| `last_panel` | value pinned in the brief | C-CF-549 | Core features, Consent, measurement and page views rule 5 |
| `tip_control_pressed` | value pinned in the brief | C-CF-550 | Core features, Consent, measurement and page views rule 5 |
| `route` | value pinned in the brief | C-CF-550 | Core features, Consent, measurement and page views rule 5 |
| `chapter_load_failed` | value pinned in the brief | C-CF-551 | Core features, Consent, measurement and page views rule 5 |
| `failure` | value pinned in the brief | C-CF-551 | Core features, Consent, measurement and page views rule 5 |
| `language_switched` | value pinned in the brief | C-CF-552 | Core features, Consent, measurement and page views rule 5 |
| `fullscreen_toggled` | value pinned in the brief | C-CF-553 | Core features, Consent, measurement and page views rule 5 |
| `state` | value pinned in the brief | C-CF-553 | Core features, Consent, measurement and page views rule 5 |
| `POST /api/page-views` | value pinned in the brief | C-CF-556 | Core features, Consent, measurement and page views rule 6 |
| `chapter-id` | value pinned in the brief | C-CF-559 | Core features, Consent, measurement and page views rule 6 |
| `index` | value pinned in the brief | C-CF-560 | Core features, Consent, measurement and page views rule 6 |
| `legal` | value pinned in the brief | C-CF-560 | Core features, Consent, measurement and page views rule 6 |
| `support-return` | value pinned in the brief | C-CF-560 | Core features, Consent, measurement and page views rule 6 |
| `account` | value pinned in the brief | C-CF-560 | Core features, Consent, measurement and page views rule 6 |
| `not-found` | value pinned in the brief | C-CF-560 | Core features, Consent, measurement and page views rule 6 |
| `GET /api/studio/page-views` | value pinned in the brief | C-CF-565 | Core features, Consent, measurement and page views rule 8 |
| `GET /api/studio/insights` | value pinned in the brief | C-CF-567 | Core features, Consent, measurement and page views rule 8 |
| `is Doudou!` | value pinned in the brief | C-CF-580 | Core features, About and legal rule 3 |
| `support.chip_tip` | value pinned in the brief | C-CF-592 | Core features, About and legal rule 5 |
| `$` | value pinned in the brief | C-CF-595 | Core features, About and legal rule 5 |
| `$5.00` | value pinned in the brief | C-CF-595 | Core features, About and legal rule 5 |
| `5,00 $` | value pinned in the brief | C-CF-596 | Core features, About and legal rule 5 |
| `Tips of $5.00 or more read new chapters up to 7 days early.` | value pinned in the brief | C-CF-597 | Core features, About and legal rule 5 |
| `Les pourboires de 5,00 $ ou plus lisent les nouveaux chapitres jusqu'a 7 jours plus tot.` | value pinned in the brief | C-CF-598 | Core features, About and legal rule 5 |
| `#doudou` | value pinned in the brief | C-CF-599 | Core features, About and legal rule 6 |
| `#team` | value pinned in the brief | C-CF-600 | Core features, About and legal rule 6 |
| `#equipe` | value pinned in the brief | C-CF-600 | Core features, About and legal rule 6 |
| `#support` | value pinned in the brief | C-CF-601 | Core features, About and legal rule 6 |
| `hello@example.com` | value pinned in the brief | C-CF-606 | Core features, About and legal rule 8 |
| `Nimbus Edge SAS, 12 rue des Lilas, 75011 Paris, France` | value pinned in the brief | C-CF-607 | Core features, About and legal rule 8 |
| `doudoufever.example` | value pinned in the brief | C-CF-608 | Core features, About and legal rule 8 |
| `www.doudoufever.example` | value pinned in the brief | C-CF-608 | Core features, About and legal rule 8 |
| `doudou-fever.example` | value pinned in the brief | C-CF-608 | Core features, About and legal rule 8 |
| `doudoufever-comic.example` | value pinned in the brief | C-CF-608 | Core features, About and legal rule 8 |
| `Registre Clair SARL, 4 quai du Port, 13002 Marseille, France` | value pinned in the brief | C-CF-609 | Core features, About and legal rule 8 |
| `GET /api/studio/volumes` | value pinned in the brief | C-CF-631 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 1 |
| `label` | value pinned in the brief | C-CF-632 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 1 |
| `POST /api/studio/volumes` | value pinned in the brief | C-CF-632 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 1 |
| `POST /api/studio/volumes/{id}/chapters` | value pinned in the brief | C-CF-636 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 2 |
| `draft` | value pinned in the brief | C-CF-636 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 2 |
| `GET /api/studio/volumes/{id}/chapters` | value pinned in the brief | C-CF-641 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 3 |
| `POST /api/studio/chapters/{id}/boards` | value pinned in the brief | C-CF-646 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 4 |
| `PUT /api/studio/chapters/{id}/cover` | value pinned in the brief | C-CF-647 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 4 |
| `POST /api/studio/boards/{id}/imports` | value pinned in the brief | C-CF-648 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 5; restated in Definition of done |
| `files` | value pinned in the brief | C-CF-648 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 5; restated in Definition of done |
| `file` | value pinned in the brief | C-CF-651 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 5 |
| `c<chapter>b<board>p<panel>-<role>` | value pinned in the brief | C-CF-653 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 6 |
| `c1b1p1-back.png` | value pinned in the brief | C-CF-653 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 6 |
| `chapters/{volume_order}/{chapter_number}/{file_identifier}/{sha256_of_bytes}.png` | value pinned in the brief | C-CF-677 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 11 |
| `.json` | value pinned in the brief | C-CF-680 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 11 |
| `covers/{volume_order}/{chapter_number}/{sha256_of_bytes}.png` | value pinned in the brief | C-CF-681 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 11 |
| `PATCH /api/studio/layers/{id}` | value pinned in the brief | C-CF-685 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `blend` | value pinned in the brief | C-CF-690 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `normal` | value pinned in the brief | C-CF-690 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `additive` | value pinned in the brief | C-CF-690 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `loop_mode` | value pinned in the brief | C-CF-696 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `once` | value pinned in the brief | C-CF-696 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `loop` | value pinned in the brief | C-CF-696 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `ping-pong` | value pinned in the brief | C-CF-696 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 13 |
| `PATCH /api/studio/panels/{id}` | value pinned in the brief | C-CF-698 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 14 |
| `descriptions` | value pinned in the brief | C-CF-698 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 14 |
| `409` | value pinned in the brief | C-CF-706 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 15 |
| `version_conflict` | value pinned in the brief | C-CF-706 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 15 |
| `GET /api/studio/search?q=` | value pinned in the brief | C-CF-713 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 17 |
| `layer` | value pinned in the brief | C-CF-714 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 17 |
| `translation` | value pinned in the brief | C-CF-714 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 17 |
| `GET /api/studio/chapters/{id}/manifest` | value pinned in the brief | C-CF-716 | Core features, Studio content: volumes, chapters, boards, panels and layers rule 18 |
| `ready` | value pinned in the brief | C-CF-718 | Core features, Release scheduling rule 1 |
| `scheduled` | value pinned in the brief | C-CF-718 | Core features, Release scheduling rule 1 |
| `published` | value pinned in the brief | C-CF-718 | Core features, Release scheduling rule 1 |
| `unpublished` | value pinned in the brief | C-CF-718 | Core features, Release scheduling rule 1 |
| `POST /api/studio/chapters/{id}/preflight` | value pinned in the brief | C-CF-727 | Core features, Release scheduling rule 2; restated in Definition of done |
| `passed` | value pinned in the brief | C-CF-727 | Core features, Release scheduling rule 2; restated in Definition of done |
| `failures` | value pinned in the brief | C-CF-727 | Core features, Release scheduling rule 2; restated in Definition of done |
| `rule` | value pinned in the brief | C-CF-727 | Core features, Release scheduling rule 2; restated in Definition of done |
| `message` | value pinned in the brief | C-CF-727 | Core features, Release scheduling rule 2; restated in Definition of done |
| `24000000` | value pinned in the brief | C-CF-732 | Core features, Release scheduling rule 2 |
| `3000000` | value pinned in the brief | C-CF-733 | Core features, Release scheduling rule 2 |
| `preflight_failed` | value pinned in the brief | C-CF-741 | Core features, Release scheduling rule 3 |
| `release_at` | value pinned in the brief | C-CF-745 | Core features, Release scheduling rule 4 |
| `2027-03-28T20:00:00+02:00` | value pinned in the brief | C-CF-745 | Core features, Release scheduling rule 4 |
| `2027-03-28T18:00:00Z` | value pinned in the brief | C-CF-745 | Core features, Release scheduling rule 4 |
| `Europe/Paris` | value pinned in the brief | C-CF-746 | Core features, Release scheduling rule 4 |
| `preflight_failed_at_release` | value pinned in the brief | C-CF-750 | Core features, Release scheduling rule 5 |
| `7` | value pinned in the brief | C-CF-757 | Core features, Release scheduling rule 8 |
| `waivers` | value pinned in the brief | C-CF-759 | Core features, Release scheduling rule 9 |
| `reason` | value pinned in the brief | C-CF-759 | Core features, Release scheduling rule 9 |
| `chapter.published` | value pinned in the brief | C-CF-764 | Core features, Release scheduling rule 10 |
| `chapter.scheduled` | value pinned in the brief | C-CF-765 | Core features, Release scheduling rule 10 |
| `chapter.unpublished` | value pinned in the brief | C-CF-766 | Core features, Release scheduling rule 10 |
| `layer.imported` | value pinned in the brief | C-CF-767 | Core features, Release scheduling rule 10 |
| `translated` | value pinned in the brief | C-CF-773 | Core features, Translations rule 1 |
| `reviewed` | value pinned in the brief | C-CF-773 | Core features, Translations rule 1 |
| `chrome` | value pinned in the brief | C-CF-774 | Core features, Translations rule 1 |
| `reader` | value pinned in the brief | C-CF-774 | Core features, Translations rule 1 |
| `consent` | value pinned in the brief | C-CF-774 | Core features, Translations rule 1 |
| `support` | value pinned in the brief | C-CF-774 | Core features, Translations rule 1 |
| `GET /api/studio/translations/coverage` | value pinned in the brief | C-CF-775 | Core features, Translations rule 2 |
| `total` | value pinned in the brief | C-CF-775 | Core features, Translations rule 2 |
| `percent` | value pinned in the brief | C-CF-775 | Core features, Translations rule 2 |
| `GET /api/studio/translations/{locale}?namespace=` | value pinned in the brief | C-CF-778 | Core features, Translations rule 3 |
| `key` | value pinned in the brief | C-CF-778 | Core features, Translations rule 3 |
| `source` | value pinned in the brief | C-CF-778 | Core features, Translations rule 3 |
| `value` | value pinned in the brief | C-CF-778 | Core features, Translations rule 3 |
| `note` | value pinned in the brief | C-CF-778 | Core features, Translations rule 3 |
| `PUT /api/studio/translations/{locale}/{key}` | value pinned in the brief | C-CF-779 | Core features, Translations rule 3 |
| `GET /api/studio/tips` | value pinned in the brief | C-CF-787 | Core features, Supporters, insights and settings rule 1 |
| `50` | value pinned in the brief | C-CF-787 | Core features, Supporters, insights and settings rule 1 |
| `next_cursor` | value pinned in the brief | C-CF-788 | Core features, Supporters, insights and settings rule 1 |
| `tip_id` | value pinned in the brief | C-CF-790 | Core features, Supporters, insights and settings rule 1 |
| `tipbox` | value pinned in the brief | C-CF-791 | Core features, Supporters, insights and settings rule 1 |
| `manual` | value pinned in the brief | C-CF-791 | Core features, Supporters, insights and settings rule 1 |
| `POST /api/studio/tips` | value pinned in the brief | C-CF-792 | Core features, Supporters, insights and settings rule 3 |
| `amount` | value pinned in the brief | C-CF-792 | Core features, Supporters, insights and settings rule 3 |
| `received_at` | value pinned in the brief | C-CF-792 | Core features, Supporters, insights and settings rule 3 |
| `entitlement` | value pinned in the brief | C-CF-794 | Core features, Supporters, insights and settings rule 1 |
| `unmatched` | value pinned in the brief | C-CF-794 | Core features, Supporters, insights and settings rule 1 |
| `awaiting_confirmation` | value pinned in the brief | C-CF-794 | Core features, Supporters, insights and settings rule 1 |
| `revoked` | value pinned in the brief | C-CF-794 | Core features, Supporters, insights and settings rule 1 |
| `received` | value pinned in the brief | C-CF-795 | Core features, Supporters, insights and settings rule 1 |
| `POST /api/studio/tips/{id}/confirm-match` | value pinned in the brief | C-CF-796 | Core features, Supporters, insights and settings rule 2 |
| `GET /api/studio/tips/totals` | value pinned in the brief | C-CF-801 | Core features, Supporters, insights and settings rule 4 |
| `settled_amount` | value pinned in the brief | C-CF-801 | Core features, Supporters, insights and settings rule 4 |
| `YYYY-MM` | value pinned in the brief | C-CF-801 | Core features, Supporters, insights and settings rule 4 |
| `GET /api/studio/overview` | value pinned in the brief | C-CF-804 | Core features, Supporters, insights and settings rule 5 |
| `next_drop` | value pinned in the brief | C-CF-804 | Core features, Supporters, insights and settings rule 5 |
| `unready` | value pinned in the brief | C-CF-804 | Core features, Supporters, insights and settings rule 5 |
| `reading` | value pinned in the brief | C-CF-804 | Core features, Supporters, insights and settings rule 5 |
| `GET /api/studio/settings` | value pinned in the brief | C-CF-810 | Core features, Supporters, insights and settings rule 6 |
| `contact_email` | value pinned in the brief | C-CF-810 | Core features, Supporters, insights and settings rule 6 |
| `time_zone` | value pinned in the brief | C-CF-810 | Core features, Supporters, insights and settings rule 6 |
| `PATCH /api/studio/settings` | value pinned in the brief | C-CF-811 | Core features, Supporters, insights and settings rule 6 |
| `currency` | value pinned in the brief | C-CF-812 | Core features, Supporters, insights and settings rule 6 |
| `default_locale` | value pinned in the brief | C-CF-812 | Core features, Supporters, insights and settings rule 6 |
| `asset_version` | value pinned in the brief | C-CF-812 | Core features, Supporters, insights and settings rule 6 |
| `GET /api/studio/integrations/tipbox` | value pinned in the brief | C-CF-816 | Core features, Supporters, insights and settings rule 7 |
| `page_url` | value pinned in the brief | C-CF-816 | Core features, Supporters, insights and settings rule 7 |
| `secret_last_four` | value pinned in the brief | C-CF-816 | Core features, Supporters, insights and settings rule 7 |
| `secret_created_at` | value pinned in the brief | C-CF-816 | Core features, Supporters, insights and settings rule 7 |
| `secret_last_used_at` | value pinned in the brief | C-CF-816 | Core features, Supporters, insights and settings rule 7 |
| `81d7` | value pinned in the brief | C-CF-817 | Core features, Supporters, insights and settings rule 7 |
| `PUT /api/studio/integrations/tipbox/secret` | value pinned in the brief | C-CF-819 | Core features, Supporters, insights and settings rule 7 |
| `secret` | value pinned in the brief | C-CF-819 | Core features, Supporters, insights and settings rule 7 |
| `POST /api/studio/asset-version` | value pinned in the brief | C-CF-822 | Core features, Supporters, insights and settings rule 8 |
| `66` | value pinned in the brief | C-CF-825 | Core features, Supporters, insights and settings rule 8 |
| `/studio` | value pinned in the brief | C-UF-02 | User flow, Routes table |
| `Next drop` | value pinned in the brief | C-UF-02 | User flow, Routes table |
| `Unready work` | value pinned in the brief | C-UF-02 | User flow, Routes table |
| `Support` | value pinned in the brief | C-UF-02 | User flow, Routes table |
| `Reading` | value pinned in the brief | C-UF-02 | User flow, Routes table |
| `/studio/volumes` | value pinned in the brief | C-UF-03 | User flow, Routes table |
| `New volume` | value pinned in the brief | C-UF-03 | User flow, Routes table |
| `/studio/volumes/:volumeId` | value pinned in the brief | C-UF-04 | User flow, Routes table |
| `New chapter` | value pinned in the brief | C-UF-04 | User flow, Routes table |
| `Doudou steps off the night bus into Varny.` | value pinned in the brief | C-UF-36 | User flow, Journeys journey 6 |
| `Vol. II` | value pinned in the brief | C-UF-38 | User flow, Journeys journey 8 |
| `the night shift` | value pinned in the brief | C-UF-38 | User flow, Journeys journey 8 |
| `le service de nuit` | value pinned in the brief | C-UF-38 | User flow, Journeys journey 8 |
| `New board` | value pinned in the brief | C-UF-39 | User flow, Journeys journey 8 |
| `c1b1p1-stage.png` | value pinned in the brief | C-UF-40 | User flow, Journeys journey 8 |
| `stage` | value pinned in the brief | C-UF-41 | User flow, Journeys journey 8 |
| `3` | value pinned in the brief | C-UF-41 | User flow, Journeys journey 8 |
| `Server counts` | value pinned in the brief | C-UF-45 | User flow, Journeys journey 10 |
| `Measured events` | value pinned in the brief | C-UF-45 | User flow, Journeys journey 10 |
| `/studio/insights` | value pinned in the brief | C-UF-45 | User flow, Journeys journey 10 |
| `Inter` | value pinned in the brief | C-UX-20 | UI/UX notes, Typeface and type paragraph |
| `GET /api/health` | value pinned in the brief | C-TR-12 | Technical requirements health |
| `{"status": "ok"}` | value pinned in the brief | C-TR-12 | Technical requirements health |
| `/api` | value pinned in the brief | C-TR-19 | Technical requirements bullet 1 |
| `X-Request-Id` | value pinned in the brief | C-TR-19 | Technical requirements bullet 1 |
| `request_id` | value pinned in the brief | C-TR-20 | Technical requirements bullet 1 |
| `{"error": {"code": ..., "message": ..., "field": ..., "request_id": ...}}` | value pinned in the brief | C-TR-21 | Technical requirements bullet 2 |
| `Strict-Transport-Security` | value pinned in the brief | C-TR-28 | Technical requirements security |
| `Content-Security-Policy` | value pinned in the brief | C-TR-29 | Technical requirements security |
| `frame-ancestors 'none'` | value pinned in the brief | C-TR-29 | Technical requirements security |
| `X-Frame-Options: DENY` | value pinned in the brief | C-TR-30 | Technical requirements security |
| `X-Content-Type-Options: nosniff` | value pinned in the brief | C-TR-31 | Technical requirements security |
| `Referrer-Policy: strict-origin-when-cross-origin` | value pinned in the brief | C-TR-32 | Technical requirements security |
| `Permissions-Policy` | value pinned in the brief | C-TR-33 | Technical requirements security |
| `fullscreen` | value pinned in the brief | C-TR-33 | Technical requirements security |
| `Cache-Control: public, max-age=31536000, immutable` | value pinned in the brief | C-TR-34 | Technical requirements caching |
| `public` | value pinned in the brief | C-TR-35 | Technical requirements caching |
| `max-age` | value pinned in the brief | C-TR-35 | Technical requirements caching |
| `private` | value pinned in the brief | C-TR-36 | Technical requirements caching |
| `no-store` | value pinned in the brief | C-TR-36 | Technical requirements caching |
| `/api/me` | value pinned in the brief | C-TR-39 | Technical requirements caching |
| `image_signing_key` | value pinned in the brief | C-TR-42 | Technical requirements signatures |
| `"Helvetica Neue", Helvetica, Arial, "Liberation Sans", system-ui, sans-serif` | value pinned in the brief | C-TR-47 | Technical requirements fonts |
| `en-GB` | value pinned in the brief | C-DM-11 | Data model locales |
| `English` | value pinned in the brief | C-DM-11 | Data model locales |
| `fr-FR` | value pinned in the brief | C-DM-11 | Data model locales |
| `Francais` | value pinned in the brief | C-DM-11 | Data model locales |
| `kind` | value pinned in the brief | C-DM-50 | Data model layers |
| `image` | value pinned in the brief | C-DM-50 | Data model layers |
| `map` | value pinned in the brief | C-DM-50 | Data model layers |
| `sprite` | value pinned in the brief | C-DM-50 | Data model layers |
| `revoked_reason` | value pinned in the brief | C-DM-52 | Data model entitlements |
| `18:00` | value pinned in the brief | C-DM-66 | Data model seed table |
| `back` | value pinned in the brief | C-DM-73 | Data model seed data |
| `-4` | value pinned in the brief | C-DM-73 | Data model seed data |
| `characters` | value pinned in the brief | C-DM-76 | Data model seed data |
| `2` | value pinned in the brief | C-DM-76 | Data model seed data |
| `sign` | value pinned in the brief | C-DM-77 | Data model seed data |
| `selectable` | value pinned in the brief | C-DM-79 | Data model seed data |
| `entry_duration` | value pinned in the brief | C-DM-79 | Data model seed data |
| `0.6` | value pinned in the brief | C-DM-79 | Data model seed data |
| `Doudou arrives in Varny with a suitcase full of records.` | value pinned in the brief | C-DM-81 | Data model chapter descriptions table |
| `Doudou arrive a Varny avec une valise pleine de disques.` | value pinned in the brief | C-DM-82 | Data model chapter descriptions table |
| `The first gig goes wrong in every possible way.` | value pinned in the brief | C-DM-83 | Data model chapter descriptions table |
| `Le premier concert tourne mal de toutes les facons.` | value pinned in the brief | C-DM-84 | Data model chapter descriptions table |
| `A night without sleep before the big audition.` | value pinned in the brief | C-DM-85 | Data model chapter descriptions table |
| `Une nuit blanche avant la grande audition.` | value pinned in the brief | C-DM-86 | Data model chapter descriptions table |
| `Doudou efface tout le set et recommence.` | value pinned in the brief | C-DM-88 | Data model chapter descriptions table |
| `The crowd finally dances.` | value pinned in the brief | C-DM-89 | Data model chapter descriptions table |
| `La foule danse enfin.` | value pinned in the brief | C-DM-90 | Data model chapter descriptions table |
| `Jean-Loic et Milan preparent la plus grande fete de Varny.` | value pinned in the brief | C-DM-92 | Data model chapter descriptions table |
| `Doudou descend du bus de nuit a Varny.` | value pinned in the brief | C-DM-94 | Data model panel descriptions table |
| `L'appartement au-dessus du bar est petit et bruyant.` | value pinned in the brief | C-DM-96 | Data model panel descriptions table |
| `Jean-Loic donne a Doudou une cle et un avertissement.` | value pinned in the brief | C-DM-98 | Data model panel descriptions table |
| `Milan films dinner for her followers.` | value pinned in the brief | C-DM-99 | Data model panel descriptions table |
| `Milan filme le diner pour ses abonnes.` | value pinned in the brief | C-DM-100 | Data model panel descriptions table |
| `Doudou unpacks the turntables on the kitchen table.` | value pinned in the brief | C-DM-101 | Data model panel descriptions table |
| `Doudou deballe les platines sur la table de la cuisine.` | value pinned in the brief | C-DM-102 | Data model panel descriptions table |
| `The speakers crackle before the first song.` | value pinned in the brief | C-DM-103 | Data model panel descriptions table |
| `Les enceintes gresillent avant le premier morceau.` | value pinned in the brief | C-DM-104 | Data model panel descriptions table |
| `Nobody on the dance floor moves.` | value pinned in the brief | C-DM-105 | Data model panel descriptions table |
| `Personne ne bouge sur la piste.` | value pinned in the brief | C-DM-106 | Data model panel descriptions table |
| `Doudou pulls the plug in a panic.` | value pinned in the brief | C-DM-107 | Data model panel descriptions table |
| `Doudou debranche tout en panique.` | value pinned in the brief | C-DM-108 | Data model panel descriptions table |
| `Doudou counts beats instead of sheep.` | value pinned in the brief | C-DM-109 | Data model panel descriptions table |
| `Doudou compte des temps au lieu des moutons.` | value pinned in the brief | C-DM-110 | Data model panel descriptions table |
| `Milan brings midnight pancakes.` | value pinned in the brief | C-DM-111 | Data model panel descriptions table |
| `Milan apporte des crepes de minuit.` | value pinned in the brief | C-DM-112 | Data model panel descriptions table |
| `The sun rises over an unfinished mix.` | value pinned in the brief | C-DM-113 | Data model panel descriptions table |
| `Le soleil se leve sur un mix inacheve.` | value pinned in the brief | C-DM-114 | Data model panel descriptions table |
| `Doudou deletes every track on the laptop.` | value pinned in the brief | C-DM-115 | Data model panel descriptions table |
| `Doudou efface chaque morceau de l'ordinateur.` | value pinned in the brief | C-DM-116 | Data model panel descriptions table |
| `Jean-Loic hums a tune from the bar.` | value pinned in the brief | C-DM-117 | Data model panel descriptions table |
| `Jean-Loic fredonne un air du bar.` | value pinned in the brief | C-DM-118 | Data model panel descriptions table |
| `A new beat starts with that tune.` | value pinned in the brief | C-DM-119 | Data model panel descriptions table |
| `Un nouveau rythme nait de cet air.` | value pinned in the brief | C-DM-120 | Data model panel descriptions table |
| `The whole town queues outside the bar.` | value pinned in the brief | C-DM-121 | Data model panel descriptions table |
| `Toute la ville fait la queue devant le bar.` | value pinned in the brief | C-DM-122 | Data model panel descriptions table |
| `Doudou drops the first beat.` | value pinned in the brief | C-DM-123 | Data model panel descriptions table |
| `Doudou lance le premier rythme.` | value pinned in the brief | C-DM-124 | Data model panel descriptions table |
| `Varny dances until morning.` | value pinned in the brief | C-DM-125 | Data model panel descriptions table |
| `Varny danse jusqu'au matin.` | value pinned in the brief | C-DM-126 | Data model panel descriptions table |
| `Posters for the big mix cover the flat.` | value pinned in the brief | C-DM-127 | Data model panel descriptions table |
| `Les affiches du grand mix couvrent l'appartement.` | value pinned in the brief | C-DM-128 | Data model panel descriptions table |
| `1.000000` | value pinned in the brief | C-DM-129 | Data model seed tips |
| `go doudou go` | value pinned in the brief | C-DM-129 | Data model seed tips |
| `tbx_seed_002` | value pinned in the brief | C-DM-130 | Data model seed tips |
| `friend@example.com` | value pinned in the brief | C-DM-130 | Data model seed tips |
| `for the bus scene` | value pinned in the brief | C-DM-130 | Data model seed tips |
| `overview` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `volumes` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `translations` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `releases` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `supporters` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `insights` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `settings` | value pinned in the brief | C-FE-51 | Front-end specification studio console |
| `Number` | value pinned in the brief | C-FE-53 | Front-end specification studio console |
| `Title` | value pinned in the brief | C-FE-53 | Front-end specification studio console |
| `State` | value pinned in the brief | C-FE-53 | Front-end specification studio console |
| `Release` | value pinned in the brief | C-FE-53 | Front-end specification studio console |
| `Readiness` | value pinned in the brief | C-FE-53 | Front-end specification studio console |
| `Image bytes` | value pinned in the brief | C-FE-53 | Front-end specification studio console |
| `0.0.0.0` | value pinned in the brief | C-DC-03 | Deployment contract bullet 9 |
| `127.0.0.1` | value pinned in the brief | C-DC-03 | Deployment contract bullet 9 |
| `localhost` | value pinned in the brief | C-DC-03 | Deployment contract bullet 9 |
| `${APP_PUBLIC_PORT}:4173` | value pinned in the brief | C-DC-04 | Deployment contract bullet 1 |
| `4173` | value pinned in the brief | C-DC-04 | Deployment contract bullet 1 |
| `{"items": [...], "next_cursor": ...}` | value pinned in the brief | C-DC-19 | Deployment contract API shapes |
| `cursor` | value pinned in the brief | C-DC-19 | Deployment contract API shapes |
| `by Camille Rouyer and Damien Lorca` | English value of chrome.byline | C-CF-338 | Core features, Languages and localisation rule 5 |
| `This chapter opens {date}.` | English value of locked.timing | C-CF-354 | Core features, Languages and localisation rule 5 |
| `This chapter is still being drawn.` | English value of locked.drawing | C-CF-355 | Core features, Languages and localisation rule 5 |
| `Supporters read it as soon as it is finished.` | English value of locked.support | C-CF-357 | Core features, Languages and localisation rule 5 |
| `Hey you ✨ This site uses cookies to measure the traffic.` | English value of consent.message | C-CF-358 | Core features, Languages and localisation rule 5 |
| `Thank you. Sign in and we will attach it to your account.` | English value of support.sign_in | C-CF-362 | Core features, Languages and localisation rule 5 |
| `Thank you. Every tip helps, and this one goes straight into the next chapter.` | English value of support.below_threshold | C-CF-363 | Core features, Languages and localisation rule 5 |
| `This thank-you link has expired.` | English value of support.expired | C-CF-365 | Core features, Languages and localisation rule 5 |
| `♥ give a tip ♥` | English value of support.chip_tip | C-CF-366 | Core features, Languages and localisation rule 5 |
| `Doudou is a megalomaniac sheep, tender and dead set on becoming a DJ. With Jean-Loic, a wild barman, and Milan, a future cooking star on socials, he mixes chaos and big dreams in a flat full of laughs and late-night noise. It's cool, it's fun, it's Doudou Fever.` | English value of about.legend_body | C-CF-409 | Core features, Languages and localisation rule 5 |
| `Creative developer and animator, half-coder half-wizard. He animates images, makes pixels move, and transforms lines of code into cool and magical experiences.` | English value of about.team_dam_body | C-CF-411 | Core features, Languages and localisation rule 5 |
| `Art director, illustrator and digital brush master. She draws faster than her shadow and gives life to each character with style, emotion...` | English value of about.team_ca_body | C-CF-413 | Core features, Languages and localisation rule 5 |
| `Support Doudou on his way to glory and help him become a legend. One day, maybe : a printed edition, sweet merch, and Doudou stealing the spotlight!` | English value of about.support_body | C-CF-414 | Core features, Languages and localisation rule 5 |
| `Be part of the adventure, or live with this question forever "What if I had helped Doudou become a legend?"` | English value of about.support_hidden | C-CF-415 | Core features, Languages and localisation rule 5 |
| `The Doudou Fever website is created and published by Damien Lorca and Camille Rouyer.` | English value of legal.publisher_body | C-CF-418 | Core features, Languages and localisation rule 5 |
| `The domains doudoufever.example, www.doudoufever.example, doudou-fever.example and doudoufever-comic.example are registered with Registre Clair SARL, 4 quai du Port, 13002 Marseille, France.` | English value of legal.domains_body | C-CF-421 | Core features, Languages and localisation rule 5 |
| `All content of this website is protected. No licence is granted, and any reproduction, distribution, modification or exploitation without prior authorisation is prohibited.` | English value of legal.property_body | C-CF-422 | Core features, Languages and localisation rule 5 |
| `Use of this website is personal. Users agree not to disrupt the site. External links such as Tipbox are outside the publisher's responsibility, including for payment incidents. The site may be modified or suspended without notice.` | English value of legal.terms_body | C-CF-423 | Core features, Languages and localisation rule 5 |
| `A reader's address, progress and matched tips are collected only to run the reader account. They are never resold, and can be exported, corrected or deleted from the account page.` | English value of legal.data_body | C-CF-424 | Core features, Languages and localisation rule 5 |
| `The functional keys dd-consent, dd-language, dd-last-chapter, the dd-progress- keys, dd-session and dd-studio-session are set whatever the consent decision because they only remember the reader's place, language and session. Measurement runs only after Accept.` | English value of legal.cookies_body | C-CF-425 | Core features, Languages and localisation rule 5 |
| `Coucou ✨ Ce site utilise des cookies pour mesurer la frequentation.` | French value of consent.message | C-CF-450 | Core features, Languages and localisation rule 5 |
| `♥ laisse un pourboire ♥` | French value of support.chip_tip | C-CF-458 | Core features, Languages and localisation rule 5 |
| `Doudou erases the whole set and starts again.` | English description of chapter 4 | C-DM-87 | Data model chapter descriptions table |
| `Jean-Loic and Milan plan the biggest party in Varny.` | English description of chapter 6 | C-DM-91 | Data model chapter descriptions table |
| `The flat above the bar is small and loud.` | English description of chapter 1 board 1 panel 2 | C-DM-95 | Data model panel descriptions table |
| `Jean-Loic hands Doudou a key and a warning.` | English description of chapter 1 board 1 panel 3 | C-DM-97 | Data model panel descriptions table |
| `Doudou Fever - Interactive Comic` | English title of / | C-CF-53 | Core features, The reading surface rule 3 |
| `Doudou Fever is an interactive comic. Follow the adventure of a megalomaniac sheep who wants to make the world dance. Created by Camille Rouyer & Damien Lorca.` | English description of / | C-CF-54 | Core features, The reading surface rule 3 |
| `Chapters &#124; Doudou Fever - Interactive Comic` | English title of /chapters | C-CF-55 | Core features, The reading surface rule 3 |
| `Pick a track from the Doudou Fever record rack and start reading.` | English description of /chapters | C-CF-56 | Core features, The reading surface rule 3 |
| `Chapter #1: Welcome To Varny - Doudou Fever - Interactive Comic` | English title of /chapter/1 | C-CF-57 | Core features, The reading surface rule 3 |
| `Read chapter 1, welcome to Varny, of the Doudou Fever interactive comic.` | English description of /chapter/1 | C-CF-58 | Core features, The reading surface rule 3 |
| `About &#124; Doudou Fever - Interactive Comic` | English title of /about | C-CF-59 | Core features, The reading surface rule 3 |
| `Meet Doudou, the sheep who wants to make the world dance, and the two people who draw and animate him.` | English description of /about | C-CF-60 | Core features, The reading surface rule 3 |
| `Legal Notice and Terms of Use &#124; Doudou Fever - Interactive Comic` | English title of /legal | C-CF-61 | Core features, The reading surface rule 3 |
| `Publisher, hosting, rights, terms, personal data and cookies for the Doudou Fever website.` | English description of /legal | C-CF-62 | Core features, The reading surface rule 3 |
| `Thank You &#124; Doudou Fever - Interactive Comic` | English title of /support/return | C-CF-63 | Core features, The reading surface rule 3 |
| `Thanks for tipping Doudou Fever.` | English description of /support/return | C-CF-64 | Core features, The reading surface rule 3 |
| `Your Account &#124; Doudou Fever - Interactive Comic` | English title of /account | C-CF-65 | Core features, The reading surface rule 3 |
| `Your Doudou Fever reading account.` | English description of /account | C-CF-66 | Core features, The reading surface rule 3 |
| `Page Not Found &#124; Doudou Fever - Interactive Comic` | English title of not-found | C-CF-67 | Core features, The reading surface rule 3 |
| `This page of Doudou Fever does not exist.` | English description of not-found | C-CF-68 | Core features, The reading surface rule 3 |
| `Doudou Fever - BD interactive` | French title of /fr | C-CF-71 | Core features, The reading surface rule 3 |
| `Doudou Fever est une BD interactive. Suis l'aventure d'un mouton megalomane qui veut faire danser le monde. Creee par Camille Rouyer & Damien Lorca.` | French description of /fr | C-CF-72 | Core features, The reading surface rule 3 |
| `Chapitres &#124; Doudou Fever - BD interactive` | French title of /fr/chapters | C-CF-73 | Core features, The reading surface rule 3 |
| `Choisis une piste dans le bac a disques de Doudou Fever et commence a lire.` | French description of /fr/chapters | C-CF-74 | Core features, The reading surface rule 3 |
| `Chapitre #1 : Bonjour Varny - Doudou Fever - BD interactive` | French title of /fr/chapter/1 | C-CF-75 | Core features, The reading surface rule 3 |
| `Lis le chapitre 1, bonjour Varny, de la BD interactive Doudou Fever.` | French description of /fr/chapter/1 | C-CF-76 | Core features, The reading surface rule 3 |
| `A propos &#124; Doudou Fever - BD interactive` | French title of /fr/about | C-CF-77 | Core features, The reading surface rule 3 |
| `Rencontre Doudou, le mouton qui veut faire danser le monde, et les deux personnes qui le dessinent et l'animent.` | French description of /fr/about | C-CF-78 | Core features, The reading surface rule 3 |
| `Mentions legales et conditions d'utilisation &#124; Doudou Fever - BD interactive` | French title of /fr/legal | C-CF-79 | Core features, The reading surface rule 3 |
| `Editeur, hebergement, droits, conditions, donnees personnelles et cookies du site Doudou Fever.` | French description of /fr/legal | C-CF-80 | Core features, The reading surface rule 3 |
| `Merci &#124; Doudou Fever - BD interactive` | French title of /fr/support/return | C-CF-81 | Core features, The reading surface rule 3 |
| `Merci d'avoir soutenu Doudou Fever.` | French description of /fr/support/return | C-CF-82 | Core features, The reading surface rule 3 |
| `Ton compte &#124; Doudou Fever - BD interactive` | French title of /fr/account | C-CF-83 | Core features, The reading surface rule 3 |
| `Ton compte de lecture Doudou Fever.` | French description of /fr/account | C-CF-84 | Core features, The reading surface rule 3 |
| `Page introuvable &#124; Doudou Fever - BD interactive` | French title of not-found | C-CF-85 | Core features, The reading surface rule 3 |
| `Cette page de Doudou Fever n'existe pas.` | French description of not-found | C-CF-86 | Core features, The reading surface rule 3 |
| `This chapter opens {date}.` | English value of locked.timing | C-CF-151 | Core features, The reading surface rule 15 |
| `Ce chapitre sort le {date}.` | French value of locked.timing | C-CF-151 | Core features, The reading surface rule 15 |
| `This chapter opens {date}.` | English value of locked.timing | C-CF-354 | Core features, Languages and localisation rule 5 |
| `Ce chapitre sort le {date}.` | French value of locked.timing | C-CF-354 | Core features, Languages and localisation rule 5 |
| `This chapter opens {date}.` | English value of locked.timing | C-CF-446 | Core features, Languages and localisation rule 5 |
| `Ce chapitre sort le {date}.` | French value of locked.timing | C-CF-446 | Core features, Languages and localisation rule 5 |
| `Supporters read it as soon as it is finished.` | English value of locked.support | C-CF-154 | Core features, The reading surface rule 15 |
| `Les soutiens le lisent des qu'il est fini.` | French value of locked.support | C-CF-154 | Core features, The reading surface rule 15 |
| `Supporters read it as soon as it is finished.` | English value of locked.support | C-CF-357 | Core features, Languages and localisation rule 5 |
| `Les soutiens le lisent des qu'il est fini.` | French value of locked.support | C-CF-357 | Core features, Languages and localisation rule 5 |
| `Supporters read it as soon as it is finished.` | English value of locked.support | C-CF-449 | Core features, Languages and localisation rule 5 |
| `Les soutiens le lisent des qu'il est fini.` | French value of locked.support | C-CF-449 | Core features, Languages and localisation rule 5 |
| `This chapter is still being drawn.` | English value of locked.drawing | C-CF-157 | Core features, The reading surface rule 15 |
| `Ce chapitre est encore en dessin.` | French value of locked.drawing | C-CF-157 | Core features, The reading surface rule 15 |
| `This chapter is still being drawn.` | English value of locked.drawing | C-CF-355 | Core features, Languages and localisation rule 5 |
| `Ce chapitre est encore en dessin.` | French value of locked.drawing | C-CF-355 | Core features, Languages and localisation rule 5 |
| `This chapter is still being drawn.` | English value of locked.drawing | C-CF-447 | Core features, Languages and localisation rule 5 |
| `Ce chapitre est encore en dessin.` | French value of locked.drawing | C-CF-447 | Core features, Languages and localisation rule 5 |
| `Thank you. Sign in and we will attach it to your account.` | English value of support.sign_in | C-CF-238 | Core features, Tips and early access rule 2 |
| `Merci. Connecte-toi et nous l'ajouterons a ton compte.` | French value of support.sign_in | C-CF-238 | Core features, Tips and early access rule 2 |
| `Thank you. Sign in and we will attach it to your account.` | English value of support.sign_in | C-CF-362 | Core features, Languages and localisation rule 5 |
| `Merci. Connecte-toi et nous l'ajouterons a ton compte.` | French value of support.sign_in | C-CF-362 | Core features, Languages and localisation rule 5 |
| `Thank you. Sign in and we will attach it to your account.` | English value of support.sign_in | C-CF-454 | Core features, Languages and localisation rule 5 |
| `Merci. Connecte-toi et nous l'ajouterons a ton compte.` | French value of support.sign_in | C-CF-454 | Core features, Languages and localisation rule 5 |
| `Thank you. Your early access is active.` | English value of support.granted | C-CF-239 | Core features, Tips and early access rule 2 |
| `Merci. Ton acces anticipe est actif.` | French value of support.granted | C-CF-239 | Core features, Tips and early access rule 2 |
| `Thank you. Your early access is active.` | English value of support.granted | C-CF-361 | Core features, Languages and localisation rule 5 |
| `Merci. Ton acces anticipe est actif.` | French value of support.granted | C-CF-361 | Core features, Languages and localisation rule 5 |
| `Thank you. Your early access is active.` | English value of support.granted | C-CF-453 | Core features, Languages and localisation rule 5 |
| `Merci. Ton acces anticipe est actif.` | French value of support.granted | C-CF-453 | Core features, Languages and localisation rule 5 |
| `Thank you. Every tip helps, and this one goes straight into the next chapter.` | English value of support.below_threshold | C-CF-239 | Core features, Tips and early access rule 2 |
| `Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.` | French value of support.below_threshold | C-CF-239 | Core features, Tips and early access rule 2 |
| `Thank you. Every tip helps, and this one goes straight into the next chapter.` | English value of support.below_threshold | C-CF-363 | Core features, Languages and localisation rule 5 |
| `Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.` | French value of support.below_threshold | C-CF-363 | Core features, Languages and localisation rule 5 |
| `Thank you. Every tip helps, and this one goes straight into the next chapter.` | English value of support.below_threshold | C-CF-455 | Core features, Languages and localisation rule 5 |
| `Merci. Chaque pourboire aide, et celui-ci part droit dans le prochain chapitre.` | French value of support.below_threshold | C-CF-455 | Core features, Languages and localisation rule 5 |
| `Thank you. Your tip is on its way to us.` | English value of support.pending | C-CF-239 | Core features, Tips and early access rule 2 |
| `Merci. Ton pourboire est en route.` | French value of support.pending | C-CF-239 | Core features, Tips and early access rule 2 |
| `Thank you. Your tip is on its way to us.` | English value of support.pending | C-CF-364 | Core features, Languages and localisation rule 5 |
| `Merci. Ton pourboire est en route.` | French value of support.pending | C-CF-364 | Core features, Languages and localisation rule 5 |
| `Thank you. Your tip is on its way to us.` | English value of support.pending | C-CF-456 | Core features, Languages and localisation rule 5 |
| `Merci. Ton pourboire est en route.` | French value of support.pending | C-CF-456 | Core features, Languages and localisation rule 5 |
| `This thank-you link has expired.` | English value of support.expired | C-CF-242 | Core features, Tips and early access rule 2 |
| `Ce lien de remerciement a expire.` | French value of support.expired | C-CF-242 | Core features, Tips and early access rule 2 |
| `This thank-you link has expired.` | English value of support.expired | C-CF-365 | Core features, Languages and localisation rule 5 |
| `Ce lien de remerciement a expire.` | French value of support.expired | C-CF-365 | Core features, Languages and localisation rule 5 |
| `This thank-you link has expired.` | English value of support.expired | C-CF-457 | Core features, Languages and localisation rule 5 |
| `Ce lien de remerciement a expire.` | French value of support.expired | C-CF-457 | Core features, Languages and localisation rule 5 |
| `Hey you ✨ This site uses cookies to measure the traffic.` | English value of consent.message | C-CF-358 | Core features, Languages and localisation rule 5 |
| `Coucou ✨ Ce site utilise des cookies pour mesurer la frequentation.` | French value of consent.message | C-CF-358 | Core features, Languages and localisation rule 5 |
| `Hey you ✨ This site uses cookies to measure the traffic.` | English value of consent.message | C-CF-450 | Core features, Languages and localisation rule 5 |
| `Coucou ✨ Ce site utilise des cookies pour mesurer la frequentation.` | French value of consent.message | C-CF-450 | Core features, Languages and localisation rule 5 |
| `Hey you ✨ This site uses cookies to measure the traffic.` | English value of consent.message | C-CF-531 | Core features, Consent, measurement and page views rule 1 |
| `Coucou ✨ Ce site utilise des cookies pour mesurer la frequentation.` | French value of consent.message | C-CF-531 | Core features, Consent, measurement and page views rule 1 |
| `{title}, locked, opens {date}` | English value of chapters.locked_name | C-CF-105 | Core features, The reading surface rule 6 |
| `{title}, verrouille, sort le {date}` | French value of chapters.locked_name | C-CF-105 | Core features, The reading surface rule 6 |
| `{title}, locked, opens {date}` | English value of chapters.locked_name | C-CF-400 | Core features, Languages and localisation rule 5 |
| `{title}, verrouille, sort le {date}` | French value of chapters.locked_name | C-CF-400 | Core features, Languages and localisation rule 5 |
| `{title}, locked, opens {date}` | English value of chapters.locked_name | C-CF-492 | Core features, Languages and localisation rule 5 |
| `{title}, verrouille, sort le {date}` | French value of chapters.locked_name | C-CF-492 | Core features, Languages and localisation rule 5 |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 10 | 20 |
| User roles | 13 | 32 |
| Core features | 312 | 825 |
| User flow | 51 | 57 |
| UI/UX notes | 47 | 93 |
| Technical requirements | 27 | 51 |
| Data model | 54 | 133 |
| Front-end specification | 36 | 63 |
| Constraints | 12 | 16 |
| Deployment contract | 84 | 121 |
| Definition of done | 0 | 0 |

Sentence counts are recounted from instruction.md: each obligation-bearing sentence, list entry and table row counts once. The brief's untitled preamble is restated in the Overview and its items cite the preamble. Definition of done restates asks already itemised; the items it restates cite it in their `src`.
