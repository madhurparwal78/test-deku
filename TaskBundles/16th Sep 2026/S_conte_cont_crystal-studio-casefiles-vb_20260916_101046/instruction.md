# Facet

Build and deploy a working web application from this brief. There is no starting codebase. When you are done, a stranger must be able to open the app in a browser, open the menu, filter the studio's case files by sector and read a case file that a studio author wrote, submitted, had approved by an editor and published through the app, then see that same case file change after its author rewrites and republishes it, without hitting an error page. The hard part is that publication is real. A case file that is not published, and every image uploaded to it, must stay unreadable to anyone without a studio session, by any means, including a direct request for its address or for the image itself. Every uploaded image must exist as a real object in the MinIO bucket at its pinned key; a copy on the app's own disk, or bytes the app keeps in its own tables, does not count.

## Overview

Facet is the public site and the studio console of Kelo, a small creative studio whose wordmark reads `Kelo · Creative Studio` over `Since 2011`. The public site behaves like an object rather than a document. The window is filled edge to edge with one near-black screen carrying a single slowly turning faceted crystal, with the wordmark inside it. There is no scrollbar on arrival, no header bar, no navigation strip and no footer, and the home screen is exactly one window tall. Four small controls sit in the four corners of the window and nothing else does. Every other surface (the menu, the studio story, the work carousel, the project grid, a case file, the showreel, the contact surface and the privacy notice page) arrives over that screen as a layer when a corner control or a menu word is used, leaves the same way, and has its own address so it can be linked, bookmarked and shared. Nothing ever loads a new document.

Around that site Facet adds the machinery a studio site needs to stay alive: an author who writes case files, an editor who reviews and approves them, a publication step between what is written and what a visitor sees, an enquiry that reaches a person, and a visitor who can keep a shortlist of the work they liked. A case file is the unit the studio is judged on: a header, an ordered run of chapters of eight kinds, and a footer.

Four audiences use it. A signed-out visitor wants to judge whether the studio can do the thing they need. A signed-in visitor keeps a shortlist and an enquiry thread. An author, a studio member, wants to publish a case file that reads the way the studio's work looks. An editor, the studio's owner, approves, publishes, orders the public grid and takes work down.

Facet is deliberately not a social product or a shop: no comments, likes, follows or public profiles; no pricing or checkout; no search box on the public site; no collaborative co-editing of one field; no outbound email; no notification bell, badge count or toast stack; and no image, font, audio or video file of its own is shipped or fetched.

Every numbered rule in this brief is normative and part of the product's acceptance; anything said about how the reference studio built its own site is informational only, and every extension beyond that reference is specified here rather than left to evidence. The whole product rests on one assertion: a case file an author writes reaches the public only through review and publication, and reaches it immediately when it does.

The genuinely hard part is the editorial state machine behind a public surface that must never show what is not published: a case file moves through draft, submitted, changes requested, approved and published, nobody approves their own work, and a live case file can be rewritten while the public keeps seeing the published text until its author publishes the changes.

## User roles

| Role | Can do |
|---|---|
| Signed-out visitor | View the public site; turn and reseed the crystal; filter the project grid; read published case files; send an enquiry that is not attributed to any account; subscribe to `DISPATCH`; keep a shortlist in this browser only. **Cannot see the console and cannot read anything that is not published.** |
| `visitor` | Everything above. Once the address is verified: keep a shortlist that follows the account to another device, and send an enquiry attributed to the account, which the studio can reply to. **Cannot see the console, and cannot become an author or an editor by any action of their own.** |
| `author` | Everything a visitor can do; see the studio console; create a case file; edit, arrange, upload media to and submit a case file they created; publish changes to their own published case file. **Cannot open or edit a case file somebody else created, cannot approve or return anything, cannot publish or unpublish, cannot reorder the public grid, cannot edit the sector taxonomy, the client roster or the notice page, cannot read the enquiry inbox or the outbox, cannot invite anyone or change any role, cannot delete a case file.** |
| `editor` | Everything an author can do, on any case file; approve or return a submitted case file; publish and unpublish; reorder the public grid; edit the sector taxonomy, the client roster and the notice page; read and reply to enquiries; read the outbox; invite accounts; change another account's role; delete a case file that was never published; remove the seeded examples; export every entity. **Cannot change their own role, cannot approve their own case file while another editor exists, and cannot delete a case file that was ever published.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a visitor or author session to any editor-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged. The same holds for reads: a studio read from a visitor session, or an author's read of another person's case file, is denied and returns nothing of the case file.

Enforcement happens on the request. Every request is checked in this order, and a failure at any step stops there: is the caller signed in, is the caller's role allowed, does the caller own the thing (unless an editor), and is the thing in a state where the action makes sense.

Sign-up is **open** at `/join` and always creates a `visitor`, whatever the request asks for. An `author` or an `editor` exists only by invitation from an existing editor, and the only way to change a role is an editor changing another account's role; there is no other surface anywhere in the product that promotes an account.

Nobody approves their own work, including the person who runs the studio. An author never approves anything. A case file submitted by an editor is approved by a different editor. Where the studio has exactly one editor, that editor's own case files skip `submitted` and move from `draft` straight to `approved`, and the case file records that no second pair of eyes saw it: the case file list shows `SELF APPROVED` in place of the reviewer's name.

Seeded accounts, all using the password stated in `## Data model`: `editor@example.com` (editor, Ines Varga), `author@example.com` (author, Theo Lamb), `author2@example.com` (author, Juno Park) and `visitor@example.com` (visitor with a verified address, Sam Reed). The seeded studio therefore has exactly one editor.

## Core features

### The critical rule: uploaded media and what the public may read

1. An image for an `image`, `device` or `split` chapter is uploaded by the case file's author or by an editor with `POST /api/studio/case-files/{id}/media` and stored as an object in the MinIO bucket named by `STORAGE_BUCKET`, at the key `case-files/{case_file_id}/{sha256_of_bytes}.{ext}`, where `{sha256_of_bytes}` is the lowercase hex SHA-256 of the uploaded bytes and `{ext}` is `png`, `jpg` or `webp`. For example: `case-files/42/9f2a...d0.png`. The bytes live in the bucket and nowhere else: not on the app's filesystem and not in any database column.
2. An upload that is not a PNG, JPEG or WebP image, or that is larger than 5242880 bytes, is rejected as invalid with the field named `file`, and nothing is written to the bucket or the database.
3. Media is served only through `GET /api/media/{media_id}`, streamed from the bucket with the stored content type. **While its case file is not `published`, a request with no session, from a visitor, or from an author who does not own the case file is denied as not found and receives no bytes**; the owner and any editor receive the bytes. Once the case file is published, anyone receives them. No public or presigned bucket address is ever handed out.
4. **A case file that is not published does not exist publicly.** `GET /api/case-files/{slug}` and the page at `/work/{slug}` answer not found for any case file whose state is not `published`, including one that was published and later taken down, and the public list never includes it. Its owner and any editor see it only inside the studio, at `/studio/case/{case-file-id}`, in a preview that renders it exactly as the public surface will.
5. Only the case file's author or an editor may upload to it. Anyone else is denied, and nothing is stored.

### Auth

6. Accounts use app-implemented email and password with bearer tokens. `POST /api/auth/login` takes `{"email", "password"}` and returns `{"access_token", "account"}`; every protected call sends `Authorization: Bearer <access_token>`. The token is the opaque identifier of a server-side session, and a new one is issued on every sign-in and on every privilege change.
7. A failed sign-in answers `That combination is not one we know.` and never says whether the address exists or which half was wrong.
8. Passwords are 12 to 128 characters, stored only as an argon-family hash, and never returned by any endpoint. A shorter one is rejected with `Passwords are at least twelve characters.`.
9. Email addresses are lowercased on save and unique; a second account for the same address is rejected as a conflict.
10. A visitor session lasts 30 days and has no idle timeout. An author or editor session lasts 12 hours and ends after 2 hours without use. `GET /api/auth/sessions` lists the caller's sessions with `expires_at` and `idle_timeout_seconds`, several sessions may be live at once, and any one of them can be revoked individually with `DELETE /api/auth/sessions/{id}`.
11. `POST /api/auth/logout` revokes the current session only, unless the body carries `"all_devices": true`, which revokes every session of the account. A revoked or expired token is refused on every protected call.
12. Sign-up at `POST /api/auth/signup` creates a `visitor` with an unverified address, signs them in immediately with reduced capability, and writes a `Confirm your address` message carrying one link to `/verify?token=<token>` that stays valid for 7 days. Following it (`POST /api/accounts/verifications` with the token) marks the address verified. An address left unverified for 7 days is deleted with its account and becomes free for a new sign-up; the account shows its `verification_deadline`.
13. An unverified visitor may keep a shortlist only in the browser, may not send an attributed enquiry and may not be replied to, and sees `CONFIRM YOUR ADDRESS TO GET A REPLY` above the enquiry form.
14. A password reset (`POST /api/accounts/resets`) always answers `If that address has an account, a reset link is on its way.`, whether the address exists or not. When it does exist, a `Reset your password` message is written with one link to `/reset?token=<token>`, valid for 60 minutes, single use, and void once the account signs in successfully. Completing a reset revokes every session of that account, including the one that asked for it.
15. An editor invites an account with `POST /api/studio/invitations`, naming the address, the display name and the role (`author` or `editor`). The response carries `invite_url` (`/invite?token=<token>`), and a `Kelo has invited you` message is written naming who invited them, the role and the 14 day expiry. Accepting at `POST /api/invitations/accept` sets the password and signs the new account in.
16. An account holder may change their display name, their password and their email address (the old address is kept as a recovery route for 30 days, shown as `previous_email` and `previous_email_until`). Only an editor may change a role, and never their own; an editor trying to change their own role is refused with `Not for you` at the field and the role stays as it was.
17. A session that expires while the console is open does not throw anyone out. The next save fails, the field's label turns the warm sand colour, and a sign-in layer opens over the console with the console's state and the typed text intact behind it; signing back in retries the failed save. An editor that loses a paragraph on session expiry is not acceptable.
18. Five failed sign-ins for one account within 15 minutes lock further attempts for that account for the rest of the window; the surface shows `Too many tries. Give it a minute.` and counts down.

### The one-screen shell and the crystal

19. The home screen at `/` is exactly one window tall: the document's height equals the window's height and there is no document scroll. It shows only the crystal, the two-line wordmark (`Kelo · Creative Studio`, then `Since 2011`, one heading with a line break, not two headings) and the four corner controls.
20. The crystal is a single continuously rotating faceted object rendered into a surface that fills the window at the device's pixel density, redrawn per frame without re-laying out the document. It reads as a shattered mass rather than a smooth ball, with several of its faces visibly detached and floating clear of the rest; only a few faces are bright in any frame, against a ground within a few shades of the crystal layer's near-black; every bright edge carries an opposed two-colour fringe (a cold cyan edge on one side, a warm red edge on the other); and the wordmark sits inside the object's depth, with facets passing both in front of and behind the letters.
21. Dragging anywhere on the home screen rotates the crystal with the pointer; on release it keeps its momentum and decays back to its idle rotation. A drag that starts on the wordmark reaches the crystal, never selecting the text.
22. The `Drop` control reseeds the crystal: every facet is thrown outward and falls back together in a new arrangement, without reloading the scene, and the reseed counter in the interaction bar increments and rolls to its new value.
23. The crystal's resting angle, its seed and the reseed count are stored per visitor in browser storage under the keys `crystal_angle`, `crystal_seed` and `crystal_count`, and survive a reload. The counter's shown and stored values are clamped at `999999`, and a stored value that is not a number resets to zero. The count never leaves the device.
24. When three-dimensional rendering is unavailable, the crystal is replaced by a static drawing of the same object at the same place over the same ground, and the rest of the product stays fully usable. The crystal is never hidden at any width, and it is built once when the site opens and keeps turning behind every other layer; opening or closing a layer never rebuilds it or forgets how the visitor turned it.
25. The home screen is never destroyed; every other layer opens over it and the crystal keeps turning behind each one. In the studio console it turns at half its idle rate.
26. The arrival sequence shows the drop mark, a thin progress line that fills from left to right as a true report of loading, and then the wordmark fading in; the corner controls appear only after it completes, one after another. The wordmark and the progress report appear within 1 second of the document arriving; a spinner is never shown without a progress fill beside it; and the arrival overlay is never held for more than 8 seconds, after which the home screen is revealed with whatever has loaded and the shortfall is reported in the interaction bar's message. Deep entry to any other address skips the arrival sequence and opens that layer with the crystal already at rest.

### The corner controls and the interaction bar

27. Four corner controls are the whole navigation: `Drop` (top left, reseeds the crystal), `Discover` (top right, opens the menu), `Showreel` (bottom left, opens the reel) and `Audio` (bottom right, toggles sound). Each is a small mark whose name appears only when the pointer comes near it.
28. Each corner control is acquired from well before the pointer reaches the mark: an invisible circular catchment several times the mark's size is pushed out toward the window's corner, so the empty corner the pointer sweeps through on its way in is already live. A pointer entering a corner acquires that control roughly a hundred pixels before it reaches the mark. This catchment is the product's central interaction decision and is never approximated away.
29. The corner controls never move into a bar and never collapse into a menu sheet, at any width.
30. While any layer is open, a wider close control replaces `Discover` in the top right, labelled for what closing does: `Close Project` (case file), `Close Showreel`, `Close All Projects` (project grid), `Close Story`, `Close Contact`, `Close Notice` and `Close Studio` (console). Each open layer has exactly one closing affordance, and one action closes it. The menu is the one layer whose close control carries no label: it keeps the plain close mark, because the three words are the whole of it.
31. Along the bottom centre of the window sits the interaction bar: a short message line in small spaced capitals, a thin line, a ring that turns for anything pending, and the reseed counter, whose digits roll like an odometer when the count changes. Bar messages are uppercase, at most 24 characters, held for 2 seconds and then faded. The bar is the only place ignorable news is said: `SAVED`, `ORDER SAVED`, `ORDER NOT SAVED`, `GRID ORDER NOT SAVED`, `NOT SAVED`, `SENT FOR REVIEW`, `APPROVED`, `LIVE`, `TAKEN DOWN`, `NEW ENQUIRY`, `OFFLINE`, `BACK ONLINE`, `OFFLINE, SAVING LATER`, `SAVED WHAT YOU MISSED`, `SHOWING WHAT WE HAD` and `REDUCED GRAPHICS`.
32. Nothing a visitor must act on is ever said only in the bar: every such message also appears as an inline notice or a pinned note, and the bar's text is announced to screen readers through a polite live region.

### Sound

33. Sound is off on arrival, always, with no autoplay attempt; nothing in the arrival sequence waits on audio; and no audio is fetched or synthesised until the visitor turns sound on with the `Audio` control, whose two states are distinguishable from the mark alone (a speaker with a cross when off, a speaker with two arcs when on).
34. The choice persists per visitor in browser storage under the key `sound` and survives a reload.
35. Every bed and cue is synthesised in the page, never played from a file: a low, slow, almost-still ambient bed behind the home screen; the same bed opened up while the menu is forward; a bed with a slow added pulse behind the work carousel; a brief band of air for a layer transition; a reedy swelling bed for the narrow-window card; a very short quiet tick when the pointer approaches a corner control; a short falling tone when a control is pressed; and a low falling tone with a shudder in it for a reseed. Turning sound on fades the current surface's bed in; turning it off fades it out and releases the audio device. A surface change crossfades the outgoing bed into the incoming one so two beds never play at full level at once, and a cue never raises the total level above the bed's own.

### The menu

36. `Discover` opens the menu over the home screen, which stays visible behind it. The menu is three enormous words in one row, in sentence case: `About` opens the studio story, `Work` opens the work carousel, `Contact` opens the contact surface. The address does not change while the menu is open.
37. The words arrive in depth one after another. Pointing at one keeps it at full strength while the other two dim. Choosing one closes the menu and opens the chosen surface. Escape or the close control closes the menu. Tab moves through the three words left to right.
38. While the words are still moving into place an invisible sheet covers them, so a word that lands under a resting pointer does not react; nothing responds until the words have settled and the pointer actually moves.
39. Below the three words, at the bottom centre of the menu, a small line of capitals is the account entry: `Studio Sign In` when signed out, `Studio` for an author or editor, `Your Shortlist` for a visitor. It is never a fourth large word. A locale control sits at the foot of the menu layer.

