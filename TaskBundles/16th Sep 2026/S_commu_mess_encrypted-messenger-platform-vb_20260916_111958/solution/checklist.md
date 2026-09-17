# Checklist: Beacon: Encrypted Messenger Platform

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, techrequirements, datamodel, frontend, buildplan, constraints, deployment, definition of done
Sections absent: none
Items: 590
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` Beacon offers a private messenger beside the marketing home under one name `src: Overview para 1`
- [ ] `C-OV-02` `constraint` Beacon carries no ads, affiliate marketers or trackers of any kind `src: Overview para 3; Constraints, item 11`
- [ ] `C-OV-03` `constraint` Beacon asks for no phone number `src: Overview para 3; Constraints, item 3`
- [ ] `C-OV-04` `constraint` The service offers no reading, indexing, searching or moderation of message content `src: Overview para 3; Constraints, item 13`
- [ ] `C-OV-05` `constraint` Beacon sends no SMS `src: Overview para 3; Constraints, item 3`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor without a device token cannot fetch envelopes `src: User roles table row 1`
- [ ] `C-RL-02` `role` A visitor without a device token cannot fetch key bundles `src: User roles table row 1`
- [ ] `C-RL-03` `role` A person cannot unlink a device belonging to another account `src: User roles table row 2`
- [ ] `C-RL-04` `role` A person who is not a group member cannot change the group `src: User roles table row 2`
- [ ] `C-RL-05` `role` A denied call leaves the protected state unchanged `src: User roles, authorization paragraph`
- [ ] `C-RL-06` `capability` Signup at `/signup` is open to anyone `src: User roles, signup paragraph`
- [ ] `C-RL-07` `literal` The seeded account `user@example.com` carries the username `nova` `src: User roles, seeded accounts table row 1`
- [ ] `C-RL-08` `literal` The seeded account `user2@example.com` carries the username `juniper` `src: User roles, seeded accounts table row 2`
- [ ] `C-RL-09` `literal` The seeded account `user3@example.com` carries the username `sol` `src: User roles, seeded accounts table row 3`
- [ ] `C-RL-10` `literal` The seeded account `user4@example.com` carries the username `wren` `src: User roles, seeded accounts table row 4`
- [ ] `C-RL-11` `role` A visitor with no account reads `/`, the eleven translations, the declared pages with `/terms` `src: User roles table row 1; User flow, route table`
- [ ] `C-RL-12` `role` A visitor with no account gives a donation through `POST /api/donations` `src: User roles table row 1`

## C-CF Core features

- [ ] `C-CF-01` `constraint` The service never holds the plaintext of any message, call, name, avatar or attachment `src: Core features, opening paragraph`
- [ ] `C-CF-02` `capability` A one-to-one send to another person carries the `Unidentified-Access-Key` header with no `Authorization` header `src: Core features, feature 1 rule 1`
- [ ] `C-CF-03` `constraint` A send with a wrong or missing access key is denied with nothing queued `src: Core features, feature 1 rule 1`
- [ ] `C-CF-04` `constraint` A device-token send addressed to another account is denied with nothing queued `src: Core features, feature 1 rule 2; User roles table row 2`
- [ ] `C-CF-05` `capability` A device-token send addressed to the caller's own account is accepted `src: Core features, feature 1 rule 2`
- [ ] `C-CF-06` `constraint` A send leaving out an active device is rejected with `missing_devices` naming the device id `src: Core features, feature 1 rule 3`
- [ ] `C-CF-07` `constraint` A send to an account with no active device is rejected, queuing nothing `src: Core features, feature 1 rule 3`
- [ ] `C-CF-08` `constraint` A send naming a device outside the active set is rejected with `extra_devices` naming the device id `src: Core features, feature 1 rule 3`
- [ ] `C-CF-09` `constraint` A rejected device-mismatch send queues nothing for any device `src: Core features, feature 1 rule 3`
- [ ] `C-CF-10` `constraint` A send to your own account names every active device except the sending device `src: Core features, feature 1 rule 3`
- [ ] `C-CF-11` `capability` `GET /api/messages` returns only the envelopes waiting for the calling device, oldest first `src: Core features, feature 1 rule 4`
- [ ] `C-CF-12` `constraint` Another account never receives envelopes queued for a different account's device `src: Core features, feature 1 rule 4`
- [ ] `C-CF-13` `constraint` Acknowledging a guid queued for another device is rejected with the envelope still queued `src: Core features, feature 1 rule 4; User roles table row 2`
- [ ] `C-CF-14` `data` An envelope carries exactly the fields `guid`, `ciphertext`, `server_timestamp`, `group_id` `src: Core features, feature 1 rule 5`
- [ ] `C-CF-15` `constraint` No envelope field or stored row names the sender `src: Core features, feature 1 rule 5; Data model, envelopes table`
- [ ] `C-CF-16` `capability` `DELETE /api/messages/{guid}` deletes the envelope ciphertext from the database outright `src: Core features, feature 1 rule 6`
- [ ] `C-CF-17` `constraint` Acknowledging on one device leaves another device's copy of the guid queued `src: Core features, feature 1 rule 6`
- [ ] `C-CF-18` `constraint` A resent guid already queued for a device queues no second copy `src: Core features, feature 1 rule 7`
- [ ] `C-CF-19` `constraint` A resent guid already acknowledged by a device is never delivered again `src: Core features, feature 1 rule 7`
- [ ] `C-CF-20` `constraint` Simultaneous duplicate sends of one guid leave one envelope `src: Core features, feature 1 rule 7`
- [ ] `C-CF-21` `constraint` A device holds at most 1000 waiting envelopes, dropping the oldest first, even under simultaneous sends `src: Core features, feature 1 rule 8`
- [ ] `C-CF-22` `constraint` A ciphertext outside 1 to 1048576 bytes of standard base64 with padding is rejected with nothing queued `src: Core features, feature 1 rule 9`
- [ ] `C-CF-23` `constraint` A guid that is not a lowercase UUID is rejected with nothing queued `src: Core features, feature 1 rule 9`
- [ ] `C-CF-24` `capability` An accepted send to another account with every device queue empty sends one nudge email through Mailpit `src: Core features, feature 2 rule 1`
- [ ] `C-CF-25` `constraint` The nudge email goes only to the recipient account's email address with no cc or bcc `src: Core features, feature 2 rule 1`
- [ ] `C-CF-26` `literal` The nudge subject is `You have something waiting on Beacon` `src: Core features, feature 2 rule 2`
- [ ] `C-CF-27` `literal` The nudge body is `Open Beacon to read what is waiting for you.` `src: Core features, feature 2 rule 2`
- [ ] `C-CF-28` `constraint` The nudge email never names the sender, the message, the ciphertext, the guid or a group `src: Core features, feature 2 rule 3`
- [ ] `C-CF-29` `constraint` No nudge is sent during a period when the recipient account still has envelopes waiting `src: Core features, feature 2 rule 4`
- [ ] `C-CF-30` `constraint` No nudge is sent for a send to your own devices `src: Core features, feature 2 rule 4`
- [ ] `C-CF-31` `constraint` No nudge is sent for a rejected send `src: Core features, feature 2 rule 4`
- [ ] `C-CF-32` `constraint` No nudge is sent for an idempotent resend `src: Core features, feature 2 rule 4`
- [ ] `C-CF-33` `capability` `POST /api/auth/signup` creates an account from an email, a username with a password `src: Core features, feature 3 rule 1`
- [ ] `C-CF-34` `constraint` A username outside `^[a-z][a-z0-9_]{2,19}$` is rejected with nothing stored `src: Core features, feature 3 rule 1`
- [ ] `C-CF-35` `constraint` A password shorter than 12 characters is rejected with nothing stored `src: Core features, feature 3 rule 1`
- [ ] `C-CF-36` `constraint` An email differing from an existing one only in letter case is rejected `src: Core features, feature 3 rule 1`
- [ ] `C-CF-37` `constraint` A username already taken is rejected with nothing stored `src: Core features, feature 3 rule 1`
- [ ] `C-CF-38` `constraint` The plaintext password never appears in any database row `src: Core features, feature 3 rule 2`
- [ ] `C-CF-39` `capability` `POST /api/auth/login` returns an `access_token` `src: Core features, feature 3 rule 3`
- [ ] `C-CF-40` `constraint` Five consecutive wrong passwords lock sign-in for that email for fifteen minutes, even with the right password `src: Core features, feature 3 rule 3`
- [ ] `C-CF-41` `constraint` Simultaneous wrong passwords never buy more than five attempts before the lock `src: Core features, feature 3 rule 3`
- [ ] `C-CF-42` `constraint` An account token is accepted only by `POST /api/devices`, `POST /api/recovery/restore`, `GET /api/me`, rejected by every other device endpoint `src: Core features, feature 3 rule 4`
- [ ] `C-CF-43` `capability` `POST /api/devices` returns a `device_id` beside a `device_token` `src: Core features, feature 4 rule 1`
- [ ] `C-CF-44` `constraint` Device ids start at 1 per account, never reused `src: Core features, feature 4 rule 1`
- [ ] `C-CF-45` `capability` An account with no active device registers the first device freely `src: Core features, feature 4 rule 2`
- [ ] `C-CF-46` `constraint` A later device without a link code is denied with no device created `src: Core features, feature 4 rule 2`
- [ ] `C-CF-47` `constraint` A link code from another account, an unknown code or a used code is denied `src: Core features, feature 4 rule 2`
- [ ] `C-CF-48` `capability` `POST /api/devices/link-codes` issues an eight-character code of capital letters or digits `src: Core features, feature 4 rule 3`
- [ ] `C-CF-49` `constraint` A link code links one device for its own account once `src: Core features, feature 4 rule 3`
- [ ] `C-CF-50` `constraint` A link code presented by two registrations at the same moment admits one device `src: Core features, feature 4 rule 3`
- [ ] `C-CF-51` `capability` Registration with `replace_existing` plus the right recovery `access_verifier` revokes every active device `src: Core features, feature 4 rule 4`
- [ ] `C-CF-52` `constraint` A replacement with a wrong verifier counts as a wrong recovery guess, creating nothing `src: Core features, feature 4 rule 4`
- [ ] `C-CF-53` `constraint` Replaced devices lose their tokens with their waiting envelopes deleted `src: Core features, feature 4 rule 4`
- [ ] `C-CF-54` `capability` `GET /api/devices` lists the account's active devices `src: Core features, feature 4 rule 5`
- [ ] `C-CF-55` `constraint` An unlinked device's token is rejected everywhere `src: Core features, feature 4 rule 5`
- [ ] `C-CF-56` `constraint` An unlinked device's waiting envelopes are deleted `src: Core features, feature 4 rule 5`
- [ ] `C-CF-57` `constraint` An unlinked device disappears from key bundles `src: Core features, feature 4 rule 5`
- [ ] `C-CF-58` `constraint` A send naming an unlinked device is rejected with that device id in `extra_devices` `src: Core features, feature 4 rule 5`
- [ ] `C-CF-59` `capability` A newly linked browser receives messages from the moment of linking `src: Core features, feature 4 rule 6`
- [ ] `C-CF-60` `constraint` Nothing about earlier conversations is ever staged readable on the service for a newly linked browser `src: Core features, feature 4 rule 6`
- [ ] `C-CF-61` `constraint` Registration without a well-formed identity key, signed pre-key or post-quantum pre-key is rejected `src: Core features, feature 5 rule 1`
- [ ] `C-CF-62` `constraint` One upload carries at most 100 one-time pre-keys `src: Core features, feature 5 rule 1`
- [ ] `C-CF-63` `capability` Registration accepts keys of the stated sizes without the service verifying signatures `src: Core features, feature 5 rule 1`
- [ ] `C-CF-64` `capability` `GET /api/keys/{username}` returns the access key with one bundle per active device `src: Core features, feature 5 rule 2`
- [ ] `C-CF-65` `constraint` A one-time pre-key is handed out at most once, even under simultaneous requests `src: Core features, feature 5 rule 2`
- [ ] `C-CF-66` `capability` A device with no one-time pre-keys left still returns a bundle with `one_time_prekey` null `src: Core features, feature 5 rule 2`
- [ ] `C-CF-67` `literal` An account that never published a profile returns `access_key` null `src: Core features, feature 5 rule 2`
- [ ] `C-CF-68` `literal` An account with no active device returns `devices` as an empty list `src: Core features, feature 5 rule 2`
- [ ] `C-CF-69` `capability` `POST /api/keys/one-time` adds one-time pre-keys `src: Core features, feature 5 rule 3`
- [ ] `C-CF-70` `capability` `GET /api/keys/count` returns the calling device's remaining one-time pre-keys `src: Core features, feature 5 rule 3`
- [ ] `C-CF-71` `constraint` Uploading a key id already uploaded for that device is rejected `src: Core features, feature 5 rule 3`
- [ ] `C-CF-72` `constraint` A device making more than 300 `GET /api/keys/{username}` requests in a rolling sixty seconds is refused `src: Core features, feature 5 rule 4`
- [ ] `C-CF-73` `constraint` Contact discovery is exact-username lookup with no directory of accounts `src: Core features, feature 5 rule 5; Constraints, item 3`
- [ ] `C-CF-74` `capability` `POST /api/groups` makes the creator the only admin at revision 1 `src: Core features, feature 6 rule 1`
- [ ] `C-CF-75` `constraint` A group naming an unknown username is rejected with no group created `src: Core features, feature 6 rule 1`
- [ ] `C-CF-76` `capability` Joining a group by invite happens when the admin adds the invited username `src: Core features, feature 6 rule 1`
- [ ] `C-CF-77` `capability` A group change carrying the current `expected_revision` raises the revision by one `src: Core features, feature 6 rule 2`
- [ ] `C-CF-78` `constraint` Of two simultaneous same-revision group changes exactly one succeeds `src: Core features, feature 6 rule 2`
- [ ] `C-CF-79` `constraint` The losing group change returns the current `revision` with nothing changed `src: Core features, feature 6 rule 2`
- [ ] `C-CF-80` `role` Only the group admin may add members, remove someone else or replace the encrypted state `src: Core features, feature 6 rule 3; User roles, authorization paragraph`
- [ ] `C-CF-81` `capability` A group member who is not the admin may change the group only to remove themselves `src: Core features, feature 6 rule 3`
- [ ] `C-CF-82` `capability` A group send takes one ciphertext queued for every current member device except the sending device `src: Core features, feature 6 rule 4`
- [ ] `C-CF-83` `constraint` A removed member receives nothing sent after removal `src: Core features, feature 6 rule 4`
- [ ] `C-CF-84` `constraint` A newly added member receives nothing sent before joining `src: Core features, feature 6 rule 4`
- [ ] `C-CF-85` `constraint` A group send from a non-member is denied with nothing queued `src: Core features, feature 6 rule 4`
- [ ] `C-CF-86` `capability` `GET /api/groups/{group_id}` returns one roster to every member `src: Core features, feature 6 rule 5`
- [ ] `C-CF-87` `constraint` A group read from a non-member is denied `src: Core features, feature 6 rule 5`
- [ ] `C-CF-88` `capability` The group conversation header starts a voice call to the whole group `src: Core features, feature 6 rule 6`
- [ ] `C-CF-89` `capability` Sign-in on a browser holding no device for an account without devices registers the browser without asking `src: Core features, feature 7 rule 1`
- [ ] `C-CF-90` `capability` Sign-in for an account whose devices are elsewhere lands on `/link` offering a link code or the recovery PIN `src: Core features, feature 7 rule 1; User flow, entry and redirects`
- [ ] `C-CF-91` `capability` Registering a device in the browser publishes the encrypted profile with the access key before `/chats` `src: Core features, feature 7 rule 2`
- [ ] `C-CF-92` `capability` A reload or new tab asks for the account password at `/unlock` before showing stored conversations `src: Core features, feature 7 rule 3`
- [ ] `C-CF-93` `capability` Each `/chats` row previews the last message `src: Core features, feature 7 rule 4`
- [ ] `C-CF-94` `capability` Each `/chats` row shows the number of unread messages `src: Core features, feature 7 rule 4`
- [ ] `C-CF-95` `ui` Each chats row shows the other person's name with the time of the last message `src: Core features, feature 7 rule 4`
- [ ] `C-CF-96` `capability` The `New chat` dialog starts a conversation with an exact username `src: Core features, feature 7 rule 4`
- [ ] `C-CF-97` `capability` The `New group` dialog creates a group from a name with usernames `src: Core features, feature 7 rule 4`
- [ ] `C-CF-98` `capability` The conversation view lists messages oldest to newest `src: Core features, feature 7 rule 5`
- [ ] `C-CF-99` `literal` An outgoing bubble shows one of `Sending`, `Sent`, `Delivered`, `Read` `src: Core features, feature 7 rule 5`
- [ ] `C-CF-100` `constraint` Delivery receipts travel as sealed messages `src: Core features, feature 7 rule 5`
- [ ] `C-CF-101` `capability` New messages appear within five seconds without a reload `src: Core features, feature 7 rule 6`
- [ ] `C-CF-102` `capability` The composer sends photos `src: Core features, feature 7 rule 7`
- [ ] `C-CF-103` `capability` The composer sends video `src: Core features, feature 7 rule 7`
- [ ] `C-CF-104` `capability` The composer sends files `src: Core features, feature 7 rule 7`
- [ ] `C-CF-105` `capability` The composer sends voice messages recorded with the microphone `src: Core features, feature 7 rule 7`
- [ ] `C-CF-106` `capability` The composer sends stickers from the built-in sticker pack `src: Core features, feature 7 rule 7`
- [ ] `C-CF-107` `constraint` Attachment bytes never reach the service readable `src: Core features, feature 7 rule 7`
- [ ] `C-CF-108` `capability` An edit to an outgoing message reaches the user's other devices with the other people in the conversation `src: Core features, feature 7 rule 8`
- [ ] `C-CF-109` `capability` Deleting an outgoing message after confirmation removes the message on the user's linked devices `src: Core features, feature 7 rule 8`
- [ ] `C-CF-110` `capability` Archiving a conversation removes the conversation row from `/chats` on every linked browser of the user `src: Core features, feature 7 rule 8`
- [ ] `C-CF-111` `capability` The conversation header offers a mute control beside archive `src: Core features, feature 7 rule 8`
- [ ] `C-CF-112` `capability` The conversation header starts a voice call opening the call screen with a hang-up control `src: Core features, feature 7 rule 9`
- [ ] `C-CF-113` `capability` The conversation header starts a video call opening the call screen `src: Core features, feature 7 rule 9`
- [ ] `C-CF-114` `capability` The called person's open Beacon shows an incoming call naming the caller with answer or decline controls `src: Core features, feature 7 rule 9`
- [ ] `C-CF-115` `capability` Declining or hanging up closes both call screens within five seconds `src: Core features, feature 7 rule 9`
- [ ] `C-CF-116` `capability` A profile name set at `/settings/profile` appears in a contact's conversation header `src: Core features, feature 7 rule 10`
- [ ] `C-CF-117` `constraint` The profile name reaches the service only as `profile_ciphertext` `src: Core features, feature 7 rule 10`
- [ ] `C-CF-118` `capability` `/settings/devices` lists linked devices `src: Core features, feature 7 rule 11`
- [ ] `C-CF-119` `capability` `/settings/devices` issues a link code `src: Core features, feature 7 rule 11`
- [ ] `C-CF-120` `capability` Signing out from `/settings/devices` returns the browser to `/login` `src: Core features, feature 7 rule 11`
- [ ] `C-CF-121` `literal` `/settings/recovery` saves a PIN of six or more digits, confirming `Recovery PIN saved` `src: Core features, feature 7 rule 12`
- [ ] `C-CF-122` `capability` `POST /api/recovery/restore` returns the recovery record for the right verifier `src: Core features, feature 7 rule 12`
- [ ] `C-CF-123` `literal` A wrong verifier is refused with `remaining_guesses` `src: Core features, feature 7 rule 12`
- [ ] `C-CF-124` `constraint` Ten consecutive wrong guesses destroy the recovery record `src: Core features, feature 7 rule 12`
- [ ] `C-CF-125` `constraint` A right guess resets the wrong-guess count `src: Core features, feature 7 rule 12`
- [ ] `C-CF-126` `constraint` Simultaneous wrong recovery guesses never buy more than ten `src: Core features, feature 7 rule 12`
- [ ] `C-CF-127` `constraint` A tampered message is never shown `src: Core features, feature 8 rule 1`
- [ ] `C-CF-128` `capability` A dropped tampered message shows the pinned decrypt notice on `/chats` `src: Core features, feature 8 rule 1`
- [ ] `C-CF-129` `constraint` A replayed message under a new guid appears once `src: Core features, feature 8 rule 2`
- [ ] `C-CF-130` `capability` Messages arriving out of order or after a gap appear in the order written `src: Core features, feature 8 rule 3`
- [ ] `C-CF-131` `constraint` The same text sent twice in one conversation produces two different ciphertext values `src: Core features, feature 8 rule 4`
- [ ] `C-CF-132` `constraint` A message whose session cannot be established stays Sending, with no request carrying the text `src: Core features, feature 8 rule 5`
- [ ] `C-CF-133` `capability` A contact identity change shows a banner blocking sends until accepted `src: Core features, feature 8 rule 6`
- [ ] `C-CF-134` `capability` The safety number shows sixty digits in twelve groups of five `src: Core features, feature 9 rule 1`
- [ ] `C-CF-135` `constraint` Two people see the same safety number for each other `src: Core features, feature 9 rule 2`
- [ ] `C-CF-136` `constraint` The safety number changes when either side's identity keys change `src: Core features, feature 9 rule 3`
- [ ] `C-CF-137` `capability` Each conversation offers a disappearing-message timer of off, 30 seconds, 5 minutes, 1 hour, 1 day or 1 week `src: Core features, feature 10 rule 1`
- [ ] `C-CF-138` `capability` A timer change applies on every participant's devices `src: Core features, feature 10 rule 1`
- [ ] `C-CF-139` `capability` The conversation header shows the disappearing-message timer whenever one is set `src: Core features, feature 10 rule 1`
- [ ] `C-CF-140` `constraint` A timed message is deleted from every participant's devices when the time runs out `src: Core features, feature 10 rule 2`
- [ ] `C-CF-141` `constraint` Browser storage holds no readable message text, attachment bytes or profile names `src: Core features, feature 10 rule 3`
- [ ] `C-CF-142` `literal` The `/donate` amounts are `$5`, `$10`, `$25`, `$50`, `$100` beside a custom dollar amount `src: Core features, feature 11 rule 1`
- [ ] `C-CF-143` `constraint` The donation page asks for no card details `src: Core features, feature 11 rule 1`
- [ ] `C-CF-144` `literal` A recorded gift shows the inline banner `Thank you. Your gift of $25.00 was received.` with the gift's own amount in place of `$25.00` `src: Core features, feature 11 rule 1`
- [ ] `C-CF-145` `capability` `POST /api/donations` returns `amount_minor`, `currency` with `status` set to received `src: Core features, feature 11 rule 2`
- [ ] `C-CF-146` `constraint` `amount_minor` is an integer from 100 to 1000000 `src: Core features, feature 11 rule 2`
- [ ] `C-CF-147` `literal` `currency` is exactly `usd` `src: Core features, feature 11 rule 2`
- [ ] `C-CF-148` `constraint` A donation without an `Idempotency-Key` header is rejected `src: Core features, feature 11 rule 3`
- [ ] `C-CF-149` `constraint` A refused donation stores nothing with no email sent `src: Core features, feature 11 rule 3`
- [ ] `C-CF-150` `capability` The donation form shows a refusal inline naming the field `src: Core features, feature 11 rule 3`
- [ ] `C-CF-151` `constraint` Repeating an `Idempotency-Key` with the same body stores nothing new `src: Core features, feature 11 rule 4`
- [ ] `C-CF-152` `constraint` Simultaneous repeats of one `Idempotency-Key` record one gift `src: Core features, feature 11 rule 4`
- [ ] `C-CF-153` `constraint` One `Idempotency-Key` sent with a different body is rejected `src: Core features, feature 11 rule 4`
- [ ] `C-CF-154` `capability` Each recorded gift sends exactly one receipt email to the donor only `src: Core features, feature 11 rule 5`
- [ ] `C-CF-155` `literal` The receipt subject is `Thank you for supporting Beacon` `src: Core features, feature 11 rule 5`
- [ ] `C-CF-156` `capability` The receipt body names the amount written like $25.00 beside Beacon Technology Foundation `src: Core features, feature 11 rule 5`
- [ ] `C-CF-157` `capability` The HTML served for `/` already carries `Speak Freely`, the lead, the `Get Beacon` button before any script runs `src: Core features, feature 12 rule 1`
- [ ] `C-CF-158` `literal` The English home root element declares `lang="en"` `src: Core features, feature 12 rule 1`
- [ ] `C-CF-159` `capability` Each of the eleven locale routes serves a complete document before any script runs `src: Core features, feature 12 rule 2`
- [ ] `C-CF-160` `ui` Each locale route shows the home translated into its language `src: Core features, feature 12 rule 2`
- [ ] `C-CF-161` `constraint` Each locale document declares its own language code on the root element `src: Core features, feature 12 rule 2`
- [ ] `C-CF-162` `literal` The `/ar` document declares `dir="rtl"` `src: Core features, feature 12 rule 2`
- [ ] `C-CF-163` `capability` The top bar language control shows the current language's own name `src: Core features, feature 12 rule 3`
- [ ] `C-CF-164` `capability` The language control opens the dialog `Select your language` listing twelve language names `src: Core features, feature 12 rule 3`
- [ ] `C-CF-165` `constraint` The open language dialog keeps keyboard focus inside the dialog `src: Core features, feature 12 rule 3`
- [ ] `C-CF-166` `capability` Escape closes the language dialog, returning focus to the language control `src: Core features, feature 12 rule 3`
- [ ] `C-CF-167` `constraint` A marketing page requests nothing from any other origin `src: Core features, feature 12 rule 4`
- [ ] `C-CF-168` `capability` The declared pages render the top bar with the footer around their own heading `src: Core features, feature 12 rule 5`
- [ ] `C-CF-169` `capability` `/get` offers Android, iPhone or iPad store listings beside Windows, Mac or Linux downloads `src: Core features, feature 12 rule 5`
- [ ] `C-CF-170` `capability` Every listed marketing page footer links to `/terms`, reading `Terms & Privacy Policy` on the English pages `src: Core features, feature 12 rule 6`
- [ ] `C-CF-171` `capability` The `/terms` privacy page carries the privacy table word for word `src: Core features, feature 12 rule 6`
- [ ] `C-CF-172` `capability` `/sitemap.xml` lists exactly the twenty public routes as absolute addresses built from `APP_PUBLIC_URL` `src: Core features, feature 12 rule 7`
- [ ] `C-CF-173` `capability` `/robots.txt` carries a `Sitemap:` line pointing at the sitemap `src: Core features, feature 12 rule 7`
- [ ] `C-CF-174` `capability` `GET /api/me` returns `username` with `email` `src: Core features, feature 3 rule 4; Deployment contract, API shapes`
- [ ] `C-CF-175` `capability` `GET /api/me` accepts an account token or a device token `src: Core features, feature 3 rule 4`
- [ ] `C-CF-176` `constraint` A signup with an invalid email is rejected with nothing stored `src: Core features, feature 3 rule 1`
- [ ] `C-CF-177` `capability` A device with no existing device to authorise the addition joins only through the recovery replacement `src: Core features, feature 4 rule 2`
- [ ] `C-CF-178` `constraint` A newly linked browser shows no message from before linking `src: Core features, feature 4 rule 6`
- [ ] `C-CF-179` `constraint` A key bundle request for a username with no account is rejected `src: Core features, feature 5 rule 2`
- [ ] `C-CF-180` `constraint` A leaving member carries the current `encrypted_state` unchanged, a different state counting as a replacement `src: Core features, feature 6 rule 3`
- [ ] `C-CF-181` `capability` A group send applies the nudge rule to each member account `src: Core features, feature 6 rule 4`
- [ ] `C-CF-182` `capability` The group conversation header starts a video call to the whole group `src: Core features, feature 6 rule 6`
- [ ] `C-CF-183` `capability` Starting a group call opens the call screen naming the group with a hang-up control `src: Core features, feature 6 rule 6`
- [ ] `C-CF-184` `capability` A group call shows every other member's open Beacon an incoming call naming the group `src: Core features, feature 6 rule 6`
- [ ] `C-CF-185` `capability` `PUT /api/profile` stores `profile_ciphertext` beside `access_key` `src: Core features, feature 7 rule 2`
- [ ] `C-CF-186` `capability` Replacing every device with the recovery PIN on `/link` lands on `/chats` with the recovery contacts plus settings restored, showing no earlier message `src: Core features, feature 7 rule 2`
- [ ] `C-CF-187` `capability` Unlocking at `/unlock` returns to the route first asked for `src: Core features, feature 7 rule 3`
- [ ] `C-CF-188` `capability` A `New chat` username with no account shows an inline banner in the dialog, opening no conversation `src: Core features, feature 7 rule 4`
- [ ] `C-CF-189` `literal` An outgoing bubble reads `Sent` once the service accepts the message `src: Core features, feature 7 rule 5`
- [ ] `C-CF-190` `literal` An outgoing bubble reads `Delivered` once a recipient device decrypts the message `src: Core features, feature 7 rule 5`
- [ ] `C-CF-191` `literal` An outgoing bubble reads `Read` once a recipient screen shows the message `src: Core features, feature 7 rule 5`
- [ ] `C-CF-192` `capability` Delivery or read receipts appear within five seconds without a reload `src: Core features, feature 7 rule 6`
- [ ] `C-CF-193` `capability` An incoming call appears within five seconds without a reload `src: Core features, feature 7 rule 6`
- [ ] `C-CF-194` `capability` The composer sends text messages `src: Core features, feature 7 rule 7`
- [ ] `C-CF-195` `literal` The built-in sticker pack holds six stickers: `Wave`, `Heart`, `Thumbs Up`, `Laugh`, `Party`, `Beacon Light` `src: Core features, feature 7 rule 7; Front-end specification, machine-readable hooks`
- [ ] `C-CF-196` `capability` Muting marks the conversation row with `data-muted` set to `true` `src: Core features, feature 7 rule 8`
- [ ] `C-CF-197` `capability` Muting converges on every linked browser of the user `src: Core features, feature 7 rule 8`
- [ ] `C-CF-198` `capability` Reading on one browser converges the read state on the user's other browsers `src: Core features, feature 7 rule 8`
- [ ] `C-CF-199` `capability` The call screen names the other person `src: Core features, feature 7 rule 9`
- [ ] `C-CF-200` `constraint` Call media flows directly between the two browsers `src: Core features, feature 7 rule 9`
- [ ] `C-CF-201` `capability` `GET /api/profile/{username}` returns the account's `profile_ciphertext` to a device `src: Core features, feature 7 rule 10`
- [ ] `C-CF-202` `capability` `/settings/devices` unlinks a linked device `src: Core features, feature 7 rule 11`
- [ ] `C-CF-203` `capability` Signing out unlinks the browser's own device `src: Core features, feature 7 rule 11`
- [ ] `C-CF-204` `capability` Signing out wipes what the browser stored `src: Core features, feature 7 rule 11`
- [ ] `C-CF-205` `capability` `PUT /api/recovery` stores `recovery_blob` beside `access_verifier` `src: Core features, feature 7 rule 12`
- [ ] `C-CF-206` `constraint` A tampered message is acknowledged, leaving no stored envelope `src: Core features, feature 8 rule 1`
- [ ] `C-CF-207` `constraint` No two envelopes a client sends carry the same ciphertext `src: Core features, feature 8 rule 4`
- [ ] `C-CF-208` `capability` A message whose session cannot start shows an inline banner naming the failure `src: Core features, feature 8 rule 5`
- [ ] `C-CF-209` `capability` A timed message leaves the sender's devices counted from sending `src: Core features, feature 10 rule 2`
- [ ] `C-CF-210` `capability` A timed message leaves a recipient's devices counted from first display `src: Core features, feature 10 rule 2`
- [ ] `C-CF-211` `constraint` An `Idempotency-Key` outside 8 to 64 letters, digits, `_` or `-` is rejected `src: Core features, feature 11 rule 2`
- [ ] `C-CF-212` `constraint` A donation with an invalid email is rejected with nothing stored `src: Core features, feature 11 rule 3`
- [ ] `C-CF-213` `capability` A repeated `Idempotency-Key` with the same body returns the same gift `src: Core features, feature 11 rule 4`
- [ ] `C-CF-214` `capability` A resend of a guid already queued for a device is accepted `src: Core features, feature 1 rule 7`
- [ ] `C-CF-215` `data` A one-to-one envelope carries `group_id` null `src: Core features, feature 1 rule 5`
- [ ] `C-CF-216` `data` `missing_devices` with `extra_devices` list device ids in ascending order `src: Core features, feature 1 rule 3`
- [ ] `C-CF-217` `constraint` A send naming one device twice is rejected with nothing queued `src: Core features, feature 1 rule 3`
- [ ] `C-CF-218` `constraint` A group change carrying a stale `expected_revision` is rejected with the current `revision` `src: Core features, feature 6 rule 2; Deployment contract, API shapes`
- [ ] `C-CF-219` `capability` Each language name in the dialog links to its route `src: Core features, feature 12 rule 3`
- [ ] `C-CF-220` `capability` The language dialog close control closes the dialog `src: Core features, feature 12 rule 3`
- [ ] `C-CF-221` `capability` Sign-up at `/signup` lands on `/chats` `src: Core features, feature 7 rule 1`
- [ ] `C-CF-222` `constraint` The browser learns of new envelopes only by requesting `GET /api/messages`, never through a push channel `src: Core features, feature 7 rule 6`
- [ ] `C-CF-223` `capability` The call screen opens at once regardless of microphone or camera access, showing any media failure inside the call screen `src: Core features, feature 7 rule 9`
- [ ] `C-CF-224` `constraint` The wrong recovery guess count survives restarts `src: Core features, feature 7 rule 12`
- [ ] `C-CF-225` `capability` A linked browser also receives what the user sends from other browsers `src: Core features, feature 4 rule 6`
- [ ] `C-CF-226` `capability` Later messages show as soon as each decrypts, a late message taking its written position on arrival `src: Core features, feature 8 rule 3`
- [ ] `C-CF-227` `capability` Each browser keeps its conversations, messages, unread counts, contacts, settings between visits `src: Core features, feature 10 rule 3`
- [ ] `C-CF-228` `capability` Creating a group in the `New group` dialog opens `/groups/{group_id}` `src: Core features, feature 7 rule 4`
- [ ] `C-CF-229` `capability` A resend of a guid the device already acknowledged is accepted `src: Core features, feature 1 rule 7`
- [ ] `C-CF-230` `capability` The language dialog close control returns focus to the language control `src: Core features, feature 12 rule 3`
- [ ] `C-CF-231` `capability` A wrong password at `/unlock` shows an inline banner, keeping the store locked `src: Core features, feature 7 rule 3`
- [ ] `C-CF-232` `capability` A chosen file goes when Send is pressed `src: Core features, feature 7 rule 7`
- [ ] `C-CF-233` `constraint` The recovery record is encrypted in the browser under a key derived from the PIN, unreadable by the service `src: Core features, feature 7 rule 12`

## C-UF User flow

- [ ] `C-UF-01` `capability` Opening a device route without signing in redirects to `/login` `src: User flow, entry and redirects`
- [ ] `C-UF-02` `capability` Sign-in lands on `/chats` `src: User flow, entry and redirects`
- [ ] `C-UF-03` `capability` A browser whose device was unlinked or replaced elsewhere returns to `/login` showing the pinned unlinked banner `src: User flow, entry and redirects`
- [ ] `C-UF-04` `capability` A user opening a group without membership sees the pinned group-unavailable message `src: User flow, entry and redirects`
- [ ] `C-UF-05` `capability` The `/link` screen links a browser with a code from the user's first browser `src: User flow, journey 8`
- [ ] `C-UF-06` `literal` The `/chats` list shows the empty state `No conversations yet` `src: User flow, states`
- [ ] `C-UF-07` `ui` Every page shows a loading state during a wait `src: User flow, states`
- [ ] `C-UF-08` `ui` A failed request shows an inline banner saying what went wrong `src: User flow, states`
- [ ] `C-UF-09` `capability` Errors leave no blank or broken page `src: User flow, states`
- [ ] `C-UF-10` `literal` `/chats/{username}` shows the conversation view `src: User flow, route table`
- [ ] `C-UF-11` `literal` `/chats/{username}/safety` shows the safety number `src: User flow, route table`
- [ ] `C-UF-12` `literal` `/groups/{group_id}` shows the group conversation view with its members `src: User flow, route table`
- [ ] `C-UF-13` `literal` The declared pages live at `/get`, `/help`, `/blog`, `/developers`, `/careers`, `/brand` `src: User flow, route table; Core features, feature 12 rule 5`
- [ ] `C-UF-14` `literal` The locale routes are `/af`, `/ar`, `/az`, `/bg`, `/bn`, `/bs`, `/ca`, `/cs`, `/da`, `/de`, `/el` `src: User flow, route table; Core features, feature 12 rule 2`
- [ ] `C-UF-15` `literal` `/signup` creates an account, `/login` signs in, `/unlock` unlocks the browser `src: User flow, route table`
- [ ] `C-UF-16` `capability` The group-unavailable screen offers a way back to `/chats` `src: User flow, entry and redirects`
- [ ] `C-UF-17` `capability` A browser whose device was unlinked or replaced elsewhere wipes its store `src: User flow, entry and redirects`
- [ ] `C-UF-18` `capability` Every list shows an empty state when empty `src: User flow, states`

## C-UX UI/UX notes

- [ ] `C-UX-01` `ui` The home shows no scroll-scrubbed animation, runtime motion graphics or dark hero video `src: UI/UX notes, north star paragraph`
- [ ] `C-UX-02` `capability` Primary text is a near-black neutral ink on near-white neutral grounds `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-03` `ui` Vivid blues appear only on controls a person can act on, the wordmark or outgoing bubbles `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-04` `capability` The changed-identity warning wears one deep amber beside its words `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-05` `ui` The hero band is a light periwinkle, a light soft blue `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-06` `capability` The footer uses deep cool or near-black neutrals with near-white text `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-07` `ui` Illustrations add only a soft teal panel, a violet accent or a pale teal band `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-08` `capability` Inter supplies every text on the home in the extrabold, semibold, medium or regular faces `src: UI/UX notes, type paragraph`
- [ ] `C-UX-09` `ui` Cards float on a very soft shadow over gently rounded corners `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-10` `capability` The sticky top bar gains a soft shadow only once the page has scrolled `src: UI/UX notes, shape paragraph`
- [ ] `C-UX-11` `ui` Links carry an underline on hover or focus `src: UI/UX notes, components paragraph`
- [ ] `C-UX-12` `capability` Signing out asks for confirmation first `src: UI/UX notes, components paragraph`
- [ ] `C-UX-13` `ui` Feedback appears as an inline banner where the action happened `src: UI/UX notes, components paragraph`
- [ ] `C-UX-14` `capability` Outgoing bubbles sit on one side in the brand blue with incoming bubbles on the other side in a near-white neutral `src: UI/UX notes, components paragraph`
- [ ] `C-UX-15` `capability` Every interactive colour change uses one shared short transition `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-16` `ui` Only three utility animations exist: a spinner, a soft pulse, an indeterminate shimmer `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-17` `constraint` A reduced-motion preference stops every transition with every animation `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-18` `ui` Light mode is designed fully with dark only a readable courtesy layer `src: UI/UX notes, mode paragraph`
- [ ] `C-UX-19` `capability` On a narrow viewport the top bar links tuck behind a menu button `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-20` `capability` On a tablet the feature cards pair up two by two `src: UI/UX notes, responsive paragraph; Front-end specification, responsive tiers`
- [ ] `C-UX-21` `capability` On a laptop the hero puts the words left of the phones `src: UI/UX notes, responsive paragraph; Front-end specification, responsive tiers`
- [ ] `C-UX-22` `constraint` Nothing scrolls sideways at any width `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-23` `constraint` Body text meets the WCAG AA contrast bar on white, on the pale grey feature field or in the footer `src: UI/UX notes, accessibility floor; Front-end specification, accessibility values`
- [ ] `C-UX-24` `constraint` Under a dark preference body text still meets the WCAG AA contrast bar `src: UI/UX notes, accessibility floor; Front-end specification, accessibility values`
- [ ] `C-UX-25` `literal` Touch targets are at least `44` by `44` CSS pixels `src: Front-end specification, accessibility values; UI/UX notes, accessibility floor`
- [ ] `C-UX-26` `ui` Keyboard navigation reaches every control with a visible focus ring `src: UI/UX notes, accessibility floor`
- [ ] `C-UX-27` `capability` The wordmark, the globe control, the menu button with every icon-only control carry text alternatives `src: UI/UX notes, accessibility floor`
- [ ] `C-UX-28` `capability` Each `hero-phone` carries alternative text describing the drawing `src: UI/UX notes, accessibility floor; Front-end specification, home item 1`
- [ ] `C-UX-29` `capability` Feature card illustrations, band drawings, the details inside the phone screens are marked decorative `src: UI/UX notes, accessibility floor; Front-end specification, home item 4`
- [ ] `C-UX-30` `ui` Each page leads with one primary action: `Get Beacon` on the home, Donate on `/donate`, Send in a conversation `src: UI/UX notes, primary action`
- [ ] `C-UX-31` `ui` No page is dominated by a single hue family without a second signal `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-32` `ui` No decoration stands in for content `src: UI/UX notes, what it must not look like`
- [ ] `C-UX-33` `capability` The messenger carries no marketing composition `src: UI/UX notes, what it must not look like; UI/UX notes, north star`
- [ ] `C-UX-34` `constraint` The interactive blue meets the WCAG AA contrast bar `src: UI/UX notes, accessibility floor`
- [ ] `C-UX-35` `capability` Every document declares its language `src: UI/UX notes, accessibility floor`
- [ ] `C-UX-36` `ui` Keyboard navigation follows a logical order `src: UI/UX notes, accessibility floor`
- [ ] `C-UX-37` `capability` The vertical scrollbar is always present `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-38` `capability` A phone width shows a single column `src: UI/UX notes, responsive paragraph; Front-end specification, responsive tiers`
- [ ] `C-UX-39` `capability` On a phone the hero phones stack below the hero words `src: UI/UX notes, responsive paragraph; Front-end specification, home item 1`
- [ ] `C-UX-40` `capability` On a widescreen the container widens `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-41` `capability` On the widest screens the content stops stretching, centring with generous margins `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-42` `capability` Failure appears in one deep red used nowhere else `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-43` `capability` Success appears in one deep green `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-44` `capability` In-progress states use the mid cool neutral with the pulse `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-45` `capability` Muted secondary paragraphs use a deep cool neutral `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-46` `capability` Borders, dividers or unavailable states use the mid, light, near-white cool neutral scale `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-47` `ui` Alternating section grounds use three barely different near-white neutrals `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-48` `capability` Pressed states with gradient stops use two mid, vivid blues `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-49` `capability` Top bar links rest in the ink, moving to the interactive blue on hover or focus `src: UI/UX notes, palette paragraph; UI/UX notes, motion paragraph`
- [ ] `C-UX-50` `capability` A top bar link ground stays transparent through the colour transition `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-51` `capability` Feature cards add a matching fade with a slight lift `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-52` `capability` One gentle symmetric ease exists, used once on the attention pulse `src: UI/UX notes, motion paragraph`
- [ ] `C-UX-53` `capability` Figures align wherever amounts or times stack `src: UI/UX notes, type paragraph`
- [ ] `C-UX-54` `ui` Inter reads friendly with a neutral, never technical, voice `src: UI/UX notes, type paragraph`
- [ ] `C-UX-55` `capability` Captions such as message times use the dense body size `src: UI/UX notes, type paragraph`
- [ ] `C-UX-56` `ui` Buttons with the menu button round less than boxes `src: UI/UX notes, shape and density`
- [ ] `C-UX-57` `ui` Buttons carry a lighter shadow than cards `src: UI/UX notes, shape and density`
- [ ] `C-UX-58` `ui` Home sections read as separate at a glance without dividing lines `src: UI/UX notes, shape and density`
- [ ] `C-UX-59` `capability` A full screen of conversation fits without crowding `src: UI/UX notes, shape and density`
- [ ] `C-UX-60` `capability` Every control has resting, pointed-at, pressed, focused, unavailable states `src: UI/UX notes, components paragraph`
- [ ] `C-UX-61` `capability` An unavailable control is never signalled by colour alone `src: UI/UX notes, components paragraph`
- [ ] `C-UX-62` `capability` Every dialog closes on Escape, returning focus to the opener `src: UI/UX notes, components paragraph`
- [ ] `C-UX-63` `capability` Unlinking a device asks for confirmation first `src: UI/UX notes, components paragraph`
- [ ] `C-UX-64` `capability` Replacing every device asks for confirmation first `src: UI/UX notes, components paragraph`
- [ ] `C-UX-65` `capability` In-text links with the filled `Get Beacon` button use the brand blue `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-66` `capability` The periwinkle hero ground with drawing gradient stops are the only other blues `src: UI/UX notes, palette paragraph`
- [ ] `C-UX-67` `capability` On a tablet the top bar links sit inline `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-68` `capability` The menu button appears only on narrow viewports `src: Front-end specification, iconography`
- [ ] `C-UX-69` `capability` On a laptop the four feature cards sit in two rows `src: UI/UX notes, responsive paragraph`
- [ ] `C-UX-70` `capability` The filled `Get Beacon` button moves to the interactive blue on hover `src: UI/UX notes, palette paragraph`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` The service distributes public key material only, never holding a private key `src: Technical requirements, key material paragraph`
- [ ] `C-TR-02` `contract` The server runs Fastify on Node.js 20 with a Preact + Vite web client `src: Technical requirements, stack paragraph`
- [ ] `C-TR-03` `contract` Marketing routes arrive as build-time HTML, with messenger routes rendering in the browser against `/api` `src: Technical requirements, stack paragraph`
- [ ] `C-TR-04` `contract` Only the libraries in the library table plus direct dependencies are used `src: Technical requirements, libraries paragraph`
- [ ] `C-TR-05` `contract` The only backing services are PostgreSQL at `DATABASE_URL` or Mailpit at `SMTP_HOST` `src: Technical requirements, libraries paragraph`
- [ ] `C-TR-06` `contract` Hosts, ports or credentials come from the environment variables, never hardcoded `src: Technical requirements, environment paragraph`
- [ ] `C-TR-07` `literal` Mail goes from `Beacon <no-reply@beacon.example.org>` `src: Technical requirements, environment paragraph`
- [ ] `C-TR-08` `constraint` All cryptography comes from `libsodium-wrappers-sumo` or `@noble/post-quantum` `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-09` `capability` Session setup mixes in a post-quantum encapsulation against the recipient's post-quantum pre-key `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-10` `constraint` Every message type is sealed with authenticated encryption under a message key with a nonce used once `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-11` `capability` The sender identity travels inside the sealed envelope, proven to the recipient `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-12` `constraint` A removed group member cannot read anything sent afterwards `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-13` `constraint` Sync records between a person's own devices are encrypted to those devices `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-14` `constraint` Every wrong guess of the same kind receives the same refusal `src: Technical requirements, secrets paragraph`
- [ ] `C-TR-15` `capability` Cryptographic work in the web client runs in a Web Worker `src: Technical requirements, responsiveness paragraph`
- [ ] `C-TR-16` `capability` Typing in the composer never stalls as a backlog decrypts `src: Technical requirements, responsiveness paragraph`
- [ ] `C-TR-17` `capability` The Inter weights 400, 500, 600 with 800 are self-hosted with `font-display: swap` `src: Technical requirements, performance paragraph`
- [ ] `C-TR-18` `capability` Phone renders reserve their space before drawing `src: Technical requirements, performance paragraph`
- [ ] `C-TR-19` `literal` `fastify` with `@fastify/static` serve HTTP with static files `src: Technical requirements, library table`
- [ ] `C-TR-20` `literal` `pg` is the PostgreSQL client `src: Technical requirements, library table`
- [ ] `C-TR-21` `literal` `nodemailer` sends SMTP mail `src: Technical requirements, library table`
- [ ] `C-TR-22` `literal` `bcryptjs` hashes passwords `src: Technical requirements, library table`
- [ ] `C-TR-23` `literal` `preact`, `preact-iso`, `vite`, `preact-render-to-string` build the UI `src: Technical requirements, library table`
- [ ] `C-TR-24` `literal` `libsodium-wrappers-sumo` supplies X25519, Ed25519, XChaCha20-Poly1305, BLAKE2b, Argon2id `src: Technical requirements, library table`
- [ ] `C-TR-25` `literal` `@noble/post-quantum` supplies ML-KEM-768 key encapsulation `src: Technical requirements, library table`
- [ ] `C-TR-26` `literal` `idb` wraps browser storage `src: Technical requirements, library table`
- [ ] `C-TR-27` `literal` `@fontsource/inter` supplies the Inter font files `src: Technical requirements, library table`
- [ ] `C-TR-28` `literal` The app reads `DATABASE_URL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `APP_PUBLIC_URL`, `APP_PUBLIC_PORT` `src: Technical requirements, environment paragraph`
- [ ] `C-TR-29` `capability` Key agreement binds each party's identity key to the session `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-30` `capability` Key agreement mixes in the recipient's signed pre-key `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-31` `capability` Key agreement uses a one-time pre-key whenever one is available `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-32` `constraint` Compromising today's keys reveals nothing about earlier messages `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-33` `capability` Fresh key agreement heals a session after a compromise `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-34` `constraint` A captured message cannot be replayed into another conversation `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-35` `capability` Each group sender distributes a sender key over the pairwise sessions `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-36` `constraint` A membership change in a large group never stalls sending for other members `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-37` `constraint` Concurrent sync changes resolve the same way on every device `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-38` `constraint` No limit on Beacon needs to know who messages whom `src: Technical requirements, key material paragraph`
- [ ] `C-TR-39` `constraint` Token hashes, access keys, link codes, recovery verifiers compare in constant time `src: Technical requirements, secrets paragraph`
- [ ] `C-TR-40` `capability` Scrolling the conversation never stalls as a backlog decrypts `src: Technical requirements, responsiveness paragraph`
- [ ] `C-TR-41` `capability` Illustrations reserve their space before drawing `src: Technical requirements, performance paragraph`
- [ ] `C-TR-42` `capability` Large illustrations below the fold draw lazily `src: Technical requirements, performance paragraph`
- [ ] `C-TR-43` `constraint` A new group member never receives the sender key for earlier messages `src: Technical requirements, cryptography paragraph`
- [ ] `C-TR-44` `capability` Profile changes reach the user's own other devices through encrypted sync records `src: Technical requirements, cryptography paragraph`

## C-DM Data model

- [ ] `C-DM-01` `data` Gifts persist in `donations` with `amount_minor`, `currency`, `email` `src: Data model, donations table`
- [ ] `C-DM-02` `data` Envelope `server_timestamp` values are integer milliseconds since the epoch in UTC `src: Core features, feature 1 rule 5; Data model, opening paragraph`
- [ ] `C-DM-03` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: Data model, password paragraph`
- [ ] `C-DM-04` `data` Acknowledged guids are remembered without ciphertext `src: Data model, acknowledged_guids table`
- [ ] `C-DM-05` `constraint` Profile names with delivery states stay computed in the browser, never stored `src: Data model, derived paragraph`
- [ ] `C-DM-06` `constraint` No row in any table holds a readable message, attachment, profile name, contact list or sender `src: Data model, holds paragraph`
- [ ] `C-DM-07` `data` Seeded accounts start with no device `src: Data model, seed data`
- [ ] `C-DM-08` `constraint` Restarting the app duplicates no seeded account `src: Data model, seed data`
- [ ] `C-DM-09` `data` PostgreSQL holds the tables `accounts`, `devices`, `one_time_prekeys`, `link_codes`, `profiles`, `envelopes`, `acknowledged_guids`, `groups`, `group_members`, `recovery_records`, `donations` `src: Data model, opening paragraph`
- [ ] `C-DM-10` `data` `accounts` carries `email`, `username`, `password_hash`, `failed_sign_ins`, `locked_until` `src: Data model, accounts table`
- [ ] `C-DM-11` `data` `devices` carries `account_id`, `device_id`, `identity_key`, `token_hash`, `revoked_at` `src: Data model, devices table`
- [ ] `C-DM-12` `data` `one_time_prekeys` carries `device_ref`, `key_id`, `public_key`, `handed_out_at` `src: Data model, one_time_prekeys table`
- [ ] `C-DM-13` `data` `link_codes` carries a unique `code` with `used_at` `src: Data model, link_codes table`
- [ ] `C-DM-14` `data` `profiles` carries one row per account with `profile_ciphertext`, `access_key` `src: Data model, profiles table`
- [ ] `C-DM-15` `data` `envelopes` carries `recipient_device`, `guid`, `ciphertext`, `group_id`, `server_timestamp` `src: Data model, envelopes table`
- [ ] `C-DM-16` `data` `groups` carries `revision` with `encrypted_state` `src: Data model, groups table`
- [ ] `C-DM-17` `data` `group_members` carries a unique `group_id` with `account_id` pair plus `is_admin` `src: Data model, group_members table`
- [ ] `C-DM-18` `data` `recovery_records` carries `recovery_blob`, `access_verifier`, `failed_guesses` `src: Data model, recovery_records table`
- [ ] `C-DM-19` `data` Seeded accounts start with no profile, group or donation `src: Data model, seed data`
- [ ] `C-DM-20` `data` The delivered app holds the seeded accounts with no device, profile, recovery record, group, waiting envelope or sign-in lock `src: Data model, seed data`
- [ ] `C-DM-21` `literal` `/app/USER_README.md` carries one line per seeded account in the form `email: user@example.com password: deku-demo-pw-2026` `src: Data model, password paragraph`
- [ ] `C-DM-22` `literal` The tables live in the `public` schema `src: Data model, opening paragraph`
- [ ] `C-DM-23` `data` Every stored timestamp is UTC `src: Data model, opening paragraph`
- [ ] `C-DM-24` `constraint` Unread counts, previews, safety numbers stay computed in the browser, never stored `src: Data model, derived paragraph`
- [ ] `C-DM-25` `data` `devices` also carries `signed_prekey_id`, `signed_prekey_public`, `signed_prekey_signature`, `pq_prekey_id`, `pq_prekey_public`, `pq_prekey_signature`, `created_at` `src: Data model, devices table`
- [ ] `C-DM-26` `data` `accounts`, `groups`, `donations` carry `created_at`; `link_codes` carries `issued_by_device`; `donations` carries `idempotency_key` with `request_fingerprint` `src: Data model, accounts table; Data model, donations table`
- [ ] `C-DM-27` `data` `link_codes` carries `account_id`; `acknowledged_guids` carries a unique `recipient_device` with `guid` pair; `recovery_records` carries `account_id` `src: Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table`

