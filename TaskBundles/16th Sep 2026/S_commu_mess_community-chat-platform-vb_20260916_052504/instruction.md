# Rookery

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, read the home page, follow the action that opens the product without installing anything, sign up, redeem the invite code `NIGHTJAR-ONE`, land on a confirmation naming `Nightjar Collective`, and send a message into `#general` that a second signed-in member sees appear without reloading the page, all without hitting an error page. Two things in that sentence cannot be arranged inside the app's own screens. `Nightjar Collective` opens with exactly one seat left against a member cap of `4`, so a second stranger redeeming `NIGHTJAR-ONE` at the same instant must not also get in: one joins, the other is refused, and the space never holds five members. And when `member@example.com` mentions `owner@example.com` in `#general`, a real mail must arrive in Mailpit addressed to `owner@example.com` and to nobody else; a badge the app draws for itself does not count, and neither does a mail that also reaches `moderator@example.com`.

## Overview

Rookery is a group communication product for friend groups, gaming clans and large public communities, and it is also the public page that sells it. Both live on one origin and they are deliberately two different products wearing one brand.

The public site is a single long marketing page plus a small set of support and policy routes. Its job is to make a place to talk feel like somewhere worth spending an evening, and then to collect exactly one of three actions: download the application, open the product in a browser without installing anything, or sign in because the visitor already has an account. The third of those is on screen at every scroll position.

The product is the signed-in client. A member belongs to spaces; a space holds categories, text channels, voice channels, forum channels and stage channels; a channel holds messages, and a message can hold a side conversation. Roles carry permissions, channel overwrites bend those permissions per channel, presence says who is around, search reaches back through history, moderators keep order and leave a record that cannot be quietly edited, and a paid tier called `Loft` unlocks a handful of features through entitlements rather than through a subscription check.

The genuinely hard part is that almost every count and every unread mark in this product is derived rather than stored, and every one of them is tempting to store. A reaction count is the size of a set of people, not a tally. An unread channel is one whose newest message is newer than the newest message you have read, not a boolean. A mention count is a cache of a query, and every path that cannot be expressed as one step up or one step down re-runs the query instead of guessing. Get any of those wrong and the product looks correct for about a day.

Rookery deliberately is not several things. There is no real-time audio or video media, no timeline or algorithmic feed, no direct messages between accounts outside a space, no native application, and no payment provider: the paid tier is granted and revoked inside this app.

## User roles

An account is one kind of thing. Authority is a property of a membership, not of an account, so the same person can own one space and be an ordinary member of another.

| Role | Can do | Cannot do |
|---|---|---|
| Visitor (signed out) | Read every public route, read the policy set, read `/discover`, open a public space's preview, sign up, sign in, redeem an invite code by signing up first | **Never read a channel, never send, never react, never see a member list, never read another account's anything** |
| Member | Read and send in every channel their resolved permissions allow, react, start and join side conversations, join voice channels, search the spaces they belong to, edit and delete their own messages, set presence and notification levels, hold an entitlement | **Never read a channel they lack visibility of, never edit or delete another member's message, never assign a role, never time out, kick or ban, never read the audit record, never read a space they have not joined** |
| Moderator | All of a member, plus timeout, kick and ban within their authority, delete and pin any message in channels they can see, manage automatic rules, read the audit record, manage side conversations | **Never act on a member whose highest role sits at or above their own, never grant a permission they do not themselves hold, never edit a role positioned at or above their own, never transfer ownership** |
| Space owner | Everything in their own space, including transferring ownership, and no channel overwrite can take any of it away | **Never act inside a space they do not own beyond the role their membership there gives them** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a Member session to any Moderator-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Signup is open. Four accounts are seeded, all on the seeded password: `owner@example.com` owns `Nightjar Collective`; `moderator@example.com` holds `Moderators`; `member@example.com` holds both `Regulars` and `Archivists`, which is the pair that disagree with each other in `#build-log`; and `member2@example.com` belongs only to `Studio Loft` and is the cross-space boundary.

## Core features

### Auth

Email and password are exchanged for a bearer token sent on every signed-in request. An absent, expired or revoked token is rejected and mutates nothing. Signup refuses an address that is already registered, and refuses it in a way that does not tell the caller whether that address has an account: registration, password reset and sign-in all answer the same way for a known and an unknown address, and the failure path for an unknown account and for a wrong password takes the same time. Passwords are stored under a memory-hard hash with a unique salt per account and with its parameters stored beside the hash, so that when policy is raised a successful sign-in rehashes transparently. The policy is a minimum of `8` characters and no maximum below `128`, with no composition rules.

1. A refresh token is long lived, is stored, and rotates on every exchange: the old one stops working as the new one is issued. Refresh tokens form a family. Presenting a token that has already been exchanged means the family is compromised, so the **entire family** is revoked at once, every session opened under it is closed, and the account is told which device was affected. Refusing only the reused token and leaving the rest of the family alive is not this rule. A retried exchange inside a grace of `10` seconds is not read as theft.
2. A second factor is offered in two forms: a time-based code of `6` digits on a `30` second step with one step of tolerance either way, where **a code is single use** and a replay inside its own window is refused; and `10` backup codes, shown once, stored hashed, single use, where regenerating invalidates the whole previous set.
3. Changing a password, or adding or removing a second factor, revokes every session except the one acting. Changing the address confirms to both the old and the new address and preserves sessions. A deletion request starts a hold of `14` days that signing in during the hold cancels.
4. A session records its device kind, an approximate location and its first and last seen times. Ending a session ends its live connection rather than waiting for its token to expire, and an account may end any session except the one it is acting from.

### Spaces, channels and joining

5. An invite code names a space and a channel. Redeeming it joins the account to the space and lands on a confirmation page naming the space. `NIGHTJAR-ONE` has a use limit of `1`.
6. **A space never exceeds its member cap.** `Nightjar Collective` has a cap of `4` and opens with three members, so exactly one seat remains. Two simultaneous redemptions of `NIGHTJAR-ONE` must not both succeed: one joins and lands on the confirmation, the other is refused as invalid with the reason `That invite has already been used.`, no membership row is written for the loser, and the member count never reaches five. A refused redemption leaves no partial state: no orphaned membership, no consumed use, no read state.
7. A channel belongs to a space and may sit under a category. The kinds are `text`, `voice`, `forum` and `stage`. Moving a channel into a category whose overwrites are synchronized replaces the channel's own overwrites with the category's.
8. A space the account has not joined reads as not found rather than as forbidden, and so does a channel the account cannot see. `member2@example.com` requesting any `Nightjar Collective` channel directly must read as not found, and the reverse must hold for `member@example.com` against `#studio`.

### Permissions

Permissions are a named set carried over the wire as a decimal string rather than as a number, because the set is wider than a numeric type with `53` bits of mantissa can carry without loss, and the highest bits are exactly where that loss begins. The named permissions are `CREATE_INVITE`, `KICK_MEMBERS`, `BAN_MEMBERS`, `ADMINISTRATOR`, `MANAGE_CHANNELS`, `MANAGE_SPACE`, `ADD_REACTIONS`, `VIEW_AUDIT_LOG`, `PRIORITY_SPEAKER`, `STREAM`, `VIEW_CHANNEL`, `SEND_MESSAGES`, `SEND_TTS`, `MANAGE_MESSAGES`, `EMBED_LINKS`, `ATTACH_FILES`, `READ_HISTORY`, `MENTION_EVERYONE`, `USE_EXTERNAL_EMOJI`, `VIEW_INSIGHTS`, `CONNECT`, `SPEAK`, `MUTE_MEMBERS`, `DEAFEN_MEMBERS`, `MOVE_MEMBERS`, `USE_VAD`, `CHANGE_NICKNAME`, `MANAGE_NICKNAMES`, `MANAGE_ROLES`, `MANAGE_WEBHOOKS`, `MANAGE_EXPRESSIONS`, `USE_APP_COMMANDS`, `REQUEST_TO_SPEAK`, `MANAGE_EVENTS`, `MANAGE_THREADS`, `CREATE_PUBLIC_THREAD`, `CREATE_PRIVATE_THREAD`, `SEND_IN_THREAD`, `MODERATE_MEMBERS`, `USE_SOUNDBOARD`, `CREATE_EXPRESSIONS` and `PIN_MESSAGES`.

Most of those names say what they do. Three do not, and they are pinned here: `PRIORITY_SPEAKER` lets a member attenuate everyone else while they are speaking; `MENTION_EVERYONE` is what allows the space-wide and role-wide mentions; and `USE_VAD` allows transmitting without holding a control down.

Permissions come from the `@everyone` role, which is always present at position `0` and cannot be deleted; from the other roles a member holds, ordered by position; from a channel overwrite for `@everyone`; from a channel overwrite for a role; from a channel overwrite for a member; and from space ownership, which is above all of it.

Resolving a member's permissions in a channel has exactly one answer, and these are the six properties of it that decide whether the answer is right:

9. **Roles are unioned, never ranked.** A member's own permissions are everything any role they hold grants. Role position orders authority over other members and other roles; it does not order a member's own permissions, so the lowest role in the list can grant something the highest does not. `member@example.com` holds `Regulars`, which is denied `SEND_MESSAGES` in `#build-log`, and `Archivists`, which is allowed it, and they can post.
10. **An administrator, and an owner, cannot be denied by a channel overwrite.** The administrator answer is decided before any overwrite is read. Denying `VIEW_CHANNEL` to `@everyone` in `#mods-only` must still leave `owner@example.com` able to see it.
11. **Every role deny is applied before every role allow**, as one pass over all the roles rather than a deny-and-allow pass per role. Where one role denies what another allows, the allow wins, and **the answer does not change when the roles are reordered**. This is the single rule most often built the other way.
12. **The member overwrite beats every role overwrite, in both directions.** A member allow beats a role deny and a member deny beats a role allow.
13. **A communication timeout masks rather than clears.** A member under a timeout keeps `VIEW_CHANNEL` and `READ_HISTORY` and loses everything else, including `ADD_REACTIONS`. A timed-out member can read the channel, cannot post, and **cannot react**.
14. **Losing visibility voids the whole set.** Without `VIEW_CHANNEL` in a channel, the resolved set in that channel is empty rather than partial, and the app must never report `SEND_MESSAGES` in a channel the member cannot see.
15. A member may only modify a role positioned strictly below their own highest, and may only act on a member whose highest role is strictly below their own highest; equal positions permit action in neither direction. **A member may never grant a permission they do not themselves hold**, and that check is per named permission rather than over the set as a whole: a moderator without `BAN_MEMBERS` editing a role must be refused when they add `BAN_MEMBERS` and allowed when they add something they hold.
16. A permission change reaches every live session within `2` seconds. Editing a role's permissions affects every member holding it in every channel; assigning or removing a role affects that member in every channel; editing a channel overwrite affects every member in that channel; moving a role's position changes authority only and no resolved set. Losing `VIEW_CHANNEL` while a channel is open removes it from the sidebar, closes it, and drops its cached messages. Gaining it does not back-fill unread counts for the period before the grant.

### Messaging

