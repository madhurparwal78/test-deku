# Checklist: Verso

Items: 259
Unpinned values flagged: 6
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The product serves visitors browsing a studio's client work plus the studio publishing that work, as one application. `src: Overview paragraph 1`
- [ ] `C-OV-02` `capability` French is served without a prefix as the default locale, English under a prefix. `src: Overview paragraph 3`
- [ ] `C-OV-03` `capability` A qualified enquiry ends the visitor's journey, becoming a record the studio answers on a clock. `src: Overview paragraph 4`
- [ ] `C-OV-04` `constraint` The application contacts no outside origin at run time other than the named mail server. `src: Overview paragraph 10`

## C-RL User roles

- [ ] `C-RL-01` `role` An anonymous visitor reads every published project, expertise record, person, award in the requested locale. `src: User roles table`
- [ ] `C-RL-02` `role` An anonymous visitor submits an enquiry through any of the three branches. `src: User roles table`
- [ ] `C-RL-03` `role` An anonymous visitor is refused every unpublished record, every enquiry, every document, every activity entry. `src: User roles table`
- [ ] `C-RL-04` `role` An anonymous visitor requesting a console address is refused. `src: User roles table`
- [ ] `C-RL-05` `role` An `editor` creates, edits, reviews, schedules, publishes, withdraws, re-slugs records. `src: User roles table`
- [ ] `C-RL-06` `role` An `editor` requesting a lead, a lead answer, a consent record, a document, the activity log is refused by the server. `src: User roles table`
- [ ] `C-RL-07` `role` A `commercial` reads the lead inbox, assigns an owner, moves a lead through states, closes with a reason. `src: User roles table`
- [ ] `C-RL-08` `role` A `commercial` attempting a record write, a publish, a block reorder is refused by the server. `src: User roles table`
- [ ] `C-RL-09` `role` Authorization is decided in one place taking the principal, the action, the subject, never once per handler. `src: User roles authorization paragraph`
- [ ] `C-RL-10` `role` A refusal carries the same status an absent record would carry, so the console enumerates nothing. `src: User roles authorization paragraph`
- [ ] `C-RL-11` `role` Signup is open, a new account being an `editor` holding no records. `src: User roles signup policy`
- [ ] `C-RL-12` `literal` Four accounts are seeded: `editor@example.com`, `editor2@example.com`, `commercial@example.com`, `commercial2@example.com`. `src: User roles seeded accounts`
- [ ] `C-RL-13` `literal` Every seeded account signs in with the password `deku-demo-pw-2026`. `src: User roles seeded accounts`

## C-CF Core features

