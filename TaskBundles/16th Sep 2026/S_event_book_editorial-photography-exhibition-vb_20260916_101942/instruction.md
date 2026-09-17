# The New Hollywood Photography Exhibition

Build and deploy a working web application from this brief. There is no starting codebase. When you
are done, a stranger must be able to open the app in a browser, fall through the title sequence into
one of two galleries, open a portrait to its caption, sign up, keep that portrait in a personal
selection, and reserve a timed visit that comes back with a reservation code, without hitting an error
page. The last place in an entry time goes to exactly one visitor however many ask for it at the same
moment: the reservation must exist as a real row in `reservations` in `postgres`, and its confirmation
must arrive as real mail in the `mailpit` inbox over SMTP. A code the page draws for itself is not a
reservation, and a saved frame that lives only in the browser is not a selection.

## Overview

The New Hollywood Photography Exhibition is the single-visit web front door to a photography show
mounted by two magazines, AURA and Gazette, inside Beacon Tower in New York City. Its job is not to
sell anything. It makes a gallery of magazine photography feel like walking into a darkened room where
the pictures arrive one at a time: a cinematic entrance, a choice of two rooms, a wall text, and then
the work. Everything is staged on a near-black or bare pale grey ground with a single pink accent and
a constant film grain over every route.

Four audiences use it. Culture and press readers come for the show and its framing, which the landing
title sequence and the two introductions serve. Photography and fashion followers come for the images,
which the two galleries and the frame detail serve. Prospective visitors come for where and when, and
a way in, which the menu overlay and the visit reservation serve. Return visitors come back for the
frames they kept, which the personal selection serves. The primary actions, in order: enter the
exhibition by scrolling the title sequence to the gallery chooser, choose a gallery, open a frame to its
detail, save a frame to a personal selection, and reserve a timed visit.

It is deliberately not a ticket shop, not a social product and not a content management system: no
prices, no payment, no comments, no likes, no sharing, no uploads, no staff console and no editing of
galleries, frames or entry times inside the app. Every photograph is a generated stand-in; no image,
font, audio or video file is ever served.

The genuinely hard part is the last place in a timed entry: two visitors asking for it at the same
instant must never both be confirmed, and the places booked for an entry time must never exceed its
capacity.

## User roles

| Role | Can do |
|---|---|
| Anyone, signed out | Open every route except `/selection`, walk the title sequence, read both introductions, scroll both galleries, open any frame to its detail, read the entry times and the places left on `/visit`, read the privacy and terms pages, and create an account. **Cannot** save a frame, read or change any selection, reserve a visit, or read or cancel any reservation. |
| `visitor` | Everything a signed-out person can do, plus save and remove frames in their own selection, reserve timed visits, list their own reservations and cancel their own reservations. **Cannot** read or change another visitor's selection, and **cannot** read or cancel another visitor's reservation. |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a button in the UI is not authorization: a direct API call from a signed-out session to any visitor-only endpoint must be rejected by the server (an unauthorized request is denied, not served), leaving the protected state unchanged.

Ownership is enforced the same way: a direct API call from one visitor against another visitor's
reservation is denied, and the reservation row does not change. A visitor's selection and reservation
lists only ever contain that visitor's own rows.

Signup is open: anyone can create a `visitor` account at `/signup`. Three visitors are seeded:
`visitor@example.com` (display name `Nadia Rowe`), `visitor2@example.com` (`Omar Lindgren`) and
`visitor3@example.com` (`Hana Petrov`). Every seeded account signs in with the password
`deku-demo-pw-2026`.

## Core features

### Accounts and sign in

1. `POST /api/auth/signup` with `email`, `password` and `displayName` creates a visitor and returns
   `{id, email, displayName}`. The email is stored lowercased.
2. A signup with an email that is already registered, in any letter case, is rejected as invalid and
   creates no second visitor.
3. A signup with a password shorter than 10 characters is rejected as invalid, naming `password`, and
   creates no visitor. A malformed email is rejected as invalid, naming `email`. An email is well formed
   when it has one `@`, at least one character before it, and after it a domain that contains a dot.
   A `displayName` that is empty or longer than 60 characters is rejected as invalid, naming
   `displayName`, and creates no visitor.
4. `POST /api/auth/login` with a correct email and password returns a JSON object carrying
   `access_token`. A wrong password is denied, and the refusal is identical to the refusal for an email
   that is not registered, so it never says which half of the pair was wrong.
5. Every visitor-only API call carries an `Authorization` header of `Bearer`, a space and the token. A
   missing or malformed token is denied.
6. `GET /api/me` returns `{id, email, displayName}` for the token's visitor.
7. Passwords are stored hashed, never as written.
8. The signup form at `/signup` has fields labelled `Email`, `Password` and `Display name` and a
   `Create account` button; the sign-in form at `/login` has `Email` and `Password`, a `Sign in`
   button, and a `Create an account` link to `/signup`. A successful signup signs the visitor in.

### The landing: title lock-up, title sequence and gallery chooser

9. `/` has the document title `The New Hollywood Photography Exhibition`. On arrival it shows, centred
   over black, the lock-up: a small `THE`, the partner titles `AURA` and `Gazette` joined by a
   handwritten script `and`, and `HOLLYWOOD` set largest in muted grey beneath them.
10. Beneath the lock-up a two-line subtitle reads `As seen in the Beacon Tower, located in` and
    `New York City`, and a small ring turns steadily beneath them while the page is at rest.
11. Scrolling runs the title sequence: a scatter of tilted photographic planes travels out of depth
    toward the viewer, turning and growing, a few passing close enough to fill a third of the frame,
    until the field resolves into two upright covers standing side by side. The sequence follows the
    scroll position exactly, and scrolling back up runs it in reverse into the lock-up.
12. The settled state is the gallery chooser: the prompt `Choose which gallery you want to explore`
    above two covers. The left cover is AURA and opens `/aura-intro`; the right cover is Gazette and
    opens `/gazette-intro`. Both covers are links a keyboard can reach and activate.
13. The landing carries no header and no menu control: only the ring, the grain, the pointer mark and
    the sequence.

