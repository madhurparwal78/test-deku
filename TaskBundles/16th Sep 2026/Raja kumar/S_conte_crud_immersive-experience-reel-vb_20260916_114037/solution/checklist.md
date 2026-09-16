# Checklist: deku/immersive-experience-reel-vb

Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Items: 306
Unpinned values flagged: 5

## C-OV Overview

- [ ] `C-OV-01` `capability` A visitor moves from the entry scene into the reel of work `src: Overview, moves through a reel of projects`
- [ ] `C-OV-02` `capability` A signed in producer collects projects into a reel `src: Overview, a signed in producer collects projects into a reel`
- [ ] `C-OV-03` `capability` Studio staff reply on the pitch queue `src: Overview, studio staff read the pitch queue and reply`
- [ ] `C-OV-04` `constraint` The product fetches no image, video or audio file of its own `src: Overview, It does not ship a single image, video, texture, model, font file or audio file of its own`
- [ ] `C-OV-05` `constraint` The product loads no third-party analytics `src: Overview, no third-party analytics`
- [ ] `C-OV-06` `constraint` A write made against an old version of a reel is refused rather than merged `src: Overview, writes made against an old version of it are refused rather than quietly merged`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor views every public state with no account `src: User roles, View every public state`
- [ ] `C-RL-02` `constraint` A visitor is refused every reel endpoint `src: User roles, Cannot create a reel, add to one, read a shared reel`
- [ ] `C-RL-03` `constraint` A visitor is refused every pitch endpoint `src: User roles, submit or read a pitch`
- [ ] `C-RL-04` `constraint` A visitor is refused every account read `src: User roles, or read any account`
- [ ] `C-RL-05` `role` A producer creates reels up to ten `src: User roles, create reels (at most ten)`
- [ ] `C-RL-06` `constraint` Another producer's reel answers exactly as a missing reel `src: User roles, it answers exactly as a reel or pitch that does not exist`
- [ ] `C-RL-07` `constraint` Another producer's pitch answers exactly as a missing pitch `src: User roles, it answers exactly as a reel or pitch that does not exist`
- [ ] `C-RL-08` `constraint` A producer asking for a pitch state besides withdrawn is refused as forbidden `src: User roles, cannot change a pitch to any state other than`
- [ ] `C-RL-09` `role` An editor reads every reel read-only `src: User roles, read every reel read-only`
- [ ] `C-RL-10` `role` An editor sees draft projects with the draft state `src: User roles, see draft projects and their state`
- [ ] `C-RL-11` `constraint` An editor is refused publishing a project `src: User roles, cannot publish or unpublish a project`
- [ ] `C-RL-12` `role` An admin publishes or unpublishes a project `src: User roles, publish and unpublish projects`
- [ ] `C-RL-13` `constraint` An admin is refused a change to the admin's own role `src: User roles, Cannot change their own role`
- [ ] `C-RL-14` `constraint` A producer session calling an editor or admin endpoint is refused by the server `src: User roles, a direct API call from a producer session to any editor-only or admin-only endpoint must be rejected by the server`
- [ ] `C-RL-15` `role` Self-signup creates a producer `src: User roles, self-signup always creates a`
- [ ] `C-RL-16` `literal` The seeded admin signs in as `admin@example.com` `src: User roles, admin@example.com`
- [ ] `C-RL-17` `literal` The seeded editor signs in as `editor@example.com` `src: User roles, editor@example.com`
- [ ] `C-RL-18` `literal` The seeded producer signs in as `producer@example.com` `src: User roles, producer@example.com`
- [ ] `C-RL-19` `literal` The second seeded producer signs in as `producer2@example.com` `src: User roles, producer2@example.com`
- [ ] `C-RL-20` `literal` The seeded producer belongs to `Northlight Agency` `src: User roles, Northlight Agency`
- [ ] `C-RL-21` `literal` The second seeded producer belongs to `Farrow Kiln` `src: User roles, Farrow Kiln`

## C-CF Core features

