# Checklist: Atelier Moreau

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 522
Unpinned values flagged: 2

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public portfolio plus the booking layer behind the portfolio. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app shows nine projects on the public site. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The app converts a visitor into a scoped enquiry without a signup. `src: Overview para 1`
- [ ] `C-OV-04` `capability` The app turns an enquiry into an agreed start date through a proposal. `src: Overview para 1`
- [ ] `C-OV-05` `role` The app lets a visitor with no account read the work, hold a window, send a brief. `src: Overview, three kinds of person`
- [ ] `C-OV-06` `role` The app lets a client follow an enquiry, reply, accept a start date. `src: Overview, three kinds of person`
- [ ] `C-OV-07` `role` The app gives the studio one account reading the pipeline, replying, proposing, declining, opening or closing windows. `src: Overview, three kinds of person`
- [ ] `C-OV-08` `ui` The app presents three public documents on alternating grounds under one fixed chrome. `src: Overview, information architecture`
- [ ] `C-OV-09` `ui` The app presents the operational half behind the sign-in in a quiet dense register. `src: Overview, information architecture`
- [ ] `C-OV-10` `constraint` The app takes no money at any point. `src: Overview, what the product is not`
- [ ] `C-OV-11` `constraint` The app accepts no attachment on any surface. `src: Overview, what the product is not`
- [ ] `C-OV-12` `contract` The app commits capacity at acceptance, never at hold. `src: Overview, the hard part`

## C-RL User roles

- [ ] `C-RL-01` `role` The app lets a client read every public route. `src: User roles table row 1`
- [ ] `C-RL-02` `role` The app lets a client hold an open window. `src: User roles table row 1`
- [ ] `C-RL-03` `role` The app lets a client submit an enquiry. `src: User roles table row 1`
- [ ] `C-RL-04` `role` The app lets a client read, reply on, accept a proposal on, withdraw their own enquiry. `src: User roles table row 1`
- [ ] `C-RL-05` `constraint` The app denies a client every read of an enquiry belonging to somebody else. `src: User roles table row 1`
- [ ] `C-RL-06` `constraint` The app denies a client the proposal of a start date. `src: User roles table row 1`
- [ ] `C-RL-07` `constraint` The app denies a client the decline of an enquiry. `src: User roles table row 1`
- [ ] `C-RL-08` `constraint` The app denies a client the creation, move or close of a window. `src: User roles table row 1`
- [ ] `C-RL-09` `constraint` The app denies a client every read of the pipeline plus the export. `src: User roles table row 1`
- [ ] `C-RL-10` `role` The app lets the studio read, reply on any enquiry. `src: User roles table row 2`
- [ ] `C-RL-11` `role` The app lets the studio propose a start date, decline an enquiry. `src: User roles table row 2`
- [ ] `C-RL-12` `role` The app lets the studio create, move, close a window. `src: User roles table row 2`
- [ ] `C-RL-13` `constraint` The app denies the studio the acceptance of a proposal on behalf of a client. `src: User roles table row 2`
- [ ] `C-RL-14` `constraint` The app denies the studio the withdrawal of a client's enquiry. `src: User roles table row 2`
- [ ] `C-RL-15` `contract` The app enforces authorization on the server for every mutating endpoint. `src: User roles, authorization paragraph`
- [ ] `C-RL-16` `constraint` The app leaves the protected state unchanged after denying an unauthorized request. `src: User roles, authorization paragraph`
- [ ] `C-RL-17` `capability` The app authenticates by email plus password on an account. `src: User roles, authentication paragraph`
- [ ] `C-RL-18` `capability` The app authenticates by a link for anybody without an account. `src: User roles, authentication paragraph`
- [ ] `C-RL-19` `contract` The app grants an anonymous visitor every public read, one hold, one enquiry submission. `src: User roles, capability matrix`
- [ ] `C-RL-20` `literal` The app holds an open window for an anonymous visitor for `72 hours`. `src: User roles, anonymous paragraph`
- [ ] `C-RL-21` `literal` The app grants an enquiry token read, reply, accept, withdraw on one enquiry for `90 days`. `src: User roles, anonymous paragraph`
- [ ] `C-RL-22` `constraint` The app puts no registration in front of the contact form. `src: User roles, anonymous paragraph`
- [ ] `C-RL-23` `constraint` The app never treats an enquiry token as a session, never gives a token a role. `src: User roles, the enquiry token`
- [ ] `C-RL-24` `constraint` The app opens one enquiry per token, nothing else. `src: User roles, the enquiry token`
- [ ] `C-RL-25` `data` The app stores a recovery address on the studio account distinct from the sign-in address. `src: User roles, the single-operator risk`
- [ ] `C-RL-26` `contract` The app addresses the enquiry notification to a second address that is not the studio account's. `src: User roles, the single-operator risk`
- [ ] `C-RL-27` `capability` The app exports the whole pipeline in one action. `src: User roles, the single-operator risk`
- [ ] `C-RL-28` `capability` The app opens signup to anyone. `src: User roles, signup paragraph`
- [ ] `C-RL-29` `literal` The app assigns the role `client` to every account created at signup. `src: User roles, signup paragraph`
- [ ] `C-RL-30` `constraint` The app carries exactly one `studio` account, created only by seed. `src: User roles, signup paragraph`
- [ ] `C-RL-31` `literal` The app seeds an account at `studio@example.com` named `Elian Moreau` at `Atelier Moreau`. `src: User roles, seeded accounts table`
- [ ] `C-RL-32` `literal` The app seeds an account at `client@example.com` named `Alex Renard` at `Northgate`. `src: User roles, seeded accounts table`
- [ ] `C-RL-33` `literal` The app accepts `deku-demo-pw-2026` at login for both seeded accounts. `src: User roles, seeded accounts password`

## C-CF Core features