- [ ] `C-CF-01` `capability` `POST /api/auth/signup` creates an account, returning a bearer token. `src: Core features rule 1`
- [ ] `C-CF-02` `capability` A signup reusing an existing address is refused as invalid, creating no second account. `src: Core features rule 1`
- [ ] `C-CF-03` `capability` `POST /api/auth/login` returns a bearer token for a seeded address with the corpus password. `src: Core features rule 2`
- [ ] `C-CF-04` `capability` A login carrying a wrong password is denied, returning no token. `src: Core features rule 2`
- [ ] `C-CF-05` `capability` Every route under `/api/console/` refuses a request carrying no bearer token. `src: Core features rule 3`
- [ ] `C-CF-06` `capability` An anonymous visitor requesting a console address is sent to `/atelier/connexion/`, returning afterwards to the requested address. `src: Core features rule 4`
- [ ] `C-CF-07` `capability` Signing out returns the visitor to `/`, invalidating the token so a later request carrying the token is denied. `src: Core features rule 5`
- [ ] `C-CF-08` `capability` Nine public route shapes exist in French without a prefix, nine in English under `/en/`. `src: Core features rule 6`
- [ ] `C-CF-09` `capability` Every public address ends in a trailing slash, being lowercase throughout. `src: Core features rule 7`
- [ ] `C-CF-10` `capability` A path missing the trailing slash, a path carrying an uppercase letter, each answers with a permanent redirect to the canonical form. `src: Core features rule 7`
- [ ] `C-CF-11` `capability` The site never redirects on the browser's language header. `src: Core features rule 8`
- [ ] `C-CF-12` `capability` The language switch resolves through the record's translation group, leading to the paired record. `src: Core features rule 9`
- [ ] `C-CF-13` `capability` A record holding no published translation renders the switch disabled, carrying an explanation. `src: Core features rule 10`
- [ ] `C-CF-14` `literal` The French unavailability line reads `Cette page n'existe pas encore en anglais`. `src: Core features rule 10`
- [ ] `C-CF-15` `literal` The English unavailability line reads `not available in French yet`, prefixed by the page noun. `src: Core features rule 10`
- [ ] `C-CF-16` `capability` The chosen language is remembered on the visitor's own device, being offered later as a suggestion rather than a redirect. `src: Core features rule 11`
- [ ] `C-CF-17` `capability` Every route declares a language matching what the route renders. `src: Core features rule 12`
- [ ] `C-CF-18` `capability` `GET /api/catalogue` takes a `locale` of `fr` or `en`, answering only with records published in that locale. `src: Core features rule 13`
- [ ] `C-CF-19` `capability` The catalogue renders published projects as a three-tier mosaic of feature cards, secondary cards, list rows. `src: Core features rule 14`
- [ ] `C-CF-20` `data` Tier belongs to the record rather than to the card's position in the grid. `src: Core features rule 14`
- [ ] `C-CF-21` `capability` A total sits above the mosaic, counting the published projects in the requested locale. `src: Core features rule 15`
- [ ] `C-CF-22` `capability` Four discipline facets sit above the mosaic, each carrying a live count. `src: Core features rule 16`
- [ ] `C-CF-23` `literal` The four French facet labels read `Direction artistique`, `Experience digitale`, `Site vitrine`, `E-commerce`. `src: Core features rule 16`
- [ ] `C-CF-24` `data` A project carries one discipline or several, so the four counts sum above the total. `src: Core features rule 17`
- [ ] `C-CF-25` `data` The four counts plus the cards beneath come from one read, describing the same instant. `src: Core features rule 18`
- [ ] `C-CF-26` `capability` The filter bar offers an any-filter mode plus an all-filter mode, the count reflecting the chosen mode. `src: Core features rule 19`
- [ ] `C-CF-27` `literal` The clear control reads `Tout effacer` in French, `Clear all` in English. `src: Core features rule 20`
- [ ] `C-CF-28` `capability` The whole filter state lives in the address, so a copied address reproduces the view in a fresh session. `src: Core features rule 21`
- [ ] `C-CF-29` `literal` The four discipline values are `art_direction`, `digital_experience`, `showcase_site`, `commerce`. `src: Core features rule 21`
- [ ] `C-CF-30` `literal` The two filter-mode values are `any`, `all`. `src: Core features rule 21`
- [ ] `C-CF-31` `capability` Applying a filter changes the address, reloading that address rendering the same set from the server. `src: Core features rule 22`
- [ ] `C-CF-32` `capability` A filter combination matching nothing renders the empty panel carrying a zero total plus the clear control. `src: Core features rule 23`
- [ ] `C-CF-33` `literal` The empty-filter panel title reads `Aucun projet ne correspond`. `src: Core features rule 23`
- [ ] `C-CF-34` `literal` A locale holding no published project renders `Bientot` over `Les projets arrivent. En attendant, parlons du votre.`. `src: Core features rule 24`
- [ ] `C-CF-35` `capability` A card's hover content lives in the card's accessible name, being visible without hover on a touch device. `src: Core features rule 25`
- [ ] `C-CF-36` `capability` `GET /api/catalogue` returns an object carrying `total`, `facets`, `results`. `src: Core features rule 26`
- [ ] `C-CF-37` `capability` A case study renders a hero, a block sequence, a return control. `src: Core features rule 27`
- [ ] `C-CF-38` `capability` Eleven block kinds are built, a block being an ordered row rather than a field. `src: Core features rule 28`
- [ ] `C-CF-39` `data` The gap before a block is decided by the pair of kinds, two full-bleed blocks meeting with no gap. `src: Core features rule 29`
- [ ] `C-CF-40` `constraint` A full-bleed image block carries two crops, reaching no published state with one. `src: Core features rule 30`
- [ ] `C-CF-41` `constraint` An autoplaying video block carries a description, reaching no published state without one. `src: Core features rule 31`
- [ ] `C-CF-42` `constraint` Every content image carries alternative text or a decorative declaration, the preflight naming any block missing both. `src: Core features rule 32`
- [ ] `C-CF-43` `capability` An inline video holding no source renders a poster under the controls, carrying a line saying no source is attached. `src: Core features rule 33`
- [ ] `C-CF-44` `capability` The return control restores the catalogue's filters plus the scroll position the visitor left. `src: Core features rule 34`
- [ ] `C-CF-45` `capability` `quai-douze` is published in French alone, so the switch on that record explains itself. `src: Core features rule 35`
- [ ] `C-CF-46` `capability` A carousel is operable from the keyboard, the position being announced. `src: Core features rule 36`
- [ ] `C-CF-47` `data` A statistics row renders stored figures rather than text typed into a paragraph. `src: Core features rule 37`
- [ ] `C-CF-48` `capability` The call-to-action block leads to the contact route in the same locale. `src: Core features rule 38`
- [ ] `C-CF-49` `capability` The home route renders five bands in order: hero, pinned sequence, feature rail, catalogue column, award panel. `src: Core features rule 39`
- [ ] `C-CF-50` `capability` The home route carries one first-level heading, a visually hidden heading standing behind the drawn wordmark. `src: Core features rule 40`
- [ ] `C-CF-51` `capability` Adding a fourth featured project lengthens the pinned sequence rather than compressing the contents. `src: Core features rule 41`
- [ ] `C-CF-52` `capability` The pinned sequence unpins in a short landscape window, rendering as stacked sections. `src: Core features rule 42`
- [ ] `C-CF-53` `capability` The pinned sequence unpins on a struggling machine, becoming stacked sections rather than stuttering. `src: Core features rule 43`
- [ ] `C-CF-54` `capability` The feature rail is keyboard reachable in a linear reading order, stacking vertically at the narrow arrangement. `src: Core features rule 44`
- [ ] `C-CF-55` `literal` The award panel names `Webframe`, `DDA`, each carrying a count. `src: Core features rule 45`
- [ ] `C-CF-56` `literal` Three award row titles read `Site Of The Month`, `Site Of The Day`, `Developer Award` in both locales. `src: Core features rule 45`
- [ ] `C-CF-57` `constraint` The award stage renders a poster composition, the dimensional scene layer being declared absent. `src: Core features rule 45`
- [ ] `C-CF-58` `capability` The expertise route renders five services, each carrying a skill list, beside drawn letter tiles. `src: Core features rule 46`
- [ ] `C-CF-59` `capability` Every expertise entry leading to a detail carries a visible resting affordance. `src: Core features rule 46`
- [ ] `C-CF-60` `capability` The agency route renders the studio's story, a three-word marquee, the team, the awards, the clients. `src: Core features rule 47`
- [ ] `C-CF-61` `capability` The contact route renders three entry cards, each leading to a branch of the funnel. `src: Core features rule 48`
- [ ] `C-CF-62` `literal` The three French entry cards read `Un projet`, `Candidature`, `En savoir plus`. `src: Core features rule 48`
- [ ] `C-CF-63` `capability` A closed branch renders a line naming a mail address rather than a control leading nowhere. `src: Core features rule 48`
- [ ] `C-CF-64` `literal` The footer carries `contact@example.com`, `jobs@example.com`, the phone number rendered once. `src: Core features rule 49`
- [ ] `C-CF-65` `data` The footer's copyright year is computed rather than typed. `src: Core features rule 49`
- [ ] `C-CF-66` `data` A record is a translation group holding one row per locale. `src: Core features rule 50`
- [ ] `C-CF-67` `data` A record moves through `draft`, `in_review`, `scheduled`, `published`, `withdrawn`, any other transition being refused. `src: Core features rule 51`
- [ ] `C-CF-68` `capability` The preflight returns every unmet obligation rather than the first. `src: Core features rule 52`
- [ ] `C-CF-69` `capability` A publish attempt on `lune-basse` names two unmet obligations. `src: Core features rule 53`
- [ ] `C-CF-70` `data` A publish is one transaction across the state, the slug history, the redirect, the revision, the invalidation. `src: Core features rule 54`
- [ ] `C-CF-71` `capability` Publishing one project rebuilds that route, the catalogue, the counts, the sitemap, never the whole site. `src: Core features rule 55`
- [ ] `C-CF-72` `data` A publish writes a revision naming the actor plus the instant, restorable into draft. `src: Core features rule 56`
- [ ] `C-CF-73` `capability` A failed scheduled publish stays scheduled, raising an alert before a retry. `src: Core features rule 57`
- [ ] `C-CF-74` `capability` Creating a project runs through three addressed steps, each reachable by a link of its own. `src: Core features rule 58`
- [ ] `C-CF-75` `capability` A reordered block moves before the server answers, a refused reorder returning the row to the prior position. `src: Core features rule 59`
- [ ] `C-CF-76` `data` Rank is rebalanced across the list, so inserting a block rewrites no whole project. `src: Core features rule 60`
- [ ] `C-CF-77` `capability` A second write against a record already changed is refused, naming the editor responsible. `src: Core features rule 61`
- [ ] `C-CF-78` `capability` Changing a published slug writes a permanent redirect from the old path automatically. `src: Core features rule 62`
- [ ] `C-CF-79` `data` Slug history is per locale, a French rename touching no English address. `src: Core features rule 63`
- [ ] `C-CF-80` `capability` A redirect chain is served in one hop, never through an intermediate address. `src: Core features rule 64`
- [ ] `C-CF-81` `capability` `port-neuf` carries one superseded French path before the studio acts. `src: Core features rule 64`
- [ ] `C-CF-82` `capability` Withdrawing a record requires a choice between gone status plus a redirect target. `src: Core features rule 65`
- [ ] `C-CF-83` `literal` The gone copy reads `Cette page a ete retiree volontairement.`. `src: Core features rule 65`
- [ ] `C-CF-84` `constraint` A redirect target is a path beginning with one slash or an allow-listed address, rejected at write, rejected again at serve. `src: Core features rule 66`
- [ ] `C-CF-85` `capability` `GET /api/console/redirects` lists every redirect with source, target, status, origin. `src: Core features rule 67`
- [ ] `C-CF-86` `capability` A sitemap lists every published address in the locale, every internal link on every public route resolving. `src: Core features rule 68`
- [ ] `C-CF-87` `capability` The project branch runs over three addressed steps, the application branch over two, the question branch over one. `src: Core features rule 69`
- [ ] `C-CF-88` `literal` The funnel controls read `Retour`, `Continuer`, `Envoyer`, `Envoi en cours`. `src: Core features rule 70`
- [ ] `C-CF-89` `capability` The draft is held on the visitor's own device, surviving a reload, a closed tab, a refused submit. `src: Core features rule 71`
- [ ] `C-CF-90` `capability` Validation names the field inline, a summary counting what is left to fix. `src: Core features rule 72`
- [ ] `C-CF-91` `literal` The required-answer message reads `Cette reponse est necessaire pour continuer.`. `src: Core features rule 72`
- [ ] `C-CF-92` `constraint` A rejected step writes nothing, leaving no partial lead, no orphan answer. `src: Core features rule 73`
- [ ] `C-CF-93` `literal` The budget question offers `Je ne sais pas encore` as a real answer. `src: Core features rule 74`
- [ ] `C-CF-94` `constraint` The consent statement is never pre-selected, the submission being refused without agreement. `src: Core features rule 75`
- [ ] `C-CF-95` `capability` Submitting twice under one `Idempotency-Key` produces exactly one lead, the store arbitrating. `src: Core features rule 76`
- [ ] `C-CF-96` `capability` A second caller sharing the key receives the first caller's reference rather than a conflict. `src: Core features rule 76`
- [ ] `C-CF-97` `data` The acknowledgement is committed in the transaction writing the lead. `src: Core features rule 77`
- [ ] `C-CF-98` `constraint` The acknowledgement is addressed to the one typed address, carrying no carbon copy, no blind carbon copy. `src: Core features rule 78`
- [ ] `C-CF-99` `literal` A project acknowledgement subject begins `Nous avons bien recu votre demande`, the reference following a colon. `src: Core features rule 79`
- [ ] `C-CF-100` `literal` An application acknowledgement subject begins `Votre candidature est bien arrivee`. `src: Core features rule 79`
- [ ] `C-CF-101` `literal` A reference is `VRS-` followed by six uppercase letters or digits. `src: Core features rule 79`
- [ ] `C-CF-102` `constraint` The acknowledgement body names the studio, never quoting the submitted payload back. `src: Core features rule 80`
- [ ] `C-CF-103` `constraint` Only a submission plus an application outcome send mail, a state change sending nothing. `src: Core features rule 81`
- [ ] `C-CF-104` `literal` The confirmation route renders `C'est envoye` over a line naming the reference. `src: Core features rule 82`
- [ ] `C-CF-105` `capability` A refused submit keeps every answer, a retry reusing the same idempotency key. `src: Core features rule 84`
- [ ] `C-CF-106` `constraint` A submission judged automated receives the status, the body, the confirmation any other submission receives. `src: Core features rule 85`
- [ ] `C-CF-107` `data` The funnel records the question wording used at submission, the detail view rendering the stored wording. `src: Core features rule 86`
- [ ] `C-CF-108` `capability` The lead inbox renders reference, branch, name, subject, state, owner, time left. `src: Core features rule 87`
- [ ] `C-CF-109` `data` A lead moves through `new`, `routed`, `acknowledged`, `in_progress`, `answered`, `closed`, `withdrawn`. `src: Core features rule 88`
- [ ] `C-CF-110` `capability` A lead state change updates the row before the server answers, a refusal returning the prior state. `src: Core features rule 88`
- [ ] `C-CF-111` `capability` Every lead is routed to an owner or appears in an unrouted queue, no third place existing. `src: Core features rule 89`
- [ ] `C-CF-112` `constraint` Closing a lead requires a reason, being refused without one. `src: Core features rule 90`
- [ ] `C-CF-113` `constraint` Lead text is never rendered as markup anywhere, mail included. `src: Core features rule 91`
- [ ] `C-CF-114` `data` The response-time clock respects the studio's working hours. `src: Core features rule 92`
- [ ] `C-CF-115` `capability` `GET /api/console/leads` is readable by `commercial`, refused to `editor` with an absent-record status. `src: Core features rule 93`
- [ ] `C-CF-116` `capability` The lead list, the media list, the record list each answer in one query whose count never grows with the rows. `src: Core features rule 94`
- [ ] `C-CF-117` `capability` Console list filters live in the address exactly as the public catalogue's do. `src: Core features rule 95`
- [ ] `C-CF-118` `constraint` A delimited export neutralises a leading character a spreadsheet would read as a formula. `src: Core features rule 96`
- [ ] `C-CF-119` `data` A document is stored under a server-generated identifier, the arriving name being metadata alone. `src: Core features rule 97`
- [ ] `C-CF-120` `constraint` An upload whose declared type disagrees with the first bytes is rejected. `src: Core features rule 98`
- [ ] `C-CF-121` `constraint` A document is unreachable until the scan state is `clean`, decided where the bytes are read. `src: Core features rule 99`
- [ ] `C-CF-122` `capability` A rejected document is retained carrying the reason, the application staying readable. `src: Core features rule 100`
- [ ] `C-CF-123` `constraint` The activity entry for a download is written before the download target is issued. `src: Core features rule 101`
- [ ] `C-CF-124` `capability` The download endpoint refuses an `editor`, refuses an unauthenticated caller, refuses a document not yet clean. `src: Core features rule 102`
- [ ] `C-CF-125` `literal` An application outcome subject begins `Suite a votre candidature` in the positive case plus the negative case alike. `src: Core features rule 102`
- [ ] `C-CF-126` `constraint` Nothing non-essential is written to a visitor's device before a consent decision. `src: Core features rule 103`
- [ ] `C-CF-127` `constraint` Refusing consent takes the number of actions accepting takes, on the same surface. `src: Core features rule 103`
- [ ] `C-CF-128` `data` The consent decision survives a reload, being recorded on the server beside the lead. `src: Core features rule 104`
- [ ] `C-CF-129` `capability` A withdrawal completes in one action from the acknowledgement link, asking for confirmation alone. `src: Core features rule 105`
- [ ] `C-CF-130` `constraint` A withdrawal deletes the derived copies before the primary record, verifying each absence. `src: Core features rule 106`
- [ ] `C-CF-131` `capability` A completed withdrawal issues a certificate naming every store the record left. `src: Core features rule 107`
- [ ] `C-CF-132` `capability` A withdrawn lead is absent from the inbox, absent from every export, the reference resolving no longer. `src: Core features rule 108`
- [ ] `C-CF-133` `constraint` A restored backup runs retention before the environment becomes reachable. `src: Core features rule 109`
- [ ] `C-CF-134` `constraint` Activity entries are append-only at the database grant, no update reaching them, no delete reaching them. `src: Core features rule 110`
- [ ] `C-CF-135` `capability` The activity log is rendered to `commercial`, refused to `editor`. `src: Core features rule 111`
- [ ] `C-CF-136` `capability` A command palette holds its own address, opening over any console route. `src: Core features rule 112`
- [ ] `C-CF-137` `capability` Every console destination is reachable from the palette by typing. `src: Core features rule 113`
- [ ] `C-CF-138` `capability` An unavailable search component leaves the console falling back to a plain listing carrying a notice. `src: Core features rule 114`
- [ ] `C-CF-139` `ui` The console's record lists render as tables whose deciding column sorts by default. `src: Core features rule 115`
- [ ] `C-CF-140` `capability` The console home renders records awaiting review, scheduled publishes due, leads past commitment, documents awaiting a scan. `src: Core features rule 116`
- [ ] `C-CF-141` `constraint` The console is one locale, never translated. `src: Core features rule 117`
- [ ] `C-CF-142` `capability` An unknown address renders the studio's own not-found page, answering with the not-found status. `src: Core features rule 118`
- [ ] `C-CF-143` `literal` The French not-found body reads `Cette page n'existe pas, ou plus. Voici trois choses qui existent.`. `src: Core features rule 118`
- [ ] `C-CF-144` `capability` A not-found on an English path answers in English, a not-found on a French path answering in French. `src: Core features rule 119`
- [ ] `C-CF-145` `literal` The server-failure body reads `Quelque chose a casse de notre cote. Nous sommes prevenus.`. `src: Core features rule 120`
- [ ] `C-CF-146` `capability` Every public route carries a title plus a description no other route shares. `src: Core features rule 121`
- [ ] `C-CF-147` `literal` The French home title reads `Agence web Ghent : creation de site internet et design graphique`. `src: Core features rule 121`
- [ ] `C-CF-148` `capability` Every public route declares one canonical address, the other locale being declared as the alternate. `src: Core features rule 122`
- [ ] `C-CF-149` `capability` The personal-data page states what the studio records, how long the studio keeps each record, how removal happens. `src: Core features rule 123`
- [ ] `C-CF-150` `capability` The personal-data page is reachable from the footer of every page, the error routes included. `src: Core features rule 123`

