# Studio AVX

Build and deploy a working web application from this brief. There is no starting
codebase. When you are done, a stranger must be able to open the app in a browser,
watch twenty works float in a live three dimensional gallery and switch it between rings
and a spiral, narrow the Works catalogue to one discipline, open a project, and send an
enquiry from the contact page that the studio then finds in its inbox, without hitting an
error page.

A different stranger, not signed in as the studio, must NOT be able to read any stored
enquiry by any means: not through the app, not by asking the read surface for the list,
not by guessing an enquiry reference. An enquiry must be a real row in PostgreSQL and its
notification must be a real message delivered through the mail transport; a message the
app only logs does not count, and a confirmation the page shows without a stored row does
not count either.

## Overview

Studio AVX is a brand and digital design studio based in Catania, Sicily, working since
2017. This site is its public portfolio, and its one job is to make a prospective client
feel the studio's craft within the first few seconds, browse twenty selected works,
understand the disciplines on offer, and make contact.

The site has one signature surface and several supporting routes. The home is a full
viewport three dimensional gallery: twenty project cards float in an electric blue void
around a central chrome spine, scrolling moves the focus from one card to the next, and
the arrangement morphs between two named formations, `Rings` and `Spiral`. The same
twenty projects live on the Works route as a flat, filterable catalogue with a `Grid` and
a `List` view, which is also the accessible equivalent of the gallery and the fallback
where a device cannot draw it. A project detail page, a long editorial studio page, a
contact page with an enquiry form, a privacy and cookie policy, and a bespoke not-found
page complete the site. Everything speaks Italian and English.

The genuinely hard part is that the site is almost entirely presentation, and the one
action that touches state has to be as trustworthy as the presentation is striking. An
enquiry is validated, stored, and delivered to the studio as a mail message; a decoy
field and a rate limit keep it from being flooded; and the stored enquiries are readable
by the studio alone.

The non-goals are as firm as the goals. What this site deliberately is not: no content
editing interface, no project creation or editing through the product, no shop, no
newsletter, no blog, no ambient audio, and no tracking cookie before a visitor has made a
consent choice.

## User roles

| Role | Can do |
|---|---|
| visitor | Read every public route without an account: the gallery at `/it` and `/en`, the Works catalogue in both views with every facet, every project page, the studio page, the contact page and the privacy page. Send an enquiry. Make a consent choice. **Cannot read, list, or change any stored enquiry, and cannot reach `/inbox`.** |
| studio | Everything a visitor can do, and: sign in, read every stored enquiry in `/inbox`, and move an enquiry between the statuses `new`, `replied` and `archived`. **Cannot create, edit or delete a project, and cannot delete an enquiry.** |

Authorization is enforced **server-side on every mutating endpoint**. Hiding a
control in the UI is not authorization: a direct API call from a visitor with no
token to any studio-only endpoint must be rejected by the server (an unauthorized
request is denied, not served), leaving the protected state unchanged.

There is no public signup. Two studio accounts are seeded for grading, both with the
password `deku-demo-pw-2026`:

| Email | Name | Role |
|---|---|---|
| `studio@example.com` | Giulia Ferro | studio |
| `studio2@example.com` | Marco Lentini | studio |

Three enquiries are seeded: `ENQ-0001` from Anna Rizzo at the status `new`, `ENQ-0002`
from Luca Bianchi at the status `replied`, and `ENQ-0003` from Sofia Greco at the status
`archived`.

## Core features

### Auth

Accounts are email and password, implemented by the app. `POST /api/auth/login` takes
`email` and `password` and returns a bearer `token` plus the signed-in `user`. Every later
call carries `Authorization: Bearer <token>`. A token expires 24 hours after it is issued.
`POST /api/auth/logout` retires the token.

1. A wrong password and an unknown email are refused with the same message,
   `Sign in failed`, so neither answer reveals whether the account exists. A missing
   token, an unknown token, a retired token and a token past its expiry are all refused
   as unauthenticated, and nothing they asked to change is changed.
2. Passwords are stored hashed. The literal `deku-demo-pw-2026` must work at login for
   both seeded accounts and must not appear in any stored record.
3. `/login` is the sign-in page. A visitor who opens `/inbox` without a session is sent to
   `/login` and arrives at `/inbox` after signing in.

### 1. The spatial gallery

`/it` and `/en` are the home, the same gallery in the two languages.

1. The home renders a live three dimensional scene filling the viewport over the brand
   blue. Twenty project cards are placed as flat textured planes in depth around a
   central chrome spine built from stacked rounded bead forms with a reflective finish.
2. Two formations, `Rings` and `Spiral`, are switched by a frosted segmented control at
   the top centre on a wide screen and at the bottom left on a narrow one. `Rings` is the
   default. Switching morphs the cards from one arrangement to the other rather than
   cutting between them. The chosen formation is remembered for the next visit.
