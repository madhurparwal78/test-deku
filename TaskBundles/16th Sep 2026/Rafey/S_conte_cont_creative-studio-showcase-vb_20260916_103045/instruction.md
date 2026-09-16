# Naught'

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the site in a browser, scroll
the home route to the showreel, open a case study from the featured rail, read it, press
`book a call`, and file an enquiry, without hitting an error page. A studio author must be
able to sign in, create a case study as a draft, upload its cover image, and publish it so it
appears in the catalogue. Until that moment the draft, and every image it owns, must be
unreadable to anyone who is not a studio author, by any means, including a direct request
for the image's exact storage key. The image has to be a real object in the object store:
bytes kept anywhere else do not count.

## Overview

Naught' is the public site of a small creative studio in Milan that sells brand identities,
campaigns, digital experiences, events and visual systems. The site is itself a piece of
work: it is trying to demonstrate craft rather than describe it, in about ninety seconds of
scrolling, and then to be easy to contact. The studio is named after the word for nothing,
and the manifesto turns that into a paradox.

The public site has four templates. A home route that scrolls like a short film and doubles
as the manifesto. A works index of seven case studies. A case study route for each project.
And a playful not-found route. Two films carry the emotional weight: a showreel that grows
out of a rendered room, and a manifesto film with decaying typography over it. Both play
muted until the visitor asks for sound.

It serves, in the site's own order: a brand or marketing lead deciding whether the studio is
good; the same person comparing studios in the catalogue; a reader who has decided and
reaches for `book a call`; a recruit or collaborator reading the people and the credits; and
a visitor who mistyped a path. Behind the public site, studio authors keep each case study as
a draft until it is ready, upload its cover and gallery images to object storage, publish it,
and read the enquiries that booking a call files.

The commercial shape is services, not products. Nothing is priced, nothing is sold on the
page, and there is no pricing, search, newsletter, comments, sharing, shop or second language.
The conversion event is a booked call, and the site gives it a button in the menu overlay, in
the hero, at the foot of every route and in a closing panel of its own.

The genuinely hard part is twofold. The home route is choreographed from scroll position
almost pixel for pixel, reversibly and without easing. And publication is the only act that
exposes a case study: a draft's route, its record and its images answer as missing to
everyone but a studio author.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| `author` | Sign in to the studio console; create a case study as a draft; edit any case study; upload and remove its cover and gallery images; publish and unpublish it; mark it featured; read every enquiry; change an enquiry's status; read the page view record; read a draft case study and its images | **Cannot create another account with the `author` role through any route. Cannot delete an enquiry.** |
| `reader` | Everything a visitor can do; book a call signed in, so the enquiry is attached to the account; read their own enquiries and their status at `/account` | **Cannot reach the studio console. Cannot read any draft case study or any draft image. Cannot read another reader's enquiries. Cannot change any enquiry's status. Cannot create, edit, publish or upload anything.** |

A visitor with no account reads the whole public site, uses the menu, the sound toggle and
the mail link, and books a call. That is not a role, and it grants nothing else: a visitor
cannot read a draft or any enquiry.

Authorization is enforced **server-side on every mutating endpoint**. Hiding a control in the
UI is not authorization: a direct API call from a `reader` session to any `author`-only
endpoint must be rejected by the server (an unauthorized request is denied, not served),
leaving the protected state unchanged.

A request for a draft case study, a draft image, or another reader's enquiry is answered as a
missing record, never as a refusal, because a refusal confirms the thing exists.

Signup is **open**. Anyone can create an account with a display name, an email address and a
password from `/sign-up`, and the account is usable at once as a `reader`. The `author` role is
assigned where the accounts are, and no route grants it.

Three accounts are seeded, and every seeded account uses the password `deku-demo-pw-2026`.

| Email | Display name | Role |
|---|---|---|
| `author@example.com` | Lena March | `author` |
| `reader@example.com` | Paolo Ferri | `reader` |
| `reader2@example.com` | Ada Rinaldi | `reader` |

`reader2@example.com` exists so that isolation is observable: its enquiry must read as missing
to `reader@example.com`, and the draft case study must read as missing to both.
## Core features

### Drafts and publication

A case study is in one of two states, `draft` or `published`, and no other. It is created as
a draft. Publishing is the only act that exposes it, and unpublishing returns it to draft.

1. **A draft is unreadable to anyone who is not a studio author.** Its route
   `/works/<slug>` renders the not-found template with status `404`. `GET /api/works/<slug>`
   answers `404`. It is absent from `GET /api/works`, from the catalogue, from the home
   route's featured rail, from every next-subject row and from every compact list. A request
   for any of its images, including by the image's exact storage key, answers `404`. The
   object itself stays in the store, untouched.
2. **Publishing exposes all of it at once.** After `POST /api/works/{id}/publish` the route
   answers `200`, the record appears in `GET /api/works` in ordinal order, the card appears
   in the catalogue, and every one of its images is served.
3. **Unpublishing withdraws all of it at once**, with the same effect as rule 1, and leaves
   every stored object in place so that republishing needs no re-upload.
4. **A studio author reads a draft as it will look.** Signed in as an `author`, the draft's
   route renders the case study, and its images are served.
5. **The ordinal is stored, never derived.** Every case study carries an ordinal from `1` to
   `99`, printed `W'` and two digits. Unpublishing one case study renumbers nothing; the
   catalogue and the next-subject rows close over the gap.

Seven case studies are published and one is a draft. The draft is `Veloce`, ordinal `W'08`.

### Media in the object store

Every cover and gallery image is an object in the store, and its bytes live nowhere else: not
on the application's filesystem and not in the database. The object key is
`works/{work_id}/{sha256_of_bytes}.{ext}`, where `sha256_of_bytes` is the lowercase hex digest
of the uploaded bytes and `ext` is `png`, `jpg` or `webp` from the content type. For example,
a PNG whose digest begins `9f2a` uploaded to the case study with id `3` is stored at
`works/3/9f2a...d0.png`.

Images reach a browser through `GET /media/<storage key>`, which streams the object from the
store. That route is the only way an image is read: the bucket is private, and an anonymous
request straight to the store is refused. The route serves an image whose case study is
published to anyone, serves a draft's image to a studio author, and answers `404` to everyone
else.

An author uploads with `POST /api/works/{id}/media`, giving the file, whether it is the
`cover` or a `gallery` image, a written description, and for a gallery image its layout, its
optional band colour and its optional caption. Uploading the same bytes twice to one case study
stores one object. Removing an image removes its record and its object.

Every image's description is written per image and stored, never generated. It becomes the
image's alternative text.

The application seeds its own images. When it starts with an empty store it generates one
cover and four gallery stand-ins per case study from the recipe in
`## Front-end specification`, and writes each under the key scheme above. No image file ships
in the source.

### Booking a call

`book a call` opens a panel that slides over the current route from the right, without
leaving it. The panel asks for a name, an email address, an optional company, the service of
interest (one of the five services), a preferred date, a time window of `morning` or
`afternoon`, and a message. Submitting files an enquiry with `POST /api/enquiries` and replaces
the form with the line `Thanks. We'll be in touch within one working day.`

| Field | Rule | Message when broken |
|---|---|---|
| name | required, `1` to `80` characters after trimming | `Tell us your name` |
| email | required, a valid address, trimmed and lowercased | `We need an email to reply to` |
| company | optional, at most `80` characters | `That company name is too long` |
| service | required, one of the five service labels | `Pick what you have in mind` |
| preferred date | required, today or later | `Pick a date from today on` |
| time window | required, `morning` or `afternoon` | `Pick a time of day` |
| message | required, `1` to `1000` characters after trimming | `Say a little about the project` |

A rejected submission files nothing, keeps every value the visitor typed, and shows each
message beside its field.

Anyone can book a call. When a signed-in `reader` books, the enquiry is attached to that
account, and it appears at `/account` with its status. A new enquiry's status is `new`; a
studio author moves it to `contacted` and then `closed`.

`drop us an email` is a mail link to `studio@example.com`. It opens the visitor's mail client
and files nothing.

### Identity

Email and password. `/sign-up` asks for a display name of `1` to `60` characters, an email
address and a password of `8` to `200` characters, and creates a `reader`. `/sign-in` signs any
account in. A wrong password and an unknown address answer with the same message:
`That email and password do not match`. An address already registered answers
`That email is already registered`.

Signing in returns a bearer token for the API and sets an HTTP-only session cookie for pages;
the API accepts either. Signing out ends both.

`/account` and `/studio` without a session redirect to `/sign-in` with a `next` parameter and
return there after signing in. A `reader` asking for any `/studio` route gets the not-found
template with `404`. An `author` asking for `/account` is redirected to `/studio`.