17. Every space, channel, role, message, thread, attachment and account carries an ordered identifier that encodes the moment it was created, so sorting by identifier sorts by creation time and no second timestamp column orders anything. Identifiers are carried over the wire as strings. A creation time derived from an identifier and a stored timestamp must never disagree. If the clock moves backwards the generator must refuse to issue rather than issue an identifier below one already issued, and exhausting a millisecond waits for the next one rather than borrowing from another field.
18. A message carries its channel, its author, its content of at most `4000` extended grapheme clusters, its kind, an optional reference to another message, its attachments, its reactions, its computed mentions, its flags, the client's nonce, and an optional side conversation. Its kinds are `default`, `join`, `pin`, `thread_started`, `reply` and `call`.
19. Sending validates in a fixed order, because the reason the sender is shown depends on it: permission, then rate limit, then content validity, then attachment availability, then poll validity.
20. Editing is the author's alone, changes content only, records an edited time, never changes the identifier and never reorders. Deleting is the author's or a holder of `MANAGE_MESSAGES` in that channel. A bulk delete of up to `100` identifiers of messages under `14` days old emits **one** event and not one per message. Replies to a deleted message survive and render as a reference to a removed message. A delete that arrives before its own send has resolved marks the pending row rather than being dropped.
21. Pagination of history is read a page at a time, `1` to `100` rows and `50` by default, either strictly older than an identifier, strictly newer than one, or around one. **Both directions return newest first**, which is the trap: a page of newer messages is not ascending. Around an identifier returns the older half, the message itself, and the newer half, with the extra row going to the newer side when the limit is even. Around the first or last message of a channel returns a short page rather than an error, and a short page is never read as the end of the channel in the other direction. Cursors are identifiers rather than offsets, so a message arriving mid-page can neither skip a row nor repeat one.
22. **Sending is idempotent by nonce.** The client generates a nonce per logical send and keeps it stable across retries of that send. A retry carrying a nonce the service has already stored for that channel and author returns the original message and creates no second one. Two different sends colliding on one nonce is refused as invalid rather than silently answered with the first. The service holds a nonce for `300` seconds per channel per author.
23. **A reaction is a set of people, never a counter.** The count rendered is the size of that set and is never incremented or decremented directly. Fifty simultaneous additions and removals must leave a count that equals the set exactly. A message receiving more than `20` reaction events within `1` second is delivered as one summary carrying the whole set rather than as individual events, and the client accepts both shapes.
24. Mentions are computed **by the service at send time** from the permissions resolved at that moment, and are stored on the message. A member who later loses `MENTION_EVERYONE` must not retroactively un-notify the people already notified, and editing a message to add a mention notifies nobody. A channel mention renders as a link only for a reader who can see that channel and as plain text for everyone else.

### Delivery, unread and the mention notice

25. **A message another member sends into an open channel appears without reloading the page.** Live delivery is this app's own realtime protocol on the same origin. Each delivered event arrives in one envelope carrying its number, its kind and its payload, and each live session numbers the events delivered to it, incrementing by exactly one per event. That numbering restarts when a session is replaced rather than resumed.
26. The live connection is checked for liveness on a rhythm the service sets rather than one the client picks, and each heartbeat carries the last event number seen. **The client must confirm that the service did acknowledge the check rather than only sending it**, because a connection whose heartbeat goes unanswered is dead while still looking open, and the reader notices nothing until they try to send. The first check is sent at a random point inside the first interval rather than at a fixed offset, so a restart does not make every client check in on the same beat. Reconnection uses an exponential backoff with jitter, growing to no more than `30` seconds, and the attempt counter resets when a session is ready rather than when a connection merely opens.
27. A session that reconnects naming the last number it saw resumes: it receives exactly the events it missed, in order, with no duplicates and no gaps. The retained window is the last `1000` events or `180` seconds of them, whichever is smaller, per session. **A reconnect naming a number older than that window is refused outright rather than partly served**, and the client discards what it holds and refetches, because a partial replay is a silent hole and a refusal is not. Refusals divide in two. A resumable one, such as an unknown failure, a frame the service could not decode, or a session that is already authenticated, is resumed. A terminal one, such as a revoked credential or a misconfigured client, is not retried at all, because retrying it in a loop exhausts the refusal budget and blocks the whole caller rather than just that connection.
28. After reconnecting, the client compares the newest identifier it holds for a channel against the oldest identifier in what it was just sent. If the two do not meet, the range between them is a hole: it is fetched rather than assumed empty, and until it is fetched the channel shows the hole rather than joining the two ranges into a continuity that is not there.
29. Unread is derived: a channel is unread when its newest message is newer than the newest message this account has read. It is never stored as a flag. **Acknowledgement is monotonic**: a request naming an identifier below the stored mark is accepted and does nothing, so two devices reading at once cannot push the mark back and forth. Acknowledgement is idempotent. The one path allowed to jump straight to the channel's newest message is an explicit mark-as-read. Every acknowledgement reaches the account's other sessions within `2` seconds.
30. The mention count is a cache of a query. An arriving mention steps it up. An acknowledgement past it **recomputes** it as the number of mentioning messages above the read mark rather than zeroing it. Deleting a mentioning message steps it down and never below zero. A bulk delete recomputes the channel rather than subtracting once per message. Leaving and rejoining resets it to zero and moves the read mark to the newest message.
31. Notification level is stored at four scopes, each inheriting from the one above: the account default, then the space, then the category, then the channel. The values are `all`, `mentions`, `nothing` and `inherit`. **`inherit` is a real stored value**, distinct from whatever it currently resolves to, so changing a space default takes effect on every channel that never overrode it. Suppressing everyone-mentions, suppressing role-mentions and muting are separate flags that compose with the level, and a mute with an expiry stores an absolute instant and is evaluated when it is read.
32. **The mention notice is the delivery rule this product is judged on.** When a message mentions a member who has no live session, exactly one mail is sent over real SMTP to that member's address alone, with no cc and no bcc. A live session here means an open connection to that account's event stream, held at the moment the message is sent. A bearer token that was issued earlier and is not currently carrying an event stream is not a live session, so a member who signed in and went away is mailed. The subject begins `Rookery mention:` followed by a space and the channel name, so a mention in `#general` reads `Rookery mention: #general`. The body names the space, the channel, the display name of the author and the text of the message. A mention of a member who does have a live session sends no mail, and neither does a reaction, a typing event, an edit that adds a mention, a thread archival, a join, or a member mentioning themselves. A mention of two members sends one mail to each of them and to nobody else.

### Side conversations, boards, stages, events and polls

33. A side conversation hangs off a message or stands alone in a channel. It inherits the parent channel's permissions and is not independently overwritable, except that a private one carries an explicit member list. Joining is implicit on posting and explicit on being added, and it drives notification routing only. It folds itself away after an idle window of `60`, `1440`, `4320` or `10080` minutes, chosen per conversation, and any post unfolds it, restoring it to the sidebar for **every** member who had it there rather than only for the poster. A locked one refuses posts and refuses unfolding by anyone without `MANAGE_THREADS`. Its message and member counts stop being exact above `50` and say so.
34. **The idle clock runs from the last message ever posted, deleted or not.** Deleting the newest message must not hand the conversation a fresh clock from the message before it, because that lets a deletion wake a conversation that had been asleep for a week.
35. A board channel has no messages of its own and its children are side conversations. A post is one of those with a title, a required first message and `0` to `5` tags. Tags are defined per channel, up to `20`, and may be marked moderator-only. Sorting is by recent activity or by creation, and **recent activity means the last message in the conversation, which changes when one is deleted as well as when one is posted**. A channel that requires a tag refuses a post carrying none, at creation, with the error named against the tag field rather than as a general refusal.
36. A stage channel has speakers who transmit, an audience who receive, and moderators who promote and demote. Raising a hand records a time, and moderators see the queue in request order. Promotion clears that time and grants transmission **without dropping the member out of the room and back in**. Ending a stage moves everyone out and closes the scheduled event attached to it.
37. A scheduled event carries a kind of `stage`, `voice` or `external`, a start, an end required for `external` only, a status among `scheduled`, `active`, `completed` and `cancelled` with forward transitions only, an interest set whose count is derived from it, and an optional repeat.
38. A repeat is stored **with the organiser's zone name and never with a fixed offset**, so a weekly event at `19:00` stays at `19:00` local across a daylight transition instead of moving by an hour twice a year. Its frequency is `DAILY`, `WEEKLY`, `MONTHLY` or `YEARLY` with an interval of `1` to `12`; weekly repeats name weekdays; monthly repeats name either a day of the month or an ordinal weekday, never both; yearly repeats name months; and exactly one of a count or an end date is required. Occurrences are computed rather than stored, except the next `100`, which are kept for reminders and discarded as a set whenever the rule changes. An occurrence at a local time that does not exist moves forward to the first valid instant; one at a local time that happens twice takes the first. **A monthly repeat on day `31` produces no occurrence in a month of `30` days: it is skipped, never moved to the `30th`.** Editing one occurrence detaches it as an exception, and editing the rule afterwards does not reclaim it.
39. Reminders fire `60` minutes before, `10` minutes before and at the start. Delivery is at least once, so the client deduplicates on the event and the occurrence start, and a reminder for an occurrence that has since been cancelled is dropped when it would be delivered rather than when it was scheduled.
40. A poll carries a question of at most `300` clusters, `1` to `10` answers, an expiry at most `32` days out, and whether more than one answer may be chosen. One vote set per account per poll, replaced rather than appended, so changing a vote is not two votes. Counts are derived from the votes. A vote cast within `2` seconds of expiry is accepted and one after it is refused with a reason of its own, which the client must not show as pending. The result freezes exactly once and is immutable afterwards, and a voter who later deletes their account leaves their vote in the total without leaving their identity.

### Presence, typing and member lists

41. Presence belongs to a connection rather than to an account. The effective status of an account is the strongest of its live sessions in the order `online`, `idle`, `dnd`, `offline`, except that an explicit `dnd` or `invisible` on any session wins outright. `idle` is set by the client after `600` seconds without input and is never inferred by the service. Activities are an ordered list of which only the first is rendered where space is short.
42. **`invisible` must not leak.** It is reported to the account's own sessions as `invisible` and to everyone else as `offline`, and it must not surface through voice state, through typing, or through the member list. Those are three separate holes and each is closed on its own.
43. A typing indicator lives `10` seconds from the service's own timestamp on the event. The client sends at most one typing call per `8` seconds per channel while the composer holds uncommitted text, and stops immediately on send. **Remaining life is computed against how long ago the service said it happened**, never by comparing a stored instant to the device's own clock, because a device whose clock is a minute fast would show every indicator as already expired and one a minute slow would show them forever. Typing is suppressed for anyone the reader has blocked and for invisible sessions.
44. A member list is a set of ranges over an ordered view rather than a list. A session subscribes only to the ranges it is showing plus one screen beyond, and re-subscribes after it stops scrolling. Updates arrive as instructions to synchronize a range, update a row, insert a row, delete a row, or void a range. **Inserts and deletes shift every index after them and are applied one at a time in order**, never batched into a set operation. Voiding a range means the held copy is void and must be re-requested; it is not a hint. Group counts are authoritative even for ranges the session does not hold, so the headings read correctly above rows that are not loaded. A member becoming invisible produces a delete at their index and an insert into the offline group, in that order, in one event.
45. The member list for a channel is identified by its overwrite set, so two channels configured alike share one list and one computation. `#general` and `#build-log` are seeded with identical overwrites and must share an identity. The identity changes when an overwrite changes, and every subscriber of the old identity is told their held ranges are void.
46. Voice state is separate from presence and survives a reconnect: a member in `Main Stage` whose connection drops stays in `Main Stage`, and the reconnected session is told so rather than inferring it. A voice channel holds at most `99` members, a stage at most `50` speakers with an unlimited audience. Joining, leaving, self-mute, self-deaf, server-mute, server-deaf and the speaking signal are all records, and the speaking signal comes from the control path rather than from decoded audio.

