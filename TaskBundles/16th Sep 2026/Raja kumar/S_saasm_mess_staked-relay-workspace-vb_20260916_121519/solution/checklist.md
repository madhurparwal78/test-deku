# Checklist: deku/staked-relay-workspace-vb

Source: instruction.md
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-FE, C-TR, C-DM, C-CN, C-DC
Sections absent: C-BP
Items: 336
Unpinned values flagged: 4

## C-OV Overview

- [ ] `C-OV-01` `capability` A signed-up stranger exchanges a message with another member that opens only on their approved devices `src: Definition of done, exchange messages with another member that only their approved devices can open`
- [ ] `C-OV-02` `constraint` The server never stores readable message text `src: Overview, it can never open anything it stores`
- [ ] `C-OV-03` `constraint` A closed epoch pays each relay exactly once `src: Overview, money arithmetic that is exact, frozen at the epoch boundary and paid exactly once`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor is denied every member-only API `src: User roles, Cannot reach anything under /app or any member-only API`
- [ ] `C-RL-02` `role` A member session is denied every treasurer-only endpoint `src: User roles, a direct API call from a Member session to any Treasurer-only endpoint must be rejected`
- [ ] `C-RL-03` `constraint` A refused treasurer action leaves the epoch state unchanged `src: User roles, leaving the protected state unchanged`
- [ ] `C-RL-04` `role` A non-owner removing a group member is denied `src: User roles, a non-owner removing a group member`
- [ ] `C-RL-05` `role` A member reading the probe of a relay operated by someone else is denied `src: User roles, a member reading another operator's probe`
- [ ] `C-RL-06` `capability` Anyone creates a member account with an email plus a password `src: User roles, Signup is open`
- [ ] `C-RL-07` `literal` The seeded treasurer signs in as `treasurer@example.com` `src: User roles, seeded accounts table`
- [ ] `C-RL-08` `literal` The seeded operator signs in as `member4@example.com` `src: User roles, seeded accounts table`
- [ ] `C-RL-09` `literal` The seeded lapsed member signs in as `member3@example.com` `src: User roles, seeded accounts table`
- [ ] `C-RL-10` `literal` The seeded member signs in as `member@example.com` `src: User roles, seeded accounts table`
- [ ] `C-RL-11` `literal` The second seeded member signs in as `member2@example.com` `src: User roles, seeded accounts table`
- [ ] `C-RL-12` `literal` The second seeded member's contact code is `NJ-MEMBER23` `src: User roles, seeded accounts table`
- [ ] `C-RL-13` `role` The treasurer reads the whitelist applications `src: User roles, Treasurer row`

## C-CF Core features