- [ ] `C-CF-01` `contract` The app stores a password hashed. `src: Core features, Auth`
- [ ] `C-CF-02` `constraint` The app returns no password hash from any endpoint. `src: Core features, Auth`
- [ ] `C-CF-03` `contract` The app returns a bearer token on a successful login. `src: Core features, Auth`
- [ ] `C-CF-04` `literal` The app expires a bearer token after `24 hours`. `src: Core features, Auth`
- [ ] `C-CF-05` `constraint` The app rejects a signup whose email already has an account, naming the field at fault. `src: Core features rule 1`
- [ ] `C-CF-06` `constraint` The app writes no second account row for a rejected signup. `src: Core features rule 1`
- [ ] `C-CF-07` `constraint` The app ignores a role named in a signup request body. `src: Core features rule 2`
- [ ] `C-CF-08` `constraint` The app rejects a request carrying no token, an expired token or a tampered token. `src: Core features rule 3`
- [ ] `C-CF-09` `constraint` The app exempts signup, login, health, the public reads from the token requirement. `src: Core features rule 3`
- [ ] `C-CF-10` `contract` The app accepts every sign-in link request whether or not the address has an enquiry. `src: Core features rule 4`
- [ ] `C-CF-11` `literal` The app answers a sign-in link request `If that address has an enquiry with us, a sign-in link is on its way.` `src: Core features rule 4`
- [ ] `C-CF-12` `constraint` The app reveals nothing about who has written in through the sign-in link endpoint. `src: Core features rule 4`
- [ ] `C-CF-13` `ui` The app carries the hero, the about section, the selected-work preview on `/` in that order. `src: Core features rule 5`
- [ ] `C-CF-14` `ui` The app carries the nine-project index on `/work`. `src: Core features rule 5`
- [ ] `C-CF-15` `ui` The app carries the enquiry form on `/contact`. `src: Core features rule 5`
- [ ] `C-CF-16` `ui` The app carries the current state plus the open windows on `/availability`. `src: Core features rule 5`
- [ ] `C-CF-17` `contract` The app redirects `/work/` permanently to `/work`. `src: Core features rule 6`
- [ ] `C-CF-18` `ui` The app updates the fragment for `Home` plus `About`, the path for `Work` plus `Contact`. `src: Core features rule 7`
- [ ] `C-CF-19` `ui` The app scrolls an anchor reached on a cold load to the anchor's own position. `src: Core features rule 7`
- [ ] `C-CF-20` `ui` The app presents the chrome carrying the lockup, the pill, a sound control, four navigation targets on every public route. `src: Core features rule 8`
- [ ] `C-CF-21` `ui` The app reads `Sound | OFF` or `Sound | ON` on the sound control. `src: Core features rule 8`
- [ ] `C-CF-22` `ui` The app names a control reading `Sound | OFF` as `Turn sound on` for assistive technology. `src: Core features rule 9`
- [ ] `C-CF-23` `constraint` The app signals no state, confirmation or error by sound alone. `src: Core features rule 9`
- [ ] `C-CF-24` `data` The app seeds nine projects, each with a title, a discipline, a year, a slug, a position. `src: Core features rule 10`
- [ ] `C-CF-25` `ui` The app draws both project presentations from one record set. `src: Core features rule 10`
- [ ] `C-CF-26` `literal` The app reads the work index count as `(09)` with nine published projects. `src: Core features rule 11`
- [ ] `C-CF-27` `contract` The app resolves `/work/{slug}` to one project. `src: Core features rule 12`
- [ ] `C-CF-28` `contract` The app answers not-found for a slug with no project, rendering the product's own not-found surface. `src: Core features rule 12`
- [ ] `C-CF-29` `data` The app seeds three services, each a title plus a line. `src: Core features rule 13`
- [ ] `C-CF-30` `contract` The app computes the availability mode from the windows on every read. `src: Core features rule 14`
- [ ] `C-CF-31` `constraint` The app stores no typed availability mode, accepts a mode at no endpoint. `src: Core features rule 14`
- [ ] `C-CF-32` `literal` The app derives `open_now` when an `open` window starts within `14 days`. `src: Core features rule 14 mode table`
- [ ] `C-CF-33` `literal` The app reads `available now for work` in the pill under `open_now`. `src: Core features rule 14 mode table`
- [ ] `C-CF-34` `literal` The app derives `open_from` when an `open` window starts later, reading `available from` plus the month. `src: Core features rule 14 mode table`
- [ ] `C-CF-35` `literal` The app derives `booked_until` when every window is `booked` or `closed` with one `booked`, reading `booked until` plus the month. `src: Core features rule 14 mode table`
- [ ] `C-CF-36` `literal` The app derives `not_taking` when no window exists, reading `not taking new work`. `src: Core features rule 14 mode table`
- [ ] `C-CF-37` `contract` The app reads the same record for the pill plus the availability page. `src: Core features rule 15`
- [ ] `C-CF-38` `constraint` The app never renders a public route without the pill. `src: Core features rule 15`
- [ ] `C-CF-39` `constraint` The app carries the availability state in the pill's words, never in the dot's colour alone. `src: Core features rule 16`
- [ ] `C-CF-40` `capability` The app shows a free studio `note` on the availability page. `src: Core features rule 17`
- [ ] `C-CF-41` `constraint` The app never shows the studio `note` in the pill. `src: Core features rule 17`
- [ ] `C-CF-42` `ui` The app lists the next open windows on `/availability`, each with a start date, a length in weeks, a capacity in days per week. `src: Core features rule 18`
- [ ] `C-CF-43` `literal` The app offers a control reading `Start an enquiry` against a chosen window. `src: Core features rule 18`
- [ ] `C-CF-44` `data` The app stores a window as a start date, a length in `weeks`, a `capacity_days`, a `committed_days`. `src: Core features rule 19`
- [ ] `C-CF-45` `literal` The app bounds `capacity_days` between `1` plus `5`. `src: Core features rule 19`
- [ ] `C-CF-46` `literal` The app starts `committed_days` at `0`. `src: Core features rule 19`
- [ ] `C-CF-47` `literal` The app carries a window state of `open`, `held`, `booked` or `closed`. `src: Core features rule 19`
- [ ] `C-CF-48` `contract` The app creates a hold expiring after `72 hours` when a visitor presses the enquiry control against an open window. `src: Core features rule 20`
- [ ] `C-CF-49` `ui` The app opens the enquiry form with the held window named at the form's head. `src: Core features rule 20`
- [ ] `C-CF-50` `constraint` The app changes no `committed_days` when a hold is created. `src: Core features rule 21`
- [ ] `C-CF-51` `constraint` The app reduces nothing another visitor may be offered when a hold is created. `src: Core features rule 21`
- [ ] `C-CF-52` `literal` The app allows at most `3` live holds on one window. `src: Core features rule 22`
- [ ] `C-CF-53` `literal` The app refuses a fourth hold with the pinned nearly-full refusal copy. `src: Core features rule 22`
- [ ] `C-CF-54` `contract` The app still opens the enquiry form without a window after refusing a fourth hold. `src: Core features rule 22`
- [ ] `C-CF-55` `constraint` The app refuses a hold on a window that is not `open`, stating the reason under the control. `src: Core features rule 23`
- [ ] `C-CF-56` `constraint` The app refuses a hold on a window with no remaining capacity. `src: Core features rule 23`
- [ ] `C-CF-57` `contract` The app releases a hold immediately when the hold's enquiry is withdrawn. `src: Core features rule 24`
- [ ] `C-CF-58` `contract` The app releases a hold immediately when the studio closes the window the hold sits on. `src: Core features rule 24`
- [ ] `C-CF-59` `literal` The app keeps a hand-released hold undoable for ten seconds, asking for no confirmation first. `src: Core features rule 24`
- [ ] `C-CF-60` `ui` The app carries six numbered fields on the enquiry form, each a label over an underlined input. `src: Core features, the enquiry form`
- [ ] `C-CF-61` `literal` The app labels field one `My Name`, required, 1 to 80 characters. `src: Core features, the enquiry field table`
- [ ] `C-CF-62` `literal` The app refuses an empty name reading `We need something to call you.` `src: Core features, the enquiry field table`
- [ ] `C-CF-63` `literal` The app labels field two `My Email`, required, a valid address. `src: Core features, the enquiry field table`
- [ ] `C-CF-64` `literal` The app refuses a missing address reading `We need an address to reply to.` `src: Core features, the enquiry field table`
- [ ] `C-CF-65` `literal` The app labels field three `I work at`, optional, up to 120 characters. `src: Core features, the enquiry field table`
- [ ] `C-CF-66` `literal` The app refuses an over-long organisation reading `That is longer than we can store.` `src: Core features, the enquiry field table`
- [ ] `C-CF-67` `literal` The app labels field four `I am looking for`, required, 3 to 200 characters. `src: Core features, the enquiry field table`
- [ ] `C-CF-68` `literal` The app refuses a missing subject reading `A few words about what you need.` `src: Core features, the enquiry field table`
- [ ] `C-CF-69` `literal` The app labels field five `My budget is`, required, one of the four bands. `src: Core features, the enquiry field table`
- [ ] `C-CF-70` `literal` The app refuses a missing band reading `Choose a range, even a rough one.` `src: Core features, the enquiry field table`
- [ ] `C-CF-71` `literal` The app labels field six `My message`, required, 20 to 4000 characters. `src: Core features, the enquiry field table`
- [ ] `C-CF-72` `literal` The app refuses a short message reading `Tell us a little more, at least twenty characters.` `src: Core features, the enquiry field table`
- [ ] `C-CF-73` `literal` The app offers the largest pinned budget band as the first option. `src: Core features rule 25`
- [ ] `C-CF-74` `literal` The app offers the band `USD $10001-$20000` as the second option. `src: Core features rule 25`
- [ ] `C-CF-75` `literal` The app offers the band `USD $5001-$10000` as the third option. `src: Core features rule 25`
- [ ] `C-CF-76` `literal` The app offers the band `USD $2000-$5000` as the fourth option. `src: Core features rule 25`
- [ ] `C-CF-77` `constraint` The app names the currency on every budget band. `src: Core features rule 25`
- [ ] `C-CF-78` `constraint` The app offers no band below the lowest, keeping the floor where the floor is. `src: Core features rule 26`
- [ ] `C-CF-79` `literal` The app sits the pinned smaller-budget line under the band select. `src: Core features rule 26`
- [ ] `C-CF-80` `literal` The app reads the pinned submit copy on the submit control. `src: Core features rule 27`
- [ ] `C-CF-81` `contract` The app runs field validation on blur, never on keystroke. `src: Core features rule 28`
- [ ] `C-CF-82` `contract` The app re-validates a failed field on keystroke until the field passes. `src: Core features rule 28`
- [ ] `C-CF-83` `contract` The app re-validates the whole form on submit. `src: Core features rule 28`
- [ ] `C-CF-84` `constraint` The app writes nothing for a rejected field, leaving every other answer as the visitor typed. `src: Core features rule 28`
- [ ] `C-CF-85` `ui` The app sits a privacy link beside the submit control. `src: Core features rule 29`
- [ ] `C-CF-86` `contract` The app creates an enquiry in state `new` linked to the held window on submit. `src: Core features rule 30`
- [ ] `C-CF-87` `literal` The app issues an opaque enquiry `token` valid for `90 days`. `src: Core features rule 30`
- [ ] `C-CF-88` `contract` The app lands the visitor on `/enquiry/{id}` carrying the enquiry token. `src: Core features rule 30`
- [ ] `C-CF-89` `contract` The app accepts an enquiry without a window when the hold expired during writing, saying so. `src: Core features rule 31`
- [ ] `C-CF-90` `literal` The app shows the pinned lapsed-hold message when a hold lapses during writing. `src: Core features rule 31`
- [ ] `C-CF-91` `contract` The app keeps every typed answer when a hold lapses during writing. `src: Core features rule 31`
- [ ] `C-CF-92` `contract` The app rate limits the enquiry form per address, naming the wait in words. `src: Core features rule 32`
- [ ] `C-CF-93` `contract` The app holds a submission carrying a spam signal for studio review rather than dropping the submission silently. `src: Core features rule 32`
- [ ] `C-CF-94` `contract` The app moves an enquiry from `new` to `reading` when the studio opens the enquiry. `src: Core features rule 33`
- [ ] `C-CF-95` `ui` The app shows the reading state on the client's own enquiry page. `src: Core features rule 33`
- [ ] `C-CF-96` `contract` The app creates a message on a reply from either side, mailing the other side. `src: Core features rule 34`
- [ ] `C-CF-97` `constraint` The app changes no enquiry state on a reply. `src: Core features rule 34`
- [ ] `C-CF-98` `contract` The app takes a start date, a length in weeks, a capacity in days per week, a free note on a proposal. `src: Core features rule 35`
- [ ] `C-CF-99` `constraint` The app refuses a proposal whose dates fall outside the enquiry's window. `src: Core features rule 35`
- [ ] `C-CF-100` `constraint` The app refuses a proposal whose days per week exceed what the window has left. `src: Core features rule 35`
- [ ] `C-CF-101` `contract` The app moves an enquiry to `proposed`, extends the hold to the proposal's expiry, mails the client. `src: Core features rule 35`
- [ ] `C-CF-102` `constraint` The app keeps at most one `live` proposal per enquiry. `src: Core features rule 36`
- [ ] `C-CF-103` `contract` The app supersedes the previous proposal when the studio proposes again. `src: Core features rule 36`
- [ ] `C-CF-104` `contract` The app writes a booking, moves the enquiry to `booked` when the client or the token holder accepts. `src: Core features rule 37`
- [ ] `C-CF-105` `contract` The app raises the window's `committed_days` by the proposal's days per week at acceptance. `src: Core features rule 37`
- [ ] `C-CF-106` `contract` The app moves a window to `booked` once the window is full. `src: Core features rule 37`
- [ ] `C-CF-107` `contract` The app resolves two acceptances against the last remaining capacity of one window to exactly one booking. `src: Core features rule 38`
- [ ] `C-CF-108` `constraint` The app never lets `committed_days` pass `capacity_days`. `src: Core features rule 38`
- [ ] `C-CF-109` `constraint` The app leaves no partial booking behind after a refused acceptance. `src: Core features rule 38`
- [ ] `C-CF-110` `literal` The app refuses the losing acceptance reading `That window filled up. Here is what is open.` `src: Core features rule 38`
- [ ] `C-CF-111` `contract` The app carries the open windows with a refused acceptance. `src: Core features rule 38`
- [ ] `C-CF-112` `literal` The app refuses acceptance of an expired proposal reading `That proposal has expired. Ask for a new one.` `src: Core features rule 39`
- [ ] `C-CF-113` `ui` The app offers a control asking for a new proposal after refusing an expired one. `src: Core features rule 39`
- [ ] `C-CF-114` `contract` The app moves an enquiry to `withdrawn`, releases the hold when the client or the token holder withdraws. `src: Core features rule 40`
- [ ] `C-CF-115` `constraint` The app deletes nothing on a withdrawal. `src: Core features rule 40`
- [ ] `C-CF-116` `contract` The app moves an enquiry to `declined`, always mails the client when the studio declines. `src: Core features rule 41`
- [ ] `C-CF-117` `constraint` The app offers no silent decline. `src: Core features rule 41`
- [ ] `C-CF-118` `literal` The app moves an enquiry with no reply for `30 days` to `lapsed`, releasing the hold. `src: Core features rule 42`
- [ ] `C-CF-119` `constraint` The app mails nobody about a lapsed enquiry. `src: Core features rule 42`
- [ ] `C-CF-120` `constraint` The app never deletes an enquiry, carrying `withdrawn`, `declined`, `lapsed` as states. `src: Core features rule 43`
- [ ] `C-CF-121` `contract` The app re-derives the availability mode on the next read after a booking. `src: Core features rule 44`
- [ ] `C-CF-122` `ui` The app lays the pipeline out as a calendar grid by window, by state on `/studio/pipeline`. `src: Core features rule 45`
- [ ] `C-CF-123` `contract` The app orders enquiries newest first within each pipeline state. `src: Core features rule 45`
- [ ] `C-CF-124` `capability` The app filters the pipeline by state, by budget band. `src: Core features rule 46`
- [ ] `C-CF-125` `contract` The app carries the current pipeline filter in the address so a filtered view can be shared. `src: Core features rule 46`
- [ ] `C-CF-126` `contract` The app returns every enquiry, message, proposal, booking, window in one export response. `src: Core features rule 47`
- [ ] `C-CF-127` `constraint` The app serves the export to the studio alone. `src: Core features rule 47`
- [ ] `C-CF-128` `contract` The app sends mail over real SMTP, reading the host, the port, the user, the password from the environment. `src: Core features, transactional mail preamble`
- [ ] `C-CF-129` `constraint` The app writes every message as plain text carrying one primary link. `src: Core features, transactional mail preamble`
- [ ] `C-CF-130` `contract` The app states at each message's foot which address the message went to, why. `src: Core features, transactional mail preamble`
- [ ] `C-CF-131` `literal` The app mails the sender a message whose subject begins `We have your enquiry` on submission. `src: Core features rule 48 mail table`
- [ ] `C-CF-132` `literal` The app mails the studio a message whose subject begins `New enquiry` on submission. `src: Core features rule 48 mail table`
- [ ] `C-CF-133` `literal` The app mails the sender a message whose subject begins `A reply to your enquiry` when the studio replies. `src: Core features rule 48 mail table`
- [ ] `C-CF-134` `literal` The app mails the studio a message whose subject begins `A reply from` when the client replies. `src: Core features rule 48 mail table`
- [ ] `C-CF-135` `literal` The app mails the client a message whose subject begins `A start date for your project` when a proposal is sent. `src: Core features rule 48 mail table`
- [ ] `C-CF-136` `literal` The app mails the client a message whose subject begins `Booked` when a proposal is accepted. `src: Core features rule 48 mail table`
- [ ] `C-CF-137` `literal` The app mails the studio a message whose subject begins `Booked` when a proposal is accepted. `src: Core features rule 48 mail table`
- [ ] `C-CF-138` `literal` The app mails the client once a message whose subject begins `Your start date offer expires soon` within `48 hours` of expiry. `src: Core features rule 48 mail table`
- [ ] `C-CF-139` `literal` The app mails the client a message whose subject begins `About your enquiry` on a decline. `src: Core features rule 48 mail table`
- [ ] `C-CF-140` `literal` The app mails the requesting address a message whose subject begins `Your sign-in link` on a link request. `src: Core features rule 48 mail table`
- [ ] `C-CF-141` `constraint` The app addresses every message to exactly the named recipient, with no cc, no bcc. `src: Core features rule 48`
- [ ] `C-CF-142` `contract` The app follows the enquiry confirmation subject with a space plus the enquiry id. `src: Core features rule 48 worked example`
- [ ] `C-CF-143` `contract` The app carries the sender's own six answers back in the confirmation, as submitted. `src: Core features rule 49`
- [ ] `C-CF-144` `contract` The app sends mail after the state change commits. `src: Core features rule 50`
- [ ] `C-CF-145` `constraint` The app never fails an action because mail failed. `src: Core features rule 50`
- [ ] `C-CF-146` `ui` The app flags a mail failure on the studio's pipeline with a control sending the message again. `src: Core features rule 50`
- [ ] `C-CF-147` `constraint` The app sends no mail when an enquiry lapses, when a hold expires, when the studio reads an enquiry. `src: Core features rule 51`
- [ ] `C-CF-148` `constraint` The app sends no mail on creating or closing a window. `src: Core features rule 51`
- [ ] `C-CF-149` `constraint` The app sends no follow-up chasing an unanswered enquiry, no newsletter, no marketing of any kind. `src: Core features rule 51`
- [ ] `C-CF-150` `ui` The app carries a full-width band under the chrome holding something true right now, staying until the condition clears. `src: Core features rule 52`
- [ ] `C-CF-151` `ui` The app carries an inline confirmation under the control that caused the confirmation, for about two seconds. `src: Core features rule 52`
- [ ] `C-CF-152` `ui` The app carries an action band above the control that failed, staying until dismissal or a retry. `src: Core features rule 52`
- [ ] `C-CF-153` `constraint` The app offers three notification surfaces, no others. `src: Core features rule 52`
- [ ] `C-CF-154` `contract` The app shows one band at a time, the highest ranked band winning. `src: Core features rule 53`
- [ ] `C-CF-155` `literal` The app ranks the bands offline, a lapsed hold, a proposal awaiting the visitor, a proposal expiring within `48 hours`, the studio has replied. `src: Core features rule 53`
- [ ] `C-CF-156` `contract` The app states what the enquiry form stores, how long an enquiry is kept, how long a booking is kept on `/legal/privacy`. `src: Core features rule 54`
- [ ] `C-CF-157` `ui` The app links the privacy route from the footer of every public route. `src: Core features rule 54`
- [ ] `C-CF-158` `contract` The app states the terms of use on `/legal/terms`, linked from the footer of every public route. `src: Core features rule 55`
- [ ] `C-CF-159` `ui` The app asks a first-time visitor once about non-essential cookies. `src: Core features rule 56`
- [ ] `C-CF-160` `contract` The app survives a reload with the cookie answer intact. `src: Core features rule 56`
- [ ] `C-CF-161` `constraint` The app records a page view only when the cookie answer was yes. `src: Core features rule 56`
- [ ] `C-CF-162` `data` The app records the route, the time on a page view, nothing about the person. `src: Core features rule 56`
- [ ] `C-CF-163` `contract` The app declares a social preview title, an image on every public route. `src: Core features rule 57`
- [ ] `C-CF-164` `constraint` The app declares no duplicate social preview pair across two routes. `src: Core features rule 57`
- [ ] `C-CF-165` `contract` The app resolves every declared social preview image. `src: Core features rule 57`
- [ ] `C-CF-166` `constraint` The app offers no search on the work index. `src: Core features rule 58`
- [ ] `C-CF-167` `capability` The app matches a pipeline search against the enquiry's name, organisation, subject line. `src: Core features rule 58`
- [ ] `C-CF-168` `contract` The app applies a pipeline search on top of the state filter, the band filter. `src: Core features rule 58`
- [ ] `C-CF-169` `contract` The app sorts the pipeline newest first by default. `src: Core features rule 59`
- [ ] `C-CF-170` `capability` The app sorts the pipeline by budget band, largest band first. `src: Core features rule 59`
- [ ] `C-CF-171` `ui` The app shows a reply in the thread the moment the reply is sent, before the server confirms. `src: Core features rule 60`
- [ ] `C-CF-172` `ui` The app rolls a failed reply back with a message above the control. `src: Core features rule 60`
- [ ] `C-CF-173` `constraint` The app makes a hold, a proposal, an acceptance each wait for the server. `src: Core features rule 60`
- [ ] `C-CF-174` `ui` The app shows on the client's own page that an enquiry open in the studio's pipeline is being read. `src: Core features rule 61`
- [ ] `C-CF-175` `constraint` The app shows no cursor position, no typing indicator, no last-seen time to anybody. `src: Core features rule 61`
- [ ] `C-CF-176` `contract` The app reaches an already-open enquiry page with the other side's change within a few seconds, without a reload. `src: Core features rule 62`
- [ ] `C-CF-177` `literal` The app renders the studio's local time in the footer as a twelve-hour clock naming the offset. `src: Core features rule 63`
- [ ] `C-CF-178` `constraint` The app ships in one language, untranslated. `src: Core features rule 63`
- [ ] `C-CF-179` `literal` The app writes a date as a day, a month name, a year. `src: Core features rule 64`
- [ ] `C-CF-180` `contract` The app writes a window's length in weeks, a window's capacity in days per week. `src: Core features rule 64`
- [ ] `C-CF-181` `contract` The app writes a budget band exactly as the band's option reads, currency included. `src: Core features rule 64`
- [ ] `C-CF-182` `contract` The app renders a timestamp shown to a client in that client's own timezone. `src: Core features rule 64`
- [ ] `C-CF-183` `contract` The app renders a timestamp shown to the studio in the studio's timezone. `src: Core features rule 64`
- [ ] `C-CF-184` `data` The app records an availability view carrying the count of open windows. `src: Core features rule 65`
- [ ] `C-CF-185` `data` The app records a hold created carrying the window, the days until the window starts. `src: Core features rule 65`
- [ ] `C-CF-186` `data` The app records an enquiry submitted carrying the budget band, whether the enquiry had a window, the message length. `src: Core features rule 65`
- [ ] `C-CF-187` `data` The app records an enquiry abandoned carrying the furthest field reached, for a draft thirty days old, unsent. `src: Core features rule 65`
- [ ] `C-CF-188` `data` The app records a proposal sent carrying the days since the enquiry. `src: Core features rule 65`
- [ ] `C-CF-189` `data` The app records a proposal accepted carrying the days since the proposal. `src: Core features rule 65`
- [ ] `C-CF-190` `data` The app records the moving ground degrading carrying the stage the ground fell back to. `src: Core features rule 65`
- [ ] `C-CF-191` `constraint` The app records seven events, no others. `src: Core features rule 65`
- [ ] `C-CF-192` `constraint` The app puts no name, no address, no employer, no message body on any recorded event. `src: Core features rule 65`
- [ ] `C-CF-193` `capability` The app lets the studio read how many arrived, how many started an enquiry, how many finished, how many became a booking. `src: Core features rule 66`
- [ ] `C-CF-194` `constraint` The app records nothing at all until the cookie answer is yes. `src: Core features rule 67`
- [ ] `C-CF-195` `contract` The app stops recording from the next page onward when the cookie answer is revoked. `src: Core features rule 67`

