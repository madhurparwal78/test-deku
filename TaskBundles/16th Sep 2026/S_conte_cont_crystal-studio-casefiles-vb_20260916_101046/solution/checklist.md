# Checklist: Facet

Source: instruction.md
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC
Sections absent: C-BP
Items: 679
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` Facet is the public site of the Kelo creative studio. `src: Overview para 1`
- [ ] `C-OV-02` `ui` The home screen is one near-black window carrying a turning faceted crystal with the wordmark inside. `src: Overview para 1`
- [ ] `C-OV-03` `constraint` The home screen shows no scrollbar, header bar, navigation strip or footer on arrival. `src: Overview para 1`
- [ ] `C-OV-04` `capability` Every other public surface opens over the home screen as a layer. `src: Overview para 1`
- [ ] `C-OV-05` `capability` Every layer has its own address for linking. `src: Overview para 1`
- [ ] `C-OV-06` `constraint` Moving between surfaces never loads a new document. `src: Overview para 1`
- [ ] `C-OV-07` `constraint` Facet has no comments, likes, follows or public profiles. `src: Overview para 4`
- [ ] `C-OV-08` `constraint` Facet has no pricing or checkout. `src: Overview para 4`
- [ ] `C-OV-09` `constraint` Facet has no search box on the public site. `src: Overview para 4`
- [ ] `C-OV-10` `constraint` Facet has no notification bell, badge count or toast stack. `src: Overview para 4`
- [ ] `C-OV-11` `constraint` Facet ships or fetches no image, font, audio or video file of its own. `src: Overview para 4`
- [ ] `C-OV-12` `capability` A published case file keeps serving published text during an author rewrite of a pending copy. `src: Overview para 5`

## C-RL User roles

- [ ] `C-RL-01` `role` A signed-out visitor reads published case files. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A signed-out visitor sends an enquiry attributed to no account. `src: User roles table row 1`
- [ ] `C-RL-03` `constraint` A signed-out visitor cannot reach the studio console. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A visitor with a verified address sends an enquiry attributed to the account. `src: User roles table row 2`
- [ ] `C-RL-05` `role` A visitor cannot reach the studio console. `src: User roles table row 2`
- [ ] `C-RL-06` `role` A visitor cannot gain the author or editor role through any own action. `src: User roles table row 2`
- [ ] `C-RL-07` `role` An author creates a case file. `src: User roles table row 3`
- [ ] `C-RL-08` `role` An author edits a case file the author created. `src: User roles table row 3`
- [ ] `C-RL-09` `role` An author submits a case file the author created. `src: User roles table row 3`
- [ ] `C-RL-10` `role` An author cannot open a case file somebody else created. `src: User roles table row 3`
- [ ] `C-RL-11` `role` An author cannot edit a case file somebody else created. `src: User roles table row 3`
- [ ] `C-RL-12` `role` An author cannot approve or return a case file. `src: User roles table row 3`
- [ ] `C-RL-13` `role` An author cannot publish or unpublish a case file. `src: User roles table row 3`
- [ ] `C-RL-14` `role` An author cannot reorder the public grid. `src: User roles table row 3`
- [ ] `C-RL-15` `role` An author cannot edit sectors, the client roster or the notice page. `src: User roles table row 3`
- [ ] `C-RL-16` `role` An author cannot read the enquiry inbox or the outbox. `src: User roles table row 3`
- [ ] `C-RL-17` `role` An author cannot invite an account or change a role. `src: User roles table row 3`
- [ ] `C-RL-18` `role` An author cannot delete a case file. `src: User roles table row 3`
- [ ] `C-RL-19` `role` An editor approves a submitted case file. `src: User roles table row 4`
- [ ] `C-RL-20` `role` An editor returns a submitted case file. `src: User roles table row 4`
- [ ] `C-RL-21` `role` An editor publishes an approved case file. `src: User roles table row 4`
- [ ] `C-RL-22` `role` An editor unpublishes a published case file. `src: User roles table row 4`
- [ ] `C-RL-23` `role` An editor reorders the public grid. `src: User roles table row 4`
- [ ] `C-RL-24` `role` An editor edits sectors, the client roster or the notice page. `src: User roles table row 4`
- [ ] `C-RL-25` `role` An editor reads the enquiry inbox. `src: User roles table row 4`
- [ ] `C-RL-26` `role` An editor reads the outbox. `src: User roles table row 4`
- [ ] `C-RL-27` `role` An editor invites an account. `src: User roles table row 4`
- [ ] `C-RL-28` `role` An editor changes the role of another account. `src: User roles table row 4`
- [ ] `C-RL-29` `role` An editor exports every entity. `src: User roles table row 4`
- [ ] `C-RL-30` `role` An editor cannot change the role of the editor's own account. `src: User roles table row 4`
- [ ] `C-RL-31` `role` An editor cannot approve an own case file whenever another editor exists. `src: User roles table row 4`
- [ ] `C-RL-32` `contract` The server enforces authorization on every mutating endpoint. `src: User roles para 1`
- [ ] `C-RL-33` `contract` A direct call from a visitor or author session to an editor-only endpoint is denied. `src: User roles para 1`
- [ ] `C-RL-34` `contract` A denied call leaves the protected state unchanged. `src: User roles para 1`
- [ ] `C-RL-35` `contract` A studio read from a visitor session returns nothing of the case file. `src: User roles para 1`
- [ ] `C-RL-36` `contract` An author read of another person's case file returns nothing of the case file. `src: User roles para 1`
- [ ] `C-RL-37` `contract` The server refuses an unsigned request before judging role, ownership or state. `src: User roles para 2`
- [ ] `C-RL-38` `capability` Sign-up is open at `/join`. `src: User roles para 3`
- [ ] `C-RL-39` `role` Sign-up creates a `visitor` account whatever the request asks for. `src: User roles para 3`
- [ ] `C-RL-40` `role` An author or editor account exists only through an editor invitation. `src: User roles para 3`
- [ ] `C-RL-41` `role` A case file submitted by an editor is approved by a different editor. `src: User roles para 4`
- [ ] `C-RL-42` `capability` A sole editor's own case file moves from `draft` to `approved` on submit. `src: User roles para 4`
- [ ] `C-RL-43` `ui` The case file list shows `SELF APPROVED` in place of a reviewer name for a self-approved case file. `src: User roles para 4`
- [ ] `C-RL-44` `literal` The seeded accounts are `editor@example.com`, `author@example.com`, `author2@example.com`, `visitor@example.com`. `src: User roles para 5`
- [ ] `C-RL-45` `data` The seeded studio holds exactly one editor. `src: User roles para 5`

## C-CF Core features

- [ ] `C-CF-01` `contract` An uploaded chapter image is stored as an object in the MinIO bucket named by `STORAGE_BUCKET`. `src: Core features rule 1`
- [ ] `C-CF-02` `literal` An uploaded image key follows `case-files/{case_file_id}/{sha256_of_bytes}.{ext}`. `src: Core features rule 1`
- [ ] `C-CF-03` `contract` The key digest is the lowercase hex SHA-256 of the uploaded bytes. `src: Core features rule 1`
- [ ] `C-CF-04` `contract` Uploaded bytes are never stored in a database column. `src: Core features rule 1`
- [ ] `C-CF-05` `contract` Uploaded bytes are never written to the app filesystem. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` An upload that is not a PNG, JPEG or WebP image is rejected as invalid. `src: Core features rule 2`
- [ ] `C-CF-07` `literal` An upload larger than `5242880` bytes is rejected as invalid. `src: Core features rule 2`
- [ ] `C-CF-08` `constraint` A rejected upload writes nothing to the bucket or the database. `src: Core features rule 2`
- [ ] `C-CF-09` `contract` Media is served from the bucket through `GET /api/media/{media_id}`. `src: Core features rule 3`
- [ ] `C-CF-10` `contract` Media of an unpublished case file is denied to a request with no session. `src: Core features rule 3`
- [ ] `C-CF-11` `contract` Media of an unpublished case file is denied to a visitor or a non-owning author. `src: Core features rule 3`
- [ ] `C-CF-12` `contract` Media of an unpublished case file reaches the owner or an editor. `src: Core features rule 3`
- [ ] `C-CF-13` `contract` Media of a published case file reaches a request with no session. `src: Core features rule 3`
- [ ] `C-CF-14` `constraint` No public or presigned bucket address is ever handed out. `src: Core features rule 3`
- [ ] `C-CF-15` `contract` `GET /api/case-files/{slug}` answers not found for a case file that is not published. `src: Core features rule 4`
- [ ] `C-CF-16` `contract` The public list never includes a case file that is not published. `src: Core features rule 4`
- [ ] `C-CF-17` `contract` A case file taken down answers not found at the public address. `src: Core features rule 4`
- [ ] `C-CF-18` `capability` The owner or an editor previews an unpublished case file inside the studio. `src: Core features rule 4`
- [ ] `C-CF-19` `contract` An upload from anyone other than the owning author or an editor is denied with nothing stored. `src: Core features rule 5`
- [ ] `C-CF-20` `contract` `POST /api/auth/login` returns an `access_token` for valid credentials. `src: Core features rule 6`
- [ ] `C-CF-21` `contract` A protected call is accepted with the bearer token in the `Authorization` header. `src: Core features rule 6`
- [ ] `C-CF-22` `contract` Every sign-in issues a new session token. `src: Core features rule 6`
- [ ] `C-CF-23` `literal` A failed sign-in answers `That combination is not one we know.`. `src: Core features rule 7`
- [ ] `C-CF-24` `constraint` A failed sign-in answers the same way for an unknown address. `src: Core features rule 7`
- [ ] `C-CF-25` `constraint` A password shorter than 12 characters is refused with the pinned password message. `src: Core features rule 8`
- [ ] `C-CF-26` `constraint` No endpoint returns a password or a password hash. `src: Core features rule 8`
- [ ] `C-CF-27` `data` Email addresses are lowercased on save. `src: Core features rule 9`
- [ ] `C-CF-28` `constraint` A second account for the same address is refused as a conflict. `src: Core features rule 9`
- [ ] `C-CF-29` `capability` A visitor session lasts 30 days with no idle timeout. `src: Core features rule 10`
- [ ] `C-CF-30` `capability` An author or editor session lasts 12 hours. `src: Core features rule 10`
- [ ] `C-CF-31` `capability` An author or editor session ends after 2 hours without use. `src: Core features rule 10`
- [ ] `C-CF-32` `capability` `GET /api/auth/sessions` lists the caller's live sessions. `src: Core features rule 10`
- [ ] `C-CF-33` `capability` `DELETE /api/auth/sessions/{id}` revokes one session. `src: Core features rule 10`
- [ ] `C-CF-34` `capability` Logout revokes only the current session by default. `src: Core features rule 11`
- [ ] `C-CF-35` `capability` Logout with `all_devices` true revokes every session of the account. `src: Core features rule 11`
- [ ] `C-CF-36` `contract` A revoked token is refused on every protected call. `src: Core features rule 11`
- [ ] `C-CF-37` `capability` Sign-up creates a visitor with an unconfirmed address. `src: Core features rule 12`
- [ ] `C-CF-38` `capability` Sign-up signs the new visitor in at once. `src: Core features rule 12`
- [ ] `C-CF-39` `literal` Sign-up writes a `Confirm your address` message. `src: Core features rule 12`
- [ ] `C-CF-40` `capability` The address confirmation link stays valid for 7 days. `src: Core features rule 12`
- [ ] `C-CF-41` `capability` Following the confirmation link marks the address confirmed. `src: Core features rule 12`
- [ ] `C-CF-42` `data` An unconfirmed account shows a `verification_deadline` 7 days after sign-up. `src: Core features rule 12`
- [ ] `C-CF-43` `constraint` An unconfirmed visitor cannot send an attributed enquiry. `src: Core features rule 13`
- [ ] `C-CF-44` `ui` An unconfirmed visitor sees `CONFIRM YOUR ADDRESS TO GET A REPLY` above the enquiry form. `src: Core features rule 13`
- [ ] `C-CF-45` `literal` A reset request answers `If that address has an account, a reset link is on its way.` for any address. `src: Core features rule 14`
- [ ] `C-CF-46` `literal` A reset for an existing address writes a `Reset your password` message. `src: Core features rule 14`
- [ ] `C-CF-47` `capability` A reset message states a 60 minute expiry. `src: Core features rule 14`
- [ ] `C-CF-48` `constraint` A reset link works only once. `src: Core features rule 14`
- [ ] `C-CF-49` `constraint` A reset link stops working after a successful sign-in. `src: Core features rule 14`
- [ ] `C-CF-50` `capability` Completing a reset revokes every session of the account. `src: Core features rule 14`
- [ ] `C-CF-51` `capability` An editor invites an account naming the address, the display name, the role. `src: Core features rule 15`
- [ ] `C-CF-52` `contract` The invitation response carries `invite_url`. `src: Core features rule 15`
- [ ] `C-CF-53` `literal` An invitation writes a `Kelo has invited you` message. `src: Core features rule 15`
- [ ] `C-CF-54` `capability` The invitation message names the inviter, the role, the 14 day expiry. `src: Core features rule 15`
- [ ] `C-CF-55` `capability` Accepting an invitation sets the password. `src: Core features rule 15`
- [ ] `C-CF-56` `capability` Accepting an invitation signs the new account in. `src: Core features rule 15`
- [ ] `C-CF-57` `capability` An account holder changes the own display name. `src: Core features rule 16`
- [ ] `C-CF-58` `capability` A changed email keeps the old address as `previous_email` for 30 days. `src: Core features rule 16`
- [ ] `C-CF-59` `constraint` An editor changing the own role is refused with the role unchanged. `src: Core features rule 16`
- [ ] `C-CF-60` `constraint` Five failed sign-ins within 15 minutes lock further attempts for the account. `src: Core features rule 18`
- [ ] `C-CF-61` `capability` A locked sign-in answers with the pinned too-many-tries message. `src: Core features rule 18`
- [ ] `C-CF-62` `capability` The home screen at `/` is exactly one window tall with no document scroll. `src: Core features rule 19`
- [ ] `C-CF-63` `ui` The wordmark reads `Kelo · Creative Studio` over `Since 2011` inside one heading. `src: Core features rule 19`
- [ ] `C-CF-64` `ui` The crystal rotates continuously in a surface filling the window. `src: Core features rule 20`
- [ ] `C-CF-65` `ui` The crystal reads as forty to sixty flat facets on a broken silhouette. `src: Front-end specification crystal`
- [ ] `C-CF-66` `ui` Only a few crystal facets are bright in any frame. `src: Core features rule 20`
- [ ] `C-CF-67` `ui` Every bright crystal edge carries a cyan fringe on one side, a red fringe on the other. `src: Core features rule 20`
- [ ] `C-CF-68` `ui` Crystal facets pass in front of the wordmark letters. `src: Core features rule 20`
- [ ] `C-CF-69` `capability` Dragging on the home screen rotates the crystal with the pointer. `src: Core features rule 21`
- [ ] `C-CF-70` `ui` A released crystal keeps momentum before settling to the idle rotation. `src: Core features rule 21`
- [ ] `C-CF-71` `constraint` A drag starting on the wordmark never selects the wordmark text. `src: Core features rule 21`
- [ ] `C-CF-72` `capability` The `Drop` control reseeds the crystal without reloading the scene. `src: Core features rule 22`
- [ ] `C-CF-73` `capability` A reseed increments the reseed counter. `src: Core features rule 22`
- [ ] `C-CF-74` `data` The crystal angle, seed, count persist under `crystal_angle`, `crystal_seed`, `crystal_count`. `src: Core features rule 23`
- [ ] `C-CF-75` `constraint` A stored counter value that is not a number resets to zero. `src: Core features rule 23`
- [ ] `C-CF-76` `ui` The crystal stays visible at every width. `src: Core features rule 24`
- [ ] `C-CF-77` `capability` The crystal keeps turning behind every opened layer. `src: Core features rule 25`
- [ ] `C-CF-78` `ui` The crystal turns at half the idle rate in the studio console. `src: Core features rule 25`
- [ ] `C-CF-79` `ui` The arrival shows the drop mark, a filling progress line, the fading wordmark. `src: Core features rule 26`
- [ ] `C-CF-80` `ui` The corner controls appear one after another once arrival completes. `src: Core features rule 26`
- [ ] `C-CF-81` `ui` A spinner never shows without a progress fill beside the spinner. `src: Core features rule 26`
- [ ] `C-CF-82` `capability` Deep entry to another address skips the arrival sequence. `src: Core features rule 26`
- [ ] `C-CF-83` `ui` The corner controls are `Drop` top left, `Discover` top right, `Showreel` bottom left, `Audio` bottom right. `src: Core features rule 27`
- [ ] `C-CF-84` `ui` A corner control shows the control name only when the pointer comes near. `src: Core features rule 27`
- [ ] `C-CF-85` `ui` A corner control is acquired well before the pointer reaches the mark, the catchment size UNPINNED. `src: Core features rule 28`
- [ ] `C-CF-86` `ui` The corner controls never move into a bar or collapse into a menu sheet. `src: Core features rule 29`
- [ ] `C-CF-87` `ui` An open layer replaces `Discover` with a close control labelled for the layer. `src: Core features rule 30`
- [ ] `C-CF-88` `ui` The close labels are `Close Project`, `Close Showreel`, `Close All Projects`, `Close Story`, `Close Contact`, `Close Notice`, `Close Studio`. `src: Core features rule 30`
- [ ] `C-CF-89` `ui` The interaction bar sits at the bottom centre with a message, a line, a ring, a rolling counter. `src: Core features rule 31`
- [ ] `C-CF-90` `ui` Bar messages are uppercase, at most 24 characters, faded after 2 seconds. `src: Core features rule 31`
- [ ] `C-CF-91` `ui` A message a visitor must act on also appears as an inline notice or a pinned note. `src: Core features rule 32`
- [ ] `C-CF-92` `ui` Bar text is announced through a polite live region. `src: Core features rule 32`
- [ ] `C-CF-93` `ui` The `Audio` mark shows sound off on arrival. `src: Core features rule 33`
- [ ] `C-CF-94` `constraint` No audio is fetched before the visitor turns sound on. `src: Core features rule 33`
- [ ] `C-CF-95` `ui` The `Audio` mark shows a crossed speaker when off, a speaker with two arcs when on. `src: Core features rule 33`
- [ ] `C-CF-96` `data` The sound choice persists in browser storage under `sound`. `src: Core features rule 34`
- [ ] `C-CF-97` `constraint` No bed or cue is played from a file. `src: Core features rule 35`
- [ ] `C-CF-98` `capability` `Discover` opens the menu over the home screen without changing the address. `src: Core features rule 36`
- [ ] `C-CF-99` `ui` The menu shows `About`, `Work`, `Contact` as three large sentence-case words. `src: Core features rule 36`
- [ ] `C-CF-100` `capability` `About` opens the studio story. `src: Core features rule 36`
- [ ] `C-CF-101` `capability` `Work` opens the work carousel. `src: Core features rule 36`
- [ ] `C-CF-102` `capability` `Contact` opens the contact surface. `src: Core features rule 36`
- [ ] `C-CF-103` `ui` Pointing at a menu word dims the other two words. `src: Core features rule 37`
- [ ] `C-CF-104` `capability` Escape closes the menu. `src: Core features rule 37`
- [ ] `C-CF-105` `ui` A resting pointer triggers no menu word reaction during the arrival of the words. `src: Core features rule 38`
- [ ] `C-CF-106` `ui` The menu account line reads `Studio Sign In` for a signed-out visitor. `src: Core features rule 39`
- [ ] `C-CF-107` `ui` The menu account line reads `Studio` for an author or editor. `src: Core features rule 39`
- [ ] `C-CF-108` `ui` The menu account line reads `Your Shortlist` for a visitor. `src: Core features rule 39`
- [ ] `C-CF-109` `ui` The story shows the title, the promise, the disciplines, the client rows, the awards in order. `src: Core features rule 40`
- [ ] `C-CF-110` `literal` The studio promise reads `Making the story move.`. `src: Core features rule 40`
- [ ] `C-CF-111` `literal` The disciplines line reads `Brand · Content · Experience · Digital`. `src: Core features rule 40`
- [ ] `C-CF-112` `ui` The story headings read `Selected Clients` over the sector rows, `Awards` over the award names. `src: Core features rule 40`
- [ ] `C-CF-113` `ui` The story layer scrolls inside itself with the page staying one window tall. `src: Core features rule 41`
- [ ] `C-CF-114` `constraint` Client names on the story are not links. `src: Core features rule 41`
- [ ] `C-CF-115` `ui` Client names are separated by a generated middle dot with no trailing dot. `src: Core features rule 42`
- [ ] `C-CF-116` `capability` An editor maintains the client roster with the sector labels. `src: Core features rule 43`
- [ ] `C-CF-117` `constraint` A sector label holds at most 24 characters. `src: Core features rule 43`
- [ ] `C-CF-118` `literal` The story title elements carry the class names `about__studioTitle`, `about__studioSubtitle`. `src: Core features rule 44`
- [ ] `C-CF-119` `constraint` No class name in the page carries the studio name. `src: Core features rule 44`
- [ ] `C-CF-120` `ui` The carousel shows published titles in depth with a poster behind each title. `src: Core features rule 45`
- [ ] `C-CF-121` `ui` Releasing a carousel drag settles on the nearest title. `src: Core features rule 45`
- [ ] `C-CF-122` `capability` Choosing a carousel item opens the chosen case file. `src: Core features rule 45`
- [ ] `C-CF-123` `capability` The carousel holds only published case files in grid order, at most twelve. `src: Core features rule 46`
- [ ] `C-CF-124` `ui` A drag affordance draws on stroke by stroke when the carousel becomes draggable. `src: Core features rule 47`
- [ ] `C-CF-125` `capability` `View All Projects` opens the project grid. `src: Core features rule 48`
- [ ] `C-CF-126` `ui` The grid shows published case files as tiles two across with the project name under the poster. `src: Core features rule 49`
- [ ] `C-CF-127` `ui` The grid lists `All` before the seven sector labels, unselected sectors dimmed. `src: Core features rule 49`
- [ ] `C-CF-128` `literal` The sector labels are `Technology & Futures`, `Climate & Startups`, `Fashion & Beauty`, `Chain`, `Entertainment & Culture`, `Automotive`, `Collaborations`. `src: Core features rule 49`
- [ ] `C-CF-129` `ui` Choosing a sector restacks the tiles in a ripple without reloading. `src: Core features rule 50`
- [ ] `C-CF-130` `capability` A chosen sector sets the address to `/work/all?sector=<token>`. `src: Core features rule 50`
- [ ] `C-CF-131` `ui` Pointing at a tile lifts the tile poster toward the viewer. `src: Core features rule 51`
- [ ] `C-CF-132` `ui` An empty sector shows the pinned empty-grid lines with `SEE ALL WORK`. `src: Core features rule 52`
- [ ] `C-CF-133` `capability` `SEE ALL WORK` returns the grid to `All`. `src: Core features rule 52`
- [ ] `C-CF-134` `capability` `Close All Projects` returns to the carousel. `src: Core features rule 53`
- [ ] `C-CF-135` `ui` A case file page shows the header, the chapters, the footer, the next case file preview. `src: Core features rule 54`
- [ ] `C-CF-136` `ui` A case file header shows the launch address under `LAUNCHED AT`. `src: Core features rule 54`
- [ ] `C-CF-137` `capability` The public case file carries the next case file in grid order. `src: Core features rule 54`
- [ ] `C-CF-138` `literal` Chapter kinds are `headline`, `text`, `list`, `image`, `video`, `video_loop`, `device`, `split`. `src: Core features rule 55`
- [ ] `C-CF-139` `ui` A text chapter shows a short label column beside a column of writing. `src: Core features rule 55`
- [ ] `C-CF-140` `ui` A video chapter shows a poster with a round play control. `src: Core features rule 55`
- [ ] `C-CF-141` `ui` A device chapter screen scrolls by drag inside the frame. `src: Core features rule 55`
- [ ] `C-CF-142` `ui` Split chapter images never stretch at any handle position. `src: Core features rule 56`
- [ ] `C-CF-143` `ui` Pressing the split handle shrinks the handle with the arrow mark hidden. `src: Core features rule 56`
- [ ] `C-CF-144` `ui` An expand control fills the window with the chapter media. `src: Core features rule 57`
- [ ] `C-CF-145` `ui` An image chapter with no upload shows a gradient placeholder carrying the client name. `src: Core features rule 58`
- [ ] `C-CF-146` `capability` An image chapter stores an `alt` used as the image text alternative. `src: Core features rule 59`
- [ ] `C-CF-147` `ui` Footer awards align along the bottom edge. `src: Core features rule 60`
- [ ] `C-CF-148` `ui` The owning author sees the edit control on the own published case file. `src: Core features rule 61`
- [ ] `C-CF-149` `ui` The reel layer shows a poster with a dark play control labelled `Showreel`. `src: Core features rule 62`
- [ ] `C-CF-150` `ui` Playing the reel fades the poster with the transport rising into view. `src: Core features rule 62`
- [ ] `C-CF-151` `capability` `Close Showreel` closes the reel layer. `src: Core features rule 62`
- [ ] `C-CF-152` `ui` A reel with no film shows `No reel yet.` with `SEE THE WORK`. `src: Core features rule 63`
- [ ] `C-CF-153` `ui` The contact surface shows `Contact` beside `newwork@kelo.example.com` over `careers.kelo.example`. `src: Core features rule 64`
- [ ] `C-CF-154` `literal` The offices are `HARBOURSIDE` on `+00 1 234 5670`, `NORTHGATE` on `+00 2 345 6780`. `src: Core features rule 64`
- [ ] `C-CF-155` `literal` The HARBOURSIDE lines are `12 Quay Street`, `Harbourside Works`, `Floor 3`, `HS1 4QA`. `src: Core features rule 64`
- [ ] `C-CF-156` `literal` The NORTHGATE lines are `40 North Row`, `NG2 7LT`. `src: Core features rule 64`
- [ ] `C-CF-157` `literal` The social lines under `SOCIAL` are `Directory`, `Pictures`, `Feed`. `src: Core features rule 64`
- [ ] `C-CF-158` `ui` The enquiry form sits above the newsletter strip under the pinned enquiry heading. `src: Core features rule 65`
- [ ] `C-CF-159` `literal` The enquiry fields are `name`, `email`, `organisation`, `budget`, `brief`, `sector`, `consent`. `src: Core features rule 65`
- [ ] `C-CF-160` `constraint` The enquiry `name` needs 2 to 80 characters. `src: Core features rule 65`
- [ ] `C-CF-161` `constraint` The enquiry `email` needs one at sign followed by a dot. `src: Core features rule 65`
- [ ] `C-CF-162` `constraint` The enquiry `organisation` allows at most 120 characters. `src: Core features rule 65`
- [ ] `C-CF-163` `capability` The enquiry `budget` offers five bands in thousands. `src: Core features rule 65`
- [ ] `C-CF-164` `constraint` The enquiry `brief` needs 40 to 4000 characters. `src: Core features rule 65`
- [ ] `C-CF-165` `constraint` The enquiry `consent` is required. `src: Core features rule 65`
- [ ] `C-CF-166` `capability` A valid enquiry is stored with state `new`. `src: Core features rule 66`
- [ ] `C-CF-167` `ui` A valid enquiry replaces the form with `Thank you.` over the two working day line. `src: Core features rule 66`
- [ ] `C-CF-168` `capability` An enquiry from a verified signed-in visitor is attributed to the account. `src: Core features rule 66`
- [ ] `C-CF-169` `capability` Any other enquiry is stored unattributed. `src: Core features rule 66`
- [ ] `C-CF-170` `ui` `DISPATCH` turns the newsletter strip into one line of form in place. `src: Core features rule 67`
- [ ] `C-CF-171` `capability` A valid newsletter address is stored once. `src: Core features rule 67`
- [ ] `C-CF-172` `literal` The newsletter success copy reads `Thanks! You are now subscribed.`. `src: Core features rule 67`
- [ ] `C-CF-173` `constraint` A repeated newsletter address creates no second row. `src: Core features rule 67`
- [ ] `C-CF-174` `capability` `PRIVACY` opens the notice page over the contact layer. `src: Core features rule 67`
- [ ] `C-CF-175` `capability` `Close Contact` returns to the home screen. `src: Core features rule 68`
- [ ] `C-CF-176` `ui` The notice page shows the title `Kelo Customer Privacy Notice` above the pinned description. `src: Core features rule 69`
- [ ] `C-CF-177` `literal` The notice contact strip carries `EMAIL` with `privacy@kelo.example.com`, `ADDRESS, ONE`, `ADDRESS, TWO`. `src: Core features rule 69`
- [ ] `C-CF-178` `literal` The fourteen notice rows carry the pinned labels in order, the body copy UNPINNED. `src: Core features rule 70`
- [ ] `C-CF-179` `capability` The first notice row states what the studio stores about a visitor. `src: Core features rule 70`
- [ ] `C-CF-180` `ui` The notice copy is set near headline size with very large gaps between rows. `src: Core features rule 71`
- [ ] `C-CF-181` `ui` The operative phrase of a notice paragraph shows in the warm sand colour. `src: Core features rule 71`
- [ ] `C-CF-182` `ui` A notice link turns warm sand on hover. `src: Core features rule 71`
- [ ] `C-CF-183` `capability` An editor edits a notice row through `PATCH /api/studio/notice-rows/{id}`. `src: Core features rule 72`
- [ ] `C-CF-184` `constraint` A saved notice body keeps only `p`, `ul`, `li`, `a`, `em` elements. `src: Core features rule 72`
- [ ] `C-CF-185` `constraint` A saved notice body drops every attribute other than a link `href`. `src: Core features rule 72`
- [ ] `C-CF-186` `constraint` A notice link outside `https:` or `mailto:` is dropped with the link text kept. `src: Core features rule 72`
- [ ] `C-CF-187` `capability` `Close Notice` returns to the contact layer. `src: Core features rule 72`
- [ ] `C-CF-188` `capability` A case file address opened in a fresh browser opens the named case file. `src: Core features rule 73`
- [ ] `C-CF-189` `capability` The browser back control closes the open layer instead of leaving the site. `src: Core features rule 73`
- [ ] `C-CF-190` `capability` Every public surface is reachable in at most three actions from the home screen. `src: Core features rule 73`
- [ ] `C-CF-191` `capability` Tab on the home screen moves through `Discover`, `Showreel`, `Audio`, `Drop` in order. `src: Core features rule 74`
- [ ] `C-CF-192` `capability` The `R` key reseeds the crystal. `src: Core features rule 74`
- [ ] `C-CF-193` `capability` Escape closes the topmost open layer. `src: Core features rule 74`
- [ ] `C-CF-194` `ui` The console keeps the near-black ground with the crystal turning behind. `src: Core features rule 75`
- [ ] `C-CF-195` `ui` The console shows no save button anywhere. `src: Core features rule 75`
- [ ] `C-CF-196` `ui` The case file list shows grid position, title, client, sector, state, last update per row. `src: Core features rule 76`
- [ ] `C-CF-197` `ui` A list row owned by another person shows a dimmed title that is not a link. `src: Core features rule 76`
- [ ] `C-CF-198` `capability` An author's case file list returns every case file row. `src: Core features rule 76`
- [ ] `C-CF-199` `ui` The case file list offers a state filter, a sector filter, a search field, `NEW CASE FILE`. `src: Core features rule 76`
- [ ] `C-CF-200` `ui` The editor shows the chapter list on the left beside the chosen chapter fields. `src: Core features rule 77`
- [ ] `C-CF-201` `ui` The editor holds the header, chapters, footer, publication blocks. `src: Core features rule 77`
- [ ] `C-CF-202` `ui` An editor sees who wrote the case file with the last touch time. `src: Core features rule 77`
- [ ] `C-CF-203` `ui` A console field saves when left, with `SAVED` in the bar. `src: Core features rule 78`
- [ ] `C-CF-204` `capability` The chapter arranger saves a new order as one request carrying the complete list. `src: Core features rule 79`
- [ ] `C-CF-205` `ui` The review queue lists submitted case files with `APPROVE` beside `RETURN` per row. `src: Core features rule 80`
- [ ] `C-CF-206` `constraint` A return note outside 10 to 500 characters is refused with `Say what needs changing.`. `src: Core features rule 80`
- [ ] `C-CF-207` `capability` Dragging a tile out of the grid arranger takes the case file down. `src: Core features rule 81`
- [ ] `C-CF-208` `capability` The inbox lists enquiries newest first. `src: Core features rule 82`
- [ ] `C-CF-209` `ui` Unread inbox rows show at full strength with read rows dimmed. `src: Core features rule 82`
- [ ] `C-CF-210` `capability` An editor marks an enquiry read. `src: Core features rule 82`
- [ ] `C-CF-211` `capability` An editor assigns an enquiry. `src: Core features rule 82`
- [ ] `C-CF-212` `capability` A reply is stored on the enquiry with state `answered`. `src: Core features rule 82`
- [ ] `C-CF-213` `capability` A reply is shown to the attributed sender under the sender's own account. `src: Core features rule 82`
- [ ] `C-CF-214` `constraint` An unattributed enquiry cannot be replied to in the app. `src: Core features rule 82`
- [ ] `C-CF-215` `capability` The outbox lists every stored message newest first. `src: Core features rule 83`
- [ ] `C-CF-216` `ui` The site settings surface holds the sector taxonomy, the client roster, the notice rows, the export. `src: Core features rule 83`
- [ ] `C-CF-217` `capability` The account surface lists the live sessions, each one revocable. `src: Core features rule 84`
- [ ] `C-CF-218` `capability` A visitor's account surface lists own enquiries with any reply. `src: Core features rule 84`
- [ ] `C-CF-219` `capability` A second person in the case file shows a pinned presence line naming that person. `src: Core features rule 85`
- [ ] `C-CF-220` `constraint` A save to a field another person holds is refused as a conflict. `src: Core features rule 85`
- [ ] `C-CF-221` `capability` The case file carries `presence` listing the other people with the field each holds. `src: Core features rule 85`
- [ ] `C-CF-222` `capability` Releasing a field frees the hold for others. `src: Core features rule 85`
- [ ] `C-CF-223` `data` A case file state is one of `draft`, `submitted`, `changes_requested`, `approved`, `published`. `src: Core features rule 86`
- [ ] `C-CF-224` `capability` A state move is made through `POST /api/studio/case-files/{id}/transitions` naming `to`. `src: Core features rule 86`
- [ ] `C-CF-225` `role` The owner or an editor moves `draft` to `submitted`. `src: Core features rule 86`
- [ ] `C-CF-226` `role` Only an editor other than the owner moves `submitted` to `changes_requested`. `src: Core features rule 86`
- [ ] `C-CF-227` `role` Only an editor other than the owner moves `submitted` to `approved`. `src: Core features rule 86`
- [ ] `C-CF-228` `role` The owner moves `changes_requested` back to `submitted`. `src: Core features rule 86`
- [ ] `C-CF-229` `role` Only an editor moves `approved` to `published`. `src: Core features rule 86`
- [ ] `C-CF-230` `role` Only an editor moves `approved` back to `draft`. `src: Core features rule 86`
- [ ] `C-CF-231` `role` Only an editor moves `published` back to `approved`. `src: Core features rule 86`
- [ ] `C-CF-232` `constraint` A move outside the allowed set is refused with the state unchanged. `src: Core features rule 86`
- [ ] `C-CF-233` `capability` `NEW CASE FILE` creates a `draft` titled `Untitled` owned by the caller. `src: Core features rule 87`
- [ ] `C-CF-234` `data` A new case file carries no slug, no chapters, no sector. `src: Core features rule 87`
- [ ] `C-CF-235` `constraint` A title save outside 2 to 80 characters is refused with the pinned title message. `src: Core features rule 88`
- [ ] `C-CF-236` `constraint` A client save outside 1 to 60 characters is refused with the pinned client message. `src: Core features rule 88`
- [ ] `C-CF-237` `literal` A sector outside the seven is refused with `Pick a sector.`. `src: Core features rule 88`
- [ ] `C-CF-238` `literal` A description outside 40 to 400 characters is refused with `The description needs to be at least forty characters.`. `src: Core features rule 88`
- [ ] `C-CF-239` `literal` A launch address without `https` is refused with `That launch address does not look right.`. `src: Core features rule 88`
- [ ] `C-CF-240` `constraint` A case file holds at most six information items. `src: Core features rule 88`
- [ ] `C-CF-241` `constraint` An information heading holds 1 to 24 characters. `src: Core features rule 88`
- [ ] `C-CF-242` `literal` An award mark is one of `treatment-1` to `treatment-8`. `src: Core features rule 88`
- [ ] `C-CF-243` `constraint` A save carrying an invalid value writes nothing. `src: Core features rule 88`
- [ ] `C-CF-244` `capability` The first non-empty title save derives the slug by lowercasing with hyphens between words. `src: Core features rule 89`
- [ ] `C-CF-245` `literal` The title `The Long Room` derives the slug `the-long-room`. `src: Core features rule 89`
- [ ] `C-CF-246` `literal` A clashing slug gains `-2` to become unique. `src: Core features rule 89`
- [ ] `C-CF-247` `constraint` The slug stays fixed when the title changes. `src: Core features rule 89`
- [ ] `C-CF-248` `capability` An editor changes a slug exactly once. `src: Core features rule 89`
- [ ] `C-CF-249` `capability` A changed slug makes the old public address answer a permanent redirect. `src: Core features rule 89`
- [ ] `C-CF-250` `constraint` An issued slug is never issued again after deletion. `src: Core features rule 89`
- [ ] `C-CF-251` `capability` A new chapter is added at the end of the list. `src: Core features rule 90`
- [ ] `C-CF-252` `data` A chapter stores `position`, `kind`, `payload`. `src: Core features rule 90`
- [ ] `C-CF-253` `constraint` An unknown chapter kind is refused. `src: Core features rule 90`
- [ ] `C-CF-254` `capability` A chapter may be saved unfinished. `src: Core features rule 90`
- [ ] `C-CF-255` `data` Each chapter kind has the pinned finished rule for its payload fields. `src: Core features rule 90`
- [ ] `C-CF-256` `capability` The chapter-order request rewrites every position from the complete list. `src: Core features rule 91`
- [ ] `C-CF-257` `constraint` An incomplete, repeated or foreign chapter list is refused with no position changed. `src: Core features rule 91`
- [ ] `C-CF-258` `constraint` A submit moves nothing when any gate fails. `src: Core features rule 92`
- [ ] `C-CF-259` `capability` A refused submit names every failed gate under `fields`. `src: Core features rule 92`
- [ ] `C-CF-260` `ui` The console lists each submit failure by number. `src: Core features rule 92`
- [ ] `C-CF-261` `capability` A submit of an `Untitled` case file fails under `title`. `src: Core features rule 92`
- [ ] `C-CF-262` `literal` A submit with no chapter fails under `chapters` with `A case file needs at least one chapter.`. `src: Core features rule 92`
- [ ] `C-CF-263` `capability` A submit with an unfinished chapter fails under `chapter_payloads` naming the chapter position. `src: Core features rule 92`
- [ ] `C-CF-264` `capability` A submit with an information item missing a value fails under `information_items`. `src: Core features rule 92`
- [ ] `C-CF-265` `capability` A successful submit sets `submitted` recording `submitted_at`. `src: Core features rule 93`
- [ ] `C-CF-266` `ui` A successful submit shows `SENT FOR REVIEW`. `src: Core features rule 93`
- [ ] `C-CF-267` `constraint` An author edit of a `submitted` case file is refused with nothing changed. `src: Core features rule 93`
- [ ] `C-CF-268` `ui` The submit control reads `WITH THE EDITOR` for a submitted case file. `src: Core features rule 93`
- [ ] `C-CF-269` `constraint` A submitted case file cannot be submitted again. `src: Core features rule 93`
- [ ] `C-CF-270` `capability` `RETURN` sets `changes_requested` storing the note as `return_note`. `src: Core features rule 94`
- [ ] `C-CF-271` `capability` A returned case file accepts author edits again. `src: Core features rule 94`
- [ ] `C-CF-272` `ui` The return note is pinned above the header under a warm sand label. `src: Core features rule 94`
- [ ] `C-CF-273` `capability` `APPROVE` sets `approved` recording `reviewed_by`. `src: Core features rule 95`
- [ ] `C-CF-274` `capability` Acting on a case file no longer submitted is refused as a conflict naming who moved the case file. `src: Core features rule 95`
- [ ] `C-CF-275` `constraint` Two simultaneous approvals of one case file admit exactly one approval. `src: Core features rule 95`
- [ ] `C-CF-276` `capability` `PUBLISH` sets `published` at the end of the grid order. `src: Core features rule 96`
- [ ] `C-CF-277` `ui` A publish shows `LIVE`. `src: Core features rule 96`
- [ ] `C-CF-278` `capability` A published case file appears in the public list at once. `src: Core features rule 96`
- [ ] `C-CF-279` `capability` A content change to a published case file is written to `draft_payload`. `src: Core features rule 97`
- [ ] `C-CF-280` `constraint` The public address keeps serving published content whenever a pending copy exists. `src: Core features rule 97`
- [ ] `C-CF-281` `capability` `PUBLISH CHANGES` copies the pending copy over the live content. `src: Core features rule 98`
- [ ] `C-CF-282` `capability` `PUBLISH CHANGES` clears `draft_payload`. `src: Core features rule 98`
- [ ] `C-CF-283` `constraint` `PUBLISH CHANGES` leaves `published_at` unchanged. `src: Core features rule 98`
- [ ] `C-CF-284` `role` The owning author publishes changes without a second review. `src: Core features rule 98`
- [ ] `C-CF-285` `role` An author cannot publish changes to another person's case file. `src: Core features rule 98`
- [ ] `C-CF-286` `capability` A fresh client sees the new content on the next request after changes are published. `src: Core features rule 98`
- [ ] `C-CF-287` `constraint` A case file that was ever published cannot be deleted. `src: Core features rule 99`
- [ ] `C-CF-288` `capability` Taking a case file down clears the grid position. `src: Core features rule 99`
- [ ] `C-CF-289` `capability` A taken-down case file can be published again. `src: Core features rule 99`
- [ ] `C-CF-290` `ui` Unpublishing the only case file of a sector leaves that sector on the empty grid state. `src: Core features rule 100`
- [ ] `C-CF-291` `constraint` A write carrying a stale `version` is refused as a version conflict. `src: Core features rule 101`
- [ ] `C-CF-292` `data` A case file `version` increases on every write. `src: Core features rule 101`
- [ ] `C-CF-293` `contract` Every form control carries the field name as the `name` attribute. `src: Core features rule 102`
- [ ] `C-CF-294` `capability` Every form rejects invalid input inline under the field concerned. `src: Core features rule 102`
- [ ] `C-CF-295` `constraint` A form rejected for invalid input writes nothing. `src: Core features rule 102`
- [ ] `C-CF-296` `literal` An empty enquiry name shows `We need a name to reply to.`. `src: Core features rule 102`
- [ ] `C-CF-297` `literal` A malformed enquiry address shows `That address does not look right.`. `src: Core features rule 102`
- [ ] `C-CF-298` `literal` A short enquiry brief shows `Tell us a little more, forty characters at least.`. `src: Core features rule 102`
- [ ] `C-CF-299` `capability` An unticked consent shows the pinned consent message. `src: Core features rule 102`
- [ ] `C-CF-300` `ui` Validation never runs on a keystroke. `src: Core features rule 103`
- [ ] `C-CF-301` `ui` A field validates on leaving once the field was left non-empty. `src: Core features rule 103`
- [ ] `C-CF-302` `ui` Submitting moves focus to the first invalid field. `src: Core features rule 103`
- [ ] `C-CF-303` `contract` The server refuses an invalid request naming each field with a message. `src: Core features rule 103`
- [ ] `C-CF-304` `ui` The submit control is never disabled for an incomplete form. `src: Core features rule 104`
- [ ] `C-CF-305` `ui` A pending submit shows the turning ring with the fields still editable. `src: Core features rule 105`
- [ ] `C-CF-306` `ui` A field-level rejection marks the fields warm sand with every value kept. `src: Core features rule 107`
- [ ] `C-CF-307` `data` The unsent enquiry is kept in browser storage under `enquiry_draft`. `src: Core features rule 108`
- [ ] `C-CF-308` `capability` A reload restores the values of an unsent enquiry. `src: Core features rule 108`
- [ ] `C-CF-309` `capability` A successful enquiry clears the kept draft. `src: Core features rule 108`
- [ ] `C-CF-310` `ui` Every surface offers loading, empty, error, offline faces from four shared layouts. `src: Core features rule 109`
- [ ] `C-CF-311` `ui` No status code is ever shown on a surface. `src: Core features rule 109`
- [ ] `C-CF-312` `ui` A skeleton shows plain blocks with no shimmer or pulse. `src: Core features rule 109`
- [ ] `C-CF-313` `ui` Each surface shows the pinned state copy for the state reached. `src: Core features rule 110`
- [ ] `C-CF-314` `capability` Moving between loaded surfaces keeps working offline with the bar reading `OFFLINE`. `src: Core features rule 111`
- [ ] `C-CF-315` `capability` Every filter parameter lives in the address. `src: Core features rule 113`
- [ ] `C-CF-316` `capability` A filter change replaces the history entry. `src: Core features rule 113`
- [ ] `C-CF-317` `constraint` The public grid takes no free-text parameter. `src: Core features rule 114`
- [ ] `C-CF-318` `capability` An unknown sector token on the public list is refused as invalid. `src: Core features rule 114`
- [ ] `C-CF-319` `capability` Combined console filters intersect. `src: Core features rule 115`
- [ ] `C-CF-320` `ui` A filter combination with no results offers `CLEAR FILTERS`. `src: Core features rule 115`
- [ ] `C-CF-321` `capability` Console free text matches case file titles. `src: Core features rule 116`
- [ ] `C-CF-322` `capability` Console free text matches case file clients. `src: Core features rule 116`
- [ ] `C-CF-323` `capability` Inbox free text matches enquiry names, organisations, briefs. `src: Core features rule 116`
- [ ] `C-CF-324` `capability` Free text ignores letter case. `src: Core features rule 116`
- [ ] `C-CF-325` `capability` Free text ignores accents. `src: Core features rule 116`
- [ ] `C-CF-326` `capability` A title-beginning match ranks above a client match. `src: Core features rule 116`
- [ ] `C-CF-327` `capability` Free text under 2 characters is ignored. `src: Core features rule 116`
- [ ] `C-CF-328` `ui` The matched run of a search is highlighted warm sand. `src: Core features rule 116`
- [ ] `C-CF-329` `capability` `sort=order` returns the grid position ascending. `src: Core features rule 117`
- [ ] `C-CF-330` `capability` `sort=title` returns case files alphabetically ignoring accents. `src: Core features rule 117`
- [ ] `C-CF-331` `capability` `sort=newest` on the public list returns publication time descending. `src: Core features rule 117`
- [ ] `C-CF-332` `constraint` The public site opens no live connection. `src: Core features rule 118`
- [ ] `C-CF-333` `capability` A newly submitted case file appears in an open review queue within 5 seconds without a reload. `src: Core features rule 118`
- [ ] `C-CF-334` `capability` A new enquiry appears in an open inbox within 5 seconds with `NEW ENQUIRY`. `src: Core features rule 118`
- [ ] `C-CF-335` `ui` A shortlist change appears at once before the server confirms. `src: Core features rule 119`
- [ ] `C-CF-336` `constraint` An ordering is replaced whole or not at all. `src: Core features rule 121`
- [ ] `C-CF-337` `ui` Messages appear only in the bar, inline notices, pinned notes. `src: Core features rule 122`
- [ ] `C-CF-338` `capability` Each message is stored once per event, addressed to an email address. `src: Core features rule 123`
- [ ] `C-CF-339` `capability` An account reads the messages addressed to the account at `GET /api/messages`. `src: Core features rule 123`
- [ ] `C-CF-340` `capability` An editor reads every message at `GET /api/studio/outbox`. `src: Core features rule 123`
- [ ] `C-CF-341` `constraint` A message subject stays under 60 characters. `src: Core features rule 123`
- [ ] `C-CF-342` `constraint` A message carries at most one link. `src: Core features rule 123`
- [ ] `C-CF-343` `capability` A confirmation message links to the address confirmation route stating 7 days. `src: Core features rule 123`
- [ ] `C-CF-344` `literal` A return writes `<title> needs changes` to the author carrying the note verbatim. `src: Core features rule 123`
- [ ] `C-CF-345` `literal` A first publication writes `<title> is live` to the author. `src: Core features rule 123`
- [ ] `C-CF-346` `constraint` Publishing changes writes no message. `src: Core features rule 123`
- [ ] `C-CF-347` `literal` An enquiry writes `We got your message` to the sender. `src: Core features rule 123`
- [ ] `C-CF-348` `literal` An enquiry writes `Enquiry from <name>` to every editor. `src: Core features rule 123`
- [ ] `C-CF-349` `capability` The editors' enquiry message carries every enquiry field with one link to `/studio/enquiries`. `src: Core features rule 123`
- [ ] `C-CF-350` `constraint` The editors' enquiry message writes a web address separator `://` as `[:]//`. `src: Core features rule 123`
- [ ] `C-CF-351` `constraint` No message contains a password or a session token. `src: Core features rule 124`
- [ ] `C-CF-352` `capability` Every message names the studio with `newwork@kelo.example.com`. `src: Core features rule 124`
- [ ] `C-CF-353` `constraint` A saved field writes no message. `src: Core features rule 124`
- [ ] `C-CF-354` `data` A signed-out shortlist lives in browser storage under `shortlist`. `src: Core features rule 125`
- [ ] `C-CF-355` `capability` A verified visitor adds a case file to the server shortlist with a repeatable `PUT`. `src: Core features rule 125`
- [ ] `C-CF-356` `capability` A verified visitor removes a case file from the shortlist with a repeatable `DELETE`. `src: Core features rule 125`
- [ ] `C-CF-357` `constraint` Only a published case file can be shortlisted. `src: Core features rule 125`
- [ ] `C-CF-358` `constraint` An unconfirmed visitor's server shortlist write is refused. `src: Core features rule 125`
- [ ] `C-CF-359` `capability` Signing in merges the local shortlist into the server shortlist as a union. `src: Core features rule 126`
- [ ] `C-CF-360` `constraint` A duplicate entry in the merge causes no error. `src: Core features rule 126`
- [ ] `C-CF-361` `capability` A private window with storage blocked shows the wordmark with no error. `src: Core features rule 127`
- [ ] `C-CF-362` `data` The locale is kept under `locale`. `src: Core features rule 127`
- [ ] `C-CF-363` `data` A first run seeds three published example case files at grid positions one to three. `src: Core features rule 128`
- [ ] `C-CF-364` `capability` An editor is offered `REMOVE THE EXAMPLES` whenever the seeded examples exist. `src: Core features rule 128`
- [ ] `C-CF-365` `capability` `REMOVE THE EXAMPLES` deletes the three seeded examples with the example chapters. `src: Core features rule 128`
- [ ] `C-CF-366` `ui` A delete control arms as `REALLY?` in bright yellow for 4 seconds. `src: Core features rule 129`
- [ ] `C-CF-367` `capability` An editor deletes a never-published case file with the case file chapters. `src: Core features rule 129`
- [ ] `C-CF-368` `constraint` Deleting an account needs `confirm_display_name` matching the display name. `src: Core features rule 129`
- [ ] `C-CF-369` `capability` Deleting an account moves the owned case files to the deleting editor. `src: Core features rule 129`
- [ ] `C-CF-370` `capability` A moved case file records the original author name. `src: Core features rule 129`
- [ ] `C-CF-371` `ui` The bright yellow appears only during an armed delete. `src: Core features rule 130`
- [ ] `C-CF-372` `constraint` Deleting a sector in use is refused. `src: Core features rule 131`
- [ ] `C-CF-373` `capability` An editor exports every entity as one document at `GET /api/studio/export`. `src: Core features rule 131`
- [ ] `C-CF-374` `capability` The document declares English as the source locale. `src: Core features rule 132`
- [ ] `C-CF-375` `ui` A locale control sits at the foot of the menu layer. `src: Core features rule 132`
- [ ] `C-CF-376` `ui` An absolute date reads day, month name, year. `src: Core features rule 133`
- [ ] `C-CF-377` `ui` A recent update reads as a relative time such as `12 minutes ago`. `src: Core features rule 133`
- [ ] `C-CF-378` `contract` The server document for every public address carries a `<title>` before scripts run. `src: Core features rule 136`
- [ ] `C-CF-379` `contract` The server document for every public address carries `og:title` with `og:image`. `src: Core features rule 136`
- [ ] `C-CF-380` `contract` Every `og:image` resolves on the app origin to a generated image. `src: Core features rule 136`
- [ ] `C-CF-381` `literal` A case file preview image lives at `/api/preview/<case-file-slug>.png`. `src: Core features rule 136`
- [ ] `C-CF-382` `literal` Other public addresses use `/api/preview/site.png`. `src: Core features rule 136`
- [ ] `C-CF-383` `literal` A case file `og:title` ends with ` · Kelo`. `src: Core features rule 136`
- [ ] `C-CF-384` `ui` An empty shortlist shows `Nothing saved.` over the pinned invitation line with `SEE ALL WORK`. `src: Core features rule 110`
- [ ] `C-CF-385` `ui` An empty chapter arranger shows `No chapters yet.` over `Add something to arrange.` with `BACK TO THE EDITOR`. `src: Core features rule 110`
- [ ] `C-CF-386` `ui` An empty case file list shows `Nothing yet.` over the pinned starting line with `NEW CASE FILE`. `src: Core features rule 110`
- [ ] `C-CF-387` `capability` The bar reads `BACK ONLINE` when the connection returns. `src: Core features rule 111`
- [ ] `C-CF-388` `capability` An offline contact surface replaces the enquiry form with the pinned saved-here notice. `src: Core features rule 110`
- [ ] `C-CF-389` `capability` An offline studio story replaces its rows with the pinned offline face. `src: Core features rule 110`
- [ ] `C-CF-390` `ui` An empty enquiry inbox shows `No enquiries.` over the pinned waiting line with `SEE THE CONTACT PAGE`. `src: Core features rule 110`