- [ ] `C-CF-01` `capability` Signup returns an `access_token` for a valid email with a password of at least twelve characters `src: Core features, Accounts rule 2`
- [ ] `C-CF-02` `constraint` Signup with an invalid email creates no account `src: Core features, Accounts rule 2`
- [ ] `C-CF-03` `capability` Signing out stops that token from working `src: Core features, Accounts rule 2`
- [ ] `C-CF-04` `constraint` Signing out one session leaves other sessions of the account working `src: Core features, Accounts rule 2`
- [ ] `C-CF-05` `capability` A wallet challenge returns the exact message to sign with an expiry `src: Core features, Accounts rule 3`
- [ ] `C-CF-06` `constraint` A used wallet challenge issues no second session `src: Core features, Accounts rule 4`
- [ ] `C-CF-07` `constraint` Simultaneous verifications of one wallet challenge issue exactly one session `src: Core features, Accounts rule 4`
- [ ] `C-CF-08` `constraint` A wallet signature from a different key is refused `src: Core features, Accounts rule 4`
- [ ] `C-CF-09` `constraint` An expired wallet challenge is refused `src: Core features, Accounts rule 4`
- [ ] `C-CF-10` `constraint` A whitelist challenge never signs anyone in `src: Core features, Accounts rule 4`
- [ ] `C-CF-11` `capability` Wallet sign-in with an unattached address creates a new account `src: Core features, Accounts rule 5`
- [ ] `C-CF-12` `capability` Wallet sign-in after connecting the wallet reaches the same `account_id` `src: Core features, Accounts rule 6`
- [ ] `C-CF-13` `constraint` Connecting a wallet attached to a different account is refused with neither account changed `src: Core features, Accounts rule 6`
- [ ] `C-CF-14` `constraint` A wallet-created account whose address was attached elsewhere starts with no trial `src: Core features, Accounts rule 7`
- [ ] `C-CF-15` `ui` The first device setup shows the key warning before the workspace opens `src: Core features, Accounts rule 8`
- [ ] `C-CF-16` `ui` The workspace opens only once the key acknowledgement checkbox is ticked before Continue is pressed `src: Core features, Accounts rule 8`
- [ ] `C-CF-17` `capability` The first device of an account is active at once `src: Core features, Devices rule 2`
- [ ] `C-CF-18` `capability` A later device of an account starts pending `src: Core features, Devices rule 2`
- [ ] `C-CF-19` `constraint` A pending device shows each message with the unopenable line `src: Core features, Devices rule 2`
- [ ] `C-CF-20` `role` A pending device asking to approve itself is denied `src: Core features, Devices rule 3`
- [ ] `C-CF-21` `capability` An active device of the same account approves a pending device `src: Core features, Devices rule 3`
- [ ] `C-CF-22` `capability` An approved device opens messages sent after its approval `src: Core features, Devices rule 4`
- [ ] `C-CF-23` `constraint` An approved device still shows messages sent before its approval as unopenable `src: Core features, Devices rule 4`
- [ ] `C-CF-24` `constraint` A removed device token stops working `src: Core features, Devices rule 5`
- [ ] `C-CF-25` `capability` Removing a device advances the key epoch of every conversation of the account `src: Core features, Devices rule 5`
- [ ] `C-CF-26` `constraint` The key directory lists no pending device `src: Core features, Devices rule 6`
- [ ] `C-CF-27` `constraint` The key directory lists no removed device `src: Core features, Devices rule 6`
- [ ] `C-CF-28` `constraint` Typed message text never appears in any request the sending browser makes `src: Core features, Sealed messages rule 1`
- [ ] `C-CF-29` `constraint` Typed message text never appears in the database `src: Core features, Sealed messages rule 1`
- [ ] `C-CF-30` `constraint` A message with altered sealed bytes shows the unopenable line instead of text `src: Core features, Sealed messages rule 6`
- [ ] `C-CF-31` `constraint` The relay refuses an envelope sealed to a device of a removed member `src: Core features, Sealed messages rule 3`
- [ ] `C-CF-32` `constraint` The relay refuses an envelope sealed to a pending device `src: Core features, Sealed messages rule 3`
- [ ] `C-CF-33` `constraint` A refused envelope stores nothing `src: Core features, Sealed messages rule 3`
- [ ] `C-CF-34` `constraint` An envelope with a stale epoch is refused with reason `stale_epoch` carrying `current_epoch` `src: Core features, Sealed messages rule 3`
- [ ] `C-CF-35` `constraint` A repeated `client_id` from one device returns the same `envelope_id` `src: Core features, Sealed messages rule 4`
- [ ] `C-CF-36` `constraint` Simultaneous repeats of one `client_id` store exactly one envelope row `src: Core features, Sealed messages rule 4`
- [ ] `C-CF-37` `capability` History lists envelopes by `clock` regardless of arrival order `src: Core features, Sealed messages rule 5`
- [ ] `C-CF-38` `capability` History marks `gap_before` when the preceding `sender_seq` is missing `src: Core features, Sealed messages rule 5`
- [ ] `C-CF-39` `capability` A late envelope clears the gap flag over the envelope after the filled gap `src: Core features, Sealed messages rule 5`
- [ ] `C-CF-40` `constraint` A receipt is refused unless reader plus author both switched read receipts on `src: Core features, Sealed messages rule 9`
- [ ] `C-CF-41` `capability` A receipt between two opted-in members reaches the author's sync feed `src: Core features, Sealed messages rule 9`
- [ ] `C-CF-42` `capability` Each membership change advances the conversation epoch by one `src: Core features, Conversations rule 2`
- [ ] `C-CF-43` `constraint` A removed member keeps history accepted before the removal `src: Core features, Conversations rule 3`
- [ ] `C-CF-44` `constraint` A removed member sees nothing accepted after the removal `src: Core features, Conversations rule 3`
- [ ] `C-CF-45` `constraint` A re-added member sees nothing accepted during the gap between periods `src: Core features, Conversations rule 3`
- [ ] `C-CF-46` `role` History of a conversation the account never joined is denied `src: Core features, Conversations rule 3`
- [ ] `C-CF-47` `role` Only the group owner removes a member, a refused removal leaving members plus epoch unchanged `src: Core features, Conversations rule 4`
- [ ] `C-CF-48` `ui` Removing a member shows the line saying removed members keep what was already received `src: Core features, Conversations rule 4`
- [ ] `C-CF-49` `capability` A member offline across two changes finds both membership events in order `src: Core features, Conversations rule 6`
- [ ] `C-CF-50` `constraint` A removed member's sync feed carries nothing from after the removal `src: Core features, Conversations rule 6`
- [ ] `C-CF-51` `ui` Joining a public group shows the public-group notice `src: Core features, Conversations rule 7`
- [ ] `C-CF-52` `ui` Posting in a public group shows the public-group notice above the composer `src: Core features, Conversations rule 7`
- [ ] `C-CF-53` `role` A channel subscriber posting is denied `src: Core features, Conversations rule 8`
- [ ] `C-CF-54` `ui` A channel subscriber sees a line saying only broadcasters post `src: Core features, Conversations rule 8`
- [ ] `C-CF-55` `constraint` A join request to a private group is refused `src: Core features, Conversations rule 8`
- [ ] `C-CF-56` `constraint` A join request to a chat is refused `src: Core features, Conversations rule 8`
- [ ] `C-CF-57` `constraint` A closed group refuses every post `src: Core features, Conversations rule 9`
- [ ] `C-CF-58` `capability` A closed group keeps its history readable to its members `src: Core features, Conversations rule 9`
- [ ] `C-CF-59` `capability` Renaming a task gives its conversation the same `sealed_topic` `src: Core features, Planner rule 1`
- [ ] `C-CF-60` `capability` A person added to a shared group later becomes a task reader `src: Core features, Planner rule 2`
- [ ] `C-CF-61` `constraint` A person removed from a shared group can no longer be sealed task messages `src: Core features, Planner rule 2`
- [ ] `C-CF-62` `constraint` Un-sharing one group keeps a reader who is still granted by another group `src: Core features, Planner rule 3`
- [ ] `C-CF-63` `constraint` Un-sharing a group removes a reader granted by that group alone `src: Core features, Planner rule 3`
- [ ] `C-CF-64` `capability` The placement with the higher `clock` decides where a task sits in either arrival order `src: Core features, Planner rule 5`
- [ ] `C-CF-65` `capability` Equal clocks resolve to the placement from the higher `device_id` `src: Core features, Planner rule 5`
- [ ] `C-CF-66` `capability` Equal positions order by `client_id` `src: Core features, Planner rule 5`
- [ ] `C-CF-67` `constraint` A task sent again with its `client_id` creates no second task `src: Core features, Planner rule 6`
- [ ] `C-CF-68` `ui` A card moves between columns through its Move menu using the keyboard `src: Core features, Planner rule 8`
- [ ] `C-CF-69` `constraint` A typed file name never appears in any request the uploading browser makes `src: Core features, Storage rule 1`
- [ ] `C-CF-70` `constraint` Typed file contents never appear in the database `src: Core features, Storage rule 1`
- [ ] `C-CF-71` `constraint` A piece whose length differs from `piece_size` is refused `src: Core features, Storage rule 2`
- [ ] `C-CF-72` `literal` The account quota is `67108864` bytes `src: Core features, Storage rule 3`
- [ ] `C-CF-73` `constraint` Simultaneous file creations never take an account over the quota `src: Core features, Storage rule 3`
- [ ] `C-CF-74` `ui` The storage page shows the used amount against the quota with the refusal notice `src: Core features, Storage rule 3`
- [ ] `C-CF-75` `capability` A file that lost a stored piece reads `unavailable` `src: Core features, Storage rule 4`
- [ ] `C-CF-76` `constraint` A revoked link is refused with `reason` `revoked` `src: Core features, Storage rule 8`
- [ ] `C-CF-77` `constraint` An expired link is refused with reason `expired` carrying the expired-link message `src: Core features, Storage rule 8`
- [ ] `C-CF-78` `constraint` Revoking a link leaves conversation member access to the file intact `src: Core features, Storage rule 9`
- [ ] `C-CF-79` `constraint` Removing a conversation member leaves links to the file working `src: Core features, Storage rule 9`
- [ ] `C-CF-80` `constraint` A removed conversation member loses access to a file shared there `src: Core features, Storage rule 6`
- [ ] `C-CF-81` `literal` Every account starts with `call_route` `private` `src: Core features, Calls rule 2`
- [ ] `C-CF-82` `ui` The call route setting shows the privacy choice with Private selected `src: Core features, Calls rule 2`
- [ ] `C-CF-83` `constraint` A chat call is `relay` unless both participants chose `direct` `src: Core features, Calls rule 3`
- [ ] `C-CF-84` `constraint` A group call is `relay` even when everyone chose `direct` `src: Core features, Calls rule 3`
- [ ] `C-CF-85` `constraint` `peer_address` appears only on a `direct` call `src: Core features, Calls rule 4`
- [ ] `C-CF-86` `constraint` A repeated `ring_id` rings once `src: Core features, Calls rule 5`
- [ ] `C-CF-87` `constraint` A ring after the call ended is refused `src: Core features, Calls rule 5`
- [ ] `C-CF-88` `constraint` A stake below `10000` NJR is refused `src: Core features, Relay network rule 2`
- [ ] `C-CF-89` `data` A stake of 20000 NJR registers at tier `level-1` `src: Core features, Relay network rule 3`
- [ ] `C-CF-90` `constraint` A withdrawal leaving less than `10000` NJR is refused `src: Core features, Relay network rule 4`
- [ ] `C-CF-91` `constraint` A repeated probe answer counts nothing `src: Core features, Relay network rule 5`
- [ ] `C-CF-92` `constraint` A probe answer carrying another relay's nonce counts nothing `src: Core features, Relay network rule 5`
- [ ] `C-CF-93` `constraint` An answer to a superseded probe round counts nothing `src: Core features, Relay network rule 5`
- [ ] `C-CF-94` `constraint` Self-reported heartbeat figures change nothing counted `src: Core features, Relay network rule 6`
- [ ] `C-CF-95` `capability` Conversation `routing` reads `open_network` with `fell_back` once the core node misses the latest round `src: Core features, Relay network rule 8`
- [ ] `C-CF-96` `ui` Starting relay mode first shows the operator notice with Start plus Cancel `src: Core features, Relay network rule 9`
- [ ] `C-CF-97` `ui` The network limits page states that no stake is slashed `src: Core features, Relay network rule 7`
- [ ] `C-CF-98` `ui` The network limits page states the network does not resist a whole-network observer `src: Core features, Relay network rule 10`
- [ ] `C-CF-99` `literal` A month on the `njr` rail costs `225` cents `src: Core features, Membership rule 1`
- [ ] `C-CF-100` `literal` A month on the `usdc` rail costs `350` cents `src: Core features, Membership rule 1`
- [ ] `C-CF-101` `constraint` A quote is refused with `rate_stale` when the latest rate is over ten minutes old `src: Core features, Membership rule 2`
- [ ] `C-CF-102` `capability` `amount_due` rounds up to a whole base unit of the rail `src: Core features, Membership rule 3`
- [ ] `C-CF-103` `literal` An `xmr` quote at rate `157300000` asks `22250476796` `src: Core features, Membership rule 3 table`
- [ ] `C-CF-104` `constraint` A watcher event without a valid signature changes nothing `src: Core features, Membership rule 5`
- [ ] `C-CF-105` `constraint` A payment below its confirmation depth reads `seen` with nothing granted `src: Core features, Membership rule 6`
- [ ] `C-CF-106` `capability` A payment with a block time before expiry settles at the quote's own amount however late the report arrives `src: Core features, Membership rule 7`
- [ ] `C-CF-107` `capability` A payment with a block time after expiry is re-quoted at the rate in force at that block time `src: Core features, Membership rule 7`
- [ ] `C-CF-108` `constraint` Simultaneous reports of one payment reaching depth extend membership once `src: Core features, Membership rule 7`
- [ ] `C-CF-109` `capability` A second transaction on a settled quote becomes `credited` without extending membership `src: Core features, Membership rule 7`
- [ ] `C-CF-110` `capability` A shortfall of at most half a per cent settles `src: Core features, Membership rule 7 table`
- [ ] `C-CF-111` `capability` A larger shortfall reads `underpaid` with its `shortfall` `src: Core features, Membership rule 7 table`
- [ ] `C-CF-112` `capability` A settled payment extends `paid_until` by thirty days `src: Core features, Membership rule 7`
- [ ] `C-CF-113` `capability` Membership `state` reads `suspended` once paid time plus trial have both ended `src: Core features, Membership rule 9`
- [ ] `C-CF-114` `constraint` A suspended account still reads its history `src: Core features, Membership rule 10`
- [ ] `C-CF-115` `constraint` A suspended account sending an envelope is refused with `membership_suspended` `src: Core features, Membership rule 10`
- [ ] `C-CF-116` `constraint` A suspended account keeps its devices `src: Core features, Membership rule 10`
- [ ] `C-CF-117` `capability` Paying again restores sending at once `src: Core features, Membership rule 10`
- [ ] `C-CF-118` `ui` A suspended account sees the membership expired notice `src: Core features, Membership rule 10`
- [ ] `C-CF-119` `capability` A sponsored payment extends the beneficiary's membership `src: Core features, Membership rule 7`
- [ ] `C-CF-120` `constraint` The sponsor list carries only the recipient code plus the sponsorship state `src: Core features, Membership rule 12`
- [ ] `C-CF-121` `capability` Declining a sponsorship ends the sponsored time at once `src: Core features, Membership rule 12`
- [ ] `C-CF-122` `capability` A payment settling after an epoch closed belongs to the next epoch `src: Core features, Epochs rule 2`
- [ ] `C-CF-123` `capability` A dollar-rail receipt contributes its price divided by the NJR rate at settlement `src: Core features, Epochs rule 3`
- [ ] `C-CF-124` `capability` A relay earns per answered round at the tier held when that round was issued `src: Core features, Epochs rule 4`
- [ ] `C-CF-125` `capability` Each relay share rounds down to a millionth of an NJR `src: Core features, Epochs rule 5`
- [ ] `C-CF-126` `capability` The rounding remainder stays with the treasury as `remainder_micro` `src: Core features, Epochs rule 5`
- [ ] `C-CF-127` `constraint` A stake withdrawn after the close leaves that epoch's shares unchanged `src: Core features, Epochs rule 6`
- [ ] `C-CF-128` `constraint` Settling an epoch twice pays no relay a second time `src: Core features, Epochs rule 7`
- [ ] `C-CF-129` `constraint` Simultaneous settlement runs pay each relay exactly one transfer `src: Core features, Epochs rule 7`
- [ ] `C-CF-130` `capability` A settlement run with `limit` pays at most that many relays in ascending name order `src: Core features, Epochs rule 7`
- [ ] `C-CF-131` `capability` The epoch audit shows answered rounds by tier for every relay `src: Core features, Epochs rule 8`
- [ ] `C-CF-132` `literal` Seeded epoch 1 leaves `remainder_micro` `1`, shown as `0.000001 NJR` `src: Core features, Epochs rule 9`
- [ ] `C-CF-133` `ui` The token-sale terms stay hidden until the eligibility statement is ticked `src: Core features, Token-sale surface rule 2`
- [ ] `C-CF-134` `data` The token event schedules number eleven rows `src: Core features, Token-sale surface rule 3`
- [ ] `C-CF-135` `ui` The whitepaper page shows an event supply of `16400000` NJR `src: Core features, Token-sale surface rule 4`
- [ ] `C-CF-136` `capability` Nothing of the linear part is claimable before the cliff ends `src: Core features, Token-sale surface rule 6`
- [ ] `C-CF-137` `capability` The accrued linear part becomes claimable at once when the cliff ends `src: Core features, Token-sale surface rule 6`
- [ ] `C-CF-138` `capability` Moving the token event changes the claimable balance at once `src: Core features, Token-sale surface rule 7`
- [ ] `C-CF-139` `constraint` Simultaneous claims on one position transfer the claimable balance once `src: Core features, Token-sale surface rule 8`
- [ ] `C-CF-140` `capability` Claims across any sequence of corrections total the allocation once fully vested `src: Core features, Token-sale surface rule 8`
- [ ] `C-CF-141` `capability` `Back` from the whitelist review step returns to the details step with entries kept `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-142` `constraint` An intended amount outside `500000` to `5000000` cents is refused `src: Core features, Token-sale surface rule 11`
- [ ] `C-CF-143` `constraint` Simultaneous applications from one wallet address file exactly one application `src: Core features, Token-sale surface rule 11`
- [ ] `C-CF-144` `capability` An accepted application sends one email to the applicant address only `src: Core features, Token-sale surface rule 12`
- [ ] `C-CF-145` `capability` The first Tab press focuses Skip the intro `src: Core features, Public page rule 3`
- [ ] `C-CF-146` `capability` A visit to a section address shows no introduction `src: Core features, Public page rule 5`
- [ ] `C-CF-147` `capability` A returning visitor sees no introduction after a reload `src: Core features, Public page rule 6`
- [ ] `C-CF-148` `constraint` With scripts unavailable the page shows every section `src: Core features, Public page rule 8`
- [ ] `C-CF-149` `capability` With scripts unavailable the page scrolls `src: Core features, Public page rule 4`
- [ ] `C-CF-150` `capability` Under reduced motion the six stages show together as stills `src: Core features, Public page rule 7`
- [ ] `C-CF-151` `constraint` Under reduced motion the repeating banner stays still `src: Core features, Public page rule 7`
- [ ] `C-CF-152` `constraint` Assistive technology reads the banner phrase once `src: Core features, Public page rule 9`
- [ ] `C-CF-153` `capability` Choosing a navigation anchor adds a history entry the back button reverses `src: Core features, Public page rule 1`
- [ ] `C-CF-154` `ui` An expanded question shows its answer `src: Core features, Public page rule 10`
- [ ] `C-CF-155` `ui` The waitlist form states its purpose inside the form `src: Core features, Public page rule 12`
- [ ] `C-CF-156` `constraint` A waitlist request with an extra field is refused with nothing sent `src: Core features, Public page rule 13`
- [ ] `C-CF-157` `constraint` A waitlist request without consent is refused with nothing sent `src: Core features, Public page rule 13`
- [ ] `C-CF-158` `constraint` A waitlist request with the decoy field filled is refused with nothing sent `src: Core features, Public page rule 13`
- [ ] `C-CF-159` `capability` A waitlist confirmation email reaches the requester with no cc or bcc `src: Core features, Public page rule 14`
- [ ] `C-CF-160` `literal` The waitlist email subject begins `Confirm your Nightjar waitlist place` `src: Core features, Public page rule 14`
- [ ] `C-CF-161` `constraint` Simultaneous waitlist requests for one address send one confirmation email `src: Core features, Public page rule 14`
- [ ] `C-CF-162` `capability` A confirmation link opened twice shows the already-used line `src: Core features, Public page rule 15`
- [ ] `C-CF-163` `constraint` An invalid signup email shows an inline message naming the Email field `src: Core features, Public page rule 16`
- [ ] `C-CF-164` `constraint` Every public content image carries alternative text `src: Core features, Public page rule 17`
- [ ] `C-CF-165` `ui` An unknown address shows Page not found with a Back to Nightjar link `src: Core features, Public page rule 18`
- [ ] `C-CF-166` `contract` An unknown address answers with a not-found status `src: Core features, Public page rule 18`
- [ ] `C-CF-167` `contract` The sitemap lists the absolute address of every public route but no route under `/app` `src: Core features, Public page rule 19`
- [ ] `C-CF-168` `contract` The robots file names the sitemap's absolute address on a `Sitemap:` line `src: Core features, Public page rule 19`
- [ ] `C-CF-169` `ui` The roadmap marks the whitepaper entry Delivered `src: Core features, Public page rule 11`
- [ ] `C-CF-170` `ui` The storage page states that padding costs bandwidth but hides size `src: Core features, Storage rule 2`
- [ ] `C-CF-171` `ui` A trial account's membership page shows the free trial days left `src: Core features, Membership rule 11`
- [ ] `C-CF-172` `ui` The whitelist stepper states in the form why the email with the amount are collected `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-173` `ui` The epoch audit page lets an operator follow how each relay share was reached `src: Core features, Epochs rule 8`
- [ ] `C-CF-174` `ui` The membership page explains the per-account plus per-wallet trial limit in plain words `src: Core features, Accounts rule 7`
- [ ] `C-CF-175` `capability` A wallet challenge message closes with the no-funds sentence `src: Core features, Accounts rule 3`
- [ ] `C-CF-176` `role` Another account's device approving a pending device is denied `src: Core features, Devices rule 3`
- [ ] `C-CF-177` `capability` History orders equal clocks by `sender_device_id` then by `client_id` `src: Core features, Sealed messages rule 5`
- [ ] `C-CF-178` `capability` A task conversation epoch advances when its reader set changes `src: Core features, Planner rule 2`
- [ ] `C-CF-179` `capability` Conversation `routing` reads `core_node` again once the core relay answers the latest round `src: Core features, Relay network rule 8`
- [ ] `C-CF-180` `capability` A first visit to the public page shows the region labelled `Introduction` `src: Core features, Public page rule 2`
- [ ] `C-CF-181` `capability` Pressing Enter on Skip the intro ends the introduction with scrolling restored `src: Core features, Public page rule 3`
- [ ] `C-CF-182` `capability` A visit to a section address lands at that section `src: Core features, Public page rule 5`
- [ ] `C-CF-183` `constraint` Every decorative drawing on the public pages declares itself decorative `src: Core features, Public page rule 17`
- [ ] `C-CF-184` `capability` The thirty days run from the later of the current `paid_until` or the payment `block_time` `src: Core features, Membership rule 7`
- [ ] `C-CF-185` `capability` A stake withdrawal lowers the relay tier at once `src: Core features, Relay network rule 4`
- [ ] `C-CF-186` `capability` Added stake raises the relay tier at once `src: Core features, Relay network rule 4`
- [ ] `C-CF-187` `capability` A claim with nothing newly vested transfers nothing `src: Core features, Token-sale surface rule 8`
- [ ] `C-CF-188` `data` The `team` schedule releases nothing before its twelve month cliff ends `src: Core features, Token-sale surface rule 3`
- [ ] `C-CF-189` `data` The `liquidity` schedule releases the whole allocation at the token event `src: Core features, Token-sale surface rule 3`
- [ ] `C-CF-190` `data` The `community` schedule releases a lump when its one month cliff ends `src: Core features, Token-sale surface rule 3`
- [ ] `C-CF-191` `literal` An accepted waitlist request answers `Check your inbox to confirm.` `src: Core features, Public page rule 14`
- [ ] `C-CF-192` `capability` The waitlist email body begins with the `/waitlist/confirm?token=` link `src: Core features, Public page rule 14`
- [ ] `C-CF-193` `capability` The waitlist email body carries a `/waitlist/remove?token=` link `src: Core features, Public page rule 14`
- [ ] `C-CF-194` `literal` Opening a confirmation link shows `You are on the Nightjar waitlist.` `src: Core features, Public page rule 15`
- [ ] `C-CF-195` `literal` Opening a removal link shows `Removed. Nightjar no longer holds your address.` `src: Core features, Public page rule 15`
- [ ] `C-CF-196` `constraint` A waitlist request with an invalid email is refused with nothing sent `src: Core features, Public page rule 13`
- [ ] `C-CF-197` `constraint` A later waitlist request for one address inside 24 hours sends no second email `src: Core features, Public page rule 14`
- [ ] `C-CF-198` `contract` The robots file disallows `/app` `src: Core features, Public page rule 19`
- [ ] `C-CF-199` `literal` The whitelist acknowledgement subject begins `Nightjar whitelist application received` `src: Core features, Token-sale surface rule 12`
- [ ] `C-CF-200` `capability` The whitelist acknowledgement body begins with the not-an-allocation line `src: Core features, Token-sale surface rule 12`
- [ ] `C-CF-201` `constraint` A later second application from one wallet address is refused `src: Core features, Token-sale surface rule 11`
- [ ] `C-CF-202` `capability` The whitelist stepper moves through `/whitelist/details` then `/whitelist/review` `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-203` `capability` The whitelist wallet step offers `Wallet address`, `Get message to sign`, `Message to sign`, `Signature`, `Continue` `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-204` `capability` The whitelist details step offers `Email`, `Amount in USD`, `Continue` `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-205` `capability` The whitelist review step submits with `Apply` `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-206` `literal` A pending device shows `Waiting for approval from one of your other devices.` `src: Core features, Devices rule 2`
- [ ] `C-CF-207` `capability` Devices are named `Device 1` then `Device 2` in enrolment order `src: Core features, Devices rule 1`
- [ ] `C-CF-208` `capability` Each approve button reads `Approve` followed by the device name `src: Core features, Devices rule 3`
- [ ] `C-CF-209` `capability` A conversation page composer is a field labelled `Message` with a `Send` button `src: Core features, Sealed messages rule 6`
- [ ] `C-CF-210` `literal` The `njr` rail settles at `12` confirmations `src: Core features, Membership rule 1 table`
- [ ] `C-CF-211` `literal` The `xmr` rail settles at `10` confirmations `src: Core features, Membership rule 1 table`
- [ ] `C-CF-212` `literal` A `piece_size` other than `65536`, `1048576`, `4194304` is refused `src: Core features, Storage rule 2`
- [ ] `C-CF-213` `literal` The public page carries the sections `aboutSection`, `featuresSection`, `ecosystemSection`, `tokenSaleSection`, `roadmapSection`, `faqSection`, `subscribeSection` `src: Core features, Public page rule 1`
- [ ] `C-CF-214` `capability` An epoch pool is eighty per cent of its contributions rounded down `src: Core features, Epochs rule 3`
- [ ] `C-CF-215` `capability` A settled `njr` receipt contributes the smaller of `amount` or `amount_due` `src: Core features, Epochs rule 3`
- [ ] `C-CF-216` `literal` An epoch reads `settling` after a partial settlement run `src: Core features, Epochs rule 1`
- [ ] `C-CF-217` `literal` An epoch reads `settled` once the last share is paid `src: Core features, Epochs rule 1`
- [ ] `C-CF-218` `capability` Closing the open epoch opens the next epoch `src: Core features, Epochs rule 6`
- [ ] `C-CF-219` `capability` An underpaid quote settles once a later payment clears the half per cent rule `src: Core features, Membership rule 7`
- [ ] `C-CF-220` `capability` An amount over `amount_due` is held as `credit` `src: Core features, Membership rule 7`
- [ ] `C-CF-221` `literal` An `app_store` quote asks `350` cents with no rate `src: Core features, Membership rule 2`
- [ ] `C-CF-222` `capability` A sponsored payment after a decline is credited back to the sponsor `src: Core features, Membership rule 12`
- [ ] `C-CF-223` `literal` A new account's membership reads `trial` `src: Core features, Membership rule 9`
- [ ] `C-CF-224` `constraint` A suspended account creating a file is refused `src: Core features, Membership rule 10`
- [ ] `C-CF-225` `capability` The storage page lists each file by the name opened on the uploading device `src: Core features, Storage rule 1`
- [ ] `C-CF-226` `capability` The storage page uploads through `Choose file` with `Upload` `src: Core features, Storage rule 1`
- [ ] `C-CF-227` `ui` The roadmap marks the Q2 2026 token sale entry Missed `src: Core features, Public page rule 11`
- [ ] `C-CF-228` `ui` The whitelist stepper states that only the treasurer reads the details `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-229` `ui` The whitelist stepper states that the details are deleted a year after the sale closes `src: Core features, Token-sale surface rule 10`
- [ ] `C-CF-230` `ui` The waitlist consent checkbox starts unticked `src: Core features, Public page rule 12`
- [ ] `C-CF-231` `ui` Each question answer states a claim the workspace honours `src: Core features, Public page rule 10`
- [ ] `C-CF-232` `capability` The board wizard offers `Board name`, `Next`, `Create board` with the default columns `To do`, `Doing`, `Done` `src: Core features, Planner rule 1`
- [ ] `C-CF-233` `literal` Deleting a file shows `Removed from your storage. Pieces already distributed can't be recalled.` `src: Core features, Storage rule 5`
- [ ] `C-CF-234` `role` A bare account `access_token` approving a pending device is refused `src: Core features, Devices rule 3`
- [ ] `C-CF-235` `capability` `DELETE /api/me/wallets/{address}` detaches the wallet so a later wallet sign-in creates a new account `src: Core features, Accounts rule 6`
- [ ] `C-CF-236` `capability` Under reduced motion nothing holds scrolling `src: Core features, Public page rule 7`
- [ ] `C-CF-237` `capability` The sync feed delivers each envelope sealed to the calling device `src: Core features, Conversations rule 6`
- [ ] `C-CF-238` `literal` Seeded epoch 1 weighs Kestrel `150`, Heron `40`, Osprey `105`, Plover `0` with shares `47457626`, `12655367`, `33220338`, `0` `src: Core features, Epochs rule 9`
- [ ] `C-CF-239` `literal` The floating navigation reads `About`, `Features`, `Ecosystem`, `Token Sale`, `Subscribe` `src: Core features, Public page rule 1`
- [ ] `C-CF-240` `capability` A file reserves `piece_size` times `piece_count` bytes at creation, reported in `used_bytes` `src: Core features, Storage rule 3`