## C-UF User flow

- [ ] `C-UF-01` `capability` Every route in the flow table is reachable at the auth level the table names. `src: User flow route table`
- [ ] `C-UF-02` `capability` An expired token mid-action leaves the action unperformed, asking for sign-in again. `src: User flow entry and redirects`
- [ ] `C-UF-03` `capability` Narrowing the catalogue to one discipline moves the total beside the four counts in one repaint. `src: User flow journey 1`
- [ ] `C-UF-04` `capability` A publish moves the public total by one, each carried discipline rising by one. `src: User flow journey 2`
- [ ] `C-UF-05` `capability` A renamed French slug leaves `/en/projects/new-harbour/` untouched. `src: User flow journey 3`
- [ ] `C-UF-06` `capability` A candidate document is refused until the scan returns clean, the release writing an entry first. `src: User flow journey 4`
- [ ] `C-UF-07` `capability` A withdrawal leaves an activity entry no later request updates, no later request deletes. `src: User flow journey 5`
- [ ] `C-UF-08` `capability` Every list renders an empty state, no list rendering a blank region. `src: User flow states`
- [ ] `C-UF-09` `capability` The funnel renders six states: empty, saved draft, invalid, sending, refused, done. `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The mood is editorial, confident, quiet, the work carrying the argument. `src: UI/UX notes Mood`
- [ ] `C-UX-02` `ui` The ground is a warm off-white, the ink a near-black rather than a pure black. `src: UI/UX notes Mood`
- [ ] `C-UX-03` `ui` The root size is a fraction of the window's width, the fraction chosen on orientation. `src: UI/UX notes scale system`
- [ ] `C-UX-04` `ui` The arrangement is keyed on width across five tiers, never merged with the scale system. `src: UI/UX notes scale system`
- [ ] `C-UX-05` `ui` Two type families ship, the interface face carrying a regular cut beside a medium cut. `src: UI/UX notes Type`
- [ ] `C-UX-06` `ui` The display face is never loaded, the wordmark shipping as drawn geometry. `src: UI/UX notes Type`
- [ ] `C-UX-07` `ui` Fourteen palette roles exist, four card grounds belonging to the record rather than the position. `src: UI/UX notes Palette`
- [ ] `C-UX-08` `ui` Every visible edge is a hairline inset ring, no shadow appearing anywhere. `src: UI/UX notes Palette`
- [ ] `C-UX-09` `ui` Colour is never the only carrier of meaning, the active filter changing a mark beside a tone. `src: UI/UX notes Palette`
- [ ] `C-UX-10` `ui` Seven easing shapes exist, one house curve carrying the majority, nothing springing. `src: UI/UX notes Motion`
- [ ] `C-UX-11` `ui` No blanket property transition exists, every transition naming what the transition animates. `src: UI/UX notes Motion`
- [ ] `C-UX-12` `ui` Six scroll affordances are restored: paging keys, home, find-in-page, fragment links, tab-into-view, a draggable indicator. `src: UI/UX notes Motion`
- [ ] `C-UX-13` `ui` Reduced motion renders the home route as four stacked readable sections. `src: UI/UX notes Motion`
- [ ] `C-UX-14` `ui` The navigation is a full-window overlay holding modal semantics, a focus trap, an escape key, focus returned to the burger. `src: UI/UX notes Density`
- [ ] `C-UX-15` `ui` The console is information-dense, leading with a command palette rather than navigation. `src: UI/UX notes Density`
- [ ] `C-UX-16` `ui` Eight structural risks each carry a named repair. `src: UI/UX notes eight risks`
- [ ] `C-UX-17` `ui` Body text meets the contrast bar, focus rings staying visible against the light ground beside the dark one. `src: UI/UX notes Accessibility bars`
- [ ] `C-UX-18` `ui` Every surface leads with exactly one primary action, visually distinct from every secondary one. `src: UI/UX notes primary action`

## C-TR Technical requirements

- [ ] `C-TR-01` `constraint` The application is server-rendered with progressive enhancement, no client framework shipping. `src: Technical requirements Stack`
- [ ] `C-TR-02` `constraint` PostgreSQL plus the mail server are the only backing services, neither being installed by the application. `src: Technical requirements Stack`
- [ ] `C-TR-03` `capability` The catalogue filters, the funnel completes, the navigation opens with scripting unavailable. `src: Technical requirements progressive enhancement`
- [ ] `C-TR-04` `contract` Every host, port, credential is read from the environment, never hardcoded, never defaulted silently. `src: Technical requirements Environment`
- [ ] `C-TR-05` `capability` An unavailable mail server leaves the lead written, the confirmation saying an acknowledgement is on the way. `src: Technical requirements Mail`
- [ ] `C-TR-06` `constraint` The public site requests no origin the visitor did not choose. `src: Technical requirements No third-party origin`
- [ ] `C-TR-07` `constraint` Every response carries a strict transport policy, a nosniff policy, a referrer policy, a frame-ancestors restriction, a permissions policy. `src: Technical requirements Security headers`
- [ ] `C-TR-08` `constraint` The content policy carries no unsafe-inline for scripts. `src: Technical requirements Security headers`
- [ ] `C-TR-09` `constraint` No credential, token, database address, mail password appears in anything the browser downloads. `src: Technical requirements Nothing secret`
- [ ] `C-TR-10` `constraint` Object keys derive from a server-generated identifier, never from a supplied filename. `src: Technical requirements Input handling`
- [ ] `C-TR-11` `data` Cache invalidation bumps a version suffix rather than deleting the key. `src: Technical requirements Caching`
- [ ] `C-TR-12` `data` Every maintenance operation runs twice with no observable difference. `src: Technical requirements Idempotency`
- [ ] `C-TR-13` `constraint` No personal data reaches a log, enforced by a redaction step at the logging boundary. `src: Technical requirements Logging`
- [ ] `C-TR-14` `capability` Seeding is idempotent, a second start producing the same rows rather than a copy. `src: Technical requirements Seeding`

## C-DM Data model

- [ ] `C-DM-01` `data` A translation group is the identity a record holds across locales. `src: Data model translation_group`
- [ ] `C-DM-02` `data` A project translation carries a locale, a title, a slug, a state, a version. `src: Data model project_translation`
- [ ] `C-DM-03` `data` `project_discipline` is a many-to-many, so a project carries several disciplines. `src: Data model project_discipline`
- [ ] `C-DM-04` `data` A block carries a kind, a position within the translation, the referenced media. `src: Data model block`
- [ ] `C-DM-05` `data` `slug_history` records every slug a translation ever carried with the locale. `src: Data model slug_history`
- [ ] `C-DM-06` `data` A redirect stores a source, a target, a status, an origin of automatic or manual. `src: Data model redirect`
- [ ] `C-DM-07` `data` A lead carries a reference, a branch, an idempotency key unique at the store. `src: Data model lead`
- [ ] `C-DM-08` `data` `lead_answer` carries the question text as worded at submission beside the answer. `src: Data model lead_answer`
- [ ] `C-DM-09` `data` A document carries a scan state of `pending_scan`, `clean`, `rejected`. `src: Data model document`
- [ ] `C-DM-10` `data` The facet counts, the catalogue total, the block gap, the lead deadline, the card ground are derived rather than stored. `src: Data model Derived`
- [ ] `C-DM-11` `literal` Six French project slugs are seeded: `maison-carre`, `atelier-brune`, `port-neuf`, `serre-verte`, `lune-basse`, `quai-douze`. `src: Data model Seed data`
- [ ] `C-DM-12` `literal` Five English project slugs are seeded: `carre-house`, `brune-studio`, `new-harbour`, `green-glasshouse`, `low-moon`. `src: Data model Seed data`
- [ ] `C-DM-13` `data` The French total is `5`, the four French facet counts being `3`, `1`, `3`, `2`, summing to `9`. `src: Data model Seed data`
- [ ] `C-DM-14` `data` `atelier-brune` is the only feature-tier project, the case study carrying one of every block kind. `src: Data model Seed data`
- [ ] `C-DM-15` `data` Three leads are seeded across the project branch, the question branch, the application branch. `src: Data model Seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` Every length in the system is a multiple of the root, no component introducing another unit. `src: Front-end specification root scale`
- [ ] `C-FE-02` `ui` The root stops growing past a very wide window, so a large monitor gets a bigger window rather than bigger letters. `src: Front-end specification root scale`
- [ ] `C-FE-03` `ui` Five width tiers exist, no component receiving a sixth breakpoint of its own. `src: Front-end specification Width tiers`
- [ ] `C-FE-04` `ui` The responsive matrix names a narrow, intermediate, wide behaviour for every surface. `src: Front-end specification responsive matrix`
- [ ] `C-FE-05` `ui` Ink on the page ground clears the strictest contrast level, the accent ground carrying display type alone. `src: Front-end specification palette table`
- [ ] `C-FE-06` `ui` The violet index marker appears on numbered list markers, nowhere else. `src: Front-end specification palette table`
- [ ] `C-FE-07` `ui` Exactly two typeface requests occur on a cold route load, none on a warm one. `src: Front-end specification Type`
- [ ] `C-FE-08` `ui` The year badge holds no fixed width, fitting a five-character value. `src: Front-end specification Shape`
- [ ] `C-FE-09` `ui` Two layer values escape a stacking context: the overlay navigation, the position indicator. `src: Front-end specification Shape`
- [ ] `C-FE-10` `ui` The language switch marks the current locale as current rather than colouring alone. `src: Front-end specification chrome`
- [ ] `C-FE-11` `ui` Three catalogue card shapes share one base carrying the ground, the overlay, the container. `src: Front-end specification catalogue mosaic`
- [ ] `C-FE-12` `ui` One scroll engine plus one lock stack exist for the life of the document. `src: Front-end specification Scroll`
- [ ] `C-FE-13` `ui` Generated imagery is deterministic on the record identifier, a rebuild changing nothing. `src: Front-end specification Imagery`
- [ ] `C-FE-14` `ui` A background video is generated by a slow drift rather than a file, reduced motion rendering one still frame. `src: Front-end specification Imagery`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The delivery tree carries no image file, no video file, no typeface file, no model, no vector file. `src: Constraints`
- [ ] `C-CN-02` `constraint` The two award scenes are not substituted, the stage shipping the poster composition. `src: Constraints`
- [ ] `C-CN-03` `constraint` No icon font ships, no downloaded icon ships, every mark being inline geometry. `src: Constraints`
- [ ] `C-CN-04` `constraint` No second datastore, cache server, queue, object store, identity provider is introduced. `src: Constraints`
- [ ] `C-CN-05` `constraint` No background scheduler runs, deadline work being evaluated on read or reached through a maintenance endpoint. `src: Constraints`
- [ ] `C-CN-06` `constraint` The application stays responsive with a thousand projects, ten thousand blocks, ten thousand leads loaded. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The application is reachable at `APP_PUBLIC_URL`, the mapping being `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract`
- [ ] `C-DC-02` `contract` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract`
- [ ] `C-DC-03` `contract` `GET /api/health` returns `200` once the application is ready. `src: Deployment contract`
- [ ] `C-DC-04` `contract` The application starts from the environment image with no manual step. `src: Deployment contract`
- [ ] `C-DC-05` `contract` Credentials are written to `/app/USER_README.md`. `src: Deployment contract`
- [ ] `C-DC-06` `contract` Reserved `.browser_screenshots/` plus `.downloads/` directories exist at the application root, empty. `src: Deployment contract`
- [ ] `C-DC-07` `contract` A production build is served, never a dev server. `src: Deployment contract`
- [ ] `C-DC-08` `contract` The server keeps running after the session ends, being no child of the shell. `src: Deployment contract`
- [ ] `C-DC-09` `contract` The listener binds `0.0.0.0`, so the application answers from outside the container. `src: Deployment contract`
- [ ] `C-DC-10` `contract` The application reaches `postgres` plus `mailpit` at their environment variables without starting a copy. `src: Deployment contract`
- [ ] `C-DC-11` `contract` No persistent volume, no fixed container name, no custom network is added. `src: Deployment contract`
- [ ] `C-DC-12` `contract` A plain list endpoint returns a top-level JSON array, the catalogue endpoint returning an object. `src: Deployment contract API shapes`
- [ ] `C-DC-13` `contract` An invalid, unauthorized, conflicting call is refused as a client error carrying a message naming the reason. `src: Deployment contract API shapes`
- [ ] `C-DC-14` `contract` Bearer auth is required under `/api/console/` plus `/api/maintenance/`, nowhere else. `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` The lead, the answers, the consent record, the redirect, the revision, the activity entry are real rows in `postgres`. `src: Deployment contract No mocks`
- [ ] `C-DC-16` `contract` The acknowledgement is a real message on the mail server rather than a confirmation the application draws. `src: Deployment contract No mocks`

