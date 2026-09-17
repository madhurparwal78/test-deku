# Beacon: Encrypted Messenger Platform

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open Beacon in a browser, sign up and send a message that another person reads in their own browser, without hitting an error page. The hard part cannot be arranged on screen: the Beacon service must only ever hold ciphertext. The words of a message, the bytes of an attachment and a person's profile name must never appear in anything the browser sends to the service or in any database row, and a message that only looks private because the page hides it does not count.

## Overview

Beacon is two things that share one identity. The first is a private messenger for everyday people talking with family, friends and coworkers: text, voice messages, photos, video, files, stickers, groups, and voice and video calls, where every message and every call is end-to-end encrypted so that neither the operator of the service nor anyone watching the network can read or hear the contents. The second is the marketing home: one tall, calm page that states the privacy promise, walks through the features, explains that Beacon is an independent nonprofit run by Beacon Technology Foundation, and routes a visitor toward installing Beacon or giving money to fund it. The page makes a promise ("We can't read your messages or listen to your calls") that the application is required to actually keep.

For a messenger, correctness is not "the message arrived". It is: the message arrived, was readable only by its intended recipients, could not have been silently altered, and left the service knowing as little as the design allows about who spoke to whom. Cryptographic mistakes are silent: a session with the wrong key or a skipped authentication check still sends and shows messages that look normal. Beacon delivers each message only to its intended recipients, unaltered, and tells the service as little as the design allows about who spoke to whom.

Beacon is a consumer community-social product: people talking with people through a messaging inbox. Beacon is not: an advertising product (no ads, no affiliate marketers, no trackers of any kind), a phone-number messenger (no phone numbers, no SMS, no address-book upload), a payment processor (a donation is a pledge receipted by email; no card details are ever asked for), a native app store build (the download page links out), or a service that can moderate, index or search what people say.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| visitor (no account) | read the home page and its eleven translations, open the language dialog, read every declared page, give a donation, read the terms and privacy page | **cannot open any conversation, fetch anyone's keys, send or fetch envelopes** |
| user (signed-up account) | register, link and unlink **its own** devices; publish keys, an encrypted profile and an access key; send sealed messages; fetch and acknowledge **its own device's** envelopes; create groups and send in groups it belongs to; leave a group; keep a recovery record | **cannot fetch or acknowledge another device's envelopes, cannot unlink another account's device, cannot send to another account using its own device token, cannot change a group it is not a member of** |
| group admin (the user who created a group) | add members to that group, remove any member, replace the group's encrypted state | **a group admin's powers end at that group's edge** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a user session to any group admin-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds for every "cannot" in the table: a direct call is denied and nothing it names changes.

Signup is open: anyone can create an account at `/signup`. Four seeded accounts exist so people can sign in straight away:

| Email | Username |
|---|---|
| `user@example.com` | `nova` |
| `user2@example.com` | `juniper` |
| `user3@example.com` | `sol` |
| `user4@example.com` | `wren` |

## Core features

The non-negotiable, across every surface below: the service must never possess the plaintext of any message, call, name, avatar or attachment. Privacy is not a mode a person can be in or out of; it is the only mode. Any feature that cannot be built without the service reading content is out of scope, and no path ever sends content to the service in the clear.

**At a glance.** The twelve features below, one line each:

1. Sealed delivery: a message reaches exactly the recipient's active devices, and nothing is queued when the named device set is wrong.
2. Nudge email: one contentless email when an account with nothing waiting receives something new.
3. Accounts: open sign-up, hashed passwords, and a fifteen-minute lock after five wrong passwords.
4. Devices: the first device is free; every later device needs a link code or the recovery PIN.
5. Keys: a one-time pre-key is handed out at most once, and a device may fetch 300 key bundles a minute.
6. Groups: of two changes from one revision exactly one wins, and only the admin changes other members.
7. Web client: conversations, attachments, stickers, calls, edits, archive and mute on every linked browser.
8. Failing safe: tampered, replayed, reordered and identity-changed messages are handled without trusting them.
9. Safety numbers: sixty digits, identical on both sides, changing whenever a device changes.
10. Disappearing messages and an encrypted browser store unlocked at `/unlock`.
11. Donations at `/donate`: pledges in minor units, one gift and one receipt per `Idempotency-Key`.
12. The marketing home in twelve languages, its language dialog, the `/terms` privacy table, the sitemap and robots file, and nothing loaded from another origin.

### 1. Sealed delivery to the right recipient only (the rule everything else rests on)

1. A one-to-one message to another person is sent with `PUT /api/messages/{username}` carrying the header `Unidentified-Access-Key` set to that person's access key and no `Authorization` header. The service accepts it only when the key matches; a wrong or missing key is denied and nothing is queued.
2. A send authenticated with a device token (`Authorization: Bearer <device_token>`) is accepted only when `{username}` is the caller's own account. The same send addressed to another person is denied and nothing is queued. The service is never told, for one-to-one messages, who sent them.
3. The send body is `{"messages": [{"device_id", "guid", "ciphertext"}]}` with one entry per device. It must name every active device of the recipient account exactly once, and nothing else; for a send to your own account it must name every active device except the sending device. Any mismatch is rejected as a client error whose body is `{"missing_devices": [...], "extra_devices": [...]}`, both lists of device ids in ascending order, and **nothing is queued for any device, and no email is sent**. A send to an account with no active device is rejected the same way and queues nothing.
4. Each accepted entry queues one envelope for exactly that device. `GET /api/messages` with a device token returns only the envelopes waiting for that device, oldest first. Another device of the same account, another account and a visitor never receive them. Acknowledging someone else's guid with `DELETE /api/messages/{guid}` is rejected and the envelope stays queued.
5. An envelope returned by `GET /api/messages` has exactly four fields: `guid`, `ciphertext`, `server_timestamp` (integer milliseconds since the epoch, UTC) and `group_id` (null for one-to-one messages). No field names or hints at the sender, and no stored row does either.
6. `DELETE /api/messages/{guid}` acknowledges delivery to that device: the envelope and its ciphertext are deleted outright from the database, not hidden or archived. Another device's copy of the same guid is untouched.
7. Delivery is idempotent per device and guid: resending a guid that is already queued for a device, or that device has already acknowledged, succeeds without queuing a second copy, and the recipient never receives the same guid twice. Simultaneous duplicate sends still leave one envelope.
8. Retention is bounded: undelivered messages are retained only as long as needed to deliver them, and a device holds at most 1000 waiting envelopes, even when sends arrive at the same moment. When a send would exceed that, the oldest envelopes for that device are dropped first. The queue is a relay, not an archive.
9. `ciphertext` is standard base64 (with padding) of 1 to 1048576 bytes; `guid` is a lowercase UUID string. Anything else is rejected as invalid and nothing is queued.

### 2. The contentless nudge email

1. When an accepted send queues at least one envelope for another account, and every active device of that account had no envelope waiting immediately before the send, Beacon sends one email through Mailpit (`mailpit`) to that account's email address, and to no one else: no cc, no bcc.
2. The subject is exactly `You have something waiting on Beacon` and the body is exactly `Open Beacon to read what is waiting for you.`
3. The email never contains the sender's username or email, the message, the ciphertext, the guid, a group name or a group id.
4. No nudge is sent while that account still has envelopes waiting from an earlier send, for a send to your own devices, for a rejected send, or for an idempotent resend.

### 3. Accounts and sign-in