### The studio console

`/studio` lists every case study, draft and published, as cards in ordinal order: the
eyebrow, the tagline, the cover, a state label reading `Draft` or `Published`, and a featured
switch. `New case study` opens the same slide-over panel the booking form uses, holding the
case study fields; saving creates a draft. Choosing a card opens the panel with that case
study, its images and an upload control.

The panel's `Publish` and `Unpublish` controls wait for the service before the card changes,
because each changes what the public can read. The featured switch changes the card at once
and returns to its previous position, with the message `Could not save that change`, if the
service refuses.

`/studio/enquiries` lists every enquiry, newest first, one row each: the name, the email, the
company, the service, the preferred date and time window, the first line of the message, the
filed date, and a status control. Changing a status changes the row at once and rolls back with
`Could not save that change` if the service refuses.

The home route's featured rail shows exactly the published case studies marked featured, in
ordinal order, at most five.

### The home route

Thirteen bands in one scrolling document, specified in `## Front-end specification`. The ground
is white for the first band and black for every band after it, and it never switches back. The
featured rail's `View all` control shows the count of published case studies as two digits in
parentheses, `( 07 )` with the seed, read from the catalogue rather than from the rail.

### The works index

`/works` lists every published case study as a card, in ordinal order, under the masthead
`Works` beside the copyright range `©24 . 26` at the same size. The whole card is the link to
its case study.

### The case study route

`/works/<slug>` serves a published case study: the masthead with its title and ordinal; the
year range and disciplines; the brief; the concept; the gallery bands in order; `All Works`
with a corner arrow; the credits; a centred closing panel; the next published case study's
masthead as a link, wrapping from the last ordinal to the first; and a compact list of every
other published case study, one row each, name and ordinal digit, omitting the current one.

A case study with no gallery images renders no gallery and no placeholder text.

### The not-found route

Any path that does not resolve to the home route, the works index, a published case study,
the privacy page, the identity routes or a console route the requester may reach renders the
not-found template, with the full chrome and overlay, and answers `404`. Its document title is
`Naught' to see here...`. Its body is the scattered letters of `ERROR 404`, a visually hidden
heading reading `ERROR 404` for assistive technology, and one pill reading `Homepage` that
returns to `/`.

### Films and sound

Two films: the showreel on the home route and the manifesto film below it. Every film plays
without a gesture, muted, looping, with no controls, no poster flash and no play button, and
starts muted again on every route change. A `SOUND` toggle appears at the top centre of the
window only while a film is on screen; it is the only way sound is ever turned on, its state
lasts for the session and does not survive into a new one, and it announces its state to
assistive technology as a toggle button that reads as pressed while sound is on. No film is
fetched until its band is within two window heights of the window. Each film is a `video`
element, the stand-in's drawing surface streamed into it, so a supplied film later replaces
only its source.

The films are generated stand-ins, specified in `## Front-end specification`, because the
footage is the studio's to supply.

### The privacy page

`/privacy` is linked from the footer of every public route. It states what the studio keeps
when a visitor books a call (the name, email, company, service, preferred date and time window
and message), why (to reply and arrange the call), how long (twelve months after the enquiry is
closed), that page views are recorded by route and time without identifying anybody, and that
`studio@example.com` is where to ask for a record to be deleted.

### Page views

Every public page view is recorded with its route, stored as the path such as `/works`, and
the instant it was served. A studio
author reads the record at `GET /api/page-views`, filtered by route. Nobody else can read it,
and it carries nothing that identifies a visitor. No third-party analytics runs anywhere, so
no consent banner is needed; the record is the site's only measurement.

### Links and previews

Every internal link on every public route resolves to a page that answers `200`. Every public
route declares its own social preview title and image in the document head, and the image
address answers `200` with an image: a case study uses its cover, and every other route uses a
preview image the application generates.
## User flow

### Routes

| Route | Title | What it is |
|---|---|---|
| `/` | `Naught' \| Home` | The home route. Thirteen bands |
| `/works` | `Naught' \| Works` | The works index of published case studies |
| `/works/<slug>` | `Naught' \| ` and the case study title | A published case study, or a draft for an author |
| `/privacy` | `Naught' \| Privacy` | What the studio keeps and why |
| `/sign-in` | `Naught' \| Sign in` | Sign in, with an optional `next` path |
| `/sign-up` | `Naught' \| Sign up` | Create a reader account |
| `/account` | `Naught' \| Your enquiries` | A reader's own enquiries |
| `/studio` | `Naught' \| Studio` | An author's case studies as cards |
| `/studio/enquiries` | `Naught' \| Enquiries` | An author's enquiry inbox |
| anything else | `Naught' to see here...` | The not-found template, answering `404` |

The title separator is a space, a vertical bar and a space. There are exactly five ways to move
between the public routes: the header mark to `/`; the menu overlay to `/`, `/works` or the two
contact actions; a featured card on `/` to its case study; `View all` on `/` to `/works`; and
`All Works` on a case study to `/works`. Plus one that does not look like a link: the next case
study's masthead at the foot of a case study.

The menu overlay's first row is the only conditional row on the site: it reads `home` on every
route except `/`, where it reads `works`.

### Entry and redirects

| Route | Visitor | Reader | Author |
|---|---|---|---|
| public routes | renders | renders | renders |
| `/works/<slug>`, draft | not found, `404` | not found, `404` | renders |
| `/sign-in`, `/sign-up` | renders | redirect to `/account` | redirect to `/studio` |
| `/account` | redirect to `/sign-in?next=/account` | renders | redirect to `/studio` |
| `/studio`, `/studio/enquiries` | redirect to `/sign-in?next=/studio` | not found, `404` | renders |

A `next` value is used only when it is a path on this site beginning with a single `/`; any
other value sends the visitor to `/`.

### Journeys

**A visitor decides.** They open `/` and see the studio initial and its apostrophe alone on a
white screen while the page loads. The cover lifts, the two-line claim and the black
`book a call` pill arrive, and the full wordmark fills the width. They scroll: the ground turns
black, two headline pairs pass, the word `works` assembles, five featured cards unzip in two
staggered columns, and the showreel grows out of a room until it fills the window while the
`SOUND` toggle appears. They open the `Solace` card and read the brief and the concept. At the
foot they press `book a call`, fill the slide-over and submit, and the form is replaced by the
thanks line.

**A reader follows up.** They sign up at `/sign-up`, book a call while signed in, and open
`/account`, where the enquiry is listed with its service, its preferred date and time window,
and the status `new`.

**An author publishes.** They sign in as `author@example.com` and land on `/studio`. They open
`New case study`, fill the panel and save, and a card labelled `Draft` appears. They upload a
cover. Signed out, in another browser, the case study's address answers not found. Back in the
console they press `Publish`; the card reads `Published`, and the case study appears in
`/works` at its ordinal, with its cover.

**An author answers.** They open `/studio/enquiries`, find the newest enquiry at the top, and
set its status to `contacted`; the row changes at once.

**A visitor gets lost.** They type `/nowhere`. The not-found page answers `404`, shows scattered
letters that turn out to spell `ERROR 404` once the pointer moves, and offers `Homepage`.

### States

| Surface | Loading | Empty | Error |
|---|---|---|---|
| Any public route | the studio initial and its apostrophe, centred, spinning slowly, on the route's opening ground | not reachable | the not-found template for a missing record |
| The booking panel | the submit control reads `Sending` and every field is disabled | the form | each message beside its field, values kept |
| `/account` | the list area is blank until the enquiries arrive | `No enquiries yet.` with a `book a call` pill | `Could not load your enquiries.` |
| `/studio` | cards appear as they load | `No case studies yet.` with `New case study` | `Could not load case studies.` |
| `/studio/enquiries` | rows appear as they load | `No enquiries yet.` | `Could not load enquiries.` |
## UI/UX notes

A visitor should understand within one window that this studio is good at making things feel
made. The register is editorial and cinematic rather than operational: the work and the
studio's name are seen first, almost nothing sits on top of them, and the page behaves like a
film the visitor scrolls. Where a judgement is close, the tiebreak is craft over convenience on
the public routes, and plain legibility in the studio console and the account page.