### The studio story

40. `/story` shows, in order: a visually hidden first heading `About`; the studio title `Kelo · Creative Studio`; a rule; the promise `Making the story move.`; the disciplines line `Brand · Content · Experience · Digital`; a rule; the heading `Selected Clients` over one row per sector, each row a sector label beside that sector's client names; a rule; the heading `Awards` over the award names three to a row; a rule.
41. The layer scrolls inside itself while the page behind it stays one window tall and the crystal keeps turning behind it. Nothing on it is a link except the close control; client names are not links.
42. Client names in a row are separated by a middle dot with a non-breaking space on each side, generated after each name rather than typed into the names, so removing the last client of a row never leaves a trailing dot.
43. The client roster and the sector labels are data an editor maintains. A sector label is at most 24 characters and always fits on one line; the row aligns along its bottom edge.
44. The story's structure keeps the reference's block order. Both brand-derived identifiers are renamed: the studio-title and studio-subtitle elements carry the class names `about__studioTitle` and `about__studioSubtitle`, and no class name anywhere carries the studio's name.

### The work carousel

45. `/work` shows the work as a depth carousel: published case file titles laid out in a line running away from the viewer, each with a poster behind it. Dragging left or right swings the line past, titles ahead growing and titles behind shrinking; releasing settles on the nearest title; the previous and next arrows move by one item; pointing at an item that is not active raises its client line to full strength; choosing an item opens that case file.
46. The carousel holds only published case files, in the grid order an editor sets, capped at the first twelve of that order; the thirteenth and later are reachable only through `View All Projects`. A case file published to the end of the grid order therefore reaches the carousel only once its position is twelfth or better.
47. A drag affordance, a line with an arrowhead at each end, draws itself on stroke by stroke when the carousel becomes draggable. It is the only instruction the site ever gives, and it is drawn rather than written.
48. `View All Projects`, a small line of spaced capitals above the carousel, opens the project grid.

### The project grid and the sector filter

49. `/work/all` shows the published case files as tiles two across, a page of twenty-four at a time and the next page fetched as the visitor reaches the end, each tile a poster with the project name in small capitals under it and the client name under that in grey. Above the tiles, the word `Filter` sits almost invisible as a legend, and below it the sectors are listed very large with every unselected one dimmed: `All`, then `Technology & Futures`, `Climate & Startups`, `Fashion & Beauty`, `Chain`, `Entertainment & Culture`, `Automotive`, `Collaborations`.
50. One sector is selected at a time; `All` is the absence of a sector and renders in the same list at the same size as the first entry. Choosing a sector restacks the tiles into their new positions one after another in a quick ripple, never reloading them, and updates the address to `/work/all?sector=<token>` (for example `/work/all?sector=sector-3`). The unfiltered grid is `/work/all` and nothing else.
51. The grid is dragged rather than scrolled; while the pointer is over the grid away from a tile, the site's own round cursor replaces the arrow and follows the pointer; pointing at a tile lifts its poster toward the viewer and raises its caption to full strength.
52. A sector with no published case file replaces the tiles with one centred line `Nothing here yet.`, a smaller line `No work in this category yet.`, and one control `SEE ALL WORK`, which returns the grid to `All`.
53. `Close All Projects` returns to the carousel.

### The case file

54. `/work/<case-file-slug>` shows one published case file: a header (the title, the description, up to six information items each a heading over a value, and the launch address under the label `LAUNCHED AT`), then its chapters in their stored order, then a footer (its awards, the launch line drawn as a thin rule across the page), then a preview of the next case file in grid order under `NEXT`, which opens that case file in place.
55. A chapter is one of eight kinds, and each renders as described: `headline` (a big title), `text` (a short label column beside a column of writing, with underlined links), `list` (a bulleted list), `image` (a still that fills its block without distortion, with an expand control), `video` (a poster with a round play control; playing fades the poster, starts the film and shows the transport; with close and expand controls), `video_loop` (a film that loops with no controls over a faintly darkened ground), `device` (a phone or tablet frame, portrait or landscape, whose screen image can be dragged to scroll inside the frame, with a small rotated scroll hint beside it when it scrolls), and `split` (a before-and-after comparison revealed by dragging a round handle, vertical or horizontal).
56. In a `split` chapter the two media sit end to end inside a clipped window and the drag moves the pair, so neither image stretches or squashes at any handle position. Pressing the handle shrinks it almost to nothing and removes its arrow mark, so nothing sits between the visitor and the two images while dragging; releasing restores it. Its two labels sit in the corners of the frame. The drag is catchable a little outside the visible frame.
57. An expand control fills the window with that chapter's media over everything and shows a close control. Each chapter's text reveals as it enters the window while the case file scrolls inside itself.
58. An image chapter without an uploaded image shows a generated placeholder: a gradient between two of the product's own dark tones, chosen and angled deterministically from the case file's slug, with a faint grain over it and the client name centred in small spaced capitals. A video chapter without a film shows the showreel-style empty layout rather than a fake film.
59. Every image chapter carries alternative text (its `alt`), which the page uses as the image's text alternative.
60. Awards in the footer sit in a row that aligns along its bottom edge, each rendered as its name under a short rule at its treatment's height.
61. `Close Project` returns to wherever the case file was opened from. For a published case file its own author sees one extra control, `EDIT THIS`, below the close control.

### The showreel

62. `Showreel` opens `/reel`: a still poster fills the window with one dark rectangular play control in the middle labelled `Showreel` beside a small triangle. Pressing it fades the poster, plays the film full window, and raises the transport from just below the bottom edge; the playhead follows the pointer on the transport bar; the transport lowers again after 2 seconds with the pointer away from it. Space plays or pauses while the reel is open. `Close Showreel` or Escape stops playback and closes the layer.
63. The reel's film is the operator's. Until one is supplied the layer shows the centred notice `No reel yet.`, `The studio has not put a reel up.` and `SEE THE WORK`, never a placeholder film or a looping colour bar. The poster is generated from the product's own palette and the crystal.

### Contact, enquiry and the newsletter