1. `POST /api/auth/signup` with `{"email", "username", "password"}` creates an account. The username matches `^[a-z][a-z0-9_]{2,19}$`; the password has at least 12 characters; the email is a valid address. Emails and usernames are unique ignoring letter case, so `USER@example.com` cannot join beside `user@example.com`. Any invalid or duplicate signup is rejected and nothing is stored.
2. Passwords are stored only as a hash; the plaintext password never appears in any database row.
3. `POST /api/auth/login` with `{"email", "password"}` returns `{"access_token"}`, an account token. After five consecutive wrong passwords for one email, sign-in for that email is refused for fifteen minutes, even with the right password, and even when the wrong passwords arrive at the same moment.
4. An account token is accepted only by `POST /api/devices`, `POST /api/recovery/restore` and `GET /api/me`. Every other device endpoint rejects it.

### 4. Devices are first-class parties

1. `POST /api/devices` with an account token registers a device with its own keys (shapes in the Deployment contract) and returns `{"device_id", "device_token"}`. Device ids start at `1` for each account and are never reused.
2. An account with no active device registers its first device freely. After that, no device can be added without an action authenticated by an existing device, except the recovery replacement of rule 4: another device needs `"link_code"` from a code issued to that same account. Without one, registration is denied and no device is created. A code from another account, an unknown code or a used code is denied the same way, with the same refusal.
3. `POST /api/devices/link-codes` with a device token issues `{"code"}`: eight characters from `A` to `Z` and `0` to `9`, bound to that account, usable once, even when two registrations present it at the same moment.
4. A user who has lost every device can replace them all with `"replace_existing": true` together with the right recovery `"access_verifier"` (feature 7 rule 12). Every active device is revoked before the new one is created: their tokens stop working and their waiting envelopes are deleted. A wrong verifier counts as a wrong recovery guess and creates nothing; contacts then see a safety number change.
5. `GET /api/devices` lists the account's active devices; `DELETE /api/devices/{device_id}` unlinks one. An unlinked device's token is rejected everywhere, its waiting envelopes are deleted, it disappears from key bundles, and a send naming it is rejected with that id in `extra_devices`. Unlinking another account's device is denied and the device stays active.
6. Linking transfers trust, not history: a newly linked browser shows no message from before it was linked, and from that moment receives every new message in the user's conversations, including the ones the user sends from other browsers; nothing about earlier conversations is ever staged readable on the service.

### 5. Keys for starting sessions with people who are offline

1. Every device publishes an identity key, a signed pre-key, a post-quantum pre-key and up to 100 one-time pre-keys per upload. Registration without a well-formed identity key, signed pre-key or post-quantum pre-key is rejected and nothing is stored; well-formed means the key sizes in the Deployment contract, and the service does not verify signatures.
2. `GET /api/keys/{username}` with a device token returns the account's access key and one bundle per active device. Each bundle carries at most one one-time pre-key, and **a one-time pre-key is handed out at most once, ever, even when many requests arrive at the same moment**. When a device has none left, its bundle still returns with `"one_time_prekey": null` and the rest of its keys. An account that has never published a profile returns `"access_key": null`; an account with no active device returns `"devices": []`. A username with no account is rejected as a client error.
3. `POST /api/keys/one-time` adds one-time pre-keys; `GET /api/keys/count` returns how many remain for the calling device. A key id already uploaded for that device, even one already handed out, is rejected.
4. A device may make at most 300 `GET /api/keys/{username}` requests in any rolling sixty seconds; further requests are refused until the window moves on.
5. Private contact discovery is exact-username lookup: the service learns only the one username a person types, never an address book, and there is no directory of accounts.

### 6. Groups

1. `POST /api/groups` creates a group from `{"encrypted_state", "members"}` (usernames). The creator becomes a member and the only admin; revision starts at `1`. An unknown username is rejected and no group is created. Joining by invite means the admin adds the invited username.
2. `PATCH /api/groups/{group_id}` with `{"expected_revision", "encrypted_state", "add", "remove"}` succeeds only when `expected_revision` is the current revision, and the revision goes up by one. **When two changes carry the same revision at the same moment, exactly one succeeds**; the other is rejected with the current `revision` and changes nothing.
3. Only the admin may add members, remove someone else or replace the encrypted state. A member who is not the admin may send a change only to remove themselves, carrying the current `encrypted_state` unchanged; a different `encrypted_state` from them counts as a replacement, and any change other than leaving is denied and leaves the group unchanged.
4. `PUT /api/groups/{group_id}/messages` with `{"guid", "ciphertext"}` takes one ciphertext, encrypted once with the sender's group key, and queues it for every active device of every current member except the sending device. A removed member receives nothing sent after removal, and a newly added member receives nothing sent before joining. A non-member's send is denied and nothing is queued. The nudge rule of feature 2 applies to each member account.
5. Every member sees one authenticated roster, shown on the group conversation view at `/groups/{group_id}`: `GET /api/groups/{group_id}` returns the same `members`, `admins` and `revision` to every member, and is denied to anyone else.
6. The group conversation header offers a voice call and a video call to the whole group. Starting one opens the call screen naming the group, with a hang-up control, and every other member's open Beacon shows an incoming call naming the group, with answer and decline controls; the offer travels as a sealed message to each member.

### 7. The web client

1. Sign-up at `/signup` and sign-in at `/login` land on `/chats`. If this browser holds no device and the account has none, Beacon registers this browser as the first device without asking. If the account already has a device, `/link` offers two choices: enter a link code created on one of the user's own browsers, or enter the recovery PIN to replace every device.
2. Registering a device publishes the account's encrypted profile and access key with `PUT /api/profile` before the browser shows `/chats`, so the new device can be messaged at once. Replacing every device with the recovery PIN on `/link` lands on `/chats` with the contacts and settings from the recovery record restored and no earlier message shown.
3. Opening Beacon in a new tab or after a reload asks for the account password at `/unlock` before anything from this browser's store is shown, then returns to the route that was asked for; a wrong password shows an inline banner and keeps the store locked.
4. `/chats` is the conversation list: each row shows the other person's name, the time of the last message, a preview of the last message and the number of unread messages. `New chat` opens a dialog that starts a conversation with an exact username, and a username with no account shows an inline banner in the dialog saying so and opens nothing; `New group` opens a dialog that creates a group from a name and usernames, then opens that group at `/groups/{group_id}`.
5. `/chats/{username}` is the conversation view: a scrollback of messages oldest to newest, each outgoing message carrying its delivery state, one of `Sending`, `Sent`, `Delivered`, `Read`. `Sent` means the service accepted it; `Delivered` means a recipient device decrypted it; `Read` means it was shown on a recipient's screen. Delivery and read receipts travel as sealed messages, so the service never learns them.
6. New messages, receipts and calls appear within five seconds, without reloading, while `/chats` or a conversation is open. The browser learns of new envelopes only by requesting `GET /api/messages` (a query string is allowed), never through a push channel.
7. The composer sends text, photos, video, files (a chosen file goes when Send is pressed), voice messages recorded with the microphone, and stickers from Beacon's built-in pack of six: `Wave`, `Heart`, `Thumbs Up`, `Laugh`, `Party` and `Beacon Light`. Attachments travel inside the sealed message itself, so their bytes never reach the service readable.
8. A user can edit or delete their own message, and archive or mute a conversation from its header. Deleting asks for confirmation first. Archiving removes the conversation's row from `/chats` on every one of the user's browsers; muting marks the row as muted. Each of these, like reads and timer changes, converges on every one of the user's linked devices, and an edit also reaches the other people in the conversation.
9. The conversation header offers a voice call and a video call. Starting one opens the call screen naming the other person, with a hang-up control; the call screen opens at once, before and regardless of microphone or camera access, and a media failure shows inside the call screen. The other person's open Beacon shows an incoming call naming the caller, with answer and decline controls; declining, or hanging up on either side, closes both call screens within five seconds. Call offers and answers travel as sealed messages and media flows directly between the two browsers.
10. `/settings/profile` sets a profile name that contacts see in their conversation headers, read with `GET /api/profile/{username}`. The name is encrypted before it leaves the browser; the service stores only `profile_ciphertext` and the access key.
11. `/settings/devices` lists linked devices, issues a link code and unlinks a device; signing out asks for confirmation, unlinks this browser and wipes what it stored.
12. `/settings/recovery` sets a recovery PIN of six or more digits and confirms with `Recovery PIN saved`. The browser derives, from the PIN, a key that encrypts a recovery record (contacts and settings) and a separate `access_verifier`; the browser saves both with `PUT /api/recovery`, and the service stores the encrypted record and cannot read it. `POST /api/recovery/restore` returns the record for the right verifier; each wrong one is refused with `remaining_guesses`; after ten consecutive wrong guesses the record is destroyed and even the right verifier is refused from then on, and simultaneous wrong guesses never buy more than ten. A right guess resets the count. This environment offers no secure hardware to hold the limit beyond the service's reach, so the service holds it with the strongest guarantee available here: the count survives restarts and holds under simultaneous guesses.

