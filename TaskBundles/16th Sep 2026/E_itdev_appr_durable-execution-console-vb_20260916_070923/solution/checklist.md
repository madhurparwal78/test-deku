# Checklist: Perpetua Cloud

Source: instruction.md
Sections present: overview, roles, features, flow, uiux, technical, datamodel, frontend, constraints, deployment
Sections absent: buildplan
Items: 343
Unpinned values flagged: 3

## C-OV Overview

- [ ] `C-OV-01` `capability` The product presents an operator console for a durable execution platform. `src: Overview para 1`
- [ ] `C-OV-02` `capability` The product presents a public product surface beside the console. `src: Overview para 1`
- [ ] `C-OV-03` `capability` A platform team manages namespaces across regions from the console. `src: Overview para 4`
- [ ] `C-OV-04` `capability` An engineer browses running workflow executions from the console. `src: Overview para 4`
- [ ] `C-OV-05` `capability` An engineer files a namespace change request from the console. `src: Overview para 4`
- [ ] `C-OV-06` `role` A namespace admin reviews a filed namespace change request. `src: Overview para 4`
- [ ] `C-OV-07` `constraint` The product omits every money path. `src: Overview final para`
- [ ] `C-OV-08` `constraint` The product omits schedules. `src: Overview final para`
- [ ] `C-OV-09` `constraint` The product omits outbound webhooks. `src: Overview final para`
- [ ] `C-OV-10` `capability` Authorisation resolves again immediately before a change request is applied. `src: Overview hard-part para`
- [ ] `C-OV-11` `data` Organisations never nest inside other organisations. `src: Overview information-architecture para`
- [ ] `C-OV-12` `data` A project groups namespaces without forming a tenancy boundary. `src: Overview information-architecture para`

## C-RL User roles

- [ ] `C-RL-01` `role` A `developer` reads executions inside a namespace covered by a held grant. `src: User roles table row 1`
- [ ] `C-RL-02` `role` A `developer` files a change request. `src: User roles table row 1`
- [ ] `C-RL-03` `role` A `developer` withdraws a change request filed by that same principal. `src: User roles table row 1`
- [ ] `C-RL-04` `role` A `developer` never approves any change request. `src: User roles table row 1`
- [ ] `C-RL-05` `role` A `developer` never applies any change request. `src: User roles table row 1`
- [ ] `C-RL-06` `role` A `developer` never creates a namespace. `src: User roles table row 1`
- [ ] `C-RL-07` `role` A `developer` never grants a role. `src: User roles table row 1`
- [ ] `C-RL-08` `role` A `developer` never reads a namespace covered by no held grant. `src: User roles table row 1`
- [ ] `C-RL-09` `role` A `namespace-admin` approves a change request filed by another principal. `src: User roles table row 2`
- [ ] `C-RL-10` `role` A `namespace-admin` applies an approved change request. `src: User roles table row 2`
- [ ] `C-RL-11` `role` A `namespace-admin` creates a namespace. `src: User roles table row 2`
- [ ] `C-RL-12` `role` A `namespace-admin` never approves a change request filed by that same principal. `src: User roles table row 2`
- [ ] `C-RL-13` `role` A `namespace-admin` never reads another organisation. `src: User roles table row 2`
- [ ] `C-RL-14` `role` An `owner` grants a role at organisation scope. `src: User roles table row 3`
- [ ] `C-RL-15` `role` An `owner` reads the audit trail. `src: User roles table row 3`
- [ ] `C-RL-16` `role` An `owner` never approves a change request filed by that same principal. `src: User roles table row 3`
- [ ] `C-RL-17` `role` An `owner` never edits an audit entry. `src: User roles table row 3`
- [ ] `C-RL-18` `role` The server refuses a mutating call from a lower role to a higher-role endpoint. `src: User roles authorization para`
- [ ] `C-RL-19` `constraint` A refused mutating call leaves the protected state unchanged. `src: User roles authorization para`
- [ ] `C-RL-20` `constraint` No route creates an account. `src: User roles signup para`
- [ ] `C-RL-21` `data` A grant carries an effect of either `allow` or `deny`. `src: User roles closing para`
- [ ] `C-RL-22` `data` A grant carries an optional expiry. `src: User roles closing para`

## C-CF Core features