3. The page itself does not scroll. The wheel, a trackpad and a touch drag instead move a
   focus index through the twenty cards, one at a time, in catalogue order. The focused
   card grows, turns to face the viewer and centres.
4. The focused card shows a frosted label pill carrying the project title, its first
   discipline label and a north east arrow. A second pill reading `SCROLL` shows until the
   visitor first scrolls.
5. Choosing the focused card or its arrow opens that project's page through the page
   transition.
6. A visually hidden `h1` carries the real page heading, `AVX - Brand & Digital Design
   Studio`, so the home has a true heading for assistive technology.
7. The home footer is one line in three parts: `BRAND & DIGITAL DESIGN STUDIO` at the
   left, the count of featured works over the total followed by `selected Works` in the
   centre with `Works` linking to `/works`, and `© 2026` at the right. The two numerals
   are counted from the projects, never typed; with the seed they read `12 / 20`.
8. **Where the browser cannot draw a three dimensional scene, the home shows the flat
   Works catalogue instead of a broken canvas**, with every one of the twenty projects
   reachable.
9. Under reduced motion the focus moves without travel, the formation switch changes the
   arrangement without morphing, and the ambient scene motion stops.

### 2. The works catalogue

`/works` is the same twenty projects as a flat catalogue. `/works/` answers with a
permanent redirect to `/works`.

1. Two views are switched by a frosted segmented control, `Grid` and `List`. `Grid` is the
   default and shows each project's cover, slightly rotated and perspective skewed over a
   faint darker blue perspective floor. `List` shows a typographic index: title,
   disciplines, year and client, one row per project.
2. Six facets sit in a frosted filter pill at the bottom centre, in this order, each with
   its count in brackets: `All`, `Branding`, `Editorial`, `Type Design`, `Web Design`,
   `Packaging` in English, and `Tutti`, `Branding`, `Editoria`, `Type Design`,
   `Web Design`, `Packaging` in Italian. The filter pill has a close control labelled
   `×`.
3. **Every count is computed from the projects' disciplines when it is read, never
   stored.** With the seed the counts read `All (20)`, `Branding (11)`, `Editorial (5)`,
   `Type Design (3)`, `Web Design (3)`, `Packaging (2)`. A project may carry more than one
   discipline, so the five discipline counts sum past twenty, and `All` is the true total.
4. Choosing a facet narrows the grid or the list in place to the projects carrying that
   discipline, keeping catalogue order, with the rising staggered reveal. The chosen view
   and facet are remembered while the visitor stays on the site.
5. Every card and every row links to its project page.

### 3. Project detail

`/works/<slug>` is one project.

1. The page shows the large cover, the title, the discipline labels, the year, the client,
   a summary in the current language, and a gallery of images.
2. The page offers the previous and the next project in catalogue order, wrapping from the
   last to the first and from the first to the last, and a link back to `/works`.
3. An unknown slug answers as not found and shows the not-found page.
4. The title and the metadata arrive with the split word reveal.

### 4. The studio page

`/studio` is a long editorial page about the studio. `/studio/` answers with a permanent
redirect to `/studio`. Unlike the home and Works, this page scrolls normally.

The page's structure runs hero, intro, services, sculpture and images.

1. The hero carries a visually hidden `h1`, `Studio AVX - grafica, branding e
   comunicazione a Catania`, the visible word `STUDIO` revealed glyph by glyph, three
   eyebrow lines `BASED IN CATANIA / SICILY`, `SINCE 2017` and
   `BRANDING / DIGITAL / TYPE / PACKAGING`, and the statement
   `WE DON'T JUST DESIGN WE DEFINE ATTITUDES`, which reveals as the page scrolls.
2. An intro paragraph in the current language introduces the studio as active since 2017
   and working from Sicily nationally and internationally.
3. A two column list of services follows, the discipline label at the left and a paragraph
   at the right, separated by hairlines. Six services are seeded, in this order, with these
   Italian labels: `DESIGN EDITORIALE`, `TYPE DESIGN`, `SOCIAL MEDIA DESIGN`,
   `COPYWRITING E NAMING`, `BRANDING`, `WEB DESIGN`. The English labels are
   `EDITORIAL DESIGN`, `TYPE DESIGN`, `SOCIAL MEDIA DESIGN`, `COPYWRITING AND NAMING`,
   `BRANDING`, `WEB DESIGN`.
4. A large reflective sculpture built from stacked rounded forms turns slowly down the
   centre column as the page scrolls.
5. Editorial images wipe open from the bottom as they enter and drift at a slightly
   different speed from the text.

### 5. Contact and enquiry

`/contact` is the enquiry page and the one place a visitor writes anything.

1. The page shows the public address `hello@avx-studio.example.com` as a link that opens a
   new mail message to it.
2. The form collects a name, an email address and a message. The labels read `Name`,
   `Email` and `Message` in English and `Nome`, `Email` and `Messaggio` in Italian, and the
   submit action reads `Send enquiry` or `Invia richiesta`. Every field has a real label
   element.