**Two grounds and no third.** Every band on every route is either a near-white neutral ground
with near-black neutral marks, or a near-black neutral ground with near-white neutral marks.
There is no grey card on black and no pale card on white; depth comes from imagery and scale,
never from a raised surface. One light neutral carries the eyebrow above each case study
tagline and secondary meta, and on the dark ground it is lifted to a near-white neutral so that
it meets the contrast bar below. Two deep neutrals set fine print on a near-white band. A
second near-white neutral, faintly warm, is carried as a named token, and a third near-white
neutral is the off-white the light bands actually sit on. Secondary type is white or black
turned down in strength rather than a mixed grey. Hairlines use a near-white neutral. A mid,
vivid green exists only as a status token for the studio console's saved state and never
appears on a public route. The home route opens white,
turns black after the hero and stays black; the works index and the not-found route are black
throughout; a case study is white throughout, with full-bleed gallery bands supplying their
own colour.

**Two faces.** `Inter` carries everything read as language, from the wordmark down to body
text. `IBM Plex Mono` carries everything read as a label, a number or a category, always
uppercased, letter-spaced and small: the eyebrow, the year range, the discipline list, the
button labels, the menu control and the language chip. The rendered sizes at full width, which
all scale together to nine tenths below the laptop breakpoint:

| Role | Face | Size | Weight | Line height |
|---|---|---|---|---|
| Masthead, full width | Inter | `100px` | 500 | `100px` |
| Masthead, scaled | Inter | `90px` | 500 | `90px` |
| Closing line and manifesto lines | Inter | `52px` | 500 | `52px` |
| Home band headlines | Inter | `40px` | 500 | `40px` |
| Card tagline | Inter | `30px` | 700 | `33px` |
| Body at the scaled width | Inter | `22.5px` | 500 | `27px` |
| Brief and concept body | Inter | `20px` | 500 | `24px` |
| Byline and footer credits | Inter | `18px` | 400 | `18px` |
| Service list | Inter | `18px` | 500 | `21.6px` |
| Byline, scaled | Inter | `16.2px` | 400 | `16.2px` |
| Monospace heading | IBM Plex Mono | `16px` | 700 | `16px` |
| Monospace heading, scaled | IBM Plex Mono | `14.4px` | 700 | `14.4px` |
| Default body | Inter | `14px` | 500 | `15.4px` |
| Eyebrow | IBM Plex Mono | `12px` | 700 | `12px` |
| Smallest meta | Inter | `12px` | 500 | `13.2px` |
| Eyebrow, scaled | IBM Plex Mono | `10.8px` | 700 | `10.8px` |

Copy uses typographic apostrophes, three-period ellipses, and section labels in parentheses
with a space inside each parenthesis. Every string in this brief is written with a straight
apostrophe and renders with the typographic one.

**Motion is position, not time.** Almost every movement on the site is written directly from
the scroll position or the pointer position, frame by frame, rather than played. Every
scroll-driven value is reversible, so scrolling up plays it backwards exactly; positional, so
stopping leaves it stopped; unentered, with no start event; and uneased, a straight line from
position to value. The scroll itself is smoothed, so a wheel notch becomes a short glide. Two
tempos exist and no third: quick interface feedback, a fade or a border change in well under
half a second, and slow ambient drift of one to eight seconds a cycle. Text rises line by line
from behind its own edge, each line travelling its own height; only mastheads rise letter by
letter. Every image uncovers diagonally from a bottom corner that alternates between columns, so
a column of cards unzips. Images drift a few pixels inside their frames against the page.
Entrances decelerate, the wordmark collapse decelerates hard, the menu opens decelerating and
closes accelerating away, and the route cover eases in and out. There is no scroll progress
indicator, no hover growth on cards, no parallax on body copy and no letter animation on body
text.

**Chrome inverts rather than recolours.** The header mark, the corner arrows and the assembling
word are composited against whatever passes under them, so white over white turns black, white
over black stays white, and over a film they become its negative. That is intended.

**Pointer feedback lives in its own layer.** Almost nothing under the pointer changes. Instead,
letters follow the pointer on the home route and the not-found route, and a short label grows
from nothing at the pointer over a work card. The one hover change on an element is an outlined
pill's border going from partial to full strength. On a device that cannot hover, the followers
and the label are not rendered, and outlined pill borders sit at full strength permanently.

**Accessibility.** Body text and its ground meet the WCAG AA contrast bar of 4.5:1 on every
surface, including the eyebrow on the dark ground. With reduced motion requested, every reveal
is at its end state, every wipe fully revealed, image drift held at rest, the word assembled,
the showreel full bleed at full size with no room, the followers, drifting objects and flicker
not rendered, the films not autoplaying but showing a still frame with a play control, the
route cover a cut, and the scroll smoothing off. Keyboard navigation reaches every link and
control in document order: a skip link to the main content comes first on every route, the menu
overlay traps focus, closes on escape and returns focus to the MENU control, focus shows a
visible outline in the ground's opposite colour on both grounds, and nothing at zero scale is
focusable. The followers, the work label and the not-found letters are hidden from assistive
technology. Each film carries a caption track and a short text description, shown in its band
when the film is not playing.

**Responsive.** One design at every viewport, turned down to nine tenths below the laptop
breakpoint rather than redrawn. Below that breakpoint the staggered columns become one column,
so the works index and the home route get taller at a tablet width than at a laptop width, and
shorter again at a phone width. Below the tablet breakpoint the word `MENU` is dropped and the
four-dot mark stands alone at its own size, and the case study meta row stacks under the
masthead. Below the phone breakpoint gallery bands go full bleed single, the footer stacks, the
manifesto's outer text blocks and the smallest drifting objects are dropped. Nothing overflows
sideways at a narrow viewport. On a very wide window the gutter grows with the window and the
type stops growing at the laptop size.
## Front-end specification

### The palette that renders

The renderable palette is small, and a build that reaches for a platform's default link, form
or error colours will produce a site this one is not. Every colour below has a role; nothing
else is put on a public page.

| Token | Colour | Role |
|---|---|---|
| `white` | a near-white neutral | the light ground, and every mark on the dark ground |
| `black` | a near-black neutral | the dark ground, and every mark on the light ground |
| `grey-mid` | a light neutral | the eyebrow above every card tagline, and secondary meta; lifted to `grey-soft` on the dark ground |
| `grey-line` | a near-white neutral | hairline rules and disabled marks |
| `grey-soft` | a near-white neutral | the second hairline weight, and the eyebrow on the dark ground |
| `grey-deep` | a light neutral | the third grey, used once per template at most |
| `ink-soft` | a deep neutral | near-black type on a near-white band |
| `ink-mid` | a deep neutral | the second near-black |
| `paper` | a near-white neutral | the off-white the light bands actually sit on |
| `neutral-300` | a near-white neutral | the one faintly warm neutral, carried as a named token |
| `transparent` | fully transparent | the transparent end of every gradient |
| `status-saved` | a mid, vivid green | the studio console's saved state only; never on a public page |
| `builder-grey` | a light neutral | carried for completeness, placed on no page |

Four partial strengths carry the secondary-text system, because it is built from white or
black turned down rather than from a grey: white at forty per cent for the resting border of an
outlined pill and secondary type on the dark ground; black at forty per cent for the same on the
light ground; the second deep neutral at forty per cent for third-level meta on the light ground;
and black at ten per cent as the only shadow-weight tint in the system.

| Route | Opening ground | Closing ground | Switches |
|---|---|---|---|
| home | white | black | one, at the end of the hero |
| works index | black | black | none |
| case study | white | white | none in the chrome; gallery bands supply their own colour |
| not found | black | black | none |

The switch on the home route is not a fade: it is the boundary of a full-bleed band, and the
chrome that crosses it inverts itself.

### Type and layout

Two families and one fallback. `Inter` in weights 400, 500 and 700 for the display and body;
`IBM Plex Mono` in 400 and 700 for meta and labels; then a system grotesque, the platform sans
and `sans-serif`, stated once as a custom property. Load three display weights, not seven, and
subset both families to the character set of the copy deck plus digits and the mastheads'
punctuation. Serve with a swap behaviour so first render is never blocked.

Every size is set against a root that carries the scale factor, never as a fixed pixel value at
the call site. The type table in `## UI/UX notes` gives the rendered result.

The page runs edge to edge with a very narrow gutter, about a finger's width on a laptop. The
layout is a twelve-column grid in name only; what governs the page is a two-column asymmetric
split used three ways, plus full bleed:

| Split | Where | Behaviour |
|---|---|---|
| label left, prose right | the manifesto bands, the studio band, the concept | the label column is about a fifth of the measure and holds a parenthesised phrase |
| prose left, media right | the step-aside band | the media column runs full bleed to the right edge |
| staggered halves | the works index and the home rail | two columns of cards, the right column starting about half a card lower, the offset made by the column's own top padding and scroll transform, not by absolute positioning |
| full bleed | films, gallery bands, the mastheads | edge to edge, ignoring the gutter |

