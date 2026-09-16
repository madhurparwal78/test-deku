# Checklist: Milo Rennick Brand Platform

Source: instruction.md
Sections present: overview, roles, features, seasondata, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 1007
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The app serves a public brand property for a professional racing driver. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The app serves an editorial workspace for the management team. `src: Overview para 1`
- [ ] `C-OV-03` `capability` The public half carries the season calendar with session times. `src: Overview para 2`
- [ ] `C-OV-04` `capability` The public half carries the career record. `src: Overview para 2`
- [ ] `C-OV-05` `capability` The public half carries editorial stories with galleries. `src: Overview para 2`
- [ ] `C-OV-06` `capability` The public half carries a curated merchandise strip. `src: Overview para 2`
- [ ] `C-OV-07` `capability` The public half links out to the storefront. `src: Overview para 2`
- [ ] `C-OV-08` `constraint` The app offers no fan account. `src: Overview para 2`
- [ ] `C-OV-09` `constraint` The app offers no comment feature. `src: Overview para 2`
- [ ] `C-OV-10` `constraint` The app accepts no upload from the public. `src: Overview para 2`
- [ ] `C-OV-11` `constraint` The app offers no messaging surface. `src: Overview para 2`
- [ ] `C-OV-12` `constraint` The only fan identity is a confirmed email address. `src: Overview para 2`
- [ ] `C-OV-13` `constraint` Unpublished editorial stays unreadable to everyone outside the signed-in team. `src: Overview para 3`
- [ ] `C-OV-14` `constraint` The photograph bytes behind unpublished editorial stay unreadable on direct request. `src: Overview para 3`
- [ ] `C-OV-15` `constraint` Season data from the feed reconciles rather than overwrites. `src: Overview para 3`
- [ ] `C-OV-16` `constraint` A retried delivery carrying an older classification never moves a final result backwards. `src: Overview para 3`
- [ ] `C-OV-17` `capability` A stranger can open the app in a browser to see which race is next. `src: Overview framing para`
- [ ] `C-OV-18` `capability` A stranger can read a published story with the gallery of the story. `src: Overview framing para`
- [ ] `C-OV-19` `capability` A stranger can subscribe for updates, then confirm the subscription. `src: Overview framing para`
- [ ] `C-OV-20` `constraint` Uploaded bytes live in the `minio` bucket at the key scheme of the bucket. `src: Overview framing para`
- [ ] `C-OV-21` `constraint` A copy of an uploaded photograph kept on the app container disk does not satisfy the storage obligation. `src: Overview framing para`

## C-RL User roles

- [ ] `C-RL-01` `role` A `visitor` reads published stories. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A `visitor` reads the photographs of published stories. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `visitor` reads the season. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A `visitor` reads the results. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A `visitor` reads the profile. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `visitor` reads the partner list. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A `visitor` reads the merchandise strip. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A `visitor` subscribes for updates. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A `visitor` sends a business enquiry. `src: User roles table row 1`
- [ ] `C-RL-10` `role` A `visitor` is denied any read of a story in `draft`. `src: User roles table row 1`
- [ ] `C-RL-11` `role` A `visitor` is denied any read of a story in `in_review`. `src: User roles table row 1`
- [ ] `C-RL-12` `role` A `visitor` is denied any read of a story in `scheduled`. `src: User roles table row 1`
- [ ] `C-RL-13` `role` A `visitor` is denied any read of a story in `unpublished`. `src: User roles table row 1`
- [ ] `C-RL-14` `role` A `visitor` is denied any read of a story in `archived`. `src: User roles table row 1`
- [ ] `C-RL-15` `role` A `visitor` is denied the photograph bytes behind a story that is not public. `src: User roles table row 1`
- [ ] `C-RL-16` `role` A `visitor` cannot create a story. `src: User roles table row 1`
- [ ] `C-RL-17` `role` A `visitor` cannot upload a photograph. `src: User roles table row 1`
- [ ] `C-RL-18` `role` A `visitor` cannot publish a story. `src: User roles table row 1`
- [ ] `C-RL-19` `role` A `visitor` cannot run an ingestion. `src: User roles table row 1`
- [ ] `C-RL-20` `role` A `visitor` cannot read the enquiry inbox. `src: User roles table row 1`
- [ ] `C-RL-21` `role` A `visitor` cannot read the subscriber list. `src: User roles table row 1`
- [ ] `C-RL-22` `role` A `contributor` creates a story. `src: User roles table row 2`
- [ ] `C-RL-23` `role` A `contributor` uploads a gallery photograph. `src: User roles table row 2`
- [ ] `C-RL-24` `role` A `contributor` sets alternative text on a photograph. `src: User roles table row 2`
- [ ] `C-RL-25` `role` A `contributor` submits a story for review. `src: User roles table row 2`
- [ ] `C-RL-26` `role` A `contributor` cannot publish a story. `src: User roles table row 2`
- [ ] `C-RL-27` `role` A `contributor` cannot unpublish a story. `src: User roles table row 2`
- [ ] `C-RL-28` `role` A `contributor` cannot run an ingestion. `src: User roles table row 2`
- [ ] `C-RL-29` `role` A `contributor` cannot read the subscriber list. `src: User roles table row 2`
- [ ] `C-RL-30` `role` A `contributor` cannot read the enquiry inbox. `src: User roles table row 2`
- [ ] `C-RL-31` `role` A `contributor` cannot manage editors. `src: User roles table row 2`
- [ ] `C-RL-32` `role` An `editor` publishes a story. `src: User roles table row 3`
- [ ] `C-RL-33` `role` An `editor` unpublishes a story. `src: User roles table row 3`
- [ ] `C-RL-34` `role` An `editor` reads every story in every state. `src: User roles table row 3`
- [ ] `C-RL-35` `role` An `editor` reads the enquiry inbox. `src: User roles table row 3`
- [ ] `C-RL-36` `role` An `editor` reads the subscriber list. `src: User roles table row 3`
- [ ] `C-RL-37` `role` An `editor` runs an ingestion. `src: User roles table row 3`
- [ ] `C-RL-38` `role` An `editor` records a manual override. `src: User roles table row 3`
- [ ] `C-RL-39` `role` An `editor` cannot manage editors. `src: User roles table row 3`
- [ ] `C-RL-40` `role` An `editor` cannot read workspace settings. `src: User roles table row 3`
- [ ] `C-RL-41` `role` An `owner` reads the editor list. `src: User roles table row 4`
- [ ] `C-RL-42` `role` An `owner` reads workspace settings. `src: User roles table row 4`
- [ ] `C-RL-43` `role` An `owner` cannot be created by signup. `src: User roles table row 4`
- [ ] `C-RL-44` `contract` Authorization is enforced server-side on every mutating endpoint. `src: User roles para after table`
- [ ] `C-RL-45` `contract` Hiding a control in the interface does not satisfy the authorization obligation. `src: User roles para after table`
- [ ] `C-RL-46` `contract` A direct API call from a lower role to an endpoint above the rung of the role is rejected by the server. `src: User roles para after table`
- [ ] `C-RL-47` `contract` A rejected call leaves the protected state unchanged. `src: User roles para after table`
- [ ] `C-RL-48` `capability` Signup is open to anyone. `src: User roles closing para`
- [ ] `C-RL-49` `contract` Signup always creates a `visitor`. `src: User roles closing para`
- [ ] `C-RL-50` `literal` The four seeded accounts use the password `deku-demo-pw-2026`. `src: User roles closing para`
- [ ] `C-RL-51` `literal` The seeded owner account is `owner@example.com`. `src: User roles closing para`
- [ ] `C-RL-52` `literal` The seeded editor account is `editor@example.com`. `src: User roles closing para`
- [ ] `C-RL-53` `literal` The seeded contributor account is `contributor@example.com`. `src: User roles closing para`
- [ ] `C-RL-54` `literal` The seeded visitor account is `visitor@example.com`. `src: User roles closing para`

## C-CF Core features