3. **Validation happens in the browser and again on the server, with the same rules.** The
   name is 2 to 120 characters after trimming, the email is a well formed address, and the
   message is 20 to 4000 characters after trimming. An invalid field is named beside the
   field in the current language before anything is sent, and the server refuses the same
   input with a field-keyed map under `errors` so the form renders the server's refusal in
   the same place.
4. The form carries a decoy field, `company_website`, hidden from people and from
   assistive technology. **A submission whose decoy field is not empty is refused, stores
   nothing and sends nothing.**
5. An accepted submission stores one enquiry with a reference of the form `ENQ-` followed
   by four digits, sequential, the status `new`, the name, the email, the message, the
   current language and the time received. The answer carries `reference` and
   `created_at`.
6. On success a toast confirms, naming the reference: `Thanks, we got your enquiry` or
   `Grazie, abbiamo ricevuto la tua richiesta`. The form then clears.
7. **On failure the form never loses what was typed.** A refused or failed submission
   shows the reason in a toast and beside the field it concerns, and every field keeps its
   value.
8. **Each accepted enquiry sends exactly one mail message** to
   `hello@avx-studio.example.com` and to nobody else, with no copied or blind-copied
   recipient. Its subject is `Enquiry from ` followed by the visitor's name, and its body
   carries the name, the email address, the message and the reference. Nothing is mailed
   to the visitor. A refused submission sends no mail at all.
9. **At most ten enquiries are accepted from one address in any rolling hour.** The
   eleventh is refused, stores nothing, sends nothing, and says when the visitor may try
   again. Refused submissions do not count toward the ten.
10. The enquiry endpoint sets no cookie of any kind.

### 6. The studio inbox

`/inbox` is where the studio reads what visitors sent. It is a table first.

1. `/inbox` shows every stored enquiry as one row of a table, newest first, with the
   columns `Reference`, `Received`, `Name`, `Email` and `Status`. Opening a row shows the
   full message and the language it was sent in.
2. **The row shows exactly what the visitor submitted**: the same name, the same email and
   the same message, character for character.
3. A status control on each enquiry moves it between `new`, `replied` and `archived`. The
   change is saved at once, a toast confirms it, and **reloading `/inbox` shows the saved
   status**. Any other status value is refused and the stored status is unchanged.
4. An enquiry cannot be deleted from the inbox or from the read surface.
5. `GET /api/enquiries`, `GET /api/enquiries/<reference>` and
   `PATCH /api/enquiries/<reference>` answer the studio alone. A visitor with no token, an
   unknown token or an expired token is denied, and **no enquiry's name, email or message
   appears in any response to a caller who is not the studio.**
6. An unknown reference answers as not found.

### 7. Localisation

Two languages: Italian, `it`, the default, and English, `en`.

1. `/` answers with a redirect to `/en` when the request's preferred language is English,
   and to `/it` otherwise.
2. The header carries a language switch, `IT` and `EN` separated by `/`, with the inactive
   language at half opacity. On the home, switching moves between `/it` and `/en`.
   Elsewhere the route re-renders in the other language, and the choice is remembered on
   the device without a cookie.
3. The header links read `All Works`, `Studio` and `Contact` in English and
   `Tutti i progetti`, `Studio` and `Contatti` in Italian.
4. Every content read accepts `locale` as `it` or `en`, defaults to `it`, and refuses any
   other value. Project summaries, discipline labels, the studio intro and service
   paragraphs, the navigation labels and the footer all come back in the language asked
   for. Project titles and clients are the same in both.
5. Every route declares its own document title and description in the current language.
   The English home is titled `Studio AVX | Brand & Digital Design Studio based in Italy`
   and the Italian studio page `Studio grafico e di comunicazione a Catania`.

### 8. Consent

1. On a first visit a consent banner offers `Accept` and `Reject`, or `Accetta` and
   `Rifiuta`, with a link to `/privacy`. It uses its own grey palette, which appears on no
   other surface, and sits above everything else.
2. **Before a choice is made, no response sets a cookie**, on any route or any read.
3. Making a choice writes the cookie `cc_cookie` recording which choice was made, and the
   banner does not return on later visits.
4. This build loads no third-party analytics script. The recorded choice is honoured so
   that any measurement added later stays off after `Reject`.

### 9. The not-found page

1. Any address that is not a route answers with the not-found status while still serving
   the page, including addresses that look plausible. The addresses probed on the reference,
   `/gs`, `/g/d`, `/as`, `/as/d`, `/test` and `/gtag/js`, are non-routes and answer this way.
2. The page is a simulated broken television: the blue screen framed as a curved tube, the
   corners falling to black, a soft sheen across the top, the whole surface bowed as if
   pressed onto curved glass, the glare of a soft top sheen, the bulge of an SVG displacement filter that warps the
   surface like curved CRT glass, a live animated static layer fading as it clears, and a
   glitch in which live layers tear the text into horizontal streaks before it settles.