Nine stacking layers are used, assigned by name and never by number at the call site: overlay
(the menu overlay and the loading cover), chrome (the header mark and menu control), float (the
sound toggle and language chip), lift (a card raised while it is entered), content (the default),
mid (media inside a card), low (a caption over media), base (band backgrounds) and ground.

Radii: the pill's ends are true semicircles at every width, which means its corner radius is
larger than half its height and scales with the root; every image and media frame and the
language chip carries a small, barely-rounded corner that scales with the root; the service list
bullet and the sound toggle's indicator are circles. Borders: one weight, one colour per ground,
and one transition on the border colour, resting at partial strength and reaching full strength
under the pointer.

The scale rule: there is one stylesheet and one scale factor, nine tenths. Below the laptop
breakpoint the root drops by a tenth and everything expressed against it shrinks together: the
masthead from `100px` to `90px`, the byline from `18px` to `16.2px`, the monospace heading from
`16px` to `14.4px`, the eyebrow from `12px` to `10.8px`, the pill and image corners, and the
letter reveal's travel. Four media conditions exist: the laptop breakpoint governs the scale
factor and the switch from staggered halves to one column; the tablet breakpoint drops the word
`MENU` and reflows the mastheads; the phone breakpoint takes gallery bands full bleed single and
stacks the footer; and a hover-capable minimum width governs every pointer behaviour.

### Iconography and the wordmark

Five pieces of drawn artwork and no icon font. Every one is inline vector geometry.

| Name | Box | Primitives | Where |
|---|---|---|---|
| menu mark | `0 0 6 6` | 4 squares | the menu control, top right of every route |
| arrow, corner | `-8 -1 26 14` | 2 polylines | `All Works` and the scroll cue |
| arrow, inline | `0 0 14 10` | 1 path, 1 line | inside the `book a call` and `Homepage` pills |
| loading initial | `0 0 99 120` | 1 path | the loading state |
| loading apostrophe | `0 0 41 50` | 1 path | the loading state |

The menu mark is four 2-by-2 squares in a 6-by-6 box with a 2-unit gutter, filled with the
current colour so it inverts with the chrome. It is not a hamburger: it reads as two colons,
which is why the control is the word `MENU` followed by the mark. The corner arrow is two
polylines stroked in the current colour at 1.5 units with no fill, so shaft and head can be drawn
independently. The inline arrow's head is the chevron
`M8.60254 0.353516 L13.1188 4.86981 L8.60254 9.3861` with its apex on the vertical centre of a
14-by-10 box, and its shaft is a line from the left edge to the apex, stroked white on the dark
ground and black on the light one.

**The wordmark is a mechanism, not an image.** It is seven glyph paths, six letters and a closing
apostrophe, spelling `Naught'` in a `0 0 1408 294` box, drawn from `Inter` converted to outlines
at build time, and used three ways: all seven glyphs full width in the home hero, all seven full
width at the foot of the home route cropped by the page edge, and two glyphs, the `N` and the
apostrophe, as the header mark on every route in a `0 0 338 291` box.

The header mark is the same seven paths in a narrower window. Each of the five middle glyphs sits
in a group clipped by one rectangle spanning the full glyph height, cut to that glyph's width. To
collapse the mark, each of those five glyphs is translated straight down by more than the box
height, so it disappears behind the bottom edge of its own clip, and the apostrophe is translated
left to close the gap. Expanding reverses both. The collapse plays once on each route entry, on
the first scroll of the home route, and plays backwards when a visitor returns to the top of the
home route. Both the glyph paths and the apostrophe hint that their transform will change.

In the home hero the apostrophe arrives separately: the six letters resolve, then the apostrophe
grows from nothing to full size about its own position.

The loading glyphs are separate drawings, not taken from the wordmark: an initial in a
`0 0 99 120` box and an apostrophe in a `0 0 41 50` box, the same letterforms cut heavier for use
small and alone.

**The letter cursors** are six single letters drawn as polygons with no curves, the display
family's letterforms flattened to their skeleton.

| Name | Box | Home route position |
|---|---|---|
| `n-cursor`, large | `0 0 62 69` | lower third, left of centre |
| `n-cursor`, small | `0 0 62 69` | lower third, right of centre |
| `t-cursor` | `0 0 31 33` | lower third, upper left |
| `h-cursor` | `0 0 17 18` | lower third, lower left |
| `i-cursor` | `0 0 13 22` | lower third, bottom centre |
| `apos-cursor` | `0 0 24 25` | lower third, right |

Two are exact. `t-cursor`:
`M11.5142 28.4178 L6.17276 25.0772 L16.7141 8.22217 L10.5419 4.36195 L13.27 -0.000193374 L30.9263 11.0423 L28.1982 15.4044 L22.0555 11.5628 L11.5142 28.4178 Z`.
`i-cursor`: `M5.03568 21.9525 L9.34553e-05 20.0024 L7.74633 -8.77758e-05 L12.7819 1.95001 L5.03568 21.9525 Z`.
Draw the other four the same way, from the same family, at their boxes.

### Global chrome

Four things are present on every route: the header mark, the menu control, the language chip
and the standing byline. Three more are present on every route except not found: the sound
toggle, the closing call to action and the footer. There is no persistent navigation bar, no
breadcrumb, no progress indicator and no cookie banner.

**The header.** Two fixed elements at the chrome layer: the collapsed wordmark at the top left,
wrapped in a link to `/`, and the menu control at the top right, the word `MENU` in the monospace
face uppercased, then the four-dot mark. The mark's link is absent during loading, fades in as
the route enters, and flickers while it arrives. Below the tablet breakpoint the word `MENU` is
dropped and the mark keeps its own box without growing.

**The difference composite.** The corner arrow wrapper, the band that sits under the header
while the ground changes, and the assembling word wrapper are composited with a difference blend.
Difference is correct and a colour swap is not: a swap needs a scroll threshold per band and
breaks the moment a band moves or a film's brightness changes, while difference needs to know
nothing. The mark must be pure white in its own right, because difference against anything else
produces a tint. Over imagery it reads as inverted, and that is intended.

**The menu overlay.** Opened and closed by the menu control, covering the route entirely at the
overlay layer.

| Row | Content | Face |
|---|---|---|
| 1 | `works`, or `home` on every route except `/` | display, large |
| 2 | `STUDIO`, a scroll target on `/` rather than a route | display, large |
| 3 | `contact`, which opens the booking panel | display, large |
| 4 | the two call-to-action pills | monospace |
| 5 | the standing byline | display, small |
| 6 | the social rail and the language chip | monospace |

All three large rows render uppercase whatever their source case; set the transform in the
stylesheet.

**The language chip.** `EN` in the monospace face in a small-cornered chip at the float layer, on
every route and in the overlay. It is a real control with a single option, because one language
is published, and it moves rather than disappears as the width narrows. It flickers while it
arrives, like the header.

**The standing byline and the social rail.** `Creative studio in Milan`, display face, `18px`,
in the overlay, the home hero and the footer. The social rail beside it carries three links, and
every link carries a short form shown at rest and a long form that swaps in on pointer entry:
`LKDN` and `Linkedin`, `insta` and `Instagram`, `BHNC` and `Behance`. A `/` text node separates
the links.

**The closing call to action.** Two outlined pills side by side: `book a call`, trailed by the
inline arrow, which opens the booking panel; and `drop us an email`, trailed by an `@` set as its
own element at the pill's optical right outside the label's letter-spacing, which is a mail link
to `studio@example.com`. Above them, on the home route, the works index and the case studies,
sits the closing line: `Let's start` and `from naught'` on two lines on the home route, and
`Let's start from naught'` on one centred line on a case study.

**The sound toggle.** A pill labelled `SOUND` with a circular indicator, at the float layer,
centred at the top of the window, present only while a film is on screen and fading in with the
film band. Its indicator fills when sound is on, and it is the only element whose fill signals a
state.

**The footer.** Three cells on one row: the left cell `©24 . 26 - Founded by Lena March`, the
centre cell `Site by Antoine Marlet & Julien Mercer`, the right cell `Visuals by Frederic Delorme`,
followed by a link to `/privacy` reading `Privacy`. The copyright range is stored, not computed.

### Motion language

One declared keyframe exists, a slow full rotation called `spin`, and it drives only the loading
state. Two transitions are declared: an opacity fade for every fade in the system, and a
border-colour change for the one hover effect. Do not declare a transition on `all`; a platform
default of that kind makes a hand-built site feel mushy where this one is crisp.