### Search

47. Search takes words, quoted phrases and filters, where a filter is a key and a value and any term may be negated. The keys are `from`, `mentions`, `has`, `in`, `before`, `during`, `after` and `pinned`. Different keys combine as an and; repeated uses of one key combine as an or, so `from:a from:b has:file` means from either author and carrying a file. A negation negates only its own filter. **An unterminated quote closes at the end of the input rather than failing**, because the query runs while it is being typed, and an unknown key is a literal word rather than a syntax error. `during:` expands to a day, a month or a year in the **reader's** zone.
48. **Results are filtered against permissions resolved at the moment of the query**, never against permissions recorded in an index. A member who lost access to a channel a second ago must not see its content, so a page is fetched over-wide and trimmed and the total is therefore approximate, which the response says.
49. The search index stands in eventual consistency with the messages beneath it, and the product is honest about that rather than hiding it. A space whose index is still building answers with an explicit still-indexing state carrying a retry hint, and the client renders that state rather than an empty result. Reporting nothing found for an unbuilt index tells the reader their messages are gone, which is a defect and not a shortcut.
50. Deletions are applied ahead of insertions, because content a moderator removed staying findable is a safety failure while a new message being briefly unfindable is an inconvenience. An edit is applied as a removal and an insertion rather than in place. Paging uses a snapshot taken at the first page so results do not shuffle as new messages arrive; the snapshot expires after `600` seconds, and a page requested from an expired one is refused with a reason of its own so the client can restart the search.

### Attachments

51. An attachment is created in three steps rather than one: a session is opened naming the filename, the declared size and the declared leading bytes; the transfer happens against the target that session returned; and the message is then sent naming the attachment. A target is scoped to one account, one channel and one declared size, expires in `1800` seconds, and is refused when reused for a second file or for a file larger than declared.
52. Transfer is resumable in chunks of `5MB` with a smaller final chunk, up to `3` in flight and out of order, each carrying its own checksum and the whole carrying one verified before the attachment becomes readable. **A chunk retried at an offset already received is acknowledged rather than stored again, and is charged to the quota once.** An upload idle for `1800` seconds is reaped and its reserved quota released.
53. **Quota is reserved when the session is opened and settled when the transfer completes.** Charging only at completion lets twenty parallel uploads exceed the allowance, so twenty sessions totalling twice the quota must be refused at reservation. Storage is addressed by content, so identical bytes are one stored object with a reference count, and the quota is charged per account per reference, so two accounts uploading the same file each pay and neither can free the other's copy.
54. **The type is determined from the declared leading bytes, never from the filename and never from what the client called it.** A mismatch is not an error: the detected type wins and is what is stored, served and rendered, and anything outside a small allow list is never rendered inline.
55. Scanning is asynchronous. The message posts immediately, the attachment renders in a pending state for its poster and is withheld from everyone else until the scan clears. Blocking the message on the scan makes every post feel broken; serving the file to everyone during the scan is not scanning at all.

### Moderation

56. A timeout requires `MODERATE_MEMBERS` and authority, carries an **absolute expiry rather than a duration** so it survives a restart and does not drift, and is evaluated when it is read, so a timeout that expires while nobody is looking has still expired. A kick removes membership and leaves invites working. A ban removes membership, refuses rejoining, and optionally removes the last `1` to `7` days of that account's messages. Bans are evaluated on join, on invite use and on every reconnection, so a banned account holding a live session is disconnected rather than merely blocked from rejoining. Unbanning removes the ban and does not restore membership.
57. A space holds up to `6` automatic rules, each with a trigger, exemptions and actions. The triggers are a keyword list of up to `1000` substrings and up to `10` patterns with wildcard anchors at either end; a maintained preset covering profanity, sexual content and slurs, kept centrally; repeated content across channels within `60` seconds; a burst of distinct mentions in one message; and links to domains outside an allow list. Actions are block, alert to a channel, and timeout, and they compose.
58. **A pattern supplied by a space runs in time proportional to the length of the message and no worse.** A pattern of nested repetition applied to a long message must not become a way for any member to stall the service by posting a paragraph, and the rule author does not have to be malicious to write one by accident. Patterns are capped at `260` characters and are compiled when they are saved, with a compile failure named against the pattern field.
59. Evaluation order is fixed: permission, then rate limit, then the automatic rules in creation order with the first blocking action winning, then mention resolution, then the write, then delivery. **A blocked message is never stored, never given an identifier and never delivered**, and its sender is told which rule stopped it while every other member sees nothing at all.
60. A report carries the message, the reporter, a category and optional context, is rate limited per reporter per space, is deduplicated by message, and **snapshots the reported content at the moment of the report** so that deleting it does not destroy the evidence.
61. Every state change by a moderator or an owner is recorded as an entry carrying the actor, the target, the action, the before and after of each changed key, an optional reason, and the fingerprint of the entry before it. **The record is append-only and chained**, so removing or altering an entry breaks every fingerprint after it and is detectable. The chain is per space and entries are appended one at a time, so that under concurrent moderation no two entries claim the same predecessor. Anyone with `VIEW_AUDIT_LOG` can run a verification pass over it. Entries are shown for `90` days and the chain is kept indefinitely.

### The paid tier

62. `Loft` is sold as `Loft Monthly` at `1000` and `Loft Yearly` at `10000`, both in `usd`. **What the product checks before unlocking a feature is an entitlement, never a subscription**, so a paid subscription, a gift and a staff grant are indistinguishable at the point of use and a billing problem cannot take a feature away from somebody who already holds it.
63. A subscription moves `incomplete` to `active` to `past_due` to `unpaid` to `cancelled`, forward only, with two exits from the middle: cancelled immediately, or recovered to `active`. An `incomplete` subscription grants nothing. An `active` one grants through the end of its period. **A `past_due` one still grants**, for a grace of `7` days while recovery is attempted. An `unpaid` one grants nothing. A cancelled one grants through the end of the period when it was cancelled at period end, and nothing at all when it was cancelled for fraud.
64. Dunning recovers a failed payment. Recovery is attempted at the failure, then `3` days later, then `5` days later, then `7` days later and no more, each attempt notifying once. Recovering at any point restores `active` **without changing the end of the period**, so recovering does not shorten the time already paid for.
65. Proration governs changing plan mid-period. It computes the credit for the unused remainder as the **seconds remaining over the seconds in that actual period**, using the real length of the real period rather than an assumed `30` days, and computes the new charge over the same remaining seconds. Both are integer minor units, and **rounding is applied once at the end and never per line**, rounding half away from zero. A downgrade whose credit exceeds the new charge is not refunded; it becomes account credit applied to the next invoice. An upgrade takes effect immediately and a downgrade at the end of the period, and both are recorded as scheduled changes the account can see and cancel. Every amount stores its currency, and no currency is assumed anywhere.
66. **Gifting is by single-use code, and redeeming one is a single indivisible step.** `LOFT-ONE-SEAT` grants `Loft Yearly`. Two redemptions of one code at the same instant produce exactly one entitlement and one clear refusal, never two entitlements and never a silent second grant. Codes carry an expiry, may be revoked before redemption, and a revocation that lands while somebody is mid-redemption fails that redemption rather than granting it.

### Commands, components and webhooks

67. A registered command is a name, a description and a typed option list. The option types are string, integer, number, boolean, user, channel, role, mentionable, attachment, subcommand and subcommand group. Resolved options arrive with the invocation rather than as an identifier the app must fetch; nesting is capped at two levels; a command carrying subcommands is not itself invocable; and choice lists hold at most `25` entries. A registration for one space is immediate and a global one takes up to `3600` seconds to appear, and the client renders whichever set the service currently reports.
68. **The deadline is on the acknowledgement, not on the work.** An invocation must be acknowledged within `3` seconds, either with a response or with a deferral that shows a thinking state, and a deferral then has `900` seconds to follow up. An app that does its work first and answers afterwards fails on exactly the slow calls a person is watching. An initial response may be sent only once; a second attempt is refused as invalid and the correct call for a second message is a follow-up. An invocation is delivered at least once, so it is deduplicated on its own identifier.
69. An option marked for autocomplete turns every keystroke into a request answered within `3` seconds with up to `25` choices. **Out-of-order answers are the normal case here rather than an edge case**: the client settles before it asks, abandons the request in flight, and renders only the answer to the newest request, because rendering whichever arrives last shows suggestions for a prefix the reader already deleted.
70. A component on a message carries at most `100` characters of its own state and nothing else, and that state carries a version prefix, because a message with a button in it outlives several deployments of the app that made it. State the app no longer understands produces a polite refusal rather than a failure, and such components are disabled on the next render rather than left live.
71. Every interaction delivered to an app is signed over the timestamp and the **raw request body** as it arrived rather than a re-serialized copy, is refused when the timestamp is more than `300` seconds from now, is compared in constant time, and is verified before parsing, before routing and before any logging that includes the body.
72. An outbound webhook is delivered at least once, carries a stable delivery identifier the receiver deduplicates on and a sequence it may use for ordering, retries under an exponential backoff with jitter, spanning about `24` hours across `8` attempts, and is stored for `72` hours and re-drivable by hand after the last attempt. A target failing every delivery for `72` hours is disabled and its owner told.
73. **An app can never act above the member who invoked it.** Its effective permissions in a channel for anything done on a member's behalf are the intersection of its own and that member's.

### Text handling

74. Every string a person sees comes from a catalogue keyed by what the string is for rather than by its English text, interpolated by named placeholder. **Translated fragments are never concatenated**, because word order is not universal, and plurals use the full category set of the target language rather than a one and an other.
75. In a right-to-left language the layout mirrors: the rail moves to the right, the member list to the left, chevrons flip, and alignment follows. Direction within a message is decided per message from its first strong directional character, so one message in the other direction renders correctly without affecting its neighbours.
76. **Length is counted in extended grapheme clusters, never in code units.** A family emoji is one character to a person and up to eleven code units to a machine, and a limit counted the machine's way cuts a message in the middle of a person. A message of `4000` family emoji is accepted and rendered whole. Truncation is always at a cluster boundary and never inside a joined sequence.
77. Bidirectional override and isolate characters are stripped from display names and neutralized in message content, because they can make a message render as text it does not contain. Zero-width and invisible characters are stripped from names, preserved in message content, and counted toward the limit either way.
78. A display name that renders identically to another member's in the same space is refused, checked against a mapping of confusable characters. Identifiers are normalized before comparison and stored normalized, so two spellings of one name cannot both be registered. Sorting uses locale-aware collation rather than code-point order.

### The public site