- [ ] `C-CF-01` `literal` Signing in reaches the identity provider at `AUTH_URL`. `src: Core features Auth rule 1`
- [ ] `C-CF-02` `literal` The endpoint `/api/auth/login` accepts an email with a password. `src: Core features Auth rule 1`
- [ ] `C-CF-03` `capability` A successful sign-in returns a bearer token. `src: Core features Auth rule 1`
- [ ] `C-CF-04` `capability` A successful sign-in returns the effective roles of the principal. `src: Core features Auth rule 1`
- [ ] `C-CF-05` `constraint` A request carrying no bearer token is denied. `src: Core features Auth rule 2`
- [ ] `C-CF-06` `constraint` A request carrying an expired bearer token is denied. `src: Core features Auth rule 2`
- [ ] `C-CF-07` `capability` A token minted at sign-in stays usable for at least one hour. `src: Core features Auth rule 3`
- [ ] `C-CF-08` `constraint` No endpoint echoes a password back. `src: Core features Auth rule 4`
- [ ] `C-CF-09` `capability` Signing out invalidates the session. `src: Core features Auth rule 5`
- [ ] `C-CF-10` `constraint` A replayed token from an invalidated session is denied. `src: Core features Auth rule 5`
- [ ] `C-CF-11` `constraint` A failed sign-in never falls back to a weaker authentication method. `src: Core features Auth rule 6`
- [ ] `C-CF-12` `constraint` A failed sign-in message never reveals whether an address exists. `src: Core features Auth rule 6`
- [ ] `C-CF-13` `capability` The home route carries an interactive failure-and-recovery demonstrator. `src: Core features 1 rule 1`
- [ ] `C-CF-14` `capability` The demonstrator fails a third activity deliberately, then recovers. `src: Core features 1 rule 1`
- [ ] `C-CF-15` `constraint` Recovery redraws no activity bar already completed. `src: Core features 1 rule 2`
- [ ] `C-CF-16` `constraint` The demonstrator fetches no media file. `src: Core features 1 rule 3`
- [ ] `C-CF-17` `constraint` The transcript stays put when the reader has scrolled upward. `src: Core features 1 rule 4`
- [ ] `C-CF-18` `literal` The route `/product` tours the platform capabilities. `src: Core features 1 rule 5`
- [ ] `C-CF-19` `literal` The route `/pricing` presents a four-column entitlement matrix. `src: Core features 1 rule 6`
- [ ] `C-CF-20` `literal` The route `/security` states the isolation posture in prose. `src: Core features 1 rule 7`
- [ ] `C-CF-21` `constraint` No route reproduces a compliance certification claim. `src: Core features 1 rule 7`
- [ ] `C-CF-22` `literal` The route `/privacy` states what the product stores about a person. `src: Core features 1 rule 8`
- [ ] `C-CF-23` `capability` A privacy link reaches the privacy page from the footer of every page. `src: Core features 1 rule 8`
- [ ] `C-CF-24` `literal` The route `/get-cloud` records an account enquiry. `src: Core features 1 rule 9`
- [ ] `C-CF-25` `constraint` The account enquiry route creates no account. `src: Core features 1 rule 9`
- [ ] `C-CF-26` `capability` Every form rejects invalid input inline. `src: Core features 1 rule 10`
- [ ] `C-CF-27` `capability` Every form names the offending field beside the field. `src: Core features 1 rule 10`
- [ ] `C-CF-28` `constraint` An invalid submission writes no row. `src: Core features 1 rule 10`
- [ ] `C-CF-29` `capability` An unknown address renders the product not-found page. `src: Core features 1 rule 11`
- [ ] `C-CF-30` `capability` The not-found page offers a way back. `src: Core features 1 rule 11`
- [ ] `C-CF-31` `constraint` Every internal link on a public route resolves. `src: Core features 1 rule 12`
- [ ] `C-CF-32` `capability` The site serves a favicon declared in the document head. `src: Core features 1 rule 13`
- [ ] `C-CF-33` `literal` The route `/sitemap.xml` lists every public route served. `src: Core features 1 rule 14`
- [ ] `C-CF-34` `literal` The route `/robots.txt` refers to the sitemap. `src: Core features 1 rule 14`
- [ ] `C-CF-35` `constraint` No public route reads the control plane. `src: Core features 1 rule 15`
- [ ] `C-CF-36` `constraint` No public route requires a session. `src: Core features 1 rule 15`
- [ ] `C-CF-37` `data` The reviewable change kinds form a closed set of ten names. `src: Core features 2 rule 1`
- [ ] `C-CF-38` `data` Each change kind carries how many approvals the kind needs. `src: Core features 2 rule 1`
- [ ] `C-CF-39` `ui` Filing a change request opens in a modal from the request queue. `src: Core features 2 rule 2`
- [ ] `C-CF-40` `capability` Filing a change request lands on a full-page confirmation. `src: Core features 2 rule 2`
- [ ] `C-CF-41` `data` A change request moves through the nine named lifecycle states. `src: Core features 2 rule 3`
- [ ] `C-CF-42` `data` A change request enters `pending` on submission. `src: Core features 2 rule 3`
- [ ] `C-CF-43` `data` A failed change request carries a reason. `src: Core features 2 rule 3`
- [ ] `C-CF-44` `role` The requesting principal is never the sole approver of a change request. `src: Core features 2 rule 4`
- [ ] `C-CF-45` `role` Self-approval is denied even for a principal holding every role. `src: Core features 2 rule 4`
- [ ] `C-CF-46` `constraint` A denied self-approval records no approval against the request. `src: Core features 2 rule 4`
- [ ] `C-CF-47` `capability` Policy resolves at submission of a change request. `src: Core features 2 rule 5`
- [ ] `C-CF-48` `capability` Policy resolves again immediately before application of a change request. `src: Core features 2 rule 5`
- [ ] `C-CF-49` `capability` A request whose filer lost the underlying permission fails at application. `src: Core features 2 rule 5`
- [ ] `C-CF-50` `capability` The failure reason names the lost permission. `src: Core features 2 rule 5`
- [ ] `C-CF-51` `constraint` A failed application leaves the subject unchanged. `src: Core features 2 rule 5`
- [ ] `C-CF-52` `capability` A request whose approver lost the permission fails at application. `src: Core features 2 rule 5`
- [ ] `C-CF-53` `capability` Application is idempotent on a caller-supplied request identifier. `src: Core features 2 rule 6`
- [ ] `C-CF-54` `constraint` Two applications of one approved request produce one audit entry. `src: Core features 2 rule 6`
- [ ] `C-CF-55` `constraint` Two concurrent approvals produce one applied change. `src: Core features 2 rule 7`
- [ ] `C-CF-56` `constraint` A partly failed application never leaves the request `applied`. `src: Core features 2 rule 8`
- [ ] `C-CF-57` `role` An approve call from a `developer` session is denied. `src: Core features 2 rule 9`
- [ ] `C-CF-58` `constraint` A denied approve call leaves the request row unchanged. `src: Core features 2 rule 9`
- [ ] `C-CF-59` `capability` The request queue offers three named views. `src: Core features 2 rule 10`
- [ ] `C-CF-60` `ui` The request queue shows a count beside the rail entry. `src: Core features 2 rule 10`
- [ ] `C-CF-61` `ui` The request detail shows the subject as a before comparison against an after comparison. `src: Core features 2 rule 11`
- [ ] `C-CF-62` `capability` The before side of a request detail is read when the detail opens. `src: Core features 2 rule 11`
- [ ] `C-CF-63` `ui` The request detail marks a before side changed since submission. `src: Core features 2 rule 11`
- [ ] `C-CF-64` `ui` The request detail redacts any secret value. `src: Core features 2 rule 11`
- [ ] `C-CF-65` `capability` Rejecting a change request requires a reason. `src: Core features 2 rule 12`
- [ ] `C-CF-66` `role` Withdrawing a change request is available only to the requester. `src: Core features 2 rule 12`
- [ ] `C-CF-67` `capability` A request passing its expiry without the required approvals becomes `expired`. `src: Core features 2 rule 13`
- [ ] `C-CF-68` `data` A namespace belongs to exactly one organisation. `src: Core features 3 rule 1`
- [ ] `C-CF-69` `data` A namespace name is unique within one organisation. `src: Core features 3 rule 1`
- [ ] `C-CF-70` `capability` The namespace uniqueness check runs again at commit. `src: Core features 3 rule 1`
- [ ] `C-CF-71` `data` The legal namespace regions form a closed set of three names. `src: Core features 3 rule 2`
- [ ] `C-CF-72` `data` Namespace creation carries a visible state from four named values. `src: Core features 3 rule 3`
- [ ] `C-CF-73` `constraint` A failed namespace creation leaves no half-created namespace listed. `src: Core features 3 rule 3`
- [ ] `C-CF-74` `constraint` A namespace region never changes after creation. `src: Core features 3 rule 4`
- [ ] `C-CF-75` `ui` The namespace creation form states the region immutability during choosing. `src: Core features 3 rule 4`
- [ ] `C-CF-76` `ui` Reducing retention states how many executions the reduction affects. `src: Core features 3 rule 6`
- [ ] `C-CF-77` `ui` Reducing retention requires the operator to type the namespace name. `src: Core features 3 rule 6`
- [ ] `C-CF-78` `capability` A retention reduction under review is filed as a change request. `src: Core features 3 rule 6`
- [ ] `C-CF-79` `capability` A certificate bundle replacement accepts both entries during an overlap window. `src: Core features 3 rule 7`
- [ ] `C-CF-80` `constraint` A namespace never interacts with another namespace. `src: Core features 3 rule 8`
- [ ] `C-CF-81` `capability` The isolation check resolves the namespace from the credential. `src: Core features 3 rule 8`
- [ ] `C-CF-82` `constraint` A cross-organisation request is answered as a resource that does not exist. `src: Core features 3 rule 9`
- [ ] `C-CF-83` `constraint` No operation moves a region-pinned namespace payload out of the region. `src: Core features 3 rule 10`
- [ ] `C-CF-84` `data` A replicated namespace carries one primary region with standby regions. `src: Core features 3 rule 11`
- [ ] `C-CF-85` `ui` The failover control shows the current replication lag beside the control. `src: Core features 3 rule 12`
- [ ] `C-CF-86` `capability` An operator-initiated failover is filed as a change request. `src: Core features 3 rule 12`
- [ ] `C-CF-87` `data` An execution carries a caller-chosen workflow identifier. `src: Core features 4 rule 1`
- [ ] `C-CF-88` `data` An execution carries a platform-generated run identifier. `src: Core features 4 rule 1`
- [ ] `C-CF-89` `data` An execution status comes from the seven named values. `src: Core features 4 rule 2`
- [ ] `C-CF-90` `constraint` Ten simultaneous starts of one workflow identifier produce exactly one execution. `src: Core features 4 rule 3`
- [ ] `C-CF-91` `capability` The execution list presents a queue ordered newest first. `src: Core features 4 rule 4`
- [ ] `C-CF-92` `ui` Selecting a quick-filter chip writes the chip query into the query bar. `src: Core features 4 rule 5`
- [ ] `C-CF-93` `capability` The query bar accepts a structured query rather than free text. `src: Core features 4 rule 6`
- [ ] `C-CF-94` `capability` A query syntax error appears inline at the causing character offset. `src: Core features 4 rule 6`
- [ ] `C-CF-95` `capability` Execution list paging uses a cursor rather than an offset. `src: Core features 4 rule 7`
- [ ] `C-CF-96` `constraint` An insertion between two page fetches produces no duplicated row. `src: Core features 4 rule 7`
- [ ] `C-CF-97` `constraint` An insertion between two page fetches produces no skipped row. `src: Core features 4 rule 7`
- [ ] `C-CF-98` `constraint` A cursor from a differently sorted query is rejected. `src: Core features 4 rule 7`
- [ ] `C-CF-99` `ui` A retried activity appears as segments within one timeline bar. `src: Core features 4 rule 9`
- [ ] `C-CF-100` `constraint` The execution header renders without fetching the event history. `src: Core features 4 rule 10`
- [ ] `C-CF-101` `capability` A history download is a queued job rather than a synchronous stream. `src: Core features 4 rule 11`
- [ ] `C-CF-102` `constraint` A history download result reference is bound to the submitting principal. `src: Core features 4 rule 11`
- [ ] `C-CF-103` `ui` A payload renders in one of the five named states. `src: Core features 4 rule 12`
- [ ] `C-CF-104` `constraint` No server-side call to a codec endpoint exists. `src: Core features 4 rule 13`
- [ ] `C-CF-105` `capability` Payload decoding happens in the operator browser. `src: Core features 4 rule 13`
- [ ] `C-CF-106` `data` An execution status is derived from the event history. `src: Core features 4 rule 14`
- [ ] `C-CF-107` `constraint` No event is modified after being appended. `src: Core features 4 rule 14`
- [ ] `C-CF-108` `capability` Resetting an execution creates a new run from a chosen event. `src: Core features 4 rule 15`
- [ ] `C-CF-109` `constraint` Resetting an execution leaves the old run unmodified. `src: Core features 4 rule 15`
- [ ] `C-CF-110` `capability` The empty execution list offers a direct lookup by identifier. `src: Core features 4 rule 16`
- [ ] `C-CF-111` `data` The history store stays authoritative over the search index. `src: Core features 4 rule 16`
- [ ] `C-CF-112` `constraint` No operation writes to the search index. `src: Core features 4 rule 16`
- [ ] `C-CF-113` `ui` The cancel action never sits beside the terminate action. `src: Core features 4 rule 17`
- [ ] `C-CF-114` `ui` Terminating requires the workflow identifier to be typed. `src: Core features 4 rule 17`
- [ ] `C-CF-115` `constraint` A retried terminate produces one audit entry. `src: Core features 4 rule 17`
- [ ] `C-CF-116` `data` A principal is one of the three named kinds. `src: Core features 5 rule 1`
- [ ] `C-CF-117` `capability` An explicit deny grant defeats an allow grant at a wider scope. `src: Core features 5 rule 3`
- [ ] `C-CF-118` `constraint` An expired grant is never collected for a decision. `src: Core features 5 rule 4`
- [ ] `C-CF-119` `capability` Grant expiry resolves at decision time against the request clock. `src: Core features 5 rule 4`
- [ ] `C-CF-120` `capability` An expired grant stays visible marked as expired. `src: Core features 5 rule 4`
- [ ] `C-CF-121` `constraint` A principal never creates a custom role exceeding held permissions. `src: Core features 5 rule 5`
- [ ] `C-CF-122` `constraint` The rail filtering is never the authorisation check. `src: Core features 5 rule 6`
- [ ] `C-CF-123` `capability` The rail is filtered on the server by effective permissions. `src: Core features 5 rule 6`
- [ ] `C-CF-124` `constraint` An invitation to an existing member address is refused. `src: Core features 5 rule 8`
- [ ] `C-CF-125` `capability` Removing a person revokes every grant held by that person. `src: Core features 5 rule 9`
- [ ] `C-CF-126` `constraint` Removing a person deletes no audit entry attributed to that person. `src: Core features 5 rule 9`
- [ ] `C-CF-127` `constraint` The last owner of an organisation is never removed. `src: Core features 5 rule 10`
- [ ] `C-CF-128` `constraint` A directory-provisioned group membership is read-only in the console. `src: Core features 5 rule 11`
- [ ] `C-CF-129` `constraint` Sign-on enforcement is never enabled without a verified domain. `src: Core features 5 rule 13`
- [ ] `C-CF-130` `data` A worker reachability state is derived from the last poll time. `src: Core features 6 rule 1`
- [ ] `C-CF-131` `constraint` Nothing opens a connection into a customer network. `src: Core features 6 rule 3`
- [ ] `C-CF-132` `capability` The namespace home shows the task-queue backlog. `src: Core features 6 rule 4`
- [ ] `C-CF-133` `capability` Every mutating operation writes exactly one audit entry. `src: Core features 7 rule 1`
- [ ] `C-CF-134` `constraint` No endpoint updates an audit entry. `src: Core features 7 rule 2`
- [ ] `C-CF-135` `constraint` No endpoint deletes an audit entry. `src: Core features 7 rule 2`
- [ ] `C-CF-136` `data` An audit entry carries the hash of the previous entry. `src: Core features 7 rule 3`
- [ ] `C-CF-137` `capability` A denied attempt is written to the audit trail. `src: Core features 7 rule 4`
- [ ] `C-CF-138` `capability` Deleting a person leaves a stable pseudonymous attribution. `src: Core features 7 rule 5`
- [ ] `C-CF-139` `capability` An applied change request names every approving principal in the audit entry. `src: Core features 7 rule 6`
- [ ] `C-CF-140` `capability` The scope of a console route appears in the address. `src: Core features 8 rule 1`
- [ ] `C-CF-141` `ui` A breadcrumb trail names every level from the organisation downward. `src: Core features 8 rule 2`
- [ ] `C-CF-142` `ui` Switching scope never leaves the viewer on the old scope screen. `src: Core features 8 rule 3`