## C-UF User flow

- [ ] `C-UF-01` `ui` The app serves the home document carrying the hero, the about section, selected work at `/`. `src: User flow route table`
- [ ] `C-UF-02` `ui` The app serves the nine-project index at `/work`, one project at `/work/{slug}`. `src: User flow route table`
- [ ] `C-UF-03` `ui` The app serves the six-field enquiry form at `/contact`. `src: User flow route table`
- [ ] `C-UF-04` `ui` The app serves the current state plus the open windows at `/availability`. `src: User flow route table`
- [ ] `C-UF-05` `ui` The app serves a sign-in request surface at `/signin`, the client's own enquiries plus bookings at `/account`. `src: User flow route table`
- [ ] `C-UF-06` `ui` The app serves one enquiry plus the enquiry's thread at `/enquiry/{id}`. `src: User flow route table`
- [ ] `C-UF-07` `ui` The app serves the studio's home at `/studio`, the calendar grid at `/studio/pipeline`. `src: User flow route table`
- [ ] `C-UF-08` `contract` The app sends an unauthenticated request for a private route to `/signin` with the destination remembered. `src: User flow, entry and redirects`
- [ ] `C-UF-09` `constraint` The app honours a remembered destination only when the destination is a path on the app's own origin beginning with a single slash. `src: User flow, entry and redirects`
- [ ] `C-UF-10` `contract` The app gives a client reaching a studio route the denied surface, not a redirect. `src: User flow, entry and redirects`
- [ ] `C-UF-11` `contract` The app sends a studio session reaching `/account` to `/studio`. `src: User flow, entry and redirects`
- [ ] `C-UF-12` `contract` The app opens `/enquiry/{id}` for the token, the owner, the studio. `src: User flow, entry and redirects`
- [ ] `C-UF-13` `constraint` The app renders a denied surface that is byte-identical whether the enquiry exists or not. `src: User flow, entry and redirects`
- [ ] `C-UF-14` `ui` The app renders a distinct expired-link surface with a control asking for another link. `src: User flow, entry and redirects`
- [ ] `C-UF-15` `contract` The app returns to `/` on sign-out, leaving the previous private route unreachable by going back. `src: User flow, entry and redirects`
- [ ] `C-UF-16` `ui` The app slides the lockup in from the left, arrives the pill from the upper left on load. `src: User flow journey 1`
- [ ] `C-UF-17` `ui` The app slides the pale about sheet up over the dark hero under scroll. `src: User flow journey 1`
- [ ] `C-UF-18` `ui` The app shows the current state at display size on `/availability`. `src: User flow journey 2`
- [ ] `C-UF-19` `ui` The app explains what a window means under the listed windows. `src: User flow journey 2`
- [ ] `C-UF-20` `capability` The app walks a visitor from an open window through six fields to a submitted enquiry. `src: User flow journey 3`
- [ ] `C-UF-21` `capability` The app walks the studio from the pipeline through a reply to a proposal. `src: User flow journey 4`
- [ ] `C-UF-22` `ui` The app shows the window's remaining capacity live above the proposal fields. `src: User flow journey 4`
- [ ] `C-UF-23` `capability` The app books the enquiry when the client accepts, raising the window's committed days. `src: User flow journey 5`
- [ ] `C-UF-24` `contract` The app moves the pill to the booked form on the next read once no window remains open. `src: User flow journey 6`
- [ ] `C-UF-25` `contract` The app resolves two simultaneous acceptances against one last place to exactly one booking. `src: User flow journey 7`
- [ ] `C-UF-26` `contract` The app accepts the enquiry without a window after a hold lapses mid-writing, saying so. `src: User flow journey 8`
- [ ] `C-UF-27` `ui` The app shows a quiet placeholder in place during a surface load, rather than collapsing. `src: User flow, states`
- [ ] `C-UF-28` `ui` The app shows a working control on the control itself rather than blocking the page. `src: User flow, states`
- [ ] `C-UF-29` `literal` The app reads `An enquiry appears here once you send one.` for a client with no enquiries. `src: User flow, states`
- [ ] `C-UF-30` `literal` The app reads `The pipeline is clear.` for an empty pipeline. `src: User flow, states`
- [ ] `C-UF-31` `literal` The app reads `No projects listed.` for a work index with nothing published. `src: User flow, states`
- [ ] `C-UF-32` `literal` The app reads `That did not load.` with a control reading `Try again` on a failed read. `src: User flow, states`
- [ ] `C-UF-33` `literal` The app reads `That is not yours to open.` on a denied surface. `src: User flow, states`
- [ ] `C-UF-34` `literal` The app reads `We cannot find that.` on a missing surface. `src: User flow, states`
- [ ] `C-UF-35` `literal` The app reads `You are offline. Your draft is safe.` for a visitor with no connection. `src: User flow, states`
- [ ] `C-UF-36` `contract` The app survives a reload with the enquiry draft intact in the same browser. `src: User flow, states`
- [ ] `C-UF-37` `constraint` The app shows no blank screen, no unhandled error on any route. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The app makes the first screen read as one person's craft rather than an agency's brochure. `src: UI/UX notes, north star`
- [ ] `C-UX-02` `ui` The app answers whether the studio is free without scrolling, reading or asking. `src: UI/UX notes, north star`
- [ ] `C-UX-03` `ui` The app holds an editorial unhurried register on the public routes. `src: UI/UX notes, register`
- [ ] `C-UX-04` `ui` The app holds a quiet operational register on the studio surfaces, using the same tokens. `src: UI/UX notes, register`
- [ ] `C-UX-05` `ui` The app takes space around the subject, one thing dominant per view. `src: UI/UX notes, the chain to consequence`
- [ ] `C-UX-06` `ui` The app reserves the largest type for the name plus the statement. `src: UI/UX notes, the chain to consequence`
- [ ] `C-UX-07` `ui` The app keeps the enquiry surface still, plainly worded, carrying no decoration. `src: UI/UX notes, the chain to consequence`
- [ ] `C-UX-08` `ui` The app sets the display face as an outline rather than a fill. `src: UI/UX notes, the chain to consequence`
- [ ] `C-UX-09` `ui` The app draws every stroked mark on rather than fading the mark in. `src: UI/UX notes, the chain to consequence`
- [ ] `C-UX-10` `contract` The app derives availability rather than letting the owner type a badge. `src: UI/UX notes, the chain to consequence`
- [ ] `C-UX-11` `ui` The app alternates two grounds down the document, a near-black neutral against a pale cool near-white lavender in cast. `src: UI/UX notes, colour`
- [ ] `C-UX-12` `ui` The app uses one accent, a deep soft indigo, as the ink on the pale ground plus the fill of every solid control. `src: UI/UX notes, colour`
- [ ] `C-UX-13` `constraint` The app shows two brighter indigos only as the stops of the hero's halo. `src: UI/UX notes, colour`
- [ ] `C-UX-14` `ui` The app keeps every supporting role neutral, a near-white for text on dark, the palest cool near-white for panels, a light cool neutral for secondary text. `src: UI/UX notes, colour`
- [ ] `C-UX-15` `literal` The app carries one signal colour, a `mid soft green`, meaning the studio is available. `src: UI/UX notes, colour`
- [ ] `C-UX-16` `constraint` The app permits the signal green a second use only as the focus rule on the dark ground. `src: UI/UX notes, colour`
- [ ] `C-UX-17` `constraint` The app never sits the signal green on the pale ground. `src: UI/UX notes, colour`
- [ ] `C-UX-18` `constraint` The app renders no `mid vivid red`, no `mid vivid amber` from the dependency's colour-name table. `src: UI/UX notes, colour`
- [ ] `C-UX-19` `constraint` The app renders an error as the product's own purple selection tint plus the words, never red. `src: UI/UX notes, colour`
- [ ] `C-UX-20` `ui` The app names three faces, a working face, the working face's bold, a condensed display face used only as an outline. `src: UI/UX notes, type`
- [ ] `C-UX-21` `contract` The app names a metrics-matched fallback for each face so the page does not reflow on arrival. `src: UI/UX notes, type`
- [ ] `C-UX-22` `constraint` The app ships no font binary. `src: UI/UX notes, type`
- [ ] `C-UX-23` `ui` The app draws the hero eyebrow plus both section titles with a stroke, a transparent fill. `src: UI/UX notes, type`
- [ ] `C-UX-24` `ui` The app fills the name alone, directly under an outlined eyebrow in the same face. `src: UI/UX notes, type`
- [ ] `C-UX-25` `ui` The app derives the type scale from one ratio applied repeatedly to one root size. `src: UI/UX notes, type`
- [ ] `C-UX-26` `ui` The app sets display type solid, body type loose at half again. `src: UI/UX notes, type`
- [ ] `C-UX-27` `ui` The app sets the about statement at display size loose, as the one deliberate exception. `src: UI/UX notes, type`
- [ ] `C-UX-28` `ui` The app uses two corner families, a generous rounding for a surface, a smaller one for anything sitting on a surface. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-29` `ui` The app uses a full pill radius for anything that is a control. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-30` `ui` The app rounds some panels on two corners only so sections read as sheets sliding over one another. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-31` `ui` The app orders depth as a render layer, the document, sticky things, the chrome, then the cursor plus the modal. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-32` `ui` The app builds the chrome as one layer whose children are ordered in the document. `src: UI/UX notes, shape and depth`
- [ ] `C-UX-33` `ui` The app carries one signature curve holding still, accelerating hard, stopping hard, symmetric at both ends. `src: UI/UX notes, motion`
- [ ] `C-UX-34` `ui` The app runs one duration of around half a second on almost every transform. `src: UI/UX notes, motion`
- [ ] `C-UX-35` `ui` The app runs two shorter durations for control states, one quick, one nearly instant on press. `src: UI/UX notes, motion`
- [ ] `C-UX-36` `ui` The app fades the hero's scroll invitation in slowly, arriving after everything else has settled. `src: UI/UX notes, motion`
- [ ] `C-UX-37` `constraint` The app names the properties that move rather than transitioning everything. `src: UI/UX notes, motion`
- [ ] `C-UX-38` `ui` The app splits the about statement per word, rising each word over the word's own faint twin as the document advances. `src: UI/UX notes, motion`
- [ ] `C-UX-39` `constraint` The app keeps the about statement selectable, announced as one string. `src: UI/UX notes, motion`
- [ ] `C-UX-40` `ui` The app draws every stroked mark on rather than appearing the mark. `src: UI/UX notes, motion`
- [ ] `C-UX-41` `ui` The app resolves every named motion moment to the moment's rest state under a reduced-motion preference. `src: UI/UX notes, motion`
- [ ] `C-UX-42` `constraint` The app removes nothing under reduced motion, stopping movement alone. `src: UI/UX notes, motion`
- [ ] `C-UX-43` `ui` The app draws the submit's pending state as the stroke drawing around the control's own outline. `src: UI/UX notes, motion`
- [ ] `C-UX-44` `constraint` The app shows no spinner anywhere. `src: UI/UX notes, motion`
- [ ] `C-UX-45` `ui` The app draws every mark as geometry rather than an image file, single colour, recoloured with the surface. `src: UI/UX notes, iconography`
- [ ] `C-UX-46` `constraint` The app replaces the award badges plus the tool band with neutral drawn marks. `src: UI/UX notes, iconography`
- [ ] `C-UX-47` `ui` The app keeps the public site spacious, the pipeline compact with rows sitting tight. `src: UI/UX notes, density and layout`
- [ ] `C-UX-48` `contract` The app holds pipeline controls in the same position between sessions. `src: UI/UX notes, density and layout`
- [ ] `C-UX-49` `constraint` The app uses four breakpoints, no others: a small-phone correction, the dominant mobile switch, a mid switch, a wide-desktop switch. `src: UI/UX notes, density and layout`
- [ ] `C-UX-50` `ui` The app folds the navigation to a burger below the mid switch, drops the lockup to the monogram on the smallest. `src: UI/UX notes, density and layout`
- [ ] `C-UX-51` `ui` The app steps the hero name plus the about statement each down two sizes on a narrow viewport. `src: UI/UX notes, density and layout`
- [ ] `C-UX-52` `ui` The app stacks the work index in one left-aligned column in date order below the mid switch. `src: UI/UX notes, density and layout`
- [ ] `C-UX-53` `ui` The app renders the project view as a panel rather than a modal below the mid switch. `src: UI/UX notes, density and layout`
- [ ] `C-UX-54` `ui` The app hides the fixed rail, goes the contact form to one column, shows fewer tool marks below the mid switch. `src: UI/UX notes, density and layout`
- [ ] `C-UX-55` `constraint` The app overflows nothing sideways at a narrow viewport, keeping every navigation target reachable. `src: UI/UX notes, density and layout`
- [ ] `C-UX-56` `ui` The app gives the scroll prompt a single weighted bounce, the only bounce in the product. `src: UI/UX notes, two motion details`
- [ ] `C-UX-57` `ui` The app runs the chrome, the pill, the flag bar entrances once on load with a long tail. `src: UI/UX notes, two motion details`
- [ ] `C-UX-58` `contract` The app defaults sound to off, stating the default in the control. `src: UI/UX notes, two motion details`
- [ ] `C-UX-59` `ui` The app renders no custom cursor below the mid switch, making the cursor's label a visible control on each row. `src: UI/UX notes, touch`
- [ ] `C-UX-60` `ui` The app ties the grayscale-to-colour treatment on media to entering the frame rather than to hover. `src: UI/UX notes, touch`
- [ ] `C-UX-61` `ui` The app sizes every control as a comfortable fingertip target, achieved with padding. `src: UI/UX notes, touch`
- [ ] `C-UX-62` `constraint` The app stops the tool band auto-scrolling during a touch on the band. `src: UI/UX notes, touch`
- [ ] `C-UX-63` `contract` The app meets WCAG AA contrast between body text plus the text's background. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-64` `ui` The app replaces the reference's placeholder colour with the secondary text colour, which passes. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-65` `ui` The app shows focus on every interactive element, green on the dark ground, indigo on the pale one. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-66` `constraint` The app never removes focus, letting a focus ring plus a hover treatment happen at once. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-67` `contract` The app hides the two split treatments from assistive technology as split elements, with the original string present once in reading order. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-68` `contract` The app names every icon-only control. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-69` `contract` The app reaches every control on every route from the keyboard. `src: UI/UX notes, accessibility floors`
- [ ] `C-UX-70` `constraint` The app is not a dashboard with a portfolio pasted on top. `src: UI/UX notes, what this must not look like`
- [ ] `C-UX-71` `constraint` The app is not a page dominated by one hue family with no second signal. `src: UI/UX notes, what this must not look like`
- [ ] `C-UX-72` `constraint` The app is not a build whose stroked marks fade in. `src: UI/UX notes, what this must not look like`
- [ ] `C-UX-73` `constraint` The app degrades the moving ground to a still ground in the same colours, never an empty rectangle. `src: UI/UX notes, what this must not look like`
- [ ] `C-UX-74` `constraint` The app is not a floating message arriving from a corner. `src: UI/UX notes, what this must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app serves an application shell on first paint, assembling every later screen in the browser from the app's own JSON API. `src: Technical requirements, the render model`
- [ ] `C-TR-02` `contract` The app keeps the fixed chrome alive across a route change with no full page load. `src: Technical requirements, the render model`
- [ ] `C-TR-03` `literal` The app builds the frontend with `Svelte` plus `Vite` to a production bundle. `src: Technical requirements, stack`
- [ ] `C-TR-04` `literal` The app serves the HTTP API with `Hono` on Node on the same origin under the `/api` prefix. `src: Technical requirements, stack`
- [ ] `C-TR-05` `literal` The app reaches PostgreSQL at `DATABASE_URL`. `src: Technical requirements, stack`
- [ ] `C-TR-06` `literal` The app reaches `mailpit` over real SMTP at `SMTP_HOST` plus `SMTP_PORT`. `src: Technical requirements, stack`
- [ ] `C-TR-07` `literal` The app reads `SMTP_USER` plus `SMTP_PASS` from the environment. `src: Technical requirements, stack`
- [ ] `C-TR-08` `contract` The app declares a health route answering `200` once the app is ready. `src: Technical requirements, stack`
- [ ] `C-TR-09` `contract` The app writes request logs to stdout. `src: Technical requirements, stack`
- [ ] `C-TR-10` `constraint` The app hardcodes no host, no port, no credential, reading each from the environment. `src: Technical requirements, environment paragraph`
- [ ] `C-TR-11` `constraint` The app downloads, installs, compiles or starts no copy of a backing service. `src: Technical requirements, environment paragraph`
- [ ] `C-TR-12` `constraint` The app introduces no second database, cache, queue, object store, identity provider or mail vendor. `src: Technical requirements, libraries paragraph`
- [ ] `C-TR-13` `contract` The app resolves two acceptances against one window's last capacity to exactly one booking. `src: Technical requirements, capacity under contention`
- [ ] `C-TR-14` `contract` The app tells the refused caller which window filled, what is still open. `src: Technical requirements, capacity under contention`
- [ ] `C-TR-15` `contract` The app puts every named message in `mailpit` as a real message. `src: Technical requirements, mail is real`
- [ ] `C-TR-16` `contract` The app leaves the state change standing when a send fails. `src: Technical requirements, mail is real`
- [ ] `C-TR-17` `contract` The app decides authorisation on every write from the session or the enquiry token, never from a request body field. `src: Technical requirements, authorisation per write`
- [ ] `C-TR-18` `contract` The app rate limits the enquiry form plus the sign-in link request per address, stating the wait in words. `src: Technical requirements, rate limits`
- [ ] `C-TR-19` `contract` The app carries the standard security headers on every response, among them a strict transport policy plus a nosniff policy. `src: Technical requirements, security headers`
- [ ] `C-TR-20` `constraint` The app puts no credential, no API key, no admin token in anything the browser downloads. `src: Technical requirements, no secrets in the bundle`
- [ ] `C-TR-21` `constraint` The app renders every stored enquiry value as text, never as markup. `src: Technical requirements, security and abuse`
- [ ] `C-TR-22` `contract` The app shows a hostile input back to the studio exactly as the input was typed. `src: Technical requirements, security and abuse`
- [ ] `C-TR-23` `constraint` The app keeps every token opaque, single-purpose, expiring. `src: Technical requirements, security and abuse`
- [ ] `C-TR-24` `contract` The app ends a session on sign-out, refusing a resume by going back. `src: Technical requirements, security and abuse`
- [ ] `C-TR-25` `constraint` The app subsets each face to the glyphs the product sets, offering a legacy format only where the modern one is refused. `src: Technical requirements, the font budget`
- [ ] `C-TR-26` `contract` The app renders the first screen of the home document before the display faces arrive. `src: Technical requirements, performance`
- [ ] `C-TR-27` `contract` The app defers everything below the first screen, every project medium, the moving hero ground. `src: Technical requirements, performance`
- [ ] `C-TR-28` `constraint` The app records the seven named events in the product's own store, sending them nowhere else. `src: Technical requirements, instrumentation`
- [ ] `C-TR-29` `literal` The app names a responsiveness bar of `9` projects, `40` windows, `500` enquiries, `2000` messages. `src: Technical requirements, responsiveness bar`
- [ ] `C-TR-30` `contract` The app keeps the home document scrolling smoothly at the stated bar. `src: Technical requirements, responsiveness bar`
- [ ] `C-TR-31` `contract` The app lists every public route at `GET /sitemap.xml`. `src: Technical requirements, discovery`
- [ ] `C-TR-32` `contract` The app directs `GET /robots.txt` at the sitemap by the sitemap's absolute address. `src: Technical requirements, discovery`

