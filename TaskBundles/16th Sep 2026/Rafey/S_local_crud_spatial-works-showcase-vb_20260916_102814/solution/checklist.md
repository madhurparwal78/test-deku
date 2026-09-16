# Checklist: Studio AVX

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, frontend, technical, datamodel, constraints, deployment
Sections absent: buildplan
Items: 247
Unpinned values flagged: 0

## C-OV Overview

- [ ] `C-OV-01` `capability` The home gallery shows twenty project cards floating at different depths around a chrome spine over the electric blue `src: Overview`
- [ ] `C-OV-02` `capability` The formation switch moves the gallery cards between Rings plus Spiral `src: Overview`
- [ ] `C-OV-03` `capability` The Works catalogue carries the same twenty projects stored once in catalogue order `src: Overview`
- [ ] `C-OV-04` `capability` The flat catalogue is the accessible equivalent of the home, which shows the flat catalogue where WebGL is unavailable `src: Overview`
- [ ] `C-OV-05` `capability` An accepted enquiry is stored exactly as submitted `src: Overview`
- [ ] `C-OV-06` `capability` An enquiry notification mail reaches the studio inbox alone `src: Overview`
- [ ] `C-OV-07` `constraint` A filled decoy field is refused, with nothing stored or mailed `src: Overview`
- [ ] `C-OV-08` `constraint` A visitor cannot list or read any stored enquiry `src: Overview`
- [ ] `C-OV-09` `constraint` No response sets a cookie before a consent choice `src: Overview`
- [ ] `C-OV-10` `capability` The site answers in Italian plus English, with navigation labels following the requested locale `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads every public route without an account, which is why every internal link leads to a route answering success `src: User roles`
- [ ] `C-RL-02` `role` A visitor sends an enquiry, which is accepted then stored exactly as submitted `src: User roles`
- [ ] `C-RL-03` `role` A visitor cannot list, read, or change any stored enquiry `src: User roles`
- [ ] `C-RL-04` `role` The inbox sends a visitor without a session to sign in `src: User roles`
- [ ] `C-RL-05` `role` The studio lists every stored enquiry newest first `src: User roles`
- [ ] `C-RL-06` `role` The studio moves an enquiry between `new`, `replied`, `archived`, a status change surviving a reload `src: User roles`
- [ ] `C-RL-07` `role` A stored enquiry cannot be deleted by the studio `src: User roles`
- [ ] `C-RL-08` `contract` Authorization is enforced server-side, so a visitor cannot read any stored enquiry through a direct call to a studio endpoint `src: User roles`
- [ ] `C-RL-09` `contract` A refused visitor call leaves the stored enquiry status unchanged `src: User roles`
- [ ] `C-RL-10` `literal` Two studio accounts are seeded, stored once with hashed passwords, both using `deku-demo-pw-2026` `src: User roles`
- [ ] `C-RL-11` `literal` The seeded studio account `studio@example.com` is Giulia Ferro, stored once with a hashed password `src: User roles`
- [ ] `C-RL-12` `literal` The seeded studio account `studio2@example.com` is Marco Lentini, stored once with a hashed password `src: User roles`
- [ ] `C-RL-13` `literal` The studio lists the seeded enquiries `ENQ-0001` from Anna Rizzo at `new`, `ENQ-0002` from Luca Bianchi at `replied`, `ENQ-0003` from Sofia Greco at `archived` `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `contract` `POST /api/auth/login` takes `email` plus `password`, refusing a wrong password as the login refuses an unknown email `src: Core features`
- [ ] `C-CF-02` `literal` A wrong password is refused with the message `Sign in failed`, alike to an unknown email `src: Core features`
- [ ] `C-CF-03` `constraint` A missing token, an unknown token, a retired token are all refused `src: Core features`
- [ ] `C-CF-04` `contract` `POST /api/auth/logout` retires the token `src: Core features`
- [ ] `C-CF-05` `literal` A token expires 24 hours after issue; a retired token is refused like a missing one `src: Core features`
- [ ] `C-CF-06` `constraint` Passwords are stored hashed, the seeded accounts signing in with the literal without the literal being stored `src: Core features`
- [ ] `C-CF-07` `capability` `/login` is the sign-in page; the inbox sends a visitor without a session to sign in, returning to `/inbox` afterwards `src: Core features`
- [ ] `C-CF-08` `ui` Signing in at `/login` as `studio@example.com` with a wrong password shows the refusal message `Sign in failed` `src: Core features`
- [ ] `C-CF-09` `capability` The home draws a live three dimensional canvas filling the viewport over the brand blue `src: Core features`
- [ ] `C-CF-10` `ui` Twenty project cards float at different depths around a central chrome spine of rounded bead forms `src: Core features`
- [ ] `C-CF-11` `ui` The formation switch reads `Rings` beside `Spiral`, at the top centre on a wide screen, `Rings` being the default `src: Core features`
- [ ] `C-CF-12` `ui` Choosing `Spiral` in the formation switch makes the cards rearrange into a helix, the chosen formation still selected after a reload `src: Core features`
- [ ] `C-CF-13` `ui` Scrolling over the home changes the focused card, the label pill then showing a different project title `src: Core features`
- [ ] `C-CF-14` `ui` The focused card carries a frosted label pill with the project title, the first discipline, a north east arrow `src: Core features`
- [ ] `C-CF-15` `ui` A pill reading `SCROLL` shows on the home until the first scroll changes the focused card `src: Core features`
- [ ] `C-CF-16` `capability` Choosing the focused card opens the project page through a sliding panel `src: Core features`
- [ ] `C-CF-17` `literal` The home keeps a visually hidden `h1` reading `AVX - Brand & Digital Design Studio`, with the live canvas marked decorative `src: Core features`
- [ ] `C-CF-18` `literal` The home footer line reads `BRAND & DIGITAL DESIGN STUDIO`, `12 / 20` `selected Works`, `© 2026` `src: Core features`
- [ ] `C-CF-19` `data` The footer counts featured over total projects from stored rows rather than typed numerals `src: Core features`
- [ ] `C-CF-20` `capability` Without WebGL the home shows the flat catalogue, reaching every one of the twenty projects `src: Core features`
- [ ] `C-CF-21` `ui` Under reduced motion the formation switch changes the arrangement of the cards without a continuous rearrangement `src: Core features`
- [ ] `C-CF-22` `contract` The works slash form redirects permanently: `/works/` to `/works` `src: Core features`
- [ ] `C-CF-23` `ui` The catalogue grid floats slightly rotated covers over a darker blue perspective floor `src: Core features`
- [ ] `C-CF-24` `ui` Opening `/works` shows a grid of twenty project covers with the filter pill reading `All (20)` `src: Core features`
- [ ] `C-CF-25` `ui` The view switch offers `Grid` plus `List`; choosing `List` shows the projects as rows with disciplines, year, client `src: Core features`
- [ ] `C-CF-26` `literal` The English facet labels are `All`, `Branding`, `Editorial`, `Type Design`, `Web Design`, `Packaging`, in that facet order with counts computed `src: Core features`
- [ ] `C-CF-27` `literal` The Italian facet labels are `Tutti`, `Branding`, `Editoria`, `Type Design`, `Web Design`, `Packaging`, the counts computed identically `src: Core features`
- [ ] `C-CF-28` `literal` Facet counts are computed from stored disciplines: `All (20)`, `Branding (11)`, `Editorial (5)`, `Type Design (3)`, `Web Design (3)`, `Packaging (2)` `src: Core features`
- [ ] `C-CF-29` `constraint` Facet counts are computed at read time from the stored disciplines, never stored as numbers `src: Core features`
- [ ] `C-CF-30` `capability` A discipline facet narrows the catalogue in place, keeping catalogue order `src: Core features`
- [ ] `C-CF-31` `ui` Choosing a facet in the filter pill narrows the covers with a rising staggered reveal, a close control reading `×` closing the list `src: Core features`
- [ ] `C-CF-32` `ui` Choosing `Packaging (2)` in the filter narrows the grid to Etna Wine Cellars plus Sale Marino `src: Core features`
- [ ] `C-CF-33` `capability` A project page carries the large cover, title, disciplines, year, client, a localised summary, gallery images as metadata `src: Core features`
- [ ] `C-CF-34` `capability` A project page offers the previous project plus the next project in catalogue order, wrapping at both ends `src: Core features`
- [ ] `C-CF-35` `ui` A project page offers a way back to the catalogue alongside the previous plus next project `src: Core features`
- [ ] `C-CF-36` `constraint` An unknown project slug answers as not found `src: Core features`
- [ ] `C-CF-37` `ui` Opening Sale Marino shows the project page with the year `2023` plus the client Saline di Trapani `src: Core features`
- [ ] `C-CF-38` `ui` Choosing the next project from Sale Marino opens Teatro Bellini `src: Core features`
- [ ] `C-CF-39` `contract` The studio slash form redirects permanently: `/studio/` to `/studio` `src: Core features`
- [ ] `C-CF-40` `literal` The studio content serves the eyebrows `BASED IN CATANIA / SICILY`, `SINCE 2017`, `BRANDING / DIGITAL / TYPE / PACKAGING` `src: Core features`
- [ ] `C-CF-41` `literal` The studio content serves the statement `WE DON'T JUST DESIGN WE DEFINE ATTITUDES` `src: Core features`
- [ ] `C-CF-42` `literal` The studio content serves six Italian services: `DESIGN EDITORIALE`, `TYPE DESIGN`, `SOCIAL MEDIA DESIGN`, `COPYWRITING E NAMING`, `BRANDING`, `WEB DESIGN` `src: Core features`
- [ ] `C-CF-43` `literal` The English studio content serves `DESIGN EDITORIALE` as `EDITORIAL DESIGN`, keeping `TYPE DESIGN`, `SOCIAL MEDIA DESIGN`, `BRANDING`, `WEB DESIGN` across the six services `src: Core features`
- [ ] `C-CF-44` `literal` The studio page keeps a hidden `h1` reading `Studio AVX - grafica, branding e comunicazione a Catania` beside the display word `STUDIO` `src: Core features`
- [ ] `C-CF-45` `ui` The studio page lists the services as a two column list separated by hairlines beside a turning chrome sculpture `src: Core features`
- [ ] `C-CF-46` `ui` Scrolling `/studio` reveals the eyebrow `SINCE 2017`, the statement, six service labels `src: Core features`
- [ ] `C-CF-47` `literal` The contact page shows the public address `hello@avx-studio.example.com`, the studio inbox the notification mail reaches `src: Core features`
- [ ] `C-CF-48` `ui` The enquiry form labels read `Name`, `Email`, `Message` or `Nome`, `Email`, `Messaggio`, every field carrying a visible label `src: Core features`
- [ ] `C-CF-49` `literal` An invalid enquiry name outside 2 to 120 characters is refused with field-keyed errors, nothing stored `src: Core features`
- [ ] `C-CF-50` `literal` An invalid enquiry message outside 20 to 4000 characters is refused with field-keyed errors, nothing stored `src: Core features`
- [ ] `C-CF-51` `constraint` A malformed email is an invalid enquiry field, refused with the error keyed by the field, nothing stored `src: Core features`
- [ ] `C-CF-52` `ui` The enquiry form names each invalid field beside the field before anything is sent `src: Core features`
- [ ] `C-CF-53` `ui` Submitting a message of five characters names the message field invalid beside the field with nothing sent `src: Core features`
- [ ] `C-CF-54` `literal` A filled decoy field `company_website` is refused, nothing stored, nothing mailed `src: Core features`
- [ ] `C-CF-55` `literal` An accepted enquiry is stored exactly as submitted, with a reference `ENQ-` plus four digits, the status `new`, the locale `src: Core features`
- [ ] `C-CF-56` `contract` Enquiry references are sequential, well formed, following the seeded ones `src: Core features`
- [ ] `C-CF-57` `ui` Completing the message then submitting shows a toast naming a reference beginning `ENQ-`, the form then clearing `src: Core features`
- [ ] `C-CF-58` `literal` The success toast reads `Thanks, we got your enquiry` or `Grazie, abbiamo ricevuto la tua richiesta` `src: Core features`
- [ ] `C-CF-59` `ui` A refused submission keeps every typed value in the enquiry form `src: Core features`
- [ ] `C-CF-60` `literal` The notification mail reaches the studio inbox alone, with the subject `Enquiry from ` plus the visitor's name `src: Core features`
- [ ] `C-CF-61` `constraint` Each accepted enquiry sends exactly one notification mail, nothing mailed to the visitor `src: Core features`
- [ ] `C-CF-62` `literal` The enquiry limit refuses the eleventh accepted enquiry from one address in an hour, which stores nothing `src: Core features`
- [ ] `C-CF-63` `constraint` An enquiry refused by the limit stores nothing, sends nothing, says when to retry `src: Core features`
- [ ] `C-CF-64` `constraint` The enquiry response sets no cookie `src: Core features`
- [ ] `C-CF-65` `ui` The inbox is a table of stored enquiries with a status control per row `src: Core features`
- [ ] `C-CF-66` `capability` The studio lists every stored enquiry newest first `src: Core features`
- [ ] `C-CF-67` `constraint` The inbox row shows exactly what the visitor submitted, which is the stored enquiry accepted `src: Core features`
- [ ] `C-CF-68` `capability` A status change is stored, surviving a reload of the inbox `src: Core features`
- [ ] `C-CF-69` `constraint` An unknown status is refused, the stored status unchanged `src: Core features`
- [ ] `C-CF-70` `constraint` A stored enquiry cannot be deleted `src: Core features`
- [ ] `C-CF-71` `constraint` A visitor cannot list or read any stored enquiry; no enquiry content reaches a visitor `src: Core features`
- [ ] `C-CF-72` `constraint` An unknown enquiry reference answers as not found `src: Core features`
- [ ] `C-CF-73` `ui` Signing in as the studio lists the walkthrough visitor's enquiry first in the inbox with the status `new` `src: Core features`
- [ ] `C-CF-74` `ui` Marking the enquiry `replied` shows a toast; a reload of the inbox still reads `replied` `src: Core features`
- [ ] `C-CF-75` `capability` The root redirects to the home in the preferred language: `/en` for English, the Italian home otherwise `src: Core features`
- [ ] `C-CF-76` `ui` Choosing the Italian option in the header language switch on `/works` makes the filter pill read `Tutti (20)`, offering `Editoria (5)` `src: Core features`
- [ ] `C-CF-77` `literal` The navigation labels follow the requested locale: `All Works`, `Studio`, `Contact` or `Tutti i progetti`, `Studio`, `Contatti` `src: Core features`
- [ ] `C-CF-78` `contract` Every content read accepts `locale` as the Italian or English code; an unknown locale is refused `src: Core features`
- [ ] `C-CF-79` `capability` The project list serves localised discipline labels in catalogue order `src: Core features`
- [ ] `C-CF-80` `contract` Every public route declares its own title plus description; the English home title is `Studio AVX | Brand & Digital Design Studio based in Italy` `src: Core features`
- [ ] `C-CF-81` `literal` The Italian studio route declares its own title `Studio grafico e di comunicazione a Catania` `src: Core features`
- [ ] `C-CF-82` `constraint` No response sets a cookie before a consent choice `src: Core features`
- [ ] `C-CF-83` `ui` The consent banner offers `Accept` plus `Reject`; choosing reject keeps the banner from returning after a reload `src: Core features`
- [ ] `C-CF-84` `literal` A consent choice writes `cc_cookie`, the consent banner staying away afterwards `src: Core features`
- [ ] `C-CF-85` `ui` The consent banner alone uses a grey palette; the electric blue carries every other surface `src: Core features`
- [ ] `C-CF-86` `constraint` An unknown address answers with the not-found status, such as `/gs` or `/g/d` `src: Core features`
- [ ] `C-CF-87` `ui` The not-found page presents a broken television with darkened corners, static, torn text `src: Core features`
- [ ] `C-CF-88` `literal` The Italian not-found page reads `404`, `Pagina non trovata.`, offering `Torna alla home` back to the home `src: Core features`
- [ ] `C-CF-89` `literal` The English not-found page reads `Page not found.`, offering `Back to home` as the action returning home `src: Core features`
- [ ] `C-CF-90` `capability` Every project image carries alternative text naming the project `src: Core features`
- [ ] `C-CF-91` `constraint` A narrow viewport of 390px shows no sideways overflow on any route `src: Core features`
- [ ] `C-CF-92` `ui` Narrowing the viewport to a phone width collapses the header links behind `MENU`, whose button then reads `× CLOSE` `src: Core features`
- [ ] `C-CF-93` `constraint` Every internal link leads to a route that answers with success `src: Core features`
- [ ] `C-CF-94` `literal` The privacy page carries the controller `Grafiche Meridiane`, `Note legali`, `Ultimo aggiornamento: 15 giugno 2026` `src: Core features`
- [ ] `C-CF-95` `literal` The privacy page carries seven sections: `1. Titolare del trattamento`, `2. Tipologie di dati e finalità`, `3. Modalità del trattamento`, `4. Destinatari dei dati`, `5. Conservazione dei dati`, `6. Diritti dell'interessato`, `7. Cookie Policy` `src: Core features`
- [ ] `C-CF-96` `ui` Opening `/privacy` shows the title `Privacy & Cookie Policy` with the seven numbered section headings `src: Core features`

