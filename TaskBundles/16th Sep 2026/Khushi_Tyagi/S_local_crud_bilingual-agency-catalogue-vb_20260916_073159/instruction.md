# Verso

Build and deploy a working web application from this brief. There is no starting codebase.
When you are done, a stranger must be able to open the app in a browser in French, narrow a
catalogue of the studio's client projects to one discipline and watch the total and the four
counts move together, open a case study, switch that case study to English at a different
address, and finish by sending a qualified enquiry through three addressed steps that lands
as a real row in `postgres` and an acknowledgement on `mailpit`. A visitor holding a link to
a project whose address the studio changed last month must arrive at the project, in one
hop, rather than at a not-found page. The lead, its answers as they were worded when they
were asked, its consent record and the log entry for every privileged read of it must be
real rows that survive a restart; a confirmation the app draws for itself does not count.

## Overview

Verso is a web design studio in Ghent that sells two things: bespoke showcase sites and
online stores. This is the studio's own site, and it does three jobs at once.

It is a catalogue. Every client project the studio has shipped is a record with a discipline
or several, a year, a client, a colour of its own and a case study behind it. A visitor
browses that catalogue as a mosaic of three card sizes, narrows it by discipline, and opens
one project to read the work in detail.

It is bilingual, and not in the cheap way. French is the studio's own language and is served
without a prefix, because it is the default rather than an option. English is served under a
prefix and is separately slugged: the English address for a project is not a translation of
the French one and is never derived from it. A record is two rows joined by a translation
group, and the language switch resolves through that group, so a project published in French
and not yet in English offers an explanation rather than a dead link.

And it is a front door. The contact route offers three ways in -- a project, an application,
or a question -- and each is a short sequence of addressed steps that ends with a reference,
a response-time commitment, and an acknowledgement in the enquirer's mailbox. Behind that,
the studio works from a console nobody outside the studio sees: it writes the records,
publishes them, reads the enquiries and answers them on a clock.

Four audiences arrive and each wants something different. A prospect with a budget wants
evidence of craft and then a way to start a conversation. A prospect browsing wants to be
impressed in under a second. A job candidate wants to know whether the studio is hiring and
to attach a document. And a search engine wants a stable, crawlable set of addresses in two
languages, which is why the address discipline in this brief is as long as it is.

The visible product is a few dozen surfaces. The product's real difficulty is underneath
them, and it is in three places.

The first is that a published address is a promise. The studio renames things: a client
rebrands, a project is re-titled, a case study moves from one discipline to another. Every
address a record has ever carried has to keep resolving, in one hop, in both languages,
forever, and a record cannot leave the published state without the studio deciding whether
its old address is gone or points somewhere.

The second is that the count above a list and the list beneath it are one fact. Four
discipline facets sit above the catalogue, each carrying a live count, and a project carries
more than one discipline, so the four counts sum to more than the total and that is correct.
Computing the counts and the list in two reads at two instants produces a bar whose numbers
do not match the wall beneath it, and it is the most common defect in a product of this
shape.

The third is that an enquiry is a record with obligations attached. It must exist exactly
once however many times a nervous visitor presses send. Its acknowledgement must be
committed with it, so a lead that exists always has one on the way and a lead that does not
never sent one. It must remember the questions as they were worded at the moment they were
asked. It must carry a consent decision. And it must be removable on one action by the
person who sent it, with a certificate naming every place it was removed from.

Two decisions in the shape of the design carry the rest of the risk. The root size of every
page is a fraction of the window's width rather than a fixed number, and which fraction is
used is decided by the window's orientation rather than by its width; every dimension in the
document is a multiple of that root, so the whole page scales as one object. Separately, the
arrangement is chosen by width across five tiers. The two systems agree most of the time and
must never be merged: a phone held sideways takes the landscape scale and the narrow
arrangement. The measured consequence reads as a bug and is not one: a medium landscape
window produces the shortest pages on the whole site, because it renders the wide
arrangement at about two thirds size.

Verso deliberately is not: a native application, a photography host, a font foundry, a
malware scanner, a search vendor, a content delivery network or a mail vendor of its own. It
ships no photograph, no video, no typeface file and no compiled three-dimensional scene, and
it makes no network call at run time except to the mail server this brief names. What would
be a third-party service in a larger product is an in-product component here with the same
observable contract.

## User roles

| Role | Can do | Cannot do |
|---|---|---|
| Anonymous visitor | Read every published project, expertise, person and award in the requested locale, filter the catalogue, open a case study, read the legal notices and the personal-data page, submit an enquiry through any of the three branches, and withdraw an enquiry they sent using the one-action link in their own acknowledgement | **Cannot read any record that is not published, any enquiry, any lead answer, any consent record, any document or any activity entry. Cannot reach any console address** |
| `editor` | Everything a visitor can, plus create, edit, review, schedule, publish, withdraw and re-slug projects, expertise records, people, awards and pages; add, reorder and remove blocks; run a publish preflight; upload media and set a focal point; read the slug history, the redirect list and the revision history of any record | **Cannot read or write a lead, a lead answer, a lead note, a consent record or a candidate document. Cannot read the activity log. Cannot assign or close an enquiry** |
| `commercial` | Everything a visitor can, plus read the lead inbox and any lead in it, read a lead's answers as they were asked, assign a lead to an owner, move a lead through its states, close a lead with a reason, add a note, read a consent record, complete the second assertion that releases a candidate document, and read the activity log | **Cannot create, edit, publish, withdraw or re-slug any record. Cannot add or reorder a block. Cannot upload media. Cannot write or delete an activity entry. Cannot read a candidate document whose scan has not returned clean** |

Authorization is enforced **server-side on every mutating endpoint**, and it is decided in
one place rather than once per handler: a single decision taking the principal, the action
and the subject. Hiding a control is never the protection. A direct API call from an
`editor` session to any `commercial`-only endpoint must be rejected by the server, leaving
the protected state unchanged, and the refusal must carry the same status an absent record
would carry, so the console cannot be used to enumerate what exists. Every list endpoint
filters by permission inside the query rather than filtering a full result afterwards.

Signup is open. Anyone can create an account, and a new account is an `editor` with no
records of its own until the studio grants otherwise. A role is read from the session, never
from the request body.

Four accounts are seeded, every one with the password `deku-demo-pw-2026`:
`editor@example.com` and `editor2@example.com` as editors, `commercial@example.com` and
`commercial2@example.com` as commercial.

## Core features

### Accounts and the console door

Email and password, hashed, with a bearer token returned at login and sent on every
authenticated request. Tokens expire; an expired token leaves the attempted action
unperformed and asks for sign-in again.

1. `POST /api/auth/signup` with `email` and `password` creates an account and returns a
   token. A signup reusing a seeded or existing address is rejected as invalid and creates
   no second account.
2. `POST /api/auth/login` with a seeded address and `deku-demo-pw-2026` returns a bearer
   token. A wrong password is denied and returns no token.
3. Every route under `/api/console/` and every maintenance route requires a bearer token. A
   request without one is denied. The public catalogue routes, the enquiry submission route,
   the withdrawal route, `POST /api/auth/signup`, `POST /api/auth/login` and
   `GET /api/health` do not.
4. The console lives at `/atelier/` and its sign-in at `/atelier/connexion/`. An anonymous
   visitor who requests any console address is sent to the sign-in and returned to the
   address they asked for once signed in. A visitor who asks for nothing in particular lands
   on `/atelier/`.
5. Signing out returns the visitor to `/` and invalidates the token, so the next request
   carrying it is denied rather than served from a cache.

### Two languages, and the addresses that carry them

The site has nine public route shapes and each exists twice. French is the default and is
served without a prefix. English is served under `/en/` and is **separately slugged**: the
English address of a record is chosen by the studio, never derived from the French one.

6. The French shapes are `/`, `/projets/`, `/projets/<slug>/`, `/expertises/`,
   `/expertises/<slug>/`, `/agence/`, `/contact/`, `/mentions-legales/` and
   `/confidentialite/`. The English shapes are `/en/`, `/en/projects/`,
   `/en/projects/<slug>/`, `/en/expertise/`, `/en/expertise/<slug>/`, `/en/agency/`,
   `/en/contact/`, `/en/legal/` and `/en/privacy/`.
7. Every address ends in a trailing slash and is lowercase. A request for a path without the
   trailing slash, or carrying an uppercase letter, answers with a permanent redirect to the
   canonical form rather than serving both. Two addresses that render the same page are two
   addresses a search engine has to choose between, and the product should choose.
8. **The site never redirects on the browser's language header.** A visitor asking for `/`
   gets French whatever their browser prefers, and a visitor asking for `/en/` gets English.
   A header-driven redirect makes a shared link resolve differently for the person who
   shared it and the person who received it, and makes the French site unreachable to most
   of the world.
9. The language switch on any route leads to the same content in the other language. On a
   record it resolves through the record's translation group: `maison-carre` in French is
   `carre-house` in English and the switch leads there. On a route shape with no record it
   leads to the paired shape.
10. When a record has no published translation in the other language the switch is present
    and disabled, and it states why: `Cette page n'existe pas encore en anglais` in French,
    `This page is not available in French yet` in English. It never leads to the other
    language's index instead, and it never silently disappears: a visitor who cannot tell
    whether a translation is missing or the control is broken will assume the latter.
11. The chosen language is remembered on the visitor's own device and is offered on a later
    visit as a suggestion, never as a redirect.
12. Every route declares its own language, and the declaration matches what is rendered. A
    quotation in the other language declares its own.
13. `GET /api/catalogue` takes a `locale` of `fr` or `en` and answers only with records
    published in that locale. A record published in French only is absent from the English
    catalogue rather than present with French text in it.

### The catalogue

The catalogue is the spine of the product: a filterable listing that leads to a detail, and
every other public surface is arranged around it.

14. `/projets/` and `/en/projects/` render every published project in the requested locale as
    a three-tier mosaic. The tiers are **feature**, a large square card; **secondary**, a
    wide card; and **list**, a full-width row carrying a small image. Tier is a property of
    the record, chosen by the studio, not of the card's position in the grid.
15. Above the mosaic sits a total, rendered as `<COUNT> projets` in French and
    `<COUNT> projects` in English, where the count is the number of published projects in
    that locale.
16. Four discipline facets sit above the mosaic: `Direction artistique`, `Experience
    digitale`, `Site vitrine` and `E-commerce` in French; `Art direction`,
    `Digital experience`, `Showcase website` and `E-commerce` in English. Each carries a
    live count of the published projects in that locale carrying that discipline.
17. **A project carries one discipline or several.** The four facet counts therefore sum to
    more than the total, and a reviewer who sees that must not treat it as an error. A
    product that forces one discipline per project loses the only interesting thing about
    the studio's own taxonomy.
18. **The counts and the list are one read.** The four facet counters and the cards beneath
    them are computed together and describe the same instant. A counter maintained
    incrementally drifts the first time a publish is rolled back, so each counter is derived
    from the same query that returns the cards. Two reads at two instants produce a bar
    whose numbers do not match the wall beneath it, which a visitor will notice and a test
    will catch.
19. The filter bar has two modes: `Au moins un filtre` (`Any filter`), where a project
    matching any selected discipline is shown, and `Tous les filtres a la fois`
    (`All filters at once`), where only a project carrying every selected discipline is
    shown. The mode is a control, not a hidden default, and the count reflects it.