79. The home page is one long page of nine full-height movements: a hero, six feature movements, a band of moving words interrupting them exactly halfway, and a closing panel above the footer. The six features alternate strictly, text on one side then the other, and the band is the only thing that breaks the alternation.
80. A privacy page and **a terms page are reachable from the footer of every page on the site, and the terms page is linked from the signup form**. Each policy document carries a table of contents linking within the page, a stable identifier on every heading so a link into a clause survives a re-edit, a last-updated date, and a summary of what changed since the previous version.
81. **Every internal link on every public route resolves.** No link on the site points at an address that does not answer.
82. **An unknown address renders Rookery's own not-found page and answers not-found rather than answering as though the page were fine.** That page carries the product's chrome, a heading, a short paragraph, and three links onward, and the addresses that do not exist are not redirected to the home page and do not render the home page with an error banner over it.
83. **Every form rejects invalid input inline, names the field that was wrong, and writes nothing.** Signing up with a malformed address, a password below the minimum, or a taken handle leaves no account behind; posting to a board channel that requires a tag without one names the tag field; creating a role with a position at or above the actor's own names the position field.
84. The cookie choice, the language control and the space directory are the public site's only stateful surfaces, and the cookie choice never blocks the first paint.
85. The application entry route renders no marketing content at all: no navigation, no footer. A visitor with a valid session lands in the client and it starts drawing before the live connection is established rather than waiting for it. A visitor without one is sent to sign in **carrying the address they were trying to reach**, including a specific channel and a specific message inside it, and signing in lands them exactly there.
86. The download action names the platform the visitor is on, falls back to the label `Download` when the platform is unknown, and lists every platform's build beneath it. Detection changes what the action says and never what it does, so a wrong guess is cosmetic rather than a dead end.
87. Each page view is recorded with its route and the time it happened, readable by the space owner and by nobody else.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | the home page, nine movements | public |
| `/download` | every platform's build | public |
| `/loft` | what the paid tier carries | public |
| `/discover` | the space directory | public |
| `/safety` | the safety tree | public |
| `/quests` | the community programme | public |
| `/support` | help and feedback | public |
| `/blog` | the editorial index | public |
| `/developers` | the developer tree | public |
| `/careers` | jobs | public |
| `/legal/terms` | the terms document | public |
| `/legal/privacy` | the privacy document | public |
| `/legal/guidelines` | the community guidelines | public |
| `/legal/cookies` | the cookie choice | public |
| `/legal/acknowledgements` | acknowledgements | public |
| `/legal/licenses` | licenses | public |
| `/legal/company` | company information | public |
| `/sign-in` | account entry | public |
| `/sign-up` | account creation | public |
| `/app` | the entry into the client | public |
| `/join/<code>` | redeem an invite, ends on a confirmation | member |
| `/redeem/<code>` | redeem a gift code, ends on a confirmation | member |
| `/app/spaces/<space>/channels/<channel>` | a channel | member |
| `/app/spaces/<space>/channels/<channel>/<message>` | a channel opened around one message | member |
| `/app/spaces/<space>/threads/<thread>` | one side conversation | member |
| `/app/spaces/<space>/events` | scheduled events | member |
| `/app/spaces/<space>/settings/roles` | roles and positions | moderator |
| `/app/spaces/<space>/settings/automod` | automatic rules | moderator |
| `/app/spaces/<space>/settings/audit` | the audit record | moderator |
| `/app/search` | search within a space | member |
| `/app/settings/account` | account, sessions, second factor | member |
| `/app/settings/notifications` | the inheritance tree | member |
| `/app/settings/billing` | plan, entitlements, gift codes | member |

**Entry and redirects.** A signed-out request for any `/app` route lands on `/sign-in` carrying the address it was trying to reach and returns exactly there after signing in, including a channel and a message inside it; with no intended address it lands on the first space in the rail. Signing out returns to `/`. A token that has expired mid-action refuses the action, changes nothing, and returns to `/sign-in`. A member reaching a moderator-only settings route is refused by the server and shown the channel they came from. A space the account has not joined, and a channel the account cannot see, both read as not found rather than as forbidden.

**Journeys.**

1. Open `/`, scroll through the nine movements to the closing panel, follow the action that opens the product in a browser, sign up as a new account, redeem `NIGHTJAR-ONE` at `/join/NIGHTJAR-ONE`, read the confirmation naming `Nightjar Collective`, and send a message into `#general`; a second window signed in as `member@example.com` shows that message arriving without a reload.
2. Sign in as `member@example.com`, mention `owner@example.com` in `#general`, and see the owner's mention count rise; one mail reaches `owner@example.com` and no other address receives it.
3. Sign in as `member@example.com` and post into `#build-log`, where `Regulars` is denied and `Archivists` is allowed; the post succeeds. Sign in as `owner@example.com`, reorder those two roles, and post again; it still succeeds.
4. Sign in as `moderator@example.com`, time out `member@example.com`, then sign in as `member@example.com` and confirm the channel still reads, the composer refuses, and adding a reaction refuses.
5. Sign in as `owner@example.com`, open `/app/spaces/nightjar-collective/settings/audit`, and run the verification pass over the chain.
6. Sign in as `member2@example.com` and request `/app/spaces/nightjar-collective/channels/general` directly; it reads as not found.

**States.** Every list has an empty state naming what would fill it, including a channel with no messages, a space directory with no results, a search with no hits and a member list with nobody online. Every page has a loading state that reserves the space its content will occupy so nothing moves when the content lands. Every error is a rendered page or an inline message beside the field that caused it, never a blank screen and never a crash. A channel whose history has a hole shows the hole rather than closing it. A search over a space whose index is still building says so rather than reporting nothing found.

## UI/UX notes

Somebody arriving at the public page should understand within a few seconds that this is a place a group of friends already lives in, and should feel invited rather than sold to. Somebody already signed in should stop noticing the interface at all and see only the conversation. Those are two different products wearing one brand, and the tension between them is resolved by scoping rather than by splitting the difference: the public page is consumer and expressive and may carry atmosphere, with the product itself the first thing seen; the client is operational, quiet and dense but organised, built for scanning and for repeated action, and carries no editorial composition and no oversized hero anywhere inside it. Calm over expressive inside the client; atmosphere over restraint outside it.

The ground the client sits on is a near-black neutral with a faint cool cast, and raised surfaces are one step up from it in the same family rather than a different colour. One mid, vivid indigo is the primary action, and it is the only thing on any screen wearing that colour. Four further colours each carry exactly one meaning and appear nowhere else: a green for a member who is around, an amber for one who has stepped away, a red for one who does not want to be disturbed and for something that has gone wrong, and a magenta reserved for the paid tier. A state that is none of those may not borrow any of them. The exact shades are yours, so long as those two rules hold: one colour per meaning, and the primary action alone in its own.

Colour is never the only carrier of a meaning. Presence carries a distinct shape as well as a distinct colour, so the four states still read for somebody who cannot tell the green from the red.

Type carries three roles and the relationship between two of them is the loudest signal on the public page. A display grotesque, extended and set in capitals at its heaviest weights, sits on leading that is **tighter than the size of the type itself**, so a three-line headline reads as one solid block of letterforms rather than as three lines. Body type sits on generous leading by contrast, and the gap between those two densities is what makes the page read as loud and friendly rather than corporate. A neutral text grotesque carries everything else, and a monospace face is reserved for identifiers and for nothing else. Figures align down a column wherever amounts, counts, versions or identifiers stack. No font binary is fetched; each role ends in a face the reader's system already has, so there is no loading phase and no moment of invisible text.

Motion is **eased**: entrances and exits are deliberate, everything moves on one family of curves, and nothing uses a different speed to feel special. Timing is chosen by the size of the thing moving rather than by the property being animated, so something the size of a checkbox settles almost at once, something the size of a whole section takes noticeably longer, and most of the product sits between them. The named properties are the ones that move; a blanket rule that animates everything is a defect, because it quietly animates things nobody intended. The moments worth naming, because a build that names none of them will ship none of them: a press leaves a ripple that has already faded by the time it stops growing; something arriving rises a short distance while fading up; a loading skeleton breathes rather than blinking; a highlight sweeps once across a card and stops; a gradient drags across text that is still waiting; a confirmation is a dot that swells and vanishes in the same frame a check appears in its place, so it reads as one thing becoming another rather than as two things; a pressed control squashes wide, springs tall and wobbles smaller until it settles, keeping its volume at every step; a band of words slides sideways forever without a stutter; a divider's wave reshapes rather than slides; and one deliberately excessive overshoot is reserved for a single celebratory moment and appears nowhere else. Under a reduced-motion preference every one of those is replaced by its final state, nothing is left part-way, the starfield stops, and the excessive overshoot does not run at all.

Depth comes from blur and from one real perspective, never from a scale of drop shadows. Things read as near or far because the far ones are slightly out of focus, exactly as in a photograph. The large feature cards on the public page are frosted over the starfield behind them, heavily enough that the stars melt into a field of light, while the scene inside each card stays perfectly sharp; that contrast between the two edges is the whole effect, and a build that reaches for a shadow scale will look like a different product. Space over dividers: sections read as separate because of the room around them rather than because a line was drawn between them.

Corners are barely softened on ordinary controls. The large feature cards are rounded so heavily that they stop reading as boxes and start reading as capsules, and that softening grows at each wider boundary until the largest breakpoint, where the cards are at their roundest. The navigation panel is square across the top and deeply rounded at the bottom, so it reads as having been poured out of the bar rather than opened from it.

Density is comfortable on the public page and compact inside the client, where rows sit tight enough that a busy channel and its member list fit one screen without scrolling to find the composer. The layout archetype is a persistent left rail: a narrow strip of one control per joined space, then the channel sidebar, then the conversation, then the member list, which is a split detail pane in the two middle columns and the shape the product is recognised by.

Every component states its behaviour rather than its measurements. Controls have resting, pointed-at, pressed, focused and unavailable states, and unavailable is never signalled by colour alone. Pointing at a navigation entry fills the whole entry rather than underlining its label, and every link in the plain chrome underlines on hover and at rest does not. Every hover treatment is declared only where a pointer actually exists, so tapping a navigation entry on a phone does not leave it stuck looking pressed until something else is tapped. Escape closes any open panel and returns focus to the control that opened it. Destructive actions confirm first.

Accessibility is contract and does not vary with any of the above. Body text meets WCAG AA contrast against its own ground on both the dark and the light surfaces, and large display type meets the large-text bar. Keyboard navigation reaches every control in reading order with a visible focus ring that is never the hover state and never depends on the primary colour. A skip link is the first focusable element on every page. Icon-only controls carry a name that says what they do rather than what they depict. No interactive target is smaller than a comfortable fingertip, which means the row of small marks in the footer needs padding around its drawn size. The band of sliding words is hidden from assistive technology and its words appear once as static text, because a loop read aloud forever is unusable. Every picture of the product carries a description of what the interface in it is doing rather than what it looks like. In a busy channel, arriving messages are announced only while the list is already at the bottom, because announcing every message in a fast channel is worse than announcing none. Every content image carries alternative text and every decorative one declares itself decorative.

The product is responsive across four boundaries and no more, every rule written the same way round and mobile first, and the layout holds at every width between them rather than only at the named ones. Going up through them: stacked actions come side by side, the menu control becomes a row of navigation entries, feature cards put their scene beside their text rather than above it, corners grow rounder, the member list appears, and the full set of scroll-driven movement switches on. At a narrow viewport nothing overflows sideways, every navigation target stays reachable, and the two left columns of the client become a drawer. A window that is short rather than narrow suppresses the full-height treatment instead of squashing it.