### The gallery introductions

14. `/aura-intro` has the document title `AURA: The New Hollywood`, and `/gazette-intro` has
    `Gazette Goes to Hollywood`. Both sit on the deep neutral introduction ground.
15. Each introduction opens on a stacked display heading reading `THE`, `NEW`, `HOLLYWOOD`, one word
    per line.
16. Each introduction carries a three-paragraph manifesto that reveals character by character as the
    visitor scrolls it into view and un-reveals as it scrolls away. The AURA manifesto reads exactly:

    > AURA has long been a partner for women in Hollywood, to connect, to provoke, to move the cultural needle. In these photographs, taken from 2018 to 2025, their growing power dominates every frame.
    >
    > The old binary, serious actress or brand-builder, artistic or commercial, has collapsed. In its place stands a new kind of force: the multihyphenate woman who shapes her own image and owns the infrastructure behind it.
    >
    > Performers like Odessa Vane, Lilou Marchetti and Priya Castellane no longer merely take roles: they choose them, develop them and use their visibility to elevate passion projects. Their legacy is built on craft, but also on never surrendering the narrative.

    The Gazette manifesto reads exactly:

    > Gazette has spent decades writing about the men of Hollywood, to question them, to celebrate them, to take their measure. In these photographs, taken from 2018 to 2025, a different kind of leading man steps into the light.
    >
    > The old script, the tough guy or the heartthrob, the star or the character actor, has been torn up. In its place stands a performer who is allowed to be tender, strange and funny in the same frame, and who chooses which of those the camera sees.
    >
    > Actors like Rafe Okonkwo, Teodor Lindqvist and Marcus Delacroix-Bell no longer wait for the part to find them: they write it, produce it and carry it to the screen. Their legacy is built on range, and on the nerve to let an audience see them change.

17. Below the manifesto a hand-drawn signature draws itself on, stroke by stroke, over a two-line
    credit: `Photographs by Celine Armand` and `for AURA` on the AURA introduction,
    `Photographs by Tomas Ekwueme` and `for Gazette` on the Gazette introduction. There is no other
    footer: no link row, no social bar.
18. At the foot of each introduction a single filled `Go to Gallery` button is the advance from the wall text to that title's gallery:
    `/aura` from `/aura-intro`, `/gazette` from `/gazette-intro`.

### The galleries

19. `/aura` has the document title `AURA: The New Hollywood`; `/gazette` has `Gazette Goes to
    Hollywood`. Each opens on its partner wordmark set enormous in muted grey, filling most of the
    width: `AURA` upright in the display serif on a near-black ground, `Gazette` in the swash display
    face on a pale grey ground.
20. Above the wordmark sits the prompt `Scroll to explore`, shown in capitals, which fades as the first
    photographs enter.
21. A fixed header on each gallery carries the text controls `View` and `Menu` and the sound control,
    in the interface grotesque. The header slides up out of view while the visitor scrolls down and slides back while
    the visitor scrolls up, without shifting the layout beneath it.
22. Below the wordmark the gallery is one column of full-bleed photographs in the gallery's order, each
    filling its frame width from the centre and cropping rather than letterboxing. Over each photograph
    the partner masthead is set as live text: white on AURA frames, the pink accent on Gazette frames.
23. Every frame is exposed to assistive technology as an image whose alternative text reads
    the subject, a comma, the words `photographed by` and the photographer, for example
    `Odessa Vane, photographed by Celine Armand`.
    The film grain, the pointer mark, the drawn strokes, the title-sequence planes and the individual
    split characters are decorative non-content graphics and are hidden from assistive technology.
24. Pressing `View` in the header turns view mode on: every frame in the column shows a visible `View`
    label, which is how a keyboard or touch visitor finds what can be opened. Pressing `View` again
    turns the labels off. Every frame can be opened by pointer, by tap and by pressing Enter when it
    has focus.
25. `GET /api/galleries` returns the two galleries in order and `GET /api/galleries/{slug}` returns one
    gallery with its introduction and its frames in column order. An unknown slug answers not-found.
    `GET /api/frames/{id}` returns one frame; an unknown id answers not-found.

### The frame detail

26. Opening a frame shows it large and centred over a dimmed, grain-covered ground, above the page and
    below the pointer mark, with its caption: the subject, the photographer, the publication and the
    year. For the first AURA frame the caption carries `Odessa Vane`, `Celine Armand`, `AURA` and `2025`.
27. `Previous` and `Next` controls, and the left and right arrow keys, move to the neighbouring frame in
    the same gallery without closing. `Previous` on the first frame and `Next` on the last frame are
    unavailable; the sequence does not wrap.
28. A `Close` control drawn as a thin cross, and the Escape key, close the detail and return the visitor
    to the gallery at that frame's place in the column, with the header restored.
29. While the detail is open, keyboard focus stays inside it; on close, focus returns to the frame that
    was opened.
30. The detail carries the save control described under the personal selection.

### The menu overlay

31. `Menu` appears in the header of both galleries, both introductions, `/selection`, `/visit`,
    `/privacy` and `/terms`. Pressing it opens a full-screen overlay above the page and below the
    pointer mark, and the `Menu` control becomes a thin cross labelled `Close`. Escape also closes it.
32. The overlay carries these links, set in the display serif at heading scale and revealing letter by
    letter as it opens: `AURA gallery` to `/aura`, `AURA introduction` to `/aura-intro`,
    `Gazette gallery` to `/gazette`, `Gazette introduction` to `/gazette-intro`, `Reserve a visit` to
    `/visit`, `Your selection` to `/selection`, `Privacy` to `/privacy` and `Terms` to `/terms`.
33. `Your selection` shows beside it the number of frames the signed-in visitor has saved, and that
    number changes the moment a frame is saved or removed, without a reload.
34. The overlay states the exhibition facts: `The New Hollywood Photography Exhibition`, `Beacon Tower`,
    `New York City`, and the run as its first date, the word `to` and its last date, both written
    `YYYY-MM-DD`.
    `GET /api/exhibition` returns `{title, venue, city, runStart, runEnd}`.