Two tempos and no third, which is what the duration census of the reference shows. Interface
feedback is quick. Ambient motion, the loading spin and the
drifting objects, runs on slow cycles of one, three, four and eight seconds. Anything in between
reads as foreign.

Easing is assigned by effect, in words: every entrance, a line rising or a card arriving,
decelerates smoothly; the wordmark collapse decelerates hard; the menu overlay opens decelerating
and closes accelerating away; a symmetric move such as the language chip or the sound indicator
eases in and out evenly; the corner arrow on hover decelerates gently; and the route cover eases
strongly in and out in both directions. Nothing scroll-driven takes an easing at all, because
easing a sampled value makes the element lag the finger.

**The flicker.** The header element and the hero's language wrapper flicker as they enter: on
each frame, their strength is set to a value drawn from a fixed set weighted so that it sits
above ninety-five per cent about three quarters of the time with occasional deep dips to about a
third, and the flicker stops once the element has entered, within a second. It is an affectation
that makes the site feel made rather than generated. Keep it brief.

**The loading state and the route cover.**

| Phase | What happens |
|---|---|
| loading | the loading initial and apostrophe, centred on the route's opening ground, turning with `spin`, until the route's content is ready |
| enter | the cover lifts, the masthead lines rise from below their own clip, the header mark fades in |
| leave | a cover in the ground colour of the route being left closes over it before the next route is revealed |

The cover is why there is never a white flash between the black works index and a white case
study.

Motion deliberately absent: no scroll position indicator, no hover growth on cards, no parallax
on body copy, and no letter animation on body text.
### Scroll system

The scroll system is the product.

**Smoothing.** The page never scrolls at the operating system's raw wheel granularity. It
interpolates the scroll position toward its target every frame, so a wheel notch produces a
short glide and every scroll-derived value is continuous rather than stepped.

**The scrub contract.** Every scroll-driven value is a pure function of scroll position, and so
it is reversible (scrolling up plays it backwards exactly, with no replay and no re-trigger),
positional (stopping mid-effect leaves it stopped indefinitely), unentered (there is no
threshold at which an effect begins) and uneased (the mapping is linear). An effect that fires
once when an element enters the window and cannot be rewound is a different thing, and this site
has none.

**Page length.** Case study length varies by nearly a factor of two with the number of gallery
bands, and the home route and the works index are taller at a tablet width than at a laptop
width. No choreography may assume a fixed page length; positions are recomputed per width.

**The two reveal units.** Everything textual reveals by rising from behind its own edge, in
exactly one of two units:

| Unit | Applied to | Travel |
|---|---|---|
| line | one rendered line of a paragraph, heading, tagline or the manifesto | one line height of that line |
| letter | one glyph of a masthead, punctuation included | one line height of the masthead plus a small overshoot |

Each unit needs a wrapper with hidden overflow and one child per unit; the wrapper is the mask and
the child is what moves. Text is split into rendered lines after layout, re-split on resize, and
never authored pre-split. Body text never uses the letter unit, and mastheads never use the line
unit.

**The corner wipe.** Every image arrives by uncovering itself, with the wipe on the image's
wrapper and never on the image. Three variants, all ending fully revealed: straight up; from the
bottom-left corner, top and right receding together; and from the bottom-right corner, top and
left receding together. On the staggered columns the left column uncovers from one corner and the
right from the other, so a scroll down the works index feels like a zip. The wipe is a proportion
of the wrapper, so it needs no remeasuring per width.

**The differential rate.** Every image in a card or gallery frame rests offset upward inside a
frame that hides overflow, sized about a fifth taller than the frame, and drifts a few pixels
against the page as the frame passes: a few pixels on a home rail card, a little more on a works
index card, more again on a gallery image, and in the opposite direction on a band's right-hand
media block. It is a drift, not a parallax; overdo it and the site becomes a cheaper site.

**The assembling word.** About a quarter of the way down the home route, the word `works`
assembles out of five separately transformed letters. Each letter starts at about a fifth of its
final size and at a wildly different horizontal offset along a track more than three window
widths wide, and all five converge and grow into one word as the band passes. The group scales up
while its letters scale up, so the perceived growth compounds to roughly twenty-five-fold. The
assembly sits inside the difference composite.

**The scale stage.** The most expensive moment on the site, and the one to build last. Across one
band on the home route, four things move together: a rendered room scales up and slides down out
of the window; the showreel, which begins as a small framed picture on the room's back wall,
scales up faster, overtakes the room, fills the window and keeps growing past full bleed; and an
interference overlay strengthens across the move. The film reaches full size at the moment the
`SOUND` toggle fades in. Beneath the film a second copy of it runs heavily blurred at about two
thirds strength as its reflection on the floor, a band carrying a gradient from black to
transparent removes the reflection's bottom edge, and a still of the same subject at high
strength sits behind the film while it is small, so the room never looks empty.

**The manifesto band.** A phrase is repeated across the manifesto film in blocks of four lines,
at least six blocks, each repetition rotated about twenty degrees off horizontal in either
direction, never above about a third of full strength, drifting vertically as the band passes,
and placed at the edges of the frame, never over the centre. Blocks are transformed as blocks,
not per character.

### The pointer layer

Almost nothing under the pointer changes. The pointer feedback lives in a layer of its own.

**The letter followers.** On the home route's object field and on the not-found route, single
letters follow the pointer. Each letter interpolates its own position toward the pointer at its
own rate per frame, so a fast sweep strings them out like a comet's tail and they settle at
different moments; five distinct rates, the heaviest arriving last and trailing furthest, nearly a
hand's width at full stretch, the lightest barely leaving home. Each letter tips and grows in
proportion to how far it trails: at its furthest, about eight degrees and about four per cent
larger. The followers on the home route also drift with the page, and both inputs sum into one
transform.

**The work cursor.** Over a work card, the label `VIEW` in the monospace face grows from nothing,
centred on the pointer, and shrinks back to nothing when the pointer leaves. At rest it is present
in the document at zero scale, which is why nothing inside it may be focusable.

**The one hover on an element.** An outlined pill's border goes from partial to full strength
over a quick fade: white at forty per cent to white on the dark ground, black at forty per cent to
black on the light ground. The `Homepage` pill on the not-found route is the measured instance.

**Touch.** Where a pointer cannot hover, the followers and the work cursor are not rendered at
all, and outlined pill borders sit at full strength permanently, so the site is never faint.

### The media layer

**The film contract.** Every film autoplays without a gesture on every route it appears on; plays
muted until the `SOUND` toggle says otherwise and starts muted again on every route change; loops
with no visible seam; carries no native controls, no poster frame flash and no play button; holds
its own frame during the scale stage without reflowing anything around it; and decodes without
stalling the scroll smoothing. Each film is offered in at least two encodings, the more efficient
first, fetched only when its band is within two window heights, at a resolution chosen from the
window width, never blocking first render, with a poster generated from its first frame. When real films are supplied they are served
range-request capable, long-cached and immutable by name.

**The audio layer.** Two optional sounds, both off until the toggle is used: the film's own
audio, and an interface tick when the pointer enters the toggle's indicator. Muting is instant;
unmuting fades in quickly.

**The drifting object field.** At least ten still objects float across the lower third of the
home route: a foil star, a chrome heart, a wrapped sweet, a crumpled pink ball, a balloon, a paper
form, a chewing gum, a smiley, a cube and a buoy. Each rests at its own angle, and drifts and grows
as it travels, vertical-dominant, at roughly one per cent of scale per twenty pixels of travel.
Two of them, the balloon and a sausage, are pinned to the page instead, moving on one axis at a
differential rate like the card images. Scattered among the objects, at the same small scale and
their own angles, are the six letter cursors, which spell the studio name in pieces and follow the
pointer when it comes near.

**The interference overlay.** One fine-grained noise layer tiled over the showreel band,
strengthening across the scale stage. It is the only texture composited over content.

### Route: home

Thirteen bands; the ground switches once, from white to black after the hero.

| Band | Ground | Content |
|---|---|---|
| 1, hero | white | two-line headline, the one filled pill, the full wordmark, byline, social rail, language chip |
| 2, first headline pair | black | `Most brands produce content.` / `We prefer ideas.` |
| 3, the step aside | black | label and four prose lines beside a full-bleed media panel |
| 4, the assembling word | black | `works` assembling across about two windows of scroll |
| 5, second headline pair | black | `Good brands communicate.` / `Great brands surprise.` |
| 6, featured rail | black | the featured cards, then `View all ( 07 )`, the copyright, `Sound` |
| 7, showreel stage | black | the scale stage; no copy at all |
| 8, the studio | black | label, three prose lines, a two-line phrase apart from them, a media panel |
| 9, forms follow perspective | black | the largest type after the wordmark, then the service row |
| 10, the people | black | the heading and two groups of names |
| 11, the object field | black | the drifting objects and scattered letters, overlapping bands 9 to 12 |
| 12, the manifesto film | black | the film with the repeated phrase at its edges |
| 13, the closing panel | black | the closing line, both pills, three social lines, the cropped wordmark, the footer |

