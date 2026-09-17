# Checklist: Tallow

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 519
Unpinned values flagged: 5

## C-OV Overview

- [ ] `C-OV-01` `capability` The site turns a brand marketing director carrying a shortlist into a booked introductory call. `src: Overview para 1`
- [ ] `C-OV-02` `data` Tallow is a two-principal advertising agency. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The work index carries seventeen productions, numbered. `src: Overview para 2`
- [ ] `C-OV-04` `capability` Each index entry carries its client. `src: Overview para 2`
- [ ] `C-OV-05` `capability` Each index entry carries its category. `src: Overview para 2`
- [ ] `C-OV-06` `capability` Each index entry carries its running time. `src: Overview para 2`
- [ ] `C-OV-07` `capability` Opening a production gives a case study built around a hero reel. `src: Overview para 2`
- [ ] `C-OV-08` `capability` A case study carries the credits for the crew assembled for that production. `src: Overview para 2`
- [ ] `C-OV-09` `capability` A case study carries galleries of stills. `src: Overview para 2`
- [ ] `C-OV-10` `constraint` Every still in a gallery carries a caption. `src: Overview para 2`
- [ ] `C-OV-11` `capability` The index flips from a grid of cards to a dense list without leaving the page. `src: Overview para 2`
- [ ] `C-OV-12` `capability` The index flips from a dense list back to a grid of cards without leaving the page. `src: Overview para 2`
- [ ] `C-OV-13` `constraint` The index flip changes the shape only, leaving the same seventeen productions in the same order. `src: Overview para 2`
- [ ] `C-OV-14` `capability` One conversion action appears on every route. `src: Overview para 3`
- [ ] `C-OV-15` `constraint` No second conversion action competes with the single call to action. `src: Overview para 3`
- [ ] `C-OV-16` `capability` The single conversion action books a fifteen minute call. `src: Overview para 3`
- [ ] `C-OV-17` `capability` The agency publishes its availability. `src: Overview para 3`
- [ ] `C-OV-18` `capability` A visitor picks a slot from the published availability. `src: Overview para 3`
- [ ] `C-OV-19` `capability` The chosen slot is held over the period a visitor types their details. `src: Overview para 3`
- [ ] `C-OV-20` `capability` Confirming a slot sends the visitor a message. `src: Overview para 3`
- [ ] `C-OV-21` `role` The two people who run the agency sign in to read what has been booked. `src: Overview para 3`
- [ ] `C-OV-22` `role` The two people who run the agency sign in to publish more time. `src: Overview para 3`
- [ ] `C-OV-23` `constraint` A hold expires. `src: Overview para 4`
- [ ] `C-OV-24` `constraint` A repeat submission does not make a second booking. `src: Overview para 4`
- [ ] `C-OV-25` `constraint` Two simultaneous confirmations of one slot leave exactly one booking. `src: Overview para 4`

## C-RL User roles

- [ ] `C-RL-01` `role` A `visitor` reads the index in either shape. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A `visitor` opens any case study. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `visitor` watches a film. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A `visitor` reads the about page. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A `visitor` reads the privacy page. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `visitor` books a call. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A `visitor` needs no account for any visitor capability. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A `visitor` cannot read the agency's booking list. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A `visitor` cannot publish availability. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A `visitor` cannot withdraw availability. `src: User roles table row 1`
- [ ] `C-RL-11` `role` A `visitor` cannot see who else has booked a slot. `src: User roles table row 1`
- [ ] `C-RL-12` `role` A `principal` does everything a `visitor` does. `src: User roles table row 2`
- [ ] `C-RL-13` `role` A `principal` signs in. `src: User roles table row 2`
- [ ] `C-RL-14` `role` A `principal` reads the booking list. `src: User roles table row 2`
- [ ] `C-RL-15` `role` A `principal` publishes availability. `src: User roles table row 2`
- [ ] `C-RL-16` `role` A `principal` withdraws a slot nobody has taken. `src: User roles table row 2`
- [ ] `C-RL-17` `role` A `principal` cannot withdraw a slot carrying a confirmed booking. `src: User roles table row 2`
- [ ] `C-RL-18` `role` A `principal` cannot publish availability belonging to the other principal. `src: User roles table row 2`
- [ ] `C-RL-19` `role` A `principal` cannot withdraw availability belonging to the other principal. `src: User roles table row 2`
- [ ] `C-RL-20` `constraint` Authorization is enforced server-side on every mutating endpoint. `src: User roles para after table`
- [ ] `C-RL-21` `constraint` A direct API call from a `visitor` session to any principal-only endpoint is rejected by the server. `src: User roles para after table`
- [ ] `C-RL-22` `constraint` A denied request leaves the protected state unchanged. `src: User roles para after table`
- [ ] `C-RL-23` `constraint` Hiding a button in the interface does not stand in for authorization. `src: User roles para after table`
- [ ] `C-RL-24` `constraint` The product carries no public signup. `src: User roles para 3`
- [ ] `C-RL-25` `constraint` Accounts exist only because seeding creates them. `src: User roles para 3`
- [ ] `C-RL-26` `constraint` The product carries no password reset. `src: User roles para 3`
- [ ] `C-RL-27` `constraint` The product carries no invitation flow. `src: User roles para 3`
- [ ] `C-RL-28` `constraint` Booking requires no account at all. `src: User roles para 3`
- [ ] `C-RL-29` `literal` Every seeded account shares the password `deku-studio-2026`. `src: User roles seed table intro`
- [ ] `C-RL-30` `literal` The address `dara@tallow.agency` is seeded with display name Dara Okonjo. `src: User roles seed table row 1`
- [ ] `C-RL-31` `literal` The address `dara@tallow.agency` is seeded with role `principal`. `src: User roles seed table row 1`
- [ ] `C-RL-32` `literal` The address `otis@tallow.agency` is seeded with display name Otis Vandermeer. `src: User roles seed table row 2`
- [ ] `C-RL-33` `literal` The address `otis@tallow.agency` is seeded with role `principal`. `src: User roles seed table row 2`
- [ ] `C-RL-34` `literal` The address `casey@tallow.agency` is seeded with display name Casey Brandt. `src: User roles seed table row 3`
- [ ] `C-RL-35` `literal` The address `casey@tallow.agency` is seeded with role `visitor`. `src: User roles seed table row 3`

## C-CF Core features