35. Signed out, the overlay offers `Sign in` to `/login`; signed in, it shows the visitor's display name
    and `Sign out`, which ends the session and returns to `/`.
36. Closing the overlay returns the visitor to the exact scroll position they left.

### The personal selection

37. A signed-in visitor saves a frame with a `Save to selection` control on the frame detail. The
    control reads `Saved` the moment it is pressed, before the server answers; if the write fails the
    control returns to `Save to selection` and a short message says the frame was not saved.
    Pressing `Saved` removes the frame again.
38. Pressing `Save to selection` while signed out opens `/login`, and a successful sign in returns the
    visitor to the gallery they came from.
39. `POST /api/selection` with `{frameId, galleryId, action}` saves or removes a frame, where
    `galleryId` is the gallery slug (`aura` or `gazette`) and `action` is `add` or `remove`. A
    successful write returns `{ok: true, selection: [{frameId, galleryId, savedAt}]}` carrying the
    visitor's whole selection, newest first.
40. A frame appears in one visitor's selection at most once: adding a frame that is already saved
    returns success and leaves exactly one row in `selections`. Removing a frame that is not saved
    returns success and changes nothing.
41. An unknown `frameId`, a `galleryId` that is not the frame's own gallery, or an `action` other than
    `add` or `remove` is rejected as invalid with `{ok: false, message}`, and nothing is written.
42. `GET /api/selection` returns the signed-in visitor's own saved frames as
    `[{frameId, galleryId, savedAt}]`, newest first, and never another visitor's frames. The selection
    survives a reload and a new sign in.
43. `/selection` shows the saved frames as a grid. Each tile opens that frame's detail and carries a
    `Remove` control. With nothing saved the page reads `Nothing saved yet` and links to both
    galleries. Opening `/selection` signed out lands on `/login`, and a successful sign in returns to
    `/selection`.

### The visit reservation

44. The exhibition runs for thirty days. The run starts on the UTC date before the app first started,
    so the first day of the run is already in the past. Every day of the run has five entry times,
    `10:00`, `12:00`, `14:00`, `16:00` and `18:00` UTC, and each entry time holds `8` places.
45. `GET /api/slots` lists every entry time of the run, earliest first, as
    `[{id, startsAt, capacity, placesLeft, status}]`. `placesLeft` is the capacity minus the party
    sizes of confirmed reservations for that entry time. `status` is `past` once the entry time has
    started, otherwise `full` when no place is left, otherwise `open`.
46. `/visit` shows the entry times as a calendar grid: one row per run day, one column per entry time.
    Each cell shows its time and the places left, from `8 places left` down to `2 places left`, then
    `1 place left`, or reads `Full` or `Past`. Each cell
    carries `data-slot-id` set to the entry time's id and `data-slot-state` set to `open`, `full` or
    `past`. Full and past cells cannot be chosen.
47. Choosing an open cell while signed out opens `/login` and returns to `/visit`. Signed in, it opens
    a modal form over the grid showing the chosen date and time, with fields labelled `Name` (filled
    with the display name), `Email` (filled with the account email) and `Party size` (1 to 4), and a
    submit reading `Reserve a visit`. Escape closes the modal.
48. While the reservation is being written the submit reads `Reserving` and cannot be pressed again.
    On success the modal closes, an inline banner reading `Reserved` appears at the top of
    the grid carrying the reservation code with the date and time, and the chosen cell's places left
    updates without a reload.
49. `POST /api/reservations` with `{name, email, partySize, slotId}` from a signed-in visitor confirms
    a reservation and returns `{ok: true, reservation: {id, slotId, code}}`. The row in `reservations`
    has `status` `confirmed`. The `code` is 8 characters drawn from capital letters and digits, unique
    across all reservations.
50. **The booked places for an entry time never exceed its capacity of 8.** When two visitors ask for
    the last place in the same entry time at the same moment, exactly one reservation is confirmed and
    the other is rejected with `{ok: false, field: "slotId", message}` and leaves no row. This holds for
    the rows stored in `reservations` under real concurrency, whatever the mix of party sizes.
51. A `partySize` larger than the places left, on an entry time that still has at least one place, is
    rejected naming `partySize`, and nothing is written; when no place is left the refusal names `slotId`.
    A `partySize` below 1, above 4 or not a whole number is rejected as invalid, naming `partySize`.
52. A reservation for an entry time whose status is `past` or `full` is rejected, naming `slotId`, and
    nothing is written.
53. A visitor who already holds a confirmed reservation for an entry time cannot reserve that entry time
    again: the second request is rejected, naming `slotId`, even when places remain.
54. A missing name, or one longer than 80 characters, is rejected, naming `name`; a malformed email is rejected, naming `email`. Every
    refusal is a client error carrying `{ok: false, field, message}`, the modal shows the message beside
    the named field, and the entered values stay in the form. When one request breaks several of these
    rules, the refusal names the first failing field in the order `name`, `email`, `partySize`, `slotId`.
55. A reservation request with no valid token is denied and writes nothing.
56. A confirmed reservation sends exactly one confirmation email over SMTP through `SMTP_HOST` and
    `SMTP_PORT`, delivered to the `mailpit` inbox and addressed only to the reservation's `email`, with
    no cc and no bcc. Its subject begins with `Visit reserved:` followed by a space and the reservation
    code, for example `Visit reserved: K7Q2XM4P`. Its body names `Beacon Tower`, the entry date written
    `YYYY-MM-DD`, the entry time written `HH:MM UTC`, the party size and the code. A rejected
    reservation sends no email; cancelling a reservation, signing up and saving a frame send no email.
57. `GET /api/reservations` returns the signed-in visitor's own reservations, confirmed and cancelled,
    earliest entry time first, as `[{id, slotId, code, status, name, email, partySize, startsAt}]`,
    and never another visitor's.
58. Below the grid, `Your visits` lists the signed-in visitor's reservations with the code, the date and
    time, the party size and the status. With none it reads `No visits reserved yet`.