20. A clear control reading `Tout effacer` (`Clear all`) removes every selection and is
    present whenever at least one is made.
21. **The whole filter state is the address.** `GET /projets/?discipline=art_direction,commerce&mode=all`
    reproduces exactly what the visitor saw, in a fresh session, on another machine. The
    discipline values are `art_direction`, `digital_experience`, `showcase_site` and
    `commerce`, and the mode values are `any` and `all`. A filter state that lives only in
    the page loses the shared link, the back button and every organic entry point at once.
22. Applying a filter changes the address without a full page load where the browser allows
    it, and reloading that address renders the same set from the server. Both paths produce
    the same result; neither is the privileged one.
23. A combination matching nothing renders the empty panel: the title
    `Aucun projet ne correspond` (`No projects match`), then the body, which reads
    `Aucun projet ne correspond a cette combinaison de filtres. Effacez-en un pour elargir la recherche.`
    in French and `No project matches this combination of filters. Clear one to widen the search.`
    in English, a
    total of zero, and the clear control. It does not render an empty grid with no
    explanation.
24. A locale with no published project at all renders a different panel: `Bientot`
    (`Coming soon`) over `Les projets arrivent. En attendant, parlons du votre.`
    (`The projects are on their way. In the meantime, let us talk about yours.`). An empty
    catalogue and an over-narrow filter are two different situations and telling a visitor
    the wrong one wastes their time.
25. Each card carries the project's title, its client, its year and its disciplines. A card
    reveals its client and disciplines on hover on a pointer device, and **the same
    information is in the card's accessible name and is visible without hover on a touch
    device.** Content that only exists under a mouse does not exist for most visitors.
26. `GET /api/catalogue?locale=fr` returns an object carrying `total`, `facets` and
    `results`, where `facets` is the four disciplines with their counts and each result
    carries `slug`, `title`, `client`, `year`, `tier`, `disciplines` and `ground`. The
    counts in `facets` and the length of a fully-unfiltered `results` describe the same
    read.

### The case study

27. `/projets/<slug>/` renders one project: a hero carrying the title, the client, the year
    and the disciplines, then a sequence of blocks, then a return control.
28. There are eleven block kinds and every one is built: a full-bleed image, a full-bleed
    video, a text block, a two-column text block, a quotation, a grid of images, a
    side-by-side image pair, an inline video, a carousel, a statistics row, and a
    call-to-action. A block is an ordered row in the project, not a field on it.
29. **Spacing between two blocks is decided by the pair of kinds, not by a fixed rule.** Two
    full-bleed blocks in sequence meet with no gap at all; a text block following a
    full-bleed block is separated by the largest gap in the system; two text blocks take the
    ordinary gap. A single spacing value between every block is the most common way a case
    study reads as a form rather than as a composition.
30. A full-bleed image block carries **two crops**, one for the narrow arrangement and one
    for the wide, and the narrow one is not the wide one scaled. A full-bleed image block
    cannot reach the published state with only one.
31. An autoplaying background video block carries a text description of what it shows, and
    cannot reach the published state without one. It is muted, it loops, and under reduced
    motion it renders a single still frame instead.
32. Every content image carries alternative text, or declares itself decorative. A block
    carrying an image with neither blocks publication, and the preflight names the block.
33. An inline video block with no source attached renders its poster with the player
    controls over it and a line saying no source is attached. That is a legitimate empty
    state and is built rather than hidden.
34. The return control leads back to the catalogue **and restores the filters and the scroll
    position the visitor left it in.** Returning to an unfiltered catalogue scrolled to the
    top is the single most irritating defect in a product of this shape, because it punishes
    exactly the visitor who is comparing three projects.
35. The language switch on a case study leads to that case study in the other language or is
    disabled with the explanation rule 10 names. `quai-douze` is published in French only
    and is the case that must explain itself.
36. A carousel is operable from the keyboard: the controls are reachable in the tab order,
    the arrow keys move it, and the current position is announced. A carousel a keyboard
    cannot drive is a block of content that some visitors cannot reach.
37. A statistics row renders figures and their labels, and the figures are stored values
    rather than text typed into a paragraph, so a correction is one edit rather than a
    search.
38. The call-to-action block is the case study's one primary action and leads to the contact
    route in the same locale.

### The home route and the rest of the public site

39. `/` and `/en/` render five bands in order: a hero carrying the wordmark and the studio's
    standfirst, a pinned sequence, a horizontal feature rail of the projects the studio has
    chosen to lead with, a column of catalogue cards, and an award panel.
40. The hero's first line is `<BRAND>, agence web creative a <CITY>` in French and
    `<BRAND>, creative web agency in <CITY>` in English, and it is the route's only
    first-level heading. The wordmark beside it is drawn geometry rather than text, so a
    visually hidden heading carries the real title.
41. The pinned sequence holds its place while the visitor scrolls through it and releases
    when it ends. **Adding a fourth featured project lengthens it** rather than compressing
    its contents, because a sequence whose length is a fixed number silently clips its own
    content the moment the studio adds work.
42. The pinned sequence needs a minimum window height. In a short landscape window it
    unpins and renders as ordinary stacked sections, which is the same behaviour reduced
    motion produces. A pinned sequence that clips itself with no way to reach the clipped
    part is worse than no sequence.
43. If the sequence cannot keep up on a visitor's machine it gives up gracefully and becomes
    stacked sections rather than stuttering. That path is a real feature and is built, not a
    fallback nobody exercises: the visitor who needs it is the visitor least likely to
    report it.
44. The feature rail scrolls horizontally as the visitor scrolls down. It is reachable from
    the keyboard, focus advances it, and its reading order is linear. Below the narrow width
    it is a vertical stack.
45. The award panel names two award bodies, `Webframe` and `DDA`, each with a count, and
    three fixed row titles that are the same in both locales: `Site Of The Month`,
    `Site Of The Day` and `Developer Award`. The panel's stage renders a poster composition;
    the three-dimensional scene layer is declared absent and the composition is the shipped
    state rather than a placeholder for it.
46. `/expertises/` and `/en/expertise/` render the studio's five services --
    `Strategie et conseil`, `Direction artistique`, `Site e-commerce`, `Site vitrine` and
    `Experience digitale` in French -- each with its list of skills, and a row of large
    letter tiles that are drawn geometry rather than typed text. **Every service that links
    to a detail carries a visible resting affordance saying so**, because a page where some
    items are links and some are not, with no difference until the pointer arrives, is a
    page a keyboard visitor cannot navigate.
47. `/agence/` and `/en/agency/` render the studio's story, a marquee of three words
    (`creatif`, `passionne`, `independant` in French), the team, the awards and the clients.
48. `/contact/` and `/en/contact/` render three entry cards -- `Un projet` (`A project`),
    `Candidature` (`Application`) and `En savoir plus` (`Find out more`) -- each leading to
    its own branch of the funnel. An entry whose branch is closed renders `Cette voie est
    fermee pour le moment. Ecrivez-nous a contact@example.com.` rather than a control that
    leads nowhere.
49. The footer is on every public route and carries the studio's address --
    `12 Kaai Verbeke`, `9000` `Ghent`, `Belgium` -- the two mail addresses
    `contact@example.com` and `jobs@example.com`, the phone number `04 82 33 85 10`
    **rendered once**, four social links, the legal notices and the personal-data page. The
    copyright year is computed rather than typed, so it cannot go stale.

### Records, review and publishing

50. A record is a **translation group** holding one row per locale. Creating a project
    creates the group and the French row; adding English adds a row to the same group. The
    group is what the language switch resolves through and what a publish acts on per
    locale.
51. A record moves through `draft`, `in_review`, `scheduled`, `published` and `withdrawn`.
    The transitions are draft to in review, in review back to draft or on to scheduled or
    published, scheduled to published or back to draft, and published to withdrawn. Any
    other transition is refused and the record is left as it was.
52. `POST /api/console/projects/{id}/preflight` returns **every** unmet obligation, not the
    first. The obligations are: a title, a slug, a client, a year, at least one discipline, a
    tier, at least one block, both crops on every full-bleed image block, a description on
    every autoplaying video block, and alternative text or a decorative declaration on every
    content image. A preflight that stops at the first failure makes publishing a sequence of
    attempts rather than one decision.
53. `POST /api/console/projects/{id}/publish` refuses when the preflight is not clean, and
    the refusal names the same obligations. The seeded `lune-basse` sits in draft with a
    full-bleed image missing its narrow crop and a content image missing alternative text,
    so a first publish attempt on it names two unmet obligations.
54. **A publish is one transaction** across the state change, the slug history entry, any
    redirect the change implies, the revision and the invalidation of the cached catalogue.
    A publish that is rolled back leaves no redirect, no revision and no changed count. Half
    a publish is worse than none, because the parts that landed look like the truth.
55. Publishing one project rebuilds that project's route, the catalogue, the four counts and
    the sitemap. It does not rebuild the whole site. A publish that invalidates everything is
    a publish the studio stops doing.
56. A publish writes a revision carrying who published, when, and the record as it then
    was. The revision list is readable and a revision is restorable into draft.
57. A scheduled publish that fails stays scheduled, raises an alert and is retried. It does
    not silently become published and does not silently become a draft.
58. `POST /api/console/projects` creates a project through three addressed steps at
    `/atelier/projets/nouveau/1/`, `/atelier/projets/nouveau/2/` and
    `/atelier/projets/nouveau/3/` -- identity, disciplines and tier, then the first block.
    Each step is its own address, is reachable by its own link, and carries a `Etape <N> sur
    <TOTAL>` indicator. Leaving at step two and returning finds the answers from step one.
59. A project's blocks are ordered, and reordering one moves it in the list **before the
    server answers**, reconciling when it does. A reorder the server refuses returns the row
    to where it was and says why, rather than leaving the list showing an order the database
    does not hold.
60. Rank is rebalanced across the list rather than stored as a dense integer per row, so
    inserting a block between two others does not rewrite the whole project.
61. Two editors holding the same record are not allowed to overwrite each other silently:
    the second write is refused, names the editor who changed it, and re-renders with the
    current state. A record open for editing carries a lock that warns at `2 minutes`
    remaining and is extendable.

### Addresses that survive

62. Changing a published project's slug **automatically** writes a permanent redirect from
    the old path to the new one. The studio is not asked to remember; a redirect somebody
    has to remember to create is a redirect that does not exist.
63. Slug history is per locale. Renaming the French slug does not touch the English address
    and does not create a redirect in the English tree.
64. A redirect chain is served in **one hop**. If `a` became `b` and `b` became `c`, then
    `a` answers with a permanent redirect straight to `c`, never to `b`. The seeded
    `port-neuf` already carries one superseded French path, so a chain exists before the
    studio does anything.
65. Withdrawing a published record cannot complete without choosing one of two outcomes.
    Either the address is **gone**, answering with the gone status over the copy
    `Cette page a ete retiree volontairement.` in French and
    `This page was deliberately withdrawn.` in English; or the address **redirects**, and the
    studio names the target. A withdrawn record whose address answers not-found loses every
    link anybody ever made to it.
66. A redirect target is either a path beginning with a single slash, or an address on a
    configured allow-list. Anything else is rejected **at write time by the console and
    again at serve time by the router**. An editable list of places to send visitors is an
    open redirect with an administration interface unless both checks exist.