- [ ] `C-CF-01` `capability` Asking for availability returns only slots whose state is `published`. `src: Core features, Booking a call item 1`
- [ ] `C-CF-02` `constraint` Asking for availability returns only slots carrying no confirmed booking. `src: Core features, Booking a call item 1`
- [ ] `C-CF-03` `constraint` A slot already taken is never offered. `src: Core features, Booking a call item 1`
- [ ] `C-CF-04` `capability` Choosing a slot places a hold on that slot. `src: Core features, Booking a call item 2`
- [ ] `C-CF-05` `constraint` A second request to hold a slot carrying a live hold is refused as a conflict. `src: Core features, Booking a call item 2`
- [ ] `C-CF-06` `constraint` A booking attempt on a slot carrying another caller's live hold is refused as a conflict. `src: Core features, Booking a call item 2`
- [ ] `C-CF-07` `literal` A hold lasts `600` seconds from creation. `src: Core features, Booking a call item 3`
- [ ] `C-CF-08` `capability` A slot whose hold has lapsed is offered again. `src: Core features, Booking a call item 3`
- [ ] `C-CF-09` `constraint` Confirming against a lapsed hold is refused as gone rather than silently succeeding. `src: Core features, Booking a call item 3`
- [ ] `C-CF-10` `capability` Confirming a held slot creates one booking with status `confirmed`. `src: Core features, Booking a call item 4`
- [ ] `C-CF-11` `data` A confirmed booking records the attendee's name. `src: Core features, Booking a call item 4`
- [ ] `C-CF-12` `data` A confirmed booking records the attendee's address. `src: Core features, Booking a call item 4`
- [ ] `C-CF-13` `data` A confirmed booking records the attendee's timezone. `src: Core features, Booking a call item 4`
- [ ] `C-CF-14` `data` A confirmed booking records the attendee's agenda. `src: Core features, Booking a call item 4`
- [ ] `C-CF-15` `constraint` Two confirmations of the same slot arriving at the same instant do not both succeed. `src: Core features, Booking a call item 5`
- [ ] `C-CF-16` `constraint` Exactly one confirmed booking exists for a contested slot afterwards. `src: Core features, Booking a call item 5`
- [ ] `C-CF-17` `capability` The caller losing a contested slot is refused as a conflict. `src: Core features, Booking a call item 5`
- [ ] `C-CF-18` `constraint` The one-confirmation rule holds at the database level rather than only in application logic. `src: Core features, Booking a call item 5`
- [ ] `C-CF-19` `constraint` A rejected confirmation leaves no orphaned hold. `src: Core features, Booking a call item 5`
- [ ] `C-CF-20` `constraint` A rejected confirmation leaves no second booking row. `src: Core features, Booking a call item 5`
- [ ] `C-CF-21` `capability` A booking request carries an idempotency key. `src: Core features, Booking a call item 6`
- [ ] `C-CF-22` `capability` Submitting the same idempotency key twice returns the booking already created. `src: Core features, Booking a call item 6`
- [ ] `C-CF-23` `constraint` Submitting the same idempotency key twice creates no second booking. `src: Core features, Booking a call item 6`
- [ ] `C-CF-24` `constraint` The idempotency rule holds whatever the interval between the two submissions. `src: Core features, Booking a call item 6`
- [ ] `C-CF-25` `literal` An agenda outside one to `2000` characters is rejected as invalid. `src: Core features, Booking a call item 7`
- [ ] `C-CF-26` `literal` An attendee name outside two to `80` characters is rejected as invalid. `src: Core features, Booking a call item 7`
- [ ] `C-CF-27` `constraint` A booking rejected for an out-of-range value writes nothing. `src: Core features, Booking a call item 7`
- [ ] `C-CF-28` `constraint` Booking requires no account. `src: Core features, Booking a call item 8`
- [ ] `C-CF-29` `capability` A signed-out visitor completes the whole booking flow. `src: Core features, Booking a call item 8`
- [ ] `C-CF-30` `capability` A booking reaching `confirmed` sends exactly one message. `src: Core features, The confirmation message item 1`
- [ ] `C-CF-31` `constraint` The confirmation message is addressed to that booking's own attendee address. `src: Core features, The confirmation message item 2`
- [ ] `C-CF-32` `constraint` The confirmation message carries no cc. `src: Core features, The confirmation message item 2`
- [ ] `C-CF-33` `constraint` The confirmation message carries no bcc. `src: Core features, The confirmation message item 2`
- [ ] `C-CF-34` `literal` The confirmation subject begins `Call confirmed:` followed by a space, then the principal's display name. `src: Core features, The confirmation message item 3`
- [ ] `C-CF-35` `literal` A call booked with Dara Okonjo carries the subject `Call confirmed: Dara Okonjo`. `src: Core features, The confirmation message item 3`
- [ ] `C-CF-36` `constraint` The confirmation body is not empty. `src: Core features, The confirmation message item 4`
- [ ] `C-CF-37` `capability` The confirmation body names the principal. `src: Core features, The confirmation message item 4`
- [ ] `C-CF-38` `capability` The confirmation body names the start time. `src: Core features, The confirmation message item 4`
- [ ] `C-CF-39` `constraint` Placing a hold sends no mail. `src: Core features, The confirmation message item 5`
- [ ] `C-CF-40` `constraint` A hold lapsing sends no mail. `src: Core features, The confirmation message item 5`
- [ ] `C-CF-41` `constraint` Withdrawing an untaken slot sends no mail. `src: Core features, The confirmation message item 5`
- [ ] `C-CF-42` `constraint` A refused booking sends no mail. `src: Core features, The confirmation message item 5`
- [ ] `C-CF-43` `constraint` Nothing else in the product sends mail. `src: Core features, The confirmation message item 5`
- [ ] `C-CF-44` `capability` The work index returns all seventeen productions in `sort_index` order. `src: Core features, The index and its two orderings item 1`
- [ ] `C-CF-45` `literal` The work index numbers productions from `01` to `17`. `src: Core features, The index and its two orderings item 1`
- [ ] `C-CF-46` `capability` The home feed returns the eleven productions carrying `featured_on_home`. `src: Core features, The index and its two orderings item 2`
- [ ] `C-CF-47` `capability` The home feed returns those eleven productions in `home_sort_index` order. `src: Core features, The index and its two orderings item 2`
- [ ] `C-CF-48` `constraint` The index ordering is independent of the home ordering. `src: Core features, The index and its two orderings item 3`
- [ ] `C-CF-49` `constraint` The home feed is not the first eleven of the index. `src: Core features, The index and its two orderings item 3`
- [ ] `C-CF-50` `constraint` The home feed is not the index order with six rows removed. `src: Core features, The index and its two orderings item 3`
- [ ] `C-CF-51` `constraint` A build deriving either ordering from the other is wrong. `src: Core features, The index and its two orderings item 3`
- [ ] `C-CF-52` `data` A production carrying `featured_on_home` also carries a `home_sort_index`. `src: Core features, The index and its two orderings item 4`
- [ ] `C-CF-53` `data` A production without `featured_on_home` carries no `home_sort_index`. `src: Core features, The index and its two orderings item 4`
- [ ] `C-CF-54` `constraint` Flipping the index shape leaves the membership unchanged. `src: Core features, The index and its two orderings item 5`
- [ ] `C-CF-55` `constraint` Flipping the index shape leaves the order unchanged. `src: Core features, The index and its two orderings item 5`
- [ ] `C-CF-56` `constraint` The same seventeen productions appear in both index shapes. `src: Core features, The index and its two orderings item 5`
- [ ] `C-CF-57` `capability` The work count beside the navigation comes from the stored rows. `src: Core features, The index and its two orderings item 6`
- [ ] `C-CF-58` `capability` The count beside the index heading comes from the stored rows. `src: Core features, The index and its two orderings item 6`
- [ ] `C-CF-59` `capability` The count on the home feed comes from the stored rows. `src: Core features, The index and its two orderings item 6`
- [ ] `C-CF-60` `capability` Opening a production at its own address returns its title. `src: Core features, A case study item 1`
- [ ] `C-CF-61` `capability` Opening a production at its own address returns its client. `src: Core features, A case study item 1`
- [ ] `C-CF-62` `capability` Opening a production at its own address returns its category. `src: Core features, A case study item 1`
- [ ] `C-CF-63` `capability` Opening a production at its own address returns its running time. `src: Core features, A case study item 1`
- [ ] `C-CF-64` `capability` Opening a production at its own address returns its year. `src: Core features, A case study item 1`
- [ ] `C-CF-65` `capability` Opening a production at its own address returns its hero reel. `src: Core features, A case study item 1`
- [ ] `C-CF-66` `capability` Opening a production at its own address returns its credits in stored order. `src: Core features, A case study item 1`
- [ ] `C-CF-67` `capability` Opening a production at its own address returns its galleries. `src: Core features, A case study item 1`
- [ ] `C-CF-68` `data` Every gallery still carries a caption. `src: Core features, A case study item 2`
- [ ] `C-CF-69` `constraint` A gallery still with no caption cannot be stored. `src: Core features, A case study item 2`
- [ ] `C-CF-70` `data` The caption requirement lives in the stored data rather than only in the interface. `src: Core features, A case study item 2`
- [ ] `C-CF-71` `capability` Galleries are returned in their stored order. `src: Core features, A case study item 3`
- [ ] `C-CF-72` `capability` The stills within a gallery are returned in their stored order. `src: Core features, A case study item 3`
- [ ] `C-CF-73` `capability` An unknown production slug renders the product's own not-found page. `src: Core features, A case study item 4`
- [ ] `C-CF-74` `constraint` An unknown production slug renders neither a blank page nor an unstyled error. `src: Core features, A case study item 4`
- [ ] `C-CF-75` `capability` A principal signs in. `src: Core features, The principal surfaces item 1`
- [ ] `C-CF-76` `capability` The booking list shows the attendee for every confirmed booking against that principal. `src: Core features, The principal surfaces item 1`
- [ ] `C-CF-77` `capability` The booking list shows the time for every confirmed booking against that principal. `src: Core features, The principal surfaces item 1`
- [ ] `C-CF-78` `capability` The booking list shows the slot for every confirmed booking against that principal. `src: Core features, The principal surfaces item 1`
- [ ] `C-CF-79` `capability` A principal publishes further availability. `src: Core features, The principal surfaces item 2`
- [ ] `C-CF-80` `capability` Newly published availability appears in what visitors are offered. `src: Core features, The principal surfaces item 2`
- [ ] `C-CF-81` `capability` A principal withdraws a slot nobody has taken. `src: Core features, The principal surfaces item 3`
- [ ] `C-CF-82` `capability` A withdrawn slot stops being offered. `src: Core features, The principal surfaces item 3`
- [ ] `C-CF-83` `constraint` Withdrawing a slot that carries a confirmed booking is refused. `src: Core features, The principal surfaces item 4`
- [ ] `C-CF-84` `constraint` A confirmed booking is never taken away silently. `src: Core features, The principal surfaces item 4`
- [ ] `C-CF-85` `ui` The refusal to withdraw a booked slot says why the withdrawal was refused. `src: Core features, The principal surfaces item 4`
- [ ] `C-CF-86` `role` A principal acting on the other principal's availability is denied. `src: Core features, The principal surfaces item 5`
- [ ] `C-CF-87` `constraint` A denied cross-principal action leaves the row unchanged. `src: Core features, The principal surfaces item 5`
- [ ] `C-CF-88` `role` A `visitor` session asking for any principal endpoint is denied by the server. `src: Core features, The principal surfaces item 6`
- [ ] `C-CF-89` `constraint` A denied visitor request changes nothing. `src: Core features, The principal surfaces item 6`
- [ ] `C-CF-90` `capability` A privacy page states what the agency records about a person who books. `src: Core features, The public surface item 1`
- [ ] `C-CF-91` `capability` The privacy page is reachable from the footer of every route. `src: Core features, The public surface item 2`
- [ ] `C-CF-92` `constraint` Every internal link on every public route resolves. `src: Core features, The public surface item 2`
- [ ] `C-CF-93` `capability` An address matching no route renders the product's own not-found page. `src: Core features, The public surface item 3`
- [ ] `C-CF-94` `ui` The not-found page carries a way back. `src: Core features, The public surface item 3`
- [ ] `C-CF-95` `constraint` An address matching no route answers as not found rather than as success. `src: Core features, The public surface item 3`
- [ ] `C-CF-96` `ui` Every form rejects invalid input inline. `src: Core features, The public surface item 4`
- [ ] `C-CF-97` `ui` Every form names the wrong field in words beside that field. `src: Core features, The public surface item 4`
- [ ] `C-CF-98` `constraint` A form rejecting invalid input writes nothing. `src: Core features, The public surface item 4`
- [ ] `C-CF-99` `capability` Sign-in takes an email with a password. `src: Core features, Auth intro`
- [ ] `C-CF-100` `literal` A successful sign-in returns a bearer token in a field named `access_token`. `src: Core features, Auth intro`
- [ ] `C-CF-101` `capability` The client sends the bearer token on every authenticated request. `src: Core features, Auth intro`
- [ ] `C-CF-102` `constraint` Passwords are stored hashed, never in plain text. `src: Core features, Auth intro`
- [ ] `C-CF-103` `constraint` No endpoint returns a password. `src: Core features, Auth intro`
- [ ] `C-CF-104` `constraint` No endpoint returns a password hash. `src: Core features, Auth intro`
- [ ] `C-CF-105` `constraint` A token is valid for twenty-four hours from issue. `src: Core features, Auth intro`
- [ ] `C-CF-106` `constraint` An expired token is denied exactly as a missing one. `src: Core features, Auth intro`
- [ ] `C-CF-107` `constraint` A malformed token is denied exactly as a missing one. `src: Core features, Auth intro`
- [ ] `C-CF-108` `literal` Signing in with a seeded email plus `deku-studio-2026` succeeds. `src: Core features, Auth item 1`
- [ ] `C-CF-109` `literal` A successful sign-in response carries `access_token`. `src: Core features, Auth item 1`
- [ ] `C-CF-110` `constraint` Signing in with a seeded email plus any other password is denied. `src: Core features, Auth item 2`
- [ ] `C-CF-111` `constraint` A denied sign-in response does not reveal whether the address exists. `src: Core features, Auth item 2`
- [ ] `C-CF-112` `constraint` Signing in with an unknown address is denied identically to a wrong password. `src: Core features, Auth item 3`
- [ ] `C-CF-113` `capability` Reading the session with a valid token returns that account's address. `src: Core features, Auth item 4`
- [ ] `C-CF-114` `capability` Reading the session with a valid token returns that account's display name. `src: Core features, Auth item 4`
- [ ] `C-CF-115` `capability` Reading the session with a valid token returns that account's role. `src: Core features, Auth item 4`
- [ ] `C-CF-116` `constraint` Reading the session without a token is denied. `src: Core features, Auth item 4`