- [ ] `C-CF-01` `literal` A story state is one of `draft`, `in_review`, `scheduled`, `published`, `unpublished`, `archived`. `src: Core features, editorial state item 1`
- [ ] `C-CF-02` `contract` Creating a story always produces the `draft` state. `src: Core features, editorial state item 1`
- [ ] `C-CF-03` `contract` Public visibility of a story is derived rather than stored as a flag an editor sets. `src: Core features, editorial state item 2`
- [ ] `C-CF-04` `contract` A story is public when the state of the story is `published`. `src: Core features, editorial state item 2`
- [ ] `C-CF-05` `contract` A story is public only when the publication instant of the story is not in the future. `src: Core features, editorial state item 2`
- [ ] `C-CF-06` `contract` A `scheduled` story whose instant has not arrived is absent from every public read. `src: Core features, editorial state item 2`
- [ ] `C-CF-07` `contract` A `scheduled` story whose instant has not arrived is refused on direct request. `src: Core features, editorial state item 2`
- [ ] `C-CF-08` `contract` The public story list holds public stories only. `src: Core features, editorial state item 3`
- [ ] `C-CF-09` `contract` A direct request for a story that is not public is refused rather than partially served. `src: Core features, editorial state item 3`
- [ ] `C-CF-10` `contract` Public story order is newest publication instant first. `src: Core features, editorial state item 4`
- [ ] `C-CF-11` `literal` Against the shipped seed the public story list holds `3 stories`. `src: Core features, editorial state item 4`
- [ ] `C-CF-12` `literal` Publishing a fourth story makes the public count read `4 stories`. `src: Core features, editorial state item 4`
- [ ] `C-CF-13` `contract` Unpublishing removes a story from the public list immediately. `src: Core features, editorial state item 5`
- [ ] `C-CF-14` `contract` The public id of an unpublished story answers as not found. `src: Core features, editorial state item 5`
- [ ] `C-CF-15` `contract` The public id of an unpublished story does not redirect. `src: Core features, editorial state item 5`
- [ ] `C-CF-16` `capability` A contributor creates a story at the dedicated address of the create surface. `src: Core features, publishing item 1`
- [ ] `C-CF-17` `capability` A contributor attaches gallery photographs to a story. `src: Core features, publishing item 1`
- [ ] `C-CF-18` `capability` A contributor submits a story for review, moving the story to `in_review`. `src: Core features, publishing item 1`
- [ ] `C-CF-19` `contract` Pre-publication validation runs before every publish. `src: Core features, publishing item 2`
- [ ] `C-CF-20` `contract` Publication is blocked with a message naming the reason. `src: Core features, publishing item 2`
- [ ] `C-CF-21` `contract` A blocked publication is a refusal rather than a dismissible warning. `src: Core features, publishing item 2`
- [ ] `C-CF-22` `contract` Publication is blocked when a gallery photograph on the story carries no alternative text. `src: Core features, publishing item 2 bullet 1`
- [ ] `C-CF-23` `contract` Publication is blocked when a `quotation` on the story carries no attribution. `src: Core features, publishing item 2 bullet 2`
- [ ] `C-CF-24` `contract` Publication is blocked when the story references a round outside the current season. `src: Core features, publishing item 2 bullet 3`
- [ ] `C-CF-25` `contract` Publishing sets the story state to `published`. `src: Core features, publishing item 3`
- [ ] `C-CF-26` `contract` Publishing stamps the publication instant exactly once. `src: Core features, publishing item 3`
- [ ] `C-CF-27` `contract` Publishing a story a second time changes nothing. `src: Core features, publishing item 3`
- [ ] `C-CF-28` `contract` Publishing a story a second time is not an error. `src: Core features, publishing item 3`
- [ ] `C-CF-29` `contract` A story slug is unique across the table of stories. `src: Core features, publishing item 4`
- [ ] `C-CF-30` `contract` A create carrying a slug already taken is rejected as invalid. `src: Core features, publishing item 4`
- [ ] `C-CF-31` `contract` A rejected create leaves no story row behind. `src: Core features, publishing item 4`
- [ ] `C-CF-32` `contract` A rejected create leaves no stored object behind. `src: Core features, publishing item 4`
- [ ] `C-CF-33` `contract` A story public id is opaque rather than a sequential number. `src: Core features, publishing item 5`
- [ ] `C-CF-34` `contract` Two story public ids cannot be reached from each other by counting. `src: Core features, publishing item 5`
- [ ] `C-CF-35` `contract` A visitor cannot walk the story catalogue by incrementing an identifier. `src: Core features, publishing item 5`
- [ ] `C-CF-36` `contract` A visitor cannot learn how much unpublished editorial exists by observing gaps. `src: Core features, publishing item 5`
- [ ] `C-CF-37` `data` An internal story identifier may stay sequential. `src: Core features, publishing item 5`
- [ ] `C-CF-38` `data` The internal identifier of a story is a separate field from the public id. `src: Core features, publishing item 5`
- [ ] `C-CF-39` `contract` Concurrent editing of a story is detected rather than lost. `src: Core features, publishing item 6`
- [ ] `C-CF-40` `contract` An edit carries the version the editor loaded. `src: Core features, publishing item 6`
- [ ] `C-CF-41` `contract` An edit carrying a stale version is refused with a message. `src: Core features, publishing item 6`
- [ ] `C-CF-42` `contract` Publication ordering completes the photographs before the record is published. `src: Core features, publishing item 7`
- [ ] `C-CF-43` `contract` Publication ordering verifies the public route after the record is published. `src: Core features, publishing item 7`
- [ ] `C-CF-44` `contract` A story is never announced anywhere before the story is visible. `src: Core features, publishing item 7`
- [ ] `C-CF-45` `contract` One authenticated route on the app origin serves photograph bytes. `src: Core features, photograph boundary item 1`
- [ ] `C-CF-46` `contract` A photograph on a public story is served to any caller. `src: Core features, photograph boundary item 1`
- [ ] `C-CF-47` `contract` A photograph on a story that is not public is served only to a signed-in `contributor`, `editor`, `owner`. `src: Core features, photograph boundary item 1`
- [ ] `C-CF-48` `contract` An anonymous request for the photograph of a `scheduled` story is denied. `src: Core features, photograph boundary item 2`
- [ ] `C-CF-49` `contract` A signed-in `visitor` request for the photograph of a `scheduled` story is denied. `src: Core features, photograph boundary item 2`
- [ ] `C-CF-50` `contract` An `editor` request for the photograph of a `scheduled` story returns the bytes. `src: Core features, photograph boundary item 2`
- [ ] `C-CF-51` `contract` A denied photograph request returns no low-quality placeholder. `src: Core features, photograph boundary item 3`
- [ ] `C-CF-52` `contract` A denied photograph request returns no redirect to the object store. `src: Core features, photograph boundary item 3`
- [ ] `C-CF-53` `contract` A denied photograph request returns no presigned link. `src: Core features, photograph boundary item 3`
- [ ] `C-CF-54` `contract` A denied photograph request leaves the stored object untouched. `src: Core features, photograph boundary item 3`
- [ ] `C-CF-55` `ui` The footer of every route carries a subscribe form of one email field. `src: Core features, subscribing item 1`
- [ ] `C-CF-56` `ui` The subscribe email field carries a visible label rather than a placeholder standing in for one. `src: Core features, subscribing item 1`
- [ ] `C-CF-57` `ui` The subscribe form carries a consent statement. `src: Core features, subscribing item 1`
- [ ] `C-CF-58` `ui` The subscribe form links to the privacy route. `src: Core features, subscribing item 1`
- [ ] `C-CF-59` `contract` A subscribe submission creates a subscriber at status `pending`. `src: Core features, subscribing item 2`
- [ ] `C-CF-60` `contract` A subscribe submission returns a single-purpose confirmation token. `src: Core features, subscribing item 2`
- [ ] `C-CF-61` `contract` A pending subscriber is never counted as a confirmed subscriber. `src: Core features, subscribing item 2`
- [ ] `C-CF-62` `contract` Confirming with the confirmation token moves the subscriber to `confirmed`. `src: Core features, subscribing item 3`
- [ ] `C-CF-63` `contract` Confirming stamps the confirmation instant. `src: Core features, subscribing item 3`
- [ ] `C-CF-64` `contract` Presenting the confirmation token to the unsubscribe route does nothing. `src: Core features, subscribing item 3`
- [ ] `C-CF-65` `contract` Unsubscribing takes a token of the own kind of the unsubscribe route. `src: Core features, subscribing item 4`
- [ ] `C-CF-66` `contract` An unsubscribe token never expires. `src: Core features, subscribing item 4`
- [ ] `C-CF-67` `contract` Unsubscribing changes state only on an explicit positive action. `src: Core features, subscribing item 4`
- [ ] `C-CF-68` `contract` A mail client that merely fetches the unsubscribe link cannot unsubscribe anyone. `src: Core features, subscribing item 4`
- [ ] `C-CF-69` `contract` A repeat subscribe submission for a known address answers exactly as the first one did. `src: Core features, subscribing item 5`
- [ ] `C-CF-70` `contract` A repeat subscribe submission states nothing about whether the address was already on the list. `src: Core features, subscribing item 5`
- [ ] `C-CF-71` `contract` A pending record not confirmed within the workspace window is deleted rather than retained. `src: Core features, subscribing item 6`
- [ ] `C-CF-72` `contract` An address in a `suppressed` state creates no pending record. `src: Core features, subscribing item 7`
- [ ] `C-CF-73` `contract` An address in a `suppressed` state receives no token. `src: Core features, subscribing item 7`
- [ ] `C-CF-74` `contract` An address in a `suppressed` state receives the same pending message as any other submission. `src: Core features, subscribing item 7`
- [ ] `C-CF-75` `literal` A privacy page is reachable at `/legal/privacy-policy`. `src: Core features, public pages item 1`
- [ ] `C-CF-76` `ui` The privacy page is reachable from the footer of every route. `src: Core features, public pages item 1`
- [ ] `C-CF-77` `ui` The privacy page states that the platform stores a subscriber email address. `src: Core features, public pages item 1`
- [ ] `C-CF-78` `ui` The privacy page states that the platform stores the chosen subscriber topics. `src: Core features, public pages item 1`
- [ ] `C-CF-79` `ui` The privacy page states that the platform stores the subscriber consent record. `src: Core features, public pages item 1`
- [ ] `C-CF-80` `ui` The privacy page states that the platform stores the enquiry name, organisation, message. `src: Core features, public pages item 1`
- [ ] `C-CF-81` `literal` A terms page is reachable at `/legal/terms-conditions`. `src: Core features, public pages item 2`
- [ ] `C-CF-82` `ui` The terms page is reachable from the footer of every route. `src: Core features, public pages item 2`
- [ ] `C-CF-83` `ui` An unknown address renders the platform not-found route. `src: Core features, public pages item 3`
- [ ] `C-CF-84` `literal` The not-found route carries a `Back to the season` action. `src: Core features, public pages item 3`
- [ ] `C-CF-85` `contract` An unknown address answers as not found rather than as a page that exists. `src: Core features, public pages item 3`
- [ ] `C-CF-86` `contract` Every internal link on every public route resolves. `src: Core features, public pages item 4`
- [ ] `C-CF-87` `contract` A link in the chrome never lands on the not-found route. `src: Core features, public pages item 4`
- [ ] `C-CF-88` `contract` A link in the footer never lands on the not-found route. `src: Core features, public pages item 4`
- [ ] `C-CF-89` `contract` A link in the body of a public story never lands on the not-found route. `src: Core features, public pages item 4`
- [ ] `C-CF-90` `contract` Every public route carries an own title. `src: Core features, public pages item 5`
- [ ] `C-CF-91` `contract` Every public route carries an own description. `src: Core features, public pages item 5`
- [ ] `C-CF-92` `contract` No two public routes share a title. `src: Core features, public pages item 5`
- [ ] `C-CF-93` `contract` No two public routes share a description. `src: Core features, public pages item 5`
- [ ] `C-CF-94` `contract` Public addresses are lowercase, hyphen-separated, with no trailing slash except the site root. `src: Core features, public pages item 5`
- [ ] `C-CF-95` `contract` A request carrying a trailing slash redirects permanently to the canonical form. `src: Core features, public pages item 5`
- [ ] `C-CF-96` `contract` A request in mixed case redirects permanently to the canonical form. `src: Core features, public pages item 5`
- [ ] `C-CF-97` `contract` Every route emits a canonical link. `src: Core features, public pages item 5`
- [ ] `C-CF-98` `contract` Every route emits a social preview set. `src: Core features, public pages item 5`
- [ ] `C-CF-99` `ui` A structured-data block describes the athlete on the home route. `src: Core features, public pages item 5`
- [ ] `C-CF-100` `ui` A structured-data block describes the sporting events on the calendar route. `src: Core features, public pages item 5`
- [ ] `C-CF-101` `ui` A structured-data block is generated from the same records that render the page. `src: Core features, public pages item 5`
- [ ] `C-CF-102` `literal` A maintenance state reads `Back shortly. We are making a change.` `src: Core features, public pages item 6`
- [ ] `C-CF-103` `ui` The maintenance state replaces a server error page. `src: Core features, public pages item 6`
- [ ] `C-CF-104` `constraint` The subscribe form is one of only two public write surfaces. `src: Core features, abuse control para 1`
- [ ] `C-CF-105` `constraint` The enquiry form is one of only two public write surfaces. `src: Core features, abuse control para 1`
- [ ] `C-CF-106` `contract` A decoy field hidden from people is present to naive automation. `src: Core features, abuse control para 1`
- [ ] `C-CF-107` `contract` Completion of the decoy field silently discards the submission. `src: Core features, abuse control para 1`
- [ ] `C-CF-108` `contract` A minimum elapsed time between render, submit is enforced. `src: Core features, abuse control para 1`
- [ ] `C-CF-109` `contract` A submission below the minimum elapsed time is discarded. `src: Core features, abuse control para 1`
- [ ] `C-CF-110` `contract` A signed expiring token is issued with each public form. `src: Core features, abuse control para 1`
- [ ] `C-CF-111` `contract` The signed form token is required at submit. `src: Core features, abuse control para 1`
- [ ] `C-CF-112` `contract` The signed form token is the cross-site request forgery protection. `src: Core features, abuse control para 1`
- [ ] `C-CF-113` `contract` A rate limit applies per address on the public write surfaces. `src: Core features, abuse control para 1`
- [ ] `C-CF-114` `contract` A rate limit applies per calling origin on the public write surfaces. `src: Core features, abuse control para 1`
- [ ] `C-CF-115` `contract` A challenge appears only on the enquiry form. `src: Core features, abuse control para 1`
- [ ] `C-CF-116` `contract` A challenge appears only when the earlier layers scored the submission as suspicious. `src: Core features, abuse control para 1`
- [ ] `C-CF-117` `contract` Bot handling is by behaviour, reputation rather than by matching a user-agent string. `src: Core features, abuse control para 1`
- [ ] `C-CF-118` `contract` A search crawler is served exactly the content a person is served. `src: Core features, abuse control para 1`
- [ ] `C-CF-119` `contract` Every field is validated at the server against one declared schema. `src: Core features, abuse control para 2`
- [ ] `C-CF-120` `contract` The declared schema is also the source of the client rules. `src: Core features, abuse control para 2`
- [ ] `C-CF-121` `contract` The server trims a submitted value before validating. `src: Core features, abuse control para 2`
- [ ] `C-CF-122` `contract` The server collapses internal whitespace before validating. `src: Core features, abuse control para 2`
- [ ] `C-CF-123` `contract` The server lowercases the address domain before validating. `src: Core features, abuse control para 2`
- [ ] `C-CF-124` `contract` The server rejects a control character rather than silently stripping one. `src: Core features, abuse control para 2`
- [ ] `C-CF-125` `contract` The server rejects a field absent from the declared schema. `src: Core features, abuse control para 2`
- [ ] `C-CF-126` `contract` The server bounds every submitted string. `src: Core features, abuse control para 2`
- [ ] `C-CF-127` `contract` The server bounds the whole request body. `src: Core features, abuse control para 2`
- [ ] `C-CF-128` `contract` The enquiry name is non-empty after trimming. `src: Core features, abuse control para 2`
- [ ] `C-CF-129` `contract` The enquiry name is length-bounded. `src: Core features, abuse control para 2`
- [ ] `C-CF-130` `contract` The enquiry message is length-bounded at both ends. `src: Core features, abuse control para 2`
- [ ] `C-CF-131` `contract` The enquiry organisation is optional, length-bounded. `src: Core features, abuse control para 2`
- [ ] `C-CF-132` `contract` The enquiry consent box is never pre-checked. `src: Core features, abuse control para 2`
- [ ] `C-CF-133` `contract` The enquiry consent box must be explicitly ticked. `src: Core features, abuse control para 2`
- [ ] `C-CF-134` `contract` The public site never waits on the timing provider. `src: Season data and the feed item 1`
- [ ] `C-CF-135` `contract` Every ingested value is persisted locally. `src: Season data and the feed item 1`
- [ ] `C-CF-136` `contract` Every ingested value is served from local storage on a visitor request. `src: Season data and the feed item 1`
- [ ] `C-CF-137` `contract` Every ingestion payload is validated against a declared schema. `src: Season data and the feed item 2`
- [ ] `C-CF-138` `contract` A malformed ingestion payload is rejected rather than persisted. `src: Season data and the feed item 2`
- [ ] `C-CF-139` `contract` The raw payload of every ingestion run is retained for a bounded window. `src: Season data and the feed item 2`
- [ ] `C-CF-140` `contract` An ingestion run is submitted by an `editor` or an `owner`. `src: Season data and the feed item 3`
- [ ] `C-CF-141` `data` An ingestion run carries a run identifier plus a list of entities. `src: Season data and the feed item 3`
- [ ] `C-CF-142` `contract` Applying the same ingestion run identifier twice produces the same result. `src: Season data and the feed item 3`
- [ ] `C-CF-143` `contract` A repeated ingestion run applies nothing. `src: Season data and the feed item 3`
- [ ] `C-CF-144` `contract` A repeated ingestion run reports itself as a duplicate. `src: Season data and the feed item 3`
- [ ] `C-CF-145` `data` Every ingested entity carries the provider update instant of the entity. `src: Season data and the feed item 4`
- [ ] `C-CF-146` `contract` An ingested entity is applied only when the provider update instant is newer than what is stored. `src: Season data and the feed item 4`
- [ ] `C-CF-147` `contract` An out-of-order ingested entity is counted as superseded. `src: Season data and the feed item 4`
- [ ] `C-CF-148` `contract` An out-of-order ingested entity changes nothing. `src: Season data and the feed item 4`
- [ ] `C-CF-149` `contract` A provisional classification arriving after the final one never moves the result backwards. `src: Season data and the feed item 4`
- [ ] `C-CF-150` `contract` Ingestion is a reconciliation rather than an overwrite. `src: Season data and the feed item 5`
- [ ] `C-CF-151` `contract` Every incoming record is classified as unchanged, changed, new, missing. `src: Season data and the feed item 5`
- [ ] `C-CF-152` `contract` A round present locally, absent from the payload moves to `missing_review`. `src: Season data and the feed item 5`
- [ ] `C-CF-153` `contract` A round in `missing_review` is kept for a person rather than deleted. `src: Season data and the feed item 5`
- [ ] `C-CF-154` `contract` A field carrying an active manual override is never overwritten by a run. `src: Season data and the feed item 6`
- [ ] `C-CF-155` `contract` A run records the clash with a manual override as a conflict. `src: Season data and the feed item 6`
- [ ] `C-CF-156` `contract` A run leaves the override value standing. `src: Season data and the feed item 6`
- [ ] `C-CF-157` `contract` Concurrent ingestion runs are prevented by a lease. `src: Season data and the feed item 7`
- [ ] `C-CF-158` `contract` A manual refresh submitted during a run in flight is refused rather than interleaved. `src: Season data and the feed item 7`
- [ ] `C-CF-159` `contract` The next round is the earliest round whose end instant is still ahead. `src: Season data and the feed item 8`
- [ ] `C-CF-160` `contract` The next round state is neither `complete` nor `cancelled`. `src: Season data and the feed item 8`
- [ ] `C-CF-161` `contract` A completed round is never presented as upcoming at any layer. `src: Season data and the feed item 8`
- [ ] `C-CF-162` `contract` The next round is computed on read. `src: Season data and the feed item 8`
- [ ] `C-CF-163` `data` A session time is stored as an absolute instant. `src: Season data and the feed item 9`
- [ ] `C-CF-164` `ui` A session time is rendered with the name of the zone being shown. `src: Season data and the feed item 9`
- [ ] `C-CF-165` `ui` The calendar offers the circuit own zone as the alternative. `src: Season data and the feed item 9`
- [ ] `C-CF-166` `ui` Inside a weekend window the next-race card carries a countdown to the next session start. `src: Season data and the feed item 10`
- [ ] `C-CF-167` `ui` The countdown is announced politely at meaningful thresholds rather than on every tick. `src: Season data and the feed item 10`
- [ ] `C-CF-168` `ui` The countdown disappears rather than counting past zero. `src: Season data and the feed item 10`
- [ ] `C-CF-169` `ui` A figure older than the freshness budget states when the figure was last confirmed. `src: Season data and the feed item 11`
- [ ] `C-CF-170` `data` A freshness budget is a workspace setting rather than a constant in the code. `src: Season data and the feed item 11`
- [ ] `C-CF-171` `literal` An ingestion entity carries a `type` of `round`, `session`, `classification`, `standing`. `src: Season data and the feed item 12`
- [ ] `C-CF-172` `data` An ingestion entity carries the round number the entity belongs to. `src: Season data and the feed item 12`
- [ ] `C-CF-173` `data` An ingestion entity carries a `providerUpdatedAt` instant. `src: Season data and the feed item 12`
- [ ] `C-CF-174` `data` A classification entity carries `sessionKind`, `position`, `status`, `provisional`. `src: Season data and the feed item 12`
- [ ] `C-CF-175` `data` A round entity carries a `state`. `src: Season data and the feed item 12`
- [ ] `C-CF-176` `contract` An entity of an unknown type is rejected as invalid rather than ignored. `src: Season data and the feed item 12`
- [ ] `C-CF-177` `data` The ingestion response reports `applied`, `superseded`, `conflicted`, `missing` as counts. `src: Season data and the feed item 13`
- [ ] `C-CF-178` `data` The ingestion response reports `duplicate` as a boolean true only for a replayed run. `src: Season data and the feed item 13`
- [ ] `C-CF-179` `contract` A payload omitting a `type` on any entity is rejected as invalid. `src: Season data and the feed item 13`
- [ ] `C-CF-180` `contract` A rejected payload applies nothing. `src: Season data and the feed item 13`
- [ ] `C-CF-181` `contract` A rejected payload records no run. `src: Season data and the feed item 13`

## C-UF User flow