67. `GET /api/console/redirects` lists every redirect with its source, its target, its
    status and whether it was written automatically or by hand. A redirect the studio cannot
    see is a redirect the studio cannot fix.
68. A sitemap at `/plan-du-site/` and `/en/sitemap/` lists every published address in that
    locale, and every internal link on every public route resolves.

### The enquiry funnel

The contact route promises a procedure and then delivers one. Three branches, each a short
sequence of addressed steps, each ending in a record the studio can answer.

69. The project branch runs at `/contact/projet/1/`, `/contact/projet/2/` and
    `/contact/projet/3/` -- what you want to build, when and at what scale, and who you are.
    The application branch runs at `/contact/candidature/1/` and `/contact/candidature/2/`.
    The question branch is a single step at `/contact/question/1/`. Each step is its own
    address and the back control moves between them without losing an answer.
70. Every step shows `Etape <N> sur <TOTAL>`, and the controls read `Retour` (`Back`),
    `Continuer` (`Continue`) and, on the last step, `Envoyer` (`Send`). While a submission is
    in flight the control reads `Envoi en cours` (`Sending`) and cannot be pressed twice.
71. The draft is held on the visitor's own device and survives a reload, a closed tab and a
    refused submit. A visitor who typed four paragraphs and lost them to a network blip does
    not type them again.
72. Validation names the field and says what is wrong, inline, next to it, and a summary at
    the top of the step reads `Il reste <COUNT> chose(s) a corriger.` A missing required
    answer reads `Cette reponse est necessaire pour continuer.`; a malformed address reads
    `Verifiez l'adresse : il manque quelque chose apres l'arobase.`; a too-short answer reads
    `Un peu plus long, s'il vous plait : au moins <COUNT> caracteres.` A form that rejects
    input without naming the field is a form people abandon.
73. A rejected step **writes nothing**. There is no partial lead and no orphan answer row.
74. The budget question offers `Je ne sais pas encore` (`Not sure yet`) as a real answer
    rather than forcing a number. A required field a prospect cannot honestly answer is a
    field that loses the prospect.
75. The last step carries a consent statement, which reads
    `J'accepte que Verso conserve ces informations pour repondre a ma demande.`
    It is not pre-selected, and the submission is refused without it.
76. `POST /api/enquiries` carries an `Idempotency-Key`. **Submitting twice, or retrying
    after a timeout, produces exactly one lead**, and the arbitration is the database's
    rather than a check the application performs before writing. Two submissions four
    milliseconds apart leave one row; the second caller receives the same reference as the
    first, not a conflict.
77. **The acknowledgement is committed in the same transaction as the lead.** A lead that
    exists always has an acknowledgement on its way, and a lead that was rolled back never
    sent one. It is sent over SMTP to the mail server this brief names, at the host and port
    read from the environment.
78. The acknowledgement is addressed to **exactly the one address typed on the last step of
    the funnel, with no carbon copy and no blind carbon copy.** A studio mailbox on the
    copy line turns every acknowledgement into a second inbox nobody reads and leaks one
    enquirer's address to the next.
79. The subject **begins with a fixed phrase, then a space, a colon, a space and the
    reference.** For the project and question branches the phrase is `Nous avons bien recu
    votre demande`, so a worked example is `Nous avons bien recu votre demande : VRS-2K4F7A`.
    For the application branch the phrase is `Votre candidature est bien arrivee`, so a
    worked example is `Votre candidature est bien arrivee : VRS-9H3D1B`. A reference is
    `VRS-` followed by six uppercase letters and digits.
80. The body is never empty and names the studio by name. It names four things and no more:
    the reference, the response-time commitment, how long the studio keeps the information,
    and a one-action withdrawal link. **No acknowledgement quotes the submitted payload
    back**, because a mailbox is not a place to put somebody's answers.
81. **Only two events send mail to an enquirer: a submission, and an application outcome.**
    Moving a lead to `routed`, `acknowledged`, `in_progress`, `answered` or `closed` sends
    nothing at all. A studio that mails somebody every time a row changes state teaches them
    to filter the studio out.
82. A successful submission lands on `/contact/merci/<ref>/`, which renders `C'est envoye`
    (`Sent`) over `Reference <REF>. Nous repondons sous <SLA>. Un accuse de reception part
    vers <EMAIL>.` The reference is the visitor's handle on the enquiry and is what a
    follow-up call quotes.
83. A submission the server refuses renders
    `Nous n'avons pas pu enregistrer votre demande. Vos reponses sont conservees. Reessayez.`
    and keeps every answer. A retry uses the same idempotency key, so a retry that succeeds
    after a timeout still produces one lead.
84. A submission judged to be automated is refused **and receives the same status, the same
    body and the same confirmation as any other**. Telling a sender that their message was
    classified as spam teaches whoever is probing exactly what to change.
85. The funnel records the questions **as they were worded at submission**. Re-wording a step
    next year does not rewrite what somebody was asked this year, and the lead detail view
    renders the stored wording rather than the current set.

### The lead inbox

86. `/atelier/demandes/` renders every lead as a table: reference, branch, name, subject,
    state, owner, and time left against the response-time commitment. It is a working
    surface, so the columns that decide what to do next are the ones that sort.
87. A lead moves through `new`, `routed`, `acknowledged`, `in_progress`, `answered`,
    `closed` and `withdrawn`. A state change updates the row **before the server answers**
    and reconciles when it does; a refused change returns the row to its previous state and
    says why.
88. Every lead is routed to an owner or appears in an unrouted queue. **There is no third
    place for a lead to be.** A lead that is neither assigned nor visibly unassigned is a
    lead nobody answers.
89. Closing a lead requires a reason and refuses without one. A closed lead with no reason is
    a lead nobody can learn from.
90. `/atelier/demandes/<id>/` renders the lead's answers using the question wording stored
    with them, the consent record, the acknowledgement's delivery state, and the notes the
    studio has added. It never renders a lead's text as markup, anywhere, including in mail.
91. The response-time clock respects the studio's working hours: an enquiry arriving on a
    Saturday evening is not overdue on Sunday morning.
92. `GET /api/console/leads` is readable by `commercial` and refused to `editor`, and the
    refusal carries the status an absent record would carry. The list filters by permission
    inside the query rather than filtering a full result afterwards.
93. The lead list, the media list and the record list each answer in **one query regardless
    of how many rows they return**. A list that asks the database one question per row works
    at ten rows and falls over at a thousand, and it is the most common way a console dies.
94. Console list filters live in the address exactly as the public catalogue's do, so a
    studio member can send a colleague a link to the six overdue leads rather than describing
    how to reach them.
95. A delimited export of leads neutralises a leading character that a spreadsheet would read
    as a formula. An export is the one action that takes personal information out of
    everything protecting it.

### Applications and candidate documents

96. The application branch accepts one document per application. The document is stored under
    a **server-generated identifier**; the name it arrived with is metadata and is never part
    of the key. A filename is a message from a stranger.
97. An upload whose declared type and actual first bytes disagree is rejected.
98. A document enters the `pending_scan` state and is **unreachable until its scan returns
    clean**. The check is made where the bytes are read, not by hiding the download control.
    The seeded application carries a document still in `pending_scan`, so the boundary has a
    case on the first page load.
99. A document whose scan rejects it is retained in the rejected state with the reason, and
    the application remains readable without it.
100. Downloading a clean document requires a second assertion from the signed-in
    `commercial`, and **the log entry is written before the download target is issued**. A
    log written afterwards is a log that misses exactly the download that failed halfway.
101. `GET /api/console/documents/{id}/download` is refused to `editor`, refused to an
    unauthenticated caller, and refused for a document that is not clean, each with the same
    status.
102. An application's outcome is recorded and the candidate is written to, with a subject
    beginning `Suite a votre candidature` followed by a space, a colon, a space and the
    reference, in **both** the positive and the negative case: a worked example is
    `Suite a votre candidature : VRS-9H3D1B`. The two outcomes share a subject on purpose,
    because a subject line that reveals the answer is read in a corridor. A candidate who
    hears nothing at all is the most common complaint about a studio's hiring.

### Consent, retention and the record of who did what

103. Nothing non-essential is written to a visitor's device before a consent decision. The
     panel asks once, and **refusing takes the same number of actions as accepting, on the
     same surface**. A refusal buried one level deeper than an acceptance is not a choice.
104. The consent decision survives a reload and is recorded on the server alongside the lead
     it applies to, so the studio can show what was agreed and when.
105. `/retrait/<token>/` and `/en/withdraw/<token>/` complete a withdrawal in **one action**
     from the link in the acknowledgement. It asks for confirmation and nothing else: no
     account, no sign-in, no form.
106. A withdrawal deletes the **derived copies before the primary record** and verifies each
     absence afterwards. Deleting the record first leaves copies with nothing pointing at
     them, which is how a store gets forgotten.
107. A completed withdrawal issues a **certificate naming every store** the record was
     removed from. A certificate that says "deleted" and names nothing is a claim, not
     evidence.
108. A withdrawn lead is gone from the inbox and from every export, and its reference no
     longer resolves.
109. The retention job removes leads past their retention period on the same rule, and a
     restore of a backup runs retention **before the environment is reachable**. A backup
     restored after an erasure quietly un-deletes somebody the studio certified as gone.
110. Every privileged read -- a lead opened, a document released, an export taken, a record
     published -- writes an activity entry naming who, what, which record and when. The
     entries are **append-only: no update and no delete reaches them**, and the restriction
     is at the database grant rather than in the application, because an application-level
     rule protects nothing from the next handler somebody writes.
111. `/atelier/journal/` renders the activity log to `commercial` and refuses it to `editor`.
     It is readable, filterable by actor and record, and is the answer to who did what to
     which record when.

### The console shell

112. The console's primary way to reach anything is a **command palette**. It has its own
     address at `/atelier/palette/`, opens over any console route, and takes a typed query
     that matches records by title and slug, leads by reference and name, and the console's
     own destinations by name.
113. Every console destination is reachable from the palette by typing, and the palette is
     reachable from every console route. A palette that is the fast path for some surfaces
     and the only path for none is decoration.
114. `POST /api/console/search` answers the palette. When the search component is
     unavailable the console falls back to a plain listing **and says so** rather than
     rendering an empty result that reads as "there is nothing".
115. The console's record lists and the lead inbox are tables. Rows sit tight enough that a
     working queue fits one screen, numbers align in a column, and the column that decides
     what to do next is the one that sorts by default.
116. `/atelier/` renders what needs attention: records awaiting review, scheduled publishes
     due, leads past their commitment, and documents awaiting a scan.
117. The console is one locale. It is the studio's tool, not a public surface, and doubling
     it would double the translation work for an audience of five.

### Error routes, titles and the crawl surface

118. An unknown address renders the studio's own not-found page, **answers with the
     not-found status**, and offers a way back: the heading `404` over the body, which reads
     `Cette page n'existe pas, ou plus. Voici trois choses qui existent.`
     in French and `This page does not exist, or no longer does. Here are three that do.` in
     English, and three links that resolve. A not-found page that answers with a success
     status tells a search engine the page exists.
119. A `404` on an English path answers in English; a `404` on a French path answers in
     French. The error route inherits the locale of the address that produced it.