## C-UF User flow

- [ ] `C-UF-01` `contract` `/` redirects to the home in the preferred language `src: User flow`
- [ ] `C-UF-02` `ui` The Italian plus English home addresses serve the home spatial gallery with the formation switch `src: User flow`
- [ ] `C-UF-03` `contract` `/works` serves the catalogue; the discipline facet narrows the catalogue in order `src: User flow`
- [ ] `C-UF-04` `contract` `/works/<slug>` serves one project with previous plus next; an unknown project slug answers not found `src: User flow`
- [ ] `C-UF-05` `contract` `/studio` serves the studio page, whose content serves eyebrows, the statement, six services `src: User flow`
- [ ] `C-UF-06` `ui` `/contact` serves the enquiry form beside the public address `src: User flow`
- [ ] `C-UF-07` `contract` `/privacy` serves the privacy page, which carries the controller plus seven sections `src: User flow`
- [ ] `C-UF-08` `ui` `/inbox` serves the stored enquiries table with a status per row for the studio `src: User flow`
- [ ] `C-UF-09` `contract` Any other address answers with the not-found status `src: User flow`
- [ ] `C-UF-10` `constraint` Nothing a visitor reads is behind an account, so every internal link on a public route answers success `src: User flow`
- [ ] `C-UF-11` `contract` `/works/` plus `/studio/` redirect permanently to the bare slash forms `src: User flow`
- [ ] `C-UF-12` `capability` The inbox sends a visitor without a session to sign in at `/login`, arriving at `/inbox` afterwards `src: User flow`
- [ ] `C-UF-13` `ui` Opening the site root arrives at a home where the counting boot loader gives way to a live scene of floating project cards `src: User flow`
- [ ] `C-UF-14` `ui` Scrolling the home changes the focused card, the label pill showing a different project title `src: User flow`
- [ ] `C-UF-15` `ui` Choosing Spiral rearranges the cards into a helix; after a reload Spiral is still selected `src: User flow`
- [ ] `C-UF-16` `ui` Opening the Works grid shows twenty project covers with the filter pill reading `All (20)` `src: User flow`
- [ ] `C-UF-17` `ui` Choosing `Packaging (2)` narrows the grid to Etna Wine Cellars plus Sale Marino, then choosing List shows the two as rows `src: User flow`
- [ ] `C-UF-18` `ui` Opening Sale Marino shows the year `2023` with the client Saline di Trapani; choosing next opens Teatro Bellini `src: User flow`
- [ ] `C-UF-19` `ui` A message of five characters is named invalid beside the message field with nothing sent `src: User flow`
- [ ] `C-UF-20` `ui` Completing the message then submitting shows a toast naming a reference beginning `ENQ-`, clearing the form `src: User flow`
- [ ] `C-UF-21` `ui` Signing in as the studio lists the walkthrough enquiry first in the inbox with the status `new`, the exact message shown `src: User flow`
- [ ] `C-UF-22` `ui` Marking the enquiry replied shows a toast; after a reload the status still reads replied `src: User flow`
- [ ] `C-UF-23` `ui` Choosing the Italian option on `/works` makes the filter pill read `Tutti (20)` with `Editoria (5)` offered `src: User flow`
- [ ] `C-UF-24` `ui` Opening an address that is not a route shows the broken television page with `404` plus an action back to the home `src: User flow`
- [ ] `C-UF-25` `ui` The boot loader shows once per visit, counting up before the scene `src: User flow`
- [ ] `C-UF-26` `ui` The enquiry form's sending state keeps every typed value, a refusal keeping the fields filled `src: User flow`
- [ ] `C-UF-27` `ui` An empty inbox table states that no enquiries have arrived rather than showing a blank table `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` One electric ultramarine blue carries the palette with white type across the gallery, the catalogue, the project pages, the studio page `src: UI/UX notes`
- [ ] `C-UX-02` `ui` Pure black appears on the letterbox of the not-found page `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Frosted controls read as a faint dark glass fill with a white hairline over the blue `src: UI/UX notes`
- [ ] `C-UX-04` `ui` The consent banner alone uses a neutral grey scale appearing on no other surface `src: UI/UX notes`
- [ ] `C-UX-05` `ui` The live scene of the home gallery carries white with cyan, green, orange, red accents over very dark greys around the chrome spine `src: UI/UX notes`
- [ ] `C-UX-06` `ui` One variable sans family carries every size on the studio page, from eyebrows to the display word `src: UI/UX notes`
- [ ] `C-UX-07` `literal` Display sizes on the studio page are `165.6px`, `113.85px`, `76px` with tight line heights in one sans family `src: UI/UX notes`
- [ ] `C-UX-08` `literal` Sub-headings sit at `28px`, lead paragraphs at `20px`, body at `16px`, captions at `14px`, labels at `13px`, all in the one sans family of the studio page `src: UI/UX notes`
- [ ] `C-UX-09` `literal` The twelve column grid uses a `58px` margin, a `110px` large margin, spacing steps of `60px`, `80px`, `160px`, carrying the display layout of the studio page `src: UI/UX notes`
- [ ] `C-UX-10` `ui` Headings plus paragraphs rise into place word by word, glyph by glyph `src: UI/UX notes`
- [ ] `C-UX-11` `ui` Rows of catalogue items rise in a staggered wave, one after another `src: UI/UX notes`
- [ ] `C-UX-12` `ui` Large elements settle with a slow expressive ease; controls move with a quick standard ease `src: UI/UX notes`
- [ ] `C-UX-13` `ui` The page transition slides a full panel across between routes rather than cutting `src: UI/UX notes`
- [ ] `C-UX-14` `ui` Under reduced motion every reveal resolves to the end state with the scene calmed, the formation switch still changing the cards `src: UI/UX notes`
- [ ] `C-UX-15` `ui` On the home plus Works the wheel drives the scene rather than scrolling the document `src: UI/UX notes`
- [ ] `C-UX-16` `ui` On the studio page a scroll-scrubbed timeline ties the word reveals to the turning chrome sculpture `src: UI/UX notes`
- [ ] `C-UX-17` `literal` Below `768px` the header collapses behind the MENU button, the formation switch moving to the bottom left `src: UI/UX notes`
- [ ] `C-UX-18` `literal` A second breakpoint at `1024px` separates the tablet band, every route staying within the viewport width at a phone width `src: UI/UX notes`
- [ ] `C-UX-19` `ui` Touch screens drag the scene with a finger without a custom cursor; the phone width header keeps the MENU button `src: UI/UX notes`
- [ ] `C-UX-20` `ui` Keyboard alone reaches the language switch, the view switch, the facets, the filter close control, the enquiry form, each with a visible focus state `src: UI/UX notes`
- [ ] `C-UX-21` `constraint` Body text meets the contrast bar against the background, measured to the WCAG standard for the size of the text `src: UI/UX notes`
- [ ] `C-UX-22` `ui` Icon-only controls carry accessible names reachable by keyboard with a visible focus state `src: UI/UX notes`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The header, cursor, boot loader, transition panel, consent banner persist across routes; one live render context swaps what the home gallery shows `src: Front-end specification`
- [ ] `C-FE-02` `ui` The `AVX` wordmark sits at the left of the header in solid white type over the electric blue palette `src: Front-end specification`
- [ ] `C-FE-03` `ui` Each header link carries a leading dot, the header collapsing behind the MENU button at a phone width `src: Front-end specification`
- [ ] `C-FE-04` `literal` The mobile menu button reads `MENU`, then `× CLOSE` once the menu opens at a phone width `src: Front-end specification`
- [ ] `C-FE-05` `ui` The cursor is a filled dot with a difference blend, absent on touch screens at a phone width `src: Front-end specification`
- [ ] `C-FE-06` `literal` The boot loader counts up from `[0]` before white patches wipe the screen, once per visit `src: Front-end specification`
- [ ] `C-FE-07` `ui` The page transition is a full panel sliding a viewport height across when a project page opens `src: Front-end specification`
- [ ] `C-FE-08` `ui` The north east arrow on the project label pill is inline stroked white geometry on the focused card `src: Front-end specification`
- [ ] `C-FE-09` `ui` Top plus bottom edge gradients fade the blue so gallery cards never collide with the chrome `src: Front-end specification`
- [ ] `C-FE-10` `ui` In `Rings` the cards sit on ring paths in depth; in `Spiral` the same cards wind along one helix `src: Front-end specification`
- [ ] `C-FE-11` `ui` The chrome spine takes a reflective material mirroring a blue gradient environment on the home gallery `src: Front-end specification`
- [ ] `C-FE-12` `ui` The catalogue covers fade in over the darker blue perspective floor once loaded, the view switch at the top centre `src: Front-end specification`
- [ ] `C-FE-13` `ui` The filter pill at the bottom centre of the catalogue opens the facet list with counts `src: Front-end specification`
- [ ] `C-FE-14` `ui` Studio page images wipe open from the bottom edge beside the services list `src: Front-end specification`
- [ ] `C-FE-15` `ui` The not-found tube layers a vignette to black corners, a top sheen, a bowed surface, clearing static `src: Front-end specification`
- [ ] `C-FE-16` `ui` The `404` glyphs split into halves that tear, with a clear action back to the home `src: Front-end specification`
- [ ] `C-FE-17` `constraint` No binary asset is required: covers, gallery images, spine, sculpture, static are drawn by code, every project image still carrying alternative text naming the project `src: Front-end specification`
- [ ] `C-FE-18` `literal` The fallback family stack is `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` for the one sans family of the studio page `src: Front-end specification`
- [ ] `C-FE-19` `capability` Graceful degradation: without WebGL the home shows the flat catalogue `src: Front-end specification`
- [ ] `C-FE-20` `capability` Where WebGL is supported the home draws a live three dimensional canvas `src: Front-end specification`
- [ ] `C-FE-21` `ui` Opening a project from the gallery slides the transition panel to the project page `src: Front-end specification`

## C-TR Technical requirements

- [ ] `C-TR-01` `literal` The frontend is Lit built with Vite; the read surface under `/api` is NestJS, served by the one process where the shell shares the api origin `src: Technical requirements`
- [ ] `C-TR-02` `contract` The server answers `/` with a redirect to the home in the preferred language `src: Technical requirements`
- [ ] `C-TR-03` `contract` The server answers `/works/` plus `/studio/` with permanent redirects to the bare slash forms `src: Technical requirements`
- [ ] `C-TR-04` `contract` The server answers an unknown address with the not-found status, still serving the shell `src: Technical requirements`
- [ ] `C-TR-05` `literal` The datastore is PostgreSQL read from `DATABASE_URL`, holding the seeded projects stored once in catalogue order `src: Technical requirements`
- [ ] `C-TR-06` `literal` Mail is sent over SMTP to `SMTP_HOST`, which is how the notification mail reaches the studio inbox `src: Technical requirements`
- [ ] `C-TR-07` `literal` The app address comes from `APP_PUBLIC_URL` plus `APP_PUBLIC_PORT`, where the shell shares the api origin `src: Technical requirements`
- [ ] `C-TR-08` `constraint` Content is seeded rather than edited: the twenty projects are stored once in catalogue order `src: Technical requirements`
- [ ] `C-TR-09` `constraint` Counts are queries: the footer counts featured plus total projects from stored rows `src: Technical requirements`
- [ ] `C-TR-10` `constraint` Facet counts are computed from stored disciplines at read time `src: Technical requirements`
- [ ] `C-TR-11` `constraint` Passwords are stored hashed for the seeded studio accounts `src: Technical requirements`
- [ ] `C-TR-12` `capability` Anti-abuse: the enquiry limit refuses the eleventh, which stores nothing `src: Technical requirements`
- [ ] `C-TR-13` `constraint` Anti-abuse: a filled decoy field is refused, nothing stored `src: Technical requirements`
- [ ] `C-TR-14` `constraint` No response sets a cookie before a consent choice, the only site cookie being `cc_cookie` `src: Technical requirements`
- [ ] `C-TR-15` `contract` `GET /api/health` returns `200` once ready, the shell sharing the api origin `src: Technical requirements`
- [ ] `C-TR-16` `constraint` No stored credential reaches anything the browser downloads `src: Technical requirements`
- [ ] `C-TR-17` `contract` A validation failure carries field-keyed errors under `errors`, an invalid enquiry refused with nothing stored `src: Technical requirements`

## C-DM Data model

- [ ] `C-DM-01` `literal` The seeded studio accounts use the password `deku-demo-pw-2026`, stored hashed, written to `/app/USER_README.md` `src: Data model`
- [ ] `C-DM-02` `data` `users` holds `email`, `name`, `role`, `password_hash` for the two seeded studio accounts stored once `src: Data model`
- [ ] `C-DM-03` `data` `sessions` holds the token with `retired_at`, so a retired token is refused `src: Data model`
- [ ] `C-DM-04` `literal` `disciplines` holds five keys in facet order: `branding`, `editorial`, `type-design`, `web-design`, `packaging`, from which counts are computed `src: Data model`
- [ ] `C-DM-05` `data` Each discipline carries an Italian plus English label, served as localised labels by the project list `src: Data model`
- [ ] `C-DM-06` `data` `projects` holds `slug`, `title`, `client`, `year`, `featured`, `position` for twenty projects stored once in catalogue order `src: Data model`
- [ ] `C-DM-07` `literal` Projects one to four are `amts-card`, `infectious-diseases`, `avx-alphabet`, `herbert`, stored once in catalogue order `src: Data model`
- [ ] `C-DM-08` `literal` Projects five to eight are `stelvio-grotesk`, `etna-wine-cellars`, `sale-marino`, `teatro-bellini`, each carrying two disciplines in catalogue order `src: Data model`
- [ ] `C-DM-09` `literal` Projects nine to twelve are `ortigia-journal`, `lava-coffee`, `porto-digitale`, `museo-diffuso`, the last of the twelve featured projects the footer counts `src: Data model`
- [ ] `C-DM-10` `literal` Projects thirteen to twenty are `fiera-del-libro`, `agrumi-bio`, `cinema-lumiere`, `atlante-verde`, `kiosk-app`, `scirocco-festival`, `bottega-ceramica`, `marea-hotel`, none featured, so the footer counts twelve of twenty projects `src: Data model`
- [ ] `C-DM-11` `literal` `sale-marino` is Sale Marino, `2023`, client Saline di Trapani, carrying packaging then branding, whose project page wraps previous to `etna-wine-cellars` `src: Data model`
- [ ] `C-DM-12` `data` The first discipline listed for a project leads the localised labels the project list serves, in the order the gallery label pill uses `src: Data model`
- [ ] `C-DM-13` `data` `project_disciplines` holds twenty four rows unique on the project plus discipline pair, from which facet counts are computed `src: Data model`
- [ ] `C-DM-14` `data` `project_media` holds three rows per project, each image carrying alternative text naming the project `src: Data model`
- [ ] `C-DM-15` `data` `studio_services` holds six rows, the studio content serving six services `src: Data model`
- [ ] `C-DM-16` `data` `enquiries` holds `reference` unique, `name`, `email`, `message`, `locale`, `status`, the accepted enquiry stored exactly as submitted `src: Data model`
- [ ] `C-DM-17` `literal` `enquiries` status is `new`, `replied` or `archived`; an unknown status is refused, the stored status unchanged `src: Data model`
- [ ] `C-DM-18` `literal` The seeded enquiries are `ENQ-0001` Anna Rizzo `anna.rizzo@example.com`, `ENQ-0002` Luca Bianchi `luca.bianchi@example.com`, `ENQ-0003` Sofia Greco `sofia.greco@example.com`, stored enquiry rows the studio lists `src: Data model`
- [ ] `C-DM-19` `data` `address_hash` stores a one-way hash of the sender address for the enquiry limit, never the address `src: Data model`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` No content editing interface exists: the twenty projects stay stored once in catalogue order `src: Constraints`
- [ ] `C-CN-02` `constraint` No public signup: the two studio accounts are seeded, stored once `src: Constraints`
- [ ] `C-CN-03` `constraint` No enquiry deletion: a stored enquiry cannot be deleted `src: Constraints`
- [ ] `C-CN-04` `constraint` No third-party script plus no analytics provider, so no response sets a cookie before consent `src: Constraints`
- [ ] `C-CN-05` `constraint` No external network call at runtime: every route answers from the one process where the shell shares the api origin `src: Constraints`
- [ ] `C-CN-06` `constraint` The sign-in page plus `/inbox` are the only non-reference surfaces; the inbox sends a visitor without a session to sign in `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` on the mapping `${APP_PUBLIC_PORT}:4173`, the shell sharing the api origin `src: Deployment contract`
- [ ] `C-DC-02` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the app root `src: Deployment contract`
- [ ] `C-DC-03` `contract` Login credentials are written to `/app/USER_README.md` for the seeded studio accounts stored once `src: Deployment contract`
- [ ] `C-DC-04` `contract` The studio lists every stored enquiry newest first as a top-level JSON array `src: Deployment contract`
- [ ] `C-DC-05` `contract` `POST /api/auth/logout` retires the token, answering `{}` `src: Deployment contract`
- [ ] `C-DC-06` `contract` `GET /api/projects` takes `locale` plus `discipline`, serving the project list in catalogue order with localised labels `src: Deployment contract`
- [ ] `C-DC-07` `contract` `GET /api/projects/{slug}` carries metadata, `media`, `previous`, `next`, wrapping at both ends of the project list `src: Deployment contract`
- [ ] `C-DC-08` `contract` `GET /api/facets` serves `all` first, each facet with `key`, `label`, `count` computed from stored disciplines `src: Deployment contract`
- [ ] `C-DC-09` `contract` `GET /api/studio` serves the studio content: `eyebrows`, `statement`, `intro`, six `services` `src: Deployment contract`
- [ ] `C-DC-10` `contract` `GET /api/global` serves `nav` labels following the requested locale `src: Deployment contract`
- [ ] `C-DC-11` `contract` `POST /api/enquiries` takes `name`, `email`, `message`, `locale`, `company_website`, answering an accepted enquiry with `reference`, `created_at` `src: Deployment contract`
- [ ] `C-DC-12` `contract` `GET /api/enquiries/{reference}` answers an unknown enquiry reference as not found `src: Deployment contract`
- [ ] `C-DC-13` `contract` `PATCH /api/enquiries/{reference}` takes `status`, the status change stored, surviving a reload `src: Deployment contract`
- [ ] `C-DC-14` `constraint` An enquiry held in a module-level array rather than stored is a contract violation; the accepted enquiry must be stored exactly as submitted `src: Deployment contract`
- [ ] `C-DC-15` `constraint` A notification written to the log instead of sent is a contract violation; the notification mail must reach the studio inbox `src: Deployment contract`
- [ ] `C-DC-16` `constraint` A facet count typed into the page is a contract violation; facet counts are computed from stored disciplines `src: Deployment contract`