59. Each confirmed visit under `Your visits` whose entry time has not started has a `Cancel visit`
    control. It first asks
    `Cancel this visit?` with `Yes, cancel` and `Keep it`; confirming calls
    `POST /api/reservations/{id}/cancel`, which returns `{ok: true, reservation: {id, slotId, code, status}}`
    with `status` `cancelled`, and that entry time's places return at once.
60. Cancelling a reservation that is already cancelled, or whose entry time has already started, is
    rejected as invalid and changes nothing. Cancelling an id that matches no reservation answers
    not-found.
    Cancelling another visitor's reservation is denied, the row stays `confirmed` and the places left
    do not change.

### The not-found page

61. Every path that is not a page route in the User flow route table, an endpoint under API shapes, or a
    static file the pages load, including analytics collection paths and shortened alias fragments,
    answers not-found with the product's own not-found document.
62. The not-found document keeps the grain and the pointer mark, carries no gallery body and no header,
    and shows centred: `404`, `Page Not Found`, `You may have made a mistake.`, `This page does not exist.`
    and a single `Back to Homepage` link to `/` whose letters reveal one at a time.

### Privacy and terms

63. A privacy page at `/privacy` states what the exhibition keeps about a visitor: the email address,
    the display name, the saved frames and the reservations. It also states that mail is sent only to
    confirm a reservation and that the site runs no analytics. It is linked from the menu overlay and
    from the signup form.
64. A terms page at `/terms` states the visit terms: one reservation per visitor per entry time, a party
    of up to four, arrival within the hour that begins at the reserved entry time, and that a cancelled visit returns its places. It is
    linked from the signup form, which reads `By creating an account you accept the Terms`, and from the
    menu overlay.

### Forms

65. Every form in the product, the signup form, the sign-in form and the reservation modal, rejects
    invalid input inline beside the field, names the field in its message, keeps what was typed, and
    writes nothing.

### Sound

66. The product has sound, and it is gesture-gated: off until the visitor asks for it. A `Sound: off` control in the
    header of every route that has a header, and in the menu overlay, turns it on and then reads
    `Sound: on`; pressing it again turns it off. Nothing plays before that gesture, and nothing ever
    autoplays.
67. Every sound is generated in the browser, and no audio file is ever loaded. Everything in the product
    works with the sound off.

## User flow

The information architecture is eleven routes plus the not-found document.

| Route | Purpose | Auth |
|---|---|---|
| `/` | title lock-up, title sequence, gallery chooser | none |
| `/aura-intro` | AURA introduction | none |
| `/aura` | AURA gallery and frame detail | none to view, visitor to save |
| `/gazette-intro` | Gazette introduction | none |
| `/gazette` | Gazette gallery and frame detail | none to view, visitor to save |
| `/selection` | the visitor's saved frames | visitor |
| `/visit` | calendar grid of entry times, reservation modal, Your visits | none to view, visitor to reserve |
| `/signup` | create a visitor account | none |
| `/login` | sign in | none |
| `/privacy` | privacy page | none |
| `/terms` | terms page | none |
| any other path | not-found document, answers not-found | none |

**Entry and redirects.** Opening `/selection` signed out lands on `/login`, and a successful sign in
returns to `/selection`. Pressing `Save to selection` or choosing an open entry time while signed out
lands on `/login` and returns to the page the visitor came from. A successful signup signs the visitor
in and returns to `/`. `Sign out` ends the session and returns to `/`. There is no role that a visitor could be wrong for: every visitor-only route opens for any signed-in
visitor.

**Journeys.**

1. Open `/`, see the lock-up and the turning ring, scroll, watch the planes tumble and settle into two
   covers under `Choose which gallery you want to explore`, press the AURA cover, and arrive at
   `/aura-intro`.
2. On `/aura-intro` scroll the manifesto in letter by letter, see the signature draw over
   `Photographs by Celine Armand`, press `Go to Gallery`, and arrive at `/aura`.
3. On `/aura` see the `AURA` wordmark and `Scroll to explore`, scroll down and see the header slide away,
   scroll up and see it return, open `Odessa Vane` and read `Celine Armand`, `AURA` and `2025`, press
   the right arrow key to reach `Lilou Marchetti`, press Escape, and land at the same place in the column.
4. Sign in as `visitor@example.com`, open `Priya Castellane` on `/aura`, press `Save to selection`, see
   `Saved` and the menu count rise by one, reload, open `Your selection` from the menu, see
   `Priya Castellane` beside the seeded `Odessa Vane` and `Rafe Okonkwo`, press `Remove`, and see it
   leave the grid.
5. Signed in as `visitor@example.com`, open `/visit`, see tomorrow at `16:00` marked `Full` and every
   entry time of the run's first day marked `Past`, choose tomorrow at `14:00` showing `1 place left`,
   enter a party size of 2 and see the refusal beside `Party size`, change it to 1, press
   `Reserve a visit`, and see the banner carrying the reservation code; the same code appears under
   `Your visits`, and a confirmation email arrives for that address.
6. Under `Your visits` press `Cancel visit`, confirm with `Yes, cancel`, and see tomorrow at `14:00`
   show `1 place left` again.
7. Open `/nowhere`, see `404`, `Page Not Found`, both lines and `Back to Homepage`, press it, and land
   on `/`.

**States.** Every list has an empty state: `/selection` with nothing saved reads `Nothing saved yet`,
and `Your visits` with nothing reserved reads `No visits reserved yet`. Every page shows the turning
ring while its data is in flight. Errors appear as a message in place and never crash the page or show
a raw error.

## UI/UX notes

The character here belongs to this exhibition alone. The
north star: in the first moment the visitor should feel they have walked into a darkened room where
the pictures arrive one at a time. The register is editorial and cultural, so atmosphere is allowed,
but the photograph is always what is seen first. Three stances a competing product could rationally
invert: darkness over chrome, one picture at a time in the galleries over a grid of thumbnails, and slow continuous
motion over snappy feedback.