120. A withdrawn-as-gone address answers with the gone status and the copy rule 65 names. A
     server failure renders `Quelque chose a casse de notre cote. Nous sommes prevenus.`
     (`Something broke on our side. We have been told.`) and a refused rate renders
     `Un peu trop de demandes. Reessayez dans <SECONDS> secondes.`
121. **Every public route carries its own title and its own description, and no two routes
     share either.** The home route's French title is
     `Agence web Ghent : creation de site internet et design graphique`; the catalogue's is
     `Decouvrez l'ensemble des projets digitaux de l'agence Verso`; the contact route's is
     `Contactez Verso, agence web a Ghent`. A site where forty pages share one title is forty
     pages a search engine treats as one.
122. Every public route declares one canonical address, and the other locale's address is
     declared as the alternate for that language.
123. `/confidentialite/` and `/en/privacy/` state what the studio records about a visitor and
     about an enquirer, how long it keeps it, and how to have it removed. The page is
     reachable from the footer of **every** page, including the error routes.

### Console sessions, access and notification

124. A console session carries a cookie marked http-only, secure, same-site lax, host-only
     and scoped to the root path. A session holds an idle lifetime and a separate absolute
     lifetime, and the identifier is reissued on any privilege change and on every
     re-authentication, so a stolen identifier stops being useful the moment the account it
     belongs to changes shape.
125. A record open for editing holds an edit lock whose duration renews on every save and on
     every heartbeat from the surface that holds it. A lock that expires releases the record
     rather than stranding it.
126. Sorting is a first-class part of every console list: the deciding column sorts by
     default, any column the studio works from sorts on request, and the sort lives in the
     address beside the filters.
127. The console carries an in-console notification feed. Three events reach it: a console
     invitation, naming the invitee; a session revoked elsewhere, naming the person an owner
     revoked; and a lead breaching its commitment. Each is delivered immediately. A person
     may set a digest to immediate, hourly or daily for every batched class, and the choice
     is theirs rather than the studio's.
128. The console dashboard is the reporting surface: the queue of what needs attention, plus
     a weekly batched summary mailed to the studio. It is the one place a person sees the
     whole state of the studio's work without opening a list.
129. Managing integrations and secrets is a permission held by nobody in this build. Rotating
     or revealing an integration secret is recorded as an activity entry the moment either
     happens, and rotation is supported without a deploy, with an overlap window during
     which both the previous secret and the new one are accepted. A secret that can only be
     rotated by a deploy is a secret nobody rotates.
130. Roles are an enumerated set, and the permission matrix binding a role to an action is
     held in one place in the code, reviewable as a single diff. A permission scattered
     across handlers is a permission nobody can audit, which matters because an external
     auditor requiring a queryable trail of who could have seen a candidate's document needs
     an answer that does not depend on reading every route.

### Lead scoring, routing and the application fields

131. Every lead carries a score computed at submission from named signals. A mail domain
     belonging to a free consumer provider lowers it. A spam verdict of suspect lowers it
     considerably. A named company, a stated budget and a described project raise it. The
     score is a routing input, never a reason to refuse an enquiry.
132. Routing sends a scored lead to an owner by branch and by availability, or to the
     unrouted queue when no owner matches. Routing is re-run when an owner changes, so a
     lead never belongs to somebody who has left.
133. The application branch collects a role, a few words, an optional document, an
     availability chosen from an enumerated set, and a location as free text. Only one
     portable document format is accepted, and an upload in any other format is refused at
     the step rather than after the send.
134. Validation runs twice and differently: on leaving a field, the format of what was typed
     is checked; on submitting a step, the completeness of the step is checked. Checking
     completeness on every keystroke tells somebody their answer is wrong before they have
     finished writing it.
135. A submission whose score is raised enough to be suspect is asked to complete a
     privacy-preserving proof of work rather than a puzzle. The challenge is invoked only on
     a raised score, never on every sender, because a challenge everybody sees is a tax on
     the honest.

### Maintenance, integrations and the crawl surface

136. Four maintenance operations exist, each reachable through the maintenance endpoint and
     each safe to execute twice: running retention, rotating the analytics salt, pruning
     superseded revisions, and pruning read notifications. Execution of any of them records
     its attempt count, its idempotency key and its outcome, so a repeated execution is
     visible as one effect rather than two. In a larger deployment each would
     be a nightly or daily cron; here each is an operation the studio can run, and the
     absence of a cron changes nothing about what each does.
137. Work that leaves the request runs through a durable, at-least-once queue. A failure is
     retried with exponential backoff and jitter rather than at a fixed interval, so a
     recovering service is not struck by every retry at once. A dead letter arrival is
     surfaced, batched hourly, and never silently dropped.
138. An outbound event carries a schema version field. A consumer on an older version renders
     what it can understand and ignores the rest rather than failing, which is what makes a
     version bump a safe act rather than a coordinated deploy.
139. Some paths exist for machines rather than for people. The sitemap, the robots file and
     the catalogue feed are unlinked from the site's own navigation and are reachable by
     address alone; each is a machine-only path, and each is listed so nothing about the
     crawl surface is accidental.
140. The legal notices and the personal-data page each carry a structured web-page
     description naming a modification date, so a reader can tell when the studio last
     changed what it promises.
141. Access to a candidate document is a step-up: the mechanism is a second assertion by the
     already-signed-in account, not a second account. Deletion of a document removes the
     stored bytes, every rendition derived from them, and the usage rows pointing at them,
     in that order.

### Copy the product says

142. The overlay navigation's close control reads `Fermer` in French, `Close` in English.
143. The contact route's instruction line reads `Suivez calmement la procedure.` in French,
     `Follow the procedure calmly.` in English. The third entry card's body reads
     `Presse, partenariat, ou simplement une question.` in French,
     `Press, partnership, or simply a question.` in English.
144. The catalogue's standfirst reads, in French, `Chaque projet priorise l'excellence dans
     le but de plonger vos visiteurs dans un univers puissant et percutant. Nous croyons que
     rien ne vaut une experience immersive, et surtout une experience bien a vous.` The
     English reads `Every project puts excellence first, to immerse your visitors in a world
     that is powerful and striking. We believe nothing beats an immersive experience, and
     above all an experience that is genuinely yours.`
145. The art-direction service lists its skills as `Identite visuelle / Logo / Charte
     graphique / Design graphique / Maquettes et prototypes / UI et UX design` in French,
     and `Visual identity / Logo / Graphic charter / Graphic design / Mockups and prototypes
     / UI and UX design` in English.
146. A console invitation is subject `Votre acces a l'atelier Verso` in French,
     `Your access to the Verso workroom` in English.
147. An offline surface exists for a visitor whose connection has gone: `Hors ligne`
     (`Offline`) over a line offering the pages already on their device.
148. Copy conventions hold across the whole deck: sentence case in body copy in both
     locales, uppercase applied by the type style rather than typed into a string, plain
     ASCII punctuation only, and no typographic dashes anywhere. A dash typed as a
     typographic character is a dash that breaks in one of the two locales.
149. The legal notices ship as **marked placeholder text**, not as legal advice. Four clause
     groups are present in outline -- identification, terms of use, intellectual property
     and liability -- and the intellectual-property clause is the one whose source was
     truncated mid-sentence at `de modifier, copier, reproduire, telecharg`, completed here
     to name diffuser, transmettre and exploiter commercialement so the page reads as a
     sentence. Every clause is marked for replacement by the studio's own wording before
     publication.

## User flow

| Route | Purpose | Auth |
|---|---|---|
| `/` | Home in French: hero, pinned sequence, feature rail, catalogue column, award panel | Public |
| `/en/` | Home in English | Public |
| `/projets/` | The catalogue in French: three-tier mosaic, total, four facet counts, filter modes | Public |
| `/en/projects/` | The catalogue in English | Public |
| `/projets/<slug>/` | One case study in French: hero, blocks, return control | Public |
| `/en/projects/<slug>/` | One case study in English, under its own slug | Public |
| `/expertises/` | The five services, their skills and the letter tiles, in French | Public |
| `/en/expertise/` | The same in English | Public |
| `/expertises/<slug>/` | One service in detail, in French | Public |
| `/en/expertise/<slug>/` | One service in detail, in English | Public |
| `/agence/` | The studio: story, marquee, team, awards, clients, in French | Public |
| `/en/agency/` | The same in English | Public |
| `/contact/` | The three entry cards, in French | Public |
| `/en/contact/` | The three entry cards, in English | Public |
| `/contact/projet/1/` `/2/` `/3/` | The project branch of the funnel, one step per address | Public |
| `/contact/candidature/1/` `/2/` | The application branch, one step per address | Public |
| `/contact/question/1/` | The question branch, a single step | Public |
| `/contact/merci/<ref>/` | The confirmation: reference, commitment, acknowledgement destination | Public |
| `/en/contact/project/1/` `/2/` `/3/` | The project branch in English | Public |
| `/en/contact/application/1/` `/2/` | The application branch in English | Public |
| `/en/contact/question/1/` | The question branch in English | Public |
| `/en/contact/thanks/<ref>/` | The confirmation in English | Public |
| `/retrait/<token>/` | One-action withdrawal from the acknowledgement link, in French | Public, token |
| `/en/withdraw/<token>/` | The same in English | Public, token |
| `/mentions-legales/` | The legal notices in French | Public |
| `/en/legal/` | The legal notices in English | Public |
| `/confidentialite/` | What the studio records, keeps and removes, in French | Public |
| `/en/privacy/` | The same in English | Public |
| `/plan-du-site/` | Every published French address | Public |
| `/en/sitemap/` | Every published English address | Public |
| `/atelier/connexion/` | Console sign-in | Public |
| `/atelier/` | Console home: what needs attention | `editor` or `commercial` |
| `/atelier/palette/` | The command palette as its own address | `editor` or `commercial` |
| `/atelier/projets/` | The project table | `editor` |
| `/atelier/projets/nouveau/1/` `/2/` `/3/` | Creating a project, one step per address | `editor` |
| `/atelier/projets/<id>/` | One record: fields, state, preflight, publish | `editor` |
| `/atelier/projets/<id>/blocs/` | The block list, ordered and reorderable | `editor` |
| `/atelier/expertises/` | The expertise table | `editor` |
| `/atelier/redirections/` | Every redirect, its source, target, status and origin | `editor` |
| `/atelier/demandes/` | The lead inbox | `commercial` |
| `/atelier/demandes/<id>/` | One lead: answers as asked, consent, acknowledgement, notes | `commercial` |
| `/atelier/documents/<id>/` | One candidate document, its scan state and its release | `commercial` |
| `/atelier/journal/` | The activity log | `commercial` |

**Entry and redirects.** An anonymous visitor requesting any `/atelier/` address is sent to
`/atelier/connexion/` and, once signed in, is returned to the address they asked for; a
sign-in that was not preceded by a request lands on `/atelier/`. Signing out returns to `/`
and invalidates the token, so a request carrying it afterwards is denied. A token that
expires part-way through an action leaves the action unperformed, keeps nothing half-written,
and asks for sign-in again. An `editor` requesting `/atelier/demandes/`, a lead, a document or
the activity log is refused by the server with the same status an absent record would carry,
and a `commercial` attempting to publish, re-slug or add a block is refused the same way. A
path missing its trailing slash, or carrying an uppercase letter, answers with a permanent
redirect to the canonical form. A path that a record used to occupy answers with a permanent
redirect to the address that record occupies now, in one hop. The browser's language header
changes nothing.

