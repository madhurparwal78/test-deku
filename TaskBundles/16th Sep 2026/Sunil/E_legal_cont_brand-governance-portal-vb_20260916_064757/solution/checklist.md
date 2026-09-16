# Checklist: Tessera Brand Guidelines

Items: 300
Unpinned values flagged: 7
Sections present: C-OV, C-RL, C-CF, C-UF, C-UX, C-TR, C-DM, C-FE, C-CN, C-DC

## C-OV Overview

- [ ] `C-OV-01` `capability` The public reading surface answers without an account `src: Overview`
- [ ] `C-OV-02` `capability` The governed surface answers only a signed in principal `src: Overview`
- [ ] `C-OV-03` `capability` A published chapter statement carries a stable identifier a usage request cites `src: Overview`
- [ ] `C-OV-04` `capability` Availability is computed for one principal against one asset at the moment of asking `src: Overview`
- [ ] `C-OV-05` `constraint` No path reaches a released binary without a recorded policy decision `src: Overview`
- [ ] `C-OV-06` `constraint` An audit record cannot be altered by any principal `src: Overview`

## C-RL User roles

- [ ] `C-RL-01` `role` A visitor reads all nine public routes without an account `src: User roles`
- [ ] `C-RL-02` `role` A visitor cannot open the asset library `src: User roles`
- [ ] `C-RL-03` `role` A visitor cannot download an asset binary `src: User roles`
- [ ] `C-RL-04` `role` An employee downloads an asset badged `Available` `src: User roles`
- [ ] `C-RL-05` `role` An employee cannot open the approval queue `src: User roles`
- [ ] `C-RL-06` `role` An employee cannot read a request belonging to another principal `src: User roles`
- [ ] `C-RL-07` `role` An employee cannot read the audit record `src: User roles`
- [ ] `C-RL-08` `role` A partner downloads only inside the asset classes their own engagement grants `src: User roles`
- [ ] `C-RL-09` `role` A partner is refused a download once the engagement end date has passed `src: User roles`
- [ ] `C-RL-10` `role` A reviewer opens the approval queue `src: User roles`
- [ ] `C-RL-11` `role` A reviewer cannot decide a stage of a request the same reviewer raised `src: User roles`
- [ ] `C-RL-12` `role` A reviewer cannot remove an audit record `src: User roles`
- [ ] `C-RL-13` `role` No principal can create an account through the app `src: User roles`
- [ ] `C-RL-14` `role` A direct call from an employee session to a reviewer only endpoint leaves the protected state unchanged `src: User roles`
- [ ] `C-RL-15` `role` A reviewer decides a stage assigned to that same reviewer `src: User roles`

## C-CF Core features