### 8. Failing safe: what the client must do when something is wrong

When something is wrong, Beacon's client behaves as follows.

1. **Tampered.** A message whose ciphertext was changed in any way fails authentication. It is dropped (acknowledged and discarded), never shown, and `/chats` shows the notice `A message could not be verified and was not shown`.
2. **Replayed.** A second copy of a message already received, even under a new guid, is not shown again: the message appears once.
3. **Ordering and gaps.** Delivery tolerates out-of-order arrival and missed messages: messages arriving in a different order, or with a gap where one arrives long after later ones, all decrypt and appear in the order the sender wrote them. Later messages show as soon as they decrypt, and a late message takes its written position when it arrives.
4. **Unique keys.** The same text sent twice in one conversation produces two different `ciphertext` values, and no two envelopes a client sends ever carry the same ciphertext.
5. **No downgrade.** When a session cannot be established (for example, the recipient has no device), the message stays `Sending`, an inline banner names the failure, and no request carries the text.
6. **Changed identity.** When a contact's identity keys change (a new, linked, unlinked or replaced device), the conversation shows a warning banner and sending stays blocked until the user gives explicit acceptance of the change.

### 9. Safety numbers

1. `/chats/{username}/safety` shows a safety number: sixty digits in twelve groups of five, computed in the browser from the identity keys of every active device of both accounts.
2. Two people looking at each other's safety number see exactly the same sixty digits.
3. The safety number changes whenever either side's identity keys change.

### 10. Disappearing messages and the local store

1. Each conversation has a disappearing-message timer: off, 30 seconds, 5 minutes, 1 hour, 1 day or 1 week. Changing it applies on every participant's devices, sealed like any other message, and the conversation header shows the timer while one is set.
2. With a timer set, a message is deleted from every participant's devices when its time runs out: for the sender from when it was sent, for a recipient from when it was first shown.
3. Each browser keeps its own conversations, messages, unread counts, contacts and settings between visits, so after a reload or in a new tab (once unlocked) `/chats` and every conversation show what they showed before. What Beacon keeps in this browser's storage holds no readable message text, attachment bytes or profile names; it is encrypted under a key that only the account password unlocks.

### 11. Donations

1. `/donate` offers `$5`, `$10`, `$25`, `$50` and `$100`, a custom amount in dollars, and an email field; no card details are asked for. Giving is a pledge recorded by Beacon Technology Foundation. A recorded gift shows the inline banner `Thank you. Your gift of $25.00 was received.` with its own amount in place of `$25.00`.
2. `POST /api/donations` takes `{"amount_minor", "currency", "email"}` with an `Idempotency-Key` header (8 to 64 characters from letters, digits, `_` and `-`). `amount_minor` is an integer from `100` to `1000000` (`$25.00` is `2500`, not `25`, not `25.00`); `currency` is exactly `usd`. It returns `{"amount_minor", "currency", "status": "received"}`.
3. A missing key, a non-integer or out-of-range amount, any other currency or an invalid email is rejected, stores nothing and sends no email. The form shows the refusal inline in `donate-error`, naming the field, never through the browser's own validation bubble.
4. Repeating a request with the same `Idempotency-Key` and the same body returns the same gift and stores nothing new, even when the repeats arrive at the same moment; the same key with a different body is rejected.
5. Each recorded gift sends exactly one receipt email to the donor, and to no one else: subject exactly `Thank you for supporting Beacon`; body names the amount written like `$25.00` and names Beacon Technology Foundation.

### 12. The marketing home, its languages and its pages

1. `/` serves the English home as a complete document: the HTML response itself, before any script runs, already carries the headline `Speak Freely`, the hero lead, the `Get Beacon` button and `lang="en"` on the root element.
2. `/af`, `/ar`, `/az`, `/bg`, `/bn`, `/bs`, `/ca`, `/cs`, `/da`, `/de` and `/el` serve the same page translated into Afrikaans, Arabic, Azerbaijani, Bulgarian, Bengali, Bosnian, Catalan, Czech, Danish, German and Greek, each also complete before any script runs, each declaring its own language code on the root element; `/ar` also declares `dir="rtl"`. A locale is a path prefix over one page, never a separate page design.
3. The top bar's language control shows a globe and the current language's own name (`English` on `/`, `Deutsch` on `/de`). It opens a dialog titled `Select your language` that lists English, Afrikaans, العربية, Azərbaycan dili, Български, বাংলা, Bosanski, Català, Čeština, Dansk, Deutsch and Ελληνικά, each a link to its route. The dialog keeps keyboard focus inside itself while open; Escape or its close control closes it and returns focus to the language control.
4. Loading any marketing page requests nothing from any other origin: fonts, styles, scripts and images are all served by Beacon itself, and no analytics, advertising or tracking request is ever made.
5. The declared pages `/get`, `/help`, `/blog`, `/developers`, `/careers` and `/brand` each render Beacon's top bar and footer around their own heading and a short paragraph; `/get` offers the Android, iPhone and iPad store listings and the Windows, Mac and Linux downloads.
6. A privacy page at `/terms` is linked from the footer of the home, each translation, `/get`, `/help`, `/blog`, `/developers`, `/careers`, `/donate`, `/terms` and `/brand` (reading `Terms & Privacy Policy` on the English pages). It states what the Beacon service holds and never holds, carrying the table in the Front-end specification word for word.
7. `/sitemap.xml` lists every public route as an absolute address built from `APP_PUBLIC_URL`: the home, its eleven translations, `/get`, `/help`, `/blog`, `/developers`, `/careers`, `/donate`, `/terms` and `/brand`, and nothing else (no sign-in or signed-in route). `/robots.txt` carries a `Sitemap:` line pointing at it.

## User flow

Beacon's information architecture is one marketing page served at the site root and at eleven language prefixes, a handful of declared pages, and the signed-in messenger.

**Journeys.**

