# Immersive Experience Reel

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, move from the entry scene into the reel of work and open a project without a page load, and a signed in producer must be able to star three projects, drag them into order, write a note, reload and find both kept, and send the reel as a pitch the studio answers, without hitting an error page. A second producer must not be able to learn that the first producer's reel exists by any means: another producer's reel, a reel that was never created and a reel id of the wrong shape answer identically. Every pitch and reset mail must arrive as a real message in Mailpit; a line the app writes to its own log or its own table does not count.

## Overview

Immersive Experience Reel is the public showcase of Halcyon Works, a creative technology studio that builds games, multiplayer experiences, extended reality and installation pieces, and websites that behave like places, together with the private client desk attached to it. The showcase is presented as a single continuous rendered environment rather than a set of documents: a visitor arrives into a loading sequence, is asked `What are you looking for?`, moves through a reel of projects, opens one, reads its case line, and can ask the in-scene assistant about it. The extension adds accounts: a signed in producer collects projects into a reel, orders and annotates it, and submits it as a pitch; studio staff read the pitch queue and reply.

Its audiences are brand and platform clients looking for proof the studio can build what they need, producers sizing a pitch who want year, client and category per project, candidates who want to know what the studio makes and how it feels to use, and signed in producers returning to the reel they were assembling last visit. Studio editors answer pitches and look after the work; the admin also decides what is published and who is staff.

It deliberately is not a social product and not a content management suite. There are no comments, likes or follows, no public gallery of producers' reels, no presence and no live cursor, no floating toast, no dropdown anywhere, no paging of the fifteen projects, no payment of any kind, no third-party analytics, and no second language at launch. It does not ship a single image, video, texture, model, font file or audio file of its own: everything visible and audible is generated.

The genuinely hard part is that one rendered scene carries every public state while every word in it stays real, reachable text, and that a producer's reel stays exactly one reel: writes made against an old version of it are refused rather than quietly merged, and nobody outside its owner and the studio can learn it exists.

## User roles

| Role | Can do |
|---|---|
| Visitor (not signed in) | View every public state; use the assistant; send an enquiry; sign up, sign in, reset a password. **Cannot create a reel, add to one, read a shared reel, submit or read a pitch, or read any account.** A visitor is asked to sign in at the first action that would write anything. |
| `producer` | Everything a visitor can do, plus: create reels (at most ten), add and remove published projects on their own reels, reorder and annotate their own reels, share and revoke a link to their own reel, read any shared reel while holding its link, submit their own draft reel as a pitch once their email is verified, read and reply on their own pitches, withdraw their own pitch. **Cannot read or change another producer's reel or pitch (it answers exactly as a reel or pitch that does not exist), cannot change a pitch to any state other than `withdrawn`, cannot see draft projects, cannot publish or edit projects, cannot reach any studio route or account.** |
| `editor` | Everything a visitor can do, plus: read every reel read-only, read every shared reel, read every pitch, reply on any pitch, change a pitch to `acknowledged`, `in_conversation` or `closed`, see draft projects and their state, edit a project's text fields and link. **Cannot create or change a reel, cannot submit a pitch, cannot publish or unpublish a project, cannot change any account's role.** |
| `admin` | Everything an editor can do, plus: publish and unpublish projects, and change another account's role from `/studio/people`. **Cannot change their own role, and cannot demote the last remaining admin.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a producer session to any editor-only or admin-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. Every write is checked in order: is there a session, does the role permit the capability, and does this account own the object.

Signup is **open**: anybody may sign up, and self-signup always creates a `producer`. `editor` and `admin` are granted by an admin, never requested. Four accounts are seeded:

| Email | Role | Display name | Organisation | Verified |
|---|---|---|---|---|
| `admin@example.com` | `admin` | `Mira Halden` | `Halcyon Works` | yes |
| `editor@example.com` | `editor` | `Theo Vance` | `Halcyon Works` | yes |
| `producer@example.com` | `producer` | `Priya Castell` | `Northlight Agency` | yes |
| `producer2@example.com` | `producer` | `Jonah Reyes` | `Farrow Kiln` | yes |

## Core features

### The scene and its states

1. The public site is one rendered scene with six states, not a set of pages: `loading` (on arrival, the requested address is held), `entry` at `/`, `intent` at `/work?category=<slug>`, `reel` at `/work`, `project` at `/work/<slug>`, and `contact` at `/contact`. Changing state never reloads the document and never tears down the environment.
2. The document never scrolls on a public route: the document is exactly one viewport tall at every width and no surface relies on document scroll position. Wheel, trackpad, touch drag, arrow keys and page keys all drive a single normalised state position instead.
3. Wheel input is accumulated and normalised rather than applied per event. An accumulated normalised delta of `1.0` advances one state, and the accumulator decays to zero after `0.4s` without input, so a slow scroll never trips a state change on its own. Touch drag counts at `1.5` times its pixel delta.
4. `ArrowDown`, `PageDown` and `Space` advance one state; `ArrowUp`, `PageUp` and `Shift+Space` retreat one state; `Escape` leaves a project, the same as `<- Close`. From `entry`, advancing enters `reel`. From `reel`, selecting a project enters `project`. From `project`, advancing (the `SCROLL TO CLOSE` prompt) returns to `reel`: the same wheel gesture means go deeper in `reel` and come back in `project`.
5. **`Tab` never changes scene state.** A person moving through the interface with `Tab` reaches every control while the environment stays still and the address does not change.
6. `SCROLL DOWN` and `SCROLL TO CLOSE` are focusable buttons, not decorative text: `Enter` on `SCROLL DOWN` does exactly what `ArrowDown` does from `entry`, and `Enter` on `SCROLL TO CLOSE` returns a project to `reel`.
7. Every state change rewrites the address without a document load, and every address resolves directly into its state on a cold load. A state change replaces the history entry within one state family and pushes a new entry between families, so the browser's back control leaves a project rather than replaying every wheel notch.
8. **Every string drawn into the scene also exists in the document as text**, in reading order, available to assistive technology and to text search, hidden visually by a technique that keeps it in the accessibility tree. Sizing it to nothing is acceptable; removing it from layout is not. When the render context is unavailable those strings become the visible page.
9. **A machine that cannot draw the scene still gets the whole site.** A browser without hardware acceleration is never refused outright; it degrades. When the render context is unavailable, the environment becomes its state's clear colour, the interface renders unchanged, every state stays reachable, and a banner reads `Running without the full scene.` It is never a full-screen refusal and never a notice that the browser is not supported.
10. Every state change is announced assertively with the state's name and its heading, because nothing else tells a listener the world changed.

### The entry state and the intent links

1. `/` shows the question `What are you looking for?` and exactly five intent links, in this order: `-> games`, `-> multiplayer`, `-> XR / VR / AI`, `-> installations`, `-> websites`. The `->` is literal text, and `XR / VR / AI` is written space slash space.
2. The five links are the project category vocabulary and the filter control at once: they resolve, in order, to `/work?category=games`, `/work?category=multiplayer`, `/work?category=xr`, `/work?category=installation` and `/work?category=web`. The entry state carries no other positioning statement, no wordmark in the chrome, no menu and no footer.
3. On a reel with no category set the five links are shown; with one set they collapse to the selected one plus a clear control.
4. `SCROLL DOWN` sits above the intent list. The studio mark sits at the centre of the entry state inside the scene, and it is not a link.

### The reel of work

1. `/work` lists every published project, one row each, in a single column at every width. A row carries the project title, a metadata line reading year, client and category separated by space slash space, for example `2021 / U.S. Skyforce / xr`, and a rule under it. The metadata line shows the first of the project's categories in category order, as its lower-case slug.
2. Selection: pointing at a row brings its title to full strength and dims the other rows. Selecting a row enters that project, and the environment retints toward the selected project's colour during the transition, so the project's colour arrives before its copy does.
3. Each row carries a star control at its right edge. Its accessible name is `Add <title> to your reel` when the project is not on the active reel and `Remove <title> from your reel` when it is. Signed out, the star is present and routes to `/signin?next=/work`, so the reel looks the same to everyone.
4. The star acts immediately: the star fills and the account pill count rises before the server answers, with no waiting indicator. If the server refuses, the change is put back first and only then does the failure appear.

### Search, filter and sort

1. Every part of the query lives in the address, so a filtered view can be sent, bookmarked and reloaded without loss, and it survives the state machine. The parameters are `category` (one of the five slugs, repeatable), `year` (four digits, repeatable), `client` (a client slug), `q` (free text, at most `80` characters) and `sort` (`recent`, `oldest` or `title`, default `recent`). There is no `page`.
2. Values inside one parameter combine with **or**; different parameters combine with **and**. For example `/api/projects?category=games&year=2021&year=2022` returns `Welcome to Stonehall`, `20 Years of Nexus` and `Discover your Familiar`, in that order, with `total` `3`. The control row states the combining rule in words whenever more than one parameter is set.
3. A client slug is the client name with accents removed, lower-cased, every run of characters that are not letters or digits replaced by one hyphen, and leading and trailing hyphens trimmed: `U.S. Skyforce` is `u-s-skyforce` and `Papier Mâché Press` is `papier-mache-press`. An unknown client slug returns an empty result, not an error.
4. `q` matches the project title, the client name and the description as a substring, case-insensitive and **accent-insensitive**: `societe` finds the project whose client is `Société Parallèle`, and `mache` finds the one whose client is `Papier Mâché Press`. There is no fuzzy matching and no stemming.
5. Matches are ordered by where they matched first, then by the sort: every title match comes before every client-name match, which comes before every description-only match, and inside each group the sort applies. For example `q=frontier` with the default sort returns `Frontier Beyond`, `Renewable Frontiers`, then `Secret Tide`, because `Secret Tide` matches only in its description.
6. `recent` orders by year, newest first, and projects sharing a year by the studio's own order (`position`, lowest first). `oldest` is the exact reverse of `recent`, so projects sharing a year come out in descending `position`. `title` orders alphabetically, case-insensitive and accent-insensitive, comparing the folded titles character by character.
7. An unknown category, a `year` that is not four digits, a `q` longer than `80` characters or an unknown `sort` is rejected as invalid with the field named, and nothing else is returned.
8. The search field updates the address after the typing has settled (`300ms` after the last keystroke) and replaces the history entry rather than adding one, so `Back` leaves the reel rather than replaying every keystroke. Sorting is three capsules, never a dropdown.
9. A filter that matches nothing shows `Nothing matches that.`, a line naming the filters in effect, and a `Clear filters` control. `Clear filters` keeps `sort`.