**Band 1.** The only white band, one window tall. Headline, `Inter` `40px` set solid:
`Not a style, a perspective.` / `Because Naught' is Everythin'.` Under it the one filled pill on
the site, black with a white label, `book a call`. The wordmark fills the width with all seven
glyphs. Bottom left, the byline; bottom right, the monospace social rail at `12px` and the
language chip. No navigation, no scroll cue, no subtitle, no client logos.

**Bands 2 and 5** are one component with two content slots: a pair of display lines at `40px`,
left in the gutter, on the vertical centre of a full window, each line revealed by the line unit.
The rhetorical shape is a concession, then a claim.

**Band 3.** Label `( The step aside )`, then:
`In a world of infinite images, the rare thing is` / `clarity. Images defend ideas, experiences` /
`shift perception, and brands change how` / `people see the world.` Beside it a full-bleed media
panel about half a window tall, running to the right edge. Small objects pass through band 4 at
low scale during the assembly and are gone by the time it completes.

**Band 6.** The featured cards, on the staggered split; the gap between the columns opens as the
band passes. Each card is an eyebrow (the case study title, monospace `12px` weight 700,
uppercased), a tagline (`Inter` `30px` weight 700 over `33px`, one sentence ending in a full
stop), and the cover (corner wipe, differential rate). Below the cards: `View all`, then `(`,
the published count as two digits, `)` as three elements, fading in after the last card; the
copyright `©24 . 26`; and `Sound`.

**Band 7.** The scale stage in full, about a window and a half of scroll. The showreel is at full
frame and playing before the band reaches the window, because the first frame of a showreel is
its worst. No caption, title or credit.

**Band 8.** Label `( The Studio )`, then:
`We called it Naught' because it started as a paradox,` /
`an empty space open enough to become anything:` / `a campaign, a space, an event, a system...`,
then, as a separate smaller block at body size with its own late reveal: `or something` /
`unexpected.` Below, a media panel shaped like band 3's.

**Band 9.** `Forms follow` / `perspective.` at a size that fills the window width. Under it a
three-column row at `18px`: `We design :` on the left; the five services one per line, each after
a circular bullet that pops in from nothing as its line reveals, in the centre; and
`Perspective is where strategy` / `meets visual culture.` on the right, rendered once and repeated
by a marquee rather than authored twice.

**Band 10.** `Naught' without people :`, then `founders & management` with `Lena March`,
`Marie-Line Vo`, `Gabriel March`, `Frederic Valmont`, then `creative partners` with
`Antoine Marlet`, `Julien Mercer`, `Frederic Delorme`. Body size, one name per line, group labels
lowercase, no roles, photographs or links.

**Band 12.** The manifesto film, full bleed, with the repeated phrase `we are naught'` at its
edges decaying as it repeats. Each block is four lines: one or two lines clean; the others with
one to three characters swapped for a lookalike (an uppercase lookalike, a digit, a subscript form
or a punctuation mark), clustering at the start of each word and at the closing apostrophe; and the
fourth line fully substituted, the last rung of the corruption ladder, as noise that keeps the phrase's word spacing and punctuation
positions. For example, a block reads `we are naught'` / `wM are naE!ht'` / `we are naught'` / a
noise line. At the centre of the frame one line at full strength reads `We create from nothing.`

**Band 13.** The closing line `Let's start` / `from naught'` at `52px` in the upper third, the two
outlined pills under it, `Linkedin`, `Instagram` and `Behance` one per line in the display face at
`20px` on the right, then the full wordmark in white cropped by the bottom edge of the document,
then the footer row fading in after it.

### Route: works index

Black throughout and the shortest route. The masthead is one row: `Works` on the left and
`©24 . 26` on the right, both `Inter` `100px` set solid, both revealed by the letter unit one
glyph at a time including every digit, space and point. Setting the copyright at title size makes
it the second half of a two-word headline. Below it, one card per published case study, the same
card as the home rail, on the staggered split, with the gap opening across the document and the
whole card as the link target. Then the closing line, the pills, the three social lines and the
footer. At a tablet width the columns become one with images at the full measure, so the route is
at its tallest; at a phone width it shortens again.

### Route: case study

White throughout.

| Part | Content |
|---|---|
| masthead | the title on the left, one glyph per child, and `W'` with the two-digit ordinal on the right, both at the masthead size, letter-revealed |
| meta row | bottom left of the first window: the year range, then the disciplines joined by a space, a solidus and a space; stacks under the masthead below the tablet breakpoint |
| brief | right column, `20px` over `24px`, each rendered line revealed: what the client is, what they had that was unusual, and a short last sentence naming the problem |
| concept | label `( Concept )`, then prose opening with the word `So` and closing on a short declarative line |
| gallery bands | in stored order, each one of four layouts: full bleed; a coloured band with one to three images inset; a split of two images with the gutter between; a gradient band with images inset. Band colours belong to the case study, not the palette |
| all works | `All Works` at `52px` with the corner arrow turning right then up, and the credits beside it |
| credits | `Crédits :` then one to three names joined by a space, a solidus and a space, each with its role before it only when a role is stored, and a link where a collaborator has a site |
| closing panel | the closing line on one centred line, both outlined pills centred; the only centred block on the site |
| next subject | the next published case study's masthead at full size, letter-revealed, the whole row a link |
| compact list | every other published case study, one row each, title and ordinal digit, the current one omitted |

### Route: not found

Black, one window, nothing below it. The letters `E`, `R`, `R`, `O`, `R`, `4`, `0`, `4` are drawn
through the letter cursor drawings, scattered across the window at their own angles and sizes,
and they follow the pointer with the follower rates, so the debris only reads as `ERROR 404` once
the pointer moves. Five drifting objects sit among them at fixed angles, drifting slowly and not
following the pointer: the foil star, a chrome asterisk-shaped balloon, the chrome heart, the
crumpled pink ball and the wrapped sweet. One outlined pill, `Homepage` with the inline arrow, sits
centred at the foot of the window, with an accessible name saying it goes to the home page. The
chrome and the overlay are intact. At a narrow viewport the letters tighten toward the centre.

### The booking panel and the console surfaces

The booking panel slides over the route from the right edge at the overlay layer, on the route's
own ground, with a close control and escape to close. Its fields are single hairline-underlined
rows in `Inter` `20px`, labels in the monospace eyebrow style, the service chosen from five
outlined pills, and the submit control an outlined pill reading `Send`. Focus moves into the panel
when it opens, stays inside it, and returns to the control that opened it.

`/sign-in`, `/sign-up`, `/account` and the studio console are plain and legible on the white
ground with near-black ink, in the same two faces and the same pill: the console's cards are the
works index card with a state label and a featured switch added, and its enquiry rows are
hairline-separated.

### Component architecture

Four layers that may not be collapsed into each other: the document (markup, type, grounds,
bands); the scroll layer (one interpolated scroll position and one frame loop); the pointer layer
(one interpolated pointer position, the followers and the work cursor, reading nothing from the
scroll layer); and the route layer (the cover, the loading state, the wordmark collapse). The
followers take input from both the pointer and scroll layers and sum the two, so a stationary
pointer during a scroll must still move them correctly.

The scroll controller is one instance with one frame loop for the whole document. Every effect
registers a start position, an end position and a pure mapping from progress to value, and holds
no state between frames. Each frame does all reads, then all writes. An effect whose element is
more than one window outside the window is not evaluated. Every scroll-driven property is a
transform, a filter or a strength, never layout.

One pill in three variants (filled, outlined on dark, outlined on light), one card, one masthead
with a slot per cell, one band primitive with five arrangements (label left prose right; prose
left media right; staggered pair; full bleed; centred), one line reveal and one letter reveal.
The route controller closes the cover in the ground colour of the route being left, plays the
wordmark collapse once per route entry and reverses it at the top of the home route, and resets
the scroll position and the interpolated position to zero on entry without easing to it. Name
things by role: `mark`, `menu-control`, `pill`, `pill-label`, `pill-mark`, `line`, `glyph`,
`card-media`, `word-letter`, `follower`, `cursor-label`, `sound`, `sound-state`, `lang`,
`drifter`, `reflection`, `interference`.

### Responsive reflows