1. A visitor opens `/`, reads `Speak Freely`, scrolls past `Why use Beacon?`, `Share Without Insecurity`, the four feature cards, `No ads. No trackers. No kidding.` and `Free for Everyone`, and reaches the dark footer.
2. A visitor opens the language control, sees `Select your language`, chooses `Deutsch`, and lands on `/de` with the control reading `Deutsch`.
3. A visitor opens `/donate`, chooses `$25`, enters an email, presses Donate, and sees an inline banner reading `Thank you. Your gift of $25.00 was received.` while the receipt arrives in their inbox.
4. A user signs in at `/login` as `user@example.com`, lands on `/chats` showing `No conversations yet`, opens `/settings/devices`, sees this browser as the one linked device, creates a link code, and saves a recovery PIN at `/settings/recovery`.
5. After journey 4 has registered `nova`'s browser, a user signs in as `user2@example.com`, opens New chat, enters `nova`, sends `Hello from Juniper`, and sees the bubble reach `Sent`; back on `/chats`, the row for `nova` previews `Hello from Juniper`.
6. After journey 4, a user signs in as `user3@example.com`, opens `/chats/nova`, opens the safety number and sees sixty digits in twelve groups, then sets the disappearing-message timer to 1 hour and sees the timer in the conversation header.
7. After journey 4, a user signs in as `user4@example.com`, creates the group `Weekend Hike` with `nova`, sees two members, sends a sticker, starts a voice call from the group header and sees the call screen, starts a video call from `/chats/nova`, then signs out from `/settings/devices`.
8. A user who already uses Beacon signs in on a second browser, lands on `/link`, enters a code created on their first browser, and from then on sees new messages on both browsers, including the ones they send from either.

**States.** Every list has an empty state (`No conversations yet` on `/chats`); every page shows a loading state while it waits; every failed request shows an inline banner that says what went wrong; no error ever leaves a blank or broken page.

| Route | Purpose | Auth |
|---|---|---|
| `/` | English marketing home | none |
| `/{locale}` | the home in one of the eleven languages: `af`, `ar` (right to left), `az`, `bg`, `bn`, `bs`, `ca`, `cs`, `da`, `de`, `el` | none |
| `/get` `/help` `/blog` `/developers` `/careers` `/brand` | declared pages: download and install, support centre, news and announcements, technical and integration documentation, open roles at the nonprofit, brand and press assets | none |
| `/donate` | donation form | none |
| `/terms` | terms and privacy page | none |
| `/sitemap.xml` | sitemap of public routes | none |
| `/robots.txt` | robots file naming the sitemap | none |
| `/signup` | create an account | none |
| `/login` | sign in | none |
| `/unlock` | unlock this browser with the account password | browser holds a device |
| `/link` | link this browser with a code, or replace every device with the recovery PIN | signed in, account already has a device |
| `/chats` | conversation list with new chat and new group dialogs | device |
| `/chats/{username}` | conversation view, composer, call buttons, timer, archive and mute | device |
| `/chats/{username}/safety` | safety number with that person | device |
| `/groups/{group_id}` | group conversation view with its members, call buttons and timer | device, member |
| `/settings/profile` | profile name | device |
| `/settings/devices` | linked devices, link code, unlink, sign out | device |
| `/settings/recovery` | recovery PIN | device |

**Entry and redirects.** Opening any device route without a signed-in browser redirects to `/login`. Sign-in lands on `/chats`, on `/link` when the account already has a device and this browser is not one of them, or on `/unlock` when this browser's store is locked. A browser whose device was unlinked or replaced elsewhere wipes its store and returns to `/login` with the banner `This browser was unlinked`. A user opening a group they do not belong to sees `This group is not available` with a way back to `/chats`. Signing out returns to `/login`.

## UI/UX notes

**At a glance.** Calm and trustworthy, with the promise seen first. Vivid blue only on what a person can act on, on the wordmark and on outgoing bubbles, near-black ink on near-white grounds, a dark footer. Every control shows its states and every action gets inline feedback. One clear primary action per page. Light design with only a readable dark courtesy layer. Inter throughout. Soft cards, generous marketing spacing, a comfortable messenger. WCAG AA contrast, keyboard reach and text alternatives. One shared short transition and three utility animations, stopped under reduced motion. One column on a phone, paired cards on a tablet, a split hero on a laptop.

**North star.** A visitor should understand in the first moment that Beacon is trustworthy because it is calm. **Register.** Consumer: the marketing home may carry atmosphere, with the promise itself seen first; the messenger is a quiet working surface built for reading and replying. The restraint is the brand: a product whose entire pitch is trust does not perform tricks at you, so there is no scroll-scrubbed animation, no runtime motion graphics driving the layout and no dark hero video.

**Palette by role, carried in words.** Primary text is a near-black neutral ink, and the dominant pairing is that ink on a near-white neutral ground. The page and card ground is a near-white neutral (pure white); alternating section grounds are three barely different near-white neutrals; the band behind the feature cards is a pale near-white neutral grey. Muted secondary paragraphs use a deep cool neutral. The neutral scale for borders, dividers and unavailable states runs mid cool neutral, light cool neutral and near-white cool neutral. The wordmark, in-text links, the filled `Get Beacon` button (moving to the interactive blue on hover) and outgoing message bubbles use the brand blue, a light, vivid blue; the top bar's links, its `Get Beacon` link included, rest in the ink and move to the interactive blue, a second light, vivid blue, on hover and focus; pressed states and gradient stops use two mid, vivid blues. The vivid blues appear only on things a person can act on, on the wordmark and on outgoing bubbles, so vivid blue means "you can act here"; the soft periwinkle of the hero ground and the gradient stops inside drawings are the only other blues. The hero band is a light periwinkle, a light, soft blue close to a near-white cool neutral. The footer and deep panels use deep cool neutrals and near-black neutrals, with near-white text. Illustrations add a soft teal panel, a violet (purple) accent and a pale teal band, and nothing else. Failure uses one deep red that appears nowhere else; success one deep green; the changed-identity warning one deep amber, always beside its words; in-progress the mid cool neutral with the pulse. The exact shades are yours so long as every role above keeps its word and its exclusivity.

**Components and states.** Every control has resting, pointed-at, pressed, focused and unavailable states; unavailable is never signalled by colour alone. Links carry an underline on hover and focus, so colour is never the only cue that something is interactive. Dialogs close on Escape and return focus to what opened them. Destructive actions (deleting a message, unlinking a device, replacing every device, signing out) confirm first. Feedback is an inline banner in the place where the action happened. In a conversation, outgoing message bubbles sit on one side in the brand blue and incoming bubbles on the other side in a near-white neutral, the same pairing the hero's chat phone shows.

**Primary action.** Every page is led by a single primary action that outranks everything else on it: `Get Beacon` on the home, Donate on `/donate`, Send in a conversation.

**Mode.** Light, designed fully. The product respects a dark preference only as a thin courtesy layer that keeps text readable; it never ships a parallel dark palette.

**Type.** One family does all the work: `Inter`, with the system fallback stack named in the Front-end specification, in four weights: extrabold for the hero and section headings, semibold for card titles and buttons, medium for occasional emphasis, regular for reading. Figures align wherever amounts or times stack. The exact sizes and line heights are fixed in the Front-end specification. Inter reads as friendly and neutral, never technical. Captions, such as message times, use the dense body size.

**Shape and density.** Boxes, media and phone frames have gently rounded corners; buttons and the menu button round less; the language dialog's close control is a full pill. Cards float on a very soft double shadow, like paper laid on a table; buttons carry a lighter one; the sticky top bar gains a soft shadow only once the page has scrolled. Spacing is generous on the marketing home, where sections read as separate at a glance without dividing lines, and comfortable in the messenger, where a full screen of conversation fits without crowding.

**Accessibility floor.** Body text and its background meet the WCAG AA contrast bar on white, on the pale grey feature field and in the near-white footer text on its near-black ground; the interactive blue meets it too, and under a dark preference text and its background still meet it (the ratio is in the Front-end specification). Keyboard navigation reaches every link, the language control, the dialog and every button in a logical order with a visible focus ring. Touch targets are comfortably sized for a fingertip, with the minimum in the Front-end specification. The wordmark, the globe control, the menu button and every icon-only control carry text alternatives. Each phone render carries alternative text that describes what it shows, while the feature card illustrations, the band drawings and the details inside the phone screens are ornamental and marked decorative. Every document declares its language.