### The project view

1. `/work/<slug>` shows, in the lower left of the frame and nowhere else: the title, the metadata line, the description (one or two sentences, stored in sentence case and rendered upper case), `Project Link` (underlined, the only underline in the product, opening the project link in a new context) and `<- Close`. `SCROLL TO CLOSE` sits near the top centre. The assistant input sits below the copy.
2. The two captured projects carry their measured copy exactly. `E.D.E.N.`: `2021 / U.S. Skyforce / xr`, `A cinematic real-time experience offering guided levels to test and enhance cognitive skills`. `Rally`: `2014 / Nimbus / installation`, `A multi-device racing experience that syncs in real-time. Developed for the client's developer conference`. Neither description ends in a full stop, and that is reproduced.
3. There are three ways out of a project and all return to `reel`: `SCROLL TO CLOSE`, `<- Close` and `Escape`. There is no related-projects row.
4. Each project carries a tint and a key-light direction. The interface never reads them: the text stays the same near-white on every project, and the environment alone changes colour.
5. For a signed in producer the star sits to the right of `<- Close`, with a metadata-sized line under it naming the reel the project is on when it is on one.
6. A draft project, a project that does not exist, and a slug of the wrong shape all render the not-found state for anybody who is not an editor or admin.

### The not-found page

1. An address the product does not serve, and `/work/<slug>` for a slug that is not a published project, render the product's own not-found page: `We cannot find that.`, a short line in ordinary words, and a capsule back to the reel. The chrome and the environment stay.
2. The not-found page answers not-found: the HTML document for that address comes back with a not-found status, not a success status, even though the application shell renders it.
3. Under `/desk` and `/studio` the same layout reads `That is not yours to open.`, a line naming the role that can open it, and a capsule back to the visitor's home. A missing object and a forbidden one render identically.

### Contact and enquiries

1. `/contact` offers both an enquiry form and the assistant, and says which is which: the form is for somebody who wants a record of what they sent, the assistant for somebody who wants an answer now. It also shows the heading `Contact`, the studio address `hello@example.com`, and a row of three social marks.
2. The enquiry form takes `name`, `email`, `timing`, `summary` and `contact_preference`. `name` is required (`Tell us your name.`), `email` must be a valid address (`Enter an email address we can reply to.`), `timing` is one of the four timings (`Choose a timeframe.`), `summary` is `20` to `2000` characters (`Tell us a little more, at least twenty characters.` or `That is over two thousand characters.`), and `contact_preference` is `email` or `call` (`Choose how we should reply.`).
3. The form carries an unattended decoy field named `company_website`. An enquiry that arrives with `company_website` filled in is refused as invalid, nothing is stored, and no mail is sent.
4. A form submitted repeatedly in quick succession is refused: at most `5` enquiries per hour are accepted from one address block, and each one beyond that is refused with `That is a lot of enquiries. Try again in an hour.`, stores nothing and sends nothing.
5. An accepted enquiry gets a reference `EN-` followed by six digits, starting at `EN-000001`, and sends two mails: one to the sender and one to the studio queue (see Mail).

### The assistant

1. The resting assistant is a text input reading `ASK ME ANYTHING...`. Opening it focuses the input and opens the panel without changing scene state. `Escape` closes the panel and returns focus to the input.
2. A question asked in `project` state carries that project as context; asked anywhere else, the studio and its published work are the context. The project context is attached by the server from `project_slug`, never taken from anything in the question text. An answer given with a project as context names that project's title.
3. The assistant answers from the studio's own published records. There is no outside model service in this environment and none may be called.
4. The typing indicator appears the moment a question is submitted and is removed when the first part of the answer renders, never on a timer. The answer renders progressively.
5. A question is capped at `500` characters on the server: a longer one is rejected as invalid with `Keep your question under five hundred characters.`, and an empty one with `Ask a question first.`
6. **An answer is plain text and never carries an outbound link.** It may name a route on this site, such as `/contact`; it never contains an `http://` or `https://` address, including a project's own link. Angle brackets in an answer show as characters.
7. **A draft project is never context.** `project_slug` naming a draft project, or a project that does not exist, is answered as not found for anybody who is not an editor or admin, and the answer never mentions a draft project's title.
8. When the service fails the panel stays open and shows `That did not reach us. Try again.` with a retry control, and the question stays in the input. An answer that is refused or empty reads `I do not have an answer for that one.` with a link to `/contact`. Scrolling while the panel is open closes it and advances the state, because the wheel belongs to the scene.
9. It never claims to be a person, never asks for an email address inside the conversation, and is never the only way to reach the studio. A question that tries to instruct it out of its role gets an ordinary answer or a refusal, never a change of behaviour and never a view of its configuration.
10. At most `40` questions per hour are answered per session and `200` per hour per address block; the question beyond either is refused with `That is a lot of questions. Try again shortly.` rendered in the panel, never as a browser error. A visitor without an account has a session too: the first answer sets an `assistant_session` cookie, and later questions carrying that cookie, or carrying a bearer token, count against that session.
11. Each answered question is kept as one assistant turn for `30` days for abuse handling only: it is never attached to an account, never mailed, and never becomes an analytics property. The conversation shown in the panel lasts only as long as the tab.

### Audio

1. The site has an ambient music bed of four generated tracks. `Toggle Audio` is the first control in the document on every route: a button whose text is `Toggle Audio` followed by a space and its current state, `Toggle Audio OFF` or `Toggle Audio ON`, and whose accessible name states the state it will move to.
2. Audio is **off** on first arrival, always, and off by default under a reduced-motion preference. The first press of `Toggle Audio` starts it.
3. The setting persists per browser and is restored on return; once signed in it is also kept on the account, so it follows the producer to another machine.
4. The ticker names the playing track as the title, two hyphens and the artist, for example `Slow Current--Halcyon Works`, and its previous and next controls change track. The two hyphens are literal, never a typographic dash.
5. Ducking: the bed drops to `0.3` of its level while the assistant is streaming an answer and restores afterwards on the signature curve.

### Consent, privacy and analytics

1. On every public route a consent surface reads `Our site uses essential cookies and, with your consent, analytics cookies. Details in` followed by the link `Privacy Notice.`, with two equal capsules, `Accept Cookies` and `Reject Cookies`. The sentence runs straight into the link and ends without its own full stop.
2. A first-time visitor is asked once; the answer survives a reload and the question is not asked again. There are exactly two categories, essential (always on) and analytics (off until accepted).
3. `Privacy Notice.` opens `/legal/privacy`, served from this origin in the site's own type. The privacy page states what the studio stores about a person: the account's email, display name and organisation; reels, their items and notes; pitches and their messages; enquiries; assistant questions and answers kept for thirty days and never attached to an account; and, only in the browser, the consent answer, the audio setting, the active reel and any changes held while offline. It also carries a `Cookie preferences` control that reopens the choice, because a dismissed consent surface is otherwise unreachable and consent is revocable; that re-entry point is the only way back to the question. The assistant panel's footer carries the same `Cookie preferences` control.
4. Analytics events are recorded by the app itself, never by a third party. Three events carry no identifier and may be recorded before consent: `loader_complete`, `motion_reduced` and `render_degraded`. Every other event is recorded only after `Accept Cookies`; a refusal is durable, and events that would have fired are dropped, never queued.
5. **Nothing a person typed is ever an analytics property.** A search is recorded by its length, a note by its length, a question by its length; never the text, never an email, display name, organisation, pitch summary, reel title or share address.

### Accounts

1. **Sign up** takes `email`, `display_name`, `organisation` and `password`, in that order. `email` must be a valid address and is **case-folded on write and unique regardless of case**: once `producer@example.com` exists, `Producer@Example.com` is refused as a conflict with `That email already has an account.` `display_name` is `1` to `60` characters, `organisation` is `1` to `120` characters, and `password` is at least `10` characters. Sign up creates an unverified `producer`, signs them in, sends the confirmation mail, and lands them on `/desk` with the unverified banner.
2. **Verification.** The confirmation mail carries a link to `/verify?token=<token>`. The token verifies the account once; a used or unknown token is refused with `That link has expired. Ask for a new one.` `Resend` on the unverified banner sends a fresh confirmation mail and invalidates the earlier link. An unverified producer may build reels but not submit a pitch.
3. **Sign in** takes `email` and `password`; the `/signin` form labels its fields `Email` and `Password` and submits with a `Sign in` button. The email is matched regardless of case. Every failure answers `That email and password do not match.`, never saying which half was wrong.
4. **After five failed sign-ins against one email inside fifteen minutes**, further attempts on that email are refused as too many, with the same message `That email and password do not match.` and without checking the password, for fifteen minutes from the fifth failure, even when the password is correct. The count belongs to the email regardless of how it was cased in each attempt.
5. **Reset** takes one `email` and always answers the same accepted response, `If that address has an account, a reset link is on its way.`, whether or not the address has an account. At most `3` reset requests per email per hour are accepted, and **only the first of them in that hour sends mail**. The mail carries a link to `/reset?token=<token>`; the token is single use, valid for `60` minutes, and **invalidated by use or by any successful sign-in to that account**. Completing a reset with a used, expired or invalidated token is refused with `That link has expired. Ask for a new one.`
6. **Sessions** last `30` days and are extended on use. `Sign out` ends the session on the server and its token stops working at once. **A role change ends every session of that account**: a token issued before the change is refused, and the account signs in again to act with its new role.
7. Signed in, a second capsule joins the chrome showing the account's initials and the active reel's item count as two digits, for example `PC_03` for `Priya Castell` with three items on the active reel and `JR_00` with none. Initials are the first letters of the first two words of the display name, upper case. Signed out the slot is empty and the chrome capsule does not move.
8. The account panel, opened from that capsule, lists the display name and organisation, `Your reels` with a count, `Your pitches` with a count, `Audio`, and `Sign out`.
9. `next` is honoured after sign in only when it is a path on this origin beginning with a single `/` and not `//`; anything else falls back to the role's home, `/desk` for a producer and `/studio` for an editor or admin.