- [ ] `C-CF-01` `capability` Changing scene state never loads a new document `src: Core features, Changing state never reloads the document`
- [ ] `C-CF-02` `constraint` The document never scrolls on a public route `src: Core features, The document never scrolls on a public route`
- [ ] `C-CF-03` `capability` Pressing ArrowDown on the entry state enters the reel `src: Core features, advancing enters`
- [ ] `C-CF-04` `capability` Pressing Escape on a project returns to the reel `src: Core features, leaves a project, the same as`
- [ ] `C-CF-05` `constraint` Pressing Tab never changes scene state `src: Core features, never changes scene state`
- [ ] `C-CF-06` `capability` SCROLL DOWN is a focusable button entering the reel on Enter `src: Core features, are focusable buttons, not decorative text`
- [ ] `C-CF-07` `capability` Every scene address opens directly into its state on a cold load `src: Core features, every address resolves directly into its state on a cold load`
- [ ] `C-CF-08` `capability` Leaving a project pushes a history entry, so Back returns to the project `src: Core features, pushes a new entry between families`
- [ ] `C-CF-09` `constraint` Every string drawn into the scene exists in the document as text `src: Core features, Every string drawn into the scene also exists in the document as text`
- [ ] `C-CF-10` `capability` A browser with no render context still reaches every state `src: Core features, A machine that cannot draw the scene still gets the whole site`
- [ ] `C-CF-11` `literal` A missing render context shows the banner `Running without the full scene.` `src: Core features, a banner reads`
- [ ] `C-CF-12` `capability` A state change is announced assertively with the state name `src: Core features, Every state change is announced assertively`
- [ ] `C-CF-13` `literal` The entry state asks `What are you looking for?` `src: Core features, shows the question`
- [ ] `C-CF-14` `literal` The entry state offers intent links reading `-> games`, `-> multiplayer`, `-> XR / VR / AI`, `-> installations`, `-> websites` `src: Core features, exactly five intent links, in this order`
- [ ] `C-CF-15` `data` Each intent link resolves to the category filter address on the reel `src: Core features, they resolve, in order`
- [ ] `C-CF-16` `ui` The entry state carries no wordmark, menu or footer `src: Core features, no wordmark in the chrome, no menu and no footer`
- [ ] `C-CF-17` `ui` A reel filtered to one category shows the selected intent link plus a clear control `src: Core features, they collapse to the selected one plus a clear control`
- [ ] `C-CF-18` `ui` SCROLL DOWN sits above the intent list `src: Core features, sits above the intent list`
- [ ] `C-CF-19` `capability` The reel lists every published project `src: Core features, lists every published project, one row each`
- [ ] `C-CF-20` `ui` The reel shows one row per project in a single column `src: Core features, in a single column at every width`
- [ ] `C-CF-21` `data` A row metadata line reads year, client name, first category slug separated by space slash space `src: Core features, a metadata line reading year, client and category separated by space slash space`
- [ ] `C-CF-22` `ui` Pointing at a reel row dims every other row `src: Core features, pointing at a row brings its title to full strength and dims the other rows`
- [ ] `C-CF-23` `ui` Selecting a row retints the environment toward the project colour before the copy arrives `src: Core features, the environment retints toward the selected project's colour`
- [ ] `C-CF-24` `constraint` Each reel row star carries the accessible name Add or Remove with the project title `src: Core features, Its accessible name is`
- [ ] `C-CF-25` `capability` A signed out star routes to sign in with next set to the reel `src: Core features, Signed out, the star is present and routes to`
- [ ] `C-CF-26` `capability` The account pill count rises before the server answers a star `src: Core features, the account pill count rises before the server answers`
- [ ] `C-CF-27` `capability` A refused star is put back before the failure appears `src: Core features, the change is put back first and only then does the failure appear`
- [ ] `C-CF-28` `capability` Every part of the reel query lives in the address `src: Core features, Every part of the query lives in the address`
- [ ] `C-CF-29` `data` Values inside one parameter widen the result `src: Core features, Values inside one parameter combine with`
- [ ] `C-CF-30` `data` Different parameters narrow the result `src: Core features, different parameters combine with`
- [ ] `C-CF-31` `literal` The query `category=games&year=2021&year=2022` returns `Welcome to Stonehall`, `20 Years of Nexus`, `Discover your Familiar` `src: Core features, For example`
- [ ] `C-CF-32` `ui` The control row states the combining rule in words when several parameters are set `src: Core features, The control row states the combining rule in words`
- [ ] `C-CF-33` `data` A client slug folds accents, lower-cases, joins words with single hyphens `src: Core features, A client slug is the client name with accents removed`
- [ ] `C-CF-34` `data` An unknown client slug returns an empty result `src: Core features, An unknown client slug returns an empty result, not an error`
- [ ] `C-CF-35` `data` Search matches the title, client name or description ignoring accents or case `src: Core features, case-insensitive and`
- [ ] `C-CF-36` `data` Title matches come before client matches, which come before description matches `src: Core features, every title match comes before every client-name match`
- [ ] `C-CF-37` `data` The recent sort orders projects newest first, then by studio position `src: Core features, orders by year, newest first`
- [ ] `C-CF-38` `data` The oldest sort is the exact reverse of recent `src: Core features, is the exact reverse of`
- [ ] `C-CF-39` `data` The title sort compares folded titles ignoring case or accents `src: Core features, orders alphabetically, case-insensitive and accent-insensitive`
- [ ] `C-CF-40` `constraint` An invalid category, year, search length or sort is refused naming the field `src: Core features, is rejected as invalid with the field named`
- [ ] `C-CF-41` `literal` A search holds at most `80` characters `src: Core features, at most`
- [ ] `C-CF-42` `capability` The search field updates the address after typing settles `src: Core features, The search field updates the address after the typing has settled`
- [ ] `C-CF-43` `ui` Sorting is three capsules, never a dropdown `src: Core features, Sorting is three capsules, never a dropdown`
- [ ] `C-CF-44` `literal` A filter matching nothing shows `Nothing matches that.` beside `Clear filters` `src: Core features, A filter that matches nothing shows`
- [ ] `C-CF-45` `capability` Clear filters keeps the sort `src: Core features, Clear filters keeps`
- [ ] `C-CF-46` `constraint` A project view carries the title, metadata line, description, Project Link, a Close control `src: Core features, shows, in the lower left of the frame and nowhere else`
- [ ] `C-CF-47` `ui` Project copy sits in the lower left of the frame `src: Core features, in the lower left of the frame and nowhere else`
- [ ] `C-CF-48` `literal` E.D.E.N. reads `2021 / U.S. Skyforce / xr` `src: Core features, The two captured projects carry their measured copy exactly`
- [ ] `C-CF-49` `literal` Rally reads `2014 / Nimbus / installation` `src: Core features, The two captured projects carry their measured copy exactly`
- [ ] `C-CF-50` `constraint` Neither measured description ends in a full stop `src: Core features, Neither description ends in a full stop`
- [ ] `C-CF-51` `capability` SCROLL TO CLOSE, Close or Escape each return a project to the reel `src: Core features, There are three ways out of a project`
- [ ] `C-CF-52` `ui` Interface text keeps one near-white on every project `src: Core features, the text stays the same near-white on every project`
- [ ] `C-CF-53` `ui` A signed in producer sees the project star beside Close `src: Core features, For a signed in producer the star sits to the right of`
- [ ] `C-CF-54` `constraint` A draft project address renders the not-found state for a visitor `src: Core features, A draft project, a project that does not exist, and a slug of the wrong shape all render the not-found state`
- [ ] `C-CF-55` `literal` The not-found page reads `We cannot find that.` `src: Core features, render the product's own not-found page`
- [ ] `C-CF-56` `constraint` An unserved address answers a not-found status at the document level `src: Core features, the HTML document for that address comes back with a not-found status`
- [ ] `C-CF-57` `literal` A forbidden desk or studio page reads `That is not yours to open.` `src: Core features, the same layout reads`
- [ ] `C-CF-58` `constraint` A missing desk object renders the same page as a forbidden one `src: Core features, A missing object and a forbidden one render identically`
- [ ] `C-CF-59` `literal` The contact page shows the studio address `hello@example.com` `src: Core features, the studio address`
- [ ] `C-CF-60` `ui` The contact page says which of the enquiry form or the assistant suits a record `src: Core features, offers both an enquiry form and the assistant, and says which is which`
- [ ] `C-CF-61` `constraint` Each invalid enquiry field is refused with the message naming the field `src: Core features, The enquiry form takes`
- [ ] `C-CF-62` `constraint` An enquiry carrying the decoy field is refused, storing nothing `src: Core features, An enquiry that arrives with`
- [ ] `C-CF-63` `literal` The enquiry decoy field is named `company_website` `src: Core features, The form carries an unattended decoy field named`
- [ ] `C-CF-64` `constraint` At most five enquiries an hour are accepted from one address block `src: Core features, at most`
- [ ] `C-CF-65` `data` An accepted enquiry gets a reference EN followed by six digits `src: Core features, An accepted enquiry gets a reference`
- [ ] `C-CF-66` `capability` An accepted enquiry sends one mail to the sender plus one to the studio queue `src: Core features, sends two mails`
- [ ] `C-CF-67` `literal` The resting assistant input reads `ASK ME ANYTHING...` `src: Core features, The resting assistant is a text input reading`
- [ ] `C-CF-68` `ui` Escape closes the assistant panel `src: Core features, Escape closes the panel and returns focus to the input`
- [ ] `C-CF-69` `capability` An answer given with a project as context names the project title `src: Core features, An answer given with a project as context names that project's title`
- [ ] `C-CF-70` `capability` The assistant answers from the studio's own published records `src: Core features, The assistant answers from the studio's own published records`
- [ ] `C-CF-71` `constraint` An assistant answer carries no http or https address `src: Core features, An answer is plain text and never carries an outbound link`
- [ ] `C-CF-72` `constraint` A question over five hundred characters is refused `src: Core features, A question is capped at`
- [ ] `C-CF-73` `constraint` A draft project slug is answered as not found by the assistant `src: Core features, A draft project is never context`
- [ ] `C-CF-74` `constraint` The assistant never claims to be a person `src: Core features, It never claims to be a person`
- [ ] `C-CF-75` `constraint` The assistant never asks for an email address in the conversation `src: Core features, never asks for an email address inside the conversation`
- [ ] `C-CF-76` `constraint` At most forty questions an hour are answered per session `src: Core features, questions per hour are answered per session`
- [ ] `C-CF-77` `data` The first answer sets an assistant session cookie `src: Core features, the first answer sets an`
- [ ] `C-CF-78` `ui` The typing indicator shows from submission until the first answer text `src: Core features, The typing indicator appears the moment a question is submitted`
- [ ] `C-CF-79` `data` Each answered question is kept as one turn attached to no account `src: Core features, Each answered question is kept as one assistant turn`
- [ ] `C-CF-80` `data` The ambient bed holds four generated tracks `src: Core features, an ambient music bed of four generated tracks`
- [ ] `C-CF-81` `constraint` The audio toggle is the first control in the document `src: Core features, is the first control in the document on every route`
- [ ] `C-CF-82` `constraint` Audio is off on first arrival `src: Core features, on first arrival, always`
- [ ] `C-CF-83` `capability` The audio setting survives a reload in the same browser `src: Core features, The setting persists per browser`
- [ ] `C-CF-84` `literal` The ticker names the track as `Slow Current--Halcyon Works` `src: Core features, The ticker names the playing track`
- [ ] `C-CF-85` `capability` The ticker next control changes the named track `src: Core features, its previous and next controls change track`
- [ ] `C-CF-86` `literal` The consent surface reads `Our site uses essential cookies and, with your consent, analytics cookies. Details in` `src: Core features, On every public route a consent surface reads`
- [ ] `C-CF-87` `literal` The consent surface offers `Accept Cookies` beside `Reject Cookies` `src: Core features, On every public route a consent surface reads`
- [ ] `C-CF-88` `capability` A consent answer survives a reload `src: Core features, the answer survives a reload and the question is not asked again`
- [ ] `C-CF-89` `data` The Privacy Notice link opens the privacy page on the app origin `src: Core features, opens`
- [ ] `C-CF-90` `capability` The privacy page states what the studio stores about a person `src: Core features, The privacy page states what the studio stores about a person`
- [ ] `C-CF-91` `capability` Cookie preferences on the privacy page reopens the consent question `src: Core features, control that reopens the choice`
- [ ] `C-CF-92` `data` Only the three exempt events are stored before consent `src: Core features, Three events carry no identifier and may be recorded before consent`
- [ ] `C-CF-93` `constraint` A rejected consent drops later events `src: Core features, a refusal is durable, and events that would have fired are dropped`
- [ ] `C-CF-94` `constraint` Nothing a person typed becomes an analytics property `src: Core features, Nothing a person typed is ever an analytics property`
- [ ] `C-CF-95` `capability` Sign up takes email, display name, organisation, password `src: Core features, Sign up`
- [ ] `C-CF-96` `constraint` A sign up email is unique regardless of case `src: Core features, is case-folded on write and unique regardless of case`
- [ ] `C-CF-97` `literal` A taken email is refused with `That email already has an account.` `src: Core features, is refused as a conflict with`
- [ ] `C-CF-98` `constraint` Sign up refuses a malformed email, an empty name, a long organisation or a short password `src: Core features, password`
- [ ] `C-CF-99` `capability` Sign up sends the confirmation mail `src: Core features, sends the confirmation mail`
- [ ] `C-CF-100` `capability` A confirmation token verifies the account once `src: Core features, The token verifies the account once`
- [ ] `C-CF-101` `literal` A used or unknown token is refused with `That link has expired. Ask for a new one.` `src: Core features, a used or unknown token is refused with`
- [ ] `C-CF-102` `capability` Resend sends a fresh confirmation mail, invalidating the earlier link `src: Core features, sends a fresh confirmation mail and invalidates the earlier link`
- [ ] `C-CF-103` `constraint` An unverified producer is refused a pitch `src: Core features, An unverified producer may build reels but not submit a pitch`
- [ ] `C-CF-104` `ui` The sign in form labels fields Email, Password with a Sign in button `src: Core features, form labels its fields`
- [ ] `C-CF-105` `capability` Sign in matches the email regardless of case `src: Core features, The email is matched regardless of case`
- [ ] `C-CF-106` `constraint` Every failed sign in answers with one shared failure message naming neither half `src: Core features, Every failure answers`
- [ ] `C-CF-107` `constraint` Five failed sign ins against one email lock the email for fifteen minutes `src: Core features, After five failed sign-ins against one email inside fifteen minutes`
- [ ] `C-CF-108` `constraint` The failure count belongs to the email however each attempt was cased `src: Core features, The count belongs to the email regardless of how it was cased`
- [ ] `C-CF-109` `literal` Reset always answers `If that address has an account, a reset link is on its way.` `src: Core features, always answers the same accepted response`
- [ ] `C-CF-110` `constraint` Only the first reset request in an hour sends mail `src: Core features, only the first of them in that hour sends mail`
- [ ] `C-CF-111` `constraint` A reset token works once `src: Core features, the token is single use`
- [ ] `C-CF-112` `constraint` A successful sign in invalidates an outstanding reset token `src: Core features, invalidated by use or by any successful sign-in to that account`
- [ ] `C-CF-113` `capability` Sign out ends the session on the server at once `src: Core features, ends the session on the server and its token stops working at once`
- [ ] `C-CF-114` `constraint` A role change ends every session of the account `src: Core features, A role change ends every session of that account`
- [ ] `C-CF-115` `literal` The account capsule shows initials with the reel count, for example `JR_00` `src: Core features, for example`
- [ ] `C-CF-116` `constraint` An unsafe next falls back to the role home `src: Core features, is honoured after sign in only when it is a path on this origin`
- [ ] `C-CF-117` `literal` Changing one's own role is refused with `You cannot change your own role.` `src: Core features, changing one's own role is refused with`
- [ ] `C-CF-118` `literal` Demoting the last admin is refused with `The last owner cannot be demoted.` `src: Core features, The last remaining admin cannot be demoted`
- [ ] `C-CF-119` `constraint` Two admins demoting each other at one instant leave one admin `src: Core features, This holds when two admins try to demote each other at the same instant`
- [ ] `C-CF-120` `data` Every accepted reel write raises the reel version by one `src: Core features, every accepted write raises the reel's`
- [ ] `C-CF-121` `constraint` A reel write carrying a stale version is refused with the current version plus the current reel `src: Core features, A write carrying any other version is refused as a conflict`
- [ ] `C-CF-122` `constraint` Two reel writes on one version at one instant are never both accepted `src: Core features, Two writes carrying the same version that arrive at the same instant are never both accepted`
- [ ] `C-CF-123` `literal` An eleventh reel is refused with `You have ten reels. Rename or delete one.` `src: Core features, the eleventh is refused with`
- [ ] `C-CF-124` `data` Adding a project puts the project at the end of the order `src: Core features, Adding a project puts it at the end of the order`
- [ ] `C-CF-125` `constraint` Only a published project joins a reel `src: Core features, Only a published project can be added`
- [ ] `C-CF-126` `constraint` A project added twice to one reel is refused as a conflict with the already-on-reel message `src: Core features, A project already on the reel is refused as a conflict with`
- [ ] `C-CF-127` `literal` A sixteenth item is refused with `A reel holds every project there is. Remove one to add another.` `src: Core features, A sixteenth item is refused with`
- [ ] `C-CF-128` `data` Reel positions run from one to the item count with no gap `src: Core features, Positions always run`
- [ ] `C-CF-129` `constraint` An incomplete reorder is refused with the message asking for every project exactly once `src: Core features, anything else is rejected as invalid with`
- [ ] `C-CF-130` `literal` A note over five hundred characters is refused with `A note holds up to five hundred characters.` `src: Core features, A note is plain text of at most`
- [ ] `C-CF-131` `data` Markup in a note is stored as the typed characters `src: Core features, Markup in a note is stored and shown as its characters`
- [ ] `C-CF-132` `ui` Saving a note shows Saved `src: Core features, saving shows`
- [ ] `C-CF-133` `data` An unpublished item stays on the reel reading as unavailable `src: Core features, stays on the reel, reads as unavailable`
- [ ] `C-CF-134` `data` The stored reel order with notes matches the desk after a reload `src: Core features, The order and the notes are what the reel shows after a reload`
- [ ] `C-CF-135` `capability` Any signed in role holding a share link reads the reel with notes `src: Core features, Anyone signed in, in any role, holding the link reads the reel including its notes`
- [ ] `C-CF-136` `constraint` A visitor opening a share link is sent to sign in `src: Core features, a visitor who is not signed in is sent to sign in`
- [ ] `C-CF-137` `constraint` A revoked share token answers exactly as a missing reel `src: Core features, A revoked or never-minted token answers exactly as a missing reel`
- [ ] `C-CF-138` `constraint` A missing reel, a wrong-shape reel id or another producer's reel get one not-found body `src: Core features, all get the same not-found answer with the same body`
- [ ] `C-CF-139` `constraint` An editor writing a reel is refused `src: Core features, Editors and admins read any reel but cannot write one`
- [ ] `C-CF-140` `constraint` Deleting a reel under a wrong confirming title is refused with the type-the-title message `src: Core features, A draft reel is deleted by confirming its exact title`
- [ ] `C-CF-141` `data` A deleted reel is kept recoverable `src: Core features, it disappears from the desk and is kept, recoverable`
- [ ] `C-CF-142` `constraint` Deleting a reel holding an open pitch is refused with the withdraw-first message `src: Core features, A reel with an open pitch is refused with`
- [ ] `C-CF-143` `constraint` A submitted reel refuses item, order, note or title edits with the reel-sent message `src: Core features, is read-only`
- [ ] `C-CF-144` `capability` A submitted reel keeps sharing `src: Core features, sharing and revoking still work`
- [ ] `C-CF-145` `ui` Removing an item offers undo from the band `src: Core features, Removing an item applies at once and can be undone from the band`
- [ ] `C-CF-146` `constraint` Each invalid pitch field is refused with the field message `src: Core features, A pitch takes`
- [ ] `C-CF-147` `literal` A pitch missing a budget band is refused with `Choose a budget band.` `src: Core features, plus`
- [ ] `C-CF-148` `literal` The budget bands are `under-50k`, `50k-100k`, `100k-250k`, `250k-500k`, `500k-plus` `src: Core features, The five budget bands are`
- [ ] `C-CF-149` `constraint` A pitch timing is one of four pinned timing slugs from the current month to just exploring `src: Core features, The four timings are`
- [ ] `C-CF-150` `constraint` A reel with no available item is refused a pitch with the add-a-project message `src: Core features, only with at least one available item`
- [ ] `C-CF-151` `literal` An unverified producer is refused a pitch with `Confirm your email to send a pitch.` `src: Core features, only once the account is verified`
- [ ] `C-CF-152` `literal` A sixth open pitch is refused with `You have five open pitches. We will get to them.` `src: Core features, the sixth is refused with`
- [ ] `C-CF-153` `data` A submitted pitch gets a reference PT followed by six digits in state submitted `src: Core features, A submitted pitch gets a reference`
- [ ] `C-CF-154` `data` The reel moves to submitted with the pitch `src: Core features, The reel moves to`
- [ ] `C-CF-155` `data` A pitch lists unavailable item titles apart from carried titles `src: Core features, separately, the titles of any unavailable items it left out`
- [ ] `C-CF-156` `constraint` Two submissions of one reel at one instant create one pitch with one set of mails `src: Core features, Two submissions of the same reel arriving at the same instant create exactly one pitch`
- [ ] `C-CF-157` `capability` A producer lands on the pitch page after submitting `src: Core features, The producer lands on`
- [ ] `C-CF-158` `ui` A failed pitch submission keeps the form filled `src: Core features, A failed submission keeps the form filled`
- [ ] `C-CF-159` `capability` An editor moves an open pitch to closed `src: Core features, An editor or admin may move an open pitch to`
- [ ] `C-CF-160` `constraint` Changing a closed or withdrawn pitch is refused with the change-not-allowed message `src: Core features, Changing a`
- [ ] `C-CF-161` `capability` Withdrawing a pitch returns the reel to draft `src: Core features, returns the reel to`
- [ ] `C-CF-162` `capability` Withdrawing a pitch mails the studio queue `src: Core features, and mails the studio queue`
- [ ] `C-CF-163` `constraint` A message on a closed pitch is refused with the closed-to-new-messages message `src: Core features, otherwise`
- [ ] `C-CF-164` `capability` A studio message on a submitted pitch moves the pitch into conversation `src: Core features, A message from an editor or admin on a`
- [ ] `C-CF-165` `capability` A studio message mails the producer `src: Core features, mails the producer`
- [ ] `C-CF-166` `constraint` A producer's own message changes no state, sending no mail `src: Core features, A message from the producer never changes the state and sends no mail`
- [ ] `C-CF-167` `literal` A twenty-first pitch message in an hour is refused with `That is a lot of messages. Try again shortly.` `src: Core features, messages per pitch per hour are accepted`
- [ ] `C-CF-168` `data` The studio queue lists every pitch newest first with the producer organisation `src: Core features, lists every pitch newest first`
- [ ] `C-CF-169` `capability` Mail travels over SMTP into Mailpit `src: Core features, The app sends real mail over SMTP`
- [ ] `C-CF-170` `constraint` Every mail is plain text carrying one link `src: Core features, Every mail is plain text only, carries exactly one link`
- [ ] `C-CF-171` `data` Every mail names the address the mail went to `src: Core features, ends with a line stating which address it went to and why`
- [ ] `C-CF-172` `constraint` Each mail goes to one recipient with no copy `src: Core features, each mail goes to one recipient with no cc and no bcc`
- [ ] `C-CF-173` `literal` Mail subjects open `Confirm your email`, `Reset your password`, `We have your pitch`, `New pitch from`, `The studio replied`, `Pitch withdrawn`, `Your enquiry`, `Enquiry from` `src: Core features, Subjects are exact`
- [ ] `C-CF-174` `data` The confirmation link targets the email confirmation route carrying a token `src: Core features, The confirmation link is`
- [ ] `C-CF-175` `data` The reset link targets the reset route with a token `src: Core features, the reset link is`
- [ ] `C-CF-176` `literal` A dropped connection shows `You are offline. Changes are held.` `src: Core features, When the connection drops a banner reads`
- [ ] `C-CF-177` `capability` A star made offline is held, then sent once the connection returns `src: Core features, When the connection returns the held changes are sent in order`
- [ ] `C-CF-178` `ui` A desk holding no reel reads No reels yet. `src: Core features, with no reels`
- [ ] `C-CF-179` `capability` A star made with no reel creates a reel titled Untitled reel `src: Core features, A reel created by starring without a reel gets the title`
- [ ] `C-CF-180` `ui` The pitch form lists the reel items read-only `src: Core features, opens the pitch form listing the reel's items, read-only there`
- [ ] `C-CF-181` `ui` The account panel lists the display name, organisation, Your reels, Your pitches, Audio, Sign out `src: Core features, The account panel, opened from that capsule, lists the display name and organisation`
- [ ] `C-CF-182` `data` A pitch mail links to the pitch page, a studio mail to the studio queue, an enquiry mail to the contact page `src: Core features, a pitch mail to the producer links to their pitch page`
- [ ] `C-CF-183` `capability` A studio reply reaches an open pitch page within twenty seconds with no reload `src: Core features, see new messages and state changes within twenty seconds while the tab is visible`
- [ ] `C-CF-184` `literal` An empty question is refused with `Ask a question first.` `src: Core features, and an empty one with`
- [ ] `C-CF-185` `capability` The active reel defaults to the most recently updated reel on a new machine `src: Core features, The active reel defaults to the most recently updated reel on a new machine`
- [ ] `C-CF-186` `constraint` The session token is never kept in browser storage `src: Core features, The session is therefore not kept in browser storage`