**Motion.** Motion is almost entirely restraint. Every interactive colour change uses one shared, short transition: the text and border of the primary get link, the language selector and the underline borders slide from ink to the interactive blue smoothly rather than snapping, and the background stays transparent throughout. Cards add a matching fade and lift. One gentle, symmetric ease exists and is used once, on the attention pulse. Beyond that there are only three honest utility animations: a spinner that turns while something loads, a soft attention pulse, and an indeterminate progress shimmer. Under a reduced-motion preference every transition and animation stops.

**Responsive.** The page reflows at every width between the named tiers. On a narrow viewport (a phone) it is a single column, the top bar's links tuck behind a three-line menu button, and the two phones stack under the hero words with the headline shrinking to its mobile size. On a tablet the feature cards pair up two by two with links inline. On a laptop the hero splits into words on the left and phones on the right with the four cards in two rows; on a widescreen the container widens; on the widest screens the content stops stretching and centres with generous margins. Nothing ever scrolls sideways, and the vertical scrollbar is always present so the layout never shifts as it appears.

**What it must not look like.** No page dominated by a single hue family with no second signal; no decoration standing in for content; no dark, cinematic hero; no marketing composition where the working messenger belongs.

## Technical requirements

**Stack.** The server is **Fastify** on Node.js 20; the web client is **Preact + Vite**. Rendering: the marketing routes (the home, its eleven translations, the declared pages, `/donate` and `/terms`) are rendered at build time into complete HTML documents that the browser receives ready to read and then hydrates; the signed-in messenger routes are a client-rendered single-page app that talks JSON to the API on the same origin under `/api`.

Libraries:

| Concern | Library |
|---|---|
| HTTP server and static files | `fastify`, `@fastify/static` |
| PostgreSQL client | `pg` |
| SMTP | `nodemailer` |
| Password hashing | `bcryptjs` |
| UI, routing, build | `preact`, `preact-iso`, `vite`, `preact-render-to-string` |
| Cryptographic primitives (X25519, Ed25519, XChaCha20-Poly1305, BLAKE2b, Argon2id) | `libsodium-wrappers-sumo` |
| Post-quantum key encapsulation (ML-KEM-768) | `@noble/post-quantum` |
| Browser storage | `idb` |
| Inter font files | `@fontsource/inter` |

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL (`postgres`) at `DATABASE_URL` and Mailpit (`mailpit`) at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`, and reaching for anything else is a contract violation.

**Environment.** Read `DATABASE_URL`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` from the environment; never hardcode a host, port or credential. Mail goes from `Beacon <no-reply@beacon.example.org>`.

**Cryptography.** All cryptography comes from vetted, published constructions in `libsodium-wrappers-sumo` and `@noble/post-quantum`; Beacon invents no cipher, curve or construction of its own. New conversations establish shared secrets through an authenticated key agreement that binds each party's identity key to the session and mixes in the recipient's signed pre-key, a one-time pre-key when one is available, and a post-quantum key encapsulation against the recipient's post-quantum pre-key, so traffic recorded today cannot be decrypted later by someone who stores it and waits. That is Beacon's post-quantum readiness: the key-agreement layer is constructed as a hybrid of the classical agreement and the post-quantum key encapsulation. Every message of every type (text, attachment, receipt, edit, delete, timer change, call signalling, sync record, group key) is sealed with authenticated encryption under a message key and nonce used exactly once, derived from a chain that advances and forgets with each message, so compromising today's keys reveals nothing about earlier messages, and fresh key agreement mixed in as the conversation continues heals the session after a compromise. The associated data binds sender and recipient identity so a captured message cannot be replayed into another conversation. The sender's identity travels inside the sealed envelope, proven to the recipient and not to the service. Group messages use a sender key that each sender distributes over the pairwise sessions, rotated whenever a member is removed so the departed member cannot read anything sent afterwards, and never handed to a new member for earlier messages; a membership change in a large group never stalls sending for everyone else. Sync records that carry reads, deletes, edits, archive and mute settings, timer changes and profile changes between a user's own devices are encrypted to those devices, and concurrent changes resolve the same way everywhere.

**Key material.** The service distributes public key material only and never holds a private key, and no limit on Beacon ever needs to know who is messaging whom.

**Secrets on the server.** Token hashes, access keys, link codes and recovery verifiers are compared in constant time, and every wrong guess of the same kind receives the same refusal.

**Responsiveness of the client.** Encryption, decryption, session setup, ratchet steps and group re-keying run in a Web Worker, so typing in the composer and scrolling the conversation never stall, even while a backlog decrypts.

**Performance of the home.** The headline, the lead and the primary button are in the first HTML response, so they arrive before the phone renders and illustrations draw. The four Inter weights (400, 500, 600 and 800) are self-hosted and declared with `font-display: swap`, so text renders at once in a system face while Inter loads. The phone renders and illustrations reserve their space before they draw, so nothing on the page moves as they appear, and Beacon ships no image binaries for the first screen to wait on. Weight discipline: the heavy payload of a page like this is imagery and fonts rather than code, so large illustrations are sized in advance and drawn lazily below the fold, never holding the hero hostage.

**Module and component architecture.** Beacon's parts are these; the names describe responsibilities, not required file or module names, and the file layout is yours. Marketing front: ChromeBar (the sticky top bar with its collapse), LanguageModal, Hero (headline, lead, primary button, the two tilted phones), FeatureCard (four instances), ClaimBand (the full-width statement bands) and SiteFooter. Application core, each defined by what it must do: SessionEngine (key agreement and per-message ratchet), GroupKeyService (sender keys and re-keying), DeviceLinker (linking and revocation), SyncLog (encrypted, convergent state between a user's own devices), Transport (pre-key fetch, sealed queue, acknowledgement, the contentless nudge), Envelope (sealed sender and metadata minimisation), Identity (registration, usernames, safety numbers, the key-change warning), Recovery (the recovery record) and LocalStore (the encrypted message store in the browser and disappearing-message timers). No part ever exposes plaintext to the transport or the service.

**Health.** `GET /api/health` returns `200` once the database is reachable.

## Data model

Eleven tables in PostgreSQL, in the `public` schema. All timestamps are UTC. Money is integer minor units with the lowercase currency `usd`.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in, one line per seeded account in exactly this form: `email: user@example.com password: deku-demo-pw-2026`, likewise for `user2@example.com`, `user3@example.com` and `user4@example.com`.

- **accounts**: `id`, `email` (unique ignoring case), `username` (unique ignoring case), `password_hash`, `failed_sign_ins`, `locked_until`, `created_at`.
- **devices**: `id`, `account_id`, `device_id` (per account, from 1, never reused; unique with `account_id`), `identity_key`, `signed_prekey_id`, `signed_prekey_public`, `signed_prekey_signature`, `pq_prekey_id`, `pq_prekey_public`, `pq_prekey_signature`, `token_hash`, `revoked_at`, `created_at`.
- **one_time_prekeys**: `id`, `device_ref`, `key_id` (unique per device, even after hand-out), `public_key`, `handed_out_at`.
- **link_codes**: `id`, `account_id`, `code` (unique), `issued_by_device`, `used_at`.
- **profiles**: `account_id` (one row per account), `profile_ciphertext`, `access_key`.
- **envelopes**: `id`, `recipient_device`, `guid` (unique per recipient device), `ciphertext`, `group_id`, `server_timestamp`. There is no sender column.
- **acknowledged_guids**: `recipient_device`, `guid` (unique pair). The guid alone, never the ciphertext.
- **groups**: `id`, `revision`, `encrypted_state`, `created_at`.
- **group_members**: `group_id`, `account_id` (unique pair), `is_admin`.
- **recovery_records**: `account_id` (one per account), `recovery_blob`, `access_verifier`, `failed_guesses`.
- **donations**: `id`, `amount_minor`, `currency`, `email`, `idempotency_key` (unique), `request_fingerprint`, `created_at`.