- [ ] `C-UF-01` `literal` The home route is at `/`. `src: User flow route table row 1`
- [ ] `C-UF-02` `literal` The record route is at `/on-track`. `src: User flow route table row 2`
- [ ] `C-UF-03` `literal` The person route is at `/off-track`. `src: User flow route table row 3`
- [ ] `C-UF-04` `literal` The season route is at `/calendar`. `src: User flow route table row 4`
- [ ] `C-UF-05` `literal` A story detail route is at `/stories/:public_id`. `src: User flow route table row 5`
- [ ] `C-UF-06` `literal` The confirmation landing is at `/subscribe/confirm`. `src: User flow route table row 7`
- [ ] `C-UF-07` `literal` The unsubscribe landing is at `/subscribe/unsubscribe`. `src: User flow route table row 7`
- [ ] `C-UF-08` `literal` The sign-in route is at `/login`. `src: User flow route table row 8`
- [ ] `C-UF-09` `literal` The registration route is at `/signup`. `src: User flow route table row 8`
- [ ] `C-UF-10` `literal` The workspace dashboard is at `/studio`. `src: User flow route table row 9`
- [ ] `C-UF-11` `literal` The workspace story list is at `/studio/stories`. `src: User flow route table row 10`
- [ ] `C-UF-12` `literal` The workspace create address is at `/studio/stories/new`. `src: User flow route table row 10`
- [ ] `C-UF-13` `literal` The workspace media library is at `/studio/media`. `src: User flow route table row 11`
- [ ] `C-UF-14` `literal` The workspace ingestion surface is at `/studio/calendar`. `src: User flow route table row 12`
- [ ] `C-UF-15` `literal` The workspace enquiry inbox is at `/studio/enquiries`. `src: User flow route table row 13`
- [ ] `C-UF-16` `literal` The workspace audience surface is at `/studio/audience`. `src: User flow route table row 13`
- [ ] `C-UF-17` `literal` The workspace settings surface is at `/studio/settings`. `src: User flow route table row 14`
- [ ] `C-UF-18` `contract` The workspace dashboard requires at least the `contributor` role. `src: User flow route table row 9`
- [ ] `C-UF-19` `contract` The workspace ingestion surface requires at least the `editor` role. `src: User flow route table row 12`
- [ ] `C-UF-20` `contract` The workspace settings surface requires the `owner` role. `src: User flow route table row 14`
- [ ] `C-UF-21` `contract` An unauthenticated workspace request goes to the sign-in route. `src: User flow, entry and redirects`
- [ ] `C-UF-22` `contract` Signing in lands on the route asked for. `src: User flow, entry and redirects`
- [ ] `C-UF-23` `contract` A signed-in `visitor` at the workspace is refused with a message. `src: User flow, entry and redirects`
- [ ] `C-UF-24` `contract` A signed-in `visitor` at the workspace is not looped back to sign in. `src: User flow, entry and redirects`
- [ ] `C-UF-25` `contract` After login a `contributor` lands on the workspace dashboard. `src: User flow, entry and redirects`
- [ ] `C-UF-26` `contract` After login an `editor` lands on the workspace dashboard. `src: User flow, entry and redirects`
- [ ] `C-UF-27` `contract` After login an `owner` lands on the workspace dashboard. `src: User flow, entry and redirects`
- [ ] `C-UF-28` `contract` After login a `visitor` lands on the home route. `src: User flow, entry and redirects`
- [ ] `C-UF-29` `contract` Logout discards the bearer token. `src: User flow, entry and redirects`
- [ ] `C-UF-30` `contract` An expiry mid-action refuses the action. `src: User flow, entry and redirects`
- [ ] `C-UF-31` `contract` An expiry mid-action returns the session to the sign-in route. `src: User flow, entry and redirects`
- [ ] `C-UF-32` `contract` An unknown story id at the story detail route shows the not-found route. `src: User flow, entry and redirects`
- [ ] `C-UF-33` `contract` A story id that is not public shows the not-found route. `src: User flow, entry and redirects`
- [ ] `C-UF-34` `literal` The next-race card on the home route reads `Sundown`. `src: User flow journey 1`
- [ ] `C-UF-35` `literal` The next-race card carries the round designation `04`. `src: User flow journey 1`
- [ ] `C-UF-36` `literal` The next-race standing line names the constructor `Halcyon`. `src: User flow journey 1`
- [ ] `C-UF-37` `literal` The next-race standing line names the debut year `2019`. `src: User flow journey 1`
- [ ] `C-UF-38` `ui` The home teaser strip carries the live public story count. `src: User flow journey 1`
- [ ] `C-UF-39` `ui` Following a teaser opens the story detail route. `src: User flow journey 1`
- [ ] `C-UF-40` `ui` A story gallery renders captions in the place-comma-year form. `src: User flow journey 1`
- [ ] `C-UF-41` `literal` The calendar route lists six rounds of the `2026` season. `src: User flow journey 2`
- [ ] `C-UF-42` `literal` The calendar route names the series `Prime One`. `src: User flow journey 2`
- [ ] `C-UF-43` `ui` Three of the six seeded rounds are complete. `src: User flow journey 2`
- [ ] `C-UF-44` `ui` The featured calendar panel carries the date range of the next round. `src: User flow journey 2`
- [ ] `C-UF-45` `ui` The featured calendar panel carries the circuit length of the next round. `src: User flow journey 2`
- [ ] `C-UF-46` `ui` The featured calendar panel carries the lap count of the next round. `src: User flow journey 2`
- [ ] `C-UF-47` `ui` The featured calendar panel carries the first year competed at the next round. `src: User flow journey 2`
- [ ] `C-UF-48` `ui` The featured calendar panel carries a schedule table of the sessions of the round. `src: User flow journey 2`
- [ ] `C-UF-49` `ui` The schedule table names the zone the times are shown in. `src: User flow journey 2`
- [ ] `C-UF-50` `ui` The calendar view mode is reflected in the address so a view can be shared. `src: User flow journey 2`
- [ ] `C-UF-51` `ui` Subscribing from the footer replaces the form in place with a message. `src: User flow journey 3`
- [ ] `C-UF-52` `literal` The pending subscribe message reads `Check your inbox to confirm.` `src: User flow journey 3`
- [ ] `C-UF-53` `contract` The subscribe response carries a confirmation token. `src: User flow journey 3`
- [ ] `C-UF-54` `contract` Confirming at the confirmation landing moves the subscriber to `confirmed`. `src: User flow journey 3`
- [ ] `C-UF-55` `contract` Submitting the same address again shows the identical pending message. `src: User flow journey 3`
- [ ] `C-UF-56` `capability` Signing in as the seeded editor reaches the workspace story list. `src: User flow journey 4`
- [ ] `C-UF-57` `ui` The workspace story list shows six seeded stories across every state. `src: User flow journey 4`
- [ ] `C-UF-58` `literal` Publishing the story `What Sundown Asks For` raises the public count. `src: User flow journey 4`
- [ ] `C-UF-59` `capability` Signing in as the seeded contributor reaches the create address. `src: User flow journey 5`
- [ ] `C-UF-60` `capability` A contributor attaches a photograph to a newly created story. `src: User flow journey 5`
- [ ] `C-UF-61` `capability` A contributor submits a newly created story for review. `src: User flow journey 5`
- [ ] `C-UF-62` `contract` A contributor attempting to publish is refused. `src: User flow journey 5`
- [ ] `C-UF-63` `literal` Signed out, the story `2a9b7f31c8` is not found. `src: User flow journey 6`
- [ ] `C-UF-64` `contract` Signed out, the photograph route of a draft story is denied. `src: User flow journey 6`
- [ ] `C-UF-65` `contract` As the seeded visitor the photograph of a draft story is still denied. `src: User flow journey 6`
- [ ] `C-UF-66` `contract` As the seeded editor the photograph of a draft story is served. `src: User flow journey 6`
- [ ] `C-UF-67` `ui` The menu overlay carries the business enquiry surface. `src: User flow journey 7`
- [ ] `C-UF-68` `ui` The enquiry form takes a name, an email address, an enquiry type, a message, a consent box. `src: User flow journey 7`
- [ ] `C-UF-69` `literal` The enquiry confirmation reads back the reference `ENQ-00001`. `src: User flow journey 7`
- [ ] `C-UF-70` `contract` An enquiry with the organisation left blank still sends. `src: User flow journey 7`
- [ ] `C-UF-71` `contract` An enquiry with the message left blank is refused. `src: User flow journey 7`
- [ ] `C-UF-72` `ui` A refused enquiry raises an error summary naming the field at fault. `src: User flow journey 7`
- [ ] `C-UF-73` `ui` Every list has an empty state naming what is missing. `src: User flow, states`
- [ ] `C-UF-74` `ui` Every route has a loading state. `src: User flow, states`
- [ ] `C-UF-75` `ui` A rejected submission keeps what was typed. `src: User flow, states`
- [ ] `C-UF-76` `ui` A rejected submission names the field at fault. `src: User flow, states`
- [ ] `C-UF-77` `ui` A stale figure is shown with the instant of last confirmation rather than as current. `src: User flow, states`
- [ ] `C-UF-78` `ui` No error leaves a blank page. `src: User flow, states`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The property reads as an editorial surface wrapped around a live scoreboard. `src: UI/UX notes para 1`
- [ ] `C-UX-02` `ui` The voice is plain rather than breathless. `src: UI/UX notes para 1`
- [ ] `C-UX-03` `ui` The next-race card is the one place the design raises the voice of the design. `src: UI/UX notes para 1`
- [ ] `C-UX-04` `ui` A variable grotesque carries everything structural. `src: UI/UX notes para 2`
- [ ] `C-UX-05` `ui` The grotesque carries navigation, statistics, tables, body copy. `src: UI/UX notes para 2`
- [ ] `C-UX-06` `ui` A high-contrast display serif carries pull-quotes. `src: UI/UX notes para 2`
- [ ] `C-UX-07` `ui` The display serif carries single accent words inside sans headings. `src: UI/UX notes para 2`
- [ ] `C-UX-08` `ui` The display serif carries the second line of every split heading. `src: UI/UX notes para 2`
- [ ] `C-UX-09` `ui` The split heading sets the first line in the grotesque at a heavy cut. `src: UI/UX notes para 2`
- [ ] `C-UX-10` `ui` The split heading appears on the calendar hero. `src: UI/UX notes para 2`
- [ ] `C-UX-11` `ui` The split heading appears on the off-track hero. `src: UI/UX notes para 2`
- [ ] `C-UX-12` `ui` The split heading is a required device rather than a decoration. `src: UI/UX notes para 2`
- [ ] `C-UX-13` `ui` Ground alternates by route as the primary structural signal. `src: UI/UX notes para 3`
- [ ] `C-UX-14` `ui` The light routes sit on a near-white neutral. `src: UI/UX notes para 3`
- [ ] `C-UX-15` `ui` Editorial sections sit on a warmer near-white neutral. `src: UI/UX notes para 3`
- [ ] `C-UX-16` `ui` The record route sits on a near-black neutral. `src: UI/UX notes para 3`
- [ ] `C-UX-17` `ui` The season route sits on a near-black neutral. `src: UI/UX notes para 3`
- [ ] `C-UX-18` `ui` The menu overlay sits on a deep neutral. `src: UI/UX notes para 3`
- [ ] `C-UX-19` `ui` The footer sits on a deep neutral. `src: UI/UX notes para 3`
- [ ] `C-UX-20` `ui` The accent is one mid, vivid lime. `src: UI/UX notes para 3`
- [ ] `C-UX-21` `ui` The accent is never diluted into a tint ramp. `src: UI/UX notes para 3`
- [ ] `C-UX-22` `ui` A receding accent changes to a second mid, vivid lime. `src: UI/UX notes para 3`
- [ ] `C-UX-23` `ui` A mid, vivid orange is the secondary accent for alert states. `src: UI/UX notes para 3`
- [ ] `C-UX-24` `ui` A light, vivid red belongs to the error surface alone. `src: UI/UX notes para 3`
- [ ] `C-UX-25` `ui` Light neutrals carry captions, dividers, secondary text. `src: UI/UX notes para 3`
- [ ] `C-UX-26` `ui` Deep neutrals carry raised surfaces on the dark routes. `src: UI/UX notes para 3`
- [ ] `C-UX-27` `ui` Every typographic value on the wide layouts derives from one clamped viewport ratio. `src: UI/UX notes para 4`
- [ ] `C-UX-28` `ui` Rendered sizes are not round numbers, which is correct. `src: UI/UX notes para 4`
- [ ] `C-UX-29` `ui` One long, hard, late-settling ease carries almost everything. `src: UI/UX notes para 5`
- [ ] `C-UX-30` `ui` Headings reveal line by line on a wipe from the left with a per-line stagger. `src: UI/UX notes para 5`
- [ ] `C-UX-31` `ui` Photographs enter on a mask that opens. `src: UI/UX notes para 5`
- [ ] `C-UX-32` `ui` The pinned photograph track scrubs against scroll. `src: UI/UX notes para 5`
- [ ] `C-UX-33` `ui` The accent stroke draws itself across the hero. `src: UI/UX notes para 5`
- [ ] `C-UX-34` `ui` Under a reduced-motion preference every travel collapses to a cross fade in place. `src: UI/UX notes para 5`
- [ ] `C-UX-35` `ui` Under a reduced-motion preference nothing carrying information is lost. `src: UI/UX notes para 5`
- [ ] `C-UX-36` `ui` Contrast meets WCAG AA against the ground in every state. `src: UI/UX notes para 6`
- [ ] `C-UX-37` `ui` Keyboard navigation reaches every calendar row with a visible focus ring. `src: UI/UX notes para 6`
- [ ] `C-UX-38` `ui` Keyboard navigation reaches every gallery item with a visible focus ring. `src: UI/UX notes para 6`
- [ ] `C-UX-39` `ui` Every photograph carries alternative text. `src: UI/UX notes para 6`
- [ ] `C-UX-40` `ui` A failed enquiry raises an error summary at the top of the form. `src: UI/UX notes para 6`
- [ ] `C-UX-41` `ui` The enquiry error summary moves focus to the summary. `src: UI/UX notes para 6`
- [ ] `C-UX-42` `ui` The submit control is never disabled for being invalid. `src: UI/UX notes para 6`
- [ ] `C-UX-43` `ui` Meaning is never signalled by colour alone. `src: UI/UX notes para 6`
- [ ] `C-UX-44` `ui` The layout is a top navigation bar with a centre monogram. `src: UI/UX notes para 7`
- [ ] `C-UX-45` `ui` A persistent store button sits at the top right. `src: UI/UX notes para 7`
- [ ] `C-UX-46` `ui` The work surfaces are card grids. `src: UI/UX notes para 7`
- [ ] `C-UX-47` `ui` Reading routes sit in a centred column with generous gutters. `src: UI/UX notes para 7`
- [ ] `C-UX-48` `ui` Each route leads with one clear primary action. `src: UI/UX notes para 7`
- [ ] `C-UX-49` `ui` The primary action is visually distinct from every secondary one. `src: UI/UX notes para 7`
- [ ] `C-UX-50` `ui` At a phone width the navigation collapses into the menu overlay. `src: UI/UX notes para 7`
- [ ] `C-UX-51` `ui` At a phone width the calendar list becomes the default mode. `src: UI/UX notes para 7`
- [ ] `C-UX-52` `ui` At a phone width nothing overflows sideways. `src: UI/UX notes para 7`
- [ ] `C-UX-53` `ui` At a phone width every navigation target stays reachable. `src: UI/UX notes para 7`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is Angular. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The backend is Fastify. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The rendering model is a single-page application over a JSON API. `src: Technical requirements para 1`
- [ ] `C-TR-04` `contract` The browser receives an application shell on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` Every route content arrives as JSON from the same origin. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` The server renders no page HTML. `src: Technical requirements para 1`
- [ ] `C-TR-07` `contract` Both halves install from the public npm registry at image build time. `src: Technical requirements para 2`
- [ ] `C-TR-08` `contract` Both halves run on the Node 20 runtime the environment image carries. `src: Technical requirements para 2`
- [ ] `C-TR-09` `literal` Storage is PostgreSQL reached at `DATABASE_URL`. `src: Technical requirements para 3`
- [ ] `C-TR-10` `literal` Object storage is MinIO reached at `STORAGE_ENDPOINT`. `src: Technical requirements para 3`
- [ ] `C-TR-11` `literal` The object bucket is named by `STORAGE_BUCKET`. `src: Technical requirements para 3`
- [ ] `C-TR-12` `literal` The object credentials are `STORAGE_ACCESS_KEY`, `STORAGE_SECRET_KEY`. `src: Technical requirements para 3`
- [ ] `C-TR-13` `contract` Both backing services are already running in the environment. `src: Technical requirements para 3`
- [ ] `C-TR-14` `contract` Every host is read from the environment rather than hardcoded. `src: Technical requirements para 3`
- [ ] `C-TR-15` `contract` Auth is app-implemented email with password. `src: Technical requirements para 4`
- [ ] `C-TR-16` `contract` A password is stored hashed. `src: Technical requirements para 4`
- [ ] `C-TR-17` `literal` Login returns `access_token`. `src: Technical requirements para 4`
- [ ] `C-TR-18` `literal` The client sends `Authorization: Bearer <access_token>` on every guarded request. `src: Technical requirements para 4`
- [ ] `C-TR-19` `contract` A token expires after 24 hours. `src: Technical requirements para 4`
- [ ] `C-TR-20` `contract` An expired token is refused. `src: Technical requirements para 4`
- [ ] `C-TR-21` `contract` The three team roles are seeded rather than created by signup. `src: Technical requirements para 4`
- [ ] `C-TR-22` `constraint` There is no password reset. `src: Technical requirements para 4`
- [ ] `C-TR-23` `constraint` There is no external identity provider. `src: Technical requirements para 4`
- [ ] `C-TR-24` `literal` The health route `GET /api/health` returns `200` with a JSON body once ready. `src: Technical requirements para 5`
- [ ] `C-TR-25` `contract` Request logging is structured to stdout, one line per request. `src: Technical requirements para 5`
- [ ] `C-TR-26` `contract` A request log line carries the method, path, status, duration. `src: Technical requirements para 5`
- [ ] `C-TR-27` `contract` A request log line never carries a password. `src: Technical requirements para 5`
- [ ] `C-TR-28` `contract` A request log line never carries a bearer token. `src: Technical requirements para 5`
- [ ] `C-TR-29` `contract` A request log line never carries object bytes. `src: Technical requirements para 5`
- [ ] `C-TR-30` `contract` Every photograph lives in `minio` alone. `src: Technical requirements para 6`
- [ ] `C-TR-31` `contract` Every derivative lives in `minio` alone. `src: Technical requirements para 6`
- [ ] `C-TR-32` `contract` Protected bytes are served through an authenticated streaming route on the app origin. `src: Technical requirements para 6`
- [ ] `C-TR-33` `contract` Protected bytes are never served by handing out a presigned URL. `src: Technical requirements para 6`
- [ ] `C-TR-34` `contract` One route owns the visibility decision for every object. `src: Technical requirements para 6`
- [ ] `C-TR-35` `contract` Every response is shaped by an explicit field allowlist per resource. `src: Technical requirements para 7`
- [ ] `C-TR-36` `contract` No public response carries a provider identifier. `src: Technical requirements para 7`
- [ ] `C-TR-37` `contract` No public response carries an author identifier. `src: Technical requirements para 7`
- [ ] `C-TR-38` `contract` No public response carries a revision. `src: Technical requirements para 7`
- [ ] `C-TR-39` `contract` No public response carries a scheduling instant. `src: Technical requirements para 7`
- [ ] `C-TR-40` `contract` No public response carries a subscriber field. `src: Technical requirements para 7`
- [ ] `C-TR-41` `contract` No public response carries an enquiry field. `src: Technical requirements para 7`
- [ ] `C-TR-42` `contract` No serialiser returns a record by spreading the stored row of the record. `src: Technical requirements para 7`
- [ ] `C-TR-43` `contract` No relation is included unless the allowlist for that audience names the relation. `src: Technical requirements para 7`
- [ ] `C-TR-44` `contract` Every read carries the visibility scope the read is entitled to. `src: Technical requirements para 8`
- [ ] `C-TR-45` `contract` Every write carries the visibility scope the write is entitled to. `src: Technical requirements para 8`
- [ ] `C-TR-46` `contract` A query that omits the scope returns nothing rather than everything. `src: Technical requirements para 8`
- [ ] `C-TR-47` `contract` Draft editorial never reaches a public read through a missing state filter. `src: Technical requirements para 8`
- [ ] `C-TR-48` `contract` A subscriber address never reaches a public response through an included relation. `src: Technical requirements para 8`
- [ ] `C-TR-49` `contract` An enquiry body never reaches a public response through an included relation. `src: Technical requirements para 8`
- [ ] `C-TR-50` `contract` Draft editorial never reaches a warmed public response. `src: Technical requirements para 8`
- [ ] `C-TR-51` `contract` Sign-out destroys the server-side session rather than only clearing the cookie. `src: Technical requirements para 9`
- [ ] `C-TR-52` `contract` An owner revokes every session belonging to any team account. `src: Technical requirements para 9`
- [ ] `C-TR-53` `contract` A password change revokes every other session for that account. `src: Technical requirements para 9`
- [ ] `C-TR-54` `contract` A password change keeps the current session. `src: Technical requirements para 9`
- [ ] `C-TR-55` `contract` A session identifier is regenerated on sign-in. `src: Technical requirements para 9`
- [ ] `C-TR-56` `contract` A session identifier is regenerated on any change of role. `src: Technical requirements para 9`
- [ ] `C-TR-57` `contract` Cross-site request forgery is closed by the signed expiring form token. `src: Technical requirements para 10`
- [ ] `C-TR-58` `contract` A document tree carrying a node type outside the declared schema is rejected. `src: Technical requirements para 10`
- [ ] `C-TR-59` `contract` Rate limits apply on the two public write surfaces. `src: Technical requirements para 10`
- [ ] `C-TR-60` `contract` Rate limits apply on login. `src: Technical requirements para 10`
- [ ] `C-TR-61` `contract` Rate limits apply on the ingestion endpoint. `src: Technical requirements para 10`
- [ ] `C-TR-62` `contract` A read of public season data is not rate limited. `src: Technical requirements para 10`
- [ ] `C-TR-63` `contract` An audit trail records every publish. `src: Technical requirements para 11`
- [ ] `C-TR-64` `contract` An audit trail records every unpublish. `src: Technical requirements para 11`
- [ ] `C-TR-65` `contract` An audit trail records every override. `src: Technical requirements para 11`
- [ ] `C-TR-66` `contract` An audit trail records every ingestion run. `src: Technical requirements para 11`
- [ ] `C-TR-67` `contract` An audit trail records every role change. `src: Technical requirements para 11`
- [ ] `C-TR-68` `contract` An audit trail records every audience export. `src: Technical requirements para 11`
- [ ] `C-TR-69` `contract` An audit entry carries the account, the instant, the record. `src: Technical requirements para 11`
- [ ] `C-TR-70` `contract` Logs carry a request identifier so one request can be followed end to end. `src: Technical requirements para 11`
- [ ] `C-TR-71` `contract` Errors are aggregated rather than only printed. `src: Technical requirements para 11`
- [ ] `C-TR-72` `contract` An ingestion run past the freshness budget raises an alarm on the workspace dashboard. `src: Technical requirements para 11`
- [ ] `C-TR-73` `contract` No served script carries a database password. `src: Technical requirements para 12`
- [ ] `C-TR-74` `contract` No served document carries an object-store access key. `src: Technical requirements para 12`
- [ ] `C-TR-75` `contract` No served payload carries an object-store secret. `src: Technical requirements para 12`
- [ ] `C-TR-76` `contract` No served payload carries a bearer token belonging to a seeded account. `src: Technical requirements para 12`
- [ ] `C-TR-77` `contract` Every response carries a strict transport policy header. `src: Technical requirements para 13`
- [ ] `C-TR-78` `contract` Every response carries a nosniff content-type policy header. `src: Technical requirements para 13`
- [ ] `C-TR-79` `constraint` Only the libraries named in the brief plus the direct dependencies are used. `src: Technical requirements para 14`
- [ ] `C-TR-80` `constraint` No second database is introduced. `src: Technical requirements para 14`
- [ ] `C-TR-81` `constraint` No cache service is introduced. `src: Technical requirements para 14`
- [ ] `C-TR-82` `constraint` No queue service is introduced. `src: Technical requirements para 14`
- [ ] `C-TR-83` `constraint` No second object store is introduced. `src: Technical requirements para 14`
- [ ] `C-TR-84` `constraint` No external identity provider is introduced. `src: Technical requirements para 14`
- [ ] `C-TR-85` `constraint` No mail vendor is introduced. `src: Technical requirements para 14`