### Granting a role

1. Only an admin changes a role, only from `/studio/people`, and never their own role: changing one's own role is refused with `You cannot change your own role.`
2. **The last remaining admin cannot be demoted**: the change is refused with `The last owner cannot be demoted.` and the role is unchanged. This holds when two admins try to demote each other at the same instant: exactly one change succeeds, one admin remains, and the other request is refused, either with that message or because its own session ended with the first change.

### Reels

1. A reel belongs to one producer, has a `title` of `1` to `120` characters, a `state` of `draft` or `submitted`, a `share_token` or none, an integer `version`, and at most `15` items. A producer holds at most `10` reels; the eleventh is refused with `You have ten reels. Rename or delete one.` A reel created by starring without a reel gets the title `Untitled reel`.
2. **Every write to a reel or its items carries the `version` it was made against, and every accepted write raises the reel's `version` by exactly one.** A write carrying any other version is refused as a conflict, changes nothing, and the refusal carries the reel's current `version` and its current state so the client can reconcile.
3. **Two writes carrying the same version that arrive at the same instant are never both accepted**: exactly one succeeds and raises the version by one, and the other is refused as a conflict carrying the new state.
4. Adding a project puts it at the end of the order. Only a published project can be added; a draft or missing project is not found. A project already on the reel is refused as a conflict with `That project is already on this reel.` A sixteenth item is refused with `A reel holds every project there is. Remove one to add another.`
5. Positions always run `1` to the item count with no gap: removing an item closes the gap and keeps the relative order of the rest.
6. Reordering sends every project on the reel exactly once, in the new order; anything else is rejected as invalid with `The order must list every project on this reel exactly once.` The change applies at once in the interface and the row settles into place.
7. A note is plain text of at most `500` characters (`A note holds up to five hundred characters.`), saved when focus leaves the field. A counter appears at `450` characters, and saving shows `Saved` for two seconds. Markup in a note is stored and shown as its characters, uninterpreted. A failed save keeps the text, shows `Not saved, we will retry.`, and retries twice before showing the failure band.
8. A reel item whose project was unpublished after it was added stays on the reel, reads as unavailable (`UNAVAILABLE`), and is excluded from any pitch.
9. The order and the notes are what the reel shows after a reload, on another tab and on another machine: the stored reel matches what the desk displayed.
10. **Share.** The owner may generate a share link, which sets a `share_token` minted by the server, and may revoke it, which clears it. Anyone signed in, in any role, holding the link reads the reel including its notes at `/shared/<token>`; a visitor who is not signed in is sent to sign in. A revoked or never-minted token answers exactly as a missing reel. A `submitted` reel keeps its share link working.
11. **Ownership.** A producer reading or writing another producer's reel, a reel that does not exist, and a reel id of the wrong shape all get the same not-found answer with the same body. Editors and admins read any reel but cannot write one.
12. **Delete.** A `draft` reel is deleted by confirming its exact title (`Type the reel title to delete it.` when it does not match); it disappears from the desk and is kept, recoverable, for `30` days. A reel with an open pitch is refused with `Withdraw the pitch before deleting this reel.`
13. A `submitted` reel is read-only: every item write, reorder, note and rename is refused as a conflict with `This reel has been sent. Withdraw the pitch to change it.`; sharing and revoking still work.
14. Removing an item applies at once and can be undone from the band for ten seconds. Nothing is deleted without either a typed confirmation or an undo, and nothing has both.

### Pitches

1. `Submit as pitch` on a draft reel opens the pitch form listing the reel's items, read-only there. A pitch takes `budget_band` (one of five), `timing` (one of four), `summary` (`20` to `2000` characters) and `contact_preference` (`email` or `call`), with the same messages as the enquiry form plus `Choose a budget band.` The five budget bands are `under-50k` (`Under 50k USD`), `50k-100k` (`50k to 100k USD`), `100k-250k` (`100k to 250k USD`), `250k-500k` (`250k to 500k USD`) and `500k-plus` (`500k USD and above`). The four timings are `this-month` (`This month`), `next-quarter` (`Next quarter`), `this-year` (`This year`) and `exploring` (`Just exploring`).
2. Only the reel's owner submits, only while the reel is `draft`, only with at least one available item (`Add a project before sending this reel.`), and only once the account is verified (`Confirm your email to send a pitch.`). A producer holds at most `5` open pitches (`submitted`, `acknowledged` or `in_conversation`); the sixth is refused with `You have five open pitches. We will get to them.`
3. A submitted pitch gets a reference `PT-` followed by six digits, continuing after the seeded `PT-000001`, and state `submitted`. The reel moves to `submitted` in the same step. The pitch lists the titles of the items it carries and, separately, the titles of any unavailable items it left out.
4. **A reel carries at most one open pitch. Two submissions of the same reel arriving at the same instant create exactly one pitch and exactly one set of mails**; the other is refused because the reel is no longer a draft.
5. The producer lands on `/desk/pitches/<id>` after submitting. A failed submission keeps the form filled, shows an error band above the submit control, and leaves the reel `draft`. A submission is never retried automatically.
6. A pitch state is one of `submitted`, `acknowledged`, `in_conversation`, `closed` and `withdrawn`. An editor or admin may move an open pitch to `acknowledged`, `in_conversation` or `closed`. The owner may only move their own open pitch to `withdrawn`; any other state they ask for is refused as forbidden. Changing a `closed` or `withdrawn` pitch is refused as invalid with `That change is not allowed for this pitch.`
7. **Withdrawing** moves the pitch to `withdrawn`, returns the reel to `draft` and makes it editable again, and mails the studio queue.
8. **Messages.** The owner, an editor or an admin may add a message of `1` to `2000` characters to a pitch that is not `closed` or `withdrawn` (`This pitch is closed to new messages.` otherwise). A message from an editor or admin on a `submitted` or `acknowledged` pitch moves it to `in_conversation` and mails the producer. A message from the producer never changes the state and sends no mail. At most `20` messages per pitch per hour are accepted; the next is refused with `That is a lot of messages. Try again shortly.`
9. `/studio/pitches` lists every pitch newest first with its reference, the producer's organisation and its state. A producer sees only their own pitches. The producer's pitch page and any studio member with the queue open see new messages and state changes within twenty seconds while the tab is visible, and stop checking while it is hidden.

### Mail

1. The app sends real mail over SMTP at `SMTP_HOST:SMTP_PORT` from `hello@example.com`. Every mail is plain text only, carries exactly one link, carries no image and no tracking of any kind, and ends with a line stating which address it went to and why, for example `This message went to producer@example.com because you submitted a pitch.`
2. Mail is sent after the change it reports is stored, never before, and a mail failure never fails the action. A failed send is retried three times over thirty minutes; if all three fail, the studio queue shows the pitch with `Notification not delivered`.
3. Subjects are exact, and each mail goes to one recipient with no cc and no bcc:

| Trigger | To | Subject |
|---|---|---|
| sign up | the new account's email | `Confirm your email` |
| accepted reset request, first in the hour | the address | `Reset your password` |
| pitch submitted | the producer's account email | `We have your pitch` followed by a space and the reference, for example `We have your pitch PT-000002` |
| pitch submitted | `studio@example.com` | `New pitch from` followed by a space, the organisation, a space and the reference, for example `New pitch from Farrow Kiln PT-000002` |
| editor or admin message moves or keeps a pitch in conversation | the producer's account email | `The studio replied` followed by a space and the reference |
| pitch withdrawn | `studio@example.com` | `Pitch withdrawn` followed by a space and the reference |
| enquiry accepted | the sender's email | `Your enquiry` followed by a space and the reference, for example `Your enquiry EN-000001` |
| enquiry accepted | `studio@example.com` | `Enquiry from` followed by a space, the sender's name, a space and the reference, for example `Enquiry from Ada Lin EN-000001` |

4. The confirmation link is `APP_PUBLIC_URL` followed by `/verify?token=<token>`; the reset link is `APP_PUBLIC_URL` followed by `/reset?token=<token>`; a pitch mail to the producer links to their pitch page, a mail to the studio queue links to `/studio/pitches`, and enquiry mails link to `/contact`. No mail is sent for anything else: no digest, no reminder, no marketing, and never for an assistant conversation.

### Empty, loading, error and offline states