## C-UF User flow

- [ ] `C-UF-01` `ui` The new conversation wizard steps through `/app/conversations/new`, `/app/conversations/new/people` then `/app/conversations/new/name` `src: User flow, route table`
- [ ] `C-UF-02` `ui` The new board wizard creates a board with its named columns `src: User flow, Journeys item 6`
- [ ] `C-UF-03` `ui` A task chat carries the renamed task title `src: User flow, Journeys item 6`
- [ ] `C-UF-04` `ui` The devices page lists each device with state, added time plus last active time `src: User flow, route table`
- [ ] `C-UF-05` `ui` The call route choice stays on Direct after a reload `src: User flow, Journeys item 8`
- [ ] `C-UF-06` `ui` The epochs page lists epoch 1 as closed with the last epoch open `src: Data model, Seed data`
- [ ] `C-UF-07` `capability` The whitelist application page shows the not-an-allocation line after Apply `src: User flow, Journeys item 14`
- [ ] `C-UF-08` `ui` The empty conversation queue reads `No conversations yet.` `src: User flow, States`
- [ ] `C-UF-09` `ui` The new board wizard steps through `/app/boards/new` then `/app/boards/new/columns` `src: User flow, route table`
- [ ] `C-UF-10` `ui` The relay page lists each relay the member operates with its tier `src: User flow, route table`
- [ ] `C-UF-11` `role` A member opening `/app/treasury/whitelist` sees the treasurer-only notice without application data `src: User flow, Entry and redirects`
- [ ] `C-UF-12` `ui` Loading states take the shape of the awaited content `src: User flow, States`
- [ ] `C-UF-13` `ui` Each action outcome arrives as a toast stating the reason for any failure `src: User flow, States`
- [ ] `C-UF-14` `capability` The sign-in page offers `Email`, `Password`, `Sign in` `src: User flow, Entry and redirects`
- [ ] `C-UF-15` `capability` The sign-up page offers a `Create account` button `src: User flow, Entry and redirects`
- [ ] `C-UF-16` `capability` An NJR amount displays in whole units with trailing zeros dropped before the code `NJR` `src: User flow, Display formats`
- [ ] `C-UF-17` `capability` On a phone each board column is at least 60 per cent of the viewport wide `src: User flow, Entry and redirects`
- [ ] `C-UF-18` `capability` On a phone every workspace page offers a `Menu` button opening the sidebar links `src: User flow, Entry and redirects`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` One light vivid lime marks the primary action on each page with every other control quieter `src: UI/UX notes, Palette by role`
- [ ] `C-UX-02` `ui` A light vivid red marks failure only `src: UI/UX notes, Palette by role`
- [ ] `C-UX-03` `ui` The display face is condensed, heavy, all-capitals `src: UI/UX notes, Type`
- [ ] `C-UX-04` `ui` Focus is drawn visibly in the lime on the near-black ground `src: UI/UX notes, Components`
- [ ] `C-UX-05` `ui` Motion enters decelerating, exits accelerating, with one symmetrical curve for swaps `src: UI/UX notes, Motion`
- [ ] `C-UX-06` `ui` The workspace reads quiet plus operational without the brochure's oversized type `src: UI/UX notes, register`
- [ ] `C-UX-07` `capability` On a phone the board columns sit in one row that pages sideways `src: UI/UX notes, Responsive`
- [ ] `C-UX-08` `ui` Destructive actions confirm first `src: UI/UX notes, Components`
- [ ] `C-UX-09` `capability` On a phone the workspace sidebar gives way to a menu `src: UI/UX notes, Responsive`
- [ ] `C-UX-10` `ui` Figures align in columns where amounts stack on money pages `src: UI/UX notes, Type`
- [ ] `C-UX-11` `ui` No state relies on colour alone, with success pairing the lime to a check mark plus a word `src: UI/UX notes, Palette by role`
- [ ] `C-UX-12` `ui` Each unavailable control states why `src: UI/UX notes, Components`
- [ ] `C-UX-13` `ui` Attention states wear the light neutral text with a hollow ring mark plus a word, never the alert red `src: UI/UX notes, Palette by role`
- [ ] `C-UX-14` `ui` The public page is spacious plus cinematic `src: UI/UX notes, Shape and density`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` The public page first load fetches only woff2 fonts `src: Front-end specification, The faces are woff, not woff2`
- [ ] `C-FE-02` `constraint` The public page first load fetches no PNG image `src: Front-end specification, Performance`
- [ ] `C-FE-03` `ui` The introduction is illustrated with captions rather than footage `src: Front-end specification, Zero-asset substitution`
- [ ] `C-FE-04` `ui` Toasts use the product palette rather than a library default theme `src: Front-end specification, Forty-one properties that belong to somebody else`
- [ ] `C-FE-05` `ui` The hexagon mark appears in the hero headline `src: Front-end specification, The hexagon`
- [ ] `C-FE-06` `capability` The fixed navigation bar keeps an opaque backing with each label at a contrast of at least `4.5` to 1 against that backing `src: Front-end specification, Chrome`
- [ ] `C-FE-07` `ui` The copy reads Know more from our Whitepaper `src: Front-end specification, Copy deck`
- [ ] `C-FE-08` `ui` Angled section edges never cut into text on a narrow screen `src: Front-end specification, What moves under scroll`
- [ ] `C-FE-09` `capability` On a phone the introduction keeps `Skip the intro` on screen with the six stage labels in one row that never widens the page `src: Front-end specification, The intro on a small screen`
- [ ] `C-FE-10` `ui` Workspace limit notices use the new copy strings word for word `src: Front-end specification, New copy the workspace needs`
- [ ] `C-FE-11` `ui` The hexagon mark separates repeats of the banner phrase `src: Front-end specification, The hexagon`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` Everything the public page fetches before load totals at most `250000` bytes `src: Technical requirements, Public page byte budgets`
- [ ] `C-TR-02` `contract` Scripts fetched before load total at most `150000` bytes `src: Technical requirements, Public page byte budgets`
- [ ] `C-TR-03` `contract` Fonts fetched before load total at most `120000` bytes `src: Technical requirements, Public page byte budgets`
- [ ] `C-TR-04` `constraint` The public page first load fetches no video or audio file `src: Technical requirements, Public page byte budgets`
- [ ] `C-TR-05` `contract` Watcher events are accepted only when signed by the public key `efe6e71259fd773f94f0a96ae30a706f1a74dc8a5fd275b71942f37b5f75ab1f` `src: Technical requirements, The chain watcher`
- [ ] `C-TR-06` `contract` A device token authenticates the account endpoints `src: Technical requirements, Auth`
- [ ] `C-TR-07` `contract` Wallet signatures cover the UTF-8 bytes of the stored challenge message `src: Technical requirements, Sealing`
- [ ] `C-TR-08` `constraint` A losing simultaneous request writes no second row `src: Technical requirements, Invariants under simultaneous requests`
- [ ] `C-TR-09` `contract` Watcher events carry the signature in the `X-Watcher-Signature` header `src: Technical requirements, The chain watcher`

## C-DM Data model

- [ ] `C-DM-01` `data` Every seeded account signs in with `deku-demo-pw-2026` `src: Data model, password paragraph`
- [ ] `C-DM-02` `data` `envelopes`.`ciphertext` holds the posted base64 unchanged `src: Data model, Conversations and messages`
- [ ] `C-DM-03` `data` `memberships` carries `paid_until` plus `trial_ends_at` per `account_id` `src: Data model, Membership and payment`
- [ ] `C-DM-04` `data` `wallet_challenges`.`expires_at` bounds the challenge `src: Data model, Accounts and devices`
- [ ] `C-DM-05` `data` `file_pieces` holds one row per stored piece index `src: Data model, Storage`
- [ ] `C-DM-06` `data` `file_links`.`expires_at` bounds the link `src: Data model, Storage`
- [ ] `C-DM-07` `data` The eight seeded relays are stored once each `src: Data model, Seed data`
- [ ] `C-DM-08` `data` Seeded epochs 1 to 4 carry the stated rounds by relay `src: Data model, Seed data table`
- [ ] `C-DM-09` `data` Seeded epochs 1 to 4 carry the stated receipts `src: Data model, Seed data table`
- [ ] `C-DM-10` `data` The member position seeds `40000000000` millionths on the `visioners` schedule `src: Data model, Seed data`
- [ ] `C-DM-11` `data` Restarting seeding duplicates no row `src: Data model, Seeding must be idempotent`
- [ ] `C-DM-12` `data` The seeded public group `Open Relay Commons` accepts joins `src: Data model, Seed data`
- [ ] `C-DM-13` `data` The seeded channel `Relay Bulletins` is listed on explore with subscriber posts refused `src: Data model, Seed data`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No application-store badge appears on the public page `src: Constraints, No native mobile or desktop application`
- [ ] `C-CN-02` `constraint` The public page fetches nothing from another origin `src: Constraints, No third-party analytics, fonts, scripts or trackers`
- [ ] `C-CN-03` `constraint` The public page compares Nightjar to no named messenger or blockchain `src: Constraints, no comparison to any named messenger or blockchain`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app answers at `APP_PUBLIC_URL` `src: Deployment contract, The app must be reachable`
- [ ] `C-DC-02` `contract` The API answers under the `/api` prefix on the same origin `src: Deployment contract, served on that same origin`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` `src: Deployment contract, GET /api/health`
- [ ] `C-DC-04` `contract` Signup returns `access_token` `src: Deployment contract, API shapes table`
- [ ] `C-DC-05` `contract` A refusal body carries `reason` `src: Deployment contract, API shapes`
- [ ] `C-DC-06` `contract` Envelope creation returns `envelope_id` with `accepted_at` `src: Deployment contract, API shapes table`
- [ ] `C-DC-07` `contract` The sync feed returns `items` with `next_cursor` plus `has_more` `src: Deployment contract, API shapes table`
- [ ] `C-DC-08` `contract` The epoch audit returns `pool_micro` with `remainder_micro` `src: Deployment contract, API shapes table`
- [ ] `C-DC-09` `contract` The settlement run returns `paid` with `remaining` `src: Deployment contract, API shapes table`
- [ ] `C-DC-10` `contract` A quote returns `amount_due` with `deposit_reference` `src: Deployment contract, API shapes table`
- [ ] `C-DC-11` `contract` API field names match the API shapes table `src: Deployment contract, Field names are exact`
- [ ] `C-DC-12` `contract` A refused call answers a 4xx client error rather than a 5xx `src: Deployment contract, rejected as a client error`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `treasurer@example.com` | the seeded treasurer | `C-RL-07` |
| `member4@example.com` | the seeded operator | `C-RL-08` |
| `member3@example.com` | the seeded lapsed member | `C-RL-09` |
| `access_token` | the session token key | `C-CF-01` |
| `account_id` | the account identifier key | `C-CF-12` |
| `current_epoch` | the stale epoch refusal key | `C-CF-34` |
| `client_id` | the browser-made idempotency key | `C-CF-35` |
| `envelope_id` | the envelope identifier key | `C-CF-35` |
| `clock` | the sender logical clock | `C-CF-37` |
| `gap_before` | the history gap flag | `C-CF-38` |
| `sender_seq` | the per-device sequence | `C-CF-38` |
| `sealed_topic` | the sealed conversation name | `C-CF-59` |
| `device_id` | the device identifier key | `C-CF-65` |
| `piece_size` | the file piece size class | `C-CF-71` |
| `67108864` | the account quota in bytes | `C-CF-72` |
| `reason` | the refusal body key | `C-CF-76` |
| `revoked` | the revoked link reason | `C-CF-76` |
| `call_route` | the call route setting | `C-CF-81` |
| `private` | the default call route | `C-CF-81` |
| `relay` | the relayed call route | `C-CF-83` |
| `direct` | the direct call route | `C-CF-83` |
| `peer_address` | the direct call address field | `C-CF-85` |
| `ring_id` | the ring idempotency key | `C-CF-86` |
| `10000` | the stake floor | `C-CF-88` |
| `level-1` | the second tier | `C-CF-89` |
| `routing` | the conversation routing object | `C-CF-95` |
| `open_network` | the fallback routing mode | `C-CF-95` |
| `fell_back` | the fallback flag | `C-CF-95` |
| `njr` | the token rail | `C-CF-99` |
| `225` | the token rail price in cents | `C-CF-99` |
| `usdc` | a dollar stablecoin rail | `C-CF-100` |
| `350` | the other rails price in cents | `C-CF-100` |
| `rate_stale` | the stale rate reason | `C-CF-101` |
| `amount_due` | the quoted amount key | `C-CF-102` |
| `xmr` | the privacy coin rail | `C-CF-103` |
| `157300000` | the worked privacy coin rate | `C-CF-103` |
| `22250476796` | the worked privacy coin amount due | `C-CF-103` |
| `underpaid` | the short payment state | `C-CF-111` |
| `shortfall` | the short payment amount key | `C-CF-111` |
| `paid_until` | the paid membership end | `C-CF-112` |
| `state` | the membership state key | `C-CF-113` |
| `suspended` | the lapsed membership state | `C-CF-113` |
| `membership_suspended` | the suspended send reason | `C-CF-115` |
| `remainder_micro` | the epoch remainder key | `C-CF-126` |
| `limit` | the settlement batch size | `C-CF-130` |
| `1` | the seeded epoch 1 remainder | `C-CF-132` |
| `0.000001 NJR` | the seeded epoch 1 remainder as displayed | `C-CF-132` |
| `seen` | the below-depth payment state | `C-CF-105` |
| `47457626` | the seeded epoch 1 Kestrel share | `C-CF-238` |
| `12655367` | the seeded epoch 1 Heron share | `C-CF-238` |
| `33220338` | the seeded epoch 1 Osprey share | `C-CF-238` |
| `150` | the seeded epoch 1 Kestrel weight | `C-CF-238` |
| `105` | the seeded epoch 1 Osprey weight | `C-CF-238` |
| `40` | the seeded epoch 1 Heron weight | `C-CF-238` |
| `0` | the seeded epoch 1 Plover weight plus share | `C-CF-238` |
| `About` | the first navigation label | `C-CF-239` |
| `Features` | the second navigation label | `C-CF-239` |
| `Ecosystem` | the third navigation label | `C-CF-239` |
| `Token Sale` | the fourth navigation label | `C-CF-239` |
| `Subscribe` | the fifth navigation label | `C-CF-239` |
| `4.5` | the text contrast ratio | `C-FE-06` |
| `used_bytes` | the storage usage field | `C-CF-240` |
| `16400000` | the event supply in NJR | `C-CF-135` |
| `Confirm your Nightjar waitlist place` | the waitlist email subject prefix | `C-CF-160` |
| `Sitemap:` | the robots sitemap line | `C-CF-168` |
| `/app` | the workspace route prefix | `C-CF-167` |
| `/app/conversations/new` | the wizard first step | `C-UF-01` |
| `/app/conversations/new/people` | the wizard second step | `C-UF-01` |
| `/app/conversations/new/name` | the wizard third step | `C-UF-01` |
| `250000` | the first load byte budget | `C-TR-01` |
| `150000` | the script byte budget | `C-TR-02` |
| `120000` | the font byte budget | `C-TR-03` |
| `efe6e71259fd773f94f0a96ae30a706f1a74dc8a5fd275b71942f37b5f75ab1f` | the watcher public key | `C-TR-05` |
| `deku-demo-pw-2026` | the seeded password | `C-DM-01` |
| `envelopes` | the envelope table | `C-DM-02` |
| `ciphertext` | the sealed bytes column | `C-DM-02` |
| `memberships` | the membership table | `C-DM-03` |
| `trial_ends_at` | the trial end column | `C-DM-03` |
| `wallet_challenges` | the challenge table | `C-DM-04` |
| `expires_at` | the expiry column | `C-DM-04` |
| `file_pieces` | the piece table | `C-DM-05` |
| `file_links` | the link table | `C-DM-06` |
| `40000000000` | the seeded vesting allocation in millionths | `C-DM-10` |
| `visioners` | the Visioners Round schedule key | `C-DM-10` |
| `Open Relay Commons` | the seeded public group | `C-DM-12` |
| `Relay Bulletins` | the seeded channel | `C-DM-13` |
| `APP_PUBLIC_URL` | the public address | `C-DC-01` |
| `/api` | the API prefix | `C-DC-02` |
| `200` | the readiness response | `C-DC-03` |
| `items` | the sync feed list key | `C-DC-07` |
| `next_cursor` | the sync feed cursor key | `C-DC-07` |
| `has_more` | the sync feed continuation key | `C-DC-07` |
| `pool_micro` | the epoch pool key | `C-DC-08` |
| `paid` | the settlement paid list key | `C-DC-09` |
| `remaining` | the settlement remaining count key | `C-DC-09` |
| `deposit_reference` | the quote payment reference | `C-DC-10` |
| `No conversations yet.` | the empty queue line | `C-UF-08` |
| `NJ-MEMBER23` | the second seeded member contact code | `C-RL-12` |
| `member@example.com` | the seeded member | `C-RL-10` |
| `member2@example.com` | the second seeded member | `C-RL-11` |
| `This message can't be opened on this device.` | the unopenable line | `C-CF-19` |
| `stale_epoch` | the stale epoch reason | `C-CF-34` |
| `expired` | the expired link reason | `C-CF-77` |
| `This link has expired.` | the expired link message | `C-CF-77` |
| `500000` | the lowest intended amount in cents | `C-CF-142` |
| `5000000` | the highest intended amount in cents | `C-CF-142` |
| `This confirmation link has already been used.` | the reused confirmation line | `C-CF-162` |
| `X-Watcher-Signature` | the watcher signature header | `C-TR-09` |
| `It cannot move funds.` | the challenge message closing sentence | `C-CF-175` |
| `sender_device_id` | the history tie-break field | `C-CF-177` |
| `core_node` | the pinned routing mode | `C-CF-179` |
| `Introduction` | the introduction region label | `C-CF-180` |
| `block_time` | the payment block time field | `C-CF-184` |
| `team` | the team schedule key | `C-CF-188` |
| `liquidity` | the liquidity schedule key | `C-CF-189` |
| `community` | the community schedule key | `C-CF-190` |
| `Check your inbox to confirm.` | the waitlist accepted line | `C-CF-191` |
| `/waitlist/confirm?token=` | the confirmation link path | `C-CF-192` |
| `/waitlist/remove?token=` | the removal link path | `C-CF-193` |
| `You are on the Nightjar waitlist.` | the confirmed line | `C-CF-194` |
| `Removed. Nightjar no longer holds your address.` | the removed line | `C-CF-195` |
| `Nightjar whitelist application received` | the whitelist subject prefix | `C-CF-199` |
| `Application received. It is not an allocation, and we'll be in touch.` | the whitelist acknowledgement line | `C-CF-200` |
| `/whitelist/details` | the stepper details step | `C-CF-202` |
| `/whitelist/review` | the stepper review step | `C-CF-202` |
| `Wallet address` | the wallet address field | `C-CF-203` |
| `Get message to sign` | the challenge button | `C-CF-203` |
| `Message to sign` | the challenge message field | `C-CF-203` |
| `Signature` | the signature field | `C-CF-203` |
| `Continue` | the continue control | `C-CF-203` |
| `Email` | the email field | `C-CF-204` |
| `Amount in USD` | the amount field | `C-CF-204` |
| `Back` | the back control | `C-CF-141` |
| `Apply` | the apply control | `C-CF-205` |
| `Waiting for approval from one of your other devices.` | the pending device notice | `C-CF-206` |
| `Device 1` | the first device name | `C-CF-207` |
| `Device 2` | the second device name | `C-CF-207` |
| `Approve` | the approve button prefix | `C-CF-208` |
| `Message` | the composer field | `C-CF-209` |
| `Send` | the send button | `C-CF-209` |
| `12` | the token and stablecoin confirmation depth | `C-CF-210` |
| `10` | the privacy coin confirmation depth | `C-CF-211` |
| `65536` | the smallest piece class | `C-CF-212` |
| `1048576` | the middle piece class | `C-CF-212` |
| `4194304` | the largest piece class | `C-CF-212` |
| `aboutSection` | the about section id | `C-CF-213` |
| `featuresSection` | the features section id | `C-CF-213` |
| `ecosystemSection` | the ecosystem section id | `C-CF-213` |
| `tokenSaleSection` | the token sale section id | `C-CF-213` |
| `roadmapSection` | the roadmap section id | `C-CF-213` |
| `faqSection` | the questions section id | `C-CF-213` |
| `subscribeSection` | the subscribe section id | `C-CF-213` |
| `amount` | the payment amount field | `C-CF-215` |
| `settling` | the partly paid epoch state | `C-CF-216` |
| `settled` | the fully paid epoch state | `C-CF-217` |
| `credit` | the payment credit field | `C-CF-220` |
| `app_store` | the store rail | `C-CF-221` |
| `trial` | the trial membership state | `C-CF-223` |
| `Choose file` | the file picker | `C-CF-226` |
| `Upload` | the upload button | `C-CF-226` |
| `Password` | the password field | `C-UF-14` |
| `Sign in` | the sign in button | `C-UF-14` |
| `Create account` | the create account button | `C-UF-15` |
| `Menu` | the phone sidebar button | `C-UF-18` |
| `Board name` | the board wizard name field | `C-CF-232` |
| `Create board` | the board wizard create button | `C-CF-232` |
| `Removed from your storage. Pieces already distributed can't be recalled.` | the file deletion notice | `C-CF-233` |
| `/app/boards/new` | the board wizard first step | `C-UF-09` |
| `/app/boards/new/columns` | the board wizard second step | `C-UF-09` |
| `/app/treasury/whitelist` | the treasurer applications route | `C-UF-11` |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the exact colour shades, carried as family plus tone plus shade | `C-UX-01` | the builder chooses the value inside the stated roles |
| the openly licensed display and text families | `C-UX-03` | the source names no family |
| the exact motion curves and durations, carried as character | `C-UX-05` | the builder chooses the values |
| the breakpoint cut points above the phone tier, carried as named tiers | `C-UX-09` | the builder chooses the widths |