- [ ] `C-CF-01` `capability` Signing in with a seeded email address returns a bearer token `src: Core features > Sign in`
- [ ] `C-CF-02` `constraint` Signing in with an unknown email address returns no token `src: Core features > Sign in`
- [ ] `C-CF-03` `constraint` Signing in with a wrong password returns no token `src: Core features > Sign in`
- [ ] `C-CF-04` `constraint` The app exposes no route that creates a principal `src: Core features > Sign in`
- [ ] `C-CF-05` `capability` The hub answers at `/` without an account `src: Core features > The routes`
- [ ] `C-CF-06` `capability` Each of the eight chapter routes answers without an account `src: Core features > The routes`
- [ ] `C-CF-07` `literal` The reserved address `/2/` answers the not-found page at `404` `src: Core features > The not found route`
- [ ] `C-CF-08` `literal` The reserved address `/as` answers the not-found page at `404` `src: Core features > The not found route`
- [ ] `C-CF-09` `literal` The reserved address `/gs` answers the not-found page at `404` `src: Core features > The not found route`
- [ ] `C-CF-10` `capability` An address that is not a route answers the not-found page at `404` `src: Core features > The not found route`
- [ ] `C-CF-11` `ui` The not-found page carries the chapter menu as the way back `src: Core features > The not found route`
- [ ] `C-CF-12` `constraint` A retired chapter address answers not found rather than redirecting to the hub `src: Core features > The not found route`
- [ ] `C-CF-13` `constraint` A chapter created under a reserved slug is refused `src: Core features > The not found route`
- [ ] `C-CF-14` `ui` The hub renders eight tiles, one per chapter `src: Core features > The hub`
- [ ] `C-CF-15` `ui` The eight hub tiles reach their final geometry at full scroll of the hub `src: Core features > The hub`
- [ ] `C-CF-16` `data` The eight chapters render in the display order held on the chapter record `src: Core features > The hub`
- [ ] `C-CF-17` `ui` Each hub tile carries its own ground colour from the chapter palette `src: Core features > The hub`
- [ ] `C-CF-18` `ui` Each hub tile links to its own chapter route `src: Core features > The hub`
- [ ] `C-CF-19` `ui` A chapter carries a vertical rail showing the chapter title `src: Core features > The eight chapters`
- [ ] `C-CF-20` `ui` The vertical rail fills as a chapter is scrolled `src: Core features > The eight chapters`
- [ ] `C-CF-21` `constraint` A chapter carries no breadcrumb `src: Core features > The eight chapters`
- [ ] `C-CF-22` `constraint` A chapter carries no next chapter link `src: Core features > The eight chapters`
- [ ] `C-CF-23` `ui` Lateral movement between chapters goes through the menu overlay `src: Core features > The eight chapters`
- [ ] `C-CF-24` `ui` The menu overlay lists the same eight chapters in the same fixed order `src: Core features > The eight chapters`
- [ ] `C-CF-25` `literal` The framework chapter publishes the principle `Prioritize Simplicity` `src: Core features > The eight chapters`
- [ ] `C-CF-26` `literal` The framework chapter publishes the principle `Deepen Understanding` `src: Core features > The eight chapters`
- [ ] `C-CF-27` `literal` The framework chapter publishes the principle `Instant Feedback` `src: Core features > The eight chapters`
- [ ] `C-CF-28` `literal` The framework chapter publishes the principle `Subtle Playfulness` `src: Core features > The eight chapters`
- [ ] `C-CF-29` `ui` The voice chapter shows one message written for three named delivery surfaces `src: Core features > The eight chapters`
- [ ] `C-CF-30` `literal` The logo chapter labels the mark expression `Version A` `src: Core features > The eight chapters`
- [ ] `C-CF-31` `literal` The logo chapter labels the mark expression `Version B` `src: Core features > The eight chapters`
- [ ] `C-CF-32` `ui` The typography chapter runs a live ruler driving the variable axis of the display face `src: Core features > The eight chapters`
- [ ] `C-CF-33` `ui` The iconography chapter runs three counter scrolling marquees `src: Core features > The eight chapters`
- [ ] `C-CF-34` `ui` The colour chapter runs a rotating palette wheel `src: Core features > The eight chapters`
- [ ] `C-CF-35` `ui` The motion chapter runs a timeline editor carrying keyframe markers `src: Core features > The eight chapters`
- [ ] `C-CF-36` `constraint` No explanatory figure in a chapter is a flat image `src: Core features > The eight chapters`
- [ ] `C-CF-37` `data` A published statement carries an identifier shaped `<chapter-slug>.<section>.<n>` `src: Core features > The eight chapters`
- [ ] `C-CF-38` `literal` A logo chapter statement identifier reads `logo.expressions.2` `src: Core features > The eight chapters`
- [ ] `C-CF-39` `data` A released icon whose declared dimensions mismatch the class is refused `src: Core features > The eight chapters`
- [ ] `C-CF-40` `literal` The outro carries the destination `Brand Partner Toolkit` `src: Core features > The outro and the footer`
- [ ] `C-CF-41` `literal` The outro carries the destination `Legal Branding Resources` `src: Core features > The outro and the footer`
- [ ] `C-CF-42` `literal` The outro carries the destination `Tessera Design` `src: Core features > The outro and the footer`
- [ ] `C-CF-43` `ui` Every public route ends with the same outro `src: Core features > The outro and the footer`
- [ ] `C-CF-44` `literal` The footer carries the destination `Modern Slavery Statement` `src: Core features > The outro and the footer`
- [ ] `C-CF-45` `literal` The footer carries the destination `Impressum` `src: Core features > The outro and the footer`
- [ ] `C-CF-46` `literal` The footer carries the destination `Cancel Contract` `src: Core features > The outro and the footer`
- [ ] `C-CF-47` `literal` The footer carries the destination `Cookies & CCPA preferences` `src: Core features > The outro and the footer`
- [ ] `C-CF-48` `capability` Every internal link on every public route resolves `src: Core features > The outro and the footer`
- [ ] `C-CF-49` `ui` A first time visitor is asked once about non essential cookie use `src: Core features > The cookie choice`
- [ ] `C-CF-50` `literal` The consent frame carries the control `Do not sell or share my personal data to third parties` `src: Core features > The cookie choice`
- [ ] `C-CF-51` `data` A recorded consent answer survives a reload `src: Core features > The cookie choice`
- [ ] `C-CF-52` `constraint` A visitor who has answered the cookie choice is not asked a second time `src: Core features > The cookie choice`
- [ ] `C-CF-53` `ui` The footer preferences link reopens the cookie choice `src: Core features > The cookie choice`
- [ ] `C-CF-54` `capability` The library at `/library` lists every asset to a signed in principal `src: Core features > The asset library`
- [ ] `C-CF-55` `constraint` The library is never empty for a principal holding no permission `src: Core features > The asset library`
- [ ] `C-CF-56` `data` Every asset card carries exactly one availability badge `src: Core features > The asset library`
- [ ] `C-CF-57` `literal` An availability badge reads `Available` when the caller may download now `src: Core features > The asset library`
- [ ] `C-CF-58` `literal` An availability badge reads `Request required` when the caller must ask `src: Core features > The asset library`
- [ ] `C-CF-59` `literal` An availability badge reads `Restricted` when a grant is needed `src: Core features > The asset library`
- [ ] `C-CF-60` `literal` An availability badge reads `Retired` when the asset is withdrawn `src: Core features > The asset library`
- [ ] `C-CF-61` `constraint` An availability answer computed for one principal is never served to another `src: Core features > The asset library`
- [ ] `C-CF-62` `ui` A filter excluding every result names the filter responsible `src: Core features > The asset library`
- [ ] `C-CF-63` `ui` The filter rail offers a chapter filter `src: Core features > The asset library`
- [ ] `C-CF-64` `ui` The filter rail offers an asset class filter `src: Core features > The asset library`
- [ ] `C-CF-65` `data` An asset carries one class from the seven named classes `src: Core features > The asset library`
- [ ] `C-CF-66` `capability` Asset detail at `/asset/<asset-id>` shows the licence record `src: Core features > Asset detail`
- [ ] `C-CF-67` `ui` Asset detail shows the preview from the asset derivative `src: Core features > Asset detail`
- [ ] `C-CF-68` `constraint` Asset detail never shows the asset master as its preview `src: Core features > Asset detail`
- [ ] `C-CF-69` `ui` Asset detail links the governing statement identifier `src: Core features > Asset detail`
- [ ] `C-CF-70` `ui` A disabled action control states the reason for being disabled `src: Core features > Asset detail`
- [ ] `C-CF-71` `constraint` A download of a `Restricted` asset without a covering grant is refused `src: Core features > Asset detail`
- [ ] `C-CF-72` `ui` A refused download names what is missing `src: Core features > Asset detail`
- [ ] `C-CF-73` `constraint` A `Retired` asset is never downloadable `src: Core features > Asset detail`
- [ ] `C-CF-74` `ui` A retired asset detail names the successor asset `src: Core features > Asset detail`
- [ ] `C-CF-75` `capability` A signed in principal raises a usage request against an asset `src: Core features > The usage request desk`
- [ ] `C-CF-76` `capability` The request desk at `/requests` lists the caller's own requests only `src: Core features > The usage request desk`
- [ ] `C-CF-77` `data` A submitted request records the chapter version current at submission `src: Core features > The usage request desk`
- [ ] `C-CF-78` `data` A submitted request records the statement identifiers the requester cited `src: Core features > The usage request desk`
- [ ] `C-CF-79` `data` A submitted request records the policy version that evaluates the request `src: Core features > The usage request desk`
- [ ] `C-CF-80` `data` A request carries one state from the nine named states `src: Core features > The usage request desk`
- [ ] `C-CF-81` `data` A request in any state names exactly one holder `src: Core features > The usage request desk`
- [ ] `C-CF-82` `data` A request carries one application class from the six named classes `src: Core features > The usage request desk`
- [ ] `C-CF-83` `capability` A requester withdraws their own request before a decision `src: Core features > The usage request desk`
- [ ] `C-CF-84` `data` A resubmitted request returns to `routed` for a fresh policy evaluation `src: Core features > The usage request desk`
- [ ] `C-CF-85` `data` An application class of `co_brand` adds a legal stage `src: Core features > Routing and the approval queue`
- [ ] `C-CF-86` `data` An application class of `merchandise` adds a legal stage `src: Core features > Routing and the approval queue`
- [ ] `C-CF-87` `data` An application class of `partnership` adds a legal stage `src: Core features > Routing and the approval queue`
- [ ] `C-CF-88` `data` An asset class of `mark` adds a second stage held by a distinct reviewer `src: Core features > Routing and the approval queue`
- [ ] `C-CF-89` `constraint` A requester who is a reviewer is never assigned their own request `src: Core features > Routing and the approval queue`
- [ ] `C-CF-90` `capability` The queue at `/queue` lists the stages awaiting the calling reviewer `src: Core features > Routing and the approval queue`
- [ ] `C-CF-91` `data` The queue orders stages by the deadline stored on the request `src: Core features > Routing and the approval queue`
- [ ] `C-CF-92` `ui` The decision panel explains why a request reached the holding reviewer `src: Core features > Routing and the approval queue`
- [ ] `C-CF-93` `ui` The decision panel shows the cap that will apply to the grant `src: Core features > Routing and the approval queue`
- [ ] `C-CF-94` `data` A deadline is stored on a request at submission `src: Core features > Routing and the approval queue`
- [ ] `C-CF-95` `constraint` A later policy change does not move a deadline already stored `src: Core features > Routing and the approval queue`
- [ ] `C-CF-96` `data` A condition carries one kind from the six named kinds `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-97` `capability` A reviewer attaches a condition to an approval `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-98` `data` A `proof_required` condition creates the grant with a future start date `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-99` `data` Accepting a proof activates the grant waiting on the proof `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-100` `constraint` A proof whose scan state is `pending` is never rendered `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-101` `data` A proof carries one scan state from `pending`, `clean`, `quarantined` `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-102` `data` The last approval mints exactly one grant `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-103` `data` A grant end date is the earliest of the four candidate dates `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-104` `data` A grant carries the identifier of the request that justified the grant `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-105` `constraint` A retried approval yields the grant that already exists `src: Core features > Conditions, proofs and grants`
- [ ] `C-CF-106` `constraint` Two reviewers approving one stage at once produce exactly one recorded decision `src: Core features > Decisions are made once`
- [ ] `C-CF-107` `constraint` The losing decision on a contested stage is refused as a conflict `src: Core features > Decisions are made once`
- [ ] `C-CF-108` `ui` The refused decision reports the outcome that won `src: Core features > Decisions are made once`
- [ ] `C-CF-109` `constraint` A contested stage decision is refused as a client error `src: Core features > Decisions are made once`
- [ ] `C-CF-110` `data` An approved request writes exactly one audit record per transition `src: Core features > Decisions are made once`
- [ ] `C-CF-111` `constraint` A withdrawal during a decision wins over the decision `src: Core features > Decisions are made once`
- [ ] `C-CF-112` `data` Retiring an asset under review rejects the open request automatically `src: Core features > Decisions are made once`
- [ ] `C-CF-113` `ui` The automatic rejection names the successor asset identifier `src: Core features > Decisions are made once`
- [ ] `C-CF-114` `constraint` One request submitted twice in quick succession produces one submission `src: Core features > Decisions are made once`
- [ ] `C-CF-115` `capability` The audit surface at `/admin/audit` answers a query over the record `src: Core features > The audit record`
- [ ] `C-CF-116` `data` An audit record names the acting principal `src: Core features > The audit record`
- [ ] `C-CF-117` `data` An audit record names the principal type `src: Core features > The audit record`
- [ ] `C-CF-118` `data` An audit record names the address the action came from `src: Core features > The audit record`
- [ ] `C-CF-119` `data` An audit record names the request identifier `src: Core features > The audit record`
- [ ] `C-CF-120` `data` An audit record carries the state before the transition `src: Core features > The audit record`
- [ ] `C-CF-121` `data` An audit record carries the state after the transition `src: Core features > The audit record`
- [ ] `C-CF-122` `constraint` An attempt to remove an audit record is refused `src: Core features > The audit record`
- [ ] `C-CF-123` `constraint` A form submission filling the decoy field is refused `src: Core features > Forms refuse a robot`
- [ ] `C-CF-124` `constraint` The same form submitted repeatedly in quick succession is refused `src: Core features > Forms refuse a robot`
- [ ] `C-CF-125` `constraint` A refused form submission writes nothing `src: Core features > Forms refuse a robot`
- [ ] `C-CF-126` `ui` A form rejecting invalid input names the field at fault `src: Core features > Forms refuse a robot`
- [ ] `C-CF-127` `ui` The chapter outro shows the partner destination beside the legal destination as two distinct links `src: Core features > The outro and the footer`