## C-FE Front-end specification

- [ ] `C-FE-01` `literal` Body text uses the stack `Inter, SF Pro, Segoe UI, Roboto, Oxygen, Ubuntu, Helvetica Neue, Helvetica, Arial, sans-serif` `src: Front-end specification, type scale`
- [ ] `C-FE-02` `literal` The hero headline is `60px` at `800` with a `64px` line on a laptop, `28px` with a `32px` line on a phone `src: Front-end specification, type scale table`
- [ ] `C-FE-03` `capability` Section headings are 40px at 800 with a 44px line `src: Front-end specification, type scale table`
- [ ] `C-FE-04` `capability` Card titles are 20px at 600 with a 28px line `src: Front-end specification, type scale table`
- [ ] `C-FE-05` `capability` The lead paragraph is 20px at 400 with a 28px line `src: Front-end specification, type scale table`
- [ ] `C-FE-06` `literal` Buttons with strong labels are `16px` at `600` with a `22px` line `src: Front-end specification, type scale table`
- [ ] `C-FE-07` `literal` Body paragraphs are `16px` at `400` with a `24px` line `src: Front-end specification, type scale table`
- [ ] `C-FE-08` `literal` The sticky top bar carries the id `brandNavbar` `src: Front-end specification, global chrome`
- [ ] `C-FE-09` `capability` The top bar links read Get Beacon, Help, Blog, Developers, Careers, Donate in that order `src: Front-end specification, global chrome`
- [ ] `C-FE-10` `literal` The hero Get Beacon button carries the class `get-app` `src: Front-end specification, global chrome`
- [ ] `C-FE-11` `capability` The dark footer holds the `Organization`, `Download`, `Social`, `Help` link columns `src: Front-end specification, global chrome table`
- [ ] `C-FE-12` `ui` The language dialog is a centred card over a dimmed scrim with a pill-shaped close control `src: Front-end specification, global chrome`
- [ ] `C-FE-13` `ui` The menu button draws three thin rounded bars centred in a square tap target `src: Front-end specification, iconography`
- [ ] `C-FE-14` `ui` The globe draws a circle outline with curved meridians over latitude lines `src: Front-end specification, iconography`
- [ ] `C-FE-15` `ui` The wordmark sets Beacon in blue beside a speech-bubble ring with a small tail `src: Front-end specification, iconography`
- [ ] `C-FE-16` `capability` The hero shows the headline Speak Freely, the lead, the filled Get Beacon button beside two tilted phones `src: Front-end specification, home item 1`
- [ ] `C-FE-17` `capability` Each `hero-phone` element is tilted 22.5 degrees clockwise `src: Front-end specification, home item 1`
- [ ] `C-FE-18` `ui` One hero phone shows a group video call grid, the other chat bubbles with a voice waveform `src: Front-end specification, home item 1`
- [ ] `C-FE-19` `ui` The privacy statement sits beside a chat bubble drawing on a soft teal panel `src: Front-end specification, home item 3`
- [ ] `C-FE-20` `capability` Four feature cards read Say Anything, Speak Freely, Make Privacy Stick, Get Together with Groups `src: Front-end specification, home item 4`
- [ ] `C-FE-21` `ui` The four white feature cards rest on the pale grey field over flat vector illustrations `src: Front-end specification, home item 4`
- [ ] `C-FE-22` `capability` The home carries the No ads No trackers No kidding band with the Free for Everyone band `src: Front-end specification, home items 5 to 6`
- [ ] `C-FE-23` `ui` The no-tracking band shows a violet struck-through browser window `src: Front-end specification, home item 5`
- [ ] `C-FE-24` `ui` The nonprofit band shows a halftone globe wreathed in speech bubbles on pale teal `src: Front-end specification, home item 6`
- [ ] `C-FE-25` `capability` The Donate to Beacon button opens `/donate` `src: Front-end specification, home item 6`
- [ ] `C-FE-26` `literal` The utility animations are named `spinAround`, `pulsate`, `moveIndeterminate` `src: Front-end specification, motion names`
- [ ] `C-FE-27` `ui` Phone renders are dark rounded frames drawn from shapes with seeded gradient faces `src: Front-end specification, zero-asset substitution guide`
- [ ] `C-FE-28` `constraint` The home loads no raster image files `src: Front-end specification, zero-asset substitution guide`
- [ ] `C-FE-29` `capability` Every copy deck string appears on the English home `src: Front-end specification, copy deck`
- [ ] `C-FE-30` `constraint` The English home text carries no typographic dashes `src: Front-end specification, copy deck`
- [ ] `C-FE-31` `literal` Body text is `1em` at the regular `400` face with line height `1.5` under `optimizeLegibility` `src: Front-end specification, type scale`
- [ ] `C-FE-32` `literal` Inline code uses `Inconsolata, Hack, SF Mono, Roboto Mono, Source Code Pro, Ubuntu Mono, monospace` `src: Front-end specification, type scale`
- [ ] `C-FE-33` `literal` Sub-section headings are `28px` at `800` with a `32px` line `src: Front-end specification, type scale table`
- [ ] `C-FE-34` `literal` The large lead is `24px` at `400` with a `24px` line `src: Front-end specification, type scale table`
- [ ] `C-FE-35` `literal` Dense body text is `16px` at `400` with a `22px` line `src: Front-end specification, type scale table`
- [ ] `C-FE-36` `capability` The top bar has a white ground `src: Front-end specification, global chrome`
- [ ] `C-FE-37` `capability` The open language dialog sits above the top bar `src: Front-end specification, global chrome`
- [ ] `C-FE-38` `ui` The dialog header rounds top corners, the footer bottom corners, the card a hairline edge `src: Front-end specification, global chrome`
- [ ] `C-FE-39` `ui` The globe inherits the text colour, turning blue on hover with its label `src: Front-end specification, iconography`
- [ ] `C-FE-40` `ui` The menu button draws in the brand blue `src: Front-end specification, iconography`
- [ ] `C-FE-41` `literal` The wordmark sets Beacon in Inter `800` `src: Front-end specification, iconography`
- [ ] `C-FE-42` `capability` The home runs hero, why band, privacy statement, feature grid, no-tracking band, nonprofit band from top to bottom `src: Front-end specification, the home top to bottom`
- [ ] `C-FE-43` `capability` The `Why use Beacon?` heading is centred `src: Front-end specification, home item 2`
- [ ] `C-FE-44` `capability` The two hero phones overlap `src: Front-end specification, home item 1`
- [ ] `C-FE-45` `ui` The chat phone shows a disappearing-message timer `src: Front-end specification, home item 1`
- [ ] `C-FE-46` `ui` The privacy statement drawing shows a chat bubble carrying the pinned greeting `src: Front-end specification, home item 3`
- [ ] `C-FE-47` `capability` The `No ads. No trackers. No kidding.` heading is left-aligned `src: Front-end specification, home item 5`
- [ ] `C-FE-48` `ui` Each built-in sticker is drawn as a simple picture of its name `src: Front-end specification, zero-asset substitution guide`
- [ ] `C-FE-49` `literal` The responsive tiers break at `768`, `1023`, `1215`, `1407` CSS pixels `src: Front-end specification, responsive tiers`
- [ ] `C-FE-50` `literal` The body never narrows below `300` CSS pixels `src: Front-end specification, responsive tiers`
- [ ] `C-FE-51` `literal` Body text contrast is at least `4.5:1` in both colour preferences `src: Front-end specification, accessibility values`
- [ ] `C-FE-52` `literal` The language dialog lists `English`, `Afrikaans`, `العربية`, `Azərbaycan dili`, `Български`, `বাংলা`, `Bosanski`, `Català`, `Čeština`, `Dansk`, `Deutsch`, `Ελληνικά` `src: Core features, feature 12 rule 3; Front-end specification, global chrome`
- [ ] `C-FE-53` `literal` Every hook is a `data-testid` attribute carrying exactly the listed name `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-54` `capability` The `Donate to Beacon` button is an outline button `src: Front-end specification, home item 6`
- [ ] `C-FE-55` `capability` The footer carries the copyright, trademark, media lines on the left `src: Front-end specification, global chrome`
- [ ] `C-FE-56` `capability` The globe is a single unfilled stroke `src: Front-end specification, iconography`
- [ ] `C-FE-57` `literal` `spinAround` turns a full circle, `pulsate` dims to half opacity midway, `moveIndeterminate` slides a shimmer across `src: Front-end specification, motion names`
- [ ] `C-FE-58` `literal` The Organization column lists `Donate`, `Careers`, `Blog`, `Brand Assets`, `Terms & Privacy Policy` `src: Front-end specification, global chrome table`
- [ ] `C-FE-59` `literal` The Download column lists `Android`, `iPhone & iPad`, `Windows`, `Mac`, `Linux` `src: Front-end specification, global chrome table`
- [ ] `C-FE-60` `literal` The Social column lists `Bluesky`, `GitHub`, `Instagram`, `Mastodon`, `X` `src: Front-end specification, global chrome table`
- [ ] `C-FE-61` `literal` The Help column lists `Support Center`, `Community` `src: Front-end specification, global chrome table`
- [ ] `C-FE-62` `capability` The top bar shows the wordmark on the left, the links on the right, the language control after the links `src: Front-end specification, global chrome`
- [ ] `C-FE-63` `literal` The hook `language-control` marks the top bar's language button `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-64` `literal` The hook `language-dialog` marks the language dialog, with `role="dialog"`, `aria-modal="true"` `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-65` `literal` The hook `menu-button` marks the narrow-viewport menu button, with `aria-expanded` `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-66` `literal` The hook `hero-phone` marks each rotated phone render `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-67` `literal` The hook `feature-illustration` marks each feature card illustration `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-68` `literal` The hook `donate-amount` marks each preset amount button, carrying `data-amount-minor` (`500`, `1000`, `2500`, `5000`, `10000`) `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-69` `literal` The hook `donate-custom-amount` marks the custom amount field, in dollars `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-70` `literal` The hook `donate-email` marks the donor email field `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-71` `literal` The hook `donate-submit` marks the Donate button `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-72` `literal` The hook `donate-confirmation` marks the inline banner after a recorded gift `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-73` `literal` The hook `donate-error` marks the inline refusal naming the field `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-74` `literal` The hooks `signup-email`, `signup-username`, `signup-password`, `signup-submit` mark the sign-up form `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-75` `literal` The hooks `login-email`, `login-password`, `login-submit` mark the sign-in form `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-76` `literal` The hooks `unlock-password`, `unlock-submit` mark the unlock form `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-77` `literal` The hooks `link-code-input`, `link-code-submit` mark entering a link code on `/link` `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-78` `literal` The hooks `recovery-replace-pin`, `recovery-replace-submit`, `recovery-replace-confirm` mark replacing every device with the recovery PIN on `/link`, its confirmation `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-79` `literal` The hooks `new-chat`, `new-chat-username`, `new-chat-start` mark the new chat dialog `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-80` `literal` The hooks `new-group`, `new-group-name`, `new-group-members`, `new-group-create` mark the new group dialog, members are comma-separated usernames `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-81` `literal` The hook `conversation-row` marks each row on `/chats`, carrying `data-username` (or `data-group-id` for a group), `data-muted="true"` when the conversation is muted `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-82` `literal` The hook `unread-count` marks the unread number inside a row `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-83` `literal` The hook `conversation-title` marks the conversation header's name: the contact's profile name once known, else the username `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-84` `literal` The hooks `conversation-archive`, `conversation-mute` mark the header's archive, mute controls `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-85` `literal` The hook `message-bubble` marks each message, carrying `data-direction` of `in` or `out` `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-86` `literal` The hook `message-text` marks the text inside a bubble `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-87` `literal` The hook `message-status` marks an outgoing bubble's state text: `Sending`, `Sent`, `Delivered` or `Read` `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-88` `literal` The hooks `message-edit`, `message-edit-input`, `message-edit-save` mark editing an outgoing message, `message-edit` sits inside its `message-bubble`, may appear when the bubble is pointed at `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-89` `literal` The hooks `message-delete`, `message-delete-confirm` mark deleting an outgoing message, its confirmation, `message-delete` sits inside its `message-bubble`, may appear when the bubble is pointed at `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-90` `literal` The hooks `message-image`, `message-video`, `message-file`, `message-voice`, `message-sticker` mark an attachment inside a bubble, `message-file` shows the file name, `message-sticker` carries the sticker's name as its accessible name `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-91` `literal` The hook `decrypt-error-notice` marks the notice on `/chats` reading the pinned text `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-92` `literal` The hooks `composer-input`, `composer-send` mark the composer text field, Send button `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-93` `literal` The hook `composer-attach` marks the file input for photos, video, files `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-94` `literal` The hook `composer-voice` marks start, then stop, send, a voice message `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-95` `literal` The hooks `composer-sticker`, `sticker-option` mark the sticker picker, each built-in sticker, whose accessible name is the sticker's name `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-96` `literal` The hooks `call-voice`, `call-video`, `call-screen`, `call-hang-up` mark call controls, the call screen `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-97` `literal` The hooks `call-incoming`, `call-answer`, `call-decline` mark the incoming call shown to the person being called `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-98` `literal` The hooks `safety-number-link`, `safety-number` mark the link to, the display of the safety number, as twelve groups of five digits separated by spaces `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-99` `literal` The hooks `identity-change-banner`, `identity-change-accept` mark the changed-identity warning, its accept control `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-100` `literal` The hook `disappearing-timer` marks the timer select, with option values `off`, `30s`, `5m`, `1h`, `1d`, `1w` `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-101` `literal` The hook `group-members` marks the member list in a group conversation `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-102` `literal` The hooks `profile-name-input`, `profile-save` mark the profile form `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-103` `literal` The hooks `device-row`, `link-code-create`, `link-code-value`, `device-unlink`, `device-unlink-confirm`, `sign-out`, `sign-out-confirm` mark the devices page, each `device-row` carries `data-device-id`, holds its own `device-unlink`, unlinking asks for confirmation first `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-104` `literal` The hooks `recovery-pin-input`, `recovery-save` mark the recovery form `src: Front-end specification, machine-readable hooks`
- [ ] `C-FE-105` `capability` The English home renders every copy deck string of the top bar links line exactly `src: Front-end specification, copy deck line 1`
- [ ] `C-FE-106` `capability` The English home renders every copy deck string of the hero headline line exactly `src: Front-end specification, copy deck line 2`
- [ ] `C-FE-107` `capability` The English home renders every copy deck string of the why band heading line exactly `src: Front-end specification, copy deck line 3`
- [ ] `C-FE-108` `capability` The English home renders every copy deck string of the privacy statement heading line exactly `src: Front-end specification, copy deck line 4`
- [ ] `C-FE-109` `capability` The English home renders every copy deck string of the card say anything line exactly `src: Front-end specification, copy deck line 5`
- [ ] `C-FE-110` `capability` The English home renders every copy deck string of the card speak freely line exactly `src: Front-end specification, copy deck line 6`
- [ ] `C-FE-111` `capability` The English home renders every copy deck string of the card make privacy stick line exactly `src: Front-end specification, copy deck line 7`
- [ ] `C-FE-112` `capability` The English home renders every copy deck string of the card get together with groups line exactly `src: Front-end specification, copy deck line 8`
- [ ] `C-FE-113` `capability` The English home renders every copy deck string of the no-tracking heading line exactly `src: Front-end specification, copy deck line 9`
- [ ] `C-FE-114` `capability` The English home renders every copy deck string of the nonprofit heading line exactly `src: Front-end specification, copy deck line 10`
- [ ] `C-FE-115` `capability` The English home renders every copy deck string of the footer copyright line exactly `src: Front-end specification, copy deck line 11`
- [ ] `C-FE-116` `capability` The `/terms` privacy table Accounts row carries its holds with never-holds cells word for word `src: Front-end specification, privacy table; Core features, feature 12 rule 6`
- [ ] `C-FE-117` `capability` The `/terms` privacy table Messages row carries its holds with never-holds cells word for word `src: Front-end specification, privacy table; Core features, feature 12 rule 6`
- [ ] `C-FE-118` `capability` The `/terms` privacy table Groups row carries its holds with never-holds cells word for word `src: Front-end specification, privacy table; Core features, feature 12 rule 6`
- [ ] `C-FE-119` `capability` The `/terms` privacy table Delivery row carries its holds with never-holds cells word for word `src: Front-end specification, privacy table; Core features, feature 12 rule 6`
- [ ] `C-FE-120` `capability` The `/terms` privacy table Recovery row carries its holds with never-holds cells word for word `src: Front-end specification, privacy table; Core features, feature 12 rule 6`
- [ ] `C-FE-121` `capability` The `/terms` privacy table Donations row carries its holds with never-holds cells word for word `src: Front-end specification, privacy table; Core features, feature 12 rule 6`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Every account is a peer with no tenancy `src: Constraints, item 1`
- [ ] `C-CN-02` `constraint` No native Android, iPhone, iPad, Windows, Mac or Linux app ships in the build `src: Constraints, item 2`
- [ ] `C-CN-03` `constraint` No address-book upload exists `src: Constraints, item 3`
- [ ] `C-CN-04` `constraint` No password reset exists `src: Constraints, item 4`
- [ ] `C-CN-05` `constraint` No sticker pack editor exists `src: Constraints, item 7`
- [ ] `C-CN-06` `constraint` No group invite links exist `src: Constraints, item 8`
- [ ] `C-CN-07` `constraint` No language beyond English with the eleven named translations is offered `src: Constraints, item 9`
- [ ] `C-CN-08` `constraint` The help, blog, developers, careers, brand pages hold only a heading with a short paragraph `src: Constraints, item 10`
- [ ] `C-CN-09` `constraint` No analytics, tracking pixel, third-party font or third-party script loads `src: Constraints, item 11`
- [ ] `C-CN-10` `capability` The app stays responsive with 1000 waiting envelopes on a device `src: Constraints, item 14`
- [ ] `C-CN-11` `constraint` No call relay carries call media `src: Constraints, item 6`
- [ ] `C-CN-12` `constraint` No external network call happens at runtime `src: Constraints, item 12`
- [ ] `C-CN-13` `capability` The app stays responsive with a conversation of several thousand messages `src: Constraints, item 14`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` on the mapped port `src: Deployment contract, item 1`
- [ ] `C-DC-02` `contract` The HTTP API is served on the same origin under `/api` `src: Deployment contract, item 2`
- [ ] `C-DC-03` `contract` `GET /api/health` returns 200 once the app is ready `src: Deployment contract, item 3`
- [ ] `C-DC-04` `contract` The app starts from the environment image with no manual steps `src: Deployment contract, item 4`
- [ ] `C-DC-05` `contract` Login credentials are written to `/app/USER_README.md` `src: Deployment contract, item 5`
- [ ] `C-DC-06` `contract` Empty `.browser_screenshots/` with `.downloads/` directories exist at the app root `src: Deployment contract, item 6`
- [ ] `C-DC-07` `contract` A production build is served, never a dev server `src: Deployment contract, item 7`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends `src: Deployment contract, item 8`
- [ ] `C-DC-09` `contract` The server binds `0.0.0.0` `src: Deployment contract, item 9`
- [ ] `C-DC-10` `contract` The already running backing services are used, never installed or started `src: Deployment contract, item 10`
- [ ] `C-DC-11` `contract` No persistent volumes, fixed container names or custom networks are used `src: Deployment contract, item 12`
- [ ] `C-DC-12` `contract` Every refusal is a client error, never a `5xx` `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-13` `data` List endpoints return a top-level JSON array `src: Deployment contract, API shapes paragraph`
- [ ] `C-DC-14` `data` Group `members` with `admins` list usernames in ascending order `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-15` `contract` PostgreSQL with Mailpit hold the real data, never an in-memory stand-in `src: Deployment contract, no mocks`
- [ ] `C-DC-16` `literal` The container serves on port `4173`, mapped from `APP_PUBLIC_PORT` `src: Deployment contract, item 1`
- [ ] `C-DC-17` `contract` Only the providers named in the brief are used `src: Deployment contract, item 11`
- [ ] `C-DC-18` `contract` No edge functions are used `src: Deployment contract, item 11`
- [ ] `C-DC-19` `data` `POST /api/auth/signup` returns `username` `src: Deployment contract, API shapes`
- [ ] `C-DC-20` `data` An accepted send returns `accepted` set to `true` `src: Deployment contract, API shapes`
- [ ] `C-DC-21` `data` Group creation with group changes return `group_id`, `revision`, `members`, `admins` `src: Deployment contract, API shapes`
- [ ] `C-DC-22` `data` `GET /api/groups/{group_id}` adds `encrypted_state` to the group fields `src: Deployment contract, API shapes`
- [ ] `C-DC-23` `data` `GET /api/devices` returns `device_id` entries in ascending order `src: Deployment contract, API shapes`
- [ ] `C-DC-24` `data` `POST /api/keys/one-time` with `GET /api/keys/count` return `one_time_prekeys` as the remaining count `src: Deployment contract, API shapes`
- [ ] `C-DC-25` `data` Bundle devices carry `device_id`, `identity_key`, `signed_prekey`, `pq_prekey`, `one_time_prekey` in ascending device order `src: Deployment contract, API shapes`
- [ ] `C-DC-26` `data` `POST /api/devices` takes `identity_key`, `signed_prekey`, `pq_prekey`, `one_time_prekeys` with optional `link_code`, `replace_existing`, `access_verifier` `src: Deployment contract, API shapes`
- [ ] `C-DC-27` `data` A send body is `messages` holding `device_id`, `guid`, `ciphertext` entries `src: Deployment contract, API shapes; Core features, feature 1 rule 3`
- [ ] `C-DC-28` `literal` `DELETE /api/devices/{device_id}` unlinks a device `src: Deployment contract, API shapes`
- [ ] `C-DC-29` `data` `identity_key` decodes to 32 bytes `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-30` `data` `signed_prekey.public_key` decodes to 32 bytes beside a 64-byte `signature` `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-31` `data` `pq_prekey.public_key` decodes to 1184 bytes beside a 64-byte `signature` `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-32` `data` Each one-time `public_key` decodes to 32 bytes `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-33` `data` `access_key` decodes to 16 bytes `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-34` `data` `access_verifier` decodes to 32 bytes `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-35` `data` `profile_ciphertext`, `encrypted_state`, `recovery_blob` each decode to 1 to 65536 bytes `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-36` `literal` Every `key_id` is an integer from `1` to `16777215` `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-37` `constraint` A `key_id` repeated within one upload is rejected `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-38` `literal` Sends use `PUT /api/messages/{username}` `src: Deployment contract, API shapes`
- [ ] `C-DC-39` `literal` Group changes use `PATCH /api/groups/{group_id}` with `expected_revision`, `encrypted_state`, `add`, `remove` `src: Deployment contract, API shapes`
- [ ] `C-DC-40` `literal` Group sends use `PUT /api/groups/{group_id}/messages` with `guid`, `ciphertext` `src: Deployment contract, API shapes`
- [ ] `C-DC-41` `literal` `POST /api/devices/link-codes` returns `code` `src: Deployment contract, API shapes`
- [ ] `C-DC-42` `literal` Device calls carry `Authorization: Bearer <device_token>`, account calls `Authorization: Bearer <access_token>` `src: Deployment contract, API shapes`
- [ ] `C-DC-43` `constraint` A request body outside the stated shapes is rejected, storing nothing `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-44` `constraint` Signed, post-quantum, one-time pre-keys each keep their own `key_id` space `src: Deployment contract, key sizes paragraph`
- [ ] `C-DC-45` `literal` `POST /api/groups` takes `encrypted_state` with `members` usernames `src: Deployment contract, API shapes; Core features, feature 6 rule 1`
- [ ] `C-DC-46` `literal` `POST /api/recovery/restore` returns `recovery_blob` for the right verifier `src: Deployment contract, API shapes`
- [ ] `C-DC-47` `literal` `POST /api/auth/signup` takes `email`, `username`, `password` `src: Deployment contract, API shapes`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `/signup` | Signup at /signup is open to anyone | C-RL-06 | User roles, signup paragraph |
| `user@example.com` | The seeded account user@example.com carries the username nova | C-RL-07 | User roles, seeded accounts table row 1 |
| `nova` | The seeded account user@example.com carries the username nova | C-RL-07 | User roles, seeded accounts table row 1 |
| `user2@example.com` | The seeded account user2@example.com carries the username juniper | C-RL-08 | User roles, seeded accounts table row 2 |
| `juniper` | The seeded account user2@example.com carries the username juniper | C-RL-08 | User roles, seeded accounts table row 2 |
| `user3@example.com` | The seeded account user3@example.com carries the username sol | C-RL-09 | User roles, seeded accounts table row 3 |
| `sol` | The seeded account user3@example.com carries the username sol | C-RL-09 | User roles, seeded accounts table row 3 |
| `user4@example.com` | The seeded account user4@example.com carries the username wren | C-RL-10 | User roles, seeded accounts table row 4 |
| `wren` | The seeded account user4@example.com carries the username wren | C-RL-10 | User roles, seeded accounts table row 4 |
| `/` | A visitor with no account reads /, the eleven translations, the declared pages with /terms | C-RL-11 | User roles table row 1; User flow, route table |
| `/terms` | A visitor with no account reads /, the eleven translations, the declared pages with /terms | C-RL-11 | User roles table row 1; User flow, route table |
| `POST /api/donations` | A visitor with no account gives a donation through POST /api/donations | C-RL-12 | User roles table row 1 |
| `Unidentified-Access-Key` | A one-to-one send to another person carries the Unidentified-Access-Key header with no ... | C-CF-02 | Core features, feature 1 rule 1 |
| `Authorization` | A one-to-one send to another person carries the Unidentified-Access-Key header with no ... | C-CF-02 | Core features, feature 1 rule 1 |
| `missing_devices` | A send leaving out an active device is rejected with missing_devices naming the device id | C-CF-06 | Core features, feature 1 rule 3 |
| `extra_devices` | A send naming a device outside the active set is rejected with extra_devices naming ... | C-CF-08 | Core features, feature 1 rule 3 |
| `GET /api/messages` | GET /api/messages returns only the envelopes waiting for the calling device, oldest first | C-CF-11 | Core features, feature 1 rule 4 |
| `guid` | An envelope carries exactly the fields guid, ciphertext, server_timestamp, group_id | C-CF-14 | Core features, feature 1 rule 5 |
| `ciphertext` | An envelope carries exactly the fields guid, ciphertext, server_timestamp, group_id | C-CF-14 | Core features, feature 1 rule 5 |
| `server_timestamp` | An envelope carries exactly the fields guid, ciphertext, server_timestamp, group_id | C-CF-14 | Core features, feature 1 rule 5 |
| `group_id` | An envelope carries exactly the fields guid, ciphertext, server_timestamp, group_id | C-CF-14 | Core features, feature 1 rule 5 |
| `DELETE /api/messages/{guid}` | DELETE /api/messages/{guid} deletes the envelope ciphertext from the database outright | C-CF-16 | Core features, feature 1 rule 6 |
| `You have something waiting on Beacon` | The nudge subject is You have something waiting on Beacon | C-CF-26 | Core features, feature 2 rule 2 |
| `Open Beacon to read what is waiting for you.` | The nudge body is Open Beacon to read what is waiting for you. | C-CF-27 | Core features, feature 2 rule 2 |
| `POST /api/auth/signup` | POST /api/auth/signup creates an account from an email, a username with a password | C-CF-33 | Core features, feature 3 rule 1 |
| `^[a-z][a-z0-9_]{2,19}$` | A username outside ^[a-z][a-z0-9_]{2,19}$ is rejected with nothing stored | C-CF-34 | Core features, feature 3 rule 1 |
| `POST /api/auth/login` | POST /api/auth/login returns an access_token | C-CF-39 | Core features, feature 3 rule 3 |
| `access_token` | POST /api/auth/login returns an access_token | C-CF-39 | Core features, feature 3 rule 3 |
| `POST /api/devices` | An account token is accepted only by POST /api/devices, POST /api/recovery/restore, ... | C-CF-42 | Core features, feature 3 rule 4 |
| `POST /api/recovery/restore` | An account token is accepted only by POST /api/devices, POST /api/recovery/restore, ... | C-CF-42 | Core features, feature 3 rule 4 |
| `GET /api/me` | An account token is accepted only by POST /api/devices, POST /api/recovery/restore, ... | C-CF-42 | Core features, feature 3 rule 4 |
| `POST /api/devices` | POST /api/devices returns a device_id beside a device_token | C-CF-43 | Core features, feature 4 rule 1 |
| `device_id` | POST /api/devices returns a device_id beside a device_token | C-CF-43 | Core features, feature 4 rule 1 |
| `device_token` | POST /api/devices returns a device_id beside a device_token | C-CF-43 | Core features, feature 4 rule 1 |
| `POST /api/devices/link-codes` | POST /api/devices/link-codes issues an eight-character code of capital letters or digits | C-CF-48 | Core features, feature 4 rule 3 |
| `replace_existing` | Registration with replace_existing plus the right recovery access_verifier revokes ... | C-CF-51 | Core features, feature 4 rule 4 |
| `access_verifier` | Registration with replace_existing plus the right recovery access_verifier revokes ... | C-CF-51 | Core features, feature 4 rule 4 |
| `GET /api/devices` | GET /api/devices lists the account's active devices | C-CF-54 | Core features, feature 4 rule 5 |
| `extra_devices` | A send naming an unlinked device is rejected with that device id in extra_devices | C-CF-58 | Core features, feature 4 rule 5 |
| `GET /api/keys/{username}` | GET /api/keys/{username} returns the access key with one bundle per active device | C-CF-64 | Core features, feature 5 rule 2 |
| `one_time_prekey` | A device with no one-time pre-keys left still returns a bundle with one_time_prekey null | C-CF-66 | Core features, feature 5 rule 2 |
| `access_key` | An account that never published a profile returns access_key null | C-CF-67 | Core features, feature 5 rule 2 |
| `devices` | An account with no active device returns devices as an empty list | C-CF-68 | Core features, feature 5 rule 2 |
| `POST /api/keys/one-time` | POST /api/keys/one-time adds one-time pre-keys | C-CF-69 | Core features, feature 5 rule 3 |
| `GET /api/keys/count` | GET /api/keys/count returns the calling device's remaining one-time pre-keys | C-CF-70 | Core features, feature 5 rule 3 |
| `GET /api/keys/{username}` | A device making more than 300 GET /api/keys/{username} requests in a rolling sixty ... | C-CF-72 | Core features, feature 5 rule 4 |
| `POST /api/groups` | POST /api/groups makes the creator the only admin at revision 1 | C-CF-74 | Core features, feature 6 rule 1 |
| `expected_revision` | A group change carrying the current expected_revision raises the revision by one | C-CF-77 | Core features, feature 6 rule 2 |
| `revision` | The losing group change returns the current revision with nothing changed | C-CF-79 | Core features, feature 6 rule 2 |
| `GET /api/groups/{group_id}` | GET /api/groups/{group_id} returns one roster to every member | C-CF-86 | Core features, feature 6 rule 5 |
| `/link` | Sign-in for an account whose devices are elsewhere lands on /link offering a link code ... | C-CF-90 | Core features, feature 7 rule 1; User flow, entry and redirects |
| `/chats` | Registering a device in the browser publishes the encrypted profile with the access ... | C-CF-91 | Core features, feature 7 rule 2 |
| `/unlock` | A reload or new tab asks for the account password at /unlock before showing stored ... | C-CF-92 | Core features, feature 7 rule 3 |
| `/chats` | Each /chats row previews the last message | C-CF-93 | Core features, feature 7 rule 4 |
| `/chats` | Each /chats row shows the number of unread messages | C-CF-94 | Core features, feature 7 rule 4 |
| `New chat` | The New chat dialog starts a conversation with an exact username | C-CF-96 | Core features, feature 7 rule 4 |
| `New group` | The New group dialog creates a group from a name with usernames | C-CF-97 | Core features, feature 7 rule 4 |
| `Sending` | An outgoing bubble shows one of Sending, Sent, Delivered, Read | C-CF-99 | Core features, feature 7 rule 5 |
| `Sent` | An outgoing bubble shows one of Sending, Sent, Delivered, Read | C-CF-99 | Core features, feature 7 rule 5 |
| `Delivered` | An outgoing bubble shows one of Sending, Sent, Delivered, Read | C-CF-99 | Core features, feature 7 rule 5 |
| `Read` | An outgoing bubble shows one of Sending, Sent, Delivered, Read | C-CF-99 | Core features, feature 7 rule 5 |
| `/chats` | Archiving a conversation removes the conversation row from /chats on every linked ... | C-CF-110 | Core features, feature 7 rule 8 |
| `/settings/profile` | A profile name set at /settings/profile appears in a contact's conversation header | C-CF-116 | Core features, feature 7 rule 10 |
| `profile_ciphertext` | The profile name reaches the service only as profile_ciphertext | C-CF-117 | Core features, feature 7 rule 10 |
| `/settings/devices` | /settings/devices lists linked devices | C-CF-118 | Core features, feature 7 rule 11 |
| `/settings/devices` | /settings/devices issues a link code | C-CF-119 | Core features, feature 7 rule 11 |
| `/settings/devices` | Signing out from /settings/devices returns the browser to /login | C-CF-120 | Core features, feature 7 rule 11 |
| `/login` | Signing out from /settings/devices returns the browser to /login | C-CF-120 | Core features, feature 7 rule 11 |
| `/settings/recovery` | /settings/recovery saves a PIN of six or more digits, confirming Recovery PIN saved | C-CF-121 | Core features, feature 7 rule 12 |
| `Recovery PIN saved` | /settings/recovery saves a PIN of six or more digits, confirming Recovery PIN saved | C-CF-121 | Core features, feature 7 rule 12 |
| `POST /api/recovery/restore` | POST /api/recovery/restore returns the recovery record for the right verifier | C-CF-122 | Core features, feature 7 rule 12 |
| `remaining_guesses` | A wrong verifier is refused with remaining_guesses | C-CF-123 | Core features, feature 7 rule 12 |
| `/chats` | A dropped tampered message shows the pinned decrypt notice on /chats | C-CF-128 | Core features, feature 8 rule 1 |
| `A message could not be verified and was not shown` | A dropped tampered message shows the pinned decrypt notice on /chats | C-CF-128 | Core features, feature 8 rule 1 |
| `/donate` | The /donate amounts are $5, $10, $25, $50, $100 beside a custom dollar amount | C-CF-142 | Core features, feature 11 rule 1 |
| `$5` | The /donate amounts are $5, $10, $25, $50, $100 beside a custom dollar amount | C-CF-142 | Core features, feature 11 rule 1 |
| `$10` | The /donate amounts are $5, $10, $25, $50, $100 beside a custom dollar amount | C-CF-142 | Core features, feature 11 rule 1 |
| `$25` | The /donate amounts are $5, $10, $25, $50, $100 beside a custom dollar amount | C-CF-142 | Core features, feature 11 rule 1 |
| `$50` | The /donate amounts are $5, $10, $25, $50, $100 beside a custom dollar amount | C-CF-142 | Core features, feature 11 rule 1 |
| `$100` | The /donate amounts are $5, $10, $25, $50, $100 beside a custom dollar amount | C-CF-142 | Core features, feature 11 rule 1 |
| `Thank you. Your gift of $25.00 was received.` | A recorded gift shows the inline banner Thank you. Your gift of $25.00 was received. ... | C-CF-144 | Core features, feature 11 rule 1 |
| `$25.00` | A recorded gift shows the inline banner Thank you. Your gift of $25.00 was received. ... | C-CF-144 | Core features, feature 11 rule 1 |
| `POST /api/donations` | POST /api/donations returns amount_minor, currency with status set to received | C-CF-145 | Core features, feature 11 rule 2 |
| `amount_minor` | POST /api/donations returns amount_minor, currency with status set to received | C-CF-145 | Core features, feature 11 rule 2 |
| `currency` | POST /api/donations returns amount_minor, currency with status set to received | C-CF-145 | Core features, feature 11 rule 2 |
| `status` | POST /api/donations returns amount_minor, currency with status set to received | C-CF-145 | Core features, feature 11 rule 2 |
| `amount_minor` | amount_minor is an integer from 100 to 1000000 | C-CF-146 | Core features, feature 11 rule 2 |
| `currency` | currency is exactly usd | C-CF-147 | Core features, feature 11 rule 2 |
| `usd` | currency is exactly usd | C-CF-147 | Core features, feature 11 rule 2 |
| `Idempotency-Key` | A donation without an Idempotency-Key header is rejected | C-CF-148 | Core features, feature 11 rule 3 |
| `Idempotency-Key` | Repeating an Idempotency-Key with the same body stores nothing new | C-CF-151 | Core features, feature 11 rule 4 |
| `Idempotency-Key` | Simultaneous repeats of one Idempotency-Key record one gift | C-CF-152 | Core features, feature 11 rule 4 |
| `Idempotency-Key` | One Idempotency-Key sent with a different body is rejected | C-CF-153 | Core features, feature 11 rule 4 |
| `Thank you for supporting Beacon` | The receipt subject is Thank you for supporting Beacon | C-CF-155 | Core features, feature 11 rule 5 |
| `/` | The HTML served for / already carries Speak Freely, the lead, the Get Beacon button ... | C-CF-157 | Core features, feature 12 rule 1 |
| `Speak Freely` | The HTML served for / already carries Speak Freely, the lead, the Get Beacon button ... | C-CF-157 | Core features, feature 12 rule 1 |
| `Get Beacon` | The HTML served for / already carries Speak Freely, the lead, the Get Beacon button ... | C-CF-157 | Core features, feature 12 rule 1 |
| `lang="en"` | The English home root element declares lang="en" | C-CF-158 | Core features, feature 12 rule 1 |
| `/ar` | The /ar document declares dir="rtl" | C-CF-162 | Core features, feature 12 rule 2 |
| `dir="rtl"` | The /ar document declares dir="rtl" | C-CF-162 | Core features, feature 12 rule 2 |
| `Select your language` | The language control opens the dialog Select your language listing twelve language names | C-CF-164 | Core features, feature 12 rule 3 |
| `/get` | /get offers Android, iPhone or iPad store listings beside Windows, Mac or Linux downloads | C-CF-169 | Core features, feature 12 rule 5 |
| `/terms` | Every listed marketing page footer links to /terms, reading Terms & Privacy Policy on ... | C-CF-170 | Core features, feature 12 rule 6 |
| `Terms & Privacy Policy` | Every listed marketing page footer links to /terms, reading Terms & Privacy Policy on ... | C-CF-170 | Core features, feature 12 rule 6 |
| `/terms` | The /terms privacy page carries the privacy table word for word | C-CF-171 | Core features, feature 12 rule 6 |
| `/sitemap.xml` | /sitemap.xml lists exactly the twenty public routes as absolute addresses built from ... | C-CF-172 | Core features, feature 12 rule 7 |
| `APP_PUBLIC_URL` | /sitemap.xml lists exactly the twenty public routes as absolute addresses built from ... | C-CF-172 | Core features, feature 12 rule 7 |
| `/robots.txt` | /robots.txt carries a Sitemap: line pointing at the sitemap | C-CF-173 | Core features, feature 12 rule 7 |
| `Sitemap:` | /robots.txt carries a Sitemap: line pointing at the sitemap | C-CF-173 | Core features, feature 12 rule 7 |
| `GET /api/me` | GET /api/me returns username with email | C-CF-174 | Core features, feature 3 rule 4; Deployment contract, API shapes |
| `username` | GET /api/me returns username with email | C-CF-174 | Core features, feature 3 rule 4; Deployment contract, API shapes |
| `email` | GET /api/me returns username with email | C-CF-174 | Core features, feature 3 rule 4; Deployment contract, API shapes |
| `GET /api/me` | GET /api/me accepts an account token or a device token | C-CF-175 | Core features, feature 3 rule 4 |
| `encrypted_state` | A leaving member carries the current encrypted_state unchanged, a different state ... | C-CF-180 | Core features, feature 6 rule 3 |
| `PUT /api/profile` | PUT /api/profile stores profile_ciphertext beside access_key | C-CF-185 | Core features, feature 7 rule 2 |
| `profile_ciphertext` | PUT /api/profile stores profile_ciphertext beside access_key | C-CF-185 | Core features, feature 7 rule 2 |
| `access_key` | PUT /api/profile stores profile_ciphertext beside access_key | C-CF-185 | Core features, feature 7 rule 2 |
| `/link` | Replacing every device with the recovery PIN on /link lands on /chats with the ... | C-CF-186 | Core features, feature 7 rule 2 |
| `/chats` | Replacing every device with the recovery PIN on /link lands on /chats with the ... | C-CF-186 | Core features, feature 7 rule 2 |
| `/unlock` | Unlocking at /unlock returns to the route first asked for | C-CF-187 | Core features, feature 7 rule 3 |
| `New chat` | A New chat username with no account shows an inline banner in the dialog, opening no ... | C-CF-188 | Core features, feature 7 rule 4 |
| `Sent` | An outgoing bubble reads Sent once the service accepts the message | C-CF-189 | Core features, feature 7 rule 5 |
| `Delivered` | An outgoing bubble reads Delivered once a recipient device decrypts the message | C-CF-190 | Core features, feature 7 rule 5 |
| `Read` | An outgoing bubble reads Read once a recipient screen shows the message | C-CF-191 | Core features, feature 7 rule 5 |
| `Wave` | The built-in sticker pack holds six stickers: Wave, Heart, Thumbs Up, Laugh, Party, ... | C-CF-195 | Core features, feature 7 rule 7; Front-end specification, machine-readable hooks |
| `Heart` | The built-in sticker pack holds six stickers: Wave, Heart, Thumbs Up, Laugh, Party, ... | C-CF-195 | Core features, feature 7 rule 7; Front-end specification, machine-readable hooks |
| `Thumbs Up` | The built-in sticker pack holds six stickers: Wave, Heart, Thumbs Up, Laugh, Party, ... | C-CF-195 | Core features, feature 7 rule 7; Front-end specification, machine-readable hooks |
| `Laugh` | The built-in sticker pack holds six stickers: Wave, Heart, Thumbs Up, Laugh, Party, ... | C-CF-195 | Core features, feature 7 rule 7; Front-end specification, machine-readable hooks |
| `Party` | The built-in sticker pack holds six stickers: Wave, Heart, Thumbs Up, Laugh, Party, ... | C-CF-195 | Core features, feature 7 rule 7; Front-end specification, machine-readable hooks |
| `Beacon Light` | The built-in sticker pack holds six stickers: Wave, Heart, Thumbs Up, Laugh, Party, ... | C-CF-195 | Core features, feature 7 rule 7; Front-end specification, machine-readable hooks |
| `data-muted` | Muting marks the conversation row with data-muted set to true | C-CF-196 | Core features, feature 7 rule 8 |
| `true` | Muting marks the conversation row with data-muted set to true | C-CF-196 | Core features, feature 7 rule 8 |
| `GET /api/profile/{username}` | GET /api/profile/{username} returns the account's profile_ciphertext to a device | C-CF-201 | Core features, feature 7 rule 10 |
| `profile_ciphertext` | GET /api/profile/{username} returns the account's profile_ciphertext to a device | C-CF-201 | Core features, feature 7 rule 10 |
| `/settings/devices` | /settings/devices unlinks a linked device | C-CF-202 | Core features, feature 7 rule 11 |
| `PUT /api/recovery` | PUT /api/recovery stores recovery_blob beside access_verifier | C-CF-205 | Core features, feature 7 rule 12 |
| `recovery_blob` | PUT /api/recovery stores recovery_blob beside access_verifier | C-CF-205 | Core features, feature 7 rule 12 |
| `access_verifier` | PUT /api/recovery stores recovery_blob beside access_verifier | C-CF-205 | Core features, feature 7 rule 12 |
| `Idempotency-Key` | An Idempotency-Key outside 8 to 64 letters, digits, _ or - is rejected | C-CF-211 | Core features, feature 11 rule 2 |
| `_` | An Idempotency-Key outside 8 to 64 letters, digits, _ or - is rejected | C-CF-211 | Core features, feature 11 rule 2 |
| `-` | An Idempotency-Key outside 8 to 64 letters, digits, _ or - is rejected | C-CF-211 | Core features, feature 11 rule 2 |
| `Idempotency-Key` | A repeated Idempotency-Key with the same body returns the same gift | C-CF-213 | Core features, feature 11 rule 4 |
| `group_id` | A one-to-one envelope carries group_id null | C-CF-215 | Core features, feature 1 rule 5 |
| `missing_devices` | missing_devices with extra_devices list device ids in ascending order | C-CF-216 | Core features, feature 1 rule 3 |
| `extra_devices` | missing_devices with extra_devices list device ids in ascending order | C-CF-216 | Core features, feature 1 rule 3 |
| `expected_revision` | A group change carrying a stale expected_revision is rejected with the current revision | C-CF-218 | Core features, feature 6 rule 2; Deployment contract, API shapes |
| `revision` | A group change carrying a stale expected_revision is rejected with the current revision | C-CF-218 | Core features, feature 6 rule 2; Deployment contract, API shapes |
| `/signup` | Sign-up at /signup lands on /chats | C-CF-221 | Core features, feature 7 rule 1 |
| `/chats` | Sign-up at /signup lands on /chats | C-CF-221 | Core features, feature 7 rule 1 |
| `GET /api/messages` | The browser learns of new envelopes only by requesting GET /api/messages, never ... | C-CF-222 | Core features, feature 7 rule 6 |
| `New group` | Creating a group in the New group dialog opens /groups/{group_id} | C-CF-228 | Core features, feature 7 rule 4 |
| `/groups/{group_id}` | Creating a group in the New group dialog opens /groups/{group_id} | C-CF-228 | Core features, feature 7 rule 4 |
| `/unlock` | A wrong password at /unlock shows an inline banner, keeping the store locked | C-CF-231 | Core features, feature 7 rule 3 |
| `/login` | Opening a device route without signing in redirects to /login | C-UF-01 | User flow, entry and redirects |
| `/chats` | Sign-in lands on /chats | C-UF-02 | User flow, entry and redirects |
| `/login` | A browser whose device was unlinked or replaced elsewhere returns to /login showing ... | C-UF-03 | User flow, entry and redirects |
| `This browser was unlinked` | A browser whose device was unlinked or replaced elsewhere returns to /login showing ... | C-UF-03 | User flow, entry and redirects |
| `This group is not available` | A user opening a group without membership sees the pinned group-unavailable message | C-UF-04 | User flow, entry and redirects |
| `/link` | The /link screen links a browser with a code from the user's first browser | C-UF-05 | User flow, journey 8 |
| `/chats` | The /chats list shows the empty state No conversations yet | C-UF-06 | User flow, states |
| `No conversations yet` | The /chats list shows the empty state No conversations yet | C-UF-06 | User flow, states |
| `/chats/{username}` | /chats/{username} shows the conversation view | C-UF-10 | User flow, route table |
| `/chats/{username}/safety` | /chats/{username}/safety shows the safety number | C-UF-11 | User flow, route table |
| `/groups/{group_id}` | /groups/{group_id} shows the group conversation view with its members | C-UF-12 | User flow, route table |
| `/get` | The declared pages live at /get, /help, /blog, /developers, /careers, /brand | C-UF-13 | User flow, route table; Core features, feature 12 rule 5 |
| `/help` | The declared pages live at /get, /help, /blog, /developers, /careers, /brand | C-UF-13 | User flow, route table; Core features, feature 12 rule 5 |
| `/blog` | The declared pages live at /get, /help, /blog, /developers, /careers, /brand | C-UF-13 | User flow, route table; Core features, feature 12 rule 5 |
| `/developers` | The declared pages live at /get, /help, /blog, /developers, /careers, /brand | C-UF-13 | User flow, route table; Core features, feature 12 rule 5 |
| `/careers` | The declared pages live at /get, /help, /blog, /developers, /careers, /brand | C-UF-13 | User flow, route table; Core features, feature 12 rule 5 |
| `/brand` | The declared pages live at /get, /help, /blog, /developers, /careers, /brand | C-UF-13 | User flow, route table; Core features, feature 12 rule 5 |
| `/af` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/ar` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/az` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/bg` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/bn` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/bs` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/ca` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/cs` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/da` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/de` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/el` | The locale routes are /af, /ar, /az, /bg, /bn, /bs, /ca, /cs, /da, /de, /el | C-UF-14 | User flow, route table; Core features, feature 12 rule 2 |
| `/signup` | /signup creates an account, /login signs in, /unlock unlocks the browser | C-UF-15 | User flow, route table |
| `/login` | /signup creates an account, /login signs in, /unlock unlocks the browser | C-UF-15 | User flow, route table |
| `/unlock` | /signup creates an account, /login signs in, /unlock unlocks the browser | C-UF-15 | User flow, route table |
| `/chats` | The group-unavailable screen offers a way back to /chats | C-UF-16 | User flow, entry and redirects |
| `44` | Touch targets are at least 44 by 44 CSS pixels | C-UX-25 | Front-end specification, accessibility values; UI/UX notes, accessibility floor |
| `hero-phone` | Each hero-phone carries alternative text describing the drawing | C-UX-28 | UI/UX notes, accessibility floor; Front-end specification, home item 1 |
| `Get Beacon` | Each page leads with one primary action: Get Beacon on the home, Donate on /donate, ... | C-UX-30 | UI/UX notes, primary action |
| `/donate` | Each page leads with one primary action: Get Beacon on the home, Donate on /donate, ... | C-UX-30 | UI/UX notes, primary action |
| `Get Beacon` | In-text links with the filled Get Beacon button use the brand blue | C-UX-65 | UI/UX notes, palette paragraph |
| `Get Beacon` | The filled Get Beacon button moves to the interactive blue on hover | C-UX-70 | UI/UX notes, palette paragraph |
| `/api` | Marketing routes arrive as build-time HTML, with messenger routes rendering in the ... | C-TR-03 | Technical requirements, stack paragraph |
| `DATABASE_URL` | The only backing services are PostgreSQL at DATABASE_URL or Mailpit at SMTP_HOST | C-TR-05 | Technical requirements, libraries paragraph |
| `SMTP_HOST` | The only backing services are PostgreSQL at DATABASE_URL or Mailpit at SMTP_HOST | C-TR-05 | Technical requirements, libraries paragraph |
| `Beacon <no-reply@beacon.example.org>` | Mail goes from Beacon <no-reply@beacon.example.org> | C-TR-07 | Technical requirements, environment paragraph |
| `libsodium-wrappers-sumo` | All cryptography comes from libsodium-wrappers-sumo or @noble/post-quantum | C-TR-08 | Technical requirements, cryptography paragraph |
| `@noble/post-quantum` | All cryptography comes from libsodium-wrappers-sumo or @noble/post-quantum | C-TR-08 | Technical requirements, cryptography paragraph |
| `font-display: swap` | The Inter weights 400, 500, 600 with 800 are self-hosted with font-display: swap | C-TR-17 | Technical requirements, performance paragraph |
| `fastify` | fastify with @fastify/static serve HTTP with static files | C-TR-19 | Technical requirements, library table |
| `@fastify/static` | fastify with @fastify/static serve HTTP with static files | C-TR-19 | Technical requirements, library table |
| `pg` | pg is the PostgreSQL client | C-TR-20 | Technical requirements, library table |
| `nodemailer` | nodemailer sends SMTP mail | C-TR-21 | Technical requirements, library table |
| `bcryptjs` | bcryptjs hashes passwords | C-TR-22 | Technical requirements, library table |
| `preact` | preact, preact-iso, vite, preact-render-to-string build the UI | C-TR-23 | Technical requirements, library table |
| `preact-iso` | preact, preact-iso, vite, preact-render-to-string build the UI | C-TR-23 | Technical requirements, library table |
| `vite` | preact, preact-iso, vite, preact-render-to-string build the UI | C-TR-23 | Technical requirements, library table |
| `preact-render-to-string` | preact, preact-iso, vite, preact-render-to-string build the UI | C-TR-23 | Technical requirements, library table |
| `libsodium-wrappers-sumo` | libsodium-wrappers-sumo supplies X25519, Ed25519, XChaCha20-Poly1305, BLAKE2b, Argon2id | C-TR-24 | Technical requirements, library table |
| `@noble/post-quantum` | @noble/post-quantum supplies ML-KEM-768 key encapsulation | C-TR-25 | Technical requirements, library table |
| `idb` | idb wraps browser storage | C-TR-26 | Technical requirements, library table |
| `@fontsource/inter` | @fontsource/inter supplies the Inter font files | C-TR-27 | Technical requirements, library table |
| `DATABASE_URL` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `SMTP_HOST` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `SMTP_PORT` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `SMTP_USER` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `SMTP_PASS` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `APP_PUBLIC_URL` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `APP_PUBLIC_PORT` | The app reads DATABASE_URL, SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, ... | C-TR-28 | Technical requirements, environment paragraph |
| `donations` | Gifts persist in donations with amount_minor, currency, email | C-DM-01 | Data model, donations table |
| `amount_minor` | Gifts persist in donations with amount_minor, currency, email | C-DM-01 | Data model, donations table |
| `currency` | Gifts persist in donations with amount_minor, currency, email | C-DM-01 | Data model, donations table |
| `email` | Gifts persist in donations with amount_minor, currency, email | C-DM-01 | Data model, donations table |
| `server_timestamp` | Envelope server_timestamp values are integer milliseconds since the epoch in UTC | C-DM-02 | Core features, feature 1 rule 5; Data model, opening paragraph |
| `deku-demo-pw-2026` | Every seeded account signs in with the password deku-demo-pw-2026 | C-DM-03 | Data model, password paragraph |
| `accounts` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `devices` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `one_time_prekeys` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `link_codes` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `profiles` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `envelopes` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `acknowledged_guids` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `groups` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `group_members` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `recovery_records` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `donations` | PostgreSQL holds the tables accounts, devices, one_time_prekeys, link_codes, profiles, ... | C-DM-09 | Data model, opening paragraph |
| `accounts` | accounts carries email, username, password_hash, failed_sign_ins, locked_until | C-DM-10 | Data model, accounts table |
| `email` | accounts carries email, username, password_hash, failed_sign_ins, locked_until | C-DM-10 | Data model, accounts table |
| `username` | accounts carries email, username, password_hash, failed_sign_ins, locked_until | C-DM-10 | Data model, accounts table |
| `password_hash` | accounts carries email, username, password_hash, failed_sign_ins, locked_until | C-DM-10 | Data model, accounts table |
| `failed_sign_ins` | accounts carries email, username, password_hash, failed_sign_ins, locked_until | C-DM-10 | Data model, accounts table |
| `locked_until` | accounts carries email, username, password_hash, failed_sign_ins, locked_until | C-DM-10 | Data model, accounts table |
| `devices` | devices carries account_id, device_id, identity_key, token_hash, revoked_at | C-DM-11 | Data model, devices table |
| `account_id` | devices carries account_id, device_id, identity_key, token_hash, revoked_at | C-DM-11 | Data model, devices table |
| `device_id` | devices carries account_id, device_id, identity_key, token_hash, revoked_at | C-DM-11 | Data model, devices table |
| `identity_key` | devices carries account_id, device_id, identity_key, token_hash, revoked_at | C-DM-11 | Data model, devices table |
| `token_hash` | devices carries account_id, device_id, identity_key, token_hash, revoked_at | C-DM-11 | Data model, devices table |
| `revoked_at` | devices carries account_id, device_id, identity_key, token_hash, revoked_at | C-DM-11 | Data model, devices table |
| `one_time_prekeys` | one_time_prekeys carries device_ref, key_id, public_key, handed_out_at | C-DM-12 | Data model, one_time_prekeys table |
| `device_ref` | one_time_prekeys carries device_ref, key_id, public_key, handed_out_at | C-DM-12 | Data model, one_time_prekeys table |
| `key_id` | one_time_prekeys carries device_ref, key_id, public_key, handed_out_at | C-DM-12 | Data model, one_time_prekeys table |
| `public_key` | one_time_prekeys carries device_ref, key_id, public_key, handed_out_at | C-DM-12 | Data model, one_time_prekeys table |
| `handed_out_at` | one_time_prekeys carries device_ref, key_id, public_key, handed_out_at | C-DM-12 | Data model, one_time_prekeys table |
| `link_codes` | link_codes carries a unique code with used_at | C-DM-13 | Data model, link_codes table |
| `code` | link_codes carries a unique code with used_at | C-DM-13 | Data model, link_codes table |
| `used_at` | link_codes carries a unique code with used_at | C-DM-13 | Data model, link_codes table |
| `profiles` | profiles carries one row per account with profile_ciphertext, access_key | C-DM-14 | Data model, profiles table |
| `profile_ciphertext` | profiles carries one row per account with profile_ciphertext, access_key | C-DM-14 | Data model, profiles table |
| `access_key` | profiles carries one row per account with profile_ciphertext, access_key | C-DM-14 | Data model, profiles table |
| `envelopes` | envelopes carries recipient_device, guid, ciphertext, group_id, server_timestamp | C-DM-15 | Data model, envelopes table |
| `recipient_device` | envelopes carries recipient_device, guid, ciphertext, group_id, server_timestamp | C-DM-15 | Data model, envelopes table |
| `guid` | envelopes carries recipient_device, guid, ciphertext, group_id, server_timestamp | C-DM-15 | Data model, envelopes table |
| `ciphertext` | envelopes carries recipient_device, guid, ciphertext, group_id, server_timestamp | C-DM-15 | Data model, envelopes table |
| `group_id` | envelopes carries recipient_device, guid, ciphertext, group_id, server_timestamp | C-DM-15 | Data model, envelopes table |
| `server_timestamp` | envelopes carries recipient_device, guid, ciphertext, group_id, server_timestamp | C-DM-15 | Data model, envelopes table |
| `groups` | groups carries revision with encrypted_state | C-DM-16 | Data model, groups table |
| `revision` | groups carries revision with encrypted_state | C-DM-16 | Data model, groups table |
| `encrypted_state` | groups carries revision with encrypted_state | C-DM-16 | Data model, groups table |
| `group_members` | group_members carries a unique group_id with account_id pair plus is_admin | C-DM-17 | Data model, group_members table |
| `group_id` | group_members carries a unique group_id with account_id pair plus is_admin | C-DM-17 | Data model, group_members table |
| `account_id` | group_members carries a unique group_id with account_id pair plus is_admin | C-DM-17 | Data model, group_members table |
| `is_admin` | group_members carries a unique group_id with account_id pair plus is_admin | C-DM-17 | Data model, group_members table |
| `recovery_records` | recovery_records carries recovery_blob, access_verifier, failed_guesses | C-DM-18 | Data model, recovery_records table |
| `recovery_blob` | recovery_records carries recovery_blob, access_verifier, failed_guesses | C-DM-18 | Data model, recovery_records table |
| `access_verifier` | recovery_records carries recovery_blob, access_verifier, failed_guesses | C-DM-18 | Data model, recovery_records table |
| `failed_guesses` | recovery_records carries recovery_blob, access_verifier, failed_guesses | C-DM-18 | Data model, recovery_records table |
| `/app/USER_README.md` | /app/USER_README.md carries one line per seeded account in the form email: ... | C-DM-21 | Data model, password paragraph |
| `email: user@example.com password: deku-demo-pw-2026` | /app/USER_README.md carries one line per seeded account in the form email: ... | C-DM-21 | Data model, password paragraph |
| `public` | The tables live in the public schema | C-DM-22 | Data model, opening paragraph |
| `devices` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `signed_prekey_id` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `signed_prekey_public` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `signed_prekey_signature` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `pq_prekey_id` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `pq_prekey_public` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `pq_prekey_signature` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `created_at` | devices also carries signed_prekey_id, signed_prekey_public, signed_prekey_signature, ... | C-DM-25 | Data model, devices table |
| `accounts` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `groups` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `donations` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `created_at` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `link_codes` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `issued_by_device` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `idempotency_key` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `request_fingerprint` | accounts, groups, donations carry created_at; link_codes carries issued_by_device; ... | C-DM-26 | Data model, accounts table; Data model, donations table |
| `link_codes` | link_codes carries account_id; acknowledged_guids carries a unique recipient_device ... | C-DM-27 | Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table |
| `account_id` | link_codes carries account_id; acknowledged_guids carries a unique recipient_device ... | C-DM-27 | Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table |
| `acknowledged_guids` | link_codes carries account_id; acknowledged_guids carries a unique recipient_device ... | C-DM-27 | Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table |
| `recipient_device` | link_codes carries account_id; acknowledged_guids carries a unique recipient_device ... | C-DM-27 | Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table |
| `guid` | link_codes carries account_id; acknowledged_guids carries a unique recipient_device ... | C-DM-27 | Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table |
| `recovery_records` | link_codes carries account_id; acknowledged_guids carries a unique recipient_device ... | C-DM-27 | Data model, link_codes table; Data model, acknowledged_guids table; Data model, recovery_records table |
| `Inter, SF Pro, Segoe UI, Roboto, Oxygen, Ubuntu, Helvetica Neue, Helvetica, Arial, sans-serif` | Body text uses the stack Inter, SF Pro, Segoe UI, Roboto, Oxygen, Ubuntu, Helvetica ... | C-FE-01 | Front-end specification, type scale |
| `60px` | The hero headline is 60px at 800 with a 64px line on a laptop, 28px with a 32px line ... | C-FE-02 | Front-end specification, type scale table |
| `800` | The hero headline is 60px at 800 with a 64px line on a laptop, 28px with a 32px line ... | C-FE-02 | Front-end specification, type scale table |
| `64px` | The hero headline is 60px at 800 with a 64px line on a laptop, 28px with a 32px line ... | C-FE-02 | Front-end specification, type scale table |
| `28px` | The hero headline is 60px at 800 with a 64px line on a laptop, 28px with a 32px line ... | C-FE-02 | Front-end specification, type scale table |
| `32px` | The hero headline is 60px at 800 with a 64px line on a laptop, 28px with a 32px line ... | C-FE-02 | Front-end specification, type scale table |
| `16px` | Buttons with strong labels are 16px at 600 with a 22px line | C-FE-06 | Front-end specification, type scale table |
| `600` | Buttons with strong labels are 16px at 600 with a 22px line | C-FE-06 | Front-end specification, type scale table |
| `22px` | Buttons with strong labels are 16px at 600 with a 22px line | C-FE-06 | Front-end specification, type scale table |
| `16px` | Body paragraphs are 16px at 400 with a 24px line | C-FE-07 | Front-end specification, type scale table |
| `400` | Body paragraphs are 16px at 400 with a 24px line | C-FE-07 | Front-end specification, type scale table |
| `24px` | Body paragraphs are 16px at 400 with a 24px line | C-FE-07 | Front-end specification, type scale table |
| `brandNavbar` | The sticky top bar carries the id brandNavbar | C-FE-08 | Front-end specification, global chrome |
| `get-app` | The hero Get Beacon button carries the class get-app | C-FE-10 | Front-end specification, global chrome |
| `Organization` | The dark footer holds the Organization, Download, Social, Help link columns | C-FE-11 | Front-end specification, global chrome table |
| `Download` | The dark footer holds the Organization, Download, Social, Help link columns | C-FE-11 | Front-end specification, global chrome table |
| `Social` | The dark footer holds the Organization, Download, Social, Help link columns | C-FE-11 | Front-end specification, global chrome table |
| `Help` | The dark footer holds the Organization, Download, Social, Help link columns | C-FE-11 | Front-end specification, global chrome table |
| `hero-phone` | Each hero-phone element is tilted 22.5 degrees clockwise | C-FE-17 | Front-end specification, home item 1 |
| `/donate` | The Donate to Beacon button opens /donate | C-FE-25 | Front-end specification, home item 6 |
| `spinAround` | The utility animations are named spinAround, pulsate, moveIndeterminate | C-FE-26 | Front-end specification, motion names |
| `pulsate` | The utility animations are named spinAround, pulsate, moveIndeterminate | C-FE-26 | Front-end specification, motion names |
| `moveIndeterminate` | The utility animations are named spinAround, pulsate, moveIndeterminate | C-FE-26 | Front-end specification, motion names |
| `1em` | Body text is 1em at the regular 400 face with line height 1.5 under optimizeLegibility | C-FE-31 | Front-end specification, type scale |
| `400` | Body text is 1em at the regular 400 face with line height 1.5 under optimizeLegibility | C-FE-31 | Front-end specification, type scale |
| `1.5` | Body text is 1em at the regular 400 face with line height 1.5 under optimizeLegibility | C-FE-31 | Front-end specification, type scale |
| `optimizeLegibility` | Body text is 1em at the regular 400 face with line height 1.5 under optimizeLegibility | C-FE-31 | Front-end specification, type scale |
| `Inconsolata, Hack, SF Mono, Roboto Mono, Source Code Pro, Ubuntu Mono, monospace` | Inline code uses Inconsolata, Hack, SF Mono, Roboto Mono, Source Code Pro, Ubuntu ... | C-FE-32 | Front-end specification, type scale |
| `28px` | Sub-section headings are 28px at 800 with a 32px line | C-FE-33 | Front-end specification, type scale table |
| `800` | Sub-section headings are 28px at 800 with a 32px line | C-FE-33 | Front-end specification, type scale table |
| `32px` | Sub-section headings are 28px at 800 with a 32px line | C-FE-33 | Front-end specification, type scale table |
| `24px` | The large lead is 24px at 400 with a 24px line | C-FE-34 | Front-end specification, type scale table |
| `400` | The large lead is 24px at 400 with a 24px line | C-FE-34 | Front-end specification, type scale table |
| `16px` | Dense body text is 16px at 400 with a 22px line | C-FE-35 | Front-end specification, type scale table |
| `400` | Dense body text is 16px at 400 with a 22px line | C-FE-35 | Front-end specification, type scale table |
| `22px` | Dense body text is 16px at 400 with a 22px line | C-FE-35 | Front-end specification, type scale table |
| `800` | The wordmark sets Beacon in Inter 800 | C-FE-41 | Front-end specification, iconography |
| `Why use Beacon?` | The Why use Beacon? heading is centred | C-FE-43 | Front-end specification, home item 2 |
| `Hey check this out!` | The privacy statement drawing shows a chat bubble carrying the pinned greeting | C-FE-46 | Front-end specification, home item 3 |
| `No ads. No trackers. No kidding.` | The No ads. No trackers. No kidding. heading is left-aligned | C-FE-47 | Front-end specification, home item 5 |
| `768` | The responsive tiers break at 768, 1023, 1215, 1407 CSS pixels | C-FE-49 | Front-end specification, responsive tiers |
| `1023` | The responsive tiers break at 768, 1023, 1215, 1407 CSS pixels | C-FE-49 | Front-end specification, responsive tiers |
| `1215` | The responsive tiers break at 768, 1023, 1215, 1407 CSS pixels | C-FE-49 | Front-end specification, responsive tiers |
| `1407` | The responsive tiers break at 768, 1023, 1215, 1407 CSS pixels | C-FE-49 | Front-end specification, responsive tiers |
| `300` | The body never narrows below 300 CSS pixels | C-FE-50 | Front-end specification, responsive tiers |
| `4.5:1` | Body text contrast is at least 4.5:1 in both colour preferences | C-FE-51 | Front-end specification, accessibility values |
| `English` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Afrikaans` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `العربية` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Azərbaycan dili` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Български` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `বাংলা` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Bosanski` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Català` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Čeština` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Dansk` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Deutsch` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `Ελληνικά` | The language dialog lists English, Afrikaans, العربية, Azərbaycan dili, Български, ... | C-FE-52 | Core features, feature 12 rule 3; Front-end specification, global chrome |
| `data-testid` | Every hook is a data-testid attribute carrying exactly the listed name | C-FE-53 | Front-end specification, machine-readable hooks |
| `Donate to Beacon` | The Donate to Beacon button is an outline button | C-FE-54 | Front-end specification, home item 6 |
| `spinAround` | spinAround turns a full circle, pulsate dims to half opacity midway, moveIndeterminate ... | C-FE-57 | Front-end specification, motion names |
| `pulsate` | spinAround turns a full circle, pulsate dims to half opacity midway, moveIndeterminate ... | C-FE-57 | Front-end specification, motion names |
| `moveIndeterminate` | spinAround turns a full circle, pulsate dims to half opacity midway, moveIndeterminate ... | C-FE-57 | Front-end specification, motion names |
| `Donate` | The Organization column lists Donate, Careers, Blog, Brand Assets, Terms & Privacy Policy | C-FE-58 | Front-end specification, global chrome table |
| `Careers` | The Organization column lists Donate, Careers, Blog, Brand Assets, Terms & Privacy Policy | C-FE-58 | Front-end specification, global chrome table |
| `Blog` | The Organization column lists Donate, Careers, Blog, Brand Assets, Terms & Privacy Policy | C-FE-58 | Front-end specification, global chrome table |
| `Brand Assets` | The Organization column lists Donate, Careers, Blog, Brand Assets, Terms & Privacy Policy | C-FE-58 | Front-end specification, global chrome table |
| `Terms & Privacy Policy` | The Organization column lists Donate, Careers, Blog, Brand Assets, Terms & Privacy Policy | C-FE-58 | Front-end specification, global chrome table |
| `Android` | The Download column lists Android, iPhone & iPad, Windows, Mac, Linux | C-FE-59 | Front-end specification, global chrome table |
| `iPhone & iPad` | The Download column lists Android, iPhone & iPad, Windows, Mac, Linux | C-FE-59 | Front-end specification, global chrome table |
| `Windows` | The Download column lists Android, iPhone & iPad, Windows, Mac, Linux | C-FE-59 | Front-end specification, global chrome table |
| `Mac` | The Download column lists Android, iPhone & iPad, Windows, Mac, Linux | C-FE-59 | Front-end specification, global chrome table |
| `Linux` | The Download column lists Android, iPhone & iPad, Windows, Mac, Linux | C-FE-59 | Front-end specification, global chrome table |
| `Bluesky` | The Social column lists Bluesky, GitHub, Instagram, Mastodon, X | C-FE-60 | Front-end specification, global chrome table |
| `GitHub` | The Social column lists Bluesky, GitHub, Instagram, Mastodon, X | C-FE-60 | Front-end specification, global chrome table |
| `Instagram` | The Social column lists Bluesky, GitHub, Instagram, Mastodon, X | C-FE-60 | Front-end specification, global chrome table |
| `Mastodon` | The Social column lists Bluesky, GitHub, Instagram, Mastodon, X | C-FE-60 | Front-end specification, global chrome table |
| `X` | The Social column lists Bluesky, GitHub, Instagram, Mastodon, X | C-FE-60 | Front-end specification, global chrome table |
| `Support Center` | The Help column lists Support Center, Community | C-FE-61 | Front-end specification, global chrome table |
| `Community` | The Help column lists Support Center, Community | C-FE-61 | Front-end specification, global chrome table |
| `language-control` | The hook language-control marks the top bar's language button | C-FE-63 | Front-end specification, machine-readable hooks |
| `language-dialog` | The hook language-dialog marks the language dialog, with role="dialog", aria-modal="true" | C-FE-64 | Front-end specification, machine-readable hooks |
| `role="dialog"` | The hook language-dialog marks the language dialog, with role="dialog", aria-modal="true" | C-FE-64 | Front-end specification, machine-readable hooks |
| `aria-modal="true"` | The hook language-dialog marks the language dialog, with role="dialog", aria-modal="true" | C-FE-64 | Front-end specification, machine-readable hooks |
| `menu-button` | The hook menu-button marks the narrow-viewport menu button, with aria-expanded | C-FE-65 | Front-end specification, machine-readable hooks |
| `aria-expanded` | The hook menu-button marks the narrow-viewport menu button, with aria-expanded | C-FE-65 | Front-end specification, machine-readable hooks |
| `hero-phone` | The hook hero-phone marks each rotated phone render | C-FE-66 | Front-end specification, machine-readable hooks |
| `feature-illustration` | The hook feature-illustration marks each feature card illustration | C-FE-67 | Front-end specification, machine-readable hooks |
| `donate-amount` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `data-amount-minor` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `500` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `1000` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `2500` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `5000` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `10000` | The hook donate-amount marks each preset amount button, carrying data-amount-minor ... | C-FE-68 | Front-end specification, machine-readable hooks |
| `donate-custom-amount` | The hook donate-custom-amount marks the custom amount field, in dollars | C-FE-69 | Front-end specification, machine-readable hooks |
| `donate-email` | The hook donate-email marks the donor email field | C-FE-70 | Front-end specification, machine-readable hooks |
| `donate-submit` | The hook donate-submit marks the Donate button | C-FE-71 | Front-end specification, machine-readable hooks |
| `donate-confirmation` | The hook donate-confirmation marks the inline banner after a recorded gift | C-FE-72 | Front-end specification, machine-readable hooks |
| `donate-error` | The hook donate-error marks the inline refusal naming the field | C-FE-73 | Front-end specification, machine-readable hooks |
| `signup-email` | The hooks signup-email, signup-username, signup-password, signup-submit mark the ... | C-FE-74 | Front-end specification, machine-readable hooks |
| `signup-username` | The hooks signup-email, signup-username, signup-password, signup-submit mark the ... | C-FE-74 | Front-end specification, machine-readable hooks |
| `signup-password` | The hooks signup-email, signup-username, signup-password, signup-submit mark the ... | C-FE-74 | Front-end specification, machine-readable hooks |
| `signup-submit` | The hooks signup-email, signup-username, signup-password, signup-submit mark the ... | C-FE-74 | Front-end specification, machine-readable hooks |
| `login-email` | The hooks login-email, login-password, login-submit mark the sign-in form | C-FE-75 | Front-end specification, machine-readable hooks |
| `login-password` | The hooks login-email, login-password, login-submit mark the sign-in form | C-FE-75 | Front-end specification, machine-readable hooks |
| `login-submit` | The hooks login-email, login-password, login-submit mark the sign-in form | C-FE-75 | Front-end specification, machine-readable hooks |
| `unlock-password` | The hooks unlock-password, unlock-submit mark the unlock form | C-FE-76 | Front-end specification, machine-readable hooks |
| `unlock-submit` | The hooks unlock-password, unlock-submit mark the unlock form | C-FE-76 | Front-end specification, machine-readable hooks |
| `link-code-input` | The hooks link-code-input, link-code-submit mark entering a link code on /link | C-FE-77 | Front-end specification, machine-readable hooks |
| `link-code-submit` | The hooks link-code-input, link-code-submit mark entering a link code on /link | C-FE-77 | Front-end specification, machine-readable hooks |
| `/link` | The hooks link-code-input, link-code-submit mark entering a link code on /link | C-FE-77 | Front-end specification, machine-readable hooks |
| `recovery-replace-pin` | The hooks recovery-replace-pin, recovery-replace-submit, recovery-replace-confirm mark ... | C-FE-78 | Front-end specification, machine-readable hooks |
| `recovery-replace-submit` | The hooks recovery-replace-pin, recovery-replace-submit, recovery-replace-confirm mark ... | C-FE-78 | Front-end specification, machine-readable hooks |
| `recovery-replace-confirm` | The hooks recovery-replace-pin, recovery-replace-submit, recovery-replace-confirm mark ... | C-FE-78 | Front-end specification, machine-readable hooks |
| `/link` | The hooks recovery-replace-pin, recovery-replace-submit, recovery-replace-confirm mark ... | C-FE-78 | Front-end specification, machine-readable hooks |
| `new-chat` | The hooks new-chat, new-chat-username, new-chat-start mark the new chat dialog | C-FE-79 | Front-end specification, machine-readable hooks |
| `new-chat-username` | The hooks new-chat, new-chat-username, new-chat-start mark the new chat dialog | C-FE-79 | Front-end specification, machine-readable hooks |
| `new-chat-start` | The hooks new-chat, new-chat-username, new-chat-start mark the new chat dialog | C-FE-79 | Front-end specification, machine-readable hooks |
| `new-group` | The hooks new-group, new-group-name, new-group-members, new-group-create mark the new ... | C-FE-80 | Front-end specification, machine-readable hooks |
| `new-group-name` | The hooks new-group, new-group-name, new-group-members, new-group-create mark the new ... | C-FE-80 | Front-end specification, machine-readable hooks |
| `new-group-members` | The hooks new-group, new-group-name, new-group-members, new-group-create mark the new ... | C-FE-80 | Front-end specification, machine-readable hooks |
| `new-group-create` | The hooks new-group, new-group-name, new-group-members, new-group-create mark the new ... | C-FE-80 | Front-end specification, machine-readable hooks |
| `conversation-row` | The hook conversation-row marks each row on /chats, carrying data-username (or ... | C-FE-81 | Front-end specification, machine-readable hooks |
| `/chats` | The hook conversation-row marks each row on /chats, carrying data-username (or ... | C-FE-81 | Front-end specification, machine-readable hooks |
| `data-username` | The hook conversation-row marks each row on /chats, carrying data-username (or ... | C-FE-81 | Front-end specification, machine-readable hooks |
| `data-group-id` | The hook conversation-row marks each row on /chats, carrying data-username (or ... | C-FE-81 | Front-end specification, machine-readable hooks |
| `data-muted="true"` | The hook conversation-row marks each row on /chats, carrying data-username (or ... | C-FE-81 | Front-end specification, machine-readable hooks |
| `unread-count` | The hook unread-count marks the unread number inside a row | C-FE-82 | Front-end specification, machine-readable hooks |
| `conversation-title` | The hook conversation-title marks the conversation header's name: the contact's ... | C-FE-83 | Front-end specification, machine-readable hooks |
| `conversation-archive` | The hooks conversation-archive, conversation-mute mark the header's archive, mute controls | C-FE-84 | Front-end specification, machine-readable hooks |
| `conversation-mute` | The hooks conversation-archive, conversation-mute mark the header's archive, mute controls | C-FE-84 | Front-end specification, machine-readable hooks |
| `message-bubble` | The hook message-bubble marks each message, carrying data-direction of in or out | C-FE-85 | Front-end specification, machine-readable hooks |
| `data-direction` | The hook message-bubble marks each message, carrying data-direction of in or out | C-FE-85 | Front-end specification, machine-readable hooks |
| `in` | The hook message-bubble marks each message, carrying data-direction of in or out | C-FE-85 | Front-end specification, machine-readable hooks |
| `out` | The hook message-bubble marks each message, carrying data-direction of in or out | C-FE-85 | Front-end specification, machine-readable hooks |
| `message-text` | The hook message-text marks the text inside a bubble | C-FE-86 | Front-end specification, machine-readable hooks |
| `message-status` | The hook message-status marks an outgoing bubble's state text: Sending, Sent, ... | C-FE-87 | Front-end specification, machine-readable hooks |
| `Sending` | The hook message-status marks an outgoing bubble's state text: Sending, Sent, ... | C-FE-87 | Front-end specification, machine-readable hooks |
| `Sent` | The hook message-status marks an outgoing bubble's state text: Sending, Sent, ... | C-FE-87 | Front-end specification, machine-readable hooks |
| `Delivered` | The hook message-status marks an outgoing bubble's state text: Sending, Sent, ... | C-FE-87 | Front-end specification, machine-readable hooks |
| `Read` | The hook message-status marks an outgoing bubble's state text: Sending, Sent, ... | C-FE-87 | Front-end specification, machine-readable hooks |
| `message-edit` | The hooks message-edit, message-edit-input, message-edit-save mark editing an outgoing ... | C-FE-88 | Front-end specification, machine-readable hooks |
| `message-edit-input` | The hooks message-edit, message-edit-input, message-edit-save mark editing an outgoing ... | C-FE-88 | Front-end specification, machine-readable hooks |
| `message-edit-save` | The hooks message-edit, message-edit-input, message-edit-save mark editing an outgoing ... | C-FE-88 | Front-end specification, machine-readable hooks |
| `message-bubble` | The hooks message-edit, message-edit-input, message-edit-save mark editing an outgoing ... | C-FE-88 | Front-end specification, machine-readable hooks |
| `message-delete` | The hooks message-delete, message-delete-confirm mark deleting an outgoing message, ... | C-FE-89 | Front-end specification, machine-readable hooks |
| `message-delete-confirm` | The hooks message-delete, message-delete-confirm mark deleting an outgoing message, ... | C-FE-89 | Front-end specification, machine-readable hooks |
| `message-bubble` | The hooks message-delete, message-delete-confirm mark deleting an outgoing message, ... | C-FE-89 | Front-end specification, machine-readable hooks |
| `message-image` | The hooks message-image, message-video, message-file, message-voice, message-sticker ... | C-FE-90 | Front-end specification, machine-readable hooks |
| `message-video` | The hooks message-image, message-video, message-file, message-voice, message-sticker ... | C-FE-90 | Front-end specification, machine-readable hooks |
| `message-file` | The hooks message-image, message-video, message-file, message-voice, message-sticker ... | C-FE-90 | Front-end specification, machine-readable hooks |
| `message-voice` | The hooks message-image, message-video, message-file, message-voice, message-sticker ... | C-FE-90 | Front-end specification, machine-readable hooks |
| `message-sticker` | The hooks message-image, message-video, message-file, message-voice, message-sticker ... | C-FE-90 | Front-end specification, machine-readable hooks |
| `decrypt-error-notice` | The hook decrypt-error-notice marks the notice on /chats reading the pinned text | C-FE-91 | Front-end specification, machine-readable hooks |
| `/chats` | The hook decrypt-error-notice marks the notice on /chats reading the pinned text | C-FE-91 | Front-end specification, machine-readable hooks |
| `composer-input` | The hooks composer-input, composer-send mark the composer text field, Send button | C-FE-92 | Front-end specification, machine-readable hooks |
| `composer-send` | The hooks composer-input, composer-send mark the composer text field, Send button | C-FE-92 | Front-end specification, machine-readable hooks |
| `composer-attach` | The hook composer-attach marks the file input for photos, video, files | C-FE-93 | Front-end specification, machine-readable hooks |
| `composer-voice` | The hook composer-voice marks start, then stop, send, a voice message | C-FE-94 | Front-end specification, machine-readable hooks |
| `composer-sticker` | The hooks composer-sticker, sticker-option mark the sticker picker, each built-in ... | C-FE-95 | Front-end specification, machine-readable hooks |
| `sticker-option` | The hooks composer-sticker, sticker-option mark the sticker picker, each built-in ... | C-FE-95 | Front-end specification, machine-readable hooks |
| `call-voice` | The hooks call-voice, call-video, call-screen, call-hang-up mark call controls, the ... | C-FE-96 | Front-end specification, machine-readable hooks |
| `call-video` | The hooks call-voice, call-video, call-screen, call-hang-up mark call controls, the ... | C-FE-96 | Front-end specification, machine-readable hooks |
| `call-screen` | The hooks call-voice, call-video, call-screen, call-hang-up mark call controls, the ... | C-FE-96 | Front-end specification, machine-readable hooks |
| `call-hang-up` | The hooks call-voice, call-video, call-screen, call-hang-up mark call controls, the ... | C-FE-96 | Front-end specification, machine-readable hooks |
| `call-incoming` | The hooks call-incoming, call-answer, call-decline mark the incoming call shown to the ... | C-FE-97 | Front-end specification, machine-readable hooks |
| `call-answer` | The hooks call-incoming, call-answer, call-decline mark the incoming call shown to the ... | C-FE-97 | Front-end specification, machine-readable hooks |
| `call-decline` | The hooks call-incoming, call-answer, call-decline mark the incoming call shown to the ... | C-FE-97 | Front-end specification, machine-readable hooks |
| `safety-number-link` | The hooks safety-number-link, safety-number mark the link to, the display of the ... | C-FE-98 | Front-end specification, machine-readable hooks |
| `safety-number` | The hooks safety-number-link, safety-number mark the link to, the display of the ... | C-FE-98 | Front-end specification, machine-readable hooks |
| `identity-change-banner` | The hooks identity-change-banner, identity-change-accept mark the changed-identity ... | C-FE-99 | Front-end specification, machine-readable hooks |
| `identity-change-accept` | The hooks identity-change-banner, identity-change-accept mark the changed-identity ... | C-FE-99 | Front-end specification, machine-readable hooks |
| `disappearing-timer` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `off` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `30s` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `5m` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `1h` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `1d` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `1w` | The hook disappearing-timer marks the timer select, with option values off, 30s, 5m, ... | C-FE-100 | Front-end specification, machine-readable hooks |
| `group-members` | The hook group-members marks the member list in a group conversation | C-FE-101 | Front-end specification, machine-readable hooks |
| `profile-name-input` | The hooks profile-name-input, profile-save mark the profile form | C-FE-102 | Front-end specification, machine-readable hooks |
| `profile-save` | The hooks profile-name-input, profile-save mark the profile form | C-FE-102 | Front-end specification, machine-readable hooks |
| `device-row` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `link-code-create` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `link-code-value` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `device-unlink` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `device-unlink-confirm` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `sign-out` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `sign-out-confirm` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `data-device-id` | The hooks device-row, link-code-create, link-code-value, device-unlink, ... | C-FE-103 | Front-end specification, machine-readable hooks |
| `recovery-pin-input` | The hooks recovery-pin-input, recovery-save mark the recovery form | C-FE-104 | Front-end specification, machine-readable hooks |
| `recovery-save` | The hooks recovery-pin-input, recovery-save mark the recovery form | C-FE-104 | Front-end specification, machine-readable hooks |
| `Get Beacon` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Help` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Blog` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Developers` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Careers` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Donate` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `English` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Select your language` | The English home renders every copy deck string of the top bar links line exactly | C-FE-105 | Front-end specification, copy deck line 1 |
| `Speak Freely` | The English home renders every copy deck string of the hero headline line exactly | C-FE-106 | Front-end specification, copy deck line 2 |
| `Say "hello" to a different messaging experience. An unexpected focus on privacy, combined with all of the features you expect.` | The English home renders every copy deck string of the hero headline line exactly | C-FE-106 | Front-end specification, copy deck line 2 |
| `Get Beacon` | The English home renders every copy deck string of the hero headline line exactly | C-FE-106 | Front-end specification, copy deck line 2 |
| `Why use Beacon?` | The English home renders every copy deck string of the why band heading line exactly | C-FE-107 | Front-end specification, copy deck line 3 |
| `Explore below to see why Beacon is a simple, powerful, and secure messenger` | The English home renders every copy deck string of the why band heading line exactly | C-FE-107 | Front-end specification, copy deck line 3 |
| `Share Without Insecurity` | The English home renders every copy deck string of the privacy statement heading line ... | C-FE-108 | Front-end specification, copy deck line 4 |
| `State-of-the-art end-to-end encryption (powered by the open source Beacon Protocol) keeps your conversations secure. We can't read your messages or listen to your calls, and no one else can either. Privacy isn't an optional mode. It's just the way that Beacon works. Every message, every call, every time.` | The English home renders every copy deck string of the privacy statement heading line ... | C-FE-108 | Front-end specification, copy deck line 4 |
| `Say Anything` | The English home renders every copy deck string of the card say anything line exactly | C-FE-109 | Front-end specification, copy deck line 5 |
| `Share text, voice messages, photos, videos, GIFs and files for free. Beacon uses your phone's data connection so you can avoid SMS and MMS fees.` | The English home renders every copy deck string of the card say anything line exactly | C-FE-109 | Front-end specification, copy deck line 5 |
| `Speak Freely` | The English home renders every copy deck string of the card speak freely line exactly | C-FE-110 | Front-end specification, copy deck line 6 |
| `Make crystal-clear voice and video calls to people who live across town, or across the ocean, with no long-distance charges.` | The English home renders every copy deck string of the card speak freely line exactly | C-FE-110 | Front-end specification, copy deck line 6 |
| `Make Privacy Stick` | The English home renders every copy deck string of the card make privacy stick line ... | C-FE-111 | Front-end specification, copy deck line 7 |
| `Add a new layer of expression to your conversations with encrypted stickers. You can also create and share your own sticker packs.` | The English home renders every copy deck string of the card make privacy stick line ... | C-FE-111 | Front-end specification, copy deck line 7 |
| `Get Together with Groups` | The English home renders every copy deck string of the card get together with groups ... | C-FE-112 | Front-end specification, copy deck line 8 |
| `Group chats make it easy to stay connected to your family, friends, and coworkers.` | The English home renders every copy deck string of the card get together with groups ... | C-FE-112 | Front-end specification, copy deck line 8 |
| `No ads. No trackers. No kidding.` | The English home renders every copy deck string of the no-tracking heading line exactly | C-FE-113 | Front-end specification, copy deck line 9 |
| `There are no ads, no affiliate marketers, and no creepy tracking in Beacon. So focus on sharing the moments that matter with the people who matter to you.` | The English home renders every copy deck string of the no-tracking heading line exactly | C-FE-113 | Front-end specification, copy deck line 9 |
| `Free for Everyone` | The English home renders every copy deck string of the nonprofit heading line exactly | C-FE-114 | Front-end specification, copy deck line 10 |
| `Beacon is an independent nonprofit. We're not tied to any major tech companies, and we can never be acquired by one either. Development is supported by grants and donations from people like you.` | The English home renders every copy deck string of the nonprofit heading line exactly | C-FE-114 | Front-end specification, copy deck line 10 |
| `Donate to Beacon` | The English home renders every copy deck string of the nonprofit heading line exactly | C-FE-114 | Front-end specification, copy deck line 10 |
| `© 2013-2026 Beacon, a nonprofit.` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `"Beacon", Beacon logos, and other trademarks are trademarks or registered trademarks of Beacon Technology Foundation in the United States and other countries (more info here).` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `For media inquiries, contact press@beacon.example.org` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `Organization` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `Download` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `Social` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `Help` | The English home renders every copy deck string of the footer copyright line exactly | C-FE-115 | Front-end specification, copy deck line 11 |
| `/terms` | The /terms privacy table Accounts row carries its holds with never-holds cells word ... | C-FE-116 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `an identifier, a set of published pre-keys, encrypted profile blobs` | The /terms privacy table Accounts row carries its holds with never-holds cells word ... | C-FE-116 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `plaintext names, avatars, or contact lists` | The /terms privacy table Accounts row carries its holds with never-holds cells word ... | C-FE-116 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `/terms` | The /terms privacy table Messages row carries its holds with never-holds cells word ... | C-FE-117 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `opaque encrypted envelopes queued for offline recipients, then deleted` | The /terms privacy table Messages row carries its holds with never-holds cells word ... | C-FE-117 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `any plaintext message, call audio, or attachment` | The /terms privacy table Messages row carries its holds with never-holds cells word ... | C-FE-117 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `/terms` | The /terms privacy table Groups row carries its holds with never-holds cells word for word | C-FE-118 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `encrypted group state and routing membership sufficient to fan out` | The /terms privacy table Groups row carries its holds with never-holds cells word for word | C-FE-118 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `group names, group avatars or readable group content` | The /terms privacy table Groups row carries its holds with never-holds cells word for word | C-FE-118 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `/terms` | The /terms privacy table Delivery row carries its holds with never-holds cells word ... | C-FE-119 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `acknowledgements and contentless push triggers` | The /terms privacy table Delivery row carries its holds with never-holds cells word ... | C-FE-119 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `message content in any push payload` | The /terms privacy table Delivery row carries its holds with never-holds cells word ... | C-FE-119 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `/terms` | The /terms privacy table Recovery row carries its holds with never-holds cells word ... | C-FE-120 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `a recovery store the service cannot read, guarded by a ten-guess limit` | The /terms privacy table Recovery row carries its holds with never-holds cells word ... | C-FE-120 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `the user's recovery secret` | The /terms privacy table Recovery row carries its holds with never-holds cells word ... | C-FE-120 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `/terms` | The /terms privacy table Donations row carries its holds with never-holds cells word ... | C-FE-121 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `the donor's email and the amount` | The /terms privacy table Donations row carries its holds with never-holds cells word ... | C-FE-121 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `card details of any kind` | The /terms privacy table Donations row carries its holds with never-holds cells word ... | C-FE-121 | Front-end specification, privacy table; Core features, feature 12 rule 6 |
| `APP_PUBLIC_URL` | The app is reachable at APP_PUBLIC_URL on the mapped port | C-DC-01 | Deployment contract, item 1 |
| `/api` | The HTTP API is served on the same origin under /api | C-DC-02 | Deployment contract, item 2 |
| `GET /api/health` | GET /api/health returns 200 once the app is ready | C-DC-03 | Deployment contract, item 3 |
| `/app/USER_README.md` | Login credentials are written to /app/USER_README.md | C-DC-05 | Deployment contract, item 5 |
| `.browser_screenshots/` | Empty .browser_screenshots/ with .downloads/ directories exist at the app root | C-DC-06 | Deployment contract, item 6 |
| `.downloads/` | Empty .browser_screenshots/ with .downloads/ directories exist at the app root | C-DC-06 | Deployment contract, item 6 |
| `0.0.0.0` | The server binds 0.0.0.0 | C-DC-09 | Deployment contract, item 9 |
| `5xx` | Every refusal is a client error, never a 5xx | C-DC-12 | Deployment contract, API shapes paragraph |
| `members` | Group members with admins list usernames in ascending order | C-DC-14 | Deployment contract, key sizes paragraph |
| `admins` | Group members with admins list usernames in ascending order | C-DC-14 | Deployment contract, key sizes paragraph |
| `4173` | The container serves on port 4173, mapped from APP_PUBLIC_PORT | C-DC-16 | Deployment contract, item 1 |
| `APP_PUBLIC_PORT` | The container serves on port 4173, mapped from APP_PUBLIC_PORT | C-DC-16 | Deployment contract, item 1 |
| `POST /api/auth/signup` | POST /api/auth/signup returns username | C-DC-19 | Deployment contract, API shapes |
| `username` | POST /api/auth/signup returns username | C-DC-19 | Deployment contract, API shapes |
| `accepted` | An accepted send returns accepted set to true | C-DC-20 | Deployment contract, API shapes |
| `true` | An accepted send returns accepted set to true | C-DC-20 | Deployment contract, API shapes |
| `group_id` | Group creation with group changes return group_id, revision, members, admins | C-DC-21 | Deployment contract, API shapes |
| `revision` | Group creation with group changes return group_id, revision, members, admins | C-DC-21 | Deployment contract, API shapes |
| `members` | Group creation with group changes return group_id, revision, members, admins | C-DC-21 | Deployment contract, API shapes |
| `admins` | Group creation with group changes return group_id, revision, members, admins | C-DC-21 | Deployment contract, API shapes |
| `GET /api/groups/{group_id}` | GET /api/groups/{group_id} adds encrypted_state to the group fields | C-DC-22 | Deployment contract, API shapes |
| `encrypted_state` | GET /api/groups/{group_id} adds encrypted_state to the group fields | C-DC-22 | Deployment contract, API shapes |
| `GET /api/devices` | GET /api/devices returns device_id entries in ascending order | C-DC-23 | Deployment contract, API shapes |
| `device_id` | GET /api/devices returns device_id entries in ascending order | C-DC-23 | Deployment contract, API shapes |
| `POST /api/keys/one-time` | POST /api/keys/one-time with GET /api/keys/count return one_time_prekeys as the ... | C-DC-24 | Deployment contract, API shapes |
| `GET /api/keys/count` | POST /api/keys/one-time with GET /api/keys/count return one_time_prekeys as the ... | C-DC-24 | Deployment contract, API shapes |
| `one_time_prekeys` | POST /api/keys/one-time with GET /api/keys/count return one_time_prekeys as the ... | C-DC-24 | Deployment contract, API shapes |
| `device_id` | Bundle devices carry device_id, identity_key, signed_prekey, pq_prekey, ... | C-DC-25 | Deployment contract, API shapes |
| `identity_key` | Bundle devices carry device_id, identity_key, signed_prekey, pq_prekey, ... | C-DC-25 | Deployment contract, API shapes |
| `signed_prekey` | Bundle devices carry device_id, identity_key, signed_prekey, pq_prekey, ... | C-DC-25 | Deployment contract, API shapes |
| `pq_prekey` | Bundle devices carry device_id, identity_key, signed_prekey, pq_prekey, ... | C-DC-25 | Deployment contract, API shapes |
| `one_time_prekey` | Bundle devices carry device_id, identity_key, signed_prekey, pq_prekey, ... | C-DC-25 | Deployment contract, API shapes |
| `POST /api/devices` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `identity_key` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `signed_prekey` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `pq_prekey` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `one_time_prekeys` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `link_code` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `replace_existing` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `access_verifier` | POST /api/devices takes identity_key, signed_prekey, pq_prekey, one_time_prekeys with ... | C-DC-26 | Deployment contract, API shapes |
| `messages` | A send body is messages holding device_id, guid, ciphertext entries | C-DC-27 | Deployment contract, API shapes; Core features, feature 1 rule 3 |
| `device_id` | A send body is messages holding device_id, guid, ciphertext entries | C-DC-27 | Deployment contract, API shapes; Core features, feature 1 rule 3 |
| `guid` | A send body is messages holding device_id, guid, ciphertext entries | C-DC-27 | Deployment contract, API shapes; Core features, feature 1 rule 3 |
| `ciphertext` | A send body is messages holding device_id, guid, ciphertext entries | C-DC-27 | Deployment contract, API shapes; Core features, feature 1 rule 3 |
| `DELETE /api/devices/{device_id}` | DELETE /api/devices/{device_id} unlinks a device | C-DC-28 | Deployment contract, API shapes |
| `identity_key` | identity_key decodes to 32 bytes | C-DC-29 | Deployment contract, key sizes paragraph |
| `signed_prekey.public_key` | signed_prekey.public_key decodes to 32 bytes beside a 64-byte signature | C-DC-30 | Deployment contract, key sizes paragraph |
| `signature` | signed_prekey.public_key decodes to 32 bytes beside a 64-byte signature | C-DC-30 | Deployment contract, key sizes paragraph |
| `pq_prekey.public_key` | pq_prekey.public_key decodes to 1184 bytes beside a 64-byte signature | C-DC-31 | Deployment contract, key sizes paragraph |
| `signature` | pq_prekey.public_key decodes to 1184 bytes beside a 64-byte signature | C-DC-31 | Deployment contract, key sizes paragraph |
| `public_key` | Each one-time public_key decodes to 32 bytes | C-DC-32 | Deployment contract, key sizes paragraph |
| `access_key` | access_key decodes to 16 bytes | C-DC-33 | Deployment contract, key sizes paragraph |
| `access_verifier` | access_verifier decodes to 32 bytes | C-DC-34 | Deployment contract, key sizes paragraph |
| `profile_ciphertext` | profile_ciphertext, encrypted_state, recovery_blob each decode to 1 to 65536 bytes | C-DC-35 | Deployment contract, key sizes paragraph |
| `encrypted_state` | profile_ciphertext, encrypted_state, recovery_blob each decode to 1 to 65536 bytes | C-DC-35 | Deployment contract, key sizes paragraph |
| `recovery_blob` | profile_ciphertext, encrypted_state, recovery_blob each decode to 1 to 65536 bytes | C-DC-35 | Deployment contract, key sizes paragraph |
| `key_id` | Every key_id is an integer from 1 to 16777215 | C-DC-36 | Deployment contract, key sizes paragraph |
| `1` | Every key_id is an integer from 1 to 16777215 | C-DC-36 | Deployment contract, key sizes paragraph |
| `16777215` | Every key_id is an integer from 1 to 16777215 | C-DC-36 | Deployment contract, key sizes paragraph |
| `key_id` | A key_id repeated within one upload is rejected | C-DC-37 | Deployment contract, key sizes paragraph |
| `PUT /api/messages/{username}` | Sends use PUT /api/messages/{username} | C-DC-38 | Deployment contract, API shapes |
| `PATCH /api/groups/{group_id}` | Group changes use PATCH /api/groups/{group_id} with expected_revision, ... | C-DC-39 | Deployment contract, API shapes |
| `expected_revision` | Group changes use PATCH /api/groups/{group_id} with expected_revision, ... | C-DC-39 | Deployment contract, API shapes |
| `encrypted_state` | Group changes use PATCH /api/groups/{group_id} with expected_revision, ... | C-DC-39 | Deployment contract, API shapes |
| `add` | Group changes use PATCH /api/groups/{group_id} with expected_revision, ... | C-DC-39 | Deployment contract, API shapes |
| `remove` | Group changes use PATCH /api/groups/{group_id} with expected_revision, ... | C-DC-39 | Deployment contract, API shapes |
| `PUT /api/groups/{group_id}/messages` | Group sends use PUT /api/groups/{group_id}/messages with guid, ciphertext | C-DC-40 | Deployment contract, API shapes |
| `guid` | Group sends use PUT /api/groups/{group_id}/messages with guid, ciphertext | C-DC-40 | Deployment contract, API shapes |
| `ciphertext` | Group sends use PUT /api/groups/{group_id}/messages with guid, ciphertext | C-DC-40 | Deployment contract, API shapes |
| `POST /api/devices/link-codes` | POST /api/devices/link-codes returns code | C-DC-41 | Deployment contract, API shapes |
| `code` | POST /api/devices/link-codes returns code | C-DC-41 | Deployment contract, API shapes |
| `Authorization: Bearer <device_token>` | Device calls carry Authorization: Bearer <device_token>, account calls Authorization: ... | C-DC-42 | Deployment contract, API shapes |
| `Authorization: Bearer <access_token>` | Device calls carry Authorization: Bearer <device_token>, account calls Authorization: ... | C-DC-42 | Deployment contract, API shapes |
| `key_id` | Signed, post-quantum, one-time pre-keys each keep their own key_id space | C-DC-44 | Deployment contract, key sizes paragraph |
| `POST /api/groups` | POST /api/groups takes encrypted_state with members usernames | C-DC-45 | Deployment contract, API shapes; Core features, feature 6 rule 1 |
| `encrypted_state` | POST /api/groups takes encrypted_state with members usernames | C-DC-45 | Deployment contract, API shapes; Core features, feature 6 rule 1 |
| `members` | POST /api/groups takes encrypted_state with members usernames | C-DC-45 | Deployment contract, API shapes; Core features, feature 6 rule 1 |
| `POST /api/recovery/restore` | POST /api/recovery/restore returns recovery_blob for the right verifier | C-DC-46 | Deployment contract, API shapes |
| `recovery_blob` | POST /api/recovery/restore returns recovery_blob for the right verifier | C-DC-46 | Deployment contract, API shapes |
| `POST /api/auth/signup` | POST /api/auth/signup takes email, username, password | C-DC-47 | Deployment contract, API shapes |
| `email` | POST /api/auth/signup takes email, username, password | C-DC-47 | Deployment contract, API shapes |
| `username` | POST /api/auth/signup takes email, username, password | C-DC-47 | Deployment contract, API shapes |
| `password` | POST /api/auth/signup takes email, username, password | C-DC-47 | Deployment contract, API shapes |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced | Note |
|---|---|---|---|
| Overview | 5 | 5 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| User roles | 4 | 12 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Core features | 59 | 233 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| User flow | 8 | 18 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| UI/UX notes | 7 | 70 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Technical requirements | 6 | 44 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Data model | 4 | 27 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Front-end specification | 9 | 121 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Constraints | 0 | 13 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Deployment contract | 13 | 47 | sentences counted from instruction.md by the obligation markers, independent of the citations |
| Build plan | 0 | 0 | a build order whose outcomes restate Core features items |
| Definition of done | 0 | 0 | restates Deployment contract item 3 with Core features 1, 7, 11 and 12 |