3. In Italian it reads `404`, `Pagina non trovata.`,
   `Il contenuto che stai cercando non esiste o è stato spostato.` and offers
   `Torna alla home`. In English it reads `404`, `Page not found.`,
   `The content you are looking for does not exist or has moved.` and offers
   `Back to home`. The action returns to the home in the current language, and the header
   stays in place.

### 10. The site's own surface

1. Every cover, every gallery image and the wordmark carries alternative text; a project
   image's alternative text names the project. The three dimensional canvases are marked
   decorative, because the Works catalogue and the project pages carry the same content.
2. At a narrow viewport of 390px no route scrolls sideways. Below 768px the header links
   collapse behind a frosted `MENU` button that opens a full overlay whose button then
   reads `× CLOSE`.
3. Every internal link on every public route leads to a route that answers with success;
   no internal link leads to the not-found page.
4. `/privacy` carries the eyebrow `Note legali`, the title `Privacy & Cookie Policy`, the
   line `Ultimo aggiornamento: 15 giugno 2026`, the data controller `Grafiche Meridiane`,
   which is the registered legal entity, with its VAT registration number, its registered
   street address and the contact address, and seven numbered sections headed
   `1. Titolare del trattamento`, `2. Tipologie di dati e finalità`,
   `3. Modalità del trattamento`, `4. Destinatari dei dati`,
   `5. Conservazione dei dati`, `6. Diritti dell'interessato` and `7. Cookie Policy`. The
   cookie section carries a table headed `Nome`, `Tipo`, `Finalità` and `Durata` with a row
   for `cc_cookie`.

## User flow

| Path | Who | What |
|---|---|---|
| `/` | anyone | redirects to `/it` or `/en` by preferred language |
| `/it`, `/en` | anyone | the spatial gallery with the formation switch and the footer line |
| `/works` | anyone | the catalogue in `Grid` or `List` with the six facets |
| `/works/<slug>` | anyone | one project with previous and next |
| `/studio` | anyone | the studio page with the turning sculpture |
| `/contact` | anyone | the enquiry form and the public address |
| `/privacy` | anyone | the privacy and cookie policy |
| `/login` | studio | sign in |
| `/inbox` | studio | the stored enquiries as a table with a status per row |
| anything else | anyone | the broken-television not-found page with the not-found status |

### Entry and redirects

The front door is `/`, which redirects to the home in the visitor's language. Nothing a
visitor reads is behind an account. `/works/` and `/studio/` redirect permanently to their
bare forms. A visitor who opens `/inbox` without a session is sent to `/login` and returns
to `/inbox` after signing in. A signed-in studio member who opens `/login` is sent to
`/inbox`.

### Journeys

1. **Fly the gallery.** Open `/en`. The boot loader counts up from `[0]` and wipes away to
   reveal the scene. Scroll, and the focus moves from one card to the next with its label
   pill. Choose `Spiral`; the cards morph from rings into a helix. Reload; `Spiral` is
   still chosen.
2. **Narrow the catalogue.** Open `/works`. The grid shows twenty covers and the filter
   pill reads `All (20)`. Open the filter and choose `Packaging (2)`; the grid narrows to
   `Etna Wine Cellars` and `Sale Marino`. Switch to `List`; the same two rows show as a
   typographic index.
3. **Open a project.** Choose `Sale Marino`. The page transition slides across and the
   project page shows its cover, disciplines, year `2023` and client `Saline di Trapani`.
   Choose next; `Teatro Bellini` opens.
4. **Send an enquiry.** Open `/contact`. Submit with a message of five characters; the
   message field is named invalid beside it and nothing is sent. Complete the message and
   submit; a toast confirms with a reference beginning `ENQ-`, and the form clears.
5. **Read it as the studio.** Sign in at `/login` as `studio@example.com`. `/inbox` lists
   the new enquiry first with the status `new` and the exact name, email and message.
   Mark it `replied`; a toast confirms. Reload; it still reads `replied`.
6. **Change the language.** Choose `IT` in the header on `/works`; the filter reads
   `Tutti (20)` and `Editoria (5)`.
7. **Land nowhere.** Open `/test`. The broken television appears with `404` and an action
   back to the home.

### States

The gallery's loading state is the boot loader, shown once per visit. A facet that matches
nothing cannot occur with the seed, but the catalogue still states an empty result rather
than showing a blank floor. The enquiry form's sending state disables the submit action and
keeps every field's value. An empty inbox states that no enquiries have arrived. A device
that cannot draw the three dimensional scene gets the flat catalogue on the home rather
than an error.

## UI/UX notes

**Colour.** One electric ultramarine blue carries almost the entire site: it is the void
behind the gallery, the ground of every route, and the single accent. Against it sit white
for type, marks and cards, and pure black for the letterbox of the not-found page, deep
shadow, and the base the cursor blends against. A darker blue marks pressed and deep
states; a handful of near-black tones appear on rare dark surfaces. White is used at many
strengths for hairlines and secondary type, and frosted controls take a faint dark glass
fill with a white hairline. The consent banner alone uses a self-contained neutral grey
scale, from a dark slate grey for its text to pale blue-grey panel fills, and that grey
appears nowhere else. The three dimensional layer carries its own small palette of white
with cyan, green, orange and red accents over very dark greys.