## C-UF User flow

- [ ] `C-UF-01` `literal` The public routes are `/`, `/story`, `/work`, `/work/all`, `/work/<case-file-slug>`, `/reel`, `/contact`, `/notice`. `src: User flow route table`
- [ ] `C-UF-02` `literal` The account routes are `/join`, `/invite`, `/reset`, `/shortlist`. `src: User flow route table`
- [ ] `C-UF-03` `literal` The studio routes are `/studio/sign-in`, `/studio`, `/studio/review`, `/studio/grid`, `/studio/enquiries`, `/studio/outbox`, `/studio/site`, `/studio/account`. `src: User flow route table`
- [ ] `C-UF-04` `literal` The case file editor lives at `/studio/case/<case-file-id>`. `src: User flow route table`
- [ ] `C-UF-05` `capability` A signed-out studio address redirects to the sign-in layer with `next` set to the requested path. `src: User flow entry bullet 2`
- [ ] `C-UF-06` `literal` A signed-out `/studio` redirects to `/studio/sign-in?next=/studio`. `src: User flow entry bullet 2`
- [ ] `C-UF-07` `constraint` A `next` value is honoured only for a same-origin path starting with exactly one slash. `src: User flow entry bullet 2`
- [ ] `C-UF-08` `capability` A visitor on a studio surface other than the account sees the denied surface. `src: User flow entry bullet 3`
- [ ] `C-UF-09` `capability` An author on the review, grid, enquiries, outbox or site surface sees the denied surface. `src: User flow entry bullet 4`
- [ ] `C-UF-10` `ui` The denied surface shows `Not for you` over the pinned line with `BACK TO THE WORK`. `src: User flow entry bullet 5`
- [ ] `C-UF-11` `ui` An unknown or unpublished case file address shows `Not here.` with the address unchanged. `src: User flow entry bullet 6`
- [ ] `C-UF-12` `capability` After sign-in the `next` path opens. `src: User flow entry bullet 7`
- [ ] `C-UF-13` `capability` Sign-out returns to `/`. `src: User flow entry bullet 7`
- [ ] `C-UF-14` `capability` The public journey returns to `/` after `Close Story`. `src: User flow journey 1`
- [ ] `C-UF-15` `capability` The work journey reaches a case file through the filtered grid. `src: User flow journey 2`
- [ ] `C-UF-16` `capability` The browser back control from the filtered grid returns to `/work`. `src: User flow journey 2`
- [ ] `C-UF-17` `capability` `Close Notice` returns the contact journey to `/contact`. `src: User flow journey 3`
- [ ] `C-UF-18` `capability` The authoring journey takes a new case file from `Untitled` to `WITH THE EDITOR`. `src: User flow journey 4`
- [ ] `C-UF-19` `capability` The review journey returns, resubmits, approves, publishes a case file. `src: User flow journey 5`
- [ ] `C-UF-20` `capability` A fresh browser sees the rewritten description only after changes are published. `src: User flow journey 6`
- [ ] `C-UF-21` `capability` The editor inbox lists the enquiry sent on the contact surface with the sender name. `src: User flow journey 7`
- [ ] `C-UF-22` `capability` A taken-down case file address shows `Not here.` in a fresh browser. `src: User flow journey 8`
- [ ] `C-UF-23` `capability` Tab with Enter opens the menu, then the story, with Escape returning to `/`. `src: User flow journey 9`
- [ ] `C-UF-24` `capability` The enquiry form can be sent by keyboard alone. `src: User flow journey 9`
- [ ] `C-UF-25` `capability` A new visitor confirms the address from the confirmation message link. `src: User flow journey 10`
- [ ] `C-UF-26` `capability` A shortlisted case file appears at `/shortlist`. `src: User flow journey 10`
- [ ] `C-UF-27` `constraint` Errors never crash the app. `src: User flow states para`
- [ ] `C-UF-28` `capability` `/shortlist` shows the visitor's shortlist. `src: User flow route table`
- [ ] `C-UF-29` `role` `/studio/case/<case-file-id>` opens only for the owning author or an editor. `src: User flow route table`
- [ ] `C-UF-30` `role` The review, grid, enquiries, outbox, site surfaces open only for an editor. `src: User flow route table`
- [ ] `C-UF-31` `capability` `/studio/account` opens for any signed-in account. `src: User flow route table`
- [ ] `C-UF-32` `ui` The sign-in layer heading reads `Studio`. `src: User flow route table`
- [ ] `C-UF-33` `ui` A gated surface resolves who is asking before the first paint. `src: User flow entry bullet 1`
- [ ] `C-UF-34` `capability` An author on `/studio` sees the case file list. `src: User flow entry bullet 4`
- [ ] `C-UF-35` `capability` A studio account signing in with no `next` lands on `/studio`. `src: User flow entry bullet 7`
- [ ] `C-UF-36` `capability` A visitor signing in with no `next` lands on `/`. `src: User flow entry bullet 7`
- [ ] `C-UF-37` `capability` Pasting `/work/glass-harbour` into a fresh browser opens `Glass Harbour` with no arrival sequence. `src: User flow journey 2`
- [ ] `C-UF-38` `capability` An image chapter accepts a picture uploaded from the editor. `src: User flow journey 4`
- [ ] `C-UF-39` `ui` A returned case file leaves the review queue with other submitted rows still listed. `src: User flow journey 5`
- [ ] `C-UF-40` `ui` Taking a case file down from the grid arranger shows `TAKEN DOWN`. `src: User flow journey 8`
- [ ] `C-UF-41` `capability` With the network off the bar reads `OFFLINE`, with loaded surfaces still opening. `src: User flow states para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The public site reads editorial, with the subject seen first over almost no interface. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The console reads quiet, dense, organised. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The product ships one fully designed dark mode with no light theme. `src: UI/UX notes para 2`
- [ ] `C-UX-04` `ui` The page ground is a near-black neutral with the crystal layer a warmer near-black, the seam invisible, the two shades UNPINNED. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` Near-black grounds lighten the further a surface sits from the page. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` Section rules are a deep neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` Most type is near-white with secondary copy in a mid neutral. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` The warm sand is the only warm colour in the product. `src: UI/UX notes para 3`
- [ ] `C-UX-09` `ui` On the public site the warm sand appears only inside the privacy notice. `src: UI/UX notes para 3`
- [ ] `C-UX-10` `ui` In the forms or the console the warm sand marks what needs attention. `src: UI/UX notes para 3`
- [ ] `C-UX-11` `ui` Meaning never depends on colour alone. `src: UI/UX notes para 3`
- [ ] `C-UX-12` `literal` The product font is `Inter` with the fallback `Arial, sans-serif`. `src: UI/UX notes para 4`
- [ ] `C-UX-13` `ui` Display text uses an extralight cut with reading text in a light cut. `src: UI/UX notes para 4`
- [ ] `C-UX-14` `ui` The menu words with the carousel titles are set at 65px. `src: Front-end specification type`
- [ ] `C-UX-15` `literal` The wordmark is set at `48px`. `src: Front-end specification type`
- [ ] `C-UX-16` `ui` The register changes by stroke thickness with size, never by colour. `src: UI/UX notes para 4`
- [ ] `C-UX-17` `ui` Labels are small spaced capitals, with menu words in sentence case. `src: UI/UX notes para 4`
- [ ] `C-UX-18` `ui` No card, panel or border appears on the public surfaces. `src: UI/UX notes para 5`
- [ ] `C-UX-19` `ui` Only round controls carry rounded corners. `src: UI/UX notes para 5`
- [ ] `C-UX-20` `ui` A large gap with a thin rule marks the start of a new thought. `src: UI/UX notes para 5`
- [ ] `C-UX-21` `ui` A link shows a faint underline with a bright underline drawn across on pointing. `src: UI/UX notes para 5`
- [ ] `C-UX-22` `ui` Every control has distinct resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes para 6`
- [ ] `C-UX-23` `ui` Each surface leads with one primary action, distinct from every secondary action. `src: UI/UX notes para 6`
- [ ] `C-UX-24` `ui` `SEND` is the primary action on the contact surface. `src: UI/UX notes para 6`
- [ ] `C-UX-25` `ui` Everything moves at one of three speeds, each duration UNPINNED. `src: UI/UX notes para 7`
- [ ] `C-UX-26` `ui` Nothing drifts, pulses or loops on its own except the crystal. `src: UI/UX notes para 7`
- [ ] `C-UX-27` `ui` Surfaces fade into place instead of sliding in from the edges. `src: UI/UX notes para 7`
- [ ] `C-UX-28` `ui` Under reduced motion every moment resolves to a legible end state with the crystal held still. `src: UI/UX notes para 7`
- [ ] `C-UX-29` `ui` Body text meets WCAG AA contrast against the page ground. `src: UI/UX notes para 8`
- [ ] `C-UX-30` `ui` Interactive targets measure at least 44px in each direction. `src: UI/UX notes para 8`
- [ ] `C-UX-31` `ui` Keyboard focus is visible on every control. `src: UI/UX notes para 8`
- [ ] `C-UX-32` `ui` Every icon-only control has a text label. `src: UI/UX notes para 8`
- [ ] `C-UX-33` `ui` Every surface has one first-level heading. `src: UI/UX notes para 8`
- [ ] `C-UX-34` `ui` Reading surfaces allow text selection. `src: UI/UX notes para 8`
- [ ] `C-UX-35` `ui` The layout adapts across five breakpoint tiers. `src: UI/UX notes para 9`
- [ ] `C-UX-36` `constraint` No surface scrolls sideways at a narrow viewport. `src: UI/UX notes para 9`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The front end is a Vue 3 application. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The server answers every public address with the one application document. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` Case file data persists in PostgreSQL at `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` Uploaded bytes persist in MinIO at `STORAGE_ENDPOINT` in `STORAGE_BUCKET`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `constraint` No credential or bucket secret appears in anything the browser downloads. `src: Technical requirements para 4`
- [ ] `C-TR-06` `contract` Every response carries `Strict-Transport-Security` with `includeSubDomains`. `src: Technical requirements security headers`
- [ ] `C-TR-07` `contract` Every response carries `X-Content-Type-Options: nosniff`. `src: Technical requirements security headers`
- [ ] `C-TR-08` `contract` Every response carries `X-Frame-Options: DENY`. `src: Technical requirements security headers`
- [ ] `C-TR-09` `contract` Every response carries `Referrer-Policy: same-origin`. `src: Technical requirements security headers`
- [ ] `C-TR-10` `contract` Every response carries a `Content-Security-Policy`. `src: Technical requirements security headers`
- [ ] `C-TR-11` `constraint` The content policy allows no inline script, no eval. `src: Technical requirements security headers`
- [ ] `C-TR-12` `constraint` The content policy denies framing with `frame-ancestors 'none'`. `src: Technical requirements security headers`
- [ ] `C-TR-13` `constraint` A request from another origin receives no cross-origin permission. `src: Technical requirements security headers`
- [ ] `C-TR-14` `constraint` Any app cookie is http-only with same-site strict. `src: Technical requirements security headers`
- [ ] `C-TR-15` `contract` A rate-limit refusal carries `retry_after` in seconds. `src: Technical requirements rate limits`
- [ ] `C-TR-16` `literal` Sign-up allows `3` requests per email address per hour. `src: Technical requirements rate limits`
- [ ] `C-TR-17` `literal` Reset requests allow `3` per email address per hour. `src: Technical requirements rate limits`
- [ ] `C-TR-18` `literal` Enquiries allow `3` per sender address per hour. `src: Technical requirements rate limits`
- [ ] `C-TR-19` `literal` Newsletter subscriptions allow `5` per email address per hour. `src: Technical requirements rate limits`
- [ ] `C-TR-20` `literal` Console writes allow `120` per minute per account. `src: Technical requirements rate limits`
- [ ] `C-TR-21` `literal` Each ordering route allows `30` replacements per minute per account. `src: Technical requirements rate limits`
- [ ] `C-TR-22` `constraint` A text field is stored trimmed with control characters stripped. `src: Technical requirements input handling`
- [ ] `C-TR-23` `ui` Markup typed into a case file title shows as visible text. `src: Technical requirements input handling`
- [ ] `C-TR-24` `constraint` A path traversal attempt in a slug answers not found. `src: Technical requirements input handling`
- [ ] `C-TR-25` `constraint` A slug from a request is accepted only from an editor matching lowercase letters, digits, hyphens. `src: Technical requirements input handling`
- [ ] `C-TR-26` `capability` The page sends a `site_opened` event to `POST /api/events` on the app origin. `src: Technical requirements analytics`
- [ ] `C-TR-27` `constraint` The server refuses an event name outside the named list. `src: Technical requirements analytics`
- [ ] `C-TR-28` `constraint` The server stores only the named properties of each event. `src: Technical requirements analytics`
- [ ] `C-TR-29` `constraint` The page calls no third-party host at runtime. `src: Technical requirements analytics`
- [ ] `C-TR-30` `capability` An editor reads stored events at `GET /api/studio/events`. `src: Technical requirements analytics`
- [ ] `C-TR-31` `literal` A first visit to the home screen transfers at most `320` kilobytes. `src: Technical requirements performance`
- [ ] `C-TR-32` `constraint` Opening the home screen fetches no poster, media or console code. `src: Technical requirements performance`

## C-DM Data model

- [ ] `C-DM-01` `data` The data model holds the nineteen named tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` API timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` Every seeded account signs in with `deku-demo-pw-2026`. `src: Data model credential block`
- [ ] `C-DM-04` `data` The account public shape carries `id`, `email`, `display_name`, `role`, `email_verified`, `verification_deadline`, `previous_email`, `previous_email_until`, `created_at`. `src: Data model account`
- [ ] `C-DM-05` `data` A visitor session expires 30 days after creation with a null idle timeout. `src: Data model account_session`
- [ ] `C-DM-06` `data` A studio session expires 12 hours after creation with `idle_timeout_seconds` of `7200`. `src: Data model account_session`
- [ ] `C-DM-07` `data` An invitation expires 14 days after creation. `src: Data model invitation`
- [ ] `C-DM-08` `data` A sector holds a unique kebab `token`, a `label`, a unique `position`. `src: Data model sector`
- [ ] `C-DM-09` `data` A client entry holds `sector_id`, `name`, a position unique within the sector. `src: Data model client_entry`
- [ ] `C-DM-10` `data` A case file `slug` stays null until the first title save. `src: Data model case_file`
- [ ] `C-DM-11` `data` A case file `version` starts at 1. `src: Data model case_file`
- [ ] `C-DM-12` `data` A case file `position` is set only for a published case file. `src: Data model case_file`
- [ ] `C-DM-13` `data` A chapter row holds `case_file_id`, `kind`, `position`, `payload`. `src: Data model chapter`
- [ ] `C-DM-14` `data` An information item row holds `heading`, `value`, `position`. `src: Data model information_item`
- [ ] `C-DM-15` `data` An award row holds `name`, `mark`, `position`. `src: Data model award`
- [ ] `C-DM-16` `data` A `case_media` row holds `key`, `content_type`, `size_bytes`, `sha256` with no byte column. `src: Data model case_media`
- [ ] `C-DM-17` `data` `slug_redirect` maps an `old_slug` to the case file. `src: Data model slug_redirect`
- [ ] `C-DM-18` `data` `retired_slug` keeps every issued slug. `src: Data model retired_slug`
- [ ] `C-DM-19` `data` A notice row holds `label`, `body`, a unique `position`, `updated_at`. `src: Data model notice_row`
- [ ] `C-DM-20` `data` An enquiry row holds the enquiry fields with a `state` defaulting to `new`. `src: Data model enquiry`
- [ ] `C-DM-21` `literal` The enquiry budget tokens are `under-25`, `25-50`, `50-100`, `100-250`, `250-up`. `src: Data model enquiry`
- [ ] `C-DM-22` `data` An enquiry `account_id` is set only for a verified signed-in sender. `src: Data model enquiry`
- [ ] `C-DM-23` `data` A shortlist holds one entry per account per case file. `src: Data model shortlist_entry`
- [ ] `C-DM-24` `data` A subscriber email is lowercased with no duplicate. `src: Data model subscriber`
- [ ] `C-DM-25` `literal` A message `kind` is one of `verify_address`, `reset_password`, `invitation`, `case_file_returned`, `case_file_live`, `enquiry_received`, `enquiry_arrived`. `src: Data model message`
- [ ] `C-DM-26` `data` An analytics event row holds a `name` with `properties`. `src: Data model analytics_event`
- [ ] `C-DM-27` `constraint` Two simultaneous sign-ups for one address create exactly one account. `src: Data model invariants`
- [ ] `C-DM-28` `constraint` Two simultaneous subscriptions for one address create exactly one subscriber. `src: Data model invariants`
- [ ] `C-DM-29` `constraint` No two published case files share a grid position. `src: Data model invariants`
- [ ] `C-DM-30` `constraint` No two chapters of one case file share a position. `src: Data model invariants`
- [ ] `C-DM-31` `data` The next case file is derived from the current grid order. `src: Data model derived`
- [ ] `C-DM-32` `constraint` Seeding creates no duplicate rows. `src: Data model seed data`
- [ ] `C-DM-33` `literal` The seeded display names are `Ines Varga`, `Theo Lamb`, `Juno Park`, `Sam Reed`. `src: Data model seed data`
- [ ] `C-DM-34` `literal` The seeded sector tokens run `sector-1` to `sector-7` in the pinned order. `src: Data model seed data`
- [ ] `C-DM-35` `data` The client roster seeds twenty-nine names in the pinned groups. `src: Data model seed data`
- [ ] `C-DM-36` `literal` The studio awards are `Harbour Prize`, `Wexel`, `A&DX`, `Open Show`, `Acclaims`, `FWX`. `src: Data model seed data`
- [ ] `C-DM-37` `literal` `Glass Harbour` at `glass-harbour` is seeded published with chapters `headline`, `text`, `image`, `list`. `src: Data model seed data`
- [ ] `C-DM-38` `literal` `Glass Harbour` carries the awards `Harbour Prize`, `Wexel` with information items `Year` over `2024`, `Role` over `Brand system`. `src: Data model seed data`
- [ ] `C-DM-39` `literal` `Night Signal` at `night-signal` is seeded published with chapters `headline`, `text`, `video`, `device`. `src: Data model seed data`
- [ ] `C-DM-40` `literal` `Soft Machinery` at `soft-machinery` is seeded published with chapters `headline`, `text`, `split`, `video_loop`. `src: Data model seed data`
- [ ] `C-DM-41` `literal` `Paper Orchard` at `paper-orchard` is seeded as a draft of `author@example.com` with an image object in the bucket. `src: Data model seed data`
- [ ] `C-DM-42` `literal` `Quiet Engine` at `quiet-engine` is seeded as submitted by `author2@example.com`. `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Five near-black grounds are ordered strictly by distance from the page. `src: Front-end specification palette`
- [ ] `C-FE-02` `ui` Translucent whites mark hairlines, dividers, field borders, the scrollbar thumb. `src: Front-end specification palette`
- [ ] `C-FE-03` `ui` The half-transparent blue development ground never appears. `src: Front-end specification palette`
- [ ] `C-FE-04` `ui` No colour from a scene library built-in table, such as a soft teal, appears on the site. `src: Front-end specification palette`
- [ ] `C-FE-05` `literal` The four weights in use are `200`, `300`, `400`, `500`. `src: Front-end specification type`
- [ ] `C-FE-06` `constraint` No font file is fetched by the app. `src: Front-end specification type`
- [ ] `C-FE-07` `ui` Type sizes follow the pinned ramp from 65px down to 10px. `src: Front-end specification type`
- [ ] `C-FE-08` `ui` Control labels stay at or above 11px with body copy at or above 13px. `src: Front-end specification type`
- [ ] `C-FE-09` `ui` The notice page with the console share one sixteen-column container. `src: Front-end specification space`
- [ ] `C-FE-10` `ui` Only circles, the scrollbar thumb, a device frame carry a radius. `src: Front-end specification space`
- [ ] `C-FE-11` `ui` The scrollbar is styled rather than hidden. `src: Front-end specification space`
- [ ] `C-FE-12` `literal` The document carries the fifteen named icon symbols inline, `arrow` through `social-b`. `src: Front-end specification iconography`
- [ ] `C-FE-13` `ui` Action marks are unfilled strokes, with object marks filled. `src: Front-end specification iconography`
- [ ] `C-FE-14` `ui` Every icon stroke is two units wide with sharp mitred corners. `src: Front-end specification iconography`
- [ ] `C-FE-15` `ui` The close control carries a short white vertical divider at the right edge. `src: Front-end specification global chrome`
- [ ] `C-FE-16` `ui` The reseed counter digits roll through a clipped box. `src: Front-end specification global chrome`
- [ ] `C-FE-17` `ui` The grid shows the site's own round drag cursor. `src: Front-end specification global chrome`
- [ ] `C-FE-18` `ui` The pending ring reads as accelerating rather than ticking. `src: Front-end specification motion`
- [ ] `C-FE-19` `ui` A control at rest never animates. `src: Front-end specification motion`
- [ ] `C-FE-20` `ui` A reseed swells the crystal facets outward before the facets return. `src: Front-end specification crystal`
- [ ] `C-FE-21` `ui` Several crystal facets float visibly detached from the mass. `src: Front-end specification crystal`
- [ ] `C-FE-22` `ui` The crystal region takes keyboard focus with a text label. `src: Front-end specification crystal`
- [ ] `C-FE-23` `ui` The `Audio` off mark reuses the crossed lines of the `close` mark. `src: Front-end specification sound`
- [ ] `C-FE-24` `ui` The menu words move in visible perspective. `src: Front-end specification home screen menu`
- [ ] `C-FE-25` `ui` The story sector label column spans a third of the reading column. `src: Front-end specification public layers`
- [ ] `C-FE-26` `ui` The carousel drag mark is a line with arrowheads at both ends. `src: Front-end specification public layers`
- [ ] `C-FE-27` `ui` The grid filter label is almost invisible. `src: Front-end specification public layers`
- [ ] `C-FE-28` `ui` Grid tiles move into place instead of reflowing. `src: Front-end specification public layers`
- [ ] `C-FE-29` `ui` A device frame is a rounded outline in the hint tone. `src: Front-end specification public layers`
- [ ] `C-FE-30` `ui` The showreel play control is a dark rectangle in front of the poster. `src: Front-end specification public layers`
- [ ] `C-FE-31` `ui` Notice rows pair a label column with a large copy column. `src: Front-end specification public layers`
- [ ] `C-FE-32` `ui` Console controls are small uppercase text with the double underline. `src: Front-end specification console`
- [ ] `C-FE-33` `ui` A resting field shows a thin border at the focused strength. `src: Front-end specification forms`
- [ ] `C-FE-34` `ui` A focused field shows a thicker border with the white outline. `src: Front-end specification forms`
- [ ] `C-FE-35` `ui` An invalid field shows a warm sand border over a warm sand message. `src: Front-end specification forms`
- [ ] `C-FE-36` `ui` The narrow tier shows the dismissible accordion arrival card at most once per visitor. `src: Front-end specification responsive`
- [ ] `C-FE-37` `literal` The arrival card reads `Someone is playing the accordion. Carry on.` with `CARRY ON`. `src: Front-end specification responsive`
- [ ] `C-FE-38` `ui` At the narrow tier the menu stacks the three words one per row. `src: Front-end specification responsive`
- [ ] `C-FE-39` `ui` At the narrow tier the grid shows one tile per row. `src: Front-end specification responsive`
- [ ] `C-FE-40` `ui` At the narrow tier a text chapter stacks the label above the copy. `src: Front-end specification responsive`
- [ ] `C-FE-41` `ui` Focus moves into an opened layer, stays trapped, returns to the opener on close. `src: Front-end specification accessibility`
- [ ] `C-FE-42` `ui` A focused corner control shows a thin white ring at the catchment bounds. `src: Front-end specification accessibility`
- [ ] `C-FE-43` `ui` Chapter rows reorder by keyboard with Space plus the arrow keys. `src: Front-end specification accessibility`
- [ ] `C-FE-44` `ui` A lifted row announces the pinned position message. `src: Front-end specification accessibility`
- [ ] `C-FE-45` `ui` The split handle moves by keyboard arrows with Home or End reaching the ends. `src: Front-end specification accessibility`
- [ ] `C-FE-46` `ui` The menu is a navigation landmark. `src: Front-end specification accessibility`
- [ ] `C-FE-47` `ui` A fine static monochrome grain lies over the window. `src: Front-end specification generated assets`
- [ ] `C-FE-48` `ui` An award renders as the award name under a short white rule. `src: Front-end specification generated assets`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product serves one studio tenant. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The product sends no email or SMS. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The product offers no payments or invoices. `src: Constraints bullet 3`
- [ ] `C-CN-04` `constraint` Two people cannot co-edit one field. `src: Constraints bullet 5`
- [ ] `C-CN-05` `constraint` The product offers no external identity provider or single sign-on. `src: Constraints bullet 7`
- [ ] `C-CN-06` `constraint` The app fetches no image, font, audio, video, texture or model file of its own. `src: Constraints bullet 8`
- [ ] `C-CN-07` `constraint` The app offers no light theme. `src: Constraints bullet 12`
- [ ] `C-CN-08` `constraint` The crawler fragments `/a/`, `/a/b`, `/a/i`, `/wa/`, `/abc/`, `/url/` are not product pages. `src: Constraints bullet 13`
- [ ] `C-CN-09` `constraint` No second locale ships. `src: Constraints bullet 10`
- [ ] `C-CN-10` `constraint` The product ships no native app. `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-05` `contract` The app serves a production build, never a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-06` `contract` The server keeps running after the build session ends, detached from the shell that started the server. `src: Deployment contract bullet 8`
- [ ] `C-DC-07` `contract` The server binds `0.0.0.0` rather than `127.0.0.1` or `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-08` `contract` List endpoints return a top-level JSON array. `src: Deployment contract API shapes para 1`
- [ ] `C-DC-09` `contract` Every studio endpoint refuses a request with no bearer token. `src: Deployment contract API shapes para 1`
- [ ] `C-DC-10` `contract` An invalid or unauthorized call answers a client error, never a server error. `src: Deployment contract API shapes para 1`
- [ ] `C-DC-11` `data` Every non-success body carries `error`, `message`, `fields`, `retry_after`. `src: Deployment contract API shapes para 2`
- [ ] `C-DC-12` `literal` The error tokens are `validation_failed`, `not_authenticated`, `not_authorised`, `not_found`, `conflict`, `version_conflict`, `state_not_allowed`, `rate_limited`, `server_error`. `src: Deployment contract API shapes para 2`
- [ ] `C-DC-13` `data` The public summary carries `id`, `slug`, `title`, `client`, `sector`, `sector_label`, `description`, `position`, `published_at`. `src: Deployment contract API shapes para 3`
- [ ] `C-DC-14` `data` The full public shape adds `launch_url`, `information_items`, `chapters`, `awards`, `next`. `src: Deployment contract API shapes para 3`
- [ ] `C-DC-15` `data` The studio shape adds `state`, `owner_id`, `reviewed_by`, `self_approved`, `return_note`, `version`, `draft_payload`, `presence`. `src: Deployment contract API shapes para 3`
- [ ] `C-DC-16` `data` `GET /api/site` returns `studio`, `sectors`, `clients`, `awards`, `contact`, `notice`, `newsletter`. `src: Deployment contract API shapes table`
- [ ] `C-DC-17` `capability` `GET /api/case-files` returns at most 24 case files per page. `src: Deployment contract API shapes table`
- [ ] `C-DC-18` `capability` `GET /api/enquiries/mine` lists the signed-in sender's enquiries. `src: Deployment contract API shapes table`
- [ ] `C-DC-19` `capability` `GET /api/studio/examples` reports `present` with `count`. `src: Deployment contract API shapes table`
- [ ] `C-DC-20` `data` The export carries `accounts`, `sectors`, `clients`, `case_files`, `chapters`, `enquiries`, `messages`. `src: Deployment contract API shapes table`
- [ ] `C-DC-21` `role` An author is refused on grid order, enquiries, invitations, the outbox, sectors, clients, notice rows, export, events, examples. `src: Deployment contract endpoint roles`
- [ ] `C-DC-22` `contract` The shortlist, messages, account endpoints refuse a request with no session. `src: Deployment contract endpoint roles`
- [ ] `C-DC-23` `contract` The interface reflects the rows in PostgreSQL with the objects in the MinIO bucket. `src: Deployment contract no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `editor@example.com` | seeded accounts | C-RL-44 | User roles para 5 |
| `author@example.com` | seeded accounts | C-RL-44 | User roles para 5 |
| `author2@example.com` | seeded accounts | C-RL-44 | User roles para 5 |
| `visitor@example.com` | seeded accounts | C-RL-44 | User roles para 5 |
| `case-files/{case_file_id}/{sha256_of_bytes}.{ext}` | uploaded image key follows | C-CF-02 | Core features rule 1 |
| `5242880` | upload larger than bytes | C-CF-07 | Core features rule 2 |
| `That combination is not one we know.` | failed sign-in answers | C-CF-23 | Core features rule 7 |
| `Confirm your address` | sign-up | C-CF-39 | Core features rule 12 |
| `If that address has an account, a reset link is on its way.` | reset request | C-CF-45 | Core features rule 14 |
| `Reset your password` | reset for an existing address | C-CF-46 | Core features rule 14 |
| `Kelo has invited you` | invitation | C-CF-53 | Core features rule 15 |
| `Making the story move.` | studio promise reads | C-CF-110 | Core features rule 40 |
| `Brand · Content · Experience · Digital` | disciplines line reads | C-CF-111 | Core features rule 40 |
| `about__studioTitle` | story title elements | C-CF-118 | Core features rule 44 |
| `about__studioSubtitle` | story title elements | C-CF-118 | Core features rule 44 |
| `Technology & Futures` | sector labels | C-CF-128 | Core features rule 49 |
| `Climate & Startups` | sector labels | C-CF-128 | Core features rule 49 |
| `Fashion & Beauty` | sector labels | C-CF-128 | Core features rule 49 |
| `Chain` | sector labels | C-CF-128 | Core features rule 49 |
| `Entertainment & Culture` | sector labels | C-CF-128 | Core features rule 49 |
| `Automotive` | sector labels | C-CF-128 | Core features rule 49 |
| `Collaborations` | sector labels | C-CF-128 | Core features rule 49 |
| `headline` | chapter kinds | C-CF-138 | Core features rule 55 |
| `text` | chapter kinds | C-CF-138 | Core features rule 55 |
| `list` | chapter kinds | C-CF-138 | Core features rule 55 |
| `image` | chapter kinds | C-CF-138 | Core features rule 55 |
| `video` | chapter kinds | C-CF-138 | Core features rule 55 |
| `video_loop` | chapter kinds | C-CF-138 | Core features rule 55 |
| `device` | chapter kinds | C-CF-138 | Core features rule 55 |
| `split` | chapter kinds | C-CF-138 | Core features rule 55 |
| `HARBOURSIDE` | offices | C-CF-154 | Core features rule 64 |
| `+00 1 234 5670` | offices | C-CF-154 | Core features rule 64 |
| `NORTHGATE` | offices | C-CF-154 | Core features rule 64 |
| `+00 2 345 6780` | offices | C-CF-154 | Core features rule 64 |
| `12 Quay Street` | harbourside lines | C-CF-155 | Core features rule 64 |
| `Harbourside Works` | harbourside lines | C-CF-155 | Core features rule 64 |
| `Floor 3` | harbourside lines | C-CF-155 | Core features rule 64 |
| `HS1 4QA` | harbourside lines | C-CF-155 | Core features rule 64 |
| `40 North Row` | northgate lines | C-CF-156 | Core features rule 64 |
| `NG2 7LT` | northgate lines | C-CF-156 | Core features rule 64 |
| `SOCIAL` | social lines under | C-CF-157 | Core features rule 64 |
| `Directory` | social lines under | C-CF-157 | Core features rule 64 |
| `Pictures` | social lines under | C-CF-157 | Core features rule 64 |
| `Feed` | social lines under | C-CF-157 | Core features rule 64 |
| `name` | enquiry fields | C-CF-159 | Core features rule 65 |
| `email` | enquiry fields | C-CF-159 | Core features rule 65 |
| `organisation` | enquiry fields | C-CF-159 | Core features rule 65 |
| `budget` | enquiry fields | C-CF-159 | Core features rule 65 |
| `brief` | enquiry fields | C-CF-159 | Core features rule 65 |
| `sector` | enquiry fields | C-CF-159 | Core features rule 65 |
| `consent` | enquiry fields | C-CF-159 | Core features rule 65 |
| `Thanks! You are now subscribed.` | newsletter success copy reads | C-CF-172 | Core features rule 67 |
| `EMAIL` | notice contact strip | C-CF-177 | Core features rule 69 |
| `privacy@kelo.example.com` | notice contact strip | C-CF-177 | Core features rule 69 |
| `ADDRESS, ONE` | notice contact strip | C-CF-177 | Core features rule 69 |
| `ADDRESS, TWO` | notice contact strip | C-CF-177 | Core features rule 69 |
| `Pick a sector.` | sector outside the seven | C-CF-237 | Core features rule 88 |
| `The description needs to be at least forty characters.` | description outside 40 to 400 characters | C-CF-238 | Core features rule 88 |
| `https` | launch address without | C-CF-239 | Core features rule 88 |
| `That launch address does not look right.` | launch address without | C-CF-239 | Core features rule 88 |
| `treatment-1` | award | C-CF-242 | Core features rule 88 |
| `treatment-8` | award | C-CF-242 | Core features rule 88 |
| `The Long Room` | title | C-CF-245 | Core features rule 89 |
| `the-long-room` | title | C-CF-245 | Core features rule 89 |
| `-2` | clashing slug | C-CF-246 | Core features rule 89 |
| `chapters` | submit with no chapter fails under | C-CF-262 | Core features rule 92 |
| `A case file needs at least one chapter.` | submit with no chapter fails under | C-CF-262 | Core features rule 92 |
| `We need a name to reply to.` | empty enquiry | C-CF-296 | Core features rule 102 |
| `That address does not look right.` | malformed enquiry address shows | C-CF-297 | Core features rule 102 |
| `Tell us a little more, forty characters at least.` | short enquiry brief shows | C-CF-298 | Core features rule 102 |
| `<title> needs changes` | message subject | C-CF-344 | Core features rule 123 |
| `<title> is live` | message subject | C-CF-345 | Core features rule 123 |
| `We got your message` | message subject | C-CF-347 | Core features rule 123 |
| `Enquiry from <name>` | message subject | C-CF-348 | Core features rule 123 |
| `/api/preview/<case-file-slug>.png` | case file preview image | C-CF-381 | Core features rule 136 |
| `/api/preview/site.png` | other public addresses use | C-CF-382 | Core features rule 136 |
| `og:title` | case file | C-CF-383 | Core features rule 136 |
| ` · Kelo` | case file | C-CF-383 | Core features rule 136 |
| `/` | public routes | C-UF-01 | User flow route table |
| `/story` | public routes | C-UF-01 | User flow route table |
| `/work` | public routes | C-UF-01 | User flow route table |
| `/work/all` | public routes | C-UF-01 | User flow route table |
| `/work/<case-file-slug>` | public routes | C-UF-01 | User flow route table |
| `/reel` | public routes | C-UF-01 | User flow route table |
| `/contact` | public routes | C-UF-01 | User flow route table |
| `/notice` | public routes | C-UF-01 | User flow route table |
| `/join` | account routes | C-UF-02 | User flow route table |
| `/invite` | account routes | C-UF-02 | User flow route table |
| `/reset` | account routes | C-UF-02 | User flow route table |
| `/shortlist` | account routes | C-UF-02 | User flow route table |
| `/studio/sign-in` | studio routes | C-UF-03 | User flow route table |
| `/studio` | studio routes | C-UF-03 | User flow route table |
| `/studio/review` | studio routes | C-UF-03 | User flow route table |
| `/studio/grid` | studio routes | C-UF-03 | User flow route table |
| `/studio/enquiries` | studio routes | C-UF-03 | User flow route table |
| `/studio/outbox` | studio routes | C-UF-03 | User flow route table |
| `/studio/site` | studio routes | C-UF-03 | User flow route table |
| `/studio/account` | studio routes | C-UF-03 | User flow route table |
| `/studio/case/<case-file-id>` | case file editor | C-UF-04 | User flow route table |
| `/studio` | signed-out redirects | C-UF-06 | User flow entry bullet 2 |
| `/studio/sign-in?next=/studio` | signed-out redirects | C-UF-06 | User flow entry bullet 2 |
| `Inter` | product font | C-UX-12 | UI/UX notes para 4 |
| `Arial, sans-serif` | product font | C-UX-12 | UI/UX notes para 4 |
| `48px` | wordmark | C-UX-15 | Front-end specification type |
| `3` | sign-up | C-TR-16 | Technical requirements rate limits |
| `3` | reset requests | C-TR-17 | Technical requirements rate limits |
| `3` | enquiries | C-TR-18 | Technical requirements rate limits |
| `5` | newsletter subscriptions | C-TR-19 | Technical requirements rate limits |
| `120` | console | C-TR-20 | Technical requirements rate limits |
| `30` | ordering route | C-TR-21 | Technical requirements rate limits |
| `320` | first visit to the home screen transfers | C-TR-31 | Technical requirements performance |
| `deku-demo-pw-2026` | seeded account | C-DM-03 | Data model credential block |
| `under-25` | enquiry budget tokens | C-DM-21 | Data model enquiry |
| `25-50` | enquiry budget tokens | C-DM-21 | Data model enquiry |
| `50-100` | enquiry budget tokens | C-DM-21 | Data model enquiry |
| `100-250` | enquiry budget tokens | C-DM-21 | Data model enquiry |
| `250-up` | enquiry budget tokens | C-DM-21 | Data model enquiry |
| `kind` | message | C-DM-25 | Data model message |
| `verify_address` | message | C-DM-25 | Data model message |
| `reset_password` | message | C-DM-25 | Data model message |
| `invitation` | message | C-DM-25 | Data model message |
| `case_file_returned` | message | C-DM-25 | Data model message |
| `case_file_live` | message | C-DM-25 | Data model message |
| `enquiry_received` | message | C-DM-25 | Data model message |
| `enquiry_arrived` | message | C-DM-25 | Data model message |
| `Ines Varga` | seeded display | C-DM-33 | Data model seed data |
| `Theo Lamb` | seeded display | C-DM-33 | Data model seed data |
| `Juno Park` | seeded display | C-DM-33 | Data model seed data |
| `Sam Reed` | seeded display | C-DM-33 | Data model seed data |
| `sector-1` | seeded sector tokens | C-DM-34 | Data model seed data |
| `sector-7` | seeded sector tokens | C-DM-34 | Data model seed data |
| `Harbour Prize` | studio awards | C-DM-36 | Data model seed data |
| `Wexel` | studio awards | C-DM-36 | Data model seed data |
| `A&DX` | studio awards | C-DM-36 | Data model seed data |
| `Open Show` | studio awards | C-DM-36 | Data model seed data |
| `Acclaims` | studio awards | C-DM-36 | Data model seed data |
| `FWX` | studio awards | C-DM-36 | Data model seed data |
| `Glass Harbour` | seeded case file | C-DM-37 | Data model seed data |
| `glass-harbour` | seeded case file | C-DM-37 | Data model seed data |
| `headline` | seeded case file | C-DM-37 | Data model seed data |
| `text` | seeded case file | C-DM-37 | Data model seed data |
| `image` | seeded case file | C-DM-37 | Data model seed data |
| `list` | seeded case file | C-DM-37 | Data model seed data |
| `Glass Harbour` | seeded case file detail | C-DM-38 | Data model seed data |
| `Harbour Prize` | seeded case file detail | C-DM-38 | Data model seed data |
| `Wexel` | seeded case file detail | C-DM-38 | Data model seed data |
| `Year` | seeded case file detail | C-DM-38 | Data model seed data |
| `2024` | seeded case file detail | C-DM-38 | Data model seed data |
| `Role` | seeded case file detail | C-DM-38 | Data model seed data |
| `Brand system` | seeded case file detail | C-DM-38 | Data model seed data |
| `Night Signal` | seeded case file | C-DM-39 | Data model seed data |
| `night-signal` | seeded case file | C-DM-39 | Data model seed data |
| `headline` | seeded case file | C-DM-39 | Data model seed data |
| `text` | seeded case file | C-DM-39 | Data model seed data |
| `video` | seeded case file | C-DM-39 | Data model seed data |
| `device` | seeded case file | C-DM-39 | Data model seed data |
| `Soft Machinery` | seeded case file | C-DM-40 | Data model seed data |
| `soft-machinery` | seeded case file | C-DM-40 | Data model seed data |
| `headline` | seeded case file | C-DM-40 | Data model seed data |
| `text` | seeded case file | C-DM-40 | Data model seed data |
| `split` | seeded case file | C-DM-40 | Data model seed data |
| `video_loop` | seeded case file | C-DM-40 | Data model seed data |
| `Paper Orchard` | seeded draft case file | C-DM-41 | Data model seed data |
| `paper-orchard` | seeded draft case file | C-DM-41 | Data model seed data |
| `author@example.com` | seeded draft case file | C-DM-41 | Data model seed data |
| `Quiet Engine` | seeded submitted case file | C-DM-42 | Data model seed data |
| `quiet-engine` | seeded submitted case file | C-DM-42 | Data model seed data |
| `author2@example.com` | seeded submitted case file | C-DM-42 | Data model seed data |
| `200` | four weights | C-FE-05 | Front-end specification type |
| `300` | four weights | C-FE-05 | Front-end specification type |
| `400` | four weights | C-FE-05 | Front-end specification type |
| `500` | four weights | C-FE-05 | Front-end specification type |
| `arrow` | document | C-FE-12 | Front-end specification iconography |
| `social-b` | document | C-FE-12 | Front-end specification iconography |
| `Someone is playing the accordion. Carry on.` | arrival card | C-FE-37 | Front-end specification responsive |
| `CARRY ON` | arrival card | C-FE-37 | Front-end specification responsive |
| `${APP_PUBLIC_PORT}:4173` | port mapping is | C-DC-02 | Deployment contract bullet 1 |
| `validation_failed` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `not_authenticated` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `not_authorised` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `not_found` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `conflict` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `version_conflict` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `state_not_allowed` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `rate_limited` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `server_error` | error tokens | C-DC-12 | Deployment contract API shapes para 2 |
| `Give it a title.` | title message | C-CF-235 | Core features rule 88 |
| `Say who it was for.` | client message | C-CF-236 | Core features rule 88 |
| `Passwords are at least twelve characters.` | password message | C-CF-25 | Core features rule 8 |
| `Too many tries. Give it a minute.` | rate-limit message | C-CF-61 | Core features rule 18 |
| `We need this to be able to reply.` | consent message | C-CF-299 | Core features rule 102 |
| `That is longer than we can store.` | organisation message | C-CF-294 | Core features rule 102 |
| `This part of the site belongs to the studio. If you think it should belong to you as well, ask whoever runs it.` | denied surface line | C-UF-10 | User flow entry bullet 5 |
| `BACK TO THE WORK` | denied surface control | C-UF-10 | User flow entry bullet 5 |
| `Not for you` | denied surface heading | C-UF-10 | User flow entry bullet 5 |
| `Nothing here yet.` | empty grid heading | C-CF-132 | Core features rule 52 |
| `No work in this category yet.` | empty grid line | C-CF-132 | Core features rule 52 |
| `SEE ALL WORK` | empty grid control | C-CF-132 | Core features rule 52 |
| `Tell us about it.` | enquiry heading | C-CF-158 | Core features rule 65 |
| `SEND` | enquiry control | C-UX-24 | UI/UX notes para 6 |
| `Thank you.` | enquiry success heading | C-CF-167 | Core features rule 66 |
| `We read everything and answer within two working days.` | enquiry success line | C-CF-167 | Core features rule 66 |
| `Kelo Customer Privacy Notice` | notice title | C-CF-176 | Core features rule 69 |
| `This privacy notice tells you what to expect us to do with your personal information.` | notice description | C-CF-176 | Core features rule 69 |
| `The chapter order is broken. Open the arranger and save it again.` | chapter order gate message | C-CF-259 | Core features rule 92 |
| `Another case file already has that address.` | slug gate message | C-CF-259 | Core features rule 92 |
| `Chapter <n> is not finished.` | chapter gate message | C-CF-263 | Core features rule 92 |
| `Information item <n> is missing a value.` | information gate message | C-CF-240 | Core features rule 88 |
| `Information item <n> is missing a heading.` | information heading message | C-CF-241 | Core features rule 88 |
| `Already handled by <name>.` | conflict message | C-CF-274 | Core features rule 95 |
| `<name> is also in here.` | presence line | C-CF-219 | Core features rule 85 |
| `Not here.` | not-found heading | C-UF-11 | User flow entry bullet 6 |
| `This piece is not published, or it never was.` | not-found line | C-UF-11 | User flow entry bullet 6 |
| `No reel yet.` | empty reel heading | C-CF-152 | Core features rule 63 |
| `The studio has not put a reel up.` | empty reel line | C-CF-152 | Core features rule 63 |
| `under 25` | budget band | C-CF-163 | Core features rule 65 |
| `25 to 50` | budget band | C-CF-163 | Core features rule 65 |
| `50 to 100` | budget band | C-CF-163 | Core features rule 65 |
| `100 to 250` | budget band | C-CF-163 | Core features rule 65 |
| `250 and up` | budget band | C-CF-163 | Core features rule 65 |
| `Kelo · Creative Studio` | wordmark line one | C-CF-63 | Core features rule 19 |
| `Since 2011` | wordmark line two | C-CF-63 | Core features rule 19 |
| `Studio Sign In` | menu account line | C-CF-106 | Core features rule 39 |
| `Your Shortlist` | menu account line | C-CF-108 | Core features rule 39 |
| `View All Projects` | archive control | C-CF-125 | Core features rule 48 |
| `NEW CASE FILE` | console control | C-CF-233 | Core features rule 87 |
| `SUBMIT FOR REVIEW` | console control | C-CF-258 | Core features rule 92 |
| `WITH THE EDITOR` | console control | C-CF-268 | Core features rule 93 |
| `APPROVE` | review control | C-CF-273 | Core features rule 95 |
| `RETURN` | review control | C-CF-270 | Core features rule 94 |
| `PUBLISH` | publication control | C-CF-276 | Core features rule 96 |
| `PUBLISH CHANGES` | publication control | C-CF-281 | Core features rule 98 |
| `SELF APPROVED` | list marker | C-RL-43 | User roles para 4 |
| `REMOVE THE EXAMPLES` | console control | C-CF-364 | Core features rule 128 |
| `REALLY?` | armed delete | C-CF-366 | Core features rule 129 |
| `EDIT THIS` | case file control | C-CF-148 | Core features rule 61 |
| `CONFIRM YOUR ADDRESS TO GET A REPLY` | unconfirmed notice | C-CF-44 | Core features rule 13 |
| `CLEAR FILTERS` | empty filter control | C-CF-320 | Core features rule 115 |
| `Nothing waiting.` | empty review queue | C-CF-313 | Core features rule 110 |
| `Say what needs changing.` | return note message | C-CF-206 | Core features rule 80 |
| `DISPATCH` | newsletter name | C-CF-170 | Core features rule 67 |
| `PRIVACY` | notice link | C-CF-174 | Core features rule 67 |
| `Selected Clients` | story heading | C-CF-112 | Core features rule 40 |
| `Awards` | story heading | C-CF-112 | Core features rule 40 |
| `LAUNCHED AT` | case file label | C-CF-136 | Core features rule 54 |
| `/verify` | address confirmation route | C-CF-343 | Core features rule 123 |
| `APP_PUBLIC_URL` | app address variable | C-DC-01 | Deployment contract bullet 1 |
| `DATABASE_URL` | database variable | C-TR-03 | Technical requirements para 1 |
| `STORAGE_ENDPOINT` | storage variable | C-TR-04 | Technical requirements para 1 |
| `STORAGE_BUCKET` | storage variable | C-CF-01 | Core features rule 1 |
| `/api/health` | health route | C-DC-04 | Deployment contract bullet 3 |
| `SAVED` | bar message | C-CF-203 | Core features rule 78 |
| `ORDER SAVED` | bar message | C-CF-204 | Core features rule 79 |
| `SENT FOR REVIEW` | bar message | C-CF-266 | Core features rule 93 |
| `LIVE` | bar message | C-CF-277 | Core features rule 96 |
| `TAKEN DOWN` | bar message | C-UF-40 | User flow journey 8 |
| `NEW ENQUIRY` | bar message | C-CF-334 | Core features rule 118 |
| `OFFLINE` | bar message | C-CF-314 | Core features rule 111 |
| `What information we collect, use, and why` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `LAWFUL BASES part 1` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `LAWFUL BASES part 2` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `Where we get personal information from` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `HOW LONG WE KEEP INFORMATION` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `who we share information with` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `your data protection rights` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `How to complain, United States` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `How to complain, European Union` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `How to complain, Canada` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `How to complain, Australia` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `How to complain, New Zealand` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `How to complain, United Kingdom` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `When this notice was last updated` | seeded notice row label | C-CF-178 | Core features rule 70 |
| `Aster` | seeded client roster name | C-DM-35 | Data model seed data |
| `Gannet` | seeded client roster name | C-DM-35 | Data model seed data |
| `Paper Lens` | seeded client roster name | C-DM-35 | Data model seed data |
| `Sandbox` | seeded client roster name | C-DM-35 | Data model seed data |
| `Alder Labs` | seeded client roster name | C-DM-35 | Data model seed data |
| `Groundswell Energy` | seeded client roster name | C-DM-35 | Data model seed data |
| `Sable` | seeded client roster name | C-DM-35 | Data model seed data |
| `Thornfield` | seeded client roster name | C-DM-35 | Data model seed data |
| `harbour Classics` | seeded client roster name | C-DM-35 | Data model seed data |
| `Clarelle` | seeded client roster name | C-DM-35 | Data model seed data |
| `Solene` | seeded client roster name | C-DM-35 | Data model seed data |
| `Trelawn & Co` | seeded client roster name | C-DM-35 | Data model seed data |
| `KVN` | seeded client roster name | C-DM-35 | Data model seed data |
| `Nautilus` | seeded client roster name | C-DM-35 | Data model seed data |
| `Zephyr` | seeded client roster name | C-DM-35 | Data model seed data |
| `Skra` | seeded client roster name | C-DM-35 | Data model seed data |
| `Nightly` | seeded client roster name | C-DM-35 | Data model seed data |
| `OBX` | seeded client roster name | C-DM-35 | Data model seed data |
| `Rook Games` | seeded client roster name | C-DM-35 | Data model seed data |
| `Playmarket` | seeded client roster name | C-DM-35 | Data model seed data |
| `Younger` | seeded client roster name | C-DM-35 | Data model seed data |
| `Lexon` | seeded client roster name | C-DM-35 | Data model seed data |
| `Torvid` | seeded client roster name | C-DM-35 | Data model seed data |
| `Lumen Motors` | seeded client roster name | C-DM-35 | Data model seed data |
| `Sabres` | seeded client roster name | C-DM-35 | Data model seed data |
| `Marconti` | seeded client roster name | C-DM-35 | Data model seed data |
| `MCK` | seeded client roster name | C-DM-35 | Data model seed data |
| `Emery Lauden` | seeded client roster name | C-DM-35 | Data model seed data |
| `Gallery Research Trust` | seeded client roster name | C-DM-35 | Data model seed data |
| `Nothing saved.` | empty shortlist heading | C-CF-384 | Core features rule 110 |
| `Open a case file and keep it here.` | empty shortlist line | C-CF-384 | Core features rule 110 |
| `No chapters yet.` | empty arranger heading | C-CF-385 | Core features rule 110 |
| `Add something to arrange.` | empty arranger line | C-CF-385 | Core features rule 110 |
| `BACK TO THE EDITOR` | empty arranger control | C-CF-385 | Core features rule 110 |
| `Nothing yet.` | empty case file list heading | C-CF-386 | Core features rule 110 |
| `No case files. Start one.` | empty case file list line | C-CF-386 | Core features rule 110 |
| `BACK ONLINE` | bar message | C-CF-387 | Core features rule 111 |
| `You are offline.` | offline heading | C-CF-389 | Core features rule 110 |
| `This page needs a connection. The work you have already opened still works.` | offline line | C-CF-389 | Core features rule 110 |
| `Your message is saved here and will send when you are back.` | offline contact notice | C-CF-388 | Core features rule 110 |
| `Anything you were writing is still on this device.` | offline console line | C-CF-389 | Core features rule 110 |
| `Nobody has written yet.` | empty inbox line | C-CF-390 | Core features rule 110 |
| `SEE THE CONTACT PAGE` | empty inbox control | C-CF-390 | Core features rule 110 |
| `No enquiries.` | empty inbox heading | C-CF-390 | Core features rule 110 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact shade behind each named colour family, tone, shade | C-UX-04 | the builder chooses the value within the stated relationships |
| the exact duration behind each of the three motion speeds | C-UX-25 | the builder chooses the value within the stated character |
| the exact size of a corner control catchment | C-CF-85 | stated as a relationship to the mark |
| the placeholder body text of the fourteen notice rows | C-CF-178 | only the labels are pinned |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 8 | 12 |
| User roles | 20 | 45 |
| Core features | 235 | 390 |
| User flow | 40 | 41 |
| UI and UX notes | 30 | 36 |
| Technical requirements | 30 | 32 |
| Data model | 40 | 42 |
| Front-end specification | 45 | 48 |
| Constraints | 10 | 10 |
| Deployment contract | 20 | 23 |