Each page leads with one clear primary action, visually distinct from every secondary one on that page.

What this must not look like: no page dominated by a single hue family with no second signal; no decoration standing in for content; no marketing composition inside the client, where the working interface belongs; and no scene clipped tidily inside its card, because the objects that cross a card's boundary are the composition and clipping them produces a neater page that has lost the entire effect.

## Technical requirements

The stack is fixed. The rendering model is a single-page application against a JSON API: the browser receives an application shell on first paint and every route's content arrives over the same-origin API rather than inside the first document. The frontend is **SolidJS built with Vite**, compiled to a production build and served as static files by the backend. The backend is **Flask**, serving the HTTP API on that same origin under the `/api` prefix. The datastore is **PostgreSQL** at `DATABASE_URL`. Mail goes over real SMTP to **Mailpit** at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. The public origin and port are `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Read every host and port from the environment and never hardcode one. The backing services named in this brief are already running at those variables.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor. The only backing services available in this environment are PostgreSQL and Mailpit, and reaching for anything else is a contract violation.

The module architecture is layered and the layering does not reverse: a token layer, then primitives, then compositions, then the marketing routes; the client shell consumes tokens and primitives and never a marketing composition, and the marketing site never consumes client state.

Auth is app-implemented: email and password exchanged for a bearer token, passwords stored under a modern memory-hard password hash, tokens expiring. `GET /api/health` returns `200` once the app is ready.

**No credential, API key, admin token or database password appears in anything the browser downloads.** Nothing in the built frontend bundle, in any JSON the API returns to a signed-out caller, in a source map, or in a rendered comment carries a value read from the environment other than the public origin and port.

**Every response carries the standard security headers**, including a strict transport policy, a policy that refuses content-type sniffing, a frame policy and a referrer policy.

**Every public route declares its own social preview title, its own description and its own preview image**, and that preview image resolves rather than pointing at an address that does not answer. No two public routes share a preview title.

Observability is a requirement rather than a nicety, because without it a slow message is not a debuggable statement. Logs are structured, one line of JSON per request on standard output, carrying the method, the route, the status, the elapsed milliseconds and a `request_id` generated at the edge of the request. That same `request_id` is returned in the body of every error response and travels with the request into the delivered events, so tracing one message from the composer to another reader's screen needs one value and nothing else. **Message content, attachment content, credentials, tokens and full network addresses are never written to a log**, not even temporarily, because a log holding message bodies is a second unmanaged copy of every private conversation.

Every request is counted against a bucket identified by an opaque value the response carries, because two different routes may share one allowance and only the service knows which; a caller keys its own accounting by the value it was told rather than by the route it thought it was calling. Each response states the allowance, what is left of it, when it resets as an absolute moment and how long until it resets as a duration. A refusal names the wait as a **duration** rather than as a moment, so a caller whose clock is wrong still waits the right amount. A refused request has not consumed allowance. Refusals for an unauthenticated, forbidden or rate-limited request count against a much larger budget whose exhaustion blocks the caller ahead of the application, which is why a refusal naming a revoked credential must not be retried in a loop. Whatever algorithm the limiter uses, two instances of the app must not each grant a full allowance for one bucket, and a window that resets on a fixed boundary must not permit double the intended rate across that boundary. The stated allowances are `50` requests per second per account overall, `5` message sends per `5` seconds per account per channel, `1` new session per `5` seconds per account, and `120` live-connection messages per `60` seconds per connection.

Every list endpoint accepts a `page_size`, defaults it to `50` and caps it at `100`. A request naming a page size above that cap is refused with the cap named rather than quietly served a smaller page. Every list response carries `next_cursor` beside its `data` array together with a `has_more` flag, and that opaque cursor is the only handle a caller needs to ask for the next page. The cursor is a keyset cursor over a stable ordering key rather than an offset, so a list that receives new rows between two reads never repeats a row and never skips one.

**Simultaneous requests.** When two requests race to write the same row, exactly one wins and the other is refused with a conflict naming what was already taken, never a silent success and never a second row written behind the first. This holds for the last seat against a member cap, for a single-use invite, for a single-use gift code, for a nonce, and for a display name within a space. A failed attempt leaves no partial state.

Every queue in this app states its bound and what happens at that bound. An unbounded queue is a defect, and the question about each one is not how big it is but what it does when it is full. The answers used here are three: presence and typing for the same subject collapse to the newest; a session whose backlog would overflow at `4096` pending events is closed with a resumable refusal so that it reconnects and replays; and a write that cannot be accepted is refused with a retryable reason. **A message is never collapsed and never dropped.** Events for one connection are flushed at most once per `50` milliseconds, preserving order within the flush.

Under pressure the app sheds capability down a degradation ladder, in a fixed order and never out of order: typing indicators first, then presence updates with the last known state frozen and labelled stale, then member list ranges served from cache, then search answering with its still-indexing state, then history beyond the most recent page refused with a retryable reason, then message sending rate limited harder, and finally read-only, where sending is refused and reading works. **Reading is the last thing to go**, because somebody who cannot read what was said gets nothing from a service that will accept their reply. Each step is an operator switch, per space and globally, and each is visible to the reader as an explicit banner rather than as an unexplained failure.

A schema change reaches production as expand, then migrate, then contract, and never as one step: the new shape is added and written alongside the old; the backfill runs in bounded batches under a rate limit, resumable from a cursor and verified; and only later is the old shape stopped and removed. No single deploy both writes a new shape and removes the old one, so a rollback to the immediately previous version is always possible without data loss. Every migration is demonstrable on a real change.

The performance budget of this build comes from its shape rather than from tuning. Nothing scrubbed by scroll position is a property that triggers layout, the message list renders only the rows within the visible window plus one window beyond it in each direction so that the rendered row count does not grow with the size of the channel, and no binary asset of any kind is fetched at run time.

## Data model

Forty-one tables. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

**Accounts and sessions.** `account` holds `id`, `email` unique and compared case-insensitively, `handle` unique and stored normalized, `display_name`, `password_hash`, `password_params`, `status`, `deletion_hold_until` and `created_at`. `session` holds `id`, `account_id`, `device_kind`, `approximate_location`, `refresh_family_id`, `refresh_token_hash`, `superseded_at`, `revoked_at`, `first_seen` and `last_seen`. `second_factor` holds `id`, `account_id`, `kind`, `secret_hash` and `enrolled_at`. `backup_code` holds `id`, `account_id`, `code_hash` and `used_at`.

**Spaces and membership.** `space` holds `id`, `name`, `slug` unique, `owner_account_id`, `member_cap`, `visibility`, `presence_fanout_threshold` and `created_at`. `membership` holds `id`, `space_id`, `account_id`, `nickname`, `joined_at` and `timeout_expires_at`, unique on the space and the account together. `role` holds `id`, `space_id`, `name`, `position`, `permissions` as a decimal string, `hoisted` and `mentionable`, with `position` unique within a space. `member_role` pairs a membership with a role.

**Channels.** `channel` holds `id`, `space_id`, `parent_category_id`, `kind`, `name`, `topic`, `position`, `capacity`, `required_tag`, `overwrite_digest` and `created_at`. `channel_overwrite` holds `id`, `channel_id`, `subject_kind` among `everyone`, `role` and `member`, `subject_id`, `allow` and `deny`, both decimal strings. `overwrite_digest` is **derived** from the channel's overwrite set rather than stored independently, and it is what makes two identically configured channels share one member list.

**Messages.** `message` holds `id`, `channel_id`, `author_account_id`, `content`, `kind`, `reference_message_id`, `edited_at`, `flags`, `nonce`, `thread_id` and `deleted_at`. A message's creation time is **derived** from its identifier and is never stored separately. `message_mention` holds `message_id`, `subject_kind` and `subject_id`, written once at send. `reaction` holds `message_id`, `emoji` and `account_id`, unique as a triple; a reaction count is **derived** as the number of those rows and is never stored.

**Side conversations and boards.** `thread` holds `id`, `parent_channel_id`, `origin_message_id`, `title`, `archive_window_minutes`, `last_activity_id`, `locked` and `archived`. `thread_member` pairs a conversation with an account. `forum_tag` holds `id`, `channel_id`, `name` and `moderator_only`; `thread_tag` pairs a conversation with a tag.

**Presence and voice.** `presence` holds `session_id`, `account_id`, `status`, `activity` and `updated_at`; an account's effective status is **derived** across its sessions. `typing` holds `channel_id`, `account_id` and `started_at`, and its remaining life is **derived**. `voice_state` holds `id`, `channel_id`, `account_id`, `self_mute`, `self_deaf`, `server_mute`, `server_deaf`, `speaking`, `request_to_speak_at` and `joined_at`.

**Read state.** `read_state` holds `account_id`, `channel_id`, `last_message_id`, `last_read_id`, `mention_count` and `flags`, unique on the account and the channel. Whether the channel is unread is **derived** by comparing those two identifiers and is never stored. `mention_count` is a cache of a count over the messages above the read mark, and every path that cannot be expressed as one step re-runs that count. `notification_setting` holds `id`, `account_id`, `scope_kind` among `account`, `space`, `category` and `channel`, `scope_id`, `level` among `all`, `mentions`, `nothing` and `inherit`, and `muted_until`; `inherit` is stored as itself and resolved when it is read.

**Events and polls.** `scheduled_event` holds `id`, `space_id`, `channel_id`, `title`, `entity_kind`, `scheduled_start`, `scheduled_end`, `status`, `organiser_zone` and `recurrence`. `event_occurrence` holds `id`, `scheduled_event_id`, `starts_at`, `detached` and `cancelled`; occurrences beyond the retained hundred are **derived** from the rule and the zone. `event_interest` holds the event, the occurrence start and the account, and its count is **derived**. `poll` holds `id`, `message_id`, `question`, `expires_at`, `multiselect` and `finalized`; `poll_answer` holds `id`, `poll_id`, `text` and `emoji`; `poll_vote` holds `poll_id`, `answer_id` and `account_id`, and every count is **derived** from it.

**Attachments.** `attachment` holds `id`, `channel_id`, `uploader_account_id`, `filename`, `declared_size`, `leading_bytes`, `detected_kind`, `digest`, `state` and `expires_at`. `stored_object` holds `digest` as its key, `byte_size` and `reference_count`. `quota_reservation` holds `id`, `account_id`, `attachment_id`, `reserved_bytes` and `settled_at`.

**Moderation.** `automod_rule` holds `id`, `space_id`, `position`, `trigger_kind`, `parameters`, `actions` and `exemptions`. `audit_entry` holds `id`, `space_id`, `actor_account_id`, `target_id`, `action`, `changes` as a list of a key with its old and new value, `reason`, `prev_hash` and `hash`, where `hash` covers every other field including `prev_hash`. `report` holds `id`, `message_id`, `reporter_account_id`, `category`, `context` and `snapshot`. `ban` holds `space_id`, `account_id`, `reason` and `created_at`.