## Pinned literals

| Value | What the instruction calls it | Item |
|---|---|---|
| `editor@example.com` | the first seeded editor | `C-RL-12` |
| `editor2@example.com` | the second seeded editor | `C-RL-12` |
| `commercial@example.com` | the first seeded commercial account | `C-RL-12` |
| `commercial2@example.com` | the second seeded commercial account | `C-RL-12` |
| `deku-demo-pw-2026` | the corpus password | `C-RL-13` |
| `/app/USER_README.md` | the credentials file | `C-DC-05` |
| `Cette page n'existe pas encore en anglais` | the French unavailability line | `C-CF-14` |
| `not available in French yet` | the English unavailability line | `C-CF-15` |
| `Direction artistique` | the first French facet label | `C-CF-23` |
| `Experience digitale` | the second French facet label | `C-CF-23` |
| `Site vitrine` | the third French facet label | `C-CF-23` |
| `E-commerce` | the fourth French facet label | `C-CF-23` |
| `art_direction` | the first discipline value | `C-CF-29` |
| `digital_experience` | the second discipline value | `C-CF-29` |
| `showcase_site` | the third discipline value | `C-CF-29` |
| `commerce` | the fourth discipline value | `C-CF-29` |
| `any` | the permissive filter mode | `C-CF-30` |
| `all` | the strict filter mode | `C-CF-30` |
| `Tout effacer` | the French clear control | `C-CF-27` |
| `Clear all` | the English clear control | `C-CF-27` |
| `Aucun projet ne correspond` | the empty-filter panel title | `C-CF-33` |
| `Bientot` | the nothing-published panel title | `C-CF-34` |
| `Les projets arrivent. En attendant, parlons du votre.` | the nothing-published panel body | `C-CF-34` |
| `Webframe` | the first award body | `C-CF-55` |
| `DDA` | the second award body | `C-CF-55` |
| `Site Of The Month` | the first award row title | `C-CF-56` |
| `Site Of The Day` | the second award row title | `C-CF-56` |
| `Developer Award` | the third award row title | `C-CF-56` |
| `Un projet` | the first contact entry card | `C-CF-62` |
| `Candidature` | the second contact entry card | `C-CF-62` |
| `En savoir plus` | the third contact entry card | `C-CF-62` |
| `contact@example.com` | the studio contact address | `C-CF-64` |
| `jobs@example.com` | the studio jobs address | `C-CF-64` |
| `Cette page a ete retiree volontairement.` | the gone copy | `C-CF-83` |
| `Retour` | the funnel back control | `C-CF-88` |
| `Continuer` | the funnel continue control | `C-CF-88` |
| `Envoyer` | the funnel send control | `C-CF-88` |
| `Envoi en cours` | the funnel sending state | `C-CF-88` |
| `Cette reponse est necessaire pour continuer.` | the required-answer message | `C-CF-91` |
| `Je ne sais pas encore` | the budget escape answer | `C-CF-93` |
| `Nous avons bien recu votre demande` | the project acknowledgement subject phrase | `C-CF-99` |
| `Votre candidature est bien arrivee` | the application acknowledgement subject phrase | `C-CF-100` |
| `VRS-` | the reference prefix | `C-CF-101` |
| `C'est envoye` | the confirmation heading | `C-CF-104` |
| `Suite a votre candidature` | the application outcome subject phrase | `C-CF-125` |
| `Cette page n'existe pas, ou plus. Voici trois choses qui existent.` | the French not-found body | `C-CF-143` |
| `Quelque chose a casse de notre cote. Nous sommes prevenus.` | the server-failure body | `C-CF-145` |
| `Agence web Ghent : creation de site internet et design graphique` | the French home title | `C-CF-147` |
| `maison-carre` | the first seeded French slug | `C-DM-11` |
| `atelier-brune` | the second seeded French slug | `C-DM-11` |
| `port-neuf` | the third seeded French slug | `C-DM-11` |
| `serre-verte` | the fourth seeded French slug | `C-DM-11` |
| `lune-basse` | the fifth seeded French slug | `C-DM-11` |
| `quai-douze` | the sixth seeded French slug | `C-DM-11` |
| `carre-house` | the first seeded English slug | `C-DM-12` |
| `brune-studio` | the second seeded English slug | `C-DM-12` |
| `new-harbour` | the third seeded English slug | `C-DM-12` |
| `green-glasshouse` | the fourth seeded English slug | `C-DM-12` |
| `low-moon` | the fifth seeded English slug | `C-DM-12` |
| `5` | the French catalogue total | `C-DM-13` |
| `9` | the sum of the four French facet counts | `C-DM-13` |
| `4173` | the container-internal port | `C-DC-01` |
| `200` | the health status | `C-DC-03` |
| `0.0.0.0` | the bind address | `C-DC-09` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the response-time commitment per branch | `C-CF-104` |
| the retention period the acknowledgement names | `C-CF-102` |
| the edit-lock warning threshold | `C-CF-77` |
| the minimum window height the pinned sequence needs | `C-CF-52` |
| the frame rate below which the sequence unpins | `C-CF-53` |
| the studio's working hours | `C-CF-114` |

## Coverage ledger

| Section | Obligation sentences | Items |
|---|---|---|
| Overview | 4 | 4 |
| User roles | 4 | 13 |
| Core features | 123 | 150 |
| User flow | 6 | 9 |
| UI and UX notes | 12 | 18 |
| Technical requirements | 12 | 14 |
| Data model | 10 | 15 |
| Front-end specification | 11 | 14 |
| Constraints | 4 | 6 |
| Deployment contract | 13 | 16 |