**Typography.** One variable sans family carries everything, from micro labels to display
headings nearly the height of the screen, across a weight axis from 100 to 900, loaded with
a swap so text is never invisible. Display sizes run at `165.6px`, `113.85px` and `76px`
with tight line heights near nine tenths of the size; sub-headings at `28px`; lead
paragraphs at `20px`; body at `16px` in regular and bold; captions at `14px`; labels and
eyebrows at `13px` at a medium weight.

**Grid and depth.** Layout sits on a twelve column grid with a `58px` side margin and a
larger `110px` margin, a gap of a quarter column, and three vertical spacing steps of
`60px`, `80px` and `160px`. The shell isolates its blend scope so the difference-blended
cursor and any screen-blended layer composite against a known backdrop. The consent banner
sits above everything.

**Motion.** Motion is the product here, and nothing simply appears. The easing vocabulary has two speeds:
a quick, crisp standard ease for grids, menus and controls, and a slower expressive settle
that rushes in and eases to a soft stop for reveals and large elements. Rows of items rise
in a staggered wave with incrementing delays. Headings and paragraphs are split into words
and glyphs that translate up into place. Large elements fade in over most of a second.
Every transition names the properties it animates. The page transition slides a full panel
across the viewport between routes. The custom cursor is a small filled dot that inverts
whatever is behind it and follows the pointer with an eased lag. **Under reduced motion
every reveal resolves to its end state without travel, scroll no longer scrubs large
motion, and the ambient scene motion calms**; nothing that carries information is removed.

**Scroll.** Scrolling has weight: the wheel feeds an eased velocity rather than moving the
page one to one. On the home and on Works the document does not scroll and the wheel drives
the scene instead. On the studio page and the privacy page the document scrolls normally,
and on the studio page a scroll-scrubbed timeline ties the word reveals, the image wipes and the
turning sculpture to the scroll position.

**Responsive.** The breakpoint that matters is `768px`: below it the header collapses
behind the frosted `MENU` button, the formation switch moves to the bottom left thumb zone,
and the Works controls reposition. A second breakpoint at `1024px` separates the tablet
band. Pointer and hover are branched explicitly, so a precise pointer gets the custom cursor
and hover affordances and a touch screen gets neither and drags the scene with a finger.
The three dimensional scene refits its spacing and camera framing to a tall narrow viewport.

**Accessibility.** Keyboard navigation reaches every route, the language switch, the
formation and view switches, the facets, the filter close control and the enquiry form, in
a logical order with a visible focus state. The Works catalogue is the complete keyboard and
screen reader equivalent of the gallery. White type over the blue and over bright covers
keeps a soft legibility shadow, and every text and ground pairing is measured against the
WCAG contrast standard for its size. Icon-only controls carry accessible names: the arrow,
the menu button, the language switch and the filter close control. The home and the studio
page keep a real `h1` in the document while the visible heading is a decorative split-text
effect.

## Front-end specification

### The shell

The module architecture starts from the app shell. The app shell holds the header, the cursor, the boot loader, the page transition layer
and the consent banner, and they persist across route changes. **One long-lived three
dimensional render context survives route changes** and swaps what it shows (the home
gallery, the studio sculpture, the not-found layers) rather than being torn down and
rebuilt on every route. A scroll orchestrator instance maps the smooth-scroll position onto the
scene's focus index on the fixed-viewport routes. Visual state is class driven: an active control, a revealed canvas,
a visible element, a scrolling document and an open menu each set a class, transitions key
off the class, and the render layer reads the same flags.

### Global chrome

- **Header.** Fixed across the top. The `AVX` wordmark sits at the left, set as a three
  glyph logotype in the site family and shown solid white on the blue. The links and the
  language switch sit at the right. Each link carries a leading dot that scales in from
  nothing when the header reveals. Link type keeps a soft dark legibility shadow.
- **Mobile menu.** Below `768px` the links collapse behind a frosted pill reading `MENU`.
  Opened, it becomes a full overlay, its label reads `× CLOSE`, and the menu link glyphs
  rise into place one by one.
- **Cursor.** A single filled dot with a difference blend that inverts whatever is behind
  it, following the pointer with an eased lag. It is absent on a coarse pointer.
- **Boot loader.** On the first load of a visit, a full screen loader with a counter counting up from `[0]`
  while white patches wipe the screen, then reveals the scene. It does not return on
  route changes.
- **Page transition.** A full-bleed panel slides a viewport height across between routes,
  so no route ever simply cuts to the next.
- **Consent banner.** First visit only, on its own grey palette, above everything.
- **Home footer.** The three part line of core feature 1.

### Iconography