## C-UF User flow

- [ ] `C-UF-01` `capability` An unauthenticated request for a console route reaches the sign-in route. `src: User flow entry para`
- [ ] `C-UF-02` `capability` Signing in lands on the originally requested address. `src: User flow entry para`
- [ ] `C-UF-03` `capability` Signing out returns to the home route. `src: User flow entry para`
- [ ] `C-UF-04` `capability` A principal belonging to several organisations reaches an organisation chooser. `src: User flow entry para`
- [ ] `C-UF-05` `capability` A token expiring mid-action leaves the work in progress on screen. `src: User flow entry para`
- [ ] `C-UF-06` `ui` A route beyond a principal grant renders a not-permitted state. `src: User flow entry para`
- [ ] `C-UF-07` `capability` A developer files a retention reduction from the namespace settings screen. `src: User flow journey 1`
- [ ] `C-UF-08` `capability` A namespace admin approves the filed retention reduction with a reason. `src: User flow journey 1`
- [ ] `C-UF-09` `capability` Applying the approved reduction changes the reported namespace retention. `src: User flow journey 1`
- [ ] `C-UF-10` `capability` The audit trail carries one entry naming both principals. `src: User flow journey 1`
- [ ] `C-UF-11` `role` A developer approve call on a self-filed request is denied. `src: User flow journey 2`
- [ ] `C-UF-12` `role` An owner approve call on a self-filed request is denied. `src: User flow journey 2`
- [ ] `C-UF-13` `capability` Revoking the filer grant before application moves the request to `failed`. `src: User flow journey 3`
- [ ] `C-UF-14` `capability` An engineer reads a failed execution event history by cursor. `src: User flow journey 4`
- [ ] `C-UF-15` `constraint` A second-organisation session reading the first organisation namespace is refused. `src: User flow journey 5`
- [ ] `C-UF-16` `ui` Every list carries an empty state distinguishing never-existed from filter-too-narrow. `src: User flow states para`
- [ ] `C-UF-17` `ui` Every page carries a loading state reserving the content space. `src: User flow states para`
- [ ] `C-UF-18` `ui` A failed fetch keeps the last good data beside a banner. `src: User flow states para`
- [ ] `C-UF-19` `ui` A form failing validation keeps what the operator typed. `src: User flow states para`