| Route | Below the laptop breakpoint | Below the tablet breakpoint | Below the phone breakpoint |
|---|---|---|---|
| home | the featured rail goes one column and the route gets taller | the word `MENU` drops, leaving the mark | the object field thins, the manifesto blocks reduce to two |
| works index | the staggered columns become one and the route nearly doubles | as above | images narrow and the route shortens |
| case study | gallery splits become single | the meta row stacks under the masthead | gallery bands go full bleed single |
| not found | the letter field tightens toward the centre | as above | the pointer layer is not rendered |

Nothing about a route's structure is dropped at any width; there is one page that narrows.

### Accessibility, in full

The site is hostile by construction in four ways, and none has to stay a problem: every effect is
scroll-driven, the pointer layer is the hover language, the difference composite makes contrast
guaranteed but colour unpredictable, and two films autoplay. `## UI/UX notes` gives the reduced
motion behaviour, the keyboard requirements and the contrast bar. The eyebrow on the dark ground
is the one real contrast failure in the reference and is lifted. A resting pill border at partial
strength is decoration only, because the label inside it is at full contrast. The followers, the
work cursor and the not-found letters are hidden from assistive technology, the not-found route
carries a real visually hidden `ERROR 404` heading, and every image carries its stored
description.

### Performance

Films are the site's weight, about eighty-five per cent of everything the reference transferred.
The home route transfers under `3MB` before the showreel is fetched; first contentful paint is
under `1.2s`, largest contentful paint under `2.5s`, interaction to next paint under `200ms`, and
the frame budget holds at `16ms` through the scale stage. The heavy reflection blur is rendered
once to an offscreen surface and transformed, not recomputed each frame; the difference-composited
elements are kept tiny; and the interference overlay is generated once at low resolution and
tiled.

### Zero-asset construction: the substitution guide

The build runs with an empty asset directory.

**Grain and the interference overlay.** One recipe: a fractal-noise turbulence filter with four
octaves at a fine base frequency on a 300-unit tile, desaturated to grey, serialised as inline
vector data and tiled, with enough tonal variation that the tile does not read as a pattern; a coarser base frequency for the paper form.

**The drifting objects.** Each is a simple form lit in one of three finishes, keeping its object
name so its placement still addresses it: mirror chrome (the heart, the asterisk balloon, the
wrapped sweet), a radial lighting map with a bright upper hemisphere, a dark lower hemisphere, a
soft horizon and one small hard highlight placed off centre; coloured foil (the star, the balloon),
the same map multiplied by a single hue with the highlight left white; and matte crumple (the pink
ball, the paper form, the chewing gum), the same map at low contrast with the grain over it.
Compose them from primitives: a sphere, a swept profile, a capsule chain, a rounded box. The one
thing not to skimp is the single hard highlight on every object.

**The rendered room.** A flat scene with no geometry: a horizon at two thirds height, a floor as a
vertical gradient from a deep neutral to black with a soft specular streak down its centre, two
plinths as rounded rectangles, and the film's frame as a rectangle on the back wall. It is never
in focus.

**The films.** Stand-ins generated on a drawing surface at each film's framing: a slow greyscale
drift across the grain field at low contrast, looping every eight seconds. Deliberately dull, so
nobody ships it.

**Audio.** The tick is one square-wave oscillator at `1800Hz` gated by a very short attack and
decay at low gain. The ambient bed, only while stand-in films are in use, is two sine oscillators
at `55Hz` and `55.3Hz` beating slowly against each other through a low-pass filter at `400Hz`
whose cutoff is modulated by an oscillator at `0.08Hz`.

**Photography.** Every cover and gallery stand-in is generated from a seed of the case study slug
and the image position, so a slot always produces the same image: a two-stop linear gradient
between two greys from the palette at a seeded angle; the grain multiplied over it at low strength;
one soft elliptical highlight at a seeded position; and the case study's ordinal set small in a
corner in the monospace face. Coloured gallery bands stay on the route's own ground until real
colours are stored.

**Type.** The wordmark is drawn geometry made once from `Inter` outlines, so the display family's
licence does not affect it.

## Technical requirements

Server-rendered pages. Every route's HTML is produced on the server from templates, and the
browser receives finished markup on first paint; the interactive parts are enhanced in place.

| Layer | What to use |
|---|---|
| Server | Flask on Python 3.12, rendering Jinja templates, served by gunicorn |
| Interactive parts | Alpine.js for the menu overlay, the booking and console panels and the sound toggle |
| Scroll, pointer and route controllers | hand-written ES modules, no animation library |
| Datastore | PostgreSQL, reached with psycopg at `DATABASE_URL` |
| Object store | MinIO, reached with boto3 at `STORAGE_ENDPOINT`, bucket `STORAGE_BUCKET`, credentials `STORAGE_ACCESS_KEY` and `STORAGE_SECRET_KEY` |
| Generated images | Pillow |

Use only the libraries named here plus their direct dependencies. Do not introduce a second
database, cache, queue, object store, identity provider or mail vendor: the only backing
services available in this environment are PostgreSQL and MinIO, and reaching for anything else
is a contract violation.

**Identity.** Email and password, implemented by this application, with no external identity
provider. `POST /api/auth/sign-in` returns a bearer token and sets an HTTP-only, same-site session
cookie; every API route accepts either the `Authorization: Bearer` header or the cookie. A
password is stored only as a salted one-way hash and never returned by any response. Signing out
revokes the token and ends the session.

**Media.** Object keys follow `works/{work_id}/{sha256_of_bytes}.{ext}`. The bucket carries no
anonymous read policy. `GET /media/<storage key>` is the only path an image travels to a browser,
streaming from the store with the object's content type. Uploads accept `image/png`, `image/jpeg`
and `image/webp` up to `10MB`; anything else is refused as invalid.

**Status codes.** An unmatched path, a draft case study requested by anyone but an author, and a
draft image requested by anyone but an author all answer `404`. The not-found template is the
body of every public `404`.

**Seeding.** On start the application creates its schema, seeds the accounts, services, people,
settings, case studies and enquiries in `## Data model` if they are absent, and generates and
uploads each case study's stand-in images if the store holds none for it. Starting twice leaves
exactly one copy of every seeded row and object.

**Page views.** Every public page view is recorded with its route, stored as the path such as `/works`, and
the instant it was served.

**Social previews.** Every public route declares `og:title` and `og:image` in its head. A case
study's `og:image` is its cover's `/media/` address. Every other public route's is
`/og/<route name>.png`, an image the application generates and serves, where the route name is
`home`, `works` or `privacy`.

**Performance.** First contentful paint under `1.2s`, largest contentful paint under `2.5s`,
interaction to next paint under `200ms`, the frame budget at `16ms` through the scale stage, and
the home route under `3MB` before the showreel is fetched.

## Data model

**Entities.** Each entity is one table named exactly as the entity, and each field
named below is a column of the same name.

`account` carries `id`, `email`, `display_name`, a password hash, `role` (`author` or `reader`)
and `created_at`.

`work` carries `id`, `slug`, `title`, `ordinal`, `year_from`, `year_to`, `disciplines` (an
ordered list), `tagline`, `brief`, `concept`, `credits` (an ordered list of `role` and `name`),
`published`, `featured` and `updated_at`.

`media` carries `id`, `work_id`, `kind` (`cover` or `gallery`), `storage_key`, `content_type`,
`sha256`, `byte_size`, `description`, `layout` (`full-bleed`, `coloured-band`, `split` or
`gradient-band`, for a gallery image), `band_colour`, `caption` and `position`.

`service` carries `label` and `position`. `person` carries `name`, `group`
(`founders & management` or `creative partners`) and `position`. `settings` is one record:
`byline`, `contact_email`, `copyright_from`, `copyright_to` and `sound_default`.

`enquiry` carries `id`, `account_id` (empty for a visitor), `name`, `email`, `company`,
`service`, `preferred_date`, `time_window` (`morning` or `afternoon`), `message`, `status`
(`new`, `contacted` or `closed`) and `created_at`.

`page_view` carries `id`, `route` and `viewed_at`.

**Field rules.**

| Field | Rule |
|---|---|
| `work.slug` | unique, lowercase letters, digits and hyphens |
| `work.ordinal` | unique, `1` to `99`, stored |
| `work.title` | `1` to `24` characters |
| `work.year_from`, `work.year_to` | two-digit integers, `year_from` not after `year_to` |
| `work.disciplines` | each one of `Branding`, `Webdesign`, `Development`, `Digital`, `Packaging`, `Space design` |
| `work.tagline` | one sentence, at most `60` characters |
| `media.storage_key` | follows the key scheme and is unique |
| `media.description` | required, `1` to `200` characters |
| `enquiry.service` | one of the five service labels |
| `enquiry.message` | `1` to `1000` characters |
| `account.email` | unique, trimmed, lowercased |