## C-UF User flow

- [ ] `C-UF-01` `capability` The route `/` serves the home feed of eleven productions. `src: User flow, Routes table row 1`
- [ ] `C-UF-02` `capability` The route `/` carries the agency band, the information band, the contact band. `src: User flow, Routes table row 1`
- [ ] `C-UF-03` `capability` The route `/work` serves all seventeen productions, numbered. `src: User flow, Routes table row 2`
- [ ] `C-UF-04` `capability` The route `/work` offers a grid shape. `src: User flow, Routes table row 2`
- [ ] `C-UF-05` `capability` The route `/work` offers a list shape. `src: User flow, Routes table row 2`
- [ ] `C-UF-06` `capability` The route `/work/{slug}` serves one case study with hero reel, credits, captioned galleries. `src: User flow, Routes table row 3`
- [ ] `C-UF-07` `capability` The route `/about` states what the agency does, how the agency works, who runs the agency. `src: User flow, Routes table row 4`
- [ ] `C-UF-08` `capability` The route `/contact` sets the agency address large beside the booking entry point. `src: User flow, Routes table row 5`
- [ ] `C-UF-09` `capability` The route `/book` serves the booking panel as its own address. `src: User flow, Routes table row 6`
- [ ] `C-UF-10` `capability` The route `/privacy` states what the agency records about a person who books. `src: User flow, Routes table row 7`
- [ ] `C-UF-11` `capability` The route `/legal` serves the disclaimer. `src: User flow, Routes table row 8`
- [ ] `C-UF-12` `capability` The route `/sign-in` serves sign in. `src: User flow, Routes table row 9`
- [ ] `C-UF-13` `capability` The route `/studio` serves the principal's booking list. `src: User flow, Routes table row 10`
- [ ] `C-UF-14` `role` The route `/studio` requires a `principal`. `src: User flow, Routes table row 10`
- [ ] `C-UF-15` `capability` The route `/studio/availability` publishes availability. `src: User flow, Routes table row 11`
- [ ] `C-UF-16` `capability` The route `/studio/availability` withdraws availability. `src: User flow, Routes table row 11`
- [ ] `C-UF-17` `role` The route `/studio/availability` requires a `principal`. `src: User flow, Routes table row 11`
- [ ] `C-UF-18` `constraint` The nine public routes listed in the table need no auth. `src: User flow, Routes table Auth column`
- [ ] `C-UF-19` `capability` A signed-out visitor opening `/studio` is sent to `/sign-in`. `src: User flow, Entry and redirects`
- [ ] `C-UF-20` `capability` A signed-out visitor opening `/studio/availability` is sent to `/sign-in`. `src: User flow, Entry and redirects`
- [ ] `C-UF-21` `capability` A successful sign-in lands on the address originally asked for rather than a generic home. `src: User flow, Entry and redirects`
- [ ] `C-UF-22` `ui` A signed-in `visitor` opening a studio route is shown a refusal saying the surface belongs to the agency. `src: User flow, Entry and redirects`
- [ ] `C-UF-23` `constraint` A signed-in `visitor` refused at a studio route is not sent to sign in again. `src: User flow, Entry and redirects`
- [ ] `C-UF-24` `capability` Signing out returns the visitor to `/`. `src: User flow, Entry and redirects`
- [ ] `C-UF-25` `capability` Signing out discards the token. `src: User flow, Entry and redirects`
- [ ] `C-UF-26` `ui` A token expiring mid-action leaves the principal on the same surface. `src: User flow, Entry and redirects`
- [ ] `C-UF-27` `ui` A token expiring mid-action shows a message saying the session ended. `src: User flow, Entry and redirects`
- [ ] `C-UF-28` `ui` A token expiring mid-action offers a control to sign in again. `src: User flow, Entry and redirects`
- [ ] `C-UF-29` `ui` A hold lapsing under an open booking panel stops the countdown. `src: User flow, Entry and redirects`
- [ ] `C-UF-30` `ui` A hold lapsing under an open booking panel disables confirm. `src: User flow, Entry and redirects`
- [ ] `C-UF-31` `ui` A hold lapsing under an open booking panel offers to hold again. `src: User flow, Entry and redirects`
- [ ] `C-UF-32` `ui` A hold lapsing under an open booking panel keeps every detail already typed. `src: User flow, Entry and redirects`
- [ ] `C-UF-33` `ui` The home feed shows eleven productions beginning with Vertical Mile, then Master the Route. `src: User flow, Journeys item 1`
- [ ] `C-UF-34` `literal` The work index shows seventeen productions numbered `01` to `17`. `src: User flow, Journeys item 1`
- [ ] `C-UF-35` `ui` The work index begins with Vertical Mile. `src: User flow, Journeys item 1`
- [ ] `C-UF-36` `ui` The work index ends with Steppe Space Shuttle. `src: User flow, Journeys item 1`
- [ ] `C-UF-37` `ui` Flipping to the list shape shows the same seventeen productions in the same order. `src: User flow, Journeys item 1`
- [ ] `C-UF-38` `ui` Opening `norvel-drift` shows its credits. `src: User flow, Journeys item 1`
- [ ] `C-UF-39` `ui` Opening `norvel-drift` shows its captioned galleries. `src: User flow, Journeys item 1`
- [ ] `C-UF-40` `ui` The single call to action opens the booking panel over the page. `src: User flow, Journeys item 2`
- [ ] `C-UF-41` `ui` Picking a published slot starts a countdown. `src: User flow, Journeys item 2`
- [ ] `C-UF-42` `ui` The details form takes a name, an address, a timezone, an agenda. `src: User flow, Journeys item 2`
- [ ] `C-UF-43` `ui` Confirming replaces the panel's content in place with a confirmation naming Dara Okonjo beside the time. `src: User flow, Journeys item 2`
- [ ] `C-UF-44` `literal` The attendee address holds one message whose subject is `Call confirmed: Dara Okonjo`. `src: User flow, Journeys item 2`
- [ ] `C-UF-45` `ui` The second of two visitors holding one slot in turn is refused as a conflict. `src: User flow, Journeys item 3`
- [ ] `C-UF-46` `ui` The grid refreshes in place after a conflict refusal. `src: User flow, Journeys item 3`
- [ ] `C-UF-47` `ui` The details already typed are kept after a conflict refusal. `src: User flow, Journeys item 3`
- [ ] `C-UF-48` `ui` Opening `/studio` as `dara@tallow.agency` lists the booking with its attendee beside its time. `src: User flow, Journeys item 4`
- [ ] `C-UF-49` `ui` Withdrawing an untaken slot at `/studio/availability` stops that slot being offered. `src: User flow, Journeys item 4`
- [ ] `C-UF-50` `constraint` Attempting to withdraw a slot carrying a confirmed booking is refused, leaving the booking untouched. `src: User flow, Journeys item 4`
- [ ] `C-UF-51` `ui` Opening `/studio` as `casey@tallow.agency` is refused as an agency surface. `src: User flow, Journeys item 5`
- [ ] `C-UF-52` `constraint` Asking the availability endpoint directly with a visitor token is denied, changing no row. `src: User flow, Journeys item 5`
- [ ] `C-UF-53` `ui` Every list carries an empty state written for that list. `src: User flow, States`
- [ ] `C-UF-54` `ui` A principal with nothing booked is told no call has been booked yet. `src: User flow, States`
- [ ] `C-UF-55` `ui` A day with no free slot is told the day is full rather than shown an empty grid. `src: User flow, States`
- [ ] `C-UF-56` `constraint` The index is never empty, because all seventeen productions are seeded. `src: User flow, States`
- [ ] `C-UF-57` `ui` Every route carries a loading state holding the final layout's shape. `src: User flow, States`
- [ ] `C-UF-58` `constraint` Nothing jumps when content arrives. `src: User flow, States`
- [ ] `C-UF-59` `ui` An unknown slug reaches the product's own not-found page. `src: User flow, States`
- [ ] `C-UF-60` `ui` An unknown address reaches the product's own not-found page. `src: User flow, States`
- [ ] `C-UF-61` `ui` The not-found page carries a link home. `src: User flow, States`
- [ ] `C-UF-62` `ui` The not-found page carries a link to the work index. `src: User flow, States`
- [ ] `C-UF-63` `ui` A failed request says what failed. `src: User flow, States`
- [ ] `C-UF-64` `ui` A failed request offers the action again. `src: User flow, States`
- [ ] `C-UF-65` `constraint` No route leaves the visitor on a blank page. `src: User flow, States`
- [ ] `C-UF-66` `constraint` No route leaves the visitor on an unstyled error. `src: User flow, States`