## C-UX UI and UX notes

- [ ] `C-UX-01` `ui` The interface reads quiet, information-dense, built for scanning. `src: UI/UX notes register para`
- [ ] `C-UX-02` `ui` The page ground is a near-black neutral under near-white neutral ink. `src: UI/UX notes ground para`
- [ ] `C-UX-03` `ui` Supporting copy on a dark ground uses the lighter muted blue. `src: UI/UX notes ground para`
- [ ] `C-UX-04` `ui` The primary action wears the blended blue into indigo exclusively. `src: UI/UX notes colour para`
- [ ] `C-UX-05` `ui` Failure colour appears nowhere except where something has gone wrong. `src: UI/UX notes colour para`
- [ ] `C-UX-06` `ui` The display family carries prose, the monospace family carries machine utterances. `src: UI/UX notes type para`
- [ ] `C-UX-07` `ui` No italic appears anywhere in the build. `src: UI/UX notes type para`
- [ ] `C-UX-08` `ui` Motion character is mechanical, landing state changes promptly. `src: UI/UX notes motion para`
- [ ] `C-UX-09` `constraint` No ambient animation runs anywhere inside the console. `src: UI/UX notes motion para`
- [ ] `C-UX-10` `ui` A reduced-motion preference keeps pointer transitions at full strength. `src: UI/UX notes motion para`
- [ ] `C-UX-11` `ui` Console density is compact so a full queue fits one screen. `src: UI/UX notes density para`
- [ ] `C-UX-12` `ui` Nothing overflows sideways at any viewport on any route. `src: UI/UX notes responsive para`
- [ ] `C-UX-13` `ui` Body text meets WCAG AA contrast against the ground. `src: UI/UX notes accessibility para`
- [ ] `C-UX-14` `ui` Keyboard navigation reaches every control with a visible focus ring. `src: UI/UX notes accessibility para`
- [ ] `C-UX-15` `ui` Meaning is never carried by colour alone. `src: UI/UX notes accessibility para`
- [ ] `C-UX-16` `ui` Every dialog traps focus during the open period. `src: UI/UX notes structure para`
- [ ] `C-UX-17` `ui` Every dialog closes on the escape key. `src: UI/UX notes structure para`
- [ ] `C-UX-18` `ui` Every dialog restores focus to the opening control. `src: UI/UX notes structure para`