**The palette is almost colourless on purpose.** The landing ground is a near-black neutral; the
introductions and the visit page sit on a deep neutral a shade lifted from black; the Gazette gallery
is a near-white neutral pale grey room. The muted grey that carries most of the
page is a mid neutral with a faint warm cast, and it is the colour of the giant wordmarks and of
display type at rest. A light neutral grey is the secondary display tone and the hover lift. Body copy
on dark grounds is a mid neutral, captions and fine rules a darker mid neutral, and panel and filled
control surfaces a deep neutral. One mid cool neutral, a blue-leaning slate, marks secondary details, such as the run dates in the
menu overlay, and nothing else. White is the sharp exception: interface copy and the AURA mastheads. On the pale
Gazette room itself, outside the frame detail and the menu overlay that open over it, the interface
copy and the stacked interface labels rest in a deep neutral ink instead,
and the light and lighter dividers on the pale ground, wherever they appear, are near-white neutral. Translucent white veils sit behind any copy laid over a photograph. The build should weight
the page toward grey, with white as the exception.

**There is exactly one colour, and it has two jobs.** A light, vivid magenta, a hot pink, is the
Gazette masthead and the highlight on whatever the visitor is about to interact with, and it appears
nowhere else. Failure, success and in-progress on the visit page are said in words and with a small
drawn mark beside the grey scale, so meaning is never carried by colour alone and pink is never the
only signal. The exact shade of any colour is yours, so long as it holds these roles.

**Typography is an identity, so the faces and sizes are named exactly.** Six roles, kept distinct. The poster
display serif, for the wordmarks and the giant headings, and the editorial serif, for the manifesto,
are both a thin, high-contrast serif used at its thinnest weight so the wordmark hairlines survive,
named first as `Bodoni Moda` with the fallback stack `Didot`, `Times New Roman`, serif. The interface
grotesque, for controls, the chooser prompt and the not-found body, is `Inter` at weight 300 with
system-ui and sans-serif behind it. The script connector, the lowercase `and` in the lock-up, is
`Pinyon Script` falling back to cursive. The swash display, for the Gazette wordmark, is `Playfair Display`
in italic falling back to a serif italic. The micro interface face, for the scroll prompt, small
labels and the `404`, is `Inter` at weights 400 and 500. Sizes are fluid, growing smoothly with the
viewport width from a phone 375px wide to a desktop 1920px wide and holding at both ends: labels
(the form field labels) 12px to 14px, calls to action (`Go to Gallery`, `Reserve a visit` and the save
control) 14px to 16px, body (the manifesto) 16px to 20px, small headlines (the `Your visits` heading)
20px to 30px, mid headlines 36px to 54px for the menu overlay links and 35px to 60px for
`Page Not Found`, subheadlines (the chooser prompt) 30px to 40px, and the wordmarks and the
introduction heading 50px to 100px. Type never steps at a breakpoint; only layout does. Figures that
stack in columns, the places left in the calendar grid and the dates, times and codes under
`Your visits`, use tabular numerals so the digits line up.

**The product commits to dark.** The landing and the not-found page sit on the near-black ground; the
introductions, `/visit`, `/selection`, `/signup`, `/login`, `/privacy` and `/terms` sit on the deep
neutral ground; the AURA gallery is near-black; the Gazette gallery is the one pale room. There is no
alternate colour scheme and no light or dark switch.

**Shape and density.** There are exactly two corner treatments: a soft rounded corner on the filled
buttons (`Go to Gallery`, `Reserve a visit`, the save control), and fully round on the pointer dots and
the ring. Everything else is a hard-cornered, full-bleed rectangle; a third corner treatment is a
defect. The density is spacious: one photograph at a time owns the width, and nothing crowds it.

**Motion is slow, continuous and matched.** Every colour and tone change on a control glides on one
slow, symmetric house curve that is slow at both ends, with colour, background, border and outline moving
together. Small state changes use a quick default transition and are never slowed to match. One gentle
decelerating arrival is the exception. The ring turns steadily and without end, the grain shivers
constantly, letters sharpen out of a blur, scribbles draw themselves on, and the large set pieces move
only as far as the visitor scrolls and reverse when they scroll back. Under a reduced-motion preference
the letter reveals become a plain fade (the fade stays), photographs present already clear, the title
sequence presents settled on the two covers, the grain holds still on one frame, the ring stops, and
drawn strokes present fully drawn; content and order do not change.

**Components carry states, not measurements.** Buttons have resting, pointed-at (a tone lift on the
slow glide), pressed, focused and unavailable states, and unavailable is said in words, never by colour
alone. Overlays close on Escape. Cancelling a visit asks first. Icon-only controls (close, previous,
next) carry text labels for assistive technology.

**Accessibility floors are contract.** Body text meets WCAG AA contrast against its actual ground,
including any copy set over a photograph or over the pale gallery, where a translucent scrim is added
if the ground varies. Touch targets are comfortably sized, at least 44 by 44 points. Every control, the
`View` and `Menu` controls, every frame, the detail's previous, next, save and close, the menu links,
the save controls and the reservation form, works with full keyboard navigation in a logical order,
with a visible focus ring that stays visible on both the near-black and the pale grounds.

**Responsive behaviour holds at every width.** The layout is responsive, and type holds its floor at
375px wide and below and its ceiling at 1920px wide and above. On a device without hover, the pointer mark
and its halo do not exist, a tap opens a frame, and the title sequence presents settled on the two
covers. At a narrow viewport the wordmark sits at its smallest size, the gallery stays a
single full-bleed column, the header keeps `Menu` and a compact `View`, and nothing scrolls sideways.

## Front-end specification

This section carries the measured detail of the visual system. Everything here is required.

**Scaling.** One shared viewport slope drives every type size between a lower and an upper width and
clamps outside them; spacing multiples derive from one shared base unit.
Three widths were the reference points: a desktop, a tablet and a phone. The layout breakpoints step
at five widths in root-relative units plus a phone rule and a hover-capability query; those change
layout, never type size.

**Layering.** The pointer mark sits above everything. The menu overlay and the frame detail sit above
the page and below the pointer mark. The gallery header sits above the column. Decorative ground layers
sit at the bottom.