**Invites and billing.** `invite` holds `code` unique, `space_id`, `channel_id`, `created_by`, `max_uses`, `uses`, `expires_at` and `revoked_at`; `uses` never exceeds `max_uses`. `plan` holds `id`, `name`, `interval`, `price_minor` and `currency`. `subscription` holds `id`, `account_id`, `plan_id`, `status`, `period_start`, `period_end`, `cancel_at_period_end` and `scheduled_plan_id`. `entitlement` holds `id`, `account_id`, `feature`, `source` among `subscription`, `gift` and `grant`, `starts_at` and `ends_at`; it is what every feature gate reads. `gift_code` holds `code` unique, `plan_id`, `state`, `redeemed_by`, `redeemed_at` and `expires_at`. `account_credit` holds `account_id`, `amount_minor` and `currency`.

**Extensibility and operations.** `app_command` holds `id`, `space_id` which may be absent for a global registration, `name`, `description`, `options` and `registered_at`. `interaction` holds `id`, `command_id`, `account_id`, `state`, `token`, `token_expires_at` and `acknowledged_at`. `webhook` holds `id`, `space_id`, `target_url`, `secret`, `state` and `failing_since`. `webhook_delivery` holds `id`, `webhook_id`, `delivery_id`, `sequence`, `attempt`, `state` and `next_attempt_at`. `session_event` holds `id`, `session_id`, `sequence`, `kind`, `payload` and `created_at`, where `sequence` rises by exactly one within a session. `outbox` holds `id`, `topic`, `payload`, `created_at` and `published_at`. `page_view` holds `id`, `route` and `viewed_at`.

**Consistency guarantees and invariants, as properties of the running system.** A read mark never moves backwards. A reaction count equals the number of reaction rows for that message and emoji at every moment. A space's membership count never exceeds its `member_cap`, under concurrent joins as well as sequential ones. An invite's `uses` never exceeds its `max_uses`, under concurrent redemptions. A gift code moves to redeemed exactly once, however many redemptions arrive together. A message and its outbox row both exist or neither does, so a message that is in the history was also delivered. Authorization is answered from a source that has seen every write already made to it, because a stale permission answer is a safety failure while a stale message read is an inconvenience. Reading your own writes holds for the account that made them, and a second read of a channel never returns an older view than the first.

The client holds at most `500` messages per channel, at most `20` channels, at most `5000` member records per space, and a measured row height for exactly the messages it holds. Drafts are never evicted and survive a reload. **Eviction never removes rows in a way that would join two ranges that are not next to each other**, because that recreates the false continuity the hole marker exists to prevent.

**Seed data.** Four accounts: `owner@example.com`, `moderator@example.com`, `member@example.com` and `member2@example.com`, display names `Wren`, `Ember`, `Juniper` and `Hazel`. One space `Nightjar Collective`, slug `nightjar-collective`, owned by `owner@example.com`, with a `member_cap` of `4` and three members seeded, so exactly one seat is free. Its roles are `@everyone` at position `0`, `Regulars` at `1`, `Archivists` at `2` and `Moderators` at `3`. `member@example.com` holds `Regulars` and `Archivists`; `moderator@example.com` holds `Moderators`. Its channels are the text channels `#welcome`, `#general`, `#build-log` and `#mods-only`, the board channel `#showcase`, the voice channel `Main Stage` and the stage channel `Front Room`. `#build-log` denies `SEND_MESSAGES` to `Regulars` and allows it to `Archivists`. `#mods-only` denies `VIEW_CHANNEL` to `@everyone`. `#general` and `#build-log` carry identical overwrite sets and therefore share one member list identity. Three messages are seeded in `#general`. A second space `Studio Loft`, slug `studio-loft`, is owned by `member2@example.com` and holds one channel `#studio`. One invite `NIGHTJAR-ONE` on `Nightjar Collective` into `#general` with a `max_uses` of `1`. One gift code `LOFT-ONE-SEAT` for `Loft Yearly`. Two plans, `Loft Monthly` at `1000` and `Loft Yearly` at `10000`, both `usd`.

Seeding must be idempotent, so restarting the app must not duplicate rows.

## Front-end specification

This section carries the visual and structural detail that `## UI/UX notes` states as intent. Everything here is a requirement on what a reader sees, never a value to copy: no colour is given as a code, no space as a measurement, and no motion as a timing.

### The token layer

One token layer, defined once at the root and consumed everywhere, with five families: palette ramps, spacing steps with named aliases, a radius scale, type stacks with their weights, and one namespace of component tokens per component that needs them.

Every palette token is stored as **the components a colour is made of rather than as a finished colour**, so any consumer can compose a new transparency or a new lightness against the same hue without a second token being minted, and the finished colour is derived from the components and never the other way round. Carried with those components is one saturation control on the root, so that setting a single property desaturates the entire product for a reader who finds strong colour difficult without touching a single component.

### Palette, by role

Every colour below is a role, and its family, tone and shade. No code appears anywhere in this build.

| Role | The colour |
|---|---|
| The ground the client sits on | a near-black neutral, faintly cool |
| Raised surfaces | a deep neutral, one step up from the ground |
| Muted text on dark | a mid cool neutral |
| Text on dark, and the surface of the light pages | a near-white neutral |
| The light page ground | a near-white neutral, one step off plain white |
| Overlay and shadow base | a near-black neutral |
| The primary action, everywhere | a mid, vivid indigo |
| A member who is around | a mid, soft green |
| Something that worked | a light, vivid green |
| A member who has stepped away, and a warning | a light, vivid amber |
| A member who does not want to be disturbed, and an error | a mid, vivid red |
| The paid tier | a mid, vivid magenta |
| An inline link inside the client | a mid, vivid cyan |
| That link, pointed at | a light, soft indigo |
| First feature scene | a mid, vivid magenta into a near-black neutral |
| A violet into a dusty pink | a soft violet falling into a light, soft dusty pink |
| A pink into an orange | a light, vivid pink into a light, soft orange |
| A plum into a purple | a near-black plum into a deep purple |
| Second and fifth feature scenes | a mid, soft green |
| Third feature scene | a near-black neutral over indigo |
| Fourth feature scene | a mid, vivid magenta into a mid, vivid violet |
| Sixth feature scene | indigo into a mid, vivid violet |
| The aurora pair | deep blues with a mid, vivid teal |
| The chroma pair | a mid, vivid teal with a mid, vivid violet |
| The twilight pair | a mid, vivid blue into a deep indigo |
| The midnight pair | a mid, soft indigo into a near-black violet |
| The cotton pair | a light, soft red into a light, soft blue |
| The citrus pair | a light, vivid amber into a light, soft orange |

Overlays are a **closed set of five**: three white washes at three strengths, one stronger white wash, and one black wash for the light pages. A sixth strength is a design decision rather than something invented at a call site.

Gradients are tokens, never one-offs. There are named pairs and a named set of five for each of the larger grounds, composed rather than authored per use. Four of the composed gradients are the same idea four times: a very low-strength white sheen laid diagonally across a surface so it reads as glass rather than as a flat panel, and that sheen is a primitive applied to any glass surface rather than written out wherever it is needed. One further gradient is the only one that is a solid brand colour rather than a sheen, and it is the fade at the foot of the open mobile menu, so the list fades into the primary colour rather than ending at an edge.

### Typography

Three roles, and no fourth.

- **Display.** An extended grotesque, set in capitals, at the two heaviest weights, with an italic cut used for emphasis in a few places only. Its leading is tighter than its own size, so a three-line headline reads as one solid block.
- **Text.** A neutral grotesque across the ordinary range of weights with an italic at each, used for everything the display face does not carry. Its leading is generous, and the contrast between the two densities is the loudest typographic signal on the page.
- **Code.** A monospace stack used for identifiers and for nothing else.

Each stack ends in a face the reader's system already has, and no font binary is fetched, so there is no loading phase, no swap and no period of invisible text. Where the display role falls back to a system grotesque it takes the heaviest available weight, a slight negative tracking and the same tight leading, because the character lives in that relationship rather than in the particular face. Where the arcade face used for one single string is unavailable, that string is set in the display face at the same size and the effect is simply dropped.

The display face is treated as a variable face where one is available, so a headline can gain weight under the pointer without the line rewrapping. Where none is available that moment degrades to a change of colour and **never** to a swap between two static cuts, because a swap reflows the line.

### The motion vocabulary

The working vocabulary of movement is small, closed, and each character has a job. Nothing moves in a way that is outside it.

- A very fast start with a long settle, for panels opening and for page-level reveals.
- An overshoot that passes its end and returns, for anything that should feel springy: a badge, a reaction.
- A gentle, near symmetric change, for colour and opacity.
- A slow start with a hard finish, for an element leaving.
- One accelerating throughout, for dismissals.
- One accelerating with no settle at all, for items thrown off screen.
- A back-out overshoot, for check marks and confirmations.
- Soft at both ends, for large surfaces moving.
- A quick departure with a long tail, for list items.
- A symmetric one, for loops.
- One violent overshoot, more than three times the distance, reserved for a single celebratory moment and used nowhere else.

Timing is chosen by the size of the thing moving rather than by the property. The named moments are these, and a build that names none of them ships none of them: a press ripple that has already faded by the time it stops growing; a squash, an overshoot and a settle; a standard entrance that rises a short distance while fading up; a plain fade, which is the most used of all; a loading skeleton breathing between two levels; a diagonal highlight crossing a card and stopping, with half its cycle spent off screen; the horizontal version of the same idea; a gradient dragged across text from one side to the other; a small repeated nudge on an arrow, horizontally and vertically; a tilt, a hold, a counter-tilt and a settle; a dot that swells and vanishes in the same frame a check is drawn in its place, which is one animation in two elements and reads as the dot becoming the check; four decaying squash-and-stretch bounces in which the volume is conserved at every step; a loader that turns; a doubled starfield sliding by exactly half its own width so it loops without a seam; a band translating by exactly one repeat of its own content; a field growing when it takes focus; a ring emptying, driven by a property so that where it stops is configurable; a divider whose wave reshapes rather than slides; and a text bounce measured against the type size so it scales with the type.

### Shape, spacing and depth

Spacing is one scale of steps with named aliases, and it is deliberately not a pure doubling: a small number of off-steps sit alongside it and are used where a doubling step would have been wrong. Keep them.

The radius scale runs from square through a small chip, an inline link, a menu toggle, the standard control, and two larger steps, to a fully round pill. Beyond the scale the public page uses four larger radii that are layout gestures rather than control gestures, and they are what give the page its capsule rhythm: the outer feature cards are rounded progressively more at each wider boundary, the inner scene inside them carries its own two steps, the navigation panel is square at the top and deeply rounded at the bottom, the reduced-motion still images inside the cards carry two of their own, and the mobile menu control carries one.

There is no shadow token family and no drop shadow anywhere. Depth is made three ways: a backdrop blur behind the navigation bar and behind the large feature cards; a static blur on objects that are meant to read as further away, including every star; and one real perspective on the hero composition alone, with three-dimensional transforms preserved through it.

### Iconography

Every icon is drawn geometry rather than an image file or an icon font, which is what lets this build ship no binary and still have the right shapes. Icons inherit their colour from the text around them except where a stroke colour is deliberately authored, as on the chevron, which carries its own half transparency in the stroke rather than on the element so that it does not fade its own hit area.

There are **two different three-bar menu marks and they are not interchangeable**: one with square ends and three equal bars, one with round caps and a shorter third bar, used in different places. Do not tidy them into one.

