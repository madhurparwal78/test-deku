# Staked Relay Workspace

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, sign up, and exchange a message with another member that only the two members' approved devices can read, without hitting an error page. A different member, a device that was never approved, the database, and anything watching the traffic between the browser and the server must NOT be able to read that message by any means: the words are sealed inside the sender's browser before they leave it, and a server that stores readable text, or seals it with a key the server also holds, does not count.

## Overview

Nightjar is a private workspace carried over a relay network its own subscribers run. It is three products sharing one message layer: a messenger (one-to-one chats, private groups, public groups and broadcast channels, with voice and video calls), encrypted file storage, and a simple planning board where every task is also a chat. Traffic is described as passing through computers run by other subscribers rather than company servers; operators stake NJR, the product's own token, for a place in the network, and share eighty per cent of what members pay, weighted by the tier they staked for and by how long they measurably stayed up.

The app has two halves that share a brand and almost nothing else. The **public page** at `/` is a brochure held to the byte budgets in Technical requirements: an introduction sequence, five feature blocks, an ecosystem section, a token-sale section, a roadmap, questions and a waitlist. The **workspace** under `/app` holds private keys, and the public page must never be given access to anything the workspace holds. Inside the workspace, keys are generated and held in the browser, messages, file names, board names and task titles are sealed there, and the server is a relay: it stores sealed objects, enforces who may send what to which device, measures relay uptime, prices memberships and settles epochs, and it can never open anything it stores. The accounting side (membership, stakes, epochs, rewards, vesting) is a separate system from the message side; the only fact that crosses between them is whether an account's membership lets it send.

The original product this brief describes does not exist yet: the reference is a marketing page for an unreleased app that also raises money through a token sale. So this brief turns the page's promises into obligations, and it handles the sale at arm's length: the token-sale section is built as a set of screens and an application form, no token is sold, no money moves, and the page says so.

It deliberately is not: an organisation console, an administrative view over other people's accounts (the one seeded treasurer runs the accounting and reads whitelist applications, and sees no member's content), a moderation tool, a way for anyone at Nightjar to read, recover or moderate member content, a real blockchain client, a card or bank payment system, or a comparison against other messengers. The genuinely hard parts are sealing on the device with membership that changes over time, a relay that refuses to seal anything to a device or member who is not entitled to it, money arithmetic that is exact, frozen at the epoch boundary and paid exactly once.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (not signed in) | Read the public page, the whitelist stepper, the network limits page and the whitepaper page; join the waitlist; submit a whitelist application with a wallet signature; open a file through a shared link | **Cannot reach anything under `/app` or any member-only API.** **Cannot read any conversation, board, file or membership** |
| Member (signed in) | Enrol and approve devices; send and read sealed messages in conversations they belong to; own private groups, boards and files; join public groups and subscribe to channels; place calls; take quotes and pay for their own or another member's membership; register and stake relays and answer probes for relays they operate; hold and claim vesting positions | **Cannot read a conversation outside the times they were a member of it.** **Cannot seal a message to a device that is not an approved device of a current member.** **Cannot post in a channel unless they are one of its broadcasters.** **Cannot approve a device from that same device.** **Cannot close or settle an epoch, issue probe rounds, move the token event, create vesting positions or read whitelist applications** |
| Treasurer (seeded only) | Everything a member can do; close the open epoch; issue probe rounds; settle closed epochs; set the token event instant; create vesting positions; read whitelist applications | **Cannot read any member's messages, file contents, file names, board names or task titles**, because none of them is ever readable on the server |

Inside a conversation there are per-conversation standings as well: the **owner** of a private group adds and removes members, closes the group and picks its core node; a **broadcaster** of a channel may post in it; a **subscriber** of a channel may read it and never post. These are properties of one conversation, not account roles.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Member session to any Treasurer-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds inside a conversation: a subscriber posting to a channel, a non-owner removing a group member, a pending device approving itself, and a member reading another operator's probe are each denied and change nothing.

Signup is **open**: anyone can create a member account at `/signup` with an email and a password, or by signing a challenge with a wallet. There is no name, no avatar, no phone number and no profile field anywhere. Five accounts are seeded:

| Email | Role | Contact code | Seeded state |
|---|---|---|---|
| `member@example.com` | member | `NJ-MEMBER22` | paid membership, a Visioners vesting position of `40000` NJR |
| `member2@example.com` | member | `NJ-MEMBER23` | paid membership |
| `member3@example.com` | member | `NJ-MEMBER24` | membership lapsed: trial and paid time both ended |
| `treasurer@example.com` | treasurer | `NJ-TREASURY` | paid membership, owner of the seeded public group and channel |
| `member4@example.com` | member | `NJ-OPERATOR` | paid membership, operator of all eight seeded relays |

## Core features

Three rules decide whether the product is what it claims: the relay accepts an envelope only when every device it is sealed to is an active device of a current member at that moment (Section 2 rule 3); a settlement run pays each relay of a closed epoch exactly one transfer however it is started (Section 8 rule 7); and a waitlist request sends at most one confirmation email in 24 hours, addressed to that address alone (Section 10 rule 14).

### 1. Identity: accounts, sessions, the key and devices

**Accounts and sessions.**

1. **An identity is a keypair, not a record.** An account holds an email (only when it signed up with one), a password hash (likewise), a server-generated contact code and its settings. A contact code is `NJ-` followed by eight characters from `A` to `Z` and `2` to `7`, unique, and it is how members find each other. There is no display name, profile, address book or recovery address on the server.
2. Signing up with an email and a password (`POST /api/auth/signup`) creates a member account and returns an `access_token`. The email must be a syntactically valid address and unused; the password must be at least `12` characters. An invalid email, a short password or a taken email is refused and creates nothing. Signing in (`POST /api/auth/login`) returns an `access_token`; signing out (`POST /api/auth/logout`) ends that session and the old token stops working at once, while other sessions of the same account keep working. A session lasts `12` hours.
3. **A wallet signature is an authentication, not a session.** A wallet is an Ed25519 key; its address is `0x` followed by the 64 lowercase hex characters of the public key, and a signature is 128 lowercase hex characters over the UTF-8 bytes of the challenge message. `POST /api/auth/wallet/challenge` takes an `address` and a `purpose` (`sign_in`, `connect` or `whitelist`) and returns a `challenge_id`, the exact `message` to sign and its `expires_at`, `5` minutes after creation. The message names the host of `APP_PUBLIC_URL`, the address, a fresh nonce, the expiry and the purpose, and ends with the sentence `This signature proves you control this wallet. It cannot move funds.`
4. A challenge is used **once**: a verification that presents a used challenge is refused and issues nothing, and when several verifications present the same challenge at the same instant exactly one of them succeeds. A challenge is refused when it has expired, when the signature does not verify against the challenge's own address and its own stored message, and when it is presented to an endpoint of a different purpose: a `whitelist` challenge never signs anyone in, and a `sign_in` challenge never files an application.
5. `POST /api/auth/wallet/verify` with a `sign_in` challenge signs in the account the wallet is attached to. When the wallet is attached to no account, it creates a new member account with that wallet attached and no email.
6. **The two paths never silently create two accounts.** A member signed in with a password attaches a wallet with a `connect` challenge (`POST /api/me/wallets`); from then on, wallet sign-in with that address signs into the same account (same `account_id`). Connecting a wallet that is attached to a different account is refused and changes neither account. `DELETE /api/me/wallets/{address}` detaches a wallet; an account must always keep one way in, so the last wallet of an account without a password cannot be detached.
7. **Trials are one per account and one per wallet.** A new account starts a `14` day free trial at the moment it is created, with one exception: an account created by wallet sign-in whose address has ever been attached to another account starts with no trial. Connecting or detaching a wallet never adds or removes a trial. The membership page states the choice in plain words: trials are limited per account and per wallet, which stops the same wallet collecting trial after trial without asking anyone for personal data, and does not stop someone making new accounts.
8. **Loss is the defining case, and it is said out loud when the key is made.** When an account's first device is set up in a browser, before anything is sealed, a dialog states `This key is the only way into your account. Nobody can restore it, including us.` and the workspace does not open until the checkbox `I understand that nobody can restore this key` is ticked and `Continue` is pressed. There is no recovery path, and the dialog says that too.

**Devices.**