Almost nothing is an icon file. The one icon that matters is the north east "open" arrow on
every project label, drawn as inline geometry on a twelve unit box: a single stroked white
path with no fill, a diagonal shaft from the lower left to the upper right and two short
arrowhead legs back along the top edge and down the right edge. Several marks are pure
circles drawn as fully rounded boxes rather than glyphs: the cursor, the navigation link
dots, the not-found page's home bullet and the Works filter bullet.

### The gallery

- The canvas fills the viewport over the blue. Top and bottom edge gradients fade the blue
  to transparent so cards never collide with the header or the footer line.
- In `Rings`, cards are distributed around ring paths in depth with the chrome spine
  threading through the centre; the focused card sits large and upright at centre right
  while the others recede as small perspective-skewed planes. In `Spiral`, the same cards
  wind along one helical path receding into depth.
- The formation switch is a frosted fully rounded segmented control revealed with a blur.
- The label pill is frosted and fully rounded, carrying the title, the first discipline
  label and the arrow. The `SCROLL` cue is a separate pill.
- The spine and the studio sculpture take a chrome material reflecting an environment
  painted as a vertical gradient, brighter above and darker below, tinted toward the blue,
  with one small hot white highlight for a crisp specular.

### The catalogue

- The grid floats slightly rotated covers over a faint darker blue perspective grid
  receding to a vanishing point. Wheel and drag pan the grid.
- The covers fade in on a dedicated reveal canvas once loaded.
- The view switch is the same frosted segmented control as the formation switch; the
  filter is a frosted pill at the bottom centre that opens the facet list.
- Grid thumbnails load the small cover and the project page loads the large one.

### The studio page and the not-found page

- The studio page's editorial images wipe open from the bottom edge as scroll reaches them,
  and drift with a gentle parallax.
- The not-found tube is built from layers: a vignette taking the corners to black, a soft
  top sheen blended onto the screen, a bezel and letterbox that mask everything outside the
  rounded tube to black, and a displacement filter that bows the whole surface. The `404`
  glyphs are split into top and bottom halves so they shear independently. The code, the
  title and the copy keep a heavier legibility shadow.

### Assets

This is the zero-asset substitution guide. **No binary asset, image file, model file or font
file is required for the site to stand up.**

- Cover and gallery images are generated on a canvas, seeded per project so each is stable
  and distinct: a brand blue field, a bold off-centre white shape or initial, and a soft
  dark corner vignette. The small and large variants come from the same generator at two
  sizes.
- The spine and the sculpture are built from primitives: rounded boxes and capsules stacked
  along a vertical path for the beaded spine, and a taller stack of rounded forms for the
  studio object.
- The CRT static and grain on the not-found page are drawn fresh as random luminance noise each frame, and the tearing
  is a horizontally shifted copy.
- The single variable family is named with the fallback stack
  `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif`.

### Performance

- The home gallery holds a smooth frame rate on a mid-range laptop of a few years' age, and
  the smooth scroll and the render loop are driven from one animation frame so they never
  fight.
- Models and large imagery load only when the route and formation need them.
- The shell and its text arrive before the render layer, which starts once the page is
  interactive.
- Graceful degradation: where WebGL is unavailable or the device is weak, the flat catalogue is
  the primary experience and the site falls back to it rather than showing a broken canvas.

## Technical requirements

Serve this site as a single-page application rendering every route in the browser from a
JSON surface. The frontend is **Lit components built with Vite**, and the read and write
surface under `/api` is **NestJS**, served by the same process on the same origin and port,
which also serves the built application shell. The server answers `/` with a redirect to
the home in the preferred language, answers `/works/` and `/studio/` with permanent
redirects, and answers any address that is not a route with the not-found status while still
serving the shell. The three dimensional layer runs in the browser.

The datastore is **PostgreSQL**, read from `DATABASE_URL`, which the environment also
injects as `DB_URL` carrying the same value. Mail is sent over SMTP to `SMTP_HOST`. The
app's own address and port come from `APP_PUBLIC_URL` and `APP_PUBLIC_PORT`. Never hardcode
a host or a port; read every one of them from the environment. Both backing services are
**already running** and reachable at those variables and must not be downloaded, installed,
compiled or started.

Use only the libraries named here plus their direct dependencies. Do not introduce
a second database, cache, queue, object store, identity provider or mail vendor: the
only backing services available in this environment are PostgreSQL and Mailpit, and
reaching for anything else is a contract violation.

**Content is seeded, not edited.** The twenty projects, the five disciplines, the studio
content and the privacy text are seed rows in PostgreSQL. There is no content editing
surface and no external content service.

**Identity.** No account is needed to read anything or to send an enquiry. An account
exists for one job, reading and triaging enquiries, and holds an identifier, an email, a
name, a role and a password hash, nothing more. Authentication is app-implemented email and
password with bearer tokens as described under `### Auth`. Passwords are stored hashed and
never in a recoverable form.