## C-UX UI and UX notes

- [ ] `C-UX-01` `literal` The design direction is `playful-consumer`. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The mood is bright, energetic, consumer-grade. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The type personality is a geometric sans carrying one characterful display face. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `literal` The motion character is `springy`. `src: UI/UX notes para 1`
- [ ] `C-UX-05` `ui` The density is comfortable. `src: UI/UX notes para 1`
- [ ] `C-UX-06` `ui` The layout archetype is a persistent rail beside the content column. `src: UI/UX notes para 1`
- [ ] `C-UX-07` `ui` A marketing director comes away believing these people make excellent film. `src: UI/UX notes, North star`
- [ ] `C-UX-08` `ui` A marketing director never has to hunt for how to talk to the agency. `src: UI/UX notes, North star`
- [ ] `C-UX-09` `ui` The register is editorial, with the film as the subject. `src: UI/UX notes, Register`
- [ ] `C-UX-10` `ui` The interface is the frame around the picture rather than the picture. `src: UI/UX notes, Register`
- [ ] `C-UX-11` `ui` The ground is dark, near-neutral. `src: UI/UX notes, Ground and the four meanings para 1`
- [ ] `C-UX-12` `ui` Two slightly deeper variants of the ground mark where one band of content ends. `src: UI/UX notes, Ground and the four meanings para 1`
- [ ] `C-UX-13` `ui` Cards sit on a surface barely lighter than the ground. `src: UI/UX notes, Ground and the four meanings para 1`
- [ ] `C-UX-14` `constraint` A card stays visibly separate from the ground without a border. `src: UI/UX notes, Ground and the four meanings para 1`
- [ ] `C-UX-15` `constraint` A card stays visibly separate from the ground without a shadow. `src: UI/UX notes, Ground and the four meanings para 1`
- [ ] `C-UX-16` `ui` Card separation rests on the difference between the card surface, the ground alone. `src: UI/UX notes, Ground and the four meanings para 1`
- [ ] `C-UX-17` `ui` Four colours carry meaning, each belonging to exactly one job. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-18` `ui` One accent marks the single call to action. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-19` `constraint` The call-to-action accent is the only saturated colour anywhere in the interface. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-20` `ui` One colour marks a refusal. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-21` `ui` One colour marks a hold that is still running. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-22` `ui` One colour marks a slot already taken. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-23` `constraint` A surface carrying none of those four meanings borrows none of those four colours. `src: UI/UX notes, Ground and the four meanings para 2`
- [ ] `C-UX-24` `literal` The `energetic` quality is scoped to the one call-to-action accent. `src: UI/UX notes, Ground and the four meanings para 3`
- [ ] `C-UX-25` `ui` The call to action is the brightest thing on every route. `src: UI/UX notes, Ground and the four meanings para 3`
- [ ] `C-UX-26` `constraint` Nothing else competes with the call to action. `src: UI/UX notes, Ground and the four meanings para 3`
- [ ] `C-UX-27` `ui` Every other button in the product is quiet. `src: UI/UX notes, Ground and the four meanings para 3`
- [ ] `C-UX-28` `ui` Each page leads with one primary action, visually distinct from every secondary one. `src: UI/UX notes, Ground and the four meanings para 3`
- [ ] `C-UX-29` `constraint` No page carries a second action dressed to look equal to the primary one. `src: UI/UX notes, Ground and the four meanings para 3`
- [ ] `C-UX-30` `ui` Text carries three levels of presence, no more. `src: UI/UX notes, Ground and the four meanings para 4`
- [ ] `C-UX-31` `ui` The three text levels are the thing being read, the label naming the thing, the quiet metadata beneath. `src: UI/UX notes, Ground and the four meanings para 4`
- [ ] `C-UX-32` `constraint` The product ships one fully designed dark appearance, no second one. `src: UI/UX notes, Mode`
- [ ] `C-UX-33` `constraint` The product carries no light mode. `src: UI/UX notes, Mode`
- [ ] `C-UX-34` `constraint` The product carries no theme switch. `src: UI/UX notes, Mode`
- [ ] `C-UX-35` `ui` Every contrast floor is stated against the single dark appearance. `src: UI/UX notes, Mode`
- [ ] `C-UX-36` `literal` A `geometric sans` carries the whole interface. `src: UI/UX notes, Type`
- [ ] `C-UX-37` `ui` One characterful display face is reserved for the largest type only. `src: UI/UX notes, Type`
- [ ] `C-UX-38` `ui` The display face sets a production title on its own case study. `src: UI/UX notes, Type`
- [ ] `C-UX-39` `ui` The display face sets the agency's address on the contact route. `src: UI/UX notes, Type`
- [ ] `C-UX-40` `ui` The agency's address on the contact route is set enormous. `src: UI/UX notes, Type`
- [ ] `C-UX-41` `constraint` Nothing between those two sizes uses the display face. `src: UI/UX notes, Type`
- [ ] `C-UX-42` `ui` Section labels are set in a monospace, small, in square brackets. `src: UI/UX notes, Type`
- [ ] `C-UX-43` `ui` Counts are set in a monospace, small, in square brackets. `src: UI/UX notes, Type`
- [ ] `C-UX-44` `constraint` Monospace appears nowhere else in the product. `src: UI/UX notes, Type`
- [ ] `C-UX-45` `ui` Running times line up in a column wherever running times stack. `src: UI/UX notes, Type`
- [ ] `C-UX-46` `ui` Ordinals line up in a column wherever ordinals stack. `src: UI/UX notes, Type`
- [ ] `C-UX-47` `ui` The gap between two bands of content is roughly three times the gap beneath a heading. `src: UI/UX notes, Density and rhythm`
- [ ] `C-UX-48` `ui` The gap between bands about halves on a narrow screen. `src: UI/UX notes, Density and rhythm`
- [ ] `C-UX-49` `constraint` Every gap derives from one base unit. `src: UI/UX notes, Density and rhythm`
- [ ] `C-UX-50` `constraint` No gap takes a value that is not a multiple of the base unit. `src: UI/UX notes, Density and rhythm`
- [ ] `C-UX-51` `ui` Bands read as separate at a glance without a dividing line. `src: UI/UX notes, Density and rhythm`
- [ ] `C-UX-52` `literal` The `springy` character is bound to the booking confirmation, to nothing else. `src: UI/UX notes, Motion`
- [ ] `C-UX-53` `ui` The booking confirmation settles into place with a slight overshoot, once. `src: UI/UX notes, Motion`
- [ ] `C-UX-54` `constraint` A film card being pointed at does not overshoot. `src: UI/UX notes, Motion`
- [ ] `C-UX-55` `constraint` A panel opening does not overshoot. `src: UI/UX notes, Motion`
- [ ] `C-UX-56` `constraint` No other surface in the product overshoots. `src: UI/UX notes, Motion`
- [ ] `C-UX-57` `ui` The index flip carries no springy character. `src: UI/UX notes, Motion`
- [ ] `C-UX-58` `ui` Each card travels from where the card was to where the card lands across the index flip. `src: UI/UX notes, Motion`
- [ ] `C-UX-59` `constraint` Cards do not fade out across the index flip. `src: UI/UX notes, Motion`
- [ ] `C-UX-60` `ui` The hold countdown runs continuously, visibly, for the life of a hold. `src: UI/UX notes, Motion`
- [ ] `C-UX-61` `ui` A reader who has asked their system to reduce motion gets the whole product with every transition removed. `src: UI/UX notes, Motion`
- [ ] `C-UX-62` `ui` Under reduced motion the index flip becomes an instant relayout. `src: UI/UX notes, Motion`
- [ ] `C-UX-63` `ui` Under reduced motion the confirmation simply appears. `src: UI/UX notes, Motion`
- [ ] `C-UX-64` `ui` Under reduced motion the countdown remains a live number. `src: UI/UX notes, Motion`
- [ ] `C-UX-65` `ui` The rail is persistent beside the content on every route. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-66` `ui` The rail carries the wordmark. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-67` `ui` The rail carries the four destinations. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-68` `ui` The rail carries the live work count beside the work link. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-69` `ui` The rail carries the single call to action. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-70` `constraint` The rail does not scroll with the page. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-71` `ui` On a narrow viewport the rail collapses to the wordmark beside one control. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-72` `ui` The rail's narrow-viewport control opens the rail as a full-height panel. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-73` `ui` The call to action stays reachable on a narrow viewport without opening the rail. `src: UI/UX notes, The surfaces, The rail`
- [ ] `C-UX-74` `ui` The work index uses a split shape, the list of productions beside the one currently selected. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-75` `constraint` Choosing a production does not throw away the list. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-76` `ui` Each index row carries its ordinal, title, client, category, running time. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-77` `ui` In the grid shape each row becomes a card with the still above the same metadata. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-78` `ui` The grid shape holds one column on a phone. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-79` `ui` The grid shape holds two columns on a tablet. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-80` `ui` The grid shape holds three columns on a wide screen. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-81` `constraint` The grid gap never collapses. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-82` `constraint` The grid layout holds at every width between the named sizes. `src: UI/UX notes, The surfaces, The work index`
- [ ] `C-UX-83` `ui` A case study leads with the hero reel at the full width of the content column. `src: UI/UX notes, The surfaces, A case study`
- [ ] `C-UX-84` `ui` A case study places the credits after the hero reel as a plain two-column list of role beside name. `src: UI/UX notes, The surfaces, A case study`
- [ ] `C-UX-85` `ui` A case study places the galleries after the credits. `src: UI/UX notes, The surfaces, A case study`
- [ ] `C-UX-86` `ui` Each gallery sits under its own bracketed label. `src: UI/UX notes, The surfaces, A case study`
- [ ] `C-UX-87` `ui` Every still carries its caption as visible text rather than only as a text alternative. `src: UI/UX notes, The surfaces, A case study`
- [ ] `C-UX-88` `ui` The booking panel slides over whatever was being read rather than replacing the page. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-89` `ui` The booking panel keeps the visitor's place. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-90` `ui` A month view shows only days carrying a free slot. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-91` `ui` Times are shown in the visitor's own zone with the zone named. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-92` `ui` The agency's own city is stated beside the visitor's zone. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-93` `ui` Choosing a time starts the countdown. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-94` `ui` The details form sits under the chosen time. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-95` `constraint` The details form never sits on a separate step. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-96` `ui` On success the panel's content is replaced in place by a confirmation naming the principal beside the time. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-97` `constraint` The confirmation is a banner within the panel rather than a new page. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-98` `constraint` The confirmation does not disappear on its own. `src: UI/UX notes, The surfaces, The booking panel`
- [ ] `C-UX-99` `ui` The principal surfaces are quiet, dense, built for a person checking their day. `src: UI/UX notes, The surfaces, The principal surfaces`
- [ ] `C-UX-100` `ui` The booking list is a table of attendee, time, slot. `src: UI/UX notes, The surfaces, The principal surfaces`
- [ ] `C-UX-101` `constraint` The principal surfaces carry no hero. `src: UI/UX notes, The surfaces, The principal surfaces`
- [ ] `C-UX-102` `constraint` The principal surfaces carry no oversized heading. `src: UI/UX notes, The surfaces, The principal surfaces`
- [ ] `C-UX-103` `ui` One primary action style carries the accent. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-104` `ui` One quieter alternative action style carries neither the accent nor the primary treatment. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-105` `ui` Both action styles have resting, pointed-at, pressed, focused, unavailable states. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-106` `constraint` An unavailable control is never signalled by colour alone. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-107` `ui` An unavailable control loses its fill. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-108` `ui` An unavailable control takes a cursor saying the control cannot be used. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-109` `ui` Every field has resting, focused, filled, invalid, disabled states. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-110` `ui` An invalid field says what is wrong beneath the field in words rather than only changing colour. `src: UI/UX notes, Components and their states`
- [ ] `C-UX-111` `ui` Body text clears the WCAG AA contrast floor against whichever ground sits behind. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-112` `ui` Every control label clears the WCAG AA contrast floor against whichever ground sits behind. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-113` `ui` Large type clears the large-text contrast floor. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-114` `ui` Every control is reachable by keyboard navigation in the order the control reads on the page. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-115` `ui` The focus indicator is visible against all of the grounds rather than only the darkest. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-116` `ui` Every still carries its caption as its text alternative. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-117` `ui` The film player is operable from the keyboard. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-118` `ui` Each film player control is labelled. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-119` `ui` The countdown is announced as the countdown changes rather than only drawn. `src: UI/UX notes, Accessibility`
- [ ] `C-UX-120` `ui` The layout holds from a narrow phone viewport to a wide desktop. `src: UI/UX notes, Responsive`
- [ ] `C-UX-121` `constraint` The layout survives every width between the chosen breakpoints. `src: UI/UX notes, Responsive`
- [ ] `C-UX-122` `constraint` No surface scrolls horizontally at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-123` `ui` The hero reel scales to the column rather than pushing the column. `src: UI/UX notes, Responsive`
- [ ] `C-UX-124` `ui` Every navigation target stays reachable at a narrow viewport. `src: UI/UX notes, Responsive`
- [ ] `C-UX-125` `constraint` The product does not look like a dashboard. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-126` `constraint` The product's chrome does not compete with the film. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-127` `constraint` Decoration does not stand in for work. `src: UI/UX notes, What it must not look like`
- [ ] `C-UX-128` `constraint` The layout is not borrowed from an unrelated subject. `src: UI/UX notes, What it must not look like`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The application is one client-routed document against a JSON API. `src: Technical requirements para 1`
- [ ] `C-TR-02` `constraint` The index runs without a full page load. `src: Technical requirements para 1`
- [ ] `C-TR-03` `constraint` The case studies run without a full page load. `src: Technical requirements para 1`
- [ ] `C-TR-04` `constraint` The booking panel runs without a full page load. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` The frontend is Vue 3 with Vite. `src: Technical requirements stack list`
- [ ] `C-TR-06` `contract` The backend is Litestar. `src: Technical requirements stack list`
- [ ] `C-TR-07` `contract` The backend serves one JSON API under the `/api` prefix on the same origin. `src: Technical requirements stack list`
- [ ] `C-TR-08` `contract` The datastore is PostgreSQL, reached through `DATABASE_URL`. `src: Technical requirements stack list`
- [ ] `C-TR-09` `contract` Mail goes over real SMTP to Mailpit. `src: Technical requirements stack list`
- [ ] `C-TR-10` `contract` SMTP is reached through `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`. `src: Technical requirements stack list`
- [ ] `C-TR-11` `contract` The environment carries `AUTH_SECRET`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT`. `src: Technical requirements stack list`
- [ ] `C-TR-12` `constraint` PostgreSQL is already running, reachable at its variables. `src: Technical requirements para after stack list`
- [ ] `C-TR-13` `constraint` Mailpit is already running, reachable at its variables. `src: Technical requirements para after stack list`
- [ ] `C-TR-14` `contract` `POST /api/auth/login` signs in with no auth, returning `access_token`. `src: Technical requirements, API surface table row 1`
- [ ] `C-TR-15` `contract` `GET /api/session` returns the current account for a token. `src: Technical requirements, API surface table row 2`
- [ ] `C-TR-16` `contract` `GET /api/health` reports readiness with no auth. `src: Technical requirements, API surface table row 3`
- [ ] `C-TR-17` `contract` `GET /api/productions` returns all seventeen productions in index order with no auth. `src: Technical requirements, API surface table row 4`
- [ ] `C-TR-18` `contract` `GET /api/productions/{slug}` returns one case study with credits, galleries, no auth. `src: Technical requirements, API surface table row 5`
- [ ] `C-TR-19` `contract` `GET /api/home-feed` returns the eleven productions in home order with no auth. `src: Technical requirements, API surface table row 6`
- [ ] `C-TR-20` `contract` `GET /api/availability` returns published slots carrying no confirmed booking, no auth. `src: Technical requirements, API surface table row 7`
- [ ] `C-TR-21` `contract` `POST /api/holds` holds a slot with no auth. `src: Technical requirements, API surface table row 8`
- [ ] `C-TR-22` `contract` `DELETE /api/holds/{id}` releases a hold with no auth. `src: Technical requirements, API surface table row 9`
- [ ] `C-TR-23` `contract` `POST /api/bookings` confirms a held slot with no auth. `src: Technical requirements, API surface table row 10`
- [ ] `C-TR-24` `contract` `GET /api/principal/bookings` returns the signed-in principal's bookings for a `principal`. `src: Technical requirements, API surface table row 11`
- [ ] `C-TR-25` `contract` `POST /api/principal/availability` publishes a slot for a `principal`. `src: Technical requirements, API surface table row 12`
- [ ] `C-TR-26` `contract` `POST /api/principal/availability/{id}/withdraw` withdraws an untaken slot for a `principal`. `src: Technical requirements, API surface table row 13`
- [ ] `C-TR-27` `literal` A booking request carries its idempotency key in an `Idempotency-Key` header. `src: Technical requirements para after API table`
- [ ] `C-TR-28` `literal` The idempotency key runs one to `200` characters. `src: Technical requirements para after API table`
- [ ] `C-TR-29` `literal` A read is reported as `200`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-30` `literal` A creation is reported as `201`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-31` `literal` A malformed body is reported as `400`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-32` `literal` A missing, expired or bad token is reported as `401`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-33` `literal` A caller authenticated but not entitled is reported as `403`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-34` `literal` An unknown address or identifier is reported as `404`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-35` `literal` A slot already held or already booked is reported as `409`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-36` `literal` A withdrawal refused by a confirmed booking is reported as `409`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-37` `literal` A lapsed hold is reported as `410`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-38` `literal` A value outside its declared range is reported as `422`. `src: Technical requirements, outcomes para`
- [ ] `C-TR-39` `literal` The application serves a production build on the container-internal port `4173`. `src: Technical requirements last para`
- [ ] `C-TR-40` `literal` The application binds `0.0.0.0`. `src: Technical requirements last para`
- [ ] `C-TR-41` `constraint` Every dependency installs at image build time. `src: Technical requirements last para`
- [ ] `C-TR-42` `constraint` There is no network at run time. `src: Technical requirements last para`

## C-DM Data model

- [ ] `C-DM-01` `data` The schema holds eight tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-03` `data` Every table carries its own `id`, the child tables included. `src: Data model para 1`
- [ ] `C-DM-04` `data` The table `accounts` carries `id`, `email` unique, `display_name`, `role`, `password_hash`, `timezone`, `created_at`. `src: Data model, accounts para`
- [ ] `C-DM-05` `data` The column `accounts.role` is one of `principal` or `visitor`. `src: Data model, accounts para`
- [ ] `C-DM-06` `data` The table `accounts` holds three seeded rows. `src: Data model, accounts para`
- [ ] `C-DM-07` `data` The table `productions` carries `id`, `slug` unique, `title`, `client_name`, `category`, `duration_seconds`, `year`, `sort_index` unique, `featured_on_home`, `home_sort_index`, `status`, `created_at`. `src: Data model, productions para`
- [ ] `C-DM-08` `data` The column `productions.home_sort_index` is nullable, unique among the rows carrying one. `src: Data model, productions para`
- [ ] `C-DM-09` `data` The column `productions.category` is a closed set of seven values. `src: Data model, productions para`
- [ ] `C-DM-10` `literal` The seven categories are `Campaign`, `Film`, `Documentary`, `Re-Brand`, `Out-of-Home`, `Collaboration`, `Integrated`. `src: Data model, productions para`
- [ ] `C-DM-11` `data` The table `productions` holds seventeen seeded rows. `src: Data model seed table`
- [ ] `C-DM-12` `data` The seed table pins slug, title, client, category, running time, home ordinal for all seventeen productions. `src: Data model seed table`
- [ ] `C-DM-13` `literal` The first production in index order is `tanaka-vertical-mile`. `src: Data model seed table row 1`
- [ ] `C-DM-14` `literal` The last production in index order is `tanaka-steppe-space-shuttle`. `src: Data model seed table row 17`
- [ ] `C-DM-15` `data` The production `norvel-drift` carries no `featured_on_home`. `src: Data model seed table row 8`
- [ ] `C-DM-16` `literal` The second production in home order is `norvel-master-the-route`. `src: Data model seed table row 12`
- [ ] `C-DM-17` `data` Eleven seeded productions carry a home ordinal. `src: Data model seed table Home column`
- [ ] `C-DM-18` `data` Six seeded productions carry a dash in the Home column, carrying neither a home flag nor a home ordinal. `src: Data model seed table Home column`
- [ ] `C-DM-19` `data` Read in home ordinal order the home feed runs `tanaka-vertical-mile`, `norvel-master-the-route`, `pulsebody-quiet-in-the-din`, `pawsure-quit-procrastinating`, `norvel-no-quiet-miles`, `arden-cold-start`, `bout-fight-game`, `kavi-low-priced-groceries`, `fell-rover-ride-harder`, `kopje-gold-marked-by-courage`, `pharos-science-endures`. `src: Data model para after seed table`
- [ ] `C-DM-20` `data` The table `production_galleries` carries `id`, `production_id`, `label`, `title`, `sort_index`. `src: Data model, production_galleries para`
- [ ] `C-DM-21` `data` The table `production_galleries` holds two seeded rows per production. `src: Data model, production_galleries para`
- [ ] `C-DM-22` `literal` The two seeded gallery labels are `[S.01]`, `[S.02]`. `src: Data model, production_galleries para`
- [ ] `C-DM-23` `data` The table `gallery_images` carries `id`, `gallery_id`, `caption`, `sort_index`. `src: Data model, gallery_images para`
- [ ] `C-DM-24` `data` The table `gallery_images` holds three seeded rows per gallery. `src: Data model, gallery_images para`
- [ ] `C-DM-25` `constraint` A `gallery_images` row with no caption cannot be written. `src: Data model, gallery_images para`
- [ ] `C-DM-26` `data` The table `production_credits` carries `id`, `production_id`, `role`, `person_name`, `sort_index`. `src: Data model, production_credits para`
- [ ] `C-DM-27` `data` The table `production_credits` holds four seeded rows per production. `src: Data model, production_credits para`
- [ ] `C-DM-28` `data` The table `availability_slots` carries `id`, `principal_id`, `starts_at`, `ends_at`, `state`, `created_at`. `src: Data model, availability_slots para`
- [ ] `C-DM-29` `data` The column `availability_slots.state` is one of `published` or `withdrawn`. `src: Data model, availability_slots para`
- [ ] `C-DM-30` `data` Every slot runs fifteen minutes. `src: Data model, availability_slots para`
- [ ] `C-DM-31` `data` The table `availability_slots` holds sixteen seeded rows, all published. `src: Data model, availability_slots para`
- [ ] `C-DM-32` `literal` Four seeded slots fall on each of `2026-10-05`, `2026-10-06` for `dara@tallow.agency`. `src: Data model, availability_slots para`
- [ ] `C-DM-33` `literal` Four seeded slots fall on each of `2026-10-07`, `2026-10-08` for `otis@tallow.agency`. `src: Data model, availability_slots para`
- [ ] `C-DM-34` `literal` Seeded slots begin at `14:00`, `14:15`, `14:30`, `14:45` UTC on each seeded day. `src: Data model, availability_slots para`
- [ ] `C-DM-35` `data` The table `slot_holds` carries `id`, `slot_id`, `fingerprint`, `expires_at`, `created_at`. `src: Data model, slot_holds para`
- [ ] `C-DM-36` `data` The table `slot_holds` is not seeded. `src: Data model, slot_holds para`
- [ ] `C-DM-37` `data` The table `bookings` carries `id`, `slot_id` unique, `principal_id`, `attendee_name`, `attendee_email`, `attendee_timezone`, `agenda`, `status`, `idempotency_key` unique, `created_at`. `src: Data model, bookings para`
- [ ] `C-DM-38` `data` The column `bookings.status` is one of `confirmed` or `cancelled`. `src: Data model, bookings para`
- [ ] `C-DM-39` `literal` One seeded booking holds the `2026-10-05` `14:00` slot with Dara Okonjo, confirmed for Marta Iglesias at `marta@example.com`. `src: Data model, bookings para`
- [ ] `C-DM-40` `constraint` A `sort_index` is unique across productions. `src: Data model, invariants list`
- [ ] `C-DM-41` `constraint` A `home_sort_index` is unique among the rows carrying one. `src: Data model, invariants list`
- [ ] `C-DM-42` `constraint` A production carrying `featured_on_home` carries a `home_sort_index`. `src: Data model, invariants list`
- [ ] `C-DM-43` `constraint` A production without `featured_on_home` carries no `home_sort_index`. `src: Data model, invariants list`
- [ ] `C-DM-44` `constraint` A gallery image always carries a caption. `src: Data model, invariants list`
- [ ] `C-DM-45` `constraint` At most one confirmed booking exists for any slot, whatever order two requests arrive in. `src: Data model, invariants list`
- [ ] `C-DM-46` `constraint` A live hold never coexists with a confirmed booking for one slot. `src: Data model, invariants list`
- [ ] `C-DM-47` `constraint` An `idempotency_key` appears at most once across all bookings. `src: Data model, invariants list`
- [ ] `C-DM-48` `constraint` A slot carrying a confirmed booking is never in state `withdrawn`. `src: Data model, invariants list`
- [ ] `C-DM-49` `constraint` The invariants hold in the stored data rather than only in the code that writes the data. `src: Data model, invariants intro`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The product is single tenancy, one agency, two principals, one set of work. `src: Constraints bullet 1`
- [ ] `C-CN-02` `constraint` The product carries no visitor accounts. `src: Constraints bullet 2`
- [ ] `C-CN-03` `constraint` The product carries no public signup. `src: Constraints bullet 2`
- [ ] `C-CN-04` `constraint` The product carries no password reset. `src: Constraints bullet 2`
- [ ] `C-CN-05` `constraint` The product carries no invitation. `src: Constraints bullet 2`
- [ ] `C-CN-06` `constraint` The product carries no account deletion. `src: Constraints bullet 2`
- [ ] `C-CN-07` `constraint` The product carries no cart. `src: Constraints bullet 3`
- [ ] `C-CN-08` `constraint` The product carries no payment. `src: Constraints bullet 3`
- [ ] `C-CN-09` `constraint` The product carries no pricing. `src: Constraints bullet 3`
- [ ] `C-CN-10` `constraint` The product carries no comments. `src: Constraints bullet 4`
- [ ] `C-CN-11` `constraint` The product carries no likes. `src: Constraints bullet 4`
- [ ] `C-CN-12` `constraint` The product carries no reactions. `src: Constraints bullet 4`
- [ ] `C-CN-13` `constraint` The product carries no search. `src: Constraints bullet 4`
- [ ] `C-CN-14` `constraint` The product carries no tag pages. `src: Constraints bullet 4`
- [ ] `C-CN-15` `constraint` The product carries no newsletter. `src: Constraints bullet 4`
- [ ] `C-CN-16` `constraint` The product carries no messaging beyond the one confirmation message. `src: Constraints bullet 4`
- [ ] `C-CN-17` `constraint` The product carries no rescheduling by the visitor. `src: Constraints bullet 5`
- [ ] `C-CN-18` `constraint` The product carries no cancellation by the visitor. `src: Constraints bullet 5`
- [ ] `C-CN-19` `constraint` A confirmed booking is changed only by the agency, never silently. `src: Constraints bullet 5`
- [ ] `C-CN-20` `constraint` The product carries no crew operations. `src: Constraints bullet 6`
- [ ] `C-CN-21` `constraint` The product carries no day rates. `src: Constraints bullet 6`
- [ ] `C-CN-22` `constraint` The product carries availability for the two principals only. `src: Constraints bullet 6`
- [ ] `C-CN-23` `constraint` The product carries no awards detail rows. `src: Constraints bullet 7`
- [ ] `C-CN-24` `constraint` The product carries no client roster page. `src: Constraints bullet 7`
- [ ] `C-CN-25` `constraint` The product carries no transcode pipeline. `src: Constraints bullet 8`
- [ ] `C-CN-26` `constraint` The product carries no signed media addresses. `src: Constraints bullet 8`
- [ ] `C-CN-27` `constraint` The product carries no upload of any kind. `src: Constraints bullet 8`
- [ ] `C-CN-28` `constraint` Every still is seeded. `src: Constraints bullet 8`
- [ ] `C-CN-29` `constraint` Every reel is seeded. `src: Constraints bullet 8`
- [ ] `C-CN-30` `constraint` The product carries no cookie consent surface. `src: Constraints bullet 9`
- [ ] `C-CN-31` `constraint` The product carries no analytics. `src: Constraints bullet 9`
- [ ] `C-CN-32` `constraint` The product carries no audit trail. `src: Constraints bullet 10`
- [ ] `C-CN-33` `constraint` The product carries no outbox. `src: Constraints bullet 10`
- [ ] `C-CN-34` `constraint` The product carries no second theme. `src: Constraints bullet 11`
- [ ] `C-CN-35` `constraint` The product ships one appearance. `src: Constraints bullet 11`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `literal` The value `4173` is the container-internal port. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The variable `APP_PUBLIC_PORT` is what the outside world uses. `src: Deployment contract bullet 1`
- [ ] `C-DC-05` `constraint` Both port values are read from the environment, never hardcoded. `src: Deployment contract bullet 1`
- [ ] `C-DC-06` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-07` `literal` The route `/api/health` returns `200` once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-08` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-09` `literal` Login credentials, or an explicit statement that none exist, are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-10` `literal` A reserved `.browser_screenshots/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-11` `literal` A reserved `.downloads/` directory exists at the app root, empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-12` `contract` The app serves a production build behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-13` `constraint` The app never serves behind a dev server. `src: Deployment contract bullet 7`
- [ ] `C-DC-14` `constraint` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-15` `constraint` The server is not a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-16` `literal` The app binds `0.0.0.0`. `src: Deployment contract bullet 9`
- [ ] `C-DC-17` `constraint` The app never binds `127.0.0.1` or `localhost`. `src: Deployment contract bullet 9`
- [ ] `C-DC-18` `constraint` The backing services named in the brief are never downloaded, installed, compiled or started again. `src: Deployment contract bullet 10`
- [ ] `C-DC-19` `constraint` Only the providers named in the brief are used. `src: Deployment contract bullet 11`
- [ ] `C-DC-20` `constraint` The product carries no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-21` `constraint` The product carries no persistent volumes. `src: Deployment contract bullet 12`
- [ ] `C-DC-22` `constraint` The product carries no fixed container names. `src: Deployment contract bullet 12`
- [ ] `C-DC-23` `constraint` The product carries no custom networks. `src: Deployment contract bullet 12`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `deku-studio-2026` | seeded password for every account | C-RL-29 | User roles, seed table intro |
| `dara@tallow.agency` | first principal address | C-RL-30 | User roles, seed table row 1 |
| `otis@tallow.agency` | second principal address | C-RL-32 | User roles, seed table row 2 |
| `casey@tallow.agency` | seeded visitor address | C-RL-34 | User roles, seed table row 3 |
| `principal` | role value for the two agency accounts | C-RL-31 | User roles, seed table |
| `visitor` | role value for the seeded non-agency account | C-RL-35 | User roles, seed table |
| `published` | availability slot state offered to visitors | C-CF-01 | Core features, Booking a call item 1 |
| `confirmed` | booking status created on confirmation | C-CF-10 | Core features, Booking a call item 4 |
| `600` | hold lifetime in seconds | C-CF-07 | Core features, Booking a call item 3 |
| `2000` | agenda length ceiling in characters | C-CF-25 | Core features, Booking a call item 7 |
| `80` | attendee name length ceiling in characters | C-CF-26 | Core features, Booking a call item 7 |
| `Call confirmed:` | confirmation subject prefix | C-CF-34 | Core features, The confirmation message item 3 |
| `Call confirmed: Dara Okonjo` | worked confirmation subject | C-CF-35 | Core features, The confirmation message item 3 |
| `01` | first index ordinal | C-CF-45 | Core features, The index and its two orderings item 1 |
| `17` | last index ordinal | C-CF-45 | Core features, The index and its two orderings item 1 |
| `featured_on_home` | column marking a production for the home feed | C-CF-46 | Core features, The index and its two orderings item 2 |
| `home_sort_index` | column ordering the home feed | C-CF-47 | Core features, The index and its two orderings item 2 |
| `sort_index` | column ordering the work index | C-CF-44 | Core features, The index and its two orderings item 1 |
| `access_token` | field carrying the bearer token | C-CF-100 | Core features, Auth intro |
| `playful-consumer` | design direction | C-UX-01 | UI/UX notes para 1 |
| `springy` | motion character | C-UX-04 | UI/UX notes para 1 |
| `energetic` | quality scoped to the call-to-action accent | C-UX-24 | UI/UX notes, Ground and the four meanings para 3 |
| `geometric sans` | interface type personality | C-UX-36 | UI/UX notes, Type |
| `Idempotency-Key` | header carrying the booking idempotency key | C-TR-27 | Technical requirements, para after API table |
| `200` | read status, also the idempotency key length ceiling | C-TR-29 | Technical requirements, outcomes para |
| `201` | creation status | C-TR-30 | Technical requirements, outcomes para |
| `400` | malformed body status | C-TR-31 | Technical requirements, outcomes para |
| `401` | missing, expired or bad token status | C-TR-32 | Technical requirements, outcomes para |
| `403` | authenticated but not entitled status | C-TR-33 | Technical requirements, outcomes para |
| `404` | unknown address or identifier status | C-TR-34 | Technical requirements, outcomes para |
| `409` | already held, already booked, or refused withdrawal status | C-TR-35 | Technical requirements, outcomes para |
| `410` | lapsed hold status | C-TR-37 | Technical requirements, outcomes para |
| `422` | out-of-range value status | C-TR-38 | Technical requirements, outcomes para |
| `4173` | container-internal port | C-TR-39 | Technical requirements, last para |
| `0.0.0.0` | bind address | C-TR-40 | Technical requirements, last para |
| `Campaign` | production category value | C-DM-10 | Data model, productions para |
| `Film` | production category value | C-DM-10 | Data model, productions para |
| `Documentary` | production category value | C-DM-10 | Data model, productions para |
| `Re-Brand` | production category value | C-DM-10 | Data model, productions para |
| `Out-of-Home` | production category value | C-DM-10 | Data model, productions para |
| `Collaboration` | production category value | C-DM-10 | Data model, productions para |
| `Integrated` | production category value | C-DM-10 | Data model, productions para |
| `tanaka-vertical-mile` | first slug in index order | C-DM-13 | Data model, seed table row 1 |
| `tanaka-steppe-space-shuttle` | last slug in index order | C-DM-14 | Data model, seed table row 17 |
| `norvel-master-the-route` | second slug in home order | C-DM-16 | Data model, seed table row 12 |
| `norvel-drift` | slug carrying no home ordinal | C-DM-15 | Data model, seed table row 8 |
| `[S.01]` | first seeded gallery label | C-DM-22 | Data model, production_galleries para |
| `[S.02]` | second seeded gallery label | C-DM-22 | Data model, production_galleries para |
| `withdrawn` | availability slot state after withdrawal | C-DM-29 | Data model, availability_slots para |
| `cancelled` | second booking status value | C-DM-38 | Data model, bookings para |
| `2026-10-05` | first seeded availability date | C-DM-32 | Data model, availability_slots para |
| `2026-10-06` | second seeded availability date | C-DM-32 | Data model, availability_slots para |
| `2026-10-07` | third seeded availability date | C-DM-33 | Data model, availability_slots para |
| `2026-10-08` | fourth seeded availability date | C-DM-33 | Data model, availability_slots para |
| `14:00` | first seeded slot start, UTC | C-DM-34 | Data model, availability_slots para |
| `14:15` | second seeded slot start, UTC | C-DM-34 | Data model, availability_slots para |
| `14:30` | third seeded slot start, UTC | C-DM-34 | Data model, availability_slots para |
| `14:45` | fourth seeded slot start, UTC | C-DM-34 | Data model, availability_slots para |
| `marta@example.com` | seeded booking attendee address | C-DM-39 | Data model, bookings para |
| `idempotency_key` | unique booking column | C-DM-47 | Data model, invariants list |
| `${APP_PUBLIC_PORT}:4173` | port mapping | C-DC-02 | Deployment contract bullet 1 |
| `/api` | API prefix on the app origin | C-TR-07 | Technical requirements, stack list |
| `/api/health` | readiness route | C-DC-07 | Deployment contract bullet 3 |
| `/app/USER_README.md` | path carrying the login credentials | C-DC-09 | Deployment contract bullet 5 |
| `.browser_screenshots/` | reserved empty directory at the app root | C-DC-10 | Deployment contract bullet 6 |
| `.downloads/` | reserved empty directory at the app root | C-DC-11 | Deployment contract bullet 6 |
| `127.0.0.1` | bind address the app must never use | C-DC-17 | Deployment contract bullet 9 |
| `localhost` | bind address the app must never use | C-DC-17 | Deployment contract bullet 9 |
| `DATABASE_URL` | variable carrying the PostgreSQL address | C-TR-08 | Technical requirements, stack list |
| `APP_PUBLIC_URL` | variable carrying the app's public address | C-DC-01 | Deployment contract bullet 1 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the base spacing unit | C-UX-49 | every gap derives from a unit the brief leaves to the builder |
| the exact shades of the four meaning colours | C-UX-17 | the four jobs are pinned, the colour values are not |
| the responsive breakpoint widths | C-UX-121 | the layout must hold at every width, the breakpoints are the builder's |
| the agency's own city | C-UX-92 | shown beside the visitor's zone, named nowhere in the brief |
| the display face | C-UX-37 | one characterful face is required, no family is named |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 25 |
| User roles | 2 | 35 |
| Core features | 19 | 116 |
| User flow | 2 | 66 |
| UI and UX notes | 6 | 128 |
| Technical requirements | 2 | 42 |
| Data model | 3 | 49 |
| Constraints | 0 | 35 |
| Deployment contract | 6 | 23 |

The instruction's `## Definition of done` section carries no block of its own. Every bullet
there restates an ask already itemised above, so a block would duplicate ids rather than add
coverage. The obligation-bearing sentence counts are the tool's own recomputation over the
instruction's sections; item counts exceed them in every row because the brief packs several
asks into most sentences, notably in the tables, where one row states a route, a purpose, an
auth rule at once.