64. `/contact` shows the heading `Contact` beside two large underlined addresses, `newwork@kelo.example.com` (opens the mail client) and `careers.kelo.example` (opens the hiring site in a new tab); a rule; then two office blocks, `HARBOURSIDE` with `+00 1 234 5670` and the four lines `12 Quay Street`, `Harbourside Works`, `Floor 3`, `HS1 4QA`, and `NORTHGATE` with `+00 2 345 6780` and the two lines `40 North Row`, `NG2 7LT`; then `SOCIAL` with `Directory`, `Pictures` and `Feed` on three lines. Telephone numbers and addresses are shown exactly as stored, never reformatted, one line per stored line.
65. Above the newsletter strip sits the enquiry form under the heading `Tell us about it.`, with the fields `Your name` (`name`, required, 2 to 80 characters), `Your address` (`email`, required, one `@` with a dot after it, at most 254 characters), `Who you are with` (`organisation`, optional, at most 120), `Rough budget` (`budget`, optional, offered as the five bands `under 25`, `25 to 50`, `50 to 100`, `100 to 250` and `250 and up`, in thousands, and stored as the matching token in `## Data model`), `What you want made` (`brief`, required, 40 to 4000 characters), `What kind of work` (`sector`, optional, one of the seven sectors) and `You may keep my details to reply.` (`consent`, required), and the control `SEND`. It uses the same field and submit treatment as the newsletter strip, so the two forms read as the same species.
66. A valid enquiry is stored with state `new`, and the whole form is replaced in place by the heading `Thank you.` and the line `We read everything and answer within two working days.`. An enquiry from a signed-in visitor with a verified address is attributed to that account; any other enquiry is stored unattributed.
67. Pinned to the bottom of the contact layer is a slim newsletter strip with two small links: `DISPATCH` (the studio's newsletter gazette) and `PRIVACY`. `DISPATCH` turns the strip, in place, into one line of form (an address field and a small arrow control); the links fade out. A valid address is stored once and the strip answers `Thanks! You are now subscribed.`, then returns to its two links after 6 seconds. The same address submitted again is answered with the same success copy on the strip, while the server refuses the repeat as a conflict and stores nothing new, so nobody learns from the strip whether an address is already on the list. A failure answers `It looks like something went wrong. Please try again.` in the same strip, without anything jumping. `PRIVACY` opens the notice page over the contact layer. The newsletter is never queued while offline.
68. `Close Contact` returns to the home screen.

### The notice page (the privacy page)

69. `/notice` is the studio's privacy notice: a visually hidden first heading `Privacy`, the title `Kelo Customer Privacy Notice`, the description `This privacy notice tells you what to expect us to do with your personal information.`, a contact strip with the headings `EMAIL` (`privacy@kelo.example.com`), `ADDRESS, ONE` and `ADDRESS, TWO`, and then fourteen rows, each a short uppercase label beside a long paragraph, with the date of the last update at the foot. It is reachable from the `PRIVACY` link on the contact surface and at its own address.
70. The fourteen rows are seeded with these labels, in order: `What information we collect, use, and why`, `LAWFUL BASES part 1`, `LAWFUL BASES part 2`, `Where we get personal information from`, `HOW LONG WE KEEP INFORMATION`, `who we share information with`, `your data protection rights`, `How to complain, United States`, `How to complain, European Union`, `How to complain, Canada`, `How to complain, Australia`, `How to complain, New Zealand`, `How to complain, United Kingdom`, `When this notice was last updated`. The first row states what the studio stores about a visitor: the enquiry fields, a newsletter address, a signed-in shortlist, and the named analytics events with no typed text in them.
71. The notice is set at almost headline size with a very large gap between rows, deliberately: it reads as something the studio wrote rather than small print. Inside the paragraphs, the phrase that says what the studio does with a visitor's information is picked out in the warm sand colour, and a link on this page turns the same colour on hover. That colour appears nowhere else on the public site.
72. The notice is data an editor maintains (`PATCH /api/studio/notice-rows/{id}`). A row's body keeps only four treatments: paragraphs (`p`), unordered lists (`ul` with `li`), links (`a` with `href`) and emphasis runs (`em`). Every other element and every attribute other than a link's `href` is stripped on save. A link whose address is not `https:` or `mailto:` is dropped and its text kept. Each row's copy fades in as it enters the window. `Close Notice` returns to the contact layer.

### Addresses, history and reachability

73. Addressing: every surface has a stable address (listed in `## User flow`), so a case file's address pasted into a fresh browser opens that case file with the rest of the site behind it. Address changes are pushed onto history without a document load; the browser's back control closes the open layer rather than leaving the site. Every public surface is reachable in at most three actions from the home screen (menu one, story, carousel and contact two, grid, case file and notice three, showreel one) and closeable in one.
74. Keyboard on the home screen: Tab moves through the corner controls in the order `Discover`, `Showreel`, `Audio`, `Drop`, then the crystal as one focusable region; Enter or Space activates a focused control; with the crystal focused, the left and right arrows turn it by 0.12 radians per press; `R` reseeds it; Escape closes the topmost open layer and does nothing on the home screen. Any other key does nothing.

### The studio console

75. The console is the same site with different things on it: the same near-black ground, the same type, the crystal still turning behind it, and the same close control labelled `Close Studio`. It has no save button anywhere.
76. The case file list at `/studio` shows one row per case file, sorted by state and then by grid position, with the columns grid position (blank when unpublished), title, client, sector (uppercase), state, and last update as a relative time. An author sees every row, but a row belonging to another person shows its title dimmed and is not a link. Above the list sits the same large filter construction as the public grid, filtering by state, a second row for sector, and a free-text search field. `NEW CASE FILE` sits above the list.
77. The editor at `/studio/case/<case-file-id>` has the chapter list on the left (each row showing its kind and its first line, each draggable) and the chosen chapter's fields on the right. Its blocks are: the header (title, client, sector, description, up to six information items each with a heading and a value, the launch address), the chapters, the footer (awards, each a name and a mark treatment), and the publication block (state, grid position, and the submit or publish control). For an editor the editor also shows a line naming who wrote the case file and when they last touched it.
78. Every field saves itself when the field is left, never on a save control, and reports the save through the interaction bar as `SAVED`. A field whose save fails keeps its value, turns its label the warm sand colour, and retries twice, after 2 seconds and after 6 seconds; after the third failure it shows `Not saved. Your text is safe here.` and the case file cannot be submitted until the value is saved.
79. The chapter arranger is a full-window layer over the editor showing every chapter as a tile, two across; dragging a tile to a new place restacks the others in a quick ripple. The new order is saved as one request carrying the complete list; `ORDER SAVED` confirms it, and a failed save animates the list back to the server's order and shows `ORDER NOT SAVED`.
80. The review queue at `/studio/review` is the case file list filtered to `submitted`, with two controls per row, `APPROVE` and `RETURN`. `RETURN` requires a note of 10 to 500 characters (`Say what needs changing.` otherwise).
81. The grid arranger at `/studio/grid` renders the public grid live with every tile draggable; the new order is saved as the complete list. Dragging a tile out of the grid takes that case file down: it returns to `approved`, leaves the grid and the carousel, and its address stops resolving. A failed save shows `GRID ORDER NOT SAVED`. Sector taxonomy editing is reached from the grid arranger.
82. The enquiry inbox at `/studio/enquiries` shows one row per enquiry, newest first, unread rows at full strength and read rows dimmed, with the columns received (relative time), name, organisation, budget, sector and state (`new`, `assigned`, `answered` or `archived`). Opening a row shows the brief as reading text and marks it read; the editor may assign it, reply, or archive it. A reply is stored on the enquiry, sets it to `answered`, and is shown to its sender under their own account; an enquiry that is not attributed to an account cannot be replied to in the app.
83. `/studio/outbox` lists every message the product has written, newest first, for an editor to read and relay. `/studio/site` holds the sector taxonomy, the client roster, the notice rows, the list of accounts with their roles, and the export of every entity as one document.
84. The account surface at `/studio/account` shows the display name, the email address, a password change, the live sessions (each revocable, plus `all devices`), the account's own messages, and for a visitor the shortlist and their enquiries with any reply. An editor changing another account's role does it from the list of accounts on `/studio/site`.
85. When a second person opens the same case file, a pinned line reads `<name> is also in here.` (for example `Ines Varga is also in here.`) above the header block. A field the other person is focused on shows its border in the warm sand colour and cannot be edited until they leave it or go quiet for 30 seconds; a save to that field is refused as a conflict. Presence is announced with `POST /api/studio/case-files/{id}/presence`, and the case file carries `presence`, the other people currently in it and the field each holds. Nobody is locked out of the case file itself.

### The primary workflow: from a studio member's head to the public grid

86. A case file's state is one of `draft` (being written), `submitted` (waiting for review), `changes_requested` (returned with a note), `approved` (passed review, not on the grid) and `published` (on the public grid). Moves are made with `POST /api/studio/case-files/{id}/transitions` and `{"to": <state>, "note": <text>}`:
    - `draft` to `submitted`: the owner or an editor; in the single-editor branch an editor's own case file goes to `approved` instead, with no reviewer recorded and `self_approved` true.
    - `submitted` to `changes_requested`, or `submitted` to `approved`: an editor who is not the owner.
    - `changes_requested` to `submitted`: the owner or an editor.
    - `approved` to `published`, and `approved` back to `draft`: an editor.
    - `published` to `approved` (taking it down): an editor.
    Any other move is refused as not allowed in that state, and the stored state does not change.
87. `NEW CASE FILE` creates a case file with state `draft`, the caller as owner, the title `Untitled`, no slug, no chapters and no sector.
88. The header saves field by field: title (2 to 80 characters, never `Untitled`; `Give it a title.`), client (1 to 60; `Say who it was for.`), sector (one of the seven; `Pick a sector.`), description (40 to 400; `The description needs to be at least forty characters.`), launch address (optional; must parse and use `https`; at most 2048 characters; `That launch address does not look right.`), up to six information items (heading 1 to 24, value 1 to 60; `Information item <n> is missing a heading.` or `Information item <n> is missing a value.`), and awards (name 1 to 40, mark one of `treatment-1` to `treatment-8`). A save carrying an invalid value is refused with the field's message and writes nothing.
89. On the first save of a non-empty title the slug is derived: lowercase the title, replace every run of characters that are not letters or digits with one hyphen, trim hyphens at the ends, and append `-2`, `-3` and so on until it is unique. For example `The Long Room` gives `the-long-room`, and a second case file with the same title gives `the-long-room-2`. The slug never changes again when the title changes, because a published address must not rot. An editor may change it exactly once, and doing so makes the old public address answer a permanent redirect to the new one. A slug that has ever been issued is never issued again, even after its case file is deleted.
90. A chapter is added with `POST /api/studio/case-files/{id}/chapters` as `{"kind", "payload"}`, always at the end of the list, and each chapter is stored with its `position`, its `kind` and its `payload`. A chapter may be saved unfinished; an unknown kind is refused. A chapter is finished when: `headline` has a `title` of 1 to 120 characters; `text` has a `label` of 1 to 40 and a `body` of 1 to 4000; `list` has 1 to 20 `items`, each 1 to 200; `image` has an `alt` of 1 to 160 (and an optional `media_id`); `video` and `video_loop` have a `title` of 1 to 120 (and an optional `video_url`); `device` has an `orientation` of `portrait` or `landscape` (and an optional `media_id`); `split` has an `orientation` of `vertical` or `horizontal` and a `before_label` and an `after_label` of 1 to 24 each (and optional `before_media_id`, `after_media_id`).
91. Chapters are ordered with `PUT /api/studio/case-files/{id}/chapter-order` carrying the complete ordered list of the case file's chapter ids. Every position is rewritten in that one request; a list that leaves out a chapter, repeats one or names a chapter of another case file is refused and changes nothing, so a failed reorder can never leave the list half-ordered.
92. `SUBMIT FOR REVIEW` runs every gate first and moves nothing if any fails; each failure is listed by number in the console, and the refusal names every failed gate under `fields` with its message. The gates: (1) title 2 to 80 and not `Untitled` (`title`: `Give it a title.`); (2) client 1 to 60 (`client`: `Say who it was for.`); (3) sector is one of the seven (`sector`: `Pick a sector.`); (4) description 40 to 400 (`description`: `The description needs to be at least forty characters.`); (5) at least one chapter (`chapters`: `A case file needs at least one chapter.`); (6) every chapter finished (`chapter_payloads`: `Chapter <n> is not finished.`, where `<n>` is the chapter's position); (7) no two chapters share a position (`chapter_order`: `The chapter order is broken. Open the arranger and save it again.`); (8) the launch address, if present, is valid (`launch_url`: `That launch address does not look right.`); (9) every information item has a heading and a value (`information_items`); (10) the slug is unique (`slug`: `Another case file already has that address.`).
93. A successful submit sets `submitted`, records `submitted_at` and `submitted_by`, shows `SENT FOR REVIEW`, and makes the case file read-only for its author: an author's edit, chapter change or reorder while it is `submitted` is refused and changes nothing, and the submit control is disabled and reads `WITH THE EDITOR`. A case file that is already submitted cannot be submitted again.
94. `RETURN` sets `changes_requested`, stores the note on the case file as `return_note`, records `returned_at`, and makes the case file writable again for its author, with the note pinned above the header block under a warm sand label (`Ines Varga asked for changes: <note>`), announced as `Changes requested` to screen readers.
95. `APPROVE` sets `approved` and records `reviewed_by` (the approving editor) and `approved_at`. Approving or returning a case file that is no longer `submitted` because somebody else moved it first is refused as a conflict with `Already handled by <name>.`, and its row leaves the queue. When two approvals of one case file arrive at the same moment, exactly one succeeds and the other is refused as a conflict.
96. `PUBLISH` (in the publication block, or a drag into the grid arranger) sets `published`, records `published_at`, and places the case file at the end of the grid order unless the drag placed it elsewhere; the editor sees `LIVE`. From that moment the case file is in the public list, and in the carousel when its grid position is twelfth or better, and its address resolves, with no rebuild, cache purge or deploy: the grid is queried, not generated.
97. A published case file stays `published` while it is reopened and rewritten, from the case file list or from `EDIT THIS`. Every content change to it (header fields, information items, awards, chapters and their order) is written to a pending copy, `draft_payload`, alongside the live one, so the public surface never shows a half-finished sentence and keeps serving the published content.
98. `PUBLISH CHANGES` (`POST /api/studio/case-files/{id}/publish-changes`) is available to the author on their own published case file, without a second review, and to any editor. It copies the pending copy over the live content, clears `draft_payload`, leaves `published_at` alone and updates `updated_at`; the public address shows the new content on the next request, to a fresh device with no session and no stored data. If the live content changed under the author since the pending copy was read, the two are shown side by side and nothing is discarded until a person chooses.
99. A case file can be deleted only while it has never been published. A published case file is retired by taking it down to `approved`, which removes it from the grid and the carousel, clears its grid position and leaves its address answering not found; it can be published again.
100. Failure branches: a field save that fails keeps the value and retries as in rule 78; a save whose session expired opens the sign-in layer as in rule 17; a failed chapter reorder snaps back with `ORDER NOT SAVED`; a submit that fails a gate moves nothing and lists the failures; a publish whose slug collided since the draft was saved is refused with gate 10's message and the publication block offers a new slug; unpublishing the only case file of a sector leaves that sector showing the empty grid state.
101. Every write that carries a `version` is compared with the stored `version`, which increases on every write; a stale one is refused as a version conflict and the side-by-side resolution is offered, discarding nothing.

### Forms and validation

102. Four forms exist and all use one field treatment: the newsletter (`email`), the enquiry (`name`, `email`, `organisation`, `budget`, `brief`, `sector`, `consent`), sign-in (`email`, `password`) and the case file editor (the header and chapter fields). Every form control carries its field name as its `name` attribute (the sign-in address field is `name="email"`, the enquiry's brief is `name="brief"`), so a form can be driven by field name. Every form rejects invalid input inline, under the field it concerns, names that field, and writes nothing. The inline copy: `That address does not look right.` (email), `We need a name to reply to.` (name), `That is longer than we can store.` (organisation), `Tell us a little more, forty characters at least.` (brief, too short; a brief over 4000 characters is refused too), `We need this to be able to reply.` (consent), `Passwords are at least twelve characters.` (password), plus the editor messages in rule 88.
103. Validation never runs on a keystroke. A field validates when it is left, once it has been left non-empty at least once (a field touched and left empty validates when left; a field never touched does not). On submit every field validates, the first invalid field takes focus, and the count is announced (`<n> things need attention`). The server validates every field of every request regardless of what the page did, and answers an invalid request with the field names and their messages.
104. The submit control is disabled only while a submission is in flight, never because the form is incomplete: pressing submit on an incomplete form is how a visitor asks what is missing, and the form answers.
105. While pending, the submit control's mark is replaced by the turning ring and it stops responding to the pointer, the fields stay editable and keep their values, and the response line stays hidden. After 10 seconds with no answer the pending state ends, the failure copy is shown and every value is kept.
106. Success: the newsletter strip shows `Thanks! You are now subscribed.`; the enquiry form is replaced by `Thank you.` and `We read everything and answer within two working days.`; sign-in closes its layer and opens the destination surface; an editor field shows `SAVED` in the bar for 2 seconds.
107. A rejection is never a lost form. A field-level rejection marks the offending fields in the warm sand colour with the server's messages below them, keeps every value and moves focus to the first. A form-level rejection shows the server's message in the response line and keeps every value. A network failure shows `It looks like something went wrong. Please try again.` and keeps every value. A rate limit shows `Too many tries. Give it a minute.` and disables submit for the remaining window, counting down in small type. A conflict on save offers the side-by-side resolution.
108. Every form writes its values into browser storage whenever a field is left, under a key per form (the enquiry under `enquiry_draft`), and restores them on load if the form was not successfully submitted; storage for that form is cleared on success. A reload in the middle of a long enquiry loses nothing. A newsletter address is never stored.

### Empty, loading, error and offline states

109. Every surface and every collection has a loading, an empty, an error and an offline face, each one of four shared layouts, and no status code is ever shown to anyone. The four layouts: the centred notice (a large heading, a shorter line of at most 60 characters under it, and at most one control, with no illustration and no icon); the inline notice (one small grey line inside a block); the skeleton (the collection's own layout with each item replaced by a plain dark block of the item's size, with no shimmer and no pulse, held for at least a fifth of a second once shown so a fast answer does not flash); and the bar message.
110. The state copy, surface by surface:
    - Home screen: loading is the arrival sequence; an error falls back to the static crystal and the bar reads `REDUCED GRAPHICS`; offline changes nothing.
    - Studio story: loading is a skeleton over the client and award rows; empty is the inline notice `The roster is being updated.`; error is `That did not load.` / `We could not fetch the studio's page.` / `TRY AGAIN`; offline is `You are offline.` / `This page needs a connection. The work you have already opened still works.` with no control.
    - Work carousel: skeleton of twelve title blocks; empty `Nothing published yet.` / `The studio has not put any work up.` / `GET IN TOUCH`; error with `TRY AGAIN`; offline as above.
    - Project grid: skeleton of six tiles; empty `Nothing here yet.` / `No work in this category yet.` / `SEE ALL WORK`; error with `TRY AGAIN`.
    - Case file: skeleton of the header and three chapter blocks; error `That did not load.` / `We could not fetch this case file.` / `BACK TO THE WORK`; not found `Not here.` / `This piece is not published, or it never was.` / `SEE ALL WORK`.
    - Showreel: the poster with a dimmed play control and the turning ring while loading; empty `No reel yet.` / `The studio has not put a reel up.` / `SEE THE WORK`.
    - Contact: skeleton over the two office blocks; offline replaces the enquiry form with the inline notice `Your message is saved here and will send when you are back.`.
    - Notice page: skeleton over the rows; empty inline notice `The notice is being updated.`.
    - Newsletter strip: the ring in the submit while loading; the failure copy on error; the inline notice `You are offline.` offline.
    - Console case file list: skeleton of eight rows; empty `Nothing yet.` / `No case files. Start one.` / `NEW CASE FILE`; offline adds `Anything you were writing is still on this device.`.
    - Console editor: skeleton over the fields; errors inline per field; offline the editor stays writable, saves queue, and the bar reads `OFFLINE, SAVING LATER`.
    - Chapter arranger: empty `No chapters yet.` / `Add something to arrange.` / `BACK TO THE EDITOR`.
    - Review queue: skeleton of four rows; empty `Nothing waiting.` / `No case files are with you for review.` / `SEE ALL CASE FILES`.
    - Grid arranger: skeleton of six tiles; empty `Nothing published.` / `Approve something first.` / `SEE ALL CASE FILES`.
    - Enquiry inbox: skeleton of eight rows; empty `No enquiries.` / `Nobody has written yet.` / `SEE THE CONTACT PAGE`.
    - Shortlist: skeleton of three tiles; empty `Nothing saved.` / `Open a case file and keep it here.` / `SEE ALL WORK`; offline renders the shortlist kept in the browser.
111. Once the site has loaded, moving between surfaces already loaded keeps working with the network off; what fails is anything that needs the server. Connectivity is judged from the browser's own signal plus a request that fails after two retries. The bar reads `OFFLINE` when the connection is lost and `BACK ONLINE` when it returns. Console saves made offline are queued in order and replayed oldest first on reconnection, stopping at the first failure, and the bar reads `SAVED WHAT YOU MISSED`. The enquiry's values are kept and sent when the connection returns. Anything already fetched stays readable, and the bar reads `SHOWING WHAT WE HAD` on first interaction.
112. A browser too old to draw the graphics shows the centred notice `This browser is too old.` / `The site needs a newer browser to draw its graphics.`.

### Search, filter and sort

113. One query model serves the public grid, the console case file list and the enquiry inbox, and every parameter lives in the address, so a filtered view can be linked and shared. Parameters: `sector` (grid and case file list; one of the seven tokens or `all`), `state` (case file list; one of the five states or `all`), `owner` (case file list; an account id or `all`), `q` (case file list and inbox; free text of 2 to 60 characters), `enquiry_state` (inbox; `new`, `assigned`, `answered`, `archived` or `all`) and `sort` (`order`, `newest`, `oldest` or `title`; default `order` on the grid and `newest` elsewhere). A parameter at its default is left out of the address. Changing a filter replaces the history entry rather than adding one, so ten filter changes are one back press, and the back press from the grid returns to the carousel.
114. The public grid takes `sector` and `sort` only; there is no public text search. An unknown sector token is refused as invalid with `Pick a sector.`.
115. Filters intersect and never add up: `sector` with `state` gives case files in that sector and that state; `sector` with `q` gives case files in that sector whose title or client matches; `state` with `owner` gives that account's case files in that state. A combination with no results shows the empty layout with one control `CLEAR FILTERS`, which resets every parameter at once. Two filters that cannot both hold produce the empty state, never an error.
116. Free text searches the title and client of case files, and the name, organisation and brief of enquiries. Matching ignores letter case and accents and matches whole words and word beginnings. Title beginnings rank first, then title matches, then client matches, then brief matches. Below 2 characters the parameter is dropped. The search settles for a moment after the last keystroke before it runs, rather than firing on every keystroke, and the matched run is highlighted in the warm sand colour.
117. `order` is the grid position an editor set, ascending; `newest` is publication time descending on the public grid and last update descending in the console; `oldest` is the reverse; `title` is alphabetical, ignoring accents, with numbers before letters.

### Live updates and instant actions

118. The public site opens no live connection of any kind. In the console: a case file submitted by an author appears in an editor's review queue within 5 seconds without a reload; a row's state changes in the case file list when somebody else moves it; a new enquiry appears in the inbox within 5 seconds and the bar reads `NEW ENQUIRY`; and the presence line of rule 85 appears when a second person opens the same case file.
119. Adding to or removing from the shortlist, reordering chapters, reordering the grid and marking an enquiry read appear at once and are confirmed afterwards. A field save, a submit, an approval, a publish, an unpublish and any form submission always wait for the server, because nobody is shown that their work is live until it is.
120. An instant action that turns out to have failed visibly undoes itself, running back at the same speed and with the same easing as the action it undoes, and the bar says so: `NOT SAVED` for the shortlist and for a read mark, `ORDER NOT SAVED` for chapters, `GRID ORDER NOT SAVED` for the grid. A rollback is never silent and never a dialogue.
121. The server's answer always replaces the local state, even when they match. On a version conflict the local state is discarded, the server's adopted, the rollback shown, and a reorder re-reads the whole order rather than patching it. On a network failure the local state is kept and the action queued. Two orderings are never merged: an ordering is replaced whole or not at all.

### Messages and notices

122. In the app there are exactly three places a message appears: the bar (anything that needs no answer), the inline notice (anything attached to one block) and the pinned note (anything that must not be missed, in full-size reading type with its label in the warm sand colour, such as a returned case file's note, the presence line, or `You will be signed out in five minutes. Anything you have typed is saved.` for an author or editor). There is no notification centre, no badge count and no toast stack.
123. There is no mail service in this environment, so the product sends no email. Instead it writes exactly seven kinds of message, each stored once per event as a record addressed to an email address, readable by that account at `GET /api/messages` and by every editor in the outbox at `GET /api/studio/outbox`, each with a subject under 60 characters, a plain-text body, and at most one link:
    - `Confirm your address` (sign-up): one line, one link to `/verify`, the 7 day expiry stated.
    - `Reset your password` (reset requested for an existing address): one line, one link to `/reset`, the 60 minute expiry stated.
    - `Kelo has invited you` (an editor invites an account): who invited them, the role, one link to `/invite`, the 14 day expiry stated.
    - `<title> needs changes` (a case file is returned), to its author: the note verbatim, one link to the editor.
    - `<title> is live` (a case file is first published), to its author: one link to the public address. Publishing changes writes no message.
    - `We got your message` (an enquiry is submitted), to the sender: what they wrote and the two working day promise.
    - `Enquiry from <name>` (an enquiry is submitted), to every editor: every field of the enquiry and one link to `/studio/enquiries`. The sender's brief is plain text, and any web address in it is rendered inert by writing its `://` as `[:]//`, so nothing in it is a link the sender controls.
124. No message contains a password, a session token or any other secret. Every message names the studio and gives one way to reach a person (`newwork@kelo.example.com`). Nothing else ever writes a message: no batching, no digest, and nothing for an action the person just took on a surface they are looking at (a saved field, a reorder, a shortlist change), because the bar already told them.

### Persistence and migration: the shortlist, stored preferences and the seed

125. A signed-out visitor's shortlist lives in browser storage under the key `shortlist`. A signed-in visitor with a verified address keeps it on the server (`PUT` and `DELETE` on `/api/shortlist/{case_file_id}`, both repeatable with the same result, `GET /api/shortlist` to read); only a published case file can be shortlisted; an unverified visitor's server shortlist writes are refused.
126. A visitor who saved case files while signed out keeps all of them on signing in: the local shortlist is merged into the server's on the first signed-in request (`POST /api/shortlist/merge`), as a union ordered by the local save time, a duplicate is not an error, and the local copy is then cleared.
127. Browser storage is a convenience and never the truth. Every stored key is read defensively: a missing key, an unreadable store and a value of the wrong shape all resolve to the default with no error shown. A private window with storage blocked renders the site correctly with sound off, the crystal at its default angle and the counter at zero. The last sector filter is kept in the address and, as a fallback, in browser storage; reduced motion is always read from the system and never stored; the locale is kept under `locale`.
128. A first run produces a site that looks like a site: the seeded accounts, the seven sectors in order, the twenty-nine clients in their groups, the fourteen notice rows, the six studio awards, and three example case files that are published at grid positions one to three with four chapters of four different kinds each. While those seeded examples exist, an editor is offered `REMOVE THE EXAMPLES`, which deletes all three with their chapters; this is the only way a published case file is ever deleted.

### Destructive actions

129. Four actions destroy something, and each is handled where it happens; there is no general confirmation dialogue:
    - Deleting a case file (editor, only while never published): the row's `DELETE` control changes to `REALLY?` in the bright yellow for 4 seconds, and a second press within them deletes the case file, its chapters, its information items and its awards. Not recoverable. Deleting a published case file is refused as a conflict.
    - Removing the examples (editor): the control says what it does and needs no confirmation. Not recoverable.
    - Deleting an account (the holder, or an editor): the request must carry the account's own display name as `confirm_display_name`. Case files the account owned move to the editor who deleted it (or, for a self-deletion, to the longest-standing editor) and record the original author's display name, so history survives a person leaving. Not recoverable.
    - Unpublishing (editor): nothing is destroyed; the state changes and the address stops resolving. Recoverable by publishing again.
130. The bright yellow appears nowhere else in the product: only for the 4 seconds a delete is armed.
131. Deleting a sector is refused while any case file or client entry uses it; an editor must move that work first. A chapter written by a newer version of the site is shown by its first text field with the inline notice `This chapter needs a newer version of the site.`. An editor can export every entity as one structured document (`GET /api/studio/export`), which is the way off this product.

### Internationalisation and formatting

132. The source locale is English and is declared on the document; the visitor's stated preference comes first, then the browser's, then the source locale; the choice is kept in browser storage and on the account when signed in; a locale control in small type at the foot of the menu lists locales by their own names; a missing string falls back to the source locale, never to a key or an empty string.
133. Dates: an absolute date reads day, month name, year (`4 March 2027`). Relative times read `just now` under a minute, whole minutes under an hour (`12 minutes ago`), whole hours under a day (`5 hours ago`), whole days under a week (`3 days ago`), and the absolute date beyond. Numbers group by thousands in the locale's own separator (`12,400`). Budget bands use the locale's currency symbol and grouping with the bands unchanged (`£25,000 to £50,000`). Telephone numbers and postal addresses are never reformatted.
134. Long translated strings are bounded, never allowed to simply overflow: the three menu words drop one type step when the widest runs slightly over, and wrap to two rows of a smaller step when it runs well over, with the layer re-centred; the wordmark keeps its size and breaks where the translator breaks it; a client sector label truncates with an ellipsis and carries its full text as a title, never wrapping; the close control widens to fit, keeping its offset from the right edge, and never wraps or truncates; a carousel title shrinks to the archive title size and then truncates; a grid caption wraps to a third line and the tiles below make room; an award name wraps to two lines and the row stays bottom-aligned; a bar message is capped at 24 characters when written.
135. For a right-to-left locale five things mirror: the corner controls swap sides with their catchments, the close control moves to the top left with its divider on its left, the carousel's previous and next arrows swap, a text chapter swaps its label and copy columns, and the notice page swaps its label and copy columns. The crystal does not mirror.

### Link previews and the preview image

136. The document the server returns for every public address (`/`, `/story`, `/work`, `/work/all`, `/work/<case-file-slug>`, `/reel`, `/contact`, `/notice`) already carries that address's own `<title>`, an `og:title` and an `og:image` in its head before any script runs, because a link-preview fetcher runs no script. `og:image` is an absolute address on the app's own origin that answers with a generated image: `/api/preview/<case-file-slug>.png` for a published case file and `/api/preview/site.png` for every other public address. Both are drawn by the app from the product's own palette and are never shipped files. A case file's `og:title` is its title followed by ` · Kelo`.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home screen: crystal, wordmark, four corner controls. The menu opens here and the address stays `/` | none |
| `/story` | Studio story layer | none |
| `/work` | Work carousel layer, the first twelve published case files in grid order | none |
| `/work/all` | Project grid layer; `?sector=<token>` and `?sort=<order>` | none |
| `/work/<case-file-slug>` | One published case file | none |
| `/reel` | Showreel layer | none |
| `/contact` | Contact layer with the enquiry form and the newsletter strip | none |
| `/notice` | Privacy notice layer | none |
| `/join` | Visitor sign-up | none |
| `/verify` | Confirms an address from its link, `?token=<token>` | none |
| `/invite` | Accepts an invitation and sets a password, `?token=<token>` | none |
| `/reset` | Requests a reset, or completes one with `?token=<token>` | none |
| `/shortlist` | The visitor's shortlist | visitor, or the browser's own list when signed out |
| `/studio/sign-in` | Sign-in layer, heading `Studio`, `?next=<path>` | none |
| `/studio` | Case file list; `?state=`, `?owner=`, `?sector=`, `?q=`, `?sort=` | author, editor |
| `/studio/case/<case-file-id>` | Case file editor with the chapter arranger and the publication block | the owning author, editor |
| `/studio/review` | Review queue | editor |
| `/studio/grid` | Grid arranger and sector taxonomy | editor |
| `/studio/enquiries` | Enquiry inbox; `?enquiry_state=`, `?q=`, `?sort=` (for example `/studio/enquiries?enquiry_state=new&q=museum`) | editor |
| `/studio/outbox` | Every stored message | editor |
| `/studio/site` | Client roster, notice rows, accounts and their roles, export | editor |
| `/studio/account` | Own account, sessions, messages, shortlist and enquiries | any signed-in account |

**Entry and redirects.**

- No gated surface ever renders and then disappears: each resolves who is asking before its first paint.
- Signed out, any `/studio` address other than `/studio/sign-in` redirects to `/studio/sign-in?next=<that path>` (for example `/studio` goes to `/studio/sign-in?next=/studio`). `next` is honoured only when it is a path on this origin beginning with exactly one `/` and not `//`; anything else is discarded and sign-in proceeds to `/studio`.
- Signed in as a visitor, `/studio`, `/studio/case/<case-file-id>`, `/studio/review`, `/studio/grid`, `/studio/enquiries`, `/studio/outbox` and `/studio/site` show the denied surface; `/studio/account` shows the account surface.
- Signed in as an author, `/studio` shows the case file list, `/studio/case/<case-file-id>` shows the editor only for their own case file, and `/studio/review`, `/studio/grid`, `/studio/enquiries`, `/studio/outbox`, `/studio/site` and another person's case file show the denied surface.
- The denied surface is a written page, never a status code and never a blank page: the heading `Not for you`, the line `This part of the site belongs to the studio. If you think it should belong to you as well, ask whoever runs it.` and one control `BACK TO THE WORK`.
- `/work/<case-file-slug>` for a case file that is not published shows the not-found surface (`Not here.`) to everyone, including an unknown slug such as `/work/does-not-exist`, and the address is left unchanged. Its owner and editors preview it inside the studio.
- After sign-in the layer closes and `next` (or `/studio` for an author or editor, `/` for a visitor) opens. Sign-out returns to `/`.
- An expired session mid-edit opens the sign-in layer over the console, as in rule 17.
- Deep entry to any address opens that layer with the crystal already at rest and skips the arrival sequence; the back control closes the open layer.

**Journeys.**

1. **The public path.** Open `/`; the wordmark reads `Kelo · Creative Studio` over `Since 2011` and the page does not scroll. Point near the top-right corner; `Discover` appears. Activate it; `About`, `Work` and `Contact` arrive. Activate `About`; `/story` shows `Making the story move.` and `Selected Clients`, with `Technology & Futures` as the first sector row. Activate `Close Story`; the address is `/` again.
2. **Work and a case file.** Open the menu and choose `Work`; `/work` shows the first twelve published titles in grid order, laid out in depth, and the drag mark draws itself on. Activate `View All Projects`; `/work/all` shows `Filter` and the sector list. Choose `Automotive`; the tiles restack and the address carries `sector=sector-6`. Open a tile; `/work/<case-file-slug>` shows its title and description. Scroll to the end; `LAUNCHED AT` and the `NEXT` case file's title appear. Activate `Close Project`; the filtered grid returns at `/work/all?sector=sector-6`. Press the browser's back control; `/work` returns. Paste `/work/glass-harbour` into a fresh browser; `Glass Harbour` opens with no arrival sequence.
3. **Contact, notice and newsletter.** Choose `Contact`; `/contact` shows `Contact` and `newwork@kelo.example.com`. Activate `PRIVACY`; `/notice` shows `Kelo Customer Privacy Notice`. Activate `Close Notice`; `/contact` returns. Press `SEND` on the empty enquiry form; `We need a name to reply to.` and `We need this to be able to reply.` appear and nothing is stored. Fill `Your name`, `Your address` and a `What you want made` of 39 characters, tick consent and send; `Tell us a little more, forty characters at least.` appears. Extend the brief and send; `Thank you.` and `We read everything and answer within two working days.` replace the form. Activate `DISPATCH`, enter an address and send; `Thanks! You are now subscribed.` appears.
4. **The authoring path.** Open `/studio` signed out; the sign-in layer `Studio` opens at `/studio/sign-in?next=/studio`. Sign in with a wrong password; `That combination is not one we know.` appears. Sign in as `editor@example.com`; `NEW CASE FILE` is shown. Invite an author, open the invitation link in a fresh session, set a password and sign in as that author. Open `/studio/review`; `Not for you` appears. Return to `/studio` and activate `NEW CASE FILE`; `Untitled` opens. Activate `SUBMIT FOR REVIEW`; `Give it a title.` and `A case file needs at least one chapter.` are listed and the state stays `draft`. Set the title to `The Long Room` and leave the field; `SAVED` shows and the slug becomes `the-long-room` (or `the-long-room-2` if that address is taken). Save a client, the sector `Automotive` and a description of more than forty characters. Add a `headline`, a `text` and an `image` chapter with an uploaded picture; open the arranger and drag the third chapter to the top; `ORDER SAVED` shows. Activate `SUBMIT FOR REVIEW`; `WITH THE EDITOR` shows.
5. **Review and publication.** Sign in as `editor@example.com` and open `/studio/review`; `The Long Room` is listed. Activate `RETURN` with a note of twelve characters; `The Long Room` leaves the queue and `Quiet Engine` stays listed. Sign in as the author and open the case file; the note is pinned above the header. Change the description and submit again; `WITH THE EDITOR`. Sign in as the editor and activate `APPROVE`; `The Long Room` leaves the queue. Open the case file and activate `PUBLISH`; `LIVE` shows.
6. **The public sees it, then sees it change.** In a fresh browser with no session, open `/work/all`; `The Long Room` is listed. Filter to `Automotive`, open it and read its first chapter. As the author, change the description and leave the field; `SAVED` shows. Reload the case file in the fresh browser; the old description still shows. As the author, activate `PUBLISH CHANGES`; `LIVE` shows. Reload in the fresh browser; the new description shows.
7. **Permissions.** As an author, open `/studio/grid`, `/studio/enquiries` and `/studio/site`; each shows `Not for you` and `BACK TO THE WORK`. As the editor, open `/studio/enquiries`; the enquiry from journey 3 is listed with its sender's name.
8. **Taking work down.** As the editor, take `The Long Room` down from the grid arranger; `TAKEN DOWN` shows. In the fresh browser, open its address; `Not here.` shows. Filter the grid to a sector with nothing published; `Nothing here yet.` and `SEE ALL WORK` show; `SEE ALL WORK` returns the grid to `/work/all`.
9. **Keyboard alone.** Open `/` and press Tab four times; each corner control's name appears in turn (`Discover`, `Showreel`, `Audio`, `Drop`). Tab back to `Discover` and press Enter; the menu opens. Press Tab to `About` and Enter; `/story` opens. Press Escape; `/` returns. Reach the enquiry form on `/contact` by keyboard alone and send it; `Thank you.` appears.
10. **A visitor's shortlist.** Open `/join` and create an account; `CONFIRM YOUR ADDRESS TO GET A REPLY` shows above the enquiry form and the account surface lists `Confirm your address`. Follow its link; the address is confirmed. Open a case file and keep it; `/shortlist` lists it.

**States.** Every list has an empty state and every surface a loading state, both from the four shared layouts in `## Core features`. Errors never crash the app and never show a status code. With browser storage blocked, `/` still shows the wordmark with sound off and the counter at zero. With the network off, moving between loaded surfaces still works and the bar reads `OFFLINE`.

## UI/UX notes

The north star is the studio's work seen one piece at a time over a dark, still ground with one turning object. The register is editorial and atmospheric on the public site, where the subject comes first and there is almost no interface; the console is the same site with working things on it, quiet and dense but organised, built for the studio's own people whose taste the site advertises.

The character is near-black, weightless and quiet: stillness over decoration, space over dividers, type over colour. The product commits to one dark mode, designed fully; there is no light theme. The palette is set by role. The page is a near-black neutral, and the crystal's layer is a second near-black neutral a hair warmer, close enough that the seam between them never shows and far enough apart that the object reads as lit from inside. Three further near-blacks exist for filled controls and a lifted surface, and they are ordered strictly: the further a surface sits from the page, the lighter its near-black. Section rules are a deep neutral. Almost all type is a near-white neutral; long reading text is a slightly softer near-white neutral; secondary copy is a mid neutral; the bar message is a dimmer mid neutral; a hairline or a device frame is a light neutral. A ground tone is never used for type, and a type tone is never used for a fill.

Exactly one warm colour exists: a light, soft orange, a warm sand. On the public site it appears only inside the privacy notice, for the phrase that matters and for a link being pointed at; in the forms and the console it marks what needs attention (an invalid field, a failed save, a held field, a pinned note's label, a search match). A bright, vivid amber yellow appears only for the few seconds a delete is armed. Nothing else in the product is coloured, and the page is never dominated by one hue family with no second signal: meaning never rides on colour alone. Success carries no colour of its own: a saved field, a sent enquiry and a published case file are said in words, in the interaction bar or in the form's response line, in the same near-white as the rest of the type. The exact shades are yours, so long as those relationships hold.

Type does the work colour usually does. The whole product is set in `Inter` in four cuts, falling back to `Arial, sans-serif`: an extralight cut for display, a light cut for reading, a regular cut for labels and a medium cut for emphasis, each cut carrying the surfaces named for it in `## Front-end specification`, where the ramp is set out size by size. The register changes by weight and size, never by colour, and the three registers stand clearly apart: display type towers over reading type, reading type over the labels, with no size used to blur one band into the next, so the pages read as composed rather than filled in. Labels are small spaced capitals; the three menu words stay in sentence case.

Shape is flat: no card, no panel and no border anywhere; only round controls are rounded; one soft shadow exists, on a case file media block. Density is spacious on the public site and comfortable in the console. Two gaps do almost all the layout work: a large gap that always comes with a thin rule and means a new thought starts, and a smaller gap with no rule that means the same thought continues. Links are underlined twice over: a faint line always present, and a bright line that draws itself across it when pointed at.

Every component has resting, pointed-at, pressed, focused and unavailable states. Corner controls show their names only on approach; a pressed mark shrinks; Escape closes the topmost layer; a destructive action arms itself before it acts; an unavailable control is never signalled by colour alone. There is one primary action on each surface, visually distinct from every secondary one: on the contact surface it is `SEND`, in the console list it is `NEW CASE FILE`, in the editor it is the submit or publish control, and on the home screen it is the crystal itself.

The motion character is eased and quiet: everything moves at one of three speeds, quick for a control under the pointer, slightly slower for a control the pointer is near, and slower again for content that moves, and nothing drifts, pulses or loops on its own except the crystal. Opacity is the default verb: things fade into place rather than sliding in from the edges, a reveal is never slow, only one property moves at a time, and the main easing leaves quickly and arrives softly so a panel feels placed rather than thrown. Every animated moment has a reduced-motion form that honours the system preference, keeps every surface reachable and resolves to a legible end state at once: things arrive without travelling, the crystal holds a fixed angle, and a fade that carries state is kept rather than removed.

Accessibility is a floor, not a style. Text and its ground meet WCAG AA contrast, interactive targets are comfortably large (at least 44px in each direction, satisfied everywhere by the catchment construction), keyboard navigation reaches everything with a visible focus treatment that never relies on colour alone, every icon-only control has a text label, every surface has one first-level heading (visually hidden where the design shows none), and reading surfaces allow text selection so an address or a case file's text can be copied.

The layout is responsive across every width between a phone held upright and a very wide monitor, with five breakpoint tiers: narrow, mid, wide, wider and widest. Every public surface works at every width, nothing scrolls sideways at any viewport, the corner controls stay corner controls, their catchment shrinks but never below a comfortable thumb target, type never drops below the small label and body sizes, and the crystal is never hidden.

## Technical requirements

The rendering model is a single-page application over a JSON API: the browser receives one HTML document and one script bundle and renders every surface as a layer over the home screen, and the server answers every public address with that document, already carrying the address's own title and link-preview tags. Build the front end with **Vue 3**, **Vue Router** and **Vite**, served as a production build, and the HTTP API with **NestJS** on its Express platform, in TypeScript, on the same origin under the `/api` prefix. Persist to **PostgreSQL** (the `postgres` service), reached at `DATABASE_URL`, through **pg**. Store every uploaded byte in **MinIO** (the `minio` service), reached at `STORAGE_ENDPOINT` with `STORAGE_BUCKET`, `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY`, through **@aws-sdk/client-s3**. Render the crystal with **three**. Hash passwords with **argon2**. Clean the notice body with **sanitize-html**. The app's own address and port come from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode a host or a port; read every one of them from the environment. Both backing services are **already running** and reachable at those variables and must not be downloaded, installed, compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database, cache, queue, object store, identity provider or mail vendor - the only backing services available in this environment are PostgreSQL and MinIO, and reaching for anything else is a contract violation.

Authentication is app-implemented email and password with bearer tokens, as in `## Core features`. `GET /api/health` returns `200` once the app is ready. Request logs go to standard output, one line per request, carrying the method, the path, the status and the duration.

**No credential, API key, bucket secret or admin token appears in anything the browser downloads**: not in the served HTML, not in any script or stylesheet, not in any response to an unauthenticated request. The storage credentials are read on the server and never reach the client.

**Security headers.** Every response carries the standard security headers:

- `Strict-Transport-Security` with `includeSubDomains`;
- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options: DENY`, so framing is denied;
- `Referrer-Policy: same-origin`;
- a `Content-Security-Policy` that names only the app's own origin (which serves the pages, the API, the case file media and the reel), allows no inline script and no eval, and denies framing with `frame-ancestors 'none'`.

The API is not a public interface: requests from another origin are not served. Any cookie the app sets is http-only and same-site strict, with no domain-wide scope.

**Rate limits.** Exceeding a limit answers a rate-limit refusal whose body carries `retry_after` in seconds, and the surface shows `Too many tries. Give it a minute.` counting down. Traffic reaches the app from one shared network origin, so each limit is keyed on the email address the request names:

- sign-in: 5 failed attempts per account per 15 minutes;
- sign-up (`POST /api/auth/signup`): 3 per address per hour;
- reset requests (`POST /api/accounts/resets`): 3 per address per hour;
- enquiries (`POST /api/enquiries`): 3 per sender address per hour;
- newsletter subscriptions (`POST /api/subscribers`): 5 per address per hour;
- public case file reads (`GET /api/case-files` and `GET /api/case-files/{slug}`): 240 per minute per network address;
- every console write: 120 per minute per account;
- each ordering route: 30 replacements per minute per account.

**Input handling.** Every text field is trimmed, stripped of control characters, length-checked, stored as text and never as markup. Sanitising on input and escaping on output are both required; neither alone is enough. Markup typed into a case file title is shown as visible text. A script address in a notice link is dropped and its text kept unlinked. A brief of 4001 characters is refused on the page and by the server. A sector token that does not exist is refused with `Pick a sector.`. A stale `version` is refused as a version conflict. A path traversal attempt in a slug answers not found and is recorded as an `error_shown` event. One very long unbroken word in a case file body wraps rather than widening its column. A slug is generated, never accepted from a request, except from an editor, and then only when it matches lowercase letters, digits and hyphens, 2 to 80 characters. The enquiry form cannot be used as a relay: the editors' copy of an enquiry never carries a link the sender controls.

**Analytics.** Only named events are recorded, and they are recorded by the app itself: the page sends them to `POST /api/events` on its own origin after the arrival sequence completes, no vendor key or measurement identifier appears anywhere, and nothing is sent to a third party. The server accepts only these events and stores only each event's named properties, dropping anything else before storage:

- `site_opened` (`referrer_class`, `viewport_class`, `reduced_motion`, `webgl_available`), `arrival_completed` (`duration_ms`, `assets_ready`), `arrival_timed_out` (`duration_ms`, `missing`, when the arrival overlay hits its ceiling);
- `crystal_dragged` (`angle_delta`, `duration_ms`), kept for one drag in ten because it fires constantly by design; `crystal_reseeded` (`count_total`); `sound_toggled` (`to`);
- `menu_opened` (`from_surface`), `menu_word_chosen` (`word`), `surface_opened` (`surface`, `from_surface`, `entry`), `surface_closed` (`surface`, `dwell_ms`, `method`);
- `carousel_dragged` (`items_travelled`), `grid_filtered` (`sector`, `result_count`), `case_file_opened` (`slug`, `sector`, `from`), `case_file_read` (`slug`, `dwell_ms`, `chapters_seen`, once per case file per session, when its footer enters the window), `chapter_interacted` (`slug`, `kind`, `position`, `action`: a video plays, a split drags, a device scrolls, an image expands);
- `reel_played` (`from_surface`), `reel_completed` (`duration_ms`), `shortlist_changed` (`slug`, `to`, `signed_in`);
- `enquiry_started` (no properties, on the first keystroke), `enquiry_submitted` (`has_organisation`, `budget`, `sector`, `brief_length_band`), `enquiry_failed` (`reason`), `newsletter_submitted` (none), `newsletter_failed` (`reason`);
- `signed_in` (`role`), `signed_out` (`all_devices`), `case_file_created` (none), `case_file_submitted` (`chapter_count`, `days_in_draft`), `case_file_returned` (`note_length_band`), `case_file_approved` (`days_in_review`), `case_file_published` (`days_from_draft`), `case_file_republished` (`days_since_published`), `save_failed` (`field`, `attempt`, `reason`);
- `offline_entered` and `offline_left` (`duration_ms`), `error_shown` (`surface`, `error_token`, `status`).

Never sent: a brief, a note, case file body text or any enquiry text (only length bands); an email address, a display name, a telephone number or a postal address; an account id on a public-site event (console events carry a role, not a person); any third-party or cross-site identifier; anything before the visitor has been told, which the privacy notice does. Surface, conversion, chapter and error events are kept for every occurrence. An editor reads stored events at `GET /api/studio/events`. The reseed counter is a toy on the visitor's own device and is never sent anywhere.

**Performance.** Budgets, measured on a mid-range laptop over a 10 megabit connection with 70 milliseconds of latency and on a mid-range phone over 5 megabits with 150:

- the home screen paints within 1.2 seconds, is interactive within 2.5, and transfers at most 320 kilobytes on a first visit (40 on a repeat), covering the document, the design values, the shell, and the crystal's renderer and geometry, and nothing else;
- the menu is already loaded and responds within a tenth of a second;
- the studio story paints within 0.4 seconds (18 kilobytes), the carousel and the grid within 0.5 (24 and 12 kilobytes plus posters), a case file within 0.6 (30 kilobytes plus media), the reel's poster within 0.8 (40 kilobytes plus the film), contact within 0.3 (8 kilobytes), the notice within 0.5 (46 kilobytes), the console list within 0.6 (28 kilobytes) and the console editor within 0.7 (44 kilobytes).

The crystal holds a smooth frame rate while idle and while dragged, with the rotation following the pointer within about a thirtieth of a second; the carousel drag, the grid restack and the split drag hold the same rate; every other surface draws nothing continuously once revealed. What is deferred: sound, posters, case file media, the reel's film, the notice body, the whole console and the analytics wait until they are asked for, in that order of need: the carousel's two nearest posters first, grid posters above the fold first, a case file's media per chapter on approach, the console only once a studio session exists, analytics after the arrival sequence. What is preloaded: the four type cuts are the only fetch that blocks rendering, the icon set is inline in the document, the crystal's renderer and geometry arrive with the document, the first surface named in a deep-entry address arrives with the document, and the carousel's first three posters arrive when the site is idle after arrival; the five type cuts the reference declared but never used are never fetched.

When frames run long for a full second, measured over a rolling two-second window, the crystal steps down one rung at a time and never back up within a session: first the colour fringe takes two passes instead of three; then the facet count halves from forty-eight to twenty-four (also the default at the narrow tier); then the idle rotation halves while dragging stays fully responsive; then the rotation stops and the bar reads `REDUCED GRAPHICS`; then the object is replaced by its static drawing, again with `REDUCED GRAPHICS`. The visitor is told once, at the first rung that changes what they see. While a heavy surface is open, the idle rate drops rather than the surface being made to wait. Two costs are specific to this design: the crystal never unloads, so every surface pays for it, which is why the idle rate can drop; and the notice page is the single largest text payload, behind two actions from contact, never part of another surface's budget and never preloaded.

**Module boundaries, as observables.** The design values (every colour, type step and spacing step) live in one place and nothing else writes a literal of its own. The icon set, the motion table, the crystal, the sound layer, the shell (one instance each of the close control and the archive control, four corner controls, and two paging arrows and three menu words in the surfaces), the layer stack with the address model, one component per public surface, one component per chapter kind, the forms, the four state layouts, the API client with its error body and offline queue, the console, and the event recorder are separate parts, and dependencies only point downward. Chapter kinds form a registry: each kind registers its renderer, its editor, its validator and its payload version, so a ninth kind (the image-sequence kind the reference started and never finished, whose only trace was a half-transparent blue placeholder ground) could be added with one file and one registration. The crystal exposes only rotate, reseed, set idle rate and read angle. Reduced motion is resolved once, where motion is defined. The shell is the only writer to the interaction bar. The crystal and the sound layer are single long-lived layers that outlive every surface: after twenty navigations the crystal turns as smoothly as on the first load and still remembers the visitor's angle.

**Observed implementation, informational only.** The captured reference used a three-dimensional scene library with an effect composer for post-processing, buffer geometry and custom shader source, a text-splitting plugin, a video player, an audio playback library and a serialisation shim (each known from its licence banner or from identifiers surviving in its bundle), and the browser's audio context. None of that observed implementation is a requirement; every capability those libraries served is stated above as a requirement.

## Data model

Nineteen tables. All timestamps are UTC. Every table has an integer `id`.

> **Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a secret. Hash it as normal; the exact literal must work at login, and it must be written into `/app/USER_README.md` alongside each account so a grader can sign in.

- **`account`**: `email` (lowercased, unique), `display_name` (2 to 80), `password_hash` (never returned), `role` (`visitor`, `author` or `editor`, default `visitor`), `email_verified_at` (a nullable timestamp), `verification_deadline` (sign-up plus 7 days while unverified, otherwise null), `previous_email`, `previous_email_until` (an email change plus 30 days), `created_at`, `updated_at`, `last_seen_at` (updated when a session is used, at most once a minute). An account's public shape is `id`, `email`, `display_name`, `role`, `email_verified` (true or false), `verification_deadline`, `previous_email`, `previous_email_until`, `created_at`.
- **`account_session`**: `account_id`, `token_hash`, `created_at`, `last_used_at`, `expires_at` (created plus 30 days for a visitor, plus 12 hours for an author or editor), `idle_timeout_seconds` (null for a visitor, `7200` for an author or editor), `revoked_at`.
- **`account_token`**: `account_id`, `purpose` (`verify` or `reset`), `token_hash`, `expires_at`, `used_at`.
- **`invitation`**: `email`, `role`, `display_name`, `token_hash`, `invited_by`, `created_at`, `expires_at` (created plus 14 days), `accepted_at`.
- **`sector`**: `token` (unique lowercase kebab, for example `sector-3`), `label` (1 to 24), `position` (unique).
- **`client_entry`**: `sector_id`, `name` (1 to 40), `position` (unique within its sector).
- **`case_file`**: `slug` (unique when set, null until the first title save), `title` (default `Untitled`), `client`, `sector_id`, `description`, `launch_url` (nullable text that must parse, secure scheme only), `state` (default `draft`), `owner_id`, `original_author_name`, `submitted_by`, `submitted_at`, `reviewed_by`, `self_approved`, `return_note`, `returned_at`, `approved_at`, `published_at`, `position` (set, and unique among published case files, only while published; null otherwise), `draft_payload` (the pending copy, or null), `version` (starts at 1 and increases on every write), `seeded` (true only for the three examples), `slug_changed`, `created_at`, `updated_at`.
- **`chapter`**: `case_file_id`, `kind`, `position` (unique within its case file), `payload` (structured, shaped by the kind), `payload_version`, `version`.
- **`information_item`**: `case_file_id`, `heading`, `value`, `position` (unique within its case file; at most six per case file).
- **`award`**: `case_file_id`, `name`, `mark`, `position` (unique within its case file).
- **`case_media`**: `case_file_id`, `key` (the bucket key), `content_type`, `size_bytes`, `sha256`, `created_at`. It holds no bytes.
- **`slug_redirect`**: `old_slug` (unique), `case_file_id`.
- **`retired_slug`**: `slug` (unique): every slug ever issued, kept after a delete so it is never issued again.
- **`notice_row`**: `label`, `body`, `position` (unique), `updated_at` (set on every save and shown at the foot of the page).
- **`enquiry`**: `account_id` (set only for a verified signed-in sender), `name`, `email`, `organisation`, `budget` (`under-25`, `25-50`, `50-100`, `100-250` or `250-up`), `sector_id`, `brief`, `consent`, `state` (default `new`), `assigned_to`, `reply`, `read_at`, `created_at`, `answered_at`.
- **`shortlist_entry`**: `account_id`, `case_file_id`, `created_at`; one entry per account and case file.
- **`subscriber`**: `email` (lowercased, unique), `created_at`, `unsubscribed_at` (a nullable timestamp).
- **`message`**: `to_email`, `account_id`, `kind` (`verify_address`, `reset_password`, `invitation`, `case_file_returned`, `case_file_live`, `enquiry_received` or `enquiry_arrived`), `subject`, `body`, `link`, `created_at`.
- **`analytics_event`**: `name`, `properties` (only the event's named properties), `created_at`.

Relationships: a sector has many case files and many client entries; an account owns many case files and reviews many; a case file has at least one chapter to be published, at most six information items and many awards, all ordered; an account and a sector each have many enquiries; accounts and case files meet through shortlist entries; notice rows and subscribers stand alone. Deleting a sector that any case file or client entry uses is refused. Deleting an account that owns case files moves them as in rule 129.

Invariants that must hold under concurrent requests, each of them holding when two requests arrive at the same instant and neither request sees the other's write: a look before a write is two steps, and the second request passes through the gap between them, so each of these must hold at the database level, decided by the stored rows rather than by what the app read a moment earlier: no two accounts share an email; no two subscribers share an email; a slug belongs to at most one case file and is never reissued; no two published case files share a grid position; no two chapters of one case file share a position; one shortlist entry per account and case file; a case file leaves `submitted` exactly once, so two simultaneous approvals produce exactly one approval and one conflict; a stale `version` never overwrites a newer write.

Derived, never stored: the `next` case file (from grid order), the carousel's twelve (from grid order), whether a list row is openable by the caller, relative times, sector labels on case files, result counts, and the reseed count (browser storage only).

**Seed data.** Seeding is idempotent - restarting the app must not duplicate rows.

- Accounts: `editor@example.com` (`editor`, `Ines Varga`), `author@example.com` (`author`, `Theo Lamb`), `author2@example.com` (`author`, `Juno Park`), `visitor@example.com` (`visitor`, `Sam Reed`); all verified.
- Sectors, in order: `sector-1` `Technology & Futures`, `sector-2` `Climate & Startups`, `sector-3` `Fashion & Beauty`, `sector-4` `Chain`, `sector-5` `Entertainment & Culture`, `sector-6` `Automotive`, `sector-7` `Collaborations`.
- Client roster, twenty-nine, in these groups and this order: `Technology & Futures`: `Aster`, `Gannet`, `Paper Lens`, `Sandbox`. `Climate & Startups`: `Alder Labs`, `Groundswell Energy`, `Sable`, `Thornfield`. `Fashion & Beauty`: `harbour Classics`, `Clarelle`, `Solene`, `Trelawn & Co`. `Chain`: `KVN`, `Nautilus`, `Zephyr`, `Skra`. `Entertainment & Culture`: `Nightly`, `OBX`, `Rook Games`, `Playmarket`, `Younger`. `Automotive`: `Lexon`, `Torvid`, `Lumen Motors`, `Sabres`, `Marconti`. `Collaborations`: `MCK`, `Emery Lauden`, `Gallery Research Trust`.
- Studio awards: `Harbour Prize`, `Wexel`, `A&DX`, `Open Show`, `Acclaims`, `FWX`.
- Notice rows: the fourteen labels of rule 70, in order, with placeholder bodies.
- Case files:
  - `Glass Harbour` (`glass-harbour`), client `Aster`, `sector-1`, `published` at position 1, owner the editor, chapters `headline`, `text`, `image`, `list`, awards `Harbour Prize` (`treatment-1`) and `Wexel` (`treatment-2`), information items `Year` / `2024` and `Role` / `Brand system`, seeded example.
  - `Night Signal` (`night-signal`), client `Groundswell Energy`, `sector-2`, `published` at position 2, owner the editor, chapters `headline`, `text`, `video`, `device`, seeded example.
  - `Soft Machinery` (`soft-machinery`), client `Lumen Motors`, `sector-6`, `published` at position 3, owner the editor, chapters `headline`, `text`, `split`, `video_loop`, seeded example.
  - `Paper Orchard` (`paper-orchard`), client `Solene`, `sector-3`, `draft`, owner `author@example.com`, chapters `headline` and `image`, the image uploaded as a real object in the bucket: an unpublished case file whose address and media must stay unreadable to the public.
  - `Quiet Engine` (`quiet-engine`), client `Nightly`, `sector-5`, `submitted`, owner `author2@example.com`, chapters `headline` and `text`, waiting in the review queue.
- No enquiry, subscriber, shortlist entry, message or event is seeded.

## Front-end specification

This section carries the visual and interaction specification in full, in words. Colour is given by family, tone and shade; motion by character and relative speed; space by relationship. Type is given exactly.

### The palette, token by token

The design values live in one place, and every surface names a value from it rather than writing its own. The measured set, by role:

- five near-black neutrals, ordered by distance from the page: the page itself (the void); the crystal's layer (the shard ground, a hair warmer, the one surface between the void and the object); the scrollbar track (the only chrome the browser draws); the fill of the showreel's play control and of loading blocks (the reel ground); the fill of a case file's round play control and of the split handle (the project ground); and the one surface that must read as lifted (the raised ground, the lightest of the five). They differ by only a few shades and are never interchangeable.
- a deep neutral for every section rule on the story and contact surfaces, and a second deep neutral for the arrival line's unfilled track;
- mid neutrals: the dimmest legal text (declared once and rendered nowhere); the bar message's label tone (a label that must not compete); the secondary copy tone (case file information values, the notice page's contact block, award names);
- light neutrals: the hint tone (the device scroll hint's rule and a device frame's stroke, a rule that is not white, never used for type); a quiet tone for copy on a filled control;
- near-white neutrals: the reading tone (case file body and list copy), the control-label tone (the close control's label), and white (every heading, every menu word, every rule fill, every animated underline, and the default for type);
- the warm sand, a light, soft orange: the only warm colour in the product;
- the caution yellow, a mid, vivid amber: declared once by the reference and rendered nowhere; the product spends it only on the armed delete;
- translucent whites at six strengths: the faintest visible rule (the hairline beside a case file's launch line), a divider inside a control (the counter divider), a field border at rest and the scrollbar thumb, a focused field border, a text scrim, and a control raised out of rest (the newsletter submit when pointed at);
- one translucent black: the only shadow colour, also the ground of a looping video;
- a half-transparent blue: a development placeholder found in the reference's unshipped image-sequence chapter, which never ships.

The two greys used for secondary type and for the hint rule differ by role rather than by lightness: the first is type, the second is a rule. A ground tone is never type and a type tone is never a fill. No colour outside this set is used anywhere, including by an extension surface, which reuses the nearest measured token. The thirty colours a scene library carries as its own built-in named colour table (a light soft teal and a mid soft red among them) are not a palette and never appear on the site.

### Type

The family is `Inter` with the fallback stack `Arial, sans-serif`, exactly as the reference declared after each of its own families, and the fallback is size-adjusted so its lowercase height and average character width match `Inter` within 2%. Four visually distinct weights carry the product: extralight 200 (display), light 300 (reading), regular 400 (label) and medium 500 (emphasis). A bold 700 cut is declared and never loaded. No font file is shipped or fetched by the app: the family is named, and the fallback renders wherever `Inter` is not installed. The open-licence status of `Inter` is stated in the app's own notice.

The complete ramp, with each size exact:

- 65px display: the three menu words (set solid, tracked tight); a carousel project title (on a taller line, tracked slightly tight);
- 60px: the studio story title (reading cut, set solid, tracked tight); a case file title (display, taller line); a notice body title (display, line slightly shorter than the size); a grid sector (display, on a taller line, tracked tight); the contact heading (reading, on a shorter line); the console heading and the sign-in heading `Studio`;
- 48px display: the wordmark, and the default first-level heading;
- 46px display: an archive (next) case file title;
- 40px reading: the studio promise and the client heading (tracked tight); the centred-notice heading (display);
- 36px display: the notice body description;
- 34px display: a case file description and the notice header description (tracked slightly open);
- 32px reading: the two contact addresses and the story subtitle; the narrow-tier wordmark and the arrival card line;
- 26px display: notice body copy, on a generous line, tracked slightly open;
- 24px display: an archive case file description;
- 22px reading: the client roster, the postal addresses, case file body copy (on a generous line), the skills line, console body text, and the pinned note;
- 17px label: the interaction counter;
- 15px emphasis: a notice subtitle (tracked open) and the case file close control label;
- 14px: the showreel play label (label cut, tracked open) and a grid tile's client line (reading cut);
- 13px: the notice contact block and a contact block heading (label cut, tracked open); a case file chapter title and a grid tile's heading (emphasis cut); an award name (label cut); the inline notice and the save-failure countdown;
- 12px label: a client sector heading (uppercase, tracked open) and a carousel client line;
- 11px emphasis: `View All Projects` (uppercase, tracked open), the menu's account line, every uppercase console control, a notice page contact heading, and the device scroll hint (label cut);
- 10px emphasis: the two labels of a split chapter and the bar message (uppercase, tracked open).

At the tablet class `View All Projects` rises from 11px to 13px; it is the only type step that changes with the device. Type never drops below 11px for a control label or 13px for body copy.

### Space, rules, radius, shadow and stacking

Every spacing value is a whole or half step of one base unit, plus a small set of absolute measures. The choosing rule: the large gap separates one thought from the next inside a scrolling surface and always comes with a rule; a smaller gap separates rows within one thought and never carries a rule; the notice page and a case file each have their own paragraph rhythm, the notice's much looser; the notice's rows are separated by a very large gap; nothing between the smallest and the medium steps is used to separate blocks, those steps are padding inside a control.

Containers: the studio story's inner column is centred with a wide top margin and a very wide bottom margin; the notice page and the console share one wide centred container laid out on sixteen columns, labels in columns one to six and copy or controls in columns seven to sixteen; the contact inner is four fifths of the window between a minimum and a maximum width; the project grid is a wide centred container with a deep top and bottom padding (a proportion of the width instead, at the narrow portrait and landscape tablet classes, where it also narrows); the newsletter strip spans the full width, a short band pinned to the bottom.

There is exactly one shadow, on a case file media block that declares it. Only three radii exist: a full circle for every catchment, the case file play control and the split handle; a small softening on the scrollbar thumb; and the corner radius of a device chapter's frame, which is the one rectangular outline allowed to round its corners. Rules: a one-pixel section rule in the deep neutral across the full container on the story and contact surfaces; a hairline in the faintest translucent white across three quarters of the width beside a case file's launch line; a one-pixel white underline pinned to the bottom of a link across the link's own width (scoped to the link, never to its row); a short white divider mark for the archive chapter; a short translucent divider inside the counter.

Every underlined link carries the underline twice: a faded copy held at about a quarter strength at rest, and an animated copy held at zero that draws itself across at full strength when the link is pointed at or focused.

Stacking, from back to front: the arrival wordmark's inner block; the interaction holder; the crystal's background layer and the newsletter response; the crystal's own layer and the arrival overlay; a case file's video player, poster and image surface; a case file's video poster; every play control and its close control; the shell (the corner controls, the overlay, the archive control); the interaction bar and a media block in full window; and at the very front the drag cursor and the topmost overlays.

The scrollbar is styled rather than hidden: the track in its near-black, the thumb in the translucent white with a slightly softened corner. Every element sets no tap highlight, and the page disables text selection and dragging except on reading surfaces, which re-enable selection.

### Iconography

Every icon is drawn geometry from one hidden set declared once at the top of the document and referenced by name; none is a file. The fifteen named marks: `arrow` (one path; carousel and grid paging and every directional control), `close` (two lines; close the open layer), `close-alt` (two polylines; close at a larger size), `close-left` and `close-right` (one polyline each; the halves of a two-part close), `drag-arrows` (two polylines; the vertical drag affordance), `drop` (one path, a droplet; the control that reseeds the crystal), `fullscreen` (four polylines in three groups; expand a media block), `device` (one path, a phone outline; the case file's device frame mark), `loading-ring` (one circle; every pending state), `play` (one polygon, a triangle; play the reel or a case file video), `rotate` (one path; the reset control), `menu` (three bars; open the menu), `social-a` and `social-b` (one path each; the first and third social destinations, supplied by the operator, with the reference's marks kept as fallback geometry). Each mark keeps the reference's own drawing extent and coordinates exactly.

The drawing rule every mark obeys, and every new mark must obey: anything that means an action is drawn as an unfilled stroke (the closes, the drag arrows, the expand corners, the ring); anything that is an object is filled (play, drop, arrow, rotate, device, menu); every stroke is two units wide with sharp mitred corners, never a rounded cap or join; every coordinate lands on a whole number, a half or a tenth; and a stroked mark is inset by half its stroke plus a tenth so it sits optically inside its box rather than clipped by it. Every icon inherits a white fill from its control and fills its control in both directions, so the control alone decides its size. The four corner controls and the grid's sector arrow draw their animated state into a small drawing surface layered over the static mark, redrawn per frame without re-laying out the document, and fall back to the static geometry when that surface is unavailable.

### Global chrome

The chrome is the four corner controls, one overlay and one interaction bar, anchored to the window rather than the page, and nothing else is present at rest. Each corner control is fixed, sits in the shell layer, shows a pointer cursor, and stays hidden until the arrival sequence completes: `Drop` in the top left (a droplet mark, slightly taller than wide), `Discover` in the top right (the three-bar mark, square), `Showreel` in the bottom left (the play triangle, the smallest mark) and `Audio` in the bottom right (the speaker mark, wider than tall). Each sits a small, equal inset from its two window edges.

Each control's catchment is an invisible circle many times the mark's size, offset toward the window's corner so the mark sits near the circle's outer edge rather than its centre and most of the circle lies over the empty corner. The same construction gives the carousel's paging arrows their own circular catchments. Each control's name is a separate label beside its mark, white, in the label cut, never wrapping, hidden at rest and revealed on approach; at the widest tier each label, and the marks of `Drop` and `Audio`, shift slightly further from the edges, which is the whole of the reference's wide-screen behaviour.

The close control that replaces `Discover` while a layer is open is a wide control rather than a mark, right aligned near the top-right corner, its label in the medium cut in the control-label tone, with a short white vertical divider pinned to its right edge; at the widest tier it shifts slightly.

The archive control is a fixed, centred strip near the top of the window, invisible and not clickable until the carousel is open, holding `View All Projects` with the double underline.

The interaction bar is a short fixed line centred near the bottom of the window, never catching the pointer, carrying the message (centred, uppercase, the bar message size, in the label tone), a short white line hidden at rest, a ring drawn in a small square surface, and the counter (hidden at rest, white, in the label cut) with a small translucent divider. The counter's digits sit in a clipped box, each digit positioned on its own, so a changing digit slides the next one up through the clip rather than being replaced.

The home screen and the carousel show a grab cursor, changing to a grabbing cursor while dragging. The project grid shows a grab cursor when draggable, the default cursor when not, and no cursor while the site's own round drag cursor is shown: a circle that fades in and follows the pointer, invisible at rest.

### Motion

Two measured curves and two browser keywords carry every transition, and no third curve is invented: a strong ease-out that leaves immediately and arrives slowly (the most used); a soft, symmetric ease-in-out with no overshoot; the plain ease-in-out keyword; and the plain ease keyword. Three speeds exist and no fourth: quick for a state change on a control the pointer is on (a border colour, an opacity, a scale); slightly slower for a control the pointer is near but not on; slower again for a change that moves content rather than a control. A longer movement is composed from the slowest speed with stated delays. Every transition names the property it moves; nothing transitions everything at once.

The named moments, each with its reduced-motion form:

- `arrival-progress`: the progress fill grows across as loading truly progresses, linearly; unchanged under reduced motion, because it is a report.
- `arrival-ring`: the ring's stroke runs around continuously; replaced by a still, faint ring.
- `arrival-reveal`: the wordmark fades in with the strong ease-out; appears in one step.
- `chrome-enter`: the four corner controls fade in one after another; appear together.
- `control-approach`: a control's label fades in as the pointer enters its catchment, with the plain ease; appears in one step.
- `control-press`: the mark shrinks sharply while pressed; dims instead.
- `underline-draw`: the bright underline draws across a pointed-at link; appears whole at once.
- `underline-fade`: the underline fades back to its faint strength when the pointer leaves; changes in one step.
- `field-focus`: a field's border brightens on focus; unchanged, it is a colour change.
- `submit-hover`: the submit control brightens under the pointer; unchanged.
- `layer-open`: a layer fades in and moves forward in depth with the strong ease-out; fades only.
- `layer-close`: a layer fades out with the soft ease-in-out; fades only.
- `menu-word-hover`: the two words not pointed at dim; no change.
- `carousel-drag`: the strip tracks the pointer in depth with no easing; the drag still works, with no inertia.
- `carousel-settle`: on release the strip settles on the nearest item with the strong ease-out; jumps to it.
- `drag-icon-draw`: the drag mark's four short arrowhead strokes and its long line each grow from nothing, one after another; the mark appears complete.
- `grid-filter`: tiles fade and move to their new places one after another in a quick ripple; they rearrange with no ripple.
- `sector-arrow`: the selected sector's small arrow fades in with the plain ease; appears in one step.
- `sector-dim`: an unselected sector brightens a little under the pointer; no change.
- `handle-press`: the split handle's round ground shrinks sharply and its arrow shrinks and fades away; the handle dims with no shrink.
- `counter-roll`: the counter's digit strip slides by one digit; the digit is replaced.
- `crystal-idle`: the object rotates continuously; the object holds a fixed angle.
- `crystal-drag`: the object follows the pointer; the drag still rotates it, with no inertia.
- `crystal-reseed`: every facet flies out and falls back with a new seed, a short beat out, a pause, a short beat back; the object re-forms in one step.
- `reel-transport`: the playhead follows the pointer on the transport; unchanged.

The arrival sequence, step by step: the overlay fills the window over the void; a block centred in the window holds the droplet mark; a thin track in the deep neutral sits just below the block with a white fill of the same length growing across as loading progresses; the wordmark, two lines in the display cut, fades up; the corner controls change from hidden to shown and fade in one after another.

The one keyframe the reference declares is the pending ring: the loading ring's stroke offset runs continuously a little more than two full turns per cycle, which is why it reads as accelerating rather than ticking. It is the pending state for every asynchronous action.

The reference's runtime animation was never captured, only its declared speeds and curves, so the timings of the moments above are composed from those declared values; that evidence gap is closed by this substitution rather than by invention. Motion rules: nothing but the crystal moves more than one property at a time; a control at rest never animates, with no idle pulse, attract loop or ambient movement anywhere except the crystal; opacity is the default verb, since most elements are held invisible and revealed; a reveal is never slower than the slowest of the three speeds.

### The crystal, specified

The crystal renders into one drawing surface filling the window, over the shard ground, over the void, in the object layer. Seen at rest it is a roughly spherical mass a little under a third of the window's width at desktop, centred horizontally and sitting slightly above the window's vertical middle. It is not a solid: it reads as forty to sixty flat triangular and four-sided facets, most of them nearly black, arranged on and slightly off the surface of the sphere, several visibly detached and floating a short distance out, which is what makes it read as shattered rather than faceted. Two to five facets per frame catch a hard white specular and read as almost pure white. Bright facets migrate steadily around the mass in one direction as it turns, with no frame repeating another.

The construction, from primitives alone: start from an icosahedron subdivided twice (three hundred and twenty triangles) and take a deterministic seeded sample of forty-eight faces; detach each into its own piece so no two share a corner and each has a flat normal; push each piece out along its normal by a seeded amount up to about a fifth of the radius, roughly a fifth of them well out, which produces the visibly detached facets; turn each piece slightly about its own centre so edges never line up into a readable sphere; shade with one hard specular light placed forward, above and to the right, sharp enough that fewer than five pieces are bright at once, over a base close to the shard ground; draw the scene three times with the camera nudged a fraction of a pixel in opposite directions for two of the passes and combine them one colour channel from each, which is the fringe; and rotate the whole mass about an axis tilted from vertical, slowly enough that a full turn takes between forty and sixty seconds.

The reseed contract: the facet offsets swell to a little over three times their resting distance while the rotation speeds up to between two and three times its idle rate, hold for a beat, and return to rest, with the new seed applied.

The object is a control: dragging rotates it and it keeps its momentum on release (the resting angle is stored per visitor); `Drop` reseeds it (the seed is stored per visitor); every reseed increments and rolls the counter (the count is stored per visitor). The crystal region is focusable, carries a text label describing it in words, and is decorative to a reader that does not focus it.

The static fallback is generated from the same construction rather than fetched: drawn once at desktop size and kept as a drawing, or, when three-dimensional rendering is unavailable entirely, drawn with flat drawing operations: fill the shard ground, draw the same forty-eight seeded triangles projected once, each filled with a tone between the shard ground and white by how directly it faces the light, then stroke the six brightest triangles' edges twice, a pixel apart, in opposed colour channels.

### Sound, specified

The reference shipped ten distinct beds and cues; the product synthesises each, and none is a recording. The default mixdown is the ambient bed behind the home screen: three low sine tones, the highest detuned slightly sharp, summed through a low filter whose cutoff drifts slowly, held very quiet. The menu drop loop runs while the menu is open: the home bed with the filter opened up and a fourth, higher tone faded in. The shapes mixdown sits behind the work carousel: the home bed with a quiet triangle tone added, swelling gently. The tunnel is the bed behind a layer transition: filtered noise swept upward and faded to silence. The bats mixdown and the shapeshifter are two further scene beds. The accordion mixdown sits behind the narrow-window card: two slightly detuned sawtooth tones through a band filter, swelling in a slow repeat, the nearest a synthesised bed gets to a reeded instrument. The rollovers mixdown is the cue layer for approach and press: approaching a control plays a very short, very quiet high sine tick; pressing one plays a short tone falling by an octave. The drop vibrate cue plays on reseed: a low tone falling further with a shudder in it. The interactive cue layer is tied to the counter.

The `Audio` mark is drawn as geometry on a box wider than tall: a speaker outline in both states; the off state adds two crossed lines at the same angle as the `close` mark, which is why it reads as off rather than as a different icon; the on state adds two concentric arcs. Both are stroked two units wide and mitred.

### The home screen and the menu, specified

The home screen layer fills the window; its inner content is centred on both axes and ignores the pointer, so a drag starting on the wordmark reaches the crystal. The wordmark's opacity starts at zero and is raised by the arrival sequence.

The menu layer fills the window with a strong perspective, so a word turned even slightly shows visible convergence. The three words sit in one centred row, the first two in equal columns and the last in a slightly wider one, each word a block with generous padding above and below, its link invisible at rest and revealed in depth. The blocker is an overlay covering the whole list that ignores the pointer at rest and catches it while a transition runs. The account line sits at the bottom centre of the menu layer, uppercase, tracked open, white, with the double underline.

### The public layers, specified

**Studio story.** The layer is taller than the window and scrolls within itself while the page stays one window tall. Its inner column is wide and centred with a default cursor; the reading column is narrower. The blocks, in order: the visually hidden heading (clipped to a single pixel); the studio title (reading cut, set solid, tracked tight, followed by the large gap); a rule; the promise (tracked tight); the disciplines line (sentence case); a rule; the clients heading (tracked tight, followed by the large gap); one row per sector, each a line of client names beside a sector label column exactly a third of the reading column wide, the row aligned along its bottom edge, rows separated by the smaller gap; a rule; the awards heading; the award names three to a row, each with a gap below; a rule.

**Work carousel.** The layer fills the window with a strong perspective and a grab cursor. The item strip spans the width across the vertical middle. Each item is centred, never wraps, has generous padding and a pointer cursor; the active item ignores the pointer; its text starts invisible. The client line sits just above the title, spans its width, is uppercase and tracked open, invisible at rest and ignoring the pointer. Each poster is a cover-sized background, centred, kept in depth, and carries an invisible outline that forces it onto its own compositing layer so the poster and its title never separate by a sub-pixel during a depth move. At the narrow and tablet classes the carousel is fixed to the window rather than the page, and on one browser family it is fixed at every width.

The drag mark is a wide, thin line with two short arrowheads at each end, drawn from five one-pixel pieces rather than an icon: the line, and four arrowhead strokes each turned an eighth of a turn up or down, each piece a masked inner bar so it can be drawn on from one end; the outer pairs are kept ready to move. The paging arrows sit either side of the vertical middle, tall and narrow, each with a large circular catchment offset outward; both are hidden until the carousel is interactive; both use the `arrow` mark, the previous arrow turned half a turn.

**Project grid.** The container starts hidden, invisible and grab-cursored, becoming default when not draggable. The header holds the filter label (uppercase, the emphasis cut, almost invisible: a legend, not a control) and the sector list (each sector in the display cut, inline, with room on its right; unselected at half strength, a little stronger when pointed at, full strength when selected; the selected one carries a small arrow in a wrapper at its right that fades in). The tile list wraps two tiles across; each tile is absolutely positioned inside the wrapper and holds a poster (cover-sized, centred, kept in depth, with its own perspective) and a caption below it (a centred uppercase heading in the emphasis cut, tracked slightly open, over a centred client line in the reading cut at reduced strength). Tiles are moved into place rather than reflowed, because a list that reflows cannot animate its filter.

**Case file.** The header block starts well below the top (a proportion of the width at the tablet classes) with a deep gap under it, on its own layer; the title is centred, never wraps, and fades in; the description paragraphs fade in; the information block is a row of items each a white heading in the emphasis cut over a value in the secondary tone, the first item flush left and the rest spaced apart; a launch value sits on a taller line, rising to the same height at the wider tier.

Chapter constructions: a headline is full width on its own layer, a title in the display cut; a text chapter is a narrow label column (a fifth of the width, emphasis cut, tracked open, on a loose line) beside a wide copy column (seven tenths, offset by a tenth, reading cut in the reading tone, tracked slightly open, with underlined links); a list is seven tenths wide, offset by three tenths, indented, in the reading cut and tone; an image is a fill sized to be wholly contained, with an optional drawing surface over it and an expand control in the lower right; a video fills its block with a poster over it, a large round play control in the project ground at its centre with the play mark, and close and expand controls hidden until playback; a video loop fills its block over the translucent black ground with no controls; a device frame stretches to its block with a screen inset inside it (in portrait the screen is inset more at the top and bottom than at the sides; in landscape more at the sides than at the top and bottom); a split is the comparison below.

A device chapter whose screen scrolls carries a hint just outside the frame at its vertical middle: a short rule in the hint tone that grows from its center right, and a small label turned a quarter turn. The screen shows a grab cursor, changing to grabbing, and its image stretches to the screen.

The split chapter: the block has an invisible margin on all four sides so the drag can be caught outside the visible frame; the inner window clips its content; each item is twice the block's size in the axis of comparison and offset by half, so the two media lie end to end inside the window and the drag moves the pair rather than resizing either one (the first item sits before the window, the first item's media sits after its own half); the two labels (uppercase, the smallest emphasis size, tracked open) sit in the top-left and top-right corners for a vertical comparison and the top-left and bottom-left corners for a horizontal one; the handle is a round control centred on its position with a grab cursor, its ground a circle in the project ground held slightly under full size, collapsing to under a third of its size when pressed, its arrow mark (the two-part close geometry turned a quarter turn, and a further quarter turn for the vertical orientation) white, stroked, vanishing when pressed. Animating a width instead of moving the pair looks wrong immediately and is not acceptable.

The footer sits on its own layer with a deep gap above; awards sit a quarter of the width each, each a mark at its treatment's height (the eight treatments range from a small to a large height, which is why the row aligns to its bottom edge) over the award name in the secondary tone; the launch block pairs a label column (a quarter, white, emphasis cut) with the address and the hairline (three quarters, or the full width when there is no address); a divider with a short white mark at its left separates the footer from the next case file preview, whose title is full strength from the start (46px) over its description (24px).

**Showreel.** The layer fills the window with a moderate perspective. The poster fills the layer, hidden until ready, cover-sized, in front. The play control is a dark rectangle in the reel ground, wider than tall, centred and pushed a hair toward the viewer so it stays crisply in front of the poster during the layer's own depth move, with a pointer cursor, starting invisible; its label sits beside the triangle mark. The transport is a full-width bar that rests just below the bottom edge, off screen, and rises into view while the reel plays; inside a case file the same transport sits just above the bottom of the video.

**Contact.** The layer centres its inner block, which has generous padding and a default cursor. The address block is a row: the heading (reading cut, sentence case) with a wide gap to its right, then the two addresses one above the other, each underlined with a solid thin rule; it fades in. A rule follows with a larger gap below than above. Each detail block pairs a heading column (label cut, tracked open, fixed width, with a wide gap after it) with its body (reading cut, fading in), a telephone line followed by a line's gap. The newsletter strip is a short full-width band at the bottom: its two links (emphasis cut, tracked open) each preceded by the small arrow mark, the form wrapper hidden until opened, the field (an outlined box with no fill and a thin translucent border that brightens on focus, no outline) followed directly by the submit (no fill, no border, at low strength, brighter when pointed at or focused), the submit's pending ring in its place while pending, and the response line beside them, invisible until it speaks.

**Notice page.** The layer starts invisible with a pointer cursor; its inner container is wide, centred and default-cursored; each faded element carries its own reveal. The header is tall; its title sits in the display cut in sentence case; its description sits well below it; the contact strip is a three-column row (three tenths, a quarter, a quarter) of small emphasis headings over label-cut copy in the secondary tone. The page's plan is a two-column grid repeated down the document, and the body is the display cut throughout: each row's label is a short uppercase subtitle in the label columns, each row's copy a large paragraph in the copy columns, lists are indented discs, paragraphs are separated by the notice's loose rhythm (except the last), and rows by the very large gap (except the last).

### The console and the account surfaces, specified

The console shell uses the notice page's container and sixteen-column grid: labels in the left six columns, controls in the right ten. Its heading is display type, section labels are uppercase emphasis type tracked open, body text is reading type in the reading tone, and rows are separated by the very large gap with a deep neutral rule where one is wanted. The case file list's columns: position and client and updated in the label cut in the secondary tone; the title in the reading cut in white; the sector in small uppercase; the state in small uppercase emphasis. Each row carries the double underline across the whole row, the one place a block rather than a run of text is underlined. The state filter reuses the grid's sector construction at a smaller size, unselected states at half strength.

The editor divides into the chapter list (a fifth of the width) and the field column (seven tenths, offset by a tenth). The arranger shows chapters as tiles half the width, two across, moved into place rather than reflowed. The review queue's `APPROVE` and `RETURN`, `NEW CASE FILE`, `SUBMIT FOR REVIEW`, `PUBLISH`, `PUBLISH CHANGES`, `DELETE` and `REMOVE THE EXAMPLES` are small uppercase emphasis controls with the double underline. The inbox opens a row to show the brief in the reading cut and tone, with the reply composed in the newsletter's field treatment. The sign-in layer uses the console container and the form field treatment under its `Studio` heading; its submit is the newsletter submit, with the pending ring while pending. The account surface lists display name, email address and password (the holder), role (an editor, never their own), the live sessions, and the shortlist (a visitor).

### Forms, specified

Field states: at rest, a thin border in the translucent white at its focused strength (raised from the reference's fainter resting border, which was below the contrast floor for a control boundary); focused, a thicker border at that strength plus the white outline; invalid, the border in the warm sand with the message below in small label type in the warm sand; unavailable, the faintest translucent border with dim text and a default cursor. The border change carries the focus state, which is the only reason the browser's own focus outline may be replaced. Submit states: at rest at low strength; pointed at or focused, brighter; unavailable, low strength with no change on pointing; pending, brighter, with the ring in place of the mark.

### Responsive tiers, specified

Five tiers: narrow (phones held upright), mid (large phones and small tablets), wide (from the width of the story's reading column), wider and widest. The reference itself showed, at a phone width, only a full-bleed illustration of a figure playing an accordion with no way in; the product keeps that joke only as a dismissible arrival card at the narrow tier, shown at most once per visitor and never blocking, rendered as type alone (`Someone is playing the accordion. Carry on.` and the control `CARRY ON`) over the void with the crystal turning behind it, and builds the whole site underneath.

- Home screen: at narrow, the crystal at the reduced facet count, the wordmark at 32px on two lines, and smaller catchments that still exceed a thumb target; at mid, catchments a little under the full size; at wide and up, as measured.
- Menu: at narrow, the three words stacked one per row at 48px with the account line below; at mid, one row at 48px; at wide and up, 65px.
- Studio story: at narrow, the container spans the window less a small margin each side and each client row puts its sector above its list; at mid, a slightly larger margin with rows still side by side.
- Work carousel: at narrow, replaced by the grid, because a depth carousel dragged on a narrow screen fights the page; at mid, fixed to the window.
- Project grid: at narrow, one tile per row at full width with the sector filter stacked at 32px; at mid, two tiles per row with the filter at 48px.
- Case file: at narrow, chapters span the full width, a text chapter stacks its label above its copy, and a split chapter is forced to the vertical orientation; at mid, a text chapter keeps two columns at a quarter and three quarters.
- Showreel: at narrow, a smaller play control and the transport pinned to the bottom.
- Contact: at narrow, the address block and each detail block stack heading above body; at mid, the gaps narrow.
- Notice page: at narrow, one column with each label above its paragraph; at mid, two columns at about a third and two thirds.
- Console: at narrow, one column with the chapter list above the fields; at mid, two columns at three tenths and seven tenths.

At every width: the four corner controls never become a bar or a menu sheet; a catchment is never smaller than a comfortable thumb target and never smaller than the control plus a margin on every side; no surface scrolls sideways; type never drops below the smallest label and body sizes; the crystal is never hidden; and the document reflows at double zoom with no sideways scroll. At the tablet class the reading container scrolls with touch momentum.

### Accessibility, specified

Focus order is authored per surface rather than inherited, because every surface is a layer in one document:

- home screen: `Discover`, `Showreel`, `Audio`, `Drop`, then the crystal region;
- menu: `About`, `Work`, `Contact`, the account line, then the close control;
- studio story: the close control, then the scrolling region, and nothing else, since there are no links;
- work carousel: the close control, `View All Projects`, previous, next, then each item in depth order;
- project grid: the close control, each sector in order, then each tile in grid order;
- case file: the close control, each chapter's own controls in chapter order, the launch address, then the next case file;
- showreel: the close control, the play control, then the transport;
- contact: the close control, each address link, each enquiry field in form order, submit, then `DISPATCH` and `PRIVACY`;
- notice page: the close control, then each link in document order;
- console: the close control, the filter, the search field, then each row.

Focus moves into a layer when it opens, is trapped inside it (Tab from the last element returns to the first), and returns to the control that opened it when it closes; Escape closes the layer and restores focus.

Focus treatment, one per element class: a field's border change as above; a text control's full underline drawn exactly as when pointed at; a corner control's label shown plus a thin white ring drawn at the bounds of its catchment, slightly inset, which shows a keyboard visitor the true target that is otherwise invisible; a grid tile's thin white outline, slightly inset; the submit's brighter state; every other control's thin white outline, slightly inset. Focus is never shown by colour alone and an outline is never removed without a replacement.

Keyboard paths for every drag: reordering chapters or the grid, focus a row, Space lifts it, the up and down arrows move it, Space drops it and Escape cancels, and each move is announced as `<title>, lifted, position <n> of <m>` and then the new position; the split handle moves the comparison by 2% per arrow press, with Home and End going to the ends; a device screen scrolls by a small step per up or down arrow press; the carousel moves one item per left or right arrow; the crystal turns 0.12 radians per left or right arrow.

Announcements through live regions: a layer opening or closing (`<surface name> opened`, `<surface name> closed`, polite); every bar message (polite); a field save (`Saved`, polite) or its failure (`Not saved. Your text is safe here.`, assertive); a form sending (`Sending`, polite), succeeding (its success copy, polite) or failing validation (`<n> things need attention`, assertive, with focus moved to the first); a filter change (`<n> pieces of work`, polite); a skeleton showing (`Loading`, once, polite); connectivity (`Offline` or `Back online`, polite); a returned case file's note (`Changes requested`, then the note, assertive); a second person in the case file (`<name> is also editing this`, polite).

Contrast, pairing by pairing, against the page ground and the crystal's ground: white reads at 21 to 1 and 19.35 to 1, the control-label and reading tones above 14 to 1, the quiet tone above 10 to 1, the hint tone above 7 to 1, all passing at every size; the secondary tone at 5.32 to 1 and 4.90 to 1 passes as normal text only just, which is why it is never taken darker; the bar message's label tone at 3.54 to 1 fails as normal text and is used only for the decorative status line, with the remedy below; the dimmest tone at 2.90 to 1 fails and is rendered nowhere; the warm sand (above 13 to 1) and the caution yellow (above 18 to 1) pass. A field's resting border is not text; the change from rest to focus is a clearly visible change in contrast.

The two remedies, named so nobody reverses them: nothing a visitor must act on is shown only in the bar message, which is also announced; and the resting field border is raised to the reference's focused strength while focus takes a thicker border plus the white outline. Both reuse measured values; only their assignment changes.

Also: one first-level heading per surface, visually hidden where the design shows none, using the reference's clip rule (absolutely positioned, one pixel square, no padding, a negative margin, overflow hidden, fully clipped, no border); the menu is a navigation landmark and each surface is the main landmark while it is the topmost open layer; every interactive target is at least 44px in each direction; the document reflows to double zoom with no sideways scroll.

### Generated assets: the zero-asset substitution guide

The product ships no binary of any kind and fetches no image, font, audio, video or model file of its own. The reference used web fonts (four weights of one grotesque plus unused cuts of a second family), ten audio files, several hundred raster images, a set of award marks and films; each class is replaced by a recipe.

- **Fonts**: named, never shipped, as in the type section; the unused cuts are never fetched.
- **The crystal and its still fallback**: generated, as specified above.
- **Posters, tiles and photographic media** are the operator's own work, uploaded into the bucket. Until one is supplied the placeholder is generated: the case file's slug is hashed deterministically to a number; two tones are taken by that number, the first from the five near-black grounds and the second from the deep neutral and the two dimmer mid neutrals; they fill a straight gradient at an angle taken from the same number; the grain is laid over at a little under half strength; and the client name is drawn centred in small uppercase label type in the secondary tone. No colour outside the palette is used, so a page of placeholders still looks like this product.
- **Films**: the reel, the video chapter and the video loop are the operator's. A missing film shows the empty layout, never a placeholder film. A poster is the slug-keyed gradient with the play control drawn over it.
- **Grain**: a fine, static, monochrome grain over the window, generated as an inline turbulence pattern (fine base frequency, four octaves for tonal variation, colour removed), tiled, very faint over the shard ground, with no blend mode. It is the one visual value with nothing measured behind it.
- **Award marks**: each award is stored as a name plus one of eight treatments (`treatment-1` to `treatment-8`) and rendered as its name in the secondary tone under a short white rule at the treatment's height; an operator-supplied mark replaces the rule and keeps the height.
- **Device frames**: drawn from the insets alone as a rounded rectangle filling the block, stroked two units wide in the hint tone with no fill, in portrait or landscape.
- **Audio**: synthesised, as specified above, and not before sound is turned on.
- **The narrow-window illustration**: the arrival card rendered as type, as above; operator artwork replaces the type without changing the card's behaviour.
- **Small interface images**: the newsletter's small arrow is the `arrow` mark drawn small in the current text colour; the unsupported-browser image is the centred notice of rule 112.
- **Link previews**: the preview images are drawn by the server, as in rule 136.

## Constraints

- Single studio: one tenant, one public site, one console.
- No outbound email, no mail vendor, no SMS; the seven messages are stored and read in the app.
- No payments, pricing, checkout or invoices.
- No comments, likes, follows, public profiles or public search box.
- No collaborative co-editing of one field; two people in one case file see presence and field holds only.
- No notification bell, badge count or toast stack.
- No external identity provider or single sign-on; open sign-up creates visitors only.
- No image, font, audio, video, texture or model file of the app's own is shipped or fetched; every asset is generated or named.
- No third-party network call at runtime: no analytics vendor, no font service, no video host, no embed.
- No second locale ships; the locale machinery exists for one.
- No native app; the web app works at every width instead.
- No light theme.
- The seven addresses the reference's crawler reported (`/a/`, `/a/b`, `/a/i`, `/api`, `/wa/`, `/abc/`, `/url/`) are fragments of its tracking code, not pages; the product's addresses are only those in `## User flow`.
- The data volume to stay responsive at: a studio with twelve to forty published case files, a few dozen drafts, a few people in the console and a few hundred enquiries.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`: `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials for the four seeded accounts are written to `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An ordinary background job dies with its shell, and the app will not be running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from outside the container.
- The backing services named in this brief (PostgreSQL as `postgres`, MinIO as `minio`) are already running and reachable at their environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every request and response body is JSON except the media upload (multipart, one field `file`), the media read and the preview image. List endpoints return a top-level JSON array. Bearer auth is required on everything except `/api/health`, `/api/site`, the public case file and media reads, the preview images, `/api/enquiries`, `/api/subscribers`, `/api/events`, `/api/auth/signup`, `/api/auth/login`, `/api/accounts/verifications`, `/api/accounts/resets`, `/api/accounts/resets/complete` and `/api/invitations/accept`. A successful call returns the named resource or shape; an invalid or unauthorized call is rejected as a client error, never a server error and never a silent success.

Every non-success response carries the same body: `{"error": <token>, "message": <sentence>, "fields": {<field>: <message>}, "retry_after": <seconds or null>}`. `error` is one of nine tokens: `validation_failed`, `not_authenticated`, `not_authorised`, `not_found`, `conflict`, `version_conflict`, `state_not_allowed`, `rate_limited`, `server_error`. `message` is the sentence a person reads; `fields` maps each rejected field to its message; `retry_after` is present only on a rate-limit refusal. No status code ever reaches a visitor's screen.

The public case file summary is `{id, slug, title, client, sector, sector_label, description, position, published_at}`, where `sector` is the sector token. The full public shape adds `launch_url`, `information_items` (`[{heading, value, position}]`), `chapters` (`[{id, kind, position, payload}]`, ordered by position), `awards` (`[{name, mark, position}]`) and `next` (`{slug, title, description}` or null). The studio shape adds `state`, `owner_id`, `owner_name`, `original_author_name`, `submitted_by`, `submitted_at`, `reviewed_by`, `self_approved`, `return_note`, `returned_at`, `approved_at`, `version`, `draft_payload`, `presence` (`[{display_name, field}]`), `seeded`, `created_at` and `updated_at`; the studio summary is `{id, slug, title, client, sector, state, owner_id, owner_name, position, updated_at, editable}`.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `200` |
| `GET /api/site` | none | `{studio, sectors, clients, awards, contact, notice, newsletter}`: `studio` is `{name, line, founded, promise, skills}`; `sectors` is `[{token, label, position}]` in order; `clients` is `[{id, sector, name, position}]`; `awards` is the six names; `contact` is `{new_business_email, careers_host, offices: [{city, phone, address_lines}], social, privacy_email}`; `notice` is `{title, description, rows: [{id, label, body, position, updated_at}]}`; `newsletter` is `{name}` |
| `GET /api/case-files` | `sector`, `sort`, `page` (from 1, 24 per page) | the published case files as summaries, grid order by default |
| `GET /api/case-files/{slug}` | none | the full public shape; not found unless published; an old slug answers a permanent redirect (301 or 308) to the new address |
| `GET /api/media/{media_id}` | none | the bytes with their content type |
| `GET /api/preview/{key}.png` | `key` is `site` or a published slug | an `image/png` |
| `POST /api/enquiries` | `{name, email, organisation, budget, brief, sector, consent}`; `budget` is `under-25`, `25-50`, `50-100`, `100-250` or `250-up`; `sector` is a token | `201` with `{id}` |
| `GET /api/enquiries/mine` | none | `[{id, brief, state, reply, created_at}]` for the signed-in sender |
| `POST /api/subscribers` | `{email}` | `201`; a repeated address is a conflict and stores nothing new |
| `POST /api/events` | `{name, properties}` | `202` |
| `POST /api/auth/signup` | `{email, password, display_name}` | `201` with `{access_token, account}` |
| `POST /api/auth/login` | `{email, password}` | `200` with `{access_token, account}` |
| `POST /api/auth/logout` | `{all_devices}` (optional) | success with no body |
| `GET /api/auth/me` | none | the account's public shape |
| `GET /api/auth/sessions` | none | `[{id, current, created_at, last_used_at, expires_at, idle_timeout_seconds}]` |
| `DELETE /api/auth/sessions/{id}` | none | success with no body |
| `POST /api/accounts/verifications` | `{token}` | success with no body; an unknown token is invalid; an expired one is refused |
| `POST /api/accounts/resets` | `{email}` | `202` with `{message}` |
| `POST /api/accounts/resets/complete` | `{token, password}` | success with no body |
| `PATCH /api/accounts/{id}` | any of `{display_name, email, password, current_password, role}` | the account's public shape |
| `DELETE /api/accounts/{id}` | `{confirm_display_name}` | success with no body |
| `POST /api/invitations/accept` | `{token, password, display_name}` | `201` with `{access_token, account}` |
| `GET /api/messages` | none | `[{id, to_email, kind, subject, body, link, created_at}]`, newest first |
| `GET /api/shortlist` | none | `[{case_file_id, slug, title, created_at}]` |
| `PUT /api/shortlist/{case_file_id}` | none | success with no body |
| `DELETE /api/shortlist/{case_file_id}` | none | success with no body |
| `POST /api/shortlist/merge` | `{entries: [{case_file_id, created_at}]}` | the merged shortlist |
| `GET /api/studio/case-files` | `state`, `owner`, `sector`, `q`, `sort` | studio summaries |
| `POST /api/studio/case-files` | none | `201` with the new draft's studio shape |
| `GET /api/studio/case-files/{id}` | none | the studio shape |
| `PATCH /api/studio/case-files/{id}` | any of `{title, client, sector, description, launch_url, information_items, awards, slug, version}`; `information_items` is `[{heading, value}]`, `awards` is `[{name, mark}]` | the studio shape |
| `DELETE /api/studio/case-files/{id}` | none | success with no body |
| `POST /api/studio/case-files/{id}/transitions` | `{to, note}` | the studio shape |
| `POST /api/studio/case-files/{id}/publish-changes` | `{version}` (optional) | the studio shape |
| `POST /api/studio/case-files/{id}/presence` | `{field}` (a field name, or null to release) | success with no body |
| `PUT /api/studio/case-files/{id}/chapter-order` | `{chapter_ids}` | the chapters in their new order |
| `POST /api/studio/case-files/{id}/chapters` | `{kind, payload}` | `201` with `{id, kind, position, payload, version}` |
| `POST /api/studio/case-files/{id}/media` | multipart `file` | `201` with `{id, key, content_type, size_bytes, sha256}` |
| `PATCH /api/studio/chapters/{id}` | `{payload, version}` | the chapter |
| `DELETE /api/studio/chapters/{id}` | none | success with no body |
| `PUT /api/studio/grid-order` | `{case_file_ids}`, every published case file exactly once | the published case files in their new order |
| `GET /api/studio/enquiries` | `enquiry_state`, `q`, `sort` | `[{id, name, email, organisation, budget, sector, brief, state, assigned_to, reply, read, account_id, created_at, answered_at}]`, newest first |
| `PATCH /api/studio/enquiries/{id}` | any of `{state, assigned_to, read}` | the enquiry |
| `POST /api/studio/enquiries/{id}/replies` | `{body}` | the enquiry, now `answered` |
| `POST /api/studio/invitations` | `{email, role, display_name}` | `201` with `{id, email, role, invite_url, expires_at}` |
| `GET /api/studio/accounts` | none | public account shapes |
| `GET /api/studio/outbox` | none | every message, newest first |
| `POST /api/studio/sectors` | `{token, label}` | `201` with the sector |
| `PATCH /api/studio/sectors/{id}` | `{label}` | the sector |
| `DELETE /api/studio/sectors/{id}` | none | success with no body; a conflict while any case file or client entry uses it |
| `POST /api/studio/clients` | `{sector, name}` | `201` with the client entry |
| `DELETE /api/studio/clients/{id}` | none | success with no body |
| `PATCH /api/studio/notice-rows/{id}` | any of `{label, body}` | the row |
| `GET /api/studio/export` | none | `{accounts, sectors, clients, case_files, chapters, information_items, awards, notice_rows, enquiries, subscribers, messages}` |
| `GET /api/studio/events` | `name` | `[{id, name, properties, created_at}]` |
| `GET /api/studio/examples` | none | `{present, count}` |
| `POST /api/studio/examples/remove` | none | success with no body |

Endpoint roles: every `/api/studio/...` endpoint needs an author or editor session; an author may read and write only case files they own (and their chapters and media), may create case files, and is refused on the grid order, the enquiries, the invitations, the accounts list, the outbox, the sectors, the clients, the notice rows, the export, the events, the examples, and on delete, publish, unpublish, approve and return. The shortlist, messages, `GET /api/enquiries/mine` and the account endpoints need any session; an account may change only itself unless the caller is an editor.

### No mocks

Any of the following is a contract violation however good the interface looks: image bytes written to the app container's filesystem or into a database column; a bucket key that is not the SHA-256 of the bytes; a public or presigned bucket address handed to the browser; a case file list filtered only in the browser while the API returns unpublished rows; a role check that exists only in the interface; a message shown on screen that was never stored; an analytics call to a third party; a hardcoded `{"access_token": ...}` the app returns to itself. The named providers are the fact: the app's interface and its own tables can only reflect what lives in PostgreSQL and in the MinIO bucket, never substitute for it.

## Definition of done

A stranger can open Facet, turn the crystal, open the menu, filter the work by sector and read a published case file at its own address. A studio author can write a case file, have it returned, approved and published by an editor, and a fresh browser sees it on the grid; when the author rewrites and publishes changes, that browser sees the new text. Anything unpublished, and every image uploaded to it, stays unreadable to the public, and every uploaded image exists as a real object in the bucket at its content key.