The set is: the two menu marks, a downward chevron used both alone and inside the language control, a download mark drawn as a shaft with an arrowhead over a tray, and a row of five social marks of which four are drawn geometry. An icon is decorative and hidden from assistive technology unless it is the only content of a control, in which case it carries an accessible name saying what it does rather than what it depicts: the menu control is named for opening the menu, not for being three lines.

The brand mark is not artwork in this build. It is the product name set in the display face inside a pill occupying the same box the mark would have occupied, so every layout that reserved space for a mark still balances, plus a single-letter version in a circle on the primary colour for the places that carry the glyph alone. Four such boxes exist: a header lockup, a footer glyph, a large footer band drawn at the container's width, and the marketing header's own lockup.

### Global chrome

**Two chromes, and the difference is not cosmetic.** The marketing chrome sits on `/` with no ground of its own, so the starfield shows through it; it carries the brand lockup, nine navigation entries and the sign-in control. The utility chrome sits on every other public route on a light ground, carries the wordmark, the same nine entries as plain links and the same sign-in control, and has no scroll state. They share the navigation tree and nothing else.

At the top of the marketing page the bar shows its nine entries. **Past the hero it collapses to a pill:** the entries go, the lockup tucks into a small light capsule, and the sign-in control stays exactly where it was. This is one element changing state rather than two bars swapping over, so nothing on the page reflows as it happens, and the two treatments of the lockup are cross-faded through each other rather than switched. What sits behind the bar is genuinely blurred rather than dimmed.

**The navigation tree.** Nine top-level entries, six of which open a panel. `Download`, `Loft` and `Careers` are plain links. `Discover` opens a panel of `2` under one group heading. `Safety` opens a panel of `10` under two group headings of `5` each. `Quests` opens a panel of `3`. `Support` opens a panel of `3`. `Blog` opens a panel of `7` under one group heading. `Developers` opens a panel of `10` under two group headings, of `6` and `4`. Every entry inside a panel carries a screen-reader-only position of the form `n of m`, where `m` is that panel's own count.

**The panel itself** is square across the top and deeply rounded at the bottom, with a background layer carrying the same shape. The entry that carries new items uses a variant that is evenly rounded instead. Group headings are set at reduced opacity, and separators at a far lower one. A closed panel is fully transparent rather than removed. Pointing at an entry inside a panel reduces its opacity slightly; pointing at a top-level entry on the marketing chrome **fills the whole entry with the primary colour**, which is neither an underline nor a colour change on the label. On the light pages every text link underlines on hover and none underlines at rest, and the small decorative marks either side of a link change colour with it rather than being styled separately, which is a detail that looks broken when it is missed.

Below the tablet boundary the entries collapse behind the menu control, and the open menu blurs what is behind it and fades at its foot into the primary colour. Its close control is a softly rounded mark.

**The footer** is one footer on both chromes, with five regions: the glyph alone; a language control rendering `English`, with the chevron inside it; a row of five social marks on even centres; four link columns; and a band carrying the large wordmark. The columns are `Product` with `Download`, `Loft`, `Status`, `App Directory` and `Gift Cards`; `Company` with `About`, `Jobs`, `Brand` and `Newsroom`; `Resources` with `Support`, `Safety`, `Blog`, `Feedback`, `Creators`, `Community`, `Developers` and `Quests`; and `Policies` with `Terms`, `Privacy`, `Cookie Settings`, `Guidelines`, `Acknowledgements`, `Licenses` and `Company Information`. Column headings are set smaller than their entries. On the marketing page the illustrated band sits above the footer with the characters standing on its top edge, so that edge is a compositional line rather than a boundary.

**The skip link** is the first focusable element in the document, is parked just above the top of the viewport, becomes visible on focus, targets the main landmark, and is never removed on the grounds that it is invisible.

### The home page, movement by movement

The spine of the page is nine full-height movements in this order: the hero; feature one with its text on one side; feature two with its text on the other; feature three; the marquee band at full width; feature four; feature five; feature six; the closing panel; and then the footer band. **The alternation is strict and it is the page's whole layout rule**, and the marquee interrupts it exactly halfway.

**The hero.** A display headline in capitals over three lines at the widest tier, a short body paragraph set at about four lines across a fraction of the column, and the two actions side by side. Beside and behind them sits the product composition, under the one perspective container, over a starfield laid on a vertical gradient into the primary hue. Loose objects float outside the composition: a crown above it on one side, a soft cloud on the other, and a plump shape further back, all of them blurred. The headline column and the composition **overlap by a sliver of empty space rather than sitting in two separate halves**, and that overlap is why the composition reads as being behind the type.

**Every feature movement is the same construction**, and that construction is most of why the page reads as expensive. An outer card, rounded into a capsule, frosted so heavily over the starfield that the stars behind it become a soft field of light rather than points, with one of the white sheen gradients as its own ground. Inside it, a smaller and **perfectly sharp** panel on a saturated two-stop ground, one per card. Inside that, a small honest picture of the product actually doing the thing the headline claims, drawn as live interface at interface scale rather than as artwork. Beside it, a display headline and a body paragraph. Under a reduced-motion preference each card shows a still twin with its own slightly different rounding.

The six scenes are: an expression picker with an upload control and a reaction chip; a live stream tile over three participant tiles; a channel list with a channel title and three message rows; a member list grouped into online and offline with one row pointed at; a group call on a phone with a screen-share prompt and an activity tile; and a column of five platform badges with one enlarged beside them. **The objects that break out over a card's edges are the composition:** a head over the top edge, a cube entering from one side, a plant growing up from the bottom. A build that clips every scene inside its card produces a tidier page and loses the entire effect, which is that the illustration stands in front of the interface rather than living inside it.

**The marquee.** A full-width band, outside the card rhythm, of four short words repeating and separated by the brand glyph, set in the display face in capitals at the section headline size, translating sideways in one linear, infinite slide while the collapsed header pill floats over it. **It must be seamless**: the band is wider than the viewport and translates by exactly one full repeat of its own content, computed from the real width of the words rather than from a round number that looks close, because translating by anything else produces a visible jump on every cycle. Under reduced motion it is static and shows one full repeat.

**The closing panel.** One display line in capitals over two lines, centred, and one action, on the densest part of the starfield over the deepest ground on the page, with the cast of characters walking into frame from the bottom edge below it.

**The wave divider.** Between two movements a divider whose wave **reshapes rather than slides**, moving between three states that all keep the same number of control points, which is what lets them interpolate at all. Any replacement wave keeps that count identical across all three.

**On a phone.** The chrome is the lockup on one side and the menu control on the other, with no entries. The hero puts the composition first, then the headline, then the body, then the actions stacked and full width. The headline wraps to three lines at a reduced size. Cards go full width with the scene above the text and the smallest of the card radii. Almost none of the scroll-driven movement runs.

### The scroll system

Scroll drives a small cast of objects at different speeds, and the difference between them is what makes the flat page feel deep. Ordered from nearest to furthest, and carried as an order rather than as offsets: a coin travels furthest, an egg shape slightly less, a cube and a set of objects less again, a plump shape and a plant less again, and the second character barely moves at all. One element moves horizontally rather than vertically.

Three of them also carry a **static rotation**, which is what stops the composition reading as a stack of parallel planes. Two of those are one rule applied at two strengths: the same tilt and the same offset, then twice both. A third is a clean tilt of its own. Two objects are mirrored in three dimensions rather than flipped in two, and one is pushed slightly away from the reader.

**The starfield.** A field of individually authored stars rather than a repeating pattern. Each carries its own faintness from a small measured set of values, each fades across its own part of the scroll, and a static blur sits on the layer. That is why it reads as space rather than as wallpaper, and it is why the generated replacement must **preserve the distribution of faintness rather than scattering evenly**: the faintest values are the most common, brighter stars are drawn slightly larger, and the field is two copies side by side translated by exactly half the layer width so it loops without a seam.

Two rules bind everything here. **Scrubbing is driven from scroll position rather than from time**, so reversing the scroll reverses the animation exactly with no easing back to a resting state, and it feels attached to the reader's finger rather than played at them. And every scrubbed property is one that does not trigger layout. Hints that a property will change are declared on exactly the elements that need them and nowhere else, because declaring them globally costs more than it saves. At the narrow end almost none of this runs, and that is the specification rather than an omission: a phone would rather spend the effort on scrolling smoothly.

### The illustration layer, with no binaries

Everything visible other than type and chrome is generated under a zero-asset rule, and the substitution is described here rather than shipped. No image, video, font binary or vector-animation file ships. The whole inventory a product of this shape normally carries, hundreds of still images, animated stills, photographic poster frames, short films, audio cues and font binaries, is replaced procedurally, and each generator is deterministic so that the same seed produces the same output and a rebuild is not a redesign.

- **Grain and texture.** Each section ground carries a fine, low-contrast grain, a generated tiling texture rather than a shipped one, from a noise filter tiled so that it never shows a visible repeat at any boundary, with its colour noise removed so it does not read as a compression artefact, and laid on at a lower strength over dark grounds than over light ones.
- **Characters and objects.** Every illustrated character and object becomes a soft-edged shape seeded from the identity of the thing it replaces: a rounded blob of a handful of control points, filled with a two-stop gradient drawn from that section's own gradient pair, with a feathered edge so it reads as an out-of-focus object, at the bounding box of the object it replaces and carrying that object's transform and its place in the depth order unchanged. The placeholders keep the names and the positions of what they replace, so real artwork later is one substitution rather than a rewrite.
- **The vector animation.** A small illustration that animates by revealing itself through a changing mask, scrubbed by scroll position over the same range, authored as a short sequence of evenly spaced stops rather than played by a runtime. It reveals the wordmark from one side to the other.
- **The moving surfaces.** Where the reference used background film, a drawn loop stands in: the scene's own gradient with two slow soft highlights moving out of phase, with the interface elements drawn as **live markup over it rather than painted into it**, which is what keeps those scenes legible, selectable and translatable. Each loop starts only when its surface is at least half visible, stops when it is not, never carries sound, and shows a still frame under reduced motion.
- **Media placeholders inside the product.** Every derivative of an attachment is generated from the attachment's own identity rather than computed from bytes that do not exist. An attachment with no bytes renders as a gradient seeded from the attachment's own identity, drawn at the attachment's declared dimensions so **nothing reflows** when it resolves, with two stops from the palette at an angle from the same seed. Its blur summary is a coarse average of that gradient. An audio attachment renders a waveform that is a deterministic function of the same seed, as a fixed number of bars whose amplitudes follow a smoothed walk and decay over the last few so it reads as a recording rather than as noise. A video attachment renders the image placeholder with a play control over it. The same attachment always produces the same placeholder.

### The client shell

Four columns. A narrow **space rail** carrying one avatar control per joined space plus a create control and an explore control, which becomes a drawer at the narrow end and never disappears otherwise. A **channel sidebar** carrying the space header, the channel tree, the voice roster and the account tray, which becomes a drawer at the same point. The **message column**, fluid, with a header, the message list and the composer, going full width at the narrow end. And the **member list**, grouped by hoisted role with the online group first, hidden below the wide boundary and toggled from a control in the channel header.

The shell is one mounted tree for the whole session. **Moving between channels swaps the message column's source and must not unmount the rail, the sidebar, the voice connection or the composer draft.**