**Root state.** The root element of every page carries the class `is-fonts-ready` once the fonts have
resolved and the class `has-scrolled` once the visitor has scrolled for the first time, so entrance
timing can key off them without asking the font loader or the scroll position.

**The global chrome.** The landing carries only the ring, the grain and the pointer mark. The galleries
carry the fixed header with `View`, `Menu` and the sound control, and the scroll prompt. The credit line under each
introduction is the only footer-like element.

**The pointer mark, the cursor.** One pointer-following cursor element with four states, present only where a fine pointer
with hover exists, and never intercepting pointer events itself.
- The dot: a small circular dot centred exactly under the pointer that inverts the tone of whatever is
  beneath it, reading white over black and dark over the pale gallery, with no colour of its own.
- The halo: a larger soft round field, about four times the dot's width, that eases toward the pointer
  a beat behind the dot and also inverts what is beneath it, giving the pointer weight.
- The `View` badge: over an open-able frame or a chooser cover the dot grows into a small badge
  carrying the word `View`, and it collapses to nothing elsewhere.
- The plus mark: over a save control the badge becomes a small plus, and it inverts like the dot.

**The five motion mechanisms.** Every animated thing is one of these: declared transitions on controls
(the slow symmetric glide for tone changes, the quick default for small state changes, and the gentle
decelerating arrival as the exception); scroll-driven timelines (the title sequence, the character
reveals, the photograph reveals, the header hide); one looping keyframe spin for the ring; one looping keyframe grain
jitter; and one-shot path draws for the hand-drawn strokes, each playing forwards once and staggered.
Two heading spans additionally lift into place on a slow in-out reveal.

**The scroll system.** Raw wheel and touch input is eased into one continuous gliding scroll position.
That single position is the driver of every scroll-driven effect, so the title sequence, the reveals and
the header move in lockstep: each effect's progress through its own stretch is a pure function of how
far the visitor has scrolled, and each reverses exactly on reverse scroll. Under a reduced-motion preference the page falls back to native scrolling. Keyboard scrolling
with the arrow keys, Page Down and the space bar still moves the page.

**The title sequence.** On `/` a scroll-driven three-dimensional field of tilted photographic planes
travels from depth to the frame and resolves into the two upright covers. Each plane has its own tilt,
depth, rotation and scale, all computed from the one sequence progress; the planes are cropped by drawn
clip masks, applied in clip groups generated fresh for each build. At rest the lock-up sits centred with the ring turning beneath it,
and the ring is nudged aside across the first moments of scrolling. The prompt `Choose which gallery you
want to explore` itself resolves in, out of a blur and a lift, as the covers settle. Under a
reduced-motion preference the landing presents the settled two-cover state. The sequence exists only on
`/`.

**The character reveal.** Editorial copy, the introduction headings, the manifesto and the menu links
reveal one character at a time. Each character starts nearly invisible
and heavily blurred and clears to sharp while its opacity rises, a per-character stagger in reading order, as
its paragraph scrolls into view, and un-resolves in reverse as it leaves. The ramp runs
smoothly across neighbouring characters rather than in discrete steps. The whole phrase stays
available to assistive technology as one readable node, and the split characters are hidden from it.
Under a reduced-motion preference the blur ramp is replaced by a plain fade.

**The photographs.** No photograph file exists. Every photograph, in the galleries, the covers and the
title sequence, is a seeded procedural plane at the frame's crop: a two-stop grey gradient keyed to the
gallery ground, with a soft centred elliptical mass so a portrait crop has a subject, under the film
grain, one seed per frame so each reads as its own picture. Before the full plane resolves the frame
shows a tiny blurred low-detail stand-in of that same plane at the frame's exact shape, generated in
the page, so a frame is never empty and never pops; the full picture then rises into focus over it. The cover fit fills the frame width from the centre, cropping rather than letterboxing.
The six crops are `240x320`, `320x240`,
`280x320`, `320x200`, `200x320` and `320x160`: the portrait and landscape shapes of the editorial frames.

**The film grain.** A full-viewport grain layer runs over all content on every route, including the
photographs and the not-found page. It jitters a few percent on a short endless loop and drifts slightly
with scroll, at a strength that textures the dark grounds a little more than the pale gallery, and it
never intercepts pointer events. It is generated in the page as a fine grey turbulence, not loaded.
Under a reduced-motion preference it holds on a single static frame.

**The drawn marks.** Every mark is inline vector drawing, never a file: the two-stroke line glyph that is
the close cross and the menu cross; the open ring, about three quarters of a turn, that spins as the
loader; three loose hand-drawn underline and ring strokes that draw themselves on under words in the
display headings; the composite signature, a full word written as overlapping hand strokes with small
knockouts, drawn stroke by stroke under each introduction; and two tiny partner glyphs at label scale.
The tab icon is declared in the document head as an inline vector data address beginning
`data:image/svg+xml`, never as an icon file.

**The galleries, title by title.** AURA: near-black ground, upright display serif wordmark, white
mastheads. Gazette: pale grey ground, swash display wordmark, pink mastheads. The two galleries differ
only in ground, wordmark face and masthead colour.

**Touch and small screens.** Below the hover-capability query the pointer mark does not exist, tapping a
frame opens it, the title sequence presents settled on the two covers, and every hover
affordance has a tap equivalent.

**Performance.** The performance budget: the product stays fast, accessible and responsive, and scrolling
stays smooth on a three-year-old laptop with the gliding scroll, the character reveals, the photograph
reveals, the grain and the title sequence all running. The page's copy is readable while the ring is
still turning, not after it. Under a reduced-motion preference no looping animation keeps running.

## Technical requirements

- **Rendering model.** Every route is an HTML document rendered on the server, so the browser receives
  the page's copy on first paint; hand-written JavaScript and CSS served as static files enhance it
  with the scroll, pointer, grain, reveal, overlay and form behaviour. No front-end framework.
- **Backend.** Python 3.12 with Django 5.1 and its template engine, served in production by gunicorn 22,
  with static files served by WhiteNoise 6 from the same process.