**Relationships.** A work has one cover and zero or more gallery images, ordered. An enquiry
belongs to at most one account. Removing a media record removes its object from the store.

**Invariants.**

- A work that is not published, and every media record it owns, is readable only by an author.
- An ordinal is never reassigned when another work is unpublished.
- A media record's bytes exist only in the object store, under its storage key.
- A reader reads only the enquiries whose account is theirs.
- The featured rail shows published, featured works in ordinal order, at most five.

**Seed data.** Every seeded account uses the password `deku-demo-pw-2026`; the accounts are in
`## User roles`.

Settings: byline `Creative studio in Milan`, contact `studio@example.com`, copyright `24` to
`26`, sound off.

Services, in order: `Brand identities`, `Campaigns`, `Digital experiences`, `Events`,
`Visual systems`.

People, in order: `founders & management` `Lena March`, `Marie-Line Vo`, `Gabriel March`,
`Frederic Valmont`; `creative partners` `Antoine Marlet`, `Julien Mercer`, `Frederic Delorme`.

| Ordinal | Slug | Title | Years | Disciplines | Tagline | Published | Featured |
|---|---|---|---|---|---|---|---|
| `1` | `solace` | `Solace` | `25` to `26` | `Branding`, `Packaging`, `Space design` | `Where taste meets meaning.` | yes | yes |
| `2` | `urbana` | `Urbana` | `24` to `26` | `Branding`, `Webdesign`, `Development` | `A living instrument for reading territory.` | yes | yes |
| `3` | `un-charted` | `Un_Charted` | `25` to `26` | `Branding`, `Webdesign` | `Seize the unexpected: the invisible, made visible.` | yes | yes |
| `4` | `kwm` | `Kwm` | `25` to `26` | `Branding`, `Digital` | `Swiss clarity for French engineering.` | yes | yes |
| `5` | `tactify` | `Tactify` | `25` to `26` | `Branding`, `Webdesign`, `Development` | `Branding the forgotten sense.` | yes | yes |
| `6` | `kine` | `Kine` | `25` to `26` | `Branding`, `Digital` | `The movement, made conscious.` | yes | no |
| `7` | `chemie-union` | `Chemie Union` | `24` to `26` | `Branding`, `Packaging` | `From toxic to tomorrow: chemistry, reframed.` | yes | no |
| `8` | `veloce` | `Veloce` | `26` to `26` | `Branding` | `Speed, held still.` | no | no |

Credits: `Solace` credits `Kelly Vandroux`; `Urbana` credits `Amelie Ronsard` with the role
`Motion & development by`; `Kwm` credits `Kelly Vandroux` and `Auguste Rendell`; every other case
study credits `Auguste Rendell`.

`Solace`'s brief:
`A Swiss specialty coffee house and roaster: single-origin selections, organic, origin-guaranteed, with its own barista school. The founders are travelers and craftspeople first. The trap was obvious: specialty coffee has a house style now, clean but interchangeable, saying nothing of travel or craft.`
Its concept:
`So we built taste education into the brand itself, the Escoffier move. Each origin gets its own story, its own palate, its own reason to slow down, the way a chocolate bar earns a tasting note instead of a label. Warmth came back through texture and hand: materials you want to touch, type that feels drawn rather than set, imagery that smells of the place the bean came from. The result is a house, not a chain, somewhere the journey from plantation to cup is the whole point. Craft you can taste. Origins you can read.`

Every other case study carries a three-sentence brief in the same shape (what the client is,
what was unusual, the problem, last and short) and a concept opening with `So` and closing on a
short declarative line, written by the builder.

Each case study has one cover and four gallery stand-ins, the gallery in the layouts
`full-bleed`, `coloured-band`, `split`, `gradient-band`, each with a written description.

Enquiries: one from `reader@example.com` for `Campaigns`, status `new`; one from
`reader2@example.com` for `Events`, status `contacted`.

## Constraints

- No image, film, font or audio file ships in the source. Every image is generated; the films and
  the sounds are generated stand-ins.
- A cover or gallery image's bytes live only in the object store.
- No search, newsletter, comments, sharing, pricing, shop, second language or payment.
- No email is sent by the application; `drop us an email` is a mail link.
- Films never play sound before the `SOUND` toggle is used.
- Nothing scroll-driven touches layout, and nothing scroll-driven is eased.
- Two tempos of motion only.
- Two grounds only.
- The editor leftovers of the reference, a sentence about a text block inside a div, a bare
  `000`, and an empty-collection message, appear nowhere.
- Seeded accounts are refused by a production configuration rather than merely omitted.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173` -
  `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world uses. Read
  both from the environment; never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app root, empty.
- Serve a production build behind a static or preview server - never a dev server.
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
| `GET /api/works` | `featured=true` for featured works only | a top-level JSON array of works in ordinal order, each with `id`, `slug`, `title`, `ordinal`, `year_from`, `year_to`, `disciplines`, `tagline`, `featured`, `published`, `cover`: published works only, or every work including drafts for an author |
| `GET /api/works/<slug>` | none | the work with `brief`, `concept`, `credits`, `cover` and `gallery`, each image carrying `url`, `description`, `layout`, `band_colour`, `caption` |
| `GET /api/services` | none | a top-level JSON array of `label` in order |
| `GET /api/people` | none | a top-level JSON array of `name` and `group` in order |
| `GET /api/settings` | none | `byline`, `contact_email`, `copyright_from`, `copyright_to`, `sound_default` |
| `POST /api/auth/sign-up` | `display_name`, `email`, `password` | the account with `id`, `email`, `display_name`, `role`, and `token` |
| `POST /api/auth/sign-in` | `email`, `password` | the account and `token`, and sets the session cookie |
| `POST /api/auth/sign-out` | none | an empty body |
| `GET /api/auth/me` | none | the account |
| `POST /api/enquiries` | `name`, `email`, `company`, `service`, `preferred_date`, `time_window`, `message` | the enquiry with `id`, `status` and `created_at` |
| `GET /api/enquiries` | none | a top-level JSON array, newest first: a reader's own, or every enquiry for an author |
| `GET /api/enquiries/{id}` | none | the enquiry: a reader's own, or any for an author; anything else answers `404` |
| `PATCH /api/enquiries/{id}` | `status` | the enquiry |
| `POST /api/works` | `slug`, `title`, `ordinal`, `year_from`, `year_to`, `disciplines`, `tagline`, `brief`, `concept`, `credits` | the work, `published` false; a slug or ordinal already in use is refused with `409` |
| `PATCH /api/works/{id}` | any work field, `featured` | the work |
| `POST /api/works/{id}/publish` | none | the work, `published` true |
| `POST /api/works/{id}/unpublish` | none | the work, `published` false |
| `POST /api/works/{id}/media` | multipart: `file`, `kind`, `description`, `layout`, `band_colour`, `caption` | the media record with `id`, `storage_key`, `sha256`, `url` |
| `DELETE /api/works/{id}/media/{media_id}` | none | an empty body |
| `GET /media/<storage key>` | none | the object's bytes with its content type |
| `GET /api/page-views` | `route` | a top-level JSON array of `route` and `viewed_at` |

Field names are exact. A successful call returns the named resource or shape, and an invalid or
unauthorized call is rejected as a client error, never as a server error and never as a silent
success. Every error body carries `error`, a human-readable message, and `field`, the name of the
field at fault or null. Bearer or session authentication applies to everything except the health
route, the public reads of works, services, people and settings, `POST /api/enquiries`, sign-up,
sign-in and `/media/` for a published work's image.

### No mocks

The rows this product reports on have to exist in PostgreSQL, and every image has to exist in
MinIO. A case study list typed into a template rather than read from rows, image bytes written to
the application's disk or into a database column, a draft hidden only by leaving its card out of
the page while its route and its images still answer, an enquiry kept in memory, and a publish
flag held in a variable are each a contract violation however convincing the page looks.
PostgreSQL and MinIO are the facts: the site can only reflect what lives in them, never
substitute for them.

## Definition of done

A stranger scrolls the home route, watches the showreel grow out of its room, opens a featured
case study, books a call from its closing panel, and the enquiry exists. A reader who books while
signed in finds that enquiry at `/account`; another reader cannot. A studio author drafts a case
study, uploads a cover that lands in the store under its key, and publishes; until then the
draft's route, record and image answer as missing to everyone else, even by exact storage key.