**Journeys.**

1. **Browse to brief.** Open `/`. Follow the primary action to `/projets/`. Read the total
   and the four counts. Select `Direction artistique` and watch the total fall and the four
   counts change in the same repaint. Switch the mode to `Tous les filtres a la fois` and add
   `E-commerce`; the mosaic narrows to `serre-verte`. Open it, read the case study, and note
   that the return control brings back the same two filters and the same scroll position.
   Open `atelier-brune` instead, follow its call-to-action to `/contact/`, choose `Un projet`,
   answer the three steps at `/contact/projet/1/`, `/2/` and `/3/`, accept the consent
   statement, and press `Envoyer`. Land on `/contact/merci/<ref>/` carrying a reference.
   Observable: one lead row in `postgres`, its answers stored with the question wording used
   on the step, one consent record, and one acknowledgement on the mail server addressed to
   the address that was typed.
2. **Publish a case study.** Sign in at `/atelier/connexion/` as `editor@example.com`. Open
   the palette, type the name of a new project and create it through
   `/atelier/projets/nouveau/1/`, `/2/` and `/3/`. Add blocks at
   `/atelier/projets/<id>/blocs/`, including a full-bleed image with only its wide crop. Press
   publish: the preflight refuses and names the missing narrow crop together with every other
   unmet obligation in one answer. Supply it, publish, and see the record move to `published`
   with a revision written. Open `/projets/` in a fresh session: the total has risen by one,
   and each discipline the project carries has risen by one.
3. **Rename without losing a visitor.** As `editor@example.com`, open `/atelier/projets/` and
   change the French slug of `port-neuf`. Request `/projets/port-neuf/`: it answers with a
   permanent redirect straight to the new address, in one hop, and `/en/projects/new-harbour/`
   is untouched. Open `/atelier/redirections/` and find the redirect listed as automatic.
   Observable: the old path resolves, the English path is unchanged, and the redirect row
   exists in `postgres`.
4. **Apply for a job.** Open `/contact/`, choose `Candidature`, answer
   `/contact/candidature/1/` and `/2/`, attach a document, consent and send. Sign in as
   `commercial@example.com`, open `/atelier/demandes/`, and find the application as a lead in
   the `new` state. Open it: the document is listed, its state is `pending_scan`, and the
   download is refused. Once the scan returns clean, complete the second assertion and
   download it. Observable: the activity entry for the release exists and was written before
   the target was issued, and the same download requested with an `editor` token is refused.
5. **Withdraw.** Take the one-action link from the acknowledgement of journey 1 and open
   `/retrait/<token>/`. Confirm. Observable: a certificate naming every store the record was
   removed from, the lead absent from `/atelier/demandes/` and from any export, the reference
   no longer resolving, and an activity entry recording the withdrawal that no later request
   can update or delete.

**States.** Every list has an empty state and none of them is a blank region. The catalogue
has three distinct ones: nothing published in this locale, nothing matching this filter
combination, and nothing in this locale for a record that exists in the other. The lead inbox
has two: no leads at all, and none matching the current filters. Every route has a loading
state, and the pinned sequence has a degraded state it reaches on its own when it cannot keep
up. The funnel has six: empty, saved draft, invalid with a count of what is left to fix,
sending, refused with the answers kept, and done. A document has three: awaiting a scan,
clean, and rejected with a reason. Errors never crash the app: a failure renders the product's
own error surface with the status that matches it, in the locale of the address that produced
it.

## UI/UX notes

**Mood.** Editorial, confident and quiet. This is a studio showing its own work, so the work
is the argument and the words are the caption. Type is set very large and space is used
generously, and nothing is decorated: there is no ornament anywhere in the system, no drop
shadow, no gradient used as decoration and no illustration that is not a client's work. The
ground is a warm off-white rather than a pure white and the ink is a near-black rather than a
pure black, which is what lets a page of enormous type read as printed rather than as
shouted. Reversals -- a pure white on a near-black -- are used for the award panel and for
the overlay navigation, and nowhere else.

**The scale system, and why it is the first thing to get right.** The root size of the
document is a fraction of the window's width rather than a fixed number, and which fraction
is used is decided by the window's **orientation** rather than by its width. Every dimension
in the document -- type, space, radius, the size of a card, the height of a band -- is a
multiple of that root, so the page scales as one object rather than as a set of elements that
happen to move together. The root stops growing past a very wide window, so the type does not
run away on a large monitor.

The arrangement is a separate responsive system, keyed on the **width of the viewport**,
across five width tiers, each with its own breakpoint. The two agree most of the time and must never be merged: a
phone held sideways takes the landscape scale and the narrow arrangement, and a small window
on a desktop takes the landscape scale and, below the first breakpoint, the narrow
arrangement too. The consequence that reads as a
defect and is not: a medium landscape window produces the shortest pages on the entire site,
because it renders the wide arrangement at about two thirds size. A builder who "fixes" that
will make it worse.

**Type.** Two families, both freely licensed, both subset to Latin plus the accented range
both locales need and the punctuation the copy uses. The interface face is a neo-grotesque
with a large x-height, closed apertures and near-vertical terminals, used at a regular and a
medium weight and no other -- the reference asks in three places for a heavier weight the
loaded set does not carry, and the build sets the medium rather than letting the browser
synthesise one. Three roles: a title style for display lines, a body style for reading, and a
small label style. The small label style is the highest-risk type in the system, because it
is simultaneously the smallest, the most numerous and set uppercase with tight tracking, and
any change to it is re-checked at all three scales before it ships. A display face for the
wordmark and the giant letter tiles is **not loaded at all**: both usages ship as drawn
geometry, so the wordmark renders identically with the face absent.

**Palette, by role.** A warm off-white page ground and a near-black ink, which is the
default pairing and passes the strictest contrast level. A pure white and a pure black for
reversals. Four card grounds, each muted and each with its own character: a cool blue-grey, a
sage green, a dusty pink and a soft orange terracotta. A card's ground belongs to the **record**
rather than to the position, so a project keeps its colour wherever it appears -- on the home
column, in the mosaic, and on its own hero. Three greys for secondary, tertiary and disabled
text, and a single light, vivid indigo reserved for numbered list markers, used nowhere else on the
site. One hairline colour, and no elevation ramp at all: **every visible edge in the product
is a hairline inset ring rather than a shadow**, which is the single decision that makes the
site read as printed rather than as stacked panes.

Two measured pairings were too faint to read and are corrected rather than copied. The
breadcrumb's ancestor is set in ink at a raised opacity rather than in a mid grey at a low
one. The accent hover ink, which is the terracotta on the off-white, is given a rule beneath
it, so the colour is not the only signal -- and that is the general rule: **colour is never
the only carrier of meaning anywhere in this product**, which is why the catalogue's active
filter changes a mark as well as a tone.

**Motion.** Seven easing shapes, one of which carries the clear majority of uses and is the
house curve. The character is considered rather than bouncy: entrance and exit are
entrance and exit are asymmetric on purpose, nothing overshoots, and nothing springs. Twelve named reveals, of
which the signature is a headline whose characters rise into place one after another as it
enters. Exactly three keyframe animations exist in the whole system; everything else is a
transition. **No blanket property transition exists anywhere** -- every transition names what
it animates -- because a blanket one makes layout properties animatable and turns an ordinary
class change into a sequence of forced layouts.

Scroll is intercepted and smoothed. Six affordances that interception breaks are restored
explicitly and are treated as part of the feature rather than as a repair: paging keys, home
and end, tabbing to an element below the fold, find-in-page, same-document fragment links, and
a draggable position indicator in place of the native scrollbar. A reveal plays once per
record and does not replay when the visitor scrolls back past it. The panel that covers a
route transition uncovers within a hard limit even when the incoming route never arrives,
because a covering panel with no limit can leave the whole site unreachable behind it.

Reduced motion is honoured throughout, and it is a layout, not an absence: the home route
becomes four stacked readable sections with the feature rail vertical, the background video
becomes a single still frame, and the character reveal becomes an ordinary appearance.

**Density and layout.** Spacious. The chrome is a fixed burger and a wordmark, and the
navigation is a full-window overlay rather than a bar: it has modal semantics, traps focus,
closes on escape, makes the page behind it inert, and returns focus to the burger. The footer
sits on every route and stacks from five columns to two as the window narrows. The catalogue
is a three-tier mosaic at the wide arrangement, two across at the intermediate one, and one
column of list rows with an image at the narrow one, where the filter bar collapses behind a
control that closes on selection.

The studio console is a different room and looks like one. It is information-dense rather
than spacious: rows sit tight enough that a working queue fits one screen, figures align in a
column, and the surface leads with a command palette rather than with navigation. Creating a
record is three addressed steps rather than one long form. A row that is reordered or whose
state is changed moves immediately and settles when the server agrees.

**The eight risks this design creates, and their repairs.** Each is named because each is
beautiful and each breaks something for somebody, and shipping seven of the eight is how a
site like this fails an audit: a headline split into characters is one undivided string in the
accessible tree, with the split parts hidden and selection restored; the drawn wordmark has a
visually hidden heading behind it carrying the real title; removing the native scrollbar
restores position, dragging and keyboard paging; intercepting scroll restores fragment links,
focus scrolling and find-in-page; the horizontally-scrolling rail is keyboard reachable with a
linear reading order; hover-only card content is in the card's accessible name and visible
without hover; the overlay is modal with a focus trap and an inert background; and a route
change moves focus to the main landmark and announces the new title.

**Accessibility bars.** Body text and its background meet the contrast bar, and the default
ink-on-ground pairing exceeds it. Comfortably sized touch targets on every interactive
element, including the filter toggles and the two language-switch items. Full keyboard
navigation with a focus ring visible against both the light ground and the dark one, never
removed. Focus order follows the visual order at every width, including inside the pinned
sequence. One banner, one navigation, one main and one contentinfo per route, one
first-level heading, no skipped levels, and a skip link to the main landmark that is first in
the order and visible on focus. Labels on every icon-only control. Live regions for filter
results, form errors, route changes and save states. At twice the zoom the narrow arrangement
renders with nothing lost and no sideways scrolling, and because the root scale is a fraction
of the window rather than of the text size, that has to be tested deliberately rather than
assumed.

**One primary action per surface.** Every route leads with exactly one primary action,
visually distinct from every secondary one: the home route offers the catalogue, the
catalogue offers its first project, a case study offers the enquiry, the expertise and agency
routes offer the enquiry, the contact route offers the project branch, and the console's
record editor offers publish. A surface with two equally weighted primary actions has none.

## Technical requirements

**Stack.** Server-rendered pages with progressive enhancement. Every public route is a
complete document the server sends; behaviour attaches to markup that is already there.
Python 3.12 with Flask and Jinja templates serves both the rendered routes and the JSON API
under `/api` on one origin. There is no client framework and no component runtime in the
browser: the catalogue filter, the funnel's step machine, the overlay navigation, the command
palette and the console's row edits are enhancements over markup that works as a plain link
or a form submission without them. Node 20 is present for the asset pipeline. Data lives in
PostgreSQL, reached at `DATABASE_URL`. Transactional mail is delivered to the mail server
reached at `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS`. Both are already running
and are not installed, started or replaced by the app. These two are the only backing
services: no cache server, no queue, no object store, no identity provider and no search
service is introduced.