- **Database.** PostgreSQL (`postgres`), reached through psycopg 3.2 at `DATABASE_URL`.
- **Email.** SMTP at `SMTP_HOST` and `SMTP_PORT`, authenticating with `SMTP_USER` and `SMTP_PASS` when
  they are set, delivering into Mailpit (`mailpit`).
- **Auth.** App-implemented email and password, passwords stored hashed, bearer tokens as described
  under Accounts and sign in.
- **Health.** `GET /api/health` answers `200` with `{"status": "ok"}` and needs no token.
- **Base URL and port.** `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`, read from the environment.

Use only the libraries named here plus their direct dependencies. Do not introduce a second database,
cache, queue, object store, identity provider or mail vendor: the only backing services available in
this environment are PostgreSQL (`postgres`) and Mailpit (`mailpit`), and reaching for anything else is
a contract violation.

**No asset files: the build is zero-asset.** Every file class a photography site would normally load has a procedural substitution. No image, font, audio or video file is served or downloaded on any route: the
photographs are generated planes, their placeholders are generated in the page, the marks and the tab
icon are inline vector drawing, the fonts are named in stacks and never downloaded, and every sound is
generated in the browser. No request leaves the environment at run time: no font service, no analytics,
no third-party script.

**No secrets in the browser.** Nothing the browser downloads, no page, script or stylesheet, carries a
credential: no database address, no mail server password, no password hash, and no access token other
than the signed-in visitor's own.

**One of each shared piece, across every module boundary.** Every frame, cover and plane is the same kind of
generated photograph with the same blurred arrival. `Go to Gallery`, `Reserve a visit` and the save
control share one filled, soft-cornered button look with the same slow tone glide.

## Data model

Eight tables. All timestamps are UTC. Identifiers are integers.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark fixture data, not a
secret. Hash it as normal; the exact literal must work at login, and it must be written into
`/app/USER_README.md` alongside each account so a grader can sign in.

### `visitors`
`id`; `email` (unique, stored lowercased); `password_hash`; `display_name` (1 to 60 characters);
`created_at`.

### `exhibitions`
Exactly one row. `id`; `title` = `The New Hollywood Photography Exhibition`; `venue` = `Beacon Tower`;
`city` = `New York City`; `run_start` = the UTC date before the app first started; `run_end` =
`run_start` plus 29 days.

### `galleries`
`id`; `slug` (unique: `aura` or `gazette`); `title` (`AURA` or `Gazette`); `wordmark_face` (`serif` or
`swash`); `ground` (`dark` or `pale`); `masthead_colour` (`white` or `pink`); `sort_order` (1 or 2). The
API names these `wordmarkFace`, `ground`, `mastheadColour` and `order`.

### `introductions`
`id`; `gallery_id` (unique, references `galleries`); `heading` = `THE NEW HOLLYWOOD`; `manifesto` (three
paragraphs); `photographer`. The API returns `introduction` as `{heading, manifesto, photographer}` with
`manifesto` as an array of the three paragraph strings.

### `frames`
`id`; `gallery_id`; `subject`; `photographer`; `publication` (`AURA` or `Gazette`, equal to the gallery
title); `year` (2018 to 2025); `aspect` (`portrait` or `landscape`); `crop` (one of the six crops);
`sort_order` (unique within a gallery). The API returns
`{id, galleryId, subject, photographer, publication, year, aspect, crop, order}`, with `galleryId` as
the gallery slug.

### `slots`
`id`; `starts_at` (unique); `capacity` = 8. `placesLeft` and `status` are derived on read and never
stored.

### `reservations`
`id`; `visitor_id`; `slot_id`; `guest_name` (1 to 80 characters); `guest_email`; `party_size` (1 to 4);
`code` (unique, 8 characters of capital letters and digits); `status` (`confirmed` or `cancelled`);
`created_at`; `cancelled_at`. The API names these `name`, `email`, `partySize`, `slotId` and `startsAt`.
The sum of `party_size` over confirmed rows for one slot never exceeds that slot's capacity. Two
simultaneous reservations for the last place in a slot: exactly one row is confirmed and the other
request writes nothing. A visitor has at most one confirmed row per slot.

### `selections`
`id`; `visitor_id`; `frame_id`; `saved_at`. One visitor has at most one row for a given frame; two
simultaneous saves of the same frame by the same visitor leave exactly one row.

### Seed data

| Email | Display name |
|---|---|
| `visitor@example.com` | `Nadia Rowe` |
| `visitor2@example.com` | `Omar Lindgren` |
| `visitor3@example.com` | `Hana Petrov` |

Galleries: `aura` (`AURA`, `serif`, `dark`, `white`, order 1) and `gazette` (`Gazette`, `swash`, `pale`,
`pink`, order 2). Introductions: AURA with photographer `Celine Armand` and the AURA manifesto; Gazette
with photographer `Tomas Ekwueme` and the Gazette manifesto, both exactly as written under Core features.

Frames, in column order:

| Gallery | Order | Subject | Photographer | Year | Aspect | Crop |
|---|---|---|---|---|---|---|
| `aura` | 1 | `Odessa Vane` | `Celine Armand` | 2025 | `portrait` | `240x320` |
| `aura` | 2 | `Lilou Marchetti` | `Celine Armand` | 2023 | `landscape` | `320x240` |
| `aura` | 3 | `Priya Castellane` | `Noor Haddad` | 2021 | `portrait` | `280x320` |
| `aura` | 4 | `Wren Adebayo` | `Noor Haddad` | 2019 | `landscape` | `320x200` |
| `aura` | 5 | `Saskia Moreau` | `Celine Armand` | 2020 | `portrait` | `200x320` |
| `aura` | 6 | `Ines Valcourt` | `Jun Takeda` | 2018 | `landscape` | `320x160` |
| `gazette` | 1 | `Rafe Okonkwo` | `Tomas Ekwueme` | 2024 | `portrait` | `240x320` |
| `gazette` | 2 | `Teodor Lindqvist` | `Tomas Ekwueme` | 2022 | `landscape` | `320x240` |
| `gazette` | 3 | `Marcus Delacroix-Bell` | `Ansel Varga` | 2025 | `portrait` | `280x320` |
| `gazette` | 4 | `Dario Fontaine` | `Ansel Varga` | 2019 | `landscape` | `320x200` |
| `gazette` | 5 | `Kofi Brandt` | `Tomas Ekwueme` | 2021 | `portrait` | `200x320` |
| `gazette` | 6 | `Elias Navarro` | `Jun Takeda` | 2018 | `landscape` | `320x160` |