**Counts are queries.** Every facet count and the footer's featured and total numerals are
counted from the project rows when they are read. None is stored and none is typed into a
template.

**Anti-abuse.** The enquiry endpoint applies the decoy field and the per-address limit of core
feature 5. Sign in is limited per address with a low burst, because a failed sign in is
cheap for the caller. A limited response states when the caller may try again.

**No tracking before consent.** No response sets a cookie before a consent choice exists.
The only cookie the site itself ever writes is `cc_cookie`, and the enquiry endpoint writes
none. No third-party script loads.

`GET /api/health` returns `200` once the app is ready to serve. Log each request as one
structured line carrying the method, the path, the status and the elapsed milliseconds, to
standard output.

**Nothing the browser downloads carries a credential.** No database URL, no mail host and no
bearer token belonging to another account appears in any document, script, stylesheet or
JSON the browser can fetch.

**Responses.** A validation failure carries a field-keyed map under `errors`. A failure
carries a human message. Dates are one format in one timezone.

## Data model

Eight tables, one per entity. All timestamps are UTC.

**Every seeded account uses the password `deku-demo-pw-2026`.** It is benchmark
fixture data, not a credential to protect. Hash it as normal; the exact literal must
work at login, and it must be written into `/app/USER_README.md` alongside each
account so a grader can sign in.

**`users`** - `id`, `email` unique, `name`, `role`, `password_hash`, `created_at`. Two rows
are seeded, as listed in `## User roles`, both with the role `studio`.

**`sessions`** - `token`, `user_id`, `issued_at`, `expires_at`, `retired_at`.

**`disciplines`** - `key` unique, `label_it`, `label_en`, `position`. Five rows, in this
order:

| key | label_en | label_it |
|---|---|---|
| `branding` | Branding | Branding |
| `editorial` | Editorial | Editoria |
| `type-design` | Type Design | Type Design |
| `web-design` | Web Design | Web Design |
| `packaging` | Packaging | Packaging |

**`projects`** - `id`, `slug` unique, `title`, `client`, `year`, `summary_it`,
`summary_en`, `position`, `featured`, `cover_small`, `cover_large`. The two summaries hold the
localised strings; the client is one string in both languages; `featured` is a boolean marking
the featured subset the home footer counts. Twenty rows, in this
catalogue order:

| position | slug | title | disciplines | year | client | featured |
|---|---|---|---|---|---|---|
| 1 | `amts-card` | AMTS Card | branding | 2024 | AMTS Catania | yes |
| 2 | `infectious-diseases` | Infectious Diseases | editorial | 2023 | SIMIT Sicilia | yes |
| 3 | `avx-alphabet` | AVX Alphabet | type-design | 2022 | Studio AVX | yes |
| 4 | `herbert` | Herbert | type-design | 2021 | Studio AVX | yes |
| 5 | `stelvio-grotesk` | Stelvio Grotesk | type-design, branding | 2025 | Stelvio Tessuti | yes |
| 6 | `etna-wine-cellars` | Etna Wine Cellars | branding, packaging | 2024 | Cantine Etna Nord | yes |
| 7 | `sale-marino` | Sale Marino | packaging, branding | 2023 | Saline di Trapani | yes |
| 8 | `teatro-bellini` | Teatro Bellini | branding, web-design | 2025 | Teatro Massimo Bellini | yes |
| 9 | `ortigia-journal` | Ortigia Journal | editorial | 2022 | Ortigia Edizioni | yes |
| 10 | `lava-coffee` | Lava Coffee | branding | 2021 | Lava Coffee Roasters | yes |
| 11 | `porto-digitale` | Porto Digitale | web-design | 2026 | Porto di Catania | yes |
| 12 | `museo-diffuso` | Museo Diffuso | editorial | 2020 | Comune di Noto | yes |
| 13 | `fiera-del-libro` | Fiera del Libro | editorial | 2019 | Fiera del Libro Siciliana | no |
| 14 | `agrumi-bio` | Agrumi Bio | branding | 2020 | Agrumi Bio Paterno | no |
| 15 | `cinema-lumiere` | Cinema Lumiere | branding | 2018 | Cinema Lumiere | no |
| 16 | `atlante-verde` | Atlante Verde | editorial | 2019 | Legambiente Sicilia | no |
| 17 | `kiosk-app` | Kiosk App | web-design | 2024 | Kiosk Mobility | no |
| 18 | `scirocco-festival` | Scirocco Festival | branding | 2022 | Scirocco APS | no |
| 19 | `bottega-ceramica` | Bottega Ceramica | branding | 2018 | Bottega Ceramica Caltagirone | no |
| 20 | `marea-hotel` | Marea Hotel | branding | 2017 | Marea Hotel Taormina | no |

A project's disciplines are listed in the order its label pill uses them: the first one
listed is the one the pill shows.

**`project_disciplines`** - `project_id`, `discipline_key`, `position`, unique on the pair.
Twenty four rows, one per discipline listed above.