## C-UF User flow

- [ ] `C-UF-01` `capability` Signing in sends a producer to the desk `src: User flow, Signing in sends a producer to`
- [ ] `C-UF-02` `capability` Signing in sends an editor to the studio `src: User flow, Signing in sends a producer to`
- [ ] `C-UF-03` `capability` A visitor opening the desk is sent to sign in carrying next `src: User flow, is sent to`
- [ ] `C-UF-04` `constraint` A producer opening the studio reads That is not yours to open. `src: User flow, A producer opening`
- [ ] `C-UF-05` `capability` Signing out returns to the entry `src: User flow, Signing out ends the session and returns to`
- [ ] `C-UF-06` `capability` An editor opening the desk is sent to the studio `src: User flow, An editor or admin opening`
- [ ] `C-UF-07` `capability` A signed in producer opening sign in is sent to the desk `src: User flow, A signed in producer opening`
- [ ] `C-UF-08` `capability` Journey one opens Rally from the reel, then returns with Escape `src: User flow, Into the work`
- [ ] `C-UF-09` `capability` Journey two stars three projects, reorders the reel, annotates a row `src: User flow, Star, order and annotate`
- [ ] `C-UF-10` `capability` Journey three sends the reel as a pitch landing on the pitch page `src: User flow, Pitch`
- [ ] `C-UF-11` `capability` Journey four delivers the editor reply to the producer `src: User flow, The studio answers`
- [ ] `C-UF-12` `capability` Journey five shuts the second producer out of the seeded reel `src: User flow, Shut out`
- [ ] `C-UF-13` `capability` Journey six keeps the entry usable with no render context `src: User flow, No scene`
- [ ] `C-UF-14` `ui` An error page keeps the chrome on screen `src: User flow, the chrome and the environment stay through every failure`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` Interface controls composite onto the scene with no opaque panel `src: UI/UX notes, There is no page ground and no panel`
- [ ] `C-UX-02` `ui` Teal marks live or active state as one of two saturated colours `src: UI/UX notes, Exactly two saturated colours exist and both mean state`
- [ ] `C-UX-03` `constraint` No red appears in an error `src: UI/UX notes, There is no red anywhere`
- [ ] `C-UX-04` `ui` Interface text uses one monospaced grotesque family rendered upper case `src: UI/UX notes, One monospaced grotesque family in three cuts`
- [ ] `C-UX-05` `constraint` Interface text follows the exact type scale for intent list, metadata line, project title `src: UI/UX notes, The scale is exact`
- [ ] `C-UX-06` `ui` State changes move on one curve that front-loads motion before a long settle `src: UI/UX notes, Motion character is`
- [ ] `C-UX-07` `ui` Every interactive element shows a visible teal focus ring `src: UI/UX notes, Every interactive element shows a visible focus ring in the live teal`
- [ ] `C-UX-08` `constraint` On a phone the ticker is hidden `src: UI/UX notes, On a phone the ticker and its controls are hidden`
- [ ] `C-UX-09` `constraint` The frame never scrolls sideways at any width `src: UI/UX notes, never scrolls sideways`
- [ ] `C-UX-10` `constraint` No floating toast appears `src: UI/UX notes, a floating toast sliding in from a corner`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` The chrome capsule holds WORK beside CONTACT `src: Front-end specification, The chrome capsule contains`
- [ ] `C-FE-02` `ui` The chrome capsule glow takes colour from the environment behind `src: Front-end specification, The capsule carries a soft outer glow whose colour comes from the environment behind it`
- [ ] `C-FE-03` `constraint` The ticker controls are labelled Previous track, Next track `src: Front-end specification, they are drawn as double chevrons and labelled`
- [ ] `C-FE-04` `ui` The loading field resolves from forward slashes into digits beside a counter `src: Front-end specification, The loading field`
- [ ] `C-FE-05` `ui` A desk row carries a drag handle, a note field, a remove control `src: Front-end specification, On the desk a row adds a drag handle at its left`
- [ ] `C-FE-06` `ui` The typing indicator is three dots pulsing in turn `src: Front-end specification, The typing indicator is the`
- [ ] `C-FE-07` `ui` Form fields are drawn as lines rather than boxes `src: Front-end specification, Fields are lines, not boxes`
- [ ] `C-FE-08` `ui` A saved change confirms inline under the control that caused the change `src: Front-end specification, an inline confirmation under the control that caused it`
- [ ] `C-FE-09` `ui` The studio mark renders as a lit three-dimensional ring form with spectral colour `src: Front-end specification, The studio mark`
- [ ] `C-FE-10` `constraint` Marks are drawn inline with no bitmap fetched `src: Front-end specification, No bitmap and no vector file is fetched for any of them`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` GET of the health route returns 200 once the app is ready `src: Technical requirements, returns`
- [ ] `C-TR-02` `contract` The API authenticates a bearer access token `src: Technical requirements, issuing a bearer token sent as`
- [ ] `C-TR-03` `constraint` A state-changing cookie request lacking the request token is refused `src: Technical requirements, every state-changing request made with it carries a request token`
- [ ] `C-TR-04` `capability` A signed in web session survives a reload `src: Technical requirements, a session on one must still survive a reload`
- [ ] `C-TR-05` `data` Each public address carries the exact title in the served HTML `src: Technical requirements, The titles are exactly`
- [ ] `C-TR-06` `data` No two public addresses share a title or description `src: Technical requirements, No two of those addresses share a title or a description`
- [ ] `C-TR-07` `capability` The social preview image is generated on request as PNG or SVG `src: Technical requirements, whose preview image the server generates on request`
- [ ] `C-TR-08` `data` The reel address with query parameters carries the reel head `src: Technical requirements, with query parameters carries the same head as`
- [ ] `C-TR-09` `constraint` A share address for a token that is not current answers not found at the document level `src: Technical requirements, for a token that is not current`
- [ ] `C-TR-10` `contract` An unknown API path answers not found in JSON `src: Technical requirements, The API under`
- [ ] `C-TR-11` `contract` Every API error carries code, message, field, version, current `src: Technical requirements, Every error from`
- [ ] `C-TR-12` `contract` Error codes map to fixed statuses `src: Technical requirements, The codes and their statuses are`
- [ ] `C-TR-13` `constraint` A wrong-shape id answers not found, never a parse error `src: Technical requirements, An id of the wrong shape is`
- [ ] `C-TR-14` `constraint` A failed operation leaves no partial state `src: Technical requirements, A failed operation leaves no partial state`
- [ ] `C-TR-15` `constraint` Simultaneous reel writes on one version accept one write `src: Technical requirements, When two writes carrying the same version reach the same reel at the same instant`
- [ ] `C-TR-16` `constraint` Simultaneous submissions refuse the loser with a conflict, creating no second pitch `src: Technical requirements, When two submissions of one draft reel arrive at the same instant`
- [ ] `C-TR-17` `constraint` Simultaneous admin demotions never leave zero admins `src: Technical requirements, the product never has zero admins`
- [ ] `C-TR-18` `constraint` The sign in failure count is exact however attempts interleave `src: Technical requirements, The sign-in failure count for one email is exact however the attempts interleave`
- [ ] `C-TR-19` `contract` Every rate limit answers 429 with code rate_limited `src: Technical requirements, Every limit answers`
- [ ] `C-TR-20` `constraint` A project link lacking an http or https scheme with a host is refused with the project link message `src: Technical requirements, A project link is accepted only as`
- [ ] `C-TR-21` `data` The events route stores an event only when exempt or accepted, answering stored `src: Technical requirements, It is stored only when its name is`
- [ ] `C-TR-22` `constraint` An event property outside the event list is refused `src: Technical requirements, a property outside the event's own list below is rejected with`
- [ ] `C-TR-23` `contract` The assistant route answers a text/plain body `src: Technical requirements, is the one streaming response`