**Progressive enhancement is a contract, not a preference.** With scripting unavailable the
catalogue still filters, because the filter bar is a form whose submission is the same
address the enhanced path writes. The funnel still completes, because each step is a form
that posts to the next step's address. The overlay navigation is still reachable, because the
burger is a link to a navigation route. An enhancement that is the only path to a feature is
not an enhancement.

**Environment.** `APP_PUBLIC_URL` and `APP_PUBLIC_PORT` give the public origin and port;
`DATABASE_URL` gives the database; `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER` and `SMTP_PASS` give
the mail server. Read every one from the environment. Never hardcode a host, a port or a
credential, and never assume a default when a variable is absent: fail loudly instead.

**Mail.** The acknowledgement is sent over SMTP to the configured host and port, and it is
enqueued inside the same transaction that writes the lead. When the mail server is
unavailable the lead is still written, the acknowledgement waits, and the confirmation route
says an acknowledgement is on its way rather than claiming one was sent. Nothing about the
delivery state changes whether the lead exists.

**No third-party origin.** The public site makes no request to any origin the visitor did not
choose. There is no analytics vendor, no font host, no tag manager and no embedded player.
Page views are recorded by the product itself, with the route, the locale and the moment, and
the record is readable in the console.

**Security headers.** Every response carries a strict transport policy, a nosniff content-type
policy, a referrer policy that sends the origin only across origins, a frame-ancestors
restriction, and a permissions policy denying camera, microphone, geolocation, payment and
USB. The content policy allows scripts only from the site itself with a nonce and **carries no
unsafe-inline for scripts**: the structured data in the head is a data block rather than a
script, and the inline critical stylesheet carries the nonce. Reaching for unsafe-inline to
make the structured data work removes most of the value of the policy.

**Nothing secret reaches the browser.** No credential, no token, no database address and no
mail password appears in any document, stylesheet, script or response body the browser
downloads.

**Input handling.** Every public field is length-bounded, type-validated and normalised
before storage. Rich text written in the console is sanitised against an allow-list at write
time, and the sanitised form is what is stored. Lead content is escaped as text everywhere it
is rendered, including in mail. Object keys are derived from a server-generated identifier and
never from a supplied filename. Image processing runs with resource limits, because a decoder
is the largest untrusted-input surface in this system.

**What is being protected.** Two assets carry the risk here and everything in this section
protects one of them: a person's information, and the capability to publish. An unauthorised
publish is defacement of the studio's own shop window, so the publish transition is the most
tightly held action in the product, and every use of it is recorded.

**Authorization in one place.** Every read and every write passes through one decision taking
the principal, the action and the subject. There is no permission check in a route handler and
none in a template. Client-side checks exist to hide controls and are never the protection.
Every list filters by permission inside the query; every detail endpoint returns the same
status for absent and for forbidden.

**Query discipline.** Three lists make it likely that a page asks the database one question
per row, and each is named: building the catalogue, which needs each project's client and its
media; the lead inbox, which needs each lead's owner and note count; and the media library,
which needs each item's usage count. Each answers in one query whose count does not grow with
the number of rows, and that property is asserted rather than assumed.

**Caching.** Four values are held: the catalogue payload per locale, the four facet counts per
locale, the award totals, and the navigation destinations. Each is held under a key carrying a
version, and invalidation **bumps the version rather than deleting the key**, so the previous
value keeps answering until the new one is written. Deleting instead produces a rush of
identical expensive work the instant the key goes cold.

**Transactions.** A publish is one transaction across the state, the slug history, the
redirect and the invalidation. A lead write is one transaction across the lead, its answers,
the consent record and the acknowledgement. A rank rebalance is retried on conflict rather
than left partly applied. Two writers holding the same record do not silently overwrite each
other: the later write is refused, names the current state and the actor who set it, and the
record is left as it was.

**Idempotency.** The enquiry endpoint takes an idempotency key and the uniqueness of that key
is the database's to enforce, not the application's to check first. Every maintenance
operation runs twice with no observable difference. A job that fails is retried a bounded
number of times and then becomes a visible dead letter rather than a silent drop.

**Performance.** The largest element painted in the first screen of every route is an image
or a display line that is loaded eagerly and asked for in the head, not deferred with
everything else. Exactly two typeface requests occur on a cold route load and none on a warm
one, and the faces are content-hashed and cached for a year. Below-fold images are deferred.
Video loads its metadata only until it is in view. An internal link is prefetched when the
pointer enters it or it takes focus, at most a few at a time, cancelled on exit, and never on
a metered connection. The number of surfaces the browser is asked to hold ready to move is
bounded, and a hint is applied when an animation attaches and removed when it detaches rather
than left resident.

**Logging and measurement.** Structured logs, one object per event, carrying a correlation
identifier generated at the edge and propagated through every job. **No personal data reaches
a log**: no mail address, no name, no payload and no document reference, enforced by a
redaction step at the logging boundary with a deny-list of field names rather than by
discipline at each call site. Errors are never sampled away.

The alarm that matters most is the least obvious one: a sharp fall in enquiry volume against
the same weekday. Every other failure in this product announces itself, and a form that
quietly stops accepting submissions looks exactly like a quiet fortnight. Alongside it, a
synthetic submission runs against the real endpoint, confirms the lead was written and the
acknowledgement enqueued, and cleans up after itself, because checking that a form renders is
not checking that a form works.

**Degradation, in order.** The award stage's scene layer unavailable means the poster
composition. The console's search unavailable means a plain listing with a notice. The mail
server unavailable means leads are written and acknowledgements wait. The database
unavailable means the public site keeps serving from what it has already built, the console
is unreachable, and the enquiry endpoint refuses with a retry hint while the visitor's draft
survives on their own device. Each rung has a defined behaviour rather than a cliff.

**Architecture, as boundaries rather than as modules.** The server is organised into
modules with stated boundaries: content, media, publish, routing, leads, people, privacy,
integrations, jobs and observe. The one boundary that is load-bearing is privacy: retention,
consent and erasure live in one module with its own interface rather than sprinkled through
the others, because the way deletion goes wrong is always a store somebody forgot, and one
module is the only way there is a single inventory of everywhere personal data is kept. On
the browser side the equivalent rule is that a case-study block depends on the shared
primitives alone and never on a route's own components, because the same blocks are used by
the expertise details too.

**Observability, in three layers.** The `observe` concern covers logging, tracing, metrics
and alerting. Tracing spans a public request, a console request, a job run, an outbound call
and a rendition, each carrying the route or kind, the cache result and the duration; traces
are sampled, with every error trace and every job failure kept whatever the sample says.
Monitoring reports the field metrics per route shape, per width class and per locale, at the
seventy-fifth and the ninety-fifth percentile, and alerts on a sustained regression rather
than on a single sample. The console's own search answers within a bounded latency at the
ninety-fifth percentile, and so does a console list; a latency budget stated as an average
hides exactly the slow tail people notice.

**Backup and recovery.** The database is backed up continuously, with point-in-time recovery
to any second inside the recent window and a daily snapshot retained for longer. The object
store is versioned with a delete marker. A restore is tested on a schedule into an isolated
environment, with the result recorded. The last rule is the one that gets missed and is
stated first in importance: a restore runs retention before the environment becomes
reachable, so a backup cannot quietly reintroduce data the studio certified as deleted.

**Supply chain.** The lockfile is committed, and a build carrying an out-of-date lockfile
fails. A vulnerability scan runs on every build. The update cadence is patch weekly and
automatic, minor monthly and reviewed, major deliberate. Build artefacts are attested for
provenance and the deploy verifies the attestation before anything serves.

**More response headers.** Beyond the set already named, a cross-origin opener policy of
same-origin and a cross-origin resource policy of same-site are set. A report-only companion
policy reports to a first-party collector and is reviewed before any tightening, so a policy
change is measured before it breaks something silently.

**Measurement, collected first-party.** The analytics collector is served from a first-party
path so that nothing about it depends on whether a visitor's browser has blocked a
third-party host. Collection records the route, the locale and the moment, with a salt
rotated regularly, and there is a written inventory of every cookie and every storage key
the product writes: four strictly necessary items, one of which is the offline page store
that keeps working when the connection goes, and nothing else before consent. Tamper evidence on the activity log is deliberately **not**
specified: the studio's scale does not warrant hash chaining, and claiming a guarantee the
build does not provide is worse than stating the boundary.

**Seeding.** The app seeds its own data on first start and seeding is idempotent: starting
twice produces the same rows, not two copies.

## Data model

Persisted in PostgreSQL. Names below are the vocabulary this brief uses; the shape is the
requirement, the spelling is not.

**`account`** -- identity, hashed credential, role (`editor` or `commercial`), created
instant. **`session`** -- the bearer token, its account, its expiry.

**`translation_group`** -- the identity a record has across locales. Every project, expertise
record, person, award and page belongs to exactly one group, and the language switch resolves
through it. A group with one published side is what makes the switch explain itself rather
than lead nowhere.

**`project`** -- the record: its group, its client, its year, its tier (`feature`,
`secondary` or `list`), its card ground, its rank. **`project_translation`** -- one row per
locale: the locale, the title, the standfirst, the slug, the state (`draft`, `in_review`,
`scheduled`, `published`, `withdrawn`), the scheduled instant, the published instant, the
meta title, the meta description, and a version the concurrent-edit rule reads.
**`project_discipline`** -- the many-to-many that makes a project carry more than one
discipline, which is why the four facet counts sum to more than the total.

**`block`** -- one ordered element of a case study: its project translation, its kind (one of
the eleven), its position within the translation, its content, its modifier, and the media it
references. The gap before a block is derived from its kind and the kind of the block before
it, and is not a column.

**`media`** -- the studio's images and videos: a server-generated key, the original filename
kept as metadata only, the declared type, the detected type, the focal point, the scan state.
**`media_rendition`** -- one generated size of one media item, on a fixed ladder; arbitrary
dimensions are refused.

**`expertise`**, **`expertise_translation`** -- the five services, their skills and their
slugs, shaped like a project and its translations. **`person`** -- the team. **`award`** --
the two award bodies and their counts. **`page`**, **`page_translation`** -- the legal
notices, the personal-data page and the error copy.

**`slug_history`** -- every slug a translation has ever carried, with the locale and the
instant it was superseded. **`redirect`** -- a source path, a target, a permanent or
temporary status, and whether it was written automatically by a rename or by hand. A target
is a path beginning with one slash or an address on the allow-list, and nothing else is
stored.

**`revision`** -- a record as it was at a publish, with the actor and the instant, restorable
into draft.

**`lead`** -- the enquiry: its reference, its branch (`project`, `application` or
`question`), the submitted instant, the idempotency key, the state (`new`, `routed`,
`acknowledged`, `in_progress`, `answered`, `closed`, `withdrawn`), the owner, the closing
reason, the retention deadline and the withdrawal token. The idempotency key is unique, and
that uniqueness is the store's rule rather than a check the application makes before writing:
it is what makes two simultaneous submissions produce one row.