Four layers of state, in order of authority, and collapsing any two of them breaks the product: server truth, which is permanent and authoritative; the optimistic overlay, which lives until a send resolves and is then replaced by server truth; the local draft, which is local only and survives a reload; and ephemeral view state such as the scroll anchor and which categories are collapsed, which lives for the session. **Anything that can arrive from the service is owned by the service and is never written by the client except through the optimistic overlay.** The overlay reconciles by the client's nonce rather than by content and rather than by arrival order, so a message that arrives from the service before its own send has returned appears **exactly once** and does not reorder around its neighbours when the send finally resolves.

**The message list.** It renders only the rows in the visible window plus one window of overscan in each direction, so a channel holding a hundred thousand messages does not grow the rendered row count. Rows are variable height and their height is not known until it is measured; measured heights are cached against the message and invalidated on an edit, on an attachment resolving, and on a width change. **When older messages load in above, the row the reader is looking at must not move**, which means anchoring on a row and its offset within the window and restoring after layout, never on a distance from the top of the list. While the list is already at the bottom, an arriving message scrolls it; **once the reader has scrolled away it must not**, and a jump control appears carrying the count of what has not been seen. Jumping to an arbitrary message loads a window around it, highlights it briefly, and leaves the list in a state from which paging works in both directions. Resizing the window, toggling the member list and switching to a compact row all invalidate every cached height and none of them may lose the anchor.

**The key map belongs to the shell rather than to the composer**, because every one of these has to work while the composer holds focus, and focus is never trapped by the message list: a quick switcher that searches fuzzily across spaces, channels and people; previous and next channel in the order shown; previous and next unread channel; mark the whole space read; an escape that dismisses the reply target, then the jump state, then blurs; an up arrow in an empty composer that edits the reader's own most recent message in that channel; a microphone mute toggle; and page up and page down that page the list without moving focus out of the composer.

**Offline and reconnect.** While the live connection is retrying, a warning bar shows, the composer stays enabled and sends queue. While the browser reports no network at all, a neutral bar shows and the same holds. On reconnecting into a resumed session the bar clears and the queue flushes in order with no reload. On reconnecting into a new session the bar clears, the open channel's caches are refetched and the queue flushes after that refetch. **Queued sends flush in the order they were composed, one channel at a time, and a channel whose flush fails does not block another channel's queue.**

### The not-found page and the policy pages

The not-found page is a designed page rather than an apology, and more people will see it than will see the policy set. It carries the utility chrome on the light ground, a display headline in capitals in the primary colour in a left column, a short body of about four lines, three stacked inline links spaced evenly apart that change to a deeper shade and underline when pointed at, and an illustration in the right column carrying the numerals of the status as live type rather than as artwork so the page is legible before anything else loads. Its three links point at the status page, the product's social profile and the support site.

The policy pages carry the utility chrome, body type on comfortable leading, headings in the display face in sentence case at the card headline size, a light ground and the footer on the dark one. **This is the one part of the site with no motion of any kind, and that is correct.** The measure is capped so a line never runs much beyond about ninety characters at any width, because an uncapped legal document on a wide monitor is genuinely hard to read and this is exactly the kind of document where people give up.

### Copy

Every string is pinned. The display lines are set in capitals.

| Where | String |
|---|---|
| Hero headline | `A ROOM THAT IS ALWAYS OPEN` |
| Hero body | `Rookery is where your group already is. Make a space, add the channels you need, and talk when you feel like it. No meeting, no invite, no schedule.` |
| Primary action | `Download for Windows` |
| Secondary action | `Open Rookery in your browser` |
| Persistent action | `Log In` |
| Feature one headline | `SOUND LIKE YOURSELF` |
| Feature one body | `Reactions, custom marks and a profile that follows you into every space. Say something in a way that is recognisably yours.` |
| Feature two headline | `SHOW THE WHOLE TABLE` |
| Feature two body | `Share what is on your screen and let the room watch together, at the quality you would want if you were sitting beside them.` |
| Feature three headline | `DROP IN, DROP OUT` |
| Feature three body | `Voice channels stay open. Join when you are free, leave when you are not, and nobody has to call anybody.` |
| Feature four headline | `SEE WHO IS AROUND` |
| Feature four body | `A glance down the side of the room tells you who is here, who has stepped away and who would rather not be disturbed.` |
| Feature five headline | `SOMETHING TO DO TOGETHER` |
| Feature five body | `Boards for the things worth keeping, side conversations for the things that are not, and events for when you do want a schedule.` |
| Feature six headline | `THE SAME ROOM EVERYWHERE` |
| Feature six body | `Every space, every unread mark and every draft, in the same state on whichever thing you happened to pick up.` |
| Marquee | `TALK`, `BUILD`, `PLAY`, `STAY` |
| Closing line | `THAT IS THE BOTTOM. GO SAY SOMETHING.` |
| Not-found headline | `NOTHING LIVES HERE` |
| Not-found body | `This address does not go anywhere. It may have moved, or it may never have existed. Here are three places that do exist.` |
| Not-found links | `Status`, `Rookery on social`, `Rookery Support` |
| Skip link | `Skip to main content` |
| Language control | `English` |

The voice is casual and second person throughout, and the closing line simply admits the reader has reached the end of the page. That is a decision rather than an accident, and rewriting it into corporate English would change the product more than any colour would.

Inside the six product scenes the labels are copy rather than artwork: the expression picker reads `Upload`, `Emoji`, `Stickers` and `Frequently Used`; the stream tile reads `LIVE`; the channel list reads `Nightjar Collective`, `Text Channels`, `#welcome`, `#general`, `Voice Channels` and `Main Stage`; the member list reads `Online - 4` and `Offline - 3`, with `In a Voice Channel` beneath; the call scene reads `Front Room` and `Share your screen`; and the sixth scene carries five platform badges and no text. The member names, message lines and activity names inside those scenes are invented placeholders and are never real accounts, and no third-party product name appears in any of them.

## Constraints

- One product, two surfaces, one origin. No second origin for assets, for the client or for anything else.
- No real-time audio or video media of any kind. Voice channels carry rosters, states and capacities; they carry no sound. No audio pipeline, no codec, no media transport, no congestion control, no simulcast and no screen capture.
- No file bytes are stored anywhere. Attachments are records and accounting only, and every preview is generated.
- No payment provider, no card, no charge and no inbound provider webhook. The paid tier is granted and revoked inside this app.
- No push delivery to a device, no mobile application and no desktop application; the download action links to builds that are described rather than served.
- No sharding, no resharding, no multi-region placement and no replica topology to configure.
- No direct messages between accounts outside a space, no timeline or algorithmic feed, no friend graph, no monetised creator surface and no third-party analytics.
- No second database, cache, queue, object store, identity provider or mail vendor. No external network call at run time.
- No binary asset of any kind: no image file, no video file, no audio file, no font binary and no vector-animation file.
- The app stays responsive with a space of `100000` messages in one channel, `5000` members in one space, `40` channels in one space and `4` spaces per account.

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
- The backing services named in this brief are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password`, `handle`, `display_name` | the account and a bearer token |
| `POST /api/auth/login` | `email`, `password`, optional `second_factor_code` | a bearer token and a refresh token |
| `POST /api/auth/refresh` | `refresh_token` | a new pair, the old refresh token spent |
| `GET /api/auth/sessions` | | a top-level JSON array of this account's sessions |
| `DELETE /api/auth/sessions/<id>` | | the session ended and its live connection closed |
| `POST /api/invites/<code>/redeem` | | the membership and the space it joined |
| `GET /api/spaces` | | a top-level JSON array of the spaces this account belongs to |
| `GET /api/spaces/<space>/channels` | | a top-level JSON array of channels this account can see |
| `GET /api/spaces/<space>/members` | `ranges` | grouped counts and the rows inside the named ranges |
| `GET /api/channels/<channel>/permissions/<account>` | | the resolved permission set as a decimal string |
| `GET /api/channels/<channel>/messages` | `limit`, and one of `before`, `after`, `around` | a top-level JSON array, newest first in every direction |
| `POST /api/channels/<channel>/messages` | `content`, `nonce`, optional `reference`, `attachment_ids`, `flags`, `poll` | the message, or the original message when the nonce repeats |
| `PATCH /api/messages/<id>` | `content` | the message with `edited_at` set |
| `DELETE /api/messages/<id>` | | the message removed |
| `POST /api/channels/<channel>/messages/bulk-delete` | `ids` | one removal event, never one per message |
| `PUT /api/messages/<id>/reactions/<emoji>/me` | | the reaction set and its derived count |
| `DELETE /api/messages/<id>/reactions/<emoji>/me` | | the reaction set and its derived count |
| `POST /api/channels/<channel>/typing` | | accepted, with the service's own timestamp |
| `POST /api/channels/<channel>/ack` | `message_id`, `manual` | the read state, never moved backwards |
| `GET /api/read-states` | | a top-level JSON array of this account's read states |
| `PUT /api/notification-settings` | `scope_kind`, `scope_id`, `level`, `muted_until` | the stored setting, with `inherit` stored as itself |
| `GET /api/spaces/<space>/search` | `q`, `cursor`, `limit` | hits with context, a total marked approximate, or a still-indexing answer |
| `POST /api/channels/<channel>/attachments` | `files` with `filename`, `file_size`, `leading_bytes` | one upload target per file, with its expiry |
| `POST /api/spaces/<space>/members/<account>/timeout` | `expires_at`, `reason` | the membership with its absolute expiry |
| `POST /api/spaces/<space>/bans` | `account_id`, `reason`, `delete_message_days` | the ban, the membership removed |
| `GET /api/spaces/<space>/audit` | `cursor`, `limit` | a top-level JSON array of entries, each carrying its chain fingerprints |
| `POST /api/spaces/<space>/audit/verify` | | whether the chain verifies, and the first entry that breaks it if not |
| `POST /api/gift-codes/<code>/redeem` | | the entitlement granted, or a refusal naming the code as spent |
| `POST /api/subscriptions/change-plan` | `plan_id` | the scheduled change, with credit and charge in integer minor units |
| `GET /api/entitlements` | | a top-level JSON array of this account's live entitlements |
| `GET /api/gateway/events` | `after` | the events after that number, or a refusal when it is older than the window |
| `GET /api/health` | | readiness |

Bearer auth is required on everything except signup, login, refresh, health and the public site's own routes. A webhook receiver authenticates by signature and never by a member's token. A successful call returns the named resource or shape, and an invalid or unauthorized call is rejected as a client error, never a `5xx` and never a silent success.

### No mocks

Mail is not simulated. An in-memory list of sent messages, a log line saying a notice went out, a `{"sent": true}` the app returns to itself, or a mail written to a file on the app's own disk are each a contract violation however good the interface looks. The same holds for the datastore: rows held in a process rather than in PostgreSQL disappear when the app restarts, and a member list assembled from a module-level dictionary is not a member list. **Mailpit and PostgreSQL are the fact: this app's own screens and its own tables can only reflect what lives in them, never substitute for them.**

## Definition of done

A visitor can read the home page, open Rookery in a browser, sign up, redeem an invite and send a message into a channel that another signed-in member watches arrive without reloading. The last seat in a space goes to exactly one of two people racing for it, and the other is told the invite is spent. A mention reaches the mentioned member's own inbox and nobody else's. A member silenced by a moderator can still read the room and can neither post nor react.