## C-DM Data model

- [ ] `C-DM-01` `data` The app carries twelve tables, every timestamp in UTC. `src: Data model preamble`
- [ ] `C-DM-02` `literal` The app writes `deku-demo-pw-2026` into `/app/USER_README.md` alongside each seeded account. `src: Data model, the seeded password`
- [ ] `C-DM-03` `data` The app stores an account with an `id`, a case-folded unique `email`, a `password_hash`, a `display_name`, an `organisation`, a `role`, a `timezone`. `src: Data model, accounts`
- [ ] `C-DM-04` `data` The app stores `created_at` plus `last_seen_at` on an account. `src: Data model, accounts`
- [ ] `C-DM-05` `constraint` The app bounds an account `display_name` to 1 to 60 characters, an `organisation` to 0 to 120. `src: Data model, accounts`
- [ ] `C-DM-06` `data` The app stores a project with a unique kebab-case `slug`, a `title`, a `discipline`, a `year`, a `description`, a `link`. `src: Data model, projects`
- [ ] `C-DM-07` `data` The app stores a project `position` that is unique, ascending, plus a `state` of `published` or `draft`. `src: Data model, projects`
- [ ] `C-DM-08` `data` The app stores a service with a `title`, a `body`, a `position`. `src: Data model, services`
- [ ] `C-DM-09` `data` The app stores a social link with a `label`, an `href`, a `position`. `src: Data model, social_links`
- [ ] `C-DM-10` `data` The app stores one `site_meta` row with a `version`, a predecessor label, a predecessor link, a local timezone. `src: Data model, site_meta`
- [ ] `C-DM-11` `constraint` The app reads the footer's version from the stored meta row rather than from a build constant. `src: Data model, site_meta`
- [ ] `C-DM-12` `data` The app stores a window with a start date, a `weeks`, a `capacity_days`, a `committed_days`, a `state`. `src: Data model, windows`
- [ ] `C-DM-13` `data` The app stores a hold with a window reference, an enquiry reference, a `days`, an expiry, a release time. `src: Data model, holds`
- [ ] `C-DM-14` `contract` The app counts a hold as live when the release time is null, the expiry has not passed. `src: Data model, holds`
- [ ] `C-DM-15` `data` The app stores an enquiry with a unique opaque `token`, an account reference, the six answers, a window reference, a `state`. `src: Data model, enquiries`
- [ ] `C-DM-16` `literal` The app carries an enquiry state of `new`, `reading`, `proposed`, `booked`, `declined`, `withdrawn` or `lapsed`. `src: Data model, enquiries`
- [ ] `C-DM-17` `data` The app leaves an enquiry's account reference null when the sender took no account. `src: Data model, enquiries`
- [ ] `C-DM-18` `data` The app leaves an enquiry's window reference null when the hold lapsed before submit. `src: Data model, enquiries`
- [ ] `C-DM-19` `data` The app stores a message with an enquiry reference, an `author` of `client` or `studio`, a `body` of 1 to 4000. `src: Data model, messages`
- [ ] `C-DM-20` `data` The app stores a proposal with a start date, a `weeks`, a days per week, a `note`, an expiry. `src: Data model, proposals`
- [ ] `C-DM-21` `literal` The app carries a proposal state of `live`, `accepted`, `expired` or `superseded`. `src: Data model, proposals`
- [ ] `C-DM-22` `data` The app stores a booking with a unique enquiry reference, a window reference, a start date, a `weeks`, a days per week, a confirmation time. `src: Data model, bookings`
- [ ] `C-DM-23` `data` The app stores a page view with a `route` plus a view time. `src: Data model, page_views`
- [ ] `C-DM-24` `constraint` The app writes a page view only when the cookie answer was yes, reading the page views to the studio alone. `src: Data model, page_views`
- [ ] `C-DM-25` `data` The app relates one window to many holds, at most `3` live. `src: Data model, relationships`
- [ ] `C-DM-26` `data` The app relates one window to many bookings, bounded by the window's capacity days. `src: Data model, relationships`
- [ ] `C-DM-27` `data` The app relates one enquiry to many messages, to many proposals with at most one `live`. `src: Data model, relationships`
- [ ] `C-DM-28` `data` The app relates one enquiry to at most one booking, one account to many enquiries. `src: Data model, relationships`
- [ ] `C-DM-29` `contract` The app survives a reload, a new tab, a new device with every stored entity. `src: Data model, persistence`
- [ ] `C-DM-30` `contract` The app keeps a hold server-side, tied to the hold's enquiry rather than to a browser. `src: Data model, persistence`
- [ ] `C-DM-31` `constraint` The app keeps the enquiry draft, the sound setting, the session in the browser alone. `src: Data model, persistence`
- [ ] `C-DM-32` `contract` The app runs a schema migration before serving the first request, changing nothing on a second run. `src: Data model, persistence`
- [ ] `C-DM-33` `contract` The app keeps a window's committed days equal to the sum of days per week over that window's bookings. `src: Data model, invariants`
- [ ] `C-DM-34` `constraint` The app keeps a window's committed days from ever exceeding the window's capacity days. `src: Data model, invariants`
- [ ] `C-DM-35` `constraint` The app changes no committed days on a hold. `src: Data model, invariants`
- [ ] `C-DM-36` `constraint` The app stores the availability mode nowhere, deriving the mode on every read. `src: Data model, invariants`
- [ ] `C-DM-37` `data` The app seeds two accounts named `Elian Moreau` plus `Alex Renard`. `src: Data model, seed data`
- [ ] `C-DM-38` `literal` The app seeds an `open` window starting in `10` days for `6` weeks at `3` capacity days. `src: Data model, seed data`
- [ ] `C-DM-39` `literal` The app seeds an `open` window starting in `40` days for `8` weeks at `2` capacity days. `src: Data model, seed data`
- [ ] `C-DM-40` `literal` The app seeds a `booked` window starting in `90` days for `4` weeks at `2` capacity days with `2` committed. `src: Data model, seed data`
- [ ] `C-DM-41` `literal` The app seeds the projects `Meridian`, `Auriga Concept`, `Portfolio 2.0`, `Uplink Usability`, `Tower Supervision` in position order. `src: Data model, seed data`
- [ ] `C-DM-42` `literal` The app seeds the projects `Colisa`, `UBX Roadmap`, `Aera Unity`, `Baba Quiz` in position order. `src: Data model, seed data`
- [ ] `C-DM-43` `literal` The app seeds the services `SEO`, `UX Design`, `Web & Mobile Development`. `src: Data model, seed data`
- [ ] `C-DM-44` `data` The app seeds three social links plus one site meta row. `src: Data model, seed data`
- [ ] `C-DM-45` `data` The app seeds one enquiry from Alex Renard against the first open window in state `proposed`, carrying two messages plus one live proposal. `src: Data model, seed data`
- [ ] `C-DM-46` `contract` The app duplicates no row when restarted. `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The app presents the fixed chrome on every public route at every width, carrying four slots. `src: Front-end specification, the fixed chrome`
- [ ] `C-FE-02` `ui` The app sets the name lockup as two stacked lines with a small monogram of two stepped keycaps to the upper right. `src: Front-end specification, the fixed chrome`
- [ ] `C-FE-03` `ui` The app gives the header no ground at the top of the document, acquiring a blurred darkened ground as content passes under. `src: Front-end specification, the fixed chrome`
- [ ] `C-FE-04` `ui` The app scrubs the header's ground against scroll position rather than playing the ground on a timer. `src: Front-end specification, the fixed chrome`
- [ ] `C-FE-05` `ui` The app slides the lockup in from the left, enters the pill from the upper left, both on load. `src: Front-end specification, the fixed chrome`
- [ ] `C-FE-06` `ui` The app draws the availability pill at pill radius with a hairline border in the signal green over the dark ground. `src: Front-end specification, the availability pill`
- [ ] `C-FE-07` `ui` The app carries a small filled circle with a soft halo of the signal green in the pill. `src: Front-end specification, the availability pill`
- [ ] `C-FE-08` `constraint` The app allows the pill's words to be typed at no interface anywhere. `src: Front-end specification, the availability pill`
- [ ] `C-FE-09` `ui` The app names the current route in the top left of the content area on every route except the home document. `src: Front-end specification, the route label`
- [ ] `C-FE-10` `ui` The app gives the route label a single rounded corner where the label meets the page edge, rising into place on a route change. `src: Front-end specification, the route label`
- [ ] `C-FE-11` `ui` The app carries a narrow fixed rail at the left edge with two award badges plus a vertical label reading `Honors`, rotated bottom to top. `src: Front-end specification, the fixed rail`
- [ ] `C-FE-12` `constraint` The app never scrolls the fixed rail, treating the rail as neither chrome nor content. `src: Front-end specification, the fixed rail`
- [ ] `C-FE-13` `ui` The app replaces the pointer over the work index rows with a circular element plus a label reading `View` above the mid switch. `src: Front-end specification, the custom cursor`
- [ ] `C-FE-14` `literal` The app reads the hero eyebrow `Creative Developer`, set in the stroked display face. `src: Front-end specification, the hero`
- [ ] `C-FE-15` `ui` The app sets the name under the eyebrow at display size in the same face, filled. `src: Front-end specification, the hero`
- [ ] `C-FE-16` `literal` The app sets `Located in France` below the name with a three-segment bar under the line in blue, white, red. `src: Front-end specification, the hero`
- [ ] `C-FE-17` `constraint` The app renders the French flag as a drawn bar rather than as an image. `src: Front-end specification, the hero`
- [ ] `C-FE-18` `literal` The app reads the prompt `Scroll down to explore` with a stroked arrow, arriving last, fading in slowly. `src: Front-end specification, the hero`
- [ ] `C-FE-19` `ui` The app sits a moving ground behind the name with a halo in the two bright indigos, holding one frame under reduced motion. `src: Front-end specification, the hero`
- [ ] `C-FE-20` `ui` The app titles the about section with the word `About`, a sixteen-point asterisk, the word `me`, in the stroked display face with a drawn underline. `src: Front-end specification, the about section`
- [ ] `C-FE-21` `constraint` The app uses that title construction for both section titles, carrying no other heading system. `src: Front-end specification, the about section`
- [ ] `C-FE-22` `ui` The app sets the statement at display size loose, split per word with the shadow reveal. `src: Front-end specification, the about section`
- [ ] `C-FE-23` `ui` The app sets the figure `5+` with the label `years of experience` beside the statement. `src: Front-end specification, the about section`
- [ ] `C-FE-24` `ui` The app carries a horizontally scrolling band of tool marks, each with an accessible name, hidden from assistive technology as a group. `src: Front-end specification, the about section`
- [ ] `C-FE-25` `ui` The app shows the home preview as rules plus rows, a title at the left, a credit line right-aligned carrying the discipline plus the year. `src: Front-end specification, the work surfaces`
- [ ] `C-FE-26` `ui` The app shows `/work` as a staggered pill layout with a title pill plus a description pill. `src: Front-end specification, the work surfaces`
- [ ] `C-FE-27` `ui` The app builds one component at two densities for the two work presentations. `src: Front-end specification, the work surfaces`
- [ ] `C-FE-28` `ui` The app sits a quadratic text arc in the home preview with text set along the arc, bending as the document advances. `src: Front-end specification, the work surfaces`
- [ ] `C-FE-29` `ui` The app sets the contact surface on the dark ground with a faint contour texture. `src: Front-end specification, the contact surface`
- [ ] `C-FE-30` `literal` The app reads the contact headline `LET'S BUILD YOUR IDEA TOGETHER :)` in the stroked display face across four lines. `src: Front-end specification, the contact surface`
- [ ] `C-FE-31` `constraint` The app sets the typed emoticon at the same size as the rest, rendered as outlined glyphs rather than a drawing. `src: Front-end specification, the contact surface`
- [ ] `C-FE-32` `ui` The app sits a circular portrait with an accent ring beside the first headline line. `src: Front-end specification, the contact surface`
- [ ] `C-FE-33` `ui` The app numbers the six fields, each a label over an underlined input with no box. `src: Front-end specification, the contact surface`
- [ ] `C-FE-34` `ui` The app turns the hairline rule under each input to the signal green on focus over dark, to the accent indigo over pale. `src: Front-end specification, the contact surface`
- [ ] `C-FE-35` `ui` The app renders the required mark as the mark's own element, the placeholders as worked examples in the secondary text colour. `src: Front-end specification, the contact surface`
- [ ] `C-FE-36` `literal` The app carries a side column reading `Further Inquiries` with the contact address plus `Located in France 📍`. `src: Front-end specification, the contact surface`
- [ ] `C-FE-37` `literal` The app carries `Social Media` in the side column with the three links. `src: Front-end specification, the contact surface`
- [ ] `C-FE-38` `ui` The app places the studio surfaces under a persistent left sidebar rather than the public chrome. `src: Front-end specification, the studio surfaces`
- [ ] `C-FE-39` `ui` The app opens the proposal form as a slide-over from the right with the start date constrained to the window. `src: Front-end specification, the studio surfaces`
- [ ] `C-FE-40` `ui` The app constrains the proposal's capacity in days per week by what the window has left, showing the remaining capacity live above the fields. `src: Front-end specification, the studio surfaces`
- [ ] `C-FE-41` `literal` The app carries four footer heads: `Local Time`, `Version`, `Resource`, `Social Media`. `src: Front-end specification, the footer`
- [ ] `C-FE-42` `ui` The app closes the footer with a credit line. `src: Front-end specification, the footer`
- [ ] `C-FE-43` `ui` The app divides into a public module group that reads plus renders, a booking module group that writes. `src: Front-end specification, the module boundary`
- [ ] `C-FE-44` `constraint` The app introduces no new shape, no new colour in the booking layer. `src: Front-end specification, the module boundary`
- [ ] `C-FE-45` `constraint` The app draws every asset in code, shipping no binary. `src: Front-end specification, procedural assets`
- [ ] `C-FE-46` `contract` The app names three font families, each with a metrics-matched fallback, rather than shipping a font file. `src: Front-end specification, procedural assets`
- [ ] `C-FE-47` `ui` The app draws the monogram, the burger, the arrow, the sixteen-point asterisk, the text arc as inline stroked vector geometry. `src: Front-end specification, procedural assets`
- [ ] `C-FE-48` `constraint` The app replaces the two award badges plus the tool marks with neutral drawn marks. `src: Front-end specification, procedural assets`
- [ ] `C-FE-49` `contract` The app generates each project's media from that project's own record rather than shipping an image. `src: Front-end specification, procedural assets`
- [ ] `C-FE-50` `constraint` The app draws the hero's ground rather than playing a video, shipping no audio file. `src: Front-end specification, procedural assets`
- [ ] `C-FE-51` `literal` The app pins the pill copy `available now for work`, `available from`, `booked until`, `not taking new work`. `src: Front-end specification, copy that is pinned`
- [ ] `C-FE-52` `literal` The app pins the navigation copy `Home`, `About`, `Work`, `Contact`. `src: Front-end specification, copy that is pinned`
- [ ] `C-FE-53` `literal` The app pins the about statement as one string revealed word by word. `src: Front-end specification, copy that is pinned`
- [ ] `C-FE-54` `literal` The app pins the three service lines, the three social labels `Linkedin`, `Postline`, `Showcase`. `src: Front-end specification, copy that is pinned`
- [ ] `C-FE-55` `literal` The app pins the work headline copy on the work index. `src: Front-end specification, copy that is pinned`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The app is single tenant, with one studio, one site, no organisation above the account. `src: Constraints, single tenancy`
- [ ] `C-CN-02` `constraint` The app takes no payment of any kind, offering no contract, no invoice, no card. `src: Constraints, not built`
- [ ] `C-CN-03` `constraint` The app offers no file upload anywhere. `src: Constraints, not built`
- [ ] `C-CN-04` `constraint` The app builds no sound cue set, keeping the control, the two strings, the rule that no state is carried by sound alone. `src: Constraints, not built`
- [ ] `C-CN-05` `constraint` The app builds no real-time scene graph behind the hero, keeping a moving drawn ground. `src: Constraints, not built`
- [ ] `C-CN-06` `constraint` The app builds no password policy, no staff hierarchy, no editor role, no admin role. `src: Constraints, not built`
- [ ] `C-CN-07` `constraint` The app sends no follow-up mail chasing an unanswered enquiry, no newsletter, no marketing derived from an enquiry. `src: Constraints, not built`
- [ ] `C-CN-08` `constraint` The app uses no third-party analytics, keeping the page-view record local, gated on the cookie answer. `src: Constraints, not built`
- [ ] `C-CN-09` `constraint` The app ships in one language, translating nothing. `src: Constraints, not built`
- [ ] `C-CN-10` `constraint` The app ships no third party brand name, no proprietary font binary, no logo file, no award badge, no tool mark belonging to another organisation. `src: Constraints, no borrowed identity`
- [ ] `C-CN-11` `constraint` The app puts no product name in a class-name prefix generated by tooling. `src: Constraints, no borrowed identity`
- [ ] `C-CN-12` `literal` The app stays responsive at `9` projects, `40` windows, `500` enquiries, `2000` messages. `src: Constraints, the responsiveness bar`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-02` `literal` The app serves on the container-internal port `4173`, mapped from `APP_PUBLIC_PORT`. `src: Deployment contract, bullet 1`
- [ ] `C-DC-03` `constraint` The app hardcodes neither the public port nor the public address, reading both from the environment. `src: Deployment contract, bullet 1`
- [ ] `C-DC-04` `contract` The app serves the HTTP API on the same origin under the `/api` prefix. `src: Deployment contract, bullet 2`
- [ ] `C-DC-05` `contract` The app answers `GET /api/health` with `200` once ready. `src: Deployment contract, bullet 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual step. `src: Deployment contract, bullet 4`
- [ ] `C-DC-07` `literal` The app writes the login credentials to `/app/USER_README.md`. `src: Deployment contract, bullet 5`
- [ ] `C-DC-08` `literal` The app carries empty reserved `.browser_screenshots/` plus `.downloads/` directories at the app root. `src: Deployment contract, bullet 6`
- [ ] `C-DC-09` `constraint` The app serves a production build behind a static or preview server, never a dev server. `src: Deployment contract, bullet 7`
- [ ] `C-DC-10` `constraint` The app keeps the server running after the session ends, never as a child of the shell. `src: Deployment contract, bullet 8`
- [ ] `C-DC-11` `literal` The app binds `0.0.0.0`, never a loopback address. `src: Deployment contract, bullet 9`
- [ ] `C-DC-12` `constraint` The app starts no copy of a backing service, reaching each at the service's environment variable. `src: Deployment contract, bullet 10`
- [ ] `C-DC-13` `constraint` The app uses only the named providers, declaring no edge function. `src: Deployment contract, bullet 11`
- [ ] `C-DC-14` `constraint` The app declares no persistent volume, no fixed container name, no custom network. `src: Deployment contract, bullet 12`
- [ ] `C-DC-15` `contract` The app accepts the signup, login, session, sign-in link endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-16` `contract` The app accepts the meta, projects, services endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-17` `contract` The app accepts the availability, window create, window update endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-18` `contract` The app accepts the hold create, hold delete endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-19` `contract` The app accepts the enquiry create, read, update, message, proposal endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `contract` The app accepts the accept, withdraw endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `contract` The app accepts the pipeline, export, consent, page-view endpoints at the pinned shapes. `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `contract` The app returns a top-level JSON array from every list endpoint. `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `constraint` The app rejects an invalid or unauthorized call as a client error, never as a server error, never as a silent success. `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `contract` The app requires bearer auth on every endpoint except signup, login, health, the link request, the consent record, the public reads. `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `constraint` The app keeps `mailpit` as the only place a message lives, substituting no in-memory array, no hardcoded success, no log line. `src: Deployment contract, no mocks`
- [ ] `C-DC-26` `constraint` The app treats the window row in PostgreSQL as the capacity fact, never a count the interface keeps for itself. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-demo-pw-2026` | password for both seeded accounts | C-RL-33 | User roles, seeded accounts password |
| `studio@example.com` | the seeded studio account | C-RL-31 | User roles, seeded accounts table |
| `client@example.com` | the seeded client account | C-RL-31 | User roles, seeded accounts table |
| `Elian Moreau` | the studio display name | C-RL-31 | User roles, seeded accounts table |
| `Alex Renard` | the client display name | C-RL-31 | User roles, seeded accounts table |
| `Atelier Moreau` | the studio organisation | C-RL-31 | User roles, seeded accounts table |
| `Northgate` | the client organisation | C-RL-31 | User roles, seeded accounts table |
| `client` | the role every signup creates | C-RL-28 | User roles, signup paragraph |
| `studio` | the single seeded owner role | C-RL-28 | User roles, signup paragraph |
| `72 hours` | the hold lifetime | C-RL-20 | User roles, anonymous paragraph |
| `90 days` | the enquiry token lifetime | C-RL-20 | User roles, anonymous paragraph |
| `24 hours` | the bearer token lifetime | C-CF-01 | Core features, Auth |
| `If that address has an enquiry with us, a sign-in link is on its way.` | the sign-in link response | C-CF-10 | Core features rule 4 |
| `Turn sound on` | the sound control's accessible name | C-CF-22 | Core features rule 9 |
| `(09)` | the work index count at nine projects | C-CF-26 | Core features rule 11 |
| `open_now` | the mode when a window starts soon | C-CF-32 | Core features rule 14 mode table |
| `open_from` | the mode when a window starts later | C-CF-32 | Core features rule 14 mode table |
| `booked_until` | the mode when nothing is open | C-CF-32 | Core features rule 14 mode table |
| `not_taking` | the mode when no window exists | C-CF-32 | Core features rule 14 mode table |
| `14 days` | the open-now horizon | C-CF-32 | Core features rule 14 mode table |
| `available now for work` | the pill under open_now | C-CF-32 | Core features rule 14 mode table |
| `available from` | the pill under open_from | C-CF-32 | Core features rule 14 mode table |
| `booked until` | the pill under booked_until | C-CF-32 | Core features rule 14 mode table |
| `not taking new work` | the pill under not_taking | C-CF-32 | Core features rule 14 mode table |
| `Start an enquiry` | the control opening the form against a window | C-CF-42 | Core features rule 18 |
| `weeks` | a window's length field | C-CF-44 | Core features rule 19 |
| `capacity_days` | a window's capacity field | C-CF-44 | Core features rule 19 |
| `committed_days` | a window's committed field | C-CF-44 | Core features rule 19 |
| `1` | the lowest capacity days | C-CF-44 | Core features rule 19 |
| `5` | the highest capacity days | C-CF-44 | Core features rule 19 |
| `0` | the starting committed days | C-CF-44 | Core features rule 19 |
| `open` | a window state | C-CF-44 | Core features rule 19 |
| `held` | a window state | C-CF-44 | Core features rule 19 |
| `booked` | a window state | C-CF-44 | Core features rule 19 |
| `closed` | a window state | C-CF-44 | Core features rule 19 |
| `3` | the live hold ceiling per window | C-CF-52 | Core features rule 22 |
| `This window is nearly full. Send an enquiry without holding it.` | the fourth-hold refusal | C-CF-52 | Core features rule 22 |
| `My Name` | enquiry field one | C-CF-61 | Core features, the enquiry field table |
| `My Email` | enquiry field two | C-CF-61 | Core features, the enquiry field table |
| `I work at` | enquiry field three | C-CF-61 | Core features, the enquiry field table |
| `I am looking for` | enquiry field four | C-CF-61 | Core features, the enquiry field table |
| `My budget is` | enquiry field five | C-CF-61 | Core features, the enquiry field table |
| `My message` | enquiry field six | C-CF-61 | Core features, the enquiry field table |
| `We need something to call you.` | the missing-name error | C-CF-61 | Core features, the enquiry field table |
| `We need an address to reply to.` | the missing-address error | C-CF-61 | Core features, the enquiry field table |
| `That is longer than we can store.` | the over-long organisation error | C-CF-61 | Core features, the enquiry field table |
| `A few words about what you need.` | the missing-subject error | C-CF-61 | Core features, the enquiry field table |
| `Choose a range, even a rough one.` | the missing-band error | C-CF-61 | Core features, the enquiry field table |
| `Tell us a little more, at least twenty characters.` | the short-message error | C-CF-61 | Core features, the enquiry field table |
| `USD $20001 and up` | budget band one | C-CF-73 | Core features rule 25 |
| `USD $10001-$20000` | budget band two | C-CF-73 | Core features rule 25 |
| `USD $5001-$10000` | budget band three | C-CF-73 | Core features rule 25 |
| `USD $2000-$5000` | budget band four | C-CF-73 | Core features rule 25 |
| `Smaller than that? Say so in your message and we will point you somewhere good.` | the line under the band select | C-CF-78 | Core features rule 26 |
| `Send it now :)` | the submit control | C-CF-80 | Core features rule 27 |
| `new` | the state a submitted enquiry starts in | C-CF-86 | Core features rule 30 |
| `token` | the opaque enquiry key | C-CF-86 | Core features rule 30 |
| `Your hold on that window ran out. You can still send this.` | the lapsed-hold band | C-CF-89 | Core features rule 31 |
| `reading` | the state when the studio opens an enquiry | C-CF-94 | Core features rule 33 |
| `proposed` | the state when a proposal is sent | C-CF-98 | Core features rule 35 |
| `live` | the single active proposal state | C-CF-102 | Core features rule 36 |
| `That window filled up. Here is what is open.` | the losing acceptance refusal | C-CF-107 | Core features rule 38 |
| `That proposal has expired. Ask for a new one.` | the expired proposal refusal | C-CF-112 | Core features rule 39 |
| `withdrawn` | the state after a withdrawal | C-CF-114 | Core features rule 40 |
| `declined` | the state after a decline | C-CF-116 | Core features rule 41 |
| `30 days` | the silence before an enquiry lapses | C-CF-118 | Core features rule 42 |
| `lapsed` | the state after silence | C-CF-118 | Core features rule 42 |
| `We have your enquiry` | the sender's confirmation subject | C-CF-131 | Core features rule 48 mail table |
| `New enquiry` | the studio's notification subject | C-CF-131 | Core features rule 48 mail table |
| `A reply to your enquiry` | the studio reply subject | C-CF-131 | Core features rule 48 mail table |
| `A reply from` | the client reply subject | C-CF-131 | Core features rule 48 mail table |
| `A start date for your project` | the proposal subject | C-CF-131 | Core features rule 48 mail table |
| `Booked` | the acceptance subject to both parties | C-CF-131 | Core features rule 48 mail table |
| `Your start date offer expires soon` | the expiry warning subject | C-CF-131 | Core features rule 48 mail table |
| `About your enquiry` | the decline subject | C-CF-131 | Core features rule 48 mail table |
| `Your sign-in link` | the sign-in link subject | C-CF-131 | Core features rule 48 mail table |
| `48 hours` | the proposal expiry warning horizon | C-CF-131 | Core features rule 48 mail table |
| `An enquiry appears here once you send one.` | the empty account state | C-UF-27 | User flow, states |
| `The pipeline is clear.` | the empty pipeline state | C-UF-27 | User flow, states |
| `No projects listed.` | the empty work index state | C-UF-27 | User flow, states |
| `That did not load.` | the failed read state | C-UF-27 | User flow, states |
| `Try again` | the retry control | C-UF-27 | User flow, states |
| `That is not yours to open.` | the denied surface | C-UF-27 | User flow, states |
| `We cannot find that.` | the missing surface | C-UF-27 | User flow, states |
| `You are offline. Your draft is safe.` | the offline state | C-UF-27 | User flow, states |
| `mid soft green` | the one signal colour | C-UX-11 | UI/UX notes, colour |
| `mid vivid red` | a dependency colour name that never renders | C-UX-11 | UI/UX notes, colour |
| `mid vivid amber` | a dependency colour name that never renders | C-UX-11 | UI/UX notes, colour |
| `Svelte` | the frontend framework | C-TR-03 | Technical requirements, stack |
| `Vite` | the frontend build tool | C-TR-03 | Technical requirements, stack |
| `Hono` | the backend framework | C-TR-03 | Technical requirements, stack |
| `DATABASE_URL` | the database connection variable | C-TR-03 | Technical requirements, stack |
| `SMTP_HOST` | the mail host variable | C-TR-03 | Technical requirements, stack |
| `SMTP_PORT` | the mail port variable | C-TR-03 | Technical requirements, stack |
| `SMTP_USER` | the mail user variable | C-TR-03 | Technical requirements, stack |
| `SMTP_PASS` | the mail password variable | C-TR-03 | Technical requirements, stack |
| `mailpit` | the mail provider | C-TR-03 | Technical requirements, stack |
| `9` | the project count the bar names | C-TR-29 | Technical requirements, responsiveness bar |
| `40` | the window count the bar names | C-TR-29 | Technical requirements, responsiveness bar |
| `500` | the enquiry count the bar names | C-TR-29 | Technical requirements, responsiveness bar |
| `2000` | the message count the bar names | C-TR-29 | Technical requirements, responsiveness bar |
| `site_meta` | the one-row content table | C-DM-10 | Data model, site_meta |
| `version` | the meta row's version field | C-DM-10 | Data model, site_meta |
| `days` | a hold's requested days field | C-DM-13 | Data model, holds |
| `author` | a message's side field | C-DM-19 | Data model, messages |
| `client` | a message author value | C-DM-19 | Data model, messages |
| `studio` | a message author value | C-DM-19 | Data model, messages |
| `note` | a proposal's free field | C-DM-20 | Data model, proposals |
| `accepted` | a proposal state | C-DM-20 | Data model, proposals |
| `expired` | a proposal state | C-DM-20 | Data model, proposals |
| `superseded` | a proposal state | C-DM-20 | Data model, proposals |
| `route` | a page view's route field | C-DM-23 | Data model, page_views |
| `published` | a project state | C-DM-06 | Data model, projects |
| `draft` | a project state | C-DM-06 | Data model, projects |
| `10` | the first seeded window's start offset in days | C-DM-37 | Data model, seed data |
| `6` | the first seeded window's length in weeks | C-DM-37 | Data model, seed data |
| `2` | the second seeded window's capacity days | C-DM-37 | Data model, seed data |
| `8` | the second seeded window's length in weeks | C-DM-37 | Data model, seed data |
| `90` | the third seeded window's start offset in days | C-DM-37 | Data model, seed data |
| `4` | the third seeded window's length in weeks | C-DM-37 | Data model, seed data |
| `Meridian` | a seeded project | C-DM-37 | Data model, seed data |
| `Auriga Concept` | a seeded project | C-DM-37 | Data model, seed data |
| `Portfolio 2.0` | a seeded project | C-DM-37 | Data model, seed data |
| `Uplink Usability` | a seeded project | C-DM-37 | Data model, seed data |
| `Tower Supervision` | a seeded project | C-DM-37 | Data model, seed data |
| `Colisa` | a seeded project | C-DM-37 | Data model, seed data |
| `UBX Roadmap` | a seeded project | C-DM-37 | Data model, seed data |
| `Aera Unity` | a seeded project | C-DM-37 | Data model, seed data |
| `Baba Quiz` | a seeded project | C-DM-37 | Data model, seed data |
| `SEO` | a seeded service | C-DM-37 | Data model, seed data |
| `UX Design` | a seeded service | C-DM-37 | Data model, seed data |
| `Web & Mobile Development` | a seeded service | C-DM-37 | Data model, seed data |
| `Honors` | the fixed rail's vertical label | C-FE-11 | Front-end specification, the fixed rail |
| `View` | the custom cursor's label | C-FE-13 | Front-end specification, the custom cursor |
| `Creative Developer` | the hero eyebrow | C-FE-14 | Front-end specification, the hero |
| `Located in France` | the hero location line | C-FE-14 | Front-end specification, the hero |
| `Scroll down to explore` | the hero scroll prompt | C-FE-14 | Front-end specification, the hero |
| `About` | the about title's first word | C-FE-20 | Front-end specification, the about section |
| `me` | the about title's second word | C-FE-20 | Front-end specification, the about section |
| `5+` | the about figure | C-FE-20 | Front-end specification, the about section |
| `years of experience` | the about figure's label | C-FE-20 | Front-end specification, the about section |
| `LET'S BUILD YOUR IDEA TOGETHER :)` | the contact headline | C-FE-29 | Front-end specification, the contact surface |
| `Further Inquiries` | the contact side column head | C-FE-29 | Front-end specification, the contact surface |
| `Located in France 📍` | the contact side column location line | C-FE-29 | Front-end specification, the contact surface |
| `Social Media` | the contact side column social head | C-FE-29 | Front-end specification, the contact surface |
| `Local Time` | a footer head | C-FE-41 | Front-end specification, the footer |
| `Version` | a footer head | C-FE-41 | Front-end specification, the footer |
| `Resource` | a footer head | C-FE-41 | Front-end specification, the footer |
| `Home` | a navigation target | C-FE-51 | Front-end specification, copy that is pinned |
| `Work` | a navigation target | C-FE-51 | Front-end specification, copy that is pinned |
| `Contact` | a navigation target | C-FE-51 | Front-end specification, copy that is pinned |
| `Linkedin` | a seeded social label | C-FE-51 | Front-end specification, copy that is pinned |
| `Postline` | a seeded social label | C-FE-51 | Front-end specification, copy that is pinned |
| `Showcase` | a seeded social label | C-FE-51 | Front-end specification, copy that is pinned |
| `Elevate user experience through cutting-edge technology and design` | the work headline | C-FE-51 | Front-end specification, copy that is pinned |
| `4173` | the container-internal port | C-DC-01 | Deployment contract, bullet 1 |
| `APP_PUBLIC_PORT` | the outward port variable | C-DC-01 | Deployment contract, bullet 1 |
| `APP_PUBLIC_URL` | the public address variable | C-DC-01 | Deployment contract, bullet 1 |
| `/api` | the API prefix | C-DC-04 | Deployment contract, bullet 2 |
| `/app/USER_README.md` | the credentials file path | C-DC-07 | Deployment contract, bullet 5 |
| `.browser_screenshots/` | a reserved directory | C-DC-08 | Deployment contract, bullet 6 |
| `.downloads/` | a reserved directory | C-DC-08 | Deployment contract, bullet 6 |
| `0.0.0.0` | the bind address | C-DC-11 | Deployment contract, bullet 9 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the three font families | C-UX-21 | named by role with no family given, so the builder chooses three |
| the exact shades of the two grounds | C-UX-11 | described by family and tone with the exact values left to the builder |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 6 | 12 |
| User roles | 9 | 33 |
| Core features | 67 | 195 |
| User flow | 11 | 37 |
| UI and UX notes | 14 | 74 |
| Technical requirements | 19 | 32 |
| Data model | 14 | 46 |
| Front-end specification | 17 | 55 |
| Constraints | 5 | 12 |
| Deployment contract | 14 | 26 |