## C-UF User flow

- [ ] `C-UF-01` `capability` A visitor opens the hub at `/` as the first entry point `src: User flow`
- [ ] `C-UF-02` `capability` A visitor reaches `/typography` through the menu overlay `src: User flow`
- [ ] `C-UF-03` `capability` A visitor following an outro link without a session is asked to sign in `src: User flow`
- [ ] `C-UF-04` `capability` An employee signs in as `employee@example.com` `src: User flow`
- [ ] `C-UF-05` `capability` An employee downloads a released asset from asset detail `src: User flow`
- [ ] `C-UF-06` `data` A released download is recorded against the principal `src: User flow`
- [ ] `C-UF-07` `capability` A partner signs in as `partner@example.com` `src: User flow`
- [ ] `C-UF-08` `constraint` The partner mark download control is disabled with the reason stated `src: User flow`
- [ ] `C-UF-09` `ui` The request desk warns a requester whose campaign end falls after the engagement end `src: User flow`
- [ ] `C-UF-10` `capability` A reviewer signs in as `reviewer@example.com` `src: User flow`
- [ ] `C-UF-11` `capability` A second reviewer signs in as `reviewer2@example.com` `src: User flow`
- [ ] `C-UF-12` `data` The minted grant ends on the engagement end date rather than the campaign end date `src: User flow`
- [ ] `C-UF-13` `capability` The partner downloads the mark once the grant exists `src: User flow`
- [ ] `C-UF-14` `constraint` A reviewer calling the decision endpoint for their own request leaves the request unchanged `src: User flow`
- [ ] `C-UF-15` `capability` A reviewer queries the audit record by request identifier `src: User flow`
- [ ] `C-UF-16` `capability` Any caller opening `/gs` lands on the not-found page `src: User flow`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The product carries exactly one drop shadow, belonging to the consent frame `src: UI/UX notes`
- [ ] `C-UX-02` `ui` The product carries no photography in the chrome `src: UI/UX notes`
- [ ] `C-UX-03` `ui` Construction hairlines are drawn as real elements rather than as background decoration `src: UI/UX notes`
- [ ] `C-UX-04` `ui` Body text meets the contrast bar against its ground in every identity pairing `src: UI/UX notes`
- [ ] `C-UX-05` `ui` Every control is operable by keyboard alone in a visible order `src: UI/UX notes`
- [ ] `C-UX-06` `ui` The focus ring is always drawn `src: UI/UX notes`
- [ ] `C-UX-07` `ui` Every icon only control carries a text label for assistive technology `src: UI/UX notes`
- [ ] `C-UX-08` `ui` Every content image carries alternative text `src: UI/UX notes`
- [ ] `C-UX-09` `ui` A decorative image declares being decorative `src: UI/UX notes`
- [ ] `C-UX-10` `ui` An availability badge states a word rather than relying on colour alone `src: UI/UX notes`
- [ ] `C-UX-11` `ui` A reduced motion preference settles every scrubbed element to a final state `src: UI/UX notes`
- [ ] `C-UX-12` `ui` At a narrow viewport nothing overflows sideways `src: UI/UX notes`
- [ ] `C-UX-13` `ui` At a narrow viewport every navigation target stays reachable `src: UI/UX notes`
- [ ] `C-UX-14` `ui` The audit result table scrolls inside its own container rather than widening the page `src: UI/UX notes`
- [ ] `C-UX-15` `ui` The reader drives the scroll with no scripted interception `src: UI/UX notes`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The app reaches PostgreSQL at `DATABASE_URL` `src: Technical requirements`
- [ ] `C-TR-02` `contract` The app reaches MinIO at `STORAGE_ENDPOINT` `src: Technical requirements`
- [ ] `C-TR-03` `contract` The app uses the bucket named in `STORAGE_BUCKET` `src: Technical requirements`
- [ ] `C-TR-04` `constraint` An anonymous request for a protected object address is refused `src: Technical requirements`
- [ ] `C-TR-05` `contract` Every response carries a strict transport security header `src: Technical requirements`
- [ ] `C-TR-06` `contract` Every response carries a nosniff content type header `src: Technical requirements`
- [ ] `C-TR-07` `contract` Every response carries a frame ancestry header `src: Technical requirements`
- [ ] `C-TR-08` `contract` Every response carries a referrer policy header `src: Technical requirements`
- [ ] `C-TR-09` `capability` A successful sign in returns a bearer token authorising later calls `src: Technical requirements`
- [ ] `C-TR-10` `constraint` Authorization is decided against the session rather than a client supplied value `src: Technical requirements`
- [ ] `C-TR-11` `constraint` A stage accepts exactly one decision `src: Technical requirements`
- [ ] `C-TR-12` `constraint` Grant minting is idempotent against the request identifier `src: Technical requirements`
- [ ] `C-TR-13` `constraint` The audit record exposes no update path `src: Technical requirements`
- [ ] `C-TR-14` `constraint` A proof upload beyond the size cap is refused `src: Technical requirements`
- [ ] `C-TR-15` `constraint` A proof type is decided by inspecting content rather than by the arriving name `src: Technical requirements`
- [ ] `C-TR-16` `contract` The HTTP API answers JSON `src: Technical requirements`
- [ ] `C-TR-17` `constraint` An unauthorized call answers a client error rather than a server error `src: Technical requirements`
- [ ] `C-TR-18` `data` Times are stored in UTC `src: Technical requirements`
- [ ] `C-TR-19` `capability` All nine public routes render when the governed surface cannot answer `src: Technical requirements`
- [ ] `C-TR-20` `constraint` A collection endpoint answers a top-level JSON array `src: Technical requirements > API conventions`
- [ ] `C-TR-21` `constraint` A rejected body names the field at fault `src: Technical requirements > API conventions`
- [ ] `C-TR-22` `constraint` A campaign start after the campaign end is rejected `src: Technical requirements > API conventions`
- [ ] `C-TR-23` `constraint` A cited statement identifier absent from the chapter version is rejected `src: Technical requirements > API conventions`
- [ ] `C-TR-24` `constraint` A caller over the rate limit is refused with nothing written `src: Technical requirements > API conventions`
- [ ] `C-TR-25` `constraint` A retried request submission yields the outcome that already exists `src: Technical requirements > Concurrency`
- [ ] `C-TR-26` `constraint` No deadline depends on a client supplied time `src: Technical requirements > Concurrency`
- [ ] `C-TR-27` `data` Grant expiry is decided when a download is asked for `src: Technical requirements > Concurrency`
- [ ] `C-TR-28` `data` A principal belongs to zero or more groups carrying an entitlement `src: Technical requirements > Directory`
- [ ] `C-TR-29` `data` A partner principal carries an engagement end date attribute `src: Technical requirements > Directory`
- [ ] `C-TR-30` `constraint` A proof file is purged after the retention period `src: Technical requirements > Data governance`
- [ ] `C-TR-31` `data` A purged proof retains the checksum `src: Technical requirements > Data governance`
- [ ] `C-TR-32` `data` A purged proof retains the scan state `src: Technical requirements > Data governance`
- [ ] `C-TR-33` `capability` A bulk download decides each asset separately `src: Technical requirements > Performance`
- [ ] `C-TR-34` `capability` The library renders from the database when the object store is unreachable `src: Technical requirements > Performance`
- [ ] `C-TR-35` `data` A refusal is recorded as an event a reviewer queries `src: Technical requirements > Observability`
- [ ] `C-TR-36` `capability` The health endpoint reports the database separately from the object store `src: Technical requirements > Observability`
- [ ] `C-TR-37` `data` A request breaching the deadline records the breach `src: Technical requirements > Observability`
- [ ] `C-TR-38` `constraint` No secret appears in any response `src: Technical requirements > Security posture`
- [ ] `C-TR-39` `constraint` A stored upload takes a name the app generates `src: Technical requirements > Security posture`
- [ ] `C-TR-40` `constraint` No user supplied string is interpreted as code `src: Technical requirements > Anti-abuse`
- [ ] `C-TR-41` `constraint` Deciding a stage requires the principal to re-enter the password `src: Technical requirements > Step-up`
- [ ] `C-TR-42` `constraint` No override path writes without a record `src: Technical requirements > Step-up`
- [ ] `C-TR-43` `constraint` A partner asking for the whole request collection receives their own requests only `src: Technical requirements > Row level enforcement`
- [ ] `C-TR-44` `constraint` A search answer is narrowed to the calling principal `src: Technical requirements > Search`
- [ ] `C-TR-45` `constraint` An audit record is never reachable through search `src: Technical requirements > Search`
- [ ] `C-TR-46` `constraint` A principal matching no entitlement is refused `src: Technical requirements > Decision rules`
- [ ] `C-TR-47` `constraint` An explicit deny overrides a broader group allow `src: Technical requirements > Decision rules`
- [ ] `C-TR-48` `constraint` A change that cannot be recorded is refused `src: Technical requirements > Decision rules`
- [ ] `C-TR-49` `constraint` A licence change leaves an existing grant on the original terms `src: Technical requirements > Decision rules`
- [ ] `C-TR-50` `constraint` A draft chapter version is unreachable on the public surface `src: Technical requirements > Decision rules`
- [ ] `C-TR-51` `constraint` A failed sign in answers the same shape whether or not the address exists `src: Technical requirements > Decision rules`