Slots: every day of the thirty-day run at `10:00`, `12:00`, `14:00`, `16:00` and `18:00` UTC, capacity 8,
150 slots in all.

Selections: `visitor@example.com` saved `Odessa Vane` first and `Rafe Okonkwo` after it, so
`Rafe Okonkwo` lists first; `visitor2@example.com` holds
`Lilou Marchetti`.

Reservations, all `confirmed`, where tomorrow is the UTC date after the app first started and the
first run day is the UTC date before the app first started:

| Visitor | Entry time | Party size | Name | Email | Code |
|---|---|---|---|---|---|
| `visitor2@example.com` | tomorrow `14:00` | 4 | `Omar Lindgren` | `visitor2@example.com` | `SEEDA14B` |
| `visitor3@example.com` | tomorrow `14:00` | 3 | `Hana Petrov` | `visitor3@example.com` | `SEEDC14D` |
| `visitor2@example.com` | tomorrow `16:00` | 4 | `Omar Lindgren` | `visitor2@example.com` | `SEEDE16F` |
| `visitor3@example.com` | tomorrow `16:00` | 4 | `Hana Petrov` | `visitor3@example.com` | `SEEDG16H` |
| `visitor3@example.com` | first run day `10:00` | 2 | `Hana Petrov` | `visitor3@example.com` | `SEEDP10Q` |

So tomorrow at `14:00` has exactly one place left, tomorrow at `16:00` is full, every entry time of
the run's first day is past, and `SEEDP10Q` holds an entry time that has already started, so it can no
longer be cancelled.

Seeding must be idempotent: restarting the app must not duplicate rows.

## Constraints

- One exhibition, one venue, two galleries; no second exhibition and no tenancy.
- No purchase, price, payment or ticket product of any kind.
- No staff, curator or administrator accounts, and no editing of galleries, frames, introductions,
  entry times or capacities inside the app.
- No uploads and no photograph files; every photograph is a generated stand-in.
- No comments, likes, sharing, social feeds or messaging between visitors.
- No password reset, email verification or third-party sign-in.
- No analytics, tracking or third-party measurement call, and no other external network call at run
  time.
- No downloaded font, image, audio or video file on any route.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials, or an explicit statement that there are none, are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server, never a dev server.
- The server must keep running after this session ends and must not be a child of the shell. An
  ordinary background job dies with its shell, and the app will not be running when it is next
  opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is unreachable from
  outside the container.
- The backing services named in this brief are already running and reachable at their environment
  variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

| Endpoint | Request body / query | Returns |
|---|---|---|
| `GET /api/health` | none | `{"status": "ok"}` |
| `POST /api/auth/signup` | `{email, password, displayName}` | `{id, email, displayName}` |
| `POST /api/auth/login` | `{email, password}` | `{access_token}` |
| `GET /api/me` | none | `{id, email, displayName}` |
| `GET /api/exhibition` | none | `{title, venue, city, runStart, runEnd}` |
| `GET /api/galleries` | none | a top-level array of `{id, slug, title, wordmarkFace, ground, mastheadColour, order}` |
| `GET /api/galleries/{slug}` | none | `{id, slug, title, wordmarkFace, ground, mastheadColour, order, introduction, frames}`, with `introduction` as `{heading, manifesto, photographer}` and `frames` as an array of frame shapes in column order |
| `GET /api/frames/{id}` | none | `{id, galleryId, subject, photographer, publication, year, aspect, crop, order}` |
| `GET /api/selection` | none | a top-level array of `{frameId, galleryId, savedAt}` |
| `POST /api/selection` | `{frameId, galleryId, action}` | `{ok: true, selection: [{frameId, galleryId, savedAt}]}` |
| `GET /api/slots` | none | a top-level array of `{id, startsAt, capacity, placesLeft, status}` |
| `POST /api/reservations` | `{name, email, partySize, slotId}` | `{ok: true, reservation: {id, slotId, code}}` |
| `GET /api/reservations` | none | a top-level array of `{id, slotId, code, status, name, email, partySize, startsAt}` |
| `POST /api/reservations/{id}/cancel` | none | `{ok: true, reservation: {id, slotId, code, status}}` |

Field names are exact. `startsAt` and `savedAt` are ISO 8601 UTC; `runStart` and `runEnd` are
`YYYY-MM-DD`. A successful call returns the named resource or shape. An invalid or unauthorized call is
rejected as a client error, never as a server error and never as a silent success; the selection and
reservation writes carry `{ok: false, message}` on refusal, and the reservation write adds `field`.
Bearer auth is carried on `GET /api/me`, both selection endpoints and every reservation endpoint;
health, signup, login, the exhibition, the galleries, the frames and the slots need no token.

### No mocks

The named providers are the fact, and the app's own screens can only reflect what lives in them, never
substitute for them. Each of the following is a contract violation:

- a selection or reservation held in browser storage, a process variable or an in-memory list instead
  of rows in `selections` and `reservations`
- a places-left figure kept as a stored counter, or computed in the browser, instead of from the
  confirmed rows
- a confirmation email written to a log, a file or a table instead of delivered over SMTP to `mailpit`
- a reservation code the page invents without a confirmed row behind it
- a photograph, font, sound or icon file shipped with the app

A confirmed reservation must exist as a row in `reservations` with its code, and its confirmation must
exist as real mail in the `mailpit` inbox addressed to the reservation's email.

## Definition of done

A visitor can fall through the title sequence into either gallery, open any portrait to its caption and
step through the set, create an account, keep portraits in a selection that survives a reload, and
reserve a timed visit that confirms with a code and a confirmation email. When two visitors ask for the
last place in an entry time at the same moment, exactly one of them gets it.