## C-DM Data model

- [ ] `C-DM-01` `literal` Every seeded account uses the password `deku-demo-pw-2026` `src: Data model, Every seeded account uses the password`
- [ ] `C-DM-02` `constraint` A password is never stored readable `src: Data model, A password is never stored in readable form`
- [ ] `C-DM-03` `data` Five categories are seeded `src: Data model, Seeded`
- [ ] `C-DM-04` `data` Sixteen projects are seeded `src: Data model, Seeded projects`
- [ ] `C-DM-05` `literal` The default visitor order opens `Secret Tide`, `Tidal Cartography`, `Harmonic Drift` `src: Data model, With the default sort a visitor's`
- [ ] `C-DM-06` `data` An editor receives Lantern Protocol first with total sixteen `src: Data model, An editor or admin also receives`
- [ ] `C-DM-07` `data` A project summary carries state only for staff `src: Data model, carries`
- [ ] `C-DM-08` `data` Rally carries tint warm-amber, key light upper-right, scene seed 4107 `src: Data model, rally`
- [ ] `C-DM-09` `data` Each track source reads generated followed by the kebab title `src: Data model, each with`
- [ ] `C-DM-10` `data` A reel holds no project twice `src: Data model, unique on`
- [ ] `C-DM-11` `data` An item available flag derives from the project being published `src: Data model, is derived on read from its project being published`
- [ ] `C-DM-12` `literal` The seeded reel `Launch shortlist` holds rally, eden, glass-planes `src: Data model, One reel`
- [ ] `C-DM-13` `literal` The seeded rally note reads `The sync across devices is the part to show` `src: Data model, at position 1 with the note`
- [ ] `C-DM-14` `literal` The seeded pitch `PT-000001` is in conversation `src: Data model, One pitch on it, reference`
- [ ] `C-DM-15` `constraint` The seeded pitch carries one studio message from the seeded editor thanking the producer for a good fit `src: Data model, with one message from`
- [ ] `C-DM-16` `constraint` Seeding twice duplicates no row `src: Data model, Seeding must be idempotent`
- [ ] `C-DM-17` `constraint` An assistant turn carries no account reference `src: Data model, it has no account reference of any kind`
- [ ] `C-DM-18` `data` A reel has at most one open pitch `src: Data model, A reel has at most one pitch whose state is`
- [ ] `C-DM-19` `data` A deleted reel keeps the row with a deletion time `src: Data model, deleted_at`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Nothing is fetched from any origin but the app's own `src: Constraints, Nothing is fetched from any origin but the app's own`
- [ ] `C-CN-02` `constraint` No dropdown appears `src: Constraints, no dropdown`
- [ ] `C-CN-03` `constraint` The app stays responsive with a producer holding ten reels `src: Constraints, a producer holding ten reels of fifteen items each`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at APP_PUBLIC_URL `src: Deployment contract, The app must be reachable at`
- [ ] `C-DC-02` `contract` The API is served under the api prefix on the same origin `src: Deployment contract, The HTTP API is served on that same origin under the`
- [ ] `C-DC-03` `contract` The health route returns 200 once ready `src: Deployment contract, returns`
- [ ] `C-DC-04` `contract` The server binds all interfaces `src: Deployment contract, Bind`
- [ ] `C-DC-05` `contract` The server keeps running after the session that started the server ends `src: Deployment contract, The server must keep running after this session ends`
- [ ] `C-DC-06` `constraint` A production build is served, never a dev server `src: Deployment contract, Serve a production build behind a static or preview server, never a dev server`
- [ ] `C-DC-07` `contract` Sign in returns the account with an access token `src: Deployment contract, Bearer auth is required on every endpoint except`
- [ ] `C-DC-08` `contract` A reel is returned with items in position order `src: Deployment contract, with`
- [ ] `C-DC-09` `contract` A pitch carries items with excluded as title lists `src: Deployment contract, where`
- [ ] `C-DC-10` `contract` The me route returns reel counts with pitch counts `src: Deployment contract, GET /api/me`
- [ ] `C-DC-11` `contract` List endpoints return rows under items `src: Deployment contract, List endpoints return their rows under`
- [ ] `C-DC-12` `contract` An invalid or unauthorized call is a client error, never 5xx `src: Deployment contract, an invalid or unauthorized call is rejected as a client error`
- [ ] `C-DC-13` `constraint` Every confirmation, reset, pitch or enquiry mail exists as a real Mailpit message `src: Deployment contract, A confirmation, reset, pitch or enquiry mail must exist as a real message in Mailpit`
- [ ] `C-DC-14` `contract` DELETE requests carry the version as a query parameter `src: Deployment contract, query`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `admin@example.com` | the seeded admin | `C-RL-16` |
| `editor@example.com` | the seeded editor | `C-RL-17` |
| `producer@example.com` | the seeded producer | `C-RL-18` |
| `producer2@example.com` | the second seeded producer | `C-RL-19` |
| `Northlight Agency` | the seeded producer's organisation | `C-RL-20` |
| `Farrow Kiln` | the second producer's organisation | `C-RL-21` |
| `Running without the full scene.` | the no render context banner | `C-CF-11` |
| `What are you looking for?` | the entry question | `C-CF-13` |
| `-> games` | the first intent link | `C-CF-14` |
| `-> multiplayer` | the second intent link | `C-CF-14` |
| `-> XR / VR / AI` | the third intent link | `C-CF-14` |
| `-> installations` | the fourth intent link | `C-CF-14` |
| `-> websites` | the fifth intent link | `C-CF-14` |
| `category=games&year=2021&year=2022` | the worked filter | `C-CF-31` |
| `Welcome to Stonehall` | the first worked filter result | `C-CF-31` |
| `20 Years of Nexus` | the second worked filter result | `C-CF-31` |
| `Discover your Familiar` | the third worked filter result | `C-CF-31` |
| `80` | the longest search | `C-CF-41` |
| `Nothing matches that.` | the empty filter line | `C-CF-44` |
| `Clear filters` | the clear control | `C-CF-44` |
| `2021 / U.S. Skyforce / xr` | the E.D.E.N. metadata line | `C-CF-48` |
| `2014 / Nimbus / installation` | the Rally metadata line | `C-CF-49` |
| `We cannot find that.` | the not-found line | `C-CF-55` |
| `That is not yours to open.` | the forbidden desk line | `C-CF-57` |
| `hello@example.com` | the studio address | `C-CF-59` |
| `company_website` | the enquiry decoy field | `C-CF-63` |
| `ASK ME ANYTHING...` | the resting assistant input | `C-CF-67` |
| `Slow Current--Halcyon Works` | the ticker template | `C-CF-84` |
| `Our site uses essential cookies and, with your consent, analytics cookies. Details in` | the consent sentence | `C-CF-86` |
| `Accept Cookies` | the accept capsule | `C-CF-87` |
| `Reject Cookies` | the reject capsule | `C-CF-87` |
| `That email already has an account.` | the taken email message | `C-CF-97` |
| `That link has expired. Ask for a new one.` | the expired link message | `C-CF-101` |
| `That email and password do not match.` | the sign in failure message | `C-CF-106` |
| `If that address has an account, a reset link is on its way.` | the reset message | `C-CF-109` |
| `JR_00` | the empty account capsule | `C-CF-115` |
| `You cannot change your own role.` | the own role message | `C-CF-117` |
| `The last owner cannot be demoted.` | the last admin message | `C-CF-118` |
| `You have ten reels. Rename or delete one.` | the reel limit message | `C-CF-123` |
| `That project is already on this reel.` | the duplicate item message | `C-CF-126` |
| `A reel holds every project there is. Remove one to add another.` | the item limit message | `C-CF-127` |
| `The order must list every project on this reel exactly once.` | the reorder message | `C-CF-129` |
| `A note holds up to five hundred characters.` | the note length message | `C-CF-130` |
| `Type the reel title to delete it.` | the delete confirmation message | `C-CF-140` |
| `Withdraw the pitch before deleting this reel.` | the open pitch delete message | `C-CF-142` |
| `This reel has been sent. Withdraw the pitch to change it.` | the submitted reel message | `C-CF-143` |
| `Choose a budget band.` | the budget message | `C-CF-147` |
| `under-50k` | the first budget band | `C-CF-148` |
| `50k-100k` | the second budget band | `C-CF-148` |
| `100k-250k` | the third budget band | `C-CF-148` |
| `250k-500k` | the fourth budget band | `C-CF-148` |
| `500k-plus` | the fifth budget band | `C-CF-148` |
| `this-month` | the first timing | `C-CF-149` |
| `next-quarter` | the second timing | `C-CF-149` |
| `this-year` | the third timing | `C-CF-149` |
| `exploring` | the fourth timing | `C-CF-149` |
| `Add a project before sending this reel.` | the empty pitch message | `C-CF-150` |
| `Confirm your email to send a pitch.` | the unverified pitch message | `C-CF-151` |
| `You have five open pitches. We will get to them.` | the open pitch limit message | `C-CF-152` |
| `That change is not allowed for this pitch.` | the refused state change message | `C-CF-160` |
| `This pitch is closed to new messages.` | the closed pitch message | `C-CF-163` |
| `That is a lot of messages. Try again shortly.` | the message limit | `C-CF-167` |
| `Confirm your email` | the confirmation subject | `C-CF-173` |
| `Reset your password` | the reset subject | `C-CF-173` |
| `We have your pitch` | the pitch receipt subject | `C-CF-173` |
| `New pitch from` | the studio pitch subject | `C-CF-173` |
| `The studio replied` | the reply subject | `C-CF-173` |
| `Pitch withdrawn` | the withdrawal subject | `C-CF-173` |
| `Your enquiry` | the enquiry receipt subject | `C-CF-173` |
| `Enquiry from` | the studio enquiry subject | `C-CF-173` |
| `You are offline. Changes are held.` | the offline banner | `C-CF-176` |
| `A project link starts with http or https and names a host.` | the project link message | `C-TR-20` |
| `deku-demo-pw-2026` | the seeded password | `C-DM-01` |
| `Secret Tide` | the newest published project | `C-DM-05` |
| `Tidal Cartography` | the second newest project | `C-DM-05` |
| `Harmonic Drift` | the third newest project | `C-DM-05` |
| `Launch shortlist` | the seeded reel | `C-DM-12` |
| `The sync across devices is the part to show` | the seeded note | `C-DM-13` |
| `PT-000001` | the seeded pitch reference | `C-DM-14` |
| `Ask a question first.` | the empty question message | `C-CF-184` |
| `Thanks, this is a good fit. We will set up a call.` | the seeded studio message | `C-DM-15` |

### Referenced but not pinned

| Value | Item |
|---|---|
| the exact near-white, light neutral, teal, soft blue and near-black values, carried as roles | `C-UX-02` |
| the named open monospaced grotesque typeface, left to the build | `C-UX-04` |
| the signature easing curve and state change durations, carried by character | `C-UX-06` |
| the drag handle accessible label | `C-FE-05` |
| the search field accessible name | `C-CF-42` |

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 0 | 6 |
| User roles | 3 | 21 |
| Core features | 55 | 186 |
| User flow | 12 | 14 |
| UI/UX notes | 4 | 10 |
| Front-end specification | 7 | 10 |
| Technical requirements | 15 | 23 |
| Data model | 11 | 19 |
| Constraints | 0 | 3 |
| Deployment contract | 11 | 14 |