The invariants these tables carry are observable rules, stated in Core features, and each holds when requests arrive at the same moment: a one-time pre-key is handed out at most once; a guid is queued at most once per device, including after acknowledgement; of two group changes from the same revision exactly one is applied; one `Idempotency-Key` records at most one gift; a send with a mismatched device set leaves no envelope at all; a device never holds more than 1000 waiting envelopes; a link code admits exactly one device; ten wrong recovery verifiers destroy the record; five wrong passwords lock the email.

Derived, not stored: the number of remaining one-time pre-keys (counted), group member counts (counted), and everything the service must never know: unread counts, previews, delivery states, safety numbers and profile names, all computed in the browser.

No row in any table holds a readable message, attachment, profile name, contact list or sender: the database holds only ciphertext, queue timing and the routing the API shapes name, so a stolen database reveals only ciphertext.

**Seed data.** The four accounts in User roles, each with no device, no profile, no group and no donation (device keys can only be made in a browser). Seeding must be idempotent: restarting the app must not duplicate rows. The delivered app holds the four seeded accounts exactly as seeded, with no device, profile, recovery record, group, waiting envelope or sign-in lock.

## Front-end specification

### Type scale

The full font stack is `Inter, SF Pro, Segoe UI, Roboto, Oxygen, Ubuntu, Helvetica Neue, Helvetica, Arial, sans-serif`. The monospace stack for inline code, not used on the home page, is `Inconsolata, Hack, SF Mono, Roboto Mono, Source Code Pro, Ubuntu Mono, monospace`. Body text is `1em` with line height `1.5`, weight 400 and `optimizeLegibility` rendering.

| Size | Weight | Line height | Role |
|---|---|---|---|
| 60px | 800 | 64px | hero headline on desktop |
| 40px | 800 | 44px | section headings |
| 28px | 800 | 32px | sub-section headings (none on the home) and the hero headline on a phone |
| 24px | 400 | 24px | large lead (none on the home) |
| 20px | 600 | 28px | card titles |
| 20px | 400 | 28px | lead paragraph |
| 16px | 600 | 22px | buttons and strong labels |
| 16px | 400 | 24px | body paragraphs |
| 16px | 400 | 22px | dense body text |

### Global chrome

The top bar is sticky at the top of the window, carries the id `brandNavbar` (reachable as `#brandNavbar`), has a white ground, shows the wordmark on the left and, on the right, the links `Get Beacon`, `Help`, `Blog`, `Developers`, `Careers` and `Donate` in that order, followed by the language control. It sits above the page, and the open language dialog sits above it. The hero's filled `Get Beacon` button carries the class `get-app` (reachable as `.get-app`).

The footer is a near-black band holding the copyright, trademark and media lines on the left and four link columns:

| Column | Items |
|---|---|
| Organization | `Donate`, `Careers`, `Blog`, `Brand Assets`, `Terms & Privacy Policy` |
| Download | `Android`, `iPhone & iPad`, `Windows`, `Mac`, `Linux` |
| Social | `Bluesky`, `GitHub`, `Instagram`, `Mastodon`, `X` |
| Help | `Support Center`, `Community` |

The language dialog is a centred card over a dimmed, mostly opaque near-black scrim, titled `Select your language`, listing the twelve language names as links, with a pill-shaped close control at its top corner; its header rounds its top corners and its footer its bottom corners, and the card carries a soft shadow with a hairline edge.

### Iconography, drawn from text

- **Menu button (the burger), drawn as geometry.** Three thin rounded bars of equal width, evenly spaced, stacked and centred in a square tap target with softly rounded corners, in the brand blue; it appears only on narrow viewports.
- **Globe.** A circle outline with two curved meridians and two latitude lines, single stroke, no fill, inheriting the current text colour so it turns blue on hover with its label.
- **Wordmark.** The word `Beacon` in Inter 800 in the brand blue, with a circular speech-bubble glyph to its left drawn as a ring with a small tail.

### The home, top to bottom

1. **Hero.** A light periwinkle band. On the left, the headline `Speak Freely` (hero headline size), the lead beneath it (lead paragraph size), and the filled `Get Beacon` button (button size). On the right, two phone renders overlapping, each carrying `data-testid="hero-phone"` on the element that is rotated, each tilted 22.5 degrees clockwise (the transform `matrix(0.92388, 0.382683, -0.382683, 0.92388, 0, 0)`). Each phone render carries alternative text describing its screen. One phone shows a group video call as a grid of faces; the other shows a one-to-one chat with text bubbles, a voice message with a waveform, and a disappearing-message timer. On a phone the phones stack below the copy.
2. **Why band.** The centred heading `Why use Beacon?` (section heading size) with its one-line lead (lead paragraph size).
3. **Privacy statement.** `Share Without Insecurity` (section heading size) and its body, beside an illustration of a chat bubble reading `Hey check this out!` on a soft teal panel.
4. **Feature grid.** Four white cards on the pale grey field, each a small illustration (carrying `data-testid="feature-illustration"` and marked decorative) over a title (card title size) and two lines of body paragraph size: `Say Anything` (text, voice messages, photos, video, GIFs and files over data, avoiding carrier fees), `Speak Freely` (crystal-clear voice and video calls at any distance), `Make Privacy Stick` (encrypted stickers, and packs you create and share), `Get Together with Groups` (group chats for family, friends and coworkers).
5. **No-tracking band.** A left-aligned heading `No ads. No trackers. No kidding.` (section heading size), a short paragraph, and a violet illustration of a struck-through browser window.
6. **Nonprofit band.** A pale teal band with a halftone globe wreathed in speech bubbles on the left and, on the right, the heading `Free for Everyone` (section heading size), the nonprofit statement and an outline `Donate to Beacon` button that opens `/donate`.

### Responsive tiers

| Tier | Width | Layout |
|---|---|---|
| phone | up to 768 CSS pixels | single column; top bar links behind the menu button; hero words over stacked phones; hero headline at its phone size |
| tablet | 769 to 1023 CSS pixels | feature cards two by two; top bar links inline |
| laptop | 1024 to 1215 CSS pixels | hero words left, phones right; the four cards in two rows |
| widescreen | 1216 to 1407 CSS pixels | wider container with more gutter |
| full HD | 1408 CSS pixels and up | container stops widening and centres with generous margins |

The page never narrows below 300 CSS pixels of body width.

### Accessibility values

Body text and its background: a contrast ratio of at least 4.5:1, in both colour preferences. Touch targets: at least 44 by 44 CSS pixels.

### Motion names