1. Every list has an empty, a loading, an error and an offline state, each occupying the space the list would have, so nothing reflows when the first item arrives. The empty states read: `/work` filtered to nothing, `Nothing matches that.` with `Clear filters`; `/desk` with no reels, `No reels yet.`, `Star a project and it starts one.` and `Browse the work`; a reel with no items, `This one is empty.`, `Remove it, or star something.` and `Browse the work`; a producer with no pitches, `No pitches yet.` and `A reel becomes a pitch when you send it.`; `/studio/pitches` with none, `The queue is clear.` and `Nothing is waiting on the studio.`
2. The site has exactly two waiting signals: the loading field on a cold load and the assistant's three dots, reused inside any pending submit. List placeholders under the desk routes are row-shaped and never animated.
3. A list that fails to load shows `That did not load.`, a line naming what failed in ordinary words, and a `Try again` capsule that retries without a reload. A failed write shows a band directly above the control that failed, after the change has been rolled back.
4. **Offline.** When the connection drops a banner reads `You are offline. Changes are held.` Reel adds, removals, reorders and notes made while offline apply in place, are held, and their rows carry `Waiting to save`. When the connection returns the held changes are sent in order, the banner clears, and each row's caption clears as its change lands. A held change that fails is rolled back with the failure band, and the rest continue. Held changes survive closing the page and are sent on the next visit from the same browser. Pitch submission and assistant questions are never held: both controls are disabled offline with the reason under them.
5. One banner shows at a time, highest priority first: offline; running without the full scene; `You were signed out. Sign in to keep working.`; `Confirm your email to send a pitch.` with a `Resend` capsule; `The studio replied.` with a capsule to the pitch; then the consent question.

### Optimistic changes, reconciliation and rollback

1. What is optimistic: starring a project, removing an item, reordering, editing a note and renaming a reel apply in place before the server answers, with no pending styling, and are confirmed silently; only failure is visible. Submitting a pitch, replying on a pitch and asking the assistant are never optimistic: anything that sends mail or needs an answer from a service waits.
2. Reconciliation: when the server refuses a reel write as a conflict and returns the current reel, the client applies, in order: if the refused write was a reorder and nothing was added or removed since, it replays the reorder against the current order; if an item the write refers to no longer exists, it drops the write and removes the row; otherwise it takes the server's reel, discards the local change, and shows the failure band once, naming what was replaced.
3. Rollback restores the exact prior state, including scroll position and focus, and only then shows the failure band, so the band never sits above a screen still showing the change as though it worked.
4. Live updates between sessions: a pitch message or pitch state change reaches the producer on that pitch and any studio member with the queue open within twenty seconds while the tab is visible; a reel edited in another tab of the same account catches up on the next visibility change and on the next write's reconciliation; an unpublished project leaves the reel state on the next filter change or load. None of this is a live connection, and nothing pretends it is.

### Persistence

1. Reels, items, notes, pitches and messages belong to the account: they are the same after a reload, in a new tab, on another machine, and after signing out and back in.
2. Browser storage holds four things and no more: the active reel id, the offline queue, the consent answer and the audio setting. The session is therefore not kept in browser storage: a signed in person who reloads, opens a new tab or follows a link typed into the address bar is still signed in, so the web client's session travels in the cookie described in Technical requirements. The active reel defaults to the most recently updated reel on a new machine.
3. Signing out with held changes outstanding warns first, then discards them.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | The entry state: loading field, the studio mark, `SCROLL DOWN`, the intent list | Public |
| `/work` | The reel of published projects, filterable by address | Public |
| `/work/<slug>` | One project's state | Public |
| `/contact` | The enquiry form, the assistant, the studio address | Public |
| `/legal/privacy` | The privacy notice and `Cookie preferences` | Public |
| `/signin` | Sign in | Public, redirects when signed in |
| `/signup` | Sign up | Public, redirects when signed in |
| `/reset` | Ask for a reset link, or set a new password with `token` | Public |
| `/verify` | Confirm an email with `token` | Public |
| `/desk` | A producer's reels | `producer` |
| `/desk/reels/<id>` | One reel: rows, handles, notes, share, submit | `producer` owner; `editor` and `admin` read-only |
| `/desk/pitches/<id>` | One pitch and its messages | `producer` owner |
| `/shared/<token>` | A shared reel, read-only | Any signed-in role |
| `/studio` | The studio home | `editor`, `admin` |
| `/studio/pitches` | The pitch queue, newest first | `editor`, `admin` |
| `/studio/people` | Accounts and roles | `admin` |

**Entry and redirects.** A visitor who is not signed in and opens `/desk`, `/desk/reels/<id>`, `/desk/pitches/<id>`, `/shared/<token>`, `/studio`, `/studio/pitches` or `/studio/people` is sent to `/signin?next=` followed by that path. Signing in sends a producer to `/desk` and an editor or admin to `/studio`, or to `next` when it is a safe path. A signed in producer opening `/signin` or `/signup` is sent to `/desk`, an editor or admin to `/studio`; `/reset` always shows its form. A producer opening `/studio`, another producer's reel or a missing reel sees `That is not yours to open.` An editor or admin opening `/desk` is sent to `/studio`. Signing out ends the session and returns to `/`. When a session has expired, the next write sends the person to `/signin?next=` with the current path and keeps what they had typed; nothing is resubmitted automatically. Signed out in another tab, the account capsule disappears on the next state change and the stars fall back to their signed-out behaviour.

**Journeys.**

1. *Into the work.* Open `/`. The loading field resolves, then `What are you looking for?` and the five intent links appear. Press `ArrowDown`: the address becomes `/work` and fifteen project titles are listed. Open `Rally`: the environment turns warm, the metadata line reads `2014 / Nimbus / installation`. Press `Escape`: back on the reel.
2. *Star, order and annotate.* Sign in as `producer2@example.com`. The account capsule reads `JR_00`. On `/work` star `Archimedes`, `Glass Planes` and `Chromatik`: the capsule reads `JR_03`. Open `/desk`, open the reel: three rows in the order starred. Lift the third row with `Space` on its handle, move it up twice, drop it with `Space`: `Dropped at position 1 of 3` is announced and `Chromatik` is first. Type a note on the first row and move focus away: `Saved` shows, then clears. Reload: the order and the note are unchanged.
3. *Pitch.* On that reel press `Submit as pitch`. Submit without a budget band: `Choose a budget band.` shows and the address is unchanged. Complete the form and submit: the address is `/desk/pitches/<id>`, `We have your pitch` is in the producer's inbox, and the reel shows no drag handles.
4. *The studio answers.* Sign in as `editor@example.com`, open `/studio/pitches`: the pitch is listed first with `Farrow Kiln`. Reply. As `producer2@example.com` the pitch page shows the reply and reads `in conversation`.
5. *Shut out.* As `producer2@example.com`, open the seeded reel `Launch shortlist` by its id: `That is not yours to open.` Open `/studio`: the same words.
6. *No scene.* Open `/` on a machine with no render context: `Running without the full scene.`, `What are you looking for?` and all five intent links are readable and usable.

**States.** Every list has its empty, loading, error and offline state as written above. A cold load shows the loading field and no other waiting signal. An error never leaves the frame blank or the app unresponsive; the chrome and the environment stay through every failure.

## UI/UX notes

The north star is that the studio's work is felt before it is read: somebody arriving should sense a single lit environment that answers their input, and should still be able to read every word in it. The register is **consumer and editorial**: atmosphere is welcome, and the subject, the environment and the work inside it, is seen first and dominates everything. It is dark committed; there is no light mode.

**There is no page ground and no panel.** The ground is a rendered environment whose colour belongs to the current project, so the interface is almost entirely a near-white neutral at varying strength, which stays readable whether the environment behind it is warm, cool or nearly black. Interface over panels, light over boxes: controls composite additively onto the scene and take their light from what is behind them, and a build that gives the interface an opaque panel has broken the system. Where legibility fails, the fix is a slight blur behind the element, never an opaque ground.