## C-DM Data model

- [ ] `C-DM-01` `data` Every seeded account carries the password `deku-demo-pw-2026` `src: Data model > Seed data`
- [ ] `C-DM-02` `data` The account `employee@example.com` is seeded with role `employee` `src: Data model > Seed data`
- [ ] `C-DM-03` `data` The account `partner@example.com` is seeded with role `partner` `src: Data model > Seed data`
- [ ] `C-DM-04` `data` The account `partner2@example.com` is seeded with role `partner` `src: Data model > Seed data`
- [ ] `C-DM-05` `data` The account `reviewer@example.com` is seeded with role `reviewer` `src: Data model > Seed data`
- [ ] `C-DM-06` `data` The account `reviewer2@example.com` is seeded with role `reviewer` `src: Data model > Seed data`
- [ ] `C-DM-07` `data` The partner engagement for `partner@example.com` ends `2026-11-30` `src: Data model > Seed data`
- [ ] `C-DM-08` `data` The partner engagement for `partner2@example.com` ends `2027-03-31` `src: Data model > Seed data`
- [ ] `C-DM-09` `data` The engagement for `partner@example.com` grants `spot_icon` `src: Data model > Seed data`
- [ ] `C-DM-10` `data` The engagement for `partner@example.com` grants `pictogram` `src: Data model > Seed data`
- [ ] `C-DM-11` `data` A principal email address is unique `src: Data model`
- [ ] `C-DM-12` `data` A chapter slug is unique `src: Data model`
- [ ] `C-DM-13` `data` The eight chapters are seeded in the fixed display order `src: Data model > Seed data`
- [ ] `C-DM-14` `data` At least one asset exists for every asset class `src: Data model > Seed data`
- [ ] `C-DM-15` `data` The mark is seeded in both expressions as class `mark` `src: Data model > Seed data`
- [ ] `C-DM-16` `data` The seeded mark assets are governed by the `logo` chapter `src: Data model > Seed data`
- [ ] `C-DM-17` `data` One seeded asset carries availability `Retired` `src: Data model > Seed data`
- [ ] `C-DM-18` `data` The seeded retired asset names a successor `src: Data model > Seed data`
- [ ] `C-DM-19` `data` Every seeded asset carries a licence `src: Data model > Seed data`
- [ ] `C-DM-20` `data` A licence names the permitted application classes `src: Data model`
- [ ] `C-DM-21` `data` A licence names the prohibited application classes `src: Data model`
- [ ] `C-DM-22` `data` A licence states whether modification is permitted `src: Data model`
- [ ] `C-DM-23` `data` A request stage names the reviewer holding the stage `src: Data model`
- [ ] `C-DM-24` `data` The two stages of a `mark` request are held by two distinct reviewers `src: Data model`
- [ ] `C-DM-25` `data` A download record names the grant relied on `src: Data model`
- [ ] `C-DM-26` `data` An asset moves through drafted, released, superseded, retired `src: Data model > The asset lifecycle`
- [ ] `C-DM-27` `data` A grant covers every released variant of its asset `src: Data model > Variants`
- [ ] `C-DM-28` `data` An audit record carries a digest covering the preceding record `src: Data model > Tamper evidence`
- [ ] `C-DM-29` `capability` A broken audit digest chain is reported `src: Data model > Tamper evidence`
- [ ] `C-DM-30` `data` A page view record carries the route `src: Data model`