**`project_media`** - `id`, `project_id`, `position`, `src`, `alt`. Three rows per project.

**`studio_services`** - `id`, `position`, `label_it`, `label_en`, `body_it`, `body_en`. Six
rows, as listed under core feature 4.

**`enquiries`** - `id`, `reference` unique, `name`, `email`, `message`, `locale`, `status`
in `new`, `replied` or `archived`, `created_at`, `status_changed_at`, `address_hash`. Three
rows are seeded:

| reference | name | email | locale | status |
|---|---|---|---|---|
| `ENQ-0001` | Anna Rizzo | `anna.rizzo@example.com` | `it` | `new` |
| `ENQ-0002` | Luca Bianchi | `luca.bianchi@example.com` | `it` | `replied` |
| `ENQ-0003` | Sofia Greco | `sofia.greco@example.com` | `en` | `archived` |

`address_hash` holds a one-way hash of the sender's network address, used only for the
enquiry limit; the address itself is never stored.

## Constraints

- One studio, one site: no tenancy.
- No content editing interface: no project, discipline, studio or privacy content is
  created, edited or deleted through the product.
- No public signup and no visitor account.
- No enquiry deletion.
- No shop, newsletter, blog or search.
- No ambient or interaction audio.
- No third-party script and no analytics provider.
- No external network call at runtime: the site answers every route from PostgreSQL, the
  mail transport and its own built application.
- The sign-in page and `/inbox` are the only surfaces that are not part of the reference
  studio site; they exist so a stored enquiry can be read back.
- No native application and no installable app shell.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is
  `${APP_PUBLIC_PORT}:4173` - `4173` is the container-internal port and
  `APP_PUBLIC_PORT` is what the outside world uses. Read both from the environment;
  never hardcode either.
- The HTTP API is served on that same origin under the `/api` prefix.
- `GET /api/health` returns `200` once the app is ready.
- The app starts from the environment image with no manual steps.
- Login credentials - or an explicit statement that there are none - are written to
  `/app/USER_README.md`.
- Reserved `.browser_screenshots/` and `.downloads/` directories exist at the app
  root, empty.
- Serve a production build behind a static or preview server - never a dev server.
- The server must keep running after this session ends and must not be a child of
  the shell. An ordinary background job dies with its shell, and the app will not be
  running when it is next opened.
- Bind `0.0.0.0`, never `127.0.0.1` or `localhost`. A loopback-only listener is
  unreachable from outside the container.
- The backing services named in this brief are already running and reachable at
  their environment variables. Do not download, install, compile or start a copy of
  any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

### API shapes

Every list endpoint returns a top-level JSON array. Bearer auth is carried on the studio
endpoints. A successful call returns the named resource or shape; an invalid or
unauthorized call is rejected as a client error, never with a `5xx` and never with a silent
success.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/login` | `email`, `password` | `token`, `user` with `id`, `email`, `name`, `role` |
| `POST /api/auth/logout` | none | `{}`, and the token is retired |
| `GET /api/me` | none | `user` |
| `GET /api/projects` | `locale`, `discipline` | array of `slug`, `title`, `client`, `year`, `position`, `featured`, `disciplines` as keys, `discipline_labels`, `cover_small`, `cover_alt` |
| `GET /api/projects/{slug}` | `locale` | one project with `summary`, `cover_large`, `media` each with `src` and `alt`, `previous` and `next` each with `slug` and `title` |
| `GET /api/facets` | `locale` | array of `key`, `label`, `count`, `all` first then the five disciplines in order |
| `GET /api/studio` | `locale` | `eyebrows`, `statement`, `intro`, `services` each with `label` and `body` |
| `GET /api/global` | `locale` | `nav` with `works`, `studio`, `contact`; `footer` with `tagline`, `featured`, `total` |
| `POST /api/enquiries` | `name`, `email`, `message`, `locale`, `company_website` | `reference`, `created_at`; or a refusal with `errors` |
| `GET /api/enquiries` | none | array of `reference`, `name`, `email`, `message`, `locale`, `status`, `created_at`, newest first |
| `GET /api/enquiries/{reference}` | none | one enquiry |
| `PATCH /api/enquiries/{reference}` | `status` | the enquiry with the new status |

### No mocks

PostgreSQL and the mail transport are the facts. An enquiry held in a module-level array,
a notification written to the log instead of sent, a toast shown without a stored row, a
facet count typed into the page, a project list shipped as a static JSON file the API never
reads: each of these is a contract violation however good the page looks. The named
provider is the fact - the app's UI and its own tables can only reflect what lives in the
provider, never substitute for it.

## Definition of done

A prospective client can fly through twenty works in a live three dimensional gallery and
switch it between rings and a spiral, narrow the Works catalogue to a discipline with counts
that are always right, open a project and step through the rest, and send an enquiry that
is stored, delivered to the studio by mail, and shown back to the studio exactly as it was
written. Nobody but the studio can read a stored enquiry, and no cookie is set before the
visitor has chosen.