**`lead_answer`** -- one answer per question, carrying **the question text as it was worded at
submission** alongside the answer. The detail view renders these, so re-wording a step next
year does not rewrite what somebody was asked this year. **`lead_note`** -- what the studio
has added since.

**`consent_record`** -- what the enquirer agreed to, the wording they were shown, and when.

**`document`** -- a candidate's attachment: its lead, its server-generated key, its declared
type, its detected type, its `scan_state` of `pending_scan`, `clean` or `rejected`, and the
rejection reason. The bytes are unreachable in any state but `clean`, and that is decided
where they are read.

**`activity_entry`** -- who did what to which record and when, for every privileged read and
every publish. **Append-only at the database grant**: the application has no update or delete
permission on it, so no handler anybody writes later can weaken it.

**`job_run`** -- a scheduled publish, a retention pass or a synthetic submission, with its
attempt count, its idempotency key and its outcome. **`page_view`** -- the route, the locale
and the instant, readable in the console.

**Fields every record carries.** A created timestamp with the principal who created it, an
updated timestamp with the principal who updated it, a published timestamp with the
principal who published it, null until a first publish, and a scheduled-for timestamp, null
unless the record is scheduled. Together these are the answer to who changed what and when
without reading the activity log.

**Structure of a block's stored content.** A full-bleed image block stores a wide crop, a
narrow crop and a caption, the two crops both required. A content image stores alternative
text, an optional credit, and a decorative flag that is mutually exclusive with the
alternative text, so a decorative image with alternative text is a contradiction refused at
write. An in-page link block stores an anchor slug, null when the link leaves the page. A
carousel stores an ordered set of image references; a gallery block stores the same with a
caption per entry; an introduction block stores a standfirst and a body.

**Lead fields beyond the obvious.** A spam verdict from an enumerated set, a service-level
due timestamp, a retention due timestamp, and a withdrawn timestamp that is null until a
withdrawal. The application branch adds an availability from an enumerated set and a
location as free text.

**Translation coupling.** A translatable type shows its counterpart's state as a warning
only: publishing the French side of a record whose English side is still a draft is allowed,
with the imbalance surfaced rather than blocked, because a studio that cannot publish in one
language until both are ready publishes in neither.

**States beyond the five.** A withdrawn record may be archived, which is irreversible in the
interface: an archived record leaves every list and keeps its slug history so its addresses
still resolve. Archiving exists so a withdrawn record does not sit in the studio's way
forever.

**Derived rather than stored.** The four facet counts and the catalogue total are computed
inside the catalogue read, so they and the list describe one instant. The gap between two
blocks is derived from the pair of kinds on render. A lead's deadline is derived on read from
its submitted instant, its branch and the studio's working calendar. A project's card ground
is derived from its own identifier, so the same project always wears the same colour.
Generated imagery is deterministic on the media identifier, so the same record always produces
the same picture and building twice changes nothing.

**Seed data.** Four accounts, every one with `deku-demo-pw-2026`: `editor@example.com` and
`editor2@example.com` as `editor`, `commercial@example.com` and `commercial2@example.com` as
`commercial`.

Six project groups. Five are published in both locales and one in French only.
French slugs: `maison-carre`, `atelier-brune`, `port-neuf`, `serre-verte`, `lune-basse`,
`quai-douze`. English slugs: `carre-house`, `brune-studio`, `new-harbour`,
`green-glasshouse`, `low-moon`; `quai-douze` has none and is the case the language switch
must explain.

Disciplines are deliberately multi-valued: `maison-carre` carries `art_direction` and
`showcase_site`; `atelier-brune` carries `art_direction`, `digital_experience` and
`showcase_site`; `port-neuf` carries `commerce` and `showcase_site`; `serre-verte` carries
`art_direction` and `commerce`; `lune-basse` carries `digital_experience`; `quai-douze`
carries `showcase_site`. Five projects are published in French, so the French total is `5`
and the four French counts are `3` for `art_direction`, `1` for `digital_experience`, `3`
for `showcase_site` and `2` for `commerce`, which sum to `9`.

`atelier-brune` is the only project at `feature` tier and its case study carries one of every
block kind, including a full-bleed image with both crops and an autoplaying video with a
description. `lune-basse` sits in `draft` with a full-bleed image missing its narrow crop and
a content image missing alternative text, so a first publish attempt names two unmet
obligations. `port-neuf` is published carrying one superseded French slug in its history, so
a redirect chain exists before the studio touches anything.

Five expertise records in both locales. Four people. Two award bodies, `Webframe` and `DDA`,
each with a count. Three leads: one `routed` and `in_progress` in the `project` branch, one
`new` and unrouted in the `question` branch, and one in the `application` branch carrying a
document in `pending_scan`. Seeding is idempotent.

## Front-end specification

This section is the measured design. Where it and a general instinct disagree, this section
wins, because it was taken off a real site rather than assumed.

**The root scale.** One value governs the document: a size that is a fraction of the window's
width. Two fractions exist and the choice between them is made on **orientation**, not width
-- a portrait window takes the larger fraction and a landscape window the smaller, which is
why a phone renders larger type than a desktop does. The fraction stops applying past a very
wide window, above which the root is clamped, so a large monitor gets a bigger window rather
than bigger letters. Every length in the system -- type size, leading, tracking, gap, inset,
radius, card edge, band height -- is written as a multiple of that root, and no component
introduces a length that is not.

**Width tiers.** Five: a narrow tier, an intermediate tier, a standard desktop tier, a large
desktop tier and a very wide tier. Two shared bands exist for rules that apply to the wide
and intermediate tiers together, and to the narrow and intermediate tiers together. One
height-aware rule exists for short landscape windows, and it is there because the home
route's pinned sequence needs a minimum height. No component is given a sixth breakpoint of
its own: where a layout would break between two tiers, the tier boundary moves.

| Surface | Narrow | Intermediate | Wide |
|---|---|---|---|
| Home pinned sequence | unpinned, four stacked sections | pinned, reduced stage heights | pinned, full |
| Home hero | wordmark full width, menu becomes the burger | split with a narrow left column | split at the half |
| Feature rail | vertical stack | horizontal, one item per screen | horizontal, one and a bit |
| Home catalogue column | full-width cards, no hover state | as wide, narrower | a column at two thirds |
| Catalogue mosaic | one column, every tier as a list row with an image | feature cards full width, others two across | the three-tier mosaic |
| Filter bar | collapsed behind a control | wrapped to two rows | one row |
| Case study hero | title above image, details stacked | as wide, reduced | as measured |
| Full-bleed block | the narrow crop | the wide crop | the wide crop |
| Grid blocks | one column | two columns | three or four |
| Expertise letter tiles | two per row | three per row | four in a row |
| Overlay navigation | full-window, list stacked, no video panel | as wide | as measured |
| Footer | stacked, two columns | four columns | five columns |
| Cursor disc | absent | absent | present on a fine pointer |
| Position indicator | present, wider hit area | present | present |

**The palette, by role.** Fourteen roles and no component hard-codes a value outside them.

| Role | Character |
|---|---|
| Page ground | a warm off-white, faintly beige rather than grey |
| Ink | a near-black, warm rather than blue |
| Reverse ground | a pure black, used by the award panel and the overlay |
| Reverse ink | a pure white |
| Card ground, cool | a muted blue-grey |
| Card ground, natural | a soft sage green |
| Card ground, warm | a dusty pink |
| Card ground, accent | a light, soft orange read as a warm terracotta |
| Secondary text | a mid grey, readable at body size on the page ground |
| Tertiary text | a lighter grey, for metadata only |
| Disabled | a pale grey that reads as unavailable rather than as faint |
| Hairline | a barely-there line at low contrast against the page ground |
| Index marker | a light, vivid indigo leaning violet, on numbered list markers and nowhere else |
| Focus | a high-contrast ring legible against both the page ground and the reverse ground |

Ink on the page ground is the default pairing and clears the strictest contrast level. Ink on
the reverse ground clears it too. Ink on the cool, natural and warm card grounds clears the
standard level. Ink on the accent ground clears it **only at display sizes**, so the accent
ground carries display type and never body copy. The violet clears the standard level on the
page ground and is restricted to markers.

**Type.** Two families and no third. The interface family is a freely licensed neo-grotesque
with a large x-height, closed apertures and near-vertical terminals, loaded at a regular and a
medium weight, subset to Latin plus the accented range both locales need plus the punctuation
in the copy. It carries three roles: a **title** style at the display sizes, a **body** style
for reading, and a **small label** style set uppercase with tight tracking. Exactly two
typeface requests occur on a cold route load and none on a warm one. The fallback stack
carries metric overrides so the swap does not reflow. The wordmark and the expertise route's
giant letter tiles are **drawn geometry**, not text, and the display face they would need is
not loaded at all.

**Shape, edge and material.** One radius ladder, plus a pill for the year badge and a circle
for the burger, the cursor disc and the scroll cue. The year badge has **no fixed width** and
fits a five-character value. There is **no shadow anywhere**: every visible edge is a
hairline inset ring. Only two layer values escape a stacking context -- the overlay navigation
and the position indicator -- and every other layered surface stacks within its own context.

**The chrome.** A fixed wordmark and a fixed burger, present on every public route. The
navigation is a full-window overlay: it names the four destinations, carries the studio's
contact details, and on the wide arrangement carries a panel showing the hovered
destination's ground. It has modal semantics, traps focus, closes on escape, makes the page
behind it inert, restores the scroll position on close, and returns focus to the burger.
Opening and closing it twice leaves the document scrollable and where it was. The language
switch sits in the overlay and in the footer, carries `FR` and `EN`, marks the current locale
as current rather than only colouring it, and is disabled with an explanation where a
translation is missing. The footer stacks address, mail addresses, phone, socials and legals,
and the phone number appears **once**.

**The catalogue mosaic.** Three card shapes with three different proportions: a large square
feature card, a wide secondary card, and a full-width list row carrying a small image. All
three share one base that carries the ground, the overlay and the container, which is why all
three park their grounds at their own height rather than at the grid's. A card's resting state
shows the title and the year; its hover state adds the client and the disciplines; on a touch
device the hover content is visible at rest. The filter bar sits above the mosaic in one row
at the wide arrangement, wraps to two at the intermediate, and collapses behind a control at
the narrow one that closes on selection. An active filter carries a mark as well as a tone.

**The case study.** A hero carrying the title, the client, the year and the disciplines over
the project's own ground, then the block sequence, then a return control. **The gap before a
block is decided by the kind of the block before it**: two full-bleed blocks meet with no gap,
a text block after a full-bleed block takes the largest gap in the system, and two text blocks
take the ordinary one. A full-bleed image renders its narrow crop below the first tier
boundary and its wide crop above. A carousel is keyboard-operable with the controls in the tab
order and the position announced. An inline video with no source renders its poster with the
controls over it and a line saying so.

**The home route.** Five bands. The hero carries the drawn wordmark, a visually hidden real
heading, and the standfirst. The pinned sequence holds its place through several screens of
scroll and grows when the studio adds a featured project; it unpins below a minimum window
height and under reduced motion, and it unpins itself if it cannot keep up. The feature rail
moves horizontally as the visitor scrolls down, is keyboard reachable, and stacks vertically
at the narrow arrangement. The catalogue column repeats a subset of the mosaic at two thirds
width. The award panel is a reversal: pure white on pure black, the two award bodies with
their counts, three fixed row titles, and a stage that renders a **poster composition** with
the dimensional scene layer declared absent.