## C-FE Front-end specification

- [ ] `C-FE-01` `ui` The chrome carries a fixed menu button as the only lateral path `src: Front-end specification > Global chrome`
- [ ] `C-FE-02` `ui` The vertical rail is non interactive `src: Front-end specification > Global chrome`
- [ ] `C-FE-03` `ui` The hub carries no vertical rail `src: Front-end specification > Global chrome`
- [ ] `C-FE-04` `ui` The scroll hint retires once the reader has scrolled `src: Front-end specification > Global chrome`
- [ ] `C-FE-05` `ui` Every demonstration stage is operable by keyboard `src: Front-end specification > The demonstration canvas`
- [ ] `C-FE-06` `ui` A cursor tag follows the pointer across a demonstration stage `src: Front-end specification > The demonstration canvas`
- [ ] `C-FE-07` `ui` The consent frame sits in front of every other layer `src: Front-end specification > Stacking`
- [ ] `C-FE-08` `constraint` No element is given a shadow to imply depth `src: Front-end specification > Stacking`
- [ ] `C-FE-09` `literal` The display face is named `Ridge Grotesk` `src: Front-end specification > Chapter: Typography`
- [ ] `C-FE-10` `literal` The variable cut is named `TS Ridge Grotesk` `src: Front-end specification > Chapter: Typography`
- [ ] `C-FE-11` `literal` The text face is named `Basis Grotesk` `src: Front-end specification > Chapter: Typography`
- [ ] `C-FE-12` `literal` The foundry is named `Ridge Type` `src: Front-end specification > Chapter: Typography`
- [ ] `C-FE-13` `literal` The credit line names `Tessera Brand Studio` as the owning function `src: Front-end specification > The credit line`
- [ ] `C-FE-14` `literal` The credit line names `Meridian Studio` as the external collaborator `src: Front-end specification > The credit line`
- [ ] `C-FE-15` `ui` A placeholder asset is visibly a placeholder `src: Front-end specification > Glyphs and media`
- [ ] `C-FE-16` `constraint` No video autoplays `src: Front-end specification > Glyphs and media`
- [ ] `C-FE-17` `ui` Every public route carries a title unique to that route `src: Front-end specification > Launch readiness`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` Only PostgreSQL serves as the database `src: Constraints`
- [ ] `C-CN-02` `constraint` Only MinIO serves as the object store `src: Constraints`
- [ ] `C-CN-03` `constraint` No external identity provider is called `src: Constraints`
- [ ] `C-CN-04` `constraint` No money appears anywhere in the product `src: Constraints`
- [ ] `C-CN-05` `constraint` No email leaves the app `src: Constraints`
- [ ] `C-CN-06` `constraint` No protected object is publicly readable `src: Constraints`
- [ ] `C-CN-07` `constraint` The seven asset classes are a closed set `src: Constraints`
- [ ] `C-CN-08` `constraint` The nine request states are a closed set `src: Constraints`
- [ ] `C-CN-09` `constraint` All product text is English `src: Constraints`

## C-DC Deployment contract

- [ ] `C-DC-01` `contract` The app is reachable at `APP_PUBLIC_URL` `src: Deployment contract`
- [ ] `C-DC-02` `contract` The container-internal port is `4173` `src: Deployment contract`
- [ ] `C-DC-03` `contract` The HTTP API is served under the `/api` prefix `src: Deployment contract`
- [ ] `C-DC-04` `contract` `GET /api/health` returns `200` once ready `src: Deployment contract`
- [ ] `C-DC-05` `contract` Credentials are written to `/app/USER_README.md` `src: Deployment contract`
- [ ] `C-DC-06` `contract` The reserved directory `.browser_screenshots/` exists empty at the app root `src: Deployment contract`
- [ ] `C-DC-07` `contract` The reserved directory `.downloads/` exists empty at the app root `src: Deployment contract`
- [ ] `C-DC-08` `contract` A production build is served behind a static or preview server `src: Deployment contract`
- [ ] `C-DC-09` `contract` The server keeps running after the session ends `src: Deployment contract`
- [ ] `C-DC-10` `contract` The server binds `0.0.0.0` `src: Deployment contract`
- [ ] `C-DC-11` `contract` No copy of a backing service is downloaded or started `src: Deployment contract`
- [ ] `C-DC-12` `contract` No edge function is used `src: Deployment contract`
- [ ] `C-DC-13` `contract` No persistent volume is declared `src: Deployment contract`
- [ ] `C-DC-14` `contract` Bearer auth is required on every endpoint outside the named exemptions `src: Deployment contract > API shapes`

## Pinned literals

| Value | Where the product uses it | Item |
|---|---|---|
| `deku-demo-pw-2026` | the password on every seeded account | `C-DM-01` |
| `employee@example.com` | the seeded employee account | `C-DM-02` |
| `partner@example.com` | the seeded partner account inside an engagement | `C-DM-03` |
| `partner2@example.com` | the second seeded partner account | `C-DM-04` |
| `reviewer@example.com` | the seeded reviewer account | `C-DM-05` |
| `reviewer2@example.com` | the second seeded reviewer account | `C-DM-06` |
| `2026-11-30` | the first partner engagement end date | `C-DM-07` |
| `2027-03-31` | the second partner engagement end date | `C-DM-08` |
| `Available` | the badge for an asset the caller may download now | `C-CF-57` |
| `Request required` | the badge for an asset the caller must ask for | `C-CF-58` |
| `Restricted` | the badge for an asset needing a grant | `C-CF-59` |
| `Retired` | the badge for a withdrawn asset | `C-CF-60` |
| `logo.expressions.2` | a published statement identifier on the logo chapter | `C-CF-38` |
| `Version A` | the first permitted mark expression | `C-CF-30` |
| `Version B` | the second permitted mark expression | `C-CF-31` |
| `Prioritize Simplicity` | a published framework principle | `C-CF-25` |
| `Deepen Understanding` | a published framework principle | `C-CF-26` |
| `Instant Feedback` | a published framework principle | `C-CF-27` |
| `Subtle Playfulness` | a published framework principle | `C-CF-28` |
| `Brand Partner Toolkit` | the first outro destination | `C-CF-40` |
| `Legal Branding Resources` | the second outro destination | `C-CF-41` |
| `Tessera Design` | the third outro destination | `C-CF-42` |
| `Modern Slavery Statement` | a footer destination | `C-CF-44` |
| `Impressum` | a footer destination | `C-CF-45` |
| `Cancel Contract` | a footer destination | `C-CF-46` |
| `Cookies & CCPA preferences` | the footer destination reopening the cookie choice | `C-CF-47` |
| `Do not sell or share my personal data to third parties` | the control on the consent frame | `C-CF-50` |
| `Ridge Grotesk` | the display face | `C-FE-09` |
| `TS Ridge Grotesk` | the variable cut of the display face | `C-FE-10` |
| `Basis Grotesk` | the text face | `C-FE-11` |
| `Ridge Type` | the foundry that drew the display face | `C-FE-12` |
| `Tessera Brand Studio` | the owning in house function | `C-FE-13` |
| `Meridian Studio` | the credited external collaborator | `C-FE-14` |
| `mark` | the asset class needing two distinct reviewers | `C-CF-88` |
| `spot_icon` | an asset class granted to the first partner | `C-DM-09` |
| `pictogram` | the second asset class granted to the first partner | `C-DM-10` |
| `co_brand` | an application class adding a legal stage | `C-CF-85` |
| `merchandise` | an application class adding a legal stage | `C-CF-86` |
| `partnership` | an application class adding a legal stage | `C-CF-87` |
| `routed` | the state a resubmitted request returns to | `C-CF-84` |
| `proof_required` | the condition kind holding a grant pending | `C-CF-98` |
| `pending` | the scan state of an unscanned proof | `C-CF-100` |
| `DATABASE_URL` | the variable the database is reached at | `C-TR-01` |
| `STORAGE_ENDPOINT` | the variable the object store is reached at | `C-TR-02` |
| `STORAGE_BUCKET` | the variable naming the bucket | `C-TR-03` |
| `APP_PUBLIC_URL` | the variable the app is reachable at | `C-DC-01` |
| `4173` | the container-internal port | `C-DC-02` |
| `/api` | the prefix the HTTP API is served under | `C-DC-03` |
| `200` | the ready answer from the health endpoint | `C-DC-04` |
| `/app/USER_README.md` | the file credentials are written to | `C-DC-05` |
| `.browser_screenshots/` | a reserved directory at the app root | `C-DC-06` |
| `.downloads/` | a reserved directory at the app root | `C-DC-07` |
| `0.0.0.0` | the address the server binds | `C-DC-10` |
| `/` | the hub route | `C-CF-05` |
| `/2/` | a reserved address answering not found | `C-CF-07` |
| `/as` | a reserved address answering not found | `C-CF-08` |
| `/gs` | a reserved address answering not found | `C-CF-09` |
| `404` | the status a reserved address answers | `C-CF-10` |
| `/library` | the asset library route | `C-CF-54` |
| `/requests` | the request desk route | `C-CF-76` |
| `/queue` | the approval queue route | `C-CF-90` |
| `/admin/audit` | the audit query route | `C-CF-115` |
| `/typography` | the chapter route reached in the read flow | `C-UF-02` |

### Referenced but not pinned

| What the instruction calls it | Item |
|---|---|
| the exact colour value behind every named palette member | `C-UX-03` |
| the proof upload size cap | `C-TR-14` |
| the rate limit ceiling per principal | `C-TR-24` |
| the proof retention period | `C-TR-30` |
| the step-up validity window | `C-TR-41` |
| the deadline interval per application class | `C-CF-94` |
| the exact widths at which the layout restacks | `C-UX-12` |

## Coverage ledger

| Section | Obligation sentences | Items produced |
|---|---|---|
| Overview | 6 | 6 |
| User roles | 5 | 15 |
| Core features | 26 | 127 |
| User flow | 10 | 16 |
| UI and UX notes | 8 | 15 |
| Technical requirements | 12 | 51 |
| Data model | 9 | 30 |
| Front-end specification | 7 | 17 |
| Constraints | 4 | 9 |
| Deployment contract | 13 | 14 |