1. Every browser that signs in becomes a **device** with its own key pair generated in that browser. The browser registers only the public half (`POST /api/devices`), and receives a `device_id` and a `device_token`. Devices are named `Device 1`, `Device 2` and onward in enrolment order within the account.
2. An account's first device, and any device registered while the account has no active device, is **active** at once. Every other device starts **pending**. A pending device can open the workspace and read everything that is not sealed (membership, relays, epochs, settings), but every message, file name, board name and task title shows as unopenable on it, it cannot send, upload, post key material or approve anything, and the workspace shows `Waiting for approval from one of your other devices.`
3. **Enrolment is the one act that widens who can read, so it is deliberate, visible and reversible.** Only an **active** device of the same account can approve a pending device (`POST /api/devices/{device_id}/approve`, with that active device's token). A pending device asking to approve itself, any device of another account, or a bare account `access_token` that belongs to no device, is denied and the device stays pending. On the devices page each approve button is named `Approve` followed by that device's name. Every other active device of the account shows `A new device can now read your messages. Added <when>.` after an approval, and the devices page lists every device with its state, when it was added and when it was last active.
4. An approved device can open what is sealed to it from the moment of its approval onward; messages sent before its approval stay unopenable on it.
5. **Removal revokes.** An active device removes a device (`DELETE /api/devices/{device_id}`); the removed device's token stops working, nothing sent afterwards is sealed to it, and the devices page states `That device can no longer read anything sent from now on.` Removing a device advances the key epoch of every conversation the account belongs to by one, exactly as a membership change does.
6. The key directory (`GET /api/directory/{contact_code}`) lists only **active** devices, with their public keys. A pending or removed device never appears there, so nobody seals to a device its owner has not approved.

### 2. Sealed messages

1. **Plaintext exists only on devices.** The browser seals the text before it leaves the browser: every request body and every message the browser sends carries only sealed bytes, never the typed words in any readable, encoded or reversible form, and the database holds only sealed bytes. Every message is sealed under its own fresh message key, so sending the same words twice stores two different `ciphertext` values.
2. A message is an **envelope**: one `ciphertext` (base64 of the sealed bytes) plus one `sealed_key` per recipient device, carrying the message key sealed to that device. The sender reads the conversation's current epoch and its members' active devices from `GET /api/conversations/{conversation_id}/devices` before sealing. The seal binds the sender, the conversation and the message's position, so a sealed message lifted into another conversation does not open there.
3. The relay accepts an envelope (`POST /api/conversations/{conversation_id}/envelopes`, device token) only when every one of these holds, and otherwise refuses it and stores nothing:
   - the sending device is active, its account is a current member, the conversation is not closed, and the account's membership lets it send (Section 7);
   - the shape allows the sender to post (a channel accepts posts only from its broadcasters);
   - `epoch` equals the conversation's current key epoch; a stale epoch is refused as a conflict whose body carries `current_epoch`, so a message composed before a membership change and delivered after it is refused by that stated rule rather than by whichever request arrived first;
   - **every** device named in `sealed_keys` is an active device of an account that is a current member at the moment the relay accepts the envelope. One pending device, one removed device, or one device of a removed member is enough to refuse the whole envelope.
4. **Send is idempotent under retry.** An envelope carries a `client_id` generated inside the sending browser. The relay keeps the first accepted envelope for a `client_id` from one sending device in one conversation; a repeat returns that same envelope (same `envelope_id`) and stores nothing new, and simultaneous repeats store exactly one row.
5. **Order is the sender's, not the network's.** Each envelope carries a positive integer `clock` and a per-device `sender_seq` counting 1, 2, 3 within the conversation. History (`GET /api/conversations/{conversation_id}/history`) lists envelopes by `clock` ascending, then `sender_device_id` ascending, then `client_id` ascending, with identifiers compared as strings character by character, whatever order they arrived in. Each item carries `gap_before`, which is `true` when its `sender_seq` is above 1 and the relay holds no envelope from the same sending device in that conversation with the preceding `sender_seq`; it is worked out at the moment of reading, so a late arrival clears the gap it closes.
6. In a conversation page, the composer is a field labelled `Message` with a `Send` button, and every opened message shows its text. The reader sees each message once. A message that cannot be opened on this device, because nothing was sealed to it or because its authentication check fails after the bytes were altered, is a state and not a crash: it shows `This message can't be opened on this device.` with its sender's contact code and time, and it never shows altered or partial text.
7. A message composed while the browser has no connection is shown as `Waiting to send.` until the relay has accepted it, and never as sent before then.
8. **Location is the one payload still sensitive after it opens.** The composer's attachment menu offers `Share location once`, the default, and `Share live location`, which asks for an expiry of 15 minutes, 1 hour or 8 hours before anything is shared, shows the time left while it runs, and stops by itself at the expiry.
9. **Read receipts are optional and symmetric.** `read_receipts` is off for every new account. A receipt (`POST /api/conversations/{conversation_id}/receipts`) is recorded only when both the reader and the author of that envelope have read receipts switched on; otherwise it is refused and nothing is delivered. A member with receipts off neither sends nor receives them.
10. The text a person types is never rendered by the server, never logged, never placed in a URL and never included in any email.

### 3. Conversations, membership and calls

**Conversations.**

1. There are four shapes, offered by the new conversation wizard as `Chat`, `Private group`, `Public group` and `Channel`, and they are four sets of rules over one message layer:

| Shape (`kind`) | Members | Who may post | How people join |
|---|---|---|---|
| `chat` | exactly two | both | fixed at creation; nobody is ever added or removed |
| `private_group` | few, known | every member | only the owner adds people |
| `public_group` | open | every member | anyone joins themselves |
| `channel` | open | broadcasters only | anyone subscribes themselves; the owner names broadcasters |

2. **Membership is cryptographic state.** Every conversation carries a key `epoch` starting at `1`. Each change of membership (an add, a removal, a leave, a join) advances the epoch by exactly one and is recorded as a membership event, and so does removing a device of a member (Section 1, Devices). The conversation settings page shows the current epoch as `Key epoch <n>`.
3. **Joining does not grant the past, and leaving does not surrender it.** An account can read, through history, exactly the envelopes the relay accepted while that account was a member. A member added today does not see yesterday. A member who is removed still sees everything accepted up to the moment of removal and nothing after it. A member who is removed and later added again sees both periods of membership and nothing from the gap between them. A request for the history of a conversation the account has never belonged to is denied.
4. **Removal says what it can and cannot do.** Only the owner removes a member of a private group, and a non-owner's attempt is denied and changes nothing. When the owner removes someone, the workspace says `They keep what they already received. That's on their device and we can't reach it.` and never describes removal as erasure.
5. **Re-keying reaches everyone, including people who were offline.** After a change the owner's device posts new key material for the new epoch (`POST /api/conversations/{conversation_id}/key-packages`), one sealed package per active device of the current members; the same device rules as envelopes apply. The workspace shows `Updating this group's keys.` while its own devices take up a new epoch.
6. The sync feed (`GET /api/sync`, device token) lists, in the order the relay accepted them, the envelopes sealed to that device, the key packages addressed to it, the receipts delivered to it, and membership events and calls of the conversations its account belongs to. A member who was offline across two changes finds both membership events, in order, when they return. A member who was removed finds the event that removed them and nothing that happened in that conversation afterwards.
7. **A public group protects words from the relays, and from nobody else.** Joining a public group, and posting in one, both show `Anyone can join this group, so treat it as public. Encryption hides it from the relays, not from members.` The member list of a public group or channel is visible to any signed-in account; the member list of a private group or chat is visible only to its members.
8. A channel subscriber cannot post: the relay denies it and stores nothing, and the channel's composer is replaced by a line saying only broadcasters post here. Joining a private group or a chat by request is refused.
9. The owner can close a private group (`POST /api/conversations/{conversation_id}/close`); after that every post is refused and the history stays readable to the people who were members.
10. **Blocking happens on the device**, because there is no server able to enforce it. A member's menu offers `Block`, which states `Blocking applies on this device only.` and collapses that person's messages on this device to `Message from a blocked person`, sending nothing to the server.
11. The workspace home at `/app` is a queue of the account's conversations, most recent activity first, each row showing the conversation (its opened name, or the other members' contact codes when its name cannot be opened on this device) and how many envelopes arrived since this device last opened it.

**Calls.**

1. A member places a voice or video call in a conversation they belong to (`POST /api/calls`), and anyone else is denied. A call record holds no media and no media key, and the call dialog names each other participant by the contact code whose active devices the key directory lists.
2. **The route is a choice the person makes, remembered, and private by default.** Each account's `call_route` setting is `private` or `direct`, and every account starts at `private`. Before a first call, the call dialog shows `Route privately, slower. Or connect directly, faster, and share your network address with them.` with the private option selected.
3. **A direct route needs both people.** A call is `direct` only when the conversation is a `chat` and **both** participants' `call_route` is `direct` at the moment the call is placed; in every other case it is `relay`. A group call, in any group shape, is always `relay`, whatever anyone has chosen, because a direct group call hands every participant's address to every other.
4. The call record carries `peer_address`, the other participant's network address as the relay last saw it (the `last_seen_address` of that participant's most recently active device), only when the route is `direct`, and never for a relayed call. A direct call is labelled `Direct connection. They can see your network address.` for as long as it lasts.
5. **A ring is a message.** A placed call and each ring reach the other participants' devices as `call` items in the sync feed. A ring carries a `ring_id`; the same `ring_id` arriving again rings once, and a ring arriving after the call has ended is refused and does not ring.
6. Answering, declining and ending are reachable instantly from the keyboard. The call history list is built on the device and can be cleared there; the relay keeps only the call records it needs to ring, answer and end a call, and `GET /api/calls/{call_id}` answers such a record to the call's participants alone.

### 4. The planner

1. **A task is a conversation.** A board belongs to the member who created it and has columns, each with a `column_id` chosen by the creating browser and a sealed label. Creating a task (`POST /api/boards/{board_id}/tasks`, device token) creates the task and its conversation as one object and returns both ids; the task's sealed title is the conversation's sealed topic. Renaming the task (`PATCH /api/tasks/{task_id}`) renames the conversation in the same act, so the conversation's `sealed_topic` always equals the task's `sealed_title`. There is no separate comment thread. The new board wizard takes a `Board name` and `Next` on `/app/boards/new`; its columns step on `/app/boards/new/columns` starts with the columns `To do`, `Doing` and `Done`, which can be renamed, removed or added to, and `Create board` creates the board and opens it at `/app/boards/<board_id>`.
2. **A task's audience is a set of people, a set of private groups, or both, and the two compose.** The board owner sets it (`PUT /api/tasks/{task_id}/audience`). The task's readers are the board owner, plus every member named directly, plus every **current** member of every private group named. Group membership is read live: somebody added to a named group gains the task at once, and somebody removed from it loses the task's future messages at once, exactly as a group member does, and the task conversation's epoch advances when its readers change.
3. **Un-sharing from one group removes only what that group granted.** When a task is shared to two groups and then un-shared from one, a person who is still a reader through the other group, or through being named directly, remains a reader, and only people who were readers through the removed group alone stop being readers.
4. **Moving a task changes what it says, not who can read it.** Board position and audience are independent.
5. **The board converges without an arbiter.** Every placement of a task (its creation, and every move through `POST /api/tasks/{task_id}/moves`) carries a column, a `position`, a positive integer `clock` and the placing device. A task sits where its placement with the highest `clock` put it; when two placements carry the same `clock`, the one from the device whose `device_id` sorts higher, compared as a string character by character, wins. Within a column, tasks are ordered by `position` ascending and then by `client_id` ascending, where a `position` is a string of `0` to `9` and `a` to `z` compared character by character. Two people inserting between the same two neighbours with the same `position` both keep their tasks, in `client_id` order. The board reads the same whatever order the placements reached the relay in.
6. **Creating a task with no connection is ordinary.** The browser keeps it as `Waiting to send.` and sends it when the connection returns; a task carries a `client_id` from the browser, and sending the same `client_id` again returns the task already created and creates no second task or conversation.
7. **Deleting a task deletes a conversation.** Before it happens the workspace says `Deleting this task deletes its conversation. Other members keep what is already on their devices.`, and after it the task and its conversation are gone for every reader.
8. Moving a card has a keyboard path that does not depend on dragging: with a card focused, the card's `Move` menu lists the columns and the positions within them, and choosing one moves it.
9. The board and its task conversations converge together: a reader never sees a task whose position arrived without its conversation, or a conversation for a task that is not on the board.

### 5. Storage and shared links

1. **Files are sealed on the device and only the device can open them.** A file's contents, name, size and type are sealed in the browser before anything is uploaded; the relay stores a `sealed_name`, a `sealed_meta` and sealed pieces, and never the readable name or contents in any form. The storage page uploads through `Choose file` and `Upload`, and lists each file by its name as opened on this device.
2. **Pieces are padded to a size class.** A file is uploaded as `piece_count` pieces of one `piece_size`, and `piece_size` is one of exactly three classes: `65536`, `1048576` or `4194304` bytes. Every piece the relay accepts (`PUT /api/files/{file_id}/pieces/{piece_index}`) is exactly `piece_size` bytes long; a piece of any other length is refused and stores nothing, so the relay learns only a size class and a count, never an exact length. The storage page states the trade: padding costs bandwidth and hides size.
3. **Storage has a quota.** Every account has `67108864` bytes. A file reserves `piece_size` times `piece_count` bytes the moment it is created (`POST /api/files`), and a file whose reservation would take the account over its quota is refused. Two simultaneous file creations that fit one at a time but not together: exactly one is accepted. The storage page shows `<used> of <total>. New files will be refused at the limit.`
4. **Availability is a state.** A file is `uploading` until every piece is stored, then `available`. A file that was available and is now missing any piece reads `unavailable`, worked out at the moment it is read, and shows `This file's pieces are no longer on the network.` rather than an error.
5. **Deletion is honest.** Deleting a file (`DELETE /api/files/{file_id}`) removes it from the account's storage, releases its reservation and marks it `removed`; the workspace says `Removed from your storage. Pieces already distributed can't be recalled.`
6. A member shares a file into a conversation they belong to (`POST /api/conversations/{conversation_id}/files`). Current members of that conversation can then fetch the file's pieces; a member who is removed loses that access at once. The sharer un-shares it (`DELETE /api/conversations/{conversation_id}/files/{file_id}`), after which the conversation's members no longer fetch its pieces through that share.
7. **A link is a capability, and it states its scope.** `POST /api/files/{file_id}/links` takes `expires_in_hours` from `1` to `720` and returns a `link_token` of at least 32 unguessable characters and its `expires_at`. Anyone holding the link can fetch the file's sealed metadata and pieces through it (`GET /api/links/{link_token}`) until it expires or is revoked; the link carries the file key in the part of the address after `#`, which the browser never sends to the server. Creating one shows `Anyone with this link can open the file. Expires <when>.`
8. **Revocation is real.** The file owner revokes a link (`DELETE /api/links/{link_token}`); after that the link is refused with `reason` `revoked`, and the owner sees `Link disabled. Copies already downloaded can't be recalled.` An expired link is refused with `reason` `expired` and the recipient sees `This link has expired.`
9. **A link is not a membership.** Revoking a link leaves every conversation member's access untouched, and removing someone from a conversation leaves every link to the file working.
10. Sealing and uploading a large file never freezes the interface: the upload shows its progress, and it can be cancelled.

### 6. The relay network

1. **The relay stores no path.** No envelope, history item, sync item or call record carries the route a message took or the relays it passed through, and duplicated, delayed and reordered envelopes are resolved by the message rules of Section 2 (rules 4 and 5), so nothing depends on the network delivering in order.
2. A member registers a relay they will operate (`POST /api/relays`) with a unique `name` and a `stake_tokens` amount in whole NJR. A stake below `10000` NJR is refused. The tier a relay holds is a threshold, published as data with an effective date of 1 January 2026:

| Tier | Stake at or above (NJR) | Weight per answered round |
|---|---|---|
| `basic` | `10000` | `10` |
| `level-1` | `15000` | `15` |
| `level-2` | `25000` | `25` |
| `master` | `150000` | `150` |

3. The reference page advertises a regular stake of 10,000 to 25,000 and a master stake of 150,000, while its whitepaper names a lowest tier of 15,000; this table reconciles the two by keeping 10,000 as the floor and naming it `basic`. A relay's weight comes from the threshold of the tier it holds, never from the stake above that threshold: a stake of 20,000 NJR earns at `level-1`.
4. The operator adds stake (`POST /api/relays/{relay_id}/stake`) or withdraws it (`POST /api/relays/{relay_id}/unstake`). A withdrawal lowers the stake, and therefore the tier, at once; the withdrawn NJR unlock `7` days later. A withdrawal that would leave less than `10000` NJR is refused. When a stake falls below its tier's threshold the relay page says `Your stake is below <tier>. This node earns at <lower tier> until it's topped up.`
5. **Uptime is measured, never reported.** The treasurer issues a probe round for the open epoch (`POST /api/epochs/current/probe-rounds`), which gives every registered relay a fresh nonce and records the tier each relay holds at that moment. The operator fetches their relay's latest nonce (`GET /api/relays/{relay_id}/probe`) and answers it (`POST /api/relays/{relay_id}/probe-answers`). An answer counts once, for that relay, for that round, only while that round is the latest: a repeated answer, an answer carrying another relay's nonce, and an answer to a round that is no longer the latest are each refused and count nothing. A member who does not operate a relay is denied its nonce.
6. A relay may send heartbeats with self-reported figures (`POST /api/relays/{relay_id}/heartbeats`); the relay accepts them and they change nothing that is counted or paid.
7. **A relay that takes the reward and drops the traffic earns nothing for the rounds it did not answer, and no stake is slashed.** That is the decision, and the network limits page says so.
8. **A group may pin its traffic to one relay.** The owner of a private group chooses a core node (`PUT /api/conversations/{conversation_id}/core-node`). The setting states `This group's traffic will go through <node>. It will see when the group is active, and if it goes offline the group falls back to the open network.` The core node cannot read the group's content. A conversation's `routing` reads `core_node` while that relay answered the latest probe round of the open epoch, and `open_network` with `fell_back` true when it did not, worked out at the moment it is read; while the open epoch has no probe round yet, it reads `core_node`. The group is told when it falls back.
9. **Running a relay has a duty of care.** Starting relay mode on the relay page first shows `Other people's encrypted traffic will pass through your connection while this runs.` with `Start` and `Cancel`, and a running relay offers `Stop relay mode`, which stops it at once.
10. **The limits are published in the product.** `/network-limits` states plainly that encryption hides what was said and not that something was said, when, or roughly how much; that someone watching both ends of a path can correlate traffic; that the network pads pieces to size classes and sends no cover traffic; that it does not attempt to resist an observer who can see the whole network; and that a chosen core node sees when its group is busy.
11. The page does not claim the applications or the relay client are open source until a public repository and reproducible builds exist, because a claim nobody can check is decoration.

### 7. Membership and payment

1. **Two prices, five rails, one entitlement.** A membership month costs `225` US cents ($2.25) paid on the `njr` rail and `350` US cents ($3.50) on each of the other four rails. Both prices are data, not code: they live in `rail_prices` with each rail's decimals and confirmation depth. Paying more buys nothing more: every rail grants the same thirty days of the same service.

| Rail | Asset | Base unit | Price | Confirmation depth |
|---|---|---|---|---|
| `njr` | NJR, the Nightjar token | one millionth of an NJR (`6` decimals) | `225` cents | `12` confirmations |
| `usdc` | a dollar stablecoin | one millionth (`6` decimals) | `350` cents | `12` confirmations |
| `usdt` | a dollar stablecoin | one millionth (`6` decimals) | `350` cents | `12` confirmations |
| `xmr` | a privacy coin | one trillionth (`12` decimals) | `350` cents | `10` confirmations |
| `app_store` | an application store's own billing, in US cents | one cent | `350` cents | the store reports `settled` |

2. **Rates have a source and an age.** The chain watcher reports rates (`POST /api/watcher/rates`) as `usd_micros`, the US-dollar price of one whole unit of the asset in millionths of a dollar, with the `observed_at` instant the watcher saw it. A quote is refused with `reason` `rate_stale` when the most recent rate for its asset was observed more than `10` minutes before the quote is made. The `app_store` rail needs no rate. The `asset` of a rate, a quote and a `rail_prices` row is the lowercase code of that rail's asset, `njr`, `usdc`, `usdt` or `xmr`; the capitalised codes in Display formats are for display only. The membership page shows the latest rate per asset with when it was observed, read from `GET /api/rates`.
3. **A quote states its amount, its rate, the rate's age and its expiry.** `POST /api/quotes` returns `amount_due` in the rail's base unit, computed as the price in millionths of a dollar times ten to the rail's decimals, divided by `usd_micros`, **rounded up** to a whole base unit; the rate used and when it was observed; `expires_at`, `15` minutes after the quote; and a `deposit_reference` unique to that quote. The membership page shows it as `<amount> <asset>, at a rate from <when>. Expires in <n> minutes.`, where `<amount>` is the bare figure and `<asset>` the capitalised code (`15 NJR, at a rate from 2026-09-16 12:00 UTC. Expires in 15 minutes.`); an `app_store` quote reads `$3.50. Expires in <n> minutes.`; and a lapsed quote is replaced with `That quote has expired. Here's a fresh one.`

| Rail | Rate (`usd_micros`) | `amount_due` |
|---|---|---|
| `njr` | `150000` | `15000000` |
| `njr` | `140000` | `16071429` |
| `xmr` | `157300000` | `22250476796` |
| `usdc` | `999800` | `3500701` |

4. **Every payment carries the quote's `deposit_reference`**, so an inbound payment on any rail, the privacy coin included, is matched to its quote by that reference and never by watching addresses. A quote may name another member's contact code as the beneficiary, which is how a member pays for family, friends or colleagues.
5. **Chain facts arrive signed.** The watcher reports payments (`POST /api/watcher/payments`) and rates as JSON bodies signed with Ed25519: the header `X-Watcher-Signature` carries the 128 hex character signature over the exact raw body bytes, and the watcher's public key is `efe6e71259fd773f94f0a96ae30a706f1a74dc8a5fd275b71942f37b5f75ab1f`. An event with no signature, a signature by any other key, or a body altered after signing is refused and changes nothing.
6. **A payment is a progression, not a moment.** A payment event carries `rail`, `tx_hash`, `deposit_reference`, `amount` in the rail's base unit, `block_time` and `confirmations` (the `app_store` rail carries `state` `pending`, `settled` or `refunded` instead of confirmations). The same `tx_hash` on the same rail is one payment however many times it is reported; each report may raise its confirmations. A payment below its rail's confirmation depth is `seen`, grants nothing, and the membership page shows `Payment seen. Waiting for confirmation.`
7. **The moment a payment reaches its depth, it is decided once**, and simultaneous reports of that moment decide it once:
   - **the rate that applies is set by the block time, not by when the report arrives.** When `block_time` is at or before the quote's `expires_at`, the quote's own `amount_due` applies, however late the report arrives. When `block_time` is after `expires_at`, the payment is re-quoted: `amount_due` is recomputed from the most recent rate for that asset observed at or before `block_time`;
   - when the quote was already settled by a different payment, this payment is `credited`: its whole amount is held as credit and the membership is not extended;
   - when `amount` times `1000` is at least `amount_due` times `995` (a shortfall of at most half a per cent), the payment is `settled`, any excess over `amount_due` is held as credit, and the beneficiary's membership is extended by `30` days from the later of its current `paid_until` and the payment's `block_time`;
   - otherwise it is `underpaid`, with `shortfall` equal to `amount_due` minus `amount`, and the membership page shows `<amount> short. Send the difference or we'll return it.` A later payment carrying the same `deposit_reference` adds to it, and the quote settles once the total clears the same half per cent rule.

| `amount_due` | `amount` paid | Outcome |
|---|---|---|
| `16071429` | `15991072` | `settled`, no credit |
| `16071429` | `15991071` | `underpaid`, `shortfall` `80358` |
| `16071429` | `16100000` | `settled`, credit `28571` |

8. An `app_store` payment reported `refunded` after it settled removes the thirty days it added. The application store settles on its own schedule, so its state is reconciled from what the store reports, never assumed.
9. **Membership has a period, a state and an expiry, and its state is worked out when it is read.** `GET /api/membership` returns `state` `active` while `paid_until` is in the future, `trial` while the trial is still running and there is no paid time, and `suspended` otherwise. While `active`, the membership page shows `Member until <date>.`
10. **Failure to renew suspends and deletes nothing.** A suspended account keeps its keys, devices, conversations, history, files and board. It can still sign in, read history, approve and remove devices, and pay. What stops is carrying new traffic across other people's relays: sending envelopes and key packages, and creating files, are refused with `reason` `membership_suspended`. The workspace shows `Membership expired. Nothing has been deleted. Sending stops until you renew.` Paying again restores sending at once, with every device and conversation as it was.
11. The trial is a real state and the membership page shows `Free trial, <n> days left.` while it runs.
12. **Paying for someone else grants no view of them.** A sponsored member sees `<sponsor> is paying for your membership.` with the sponsor's contact code, and can decline (`POST /api/membership/sponsorship/decline`), which ends the sponsored time at once: `paid_until` moves back by the sponsored days, derived when read as thirty for each settled, unrefunded payment since the last decline whose quote named this member as beneficiary and another account as payer; the member has no paid time when that leaves `paid_until` at or before the moment of the decline, and any later sponsored payment is `credited` back to the sponsor. The sponsor's list of sponsorships (`GET /api/sponsorships`) shows, per recipient, only the recipient's contact code and whether the sponsorship is `active` or `declined`, nothing about the recipient's devices, activity, conversations or paid dates. A sponsorship ending suspends by the rule above and deletes nothing.

### 8. Epochs, settlement and rewards

1. **The objects.** An epoch has a number, an opening, a closing and a state: `open` until the treasurer closes it; `closed` from then until a settlement run pays its first share; `settling` while some shares are paid and others are not; and `settled` once every share above zero is paid. An epoch with no share above zero reads `settled` after its first settlement run. A stake has an amount, an owner, a lock and the tier it qualifies for. A relay has an operator, a tier and a measured uptime within each epoch. An epoch's pool is what members paid during it, by rail. A distribution is the share computed for each relay of a closed epoch.
2. **A receipt belongs to the epoch that is open at the moment its payment settles.** A payment whose block time falls inside one epoch and which settles after that epoch has closed belongs to the next epoch, and a closed epoch's receipts, pool and weights never change.
3. **Every rail enters the pool, at a stated rate.** A settled `njr` payment contributes the smaller of its `amount` and its `amount_due`, in millionths of an NJR. A settled payment on any other rail contributes its price in millionths of a dollar (`3500000`) times one million, divided by the most recent NJR rate observed at or before the moment it settled, rounded down; when no NJR rate had been observed by then it contributes `0` and still counts as a receipt of that epoch. Credit never enters the pool. The pool is eighty per cent of the sum of an epoch's contributions, rounded down to a millionth of an NJR.
4. **Weight is tier and measured time.** A relay's weight in an epoch is the sum, over every probe round of that epoch the relay answered, of the weight of the tier the relay held when that round was issued. A relay whose stake fell from `level-2` to `level-1` halfway through an epoch earned at `25` for the rounds before and at `15` for the rounds after.
5. **Rounding goes to one place, every time.** Each relay's share is the pool times its weight, divided by the epoch's total weight, rounded down to a millionth of an NJR. What rounding leaves over is the epoch's `remainder` and stays with the treasury; the total paid never exceeds the pool. When the total weight is zero the whole pool is remainder.
6. **Settlement is computed from the frozen snapshot taken at close.** Closing the open epoch (`POST /api/epochs/current/close`, treasurer) freezes its receipts, pool, rounds and every relay's weight, and opens the next epoch. A stake withdrawn or added after the close, a relay retired after it, and a payment settling after it all leave that epoch's shares exactly as they were.
7. **A closed epoch is paid exactly once.** `POST /api/epochs/{number}/settle` (treasurer) pays every relay with a share above zero one `reward` transfer in NJR to its operator's token ledger. It takes an optional `limit`: a run pays at most `limit` unpaid relays, in ascending relay name order, and reports the rest as `remaining`, so a run that stops partway is ordinary. Running settlement again, running it after a partial run, or running it several times at once never pays any relay a second time; together the runs pay each relay with a share above zero exactly one transfer of exactly its share. Settling an open epoch is refused. After the last share is paid the epoch reads `settled`.
8. **A settled epoch is auditable.** `GET /api/epochs/{number}` shows, to any signed-in account, the epoch's contributions, pool, total weight, remainder, and for every relay its answered rounds by tier, its weight, its share and whether it has been paid, which the epoch page shows per relay as `Paid` or `Unpaid`. The operator's relay page shows `Epoch <n> settled. Your share: <amount>, from <uptime> uptime at <tier>.`, where uptime is the share of that epoch's rounds the relay answered and tier is the tier it held when the epoch closed.
9. **Worked example: seeded epoch 1** (closed, not settled). Six probe rounds. Kestrel answered all six at `level-2` (weight `150`); Heron answered four at `basic` (weight `40`); Osprey answered three at `level-2` and two at `level-1` (weight `105`); Plover answered none (weight `0`). Total weight `295`. Receipts: three `njr` payments of `15000000` each; two `usdc` payments that settled while NJR was at `150000`, contributing `23333333` each; one `xmr` payment that settled while NJR was at `140000`, contributing `25000000`. Contributions `116666666`; pool `93333332`. Shares: Kestrel `47457626`, Heron `12655367`, Osprey `33220338` (rounded down; rounding to nearest would pay `33220339`), Plover `0`; remainder `1`.
10. The circularity is modelled as a flow, not a stock that is assumed to balance: operators are paid in NJR, NJR buys memberships at a discount, and memberships fund the pool. The pool is what was received, and a share of a smaller pool is smaller; nothing tops a pool up.

### 9. The token-sale surface, vesting and the whitelist

1. **This section is screens and records, and it authorises no sale.** Offering a transferable token with a valuation and a vesting schedule is a regulated activity, and who may be offered it, where and with which warnings is a legal determination this product does not make. The token-sale section says `Nightjar does not sell tokens on this page. An application records your interest and is not an allocation.` No payment is ever taken for tokens anywhere in the app.
2. **The offer is not displayed before the eligibility statement.** The Visioners Round terms stay hidden until the visitor ticks `I am a private investor and a potential user of Nightjar` and presses `Show the terms`. The terms then read: `Visioners Round`, `$0.035 for token`, `10 000 000 tokens are for sale to early bird members (10% of total supply)`, `$3.5 mln FDV at this round`, `$5,000 to $50,000 in USDC min and max investment per wallet`, `10% unlocked at TGE, then 3 months cliff and 9 months of linear vesting`, and `availability: available only for private investors - potential users of Nightjar`. Total supply is `100000000` NJR.
3. **A vesting schedule is a record, not a branch.** One calculation serves all eleven schedules (`GET /api/token/schedules`), and each is a row of data:

| `schedule` | Label | Share of supply | Released at the token event | Cliff (months) | Linear release (months) |
|---|---|---|---|---|---|
| `team` | Team | 15% | 0% | 12 | 24 |
| `treasury` | Treasury | 20% | 0% | 6 | 36 |
| `visioners` | Visioners Round | 10% | 10% | 3 | 9 |
| `seed` | Seed Round | 5% | 5% | 6 | 12 |
| `private` | Private Round | 8% | 10% | 3 | 12 |
| `strategic` | Strategic Round | 4% | 15% | 3 | 9 |
| `public` | Public Round | 3% | 25% | 0 | 6 |
| `liquidity` | Exchange Liquidity | 10% | 100% | 0 | 0 |
| `bounty` | Testnet Bounty | 2% | 50% | 0 | 6 |
| `community` | Community Incentives | 13% | 0% | 1 | 36 |
| `genesis` | Genesis Infrastructure Supply | 10% | 20% | 0 | 24 |

4. The table reconciles and the whitepaper page shows the proof: the shares sum to one hundred per cent, and applying each row's event release to its share gives an event supply of `16400000` NJR.
5. **Time is the token event, not the purchase.** Every position is anchored to the one token event instant, which the treasurer sets (`PUT /api/token/event`) and may correct; the token page and the whitepaper page show the event instant from `GET /api/token/event`. A month is exactly `30` days.
6. **The cliff is a period of no release, not of no accrual.** For an allocation `A` in millionths of an NJR: the event part is `A` times the event release, rounded down; the rest is `A` minus the event part. With `t` the seconds since the token event, `C` the cliff and `D` the cliff plus the linear release, both in seconds: before the event nothing is vested; from the event until `C` only the event part is vested; from `C` the event part plus the rest times `t` divided by `D`, rounded down, is vested, and from `D` onward all of `A`. So accrual runs from the event, nothing of it is released during the cliff, and what accrued is released at once when the cliff ends.

| Visioners position of `1000000` NJR | Vested |
|---|---|
| before the token event | `0` NJR |
| `89` days after | `100000` NJR |
| `90` days after | `325000` NJR |
| `120` days after | `400000` NJR |
| `360` days or more after | `1000000` NJR |

7. **The claimable balance is computed fresh, never kept as a running total.** Claimable is vested now minus already claimed, and never below zero. Moving the token event changes what is claimable at once, in either direction.
8. **Claiming twice transfers once.** `POST /api/token/claims` transfers the whole claimable balance of one position as one `vesting` transfer to the holder's token ledger. A second claim with nothing newly vested transfers nothing and writes no ledger row, and while nothing is claimable the token page's `Claim` button is unavailable and says so. Simultaneous claims on one position transfer the claimable balance exactly once between them. A holder who claims in month five and again in month seven receives exactly what vested between, and across any sequence of claims and corrections the total ever claimed equals the allocation once the schedule has fully vested, to the last millionth.
9. The token page shows each position as `<claimable> claimable now. <locked> unlocks by <date>.`
10. **The whitelist is an application, not an allocation.** The stepper at `/whitelist` has three steps at their own addresses, `/whitelist` (the wallet), `/whitelist/details` and `/whitelist/review`. The wallet step asks for a `Wallet address`, fetches a `whitelist` challenge when `Get message to sign` is pressed and shows its message in a read-only field labelled `Message to sign`, takes the `Signature`, and moves on with `Continue`; the details step takes `Email` and `Amount in USD` (whole dollars) and moves on with `Continue`; the review step submits with `Apply`. `Back` never loses what was entered, and a stepper left partway resumes where it was after a reload. The stepper states in the form why the email and amount are collected, that only the treasurer reads them, that they are stored apart from everything else in the workspace, and that they are deleted a year after the sale closes.
11. `POST /api/whitelist/applications` takes the signed `whitelist` challenge, the `email` and `intended_usd_cents`, which must be from `500000` to `5000000` ($5,000 to $50,000). The limit is a per-wallet mechanic, not a per-person policy, and the stepper says so. **One wallet address files one application**: a second application from the same address is refused, and simultaneous applications from one address produce exactly one application and one email. An accepted application is `applied`, never `reserved`, and the page shows `Application received. It is not an allocation, and we'll be in touch.`
12. An accepted application sends one email to the address in the application only, with no cc and no bcc, whose subject begins `Nightjar whitelist application received` and whose body begins with `Application received. It is not an allocation, and we'll be in touch.`
13. A signature requested here authenticates the wallet exactly as sign-in does, with the same single use, expiry and purpose rules, and it cannot authorise a transfer.

### 10. The public page

1. **One document, deep-linkable, never dependent on being scrolled in order.** `/` carries the sections `aboutSection`, `featuresSection`, `ecosystemSection`, `tokenSaleSection`, `roadmapSection`, `faqSection` and `subscribeSection`, each addressable by `#` and its id. The floating navigation reads About, Features, Ecosystem, Token Sale and Subscribe. Choosing one moves to its section and is a history entry the back button reverses, and arriving at `/#<id>` lands at that section.
2. **The introduction is the page's most consequential interaction.** On a first visit the page opens on an introduction, a region labelled `Introduction`, that steps through six stages, `Security`, `Chat`, `Voice messages`, `Storage`, `Task setup` and `Planner`, as illustrations with their captions in a strip beneath a drawn phone, with a `Skip the intro` button.
3. **The skip control is the first thing the keyboard reaches**: the first press of Tab on a freshly loaded page focuses `Skip the intro`, and pressing Enter on it ends the introduction and returns scrolling to the page.
4. **Holding the page still has an owner and a guaranteed end.** The introduction is the only thing in the product entitled to stop the page scrolling, and it releases scrolling when it is skipped, when its sixth stage has shown, when anything it waits on fails to arrive, and in every case within `30` seconds of starting. The page never starts in a state that only a script can release: with scripts unavailable there is no introduction overlay and the page scrolls.
5. **Arriving at a section never shows the introduction.** A visit to `/#<any section id>` shows no introduction and lands at that section.
6. **A returning visitor does not sit through it again.** After the introduction has been skipped or has finished once, reloading `/` or visiting it again later in the same browser shows no introduction.
7. **Under a reduced-motion preference** the introduction does not play: the six stages show together as stills with their captions, nothing holds scrolling, the repeating banner does not move, smooth scrolling gives way to the browser's own, scroll-linked movement rests at its end state, and the spinner becomes a still indicator.
8. **The page is complete before any reveal runs.** Every section, heading and paragraph is visible and readable with scripts unavailable, with the reveal-on-scroll behaviour unsupported, and under the reduced-motion preference; fading content in as it scrolls into view is an enhancement over a page that is already whole.
9. **The repeating banner** carries `get to know Nightjar better` separated by the hexagon mark, repeated so the loop closes without a jump. It moves continuously, pauses while it is pointed at or holds focus, stops under the reduced-motion preference, and assistive technology reads its phrase once, not once per repeat. The ecosystem section carries a second banner, `Ecosystem operated by users`, under the same rules.
10. **The questions are disclosures.** The four questions (why privacy matters, why the operators cannot read anything, how the network compares with other networks, and why the service is paid) each have a heading that is a button announcing whether it is expanded; a collapsed answer is out of the reading order, and an expanded answer can be reached from the keyboard at once. The answers make claims the workspace honours and name no other product.
11. **The roadmap is data with dates.** Its five entries (`April 2024` Whitepaper v.0.1.0 developed, `Summer 2024` Investment, `Q3 2025` Token sale (moved to Q2 2026), `Q2 2026` Token sale, `Q3 2026` Native app) each show a state worked out from their dates and whether they were delivered: `Delivered`, `Missed` once their period has ended undelivered, or `Upcoming`. Only the whitepaper and the investment entries are delivered. The token-sale section dates the sale `Q2 2026`, the date of the roadmap's current token-sale entry, and neither states any other date for it.
12. **The waitlist collects one thing and says why in the form.** The subscribe form takes an `Email`, an unticked checkbox `I agree to receive Nightjar news by email`, and a `Subscribe` button, and states inside the form, before anything is sent: `We use this address only to send Nightjar news. Nightjar holds it and shares it with nobody. We keep it until you remove it, and every email has a link that removes it at once.` Nothing else is collected with it, and the public page loads no third-party analytics.
13. `POST /api/waitlist` accepts only `email`, `consent` and `website`. It is refused, with nothing stored and nothing sent, when the email is not a valid address, when `consent` is not `true`, or when any other field is present. `website` is a field no person sees or fills; **a form arriving with `website` filled in came from a bot and is refused** and sends nothing.
14. **Double opt-in, delivered to the right address only.** An accepted request answers `Check your inbox to confirm.` whatever the address's history, and sends one email addressed to that address only, with no cc and no bcc, whose subject begins `Confirm your Nightjar waitlist place` and whose body begins with the confirmation link, `<APP_PUBLIC_URL>/waitlist/confirm?token=<token>`, and also carries a removal link, `<APP_PUBLIC_URL>/waitlist/remove?token=<token>`. **At most one confirmation email goes to an address in any 24 hours, however many requests arrive, including requests submitted repeatedly in quick succession and requests arriving at the same instant.** The address is on the list only after its confirmation link is opened.
15. Opening a confirmation link shows `You are on the Nightjar waitlist.`; opening the same link again shows `This confirmation link has already been used.`; opening a removal link removes the address and shows `Removed. Nightjar no longer holds your address.` After a removal, a new request sends a new confirmation, but never sooner than 24 hours after the last one sent to that address: removal deletes the address and both tokens and keeps only a SHA-256 digest of the lowercased address with the time of its last email.
16. **Every form rejects invalid input inline, names the field, and writes nothing.** On the waitlist form, the sign-up form and the whitelist stepper, an invalid entry shows a message beside the field that names it (for example `Email: enter a valid email address`), and nothing is stored or sent.
17. **Every image carries alternative text.** Every content image on the public page, the whitelist stepper, the network limits page and the whitepaper page has alternative text describing it, and every decorative image or drawing (the hexagon, the gradients, the drawn phone's frame) declares itself decorative and is skipped by assistive technology.
18. **An unknown address renders Nightjar's own not-found page.** Any public address the app does not serve, and any address under `/app` it does not serve when the visitor is signed in, answers not-found with a page reading `Page not found` and a link `Back to Nightjar` to `/`.
19. **A sitemap and a robots file describe the public routes.** `/sitemap.xml` lists the absolute addresses of exactly these six public routes, `/`, `/whitelist`, `/network-limits`, `/whitepaper`, `/signin` and `/signup`, and no address under `/app`; `/robots.txt` names the sitemap's absolute address on a `Sitemap:` line and disallows `/app`.
20. **Integrity.** No screen recording of the unreleased app appears anywhere: the introduction is illustrated and captioned. No application-store badge, and no comparison to any named messenger or blockchain, appears; the availability block reads `Install on mobile` and `Install on desktop`, each `Coming Soon`, as text.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The public page: introduction, features, ecosystem, token sale, roadmap, questions, waitlist | public |
| `/whitelist` | Whitelist stepper, step 1: wallet address, message to sign, signature | public |
| `/whitelist/details` | Whitelist stepper, step 2: email and amount in USD | public |
| `/whitelist/review` | Whitelist stepper, step 3: review and `Apply` | public |
| `/network-limits` | What the network does and does not hide, and the slashing decision | public |
| `/whitepaper` | Tiers, the operator split, the eleven schedules and their reconciliation | public |
| `/waitlist/confirm` | Confirms a waitlist address from its emailed link | public |
| `/waitlist/remove` | Removes a waitlist address from its emailed link | public |
| `/signup` | Create an account with email and password, or with a wallet | public |
| `/signin` | Sign in with email and password, or with a wallet | public |
| `/links/<link_token>` | Opens a file shared by link | public |
| `/app` | The conversation queue, most recent activity first | member |
| `/app/conversations/new` | New conversation wizard, step 1: choose the shape | member |
| `/app/conversations/new/people` | Wizard step 2: add people by contact code | member |
| `/app/conversations/new/name` | Wizard step 3: name it and create | member |
| `/app/conversations/<conversation_id>` | One conversation: history, composer, calls, attachments | member |
| `/app/conversations/<conversation_id>/settings` | Members, removal, core node, close, broadcasters | member |
| `/app/explore` | Public groups and channels to join | member |
| `/app/boards` | The member's boards | member |
| `/app/boards/new` | New board wizard, step 1: name | member |
| `/app/boards/new/columns` | New board wizard, step 2: columns, then create | member |
| `/app/boards/<board_id>` | One board, its columns and cards | member |
| `/app/boards/<board_id>/tasks/new` | New task wizard, step 1: title and column | member |
| `/app/boards/<board_id>/tasks/new/audience` | New task wizard, step 2: people and groups | member |
| `/app/boards/<board_id>/tasks/new/review` | New task wizard, step 3: review and create | member |
| `/app/storage` | Files, quota, upload, links, deletion | member |
| `/app/calls` | Call route choice and this device's call history | member |
| `/app/membership` | State, trial, quotes, payments, credit, sponsorships | member |
| `/app/relay` | Relays operated, each with its stake and tier, probes, relay mode, epoch shares | member |
| `/app/token` | Vesting positions, claims and the token ledger | member |
| `/app/devices` | Devices with state, added and last active; approve and remove | member |
| `/app/settings` | Read receipts, wallets, sign out | member |
| `/app/epochs` | Epochs with their states | member |
| `/app/epochs/<number>` | One epoch's audit; treasurer actions when signed in as treasurer | member |
| `/app/treasury/whitelist` | Whitelist applications | treasurer |

**Entry and redirects.** `/signin` has the fields `Email` and `Password` and a `Sign in` button; `/signup` has the fields `Email` and `Password` and a `Create account` button. Every approve button on `/app/devices` is named `Approve` followed by the device's name. A visitor opening any `/app` route is sent to `/signin?next=<that route>`, and signing in returns them there, or to `/app` when there is no `next`. A signed-in account opening `/signin` or `/signup` is sent to `/app`. Setting up an account's first device shows the key dialog before `/app` opens; a pending device opens `/app` with the waiting notice. Signing out returns to `/signin`. When a session expires in the middle of an action, a toast says the session ended, the page goes to `/signin?next=<the current route>`, and anything being composed stays on the device as `Waiting to send.` A member opening `/app/treasury/whitelist` sees `Only the treasurer can open this page.` with a link back to `/app` and no application data. A suspended account sees the lapse notice at the top of every workspace page. Every workspace page carries a sidebar, a navigation landmark linking to `/app`, `/app/explore`, `/app/boards`, `/app/storage`, `/app/calls`, `/app/membership`, `/app/relay`, `/app/token`, `/app/devices`, `/app/epochs` and `/app/settings`. At any viewport 430 CSS pixels wide or narrower, every workspace page hides that sidebar and offers a button named `Menu` that opens the same links; a board's columns sit side by side in one row that pages sideways, each column at least 60 per cent of the viewport wide; and the introduction keeps `Skip the intro` on screen with its six stage labels in one horizontally scrolling row that never widens the page.

**Journeys.**

1. Sign up: open `/signup`, enter an Email and a Password, press `Create account`, read the key dialog, tick `I understand that nobody can restore this key`, press `Continue`, and arrive at `/app` with an empty queue reading `No conversations yet.`
2. Start a private group: from `/app` press `New conversation`, choose `Private group` on `/app/conversations/new` and press `Next`, add `NJ-MEMBER23` with `Add person` on `/app/conversations/new/people` and press `Next`, name it on `/app/conversations/new/name`, press `Create`, and land on the new conversation with a toast confirming it.
3. Approve a device: sign in on a second browser and see `Waiting for approval from one of your other devices.`; on the first browser open `/app/devices`, press `Approve Device 2`, and see `A new device can now read your messages. Added <when>.`
4. Remove a member: open the group's settings, press `Remove` beside a member, read `They keep what they already received. That's on their device and we can't reach it.`, confirm, and see `Key epoch <n>` on the settings page rise by one.
5. Join a public group: open `/app/explore`, choose `Open Relay Commons`, read `Anyone can join this group, so treat it as public. Encryption hides it from the relays, not from members.`, press `Join`, and see the same line above the composer.
6. Plan work: open `/app/boards`, press `New board`, enter `Launch Plan` as the `Board name` and press `Next`, keep the columns `To do`, `Doing` and `Done`, press `Create board`, then press `New task`, title it `Draft relay notice` in `To do`, add people or groups, create it, rename it `Publish relay notice`, open its chat and see the chat named `Publish relay notice`, then focus the card, open `Move`, choose `Doing`, and see the card in `Doing`.
7. Share a file: open `/app/storage`, pick a file with `Choose file`, press `Upload` and watch its progress, press `Share link`, choose an expiry and read `Anyone with this link can open the file. Expires <when>.`, then `Revoke` it and read `Link disabled. Copies already downloaded can't be recalled.`, then `Delete` the file and read `Removed from your storage. Pieces already distributed can't be recalled.`
8. Choose a call route: open `/app/calls`, read `Route privately, slower. Or connect directly, faster, and share your network address with them.` with `Private` selected, choose `Direct`, reload, and find `Direct` still selected.
9. Pay: open `/app/membership`, pick a rail, read the quote line, pay to its deposit reference, and watch the payment move from `Payment seen. Waiting for confirmation.` to an extended membership.
10. Run a relay: open `/app/relay` as `member4@example.com`, press `Start relay mode`, read `Other people's encrypted traffic will pass through your connection while this runs.`, then press `Start` and see `Stop relay mode` offered while it runs, or press `Cancel` and see `Start relay mode` still offered.
11. Settle an epoch: as `treasurer@example.com` open `/app/epochs/1`, read each relay's rounds, weight and share, press `Settle`, and see the epoch read `settled` with every share above zero marked paid.
12. Claim tokens: as `member@example.com` open `/app/token`, read `<claimable> claimable now. <locked> unlocks by <date>.` with a claimable amount above zero on the seeded position, press `Claim`, and see the claimable amount read `0 NJR` and the claim listed in the token ledger.
13. Read the sale terms: on `/` open Token Sale, tick `I am a private investor and a potential user of Nightjar`, press `Show the terms`, and read the Visioners Round terms and the statement that no tokens are sold on the page.
14. Apply to the whitelist: on `/whitelist` enter a `Wallet address`, sign the `Message to sign` and paste the `Signature`, continue to `/whitelist/details`, enter `Email` and `Amount in USD`, continue to `/whitelist/review`, press `Apply`, and read `Application received. It is not an allocation, and we'll be in touch.`
15. Exchange a message: in a second browser sign in as `member2@example.com`, whose first device is active at once, and leave it at `/app`; then from `/app` press `New conversation`, choose `Chat` and press `Next`, add `NJ-MEMBER23` with `Add person` and press `Next`, press `Create` on `/app/conversations/new/name`, type in `Message`, press `Send`, and see the text in the conversation; then in the second browser open the chat from the queue and read the same text.

**States.** Every list has an empty state: the queue reads `No conversations yet.`, boards read `No boards yet.`, storage reads `No files yet.`, devices always list at least this device, epochs always list the seeded epochs, and the token page with no positions reads `No vesting positions.` Every page and list shows a loading state shaped like the content it is waiting for. Every outcome of an action is reported with a toast in the product's own palette, announced to assistive technology, and every failure states its reason; an error never blanks or crashes a page. An unopenable message, an unavailable file and a pending device are states with their own lines, never errors. The attention states are `seen`, `underpaid`, `suspended` and its lapse notice, a pending device, `unavailable`, `Missed` and a stake below its tier.

**Display formats.** Wherever a page shows an amount, an NJR, USDC or USDT amount is in whole units with up to `6` decimals and no trailing zeros, followed by its asset code in capitals (`47.457626 NJR`, `15 NJR`); an XMR amount is the same with up to `12` decimals (`22.250476796 XMR`); an `app_store` amount is in dollars with two decimals (`$3.50`). `<asset>` is that capitalised code (`NJR`, `USDC`, `USDT`, `XMR`, `USD`). `<uptime>` is a whole percentage rounded down (`83%`). `<tier>` and `<lower tier>` are tier names as the tier table writes them. `<used>` and `<total>` are megabytes of `1048576` bytes with one decimal, rounded down (`0.3 MB`, `64.0 MB`). `<when>` and `<date>` are written `YYYY-MM-DD HH:MM UTC`. `<n>` is a whole number rounded down, `<node>` a relay's name, and `<sponsor>` the sponsor's contact code.

## UI/UX notes

The first thing someone should understand, on the public page and in the workspace alike, is that this product is discreet: nothing decorates, nothing is tracked, and what cannot be protected is said plainly. The register is a confident dark brochure outside and a quiet, operational messenger inside; the workspace is built for scanning and repeated action, and it never borrows the brochure's oversized type.

**Palette by role.** The ground is near-black neutral, raised surfaces step up to deep neutral, primary text is near-white neutral and quieter text is a light neutral one step down. One light, vivid lime does all the emphasis: the primary action on a page wears it and nothing else competes, its hover moves to a second light, vivid lime step (or to white on the brand button), and a mid, soft lime marks the pressed state. The one colour that means something has gone wrong is a light, vivid red, the alert red, and it appears nowhere else. Success wears the lime with a check mark and a word, and work in progress wears the quieter neutral with a still or turning indicator and a word, so no state is ever signalled by colour alone. States that need attention without being failures wear the light neutral text with a hollow ring mark and their word, never the red and never the lime. Hairline borders are white at low strength and are decoration, never the only sign of a boundary. The exact shades are yours, so long as those roles and exclusivities hold.

**Motion.** The motion character is eased: entrances decelerate into place, exits accelerate away, and state swaps use one symmetrical curve; every transition names the properties it moves, and those three are the only eased curves in the product; the repeating banners and the spinner move at a constant speed. Under a reduced-motion preference everything in Core features section 10 rule 7 applies, a progress ring shows current progress without animating, and every other animation resolves to its end state.

**Accessibility.** Text meets a contrast ratio of at least 4.5 to 1, and large text, icons and control boundaries at least 3 to 1, in both directions, lime on near-black and near-black on lime, and the secondary greys are measured rather than assumed. Full keyboard navigation reaches everything with a visible focus ring, icon-only controls carry labels, touch targets are at least 44 by 44 CSS pixels, and every content image carries alternative text while decorative drawings declare themselves decorative. The states nobody can see are announced: a message waiting to send, a group changing its keys, a payment waiting for confirmation, and above all a call connected directly.

**Components.** Every control has a resting, pointed-at, pressed, focused and unavailable appearance, and focus is never hover reused: on the near-black ground focus is drawn deliberately in the lime, clearly visible. Escape closes any dialog, destructive actions (removing a member, deleting a task or file, revoking a device or link) confirm first, and unavailable controls say why.

**Mode.** Dark only, designed fully; there is no light theme.

**Type.** Two faces only. The display face is a condensed, heavy, all-capitals face, openly licensed, and genuinely condensed and genuinely heavy: a default grotesque at a bold weight is not the same design. The text face is an openly licensed family used at exactly three weights, 400, 500 and 600. The rendered scale is exact and is pinned, size by size, in the Front-end specification's Typography table. Figures align in columns wherever amounts stack, on membership, relay, epoch and token pages.

**Shape and density.** Four corner treatments carry the whole design: a pill for buttons, a large soft corner for panels, the intro stepper and the skip control, a smaller soft corner for inputs and cards, and a full circle for the menu, close and unwrap controls. The hexagon is the brand's second mark. The public page is spacious and cinematic; the workspace is comfortable, with rows that read at a glance and hit areas at least 44 by 44 CSS pixels.

**Responsive.** The layout is designed at four named breakpoints, phone, tablet, desktop and wide, each declared once, and it holds at every viewport width between them. On a phone the workspace sidebar gives way to a menu, the board's columns page sideways one at a time, a card moves between columns through its `Move` menu rather than an off-screen drop, and the introduction rearranges rather than shrinking a phone inside a phone, with its stage labels in one scrolling row and the skip control on screen.

## Technical requirements

**Stack.** The app is server-rendered with islands of interactivity: **SvelteKit** (Svelte 5, served as a production Node build) renders every page on the server, so the public page's HTML arrives complete in the first response and reads whole before any script runs, and the workspace's interactive parts take over in the browser. The HTTP API is **Hono** on Node.js 20, mounted on the same origin under `/api`. The datastore is **PostgreSQL**, already running and reachable at `DATABASE_URL`. Outgoing mail goes over real SMTP to **Mailpit** at `SMTP_HOST` and `SMTP_PORT`, authenticating with `SMTP_USER` and `SMTP_PASS`, all read from the environment.

Allowed libraries: `@sveltejs/kit`, `@sveltejs/adapter-node`, `svelte`, `vite`, `hono`, `@hono/node-server`, `postgres` or `pg` for PostgreSQL, `nodemailer` for SMTP, `@node-rs/argon2` or `bcryptjs` for password hashing, `zod` for request validation, and `@noble/curves`, `@noble/ciphers` and `@noble/hashes` for Curve25519, Ed25519, AES-256 and hashing, on the server and in the browser. The app must work when it is opened over plain HTTP at an address other than `localhost`, where the browser withholds every feature it reserves for secure origins, so sealing, key generation and identifiers made in the browser cannot depend on such features.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL (`postgres`) and Mailpit (`mailpit`), and reaching for anything else is a contract violation.

**Auth.** App-implemented email and password with bearer tokens, plus wallet sign-in by signed challenge. Every member-only request carries `Authorization: Bearer <token>`, where the token is either an account `access_token` or a `device_token`; a device token authenticates everything its account's access token does, plus the device-scoped actions (posting envelopes and key packages, creating tasks and moves, creating files and uploading pieces, approving and removing devices, receipts and the sync feed). Passwords are stored only as salted hashes. Tokens are opaque, server-revocable and expire after `12` hours; a revoked device's token and a signed-out token are refused everywhere at once. Login, signup, wallet challenge and verify, health, waitlist, whitelist applications, link reads, and the two watcher endpoints need no bearer token; the watcher endpoints authenticate by signature instead.

**The chain watcher.** Rates and payments arrive only through `POST /api/watcher/rates` and `POST /api/watcher/payments`, each authenticated by an Ed25519 signature in `X-Watcher-Signature` over the exact raw request body, verified against the watcher public key `efe6e71259fd773f94f0a96ae30a706f1a74dc8a5fd275b71942f37b5f75ab1f`. Nothing else in the app can create a rate, confirm a payment or extend a membership.

**Sealing.** Keys are made in the browser and private keys never leave it. The browser seals message text, file contents, file names and types, board names, column labels and task titles before sending them, and the server treats every sealed field as opaque base64 it never interprets. Keys are agreed on elliptic-curve key pairs over Curve25519 and content is sealed with AES-256 in an authenticated mode, the two algorithms the product publishes; the long-term device key is never the key that seals a message. Calls in this environment are signalling and records only; no microphone or camera capture is required. Wallet addresses are `0x` plus 64 lowercase hex characters of an Ed25519 public key, and wallet signatures are 128 lowercase hex characters over the UTF-8 bytes of the stored challenge message.

**Health and logging.** `GET /api/health` returns `200` with `{"status": "ok"}` once the database is reachable and seeding has finished. The server writes structured JSON logs to stdout, one object per request with a request identifier, route, status and duration; no log line ever carries a token, a password, a signature, a sealed field, a waitlist or whitelist email, or a network address.

**Formats.** All timestamps are ISO 8601 in UTC with a trailing `Z`. Money is integers only: US prices in cents, rates in `usd_micros`, token amounts in millionths of an NJR (`_micro` fields), and chain amounts in each rail's base unit; stakes are whole NJR in `stake_tokens`. Identifiers in the API are strings.

**Invariants under simultaneous requests.** Each of these holds when the requests arrive at the same instant, not only one after another:

- one wallet challenge issues at most one session or application, and exactly one of several simultaneous uses succeeds;
- one `client_id` from one device in one conversation stores exactly one envelope, and one `client_id` on one board stores exactly one task;
- simultaneous file creations never take an account over its quota: exactly one of two that only fit one at a time is accepted;
- simultaneous reports that a payment has reached its depth decide it once, and extend a membership at most once;
- simultaneous settlement runs of one epoch pay each relay exactly one transfer;
- simultaneous claims on one position transfer its claimable balance exactly once;
- simultaneous applications from one wallet address produce exactly one application and one email;
- simultaneous waitlist requests for one address send at most one confirmation email in 24 hours.

A request that loses one of these races is refused as a conflict or answered with the outcome already recorded, and it never writes a second row, a second transfer or a second email.

**Public page byte budgets.** Loading `/` in a fresh browser with an empty cache at a desktop width, everything fetched before the page's load event totals at most `250000` bytes on the wire; of that, scripts total at most `150000` bytes and fonts at most `120000` bytes; no video or audio file is fetched at all; and no code for the wallet step is fetched before `/whitelist` is opened.

**Separation.** The public page and the workspace are separate builds within the one app: the public page loads no workspace code, and nothing the public page runs can read the workspace's keys, tokens or sealed data.

## Data model

Forty-two tables. All timestamps are UTC. Identifiers are opaque strings or integers, returned as strings by the API, and every `id` column holds exactly the identifier the API returns for that object (a challenge's `id` is its `challenge_id`, an envelope's is its `envelope_id`); `account_id`, `conversation_id` and `file_id` columns hold the API's identifiers too.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### Accounts and devices

- `accounts`: `id`, `email` (unique when present, lowercase), `password_hash` (nullable for wallet-created accounts), `contact_code` (unique), `role` (`member` or `treasurer`), `read_receipts` (boolean, default false), `call_route` (`private` or `direct`, default `private`), `created_at`.
- `sessions`: `id`, `account_id`, `device_id` (null for an account token), `token_hash`, `created_at`, `expires_at`, `revoked_at`.
- `devices`: `id`, `account_id`, `name`, `identity_key`, `state` (`active`, `pending` or `removed`), `added_at`, `approved_at`, `removed_at`, `last_active_at`, `last_seen_address`.
- `wallets`: `address`, `account_id`, `attached_at`, `detached_at`. An address is attached to at most one account at a time; its history of attachments is kept.
- `wallet_challenges`: `id`, `address`, `purpose`, `message`, `nonce`, `created_at`, `expires_at`, `used_at`. A challenge with `used_at` set, or with `expires_at` in the past, is never accepted.

### Conversations and messages

- `conversations`: `id`, `kind`, `sealed_topic` (null for public shapes), `public_name` (public shapes only), `owner_account_id`, `epoch` (integer from 1, the stored version the relay compares envelopes against, always one plus the count of the conversation's membership events), `closed_at`, `core_relay_id`, `created_at`.
- `conversation_members`: `id`, `conversation_id`, `account_id`, `standing` (`owner`, `member`, `broadcaster` or `subscriber`), `joined_at`, `left_at`. One row per period of membership; a member added again gets a new row, so the periods are the membership history.
- `membership_events`: `id`, `conversation_id`, `epoch`, `change` (`added`, `removed`, `left`, `joined` or `device_removed`), `account_id`, `created_at`.
- `envelopes`: `id`, `conversation_id`, `sender_device_id`, `client_id`, `epoch`, `clock`, `sender_seq`, `ciphertext` (text, the base64 exactly as posted), `accepted_at`. One row per `client_id` per sending device per conversation.
- `envelope_keys`: `envelope_id`, `device_id`, `sealed_key`.
- `key_packages`: `id`, `conversation_id`, `epoch`, `device_id`, `sealed_group_key`, `created_at`.
- `read_receipts`: `id`, `conversation_id`, `envelope_id`, `reader_account_id`, `created_at`.
- `sync_events`: `id` (the cursor order), `device_id`, `type`, `ref_id`, `created_at`.

`gap_before`, the conversation's `routing` and every history visibility decision are derived when read, never stored.

### Planner

- `boards`: `id`, `owner_account_id`, `client_id`, `sealed_name`, `created_at`.
- `board_columns`: `board_id`, `column_id`, `sealed_label`, `ordinal`.
- `tasks`: `id`, `board_id`, `client_id` (unique per board), `conversation_id` (unique), `sealed_title`, `created_at`, `deleted_at`.
- `task_placements`: `id`, `task_id`, `column_id`, `position`, `clock`, `device_id`, `created_at`. Every creation and move is kept; where a task sits is derived from them when read.
- `task_audience`: `task_id`, `member_account_id` or `group_conversation_id`. Readers are derived when read from the owner, these rows and the live membership of each named group.

### Storage

- `files`: `id`, `account_id`, `client_id`, `sealed_name`, `sealed_meta`, `piece_size`, `piece_count`, `created_at`, `completed_at`, `removed_at`.
- `file_pieces`: `file_id`, `piece_index`, `bytes`, `stored_at`. `state` (`uploading`, `available`, `unavailable`, `removed`) is derived from `files` and `file_pieces` when read.
- `file_shares`: `file_id`, `conversation_id`, `created_at`, `removed_at`.
- `file_links`: `link_token` (unique), `file_id`, `expires_at`, `revoked_at`, `created_at`.

### Calls

- `calls`: `id`, `conversation_id`, `caller_account_id`, `media` (`voice` or `video`), `route` (`relay` or `direct`), `state` (`ringing`, `active` or `ended`), `created_at`, `ended_at`.
- `call_rings`: `call_id`, `ring_id` (unique per call), `created_at`.

### Membership and payment

- `rail_prices`: `rail` (unique), `asset`, `price_usd_cents`, `decimals`, `confirmation_depth` (null for `app_store`). Quotes and settlement read prices and depths from it.
- `rates`: `id`, `asset`, `usd_micros`, `observed_at`, `received_at`.
- `quotes`: `id`, `account_id`, `beneficiary_account_id`, `rail`, `price_usd_cents`, `amount_due`, `rate_usd_micros`, `rate_observed_at`, `deposit_reference` (unique), `created_at`, `expires_at`, `settled_at`.
- `payments`: `id`, `rail`, `tx_hash` (unique per rail), `quote_id`, `amount`, `block_time`, `confirmations`, `store_state`, `state` (`seen`, `settled`, `underpaid`, `credited` or `refunded`), `amount_due_applied`, `shortfall`, `credit`, `settled_rate_usd_micros`, `settled_at`, `epoch_number`, `contribution_micro`, `njr_rate_usd_micros`. `quote_id` is null for the seeded epoch receipts.
- `memberships`: `account_id` (unique), `paid_until`, `trial_ends_at`, `sponsor_account_id`, `sponsorship_declined_at`. Sponsored days are derived when read from `payments` and `quotes`. `state` is derived when read.

### Relays, epochs and rewards

- `relays`: `id`, `name` (unique), `operator_account_id`, `registered_at`, `retired_at`. A relay's stake is the sum of its `stake_changes`, its registration included, derived when read.
- `stake_changes`: `id`, `relay_id`, `delta_tokens`, `created_at`, `unlocks_at`.
- `tiers`: `tier`, `min_stake_tokens`, `weight`, `effective_from`.
- `epochs`: `number` (unique), `opened_at`, `closed_at`, `settled_at`. `settled_at` is set once, by the settlement run after which no share above zero is unpaid; `state` is derived when read: `open` while `closed_at` is null, `settled` once `settled_at` is set, `settling` while some of its `distributions` are paid, and `closed` otherwise.
- `probe_rounds`: `id`, `epoch_number`, `issued_at`.
- `probes`: `round_id`, `relay_id`, `nonce`, `tier_at_issue`, `answered_at`. One row per relay per round.
- `distributions`: `epoch_number`, `relay_id`, `weight`, `share_micro`, `paid_at`. Written once, when the epoch closes, from the frozen snapshot; `paid_at` is set once.

### Token surface

- `token_schedules`: `schedule` (unique), `label`, `allocation_bp`, `event_bp`, `cliff_months`, `linear_months`.
- `token_event`: `launch_at`, one row.
- `token_positions`: `id`, `account_id`, `schedule`, `allocation_micro`, `created_at`. Claimed, claimable and locked amounts are derived when read; claimed is the sum of the position's `vesting` transfers.
- `ledger_transfers`: `id`, `account_id`, `kind` (`reward` or `vesting`), `amount_micro`, `epoch_number`, `relay_id`, `position_id`, `created_at`. At most one `reward` transfer per epoch per relay.
- `whitelist_applications`: `id`, `address` (unique), `email`, `intended_usd_cents`, `state` (`applied`), `created_at`.
- `waitlist_entries`: `email_digest` (unique, SHA-256 hex of the lowercased address), `email` (null once removed), `state` (`pending`, `confirmed` or `removed`), `confirm_token`, `remove_token`, `last_mail_at`, `confirmed_at`.

### Seed data

Seeding is part of the app's own first start. Every seeded relative time is measured from that first start.

- **Accounts:** the five accounts in User roles with their contact codes and the corpus password. Memberships: `member@example.com`, `member2@example.com`, `treasurer@example.com` and `member4@example.com` have `paid_until` thirty days after first start and a trial that ended the day before first start; `member3@example.com` has `paid_until` forty days before first start and a trial that ended sixty days before first start. No device is seeded for any account.
- **Public conversations:** the public group `Open Relay Commons` and the channel `Relay Bulletins`, each owned by `treasurer@example.com`, who is the channel's broadcaster; no envelopes.
- **Rails:** the five rows of the rail table in `rail_prices`.
- **Tiers:** the four rows of the tier table, effective from `2026-01-01T00:00:00Z`.
- **Relays,** all operated by `member4@example.com`, each with one stake change giving its current stake in whole NJR: `Kestrel` `25000`, `Heron` `10000`, `Osprey` `15000`, `Plover` `150000`, `Wren` `150000`, `Tern` `25000`, `Avocet` `15000`, `Sanderling` `10000`.
- **Epochs:** epochs `1` to `4` are closed and unsettled, each thirty days long, the first opening one hundred and fifty days before first start; epoch `5` is open, opened thirty days before first start, with no probe rounds and no receipts. The closed epochs carry exactly these rounds and receipts (a receipt on a dollar rail lists the NJR rate in force when it settled):

| Epoch | Probe rounds | Rounds answered, by relay and by the tier held when each round was issued | Receipts |
|---|---|---|---|
| `1` | `6` | Kestrel `6` at `level-2`; Heron `4` at `basic`; Osprey `3` at `level-2` and `2` at `level-1`; Plover `0` | three `njr` payments each with `amount` and `amount_due` `15000000`; two `usdc` payments at NJR rate `150000`; one `xmr` payment at NJR rate `140000` |
| `2` | `8` | Heron `8` at `basic`; Kestrel `7` at `level-2`; Osprey `5` at `level-1`; Wren `2` at `master` and `1` at `level-2` | four `njr` payments each with `amount` and `amount_due` `15000000`; one `njr` payment with `amount` `14925000` and `amount_due` `15000000`; three `usdt` payments at NJR rate `145000`; two `app_store` payments at NJR rate `155000` |
| `3` | `10` | Plover `9` at `level-1`; Tern `6` at `level-2` and `4` at `basic`; Wren `10` at `master`; Avocet `7` at `basic`; Sanderling `0` | six `njr` payments each with `amount` and `amount_due` `16071429`; four `xmr` payments at NJR rate `138500`; five `usdc` payments at NJR rate `151250` |
| `4` | `5` | Avocet `5` at `level-1`; Heron `3` at `basic`; Kestrel `2` at `level-2` and `2` at `level-1`; Tern `5` at `basic` | seven `usdc` payments at NJR rate `147000`; two `njr` payments each with `amount` and `amount_due` `15000000` |

- **Token surface:** the eleven schedule rows; the token event one hundred days before first start; one `visioners` position for `member@example.com` of `40000` NJR (`40000000000` millionths). No rates, quotes, payments beyond the epoch receipts, whitelist applications or waitlist entries are seeded.

Seeding must be idempotent - restarting the app must not duplicate rows.

## Front-end specification

### Provenance: what this specification is built from

The reference was captured as one route at three viewport widths and nine scroll positions each: twenty-seven screenshots, seven hundred and twenty-six network responses and a frozen evidence ledger. Its source separates three kinds of statement, and this brief keeps the distinction: an **observed implementation** is informational evidence of what the reference does, not an instruction; a **capability requirement** is normative and says what the build must do; an **addition** is normative, absent from the reference, and specified here on purpose. Names are tokenised in the source and re-cast here: the brand is Nightjar, the unit of account is NJR, the studio credited in the footer is Coldframe, and the host is whatever serves the app.

**The condition that governs everything below: the product does not exist yet.** Both applications are marked `Coming Soon`; the captured route is a single marketing and fundraising page describing a system that has not shipped, and its roadmap places the applications and the token generation event in the same future quarter. There was nothing to measure except the promises, so every claim about encryption, routing, storage, groups, calls, staking and rewards is a published claim converted into an obligation. **Scope:** build the workspace (identity, messaging, groups and channels, storage, the planner, calls and the subscription that pays for it), the relay network's contract with the client, and the accounting that pays operators. What stays out: an organisation hierarchy, an administrative console over other people's accounts, a compliance regime, and delegated roles beyond the standings a group needs and the one seeded treasury role; this is a product sold to individuals and small teams by public signup. Operating an actual sale of an investment instrument is excluded for a different reason: it is regulated, and this specification neither authorises it nor could.

The reference publishes five claims, numbered by its own feature blocks:

| # | Claim | Where this brief makes it true |
|---|---|---|
| 01 | Fully decentralized: a physical infrastructure network of user-run nodes; no profile stored | the relay network and identity features |
| 02 | Highest security standards: elliptic-curve end-to-end encryption, symmetric encryption at rest | sealed messages and storage |
| 03 | No data tracking: no logs, onion routing across random nodes to conceal the sender | the relay network, and no analytics anywhere |
| 04 | Private network segments: run your own node and make it a group's core node | the core node rule |
| 05 | New way of discussions: chats, private groups, public groups and channels, plus a planner whose tasks are chats | conversations and the planner |

What the reference publishes about money, and where each figure lands:

| Item | As published | In this build |
|---|---|---|
| Subscription | `$2.25` paying in the token, `$3.5` paying in two stablecoins, a privacy coin, or in-app purchase | the five rails and two prices |
| Trial | any user will have a free trial period | fourteen days, one per account and one per wallet |
| Regular node stake | `10 000` to `25 000` tokens | `basic`, `level-1` and `level-2` tiers |
| Master node stake | `150 000` tokens | the `master` tier |
| Operator share | `80%` of subscription tokens received in the previous epoch | the pool is eighty per cent of an epoch's contributions |
| Distribution basis | node level, and total operating time during the period | tier weight per answered probe round |

The reference also names three established messengers as the experience it intends to match, and two public blockchains in an analogy about node quality; this build carries neither comparison.

**What the capture could not see, and what this brief does about each gap:**

| Gap | What is missing | What this brief does |
|---|---|---|
| The entire product | both applications are marked unreleased; nothing about identity, messages, groups, storage, planner, calls, relays or accounting exists to be observed | those features are specification derived from published claims, by far the largest gap in the corpus the reference came from |
| The protocol | two algorithm names are published; no key schedule, no ratchet, no group scheme, no wire format | the sealed message rules state the properties the claim implies |
| The relay network | no node, no path, no routing behaviour was observed | the relay rules are derived from four paragraphs and one question's answer |
| The accounting | no epoch, stake, uptime measurement or settlement was observed | the epoch rules are derived from three sentences |
| The whitepaper | closed: downloaded, twenty-three pages with no extractable text, every page a single image, extracted, converted and read visually | it settled the storage reading, added shared links, and produced three defects |
| The protocol, still | the whitepaper names the same two algorithms as the page and no key schedule, ratchet or group scheme | the sealed message rules remain specification |
| Below the ninth scroll sample | the desktop page is about seventeen thousand pixels tall and nine frames do not reach its end | the supplementary page extraction supplies the copy |
| Hover | one delta captured across the whole page | the interactive states rule |
| The reduced-motion preference | no query captured | the reduced-motion rules are entirely requirement |
| The intro on mobile | scroll suppression interfered with the sample | the scroll-lock rules |
| Stylesheet sizes | reported zero, cache-served | not used as evidence |

**The two supplementary sources.** A full text extraction of the captured route supplied the intro stage names, the feature bodies, the answers to the questions, the roadmap entries and the footer, all below the ninth scroll sample, under a usage rule: copy and structure are usable, no colour, curve, duration or measured dimension is, and the ledger wins any disagreement. The whitepaper is the single outbound link on the route, a rendered artefact of twenty-three image pages; where it and the page disagree, both are recorded and the disagreement is itself the finding. Its effects:

| Effect | Where it lands |
|---|---|
| Settled the storage contradiction in the page's favour of neither reading | storage: local sealed store by default, sealed upload as a separate deliberate act |
| Added the shared-link capability, absent from the page entirely | shared links |
| Gave three exact node tiers where the page gives a band, and disagrees with it | the tier table and its reconciliation |
| Gave the supply, the nominal value and the chain | total supply of one hundred million NJR, a nominal value of fifteen US cents, a common token standard on a named layer-two chain |
| Turned one vesting schedule into eleven, with an arithmetic self-check | the eleven schedule rows and their reconciliation |
| Produced three defects of its own | the defects table below |

It did not close the protocol gap: it names the same two algorithms and no key schedule, ratchet or group scheme.

**What the source's acceptance checklist adds.** Nothing beyond the rules above: its twelve areas (the public page, identity, messages, groups, storage and the planner, calls, the relay network, money, epochs and rewards, vesting, the client, and integrity) are each restated as rules of the feature they belong to.

**Taxonomy.** The source places the product as a messaging workspace sold by public signup to individuals and small teams: public channels exist, but it is a workspace rather than a community, and a group owner administers a group, not a company.

**Confidence in the source, by area:**

| Area | Confidence | Basis |
|---|---|---|
| Route inventory | complete | one route, discovered and captured |
| Palette, radius, tokens | high | declared in stylesheets and read directly |
| Typography | high | twenty-one faces declared, a rendered scale measured |
| Motion values | high | five keyframe sets and eight curves recovered |
| The marquee | high | caught running, twice |
| Copy | high | full deck, corroborated by the extraction |
| Asset weight | high | seven hundred and twenty-six responses measured |
| Published commercial terms | high as published | prices, stakes and sale terms read directly and cross-checked against the whitepaper |
| Token supply, distribution and vesting | high as published | an eleven-row table that reconciles to its own stated event supply |
| Scroll behaviour | medium | interfered with on mobile |
| Hover and interactive states | low | one delta |
| The protocol | none, and the whitepaper did not help | specification |
| The relay network | none | specification |
| The accounting | none | specification |
| The application | none, and it does not exist | specification |

### Two surfaces, one brand

**One route.** Route discovery on the reference found one document: navigation is five in-page anchors (About, Features, Ecosystem, Token Sale, Subscribe) and the only outbound link was a whitepaper; the section ids recovered from its effects catalogue were `aboutSection`, `featuresSection`, `ecosystemSection` and `tokenSaleSection`. Anchors on one document are still navigation, which is why each is addressable, reachable from the keyboard, a history entry, and a place a deep link lands with the introduction already resolved.

**The marketing page is not the product.** Two surfaces share a brand and almost nothing else:

| Surface | Is | Built as |
|---|---|---|
| The public page | one document, anchors, an intro sequence, a waitlist, a token-sale surface | a brochure held to the public page byte budgets |
| The workspace | the application the page describes | an application holding private keys |

They are separate builds with separate budgets and separate threat models. The page is never given access to anything the workspace holds, and the workspace is not reachable by anything the page loads: the public page runs no workspace code, and the workspace's keys and session are never readable by the public page's scripts.

**What the page has instead of routes:** an intro sequence, five feature blocks, an ecosystem section, a token-sale section with a whitelist stepper, a roadmap, a set of frequently asked questions, and two subscription forms described as a waitlist. A single document carrying this much is long, so every section is deep-linkable and the page never depends on having been scrolled through in order.

### Palette and tokens

The scheme is stark: near-black grounds, a single acid-lemon accent, and greys between. The reference declared twenty-four values; their roles, carried as words:

| Value, in words | Uses on the reference | Role |
|---|---|---|
| white at one fifth strength (an rgba value) | 12 | hairline borders |
| black at two fifths strength (an rgba value) | 8 | scrims behind dialogs and over video |
| a light, vivid red | 6 | the alert red |
| white at three tenths strength (an rgba value) | 6 | borders, brighter |
| a near-black neutral | 5 | the ground |
| a deep neutral | 4 | a raised surface |
| white at two fifths strength (an rgba value) | 4 | borders, brightest |
| a light neutral | 2 | secondary text |
| a light, vivid lime | 1 | the brand accent |
| a second light, vivid lime | 1 | the accent, second step |
| a near-white neutral | 1 | light text |
| a quieter near-white neutral | 1 | light text, quieter |
| a mid, soft lime | 1 | the accent, darkened |
| two more deep neutrals | 1 each | two more near-blacks for surface steps |

**The tokens the product actually declares.** The reference declares five named tokens, and they are the only ones that belong to it: the basic brand lemon, the secondary lemon second step, the secondary dark grey, the secondary grey and the secondary grey second step. Five tokens is a complete system for this design and the naming is sound; what is missing is a name for the alert red and for the three surface steps, which the reference used unnamed, so a theme change reached five values and missed four. This build names all nine as tokens and uses nothing that is not a token.

**Forty-one properties that belong to somebody else.** Forty-six custom properties were computed on the reference's root, and forty-one of them were a third-party notification library's default theme published in full: its dark, light, info, success, warning and error colours, its spinner colours, its toast geometry, a stacking value above everything, and a six-stop rainbow gradient for a progress bar. A notification is part of this product's voice and gets this product's palette: toasts, their progress indicator and their error state use only the tokens above, no library's default theme is published on the document root, and no notification stacks above an open dialog.

### Shape, the hexagon, depth and states

**Shape.** The reference used many radii: the largest soft corner on panels, the intro stepper and the skip control; a smaller soft corner on inputs, the whitepaper button and cards; a pill on buttons; a full circle on the burger, close and unwrap controls; smaller corners on media and video; and a handful of one-offs. Two split corners joined an accordion item to its neighbour. Four radii carry the design (a pill, a panel, a card and a circle), and every one-off resolves into one of those four.

**The hexagon.** A six-sided figure clips content in three places, appears as a glyph in the hero headline and repeats as the mark in the marquee. It is the brand's second mark after the wordmark, and in this build it appears as a glyph in the hero headline and as the repeating mark between the phrases of both banners. Where it clips content it never clips text out of reach, and where it is decorative it is not announced.

**Depth.** The reference's stacking order ran as a contiguous scale of about a dozen steps, plus one value far above it from the notification library. A contiguous scale is disciplined; this build keeps one scale for everything, gives notifications a place inside it, and never lets a dependency sit above every future modal.

**Interactive states.** One hover change was captured across the whole reference page: the brand button's background moving from the lemon to white. One captured hover is thin evidence and the obligation stands regardless: every control has a resting, hover, active, focus and disabled appearance, focus is not hover reused, and on a near-black ground focus is drawn deliberately in the accent.

### Typography

**Twenty-one declared faces for a page that uses three.** The reference declared a variable display face across the full weight range and a text family as twenty separate static faces (nine weights, each normal and italic, with the heaviest appearing twice), and fetched only three files: the text family at regular, medium and semibold. Declare only the faces used: a build that ships all twenty ships eighteen it never renders, and a build that ships three while declaring twenty silently synthesises the rest the first time somebody sets a heading in light italic.

**The faces are woff, not woff2.** The reference served twenty-seven font responses in the older container. This build serves woff2 only, which is roughly a third smaller for the same outlines, subset to the characters used, one request per face.

**The rendered scale.** Only three weights ever render (400, 500 and 600). The display sizes are genuinely distinct and belong in the scale; the body sizes are 16px and 14px; and 13.3333px, which rendered two hundred and forty-three times on the reference as the compounding of a relative size inside a nested scale, is not a step and does not appear:

| Size | Weight | Line height | Used for |
|---|---|---|---|
| 110px | 500 | 110px | the hero headline, in the display face |
| 72px | 500 | 68px | section statements, in the display face |
| 60px | 600 | 60px | section titles |
| 44px | 500 | 48px | feature numbers and large figures |
| 40px | 600 | 40px | sub-section titles |
| 38px | 500 | 38px | pull statements |
| 28px | 600 | 32px | card and panel titles |
| 16px | 400 | normal | body text |
| 14px | 600 | 20px | labels, buttons and navigation |
| 14px | 400 | 20px | small text, captions and metadata |

**Display type is set solid or tighter** (110 on 110, 40 on 40, 60 on 60, and 72 on 68), which is correct for a condensed all-capitals display face and survives here. It also means the hero cannot wrap to three lines without the letters colliding, so the hero copy is written to fit two lines at every width.

### Motion

**What was recovered from the reference:** five keyframe sets, eight easing curves, fourteen transition declarations and two runtime animations caught running.

| Keyframe set | Does | In this build |
|---|---|---|
| a marquee | slides its strip left by exactly half its width | the repeating banners |
| a spinner | rotates one full turn | the in-progress indicator, still under reduced motion |
| a rise | lifts content from below into place | section entrances |
| a fade | brings opacity from nothing to full | reveal on scroll, over a page already complete |
| a stroke draw | retracts a circular ring's dash exactly once around | the circular progress ring on uploads and claims |

**The marquee.** Both caught animations were the same slow, constant-speed loop, infinite, on the headline strip and its content, carrying the invitation to know the product better separated by the hexagon. A marquee repeats its content twice and moves by exactly half its width, which is the only way its loop closes without a visible jump.

**The intro sequence.** The reference opens on a sequence with six named stages and a skip control, shown as a pill strip beneath a large phone playing a demonstration, and the sequence stops the page: the scroll root carried the smooth-scroll library's stopped state during the mobile capture. The sequence is skippable at any moment from the keyboard, the skip control is reachable before the sequence has loaded anything, scroll suppression has a guaranteed end (a visitor who never presses skip reaches the page, a visitor whose network stalls mid-sequence reaches the page, and a visitor arriving at a deep anchor never sees the sequence), each stage is addressable and the sequence can resume from a stage rather than only from the start, it does not autoplay under reduced motion, and a returning visitor does not sit through it again after a reload.

**The easing set.** The reference used eight cubic curves: one used four times, a decelerating curve that suits entrances; one that overshoots above one and settles back; four sharp accelerations that end abruptly, the signature of exits; and two more, each used once. This build names three: an entrance that decelerates, an exit that accelerates, and one symmetrical curve for state changes, and retires the rest. The overshoot is not used.

**Smooth scrolling, and what it cost the capture.** The reference's scroll root carried a smooth-scroll library's scrolling, smooth and stopped classes, and the library was fingerprinted by a runtime global and a surviving identifier. On mobile the sampled scroll positions sat at zero three times, went back to zero, and then jumped several thousand pixels, which is the library holding scroll during the intro and releasing it partway. A library that owns the wheel owns the reader's ability to leave: if this build smooths scrolling at all, anchor navigation, find-in-page, keyboard paging and the browser's own restoration of scroll position on a back navigation keep working, and it yields entirely under reduced motion. Scroll suppression is a state with an owner and a timeout; only the intro takes it, it releases on skip, completion and failure, and nothing else in the product takes that lock.

**Reduced motion.** No reduced-motion query was captured on the reference, against five keyframe sets, an infinite marquee, a scroll-driven intro and a smooth-scroll library. Under the preference: the marquee stops, the intro does not autoplay and its six stages remain available as stills with their copy, smooth scrolling yields to the browser's own, scroll-linked transforms resolve to their end state, and the spinner is replaced by a non-rotating indicator.

### The public page in detail

**Chrome.** A floating pill bar carries the wordmark, the anchors and a filled accent button, with pill controls and circular burger and close controls. The bar is fixed and overlaps content, so it has a background that guarantees contrast against whatever passes beneath it, including the animated gradients; a translucent bar over moving imagery would be legible for only part of every loop.

**The sections.** Five feature blocks, each with an icon, a number and an animated gradient where the reference had a video; an ecosystem section; a token-sale section; a roadmap of five dated entries; a set of questions; and two subscription forms. On the reference sixty-six elements started at zero opacity, including the ecosystem and token-sale sections, so the page revealed on scroll and would have been blank had the reveal failed; here every section is visible with scripting unavailable, with the observer unsupported, or under reduced motion.

**The waitlist.** Both forms on the reference were described as a waitlist rather than a subscription: `Join the waitlist to receive our newsletters`. This is the only place the page collects anything, and it collects an email address from people attracted by a promise of not being tracked, so the purpose is stated at the point of entry, in the form and not in a policy page: what the address is for, who holds it, how long, and how to be removed. Consent is explicit and unbundled, nothing else is collected alongside it, and the page carries no third-party analytics.

**The frequently asked questions.** Four, substantive rather than promotional: why privacy matters, why the operators cannot read anything, how the network compares to others, and why the service is paid. The reference animated the accordion on its grid rows, which is the right current technique for animating to an unknown height; the answers make falsifiable technical claims that the workspace honours, they are content rather than decoration, and each heading is a button whose state is announced, with its panel out of the reading order while collapsed.

**The roadmap.** Five dated entries running from a whitepaper through an equity round, two token sales, and the applications with the token event. A roadmap is data with dates and dates pass: every entry has a state, and the page shows whether a date was met or missed without an edit.

### Copy deck

Every string on the page, with the brand re-cast, the reference's grammatical errors corrected, and generic users never gendered. The reference's errors are recorded in the defects table below; the build ships the corrected text.

**Chrome and hero.** `About` `Features` `Ecosystem` `Token Sale` `Subscribe`; the hero reads `bringing back privacy to users`; the repeating banner reads `get to know Nightjar better` with the hexagon between repeats.

**The intro sequence.** Stage captions `Security`, `Chat`, `Voice messages`, `Storage`, `Task setup`, `Planner`; control `Skip the intro`.

**The two invitations beneath the intro.** `Share computing power, earn rewards` with `Get rewarded for your unused internet and computer resources by powering the Nightjar Network` and a `Find more` link to the ecosystem section; `Be among the first believers in Nightjar` with `Participate in our upcoming Token sale to get the best entry point into the Nightjar ecosystem` and a `Yes, I want it` link to the token-sale section.

**About and the waitlist.** `About`, then `Nightjar is the first distributed digital workspace that allows individuals and teams to communicate and collaborate effectively with each other using a completely secure and private ecosystem. The service combines the functionality of a messenger, a distributed file storage, and a simple distributed planning system (Kanban).` Then `Be among the first to know`, `Nightjar provides you with rich functionality, the highest reliability and privacy of your data. All your data and files transmitted or received by you will be securely encrypted on your device, and all connections by default will be encrypted using end-to-end encryption algorithms. Join the waitlist to receive our newsletters`, `Subscribe`, and the repeating ribbon `waitlist subscribe` separated by slashes.

**The five features.** `01 Fully decentralized`, `02 Highest security standards`, `03 No data tracking`, `04 Private network segments`, `05 New way of discussions`, each labelled `Feature`, and the link `Know more from our Whitepaper`.

**Ecosystem.** The banner `Ecosystem operated by users`; `Provide resources to earn`; `End-user experience`; `Staking amount will vary from 10 000 to 25 000 Tokens for regular nodes and 150 000 for master nodes`; `Download Whitepaper`; and the two prices with the currency symbol before the figure in both: `$2.25 when paying NJR tokens` and `$3.50 when paying in USDC / USDT, XMR or via in-app purchases`.

**Availability.** `Whitepaper` with `Download`; `Install on mobile` and `Install on desktop`, each `Coming Soon`.

**Token sale.** `be a part of a new ecosystem`; `Purchase`; `Nightjar token utility` with `Discount`, `Rewards`, `Resources` and `Nightjar ecosystem`; the Visioners Round terms of Core features section 9 rule 2; `Whitelist`; `Apply`; `Connect your wallet to continue`; `Connect wallet`.

**Roadmap and footer.** `Nightjar Roadmap`, the five entries with every quarter written in capitals (`Q3 2025`, `Q2 2026`, `Q3 2026`); `FAQ`; `Still have questions?`; `Contact our support team`; `All rights reserved (C) Nightjar <current year>`; `Powered by Coldframe`.

**New copy the workspace needs.** Written in the reference's register: direct, technical, unembarrassed about what it cannot do.

| Slot | String |
|---|---|
| Key created, the warning | `This key is the only way into your account. Nobody can restore it, including us.` |
| Device enrolled | `A new device can now read your messages. Added <when>.` |
| Device removed | `That device can no longer read anything sent from now on.` |
| Removal, honest | `They keep what they already received. That's on their device and we can't reach it.` |
| Re-keying | `Updating this group's keys.` |
| Undecryptable | `This message can't be opened on this device.` |
| Public group, at joining | `Anyone can join this group, so treat it as public. Encryption hides it from the relays, not from members.` |
| Queued, not sent | `Waiting to send.` |
| Core node chosen | `This group's traffic will go through <node>. It will see when the group is active, and if it goes offline the group falls back to the open network.` |
| Relay operator notice | `Other people's encrypted traffic will pass through your connection while this runs.` |
| Call routing choice | `Route privately, slower. Or connect directly, faster, and share your network address with them.` |
| Call routed directly | `Direct connection. They can see your network address.` |
| Rate quote | `<amount> <asset>, at a rate from <when>. Expires in <n> minutes.` |
| Quote expired | `That quote has expired. Here's a fresh one.` |
| Payment pending | `Payment seen. Waiting for confirmation.` |
| Underpaid | `<amount> short. Send the difference or we'll return it.` |
| Membership lapsed | `Membership expired. Nothing has been deleted. Sending stops until you renew.` |
| Trial | `Free trial, <n> days left.` |
| Sponsored | `<sponsor> is paying for your membership.` |
| Storage quota | `<used> of <total>. New files will be refused at the limit.` |
| File unavailable | `This file's pieces are no longer on the network.` |
| Deletion, honest | `Removed from your storage. Pieces already distributed can't be recalled.` |
| Epoch settled | `Epoch <n> settled. Your share: <amount>, from <uptime> uptime at <tier>.` |
| Stake below tier | `Your stake is below <tier>. This node earns at <lower tier> until it's topped up.` |
| Whitelist applied | `Application received. It is not an allocation, and we'll be in touch.` |
| Vesting | `<claimable> claimable now. <locked> unlocks by <date>.` |
| Link created | `Anyone with this link can open the file. Expires <when>.` |
| Link revoked | `Link disabled. Copies already downloaded can't be recalled.` |
| Link expired, to the recipient | `This link has expired.` |

### Zero-asset substitution

The reference's asset manifest, and what replaces each class:

| Class | On the reference | Replaced by |
|---|---|---|
| Video | two hundred and thirty-two responses, twelve distinct clips | animated gradients drawn live, and an illustrated intro |
| Feature icons, roadmap illustrations, glyphs | one hundred and thirty-five PNG images | inline vectors |
| Typefaces | twenty-seven responses, three faces used | openly licensed woff2 faces |
| Inline vectors | forty-five SVG | transcribed vectors |
| Application-store badges | two | not replaced: omitted |

**The video.** Eleven of the twelve clips sat behind or beside text as decoration, abstract motion in the palette; each becomes a slow drift across a two-stop gradient with grain, or a looping vector animation of the hexagon, costing kilobytes and carrying the same meaning. **The intro is different and is not substituted with footage**: it showed a messenger that has never run, so the build ships the six stages as an illustrated sequence drawn as vectors with their captions, and adds real footage only when there is a real product; generating a fake screen recording would be manufacturing evidence of a working product.

**The illustrations and icons.** Five feature icons, four roadmap illustrations, a locker glyph and section imagery, all flat, small and single-purpose, are drawn as inline vectors in the accent and the greys, following the current colour so they follow the theme; the locker in the hero sits inside the hexagon clip and becomes two shapes. The two that are truly photographic are served in a compressed photographic format at display size.

**The typefaces.** A condensed all-capitals display face and a text family at three weights, substituted by openly licensed equivalents, woff2, subset, one request per face; the display face carries the whole personality of the page, so its substitute is genuinely condensed and genuinely heavy.

**Inline vectors.** The structural ones are small (a plus, a device outline, a wordmark) and are transcribed; the hexagon needs no file at all.

**The application-store badges** carried a named platform's exact brand colours. They are another company's trademarks with published usage rules, and there is no listing to link to, so they are omitted and the unreleased state is shown as text.

### Responsive behaviour

**The queries.** The reference used six media queries at five distinct widths: a wide maximum width used eight times, a small phone maximum used four times, a tablet maximum used three times, a screen query with a tablet minimum width used twice, one unexplained width between tablet and laptop used once, and a screen query with a maximum width one pixel below the tablet boundary used once. Two inconsistencies follow: the tablet boundary was written two ways, one pixel apart, and the tablet maximum and minimum overlapped at exactly that width. This build declares four named breakpoints once (phone, tablet, desktop and wide), each boundary written one way, and drops the unexplained width.

**Scroll depth.** The reference document was about seventeen thousand pixels tall at desktop, slightly taller at tablet, and interfered with on mobile; a tablet document taller than the desktop one usually means the two-column arrangement collapses before the type has reflowed, so this build reflows type before it collapses columns.

**What moves under scroll.** Six selectors changed at desktop and four at tablet: the marquee content and headline, a vector use element, two trapezoid sections and the about section, the marquee accounting for most of it. Two sections have angled edges, and a section whose edges are angled has a different safe area at every width: text never enters the angle, and on a narrow screen the angle never consumes so much height that it becomes the section.

**The intro on a small screen.** The intro is a phone rendered inside a phone. On a narrow viewport the arrangement changes rather than shrinking: the six stage labels become a horizontally scrolling strip that never widens the page, and the skip control never moves off screen.

**The workspace at small widths.** The workspace is a messenger, a phone product first. The board is the surface that resists a narrow screen most: its columns become a paged arrangement, and moving a card between columns works without a pointer and without an off-screen drop target.

### Accessibility

**The intro is the first barrier.** It is reachable and dismissible from the keyboard before anything else, focus moves into it when it begins, and the skip control is the first focusable thing on the page; a sequence that takes the scroll and cannot be dismissed without a pointer has locked a reader out entirely.

**The marquee** pauses on hover and on focus, stops under reduced motion, and because its content is duplicated to make the loop close cleanly, the duplicate is hidden from assistive technology so the phrase is announced once.

**Contrast on a near-black ground.** The accent on the ground and the ground on the accent are two different checks and both are needed, since the brand button inverts to white on hover. The secondary greys on the ground are the risk and are checked rather than assumed, and the hairline borders are decoration and never the only indication of a boundary.

**The accordion.** The heading is a button, its expanded state is announced, the panel is out of the reading order while collapsed, and the animation never prevents the panel being reached immediately by keyboard.

**The workspace.** Everything is operable without a pointer, and three surfaces need naming: the board, where moving a card has a keyboard path that does not depend on dragging; calls, where answering, declining and ending are reachable instantly; and message history, where a long list that recycles rows never breaks the reading order or loses focus. A message that failed to open is announced as such rather than rendering as empty.

**Announcing what cannot be seen.** A message queued rather than sent, a group that has re-keyed, a call routed directly rather than privately, and a payment pending confirmation are announced. The privacy-relevant ones are not optional: the call routing changes what a third party learns, and a reader who cannot see the indicator is still told.

**Language.** The reference carried a grammatical error in several feature blocks and referred to a generic user with a masculine pronoun. The copy is edited and generic users are not gendered; a reader relying on a screen reader hears every error at dictation speed.

### Client obligations and compound cases

**The client holds the only copy.** Keys, message history, the storage index, the board and the call history live on the device; there is no server-side readable copy to fall back on.

**Offline is the normal state.** The app opens, reads history, composes messages, moves cards and takes notes with no connection at all, and reconciles when one returns; a queued action is visible as queued, not as sent, because there is no server acknowledging receipt, only a relay accepting a parcel.

**Convergence without a coordinator.** Message order, the board, the storage index, read state and group membership are all shared state with no arbiter, and this build uses one rule for all of them: the logical clock decides, the device identifier breaks ties, and the arrival order never matters.

**The cryptography stays off the interface.** Sealing a large file, opening a long history and deriving group material are expensive, and they run without freezing the interface; a long operation reports progress and can be interrupted.

**The local store is a security boundary.** What the browser keeps is itself sealed under a key held only by that browser; the workspace locks after `15` minutes idle and on demand, and the locked state shows nothing decrypted and leaves no decrypted preview on screen. Search runs over content only the device can read, so its index is built on the device and is as sensitive as the content.

**History is unbounded and the device is not.** The conversation list, a long history and a large board render without holding everything at once, and the storage index has a retention setting the owner controls.

**Client compound cases, each answered once:**

| Case | This build's answer |
|---|---|
| A second device is enrolled while the first is offline composing | the queued message is sealed to the devices active when it is finally sent, which includes the new device if it was approved by then |
| A group re-keys while the reader is scrolled into its history | messages on screen stay open; new messages use the new epoch, and the reader sees `Updating this group's keys.` until their device has the new material |
| Two devices move the same card while both are offline | the placement with the higher clock wins on reconnection, ties to the higher device identifier |
| A large attachment is sealing when the application locks | the sealing is cancelled, its plaintext is discarded, and the upload restarts after unlock |
| A task is un-shared from a group while a member of that group is typing into its chat | the draft stays on that member's device and sending it is refused with the stale-epoch reason |
| The application opens for the first time on a device with no network | it shows that a first sign-in needs a connection, because identity is created with the relay |
| A call arrives while a re-key is in progress | the call authenticates against the device keys, which a re-key does not change |
| History exceeds the device's storage while a file download is in flight | the download pauses and the owner is asked which history to let go; nothing is dropped silently |

### Architecture of the two systems

**What the reference is built on**, as observed: an application framework (definitive, from its static asset path, with a version literal found in a bundle), a smooth-scroll library (definitive from its state classes, and high confidence from a runtime global and a surviving identifier), four further version literals, and a notification library shipping its entire default theme. The reference did not publish its source maps, which was the right call, and this build publishes none either.

**The marketing page, architecturally**, is a statically rendered document with a scroll-driven intro, a marquee, an accordion, two forms and a wallet step; the wallet step is the only part touching a user's credentials, so its code loads on demand when the reader reaches the whitelist stepper and never on the first paint.

**The workspace, architecturally**, keeps accounting apart from messaging. Each relay is meant to learn one hop in each direction and nothing more: the sending browser picks the path, paths change during a session, and a relay that drops, delays, duplicates or reorders traffic is routed around. The accounting side settles epochs, holds stakes and pays operators and never sees a message, settlement is computed from the frozen snapshot, and who may read something is decided once, by membership, so the public page loads no workspace code and no domain screen decides access on its own.

**Network and accounting compound cases, each answered once:**

| Case | This build's answer |
|---|---|
| An epoch closes while a node is mid-restart | the node earns for the rounds it answered before the close; a round it missed is not counted |
| A subscription is paid on the last block of an epoch and confirms in the next | it belongs to the epoch open when it settles |
| An operator unstakes below their tier threshold between the snapshot and the payout | the payout uses the snapshot; the new tier applies from the next round issued |
| A settlement job is retried after a partial failure while a stake is being withdrawn | the retry pays only unpaid relays, from the snapshot |
| A group's chosen core node stops relaying but stays reachable | it misses the next probe round, the group falls back to open routing and is told, and the relay earns nothing for that round |
| A member's payment lapses while they hold a group's material | sending stops; the material stays on their device, and nothing can take it back |
| The exchange rate moves between quote and settlement across an epoch boundary | the payment's block time decides the rate, and the moment it settles decides the epoch |
| A relay is paid for carrying traffic it dropped | it is paid only for probe rounds it answered, and nobody's stake is slashed |

### Performance

**The measured weight of the reference**, one route at three widths: about seven hundred and fifty-four megabytes of MP4 video across two hundred and thirty-two responses (the heaviest single document recorded anywhere in its corpus), about thirty megabytes of PNG images across one hundred and thirty-five, about one and a half megabytes of application JavaScript across two hundred and seven responses, nearly a megabyte of woff fonts across twenty-seven, some octet-stream downloads, forty-five small SVG files, and cache-served CSS. Twelve distinct clips were fetched two hundred and thirty-two times: an intro at full high definition, a loading clip, one per feature block, two in the main information blocks, and four in the token-utility blocks, most decorating sections many visitors never reach, all at full high definition though they played in small boxes behind text.

The rules that answer it: the intro renders at first paint as a still illustration, nothing below the fold is fetched before it is near, every animated background is muted, silent and drawn rather than streamed, the flat images are vectors and no PNG image is fetched, the fonts are woff2 files served from the app's own origin, and the byte budgets in Technical requirements hold. **The blanket transition:** the reference set a transition on all properties on more than fourteen hundred elements; this build declares transitions per property, as the reference's own authored rules for the accordion and the colour changes already did.

### Defects on the reference, and this build's answer to each

| Defect | This build |
|---|---|
| Seven hundred and fifty-four megabytes of video on one document | no video; drawn gradients and an illustrated intro |
| Fonts in the older container | woff2 only |
| Twenty-one faces declared, three rendered, three fetched | declare only the faces used |
| 13.3333px rendered two hundred and forty-three times | not a step; resolves to 14px |
| Forty-one of forty-six root custom properties belong to a notification library | toasts use the product's tokens only |
| That library's stacking value sits above a disciplined scale | one scale with notifications inside it |
| The alert red and three surface greys used but not tokenised | nine named tokens |
| A transition on all properties on more than fourteen hundred elements | transitions declared per property |
| Eight easing curves, seven used once each | three named curves |
| The tablet boundary written two ways; the tablet width overlapping itself | four named breakpoints, each declared once |
| Scroll suppression observed misbehaving on mobile | one owner, a guaranteed end |
| Sixty-six elements at zero opacity awaiting a reveal that may not run | the page is complete without the reveal |
| The whitepaper contradicts itself on four token allocations | the eleven-row schedule table, reconciled |
| The stated initial market cap excludes one of the two things its label names | the whitepaper page states supply and event supply from the schedule table |
| The page and the whitepaper disagree on the lowest node stake | the reconciled tier table |
| The heading DISRIBUTION misspelt at display size in the whitepaper | the whitepaper page is proofread |
| The token-sale date contradicts the roadmap | one date for the sale everywhere |
| The footer year contradicts the roadmap | the footer shows the current year |
| Distributed file storage contradicts storage only on end devices | local sealed store by default, sealed upload as a deliberate act |
| `Know more from out Whitepaper` | `Know more from our Whitepaper` |
| `All right is reserved` | `All rights reserved` |
| `Power by` | `Powered by` |
| `Still have a questions?` | `Still have questions?` |
| Doesn't store or analyzes | the network limits page is proofread |
| A doubled and before leave it on | the relay page is proofread |
| A generic user referred to with a masculine pronoun | no gendered generic users |
| The currency symbol after the figure in one block, before it elsewhere | before the figure everywhere |
| Two roadmap quarters lower case where three are upper | every quarter in capitals |

Six of these are substantive: the video weight; the date contradiction; the two sources disagreeing about the lowest node stake; and, inside the whitepaper, four allocations differing between two of its own pages plus a market capitalisation excluding one of the two things its label names. The financial contradictions matter more than their size suggests, because they are the numbers a prospective purchaser reads. The storage contradiction that looked substantive is resolved: files live only on the member's devices, and uploading a sealed copy to the network is a separate thing the member chooses to do.

### Refusals

Four, and each is kept: **a fabricated product demonstration** (the intro video showed a messenger that does not exist, and generating a replacement would manufacture evidence that an unreleased product works, on a page raising money against it); **the application-store badges** (third-party trademarks linking to listings that do not exist); **the comparisons** (other people's marks used to borrow credibility a rebuild has not earned); and **operating the token sale** (the interface is specified and the activity is not authorised). None of the first three is a criticism of the reference, which is entitled to its own footage, listings and comparisons.

### Additions beyond the reference

| Addition | Why it exists |
|---|---|
| Device enrolment as an explicit, listed, revocable act | it is the operation that widens who can read everything |
| A device list with last-seen and removal | no session surface was published |
| The key-loss consequence stated at key creation | with no profile there is no recovery |
| Message keys used once, with forward and post-compromise properties | two algorithms are named and none of this is |
| Authenticated encryption, and context binding on every seal | the threat model is intermediaries |
| Verifiable ordering, duplicate suppression, idempotent send | relays are lossy and unordered by construction |
| An undecryptable-message state | re-keying guarantees it will occur |
| Location sharing made explicit, one-shot, expiring | the one payload still sensitive after decryption |
| Symmetric, optional read receipts | a product about not being observed |
| Group re-keying with no coordinator, and offline convergence | membership is cryptographic state |
| An honest statement of what public groups do and do not protect | encryption over open membership protects from relays only |
| Device-side blocking and group removal | an unreadable network cannot moderate centrally |
| Sealed filenames, sizes and types | metadata is disclosure |
| Padding to size classes, as a stated trade | chunk size reveals length |
| An honest deletion state | distributed blocks cannot be recalled |
| File availability as a first-class state, with stated redundancy | no central store means availability is not guaranteed |
| A storage quota | unbounded cost falls on fixed-share operators |
| Task audiences composing individuals and groups, with re-keying | a task is a chat |
| Board convergence with no coordinator | shared mutable state, no arbiter |
| Media transport separated from message transport | a call cannot ride the message layer |
| The routing choice on a call, stated to the user, private by default | the honest limit of onion-routed real time |
| Client-chosen paths, rotated, with misbehaving relays routed around | a network that assigns routes can assign its own |
| A published statement of what timing and volume still reveal | the limit of the claim |
| The core-node trade stated at the point of choice | a single point of observation and failure |
| A duty of care for the non-technical relay operator | strangers' traffic crosses their connection |
| Rate quoting with a source, a staleness bound and an expiry | two prices, five rails, none of them the quoted currency |
| Payment as a progression with a stated entitlement point | chain payments are not moments |
| Under, over and late payment outcomes; idempotent crediting | all three are ordinary |
| Lapse suspends and never deletes | the keys are irrecoverable |
| A stated trial limit that does not require the data the product refuses to hold | a genuine tension, named rather than dissolved |
| Sponsored membership without visibility of the recipient | the utility is published and its privacy consequence is not |
| An epoch, stake, uptime and distribution model | the published formula is one sentence |
| Level weighting, uptime measurement and pool composition made explicit | each changes every payout and none is published |
| Settlement idempotent, snapshot-frozen, resumable and auditable | its failure mode is paying twice |
| A stake lifecycle, and a decision on slashing | neither is published |
| Vesting computed from allocation and elapsed time, claims idempotent | a stored running total drifts |
| The cliff's accrual behaviour made explicit | two readings give different month-four balances |
| The whitelist as an application, not an allocation | the copy says requests are reviewed |
| One convergence strategy across all shared state | five interacting strategies are worse than one |
| Cryptography off the interface thread, interruptible, with progress | a wait with no progress is a hang |
| Local store encrypted at rest, with an idle lock | the store is a security boundary |
| Retention the owner controls | history is unbounded and devices are not |
| A shared-link capability with scope, expiry and revocation | the whitepaper adds it and says nothing of its lifetime |
| One vesting function over eleven schedule records | a code path per round does not survive the twelfth |
| A reconciliation over the distribution table | the allocations and the event supply must agree, and can be checked |
| A stated reconciliation between the page's stake band and the whitepaper's tiers | two published sources disagree |
| Twenty-nine new copy strings | the product had no interface yet |
| A performance budget far below the reference's own weight | seven hundred and fifty-four megabytes on one page |

Deliberately not added: an organisation hierarchy, an administrative console over other accounts, delegated roles beyond the one seeded treasury role, an audit regime, or any capability that would let the operator read, moderate or recover a user's content. The last is not a gap; it is the product.

## Constraints

- One product, open signup, two account roles; no organisation, tenancy, administrative console over other accounts, moderation queue or audit regime.
- No readable copy of any member content on the server, and no feature that would let anyone at Nightjar read, recover or moderate it.
- No real blockchain, wallet extension, card, bank or application-store integration: chain and store facts arrive only as signed watcher events, and no token is ever sold or transferred outside the app's own ledger.
- No push notifications, no SMS, and no email other than the waitlist confirmation and the whitelist acknowledgement.
- No third-party analytics, fonts, scripts or trackers loaded at runtime, and no external network calls at runtime.
- No native mobile or desktop application, no application-store badges, no product footage, and no comparison to any named messenger or blockchain.
- A conversation of `10000` envelopes opens by fetching only its newest `50`, and a board of `500` cards and a storage page of `500` files open complete.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief are already running and reachable at their environment variables: PostgreSQL (`postgres`) at `DATABASE_URL`, and Mailpit (`mailpit`) at `SMTP_HOST` and `SMTP_PORT` with `SMTP_USER` and `SMTP_PASS`. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. Every request and response body is JSON unless a row says otherwise. A successful call returns the named shape; an invalid, unauthorized or refused call is rejected as a client error (never a `5xx`, never a silent success), with a body carrying `reason` and `message`, and where a row names a `reason` value that value is used. A conflict between simultaneous requests is answered `409` or with the outcome already recorded. Anything not listed here is yours to design.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `200` `{"status": "ok"}` |
| `POST /api/auth/signup` | `{"email", "password"}` | `201` `{"access_token", "account_id", "contact_code"}` |
| `POST /api/auth/login` | `{"email", "password"}` | `200` `{"access_token", "account_id", "contact_code"}` |
| `POST /api/auth/logout` | bearer only | success with no body required; that token stops working |
| `POST /api/auth/wallet/challenge` | `{"address", "purpose"}` with `purpose` one of `sign_in`, `connect`, `whitelist` | `201` `{"challenge_id", "message", "expires_at"}` |
| `POST /api/auth/wallet/verify` | `{"challenge_id", "address", "signature"}` | `200` `{"access_token", "account_id", "contact_code", "created"}` |
| `GET /api/me` | bearer | `{"account_id", "contact_code", "role", "email", "settings": {"read_receipts", "call_route"}, "wallets": [address]}` |
| `PATCH /api/me/settings` | `{"read_receipts"}` and/or `{"call_route"}` | the `settings` object |
| `POST /api/me/wallets` | `{"challenge_id", "address", "signature"}` with a `connect` challenge | `{"wallets": [address]}` |
| `DELETE /api/me/wallets/{address}` | bearer | `{"wallets": [address]}` |
| `POST /api/devices` | `{"identity_key"}`, base64 of a 32 byte public key | `201` `{"device_id", "name", "state", "device_token"}` |
| `GET /api/devices` | bearer | array of `{"device_id", "name", "state", "added_at", "approved_at", "last_active_at"}` |
| `POST /api/devices/{device_id}/approve` | device token of an active device of the same account | the device object with `state` `active` |
| `DELETE /api/devices/{device_id}` | device token of an active device of the same account | the device object with `state` `removed` |
| `GET /api/directory/{contact_code}` | bearer | `{"contact_code", "devices": [{"device_id", "identity_key"}]}`, active devices only |
| `POST /api/conversations` | `{"kind", "members": [contact_code]}` plus `sealed_topic` for private shapes or `public_name` for public shapes | `201` the conversation object |
| `GET /api/conversations` | bearer | array of conversation objects the account currently belongs to |
| `GET /api/conversations/{conversation_id}` | bearer | `{"conversation_id", "kind", "sealed_topic", "public_name", "owner_contact_code", "epoch", "closed", "members": [{"contact_code", "standing"}], "routing": {"mode", "relay_id", "fell_back"}}` |
| `GET /api/explore` | bearer | array of `{"conversation_id", "kind", "public_name", "member_count"}` for public groups and channels |
| `POST /api/conversations/{conversation_id}/members` | `{"contact_code"}` | the conversation object |
| `DELETE /api/conversations/{conversation_id}/members/{contact_code}` | bearer | the conversation object |
| `POST /api/conversations/{conversation_id}/join` | bearer | the conversation object |
| `POST /api/conversations/{conversation_id}/broadcasters` | `{"contact_code"}` | the conversation object |
| `POST /api/conversations/{conversation_id}/close` | bearer | the conversation object with `closed` true |
| `GET /api/conversations/{conversation_id}/devices` | bearer | `{"epoch", "devices": [{"device_id", "contact_code", "identity_key"}]}` |
| `PUT /api/conversations/{conversation_id}/core-node` | `{"relay_id"}`, or `{"relay_id": null}` to clear | the conversation object |
| `POST /api/conversations/{conversation_id}/envelopes` | device token; `{"client_id", "epoch", "clock", "sender_seq", "ciphertext", "sealed_keys": [{"device_id", "sealed_key"}]}` | `201` new or `200` repeat: `{"envelope_id", "client_id", "epoch", "clock", "sender_seq", "accepted_at"}`; a stale epoch is refused with `reason` `stale_epoch` and `current_epoch`; a device not entitled is refused with `reason` `device_not_entitled`; a suspended membership is refused with `reason` `membership_suspended` |
| `GET /api/conversations/{conversation_id}/history` | `limit`, default `50`, at most `200` | array, in the pinned order, of the last `limit` visible envelopes: `{"envelope_id", "client_id", "sender_device_id", "sender_contact_code", "epoch", "clock", "sender_seq", "ciphertext", "sealed_key", "gap_before", "accepted_at"}`, with `sealed_key` for the calling device or `null` |
| `POST /api/conversations/{conversation_id}/key-packages` | device token; `{"epoch", "packages": [{"device_id", "sealed_group_key"}]}` | `201` `{"epoch", "count"}` |
| `POST /api/conversations/{conversation_id}/receipts` | device token; `{"envelope_id"}` | `201` `{"envelope_id"}` |
| `POST /api/conversations/{conversation_id}/files` | `{"file_id"}` | `201` `{"file_id", "conversation_id"}` |
| `DELETE /api/conversations/{conversation_id}/files/{file_id}` | bearer | success |
| `GET /api/sync` | device token; `after` (a cursor, optional), `limit`, default `100`, at most `500` | `{"items": [...], "next_cursor", "has_more"}`; every item has `cursor`, `type` and `conversation_id`; `envelope` items add the history fields; `membership` items add `epoch`, `change` and `contact_code`; `key_package` items add `epoch` and `sealed_group_key`; `receipt` items add `envelope_id` and `reader_contact_code`; `call` items add `call_id`, `media`, `route`, `state` and `ring_id` |
| `POST /api/boards` | `{"client_id", "sealed_name", "columns": [{"column_id", "sealed_label"}]}` | `201` `{"board_id", "sealed_name", "columns": [{"column_id", "sealed_label"}]}` |
| `GET /api/boards` | bearer | array of boards the account owns or reads a task on |
| `GET /api/boards/{board_id}` | bearer | `{"board_id", "sealed_name", "columns": [{"column_id", "sealed_label", "tasks": [task_id]}]}`, tasks in board order, only tasks the caller reads |
| `POST /api/boards/{board_id}/tasks` | device token; `{"client_id", "sealed_title", "column_id", "position", "clock"}` | `201` new or `200` repeat: the task object |
| `GET /api/tasks/{task_id}` | bearer | `{"task_id", "board_id", "client_id", "conversation_id", "sealed_title", "column_id", "position", "readers": [contact_code], "epoch"}` |
| `PATCH /api/tasks/{task_id}` | `{"sealed_title"}` | the task object |
| `POST /api/tasks/{task_id}/moves` | device token; `{"column_id", "position", "clock"}` | the task object as it now sits |
| `PUT /api/tasks/{task_id}/audience` | `{"members": [contact_code], "groups": [conversation_id]}` | the task object |
| `DELETE /api/tasks/{task_id}` | bearer | success |
| `POST /api/files` | device token; `{"client_id", "sealed_name", "sealed_meta", "piece_size", "piece_count"}` | `201` `{"file_id", "state", "reserved_bytes"}`; over quota is refused with `reason` `quota_exceeded` |
| `PUT /api/files/{file_id}/pieces/{piece_index}` | device token; raw bytes, `application/octet-stream` | `201` `{"piece_index", "size"}` |
| `GET /api/files` | bearer | array of file objects |
| `GET /api/files/{file_id}` | bearer | `{"file_id", "sealed_name", "sealed_meta", "piece_size", "piece_count", "state", "reserved_bytes"}` |
| `GET /api/files/{file_id}/pieces/{piece_index}` | bearer | raw bytes |
| `DELETE /api/files/{file_id}` | bearer | the file object with `state` `removed` |
| `GET /api/storage` | bearer | `{"used_bytes", "quota_bytes"}` |
| `POST /api/files/{file_id}/links` | `{"expires_in_hours"}` | `201` `{"link_token", "expires_at"}` |
| `GET /api/links/{link_token}` | none | `{"file_id", "sealed_name", "sealed_meta", "piece_size", "piece_count", "expires_at"}`; a revoked link is refused with `reason` `revoked`; an expired link with `reason` `expired` and `message` `This link has expired.` |
| `GET /api/links/{link_token}/pieces/{piece_index}` | none | raw bytes, under the same refusals |
| `DELETE /api/links/{link_token}` | bearer, the file owner | `{"link_token", "revoked_at"}` |
| `POST /api/calls` | `{"conversation_id", "media"}` | `201` `{"call_id", "conversation_id", "media", "route", "state", "rings"}` plus `peer_address` only when `route` is `direct` |
| `GET /api/calls/{call_id}` | bearer | the call object |
| `POST /api/calls/{call_id}/rings` | `{"ring_id"}` | `201` new ring or `200` repeat, with the call object |
| `POST /api/calls/{call_id}/answer` | bearer | the call object |
| `POST /api/calls/{call_id}/decline` | bearer | the call object with `state` `ended` |
| `POST /api/calls/{call_id}/end` | bearer | the call object with `state` `ended` |
| `POST /api/relays` | `{"name", "stake_tokens"}` | `201` `{"relay_id", "name", "operator_contact_code", "stake_tokens", "tier", "current_epoch": {"number", "answered_rounds", "weight"}}` |
| `GET /api/relays` | bearer | array of relay objects the caller operates |
| `GET /api/relays/{relay_id}` | bearer | the relay object |
| `POST /api/relays/{relay_id}/stake` | `{"add_tokens"}` | the relay object |
| `POST /api/relays/{relay_id}/unstake` | `{"tokens"}` | the relay object plus `unlocks_at` |
| `GET /api/relays/{relay_id}/probe` | bearer, the operator | `{"round_id", "nonce"}` |
| `POST /api/relays/{relay_id}/probe-answers` | `{"round_id", "nonce"}` | `200` `{"counted": true}` |
| `POST /api/relays/{relay_id}/heartbeats` | `{"uptime_seconds", "carried_bytes"}` | `202` |
| `POST /api/epochs/current/probe-rounds` | treasurer | `201` `{"round_id", "epoch"}` |
| `POST /api/epochs/current/close` | treasurer | `{"closed": {"number", "state"}, "opened": {"number", "state"}}` |
| `GET /api/epochs` | bearer | array of `{"number", "state", "opened_at", "closed_at"}` |
| `GET /api/epochs/{number}` | bearer; for the open epoch the figures are live and every `share_micro` is `null` | `{"number", "state", "probe_rounds", "contributions_micro", "pool_micro", "total_weight", "remainder_micro", "relays": [{"relay_id", "name", "answered_rounds_by_tier": {"basic", "level-1", "level-2", "master"}, "weight", "share_micro", "paid"}]}` |
| `POST /api/epochs/{number}/settle` | treasurer; `{"limit"}` optional | `{"number", "state", "paid": [{"relay_id", "name", "amount_micro"}], "remaining"}` |
| `POST /api/watcher/rates` | signed; `{"asset", "usd_micros", "observed_at"}` | `201` |
| `POST /api/watcher/payments` | signed; `{"rail", "tx_hash", "deposit_reference", "amount", "block_time", "confirmations"}`, or for `app_store` `{"rail", "tx_hash", "deposit_reference", "amount", "block_time", "state"}` | the payment object |
| `GET /api/rates` | bearer | array of the latest `{"asset", "usd_micros", "observed_at"}` per asset |
| `POST /api/quotes` | `{"rail"}`, optionally `{"for_contact_code"}` | `201` `{"quote_id", "rail", "asset", "price_usd_cents", "amount_due", "rate_usd_micros", "rate_observed_at", "expires_at", "deposit_reference", "beneficiary_contact_code"}`; a stale rate is refused with `reason` `rate_stale` |
| `GET /api/payments` | bearer | array of `{"payment_id", "quote_id", "rail", "tx_hash", "amount", "block_time", "confirmations", "state", "amount_due", "shortfall", "credit", "settled_rate_usd_micros"}` for quotes the caller made |
| `GET /api/membership` | bearer | `{"state", "paid_until", "trial_ends_at", "sponsor_contact_code"}` |
| `POST /api/membership/sponsorship/decline` | bearer | the membership object |
| `GET /api/sponsorships` | bearer | array of `{"recipient_contact_code", "state"}` and nothing else |
| `GET /api/token/schedules` | none | array of `{"schedule", "label", "allocation_bp", "event_bp", "cliff_months", "linear_months"}` |
| `GET /api/token/event` | none | `{"launch_at"}` |
| `PUT /api/token/event` | treasurer; `{"launch_at"}` | `{"launch_at"}` |
| `POST /api/token/positions` | treasurer; `{"contact_code", "schedule", "allocation_micro"}` | `201` the position object |
| `GET /api/token/positions` | bearer | array of `{"position_id", "schedule", "allocation_micro", "claimed_micro", "claimable_micro", "locked_micro", "fully_vested_at"}` |
| `POST /api/token/claims` | `{"position_id"}` | `{"position_id", "transferred_micro", "claimed_micro", "claimable_micro"}` |
| `GET /api/token/ledger` | bearer | array of `{"transfer_id", "kind", "amount_micro", "epoch", "relay_id", "position_id", "created_at"}` for the caller |
| `POST /api/whitelist/applications` | `{"challenge_id", "address", "signature", "email", "intended_usd_cents"}` | `201` `{"application_id", "state"}` |
| `GET /api/whitelist/applications` | treasurer | array of `{"application_id", "address", "email", "intended_usd_cents", "state", "created_at"}` |
| `POST /api/waitlist` | `{"email", "consent", "website"}` | `202` `{"message": "Check your inbox to confirm."}` |

**No mocks.** Every one of these is a contract violation, however good the screens look: messages, files or accounts held in memory or in a file on the app's disk instead of PostgreSQL; a confirmation email written to the console or a log instead of sent over SMTP to Mailpit; an email marked sent without reaching Mailpit; readable text or file names in any table, column, log or request; a seal made with a key the server holds or can derive; a payment, rate or membership created by anything other than a correctly signed watcher event; a settlement that pays from live stakes instead of the frozen snapshot. The named providers are the fact - the app's UI can only reflect what lives in PostgreSQL and in Mailpit, never substitute for it.

## Definition of done

A stranger can sign up, approve a second device, and exchange messages with another member that only their approved devices can open, while the database and the traffic hold nothing readable and a removed member or unapproved device opens nothing sent to them. A closed epoch settles by exact arithmetic, paying every relay exactly once however settlement is started, and a waitlist signup delivers exactly one confirmation email to that address alone.