**Palette by role.** Primary interface text and rules are a near-white neutral; secondary text and the metadata line are a light neutral; text over a bright region of the scene is a slightly softer near-white neutral. Exactly two saturated colours exist and both mean state, never decoration: a mid, vivid teal means live or active (a focused field's underline, the focus ring, the active item), and a near-white, soft blue is reserved for the loader counter alone. Hairline rules and control borders are the near-white neutral at a tenth of its strength, a resting secondary control at three tenths, placeholder text at half, resting body copy over a lit region at six tenths, and the hover state of a secondary control at seven tenths. The only darkening in the interface is a near-black neutral at a fifth of its strength, used behind an error message. There is no red anywhere, and none may be added: an error is shown by that darkening plus the words. Every anchor declares its colour, so a stylesheet failure leaves near-white writing on the scene, never a default link blue. Each environment's clear colour is a near-black carrying its hue in a single channel: the entry environment is a near-black, muted blue, and the two other environments are near-black neutrals leaning green and red. The exact values are yours, so long as those roles and exclusions hold.

**Type.** One monospaced grotesque family in three cuts, Regular, Bold and Light, chosen from an open family that is named, licensed and metric compatible, with a stated fallback stack. The scale is exact: `16px` weight `400` at normal line height for most interface text; `16px` weight `400` on a `30px` line for the intent list, nearly double leading so five short links read as a considered list; `14px` weight `400` on a `21px` line for the project description, and at normal line height for single-line body; `14px` weight `700` at normal line height for a project title, and on a `21px` line when it wraps to two; `13px` weight `400` on a `19.5px` line for the metadata line, and at normal line height when it is one line; `12px` weight `400` on an `18px` line for consent copy and footnotes; `10px` weight `400` on a `30px` line for the ticker; and `13.3333px` weight `400` at normal line height for form controls. Everything renders uppercase: stored copy is kept in sentence case and cased at render.

**Shape, radius and density.** Two families of corner radius: full capsules for anything that takes an action (the chrome capsule, consent actions, the assistant input, submit controls), and small softened corners for anything that carries content (the assistant panel, message bubbles, the typing dots, the ticker arrows). The assistant panel squares its two bottom corners when docked to the bottom edge. Density is **spacious**: almost the whole frame is environment, and all copy sits in the lower left eighth of it on project, reel, contact and every extension state.

**Depth.** From back to front: the rendered environment, elements composited into the scene, the interface (chrome, project copy, ticker), the assistant panel, then the consent surface, and topmost the audio toggle and any blocking notice.

**Motion character is `eased`, and one curve owns it.** Nearly every state change uses the studio's signature curve, which puts almost all of the motion at the very start and lets it settle for a long time, so a change feels like something heavy arriving under its own weight rather than something switched on. Entering a project takes the long version of the same change. The loading field holds at full strength while assets arrive, waits through a long deliberate pause once the count completes, and only then fades slowly; cutting the pause removes the effect. The assistant panel fades in on a gentle sine ease, controls fade on a plain ease out, the ticker crawls linearly and endlessly, the typing indicator's three dots pulse in turn, and a dropped reel row settles into place on the signature curve. Transitions are named per property, never applied to everything at once.

**Reduced motion and vestibular safety.** A full-viewport environment that moves continuously and changes state under scroll is exactly the case the preference exists for, so it is not optional here. Under a reduced-motion preference the environment holds one rendered frame per state and every state change becomes a cut, the loading sequence becomes a text counter and a rule with no resolving field and no pause, the per-project retint happens instantly on entry, the panel fade becomes short, the ticker shows its first item still, the three dots become a static three-dot glyph, and audio stays off by default. Everything still happens; nothing glides.

**Accessibility floors.** Text meets WCAG AA contrast against the environment behind it, and the copy region in the lower-left eighth has a luminance ceiling: it never grows brighter than the light neutral used for metadata, in any project tint and at any camera position. The build enforces this rather than trusting the eye: it samples the lower-left eighth of the rendered frame per state and per project and fails when the peak luminance exceeds the ceiling. Every interactive element shows a visible focus ring in the live teal, offset from the element, and focus is never the hover state. Full keyboard navigation reaches every control, including reordering a reel with `Space`, arrow keys and `Space`. Icon-only controls carry labels, touch targets are comfortably sized through padding rather than a larger visible capsule, and meaning is never carried by colour alone.

**Responsive.** The frame fills the viewport at every width and never scrolls sideways. The reference declares no breakpoint of its own; this product adds three, and the responsive matrix follows. Three tiers: a narrow phone, a tablet, and a wide desktop. At desktop width the chrome capsule sits top right, the ticker and audio toggle top left, the intent list lower left, the copy block in the lower left eighth and the assistant panel floats. At tablet width and below the capsule moves to top centre, the intent list centres, and the assistant docks to the bottom edge. On a phone the ticker and its controls are hidden, the audio toggle moves into the account panel, the copy block spans the full width of the lower third above the assistant, a long project description truncates after four lines with a control to expand it, and hover treatments are not applied. A short landscape viewport collapses the assistant to its resting input and opens it as a full-height panel.

**The default-blue finding.** The reference's second most common colour was the browser's default link blue on hundreds of invisible hit areas nobody styled; it is not a brand colour and never appears here. **What it must not look like:** a page of grey boxes sitting on a picture, text coloured per project, a second loading spinner, a floating toast sliding in from a corner, a red error, a dropdown, or a blank black screen while the scene loads.

## Front-end specification

**The chrome.** Above the scene sit exactly four things: the chrome capsule, the audio toggle, the ticker, and whichever of the consent surface or the assistant is open. The chrome capsule contains `WORK`, a short horizontal rule, and `CONTACT`, in interface type, near-white, with a hairline border and no ground. The rule between the two labels is a hairline at the tenth-strength near-white, spans part of the capsule's inner width, and never animates. The capsule carries a soft outer glow whose colour comes from the environment behind it, warm in a warm project and cool in a cool one; that glow is the scene bleeding through an additively composited edge, and a fixed shadow looks wrong on every project but one. `WORK` enters `reel`; `CONTACT` enters `contact`.

**The ticker.** Two items crawl continuously over a short travel as a linear, infinite animation, each reading the track title, two hyphens and the artist, the measured template being `Song--Artist`. The ticker sits at low opacity and brightens whatever is behind it, so it vanishes over black; it never sits over a dark region. Its previous and next controls rest at low strength and fade up when pointed at; they are drawn as double chevrons and labelled `Previous track` and `Next track`. The ticker is hidden from assistive technology.

**The interface fade.** The scene publishes one value back to the interface as the visitor moves in: it climbs continuously with input and is clamped at nine tenths, and it drives the interface's strength, so the chrome fades up as the visitor enters the experience and never reaches full strength.

**The loading field.** A block of monospaced characters thirty columns wide and thirteen rows deep, initially all forward slashes, sits in a circle with a hard edge. As assets arrive, individual cells are replaced by digits, so the field resolves out of static. The field sits at partial opacity. A counter at its centre, in the soft blue, reads a forward slash followed by the number of assets loaded (for example `/30`, then `/75`), counting up and showing no total, replacing the character behind it. After the count completes the same element reads `>>>`, then the pause and the fade follow. The field is thirty columns at every width; on a phone it scales rather than rewrapping.

**The intent list.** `What are you looking for?` above the five links, lower left at desktop width and centred below it.

**The reel row.** Title in the bold project-title size, the metadata line under it in the light neutral, and a hairline rule under the row. On the desk a row adds a drag handle at its left (the double chevron turned upright, a real control with a role and a label), the note field at its right and the remove control at its far right; there is no new component and no new corner shape. A lifted row announces `Lifted, position 2 of 3`, each move announces its position, `Space` drops it announcing `Dropped at position 1 of 3`, and `Escape` cancels and returns it. On a phone a row can also be lifted with a long press, and each row carries up and down controls that do the same as the arrow keys.

**The project view layout.** `SCROLL TO CLOSE` near the top centre; title, metadata, description, `PROJECT LINK` and `<- CLOSE` stacked in the lower left eighth; the assistant input below everything; the chrome capsule top right. All copy occupies the lower left eighth at desktop width; the rest is environment.

**The assistant panel.** The resting input is a full capsule with a hairline border, a half-strength placeholder and no ground. The open panel has small softened corners, adds its light to the scene with a slight backdrop blur, and fades in. The message list is fully opaque over its lower three quarters and fades out over its top tenth, so older messages dissolve into the scene. Bubbles have small softened corners. The typing indicator is the `dot-flashing` animation: three dots in a row, each pulsing between three-tenths strength and full strength, a third of a cycle apart, linear and infinite.

**The consent surface, the account panel and the assistant panel are one panel component** with three contents: the same corner pair, the same additive compositing and blur, the same stacking behaviour and the same fade in. The consent surface is part of the system, not a solid box.

**Forms.** Fields are lines, not boxes: a label in the metadata size and the light neutral above, the input in body type, a hairline under the input that turns the live teal on focus, a half-strength placeholder, a helper line in the metadata size, and an error line in near-white on the fifth-strength darkening band. The submit control is the chrome capsule. Validate when focus leaves a field, never on a keystroke; re-validate on submit; a field that has failed re-validates on each keystroke until it passes. The submit control is disabled only until the form has been valid once; after that a failed submit shows the errors. While a submit is pending the capsule keeps its label, its text drops to half strength, and the three dots appear inside it; the form does not move. Success in place replaces the form with a title line and a capsule onward; success with a state change carries a banner on the destination for one state change; failure puts an error band above the submit, moves focus to it and announces it.

**In-app messages.** Exactly three surfaces: a banner under the chrome at full width, in interface type, composited into the scene, until its condition clears; an inline confirmation under the control that caused it, in the metadata size, for two seconds; an action band above a control that failed, in the metadata size on the darkening band, until dismissed or retried. The banner never moves the chrome.

**The marks.** Every mark is drawn inline as a single stroked path taking the current text colour, on one square drawing area, with one stroke weight matching bold project-title text, butt terminals and open two-stroke arrowheads: a left arrow (`<- Close` and the ticker's previous control), a right arrow (the ticker's next control), a double chevron (the ticker controls and, turned upright, the drag handle), a close cross (the consent surface and the assistant), a globe (the locale control), a five-point star (the reel control), and a filled dot (the typing indicator). No bitmap and no vector file is fetched for any of them. Three social marks sit on `/contact`.

**The studio mark.** A lit three-dimensional object at the centre of the entry state: a rounded lower-case letterform inside a ring, on a looping stem whose two arms leave the ring low on either side, cross below the ring and continue downward. Its surface is spectral: cyan, magenta and amber travel across one continuous polished form as it turns, the way light moves over a thin film of oil on water. A flat coloured version of it is wrong.

**The rendered scene.** One full-viewport rendered surface, with no second surface anywhere, carrying a continuously animated three-dimensional environment with a bloom pass, physically based shading and a colour lookup pass. In `loading` it is a near-black neutral with the resolving field only; in `entry` and `reel` it is the near-black, muted blue with the mark lit from above and behind and particles drifting, the camera withdrawn in `reel`; in `project` it is retinted by light and fog to the project's tint. Lighting is a single key from the upper left at a shallow angle making a visible vignette, a rim from behind the mark, and a broad fill from the reflection set; the gradient across the frame is fog and moves with the camera. Particles are small discs of varying size in the project's tint and its complement, drifting slowly upward and toward the camera, denser in the lower half and absent from the upper third, a few hundred at desktop width and half as many on a phone, placed from the project's `scene_seed` so a project's field is identical on every machine. Composition order, back to front: the environment's clear colour, scene geometry and the mark, the particle field, the bloom pass then the colour lookup pass, elements composited into the scene, the interface, the assistant, then consent and the audio toggle.

**Degradation.** Under reduced motion, one frame per state, held. With no render context, the clear colour, the unchanged interface and the banner described in Core features. When the frame rate stays below its floor, the bloom pass is dropped first, the particle field second, the colour lookup pass third and the reflection resolution fourth, one step at a time, each step recorded as a `render_degraded` event. On a phone the environment renders at half resolution and is upscaled.

**Zero-asset substitution guide.** No binary asset ships; every class has a generated substitute.

| Asset | Generated as |
|---|---|
| base colour | a flat mid value; all character comes from the reflection set |
| normal map | value noise at three octaves converted to a normal by finite difference |
| metal, roughness, occlusion | fully metallic, roughness from the same noise remapped into a low glossy band, no occlusion |
| diffuse reflection | the reflection environment below, blurred to a low order |
| specular reflection | the same recipe at full resolution |
| colour lookup | identity, plus a slight lift of the blue channel in the shadows and a roll-off of the brightest red, which produces the near-black navy without tinting the whole frame |
| reflection environment | a square canvas: a vertical gradient from the light neutral at the top to the state's clear colour at the bottom; a key highlight in the upper right falling off to transparent; a faint horizon band just below the middle, blurred; three small hot speculars; and for a project environment the whole multiplied by the project's tint with the key rotated to its key light |
| the mark | a torus ring, an extruded rounded letterform inside it, a swept tube stem, with the thin-film spectral term over a polished conductor |
| particles | billboarded discs placed from `scene_seed` |
| the typeface | the chosen open monospaced grotesque, loaded as a font the product names and licenses, and the in-scene glyph atlas generated at build time from every glyph in every shipped string |
| the ambient bed | generated through the browser's audio graph: two detuned oscillators a fifth apart through a low-pass filter at `400Hz`, the cutoff slowly modulated at `0.03Hz`, and a noise layer at `0.04` gain through a band-pass; four tracks differing by root note and modulation rate |
| interface sound | none |
| the showreel video | not reproduced; a project's media is its generated environment |

**Internationalisation and formatting.** Type drawn inside the scene comes from an atlas generated at build time from the union of every glyph in every shipped locale, and **the build fails when any shipped string contains a glyph the atlas does not carry**, because a missing glyph renders as nothing. One locale ships, `en`, the only member of the locale enum at launch; any other locale requires an atlas rebuild and a review at all three widths. Locale is chosen from the account's `locale`, then the `lang` cookie, then the browser's accepted languages matched against the shipped set, then `en`, and never from an address or a location. Dates read `12 March 2023`, numbers `1,000`, budget bands as written above, and currency is never converted. Project titles, client names and track titles are never translated; the five intent labels are. Text runs left to right only.

**Module architecture.** Five layers, and a dependency only points downward: states (one module per scene state), interface, the state store (the reel store, the session, the query model, the state machine), scene (environment, mark, particles, passes), and platform (the input driver, the transport, the audio graph, the atlas). The scene knows nothing about projects: it is handed a tint, a key light and a `scene_seed` and renders. The interface never reaches into the scene; the one channel between them is the normalised state position and the interface fade value, in that direction only. One input driver exists for the document; components subscribe to it and never attach their own wheel listener; the desk routes create none. The desk routes are ordinary scrolling documents against a still frame of the environment, because a list somebody drags rows around in must scroll natively. The component set is seventeen and no more: Capsule, Chrome, Ticker, AudioToggle, Mark, CopyBlock, MetaLine, IntentList, ReelRow, Loader, Panel, Field, Banner, ActionBand, StateBlock, SortableList and Dots. The stores are: session (account, role, locale, filled from `/api/me`), reels (the active reel, its items, its version, mirrored to browser storage only for the offline queue), query (the address, never duplicated in memory), scene (state position, degradation stage, reduced-motion preference) and audio (on or off and the current track, mirrored to browser storage).

**Announcements.** A state change is assertive and names the state; a banner appearing is polite; a note saving is polite; a failed action is assertive and takes focus; the assistant beginning to answer is polite, `Answering`, and finishing is polite followed by the answer text; lifting, moving or dropping a row is assertive; the loader completing is polite, `Loaded`.

**Copy deck.** Stored in sentence case and cased at render except where capitals are literal content: `SCROLL DOWN`, `SCROLL TO CLOSE`, `WORK`, `CONTACT`, `Toggle Audio` with `ON` or `OFF`, `Project Link`, `<- Close`, `ASK ME ANYTHING...`, `>>>`, `Submit as pitch`, `Saved`, `Not saved, we will retry.`, `Resend`, `Try again`, `Clear filters`, `Browse the work`, `We cannot find that.`, `That is not yours to open.`, `Running without the full scene.`, and the consent, empty-state, validation and limit copy written in Core features. The fourteen measured project titles are `Archimedes`, `Million Tile Mission`, `Renewable Frontiers`, `Glass Planes`, `E.D.E.N.`, `Harmonic Drift`, `Rally`, `Andes 20`, `Chromatik`, `20 Years of Nexus`, `Frontier Beyond`, `Welcome to Stonehall`, `Discover your Familiar` and `Secret Tide`.

## Technical requirements

The frontend is **Svelte** built with **Vite**, served as a production build, and the in-scene rendering uses **three**. The backend is **FastAPI** on Python, run under **Uvicorn**, with **SQLAlchemy** over **psycopg** for PostgreSQL and **argon2-cffi** for password hashing; mail uses the Python standard library's SMTP client. The chosen open typeface may be installed from its own package and served from this origin. The rendering model is a **single page application over a JSON API**: the browser receives an application shell on first paint and every state after that is painted from JSON the API returns, except that the HTML the server returns for each public address already carries that address's head tags, described below. Persistent state lives in **PostgreSQL** (`postgres`), reached through `DATABASE_URL`. Mail goes to **Mailpit** (`mailpit`) over SMTP at `SMTP_HOST` and `SMTP_PORT`, with `SMTP_USER` and `SMTP_PASS`. The app reads its own address from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`; never hardcode a host or a port. `GET /api/health` returns `200` once the app is ready. Authentication is email and password implemented by the app itself, issuing a bearer token sent as `Authorization: Bearer <access_token>`; there is no external identity provider. Where the web client also keeps a session cookie, that cookie is HttpOnly and SameSite Lax, is Secure whenever `APP_PUBLIC_URL` begins with `https` (a browser drops a Secure cookie on a plain `http` address, so a session on one must still survive a reload), is rotated on sign in and on any role change, and every state-changing request made with it carries a request token, a mismatch being refused as forbidden with no detail. The app logs one line per request with the method, the path and the status, and never logs a password, a token, a note, a summary or a question.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor: the only backing services available in this environment are PostgreSQL (`postgres`) and Mailpit (`mailpit`), and reaching for anything else is a contract violation. Both are **already running** and reachable at the variables above. Do not download, install, compile or start a copy of either.

**Head tags on every public address.** For `/`, `/work`, `/work/<slug>` of every published project, `/contact`, `/legal/privacy`, `/signin`, `/signup` and `/reset`, the HTML document the server returns, before any script runs, carries a `<title>`, a `<meta name="description">` whose content is non-empty, an `og:title` and an `og:image`. No two of those addresses share a title or a description. The titles are exactly: `Halcyon Works` for `/`, `Work | Halcyon Works` for `/work`, the project title followed by ` | Halcyon Works` for a project (for example `Rally | Halcyon Works`), `Contact | Halcyon Works`, `Privacy Notice | Halcyon Works`, `Sign in | Halcyon Works`, `Sign up | Halcyon Works` and `Reset password | Halcyon Works`. `og:title` equals the title. `og:image` is an absolute address on `APP_PUBLIC_URL` whose preview image the server generates on request (no shipped file) and returns with a `200` and an `image/png` or `image/svg+xml` content type. `/work` with query parameters carries the same head as `/work`.

**Not found at the document level.** Any address the product does not serve, `/work/<slug>` for a slug that is not a published project, and `/shared/<token>` for a token that is not current, return the application shell with a not-found status, and the shell renders the not-found page. The API under `/api` answers unknown paths as not found in JSON. No analytics endpoint and no internal state route is ever served as a page.

**Errors.** Every error from `/api` has one shape: `{"error": {"code", "message", "field", "version", "current"}}`. `message` is the exact copy the surface shows, `field` names the failing field or is null, `version` carries the reel's current version on a reel conflict and is null otherwise, and `current` carries the current reel on a reel conflict and is null otherwise. The codes and their statuses are: `unauthenticated` `401`; `forbidden` `403`; `not_found` `404`; `validation` `400`; `conflict` `409` on reels and their items, `422` on pitches and messages; `limit` `409` on reels and items, `422` on pitches; `rate_limited` `429`, with the wait stated in words in `message`; `assistant_unavailable` `503`; `server` `500`. `404` is answered rather than `403` for any object the caller may not know exists; `403` is used only where the caller already knows it exists, such as an editor writing a reel it can read, or a producer asking for a pitch state other than `withdrawn` on their own pitch. An id of the wrong shape is `404`, never a parse error. Every business-rule violation is rejected as a client error with a reason, never as a server error and never as a silent success. A failed operation leaves no partial state.

**Reel versions under simultaneous requests.** Each reel carries an integer `version`, starting at `1`, raised by exactly one on every accepted write to the reel or its items. A write made against a version that is not the current one is refused with `409` and code `conflict`, carries the current `version` and `current` reel, and changes nothing. When two writes carrying the same version reach the same reel at the same instant, **exactly one** is accepted; the other is refused with `409` exactly as a stale write is, and the reel's version rises by one, not two. The same holds for adds of different projects, for a reorder racing a note, and for any other pair of reel writes. A reel never holds the same project twice and never holds two items at one position. Choose any mechanism.

**Pitches, roles and sign in under simultaneous requests.** When two submissions of one draft reel arrive at the same instant, **exactly one** pitch is created and one pair of pitch mails is sent; the other is refused with `422` and code `conflict` and **must not create a second** pitch or a second mail. When two admins each ask to demote the other at the same instant, exactly one change is accepted, and the other is refused, with `The last owner cannot be demoted.` or as unauthenticated because its session ended with the accepted change; the product never has zero admins. The sign-in failure count for one email is exact however the attempts interleave.

**Rate limits.** Every limit answers `429` with code `rate_limited` and the wait in words, and the surface renders it verbatim:

| Action | Limit | Message |
|---|---|---|
| sign in, per email regardless of case | `5` failures per `15` minutes, then refused for `15` minutes | `That email and password do not match.` |
| sign in, per address block | `50` attempts per `15` minutes | `Too many sign-in attempts from here. Try again in fifteen minutes.` |
| reset, per email | `3` accepted per hour, only the first sends mail | none: every request answers `202` with the reset message |
| sign up, per address block | `10` accepted sign-ups per hour | `Too many new accounts from here. Try again in an hour.` |
| assistant, per session | `40` per hour | `That is a lot of questions. Try again shortly.` |
| assistant, per address block | `200` per hour | `That is a lot of questions. Try again shortly.` |
| pitch messages, per pitch | `20` per hour | `That is a lot of messages. Try again shortly.` |
| enquiries, per address block | `5` per hour | `That is a lot of enquiries. Try again in an hour.` |
| any read of the API (a `GET` under `/api`), per address block | `600` per minute | `Too many requests from here. Try again in a minute.` |

An address block is the request's source address; a request that arrives without a session still has one.

**Authorisation, per write, and input handling.** Every write asks, on the server and in order, whether there is a session, whether the role permits it and whether this account owns the object, and never infers any of it from a control having rendered. Every string is length-checked on the server; a surface limit is a convenience, never the enforcement. Notes, summaries, messages and enquiries are stored and rendered as plain text; no markup is interpreted anywhere. A project link is accepted only as `http` or `https` with a host (anything else is rejected with `A project link starts with http or https and names a host.`), is stored as given, and is rendered as a link with no fetch, no preview and no icon request, so a stored link never makes the site call a stranger's server.

**Analytics events.** `POST /api/events` takes `name`, `properties` and `consent` (`accepted`, `rejected` or `unanswered`). An unknown event name is rejected with `That is not an event this site records.`, and a property outside the event's own list below is rejected with `That event does not carry that property.`; in both cases nothing is stored. A known event with only its own properties is answered `202` with `{"stored": true}` when it is stored and `{"stored": false}` when it is dropped. It is stored only when its name is `loader_complete`, `motion_reduced` or `render_degraded`, or when `consent` is `accepted`. The events and their only properties are: `state_enter` (`state`, `slug`, `role`); `intent_select` (`category`); `project_open` (`slug`, `source`); `filter_apply` (`parameters`, the sorted list of parameter names); `search_submit` (`length`); `reel_add` and `reel_remove` (`slug`, `reel_size_after`); `reel_reorder` (`item_count`, `moved_distance`); `note_save` (`length`); `pitch_submit` (`item_count`, `budget_band`, `timing`); `pitch_reply` (`author_role`); `assistant_open` (`state`, `slug`); `assistant_ask` (`length`, `project_slug`); `assistant_fail` (`reason`); `audio_toggle` (`to`); `track_change` (`direction`); `loader_complete` (`duration`, `asset_count`); `motion_reduced` (`reduced`); `render_degraded` (`stage`). The client reports the environment's frame rate as a rolling median once per state, the loading duration and asset count once per session, the degradation steps taken once per session, and the assistant's time to first answer per question with no content.

**Streaming.** `POST /api/assistant` is the one streaming response: it answers `200` with a `text/plain` body written progressively. A stream that ends without any answer text is `assistant_unavailable`, never an empty answer.

**Performance.** What is deferred and what is preloaded are both stated below. On a processor running at a quarter of its speed and a `1.6Mbps` connection: the loading field is readable within `0.6s` in at most `250KB` transferred; the entry state is complete and interactive within `4s` in at most `3MB`; `reel` is instant from `entry` and `project` instant from `reel`, at most `400KB` per project; the desk routes show text within `0.8s` and are interactive within `1.5s` in at most `500KB`. The environment holds `60` frames per second at desktop width and `30` on a phone as a rolling median over `5s`; below the floor for `3s` the degradation ladder takes one step and reports it. The reflection set and the colour lookup pass wait for the loading field to be on screen, the particle field waits for the mark, a project's environment loads only when the project is entered or its row is next to the pointer, the audio bed waits for `Toggle Audio`, the assistant's code waits for its input to take focus, and the desk code waits for a session. Nothing about any project's environment loads while the visitor is on the entry state. The glyph atlas, the loading field's code and the first three projects' `scene_seed` values are preloaded. No image, video, texture, geometry, font or audio file is fetched at runtime except the named typeface.

## Data model

Twelve tables are pinned below, one per entity, with the relationships between them stated per table; the app may add its own tables for sessions, tokens, sign-in attempts and held deliveries. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

### `accounts`

`id` (opaque, server-issued, never rendered), `email` (unique, stored case-folded), `password_hash`, `display_name`, `organisation`, `role` (`producer`, `editor` or `admin`), `locale` (`en`), `audio_enabled` (boolean), `verified_at` (null until verified), `created_at`, `last_seen_at`. A password is never stored in readable form. Deleting an account anonymises it: its pitches stay with the organisation and no personal field.

### `categories`

`id`, `slug`, `intent_label`, `position`. Seeded: `games` `-> games` 1; `multiplayer` `-> multiplayer` 2; `xr` `-> XR / VR / AI` 3; `installation` `-> installations` 4; `web` `-> websites` 5.

### `projects` and `project_categories`

`projects`: `id`, `slug` (unique), `title`, `client_name`, `client_slug` (derived from `client_name` by the rule in Core features), `year`, `description`, `project_link`, `state` (`draft` or `published`), `tint`, `key_light`, `scene_seed`, `position`, `metadata_verified`, `created_at`, `updated_at`. `project_categories`: `project_id`, `category_id`, unique on the pair, one to three categories per project. `category_slugs` in any response lists a project's categories in category `position` order. A project summary carries `id`, `slug`, `title`, `client_name`, `year`, `category_slugs`, `description`, `project_link`, `tint`, `key_light` and `scene_seed`, and carries `state` only for an editor or admin. `tint` and `key_light` are the only per-project visual fields; no project carries a layout of its own. A project that any reel item refers to is never deleted; it is unpublished instead. An unset `tint` reads as `entry-navy` and an unset `scene_seed` is derived from the slug.

Seeded projects, `position` in the studio's own order. Rows 5 and 7 carry measured metadata (`metadata_verified` true); every other row is unverified placeholder content (`metadata_verified` false). Every `project_link` is `https://example.com/work/` followed by the slug.

| position | slug | title | year | client_name | categories | state | tint | key_light | scene_seed | description |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `archimedes` | `Archimedes` | 2019 | `Société Parallèle` | `web` | published | `pale-gold` | `upper-left` | `4101` | `A browser game that turns classical geometry puzzles into levers you can pull` |
| 2 | `million-tile-mission` | `Million Tile Mission` | 2020 | `Nimbus` | `multiplayer`, `web` | published | `sea-glass` | `above` | `4102` | `A shared mosaic built by thousands of players placing one tile at a time` |
| 3 | `renewable-frontiers` | `Renewable Frontiers` | 2022 | `Verdant Coöperative` | `web` | published | `moss-green` | `upper-left` | `4103` | `An interactive map of energy projects told through flights over their sites` |
| 4 | `glass-planes` | `Glass Planes` | 2018 | `Papier Mâché Press` | `installation` | published | `ice-blue` | `above` | `4104` | `A paper-craft installation where folded planes react to the people walking past` |
| 5 | `eden` | `E.D.E.N.` | 2021 | `U.S. Skyforce` | `xr` | published | `cool-steel` | `upper-right` | `4105` | `A cinematic real-time experience offering guided levels to test and enhance cognitive skills` |
| 6 | `harmonic-drift` | `Harmonic Drift` | 2023 | `Añejo Records` | `xr`, `installation` | published | `deep-violet` | `behind` | `4106` | `An audio-reactive headset piece where the room reshapes around the music` |
| 7 | `rally` | `Rally` | 2014 | `Nimbus` | `installation` | published | `warm-amber` | `upper-right` | `4107` | `A multi-device racing experience that syncs in real-time. Developed for the client's developer conference` |
| 8 | `andes-20` | `Andes 20` | 2020 | `República Andina` | `xr`, `installation` | published | `dusk-rose` | `upper-left` | `4108` | `A national pavilion that carries visitors along a mountain ridge in real time` |
| 9 | `chromatik` | `Chromatik` | 2019 | `Atelier Kolorowy` | `games`, `web` | published | `ember-red` | `above` | `4109` | `An artist archive where every painting opens into the room it was made in` |
| 10 | `20-years-of-nexus` | `20 Years of Nexus` | 2021 | `Nexus` | `games`, `web` | published | `night-teal` | `behind` | `4110` | `A playable timeline celebrating two decades of a console platform` |
| 11 | `frontier-beyond` | `Frontier Beyond` | 2023 | `U.S. Skyforce` | `games`, `xr` | published | `slate` | `upper-right` | `4111` | `An exploration piece that sends a crew past the edge of the known map` |
| 12 | `welcome-to-stonehall` | `Welcome to Stonehall` | 2022 | `Stonehall Studios` | `games`, `multiplayer` | published | `copper` | `upper-left` | `4112` | `A welcome experience that lets new fans walk the halls of a fictional school` |
| 13 | `discover-your-familiar` | `Discover your Familiar` | 2021 | `Stonehall Studios` | `games`, `web` | published | `aurora` | `above` | `4113` | `A quiz that pairs every visitor with the creature that suits them` |
| 14 | `secret-tide` | `Secret Tide` | 2024 | `Tidewater Fêtes` | `multiplayer`, `installation` | published | `sand` | `behind` | `4114` | `A festival companion that guides crowds between stages at the frontier of the shore` |
| 15 | `tidal-cartography` | `Tidal Cartography` | 2024 | `Halcyon Works` | `web` | published | `graphite` | `upper-right` | `4115` | `A shared chart of the coastline that visitors redraw together` |
| 16 | `lantern-protocol` | `Lantern Protocol` | 2025 | `Halcyon Works` | `xr` | draft | `lantern-orange` | `above` | `4116` | `A work in progress that lights a city block from a single phone` |

With the default sort a visitor's `/api/projects` returns fifteen projects with `total` `15`, in this order: `Secret Tide`, `Tidal Cartography`, `Harmonic Drift`, `Frontier Beyond`, `Renewable Frontiers`, `Welcome to Stonehall`, `E.D.E.N.`, `20 Years of Nexus`, `Discover your Familiar`, `Million Tile Mission`, `Andes 20`, `Archimedes`, `Chromatik`, `Glass Planes`, `Rally`. `sort=oldest` returns exactly that list reversed. An editor or admin also receives `Lantern Protocol`, first, with `state` `draft`, and `total` `16`.

### `reels` and `reel_items`

`reels`: `id`, `owner_id` (an `accounts` row), `title`, `state` (`draft` or `submitted`), `share_token` (null or a server-minted token, unique), `version` (integer, starting at `1`), `created_at`, `updated_at`, `deleted_at`. `reel_items`: `reel_id`, `project_id`, `position`, `note` (at most `500` characters, empty by default), `added_at`; unique on `reel_id` and `project_id`, and `position` unique within a reel. A reel holds at most `15` items and an account at most `10` reels that are not deleted. `item_count` is derived on read. An item's `available` is derived on read from its project being published.

### `pitches` and `pitch_messages`

`pitches`: `id`, `reference` (unique, `PT-` and six digits), `reel_id`, `owner_id`, `budget_band`, `timing`, `summary`, `contact_preference`, `state`, `submitted_at`, `notification_failed` (boolean). A reel has at most one pitch whose state is `submitted`, `acknowledged` or `in_conversation`. `pitch_messages`: `id`, `pitch_id`, `author_id`, `body`, `created_at`.

### `tracks`

`id`, `title`, `artist`, `source`, `position`. Seeded, in position order: `Slow Current`, `Glass Harbour`, `Night Relay`, `Amber Field`, each by artist `Halcyon Works`, each with `source` `generated:` followed by its title in lower-case kebab form, for example `generated:slow-current`.

### `assistant_turns`, `enquiries` and `analytics_events`

`assistant_turns`: `id`, `session_ref`, `project_id` (null when asked outside a project), `question`, `answer`, `created_at`; kept `30` days; it has no account reference of any kind. `enquiries`: `id`, `reference` (unique, `EN-` and six digits), `name`, `email`, `timing`, `summary`, `contact_preference`, `created_at`. `analytics_events`: `id`, `name`, `properties` (a JSON object carrying only the event's own properties), `created_at`.

### Seed data

The four accounts in User roles, with the display names, organisations and roles written there, all verified, all with `audio_enabled` false. The categories, projects and tracks above. One reel, `Launch shortlist`, owned by `producer@example.com`, state `submitted`, `version` `1`, no share link, with three items: `rally` at position 1 with the note `The sync across devices is the part to show`, `eden` at position 2 and `glass-planes` at position 3, both with empty notes. One pitch on it, reference `PT-000001`, owned by `producer@example.com`, `budget_band` `100k-250k`, `timing` `next-quarter`, `contact_preference` `email`, summary `We want a launch piece that feels like Rally but lives in a headset`, state `in_conversation`, with one message from `editor@example.com`: `Thanks, this is a good fit. We will set up a call.` `producer2@example.com` owns no reel and no pitch. No enquiry, assistant turn or analytics event is seeded. The next pitch reference is `PT-000002` and the next enquiry reference is `EN-000001`.

When migrating an existing store forward: `reel_items.position` is assigned in `added_at` order, every existing reel's `version` starts at `1`, an unset `tint` and `key_light` take the entry environment's values, and `scene_seed` is derived from the slug so seeds are stable across environments. Migrations are numbered and move forward only.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One studio, one site. No tenancy beyond account ownership, and no organisation accounts.
- No payments, invoices or cards of any kind; a budget band opens a conversation and never converts currency.
- No comments, likes, follows, public gallery of reels, presence or live cursor; only a reel's owner edits it.
- No floating toast, no dropdown, no paging, no related-projects row, no shimmer, no third waiting signal.
- No external network calls at runtime: no third-party analytics, no outside model service, no font or audio CDN, no map service. Nothing is fetched from any origin but the app's own.
- No image, video, texture, geometry, font file or audio file shipped with the product; every asset is generated. The named open typeface is the only font loaded.
- One locale, `en`, left to right only. A right-to-left locale is out of scope.
- No native application.
- The app stays responsive with all sixteen projects, a producer holding ten reels of fifteen items each, and a pitch carrying hundreds of messages.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`, where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
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

**API shapes.** Bearer auth is required on every endpoint except `GET /api/health`, `GET /api/projects`, `GET /api/projects/<slug>`, `GET /api/tracks`, `POST /api/auth/signup`, `POST /api/auth/signin`, `POST /api/auth/reset`, `POST /api/auth/reset/complete`, `POST /api/auth/verify`, `POST /api/enquiries`, `POST /api/assistant` and `POST /api/events`, which also accept a bearer token when one is sent. A reel, as returned, is `{"id", "title", "state", "share_token", "version", "item_count", "created_at", "updated_at", "items": [{"project_id", "slug", "title", "client_name", "year", "category_slugs", "position", "note", "available", "added_at"}]}` with `items` in position order. A pitch is `{"id", "reference", "reel_id", "state", "budget_band", "timing", "summary", "contact_preference", "organisation", "submitted_at", "items", "excluded", "messages": [{"author_role", "author_name", "body", "created_at"}]}` where `items` and `excluded` are lists of project titles. An account is `{"id", "email", "display_name", "organisation", "role", "locale", "audio_enabled", "verified"}`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status"}` |
| `POST /api/auth/signup` | `{"email", "display_name", "organisation", "password"}` | `201` `{"account", "access_token"}` |
| `POST /api/auth/signin` | `{"email", "password"}` | `200` `{"account", "access_token"}` |
| `POST /api/auth/signout` | none | `204` |
| `POST /api/auth/verify` | `{"token"}` | `200` `{"account"}` |
| `POST /api/auth/verify/resend` | none | `202` `{"message"}` |
| `POST /api/auth/reset` | `{"email"}` | `202` `{"message"}` |
| `POST /api/auth/reset/complete` | `{"token", "password"}` | `200` `{"account"}` |
| `GET /api/me` | none | `{"account", "reel_counts": {"draft", "submitted"}, "pitch_counts": {"open", "closed", "withdrawn"}}` |
| `PATCH /api/me` | `{"audio_enabled"}`, `{"locale"}`, or both | `{"account"}` |
| `GET /api/projects` | `category`, `year`, `client`, `q`, `sort` | `{"items": [project summary], "total"}` |
| `GET /api/projects/<slug>` | none | `{"project": project summary, "categories": [{"slug", "intent_label", "position"}]}` |
| `PATCH /api/projects/<slug>` | `{"state"}` (admin), or any of `{"title", "client_name", "year", "description", "project_link", "category_slugs"}` (editor or admin) | `{"project"}` |
| `GET /api/tracks` | none | `{"items": [{"id", "title", "artist", "source", "position"}]}` |
| `GET /api/reels` | none | `{"items": [reel without items]}`, the caller's own reels, most recently updated first |
| `POST /api/reels` | `{"title"}` | `201` reel |
| `GET /api/reels/<id>` | none | reel |
| `PATCH /api/reels/<id>` | `{"title", "version"}` or `{"share", "version"}` with `share` true or false | reel |
| `DELETE /api/reels/<id>` | query `version`, `confirm_title` | `200` `{"deleted": true}` |
| `POST /api/reels/<id>/items` | `{"project_id", "version"}` | `201` reel |
| `DELETE /api/reels/<id>/items/<project_id>` | query `version` | reel |
| `PUT /api/reels/<id>/order` | `{"project_ids", "version"}` | reel |
| `PATCH /api/reels/<id>/items/<project_id>` | `{"note", "version"}` | reel |
| `GET /api/shared/<share_token>` | none | reel, plus `"owner_organisation"` |
| `GET /api/pitches` | none | `{"items": [pitch without messages]}`, newest first |
| `POST /api/pitches` | `{"reel_id", "budget_band", "timing", "summary", "contact_preference"}` | `201` pitch |
| `GET /api/pitches/<id>` | none | pitch |
| `PATCH /api/pitches/<id>` | `{"state"}` | pitch |
| `POST /api/pitches/<id>/messages` | `{"body"}` | `201` pitch |
| `GET /api/accounts` | none | `{"items": [account]}`, admin only |
| `PATCH /api/accounts/<id>` | `{"role"}` | `{"account"}`, admin only |
| `POST /api/enquiries` | `{"name", "email", "timing", "summary", "contact_preference", "company_website"}` | `201` `{"reference"}` |
| `POST /api/assistant` | `{"question", "project_slug"}`, `project_slug` a slug or null | `200` streaming `text/plain` |
| `POST /api/events` | `{"name", "properties", "consent"}` | `202` `{"stored"}` |

List endpoints return their rows under `items`. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never as a `5xx` and never as a silent success.

**No mocks.** A confirmation, reset, pitch or enquiry mail must exist as a real message in Mailpit, addressed to the one recipient written above, with the subject written above. A line the app writes to its own log, a table of outgoing mails the app keeps for itself, or a success message the app shows without sending are all violations however convincing the page looks. Mailpit is the fact: the app's own interface and its own tables can only reflect what was actually sent, never substitute for it.

## Definition of done

A visitor moves from the entry scene into the reel and into a project without a page load, with every word real text, and still gets the whole site when the scene cannot be drawn. A producer stars, orders and annotates a reel that survives a reload, and sends it once as a pitch the studio answers in the thread, with every mail landing in Mailpit. A write against an old version of a reel changes nothing, and another producer cannot tell that reel from one that does not exist.