Sentence counts exclude restatements (a journey step restating a numbered rule, a constraint bullet restating an overview exclusion) and the obligations listed under Declared but ungraded below.

## Declared but ungraded

Obligations the brief states that no grading channel in this environment can observe. Each is recorded with its reason rather than cited falsely (OPEN-DECISIONS D-H).

- Core features rule 26: the wordmark within one second, the arrival overlay ceiling of eight seconds. why: wall-clock timing inside a grading container is not deterministic.
- Core features rule 35: the character of each synthesised bed or cue, the crossfade between beds, the ducking of cues. why: no channel can hear the page.
- Core features rule 105: the pending state ending after ten seconds. why: wall-clock timing.
- Core features rule 112: the too-old-browser notice. why: the grading browser is current.
- Core features rule 131: the newer-version chapter notice. why: no newer payload version exists to write.
- Core features rule 132: a missing string falling back to the source locale. why: only one locale ships.
- Core features rule 134: the long-string bounds of a translated locale. why: only one locale ships.
- Core features rule 135: the right-to-left mirroring. why: no right-to-left locale ships.
- Technical requirements: the use of NestJS, pg, the S3 client, three, argon2, sanitize-html. why: a black-box channel cannot read the source.
- Technical requirements: hosts or ports read from the environment rather than hardcoded. why: source-level.
- Technical requirements: no second database, cache, queue, object store, identity provider or mail vendor. why: source-level.
- Technical requirements: one request log line per request on standard output. why: the log stream is not reachable from the grading side.
- Technical requirements: the public read limit of 240 per minute per network address. why: the limit is keyed on the network address every channel shares, so the only observation of it also throttles every later public read of the same run, and the run can carry one or the other but never both.
- Technical requirements: one crystal drag in ten kept. why: sampling is decided in the page.
- Technical requirements: the paint budgets, the frame rate, the degradation ladder with its trigger. why: wall-clock or frame timing is not deterministic in a grading container.
- Technical requirements: the module boundaries, the chapter registry, the single bar writer. why: source-level.
- Technical requirements: a path traversal attempt recorded as an event. why: the event is sent by the page, not the server.
- Data model: the placeholder notice bodies; no seeded enquiry, subscriber, message or event. why: the browser pass writes these before any pytest read.
- Front-end specification: the fallback font size adjustment within two percent. why: no channel measures glyph metrics.
- Front-end specification: the static crystal fallback drawing. why: the grading browser renders three-dimensional graphics.
- Front-end specification: every transition naming the property it moves. why: source-level.
- Deployment contract: starting from the environment image with no manual steps; the credentials file at the app root; the reserved empty directories; the backing services used as already running; no edge functions; no persistent volumes, fixed names or custom networks. why: the environment operator confirms these at handoff, not an in-run channel.
- Core features rule 13: an address left unconfirmed for seven days deleted with its account. why: the window outruns any grading run.
- Core features rule 17: the sign-in layer over an expired console session, the typed text kept behind it, the retried save. why: a studio session lasts twelve hours, so the expiry cannot be reached in a run.
- Core features rule 23: the reseed counter clamped at its ceiling. why: reaching the ceiling takes a million reseeds.
- Core features rule 24: the static crystal drawing when three-dimensional rendering is unavailable. why: the grading browser draws it.
- Core features rule 78: the retries after two seconds and six seconds, and the third-failure notice. why: no channel can make a save fail.
- Core features rule 79 and rule 81: the bar messages after a failed reorder. why: no channel can make the reorder fail.
- Core features rule 107: the network-failure copy with every value kept. why: no channel can interrupt the page's own request.
- Core features rule 111: the queued console save replayed on reconnection and the message that follows it. why: the queue and the replay need an induced disconnection mid-edit.
- Core features rule 120: an instant action that fails running itself back. why: no channel can make the confirming request fail.
- Core features rule 122: the pinned note before a session ends. why: the note appears five minutes before a twelve-hour expiry.
- Constraints: the app staying responsive at forty published case files with a few hundred enquiries. why: reaching that size needs more console writes than the per-account limit admits in a run, so the state the claim is about cannot exist while anything else is observed.
- Core features rule 110: the error face of every surface, the loading skeletons, and the empty faces of the studio story, the work carousel and the review queue. why: an error face needs an induced request failure, a skeleton needs a held response, and the empty story roster, the empty carousel and the empty grid arranger are unreachable while the seeded roster and the seeded published work exist, the empty review queue while the seeded submitted case file waits. The notice page's own empty face needs the fourteen seeded rows gone.
- Core features rule 111: the bar reading `SHOWING WHAT WE HAD` on the first interaction with stale content. why: the phrase follows a failed refetch, and no channel can fail one.