## C-TR Technical requirements

- [ ] `C-TR-01` `contract` The frontend is Svelte compiled with Vite. `src: Technical requirements para 1`
- [ ] `C-TR-02` `contract` The backend is FastAPI serving the API under the prefix. `src: Technical requirements para 1`
- [ ] `C-TR-03` `contract` The browser receives an application shell on first paint. `src: Technical requirements para 1`
- [ ] `C-TR-04` `literal` The datastore is PostgreSQL read from `DATABASE_URL`. `src: Technical requirements para 1`
- [ ] `C-TR-05` `contract` Identity is Keycloak holding the seeded principals. `src: Technical requirements para 1`
- [ ] `C-TR-06` `contract` Logs go to standard output as one structured line per request. `src: Technical requirements para 1`
- [ ] `C-TR-07` `constraint` No second database is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-08` `constraint` No second identity provider is introduced. `src: Technical requirements para 2`
- [ ] `C-TR-09` `contract` Every host is read from the environment rather than hardcoded. `src: Technical requirements para 3`
- [ ] `C-TR-10` `constraint` The app creates no realm in the identity provider. `src: Technical requirements para 3`
- [ ] `C-TR-11` `contract` Every response carries the standard security headers. `src: Technical requirements para 4`
- [ ] `C-TR-12` `contract` Every response carries a content-type policy refusing sniffing. `src: Technical requirements para 4`
- [ ] `C-TR-13` `constraint` No credential appears in anything the browser downloads. `src: Technical requirements para 4`
- [ ] `C-TR-14` `contract` An error answer carries a stable machine-readable code. `src: Technical requirements para 5`
- [ ] `C-TR-15` `contract` A permission refusal matches a not-found refusal exactly. `src: Technical requirements para 5`
- [ ] `C-TR-16` `contract` A rate-limit answer carries the remaining budget with the reset time. `src: Technical requirements para 5`
- [ ] `C-TR-17` `contract` Validation rules are declared once per operation. `src: Technical requirements para 6`
- [ ] `C-TR-18` `capability` The execution detail header renders without reading the history. `src: Technical requirements para 7`
- [ ] `C-TR-19` `capability` Heavy surfaces mount only when opened. `src: Technical requirements para 7`
- [ ] `C-TR-20` `capability` Every mutating operation accepts a caller-supplied request identifier. `src: Technical requirements para 8`

## C-DM Data model

- [ ] `C-DM-01` `data` The data model carries fourteen tables. `src: Data model para 1`
- [ ] `C-DM-02` `data` All timestamps are UTC. `src: Data model para 1`
- [ ] `C-DM-03` `literal` Every seeded account uses the password `deku-demo-pw-2026`. `src: Data model password para`
- [ ] `C-DM-04` `literal` Each seeded account is written into `/app/USER_README.md`. `src: Data model password para`
- [ ] `C-DM-05` `data` An append-only table carries an occurrence timestamp without an update timestamp. `src: Data model conventions para`
- [ ] `C-DM-06` `data` Every relationship states the behaviour on far-end deletion. `src: Data model conventions para`
- [ ] `C-DM-07` `data` A person email is unique after case folding. `src: Data model person table`
- [ ] `C-DM-08` `data` A grant table is the only place authorisation is stored. `src: Data model grant table`
- [ ] `C-DM-09` `constraint` No administrator flag exists on the person table. `src: Data model grant table`
- [ ] `C-DM-10` `data` A namespace region never changes after row creation. `src: Data model namespace table`
- [ ] `C-DM-11` `data` A search attribute type comes from the seven named values. `src: Data model search attribute table`
- [ ] `C-DM-12` `data` An event identifier increases monotonically within one execution. `src: Data model execution event table`
- [ ] `C-DM-13` `constraint` No execution event row is reordered. `src: Data model execution event table`
- [ ] `C-DM-14` `data` At most one approval row exists per principal per request. `src: Data model change approval table`
- [ ] `C-DM-15` `data` An audit entry chains to the previous entry of the organisation. `src: Data model audit entry table`
- [ ] `C-DM-16` `data` A job result reference is single-use, bound to the submitter. `src: Data model job table`
- [ ] `C-DM-17` `constraint` A change request never reaches `applied` without a non-requester approval. `src: Data model invariants list`
- [ ] `C-DM-18` `constraint` Two simultaneous applications produce exactly one subject change. `src: Data model invariants list`
- [ ] `C-DM-19` `constraint` Two simultaneous namespace creations of one name produce exactly one namespace. `src: Data model invariants list`
- [ ] `C-DM-20` `constraint` An execution event identifier sequence carries no gap. `src: Data model invariants list`
- [ ] `C-DM-21` `constraint` An audit entry is never observed with different content afterwards. `src: Data model invariants list`
- [ ] `C-DM-22` `constraint` A failed operation leaves no partial state. `src: Data model invariants list`
- [ ] `C-DM-23` `literal` The seed carries the organisation `Northwind Trading`. `src: Data model seed para 1`
- [ ] `C-DM-24` `literal` The seed carries the organisation `Forgelab`. `src: Data model seed para 1`
- [ ] `C-DM-25` `literal` The seed carries the namespace `payments-prod`. `src: Data model seed para 2`
- [ ] `C-DM-26` `literal` The seed carries the namespace `orders-prod`. `src: Data model seed para 2`
- [ ] `C-DM-27` `literal` The seed carries the namespace `ledger-prod`. `src: Data model seed para 2`
- [ ] `C-DM-28` `literal` The seed carries the account `developer@example.com`. `src: Data model seed para 3`
- [ ] `C-DM-29` `literal` The seed carries the account `developer2@example.com`. `src: Data model seed para 3`
- [ ] `C-DM-30` `literal` The seed carries the account `namespace-admin@example.com`. `src: Data model seed para 3`
- [ ] `C-DM-31` `literal` The seed carries the account `namespace-admin2@example.com`. `src: Data model seed para 3`
- [ ] `C-DM-32` `literal` The seed carries the account `owner@example.com`. `src: Data model seed para 3`
- [ ] `C-DM-33` `data` The owner principal holds every other built-in role by explicit grant. `src: Data model seed para 3`
- [ ] `C-DM-34` `data` The seed carries one expired grant on the second namespace. `src: Data model seed para 4`
- [ ] `C-DM-35` `data` The seed carries one explicit deny grant at namespace scope. `src: Data model seed para 4`
- [ ] `C-DM-36` `literal` The kind `reduce_retention` requires one approval under the seeded policy. `src: Data model seed para 5`
- [ ] `C-DM-37` `data` The seed carries one pending change request with no approval recorded. `src: Data model seed para 6`
- [ ] `C-DM-38` `data` The seed carries one applied change request. `src: Data model seed para 6`
- [ ] `C-DM-39` `literal` The seed carries the execution `subscription-9f21c4d0`. `src: Data model seed para 7`
- [ ] `C-DM-40` `literal` The failed seeded execution carries the run identifier `01J7Y6M2R8`. `src: Data model seed para 7`
- [ ] `C-DM-41` `data` The failed seeded execution carries a retried activity with three segments. `src: Data model seed para 7`
- [ ] `C-DM-42` `data` The seed carries one execution in the second organisation namespace. `src: Data model seed para 7`
- [ ] `C-DM-43` `data` The seed carries one unreachable worker. `src: Data model seed para 8`
- [ ] `C-DM-44` `data` The seed carries one trust bundle entry expiring within the warning threshold. `src: Data model seed para 8`
- [ ] `C-DM-45` `data` The seed carries one payload in each of the five render states. `src: Data model seed para 9`
- [ ] `C-DM-46` `constraint` Seeding is idempotent across a restart. `src: Data model closing line`

## C-FE Front-end specification

- [ ] `C-FE-01` `constraint` No route fetches an image file. `src: Front-end specification no-asset para`
- [ ] `C-FE-02` `constraint` No route fetches an icon file. `src: Front-end specification no-asset para`
- [ ] `C-FE-03` `ui` The star field tiles seamlessly with no visible seam. `src: Front-end specification star field para`
- [ ] `C-FE-04` `ui` The star field stays stable across builds at a fixed seed. `src: Front-end specification star field para`
- [ ] `C-FE-05` `ui` The perspective grid lines fade before reaching the horizon. `src: Front-end specification grid para`
- [ ] `C-FE-06` `ui` The perspective grid converges on a horizontally centred vanishing point. `src: Front-end specification grid para`
- [ ] `C-FE-07` `constraint` No synthetic photographic likeness attaches to a named person. `src: Front-end specification likeness para`
- [ ] `C-FE-08` `ui` The gradient edge renders without a wrapper element. `src: Front-end specification gradient-edge para`
- [ ] `C-FE-09` `ui` The gradient edge degrades to a real border under forced colours. `src: Front-end specification gradient-edge para`
- [ ] `C-FE-10` `ui` Every gap is an integer multiple of one spacing unit. `src: Front-end specification scaling para`
- [ ] `C-FE-11` `ui` The header reserves one height at every width on every route. `src: Front-end specification scaling para`
- [ ] `C-FE-12` `ui` The console rail carries two tiers of navigation entries. `src: Front-end specification shell para`
- [ ] `C-FE-13` `ui` Every rail entry keeps an accessible name in the collapsed state. `src: Front-end specification shell para`
- [ ] `C-FE-14` `ui` Console table sorting happens on the server. `src: Front-end specification table para`
- [ ] `C-FE-15` `ui` Selecting the result set is separate from selecting the page. `src: Front-end specification table para`
- [ ] `C-FE-16` `ui` A console table error keeps the last good rows beside a banner. `src: Front-end specification table para`
- [ ] `C-FE-17` `ui` Every icon inherits the text colour of the container. `src: Front-end specification iconography para`
- [ ] `C-FE-18` `ui` The brand mark accessible name is the product name. `src: Front-end specification iconography para`
- [ ] `C-FE-19` `ui` The demonstrator meter announces each state change once. `src: Front-end specification demonstrator para`
- [ ] `C-FE-20` `ui` Switching the demonstrator scenario mid-run never restarts the run. `src: Front-end specification demonstrator para`
- [ ] `C-FE-21` `ui` Exactly one scroll subscription exists per public route. `src: Front-end specification scroll para`
- [ ] `C-FE-22` `ui` The fixed copy strings appear exactly as written. `src: Front-end specification copy identity para`
- [ ] `C-FE-23` `constraint` No real company name appears anywhere in the build. `src: Front-end specification copy identity para`
- [ ] `C-FE-24` `capability` An unreachable datastore leaves the public routes serving. `src: Front-end specification degraded para`
- [ ] `C-FE-25` `capability` An unreachable codec endpoint renders the decode-failed state. `src: Front-end specification degraded para`

## C-CN Constraints

- [ ] `C-CN-01` `constraint` The build serves exactly the two seeded organisations. `src: Constraints para 1`
- [ ] `C-CN-02` `constraint` No self-service organisation creation exists. `src: Constraints para 1`
- [ ] `C-CN-03` `constraint` No billing surface exists. `src: Constraints para 2`
- [ ] `C-CN-04` `constraint` No schedule surface exists. `src: Constraints para 2`
- [ ] `C-CN-05` `constraint` No outbound webhook surface exists. `src: Constraints para 2`
- [ ] `C-CN-06` `constraint` The fourteen named marketing routes are absent. `src: Constraints para 2`
- [ ] `C-CN-07` `constraint` Nothing reaches the public internet at runtime. `src: Constraints para 3`
- [ ] `C-CN-08` `constraint` No third-party font is fetched. `src: Constraints para 3`
- [ ] `C-CN-09` `constraint` No native application is built. `src: Constraints para 4`
- [ ] `C-CN-10` `constraint` No email is sent. `src: Constraints para 5`
- [ ] `C-CN-11` `constraint` No payload is parsed beyond rendering. `src: Constraints para 6`
- [ ] `C-CN-12` `constraint` The app stays responsive at the stated data volume. `src: Constraints para 7`

## C-DC Deployment contract

- [ ] `C-DC-01` `literal` The app is reachable at `APP_PUBLIC_URL`. `src: Deployment contract line 1`
- [ ] `C-DC-02` `literal` The container-internal port is `4173`. `src: Deployment contract line 1`
- [ ] `C-DC-03` `contract` The port mapping is read from the environment rather than hardcoded. `src: Deployment contract line 1`
- [ ] `C-DC-04` `contract` The HTTP API is served on the same origin under the api prefix. `src: Deployment contract line 2`
- [ ] `C-DC-05` `literal` The route `/api/health` returns a success status once ready. `src: Deployment contract line 3`
- [ ] `C-DC-06` `contract` The app starts from the environment image with no manual step. `src: Deployment contract line 4`
- [ ] `C-DC-07` `contract` Login credentials are written to the reserved readme path. `src: Deployment contract line 5`
- [ ] `C-DC-08` `contract` The reserved screenshots directory exists empty at the app root. `src: Deployment contract line 6`
- [ ] `C-DC-09` `contract` The reserved downloads directory exists empty at the app root. `src: Deployment contract line 6`
- [ ] `C-DC-10` `contract` A production build is served behind a static server. `src: Deployment contract line 7`
- [ ] `C-DC-11` `contract` The server keeps running after the session ends. `src: Deployment contract line 8`
- [ ] `C-DC-12` `contract` The server is never a child of the shell. `src: Deployment contract line 8`
- [ ] `C-DC-13` `contract` The server binds the all-interfaces address rather than loopback. `src: Deployment contract line 9`
- [ ] `C-DC-14` `contract` The named backing services are never downloaded. `src: Deployment contract line 10`
- [ ] `C-DC-15` `contract` The named backing services are never started by the app. `src: Deployment contract line 10`
- [ ] `C-DC-16` `constraint` No edge function is used. `src: Deployment contract line 11`
- [ ] `C-DC-17` `constraint` No persistent volume is declared. `src: Deployment contract line 12`
- [ ] `C-DC-18` `constraint` No custom network is declared. `src: Deployment contract line 12`
- [ ] `C-DC-19` `data` A paging list endpoint returns rows under a named items field. `src: Deployment contract API shapes note`
- [ ] `C-DC-20` `data` A non-paging list endpoint returns a top-level JSON array. `src: Deployment contract API shapes note`
- [ ] `C-DC-21` `constraint` An invalid call is rejected as a client error rather than a server error. `src: Deployment contract API shapes note`
- [ ] `C-DC-22` `constraint` An invalid call never produces a silent success. `src: Deployment contract API shapes note`
- [ ] `C-DC-23` `contract` Bearer auth is required on every endpoint beyond the three named exceptions. `src: Deployment contract API shapes note`
- [ ] `C-DC-24` `constraint` A change request exists as a real row readable by a separate connection. `src: Deployment contract no mocks para`
- [ ] `C-DC-25` `constraint` Every seeded principal exists as a real subject in the identity provider. `src: Deployment contract no mocks para`
- [ ] `C-DC-26` `constraint` No in-memory list substitutes for the change request store. `src: Deployment contract no mocks para`
- [ ] `C-DC-27` `constraint` The app never signs a token for itself without the identity provider. `src: Deployment contract no mocks para`

## Pinned literals

| Value | What it is | Item | Stated in |
|---|---|---|---|
| `AUTH_URL` | identity provider environment variable | C-CF-01 | Core features, Auth rule 1 |
| `/api/auth/login` | sign-in endpoint | C-CF-02 | Core features, Auth rule 1 |
| `/product` | public capability tour route | C-CF-18 | Core features, feature 1 rule 5 |
| `/pricing` | public plans route | C-CF-19 | Core features, feature 1 rule 6 |
| `/security` | public security posture route | C-CF-20 | Core features, feature 1 rule 7 |
| `/privacy` | public privacy route | C-CF-22 | Core features, feature 1 rule 8 |
| `/get-cloud` | public enquiry route | C-CF-24 | Core features, feature 1 rule 9 |
| `/sitemap.xml` | sitemap route | C-CF-33 | Core features, feature 1 rule 14 |
| `/robots.txt` | robots route | C-CF-34 | Core features, feature 1 rule 14 |
| `pending` | change request state on submission | C-CF-42 | Core features, feature 2 rule 3 |
| `applied` | terminal change request state after application | C-CF-56 | Core features, feature 2 rule 8 |
| `expired` | terminal change request state after expiry | C-CF-67 | Core features, feature 2 rule 13 |
| `failed` | terminal change request state after a failed application | C-UF-13 | User flow, journey 3 |
| `DATABASE_URL` | datastore environment variable | C-TR-04 | Technical requirements, para 1 |
| `deku-demo-pw-2026` | seeded password for every account | C-DM-03 | Data model, password para |
| `/app/USER_README.md` | credential file path | C-DM-04 | Data model, password para |
| `Northwind Trading` | first seeded organisation | C-DM-23 | Data model, seed para 1 |
| `Forgelab` | second seeded organisation | C-DM-24 | Data model, seed para 1 |
| `payments-prod` | first seeded namespace | C-DM-25 | Data model, seed para 2 |
| `orders-prod` | second seeded namespace | C-DM-26 | Data model, seed para 2 |
| `ledger-prod` | third seeded namespace | C-DM-27 | Data model, seed para 2 |
| `developer@example.com` | seeded developer account | C-DM-28 | Data model, seed para 3 |
| `developer2@example.com` | seeded second-organisation developer account | C-DM-29 | Data model, seed para 3 |
| `namespace-admin@example.com` | seeded namespace admin account | C-DM-30 | Data model, seed para 3 |
| `namespace-admin2@example.com` | seeded second namespace admin account | C-DM-31 | Data model, seed para 3 |
| `owner@example.com` | seeded owner account | C-DM-32 | Data model, seed para 3 |
| `reduce_retention` | reviewable change kind used by the graded journey | C-DM-36 | Data model, seed para 5 |
| `subscription-9f21c4d0` | seeded failed execution workflow identifier | C-DM-39 | Data model, seed para 7 |
| `01J7Y6M2R8` | seeded failed execution run identifier | C-DM-40 | Data model, seed para 7 |
| `APP_PUBLIC_URL` | app origin environment variable | C-DC-01 | Deployment contract, line 1 |
| `4173` | container-internal port | C-DC-02 | Deployment contract, line 1 |
| `/api/health` | health route | C-DC-05 | Deployment contract, line 3 |

### Referenced but not pinned

| What the instruction calls it | Item | Why it matters |
|---|---|---|
| the stated reachability window for a worker poll | C-CF-130 | named as stated with no duration given |
| the stated certificate expiry warning threshold | C-FE-16 | named as stated with no duration given |
| the stated replication lag threshold refusing a silent failover | C-CF-85 | named as stated with no bound given |

## Coverage ledger

| Section | Obligation-bearing sentences | Items produced |
|---|---|---|
| Overview | 3 | 12 |
| User roles | 5 | 22 |
| Core features | 39 | 142 |
| User flow | 7 | 19 |
| UI and UX notes | 3 | 18 |
| Technical requirements | 9 | 20 |
| Data model | 11 | 46 |
| Front-end specification | 5 | 25 |
| Constraints | 2 | 12 |
| Deployment contract | 16 | 27 |