## Coverage ledger

| Section | Graded asks paired | Items produced |
|---|---|---|
| Overview | 3 | 3 |
| User roles | 13 | 13 |
| Core features | 240 | 240 |
| User flow | 18 | 18 |
| UI and UX notes | 14 | 14 |
| Front-end specification | 11 | 11 |
| Technical requirements | 9 | 9 |
| Data model | 13 | 13 |
| Constraints | 3 | 3 |
| Deployment contract | 12 | 12 |

The first column counts the graded asks this checklist pairs to a grading channel, one per item; it is not a count of every obligation-bearing sentence. The brief carries the companion documents in full, and the machine count in the QC report measures every obligation-bearing sentence the brief contains; the balance is carried for fidelity to the source and declared ungraded below rather than cited falsely.

- Declared but ungraded, deployment: `/app/USER_README.md` carrying every seeded address, the reserved `.browser_screenshots/` and `.downloads/` directories, the production build behind a static or preview server, the server outliving its session, binding `0.0.0.0`, and the absence of persistent volumes, fixed container names, custom networks and edge functions are obligations no separately running grader can observe.
- Declared but ungraded, server internals: salted password hashing, the log line contents, the twelve hour session lifetime, private keys never leaving the browser beyond what the traffic shows, sealing under a fresh message key, key agreement over Curve25519 with AES-256, and the separation of the public page's code from the workspace's keys have no outside observable beyond the sealing and traffic rules graded above.
- Declared but ungraded, client behaviour needing conditions no outside request can induce: working with the network off and the `Waiting to send.` state, the idle lock, location sharing, device-side blocking, local call history, upload cancellation, progress on long sealing, retention, and the client compound case answers.
- Declared but ungraded, remaining companion depth: the Front-end specification's provenance, palette, shape, depth, typography, motion, copy deck, zero-asset substitution, responsive, accessibility, architecture, performance, defects, refusals and additions content beyond the items above is carried so the build is specified completely, and no channel grades it item by item.
- Declared but ungraded, window and table asks with no outside observable in the graders: the app store refund removing thirty days, the sponsored notice, the quote line on the membership page, the `/signin?next=` return and the signed-in redirect away from `/signin`, the thirty-second intro release, the banner pausing on hover or focus, the questions' announced expanded state, the `Coming Soon` availability text, public member-list visibility, the seven-day unlock and the below-tier line, the epoch-settled relay line, the vesting line on the token page, the task and link copy lines, no email beyond the two kinds, and the ten thousand envelope scale.
- Declared but ungraded, detail added in the second revision: the display format of amounts other than NJR shares, positions and the epoch remainder, `Key epoch <n>`, the four shape option labels, the `call` sync item with the decline endpoint, `last_seen_address`, `rail_prices`, the derived sponsored days beyond a decline with no self-paid time, the zero contribution with no NJR rate, the derived stake, claimed amount with epoch state, the moved token-sale roadmap entry with the sale date, exactly six sitemap routes, the 44 pixel touch targets with the 3 to 1 ratio for large text, icons and boundaries, journey 15, `Stop relay mode`, the constant-speed banners, the still progress ring under reduced motion, `Member until <date>.`, the `Paid` plus `Unpaid` markers, the lowercase `asset` codes, the latest rate per asset on the membership page, the `app_store` quote line, the un-share endpoint, calls as signalling only, the digest kept after a waitlist removal.
- Declared but ungraded, single sentences with no grader: the relay stores no path; a call placed by a non-member is denied; a call record holds no media key; the same words sent twice store different `ciphertext`; a `link_token` of at least 32 characters with `expires_in_hours` from `1` to `720`; the plain-HTTP secure-origin rule; no wallet-step code fetched before `/whitelist`; the empty states `No boards yet.`, `No files yet.` plus `No vesting positions.`; Escape closing dialogs; the exact type scale; the eleven-link sidebar landmark; dark only; the token-sale no-sale statement.
- Declared but ungraded, sentences added in the last revision: the token event seeded one hundred days before first start; a claim with nothing vested writes no ledger row with the `Claim` button unavailable plus its reason; the sender reading the epoch plus devices from `GET /api/conversations/{conversation_id}/devices` before sealing; the token plus whitepaper pages showing the event instant from `GET /api/token/event`; `GET /api/calls/{call_id}` answering only the call's participants; the stored conversation `epoch` equal to one plus the membership event count.
