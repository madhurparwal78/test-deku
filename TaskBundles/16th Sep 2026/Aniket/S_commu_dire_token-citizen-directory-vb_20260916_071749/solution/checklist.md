# Checklist: Keepers of the Reach

Items: 320
Unpinned values flagged: 8
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-1` `capability` The site carries a scroll driven story route as its landing surface `src: Overview p1`
- [ ] `C-OV-2` `capability` The site carries a catalogue of every Keeper filterable by visual trait `src: Overview p1`
- [ ] `C-OV-3` `capability` The site carries a membership directory of citizen pages `src: Overview p1`
- [ ] `C-OV-4` `capability` The site carries an editorial journal in four categories `src: Overview p1`
- [ ] `C-OV-5` `capability` The site carries a downloadable press library `src: Overview p1`
- [ ] `C-OV-6` `constraint` The application carries no administrator role inside the interface `src: Overview p3`
- [ ] `C-OV-7` `constraint` An account writes only to the citizen record whose address the account bound `src: Overview p3`
- [ ] `C-OV-8` `constraint` The mint route issues no Keeper `src: Overview p4`
- [ ] `C-OV-9` `constraint` The product carries no payment surface `src: Overview p4`
- [ ] `C-OV-10` `constraint` The product carries no social graph between citizens `src: Overview p4`

## C-RL User roles

- [ ] `C-RL-1` `role` A visitor with no account reads the story route `src: User roles table`
- [ ] `C-RL-2` `role` A visitor with no account reads the catalogue route `src: User roles table`
- [ ] `C-RL-3` `role` A visitor with no account reads any citizen public field `src: User roles table`
- [ ] `C-RL-4` `role` A visitor cannot read any citizen passport document `src: User roles table`
- [ ] `C-RL-5` `role` A visitor cannot write to any citizen record `src: User roles table`
- [ ] `C-RL-6` `role` An account requests a binding challenge over an address `src: User roles table`
- [ ] `C-RL-7` `role` An account cannot bind an address another account already bound `src: User roles table`
- [ ] `C-RL-8` `role` A citizen reads their own passport documents `src: User roles table`
- [ ] `C-RL-9` `role` A citizen edits their own nickname `src: User roles table`
- [ ] `C-RL-10` `role` A citizen edits their own biography `src: User roles table`
- [ ] `C-RL-11` `role` A citizen edits their own representative Keeper `src: User roles table`
- [ ] `C-RL-12` `role` A citizen cannot read another citizen passport document `src: User roles table`
- [ ] `C-RL-13` `role` A citizen cannot write another citizen record `src: User roles table`
- [ ] `C-RL-14` `role` Nobody opens the render harness through the interface `src: User roles permission matrix`
- [ ] `C-RL-15` `constraint` Authorization is decided server-side on every mutating endpoint `src: User roles authorization paragraph`
- [ ] `C-RL-16` `constraint` Authorization is never inferred from a path parameter `src: User roles authorization paragraph`
- [ ] `C-RL-17` `constraint` Signup is open to anybody with an email address `src: User roles signup policy`
- [ ] `C-RL-18` `literal` Every seeded account signs in with the password `deku-demo-pw-2026` `src: User roles seeded table`
- [ ] `C-RL-19` `literal` The first seeded account is `member@example.com` `src: User roles seeded table`
- [ ] `C-RL-20` `literal` The second seeded account is `member2@example.com` `src: User roles seeded table`
- [ ] `C-RL-21` `literal` The third seeded account is `member3@example.com` `src: User roles seeded table`

## C-CF Core features

- [ ] `C-CF-1` `capability` A successful sign in returns a bearer token `src: Core features auth rule 2`
- [ ] `C-CF-2` `contract` The bearer token travels in the Authorization header `src: Core features auth rule 2`
- [ ] `C-CF-3` `constraint` An expired bearer token is denied `src: Core features auth rule 2`
- [ ] `C-CF-4` `constraint` Passwords are stored hashed `src: Core features auth rule 1`
- [ ] `C-CF-5` `constraint` A duplicate signup email is refused as invalid `src: Core features auth rule 1`
- [ ] `C-CF-6` `constraint` A duplicate signup refusal names the email field `src: Core features auth rule 1`
- [ ] `C-CF-7` `constraint` A stored email resolves whatever case the sign in uses `src: Core features auth rule 1`
- [ ] `C-CF-8` `constraint` A wrong password is refused as a client error `src: Core features auth rule 2`
- [ ] `C-CF-9` `constraint` A form carrying a filled unattended decoy field is refused `src: Core features auth rule 4`
- [ ] `C-CF-10` `constraint` A form submitted repeatedly in quick succession from one source is refused `src: Core features auth rule 4`
- [ ] `C-CF-11` `constraint` A refused automated submission writes nothing `src: Core features auth rule 4`
- [ ] `C-CF-12` `capability` The challenge operation returns a statement over one address `src: Core features binding rule 1`
- [ ] `C-CF-13` `data` The challenge response carries a nonce issued by the server `src: Core features binding rule 1`
- [ ] `C-CF-14` `data` The challenge response carries an expiry timestamp `src: Core features binding rule 1`
- [ ] `C-CF-15` `data` The returned statement names the address being claimed `src: Core features binding rule 2`
- [ ] `C-CF-16` `capability` Returning the nonce binds the address to the calling account `src: Core features binding rule 3`
- [ ] `C-CF-17` `constraint` The binding decision is taken on the server `src: Core features binding rule 3`
- [ ] `C-CF-18` `constraint` A consumed nonce presented a second time is refused as gone `src: Core features binding rule 4`
- [ ] `C-CF-19` `constraint` An invented nonce is refused `src: Core features binding rule 4`
- [ ] `C-CF-20` `constraint` A nonce issued over one address presented against another is refused `src: Core features binding rule 4`
- [ ] `C-CF-21` `constraint` An address already bound elsewhere is refused as unavailable `src: Core features binding rule 6`
- [ ] `C-CF-22` `constraint` Two spellings of one address differing only in case resolve to one citizen `src: Core features binding rule 7`
- [ ] `C-CF-23` `constraint` An address outside the hexadecimal form is refused before any lookup `src: Core features binding rule 8`
- [ ] `C-CF-24` `capability` The catalogue index is published to the object store as one packed document `src: Core features catalogue rule 1`
- [ ] `C-CF-25` `data` The packed index carries a trait header listing every facet value once `src: Core features catalogue rule 1`
- [ ] `C-CF-26` `literal` The collection holds `10000` Keepers `src: Core features catalogue rule 2`
- [ ] `C-CF-27` `literal` The collection carries `13` traits `src: Core features catalogue rule 2`
- [ ] `C-CF-28` `data` The packed header gives each of the thirteen facets its pinned value count `src: Core features catalogue rule 2`
- [ ] `C-CF-29` `data` The seeded token table holds ten thousand rows `src: Core features catalogue rule 2`
- [ ] `C-CF-30` `data` The seeded trait table names every one of the thirteen facets `src: Core features catalogue rule 2`
- [ ] `C-CF-31` `literal` A grid thumbnail is addressed at `thumbs/<digest>.png` `src: Core features catalogue rule 3`
- [ ] `C-CF-32` `literal` A detail image is addressed at `images/<digest>.png` `src: Core features catalogue rule 3`
- [ ] `C-CF-33` `literal` A full bleed image is addressed at `images_fullbleed/<digest>.png` `src: Core features catalogue rule 3`
- [ ] `C-CF-34` `literal` The display index differs from the on-chain identifier by the shift `5022` `src: Core features catalogue rule 4`
- [ ] `C-CF-35` `data` Display index zero resolves to on-chain identifier `4978` `src: Core features catalogue rule 4`
- [ ] `C-CF-36` `data` Display index `5021` resolves to on-chain identifier `9999` `src: Core features catalogue rule 4`
- [ ] `C-CF-37` `data` The last display index in the range resolves to on-chain identifier `4977` `src: Core features catalogue rule 4`
- [ ] `C-CF-38` `constraint` A shift below zero wraps to the top of the range `src: Core features catalogue rule 4`
- [ ] `C-CF-39` `capability` Several values chosen inside one facet form a union `src: Core features catalogue rule 5`
- [ ] `C-CF-40` `capability` Values chosen across two facets form an intersection `src: Core features catalogue rule 5`
- [ ] `C-CF-41` `ui` The result count changes as facet values are chosen `src: Core features catalogue rule 5`
- [ ] `C-CF-42` `ui` The detail overlay shows both identifier forms `src: Core features catalogue rule 10`
- [ ] `C-CF-43` `ui` The detail overlay links to the licence route `src: Core features catalogue rule 10`
- [ ] `C-CF-44` `ui` The escape key closes the detail overlay `src: Core features catalogue rule 10`
- [ ] `C-CF-45` `ui` The holdings view with no address bound shows a connect prompt in place of results `src: Core features catalogue rule 9`
- [ ] `C-CF-46` `capability` The standalone filter route serves as the narrow width drill down target `src: Core features filters rule 1`
- [ ] `C-CF-47` `constraint` The facet selection lives in the address bar `src: Core features filters rule 2`
- [ ] `C-CF-48` `ui` A facet value with a zero count renders disabled rather than hidden `src: Core features filters rule 5`
- [ ] `C-CF-49` `contract` A citizen page is addressed by the bound address `src: Core features directory rule 1`
- [ ] `C-CF-50` `constraint` The address in the path is matched case insensitively `src: Core features directory rule 1`
- [ ] `C-CF-51` `data` The citizen record carries the nickname, the biography, the representative Keeper `src: Core features directory rule 2`
- [ ] `C-CF-52` `data` The citizen record carries the holdings `src: Core features directory rule 2`
- [ ] `C-CF-53` `data` The citizen record carries the earned achievements `src: Core features directory rule 2`
- [ ] `C-CF-54` `constraint` The renders key is absent from a non-owner response `src: Core features directory rule 3`
- [ ] `C-CF-55` `constraint` An address with no citizen record answers not found `src: Core features directory rule 4`
- [ ] `C-CF-56` `ui` The citizen page takes its surface colours from the representative Keeper background colour `src: Core features directory rule 5`
- [ ] `C-CF-57` `constraint` The derived colour scheme is computed rather than stored `src: Core features directory rule 5`
- [ ] `C-CF-58` `ui` A trait absent from the representative Keeper renders as a dash `src: Core features directory rule 7`
- [ ] `C-CF-59` `ui` An unearned achievement is listed rather than hidden `src: Core features directory rule 8`
- [ ] `C-CF-60` `constraint` The citizen statistics are derived rather than stored `src: Core features directory rule 9`
- [ ] `C-CF-61` `constraint` Editing is available to the owner of the bound address alone `src: Core features directory rule 10`
- [ ] `C-CF-62` `ui` An edit affordance is absent from a non-owner citizen page `src: Core features directory rule 10`
- [ ] `C-CF-63` `constraint` A nickname shorter than three characters is refused `src: Core features directory rule 11`
- [ ] `C-CF-64` `literal` A nickname longer than `24` characters is refused `src: Core features directory rule 11`
- [ ] `C-CF-65` `constraint` A nickname carrying a leading space is refused `src: Core features directory rule 11`
- [ ] `C-CF-66` `literal` A biography longer than `280` characters is refused `src: Core features directory rule 11`
- [ ] `C-CF-67` `constraint` The representative Keeper is revalidated against the holdings ledger at write time `src: Core features directory rule 11`
- [ ] `C-CF-68` `constraint` Every field rule is enforced on the server rather than in the form alone `src: Core features directory rule 11`
- [ ] `C-CF-69` `constraint` Two simultaneous claims of one nickname accept at most one `src: Core features directory rule 12`
- [ ] `C-CF-70` `constraint` A refused nickname claim writes nothing `src: Core features directory rule 12`
- [ ] `C-CF-71` `constraint` An omitted field leaves the stored value alone `src: Core features directory rule 13`
- [ ] `C-CF-72` `constraint` An explicit null clears the stored field `src: Core features directory rule 13`
- [ ] `C-CF-73` `constraint` A refused write names the offending field in the response `src: Core features directory rule 14`
- [ ] `C-CF-74` `constraint` A refused write leaves the stored record unchanged `src: Core features directory rule 14`
- [ ] `C-CF-75` `literal` The three passport faces are `document_front`, `document_back`, `share_image` `src: Core features passport rule 1`
- [ ] `C-CF-76` `constraint` A passport face is written to the object store by the server `src: Core features passport rule 1`
- [ ] `C-CF-77` `constraint` Passport bytes are never kept on the application filesystem `src: Core features passport rule 1`
- [ ] `C-CF-78` `literal` A passport object key follows `citizens/<address_lower>/<face>/<content_hash>.png` `src: Core features passport rule 2`
- [ ] `C-CF-79` `constraint` The passport key address segment is the lowercased spelling `src: Core features passport rule 2`
- [ ] `C-CF-80` `data` The content hash covers the nickname, the biography, the representative Keeper `src: Core features passport rule 3`
- [ ] `C-CF-81` `constraint` A generation run whose computed hash equals the stored hash produces nothing `src: Core features passport rule 3`
- [ ] `C-CF-82` `capability` Generation runs outside the request path `src: Core features passport rule 4`
- [ ] `C-CF-83` `data` A passport face reports a state of pending, ready, failed `src: Core features passport rule 4`
- [ ] `C-CF-84` `data` The render state response carries a suggested next poll interval `src: Core features passport rule 4`
- [ ] `C-CF-85` `constraint` A completed run writes a new object key rather than overwriting the previous object `src: Core features passport rule 5`
- [ ] `C-CF-86` `constraint` A regeneration request returns the run in flight rather than starting a second run `src: Core features passport rule 7`
- [ ] `C-CF-87` `ui` A pending face shows the previous document beside a regenerating marker `src: Core features passport rule 8`
- [ ] `C-CF-88` `constraint` A passport object is never publicly readable from the object store `src: Core features passport rule 9`
- [ ] `C-CF-89` `constraint` A read address for a passport object is minted only for the owner `src: Core features passport rule 9`
- [ ] `C-CF-90` `constraint` A request for another citizen passport document is refused `src: Core features passport rule 9`
- [ ] `C-CF-91` `constraint` A regeneration request from another account is refused `src: Core features passport rule 7`
- [ ] `C-CF-92` `constraint` The render harness refuses without a signed expiring parameter `src: Core features passport rule 10`
- [ ] `C-CF-93` `constraint` The render harness refuses a guessed signature `src: Core features passport rule 10`
- [ ] `C-CF-94` `constraint` No public route links the render harness `src: Core features passport rule 10`
- [ ] `C-CF-95` `constraint` An unpublished achievement appears in no catalogue listing `src: Core features achievements rule 5`
- [ ] `C-CF-96` `constraint` An unpublished achievement appears on no citizen record `src: Core features achievements rule 5`
- [ ] `C-CF-97` `contract` The holdings response names whether a citizen record exists `src: Core features holdings rule 2`
- [ ] `C-CF-98` `data` An address bound but holding nothing answers an empty holdings list `src: Core features holdings rule 2`
- [ ] `C-CF-99` `data` An address nobody has bound reports that no citizen record exists `src: Core features holdings rule 2`
- [ ] `C-CF-100` `constraint` The holdings cache is never the authority for a write `src: Core features holdings rule 4`
- [ ] `C-CF-101` `ui` The story route holds its stage pinned against scroll input `src: Core features story rule 1`
- [ ] `C-CF-102` `ui` The story route opens on a preloader carrying a numeric progress label `src: Core features story rule 2`
- [ ] `C-CF-103` `constraint` The preloader reports real progress against the prefetch byte total `src: Core features story rule 3`
- [ ] `C-CF-104` `constraint` The preloader gives up after ten seconds `src: Core features story rule 4`
- [ ] `C-CF-105` `ui` Choosing a story section scrubs the scroll position rather than jumping `src: Core features story rule 5`
- [ ] `C-CF-106` `ui` The protocol hold control releases when the pointer leaves the window `src: Core features protocol rule 3`
- [ ] `C-CF-107` `ui` The protocol level meter keeps moving under a synthetic envelope when sound is muted `src: Core features protocol rule 4`
- [ ] `C-CF-108` `ui` The protocol hold control works as a keyboard toggle `src: Core features protocol rule 5`
- [ ] `C-CF-109` `literal` The journal carries the category tabs `ALL`, `UPDATES`, `COMMUNITY`, `FINDERS LAB` `src: Core features journal rule 1`
- [ ] `C-CF-110` `constraint` The journal category selection is reflected in the address `src: Core features journal rule 2`
- [ ] `C-CF-111` `constraint` A journal category listing carries only that category `src: Core features journal rule 2`
- [ ] `C-CF-112` `contract` A journal entry is addressed by slug `src: Core features journal rule 3`
- [ ] `C-CF-113` `constraint` A journal body is rendered through a node resolver rather than as raw markup `src: Core features journal rule 4`
- [ ] `C-CF-114` `data` The resolver handles paragraph, heading, list, quote, link, image, video, rule, code `src: Core features journal rule 4`
- [ ] `C-CF-115` `constraint` A link is classified by the recorded link type rather than by inspecting the address `src: Core features journal rule 5`
- [ ] `C-CF-116` `constraint` A draft entry is reachable only through a non-default preview mode `src: Core features journal rule 6`
- [ ] `C-CF-117` `literal` The seeded media library holds `71` items `src: Core features media rule 1`
- [ ] `C-CF-118` `literal` The seeded media library holds `31` images `src: Core features media rule 1`
- [ ] `C-CF-119` `literal` The seeded media library holds `34` videos `src: Core features media rule 1`
- [ ] `C-CF-120` `data` The three media type counts sum to the total count `src: Core features media rule 1`
- [ ] `C-CF-121` `ui` Each media type filter shows a live count `src: Core features media rule 1`
- [ ] `C-CF-122` `constraint` The media listing exposes no bucket path `src: Core features media rule 4`
- [ ] `C-CF-123` `constraint` A download address is minted per request `src: Core features media rule 4`
- [ ] `C-CF-124` `constraint` A download address is minted on activation rather than on selection `src: Core features media rule 4`
- [ ] `C-CF-125` `data` The about roster is seeded content rather than hard coded markup `src: Core features about rule 4`
- [ ] `C-CF-126` `constraint` The roster index number is assigned by position rather than stored `src: Core features about rule 4`
- [ ] `C-CF-127` `capability` The privacy route names every stored citizen field `src: Core features legal rule 2`
- [ ] `C-CF-128` `constraint` The privacy route is reachable from the footer of every page `src: Core features legal rule 2`
- [ ] `C-CF-129` `constraint` The licence route is linked from every catalogue detail overlay `src: Core features legal rule 3`
- [ ] `C-CF-130` `ui` The backtick key toggles the console overlay `src: Core features console rule 1`
- [ ] `C-CF-131` `data` The console command set is seeded content rather than compiled in `src: Core features console rule 3`
- [ ] `C-CF-132` `literal` The seeded internal console command is `connect_citizens` `src: Core features console rule 4`
- [ ] `C-CF-133` `constraint` Console input is echoed as text rather than as markup `src: Core features console rule 5`
- [ ] `C-CF-134` `ui` The mint route presents a closed state rather than a server error `src: Core features mint route`
- [ ] `C-CF-135` `literal` The registration route title reads `THE HOLD CITIZEN BUREAU` `src: Core features registration rule 1`
- [ ] `C-CF-136` `constraint` The registration diagnostic column is hidden from assistive technology `src: Core features registration rule 2`
- [ ] `C-CF-137` `ui` A bound address holding nothing is presented as a legitimate end state `src: Core features registration rule 4`
- [ ] `C-CF-138` `constraint` Switching account with a citizen page open discards every private field on screen `src: Core features registration rule 5`

## C-UF User flow

- [ ] `C-UF-1` `contract` The story route is served at the site root `src: User flow route table`
- [ ] `C-UF-2` `contract` The catalogue is served at `/gallery` `src: User flow route table`
- [ ] `C-UF-3` `contract` The standalone facet panel is served at `/filters` `src: User flow route table`
- [ ] `C-UF-4` `contract` The journal index is served at `/journal` `src: User flow route table`
- [ ] `C-UF-5` `contract` The media library is served at `/media` `src: User flow route table`
- [ ] `C-UF-6` `contract` The roster route is served at `/about` `src: User flow route table`
- [ ] `C-UF-7` `contract` The protocol statement is served at `/protocol` `src: User flow route table`
- [ ] `C-UF-8` `contract` The licence document is served at `/legal/legal-license` `src: User flow route table`
- [ ] `C-UF-9` `contract` The privacy document is served at `/legal/privacy-policy` `src: User flow route table`
- [ ] `C-UF-10` `contract` The operator harness is served at `/render-asset` `src: User flow route table`
- [ ] `C-UF-11` `constraint` An unauthenticated visitor opening the binding route is sent to the sign-in route `src: User flow entry and redirects`
- [ ] `C-UF-12` `constraint` Signing out revokes the bearer token on the server `src: User flow entry and redirects`
- [ ] `C-UF-13` `contract` An unknown address answers not found `src: User flow entry and redirects`
- [ ] `C-UF-14` `ui` The not-found page offers a way back `src: User flow entry and redirects`
- [ ] `C-UF-15` `literal` The catalogue count reads `10000 KEEPERS` `src: User flow journey browse and filter`
- [ ] `C-UF-16` `literal` The whole-collection tab reads `KEEPERS COLLECTION` `src: User flow journey browse and filter`
- [ ] `C-UF-17` `literal` The holdings tab reads `MY COLLECTION` `src: User flow journey browse and filter`
- [ ] `C-UF-18` `capability` A new account binds an address then lands on the citizen page `src: User flow journey bind an address`
- [ ] `C-UF-19` `ui` A saved nickname appears in the citizen record at once `src: User flow journey edit a citizen page`
- [ ] `C-UF-20` `ui` A refused save puts the previous nickname back beside the reason `src: User flow journey edit a citizen page`
- [ ] `C-UF-21` `constraint` Saving an identical value queues no new generation run `src: User flow journey edit a citizen page`
- [ ] `C-UF-22` `constraint` A refused cross-account write leaves the target row unchanged `src: User flow journey the boundary`
- [ ] `C-UF-23` `constraint` A refused cross-account write is recorded in the audit trail `src: User flow journey the boundary`
- [ ] `C-UF-24` `ui` Every list carries a named empty state `src: User flow states`

## C-UX UI and UX notes

- [ ] `C-UX-1` `ui` The first screen reads as a technical document rather than a marketing page `src: UI/UX notes north star`
- [ ] `C-UX-2` `ui` Resizing the window rescales the whole interface proportionally `src: UI/UX notes scaling paragraph`
- [ ] `C-UX-3` `ui` One accent colour marks anything live or selected `src: UI/UX notes palette paragraph`
- [ ] `C-UX-4` `ui` The accent colour appears nowhere except live or selected states `src: UI/UX notes palette paragraph`
- [ ] `C-UX-5` `ui` One control dropped on the dark field, then on the light field, inverts its ink colour `src: UI/UX notes palette paragraph`
- [ ] `C-UX-6` `ui` Monospace figures line up in a column wherever numbers stack `src: UI/UX notes typography paragraph`
- [ ] `C-UX-7` `ui` The corner cut appears on every button, every panel, the console window `src: UI/UX notes shape paragraph`
- [ ] `C-UX-8` `ui` The corner cut is generated from parameters rather than drawn as an image `src: UI/UX notes shape paragraph`
- [ ] `C-UX-9` `ui` Space is made by leaving grid columns empty rather than by adding a gutter `src: UI/UX notes density paragraph`
- [ ] `C-UX-10` `ui` Every motion in the product shares one family of curves `src: UI/UX notes motion paragraph`
- [ ] `C-UX-11` `ui` A link hover panel travels one direction rather than reversing `src: UI/UX notes named moments`
- [ ] `C-UX-12` `ui` Sound is off on arrival `src: UI/UX notes reduced motion paragraph`
- [ ] `C-UX-13` `ui` A visible focus indicator appears on every focusable element `src: UI/UX notes accessibility paragraph`
- [ ] `C-UX-14` `ui` Nothing overflows sideways at a narrow viewport `src: UI/UX notes responsive paragraph`
- [ ] `C-UX-15` `ui` Each page leads with one primary action distinct from every secondary one `src: UI/UX notes primary action paragraph`

## C-TR Technical requirements

- [ ] `C-TR-1` `contract` The frontend is built for production then served by a static or preview server `src: Technical requirements stack paragraph`
- [ ] `C-TR-2` `contract` The HTTP interface is served under the `/api` prefix on the site origin `src: Technical requirements stack paragraph`
- [ ] `C-TR-3` `literal` The datastore connection is read from `DATABASE_URL` `src: Technical requirements stack paragraph`
- [ ] `C-TR-4` `literal` The object store address is read from `STORAGE_ENDPOINT` `src: Technical requirements stack paragraph`
- [ ] `C-TR-5` `literal` The object store bucket is read from `STORAGE_BUCKET` `src: Technical requirements stack paragraph`
- [ ] `C-TR-6` `literal` The object store key is read from `STORAGE_ACCESS_KEY` `src: Technical requirements stack paragraph`
- [ ] `C-TR-7` `literal` The object store secret is read from `STORAGE_SECRET_KEY` `src: Technical requirements stack paragraph`
- [ ] `C-TR-8` `literal` The public origin is read from `APP_PUBLIC_URL` `src: Technical requirements stack paragraph`
- [ ] `C-TR-9` `constraint` No host or port is hardcoded `src: Technical requirements stack paragraph`
- [ ] `C-TR-10` `contract` The health endpoint answers `200` once the app is ready `src: Technical requirements stack paragraph`
- [ ] `C-TR-11` `constraint` No second datastore, cache, queue, object store, mail vendor is introduced `src: Technical requirements library paragraph`
- [ ] `C-TR-12` `constraint` Every public route carries a distinct title `src: Technical requirements route metadata`
- [ ] `C-TR-13` `constraint` Every public route carries a distinct description `src: Technical requirements route metadata`
- [ ] `C-TR-14` `constraint` Landing on a deep address returns the same page as navigating to the address `src: Technical requirements route metadata`
- [ ] `C-TR-15` `constraint` A content addressed object carries an immutable long lived cache directive `src: Technical requirements delivery paths`
- [ ] `C-TR-16` `constraint` A response carrying citizen data carries no cacheable directive `src: Technical requirements delivery paths`
- [ ] `C-TR-17` `constraint` The packed index is fetched once per session `src: Technical requirements packed index`
- [ ] `C-TR-18` `constraint` Parsing the packed index never blocks the interface `src: Technical requirements packed index`
- [ ] `C-TR-19` `constraint` No credential appears in anything the browser downloads `src: Technical requirements secrets paragraph`
- [ ] `C-TR-20` `constraint` The object store credentials stay in the server environment `src: Technical requirements secrets paragraph`
- [ ] `C-TR-21` `data` Every request carries a request identifier echoed in the response `src: Technical requirements interface conventions`
- [ ] `C-TR-22` `constraint` A repeated idempotency key returns the first response `src: Technical requirements interface conventions`
- [ ] `C-TR-23` `data` One structured log line per request carries the identifier, route, status, duration `src: Technical requirements instrumentation`
- [ ] `C-TR-24` `constraint` A nickname never appears in a log line `src: Technical requirements instrumentation`
- [ ] `C-TR-25` `data` An error response carries a stable machine readable code `src: Technical requirements instrumentation`
- [ ] `C-TR-26` `constraint` Regeneration is limited per citizen per day `src: Technical requirements rate limits`
- [ ] `C-TR-27` `capability` The degradation ladder runs from full through reduced, still, flat, document `src: Technical requirements degradation`
- [ ] `C-TR-28` `constraint` The catalogue stays readable in every failure mode `src: Technical requirements failure behaviour`
- [ ] `C-TR-29` `constraint` Browser storage holds preferences rather than a token or an address `src: Technical requirements failure behaviour`
- [ ] `C-TR-30` `constraint` No binary asset is required for the build to run `src: Technical requirements assets`
- [ ] `C-TR-31` `capability` Keeper artwork is produced by a deterministic generator keyed by content digest `src: Technical requirements assets`
- [ ] `C-TR-32` `constraint` The same digest always produces the same generated picture `src: Technical requirements assets`
- [ ] `C-TR-33` `constraint` Icons ship as inline vector geometry rather than as a sprite sheet `src: Technical requirements assets`
- [ ] `C-TR-34` `constraint` A malformed address parameter fails closed `src: Technical requirements input handling`
- [ ] `C-TR-35` `constraint` A signed parameter is validated before any work is done `src: Technical requirements input handling`
- [ ] `C-TR-36` `constraint` A stored nickname is escaped at render rather than interpolated into markup `src: Technical requirements input handling`

## C-DM Data model

- [ ] `C-DM-1` `data` Every timestamp is recorded in UTC `src: Data model opening paragraph`
- [ ] `C-DM-2` `data` The citizen table keys on the address in the display spelling `src: Data model citizen`
- [ ] `C-DM-3` `constraint` Citizen lookup happens on the lowercase address column `src: Data model citizen`
- [ ] `C-DM-4` `constraint` One account binds at most one address `src: Data model citizen`
- [ ] `C-DM-5` `constraint` One address is bound by at most one account `src: Data model citizen`
- [ ] `C-DM-6` `data` The profile carries a normalised nickname column `src: Data model profile`
- [ ] `C-DM-7` `constraint` Two citizens cannot hold the same normalised nickname at once `src: Data model profile`
- [ ] `C-DM-8` `constraint` A citizen who never set a nickname collides with nobody `src: Data model profile`
- [ ] `C-DM-9` `data` The render row keys on the address beside the face `src: Data model render`
- [ ] `C-DM-10` `data` The render row stores a content hash of the generation inputs `src: Data model render`
- [ ] `C-DM-11` `data` An achievement carries a point value greater than zero `src: Data model achievement`
- [ ] `C-DM-12` `data` An unpublished achievement carries a null publication timestamp `src: Data model achievement`
- [ ] `C-DM-13` `constraint` The award table keys on the address beside the achievement identifier `src: Data model citizen_achievement`
- [ ] `C-DM-14` `constraint` The holdings ledger is the authority for ownership `src: Data model holding_ledger`
- [ ] `C-DM-15` `data` A Keeper stores a background colour driving the derived citizen palette `src: Data model token`
- [ ] `C-DM-16` `constraint` A Keeper carries at most one value per trait `src: Data model token_trait_value`
- [ ] `C-DM-17` `data` A challenge row carries a consumption timestamp `src: Data model session_challenge`
- [ ] `C-DM-18` `constraint` A consumed challenge row can never be consumed again `src: Data model session_challenge`
- [ ] `C-DM-19` `constraint` An audit row is written in the same transaction as the change the row records `src: Data model audit_log`
- [ ] `C-DM-20` `constraint` The audit table is append only for the application role `src: Data model audit_log`
- [ ] `C-DM-21` `data` The citizen point total is derived rather than stored `src: Data model derived rather than stored`
- [ ] `C-DM-22` `data` The media type counts are derived rather than stored `src: Data model derived rather than stored`
- [ ] `C-DM-23` `literal` The first seeded bound address is `0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801` `src: Data model seed data`
- [ ] `C-DM-24` `literal` The second seeded bound address is `0xB2c4E5d6F7a8B9c0D1e2F3a4B5c6D7e8F9a0B102` `src: Data model seed data`
- [ ] `C-DM-25` `literal` The seeded address holding nothing is `0xC3d5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1D203` `src: Data model seed data`
- [ ] `C-DM-26` `data` The seed holds eight achievements across three sectors `src: Data model seed data`
- [ ] `C-DM-27` `data` The seed leaves one achievement unpublished `src: Data model seed data`
- [ ] `C-DM-28` `constraint` Seeding is idempotent across a restart `src: Data model seed data`

## C-FE Front-end specification

- [ ] `C-FE-1` `ui` The persistent frame does not unmount on navigation `src: Front-end specification the frame`
- [ ] `C-FE-2` `ui` The burger carries two horizontal strokes of unequal length `src: Front-end specification the burger`
- [ ] `C-FE-3` `ui` The open menu traps focus inside the menu `src: Front-end specification the burger`
- [ ] `C-FE-4` `literal` The story submenu reads `Project`, `The Hold`, `Factions`, `The World` `src: Front-end specification route submenu`
- [ ] `C-FE-5` `literal` The protocol submenu reads `VISION`, `WORLD`, `CHARACTERS`, `PORTAL`, `UNION` `src: Front-end specification route submenu`
- [ ] `C-FE-6` `literal` The signed-out action slot reads `SIGN IN` `src: Front-end specification action slot`
- [ ] `C-FE-7` `literal` The unbound action slot reads `CONNECT WALLET` `src: Front-end specification action slot`
- [ ] `C-FE-8` `literal` The bound action slot offers `DISCONNECT` `src: Front-end specification action slot`
- [ ] `C-FE-9` `literal` The muted audio control reads `CLICK TO ENABLE SOUND` `src: Front-end specification audio control`
- [ ] `C-FE-10` `literal` The footer credit reads `SITE BY Studio North` `src: Front-end specification footer`
- [ ] `C-FE-11` `literal` The footer rights line reads `KEEPERS OF THE REACH. ALL RIGHTS RESERVED.` `src: Front-end specification footer`
- [ ] `C-FE-12` `ui` An unearned achievement mark shows the ring shrunk inside the resting position `src: Front-end specification iconography`
- [ ] `C-FE-13` `ui` The console window carries two cut corners of different sizes `src: Front-end specification iconography`
- [ ] `C-FE-14` `ui` At a narrow width the story route becomes an ordinary scrolling document `src: Front-end specification scroll system`
- [ ] `C-FE-15` `ui` The audio control shows a four-bar level meter beside its label `src: Front-end specification scene layer`
- [ ] `C-FE-16` `ui` One travelling band carries the entire about route motion `src: Front-end specification scene layer`
- [ ] `C-FE-17` `ui` The about roster alternates cards with empty cells crossed by diagonal hairlines `src: Front-end specification card mask`
- [ ] `C-FE-18` `ui` The narrow catalogue moves the facets to the standalone filter route `src: Front-end specification responsive table`

## C-CN Constraints

- [ ] `C-CN-1` `constraint` The product carries one collection of ten thousand Keepers `src: Constraints list`
- [ ] `C-CN-2` `constraint` The product carries no editor surface inside the application `src: Constraints list`
- [ ] `C-CN-3` `constraint` The product sends no outbound email `src: Constraints list`
- [ ] `C-CN-4` `constraint` The product makes no run-time network call beyond the datastore, the object store `src: Constraints list`
- [ ] `C-CN-5` `constraint` A nickname never leaves the product `src: Constraints list`
- [ ] `C-CN-6` `constraint` The catalogue route stays usable at ten thousand Keepers `src: Constraints list`

## C-DC Deployment contract

- [ ] `C-DC-1` `contract` The app is reachable at the public origin variable `src: Deployment contract line 1`
- [ ] `C-DC-2` `literal` The container-internal port is `4173` `src: Deployment contract line 1`
- [ ] `C-DC-3` `contract` The HTTP interface is served under the api prefix on the same origin `src: Deployment contract line 2`
- [ ] `C-DC-4` `contract` The health endpoint returns two hundred once ready `src: Deployment contract line 3`
- [ ] `C-DC-5` `constraint` The app starts from the environment image with no manual step `src: Deployment contract line 4`
- [ ] `C-DC-6` `literal` Credentials are written to `/app/USER_README.md` `src: Deployment contract line 5`
- [ ] `C-DC-7` `literal` The reserved screenshot directory `.browser_screenshots/` exists empty at the app root `src: Deployment contract line 6`
- [ ] `C-DC-8` `literal` The reserved download directory `.downloads/` exists empty at the app root `src: Deployment contract line 6`
- [ ] `C-DC-9` `constraint` A production build is served behind a static or preview server `src: Deployment contract line 7`
- [ ] `C-DC-10` `constraint` The server keeps running after the session ends `src: Deployment contract line 8`
- [ ] `C-DC-11` `literal` The server binds `0.0.0.0` `src: Deployment contract line 9`
- [ ] `C-DC-12` `constraint` No backing service is downloaded, installed, started by the app `src: Deployment contract line 10`
- [ ] `C-DC-13` `constraint` No persistent volume, fixed container name, custom network is declared `src: Deployment contract line 12`
- [ ] `C-DC-14` `contract` Every list endpoint returns a top-level JSON array `src: Deployment contract API shapes`
- [ ] `C-DC-15` `contract` An invalid call is refused as a client error rather than a server error `src: Deployment contract API shapes`
- [ ] `C-DC-16` `literal` A missing session answers the code `session_required` `src: Deployment contract API shapes`
- [ ] `C-DC-17` `literal` A cross-account write answers the code `session_address_mismatch` `src: Deployment contract API shapes`
- [ ] `C-DC-18` `literal` An unknown address answers the code `citizen_not_found` `src: Deployment contract API shapes`
- [ ] `C-DC-19` `literal` A taken nickname answers the code `nickname_taken` `src: Deployment contract API shapes`
- [ ] `C-DC-20` `literal` An unowned representative Keeper answers the code `token_not_owned` `src: Deployment contract API shapes`
- [ ] `C-DC-21` `literal` A replayed challenge answers the code `challenge_expired` `src: Deployment contract API shapes`
- [ ] `C-DC-22` `literal` A second regeneration answers the code `render_in_flight` `src: Deployment contract API shapes`
- [ ] `C-DC-23` `constraint` An in-memory stand-in for the object store is a contract violation `src: Deployment contract no mocks`
- [ ] `C-DC-24` `constraint` A public bucket policy standing in for a minted address is a contract violation `src: Deployment contract no mocks`

## Pinned literals

| Value | What it is | Item |
|---|---|---|
| `deku-demo-pw-2026` | the corpus password on every seeded account | `C-RL-18` |
| `member@example.com` | the first seeded account | `C-RL-19` |
| `member2@example.com` | the second seeded account | `C-RL-20` |
| `member3@example.com` | the third seeded account | `C-RL-21` |
| `10000` | the collection size | `C-CF-26` |
| `13` | the trait count | `C-CF-27` |
| `thumbs/<digest>.png` | the grid thumbnail address scheme | `C-CF-31` |
| `images/<digest>.png` | the detail image address scheme | `C-CF-32` |
| `images_fullbleed/<digest>.png` | the full bleed image address scheme | `C-CF-33` |
| `5022` | the identifier shift | `C-CF-34` |
| `4978` | the on-chain identifier for display index zero | `C-CF-35` |
| `5021` | the display index that wraps to the top of the range | `C-CF-36` |
| `9999` | the on-chain identifier that display index five thousand and twenty one resolves to | `C-CF-36` |
| `4977` | the on-chain identifier for the last display index | `C-CF-37` |
| `24` | the nickname length ceiling | `C-CF-64` |
| `280` | the biography length ceiling | `C-CF-66` |
| `document_front` | the first passport face | `C-CF-75` |
| `document_back` | the second passport face | `C-CF-75` |
| `share_image` | the third passport face | `C-CF-75` |
| `citizens/<address_lower>/<face>/<content_hash>.png` | the passport object key scheme | `C-CF-78` |
| `ALL` | the first journal category tab | `C-CF-109` |
| `UPDATES` | the second journal category tab | `C-CF-109` |
| `COMMUNITY` | the third journal category tab | `C-CF-109` |
| `FINDERS LAB` | the fourth journal category tab | `C-CF-109` |
| `71` | the seeded media item total | `C-CF-117` |
| `31` | the seeded media image count | `C-CF-118` |
| `34` | the seeded media video count | `C-CF-119` |
| `connect_citizens` | the seeded internal console command | `C-CF-132` |
| `THE HOLD CITIZEN BUREAU` | the registration route title | `C-CF-135` |
| `/gallery` | the catalogue route | `C-UF-2` |
| `/filters` | the standalone facet route | `C-UF-3` |
| `/journal` | the journal index route | `C-UF-4` |
| `/media` | the media library route | `C-UF-5` |
| `/about` | the roster route | `C-UF-6` |
| `/protocol` | the protocol route | `C-UF-7` |
| `/legal/legal-license` | the licence route | `C-UF-8` |
| `/legal/privacy-policy` | the privacy route | `C-UF-9` |
| `/render-asset` | the operator harness route | `C-UF-10` |
| `10000 KEEPERS` | the catalogue count label | `C-UF-15` |
| `KEEPERS COLLECTION` | the whole-collection tab label | `C-UF-16` |
| `MY COLLECTION` | the holdings tab label | `C-UF-17` |
| `DATABASE_URL` | the datastore connection variable | `C-TR-3` |
| `STORAGE_ENDPOINT` | the object store address variable | `C-TR-4` |
| `STORAGE_BUCKET` | the object store bucket variable | `C-TR-5` |
| `STORAGE_ACCESS_KEY` | the object store access key variable | `C-TR-6` |
| `STORAGE_SECRET_KEY` | the object store secret variable | `C-TR-7` |
| `APP_PUBLIC_URL` | the public origin variable | `C-TR-8` |
| `/api` | the interface prefix | `C-TR-2` |
| `200` | the ready health status | `C-TR-10` |
| `0xA7d3F1b2C4e5D6a7B8c9D0e1F2a3B4c5D6e7F801` | the first seeded bound address | `C-DM-23` |
| `0xB2c4E5d6F7a8B9c0D1e2F3a4B5c6D7e8F9a0B102` | the second seeded bound address | `C-DM-24` |
| `0xC3d5F6a7B8c9D0e1F2a3B4c5D6e7F8a9B0c1D203` | the seeded address holding nothing | `C-DM-25` |
| `Project` | the first story submenu entry | `C-FE-4` |
| `The Hold` | the second story submenu entry | `C-FE-4` |
| `Factions` | the third story submenu entry | `C-FE-4` |
| `The World` | the fourth story submenu entry | `C-FE-4` |
| `VISION` | the first protocol submenu entry | `C-FE-5` |
| `WORLD` | the second protocol submenu entry | `C-FE-5` |
| `CHARACTERS` | the third protocol submenu entry | `C-FE-5` |
| `PORTAL` | the fourth protocol submenu entry | `C-FE-5` |
| `UNION` | the fifth protocol submenu entry | `C-FE-5` |
| `SIGN IN` | the signed-out action slot label | `C-FE-6` |
| `CONNECT WALLET` | the unbound action slot label | `C-FE-7` |
| `DISCONNECT` | the bound action slot control | `C-FE-8` |
| `CLICK TO ENABLE SOUND` | the muted audio control label | `C-FE-9` |
| `SITE BY Studio North` | the footer studio credit | `C-FE-10` |
| `KEEPERS OF THE REACH. ALL RIGHTS RESERVED.` | the footer rights line | `C-FE-11` |
| `4173` | the container-internal port | `C-DC-2` |
| `/app/USER_README.md` | the credential file path | `C-DC-6` |
| `.browser_screenshots/` | the reserved screenshot directory | `C-DC-7` |
| `.downloads/` | the reserved download directory | `C-DC-8` |
| `0.0.0.0` | the bind address | `C-DC-11` |
| `session_required` | the missing session code | `C-DC-16` |
| `session_address_mismatch` | the cross-account write code | `C-DC-17` |
| `citizen_not_found` | the unknown address code | `C-DC-18` |
| `nickname_taken` | the taken nickname code | `C-DC-19` |
| `token_not_owned` | the unowned representative Keeper code | `C-DC-20` |
| `challenge_expired` | the replayed challenge code | `C-DC-21` |
| `render_in_flight` | the second regeneration code | `C-DC-22` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour values behind every named role | `C-UX-3` |
| the exact type family names beyond the stated roles | `C-UX-6` |
| the exact motion durations behind the stated character | `C-UX-10` |
| the exact breakpoint widths behind the stated behaviour | `C-UX-14` |
| the exact corner cut inset base unit | `C-UX-8` |
| the fixed design width the scale factor divides by | `C-UX-2` |
| the exact freshness window for the holdings cache | `C-CF-100` |
| the exact per-day ceiling on regeneration requests | `C-TR-26` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 1 | 10 |
| User roles | 4 | 21 |
| Core features | 42 | 138 |
| User flow | 13 | 24 |
| UI and UX notes | 4 | 15 |
| Technical requirements | 14 | 36 |
| Data model | 6 | 28 |
| Front-end specification | 3 | 18 |
| Constraints | 1 | 6 |
| Deployment contract | 11 | 24 |