## C-DM Data model

- [ ] `C-DM-01` `data` All timestamps are UTC with a zone. `src: Data model intro`
- [ ] `C-DM-02` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model intro`
- [ ] `C-DM-03` `contract` The seeded password is hashed as normal. `src: Data model intro`
- [ ] `C-DM-04` `contract` The seeded password literal works at login. `src: Data model intro`
- [ ] `C-DM-05` `literal` The seeded accounts are written into `/app/USER_README.md`. `src: Data model intro`
- [ ] `C-DM-06` `data` The users table carries an id, an email, a password hash, a role, a creation instant. `src: Data model, users`
- [ ] `C-DM-07` `literal` A user role is one of `owner`, `editor`, `contributor`, `visitor`. `src: Data model, users`
- [ ] `C-DM-08` `data` A user email is unique. `src: Data model, users`
- [ ] `C-DM-09` `data` The rounds table carries a number unique within the season. `src: Data model, rounds`
- [ ] `C-DM-10` `data` A round carries a name, a circuit, a country. `src: Data model, rounds`
- [ ] `C-DM-11` `data` A round carries a start instant with an end instant. `src: Data model, rounds`
- [ ] `C-DM-12` `literal` A round state is one of `scheduled`, `in_progress`, `complete`, `cancelled`, `postponed`, `missing_review`. `src: Data model, rounds`
- [ ] `C-DM-13` `data` A round carries a lap count, a race distance, a circuit length, a first year competed. `src: Data model, rounds`
- [ ] `C-DM-14` `data` A round carries a provider identifier with a provider update instant. `src: Data model, rounds`
- [ ] `C-DM-15` `contract` A round end instant is always after the start instant. `src: Data model, rounds`
- [ ] `C-DM-16` `contract` A race distance is fixed precision rather than floating point. `src: Data model, rounds`
- [ ] `C-DM-17` `contract` A circuit length is fixed precision rather than floating point. `src: Data model, rounds`
- [ ] `C-DM-18` `data` A session slot belongs to a round. `src: Data model, sessions_slots`
- [ ] `C-DM-19` `literal` A session kind is one of `practice`, `qualifying`, `sprint`, `race`. `src: Data model, sessions_slots`
- [ ] `C-DM-20` `data` A session slot carries a label, a position within the round, a start instant. `src: Data model, sessions_slots`
- [ ] `C-DM-21` `data` A session slot carries a flag saying whether the time is confirmed. `src: Data model, sessions_slots`
- [ ] `C-DM-22` `literal` A session slot state is one of `scheduled`, `in_progress`, `complete`, `cancelled`. `src: Data model, sessions_slots`
- [ ] `C-DM-23` `data` A classification belongs to a round with a session slot. `src: Data model, classifications`
- [ ] `C-DM-24` `data` A classification session slot reference is unique. `src: Data model, classifications`
- [ ] `C-DM-25` `literal` A classification status is one of `classified`, `retired`, `disqualified`, `did_not_start`, `did_not_qualify`. `src: Data model, classifications`
- [ ] `C-DM-26` `data` A classification carries a nullable position, a nullable elapsed time, a nullable gap text. `src: Data model, classifications`
- [ ] `C-DM-27` `data` A classification carries a championship total, a constructor name, a provisional flag. `src: Data model, classifications`
- [ ] `C-DM-28` `literal` A classification source is one of `provider`, `manual`. `src: Data model, classifications`
- [ ] `C-DM-29` `contract` A classification carrying a numeric position has the status `classified`. `src: Data model, classifications`
- [ ] `C-DM-30` `contract` A retirement, a disqualification, a non-start are distinct states never collapsed together. `src: Data model, classifications`
- [ ] `C-DM-31` `contract` A classification update whose provider instant is not newer is not applied. `src: Data model, classifications`
- [ ] `C-DM-32` `data` A standing carries a round reference, a position, a championship total, a provider instant. `src: Data model, standings`
- [ ] `C-DM-33` `data` A field override carries an entity type, an entity id, a field name. `src: Data model, field_overrides`
- [ ] `C-DM-34` `data` A field override carries the original value with the override value. `src: Data model, field_overrides`
- [ ] `C-DM-35` `data` A field override carries the editor reference, the creation instant, a nullable release instant. `src: Data model, field_overrides`
- [ ] `C-DM-36` `contract` At most one active override exists per entity type, entity id, field name. `src: Data model, field_overrides`
- [ ] `C-DM-37` `data` A story carries a unique public id with a unique slug. `src: Data model, stories`
- [ ] `C-DM-38` `literal` A story type is one of `story`, `topic`, `quotation`, `legal`. `src: Data model, stories`
- [ ] `C-DM-39` `data` A story carries a title, a body, a nullable attribution. `src: Data model, stories`
- [ ] `C-DM-40` `data` A story carries a nullable publication instant with a nullable scheduled instant. `src: Data model, stories`
- [ ] `C-DM-41` `data` A story carries an author reference with a nullable round reference. `src: Data model, stories`
- [ ] `C-DM-42` `data` A story carries a version number. `src: Data model, stories`
- [ ] `C-DM-43` `contract` A story public id is not derived from the internal identifier. `src: Data model, stories`
- [ ] `C-DM-44` `contract` A story publication instant is stamped on first publication, never rewritten. `src: Data model, stories`
- [ ] `C-DM-45` `contract` A story version rises on every edit. `src: Data model, stories`
- [ ] `C-DM-46` `contract` An edit carrying a stale story version is refused. `src: Data model, stories`
- [ ] `C-DM-47` `contract` A story slug is unique under concurrent creates rather than only in application-level checks. `src: Data model, stories`
- [ ] `C-DM-48` `contract` Two simultaneous creates of one slug never both succeed. `src: Data model, stories`
- [ ] `C-DM-49` `contract` Of two simultaneous creates of one slug exactly one wins, the other is rejected. `src: Data model, stories`
- [ ] `C-DM-50` `contract` A refused concurrent create leaves no orphaned row. `src: Data model, stories`
- [ ] `C-DM-51` `contract` A refused concurrent create leaves no orphaned object. `src: Data model, stories`
- [ ] `C-DM-52` `contract` A second arrival of one ingestion run identifier is refused rather than racing the first. `src: Data model, stories`
- [ ] `C-DM-53` `contract` A second active override on one entity, type, field is refused rather than racing the first. `src: Data model, stories`
- [ ] `C-DM-54` `data` An asset carries a nullable story reference with a storage key. `src: Data model, assets`
- [ ] `C-DM-55` `data` An asset carries a content hash, a width, a height. `src: Data model, assets`
- [ ] `C-DM-56` `data` An asset carries nullable alternative text. `src: Data model, assets`
- [ ] `C-DM-57` `data` An asset carries a caption place with a caption year. `src: Data model, assets`
- [ ] `C-DM-58` `literal` An asset derivative state is one of `pending`, `complete`, `failed`. `src: Data model, assets`
- [ ] `C-DM-59` `contract` An asset storage key holds the object key rather than the bytes. `src: Data model, assets`
- [ ] `C-DM-60` `data` A subscriber carries a unique email address. `src: Data model, subscribers`
- [ ] `C-DM-61` `literal` A subscriber status is one of `pending`, `confirmed`, `unsubscribed`, `suppressed`. `src: Data model, subscribers`
- [ ] `C-DM-62` `data` A subscriber carries a topic list. `src: Data model, subscribers`
- [ ] `C-DM-63` `data` A subscriber carries a unique confirmation token with a unique unsubscribe token. `src: Data model, subscribers`
- [ ] `C-DM-64` `data` A subscriber carries a consent source with a consent instant. `src: Data model, subscribers`
- [ ] `C-DM-65` `data` A subscriber carries a nullable confirmation instant with a nullable unsubscribe instant. `src: Data model, subscribers`
- [ ] `C-DM-66` `data` An enquiry carries a unique reference, a name, an email address. `src: Data model, enquiries`
- [ ] `C-DM-67` `data` An enquiry carries a nullable organisation with a message. `src: Data model, enquiries`
- [ ] `C-DM-68` `literal` An enquiry type is one of `partnership`, `media`, `appearance`, `other`. `src: Data model, enquiries`
- [ ] `C-DM-69` `data` An enquiry carries a consent flag. `src: Data model, enquiries`
- [ ] `C-DM-70` `literal` An enquiry reference is `ENQ-` followed by the id zero padded to five digits. `src: Data model, enquiries`
- [ ] `C-DM-71` `contract` An enquiry reference is derived at insert, then stored so the reference can be quoted back. `src: Data model, enquiries`
- [ ] `C-DM-72` `data` An ingestion run carries a unique run identifier. `src: Data model, ingest_runs`
- [ ] `C-DM-73` `data` An ingestion run carries counts of applied, superseded, conflicted, missing entities. `src: Data model, ingest_runs`
- [ ] `C-DM-74` `contract` The public story count is derived rather than stored. `src: Data model, derived values`
- [ ] `C-DM-75` `contract` The next round is derived rather than stored. `src: Data model, derived values`
- [ ] `C-DM-76` `contract` The driver age is derived from the date of birth rather than stored. `src: Data model, derived values`
- [ ] `C-DM-77` `contract` The championship position ordinal suffix is derived rather than stored. `src: Data model, derived values`
- [ ] `C-DM-78` `contract` The career aggregates on the record route are derived rather than stored. `src: Data model, derived values`
- [ ] `C-DM-79` `literal` The seed carries six rounds of the `2026` `Prime One` season. `src: Data model, seed data`
- [ ] `C-DM-80` `contract` The first three seeded rounds sit at instants already past at seed time. `src: Data model, seed data`
- [ ] `C-DM-81` `contract` The last three seeded rounds sit at instants still ahead at seed time. `src: Data model, seed data`
- [ ] `C-DM-82` `contract` Seeded round instants are computed when the seed runs. `src: Data model, seed data`
- [ ] `C-DM-83` `literal` Seeded round `01` is Verano Grand Prix at the circuit Verano. `src: Data model, seed data`
- [ ] `C-DM-84` `literal` Seeded round `02` is Kestrel Bay Grand Prix at the circuit Kestrel Bay. `src: Data model, seed data`
- [ ] `C-DM-85` `literal` Seeded round `03` is Aldenne Grand Prix at the circuit Aldenne. `src: Data model, seed data`
- [ ] `C-DM-86` `literal` Seeded round `04` is Sundown Grand Prix at the circuit Sundown. `src: Data model, seed data`
- [ ] `C-DM-87` `literal` Seeded round `05` is Port Mira Grand Prix at the circuit Port Mira. `src: Data model, seed data`
- [ ] `C-DM-88` `literal` Seeded round `06` is Caldera Grand Prix at the circuit Caldera. `src: Data model, seed data`
- [ ] `C-DM-89` `data` Each seeded round carries four session slots in the practice, qualifying, sprint, race order. `src: Data model, seed data`
- [ ] `C-DM-90` `data` Each complete seeded round carries one race classification with a numeric position. `src: Data model, seed data`
- [ ] `C-DM-91` `data` Each seeded race classification carries a false provisional flag. `src: Data model, seed data`
- [ ] `C-DM-92` `literal` The seeded story `9f3c1a7d42` is Recovery Drive at Verano in the `published` state. `src: Data model, seed data`
- [ ] `C-DM-93` `literal` The seeded story `4b82e05c17` is Two Tenths at Kestrel Bay in the `published` state. `src: Data model, seed data`
- [ ] `C-DM-94` `literal` The seeded story `d15a6f9b30` is The Aldenne Long Run in the `published` state. `src: Data model, seed data`
- [ ] `C-DM-95` `literal` The seeded story `7e0d4c82a6` is What Sundown Asks For in the `scheduled` state. `src: Data model, seed data`
- [ ] `C-DM-96` `literal` The seeded story `2a9b7f31c8` is The Winter Programme in the `draft` state. `src: Data model, seed data`
- [ ] `C-DM-97` `literal` The seeded story `b63e18a70f` is Off Season in the Workshop in the `in_review` state. `src: Data model, seed data`
- [ ] `C-DM-98` `contract` Every seeded story carries at least one real photograph object in `minio`. `src: Data model, seed data`
- [ ] `C-DM-99` `literal` A photograph object key follows `assets/{asset_id}/{sha256_of_bytes}.{ext}`. `src: Data model, seed data`
- [ ] `C-DM-100` `contract` Seeded photographs are generated procedurally at seed time. `src: Data model, seed data`
- [ ] `C-DM-101` `contract` The photograph of a story that is not public exists, so a refusal is a refusal rather than an absence. `src: Data model, seed data`
- [ ] `C-DM-102` `contract` The photograph on the seeded winter story carries no alternative text. `src: Data model, seed data`
- [ ] `C-DM-103` `contract` Publishing the seeded winter story is blocked until alternative text is set. `src: Data model, seed data`
- [ ] `C-DM-104` `contract` One seeded quotation carries no attribution. `src: Data model, seed data`
- [ ] `C-DM-105` `contract` Publishing the seeded quotation without attribution is blocked. `src: Data model, seed data`
- [ ] `C-DM-106` `literal` The seeded profile nickname is `Milo`. `src: Data model, seed data`
- [ ] `C-DM-107` `literal` The seeded profile monogram is `MR`. `src: Data model, seed data`
- [ ] `C-DM-108` `literal` The seeded profile constructor is `Halcyon`. `src: Data model, seed data`
- [ ] `C-DM-109` `literal` The seeded profile series is `Prime One`. `src: Data model, seed data`
- [ ] `C-DM-110` `literal` The seeded profile debut year is `2019`. `src: Data model, seed data`
- [ ] `C-DM-111` `literal` The seeded profile home town is `Bracken Hill`. `src: Data model, seed data`
- [ ] `C-DM-112` `literal` The seeded profile home country is `Ardenia`. `src: Data model, seed data`
- [ ] `C-DM-113` `data` The seed carries four merchandise items in the curated strip. `src: Data model, seed data`
- [ ] `C-DM-114` `data` One seeded merchandise item is explicitly sold out. `src: Data model, seed data`
- [ ] `C-DM-115` `data` One seeded merchandise item carries a price older than the freshness budget. `src: Data model, seed data`
- [ ] `C-DM-116` `contract` A merchandise item past the freshness budget is shown without a price. `src: Data model, seed data`
- [ ] `C-DM-117` `literal` The seed carries three partner marks in the `title`, `technical`, `official` categories. `src: Data model, seed data`
- [ ] `C-DM-118` `contract` Seeding is idempotent so a restart does not duplicate rows. `src: Data model, seed data`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` One drawing made at a fixed design width is multiplied by a viewport ratio. `src: Front-end specification, scaling model`
- [ ] `C-FE-02` `ui` The viewport ratio is clamped at a lower bound below which the ratio stops shrinking. `src: Front-end specification, scaling model`
- [ ] `C-FE-03` `ui` The viewport ratio is clamped at an upper bound above which the ratio stops growing. `src: Front-end specification, scaling model`
- [ ] `C-FE-04` `ui` A global multiplier scales the whole drawing at once. `src: Front-end specification, scaling model`
- [ ] `C-FE-05` `ui` Rendered sizes are outputs rather than inputs, so a size is never rounded into a step scale. `src: Front-end specification, scaling model`
- [ ] `C-FE-06` `ui` The root size differs by width, so a rem inside the scaled container means a multiple of the fluid unit. `src: Front-end specification, scaling model`
- [ ] `C-FE-07` `ui` A design change is a change to the drawing rather than to a breakpoint. `src: Front-end specification, scaling model`
- [ ] `C-FE-08` `ui` Below the narrow threshold the fluid model is abandoned. `src: Front-end specification, scaling model`
- [ ] `C-FE-09` `ui` The dominant light ground is a near-white neutral that is not white. `src: Front-end specification, colour tokens`
- [ ] `C-FE-10` `ui` A warmer near-white neutral grounds the editorial sections. `src: Front-end specification, colour tokens`
- [ ] `C-FE-11` `ui` A near-white neutral one step below the ground fills light panels. `src: Front-end specification, colour tokens`
- [ ] `C-FE-12` `ui` A workhorse near-white neutral carries the navigation text shadow. `src: Front-end specification, colour tokens`
- [ ] `C-FE-13` `ui` A light neutral carries the divider, disabled tone. `src: Front-end specification, colour tokens`
- [ ] `C-FE-14` `ui` The darkest light-family neutral carries captions on light grounds. `src: Front-end specification, colour tokens`
- [ ] `C-FE-15` `ui` A light warm neutral carries secondary text on the dark routes. `src: Front-end specification, colour tokens`
- [ ] `C-FE-16` `ui` The dominant dark ground is a deep neutral that is not black. `src: Front-end specification, colour tokens`
- [ ] `C-FE-17` `ui` A deep neutral one step above the ground carries raised surfaces on dark. `src: Front-end specification, colour tokens`
- [ ] `C-FE-18` `ui` A mid neutral carries the divider on dark. `src: Front-end specification, colour tokens`
- [ ] `C-FE-19` `ui` A near-black neutral is the reserved true black of the deepest grounds. `src: Front-end specification, colour tokens`
- [ ] `C-FE-20` `ui` The single accent is a mid, vivid lime. `src: Front-end specification, accent table`
- [ ] `C-FE-21` `ui` The resting accent is a mid, vivid lime one step muted. `src: Front-end specification, accent table`
- [ ] `C-FE-22` `ui` The accent at zero alpha is the start stop of the footer gradient. `src: Front-end specification, accent table`
- [ ] `C-FE-23` `ui` The secondary accent is a mid, vivid orange used for alert states. `src: Front-end specification, accent table`
- [ ] `C-FE-24` `ui` The error surface is a light, vivid red appearing nowhere else. `src: Front-end specification, accent table`
- [ ] `C-FE-25` `ui` The dark ground at low alpha draws the contour pattern over light grounds. `src: Front-end specification, colour tokens closing`
- [ ] `C-FE-26` `ui` There is no accent tint ramp of any depth. `src: Front-end specification, palette rule`
- [ ] `C-FE-27` `ui` A receding accent changes to the resting form or drops to nothing. `src: Front-end specification, palette rule`
- [ ] `C-FE-28` `ui` The upper home surface grounds on the light neutral with dark body text. `src: Front-end specification, ground assignment`
- [ ] `C-FE-29` `ui` The editorial home surface grounds on the warmer light neutral. `src: Front-end specification, ground assignment`
- [ ] `C-FE-30` `ui` The record route grounds on the true black with light body text. `src: Front-end specification, ground assignment`
- [ ] `C-FE-31` `ui` The person route grounds on the warmer light neutral. `src: Front-end specification, ground assignment`
- [ ] `C-FE-32` `ui` The season route grounds on the true black with light body text. `src: Front-end specification, ground assignment`
- [ ] `C-FE-33` `ui` The menu overlay grounds on the deep neutral. `src: Front-end specification, ground assignment`
- [ ] `C-FE-34` `ui` The footer grounds on the true black. `src: Front-end specification, ground assignment`
- [ ] `C-FE-35` `ui` The legal routes ground on the light neutral. `src: Front-end specification, ground assignment`
- [ ] `C-FE-36` `ui` The navigation chrome inverts against whatever sits under the chrome. `src: Front-end specification, ground assignment`
- [ ] `C-FE-37` `ui` The inversion is one blend treatment plus a class swap at measured thresholds. `src: Front-end specification, nav inversion`
- [ ] `C-FE-38` `ui` The inversion never uses two copies of the bar. `src: Front-end specification, nav inversion`
- [ ] `C-FE-39` `ui` The store button label is set in the dark ground colour rather than the light one. `src: Front-end specification, contrast obligations`
- [ ] `C-FE-40` `ui` The darkest light-family tone on the warmer ground is permitted only at the caption role. `src: Front-end specification, contrast obligations`
- [ ] `C-FE-41` `ui` The caption role is uppercase, letterspaced. `src: Front-end specification, contrast obligations`
- [ ] `C-FE-42` `ui` The light warm neutral on true black is never reduced below the caption role size. `src: Front-end specification, contrast obligations`
- [ ] `C-FE-43` `ui` A mid-transition frame is never the only frame in which text is legible. `src: Front-end specification, contrast obligations`
- [ ] `C-FE-44` `ui` The structural family is a variable grotesque across a wide axis of cuts. `src: Front-end specification, type`
- [ ] `C-FE-45` `ui` The grotesque is tight, industrial, with wide apertures. `src: Front-end specification, type`
- [ ] `C-FE-46` `ui` The display accent family is a high-contrast display serif at a heavy cut. `src: Front-end specification, type`
- [ ] `C-FE-47` `ui` Both families are declared with a swap display strategy. `src: Front-end specification, type`
- [ ] `C-FE-48` `ui` Both families carry a normative fallback stack. `src: Front-end specification, type`
- [ ] `C-FE-49` `ui` The ramp carries an impact display for the route heroes. `src: Front-end specification, type ramp`
- [ ] `C-FE-50` `ui` The ramp carries a secondary impact display. `src: Front-end specification, type ramp`
- [ ] `C-FE-51` `ui` The ramp carries a menu overlay link at three widths. `src: Front-end specification, type ramp`
- [ ] `C-FE-52` `ui` The ramp carries a section heading with a heading role. `src: Front-end specification, type ramp`
- [ ] `C-FE-53` `ui` The ramp carries a serif pull-quote role. `src: Front-end specification, type ramp`
- [ ] `C-FE-54` `ui` The ramp carries a footer button label at two widths. `src: Front-end specification, type ramp`
- [ ] `C-FE-55` `ui` The ramp carries a body large role with a body regular role. `src: Front-end specification, type ramp`
- [ ] `C-FE-56` `ui` The ramp carries a navigation button label at two widths. `src: Front-end specification, type ramp`
- [ ] `C-FE-57` `ui` The ramp carries a primary button label at three widths. `src: Front-end specification, type ramp`
- [ ] `C-FE-58` `ui` The ramp carries a caption role. `src: Front-end specification, type ramp`
- [ ] `C-FE-59` `ui` Figures align wherever numbers stack. `src: Front-end specification, type ramp`
- [ ] `C-FE-60` `ui` The eyebrow is uppercase, letterspaced, set in the grotesque. `src: Front-end specification, eyebrow`
- [ ] `C-FE-61` `ui` The eyebrow labels every card slot, every statistic, every gallery photograph. `src: Front-end specification, eyebrow`
- [ ] `C-FE-62` `ui` A gallery caption is an eyebrow in the place-comma-year form. `src: Front-end specification, eyebrow`
- [ ] `C-FE-63` `ui` A gallery caption sits above the photograph flush left with the edge of the photograph. `src: Front-end specification, eyebrow`
- [ ] `C-FE-64` `ui` A bar pinned to the top carries the wordmark on the left. `src: Front-end specification, global chrome`
- [ ] `C-FE-65` `ui` The top bar carries the monogram in the centre. `src: Front-end specification, global chrome`
- [ ] `C-FE-66` `ui` The top bar carries the store button at the top right. `src: Front-end specification, global chrome`
- [ ] `C-FE-67` `ui` A menu overlay opens over any route. `src: Front-end specification, global chrome`
- [ ] `C-FE-68` `ui` A footer closes the scrolling content of every route. `src: Front-end specification, global chrome`
- [ ] `C-FE-69` `ui` The store button is a plain cross-origin link to the storefront. `src: Front-end specification, store button`
- [ ] `C-FE-70` `ui` The store button carries the correct rel attributes for a cross-origin destination. `src: Front-end specification, store button`
- [ ] `C-FE-71` `ui` The store button opens in the same tab. `src: Front-end specification, store button`
- [ ] `C-FE-72` `ui` The store button propagates a referral parameter for attribution. `src: Front-end specification, store button`
- [ ] `C-FE-73` `contract` The store button never depends on a live call to the commerce platform. `src: Front-end specification, store button`
- [ ] `C-FE-74` `contract` The store button still works when the commerce platform is down. `src: Front-end specification, store button`
- [ ] `C-FE-75` `ui` The menu overlay sets four destinations plus the business-enquiries surface as oversized links. `src: Front-end specification, menu overlay`
- [ ] `C-FE-76` `ui` The menu overlay creates no history entry. `src: Front-end specification, menu overlay`
- [ ] `C-FE-77` `ui` The browser back button leaves the site rather than closing the overlay. `src: Front-end specification, menu overlay`
- [ ] `C-FE-78` `ui` The menu overlay traps focus for as long as the overlay is open. `src: Front-end specification, menu overlay`
- [ ] `C-FE-79` `ui` The menu overlay returns focus to the control that opened the overlay. `src: Front-end specification, menu overlay`
- [ ] `C-FE-80` `ui` A primary button carries the label twice inside a clipped frame. `src: Front-end specification, duplicate-glyph roll`
- [ ] `C-FE-81` `ui` On hover the label pair rolls so the second copy takes the place of the first. `src: Front-end specification, duplicate-glyph roll`
- [ ] `C-FE-82` `ui` On focus the label pair rolls the same way. `src: Front-end specification, duplicate-glyph roll`
- [ ] `C-FE-83` `ui` The roll is the only label transition on the site. `src: Front-end specification, duplicate-glyph roll`
- [ ] `C-FE-84` `ui` One chevron glyph drawn as inline geometry serves every direction. `src: Front-end specification, chevron`
- [ ] `C-FE-85` `ui` The chevron is rotated in place rather than redrawn per direction. `src: Front-end specification, chevron`
- [ ] `C-FE-86` `ui` A short landscape viewport shows a prompt asking the reader to rotate the device. `src: Front-end specification, rotate-device prompt`
- [ ] `C-FE-87` `ui` The rotate-device prompt is dismissible. `src: Front-end specification, rotate-device prompt`
- [ ] `C-FE-88` `ui` The calendar list mode stays reachable behind the rotate-device prompt. `src: Front-end specification, rotate-device prompt`
- [ ] `C-FE-89` `ui` The footer carries the subscribe form, the social row, the legal links, the partner line. `src: Front-end specification, footer`
- [ ] `C-FE-90` `ui` The footer gradient begins at the zero-alpha stop of the accent. `src: Front-end specification, footer`
- [ ] `C-FE-91` `ui` Footer links carry an animated underline built from two layers that swap on hover. `src: Front-end specification, footer`
- [ ] `C-FE-92` `ui` The next-race card is a small portrait card pinned to the lower left of the home hero. `src: Front-end specification, next-race card`
- [ ] `C-FE-93` `ui` The next-race card carries an eyebrow reading as the next-race label. `src: Front-end specification, next-race card`
- [ ] `C-FE-94` `ui` The next-race card carries a circuit outline drawn in stroke per round. `src: Front-end specification, next-race card`
- [ ] `C-FE-95` `ui` The next-race card carries the circuit name with the round designation. `src: Front-end specification, next-race card`
- [ ] `C-FE-96` `ui` The next-race card carries a rule between the name row, the standing row. `src: Front-end specification, next-race card`
- [ ] `C-FE-97` `ui` The next-race card carries a laurel mark above a two-line standing statement. `src: Front-end specification, next-race card`
- [ ] `C-FE-98` `contract` The next-race card is populated from the next-round query rather than a stored flag. `src: Front-end specification, next-race card`
- [ ] `C-FE-99` `ui` The home composition opens with the hero carrying the helmet plus the next-race card. `src: Front-end specification, route detail home`
- [ ] `C-FE-100` `ui` The home composition carries a split-family statement revealed line by line. `src: Front-end specification, route detail home`
- [ ] `C-FE-101` `ui` The home composition carries a pinned horizontal photograph track. `src: Front-end specification, route detail home`
- [ ] `C-FE-102` `ui` The home composition carries a portrait composition rendered with real depth. `src: Front-end specification, route detail home`
- [ ] `C-FE-103` `ui` The home composition carries a scattered gallery collage with eyebrow captions. `src: Front-end specification, route detail home`
- [ ] `C-FE-104` `ui` The home composition carries a signed pull-quote. `src: Front-end specification, route detail home`
- [ ] `C-FE-105` `ui` The home composition carries a full-bleed oval line composition on a clip scrub. `src: Front-end specification, route detail home`
- [ ] `C-FE-106` `ui` The home composition carries the on-track, off-track split gateway. `src: Front-end specification, route detail home`
- [ ] `C-FE-107` `ui` The home composition carries the livery grid on true black. `src: Front-end specification, route detail home`
- [ ] `C-FE-108` `ui` The home composition carries a partner marquee. `src: Front-end specification, route detail home`
- [ ] `C-FE-109` `ui` The home composition carries a social callout card. `src: Front-end specification, route detail home`
- [ ] `C-FE-110` `ui` The home hero carries no headline in the visible layer. `src: Front-end specification, route detail home`
- [ ] `C-FE-111` `ui` The home heading exists in the document as a visually hidden pair. `src: Front-end specification, route detail home`
- [ ] `C-FE-112` `ui` The record hero is an oversized split-family title with a handwritten accent stroke. `src: Front-end specification, route detail on track`
- [ ] `C-FE-113` `ui` The record hero stroke breaks out of the viewport on the left. `src: Front-end specification, route detail on track`
- [ ] `C-FE-114` `ui` A reserved spacer sits beneath the fixed bar on the record route. `src: Front-end specification, route detail on track`
- [ ] `C-FE-115` `ui` The record statistic strip carries three items on one baseline. `src: Front-end specification, route detail on track`
- [ ] `C-FE-116` `ui` The record statistic strip carries a nickname, an age, a home town with a flag chip. `src: Front-end specification, route detail on track`
- [ ] `C-FE-117` `ui` Each record statistic reveals on a wipe with a per-item stagger. `src: Front-end specification, route detail on track`
- [ ] `C-FE-118` `ui` The record route carries a statement paragraph with a serif accent line. `src: Front-end specification, route detail on track`
- [ ] `C-FE-119` `ui` The race context cluster carries four cards. `src: Front-end specification, route detail on track`
- [ ] `C-FE-120` `ui` The race context cluster cards are the previous round, the next round, the circuit, the standing. `src: Front-end specification, route detail on track`
- [ ] `C-FE-121` `ui` The previous round card is visually recessed relative to the next round card. `src: Front-end specification, route detail on track`
- [ ] `C-FE-122` `ui` The race context cluster is complete in the first viewport after the hero at every width. `src: Front-end specification, route detail on track`
- [ ] `C-FE-123` `ui` The record route carries the career statistics. `src: Front-end specification, route detail on track`
- [ ] `C-FE-124` `ui` The record results table lists every classified finish in reverse chronological order. `src: Front-end specification, route detail on track`
- [ ] `C-FE-125` `ui` The record route carries a podium gallery with a signed pull-quote. `src: Front-end specification, route detail on track`
- [ ] `C-FE-126` `ui` The person route grounds on the warmer light neutral. `src: Front-end specification, route detail off track`
- [ ] `C-FE-127` `ui` Person topic sections alternate side by side. `src: Front-end specification, route detail off track`
- [ ] `C-FE-128` `ui` Each person topic carries a name, a description, a gallery collage. `src: Front-end specification, route detail off track`
- [ ] `C-FE-129` `ui` Person topic order is taken from the record rather than the template. `src: Front-end specification, route detail off track`
- [ ] `C-FE-130` `literal` A seeded person topic is `Padel tennis`. `src: Front-end specification, route detail off track`
- [ ] `C-FE-131` `literal` A seeded person topic is `Music`. `src: Front-end specification, route detail off track`
- [ ] `C-FE-132` `ui` A person pull-quote carries the highlighter treatment in the accent. `src: Front-end specification, route detail off track`
- [ ] `C-FE-133` `ui` The season hero is a two-line split-family title. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-134` `contract` The season year is rendered from the current season record rather than a template literal. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-135` `ui` A large handwritten accent stroke is scrawled across both season hero lines. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-136` `ui` The season header bar carries a two-line summary revealed per line. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-137` `ui` The season header bar carries the standing as an eyebrow above a large numeral. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-138` `ui` The standing numeral carries a superscript ordinal. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-139` `ui` The season header bar carries the round as an eyebrow above a large numeral. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-140` `ui` The season header bar carries the visualiser control beside the list control. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-141` `ui` The featured round panel is bordered in the accent. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-142` `ui` The featured round panel sets the circuit name vertically at impact scale on the left edge. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-143` `ui` The featured round panel carries a country flag chip beneath the vertical circuit name. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-144` `ui` The featured round panel carries a when-label above the date range, month. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-145` `ui` The featured round panel carries the circuit length with the first year competed. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-146` `ui` The featured round panel carries the race distance with the lap count. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-147` `ui` The featured round panel carries an eyebrow naming the driver, circuit. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-148` `ui` The featured round panel carries a short editorial note. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-149` `ui` Large numerals in the featured panel are set in the accent. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-150` `ui` The month in the featured panel is set in the light ground colour. `src: Front-end specification, route detail calendar`
- [ ] `C-FE-151` `ui` Each schedule row carries a session name in uppercase. `src: Front-end specification, schedule table`
- [ ] `C-FE-152` `ui` Each schedule row carries a day with an abbreviated month. `src: Front-end specification, schedule table`
- [ ] `C-FE-153` `ui` Each schedule row carries a local start time on a 24-hour clock. `src: Front-end specification, schedule table`
- [ ] `C-FE-154` `contract` A session crossing midnight in the visitor zone renders correctly. `src: Front-end specification, schedule table`
- [ ] `C-FE-155` `contract` A session inside a daylight-saving transition renders correctly. `src: Front-end specification, schedule table`
- [ ] `C-FE-156` `ui` The list mode presents the season as rows. `src: Front-end specification, view modes`
- [ ] `C-FE-157` `ui` The visualiser mode draws the circuit outline at scale with the annotations. `src: Front-end specification, view modes`
- [ ] `C-FE-158` `ui` Both calendar modes create history entries. `src: Front-end specification, view modes`
- [ ] `C-FE-159` `ui` The track visualiser draws a single circuit outline from a stored two-dimensional path. `src: Front-end specification, track visualiser`
- [ ] `C-FE-160` `ui` The track visualiser scales the outline to the frame. `src: Front-end specification, track visualiser`
- [ ] `C-FE-161` `ui` Annotations are placed at a normalised distance along the lap. `src: Front-end specification, track visualiser`
- [ ] `C-FE-162` `ui` A collision rule drops the lower-ranked label when two annotations overlap. `src: Front-end specification, track visualiser`
- [ ] `C-FE-163` `ui` The start marker is always drawn. `src: Front-end specification, track visualiser`
- [ ] `C-FE-164` `ui` Where the path is absent the panel shows the round without the drawing. `src: Front-end specification, track visualiser`
- [ ] `C-FE-165` `ui` The story detail route opens with the photograph as the hero. `src: Front-end specification, story detail`
- [ ] `C-FE-166` `ui` The story detail title uses the split-family device. `src: Front-end specification, story detail`
- [ ] `C-FE-167` `ui` The story detail eyebrow carries the round association where one exists. `src: Front-end specification, story detail`
- [ ] `C-FE-168` `ui` The story body is an ordered sequence of blocks. `src: Front-end specification, story detail`
- [ ] `C-FE-169` `ui` The story block vocabulary is a text block, a full-bleed band, a two-up pair, a pull-quote. `src: Front-end specification, story detail`
- [ ] `C-FE-170` `ui` The story gallery renders place-comma-year captions. `src: Front-end specification, story detail`
- [ ] `C-FE-171` `ui` Each legal route carries a single rich field. `src: Front-end specification, legal and not found`
- [ ] `C-FE-172` `ui` Each legal route shows the last-updated instant taken from the publication instant. `src: Front-end specification, legal and not found`
- [ ] `C-FE-173` `ui` The not-found route carries the wordmark large on the true black ground. `src: Front-end specification, legal and not found`
- [ ] `C-FE-174` `ui` A full-viewport real-time layer is composited behind the flat content. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-175` `ui` The real-time layer renders the helmet as the home hero. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-176` `ui` The real-time layer renders the portrait composition as a displaced masked plane. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-177` `ui` The real-time layer renders the livery collection. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-178` `ui` One persistent rendering context serves the whole session. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-179` `ui` The rendering context is transparent-backed so the page ground shows through. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-180` `ui` The rendering context is capped at a device pixel ratio of two. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-181` `ui` The render loop pauses when nothing is animating. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-182` `ui` The render loop pauses when the tab is hidden. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-183` `ui` The render loop resumes on interaction. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-184` `contract` The real-time layer degrades to a still frame on a weak graphics chip. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-185` `ui` A portrait responds to pointer position with a small parallax derived from real depth. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-186` `ui` A portrait falls back to a flat masked image with a soft drop shadow. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-187` `contract` The page remains fully usable with the real-time layer unavailable. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-188` `contract` No content depends on the real-time layer. `src: Front-end specification, three-dimensional layer`
- [ ] `C-FE-189` `ui` The helmet reads as a lacquered shell with a clear coat over a base. `src: Front-end specification, materials`
- [ ] `C-FE-190` `ui` A fine flake in the helmet base breaks up under a moving light. `src: Front-end specification, materials`
- [ ] `C-FE-191` `ui` A separate matte material carries the visor seal. `src: Front-end specification, materials`
- [ ] `C-FE-192` `ui` The portrait plane carries a depth, an alpha, a soft shadow map. `src: Front-end specification, materials`
- [ ] `C-FE-193` `ui` Every material is generated in code rather than loading a texture file. `src: Front-end specification, materials`
- [ ] `C-FE-194` `ui` The lighting rig is one key light, one low fill, one rim light picked from the accent. `src: Front-end specification, lighting`
- [ ] `C-FE-195` `ui` The accent appears on the helmet as a lit edge rather than a painted stripe. `src: Front-end specification, lighting`
- [ ] `C-FE-196` `ui` The lighting rig is fixed to the camera rather than to the scene. `src: Front-end specification, lighting`
- [ ] `C-FE-197` `constraint` There is no audio layer on the site. `src: Front-end specification, audio`
- [ ] `C-FE-198` `constraint` Nothing on the site plays a sound. `src: Front-end specification, audio`
- [ ] `C-FE-199` `ui` One long, hard, late-settling ease is the default motion of the site. `src: Front-end specification, motion language`
- [ ] `C-FE-200` `ui` A heading reveals line by line on a wipe from the left. `src: Front-end specification, motion language`
- [ ] `C-FE-201` `ui` A photograph enters on a mask that opens from the edge of the photograph. `src: Front-end specification, motion language`
- [ ] `C-FE-202` `ui` The accent stroke draws itself across the hero from left to right. `src: Front-end specification, motion language`
- [ ] `C-FE-203` `ui` The partner marquee travels continuously without pausing on hover. `src: Front-end specification, motion language`
- [ ] `C-FE-204` `ui` The highlighter sweeps behind a pull-quote line as the line enters. `src: Front-end specification, motion language`
- [ ] `C-FE-205` `ui` The pinned photograph track scrubs continuously across scroll frames. `src: Front-end specification, motion language`
- [ ] `C-FE-206` `ui` The gallery collage parallax scrubs continuously across scroll frames. `src: Front-end specification, motion language`
- [ ] `C-FE-207` `ui` The oval clip scrubs continuously across scroll frames. `src: Front-end specification, motion language`
- [ ] `C-FE-208` `ui` The split gateway counter-scrub runs across scroll frames. `src: Front-end specification, motion language`
- [ ] `C-FE-209` `ui` The social callout travels on a sticky scrub. `src: Front-end specification, motion language`
- [ ] `C-FE-210` `ui` Ordinary scrolling on the reading routes is eased rather than native. `src: Front-end specification, motion language`
- [ ] `C-FE-211` `ui` Under reduced motion the scrubbed compositions settle at the resting frame. `src: Front-end specification, reduced motion`
- [ ] `C-FE-212` `ui` Under reduced motion the marquee holds. `src: Front-end specification, reduced motion`
- [ ] `C-FE-213` `ui` Under reduced motion the accent stroke is drawn complete rather than animating. `src: Front-end specification, reduced motion`
- [ ] `C-FE-214` `ui` The preloader covers the first paint until the shell resolves. `src: Front-end specification, first load`
- [ ] `C-FE-215` `ui` The preloader carries the wordmark with a progress indication on the dark ground. `src: Front-end specification, first load`
- [ ] `C-FE-216` `ui` The preloader tears down once the shell is ready. `src: Front-end specification, first load`
- [ ] `C-FE-217` `ui` The chrome performs an entrance after the preloader tears down. `src: Front-end specification, first load`
- [ ] `C-FE-218` `ui` The preloader waits at a near-complete state rather than snapping. `src: Front-end specification, first load`
- [ ] `C-FE-219` `ui` The preloader does not block interaction past the exit of the preloader. `src: Front-end specification, first load`
- [ ] `C-FE-220` `ui` Every icon is inline vector geometry rather than a shipped file. `src: Front-end specification, iconography`
- [ ] `C-FE-221` `ui` An icon inherits the current text colour unless a fill is stated. `src: Front-end specification, iconography`
- [ ] `C-FE-222` `ui` The icon set covers the monogram mark, the laurel, the flag chip, the arrow-out. `src: Front-end specification, iconography`
- [ ] `C-FE-223` `ui` The icon set covers the social marks, the card frame, the handwritten signature form. `src: Front-end specification, iconography`
- [ ] `C-FE-224` `ui` The signature form appears as the hero stroke, the standing signature, the highlighter. `src: Front-end specification, iconography`
- [ ] `C-FE-225` `ui` At the desktop range the full chrome, the fluid scaling model hold. `src: Front-end specification, responsive`
- [ ] `C-FE-226` `ui` At the desktop range the four-card race context cluster holds. `src: Front-end specification, responsive`
- [ ] `C-FE-227` `ui` At the tablet range the bar compresses to the wordmark, the monogram, the store button. `src: Front-end specification, responsive`
- [ ] `C-FE-228` `ui` At the tablet range the reading layout becomes one column. `src: Front-end specification, responsive`
- [ ] `C-FE-229` `ui` At the tablet range the race context cluster stacks two by two. `src: Front-end specification, responsive`
- [ ] `C-FE-230` `ui` Below the narrow threshold the fluid model is abandoned for a fixed root. `src: Front-end specification, responsive`
- [ ] `C-FE-231` `ui` Below the narrow threshold the schedule table becomes a stack of rows. `src: Front-end specification, responsive`
- [ ] `C-FE-232` `ui` A print stylesheet drops the chrome, the real-time layer, every scrubbed composition. `src: Front-end specification, print`
- [ ] `C-FE-233` `ui` The print stylesheet sets the body in the grotesque on white. `src: Front-end specification, print`
- [ ] `C-FE-234` `ui` The print stylesheet prints the calendar as a plain table with repeated headers. `src: Front-end specification, print`
- [ ] `C-FE-235` `ui` The print stylesheet prints the results table as a plain table with repeated headers. `src: Front-end specification, print`
- [ ] `C-FE-236` `ui` The layout is expressed in logical start, logical end rather than left, right. `src: Front-end specification, reading direction`
- [ ] `C-FE-237` `ui` The accent stroke mirrors with the writing direction. `src: Front-end specification, reading direction`
- [ ] `C-FE-238` `ui` The chevron mirrors with the writing direction. `src: Front-end specification, reading direction`
- [ ] `C-FE-239` `ui` Every route carries one `main` landmark. `src: Front-end specification, accessibility`
- [ ] `C-FE-240` `ui` Every route carries a labelled navigation landmark. `src: Front-end specification, accessibility`
- [ ] `C-FE-241` `ui` Every route carries a labelled `contentinfo` footer. `src: Front-end specification, accessibility`
- [ ] `C-FE-242` `ui` Every results row is reachable from the keyboard. `src: Front-end specification, accessibility`
- [ ] `C-FE-243` `ui` The two view-mode controls are real buttons. `src: Front-end specification, accessibility`
- [ ] `C-FE-244` `ui` The timezone control is a real button. `src: Front-end specification, accessibility`
- [ ] `C-FE-245` `ui` The menu overlay returns focus on Escape. `src: Front-end specification, accessibility`
- [ ] `C-FE-246` `ui` The enquiry error summary links each error to the field of the error. `src: Front-end specification, accessibility`
- [ ] `C-FE-247` `ui` A message beneath a field is associated with that field programmatically. `src: Front-end specification, accessibility`
- [ ] `C-FE-248` `ui` A decorative photograph declares itself decorative. `src: Front-end specification, accessibility`
- [ ] `C-FE-249` `ui` The focus ring is visible on every surface, the inverted ones too. `src: Front-end specification, accessibility`
- [ ] `C-FE-250` `ui` The styles covering the first viewport are inlined. `src: Front-end specification, performance`
- [ ] `C-FE-251` `ui` Every script is deferred so nothing script-shaped blocks the render. `src: Front-end specification, performance`
- [ ] `C-FE-252` `constraint` Development tooling is stripped from the production build. `src: Front-end specification, performance`
- [ ] `C-FE-253` `ui` Numbers carry locale-aware separators. `src: Front-end specification, performance`
- [ ] `C-FE-254` `ui` The workspace sorts with locale-aware collation. `src: Front-end specification, performance`
- [ ] `C-FE-255` `ui` Photographs load lazily in view order behind a placeholder. `src: Front-end specification, performance`
- [ ] `C-FE-256` `ui` The placeholder is derived from the stored dominant colour. `src: Front-end specification, performance`
- [ ] `C-FE-257` `ui` Nothing blocks first paint except the preloader. `src: Front-end specification, performance`
- [ ] `C-FE-258` `contract` The build is one shell holding the persistent chrome plus a routed content region. `src: Front-end specification, module architecture`
- [ ] `C-FE-259` `contract` The rendering context survives a route change. `src: Front-end specification, module architecture`
- [ ] `C-FE-260` `contract` A data layer owns every read, every write. `src: Front-end specification, module architecture`
- [ ] `C-FE-261` `contract` The data layer is the only place a scope is applied. `src: Front-end specification, module architecture`
- [ ] `C-FE-262` `contract` A domain layer owns the derived values. `src: Front-end specification, module architecture`
- [ ] `C-FE-263` `contract` A presentation layer reads from the domain layer, writes to nothing else. `src: Front-end specification, module architecture`
- [ ] `C-FE-264` `ui` One reveal primitive taking an offset with a stagger drives every entrance. `src: Front-end specification, module architecture`
- [ ] `C-FE-265` `constraint` The only principals are the four roles plus the anonymous visitor plus the ingestion run. `src: Front-end specification, principals`
- [ ] `C-FE-266` `constraint` A confirmed subscriber is an address rather than an account. `src: Front-end specification, principals`
- [ ] `C-FE-267` `data` An integration record names a kind, a state, a reference to where credentials live. `src: Front-end specification, integrations`
- [ ] `C-FE-268` `data` An integration record carries the last success instant with the last failure instant. `src: Front-end specification, integrations`
- [ ] `C-FE-269` `contract` An integration record never holds the credentials of the integration. `src: Front-end specification, integrations`
- [ ] `C-FE-270` `contract` The integration records drive the third-party list on the privacy route. `src: Front-end specification, integrations`
- [ ] `C-FE-271` `contract` The public site stays fully functional with the feed unreachable for longer than a race weekend. `src: Front-end specification, resilience`
- [ ] `C-FE-272` `contract` The public site serves the last good data rather than degrading to empty. `src: Front-end specification, resilience`
- [ ] `C-FE-273` `contract` Schema migrations run as an explicit deployment step rather than on application start. `src: Front-end specification, resilience`
- [ ] `C-FE-274` `contract` A migration changing a column in use ships as expand, then migrate, then contract. `src: Front-end specification, resilience`
- [ ] `C-FE-275` `contract` A story moves through draft, review, scheduled or published, then unpublished or archived. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-276` `contract` The review step is the only approval in the product. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-277` `contract` An editor may return a record to `draft` with a note. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-278` `constraint` There is no multi-stage approval chain. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-279` `constraint` There is no delegation of the review step. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-280` `constraint` There is no escalation on timeout. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-281` `contract` A correction to a published record raises a revision, republishes in place. `src: Front-end specification, editorial workflow`
- [ ] `C-FE-282` `ui` The workspace shows every ingestion run with the counts of the run. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-283` `ui` A round in `missing_review` is listed for a person to decide on. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-284` `ui` A conflict lists the field, the stored override, the incoming value. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-285` `contract` An override stands until a person releases the override. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-286` `contract` A run that times out retries on a jittered exponential backoff to a bounded ceiling. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-287` `contract` A run never retries a rejected credential in a loop. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-288` `ui` Historical seasons carry a relaxed budget raising a dashboard notice only. `src: Front-end specification, ingestion surface`
- [ ] `C-FE-289` `contract` The only measurement is recorded in the own tables of the app. `src: Front-end specification, analytics`
- [ ] `C-FE-290` `contract` Measurement covers route views, the subscribe funnel, the enquiry funnel, the store departure. `src: Front-end specification, analytics`
- [ ] `C-FE-291` `constraint` There is no third-party tag. `src: Front-end specification, analytics`
- [ ] `C-FE-292` `constraint` There is no external beacon. `src: Front-end specification, analytics`
- [ ] `C-FE-293` `contract` Everything held about a subscriber can be exported for that address. `src: Front-end specification, analytics`
- [ ] `C-FE-294` `contract` Everything held about a subscriber can be deleted for that address. `src: Front-end specification, analytics`
- [ ] `C-FE-295` `contract` A deletion leaves only a suppression record retaining no address in clear. `src: Front-end specification, analytics`
- [ ] `C-FE-296` `literal` The chrome wordmark reads `Milo Rennick`. `src: Front-end specification, copy deck`
- [ ] `C-FE-297` `literal` The chrome monogram reads `MR`. `src: Front-end specification, copy deck`
- [ ] `C-FE-298` `literal` The store button label reads `Store`. `src: Front-end specification, copy deck`
- [ ] `C-FE-299` `literal` The menu destinations read `Home`, `On Track`, `Off Track`, `Calendar`. `src: Front-end specification, copy deck`
- [ ] `C-FE-300` `literal` The menu carries `Business enquiries`. `src: Front-end specification, copy deck`
- [ ] `C-FE-301` `literal` The home next-race eyebrow reads `Next race`. `src: Front-end specification, copy deck`
- [ ] `C-FE-302` `literal` The home teaser strip label reads `Latest`. `src: Front-end specification, copy deck`
- [ ] `C-FE-303` `literal` The record statistic labels read `Nickname`, `Age`, `Home`. `src: Front-end specification, copy deck`
- [ ] `C-FE-304` `literal` The record career heading reads `The record`. `src: Front-end specification, copy deck`
- [ ] `C-FE-305` `literal` The results table columns read `Round`, `Date`, `Position`, `Time`. `src: Front-end specification, copy deck`
- [ ] `C-FE-306` `literal` The season header labels read `Standing`, `Round`. `src: Front-end specification, copy deck`
- [ ] `C-FE-307` `literal` The featured panel labels read `When`, `Circuit length`, `Race distance`, `Laps`, `First competed`. `src: Front-end specification, copy deck`
- [ ] `C-FE-308` `literal` The two calendar mode controls read `Visualiser`, `List`. `src: Front-end specification, copy deck`
- [ ] `C-FE-309` `literal` The subscribe field label reads `Email address`. `src: Front-end specification, copy deck`
- [ ] `C-FE-310` `literal` The enquiry field labels read `Name`, `Email address`, `Organisation`, `Enquiry type`, `Message`. `src: Front-end specification, copy deck`
- [ ] `C-FE-311` `literal` The not-found heading reads `Page not found`. `src: Front-end specification, copy deck`
- [ ] `C-FE-312` `constraint` Nothing in the build depends on a binary file. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-313` `constraint` The helmet, the portrait plane, the livery forms are generated as geometry at start-up. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-314` `constraint` Circuit outlines, the laurel, the flag chips, the signature strokes are inline vector geometry. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-315` `constraint` The typefaces come from the platform stack or a webfont fetched at build time. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-316` `constraint` No font binary ships in the repository. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-317` `constraint` Grain is generated as a noise pass rather than a tiled image. `src: Front-end specification, zero-asset substitution`
- [ ] `C-FE-318` `ui` The story detail template is reconstructed rather than measured. `src: Front-end specification, evidence gaps`
- [ ] `C-FE-319` `ui` The three-dimensional scene graph is reconstructed rather than measured. `src: Front-end specification, evidence gaps`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` There is one brand, one workspace, one production environment. `src: Constraints`
- [ ] `C-CN-02` `constraint` There is no fan profile. `src: Constraints`
- [ ] `C-CN-03` `constraint` There is no saved item feature. `src: Constraints`
- [ ] `C-CN-04` `constraint` There is no user-generated content of any kind. `src: Constraints`
- [ ] `C-CN-05` `constraint` There is no moderation queue. `src: Constraints`
- [ ] `C-CN-06` `constraint` There is no cart. `src: Constraints`
- [ ] `C-CN-07` `constraint` There is no inventory feature. `src: Constraints`
- [ ] `C-CN-08` `constraint` There is no tax calculation. `src: Constraints`
- [ ] `C-CN-09` `constraint` There is no fulfilment feature. `src: Constraints`
- [ ] `C-CN-10` `constraint` There is no card capture. `src: Constraints`
- [ ] `C-CN-11` `constraint` There is no live telemetry surface. `src: Constraints`
- [ ] `C-CN-12` `constraint` There is no lap-by-lap timing screen. `src: Constraints`
- [ ] `C-CN-13` `constraint` There is no federated sign-on. `src: Constraints`
- [ ] `C-CN-14` `constraint` There is no permission scheme beyond the four roles. `src: Constraints`
- [ ] `C-CN-15` `constraint` No email is sent by the app. `src: Constraints`
- [ ] `C-CN-16` `constraint` Subscription confirmation travels as a token the API returns. `src: Constraints`
- [ ] `C-CN-17` `constraint` Unsubscription travels as a token the API returns. `src: Constraints`
- [ ] `C-CN-18` `constraint` Enquiries are read in the workspace rather than mailed. `src: Constraints`
- [ ] `C-CN-19` `constraint` There are no external network calls at run time. `src: Constraints`
- [ ] `C-CN-20` `constraint` A visitor request never fans out to the timing provider. `src: Constraints`
- [ ] `C-CN-21` `constraint` There is no analytics vendor. `src: Constraints`
- [ ] `C-CN-22` `constraint` No binary asset ships with the build. `src: Constraints`
- [ ] `C-CN-23` `constraint` Every photograph, icon, circuit outline, three-dimensional form is generated in code. `src: Constraints`
- [ ] `C-CN-24` `constraint` The app stays responsive with a season of 500 rounds. `src: Constraints`
- [ ] `C-CN-25` `constraint` The app stays responsive with 5,000 stored subscribers. `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract bullet 1`
- [ ] `C-DC-02` `literal` The port mapping is `${APP_PUBLIC_PORT}:4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-03` `literal` The container-internal port is `4173`. `src: Deployment contract bullet 1`
- [ ] `C-DC-04` `contract` The public port is read from the environment rather than hardcoded. `src: Deployment contract bullet 1`
- [ ] `C-DC-05` `literal` The HTTP API is served on the same origin under the `/api` prefix. `src: Deployment contract bullet 2`
- [ ] `C-DC-06` `contract` The health route returns a success status once the app is ready. `src: Deployment contract bullet 3`
- [ ] `C-DC-07` `contract` The app starts from the environment image with no manual steps. `src: Deployment contract bullet 4`
- [ ] `C-DC-08` `literal` Login credentials are written to `/app/USER_README.md`. `src: Deployment contract bullet 5`
- [ ] `C-DC-09` `literal` A reserved `.browser_screenshots/` directory exists at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-10` `literal` A reserved `.downloads/` directory exists at the app root. `src: Deployment contract bullet 6`
- [ ] `C-DC-11` `contract` Both reserved directories are empty. `src: Deployment contract bullet 6`
- [ ] `C-DC-12` `contract` A production build is served behind a static or preview server. `src: Deployment contract bullet 7`
- [ ] `C-DC-13` `contract` A development server is never served. `src: Deployment contract bullet 7`
- [ ] `C-DC-14` `contract` The server keeps running after the session ends. `src: Deployment contract bullet 8`
- [ ] `C-DC-15` `contract` The server is not a child of the shell. `src: Deployment contract bullet 8`
- [ ] `C-DC-16` `literal` The listener binds `0.0.0.0` rather than a loopback address. `src: Deployment contract bullet 9`
- [ ] `C-DC-17` `contract` The backing services are already running, reachable at the environment variables. `src: Deployment contract bullet 10`
- [ ] `C-DC-18` `constraint` No copy of a backing service is downloaded, installed, compiled, started. `src: Deployment contract bullet 10`
- [ ] `C-DC-19` `constraint` Only the providers named in the brief are used. `src: Deployment contract bullet 11`
- [ ] `C-DC-20` `constraint` There are no edge functions. `src: Deployment contract bullet 11`
- [ ] `C-DC-21` `constraint` There are no persistent volumes. `src: Deployment contract bullet 12`
- [ ] `C-DC-22` `constraint` There are no fixed container names. `src: Deployment contract bullet 12`
- [ ] `C-DC-23` `constraint` There are no custom networks. `src: Deployment contract bullet 12`
- [ ] `C-DC-24` `literal` The signup endpoint is `POST /api/auth/signup`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-25` `literal` The login endpoint is `POST /api/auth/login`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-26` `literal` The health endpoint is `GET /api/health`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-27` `literal` The public story list endpoint is `GET /api/stories`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-28` `literal` The public story count endpoint is `GET /api/stories/count`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-29` `literal` The public story detail endpoint is `GET /api/stories/{}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-30` `literal` The photograph bytes endpoint is `GET /api/assets/{}/file`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-31` `literal` The season endpoint is `GET /api/season`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-32` `literal` The next-round endpoint is `GET /api/season/next-round`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-33` `literal` The results endpoint is `GET /api/results`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-34` `literal` The standings endpoint is `GET /api/standings`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-35` `literal` The profile endpoint is `GET /api/profile`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-36` `literal` The merchandise endpoint is `GET /api/merch`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-37` `literal` The partner endpoint is `GET /api/partners`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-38` `literal` The subscribe endpoint is `POST /api/subscribers`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-39` `literal` The confirmation endpoint is `POST /api/subscribers/confirm`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-40` `literal` The unsubscribe endpoint is `POST /api/subscribers/unsubscribe`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-41` `literal` The enquiry endpoint is `POST /api/enquiries`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-42` `literal` The workspace story list endpoint is `GET /api/studio/stories`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-43` `literal` The story create endpoint is `POST /api/studio/stories`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-44` `literal` The photograph upload endpoint is `POST /api/studio/stories/{}/assets`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-45` `literal` The upload multipart field is named `file`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-46` `literal` The asset patch endpoint is `PATCH /api/studio/assets/{}`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-47` `literal` The submit endpoint is `POST /api/studio/stories/{}/submit`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-48` `literal` The publish endpoint is `POST /api/studio/stories/{}/publish`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-49` `literal` The unpublish endpoint is `POST /api/studio/stories/{}/unpublish`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-50` `literal` The ingestion endpoint is `POST /api/studio/ingest`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-51` `literal` The ingestion run list endpoint is `GET /api/studio/ingest/runs`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-52` `literal` The override endpoint is `POST /api/studio/overrides`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-53` `literal` The enquiry inbox endpoint is `GET /api/studio/enquiries`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-54` `literal` The subscriber list endpoint is `GET /api/studio/subscribers`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-55` `literal` The editor list endpoint is `GET /api/studio/editors`. `src: Deployment contract, API shapes table`
- [ ] `C-DC-56` `contract` The public story list returns a top-level JSON array. `src: Deployment contract, API shapes table`
- [ ] `C-DC-57` `contract` The results endpoint returns a top-level JSON array. `src: Deployment contract, API shapes table`
- [ ] `C-DC-58` `contract` The merchandise price is displayed in the currency the platform reports. `src: Deployment contract, API shapes table`
- [ ] `C-DC-59` `contract` The merchandise price carries no local conversion. `src: Deployment contract, API shapes table`
- [ ] `C-DC-60` `contract` Field names in the API shapes table are exact. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-61` `contract` Bearer auth is required on everything except login, signup, health. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-62` `contract` Every public read accepts an anonymous caller. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-63` `contract` The subscribe, confirm, unsubscribe, enquiry writes accept an anonymous caller. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-64` `contract` A successful call returns the named shape. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-65` `contract` An invalid call is rejected as a client error. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-66` `literal` A rejected call never returns a `5xx` status. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-67` `contract` A rejected call is never a silent success. `src: Deployment contract, API shapes closing para`
- [ ] `C-DC-68` `constraint` An in-memory object map holding uploaded bytes is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-69` `constraint` Photograph bytes written to the app container filesystem are a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-70` `constraint` A database column carrying base64 image data is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-71` `constraint` A hardcoded upload response the app returns to itself is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-72` `constraint` A season served from a JSON file in the repository is a contract violation. `src: Deployment contract, no mocks`
- [ ] `C-DC-73` `constraint` The app tables can only reflect what lives in the provider. `src: Deployment contract, no mocks`

## Pinned literals

| Value | What it is | Item | Source |
|---|---|---|---|
| `deku-demo-pw-2026` | the corpus password every seeded account uses | C-RL-50 | User roles closing para |
| `owner@example.com` | seeded owner account | C-RL-51 | User roles closing para |
| `editor@example.com` | seeded editor account | C-RL-52 | User roles closing para |
| `contributor@example.com` | seeded contributor account | C-RL-53 | User roles closing para |
| `visitor@example.com` | seeded visitor account | C-RL-54 | User roles closing para |
| `draft` | the initial story state | C-RL-10 | Core features, editorial state |
| `in_review` | the submitted story state | C-RL-11 | Core features, editorial state |
| `scheduled` | the approved future story state | C-RL-12 | Core features, editorial state |
| `published` | the live story state | C-CF-01 | Core features, editorial state |
| `unpublished` | the withdrawn story state | C-RL-13 | Core features, editorial state |
| `archived` | the retired story state | C-RL-14 | Core features, editorial state |
| `3 stories` | the seeded public story count | C-CF-11 | Core features, editorial state |
| `4 stories` | the public story count after one publish | C-CF-12 | Core features, editorial state |
| `quotation` | the content type that owes an attribution | C-CF-23 | Core features, publishing |
| `contributor` | the lowest workspace role | C-RL-22 | Core features, photograph boundary |
| `editor` | the publishing role | C-RL-32 | Core features, photograph boundary |
| `owner` | the settings role | C-RL-41 | Core features, photograph boundary |
| `visitor` | the public role | C-RL-01 | User roles table |
| `pending` | the unconfirmed subscriber status | C-CF-59 | Core features, subscribing |
| `confirmed` | the confirmed subscriber status | C-CF-62 | Core features, subscribing |
| `suppressed` | the suppressed subscriber status | C-CF-72 | Core features, subscribing |
| `/legal/privacy-policy` | the privacy route | C-CF-75 | Core features, public pages |
| `/legal/terms-conditions` | the terms route | C-CF-81 | Core features, public pages |
| `Back to the season` | the not-found action label | C-CF-84 | Core features, public pages |
| `Back shortly. We are making a change.` | the maintenance copy | C-CF-102 | Core features, public pages |
| `round` | an ingestion entity type | C-CF-171 | Season data and the feed |
| `session` | an ingestion entity type | C-CF-171 | Season data and the feed |
| `classification` | an ingestion entity type | C-CF-171 | Season data and the feed |
| `standing` | an ingestion entity type | C-CF-171 | Season data and the feed |
| `providerUpdatedAt` | the provider update instant on an entity | C-CF-173 | Season data and the feed |
| `sessionKind` | a classification entity field | C-CF-174 | Season data and the feed |
| `position` | a classification entity field | C-CF-174 | Season data and the feed |
| `status` | a classification entity field | C-CF-174 | Season data and the feed |
| `provisional` | a classification entity field | C-CF-174 | Season data and the feed |
| `state` | a round entity field | C-CF-175 | Season data and the feed |
| `type` | the entity discriminator | C-CF-171 | Season data and the feed |
| `applied` | an ingestion response count | C-CF-177 | Season data and the feed |
| `superseded` | an ingestion response count | C-CF-177 | Season data and the feed |
| `conflicted` | an ingestion response count | C-CF-177 | Season data and the feed |
| `missing` | an ingestion response count | C-CF-177 | Season data and the feed |
| `duplicate` | the replay flag on an ingestion response | C-CF-178 | Season data and the feed |
| `missing_review` | the state of a round absent from a payload | C-CF-152 | Season data and the feed |
| `complete` | a finished round state | C-CF-160 | Season data and the feed |
| `cancelled` | an abandoned round state | C-CF-160 | Season data and the feed |
| `/` | the home route | C-UF-01 | User flow route table |
| `/on-track` | the record route | C-UF-02 | User flow route table |
| `/off-track` | the person route | C-UF-03 | User flow route table |
| `/calendar` | the season route | C-UF-04 | User flow route table |
| `/stories/:public_id` | the story detail route | C-UF-05 | User flow route table |
| `/subscribe/confirm` | the confirmation landing | C-UF-06 | User flow route table |
| `/subscribe/unsubscribe` | the unsubscribe landing | C-UF-07 | User flow route table |
| `/login` | the sign-in route | C-UF-08 | User flow route table |
| `/signup` | the registration route | C-UF-09 | User flow route table |
| `/studio` | the workspace dashboard | C-UF-10 | User flow route table |
| `/studio/stories` | the workspace story list | C-UF-11 | User flow route table |
| `/studio/stories/new` | the workspace create address | C-UF-12 | User flow route table |
| `/studio/media` | the workspace media library | C-UF-13 | User flow route table |
| `/studio/calendar` | the workspace ingestion surface | C-UF-14 | User flow route table |
| `/studio/enquiries` | the workspace enquiry inbox | C-UF-15 | User flow route table |
| `/studio/audience` | the workspace audience surface | C-UF-16 | User flow route table |
| `/studio/settings` | the workspace settings surface | C-UF-17 | User flow route table |
| `Sundown` | the next round circuit | C-UF-34 | User flow journey 1 |
| `04` | the next round designation | C-UF-35 | User flow journey 1 |
| `Halcyon` | the constructor | C-UF-36 | User flow journey 1 |
| `2019` | the debut year | C-UF-37 | User flow journey 1 |
| `2026` | the season year | C-UF-41 | User flow journey 2 |
| `Prime One` | the series name | C-UF-42 | User flow journey 2 |
| `Check your inbox to confirm.` | the pending subscribe message | C-UF-52 | User flow journey 3 |
| `What Sundown Asks For` | the scheduled seeded story title | C-UF-58 | User flow journey 4 |
| `2a9b7f31c8` | the draft seeded story public id | C-UF-63 | User flow journey 6 |
| `ENQ-00001` | the first enquiry reference | C-UF-69 | User flow journey 7 |
| `DATABASE_URL` | the database connection variable | C-TR-09 | Technical requirements |
| `STORAGE_ENDPOINT` | the object store endpoint variable | C-TR-10 | Technical requirements |
| `STORAGE_BUCKET` | the object bucket variable | C-TR-11 | Technical requirements |
| `STORAGE_ACCESS_KEY` | the object store key variable | C-TR-12 | Technical requirements |
| `STORAGE_SECRET_KEY` | the object store secret variable | C-TR-12 | Technical requirements |
| `access_token` | the login response field | C-TR-17 | Technical requirements |
| `Authorization: Bearer <access_token>` | the guarded request header | C-TR-18 | Technical requirements |
| `GET /api/health` | the health route | C-TR-24 | Technical requirements |
| `200` | the ready health status | C-TR-24 | Technical requirements |
| `minio` | the object store service name | C-OV-20 | Technical requirements |
| `/app/USER_README.md` | the credentials file | C-DM-05 | Data model intro |
| `story` | a content type | C-DM-38 | Data model, stories |
| `topic` | a content type | C-DM-38 | Data model, stories |
| `legal` | a content type | C-DM-38 | Data model, stories |
| `practice` | a session kind | C-DM-19 | Data model, sessions_slots |
| `qualifying` | a session kind | C-DM-19 | Data model, sessions_slots |
| `sprint` | a session kind | C-DM-19 | Data model, sessions_slots |
| `race` | a session kind | C-DM-19 | Data model, sessions_slots |
| `in_progress` | an in-flight round state | C-DM-12 | Data model, rounds |
| `postponed` | a deferred round state | C-DM-12 | Data model, rounds |
| `classified` | a classification status | C-DM-25 | Data model, classifications |
| `retired` | a classification status | C-DM-25 | Data model, classifications |
| `disqualified` | a classification status | C-DM-25 | Data model, classifications |
| `did_not_start` | a classification status | C-DM-25 | Data model, classifications |
| `did_not_qualify` | a classification status | C-DM-25 | Data model, classifications |
| `provider` | an ingested classification source | C-DM-28 | Data model, classifications |
| `manual` | an overridden classification source | C-DM-28 | Data model, classifications |
| `failed` | a derivative state | C-DM-58 | Data model, assets |
| `unsubscribed` | a subscriber status | C-DM-61 | Data model, subscribers |
| `partnership` | an enquiry type | C-DM-68 | Data model, enquiries |
| `media` | an enquiry type | C-DM-68 | Data model, enquiries |
| `appearance` | an enquiry type | C-DM-68 | Data model, enquiries |
| `other` | an enquiry type | C-DM-68 | Data model, enquiries |
| `ENQ-` | the enquiry reference prefix | C-DM-70 | Data model, enquiries |
| `9f3c1a7d42` | a published seeded story public id | C-DM-92 | Data model, seed data |
| `4b82e05c17` | a published seeded story public id | C-DM-93 | Data model, seed data |
| `d15a6f9b30` | a published seeded story public id | C-DM-94 | Data model, seed data |
| `7e0d4c82a6` | the scheduled seeded story public id | C-DM-95 | Data model, seed data |
| `b63e18a70f` | the in-review seeded story public id | C-DM-97 | Data model, seed data |
| `assets/{asset_id}/{sha256_of_bytes}.{ext}` | the photograph key scheme | C-DM-99 | Data model, seed data |
| `Milo` | the profile nickname | C-DM-106 | Data model, seed data |
| `MR` | the profile monogram | C-DM-107 | Data model, seed data |
| `Bracken Hill` | the profile home town | C-DM-111 | Data model, seed data |
| `Ardenia` | the profile home country | C-DM-112 | Data model, seed data |
| `title` | a partner category | C-DM-117 | Data model, seed data |
| `technical` | a partner category | C-DM-117 | Data model, seed data |
| `official` | a partner category | C-DM-117 | Data model, seed data |
| `01` | the first seeded round designation | C-DM-83 | Data model, seed data |
| `02` | the second seeded round designation | C-DM-84 | Data model, seed data |
| `03` | the third seeded round designation | C-DM-85 | Data model, seed data |
| `05` | the fifth seeded round designation | C-DM-87 | Data model, seed data |
| `06` | the sixth seeded round designation | C-DM-88 | Data model, seed data |
| `Padel tennis` | a seeded person topic | C-FE-130 | Front-end specification, off track |
| `Music` | a seeded person topic | C-FE-131 | Front-end specification, off track |
| `main` | the per-route landmark | C-FE-239 | Front-end specification, accessibility |
| `contentinfo` | the footer landmark | C-FE-241 | Front-end specification, accessibility |
| `Milo Rennick` | the chrome wordmark | C-FE-296 | Front-end specification, copy deck |
| `Store` | the store button label | C-FE-298 | Front-end specification, copy deck |
| `Home` | a menu destination label | C-FE-299 | Front-end specification, copy deck |
| `On Track` | a menu destination label | C-FE-299 | Front-end specification, copy deck |
| `Off Track` | a menu destination label | C-FE-299 | Front-end specification, copy deck |
| `Calendar` | a menu destination label | C-FE-299 | Front-end specification, copy deck |
| `Business enquiries` | the menu enquiry label | C-FE-300 | Front-end specification, copy deck |
| `Next race` | the next-race eyebrow | C-FE-301 | Front-end specification, copy deck |
| `Latest` | the teaser strip label | C-FE-302 | Front-end specification, copy deck |
| `Nickname` | a record statistic label | C-FE-303 | Front-end specification, copy deck |
| `Age` | a record statistic label | C-FE-303 | Front-end specification, copy deck |
| `The record` | the career heading | C-FE-304 | Front-end specification, copy deck |
| `Round` | a results table column | C-FE-305 | Front-end specification, copy deck |
| `Date` | a results table column | C-FE-305 | Front-end specification, copy deck |
| `Position` | a results table column | C-FE-305 | Front-end specification, copy deck |
| `Time` | a results table column | C-FE-305 | Front-end specification, copy deck |
| `Standing` | a season header label | C-FE-306 | Front-end specification, copy deck |
| `When` | a featured panel label | C-FE-307 | Front-end specification, copy deck |
| `Circuit length` | a featured panel label | C-FE-307 | Front-end specification, copy deck |
| `Race distance` | a featured panel label | C-FE-307 | Front-end specification, copy deck |
| `Laps` | a featured panel label | C-FE-307 | Front-end specification, copy deck |
| `First competed` | a featured panel label | C-FE-307 | Front-end specification, copy deck |
| `Visualiser` | a calendar mode control | C-FE-308 | Front-end specification, copy deck |
| `List` | a calendar mode control | C-FE-308 | Front-end specification, copy deck |
| `Email address` | the subscribe field label | C-FE-309 | Front-end specification, copy deck |
| `Name` | an enquiry field label | C-FE-310 | Front-end specification, copy deck |
| `Organisation` | an enquiry field label | C-FE-310 | Front-end specification, copy deck |
| `Enquiry type` | an enquiry field label | C-FE-310 | Front-end specification, copy deck |
| `Message` | an enquiry field label | C-FE-310 | Front-end specification, copy deck |
| `Page not found` | the not-found heading | C-FE-311 | Front-end specification, copy deck |
| `APP_PUBLIC_URL` | the public app URL variable | C-DC-01 | Deployment contract bullet 1 |
| `${APP_PUBLIC_PORT}:4173` | the port mapping | C-DC-02 | Deployment contract bullet 1 |
| `4173` | the container-internal port | C-DC-03 | Deployment contract bullet 1 |
| `/api` | the API prefix | C-DC-05 | Deployment contract bullet 2 |
| `.browser_screenshots/` | a reserved directory | C-DC-09 | Deployment contract bullet 6 |
| `.downloads/` | a reserved directory | C-DC-10 | Deployment contract bullet 6 |
| `0.0.0.0` | the bind address | C-DC-16 | Deployment contract bullet 9 |
| `POST /api/auth/signup` | the signup endpoint | C-DC-24 | Deployment contract, API shapes |
| `POST /api/auth/login` | the login endpoint | C-DC-25 | Deployment contract, API shapes |
| `GET /api/stories` | the public story list endpoint | C-DC-27 | Deployment contract, API shapes |
| `GET /api/stories/count` | the public story count endpoint | C-DC-28 | Deployment contract, API shapes |
| `GET /api/stories/{}` | the public story detail endpoint | C-DC-29 | Deployment contract, API shapes |
| `GET /api/assets/{}/file` | the photograph bytes endpoint | C-DC-30 | Deployment contract, API shapes |
| `GET /api/season` | the season endpoint | C-DC-31 | Deployment contract, API shapes |
| `GET /api/season/next-round` | the next-round endpoint | C-DC-32 | Deployment contract, API shapes |
| `GET /api/results` | the results endpoint | C-DC-33 | Deployment contract, API shapes |
| `GET /api/standings` | the standings endpoint | C-DC-34 | Deployment contract, API shapes |
| `GET /api/profile` | the profile endpoint | C-DC-35 | Deployment contract, API shapes |
| `GET /api/merch` | the merchandise endpoint | C-DC-36 | Deployment contract, API shapes |
| `GET /api/partners` | the partner endpoint | C-DC-37 | Deployment contract, API shapes |
| `POST /api/subscribers` | the subscribe endpoint | C-DC-38 | Deployment contract, API shapes |
| `POST /api/subscribers/confirm` | the confirmation endpoint | C-DC-39 | Deployment contract, API shapes |
| `POST /api/subscribers/unsubscribe` | the unsubscribe endpoint | C-DC-40 | Deployment contract, API shapes |
| `POST /api/enquiries` | the enquiry endpoint | C-DC-41 | Deployment contract, API shapes |
| `GET /api/studio/stories` | the workspace story list endpoint | C-DC-42 | Deployment contract, API shapes |
| `POST /api/studio/stories` | the story create endpoint | C-DC-43 | Deployment contract, API shapes |
| `POST /api/studio/stories/{}/assets` | the photograph upload endpoint | C-DC-44 | Deployment contract, API shapes |
| `file` | the upload multipart field | C-DC-45 | Deployment contract, API shapes |
| `PATCH /api/studio/assets/{}` | the asset patch endpoint | C-DC-46 | Deployment contract, API shapes |
| `POST /api/studio/stories/{}/submit` | the submit endpoint | C-DC-47 | Deployment contract, API shapes |
| `POST /api/studio/stories/{}/publish` | the publish endpoint | C-DC-48 | Deployment contract, API shapes |
| `POST /api/studio/stories/{}/unpublish` | the unpublish endpoint | C-DC-49 | Deployment contract, API shapes |
| `POST /api/studio/ingest` | the ingestion endpoint | C-DC-50 | Deployment contract, API shapes |
| `GET /api/studio/ingest/runs` | the ingestion run list endpoint | C-DC-51 | Deployment contract, API shapes |
| `POST /api/studio/overrides` | the override endpoint | C-DC-52 | Deployment contract, API shapes |
| `GET /api/studio/enquiries` | the enquiry inbox endpoint | C-DC-53 | Deployment contract, API shapes |
| `GET /api/studio/subscribers` | the subscriber list endpoint | C-DC-54 | Deployment contract, API shapes |
| `GET /api/studio/editors` | the editor list endpoint | C-DC-55 | Deployment contract, API shapes |
| `5xx` | the server-error class a rejection never uses | C-DC-66 | Deployment contract, API shapes |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the grotesque family behind every structural role | C-UX-04 | named by character with no family pinned, so two builds may choose differently |
| the display serif behind the pull-quotes | C-UX-06 | named by character with no family pinned, so two builds may choose differently |
| the exact shades behind the palette roles | C-UX-20 | the brief hands the shade to the builder, pinning only the exclusivity rules |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 21 |
| User roles | 2 | 54 |
| Core features | 15 | 181 |
| User flow | 5 | 78 |
| UI and UX notes | 3 | 53 |
| Technical requirements | 8 | 85 |
| Data model | 3 | 118 |
| Front-end specification | 29 | 319 |
| Constraints | 2 | 25 |
| Deployment contract | 10 | 73 |