The three utility animations are named `spinAround` (the loading spinner turning a full circle), `pulsate` (a soft attention pulse that dims to half opacity midway) and `moveIndeterminate` (the indeterminate progress bar's shimmer sliding across).

### Zero-asset substitution guide

Every picture is drawn from text; the build ships no logo, illustration, phone picture or font file of its own design. These substitutions also settle the design's evidence gaps: the exact hero shade, the globe and the wordmark are reconstructions within the palette, while the burger is carried exactly by its described geometry of three equal rounded bars.

- **Phone renders.** Two device frames, rounded rectangles filled as dark screens, keeping the tilt, which is the most recognisable gesture of the hero. The call phone holds a grid of rounded tiles filled with seeded gradient placeholders standing in for faces. The chat phone holds rounded bubbles alternating the brand blue for outgoing and a near-white neutral for incoming, plus a waveform row drawn as vertical bars of varying height.
- **Feature and band illustrations.** Flat vector compositions in the palette: rounded rectangles, circles and simple paths. The halftone globe is a circle filled with a tiled grid of small dots over the pale teal, with three rounded speech bubbles above it. The struck-through browser is a stack of offset rectangles with a heavy circle and a diagonal bar across them.
- **Seeded photographic placeholders.** Wherever a face or avatar appears (the call grid, the chat avatar), a canvas draws a soft radial or linear gradient between two palette colours from a seed, one seed per slot, so each stands in for a distinct person and the layout stays stable between builds.
- **Stickers.** The six built-in stickers are drawn from text in the palette, each a simple picture of its name: a waving hand for `Wave`, a heart for `Heart`, a raised thumb for `Thumbs Up`, a laughing face for `Laugh`, a party popper for `Party` and the wordmark's ring glowing like a lamp for `Beacon Light`.
- **Fonts.** `Inter` is an open font, self-hosted and loaded with swap, using the stack above while it loads.

### Machine-readable hooks

These `data-testid` values are part of the product and take exactly these names.

| Hook | Element |
|---|---|
| `language-control` | the top bar's language button |
| `language-dialog` | the language dialog, with `role="dialog"` and `aria-modal="true"` |
| `menu-button` | the narrow-viewport menu button, with `aria-expanded` |
| `hero-phone` | each rotated phone render |
| `feature-illustration` | each feature card illustration |
| `donate-amount` | each preset amount button, carrying `data-amount-minor` (`500`, `1000`, `2500`, `5000`, `10000`) |
| `donate-custom-amount` | the custom amount field, in dollars |
| `donate-email` | the donor email field |
| `donate-submit` | the Donate button |
| `donate-confirmation` | the inline banner after a recorded gift |
| `donate-error` | the inline refusal naming the field |
| `signup-email`, `signup-username`, `signup-password`, `signup-submit` | the sign-up form |
| `login-email`, `login-password`, `login-submit` | the sign-in form |
| `unlock-password`, `unlock-submit` | the unlock form |
| `link-code-input`, `link-code-submit` | entering a link code on `/link` |
| `recovery-replace-pin`, `recovery-replace-submit`, `recovery-replace-confirm` | replacing every device with the recovery PIN on `/link`, and its confirmation |
| `new-chat`, `new-chat-username`, `new-chat-start` | the new chat dialog |
| `new-group`, `new-group-name`, `new-group-members`, `new-group-create` | the new group dialog; members are comma-separated usernames |
| `conversation-row` | each row on `/chats`, carrying `data-username` (or `data-group-id` for a group), and `data-muted="true"` while the conversation is muted |
| `unread-count` | the unread number inside a row |
| `conversation-title` | the conversation header's name: the contact's profile name once known, else the username |
| `conversation-archive`, `conversation-mute` | the header's archive and mute controls |
| `message-bubble` | each message, carrying `data-direction` of `in` or `out` |
| `message-text` | the text inside a bubble |
| `message-status` | an outgoing bubble's state text: `Sending`, `Sent`, `Delivered` or `Read` |
| `message-edit`, `message-edit-input`, `message-edit-save` | editing an outgoing message; `message-edit` sits inside its `message-bubble` and may appear when the bubble is pointed at |
| `message-delete`, `message-delete-confirm` | deleting an outgoing message, and its confirmation; `message-delete` sits inside its `message-bubble` and may appear when the bubble is pointed at |
| `message-image`, `message-video`, `message-file`, `message-voice`, `message-sticker` | an attachment inside a bubble; `message-file` shows the file name, and `message-sticker` carries the sticker's name as its accessible name |
| `decrypt-error-notice` | the notice on `/chats` reading `A message could not be verified and was not shown` |
| `composer-input`, `composer-send` | the composer text field and Send button |
| `composer-attach` | the file input for photos, video and files |
| `composer-voice` | start, then stop and send, a voice message |
| `composer-sticker`, `sticker-option` | the sticker picker and each built-in sticker, whose accessible name is the sticker's name |
| `call-voice`, `call-video`, `call-screen`, `call-hang-up` | call controls and the call screen |
| `call-incoming`, `call-answer`, `call-decline` | the incoming call shown to the person being called |
| `safety-number-link`, `safety-number` | the link to and the display of the safety number, as twelve groups of five digits separated by spaces |
| `identity-change-banner`, `identity-change-accept` | the changed-identity warning and its accept control |
| `disappearing-timer` | the timer select, with option values `off`, `30s`, `5m`, `1h`, `1d`, `1w` |
| `group-members` | the member list in a group conversation |
| `profile-name-input`, `profile-save` | the profile form |
| `device-row`, `link-code-create`, `link-code-value`, `device-unlink`, `device-unlink-confirm`, `sign-out`, `sign-out-confirm` | the devices page; each `device-row` carries `data-device-id` and holds its own `device-unlink`, and unlinking asks for confirmation first |
| `recovery-pin-input`, `recovery-save` | the recovery form |

### Copy deck

Every string below appears on the English home exactly as written (straight or typographic quotation marks both acceptable, but only plain hyphens, never typographic dashes).

- Top bar links: `Get Beacon`, `Help`, `Blog`, `Developers`, `Careers`, `Donate`. Language control: `English`. Dialog title: `Select your language`.
- Hero headline: `Speak Freely`. Lead: `Say "hello" to a different messaging experience. An unexpected focus on privacy, combined with all of the features you expect.` Button: `Get Beacon`.
- Why band heading: `Why use Beacon?` Lead: `Explore below to see why Beacon is a simple, powerful, and secure messenger`
- Privacy statement heading: `Share Without Insecurity`. Body: `State-of-the-art end-to-end encryption (powered by the open source Beacon Protocol) keeps your conversations secure. We can't read your messages or listen to your calls, and no one else can either. Privacy isn't an optional mode. It's just the way that Beacon works. Every message, every call, every time.`
- Card `Say Anything`: `Share text, voice messages, photos, videos, GIFs and files for free. Beacon uses your phone's data connection so you can avoid SMS and MMS fees.`
- Card `Speak Freely`: `Make crystal-clear voice and video calls to people who live across town, or across the ocean, with no long-distance charges.`
- Card `Make Privacy Stick`: `Add a new layer of expression to your conversations with encrypted stickers. You can also create and share your own sticker packs.`
- Card `Get Together with Groups`: `Group chats make it easy to stay connected to your family, friends, and coworkers.`
- No-tracking heading: `No ads. No trackers. No kidding.` Body: `There are no ads, no affiliate marketers, and no creepy tracking in Beacon. So focus on sharing the moments that matter with the people who matter to you.`
- Nonprofit heading: `Free for Everyone`. Body: `Beacon is an independent nonprofit. We're not tied to any major tech companies, and we can never be acquired by one either. Development is supported by grants and donations from people like you.` Button: `Donate to Beacon`.
- Footer copyright: `© 2013-2026 Beacon, a nonprofit.` Trademark: `"Beacon", Beacon logos, and other trademarks are trademarks or registered trademarks of Beacon Technology Foundation in the United States and other countries (more info here).` Media: `For media inquiries, contact press@beacon.example.org` Column headings: `Organization`, `Download`, `Social`, `Help`.

### The privacy table carried on `/terms`

| Concern | The service holds | The service never holds |
|---|---|---|
| Accounts | an identifier, a set of published pre-keys, encrypted profile blobs | plaintext names, avatars, or contact lists |
| Messages | opaque encrypted envelopes queued for offline recipients, then deleted | any plaintext message, call audio, or attachment |
| Groups | encrypted group state and routing membership sufficient to fan out | group names, group avatars or readable group content |
| Delivery | acknowledgements and contentless push triggers | message content in any push payload |
| Recovery | a recovery store the service cannot read, guarded by a ten-guess limit | the user's recovery secret |
| Donations | the donor's email and the amount | card details of any kind |

### Names used in copy

| Name | Stands for |
|---|---|
| `Beacon` | the product and organization name |
| `Beacon Technology Foundation` | the legal nonprofit entity |
| `press@beacon.example.org` | the press and media contact |
| the Android store listing | the Android download destination linked from `/get` |
| the iPhone and iPad store listing | the iPhone and iPad download destination linked from `/get` |

## Build plan

Build in this order:

1. Design tokens: the colour roles, the Inter scale, radius, shadow and spacing that everything else consumes.
2. Global chrome: the top bar, footer and language dialog, including the scroll shadow and the narrow-viewport collapse.
3. Home page: the hero, the why band, the claim bands and the four feature cards, responsive at every tier; at this point the marketing site is complete and reviewable.
4. Transport and sessions: one end-to-end encrypted message from one device to one offline recipient, with the tampered, replayed, reordered and skipped cases handled from day one.
5. Ratchet and recovery: forward secrecy, per-message ratcheting and post-compromise healing.
6. Devices and sync: a second device linked safely, converging on the same new messages and settings.
7. Groups: sender keys, re-keying on join and leave, at scale.
8. Metadata and identity: sealed sender, usernames, safety numbers, recovery, the encrypted browser store and disappearing messages.
9. Hardening: agreement between two instances of the client, constant-time comparisons, reduced-motion and accessibility passes, and a schema in which a stolen database reveals only ciphertext.

The site ships first because it is fully specified here; the application is built correctness-first, one end-to-end encrypted message before any feature, because a feature added on top of a broken session is a broken feature.

## Constraints

- One product, no tenancy: every account is a peer.
- No native Android, iPhone, iPad, Windows, Mac or Linux app in this build; `/get` links out.
- No phone numbers, no SMS, no address-book upload, and no directory of accounts: people are found by exact username only.
- No password reset.
- No payment processor and no card details; donations are pledges receipted by email.
- No call relay: calls connect directly between browsers or not at all.
- No sticker pack editor: the composer offers the built-in pack.
- No group invite links: an admin adds an invited username.
- No languages beyond English and the eleven translations named here (the site lists twelve; a messenger of this class often lists about seventy).
- No interiors for `/help`, `/blog`, `/developers`, `/careers` and `/brand` beyond a heading and a short paragraph.
- No ads, affiliate marketers, analytics, tracking pixels, third-party fonts or third-party scripts.
- No external network calls at runtime.
- No server-side reading, indexing, searching or moderation of message content.
- Stays responsive with 1000 waiting envelopes on a device and a conversation of several thousand messages.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`: `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

All bodies are JSON. Base64 is standard base64 with padding. "device" means `Authorization: Bearer <device_token>`; "account" means `Authorization: Bearer <access_token>` from sign-in. A successful call returns the named shape; an invalid or unauthorized call is rejected as a client error (never a `5xx`, never a silent success). List endpoints return a top-level JSON array.

| Endpoint | Auth | Request body / query | Returns |
|---|---|---|---|
| `GET /api/health` | none | none | `200` |
| `POST /api/auth/signup` | none | `{"email", "username", "password"}` | `{"username"}` |
| `POST /api/auth/login` | none | `{"email", "password"}` | `{"access_token"}` |
| `GET /api/me` | account or device | none | `{"username", "email"}` |
| `POST /api/devices` | account | `{"identity_key", "signed_prekey": {"key_id", "public_key", "signature"}, "pq_prekey": {"key_id", "public_key", "signature"}, "one_time_prekeys": [{"key_id", "public_key"}], "link_code"?, "replace_existing"?, "access_verifier"?}` | `{"device_id", "device_token"}` |
| `GET /api/devices` | device | none | `[{"device_id"}]`, ascending |
| `DELETE /api/devices/{device_id}` | device | none | empty |
| `POST /api/devices/link-codes` | device | none | `{"code"}` |
| `POST /api/keys/one-time` | device | `{"one_time_prekeys": [{"key_id", "public_key"}]}` | `{"one_time_prekeys": <remaining count>}` |
| `GET /api/keys/count` | device | none | `{"one_time_prekeys": <remaining count>}` |
| `GET /api/keys/{username}` | device | none | `{"access_key", "devices": [{"device_id", "identity_key", "signed_prekey", "pq_prekey", "one_time_prekey"}]}`, devices ascending |
| `PUT /api/profile` | device | `{"profile_ciphertext", "access_key"}` | empty |
| `GET /api/profile/{username}` | device | none | `{"profile_ciphertext"}` |
| `PUT /api/messages/{username}` | header `Unidentified-Access-Key`, or device for your own account | `{"messages": [{"device_id", "guid", "ciphertext"}]}` | `{"accepted": true}`; a device mismatch returns `{"missing_devices", "extra_devices"}` |
| `GET /api/messages` | device | none | `[{"guid", "ciphertext", "server_timestamp", "group_id"}]`, oldest first |
| `DELETE /api/messages/{guid}` | device | none | empty |
| `POST /api/groups` | device | `{"encrypted_state", "members": [usernames]}` | `{"group_id", "revision", "members", "admins"}` |
| `GET /api/groups/{group_id}` | device, member | none | `{"group_id", "revision", "encrypted_state", "members", "admins"}` |
| `PATCH /api/groups/{group_id}` | device, member | `{"expected_revision", "encrypted_state", "add": [usernames], "remove": [usernames]}` | `{"group_id", "revision", "members", "admins"}`; a stale revision returns `{"revision"}` |
| `PUT /api/groups/{group_id}/messages` | device, member | `{"guid", "ciphertext"}` | `{"accepted": true}` |
| `PUT /api/recovery` | device | `{"recovery_blob", "access_verifier"}` | empty |
| `POST /api/recovery/restore` | account | `{"access_verifier"}` | `{"recovery_blob"}`; a wrong verifier returns `{"remaining_guesses"}` |
| `POST /api/donations` | none, header `Idempotency-Key` | `{"amount_minor", "currency", "email"}` | `{"amount_minor", "currency", "status"}` |

Key sizes, decoded from base64: `identity_key` 32 bytes; `signed_prekey.public_key` 32 bytes and its `signature` 64 bytes; `pq_prekey.public_key` 1184 bytes and its `signature` 64 bytes; each one-time `public_key` 32 bytes; `access_key` 16 bytes; `access_verifier` 32 bytes; `profile_ciphertext`, `encrypted_state` and `recovery_blob` 1 to 65536 bytes. Every `key_id` is an integer from 1 to 16777215. One-time pre-key ids are unique within their upload, and the signed pre-key, the post-quantum pre-key and the one-time pre-keys each have their own id space. `members` and `admins` are usernames in ascending order. Anything outside these shapes is rejected and stores nothing.

### No mocks

Each of these is a contract violation: messages, profiles or group state kept readable anywhere on the service; a sender column or sender field beside an envelope; an envelope marked delivered instead of deleted; a nudge or receipt email faked by writing it to a table or a log instead of sending it through Mailpit; a donation recorded only in memory; fonts or scripts pulled from another origin; encryption done by the service on the browser's behalf. PostgreSQL and Mailpit are the facts: the app's screens can only reflect what really lives in them, and the only readable copy of any message is in the browsers of the people in the conversation.

## Definition of done

Beacon is deployed and healthy. A visitor can read the home in any of its twelve languages and give a donation. Two people can exchange messages that each reads in their own browser, on every browser they have linked, while the service only ever holds ciphertext.