**Motion, as character.** Seven easing shapes with one house curve carrying the majority.
Entrance and exit are asymmetric on purpose. Twelve named reveals, the signature of which
raises a headline's characters into place one after another; that reveal is repaired for the
accessible tree, so the headline is one undivided string and can still be selected and copied.
Three keyframe animations in the whole system. Every transition names its properties. A reveal
plays once per record. The route-transition panel uncovers within a hard limit whatever the
incoming route does.

**Scroll.** Intercepted and smoothed, with six affordances restored: paging keys, home and
end, tab-into-view, find-in-page, fragment links, and a draggable position indicator that
replaces the native scrollbar. The indicator is non-informational -- the position is also
available from the keyboard -- and it has a wider hit area at the narrow arrangement. There is
**one scroll engine and one lock stack for the life of the document**: two of either is what
produces a route that scrolls at double speed.

**Iconography.** Every mark in the product is inline vector geometry: a set of small
shapes, each inheriting the current ink colour rather than carrying a colour of its own, and
each declared decorative unless it is the only label a control has. The scroll cue, the
burger's lines, the arrow on a link, the play triangle, the sound mark with its two arcs,
the language chevron and the filter tick are all drawn rather than fetched.

**The expertise gallery and introduction.** The expertise index opens with an introduction
band -- a two-line display heading over a standfirst -- then a gallery of the studio's work
for that discipline, then the letter tiles, then the services list with its skills. An
expertise detail repeats that structure with the discipline's own content, which is what
lets both surfaces share one set of blocks.

**Scroll-driven values, as an inventory.** Five things read the scroll position and nothing
else does: the pinned sequence's progress, the feature rail's horizontal offset, the paper
tiles' scale on the expertise route, the position indicator's thumb, and the reveal state of
each component that has entered the window at least once. Writing that inventory down is how
a sixth consumer of scroll gets noticed before it is shipped.

**Image formats and their resolution.** Three still formats are served from one source: a
modern format for browsers that take it, a legacy format as the fallback, and a lossless
format where an image carries flat colour. Each is offered at a fixed ladder of resolutions
and the browser is told the rendered width so it can choose; arbitrary dimensions are
refused. Typeface responses are two on a cold load, which is the whole typeface budget.

**The largest contentful paint.** On every route the largest element painted in the first
screen is an image or a display line, and that element is eager and preloaded rather than
deferred behind everything else. Deferring the one element the measurement watches costs a
full round trip on the number that decides how fast the page feels.

**Focus parity.** Every hover treatment in the system has a focus equivalent. The accent-ink
hover on a link is also the focus treatment for that link, with the rule beneath it in both
states. A hover treatment with no focus equivalent is a control that looks interactive to a
mouse and inert to a keyboard.

**Conventions, testing and accessibility gates.** Class naming follows one convention with
no exceptions -- a component name, then the part inside it, then the modifier -- and the
convention is held by a lint rule rather than by habit, because it is what makes the
neighbour-spacing rule expressible at all. Accessibility testing is keyboard traversal of
all five journeys with no pointer, a screen-reader pass, zoom to twice and four times the
size, reduced motion on every route shape, and contrast computed from the palette roles
rather than sampled from a screenshot. Automated rules catch roughly a third of what matters
on a design like this one and none of the eight structural risks, which is why the keyboard
traversal is the gate that actually holds the site.

**Imagery, with no binary files.** Every photograph is generated from the record's own
identifier: two overlapping soft fields in two palette roles over a third as the ground, a
gentle warp at their boundary, and a fine grain. It is deterministic on the seed, so the same
record always produces the same picture and building twice changes nothing. A portrait uses
the same generator at a taller proportion with the fields biased toward the upper third, so
the focal point lands where a face would. A placeholder is the same generator at a tiny size
inlined into the document. A background video is the same generator animated by a slow drift
rather than a file, and under reduced motion it is one still frame. The generated fields are
chosen to harmonise with the ground the card wears, so an image never fights its card.

## Constraints

Single tenancy: one studio, one catalogue, no organisations. No native application. The build
is **zero-asset**: the delivery tree carries no image file, no video file, no typeface file,
no three-dimensional model and no vector file, and every asset class the design needs is
generated from text. The two compiled award scenes are not reproducible and are not
substituted: the award stage ships the poster composition the design already specifies as its
degraded state, and the scene layer is declared absent rather than faked. No icon font and no
downloaded icon: every mark in the product is inline geometry. No third-party origin is
contacted at run time -- no analytics vendor, no font host, no tag manager, no embedded
player, no map -- so measurement, search, malware scanning, content delivery and rendition
generation are in-product components with the same observable contracts rather than external
services. Mail is the single exception and is a declared sidecar. No second datastore, no
cache server, no queue, no object store, no identity provider. No background scheduler:
anything that must happen on a deadline is evaluated when the affected data is read or is
reachable through a maintenance endpoint. The console is one locale and is not translated.
External calendar import, connector mirroring and inbound webhooks are modelled as data and
as observable outcomes and are given no surface. Co-host, support, owner, publisher and
recruiter actors exist in the authorization model as the two roles this brief names and get no
surfaces of their own. The legal notices carry placeholder text that is marked as
placeholder, because legal wording is the studio's to supply. The app must stay responsive
with six projects seeded and with a thousand projects, ten thousand blocks and ten thousand
leads loaded.


The principle behind the zero-asset rule is what the whole substitution guide rests on:
every asset class the design would otherwise need is generated from text at build time, and
each substitution states honestly what is lost rather than pretending nothing is.
There is no analytics vendor, no consent management platform and no error trace sink: each
is a placeholder in the source material with no product behind it here, and each is replaced
by a first-party path. Audio is specified nowhere in this product and none ships. The
studio's legal identity is `Verso SARL`; the country of establishment is Belgium, and the
footer carries the
postal code `9000` with the rest of the address. The whole of the source material's own
build order -- its phases, its parallelism, and what can be seen after each week -- is
deliberately not carried: this brief states the product, never the sequence in which to
build it.

## Deployment contract

- The app must be reachable at `APP_PUBLIC_URL`. The port mapping is `${APP_PUBLIC_PORT}:4173`,
  where `4173` is the container-internal port and `APP_PUBLIC_PORT` is what the outside world
  uses. Read both from the environment; never hardcode either.
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
- The backing services named in this brief are already running and reachable at their
  environment variables. Do not download, install, compile or start a copy of any of them.
- Use only the providers named in this brief. No edge functions.
- No persistent volumes, no fixed container names, no custom networks.

**API shapes.** Field names are exact. A plain list endpoint returns a top-level JSON array;
the catalogue endpoint returns an object because it carries a total and its facets alongside
the results. A successful call returns the named resource or shape. An invalid, unauthorized
or conflicting call is rejected as a client error, never as a server error and never as a
silent success, and carries a message naming the reason. Bearer auth is required on everything
under `/api/console/` and `/api/maintenance/`, and on nothing else.

| Endpoint | Request body / query | Returns |
|---|---|---|
| `POST /api/auth/signup` | `email`, `password` | the created account and a bearer token |
| `POST /api/auth/login` | `email`, `password` | a bearer token |
| `GET /api/health` | none | `200` |
| `GET /api/catalogue` | `locale`, `discipline`, `mode` | an object carrying `total`, `facets` and `results`, each result carrying `slug`, `title`, `client`, `year`, `tier`, `disciplines`, `ground` |
| `GET /api/catalogue/facets` | `locale` | the four disciplines with their counts, from the same read as the list |
| `GET /api/projects/{slug}` | `locale` | one project with its blocks in order, each block carrying `kind`, `position` and its content |
| `GET /api/expertise` | `locale` | an array of the five services with their skills |
| `GET /api/expertise/{slug}` | `locale` | one service in detail |
| `POST /api/enquiries` | `branch`, `locale`, `answers`, `consent`, header `Idempotency-Key` | the created lead with its `reference`, or the same reference on a repeat |
| `GET /api/enquiries/{ref}` | none | the lead's public shape: reference, branch, submitted instant, commitment |
| `POST /api/enquiries/{ref}/withdraw` | `token` | the certificate naming every store the record was removed from |
| `GET /api/console/projects` | `state`, `locale` | an array of records the caller may read |
| `POST /api/console/projects` | the identity fields | the created project and its French translation |
| `PATCH /api/console/projects/{id}` | any field, including `slug` and `state` | the updated translation, or a conflict naming the current version |
| `POST /api/console/projects/{id}/blocks` | `kind`, `position`, content | the created block |
| `PATCH /api/console/projects/{id}/blocks/{block_id}` | `position` or content | the updated block |
| `POST /api/console/projects/{id}/preflight` | `locale` | every unmet obligation, as an array |
| `POST /api/console/projects/{id}/publish` | `locale` | the published translation, its revision and its invalidation, or the unmet obligations |
| `POST /api/console/projects/{id}/unpublish` | `locale`, `outcome` of `gone` or `redirect`, `target` when redirecting | the withdrawn translation and the redirect it wrote |
| `PATCH /api/console/projects/{id}/rank` | `rank` | the updated ordering |
| `GET /api/console/redirects` | none | every redirect with `source`, `target`, `status`, `origin` |
| `POST /api/console/redirects` | `source`, `target`, `status` | the created redirect, or a rejection when the target is off the allow-list |
| `GET /api/console/leads` | `state`, `branch`, `owner` | an array of leads, filtered by permission in the query |
| `GET /api/console/leads/{id}` | none | one lead with its answers as they were asked, its consent record and its notes |
| `PATCH /api/console/leads/{id}` | `state` | the updated lead, or a refusal naming why |
| `POST /api/console/leads/{id}/assign` | `owner` | the routed lead |
| `POST /api/console/leads/{id}/close` | `reason` | the closed lead; refused with no reason |
| `GET /api/console/documents/{id}/download` | `assertion` | the document, only when its `scan_state` is `clean` and only to `commercial` |
| `GET /api/console/activity` | `actor`, `record` | an array of activity entries, append-only |
| `POST /api/console/search` | `query` | records, leads and destinations matching, for the palette |
| `POST /api/maintenance/run-retention` | none | the count removed, with each absence verified |
| `POST /api/maintenance/run-scheduled-publish` | none | the count published; a failure stays scheduled |

**No mocks.** The lead, its answers, its consent record, the document, the redirect, the
revision and the activity entry must be real rows in `postgres`, and the acknowledgement must
be a real message on the mail server. An in-memory list of leads, a hardcoded confirmation the
app returns to itself, a facet count computed in the browser, a redirect that exists only as a
route rule rather than as a row the studio can read, or an activity entry the application can
delete are all contract violations however good the interface looks. `postgres` and the mail
server are the facts; the app's own caches can reflect them and never substitute for them.

## Definition of done

A stranger can browse the studio's work in French, narrow it to a discipline and see the
total and the four counts agree with the mosaic beneath them, open a case study, read it in
English at a different address, and send an enquiry that arrives once, acknowledged, with the
questions recorded as they were asked. A link to an address the studio renamed last month
still arrives at the work, in one hop. And the person who sent the enquiry can take it back on
one action and be told exactly where it was removed from.