## Pinned literals

| Value | Meaning | Item | Where |
|---|---|---|---|
| `deku-demo-pw-2026` | value pinned by C-RL-10 | C-RL-10 | User roles |
| `studio@example.com` | value pinned by C-RL-11 | C-RL-11 | User roles |
| `studio2@example.com` | value pinned by C-RL-12 | C-RL-12 | User roles |
| `ENQ-0001` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `new` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `ENQ-0002` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `replied` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `ENQ-0003` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `archived` | value pinned by C-RL-13 | C-RL-13 | User roles |
| `Sign in failed` | value pinned by C-CF-02 | C-CF-02 | Core features |
| `h1` | value pinned by C-CF-17 | C-CF-17 | Core features |
| `AVX - Brand & Digital Design Studio` | value pinned by C-CF-17 | C-CF-17 | Core features |
| `BRAND & DIGITAL DESIGN STUDIO` | value pinned by C-CF-18 | C-CF-18 | Core features |
| `12 / 20` | value pinned by C-CF-18 | C-CF-18 | Core features |
| `selected Works` | value pinned by C-CF-18 | C-CF-18 | Core features |
| `© 2026` | value pinned by C-CF-18 | C-CF-18 | Core features |
| `All` | value pinned by C-CF-26 | C-CF-26 | Core features |
| `Branding` | value pinned by C-CF-26 | C-CF-26 | Core features |
| `Editorial` | value pinned by C-CF-26 | C-CF-26 | Core features |
| `Type Design` | value pinned by C-CF-26 | C-CF-26 | Core features |
| `Web Design` | value pinned by C-CF-26 | C-CF-26 | Core features |
| `Packaging` | value pinned by C-CF-26 | C-CF-26 | Core features |
| `Tutti` | value pinned by C-CF-27 | C-CF-27 | Core features |
| `Editoria` | value pinned by C-CF-27 | C-CF-27 | Core features |
| `All (20)` | value pinned by C-CF-28 | C-CF-28 | Core features |
| `Branding (11)` | value pinned by C-CF-28 | C-CF-28 | Core features |
| `Editorial (5)` | value pinned by C-CF-28 | C-CF-28 | Core features |
| `Type Design (3)` | value pinned by C-CF-28 | C-CF-28 | Core features |
| `Web Design (3)` | value pinned by C-CF-28 | C-CF-28 | Core features |
| `Packaging (2)` | value pinned by C-CF-28 | C-CF-28 | Core features |
| `BASED IN CATANIA / SICILY` | value pinned by C-CF-40 | C-CF-40 | Core features |
| `SINCE 2017` | value pinned by C-CF-40 | C-CF-40 | Core features |
| `BRANDING / DIGITAL / TYPE / PACKAGING` | value pinned by C-CF-40 | C-CF-40 | Core features |
| `WE DON'T JUST DESIGN WE DEFINE ATTITUDES` | value pinned by C-CF-41 | C-CF-41 | Core features |
| `DESIGN EDITORIALE` | value pinned by C-CF-42 | C-CF-42 | Core features |
| `TYPE DESIGN` | value pinned by C-CF-42 | C-CF-42 | Core features |
| `SOCIAL MEDIA DESIGN` | value pinned by C-CF-42 | C-CF-42 | Core features |
| `COPYWRITING E NAMING` | value pinned by C-CF-42 | C-CF-42 | Core features |
| `BRANDING` | value pinned by C-CF-42 | C-CF-42 | Core features |
| `WEB DESIGN` | value pinned by C-CF-42 | C-CF-42 | Core features |
| `EDITORIAL DESIGN` | value pinned by C-CF-43 | C-CF-43 | Core features |
| `Studio AVX - grafica, branding e comunicazione a Catania` | value pinned by C-CF-44 | C-CF-44 | Core features |
| `STUDIO` | value pinned by C-CF-44 | C-CF-44 | Core features |
| `hello@avx-studio.example.com` | value pinned by C-CF-47 | C-CF-47 | Core features |
| `company_website` | value pinned by C-CF-54 | C-CF-54 | Core features |
| `ENQ-` | value pinned by C-CF-55 | C-CF-55 | Core features |
| `Thanks, we got your enquiry` | value pinned by C-CF-58 | C-CF-58 | Core features |
| `Grazie, abbiamo ricevuto la tua richiesta` | value pinned by C-CF-58 | C-CF-58 | Core features |
| `Enquiry from ` | value pinned by C-CF-60 | C-CF-60 | Core features |
| `All Works` | value pinned by C-CF-77 | C-CF-77 | Core features |
| `Studio` | value pinned by C-CF-77 | C-CF-77 | Core features |
| `Contact` | value pinned by C-CF-77 | C-CF-77 | Core features |
| `Tutti i progetti` | value pinned by C-CF-77 | C-CF-77 | Core features |
| `Contatti` | value pinned by C-CF-77 | C-CF-77 | Core features |
| `Studio grafico e di comunicazione a Catania` | value pinned by C-CF-81 | C-CF-81 | Core features |
| `cc_cookie` | value pinned by C-CF-84 | C-CF-84 | Core features |
| `404` | value pinned by C-CF-88 | C-CF-88 | Core features |
| `Pagina non trovata.` | value pinned by C-CF-88 | C-CF-88 | Core features |
| `Torna alla home` | value pinned by C-CF-88 | C-CF-88 | Core features |
| `Page not found.` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `Back to home` | value pinned by C-CF-89 | C-CF-89 | Core features |
| `Grafiche Meridiane` | value pinned by C-CF-94 | C-CF-94 | Core features |
| `Note legali` | value pinned by C-CF-94 | C-CF-94 | Core features |
| `Ultimo aggiornamento: 15 giugno 2026` | value pinned by C-CF-94 | C-CF-94 | Core features |
| `1. Titolare del trattamento` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `2. Tipologie di dati e finalità` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `3. Modalità del trattamento` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `4. Destinatari dei dati` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `5. Conservazione dei dati` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `6. Diritti dell'interessato` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `7. Cookie Policy` | value pinned by C-CF-95 | C-CF-95 | Core features |
| `165.6px` | value pinned by C-UX-07 | C-UX-07 | UI/UX notes |
| `113.85px` | value pinned by C-UX-07 | C-UX-07 | UI/UX notes |
| `76px` | value pinned by C-UX-07 | C-UX-07 | UI/UX notes |
| `28px` | value pinned by C-UX-08 | C-UX-08 | UI/UX notes |
| `20px` | value pinned by C-UX-08 | C-UX-08 | UI/UX notes |
| `16px` | value pinned by C-UX-08 | C-UX-08 | UI/UX notes |
| `14px` | value pinned by C-UX-08 | C-UX-08 | UI/UX notes |
| `13px` | value pinned by C-UX-08 | C-UX-08 | UI/UX notes |
| `58px` | value pinned by C-UX-09 | C-UX-09 | UI/UX notes |
| `110px` | value pinned by C-UX-09 | C-UX-09 | UI/UX notes |
| `60px` | value pinned by C-UX-09 | C-UX-09 | UI/UX notes |
| `80px` | value pinned by C-UX-09 | C-UX-09 | UI/UX notes |
| `160px` | value pinned by C-UX-09 | C-UX-09 | UI/UX notes |
| `768px` | value pinned by C-UX-17 | C-UX-17 | UI/UX notes |
| `1024px` | value pinned by C-UX-18 | C-UX-18 | UI/UX notes |
| `MENU` | value pinned by C-FE-04 | C-FE-04 | Front-end specification |
| `× CLOSE` | value pinned by C-FE-04 | C-FE-04 | Front-end specification |
| `[0]` | value pinned by C-FE-06 | C-FE-06 | Front-end specification |
| `system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif` | value pinned by C-FE-18 | C-FE-18 | Front-end specification |
| `/api` | value pinned by C-TR-01 | C-TR-01 | Technical requirements |
| `DATABASE_URL` | value pinned by C-TR-05 | C-TR-05 | Technical requirements |
| `SMTP_HOST` | value pinned by C-TR-06 | C-TR-06 | Technical requirements |
| `APP_PUBLIC_URL` | value pinned by C-TR-07 | C-TR-07 | Technical requirements |
| `APP_PUBLIC_PORT` | value pinned by C-TR-07 | C-TR-07 | Technical requirements |
| `/app/USER_README.md` | value pinned by C-DM-01 | C-DM-01 | Data model |
| `disciplines` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `branding` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `editorial` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `type-design` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `web-design` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `packaging` | value pinned by C-DM-04 | C-DM-04 | Data model |
| `amts-card` | value pinned by C-DM-07 | C-DM-07 | Data model |
| `infectious-diseases` | value pinned by C-DM-07 | C-DM-07 | Data model |
| `avx-alphabet` | value pinned by C-DM-07 | C-DM-07 | Data model |
| `herbert` | value pinned by C-DM-07 | C-DM-07 | Data model |
| `stelvio-grotesk` | value pinned by C-DM-08 | C-DM-08 | Data model |
| `etna-wine-cellars` | value pinned by C-DM-08 | C-DM-08 | Data model |
| `sale-marino` | value pinned by C-DM-08 | C-DM-08 | Data model |
| `teatro-bellini` | value pinned by C-DM-08 | C-DM-08 | Data model |
| `ortigia-journal` | value pinned by C-DM-09 | C-DM-09 | Data model |
| `lava-coffee` | value pinned by C-DM-09 | C-DM-09 | Data model |
| `porto-digitale` | value pinned by C-DM-09 | C-DM-09 | Data model |
| `museo-diffuso` | value pinned by C-DM-09 | C-DM-09 | Data model |
| `fiera-del-libro` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `agrumi-bio` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `cinema-lumiere` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `atlante-verde` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `kiosk-app` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `scirocco-festival` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `bottega-ceramica` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `marea-hotel` | value pinned by C-DM-10 | C-DM-10 | Data model |
| `2023` | value pinned by C-DM-11 | C-DM-11 | Data model |
| `enquiries` | value pinned by C-DM-17 | C-DM-17 | Data model |
| `anna.rizzo@example.com` | value pinned by C-DM-18 | C-DM-18 | Data model |
| `luca.bianchi@example.com` | value pinned by C-DM-18 | C-DM-18 | Data model |
| `sofia.greco@example.com` | value pinned by C-DM-18 | C-DM-18 | Data model |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 2 | 10 |
| User roles | 2 | 13 |
| Core features | 31 | 96 |
| User flow | 8 | 27 |
| UI/UX notes | 0 | 22 |
| Front-end specification | 2 | 21 |
| Technical requirements | 9 | 17 |
| Data model | 4 | 19 |
| Constraints | 0 | 6 |
| Deployment contract | 9 | 16 |
